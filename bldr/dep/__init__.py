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
        
        return
    copy_render = CopyTemplatesRender(ctx, True)
    git_hooks_path = git_path / "hooks"
    copy_render.walk(ctx.proj_path / ".githooks", git_hooks_path)
    
    venv_path = os.getenv("VIRTUAL_ENV")
    local_script = git_hooks_path / "venv"

    if venv_path != None:
        needs_mingw_path = False
        if venv_path[1:3] == ':\\':
            needs_mingw_path = True
        for activate_path in  [f"{venv_path}/Scripts/activate", f"{venv_path}/bin/activate"]:
            if os.path.exists(activate_path):
                if needs_mingw_path:
                    activate_path = to_mingw_path(activate_path)
                local_script.write_text(f"source {activate_path}")
                break
    
    if not local_script.exists():
        # Default to no venv
        local_script.write_text(f"# No venv")

def to_mingw_path(win_path: str):
    # c:\some\nested\path -> /c/some/nested/path
    # 012345
    win_path = win_path.replace('\\','/')
    return f"/{win_path[0].lower()}/{win_path[3:]}"