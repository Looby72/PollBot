import sys
import os

#import the path of the Bot directory
dirname = os.path.dirname(__file__)
print(dirname)
path = dirname[:len(dirname) - 5]
sys.path.insert(0, path)

import unittest

class TestWiki(unittest.TestCase):
    pass