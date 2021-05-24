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


from pathlib import Path



dotbldr_path = os.path.join(os.path.abspath(os.path.dirname(bldr.__file__)), "dotbldr")

class DepsUpdateProgress(RootUpdateProgress):
    def __init__(self, ctx: Environment):
        super().__init__()
        self.ctx = ctx

    def update(self, op_code, cur_count, max_count, message):
        #self.ctx.log(f"update {op_code} {cur_count} {max_count} {message}")
        self.ctx.log(f"{cur_count}/{max_count} {message}")
        

@click.command("deps.get", short_help="Get Dependencies.")
#@click.argument("path", required=False, type=click.Path(resolve_path=True))
@pass_environment
def cli(ctx):
    """Get Dependencies"""
    ctx.log(f"Getting Dependencies")

    git_path = Path(ctx.proj_path) / '.git'

    ctx.dotbldr_path / 'dependecy.toml'
    if not git_path.exists():
        ctx.log("No .git folder")
        return -1
    
    bldr.dep.sync_githooks(ctx)
    repo = Repo(git_path)
    
    config = {name: dep for (name, dep) in ctx.env['dep']['config'].items()}
    lockfile = {name: dep for (name, dep) in ctx.env['dep']['lock'].items()}
    
    # if ctx.verbose:
    #     ctx.vlog("Current Config:" + json.dumps(config))
    #     ctx.vlog("Current Lock:" + json.dumps(lockfile))


    # Remove deps not in the config file
    lockfile = {name: dep for (name, dep) in lockfile.items() if name in config}

    # Add an new deps from config file
    lockfile.update(config)

    gitlock = {name: dep for (name, dep) in lockfile.items() if dep['type'] == 'git'}

    ctx.log("Add missing git modules")
    for (subname, lock_info) in gitlock.items():
        module_path = Path(git_path) / "modules" / lock_info['path']
        if not module_path.exists():
            ctx.log(f"submodule create {subname} {lock_info['path']} {lock_info['url']}")
            #repo.create_submodule(subname, lock_info['path'], url=lock_info['url'], no_checkout=True)
            output = repo.git.submodule('add', lock_info['url'], lock_info['path'])
            ctx.log(output)

    ctx.log("Updating git modules")
    output = repo.git.submodule('update', '--init', '--recursive')
    ctx.log(output)
    #progress = DepsUpdateProgress(ctx)
    #repo.submodule_update(init=True, recursive=True, progress=progress)
    for submodule in repo.submodules:
        sha = submodule.hexsha
        
        # Create a lock entry if the submodule was added another way
        if submodule.name not in lockfile:
            ctx.vlog("{submodule.name} not in lockfile, skipping")
            continue
            # lock_info = {
            #     'type': 'git',
            #     'path': submodule.name,
            #     'branch': submodule.branch,
            #     #'url': submodule.url
            # }
            # lockfile[submodule.name] = lock_info

        lock_info = lockfile[submodule.name]
        lock_info['sha'] = sha

        if 'branch' in lock_info:
            branch = lock_info['branch']
            sub_path = Path(ctx.proj_path) / lock_info['path']
            subrepo = submodule.module()

            ctx.log(f"Setting {submodule.name} {submodule.branch} {submodule.hexsha}")
            subrepo.git.checkout(branch)
            subrepo.git.reset('--hard', sha)

    if ctx.verbose:
        ctx.vlog("Saving Lock:" + json.dumps(lockfile))

    bldr.dep.env.save_lock(ctx.dotbldr_path, lockfile)