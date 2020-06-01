from cmath import exp, phase
from math import pi

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
