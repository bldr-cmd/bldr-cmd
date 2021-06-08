import os

from pathlib import Path

import bldr
import bldr.util
from bldr.gen.render import CopyTemplatesRender
from bldr.environment import Environment
from bldr.gen.history import targz_pack_atomic

dotbldr_path = Path(os.path.join(os.path.abspath(os.path.dirname(bldr.__file__)), "dotbldr"))


def migrate(ctx: Environment) -> bool:

    if(os.path.isdir(ctx.proj_path / ".bldr" / "module")):
        os.system("mv " + str(ctx.proj_path / ".bldr" / "module") + " " + str(ctx.proj_path / ".bldr" / "brick"))
        ctx.log("changed")

    else:
        ctx.log("no change")

    return True


    



