import os
import shutil
import unittest
from coops_nc2iso import COOPS

# Tests
class Testcoops(unittest.TestCase):
    """docstring for Testcoops"""
    def setUp(self):
        coops = COOPS()
        testfile = "/nodc/web/data.nodc/htdocs/ndbc/co-ops/2014/01/NOS_1612480_201401_D1_v00.nc"
        self.ncFiles = coops.find_nc_files()

        # Create ncml dir for testing
        if not os.path.exists("/nodc/users/tjaensch/python.git/src/coops/ncml/"):
            os.makedirs("/nodc/users/tjaensch/python.git/src/coops/ncml/")
        if not os.path.exists("/nodc/users/tjaensch/python.git/src/coops/iso_xml/"):
            os.makedirs("/nodc/users/tjaensch/python.git/src/coops/iso_xml/")
        if not os.path.exists("/nodc/users/tjaensch/python.git/src/coops/final_xml/"):
            os.makedirs("/nodc/users/tjaensch/python.git/src/coops/final_xml/")
        if not os.path.exists("/nodc/users/tjaensch/python.git/src/coops/netcdf3/"):
            os.makedirs("/nodc/users/tjaensch/python.git/src/coops/netcdf3/")
          
        # test run defs with one file
        coops.ncdump(testfile)
        coops.add_to_ncml(testfile)
        coops.xsltproc_to_iso(testfile)
        coops.add_collection_metadata(testfile)

    def tearDown(self):
        shutil.rmtree("/nodc/users/tjaensch/python.git/src/coops/ncml/")
        shutil.rmtree("/nodc/users/tjaensch/python.git/src/coops/iso_xml/")
        shutil.rmtree("/nodc/users/tjaensch/python.git/src/coops/final_xml")
        shutil.rmtree("/nodc/users/tjaensch/python.git/src/coops/netcdf3")

    def test_find_nc_files(self):
        self.assertTrue(len(self.ncFiles) > 11950)
        self.assertTrue(self.ncFiles)

    def test_ncdump(self):
        self.assertTrue(os.path.isfile("/nodc/users/tjaensch/python.git/src/coops/ncml/NOS_1612480_201401_D1_v00.ncml"))

    def test_add_to_ncml(self):
        file = open("/nodc/users/tjaensch/python.git/src/coops/ncml/NOS_1612480_201401_D1_v00.ncml", "r")
        data = file.read()
        self.assertTrue("<title>NOS_1612480_201401_D1_v00</title><englishtitle>NDBC-COOPS_1612480_201401_D1_v00 - CO-OPS buoy 1612480 for 201401, deployment 1</englishtitle><filesize>178</filesize><path>ndbc/co-ops/2014/01/</path></netcdf>" in data)

    def test_xsltproc_to_iso(self):
        file = open("/nodc/users/tjaensch/python.git/src/coops/iso_xml/NOS_1612480_201401_D1_v00.xml", "r")
        data = file.read()
        self.assertTrue("CO-OPS.NOS_1612480_201401_D1_v00" in data)
        # browse graphic generated with bounding box numbers in main XSLT file
        self.assertTrue("<gmd:MD_BrowseGraphic>" in data)

    def test_add_collection_metadata(self):
        file = open("/nodc/users/tjaensch/python.git/src/coops/final_xml/NOS_1612480_201401_D1_v00.xml", "r")
        data = file.read()
        self.assertTrue("Global Change Master Directory (GCMD) Data Center Keywords" in data)

    def test_get_english_title(self):
        file = open("/nodc/users/tjaensch/python.git/src/coops/final_xml/NOS_1612480_201401_D1_v00.xml", "r")
        data = file.read()
        self.assertTrue("NDBC-COOPS_1612480_201401_D1_v00 - CO-OPS buoy 1612480 for 201401, deployment 1" in data)

# __main__
if __name__ == '__main__':
    unittest.main()
# End __main__