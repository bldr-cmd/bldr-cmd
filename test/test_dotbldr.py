import os
import logging
import shutil
import unittest
unittest.TestLoader.sortTestMethodsUsing = None

from click.testing import CliRunner

import bldr.cli

original_cwd = os.path.abspath(os.path.curdir)
dotbldr_folder = os.path.join(original_cwd, "test/test_dotbldr")

log = logging.getLogger("LOG")

class TestDotBldr(unittest.TestCase):
    """
    Test the creation of the .bldr folder
    """
    def test_init(self):
        result = self.runner.invoke(
            bldr.cli.cmd('init'), '')
        self.assertEqual(0, result.exit_code)
        self.assertTrue(os.path.exists(".bldr"))
        self.assertTrue(os.path.exists(".bldr/cmd"))
        self.assertTrue(os.path.exists(".bldr/current"))
        self.assertTrue(os.path.exists(".bldr/next"))
        self.assertTrue(os.path.exists(".bldr/dependency.toml"))
        self.assertTrue(os.path.exists(".bldr/dependency.current.toml"))
        self.assertTrue(os.path.exists(".bldr/dependency.lock.toml"))
        
    def setUp(self):
        self.runner = CliRunner()

    @classmethod
    def setUpClass(cls):
        log.warning("Creating " + dotbldr_folder)
        if os.path.exists(dotbldr_folder):
            shutil.rmtree(dotbldr_folder)
        os.makedirs(dotbldr_folder)
        os.chdir(dotbldr_folder)

    @classmethod
    def tearDownClass(cls):
        log.warning("Removing " + dotbldr_folder)
        os.chdir(original_cwd)
        shutil.rmtree(dotbldr_folder)