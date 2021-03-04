import os
import runpy

import click

from bldr.environment import Environment

CONTEXT_SETTINGS = dict(auto_envvar_prefix="BLDR")
VERSION = "0.1.0"

pass_environment = click.make_pass_decorator(Environment, ensure=True)
cmd_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), "cmd"))

def cmd(ctx: Environment, cmd_name: str):
    cmd_mod_path = ctx.cmd_path(cmd_name)

    if cmd_mod_path != None:
        local_env = runpy.run_path(str(cmd_mod_path), globals())
        return local_env["cli"]
    else:
        return None

class BldrCLI(click.MultiCommand):
    def list_commands(self, ctx: Environment):
        rv = []
        for files in ctx.cmd_path_globs(f"*.py"):
            for fpath in files:
                (_dir, filename) = os.path.split(fpath)
                filename = filename[:-3]
                if filename not in ['__init__']:
                    rv.append(filename)
        
        rv = sorted(set(rv))
        return rv

    def get_command(self, ctx: click.Context, cmd_name: str):
        return cmd(Environment(), cmd_name)
        
@click.command(cls=BldrCLI, context_settings=CONTEXT_SETTINGS)
@click.option(
    "--cwd",
    type=click.Path(exists=True, file_okay=False, resolve_path=True),
    help="Changes the folder to operate on.",
)

@click.option("-v", "--verbose", is_flag=True, help="Enables verbose mode.")
@pass_environment
def cli(ctx, verbose, cwd):
    f"""bldr - {VERSION}"""
    ctx.verbose = verbose
    if cwd is not None:
        ctx.cwd = cwd