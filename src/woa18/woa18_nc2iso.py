import lxml.etree as ET
import fnmatch
import glob
import time
import os
import random
import subprocess
from os.path import basename

def create_output_dirs():
	if not os.path.exists("/nodc/users/tjaensch/python_onestop.git/src/woa18/ncml/"):
            os.makedirs("/nodc/users/tjaensch/python_onestop.git/src/woa18/ncml/")
            if not os.path.exists("/nodc/users/tjaensch/python_onestop.git/src/woa18/iso_xml/"):
                    os.makedirs("/nodc/users/tjaensch/python_onestop.git/src/woa18/iso_xml/")
            if not os.path.exists("/nodc/users/tjaensch/python_onestop.git/src/woa18/final_xml/"):
                    os.makedirs("/nodc/users/tjaensch/python_onestop.git/src/woa18/final_xml/")

class WOA18:
	"""docstring for WOA18"""
	def __init__(self):
		self.ncFiles = []

        def find_nc_files(self):
            source_dir = "/nodc/web/data.nodc/htdocs/woa/WOA18"
            for root, dirnames, filenames in os.walk(source_dir):
                for filename in fnmatch.filter(filenames, '*.nc'):
                    self.ncFiles.append(os.path.join(root,filename))
            print("%d files found in source directory" % len(self.ncFiles))
            return self.ncFiles

        def ncdump(self, ncFile):
        	f = open("/nodc/users/tjaensch/python_onestop.git/src/woa18/ncml/" + self.get_file_name(ncFile) + ".ncml", "w")
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
            print(os.path.getsize(ncFile) / 1024 / 1024)
            return(os.path.getsize(ncFile) / 1024 / 1024)

        def add_to_ncml(self, ncFile):
            file_path = "/nodc/users/tjaensch/python_onestop.git/src/woa18/ncml/" + self.get_file_name(ncFile) + ".ncml"
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
            xslFile = "/nodc/users/tjaensch/xsl.git/woa18/XSL/ncml2iso_modified_from_UnidataDD2MI_demo_WOA_Thomas_edits.xsl"
            parsedNcmlFile = ET.parse("/nodc/users/tjaensch/python_onestop.git/src/woa18/ncml/" + self.get_file_name(ncFile) + ".ncml")
            xslt = ET.parse(xslFile)
            transform = ET.XSLT(xslt)
            isoXmlFile = transform(parsedNcmlFile)
            with open("/nodc/users/tjaensch/python_onestop.git/src/woa18/iso_xml/" + self.get_file_name(ncFile) + ".xml", "w") as f:
                f.write(ET.tostring(isoXmlFile, pretty_print=True))
            # print(ET.tostring(isoXmlFile, pretty_print=True))
            return(ET.tostring(isoXmlFile, pretty_print=True))

        def add_collection_metadata(self, ncFile):
            isocofile = "/nodc/web/data.nodc/htdocs/nodc/archive/metadata/approved/iso/0176314.xml"
            granule = "/nodc/users/tjaensch/xsl.git/woa18/XSL/granule.xsl"
            f = open("/nodc/users/tjaensch/python_onestop.git/src/woa18/final_xml/" + self.get_file_name(ncFile) + ".xml", "w")
            subprocess.call(["xsltproc", "--stringparam", "collFile", isocofile, granule, "/nodc/users/tjaensch/python_onestop.git/src/woa18/iso_xml/" + self.get_file_name(ncFile) + ".xml"], stdout=f)
            f.close()

        def get_browse_graphic_link(self, ncFile):
            return "https://data.nodc.noaa.gov/cgi-bin/gfx?id=gov.noaa.nodc:0176314"
  	

# __main__
if __name__ == '__main__':
    start = time.time()
    
    create_output_dirs()

    woa18 = WOA18()
    ncFiles = woa18.find_nc_files()
    
    # Loop over each file in list
    for ncFile in ncFiles:
                woa18.ncdump(ncFile)
                woa18.add_to_ncml(ncFile)
                woa18.xsltproc_to_iso(ncFile)
                woa18.add_collection_metadata(ncFile)

    print 'The program took ', time.time()-start, 'seconds to complete.'
                
# End __main__
