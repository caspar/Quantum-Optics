from DataDriver import DataDriver
import matplotlib.pyplot as plt
import pandas as pd

if __name__ == "__main__":
    fname1 = "Feb_20_Run_1_BS"
    fname2 = "Feb_20_Run_2_BS"
    col_names = ['A', 'B', 'AB',
                 'AC', 'BC', 'ABC']
    beam_splitter_driver1 = DataDriver(fname1,
                                       col_names=col_names)

    beam_splitter_driver2 = DataDriver(fname2,
                                       col_names=col_names)

    beam_splitter_driver1.data =\
        beam_splitter_driver1.data[beam_splitter_driver1.data.index <
                                   beam_splitter_driver2.data.index[-1]]

    # outtablename2 = "acounts_bcounts_with_bs"
    outtablename1 = "bc_coinc_with_bs"
    full_data = pd.concat(
        [beam_splitter_driver1.data, beam_splitter_driver2.data])
    beam_splitter_driver1.data = full_data
    beam_splitter_driver1.generate_table(outtablename1,
                                         cols=['A', 'B', 'AB', 'BC'])
    # beam_splitter_driver1.generate_table(outtablename2,
    # cols=['AB', 'BC'])
