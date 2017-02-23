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
        self.browsegraphiclink = coops.get_browse_graphic_link(testfile)

        # Create ncml dir for testing
        if not os.path.exists("/nodc/users/tjaensch/python.git/src/coops/ncml/"):
            os.makedirs("/nodc/users/tjaensch/python.git/src/coops/ncml/")
        if not os.path.exists("/nodc/users/tjaensch/python.git/src/coops/iso_xml/"):
            os.makedirs("/nodc/users/tjaensch/python.git/src/coops/iso_xml/")
        if not os.path.exists("/nodc/users/tjaensch/python.git/src/coops/final_xml/"):
            os.makedirs("/nodc/users/tjaensch/python.git/src/coops/final_xml/")  
        # test run defs with one file
        coops.ncdump(testfile)
        coops.add_to_ncml(testfile)
        coops.xsltproc_to_iso(testfile)
        coops.add_collection_metadata(testfile)

    '''def tearDown(self):
        shutil.rmtree("/nodc/users/tjaensch/python.git/src/coops/ncml/")
        shutil.rmtree("/nodc/users/tjaensch/python.git/src/coops/iso_xml/")
        shutil.rmtree("/nodc/users/tjaensch/python.git/src/coops/final_xml")
        '''

    def test_find_nc_files(self):
        self.assertTrue(len(self.ncFiles) > 11950)
        self.assertTrue(self.ncFiles)

    def test_ncdump(self):
        self.assertTrue(os.path.isfile("/nodc/users/tjaensch/python.git/src/coops/ncml/NOS_1612480_201401_D1_v00.ncml"))

    def test_add_to_ncml(self):
        file = open("/nodc/users/tjaensch/python.git/src/coops/ncml/NOS_1612480_201401_D1_v00.ncml", "r")
        data = file.read()
        self.assertTrue("<title>NOS_1612480_201401_D1_v00</title><filesize>178</filesize><path>ndbc/co-ops/2014/01/</path><browsegraphic>blah</browsegraphic></netcdf>" in data)

    def test_xsltproc_to_iso(self):
        file = open("/nodc/users/tjaensch/python.git/src/coops/iso_xml/NOS_1612480_201401_D1_v00.xml", "r")
        data = file.read()
        self.assertTrue("CO-OPS.NOS_1612480_201401_D1_v00" in data)

    def test_add_collection_metadata(self):
        file = open("/nodc/users/tjaensch/python.git/src/coops/final_xml/NOS_1612480_201401_D1_v00.xml", "r")
        data = file.read()
        self.assertTrue("Global Change Master Directory (GCMD) Data Center Keywords" in data)

    def test_get_browse_graphic_link(self):
        file = open("/nodc/users/tjaensch/python.git/src/coops/final_xml/NOS_1612480_201401_D1_v00.xml", "r")
        data = file.read()
        self.assertTrue("<gmd:MD_BrowseGraphic>" in data)

# __main__
if __name__ == '__main__':
    unittest.main()
# End __main__