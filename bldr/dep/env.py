# This is used by Environment to populate its env
# Due to circular dependencies it cannot reference other parts of bldr
import toml

def default(dotbldr_path: str) -> dict:
    dep = {
        'config': toml.load(f"{dotbldr_path}/dependency.toml"),
        'lock': toml.load(f"{dotbldr_path}/dependency.lock.toml")
    }
    return dep

def save_lock(dotbldr_path: str, lock_env: dict):
    with open(f"{dotbldr_path}/dependency.lock.toml", 'w') as toml_file:
        return toml.dump(lock_env, toml_file)

def save_config(dotbldr_path: str, config_env: dict):
    with open(f"{dotbldr_path}/dependency.toml", 'w') as toml_file:
        return toml.dump(config_env, toml_file)