"""
`deps.get` Command

"""
from bldr.environment import Environment
import os

from git.objects.submodule.root import RootUpdateProgress

import bldr
import bldr.gen.render

from git import Repo

dotbldr_path = os.path.join(os.path.abspath(os.path.dirname(bldr.__file__)), "dotbldr")

from bldr.cli import pass_environment
from bldr.gen.render import render
import click

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

    # Render .gitmodules
    render(ctx.env, ctx.local_path / '.gitmodules.bldr-j2', ctx.current_path / '.gitmodules', False)
    render(ctx.env, ctx.local_path / '.gitmodules.bldr-j2', ctx.proj_path / '.gitmodules', False)

    git_path = ctx.proj_path / '.git'
    if not git_path.exists():
        ctx.log("No .git folder")
        return -1
    
    repo = Repo(git_path)
    
    submodules = {name: dep for (name, dep) in ctx.env['dep']['lock'].items() if dep['type'] == 'git'}

    ctx.log("Add missing git modules")
    for (subname, submod) in submodules.items():
        module_path = git_path / "modules" / submod['path']
        if not module_path.exists():
            ctx.log(f"submodule create {subname} {submod['path']} {submod['url']}")
            #repo.create_submodule(subname, submod['path'], url=submod['url'], no_checkout=True)
            output = repo.git.submodule('add', submod['url'], submod['path'])
            ctx.log(output)

    ctx.log("Updating git modules")
    output = repo.git.submodule('update', '--init', '--recursive')
    ctx.log(output)
    #progress = DepsUpdateProgress(ctx)
    #repo.submodule_update(init=True, recursive=True, progress=progress)
    # for submodule in repo.submodules:
    #     ctx.log(submodule.name)
    #     submodule.update(init=True, recursive=True)
