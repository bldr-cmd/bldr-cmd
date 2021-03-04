"""
Dependency fetchers

"""
import toml

import bldr
from bldr.environment import Environment

def config(ctx: Environment = Environment()):
    return toml.load(f"{ctx.dotbldr_path}/dependency.toml")
