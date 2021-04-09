import unittest
import mindpile.Utility.utility  # TODO figure out imports for tests


class TestUtility(unittest.TestCase):
    def test_removeNameSpace(self):
        self.assertEqual("abc", mindpile.Utility.utility.removeNameSpace("{asdfasdf}"))

