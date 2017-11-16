import urllib2
import numpy as np
import re

stationIds = []
latDict = {}
lonDict = {}
elevationDict = {}
stationLongNameDict = {}

def get_station_info():
    # Alternatively https://www1.ncdc.noaa.gov/ OR ftp://ftp.ncdc.noaa.gov/
    data = urllib2.urlopen(
        "https://www1.ncdc.noaa.gov/pub/data/ghcn/daily/ghcnd-stations.txt")
    for line in data:
        if not line:
            break
        # Get station IDs as substrings from each line in source file, etc.
        stationIds.append(line[0:11])
        latDict[line[0:11]] = line[12:20]
        lonDict[line[0:11]] = line[21:30]
        elevationDict[line[0:11]] = line[31:37]
        stationLongNameDict[line[0:11]] = re.sub(r'[^\x00-\x7f]', r'', line[38:71].strip())
    
    np.save('stationIds.npy', stationIds)
    np.save('latDict.npy', latDict)
    np.save('lonDict.npy', lonDict)
    np.save('elevationDict.npy', elevationDict)
    np.save('stationLongNameDict', stationLongNameDict)

get_station_info()