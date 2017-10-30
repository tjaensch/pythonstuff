def initialize_element_lists_with_time_key_and_placeholder_value(self, fileId, dictOfUniqueTimeValues, uniqueElements):
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
                dict1 = {}
                for key, value in dictOfUniqueTimeValues.items():
                    dict1[key] = -9999
                placeholderElementsFlagsList[
                    item] = dict1
            else:
                dict2 = {}
                for key, value in dictOfUniqueTimeValues.items():
                    dict2[key] = ' '
                placeholderElementsFlagsList[
                    item] = dict2
        return placeholderElementsFlagsList