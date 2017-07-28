import logging
import netCDF4
import numpy as np
import os
import time
import urllib
import urllib2
from multiprocessing import Pool


def create_output_dirs():
    logging.basicConfig(level=logging.DEBUG, filename='./errors.log')
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
        try:
            url = 'ftp://ftp.ncdc.noaa.gov/pub/data/ghcn/daily/all/%s.dly' %fileId
            urllib.urlretrieve(url, 'dly_data_as_txt/' + fileId + '.txt')
        except:
            logging.exception(fileId + ": ")
        finally:
            pass

    def parse_to_netCDF(self, fileId):
        try:
            # Load source ASCII file into variable
            data = np.genfromtxt('./dly_data_as_txt/%s' %fileId + '.txt', dtype=str, delimiter='\t')
            #print data

            # Create netcdf data object
            with netCDF4.Dataset('./netcdf/%s.nc' %fileId, mode="w", format='NETCDF4') as ds:
                # File-level metadata attributes
                ds.Conventions = "CF-1.6" 
                ds.title = 'TBA'
                ds.institution = 'TBA'
                ds.source = 'TBA'
                ds.history = 'TBA'
                ds.references = 'TBA'
                ds.comment = 'TBA'

                # Define array dimensions
                timeSeriesProfile = ds.createDimension('timeSeriesProfile', data.shape[0])

                # Variable definitions
                station_data = ds.createVariable(fileId, data.dtype, ('timeSeriesProfile',))
                station_data[:] = data[:]
                print station_data
                # Add attributes
                station_data.units = 'the_proper_unit_string'
                station_data.long_name = 'long name that describes the data'
                station_data.standard_name = 'CF_standard_name'
                print ds
        except:
            logging.exception(fileId + ": ")
        finally:
            pass

    def run_combined_defs(self, fileId):
            self.download_dly_file(fileId)
            self.parse_to_netCDF(fileId)

    def go(self):
            p = Pool(3)
            p.map(self, self.get_ids())

    def __call__(self, fileId):
        return self.run_combined_defs(fileId)


# __main__
if __name__ == '__main__':
    start = time.time()

    create_output_dirs()

    ghcn = GHCN()
    ghcn.go()

    print 'The program took ', (time.time()-start)/60, 'minutes to complete.'
                
# End __main__
