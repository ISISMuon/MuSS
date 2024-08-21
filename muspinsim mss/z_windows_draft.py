#trying for scrolable thingy
import tkinter as tk
from tkinter.ttk import Label, LabelFrame, Progressbar, Style
import customtkinter
from tkinter import filedialog
from muspinsim.input.keyword import *

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure

import os
from threading import Thread
import ase
from ase.gui.images import Images
from ase.gui.gui import GUI
# -------------------------------------
#       Homemade scripts
# -------------------------------------

# from input_class import Create_Input
import backend_mss as bck
import socket_comunication_mss as sck
import read_entries as r_e

class windows(tk.Tk):
    ''' '''

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        
        # -------------------------------------------------------------------------------------------------------
        #                           Geometry of the window
        # -------------------------------------------------------------------------------------------------------
        self.title("MuSS")
        self.geometry("1000x800")
        self.minsize(200, 200)

        
        # ------------------------------------------------------------------------------------------------------
        #                           Queing (in case is necessary)
        # ------------------------------------------------------------------------------------------------------
        self.bind("<<ThreadFinished>> ", self.thread_stopped)
        self.bind("<<SendResultStored>>", self.send_result_tored)
        
        # ------------------------------------------------------------------------------------------------------
        #                                   Esentials
        # ------------------------------------------------------------------------------------------------------
        self.file = ' '
        self.doing = None  # ?
        self.parameters = None
        self.first_param = 17.3
        

        self.Input_path = tk.StringVar()
        self.username = os.path.expanduser('~')

        self.Input_path.set(self.username+'\Documents')

        # ----------------------------------------------------------------------------------------------------------
        #                                   Calling the Frames
        # ----------------------------------------------------------------------------------------------------------
        self.create_scrollable_frame()
        self.menus()
        #self.frame_socketa(self.scrollable_frame)
        self.frame_field(self.scrollable_frame)
        #self.frame_plot(self.scrollable_frame)
        #self.frame_essential(self.scrollable_frame)

    # --------------------------------------------------------------------------------------------------------------------
    #                                   Defining frames
    # --------------------------------------------------------------------------------------------------------------------
    def create_scrollable_frame(self):
        # Create a canvas widget
        canvas = tk.Canvas(self)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Add a scrollbar to the canvas
        scrollbar = tk.Scrollbar(self, orient=tk.VERTICAL, command=canvas.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Configure the canvas
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox('all')))

        # Create a frame inside the canvas
        self.scrollable_frame = tk.Frame(canvas)
        canvas.create_window((0, 0), window=self.scrollable_frame, anchor='nw')

    def frame_essential(self,parent):
        self.frame_essentials = LabelFrame(parent, text="Essential", width=100)
        self.frame_essentials.place(x=20, y=20)
        # -contain errors
        self.buffer_entry = customtkinter.CTkEntry(
            self.frame_essentials)
        #
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
        

        self.cif_check = customtkinter.CTkLabel(
            self.frame_essentials, text="Cif File")
        self.cif_check.grid(row=3, column=0, padx=5, pady=5)
        self.cif_btn = customtkinter.CTkButton(
            self.frame_essentials, text="Load", command=lambda: self.frame_structure(), width=40)
        self.cif_btn.grid(row=3, column=1, padx=5, pady=5)

    def frame_plot(self,parent):
        self.frame_plot = LabelFrame(parent, text="Plot", width=900, height=900)
        self.frame_plot.place(x=250, y=150)

        self.runBtn = customtkinter.CTkButton(
            parent, text='Run', command=self.read_run, width=64, height=30)
        # self, text='Run', command=self.run_thread_btn, width=64, height=30)
        self.runBtn.place(x=670, y=175)

        self.selecBtn = customtkinter.CTkButton(
            parent, text='Fit Select', command=self.run_thread_btn, width=64, height=30)
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

    def frame_field(self,parent):
        self.field_frame = LabelFrame(parent, text="Field")
        self.field_frame.place(x=20, y=270)

        self.zeeman_label = customtkinter.CTkLabel(
            self.field_frame, text="zeeman")
        self.zeeman_label.grid(row=0, column=0, padx=5, pady=5)

        self.zeeman_value = tk.Text(
            self.field_frame, width=15, height=3, bd=0,)
        self.zeeman_value.grid(row=0, column=2, padx=5, pady=5)
        
        '''def dipolar_frame(a):
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

        self.framess = dipolar_frame(self.field_frame)'''

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

    def frame_socketa(self,parent):
        self.socketa = LabelFrame(parent, text="Socket")
        self.socketa.place(x=780, y=520)

        self.host_label = customtkinter.CTkLabel(self.socketa, text="Host")
        self.host_label.grid(row=1, column=0, padx=5, pady=5)
        self.host_entry = customtkinter.CTkEntry(self.socketa, width=100)
        self.host_entry.insert('end', 'localhost')
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

        self.file_menu.add_command(
            label="Load and Run", command=lambda: self.load_run())
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

    def load_run(self):
        self.loading_bar()
        bck.load_file(self)
        thread2 = Thread(target=self.run_btn,
                         args=(self,), daemon=True)
        thread2.start()

    def read_run(self):
        r_e.iniciate_params01(self)
        thread2 = Thread(target=self.run_btn,
                         args=(self,), daemon=True)
        thread2.start()
        pass

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
        print('inside stopping thread')
        # self.bar.destroy()
        print('process bar shoulfd have stopped')

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

# -------------------------------------------------
#           Run te tkinter window
# ------------------------------------------------
def create_scrollable_frame(root):
    # Create a canvas widget
    canvas = tk.Canvas(root)

    # Create a frame widget inside the canvas
    frame = tk.Frame(canvas)

    # Create vertical and horizontal scrollbars
    vsb = tk.Scrollbar(root, orient="vertical", command=canvas.yview)
    hsb = tk.Scrollbar(root, orient="horizontal", command=canvas.xview)

    # Configure the canvas to use the scrollbars
    canvas.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

    # Pack the scrollbars and the canvas
    vsb.pack(side="right", fill="y")
    hsb.pack(side="bottom", fill="x")
    canvas.pack(side="left", fill="both", expand=True)

    # Create a window in the canvas to hold the frame
    canvas_frame = canvas.create_window((0, 0), window=frame, anchor="nw")

    # Update the scroll region whenever the frame size changes
    def on_frame_configure(event):
        canvas.configure(scrollregion=canvas.bbox("all"))

    # Update the frame width to match the canvas width
    def on_canvas_configure(event):
        canvas.itemconfig(canvas_frame, width=event.width)

    frame.bind("<Configure>", on_frame_configure)
    canvas.bind("<Configure>", on_canvas_configure)

    return frame

if __name__ == "__main__":
    App=windows()
    App.mainloop()