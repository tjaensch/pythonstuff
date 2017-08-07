import datetime
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
    """Program to convert GHCN daily files to netCDF; source files and information can be found here ftp://ftp.ncdc.noaa.gov/pub/data/ghcn/daily"""
    """thomas.jaensch@noaa.gov"""

    def __init__(self):
        # Lists and dictionaries with information from ftp://ftp.ncdc.noaa.gov/pub/data/ghcn/daily/ghcnd-stations.txt to be used in netCDF variables derived with def get_stationInfo
        self.stationIds = []
        self.latDict = {}
        self.lonDict = {}
        self.stationLongNameDict = {}

    def get_stationInfo(self):
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

    def initialize_numbered_1_31_VALUE_MFLAG_QFLAG_SFLAG_lists(self):
        numberedList = {}
        for i in xrange(1,32):
            numberedList['VALUE' + str(i)] = []
            numberedList['MFLAG' + str(i)] = []
            numberedList['QFLAG' + str(i)] = []
            numberedList['SFLAG' + str(i)] = []
        return numberedList

    def parse_to_netCDF(self, fileId):
        print(fileId)
        try:

            # Fill lists with substring values 0-269 per record per line from .dly file
            with open ("./dly_data_as_txt/" + fileId + ".txt", "r") as file:
                for line in file:
                    for i in range (1,32):
                        try: 
                            timeID = netCDF4.date2num(datetime.datetime(int(line[11:15]), int(line[15:17]), i, 12, 0, 0), units='days since 1770-01-01 12:00:00', calendar='gregorian')
                            print(timeID)
                            element = line[17:21]
                            print(element)
                        except:
                            pass
        
        except KeyboardInterrupt:
            print(sys.exc_info()[0])      
        except:
            logging.exception(fileId + ": ")
        finally:
            pass
    # End def parse_to_netCDF(self, fileId)

# __main__
if __name__ == '__main__':
    start = time.time()

    create_output_dirs()

    ghcn = GHCN()
    ghcn.download_dly_file('AGE00147710')
    ghcn.parse_to_netCDF('AGE00147710')

    print('The program took ', (time.time()-start)/60, 'minutes to complete.')
                
# End __main__
