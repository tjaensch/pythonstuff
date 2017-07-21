#import csv
import netCDF4
import numpy as np
import os
import time
import urllib
import urllib2


def create_output_dirs():
    if not os.path.exists("./dly_data_as_txt/"):
            os.makedirs("./dly_data_as_txt/")
    if not os.path.exists("./netcdf/"):
            os.makedirs("./netcdf/")

class GHCN:
    """docstring for ghcn"""

    def __init__(self):
        self.stationIds = []

    def get_ids(self):
        data = urllib2.urlopen("ftp://ftp.ncdc.noaa.gov/pub/data/ghcn/daily/ghcnd-stations.txt")
        for line in data:
            if not line:
                break
            # Get station IDs as substrings from each line in source file
            self.stationIds.append(line[:11])
        # print(self.stationIds)
        print(len(self.stationIds))
        return self.stationIds

    def download_dly_file(self, fileId):
            url = 'ftp://ftp.ncdc.noaa.gov/pub/data/ghcn/daily/all/%s.dly' %fileId
            urllib.urlretrieve(url, 'dly_data_as_txt/' + fileId + '.txt')

    def parse_to_netCDF(self, fileId):
        # Load source ASCII file into variable
        data = np.genfromtxt('/nodc/users/tjaensch/python_onestop.git/src/ghcn/dly_data_as_txt/%s' %fileId + '.txt', dtype=str, delimiter='\t')
        #print data

        # Create netcdf data object
        with netCDF4.Dataset('/nodc/users/tjaensch/python_onestop.git/src/ghcn/netcdf/%s.nc' %fileId, mode="w", format='NETCDF4') as ds:
            # File-level metadata attributes
            ds.Conventions = "CF-1.6" 
            ds.title = 'TBA'
            ds.institution = 'TBA'
            ds.source = 'TBA'
            ds.history = 'TBA'
            ds.references = 'TBA'
            ds.comment = 'TBA'

            # Define array dimensions
            station = ds.createDimension('station', data.shape[0])

            # Variable definitions
            station_data = ds.createVariable(fileId, data.dtype, ('station',))
            station_data[:] = data[:]
            print station_data
            # Add attributes
            station_data.units = 'the_proper_unit_string'
            station_data.long_name = 'long name that describes the data'
            station_data.standard_name = 'CF_standard_name'
            print ds


# __main__
if __name__ == '__main__':
    start = time.time()

    create_output_dirs()

    ghcn = GHCN()
    stationIds = ghcn.get_ids()
    
    for fileId in stationIds:
        ghcn.download_dly_file(fileId)
        ghcn.parse_to_netCDF(fileId)

    print 'The program took ', time.time()-start, 'seconds to complete.'
                
# End __main__
