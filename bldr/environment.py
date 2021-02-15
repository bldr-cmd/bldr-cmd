import os
import sys

import click

class Environment:
    def __init__(self):
        self.verbose = False
        self.cwd = os.getcwd()
        self.env = {}

    def log(self, msg, *args):
        """Logs a message to stdout."""
        if args:
            msg %= args
        click.echo(msg, file=sys.stdout)

    def vlog(self, msg, *args):
        """Logs a message to stdout only if verbose is enabled."""
        if self.verbose:
            self.log(msg, *args)