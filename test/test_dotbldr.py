import os
import logging
import unittest
unittest.TestLoader.sortTestMethodsUsing = None

from click.testing import CliRunner

import bldr.command_line

original_cwd = os.path.abspath(os.path.curdir)
dotbldr_folder = os.path.join(original_cwd, "test/test_dotbldr")

log = logging.getLogger("LOG")

class TestDotBldr(unittest.TestCase):
    """
    Test the creation of the .bldr folder
    """
    def test_init(self):
        result = self.runner.invoke(
            bldr.command_line.init, '')
        self.assertEqual(0, result.exit_code)
        self.assertIn('init', result.output)
        
    def setUp(self):
        self.runner = CliRunner()

    @classmethod
    def setUpClass(cls):
        log.warning("Creating " + dotbldr_folder)
        if os.path.exists(dotbldr_folder):
            os.removedirs(dotbldr_folder)
        os.makedirs(dotbldr_folder)
        os.chdir(dotbldr_folder)

    @classmethod
    def tearDownClass(cls):
        log.warning("Removing " + dotbldr_folder)
        os.chdir(original_cwd)
        os.removedirs(dotbldr_folder)