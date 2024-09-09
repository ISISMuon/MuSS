Getting Started
===============

This section guides you through the installation process and initial setup to get MuSS running on your system.

Installation Requirements
-------------------------

1. Ensure Python is installed on your system.
2. Download and install MuSpinSim from the official repository.
3. Install dependencies:

   .. code-block:: bash

      pip install muspinsim wimda

4. Ensure WiMDA version that supports MuSS is installed on your system.


Initial Setup
-------------

- Open MuSS and configure the initial settings according to your experimental setup.
- Verify the connection settings to ensure proper integration with WiMDA.


Set up MuSS in WiMDA
--------------------

To use MuSS, you will need to have a WiMDA version that supports MuSS, available on the WiMDA GitHub.

Once you have the correct version of WiMDA, go to the MuSS GitHub and download the latest version. 
Remember the path where you saved the MuSS script. Run WiMDA as usual, and in the menu bar, click on "File" and then on "Setup" to open the "Setup" window.

In this window, most directories are defined, and you can set the directory for MuSS. In the "MuSpinSim directory" field, click the "..." button to browse to the directory where you downloaded MuSS from GitHub.

In this window, you will also see fields for "Port" and "Host". Enter the appropriate values for your communication setup:
- **Host**: Refers to the device or machine on a network, identified by an IP address or domain name. The default is `localhost`, which refers to the local machine.
- **Port**: Specifies a communication endpoint on a particular host. Ensure that you use a unique port number for this communication. The default is 9092.

Once you have set the "Host" and "Port" values, click "Done".

Now, you have MuSS set up in WiMDA. Note that, like the directory where your muon data is located, you might need to adjust the Port, Host, or MuSpinSim directory later.


My First Time Using MuSS as a Fitting Function in WiMDA
-------------------------------------------------------

Only proceed with these instructions after successfully setting up MuSS in WiMDA.

Create your input file with the atomistic parameters of your system. To do this successfully, refer to the MuSpinSim documentation and the examples of input files on their GitHub page.

In WiMDA, load your data as usual, then click "Analyse" in the menu bar to open the Analyse window. In the "Component 1" section, under "Oscillation", choose "MuSpinSim", which comes with a "Launch" button.

Once the "Launch" button is clicked, MuSS will run in the Windows PowerShell. The terminal and GUI will open. Now you're ready to use MuSS integrated with WiMDA!

In MuSS, go to "File" > "Load" in the top menu bar and select the text input file you created earlier with your atomistic parameters, based on the MuSpinSim documentation. Once the file is loaded, you will see your parameters displayed in the GUI. Click the blue "Run" button to start your simulation.

Once the simulation is complete, the graph will display the updated values. To send these initial values to WiMDA, click the "Send" button in the "Socket" frame. (This will also print the values sent in your terminal, with a message containing the word "Hello" at the end.)

Now, in WiMDA, you can plot your simulation. Once other parameters are set, click "Fit". While in the fitting loop, you should see the graph in MuSS updating, and messages being exchanged between the two programs. When the process is complete, a confirmation message will appear in your MuSS terminal.



