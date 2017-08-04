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
            # Empty lists for variables, more information here ftp://ftp.ncdc.noaa.gov/pub/data/ghcn/daily/readme.txt
            ID = []
            YEAR = []
            MONTH = []
            ELEMENT = []
            numberedList = self.initialize_numbered_1_31_VALUE_MFLAG_QFLAG_SFLAG_lists()

            # Fill lists with substring values 0-269 per record per line from .dly file
            with open ("./dly_data_as_txt/" + fileId + ".txt", "r") as file:
                for line in file:
                    ID.append(line[0:11])
                    YEAR.append(line[11:15])
                    MONTH.append(line[15:17])
                    ELEMENT.append(line[17:21])
                    numberedList['VALUE1'].append(line[21:26]); numberedList['MFLAG1'].append(line[26:27]); numberedList['QFLAG1'].append(line[27:28]); numberedList['SFLAG1'].append(line[28:29])
                    numberedList['VALUE2'].append(line[29:34]); numberedList['MFLAG2'].append(line[34:35]); numberedList['QFLAG2'].append(line[35:36]); numberedList['SFLAG2'].append(line[36:37])
                    numberedList['VALUE3'].append(line[37:42]); numberedList['MFLAG3'].append(line[42:43]); numberedList['QFLAG3'].append(line[43:44]); numberedList['SFLAG3'].append(line[44:45])
                    numberedList['VALUE4'].append(line[45:50]); numberedList['MFLAG4'].append(line[50:51]); numberedList['QFLAG4'].append(line[51:52]); numberedList['SFLAG4'].append(line[52:53])
                    numberedList['VALUE5'].append(line[53:58]); numberedList['MFLAG5'].append(line[58:59]); numberedList['QFLAG5'].append(line[59:60]); numberedList['SFLAG5'].append(line[60:61])
                    numberedList['VALUE6'].append(line[61:66]); numberedList['MFLAG6'].append(line[66:67]); numberedList['QFLAG6'].append(line[67:68]); numberedList['SFLAG6'].append(line[68:69])
                    numberedList['VALUE7'].append(line[69:74]); numberedList['MFLAG7'].append(line[74:75]); numberedList['QFLAG7'].append(line[75:76]); numberedList['SFLAG7'].append(line[76:77])
                    numberedList['VALUE8'].append(line[77:82]); numberedList['MFLAG8'].append(line[82:83]); numberedList['QFLAG8'].append(line[83:84]); numberedList['SFLAG8'].append(line[84:85])
                    numberedList['VALUE9'].append(line[85:90]); numberedList['MFLAG9'].append(line[90:91]); numberedList['QFLAG9'].append(line[91:92]); numberedList['SFLAG9'].append(line[92:93])
                    numberedList['VALUE10'].append(line[93:98]); numberedList['MFLAG10'].append(line[98:99]); numberedList['QFLAG10'].append(line[99:100]); numberedList['SFLAG10'].append(line[100:101])
                    numberedList['VALUE11'].append(line[101:106]); numberedList['MFLAG11'].append(line[106:107]); numberedList['QFLAG11'].append(line[107:108]); numberedList['SFLAG11'].append(line[108:109])
                    numberedList['VALUE12'].append(line[109:114]); numberedList['MFLAG12'].append(line[114:115]); numberedList['QFLAG12'].append(line[115:116]); numberedList['SFLAG12'].append(line[116:117])
                    numberedList['VALUE13'].append(line[117:122]); numberedList['MFLAG13'].append(line[122:123]); numberedList['QFLAG13'].append(line[123:124]); numberedList['SFLAG13'].append(line[124:125])
                    numberedList['VALUE14'].append(line[125:130]); numberedList['MFLAG14'].append(line[130:131]); numberedList['QFLAG14'].append(line[131:132]); numberedList['SFLAG14'].append(line[132:133])
                    numberedList['VALUE15'].append(line[133:138]); numberedList['MFLAG15'].append(line[138:139]); numberedList['QFLAG15'].append(line[139:140]); numberedList['SFLAG15'].append(line[140:141])
                    numberedList['VALUE16'].append(line[141:146]); numberedList['MFLAG16'].append(line[146:147]); numberedList['QFLAG16'].append(line[147:148]); numberedList['SFLAG16'].append(line[148:149])
                    numberedList['VALUE17'].append(line[149:154]); numberedList['MFLAG17'].append(line[154:155]); numberedList['QFLAG17'].append(line[155:156]); numberedList['SFLAG17'].append(line[156:157])
                    numberedList['VALUE18'].append(line[157:162]); numberedList['MFLAG18'].append(line[162:163]); numberedList['QFLAG18'].append(line[163:164]); numberedList['SFLAG18'].append(line[164:165])
                    numberedList['VALUE19'].append(line[165:170]); numberedList['MFLAG19'].append(line[170:171]); numberedList['QFLAG19'].append(line[171:172]); numberedList['SFLAG19'].append(line[172:173])
                    numberedList['VALUE20'].append(line[173:178]); numberedList['MFLAG20'].append(line[178:179]); numberedList['QFLAG20'].append(line[179:180]); numberedList['SFLAG20'].append(line[180:181])
                    numberedList['VALUE21'].append(line[181:186]); numberedList['MFLAG21'].append(line[186:187]); numberedList['QFLAG21'].append(line[187:188]); numberedList['SFLAG21'].append(line[188:189])
                    numberedList['VALUE22'].append(line[189:194]); numberedList['MFLAG22'].append(line[194:195]); numberedList['QFLAG22'].append(line[195:196]); numberedList['SFLAG22'].append(line[196:197])
                    numberedList['VALUE23'].append(line[197:202]); numberedList['MFLAG23'].append(line[202:203]); numberedList['QFLAG23'].append(line[203:204]); numberedList['SFLAG23'].append(line[204:205])
                    numberedList['VALUE24'].append(line[205:210]); numberedList['MFLAG24'].append(line[210:211]); numberedList['QFLAG24'].append(line[211:212]); numberedList['SFLAG24'].append(line[212:213])
                    numberedList['VALUE25'].append(line[213:218]); numberedList['MFLAG25'].append(line[218:219]); numberedList['QFLAG25'].append(line[219:220]); numberedList['SFLAG25'].append(line[220:221])
                    numberedList['VALUE26'].append(line[221:226]); numberedList['MFLAG26'].append(line[226:227]); numberedList['QFLAG26'].append(line[227:228]); numberedList['SFLAG26'].append(line[228:229])
                    numberedList['VALUE27'].append(line[229:234]); numberedList['MFLAG27'].append(line[234:235]); numberedList['QFLAG27'].append(line[235:236]); numberedList['SFLAG27'].append(line[236:237])
                    numberedList['VALUE28'].append(line[237:242]); numberedList['MFLAG28'].append(line[242:243]); numberedList['QFLAG28'].append(line[243:244]); numberedList['SFLAG28'].append(line[244:245])
                    numberedList['VALUE29'].append(line[245:250]); numberedList['MFLAG29'].append(line[250:251]); numberedList['QFLAG29'].append(line[251:252]); numberedList['SFLAG29'].append(line[252:253])
                    numberedList['VALUE30'].append(line[253:258]); numberedList['MFLAG30'].append(line[258:259]); numberedList['QFLAG30'].append(line[259:260]); numberedList['SFLAG30'].append(line[260:261])
                    numberedList['VALUE31'].append(line[261:266]); numberedList['MFLAG31'].append(line[266:267]); numberedList['QFLAG31'].append(line[267:268]); numberedList['SFLAG31'].append(line[268:269])

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
                ds.createVariable('year', np.array(YEAR).dtype, ('time',))[:] = np.array(YEAR)[:]
                ds.createVariable('element', np.array(ELEMENT).dtype, ('time',))[:] = np.array(ELEMENT)[:]
                
                # Loop over VALUE/MFLAG/QFLAG/SFLAG:1-31 data arrays
                for i in xrange (1,32):
                    ds.createVariable('value' + str(i), np.array(numberedList['VALUE' + str(i)]).dtype, ('time',))[:] = np.array(numberedList['VALUE' + str(i)])[:]  
                    ds.createVariable('mflag' + str(i), np.array(numberedList['MFLAG' + str(i)]).dtype, ('time',))[:] = np.array(numberedList['MFLAG' + str(i)])[:] 
                    ds.createVariable('qflag' + str(i), np.array(numberedList['QFLAG' + str(i)]).dtype, ('time',))[:] = np.array(numberedList['QFLAG' + str(i)])[:]  
                    ds.createVariable('sflag' + str(i), np.array(numberedList['SFLAG' + str(i)]).dtype, ('time',))[:] = np.array(numberedList['SFLAG' + str(i)])[:]
                
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

    print('The program took ', (time.time()-start)/60, 'minutes to complete.')
                
# End __main__
