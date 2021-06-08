
"""
`deps.get` Command

"""
from bldr.environment import Environment
import os
import sys
from git.objects.submodule.root import RootUpdateProgress

import bldr
import bldr.gen.render
import bldr.util
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
@click.option("-l", "--link", flag_value=True)
@click.option("-b", "--branch", required=False, type=str)
@click.option("-f", "--force", flag_value=True, help="Force the creation of the dependency")
@click.option("-k", "--brick", flag_value=True, help="Add the dependency to the bldr brick folder")
@click.argument("url", required=False, type=str)
@click.argument("path", required=False, type=click.Path())
@pass_environment
def cli(ctx, url, path, git, link, branch, brick, force):
    """Get Dependencies"""
    ctx.log(link)
        
    config = ctx.env['dep']['config']

    if git and link:
        ctx.log("Selected git and link, will save as symbolick link, not module")
        git = False

    if git == False and link == False:
        git = True



    if brick:
        if path == None:
            path = ctx.brick_path
        else:
            path = ctx.brick_path / path

    ctx.log(f"Adding Dependency {url} {path}")


    if url[7:] == "file://" or link:
        # Normalize the path name
        full_path = Path(path).absolute()
        if full_path.exists() and full_path.is_dir:
            repo_name = url[''.join(url).rindex('/')+1:]
            if full_path.name != repo_name:
                full_path = full_path / repo_name
            else:
                ctx.log("Path Already Exists")
                exit -1


    else:

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

    

    # Default to using git.  
    #  More important when others are added
    if url[:7] == "file://":
        git_add2(ctx, config, branch, url, path, force)

    elif link:
        add_link(ctx, config, branch, url, path, force)

    else:
        git_add(ctx, config, branch, url, path, force)

    if ctx.verbose:
        ctx.vlog("Saving Config:" + json.dumps(config))      

    bldr.dep.env.save_config(ctx.dotbldr_path, config)
    run_cmd(ctx, 'deps.get')


def git_add(ctx, config, branch, url, path, force):
    # path must only have '/' to work with git!!
    path = path.replace('\\', '/')

    if branch == None:
        branch = 'master'

    git_path = ctx.proj_path / '.git'
    if not git_path.exists():
        ctx.log("No .git folder")
        exit(-1)

    module_path = git_path / "modules" / path
    if module_path.exists():
        if force:
            bldr.util.rmtree(module_path)
        else:
            ctx.log("Module already exists at that location.  Rerun with --force to remove it")
            exit(-1)   

    repo = Repo(git_path) 
    ctx.log(f"submodule create {path} {url}")

    output = repo.git.submodule('add', url, path)
    ctx.log(output)





    config[path] = {
        'type': "git",
        'branch': branch,
        'path': path,
        'url': url,
    }




def git_add2(ctx, config, branch, url, path, force):

    # path must only have '/' to work with git!!
    path = path.replace('\\', '/')

    if branch == None:
        branch = 'master'

    git_path = ctx.proj_path / '.git'
    if not git_path.exists():
        ctx.log("No .git folder")
        exit(-1)

    module_path = git_path / "modules" / path
    if module_path.exists():
        if force:
            bldr.util.rmtree(module_path)
        else:
            ctx.log("Module already exists at that location.  Rerun with --force to remove it")
            exit(-1)   

    repo = Repo(git_path) 
    ctx.log(f"submodule create {path} {url}")
    #os.system("git clone " + url[7:])


    config[path] = {
        'type': "git",
        'branch': branch,
        'path': path,
        'url': url[7:],
    }

def add_link(ctx, config, branch, url, path, force):
    path = path.replace('\\', '/')

    ctx.log(f"Symbolic link create {path} {url}")



    config[path] = {
        'type': "link",
        'path': path,
        'link': url,
    }