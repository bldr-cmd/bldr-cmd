"""
`gen` Command

Run a generator to create templates


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

# aliases
join = os.path.join

@click.command("gen", short_help="Run Code Generator")
#@click.argument("path", required=False, type=click.Path(resolve_path=True))
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

class CopyTemplatesRender(bldr.gen.render.CommonRender):
    def render(self, source_path: str, destination_path: str):
        # if the destination does not exist, just copy the file
        self.ctx.log(f"Creating {source_path}")
        shutil.copy(source_path, destination_path)
        return True            