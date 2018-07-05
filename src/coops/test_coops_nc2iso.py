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
        self.gcmdKeywords = coops.get_gcmd_keywords_from_standard_names(testfile)

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
        coops.ncdump(testfile)
        coops.add_to_ncml(testfile)
        coops.xsltproc_to_iso(testfile)
        coops.add_collection_metadata(testfile)

    def tearDown(self):
        shutil.rmtree("./ncml/")
        shutil.rmtree("./iso_xml/")
        shutil.rmtree("./final_xml")
        shutil.rmtree("./netcdf3")

    def test_find_nc_files(self):
        self.assertTrue(len(self.ncFiles) > 11950)
        self.assertTrue(self.ncFiles)

    def test_ncdump(self):
        self.assertTrue(os.path.isfile("./ncml/NOS_1612480_201401_D1_v00.ncml"))

    def test_get_gcmd_keywords_from_standard_names(self):
        self.assertTrue('Earth Science &gt; Atmosphere &gt; Atmospheric Winds &gt; Surface Winds' in self.gcmdKeywords)
        self.assertTrue('Earth Science &gt; Atmosphere &gt; Atmospheric Pressure &gt; Sea Level Pressure' in self.gcmdKeywords)
        self.assertTrue('Earth Science &gt; Atmosphere &gt; Atmospheric Pressure &gt; Static Pressure' in self.gcmdKeywords)
        self.assertTrue('Earth Science &gt; Atmosphere &gt; Atmospheric Pressure &gt; Atmospheric Pressure Measurements' in self.gcmdKeywords)
        self.assertTrue('Earth Science &gt; Atmosphere &gt; Atmospheric Temperature &gt; Air Temperature' in self.gcmdKeywords)
        self.assertTrue('Earth Science &gt; Atmosphere &gt; Atmospheric Temperature &gt; Surface Air Temperature' in self.gcmdKeywords)
        self.assertFalse('Earth Science > Atmosphere > Atmospheric Temperature > Temperature' in self.gcmdKeywords)

    def test_add_to_ncml(self):
        file = open("./ncml/NOS_1612480_201401_D1_v00.ncml", "r")
        data = file.read()
        self.assertTrue("<title>NOS_1612480_201401_D1_v00</title><englishtitle>NDBC-COOPS_1612480_201401_D1_v00 - CO-OPS buoy 1612480 for 201401, deployment 1</englishtitle><filesize>178</filesize><path>ndbc/co-ops/2014/01/</path><keywords_from_standard_names>Earth Science &gt; Atmosphere &gt; Atmospheric Pressure &gt; Static Pressure,Earth Science &gt; Oceans &gt; Ocean Temperature &gt; Sea Surface Temperature,Earth Science &gt; Atmosphere &gt; Atmospheric Temperature &gt; Air Temperature,Earth Science &gt; Atmosphere &gt; Atmospheric Pressure &gt; Sea Level Pressure,Earth Science &gt; Atmosphere &gt; Atmospheric Pressure &gt; Atmospheric Pressure Measurements,Earth Science &gt; Atmosphere &gt; Atmospheric Winds &gt; Surface Winds,Earth Science &gt; Atmosphere &gt; Atmospheric Temperature &gt; Surface Air Temperature</keywords_from_standard_names></netcdf>" in data)

    def test_xsltproc_to_iso(self):
        file = open("./iso_xml/NOS_1612480_201401_D1_v00.xml", "r")
        data = file.read()
        self.assertTrue("CO-OPS.NOS_1612480_201401_D1_v00" in data)
        # browse graphic generated with bounding box numbers in main XSLT file
        self.assertTrue("<gmd:MD_BrowseGraphic>" in data)

    def test_add_collection_metadata(self):
        file = open("./final_xml/NOS_1612480_201401_D1_v00.xml", "r")
        data = file.read()
        self.assertTrue("Global Change Master Directory (GCMD) Data Center Keywords" in data)

    def test_get_english_title(self):
        file = open("./final_xml/NOS_1612480_201401_D1_v00.xml", "r")
        data = file.read()
        self.assertTrue("NDBC-COOPS_1612480_201401_D1_v00 - CO-OPS buoy 1612480 for 201401, deployment 1" in data)

# __main__
if __name__ == '__main__':
    unittest.main()
# End __main__