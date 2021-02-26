import os
import sys
from pathlib import Path
import click


# This is based on https://gist.github.com/DGrady/32db5223b956fece094292775e5dfd1d
def find_dotbldr_dir(here: Path = None) -> Path:
    """
    Get the path to the project directory
    
    “Project directory” means the nearest parent directory of the 
    current directory that contains a `.bldr` directory. If there
    is no such directory, returns this directory.
    """
    if here is None:
        here = Path() # Current directory
    # Get the full path
    here = here.resolve(strict=True)
    dotbldr_path = here.joinpath('.bldr')

    if dotbldr_path.exists():
        return dotbldr_path

    for parent in here.parents:
        dotbldr_path = parent.joinpath('.bldr')
        if dotbldr_path.exists():
            return dotbldr_path

    sys.exit("Unable to locate .bldr folder")
    # This will never be reached
    return None

class Environment:
    def __init__(self):
        self.verbose = False
        self.cwd = os.getcwd()
        self.env = {}
        self._dotbldr_path = None

    @property
    def dotbldr_path(self) -> Path:
        if self._dotbldr_path == None:
            self._dotbldr_path = find_dotbldr_dir()

        return self._dotbldr_path
        
    @property
    def proj_path(self) -> Path:
        return self.dotbldr_path.parents[0]

    def log(self, msg, *args):
        """Logs a message to stdout."""
        if args:
            msg %= args
        click.echo(msg, file=sys.stdout)

    def vlog(self, msg, *args):
        """Logs a message to stdout only if verbose is enabled."""
        if self.verbose:
            self.log(msg, *args)
