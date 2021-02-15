"""
`init` Command

"""
import os


import bldr
import bldr.gen.render

dotbldr_path = os.path.join(os.path.abspath(os.path.dirname(bldr.__file__)), "dotbldr")

from bldr.cli import pass_environment

import click


@click.command("init", short_help="Initializes a repo.")
@click.argument("path", required=False, type=click.Path(resolve_path=True))
@pass_environment
def cli(ctx, path):
    """Initializes a repository."""
    if path is None:
        path = ctx.cwd
    ctx.log(f"Initialized the repository in {click.format_filename(path)}")
    new_dir = os.path.join(os.path.curdir, ".bldr")
    ctx.log(f" {click.format_filename(dotbldr_path)} -> {new_dir}")
    bldr.gen.render.walk(ctx, dotbldr_path, new_dir)
  
