import lxml.etree as ET
import fnmatch
import glob
import time
import os
import random
import re
import subprocess
import urllib
from multiprocessing import Pool
from os.path import basename


def create_output_dirs():
    if not os.path.exists("./ncml/"):
        os.makedirs("./ncml/")
        if not os.path.exists("./iso_xml/"):
            os.makedirs("./iso_xml/")
        if not os.path.exists("./final_xml/"):
            os.makedirs("./final_xml/")
        if not os.path.exists("./netcdf3/"):
            os.makedirs("./netcdf3/")


class CMAN:
    """docstring for cman"""

    def __init__(self):
    	pass

    def get_nc_file_urls(self):
        self.ncFileUrls = []
        with open("files.txt") as f:
            for line in f:
                self.ncFileUrls.append("https://data.nodc.noaa.gov/ndbc/cmanwx/" + line.strip())
        return self.ncFileUrls

    def download_nc_file_from_url(self, ncFileUrl):
    	ncFile = urllib.URLopener()
        ncFile.retrieve(ncFileUrl, os.path.basename(ncFileUrl))

    def delete_nc_file_after_processing(self, ncFileUrl):
    	os.remove("./" + os.path.basename(ncFileUrl))

    def ncdump(self, ncFile):
        # Convert netcdf4 to netcdf3 for ncdump -x to work
        subprocess.call(["ncks", "-3", ncFile, "./netcdf3/" +
                         self.get_file_name(ncFile) + ".nc"])
        # actual ncdump
        f = open("./ncml/" + self.get_file_name(ncFile) + ".ncml", "w")
        subprocess.call(["ncdump", "-x", "./netcdf3/" +
                         self.get_file_name(ncFile) + ".nc"], stdout=f)
        f.close()
        os.remove("./netcdf3/" + self.get_file_name(ncFile) + ".nc")

    def get_file_name(self, ncFile):
        #print(basename(ncFile)[:-3])
        return(basename(ncFile)[:-3])

    def run_combined_defs(self, ncFileUrl):
    	print(basename(ncFileUrl))
    	self.download_nc_file_from_url(ncFileUrl)
        self.ncdump("./" + os.path.basename(ncFileUrl))
        #self.add_to_ncml(ncFile)
        #self.xsltproc_to_iso(ncFile)
        #self.add_collection_metadata(ncFile)
        self.delete_nc_file_after_processing(ncFileUrl)

    def go(self):
        p = Pool(5)
        p.map(self, self.get_nc_file_urls()[:5])

    def __call__(self, ncFile):
        return self.run_combined_defs(ncFile)


# __main__
if __name__ == '__main__':
    start = time.time()

    create_output_dirs()

    cman = CMAN()
    
    cman.go()

    #ncFileUrls = cman.get_nc_file_urls()
    #cman.download_nc_file_from_url(ncFileUrls[0])
    #cman.ncdump("./" + os.path.basename(ncFileUrls[0]))
    

    print 'The program took ', time.time() - start, 'seconds to complete.'

# End __main__
