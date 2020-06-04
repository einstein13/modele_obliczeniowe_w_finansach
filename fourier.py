# -*- coding: utf-8 -*-

from cmath import exp, phase
from math import pi
from datetime import timedelta
from random import uniform
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

def dft_inv(equation, time, signal_count):
    result = 0.0
    for el in equation:
        if type(el) in [float, int]:
            result += el
        elif type(el) is list:
            j = complex(0, 1)
            # exp(i * 2pi * omega_n * t + i*fi_n )
            partial = exp(j*(2*pi*el[1]*time + el[2]))
            # A_n / N
            partial *= 2 * el[0] / signal_count
            result += partial
    return result

def dft_inv_full(equation, timing):
    values = []
    values_abs = []
    values_fi = []
    values_re = []
    values_im = []

    signal_count = len(timing)
    for time in timing:
        partial = dft_inv(equation, time, signal_count)
        values.append(partial)
        values_abs.append(abs(partial))
        values_fi.append(phase(partial))
        values_re.append(partial.real)
        values_im.append(partial.imag)

    return [timing, values, values_abs, values_fi, values_re, values_im]


class Fitter(object):

    fourier = None
    current_equation = []
    current_distance = []

    def __init__(self, fourierAnalysisObject):
        super(Fitter, self).__init__()
        self.fourier = fourierAnalysisObject

    def calculate_distance(self, equation):
        # values
        real_values = self.fourier.data['input']['processed'][1]
        fitted_values = self.fourier.fourier_analyse_inverse(equation)
        fitted_values = fitted_values['signal_abs']

        # calculations
        itr = 0
        itr_max = len(fitted_values)
        total = 0
        while itr < itr_max:
            total += (fitted_values[itr] - real_values[itr]) ** 2
            itr += 1

        # result
        return total
    
    def randomize_equation(self, equation):
        f = range_lookup_factor
        new_equation = []
        for el in equation:
            if type(el) in [float, int]:
                new_equation.append(uniform(el-f, el+f))
            if type(el) is list:
                partial = []
                partial.append(uniform(el[0]*(1-f), el[0]*(1+f))) # amplituda
                partial.append(uniform(el[1]*(1-f), el[1]*(1+f))) # częstość
                partial.append(uniform(el[2]-f, el[2]+f)) # faza
                new_equation.append(partial)
        return new_equation

    def run_fit(self):
        self.current_equation = self.fourier.equation_from_maxims
        self.current_distance = self.calculate_distance(self.current_equation)

        counter = 0
        counter_all = 0
        while counter < failed_lookup_tries:
            counter += 1
            counter_all += 1
            new_equation = self.randomize_equation(self.current_equation)
            new_distance = self.calculate_distance(new_equation)
            if new_distance < self.current_distance:
                self.current_distance = new_distance
                self.current_equation = new_equation
                print(". -> %d" % counter)
                counter = 0

        return self.current_equation


class FourierAnalysis(object):

    data = {}
    freq_domain = {}
    valuable_maxims = []
    equation_from_maxims = []
    signal_domain = {}

    def __init__(self, data):
        super().__init__()
        self.data = data
        self.freq_domain = {}
        self.valuable_maxims = []
        self.equation_from_maxims = []
        self.signal_domain = {}
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
        values = list(self.data['input']['processed'][1])
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

    def find_valuable_maxims(self, verbose=False):
        # finds how many frequences are "above noise"
        points = self.find_maxims_index()
        
        # points and values
        halves = []
        p_max = len(self.freq_domain['omegas']) // 2 + 1
        for p in points:
            if p > p_max:
                break
            halves.append([self.freq_domain['dft_abs'][p], p])
        halves.sort(reverse=True)

        # if too many below treshold, stop
        result = [halves[0][1]]
        if verbose:
            print("* * * Znalezione częstości * * *")
            print("Amplituda / Częstość / Długość okresu / indeks")
            data = (
                halves[0][0],
                self.freq_domain['omegas'][halves[0][1]],
                1 / self.freq_domain['omegas'][halves[0][1]],
                halves[0][1]
                )
            print("%g / %g / %g / %d" % data)
        for itr in range(1, len(halves)):
            treshold = halves[itr][0] * noise_treshold

            # https://stackoverflow.com/questions/10543303/number-of-values-in-a-list-greater-than-a-certain-number
            counter = sum(el[0] > treshold for el in halves)
            if counter >= len(result) + count_treshold:
                break

            if verbose:
                data = (
                    halves[itr][0],
                    self.freq_domain['omegas'][halves[itr][1]],
                    1 / self.freq_domain['omegas'][halves[itr][1]],
                    halves[itr][1]
                    )
                print("%g / %g / %g / %d" % data)
            result.append(halves[itr][1])

        if verbose:
            print("* * * * * *")
        self.valuable_maxims = result
        return result

    def plot_freq_basic_analysis(self):
        omegas = self.freq_domain['omegas']
        dft_abs = self.freq_domain['dft_abs']
        
        points = self.find_valuable_maxims()

        file = filenames['basic_fourier_analysis_freq'] % curr

        args = {}
        args['filename'] = file
        args['data'] = [omegas, dft_abs]
        args['highlight_data'] = points
        args['y_label'] = 'amplituda'
        args['x_label'] = 'częstość [1/dzień]'
        return plot(args)

    def translate_maxims_to_equation(self):
        self.equation_from_maxims.append(self.freq_domain['input']['base_average'])

        for index in self.valuable_maxims:
            additional = []
            additional.append(self.freq_domain['dft_abs'][index])
            additional.append(self.freq_domain['omegas'][index])
            additional.append(self.freq_domain['dft_fi'][index])
            self.equation_from_maxims.append(additional)

        return self.equation_from_maxims

    def fourier_analyse_inverse(self, equation):
        partial = dft_inv_full(equation, self.freq_domain['input']['timing'])
        self.signal_domain['timing'] = self.freq_domain['input']['timing']
        self.signal_domain['signal'] = list(partial[1])
        self.signal_domain['signal_abs'] = list(partial[2])
        self.signal_domain['signal_fi'] = list(partial[3])
        self.signal_domain['signal_re'] = list(partial[4])
        self.signal_domain['signal_im'] = list(partial[5])
        return self.signal_domain

    def plot_basic_data_with_dff_fit(self):
        self.find_valuable_maxims(True)

        equation = self.translate_maxims_to_equation()
        fitted_signal = self.fourier_analyse_inverse(equation)

        file = filenames['basic_fourier_analysis_fit'] % curr
        
        args = {}
        args['data'] = [
            self.data['input']['processed'][0], # time
            self.data['input']['processed'][1], # real values
            fitted_signal['signal_abs'] # fitted values
            ]
        args['filename'] = file

        return plot(args)

    def basic_analysis(self):
        self.fourier_analyse()
        self.plot_freq_basic_analysis()
        self.plot_basic_data_with_dff_fit()
        f = Fitter(self)
        print(f.calculate_distance(self.equation_from_maxims))
        print(f.run_fit())
        print(f.current_distance)
        return


