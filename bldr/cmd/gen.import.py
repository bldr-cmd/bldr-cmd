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
@click.option("-t", "--top", is_flag=True, help="Create Top Level Module")
@pass_environment
def cli(ctx: Environment, source: str, path: str, top: bool):
    """Copy project to Local"""
    ctx.log(f"Importing {source}")

    generator_name = f"import.{Path(source).name}"
    source_path = Path(source)
    if top:
        local_path = ctx.local_path / "local"
    else:
        local_path = ctx.module_path / generator_name / "local"
    
    if path != None:
        local_path = local_path / path

    local_path.mkdir(parents=True, exist_ok=True)
    
    # Copy Files
    copy_render = ImportTemplatesRender(ctx, top) 
    copy_render.walk(source_path, local_path)

    # Save to the generator file
    bldr.gen.add_generator([generator_name], ctx)

    run_cmd(ctx, 'gen.up')
    if top:
        ctx.log(f"Import Complete.  Project can now be used as a bldr Module")
    else:
        bldr.gen.cmd(ctx, generator_name)
        ctx.log(f"Import Complete.  Run `bldr gen.up` to update files")

def key2ext(key):
    if key[0] == '.':
        return key
    else:
        return '.'+ key

def ext_regex(ext_dict):
    return '|'.join(r'\b%s\b' % re.escape(s) for s in ext_dict)

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

    def __init__(self, ctx: Environment, top: bool):
        super().__init__(ctx, True)
        self.exts = []
        self.ext_repl = {}
        self.exclude_globs = []
        self.renames = {}
        self.rename_regex = None
        self.top = top
        try:
            gen_import = ctx.env['config']['gen']['import']
            if 'renames' in gen_import:
                self.renames = gen_import['renames']
                self.rename_regex = rename_regex(self.renames)
            if 'template_exts' in gen_import:
                template_exts = gen_import['template_exts']
                self.exts = [key2ext(key) for key in template_exts.keys()]
                self.ext_repl = { key2ext(key): value for (key,value) in template_exts.items()}
                self.ext_regex = { key2ext(key): ext_regex(value) for (key,value) in template_exts.items()}
            if 'exclude_globs' in gen_import:
                self.exclude_globs = gen_import['exclude_globs']
        except KeyError:
            pass

            
    def replace_vars(self,match):
        return self.replacements[match.group(0)]

    def rename_path(self,match):
        return self.renames[match.group(0)]

    def render(self, source_path: str, destination_path: str):
        if self.rename_regex != None:
            destination_path = re.sub(self.rename_regex, self.rename_path, destination_path)

        (filename, file_ext) = os.path.splitext(destination_path)
        if file_ext in self.exts:
            spath = Path(source_path)
            text = spath.read_text()
            #text = text.replace(text_to_search, replacement_text)
            self.replacements = self.ext_repl[file_ext]
            text = re.sub(self.ext_regex[file_ext], self.replace_vars, text)
            if self.top:
                new_destination = f"{filename}.bldr-j2.bldr-pass{file_ext}"
            else:
                new_destination = f"{filename}.bldr-j2{file_ext}"
            self.ctx.log(f"Generating {new_destination}")
            dpath = Path(new_destination)
            dpath.write_text(text)
            return True
        else:
            return super().render(source_path, destination_path)
