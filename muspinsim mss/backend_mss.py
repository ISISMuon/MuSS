"""
Project: Simulations for muSR data Analysis Industrial Placement
Author: Paula Franco
Date: February 2024

Summary:
This module provides a set of functions for managing and interacting with simulation parameters, 
including GUI integration, data processing, and simulation management for a scientific or engineering application

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
import threading
from threading import Thread

import customtkinter
from tkinter.ttk import Label, LabelFrame, Progressbar
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

# -------------------------------------------------------------------------------------------------------
#                                           DATA PROCESSING
# -------------------------------------------------------------------------------------------------------

def retrieve_stored_simulation_data(object_of_class, terminator='Hello'):
    ''' 
    Retrieves the stored simulation data based on the current parameters.
    
    This function retrieves the previously stored xy data from the result_dic using the current set of parameters (fit_params_to_generate_simulation). 
    The retrieved data is then formatted into a string that includes the data, parameter values, and a terminator string.
    '''
    # retrive the stored xy according to set of current simulation parameters
    xy = object_of_class.result_dic[object_of_class.fit_params_to_generate_simulation]

    # format the message to be sent so that client can decode it retrieving y and the parameters
    formatted_data_str = ' ' + xy + ' value ' + \
        object_of_class.fit_params_to_generate_simulation + terminator
    #retrieve_stored_simulation_data
    
    return formatted_data_str

def format_simulation_data(object_of_class, terminator='Hello'):
    '''
    Formats the simulation data to be read and interpreted by the client,
    and appends a terminator to signal the end of the message.

    It also updates the simulation_object's result dictionary with the formatted data, using the
    current set of parameters as the key.
    '''

    # Initialize list to hold the x-axis values
    x_values = [] 

    # Extract the first element from each simulated x-axis value and store it in the list
    for i in range(len(object_of_class.x_axis_simulated_values)):
        x_values.append(object_of_class.x_axis_simulated_values[i][0])

    # Process the x-axis values and results, then combine them into a single string
    xy_data = data_processing(x_values) + ' ' + \
        data_processing(object_of_class.results)
    
    # Check if no parameters are set; if so, extract and update the parameters
    if object_of_class.fit_params_to_generate_simulation == ' ':
        extract_initial_variables(object_of_class)

    # define the sequence of information cleint is expecting
    formatted_data_str = ' ' + xy_data + ' value ' + \
        object_of_class.fit_params_to_generate_simulation + terminator

    # Update the result dictionary with the current parameters and processed data
    object_of_class.result_dic[object_of_class.fit_params_to_generate_simulation] = xy_data
    
    #Debug print
    print(f'The parameters set being fiited is {object_of_class.result_dic.keys()}, this was retrived from the stored dictionary')

    return formatted_data_str

def data_processing(data):
    ''' 
    Process the data resulting from the simulation (mainly)
    Converts array to string, cleans unwanted characters and add space in the beguining of the string
    '''
    # Suppress scientific notation in the numpy output
    np.set_printoptions(suppress=True)

    # Convert the array to a string
    data_string = str(data)

    # Clean the string by removing unwanted characters
    results_string = data_string.replace('[', '').replace(',', '').replace(']', '')

    # introduce space before string
    formatted_data_string = ' '+ results_string

    return formatted_data_string

def dipolar_fitting_parameter(object_of_class,simmetry):
    '''
    '''
    #x= p*np.sin(theta)*np.cos(phi)
    #y=p*np.sin(theta)* np.sin(phi)
    #z=p*cos(tetha)
    #p=sqrt(x^2+y^2+z^2)

    #object_of_class.fit_params_to_generate_simulation = distance

    #how many of the dipolar variables are being fitted against
    pass 

def extract_initial_variables(object_of_class):
    '''
    Extracts and processes the initial variables for fitting and assigns the processed variables
    to the `fit_params_to_generate_simulation` attribute of the simulation object.'''

    # Define the variable name to extract
    var = 'field'
    
    # Evaluate and retrieve the parameters from the simulation object
    i_params = object_of_class.parameters.evaluate()
    fit_var = i_params[var].value[0]

    # Adjust the fitting variable based on its length
    if len(fit_var) == 1:
        fit_var = [float(fit_var), 0, 0]
    elif len(fit_var) == 2:
        fit_var = [float(fit_var[0]), float(fit_var[0]), 0]
    
    # Process the fitting variable into a string format
    fit_var = data_processing(fit_var)
    object_of_class.fit_var=fit_var
    # Assign the processed variable to the simulation object for use in generating the simulation
    object_of_class.fit_params_to_generate_simulation = fit_var

def clean_whitespace_and_brackets(string: str) -> str:
    ''' 
    Cleans a string by removing brackets and reducing multiple spaces to a single space
    by removing '[',']' and spaces in a string
    '''
    result_string = string.replace(
        ']', '').replace('[', '').replace(
        '    ', ' ').replace('   ', ' ').replace('  ', ' ')
    return result_string

# --------------------------------------------------------------------------------------------------------------------
#                                                     Fitting
# --------------------------------------------------------------------------------------------------------------------

def fitting_options_window(parent_object):
    '''
    '''
    
    # Create a new top-level window associated with the parent object
    fitting_top_window = customtkinter.CTkToplevel(parent_object)
    # Set the window icon
    dir = os.path.dirname(__file__)
    filename = dir+'\logo_mm.ico'
    fitting_top_window.after(200, lambda: fitting_top_window.iconbitmap(filename))
    
    # Set the window title
    fitting_top_window.title("Fitting parameters")

# -------------------------------------------------------------------------------------------------------
#                                           File Reading
# -------------------------------------------------------------------------------------------------------


def load_input_file(simulation_object):
    '''
    Opens the txt input file, then variables are intepreted using the MuSpinInput class
    The characteristic called paramteres is used to store the parameters
    The variables are then displayed in the UI
    '''
    
    simulation_object.input_txt_file = filedialog.askopenfilename()
    # Debug print
    print(f'The file {simulation_object.input_txt_file} was selected as the input file')

    # store parameters
    simulation_object.parameters = MuSpinInput(open(simulation_object.input_txt_file))

    #displays variables in UI
    populate_gui_with_parameters(simulation_object)


def run_simulation(simulation_object):
    '''
    The Simulation runs and the results value is determined
    '''
    #Assert the parameters as the input of the simulation
    experiment = ExperimentRunner(simulation_object.parameters)
    simulation_object.results = experiment.run()


def get_path(object_of_class)->str:
    '''
    Returns the path where the txt file will be saved
    '''
    # Ensure the name entry field is configured correctly
    object_of_class.name_entry.configure()

    # Construct the file path using the username and name entry input
    path = object_of_class.username + '\Documents' + \
        '/'+object_of_class.name_entry.get()+'.txt'
    
    return path


def create_input_file(object_of_class):
    ''''
    Creates a new input file with the parameters specified in the simulation object's UI fields.
    '''
    
    # Access the `inn` object from the simulation object
    inn = object_of_class.inn
    
    # Set the name and spins from the respective entry fields
    inn.name = object_of_class.name_entry.get()
    inn.spins = object_of_class.spins_entry.get()

    # Set the time range if all time entries are provided
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
    
    # Set fitting parameters
    inn.fitting_tolerance = object_of_class.fitting_tolerance_value.get()
    inn.fitting_variables = object_of_class.fitting_variables_values.get(
        "1.0", "end-1c")
    inn.fitting_method = object_of_class.fitting_method.get()
    
    # Set additional simulation configuration
    inn.orientation = object_of_class.orientation_value.get("1.0", "end-1c")
    inn.polarization = object_of_class.polarization_value.get("1.0", "end-1c")
    inn.experiment = None

    # Set the x and y axes for the simulation
    inn.x_axis = object_of_class.x_axis_value.get()
    inn.y_axis = object_of_class.y_axis_value.get()

    # Finalize the creation of the input file
    inn()


def save_as_directory(object_of_class):
    '''
    This function prompts the user to select a directory where files will be saved. The selected path is then
    stored in the simulation object's `save_path` attribute for future use.
    '''
    # Open a directory selection dialog and get the chosen path
    selected_directory = filedialog.askdirectory()

    # Update the simulation object's save path with the selected directory
    object_of_class.save_path.set(selected_directory)

    # Debug print to confirm the selected path
    print(selected_directory)
    print(object_of_class.save_path.get())
    
def graph_update_and_retrieve_time(object_of_class):
    '''
    Updates the graph with the latest simulation results and retrieves the x-axis (time) values.
    
     Actions:
    1. Clears the current graph.
    2. Plots the results of the simulation against time.
    3. Draws the updated graph on the canvas.
    4. Stores the x-axis (time) values for future use.
    '''
    #the graph is cleared
    object_of_class.a.clear()

    #get the x_axis value(time) directly from the parameters plot results depending on time
    object_of_class.a.plot(object_of_class.parameters.evaluate()[
                           'time'].value, object_of_class.results)
    
    # display the updated graph on the canvas
    object_of_class.canvas.draw()

    #store x_axis value (time) in x_axis_simulation_values
    object_of_class.x_axis_simulated_values = object_of_class.parameters.evaluate()['time'].value

# --------------------------------------------------------------------------------------------------------------------
#                                                     CIF FILE
# --------------------------------------------------------------------------------------------------------------------


def selecting__nn_indices(object_of_class):
    '''
    Recognizes the elements (atoms) selected in the ASE viewer and handles the 
    initialization and visualization of the updated images with a muon added.
    '''

    # Initialize an empty list to store the indices of selected atoms
    selected_atoms = []
    
    # Loop through the selected atoms in the ASE viewer and store their indices
    for i_images_selected_atom in range(0, len(object_of_class.images.selected)):
        if object_of_class.images.selected[i_images_selected_atom]:
            selected_atoms.append(i_images_selected_atom)

    # Exit the initial GUI view
    object_of_class.gui.exit()

    # Create a new Images object with a muon added to the selected atoms
    object_of_class.images_with_muon = Images()
    object_of_class.images_with_muon.initialize(
        [add_muon_to_aseatoms(object_of_class.cif_read, nn_indices=selected_atoms)])
    
    # Initialize a new GUI to display the updated images with the muon
    object_of_class.gui_with_muon = GUI(object_of_class.images_with_muon)

    # Run the new GUI
    object_of_class.gui_with_muon.run()

def add_muon_to_aseatoms(atoms_structure:atoms, theta: float = 180, phi: float = 0, nn_indices: list = None,
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

    # Ensure that either muon_position or nn_indices is defined, but not both
    assert (muon_position is None) != (nn_indices is None)

    # Make a deep copy of the ASE atoms structure to avoid modifying the original object
    ase_atoms = copy.deepcopy(atoms_structure)
    # three possibilities:
    # 1) >2 nn_indices -> just find average, ignore angles
    # 2) 2 nn_indices or muon_position, theta not given (or 180) -> just find midpoint
    # 3) 2 nn_indices, theta and phi -- find muon_position using theta and phi

    # If nn_indices is provided, calculate the muon position
    if nn_indices is not None:
        muon_position = np.zeros((3,)) # Initialize muon position
        
        # Case 1: More than 2 nn_indices - take the average position of the neighbors
        if len(nn_indices) > 2:
            # if nn_indices are given, work out the average of them to get the muon position (there can be more than 2!)
            for nn_index in nn_indices:
                muon_position += ase_atoms[nn_index].position / len(nn_indices)
        
        # Case 2: Two nn_indices and theta is 180 (or undefined) - place the muon at the midpoint
        elif (len(nn_indices) == 2 and (theta == 180 or theta is None)):
            muon_position = ase_atoms[nn_indices[0]].position * midpoint \
                + ase_atoms[nn_indices[1]].position*(1-midpoint)
        
        # Case 3: Two nn_indices with defined theta and phi - calculate muon position based on angles
        elif len(nn_indices) == 2:
            # we need to calculate the muon position with theta and phi...

            # convert everything into TCoord3D objects (...easier to work with)
            nn_position_1 = ase_atoms[nn_indices[0]].position
            # nn_position_1 = coord(nn_position_1[0], nn_position_1[1], nn_position_1[2])
            nn_position_2 = ase_atoms[nn_indices[1]].position
            # nn_position_2 = coord(nn_position_2[0], nn_position_2[1], nn_position_2[2])

            # Ensure plane_atom_position or plane_atom_index is provided, but not both
            assert (plane_atom_index is None) != (plane_atom_position is None)

            # Get the plane atom position from its index if not directly provided
            if plane_atom_position is None:
                plane_atom_position = ase_atoms[plane_atom_index].position
            # plane_atom_position_c = coord(plane_atom_position[0], plane_atom_position[1], plane_atom_position[2])
            # muon_position = get_bent_muon_position(nn_position_1=nn_position_1, nn_position_2=nn_position_2,plane_position=plane_atom_position_c, theta=theta, phi=phi,midpoint=midpoint)

            muon_position = muon_position.tonumpyarray()

        else:
            print('Error with the muon position parameters.')
            assert False

    # Create a new atom for the muon at the calculated or provided position
    muon = atom.Atom('X', position=muon_position)

    # Append the muon to the ASE atoms structure
    ase_atoms.append(muon)

    # Update the simulation object with the modified atoms
    atoms_structure = ase_atoms

    return ase_atoms

def make_supercell(simulation_object, unperturbed_atoms: atoms = None, unperturbed_supercell=1,
                   small_output=False):
    """
    make a supercell with atoms_mu in the centre, and surrounded by unperturbed_supercell unperturbed_atoms
    :param atoms_mu: (object of the windows class-muspinism object) ASE atoms, maybe with distortions, including muon
    :param unperturbed_atoms: ASE atoms of unperturbed structure
    :param unperturbed_supercell: number of instances of unperturbed_atoms to bolt on to the end of atoms_mu
    :return: supercell of atoms_mu+unperturbed_supercell*unperturbed_atoms. If small_output==False, return ASE atoms,
             otherwise returns a list of [atom type, position]
    """
    # Retrieve the current atomic structure with the muon
    atoms_mu = simulation_object.cif_read

    # If no unperturbed_atoms are provided, use atoms_mu excluding the last atom (assumed to be the muon)
    if unperturbed_atoms is None:
        # we need to confirm that atom[-1] is the muon by convetion it is but...
        unperturbed_atoms = copy.deepcopy(atoms_mu[:-1])
    else:
        unperturbed_atoms = copy.deepcopy(unperturbed_atoms)

    # Adjust unperturbed_atoms to match the supercell dimensions of atoms_mu, if atoms_mu is already a supercell
    unperturbed_atoms = build.make_supercell(unperturbed_atoms, np.diag([1, 1, 1]) *
                                             atoms_mu.cell.lengths()[0] /
                                             unperturbed_atoms.cell.lengths()[0], wrap=False)

    # Store the muon atom for later re-insertion after constructing the supercell
    muon = copy.deepcopy(atoms_mu[-1])
    
    # Initialize output list if small_output mode is enabled
    output_list = []
    if small_output:
        output_list = [[this_atom.symbol, this_atom.position]
                       for this_atom in atoms_mu]
    
    # Remove the muon from the original structure temporaril
    del atoms_mu[-1]

    # Construct the supercell by translating and replicating unperturbed_atoms around the central cell
    for x_sign in range(-unperturbed_supercell, unperturbed_supercell + 1):
        for y_sign in range(-unperturbed_supercell, unperturbed_supercell + 1):
            for z_sign in range(-unperturbed_supercell, unperturbed_supercell + 1):
                if x_sign == y_sign == z_sign == 0: # Skip the central cell containing the muon
                    continue
                 # Calculate translation vectors for the unperturbed_atoms
                translation_vector = np.sign(x_sign) * (abs(x_sign) - 1) * unperturbed_atoms.cell[0] + \
                    np.sign(x_sign) * atoms_mu.cell[0]
                translation_vector += np.sign(y_sign) * (abs(y_sign) - 1) * unperturbed_atoms.cell[1] + \
                    np.sign(y_sign) * atoms_mu.cell[1]
                translation_vector += np.sign(z_sign) * (abs(z_sign) - 1) * unperturbed_atoms.cell[2] + \
                    np.sign(z_sign) * atoms_mu.cell[2]
                
                # Translate and append the unperturbed atoms to form the supercell
                unperturbed_atoms.translate(translation_vector)
                for this_atom in unperturbed_atoms:
                    if small_output:
                        output_list.append(
                            [this_atom.symbol, copy.deepcopy(this_atom.position)])
                    else:
                        atoms_mu.append(this_atom)
                unperturbed_atoms.translate(-1 * translation_vector)
    # Re-insert the muon at the center of the supercell
    atoms_mu.append(muon)
    if small_output:
        return output_list
    else:
        # Adjust the cell dimensions and positions to accommodate the supercell
        old_cell = atoms_mu.get_cell()
        atoms_mu.set_cell(
            old_cell*(2*unperturbed_supercell + 1), scale_atoms=False)
        atoms_mu.translate(unperturbed_supercell * old_cell[0])
        atoms_mu.translate(unperturbed_supercell * old_cell[1])
        atoms_mu.translate(unperturbed_supercell * old_cell[2])

        # Exit the old GUI and update with the new supercell structure
        simulation_object.gui_with_muon.exit()
        simulation_object.cif_read = atoms_mu
        simulation_object.cif_read = apply_mask_to_structure(
            atoms_mu, simulation_object.radius_entry.get())
        generate_cell_components_window(simulation_object)

        # Initialize a new GUI with the supercell
        simulation_object.images_supercell = Images()
        simulation_object.images_supercell.initialize([atoms_mu])
        simulation_object.gui_supercell = GUI(simulation_object.images_supercell)
        simulation_object.gui_supercell.run()

def apply_mask_to_structure(atoms_mu: atoms, radius: float)->atoms:
    '''
    Applies a spherical mask to the atoms object, selecting atoms within a specified radius from the muon.
    
    Parameters:
    atoms_with_muon: ASE atoms object containing the structure, including the muon.
    cutoff_radius: Radius within which atoms are selected relative to the muon's position.

    Returns:
    ASE atoms object containing only the atoms within the specified radius from the muon
    '''
    # Get the position of the muon (assumed to be the last atom in the structure)
    center = atoms_mu[-1].position

    # Calculate the distances of all atoms from the muon's position and create a mask for atoms within the radius
    mask = np.linalg.norm(atoms_mu.positions - center, axis=1) < int(radius)
    
    # Apply the mask to select the atoms within the specified radius
    selected_atoms = atoms_mu[mask]

    # Print the selected atoms and display them in the viewer
    print(selected_atoms)
    view(selected_atoms)

    return selected_atoms

def update_structure_data(simulation_object, iso=None):
    '''
    Updates the structure data by calculating the relative positions, magnetic moments, 
    and field strengths of atoms relative to the muon in the structure.

    Parameters:
    simulation_object: Object containing the atomic structure and simulation parameters.
    isotope: The isotope to use for calculating gyromagnetic ratio and spin. If None, defaults to standard values.
    '''
    # Initialize the structure data list to store information about each atom in the structure
    simulation_object.structure_data = []
    
    # Retrieve the position of the muon, assumed to be the last atom in the structure
    mu_position = simulation_object.cif_read[-1].position
    print('muon positon', mu_position)
    
    # Iterate over each atom in the structure to calculate its relative position, magnetic moment, and field strength
    for atom in simulation_object.cif_read:
        # Get the element symbol of the atom
        element_symbol = atom.symbol

        # Calculate the relative position of the atom with respect to the muon's position
        relative_postision = atom.position-mu_position
        print(atom.symbol, relative_postision, '@', atom.position)
        
        # If the atom is the muon (assumed to be labeled 'X'), rename the element symbol to 'mu'
        if element_symbol == 'X':
            element_symbol = 'mu'
        # Calculate the magnetic moment of the atom based on its element and isotope
        magnetic_moment = gyromagnetic_ratio(
            element_symbol, iso)*spin(element_symbol, iso)

        # Calculate the distance from the muon to the atom
        distance_to_muon = np.linalg.norm(relative_postision)

        # Calculate the magnetic field strength; if the atom is the muon itself, set the strength to 0
        if distance_to_muon == 0:
            strength = 0
        else:    
            strength = abs(magnetic_moment/distance_to_muon**3)

        # Gather information about the atom: element symbol, field strength, relative position, spin, and distance
        atom_info = (atom.symbol, strength, relative_postision,
                spin(element_symbol, iso), distance_to_muon)
        
        # Update the structure information 
        simulation_object.structure_data.append(atom_info)

def generate_cell_components_window(class_instance):
    ''' 
    Creates a window to display and interact with the structure data of a class instance.
    
    This function inserts the structure data of the provided class instance into a 
    Treeview table and allows for sorting and selection of the data, which then triggers 
    updates to the dipolar interaction frame.
    
    Args:
        class_instance: An instance of a class that contains structure_data and 
                        methods for updating interactions.
    '''
    
    # Update the structure data for the class instance (with no specific isotope selected)
    update_structure_data(class_instance, iso=None)

    # create a top-level to contain the table
    top = customtkinter.CTkToplevel(class_instance)

    # Set the window icon (after a slight delay to avoid potential timing issues)
    directory = os.path.dirname(__file__)
    filename = directory+'\logo_mm.ico'
    top.after(200, lambda: top.iconbitmap(filename))
    top.title("Characterization of muon stopping site")

    # define elements of the table
    columns = ("#1", "#2", "#3", "#4", '#5')
    tree = ttk.Treeview(top, columns=columns, show='headings')
    
    def sort_columns(column,descending):
        '''
        Sorts the Treeview data based on the selected column.
        '''
        data = [(tree.item(item)["values"], item) for item in tree.get_children()]
        data.sort(key=lambda x: x[0][tree["columns"].index(column)], reverse=descending)

        for index, (values, item) in enumerate(data):
            tree.move(item, '', index)

        # Update the heading to allow toggling between ascending and descending sort
        tree.heading(column, command=lambda: sort_columns(column, not descending))


    # Define the column headings with sorting functionality
    tree.heading("#1", text="Symmbols",command=lambda:sort_columns('#1',False))
    tree.heading("#2", text="Strentgh",command=lambda:sort_columns('#2',False))
    tree.heading("#3", text="Position",command=lambda:sort_columns('#3',False))
    tree.heading("#4", text="Spin",command=lambda:sort_columns('#4',False))
    tree.heading("#5", text="Distance",command=lambda:sort_columns('#5',False))

    # Insert elements from the structure_data into the Treeview table
    for item in class_instance.structure_data:
        tree.insert('', 'end', values=item)

    # Initialize variables for interaction tracking
    class_instance.count_dinteractions = 0
    selected_component_indices = []

    def handle_item_selection(event):
        ''' 
        Handles the selection of an item in the Treeview.

        When an item in the 'Characterization of Muon Stopping Site' table is selected,
        this function updates the dipolar interactions frame with the selected data.
        '''

        # obtain the details of selected item
        item_details = tree.item(tree.selection()[0])
        item_values = item_details['values']

        # Clean the position data for comparison
        dipolar_interaction_string = clean_whitespace_and_brackets(
            item_values[2])

        # Find and store the index of the selected components in structure_data
        for i in range(len(class_instance.structure_data)):
            maria = clean_whitespace_and_brackets(
                str(class_instance.structure_data[i][2]))
            if dipolar_interaction_string == maria:
                if i not in selected_component_indices:
                    selected_component_indices.append(i)

                    # Update the dipolar interaction frame with the selected item
                    update_spin_dipolar_interaction(class_instance,
                                                    dipolar_interaction_string, class_instance.count_dinteractions,
                                                    selected_component_indices)

        # Update the count of dipolar interactions
        class_instance.count_dinteractions = len(
            selected_component_indices)

    # Bind the Treeview selection event to the item selection handler
    tree.bind('<<TreeviewSelect>>', handle_item_selection)

    # Pack the Treeview widget
    tree.pack(fill='both', expand=True)
    
def update_spin_dipolar_interaction(class_instance, dipolar_value_str, interaction_index, selected_component_indice):
    ''' 
    Updates the dipolar interaction with spin and dipolar interactions and updates the relevant dictionary in the class instance.

    Args:
        class_instance: An instance of a class containing the GUI elements and structure data.
        dipolar_value_str: A string representing the dipolar interaction value to be added.
        interaction_index: The index of the interaction being added.
        selected_component_indice: A list of indices representing the selected components 
                                    in the structure data.
    '''
    # clean spin entry and assert the first element to be muon
    if interaction_index == 0:
        class_instance.spins_entry.delete(0, 'end')
        class_instance.spins_entry.insert(0, 'mu ')
        try:
            # Attempt to close the GUI supercell if it exists
            class_instance.gui_supercell.exit()
        finally:
            pass
    
    # retrieve symbol of selected element
    index = selected_component_indice[-1]
    element_symbol = class_instance.structure_data[index][0]
    class_instance.spins_entry.insert('end', element_symbol+' ')

    # Create a label for the dipolar interaction
    spin_entry_position = 2+interaction_index
    label = 'dipolar_1_'+str(spin_entry_position)

    # Add the label to the frame
    str_1 = tk.StringVar()
    str_1.set(dipolar_value_str)
    add_label = tk.Label(class_instance.framess, text=label)
    add_label.pack()

    # Add dipolar interaction as an entry
    add_entry = tk.Entry(class_instance.framess, textvariable=str_1)
    add_entry.pack(pady=5)

    # Store the dipolar interaction value in the class instance's dictionary    
    class_instance.dipolar_dic[spin_entry_position] = dipolar_value_str
    #Debug print
    print(class_instance.dipolar_dic,"Dipolar distionary ")

# --------------------------------------------------------------------------------------------------------------------
#                                                     Update data
# --------------------------------------------------------------------------------------------------------------------

def update_parameters(class_instance):
    '''
    Updates the parameter of the class instance based on the UI input value.
    Retrieves the value from the field input in the GUI, and if the value is not empty, it updates the 'field' parameter

    Args:
        class_instance: An instance of a class that contains GUI elements and a parameters object.
    '''
    # Retrieve the value from the field input (assumed to be a text widget) and store it
    class_instance.first_param = class_instance.field_value.get(
        1.0, "end-1c")
    
    # If the field value is not empty, update the 'field' parameter in the parameters object
    if class_instance.first_param != '':
        class_instance.parameters._keywords["field"] = KWField(
            class_instance.first_param)

# --------------------------------------------------------------------------------------------------------------------
#                                                     DRAFT
# --------------------------------------------------------------------------------------------------------------------

def populate_gui_with_parameters(class_instance):
    '''
    Populates the GUI elements with parameter values from the class instance's parameters.

    This function reads various parameters from the class instance's parameters object and 
    updates the corresponding GUI input fields, such as name, spins, time, and field.

    Args:
        class_instance: An instance of a class that contains GUI elements and a parameters object.
    '''
    
    # Evaluate and retrieve the parameters for easier readability
    i_params = class_instance.parameters.evaluate()

    # -----------------------------------
    #               Name               #
    # Clear the current name entry and insert the name parameter value
    class_instance.name_entry.delete(0, 'end')
    class_instance.name_entry.insert('0', str(i_params['name'].value[0][0]))

    # -----------------------------------
    #               Spin               #
    # Clear the spins entry and construct a string from the spins parameter values
    class_instance.spins_entry.delete(0, 'end')
    spins_str = ''
    count = 0
    for i in i_params['spins'].value[0]:
        if count == 0:
            spins_str = i
        else:
            spins_str = spins_str+' '+i
        count = count+1

    # Insert the constructed spins string into the spins entry field
    class_instance.spins_entry.insert('0', spins_str)

    # -----------------------------------
    #               Time               #
    # Clear the time entries and populate them with time parameter values
    class_instance.time_entry1.delete(0, 'end')
    class_instance.time_entry2.delete(0, 'end')
    class_instance.time_entry3.delete(0, 'end')

    class_instance.time_entry1.insert(
        'end', str(i_params['time'].value[0][0]))
    class_instance.time_entry2.insert(
        'end', str(i_params['time'].value[-1][0]))
    class_instance.time_entry3.insert(
        'end', str(len(i_params['time'].value)))

    # -----------------------------------
    #               Field              #
    # Clear the field value entry and construct a string from the field parameter values
    #class_instance.field_value.delete(0, 'end')
    field_str = ''
    count = 0
    for i in i_params['field'].value[0]:
        # print(i)
        if count == 0:
            field_str = i
        else:
            field_str = field_str+' '+i
        count = count+1

    # Insert the constructed field string into the field entry field
    class_instance.field_value.insert('end', field_str)

    # -----------------------------------
    #            Polarization          #

    # Placeholder for potential future code to handle polarization and couplings
    # Currently, these sections are not implemented but can be added later as needed

    # -----------------------------------
    #               Couplings              

    # -----------------------------------
    #                   Dipolar          #
    # Placeholder for handling dipolar couplings
    # Implementation can be added later as required

def update_param_spec(class_instance):
    '''
    Updates the parameters used for generating simulations.

    Args:
        class_instance: An instance of a class that contains parameters and fitting data
    '''
    # Update the 'field' parameter with the fitting parameters used for simulation
    class_instance.parameters._keywords["field"] = KWField(
        class_instance.fit_params_to_generate_simulation)
    
    # Evaluate the parameters to update the internal state
    i_params = class_instance.parameters.evaluate()

    # Print statements to debug and confirm the fitting variables and updated field parameter
    print('//////fitting variables', class_instance.fit_params_to_generate_simulation)
    print('***the', i_params['field'].value[0])
    
# ---------------------------------------------------------------------------------------------------------------------
#                                       Auxiliary Functions
# --------------------------------------------------------------------------------------------------------------------
def safely_destroy_progress_bar(handler):
    #safely_destroy_progress_bar
    '''
    Safely attempts to destroy the progress bar widget. 
    If the destruction fails, an error message is printed.
    '''
    try:
        handler.processBar.destroy()
    except:
        print('Failed to destroy process bar')

def handle_active_thhread():
    ''' 
    Prints information about all currently active threads, including their names 
    and statuses. Also identifies the thread from which the message originated.
    '''
    # Get a list of all active threads
    active_treads=threading.enumerate()
    # Print the number of active threads
    print(f'Currently there are {len(active_treads)} threads active')

    # Iterate over each thread and print its name and status
    for i in active_treads:
        print(f' Thread name: {i.name}, alive: {i.is_alive()}')

    # Print the thread from which this log was generated
    print(f'This message was originated from the following thread {threading.current_thread()}')



def show_selected_options(handler):
    if handler.selected_items:
        options = "\n".join(handler.selected_items)
        tk.messagebox.showinfo("Selected Options", f"Selected Options:\n{options}")
    else:
        tk.messagebox.showinfo("Selected Options", "No options selected.")

def clear_selected_options(handler):
    '''
    Clears the list of selected items and updates the corresponding label in the UI.
    Args:(object): An instance of a class that contains the list of selected items and the label to update.
    '''
    # Clear the list of selected items
    handler.selected_items=[]

    # Update the label to reflect the cleared selection
    handler.label_of.configure(text=handler.selected_items)

def run_simulation_thread(handler):
    """
    Loads an input file if none is loaded, updates parameters if necessary, 
    and starts a new thread that runs the simulation
    """
    # Immediately create a progress bar to signal the ongoing background process
    create_processBar(handler)
    
    # DEBUG: Print the current state before running the simulation
    print('################################ INSIDE RUN SIMULATION PROGRESS BAR HAS BEEN CREATED',handler.fit_params_to_generate_simulation, handler.fit_state,handler.parameters.evaluate())

    # Load an input file if none is present
    if handler.input_txt_file == ' ':
        load_input_file(handler)

    # Update parameters if not in a fitting state
    if handler.fit_state == None:
        update_parameters(handler)

    # Create and start a new thread to run the simulation
    # DEBUG: Print the current state before entering the simulation thread
    print('################################ ABOUT TO ENTER THE THREA TO SIMULATE AND POST',handler.fit_params_to_generate_simulation, handler.fit_state,handler.parameters.evaluate())
    run_simulation_thread_0 = Thread(target=execute_simulation_and_trigger_event,
                         args=(handler,), daemon=True)
    run_simulation_thread_0.start()

def load_and_run(handler):
    """
    Loads input file and starts new thread to run simulation
    only depending on the input file (offers limited interaction)
    """
    # Immediately create a progress bar to signal the ongoing background process
    create_processBar(handler)
    
    # Load the input file
    load_input_file(handler)

    # Create and start a new thread to run the simulation
    run_simulation_thread_1 = Thread(target=execute_simulation_and_trigger_event,
                         args=(handler,), daemon=True)
    run_simulation_thread_1.start()

def read_UI_entries_and_run(handler):
    """
    Reads the entries from the GUI (kEntries) and starts a new thread to run the simulation.
    """
    # Immediately create a progress bar to signal the ongoing background process
    create_processBar(handler)

    # DEBUG: Print the current fit state before processing entries
    print('#################################################################################################',handler.fit_state)
    
    
    if handler.fit_state==None:
        print('bananana')
        #r_e.initialize_simulation_parameters(handler)
        pass
           

    # Create and start a new thread to run the simulation    
    run_simulation_thread_2 = Thread(target=execute_simulation_and_trigger_event,
                         args=(handler,), daemon=True)
    run_simulation_thread_2.start()

def execute_simulation_and_trigger_event(handler):
    '''
    Executes the simulation and triggers an event to send results or display them on a graph upon completion.

    Args:handler (object): An instance of a class that manages the simulation parameters and event handling.
        _ (any): Placeholder for additional arguments that might be passed when the function is invoked as an event handler.
    '''
    # Runs the simulation
    run_simulation(handler)
        
    # DEBUG: Print the current state after the simulation has run
    print('################################ ENTERED THE THREAD AND THE SIMULATION HAS RUN',handler.fit_params_to_generate_simulation, handler.fit_state,handler.parameters.evaluate(),'results',handler.results)

    # Trigger an event indicating that the simulation thread has finished
    handler.event_generate('<<ThreadFinished>>')

def create_processBar(handler):
    '''
    Creates a progress bar and displays it in the main root window.

    Args: handler (object): An instance of a class that manages the UI elements, including where the progress bar will be displayed.
    '''
    # Initialize the progress bar with horizontal orientation and indeterminate mode
    handler.processBar = Progressbar(handler,
                               orient='horizontal', mode='indeterminate', length=300)
    
    # Position the progress bar within the main window
    handler.processBar.place(x=280, y=185) 

    # Start the progress bar animation
    handler.processBar.start()

def store_tkentries(handle):
    '''
    Stores various Tkinter entry widgets and other values into the 'kEntries' list.
    Organizes the entries by index, corresponding to the first 22 atomistic parameters in MuSpinSim.
    '''
    
    handle.kEntries[0] = handle.name_entry
    handle.kEntries[1] = handle.spins_entry
    handle.kEntries[2] = [handle.time_entry1,
                            handle.time_entry2, handle.time_entry3]
    handle.kEntries[3] = handle.field_value
    handle.kEntries[4] = handle.intrisic_field_value
    handle.kEntries[5] = handle.polarization_value
    handle.kEntries[6] = handle.buffer_entry
    handle.kEntries[7] = handle.orientation_value
    handle.kEntries[8] = handle.buffer_entry
    handle.kEntries[9] = handle.zeeman_value
    handle.kEntries[10] = handle.buffer_entry
    handle.kEntries[11] = handle.quadrupolar_value
    handle.kEntries[12] = handle.hyperfine_value
    handle.kEntries[13] = handle.x_axis_value
    handle.kEntries[14] = handle.y_axis_value
    handle.kEntries[15] = handle.celio_value
    handle.kEntries[16] = handle.buffer_entry
    handle.kEntries[17] = handle.fitting_variables_values
    handle.kEntries[18] = handle.buffer_entry
    handle.kEntries[19] = handle.fitting_method
    handle.kEntries[20] = handle.fitting_tolerance_value
    handle.kEntries[21] = handle.experiments
    handle.labels = ['name', 'spins', 'time', '']