import lxml.etree as ET
import fnmatch
import glob
import time
import os
import random
import re
import shutil
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

def cleanup():
    os.remove("./NDBC-CMANWx.xml")
    shutil.rmtree("./ncml/")
    shutil.rmtree("./iso_xml/")
    shutil.rmtree("./netcdf3/")


class CMAN:
    """docstring for cman"""

    def __init__(self):
        pass

    def download_collection_level_file(self):
        isocofile = urllib.URLopener()
        isocofile.retrieve("https://data.nodc.noaa.gov/nodc/archive/metadata/approved/iso/NDBC-CMANWx.xml", os.path.basename("https://data.nodc.noaa.gov/nodc/archive/metadata/approved/iso/NDBC-CMANWx.xml"))

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

    def ncdump(self, ncFileUrl):
        # Convert netcdf4 to netcdf3 for ncdump -x to work
        subprocess.call(["ncks", "-3", "./" + os.path.basename(ncFileUrl), "./netcdf3/" +
                         self.get_file_name("./" + os.path.basename(ncFileUrl)) + ".nc"])
        # actual ncdump
        f = open("./ncml/" + self.get_file_name("./" + os.path.basename(ncFileUrl)) + ".ncml", "w")
        subprocess.call(["ncdump", "-x", "./netcdf3/" +
                         self.get_file_name("./" + os.path.basename(ncFileUrl)) + ".nc"], stdout=f)
        f.close()
        os.remove("./netcdf3/" + self.get_file_name("./" + os.path.basename(ncFileUrl)) + ".nc")

    def get_file_name(self, ncFileUrl):
        #print(basename("./" + os.path.basename(ncFileUrl))[:-3])
        return(basename("./" + os.path.basename(ncFileUrl))[:-3])

    def get_english_title(self, ncFileUrl):
        deployment_number = re.findall('\d+', self.get_file_name("./" + os.path.basename(ncFileUrl))[19:])
        return "NDBC-CMANWx" + self.get_file_name("./" + os.path.basename(ncFileUrl))[4:] + " - C-MAN/Wx buoy " + self.get_file_name("./" + os.path.basename(ncFileUrl))[5:10] + " for " + self.get_file_name("./" + os.path.basename(ncFileUrl))[11:17] + ", deployment " + str(deployment_number[0])

    def get_file_path(self, ncFileUrl):
        abspath = os.path.dirname(ncFileUrl)[27:] + "/"
        print(abspath)
        return(abspath)

    def get_file_size(self, ncFileUrl):
        print(os.path.getsize("./" + os.path.basename(ncFileUrl)) / 1024)
        return(os.path.getsize("./" + os.path.basename(ncFileUrl)) / 1024)

    def add_to_ncml(self, ncFileUrl):
        file_path = "./ncml/" + self.get_file_name("./" + os.path.basename(ncFileUrl)) + ".ncml"
        # Replace 2nd line with <netcdf>
        with open(file_path, 'r') as f:
            get_all = f.readlines()
        with open(file_path, 'w') as f:
            for i, line in enumerate(get_all, 1):
                if i == 2:
                    f.writelines("<netcdf>\n")
                else:
                    f.writelines(line)

        # Remove last line </netcdf> from ncml file before append new tags
        os.system('sed -i "$ d" {0}'.format(file_path))
        # Append stuff
        with open(file_path, "a") as f:
            f.write("<title>%s</title><englishtitle>%s</englishtitle><filesize>%s</filesize><path>%s</path></netcdf>" %
                    (self.get_file_name("./" + os.path.basename(ncFileUrl)), self.get_english_title("./" + os.path.basename(ncFileUrl)), self.get_file_size("./" + os.path.basename(ncFileUrl)), self.get_file_path(ncFileUrl)))

    def xsltproc_to_iso(self, ncFileUrl):
        xslFile = "XSL/ncml2iso_modified_from_UnidataDD2MI_CMAN_Thomas_edits.xsl"
        parsedNcmlFile = ET.parse(
            "./ncml/" + self.get_file_name("./" + os.path.basename(ncFileUrl)) + ".ncml")
        xslt = ET.parse(xslFile)
        transform = ET.XSLT(xslt)
        isoXmlFile = transform(parsedNcmlFile)
        with open("./iso_xml/" + self.get_file_name("./" + os.path.basename(ncFileUrl)) + ".xml", "w") as f:
            f.write(ET.tostring(isoXmlFile, pretty_print=True))
        # print(ET.tostring(isoXmlFile, pretty_print=True))
        return(ET.tostring(isoXmlFile, pretty_print=True))

    def add_collection_metadata(self, ncFileUrl): 
        granule = "XSL/granule.xsl"
        f = open("./final_xml/" + self.get_file_name("./" + os.path.basename(ncFileUrl)) + ".xml", "w")
        subprocess.call(["xsltproc", "--stringparam", "collFile", "../NDBC-CMANWx.xml",
                         granule, "./iso_xml/" + self.get_file_name("./" + os.path.basename(ncFileUrl)) + ".xml"], stdout=f)
        f.close()

    def run_combined_defs(self, ncFileUrl):
    	print(basename(ncFileUrl))
    	self.download_nc_file_from_url(ncFileUrl)
        self.ncdump(ncFileUrl)
        self.add_to_ncml(ncFileUrl)
        self.xsltproc_to_iso(ncFileUrl)
        self.add_collection_metadata(ncFileUrl)
        self.delete_nc_file_after_processing(ncFileUrl)

    def go(self):
        p = Pool(5)
        p.map(self, self.get_nc_file_urls()[:])

    def __call__(self, ncFile):
        return self.run_combined_defs(ncFile)


# __main__
if __name__ == '__main__':
    start = time.time()

    create_output_dirs()

    cman = CMAN()
    cman.download_collection_level_file()
    cman.go()

    cleanup()

    print 'The program took ', time.time() - start, 'seconds to complete.'

# End __main__
