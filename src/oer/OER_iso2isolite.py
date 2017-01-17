import lxml.etree as ET
import glob
import os
import unittest

class OER:
	"""docstring for OER"""
	def __init__(self):
		self.xmlFiles = []

        def find_xml_files(self):
            os.chdir("/nodc/projects/satdata/OER/Metadata/waf/")
            for file in glob.glob("*.xml"):
        	    self.xmlFiles.append(file)
            return self.xmlFiles

        def xsltproc_to_iSO(self, xmlFile):
            xslFile = "/nodc/users/tjaensch/onestop.git/xsl/oer/XSL/OER_ISO2ISOLite_conversion.xsl"
            parsedXmlFile = ET.parse(xmlFile)
            xslt = ET.parse(xslFile)
            transform = ET.XSLT(xslt)
            newXmlFile = transform(parsedXmlFile)
            with open("/nodc/users/tjaensch/python/src/oer/oer_iso/" + xmlFile, "w") as f:
                f.write(ET.tostring(newXmlFile, pretty_print=True))
            print(ET.tostring(newXmlFile, pretty_print=True))

        def create_output_dir(self):
            os.makedirs("/nodc/users/tjaensch/python/src/oer/oer_iso/")


# __main__
if __name__ == '__main__':
	# unittest.main()
    oer = OER()
    oer.find_xml_files()
    print oer.xmlFiles
    oer.create_output_dir()
    
    for xmlFile in oer.xmlFiles:
        oer.xsltproc_to_iSO(xmlFile)
# End __main__

# Tests
class TestOER(unittest.TestCase):
    """docstring for TestOER"""
    def setUp(self):
        oer = OER()
        self.xmlFiles = oer.findXmlFiles()

    def test_find_xml_files(self):
        self.assertEqual(len(self.xmlFiles), 41850)
        self.assertTrue(self.xmlFiles)