import os
from typing import Callable

def common_filter_file(root, file):
    return True

def common_filter_dir(root, dir):
    # Skip any folder that contains a .git
    if os.path.exist(os.path.join(root,dir,".git")):
        return False
    return True

def walk_local(template_root_dir: str, source_root_dir: str, render: Callable[[str, str], bool], filter_file: Callable[[str, str], bool], filter_dir: Callable[[str, str], bool]):
    for root, dirs, files in os.walk(template_root_dir, topdown=True):
        dirs[:] = [d for d in dirs if common_filter_dir(root, d) and filter_dir(root, d)]
        destdir = root.replace(template_root_dir, source_root_dir)
        if not os.path.exists(destdir):
            os.makedirs(os.path.dirname(destdir))
        for f in files:
            if common_filter_file(root, f) and filter_file(root, f):
                source = os.path.join(root,f)
                destination = source.replace(template_root_dir, source_root_dir)
                render(source, destination)