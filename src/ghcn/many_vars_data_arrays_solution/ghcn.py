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

                time = ds.createVariable('time', 'd')
                time.long_name = 'Center time of day'
                time.standard_name = 'time'
                time.units = 'days since 1700-01-01 12:00:00'
                time.axis = 'T'
                time.calendar = 'gregorian'
                time.coverage_content_type = 'coordinate'

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

                station_name = ds.createVariable('station_name', 'string')
                station_name.long_name = self.stationLongNameDict[fileId]
                station_name.standard_name = 'platform_name'
                station_name.cf_role = 'timeseries_id'
                station_name.coverage_content_type = 'coordinate'

                station_id = ds.createVariable('station_id', 'string')
                station_id.long_name = ID[0]
                station_id.standard_name = 'platform_id'


                # Actual source data arrays
                YEAR = np.array(YEAR)
                year = ds.createVariable('year', YEAR.dtype, ('time',))
                year[:] = YEAR[:]

                ELEMENT = np.array(ELEMENT)
                element = ds.createVariable('element', ELEMENT.dtype, ('time',))
                element[:] = ELEMENT[:]
                
                VALUE1 = np.array(VALUE1)
                value1 = ds.createVariable('value1', VALUE1.dtype, ('time',))
                value1[:] = VALUE1[:]
                
                MFLAG1 = np.array(MFLAG1)
                mflag1 = ds.createVariable('mflag1', MFLAG1.dtype, ('time',))
                mflag1[:] = MFLAG1[:]
                
                QFLAG1 = np.array(QFLAG1)
                qflag1 = ds.createVariable('qflag1', QFLAG1.dtype, ('time',))
                qflag1[:] = QFLAG1[:]
                
                SFLAG1 = np.array(SFLAG1)
                sflag1 = ds.createVariable('sflag1', SFLAG1.dtype, ('time',))
                sflag1[:] = SFLAG1[:]
                
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
