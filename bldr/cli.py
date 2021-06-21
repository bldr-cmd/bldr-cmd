import os
import runpy

import click

from bldr.environment import Environment

CONTEXT_SETTINGS = dict(auto_envvar_prefix="BLDR")
VERSION = "0.15.1"

pass_environment = click.make_pass_decorator(Environment, ensure=True)
cmd_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), "cmd"))


def run_cmd(ctx: Environment, cmd_name: str, *args, **kwargs):
    click_ctx = click.get_current_context()
    click_ctx.invoke(cmd(ctx,cmd_name), *args, **kwargs)
    
def cmd(ctx: Environment, cmd_name: str):
    cmd_mod_path = ctx.cmd_path(cmd_name)

    if cmd_mod_path != None:
        local_env = runpy.run_path(str(cmd_mod_path), globals())
        return local_env["cli"]
    else:
        return None

class BldrCLI(click.MultiCommand):
    """
    bldr help
    """
    def list_commands(self, click_ctx: click.Context):
        rv = []
        ctx = Environment()
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
        
@click.command(cls=BldrCLI, context_settings=CONTEXT_SETTINGS, invoke_without_command=True, help='bldr version ' + VERSION)
@click.option("-v", "--verbose", envvar='BLDR_VERBOSE', is_flag=True, help="Enables verbose mode.")
@click.option("--version", is_flag=True, help="Prints Version")
@pass_environment
def cli(ctx, verbose, version):
    f"""bldr - {VERSION}"""
    ctx.verbose = verbose

    if version:
        ctx.log("bldr Version " + VERSION)