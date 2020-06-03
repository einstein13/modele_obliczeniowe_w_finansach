# -*- coding: utf-8 -*-

from cmath import exp, phase
from math import pi
from datetime import timedelta
from statistics import mean

from numpy import arange

from plots import plot
from settings import *

def dft(signal, timing, omega):
    if len(signal) != len(timing):
        return 0
    j = complex(0, 1)
    result = 0
    for itr in range(len(signal)):
        result += signal[itr] * exp(-j * 2 * pi * omega * timing[itr])
        itr += 1
    return result

def dft_full(signal, timing, omegas):
    # zwraca listę list
        # omegi - przestrzeń częstotliwości
        # dft - zespolone wartości transformaty
        # abs(dft) - wielkość dft
        # fi(dft) - fazę dft
        # re(dft) - część rzeczywistą dft
        # im(dft) - częśc urojoną dft
    dfts = []
    dft_abs = []
    dft_fi = []
    dft_re = []
    dft_im = []

    for omega in omegas:
        partial = dft(signal, timing, omega)
        dfts.append(partial)
        dft_abs.append(abs(partial))
        dft_fi.append(phase(partial))
        dft_re.append(partial.real)
        dft_im.append(partial.imag)

    return [omegas, dfts, dft_abs, dft_fi, dft_re, dft_im]


class FourierAnalysis(object):

    data = {}
    freq_domain = {}

    def __init__(self, data):
        super().__init__()
        self.data = data
        self.freq_domain = {}
        return

    def find_maxims_index(self):
        result = []
        delta = local_maximum_range # how far should we consider maximum

        itr = 0
        itr_max = len(self.freq_domain['omegas'])
        
        while itr < itr_max:
            p_min = max(0, itr-delta)
            p_max = min(itr_max, itr+delta)
            partial = self.freq_domain['dft_abs'][p_min:p_max]

            if max(partial) == self.freq_domain['dft_abs'][itr]:
                result.append(itr)

            itr += 1

        return result

    def prepare_omegas(self):
        # omega = [1/N * 1/dt, N/N * 1/dt]
        timing = self.data['input']['processed'][0]

        # shortest time delta between points
        dt = timing[1] - timing[0]
        for itr in range(len(timing) - 1):
            if dt > timing[itr+1] - timing[itr]:
                dt = timing[itr+1] - timing[itr]

        if dt < timedelta_epsilon:
            dt = timedelta_epsilon

        dt = dt.days + dt.seconds / 86400 # 86400 seconds == 1 day

        # number of points
        N = len(timing)

        result = arange(1 / (N * dt), 1 / dt, 1 / (N * dt))
        result = list(result)
        return result

    def prepare_timing(self):
        timing = list(self.data['input']['processed'][0])
        t0 = timing[0]
        result = []
        for itr in range(len(timing)):
            new_time = timing[itr] - t0
            new_time = new_time.days + new_time.seconds / 86400 # 86400 seconds == 1 day
            result.append(new_time)
        return result

    def prepare_values(self):
        values = self.data['input']['processed'][1]
        average = mean(values)
        for itr in range(len(values)):
            values[itr] -= average
        return [average, values]

    def fourier_analyse(self):
        self.freq_domain = {}
        omegas = self.prepare_omegas()
        timing = self.prepare_timing()
        [base, values] = self.prepare_values()
        dft_analyse = dft_full(values, timing, omegas)
        self.freq_domain['omegas'] = list(dft_analyse[0])
        self.freq_domain['dfts'] = list(dft_analyse[1])
        self.freq_domain['dft_abs'] = list(dft_analyse[2])
        self.freq_domain['dft_fi'] = list(dft_analyse[3])
        self.freq_domain['dft_re'] = list(dft_analyse[4])
        self.freq_domain['dft_im'] = list(dft_analyse[5])
        self.freq_domain['input'] = {}
        self.freq_domain['input']['base_average'] = base
        self.freq_domain['input']['values'] = list(values)
        self.freq_domain['input']['timing'] = list(timing)
        return self.freq_domain

    def plot_freq_basic_analysis(self):
        omegas = self.freq_domain['omegas']
        dft_abs = self.freq_domain['dft_abs']
        
        points = self.find_maxims_index()

        file = filenames['basic_fourier_analysis_freq'] % curr

        args = {}
        args['filename'] = file
        args['data'] = [omegas, dft_abs]
        args['highlight_data'] = points
        args['y_label'] = 'amplituda'
        args['x_label'] = 'częstość [1/dzień]'
        return plot(args)

    def basic_analysis(self):
        self.fourier_analyse()
        self.plot_freq_basic_analysis()
        return


