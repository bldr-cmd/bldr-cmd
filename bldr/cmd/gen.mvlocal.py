"""
`gen.mvlocal` Command

Move any inline templates to the Local Template folder

"""
import os
import shutil

import bldr
import bldr.gen
import bldr.gen.render

from diff_match_patch import diff_match_patch

from bldr.cli import pass_environment

import click

# aliases
join = os.path.join

@click.command("gen.mvlocal", short_help="Move Inline Templates to Local")
#@click.argument("path", required=False, type=click.Path(resolve_path=True))
@pass_environment
def cli(ctx):
    """Move Inline Templates to Localn"""
    ctx.log(f"Updating Code Generation")

    dotbldr_path = bldr.dotbldr_path()
    proj_path = bldr.proj_path()
    local_path = join(dotbldr_path, "local")

    bldr.ensure_dir(local_path)

    # Move Templates
    move_render = MoveTemplatesRender(ctx, False) 
    move_render.walk(proj_path, local_path)

class MoveTemplatesRender(bldr.gen.render.CommonRender):
    def render(self, source_path: str, destination_path: str):
        # if the destination does not exist, just copy the file
        if 'bldr-' in os.path.basename(source_path):
            self.ctx.log(f"Moving {source_path}")
            shutil.move(source_path, destination_path)
            return True
