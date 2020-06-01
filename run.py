# -*- coding: utf-8 -*-

from s1_data_import import s1_main
from s2_full_fourier import s2_main
from s3_fitting_fourier import s3_main


data = {}

# STAGE 1: importing data
s1_main(data).run()

# STAGE 2: making basic DFT analysis
s2_main(data).run()

# STAGE 3: fitting DFT result to data
s3_main(data).run()