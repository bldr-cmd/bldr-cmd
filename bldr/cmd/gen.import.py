"""
`gen.import` Command

Move any inline templates to the Local Template folder

"""
import click

import bldr.gen
from pathlib import Path
from bldr.gen.render import CopyTemplatesRender
from bldr.environment import Environment
from bldr.cli import pass_environment, run_cmd
import os
import re

@click.command("gen.import", short_help="Import Non-bldr project as a template")
@click.argument("source", required=True, type=click.Path(resolve_path=True))
@click.option("-p", "--path", type=click.Path(), help="Relative Destination Path")
@click.option("-t", "--as-template", is_flag=True, help="Import the project as template")
@pass_environment
def cli(ctx: Environment, source: str, path: str, as_template: bool):
    """Copy project to Local Templates"""
    ctx.log(f"Importing {source}")

    generator_name = f"import.{Path(source).name}"
    source_path = Path(source)
    if as_template:
        local_path = ctx.local_path / "template"
    else:
        local_path = ctx.brick_path / generator_name / "template"
        if local_path.exists():
            bldr.util.rmtree(local_path)
    
    if path != None:
        local_path = local_path / path

    local_path.mkdir(parents=True, exist_ok=True)
    
    # Copy Files
    copy_render = ImportTemplatesRender(ctx, as_template) 
    copy_render.walk(source_path, local_path)

    # Save to the generator file
    bldr.gen.add_generator(['gen.import', generator_name, source, path, as_template], ctx)
    
    if not as_template:
        bldr.gen.cmd(ctx, generator_name)

    run_cmd(ctx, 'gen.up')
    ctx.log(f"Import Complete.")

def key2ext(key):
    if key[0] == '.':
        return key
    else:
        return '.'+ key

def regex_name(regex_str : str):
    val = hash(regex_str)
    if val < 0:
        val = -val
    return "r" + str(val)

def is_regex_str(regex_str: str):
    return regex_str.startswith('r/') and regex_str.endswith('/')

def regex_strip_r(regex_str: str):
    if is_regex_str(regex_str):
        return regex_str[2:-1]
    return regex_str

def regex_for(regex_str: str):
    name = regex_name(regex_str)
    if is_regex_str(regex_str):
        return r'(?P<%s>%s)' % (name, regex_strip_r(regex_str))
    else:
        return r'(?P<%s>\b%s\b)' % (name, re.escape(regex_str))

def regex_orig(regex_str: str):
    if is_regex_str(regex_str):
        return re.compile(r'%s' % regex_strip_r(regex_str))
    else:
        return None

def ext_regex(ext_dict):
    return re.compile('|'.join( regex_for(s) for s in ext_dict))

def named_regex_dicts(regex_dic: dict):
    return {regex_name(key): (regex_orig(key), value) for (key, value) in regex_dic.items()}


def rename_regex(rename_dict):
    return '|'.join(r'\b%s\b' % re.escape(s) for s in rename_dict)

class ImportTemplatesRender(CopyTemplatesRender):
    def filter_file(self, root: str, file: str):
        path = Path(root) / file
        for glob in self.exclude_globs:
            if path.match(glob):
                self.ctx.vlog(f"Skipping File {path}")
                return False
        return True

    def filter_dir(self, root: str, dir: str):
        path = Path(root) / dir
        for glob in self.exclude_globs:
            if path.match(glob):
                self.ctx.vlog(f"Skipping Dir {path}")
                return False
        return True

    def __init__(self, ctx: Environment, as_template: bool):
        super().__init__(ctx, True)
        self.exts = []
        self.to_template_exts = []
        self.ext_repl = {}
        self.ext_regex = {}
        self.exclude_globs = []
        self.renames = {}
        self.rename_regex = None
        self.as_template = as_template
        try:
            gen_import = ctx.env['config']['gen']['import']
            if 'renames' in gen_import:
                self.renames = named_regex_dicts(gen_import['renames'])
                self.rename_regex = re.compile(ext_regex(gen_import['renames']))
            if 'replace_exts' in gen_import:
                replace_exts = gen_import['replace_exts']
                self.exts = self.exts + [key2ext(key) for key in replace_exts.keys()]
                self.ext_repl.update({ key2ext(key): named_regex_dicts(value) for (key,value) in replace_exts.items()})
                self.ext_regex.update({ key2ext(key): ext_regex(value) for (key,value) in replace_exts.items()})
            if 'template_exts' in gen_import:
                template_exts = gen_import['template_exts']
                self.to_template_exts = [key2ext(key) for key in template_exts.keys()]
                self.exts = self.exts + (self.to_template_exts)
                self.ext_repl.update({ key2ext(key): named_regex_dicts(value) for (key,value) in template_exts.items()})
                self.ext_regex.update({ key2ext(key): ext_regex(value) for (key,value) in template_exts.items()})
            if 'exclude_globs' in gen_import:
                self.exclude_globs = gen_import['exclude_globs']
        except KeyError:
            pass

            
    def replace_vars(self,match: re.Match):
        groupname = match.lastgroup
        (orig_regex, replacement) = self.replacements[groupname]
        if orig_regex == None:
            return replacement
        else:
            found_str = match.groupdict()[groupname]
            return orig_regex.sub(replacement, found_str)

    def rename_path(self,match):
        groupname = match.lastgroup
        (orig_regex, replacement) = self.renames[groupname]
        if orig_regex == None:
            return replacement
        else:
            found_str = match.groupdict()[groupname]
            return orig_regex.sub(replacement, found_str)

    def render(self, source_path: str, destination_path: str):
        if self.rename_regex != None:
            destination_path = self.rename_regex.sub(self.rename_path, destination_path)

        (filename, file_ext) = os.path.splitext(destination_path)
        if file_ext in self.exts:
            spath = Path(source_path)
            text = spath.read_text()
            #text = text.replace(text_to_search, replacement_text)
            self.replacements = self.ext_repl[file_ext]
            text = self.ext_regex[file_ext].sub(self.replace_vars, text)
            new_destination = destination_path
            if file_ext in self.to_template_exts:
                if self.as_template:
                    new_destination = f"{filename}.bldr-j2.bldr-pass{file_ext}"
                else:
                    new_destination = f"{filename}.bldr-j2{file_ext}"
            self.ctx.log(f"Generating {new_destination}")
            dpath = Path(new_destination)
            dpath.write_text(text)
            return True
        else:
            return super().render(source_path, destination_path)
