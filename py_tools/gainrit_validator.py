#!/usr/bin/env python3
"""Validate gainrit offsets in populum.c5m against the global ritual index."""

from __future__ import annotations

import argparse
import sys

from gainrit_common import (
    GAINRIT_LINE_RE,
    GAINRIT_RE,
    MOD_FILE,
    QUOTED_INTENT_RE,
    VANILLA_RITUALS,
    build_global_ritual_list,
    extract_manual_intent,
    extract_quoted_intent,
    names_match,
    offset_for_intent,
    resolve_gainrit_target,
)


def validate(mod_path=MOD_FILE, vanilla_path=VANILLA_RITUALS) -> list[dict]:
    mod_lines = mod_path.read_text(encoding="utf-8").splitlines()
    global_names, mod_rituals, mod_line_indices, vanilla_count = build_global_ritual_list(
        vanilla_path, mod_path
    )

    issues: list[dict] = []

    for i, line in enumerate(mod_lines):
        m = GAINRIT_RE.match(line.strip())
        if not m:
            continue

        offset = int(m.group(1))
        rest = m.group(2)
        src_local = mod_line_indices[i]
        if src_local < 0:
            issues.append(
                {
                    "line": i + 1,
                    "kind": "outside_ritual",
                    "text": line.strip(),
                }
            )
            continue

        src_name = mod_rituals[src_local]["name"]
        actual = resolve_gainrit_target(src_local, offset, vanilla_count, global_names)

        if actual is None:
            issues.append(
                {
                    "line": i + 1,
                    "kind": "out_of_bounds",
                    "source": src_name,
                    "offset": offset,
                    "text": line.strip(),
                }
            )
            continue

        manual = extract_manual_intent(rest)
        quoted = extract_quoted_intent(line)

        # Quoted describer comment is authoritative when present.
        if quoted:
            if not names_match(quoted, actual):
                correct, err = offset_for_intent(
                    src_local, quoted, vanilla_count, global_names
                )
                issues.append(
                    {
                        "line": i + 1,
                        "kind": "mismatch",
                        "intent_kind": "quoted",
                        "source": src_name,
                        "offset": offset,
                        "intent": quoted,
                        "actual": actual,
                        "correct_offset": correct,
                        "resolve_error": err,
                        "text": line.strip(),
                    }
                )
            continue

        # No quoted comment: validate resolvable manual shorthand/full name.
        if not manual or names_match(manual, actual):
            continue
        correct, err = offset_for_intent(
            src_local, manual, vanilla_count, global_names
        )
        if err:
            # Unresolvable shorthand (e.g. "Bulk arms") — not a offset bug.
            continue
        if correct == offset:
            continue
        issues.append(
            {
                "line": i + 1,
                "kind": "mismatch",
                "intent_kind": "manual",
                "source": src_name,
                "offset": offset,
                "intent": manual,
                "actual": actual,
                "correct_offset": correct,
                "resolve_error": err,
                "text": line.strip(),
            }
        )

    return issues


def _intent_for_fix(line: str, rest: str) -> tuple[str | None, str]:
    """Return (intent, kind) for auto-fix: quoted comment wins over manual."""
    quoted = extract_quoted_intent(line)
    if quoted:
        return quoted, "quoted"
    manual = extract_manual_intent(rest)
    if manual:
        return manual, "manual"
    return None, ""


def fix_gainrit_offsets(
    mod_path=MOD_FILE, vanilla_path=VANILLA_RITUALS
) -> tuple[int, list[dict]]:
    """Rewrite gainrit offsets to match # intent comments. Returns (fixed_count, remaining_issues)."""
    mod_lines = mod_path.read_text(encoding="utf-8").splitlines()
    global_names, mod_rituals, mod_line_indices, vanilla_count = build_global_ritual_list(
        vanilla_path, mod_path
    )

    updated = mod_lines.copy()
    fixed = 0

    for i, line in enumerate(mod_lines):
        m = GAINRIT_LINE_RE.match(line.strip())
        if not m:
            continue

        prefix, offset_str, rest = m.group(1), m.group(2), m.group(3)
        offset = int(offset_str)
        src_local = mod_line_indices[i]
        if src_local < 0:
            continue

        intent, _kind = _intent_for_fix(line, rest)
        if not intent:
            continue

        correct, err = offset_for_intent(
            src_local, intent, vanilla_count, global_names
        )
        if err or correct is None or correct == offset:
            continue

        rest_clean = QUOTED_INTENT_RE.sub("", rest).rstrip()
        updated[i] = f"{prefix}{correct}{rest_clean}   # \"{intent}\""
        fixed += 1

    if fixed:
        mod_path.write_text(
            "\n".join(updated) + "\n",
            encoding="utf-8",
        )

    remaining = validate(mod_path, vanilla_path)
    return fixed, remaining


def print_report(issues: list[dict]) -> None:
    if not issues:
        print("gainrit validation: OK (no issues)")
        return

    print(f"gainrit validation: {len(issues)} issue(s)\n")
    for issue in issues:
        line = issue["line"]
        kind = issue["kind"]
        if kind == "outside_ritual":
            print(f"  L{line}: gainrit outside newritual block")
            print(f"    {issue['text']}")
        elif kind == "out_of_bounds":
            print(
                f"  L{line}: out of bounds — {issue['source']} gainrit {issue['offset']}"
            )
            print(f"    {issue['text']}")
        else:
            correct = issue.get("correct_offset")
            extra = f" -> use offset {correct}" if correct is not None else ""
            if issue.get("resolve_error"):
                extra = f" ({issue['resolve_error']})"
            print(
                f"  L{line}: [{issue['intent_kind']}] {issue['source']} "
                f"gainrit {issue['offset']} grants {issue['actual']!r}, "
                f"expected {issue['intent']!r}{extra}"
            )
            print(f"    {issue['text']}")


def main() -> int:
    from pathlib import Path

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--mod",
        type=Path,
        default=MOD_FILE,
        help="Path to populum.c5m",
    )
    parser.add_argument(
        "--vanilla",
        type=Path,
        default=VANILLA_RITUALS,
        help="Path to vanilla Ritual Data reference",
    )
    parser.add_argument(
        "--fix",
        action="store_true",
        help="Rewrite gainrit offsets to match # intent comments, then re-validate",
    )
    args = parser.parse_args()

    if args.fix:
        fixed, issues = fix_gainrit_offsets(args.mod, args.vanilla)
        if fixed:
            print(f"Fixed {fixed} gainrit offset(s) in {args.mod}\n")
        print_report(issues)
        return 1 if issues else 0

    issues = validate(args.mod, args.vanilla)
    print_report(issues)
    return 1 if issues else 0


if __name__ == "__main__":
    sys.exit(main())
