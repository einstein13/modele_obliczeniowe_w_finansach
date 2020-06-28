# -*- coding: utf-8 -*-

from s1_data_import import s1_main
from s2_full_fourier import s2_main
from s3_rate_of_return import s3_main


data = {}

# STAGE 1: importing data
print("= = = = = = STAGE 1: importing data = = = = = =")
s1_main(data).run()
print("= = = = = = STAGE 1: importing data = = = = = =")

# STAGE 2: making basic DFT analysis
print("= = = = = = STAGE 2: basic DFT analysis = = = = = =")
s2_main(data).run()
print("= = = = = = STAGE 2: basic DFT analysis = = = = = =")

# STAGE 3: logarithmic rate of return analysis 
print("= = = = = = STAGE 1: logarithmic rate of return = = = = = =")
s3_main(data).run()
print("= = = = = = STAGE 1: logarithmic rate of return = = = = = =")