import unittest
from OER_iso2isolite import OER

# Tests
class TestOER(unittest.TestCase):
    """docstring for TestOER"""
    def setUp(self):
        oer = OER()
        self.xmlFiles = oer.find_xml_files()

    def test_find_xml_files(self):
        self.assertEqual(len(self.xmlFiles), 41850)
        self.assertTrue(self.xmlFiles)

# __main__
if __name__ == '__main__':
    unittest.main()
# End __main__