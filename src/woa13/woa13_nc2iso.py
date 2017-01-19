import lxml.etree as ET
import glob
import os

class WOA13:
	"""docstring for WOA13"""
	def __init__(self):
		self.ncFiles = []

        def find_nc_files(self):
            os.chdir("/nodc/users/tjaensch/python/src/woa13/netcdf/")
            for file in glob.glob("*.nc"):
        	    self.ncFiles.append(file)
            print(self.ncFiles)
            return self.ncFiles

# __main__
if __name__ == '__main__':
    woa13 = WOA13()
    woa13.find_nc_files()
# End __main__
