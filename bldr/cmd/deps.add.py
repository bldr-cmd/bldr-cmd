"""
`deps.get` Command

"""
from bldr.environment import Environment
import os

from git.objects.submodule.root import RootUpdateProgress

import bldr
import bldr.gen.render
from git import Repo
import click

from bldr.cli import pass_environment, run_cmd
from bldr.gen.render import render
import bldr.dep.env

dotbldr_path = os.path.join(os.path.abspath(os.path.dirname(bldr.__file__)), "dotbldr")


@click.command("deps.add", short_help="Add Dependencies.")
@click.option("-g", "--git", flag_value=True)
@click.option("-b", "--branch", required=False, type=str)
@click.argument("url", required=False, type=str)
@click.argument("path", required=False, type=click.Path())
@pass_environment
def cli(ctx, url, path, git, branch):
    """Get Dependencies"""
    ctx.log(f"Adding Dependency {url} {path}")

    config = {name: dep for (name, dep) in ctx.env['dep']['config'].items()}
    lockfile = {name: dep for (name, dep) in ctx.env['dep']['lock'].items()}

    if git:
        git_add(ctx, config, branch, url, path)

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