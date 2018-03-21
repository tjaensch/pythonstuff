import os
import shutil
import unittest
from gcmd import GCMD

# Tests


class Testgcmd(unittest.TestCase):
    """docstring for Testgcmd"""

    def setUp(self):
        gcmd = GCMD()
        testfile = "./collection_test_files/GHRSST-ABOM-L4HRfnd-AUS-RAMSSA_09km.xml"
        self.xmlFiles = gcmd.find_xml_files()
        self.themeKeywordsList = gcmd.get_theme_keywords(testfile)

    def test_find_xml_files(self):
        self.assertTrue(len(self.xmlFiles) > 0)
        self.assertTrue(self.xmlFiles)

    def test_get_theme_keywords(self):
        self.assertTrue(len(self.themeKeywordsList) == 5)
        self.assertTrue("EARTH SCIENCE > OCEANS > OCEAN TEMPERATURE > SEA SURFACE TEMPERATURE" in self.themeKeywordsList)
        self.assertTrue("satellite data" in self.themeKeywordsList)
        self.assertFalse("blah" in self.themeKeywordsList)

# __main__
if __name__ == '__main__':
    unittest.main()
# End __main__
