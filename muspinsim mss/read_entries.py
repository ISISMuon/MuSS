"""
Project: Simulations for muSR data Analysis Industrial Placement
Author: Paula Franco
Date: August 2024

Summary:

"""
import numpy as np
from tkinter import filedialog
import tkinter as tk
from muspinsim import MuSpinInput, ExperimentRunner
from muspinsim.input.keyword import *
from muspinsim.constants import gyromagnetic_ratio, spin
from tkinter.ttk import Label, LabelFrame
from ase.gui.images import Images
from ase.gui.gui import GUI

import customtkinter
from tkinter import ttk
import ase
from ase import atom, atoms, visualize, build

import copy
import ase
import ase.data
from ase.visualize import view


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


def iniciate_params01(object_of_class):
    '''
    a muspinInput object is created
    the essential object as name, spin and time are created are created
    '''

    object_of_class.parameters = MuSpinInput()

    name_entry = KWName(object_of_class.name_entry.get())
    spins_entry = KWSpins(object_of_class.spins_entry.get())
    # print(f'range({object_of_class.time_entry1.get()}, {object_of_class.time_entry2.get()}, {object_of_class.time_entry3.get()})')
    time_entry = KWTime(
        f'range({object_of_class.time_entry1.get()}, {object_of_class.time_entry2.get()}, {object_of_class.time_entry3.get()})')

    # ____INCORPORATE IT INTO THE PARAMS

    object_of_class.parameters._keywords['name'] = name_entry
    object_of_class.parameters._keywords['spins'] = spins_entry
    object_of_class.parameters._keywords['time'] = time_entry

    print('here is the thing', object_of_class.field_value.get(1.0, tk.END),
          type(object_of_class.field_value.get(1.0, tk.END)), len(object_of_class.field_value.get(1.0, tk.END)))

    if object_of_class.field_value.get(1.0, tk.END) != '\n':
        print('entered')
        object_of_class.parameters._keywords['field'] = KWField(
            object_of_class.field_value.get(1.0, tk.END))

    if object_of_class.intrisic_field_value.get(1.0, tk.END) != '\n':
        object_of_class.parameters._keywords['intrinsic_field'] = KWIntrinsicField(
            object_of_class.intrisic_field_value.get("1.0", "end-1c"))

    '''if object_of_class.polarization_value.get(1.0, tk.END) != '\n':
        object_of_class.parameters._keywords['polarization'] = KWPolarization(
            object_of_class.polarization_value.get("1.0", "end-1c"))'''

    '''if object_of_class.orientation_value.get("1.0", "end-1c") != '\n':
        object_of_class.parameters._keywords['orientation'] = KWPolarization(
            object_of_class.orientation_value.get("1.0", "end-1c"))'''
    # object_of_class.parameters._keywords['temperature'] = KWTemperature(
    #    object_of_class.polarization.get())
    '''if object_of_class.zeeman_value.get("1.0", "end-1c") != '\n':
        object_of_class.parameters._keywords['zeman'] = KWZeeman(
            object_of_class.zeeman_value.get("1.0", "end-1c"))'''

    '''if object_of_class.quadrupolar_value.get("1.0", "end-1c") != '\n':
        object_of_class.parameters._keywords['quadrupolar'] = KWQuadrupolar(
            object_of_class.quadrupolar_value.get("1.0", "end-1c"))'''

    '''if object_of_class.hyperfine_value.get("1.0", "end-1c") != '\n':
        object_of_class.parameters._keywords['hyperfine'] = KWHyperfine(
            object_of_class.hyperfine_value.get("1.0", "end-1c"))'''

    if object_of_class.zeeman_value.get(1.0, tk.END) != '\n':
        print('entered the zeeman')
        # dipolar_entry = KWDipolar(block=['0 0 8'], args=(1, 2))
        # object_of_class.parameters._keywords['dipolar'] = {
        #    '': dipolar_entry}

    if object_of_class.zeeman_value.get(1.0, tk.END) != '\n':
        a = object_of_class.zeeman_value.get("1.0", "end-1c")
        # get_lines(object_of_class.zeeman_value)
        # zeeman = KWZeeman(block=['0 0 20.0/muon_gyr'], args=[1])
        b = get_lines(object_of_class.zeeman_value)
        '''for i in range(1, len(b)):
            # if len(b)

            object_of_class.parameters._keywords['zeeman'][f"zeeman {i}"]._store_values(
                [[get_lines[i]]])
            zeeman = KWZeeman(block=[b[i]], args=[i])
            # zeeman = KWZeeman(block=[a], args=[1])'''
       # object_of_class.parameters._keywords['zeeman'] = {
        #   f'zeeman {i}': KWZeeman(block=[b[i]], args=[i]) for i in range(len(b))}
        ana = {f'zeeman_{i+1}': KWZeeman(
            block=[b[i]], args=[i+1]) for i in range(0, len(b))}
        print(ana)
        object_of_class.parameters._keywords['zeeman'] = ana
    '''dipolar_entry = KWDipolar(block=['0 0 8'], args=(1, i))
    object_of_class.parameters._keywords['dipolar'] = {'': dipolar_entry}'''
    # object_of_class.parameters._keywords['x_axis']
    # object_of_class.parameters._keywords['y_axis']
    # object_of_class.parameters._keywords['celio']
    # object_of_class.parameters._keywords['dissipation']
    # object_of_class.parameters._keywords['fitting_varaibles']
    # object_of_class.parameters._keywords['fitting_data']
    # object_of_class.parameters._keywords['fiting_method']
    # object_of_class.parameters._keywords['fitting_tollerance']
    # object_of_class.parameters._keywords['experiment']
    '''for i in range(5):
        dipolar_entry = KWDipolar(block=['0 0 8'], args=(1, i))
        object_of_class.parameters._keywords['dipolar'] = {'': dipolar_entry}'''
    aa = object_of_class.parameters.evaluate()
    print(aa['couplings'])


def get_lines(text):
    # Get the number of lines in the Text widget
    num_lines = int(text.index('end-1c').split('.')[0])
    listinha = []
    # Iterate through each line and print it
    for line_num in range(1, num_lines + 1):
        line_text = text.get(f"{line_num}.0", f"{line_num}.end")
        listinha.append(line_text)
        print(f"Line {line_num}: {line_text}")

    return listinha


def create_object_KW(par, nn):
    if nn == 0:
        value = KWName(par)
    if nn == 1:
        value = KWSpins(par)
    if nn == 2:
        value = KWTime(par)
    if nn == 3:
        value = KWField(par)
    if nn == 4:
        value = KWIntrinsicField(par)
    if nn == 5:
        value = KWPolarization(par)
    if nn == 6:
        value = KWAverageAxes(0)
    if nn == 7:
        value = KWOrientation(par)
    if nn == 8:
        value = KWTemperature(par)
    if nn == 9:
        value = KWZeeman(par)
    if nn == 10:
        value = value = KWDipolar(par)
    if nn == 11:
        value = KWQuadrupolar(par)
    if nn == 12:
        value = KWHyperfine(par)
    if nn == 13:
        value = KWXAxis(par)
    if nn == 14:
        value = KWYAxis(par)
    if nn == 15:
        value = KWCelio(par)
    if nn == 16:
        value = KWDissipation(par)
    if nn == 17:
        value = KWFittingVariables(par)
    if nn == 18:
        value = KWFittingData(par)
    if nn == 19:
        value = KWFittingMethod(par)
    if nn == 20:
        value = KWFittingTolerance(par)
    if nn == 21:
        value = KWExperiment(par)
    return value
