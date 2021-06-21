import os

from pathlib import Path

import bldr
import bldr.util
from bldr.gen.render import CopyTemplatesRender
from bldr.environment import Environment
from bldr.gen.history import targz_pack_atomic

dotbldr_path = Path(os.path.join(os.path.abspath(os.path.dirname(bldr.__file__)), "dotbldr"))

def migrate(ctx: Environment) -> bool:
    """
    Update .githooks to use new format
    """
    ctx.vlog("Migrating Git Hooks")

    old_githooks = ctx.local_path / ".githooks"
    if old_githooks.exists():
        bldr.util.rmtree(old_githooks)

    old_prj_githooks = ctx.proj_path / ".githooks"
    if old_prj_githooks.exists():
        bldr.util.rmtree(old_prj_githooks)

    copy_render = CopyTemplatesRender(ctx, True) 
    copy_render.walk(dotbldr_path / "template" / ".githooks", ctx.local_path / ".githooks")
    ctx.vlog("Migrating Git Hooks Complete")
    return True
