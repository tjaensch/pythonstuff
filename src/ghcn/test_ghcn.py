import os
import unittest
from ghcn import GHCN

# Tests
class Testghcn(unittest.TestCase):
    """docstring for Testghcn"""
    def setUp(self):
        ghcn = GHCN()
        self.stationIds = ghcn.get_ids()
        ghcn.download_dly_file("AGE00147710")

    def test_getIDs(self):
        self.assertTrue(len(self.stationIds) > 103000)

    def test_download_dly_file(self):
        self.assertTrue(os.path.isfile("./dly_data_as_txt/AGE00147710.csv"))

# __main__
if __name__ == '__main__':
    unittest.main()
# End __main__