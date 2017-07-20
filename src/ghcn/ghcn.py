import time
import urllib2


class GHCN:
    """docstring for ghcn"""

    def __init__(self):
        self.stationIds = []

    def getIDs(self):
        data = urllib2.urlopen("ftp://ftp.ncdc.noaa.gov/pub/data/ghcn/daily/ghcnd-stations.txt")
        for line in data:
            if not line:
                break
            # Get station IDs as substrings from each line in source file
            self.stationIds.append(line[:11])
        # print(self.stationIds)
        print(len(self.stationIds))
        return self.stationIds

# __main__
if __name__ == '__main__':
    start = time.time()

    ghcn = GHCN()
    ghcn.getIDs()

    print 'The program took ', time.time()-start, 'seconds to complete.'
                
# End __main__
