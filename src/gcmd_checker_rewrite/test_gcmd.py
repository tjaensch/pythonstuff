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
        self.themeKeywordsThesauriList = gcmd.get_theme_keywords_thesauri(testfile)
        self.datacenterKeywordsList = gcmd.get_datacenter_keywords(testfile)
        self.datacenterKeywordsThesauriList = gcmd.get_datacenter_keywords_thesauri(testfile)
        self.placeKeywordsList = gcmd.get_place_keywords(testfile)

    def test_find_xml_files(self):
        self.assertTrue(len(self.xmlFiles) > 0)
        self.assertTrue(self.xmlFiles)

    def test_get_theme_keywords(self):
        self.assertTrue(len(self.themeKeywordsList) == 5)
        self.assertTrue("EARTH SCIENCE > OCEANS > OCEAN TEMPERATURE > SEA SURFACE TEMPERATURE" in self.themeKeywordsList)
        self.assertFalse("EARTH SCIENCE > OCEANS > OCEAN TEMPERATURE" in self.themeKeywordsList)
        self.assertTrue("satellite data" in self.themeKeywordsList)
        self.assertFalse("blah" in self.themeKeywordsList)

    def test_get_theme_keywords_thesauri(self):
        self.assertTrue(len(self.themeKeywordsList) == 5)
        self.assertTrue("NODC DATA TYPES THESAURUS" in self.themeKeywordsThesauriList)
        self.assertFalse("BLAH THESAURUS" in self.themeKeywordsThesauriList)
        self.assertTrue("NASA/GCMD Earth Science Keywords" in self.themeKeywordsThesauriList)
        self.assertFalse("blah" in self.themeKeywordsThesauriList)

    def test_get_datacenter_keywords(self):
        self.assertTrue(len(self.datacenterKeywordsList) == 5)
        self.assertTrue("DOC/NOAA/NESDIS/NODC > National Oceanographic Data Center, NESDIS, NOAA, U.S. Department of Commerce" in self.datacenterKeywordsList)
        self.assertFalse("BLAH NESDIS" in self.datacenterKeywordsList)
        self.assertTrue("NASA/JPL/PODAAC > Physical Oceanography Distributed Active Archive Center, Jet Propulsion Laboratory, NASA" in self.datacenterKeywordsList)
        self.assertFalse("Australian Bureau of Blah" in self.datacenterKeywordsList)

    def test_get_datacenter_keywords_thesauri(self):
        self.assertTrue(len(self.datacenterKeywordsThesauriList) == 3)
        self.assertTrue("Global Change Master Directory (GCMD) Data Center Keywords" in self.datacenterKeywordsThesauriList)
        self.assertFalse("Global Change Master Directory (GCMD) Data Center" in self.datacenterKeywordsThesauriList)
        self.assertTrue("NODC COLLECTING INSTITUTION NAMES THESAURUS" in self.datacenterKeywordsThesauriList)
        self.assertFalse("Australian Bureau of Blah" in self.datacenterKeywordsThesauriList)

    def test_get_place_keywords(self):
        self.assertTrue(len(self.placeKeywordsList) == 33)
        self.assertTrue("Andaman Sea or Burma Sea" in self.placeKeywordsList)
        self.assertFalse("Bavaria" in self.placeKeywordsList)
        self.assertTrue("OCEAN > PACIFIC OCEAN > WESTERN PACIFIC OCEAN > SOUTH CHINA SEA" in self.placeKeywordsList)
        self.assertFalse("Oceaniyuck" in self.placeKeywordsList)

# __main__
if __name__ == '__main__':
    unittest.main()
# End __main__
