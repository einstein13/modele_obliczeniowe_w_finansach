# -*- coding: utf-8 -*-

import codecs


filenames = {
    'archive': 'source/archiwum_tab_a_%d.csv',
    'raw_extract': 'source/raw_extract.csv'
}


class raw_file_extract(object):
    """docstring for raw_file_extract"""
    def __init__(self):
        super().__init__()
        return

    def extract_from_file(self, year):
        # returns two lists: dates in string, values in string (comma as decimal point!)

        result = [[], []]
        # file content
        file = codecs.open(filenames['archive'] % year, encoding="cp1250", mode="r")
        content = file.read()
        file.close()
        lines = content.split("\r\n")
        
        # find USD position
        oneline = lines[0]
        oneline = oneline.split(";")
        usdpos = -1
        itr = 0
        while itr < len(oneline):
            if "USD" in oneline[itr]:
                usdpos = itr
                break
            itr += 1

        if usdpos == -1:
            return result

        # for other lines take date and usd
        itr = 1
        while itr < len(lines):
            oneline = lines[itr]
            if oneline == '':
                itr += 1
                break
            oneline = oneline.split(";")
            if oneline[0] == '':
                itr += 1
                continue
            result[0].append(oneline[0])
            result[1].append(oneline[usdpos])
            itr += 1

        return result

    def extract_from_sources(self):
        year_start = 2012
        year_end = 2020
        year = year_start

        result = [[], []]

        while year <= year_end:
            partial = self.extract_from_file(year)
            result[0] += partial[0]
            result[1] += partial[1]
            year += 1
        return result

    def save_to_file(self, data_input):
        f = open(filenames['raw_extract'], "w")
        f.write(";".join(data_input[0]))
        f.write("\n")
        f.write(";".join(data_input[1]))
        f.write("\n")
        f.close()
        return

class s1_main(object):

    data = {}

    """docstring for s1_main"""
    def __init__(self, data):
        super().__init__()
        self.data = data
        return

    def run(self):
        r = raw_file_extract()
        self.data['raw_input'] = r.extract_from_sources()
        r.save_to_file(self.data['raw_input'])
        pass
