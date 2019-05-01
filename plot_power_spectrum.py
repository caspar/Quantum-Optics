import numpy as np
import matplotlib.pyplot as plt
from DataDriver import clean_time
import pandas as pd
from functools import partial
import re


def plot_power_spectrum(time_step, times, values, data_title, data_ax,
                        ps_ax, color='k'):

    ps = abs(np.fft.fft(values))**2

    N = values.shape[0]
    freqs = np.fft.fftfreq(N, time_step)
    indices = np.argsort(freqs)[N // 2:]

    ps_ax.plot(freqs[indices], ps[indices], 'b',
               label='Power Spectrum of {}'.format(data_title),
               color=color)
    ps_ax.set_xlabel("Freq (Hz)")
    ps_ax.set_ylabel("Intensity")
    ps_ax.set_yscale('log')
    ps_ax.legend()
    ps_ax.grid(True)

    return data_ax, ps_ax


if __name__ == "__main__":
    filename = "data/Feb_20_Run_1_NoBS"
    with open(filename, 'r') as file_handle:
        line_one = file_handle.readline()
        match = re.search(r"\d+$", line_one)
        if match:
            clock_rate = int(match.group())
        else:
            clock_rate = 0
            print("Did not find clock rate")

    read_data = partial(pd.read_csv, filename,
                        skiprows=3)

    data = read_data()
    data = clean_time(data)

    times = data.index.values
    ch1 = data["Ch 1"].values
    ch2 = data["Ch 2"].values
    ch3 = data["Ch 3"].values
    time_step = 1 / clock_rate

    num_rows = 3
    fig, ax = plt.subplots(num_rows, 1, figsize=(20, 20))

    colors = ['red', 'blue', 'green']
    values = [ch1, ch2, ch3]
    titles = ['A Counts', 'B Counts', 'AB Counts']

    with plt.style.context("lab1.mplstyle"):
        for row in range(num_rows):
            plot_power_spectrum(time_step, times, values[row], titles[row],
                                ax[row], ax[row], color=colors[row])

        plt.savefig(
            "../../Lab1_Overleaf_Writeup/img/" +
            "power_spectrum_plot" +
            ".png",
            format='png',
            dpi=300,
            bbox_inches='tight')

    plt.show()
