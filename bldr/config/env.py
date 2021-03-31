# This is used by Environment to populate its env
# Due to circular dependencies it cannot reference other parts of bldr
import toml
import os
from pathlib import Path


def default(dotbldr_path: str) -> dict:
    """
    Load the config by merging the local config on top of included deps config

    The load order - Last in wins
    * .bldr/module/*/config/config.toml
    * .bldr/config/config.toml
    * .bldr/module/*/config/{BLDR_ENV}.toml
    * .bldr/config/{BLDR_ENV}.toml
    """
    bldr_env = os.getenv('BLDR_ENV')
    full_config = {}

    deps_config_files = Path(dotbldr_path).glob( "/module/*/config/config.toml")
    for dep_config_file in deps_config_files:
        dep_env = load_if_exists(dep_config_file)
        full_config.update(dep_env)
    
    local_config = load_if_exists(f"{dotbldr_path}/config/config.toml")
    full_config.update(local_config)

    if bldr_env != None:
        e_deps_config_files = Path(dotbldr_path).glob(f"/module/*/config/{bldr_env}.toml")
        for e_dep_config_file in e_deps_config_files:
            e_dep_env = load_if_exists(e_dep_config_file)
            full_config.update(e_dep_env)
        e_env = load_if_exists(f"{dotbldr_path}/config/{bldr_env}.toml")
        full_config.update(e_env)
    
    return full_config

def load_if_exists(path_str: str) -> dict:
    path = Path(path_str)
    if path.exists():
        return toml.load(path)
    else:
        return {}