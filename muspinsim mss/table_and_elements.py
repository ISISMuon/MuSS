'''
Creating a table kinda vibe
'''
import tkinter as tk


def create_table(root, rows, columns):
    # Create a table with 'rows' rows and 'columns' columns
    for i in range(rows):
        for j in range(columns):
            label = tk.Label(
                root, text=f'Row {i+1}\nColumn {j+1}', borderwidth=1, relief='solid', width=15, height=2)
            label.grid(row=i, column=j)


# Create the main window
root = tk.Tk()
root.title("Tkinter Table Example")

# Define the number of rows and columns in the table
num_rows = 5
num_columns = 3

# Create the table
create_table(root, num_rows, num_columns)

# Start the Tkinter main loop
root.mainloop()
