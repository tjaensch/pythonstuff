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
        # Returns dict of lists    
        return emptyElementFlagsList

    def create_elements_flags_data_lists(self, fileId):
        # Dict of lists
        elementAndFlagArrays = self.initialize_empty_element_lists(fileId)
        try:
            with open ("./dly_data_as_txt/" + fileId + ".txt", "r") as file:
                # Loop over values of month in line according to III. here ftp://ftp.ncdc.noaa.gov/pub/data/ghcn/daily/readme.txt 
                for line in file:
                    # Determine the element of that line
                    element = line[17:21].lower()

                    # Add values to the empty lists inside of dictionary initialized at beginning of function
                    # VALUE1
                    elementAndFlagArrays[element].append(line[21:26])
                    elementAndFlagArrays[element + '_mflag'].append(line[26:27])
                    elementAndFlagArrays[element + '_qflag'].append(line[27:28])
                    elementAndFlagArrays[element + '_sflag'].append(line[28:29])

                    # VALUE2
                    elementAndFlagArrays[element].append(line[29:34])
                    elementAndFlagArrays[element + '_mflag'].append(line[34:35])
                    elementAndFlagArrays[element + '_qflag'].append(line[35:36])
                    elementAndFlagArrays[element + '_sflag'].append(line[36:37])

                    # VALUE3
                    elementAndFlagArrays[element].append(line[37:42])
                    elementAndFlagArrays[element + '_mflag'].append(line[42:43])
                    elementAndFlagArrays[element + '_qflag'].append(line[43:44])
                    elementAndFlagArrays[element + '_sflag'].append(line[44:45])

                    # VALUE4
                    elementAndFlagArrays[element].append(line[45:50])
                    elementAndFlagArrays[element + '_mflag'].append(line[50:51])
                    elementAndFlagArrays[element + '_qflag'].append(line[51:52])
                    elementAndFlagArrays[element + '_sflag'].append(line[52:53])

                    # VALUE5
                    elementAndFlagArrays[element].append(line[53:58])
                    elementAndFlagArrays[element + '_mflag'].append(line[58:59])
                    elementAndFlagArrays[element + '_qflag'].append(line[59:60])
                    elementAndFlagArrays[element + '_sflag'].append(line[60:61])

                    # VALUE6
                    elementAndFlagArrays[element].append(line[61:66])
                    elementAndFlagArrays[element + '_mflag'].append(line[66:67])
                    elementAndFlagArrays[element + '_qflag'].append(line[67:68])
                    elementAndFlagArrays[element + '_sflag'].append(line[68:69])

                    # VALUE7
                    elementAndFlagArrays[element].append(line[69:74])
                    elementAndFlagArrays[element + '_mflag'].append(line[74:75])
                    elementAndFlagArrays[element + '_qflag'].append(line[75:76])
                    elementAndFlagArrays[element + '_sflag'].append(line[76:77])

                    # VALUE8
                    elementAndFlagArrays[element].append(line[77:82])
                    elementAndFlagArrays[element + '_mflag'].append(line[82:83])
                    elementAndFlagArrays[element + '_qflag'].append(line[83:84])
                    elementAndFlagArrays[element + '_sflag'].append(line[84:85])

                    # VALUE9
                    elementAndFlagArrays[element].append(line[85:90])
                    elementAndFlagArrays[element + '_mflag'].append(line[90:91])
                    elementAndFlagArrays[element + '_qflag'].append(line[91:92])
                    elementAndFlagArrays[element + '_sflag'].append(line[92:93])

                    # VALUE10
                    elementAndFlagArrays[element].append(line[93:98])
                    elementAndFlagArrays[element + '_mflag'].append(line[98:99])
                    elementAndFlagArrays[element + '_qflag'].append(line[99:100])
                    elementAndFlagArrays[element + '_sflag'].append(line[100:101])

                    # VALUE11
                    elementAndFlagArrays[element].append(line[101:106])
                    elementAndFlagArrays[element + '_mflag'].append(line[106:107])
                    elementAndFlagArrays[element + '_qflag'].append(line[107:108])
                    elementAndFlagArrays[element + '_sflag'].append(line[108:109])

                    # VALUE12
                    elementAndFlagArrays[element].append(line[109:114])
                    elementAndFlagArrays[element + '_mflag'].append(line[114:115])
                    elementAndFlagArrays[element + '_qflag'].append(line[115:116])
                    elementAndFlagArrays[element + '_sflag'].append(line[116:117])

                    # VALUE13
                    elementAndFlagArrays[element].append(line[117:122])
                    elementAndFlagArrays[element + '_mflag'].append(line[122:123])
                    elementAndFlagArrays[element + '_qflag'].append(line[123:124])
                    elementAndFlagArrays[element + '_sflag'].append(line[124:125])

                    # VALUE14
                    elementAndFlagArrays[element].append(line[125:130])
                    elementAndFlagArrays[element + '_mflag'].append(line[130:131])
                    elementAndFlagArrays[element + '_qflag'].append(line[131:132])
                    elementAndFlagArrays[element + '_sflag'].append(line[132:133])

                    # VALUE15
                    elementAndFlagArrays[element].append(line[133:138])
                    elementAndFlagArrays[element + '_mflag'].append(line[138:139])
                    elementAndFlagArrays[element + '_qflag'].append(line[139:140])
                    elementAndFlagArrays[element + '_sflag'].append(line[140:141])

                    # VALUE16
                    elementAndFlagArrays[element].append(line[141:146])
                    elementAndFlagArrays[element + '_mflag'].append(line[146:147])
                    elementAndFlagArrays[element + '_qflag'].append(line[147:148])
                    elementAndFlagArrays[element + '_sflag'].append(line[148:149])

                    # VALUE17
                    elementAndFlagArrays[element].append(line[149:154])
                    elementAndFlagArrays[element + '_mflag'].append(line[154:155])
                    elementAndFlagArrays[element + '_qflag'].append(line[155:156])
                    elementAndFlagArrays[element + '_sflag'].append(line[156:157])

                    # VALUE18
                    elementAndFlagArrays[element].append(line[157:162])
                    elementAndFlagArrays[element + '_mflag'].append(line[162:163])
                    elementAndFlagArrays[element + '_qflag'].append(line[163:164])
                    elementAndFlagArrays[element + '_sflag'].append(line[164:165])

                    # VALUE19
                    elementAndFlagArrays[element].append(line[165:170])
                    elementAndFlagArrays[element + '_mflag'].append(line[170:171])
                    elementAndFlagArrays[element + '_qflag'].append(line[171:172])
                    elementAndFlagArrays[element + '_sflag'].append(line[172:173])

                    # VALUE20
                    elementAndFlagArrays[element].append(line[173:178])
                    elementAndFlagArrays[element + '_mflag'].append(line[178:179])
                    elementAndFlagArrays[element + '_qflag'].append(line[179:180])
                    elementAndFlagArrays[element + '_sflag'].append(line[180:181])

                    # VALUE21
                    elementAndFlagArrays[element].append(line[181:186])
                    elementAndFlagArrays[element + '_mflag'].append(line[186:187])
                    elementAndFlagArrays[element + '_qflag'].append(line[187:188])
                    elementAndFlagArrays[element + '_sflag'].append(line[188:189])

                    # VALUE22
                    elementAndFlagArrays[element].append(line[189:194])
                    elementAndFlagArrays[element + '_mflag'].append(line[194:195])
                    elementAndFlagArrays[element + '_qflag'].append(line[195:196])
                    elementAndFlagArrays[element + '_sflag'].append(line[196:197])

                    # VALUE23
                    elementAndFlagArrays[element].append(line[197:202])
                    elementAndFlagArrays[element + '_mflag'].append(line[202:203])
                    elementAndFlagArrays[element + '_qflag'].append(line[203:204])
                    elementAndFlagArrays[element + '_sflag'].append(line[204:205])

                    # VALUE24
                    elementAndFlagArrays[element].append(line[205:210])
                    elementAndFlagArrays[element + '_mflag'].append(line[210:211])
                    elementAndFlagArrays[element + '_qflag'].append(line[211:212])
                    elementAndFlagArrays[element + '_sflag'].append(line[212:213])

                    # VALUE25
                    elementAndFlagArrays[element].append(line[213:218])
                    elementAndFlagArrays[element + '_mflag'].append(line[218:219])
                    elementAndFlagArrays[element + '_qflag'].append(line[219:220])
                    elementAndFlagArrays[element + '_sflag'].append(line[220:221])

                    # VALUE26
                    elementAndFlagArrays[element].append(line[221:226])
                    elementAndFlagArrays[element + '_mflag'].append(line[226:227])
                    elementAndFlagArrays[element + '_qflag'].append(line[227:228])
                    elementAndFlagArrays[element + '_sflag'].append(line[228:229])

                    # VALUE27
                    elementAndFlagArrays[element].append(line[229:234])
                    elementAndFlagArrays[element + '_mflag'].append(line[234:235])
                    elementAndFlagArrays[element + '_qflag'].append(line[235:236])
                    elementAndFlagArrays[element + '_sflag'].append(line[236:237])

                    # VALUE28
                    elementAndFlagArrays[element].append(line[237:242])
                    elementAndFlagArrays[element + '_mflag'].append(line[242:243])
                    elementAndFlagArrays[element + '_qflag'].append(line[243:244])
                    elementAndFlagArrays[element + '_sflag'].append(line[244:245])

                    # VALUE29
                    elementAndFlagArrays[element].append(line[245:250])
                    elementAndFlagArrays[element + '_mflag'].append(line[250:251])
                    elementAndFlagArrays[element + '_qflag'].append(line[251:252])
                    elementAndFlagArrays[element + '_sflag'].append(line[252:253])

                    # VALUE30
                    elementAndFlagArrays[element].append(line[253:258])
                    elementAndFlagArrays[element + '_mflag'].append(line[258:259])
                    elementAndFlagArrays[element + '_qflag'].append(line[259:260])
                    elementAndFlagArrays[element + '_sflag'].append(line[260:261])

                    # VALUE31
                    elementAndFlagArrays[element].append(line[261:266])
                    elementAndFlagArrays[element + '_mflag'].append(line[266:267])
                    elementAndFlagArrays[element + '_qflag'].append(line[267:268])
                    elementAndFlagArrays[element + '_sflag'].append(line[268:269])

            return elementAndFlagArrays
        
        except KeyboardInterrupt:
            print(sys.exc_info()[0])
        except:
            logging.exception(sys.exc_info()[0])
        finally:
            pass
    # End create_elements_flags_data_lists(self, fileId)

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
    ghcn.create_elements_flags_data_lists(testfile)
    ghcn.parse_to_netCDF(testfile)

    print('The program took ', (time.time()-start), 'seconds to complete.')
                
# End __main__
