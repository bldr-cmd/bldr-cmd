"""
Dependency fetchers

"""
import os
import platform
import shutil

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
    