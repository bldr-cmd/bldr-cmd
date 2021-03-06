import os
import sys
from pathlib import Path
import click

from typing import Dict, List

builtin_cmd_folder = Path(__file__).parents[0].joinpath('cmd').absolute()
builtin_migration_folder = Path(__file__).parents[0].joinpath('migration').absolute()

def find_dotbldr_dir(here: Path = None) -> Path:
    return find_parent_dir('.bldr', here)

# This is based on https://gist.github.com/DGrady/32db5223b956fece094292775e5dfd1d
def find_parent_dir(pdirname: str, here: Path = None) -> Path:
    """
    Get the path to the project directory
    
    “Project directory” means the nearest parent directory of the 
    current directory that contains a `.bldr` directory. If there
    is no such directory, returns None.
    """
    if here is None:
        here = Path() # Current directory
    # Get the full path
    here = here.resolve(strict=True)
    dotbldr_path = here.joinpath(pdirname)

    if dotbldr_path.exists():
        return dotbldr_path.resolve()

    for parent in here.parents:
        dotbldr_path = parent.joinpath(pdirname)
        if dotbldr_path.exists():
            return dotbldr_path.resolve()

    return None

def default_env(dotbldr_path: str) -> Dict:
    # Only Import once we are called to avoid circular dependencies
    import bldr.config.env
    import bldr.dep.env
    import bldr.gen.env
    import bldr.cache.env
    
    return {
        'config': bldr.config.env.default(dotbldr_path),
        'dep': bldr.dep.env.default(dotbldr_path),
        'gen': bldr.gen.env.default(dotbldr_path),
        'cache': bldr.gen.env.default(dotbldr_path),
    }

class Environment:
    def __init__(self):
        self.verbose = False
        self.cwd = os.getcwd()
        self._env = None
        self._dotbldr_path = None
        self._gen_replay = False

    @property
    def env(self) -> Dict:
        # Handle the case where we don't have a .bldr folder
        if self.dotbldr_path == None:
            return {}

        if self._env == None:
            self._env = default_env(self.dotbldr_path)
        return self._env

    @env.setter
    def env(self, env):
        self._env = env

    @property
    def gen_replay(self):
        return self._gen_replay

    @gen_replay.setter
    def gen_replay(self, replay):
        self._gen_replay = replay

    @property
    def dotbldr_path(self) -> Path:
        if self._dotbldr_path == None:
            self._dotbldr_path = find_dotbldr_dir()

        return self._dotbldr_path
        
    @property
    def proj_path(self) -> Path:
        return self.dotbldr_path.parents[0]

    @property
    def brick_path(self) -> Path:
        return self.dotbldr_path / "brick"

    @property
    def cmd_paths(self) -> List[Path]:
        if self.dotbldr_path == None:
            return [ builtin_cmd_folder ]    
        else:
            return [ self.dotbldr_path / "cmd", self.brick_path / "*/cmd", builtin_cmd_folder ]

    @property
    def history_path(self) -> Path:
        return self.dotbldr_path / "history"

    @property
    def next_path(self) -> Path:
        return self.history_path / "next"

    @property
    def current_path(self) -> Path:
        return self.history_path / "current"

    @property
    def current_targz(self) -> Path:
        return Path(f"{self.current_path}.tar.gz")
    
    @property
    def current_targz_next(self) -> Path:
        return Path(f"{self.current_path}.next.tar.gz")

    @property
    def prev_path(self) -> Path:
        return self.history_path / "previous"

    @property
    def local_path(self) -> Path:
        return self.dotbldr_path / "template"

    @property
    def generated_history(self) -> Path:
        return self.history_path / "generated"

    @property
    def next_generated_path(self) -> Path:
        return self.generated_history / "next"

    @property
    def current_generated_path(self) -> Path:
        return self.generated_history / "current"

    @property
    def current_generated_targz(self) -> Path:
        return Path(f"{self.current_generated_path}.tar.gz")
    
    @property
    def current_generated_targz_next(self) -> Path:
        return Path(f"{self.current_generated_path}.next.tar.gz")

    @property
    def previous_generated_path(self) -> Path:
        return self.generated_history / "previous"
    
    def cmd_path_globs(self, fileglob: str) -> List[Path.glob]:
        if self.dotbldr_path == None:
            return [
                builtin_cmd_folder.glob(fileglob)
            ]
        else:
            return [
                self.dotbldr_path.joinpath("cmd").glob(fileglob),
                self.brick_path.glob( "*/cmd/" + fileglob),
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

        for glob_files in self.cmd_path_globs(f"{cmd_name}.py"):
            for glob_file in glob_files:
                return glob_file


        return None


    @property
    def migrated_toml_path(self) -> Path:
        return self.dotbldr_path / "migrated.toml"

    def migration_path_globs(self, fileglob: str) -> List[Path.glob]:
        if self.dotbldr_path == None:
            return [
                builtin_cmd_folder.glob(fileglob)
            ]
        else:
            return [
                self.dotbldr_path.joinpath("migration").glob(fileglob),
                self.brick_path.glob( "*/migration/" + fileglob),
                builtin_migration_folder.glob(fileglob)
            ]

    def migrations(self):
        globs = self.migration_path_globs("*.py")
        migration_files = [file for glob in globs for file in sorted(glob, key=lambda g: g.name) if file.exists()]
        return migration_files

    def error(self, msg, *args):
        if args:
            msg %= args
        click.echo(msg, file=sys.stderr)
        
    def log(self, msg, *args):
        """Logs a message to stdout."""
        if args:
            msg %= args
        click.echo(msg, file=sys.stdout)

    def vlog(self, msg, *args):
        """Logs a message to stdout only if verbose is enabled."""
        if self.verbose:
            self.log(msg, *args)
