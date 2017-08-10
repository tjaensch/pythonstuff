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
        # Lists and dictionaries with information from
        # ftp://ftp.ncdc.noaa.gov/pub/data/ghcn/daily/ghcnd-stations.txt to be
        # used in netCDF variables derived with def get_stationInfo
        self.stationIds = []
        self.latDict = {}
        self.lonDict = {}
        self.stationLongNameDict = {}

    def get_station_info(self):
        # Alternatively https://www1.ncdc.noaa.gov/ OR ftp://ftp.ncdc.noaa.gov/
        data = urllib2.urlopen(
            "https://www1.ncdc.noaa.gov/pub/data/ghcn/daily/ghcnd-stations.txt")
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
            # Alternatively https://www1.ncdc.noaa.gov/ OR
            # ftp://ftp.ncdc.noaa.gov/
            url = 'https://www1.ncdc.noaa.gov/pub/data/ghcn/daily/all/%s.dly' % fileId
            urllib.urlretrieve(url, 'dly_data_as_txt/' + fileId + '.txt')
        except KeyboardInterrupt:
            print(sys.exc_info()[0])
        except:
            logging.exception(fileId)
        finally:
            pass

    def get_unique_time_values(self, fileId):
        uniqueTimeValues = set()
        try:
            with open("./dly_data_as_txt/" + fileId + ".txt", "r") as file:
                for line in file:
                    # Loop over days of month in line
                    for i in range(1, 32):
                        try:
                            uniqueTimeValues.add(netCDF4.date2num(datetime.datetime(int(line[11:15]), int(
                                line[15:17]), i, 12, 0, 0), units='days since 1770-01-01 12:00:00', calendar='gregorian'))
                        except:
                            pass
                # print list(sorted(uniqueTimeValues))
                return list(sorted(uniqueTimeValues))

        except KeyboardInterrupt:
            print(sys.exc_info()[0])
        except:
            logging.exception(fileId)
        finally:
            pass

    def get_time_index_for_day(self, line, dayIndex, allTimeValuesList):
        # Initialize with first value of that line's month
        timeValue = netCDF4.date2num(datetime.datetime(int(line[11:15]), int(
            line[15:17]), 1, 12, 0, 0), units='days since 1770-01-01 12:00:00', calendar='gregorian')
        try:
            timeValue = netCDF4.date2num(datetime.datetime(int(line[11:15]), int(
                line[15:17]), dayIndex, 12, 0, 0), units='days since 1770-01-01 12:00:00', calendar='gregorian')
        except:
            return -1
        return allTimeValuesList.index(timeValue)

    # Find elements like "TMIN", "TMAX", etc.
    def get_unique_elements(self, fileId):
        uniqueElements = set()
        try:
            with open("./dly_data_as_txt/" + fileId + ".txt", "r") as file:
                for line in file:
                    uniqueElements.add(line[17:21])
                return dict(enumerate(list(uniqueElements)))

        except KeyboardInterrupt:
            print(sys.exc_info()[0])
        except:
            logging.exception(fileId)
        finally:
            pass

    def create_dict_from_unique_time_values_list(self, fileId):
        uniqueTimeValuesList = self.get_unique_time_values(fileId)
        uniqueTimeValuesDict = dict(enumerate(uniqueTimeValuesList))
        return uniqueTimeValuesDict

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
            emptyElementFlagsList[item] = ['.'] * \
                len(self.get_unique_time_values(fileId))
        # Returns dict of lists
        return emptyElementFlagsList

    def create_elements_flags_data_lists(self, fileId):
        # Get list of all time values of the file
        allTimeValuesList = self.get_unique_time_values(fileId)

        # Dict of lists
        elementAndFlagArrays = self.initialize_empty_element_lists(fileId)
        try:
            with open("./dly_data_as_txt/" + fileId + ".txt", "r") as file:
                # Loop over values of month in line according to III. here
                # ftp://ftp.ncdc.noaa.gov/pub/data/ghcn/daily/readme.txt
                for line in file:
                    # Determine the element of that line
                    element = line[17:21].lower()

                    # Add values to the empty lists inside of dictionary initialized at beginning of function
                    # VALUE1
                    timeIndex = self.get_time_index_for_day(
                        line, 1, allTimeValuesList)
                    elementAndFlagArrays[element].insert(
                        timeIndex, line[21:26])
                    elementAndFlagArrays[element].pop(timeIndex + 1)

                    elementAndFlagArrays[
                        element + '_mflag'].insert(timeIndex, line[26:27])
                    elementAndFlagArrays[
                        element + '_qflag'].insert(timeIndex, line[27:28])
                    elementAndFlagArrays[
                        element + '_sflag'].insert(timeIndex, line[28:29])

                    elementAndFlagArrays[
                        element + '_mflag'].pop(timeIndex + 1)
                    elementAndFlagArrays[
                        element + '_qflag'].pop(timeIndex + 1)
                    elementAndFlagArrays[
                        element + '_sflag'].pop(timeIndex + 1)

                    # VALUE2
                    timeIndex = self.get_time_index_for_day(
                        line, 2, allTimeValuesList)
                    elementAndFlagArrays[element].insert(
                        timeIndex, line[29:34])
                    elementAndFlagArrays[element].pop(timeIndex + 1)
                    elementAndFlagArrays[
                        element + '_mflag'].insert(timeIndex, line[34:35])
                    elementAndFlagArrays[
                        element + '_qflag'].insert(timeIndex, line[35:36])
                    elementAndFlagArrays[
                        element + '_sflag'].insert(timeIndex, line[36:37])

                    elementAndFlagArrays[
                        element + '_mflag'].pop(timeIndex + 1)
                    elementAndFlagArrays[
                        element + '_qflag'].pop(timeIndex + 1)
                    elementAndFlagArrays[
                        element + '_sflag'].pop(timeIndex + 1)

                    # VALUE3
                    timeIndex = self.get_time_index_for_day(
                        line, 3, allTimeValuesList)
                    elementAndFlagArrays[element].insert(
                        timeIndex, line[37:42])
                    elementAndFlagArrays[element].pop(timeIndex + 1)
                    elementAndFlagArrays[
                        element + '_mflag'].insert(timeIndex, line[42:43])
                    elementAndFlagArrays[
                        element + '_qflag'].insert(timeIndex, line[43:44])
                    elementAndFlagArrays[
                        element + '_sflag'].insert(timeIndex, line[44:45])

                    elementAndFlagArrays[
                        element + '_mflag'].pop(timeIndex + 1)
                    elementAndFlagArrays[
                        element + '_qflag'].pop(timeIndex + 1)
                    elementAndFlagArrays[
                        element + '_sflag'].pop(timeIndex + 1)

                    # VALUE4
                    timeIndex = self.get_time_index_for_day(
                        line, 4, allTimeValuesList)
                    elementAndFlagArrays[element].insert(
                        timeIndex, line[45:50])
                    elementAndFlagArrays[element].pop(timeIndex + 1)
                    elementAndFlagArrays[
                        element + '_mflag'].insert(timeIndex, line[50:51])
                    elementAndFlagArrays[
                        element + '_qflag'].insert(timeIndex, line[51:52])
                    elementAndFlagArrays[
                        element + '_sflag'].insert(timeIndex, line[52:53])

                    elementAndFlagArrays[
                        element + '_mflag'].pop(timeIndex + 1)
                    elementAndFlagArrays[
                        element + '_qflag'].pop(timeIndex + 1)
                    elementAndFlagArrays[
                        element + '_sflag'].pop(timeIndex + 1)

                    # VALUE5
                    timeIndex = self.get_time_index_for_day(
                        line, 5, allTimeValuesList)
                    elementAndFlagArrays[element].insert(
                        timeIndex, line[53:58])
                    elementAndFlagArrays[element].pop(timeIndex + 1)
                    elementAndFlagArrays[
                        element + '_mflag'].insert(timeIndex, line[58:59])
                    elementAndFlagArrays[
                        element + '_qflag'].insert(timeIndex, line[59:60])
                    elementAndFlagArrays[
                        element + '_sflag'].insert(timeIndex, line[60:61])

                    elementAndFlagArrays[
                        element + '_mflag'].pop(timeIndex + 1)
                    elementAndFlagArrays[
                        element + '_qflag'].pop(timeIndex + 1)
                    elementAndFlagArrays[
                        element + '_sflag'].pop(timeIndex + 1)

                    # VALUE6
                    timeIndex = self.get_time_index_for_day(
                        line, 6, allTimeValuesList)
                    elementAndFlagArrays[element].insert(
                        timeIndex, line[61:66])
                    elementAndFlagArrays[element].pop(timeIndex + 1)
                    elementAndFlagArrays[
                        element + '_mflag'].insert(timeIndex, line[66:67])
                    elementAndFlagArrays[
                        element + '_qflag'].insert(timeIndex, line[67:68])
                    elementAndFlagArrays[
                        element + '_sflag'].insert(timeIndex, line[68:69])

                    elementAndFlagArrays[
                        element + '_mflag'].pop(timeIndex + 1)
                    elementAndFlagArrays[
                        element + '_qflag'].pop(timeIndex + 1)
                    elementAndFlagArrays[
                        element + '_sflag'].pop(timeIndex + 1)

                    # VALUE7
                    timeIndex = self.get_time_index_for_day(
                        line, 7, allTimeValuesList)
                    elementAndFlagArrays[element].insert(
                        timeIndex, line[69:74])
                    elementAndFlagArrays[element].pop(timeIndex + 1)
                    elementAndFlagArrays[
                        element + '_mflag'].insert(timeIndex, line[74:75])
                    elementAndFlagArrays[
                        element + '_qflag'].insert(timeIndex, line[75:76])
                    elementAndFlagArrays[
                        element + '_sflag'].insert(timeIndex, line[76:77])

                    elementAndFlagArrays[
                        element + '_mflag'].pop(timeIndex + 1)
                    elementAndFlagArrays[
                        element + '_qflag'].pop(timeIndex + 1)
                    elementAndFlagArrays[
                        element + '_sflag'].pop(timeIndex + 1)

                    # VALUE8
                    timeIndex = self.get_time_index_for_day(
                        line, 8, allTimeValuesList)
                    elementAndFlagArrays[element].insert(
                        timeIndex, line[77:82])
                    elementAndFlagArrays[element].pop(timeIndex + 1)
                    elementAndFlagArrays[
                        element + '_mflag'].insert(timeIndex, line[82:83])
                    elementAndFlagArrays[
                        element + '_qflag'].insert(timeIndex, line[83:84])
                    elementAndFlagArrays[
                        element + '_sflag'].insert(timeIndex, line[84:85])

                    elementAndFlagArrays[
                        element + '_mflag'].pop(timeIndex + 1)
                    elementAndFlagArrays[
                        element + '_qflag'].pop(timeIndex + 1)
                    elementAndFlagArrays[
                        element + '_sflag'].pop(timeIndex + 1)

                    # VALUE9
                    timeIndex = self.get_time_index_for_day(
                        line, 9, allTimeValuesList)
                    elementAndFlagArrays[element].insert(
                        timeIndex, line[85:90])
                    elementAndFlagArrays[element].pop(timeIndex + 1)
                    elementAndFlagArrays[
                        element + '_mflag'].insert(timeIndex, line[90:91])
                    elementAndFlagArrays[
                        element + '_qflag'].insert(timeIndex, line[91:92])
                    elementAndFlagArrays[
                        element + '_sflag'].insert(timeIndex, line[92:93])

                    elementAndFlagArrays[
                        element + '_mflag'].pop(timeIndex + 1)
                    elementAndFlagArrays[
                        element + '_qflag'].pop(timeIndex + 1)
                    elementAndFlagArrays[
                        element + '_sflag'].pop(timeIndex + 1)

                    # VALUE10
                    timeIndex = self.get_time_index_for_day(
                        line, 10, allTimeValuesList)
                    elementAndFlagArrays[element].insert(
                        timeIndex, line[93:98])
                    elementAndFlagArrays[element].pop(timeIndex + 1)
                    elementAndFlagArrays[
                        element + '_mflag'].insert(timeIndex, line[98:99])
                    elementAndFlagArrays[
                        element + '_qflag'].insert(timeIndex, line[99:100])
                    elementAndFlagArrays[
                        element + '_sflag'].insert(timeIndex, line[100:101])

                    elementAndFlagArrays[
                        element + '_mflag'].pop(timeIndex + 1)
                    elementAndFlagArrays[
                        element + '_qflag'].pop(timeIndex + 1)
                    elementAndFlagArrays[
                        element + '_sflag'].pop(timeIndex + 1)

                    # VALUE11
                    timeIndex = self.get_time_index_for_day(
                        line, 11, allTimeValuesList)
                    elementAndFlagArrays[element].insert(
                        timeIndex, line[101:106])
                    elementAndFlagArrays[element].pop(timeIndex + 1)
                    elementAndFlagArrays[
                        element + '_mflag'].insert(timeIndex, line[106:107])
                    elementAndFlagArrays[
                        element + '_qflag'].insert(timeIndex, line[107:108])
                    elementAndFlagArrays[
                        element + '_sflag'].insert(timeIndex, line[108:109])

                    elementAndFlagArrays[
                        element + '_mflag'].pop(timeIndex + 1)
                    elementAndFlagArrays[
                        element + '_qflag'].pop(timeIndex + 1)
                    elementAndFlagArrays[
                        element + '_sflag'].pop(timeIndex + 1)

                    # VALUE12
                    timeIndex = self.get_time_index_for_day(
                        line, 12, allTimeValuesList)
                    elementAndFlagArrays[element].insert(
                        timeIndex, line[109:114])
                    elementAndFlagArrays[element].pop(timeIndex + 1)
                    elementAndFlagArrays[
                        element + '_mflag'].insert(timeIndex, line[114:115])
                    elementAndFlagArrays[
                        element + '_qflag'].insert(timeIndex, line[115:116])
                    elementAndFlagArrays[
                        element + '_sflag'].insert(timeIndex, line[116:117])

                    elementAndFlagArrays[
                        element + '_mflag'].pop(timeIndex + 1)
                    elementAndFlagArrays[
                        element + '_qflag'].pop(timeIndex + 1)
                    elementAndFlagArrays[
                        element + '_sflag'].pop(timeIndex + 1)

                    # VALUE13
                    timeIndex = self.get_time_index_for_day(
                        line, 13, allTimeValuesList)
                    elementAndFlagArrays[element].insert(
                        timeIndex, line[117:122])
                    elementAndFlagArrays[element].pop(timeIndex + 1)
                    elementAndFlagArrays[
                        element + '_mflag'].insert(timeIndex, line[122:123])
                    elementAndFlagArrays[
                        element + '_qflag'].insert(timeIndex, line[123:124])
                    elementAndFlagArrays[
                        element + '_sflag'].insert(timeIndex, line[124:125])

                    elementAndFlagArrays[
                        element + '_mflag'].pop(timeIndex + 1)
                    elementAndFlagArrays[
                        element + '_qflag'].pop(timeIndex + 1)
                    elementAndFlagArrays[
                        element + '_sflag'].pop(timeIndex + 1)

                    # VALUE14
                    timeIndex = self.get_time_index_for_day(
                        line, 14, allTimeValuesList)
                    elementAndFlagArrays[element].insert(
                        timeIndex, line[125:130])
                    elementAndFlagArrays[element].pop(timeIndex + 1)
                    elementAndFlagArrays[
                        element + '_mflag'].insert(timeIndex, line[130:131])
                    elementAndFlagArrays[
                        element + '_qflag'].insert(timeIndex, line[131:132])
                    elementAndFlagArrays[
                        element + '_sflag'].insert(timeIndex, line[132:133])

                    elementAndFlagArrays[
                        element + '_mflag'].pop(timeIndex + 1)
                    elementAndFlagArrays[
                        element + '_qflag'].pop(timeIndex + 1)
                    elementAndFlagArrays[
                        element + '_sflag'].pop(timeIndex + 1)

                    # VALUE15
                    timeIndex = self.get_time_index_for_day(
                        line, 15, allTimeValuesList)
                    elementAndFlagArrays[element].insert(
                        timeIndex, line[133:138])
                    elementAndFlagArrays[element].pop(timeIndex + 1)
                    elementAndFlagArrays[
                        element + '_mflag'].insert(timeIndex, line[138:139])
                    elementAndFlagArrays[
                        element + '_qflag'].insert(timeIndex, line[139:140])
                    elementAndFlagArrays[
                        element + '_sflag'].insert(timeIndex, line[140:141])

                    elementAndFlagArrays[
                        element + '_mflag'].pop(timeIndex + 1)
                    elementAndFlagArrays[
                        element + '_qflag'].pop(timeIndex + 1)
                    elementAndFlagArrays[
                        element + '_sflag'].pop(timeIndex + 1)

                    # VALUE16
                    timeIndex = self.get_time_index_for_day(
                        line, 16, allTimeValuesList)
                    elementAndFlagArrays[element].insert(
                        timeIndex, line[141:146])
                    elementAndFlagArrays[element].pop(timeIndex + 1)
                    elementAndFlagArrays[
                        element + '_mflag'].insert(timeIndex, line[146:147])
                    elementAndFlagArrays[
                        element + '_qflag'].insert(timeIndex, line[147:148])
                    elementAndFlagArrays[
                        element + '_sflag'].insert(timeIndex, line[148:149])

                    elementAndFlagArrays[
                        element + '_mflag'].pop(timeIndex + 1)
                    elementAndFlagArrays[
                        element + '_qflag'].pop(timeIndex + 1)
                    elementAndFlagArrays[
                        element + '_sflag'].pop(timeIndex + 1)

                    # VALUE17
                    timeIndex = self.get_time_index_for_day(
                        line, 17, allTimeValuesList)
                    elementAndFlagArrays[element].insert(
                        timeIndex, line[149:154])
                    elementAndFlagArrays[element].pop(timeIndex + 1)
                    elementAndFlagArrays[
                        element + '_mflag'].insert(timeIndex, line[154:155])
                    elementAndFlagArrays[
                        element + '_qflag'].insert(timeIndex, line[155:156])
                    elementAndFlagArrays[
                        element + '_sflag'].insert(timeIndex, line[156:157])

                    elementAndFlagArrays[
                        element + '_mflag'].pop(timeIndex + 1)
                    elementAndFlagArrays[
                        element + '_qflag'].pop(timeIndex + 1)
                    elementAndFlagArrays[
                        element + '_sflag'].pop(timeIndex + 1)

                    # VALUE18
                    timeIndex = self.get_time_index_for_day(
                        line, 18, allTimeValuesList)
                    elementAndFlagArrays[element].insert(
                        timeIndex, line[157:162])
                    elementAndFlagArrays[element].pop(timeIndex + 1)
                    elementAndFlagArrays[
                        element + '_mflag'].insert(timeIndex, line[162:163])
                    elementAndFlagArrays[
                        element + '_qflag'].insert(timeIndex, line[163:164])
                    elementAndFlagArrays[
                        element + '_sflag'].insert(timeIndex, line[164:165])

                    elementAndFlagArrays[
                        element + '_mflag'].pop(timeIndex + 1)
                    elementAndFlagArrays[
                        element + '_qflag'].pop(timeIndex + 1)
                    elementAndFlagArrays[
                        element + '_sflag'].pop(timeIndex + 1)

                    # VALUE19
                    timeIndex = self.get_time_index_for_day(
                        line, 19, allTimeValuesList)
                    elementAndFlagArrays[element].insert(
                        timeIndex, line[165:170])
                    elementAndFlagArrays[element].pop(timeIndex + 1)
                    elementAndFlagArrays[
                        element + '_mflag'].insert(timeIndex, line[170:171])
                    elementAndFlagArrays[
                        element + '_qflag'].insert(timeIndex, line[171:172])
                    elementAndFlagArrays[
                        element + '_sflag'].insert(timeIndex, line[172:173])

                    elementAndFlagArrays[
                        element + '_mflag'].pop(timeIndex + 1)
                    elementAndFlagArrays[
                        element + '_qflag'].pop(timeIndex + 1)
                    elementAndFlagArrays[
                        element + '_sflag'].pop(timeIndex + 1)

                    # VALUE20
                    timeIndex = self.get_time_index_for_day(
                        line, 20, allTimeValuesList)
                    elementAndFlagArrays[element].insert(
                        timeIndex, line[173:178])
                    elementAndFlagArrays[element].pop(timeIndex + 1)
                    elementAndFlagArrays[
                        element + '_mflag'].insert(timeIndex, line[178:179])
                    elementAndFlagArrays[
                        element + '_qflag'].insert(timeIndex, line[179:180])
                    elementAndFlagArrays[
                        element + '_sflag'].insert(timeIndex, line[180:181])

                    elementAndFlagArrays[
                        element + '_mflag'].pop(timeIndex + 1)
                    elementAndFlagArrays[
                        element + '_qflag'].pop(timeIndex + 1)
                    elementAndFlagArrays[
                        element + '_sflag'].pop(timeIndex + 1)

                    # VALUE21
                    timeIndex = self.get_time_index_for_day(
                        line, 21, allTimeValuesList)
                    elementAndFlagArrays[element].insert(
                        timeIndex, line[181:186])
                    elementAndFlagArrays[element].pop(timeIndex + 1)
                    elementAndFlagArrays[
                        element + '_mflag'].insert(timeIndex, line[186:187])
                    elementAndFlagArrays[
                        element + '_qflag'].insert(timeIndex, line[187:188])
                    elementAndFlagArrays[
                        element + '_sflag'].insert(timeIndex, line[188:189])

                    elementAndFlagArrays[
                        element + '_mflag'].pop(timeIndex + 1)
                    elementAndFlagArrays[
                        element + '_qflag'].pop(timeIndex + 1)
                    elementAndFlagArrays[
                        element + '_sflag'].pop(timeIndex + 1)

                    # VALUE22
                    timeIndex = self.get_time_index_for_day(
                        line, 22, allTimeValuesList)
                    elementAndFlagArrays[element].insert(
                        timeIndex, line[189:194])
                    elementAndFlagArrays[element].pop(timeIndex + 1)
                    elementAndFlagArrays[
                        element + '_mflag'].insert(timeIndex, line[194:195])
                    elementAndFlagArrays[
                        element + '_qflag'].insert(timeIndex, line[195:196])
                    elementAndFlagArrays[
                        element + '_sflag'].insert(timeIndex, line[196:197])

                    elementAndFlagArrays[
                        element + '_mflag'].pop(timeIndex + 1)
                    elementAndFlagArrays[
                        element + '_qflag'].pop(timeIndex + 1)
                    elementAndFlagArrays[
                        element + '_sflag'].pop(timeIndex + 1)

                    # VALUE23
                    timeIndex = self.get_time_index_for_day(
                        line, 23, allTimeValuesList)
                    elementAndFlagArrays[element].insert(
                        timeIndex, line[197:202])
                    elementAndFlagArrays[element].pop(timeIndex + 1)
                    elementAndFlagArrays[
                        element + '_mflag'].insert(timeIndex, line[202:203])
                    elementAndFlagArrays[
                        element + '_qflag'].insert(timeIndex, line[203:204])
                    elementAndFlagArrays[
                        element + '_sflag'].insert(timeIndex, line[204:205])

                    elementAndFlagArrays[
                        element + '_mflag'].pop(timeIndex + 1)
                    elementAndFlagArrays[
                        element + '_qflag'].pop(timeIndex + 1)
                    elementAndFlagArrays[
                        element + '_sflag'].pop(timeIndex + 1)

                    # VALUE24
                    timeIndex = self.get_time_index_for_day(
                        line, 24, allTimeValuesList)
                    elementAndFlagArrays[element].insert(
                        timeIndex, line[205:210])
                    elementAndFlagArrays[element].pop(timeIndex + 1)
                    elementAndFlagArrays[
                        element + '_mflag'].insert(timeIndex, line[210:211])
                    elementAndFlagArrays[
                        element + '_qflag'].insert(timeIndex, line[211:212])
                    elementAndFlagArrays[
                        element + '_sflag'].insert(timeIndex, line[212:213])

                    elementAndFlagArrays[
                        element + '_mflag'].pop(timeIndex + 1)
                    elementAndFlagArrays[
                        element + '_qflag'].pop(timeIndex + 1)
                    elementAndFlagArrays[
                        element + '_sflag'].pop(timeIndex + 1)

                    # VALUE25
                    timeIndex = self.get_time_index_for_day(
                        line, 25, allTimeValuesList)
                    elementAndFlagArrays[element].insert(
                        timeIndex, line[213:218])
                    elementAndFlagArrays[element].pop(timeIndex + 1)
                    elementAndFlagArrays[
                        element + '_mflag'].insert(timeIndex, line[218:219])
                    elementAndFlagArrays[
                        element + '_qflag'].insert(timeIndex, line[219:220])
                    elementAndFlagArrays[
                        element + '_sflag'].insert(timeIndex, line[220:221])

                    elementAndFlagArrays[
                        element + '_mflag'].pop(timeIndex + 1)
                    elementAndFlagArrays[
                        element + '_qflag'].pop(timeIndex + 1)
                    elementAndFlagArrays[
                        element + '_sflag'].pop(timeIndex + 1)

                    # VALUE26
                    timeIndex = self.get_time_index_for_day(
                        line, 26, allTimeValuesList)
                    elementAndFlagArrays[element].insert(
                        timeIndex, line[221:226])
                    elementAndFlagArrays[element].pop(timeIndex + 1)
                    elementAndFlagArrays[
                        element + '_mflag'].insert(timeIndex, line[226:227])
                    elementAndFlagArrays[
                        element + '_qflag'].insert(timeIndex, line[227:228])
                    elementAndFlagArrays[
                        element + '_sflag'].insert(timeIndex, line[228:229])

                    elementAndFlagArrays[
                        element + '_mflag'].pop(timeIndex + 1)
                    elementAndFlagArrays[
                        element + '_qflag'].pop(timeIndex + 1)
                    elementAndFlagArrays[
                        element + '_sflag'].pop(timeIndex + 1)

                    # VALUE27
                    timeIndex = self.get_time_index_for_day(
                        line, 27, allTimeValuesList)
                    elementAndFlagArrays[element].insert(
                        timeIndex, line[229:234])
                    elementAndFlagArrays[element].pop(timeIndex + 1)
                    elementAndFlagArrays[
                        element + '_mflag'].insert(timeIndex, line[234:235])
                    elementAndFlagArrays[
                        element + '_qflag'].insert(timeIndex, line[235:236])
                    elementAndFlagArrays[
                        element + '_sflag'].insert(timeIndex, line[236:237])

                    elementAndFlagArrays[
                        element + '_mflag'].pop(timeIndex + 1)
                    elementAndFlagArrays[
                        element + '_qflag'].pop(timeIndex + 1)
                    elementAndFlagArrays[
                        element + '_sflag'].pop(timeIndex + 1)

                    # VALUE28
                    timeIndex = self.get_time_index_for_day(
                        line, 28, allTimeValuesList)
                    elementAndFlagArrays[element].insert(
                        timeIndex, line[237:242])
                    elementAndFlagArrays[element].pop(timeIndex + 1)
                    elementAndFlagArrays[
                        element + '_mflag'].insert(timeIndex, line[242:243])
                    elementAndFlagArrays[
                        element + '_qflag'].insert(timeIndex, line[243:244])
                    elementAndFlagArrays[
                        element + '_sflag'].insert(timeIndex, line[244:245])

                    elementAndFlagArrays[
                        element + '_mflag'].pop(timeIndex + 1)
                    elementAndFlagArrays[
                        element + '_qflag'].pop(timeIndex + 1)
                    elementAndFlagArrays[
                        element + '_sflag'].pop(timeIndex + 1)

                    # VALUE29
                    timeIndex = self.get_time_index_for_day(
                        line, 29, allTimeValuesList)
                    if timeIndex != -1:
                        elementAndFlagArrays[element].insert(
                            timeIndex, line[245:250])
                        elementAndFlagArrays[element].pop(timeIndex + 1)
                        elementAndFlagArrays[
                            element + '_mflag'].insert(timeIndex, line[250:251])
                        elementAndFlagArrays[
                            element + '_qflag'].insert(timeIndex, line[251:252])
                        elementAndFlagArrays[
                            element + '_sflag'].insert(timeIndex, line[252:253])

                        elementAndFlagArrays[
                            element + '_mflag'].pop(timeIndex + 1)
                        elementAndFlagArrays[
                            element + '_qflag'].pop(timeIndex + 1)
                        elementAndFlagArrays[
                            element + '_sflag'].pop(timeIndex + 1)
                    else:
                        pass

                    # VALUE30
                    timeIndex = self.get_time_index_for_day(
                        line, 30, allTimeValuesList)
                    if timeIndex != -1:
                        elementAndFlagArrays[element].insert(
                            timeIndex, line[253:258])
                        elementAndFlagArrays[element].pop(timeIndex + 1)
                        elementAndFlagArrays[
                            element + '_mflag'].insert(timeIndex, line[258:259])
                        elementAndFlagArrays[
                            element + '_qflag'].insert(timeIndex, line[259:260])
                        elementAndFlagArrays[
                            element + '_sflag'].insert(timeIndex, line[260:261])

                        elementAndFlagArrays[
                            element + '_mflag'].pop(timeIndex + 1)
                        elementAndFlagArrays[
                            element + '_qflag'].pop(timeIndex + 1)
                        elementAndFlagArrays[
                            element + '_sflag'].pop(timeIndex + 1)
                    else:
                        pass

                    # VALUE31
                    timeIndex = self.get_time_index_for_day(
                        line, 31, allTimeValuesList)
                    if timeIndex != -1:
                        elementAndFlagArrays[element].insert(
                            timeIndex, line[261:266])
                        elementAndFlagArrays[element].pop(timeIndex + 1)
                        elementAndFlagArrays[
                            element + '_mflag'].insert(timeIndex, line[266:267])
                        elementAndFlagArrays[
                            element + '_qflag'].insert(timeIndex, line[267:268])
                        elementAndFlagArrays[
                            element + '_sflag'].insert(timeIndex, line[268:269])

                        elementAndFlagArrays[
                            element + '_mflag'].pop(timeIndex + 1)
                        elementAndFlagArrays[
                            element + '_qflag'].pop(timeIndex + 1)
                        elementAndFlagArrays[
                            element + '_sflag'].pop(timeIndex + 1)
                    else:
                        pass

            return elementAndFlagArrays
            '''for key, value in elementAndFlagArrays.iteritems():
                print key, len(value)'''

        except KeyboardInterrupt:
            print(sys.exc_info()[0])
        except:
            logging.exception(fileId)
        finally:
            pass
    # End create_elements_flags_data_lists(self, fileId)

    def parse_to_netCDF(self, fileId):
        # Get unique time values of file for time variable array
        uniqueTimeValues = self.get_unique_time_values(fileId)

        # Get element and flag arrays and their values
        elementAndFlagArrays = self.create_elements_flags_data_lists(fileId)

        # Create netcdf data object
        with netCDF4.Dataset('./netcdf/ghcn-daily_v3.22.' + datetime.datetime.today().strftime('%Y-%m-%d') + '_' + fileId + '.nc', mode="w", format='NETCDF4') as ds:
            # Define dimensions
            ds.createDimension('time')
            ds.createDimension('station', 1)

            # Define variables
            ds.createVariable('time', np.array(uniqueTimeValues).dtype, ('time',))[
                :] = np.array(self.get_unique_time_values(fileId))[:]

            # Variables from data arrays
            for key, value in elementAndFlagArrays.iteritems():
                ds.createVariable(key, np.array(value).dtype, ('time',))[
                    :] = np.array(value)[:]

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
    ghcn.create_elements_flags_data_lists(testfile)
    ghcn.parse_to_netCDF(testfile)

    print('The program took ', (time.time() - start), 'seconds to complete.')

# End __main__
