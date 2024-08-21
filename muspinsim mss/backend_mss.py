"""
Project: Simulations for muSR data Analysis Industrial Placement
Author: Paula Franco
Date: February 2024

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
import os
# --------------------------------------
#       Homemade scripts
# -------------------------------------

from input_class import Create_Input


# -------------------------------------------------------------------------------------------------------
#                                           DATA PROCESSING
# -------------------------------------------------------------------------------------------------------


def data_processing_stored(object_of_class, terminator='Hello'):
    ''' '''  # what does the function do
    xy = object_of_class.result_dic[object_of_class.fitting_variables]
    # print('****************************************')  # debug
    # print(xy, type(xy))  # debug

    data_str_terminator = ' ' + xy + ' value ' + \
        object_of_class.fitting_variables + terminator
    # print(data_str_terminator)  # debug
    return data_str_terminator


def data_processing_xy(object_of_class, terminator='Hello'):

    list_x = []
    for i in range(len(object_of_class.x)):
        list_x.append(object_of_class.x[i][0])

    xy = data_processing(list_x) + ' ' + \
        data_processing(object_of_class.results)

    if object_of_class.fitting_variables == ' ':
        dt_processing_extract_var(object_of_class)

    data_str_terminator = ' ' + xy + ' value ' + \
        object_of_class.fitting_variables + terminator

    object_of_class.fitting_history.append(data_str_terminator)

    object_of_class.result_dic[object_of_class.fitting_variables] = xy
    print('***********************result dic when we are in the send processing',
          object_of_class.result_dic.keys())
    # debug
    return data_str_terminator


def data_processing(data):
    np.set_printoptions(suppress=True)
    # print('ammmm')
    data_string = str(data)
    results_string_1 = data_string.replace('[', '')
    results_string_1 = results_string_1.replace(',', '')
    results_string_2 = results_string_1.replace(']', '')
    resultsToClient = ' '+results_string_2
    return resultsToClient


'''def data_processing_xy(object_of_class, terminator='Hello'):
    data_processing(object_of_class.x)
    data_processing(object_of_class.results)
    xy = data_processing(object_of_class.x) + ' ' + \
        data_processing(object_of_class.results)
    return xy


def data_processing(data):
    np.set_printoptions(suppress=True)
    # print('ammmm')
    data_string = str(data)
    results_string_1 = data_string.replace('[', '')
    results_string_1 = results_string_1.replace(',', '')
    results_string_2 = results_string_1.replace(']', '')
    resultsToClient = ' '+results_string_2
    return resultsToClient'''


def dt_processing_extract_var(object_of_class):
    ''' Here we are extracting the initial variables'''
    '''here we get the variables from the te parameters directly meaning we need fiiting to be equated with variables'''
    # print('ab')
    var = 'field'
    i_params = object_of_class.parameters.evaluate()
    fit_var = i_params[var].value[0]
    # if object_of_class.pvar_fitting_history == []:
    # now that things are new we try only one parameter
    #    object_of_class.pvar_fitting_history.append([float(fit_var), 0, 0])
    #    pass
    if len(fit_var) == 1:
        # object_of_class.pvar_fitting_history.append([float(fit_var), 0, 0])
        fit_var = [float(fit_var), 0, 0]
    elif len(fit_var) == 2:
        # object_of_class.pvar_fitting_history.append(
        #   [float(fit_var[0]), float(fit_var[0]), 0])
        fit_var = [float(fit_var[0]), float(fit_var[0]), 0]

    # i_params[var].valufloat(fit_var), 0, 0]e[0]
    # print('here')
    # fit_var = data_processing(i_params[var].value[0])
    # print(fit_var)
    # print('a')
    # print(fit_var, type(fit_var))
    fit_var = data_processing(fit_var)
    # print(fit_var, type(fit_var))

    object_of_class.fitting_variables = fit_var

    # return fit_var


def clean_whitespace_and_brackets(string: str) -> str:
    result_string = string.replace(
        ']', '').replace('[', '').replace(
        '    ', ' ').replace('   ', ' ').replace('  ', ' ')
    return result_string

# -------------------------------------------------------------------------------------------------------
#                                           File Reading
# -------------------------------------------------------------------------------------------------------


def load_file(object_of_class):

    object_of_class.input_txt_file = filedialog.askopenfilename()
    print(object_of_class.input_txt_file)
    object_of_class.parameters = MuSpinInput(open(object_of_class.input_txt_file))
    read_variables(object_of_class)


def run_simulation(object_of_class):

    experiment = ExperimentRunner(object_of_class.parameters)
    object_of_class.results = experiment.run()


def get_path(object_of_class):
    '''
    Returns the path where the txt file will be saved
    '''
    '''
    Returns the path where the txt file will be saved
    '''
    object_of_class.name_entry.configure()
    path = object_of_class.username + '\Documents' + \
        '/'+object_of_class.name_entry.get()+'.txt'
    # print('This is the name of the txt that could be created', path)
    # print('This is the name of the txt that could be created', path)
    return path


def create(object_of_class):
    """Here we are creatingf a new input file """
    inn = object_of_class.inn
    inn.name = object_of_class.name_entry.get()
    inn.spins = object_of_class.spins_entry.get()
    if object_of_class.time_entry1.get() != '' and object_of_class.time_entry2.get() != '' and object_of_class.time_entry3.get() != '':
        inn.times = f'range({object_of_class.time_entry1.get()},{object_of_class.time_entry2.get()},{object_of_class.time_entry3.get()})'
    inn.cif = False

    inn.zeeman = object_of_class.zeeman_value.get("1.0", "end-1c")
    print(inn.zeeman)
    inn.dipolar = object_of_class.dipolar_value.get("1.0", "end-1c")
    inn.hyperfine = object_of_class.hyperfine_value.get("1.0", "end-1c")
    inn.quadripolar = object_of_class.quadrupolar_value.get("1.0", "end-1c")
    inn.field = object_of_class.field_value.get("1.0", "end-1c")
    inn.intrisic_field = object_of_class.intrisic_field_value.get(
        "1.0", "end-1c")
    inn.celio = object_of_class.celio_value.get("1.0", "end-1c")

    inn.fitting_tolerance = object_of_class.fitting_tolerance_value.get()
    inn.fitting_variables = object_of_class.fitting_variables_values.get(
        "1.0", "end-1c")
    inn.fitting_method = object_of_class.fitting_method.get()

    inn.orientation = object_of_class.orientation_value.get("1.0", "end-1c")
    inn.polarization = object_of_class.polarization_value.get("1.0", "end-1c")
    inn.experiment = None

    inn.x_axis = object_of_class.x_axis_value.get()
    inn.y_axis = object_of_class.y_axis_value.get()

    inn()


def save_as(object_of_class):
    name = filedialog.askdirectory()
    object_of_class.save_path.set(name)
    print(name)
    print(object_of_class.save_path.get())
    # save_path.config()


def graph_update(object_of_class):

    # clean_graph

    # clean_graph
    object_of_class.a.clear()
    timefrom = float(object_of_class.time_entry1.get())
    timeto = float(object_of_class.time_entry2.get())
    timedivision = float(object_of_class.time_entry3.get())
    # object_of_class.a.plot(np.linspace(
    #    timefrom, timeto, timedivision), object_of_class.results)
    object_of_class.a.plot(object_of_class.parameters.evaluate()[
                           'time'].value, object_of_class.results)
    object_of_class.canvas.draw()
    # object_of_class.x = np.linspace(0, 32, 100)
    # object_of_class.x = np.linspace(timefrom, timeto, timedivision)
    object_of_class.x = object_of_class.parameters.evaluate()['time'].value


def parameters_initialize(object_of_class):
    object_of_class.parameters = MuSpinInput()

    # call the
    pass


def read_gui_vaiables(input_object):
    # ___________ Essential frame
    if type(input_object) == MuSpinInput:
        print('banana')
        # here everything is read and transformed t
    pass
# --------------------------------------------------------------------------------------------------------------------
#                                                     CIF FILE
# --------------------------------------------------------------------------------------------------------------------


def selecting__nn_indices(object_of_class):
    ''' Recognize the elemets selected in the ase viewer'''

    # create the list where the selected atoms are stored
    selected = []
    for i_images_selected_atom in range(0, len(object_of_class.images.selected)):
        if object_of_class.images.selected[i_images_selected_atom]:
            selected.append(i_images_selected_atom)

    # exict the initial view
    object_of_class.gui.exit()

    object_of_class.images_with_muon = Images()
    object_of_class.images_with_muon.initialize(
        [add_muon_to_aseatoms(object_of_class, nn_indices=selected)])
    object_of_class.gui_with_muon = GUI(object_of_class.images_with_muon)
    object_of_class.gui_with_muon.run()
    # view(add_muon_to_aseatoms(object_of_class, nn_indices=selected))


def add_muon_to_aseatoms(object_of_class, theta: float = 180, phi: float = 0, nn_indices: list = None,
                         muon_position: np.ndarray = None, plane_atom_index: int = None,
                         plane_atom_position: np.ndarray = None, midpoint=0.5) -> atoms:
    """
    adds a muon to ase_atoms
    :param ase_atoms: ASE atoms of the crystal the muon is going to be placed into
    :param theta: F--mu--F angle in degrees. Must also define nn_indices if this is not 180deg.
    :param phi: angle of the F--mu--F plane. Must also define theta and nn_indices to use this.
    :param nn_indices: ASE index of the nearest-neighbour atoms to place the muon in between. Do not define this AND
                       muon_position
    :param muon_position: position of the muon, in angstroms. Use EITHER this or nn_indices. Do not define this and
                          theta and phi
    :param plane_atom_index: index of atom which the muon moves away from to create the angle theta. Do not define this
                             and plane_atom_position.
    :param plane_atom_position: np array of position of the plane_atom (doesn't actually need to be a position of an
                                atom per se, but useful if it is. Do not define this and the index.
    :param midpoint: weighting of the midpoint to the two nnindices. 0 puts the muon on nn_indices[0], 1 puts it on
                     nn_indices[2]. 0.5 puts it in between the two.
    :return: ase_atoms with the muon
    """

    # check either muon_position nor nn_indices is None
    assert (muon_position is None) != (nn_indices is None)

    ase_atoms = copy.deepcopy(object_of_class.cif_read)
    # three possibilities:
    # 1) >2 nn_indices -> just find average, ignore angles
    # 2) 2 nn_indices or muon_position, theta not given (or 180) -> just find midpoint
    # 3) 2 nn_indices, theta and phi -- find muon_position using theta and phi

    # see how many nn_indices there are
    if nn_indices is not None:
        muon_position = np.zeros((3,))
        # possibility 1 (or 2)
        if len(nn_indices) > 2:
            # if nn_indices are given, work out the average of them to get the muon position (there can be more than 2!)
            for nn_index in nn_indices:
                muon_position += ase_atoms[nn_index].position / len(nn_indices)
        elif (len(nn_indices) == 2 and (theta == 180 or theta is None)):
            muon_position = ase_atoms[nn_indices[0]].position * midpoint \
                + ase_atoms[nn_indices[1]].position*(1-midpoint)
        elif len(nn_indices) == 2:
            # we need to calculate the muon position with theta and phi...

            # convert everything into TCoord3D objects (...easier to work with)
            nn_position_1 = ase_atoms[nn_indices[0]].position
            # nn_position_1 = coord(nn_position_1[0], nn_position_1[1], nn_position_1[2])
            nn_position_2 = ase_atoms[nn_indices[1]].position
            # nn_position_2 = coord(nn_position_2[0], nn_position_2[1], nn_position_2[2])

            # check the plane atom has been defined
            assert (plane_atom_index is None) != (plane_atom_position is None)

            if plane_atom_position is None:
                plane_atom_position = ase_atoms[plane_atom_index].position
            # plane_atom_position_c = coord(plane_atom_position[0], plane_atom_position[1], plane_atom_position[2])
            # muon_position = get_bent_muon_position(nn_position_1=nn_position_1, nn_position_2=nn_position_2,plane_position=plane_atom_position_c, theta=theta, phi=phi,midpoint=midpoint)

            muon_position = muon_position.tonumpyarray()

        else:
            print('Error with the muon position parameters.')
            assert False

    # add the muon to the ASE atoms
    muon = atom.Atom('X', position=muon_position)

    # add the muon to the ASE atoms
    ase_atoms.append(muon)
    object_of_class.cif_read = ase_atoms
    return ase_atoms


def make_supercell(object_of_class, unperturbed_atoms: atoms = None, unperturbed_supercell=1,
                   small_output=False):
    """
    make a supercell with atoms_mu in the centre, and surrounded by unperturbed_supercell unperturbed_atoms
    :param atoms_mu: ASE atoms, maybe with distortions, including muon
    :param unperturbed_atoms: ASE atoms of unperturbed structure
    :param unperturbed_supercell: number of instances of unperturbed_atoms to bolt on to the end of atoms_mu
    :return: supercell of atoms_mu+unperturbed_supercell*unperturbed_atoms. If small_output==False, return ASE atoms,
             otherwise returns a list of [atom type, position]
    """

    atoms_mu = object_of_class.cif_read

    if unperturbed_atoms is None:
        # we need to confirm that atom[-1] is the muon by convetion it is but...
        unperturbed_atoms = copy.deepcopy(atoms_mu[:-1])
    else:
        unperturbed_atoms = copy.deepcopy(unperturbed_atoms)

    # if atoms_mu is already a supercell, then make unperturbed_atoms a supercell of the same size
    unperturbed_atoms = build.make_supercell(unperturbed_atoms, np.diag([1, 1, 1]) *
                                             atoms_mu.cell.lengths()[0] /
                                             unperturbed_atoms.cell.lengths()[0], wrap=False)

    muon = copy.deepcopy(atoms_mu[-1])

    output_list = []
    if small_output:
        output_list = [[this_atom.symbol, this_atom.position]
                       for this_atom in atoms_mu]

    del atoms_mu[-1]

    # we do the geometry of the supercell
    for x_sign in range(-unperturbed_supercell, unperturbed_supercell + 1):
        for y_sign in range(-unperturbed_supercell, unperturbed_supercell + 1):
            for z_sign in range(-unperturbed_supercell, unperturbed_supercell + 1):
                if x_sign == y_sign == z_sign == 0:
                    continue
                translation_vector = np.sign(x_sign) * (abs(x_sign) - 1) * unperturbed_atoms.cell[0] + \
                    np.sign(x_sign) * atoms_mu.cell[0]
                translation_vector += np.sign(y_sign) * (abs(y_sign) - 1) * unperturbed_atoms.cell[1] + \
                    np.sign(y_sign) * atoms_mu.cell[1]
                translation_vector += np.sign(z_sign) * (abs(z_sign) - 1) * unperturbed_atoms.cell[2] + \
                    np.sign(z_sign) * atoms_mu.cell[2]
                # print(translation_vector)
                unperturbed_atoms.translate(translation_vector)
                for this_atom in unperturbed_atoms:
                    if small_output:
                        output_list.append(
                            [this_atom.symbol, copy.deepcopy(this_atom.position)])
                    else:
                        atoms_mu.append(this_atom)
                unperturbed_atoms.translate(-1 * translation_vector)

    atoms_mu.append(muon)
    if small_output:
        return output_list
    else:

        old_cell = atoms_mu.get_cell()
        atoms_mu.set_cell(
            old_cell*(2*unperturbed_supercell + 1), scale_atoms=False)
        atoms_mu.translate(unperturbed_supercell * old_cell[0])
        atoms_mu.translate(unperturbed_supercell * old_cell[1])
        atoms_mu.translate(unperturbed_supercell * old_cell[2])

        object_of_class.gui_with_muon.exit()

        object_of_class.cif_read = atoms_mu
        object_of_class.cif_read = masking(
            atoms_mu, object_of_class.radius_entry.get())
        generate_cell_components_window(object_of_class)

        object_of_class.images_supercell = Images()
        object_of_class.images_supercell.initialize([atoms_mu])
        object_of_class.gui_supercell = GUI(object_of_class.images_supercell)
        object_of_class.gui_supercell.run()


def masking(atoms_mu: atoms, radius: float):
    center = atoms_mu[-1].position

    mask = np.linalg.norm(atoms_mu.positions - center, axis=1) < int(radius)
    i_atoms = atoms_mu[mask]
    print(i_atoms)
    view(i_atoms)
    return i_atoms


def update_strcuture_data(object_of_class, iso=None):
    object_of_class.structure_data = []
    mu_position = object_of_class.cif_read[-1].position
    print('muon positon', mu_position)
    # Create the data
    for atom in object_of_class.cif_read:
        element = atom.symbol
        relative_postision = atom.position-mu_position
        # atom.symbol
        print(atom.symbol, relative_postision, '@', atom.position)
        if element == 'X':
            element = 'mu'

        magnetic_moment = gyromagnetic_ratio(
            element, iso)*spin(element, iso)

        if np.linalg.norm(relative_postision) == 0:
            strength = 0
        strength = abs(magnetic_moment/np.linalg.norm(relative_postision)**3)
        distance = abs(np.linalg.norm(relative_postision))
        info = (atom.symbol, strength, relative_postision,
                spin(element, iso), distance)
        object_of_class.structure_data.append(info)


def generate_cell_components_window(object_of_class):
    ''' Inserts the structure_data to the table
    '''
    update_strcuture_data(object_of_class, iso=None)

    # create a window to contain the table
    top = customtkinter.CTkToplevel(object_of_class)
    dir = os.path.dirname(__file__)
    filename = dir+'\logo_mm.ico'
    # top.iconbitmap(filename)
    top.after(200, lambda: top.iconbitmap(filename))
    top.title("Characterization of muon stopping site")

    # define elements of the table
    columns = ("#1", "#2", "#3", "#4", '#5')
    tree = ttk.Treeview(top, columns=columns, show='headings')

    # define headings
    tree.heading("#1", text="Symmbols")
    tree.heading("#2", text="Strentgh")
    tree.heading("#3", text="Position")
    tree.heading("#4", text="Spin")
    tree.heading("#5", text="Distance")

    # insert elemets in the structure_data to the table
    for item in object_of_class.structure_data:
        tree.insert('', 'end', values=item)

    # Define variables
    object_of_class.count_dinteractions = 0
    index_in_structure_data_selected_components = []

    def handle_item_selection(event):
        ''' Binded to the Treeview
            Acts when an element of the table of 'Characterization of muon stopping site'
            is selected and transfer the information to dipolar interactions frame
        '''

        # obtain the selected item
        item_details = tree.item(tree.selection()[0])
        item_values = item_details['values']
        dipolar_interaction_string = clean_whitespace_and_brackets(
            item_values[2])

        # retrieve and store the index of the selected components
        for i in range(len(object_of_class.structure_data)):
            maria = clean_whitespace_and_brackets(
                str(object_of_class.structure_data[i][2]))
            if dipolar_interaction_string == maria:
                if i not in index_in_structure_data_selected_components:
                    index_in_structure_data_selected_components.append(i)

                    # add the item selected to dipolar frame
                    update_spin_dipolar_interaction(object_of_class,
                                                    dipolar_interaction_string, object_of_class.count_dinteractions,
                                                    index_in_structure_data_selected_components)

        object_of_class.count_dinteractions = len(
            index_in_structure_data_selected_components)

    # bind the clicking of the item in table to adding entry in dipolar frame
    tree.bind('<<TreeviewSelect>>', handle_item_selection)

    # Pack the Treeview widget
    tree.pack(fill='both', expand=True)


def update_spin_dipolar_interaction(object_of_class, str_dipolar_value, indexx, index_in_structure_data_selected_components):
    ''' add the spin and dipolar interactions into the dipolar frame
        update object_of_class.dipolar_dic[
    '''
    # clean spin entry and assert the first element to be muon
    if indexx == 0:
        object_of_class.spins_entry.delete(0, 'end')
        object_of_class.spins_entry.insert(0, 'mu ')
        try:
            object_of_class.gui_supercell.exit()
        finally:
            pass
    # retrieve symbol of selected element
    index = index_in_structure_data_selected_components[-1]
    element_symbol = object_of_class.structure_data[index][0]
    object_of_class.spins_entry.insert('end', element_symbol+' ')

    # create label
    spin_entry_position = 2+indexx
    label = 'dipolar_1_'+str(spin_entry_position)

    # Add the label
    str_1 = tk.StringVar()
    str_1.set(str_dipolar_value)
    add_label = tk.Label(object_of_class.framess, text=label)
    add_label.pack()

    # add dipolar interaction as entry
    add_entry = tk.Entry(object_of_class.framess, textvariable=str_1)
    add_entry.pack(pady=5)

    # store the dipolar interactions selected
    object_of_class.dipolar_dic[spin_entry_position] = str_dipolar_value
    print(object_of_class.dipolar_dic,"<  < >")

# --------------------------------------------------------------------------------------------------------------------
#                                                     Update data
# --------------------------------------------------------------------------------------------------------------------


def update_parameters(object_of_class):
    object_of_class.first_param = object_of_class.field_value.get(
        1.0, "end-1c")

    if object_of_class.first_param != '':
        object_of_class.parameters._keywords["field"] = KWField(
            object_of_class.first_param)


# --------------------------------------------------------------------------------------------------------------------
#                                                     DRAFT
# --------------------------------------------------------------------------------------------------------------------





def read_variables(object_of_class):
    '''To facilitate redability i_params is used instead'''
    # Ideally the for loops are standarized to be functions called

    i_params = object_of_class.parameters.evaluate()

    # -----------------------------------
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

    # -----------------------------------
    #               Field              #
    field_str = ''
    count = 0
    for i in i_params['field'].value[0]:
        # print(i)
        if count == 0:
            field_str = i
        else:
            field_str = field_str+' '+i
        count = count+1
    object_of_class.field_value.insert('end', field_str)

    # -----------------------------------
    #            Polarization          #

    # if for the case of    anu couplings
    # we can add for later the axis
    # we only make the rest appear if they are different from default
    # average_axes

    # -----------------------------------
    #               Couplings              #
    # ------------------------------------

    # -----------------------------------
    #                   Dipolar          #
    # Recognize how manny couplings we ha

