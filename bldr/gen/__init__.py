import os
from typing import Callable

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
    print(f"source_root_dir {source_root_dir}")
    for root, dirs, files in os.walk(source_root_dir, topdown=True):
        dirs[:] = [d for d in dirs if common_filter_dir(root, d) and filter_dir(root, d)]
        destdir = root.replace(source_root_dir, destination_root_dir)
        print(f"destdir {destdir}")
        if not os.path.exists(destdir):
            os.makedirs(destdir)
        for f in files:
            print(f"f {f}")
            if common_filter_file(root, f) and filter_file(root, f):
                source = os.path.join(root,f)
                destination = source.replace(source_root_dir, destination_root_dir)
                render(source, destination)

def walk_triple(source_root_dir: str, previous_root_dir: str, destination_root_dir: str, render: Callable[[str, str, str], bool], filter_file: Callable[[str, str], bool], filter_dir: Callable[[str, str], bool]):
    print(f"source_root_dir {source_root_dir}")
    for root, dirs, files in os.walk(source_root_dir, topdown=True):
        dirs[:] = [d for d in dirs if common_filter_dir(root, d) and filter_dir(root, d)]
        destdir = root.replace(source_root_dir, destination_root_dir)
        print(f"destdir {destdir}")
        if not os.path.exists(destdir):
            os.makedirs(destdir)
        for f in files:
            print(f"f {f}")
            if common_filter_file(root, f) and filter_file(root, f):
                source = os.path.join(root,f)
                destination = source.replace(source_root_dir, destination_root_dir)
                previous = source.replace(source_root_dir, previous_root_dir)
                render(source, previous, destination)