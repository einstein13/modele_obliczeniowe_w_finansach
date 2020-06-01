from s1_data_import import s1_main
from s2_full_fourier import s2_main


data = {}

# STAGE 1: importing data
s1_main().run(data)
# STAGE 2: making DFT analysis
s2_main().run(data)