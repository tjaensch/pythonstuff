import lxml.etree as ET
import glob
import os
import unittest

class OER:
	"""docstring for OER"""
	def __init__(self):
		self.xmlFiles = []

        def findXmlFiles(self):
            os.chdir("/nodc/projects/satdata/OER/Metadata/waf/")
            for file in glob.glob("*.xml"):
        	    self.xmlFiles.append("/nodc/projects/satdata/OER/Metadata/waf/" + file)
            return self.xmlFiles

        def xsltprocToISO(self, xmlFile):
            xslFile = "/nodc/users/tjaensch/onestop.git/xsl/oer/XSL/OER_ISO2ISOLite_conversion.xsl"
            parsedXmlFile = ET.parse(xmlFile)
            xslt = ET.parse(xslFile)
            transform = ET.XSLT(xslt)
            newXmlFile = transform(parsedXmlFile)
            with open("/nodc/users/tjaensch/python/src/oer/blah.xml", "w") as f:
                f.write(ET.tostring(newXmlFile, pretty_print=True))
            print(ET.tostring(newXmlFile, pretty_print=True))


# __main__
if __name__ == '__main__':
	# unittest.main()
    oer = OER()
    oer.findXmlFiles()
    #print oer.xmlFiles
    oer.xsltprocToISO("/nodc/projects/satdata/OER/Metadata/waf/EX1004L2_VID_20100629T021804Z_CPHD_FIRST_BOTTOM.mov.xml")
# End __main__

# Tests
class TestOER(unittest.TestCase):
    """docstring for TestOER"""
    def setUp(self):
        oer = OER()
        self.xmlFiles = oer.findXmlFiles()

    def test_findXmlFiles(self):
        self.assertEqual(len(self.xmlFiles), 41850)
        self.assertTrue(self.xmlFiles)