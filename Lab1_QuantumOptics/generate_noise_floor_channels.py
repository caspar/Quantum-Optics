from DataDriver import DataDriver
import matplotlib.pyplot as plt

if __name__ == "__main__":
    fname = "Feb_20_Noise_Floor"
    outtablename = "noise_floor_table"
    noise_data_driver = DataDriver(fname)
    noise_data_driver.generate_table(outtablename)
