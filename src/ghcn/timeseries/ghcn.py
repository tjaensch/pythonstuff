import datetime
import logging
import netCDF4
import numpy as np
import os
import sys
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
    """Program to convert GHCN daily files to netCDF; source files and information can be found here ftp://ftp.ncdc.noaa.gov/pub/data/ghcn/daily"""
    """thomas.jaensch@noaa.gov"""

    def __init__(self):
        # Lists and dictionaries with information from ftp://ftp.ncdc.noaa.gov/pub/data/ghcn/daily/ghcnd-stations.txt to be used in netCDF variables derived with def get_stationInfo
        self.stationIds = []
        self.latDict = {}
        self.lonDict = {}
        self.stationLongNameDict = {}

    def get_station_info(self):
        # Alternatively https://www1.ncdc.noaa.gov/ OR ftp://ftp.ncdc.noaa.gov/
        data = urllib2.urlopen("https://www1.ncdc.noaa.gov/pub/data/ghcn/daily/ghcnd-stations.txt")
        for line in data:
            if not line:
                break
            # Get station IDs as substrings from each line in source file, etc.
            self.stationIds.append(line[0:11])
            self.latDict[line[0:11]] = line[12:20]
            self.lonDict[line[0:11]] = line[21:30]
            self.stationLongNameDict[line[0:11]] = line[38:71]
        return self.stationIds

    def download_dly_file(self, fileId):
        try:
            # Alternatively https://www1.ncdc.noaa.gov/ OR ftp://ftp.ncdc.noaa.gov/
            url = 'https://www1.ncdc.noaa.gov/pub/data/ghcn/daily/all/%s.dly' %fileId
            urllib.urlretrieve(url, 'dly_data_as_txt/' + fileId + '.txt')
        except KeyboardInterrupt:
            print(sys.exc_info()[0])
        except:
            logging.exception(fileId + ": ")
        finally:
            pass

    def get_unique_time_values(self, fileId):
        uniqueTimeValues = set()
        try:
            with open ("./dly_data_as_txt/" + fileId + ".txt", "r") as file:
                for line in file:
                    # Loop over days of month in line
                    for i in range (1,32):
                        try: 
                            uniqueTimeValues.add(netCDF4.date2num(datetime.datetime(int(line[11:15]), int(line[15:17]), i, 12, 0, 0), units='days since 1770-01-01 12:00:00', calendar='gregorian'))
                        except:
                            pass
                #print list(sorted(uniqueTimeValues))
                return list(sorted(uniqueTimeValues))
        
        except KeyboardInterrupt:
            print(sys.exc_info()[0])
        finally:
            pass

    # Find elements like "TMIN", "TMAX", etc.
    def get_unique_elements(self, fileId):
        uniqueElements = set()
        try:
            with open ("./dly_data_as_txt/" + fileId + ".txt", "r") as file:
                for line in file:
                    uniqueElements.add(line[17:21])
                return dict(enumerate(list(uniqueElements)))
        
        except KeyboardInterrupt:
            print(sys.exc_info()[0])
        finally:
            pass

    def create_dict_from_unique_time_values_list(self, fileId):
        list1 = self.get_unique_time_values(fileId)
        dictList = dict(enumerate(list1))
        return dictList

    def initialize_empty_element_lists(self, fileId):
        uniqueElements = self.get_unique_elements(fileId)
        uniqueElementFlags = []
        for i in uniqueElements.values():
            w = i
            x = i + str('_mflag')
            y = i + str('_qflag')
            z = i + str('_sflag')
            uniqueElementFlags.append(w.lower())
            uniqueElementFlags.append(x.lower())
            uniqueElementFlags.append(y.lower())
            uniqueElementFlags.append(z.lower())
        emptyElementFlagsList = {}
        for item in uniqueElementFlags:
            emptyElementFlagsList[item] = []
        return emptyElementFlagsList

    def create_flags_data_lists(self, fileId):
        flagArrays = self.initialize_empty_element_lists(fileId)
        print flagArrays

    def parse_to_netCDF(self, fileId):
        uniqueTimeValues = self.get_unique_time_values(fileId)
        # Create netcdf data object
        with netCDF4.Dataset('./netcdf/ghcn-daily_v3.22.' + datetime.datetime.today().strftime('%Y-%m-%d') + '_' + fileId + '.nc', mode="w", format='NETCDF4') as ds:
            # Define dimensions
            ds.createDimension('time')
            ds.createDimension('station', 1)

            # Define variables
            ds.createVariable('time', np.array(uniqueTimeValues).dtype, ('time',))[:] = np.array(self.get_unique_time_values(fileId))[:]
    # End def parse_to_netCDF(self, fileId)

# __main__
if __name__ == '__main__':
    start = time.time()

    create_output_dirs()

    testfile = 'AGE00147710'

    ghcn = GHCN()
    ghcn.download_dly_file(testfile)
    ghcn.get_unique_time_values(testfile)
    ghcn.create_dict_from_unique_time_values_list(testfile)
    ghcn.get_unique_elements(testfile)
    ghcn.initialize_empty_element_lists(testfile)
    ghcn.create_flags_data_lists(testfile)
    ghcn.parse_to_netCDF(testfile)

    print('The program took ', (time.time()-start), 'seconds to complete.')
                
# End __main__
