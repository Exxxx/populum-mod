#!/usr/bin/env python3
"""Audit ritual level/levelreq against monster power assignments in populum.c5m.

Hard mismatch (auto-fixable when all casters share one power level L):
  - ritual level > L
  - active levelreq present and != L

Mixed-tier schools (manual; not auto-fixed):
  - same school assigned to monsters at different power levels

Missing school (hard):
  - transform+gainrit grants a mod-school ritual whose post-transform unit
    has no power in that school
"""

from __future__ import annotations

import argparse
import re
import sys
from collections import defaultdict
from dataclasses import dataclass, field
from pathlib import Path

from gainrit_common import (
    GAINRIT_RE,
    MOD_FILE,
    NEW_RITUAL_RE,
    VANILLA_RITUALS,
    build_global_ritual_list,
    extract_quoted_intent,
    resolve_gainrit_target,
)

NEWRITPOW_RE = re.compile(r"^newritpow\b")
RITPOW_RE = re.compile(r"^ritpow\s+(-?\d+)")
LEVEL_RE = re.compile(r"^level\s+(\d+)")
LEVELREQ_RE = re.compile(r"^levelreq\s+(\d+)")
# Commented levelreq is ignored for active gating
POWER_RE = re.compile(r"^power\s+(-?\d+)\s+(\d+)")
SELECT_MON_RE = re.compile(r'^selectmonster\s+(?:\d+:)?"([^"]+)"')
SELECT_MON_BARE_RE = re.compile(r"^selectmonster\s+(\d+)")
NEW_MON_RE = re.compile(r'^newmonster\s+"([^"]+)"')
ADDSTRING_RE = re.compile(r'^addstring\s+"([^"]+)"')
TRANSFORM_RE = re.compile(r"^transformtarg\b")
FREE_RE = re.compile(r"^free\b")
NOSTART_RE = re.compile(r"^nostart\b")


@dataclass
class RitualInfo:
    name: str
    line: int  # 1-based newritual line
    end_line: int  # last line of block (1-based, inclusive-ish)
    mod_index: int
    mod_school: int | None  # enclosing newritpow index, or None
    ritpow: int | None = None  # explicit ritpow if set
    level: int | None = None
    levelreq: int | None = None
    level_line: int | None = None  # 1-based
    levelreq_line: int | None = None
    free: bool = False
    nostart: bool = False
    transform: bool = False
    gainrits: list[tuple[int, int, str | None]] = field(default_factory=list)
    # (offset, line, quoted_intent)
    addstrings: list[str] = field(default_factory=list)

    @property
    def effective_school(self) -> tuple[str, int] | None:
        """Return ('mod', idx) or ('vanilla', nbr) or None if unknown."""
        if self.ritpow is not None and self.ritpow > 0:
            return ("vanilla", self.ritpow)
        if self.mod_school is not None:
            return ("mod", self.mod_school)
        return None


@dataclass
class Issue:
    kind: str  # uniform_mismatch | mixed_tier | missing_school
    severity: str  # error | warning
    ritual: str
    line: int
    detail: str
    school: tuple[str, int] | None = None
    target_level: int | None = None
    level_line: int | None = None
    levelreq_line: int | None = None
    current_level: int | None = None
    current_levelreq: int | None = None
    fixable: bool = False


def _strip_comment(line: str) -> str:
    s = line.strip()
    if not s or s.startswith("#"):
        return ""
    if "#" in s:
        s = s.split("#", 1)[0].strip()
    return s


def parse_mod_state(mod_path: Path = MOD_FILE) -> tuple[list[RitualInfo], dict[tuple[str, int], dict[str, int]]]:
    """Parse rituals and monster power map.

    power_map[(kind, school_id)][monster_name] = power_level
    kind is 'mod' or 'vanilla'. For mod, school_id is 0-based newritpow order.
    """
    lines = mod_path.read_text(encoding="utf-8").splitlines()
    rituals: list[RitualInfo] = []
    power_map: dict[tuple[str, int], dict[str, int]] = defaultdict(dict)

    mod_school = -1  # incremented on each newritpow
    current: RitualInfo | None = None
    pending_monster: str | None = None
    mod_ritual_index = -1

    def close_current(end_i: int) -> None:
        nonlocal current
        if current is not None:
            current.end_line = end_i
            rituals.append(current)
            current = None

    for i, raw in enumerate(lines):
        line_no = i + 1
        s = _strip_comment(raw)
        stripped = raw.strip()

        if NEWRITPOW_RE.match(stripped):
            close_current(i)
            mod_school += 1
            pending_monster = None
            continue

        m_new = NEW_RITUAL_RE.match(stripped)
        if m_new:
            close_current(i)
            mod_ritual_index += 1
            current = RitualInfo(
                name=m_new.group(1),
                line=line_no,
                end_line=line_no,
                mod_index=mod_ritual_index,
                mod_school=mod_school if mod_school >= 0 else None,
            )
            pending_monster = None
            continue

        m_sel = SELECT_MON_RE.match(stripped)
        if m_sel:
            pending_monster = m_sel.group(1)
            continue
        if SELECT_MON_BARE_RE.match(stripped):
            pending_monster = None
            continue
        m_nm = NEW_MON_RE.match(stripped)
        if m_nm:
            pending_monster = m_nm.group(1)
            continue

        m_pow = POWER_RE.match(s) if s else None
        if m_pow and pending_monster:
            pow_nbr = int(m_pow.group(1))
            pow_lvl = int(m_pow.group(2))
            if pow_nbr > 0:
                key = ("vanilla", pow_nbr)
            else:
                # 0 = last school, -1 = previous, etc.
                resolved = mod_school + pow_nbr
                if resolved < 0:
                    pending_monster = None
                    continue
                key = ("mod", resolved)
            # Later assignments for same monster+school overwrite
            power_map[key][pending_monster] = pow_lvl
            continue

        if current is None:
            continue

        if not s:
            continue

        m_rit = RITPOW_RE.match(s)
        if m_rit:
            current.ritpow = int(m_rit.group(1))
            continue
        m_lv = LEVEL_RE.match(s)
        if m_lv:
            current.level = int(m_lv.group(1))
            current.level_line = line_no
            continue
        m_lr = LEVELREQ_RE.match(s)
        if m_lr:
            current.levelreq = int(m_lr.group(1))
            current.levelreq_line = line_no
            continue
        if FREE_RE.match(s):
            current.free = True
            continue
        if NOSTART_RE.match(s):
            current.nostart = True
            continue
        if TRANSFORM_RE.match(s):
            current.transform = True
            continue
        m_as = ADDSTRING_RE.match(s)
        if m_as:
            current.addstrings.append(m_as.group(1))
            continue
        m_gr = GAINRIT_RE.match(s)
        if m_gr:
            offset = int(m_gr.group(1))
            quoted = extract_quoted_intent(raw)
            current.gainrits.append((offset, line_no, quoted))
            continue

    close_current(len(lines))
    return rituals, dict(power_map)


def _transform_targets(ritual: RitualInfo) -> list[str]:
    """Monster names from addstring that look like transform targets.

    Skip summoning-style strings: dice, counts, (-)exclusions, tagged offsets.
    """
    out: list[str] = []
    for a in ritual.addstrings:
        if a.startswith("(-)") or a.startswith("("):
            continue
        if "*" in a or "d" in a and any(c.isdigit() for c in a):
            # e.g. 2d4*Militia — keep trailing name after *
            if "*" in a:
                name = a.split("*", 1)[1].strip()
                if name and not name[0].isdigit():
                    out.append(name)
            continue
        if re.match(r"^\d+:", a):
            out.append(a.split(":", 1)[1])
            continue
        out.append(a)
    return out


def audit(
    mod_path: Path = MOD_FILE,
    vanilla_path: Path = VANILLA_RITUALS,
) -> list[Issue]:
    rituals, power_map = parse_mod_state(mod_path)
    global_names, _mod_rituals, _line_idx, vanilla_count = build_global_ritual_list(
        vanilla_path, mod_path
    )
    by_mod_index = {r.mod_index: r for r in rituals}
    issues: list[Issue] = []

    # Mixed-tier schools (mod only — vanilla ladders are intentional)
    for school_key, monsters in power_map.items():
        if school_key[0] != "mod":
            continue
        levels = set(monsters.values())
        if len(levels) > 1:
            names = ", ".join(f"{n}@{lv}" for n, lv in sorted(monsters.items()))
            issues.append(
                Issue(
                    kind="mixed_tier",
                    severity="warning",
                    ritual="",
                    line=0,
                    detail=f"school {school_key[0]}:{school_key[1]} has mixed power levels: {names}",
                    school=school_key,
                    fixable=False,
                )
            )

    mixed_schools = {
        i.school for i in issues if i.kind == "mixed_tier" and i.school is not None
    }

    for rit in rituals:
        school = rit.effective_school
        if school is None:
            continue
        casters = power_map.get(school, {})
        if not casters:
            # May still be gained via gainrit; checked in chain pass
            continue

        levels = set(casters.values())
        if len(levels) > 1:
            # Already flagged mixed_tier; skip auto-fixable uniform checks
            continue

        L = next(iter(levels))
        needs_level = rit.level is not None and rit.level > L
        needs_levelreq = rit.levelreq is not None and rit.levelreq != L
        if not needs_level and not needs_levelreq:
            continue

        caster_list = ", ".join(f"{n}@{lv}" for n, lv in sorted(casters.items()))
        parts = []
        if needs_level:
            parts.append(f"level {rit.level} > power {L}")
        if needs_levelreq:
            parts.append(f"levelreq {rit.levelreq} != power {L}")
        issues.append(
            Issue(
                kind="uniform_mismatch",
                severity="error",
                ritual=rit.name,
                line=rit.line,
                detail=f"{'; '.join(parts)}; casters: {caster_list}",
                school=school,
                target_level=L,
                level_line=rit.level_line,
                levelreq_line=rit.levelreq_line,
                current_level=rit.level,
                current_levelreq=rit.levelreq,
                fixable=school not in mixed_schools,
            )
        )

    # Missing school: transform + gainrit → target unit lacks power in target school
    for rit in rituals:
        if not rit.gainrits:
            continue
        targets = _transform_targets(rit) if rit.transform else []
        if not targets and not rit.transform:
            continue
        for offset, gr_line, quoted in rit.gainrits:
            tgt_name = resolve_gainrit_target(
                rit.mod_index, offset, vanilla_count, global_names
            )
            if quoted and not tgt_name:
                tgt_name = quoted
            if not tgt_name:
                continue
            # Find target ritual by name (mod list)
            tgt_rit = next((r for r in rituals if r.name == tgt_name), None)
            if tgt_rit is None:
                continue
            tgt_school = tgt_rit.effective_school
            if tgt_school is None or tgt_school[0] != "mod":
                continue
            casters = power_map.get(tgt_school, {})
            missing_units: list[str] = []
            check_units = targets if targets else []
            for unit in check_units:
                if unit not in casters:
                    missing_units.append(unit)
            if missing_units:
                issues.append(
                    Issue(
                        kind="missing_school",
                        severity="error",
                        ritual=rit.name,
                        line=gr_line,
                        detail=(
                            f"gainrit -> {tgt_name!r} (mod school {tgt_school[1]}); "
                            f"units lack power: {', '.join(missing_units)}"
                        ),
                        school=tgt_school,
                        target_level=1,
                        fixable=False,
                    )
                )
                # Broad transform/gainrit detection has many summoning false positives;
                # keep as warning so --audit-levelreq exit focuses on uniform mismatches.
                issues[-1].severity = "warning"

    return issues


def print_report(issues: list[Issue]) -> None:
    errors = [i for i in issues if i.severity == "error"]
    warnings = [i for i in issues if i.severity == "warning"]
    if not issues:
        print("levelreq audit: OK (no issues)")
        return
    print(
        f"levelreq audit: {len(errors)} error(s), {len(warnings)} warning(s)\n"
    )
    for i in issues:
        loc = f"L{i.line}" if i.line else "school"
        name = f" {i.ritual!r}" if i.ritual else ""
        print(f"  [{i.severity}/{i.kind}] {loc}{name}: {i.detail}")


def fix_uniform_mismatches(
    mod_path: Path = MOD_FILE,
    vanilla_path: Path = VANILLA_RITUALS,
) -> tuple[int, list[Issue]]:
    """Rewrite level/levelreq on uniform-mismatch rituals. Returns (edits, remaining)."""
    issues = audit(mod_path, vanilla_path)
    fixable = [i for i in issues if i.kind == "uniform_mismatch" and i.fixable and i.target_level]
    if not fixable:
        return 0, issues

    lines = mod_path.read_text(encoding="utf-8").splitlines()
    # Map line number -> new value for level / levelreq
    level_fixes: dict[int, int] = {}
    levelreq_fixes: dict[int, int] = {}
    for iss in fixable:
        L = iss.target_level
        assert L is not None
        if iss.current_level is not None and iss.current_level > L and iss.level_line:
            level_fixes[iss.level_line] = L
        if iss.current_levelreq is not None and iss.current_levelreq != L and iss.levelreq_line:
            levelreq_fixes[iss.levelreq_line] = L

    edits = 0
    for line_no, L in level_fixes.items():
        idx = line_no - 1
        raw = lines[idx]
        m = re.match(r"^(\s*level\s+)\d+(.*)$", raw)
        if m:
            lines[idx] = f"{m.group(1)}{L}{m.group(2)}"
            edits += 1
    for line_no, L in levelreq_fixes.items():
        idx = line_no - 1
        raw = lines[idx]
        m = re.match(r"^(\s*levelreq\s+)\d+(.*)$", raw)
        if m:
            lines[idx] = f"{m.group(1)}{L}{m.group(2)}"
            edits += 1

    if edits:
        mod_path.write_text("\n".join(lines) + "\n", encoding="utf-8")

    remaining = audit(mod_path, vanilla_path)
    return edits, remaining


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--mod", type=Path, default=MOD_FILE)
    parser.add_argument("--vanilla", type=Path, default=VANILLA_RITUALS)
    parser.add_argument(
        "--fix",
        action="store_true",
        help="Lower level/levelreq on uniform-power mismatches",
    )
    args = parser.parse_args()
    if args.fix:
        n, issues = fix_uniform_mismatches(args.mod, args.vanilla)
        if n:
            print(f"Fixed {n} level/levelreq line(s)\n")
    else:
        issues = audit(args.mod, args.vanilla)
    print_report(issues)
    errors = [i for i in issues if i.severity == "error"]
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
