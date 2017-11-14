import datetime
import netCDF4
import numpy as np
import os
import random
import shutil
import unittest
from ghcn import GHCN

testfile = "BR002141011"
destinationDir = '/nodc/data/tmp.23555/'

# Tests


class Testghcn(unittest.TestCase):
    """docstring for Testghcn"""

    def setUp(self):
        # Create dirs for testing
        if not os.path.exists(destinationDir + 'netcdf/'):
            os.makedirs(destinationDir + 'netcdf/')
        ghcn = GHCN()
        # ghcn.get_station_info()
        # Working ID AGE00147710; not working GMM00010686
        ghcn.download_dly_file(testfile)
        self.dictOfUniqueTimeValues = ghcn.get_unique_time_values(testfile)
        self.uniqueElements = ghcn.get_unique_elements(testfile)
        self.placeholderElementsFlagsList = ghcn.initialize_element_lists_with_time_key_and_placeholder_value(testfile, self.dictOfUniqueTimeValues, self.uniqueElements)
        self.timeIndex = ghcn.get_time_index_for_day(
            testfile + '190911TMAX-9999...', 20)
        self.elementsAndFlagsDataLists = ghcn.create_elements_flags_data_lists(
            testfile, self.dictOfUniqueTimeValues, self.placeholderElementsFlagsList)
        ghcn.parse_to_netCDF(testfile, self.dictOfUniqueTimeValues, self.elementsAndFlagsDataLists)

    def test_get_station_info(self):
        stationIds = np.load('stationIds.npy')
        self.assertTrue(len(stationIds) > 104000)

    def test_get_unique_time_values(self):
        self.assertTrue(len(self.dictOfUniqueTimeValues) > 28)

    def test_get_unique_elements(self):
        self.assertTrue(len(self.uniqueElements) > 0)

    def test_initialize_element_lists_with_time_key_and_placeholder_value(self):
        self.assertTrue(len(self.uniqueElements) < len(self.placeholderElementsFlagsList))

    def test_get_time_index_for_day(self):
        self.assertTrue(isinstance(self.timeIndex, float))

    def test_create_elements_flags_data_lists(self):
        self.assertTrue(
            len(random.choice(self.elementsAndFlagsDataLists.keys())) > 0)

    def test_parse_to_netCDF(self):
        pass

    def tearDown(self):
        shutil.rmtree(destinationDir + 'netcdf/')

# __main__
if __name__ == '__main__':
    unittest.main()
# End __main__
