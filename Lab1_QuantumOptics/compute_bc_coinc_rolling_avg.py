from DataDriver import DataDriver
import matplotlib.pyplot as plt

if __name__ == "__main__":
    fname1 = "Feb_20_Run_1_BS"
    fname2 = "Feb_20_Run_2_BS"
    plotName = "bc_coinc_with_bs"
    col_names = ['A Counts', 'B Counts', 'AB Counts',
                 'AC Counts', 'BC Counts', 'ABC Counts']
    beam_splitter_driver1 = DataDriver(fname1,
                                       col_names=col_names)

    beam_splitter_driver2 = DataDriver(fname2,
                                       col_names=col_names)
    # cut beam splitter Run 1 to same size as Run 2
    beam_splitter_driver1.data =\
        beam_splitter_driver1.data[beam_splitter_driver1.data.index <
                                   beam_splitter_driver2.data.index[-1]]

    beam_splitter_driver1.plot_rolling_average()
    plt.show()
