"""Shared ritual index and gainrit parsing for Populum mod tools."""

from __future__ import annotations

import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
VANILLA_RITUALS = REPO_ROOT / "py_tools" / "references" / "Ritual Data v5.33.c5m"
MOD_FILE = REPO_ROOT / "populum" / "populum.c5m"

NEW_RITUAL_RE = re.compile(r'^newritual\s+"(.+)"')
GAINRIT_RE = re.compile(r'^gainrit\s+(-?\d+)(.*)$')
GAINRIT_LINE_RE = re.compile(r'^(gainrit\s+)(-?\d+)(.*)')
QUOTED_INTENT_RE = re.compile(r'#\s*"([^"]+)"\s*$')


def parse_ritual_names(lines: list[str]) -> list[str]:
    names = []
    for line in lines:
        m = NEW_RITUAL_RE.match(line.strip())
        if m:
            names.append(m.group(1))
    return names


def parse_mod_rituals_with_line_map(lines: list[str]) -> tuple[list[dict], list[int]]:
    """Return mod rituals [{name, index}] and per-line mod-local ritual index."""
    rituals: list[dict] = []
    line_indices: list[int] = []
    current = -1
    for i, line in enumerate(lines):
        m = NEW_RITUAL_RE.match(line.strip())
        if m:
            current += 1
            rituals.append({"name": m.group(1), "line": i + 1, "index": current})
        line_indices.append(current)
    return rituals, line_indices


def build_global_ritual_list(
    vanilla_path: Path = VANILLA_RITUALS,
    mod_path: Path = MOD_FILE,
) -> tuple[list[str], list[dict], list[int], int]:
    """Vanilla rituals first, then mod newritual entries in file order."""
    vanilla_lines = vanilla_path.read_text(encoding="utf-8").splitlines()
    mod_lines = mod_path.read_text(encoding="utf-8").splitlines()
    vanilla_names = parse_ritual_names(vanilla_lines)
    mod_rituals, mod_line_indices = parse_mod_rituals_with_line_map(mod_lines)
    mod_names = [r["name"] for r in mod_rituals]
    global_names = vanilla_names + mod_names
    return global_names, mod_rituals, mod_line_indices, len(vanilla_names)


def resolve_gainrit_target(
    mod_src_index: int,
    offset: int,
    vanilla_count: int,
    global_names: list[str],
) -> str | None:
    global_src = vanilla_count + mod_src_index
    global_tgt = global_src + offset
    if 0 <= global_tgt < len(global_names):
        return global_names[global_tgt]
    return None


def extract_manual_intent(rest_of_line: str) -> str | None:
    """First # comment after offset, excluding trailing describer # \"Name\"."""
    rest = rest_of_line.strip()
    if not rest.startswith("#"):
        return None
    parts = rest.split("#")
    if len(parts) < 2:
        return None
    comment = parts[1].strip().strip('"')
    if not comment or comment.startswith('"'):
        return None
    if "note: duplicate ritual name" in comment.lower():
        return None
    return comment


def extract_quoted_intent(line: str) -> str | None:
    m = QUOTED_INTENT_RE.search(line.rstrip())
    if not m:
        return None
    intent = m.group(1).strip()
    if "note: duplicate ritual name" in intent.lower():
        return None
    return intent


def names_match(intent: str, actual: str) -> bool:
    a = intent.lower().replace(" ", "")
    b = actual.lower().replace(" ", "")
    if a == b:
        return True
    return intent.lower() in actual.lower() or actual.lower() in intent.lower()


def find_global_index_for_intent(intent: str, global_names: list[str]) -> tuple[int | None, str | None]:
    """Return (global_index, error). Uses first exact case-insensitive match."""
    key = intent.lower()
    matches = [i for i, n in enumerate(global_names) if n.lower() == key]
    if len(matches) == 1:
        return matches[0], None
    if len(matches) > 1:
        return None, f"duplicate ritual name {intent!r} ({len(matches)} matches)"
    # fuzzy: intent contained in name or vice versa (single hit only)
    fuzzy = [
        i
        for i, n in enumerate(global_names)
        if key in n.lower() or n.lower() in key
    ]
    if len(fuzzy) == 1:
        return fuzzy[0], None
    if len(fuzzy) > 1:
        return None, f"ambiguous intent {intent!r} ({len(fuzzy)} matches)"
    return None, f"ritual not found: {intent!r}"


def offset_for_intent(
    mod_src_index: int,
    intent: str,
    vanilla_count: int,
    global_names: list[str],
) -> tuple[int | None, str | None]:
    tgt_idx, err = find_global_index_for_intent(intent, global_names)
    if err:
        return None, err
    assert tgt_idx is not None
    global_src = vanilla_count + mod_src_index
    return tgt_idx - global_src, None
