"""
`deps.get` Command

"""
from bldr.environment import Environment
import os

from git.objects.submodule.root import RootUpdateProgress

import bldr
import bldr.gen.render
import giturlparse

from git import Repo
from pathlib import Path
import click

import json

from bldr.cli import pass_environment, run_cmd
from bldr.gen.render import render
import bldr.dep.env

dotbldr_path = os.path.join(os.path.abspath(os.path.dirname(bldr.__file__)), "dotbldr")


@click.command("deps.add", short_help="Add Dependencies.")
@click.option("-g", "--git", flag_value=True)
@click.option("-b", "--branch", required=False, type=str)
@click.option("-f", "--force", flag_value=True, help="Force the creation of the dependency")
@click.option("-m", "--module", flag_value=True, help="Add the dependency to the bldr modules folder")
@click.argument("url", required=False, type=str)
@click.argument("path", required=False, type=click.Path())
@pass_environment
def cli(ctx, url, path, git, branch, module, force):
    """Get Dependencies"""
    

    config = ctx.env['dep']['config']

    if module:
        if path == None:
            path = ctx.module_path
        else:
            path = ctx.module_path / path

    ctx.log(f"Adding Dependency {url} {path}")

    # Normalize the path name
    full_path = Path(path).absolute()
    if full_path.exists() and full_path.is_dir:
        repo_name = giturlparse.parse(url).name
        if full_path.name != repo_name:
            full_path = full_path / repo_name
        else:
            ctx.log("Path Already Exists")
            exit -1

    cwd = Path('.').absolute()
    path = str(full_path.relative_to(cwd))

    if git:
        git_add(ctx, config, branch, url, path)

    if ctx.verbose:
        ctx.vlog("Saving Config:" + json.dumps(config))      

    bldr.dep.env.save_config(ctx.dotbldr_path, config)
    run_cmd(ctx, 'deps.get')


def git_add(ctx, config, branch, url, path):
    if branch == None:
        branch = 'master'

    git_path = ctx.proj_path / '.git'
    if not git_path.exists():
        ctx.log("No .git folder")
        exit -1

    repo = Repo(git_path) 
    ctx.log(f"submodule create {path} {path} {url}")
    output = repo.git.submodule('add', url, path)
    ctx.log(output)

    config[path] = {
        'type': "git",
        'branch': branch,
        'path': path,
        'url': url,
    }