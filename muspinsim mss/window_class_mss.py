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
from tkinter.ttk import Label, LabelFrame, Progressbar, Style
import customtkinter
from muspinsim.input.keyword import *

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure

import os


from threading import Thread

# --------------------------------------
#       Homemade scripts
# -------------------------------------
from input_class import Create_Input
import backend_mss as bck
import socket_comunication_mss as sck


class windows(tk.Tk):
    ''' '''

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        # self.iconbitmap("mss3.ico")
        # p1 = self.PhotoImage(file='info.png')
        # print('banana')
        # path = r'C:\Users\BNW71814\Desktop\stfc-muspinsim\muspinsim mss\msss.png'
        # icon = tk.PhotoImage(file=path)
        # print('banana1')
        # self.iconphoto(True, icon)
        # self.iconphoto(False, icon)

        # -------------------------------------------------------------------------------------------------------
        #                           Geometry of the window
        # -------------------------------------------------------------------------------------------------------
        self.title("Muspinsim")
        # try and exception
        self.iconbitmap(
            r'C:\Users\BNW71814\Desktop\stfc-muspinsim\muspinsim mss\mss3.ico')

        self.geometry("1000x740")
        self.minsize(200, 200)
        # ------------------------------------------------------------------------------------------------------
        #                           Queing (in case is necessary)
        # ------------------------------------------------------------------------------------------------------
        self.bind("<<ThreadFinished>> ", self.thread_stopped)
        self.bind("<<UpdateParameters>> ", self.updat_fit)
        self.bind("<<SendResultStored>>", self.send_result_tored)
        self.bind("<<CalculateSend>>", self.run_send)
        # ------------------------------------------------------------------------------------------------------
        #                                           Variables Initiated
        # ------------------------------------------------------------------------------------------------------
        # represents all of te variables changes resgiteres by the muspinsim starting [0]=initials values
        # the history of varibles on each run stored and ready to be sent
        # the history of time and resultd on each run stored and ready to be sent
        self.hist = []  # ?????????????????
        # using a dictionary to store  the variables and time and results
        # the key of the dictionary is the list of variables each unic and the the key is the t and y results  ready to be sent
        self.result_dic = {}
        self.fitting_variables = ' '
        # fit state is varaible used  as None in the first run, True when it is needed to do some
        # calculations and be send to wimda and a number (which corresponds to the index of the time and result to be sent to wimda)
        # in the case the value already exists
        self.fit_state = None
        # This is the array with wimda time to do  the interpolation in muspinsim
        self.wimda_time = None

        # ------------------------------------------------------------------------------------------------------
        #                                   Esentials
        # ------------------------------------------------------------------------------------------------------
        self.file = ' '
        self.parameters = None

        self.first_param = 17.3
        self.frame_essential()

        # ------------------------------------------------------------------------------------------------------
        #                           Queing (in case is necessary)
        # ------------------------------------------------------------------------------------------------------
        # self.queue_results = Queue()
        # self.bind("<<CheckQueue>>", self.check_queue)

        # ------------------------------------------------------------------------------------------------------
        #                                   Esentials
        # ------------------------------------------------------------------------------------------------------
        self.file = ' '
        self.doing = None  # ?
        self.parameters = None
        self.first_param = 17.3
        self.frame_essential()

        self.Input_path = tk.StringVar()
        self.username = os.path.expanduser('~')

        self.Input_path.set(self.username+'\Documents')

        path = bck.get_path(self)
        self.inn = Create_Input(
            path, "name", "mu")

        # ----------------------------------------------------------------------------------------------------------
        #                                   Calling the Frames
        # ----------------------------------------------------------------------------------------------------------
        # self.frame_data()

        # self.frame_Axis()

        # self.frame_Others()

        self.menus()

        self.frame_socketa()

        self.frame_field()

        self.frame_plot()

        self.frame_fit_selection()

    # --------------------------------------------------------------------------------------------------------------------
    #                                   Defining frames
    # --------------------------------------------------------------------------------------------------------------------

    def frame_essential(self):
        self.frame_essentials = LabelFrame(self, text="Essential", width=100)
        self.frame_essentials.place(x=20, y=20)

        self.name_label = customtkinter.CTkLabel(
            self.frame_essentials, text="Name")
        self.name_label.grid(row=0, column=0, padx=5, pady=5)
        self.name_text = tk.StringVar()
        self.name_text.set('muspinsim01')
        self.name_entry = customtkinter.CTkEntry(
            self.frame_essentials, textvariable=self.name_text)

        self.name_entry.grid(row=0, column=1)

        self.spins_label = customtkinter.CTkLabel(
            self.frame_essentials, text="spins")
        self.spins_label.grid(row=1, column=0, padx=5, pady=5)
        self.spins_entry = customtkinter.CTkEntry(self.frame_essentials)
        self.spins_entry.insert('end', 'mu e')
        self.spins_entry.grid(row=1, column=1, padx=5, pady=5)

        self.time_label = customtkinter.CTkLabel(
            self.frame_essentials, text="Time")
        self.time_label = customtkinter.CTkLabel(
            self.frame_essentials, text="Time")
        self.time_label.grid(row=2, column=0, padx=3, pady=3)

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

        self.cif_frame = LabelFrame(self.frame_essentials)
        self.cif_frame.grid(row=3, column=1, padx=5, pady=5)
        self.cif_check = customtkinter.CTkCheckBox(
            self.cif_frame, text="Cif File")
        self.cif_check.pack()
        self.cif_radio = customtkinter.CTkRadioButton(self.cif_frame)
        self.cif_btn = customtkinter.CTkButton(
            self.cif_frame, text="Load Cif", command=bck.openn, width=40)
        self.cif_btn.pack()

    def frame_plot(self):
        self.frame_plot = LabelFrame(self, text="Plot", width=900, height=900)
        self.frame_plot.place(x=250, y=150)

        self.runBtn = customtkinter.CTkButton(
            self, text='Run', command=self.run_thread_btn, width=64, height=30)
        self.runBtn.place(x=670, y=175)

        self.selecBtn = customtkinter.CTkButton(
            self, text='Fit Select', command=self.run_thread_btn, width=64, height=30)
        self.selecBtn.place(x=590, y=175)

        self.f = Figure(figsize=(5, 5), dpi=100)
        f = self.f
        self.a = f.add_subplot(111)

        self.canvas = FigureCanvasTkAgg(f, self.frame_plot)
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

        self.dipolar_label = customtkinter.CTkLabel(
            self.field_frame, text="dipolar")
        self.dipolar_label.grid(row=1, column=0, padx=5, pady=5)

        self.dipolar_value = tk.Text(
            self.field_frame, width=15, height=3, bd=0,)
        self.dipolar_value.grid(row=1, column=2, padx=5, pady=5)

        self.field_label = customtkinter.CTkLabel(
            self.field_frame, text="field")
        self.field_label.grid(row=4, column=0, padx=5, pady=5)

        self.field_value = tk.Text(self.field_frame, width=15, height=3, bd=0,)
        self.field_value.grid(row=4, column=2, padx=5, pady=5)
        # self.field_value.get
        # self.field_value.get

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
        self.celio_label.grid(row=6, column=0, padx=5, pady=5)

        self.celio_value = tk.Text(self.field_frame, width=15, height=3, bd=0,)
        self.celio_value.grid(row=6, column=2, padx=5, pady=5)

    def frame_socketa(self):
        self.socketa = LabelFrame(self, text="Socket")
        self.socketa.place(x=780, y=520)

        self.host_label = customtkinter.CTkLabel(self.socketa, text="Host")
        self.host_label.grid(row=1, column=0, padx=5, pady=5)
        self.host_entry = customtkinter.CTkEntry(self.socketa, width=100)
        self.host_entry.insert('end', '130.246.58.40')
        self.host_entry.grid(row=1, column=1, padx=5, pady=5)

        self.port_label = customtkinter.CTkLabel(self.socketa, text="Port")
        self.port_label.grid(row=2, column=0, padx=5, pady=5)
        self.port_entry = customtkinter.CTkEntry(self.socketa, width=100)
        self.port_entry.insert('end', '9092')
        self.port_entry.grid(row=2, column=1, padx=5, pady=5)

        self.statess = 'normal'
        #
        self.connect_btn = customtkinter.CTkButton(
            self.socketa, text="Connect", state=self.statess, command=lambda: sck.server_connection_tread(self), width=50)
        self.connect_btn.grid(row=3, column=1, padx=5, pady=5)

        self.disconnect_btn = customtkinter.CTkButton(
            self.socketa, text="Disconnect", command=sck.disconnect_socket, width=50)
        self.disconnect_btn.grid(row=4, column=1, padx=5, pady=5)

        self.send_btn = customtkinter.CTkButton(
            self.socketa, text="Send", command=lambda: sck.send_function(bck.data_processing_xy(self)), width=50)
        self.send_btn.grid(row=4, column=0, padx=5, pady=5)

        self.read = customtkinter.CTkButton(
            self.socketa, text="Read", command=lambda: sck.receiver(), width=50)
        self.read.grid(row=3, column=0, padx=5, pady=5)

    def menus(self):
        self.mainmenu = tk.Menu(self)
        self.file_menu = tk.Menu(self.mainmenu, tearoff=0)
        self.mainmenu.add_cascade(label="File", menu=self.file_menu)
        self.file_menu.add_command(
            label="Save", command=lambda: bck.create(self))
        self.file_menu.add_command(
            label="Save As", command=lambda: bck.save_as(self))
        self.file_menu.add_command(
            label="Load", command=lambda: bck.load_file(self))
        # self.mainmenu.add_command(
        #    label="Fitting Data", command=lambda: self.frame_data())
        self.more_menu = tk.Menu(self.mainmenu, tearoff=0)
        self.mainmenu.add_cascade(label="More", menu=self.more_menu)
        self.more_menu.add_command(
            label="Fitting Data", command=lambda: self.frame_data())

        self.more_menu.add_command(
            label="Show axis", command=lambda: self.frame_Axis())

        self.more_menu.add_command(
            label="Others", command=lambda: self.frame_Others())
        self.mainmenu.add_command(label="Exit", command=self.destroy)

        self.config(menu=self.mainmenu)

    def frame_Axis(self):
        self.axis = LabelFrame(self, text="Axis")
        self.axis.place(x=780, y=330)

        self.x_axis = customtkinter.CTkLabel(self.axis, text="a_axis")
        self.x_axis.grid(sticky="W", row=0, column=0, padx=5, pady=5,)
        self.x_axis = customtkinter.CTkLabel(self.axis, text="a_axis")
        self.x_axis.grid(sticky="W", row=0, column=0, padx=5, pady=5,)

        self.x_axis_value = customtkinter.CTkEntry(self.axis)
        self.x_axis_value.grid(row=1, column=0, padx=5, pady=5)

        self.y_axis = customtkinter.CTkLabel(self.axis, text="y_axis")
        self.y_axis.grid(sticky="W", row=2, column=0, padx=5, pady=5)

        self.y_axis_value = customtkinter.CTkEntry(self.axis)
        self.y_axis_value.grid(row=3, column=0, padx=5, pady=5)

    def frame_Others(self):
        self.Other = LabelFrame(self, text="Other")
        self.Other.place(x=780, y=20)

        self.orientation_label = customtkinter.CTkLabel(
            self.Other, text="Orientation")
        self.orientation_label.grid(
            sticky="W", row=0, column=0, padx=10, pady=2)

        ss = customtkinter.CTkLabel(self.Other, text="  ", height=2)
        ss.grid(row=2, column=0, padx=10, pady=2)

        self.orientation_value = customtkinter.CTkTextbox(
            self.Other, width=100, height=50)
        self.orientation_value.grid(row=1, column=0, padx=10, pady=2)

        self.polarization_label = customtkinter.CTkLabel(
            self.Other, text="Polarization")
        self.polarization_label.grid(
            sticky="W", row=3, column=0, padx=10, pady=0)

        self.polarization_value = customtkinter.CTkTextbox(
            self.Other, width=100, height=50)
        self.polarization_value.grid(row=4, column=0, padx=10, pady=2)

        sss = customtkinter.CTkLabel(self.Other, text="  ", height=2)
        sss.grid(row=5, column=0, padx=10, pady=2)

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
        self.fit_selection_frame = LabelFrame(
            self, text="Fit Selection", width=900, height=100)
        self.fit_selection_frame.place(x=20, y=720)

        self.field_check = customtkinter.CTkCheckBox(
            self.fit_selection_frame, text="Field")
        self.field_check.grid(row=0, column=0, padx=5, pady=5)

        self.dipole_check = customtkinter.CTkCheckBox(
            self.fit_selection_frame, text="Dipole")
        self.dipole_check.grid(row=0, column=1, padx=5, pady=5)

        self.intrisic_check = customtkinter.CTkCheckBox(
            self.fit_selection_frame, text="Intrinsic")
        self.intrisic_check.grid(row=0, column=2, padx=5, pady=5)
        pass
    # ---------------------------------------------------------------------------------------------------------------------
    #                                       Other Functions
    # --------------------------------------------------------------------------------------------------------------------

    def run_thread_btn(self):

        self.loading_bar()
        if self.file == ' ':
            bck.load_file(self)

        if self.fit_state == None:
            bck.update_parameters(self)

        thread2 = Thread(target=self.run_btn,
                         args=(self,), daemon=True)
        thread2.start()

    def run_btn(self, _):
        '''
        Where the calculations happen
        '''

        # function2
        bck.run_simulation(self)
        self.event_generate('<<ThreadFinished>>')

    def thread_stopped(self, event):
        if self.fit_state == True:
            sck.send_function(bck.data_processing_xy(self))
        else:
            bck.graph_update(self)
        print('inside stopping thread',)
        self.bar.destroy()

    def loading_bar(self):
        self.bar = Progressbar(self,
                               orient='horizontal', mode='indeterminate', length=300)
        self.bar.place(x=280, y=185)  # x=320
        self.bar.start()

    def send_result_tored(self, _):
        '''the stored values in the dictionray of 'variables_to_fit':x and y  '''  # what happens in this function
        print('entered send stored result')  # debug
        # what is the current variables?
        # sck.send_function(bck.data_processing_xy(self))
        sck.send_function(bck.data_processing_stored(self))

    def run_send(self, _):
        '''The '''  # wat is happening in this function
        print('inside run send')  # debug

        # The parameters are updated from self.fitting_variables to self.parameters:
        bck.update_param_spec(self)
        # with the updates parameters the simulation runs
        # in the run thread there is an event that depending on the self.state_fitting will senf the results to wimda
        self.run_thread_btn()

    def interpolation(self, _):  # draft
        bck.process_time_wimda(self)  # this should give us an array of times

        pass
    # ---------------------------------------------------------------------------------------------------------------------
    #                                       Drafts
    # --------------------------------------------------------------------------------------------------------------------

    def updat_fit(self, event):

        # self.parameters._keywords["field"] = KWField(variables[0])

        bck.run_simulation(self)
        # print(self.pvar_hist)


# -------------------------------------------------
#           Run te tkinter window
# ------------------------------------------------
'''
if __name__ == "__main__":
    App=windows()
    App.mainloop()
'''
