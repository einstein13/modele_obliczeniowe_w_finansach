from datetime import timedelta

# what are the filenames
filenames = {
    'archive': 'source/archiwum_tab_a_%d.csv', # archives
    'raw_extract': 'source/raw_extract.csv', # target for raw data extract
    'basic_plot': 'plots/%s_raw_data.png', # plot for raw currency data
    'basic_fourier_analysis_freq': 'plots/%s_fourier_frequencies.png', # plot of dft result
    'basic_fourier_analysis_fit': 'plots/%s_fourier_raw_data_fit.png', # plot of fourier fit to raw data
    'basic_fit_analysis_fit': 'plots/%s_fourier_fit_data_fit.png', # plot of fit to data based on fourier
}


# # # Values used in collecting data # # #

# what are year ranges
# used for downloading data from files
years = [2012, 2020]

# what is the currency
# used for downloading data from files
curr = "USD"


# # # Values used in discrete fourier transformation # # #

# shortest timedelta for calculations (1 day)
timedelta_epsilon = timedelta(1)


# # # Values used in searching result of DFT # # #

# what is the range for local maximum (+/- from point)
# used for major frequency lookup
local_maximum_range = 15

# value in range 0.0 .. 1.0; higher value - more sine waves are respected as valuable
noise_treshold = 0.75
# int value; higher value - less strict about how many sin waves are respected
count_treshold = 5


# # # Values used in numerical fitting # # #

# how far new minimum can be; larger value - larger distance
range_lookup_factor = 0.1

# how many tries before give up; lower - faster & less exact
failed_lookup_tries = 2000