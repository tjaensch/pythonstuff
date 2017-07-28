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
                # File-level metadata attributes
                ds.Conventions = "CF-1.6" 
                ds.title = 'TBA'
                ds.institution = 'TBA'
                ds.source = 'TBA'
                ds.history = 'TBA'
                ds.references = 'TBA'
                ds.comment = 'TBA'

                # Define ID dimension
                ID = np.array(ID)
                timeSeriesProfile = ds.createDimension('station_ID', ID.shape[0])
                # Variable definitions
                station_ID = ds.createVariable('station_ID', ID.dtype, ('station_ID',))
                station_ID[:] = ID[:]
                # Add attributes
                #station_ID.units = 'the_proper_unit_string'
                #station_ID.long_name = 'long name that describes the data'
                #station_ID.standard_name = 'CF_standard_name'

                # Define YEAR dimension
                YEAR = np.array(YEAR)
                timeSeriesProfile = ds.createDimension('station_YEAR', YEAR.shape[0])
                # Variable definitions
                station_YEAR = ds.createVariable('station_YEAR', YEAR.dtype, ('station_YEAR',))
                station_YEAR[:] = YEAR[:]

                # Define MONTH dimension
                MONTH = np.array(MONTH)
                timeSeriesProfile = ds.createDimension('station_MONTH', MONTH.shape[0])
                # Variable definitions
                station_MONTH = ds.createVariable('station_MONTH', MONTH.dtype, ('station_MONTH',))
                station_MONTH[:] = MONTH[:]

                # Define ELEMENT dimension
                ELEMENT = np.array(ELEMENT)
                timeSeriesProfile = ds.createDimension('station_ELEMENT', ELEMENT.shape[0])
                # Variable definitions
                station_ELEMENT = ds.createVariable('station_ELEMENT', ELEMENT.dtype, ('station_ELEMENT',))
                station_ELEMENT[:] = ELEMENT[:]

                # Define VALUE1 dimension
                VALUE1 = np.array(VALUE1)
                timeSeriesProfile = ds.createDimension('station_VALUE1', VALUE1.shape[0])
                # Variable definitions
                station_VALUE1 = ds.createVariable('station_VALUE1', VALUE1.dtype, ('station_VALUE1',))
                station_VALUE1[:] = VALUE1[:]

                # Define VALUE2 dimension
                VALUE2 = np.array(VALUE2)
                timeSeriesProfile = ds.createDimension('station_VALUE2', VALUE2.shape[0])
                # Variable definitions
                station_VALUE2 = ds.createVariable('station_VALUE2', VALUE2.dtype, ('station_VALUE2',))
                station_VALUE2[:] = VALUE2[:]

                # Define VALUE3 dimension
                VALUE3 = np.array(VALUE3)
                timeSeriesProfile = ds.createDimension('station_VALUE3', VALUE3.shape[0])
                # Variable definitions
                station_VALUE3 = ds.createVariable('station_VALUE3', VALUE3.dtype, ('station_VALUE3',))
                station_VALUE3[:] = VALUE3[:]

                # Define VALUE4 dimension
                VALUE4 = np.array(VALUE4)
                timeSeriesProfile = ds.createDimension('station_VALUE4', VALUE4.shape[0])
                # Variable definitions
                station_VALUE4 = ds.createVariable('station_VALUE4', VALUE4.dtype, ('station_VALUE4',))
                station_VALUE4[:] = VALUE4[:]

                # Define VALUE5 dimension
                VALUE5 = np.array(VALUE5)
                timeSeriesProfile = ds.createDimension('station_VALUE5', VALUE5.shape[0])
                # Variable definitions
                station_VALUE5 = ds.createVariable('station_VALUE5', VALUE5.dtype, ('station_VALUE5',))
                station_VALUE5[:] = VALUE5[:]

                # Define VALUE6 dimension
                VALUE6 = np.array(VALUE6)
                timeSeriesProfile = ds.createDimension('station_VALUE6', VALUE6.shape[0])
                # Variable definitions
                station_VALUE6 = ds.createVariable('station_VALUE6', VALUE6.dtype, ('station_VALUE6',))
                station_VALUE6[:] = VALUE6[:]

                # Define VALUE7 dimension
                VALUE7 = np.array(VALUE7)
                timeSeriesProfile = ds.createDimension('station_VALUE7', VALUE7.shape[0])
                # Variable definitions
                station_VALUE7 = ds.createVariable('station_VALUE7', VALUE7.dtype, ('station_VALUE7',))
                station_VALUE7[:] = VALUE7[:]

                # Define VALUE8 dimension
                VALUE8 = np.array(VALUE8)
                timeSeriesProfile = ds.createDimension('station_VALUE8', VALUE8.shape[0])
                # Variable definitions
                station_VALUE8 = ds.createVariable('station_VALUE8', VALUE8.dtype, ('station_VALUE8',))
                station_VALUE8[:] = VALUE8[:]

                # Define VALUE9 dimension
                VALUE9 = np.array(VALUE9)
                timeSeriesProfile = ds.createDimension('station_VALUE9', VALUE9.shape[0])
                # Variable definitions
                station_VALUE9 = ds.createVariable('station_VALUE9', VALUE9.dtype, ('station_VALUE9',))
                station_VALUE9[:] = VALUE9[:]

                # Define VALUE10 dimension
                VALUE10 = np.array(VALUE10)
                timeSeriesProfile = ds.createDimension('station_VALUE10', VALUE10.shape[0])
                # Variable definitions
                station_VALUE10 = ds.createVariable('station_VALUE10', VALUE10.dtype, ('station_VALUE10',))
                station_VALUE10[:] = VALUE10[:]

                # Define VALUE11 dimension
                VALUE11 = np.array(VALUE11)
                timeSeriesProfile = ds.createDimension('station_VALUE11', VALUE11.shape[0])
                # Variable definitions
                station_VALUE11 = ds.createVariable('station_VALUE11', VALUE11.dtype, ('station_VALUE11',))
                station_VALUE11[:] = VALUE11[:]

                # Define VALUE12 dimension
                VALUE12 = np.array(VALUE12)
                timeSeriesProfile = ds.createDimension('station_VALUE12', VALUE12.shape[0])
                # Variable definitions
                station_VALUE12 = ds.createVariable('station_VALUE12', VALUE12.dtype, ('station_VALUE12',))
                station_VALUE12[:] = VALUE12[:]

                # Define VALUE13 dimension
                VALUE13 = np.array(VALUE13)
                timeSeriesProfile = ds.createDimension('station_VALUE13', VALUE13.shape[0])
                # Variable definitions
                station_VALUE13 = ds.createVariable('station_VALUE13', VALUE13.dtype, ('station_VALUE13',))
                station_VALUE13[:] = VALUE13[:]

                # Define VALUE14 dimension
                VALUE14 = np.array(VALUE14)
                timeSeriesProfile = ds.createDimension('station_VALUE14', VALUE14.shape[0])
                # Variable definitions
                station_VALUE14 = ds.createVariable('station_VALUE14', VALUE14.dtype, ('station_VALUE14',))
                station_VALUE14[:] = VALUE14[:]

                # Define VALUE15 dimension
                VALUE15 = np.array(VALUE15)
                timeSeriesProfile = ds.createDimension('station_VALUE15', VALUE15.shape[0])
                # Variable definitions
                station_VALUE15 = ds.createVariable('station_VALUE15', VALUE15.dtype, ('station_VALUE15',))
                station_VALUE15[:] = VALUE15[:]

                # Define VALUE16 dimension
                VALUE16 = np.array(VALUE16)
                timeSeriesProfile = ds.createDimension('station_VALUE16', VALUE16.shape[0])
                # Variable definitions
                station_VALUE16 = ds.createVariable('station_VALUE16', VALUE16.dtype, ('station_VALUE16',))
                station_VALUE16[:] = VALUE16[:]

                # Define VALUE17 dimension
                VALUE17 = np.array(VALUE17)
                timeSeriesProfile = ds.createDimension('station_VALUE17', VALUE17.shape[0])
                # Variable definitions
                station_VALUE17 = ds.createVariable('station_VALUE17', VALUE17.dtype, ('station_VALUE17',))
                station_VALUE17[:] = VALUE17[:]

                # Define VALUE18 dimension
                VALUE18 = np.array(VALUE18)
                timeSeriesProfile = ds.createDimension('station_VALUE18', VALUE18.shape[0])
                # Variable definitions
                station_VALUE18 = ds.createVariable('station_VALUE18', VALUE18.dtype, ('station_VALUE18',))
                station_VALUE18[:] = VALUE18[:]

                # Define VALUE19 dimension
                VALUE19 = np.array(VALUE19)
                timeSeriesProfile = ds.createDimension('station_VALUE19', VALUE19.shape[0])
                # Variable definitions
                station_VALUE19 = ds.createVariable('station_VALUE19', VALUE19.dtype, ('station_VALUE19',))
                station_VALUE19[:] = VALUE19[:]

                # Define VALUE20 dimension
                VALUE20 = np.array(VALUE20)
                timeSeriesProfile = ds.createDimension('station_VALUE20', VALUE20.shape[0])
                # Variable definitions
                station_VALUE20 = ds.createVariable('station_VALUE20', VALUE20.dtype, ('station_VALUE20',))
                station_VALUE20[:] = VALUE20[:]

                # Define VALUE21 dimension
                VALUE21 = np.array(VALUE21)
                timeSeriesProfile = ds.createDimension('station_VALUE21', VALUE21.shape[0])
                # Variable definitions
                station_VALUE21 = ds.createVariable('station_VALUE21', VALUE21.dtype, ('station_VALUE21',))
                station_VALUE21[:] = VALUE21[:]

                # Define VALUE22 dimension
                VALUE22 = np.array(VALUE22)
                timeSeriesProfile = ds.createDimension('station_VALUE22', VALUE22.shape[0])
                # Variable definitions
                station_VALUE22 = ds.createVariable('station_VALUE22', VALUE22.dtype, ('station_VALUE22',))
                station_VALUE22[:] = VALUE22[:]

                # Define VALUE23 dimension
                VALUE23 = np.array(VALUE23)
                timeSeriesProfile = ds.createDimension('station_VALUE23', VALUE23.shape[0])
                # Variable definitions
                station_VALUE23 = ds.createVariable('station_VALUE23', VALUE23.dtype, ('station_VALUE23',))
                station_VALUE23[:] = VALUE23[:]

                # Define VALUE24 dimension
                VALUE24 = np.array(VALUE24)
                timeSeriesProfile = ds.createDimension('station_VALUE24', VALUE24.shape[0])
                # Variable definitions
                station_VALUE24 = ds.createVariable('station_VALUE24', VALUE24.dtype, ('station_VALUE24',))
                station_VALUE24[:] = VALUE24[:]

                # Define VALUE25 dimension
                VALUE25 = np.array(VALUE25)
                timeSeriesProfile = ds.createDimension('station_VALUE25', VALUE25.shape[0])
                # Variable definitions
                station_VALUE25 = ds.createVariable('station_VALUE25', VALUE25.dtype, ('station_VALUE25',))
                station_VALUE25[:] = VALUE25[:]

                # Define VALUE26 dimension
                VALUE26 = np.array(VALUE26)
                timeSeriesProfile = ds.createDimension('station_VALUE26', VALUE26.shape[0])
                # Variable definitions
                station_VALUE26 = ds.createVariable('station_VALUE26', VALUE26.dtype, ('station_VALUE26',))
                station_VALUE26[:] = VALUE26[:]

                # Define VALUE27 dimension
                VALUE27 = np.array(VALUE27)
                timeSeriesProfile = ds.createDimension('station_VALUE27', VALUE27.shape[0])
                # Variable definitions
                station_VALUE27 = ds.createVariable('station_VALUE27', VALUE27.dtype, ('station_VALUE27',))
                station_VALUE27[:] = VALUE27[:]

                # Define VALUE28 dimension
                VALUE28 = np.array(VALUE28)
                timeSeriesProfile = ds.createDimension('station_VALUE28', VALUE28.shape[0])
                # Variable definitions
                station_VALUE28 = ds.createVariable('station_VALUE28', VALUE28.dtype, ('station_VALUE28',))
                station_VALUE28[:] = VALUE28[:]

                # Define VALUE29 dimension
                VALUE29 = np.array(VALUE29)
                timeSeriesProfile = ds.createDimension('station_VALUE29', VALUE29.shape[0])
                # Variable definitions
                station_VALUE29 = ds.createVariable('station_VALUE29', VALUE29.dtype, ('station_VALUE29',))
                station_VALUE29[:] = VALUE29[:]

                # Define VALUE30 dimension
                VALUE30 = np.array(VALUE30)
                timeSeriesProfile = ds.createDimension('station_VALUE30', VALUE30.shape[0])
                # Variable definitions
                station_VALUE30 = ds.createVariable('station_VALUE30', VALUE30.dtype, ('station_VALUE30',))
                station_VALUE30[:] = VALUE30[:]

                # Define VALUE31 dimension
                VALUE31 = np.array(VALUE31)
                timeSeriesProfile = ds.createDimension('station_VALUE31', VALUE31.shape[0])
                # Variable definitions
                station_VALUE31 = ds.createVariable('station_VALUE31', VALUE31.dtype, ('station_VALUE31',))
                station_VALUE31[:] = VALUE31[:]

                # Define MFLAG1 dimension
                MFLAG1 = np.array(MFLAG1)
                timeSeriesProfile = ds.createDimension('station_MFLAG1', MFLAG1.shape[0])
                # Variable definitions
                station_MFLAG1 = ds.createVariable('station_MFLAG1', MFLAG1.dtype, ('station_MFLAG1',))
                station_MFLAG1[:] = MFLAG1[:]

                # Define MFLAG2 dimension
                MFLAG2 = np.array(MFLAG2)
                timeSeriesProfile = ds.createDimension('station_MFLAG2', MFLAG2.shape[0])
                # Variable definitions
                station_MFLAG2 = ds.createVariable('station_MFLAG2', MFLAG2.dtype, ('station_MFLAG2',))
                station_MFLAG2[:] = MFLAG2[:]

                # Define MFLAG3 dimension
                MFLAG3 = np.array(MFLAG3)
                timeSeriesProfile = ds.createDimension('station_MFLAG3', MFLAG3.shape[0])
                # Variable definitions
                station_MFLAG3 = ds.createVariable('station_MFLAG3', MFLAG3.dtype, ('station_MFLAG3',))
                station_MFLAG3[:] = MFLAG3[:]

                # Define MFLAG4 dimension
                MFLAG4 = np.array(MFLAG4)
                timeSeriesProfile = ds.createDimension('station_MFLAG4', MFLAG4.shape[0])
                # Variable definitions
                station_MFLAG4 = ds.createVariable('station_MFLAG4', MFLAG4.dtype, ('station_MFLAG4',))
                station_MFLAG4[:] = MFLAG4[:]

                # Define MFLAG5 dimension
                MFLAG5 = np.array(MFLAG5)
                timeSeriesProfile = ds.createDimension('station_MFLAG5', MFLAG5.shape[0])
                # Variable definitions
                station_MFLAG5 = ds.createVariable('station_MFLAG5', MFLAG5.dtype, ('station_MFLAG5',))
                station_MFLAG5[:] = MFLAG5[:]

                # Define MFLAG6 dimension
                MFLAG6 = np.array(MFLAG6)
                timeSeriesProfile = ds.createDimension('station_MFLAG6', MFLAG6.shape[0])
                # Variable definitions
                station_MFLAG6 = ds.createVariable('station_MFLAG6', MFLAG6.dtype, ('station_MFLAG6',))
                station_MFLAG6[:] = MFLAG6[:]

                # Define MFLAG7 dimension
                MFLAG7 = np.array(MFLAG7)
                timeSeriesProfile = ds.createDimension('station_MFLAG7', MFLAG7.shape[0])
                # Variable definitions
                station_MFLAG7 = ds.createVariable('station_MFLAG7', MFLAG7.dtype, ('station_MFLAG7',))
                station_MFLAG7[:] = MFLAG7[:]

                # Define MFLAG8 dimension
                MFLAG8 = np.array(MFLAG8)
                timeSeriesProfile = ds.createDimension('station_MFLAG8', MFLAG8.shape[0])
                # Variable definitions
                station_MFLAG8 = ds.createVariable('station_MFLAG8', MFLAG8.dtype, ('station_MFLAG8',))
                station_MFLAG8[:] = MFLAG8[:]

                # Define MFLAG9 dimension
                MFLAG9 = np.array(MFLAG9)
                timeSeriesProfile = ds.createDimension('station_MFLAG9', MFLAG9.shape[0])
                # Variable definitions
                station_MFLAG9 = ds.createVariable('station_MFLAG9', MFLAG9.dtype, ('station_MFLAG9',))
                station_MFLAG9[:] = MFLAG9[:]

                # Define MFLAG10 dimension
                MFLAG10 = np.array(MFLAG10)
                timeSeriesProfile = ds.createDimension('station_MFLAG10', MFLAG10.shape[0])
                # Variable definitions
                station_MFLAG10 = ds.createVariable('station_MFLAG10', MFLAG10.dtype, ('station_MFLAG10',))
                station_MFLAG10[:] = MFLAG10[:]

                # Define MFLAG11 dimension
                MFLAG11 = np.array(MFLAG11)
                timeSeriesProfile = ds.createDimension('station_MFLAG11', MFLAG11.shape[0])
                # Variable definitions
                station_MFLAG11 = ds.createVariable('station_MFLAG11', MFLAG11.dtype, ('station_MFLAG11',))
                station_MFLAG11[:] = MFLAG11[:]

                # Define MFLAG12 dimension
                MFLAG12 = np.array(MFLAG12)
                timeSeriesProfile = ds.createDimension('station_MFLAG12', MFLAG12.shape[0])
                # Variable definitions
                station_MFLAG12 = ds.createVariable('station_MFLAG12', MFLAG12.dtype, ('station_MFLAG12',))
                station_MFLAG12[:] = MFLAG12[:]

                # Define MFLAG13 dimension
                MFLAG13 = np.array(MFLAG13)
                timeSeriesProfile = ds.createDimension('station_MFLAG13', MFLAG13.shape[0])
                # Variable definitions
                station_MFLAG13 = ds.createVariable('station_MFLAG13', MFLAG13.dtype, ('station_MFLAG13',))
                station_MFLAG13[:] = MFLAG13[:]

                # Define MFLAG14 dimension
                MFLAG14 = np.array(MFLAG14)
                timeSeriesProfile = ds.createDimension('station_MFLAG14', MFLAG14.shape[0])
                # Variable definitions
                station_MFLAG14 = ds.createVariable('station_MFLAG14', MFLAG14.dtype, ('station_MFLAG14',))
                station_MFLAG14[:] = MFLAG14[:]

                # Define MFLAG15 dimension
                MFLAG15 = np.array(MFLAG15)
                timeSeriesProfile = ds.createDimension('station_MFLAG15', MFLAG15.shape[0])
                # Variable definitions
                station_MFLAG15 = ds.createVariable('station_MFLAG15', MFLAG15.dtype, ('station_MFLAG15',))
                station_MFLAG15[:] = MFLAG15[:]

                # Define MFLAG16 dimension
                MFLAG16 = np.array(MFLAG16)
                timeSeriesProfile = ds.createDimension('station_MFLAG16', MFLAG16.shape[0])
                # Variable definitions
                station_MFLAG16 = ds.createVariable('station_MFLAG16', MFLAG16.dtype, ('station_MFLAG16',))
                station_MFLAG16[:] = MFLAG16[:]

                # Define MFLAG17 dimension
                MFLAG17 = np.array(MFLAG17)
                timeSeriesProfile = ds.createDimension('station_MFLAG17', MFLAG17.shape[0])
                # Variable definitions
                station_MFLAG17 = ds.createVariable('station_MFLAG17', MFLAG17.dtype, ('station_MFLAG17',))
                station_MFLAG17[:] = MFLAG17[:]

                # Define MFLAG18 dimension
                MFLAG18 = np.array(MFLAG18)
                timeSeriesProfile = ds.createDimension('station_MFLAG18', MFLAG18.shape[0])
                # Variable definitions
                station_MFLAG18 = ds.createVariable('station_MFLAG18', MFLAG18.dtype, ('station_MFLAG18',))
                station_MFLAG18[:] = MFLAG18[:]

                # Define MFLAG19 dimension
                MFLAG19 = np.array(MFLAG19)
                timeSeriesProfile = ds.createDimension('station_MFLAG19', MFLAG19.shape[0])
                # Variable definitions
                station_MFLAG19 = ds.createVariable('station_MFLAG19', MFLAG19.dtype, ('station_MFLAG19',))
                station_MFLAG19[:] = MFLAG19[:]

                # Define MFLAG20 dimension
                MFLAG20 = np.array(MFLAG20)
                timeSeriesProfile = ds.createDimension('station_MFLAG20', MFLAG20.shape[0])
                # Variable definitions
                station_MFLAG20 = ds.createVariable('station_MFLAG20', MFLAG20.dtype, ('station_MFLAG20',))
                station_MFLAG20[:] = MFLAG20[:]

                # Define MFLAG21 dimension
                MFLAG21 = np.array(MFLAG21)
                timeSeriesProfile = ds.createDimension('station_MFLAG21', MFLAG21.shape[0])
                # Variable definitions
                station_MFLAG21 = ds.createVariable('station_MFLAG21', MFLAG21.dtype, ('station_MFLAG21',))
                station_MFLAG21[:] = MFLAG21[:]

                # Define MFLAG22 dimension
                MFLAG22 = np.array(MFLAG22)
                timeSeriesProfile = ds.createDimension('station_MFLAG22', MFLAG22.shape[0])
                # Variable definitions
                station_MFLAG22 = ds.createVariable('station_MFLAG22', MFLAG22.dtype, ('station_MFLAG22',))
                station_MFLAG22[:] = MFLAG22[:]

                # Define MFLAG23 dimension
                MFLAG23 = np.array(MFLAG23)
                timeSeriesProfile = ds.createDimension('station_MFLAG23', MFLAG23.shape[0])
                # Variable definitions
                station_MFLAG23 = ds.createVariable('station_MFLAG23', MFLAG23.dtype, ('station_MFLAG23',))
                station_MFLAG23[:] = MFLAG23[:]

                # Define MFLAG24 dimension
                MFLAG24 = np.array(MFLAG24)
                timeSeriesProfile = ds.createDimension('station_MFLAG24', MFLAG24.shape[0])
                # Variable definitions
                station_MFLAG24 = ds.createVariable('station_MFLAG24', MFLAG24.dtype, ('station_MFLAG24',))
                station_MFLAG24[:] = MFLAG24[:]

                # Define MFLAG25 dimension
                MFLAG25 = np.array(MFLAG25)
                timeSeriesProfile = ds.createDimension('station_MFLAG25', MFLAG25.shape[0])
                # Variable definitions
                station_MFLAG25 = ds.createVariable('station_MFLAG25', MFLAG25.dtype, ('station_MFLAG25',))
                station_MFLAG25[:] = MFLAG25[:]

                # Define MFLAG26 dimension
                MFLAG26 = np.array(MFLAG26)
                timeSeriesProfile = ds.createDimension('station_MFLAG26', MFLAG26.shape[0])
                # Variable definitions
                station_MFLAG26 = ds.createVariable('station_MFLAG26', MFLAG26.dtype, ('station_MFLAG26',))
                station_MFLAG26[:] = MFLAG26[:]

                # Define MFLAG27 dimension
                MFLAG27 = np.array(MFLAG27)
                timeSeriesProfile = ds.createDimension('station_MFLAG27', MFLAG27.shape[0])
                # Variable definitions
                station_MFLAG27 = ds.createVariable('station_MFLAG27', MFLAG27.dtype, ('station_MFLAG27',))
                station_MFLAG27[:] = MFLAG27[:]

                # Define MFLAG28 dimension
                MFLAG28 = np.array(MFLAG28)
                timeSeriesProfile = ds.createDimension('station_MFLAG28', MFLAG28.shape[0])
                # Variable definitions
                station_MFLAG28 = ds.createVariable('station_MFLAG28', MFLAG28.dtype, ('station_MFLAG28',))
                station_MFLAG28[:] = MFLAG28[:]

                # Define MFLAG29 dimension
                MFLAG29 = np.array(MFLAG29)
                timeSeriesProfile = ds.createDimension('station_MFLAG29', MFLAG29.shape[0])
                # Variable definitions
                station_MFLAG29 = ds.createVariable('station_MFLAG29', MFLAG29.dtype, ('station_MFLAG29',))
                station_MFLAG29[:] = MFLAG29[:]

                # Define MFLAG30 dimension
                MFLAG30 = np.array(MFLAG30)
                timeSeriesProfile = ds.createDimension('station_MFLAG30', MFLAG30.shape[0])
                # Variable definitions
                station_MFLAG30 = ds.createVariable('station_MFLAG30', MFLAG30.dtype, ('station_MFLAG30',))
                station_MFLAG30[:] = MFLAG30[:]

                # Define MFLAG31 dimension
                MFLAG31 = np.array(MFLAG31)
                timeSeriesProfile = ds.createDimension('station_MFLAG31', MFLAG31.shape[0])
                # Variable definitions
                station_MFLAG31 = ds.createVariable('station_MFLAG31', MFLAG31.dtype, ('station_MFLAG31',))
                station_MFLAG31[:] = MFLAG31[:]

                # Define QFLAG1 dimension
                QFLAG1 = np.array(QFLAG1)
                timeSeriesProfile = ds.createDimension('station_QFLAG1', QFLAG1.shape[0])
                # Variable definitions
                station_QFLAG1 = ds.createVariable('station_QFLAG1', QFLAG1.dtype, ('station_QFLAG1',))
                station_QFLAG1[:] = QFLAG1[:]

                # Define QFLAG2 dimension
                QFLAG2 = np.array(QFLAG2)
                timeSeriesProfile = ds.createDimension('station_QFLAG2', QFLAG2.shape[0])
                # Variable definitions
                station_QFLAG2 = ds.createVariable('station_QFLAG2', QFLAG2.dtype, ('station_QFLAG2',))
                station_QFLAG2[:] = QFLAG2[:]

                # Define QFLAG3 dimension
                QFLAG3 = np.array(QFLAG3)
                timeSeriesProfile = ds.createDimension('station_QFLAG3', QFLAG3.shape[0])
                # Variable definitions
                station_QFLAG3 = ds.createVariable('station_QFLAG3', QFLAG3.dtype, ('station_QFLAG3',))
                station_QFLAG3[:] = QFLAG3[:]

                # Define QFLAG4 dimension
                QFLAG4 = np.array(QFLAG4)
                timeSeriesProfile = ds.createDimension('station_QFLAG4', QFLAG4.shape[0])
                # Variable definitions
                station_QFLAG4 = ds.createVariable('station_QFLAG4', QFLAG4.dtype, ('station_QFLAG4',))
                station_QFLAG4[:] = QFLAG4[:]

                # Define QFLAG5 dimension
                QFLAG5 = np.array(QFLAG5)
                timeSeriesProfile = ds.createDimension('station_QFLAG5', QFLAG5.shape[0])
                # Variable definitions
                station_QFLAG5 = ds.createVariable('station_QFLAG5', QFLAG5.dtype, ('station_QFLAG5',))
                station_QFLAG5[:] = QFLAG5[:]

                # Define QFLAG6 dimension
                QFLAG6 = np.array(QFLAG6)
                timeSeriesProfile = ds.createDimension('station_QFLAG6', QFLAG6.shape[0])
                # Variable definitions
                station_QFLAG6 = ds.createVariable('station_QFLAG6', QFLAG6.dtype, ('station_QFLAG6',))
                station_QFLAG6[:] = QFLAG6[:]

                # Define QFLAG7 dimension
                QFLAG7 = np.array(QFLAG7)
                timeSeriesProfile = ds.createDimension('station_QFLAG7', QFLAG7.shape[0])
                # Variable definitions
                station_QFLAG7 = ds.createVariable('station_QFLAG7', QFLAG7.dtype, ('station_QFLAG7',))
                station_QFLAG7[:] = QFLAG7[:]

                # Define QFLAG8 dimension
                QFLAG8 = np.array(QFLAG8)
                timeSeriesProfile = ds.createDimension('station_QFLAG8', QFLAG8.shape[0])
                # Variable definitions
                station_QFLAG8 = ds.createVariable('station_QFLAG8', QFLAG8.dtype, ('station_QFLAG8',))
                station_QFLAG8[:] = QFLAG8[:]

                # Define QFLAG9 dimension
                QFLAG9 = np.array(QFLAG9)
                timeSeriesProfile = ds.createDimension('station_QFLAG9', QFLAG9.shape[0])
                # Variable definitions
                station_QFLAG9 = ds.createVariable('station_QFLAG9', QFLAG9.dtype, ('station_QFLAG9',))
                station_QFLAG9[:] = QFLAG9[:]

                # Define QFLAG10 dimension
                QFLAG10 = np.array(QFLAG10)
                timeSeriesProfile = ds.createDimension('station_QFLAG10', QFLAG10.shape[0])
                # Variable definitions
                station_QFLAG10 = ds.createVariable('station_QFLAG10', QFLAG10.dtype, ('station_QFLAG10',))
                station_QFLAG10[:] = QFLAG10[:]

                # Define QFLAG11 dimension
                QFLAG11 = np.array(QFLAG11)
                timeSeriesProfile = ds.createDimension('station_QFLAG11', QFLAG11.shape[0])
                # Variable definitions
                station_QFLAG11 = ds.createVariable('station_QFLAG11', QFLAG11.dtype, ('station_QFLAG11',))
                station_QFLAG11[:] = QFLAG11[:]

                # Define QFLAG12 dimension
                QFLAG12 = np.array(QFLAG12)
                timeSeriesProfile = ds.createDimension('station_QFLAG12', QFLAG12.shape[0])
                # Variable definitions
                station_QFLAG12 = ds.createVariable('station_QFLAG12', QFLAG12.dtype, ('station_QFLAG12',))
                station_QFLAG12[:] = QFLAG12[:]

                # Define QFLAG13 dimension
                QFLAG13 = np.array(QFLAG13)
                timeSeriesProfile = ds.createDimension('station_QFLAG13', QFLAG13.shape[0])
                # Variable definitions
                station_QFLAG13 = ds.createVariable('station_QFLAG13', QFLAG13.dtype, ('station_QFLAG13',))
                station_QFLAG13[:] = QFLAG13[:]

                # Define QFLAG14 dimension
                QFLAG14 = np.array(QFLAG14)
                timeSeriesProfile = ds.createDimension('station_QFLAG14', QFLAG14.shape[0])
                # Variable definitions
                station_QFLAG14 = ds.createVariable('station_QFLAG14', QFLAG14.dtype, ('station_QFLAG14',))
                station_QFLAG14[:] = QFLAG14[:]

                # Define QFLAG15 dimension
                QFLAG15 = np.array(QFLAG15)
                timeSeriesProfile = ds.createDimension('station_QFLAG15', QFLAG15.shape[0])
                # Variable definitions
                station_QFLAG15 = ds.createVariable('station_QFLAG15', QFLAG15.dtype, ('station_QFLAG15',))
                station_QFLAG15[:] = QFLAG15[:]

                # Define QFLAG16 dimension
                QFLAG16 = np.array(QFLAG16)
                timeSeriesProfile = ds.createDimension('station_QFLAG16', QFLAG16.shape[0])
                # Variable definitions
                station_QFLAG16 = ds.createVariable('station_QFLAG16', QFLAG16.dtype, ('station_QFLAG16',))
                station_QFLAG16[:] = QFLAG16[:]

                # Define QFLAG17 dimension
                QFLAG17 = np.array(QFLAG17)
                timeSeriesProfile = ds.createDimension('station_QFLAG17', QFLAG17.shape[0])
                # Variable definitions
                station_QFLAG17 = ds.createVariable('station_QFLAG17', QFLAG17.dtype, ('station_QFLAG17',))
                station_QFLAG17[:] = QFLAG17[:]

                # Define QFLAG18 dimension
                QFLAG18 = np.array(QFLAG18)
                timeSeriesProfile = ds.createDimension('station_QFLAG18', QFLAG18.shape[0])
                # Variable definitions
                station_QFLAG18 = ds.createVariable('station_QFLAG18', QFLAG18.dtype, ('station_QFLAG18',))
                station_QFLAG18[:] = QFLAG18[:]

                # Define QFLAG19 dimension
                QFLAG19 = np.array(QFLAG19)
                timeSeriesProfile = ds.createDimension('station_QFLAG19', QFLAG19.shape[0])
                # Variable definitions
                station_QFLAG19 = ds.createVariable('station_QFLAG19', QFLAG19.dtype, ('station_QFLAG19',))
                station_QFLAG19[:] = QFLAG19[:]

                # Define QFLAG20 dimension
                QFLAG20 = np.array(QFLAG20)
                timeSeriesProfile = ds.createDimension('station_QFLAG20', QFLAG20.shape[0])
                # Variable definitions
                station_QFLAG20 = ds.createVariable('station_QFLAG20', QFLAG20.dtype, ('station_QFLAG20',))
                station_QFLAG20[:] = QFLAG20[:]

                # Define QFLAG21 dimension
                QFLAG21 = np.array(QFLAG21)
                timeSeriesProfile = ds.createDimension('station_QFLAG21', QFLAG21.shape[0])
                # Variable definitions
                station_QFLAG21 = ds.createVariable('station_QFLAG21', QFLAG21.dtype, ('station_QFLAG21',))
                station_QFLAG21[:] = QFLAG21[:]

                # Define QFLAG22 dimension
                QFLAG22 = np.array(QFLAG22)
                timeSeriesProfile = ds.createDimension('station_QFLAG22', QFLAG22.shape[0])
                # Variable definitions
                station_QFLAG22 = ds.createVariable('station_QFLAG22', QFLAG22.dtype, ('station_QFLAG22',))
                station_QFLAG22[:] = QFLAG22[:]

                # Define QFLAG23 dimension
                QFLAG23 = np.array(QFLAG23)
                timeSeriesProfile = ds.createDimension('station_QFLAG23', QFLAG23.shape[0])
                # Variable definitions
                station_QFLAG23 = ds.createVariable('station_QFLAG23', QFLAG23.dtype, ('station_QFLAG23',))
                station_QFLAG23[:] = QFLAG23[:]

                # Define QFLAG24 dimension
                QFLAG24 = np.array(QFLAG24)
                timeSeriesProfile = ds.createDimension('station_QFLAG24', QFLAG24.shape[0])
                # Variable definitions
                station_QFLAG24 = ds.createVariable('station_QFLAG24', QFLAG24.dtype, ('station_QFLAG24',))
                station_QFLAG24[:] = QFLAG24[:]

                # Define QFLAG25 dimension
                QFLAG25 = np.array(QFLAG25)
                timeSeriesProfile = ds.createDimension('station_QFLAG25', QFLAG25.shape[0])
                # Variable definitions
                station_QFLAG25 = ds.createVariable('station_QFLAG25', QFLAG25.dtype, ('station_QFLAG25',))
                station_QFLAG25[:] = QFLAG25[:]

                # Define QFLAG26 dimension
                QFLAG26 = np.array(QFLAG26)
                timeSeriesProfile = ds.createDimension('station_QFLAG26', QFLAG26.shape[0])
                # Variable definitions
                station_QFLAG26 = ds.createVariable('station_QFLAG26', QFLAG26.dtype, ('station_QFLAG26',))
                station_QFLAG26[:] = QFLAG26[:]

                # Define QFLAG27 dimension
                QFLAG27 = np.array(QFLAG27)
                timeSeriesProfile = ds.createDimension('station_QFLAG27', QFLAG27.shape[0])
                # Variable definitions
                station_QFLAG27 = ds.createVariable('station_QFLAG27', QFLAG27.dtype, ('station_QFLAG27',))
                station_QFLAG27[:] = QFLAG27[:]

                # Define QFLAG28 dimension
                QFLAG28 = np.array(QFLAG28)
                timeSeriesProfile = ds.createDimension('station_QFLAG28', QFLAG28.shape[0])
                # Variable definitions
                station_QFLAG28 = ds.createVariable('station_QFLAG28', QFLAG28.dtype, ('station_QFLAG28',))
                station_QFLAG28[:] = QFLAG28[:]

                # Define QFLAG29 dimension
                QFLAG29 = np.array(QFLAG29)
                timeSeriesProfile = ds.createDimension('station_QFLAG29', QFLAG29.shape[0])
                # Variable definitions
                station_QFLAG29 = ds.createVariable('station_QFLAG29', QFLAG29.dtype, ('station_QFLAG29',))
                station_QFLAG29[:] = QFLAG29[:]

                # Define QFLAG30 dimension
                QFLAG30 = np.array(QFLAG30)
                timeSeriesProfile = ds.createDimension('station_QFLAG30', QFLAG30.shape[0])
                # Variable definitions
                station_QFLAG30 = ds.createVariable('station_QFLAG30', QFLAG30.dtype, ('station_QFLAG30',))
                station_QFLAG30[:] = QFLAG30[:]

                # Define QFLAG31 dimension
                QFLAG31 = np.array(QFLAG31)
                timeSeriesProfile = ds.createDimension('station_QFLAG31', QFLAG31.shape[0])
                # Variable definitions
                station_QFLAG31 = ds.createVariable('station_QFLAG31', QFLAG31.dtype, ('station_QFLAG31',))
                station_QFLAG31[:] = QFLAG31[:]

                # Define SFLAG1 dimension
                SFLAG1 = np.array(SFLAG1)
                timeSeriesProfile = ds.createDimension('station_SFLAG1', SFLAG1.shape[0])
                # Variable definitions
                station_SFLAG1 = ds.createVariable('station_SFLAG1', SFLAG1.dtype, ('station_SFLAG1',))
                station_SFLAG1[:] = SFLAG1[:]

                # Define SFLAG2 dimension
                SFLAG2 = np.array(SFLAG2)
                timeSeriesProfile = ds.createDimension('station_SFLAG2', SFLAG2.shape[0])
                # Variable definitions
                station_SFLAG2 = ds.createVariable('station_SFLAG2', SFLAG2.dtype, ('station_SFLAG2',))
                station_SFLAG2[:] = SFLAG2[:]

                # Define SFLAG3 dimension
                SFLAG3 = np.array(SFLAG3)
                timeSeriesProfile = ds.createDimension('station_SFLAG3', SFLAG3.shape[0])
                # Variable definitions
                station_SFLAG3 = ds.createVariable('station_SFLAG3', SFLAG3.dtype, ('station_SFLAG3',))
                station_SFLAG3[:] = SFLAG3[:]

                # Define SFLAG4 dimension
                SFLAG4 = np.array(SFLAG4)
                timeSeriesProfile = ds.createDimension('station_SFLAG4', SFLAG4.shape[0])
                # Variable definitions
                station_SFLAG4 = ds.createVariable('station_SFLAG4', SFLAG4.dtype, ('station_SFLAG4',))
                station_SFLAG4[:] = SFLAG4[:]

                # Define SFLAG5 dimension
                SFLAG5 = np.array(SFLAG5)
                timeSeriesProfile = ds.createDimension('station_SFLAG5', SFLAG5.shape[0])
                # Variable definitions
                station_SFLAG5 = ds.createVariable('station_SFLAG5', SFLAG5.dtype, ('station_SFLAG5',))
                station_SFLAG5[:] = SFLAG5[:]

                # Define SFLAG6 dimension
                SFLAG6 = np.array(SFLAG6)
                timeSeriesProfile = ds.createDimension('station_SFLAG6', SFLAG6.shape[0])
                # Variable definitions
                station_SFLAG6 = ds.createVariable('station_SFLAG6', SFLAG6.dtype, ('station_SFLAG6',))
                station_SFLAG6[:] = SFLAG6[:]

                # Define SFLAG7 dimension
                SFLAG7 = np.array(SFLAG7)
                timeSeriesProfile = ds.createDimension('station_SFLAG7', SFLAG7.shape[0])
                # Variable definitions
                station_SFLAG7 = ds.createVariable('station_SFLAG7', SFLAG7.dtype, ('station_SFLAG7',))
                station_SFLAG7[:] = SFLAG7[:]

                # Define SFLAG8 dimension
                SFLAG8 = np.array(SFLAG8)
                timeSeriesProfile = ds.createDimension('station_SFLAG8', SFLAG8.shape[0])
                # Variable definitions
                station_SFLAG8 = ds.createVariable('station_SFLAG8', SFLAG8.dtype, ('station_SFLAG8',))
                station_SFLAG8[:] = SFLAG8[:]

                # Define SFLAG9 dimension
                SFLAG9 = np.array(SFLAG9)
                timeSeriesProfile = ds.createDimension('station_SFLAG9', SFLAG9.shape[0])
                # Variable definitions
                station_SFLAG9 = ds.createVariable('station_SFLAG9', SFLAG9.dtype, ('station_SFLAG9',))
                station_SFLAG9[:] = SFLAG9[:]

                # Define SFLAG10 dimension
                SFLAG10 = np.array(SFLAG10)
                timeSeriesProfile = ds.createDimension('station_SFLAG10', SFLAG10.shape[0])
                # Variable definitions
                station_SFLAG10 = ds.createVariable('station_SFLAG10', SFLAG10.dtype, ('station_SFLAG10',))
                station_SFLAG10[:] = SFLAG10[:]

                # Define SFLAG11 dimension
                SFLAG11 = np.array(SFLAG11)
                timeSeriesProfile = ds.createDimension('station_SFLAG11', SFLAG11.shape[0])
                # Variable definitions
                station_SFLAG11 = ds.createVariable('station_SFLAG11', SFLAG11.dtype, ('station_SFLAG11',))
                station_SFLAG11[:] = SFLAG11[:]

                # Define SFLAG12 dimension
                SFLAG12 = np.array(SFLAG12)
                timeSeriesProfile = ds.createDimension('station_SFLAG12', SFLAG12.shape[0])
                # Variable definitions
                station_SFLAG12 = ds.createVariable('station_SFLAG12', SFLAG12.dtype, ('station_SFLAG12',))
                station_SFLAG12[:] = SFLAG12[:]

                # Define SFLAG13 dimension
                SFLAG13 = np.array(SFLAG13)
                timeSeriesProfile = ds.createDimension('station_SFLAG13', SFLAG13.shape[0])
                # Variable definitions
                station_SFLAG13 = ds.createVariable('station_SFLAG13', SFLAG13.dtype, ('station_SFLAG13',))
                station_SFLAG13[:] = SFLAG13[:]

                # Define SFLAG14 dimension
                SFLAG14 = np.array(SFLAG14)
                timeSeriesProfile = ds.createDimension('station_SFLAG14', SFLAG14.shape[0])
                # Variable definitions
                station_SFLAG14 = ds.createVariable('station_SFLAG14', SFLAG14.dtype, ('station_SFLAG14',))
                station_SFLAG14[:] = SFLAG14[:]

                # Define SFLAG15 dimension
                SFLAG15 = np.array(SFLAG15)
                timeSeriesProfile = ds.createDimension('station_SFLAG15', SFLAG15.shape[0])
                # Variable definitions
                station_SFLAG15 = ds.createVariable('station_SFLAG15', SFLAG15.dtype, ('station_SFLAG15',))
                station_SFLAG15[:] = SFLAG15[:]

                # Define SFLAG16 dimension
                SFLAG16 = np.array(SFLAG16)
                timeSeriesProfile = ds.createDimension('station_SFLAG16', SFLAG16.shape[0])
                # Variable definitions
                station_SFLAG16 = ds.createVariable('station_SFLAG16', SFLAG16.dtype, ('station_SFLAG16',))
                station_SFLAG16[:] = SFLAG16[:]

                # Define SFLAG17 dimension
                SFLAG17 = np.array(SFLAG17)
                timeSeriesProfile = ds.createDimension('station_SFLAG17', SFLAG17.shape[0])
                # Variable definitions
                station_SFLAG17 = ds.createVariable('station_SFLAG17', SFLAG17.dtype, ('station_SFLAG17',))
                station_SFLAG17[:] = SFLAG17[:]

                # Define SFLAG18 dimension
                SFLAG18 = np.array(SFLAG18)
                timeSeriesProfile = ds.createDimension('station_SFLAG18', SFLAG18.shape[0])
                # Variable definitions
                station_SFLAG18 = ds.createVariable('station_SFLAG18', SFLAG18.dtype, ('station_SFLAG18',))
                station_SFLAG18[:] = SFLAG18[:]

                # Define SFLAG19 dimension
                SFLAG19 = np.array(SFLAG19)
                timeSeriesProfile = ds.createDimension('station_SFLAG19', SFLAG19.shape[0])
                # Variable definitions
                station_SFLAG19 = ds.createVariable('station_SFLAG19', SFLAG19.dtype, ('station_SFLAG19',))
                station_SFLAG19[:] = SFLAG19[:]

                # Define SFLAG20 dimension
                SFLAG20 = np.array(SFLAG20)
                timeSeriesProfile = ds.createDimension('station_SFLAG20', SFLAG20.shape[0])
                # Variable definitions
                station_SFLAG20 = ds.createVariable('station_SFLAG20', SFLAG20.dtype, ('station_SFLAG20',))
                station_SFLAG20[:] = SFLAG20[:]

                # Define SFLAG21 dimension
                SFLAG21 = np.array(SFLAG21)
                timeSeriesProfile = ds.createDimension('station_SFLAG21', SFLAG21.shape[0])
                # Variable definitions
                station_SFLAG21 = ds.createVariable('station_SFLAG21', SFLAG21.dtype, ('station_SFLAG21',))
                station_SFLAG21[:] = SFLAG21[:]

                # Define SFLAG22 dimension
                SFLAG22 = np.array(SFLAG22)
                timeSeriesProfile = ds.createDimension('station_SFLAG22', SFLAG22.shape[0])
                # Variable definitions
                station_SFLAG22 = ds.createVariable('station_SFLAG22', SFLAG22.dtype, ('station_SFLAG22',))
                station_SFLAG22[:] = SFLAG22[:]

                # Define SFLAG23 dimension
                SFLAG23 = np.array(SFLAG23)
                timeSeriesProfile = ds.createDimension('station_SFLAG23', SFLAG23.shape[0])
                # Variable definitions
                station_SFLAG23 = ds.createVariable('station_SFLAG23', SFLAG23.dtype, ('station_SFLAG23',))
                station_SFLAG23[:] = SFLAG23[:]

                # Define SFLAG24 dimension
                SFLAG24 = np.array(SFLAG24)
                timeSeriesProfile = ds.createDimension('station_SFLAG24', SFLAG24.shape[0])
                # Variable definitions
                station_SFLAG24 = ds.createVariable('station_SFLAG24', SFLAG24.dtype, ('station_SFLAG24',))
                station_SFLAG24[:] = SFLAG24[:]

                # Define SFLAG25 dimension
                SFLAG25 = np.array(SFLAG25)
                timeSeriesProfile = ds.createDimension('station_SFLAG25', SFLAG25.shape[0])
                # Variable definitions
                station_SFLAG25 = ds.createVariable('station_SFLAG25', SFLAG25.dtype, ('station_SFLAG25',))
                station_SFLAG25[:] = SFLAG25[:]

                # Define SFLAG26 dimension
                SFLAG26 = np.array(SFLAG26)
                timeSeriesProfile = ds.createDimension('station_SFLAG26', SFLAG26.shape[0])
                # Variable definitions
                station_SFLAG26 = ds.createVariable('station_SFLAG26', SFLAG26.dtype, ('station_SFLAG26',))
                station_SFLAG26[:] = SFLAG26[:]

                # Define SFLAG27 dimension
                SFLAG27 = np.array(SFLAG27)
                timeSeriesProfile = ds.createDimension('station_SFLAG27', SFLAG27.shape[0])
                # Variable definitions
                station_SFLAG27 = ds.createVariable('station_SFLAG27', SFLAG27.dtype, ('station_SFLAG27',))
                station_SFLAG27[:] = SFLAG27[:]

                # Define SFLAG28 dimension
                SFLAG28 = np.array(SFLAG28)
                timeSeriesProfile = ds.createDimension('station_SFLAG28', SFLAG28.shape[0])
                # Variable definitions
                station_SFLAG28 = ds.createVariable('station_SFLAG28', SFLAG28.dtype, ('station_SFLAG28',))
                station_SFLAG28[:] = SFLAG28[:]

                # Define SFLAG29 dimension
                SFLAG29 = np.array(SFLAG29)
                timeSeriesProfile = ds.createDimension('station_SFLAG29', SFLAG29.shape[0])
                # Variable definitions
                station_SFLAG29 = ds.createVariable('station_SFLAG29', SFLAG29.dtype, ('station_SFLAG29',))
                station_SFLAG29[:] = SFLAG29[:]

                # Define SFLAG30 dimension
                SFLAG30 = np.array(SFLAG30)
                timeSeriesProfile = ds.createDimension('station_SFLAG30', SFLAG30.shape[0])
                # Variable definitions
                station_SFLAG30 = ds.createVariable('station_SFLAG30', SFLAG30.dtype, ('station_SFLAG30',))
                station_SFLAG30[:] = SFLAG30[:]

                # Define SFLAG31 dimension
                SFLAG31 = np.array(SFLAG31)
                timeSeriesProfile = ds.createDimension('station_SFLAG31', SFLAG31.shape[0])
                # Variable definitions
                station_SFLAG31 = ds.createVariable('station_SFLAG31', SFLAG31.dtype, ('station_SFLAG31',))
                station_SFLAG31[:] = SFLAG31[:]
                
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
