import os
import traceback
import runpy
import toml

from pathlib import Path
from bldr.environment import Environment

def run_migration(ctx: Environment, migration_path: Path):
    local_env = runpy.run_path(str(migration_path), globals())
    return local_env["migrate"](ctx)
    

def run(ctx: Environment):
    ctx.vlog(f"Checking Migrations")
    migrated_toml = {}
    if ctx.migrated_toml_path.exists():
        migrated_toml = toml.load(ctx.migrated_toml_path)

    success = True
    for migration in ctx.migrations():
        migration_name = migration.name
       
        if migration_name not in migrated_toml:
            ctx.vlog(f"Running {migration_name} ({migration})")
            try:       
                result = run_migration(ctx, migration)
                
                if result != True:
                    success = False
                    ctx.vlog(f"Failure in {migration_name}")
                    break
            except:
                success = False
                ctx.vlog(f"Exception in {migration_name}")
                traceback.print_exc()
                break

            migrated_toml[migration_name] = True

    with open(ctx.migrated_toml_path, 'w') as toml_file:
        toml.dump(migrated_toml, toml_file)
        
    return success