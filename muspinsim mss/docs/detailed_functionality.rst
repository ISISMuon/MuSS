Detailed Functionality
======================

This section provides detailed step-by-step guides for each main feature in the MuSS application.

Load and Run
------------

**Description:**
Combines the loading and running processes into one seamless action. Ideal for users who want to quickly start their simulations or experiments without manual setups.

**Steps:**
1. From the menu, select `Load and Run`.
2. Navigate to the `.txt` file containing your input parameters.
3. Click `Load and Run` to execute.

**Limitations:**
- Input parameters in the `.txt` file are not reflected in the GUI until manually reloaded.

Load
----

**Description:**
Loads parameters from a `.txt` file into the GUI for editing or review before execution.

**Steps:**
1. Select `Load` from the main menu.
2. Choose the `.txt` file with the required parameters.
3. Parameters are displayed in the GUI for modification or confirmation.

Run
---

**Description:**
Executes the simulation using parameters set in the GUI.

**Steps:**
1. Ensure all parameters are correctly set in the GUI.
2. Click `Run` to start the simulation.

Fit wimda
---------

**Description:**
Integrates with WimDA for complex fitting processes.

**Steps:**
1. Ensure MuSS is set as the server and WimDA as the client.
2. Use the `Fit` button in WimDA to begin the fitting process based on data received from MuSS.

Fit muspinsim
-------------

**Description:**
Performs simulations within the muspinsim framework and adjusts parameters based on fitting results.

**Steps:**
1. Run the simulation with initial parameters.
2. Adjust the parameters based on the fitting analysis and rerun as needed.

Structure
---------

**Description:**
Outlines the fundamental structural design of MuSS, enabling users to understand how the modules interact.

**Details:**
- MuSS utilizes a modular architecture to ensure flexible integration and scalability.
