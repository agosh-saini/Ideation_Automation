# -------- Imports --------- #
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os
import shutil
import re
from itertools import islice
from datetime import datetime
from scipy.signal import find_peaks, peak_prominences
# -------- Imports END --------- #

# -------- Docstring --------- #
"""
Author: Agosh Saini
Website: agoshsaini.com
Contact: as7saini@gmail.com

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

    # init function
    def __init__(self, source, filename):
        self.source = source
        self.filename = filename
        self.data = pd.DataFrame()

        if os.path.exists(source + "\\" + "figures") is False:
            os.mkdir(source + "\\" + "figures")

        if os.path.exists(self.source + "\\" + "summary") is False:
            os.mkdir(self.source + "\\" + "summary")

    # this function converts the txt file to csv file
    # makes it easier to work with as well if you want to
    # go through data manually

    def convert_csv(self, location=None, file=None):
        # allows you to change location you copy to
        if location is None:
            location = self.source
        if file is None:
            file = self.filename

        # modify file names so csv is used moving forward
        file_path = self.source + '\\' + file
        self.filename = self.filename.replace('.txt', '') + '.csv'
        self.filename = self.filename.replace(',', '')
        export_path = location + '\\' + self.filename

        # create the copy
        shutil.copy(file_path, export_path)

        # delete original
        os.remove(file_path)

    # this function converts the table in txt file
    # to pandas table. It also saves the metadata
    # in the metadata column as a dictionary (maybe)
    def get_header_line(self, head=False):
        # base case
        if head is False:
            head = 'Potential/V'

        # seeing how many lines to skip during conversion
        count = 0

        # this created an array of lines
        file = open(self.source + "\\" + self.filename)
        lines = file.readlines()

        # check line to see if it contains keywords of headers
        for line in lines:
            if head in line:
                break
            count += 1
        return count

    # This function creates a csv with only values

    def format_file_to_csv(self, blank_line=1, head=False, column_index=None):
        # figure out how many lines to skip
        skip = self.get_header_line(head=head)

        # get headers
        file = open(self.source + "\\" + self.filename)
        header = islice(file, skip, skip+1)

        # get rid of blank row between data and headers
        content = islice(file, skip + blank_line + 1, None)

        # create file with headers
        if column_index is not None:
            self.filename = 'f-' + str(column_index) + '-' + self.filename
        else:
            self.filename = 'f-' + self.filename

        out = open(self.source + "\\" + self.filename, 'w')

        out.writelines(header)

        for line in content:
            out.writelines(line)
        out.close()

    # this function just creates a pandas object
    def create_df(self):
        self.data = pd.read_csv(self.source + "\\" + self.filename, index_col=0)
        return self.data

    # plot the results
    def plot_res(self, bounds=None, column=None, smooth=False, graph=False,
                 threshold=1.e-8, min_height=1e-7, direction=1):

        x = self.data

        # check to see bounds of interests on x-axis
        if bounds is not None:
            x = x.loc[x.index.to_series().between(bounds[0], bounds[1])]

        # check to see the columns of interests
        if column is not None:
            x = x.iloc[:, column]

        # smooths function if needed
        if smooth is not False:
            if smooth is True:
                smooth = 5
            # takes average of surrounding data
            x = x.ewm(span=smooth).mean()

        # this section finds peaks, it then selected the peaks that meet a certain threshold criteria
        # it then filters all the values of the peaks
        for i in range(len(x.columns)):
            # get the peaks and the height of the peak
            peaks, _ = find_peaks(direction*x.iloc[:, i].to_numpy(), height=min_height)
            prominences = peak_prominences(-x.iloc[:, i].to_numpy(), peaks)[0]

            # filter the peaks based on the threshold
            filter_arr = [(prominences[i] > threshold) for i in range(len(prominences))]
            filter_arr = np.where(filter_arr)[0]

            # removing the noise
            peaks = peaks[filter_arr]
            prominences = prominences[filter_arr]

        # plots the results
        if graph is True:
            # tag makes each graph unique so no graph is overwritten
            tag = datetime.today().strftime('%Y-%m-%d_%H-%M-%S') + ".png"

            # plot the x values
            plt.plot(x)

            # plots the peaks and adds the height of the peaks
            for i, peak in enumerate(peaks):
                plt.vlines(x=x.index.values[peak], ymin=x.iloc[peak] + prominences[i],
                           ymax=x.iloc[peak], color="C1")
                plt.text(x.index.values[peak], x.iloc[peak] + prominences[i]/2,
                         '{:.2e}'.format(prominences[i]), rotation=90, verticalalignment='center')
            # plots the peaks as x marks
            y_values = x.iloc[peaks].values.flatten()
            x_values = x.index.values[peaks]
            plt.plot(x_values, y_values, 'x')


            # plot the legend and name the labels
            plt.legend(x.columns)
            plt.xlabel(x.index.name)

            # save the image in the folder named figure
            name = self.filename.replace('.csv', '')
            plt.savefig(self.source + "\\" + "figures" + "\\" + "column_" + str(column) + "_" + name + "_" + tag)
            plt.close()

        # this section saves the peaks in a summary document
        self.insert_signal(x.iloc[peaks, :], prominences)

    # returns the min and max between ranges - Not used in current version
    def get_max_min(self, dataframe=pd.DataFrame(), get_max=False):

        # ensuring the values are set
        if dataframe.empty:
            dataframe = self.data

        # returns min or max between regions
        if get_max is False:
            return dataframe.min()
        return dataframe.max()

    # this function returns the baseline values between regions - not used in current version
    def get_baseline(self, x=pd.DataFrame(), bounds=None):

        # Filling the data
        if x.empty:
            x = self.data

        # Sorting the data
        if bounds is not None:
            x = x.loc[x.index.to_series().between(bounds[0], bounds[1])]

        return x.mean()

    # this following function takes the values of x and y and returns
    # the local min/max values
    # Not used in current version
    def get_peaks(self, x, y, threshold=(-0.4e-7)):
        # sets up numpy arrays for tracking
        peak_x = np.array([])
        peak_y = np.array([])
        peak_xy = np.array([])

        # this checks if the values is a minimum and if the value meets a threshold value
        for k in range(2, len(x)-1):
            if y[k] < y[k - 1]:
                if y[k] < y[k + 1]:
                    if y[k] < threshold:
                        peak_x = np.append(peak_x, x[k])
                        peak_y = np.append(peak_y, y[k])
            # Summarize the value into one array
            peak_xy = np.array([peak_x, peak_y])
        return peak_xy

    # the following function takes all the peaks and inputs that into a csv summary file
    def insert_signal(self, peak_y, height, location=None):
        # set up the file name
        if location is None:
            location = self.source + "\\" + "summary" + "\\" + "summary-" + self.filename

        existing_file = False
        # check if location exists
        if os.path.exists(location):
            existing_file = True

        # makes a local copy to ensure original is not edited
        local_df = peak_y.copy()

        # add the height and then save to csv
        local_df.loc[:, 'height'] = height

        if existing_file:
            local_df.to_csv(location, mode='a')
        else:
            local_df.to_csv(location)

    # the following function allows for the conversion of the tab separated file
    # to comma separated file
    def convert_deliminator(self, location=None, file=None, sep=','):
        # allows you to change location you copy to
        if location is None:
            location = self.source
        if file is None:
            file = self.filename

        # modify file names so csv is used moving forward
        file_path = self.source + '\\' + file
        local_filename = self.filename
        local_filename = local_filename.replace('.txt', '-del.txt')
        local_filename = local_filename.replace(',', '')
        export_path = location + '\\' + local_filename

        # reading given tsv file
        with open(file_path, 'r') as my_file:
            with open(export_path, 'w') as csv_file:
                content = islice(my_file, 0, None)
                for line in content:
                    # Replace every tab with comma
                    file_content = re.sub(sep, ", ", line)
                    # Writing into csv file
                    csv_file.writelines(file_content)

        # delete original
        os.remove(file_path)

        # rename changed file
        os.rename(export_path, file_path)

# -------- Class END --------- #
