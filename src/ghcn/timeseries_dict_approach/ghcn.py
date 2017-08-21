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
        self.elevationDict = {}
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
            self.elevationDict[line[0:11]] = line[31:37]
            self.stationLongNameDict[line[0:11]] = line[38:71].strip()

        return self.stationIds

    def download_dly_file(self, fileId):
        try:
            # Alternatively https://www1.ncdc.noaa.gov/ OR
            # ftp://ftp.ncdc.noaa.gov/
            url = 'https://www1.ncdc.noaa.gov/pub/data/ghcn/daily/all/%s.dly' % fileId
            urllib.urlretrieve(url, fileId + '.txt')
        except KeyboardInterrupt:
            print(sys.exc_info()[0])
        except:
            logging.exception(fileId)
        finally:
            pass

    def make_subdir_based_on_file_name(self, fileId):
        dirName = fileId[:4]
        if not os.path.exists('./netcdf/' + dirName):
            os.makedirs('./netcdf/' + dirName)
        return dirName

    # Returns dictionary of unique time values
    def get_unique_time_values(self, fileId):
        uniqueTimeValues = set()
        try:
            with open(fileId + ".txt", "r") as file:
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
            with open(fileId + ".txt", "r") as file:
                for line in file:
                    uniqueElements.add(line[17:21])
                return dict(enumerate(list(uniqueElements)))

        except KeyboardInterrupt:
            print(sys.exc_info()[0])
        except:
            logging.exception(fileId)
        finally:
            pass

    def initialize_element_lists_with_time_key_and_placeholder_value(self, fileId, dictOfUniqueTimeValues, uniqueElements):
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
        # Returns dict of lists
        return placeholderElementsFlagsList

    def create_elements_flags_data_lists(self, fileId, uniqueTimeValuesDict, elementAndFlagDicts):
        try:
            with open(fileId + ".txt", "r") as file:
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
            print len(elementAndFlagDicts)
            return elementAndFlagDicts

        except KeyboardInterrupt:
            print(sys.exc_info()[0])
        except:
            logging.exception(fileId)
        finally:
            pass
    # End create_elements_flags_data_lists(self, fileId)

    def parse_to_netCDF(self, fileId, uniqueTimeValues, elementAndFlagDicts):
        # Get unique time values of file for time variable array
        uniqueTimeValues = uniqueTimeValues.values()

        # Get element and flag arrays and their values
        #elementAndFlagDicts = self.create_elements_flags_data_lists(fileId)

        print(fileId)
        try:
            # Empty lists for variables, more information here
            # ftp://ftp.ncdc.noaa.gov/pub/data/ghcn/daily/readme.txt
            ID = []
            YEAR = []
            MONTH = []

            # Fill lists with substring values 0-269 per record per line from
            # .dly file
            with open(fileId + ".txt", "r") as file:
                for line in file:
                    ID.append(line[0:11])
                    YEAR.append(line[11:15])
                    MONTH.append(line[15:17])

            # Create netcdf data object
            with netCDF4.Dataset('./netcdf/' + self.make_subdir_based_on_file_name(fileId) + '/ghcn-daily_v3.22.' + datetime.datetime.today().strftime('%Y-%m-%d') + '_' + fileId + '.nc', mode="w", format='NETCDF4_CLASSIC') as ds:
                # Define dimensions
                ds.createDimension('time')
                ds.createDimension('station', 1)

                # Define variables
                ds.createVariable('time', 'd', ('time',))[
                    :] = np.array(uniqueTimeValues)[:]
                ds.variables['time'].long_name = 'Center time of day'
                ds.variables['time'].standard_name = 'time'
                ds.variables[
                    'time'].units = 'days since 1700-01-01 12:00:00'
                ds.variables['time'].axis = 'T'
                ds.variables['time'].calendar = 'gregorian'
                ds.variables['time'].coverage_content_type = 'coordinate'

                if 'prcp' in elementAndFlagDicts:
                    prcp = ds.createVariable('prcp', 'short', ('station', 'time',), fill_value=-9999)[
                        :] = [np.array(OrderedDict(sorted(elementAndFlagDicts.items()))['prcp'].values())][:]
                    ds.variables[
                        'prcp'].long_name = 'Total Daily Precipitation (mm)'
                    ds.variables['prcp'].standard_name = 'precipitation_amount'
                    ds.variables['prcp'].units = 'mm'
                    ds.variables['prcp'].scale_factor = 0.1
                    ds.variables['prcp'].missing_value = -9999
                    ds.variables['prcp'].valid_min = 0
                    ds.variables['prcp'].valid_max = 10000
                    ds.variables[
                        'prcp'].coordinates = 'lat lon alt station_name'
                    ds.variables[
                        'prcp'].ancillary_variables = 'mflag qflag sflag'
                # Delete key from dictionary after processing to avoid double
                # processing below with dynamically generated value arrays
                try:
                    del elementAndFlagDicts['prcp']
                except KeyError:
                    pass

                if 'snow' in elementAndFlagDicts:
                    snow = ds.createVariable('snow', 'short', ('station', 'time',), fill_value=-9999)[
                        :] = [np.array(OrderedDict(sorted(elementAndFlagDicts.items()))['snow'].values())][:]
                    ds.variables[
                        'snow'].long_name = 'Total Daily Snowfall (mm)'
                    ds.variables['snow'].standard_name = 'snowfall_amount'
                    ds.variables['snow'].units = 'mm'
                    ds.variables['snow'].scale_factor = 1.0
                    ds.variables['snow'].missing_value = -9999
                    ds.variables['snow'].valid_min = 0
                    ds.variables['snow'].valid_max = 1000
                    ds.variables[
                        'snow'].coordinates = 'lat lon alt station_name'
                    ds.variables[
                        'snow'].ancillary_variables = 'mflag qflag sflag'
                # Delete key from dictionary after processing to avoid double
                # processing below with dynamically generated value arrays
                try:
                    del elementAndFlagDicts['snow']
                except KeyError:
                    pass

                if 'snwd' in elementAndFlagDicts:
                    snwd = ds.createVariable('snwd', 'short', ('station', 'time',), fill_value=-9999)[
                        :] = [np.array(OrderedDict(sorted(elementAndFlagDicts.items()))['snwd'].values())][:]
                    ds.variables[
                        'snwd'].long_name = 'Snow Depth at time of obs (mm)'
                    ds.variables['snwd'].standard_name = 'snowfall_amount'
                    ds.variables['snwd'].units = 'mm'
                    ds.variables['snwd'].scale_factor = 1.0
                    ds.variables['snwd'].missing_value = -9999
                    ds.variables['snwd'].valid_min = 0
                    ds.variables['snwd'].valid_max = 1000
                    ds.variables[
                        'snwd'].coordinates = 'lat lon alt station_name'
                    ds.variables[
                        'snwd'].ancillary_variables = 'mflag qflag sflag'
                # Delete key from dictionary after processing to avoid double
                # processing below with dynamically generated value arrays
                try:
                    del elementAndFlagDicts['snwd']
                except KeyError:
                    pass

                if 'tmax' in elementAndFlagDicts:
                    tmax = ds.createVariable('tmax', 'short', ('station', 'time',), fill_value=-9999)[
                        :] = [np.array(OrderedDict(sorted(elementAndFlagDicts.items()))['tmax'].values())][:]
                    ds.variables[
                        'tmax'].long_name = 'Maximum Temperature (degrees C)'
                    ds.variables['tmax'].standard_name = 'air_temperature'
                    ds.variables['tmax'].units = 'degrees_Celsius'
                    ds.variables['tmax'].scale_factor = 0.1
                    ds.variables['tmax'].missing_value = -9999
                    ds.variables['tmax'].valid_min = -500
                    ds.variables['tmax'].valid_max = 500
                    ds.variables[
                        'tmax'].coordinates = 'lat lon alt station_name'
                    ds.variables[
                        'tmax'].ancillary_variables = 'mflag qflag sflag'
                # Delete key from dictionary after processing to avoid double
                # processing below with dynamically generated value arrays
                try:
                    del elementAndFlagDicts['tmax']
                except KeyError:
                    pass

                if 'tmin' in elementAndFlagDicts:
                    tmin = ds.createVariable('tmin', 'short', ('station', 'time',), fill_value=-9999)[
                        :] = [np.array(OrderedDict(sorted(elementAndFlagDicts.items()))['tmin'].values())][:]
                    ds.variables[
                        'tmin'].long_name = 'Minimum Temperature (degrees C)'
                    ds.variables['tmin'].standard_name = 'air_temperature'
                    ds.variables['tmin'].units = 'degrees_Celsius'
                    ds.variables['tmin'].scale_factor = 0.1
                    ds.variables['tmin'].missing_value = -9999
                    ds.variables['tmin'].valid_min = -500
                    ds.variables['tmin'].valid_max = 500
                    ds.variables[
                        'tmin'].coordinates = 'lat lon alt station_name'
                    ds.variables[
                        'tmin'].ancillary_variables = 'mflag qflag sflag'
                # Delete key from dictionary after processing to avoid double
                # processing below with dynamically generated value arrays
                try:
                    del elementAndFlagDicts['tmin']
                except KeyError:
                    pass

                lat = ds.createVariable('lat', 'f', ('station',))
                lat.long_name = 'Latitude'
                lat.standard_name = 'latitude'
                lat.units = 'degrees_north'
                lat.axis = 'Y'
                lat.coverage_content_type = 'coordinate'
                lat[:] = np.array(self.latDict[fileId])

                lon = ds.createVariable('lon', 'f', ('station',))
                lon.long_name = 'Longitude'
                lon.standard_name = 'longitude'
                lon.units = 'degrees_east'
                lon.axis = 'X'
                lon.coverage_content_type = 'coordinate'
                lon[:] = np.array(self.lonDict[fileId])

                alt = ds.createVariable('alt', 'f', ('station',))
                alt.long_name = 'Station Altitude'
                alt.standard_name = 'surface_altitude'
                alt.units = 'm'
                alt.axis = 'Z'
                alt.coverage_content_type = 'coordinate'
                alt.positive = 'up'
                alt[:] = np.array(self.elevationDict[fileId])

                station_name = ds.createVariable(
                    'station_name', 'S1', ('station',))
                station_name.long_name = self.stationLongNameDict[fileId]
                station_name.standard_name = 'platform_name'
                station_name.cf_role = 'timeseries_id'
                station_name.coverage_content_type = 'coordinate'

                station_id = ds.createVariable(
                    'station_id', 'S1', ('station',))
                station_id.long_name = ID[0]
                station_id.standard_name = 'platform_id'

                # Dynamically create remaining variables from data arrays that
                # have not been called out and processed previously
                for key, value in OrderedDict(sorted(elementAndFlagDicts.items())).iteritems():
                    if len(key) == 4:
                        ds.createVariable(
                            key, 'i2', ('station', 'time',), fill_value=-9999)[:] = [np.array(value.values())][:]
                    if len(key) > 4:
                        ds.createVariable(key, 'c', ('station', 'time',), fill_value=' ')[
                            :] = [np.array(value.values())][:]
                        if 'mflag' in key:
                            ds.variables[
                                key].long_name = 'Measurement flag for the day of the month with ten possible values'
                            ds.variables[key].standard_name = 'status_flag'
                            ds.variables[key].missing_value = ' '
                            ds.variables[
                                key].flag_values = '1 B D H K L O P T W'
                            ds.variables[
                                key].flag_meanings = 'no_measurement_information_applicable precipitation_total_formed_from_two_12-hour_totals precipitation_total_formed_from_four_six-hour_totals represents_highest_or_lowest_hourly_temperature_(TMAX_or_TMIN)_or_the_average_of_hourly_values_(TAVG) converted_from_knots temperature_appears_to_be_lagged_with_respect_to_reported_hour_of_observation converted_from_oktas identified_as_missing_presumed_zero_in_DSI_3200_and_3206 trace_of_precipitation_snowfall_or_snow_depth converted_from_16-point_WBAN_code_(for_wind_direction)'
                            ds.variables[
                                key].coordinates = 'lat lon alt station_name'
                        if 'qflag' in key:
                            ds.variables[
                                key].long_name = 'Quality flag for the day of the month with fifteen possible values'
                            ds.variables[key].standard_name = 'status_flag'
                            ds.variables[key].missing_value = ' '
                            ds.variables[
                                key].flag_values = '1 D G I K L M N O R S T W X Z'
                            ds.variables[key].flag_meanings = 'did_not_fail_any_quality_assurance_check failed_duplicate_check failed_gap_check failed_internal_consistency_check failed_streak_frequent-value_check failed_check_on_length_of_multiday_period failed_megaconsistency_check failed_naught_check failed_climatological_outlier_check failed_lagged_range_check failed_spatial_consistency_check failed_temporal_consistency_check temperature_too_warm_for_snow failed_bounds_check flagged_as_a_result_of_an_official_Datzilla_investigation'
                            ds.variables[
                                key].coordinates = 'lat lon alt station_name'
                        if 'sflag' in key:
                            ds.variables[
                                key].long_name = 'Source flag for the day of the month with twenty nine possible values'
                            ds.variables[key].standard_name = 'status_flag'
                            ds.variables[key].missing_value = ' '
                            ds.variables[
                                key].flag_values = '1 0 6 7 A a B b C E F G H I K M N Q R r S s T U u W X Z z'
                            ds.variables[key].flag_meanings = 'No_source_(data_value_missing) US_Cooperative_Summary_of_the_Day_(NCDC_DSI-3200) CDMP_Cooperative_Summary_of_the_Day_(NCDC_DSI-3206) US_Cooperative_Summary_of_the_Day_--_Transmitted_via_WxCoder3_(NCDC_DSI-3207) US_Automated_Surface_Observing_System_(ASOS)_real-time_data_(since_01_January_2006) Australian_data_from_the_Australian_Bureau_of_Meteorology US_ASOS_data_for_October_2000_to_December_2005_(NCDC_DSI-3211) Belarus_update Environment_Canada European_Climate_Assessment_and_Dataset_(Klein_Tank_et_al_2002) US_Fort_data Official_Global_Climate_Observing_System_(GCOS)_or_other_government-supplied_data High_Plains_Regional_Climate_Center_real-time_data International_collection_(non_US_data_received_through_personal_contacts US_Cooperative_Summary_of_the_Day_data_digitized_from_paper_observer_forms_(from_2011_to_present) Monthly_METAR_Extract_(additional_ASOS_data) Community_Collaborative_Rain_Hail_and_Snow_(CoCoRaHS) Data_from_several_African_countries_that_had_been_quarantined_withheld_from_public_release_until_permission_was_granted_from_the_respective_meteorological_services NCEI_Reference_Network_Database_(Climate_Reference_Network_and_Regional_Climate_Reference_Network) All-Russian_Research_Institute_of_Hydrometeorological_Information-World_Data_Center Global_Summary_of_the_Day_(NCDC_DSI-9618) China_Meteorological_Administration_National_Meteorological_Information_Center_Climatic_Data_Center SNOwpack_TELemtry_(SNOTEL)_data_obtained_from_the_US_Department_of_Agriculture_s_Natural_Resources_Conservation_Service Remote_Automatic_Weather_Station_(RAWS)_data_obtained_from_the_Western_Regional_Climate_Center Ukraine_update WBAN_ASOS_Summary_of_the_Day_from_NCDC_s_Integrated_Surface_Data_(ISD) US_First-Order_Summary_of_the_Day_(NCDC_DSI-3210) Datzilla_official_additions_or_replacements Uzbekistan_update'
                            ds.variables[
                                key].coordinates = 'lat lon alt station_name'
                            ds.variables[
                                key].comment = 'When data are available for the same time from more than one source, the highest priority source is chosen according to the following priority order (from highest to lowest): Z,R,0,6,C,X,W,K,7,F,B,M,r,E,z,u,b,s,a,G,Q,I,A,N,T,U,H,S. NOTE for Global Summary of the Day: S values are derived from hourly synoptic reports exchanged on the Global Telecommunications System (GTS). Daily values derived in this fashion may differ significantly from true daily data, particularly for precipitation (i.e., use with caution).'

                # Global metadata attributes
                ds.Conventions = "CF-1.6, ACDD-1.3"
                ds.ncei_template_version = "NCEI_NetCDF_Grid_Template_v2.0"
                ds.title = 'GHCN-Daily Surface Observations from ' + fileId
                ds.source = 'Surface Observations: 1) the U.S. Collection; 2) the International Collection; 3) Government Exchange Data; and 4) the Global Summary of the Day'
                ds.id = 'ghcn-daily_v3.22.' + datetime.datetime.today().strftime('%Y-%m-%d') + \
                    '_' + fileId + '.nc'
                ds.naming_authority = 'gov.noaa.ncei'
                ds.summary = 'Global Historical Climatology Network - Daily (GHCN-Daily) is an integrated database of daily climate summaries from land surface stations across the globe. GHCN-Daily is comprised of daily climate records from numerous sources that have been integrated and subjected to a common suite of quality assurance reviews. GHCN-Daily contains records from over 100,000 stations in 180 countries and territories. NCEI provides numerous daily variables, including maximum and minimum temperature, total daily precipitation, snowfall, and snow depth; however, about one half of the stations report precipitation only. Both the record length and period of record vary by station and cover intervals ranging from less than a year to more than 175 years.'
                ds.featureType = 'timeSeries'
                ds.cdm_data_type = 'Point'
                ds.history = 'File updated on ' + \
                    datetime.datetime.today().strftime('%Y-%m-%dT%H:%M:%S') + 'Z'
                ds.date_modified = datetime.datetime.today().strftime('%Y-%m-%dT%H:%M:%S') + 'Z'
                ds.date_created = datetime.datetime.today().strftime('%Y-%m-%dT%H:%M:%S') + 'Z'
                ds.product_version = 'Version 3.22'
                ds.processing_level = 'NOAA Level 2'
                ds.institution = 'NOAA National Centers for Environmental Information'
                ds.creator_url = 'https://www.ncei.noaa.gov/'
                ds.creator_email = 'matthew.menne@noaa.gov'
                ds.publisher_institution = 'NOAA National Centers for Environmental Information'
                ds.publisher_url = 'http://www.ncei.noaa.gov/'
                ds.publisher_email = 'ncei.orders@noaa.gov'
                ds.geospatial_lat_min = float(self.latDict[fileId].strip())
                ds.geospatial_lat_max = float(self.latDict[fileId].strip())
                ds.geospatial_lon_min = float(self.lonDict[fileId].strip())
                ds.geospatial_lon_max = float(self.lonDict[fileId].strip())
                ds.time_coverage_start = YEAR[0] + '-' + MONTH[0] + '-01'
                ds.time_coverage_end = YEAR[-1] + '-' + MONTH[-1] + '-01'
                ds.keywords = 'Earth Science > Atmosphere > Precipitation > Precipitation Amount > 24 Hour Precipitation Amount, Earth Science > Terrestrial Hydrosphere > Snow/Ice > Snow Depth, Earth Science > Atmosphere > Atmospheric Temperature > Surface Temperature > Maximum/Minimum Temperature > 24 Hour Maximum Temperature, Earth Science > Atmosphere > Atmospheric Temperature > Surface Temperature > Maximum/Minimum Temperature > 24 Hour Minimum Temperature'
                ds.keywords_vocabulary = 'Global Change Master Directory (GCMD) Earth Science Keywords'
                ds.standard_name_vocabulary = 'CF Standard Name Table (v46, 25 July 2017)'
                ds.metadata_link = 'https://doi.org/10.7289/V5D21VHZ'
                ds.references = 'https://doi.org/10.1175/JTECH-D-11-00103.1, https://doi.org/10.1175/2010JAMC2375.1, https://doi.org/10.1175/2007JAMC1706.1'
                ds.comment = 'Data was converted from native fixed-length text (DLY) format to NetCDF-4 format following metadata conventions.'

        except KeyboardInterrupt:
            print(sys.exc_info()[0])
        except:
            logging.exception(fileId + ": ")
        finally:
            pass

        # Clean up text file
        os.remove(fileId + ".txt")

        # End def parse_to_netCDF(self, fileId)

# __main__
if __name__ == '__main__':
    start = time.time()

    create_output_dirs()

    #testfile = "AGE00147710"
    testfile = "BR002141011"

    ghcn = GHCN()

    stationIds = ghcn.get_station_info()

    '''for testfile in stationIds:
    ghcn.download_dly_file(testfile)
    dictOfUniqueTimeValues = ghcn.get_unique_time_values(testfile)
    uniqueElements = ghcn.get_unique_elements(testfile)
    placeholderElementsFlagsList = ghcn.initialize_element_lists_with_time_key_and_placeholder_value(testfile, dictOfUniqueTimeValues, uniqueElements)
    elementsAndFlagsDataLists = ghcn.create_elements_flags_data_lists(testfile, dictOfUniqueTimeValues, placeholderElementsFlagsList)
    ghcn.parse_to_netCDF(testfile, dictOfUniqueTimeValues, elementsAndFlagsDataLists)'''

    ghcn.download_dly_file(testfile)
    dictOfUniqueTimeValues = ghcn.get_unique_time_values(testfile)
    uniqueElements = ghcn.get_unique_elements(testfile)
    placeholderElementsFlagsList = ghcn.initialize_element_lists_with_time_key_and_placeholder_value(testfile, dictOfUniqueTimeValues, uniqueElements)
    elementsAndFlagsDataLists = ghcn.create_elements_flags_data_lists(testfile, dictOfUniqueTimeValues, placeholderElementsFlagsList)
    ghcn.parse_to_netCDF(testfile, dictOfUniqueTimeValues, elementsAndFlagsDataLists)

    print('The program took ', (time.time() - start), 'seconds to complete.')

# End __main__
