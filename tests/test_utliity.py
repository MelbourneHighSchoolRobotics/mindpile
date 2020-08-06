import unittest
from .. import utility


class TestUtility(unittest.TestCase):
    def test_removeNameSpace(self):
        self.assertEqual("abc", "{asdfasdf}")

