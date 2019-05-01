from DataDriver import DataDriver
import matplotlib.pyplot as plt

if __name__ == "__main__":
    with plt.style.context("lab1.mplstyle"):
        fname1 = "Feb_20_Run_1_BS"
        fname2 = "Feb_20_Run_2_BS"
        title = 'BC Coincidences with Beam Splitter'
        plotName = "bc_coinc_with_bs"
        col_names = ['A', 'B', 'AB',
                     'AC', 'BC', 'ABC']
        beam_splitter_driver1 = DataDriver(fname1,
                                           col_names=col_names)

        beam_splitter_driver2 = DataDriver(fname2,
                                           col_names=col_names)
        fig, ax = plt.subplots(1, figsize=beam_splitter_driver1.figsize)

        # cut beam splitter Run 1 to same size as Run 2
        beam_splitter_driver1.data =\
            beam_splitter_driver1.data[beam_splitter_driver1.data.index <
                                       beam_splitter_driver2.data.index[-1]]

        beam_splitter_driver1.plot_channels(
            title=title, cols=['BC'], outFileName=plotName,
            ax=ax)
        beam_splitter_driver2.plot_channels(
            title=title, cols=['BC'], outFileName=plotName,
            ax=ax)
        # plt.show()
        # trigger plots
