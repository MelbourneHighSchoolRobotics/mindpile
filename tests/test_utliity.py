import unittest
import Utility.utility  # TODO figure out imports for tests


class TestUtility(unittest.TestCase):
    def test_removeNameSpace(self):
        self.assertEqual("abc", Utility.utility.removeNameSpace("{asdfasdf}"))

