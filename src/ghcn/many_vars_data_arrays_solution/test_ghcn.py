import netCDF4
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
        self.stationIds = ghcn.get_stationInfo()
        #Working ID AGE00147710; not working GMM00010686
        ghcn.download_dly_file("AGE00147710")
        ghcn.parse_to_netCDF("AGE00147710")
        self.numberedList = ghcn.initialize_numbered_1_31_VALUE_MFLAG_QFLAG_SFLAG_lists()

    def test_get_stationInfo(self):
        self.assertTrue(len(self.stationIds) > 103000)

    def test_download_dly_file(self):
        self.assertTrue(os.path.isfile("./dly_data_as_txt/AGE00147710.txt"))

    def test_parse_to_netCDF(self):
        self.assertTrue(os.path.isfile("./netcdf/ghcn-daily_v3.22.2017-08-03_AGE00147710.nc"))
        f = netCDF4.Dataset('./netcdf/ghcn-daily_v3.22.2017-08-03_AGE00147710.nc','r')
        self.assertTrue(len(f.dimensions) == 2)
        self.assertTrue(len(f.variables) > 15)

    def test_initialize_numbered_1_31_VALUE_MFLAG_QFLAG_SFLAG_lists(self):
        self.assertTrue(len(self.numberedList) == 124)

    '''def tearDown(self):
        shutil.rmtree("./dly_data_as_txt/")
        shutil.rmtree("./netcdf/")'''

# __main__
if __name__ == '__main__':
    unittest.main()
# End __main__