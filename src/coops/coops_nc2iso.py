import lxml.etree as ET
import fnmatch
import glob
import time
import os
import random
import subprocess
from os.path import basename

def create_output_dirs():
	if not os.path.exists("/nodc/users/tjaensch/python.git/src/coops/ncml/"):
            os.makedirs("/nodc/users/tjaensch/python.git/src/coops/ncml/")
            if not os.path.exists("/nodc/users/tjaensch/python.git/src/coops/iso_xml/"):
                    os.makedirs("/nodc/users/tjaensch/python.git/src/coops/iso_xml/")
            if not os.path.exists("/nodc/users/tjaensch/python.git/src/coops/final_xml/"):
                    os.makedirs("/nodc/users/tjaensch/python.git/src/coops/final_xml/")
            if not os.path.exists("/nodc/users/tjaensch/python.git/src/coops/netcdf3/"):
                    os.makedirs("/nodc/users/tjaensch/python.git/src/coops/netcdf3/")

class COOPS:
	"""docstring for coops"""
	def __init__(self):
		self.ncFiles = []

        def find_nc_files(self):
            source_dir = "/nodc/web/data.nodc/htdocs/ndbc/co-ops"
            for root, dirnames, filenames in os.walk(source_dir, followlinks=True):
                for filename in fnmatch.filter(filenames, '*.nc'):
                    self.ncFiles.append(os.path.join(root,filename))
            print("%d files found in source directory" % len(self.ncFiles))
            return self.ncFiles

        def ncdump(self, ncFile):
            # Convert netcdf4 to netcdf3 for ncdump -x to work
            subprocess.call(["ncks", "-3", ncFile, "./netcdf3/" + self.get_file_name(ncFile) + ".nc"])
            # actual ncdump
            f = open("/nodc/users/tjaensch/python.git/src/coops/ncml/" + self.get_file_name(ncFile) + ".ncml", "w")
            subprocess.call(["ncdump", "-x", "./netcdf3/" + self.get_file_name(ncFile) + ".nc"], stdout=f)
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
            file_path = "/nodc/users/tjaensch/python.git/src/coops/ncml/" + self.get_file_name(ncFile) + ".ncml"
            #Replace 2nd line with <netcdf>
            with open(file_path,'r') as f:
                get_all = f.readlines()
            with open(file_path,'w') as f:
                for i, line in enumerate(get_all, 1):
                    if i == 2:
                        f.writelines("<netcdf>\n")
                    else:
                        f.writelines(line)
            
            # Remove last line </netcdf> from ncml file before append new tags
            os.system('sed -i "$ d" {0}'.format(file_path))
            # Append stuff
            with open(file_path, "a") as f:
                f.write("<title>%s</title><filesize>%s</filesize><path>%s</path><browsegraphic>%s</browsegraphic></netcdf>" % (self.get_file_name(ncFile), self.get_file_size(ncFile), self.get_file_path(ncFile), self.get_browse_graphic_link(ncFile)))

        def xsltproc_to_iso(self, ncFile):
            xslFile = "/nodc/users/tjaensch/xsl.git/coops/XSL/ncml2iso_modified_from_UnidataDD2MI_COOPS_Thomas_edits.xsl"
            parsedNcmlFile = ET.parse("/nodc/users/tjaensch/python.git/src/coops/ncml/" + self.get_file_name(ncFile) + ".ncml")
            xslt = ET.parse(xslFile)
            transform = ET.XSLT(xslt)
            isoXmlFile = transform(parsedNcmlFile)
            with open("/nodc/users/tjaensch/python.git/src/coops/iso_xml/" + self.get_file_name(ncFile) + ".xml", "w") as f:
                f.write(ET.tostring(isoXmlFile, pretty_print=True))
            # print(ET.tostring(isoXmlFile, pretty_print=True))
            return(ET.tostring(isoXmlFile, pretty_print=True))

        def add_collection_metadata(self, ncFile):
            isocofile = "/nodc/web/data.nodc/htdocs/nodc/archive/metadata/approved/iso/NDBC-COOPS.xml"
            granule = "/nodc/users/tjaensch/xsl.git/coops/XSL/granule.xsl"
            f = open("/nodc/users/tjaensch/python.git/src/coops/final_xml/" + self.get_file_name(ncFile) + ".xml", "w")
            subprocess.call(["xsltproc", "--stringparam", "collFile", isocofile, granule, "/nodc/users/tjaensch/python.git/src/coops/iso_xml/" + self.get_file_name(ncFile) + ".xml"], stdout=f)
            f.close()

        def get_browse_graphic_link(self, ncFile):
            return "blah"	

# __main__
if __name__ == '__main__':
    start = time.time()
    
    create_output_dirs()

    coops = COOPS()
    ncFiles = coops.find_nc_files()
    
    # Loop over each file in list
    for ncFile in ncFiles:
                coops.ncdump(ncFile)
                coops.add_to_ncml(ncFile)
                coops.xsltproc_to_iso(ncFile)
                coops.add_collection_metadata(ncFile)

    print 'The program took ', time.time()-start, 'seconds to complete.'
                
# End __main__
