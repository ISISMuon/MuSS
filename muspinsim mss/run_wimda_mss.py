"""
Project: Simulations for muSR data Analysis Industrial Placement
Author: Paula Franco
Date: May 2024

Summary:
This script is specifically to be used with wimda as the server is being initiated
before the windows being called (thats the only difference).
"""
import os
import ctypes

# -------------------------------------
#       Homemade scripts
# -------------------------------------
from window_class_mss import MuSS_window
import socket_comunication_mss as sck


# make the logo-icon appear in  the taskbar on windows
myappid = 'mycompany.myproduct.subproduct.version'  # arbitrary string
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

if __name__ == "__main__":
    
    App = MuSS_window()

    # the server is initiated ans listening
    sck.server_connection_tread(App)

    #get the current directory as to create relative path for icon
    dir = os.path.dirname(__file__)
    filename = dir+'\logo_muss_32.ico'
    App.iconbitmap(filename)
    
    # the loop where the progran is running
    App.mainloop()
