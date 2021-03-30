# This is used by Environment to populate its env
# Due to circular dependencies it cannot reference other parts of bldr
import toml

def default(dotbldr_path: str) -> dict:
    return toml.load(f"{dotbldr_path}/generated.toml")

def save(generated_toml: dict, dotbldr_path: str):
    with open(f"{dotbldr_path}/generated.toml", 'w') as toml_file:
        return toml.dump(generated_toml, toml_file)