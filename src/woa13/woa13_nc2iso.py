import lxml.etree as ET
import glob
import os
import subprocess

def create_output_dirs():
	if not os.path.exists("/nodc/users/tjaensch/python/src/woa13/ncml/"):
            os.makedirs("/nodc/users/tjaensch/python/src/woa13/ncml/")

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

        def nc2iso(self, ncFiles):
        	for ncFile in ncFiles:
        		self.ncdump(ncFile)

# __main__
if __name__ == '__main__':
    
    create_output_dirs()

    woa13 = WOA13()
    ncFiles = woa13.find_nc_files()
    woa13.nc2iso(ncFiles)
# End __main__
