import datetime
import os
import shutil
import unittest
from ghcn_metadata import GHCN

# Tests
class Testghcn(unittest.TestCase):
    """docstring for Testghcn"""
    def setUp(self):
        ghcn = GHCN()
        testfile = './testfiles/ghcn-daily_v3.22.' + datetime.datetime.today().strftime('%Y-%m-%d') + '_AGE00147710.nc'
        self.ncFiles = ghcn.find_nc_files()

        # Create ncml dir for testing
        if not os.path.exists("./ncml/"):
            os.makedirs("./ncml/")
        if not os.path.exists("./iso_xml/"):
            os.makedirs("./iso_xml/")
          
        # test run defs with one file
        ghcn.ncdump(testfile)
        ghcn.add_to_ncml(testfile)
        ghcn.xsltproc_to_iso(testfile)
        #ghcn.add_collection_metadata(testfile)

    def tearDown(self):
        shutil.rmtree("./ncml/")
        shutil.rmtree("./iso_xml/")

    def test_find_nc_files(self):
        self.assertTrue(len(self.ncFiles) > 0)
        self.assertTrue(self.ncFiles)

    def test_ncdump(self):
        self.assertTrue(os.path.isfile('./ncml/ghcn-daily_v3.22.' + datetime.datetime.today().strftime('%Y-%m-%d') + '_AGE00147710.ncml'))

    def test_add_to_ncml(self):
        file = open('./ncml/ghcn-daily_v3.22.' + datetime.datetime.today().strftime('%Y-%m-%d') + '_AGE00147710.ncml', 'r')
        data = file.read()
        self.assertTrue('<title>ghcn-daily_v3.22.' + datetime.datetime.today().strftime('%Y-%m-%d') + '_AGE00147710</title>' in data)

    def test_xsltproc_to_iso(self):
        file = open('./iso_xml/ghcn-daily_v3.22.' + datetime.datetime.today().strftime('%Y-%m-%d') + '_AGE00147710.xml', 'r')
        data = file.read()
        self.assertTrue('GHCN.ghcn-daily_v3.22.' + datetime.datetime.today().strftime('%Y-%m-%d') + '_AGE00147710' in data)
        # browse graphic generated with bounding box numbers in main XSLT file
        self.assertTrue("<gmd:MD_BrowseGraphic>" in data)


# __main__
if __name__ == '__main__':
    unittest.main()
# End __main__