from datetime import timedelta

# what are the filenames
filenames = {
    'archive': 'source/archiwum_tab_a_%d.csv', # archives
    'raw_extract': 'source/raw_extract.csv', # target for raw data extract
    'basic_plot': 'plots/%s_raw_data.png', # plot for raw currency data
    'basic_fourier_analysis_freq': 'plots/%s_fourier_frequencies.png', # plot of dft result
    'basic_fourier_analysis_fit': 'plots/%s_fourier_raw_data_fit.png', # plot of fourier fit to raw data
}

# what are year ranges
# used for downloading data from files
years = [2012, 2020]

# what is the currency
# used for downloading data from files
curr = "USD"

# what is the range for local maximum (+/- from point)
# used for major frequency lookup
local_maximum_range = 15

# shortest timedelta for calculations (1 day)
timedelta_epsilon = timedelta(1)

# value in range 0.0 .. 1.0; higher value - more sine waves are respected as valuable
noise_treshold = 0.75
# int value; higher value - less strict about how many sin waves are respected
count_treshold = 5