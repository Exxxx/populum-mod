"""Vanilla monster sprite registry from Monster Data v5.33.c5m."""
from __future__ import annotations

import argparse
import json
import re
from dataclasses import asdict, dataclass, field, replace
from pathlib import Path

from coe5_sprite_prompts import build_sprite_subject

TOOLS_DIR = Path(__file__).resolve().parent
REPO_ROOT = TOOLS_DIR.parent
DEFAULT_MONSTER_DATA = REPO_ROOT / "py_tools" / "references" / "Monster Data v5.33.c5m"
DEFAULT_REGISTRY_CACHE = TOOLS_DIR / "generated" / "monster_sprite_registry.json"
DEFAULT_SPRITE_OVERRIDES = TOOLS_DIR / "coe5_sprite_overrides.json"
DEFAULT_CONTROLS_DIR = REPO_ROOT / "art" / "coe5_sprites" / "monster"

MONSTER_INDEX_RE = re.compile(r"newmonster\s+\"([^\"]+)\".*#\s*(\d+)")
SPRITE_NUMBER_RE = re.compile(r"#\s*sprite number\s+(\d+)")
DESCR_RE = re.compile(r'^descr\s+"((?:[^"\\]|\\.)*)"')
DESCR_MAX_LEN = 220


@dataclass
class MonsterRecord:
    monster_index: int
    name: str
    descr: str
    sprite_number: int
    sprite_role: str = "spr1"
    parent_sprite_number: int | None = None
    huge: bool = False
    melee_weapon: str | None = None
    ranged_weapon: str | None = None
    canvas: int = 64
    visual_subject: str | None = None

    def subject_for_prompt(self, *, include_descr: bool = False) -> str:
        return build_sprite_subject(
            name=self.name,
            melee_weapon=self.melee_weapon,
            ranged_weapon=self.ranged_weapon,
            huge=self.huge,
            descr=self.descr,
            include_descr=include_descr,
        )

    def subject_for_tuning(self) -> str:
        """Short visual subject for style tuning — override, name, and gear only."""
        if self.visual_subject:
            parts = [self.visual_subject.strip()]
            if self.huge:
                parts.append("huge creature")
            return ", ".join(parts)
        return self.subject_for_prompt(include_descr=False)


@dataclass
class ControlEntry:
    sprite_number: int
    path: Path
    record: MonsterRecord | None = None
    mapped: bool = False
    warnings: list[str] = field(default_factory=list)


def _truncate_descr(text: str) -> str:
    text = text.strip()
    if len(text) <= DESCR_MAX_LEN:
        return text
    return text[: DESCR_MAX_LEN - 3].rsplit(" ", 1)[0] + "..."


WEAPON_COMMENT_RE = re.compile(r"#\s*([^:]+?):")


def _parse_weapon_from_line(line: str, prefix: str) -> str | None:
    stripped = line.strip()
    if not stripped.startswith(prefix):
        return None
    quoted = re.search(r'"([^"]+)"', stripped)
    if quoted:
        return quoted.group(1).strip()
    comment = WEAPON_COMMENT_RE.search(stripped)
    if comment:
        return comment.group(1).strip()
    return None


def build_registry(monster_data_path: Path | None = None) -> dict:
    path = monster_data_path or DEFAULT_MONSTER_DATA
    lines = path.read_text(encoding="utf-8", errors="replace").splitlines()

    by_sprite: dict[int, MonsterRecord] = {}
    by_monster_index: dict[int, MonsterRecord] = {}
    claimants: dict[int, list[dict[str, int | str]]] = {}
    spr1_numbers: set[int] = set()
    current: dict | None = None

    def record_from_current() -> MonsterRecord | None:
        if current is None or current.get("sprite_number") is None:
            return None
        sn = int(current["sprite_number"])
        canvas = 128 if current.get("huge") else 64
        return MonsterRecord(
            monster_index=int(current["monster_index"]),
            name=current["name"],
            descr=_truncate_descr(current.get("descr") or current["name"]),
            sprite_number=sn,
            sprite_role="spr1",
            huge=bool(current.get("huge")),
            melee_weapon=current.get("melee_weapon"),
            ranged_weapon=current.get("ranged_weapon"),
            canvas=canvas,
        )

    def flush() -> None:
        nonlocal current
        record = record_from_current()
        if record is None:
            current = None
            return

        by_monster_index[record.monster_index] = record
        sn = record.sprite_number
        claimants.setdefault(sn, []).append(
            {"monster_index": record.monster_index, "name": record.name}
        )
        by_sprite[sn] = record
        spr1_numbers.add(sn)
        current = None

    for line in lines:
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            if stripped.startswith("# sprite number"):
                match = SPRITE_NUMBER_RE.match(stripped)
                if match and current is not None:
                    current["sprite_number"] = int(match.group(1))
            continue

        monster_match = MONSTER_INDEX_RE.match(stripped)
        if monster_match:
            flush()
            current = {
                "name": monster_match.group(1),
                "monster_index": int(monster_match.group(2)),
                "descr": None,
                "sprite_number": None,
                "huge": False,
                "melee_weapon": None,
                "ranged_weapon": None,
            }
            continue

        if current is None:
            continue

        descr_match = DESCR_RE.match(stripped)
        if descr_match:
            current["descr"] = descr_match.group(1)
            continue

        if stripped.split()[0] == "huge":
            current["huge"] = True
            continue

        if stripped.startswith("meleeweapon") and current.get("melee_weapon") is None:
            if stripped.startswith("meleeweaponbonus") or stripped.startswith("meleeweaponspec"):
                pass
            else:
                weapon = _parse_weapon_from_line(stripped, "meleeweapon")
                if weapon:
                    current["melee_weapon"] = weapon
            continue

        if stripped.startswith("rangedweapon") and current.get("ranged_weapon") is None:
            weapon = _parse_weapon_from_line(stripped, "rangedweapon")
            if weapon:
                current["ranged_weapon"] = weapon

    flush()

    # spr2 heuristic: N+1 unclaimed by another spr1
    for sn, record in list(by_sprite.items()):
        spr2_num = sn + 1
        if spr2_num in spr1_numbers:
            continue
        if spr2_num in by_sprite:
            continue
        by_sprite[spr2_num] = MonsterRecord(
            monster_index=record.monster_index,
            name=record.name,
            descr=record.descr,
            sprite_number=spr2_num,
            sprite_role="spr2",
            parent_sprite_number=sn,
            huge=record.huge,
            melee_weapon=record.melee_weapon,
            ranged_weapon=record.ranged_weapon,
            canvas=record.canvas,
        )

    return {
        "source": str(path.resolve()),
        "monster_count": len(by_monster_index),
        "sprite_count": len(by_sprite),
        "sprites": {str(k): asdict(v) for k, v in sorted(by_sprite.items())},
        "claimants": {str(k): v for k, v in sorted(claimants.items()) if len(v) > 1},
        "monsters_by_index": {str(k): asdict(v) for k, v in sorted(by_monster_index.items())},
    }


def save_registry(payload: dict, cache_path: Path | None = None) -> Path:
    out = cache_path or DEFAULT_REGISTRY_CACHE
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    return out


def load_registry_payload(cache_path: Path | None = None, *, refresh: bool = False) -> dict:
    cache = cache_path or DEFAULT_REGISTRY_CACHE
    if refresh or not cache.is_file():
        payload = build_registry()
        save_registry(payload, cache)
    else:
        payload = json.loads(cache.read_text(encoding="utf-8"))
    return payload


def load_registry(cache_path: Path | None = None, *, refresh: bool = False) -> dict[int, MonsterRecord]:
    payload = load_registry_payload(cache_path, refresh=refresh)
    records: dict[int, MonsterRecord] = {}
    for key, data in payload.get("sprites", {}).items():
        records[int(key)] = MonsterRecord(**data)
    return records


def load_monsters_by_index(cache_path: Path | None = None, *, refresh: bool = False) -> dict[int, MonsterRecord]:
    payload = load_registry_payload(cache_path, refresh=refresh)
    records: dict[int, MonsterRecord] = {}
    for key, data in payload.get("monsters_by_index", {}).items():
        records[int(key)] = MonsterRecord(**data)
    return records


def load_sprite_claimants(cache_path: Path | None = None, *, refresh: bool = False) -> dict[int, list[dict]]:
    payload = load_registry_payload(cache_path, refresh=refresh)
    return {int(k): v for k, v in payload.get("claimants", {}).items()}


def load_sprite_overrides(path: Path | None = None) -> dict[int, dict]:
    overrides_path = path or DEFAULT_SPRITE_OVERRIDES
    if not overrides_path.is_file():
        return {}
    data = json.loads(overrides_path.read_text(encoding="utf-8"))
    raw = data.get("overrides", data)
    return {int(k): v for k, v in raw.items() if not str(k).startswith("_")}


def _record_for_control_index(
    sprite_number: int,
    source: MonsterRecord,
) -> MonsterRecord:
    """Rebind a MonsterRecord to the control file index (TRS order may differ from data sprite number)."""
    return MonsterRecord(
        monster_index=source.monster_index,
        name=source.name,
        descr=source.descr,
        sprite_number=sprite_number,
        sprite_role="spr1",
        parent_sprite_number=None,
        huge=source.huge,
        melee_weapon=source.melee_weapon,
        ranged_weapon=source.ranged_weapon,
        canvas=source.canvas,
    )


def resolve_sprite_record(
    sprite_number: int,
    registry: dict[int, MonsterRecord] | None = None,
    *,
    overrides: dict[int, dict] | None = None,
    monsters_by_index: dict[int, MonsterRecord] | None = None,
    claimants: dict[int, list[dict]] | None = None,
) -> tuple[MonsterRecord | None, list[str]]:
    """Resolve the monster identity for a control/TRS file index."""
    reg = registry if registry is not None else load_registry()
    ov = overrides if overrides is not None else load_sprite_overrides()
    by_idx = monsters_by_index if monsters_by_index is not None else load_monsters_by_index()
    dupes = claimants if claimants is not None else load_sprite_claimants()

    warnings: list[str] = []

    override = ov.get(sprite_number)
    if override is not None:
        note = override.get("note")
        if note:
            warnings.append(f"override: {note}")

        if "monster_index" in override:
            source = by_idx.get(int(override["monster_index"]))
            if source is None:
                warnings.append(f"override monster_index {override['monster_index']} not found")
            else:
                record = _record_for_control_index(sprite_number, source)
                if override.get("visual_subject"):
                    record = replace(record, visual_subject=str(override["visual_subject"]))
                return record, warnings

        if override.get("name"):
            record = MonsterRecord(
                monster_index=int(override.get("monster_index", 0)),
                name=str(override["name"]),
                descr=_truncate_descr(str(override.get("descr") or override["name"])),
                sprite_number=sprite_number,
                huge=bool(override.get("huge")),
                melee_weapon=override.get("melee_weapon"),
                ranged_weapon=override.get("ranged_weapon"),
                canvas=128 if override.get("huge") else int(override.get("canvas", 64)),
                visual_subject=override.get("visual_subject"),
            )
            return record, warnings

    record = reg.get(sprite_number)
    if record is None:
        return None, warnings

    names = [c["name"] for c in dupes.get(sprite_number, [])]
    if len(names) > 1:
        warnings.append(
            f"Monster Data lists {len(names)} monsters for sprite {sprite_number}: "
            f"{', '.join(names)} (using {record.name}; add coe5_sprite_overrides.json to fix)"
        )

    return _record_for_control_index(sprite_number, record), warnings


@dataclass
class SearchMatch:
    record: MonsterRecord
    score: float
    match_fields: list[str] = field(default_factory=list)


def _normalize_text(text: str) -> str:
    return re.sub(r"\s+", " ", text.lower().strip())


def _score_monster_record(query: str, record: MonsterRecord) -> tuple[float, list[str]]:
    q = _normalize_text(query)
    if not q:
        return 0.0, []

    name = _normalize_text(record.name)
    descr = _normalize_text(record.descr)
    weapons = _normalize_text(" ".join(filter(None, [record.melee_weapon, record.ranged_weapon])))

    score = 0.0
    fields: list[str] = []

    if name == q:
        score += 100
        fields.append("name:exact")
    elif name.startswith(q):
        score += 80
        fields.append("name:prefix")
    elif re.search(rf"\b{re.escape(q)}\b", name):
        score += 65
        fields.append("name:word")
    elif q in name:
        score += 45
        fields.append("name:substring")

    tokens = [t for t in re.split(r"\W+", q) if t]
    if tokens and all(t in name for t in tokens):
        score += 25
        fields.append("name:tokens")

    if q in descr:
        score += 20
        fields.append("descr")
    elif tokens and any(t in descr for t in tokens):
        score += 10
        fields.append("descr:token")

    if weapons and q in weapons:
        score += 15
        fields.append("weapon")
    elif tokens and any(t in weapons for t in tokens):
        score += 8
        fields.append("weapon:token")

    # Prefer spr1 when scores tie
    if record.sprite_role == "spr1":
        score += 1

    return score, fields


def search_monsters(
    query: str,
    registry: dict[int, MonsterRecord] | None = None,
    *,
    spr1_only: bool = True,
    limit: int = 25,
    min_score: float = 10.0,
) -> list[SearchMatch]:
    """Search monsters by name, description, or weapon text."""
    reg = registry if registry is not None else load_registry()
    matches: list[SearchMatch] = []

    for record in reg.values():
        if spr1_only and record.sprite_role != "spr1":
            continue
        score, fields = _score_monster_record(query, record)
        if score < min_score:
            continue
        matches.append(SearchMatch(record=record, score=score, match_fields=fields))

    matches.sort(
        key=lambda m: (-m.score, m.record.name.lower(), m.record.sprite_number),
    )
    return matches[:limit]


def format_search_results(matches: list[SearchMatch]) -> str:
    lines = []
    for index, match in enumerate(matches, start=1):
        r = match.record
        fields = ", ".join(match.match_fields) if match.match_fields else "?"
        weapon = r.melee_weapon or r.ranged_weapon or "-"
        huge = " huge" if r.huge else ""
        lines.append(
            f"{index:2d}. sprite {r.sprite_number:5d}  #{r.monster_index:4d}  "
            f"[{r.sprite_role}]  {r.name}{huge}  weapon={weapon}  score={match.score:.0f}  ({fields})"
        )
    return "\n".join(lines)


def lookup_by_query(
    query: str,
    registry: dict[int, MonsterRecord] | None = None,
    *,
    pick: int | None = None,
    spr1_only: bool = True,
) -> tuple[str, MonsterRecord | None, list[SearchMatch]]:
    """Resolve a lookup query to a single record or a candidate list.

    Returns (mode, record, matches) where mode is 'sprite', 'single', 'multi', or 'none'.
    """
    reg = registry if registry is not None else load_registry()
    stripped = query.strip()

    if stripped.isdigit():
        sn = int(stripped)
        record, _ = resolve_sprite_record(sn, reg)
        if record is None:
            return "none", None, []
        return "sprite", record, [SearchMatch(record=record, score=100.0, match_fields=["sprite_number"])]

    matches = search_monsters(stripped, reg, spr1_only=spr1_only)
    if not matches:
        return "none", None, []

    if pick is not None:
        if pick < 1 or pick > len(matches):
            raise ValueError(f"--pick must be between 1 and {len(matches)}")
        return "picked", matches[pick - 1].record, matches

    if len(matches) == 1:
        return "single", matches[0].record, matches

    return "multi", None, matches


def lookup_by_sprite_number(sprite_number: int, registry: dict[int, MonsterRecord] | None = None) -> MonsterRecord | None:
    record, _ = resolve_sprite_record(sprite_number, registry)
    return record


def resolve_control_path(sprite_number: int, controls_dir: Path | None = None) -> Path | None:
    root = controls_dir or DEFAULT_CONTROLS_DIR
    if not root.is_dir():
        return None
    candidates = [
        root / f"{sprite_number:04d}.tga",
        root / f"{sprite_number}.tga",
        root / f"{sprite_number:04d}.png",
        root / f"{sprite_number}.png",
    ]
    for path in candidates:
        if path.is_file():
            return path
    return None


def list_controls(
    controls_dir: Path | None = None,
    registry: dict[int, MonsterRecord] | None = None,
) -> list[ControlEntry]:
    root = controls_dir or DEFAULT_CONTROLS_DIR
    reg = registry if registry is not None else load_registry()
    entries: list[ControlEntry] = []

    if not root.is_dir():
        return entries

    seen: set[int] = set()
    for path in sorted(root.iterdir()):
        if path.suffix.lower() not in {".tga", ".png"}:
            continue
        stem = path.stem
        try:
            sprite_number = int(stem)
        except ValueError:
            continue
        if sprite_number in seen:
            continue
        seen.add(sprite_number)
        record, warnings = resolve_sprite_record(sprite_number, reg)
        if record is None:
            warnings = [*warnings, "no registry match"]
        entries.append(
            ControlEntry(
                sprite_number=sprite_number,
                path=path,
                record=record,
                mapped=record is not None,
                warnings=warnings,
            )
        )
    return entries


def main() -> int:
    parser = argparse.ArgumentParser(description="Build or query vanilla monster sprite registry.")
    parser.add_argument("--refresh", action="store_true", help="Rebuild cache from Monster Data")
    parser.add_argument(
        "--lookup",
        metavar="QUERY",
        default=None,
        help='Sprite number or search text (e.g. "Spearman", "knight bow")',
    )
    parser.add_argument(
        "--pick",
        type=int,
        default=None,
        help="Pick one result from a text search list (use with --lookup TEXT)",
    )
    parser.add_argument(
        "--all-roles",
        action="store_true",
        help="Include spr2 entries in text search (default: spr1 only)",
    )
    parser.add_argument("--list-controls", type=Path, default=None, nargs="?", const=DEFAULT_CONTROLS_DIR)
    parser.add_argument("--claimants", type=int, default=None, metavar="SPRITE", help="List Monster Data claimants for a sprite number")
    parser.add_argument("--cache", type=Path, default=DEFAULT_REGISTRY_CACHE)
    args = parser.parse_args()

    registry = load_registry(args.cache, refresh=args.refresh or not args.cache.is_file())
    payload = load_registry_payload(args.cache)

    if args.claimants is not None:
        claimants = payload.get("claimants", {})
        key = str(args.claimants)
        names = claimants.get(key)
        if not names:
            single = registry.get(args.claimants)
            if single:
                print(f"Sprite {args.claimants}: single claimant {single.name} (#{single.monster_index})")
            else:
                print(f"Sprite {args.claimants}: no claimants in registry")
            return 0
        print(f"Sprite {args.claimants} claimants ({len(names)}):")
        for item in names:
            print(f"  #{item['monster_index']:4d}  {item['name']}")
        override_record, override_warn = resolve_sprite_record(args.claimants, registry)
        if override_record:
            print(f"\nResolved for tuning: {override_record.name} (#{override_record.monster_index})")
        for w in override_warn:
            print(f"  note: {w}")
        return 0

    print(f"Registry: {args.cache}")
    print(f"Source:   {payload.get('source')}")
    print(f"Sprites:  {len(registry)}")

    if args.lookup is not None:
        try:
            mode, record, matches = lookup_by_query(
                args.lookup,
                registry,
                pick=args.pick,
                spr1_only=not args.all_roles,
            )
        except ValueError as exc:
            print(str(exc), file=__import__("sys").stderr)
            return 2

        if mode == "none":
            print(f'No matches for "{args.lookup}"')
            return 1

        if mode == "multi":
            print(f'Matches for "{args.lookup}":\n')
            print(format_search_results(matches))
            print(f"\n{len(matches)} matches. Re-run with --pick N to show full record.")
            return 0

        print(json.dumps(asdict(record), indent=2))
        return 0

    if args.list_controls is not None:
        controls = list_controls(args.list_controls, registry)
        print(f"\nControls in {args.list_controls}: {len(controls)}")
        for entry in controls[:30]:
            name = entry.record.name if entry.record else "?"
            warn = f" [{', '.join(entry.warnings)}]" if entry.warnings else ""
            print(f"  {entry.sprite_number:5d}  {name}{warn}  {entry.path.name}")
        if len(controls) > 30:
            print(f"  ... and {len(controls) - 30} more")
        return 0

    if args.refresh:
        print(f"Refreshed cache at {args.cache}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
