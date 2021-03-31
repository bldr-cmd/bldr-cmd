"""
`gen.import` Command

Move any inline templates to the Local Template folder

"""
import click

import bldr.gen
from pathlib import Path
from bldr.gen.render import CopyTemplatesRender
from bldr.environment import Environment
from bldr.cli import pass_environment, cmd
import os
import re

@click.command("gen.import", short_help="Import Non-bldr project as a template")
@click.argument("path", required=True, type=click.Path(resolve_path=True))
@click.option("-t", "--top", is_flag=True, help="Create Top Level Module")
@pass_environment
def cli(ctx: Environment, path: str, top: bool):
    """Copy project to Local"""
    ctx.log(f"Importing {path}")

    generator_name = f"import.{Path(path).name}"
    proj_path = Path(path)
    if top:
        local_path = ctx.proj_path / "local"
    else:
        local_path = ctx.module_path / generator_name / "local"

    local_path.mkdir(parents=True, exist_ok=True)
    
    # Copy Files
    copy_render = ImportTemplatesRender(ctx) 
    copy_render.walk(proj_path, local_path)

    # Save to the generator file
    bldr.gen.add_generator([generator_name], ctx)

    if top:
        ctx.log(f"Import Complete.  Project can now be used as a bldr Module")
    else:
        bldr.gen.cmd(ctx, generator_name)
        ctx.log(f"Import Complete.  Run `bldr gen.up` to update files")



class ImportTemplatesRender(CopyTemplatesRender):
    def __init__(self, ctx: Environment):
        super().__init__(ctx, True)
        self.exts = []
        self.ext_repl = {}
        if 'gen.import' in ctx.env['config']:
            template_exts = ctx.env['config']['gen.import']['template_exts']
            self.exts = template_exts.keys()
            self.ext_repl = template_exts
            
    def replace_vars(self,match):
        return self.replacements[match.group(0)]
    def render(self, source_path: str, destination_path: str):
        (filename, file_ext) = os.path.splitext(destination_path)
        if file_ext in self.exts:
            spath = Path(source_path)
            text = spath.read_text()
            #text = text.replace(text_to_search, replacement_text)
            self.replacements = self.ext_repl[file_ext]
            text = re.sub('|'.join(r'\b%s\b' % re.escape(s) for s in self.replacements), 
                self.replace_vars, text) 
            new_destination = f"{filename}.bldr-j2{file_ext}"
            self.ctx.log(f"Generating {new_destination}")
            dpath = Path(new_destination)
            dpath.write_text(text)
            return True
        else:
            return super().render(source_path, destination_path)
