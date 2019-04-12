import os
import shutil
import unittest
from samos_nc2iso import Samos

# Tests

class Testsamos(unittest.TestCase):
    """docstring for Testsamos"""

    def setUp(self):
        samos = Samos()
        testfile = "/nodc/web/data.nodc/htdocs/coaps/samos/WTEP/2007/04/WTEP_20070415v10001.nc"
        self.ncFiles = samos.find_nc_files()

        # Create ncml dir for testing
        if not os.path.exists("./ncml/"):
            os.makedirs("./ncml/")
        if not os.path.exists("./iso_xml/"):
            os.makedirs("./iso_xml/")
        if not os.path.exists("./final_xml/"):
            os.makedirs("./final_xml/")

        # test run defs with one file
        samos.ncdump(testfile)
        samos.add_to_ncml(testfile)
        samos.xsltproc_to_iso(testfile)
        samos.add_collection_metadata(testfile)

    def tearDown(self):
        shutil.rmtree("./ncml/")
        shutil.rmtree("./iso_xml/")
        shutil.rmtree("./final_xml")
        # shutil.rmtree("./netcdf3")

    def test_find_nc_files(self):
        self.assertTrue(len(self.ncFiles) >= 144000)
        self.assertTrue(self.ncFiles)

    def test_ncdump(self):
        self.assertTrue(os.path.isfile("./ncml/WTEP_20070415v10001.ncml"))

    def test_add_to_ncml(self):
        file = open("./ncml/WTEP_20070415v10001.ncml", "r")
        data = file.read()
        self.assertTrue(
            "<title>WTEP_20070415v10001</title><filesize>127</filesize><path>coaps/samos/WTEP/2007/04/</path></netcdf>" in data)

    def test_xsltproc_to_iso(self):
        file = open("./iso_xml/WTEP_20070415v10001.xml", "r")
        data = file.read()
        self.assertTrue("COAPS.SAMOS.WTEP_20070415v10001" in data)
        # browse graphic generated with bounding box numbers in main XSLT file
        self.assertTrue("<gmd:MD_BrowseGraphic>" in data)

    def test_add_collection_metadata(self):
        file = open("./final_xml/WTEP_20070415v10001.xml", "r")
        data = file.read()
        self.assertTrue(
            "Global Change Master Directory (GCMD) Data Center Keywords" in data)

# __main__
if __name__ == '__main__':
    unittest.main()
# End __main__
