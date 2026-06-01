"""
Tool to find the offset distance between two rituals for moving rituals around.
"""
import re
import tkinter as tk
from tkinter import ttk

from gainrit_common import MOD_FILE, build_global_ritual_list

global_names, mod_rituals, _, vanilla_count = build_global_ritual_list(mod_path=MOD_FILE)

# List of ritual names for the dropdown (global index order)
ritual_names = global_names


def get_global_index(name: str) -> int | None:
    name_lower = name.lower()
    matches = [i for i, n in enumerate(global_names) if n.lower() == name_lower]
    if len(matches) == 1:
        return matches[0]
    return None


def calculate_offset(ritual_name_a: str, ritual_name_b: str) -> str:
    index_a = get_global_index(ritual_name_a)
    index_b = get_global_index(ritual_name_b)

    if index_a is None or index_b is None:
        return "One or both rituals not found (or name is ambiguous)."
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
