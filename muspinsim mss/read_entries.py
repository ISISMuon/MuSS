"""
Project: Simulations for muSR data Analysis Industrial Placement
Author: Paula Franco
Date: August 2024

Summary:

"""
import numpy as np
import tkinter as tk
from muspinsim import MuSpinInput, ExperimentRunner
from muspinsim.input.keyword import *
from tkinter.ttk import Label, LabelFrame


def iniciate_params(object_of_class):
    '''
    a muspinInput object is created
    the essential object as name, spin and time are created are created
    '''

    '''
    object_of_class.parameters = MuSpinInput()

    name_entry = KWName(object_of_class.name_entry.get())
    spins_entry = KWSpins(object_of_class.spins_entry.get())
    time_entry = KWTime(
        f'range({object_of_class.time_entry1}, {object_of_class.time_entry2}, {object_of_class.time_entry3})')
     for i in range(len( object_of_class.kEntries)):
        if i==2:
            pass
        else
            value=
            object_of_class.parameters._keywords[]'''
    # ____INCORPORATE IT INTO THE PARAMS

    '''object_of_class.parameters._keywords['name'] = name_entry
    object_of_class.parameters._keywords['spins'] = spins_entry
    object_of_class.parameters._keywords['time'] = time_entry
    object_of_class.parameters._keywords['field'] = KWField(
        object_of_class.field_value.get())
    object_of_class.parameters._keywords['intrinsic_field'] = KWIntrinsicField(
        object_of_class.intrinsic_field.get())
    object_of_class.parameters._keywords['polarization'] = KWPolarization(
        object_of_class.polarization.get())'''

    object_of_class.parameters = MuSpinInput()

    for i in range(22):
        j = object_of_class.labelstring[i]
        k = object_of_class.kEntries[i].get()
        if object_of_class.kEntries[i].get() != '':
            object_of_class.parameters._keywords[j] = create_object_KW(k, i)
    # object_of_class.parameters._keywords['dipolar']={}
    # object_of_class.parameters._keywords['field']=fied_en
    # object_of_class.parameters._keywords[]
    # ________________ Read everything_else_________________________

    for i in range(5):
        dipolar_entry = KWDipolar(block=['0 0 8'], args=(1, i))
        object_of_class.parameters._keywords['dipolar'] = {'': dipolar_entry}


def initialize_simulation_parameters(object_of_class):
    '''
    Initializes the essential simulation parameters by creating a MuSpinInput object 
    and setting up various parameters such as name, spins, and time based on user input.

    Args: handler (object): An instance of a class that manages UI elements and holds parameter values
    '''
    # Create a new MuSpinInput object to hold simulation parameters
    object_of_class.parameters = MuSpinInput()
    
    # Retrieve and set the name, spins, and time entries from the UI
    name_entry = KWName(object_of_class.name_entry.get())
    spins_entry = KWSpins(object_of_class.spins_entry.get())
    time_entry = KWTime(
        f'range({object_of_class.time_entry1.get()}, {object_of_class.time_entry2.get()}, {object_of_class.time_entry3.get()})')

    # Incorporate the retrieved entries into the parameters object
    object_of_class.parameters._keywords['name'] = name_entry
    object_of_class.parameters._keywords['spins'] = spins_entry
    object_of_class.parameters._keywords['time'] = time_entry

    # If a field value is provided, add it to the parameters
    if object_of_class.field_value.get(1.0, tk.END) != '\n':
        print('entered')
        object_of_class.parameters._keywords['field'] = KWField(
            object_of_class.field_value.get(1.0, tk.END))
        
    # If an intrinsic field value is provided, add it to the parameters
    if object_of_class.intrisic_field_value.get(1.0, tk.END) != '\n':
        object_of_class.parameters._keywords['intrinsic_field'] = KWIntrinsicField(
            object_of_class.intrisic_field_value.get("1.0", "end-1c"))

    # If Zeeman values are provided, process and add them to the parameters
    if object_of_class.zeeman_value.get(1.0, tk.END) != '\n':
        zeeman_lines  = extract_lines_from_text_widget(object_of_class.zeeman_value)
        zeeman_dict = {f'zeeman_{i+1}': KWZeeman(
            block=[zeeman_lines [i]], args=[i+1]) for i in range(0, len(zeeman_lines ))}
        print(zeeman_dict)
        object_of_class.parameters._keywords['zeeman'] = zeeman_dict
    
    # If dipolar interactions are provided, process and add them to the parameters
    if object_of_class.dipolar_dic!={}:  
        dipolar_values=list(object_of_class.dipolar_dic.values())
        dipolar_dict = {f'dipolar_{i+2}': KWDipolar(
            block=[dipolar_values[i]], args=(1,i+2)) for i in range(0, len(dipolar_values))}
        object_of_class.parameters._keywords['dipolar'] = dipolar_dict


    # object_of_class.parameters._keywords['x_axis']
    # object_of_class.parameters._keywords['y_axis']
    # object_of_class.parameters._keywords['celio']
    # object_of_class.parameters._keywords['dissipation']
    # object_of_class.parameters._keywords['fitting_varaibles']
    # object_of_class.parameters._keywords['fitting_data']
    # object_of_class.parameters._keywords['fiting_method']
    # object_of_class.parameters._keywords['fitting_tollerance']
    # object_of_class.parameters._keywords['experiment']
    evaluated_params = object_of_class.parameters.evaluate()
    print(evaluated_params['couplings'])


def extract_lines_from_text_widget(text)->list:
    '''
    Extracts all lines of text from a Text widget and returns them as a list.

    Args: text_widget (tk.Text): The Text widget from which to extract lines.
    Returns: list A list containing each line of text as a separate string.
    '''
    # Get the total number of lines in the Text widget
    num_lines = int(text.index('end-1c').split('.')[0])
    lines_list = []

    # Iterate through each line and extract the text
    for line_num in range(1, num_lines + 1):
        line_text = text.get(f"{line_num}.0", f"{line_num}.end")
        lines_list.append(line_text)
        print(f"Line {line_num}: {line_text}")

    return lines_list


def create_object_KW(par, keyword_type):
    ''' 
    Creates and returns an object of a specific keyword type based on the provided integer identifier.

    Args:
        par (str): The parameter value to be used for creating the keyword object.
        keyword_type (int): An integer identifier that specifies the type of keyword object to create.

    Returns:
        object: An instance of a keyword object corresponding to the provided identifier.
    '''
    if keyword_type == 0:
        value = KWName(par)
    if keyword_type == 1:
        value = KWSpins(par)
    if keyword_type == 2:
        value = KWTime(par)
    if keyword_type == 3:
        value = KWField(par)
    if keyword_type == 4:
        value = KWIntrinsicField(par)
    if keyword_type == 5:
        value = KWPolarization(par)
    if keyword_type == 6:
        value = KWAverageAxes(0)
    if keyword_type == 7:
        value = KWOrientation(par)
    if keyword_type == 8:
        value = KWTemperature(par)
    if keyword_type == 9:
        value = KWZeeman(par)
    if keyword_type == 10:
        value = value = KWDipolar(par)
    if keyword_type == 11:
        value = KWQuadrupolar(par)
    if keyword_type == 12:
        value = KWHyperfine(par)
    if keyword_type == 13:
        value = KWXAxis(par)
    if keyword_type == 14:
        value = KWYAxis(par)
    if keyword_type == 15:
        value = KWCelio(par)
    if keyword_type == 16:
        value = KWDissipation(par)
    if keyword_type == 17:
        value = KWFittingVariables(par)
    if keyword_type == 18:
        value = KWFittingData(par)
    if keyword_type == 19:
        value = KWFittingMethod(par)
    if keyword_type == 20:
        value = KWFittingTolerance(par)
    if keyword_type == 21:
        value = KWExperiment(par)
    return value
