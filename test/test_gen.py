import os
import logging
import unittest
unittest.TestLoader.sortTestMethodsUsing = None

from .helper import BldrTestCase

from bldr.environment import Environment
import bldr.gen
import bldr.cli

class TestGen(BldrTestCase, unittest.TestCase):
    """
    Test the Gen library
    """
    def test_gen_add_generator(self):
        
        self.bldr('init')
        ctx = Environment()
        bldr.gen.add_generator(["gen.import", 'C:\dev\sr\tlm\TesterSim', True], ctx)

        #self.assertEqual(0, )
