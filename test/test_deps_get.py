import os
import logging
import unittest
unittest.TestLoader.sortTestMethodsUsing = None

from .helper import BldrTestCase

class TestDepsGet(BldrTestCase, unittest.TestCase):
    """
    Test the creation of the .bldr folder
    """
    @unittest.skip("Needs a .git repo")
    def test_init(self):
        result = self.bldr('deps.get')
        self.log.warning('deps.get')
        self.assertEqual(0, result.exit_code)
