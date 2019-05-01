import matplotlib.pyplot as plt
import pandas as pd
import re
import os
from functools import partial
import sys


def print_number(number, title=""):
    print(title + ": {:.4E}".format(number))


def clean_time(df):
    """
    takes in a dataframe and returns the same one with time column cleaned and
    idnex set to time with proper units
    """
    df.rename({"Entry number": "entry", "Time": "time"},
              axis='columns', inplace=True)

    df.time = pd.to_timedelta(df.time, unit='s')
    df.time = df.time - df.time[0]
    df.time = df.time.dt.total_seconds()

    df.rename({"time": "time (s)"},
              axis='columns', inplace=True)
    df = df.groupby("time (s)").sum()

    return df


default_col_names = ['A', 'B', 'AB']


class DataDriver():
    def __init__(
            self,
            filename,
            col_names=default_col_names,
            number_header_lines=4):
        self.fname = filename
        self.path = "data/" + self.fname
        self.no_header = number_header_lines
        self.file_to_dataframe()
        self.figsize = (20, 20)  # make it square
        self.writeup_dir = "../../Lab1_Overleaf_Writeup/img/"
        self.tables_dir = "../../Lab1_Overleaf_Writeup/tables/"
        # when you specify which columns to analyze, you must give the column
        # names in the correct order. or change the data files
        self.data = self.data.iloc[:, 1:1 + len(col_names)]
        self.data.columns = col_names
        self.compute_BigF()
        self.compute_f2a_f2b()
        print("Initializing DataDriver with: {}".format(self.fname))
        print_number(self.clock_rate, "Clock rate (Hz)")
        print_number(self.filesize, "Filesize (Gb)")
        self.ytick_val = [10**i for i in range(6)]  # don't show 10^{-1}
        self.window = 50

    def file_to_dataframe(self):
        """
        param:   filename:    string: location of data file
        return:        df: DataFrame
                       freq, sampling frequency
        """

        with open(self.path, 'r') as file_handle:
            line_one = file_handle.readline()
            match = re.search(r"\d+$", line_one)
            if match:
                clock_rate = int(match.group())
                # print("Clock rate: {} Hz".format(clock_rate))
            else:
                clock_rate = 0
                print("Did not find clock rate")

        # note: after a quick back of the envelope calculation, chunks etc. are only
        # necessary if we leave it running for days
        # approx 12MB in half hour means we'd need O(80) half hours, or O(40) hours
        # to get a single GB
        # this was probably unecessary?
        statinfo = os.stat(self.path)
        chunk_threshold = 1.  # gigabyte
        self.filesize = statinfo.st_size / 1e9  # in gigabytes

        read_data = partial(pd.read_csv, self.path,
                            skiprows=self.no_header - 1)

        if self.filesize < chunk_threshold:
            data = read_data()
            data = clean_time(data)
        else:
            print("File too big; reading chunks")
            # at 13.8MB/181440 entries = 7.6e-5 MB/entry = 7.6e-8 GB/entry
            # so we'd need about 1.3e7 entries for 1 GB of data, so 5e6 seems a
            # reasonable chunksize - read slightly less than a Gb into memory
            data = read_data(chunksize=5000000)
            chunk_list = []
            for chunk in data:
                clean_chunk = clean_time(chunk)
                chunk_list.append(clean_chunk)
            data = pd.concat(chunk_list)

        self.data = data
        self.clock_rate = clock_rate

    def compute_BigF(self):
        """
        compute fraction of total single photon counts that are coincidences:
        frac{AB}{A+B}
        """
        if self.data is None:
            print("self.data is none")
        try:
            self.BigFAsFuncOfTime = self.data['AB Counts'] / \
                (self.data['B Counts'] + self.data['A Counts'])
            self.TotalBigF = self.data['AB Counts'].sum(
            ) / (self.data['B Counts'].sum() + self.data['A Counts'].sum())
        except BaseException:
            print("Ran into error. Could not compute Big F. Continuing")

    def compute_f2a_f2b(self):
        """
        compute frac{AB}{A} and frac{AB}{B} and make sure these are equal
        """
        try:
            self.Frac2a = self.data['AB Counts'].sum(
            ) / self.data['A Counts'].sum()
            self.Frac2b = self.data['AB Counts'].sum(
            ) / self.data['B Counts'].sum()
        except BaseException:
            print("Ran into error computing AB/A and AB/B. Continuing")

    def generate_table(self, outtablename,
                       cols=['A', 'B', 'AB'],
                       generateTable=True):
        """
        outtablename - name for output file containing latex table with info for
        columns
        cols         - list of column names for which to compute statistics
        """
        if generateTable:
            new_indices = ['time (s)', 'mean counts']
            for idx in self.data[cols].describe().index[2:]:
                new_indices.append(idx)
            outTable = self.data[cols].describe()\
                .set_index(pd.Index(new_indices))
            outTable.to_latex(
                self.tables_dir + outtablename + ".tex", float_format="%d")
        print("Outtable: ", outTable)

    def print_fractions(self):
        print_number(self.TotalBigF, "AB/(A+B)")
        print_number(self.Frac2a, "AB/A")
        print_number(self.Frac2b, "AB/B")

    def plot_channels(self, title="", cols=['Ch 1', 'Ch 2', 'Ch 3'],
                      outFileName="", ax=None):
        """
        Title - title for plot
        cols  - columns/channels to plot

        if title is passed, save as png

        returns the plotted ax
        """
        try:
            if ax is not None:
                self.data.plot(y=cols, ax=ax, title=title)
            else:
                ax = self.data.plot(y=cols, figsize=self.figsize, title=title)

            ax.set_yscale('log')
            ax.grid(True)
            ax.set_ylim(0.1, 1e5)
            ax.set_yticks(self.ytick_val)
        except KeyError:
            print("Key Error trying to plot a column using an invalid label. Exiting")
            sys.exit()
        ax.legend()
        if outFileName is not "":
            plt.savefig(
                self.writeup_dir +
                outFileName +
                ".png",
                format='png',
                dpi=100,
                bbox_inches='tight')
        ax.set_ylabel("counts/s")
        return ax

    def plot_rolling_average(self):
        rolling_mean = self.data.rolling(window=self.window).mean()
        rolling_mean.plot()


if __name__ == "__main__":
    fname = "test2_feb_13"
    test_driver = DataDriver(fname)
    test_driver.print_fractions()
    test_driver.generate_table("")
    test_driver.plot_channels(cols=['Ch 1', 'Ch 2', 'Ch 3'])
    plt.show()
