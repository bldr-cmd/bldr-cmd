import os
from typing import Callable

def common_filter_file(root, file):
    return True

def common_filter_dir(root, dir):
    # Skip any folder that contains a .git
    if os.path.exists(os.path.join(root,dir,".git")):
        return False
    return True

def walk_local(template_root_dir: str, destination_root_dir: str, render: Callable[[str, str], bool], filter_file: Callable[[str, str], bool], filter_dir: Callable[[str, str], bool]):
    print(f"template_root_dir {template_root_dir}")
    for root, dirs, files in os.walk(template_root_dir, topdown=True):
        dirs[:] = [d for d in dirs if common_filter_dir(root, d) and filter_dir(root, d)]
        destdir = root.replace(template_root_dir, destination_root_dir)
        print(f"destdir {destdir}")
        if not os.path.exists(destdir):
            os.makedirs(destdir)
        for f in files:
            print(f"f {f}")
            if common_filter_file(root, f) and filter_file(root, f):
                source = os.path.join(root,f)
                destination = source.replace(template_root_dir, destination_root_dir)
                render(source, destination)