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


@click.command("new", short_help="Add new dependency via url")
@click.option("-g", "--git", flag_value=True)
@click.option("-b", "--branch", required=False, type=str)
@click.option("-k", "--brick", flag_value=True, help="Add the dependency to the bldr modules folder")
@click.argument("url", required=False, type=str)
@pass_environment
def cli(ctx, url, git, branch, brick):
    run_cmd(ctx, 'init')
    run_cmd(ctx, 'deps.add', branch=branch, brick=brick, force=True, path=".", url=url)
    run_cmd(ctx, 'gen.up')

