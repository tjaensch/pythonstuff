import datetime
import logging
import netCDF4
import numpy as np
import os
import sys
import time
import urllib
import urllib2
#from multiprocessing import Pool


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
            if len(item) == 4:
                emptyElementFlagsList[item] = ['-9999'] * len(self.get_unique_time_values(fileId))
            else:
                emptyElementFlagsList[item] = [' '] * len(self.get_unique_time_values(fileId))    
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

        print(fileId)
        try:
            # Empty lists for variables, more information here ftp://ftp.ncdc.noaa.gov/pub/data/ghcn/daily/readme.txt
            ID = []
            YEAR = []
            MONTH = []

            # Fill lists with substring values 0-269 per record per line from .dly file
            with open ("./dly_data_as_txt/" + fileId + ".txt", "r") as file:
                for line in file:
                    ID.append(line[0:11])
                    YEAR.append(line[11:15])
                    MONTH.append(line[15:17])

            # Create netcdf data object
            with netCDF4.Dataset('./netcdf/ghcn-daily_v3.22.' + datetime.datetime.today().strftime('%Y-%m-%d') + '_' + fileId + '.nc', mode="w", format='NETCDF4') as ds:
                # Define dimensions
                ds.createDimension('time')
                ds.createDimension('station', 1)

                # Global metadata attributes
                ds.Conventions = "CF-1.6, ACDD-1.3" 
                ds.ncei_template_version = "NCEI_NetCDF_Grid_Template_v2.0"
                ds.title = 'GHCN-Daily Surface Observations from ' + fileId
                ds.source = 'Surface Observations: 1) the U.S. Collection; 2) the International Collection; 3) Government Exchange Data; and 4) the Global Summary of the Day'
                ds.id = 'ghcn-daily_v3.22.' + datetime.datetime.today().strftime('%Y-%m-%d') + '_' + fileId + '.nc'
                ds.naming_authority = 'gov.noaa.ncei'
                ds.summary = 'Global Historical Climatology Network - Daily (GHCN-Daily) is an integrated database of daily climate summaries from land surface stations across the globe. GHCN-Daily is comprised of daily climate records from numerous sources that have been integrated and subjected to a common suite of quality assurance reviews. GHCN-Daily contains records from over 100,000 stations in 180 countries and territories. NCEI provides numerous daily variables, including maximum and minimum temperature, total daily precipitation, snowfall, and snow depth; however, about one half of the stations report precipitation only. Both the record length and period of record vary by station and cover intervals ranging from less than a year to more than 175 years.'
                ds.featureType = 'timeSeries'
                ds.cdm_data_type = 'Point'
                ds.history = 'File updated on ' + datetime.datetime.today().strftime('%Y-%m-%d-%H:%M:%S')
                ds.date_modified = datetime.datetime.today().strftime('%Y-%m-%d-%H:%M:%S')
                ds.date_created = datetime.datetime.today().strftime('%Y-%m-%d-%H:%M:%S')
                ds.product_version = 'Version 3.22'
                ds.processing_level = 'NOAA Level 2'
                ds.institution = 'NOAA National Centers for Environmental Information'
                ds.creator_url = 'https://www.ncei.noaa.gov/'
                ds.creator_email = 'matthew.menne@noaa.gov'
                ds.publisher_institution = 'NOAA National Centers for Environmental Information'
                ds.publisher_url = 'http://www.ncei.noaa.gov/'
                ds.publisher_email = 'ncei.orders@noaa.gov'
                ds.geospatial_lat_min = self.latDict[fileId]
                ds.geospatial_lat_max = self.latDict[fileId]
                ds.geospatial_lon_min = self.lonDict[fileId]
                ds.geospatial_lon_max = self.lonDict[fileId]
                ds.time_coverage_start = YEAR[0] + '-' + MONTH[0] + '-01'
                ds.time_coverage_end = YEAR[-1] + '-' + MONTH[-1] + '-01'
                ds.keywords = 'Earth Science > Atmosphere > Precipitation > Precipitation Amount > 24 Hour Precipitation Amount, Earth Science > Terrestrial Hydrosphere > Snow/Ice > Snow Depth, Earth Science > Atmosphere > Atmospheric Temperature > Surface Temperature > Maximum/Minimum Temperature > 24 Hour Maximum Temperature, Earth Science > Atmosphere > Atmospheric Temperature > Surface Temperature > Maximum/Minimum Temperature > 24 Hour Minimum Temperature'
                ds.keywords_vocabulary = 'Global Change Master Directory (GCMD) Earth Science Keywords'
                ds.standard_name_vocabulary = 'CF Standard Name Table (v46, 25 July 2017)'
                ds.metadata_link = 'https://doi.org/10.7289/V5D21VHZ'
                ds.references = 'https://doi.org/10.1175/JTECH-D-11-00103.1, https://doi.org/10.1175/2010JAMC2375.1, https://doi.org/10.1175/2007JAMC1706.1'
                ds.comment = 'Data was converted from native fixed-length text (DLY) format to NetCDF-4 format following metadata conventions.'

                # Define variables
                ds.createVariable('time_array', np.array(uniqueTimeValues).dtype, ('time',))[
                    :] = np.array(self.get_unique_time_values(fileId))[:]
                time.long_name = 'Center time of day'
                time.standard_name = 'time'
                time.units = 'days since 1700-01-01 12:00:00'
                time.axis = 'T'
                time.calendar = 'gregorian'
                time.coverage_content_type = 'coordinate'

                prcp = ds.createVariable('prcp', 'short')
                prcp.long_name = 'Total Daily Precipitation (mm)'
                prcp.standard_name = 'precipitation_amount'
                prcp.units = 'mm'
                prcp.scale_factor = 0.1
                prcp.missing_value = -9999
                prcp.FillValue = -9999
                prcp.valid_min = 0
                prcp.valid_max = 10000
                prcp.coordinates = 'lat lon alt station_name'
                prcp.ancillary_variables = 'mflag qflag sflag'

                snow = ds.createVariable('snow', 'short')
                snow.long_name = 'Total Daily Snowfall (mm)'
                snow.standard_name = 'snowfall_amount'
                snow.units = 'mm'
                snow.scale_factor = 1.0
                snow.missing_value = -9999
                snow.FillValue = -9999
                snow.valid_min = 0
                snow.valid_max = 1000
                snow.coordinates = 'lat lon alt station_name'
                snow.ancillary_variables = 'mflag qflag sflag'

                snwd = ds.createVariable('snwd', 'short')
                snwd.long_name = 'Snow Depth at time of obs (mm)'
                snwd.standard_name = 'snowfall_amount'
                snwd.units = 'mm'
                snwd.scale_factor = 1.0
                snwd.missing_value = -9999
                snwd.FillValue = -9999
                snwd.valid_min = 0
                snwd.valid_max = 1000
                snwd.coordinates = 'lat lon alt station_name'
                snwd.ancillary_variables = 'mflag qflag sflag'

                tmax = ds.createVariable('tmax', 'short')
                tmax.long_name = 'Maximum Temperature (degrees C)'
                tmax.standard_name = 'air_temperature'
                tmax.units = 'degrees_Celsius'
                tmax.scale_factor = 0.1
                tmax.missing_value = -9999
                tmax.FillValue = -9999
                tmax.valid_min = -500
                tmax.valid_max = 500
                tmax.coordinates = 'lat lon alt station_name'
                tmax.ancillary_variables = 'mflag qflag sflag'

                tmin = ds.createVariable('tmin', 'short')
                tmin.long_name = 'Minimum Temperature (degrees C)'
                tmin.standard_name = 'air_temperature'
                tmin.units = 'degrees_Celsius'
                tmin.scale_factor = 0.1
                tmin.missing_value = -9999
                tmin.FillValue = -9999
                tmin.valid_min = -500
                tmin.valid_max = 500
                tmin.coordinates = 'lat lon alt station_name'
                tmin.ancillary_variables = 'mflag qflag sflag'

                mflag = ds.createVariable('mflag', 'c')
                mflag.long_name = 'Measurement flag for the first day of the month with ten possible values'
                mflag.standard_name = 'status_flag'
                mflag.FillValue = ''
                mflag.flag_values = '1 B D H K L O P T W'
                mflag.flag_meanings = 'no_measurement_information_applicable precipitation_total_formed_from_two_12-hour_totals precipitation_total_formed_from_four_six-hour_totals represents_highest_or_lowest_hourly_temperature_(TMAX_or_TMIN)_or_the_average_of_hourly_values_(TAVG) converted_from_knots temperature_appears_to_be_lagged_with_respect_to_reported_hour_of_observation converted_from_oktas identified_as_missing_presumed_zero_in_DSI_3200_and_3206 trace_of_precipitation_snowfall_or_snow_depth converted_from_16-point_WBAN_code_(for_wind_direction)'
                mflag.coordinates = 'lat lon alt station_name'

                qflag = ds.createVariable('qflag', 'c')
                qflag.long_name = 'Quality flag for the first day of the month with fifteen possible values'
                qflag.standard_name = 'status_flag'
                qflag.FillValue = ''
                qflag.flag_values = '1 D G I K L M N O R S T W X Z'
                qflag.flag_meanings = 'did_not_fail_any_quality_assurance_check failed_duplicate_check failed_gap_check failed_internal_consistency_check failed_streak_frequent-value_check failed_check_on_length_of_multiday_period failed_megaconsistency_check failed_naught_check failed_climatological_outlier_check failed_lagged_range_check failed_spatial_consistency_check failed_temporal_consistency_check temperature_too_warm_for_snow failed_bounds_check flagged_as_a_result_of_an_official_Datzilla_investigation'
                qflag.coordinates = 'lat lon alt station_name'

                sflag = ds.createVariable('sflag', 'c')
                sflag.long_name = 'Source flag for the first day of the month with twenty nine possible values'
                sflag.standard_name = 'status_flag'
                sflag.FillValue = ''
                sflag.flag_values = '1 0 6 7 A a B b C E F G H I K M N Q R r S s T U u W X Z z'
                sflag.flag_meanings = 'No_source_(data_value_missing) US_Cooperative_Summary_of_the_Day_(NCDC_DSI-3200) CDMP_Cooperative_Summary_of_the_Day_(NCDC_DSI-3206) US_Cooperative_Summary_of_the_Day_--_Transmitted_via_WxCoder3_(NCDC_DSI-3207) US_Automated_Surface_Observing_System_(ASOS)_real-time_data_(since_01_January_2006) Australian_data_from_the_Australian_Bureau_of_Meteorology US_ASOS_data_for_October_2000_to_December_2005_(NCDC_DSI-3211) Belarus_update Environment_Canada European_Climate_Assessment_and_Dataset_(Klein_Tank_et_al_2002) US_Fort_data Official_Global_Climate_Observing_System_(GCOS)_or_other_government-supplied_data High_Plains_Regional_Climate_Center_real-time_data International_collection_(non_US_data_received_through_personal_contacts US_Cooperative_Summary_of_the_Day_data_digitized_from_paper_observer_forms_(from_2011_to_present) Monthly_METAR_Extract_(additional_ASOS_data) Community_Collaborative_Rain_Hail_and_Snow_(CoCoRaHS) Data_from_several_African_countries_that_had_been_quarantined_withheld_from_public_release_until_permission_was_granted_from_the_respective_meteorological_services NCEI_Reference_Network_Database_(Climate_Reference_Network_and_Regional_Climate_Reference_Network) All-Russian_Research_Institute_of_Hydrometeorological_Information-World_Data_Center Global_Summary_of_the_Day_(NCDC_DSI-9618) China_Meteorological_Administration_National_Meteorological_Information_Center_Climatic_Data_Center SNOwpack_TELemtry_(SNOTEL)_data_obtained_from_the_US_Department_of_Agriculture_s_Natural_Resources_Conservation_Service Remote_Automatic_Weather_Station_(RAWS)_data_obtained_from_the_Western_Regional_Climate_Center Ukraine_update WBAN_ASOS_Summary_of_the_Day_from_NCDC_s_Integrated_Surface_Data_(ISD) US_First-Order_Summary_of_the_Day_(NCDC_DSI-3210) Datzilla_official_additions_or_replacements Uzbekistan_update'
                sflag.coordinates = 'lat lon alt station_name'
                sflag.comment = 'When data are available for the same time from more than one source, the highest priority source is chosen according to the following priority order (from highest to lowest): Z,R,0,6,C,X,W,K,7,F,B,M,r,E,z,u,b,s,a,G,Q,I,A,N,T,U,H,S. NOTE for Global Summary of the Day: S values are derived from hourly synoptic reports exchanged on the Global Telecommunications System (GTS). Daily values derived in this fashion may differ significantly from true daily data, particularly for precipitation (i.e., use with caution).'

                lat = ds.createVariable('lat', 'f')
                lat.long_name = 'Latitude'
                lat.standard_name = 'latitude'
                lat.units = 'degrees_north'
                lat.axis = 'Y'
                lat.coverage_content_type = 'coordinate'

                lon = ds.createVariable('lon', 'f')
                lon.long_name = 'Longitude'
                lon.standard_name = 'longitude'
                lon.units = 'degrees_east'
                lon.axis = 'X'
                lon.coverage_content_type = 'coordinate'

                alt = ds.createVariable('alt', 'f')
                alt.long_name = 'Station Altitude'
                alt.standard_name = 'surface_altitude'
                alt.units = 'm'
                alt.axis = 'Z'
                alt.coverage_content_type = 'coordinate'
                alt.positive = 'up'

                station_name = ds.createVariable('station_name', 'S1')
                station_name.long_name = self.stationLongNameDict[fileId]
                station_name.standard_name = 'platform_name'
                station_name.cf_role = 'timeseries_id'
                station_name.coverage_content_type = 'coordinate'

                station_id = ds.createVariable('station_id', 'S1')
                station_id.long_name = ID[0]
                station_id.standard_name = 'platform_id'


                # Variables from data arrays
                for key, value in elementAndFlagArrays.iteritems():
                    ds.createVariable(key + '_array', np.array(value).dtype, ('time',))[
                        :] = np.array(value)[:]

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

    stationIds = ghcn.get_station_info()

    for stationId in stationIds:
        ghcn.download_dly_file(stationId)
        ghcn.get_unique_time_values(stationId)
        ghcn.create_dict_from_unique_time_values_list(stationId)
        ghcn.get_unique_elements(stationId)
        ghcn.initialize_empty_element_lists(stationId)
        ghcn.create_elements_flags_data_lists(stationId)
        ghcn.parse_to_netCDF(stationId)

    print('The program took ', (time.time() - start)/2400, 'hours to complete.')

# End __main__