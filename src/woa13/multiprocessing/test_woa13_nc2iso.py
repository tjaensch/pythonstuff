import os
import shutil
import unittest
from woa13_nc2iso import WOA13

# Tests
class TestWOA13(unittest.TestCase):
    """docstring for TestWOA13"""
    def setUp(self):
        woa13 = WOA13()
        testfile = "/nodc/web/data.nodc/htdocs/nodc/archive/data/0114815/public/silicate/netcdf/all/1.00/woa13_all_i00_01.nc"
        self.ncFiles = woa13.find_nc_files()
        self.browsegraphiclink = woa13.get_browse_graphic_link(testfile)

        # Create ncml dir for testing
        if not os.path.exists("./ncml/"):
            os.makedirs("./ncml/")
        if not os.path.exists("./iso_xml/"):
            os.makedirs("./iso_xml/")
        if not os.path.exists("./final_xml/"):
            os.makedirs("./final_xml/")   
        # test run defs with one file
        woa13.ncdump(testfile)
        woa13.add_to_ncml(testfile)
        woa13.xsltproc_to_iso(testfile)
        woa13.add_collection_metadata(testfile)

    '''def tearDown(self):
        shutil.rmtree("./ncml/")
        shutil.rmtree("./iso_xml/")
        shutil.rmtree("./final_xml")'''

    def test_find_nc_files(self):
        self.assertEqual(len(self.ncFiles), 714)
        self.assertTrue(self.ncFiles)

    def test_ncdump(self):
        self.assertTrue(os.path.isfile("./ncml/woa13_all_i00_01.ncml"))

    def test_add_to_ncml(self):
        file = open("./ncml/woa13_all_i00_01.ncml", "r")
        data = file.read()
        self.assertTrue("<title>woa13_all_i00_01</title><filesize>176</filesize><path>nodc/archive/data/0114815/public/silicate/netcdf/all/1.00/</path><browsegraphic>" in data)

    def test_xsltproc_to_iso(self):
        file = open("./iso_xml/woa13_all_i00_01.xml", "r")
        data = file.read()
        self.assertTrue("WOA13.woa13_all_i00_01" in data)

    def test_add_collection_metadata(self):
        file = open("./final_xml/woa13_all_i00_01.xml", "r")
        data = file.read()
        self.assertTrue("ANALYSES - ANNUAL SUMMARIES</gmx:Anchor>" in data)

    def test_get_browse_graphic_link(self):
        file = open("./final_xml/woa13_all_i00_01.xml", "r")
        data = file.read()
        self.assertTrue("<gmd:MD_BrowseGraphic>" in data)

# __main__
if __name__ == '__main__':
    unittest.main()
# End __main__