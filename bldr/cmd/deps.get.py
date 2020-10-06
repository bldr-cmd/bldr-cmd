"""
`deps.get` Command

"""
import os

import bldr
import bldr.gen.render

import sh

dotbldr_path = os.path.join(os.path.abspath(os.path.dirname(bldr.__file__)), "dotbldr")

from bldr.cli import pass_environment

import click


@click.command("deps.get", short_help="Get Dependencies.")
#@click.argument("path", required=False, type=click.Path(resolve_path=True))
@pass_environment
def cli(ctx):
    """Get Dependencies"""
    ctx.log(f"Getting Dependencies")
