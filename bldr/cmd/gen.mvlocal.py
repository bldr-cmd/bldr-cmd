"""
`gen.mvlocal` Command

Move any inline templates to the Local Template folder

"""
import os
import shutil

import bldr
import bldr.gen
import bldr.gen.render

from bldr.environment import Environment
from diff_match_patch import diff_match_patch
from bldr.cli import pass_environment

import click


@click.command("gen.mvlocal", short_help="Move Inline Templates to Local")
#@click.argument("path", required=False, type=click.Path(resolve_path=True))
@pass_environment
def cli(ctx: Environment):
    """Move Inline Templates to Local"""
    ctx.log(f"Updating Code Generation")

    dotbldr_path = ctx.dotbldr_path
    proj_path = ctx.proj_path
    local_path = dotbldr_path.joinpath("local")

    local_path.mkdir(parents=True, exist_ok=True)
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
