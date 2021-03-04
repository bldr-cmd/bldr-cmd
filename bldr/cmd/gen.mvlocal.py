"""
`gen.mvlocal` Command

Move any inline templates to the Local Template folder

"""

import click

from bldr.gen.render import MoveTemplatesRender
from bldr.environment import Environment
from bldr.cli import pass_environment


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


