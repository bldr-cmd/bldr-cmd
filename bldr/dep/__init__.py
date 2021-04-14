"""
Dependency fetchers

"""

from bldr.gen.render import CopyTemplatesRender
from bldr.environment import Environment


def sync_githooks(ctx: Environment):
    git_path = ctx.proj_path / ".git"
    if git_path.exists():
        copy_render = CopyTemplatesRender(ctx, True) 
        copy_render.walk(ctx.proj_path / ".githooks", git_path / "hooks")
