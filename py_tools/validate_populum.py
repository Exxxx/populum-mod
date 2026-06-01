#!/usr/bin/env python3
"""Standard post-edit checks for populum.c5m.

Run after any change that adds, removes, or reorders newritual blocks. Inserting
or deleting rituals shifts the global ritual index; unvalidated gainrit lines can
grant the wrong ritual silently in-game.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from gainrit_common import MOD_FILE, VANILLA_RITUALS
from gainrit_describer import annotate_gainrit_lines
from gainrit_validator import fix_gainrit_offsets, print_report, validate


def run_checks(
    mod_path: Path = MOD_FILE,
    vanilla_path: Path = VANILLA_RITUALS,
    *,
    fix: bool = False,
    describe: bool = False,
) -> int:
    if fix:
        fixed, issues = fix_gainrit_offsets(mod_path, vanilla_path)
        if fixed:
            print(f"Fixed {fixed} gainrit offset(s)\n")
    else:
        issues = validate(mod_path, vanilla_path)

    if describe:
        n = annotate_gainrit_lines(mod_path, write=True)
        if n:
            print(f"Updated {n} gainrit # \"Target\" comment(s)\n")
        if fix or describe:
            issues = validate(mod_path, vanilla_path)

    print_report(issues)
    return 1 if issues else 0


def main() -> int:
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""\
Typical workflow after editing newritual / gainrit in populum.c5m:

  python py_tools/validate_populum.py --fix --describe

Use --fix when ritual order changed and quoted # "Target" comments are still correct.
Use --describe to refresh describer comments after fixing offsets or adding gainrit lines.
""",
    )
    parser.add_argument("--mod", type=Path, default=MOD_FILE)
    parser.add_argument("--vanilla", type=Path, default=VANILLA_RITUALS)
    parser.add_argument(
        "--fix",
        action="store_true",
        help="Correct gainrit offsets from # intent comments before validating",
    )
    parser.add_argument(
        "--describe",
        action="store_true",
        help="Refresh trailing # \"Target\" comments on all gainrit lines",
    )
    args = parser.parse_args()
    return run_checks(
        args.mod,
        args.vanilla,
        fix=args.fix,
        describe=args.describe,
    )


if __name__ == "__main__":
    sys.exit(main())
