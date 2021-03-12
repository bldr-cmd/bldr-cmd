import os
import toml
from typing import Callable

from bldr.environment import Environment
from bldr.gen.render import CopyTemplatesRender

def cmd(ctx: Environment, subcommand: str, args = None):
    module_local_path = ctx.module_path / subcommand / "local"
    if module_local_path.exists():
        ctx.log(f"Copying local {module_local_path}")
        copy_render = CopyTemplatesRender(ctx, False)
        copy_render.walk(module_local_path, ctx.current_generated_path)

def config(ctx: Environment = Environment()):
    return toml.load(f"{ctx.dotbldr_path}/generated.toml")

def save_config(generated_toml: dict, ctx: Environment = Environment()):
    with open(f"{ctx.dotbldr_path}/generated.toml", 'w') as toml_file:
        return toml.dump(generated_toml, toml_file)

def add_generator(generator: str, ctx: Environment = Environment()):
    config_toml = config(ctx)
    if 'generators' not in config_toml:
        config_toml['generators'] = []

    config_toml['generators'].append(generator)
    save_config(config_toml, ctx)


def common_filter_file(root, file):
    return True

def common_filter_dir(root, dir):
    # Skip any folder that contains a .git
    if os.path.exists(os.path.join(root,dir,".git")):
        return False
    if dir == ".bldr":
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