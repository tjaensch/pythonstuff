import csv
import fnmatch
import time
import os
import urllib2
from lxml import etree as et
from os.path import basename


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
        with open('invalid_GCMD_keywords_results_' + basename(os.path.splitext(file)[0]) + '.csv', 'wb') as out:
            writer = csv.writer(out)
            writer.writerow(["Invalid Keyword", "Type", "Filename", "Recommendation 1", "Recommendation 2", "Recommendation 3"])

    # THEME KEYWORDS
    def get_theme_keywords(self, file):
        themeKeywordsList = []
        xmlRoot = et.fromstring(open(file).read())
        themeKeywords = xmlRoot.xpath(
            "//gmd:MD_DataIdentification/gmd:descriptiveKeywords/gmd:MD_Keywords[gmd:type/gmd:MD_KeywordTypeCode/@codeListValue='theme']/gmd:keyword/*",
                namespaces=xmlRoot.nsmap)
        for i in range(len(themeKeywords)):
            themeKeywordsList.append(themeKeywords[i].text.upper())
        print(themeKeywordsList)
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

    def get_model_theme_keywords_list(self):
        modelThemeKeywordsList = []
        data = csv.reader(urllib2.urlopen("https://gcmdservices.gsfc.nasa.gov/static/kms/sciencekeywords/sciencekeywords.csv"))
        for row in data:
            keyword = row[0].upper().strip()
            for i in range(1,7):
                try:
                    if row[i] != "":
                        keyword = keyword + " > " + row[i].upper().strip()
                except IndexError:
                    continue
            modelThemeKeywordsList.append(keyword)    

        #print(modelThemeKeywordsList)
        return modelThemeKeywordsList

    def check_theme_keywords(self, file):
        modelThemeKeywordsList = self.get_model_theme_keywords_list()
        themeKeywordsList = self.get_theme_keywords(file)
        # check if file theme keywords are in modelThemeKeywordsList
        for keyword in themeKeywordsList:
            if keyword not in modelThemeKeywordsList:
                print("invalid theme keyword: " + keyword)
                # find similar keywords
                similarKeywords = self.get_similar_place_keywords(modelThemeKeywordsList, keyword)
                with open('invalid_GCMD_keywords_results_' + basename(os.path.splitext(file)[0]) + '.csv', 'a') as f:
                    writer = csv.writer(f)
                    writer.writerow([keyword, "theme", basename(os.path.splitext(file)[0]) + '.xml', similarKeywords[0], similarKeywords[1], similarKeywords[2]]) 

    def get_similar_theme_keywords(self, modelThemeKeywordsList, keyword):
        similarKeywords = [s for s in modelThemeKeywordsList if keyword in s]
        # make set to remove duplicates and back to list to be able to access elements 
        list(set(similarKeywords))
        similarKeywordsList = []
        for i in range(0,3):
            try:
                similarKeywordsList.append(similarKeywords[i])
            except IndexError:
                similarKeywordsList.append("N/A")
        # if no matches with the above method try first half of keyword string
        if (len(set(similarKeywordsList)) <= 1):
            similarKeywordsList = []
            keywordSubstring = keyword[0:len(keyword)/2]
            similarKeywords = [s for s in modelThemeKeywordsList if keywordSubstring in s]
            for i in range(0,3):
                try:
                    similarKeywordsList.append(similarKeywords[i])
                except IndexError:
                    similarKeywordsList.append("N/A")
        # if no matches with the above method try first third of keyword string
        if (len(set(similarKeywordsList)) <= 1):
            similarKeywordsList = []
            keywordSubstring = keyword[0:len(keyword)/3]
            similarKeywords = [s for s in modelThemeKeywordsList if keywordSubstring in s]
            for i in range(0,3):
                try:
                    similarKeywordsList.append(similarKeywords[i])
                except IndexError:
                    similarKeywordsList.append("N/A")

        #print(similarKeywordsList)
        return similarKeywordsList  
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

    def get_model_datacenter_keywords_list(self):
        modelDatacenterKeywordsList = []
        data = csv.reader(urllib2.urlopen("https://gcmdservices.gsfc.nasa.gov/static/kms/providers/providers.csv"))
        for row in data:
            keyword = row[0].upper().strip()
            for i in range(1,6):
                try:
                    if row[i] != "":
                        keyword = keyword + " > " + row[i].upper().strip()
                except IndexError:
                    continue
            modelDatacenterKeywordsList.append(keyword)    

        #print(modelDatacenterKeywordsList)
        return modelDatacenterKeywordsList

    def check_datacenter_keywords(self, file):
            modelDatacenterKeywordsList = self.get_model_datacenter_keywords_list()
            datacenterKeywordsList = self.get_datacenter_keywords(file)
            # check if file datacenter keywords are in modelDatacenterKeywordsList
            for keyword in datacenterKeywordsList:
                if keyword not in modelDatacenterKeywordsList:
                    print("invalid datacenter keyword: " + keyword)
                    # find similar keywords
                    similarKeywords = self.get_similar_place_keywords(modelDatacenterKeywordsList, keyword)
                    with open('invalid_GCMD_keywords_results_' + basename(os.path.splitext(file)[0]) + '.csv', 'a') as f:
                        writer = csv.writer(f)
                        writer.writerow([keyword, "datacenter", basename(os.path.splitext(file)[0]) + '.xml', similarKeywords[0], similarKeywords[1], similarKeywords[2]]) 

    def get_similar_datacenter_keywords(self, modelDatacenterKeywordsList, keyword):
        similarKeywords = [s for s in modelDatacenterKeywordsList if keyword in s]
        # make set to remove duplicates and back to list to be able to access elements 
        list(set(similarKeywords))
        similarKeywordsList = []
        for i in range(0,3):
            try:
                similarKeywordsList.append(similarKeywords[i])
            except IndexError:
                similarKeywordsList.append("N/A")
        # if no matches with the above method try first half of keyword string
        if (len(set(similarKeywordsList)) <= 1):
            similarKeywordsList = []
            keywordSubstring = keyword[0:len(keyword)/2]
            similarKeywords = [s for s in modelDatacenterKeywordsList if keywordSubstring in s]
            for i in range(0,3):
                try:
                    similarKeywordsList.append(similarKeywords[i])
                except IndexError:
                    similarKeywordsList.append("N/A")
        # if no matches with the above method try first third of keyword string
        if (len(set(similarKeywordsList)) <= 1):
            similarKeywordsList = []
            keywordSubstring = keyword[0:len(keyword)/3]
            similarKeywords = [s for s in modelDatacenterKeywordsList if keywordSubstring in s]
            for i in range(0,3):
                try:
                    similarKeywordsList.append(similarKeywords[i])
                except IndexError:
                    similarKeywordsList.append("N/A")

        #print(similarKeywordsList)
        return similarKeywordsList
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

    def get_model_place_keywords_list(self):
        modelPlaceKeywordsList = []
        data = csv.reader(urllib2.urlopen("https://gcmdservices.gsfc.nasa.gov/static/kms/locations/locations.csv"))
        for row in data:
            keyword = row[0].upper().strip()
            for i in range(1,5):
                try:
                    if row[i] != "":
                        keyword = keyword + " > " + row[i].upper().strip()
                except IndexError:
                    continue
            modelPlaceKeywordsList.append(keyword)    

        #print(modelPlaceKeywordsList)
        return modelPlaceKeywordsList

    def check_place_keywords(self, file):
        modelPlaceKeywordsList = self.get_model_place_keywords_list()
        placeKeywordsList = self.get_place_keywords(file)
        # check if file place keywords are in modelPlaceKeywordsList
        for keyword in placeKeywordsList:
            if keyword not in modelPlaceKeywordsList:
                print("invalid place keyword: " + keyword)
                # find similar keywords
                similarKeywords = self.get_similar_place_keywords(modelPlaceKeywordsList, keyword)
                with open('invalid_GCMD_keywords_results_' + basename(os.path.splitext(file)[0]) + '.csv', 'a') as f:
                    writer = csv.writer(f)
                    writer.writerow([keyword, "place", basename(os.path.splitext(file)[0]) + '.xml', similarKeywords[0], similarKeywords[1], similarKeywords[2]])

    def get_similar_place_keywords(self, modelPlaceKeywordsList, keyword):
        similarKeywords = [s for s in modelPlaceKeywordsList if keyword in s]
        # make set to remove duplicates and back to list to be able to access elements 
        list(set(similarKeywords))
        similarKeywordsList = []
        for i in range(0,3):
            try:
                similarKeywordsList.append(similarKeywords[i])
            except IndexError:
                similarKeywordsList.append("N/A")
        # if no matches with the above method try first half of keyword string
        if (len(set(similarKeywordsList)) <= 1):
            similarKeywordsList = []
            keywordSubstring = keyword[0:len(keyword)/2]
            similarKeywords = [s for s in modelPlaceKeywordsList if keywordSubstring in s]
            for i in range(0,3):
                try:
                    similarKeywordsList.append(similarKeywords[i])
                except IndexError:
                    similarKeywordsList.append("N/A")
        # if no matches with the above method try first third of keyword string
        if (len(set(similarKeywordsList)) <= 1):
            similarKeywordsList = []
            keywordSubstring = keyword[0:len(keyword)/3]
            similarKeywords = [s for s in modelPlaceKeywordsList if keywordSubstring in s]
            for i in range(0,3):
                try:
                    similarKeywordsList.append(similarKeywords[i])
                except IndexError:
                    similarKeywordsList.append("N/A")

        #print(similarKeywordsList)
        return similarKeywordsList

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

    def get_model_platform_keywords_list(self):
        modelPlatformKeywordsList = []
        data = csv.reader(urllib2.urlopen("https://gcmdservices.gsfc.nasa.gov/static/kms/platforms/platforms.csv"))
        for row in data:
            keyword = row[0].upper().strip()
            for i in range(1,4):
                try:
                    if row[i] != "":
                        keyword = keyword + " > " + row[i].upper().strip()
                except IndexError:
                    continue
            modelPlatformKeywordsList.append(keyword)    

        #print(modelPlatformKeywordsList)
        return modelPlatformKeywordsList

    def check_platform_keywords(self, file):
        modelPlatformKeywordsList = self.get_model_platform_keywords_list()
        platformKeywordsList = self.get_platform_keywords(file)
        # check if file platform keywords are in modelPlatformKeywordsList
        for keyword in platformKeywordsList:
            if keyword not in modelPlatformKeywordsList:
                print("invalid platform keyword: " + keyword)
                # find similar keywords
                similarKeywords = self.get_similar_place_keywords(modelPlatformKeywordsList, keyword)
                with open('invalid_GCMD_keywords_results_' + basename(os.path.splitext(file)[0]) + '.csv', 'a') as f:
                    writer = csv.writer(f)
                    writer.writerow([keyword, "platform", basename(os.path.splitext(file)[0]) + '.xml', similarKeywords[0], similarKeywords[1], similarKeywords[2]])

    def get_similar_platform_keywords(self, modelPlatformKeywordsList, keyword):
        similarKeywords = [s for s in modelPlatformKeywordsList if keyword in s]
        # make set to remove duplicates and back to list to be able to access elements 
        list(set(similarKeywords))
        similarKeywordsList = []
        for i in range(0,3):
            try:
                similarKeywordsList.append(similarKeywords[i])
            except IndexError:
                similarKeywordsList.append("N/A")
        # if no matches with the above method try first half of keyword string
        if (len(set(similarKeywordsList)) <= 1):
            similarKeywordsList = []
            keywordSubstring = keyword[0:len(keyword)/2]
            similarKeywords = [s for s in modelPlatformKeywordsList if keywordSubstring in s]
            for i in range(0,3):
                try:
                    similarKeywordsList.append(similarKeywords[i])
                except IndexError:
                    similarKeywordsList.append("N/A")
        # if no matches with the above method try first third of keyword string
        if (len(set(similarKeywordsList)) <= 1):
            similarKeywordsList = []
            keywordSubstring = keyword[0:len(keyword)/3]
            similarKeywords = [s for s in modelPlatformKeywordsList if keywordSubstring in s]
            for i in range(0,3):
                try:
                    similarKeywordsList.append(similarKeywords[i])
                except IndexError:
                    similarKeywordsList.append("N/A")

        #print(similarKeywordsList)
        return similarKeywordsList  
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

    def get_model_instrument_keywords_list(self):
        modelInstrumentKeywordsList = []
        data = csv.reader(urllib2.urlopen("https://gcmdservices.gsfc.nasa.gov/static/kms/instruments/instruments.csv"))
        for row in data:
            keyword = row[0].upper().strip()
            for i in range(1,6):
                try:
                    if row[i] != "":
                        keyword = keyword + " > " + row[i].upper().strip()
                except IndexError:
                    continue
            modelInstrumentKeywordsList.append(keyword)    

        #print(modelInstrumentKeywordsList)
        return modelInstrumentKeywordsList

    def check_instrument_keywords(self, file):
        modelInstrumentKeywordsList = self.get_model_instrument_keywords_list()
        instrumentKeywordsList = self.get_instrument_keywords(file)
        # check if file instrument keywords are in modelInstrumentKeywordsList
        for keyword in instrumentKeywordsList:
            if keyword not in modelInstrumentKeywordsList:
                print("invalid instrument keyword: " + keyword)
                # find similar keywords
                similarKeywords = self.get_similar_place_keywords(modelInstrumentKeywordsList, keyword)
                with open('invalid_GCMD_keywords_results_' + basename(os.path.splitext(file)[0]) + '.csv', 'a') as f:
                    writer = csv.writer(f)
                    writer.writerow([keyword, "instrument", basename(os.path.splitext(file)[0]) + '.xml', similarKeywords[0], similarKeywords[1], similarKeywords[2]])

    def get_similar_instrument_keywords(self, modelInstrumentKeywordsList, keyword):
        similarKeywords = [s for s in modelInstrumentKeywordsList if keyword in s]
        # make set to remove duplicates and back to list to be able to access elements 
        list(set(similarKeywords))
        similarKeywordsList = []
        for i in range(0,3):
            try:
                similarKeywordsList.append(similarKeywords[i])
            except IndexError:
                similarKeywordsList.append("N/A")
        # if no matches with the above method try first half of keyword string
        if (len(set(similarKeywordsList)) <= 1):
            similarKeywordsList = []
            keywordSubstring = keyword[0:len(keyword)/2]
            similarKeywords = [s for s in modelInstrumentKeywordsList if keywordSubstring in s]
            for i in range(0,3):
                try:
                    similarKeywordsList.append(similarKeywords[i])
                except IndexError:
                    similarKeywordsList.append("N/A")
        # if no matches with the above method try first third of keyword string
        if (len(set(similarKeywordsList)) <= 1):
            similarKeywordsList = []
            keywordSubstring = keyword[0:len(keyword)/3]
            similarKeywords = [s for s in modelInstrumentKeywordsList if keywordSubstring in s]
            for i in range(0,3):
                try:
                    similarKeywordsList.append(similarKeywords[i])
                except IndexError:
                    similarKeywordsList.append("N/A")

        #print(similarKeywordsList)
        return similarKeywordsList 
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

    def get_model_project_keywords_list(self):
        modelProjectKeywordsList = []
        data = csv.reader(urllib2.urlopen("https://gcmdservices.gsfc.nasa.gov/static/kms/projects/projects.csv"))
        for row in data:
            keyword = row[0].upper().strip()
            for i in range(1,3):
                try:
                    if row[i] != "":
                        keyword = keyword + " > " + row[i].upper().strip()
                except IndexError:
                    continue
            modelProjectKeywordsList.append(keyword)    

        #print(modelProjectKeywordsList)
        return modelProjectKeywordsList

    def check_project_keywords(self, file):
        modelProjectKeywordsList = self.get_model_project_keywords_list()
        projectKeywordsList = self.get_project_keywords(file)
        # check if file project keywords are in modelProjectKeywordsList
        for keyword in projectKeywordsList:
            if keyword not in modelProjectKeywordsList:
                print("invalid project keyword: " + keyword)
                # find similar keywords
                similarKeywords = self.get_similar_place_keywords(modelProjectKeywordsList, keyword)
                with open('invalid_GCMD_keywords_results_' + basename(os.path.splitext(file)[0]) + '.csv', 'a') as f:
                    writer = csv.writer(f)
                    writer.writerow([keyword, "project", basename(os.path.splitext(file)[0]) + '.xml', similarKeywords[0], similarKeywords[1], similarKeywords[2]])

    def get_similar_project_keywords(self, modelProjectKeywordsList, keyword):
        similarKeywords = [s for s in modelProjectKeywordsList if keyword in s]
        # make set to remove duplicates and back to list to be able to access elements 
        list(set(similarKeywords))
        similarKeywordsList = []
        for i in range(0,3):
            try:
                similarKeywordsList.append(similarKeywords[i])
            except IndexError:
                similarKeywordsList.append("N/A")
        # if no matches with the above method try first half of keyword string
        if (len(set(similarKeywordsList)) <= 1):
            similarKeywordsList = []
            keywordSubstring = keyword[0:len(keyword)/2]
            similarKeywords = [s for s in modelProjectKeywordsList if keywordSubstring in s]
            for i in range(0,3):
                try:
                    similarKeywordsList.append(similarKeywords[i])
                except IndexError:
                    similarKeywordsList.append("N/A")
        # if no matches with the above method try first third of keyword string
        if (len(set(similarKeywordsList)) <= 1):
            similarKeywordsList = []
            keywordSubstring = keyword[0:len(keyword)/3]
            similarKeywords = [s for s in modelProjectKeywordsList if keywordSubstring in s]
            for i in range(0,3):
                try:
                    similarKeywordsList.append(similarKeywords[i])
                except IndexError:
                    similarKeywordsList.append("N/A")

        #print(similarKeywordsList)
        return similarKeywordsList  
    # END PROJECT KEYWORDS

# __main__
if __name__ == '__main__':
    start = time.time()

    gcmd = GCMD()
    #testfile = "./collection_test_files/GHRSST-ABOM-L4HRfnd-AUS-RAMSSA_09km.xml" 
    testfile = "./collection_test_files/GHRSST-ABOM-L4LRfnd-GLOB-GAMSSA_28km.xml" 

    '''xmlFiles = gcmd.find_xml_files()

    for testfile in xmlFiles:

        gcmd.create_results_csv(testfile)
        
        gcmd.check_project_keywords(testfile)
        gcmd.check_datacenter_keywords(testfile)
        gcmd.check_platform_keywords(testfile)
        gcmd.check_instrument_keywords(testfile)
        gcmd.check_theme_keywords(testfile)
        gcmd.check_place_keywords(testfile)'''

    '''gcmd.create_results_csv(testfile)
    
    gcmd.check_project_keywords(testfile)
    gcmd.check_datacenter_keywords(testfile)
    gcmd.check_platform_keywords(testfile)
    gcmd.check_instrument_keywords(testfile)
    gcmd.check_theme_keywords(testfile)
    gcmd.check_place_keywords(testfile)'''

    gcmd.get_theme_keywords(testfile)
    

    print('The program took ', time.time() - start, 'seconds to complete.')

# End __main__
