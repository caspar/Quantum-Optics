from DataDriver import DataDriver
import matplotlib.pyplot as plt

if __name__ == "__main__":
    with plt.style.context("lab1.mplstyle"):
        fname = "Feb_20_Run_1_NoBS"
        title = 'Photon Counts'
        plotName = "feb_20_run_1_nobs"
        beam_splitter_driver = DataDriver(fname)
        fig, ax = plt.subplots(1, figsize=beam_splitter_driver.figsize)

        beam_splitter_driver.data = beam_splitter_driver.data.iloc[:590, :]
        beam_splitter_driver.plot_channels(
            title=title,
            cols=[
                'A',
                'B',
                'AB'],
            outFileName=plotName,
            ax=ax)
        # plt.show()
