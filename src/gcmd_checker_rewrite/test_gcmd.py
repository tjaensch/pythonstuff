import os
import shutil
import unittest
from gcmd import GCMD

# Tests


class Testgcmd(unittest.TestCase):
    """docstring for Testgcmd"""

    def setUp(self):
        gcmd = GCMD()
        #testfile = "/nodc/web/data.nodc/htdocs/ndbc/cmanwx/2016/05/NDBC_44020_201605_D6_v00.nc"
        self.xmlFiles = gcmd.find_xml_files()

    def test_find_xml_files(self):
        self.assertTrue(len(self.xmlFiles) > 0)
        self.assertTrue(self.xmlFiles)

# __main__
if __name__ == '__main__':
    unittest.main()
# End __main__
