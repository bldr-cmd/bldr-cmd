# This is used by Environment to populate its env
# Due to circular dependencies it cannot reference other parts of bldr
import toml

def default(dotbldr_path: str) -> dict:
    dep = {
        'config': toml.load(f"{dotbldr_path}/dependency.toml"),
        'lock': toml.load(f"{dotbldr_path}/dependency.lock.toml")
    }
    
    return dep