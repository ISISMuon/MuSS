"""
Project: Simulations for muSR data Analysis Industrial Placement
Author: Paula Franco
Date: December 2023

Summary:
This script is (a front-end GUI) an aid for MuSpinSim users, eliminating the necessity to write MuSpiSim script to run the program (for example run simulations).
The concept applied here is to have as entry all MuSpinSpim variables and be able to use all functionalities of MuSpiSim.
https://muon-spectroscopy-computational-project.github.io/muspinsim/ --> For information on MSS

code structure:
    *The GUI is defined as the Windows class that inherit from tkinter.
    *In the init function the tkinter window geometry is described and the functions that defined the essential frames are called.

    Additional Scripts:
        + muspinsim:
            as this GUI is made for MSS it is all based in MSS code and its only a chanel to make the usage easier
        + tkinter_muspinsim01backend as bck:
            which is where other functions are defined describing the calculations, data processing, file reading, interpretation of data
        + sockets_tk as sck :
           sockets are created and listens until the program is closes, here ports are descibed. The sockets recieve and send informtaion here.
    Run
        To run this script run_guy_2 is used as to tailor this to faster wimda comunication. Therefore, the .py file that runs in wimda is 'run_guy_2'
"""

import tkinter as tk

from tkinter.ttk import Label, LabelFrame, Progressbar, Style, Combobox
import customtkinter
from tkinter import filedialog
from muspinsim.input.keyword import *

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure

import os
from threading import Thread
import threading
import ase
from ase.gui.images import Images
from ase.gui.gui import GUI

# -------------------------------------
#       Homemade scripts
# -------------------------------------
import backend_mss as bck
import socket_comunication_mss as sck


class MuSS_window(tk.Tk):
    ''' 
     MuSS_window is the 'chassis' for the MuSS progarm
     The object of this class has tkinter methods and also the atomistic parameters
     All major frames are defined (in the Defining Frames section ) here and the entries are stored accoring to the muspinsim indexing of parameters
     The main functionalities are defined in the Auxiliary functions but the are built on top (or referencing) of other functions defined in the backend
        Note:
        Creation of thread to peform calculation so the GUI does not freeze 
        The Tkinter version used here is a single thread GUI so eveything depening on the UI must run on the main thread (but the object can be referenced in other threads)
    Run this script: create a MuSS_window object and run tkinter mainloop 
    :) 
    '''

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        
        # -------------------------------------------------------------------------------------------------------
        #                           Geometry of the window
        # -------------------------------------------------------------------------------------------------------
        self.title("MuSS")
        self.geometry("1000x800")
        self.minsize(200, 200)
        # ------------------------------------------------------------------------------------------------------
        #                           Bind Functions
        # ------------------------------------------------------------------------------------------------------
        self.bind("<<ThreadFinished>> ", self.handle_simulation_thread_completion)
        # ------------------------------------------------------------------------------------------------------
        #                                           Variables Initiated
        # ------------------------------------------------------------------------------------------------------
        self.kEntries = [None]*22  # Refering to all tkentries possible in muspinsim (collectively store the entries by index)
        # label of te muspinsim possible entries in order
        self.labelstring = ['name', 'spins', 'time', 'field', 'intrinsic_field', 'polarization', 'average_axis', 'orientation', 'temperature',
                            'zeeman', 'dipolar', 'quadrupolar', 'hyperfine', 'x_axis', 'y_axis', 'celio', 'dissipation', 'fitting_variales',
                            'fitting_data', 'fitting_method', 'fitting_tolerance', 'experiments']
        self.couplings=['zeeman', 'dipolar', 'quadrupolar', 'hyperfine']
        self.fittable_atomistic_parameters=['field', 'intrinsic_field', 'polarization', 'average_axes','orientation',self.couplings, 'temperature','celio', ]

        self.dipolar_dic = {} #stored the dipolar interaction distances with the key as the number of interaction
        #(why not combine fitting history with result_dic)

        # store the simulated data, indices are number of the fitting loop [0]=initials values
        self.fitting_history = []  #
         # store  the variables and time and results, key of the dictionary is the list of parameters
        self.result_dic = {}   
        #change the name to fitting_para
        # fit_params_to_generate_simulation is the variable  that contains the value of the variable that has been senf from wimda to MuSS to generate new simulation data 
        self.fit_params_to_generate_simulation = ' '        
        # checks if the fitting is occuring (None in the first run, True when fitting)
        self.fit_state = None               
        # array with wimda times (x-values) to do the interpolation in muspinsim
        self.wimda_time = None
                 
        
        # ------------------------------------------------------------------------------------------------------
        #                                   Esentials
        # ------------------------------------------------------------------------------------------------------
        self.input_txt_file = ' '
        self.parameters = None
        self.first_param = 17.3 #To be erased
        

        #this allows to save and open files in user´s documents 
        self.save_path = tk.StringVar() 
        self.username = os.path.expanduser('~')
        self.save_path.set(self.username+'\Documents')
        # ----------------------------------------------------------------------------------------------------------
        #                                   Calling the Frames
        # ----------------------------------------------------------------------------------------------------------

        self.menus()
        self.frame_essential()
        self.frame_socketa()
        self.frame_field()
        self.frame_plot()
        #self.frame_fit_selection()

        #retrives the path and gives the name of the file
        path = bck.get_path(self)
    # --------------------------------------------------------------------------------------------------------------------
    #                                   Defining frames
    # --------------------------------------------------------------------------------------------------------------------

    def frame_essential(self):
        """ 
        Creates the Essntial frame in the UI containing name, spins, time range 
        and the capability to load a cif file
        """
        # Create the frame that will contain thw widgets defined here
        self.frame_essentials = LabelFrame(self, text="Essential", width=100)
        self.frame_essentials.place(x=20, y=20)

        # Placeholder for buffer entry, necessary for kEntries (Temporary)
        self.buffer_entry = customtkinter.CTkEntry(
            self.frame_essentials)
        
        # param: name entry, label and default  
        self.name_label = customtkinter.CTkLabel(
            self.frame_essentials, text="Name")
        self.name_label.grid(row=0, column=0, padx=5, pady=5)
        self.name_entry = customtkinter.CTkEntry(self.frame_essentials)
        # Insert default text 'simulation_1' in the name entry field
        self.name_entry.insert('end', 'simulation_1')
        self.name_entry.grid(row=0, column=1)
        
        # Create a label and entry field for 'spins'
        self.spins_label = customtkinter.CTkLabel(
            self.frame_essentials, text="spins")
        self.spins_label.grid(row=1, column=0, padx=5, pady=5)
        self.spins_entry = customtkinter.CTkEntry(self.frame_essentials)
        # Insert default text 'mu e' in the spins entry field
        self.spins_entry.insert('end', 'mu e')
        self.spins_entry.grid(row=1, column=1, padx=5, pady=5)

        # Create a label for 'Time'
        self.time_label = customtkinter.CTkLabel(
            self.frame_essentials, text="Time")
        self.time_label = customtkinter.CTkLabel(
            self.frame_essentials, text="Time")
        self.time_label.grid(row=2, column=0, padx=3, pady=3)
        # Create a nested frame for time entry fields
        self.time_entry_frame = LabelFrame(self.frame_essentials, text="---")
        self.time_entry_frame.grid(row=2, column=1, padx=5, pady=5)

        self.time_entry1 = customtkinter.CTkEntry(
            self.time_entry_frame, width=40)

        self.time_entry1.insert('end', 0)
        self.time_entry1.grid(row=0, column=0, padx=5, pady=5)

        self.time_entry2 = customtkinter.CTkEntry(
            self.time_entry_frame, width=40)
        self.time_entry2.insert('end', 32)
        self.time_entry2.grid(row=0, column=1, padx=5, pady=5)

        self.time_entry3 = customtkinter.CTkEntry(
            self.time_entry_frame, width=40)
        self.time_entry3.grid(row=0, column=2, padx=5, pady=5)
        self.time_entry3.insert('end', 100)
       
        # Create a label for CIF file loading functionality
        self.cif_check = customtkinter.CTkLabel(
            self.frame_essentials, text="Cif File")
        self.cif_check.grid(row=3, column=0, padx=5, pady=5)
        # Create a button to load CIF files, triggering the frame_structure method when clicked
        self.cif_btn = customtkinter.CTkButton(
            self.frame_essentials, text=" Cif Load", command=lambda: self.frame_structure(), width=40)
        self.cif_btn.grid(row=3, column=1, padx=5, pady=5)

    def frame_plot(self):
        """
        Sets up the 'Plot' frame for displaying graphs and providing user interaction 
        buttons Run.
        """
        # Frame titled 'Plot'containing the graphs
        self.frame_plot = LabelFrame(self, text="Plot", width=900, height=900)
        self.frame_plot.place(x=250, y=150)

        # Create a 'Run' button that runs simulation in a thread
        self.runBtn = customtkinter.CTkButton(
            self, text='Run', command=lambda:bck.read_UI_entries_and_run(self), width=64, height=30)
        self.runBtn.place(x=670, y=175)

        # Initialize a Matplotlib figure object with a 5x5 inch size and a DPI (resolution) of 100
        self.figure = Figure(figsize=(5, 5), dpi=100)
        figure = self.figure
        
        # Add a subplot (axes) to the figure (111 means a single plot, occupying the entire figure space)
        self.a = figure.add_subplot(111) # neeeded


        self.canvas = FigureCanvasTkAgg(figure, self.frame_plot)
        self.canvas.draw()

        self.toolbar = NavigationToolbar2Tk(self.canvas, self.frame_plot)
        self.toolbar.update()

        self.canvas._tkcanvas.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    def frame_field(self):
        self.field_frame = LabelFrame(self, text="Field")
        self.field_frame.place(x=20, y=270)

        self.zeeman_label = customtkinter.CTkLabel(
            self.field_frame, text="zeeman")
        self.zeeman_label.grid(row=0, column=0, padx=5, pady=5)

        self.zeeman_value = tk.Text(
            self.field_frame, width=15, height=3, bd=0,)
        self.zeeman_value.grid(row=0, column=2, padx=5, pady=5)
        

        def dipolar_frame(a):
            dipolar_frame = LabelFrame(a, text="dipolar")
            dipolar_frame.grid(row=6, column=0, sticky="nsew", columnspan=3)

            canvas = tk.Canvas(dipolar_frame, width=100, height=80)
            canvas.grid(row=0, column=0, sticky="nsew")

            # Create a vertical scrollbar linked to the canvas
            scrollbar = tk.Scrollbar(
                dipolar_frame, orient="vertical", command=canvas.yview)
            scrollbar.grid(row=0, column=1, sticky="ns")

            def on_frame_configure(event):
                canvas.configure(scrollregion=canvas.bbox("all"))

            # Create a frame to hold the entries and add it to the canvas
            framess = tk.Frame(canvas)
            canvas.create_window((0, 0), window=framess, anchor="nw")
            framess.bind("<Configure>", on_frame_configure)

            # Configure scrollbar and canvas to work together
            canvas.configure(yscrollcommand=scrollbar.set)

            # Make the container expand with window resize, but keep canvas size fixed
            a.grid_rowconfigure(0, weight=1)
            a.grid_columnconfigure(0, weight=1)
            dipolar_frame.grid_rowconfigure(0, weight=1)
            dipolar_frame.grid_columnconfigure(0, weight=1)

            return framess

        self.framess = dipolar_frame(self.field_frame)

        self.field_label = customtkinter.CTkLabel(
            self.field_frame, text="field")
        self.field_label.grid(row=4, column=0, padx=5, pady=5)

        self.field_value = tk.Text(self.field_frame, width=15, height=3, bd=0,)
        self.field_value.grid(row=4, column=2, padx=5, pady=5)
        

        self.hyperfine_label = customtkinter.CTkLabel(
            self.field_frame, text="hyperfine")
        self.hyperfine_label.grid(row=2, column=0, padx=5, pady=5)

        self.hyperfine_value = tk.Text(
            self.field_frame, width=15, height=3, bd=0,)
        self.hyperfine_value.grid(row=2, column=2, padx=5, pady=5)
        

        self.quadrupolar_label = customtkinter.CTkLabel(
            self.field_frame, text="quadrupolar")
        self.quadrupolar_label.grid(row=3, column=0, padx=5, pady=5)

        self.quadrupolar_value = tk.Text(
            self.field_frame, width=15, height=3, bd=0,)
        self.quadrupolar_value.grid(row=3, column=2, padx=5, pady=5)

        self.intrisic_field_label = customtkinter.CTkLabel(
            self.field_frame, text="intrisic_field")
        self.intrisic_field_label.grid(row=5, column=0, padx=5, pady=5)

        self.intrisic_field_value = tk.Text(
            self.field_frame, width=15, height=3, bd=0,)
        self.intrisic_field_value.grid(row=5, column=2, padx=5, pady=5)

        self.celio_label = customtkinter.CTkLabel(
            self.field_frame, text="celio")
        self.celio_label.grid(row=1, column=0, padx=5, pady=5)

        self.celio_value = tk.Text(self.field_frame, width=15, height=3, bd=0,)
        self.celio_value.grid(row=1, column=2, padx=5, pady=5)

    def frame_socketa(self):
        """
        creates a labeled "Socket" frame in the UI, allowing the user to input a host and port, and providing 
        buttons to connect, disconnect, send data, and read data from a socket connection.
        """
        # Create a labeled frame named 'Socket' within the parent window
        self.socketa = LabelFrame(self, text="Socket")
        self.socketa.place(x=780, y=520)

        # Create entry and label for the HOST value
        self.host_label = customtkinter.CTkLabel(self.socketa, text="Host")
        self.host_label.grid(row=1, column=0, padx=5, pady=5)
        self.host_entry = customtkinter.CTkEntry(self.socketa, width=100)
        self.host_entry.insert('end', 'localhost')
        self.host_entry.grid(row=1, column=1, padx=5, pady=5)

        # Create an entry box for the user to input the port
        self.port_label = customtkinter.CTkLabel(self.socketa, text="Port")
        self.port_label.grid(row=2, column=0, padx=5, pady=5)
        self.port_entry = customtkinter.CTkEntry(self.socketa, width=100)
        self.port_entry.insert('end', '9092')
        self.port_entry.grid(row=2, column=1, padx=5, pady=5)

        # Set the initial state of the connect button to 'normal'
        self.statess = 'normal'

        # Create Connect that initiate the connection (if desable means server is operating)
        self.connect_btn = customtkinter.CTkButton(
            self.socketa, text="Connect", state=self.statess, command=lambda: sck.start_server_connection_thread(self), width=50)
        self.connect_btn.grid(row=3, column=1, padx=5, pady=5)

        # Create send button to send strings to the client (wimda)
        self.disconnect_btn = customtkinter.CTkButton(
            self.socketa, text="Disconnect", command=sck.close_socket_connection, width=50)
        self.disconnect_btn.grid(row=4, column=1, padx=5, pady=5)

        # Create a 'Disconnect' button to stop the socket connection
        self.send_btn = customtkinter.CTkButton(
            self.socketa, text="Send", command=lambda: sck.send_data(bck.format_simulation_data(self)), width=50)
        self.send_btn.grid(row=4, column=0, padx=5, pady=5)

        # Create read button to interpret the data recieved in the socket
        self.read = customtkinter.CTkButton(
            self.socketa, text="Read", command=lambda: sck.receive_and_process_socket_message(self), width=50)
        self.read.grid(row=3, column=0, padx=5, pady=5)

    def frame_structure(self):
        """
        Load a CIF file, display structure-related controls in a labeled frame (frame_structure), 
        and provides options to calculate the muon position, generate a supercell, and select the radius for masking
        Display views of the atoms (structure) in ase withh possibility of interaction (the first view), 
        Display a table with elements the radius at last
        """
        # Open a file dialog for the user to select a file and read it as an 'atoms' object
        file = filedialog.askopenfilename()
        self.cif_read = ase.io.read(file)

        # Create a labeled Structure frame and send to frontend
        frame_structure = LabelFrame(self, text="Structure", width=200)
        frame_structure.place(x=250, y=20)

        # Create a button to calculate the muon position
        calculate_button = customtkinter.CTkButton(frame_structure, text="Calculate Muon Position",
                                                   command=lambda: bck.selecting__nn_indices(self))
        calculate_button.grid(row=0, column=0, padx=5, pady=5)

        # Create a nested labeled frame within frame_structure, used for angle-related widgets
        frame_angle = LabelFrame(frame_structure, text='__')
        frame_angle.grid(row=1, column=0, padx=5, pady=5)
            # Create a label and entry widget for 'Phi' angle
        struc_phi_label = customtkinter.CTkLabel(
            master=frame_angle, text="Phi", width=40)
        struc_phi_label.grid(row=1, column=0, padx=5, pady=5)

        struc_phi_entry = customtkinter.CTkEntry(
            frame_angle, width=40)
        struc_phi_entry.grid(row=1, column=1)

            # Create a label and entry widget for 'Theta' angle 
        struc_theta_label = customtkinter.CTkLabel(
            master=frame_angle, text="Theta")
        struc_theta_label.grid(row=1, column=2, padx=5, pady=5)

        struc_phi_entry = customtkinter.CTkEntry(
            frame_angle, width=40)
        struc_phi_entry.grid(row=1, column=3)

        # Create a button to generate a supercell, calling 'make_supercell' when clicked
        calculate_button = customtkinter.CTkButton(frame_structure, text="Generate Supercell",
                                                   command=lambda: bck.make_supercell(self))
        calculate_button.grid(row=0, column=1, padx=5, pady=5)

        # Frameto contain the radius label and entry
        frame_options = LabelFrame(frame_structure, text='__')
        frame_options.grid(row=1, column=1, padx=5, pady=5)

        # Radius (distance to muon) on the elements to be considered
        radios_symmetry_label = customtkinter.CTkLabel(
            master=frame_options, text="Radius")
        radios_symmetry_label.grid(row=3, column=0, padx=5, pady=5)

        self.radius_entry = customtkinter.CTkEntry(
            frame_options, width=40)
        self.radius_entry.insert('end', '5')
        self.radius_entry.grid(row=3, column=1)

        # Generate the initial view of atoms in ase
        self.images = Images()
        self.images.initialize([self.cif_read])
        self.gui = GUI(self.images)
        self.gui.run()

    def menus(self):
        """
        Create the menu and the define te content:
        - File which contains save, save as, load, load and run
        - More where the hidden frames can be selected for display (Others, Axis,fitting)
        - Exit     
        """
        self.mainmenu = tk.Menu(self) # Create a main menu bar for the application

        # Create a 'File' menu and add it to the main menu bar
        self.file_menu = tk.Menu(self.mainmenu, tearoff=0)
            # To the file optio, save, save as,load and load and run are added
        self.mainmenu.add_cascade(label="File", menu=self.file_menu)
        self.file_menu.add_command(
            label="Save", command=lambda: bck.create(self))
        self.file_menu.add_command(
            label="Save As", command=lambda: bck.save_as_directory(self))
        self.file_menu.add_command(
            label="Load", command=lambda: bck.load_input_file(self))
        self.file_menu.add_command(
            label="Load and Run", command=lambda: bck.load_and_run(self))
        
        # Create a 'More' menu and add it to the main menu bar
        self.more_menu = tk.Menu(self.mainmenu, tearoff=0)
        self.mainmenu.add_cascade(label="More", menu=self.more_menu)
            # To the more option hidden frames can be added
        self.more_menu.add_command(
            label="Fitting Data", command=lambda: self.frame_data())
        self.more_menu.add_command(
            label="Show axis", command=lambda: self.frame_Axis())
        self.more_menu.add_command(
            label="Others", command=lambda: self.frame_Others())
        
        # 
        self.options_menu = tk.Menu(self.mainmenu, tearoff=0)
        self.mainmenu.add_cascade(label="Options", menu=self.options_menu)

        self.options_menu.add_command(
            label="Fitting Parameters", command=lambda: bck.fitting_options_window(self))

        self.options_menu.add_command(
            label="Create input file", command=lambda: bck.create_input_files_param(self))
        
        # Help is a way to undestand and be helped using the MuSS
        self.help_menu = tk.Menu(self.mainmenu, tearoff=0)
        self.mainmenu.add_cascade(label="Help", menu=self.help_menu)#

        # to be an hiperlink to the documentations
        self.help_menu.add_command(
            label="Documentation", command=lambda: self.frame_data())
        #Retuns information on active threads
        self.help_menu.add_command(
            label="Active Treads", command=bck.handle_active_thhread )
        #handle when the error happen in the thread so process can't stop (this is a manual temporary alternative)
        self.help_menu.add_command(
            label="Stop Process bar", command=lambda:bck.safely_destroy_progress_bar(self))

        self.mainmenu.add_command(label="Exit", command=self.destroy) #Exit the program
        
        # Configure the main window to display the created menu bar
        self.config(menu=self.mainmenu)

    def frame_Axis(self):
        """
        Axis frame created for input file for x-axis and y-axis
        """
        #Create a display the axis frame
        self.axis = LabelFrame(self, text="Axis")
        self.axis.place(x=780, y=330)

        #label and entry for x-axis
        self.x_axis = customtkinter.CTkLabel(self.axis, text="a_axis")
        self.x_axis.grid(sticky="W", row=0, column=0, padx=5, pady=5,)

        self.x_axis_value = customtkinter.CTkEntry(self.axis)
        self.x_axis_value.grid(row=1, column=0, padx=5, pady=5)
        
        # label and entry for y-axis
        self.y_axis = customtkinter.CTkLabel(self.axis, text="y_axis")
        self.y_axis.grid(sticky="W", row=2, column=0, padx=5, pady=5)

        self.y_axis_value = customtkinter.CTkEntry(self.axis)
        self.y_axis_value.grid(row=3, column=0, padx=5, pady=5)

    def frame_Others(self):
        """
        Frame contains the remaining of the 22 muspinsim entries
        orientation, polarization 
        """

        # Create the other frame 
        self.Other = LabelFrame(self, text="Other")
        self.Other.place(x=780, y=20)

        # Create a label for 'Orientation' 
        self.orientation_label = customtkinter.CTkLabel(
            self.Other, text="Orientation")
        self.orientation_label.grid(
            sticky="W", row=0, column=0, padx=10, pady=2)

        # create space label as a form to add space 
        sspace_1 = customtkinter.CTkLabel(self.Other, text="  ", height=2)
        sspace_1.grid(row=2, column=0, padx=10, pady=2)
        
        # Create entry for 'Orientation' 
        self.orientation_value = customtkinter.CTkTextbox(
            self.Other, width=100, height=50)
        self.orientation_value.grid(row=1, column=0, padx=10, pady=2)

        # polarization entry and label
        self.polarization_label = customtkinter.CTkLabel(
            self.Other, text="Polarization")
        self.polarization_label.grid(
            sticky="W", row=3, column=0, padx=10, pady=0)

        self.polarization_value = customtkinter.CTkTextbox(
            self.Other, width=100, height=50)
        self.polarization_value.grid(row=4, column=0, padx=10, pady=2)

        # create space label as a form to add space
        sspace_2 = customtkinter.CTkLabel(self.Other, text="  ", height=2)
        sspace_2.grid(row=5, column=0, padx=10, pady=2)

        #label and form to select different types of experiments
        self.experiments_label = customtkinter.CTkLabel(
            self.Other, text="experimemt")
        self.experiments_label.grid(
            sticky="W", row=6, column=0, padx=5, pady=2)
        
        self.experiments = customtkinter.CTkOptionMenu(
            self.Other, values=["None", "alc", "zero_field"])
        self.experiments.grid(row=7, column=0, padx=5, pady=5)

    def frame_data01(self, _):
        self.fitting_frame = LabelFrame(self, text="Fitting data")
        self.fitting_frame.place(x=250, y=20)

        self.fitting_variable = customtkinter.CTkLabel(
            self.fitting_frame, text="fitting variables")
        self.fitting_variable.grid(row=0, column=0, padx=5, pady=5)

        self.fitting_variables_values = tk.Text(
            self.fitting_frame, width=15, height=3, bd=0,)
        self.fitting_variables_values.grid(row=0, column=1, padx=5, pady=5)

        self.fitting_method_label = customtkinter.CTkLabel(
            self.fitting_frame, text="fitting_method")
        self.fitting_method_label.grid(row=2, column=0, padx=5, pady=5)

        self.fitting_method = customtkinter.CTkOptionMenu(
            self.fitting_frame, values=['', "nelder-mead", "lbfgs"])
        self.fitting_method.grid(row=2, column=1, padx=5, pady=5)

        self.fitting_data = customtkinter.CTkLabel(
            self.fitting_frame, text="fitting_data")
        self.fitting_data.grid(sticky="W", row=2, column=4, padx=10, pady=5)

        self.fitting_data_btn = customtkinter.CTkButton(
            self.fitting_frame, text="load", width=90)
        self.fitting_data_btn.grid(row=2, column=5, padx=10, pady=5)

        self.fitting_tolerance = customtkinter.CTkLabel(
            self.fitting_frame, text="fitting_tolerance")
        self.fitting_tolerance.grid(
            sticky="W", row=0, column=4, padx=10, pady=5)

        self.s = customtkinter.CTkLabel(self.fitting_frame, text="  ")
        self.s.grid(row=0, column=3, padx=10, pady=5)

        self.s = customtkinter.CTkLabel(self.fitting_frame, text="  ")
        self.s.grid(row=0, column=3, padx=10, pady=5)

        self.fitting_tolerance_value = customtkinter.CTkEntry(
            self.fitting_frame, width=90)
        self.fitting_tolerance_value.grid(row=0, column=5, padx=10, pady=5)

    def frame_data(self):
        self.fitting_frame = LabelFrame(self, text="Fitting data")
        self.fitting_frame.place(x=250, y=20)

        self.fitting_variable = customtkinter.CTkLabel(
            self.fitting_frame, text="fitting_variable")
        self.fitting_variable.grid(row=0, column=0, padx=5, pady=5)

        self.fitting_variables_values = tk.Text(
            self.fitting_frame, width=15, height=3, bd=0,)
        self.fitting_variables_values.grid(row=0, column=1, padx=5, pady=5)

        self.fitting_method_label = customtkinter.CTkLabel(
            self.fitting_frame, text="fitting_method")
        self.fitting_method_label.grid(row=2, column=0, padx=5, pady=5)

        self.fitting_method = customtkinter.CTkOptionMenu(
            self.fitting_frame, values=['', "nelder-mead", "lbfgs"])
        self.fitting_method.grid(row=2, column=1, padx=5, pady=5)

        self.fitting_data = customtkinter.CTkLabel(
            self.fitting_frame, text="fitting_data")
        self.fitting_data.grid(sticky="W", row=2, column=4, padx=10, pady=5)

        self.fitting_data_btn = customtkinter.CTkButton(
            self.fitting_frame, text="load", width=90)
        self.fitting_data_btn.grid(row=2, column=5, padx=10, pady=5)

        self.fitting_tolerance = customtkinter.CTkLabel(
            self.fitting_frame, text="fitting_tolerance")
        self.fitting_tolerance.grid(
            sticky="W", row=0, column=4, padx=10, pady=5)

        self.s = customtkinter.CTkLabel(self.fitting_frame, text="  ")
        self.s.grid(row=0, column=3, padx=10, pady=5)

        self.s = customtkinter.CTkLabel(self.fitting_frame, text="  ")
        self.s.grid(row=0, column=3, padx=10, pady=5)

        self.fitting_tolerance_value = customtkinter.CTkEntry(
            self.fitting_frame, width=90)
        self.fitting_tolerance_value.grid(row=0, column=5, padx=10, pady=5)

    def frame_fit_selection(self):
        '''
        The atomistic parameters to be used as fitting parameters are selected here
        '''
        self.fit_selection_frame = LabelFrame(
            self, text="Fit Selection", width=900, height=100)
    
        self.fit_selection_frame.place(x=600, y=20)

        
        self.max_selection = 3
        self.selected_items = []

        self.options = ['field', 'dipolar', 'zeeman', 'intrinsic_field', 'quadrupolar']

        self.dropdown = Combobox(self.fit_selection_frame, values=self.options)
        self.dropdown.grid(row=0, column=0,columnspan=2,padx=5, pady=5)
        #self.dropdown.pack(pady=10)
        self.dropdown.bind("<<ComboboxSelected>>",self.handle_dropdown_selection)
        
        self.label_of = customtkinter.CTkLabel(self.fit_selection_frame,text="---")
        #self.label_of.configure(state=tk.DISABLED)
        #self.show_button.pack(pady=10)
        self.label_of.grid(row=1, column=0,columnspan=2, padx=0, pady=5)

        self.show_button =customtkinter.CTkButton(self.fit_selection_frame, text="Show", command=lambda:bck.show_selected_options(self),width=50)
        #self.show_button.pack(pady=10)
        self.show_button.grid(row=2, column=0, padx=0, pady=5)

        self.clear_button = customtkinter.CTkButton(self.fit_selection_frame, text="Clear", command=lambda:bck.clear_selected_options(self),width=50)
        #self.show_button.pack(pady=10)
        self.clear_button.grid(row=2, column=1, padx=0, pady=5)

    # ---------------------------------------------------------------------------------------------------------------------
    #                                       Binded Functions
    # --------------------------------------------------------------------------------------------------------------------        

    def handle_simulation_thread_completion(self, event):
        """
        Handles actions to be performed when a simulation thread stops
        sending the data to wimda or showing it in graph (in the case no fitting is occuring)
        """
        # DEBUG: Print the current state when entering the completion handler
        print('################################ ENTERED THE HANDLE OF THINGS',self.fit_params_to_generate_simulation, self.fit_state,'PARAMETERS EVALUATED===============',self.parameters.evaluate())
        # Update the graph and retrieve timing data
        bck.graph_update_and_retrieve_time(self)
        
        # If fitting is occurring, send the formatted simulation data to WiMDA
        if self.fit_state == True:
            sck.send_data(bck.format_simulation_data(self))
        
        # Destroy the progress bar upon task completion
        self.processBar.destroy()

    def send_stored_simulation_result(self):
        """
        Sends stored simulation results to the client.
        This occurs when the simulation parameters have not changed or have changed insignificantly.
        """

        # send data to client
        sck.send_data(bck.retrieve_stored_simulation_data(self))

    def handle_dropdown_selection(self, event):
        '''Manages the selection from a dropdown menu. Adds the selected item to a list if it's not  already present, enforcing a maximum selection limit. Displays a message if a duplicate 
        selection is made.

        Args: handler (object): An instance of a class that contains the dropdown, selected items list, 
        and maximum selection limit
        '''
        # Retrieve the currently selected option from the dropdown
        selected_option = self.dropdown.get()
        
        # Check if an option was selected  
        if selected_option:
        # Ensure the selected option is not already in the selected items list
            if selected_option not in self.selected_items:
            # Check if the selected items list has reached its maximum limit
                if len(self.selected_items) >= self.max_selection:
                # Remove the oldest item
                    oldest_item = self.selected_items.pop(0)
                    
                
            # Add the newly selected option to the list
                self.selected_items.append(selected_option)
            # Optionally, clear the dropdown selection after adding the item
                self.dropdown.set('')
                
            else:
            # Show an information message if the selected option is a duplicate
                tk. messagebox.showinfo("Duplicate Selection", "This option is already selected.")
                self.dropdown.set('') # Clear the dropdown selection
    
    def rre(self):
        bck.update_param_spec(self)
        bck.read_UI_entries_and_run(self)