import os
import shutil
import unittest
from woa13_nc2iso import WOA13

# Tests
class TestWOA13(unittest.TestCase):
    """docstring for TestWOA13"""
    def setUp(self):
        woa13 = WOA13()
        self.ncFiles = woa13.find_nc_files()
        self.browsegraphiclink = woa13.get_browse_graphic_link("woa13_all_i00_01.nc")

        # Create ncml dir for testing
        if not os.path.exists("/nodc/users/tjaensch/python/src/woa13/ncml/"):
            os.makedirs("/nodc/users/tjaensch/python/src/woa13/ncml/")
        if not os.path.exists("/nodc/users/tjaensch/python/src/woa13/iso_xml/"):
            os.makedirs("/nodc/users/tjaensch/python/src/woa13/iso_xml/")
        if not os.path.exists("/nodc/users/tjaensch/python/src/woa13/final_xml/"):
            os.makedirs("/nodc/users/tjaensch/python/src/woa13/final_xml/")   
        # test run defs with one file
        woa13.ncdump("woa13_all_i00_01.nc")
        woa13.add_to_ncml("woa13_all_i00_01.nc")
        woa13.xsltproc_to_iso("woa13_all_i00_01.nc")
        woa13.add_collection_metadata("woa13_all_i00_01.nc")

    def tearDown(self):
        shutil.rmtree("../ncml/")
        shutil.rmtree("../iso_xml/")
        shutil.rmtree("../final_xml")

    def test_find_nc_files(self):
        self.assertEqual(len(self.ncFiles), 10)
        self.assertTrue(self.ncFiles)

    def test_ncdump(self):
        self.assertTrue(os.path.isfile("../ncml/woa13_all_i00_01.ncml"))

    def test_add_to_ncml(self):
        file = open("../ncml/woa13_all_i00_01.ncml", "r")
        data = file.read()
        self.assertTrue("<title>woa13_all_i00_01.nc</title><filesize>180765</filesize><path>/nodc/users/tjaensch/python/src/woa13/netcdf/woa13_all_i00_01.nc</path><browsegraphic>" in data)

    def test_xsltproc_to_iso(self):
        file = open("../iso_xml/woa13_all_i00_01.xml", "r")
        data = file.read()
        self.assertTrue("WOA13.woa13_all_i00_01.nc" in data)

    def test_add_collection_metadata(self):
        self.assertTrue(os.path.getsize("../iso_xml/woa13_all_i00_01.xml") < os.path.getsize("../final_xml/woa13_all_i00_01.xml"))

    def test_get_browse_graphic_link(self):
        file = open("../final_xml/woa13_all_i00_01.xml", "r")
        data = file.read()
        self.assertTrue("<gmd:MD_BrowseGraphic>" in data)




# __main__
if __name__ == '__main__':
    unittest.main()
# End __main__