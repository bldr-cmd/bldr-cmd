"""
Dependency fetchers

"""
import os
from bldr.gen.render import CopyTemplatesRender
from bldr.environment import Environment


def sync_githooks(ctx: Environment) -> None:
    git_path = ctx.proj_path / ".git"
    if not git_path.exists():
        # Nothing to do
        print("did nothing :(((")
        return
    copy_render = CopyTemplatesRender(ctx, True)
    git_hooks_path = git_path / "hooks"
    copy_render.walk(ctx.proj_path / ".githooks", git_hooks_path)
    
    venv_path = os.getenv("VIRTUAL_ENV")
    local_script = git_hooks_path / "venv"

    # Default to no venv
    local_script.write_text(f"# No venv")

    if venv_path != None:
        for activate_path in  [f"{venv_path}/Scripts/activate", f"{venv_path}/bin/activate"]:
            if os.path.exists(activate_path):
                local_script.write_text(f"source {activate_path}")
                break




 