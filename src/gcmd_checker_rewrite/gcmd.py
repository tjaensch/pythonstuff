import fnmatch
import glob
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

    def get_theme_keywords(self, file):
        themeKeywordsList = []
        xmlRoot = et.fromstring(open(file).read())
        themeKeywords = xmlRoot.xpath(
            "//gmd:MD_DataIdentification/gmd:descriptiveKeywords/gmd:MD_Keywords[gmd:type/gmd:MD_KeywordTypeCode/@codeListValue='theme']/gmd:keyword/*",
                namespaces=xmlRoot.nsmap)
        for i in range(len(themeKeywords)):
            themeKeywordsList.append(themeKeywords[i].text)
        return themeKeywordsList

# __main__
if __name__ == '__main__':
    start = time.time()

    gcmd = GCMD()
    xmlFiles = gcmd.find_xml_files()

    gcmd.get_theme_keywords(xmlFiles[0])

    print('The program took ', time.time() - start, 'seconds to complete.')

# End __main__
