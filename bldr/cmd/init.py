"""
`init` Command

"""
import os
import click

import bldr
import bldr.dep
import bldr.gen.render

from bldr.environment import Environment
from bldr.gen.render import CopyTemplatesRender
from bldr.cli import pass_environment, run_cmd

dotbldr_path = os.path.join(os.path.abspath(os.path.dirname(bldr.__file__)), "dotbldr")

@click.command("init", short_help="Initializes a project.")
@click.argument("path", required=False, type=click.Path(resolve_path=True))
@pass_environment
def cli(ctx : Environment, path):
    """Initializes a project."""
    if path is None:
        path = ctx.cwd
    ctx.log(f"Initialized the project in {click.format_filename(path)}")
    new_dir = os.path.join(os.path.curdir, ".bldr")
    ctx.vlog(f" {click.format_filename(dotbldr_path)} -> {new_dir}")
    
    copy_render = CopyTemplatesRender(ctx, True) 
    copy_render.walk(dotbldr_path, new_dir)
    
    # NOTE:  ctx cannot be used prior to this point!!
    run_cmd(ctx, 'gen.up')
    bldr.dep.sync_githooks(ctx)
