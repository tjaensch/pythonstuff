import os
import shutil
import unittest
from ghcn import GHCN

# Tests
class Testghcn(unittest.TestCase):
    """docstring for Testghcn"""
    def setUp(self):
        # Create dirs for testing
        if not os.path.exists("./dly_data_as_txt/"):
            os.makedirs("./dly_data_as_txt/")
        if not os.path.exists("./netcdf/"):
            os.makedirs("./netcdf/")
        ghcn = GHCN()
        self.stationIds = ghcn.get_ids()
        ghcn.download_dly_file("AGE00147710")
        ghcn.parse_to_netCDF("AGE00147710")

    def test_getIDs(self):
        self.assertTrue(len(self.stationIds) > 103000)

    def test_download_dly_file(self):
        self.assertTrue(os.path.isfile("./dly_data_as_txt/AGE00147710.txt"))

    def test_parse_to_netCDF(self):
        self.assertTrue(os.path.isfile("./netcdf/AGE00147710.nc"))

    def tearDown(self):
        shutil.rmtree("./dly_data_as_txt/")
        shutil.rmtree("./netcdf/")

# __main__
if __name__ == '__main__':
    unittest.main()
# End __main__