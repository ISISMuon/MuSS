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


if __name__ == "__main__":
    App = windows()
    sck.server_connection_tread(App)
    App.mainloop()
