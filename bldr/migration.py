import os
import runpy
import toml

from pathlib import Path
from bldr.environment import Environment

def run_migration(ctx: Environment, migration_path: Path):
    if migration_path != None:
        local_env = runpy.run_path(str(migration_path), globals())
        return local_env["migrate"]
    else:
        return None

def ensure_migrations(ctx: Environment):
    migrated_toml = {}
    if ctx.migrated_toml_path.exists():
        migrated_toml = toml.load(ctx.migrated_toml_path)

    for migration in ctx.migrations():
        migration_name = migration.name

        if migration_name not in migrated_toml:
            try:
                result = run_migration(ctx, migration)
                
                if result == False:
                    break
            except:
                break

            migrated_toml[migration_name] = True

    with open(ctx.migrated_toml_path, 'w') as toml_file:
        toml.dump(migrated_toml, toml_file)