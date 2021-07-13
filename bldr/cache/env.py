def default(dotbldr_path: str) -> dict:
        return toml.load(f"{dotbldr_path}/cache.toml")
         
def save_lock(dotbldr_path: str, lock_env: dict):
    with open(f"{dotbldr_path}/cache.lock.toml", 'w') as toml_file:
        return toml.dump(lock_env, toml_file)

def save_config(dotbldr_path: str, config_env: dict):
    with open(f"{dotbldr_path}/cache.toml", 'w') as toml_file:
        return toml.dump(config_env, toml_file)