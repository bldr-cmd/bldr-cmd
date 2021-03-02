import os
import sys
from pathlib import Path
import click

from typing import List

builtin_cmd_folder = Path(__file__).parents[0].joinpath('cmd').absolute()

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

    @property
    def generator_path(self) -> Path:
        return self.dotbldr_path / "generator"

    @property
    def cmd_paths(self) -> List[Path]:
        return [ self.dotbldr_path / "cmd", self.generator_path / "*/cmd", builtin_cmd_folder ]

    def cmd_path_globs(self, fileglob: str) -> List[Path.glob]:
        return [
            self.dotbldr_path.joinpath("cmd").glob(fileglob),
            self.generator_path.glob( "*/cmd/" + fileglob),
            builtin_cmd_folder.glob(fileglob)
        ]


    def cmd_path(self, cmd_name):
        """ 
        Find the path to the given command name 

        The order of search:
        .bldr/cmd
        .bldr/generator/*/cmd
        bldr/cmd
        """

        for files in self.cmd_path_globs(f"{cmd_name}.py"):
            if len(files) > 0:
                files.sort()
                return files[0]

        return None

    def log(self, msg, *args):
        """Logs a message to stdout."""
        if args:
            msg %= args
        click.echo(msg, file=sys.stdout)

    def vlog(self, msg, *args):
        """Logs a message to stdout only if verbose is enabled."""
        if self.verbose:
            self.log(msg, *args)
