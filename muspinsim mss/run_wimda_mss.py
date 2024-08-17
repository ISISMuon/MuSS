"""
Project: Simulations for muSR data Analysis Industrial Placement
Author: Paula Franco
Date: May 2024

Summary:
This script is specifically to be used with wimda as the server is being initiated
before the windows being called (thats the only difference).
"""
# -------------------------------------
#       Homemade scripts
# -------------------------------------

from window_class_mss import windows
import socket_comunication_mss as sck
import os
import ctypes

myappid = 'mycompany.myproduct.subproduct.version'  # arbitrary string
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

if __name__ == "__main__":
    App = windows()
    sck.server_connection_tread(App)
    dir = os.path.dirname(__file__)
    print(dir)

    filename = dir+'\logo_muss_32.ico'
    App.iconbitmap(filename)
    # App.deiconify()
    App.mainloop()
