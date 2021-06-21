"""
`rm` Command

Remove a directory recursively

"""
import click

import bldr.util

from bldr.environment import Environment
from bldr.cli import pass_environment


@click.command("rm", short_help="Remove directory recursively")
@click.argument("target", required=True, type=click.Path(resolve_path=True))
@pass_environment
def cli(ctx: Environment, target: str):
    """
    This is a windows safe command to remove a directory 
    
    Removing directories with read-only files (like a .git folder) is extremely hard 
    in windows
    """
    ctx.log(f"Removing {target}")
    bldr.util.rmtree(target)

       