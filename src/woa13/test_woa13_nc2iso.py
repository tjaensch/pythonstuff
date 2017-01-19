import os
import unittest
from woa13_nc2iso import WOA13

# Tests
class TestWOA13(unittest.TestCase):
    """docstring for TestWOA13"""
    def setUp(self):
        woa13 = WOA13()
        self.ncFiles = woa13.find_nc_files()

    def test_find_nc_files(self):
        self.assertEqual(len(self.ncFiles), 10)
        self.assertTrue(self.ncFiles)

# __main__
if __name__ == '__main__':
    unittest.main()
# End __main__