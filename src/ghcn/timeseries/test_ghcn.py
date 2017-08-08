import datetime
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
        self.stationIds = ghcn.get_station_info()
        #Working ID AGE00147710; not working GMM00010686
        ghcn.download_dly_file("AGE00147710")
        self.timeValues = ghcn.get_unique_time_values("AGE00147710")
        self.uniqueElements = ghcn.get_unique_elements("AGE00147710")
        self.dictTimeValues = ghcn.create_dict_from_unique_time_values_list("AGE00147710")
        self.emptyElementFlagsList = ghcn.initialize_empty_element_lists("AGE00147710")
        ghcn.parse_to_netCDF("AGE00147710")

    def test_get_station_info(self):
        self.assertTrue(len(self.stationIds) > 103000)

    def test_download_dly_file(self):
        self.assertTrue(os.path.isfile("./dly_data_as_txt/AGE00147710.txt"))

    def test_get_unique_time_values(self):
        self.assertTrue(len(self.timeValues) > 28)

    def test_get_unique_elementes(self):
        self.assertTrue(len(self.uniqueElements) > 0)

    def test_create_dict_from_unique_time_values_list(self):
        self.assertTrue(self.dictTimeValues[23] == self.timeValues[23])

    def test_initialize_empty_element_lists(self):
        self.assertTrue(len(self.emptyElementFlagsList) == len(self.uniqueElements)*4)

    def test_parse_to_netCDF(self):
        pass


    '''def tearDown(self):
        shutil.rmtree("./dly_data_as_txt/")
        shutil.rmtree("./netcdf/")'''

# __main__
if __name__ == '__main__':
    unittest.main()
# End __main__