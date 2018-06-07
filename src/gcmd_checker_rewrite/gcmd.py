import argparse
import csv
import filecmp
import fnmatch
import time
import os
import shutil
import urllib2
from lxml import etree as et
from os.path import basename
from shutil import copyfile


class GCMD:
    """
    GCMD keyword checker that checks for invalid GCMD <gmd:thesaurusName> keywords in ISO metadata XML files according to the CSV specs from here https://gcmdservices.gsfc.nasa.gov/static/kms/ 
    Questions/issues: thomas.jaensch@noaa.gov
    """

    def __init__(self):
        pass

    def get_flag_arguments(self):
        ap = argparse.ArgumentParser()
        ap.add_argument("-t", "--target", required=True, help="target file or folder")
        ap.add_argument("-n", "--new", action='store_true', help="make XML copy of original target file/s with improved GCMD keywords which will be saved into 'improved_xml' subfolder of current directory")
        args = vars(ap.parse_args())
        return args

    def process(self, xmlFile):
        try:
            print('processing ' + basename(os.path.splitext(xmlFile)[0]) + '.xml')
            if self.get_flag_arguments()["new"]: self.create_xml_copy(xmlFile)
            self.check_project_keywords(xmlFile)
            self.check_datacenter_keywords(xmlFile)
            self.check_platform_keywords(xmlFile)
            self.check_instrument_keywords(xmlFile)
            self.check_theme_keywords(xmlFile)
            self.check_place_keywords(xmlFile)
            if self.get_flag_arguments()["new"]: self.process_xml_copy(xmlFile)
            self.cleanup()
        except Exception as e:
            print(xmlFile + " failed assessment")
            print(e)
            if os.path.exists("./" + basename(os.path.splitext(xmlFile)[0]) + '_new.xml'):
                os.remove("./" + basename(os.path.splitext(xmlFile)[0]) + '_new.xml')
        print(" ")

    def cleanup(self):
        if os.path.isdir("./improved_xml/"):
            # delete if directory empty
            if not os.listdir("./improved_xml/"):
                os.rmdir("./improved_xml/") 

    def find_xml_files(self, source_dir):
        self.xmlFiles = []
        for root, dirnames, filenames in os.walk(source_dir, followlinks=True):
            for filename in fnmatch.filter(filenames, '*.xml'):
                self.xmlFiles.append(os.path.join(root, filename))
        print("%d files found in source directory" % len(self.xmlFiles))
        return self.xmlFiles

    def create_results_csv(self):
        with open('invalid_GCMD_keywords_results.csv', 'wb') as out:
            writer = csv.writer(out)
            writer.writerow(["Invalid Keyword", "Type", "Filename", "Suggestion 1", "Suggestion 2", "Suggestion 3"])

    def delete_csv_if_no_invalid_keywords_found(self):
        with open('invalid_GCMD_keywords_results.csv', 'rb') as out:
            reader = csv.reader(out)
            row_count = sum(1 for row in reader)
            if row_count == 1:
                print("no invalid GCMD keywords found")
                os.remove('invalid_GCMD_keywords_results.csv')
    
    def process_xml_copy(self, file):
        if filecmp.cmp(file, "./" + basename(os.path.splitext(file)[0]) + '_new.xml') == True:
            os.remove("./" + basename(os.path.splitext(file)[0]) + '_new.xml')
        else:
            if not os.path.exists("./improved_xml"):
                os.makedirs("./improved_xml")
            shutil.move("./" + basename(os.path.splitext(file)[0]) + '_new.xml', "./improved_xml/" + basename(os.path.splitext(file)[0]) + '.xml')

    def create_xml_copy(self, file):
        copyfile(file, "./" + basename(os.path.splitext(file)[0]) + '_new.xml')

    def replace_wrong_keyword_in_xml_copy(self, suggestions, file, keyword):
        bestSimilarKeyword = self.find_best_similar_keyword(suggestions, keyword)
        if bestSimilarKeyword == "":
            pass
        else:
            with open("./" + basename(os.path.splitext(file)[0]) + '_new.xml', 'r+') as f:
                content = f.read()
                f.seek(0)
                f.truncate()
                # replace "&" and ">" in keywords from CSV to be inserted into XML
                keyword = keyword.replace("&", "&amp;")
                f.write(content.replace("<gco:CharacterString>" + keyword.replace(">", "&gt;") + "</gco:CharacterString>", "<gco:CharacterString>" + bestSimilarKeyword + "</gco:CharacterString>"))


    def find_best_similar_keyword(self, suggestions, keyword):
        while "N/A" in suggestions: suggestions.remove("N/A")
        if not suggestions:
            return ""
        else:
            matches = [s for s in suggestions if keyword.upper() in s.upper()]
            if not matches:
                return ""
            else:
                # replace "&" and ">" in keywords from CSV to be inserted into XML
                matches = min(matches, key=len).replace("&", "&amp;")
                return matches.replace(">", "&gt;")

    def get_similar_keywords(self, modelKeywordsList, keyword):
        # get last segment after " > " if exists
        keyword = keyword.split(' > ')[-1]
        similarKeywords = [s for s in modelKeywordsList if keyword.upper() in s.upper()]
        # make set to remove duplicates and back to list to be able to access elements 
        list(set(similarKeywords))
        similarKeywordsList = []
        for i in range(0,100):
            try:
                similarKeywordsList.append(similarKeywords[i])
            except IndexError:
                continue
        # if no matches with the above method try first half of keyword string
        if (len(set(similarKeywordsList)) <= 1):
            similarKeywordsList = []
            keywordSubstring = keyword[0:len(keyword)/2]
            similarKeywords = [s for s in modelKeywordsList if keywordSubstring.upper() in s.upper()]
            for i in range(0,100):
                try:
                    similarKeywordsList.append(similarKeywords[i])
                except IndexError:
                    continue
        # if no matches with the above method try first third of keyword string
        if (len(set(similarKeywordsList)) <= 1):
            similarKeywordsList = []
            keywordSubstring = keyword[0:len(keyword)/3]
            similarKeywords = [s for s in modelKeywordsList if keywordSubstring.upper() in s.upper()]
            for i in range(0,100):
                try:
                    similarKeywordsList.append(similarKeywords[i])
                except IndexError:
                    continue
        # if no matches with the above method try latter fractions of keyword string
        if (len(set(similarKeywordsList)) <= 1):
            similarKeywordsList = []
            keywordSubstring = keyword[len(keyword)*13/15:]
            similarKeywords = [s for s in modelKeywordsList if keywordSubstring.upper() in s.upper()]
            for i in range(0,100):
                try:
                    similarKeywordsList.append(similarKeywords[i])
                except IndexError:
                    continue

        #print(similarKeywordsList)
        return similarKeywordsList 

    def apply_keyword_algorithm(self, similarKeywords, hierarchyLevel, keyword, modelKeywordsList, GCMDKeywordType, file):
        suggestions = []
        for i in similarKeywords:
            i = ' > '.join(i.split(' > ')[hierarchyLevel:])
            if i[-3:] == ' > ':
                i = i[:-3]
            suggestions.append(i)
        suggestions = [x for x in suggestions if x]
        suggestions.sort(key = lambda s: len(s))
        # get last segment after " > " if exists
        keywordLastSegment = keyword.split(' > ')[-1]
        matching = [s for s in modelKeywordsList if keywordLastSegment.upper() in s]
        matching.sort(key = lambda s: len(s))

        if (len(matching) < 1):
            try:
                keywordSecondToLastSegment = keyword.split(' > ')[-2]
                matching = [s for s in modelKeywordsList if keywordSecondToLastSegment.upper() in s]
                matching.sort(key = lambda s: len(s))
            except IndexError:
                pass

        #print(matching)
        suggestions = matching + suggestions
        suggestions = [x.title() for x in suggestions]
        suggestions.extend(('N/A', 'N/A', 'N/A'))

        with open('invalid_GCMD_keywords_results.csv', 'a') as f:
            writer = csv.writer(f)
            writer.writerow([keyword, GCMDKeywordType, basename(os.path.splitext(file)[0]) + '.xml', suggestions[0], suggestions[1], suggestions[2]])
        if self.get_flag_arguments()["new"]: self.replace_wrong_keyword_in_xml_copy(suggestions, file, keyword)

    def run_checker(self):
        self.create_results_csv()
        if os.path.isdir(self.get_flag_arguments()["target"]):
        # batch processing
            xmlFiles = self.find_xml_files(self.get_flag_arguments()["target"])
            for xmlFile in xmlFiles:
                self.process(xmlFile)
        else:
        # single file processing
            xmlFile = self.get_flag_arguments()["target"]
            self.process(xmlFile)
        self.delete_csv_if_no_invalid_keywords_found()


    # THEME KEYWORDS
    def get_theme_keywords(self, file):
        themeKeywordsList = []
        xmlRoot = et.fromstring(open(file).read())
        themeKeywords = xmlRoot.xpath(
            "//gmd:MD_DataIdentification/gmd:descriptiveKeywords/gmd:MD_Keywords[gmd:type/gmd:MD_KeywordTypeCode/@codeListValue='theme']/gmd:keyword[../gmd:thesaurusName/gmd:CI_Citation/gmd:title/*[contains(text(), 'GCMD')]]/*",
                namespaces=xmlRoot.nsmap)
        for i in range(len(themeKeywords)):
            themeKeywordsList.append(themeKeywords[i].text.encode('utf-8'))
        #print(themeKeywordsList)
        return themeKeywordsList

    def get_theme_keywords_thesauri(self, file):
        themeKeywordsThesauriList = []
        xmlRoot = et.fromstring(open(file).read())
        themeKeywordsThesauri = xmlRoot.xpath(
            "//gmd:MD_DataIdentification/gmd:descriptiveKeywords/gmd:MD_Keywords[gmd:type/gmd:MD_KeywordTypeCode/@codeListValue='theme']/gmd:thesaurusName/gmd:CI_Citation/gmd:title/*[contains(text(), 'GCMD')]",
                namespaces=xmlRoot.nsmap)
        for i in range(len(themeKeywordsThesauri)):
            themeKeywordsThesauriList.append(themeKeywordsThesauri[i].text.encode('utf-8'))
        #print(themeKeywordsThesauriList)
        return themeKeywordsThesauriList

    def get_model_theme_keywords_list(self):
        modelThemeKeywordsList = []
        data = csv.reader(urllib2.urlopen("https://gcmdservices.gsfc.nasa.gov/static/kms/sciencekeywords/sciencekeywords.csv"))
        for row in data:
            keyword = row[0].strip()
            for i in range(1,7):
                try:
                    if row[i] != "":
                        keyword = keyword + " > " + row[i].strip()
                except IndexError:
                    continue
            modelThemeKeywordsList.append(keyword.upper())    

        #print(modelThemeKeywordsList)
        return modelThemeKeywordsList

    def check_theme_keywords(self, file):
        modelKeywordsList = self.get_model_theme_keywords_list()
        keywordsList = self.get_theme_keywords(file)
        # check if file theme keywords are in modelThemeKeywordsList ignoring case
        for keyword in keywordsList:
            if keyword.upper() not in modelKeywordsList:
                print("invalid theme keyword: " + keyword)
                # find similar keywords
                similarKeywords = self.get_similar_keywords(modelKeywordsList, keyword)
                
                # apply keyword algorithm def
                self.apply_keyword_algorithm(similarKeywords, 0, keyword, modelKeywordsList, "theme", file)
    # END THEME KEYWORDS

    # DATA CENTER KEYWORDS
    def get_datacenter_keywords(self, file):
        datacenterKeywordsList = []
        xmlRoot = et.fromstring(open(file).read())
        datacenterKeywords = xmlRoot.xpath(
            "//gmd:MD_DataIdentification/gmd:descriptiveKeywords/gmd:MD_Keywords[gmd:type/gmd:MD_KeywordTypeCode/@codeListValue='dataCenter']/gmd:keyword[../gmd:thesaurusName/gmd:CI_Citation/gmd:title/*[contains(text(), 'GCMD')]]/*",
                namespaces=xmlRoot.nsmap)
        for i in range(len(datacenterKeywords)):
            datacenterKeywordsList.append(datacenterKeywords[i].text.encode('utf-8'))
        #print(datacenterKeywordsList)
        return datacenterKeywordsList

    def get_datacenter_keywords_thesauri(self, file):
        datacenterKeywordsThesauriList = []
        xmlRoot = et.fromstring(open(file).read())
        datacenterKeywordsThesauri = xmlRoot.xpath(
            "//gmd:MD_DataIdentification/gmd:descriptiveKeywords/gmd:MD_Keywords[gmd:type/gmd:MD_KeywordTypeCode/@codeListValue='dataCenter']/gmd:thesaurusName/gmd:CI_Citation/gmd:title/*[contains(text(), 'GCMD')]",
                namespaces=xmlRoot.nsmap)
        for i in range(len(datacenterKeywordsThesauri)):
            datacenterKeywordsThesauriList.append(datacenterKeywordsThesauri[i].text.encode('utf-8'))
        #print(datacenterKeywordsThesauriList)
        return datacenterKeywordsThesauriList

    def get_model_datacenter_keywords_list(self):
        modelDatacenterKeywordsList = []
        data = csv.reader(urllib2.urlopen("https://gcmdservices.gsfc.nasa.gov/static/kms/providers/providers.csv"))
        for row in data:
            try:
                keyword = row[4].strip()
            except IndexError:
                continue
            for i in range(5,6):
                try:
                    if row[i] != "":
                        keyword = keyword + " > " + row[i].strip()
                except IndexError:
                    continue
            modelDatacenterKeywordsList.append(keyword.upper())    

        #print(modelDatacenterKeywordsList)
        return modelDatacenterKeywordsList

    def check_datacenter_keywords(self, file):
            modelKeywordsList = self.get_model_datacenter_keywords_list()
            keywordsList = self.get_datacenter_keywords(file)
            # check if file datacenter keywords are in modelDatacenterKeywordsList ignoring case
            for keyword in keywordsList:
                if keyword.upper() not in modelKeywordsList:
                    print("invalid datacenter keyword: " + keyword)
                    # find similar keywords
                    similarKeywords = self.get_similar_keywords(modelKeywordsList, keyword)
                    
                    # apply keyword algorithm def
                    self.apply_keyword_algorithm(similarKeywords, 0, keyword, modelKeywordsList, "datacenter", file)
    # END DATACENTER KEYWORDS

    # PLACE KEYWORDS
    def get_place_keywords(self, file):
        placeKeywordsList = []
        xmlRoot = et.fromstring(open(file).read())
        placeKeywords = xmlRoot.xpath(
            "//gmd:MD_DataIdentification/gmd:descriptiveKeywords/gmd:MD_Keywords[gmd:type/gmd:MD_KeywordTypeCode/@codeListValue='place']/gmd:keyword[../gmd:thesaurusName/gmd:CI_Citation/gmd:title/*[contains(text(), 'GCMD')]]/*",
                namespaces=xmlRoot.nsmap)
        for i in range(len(placeKeywords)):
            placeKeywordsList.append(placeKeywords[i].text.encode('utf-8'))
        #print(placeKeywordsList)
        return placeKeywordsList

    def get_place_keywords_thesauri(self, file):
        placeKeywordsThesauriList = []
        xmlRoot = et.fromstring(open(file).read())
        placeKeywordsThesauri = xmlRoot.xpath(
            "//gmd:MD_DataIdentification/gmd:descriptiveKeywords/gmd:MD_Keywords[gmd:type/gmd:MD_KeywordTypeCode/@codeListValue='place']/gmd:thesaurusName/gmd:CI_Citation/gmd:title/*[contains(text(), 'GCMD')]",
                namespaces=xmlRoot.nsmap)
        for i in range(len(placeKeywordsThesauri)):
            placeKeywordsThesauriList.append(placeKeywordsThesauri[i].text.encode('utf-8'))
        #print(placeKeywordsThesauriList)
        return placeKeywordsThesauriList

    def get_model_place_keywords_list(self):
        modelPlaceKeywordsList = []
        data = csv.reader(urllib2.urlopen("https://gcmdservices.gsfc.nasa.gov/static/kms/locations/locations.csv"))
        for row in data:
            keyword = row[0].strip()
            for i in range(1,5):
                try:
                    if row[i] != "":
                        keyword = keyword + " > " + row[i].strip()
                except IndexError:
                    continue
            modelPlaceKeywordsList.append(keyword.upper())    

        #print(modelPlaceKeywordsList)
        return modelPlaceKeywordsList

    def check_place_keywords(self, file):
        modelKeywordsList = self.get_model_place_keywords_list()
        keywordsList = self.get_place_keywords(file)
        # check if file place keywords are in modelPlaceKeywordsList ignoring case
        for keyword in keywordsList:
            if keyword.upper() not in modelKeywordsList:
                print("invalid place keyword: " + keyword)
                # find similar keywords
                similarKeywords = self.get_similar_keywords(modelKeywordsList, keyword)
                
                # apply keyword algorithm def
                self.apply_keyword_algorithm(similarKeywords, 0, keyword, modelKeywordsList, "place", file)
    # END PLACE KEYWORDS
    
    # PLATFORM KEYWORDS
    def get_platform_keywords(self, file):
        platformKeywordsList = []
        xmlRoot = et.fromstring(open(file).read())
        platformKeywords = xmlRoot.xpath(
            "//gmd:MD_DataIdentification/gmd:descriptiveKeywords/gmd:MD_Keywords[gmd:type/gmd:MD_KeywordTypeCode/@codeListValue='platform']/gmd:keyword[../gmd:thesaurusName/gmd:CI_Citation/gmd:title/*[contains(text(), 'GCMD')]]/*",
                namespaces=xmlRoot.nsmap)
        for i in range(len(platformKeywords)):
            platformKeywordsList.append(platformKeywords[i].text.encode('utf-8'))
        #print(platformKeywordsList)
        return platformKeywordsList

    def get_platform_keywords_thesauri(self, file):
        platformKeywordsThesauriList = []
        xmlRoot = et.fromstring(open(file).read())
        platformKeywordsThesauri = xmlRoot.xpath(
            "//gmd:MD_DataIdentification/gmd:descriptiveKeywords/gmd:MD_Keywords[gmd:type/gmd:MD_KeywordTypeCode/@codeListValue='platform']/gmd:thesaurusName/gmd:CI_Citation/gmd:title/*[contains(text(), 'GCMD')]",
                namespaces=xmlRoot.nsmap)
        for i in range(len(platformKeywordsThesauri)):
            platformKeywordsThesauriList.append(platformKeywordsThesauri[i].text.encode('utf-8'))
        #print(platformKeywordsThesauriList)
        return platformKeywordsThesauriList

    def get_model_platform_keywords_list_short_hierarchy(self):
        modelPlatformKeywordsList = []
        data = csv.reader(urllib2.urlopen("https://gcmdservices.gsfc.nasa.gov/static/kms/platforms/platforms.csv"))
        for row in data:
            try:
                keyword = row[2].strip()
            except IndexError:
                continue
            for i in range(3,4):
                try:
                    if row[i] != "":
                        keyword = keyword + " > " + row[i].strip()
                except IndexError:
                    continue
            modelPlatformKeywordsList.append(keyword.upper())    

        #print(modelPlatformKeywordsList)
        return modelPlatformKeywordsList

    def get_model_platform_keywords_list_long_hierarchy(self):
        modelPlatformKeywordsList = []
        data = csv.reader(urllib2.urlopen("https://gcmdservices.gsfc.nasa.gov/static/kms/platforms/platforms.csv"))
        for row in data:
            try:
                keyword = row[0].strip()
            except IndexError:
                continue
            for i in range(1,4):
                try:
                    if row[i] != "":
                        keyword = keyword + " > " + row[i].strip()
                except IndexError:
                    continue
            modelPlatformKeywordsList.append(keyword.upper())    

        #print(modelPlatformKeywordsList)
        return modelPlatformKeywordsList

    def check_platform_keywords(self, file):
        modelPlatformKeywordsListShortHierarchy = self.get_model_platform_keywords_list_short_hierarchy()
        modelPlatformKeywordsListLongHierarchy = self.get_model_platform_keywords_list_long_hierarchy()
        platformKeywordsList = self.get_platform_keywords(file)
        # check if file platform keywords are in modelPlatformKeywordsListShortHierarchy ignoring case
        for keyword in platformKeywordsList:
            if keyword.upper() not in modelPlatformKeywordsListShortHierarchy:
                print("invalid platform keyword: " + keyword)
                # find similar keywords
                similarKeywords = self.get_similar_keywords(modelPlatformKeywordsListLongHierarchy, keyword)

                # apply keyword algorithm def
                self.apply_keyword_algorithm(similarKeywords, 2, keyword, modelPlatformKeywordsListShortHierarchy, "platform", file)
    # END PLATFORM KEYWORDS
    
    # INSTRUMENT KEYWORDS
    def get_instrument_keywords(self, file):
        instrumentKeywordsList = []
        xmlRoot = et.fromstring(open(file).read())
        instrumentKeywords = xmlRoot.xpath(
            "//gmd:MD_DataIdentification/gmd:descriptiveKeywords/gmd:MD_Keywords[gmd:type/gmd:MD_KeywordTypeCode/@codeListValue='instrument']/gmd:keyword[../gmd:thesaurusName/gmd:CI_Citation/gmd:title/*[contains(text(), 'GCMD')]]/*",
                namespaces=xmlRoot.nsmap)
        for i in range(len(instrumentKeywords)):
            instrumentKeywordsList.append(instrumentKeywords[i].text.encode('utf-8'))
        #print(instrumentKeywordsList)
        return instrumentKeywordsList

    def get_instrument_keywords_thesauri(self, file):
        instrumentKeywordsThesauriList = []
        xmlRoot = et.fromstring(open(file).read())
        instrumentKeywordsThesauri = xmlRoot.xpath(
            "//gmd:MD_DataIdentification/gmd:descriptiveKeywords/gmd:MD_Keywords[gmd:type/gmd:MD_KeywordTypeCode/@codeListValue='instrument']/gmd:thesaurusName/gmd:CI_Citation/gmd:title/*[contains(text(), 'GCMD')]",
                namespaces=xmlRoot.nsmap)
        for i in range(len(instrumentKeywordsThesauri)):
            instrumentKeywordsThesauriList.append(instrumentKeywordsThesauri[i].text.encode('utf-8'))
        #print(instrumentKeywordsThesauriList)
        return instrumentKeywordsThesauriList

    def get_model_instrument_keywords_list_short_hierarchy(self):
        modelInstrumentKeywordsList = []
        data = csv.reader(urllib2.urlopen("https://gcmdservices.gsfc.nasa.gov/static/kms/instruments/instruments.csv"))
        for row in data:
            try:
                keyword = row[4].strip()
            except IndexError:
                continue
            for i in range(5,6):
                try:
                    if row[i] != "":
                        keyword = keyword + " > " + row[i].strip()
                except IndexError:
                    continue
            modelInstrumentKeywordsList.append(keyword.upper())    

        #print(modelInstrumentKeywordsList)
        return modelInstrumentKeywordsList

    def get_model_instrument_keywords_list_long_hierarchy(self):
        modelInstrumentKeywordsList = []
        data = csv.reader(urllib2.urlopen("https://gcmdservices.gsfc.nasa.gov/static/kms/instruments/instruments.csv"))
        for row in data:
            try:
                keyword = row[0].strip()
            except IndexError:
                continue
            for i in range(1,6):
                try:
                    if row[i] != "":
                        keyword = keyword + " > " + row[i].strip()
                except IndexError:
                    continue
            modelInstrumentKeywordsList.append(keyword.upper())

        #print(modelInstrumentKeywordsList)
        return modelInstrumentKeywordsList

    def check_instrument_keywords(self, file):
        modelInstrumentKeywordsListShortHierarchy = self.get_model_instrument_keywords_list_short_hierarchy()
        modelInstrumentKeywordsListLongHierarchy = self.get_model_instrument_keywords_list_long_hierarchy()
        instrumentKeywordsList = self.get_instrument_keywords(file)
        # check if file instrument keywords are in modelInstrumentKeywordsListShortHierarchy ignoring case
        for keyword in instrumentKeywordsList:
            if keyword.upper() not in modelInstrumentKeywordsListShortHierarchy:
                print("invalid instrument keyword: " + keyword)
                # find similar keywords
                similarKeywords = self.get_similar_keywords(modelInstrumentKeywordsListLongHierarchy, keyword)

                # apply keyword algorithm def
                self.apply_keyword_algorithm(similarKeywords, 2, keyword, modelInstrumentKeywordsListShortHierarchy, "instrument", file)
    # END INSTRUMENT KEYWORDS
    
    # PROJECT KEYWORDS
    def get_project_keywords(self, file):
        projectKeywordsList = []
        xmlRoot = et.fromstring(open(file).read())
        projectKeywords = xmlRoot.xpath(
            "//gmd:MD_DataIdentification/gmd:descriptiveKeywords/gmd:MD_Keywords[gmd:type/gmd:MD_KeywordTypeCode/@codeListValue='project']/gmd:keyword[../gmd:thesaurusName/gmd:CI_Citation/gmd:title/*[contains(text(), 'GCMD')]]/*",
                namespaces=xmlRoot.nsmap)
        for i in range(len(projectKeywords)):
            projectKeywordsList.append(projectKeywords[i].text.encode('utf-8'))
        #print(projectKeywordsList)
        return projectKeywordsList

    def get_project_keywords_thesauri(self, file):
        projectKeywordsThesauriList = []
        xmlRoot = et.fromstring(open(file).read())
        projectKeywordsThesauri = xmlRoot.xpath(
            "//gmd:MD_DataIdentification/gmd:descriptiveKeywords/gmd:MD_Keywords[gmd:type/gmd:MD_KeywordTypeCode/@codeListValue='project']/gmd:thesaurusName/gmd:CI_Citation/gmd:title/*[contains(text(), 'GCMD')]",
                namespaces=xmlRoot.nsmap)
        for i in range(len(projectKeywordsThesauri)):
            projectKeywordsThesauriList.append(projectKeywordsThesauri[i].text.encode('utf-8'))
        #print(projectKeywordsThesauriList)
        return projectKeywordsThesauriList

    def get_model_project_keywords_list(self):
        modelProjectKeywordsList = []
        data = csv.reader(urllib2.urlopen("https://gcmdservices.gsfc.nasa.gov/static/kms/projects/projects.csv"))
        for row in data:
            try:
                keyword = row[1].strip()
            except IndexError:
                continue
            for i in range(2,3):
                try:
                    if row[i] != "":
                        keyword = keyword + " > " + row[i].strip()
                except IndexError:
                    continue
            modelProjectKeywordsList.append(keyword.upper())    

        #print(modelProjectKeywordsList)
        return modelProjectKeywordsList

    def check_project_keywords(self, file):
        modelKeywordsList = self.get_model_project_keywords_list()
        keywordsList = self.get_project_keywords(file)
        # check if file project keywords are in modelProjectKeywordsList ignoring case
        for keyword in keywordsList:
            if keyword.upper() not in modelKeywordsList:
                print("invalid project keyword: " + keyword)
                # find similar keywords
                similarKeywords = self.get_similar_keywords(modelKeywordsList, keyword)
                
                # apply keyword algorithm def
                self.apply_keyword_algorithm(similarKeywords, 0, keyword, modelKeywordsList, "project", file)
    # END PROJECT KEYWORDS

# __main__
if __name__ == '__main__':
    """
    run python -u gcmd.py | tee output.log to see CLI output AND get log file 
    """
    start = time.time()

    gcmd = GCMD()
    gcmd.run_checker()

    #gcmd.create_xml_copy("./collection_test_files/GHRSST-ABOM-L4HRfnd-AUS-RAMSSA_09km.xml")

    print('The program took ', time.time() - start, 'seconds to complete.')

# End __main__
