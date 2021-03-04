"""
`gen.import` Command

Move any inline templates to the Local Template folder

"""
import click

from pathlib import Path
from bldr.gen.render import CopyTemplatesRender
from bldr.environment import Environment
from bldr.cli import pass_environment, cmd


@click.command("gen.import", short_help="Import Non-bldr project as a template")
@click.argument("path", required=True, type=click.Path(resolve_path=True))
@pass_environment
def cli(ctx: Environment, path: str):
    """Copy project to Local"""
    ctx.log(f"Importing {path}")

    proj_path = Path(path)
    local_path = ctx.local_path

    local_path.mkdir(parents=True, exist_ok=True)
    
    # Copy Files
    copy_render = CopyTemplatesRender(ctx, True) 
    copy_render.walk(proj_path, local_path)

    ctx.log(f"Import Complete.  Run `bldr gen.up` to update files")

