# -*- coding: utf-8 -*-

from matplotlib import pyplot as plt

def plot(data):
    plt.clf()
    # wymagane dane

    # nie ma danych do wyświetlenia
    if 'data' not in data:
        return None
    # nie jest znany plik docelowy
    if 'filename' not in data:
        return None

    # ustawienie wartości

    # nazwa wyjściowa
    if not data['filename'].endswith(".png"):
        data['filename'] += ".png"

    # typ wykresu (liniowy / punktowy)
    availables = ['line', 'dot']
    if 'plot_type' not in data or data['plot_type'] not in availables:
        data['plot_type'] = availables[0]

    # właściwe przetwarzanie

    for itr in range(1, len(data['data'])):
        plt.plot(data['data'][0], data['data'][itr])

    if 'highlight_data' in data:
        add_data = [[], []]
        for itr in data['highlight_data']:
            add_data[0].append(data['data'][0][itr])
            add_data[1].append(data['data'][1][itr])
        size = [8]*len(add_data[0])
        plt.scatter(add_data[0], add_data[1], s=size, color='r')

    if 'y_label' in data:
        plt.ylabel(data['y_label'])
    if 'x_label' in data:
        plt.xlabel(data['x_label'])

    plt.savefig(data['filename'])
    return


