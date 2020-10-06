import os
import logging
import shutil
import unittest

from click.testing import CliRunner

import bldr.cli

unittest.TestLoader.sortTestMethodsUsing = None


original_cwd = os.path.abspath(os.path.curdir)
test_folder = os.path.join(original_cwd, "test/test_dotbldr")

log = logging.getLogger("LOG")

class BldrTestCase(unittest.TestCase):
    def setUp(self):
        self.runner = CliRunner()
        self.log = log

    def bldr(self, cmd, args = ''):
        return self.runner.invoke(bldr.cli.cmd(cmd), args)

    @classmethod
    def setUpClass(cls):
        log.warning("Creating " + test_folder)
        if os.path.exists(test_folder):
            shutil.rmtree(test_folder)
        os.makedirs(test_folder)
        os.chdir(test_folder)

    @classmethod
    def tearDownClass(cls):
        log.warning("Removing " + test_folder)
        os.chdir(original_cwd)
        shutil.rmtree(test_folder)