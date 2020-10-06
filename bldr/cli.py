import os
import sys
import runpy

import click

CONTEXT_SETTINGS = dict(auto_envvar_prefix="BLDR")
VERSION = "0.1.0"

class Environment:
    def __init__(self):
        self.verbose = False
        self.cwd = os.getcwd()
        self.env = {}

    def log(self, msg, *args):
        """Logs a message to stderr."""
        if args:
            msg %= args
        click.echo(msg, file=sys.stderr)

    def vlog(self, msg, *args):
        """Logs a message to stderr only if verbose is enabled."""
        if self.verbose:
            self.log(msg, *args)

pass_environment = click.make_pass_decorator(Environment, ensure=True)
cmd_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), "cmd"))

def cmd(cmd_name):
    cmd_mod_path = os.path.join(cmd_folder, cmd_name + ".py")

    if os.path.exists(cmd_mod_path):
        local_env = runpy.run_path(cmd_mod_path, globals())
        return local_env["cli"]
    else:
        return None

class BldrCLI(click.MultiCommand):
    def list_commands(self, ctx):
        rv = []
        for filename in os.listdir(cmd_folder):
            if filename.endswith(".py"):
                rv.append(filename[:-3])
        rv.sort()
        return rv

    def get_command(self, ctx, cmd_name):
        return cmd(cmd_name)
        
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