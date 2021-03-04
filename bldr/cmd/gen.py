"""
`gen` Command

Run a generator to create templates


"""
import os
import shutil

import click

import bldr
import bldr.gen
from bldr.gen.render import CopyTemplatesRender
from bldr.environment import Environment
from bldr.cli import pass_environment

# aliases
join = os.path.join

@click.command("gen", short_help="Run Code Generator")
@click.argument("subcommand", required=True, type=click.STRING)
@click.argument("args", required=False, nargs=-1)
@pass_environment
def cli(ctx: Environment, subcommand: str, args):
    """Generate Templates using the given Generator"""
    ctx.log(f"Running Generator {subcommand}")

    generator_local_path = ctx.generator_path / subcommand / "local"
    if generator_local_path.exists():
        ctx.log(f"Copying local {generator_local_path}")
        copy_render = CopyTemplatesRender(ctx, False)
        copy_render.walk(generator_local_path, ctx.current_generated_path)

       