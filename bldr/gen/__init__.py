import os
import toml
from typing import Callable

import bldr.gen.env
from bldr.environment import Environment
from bldr.gen.render import CopyTemplatesRender

def cmd(ctx: Environment, subcommand: str, args = None):
    module_local_path = ctx.module_path / subcommand / "local"
    if module_local_path.exists():
        ctx.log(f"Copying local {module_local_path}")
        copy_render = CopyTemplatesRender(ctx, False)
        copy_render.walk(module_local_path, ctx.current_generated_path)

def add_generator(generator: list, ctx: Environment = Environment()):
    config = {}
    if 'gen' in ctx.env:
        config = ctx.env['gen']
    if 'generators' not in config:
        config['generators'] = []

    config['generators'].append(generator)
    bldr.gen.env.save(config, ctx.dotbldr_path)


def common_filter_file(root, file):
    return True

def common_filter_dir(root, dir):
    # Skip any folder that contains a .git
    if os.path.exists(os.path.join(root,dir,".git")):
        return False
    if dir in ['.bldr', '.git']:
        return False
    return True

def walk_local(source_root_dir: str, destination_root_dir: str, render: Callable[[str, str], bool], filter_file: Callable[[str, str], bool], filter_dir: Callable[[str, str], bool]):
    #print(f"source_root_dir {source_root_dir}")
    for root, dirs, files in os.walk(source_root_dir, topdown=True):
        dirs[:] = [d for d in dirs if common_filter_dir(root, d) and filter_dir(root, d)]
        destdir = root.replace(source_root_dir, destination_root_dir)
        #print(f"destdir {destdir}")
        if not os.path.exists(destdir):
            os.makedirs(destdir)
        for f in files:
            #print(f"f {f}")
            if common_filter_file(root, f) and filter_file(root, f):
                source = os.path.join(root,f)
                destination = source.replace(source_root_dir, destination_root_dir)
                render(source, destination)

def walk_triple(source_root_dir: str, previous_root_dir: str, destination_root_dir: str, render: Callable[[str, str, str], bool], filter_file: Callable[[str, str], bool], filter_dir: Callable[[str, str], bool]):
    #print(f"source_root_dir {source_root_dir}")
    for root, dirs, files in os.walk(source_root_dir, topdown=True):
        dirs[:] = [d for d in dirs if common_filter_dir(root, d) and filter_dir(root, d)]
        destdir = root.replace(source_root_dir, destination_root_dir)
        #print(f"destdir {destdir}")
        if not os.path.exists(destdir):
            os.makedirs(destdir)
        for f in files:
            #print(f"f {f}")
            if common_filter_file(root, f) and filter_file(root, f):
                source = os.path.join(root,f)
                destination = source.replace(source_root_dir, destination_root_dir)
                previous = source.replace(source_root_dir, previous_root_dir)
                render(source, previous, destination)