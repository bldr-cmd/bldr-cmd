import os
import logging
import re
import shutil
import unittest

from click.testing import CliRunner

import bldr.cli
import bldr.util
from bldr.environment import Environment

unittest.TestLoader.sortTestMethodsUsing = None

original_cwd = os.path.abspath(os.path.curdir)
test_folder_base = os.path.join(original_cwd, "test/")

log = logging.getLogger("LOG")

class BldrTestCase():
    def setUp(self):
        self.runner = CliRunner()
        self.log = log

    def bldr(self, cmd, args = None):
        return self.runner.invoke(bldr.cli.cmd(Environment(), cmd), args)

    @classmethod
    def temp_folder(cls):
        test_name = re.sub(r'(?<!^)(?=[A-Z])', '_', cls.__name__).lower()
        return os.path.join(test_folder_base, test_name)

    @classmethod
    def setUpClass(cls):
        test_folder = cls.temp_folder()
        log.info("Creating " + test_folder)
        if os.path.exists(test_folder):
            bldr.util.rmtree(test_folder)
        os.makedirs(test_folder)
        os.chdir(test_folder)

    @classmethod
    def tearDownClass(cls):
        test_folder = cls.temp_folder()
        log.info("Removing " + test_folder)
        os.chdir(original_cwd)
        bldr.util.rmtree(test_folder)