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
    '''thomas.jaensch@noaa.gov'''

    def __init__(self):
        # Lists and dictionaries with information from https://www1.ncdc.noaa.gov/pub/data/ghcn/daily/ghcnd-stations.txt to be used in netCDF variables derived with def get_stationInfo
        self.stationIds = []
        self.latDict = {}
        self.lonDict = {}
        self.stationLongNameDict = {}

    def get_stationInfo(self):
        data = urllib2.urlopen("https://www1.ncdc.noaa.gov/pub/data/ghcn/daily/ghcnd-stations.txt")
        for line in data:
            if not line:
                break
            # Get station IDs as substrings from each line in source file, etc.
            self.stationIds.append(line[0:11])
            self.latDict[line[0:11]] = line[12:20]
            self.lonDict[line[0:11]] = line[21:30]
            self.stationLongNameDict[line[0:11]] = line[38:71]
        print(self.stationLongNameDict)
        #print(len(self.stationIds))
        return self.stationIds

    def download_dly_file(self, fileId):
        try:
            url = 'https://www1.ncdc.noaa.gov/pub/data/ghcn/daily/all/%s.dly' %fileId
            urllib.urlretrieve(url, 'dly_data_as_txt/' + fileId + '.txt')
        except:
            logging.exception(fileId + ": ")
        finally:
            pass

    def parse_to_netCDF(self, fileId):
        print(fileId)
        try:
            # Empty lists for variables, more information here ftp://ftp.ncdc.noaa.gov/pub/data/ghcn/daily/readme.txt
            ID = []
            YEAR = []
            MONTH = []
            ELEMENT = []
            # 4 lists for each day of the month 1-31
            VALUE1 = []; MFLAG1 = []; QFLAG1 = []; SFLAG1 = [];
            VALUE2 = []; MFLAG2 = []; QFLAG2 = []; SFLAG2 = [];
            VALUE3 = []; MFLAG3 = []; QFLAG3 = []; SFLAG3 = [];
            VALUE4 = []; MFLAG4 = []; QFLAG4 = []; SFLAG4 = [];
            VALUE5 = []; MFLAG5 = []; QFLAG5 = []; SFLAG5 = [];
            VALUE6 = []; MFLAG6 = []; QFLAG6 = []; SFLAG6 = [];
            VALUE7 = []; MFLAG7 = []; QFLAG7 = []; SFLAG7 = [];
            VALUE8 = []; MFLAG8 = []; QFLAG8 = []; SFLAG8 = [];
            VALUE9 = []; MFLAG9 = []; QFLAG9 = []; SFLAG9 = [];
            VALUE10 = []; MFLAG10 = []; QFLAG10 = []; SFLAG10 = [];
            VALUE11 = []; MFLAG11 = []; QFLAG11 = []; SFLAG11 = [];
            VALUE12 = []; MFLAG12 = []; QFLAG12 = []; SFLAG12 = [];
            VALUE13 = []; MFLAG13 = []; QFLAG13 = []; SFLAG13 = [];
            VALUE14 = []; MFLAG14 = []; QFLAG14 = []; SFLAG14 = [];
            VALUE15 = []; MFLAG15 = []; QFLAG15 = []; SFLAG15 = [];
            VALUE16 = []; MFLAG16 = []; QFLAG16 = []; SFLAG16 = [];
            VALUE17 = []; MFLAG17 = []; QFLAG17 = []; SFLAG17 = [];
            VALUE18 = []; MFLAG18 = []; QFLAG18 = []; SFLAG18 = [];
            VALUE19 = []; MFLAG19 = []; QFLAG19 = []; SFLAG19 = [];
            VALUE20 = []; MFLAG20 = []; QFLAG20 = []; SFLAG20 = [];
            VALUE21 = []; MFLAG21 = []; QFLAG21 = []; SFLAG21 = [];
            VALUE22 = []; MFLAG22 = []; QFLAG22 = []; SFLAG22 = [];
            VALUE23 = []; MFLAG23 = []; QFLAG23 = []; SFLAG23 = [];
            VALUE24 = []; MFLAG24 = []; QFLAG24 = []; SFLAG24 = [];
            VALUE25 = []; MFLAG25 = []; QFLAG25 = []; SFLAG25 = [];
            VALUE26 = []; MFLAG26 = []; QFLAG26 = []; SFLAG26 = [];
            VALUE27 = []; MFLAG27 = []; QFLAG27 = []; SFLAG27 = [];
            VALUE28 = []; MFLAG28 = []; QFLAG28 = []; SFLAG28 = [];
            VALUE29 = []; MFLAG29 = []; QFLAG29 = []; SFLAG29 = [];
            VALUE30 = []; MFLAG30 = []; QFLAG30 = []; SFLAG30 = [];
            VALUE31 = []; MFLAG31 = []; QFLAG31 = []; SFLAG31 = [];
            with open ("./dly_data_as_txt/" + fileId + ".txt", "r") as file:
                for line in file:
                    ID.append(line[0:11])
                    YEAR.append(line[11:15])
                    MONTH.append(line[15:17])
                    ELEMENT.append(line[17:21])
                    VALUE1.append(line[21:26]); MFLAG1.append(line[26:27]); QFLAG1.append(line[27:28]); SFLAG1.append(line[28:29])
                    VALUE2.append(line[29:34]); MFLAG2.append(line[34:35]); QFLAG2.append(line[35:36]); SFLAG2.append(line[36:37])
                    VALUE3.append(line[37:42]); MFLAG3.append(line[42:43]); QFLAG3.append(line[43:44]); SFLAG3.append(line[44:45])
                    VALUE4.append(line[45:50]); MFLAG4.append(line[50:51]); QFLAG4.append(line[51:52]); SFLAG4.append(line[52:53])
                    VALUE5.append(line[53:58]); MFLAG5.append(line[58:59]); QFLAG5.append(line[59:60]); SFLAG5.append(line[60:61])
                    VALUE6.append(line[61:66]); MFLAG6.append(line[66:67]); QFLAG6.append(line[67:68]); SFLAG6.append(line[68:69])
                    VALUE7.append(line[69:74]); MFLAG7.append(line[74:75]); QFLAG7.append(line[75:76]); SFLAG7.append(line[76:77])
                    VALUE8.append(line[77:82]); MFLAG8.append(line[82:83]); QFLAG8.append(line[83:84]); SFLAG8.append(line[84:85])
                    VALUE9.append(line[85:90]); MFLAG9.append(line[90:91]); QFLAG9.append(line[91:92]); SFLAG9.append(line[92:93])
                    VALUE10.append(line[93:98]); MFLAG10.append(line[98:99]); QFLAG10.append(line[99:100]); SFLAG10.append(line[100:101])
                    VALUE11.append(line[101:106]); MFLAG11.append(line[106:107]); QFLAG11.append(line[107:108]); SFLAG11.append(line[108:109])
                    VALUE12.append(line[109:114]); MFLAG12.append(line[114:115]); QFLAG12.append(line[115:116]); SFLAG12.append(line[116:117])
                    VALUE13.append(line[117:122]); MFLAG13.append(line[122:123]); QFLAG13.append(line[123:124]); SFLAG13.append(line[124:125])
                    VALUE14.append(line[125:130]); MFLAG14.append(line[130:131]); QFLAG14.append(line[131:132]); SFLAG14.append(line[132:133])
                    VALUE15.append(line[133:138]); MFLAG15.append(line[138:139]); QFLAG15.append(line[139:140]); SFLAG15.append(line[140:141])
                    VALUE16.append(line[141:146]); MFLAG16.append(line[146:147]); QFLAG16.append(line[147:148]); SFLAG16.append(line[148:149])
                    VALUE17.append(line[149:154]); MFLAG17.append(line[154:155]); QFLAG17.append(line[155:156]); SFLAG17.append(line[156:157])
                    VALUE18.append(line[157:162]); MFLAG18.append(line[162:163]); QFLAG18.append(line[163:164]); SFLAG18.append(line[164:165])
                    VALUE19.append(line[165:170]); MFLAG19.append(line[170:171]); QFLAG19.append(line[171:172]); SFLAG19.append(line[172:173])
                    VALUE20.append(line[173:178]); MFLAG20.append(line[178:179]); QFLAG20.append(line[179:180]); SFLAG20.append(line[180:181])
                    VALUE21.append(line[181:186]); MFLAG21.append(line[186:187]); QFLAG21.append(line[187:188]); SFLAG21.append(line[188:189])
                    VALUE22.append(line[189:194]); MFLAG22.append(line[194:195]); QFLAG22.append(line[195:196]); SFLAG22.append(line[196:197])
                    VALUE23.append(line[197:202]); MFLAG23.append(line[202:203]); QFLAG23.append(line[203:204]); SFLAG23.append(line[204:205])
                    VALUE24.append(line[205:210]); MFLAG24.append(line[210:211]); QFLAG24.append(line[211:212]); SFLAG24.append(line[212:213])
                    VALUE25.append(line[213:218]); MFLAG25.append(line[218:219]); QFLAG25.append(line[219:220]); SFLAG25.append(line[220:221])
                    VALUE26.append(line[221:226]); MFLAG26.append(line[226:227]); QFLAG26.append(line[227:228]); SFLAG26.append(line[228:229])
                    VALUE27.append(line[229:234]); MFLAG27.append(line[234:235]); QFLAG27.append(line[235:236]); SFLAG27.append(line[236:237])
                    VALUE28.append(line[237:242]); MFLAG28.append(line[242:243]); QFLAG28.append(line[243:244]); SFLAG28.append(line[244:245])
                    VALUE29.append(line[245:250]); MFLAG29.append(line[250:251]); QFLAG29.append(line[251:252]); SFLAG29.append(line[252:253])
                    VALUE30.append(line[253:258]); MFLAG30.append(line[258:259]); QFLAG30.append(line[259:260]); SFLAG30.append(line[260:261])
                    VALUE31.append(line[261:266]); MFLAG31.append(line[266:267]); QFLAG31.append(line[267:268]); SFLAG31.append(line[268:269]) 

            # Create netcdf data object
            with netCDF4.Dataset('./netcdf/%s.nc' %fileId, mode="w", format='NETCDF4') as ds:
                # Define dimensions
                ds.createDimension('time')
                ds.createDimension('station', 1)

                # File-level metadata attributes
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

                # Variable definitions

                ELEMENT = np.array(ELEMENT)
                station_ELEMENT = ds.createVariable('ELEMENT', ELEMENT.dtype, ('time',))
                station_ELEMENT[:] = ELEMENT[:]
                
                VALUE1 = np.array(VALUE1)
                station_VALUE1 = ds.createVariable('VALUE1', VALUE1.dtype, ('time',))
                station_VALUE1[:] = VALUE1[:]
                
                MFLAG1 = np.array(MFLAG1)
                station_MFLAG1 = ds.createVariable('MFLAG1', MFLAG1.dtype, ('time',))
                station_MFLAG1[:] = MFLAG1[:]
                
                QFLAG1 = np.array(QFLAG1)
                station_QFLAG1 = ds.createVariable('QFLAG1', QFLAG1.dtype, ('time',))
                station_QFLAG1[:] = QFLAG1[:]
                
                SFLAG1 = np.array(SFLAG1)
                station_SFLAG1 = ds.createVariable('SFLAG1', SFLAG1.dtype, ('time',))
                station_SFLAG1[:] = SFLAG1[:]

                station_name = ds.createVariable('station_name', 'string', ('time',))
                station_name[:] = np.array(ID[:])
                station_name.long_name = self.stationLongNameDict[fileId]
                
                # Write dataset to file
                print ds
        except:
            logging.exception(fileId + ": ")
        finally:
            pass
    # End def parse_to_netCDF(self, fileId)

    def run_combined_defs(self, fileId):
            self.download_dly_file(fileId)
            self.parse_to_netCDF(fileId)

    def go(self):
            p = Pool(5)
            p.map(self, self.get_stationInfo())

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
