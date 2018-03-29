import os
import shutil
import unittest
from gcmd import GCMD


class Testgcmd(unittest.TestCase):
    """docstring for Testgcmd"""

    def setUp(self):
        gcmd = GCMD()
        testfile = "./collection_test_files/GHRSST-ABOM-L4HRfnd-AUS-RAMSSA_09km.xml"
        self.xmlFiles = gcmd.find_xml_files()
        # THEME KEYWORDS
        self.themeKeywordsList = gcmd.get_theme_keywords(testfile)
        self.themeKeywordsThesauriList = gcmd.get_theme_keywords_thesauri(testfile)
        self.modelThemeKeywordsList = gcmd.get_model_theme_keywords_list()
        gcmd.check_theme_keywords(testfile)
        # DATACENTER KEYWORDS
        self.datacenterKeywordsList = gcmd.get_datacenter_keywords(testfile)
        self.datacenterKeywordsThesauriList = gcmd.get_datacenter_keywords_thesauri(testfile)
        self.modelDatacenterKeywordsList = gcmd.get_model_datacenter_keywords_list()
        gcmd.check_datacenter_keywords(testfile)
        # PLACE KEYWORDS
        self.placeKeywordsList = gcmd.get_place_keywords(testfile)
        self.placeKeywordsThesauriList = gcmd.get_place_keywords_thesauri(testfile)
        self.modelPlaceKeywordsList = gcmd.get_model_place_keywords_list()
        self.similarPlaceKeywords = gcmd.get_similar_place_keywords(self.modelPlaceKeywordsList, "ARABIAN SEA")
        gcmd.check_place_keywords(testfile)
        '''# PLATFORM KEYWORDS
        self.platformKeywordsList = gcmd.get_platform_keywords(testfile)
        self.platformKeywordsThesauriList = gcmd.get_platform_keywords_thesauri(testfile)
        self.modelPlatformKeywordsList = gcmd.get_model_platform_keywords_list()
        gcmd.check_platform_keywords(testfile)'''
        # INSTRUMENT KEYWORDS
        self.instrumentKeywordsList = gcmd.get_instrument_keywords(testfile)
        self.instrumentKeywordsThesauriList = gcmd.get_instrument_keywords_thesauri(testfile)
        self.modelInstrumentKeywordsList = gcmd.get_model_instrument_keywords_list()
        gcmd.check_instrument_keywords(testfile)
        # PROJECT KEYWORDS
        self.projectKeywordsList = gcmd.get_project_keywords(testfile)
        self.projectKeywordsThesauriList = gcmd.get_project_keywords_thesauri(testfile)
        self.modelProjectKeywordsList = gcmd.get_model_project_keywords_list()
        gcmd.check_project_keywords(testfile)

    def test_find_xml_files(self):
        self.assertTrue(len(self.xmlFiles) > 0)
        self.assertTrue(self.xmlFiles)

    # THEME KEYWORDS
    def test_get_theme_keywords(self):
        self.assertTrue(len(self.themeKeywordsList) == 5)
        self.assertTrue("EARTH SCIENCE > OCEANS > OCEAN TEMPERATURE > SEA SURFACE TEMPERATURE" in self.themeKeywordsList)
        self.assertFalse("EARTH SCIENCE > OCEANS > OCEAN TEMPERATURE" in self.themeKeywordsList)
        self.assertTrue("SATELLITE DATA" in self.themeKeywordsList)
        self.assertFalse("blah" in self.themeKeywordsList)

    def test_get_theme_keywords_thesauri(self):
        self.assertTrue(len(self.themeKeywordsList) == 5)
        self.assertTrue("NODC DATA TYPES THESAURUS" in self.themeKeywordsThesauriList)
        self.assertFalse("BLAH THESAURUS" in self.themeKeywordsThesauriList)
        self.assertTrue("NASA/GCMD EARTH SCIENCE KEYWORDS" in self.themeKeywordsThesauriList)
        self.assertFalse("blah" in self.themeKeywordsThesauriList)

    def test_get_model_theme_keywords_list(self):
        self.assertTrue(len(self.modelThemeKeywordsList) > 3150)
        self.assertTrue("EARTH SCIENCE > TERRESTRIAL HYDROSPHERE" in self.modelThemeKeywordsList)
        self.assertTrue("EARTH SCIENCE > ATMOSPHERE > WEATHER EVENTS > TROPICAL CYCLONES > MINIMUM CENTRAL PRESSURE > TYPHOONS (WESTERN N. PACIFIC)" in self.modelThemeKeywordsList)
        self.assertFalse("BLAH" in self.modelThemeKeywordsList)

    def test_check_theme_keywords(self):
        with open('GHRSST-ABOM-L4HRfnd-AUS-RAMSSA_09km.csv') as f:
            s = f.read()
        self.assertTrue("SEA SURFACE TEMPERATURE" in s)
        self.assertTrue("OCEANOGRAPHY" in s)
        self.assertTrue("EARTH SCIENCE > OCEANS > OCEAN TEMPERATURE > SEA SURFACE TEMPERATURE > FOUNDATION SEA SURFACE TEMPERATURE" in s)
        self.assertFalse("EARTH SCIENCE > OCEANS > OCEAN OPTICS" in s)

    # DATACENTER KEYWORDS
    def test_get_datacenter_keywords(self):
        self.assertTrue(len(self.datacenterKeywordsList) == 5)
        self.assertTrue("DOC/NOAA/NESDIS/NODC > NATIONAL OCEANOGRAPHIC DATA CENTER, NESDIS, NOAA, U.S. DEPARTMENT OF COMMERCE" in self.datacenterKeywordsList)
        self.assertFalse("BLAH NESDIS" in self.datacenterKeywordsList)
        self.assertTrue("NASA/JPL/PODAAC > PHYSICAL OCEANOGRAPHY DISTRIBUTED ACTIVE ARCHIVE CENTER, JET PROPULSION LABORATORY, NASA" in self.datacenterKeywordsList)
        self.assertFalse("Australian Bureau of Blah" in self.datacenterKeywordsList)

    def test_get_datacenter_keywords_thesauri(self):
        self.assertTrue(len(self.datacenterKeywordsThesauriList) == 3)
        self.assertTrue("GLOBAL CHANGE MASTER DIRECTORY (GCMD) DATA CENTER KEYWORDS" in self.datacenterKeywordsThesauriList)
        self.assertFalse("GLOBAL CHANGE MASTER DIRECTORY (GCMD) DATA CENTER" in self.datacenterKeywordsThesauriList)
        self.assertTrue("NODC COLLECTING INSTITUTION NAMES THESAURUS" in self.datacenterKeywordsThesauriList)
        self.assertFalse("Australian Bureau of Blah" in self.datacenterKeywordsThesauriList)

    def test_get_model_datacenter_keywords_list(self):
        self.assertTrue(len(self.modelDatacenterKeywordsList) > 3600)
        self.assertTrue("ACADEMIC > OR-STATE/EOARC > OR-STATE/EOARC > EASTERN OREGON AGRICULTURE RESEARCH CENTER, OREGON STATE UNIVERSITY" in self.modelDatacenterKeywordsList)
        self.assertTrue("GOVERNMENT AGENCIES-NON-US > GERMANY > DE/BERLIN/ILR > WILLKOMMEN ILR BERLIN" in self.modelDatacenterKeywordsList)
        self.assertFalse("BLAH" in self.modelDatacenterKeywordsList)

    def test_check_datacenter_keywords(self):
        with open('GHRSST-ABOM-L4HRfnd-AUS-RAMSSA_09km.csv') as f:
            s = f.read()
        self.assertTrue("AUSTRALIAN BUREAU OF METEOROLOGY" in s)
        self.assertTrue("US NASA; JET PROPULSION LABORATORY; PHYSICAL OCEANOGRAPHY DISTRIBUTED ACTIVE ARCHIVE CENTER" in s)
        self.assertFalse("GOVERNMENT AGENCIES-U.S. FEDERAL AGENCIES > NASA > NASA/JPL/PODAAC > PHYSICAL OCEANOGRAPHY DISTRIBUTED ACTIVE ARCHIVE CENTER, JET PROPULSION LABORATORY, NASA" in s)

    # PLACE KEYWORDS
    def test_get_place_keywords(self):
        self.assertTrue(len(self.placeKeywordsList) == 33)
        self.assertTrue("ANDAMAN SEA OR BURMA SEA" in self.placeKeywordsList)
        self.assertFalse("Bavaria" in self.placeKeywordsList)
        self.assertTrue("OCEAN > PACIFIC OCEAN > WESTERN PACIFIC OCEAN > SOUTH CHINA SEA" in self.placeKeywordsList)
        self.assertFalse("Oceaniyuck" in self.placeKeywordsList)

    def test_get_place_keywords_thesauri(self):
        self.assertTrue(len(self.placeKeywordsThesauriList) == 3)
        self.assertTrue("NODC SEA AREA NAMES THESAURUS" in self.placeKeywordsThesauriList)
        self.assertFalse("NODC SEA AREA NAMES THESAURI" in self.placeKeywordsThesauriList)
        self.assertTrue("NASA/GCMD LOCATION KEYWORDS" in self.placeKeywordsThesauriList)
        self.assertFalse("NODC SEA AREA NAMES THESAURUS BLAH" in self.placeKeywordsThesauriList)

    def test_get_model_place_keywords_list(self):
        self.assertTrue(len(self.modelPlaceKeywordsList) > 500)
        self.assertTrue("CONTINENT > AFRICA > CENTRAL AFRICA > ANGOLA" in self.modelPlaceKeywordsList)
        self.assertTrue("CONTINENT > EUROPE > NORTHERN EUROPE > SCANDINAVIA > ALAND ISLANDS" in self.modelPlaceKeywordsList)
        self.assertFalse("OUTER SPACE > MARS" in self.modelPlaceKeywordsList)

    def test_get_similar_place_keywords(self):
        self.assertTrue(len(self.similarPlaceKeywords) == 3)
        self.assertTrue("OCEAN > INDIAN OCEAN > ARABIAN SEA" in self.similarPlaceKeywords)
        self.assertTrue("N/A" in self.similarPlaceKeywords)

    def test_check_place_keywords(self):
        with open('GHRSST-ABOM-L4HRfnd-AUS-RAMSSA_09km.csv') as f:
            s = f.read()
        self.assertTrue("ARABIAN SEA" in s)
        self.assertTrue("EAST INDIAN ARCHIPELAGO" in s)
        self.assertFalse("OCEAN > ATLANTIC OCEAN > SOUTH ATLANTIC OCEAN" in s)

    '''# PLATFORM KEYWORDS
    def test_get_platform_keywords(self):
        self.assertTrue(len(self.platformKeywordsList) == 18)
        self.assertTrue("GCOM-W1" in self.platformKeywordsList)
        self.assertFalse("Bavaria" in self.platformKeywordsList)
        self.assertTrue("METOP-A > METEOROLOGICAL OPERATIONAL SATELLITE - A" in self.platformKeywordsList)
        self.assertFalse("METOP-C" in self.platformKeywordsList)

    def test_get_platform_keywords_thesauri(self):
        self.assertTrue(len(self.platformKeywordsThesauriList) == 2)
        self.assertTrue("NODC PLATFORM NAMES THESAURUS" in self.platformKeywordsThesauriList)
        self.assertFalse("NODC PLATFORM NAMES THESAURUS BLAH" in self.platformKeywordsThesauriList)
        self.assertTrue("GLOBAL CHANGE MASTER DIRECTORY (GCMD) PLATFORM KEYWORDS" in self.platformKeywordsThesauriList)
        self.assertFalse("PLATYPUS" in self.platformKeywordsThesauriList)

    def test_get_model_platform_keywords_list(self):
        self.assertTrue(len(self.modelPlatformKeywordsList) > 850)
        self.assertTrue("AIRCRAFT > A340-600 > AIRBUS A340-600" in self.modelPlatformKeywordsList)
        self.assertTrue("EARTH OBSERVATION SATELLITES > NASA DECADAL SURVEY > ACE (DECADAL SURVEY) > AEROSOL - CLOUD - ECOSYSTEMS" in self.modelPlatformKeywordsList)
        self.assertFalse("BLAH" in self.modelPlatformKeywordsList)

    def test_check_platform_keywords(self):
        with open('GHRSST-ABOM-L4HRfnd-AUS-RAMSSA_09km.csv') as f:
            s = f.read()
        self.assertTrue("AQUA SATELLITE" in s)
        self.assertTrue("NOAA-19 SATELLITE" in s)
        self.assertFalse("EARTH OBSERVATION SATELLITES > CORIOLIS > CORIOLIS" in s)'''

    # INSTRUMENT KEYWORDS
    def test_get_instrument_keywords(self):
        self.assertTrue(len(self.instrumentKeywordsList) == 11)
        self.assertTrue("AATSR-MET" in self.instrumentKeywordsList)
        self.assertFalse("Bavaria" in self.instrumentKeywordsList)
        self.assertTrue("AMSR-E > ADVANCED MICROWAVE SCANNING RADIOMETER-EOS" in self.instrumentKeywordsList)
        self.assertFalse("AATSR > ADVANCE ALONG-TRACK SCANNING" in self.instrumentKeywordsList)

    def test_get_instrument_keywords_thesauri(self):
        self.assertTrue(len(self.instrumentKeywordsThesauriList) == 2)
        self.assertTrue("NODC INSTRUMENT TYPES THESAURUS" in self.instrumentKeywordsThesauriList)
        self.assertFalse("NODC INSTRUMENT TYPES" in self.instrumentKeywordsThesauriList)
        self.assertTrue("GLOBAL CHANGE MASTER DIRECTORY (GCMD) INSTRUMENT KEYWORDS" in self.instrumentKeywordsThesauriList)
        self.assertFalse("INSTRUMENTS" in self.instrumentKeywordsThesauriList)

    def test_get_model_instrument_keywords_list(self):
        self.assertTrue(len(self.modelInstrumentKeywordsList) > 1500)
        self.assertTrue("EARTH REMOTE SENSING INSTRUMENTS > ACTIVE REMOTE SENSING > ALTIMETERS > LIDAR/LASER ALTIMETERS > ATLAS > ADVANCED TOPOGRAPHIC LASER ALTIMETER SYSTEM" in self.modelInstrumentKeywordsList)
        self.assertTrue("IN SITU/LABORATORY INSTRUMENTS > ELECTRICAL METERS > MESA > MINIATURE ELECTROSTATIC ANALYZER" in self.modelInstrumentKeywordsList)
        self.assertFalse("SOME > INSTRUMENT > DUDE" in self.modelInstrumentKeywordsList)

    def test_check_instrument_keywords(self):
        with open('GHRSST-ABOM-L4HRfnd-AUS-RAMSSA_09km.csv') as f:
            s = f.read()
        self.assertTrue("AATSR-MET" in s)
        self.assertTrue("AATSR-NR" in s)
        self.assertFalse("BLAH" in s)

    # PROJECT KEYWORDS
    def test_get_project_keywords(self):
        self.assertTrue(len(self.projectKeywordsList) == 3)
        self.assertTrue("GROUP FOR HIGH RESOLUTION SEA SURFACE TEMPERATURE (GHRSST)" in self.projectKeywordsList)
        self.assertFalse("GHRSST" in self.projectKeywordsList)
        self.assertTrue("GHRSST > GROUP FOR HIGH RESOLUTION SEA SURFACE TEMPERATURE" in self.projectKeywordsList)
        self.assertTrue("NOAA ONESTOP PROJECT" in self.projectKeywordsList)

    def test_get_project_keywords_thesauri(self):
        self.assertTrue(len(self.projectKeywordsThesauriList) == 2)
        self.assertTrue("NODC PROJECT NAMES THESAURUS" in self.projectKeywordsThesauriList)
        self.assertFalse("NODC PROJECT NAMES" in self.projectKeywordsThesauriList)
        self.assertTrue("GLOBAL CHANGE MASTER DIRECTORY (GCMD) PROJECT KEYWORDS" in self.projectKeywordsThesauriList)
        self.assertFalse("BLAH" in self.projectKeywordsThesauriList)

    def test_get_model_project_keywords_list(self):
        self.assertTrue(len(self.modelProjectKeywordsList) > 1700)
        self.assertTrue("A - C > AAE > AUSTRALASIAN ANTARCTIC EXPEDITION OF 1911-14" in self.modelProjectKeywordsList)
        self.assertTrue("M - O > NRL CORIOLIS > NAVAL RESEARCH LABORATORY CORIOLIS" in self.modelProjectKeywordsList)
        self.assertFalse("X - Y > BLAH > DUDE" in self.modelProjectKeywordsList)

    def test_check_project_keywords(self):
        with open('GHRSST-ABOM-L4HRfnd-AUS-RAMSSA_09km.csv') as f:
            s = f.read()
        self.assertTrue("GROUP FOR HIGH RESOLUTION SEA SURFACE TEMPERATURE (GHRSST)" in s)
        self.assertFalse("BLAH" in s)

# __main__
if __name__ == '__main__':
    unittest.main()
# End __main__
