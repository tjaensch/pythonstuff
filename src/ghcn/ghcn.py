import csv
import time
import urllib
import urllib2


class GHCN:
    """docstring for ghcn"""

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
            url = 'ftp://ftp.ncdc.noaa.gov/pub/data/ghcn/daily/all/%s.dly' %fileId
            urllib.urlretrieve(url, 'dly_data_as_txt/' + fileId + '.csv')

    '''def convert_to_csv(self, fileId):
        txt_file = r"dly_data_as_txt/AGE00147710.txt"
        csv_file = r"dly_data_as_txt/AGE00147710.csv"
        in_txt = csv.reader(open(txt_file, "rb"))
        out_csv = csv.writer(open(csv_file, 'wb'))
        out_csv.writerows(in_txt)'''

# __main__
if __name__ == '__main__':
    start = time.time()

    ghcn = GHCN()
    stationIds = ghcn.get_ids()
    
    for fileId in stationIds:
        ghcn.download_dly_file(fileId)

    print 'The program took ', time.time()-start, 'seconds to complete.'
                
# End __main__
