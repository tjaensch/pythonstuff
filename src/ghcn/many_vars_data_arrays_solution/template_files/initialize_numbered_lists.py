def initialize_numbered_1_31_VALUE_MFLAG_QFLAG_SFLAG_lists():
    numberedList = {}
    for i in range(1,32):
        numberedList['VALUE' + str(i)] = []
        numberedList['MFLAG' + str(i)] = []
        numberedList['QFLAG' + str(i)] = []
        numberedList['SFLAG' + str(i)] = []
    #print(numberedLists)  
    #print(len(numberedLists))
    return numberedList

initialize_numbered_1_31_VALUE_MFLAG_QFLAG_SFLAG_lists()