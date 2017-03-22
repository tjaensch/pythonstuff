import os
import shutil
import unittest
from goes_nc2iso import CMAN

# Tests
class Testcman(unittest.TestCase):
    """docstring for Testcman"""
    def setUp(self):
        cman = CMAN()
        testfile = "./testfile/GridSat-CONUS.goes13.2015.01.01.0145.v01.nc"
        self.ncFiles = cman.find_nc_files()

        # Create ncml dir for testing
        if not os.path.exists("./ncml/"):
            os.makedirs("./ncml/")
        if not os.path.exists("./iso_xml/"):
            os.makedirs("./iso_xml/")
        if not os.path.exists("./final_xml/"):
            os.makedirs("./final_xml/")
        if not os.path.exists("./netcdf3/"):
            os.makedirs("./netcdf3/")
          
        # test run defs with one file
        cman.ncdump(testfile)
        cman.add_to_ncml(testfile)
        cman.xsltproc_to_iso(testfile)
        cman.add_collection_metadata(testfile)

    '''def tearDown(self):
        shutil.rmtree("./ncml/")
        shutil.rmtree("./iso_xml/")
        shutil.rmtree("./final_xml")
        shutil.rmtree("./netcdf3")'''

    def test_find_nc_files(self):
        self.assertTrue(len(self.ncFiles) <= 1)
        self.assertTrue(self.ncFiles)

    def test_ncdump(self):
        self.assertTrue(os.path.isfile("./ncml/GridSat-CONUS.goes13.2015.01.01.0145.v01.ncml"))

    def test_add_to_ncml(self):
        file = open("./ncml/GridSat-CONUS.goes13.2015.01.01.0145.v01.ncml", "r")
        data = file.read()
        self.assertTrue("<title>GridSat-CONUS.goes13.2015.01.01.0145.v01</title><englishtitle>NDBC-CMANWxSat-CONUS.goes13.2015.01.01.0145.v01 - C-MAN/Wx buoy at-CO for US.goe, deployment 3</englishtitle><filesize>3452</filesize><path>/</path></netcdf>" in data)

    def test_xsltproc_to_iso(self):
        file = open("./iso_xml/GridSat-CONUS.goes13.2015.01.01.0145.v01.xml", "r")
        data = file.read()
        self.assertTrue("NDBC-CMANWx.GridSat-CONUS.goes13.2015.01.01.0145.v01" in data)
        # browse graphic generated with bounding box numbers in main XSLT file
        self.assertTrue("<gmd:MD_BrowseGraphic>" in data)

    def test_add_collection_metadata(self):
        file = open("./final_xml/GridSat-CONUS.goes13.2015.01.01.0145.v01.xml", "r")
        data = file.read()
        self.assertTrue("Global Change Master Directory (GCMD) Data Center Keywords" in data)

    def test_get_english_title(self):
        file = open("./final_xml/GridSat-CONUS.goes13.2015.01.01.0145.v01.xml", "r")
        data = file.read()
        self.assertTrue("NDBC-CMANWxSat-CONUS.goes13.2015.01.01.0145.v01 - C-MAN/Wx buoy at-CO for US.goe, deployment 3" in data)

# __main__
if __name__ == '__main__':
    unittest.main()
# End __main__