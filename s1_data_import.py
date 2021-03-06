# -*- coding: utf-8 -*-

import codecs
from datetime import date, timedelta
from math import log

from plots import plot
from settings import *

class RawFileExtract(object):
    def __init__(self):
        super().__init__()
        return

    def extract_from_file(self, year):
        # returns two lists: dates in string, values in string (comma as decimal point!)

        result = [[], []]
        # file content
        try:
            file = codecs.open(filenames['archive'] % year, encoding="cp1250", mode="r")
            content = file.read()
            file.close()
            lines = content.split("\r\n")
        except Exception as e:
            return result
        
        # find USD position
        oneline = lines[0]
        oneline = oneline.split(";")
        usdpos = -1
        itr = 0
        while itr < len(oneline):
            if curr in oneline[itr]:
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
        year_start = years[0]
        year_end = years[1]
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


class DataProcessor(object):

    dates_raw = []
    values_raw = []

    def __init__(self, input_raw):
        super().__init__()
        self.dates_raw = input_raw[0]
        self.values_raw = input_raw[1]
        return

    def str_to_date(self, str_date):
        if len(str_date) != 8:
            return None
        year = str_date[0:4]
        month = str_date[4:6]
        day = str_date[6:8]
        new_date = None
        try:
            year = int(year)
            month = int(month)
            day = int(day)
            new_date = date(year, month, day)
        except Exception as e:
            return None
        return new_date

    def str_to_value(self, value):
        new_value = value.replace(",", ".")
        try:
            new_value = float(new_value)
        except Exception as e:
            return None
        return new_value

    def raw_to_values(self):
        result = [[], []]

        if len(self.dates_raw) != len(self.values_raw):
            return result

        itr = 0
        while itr < len(self.dates_raw):
            date = self.dates_raw[itr]
            value = self.values_raw[itr]
            date = self.str_to_date(date)
            value = self.str_to_value(value)
            if date != None and value != None:
                result[0].append(date)
                result[1].append(value)
            else:
                break
            itr += 1

        return result

    def moving_average(self, date):
        start_date = date - timedelta(days=moving_average_delta)
        end_date = date + timedelta(days=moving_average_delta)

        result = []
        for itr in range(len(self.dates_raw)):
            actual_date = self.str_to_date(self.dates_raw[itr])
            if actual_date < start_date:
                continue
            if actual_date > end_date:
                continue
            result.append(self.str_to_value(self.values_raw[itr]))

        if len(result) == 0:
            return 0

        return sum(result) / len(result)

    def raw_to_log_returns(self):
        result = [[], []]

        if len(self.dates_raw) != len(self.values_raw):
            return result

        itr = 1
        start_date = self.dates_raw[0]
        start_date = self.str_to_date(start_date)
        end_date = self.dates_raw[len(self.dates_raw) - 1]
        end_date = self.str_to_date(end_date)
        date = start_date
        days_delta = 1 + moving_average_delta
        while date < end_date:
            value1 = self.moving_average(date)
            value2 = self.moving_average(date + timedelta(days_delta))
            if value1 == 0 or value2 == 0:
                date += timedelta(days_delta)
                continue
            value = log(value2/value1)
            if date != None and value != None:
                result[0].append(date)
                result[1].append(value)
            else:
                break
            date += timedelta(days_delta)

        return result


class Plotter(object):
    data = {}

    def __init__(self, data):
        super().__init__()
        self.data = data
        return None

    def plot_to_file(self):
        file = filenames['basic_plot'] % curr
        data = self.data['input']['processed']

        args = {}
        args['filename'] = file
        args['data'] = data
        args['y_label'] = curr + "/PLN"
        args['x_label'] = 'czas [data]'

        return plot(args)

    def plot_to_file_log_return(self):
        file = filenames['basic_log_return_plot'] % curr
        data = self.data['input']['log_returns']

        args = {}
        args['filename'] = file
        args['data'] = data
        args['y_label'] = "logarytmiczna stopa zwrotu, średnia %d dni" % (2*moving_average_delta+1)
        args['x_label'] = 'czas [data]'

        return plot(args)


class s1_main(object):

    data = {}

    """docstring for s1_main"""
    def __init__(self, data):
        super().__init__()
        self.data = data
        return

    def run(self):
        r = RawFileExtract()
        if not 'input' in self.data:
            self.data['input'] = {}
        input_raw = r.extract_from_sources()
        self.data['input']['raw'] = input_raw
        r.save_to_file(input_raw)

        d = DataProcessor(input_raw)
        input_values = d.raw_to_values()
        self.data['input']['processed'] = input_values
        input_values = d.raw_to_log_returns()
        self.data['input']['log_returns'] = input_values

        p = Plotter(self.data)
        p.plot_to_file()
        p.plot_to_file_log_return()

        return self.data
