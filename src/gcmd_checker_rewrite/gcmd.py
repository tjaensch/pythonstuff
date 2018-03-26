import csv
import fnmatch
from lxml import etree as et
import time
import os
from os.path import basename
import urllib2


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

    def create_results_csv(self, file):
        print(basename(os.path.splitext(file)[0]) + '.xml')
        with open(basename(os.path.splitext(file)[0]) + '.csv', 'wb') as out:
            writer = csv.writer(out)
            writer.writerow(["Invalid Keyword", "Type", "Filename"])

    # THEME KEYWORDS
    def get_theme_keywords(self, file):
        themeKeywordsList = []
        xmlRoot = et.fromstring(open(file).read())
        themeKeywords = xmlRoot.xpath(
            "//gmd:MD_DataIdentification/gmd:descriptiveKeywords/gmd:MD_Keywords[gmd:type/gmd:MD_KeywordTypeCode/@codeListValue='theme']/gmd:keyword/*",
                namespaces=xmlRoot.nsmap)
        for i in range(len(themeKeywords)):
            themeKeywordsList.append(themeKeywords[i].text.upper())
        #print(themeKeywordsList)
        return themeKeywordsList

    def get_theme_keywords_thesauri(self, file):
        themeKeywordsThesauriList = []
        xmlRoot = et.fromstring(open(file).read())
        themeKeywordsThesauri = xmlRoot.xpath(
            "//gmd:MD_DataIdentification/gmd:descriptiveKeywords/gmd:MD_Keywords[gmd:type/gmd:MD_KeywordTypeCode/@codeListValue='theme']/gmd:thesaurusName/gmd:CI_Citation/gmd:title/*",
                namespaces=xmlRoot.nsmap)
        for i in range(len(themeKeywordsThesauri)):
            themeKeywordsThesauriList.append(themeKeywordsThesauri[i].text.upper())
        #print(themeKeywordsThesauriList)
        return themeKeywordsThesauriList
    # END THEME KEYWORDS

    # DATA CENTER KEYWORDS
    def get_datacenter_keywords(self, file):
        datacenterKeywordsList = []
        xmlRoot = et.fromstring(open(file).read())
        datacenterKeywords = xmlRoot.xpath(
            "//gmd:MD_DataIdentification/gmd:descriptiveKeywords/gmd:MD_Keywords[gmd:type/gmd:MD_KeywordTypeCode/@codeListValue='dataCenter']/gmd:keyword/*",
                namespaces=xmlRoot.nsmap)
        for i in range(len(datacenterKeywords)):
            datacenterKeywordsList.append(datacenterKeywords[i].text.upper())
        #print(datacenterKeywordsList)
        return datacenterKeywordsList

    def get_datacenter_keywords_thesauri(self, file):
        datacenterKeywordsThesauriList = []
        xmlRoot = et.fromstring(open(file).read())
        datacenterKeywordsThesauri = xmlRoot.xpath(
            "//gmd:MD_DataIdentification/gmd:descriptiveKeywords/gmd:MD_Keywords[gmd:type/gmd:MD_KeywordTypeCode/@codeListValue='dataCenter']/gmd:thesaurusName/gmd:CI_Citation/gmd:title/*",
                namespaces=xmlRoot.nsmap)
        for i in range(len(datacenterKeywordsThesauri)):
            datacenterKeywordsThesauriList.append(datacenterKeywordsThesauri[i].text.upper())
        #print(datacenterKeywordsThesauriList)
        return datacenterKeywordsThesauriList

    def check_datacenter_keywords(self, file):
        modelDatacenterKeywordsList = []
        data = csv.reader(urllib2.urlopen("https://gcmdservices.gsfc.nasa.gov/static/kms/providers/providers.csv"))
        for row in data:
            try:
                modelDatacenterKeywordsList.append(row[4].upper()) # in case row[5] is blank
                modelDatacenterKeywordsList.append(row[4].upper() + " > " + row[5].upper()) # if value for both rows
            except IndexError:
                continue
        # check if file datacenter keywords are in modelDatacenterKeywordsList
        for keyword in self.get_datacenter_keywords(file):
            if keyword not in modelDatacenterKeywordsList:
                print("invalid datacenter keyword: " + keyword)
                with open(basename(os.path.splitext(file)[0]) + '.csv', 'a') as f:
                    writer = csv.writer(f)
                    writer.writerow([keyword, "datacenter", basename(os.path.splitext(file)[0]) + '.xml'])    
    # END DATACENTER KEYWORDS

    # PLACE KEYWORDS
    def get_place_keywords(self, file):
        placeKeywordsList = []
        xmlRoot = et.fromstring(open(file).read())
        placeKeywords = xmlRoot.xpath(
            "//gmd:MD_DataIdentification/gmd:descriptiveKeywords/gmd:MD_Keywords[gmd:type/gmd:MD_KeywordTypeCode/@codeListValue='place']/gmd:keyword/*",
                namespaces=xmlRoot.nsmap)
        for i in range(len(placeKeywords)):
            placeKeywordsList.append(placeKeywords[i].text.upper())
        #print(placeKeywordsList)
        return placeKeywordsList

    def get_place_keywords_thesauri(self, file):
        placeKeywordsThesauriList = []
        xmlRoot = et.fromstring(open(file).read())
        placeKeywordsThesauri = xmlRoot.xpath(
            "//gmd:MD_DataIdentification/gmd:descriptiveKeywords/gmd:MD_Keywords[gmd:type/gmd:MD_KeywordTypeCode/@codeListValue='place']/gmd:thesaurusName/gmd:CI_Citation/gmd:title/*",
                namespaces=xmlRoot.nsmap)
        for i in range(len(placeKeywordsThesauri)):
            placeKeywordsThesauriList.append(placeKeywordsThesauri[i].text.upper())
        #print(placeKeywordsThesauriList)
        return placeKeywordsThesauriList

    def check_place_keywords(self, file):
        modelPlaceKeywordsList = []
        data = csv.reader(urllib2.urlopen("https://gcmdservices.gsfc.nasa.gov/static/kms/locations/locations.csv"))
        for row in data:
            try:
                modelPlaceKeywordsList.append(row[0].upper()) # in case row[1] is blank
                modelPlaceKeywordsList.append(row[0].upper() + " > " + row[1].upper())
                modelPlaceKeywordsList.append(row[0].upper() + " > " + row[1].upper() + " > " + row[2].upper())
                modelPlaceKeywordsList.append(row[0].upper() + " > " + row[1].upper() + " > " + row[2].upper() + " > " + row[3].upper())
                modelPlaceKeywordsList.append(row[0].upper() + " > " + row[1].upper() + " > " + row[2].upper() + " > " + row[3].upper() + " > " + row[4].upper())
            except IndexError:
                continue
        # check if file place keywords are in modelPlatformKeywordsList
        for keyword in self.get_place_keywords(file):
            if keyword not in modelPlaceKeywordsList:
                print("invalid location keyword: " + keyword)
                with open(basename(os.path.splitext(file)[0]) + '.csv', 'a') as f:
                    writer = csv.writer(f)
                    writer.writerow([keyword, "location", basename(os.path.splitext(file)[0]) + '.xml'])    
    # END PLACE KEYWORDS
    
    # PLATFORM KEYWORDS
    def get_platform_keywords(self, file):
        platformKeywordsList = []
        xmlRoot = et.fromstring(open(file).read())
        platformKeywords = xmlRoot.xpath(
            "//gmd:MD_DataIdentification/gmd:descriptiveKeywords/gmd:MD_Keywords[gmd:type/gmd:MD_KeywordTypeCode/@codeListValue='platform']/gmd:keyword/*",
                namespaces=xmlRoot.nsmap)
        for i in range(len(platformKeywords)):
            platformKeywordsList.append(platformKeywords[i].text.upper())
        #print(platformKeywordsList)
        return platformKeywordsList

    def get_platform_keywords_thesauri(self, file):
        platformKeywordsThesauriList = []
        xmlRoot = et.fromstring(open(file).read())
        platformKeywordsThesauri = xmlRoot.xpath(
            "//gmd:MD_DataIdentification/gmd:descriptiveKeywords/gmd:MD_Keywords[gmd:type/gmd:MD_KeywordTypeCode/@codeListValue='platform']/gmd:thesaurusName/gmd:CI_Citation/gmd:title/*",
                namespaces=xmlRoot.nsmap)
        for i in range(len(platformKeywordsThesauri)):
            platformKeywordsThesauriList.append(platformKeywordsThesauri[i].text.upper())
        #print(platformKeywordsThesauriList)
        return platformKeywordsThesauriList

    def check_platform_keywords(self, file):
        modelPlatformKeywordsList = []
        data = csv.reader(urllib2.urlopen("https://gcmdservices.gsfc.nasa.gov/static/kms/platforms/platforms.csv"))
        for row in data:
            try:
                modelPlatformKeywordsList.append(row[2].upper()) # in case row[3] is blank
                modelPlatformKeywordsList.append(row[2].upper() + " > " + row[3].upper()) # if value for both rows
            except IndexError:
                continue
        # check if file platform keywords are in modelPlatformKeywordsList
        for keyword in self.get_platform_keywords(file):
            if keyword not in modelPlatformKeywordsList:
                print("invalid platform keyword: " + keyword)
                with open(basename(os.path.splitext(file)[0]) + '.csv', 'a') as f:
                    writer = csv.writer(f)
                    writer.writerow([keyword, "platform", basename(os.path.splitext(file)[0]) + '.xml'])    
    # END PLATFORM KEYWORDS
    
    # INSTRUMENT KEYWORDS
    def get_instrument_keywords(self, file):
        instrumentKeywordsList = []
        xmlRoot = et.fromstring(open(file).read())
        instrumentKeywords = xmlRoot.xpath(
            "//gmd:MD_DataIdentification/gmd:descriptiveKeywords/gmd:MD_Keywords[gmd:type/gmd:MD_KeywordTypeCode/@codeListValue='instrument']/gmd:keyword/*",
                namespaces=xmlRoot.nsmap)
        for i in range(len(instrumentKeywords)):
            instrumentKeywordsList.append(instrumentKeywords[i].text.upper())
        #print(instrumentKeywordsList)
        return instrumentKeywordsList

    def get_instrument_keywords_thesauri(self, file):
        instrumentKeywordsThesauriList = []
        xmlRoot = et.fromstring(open(file).read())
        instrumentKeywordsThesauri = xmlRoot.xpath(
            "//gmd:MD_DataIdentification/gmd:descriptiveKeywords/gmd:MD_Keywords[gmd:type/gmd:MD_KeywordTypeCode/@codeListValue='instrument']/gmd:thesaurusName/gmd:CI_Citation/gmd:title/*",
                namespaces=xmlRoot.nsmap)
        for i in range(len(instrumentKeywordsThesauri)):
            instrumentKeywordsThesauriList.append(instrumentKeywordsThesauri[i].text.upper())
        #print(instrumentKeywordsThesauriList)
        return instrumentKeywordsThesauriList

    def check_instrument_keywords(self, file):
        modelInstrumentKeywordsList = []
        data = csv.reader(urllib2.urlopen("https://gcmdservices.gsfc.nasa.gov/static/kms/instruments/instruments.csv"))
        for row in data:
            try:
                modelInstrumentKeywordsList.append(row[4].upper()) # in case row[5] is blank
                modelInstrumentKeywordsList.append(row[4].upper() + " > " + row[5].upper()) # if value for both rows
            except IndexError:
                continue
        # check if file instrument keywords are in modelInstrumentKeywordsList
        for keyword in self.get_instrument_keywords(file):
            if keyword not in modelInstrumentKeywordsList:
                print("invalid instrument keyword: " + keyword)
                with open(basename(os.path.splitext(file)[0]) + '.csv', 'a') as f:
                    writer = csv.writer(f)
                    writer.writerow([keyword, "instrument", basename(os.path.splitext(file)[0]) + '.xml'])
    # END INSTRUMENT KEYWORDS
    
    # PROJECT KEYWORDS
    def get_project_keywords(self, file):
        projectKeywordsList = []
        xmlRoot = et.fromstring(open(file).read())
        projectKeywords = xmlRoot.xpath(
            "//gmd:MD_DataIdentification/gmd:descriptiveKeywords/gmd:MD_Keywords[gmd:type/gmd:MD_KeywordTypeCode/@codeListValue='project']/gmd:keyword/*",
                namespaces=xmlRoot.nsmap)
        for i in range(len(projectKeywords)):
            projectKeywordsList.append(projectKeywords[i].text.upper())
        #print(projectKeywordsList)
        return projectKeywordsList

    def get_project_keywords_thesauri(self, file):
        projectKeywordsThesauriList = []
        xmlRoot = et.fromstring(open(file).read())
        projectKeywordsThesauri = xmlRoot.xpath(
            "//gmd:MD_DataIdentification/gmd:descriptiveKeywords/gmd:MD_Keywords[gmd:type/gmd:MD_KeywordTypeCode/@codeListValue='project']/gmd:thesaurusName/gmd:CI_Citation/gmd:title/*",
                namespaces=xmlRoot.nsmap)
        for i in range(len(projectKeywordsThesauri)):
            projectKeywordsThesauriList.append(projectKeywordsThesauri[i].text.upper())
        #print(projectKeywordsThesauriList)
        return projectKeywordsThesauriList

    def check_project_keywords(self, file):
        modelProjectKeywordsList = []
        data = csv.reader(urllib2.urlopen("https://gcmdservices.gsfc.nasa.gov/static/kms/projects/projects.csv"))
        for row in data:
            try:
                modelProjectKeywordsList.append(row[1].upper()) # in case row[2] is blank
                modelProjectKeywordsList.append(row[1].upper() + " > " + row[2].upper()) # if value for both rows
            except IndexError:
                continue
        # check if file project keywords are in modelProjectKeywordsList
        for keyword in self.get_project_keywords(file):
            if keyword not in modelProjectKeywordsList:
                print("invalid project keyword: " + keyword)
                with open(basename(os.path.splitext(file)[0]) + '.csv', 'a') as f:
                    writer = csv.writer(f)
                    writer.writerow([keyword, "project", basename(os.path.splitext(file)[0]) + '.xml'])
    # END PROJECT KEYWORDS

# __main__
if __name__ == '__main__':
    start = time.time()

    gcmd = GCMD()
    testfile = "./collection_test_files/GHRSST-ABOM-L4HRfnd-AUS-RAMSSA_09km.xml" 

    gcmd.create_results_csv(testfile)
    
    gcmd.check_datacenter_keywords(testfile)
    gcmd.check_place_keywords(testfile)
    gcmd.check_platform_keywords(testfile)
    gcmd.check_instrument_keywords(testfile)
    gcmd.check_project_keywords(testfile)
    

    print('The program took ', time.time() - start, 'seconds to complete.')

# End __main__
