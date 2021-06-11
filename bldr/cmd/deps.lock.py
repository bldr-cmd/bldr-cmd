"""
`deps.get` Command

"""
from bldr.environment import Environment
import os
import json

from git.objects.submodule.root import RootUpdateProgress

import bldr
import bldr.gen.render
from git import Repo
import click

from bldr.cli import pass_environment
from bldr.gen.render import render
import bldr.dep.env

dotbldr_path = os.path.join(os.path.abspath(os.path.dirname(bldr.__file__)), "dotbldr")

class DepsUpdateProgress(RootUpdateProgress):
    def __init__(self, ctx: Environment):
        super().__init__()
        self.ctx = ctx

    def update(self, op_code, cur_count, max_count, message):
        #self.ctx.log(f"update {op_code} {cur_count} {max_count} {message}")
        self.ctx.log(f"{cur_count}/{max_count} {message}")
        

@click.command("deps.lock", short_help="Lock Dependencies.")
@click.option("--staged", flag_value=True)
#@click.argument("path", required=False, type=click.Path(resolve_path=True))
@pass_environment
def cli(ctx, staged):
    """
    Locks Dependencies

    This hook will check to see if any submodules have changed record their new SHA 
    to the lock file
    """

    git_path = ctx.proj_path / '.git'
    if not git_path.exists():
        ctx.log("No .git folder")
        return -1
    
    repo = Repo(git_path)
    
    config = {name: dep for (name, dep) in ctx.env['dep']['config'].items()}
    lockfile = {name: dep for (name, dep) in ctx.env['dep']['lock'].items()}

    # Remove deps not in the config file
    lockfile = {name: dep for (name, dep) in lockfile.items() if name in config}

    # Add an new deps from config file
    for name in config:
        if name not in lockfile:
            lockfile[name] = config[name]

    gitlock = {name: dep for (name, dep) in lockfile.items() if dep['type'] == 'git'}

    if staged:
        # Update Locks from staging
        try:
            staged_files = repo.index.diff("HEAD")
            for staged in staged_files:
                if staged.a_path in gitlock:
                    lock_info = lockfile[staged.a_path]
                    lock_info['sha'] = staged.a_blob.hexsha
        except:
            pass
    
    if ctx.verbose:
        ctx.vlog("Saving Lock:" + json.dumps(lockfile))

    bldr.dep.env.save_lock(ctx.dotbldr_path, lockfile)