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
        	    self.xmlFiles.append(file)
            return self.xmlFiles

class TestOER(unittest.TestCase):
    """docstring for TestOER"""
    def setUp(self):
    	oer = OER()
        self.xmlFiles = oer.findXmlFiles()

    def test_findXmlFiles(self):
        self.assertEqual(len(self.xmlFiles), 41850)
        self.assertTrue(self.xmlFiles)

if __name__ == '__main__':
	unittest.main()
	oer = OER()
	oer.findXmlFiles()
	print oer.xmlFiles