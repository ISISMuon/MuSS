Welcome to MuSS' documentation
==============================

Muon Simulation Study MuSS is an interface that combines the capabilities of MuSpinSim and WiMDA. The idea is to use simulation to inform musr data analysis.
MuSS can be viewed as an outer layer of of MuSpinSim with additional capabilities for comunication with WiMDA. The communication is socket-based allowing flow of data in both directions.



MuSS capabilities:
------------------

- MuSS as a fitting function on WiMDA.

The most fundamental goal of MuSS is to use Muspinsim as one of the fiiting functions of WiMDA allowing the fiiting parameters to be atomistic varaiables,
meaning that their value reflect a physical quantity. Those atomistic variables are contained within the input of MuSpinSim. 

- MuSS as an interface for MuSpinSim.
The goal with MuSS has been to perverse the capabilities of MuSpinSim adding communication with WiMDA.
Note that MuSpinSim has more suitable interface built within Muon Galaxy when intended to be used without socket-based communication.

- MuSS as a socket server.
One of the first operation the program executes is start a server and listen to incomingg clients to be connected with.
It has the capacity of listening to multiple clients and it will print in the terminal the messages received. 
However, the messages that WiMDA will send have keywords in the script that recognize the message and according to the keyword an operation succedes.



Key Features
------------

- User-friendly interface for seamless operation.
- Integrated simulation and fitting tools.
- Real-time data exchange via socket-based communication.

Work in progress
----------------

MuSS is a work in progress and we encourage collaboration and support!
You are welcome to contribuite in our Github.