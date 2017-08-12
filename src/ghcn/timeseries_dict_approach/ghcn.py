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

    def initialize_element_lists_with_time_key_and_placeholder_value(self, fileId):
        dictOfUniqueTimeValues = self.get_unique_time_values(fileId)
        # Inverse keys and values to get the time value as the key in the
        # dictionary
        dictOfUniqueTimeValues_inversed = dict(
            (v, k) for k, v in dictOfUniqueTimeValues.iteritems())
        # Order by unique time value ascending and set all values to
        # placeholder value
        newDict1 = OrderedDict(sorted(dictOfUniqueTimeValues_inversed.fromkeys(
            dictOfUniqueTimeValues_inversed, -9999).items()))
        newDict2 = OrderedDict(sorted(dictOfUniqueTimeValues_inversed.fromkeys(
            dictOfUniqueTimeValues_inversed, ' ').items()))

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
                    item] = newDict1
            else:
                placeholderElementsFlagsList[
                    item] = newDict2

        print placeholderElementsFlagsList['tmin'][87535.0]
        # Returns dict of lists
        return placeholderElementsFlagsList

    def create_elements_flags_data_lists(self, fileId):
        # Get list of all time values of the file
        allTimeValuesList = self.get_unique_time_values(fileId)

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

                    # Add values to the empty lists inside of dictionary initialized at beginning of function
                    # VALUE1
                    timeIndex = self.get_time_index_for_day(
                        line, 1, allTimeValuesList, element)
                    elementAndFlagDicts[element][timeIndex] = line[21:26]
                    elementAndFlagArrays[
                        element + '_mflag'][timeIndex] = line[26:27]
                    elementAndFlagArrays[
                        element + '_qflag'][timeIndex] = line[27:28]
                    elementAndFlagArrays[
                        element + '_sflag'][timeIndex] = line[28:29]

            print elementAndFlagDicts

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
                    datetime.datetime.today().strftime('%Y-%m-%d-%H:%M:%S')
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

    testfile = "AGE00147710"

    ghcn = GHCN()

    ghcn.download_dly_file(testfile)
    ghcn.get_unique_time_values(testfile)
    ghcn.get_unique_elements(testfile)
    ghcn.initialize_element_lists_with_time_key_and_placeholder_value(testfile)
    # ghcn.create_elements_flags_data_lists(testfile)
    # ghcn.parse_to_netCDF(testfile)

    print('The program took ', (time.time() - start), 'seconds to complete.')

# End __main__
