import os
import shutil
import unittest
from samos_nc2iso import Samos

# Tests
class Testsamos(unittest.TestCase):
    """docstring for Testsamos"""
    def setUp(self):
        samos = Samos()
        testfile = "/nodc/web/data.nodc/htdocs/coaps/samos/WTEJ/2010/08/WTEJ_20100808v30001.nc"
        self.ncFiles = samos.find_nc_files()

        # Create ncml dir for testing
        if not os.path.exists("/nodc/users/tjaensch/python.git/src/samos/ncml/"):
            os.makedirs("/nodc/users/tjaensch/python.git/src/samos/ncml/")
        if not os.path.exists("/nodc/users/tjaensch/python.git/src/samos/iso_xml/"):
            os.makedirs("/nodc/users/tjaensch/python.git/src/samos/iso_xml/")
        if not os.path.exists("/nodc/users/tjaensch/python.git/src/samos/final_xml/"):
            os.makedirs("/nodc/users/tjaensch/python.git/src/samos/final_xml/")
        if not os.path.exists("/nodc/users/tjaensch/python.git/src/samos/netcdf3/"):
            os.makedirs("/nodc/users/tjaensch/python.git/src/samos/netcdf3/")
          
        # test run defs with one file
        samos.ncdump(testfile)
        samos.add_to_ncml(testfile)
        samos.xsltproc_to_iso(testfile)
        samos.add_collection_metadata(testfile)

    '''def tearDown(self):
        shutil.rmtree("/nodc/users/tjaensch/python.git/src/samos/ncml/")
        shutil.rmtree("/nodc/users/tjaensch/python.git/src/samos/iso_xml/")
        shutil.rmtree("/nodc/users/tjaensch/python.git/src/samos/final_xml")
        shutil.rmtree("/nodc/users/tjaensch/python.git/src/samos/netcdf3")'''

    def test_find_nc_files(self):
        self.assertTrue(len(self.ncFiles) >= 11000)
        self.assertTrue(self.ncFiles)

    def test_ncdump(self):
        self.assertTrue(os.path.isfile("/nodc/users/tjaensch/python.git/src/samos/ncml/WTEJ_20100808v30001.ncml"))

    def test_add_to_ncml(self):
        file = open("/nodc/users/tjaensch/python.git/src/samos/ncml/WTEJ_20100808v30001.ncml", "r")
        data = file.read()
        self.assertTrue("<title>WTEJ_20100808v30001</title><filesize>146</filesize><path>coaps/samos/WTEJ/2010/08/</path></netcdf>" in data)

    def test_xsltproc_to_iso(self):
        file = open("/nodc/users/tjaensch/python.git/src/samos/iso_xml/WTEJ_20100808v30001.xml", "r")
        data = file.read()
        self.assertTrue("COAPS.SAMOS.WTEJ_20100808v30001" in data)
        # browse graphic generated with bounding box numbers in main XSLT file
        self.assertTrue("<gmd:MD_BrowseGraphic>" in data)

    def test_add_collection_metadata(self):
        file = open("/nodc/users/tjaensch/python.git/src/samos/final_xml/WTEJ_20100808v30001.xml", "r")
        data = file.read()
        self.assertTrue("Global Change Master Directory (GCMD) Data Center Keywords" in data)

# __main__
if __name__ == '__main__':
    unittest.main()
# End __main__