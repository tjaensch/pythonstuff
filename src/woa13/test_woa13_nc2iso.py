import os
import shutil
import unittest
from woa13_nc2iso import WOA13

# Tests
class TestWOA13(unittest.TestCase):
    """docstring for TestWOA13"""
    def setUp(self):
        woa13 = WOA13()
        self.ncFiles = woa13.find_nc_files()

        # Create ncml dir for testing
        if not os.path.exists("/nodc/users/tjaensch/python/src/woa13/ncml/"):
            os.makedirs("/nodc/users/tjaensch/python/src/woa13/ncml/")
        # ncdump test run one file
        woa13.ncdump("woa13_all_i00_01.nc")

    def tearDown(self):
        shutil.rmtree("../ncml/")

    def test_find_nc_files(self):
        self.assertEqual(len(self.ncFiles), 10)
        self.assertTrue(self.ncFiles)

    def test_ncdump(self):
        self.assertTrue(os.path.isfile("../ncml/woa13_all_i00_01.ncml"))

# __main__
if __name__ == '__main__':
    unittest.main()
# End __main__