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
@click.option("-b", "--branch", required=False, type=str)
@click.option("-m", "--module", flag_value=True, help="Add the dependency to the bldr modules folder")
@click.argument("url", required=False, type=str)
@click.argument("path", required=False, type=click.Path())
@pass_environment
def cli(ctx, url, git, branch, module):
    run_cmd(ctx, 'init')

    cd = "deps.add " + str(url) + " . -f" 
    if(module):
        cd += " -m"
    if (branch != None):
        cd += " -b " + branch

    run_cmd(ctx, cd)

    run_cmd(ctx, 'gen.up')

    #change when other-than-git is allowed :)

