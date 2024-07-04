# EC Sensing Data Analysis Application
This application can be used to automate data analysis, graph generation, and data summarization tasks with most forms of Electrochemical Data. A video explaining how to use the software can be found by [clicking here](https://www.loom.com/share/7880c0045b4042feadb9aec0fff77dee).

## Installation
Step 1: Download [Automate_SW_v1.zip](https://github.com/agosh-saini/Ideation_Automation/blob/master/Automate_SW_v1.zip) \
Step 2: Extract the zip file into a folder with no other files \
Step 3: To run, click **Automate_SW.bat** file 

## Explanation of main functions
**Automate_SW.bat**: This file automates runs the relevant executable files \
**merge.bat**: this file merges all the comma-separated files generated for individual experiments \
**ideation_automation_ec (class)**: Class with all the functions associated with automation \
**convert.csv()**: function for converting text file normally outputted to comma-separated files \
**get_header_line()**: function that removes all the meta-data available in files to prepare for analysis \
**plot_res()**: function that takes cleaned data and graphs the results. This can detect peaks using two methods using either derivatives or can detect peaks using scipy module where a Gaussian curve is fitted to the peaks to determine the peak values.

*Note: This method only works on Windows computers, for Mac or Linux operating systems, please use Python files.*

## Acknowledgements
This work was done as part of my time at IDEATION lab under Dr. Mahla Poudineh. ChatGPT was used for resolving errors while creating the files.

## Citation Information
Please cite this package if it was used in your work. Information for citation can be found below: \
Name - Agosh Saini\
Contact - contact@agoshsaini.com \
Year of publication - 2023 \
Title - EC Sensing Data Analysis Application\
