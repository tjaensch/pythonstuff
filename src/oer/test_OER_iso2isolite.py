import os
import shutil
import unittest
from OER_iso2isolite import OER

# Tests
class TestOER(unittest.TestCase):
    """docstring for TestOER"""
    def setUp(self):
        testfile = "EX1504L2_VID_20150817T214435Z_ROVHD_SPO_DEAD.mov.xml"
        oer = OER()
        self.xmlFiles = oer.find_xml_files()

        # Create output dir for testing
        if not os.path.exists("/nodc/users/tjaensch/python.git/src/oer/oer_iso/"):
            os.makedirs("/nodc/users/tjaensch/python.git/src/oer/oer_iso/")

        # test run defs with one file
        oer.xsltproc_to_iso(testfile)

    def tearDown(self):
        shutil.rmtree("/nodc/users/tjaensch/python.git/src/oer/oer_iso/")

    def test_find_xml_files(self):
        self.assertEqual(len(self.xmlFiles), 41850)
        self.assertTrue(self.xmlFiles)

    def test_xsltproc_to_iso(self):
        file = open("/nodc/users/tjaensch/python.git/src/oer/oer_iso/EX1504L2_VID_20150817T214435Z_ROVHD_SPO_DEAD.mov.xml", "r")
        data = file.read()
        self.assertTrue("OER.EX1504L2_DIVE16_20150817T214435Z_ROVHD_SPO_DEAD" in data)

# __main__
if __name__ == '__main__':
    unittest.main()
# End __main__