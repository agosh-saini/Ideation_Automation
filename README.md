# Square Wave Electrochemical Sensing Data Analysis Software

## Motivation

Square Wave Voltammetry (SWV) is a powerful electrochemical technique used electrochemical biosensors designed to detect biomarker and other analytes. In this kind of biosensing usually  a significant  amounts of SWV data is generated, leading to researchers spending significant amounts of time in data formatting and analysis. The manual analysing of data limits the number of experiments that an individual researcher is able to perform. The Ideation Automation program is designed to help researcher in analysing SWV data. It extracts relevant points in the SWV data, generates a summary of all the values found in any specific channel of interest, and automatically generate a labeled graph with peak values. This program can significantly increase the research productively of projects utilizing SWV.

## Programming Decisions
1.	**User-Centric Design**: The program is designed with enough flexibility to ensure it can parse and remove additional information often attached to output files from different systems. The manual entry of “headers” and “blank lines” allows the user to adjust how the program parses and remove information to meet the needs of their specific system.

2.	**Data Handling and Processing**: The program automatically extracts the columns of interests and graphs the said data. The smoothing value allows for noise removal from the signal and the program can be used to determine both peaks and troughs in the data.

3.	**Automation of Analysis**: A core decision in the program's development was the automation of peak detection and data summarization. This involves setting thresholds for peak detection, which is project dependent and needs to be determined using trial and error. The program is designed to create summary documents of every step in both excel format the figure format. This allows for the user to be able to report both values if needed.

4.	**Customizability and Flexibility**: Recognizing that SWV experiments can vary significantly, the program is designed to be customizable. Functions can easily be added to python class. The use of “PySimpleGUI” module further simplifies the customization as this module allows of easy addition of inputs. 

5.	**Efficient Workflow Integration**: The program's ability to automate the generation of figures and summary documents directly into the data folder aligns with the goal of productivity increase for researcher. The summary and the figure folders are saved in the same folder as the data, ensuring that data summaries are easy to locate and associate with raw data. 

6.	**Batch Files for Additional Automation**: Batch files “Automation_SW.bat” automatically runs the python scripts so the applications can easily used without going through an Integrated Development Environment or the Command Line. 

## Conclusion

The development of the SWV automation application is designed to increase research and development productivity for individuals generating and analysing large amounts of data. The application should help reduce hours of data preparation with novel research.

## Usage Steps

Please refer to Usage_Steps.pdf usage steps. The document contains screenshots of the software GUI for easier usage. 

## Installation

**Step 1**: Download the zip file  **dist.zip** from the **Release** tab \
**Step 2**: Extract the zip file in the desired location \
**Step 3**: To run, click **Ideation Automation.bat** file \

*Note: This method only works on Windows computers, for Mac or Linux operating systems, some modidifications may be required to the python files* \


## Running Through Python Files

**Step 1**: clone the repository \
**Step 2**: Move repository folder to desired location \
**Step 3**: To run, click **main.py** file  \

## Rebuilding Executable using pyinstaller

**Step 1**: Install PyInstaller using pip 
```
    pip install -U pyinstaller
```
**Step 2**: Ensure repository and **main.spec** file are present \
**Step 3**: Run the following command 
```
    pyinstaller main.spec
```
**Step 4**: Run the **main.exe** file found in the dist folder \

## Main Functions in Class

**Automate_SW.bat**: This file automates runs the relevant executable files \
**merge.bat**: this file merges all the comma-separated files generated for individual experiments \
**ideation_automation_ec (class)**: Class with all the functions associated with automation \
**convert.csv()**: function for converting text file normally outputted to comma-separated files \
**get_header_line()**: function that removes all the meta-data available in files to prepare for analysis \
**plot_res()**: function that takes cleaned data and graphs the results. This can detect peaks using two methods using either derivatives or can detect peaks using scipy module where a Gaussian curve is fitted to the peaks to determine the peak values.

## Acknowledgements

This work was done as part of my time at IDEATION lab under Dr. Mahla Poudineh. ChatGPT was used for resolving errors while creating the files.

## Citation Information

Please cite this package if it was used in your work. Information for citation can be found below: \
Name - Agosh Saini, Fatemeh Keyvani Mahla Poudineh \
Contact - contact@agoshsaini.com \
Year of publication - 2023 \
Title - Square Wave Electrochemical Sensing Data Analysis Software\
