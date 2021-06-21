"""
Dependency fetchers

"""
import os
import platform
import shutil

from bldr.gen.render import CommonRender
from bldr.environment import Environment

def sync_githooks(ctx: Environment) -> None:
    git_path = ctx.proj_path / ".git"
    if not git_path.exists():
        # Nothing to do
        return

    copy_render = CopyHooksRender(ctx, True)
    git_hooks_path = git_path / "hooks"
    copy_render.walk(ctx.proj_path / ".githooks", git_hooks_path)

class CopyHooksRender(CommonRender):
    def render(self, source_path: str, destination_path: str):
        # if the destination does not exist, just copy the file
        self.ctx.vlog(f"Copying {source_path} -> {destination_path}")
        shutil.copy(source_path, destination_path)
        # Make sure we have the execute bit set
        os.chmod(destination_path, 0o744)
        return True