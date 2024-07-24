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
# from soprano.collection import AtomsCollection
import soprano.properties.atomsproperty
import copy
import ase
import ase.data
from ase.visualize import view
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

    # print(object_of_class.fitting_variables)
    data_str_terminator = ' ' + xy + ' value ' + \
        object_of_class.fitting_variables + terminator
    # print('aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa')
    # print(type(object_of_class.first_param))
    object_of_class.hist.append(data_str_terminator)
    # object_of_class.result_dic[dt_processing_extract_var(object_of_class)] = xy
    object_of_class.result_dic[object_of_class.fitting_variables] = xy
    print('***********************result dic when we are in the send processing',
          object_of_class.result_dic.keys())  # debug
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
    # if object_of_class.pvar_hist == []:
    # now that things are new we try only one parameter
    #    object_of_class.pvar_hist.append([float(fit_var), 0, 0])
    #    pass
    if len(fit_var) == 1:
        # object_of_class.pvar_hist.append([float(fit_var), 0, 0])
        fit_var = [float(fit_var), 0, 0]
    elif len(fit_var) == 2:
        # object_of_class.pvar_hist.append(
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

# -------------------------------------------------------------------------------------------------------
#                                           File Reading
# -------------------------------------------------------------------------------------------------------


def load_file(object_of_class):

    object_of_class.file = filedialog.askopenfilename()
    print(object_of_class.file)
    object_of_class.parameters = MuSpinInput(open(object_of_class.file))
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
    object_of_class.Input_path.set(name)
    print(name)
    print(object_of_class.Input_path.get())
    # Input_path.config()


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

# --------------------------------------------------------------------------------------------------------------------
#                                                     CIF FILE
# --------------------------------------------------------------------------------------------------------------------


muon_positio = np.zeros((3,))


def selecting__nn_indices(object_of_class):

    selected = []
    for i_images_selected_atom in range(0, len(object_of_class.images.selected)):
        if object_of_class.images.selected[i_images_selected_atom]:
            selected.append(i_images_selected_atom)
    print(selected)
    view(add_muon_to_aseatoms(object_of_class, nn_indices=selected))

    object_of_class.gui.exit()

    if selected == []:
        object_of_class.nn_indices = None
    else:
        object_of_class.nn_indices = selected


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

    # check either muon_position xor nn_indices is None
    assert (muon_position is None) != (nn_indices is None)

    # ase_atoms = copy.deepcopy(ase_atoms)
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
            # print()
            muon_position = muon_position.tonumpyarray()
            print(object_of_class.muon_position)
        else:
            print('Error with the muon position parameters.')
            assert False
    # object_of_class.muon_position = muon_position.tonumpyarray()
    # now add the muon to the ASE atoms
    muon = atom.Atom('X', position=muon_position)
    try:
        object_of_class.muon_position = muon_position
        print(object_of_class.muon_position)
    finally:
        print('Could not find muon position')
    print(muon)
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

    # make the supercell structure
    # the changes are not stressing the orginal atom
    # atoms_mu = copy.deepcopy(atoms_mu)
    atoms_mu = object_of_class.cif_read
    print(atoms_mu)

    print('this is the atom we out in and deep copy', atoms_mu)
    if unperturbed_atoms is None:
        # we need to confirm that atom[-1] is the muon by convetion it is but...
        unperturbed_atoms = copy.deepcopy(atoms_mu[:-1])
        print('the item minus1', atoms_mu[:-1])
        # view(atoms_mu)
    else:
        unperturbed_atoms = copy.deepcopy(unperturbed_atoms)
    # if atoms_mu is already a supercell, then make unperturbed_atoms a supercell of the same size

    unperturbed_atoms = build.make_supercell(unperturbed_atoms, np.diag([1, 1, 1]) *
                                             atoms_mu.cell.lengths()[0] /
                                             unperturbed_atoms.cell.lengths()[0], wrap=False)

    muon = copy.deepcopy(atoms_mu[-1])
    print('just the muon', muon)
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
    maria = atoms_mu
    print('just before', atoms_mu)
    if small_output:
        return output_list
        print(atoms_mu, 'inside if')
    else:
        # what exactly is happeining here
        print('inside else')
        old_cell = atoms_mu.get_cell()
        atoms_mu.set_cell(
            old_cell*(2*unperturbed_supercell + 1), scale_atoms=False)
        atoms_mu.translate(unperturbed_supercell * old_cell[0])
        print('a', atoms_mu)
        atoms_mu.translate(unperturbed_supercell * old_cell[1])
        print('b', atoms_mu)
        atoms_mu.translate(unperturbed_supercell * old_cell[2])
        print('c', atoms_mu)
        print('final atoms', atoms_mu)
        view(atoms_mu)
        rebeca = atoms_mu

        if rebeca != maria:
            print('not equal')
        object_of_class.cif_read = atoms_mu
        print(object_of_class.cif_read[-1])
        print(object_of_class.cif_read)
        object_of_class.cif_read = masking(
            atoms_mu, object_of_class.radius_entry.get())
        selected_table(object_of_class)
        return atoms_mu

    """
    Get the muon position by selecting two atoms to be the nearest neighbors (nn).
    :param atoms: ASE atoms of the structure
    :return: (muon position ndarray, list of the index of the atoms the muon is in between)
    """


def masking(atoms_mu: atoms, radius: float):
    center = atoms_mu[-1].position
    if radius == '':
        radius = 0.5
    mask = np.linalg.norm(atoms_mu.positions - center, axis=1) < int(radius)
    i_atoms = atoms_mu[mask]
    print(i_atoms)
    view(i_atoms)
    return i_atoms


def strength(muon_position, element, iso=None):
    # interaction with muon
    # here
    # ideally this is done in muspinsim
    if element == 'x':
        element = 'mu'
    magnetic_moment = gyromagnetic_ratio(element, iso)*spin(element, iso)
    # object_of_class.muon_position
    magnetic_m = magnetic_moment(element)
    relative_position = muon_position

    results = 'x'
    print((np.linalg.norm(relative_position))**2)

    return results


def create_table(object_of_class, iso=None):
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
        strength = magnetic_moment/np.linalg.norm(relative_postision)**3
        info = (atom.symbol, strength, relative_postision)
        object_of_class.structure_data.append(info)


def selected_table(object_of_class):
    create_table(object_of_class, iso=None)
    top = customtkinter.CTkToplevel(object_of_class)
    top.title("Custom TopLevel Window")
    columns = ("#1", "#2", "#3")
    tree = ttk.Treeview(top, columns=columns, show='headings')
    # object_of_class.tree=ttk.Treeview(root,columns)
    tree.heading("#1", text="Symmbols")
    tree.heading("#2", text="Strentgh")
    tree.heading("#3", text="Position")

    for item in object_of_class.structure_data:
        tree.insert('', 'end', values=item)

    def on_item_selected(event):
        selected_item = tree.selection()[0]
        item_details = tree.item(selected_item)
        item_values = item_details['values']
        # strv = str(item_values[2])
        item_values[2] = item_values[2].replace(']', '')
        item_values[2] = item_values[2].replace('[', '')
        ' '.join(item_values[2].split())
        print(item_values[2])
        object_of_class.dipolar_value.insert('end', item_values[2])
        print(f"Selected ...... Item: {item_values}")

    tree.bind('<<TreeviewSelect>>', on_item_selected)
    # Pack the Treeview widget
    tree.pack(fill='both', expand=True)


# --------------------------------------------------------------------------------------------------------------------
#                                                     Update data
# --------------------------------------------------------------------------------------------------------------------


def update_parameters(object_of_class):
    # value = object_of_class.field_value.get(1.0, "end-1c")
    object_of_class.first_param = object_of_class.field_value.get(
        1.0, "end-1c")
    # print('here is the value', value)
    # if value != '':
    if object_of_class.first_param != '':
        object_of_class.parameters._keywords["field"] = KWField(
            object_of_class.first_param)
        # print(type(object_of_class.first_param))


# --------------------------------------------------------------------------------------------------------------------
#                                                     DRAFT
# --------------------------------------------------------------------------------------------------------------------

def opennn(object_of_class):
    # Select the cif file
    file = filedialog.askopenfilename()
    # read the file and make it into a atoms object
    object_of_class.cif_read = ase.io.read(file)

    top = customtkinter.CTkToplevel(object_of_class)
    top.title("Custom TopLevel Window")
    top.geometry("400x300")
    frame_structure = LabelFrame(top, text="Structure", width=200)
    frame_structure.place(x=5, y=5)

    calculate_button = customtkinter.CTkButton(frame_structure, text="Calculate Muon Position",
                                               command=lambda: selecting__nn_indices(object_of_class))
    calculate_button.grid(row=0, column=0, padx=5, pady=5)

    frame_angle = LabelFrame(frame_structure, text='__')
    frame_angle.grid(row=1, column=0, padx=5, pady=5)

    struc_phi_label = customtkinter.CTkLabel(
        master=frame_angle, text="Phi", width=40)
    struc_phi_label.grid(row=1, column=0, padx=5, pady=5)

    struc_phi_entry = customtkinter.CTkEntry(
        frame_angle, width=40)
    struc_phi_entry.grid(row=1, column=1)

    struc_theta_label = customtkinter.CTkLabel(
        master=frame_angle, text="Theta")
    struc_theta_label.grid(row=1, column=2, padx=5, pady=5)

    struc_phi_entry = customtkinter.CTkEntry(
        frame_angle, width=40)
    struc_phi_entry.grid(row=1, column=3)

    calculate_button = customtkinter.CTkButton(frame_structure, text="Generate Supercell",
                                               command=lambda: make_supercell(object_of_class))
    calculate_button.grid(row=2, column=0, padx=5, pady=5)

    frame_options = LabelFrame(frame_structure, text='__')
    frame_options.grid(row=3, column=0, padx=5, pady=5)

    radios_symmetry_label = customtkinter.CTkLabel(
        master=frame_options, text="Radius")
    radios_symmetry_label.grid(row=3, column=0, padx=5, pady=5)

    radius_entry = customtkinter.CTkEntry(
        frame_options, width=40)
    radius_entry.grid(row=3, column=1)
    print('DEBUG: this is the cif file read', object_of_class.cif_read)
    # table(top, cif_data(object_of_class.cif_read))

    object_of_class.images = Images()
    object_of_class.images.initialize([object_of_class.cif_read])
    object_of_class.gui = GUI(object_of_class.images)
    object_of_class.gui.run()
   # print('babababab')


def cif_data(cif_read_io):
    cif_read_io.get_positions()
    cif_read_io.get_chemical_symbols()

    lst = []
    for i in range(cif_read_io.get_global_number_of_atoms()):
        lst_tuple = (cif_read_io.get_chemical_symbols()[
                     i], cif_read_io.get_positions()[i])
        lst.append(lst_tuple)

    return lst


def table(root, lst):
    listinha = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12,
                13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23]

    dicc = {}
    total_rows = len(lst)
    total_columns = len(lst[0])
    for i in range(total_rows):
        for j in range(total_columns):
            dicc[listinha[j]] = tk.Entry(root, width=40)
            entry = tk.Entry(root, width=40)
            entry.grid(row=i, column=j)
            entry.insert('end', lst[i][j])


def update_param_spec(object_of_class):
    # print('we entered param')
    # my_string = " ".join(str(element)
    #                     for element in object_of_class.fitting_variables)
    # print('fitting vari', object_of_class.fitting_variables)
    # print('my tring', my_string)
    # i_params = object_of_class.parameters.evaluate()
    # print('param before', i_params['field'].value[0])
    object_of_class.parameters._keywords["field"] = KWField(
        object_of_class.fitting_variables)

    i_params = object_of_class.parameters.evaluate()
    print('//////fitting variables', object_of_class.fitting_variables)
    print('***the', i_params['field'].value[0])
    # print('param after', i_params['field'].value[0])


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


def data_processing_xy_terminator(object_of_class, terminator='Hello'):
    # scientific notation is removed
    data_str_terminator = ' ' + \
        data_processing_xy(object_of_class) + terminator
    # print(data_str_terminator)
    object_of_class.hist.append(data_str_terminator)
    # print('hana is printed', object_of_class.hist)
    return data_str_terminator


def process_time_wimda(object_of_class):
    # object_of_class.wimda_time #from which we extract the times
    pass


def cif():
    Create_Input.cif_files()


def data_processing_terminator(data, terminator='Hello'):
    # scientific notation is removed
    data_str_terminator = ' '+data_processing(data) + terminator
    return data_str_terminator

    # scientific notation is removed


def load_variables(object_of_class, inn):
    object_of_class.name_text.set('mu')
    object_of_class.spins_entry.delete(0, 'end')
    object_of_class.spins_entry.insert('end', 'mu F')

    if object_of_class.time_entry1.get() != '' and object_of_class.time_entry2.get() != '' and object_of_class.time_entry3.get() != '':
        inn.times = f'range({object_of_class.time_entry1.get()},{object_of_class.time_entry2.get()},{object_of_class.time_entry3.get()})'
    inn.cif = False

    object_of_class.zeeman_value.insert('end', 'aaaaaaaaaaa')


def readding(object_of_class):

    params = MuSpinInput(open(object_of_class.file))

    params._keywords["Time"] = KWTime(
        f"range({object_of_class.time_entry1.get()},{object_of_class.time_entry2.get()},{object_of_class.time_entry3.get()})")

    params._keywords["field"] = KWField(0)

    experiment = ExperimentRunner(params)

    results = experiment.run()
    object_of_class.results = results


def transform_reading(object_of_class):
    # Essential frame
    params = MuSpinInput(open(object_of_class.file))
    params._keywords["name"] = KWName(object_of_class.name_text.get())
    params._keywords["spin"] = KWSpins[object_of_class.spins_entry.get()]
    params._keywords["Time"] = KWTime(
        f"range({object_of_class.time_entry1.get()},{object_of_class.time_entry2.get()},{object_of_class.time_entry3.get()})")


def transform_reading(object_of_class):
    # Essential frame
    params = MuSpinInput(open(object_of_class.file))
    params._keywords["name"] = KWName(object_of_class.name_text.get())
    params._keywords["spin"] = KWSpins[object_of_class.spins_entry.get()]
    params._keywords["Time"] = KWTime(
        f"range({object_of_class.time_entry1.get()},{object_of_class.time_entry2.get()},{object_of_class.time_entry3.get()})")
