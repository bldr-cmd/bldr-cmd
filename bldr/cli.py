import os
import sys
import runpy
import glob

import bldr
import click
from bldr.environment import Environment

CONTEXT_SETTINGS = dict(auto_envvar_prefix="BLDR")
VERSION = "0.1.0"

pass_environment = click.make_pass_decorator(Environment, ensure=True)
cmd_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), "cmd"))

def cmd_paths():
    dotbldr_path = bldr.dotbldr_path()
    return  [ f"{dotbldr_path}/cmd", f"{dotbldr_path}/generator/*/cmd", cmd_folder ]

def cmd_path(cmd_name):
    """ 
    Find the path to the given command name 

    The order of search:
    .bldr/cmd
    .bldr/generator/*/cmd
    bldr/cmd
    """

    for basepath in cmd_paths():
        files = glob.glob(f"{basepath}/{cmd_name}.py")
        if len(files) > 0:
            files.sort()
            return files[0]

    return None

def cmd(cmd_name):
    cmd_mod_path = cmd_path(cmd_name)

    if cmd_mod_path != None:
        local_env = runpy.run_path(cmd_mod_path, globals())
        return local_env["cli"]
    else:
        return None

class BldrCLI(click.MultiCommand):
    def list_commands(self, ctx):
        rv = []
        for basepath in cmd_paths():
            files = glob.glob(f"{basepath}/*.py")
            for fpath in files:
                (_dir, filename) = os.path.split(fpath)
                filename = filename[:-3]
                if filename not in ['__init__']:
                    rv.append(filename)
        
        rv = sorted(set(rv))
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