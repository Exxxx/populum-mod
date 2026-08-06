#!/usr/bin/env python3
"""Find gainrit offset between two rituals.

CLI (default when two ritual names are given):

  python py_tools/gainrit_distance.py "Study Basic Enchanting" "Specialize Organic Matter"

Interactive GUI (opt-in only):

  python py_tools/gainrit_distance.py --gui
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from gainrit_common import MOD_FILE, build_global_ritual_list


def _ritual_matches(name: str, ritual_names: list[str]) -> list[int]:
    name_lower = name.lower()
    return [i for i, n in enumerate(ritual_names) if n.lower() == name_lower]


def resolve_ritual_index(name: str, ritual_names: list[str]) -> int | None:
    matches = _ritual_matches(name, ritual_names)
    if len(matches) == 1:
        return matches[0]
    return None


def format_offset(
    ritual_a: str,
    ritual_b: str,
    ritual_names: list[str],
    mod_ritual_lines: dict[str, list[int]],
) -> tuple[bool, str]:
    index_a = resolve_ritual_index(ritual_a, ritual_names)
    if index_a is None:
        matches = _ritual_matches(ritual_a, ritual_names)
        if not matches:
            return False, f"Ritual not found: {ritual_a!r}"
        return False, f"Ambiguous source ritual {ritual_a!r} ({len(matches)} matches in global list)"

    matches_b = _ritual_matches(ritual_b, ritual_names)
    if not matches_b:
        return False, f"Ritual not found: {ritual_b!r}"
    if len(matches_b) == 1:
        offset = matches_b[0] - index_a
        lines = mod_ritual_lines.get(ritual_b, [])
        line_hint = f" (mod line {lines[0]})" if lines else ""
        return True, (
            f"{ritual_a} -> {ritual_b}: gainrit {offset}{line_hint}"
        )

    lines = [
        f"{ritual_a} -> {ritual_b}: ambiguous target ({len(matches_b)} rituals in global list)"
    ]
    mod_line_pool = mod_ritual_lines.get(ritual_b, [])
    for n, idx in enumerate(matches_b):
        offset = idx - index_a
        line_hint = ""
        if n < len(mod_line_pool):
            line_hint = f"  # mod line {mod_line_pool[n]}"
        lines.append(f"  gainrit {offset}{line_hint}")
    return True, "\n".join(lines)


def _mod_ritual_lines(mod_rituals: list[dict]) -> dict[str, list[int]]:
    out: dict[str, list[int]] = {}
    for ritual in mod_rituals:
        out.setdefault(ritual["name"], []).append(ritual["line"])
    return out


def create_ui(ritual_names: list[str], mod_ritual_lines: dict[str, list[int]]) -> None:
    import tkinter as tk
    from tkinter import ttk

    root = tk.Tk()
    root.title("Ritual Offset Finder")
    root.geometry("500x300")

    tk.Label(root, text="Select Ritual A:").pack(pady=5)
    ritual_a_var = tk.StringVar()
    ritual_a_entry = ttk.Combobox(root, textvariable=ritual_a_var)
    ritual_a_entry["values"] = ritual_names
    ritual_a_entry.pack(pady=5)

    tk.Label(root, text="Select Ritual B:").pack(pady=5)
    ritual_b_var = tk.StringVar()
    ritual_b_entry = ttk.Combobox(root, textvariable=ritual_b_var)
    ritual_b_entry["values"] = ritual_names
    ritual_b_entry.pack(pady=5)

    result_label = tk.Label(root, text="", font=("Arial", 12), justify="left")
    result_label.pack(pady=20)

    def update_result() -> None:
        ritual_a = ritual_a_var.get().strip()
        ritual_b = ritual_b_var.get().strip()
        ok, result = format_offset(ritual_a, ritual_b, ritual_names, mod_ritual_lines)
        result_label.config(text=result if ok else f"Error: {result}")

    tk.Button(root, text="Calculate Offset", command=update_result).pack(pady=10)
    root.mainloop()


def main() -> int:
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "ritual_a",
        nargs="?",
        help="Source ritual name (gainrit is written on this ritual)",
    )
    parser.add_argument(
        "ritual_b",
        nargs="?",
        help="Target ritual name (granted by gainrit offset)",
    )
    parser.add_argument(
        "--gui",
        action="store_true",
        help="Open the interactive offset finder window",
    )
    parser.add_argument(
        "--mod",
        type=Path,
        default=MOD_FILE,
        help="Path to populum.c5m (default: populum/populum.c5m)",
    )
    args = parser.parse_args()

    if args.gui:
        global_names, mod_rituals, _, _ = build_global_ritual_list(mod_path=args.mod)
        create_ui(global_names, _mod_ritual_lines(mod_rituals))
        return 0

    if not args.ritual_a or not args.ritual_b:
        parser.print_help()
        return 0

    global_names, mod_rituals, _, _ = build_global_ritual_list(mod_path=args.mod)
    mod_ritual_lines = _mod_ritual_lines(mod_rituals)

    ok, result = format_offset(args.ritual_a, args.ritual_b, global_names, mod_ritual_lines)
    print(result)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
