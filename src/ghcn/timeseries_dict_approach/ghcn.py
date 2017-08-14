import datetime
import logging
import netCDF4
import numpy as np
import os
import sys
import time
import urllib
import urllib2
# from multiprocessing import Pool
from ordereddict import OrderedDict


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

    # Returns dictionary of unique time values
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
                return dict(enumerate(list(sorted(uniqueTimeValues))))

        except KeyboardInterrupt:
            print(sys.exc_info()[0])
        except:
            logging.exception(fileId)
        finally:
            pass

    def get_time_index_for_day(self, line, dayIndex):
        # Initialize with first value of that line's month
        timeValue = netCDF4.date2num(datetime.datetime(int(line[11:15]), int(
            line[15:17]), 1, 12, 0, 0), units='days since 1770-01-01 12:00:00', calendar='gregorian')
        try:
            timeValue = netCDF4.date2num(datetime.datetime(int(line[11:15]), int(
                line[15:17]), dayIndex, 12, 0, 0), units='days since 1770-01-01 12:00:00', calendar='gregorian')
        except:
            return -1
        return timeValue

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

    def initialize_element_lists_with_time_key_and_placeholder_value(self, fileId):
        dictOfUniqueTimeValues = self.get_unique_time_values(fileId)

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
        placeholderElementsFlagsList = {}
        for item in uniqueElementFlags:
            if len(item) == 4:
                placeholderElementsFlagsList[
                    item] = OrderedDict(sorted(dictOfUniqueTimeValues.fromkeys(
                        dictOfUniqueTimeValues, -9999).items()))
            else:
                placeholderElementsFlagsList[
                    item] = OrderedDict(sorted(dictOfUniqueTimeValues.fromkeys(
                        dictOfUniqueTimeValues, ' ').items()))

        # print placeholderElementsFlagsList['tmax_mflag']
        # Returns dict of lists
        return placeholderElementsFlagsList

    def create_elements_flags_data_lists(self, fileId):
        # Get list of all time values of the file
        uniqueTimeValuesDict = self.get_unique_time_values(fileId)

        # Dict of lists
        elementAndFlagDicts = self.initialize_element_lists_with_time_key_and_placeholder_value(
            fileId)
        try:
            with open("./dly_data_as_txt/" + fileId + ".txt", "r") as file:
                # Loop over values of month in line according to III. here
                # ftp://ftp.ncdc.noaa.gov/pub/data/ghcn/daily/readme.txt
                for line in file:
                    # Determine the element of that line
                    element = line[17:21].lower()

                    # Add values to the placeholder lists inside of dictionary
                    # initialized at beginning of function

                    # VALUE1
                    timeIndex = self.get_time_index_for_day(
                        line, 1)
                    # Index where the line value needs to be inserted
                    indexInElementAndFlagDicts = uniqueTimeValuesDict.keys(
                    )[uniqueTimeValuesDict.values().index(timeIndex)]
                    # Insert the actual values
                    elementAndFlagDicts[element][
                        indexInElementAndFlagDicts] = line[21:26]
                    elementAndFlagDicts[
                        element + '_mflag'][indexInElementAndFlagDicts] = line[26:27]
                    elementAndFlagDicts[
                        element + '_qflag'][indexInElementAndFlagDicts] = line[27:28]
                    elementAndFlagDicts[
                        element + '_sflag'][indexInElementAndFlagDicts] = line[28:29]

                    # VALUE2
                    timeIndex = self.get_time_index_for_day(
                        line, 2)
                    # Index where the line value needs to be inserted
                    indexInElementAndFlagDicts = uniqueTimeValuesDict.keys(
                    )[uniqueTimeValuesDict.values().index(timeIndex)]
                    # Insert the actual values
                    elementAndFlagDicts[element][
                        indexInElementAndFlagDicts] = line[29:34]
                    elementAndFlagDicts[
                        element + '_mflag'][indexInElementAndFlagDicts] = line[34:35]
                    elementAndFlagDicts[
                        element + '_qflag'][indexInElementAndFlagDicts] = line[35:36]
                    elementAndFlagDicts[
                        element + '_sflag'][indexInElementAndFlagDicts] = line[36:37]

                    # VALUE3
                    timeIndex = self.get_time_index_for_day(
                        line, 3)
                    # Index where the line value needs to be inserted
                    indexInElementAndFlagDicts = uniqueTimeValuesDict.keys(
                    )[uniqueTimeValuesDict.values().index(timeIndex)]
                    # Insert the actual values
                    elementAndFlagDicts[element][
                        indexInElementAndFlagDicts] = line[37:42]
                    elementAndFlagDicts[
                        element + '_mflag'][indexInElementAndFlagDicts] = line[42:43]
                    elementAndFlagDicts[
                        element + '_qflag'][indexInElementAndFlagDicts] = line[43:44]
                    elementAndFlagDicts[
                        element + '_sflag'][indexInElementAndFlagDicts] = line[44:45]

                    # VALUE4
                    timeIndex = self.get_time_index_for_day(
                        line, 4)
                    # Index where the line value needs to be inserted
                    indexInElementAndFlagDicts = uniqueTimeValuesDict.keys(
                    )[uniqueTimeValuesDict.values().index(timeIndex)]
                    # Insert the actual values
                    elementAndFlagDicts[element][
                        indexInElementAndFlagDicts] = line[45:50]
                    elementAndFlagDicts[
                        element + '_mflag'][indexInElementAndFlagDicts] = line[50:51]
                    elementAndFlagDicts[
                        element + '_qflag'][indexInElementAndFlagDicts] = line[51:52]
                    elementAndFlagDicts[
                        element + '_sflag'][indexInElementAndFlagDicts] = line[52:53]

                    # VALUE5
                    timeIndex = self.get_time_index_for_day(
                        line, 5)
                    # Index where the line value needs to be inserted
                    indexInElementAndFlagDicts = uniqueTimeValuesDict.keys(
                    )[uniqueTimeValuesDict.values().index(timeIndex)]
                    # Insert the actual values
                    elementAndFlagDicts[element][
                        indexInElementAndFlagDicts] = line[53:58]
                    elementAndFlagDicts[
                        element + '_mflag'][indexInElementAndFlagDicts] = line[58:59]
                    elementAndFlagDicts[
                        element + '_qflag'][indexInElementAndFlagDicts] = line[59:60]
                    elementAndFlagDicts[
                        element + '_sflag'][indexInElementAndFlagDicts] = line[60:61]

                    # VALUE6
                    timeIndex = self.get_time_index_for_day(
                        line, 6)
                    # Index where the line value needs to be inserted
                    indexInElementAndFlagDicts = uniqueTimeValuesDict.keys(
                    )[uniqueTimeValuesDict.values().index(timeIndex)]
                    # Insert the actual values
                    elementAndFlagDicts[element][
                        indexInElementAndFlagDicts] = line[61:66]
                    elementAndFlagDicts[
                        element + '_mflag'][indexInElementAndFlagDicts] = line[66:67]
                    elementAndFlagDicts[
                        element + '_qflag'][indexInElementAndFlagDicts] = line[67:68]
                    elementAndFlagDicts[
                        element + '_sflag'][indexInElementAndFlagDicts] = line[68:69]

                    # VALUE7
                    timeIndex = self.get_time_index_for_day(
                        line, 7)
                    # Index where the line value needs to be inserted
                    indexInElementAndFlagDicts = uniqueTimeValuesDict.keys(
                    )[uniqueTimeValuesDict.values().index(timeIndex)]
                    # Insert the actual values
                    elementAndFlagDicts[element][
                        indexInElementAndFlagDicts] = line[69:74]
                    elementAndFlagDicts[
                        element + '_mflag'][indexInElementAndFlagDicts] = line[74:75]
                    elementAndFlagDicts[
                        element + '_qflag'][indexInElementAndFlagDicts] = line[75:76]
                    elementAndFlagDicts[
                        element + '_sflag'][indexInElementAndFlagDicts] = line[76:77]

                    # VALUE8
                    timeIndex = self.get_time_index_for_day(
                        line, 8)
                    # Index where the line value needs to be inserted
                    indexInElementAndFlagDicts = uniqueTimeValuesDict.keys(
                    )[uniqueTimeValuesDict.values().index(timeIndex)]
                    # Insert the actual values
                    elementAndFlagDicts[element][
                        indexInElementAndFlagDicts] = line[77:82]
                    elementAndFlagDicts[
                        element + '_mflag'][indexInElementAndFlagDicts] = line[82:83]
                    elementAndFlagDicts[
                        element + '_qflag'][indexInElementAndFlagDicts] = line[83:84]
                    elementAndFlagDicts[
                        element + '_sflag'][indexInElementAndFlagDicts] = line[84:85]

                    # VALUE9
                    timeIndex = self.get_time_index_for_day(
                        line, 9)
                    # Index where the line value needs to be inserted
                    indexInElementAndFlagDicts = uniqueTimeValuesDict.keys(
                    )[uniqueTimeValuesDict.values().index(timeIndex)]
                    # Insert the actual values
                    elementAndFlagDicts[element][
                        indexInElementAndFlagDicts] = line[85:90]
                    elementAndFlagDicts[
                        element + '_mflag'][indexInElementAndFlagDicts] = line[90:91]
                    elementAndFlagDicts[
                        element + '_qflag'][indexInElementAndFlagDicts] = line[91:92]
                    elementAndFlagDicts[
                        element + '_sflag'][indexInElementAndFlagDicts] = line[92:93]

                    # VALUE10
                    timeIndex = self.get_time_index_for_day(
                        line, 10)
                    # Index where the line value needs to be inserted
                    indexInElementAndFlagDicts = uniqueTimeValuesDict.keys(
                    )[uniqueTimeValuesDict.values().index(timeIndex)]
                    # Insert the actual values
                    elementAndFlagDicts[element][
                        indexInElementAndFlagDicts] = line[93:98]
                    elementAndFlagDicts[
                        element + '_mflag'][indexInElementAndFlagDicts] = line[98:99]
                    elementAndFlagDicts[
                        element + '_qflag'][indexInElementAndFlagDicts] = line[99:100]
                    elementAndFlagDicts[
                        element + '_sflag'][indexInElementAndFlagDicts] = line[100:101]

                    # VALUE11
                    timeIndex = self.get_time_index_for_day(
                        line, 11)
                    # Index where the line value needs to be inserted
                    indexInElementAndFlagDicts = uniqueTimeValuesDict.keys(
                    )[uniqueTimeValuesDict.values().index(timeIndex)]
                    # Insert the actual values
                    elementAndFlagDicts[element][
                        indexInElementAndFlagDicts] = line[101:106]
                    elementAndFlagDicts[
                        element + '_mflag'][indexInElementAndFlagDicts] = line[106:107]
                    elementAndFlagDicts[
                        element + '_qflag'][indexInElementAndFlagDicts] = line[107:108]
                    elementAndFlagDicts[
                        element + '_sflag'][indexInElementAndFlagDicts] = line[108:109]

                    # VALUE12
                    timeIndex = self.get_time_index_for_day(
                        line, 12)
                    # Index where the line value needs to be inserted
                    indexInElementAndFlagDicts = uniqueTimeValuesDict.keys(
                    )[uniqueTimeValuesDict.values().index(timeIndex)]
                    # Insert the actual values
                    elementAndFlagDicts[element][
                        indexInElementAndFlagDicts] = line[109:114]
                    elementAndFlagDicts[
                        element + '_mflag'][indexInElementAndFlagDicts] = line[114:115]
                    elementAndFlagDicts[
                        element + '_qflag'][indexInElementAndFlagDicts] = line[115:116]
                    elementAndFlagDicts[
                        element + '_sflag'][indexInElementAndFlagDicts] = line[116:117]

                    # VALUE13
                    timeIndex = self.get_time_index_for_day(
                        line, 13)
                    # Index where the line value needs to be inserted
                    indexInElementAndFlagDicts = uniqueTimeValuesDict.keys(
                    )[uniqueTimeValuesDict.values().index(timeIndex)]
                    # Insert the actual values
                    elementAndFlagDicts[element][
                        indexInElementAndFlagDicts] = line[117:122]
                    elementAndFlagDicts[
                        element + '_mflag'][indexInElementAndFlagDicts] = line[122:123]
                    elementAndFlagDicts[
                        element + '_qflag'][indexInElementAndFlagDicts] = line[123:124]
                    elementAndFlagDicts[
                        element + '_sflag'][indexInElementAndFlagDicts] = line[124:125]

                    # VALUE14
                    timeIndex = self.get_time_index_for_day(
                        line, 14)
                    # Index where the line value needs to be inserted
                    indexInElementAndFlagDicts = uniqueTimeValuesDict.keys(
                    )[uniqueTimeValuesDict.values().index(timeIndex)]
                    # Insert the actual values
                    elementAndFlagDicts[element][
                        indexInElementAndFlagDicts] = line[125:130]
                    elementAndFlagDicts[
                        element + '_mflag'][indexInElementAndFlagDicts] = line[130:131]
                    elementAndFlagDicts[
                        element + '_qflag'][indexInElementAndFlagDicts] = line[131:132]
                    elementAndFlagDicts[
                        element + '_sflag'][indexInElementAndFlagDicts] = line[132:133]

                    # VALUE15
                    timeIndex = self.get_time_index_for_day(
                        line, 15)
                    # Index where the line value needs to be inserted
                    indexInElementAndFlagDicts = uniqueTimeValuesDict.keys(
                    )[uniqueTimeValuesDict.values().index(timeIndex)]
                    # Insert the actual values
                    elementAndFlagDicts[element][
                        indexInElementAndFlagDicts] = line[133:138]
                    elementAndFlagDicts[
                        element + '_mflag'][indexInElementAndFlagDicts] = line[138:139]
                    elementAndFlagDicts[
                        element + '_qflag'][indexInElementAndFlagDicts] = line[139:140]
                    elementAndFlagDicts[
                        element + '_sflag'][indexInElementAndFlagDicts] = line[140:141]

                    # VALUE16
                    timeIndex = self.get_time_index_for_day(
                        line, 16)
                    # Index where the line value needs to be inserted
                    indexInElementAndFlagDicts = uniqueTimeValuesDict.keys(
                    )[uniqueTimeValuesDict.values().index(timeIndex)]
                    # Insert the actual values
                    elementAndFlagDicts[element][
                        indexInElementAndFlagDicts] = line[141:146]
                    elementAndFlagDicts[
                        element + '_mflag'][indexInElementAndFlagDicts] = line[146:147]
                    elementAndFlagDicts[
                        element + '_qflag'][indexInElementAndFlagDicts] = line[147:148]
                    elementAndFlagDicts[
                        element + '_sflag'][indexInElementAndFlagDicts] = line[148:149]

                    # VALUE17
                    timeIndex = self.get_time_index_for_day(
                        line, 17)
                    # Index where the line value needs to be inserted
                    indexInElementAndFlagDicts = uniqueTimeValuesDict.keys(
                    )[uniqueTimeValuesDict.values().index(timeIndex)]
                    # Insert the actual values
                    elementAndFlagDicts[element][
                        indexInElementAndFlagDicts] = line[149:154]
                    elementAndFlagDicts[
                        element + '_mflag'][indexInElementAndFlagDicts] = line[154:155]
                    elementAndFlagDicts[
                        element + '_qflag'][indexInElementAndFlagDicts] = line[155:156]
                    elementAndFlagDicts[
                        element + '_sflag'][indexInElementAndFlagDicts] = line[156:157]

                    # VALUE18
                    timeIndex = self.get_time_index_for_day(
                        line, 18)
                    # Index where the line value needs to be inserted
                    indexInElementAndFlagDicts = uniqueTimeValuesDict.keys(
                    )[uniqueTimeValuesDict.values().index(timeIndex)]
                    # Insert the actual values
                    elementAndFlagDicts[element][
                        indexInElementAndFlagDicts] = line[157:162]
                    elementAndFlagDicts[
                        element + '_mflag'][indexInElementAndFlagDicts] = line[162:163]
                    elementAndFlagDicts[
                        element + '_qflag'][indexInElementAndFlagDicts] = line[163:164]
                    elementAndFlagDicts[
                        element + '_sflag'][indexInElementAndFlagDicts] = line[164:165]

                    # VALUE19
                    timeIndex = self.get_time_index_for_day(
                        line, 19)
                    # Index where the line value needs to be inserted
                    indexInElementAndFlagDicts = uniqueTimeValuesDict.keys(
                    )[uniqueTimeValuesDict.values().index(timeIndex)]
                    # Insert the actual values
                    elementAndFlagDicts[element][
                        indexInElementAndFlagDicts] = line[165:170]
                    elementAndFlagDicts[
                        element + '_mflag'][indexInElementAndFlagDicts] = line[170:171]
                    elementAndFlagDicts[
                        element + '_qflag'][indexInElementAndFlagDicts] = line[171:172]
                    elementAndFlagDicts[
                        element + '_sflag'][indexInElementAndFlagDicts] = line[172:173]

                    # VALUE20
                    timeIndex = self.get_time_index_for_day(
                        line, 20)
                    # Index where the line value needs to be inserted
                    indexInElementAndFlagDicts = uniqueTimeValuesDict.keys(
                    )[uniqueTimeValuesDict.values().index(timeIndex)]
                    # Insert the actual values
                    elementAndFlagDicts[element][
                        indexInElementAndFlagDicts] = line[173:178]
                    elementAndFlagDicts[
                        element + '_mflag'][indexInElementAndFlagDicts] = line[178:179]
                    elementAndFlagDicts[
                        element + '_qflag'][indexInElementAndFlagDicts] = line[179:180]
                    elementAndFlagDicts[
                        element + '_sflag'][indexInElementAndFlagDicts] = line[180:181]

                    # VALUE21
                    timeIndex = self.get_time_index_for_day(
                        line, 21)
                    # Index where the line value needs to be inserted
                    indexInElementAndFlagDicts = uniqueTimeValuesDict.keys(
                    )[uniqueTimeValuesDict.values().index(timeIndex)]
                    # Insert the actual values
                    elementAndFlagDicts[element][
                        indexInElementAndFlagDicts] = line[181:186]
                    elementAndFlagDicts[
                        element + '_mflag'][indexInElementAndFlagDicts] = line[186:187]
                    elementAndFlagDicts[
                        element + '_qflag'][indexInElementAndFlagDicts] = line[187:188]
                    elementAndFlagDicts[
                        element + '_sflag'][indexInElementAndFlagDicts] = line[188:189]

                    # VALUE22
                    timeIndex = self.get_time_index_for_day(
                        line, 22)
                    # Index where the line value needs to be inserted
                    indexInElementAndFlagDicts = uniqueTimeValuesDict.keys(
                    )[uniqueTimeValuesDict.values().index(timeIndex)]
                    # Insert the actual values
                    elementAndFlagDicts[element][
                        indexInElementAndFlagDicts] = line[189:194]
                    elementAndFlagDicts[
                        element + '_mflag'][indexInElementAndFlagDicts] = line[194:195]
                    elementAndFlagDicts[
                        element + '_qflag'][indexInElementAndFlagDicts] = line[195:196]
                    elementAndFlagDicts[
                        element + '_sflag'][indexInElementAndFlagDicts] = line[196:197]

                    # VALUE23
                    timeIndex = self.get_time_index_for_day(
                        line, 23)
                    # Index where the line value needs to be inserted
                    indexInElementAndFlagDicts = uniqueTimeValuesDict.keys(
                    )[uniqueTimeValuesDict.values().index(timeIndex)]
                    # Insert the actual values
                    elementAndFlagDicts[element][
                        indexInElementAndFlagDicts] = line[197:202]
                    elementAndFlagDicts[
                        element + '_mflag'][indexInElementAndFlagDicts] = line[202:203]
                    elementAndFlagDicts[
                        element + '_qflag'][indexInElementAndFlagDicts] = line[203:204]
                    elementAndFlagDicts[
                        element + '_sflag'][indexInElementAndFlagDicts] = line[204:205]

                    # VALUE24
                    timeIndex = self.get_time_index_for_day(
                        line, 24)
                    # Index where the line value needs to be inserted
                    indexInElementAndFlagDicts = uniqueTimeValuesDict.keys(
                    )[uniqueTimeValuesDict.values().index(timeIndex)]
                    # Insert the actual values
                    elementAndFlagDicts[element][
                        indexInElementAndFlagDicts] = line[205:210]
                    elementAndFlagDicts[
                        element + '_mflag'][indexInElementAndFlagDicts] = line[210:211]
                    elementAndFlagDicts[
                        element + '_qflag'][indexInElementAndFlagDicts] = line[211:212]
                    elementAndFlagDicts[
                        element + '_sflag'][indexInElementAndFlagDicts] = line[212:213]

                    # VALUE25
                    timeIndex = self.get_time_index_for_day(
                        line, 25)
                    # Index where the line value needs to be inserted
                    indexInElementAndFlagDicts = uniqueTimeValuesDict.keys(
                    )[uniqueTimeValuesDict.values().index(timeIndex)]
                    # Insert the actual values
                    elementAndFlagDicts[element][
                        indexInElementAndFlagDicts] = line[213:218]
                    elementAndFlagDicts[
                        element + '_mflag'][indexInElementAndFlagDicts] = line[218:219]
                    elementAndFlagDicts[
                        element + '_qflag'][indexInElementAndFlagDicts] = line[219:220]
                    elementAndFlagDicts[
                        element + '_sflag'][indexInElementAndFlagDicts] = line[220:221]

                    # VALUE26
                    timeIndex = self.get_time_index_for_day(
                        line, 26)
                    # Index where the line value needs to be inserted
                    indexInElementAndFlagDicts = uniqueTimeValuesDict.keys(
                    )[uniqueTimeValuesDict.values().index(timeIndex)]
                    # Insert the actual values
                    elementAndFlagDicts[element][
                        indexInElementAndFlagDicts] = line[221:226]
                    elementAndFlagDicts[
                        element + '_mflag'][indexInElementAndFlagDicts] = line[226:227]
                    elementAndFlagDicts[
                        element + '_qflag'][indexInElementAndFlagDicts] = line[227:228]
                    elementAndFlagDicts[
                        element + '_sflag'][indexInElementAndFlagDicts] = line[228:229]

                    # VALUE27
                    timeIndex = self.get_time_index_for_day(
                        line, 27)
                    # Index where the line value needs to be inserted
                    indexInElementAndFlagDicts = uniqueTimeValuesDict.keys(
                    )[uniqueTimeValuesDict.values().index(timeIndex)]
                    # Insert the actual values
                    elementAndFlagDicts[element][
                        indexInElementAndFlagDicts] = line[229:234]
                    elementAndFlagDicts[
                        element + '_mflag'][indexInElementAndFlagDicts] = line[234:235]
                    elementAndFlagDicts[
                        element + '_qflag'][indexInElementAndFlagDicts] = line[235:236]
                    elementAndFlagDicts[
                        element + '_sflag'][indexInElementAndFlagDicts] = line[236:237]

                    # VALUE28
                    timeIndex = self.get_time_index_for_day(
                        line, 28)
                    # Index where the line value needs to be inserted
                    indexInElementAndFlagDicts = uniqueTimeValuesDict.keys(
                    )[uniqueTimeValuesDict.values().index(timeIndex)]
                    # Insert the actual values
                    elementAndFlagDicts[element][
                        indexInElementAndFlagDicts] = line[237:242]
                    elementAndFlagDicts[
                        element + '_mflag'][indexInElementAndFlagDicts] = line[242:243]
                    elementAndFlagDicts[
                        element + '_qflag'][indexInElementAndFlagDicts] = line[243:244]
                    elementAndFlagDicts[
                        element + '_sflag'][indexInElementAndFlagDicts] = line[244:245]

                    # VALUE29
                    timeIndex = self.get_time_index_for_day(
                        line, 29)
                    if timeIndex != -1:
                        # Index where the line value needs to be inserted
                        indexInElementAndFlagDicts = uniqueTimeValuesDict.keys(
                        )[uniqueTimeValuesDict.values().index(timeIndex)]
                        # Insert the actual values
                        elementAndFlagDicts[element][
                            indexInElementAndFlagDicts] = line[245:250]
                        elementAndFlagDicts[
                            element + '_mflag'][indexInElementAndFlagDicts] = line[250:251]
                        elementAndFlagDicts[
                            element + '_qflag'][indexInElementAndFlagDicts] = line[251:252]
                        elementAndFlagDicts[
                            element + '_sflag'][indexInElementAndFlagDicts] = line[252:253]
                    else:
                        pass

                    # VALUE30
                    timeIndex = self.get_time_index_for_day(
                        line, 30)
                    if timeIndex != -1:
                        # Index where the line value needs to be inserted
                        indexInElementAndFlagDicts = uniqueTimeValuesDict.keys(
                        )[uniqueTimeValuesDict.values().index(timeIndex)]
                        # Insert the actual values
                        elementAndFlagDicts[element][
                            indexInElementAndFlagDicts] = line[253:258]
                        elementAndFlagDicts[
                            element + '_mflag'][indexInElementAndFlagDicts] = line[258:259]
                        elementAndFlagDicts[
                            element + '_qflag'][indexInElementAndFlagDicts] = line[259:260]
                        elementAndFlagDicts[
                            element + '_sflag'][indexInElementAndFlagDicts] = line[260:261]
                    else:
                        pass

                    # VALUE31
                    timeIndex = self.get_time_index_for_day(
                        line, 31)
                    if timeIndex != -1:
                        # Index where the line value needs to be inserted
                        indexInElementAndFlagDicts = uniqueTimeValuesDict.keys(
                        )[uniqueTimeValuesDict.values().index(timeIndex)]
                        # Insert the actual values
                        elementAndFlagDicts[element][
                            indexInElementAndFlagDicts] = line[261:266]
                        elementAndFlagDicts[
                            element + '_mflag'][indexInElementAndFlagDicts] = line[266:267]
                        elementAndFlagDicts[
                            element + '_qflag'][indexInElementAndFlagDicts] = line[267:268]
                        elementAndFlagDicts[
                            element + '_sflag'][indexInElementAndFlagDicts] = line[268:269]
                    else:
                        pass
            # print elementAndFlagDicts['tmin'][7518]
            return elementAndFlagDicts

        except KeyboardInterrupt:
            print(sys.exc_info()[0])
        except:
            logging.exception(fileId)
        finally:
            pass
    # End create_elements_flags_data_lists(self, fileId)

    def parse_to_netCDF(self, fileId):
        # Get unique time values of file for time variable array
        uniqueTimeValues = self.get_unique_time_values(fileId).values()
        # Set type of list values
        uniqueTimeValues = map(float, uniqueTimeValues)

        # Get element and flag arrays and their values
        elementAndFlagDicts = self.create_elements_flags_data_lists(fileId)

        print(fileId)
        try:
            # Empty lists for variables, more information here
            # ftp://ftp.ncdc.noaa.gov/pub/data/ghcn/daily/readme.txt
            ID = []
            YEAR = []
            MONTH = []

            # Fill lists with substring values 0-269 per record per line from
            # .dly file
            with open("./dly_data_as_txt/" + fileId + ".txt", "r") as file:
                for line in file:
                    ID.append(line[0:11])
                    YEAR.append(line[11:15])
                    MONTH.append(line[15:17])

            # Create netcdf data object
            with netCDF4.Dataset('./netcdf/ghcn-daily_v3.22.' + datetime.datetime.today().strftime('%Y-%m-%d') + '_' + fileId + '.nc', mode="w", format='NETCDF4') as ds:
                # Define dimensions
                ds.createDimension('time')
                ds.createDimension('station', 1)

                # Define variables
                ds.createVariable('time', 'd', ('time',))[
                    :] = np.array(uniqueTimeValues)[:]

                # Variables from data arrays
                '''for key, value in elementAndFlagDicts.iteritems():
                    ds.createVariable(key, np.array(value.values()).dtype, ('time',))[
                        :] = np.array(value.values())[:]'''

                for key in OrderedDict(sorted(elementAndFlagDicts.items())):
                    print key
                    if len(key) == 4:
                        for key, value in elementAndFlagDicts.iteritems():
                            ds.createVariable(key, 'i2', ('time',))[
                                :] = np.array(value.values())[:]
                    else:
                        for key, value in elementAndFlagDicts.iteritems():
                            ds.createVariable(key, 'c', ('time',))[
                                :] = np.array(value.values())[:]

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

    testfile = "AGE00147710"

    ghcn = GHCN()

    ghcn.download_dly_file(testfile)
    ghcn.get_unique_time_values(testfile)
    ghcn.get_unique_elements(testfile)
    ghcn.initialize_element_lists_with_time_key_and_placeholder_value(testfile)
    ghcn.create_elements_flags_data_lists(testfile)
    ghcn.parse_to_netCDF(testfile)

    print('The program took ', (time.time() - start), 'seconds to complete.')

# End __main__
