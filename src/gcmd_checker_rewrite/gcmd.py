import fnmatch
import glob
import itertools
from lxml import etree as et
import time
import os


class GCMD:
    """docstring for gcmd"""

    def __init__(self):
        self.xmlFiles = []

    def find_xml_files(self):
        source_dir = "./collection_test_files"
        for root, dirnames, filenames in os.walk(source_dir, followlinks=True):
            for filename in fnmatch.filter(filenames, '*.xml'):
                self.xmlFiles.append(os.path.join(root, filename))
        print("%d files found in source directory" % len(self.xmlFiles))
        return self.xmlFiles

    def get_all_GCMD_keywords(self, file):
        allKeywords = itertools.chain(self.get_theme_keywords(file), self.get_theme_keywords_thesauri(file), self.get_datacenter_keywords(file), self.get_datacenter_keywords_thesauri(file), self.get_place_keywords(file), self.get_place_keywords_thesauri(file), self.get_platform_keywords(file), self.get_platform_keywords_thesauri(file), self.get_instrument_keywords(file), self.get_instrument_keywords_thesauri(file), self.get_project_keywords(file), self.get_project_keywords_thesauri(file))
        #print(list(allKeywords))
        return list(allKeywords)

    def get_theme_keywords(self, file):
        themeKeywordsList = []
        xmlRoot = et.fromstring(open(file).read())
        themeKeywords = xmlRoot.xpath(
            "//gmd:MD_DataIdentification/gmd:descriptiveKeywords/gmd:MD_Keywords[gmd:type/gmd:MD_KeywordTypeCode/@codeListValue='theme']/gmd:keyword/*",
                namespaces=xmlRoot.nsmap)
        for i in range(len(themeKeywords)):
            themeKeywordsList.append(themeKeywords[i].text)
        #print(themeKeywordsList)
        return themeKeywordsList

    def get_theme_keywords_thesauri(self, file):
        themeKeywordsThesauriList = []
        xmlRoot = et.fromstring(open(file).read())
        themeKeywordsThesauri = xmlRoot.xpath(
            "//gmd:MD_DataIdentification/gmd:descriptiveKeywords/gmd:MD_Keywords[gmd:type/gmd:MD_KeywordTypeCode/@codeListValue='theme']/gmd:thesaurusName/gmd:CI_Citation/gmd:title/*",
                namespaces=xmlRoot.nsmap)
        for i in range(len(themeKeywordsThesauri)):
            themeKeywordsThesauriList.append(themeKeywordsThesauri[i].text)
        #print(themeKeywordsThesauriList)
        return themeKeywordsThesauriList

    def get_datacenter_keywords(self, file):
        datacenterKeywordsList = []
        xmlRoot = et.fromstring(open(file).read())
        datacenterKeywords = xmlRoot.xpath(
            "//gmd:MD_DataIdentification/gmd:descriptiveKeywords/gmd:MD_Keywords[gmd:type/gmd:MD_KeywordTypeCode/@codeListValue='dataCenter']/gmd:keyword/*",
                namespaces=xmlRoot.nsmap)
        for i in range(len(datacenterKeywords)):
            datacenterKeywordsList.append(datacenterKeywords[i].text)
        #print(datacenterKeywordsList)
        return datacenterKeywordsList

    def get_datacenter_keywords_thesauri(self, file):
        datacenterKeywordsThesauriList = []
        xmlRoot = et.fromstring(open(file).read())
        datacenterKeywordsThesauri = xmlRoot.xpath(
            "//gmd:MD_DataIdentification/gmd:descriptiveKeywords/gmd:MD_Keywords[gmd:type/gmd:MD_KeywordTypeCode/@codeListValue='dataCenter']/gmd:thesaurusName/gmd:CI_Citation/gmd:title/*",
                namespaces=xmlRoot.nsmap)
        for i in range(len(datacenterKeywordsThesauri)):
            datacenterKeywordsThesauriList.append(datacenterKeywordsThesauri[i].text)
        #print(datacenterKeywordsThesauriList)
        return datacenterKeywordsThesauriList

    def get_place_keywords(self, file):
        placeKeywordsList = []
        xmlRoot = et.fromstring(open(file).read())
        placeKeywords = xmlRoot.xpath(
            "//gmd:MD_DataIdentification/gmd:descriptiveKeywords/gmd:MD_Keywords[gmd:type/gmd:MD_KeywordTypeCode/@codeListValue='place']/gmd:keyword/*",
                namespaces=xmlRoot.nsmap)
        for i in range(len(placeKeywords)):
            placeKeywordsList.append(placeKeywords[i].text)
        #print(placeKeywordsList)
        return placeKeywordsList

    def get_place_keywords_thesauri(self, file):
        placeKeywordsThesauriList = []
        xmlRoot = et.fromstring(open(file).read())
        placeKeywordsThesauri = xmlRoot.xpath(
            "//gmd:MD_DataIdentification/gmd:descriptiveKeywords/gmd:MD_Keywords[gmd:type/gmd:MD_KeywordTypeCode/@codeListValue='place']/gmd:thesaurusName/gmd:CI_Citation/gmd:title/*",
                namespaces=xmlRoot.nsmap)
        for i in range(len(placeKeywordsThesauri)):
            placeKeywordsThesauriList.append(placeKeywordsThesauri[i].text)
        #print(placeKeywordsThesauriList)
        return placeKeywordsThesauriList

    def get_platform_keywords(self, file):
        platformKeywordsList = []
        xmlRoot = et.fromstring(open(file).read())
        platformKeywords = xmlRoot.xpath(
            "//gmd:MD_DataIdentification/gmd:descriptiveKeywords/gmd:MD_Keywords[gmd:type/gmd:MD_KeywordTypeCode/@codeListValue='platform']/gmd:keyword/*",
                namespaces=xmlRoot.nsmap)
        for i in range(len(platformKeywords)):
            platformKeywordsList.append(platformKeywords[i].text)
        #print(platformKeywordsList)
        return platformKeywordsList

    def get_platform_keywords_thesauri(self, file):
        platformKeywordsThesauriList = []
        xmlRoot = et.fromstring(open(file).read())
        platformKeywordsThesauri = xmlRoot.xpath(
            "//gmd:MD_DataIdentification/gmd:descriptiveKeywords/gmd:MD_Keywords[gmd:type/gmd:MD_KeywordTypeCode/@codeListValue='platform']/gmd:thesaurusName/gmd:CI_Citation/gmd:title/*",
                namespaces=xmlRoot.nsmap)
        for i in range(len(platformKeywordsThesauri)):
            platformKeywordsThesauriList.append(platformKeywordsThesauri[i].text)
        #print(platformKeywordsThesauriList)
        return platformKeywordsThesauriList

    def get_instrument_keywords(self, file):
        instrumentKeywordsList = []
        xmlRoot = et.fromstring(open(file).read())
        instrumentKeywords = xmlRoot.xpath(
            "//gmd:MD_DataIdentification/gmd:descriptiveKeywords/gmd:MD_Keywords[gmd:type/gmd:MD_KeywordTypeCode/@codeListValue='instrument']/gmd:keyword/*",
                namespaces=xmlRoot.nsmap)
        for i in range(len(instrumentKeywords)):
            instrumentKeywordsList.append(instrumentKeywords[i].text)
        #print(instrumentKeywordsList)
        return instrumentKeywordsList

    def get_instrument_keywords_thesauri(self, file):
        instrumentKeywordsThesauriList = []
        xmlRoot = et.fromstring(open(file).read())
        instrumentKeywordsThesauri = xmlRoot.xpath(
            "//gmd:MD_DataIdentification/gmd:descriptiveKeywords/gmd:MD_Keywords[gmd:type/gmd:MD_KeywordTypeCode/@codeListValue='instrument']/gmd:thesaurusName/gmd:CI_Citation/gmd:title/*",
                namespaces=xmlRoot.nsmap)
        for i in range(len(instrumentKeywordsThesauri)):
            instrumentKeywordsThesauriList.append(instrumentKeywordsThesauri[i].text)
        print(instrumentKeywordsThesauriList)
        return instrumentKeywordsThesauriList

    def get_project_keywords(self, file):
        projectKeywordsList = []
        xmlRoot = et.fromstring(open(file).read())
        projectKeywords = xmlRoot.xpath(
            "//gmd:MD_DataIdentification/gmd:descriptiveKeywords/gmd:MD_Keywords[gmd:type/gmd:MD_KeywordTypeCode/@codeListValue='project']/gmd:keyword/*",
                namespaces=xmlRoot.nsmap)
        for i in range(len(projectKeywords)):
            projectKeywordsList.append(projectKeywords[i].text)
        #print(projectKeywordsList)
        return projectKeywordsList

    def get_project_keywords_thesauri(self, file):
        projectKeywordsThesauriList = []
        xmlRoot = et.fromstring(open(file).read())
        projectKeywordsThesauri = xmlRoot.xpath(
            "//gmd:MD_DataIdentification/gmd:descriptiveKeywords/gmd:MD_Keywords[gmd:type/gmd:MD_KeywordTypeCode/@codeListValue='project']/gmd:thesaurusName/gmd:CI_Citation/gmd:title/*",
                namespaces=xmlRoot.nsmap)
        for i in range(len(projectKeywordsThesauri)):
            projectKeywordsThesauriList.append(projectKeywordsThesauri[i].text)
        #print(projectKeywordsThesauriList)
        return projectKeywordsThesauriList

# __main__
if __name__ == '__main__':
    start = time.time()

    gcmd = GCMD()
    testfile = "./collection_test_files/GHRSST-ABOM-L4HRfnd-AUS-RAMSSA_09km.xml" 

    '''gcmd.get_theme_keywords(testfile)
    gcmd.get_theme_keywords_thesauri(testfile)
    gcmd.get_datacenter_keywords(testfile)
    gcmd.get_datacenter_keywords_thesauri(testfile)
    gcmd.get_place_keywords(testfile)
    gcmd.get_place_keywords_thesauri(testfile)
    gcmd.get_platform_keywords(testfile)
    gcmd.get_platform_keywords_thesauri(testfile)
    gcmd.get_instrument_keywords(testfile)
    gcmd.get_instrument_keywords_thesauri(testfile)
    gcmd.get_project_keywords(testfile)
    gcmd.get_project_keywords_thesauri(testfile)'''

    gcmd.get_all_GCMD_keywords(testfile)

    print('The program took ', time.time() - start, 'seconds to complete.')

# End __main__
