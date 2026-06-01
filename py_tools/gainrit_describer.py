"""
Goes through populum.c5m gainrit commands and adds/updates trailing # "Target" comments
using the global ritual index (vanilla + mod newritual order).
"""

from __future__ import annotations

import re
import sys

from gainrit_common import (
    GAINRIT_LINE_RE,
    MOD_FILE,
    QUOTED_INTENT_RE,
    build_global_ritual_list,
    resolve_gainrit_target,
)


def strip_trailing_quoted_comment(rest: str) -> str:
    """Remove existing describer # \"Name\" suffix; preserve manual # comments."""
    return QUOTED_INTENT_RE.sub("", rest).rstrip()


def annotate_gainrit_lines(mod_path=MOD_FILE, write: bool = True) -> int:
    mod_lines = mod_path.read_text(encoding="utf-8").splitlines(keepends=True)
    plain = [ln.rstrip("\n") for ln in mod_lines]

    global_names, mod_rituals, mod_line_indices, vanilla_count = build_global_ritual_list(
        mod_path=mod_path
    )

    updated = plain.copy()
    changed = 0

    for i, line in enumerate(plain):
        m = GAINRIT_LINE_RE.match(line.strip())
        if not m:
            continue

        prefix, offset_str, rest = m.group(1), m.group(2), m.group(3)
        offset = int(offset_str)
        src_local = mod_line_indices[i]
        if src_local < 0:
            continue

        target = resolve_gainrit_target(
            src_local, offset, vanilla_count, global_names
        )
        target_name = target if target is not None else "Unknown"

        rest_clean = strip_trailing_quoted_comment(rest)
        new_line = f"{prefix}{offset_str}{rest_clean}   # \"{target_name}\""
        if new_line != line:
            changed += 1
        updated[i] = new_line

    if write and changed:
        mod_path.write_text(
            "".join(f"{ln}\n" for ln in updated),
            encoding="utf-8",
        )

    return changed


def main() -> int:
    import argparse
    from pathlib import Path

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--mod",
        type=Path,
        default=MOD_FILE,
        help="Path to populum.c5m",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Report how many lines would change without writing",
    )
    args = parser.parse_args()

    n = annotate_gainrit_lines(args.mod, write=not args.dry_run)
    action = "Would update" if args.dry_run else "Updated"
    print(f"{action} {n} gainrit line(s) in {args.mod}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
