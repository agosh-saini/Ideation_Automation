# ------- IMPORTS --------- #
from ideation_ec_automation import ideation_ec_automation
from os import listdir
from os.path import isfile, join
import PySimpleGUI as sg
from ast import literal_eval
# ------- IMPORTS END --------- #

# ------- SCRIPT --------- #
if __name__ == '__main__':

    # Selecting the theme of the UI
    sg.theme('Black')

    # the layout of the UI (with inputs)
    layout = [[sg.Text('Extracting Information from EC Data')],
              [sg.Text('User Folder'),sg.Input(key='path'),
               sg.FolderBrowse(target='path')],
              [sg.Text('Headers'), sg.InputText(key='header')],
              [sg.Text('Seperator')],
              [sg.Listbox(values=list(['Comma', 'Tab']), size=(10, 5), key='seperator')],
              [sg.Text('Blank Lines'), sg.InputText(key='blank')],
              [sg.Text('List Columns'), sg.InputText(key='column')],
              [sg.Text('Smooth Value'), sg.InputText(key='smooth')],
              [sg.Text('Graph'), sg.Text()],
              [sg.Checkbox('Yes', default=True, key='graph')],
              [sg.Text('Threshold'), sg.InputText(key='thres')],
              [sg.Text('Min Height'), sg.InputText(key='height')],
              [sg.Text('Check for Peak, Leave Unchecked for Valley'), sg.Text()],
              [sg.Checkbox('Get Peaks', default=False, key='peak')],
              [sg.Button('Ok'), sg.Button('Cancel')]]

    # Create the Window
    window = sg.Window('IDEATION LAB', layout)

    # Event Loop to process "events" and get the "values" of the inputs
    while True:
        event, values = window.read()

        # if user closes window or clicks cancel or clicks ok -> exit
        if event == sg.WIN_CLOSED or event == 'Cancel' or event == "Ok":
            break
    # close the window
    window.close()

    # get the path of the folder
    path = values['path']

    # get all the files in the directory
    files = [f for f in listdir(path) if isfile(join(path, f))]

    # determines if peaks or valleys are desired
    if values['peak'] is False:
        direction = -1
    else:
        direction = 1

    # repeat for all the files we have
    for file in files:
        test = ideation_ec_automation(path, file)

        # change the seperator
        if values['seperator'] == ['Tab']:
            test.convert_deliminator(sep='\t')

        # remove metadata
        test.format_file_to_csv(blank_line=int(values['blank']),
                                head=values['header'])
        # convert the txt file to csv
        test.convert_csv()

        # create the pandas dataframe
        df = test.create_df()

        # look for peaks and get the graphs
        test.plot_res(column=literal_eval(values['column']),
                      smooth=float(values['smooth']), graph=values['graph'],
                      threshold=float(values['thres']),
                      min_height=float(values['height']),
                      direction=direction)

    # -------- SCRIPT END ------------- #

    # following is the test inputs for test data

    # Potential/V
    #smooth = 15
    #graph = True
    #threshold = 1.e-8
    # min_height = 1.e-7
    # column = [3]
