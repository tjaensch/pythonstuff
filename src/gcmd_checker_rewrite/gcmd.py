import fnmatch
import glob
import time
import os
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


# __main__
if __name__ == '__main__':
    start = time.time()

    gcmd = GCMD()
    gcmd.find_xml_files()

    print 'The program took ', time.time() - start, 'seconds to complete.'

# End __main__
