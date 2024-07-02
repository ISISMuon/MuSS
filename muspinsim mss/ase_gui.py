"""
Project: Simulations for muSR data Analysis Industrial Placement
Author: Paula Franco
Date: August 2023

Summary:
tkinter is used to create a Gui where the cif file is explored including
the changes done to
"""

import tkinter as tk
from tkinter.ttk import Label, LabelFrame
import pandas as pd
from muspinsim import MuSpinInput, ExperimentRunner
from muspinsim.input.keyword import *
from ase import io, Atoms, Atom


muon = Atom('X', [0, 0, 0], charge=1)

alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'k', 'l',
            'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'z']
listinha = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12,
            13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23]


def table(root, lst):
    dicc = {}
    total_rows = len(lst)
    total_columns = len(lst[0])
    for i in range(total_rows):
        for j in range(total_columns):
            dicc[listinha[j]] = tk.Entry(root, width=40)
            entry = tk.Entry(root, width=40)
            entry.grid(row=i, column=j)
            entry.insert('end', lst[i][j])


cif_red = io.read(r'c:\Users\BNW71814\Desktop\EntryWithCollCode60559.cif')
cif_red.get_positions()


def cif_data():
    cif_red.get_positions()
    cif_red.get_chemical_symbols()

    lst = []
    for i in range(cif_red.get_global_number_of_atoms()):
        lst_tuple = (cif_red.get_chemical_symbols()[
                     i], cif_red.get_positions()[i])
        lst.append(lst_tuple)

    return lst

    frame = LabelFrame(new)
    frame.grid(row=0, column=0, padx=5, pady=5)
    tk.Label(frame, text="FRAME 1").grid()

    btn = tk.Button(frame, command=lambda: table(
        frame, cif_data()), text='botton').grid()


# Position stuff
pos = cif_red.get_positions()
pos[3] = [0.1, 0.1, 0.1]
pos[7:, 0] = 9
cif_red.set_positions(pos)

# Altering particales in system
cif_red.append(muon)
dist = cif_red.get_all_distances()

# Visualistation
# visualize.view(cif_red)

# Data stuff
dictOfInfo = cif_red.todict()
# print(dictOfInfo)
dictOfInfo.pop('cell')
dictOfInfo.pop('info')
dictOfInfo["positions"] = [(pos[0], pos[1], pos[2])
                           for pos in dictOfInfo["positions"]]

dataframe = pd.DataFrame.from_dict(dictOfInfo, orient="index")


def cif_filee(self, path, position_mu):
    # Self contained version of cif_file
    read_doc = io.read(path)
    position = read_doc.get_positions()
    reltv_position = []
    for i in position:
        i = i+position_mu
        reltv_position.append(i)

    with open(self.input, 'a+') as f:
        # f.write(' {0} \n spins \n    {1} '.format(self.name))
        for j in read_doc.get_chemical_symbols():
            f.write(' {0} '.format(j))
        number = 0
        for i in reltv_position:
            # print(number)
            # print('I am i in anna', i)
            f.write('\n dipolar 1 {0}\n   '.format(number+2))
            f.write('')
            number += 1
            for ii in i:
                f.write(str(ii))
                f.write(' ')
            f.writelines('\n')


df = pd.DataFrame(columns=['chemica;symbols', 'position', 'position to muon'])
cif_red.get_positions()[0:, 0] = 0

material = {'Chemical symbols': cif_red.get_chemical_symbols(), 'x_position': cif_red.get_positions(
)[:, 0], 'y_position': cif_red.get_positions()[:, 1], 'z_position': cif_red.get_positions()[:, 2]}


df = pd.DataFrame(material)
