import os

def push_dir(new_dir: str):
    original_cwd = os.path.abspath(os.path.curdir)
    os.chdir(new_dir)
    return original_cwd

def proj_path():
    return os.path.abspath( os.path.join(dotbldr_path(), ".." ))

def dotbldr_path():
    if os.path.exists(".bldr"):
        return os.path.abspath(".bldr")
