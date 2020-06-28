# -*- coding: utf-8 -*-

from math import log

from numpy import corrcoef

from fourier import FourierAnalysis
from plots import plot
from settings import *

class RateOfReturnAnalysis(object):

    data = {}
    analyser = None
    additionals = {}

    def __init__(self, data):
        super().__init__()
        self.data = data
        self.analyser = FourierAnalysis(data)
        self.additionals = {}

    def calculate_equation_points(self):
        result = []
        equation = self.data['fourier_fit']['current_equation']
        result = self.analyser.fourier_analyse_inverse(equation)
        result = result['signal_abs']
        self.additionals['fourier_fit'] = result
        return result

    def moving_average(self, timing, date):
        start_date = date - timedelta(days=moving_average_delta)
        end_date = date + timedelta(days=moving_average_delta)

        result = []
        for itr in range(len(timing)):
            actual_date = timing[itr]
            if actual_date < start_date:
                continue
            if actual_date > end_date:
                continue
            result.append(self.additionals['fourier_fit'][itr])

        if len(result) == 0:
            return 0

        return sum(result) / len(result)

    def equation_to_log_returns(self):
        result = [[], []]

        dates = self.data['input']['processed'][0]

        itr = 1
        start_date = dates[0]
        end_date = dates[len(dates) - 1]
        date = start_date
        days_delta = 1 + moving_average_delta
        while date < end_date:
            value1 = self.moving_average(dates, date)
            value2 = self.moving_average(dates, date + timedelta(days_delta))
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

        self.data['fourier_fit']['returns'] = result

        return result

    def plot_returns(self):
        arguments = {}

        timing = self.data['fourier_fit']['returns'][0]
        values1 = self.data['input']['log_returns'][1]
        values2 = self.data['fourier_fit']['returns'][1]
        arguments['data'] = [timing, values1, values2]

        name = filenames['both_log_return_plot'] % curr
        arguments['filename'] = name

        arguments['y_label'] = "logarytmiczna stopa zwrotu, średnia %d dni" % (2*moving_average_delta+1)
        arguments['x_label'] = "czas [data]"

        return plot(arguments)

    def print_correlation(self):
        values1 = self.data['input']['log_returns'][1]
        values2 = self.data['fourier_fit']['returns'][1]
        correlation = corrcoef(values1, values2)[0, 1]
        print(correlation)
        return        


class s3_main(object):

    data = {}

    """docstring for s1_main"""
    def __init__(self, data):
        super().__init__()
        self.data = data
        return

    def run(self):
        rora = RateOfReturnAnalysis(self.data)
        rora.calculate_equation_points()
        rora.equation_to_log_returns()
        rora.plot_returns()
        rora.print_correlation()
        return


