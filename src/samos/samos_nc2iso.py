import lxml.etree as ET
import fnmatch
import glob
import time
import os
import subprocess
from multiprocessing import Pool
from os.path import basename


def create_output_dirs():
    if not os.path.exists("./ncml/"):
        os.makedirs("./ncml/")
        if not os.path.exists("./iso_xml/"):
            os.makedirs("./iso_xml/")
        if not os.path.exists("./final_xml/"):
            os.makedirs("./final_xml/")


class Samos:
    """docstring for samos"""

    def __init__(self):
        self.ncFiles = []

    def find_nc_files(self):
        source_dir = "/nodc/web/data.nodc/htdocs/coaps/samos/"
        for root, dirnames, filenames in os.walk(source_dir, followlinks=True):
            for filename in fnmatch.filter(filenames, '*.nc'):
                self.ncFiles.append(os.path.join(root, filename))
        print("%d files found in source directory" % len(self.ncFiles))
        return self.ncFiles

    def ncdump(self, ncFile):
        f = open("./ncml/" + self.get_file_name(ncFile) + ".ncml", "w")
        subprocess.call(["ncdump", "-x", ncFile], stdout=f)
        f.close()

    def get_file_name(self, ncFile):
        print(basename(ncFile)[:-3])
        return(basename(ncFile)[:-3])

    def get_file_path(self, ncFile):
        abspath = os.path.dirname(ncFile)[27:] + "/"
        print(abspath)
        return(abspath)

    def get_file_size(self, ncFile):
        print(os.path.getsize(ncFile) / 1024)
        return(os.path.getsize(ncFile) / 1024)

    def add_to_ncml(self, ncFile):
        file_path = "./ncml/" + self.get_file_name(ncFile) + ".ncml"
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
            f.write("<title>%s</title><filesize>%s</filesize><path>%s</path></netcdf>" %
                    (self.get_file_name(ncFile), self.get_file_size(ncFile), self.get_file_path(ncFile)))

    def xsltproc_to_iso(self, ncFile):
        xslFile = "/nodc/users/tjaensch/xsl.git/samos/XSL/ncml2iso_SAMOS_Thomas_edits.xsl"
        parsedNcmlFile = ET.parse(
            "./ncml/" + self.get_file_name(ncFile) + ".ncml")
        xslt = ET.parse(xslFile)
        transform = ET.XSLT(xslt)
        isoXmlFile = transform(parsedNcmlFile)
        with open("./iso_xml/" + self.get_file_name(ncFile) + ".xml", "w") as f:
            f.write(ET.tostring(isoXmlFile, pretty_print=True))
        # print(ET.tostring(isoXmlFile, pretty_print=True))
        return(ET.tostring(isoXmlFile, pretty_print=True))

    def add_collection_metadata(self, ncFile):
        isocofile = "/nodc/web/data.nodc/htdocs/nodc/archive/metadata/approved/iso/COAPS-SAMOS.xml"
        granule = "/nodc/users/tjaensch/xsl.git/samos/XSL/granule.xsl"
        f = open("./final_xml/" + self.get_file_name(ncFile) + ".xml", "w")
        subprocess.call(["xsltproc", "--stringparam", "collFile", isocofile,
                         granule, "./iso_xml/" + self.get_file_name(ncFile) + ".xml"], stdout=f)
        f.close()

    def run_combined_defs(self, ncFile):
        self.ncdump(ncFile)
        self.add_to_ncml(ncFile)
        self.xsltproc_to_iso(ncFile)
        self.add_collection_metadata(ncFile)

    def go(self):
        p = Pool(8)
        p.map(self, self.find_nc_files())

    def __call__(self, ncFile):
        return self.run_combined_defs(ncFile)

# __main__
if __name__ == '__main__':
    start = time.time()

    create_output_dirs()

    samos = Samos()
    samos.go()

    print 'The program took ', time.time() - start, 'seconds to complete.'

# End __main__
