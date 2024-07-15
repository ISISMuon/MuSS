'''
GOAL: Integrating GUI of the atoms in ase an already built in GUI tkinter
'''


import io
import io  # Correct import for BytesIO
from PIL import Image, ImageTk
from ase.visualize.plot import plot_atoms
from tkinter import Frame, Label
import threading
from ase.gui.gui import GUI
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import numpy as np
import tkinter as tk
from tkinter import Frame, Button
import ase
from ase.build import bulk
from ase.visualize import view

# --------------------------------------------------------------------------------------------------------------------
#                                           The file
# --------------------------------------------------------------------------------------------------------------------
file = ase.io.read(r'c:\Users\BNW71814\Desktop\EntryWithCollCode60559.cif')

# --------------------------------------------------------------------------------------------------------------------
#                                 Trial 1
# --------------------------------------------------------------------------------------------------------------------


def start_visualize_view01():
    # Create an Atoms object (example: bulk aluminum)
    atoms = file

    # Open ASE interactive viewer
    view(atoms)


def start_tkinter_with_visualize_view_01():
    # Create a Tkinter window
    root = tk.Tk()
    root.title("trial 02")

    # Frame to hold the button
    frame = Frame(root, width=800, height=600)
    frame.pack()

    # Button to start ASE interactive viewer
    start_viewer_button = Button(
        frame, text="Start ASE Viewer", command=start_visualize_view01)
    start_viewer_button.pack()

    # Start the Tkinter main loop
    root.mainloop()


# Call the function to start Tkinter with ASE viewer integration
def trial_01():
    print('This is the dinamic depicture of what we get with ase')
    start_tkinter_with_visualize_view_01()


# trial_01()
# --------------------------------------------------------------------------------------------------------------------
#                                 Trial 2
# --------------------------------------------------------------------------------------------------------------------


def visualize_atoms_3d_02(atoms, ax):
    """Visualize Atoms object in a 3D plot."""
    positions = atoms.get_positions()
    symbols = atoms.get_chemical_symbols()

    for pos, symbol in zip(positions, symbols):
        ax.scatter(pos[0], pos[1], pos[2], label=symbol, s=100)

    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.legend()


def start_3d_visualization_02():
    # Create a Tkinter window
    root = tk.Tk()
    root.title("trial 02")

    # Frame to hold the button and plot
    frame = Frame(root, width=800, height=600)
    frame.pack()

    # Create an Atoms object (example: bulk aluminum)

    # Create a 3D plot
    fig = plt.Figure(figsize=(8, 6))
    ax = fig.add_subplot(111, projection='3d')
    visualize_atoms_3d_02(file, ax)

    # Embed the plot into Tkinter
    canvas = FigureCanvasTkAgg(fig, master=frame)
    canvas.draw()
    canvas.get_tk_widget().pack()

    # Start the Tkinter main loop
    root.mainloop()


# Call the function to start 3D visualization
def trial_02():
    print('this is trial 2: This is a repressentation in 3d cartesian using matplotlib completly static ')
    start_3d_visualization_02()


# trial_02()
# --------------------------------------------------------------------------------------------------------------------
#                                 Trial 3
# --------------------------------------------------------------------------------------------------------------------


def visualize_atoms_3(atoms):
    """Visualize the Atoms object and save it as an image."""
    fig, ax = plt.subplots()
    plot_atoms(atoms, ax=ax, show_unit_cell=2, scale=0.5)
    buf = io.BytesIO()
    fig.savefig(buf, format='png')
    buf.seek(0)
    plt.close(fig)
    return Image.open(buf)


def display_atoms_in_frame_03(atoms, frame):
    """Display the Atoms object in a Tkinter frame."""
    img = visualize_atoms_3(atoms)
    img_tk = ImageTk.PhotoImage(img)
    label = Label(frame, image=img_tk)
    label.image = img_tk  # Keep a reference to avoid garbage collection
    label.pack()


def trial_03():
    # Create the Tkinter application
    print('trial 3: this uses the adequate imagne but id the static versio represented in a 2d cartesian coordinates')
    root = tk.Tk()
    root.title("trial03")

    # Create a frame to hold the visualization
    frame = Frame(root, width=800, height=600)
    frame.pack()

    # Display the Atoms object in the Tkinter frame
    display_atoms_in_frame_03(file, frame)

    # Start the Tkinter main loop
    root.mainloop()


# =================================================================================================================
#                                 Run Files
# --------------------------------------------------------------------------------------------------------------------

trial_03()
