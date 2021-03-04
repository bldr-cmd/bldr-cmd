"""
`example_generator` Command

Regenerate Templates

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

@click.command("example_generator", short_help="Create Template files")
@click.argument("destdir", required=False, type=click.Path(resolve_path=True))
@pass_environment
def cli(ctx, destdir):
    """Generate Template Files in parent project"""

    bldr.ensure_dir(destdir)
