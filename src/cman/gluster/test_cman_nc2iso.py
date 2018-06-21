import os
import shutil
import unittest
from cman_nc2iso import CMAN

# Tests


class Testcman(unittest.TestCase):
    """docstring for Testcman"""

    def setUp(self):
        cman = CMAN()
        testfile = "https://data.nodc.noaa.gov/ndbc/cmanwx/2016/05/NDBC_44020_201605_D6_v00.nc"
        cman.download_nc_file_from_url(testfile)

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

    def tearDown(self):
        cman = CMAN()
        testfile = "https://data.nodc.noaa.gov/ndbc/cmanwx/2016/05/NDBC_44020_201605_D6_v00.nc"
        shutil.rmtree("./ncml/")
        shutil.rmtree("./iso_xml/")
        shutil.rmtree("./final_xml")
        shutil.rmtree("./netcdf3")
        cman.delete_nc_file_after_processing(testfile)
        os.remove("./NDBC-CMANWx.xml")

    def test_get_nc_file_urls(self):
        self.assertTrue(sum(1 for line in open('files.txt')) > 12000)

    def test_ncdump(self):
        self.assertTrue(os.path.isfile("./ncml/NDBC_44020_201605_D6_v00.ncml"))

    def test_add_to_ncml(self):
        file = open("./ncml/NDBC_44020_201605_D6_v00.ncml", "r")
        data = file.read()
        self.assertTrue("<title>NDBC_44020_201605_D6_v00</title><englishtitle>NDBC-CMANWx_44020_201605_D6_v00 - C-MAN/Wx buoy 44020 for 201605, deployment 6</englishtitle><filesize>2212</filesize><path>ndbc/cmanwx/2016/05/</path></netcdf>" in data)

    def test_xsltproc_to_iso(self):
        file = open("./iso_xml/NDBC_44020_201605_D6_v00.xml", "r")
        data = file.read()
        self.assertTrue("NDBC-CMANWx.NDBC_44020_201605_D6_v00" in data)
        # browse graphic generated with bounding box numbers in main XSLT file
        self.assertTrue("<gmd:MD_BrowseGraphic>" in data)

    def test_add_collection_metadata(self):
        file = open("./final_xml/NDBC_44020_201605_D6_v00.xml", "r")
        data = file.read()
        self.assertTrue(
            "Global Change Master Directory (GCMD) Data Center Keywords" in data)

    def test_get_english_title(self):
        file = open("./final_xml/NDBC_44020_201605_D6_v00.xml", "r")
        data = file.read()
        self.assertTrue(
            "NDBC-CMANWx_44020_201605_D6_v00 - C-MAN/Wx buoy 44020 for 201605, deployment 6" in data)

# __main__
if __name__ == '__main__':
    unittest.main()
# End __main__
