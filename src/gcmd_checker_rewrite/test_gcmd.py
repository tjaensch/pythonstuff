import os
import shutil
import unittest
from gcmd import GCMD
from os.path import basename


class Testgcmd(unittest.TestCase):
    """docstring for Testgcmd"""

    def setUp(self):
        gcmd = GCMD()
        testfile = "./collection_test_files/GHRSST-ABOM-L4HRfnd-AUS-RAMSSA_09km.xml"
        self.xmlFiles = gcmd.find_xml_files("./collection_test_files")
        gcmd.create_results_csv("blank_file.xml")
        gcmd.create_xml_copy(testfile)
        gcmd.delete_csv_if_no_invalid_keywords_found("blank_file.xml")
        # THEME KEYWORDS
        self.themeKeywordsList = gcmd.get_theme_keywords(testfile)
        self.themeKeywordsThesauriList = gcmd.get_theme_keywords_thesauri(testfile)
        self.modelThemeKeywordsList = gcmd.get_model_theme_keywords_list()
        self.similarThemeKeywords = gcmd.get_similar_keywords(self.modelThemeKeywordsList, "OCEANOGRAPHY")
        # DATACENTER KEYWORDS
        self.datacenterKeywordsList = gcmd.get_datacenter_keywords(testfile)
        self.datacenterKeywordsThesauriList = gcmd.get_datacenter_keywords_thesauri(testfile)
        self.modelDatacenterKeywordsList = gcmd.get_model_datacenter_keywords_list()
        self.similarDatacenterKeywords = gcmd.get_similar_keywords(self.modelDatacenterKeywordsList, "DOC/NOAA/NESDIS/NCEI")
        # PLACE KEYWORDS
        self.placeKeywordsList = gcmd.get_place_keywords(testfile)
        self.placeKeywordsThesauriList = gcmd.get_place_keywords_thesauri(testfile)
        self.modelPlaceKeywordsList = gcmd.get_model_place_keywords_list()
        self.similarPlaceKeywords = gcmd.get_similar_keywords(self.modelPlaceKeywordsList, "ARABIAN SEA")
        # PLATFORM KEYWORDS
        self.platformKeywordsList = gcmd.get_platform_keywords(testfile)
        self.platformKeywordsThesauriList = gcmd.get_platform_keywords_thesauri(testfile)
        self.modelPlatformKeywordsList = gcmd.get_model_platform_keywords_list()
        self.similarPlatformKeywords = gcmd.get_similar_keywords(self.modelPlatformKeywordsList, "METOP-A")
        # INSTRUMENT KEYWORDS
        self.instrumentKeywordsList = gcmd.get_instrument_keywords(testfile)
        self.instrumentKeywordsThesauriList = gcmd.get_instrument_keywords_thesauri(testfile)
        self.modelInstrumentKeywordsList = gcmd.get_model_instrument_keywords_list()
        self.similarInstrumentKeywords = gcmd.get_similar_keywords(self.modelInstrumentKeywordsList, "AVHRR-3")
        # PROJECT KEYWORDS
        self.projectKeywordsList = gcmd.get_project_keywords(testfile)
        self.projectKeywordsThesauriList = gcmd.get_project_keywords_thesauri(testfile)
        self.modelProjectKeywordsList = gcmd.get_model_project_keywords_list()
        self.similarProjectKeywords = gcmd.get_similar_keywords(self.modelProjectKeywordsList, "OneStop")

    def test_find_xml_files(self):
        self.assertTrue(len(self.xmlFiles) > 0)
        self.assertTrue(self.xmlFiles)

    def test_delete_csv_if_no_invalid_keywords_found(self):
        self.assertTrue(os.path.exists('invalid_GCMD_keywords_results_' + basename(os.path.splitext("blank_file.xml")[0]) + '.csv') == False)

    def test_find_best_similar_keyword(self):
        gcmd = GCMD()
        self.assertTrue(gcmd.find_best_similar_keyword(["test", "N/A", "N/A"]) == "test")
        self.assertTrue(gcmd.find_best_similar_keyword(["N/A", "N/A", "N/A"]) == "")
        self.assertFalse(gcmd.find_best_similar_keyword(["N/A", "N/A", "N/A"]) == "test")
        self.assertTrue(gcmd.find_best_similar_keyword(["test", "testicle", "testosteron"]) == "test")
        self.assertTrue(gcmd.find_best_similar_keyword(["test", "test", "testosteron"]) == "test")
        self.assertTrue(gcmd.find_best_similar_keyword(["AVHRR-3 > Advanced Very High Resolution Radiometer-3", "N/A"]) == "AVHRR-3 &gt; Advanced Very High Resolution Radiometer-3")
        # self.assertTrue(gcmd.find_best_similar_keyword(["NOAA-17 > National Oceanic & Atmospheric Administration-17", "N/A"]) == "Earth Observation Satellites &gt; NOAA POES (Polar Orbiting Environmental Satellites) &gt; NOAA-17 &gt; National Oceanic &amp; Atmospheric Administration-17")

    def test_find_three_best_similar_keywords(self):
        gcmd = GCMD()
        self.assertTrue(gcmd.find_three_best_similar_keywords(["N/A"]) == ["N/A", "N/A", "N/A"])
        self.assertTrue(gcmd.find_three_best_similar_keywords(["N/A", "N/A"]) == ["N/A", "N/A", "N/A"])
        self.assertTrue(gcmd.find_three_best_similar_keywords(["dadada", "dada"]) == ["dada", "dadada", "N/A"])
        self.assertFalse(gcmd.find_three_best_similar_keywords(["dadada", "dada"]) == ["dadada", "dada", "N/A"])
        self.assertTrue(gcmd.find_three_best_similar_keywords(["N/A", "dadada"]) == ["dadada", "N/A", "N/A"])
        self.assertTrue(gcmd.find_three_best_similar_keywords(["N/A", "dadada", "da", "blah"]) == ["da", "blah", "dadada"])

    # THEME KEYWORDS
    def test_get_theme_keywords(self):
        self.assertTrue(len(self.themeKeywordsList) == 2)
        self.assertTrue("EARTH SCIENCE > OCEANS > OCEAN TEMPERATURE > SEA SURFACE TEMPERATURE" in self.themeKeywordsList)
        self.assertTrue("Earth Science > Oceans > Ocean Temperature > Sea Surface Temperature > Foundation Sea Surface Temperature" in self.themeKeywordsList)
        self.assertFalse("SATELLITE DATA" in self.themeKeywordsList)
        self.assertFalse("blah" in self.themeKeywordsList)

    def test_get_theme_keywords_thesauri(self):
        self.assertTrue(len(self.themeKeywordsThesauriList) == 2)
        self.assertTrue("Global Change Master Directory (GCMD) Science and Services Keywords" in self.themeKeywordsThesauriList)
        self.assertFalse("BLAH THESAURUS" in self.themeKeywordsThesauriList)
        self.assertTrue("NASA/GCMD Earth Science Keywords" in self.themeKeywordsThesauriList)
        self.assertFalse("blah" in self.themeKeywordsThesauriList)

    def test_get_model_theme_keywords_list(self):
        self.assertTrue(len(self.modelThemeKeywordsList) > 3150)
        self.assertTrue("EARTH SCIENCE > TERRESTRIAL HYDROSPHERE" in self.modelThemeKeywordsList)
        self.assertTrue("EARTH SCIENCE > ATMOSPHERE > WEATHER EVENTS > TROPICAL CYCLONES > MINIMUM CENTRAL PRESSURE > TYPHOONS (WESTERN N. PACIFIC)" in self.modelThemeKeywordsList)
        self.assertFalse("BLAH" in self.modelThemeKeywordsList)

    def test_get_similar_keywords(self):
        self.assertTrue(len(self.similarThemeKeywords) == 3)
        self.assertTrue("EARTH SCIENCE SERVICES > REFERENCE AND INFORMATION SERVICES > DIGITAL/VIRTUAL REFERENCE DESKS > ASK-A OCEANOGRAPHER" in self.similarThemeKeywords)
        self.assertTrue("N/A" in self.similarThemeKeywords)

    @unittest.skip("n flag breaks test")
    def test_check_theme_keywords(self):
        with open('invalid_GCMD_keywords_results_GHRSST-ABOM-L4HRfnd-AUS-RAMSSA_09km.csv') as f:
            s = f.read()
        self.assertTrue("Earth Science > Oceans > Ocean Temperature > Sea Surface Temperature > Foundation Sea Surface Temperature" in s)
        self.assertFalse("EARTH SCIENCE > OCEANS > OCEAN OPTICS" in s)

    # DATACENTER KEYWORDS
    def test_get_datacenter_keywords(self):
        self.assertTrue(len(self.datacenterKeywordsList) == 3)
        self.assertTrue("DOC/NOAA/NESDIS/NODC > National Oceanographic Data Center, NESDIS, NOAA, U.S. Department of Commerce" in self.datacenterKeywordsList)
        self.assertFalse("Blah NESDIS" in self.datacenterKeywordsList)
        self.assertTrue("NASA/JPL/PODAAC > Physical Oceanography Distributed Active Archive Center, Jet Propulsion Laboratory, NASA" in self.datacenterKeywordsList)
        self.assertFalse("Australian Bureau of Blah" in self.datacenterKeywordsList)

    def test_get_datacenter_keywords_thesauri(self):
        self.assertTrue(len(self.datacenterKeywordsThesauriList) == 1)
        self.assertTrue("Global Change Master Directory (GCMD) Data Center Keywords" in self.datacenterKeywordsThesauriList)
        self.assertFalse("GLOBAL CHANGE MASTER DIRECTORY (GCMD) DATA CENTER KEYWORDS" in self.datacenterKeywordsThesauriList)
        self.assertFalse("NODC COLLECTING INSTITUTION NAMES THESAURUS" in self.datacenterKeywordsThesauriList)

    def test_get_model_datacenter_keywords_list(self):
        self.assertTrue(len(self.modelDatacenterKeywordsList) > 3600)
        self.assertTrue("OR-STATE/EOARC > Eastern Oregon Agriculture Research Center, Oregon State University" in self.modelDatacenterKeywordsList)
        self.assertTrue("DOC/NOAA/OOE > Office of Ocean Exploration, National Oceanic and Atmospheric Administration, U.S. Department of Commerce" in self.modelDatacenterKeywordsList)
        self.assertFalse("BLAH" in self.modelDatacenterKeywordsList)

    def test_get_similar_keywords(self):
        self.assertTrue(len(self.similarDatacenterKeywords) == 3)
        self.assertTrue("DOC/NOAA/NESDIS/NCEI > National Centers for Environmental Information, NESDIS, NOAA, U.S. Department of Commerce" in self.similarDatacenterKeywords)
        self.assertTrue("N/A" in self.similarDatacenterKeywords)

    @unittest.skip("n flag breaks test")
    def test_check_datacenter_keywords(self):
        with open('invalid_GCMD_keywords_results_GHRSST-ABOM-L4HRfnd-AUS-RAMSSA_09km.csv') as f:
            s = f.read()
        self.assertFalse("AUSTRALIAN BUREAU OF METEOROLOGY" in s)
        self.assertFalse("DOC/NOAA/NESDIS/NCEI > National Centers for Environmental Information, NESDIS, NOAA, U.S. Department of Commerce" in s)

    # PLACE KEYWORDS
    def test_get_place_keywords(self):
        self.assertTrue(len(self.placeKeywordsList) == 9)
        self.assertTrue("OCEAN > INDIAN OCEAN" in self.placeKeywordsList)
        self.assertFalse("Bavaria" in self.placeKeywordsList)
        self.assertTrue("OCEAN > PACIFIC OCEAN > WESTERN PACIFIC OCEAN > SOUTH CHINA SEA" in self.placeKeywordsList)
        self.assertTrue("Oceania" in self.placeKeywordsList)

    def test_get_place_keywords_thesauri(self):
        self.assertTrue(len(self.placeKeywordsThesauriList) == 2)
        self.assertTrue("Global Change Master Directory (GCMD) Location Keywords" in self.placeKeywordsThesauriList)
        self.assertTrue("NASA/GCMD Location Keywords" in self.placeKeywordsThesauriList)
        self.assertFalse("NODC SEA AREA NAMES THESAURUS BLAH" in self.placeKeywordsThesauriList)

    def test_get_model_place_keywords_list(self):
        self.assertTrue(len(self.modelPlaceKeywordsList) > 500)
        self.assertTrue("CONTINENT > AFRICA > CENTRAL AFRICA > ANGOLA" in self.modelPlaceKeywordsList)
        self.assertTrue("CONTINENT > EUROPE > NORTHERN EUROPE > SCANDINAVIA > ALAND ISLANDS" in self.modelPlaceKeywordsList)
        self.assertFalse("OUTER SPACE > MARS" in self.modelPlaceKeywordsList)

    def test_get_similar_keywords(self):
        self.assertTrue(len(self.similarPlaceKeywords) == 3)
        self.assertTrue("OCEAN > INDIAN OCEAN > ARABIAN SEA" in self.similarPlaceKeywords)
        self.assertTrue("N/A" in self.similarPlaceKeywords)

    @unittest.skip("n flag breaks test")
    def test_check_place_keywords(self):
        with open('invalid_GCMD_keywords_results_GHRSST-ABOM-L4HRfnd-AUS-RAMSSA_09km.csv') as f:
            s = f.read()
        self.assertTrue("Oceania" in s)
        self.assertFalse("OCEAN > ATLANTIC OCEAN > SOUTH ATLANTIC OCEAN" in s)

    # PLATFORM KEYWORDS
    def test_get_platform_keywords(self):
        self.assertTrue(len(self.platformKeywordsList) == 9)
        self.assertTrue("AQUA > Earth Observing System, AQUA" in self.platformKeywordsList)
        self.assertFalse("Bavaria" in self.platformKeywordsList)
        self.assertTrue("METOP-A > Meteorological Operational Satellite - A" in self.platformKeywordsList)
        self.assertFalse("METOP-C" in self.platformKeywordsList)

    def test_get_platform_keywords_thesauri(self):
        self.assertTrue(len(self.platformKeywordsThesauriList) == 1)
        self.assertFalse("NODC PLATFORM NAMES THESAURUS BLAH" in self.platformKeywordsThesauriList)
        self.assertTrue("Global Change Master Directory (GCMD) Platform Keywords" in self.platformKeywordsThesauriList)
        self.assertFalse("PLATYPUS" in self.platformKeywordsThesauriList)

    def test_get_model_platform_keywords_list(self):
        self.assertTrue(len(self.modelPlatformKeywordsList) > 850)
        self.assertTrue("Aircraft > A340-600 > Airbus A340-600" in self.modelPlatformKeywordsList)
        self.assertTrue("Earth Observation Satellites > SCISAT-1/ACE > Atmospheric Chemistry Experiment" in self.modelPlatformKeywordsList)
        self.assertFalse("BLAH" in self.modelPlatformKeywordsList)

    def test_get_similar_keywords(self):
        self.assertTrue("Earth Observation Satellites > METOP > METOP-A > Meteorological Operational Satellite - A" in self.similarPlatformKeywords)
        self.assertTrue("N/A" in self.similarPlatformKeywords)

    @unittest.skip("n flag breaks test")
    def test_check_platform_keywords(self):
        with open('invalid_GCMD_keywords_results_GHRSST-ABOM-L4HRfnd-AUS-RAMSSA_09km.csv') as f:
            s = f.read()
        self.assertTrue("METOP-B" in s)
        self.assertFalse("CORIOLIS > CORIOLIS" in s)

    # INSTRUMENT KEYWORDS
    def test_get_instrument_keywords(self):
        self.assertTrue(len(self.instrumentKeywordsList) == 5)
        self.assertTrue("AATSR > Advanced Along-Track Scanning Radiometer" in self.instrumentKeywordsList)
        self.assertFalse("WINDSAT > Blah" in self.instrumentKeywordsList)
        self.assertTrue("AMSR-E > Advanced Microwave Scanning Radiometer-EOS" in self.instrumentKeywordsList)
        self.assertFalse("AATSR > ADVANCE ALONG-TRACK SCANNING" in self.instrumentKeywordsList)

    def test_get_instrument_keywords_thesauri(self):
        self.assertTrue(len(self.instrumentKeywordsThesauriList) == 1)
        self.assertTrue("Global Change Master Directory (GCMD) Instrument Keywords" in self.instrumentKeywordsThesauriList)
        self.assertFalse("NODC INSTRUMENT TYPES" in self.instrumentKeywordsThesauriList)

    def test_get_model_instrument_keywords_list(self):
        self.assertTrue(len(self.modelInstrumentKeywordsList) > 1500)
        self.assertTrue("Earth Remote Sensing Instruments > Active Remote Sensing > Altimeters > Lidar/Laser Altimeters > AIRBORNE LASER SCANNER" in self.modelInstrumentKeywordsList)
        self.assertTrue("Earth Remote Sensing Instruments > Passive Remote Sensing > Profilers/Sounders > HIWRAP > High-Altitude Imaging Wind and Rain Airborne Profiler" in self.modelInstrumentKeywordsList)
        self.assertFalse("SOME > INSTRUMENT > DUDE" in self.modelInstrumentKeywordsList)

    def test_get_similar_keywords(self):
        self.assertTrue(len(self.similarInstrumentKeywords) > 0)
        self.assertTrue("Earth Remote Sensing Instruments > Passive Remote Sensing > Spectrometers/Radiometers > Imaging Spectrometers/Radiometers > AVHRR-3 > Advanced Very High Resolution Radiometer-3" in self.similarInstrumentKeywords)
        self.assertTrue("N/A" in self.similarInstrumentKeywords)

    @unittest.skip("n flag breaks test")
    def test_check_instrument_keywords(self):
        with open('invalid_GCMD_keywords_results_GHRSST-ABOM-L4HRfnd-AUS-RAMSSA_09km.csv') as f:
            s = f.read()
        self.assertFalse("AATSR-NR" in s)
        self.assertFalse("BLAH" in s)

    # PROJECT KEYWORDS
    def test_get_project_keywords(self):
        self.assertTrue(len(self.projectKeywordsList) == 2)
        self.assertTrue("GHRSST > Group for High Resolution Sea Surface Temperature" in self.projectKeywordsList)
        self.assertFalse("GHRSST" in self.projectKeywordsList)
        self.assertTrue("NOAA OneStop Project" in self.projectKeywordsList)

    def test_get_project_keywords_thesauri(self):
        self.assertTrue(len(self.projectKeywordsThesauriList) == 1)
        self.assertFalse("NODC Project Names Thesaurus" in self.projectKeywordsThesauriList)
        self.assertTrue("Global Change Master Directory (GCMD) Project Keywords" in self.projectKeywordsThesauriList)

    def test_get_model_project_keywords_list(self):
        self.assertTrue(len(self.modelProjectKeywordsList) > 1700)
        self.assertTrue("AARDDVARK > Antarctic-Arctic Radiation-belt (Dynamic) Deposition - VLF Atmospheric Research Konsortium" in self.modelProjectKeywordsList)
        self.assertTrue("NOAA OneStop Project" in self.modelProjectKeywordsList)
        self.assertFalse("BLAH > Dude" in self.modelProjectKeywordsList)

    def test_get_similar_keywords(self):
        self.assertTrue(len(self.similarProjectKeywords) > 0)
        self.assertTrue("NOAA OneStop Project" in self.similarProjectKeywords)
        self.assertTrue("N/A" in self.similarProjectKeywords)

    @unittest.skip("n flag breaks test")
    def test_check_project_keywords(self):
        with open('invalid_GCMD_keywords_results_GHRSST-ABOM-L4HRfnd-AUS-RAMSSA_09km.csv') as f:
            s = f.read()
        self.assertFalse("NOAA OneStop Project" in s)
        self.assertFalse("AAE > Australasian Antarctic Expedition of 1911-14" in s)

# __main__
if __name__ == '__main__':
    unittest.main()
# End __main__
