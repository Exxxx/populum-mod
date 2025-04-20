"""
Goes through a mod file with "gainrit" commands and puts the associated ritual they will gainrit
"""

import re
 
# Specify the file path
filename = "E:/dev/populum/mod/populum.c5m"

# Read all lines from the file
with open(filename, 'r', encoding='utf-8') as f:
    lines = f.readlines()

# First pass: Collect all rituals and their line numbers
rituals = []  # List to store rituals with their names, line numbers, and indices
current_ritual_index = -1
line_ritual_indices = [-1] * len(lines)  # To store the ritual index for each line

for i, line in enumerate(lines):
    stripped_line = line.strip()
    # Check for 'newritual' lines
    match_newritual = re.match(r'^newritual\s+"(.+)"', stripped_line)
    if match_newritual:
        ritual_name = match_newritual.group(1)
        current_ritual_index += 1
        rituals.append({'name': ritual_name, 'line_number': i, 'index': current_ritual_index})
    # Assign the current ritual index to each line
    line_ritual_indices[i] = current_ritual_index

# Second pass: Update 'gainrit' lines with the correct ritual names
updated_lines = lines.copy()

for i, line in enumerate(lines):
    stripped_line = line.strip()
    # Check for 'gainrit' lines
    match_gainrit = re.match(r'^(gainrit\s+)(-?\d+)(.*)', stripped_line)
    if match_gainrit:
        gainrit_prefix = match_gainrit.group(1)
        offset_str = match_gainrit.group(2)
        rest_of_line = match_gainrit.group(3)
        offset = int(offset_str)

        # Get the ritual index of the current line
        ritual_index = line_ritual_indices[i]
        if ritual_index == -1:
            # The gainrit line is not within a ritual; skip updating
            continue

        # Calculate the target ritual index
        target_index = ritual_index + offset

        # Check if the target index is within bounds
        if 0 <= target_index < len(rituals):
            target_ritual_name = rituals[target_index]['name']
        else:
            target_ritual_name = 'Unknown'

        # Update the gainrit line with the ritual name
        updated_line = f"{gainrit_prefix}{offset_str}{rest_of_line}   # \"{target_ritual_name}\""
        updated_lines[i] = updated_line + '\n'

# Write the updated lines back to the file
with open(filename, 'w', encoding='utf-8') as f:
    f.writelines(updated_lines)
