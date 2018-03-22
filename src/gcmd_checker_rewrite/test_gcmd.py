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
        self.allKeywords = gcmd.get_all_GCMD_keywords(testfile)
        self.themeKeywordsList = gcmd.get_theme_keywords(testfile)
        self.themeKeywordsThesauriList = gcmd.get_theme_keywords_thesauri(testfile)
        self.datacenterKeywordsList = gcmd.get_datacenter_keywords(testfile)
        self.datacenterKeywordsThesauriList = gcmd.get_datacenter_keywords_thesauri(testfile)
        self.placeKeywordsList = gcmd.get_place_keywords(testfile)
        self.placeKeywordsThesauriList = gcmd.get_place_keywords_thesauri(testfile)
        self.platformKeywordsList = gcmd.get_platform_keywords(testfile)
        self.platformKeywordsThesauriList = gcmd.get_platform_keywords_thesauri(testfile)
        self.instrumentKeywordsList = gcmd.get_instrument_keywords(testfile)
        self.instrumentKeywordsThesauriList = gcmd.get_instrument_keywords_thesauri(testfile)
        self.projectKeywordsList = gcmd.get_project_keywords(testfile)
        self.projectKeywordsThesauriList = gcmd.get_project_keywords_thesauri(testfile)

    def test_find_xml_files(self):
        self.assertTrue(len(self.xmlFiles) > 0)
        self.assertTrue(self.xmlFiles)

    def test_get_all_GCMD_keywords(self):
        self.assertTrue(len(self.allKeywords) == len(self.themeKeywordsList) + len(self.themeKeywordsThesauriList) + len(self.datacenterKeywordsList) + len(self.datacenterKeywordsThesauriList) + len(self.placeKeywordsList) + len(self.placeKeywordsThesauriList) + len(self.platformKeywordsList) + len(self.platformKeywordsThesauriList) + len(self.instrumentKeywordsList) + len(self.instrumentKeywordsThesauriList) + len(self.projectKeywordsList) + len(self.projectKeywordsThesauriList))
        self.assertTrue("EARTH SCIENCE > OCEANS > OCEAN TEMPERATURE > SEA SURFACE TEMPERATURE" in self.allKeywords)
        self.assertTrue("Group for High Resolution Sea Surface Temperature (GHRSST)" in self.allKeywords)
        self.assertFalse("Blah" in self.allKeywords)

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

    def test_get_place_keywords_thesauri(self):
        self.assertTrue(len(self.placeKeywordsThesauriList) == 3)
        self.assertTrue("NODC SEA AREA NAMES THESAURUS" in self.placeKeywordsThesauriList)
        self.assertFalse("NODC SEA AREA NAMES THESAURI" in self.placeKeywordsThesauriList)
        self.assertTrue("NASA/GCMD Location Keywords" in self.placeKeywordsThesauriList)
        self.assertFalse("NODC SEA AREA NAMES THESAURUS BLAH" in self.placeKeywordsThesauriList)

    def test_get_platform_keywords(self):
        self.assertTrue(len(self.platformKeywordsList) == 18)
        self.assertTrue("GCOM-W1" in self.platformKeywordsList)
        self.assertFalse("Bavaria" in self.platformKeywordsList)
        self.assertTrue("METOP-A > Meteorological Operational Satellite - A" in self.platformKeywordsList)
        self.assertFalse("METOP-C" in self.platformKeywordsList)

    def test_get_platform_keywords_thesauri(self):
        self.assertTrue(len(self.platformKeywordsThesauriList) == 2)
        self.assertTrue("NODC PLATFORM NAMES THESAURUS" in self.platformKeywordsThesauriList)
        self.assertFalse("NODC PLATFORM NAMES THESAURUS BLAH" in self.platformKeywordsThesauriList)
        self.assertTrue("Global Change Master Directory (GCMD) Platform Keywords" in self.platformKeywordsThesauriList)
        self.assertFalse("PLATYPUS" in self.platformKeywordsThesauriList)

    def test_get_instrument_keywords(self):
        self.assertTrue(len(self.instrumentKeywordsList) == 11)
        self.assertTrue("AATSR-MET" in self.instrumentKeywordsList)
        self.assertFalse("Bavaria" in self.instrumentKeywordsList)
        self.assertTrue("AMSR-E > Advanced Microwave Scanning Radiometer-EOS" in self.instrumentKeywordsList)
        self.assertFalse("AATSR > Advanced Along-Track Scanning" in self.instrumentKeywordsList)

    def test_get_instrument_keywords_thesauri(self):
        self.assertTrue(len(self.instrumentKeywordsThesauriList) == 2)
        self.assertTrue("NODC INSTRUMENT TYPES THESAURUS" in self.instrumentKeywordsThesauriList)
        self.assertFalse("NODC INSTRUMENT TYPES" in self.instrumentKeywordsThesauriList)
        self.assertTrue("Global Change Master Directory (GCMD) Instrument Keywords" in self.instrumentKeywordsThesauriList)
        self.assertFalse("INSTRUMENTS" in self.instrumentKeywordsThesauriList)

    def test_get_project_keywords(self):
        self.assertTrue(len(self.projectKeywordsList) == 3)
        self.assertTrue("Group for High Resolution Sea Surface Temperature (GHRSST)" in self.projectKeywordsList)
        self.assertFalse("GHRSST" in self.projectKeywordsList)
        self.assertTrue("GHRSST > Group for High Resolution Sea Surface Temperature" in self.projectKeywordsList)
        self.assertTrue("NOAA OneStop Project" in self.projectKeywordsList)

    def test_get_project_keywords_thesauri(self):
        self.assertTrue(len(self.projectKeywordsThesauriList) == 2)
        self.assertTrue("NODC PROJECT NAMES THESAURUS" in self.projectKeywordsThesauriList)
        self.assertFalse("NODC PROJECT NAMES" in self.projectKeywordsThesauriList)
        self.assertTrue("Global Change Master Directory (GCMD) Project Keywords" in self.projectKeywordsThesauriList)
        self.assertFalse("BLAH" in self.projectKeywordsThesauriList)

# __main__
if __name__ == '__main__':
    unittest.main()
# End __main__
