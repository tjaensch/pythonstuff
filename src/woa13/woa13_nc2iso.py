import lxml.etree as ET
import glob
import os
import subprocess
from os.path import basename

def create_output_dirs():
	if not os.path.exists("/nodc/users/tjaensch/python/src/woa13/ncml/"):
            os.makedirs("/nodc/users/tjaensch/python/src/woa13/ncml/")
        if not os.path.exists("/nodc/users/tjaensch/python/src/woa13/iso_xml/"):
                os.makedirs("/nodc/users/tjaensch/python/src/woa13/iso_xml/")

class WOA13:
	"""docstring for WOA13"""
	def __init__(self):
		self.ncFiles = []

        def find_nc_files(self):
            os.chdir("/nodc/users/tjaensch/python/src/woa13/netcdf/")
            for file in glob.glob("*.nc"):
        	    self.ncFiles.append(file)
            print("%d files found in source directory" % len(self.ncFiles))
            return self.ncFiles

        def ncdump(self, ncFile):
        	f = open("/nodc/users/tjaensch/python/src/woa13/ncml/" + ncFile + "ml", "w")
        	subprocess.call(["ncdump", "-x", ncFile], stdout=f)
        	f.close()

        def get_file_name(self, ncFile):
            print(basename(ncFile))
            return(basename(ncFile))

        def get_file_path(self, ncFile):
            print(os.path.abspath(ncFile))
            return(os.path.abspath(ncFile))

        def get_file_size(self, ncFile):
            print(os.path.getsize(ncFile) / 1024)
            return(os.path.getsize(ncFile) / 1024)

        def add_to_ncml(self, ncFile):
            file_path = "/nodc/users/tjaensch/python/src/woa13/ncml/" + ncFile + "ml"
            #Replace 2nd line with <netcdf>
            with open(file_path,'r') as f:
                get_all=f.readlines()
            with open(file_path,'w') as f:
                for i,line in enumerate(get_all,1):
                    if i == 2:
                        f.writelines("<netcdf>\n")
                    else:
                        f.writelines(line)
            
            # Remove last line </netcdf> from ncml file before append new tags
            os.system('sed -i "$ d" {0}'.format(file_path))
            # Append stuff
            with open(file_path, "a") as f:
                f.write("<title>%s</title><filesize>%s</filesize><path>%s</path></netcdf>" % (self.get_file_name(ncFile), self.get_file_size(ncFile), self.get_file_path(ncFile)))

        def xsltproc_to_iso(self, ncFile):
            xslFile = "/nodc/users/tjaensch/onestop.git/xsl/woa13/XSL/ncml2iso_modified_from_UnidataDD2MI_demo_WOA_Thomas_edits.xsl"
            parsedNcmlFile = ET.parse("/nodc/users/tjaensch/python/src/woa13/ncml/" + self.get_file_name(ncFile)[:-3] + ".ncml")
            xslt = ET.parse(xslFile)
            transform = ET.XSLT(xslt)
            isoXmlFile = transform(parsedNcmlFile)
            with open("/nodc/users/tjaensch/python/src/woa13/iso_xml/" + self.get_file_name(ncFile)[:-3] + ".xml", "w") as f:
                f.write(ET.tostring(isoXmlFile, pretty_print=True))
            # print(ET.tostring(isoXmlFile, pretty_print=True))
            return(ET.tostring(isoXmlFile, pretty_print=True))
        	

# __main__
if __name__ == '__main__':
    
    create_output_dirs()

    woa13 = WOA13()
    ncFiles = woa13.find_nc_files()
    
    # Loop over each file in list
    for ncFile in ncFiles:
                woa13.ncdump(ncFile)
                woa13.add_to_ncml(ncFile)
                woa13.xsltproc_to_iso(ncFile)
                
# End __main__
