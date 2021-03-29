import os
import logging
import unittest
unittest.TestLoader.sortTestMethodsUsing = None

from .helper import BldrTestCase

class TestDotBldr(BldrTestCase, unittest.TestCase):
    """
    Test the creation of the .bldr folder
    """
    def test_init(self):
        result = self.bldr('init')
        self.assertEqual(0, result.exit_code)
        self.assertTrue(os.path.exists(".bldr"))
        self.assertTrue(os.path.exists(".bldr/cmd"))
        self.assertTrue(os.path.exists(".bldr/current"))
        self.assertTrue(os.path.exists(".bldr/next"))
        self.assertTrue(os.path.exists(".bldr/dependency.toml"))
        self.assertTrue(os.path.exists(".bldr/dependency.lock.toml"))