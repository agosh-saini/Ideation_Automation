# -------- Imports --------- #
# Importing libraries 
import matplotlib.pyplot as plt
import numpy as np

# Importing functions from libraries
from pandas import DataFrame, read_csv
from os import mkdir, remove, rename
from os.path import exists as path_exists
from shutil import copy
from re import sub
from itertools import islice
from datetime import datetime
from scipy.signal import find_peaks, peak_prominences
from typing import Optional, Tuple, Union
# -------- Imports END --------- #

# -------- Docstring --------- #
"""
Author: Agosh Saini
Website: agoshsaini.com
Contact: contact@agoshsaini.com

IDEATION Lab Contact: mahla.poudineh@uwaterloo.ca

Description:
    Inputs:
        - txt file of electrochemical data
        - Copy Paste All Headers in CSV Format
        - Seperator (tab/comma)
        - If we want graphs or not
        - Blank Lines between headers and data
        - List of columns of interests in array format [0,1,2 ....]
        - Number of points used for smoothing
        - If graphs are wanted
        - Threshold (min height of the peaks/valleys)
        - Min Height (which is the DC bias for the peak)
    Outputs:
        - Graphs the data if selected
        - result max/min value
        - height of the peaks

"""
# -------- Docstring END --------- #

# -------- Class --------- #


class ideation_ec_automation:

    def __init__(self, source: str, filename: str) -> None:
        """
        Initialize the ideation_ec_automation class.

        Parameters:
        - source (str): The source directory path.
        - filename (str): The name of the file.

        Returns:
        - None
        """
        self.source = source
        self.filename = filename
        self.data = DataFrame()

        if path_exists(source + "\\" + "figures") is False:
            mkdir(source + "\\" + "figures")

        if path_exists(self.source + "\\" + "summary") is False:
            mkdir(self.source + "\\" + "summary")

    def convert_csv(self, location: Optional[str]=None, file: Optional[str]=None) -> str:
        """
        Convert a txt file to a csv file.

        Parameters:
        - location (str, None): The location to copy the file to. If None, use self.source.
        - file (str, None): The name of the file to convert. If None, use self.filename.

        Returns:
        - str: The path of the exported csv file.
        """
        if location is None:
            location = self.source
        if file is None:
            file = self.filename

        file_path = self.source + '\\' + file
        self.filename = self.filename.replace('.txt', '') + '.csv'
        self.filename = self.filename.replace(',', '')
        export_path = location + '\\' + self.filename

        copy(file_path, export_path)
        remove(file_path)

        return export_path

    def get_header_line(self, head: Union[bool, str]=False) -> int:
        """
        Get the line number of the header in the txt file.

        Parameters:
        - head (bool, str): The keyword or boolean value to identify the header line. If False, use 'Potential/V'.

        Returns:
        - int: The line number of the header.
        """
        if head is False:
            head = 'Potential/V'

        count = 0
        file = open(self.source + "\\" + self.filename)
        lines = file.readlines()

        for line in lines:
            if head in line:
                break
            count += 1
        return count

    def format_file_to_csv(self, blank_line: int=1, head: Union[bool, str]=False, column_index: Optional[int]=None) -> None:
        """
        Format the file to a csv file.

        Parameters:
        - blank_line (int): The number of blank lines between data and headers. Default is 1.
        - head (bool, str): Whether to include headers in the csv file. Default is False.
        - column_index (int): The index of the column to include in the csv file. Default is None.

        Returns:
        - None
        """
        skip = self.get_header_line(head=head)
        file = open(self.source + "\\" + self.filename)
        header = islice(file, skip, skip+1)
        content = islice(file, skip + blank_line + 1, None)

        if column_index is not None:
            self.filename = 'f-' + str(column_index) + '-' + self.filename
        else:
            self.filename = 'f-' + self.filename

        out = open(self.source + "\\" + self.filename, 'w')
        out.writelines(header)

        for line in content:
            out.writelines(line)
        out.close()

    def create_df(self) -> DataFrame:
        """
        Create a pandas DataFrame from the csv file.

        Returns:
        - DataFrame: The created DataFrame.
        """
        self.data = read_csv(self.source + "\\" + self.filename, index_col=0)
        return self.data

    def plot_res(self, bounds: Optional[Tuple[float, float]]=None, column: Optional[int]=None,
                 smooth: Union[bool, int]=False, graph: bool=False,
                 threshold: float=1.e-8, min_height: float=1e-7, direction: int=1) -> None:
        """
        Plot the results.

        Parameters:
        - bounds (Optional[Tuple[float, float]]): The bounds of interest on the x-axis. Default is None.
        - column (Optional[int]): The index of the column to plot. Default is None.
        - smooth (Union[bool, int]): Whether to smooth the function. If True, use a default smoothing value of 5. If False, do not smooth. If int, use the specified smoothing value. Default is False.
        - graph (bool): Whether to display the graph. Default is False.
        - threshold (float): The threshold criteria for selecting peaks. Default is 1.e-8.
        - min_height (float): The minimum height of peaks. Default is 1e-7.
        - direction (int): The direction of peaks. Default is 1.

        Returns:
        - None
        """
        x = self.data

        if bounds is not None:
            x = x.loc[x.index.to_series().between(bounds[0], bounds[1])]

        if column is not None:
            x = x.iloc[:, [column]]

        if smooth is not False:
            if smooth is True:
                if type(smooth) is bool: smooth = 5
                if type(smooth) is int: smooth = smooth
            x = x.ewm(span=smooth).mean()

        for i in range(len(x.columns)):
            peaks, _ = find_peaks(direction*x.iloc[:, i].to_numpy(), height=min_height)
            prominences = peak_prominences(-x.iloc[:, i].to_numpy(), peaks)[0]
            filter_arr = [(prominences[i] > threshold) for i in range(len(prominences))]
            filter_arr = np.where(filter_arr)[0]
            peaks = peaks[filter_arr]
            prominences = prominences[filter_arr]

        if graph is True:
            tag = datetime.today().strftime('%Y-%m-%d_%H-%M-%S') + ".png"
            plt.plot(x)

            for i, peak in enumerate(peaks):
                plt.vlines(x=x.index.values[peak], ymin=x.iloc[peak] + prominences[i],
                           ymax=x.iloc[peak], color="C1")
                plt.text(x.index.values[peak], x.iloc[peak] + prominences[i]/2,
                         '{:.2e}'.format(prominences[i]), rotation=90, verticalalignment='center')
            y_values = x.iloc[peaks].values.flatten()
            x_values = x.index.values[peaks]
            plt.plot(x_values, y_values, 'x')

            plt.legend(x.columns)
            plt.xlabel(x.index.name)

            name = self.filename.replace('.csv', '')
            plt.savefig(self.source + "\\" + "figures" + "\\" + "column_" + str(column) + "_" + name + "_" + tag)
            plt.close()

        self.insert_signal(x.iloc[peaks, :], prominences)

    def get_max_min(self, dataframe: Optional[DataFrame]=None, get_max: bool=False) -> int:
        """
        Get the minimum or maximum value from a DataFrame.

        Parameters:
        - dataframe (DataFrame): The DataFrame to get the value from. If empty, use self.data. Default is an empty DataFrame.
        - get_max (bool): Whether to get the maximum value. If False, get the minimum value. Default is False.

        Returns:
        - int: The minimum or maximum value.
        """
        if dataframe is None:
            dataframe = self.data

        if get_max is False:
            return dataframe.min()
        return dataframe.max()

    def get_baseline(self, x: Optional[DataFrame]=None, bounds: Optional[Tuple[float,float]]=None) -> int:
        """
        Get the baseline values between regions.

        Parameters:
        - x (Optional[DataFrame]): The DataFrame to get the baseline from. If empty, use self.data. Default is an empty DataFrame.
        - bounds (Optional[Tuple[float,float]]): The bounds of interest. Default is None.

        Returns:
        - int: The baseline value.
        """
        if None:
            x = self.data

        if bounds is not None:
            x = x.loc[x.index.to_series().between(bounds[0], bounds[1])]

        return x.mean()

    def get_peaks(self, x: np.ndarray, y: np.ndarray, threshold: Optional[float]=None) -> np.ndarray:
        """
        Get the local min/max values from x and y arrays.

        Parameters:
        - x (np.ndarray): The x array.
        - y (np.ndarray): The y array.
        - threshold (Optional[float]): The threshold value for detecting peaks. Default is None.

        Returns:
        - np.ndarray: The array of peak values.
        """
        if threshold is None: threshold = -0.4e-7

        peak_x = np.array([])
        peak_y = np.array([])
        peak_xy = np.array([])

        for k in range(2, len(x)-1):
            if y[k] < y[k - 1]:
                if y[k] < y[k + 1]:
                    if y[k] < threshold:
                        peak_x = np.append(peak_x, x[k])
                        peak_y = np.append(peak_y, y[k])
            peak_xy = np.array([peak_x, peak_y])
        return peak_xy

    def insert_signal(self, peak_y: DataFrame, height: float, location: Optional[str]=None) -> None:
        """
        Insert the peak values into a summary document.

        Parameters:
        - peak_y (DataFrame): The DataFrame of peak values.
        - height (float): The height of the peaks.
        - location (Optional[str]): The location to save the summary document. If None, use self.source + "\\" + "summary" + "\\" + "summary-" + self.filename. Default is None.

        Returns:
        - None
        """
        if location is None:
            location = self.source + "\\" + "summary" + "\\" + "summary-" + self.filename

        existing_file = False

        if path_exists(location):
            existing_file = True

        local_df = peak_y.copy()
        local_df.loc[:, 'height'] = height

        if existing_file:
            local_df.to_csv(location, mode='a')
        else:
            local_df.to_csv(location)

    def convert_deliminator(self, location: Optional[str]=None, file: Optional[str]=None, sep: Optional[str]=None):
        """
        Convert the delimiter of a file.

        Parameters:
        - location (Optional[str]): The location of the file. If None, use self.source. Default is None.
        - file (Optional[str]): The name of the file to convert. If None, use self.filename. Default is None.
        - sep (Optional[str]): The delimiter to use. If None, use ','. Default is None.

        Returns:
        - None
        """
        if sep is None: sep = ','
        
        if location is None:
            location = self.source
        if file is None:
            file = self.filename

        file_path = self.source + '\\' + file
        local_filename = self.filename
        local_filename = local_filename.replace('.txt', '-del.txt')
        local_filename = local_filename.replace(',', '')
        export_path = location + '\\' + local_filename

        with open(file_path, 'r') as my_file:
            with open(export_path, 'w') as csv_file:
                content = islice(my_file, 0, None)
                for line in content:
                    file_content = sub(sep, ", ", line)
                    csv_file.writelines(file_content)

        remove(file_path)
        rename(export_path, file_path)

if __name__ == "__main__":
    path_in = "C:\\Users\\westw\\Documents\\Personal\\Ideation_Automation\\test_case"
    file = "modified_version.txt"
    test = ideation_ec_automation(path_in, file)
    test.convert_deliminator(sep=',')
    test.format_file_to_csv(blank_line=1, head=False)
    test.create_df()
    test.plot_res(column=2, smooth=15, graph=True, threshold=1.e-8, min_height=1.e-7, direction=1, bounds=None)
