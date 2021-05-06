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
    Move the bldr history directories
    """
    ctx.vlog("Migrating History")
    copy_render = CopyTemplatesRender(ctx, True) 
    copy_render.walk(dotbldr_path / "history", ctx.history_path)

    old_prev = ctx.dotbldr_path / "previous"
    if old_prev.exists():
        old_prev.replace(ctx.prev_path)

    old_current = ctx.dotbldr_path / "current"
    if old_current.exists():
        old_current.replace(ctx.current_path)
        targz_pack_atomic(ctx.current_targz_next, ctx.current_targz, ctx.current_path)
        

    old_next = ctx.dotbldr_path / "next"
    if old_next.exists():
        bldr.util.rmtree(old_next)

    old_current_generated = ctx.dotbldr_path / "generated" / "current"
    if old_current_generated.exists():
        old_current_generated.replace(ctx.current_generated_path)
        targz_pack_atomic(ctx.current_generated_targz_next, ctx.current_generated_targz, ctx.current_generated_path)


    old_previous_generated = ctx.dotbldr_path / "generated" / "previous"
    if old_previous_generated.exists():
        old_previous_generated.replace(ctx.previous_generated_path)

    old_generated = ctx.dotbldr_path / "generated"
    if old_generated.exists():
        bldr.util.rmtree(old_generated)
    
    ctx.vlog("Migrating History Complete")
    return True
