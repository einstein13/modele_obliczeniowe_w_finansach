# -*- coding: utf-8 -*-

from plots import plot
from fourier import FourierAnalysis
from settings import *


class s2_main(object):

    data = {}

    """docstring for s1_main"""
    def __init__(self, data):
        super().__init__()
        self.data = data
        return

    def run(self):
        f = FourierAnalysis(self.data)
        f.basic_analysis()
        return self.data
