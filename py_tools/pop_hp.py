# -*- coding: utf-8 -*-
"""
@author: Exx

Reads in a text file (e.g. yourmod.coe5) and converts all the hitpoints
"""

import re
import os

def calculate_new_hp_value(old_hp):
    """
    Applies the specified formula to calculate the new HP.
    """
    d2 = old_hp
    if d2 < 10:
        val = d2 * 2
    elif 10 <= d2 <= 19: # D2 > 9 AND D2 < 20
        val = d2 * 1.5
    elif 20 <= d2 <= 29: # D2 > 19 AND D2 < 30
        val = d2 * 1.25
    elif 30 <= d2 <= 39: # D2 > 29 AND D2 < 40
        val = d2 * 1.1
    elif 40 <= d2 <= 49: # D2 > 39 AND D2 < 50
        val = d2 * 1.05
    else: # D2 > 49 (which means D2 >= 50)
        val = d2 * 1.0 # or simply val = d2

    return int(round(val)) # round to 0 decimal places and convert to int

def process_monster_file(filepath):
    """
    Reads the monster file, processes HP lines, stores modified content,
    and writes the output to a new file in the same directory.
    """
    modified_lines = []
    try:
        # Use utf-8 encoding for broader compatibility
        with open(filepath, 'r', encoding='utf-8') as f:
            for line_number, line_content in enumerate(f, 1):
                original_line = line_content.rstrip('\n') # Preserve original line, remove only trailing newline

                # Check if the line starts with "hp" followed by whitespace.
                # This is more robust than line.startswith("hp ") as it handles various spacing.
                # We use lstrip to handle potential leading spaces on the line itself before "hp".
                stripped_for_keyword = original_line.lstrip()
                # Ensure it starts with 'hp' and the character immediately following (if any) is whitespace
                if stripped_for_keyword.startswith("hp") and \
                   (len(stripped_for_keyword) == 2 or (len(stripped_for_keyword) > 2 and stripped_for_keyword[2].isspace())):

                    # Split the line into the main part and the comment part
                    parts = original_line.split('#', 1)
                    data_segment = parts[0]  # e.g., "hp                             5 "
                    comment_segment = ""
                    if len(parts) > 1:
                        comment_segment = "#" + parts[1] # e.g., "# Hit Points."

                    # Use regex to reliably find the number immediately following 'hp' and whitespace
                    # This helps preserve the spacing around the number
                    match = re.search(r'hp\s+(\d+)', data_segment)

                    if match:
                         old_hp_str = match.group(1) # The captured number string
                         try:
                             old_hp_val = int(old_hp_str)

                             new_hp_val = calculate_new_hp_value(old_hp_val)
                             new_hp_str = str(new_hp_val)

                             # Replace the *first* occurrence of the old number string after 'hp'
                             # This is safer than replacing any instance of old_hp_str
                             # as it targets the actual value we just matched.
                             # Find the exact start index of the matched number string
                             idx_val_start = data_segment.find(old_hp_str, match.start(1)) # Find after 'hp\s+'

                             if idx_val_start != -1: # Should always be true if match is not None
                                 prefix = data_segment[:idx_val_start]
                                 suffix = data_segment[idx_val_start + len(old_hp_str):]
                                 new_data_segment = prefix + new_hp_str + suffix
                                 modified_lines.append(new_data_segment + comment_segment)
                             else:
                                 # Fallback if somehow find fails after regex match - should not happen
                                 print(f"Warning: Could not find matched number '{old_hp_str}' for replacement on line {line_number}: {original_line}")
                                 modified_lines.append(original_line)


                         except ValueError:
                             # HP value is not an integer
                             print(f"Warning: HP value is not an integer on line {line_number}: {original_line}")
                             modified_lines.append(original_line)
                         except Exception as e:
                             # Other potential errors during processing this line
                             print(f"Error processing line {line_number} ('{original_line}'): {e}")
                             modified_lines.append(original_line)
                    else:
                        # Line started with "hp" but regex didn't find a number after it
                        print(f"Warning: 'hp' tag found but could not parse value on line {line_number}: {original_line}")
                        modified_lines.append(original_line)

                else:
                    # Not an HP line or malformed hp tag
                    modified_lines.append(original_line)

        # --- Write the modified content to a new file ---

        # Get the directory and base filename
        directory = os.path.dirname(filepath)
        filename = os.path.basename(filepath)

        # Create the new filename (e.g., test.txt -> test_hp.txt)
        name, ext = os.path.splitext(filename)
        output_filename = f"{name}_hp{ext}" # You can change _hp to something else if desired

        # Create the full output file path
        output_filepath = os.path.join(directory, output_filename)

        try:
            # Write the stored modified lines to the new file
            with open(output_filepath, 'w', encoding='utf-8') as outfile:
                for line in modified_lines:
                    outfile.write(line + '\n') # Add the newline back for each line

            print(f"Successfully processed '{filename}' and saved modified content to '{output_filepath}'")

        except IOError as e:
            print(f"Error writing output file '{output_filepath}': {e}")

    except FileNotFoundError:
        print(f"Error: Input file not found at {filepath}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

# --- Main execution ---
if __name__ == "__main__":
    # IMPORTANT: Use raw string (r"...") or double backslashes ("\\") for Windows paths
    # Make sure this path is correct for your system
    file_path = r"C:\Users\your mod location\modfile_copy.txt"

    process_monster_file(file_path)