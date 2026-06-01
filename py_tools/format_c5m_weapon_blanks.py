#!/usr/bin/env python3
"""Remove unneeded blank lines inside newweapon blocks in populum.c5m.

For in-range newweapon blocks:
  - Remove blank lines between commands within the block
  - Keep exactly one blank line before each newweapon
  - Strip trailing whitespace on lines inside cleaned blocks
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from gainrit_common import MOD_FILE

DEFAULT_START = 4714
DEFAULT_END = 18532
SAMPLE_MARKER = "Huge Earth Branded Arbalest"


def is_blank(line: str) -> bool:
    return line.strip() == ""


def format_weapon_blanks(
    lines: list[str],
    start_line: int,
    end_line: int,
) -> tuple[list[str], int]:
    """Return formatted lines and count of in-range weapon blocks cleaned."""
    out: list[str] = []
    blocks_cleaned = 0
    i = 0

    while i < len(lines):
        line = lines[i]
        if line.startswith("newweapon "):
            line_no = i + 1
            if start_line <= line_no <= end_line:
                blocks_cleaned += 1
                if out and out[-1] != "":
                    out.append("")
                out.append(line.rstrip())
                i += 1
                while i < len(lines):
                    if lines[i].startswith("newweapon "):
                        break
                    if is_blank(lines[i]):
                        i += 1
                        continue
                    out.append(lines[i].rstrip())
                    i += 1
                continue
        out.append(line)
        i += 1

    return out, blocks_cleaned


def print_sample(lines: list[str], new_lines: list[str], marker: str) -> None:
    for idx, line in enumerate(lines):
        if marker in line:
            start = max(0, idx - 2)
            end = min(len(lines), idx + 14)
            print(f"--- BEFORE ({marker}) ---")
            for j in range(start, end):
                print(f"  {j + 1}: {lines[j]!r}")
            break
    else:
        print(f"Sample marker {marker!r} not found in original file.")
        return

    for idx, line in enumerate(new_lines):
        if marker in line:
            start = max(0, idx - 2)
            end = min(len(new_lines), idx + 14)
            print(f"--- AFTER ({marker}) ---")
            for j in range(start, end):
                print(f"  {j + 1}: {new_lines[j]!r}")
            break
    else:
        print(f"Sample marker {marker!r} not found in formatted output.")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--file", type=Path, default=MOD_FILE, help="Path to .c5m file")
    parser.add_argument(
        "--start",
        type=int,
        default=DEFAULT_START,
        help=f"First newweapon start line to clean (default: {DEFAULT_START})",
    )
    parser.add_argument(
        "--end",
        type=int,
        default=DEFAULT_END,
        help=f"Last newweapon start line to clean (default: {DEFAULT_END})",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print stats and sample without writing",
    )
    parser.add_argument(
        "--inplace",
        action="store_true",
        help="Rewrite the file in place",
    )
    args = parser.parse_args()

    if not args.dry_run and not args.inplace:
        parser.error("Specify --dry-run or --inplace")

    path = args.file
    text = path.read_text(encoding="utf-8", errors="replace")
    had_trailing_newline = text.endswith("\n")
    lines = text.splitlines()

    new_lines, blocks_cleaned = format_weapon_blanks(lines, args.start, args.end)
    removed = len(lines) - len(new_lines)

    print(f"File: {path}")
    print(f"Range: newweapon start lines {args.start}–{args.end}")
    print(f"Blocks cleaned: {blocks_cleaned}")
    print(f"Lines: {len(lines)} -> {len(new_lines)} ({removed} removed)")
    print()
    print_sample(lines, new_lines, SAMPLE_MARKER)

    if args.dry_run:
        return 0

    output = "\n".join(new_lines)
    if had_trailing_newline:
        output += "\n"
    path.write_text(output, encoding="utf-8", newline="\n")
    print(f"\nWrote {path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
