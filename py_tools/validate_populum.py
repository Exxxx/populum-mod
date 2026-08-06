#!/usr/bin/env python3
"""Standard post-edit checks for populum.c5m.

Run after any change that adds, removes, or reorders newritual blocks. Inserting
or deleting rituals shifts the global ritual index; unvalidated gainrit lines can
grant the wrong ritual silently in-game.

Also audit ritual level/levelreq against monster power assignments
(--audit-levelreq / --fix-levelreq).
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from gainrit_common import MOD_FILE, VANILLA_RITUALS
from gainrit_describer import annotate_gainrit_lines
from gainrit_validator import fix_gainrit_offsets, print_report, validate
from levelreq_auditor import (
    audit as audit_levelreq,
    fix_uniform_mismatches,
    print_report as print_levelreq_report,
)


def run_checks(
    mod_path: Path = MOD_FILE,
    vanilla_path: Path = VANILLA_RITUALS,
    *,
    fix: bool = False,
    describe: bool = False,
    audit_levelreq_flag: bool = False,
    fix_levelreq: bool = False,
) -> int:
    exit_code = 0
    run_gainrit = fix or describe or not (audit_levelreq_flag or fix_levelreq)

    if fix_levelreq or audit_levelreq_flag:
        if fix_levelreq:
            n, lr_issues = fix_uniform_mismatches(mod_path, vanilla_path)
            if n:
                print(f"Fixed {n} level/levelreq line(s)\n")
        else:
            lr_issues = audit_levelreq(mod_path, vanilla_path)
        print_levelreq_report(lr_issues)
        if any(i.severity == "error" for i in lr_issues):
            exit_code = 1

    if not run_gainrit:
        return exit_code

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
        issues = validate(mod_path, vanilla_path)

    print_report(issues)
    if issues:
        exit_code = 1
    return exit_code


def main() -> int:
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""\
Typical workflow after editing newritual / gainrit in populum.c5m:

  python py_tools/validate_populum.py --fix --describe

Level/levelreq vs monster power:

  python py_tools/validate_populum.py --audit-levelreq
  python py_tools/validate_populum.py --fix-levelreq

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
    parser.add_argument(
        "--audit-levelreq",
        action="store_true",
        help="Report ritual level/levelreq vs monster power mismatches",
    )
    parser.add_argument(
        "--fix-levelreq",
        action="store_true",
        help="Lower level/levelreq on uniform-power school mismatches",
    )
    args = parser.parse_args()
    return run_checks(
        args.mod,
        args.vanilla,
        fix=args.fix,
        describe=args.describe,
        audit_levelreq_flag=args.audit_levelreq,
        fix_levelreq=args.fix_levelreq,
    )


if __name__ == "__main__":
    sys.exit(main())
