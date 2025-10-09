"""
Tool to find the offset distance between two rituals for moving rituals around.
"""
import re
import tkinter as tk
from tkinter import ttk

# Specify the file path
filename = "~/mod/populum.c5m"

# Read all lines from the file
with open(filename, 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Collect all rituals and their line numbers
rituals = []
current_ritual_index = -1
line_ritual_indices = [-1] * len(lines)

for i, line in enumerate(lines):
    stripped_line = line.strip()
    match_newritual = re.match(r'^newritual\s+"(.+)"', stripped_line)
    if match_newritual:
        ritual_name = match_newritual.group(1)
        current_ritual_index += 1
        rituals.append({'name': ritual_name, 'line_number': i, 'index': current_ritual_index})
    line_ritual_indices[i] = current_ritual_index

# List of ritual names for the dropdown
ritual_names = [ritual['name'] for ritual in rituals]

# Function to get a ritual index by exact name (case insensitive)
def get_ritual_index(name):
    name_lower = name.lower()
    for ritual in rituals:
        if ritual['name'].lower() == name_lower:
            return ritual['index']
    return None

# Function to calculate offset between two rituals
def calculate_offset(ritual_name_a, ritual_name_b):
    index_a = get_ritual_index(ritual_name_a)
    index_b = get_ritual_index(ritual_name_b)
    
    if index_a is None or index_b is None:
        return "One or both rituals not found."
    offset = index_b - index_a
    return f"Offset from '{ritual_name_a}' to '{ritual_name_b}': {offset}"

# Initialize the UI
def create_ui():
    # Root window
    root = tk.Tk()
    root.title("Ritual Offset Finder")
    root.geometry("500x300")

    # Ritual A selection
    tk.Label(root, text="Select Ritual A:").pack(pady=5)
    ritual_a_var = tk.StringVar()
    ritual_a_entry = ttk.Combobox(root, textvariable=ritual_a_var)
    ritual_a_entry['values'] = ritual_names  # Populate the dropdown with exact ritual names
    ritual_a_entry.pack(pady=5)

    # Ritual B selection
    tk.Label(root, text="Select Ritual B:").pack(pady=5)
    ritual_b_var = tk.StringVar()
    ritual_b_entry = ttk.Combobox(root, textvariable=ritual_b_var)
    ritual_b_entry['values'] = ritual_names  # Populate the dropdown with exact ritual names
    ritual_b_entry.pack(pady=5)

    # Display result
    result_label = tk.Label(root, text="", font=("Arial", 12))
    result_label.pack(pady=20)

    # Function to update offset result
    def update_result():
        ritual_a = ritual_a_var.get().strip()  # Strip whitespace
        ritual_b = ritual_b_var.get().strip()  # Strip whitespace
        result = calculate_offset(ritual_a, ritual_b)
        result_label.config(text=result)

    # Calculate button
    calc_button = tk.Button(root, text="Calculate Offset", command=update_result)
    calc_button.pack(pady=10)

    # Run the UI loop
    root.mainloop()

# Run the UI
create_ui()
