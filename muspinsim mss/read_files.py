"""
Project: Simulations for muSR data Analysis Industrial Placement
Author: Paula Franco
Date: July 2024

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
# --------------------------------------
#       Homemade scripts
# -------------------------------------
'''
1- name                                 MuSpinKeyword
2- spins                                MuSpinKeyword
3- time                                 MuSpinExpandKeyword

4- field                                MuSpinExpandKeyword
5- intrinsic_field                      MuSpinExpandKeyword

6- polarization                         MuSpinExpandKeyword
7- average_axis                         MuSpinKeyword
8- orientation                          MuSpinExpandKeyword
9- temperature                          MuSpinExpandKeyword

10- zeeman                             MuSpinCouplingKeyword
11- dipolar                            MuSpinCouplingKeyword
12- quadrupolar                        MuSpinCouplingKeyword
13- hyperfine                          MuSpinCouplingKeyword

14- x_axis                             MuSpinKeyword
15- y_axis                             MuSpinKeyword

16- celio                              MuSpinKeyword
17- dissipation                        MuSpinCouplingKeyword

18- fitting_variables                  MuSpinKeyword    
19- fitting_data                       MuSpinExpandKeyword    
20- fitting_method                     MuSpinKeyword
21- fitting_tollerance                 MuSpinKeyword

22- experiment                         MuSpinKeyword
...                                    MuSpinKeyword from KWExperiment
'''


def read_variables(object_of_class):
    '''From the parameters we return the visualized form in GUI
    To facilitate redability i_params is used instead'''
    # Ideally the for loops are standarized to be functions called

    i_params = object_of_class.parameters.evaluate()
    couplings = ['dipolar', 'zeeman',
                 'quadrupolar', 'hyperfine', 'dissipation']

    list_result = [item for item in list(
        object_of_class.parameters._keywords.keys()) if item not in couplings]

    for i in list_result:
        ii = str(i_params[i].value[0]).replace('[', '').replace(']', '')

    read_essential_frame(object_of_class, i_params)

    # -----------------------------------------
    #               Field              #
    field = str(i_params['field'].value[0]).replace('[', '').replace(']', '')
    object_of_class.field_value.insert('end', field)
    # ----------------------------------------
    #            Intrinsic_Field          #
    intrisic_field = str(i_params['intrinsic_field'].value[0]).replace(
        '[', '').replace(']', '')
    object_of_class.intrisic_field_value.insert('end', intrisic_field)

    # ---------------------------------------
    #             Polarization             #
    polarization = str(i_params['polarization'].value[0]).replace(
        '[', '').replace(']', '')
    object_of_class.polarization_value.insert('end', polarization)

    # ---------------------------------------
    #             Polarization             #
    polarization = str(i_params['polarization'].value[0]).replace(
        '[', '').replace(']', '')
    object_of_class.polarization_value.insert('end', polarization)


def read_essential_frame(object_of_class, i_params):
    # ---------------------------------------
    #               Name               #
    object_of_class.name_entry.delete(0, 'end')
    object_of_class.name_entry.insert('0', str(i_params['name'].value[0][0]))

    # -----------------------------------
    #               Spin               #
    object_of_class.spins_entry.delete(0, 'end')
    spins_str = ''
    count = 0
    for i in i_params['spins'].value[0]:
        # print(i)
        if count == 0:
            spins_str = i
        else:
            spins_str = spins_str+' '+i
        count = count+1

    object_of_class.spins_entry.insert('0', spins_str)

    # -----------------------------------
    #               Time               #
    object_of_class.time_entry1.delete(0, 'end')
    object_of_class.time_entry2.delete(0, 'end')
    object_of_class.time_entry3.delete(0, 'end')

    object_of_class.time_entry1.insert(
        'end', str(i_params['time'].value[0][0]))
    object_of_class.time_entry2.insert(
        'end', str(i_params['time'].value[-1][0]))
    object_of_class.time_entry3.insert(
        'end', str(len(i_params['time'].value)))


def read_couplings(object_of_class, i_params):
    pass


def read_fields_more(object_of_class, i_params):
    field = str(i_params['field'].value[0]).replace('[', '').replace(']', '')
    object_of_class.field_value.insert('end', field)


def read_fittings():
    pass


def translation(object_of_class):
    object_of_class.parameters.evaluate()

    pass
