from DataDriver import DataDriver
import matplotlib.pyplot as plt

if __name__ == "__main__":
    with plt.style.context("lab1.mplstyle"):
        fname = "Feb_20_Noise_Floor"
        title = 'Noise Floor'
        plot_name = "noise_floor_channels"
        noise_data_driver = DataDriver(
            fname, col_names=[
                'A Counts', 'B Counts', 'AB Counts'])
        noise_data_driver.plot_rolling_average()

        plt.show()
