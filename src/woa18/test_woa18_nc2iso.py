import os
import shutil
import unittest
from woa18_nc2iso import WOA18

# Tests
class TestWOA18(unittest.TestCase):
    """docstring for TestWOA18"""
    def setUp(self):
        woa18 = WOA18()
        testfile = "/nodc/www/data.nodc/htdocs/woa/WOA18/DATA/density/netcdf/95A4/1.00/woa18_95A4_I00_01.nc"
        self.ncFiles = woa18.find_nc_files()
        self.browsegraphiclink = woa18.get_browse_graphic_link(testfile)

        # Create ncml dir for testing
        if not os.path.exists("/nodc/users/tjaensch/python_onestop.git/src/woa18/ncml/"):
            os.makedirs("/nodc/users/tjaensch/python_onestop.git/src/woa18/ncml/")
        if not os.path.exists("/nodc/users/tjaensch/python_onestop.git/src/woa18/iso_xml/"):
            os.makedirs("/nodc/users/tjaensch/python_onestop.git/src/woa18/iso_xml/")
        if not os.path.exists("/nodc/users/tjaensch/python_onestop.git/src/woa18/final_xml/"):
            os.makedirs("/nodc/users/tjaensch/python_onestop.git/src/woa18/final_xml/")   
        # test run defs with one file
        woa18.ncdump(testfile)
        woa18.add_to_ncml(testfile)
        woa18.xsltproc_to_iso(testfile)
        woa18.add_collection_metadata(testfile)

    def tearDown(self):
        shutil.rmtree("/nodc/users/tjaensch/python_onestop.git/src/woa18/ncml/")
        shutil.rmtree("/nodc/users/tjaensch/python_onestop.git/src/woa18/iso_xml/")
        shutil.rmtree("/nodc/users/tjaensch/python_onestop.git/src/woa18/final_xml")

    def test_find_nc_files(self):
        self.assertEqual(len(self.ncFiles), 1002)
        self.assertTrue(self.ncFiles)

    def test_ncdump(self):
        self.assertTrue(os.path.isfile("/nodc/users/tjaensch/python_onestop.git/src/woa18/ncml/woa18_95A4_I00_01.ncml"))

    def test_add_to_ncml(self):
        file = open("/nodc/users/tjaensch/python_onestop.git/src/woa18/ncml/woa18_95A4_I00_01.ncml", "r")
        data = file.read()
        self.assertTrue("<title>woa18_95A4_I00_01</title><filesize>126</filesize><path>woa/WOA18/DATA/density/netcdf/95A4/1.00/</path>" in data)

    def test_xsltproc_to_iso(self):
        file = open("/nodc/users/tjaensch/python_onestop.git/src/woa18/iso_xml/woa18_95A4_I00_01.xml", "r")
        data = file.read()
        self.assertTrue("WOA18.woa18_95A4_I00_01" in data)

    def test_add_collection_metadata(self):
        file = open("/nodc/users/tjaensch/python_onestop.git/src/woa18/final_xml/woa18_95A4_I00_01.xml", "r")
        data = file.read()
        self.assertTrue("ANALYSES - ANNUAL SUMMARIES</gmx:Anchor>" in data)

    def test_get_browse_graphic_link(self):
        file = open("/nodc/users/tjaensch/python_onestop.git/src/woa18/final_xml/woa18_95A4_I00_01.xml", "r")
        data = file.read()
        self.assertTrue("<gmd:MD_BrowseGraphic>" in data)


# __main__
if __name__ == '__main__':
    unittest.main()
# End __main__