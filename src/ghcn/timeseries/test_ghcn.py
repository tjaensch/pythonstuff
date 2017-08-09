import datetime
import netCDF4
import os
import random
import shutil
import unittest
from ghcn import GHCN

testfile = "AGE00147710"

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
        # Working ID AGE00147710; not working GMM00010686
        ghcn.download_dly_file(testfile)
        self.timeValues = ghcn.get_unique_time_values(testfile)
        self.uniqueElements = ghcn.get_unique_elements(testfile)
        self.dictTimeValues = ghcn.create_dict_from_unique_time_values_list(
            testfile)
        self.emptyElementFlagsList = ghcn.initialize_empty_element_lists(
            testfile)
        self.elementAndFlagArrays = ghcn.create_elements_flags_data_lists(
            testfile)
        self.timeIndex = ghcn.get_time_index_for_day(
            testfile + '190911TMAX-9999...', 1, self.timeValues)
        ghcn.parse_to_netCDF(testfile)

    def test_get_station_info(self):
        self.assertTrue(len(self.stationIds) > 103000)

    def test_download_dly_file(self):
        self.assertTrue(os.path.isfile(
            './dly_data_as_txt/' + testfile + '.txt'))

    def test_get_unique_time_values(self):
        self.assertTrue(len(self.timeValues) > 28)

    def test_get_time_index_for_day(self):
        self.assertTrue(isinstance(self.timeIndex, int))

    def test_get_unique_elementes(self):
        self.assertTrue(len(self.uniqueElements) > 0)

    def test_create_dict_from_unique_time_values_list(self):
        self.assertTrue(self.dictTimeValues[23] == self.timeValues[23])

    def test_initialize_empty_element_lists(self):
        self.assertTrue(len(self.emptyElementFlagsList)
                        == len(self.uniqueElements) * 4)

    def test_create_elements_flags_data_lists(self):
        self.assertTrue(
            len(random.choice(self.elementAndFlagArrays.keys())) > 0)

    def test_parse_to_netCDF(self):
        pass

    '''def tearDown(self):
        shutil.rmtree("./dly_data_as_txt/")
        shutil.rmtree("./netcdf/")'''

# __main__
if __name__ == '__main__':
    unittest.main()
# End __main__
