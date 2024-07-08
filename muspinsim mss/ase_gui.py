"""
Project: Simulations for muSR data Analysis Industrial Placement
Author: Paula Franco
Date: August 2023

Summary:
tkinter is used to create a Gui where the cif file is explored including
the changes done to
"""

import io
import tkinter as tk
import pandas as pd
import numpy as np
from ase import Atoms, Atom
from ase.gui.images import Images
from ase.gui.gui import GUI
import ase.visualize

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


cif_red = ase.io.read(r'c:\Users\BNW71814\Desktop\EntryWithCollCode60559.cif')
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


# Your existing function modified to use Tkinter

def get_muon_pos_nn_visually(atoms: Atoms):
    """
    Get the muon position by selecting two atoms to be the nearest neighbors (nn).
    :param atoms: ASE atoms of the structure
    :return: (muon position ndarray, list of the index of the atoms the muon is in between)
    """

    def on_close():
        # When the GUI is closed, retrieve the selected atoms and calculate the muon position
        selected = []
        for i_images_selected_atom in range(0, len(images.selected)):
            if images.selected[i_images_selected_atom]:
                selected.append(i_images_selected_atom)
        if len(selected) != 2:
            print("Please select exactly two atoms.")
            return

        pos1 = atoms[selected[0]].position
        pos2 = atoms[selected[1]].position
        muon_pos = (pos1 + pos2) / 2

        result_label.config(
            text=f"Muon location: ({muon_pos[0]:.2f}, {muon_pos[1]:.2f}, {muon_pos[2]:.2f})")

    # Initialize the top level window
    window = tk.Toplevel()
    window.title("Muon Position Selector")

    # Create an Images and GUI instance from ASE
    images = Images()
    images.initialize([atoms])
    GUI(images)

    # Add a button to calculate the muon position
    calculate_button = tk.Button(
        window, text="Calculate Muon Position", command=on_close)
    calculate_button.pack(pady=10)

    # Label to display the result
    result_label = tk.Label(
        window, text="Select two atoms and click the button.")
    result_label.pack(pady=10)

######################################################################################## DRAFT            ##########################
