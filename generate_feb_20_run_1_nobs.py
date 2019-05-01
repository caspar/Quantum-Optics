from DataDriver import DataDriver
import matplotlib.pyplot as plt

if __name__ == "__main__":
    fname = "Feb_20_Run_1_NoBS"
    outtablename = "nobs_photon_counts"
    noise_data_driver = DataDriver(fname)
    noise_data_driver.generate_table(outtablename)
