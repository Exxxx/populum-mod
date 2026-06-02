"""Parse CoE5 mod files and build jobs for missing sprite assets."""
from __future__ import annotations

import argparse
import json
import re
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path

from coe5_probe_common import probe_timestamp, write_probe_index_html
from coe5_sprite_prompts import build_sprite_subject, infer_attack_action
from coe5_sprite_jobs import save_jobs_json

QUOTE_RE = re.compile(r'^(\S+)\s+"((?:[^"\\]|\\.)*)"\s*(?:#.*)?$')
TOKEN_RE = re.compile(r'^(\S+)(?:\s+(.+?))?\s*(?:#.*)?$')


@dataclass
class EntityBlock:
    kind: str  # monster | item | terrain
    name: str = ""
    line: int = 0
    spr1: str | None = None
    spr2: str | None = None
    spr: str | None = None
    descr: str | None = None
    huge: bool = False
    copyspr: bool = False
    melee_weapon: str | None = None
    ranged_weapon: str | None = None


@dataclass
class ScanResult:
    mod_file: Path
    mod_root: Path
    jobs: list[dict] = field(default_factory=list)
    referenced_paths: dict[str, dict] = field(default_factory=dict)
    missing_paths: set[str] = field(default_factory=set)


def parse_quoted_command(line: str) -> tuple[str, str] | None:
    match = QUOTE_RE.match(line.strip())
    if not match:
        return None
    return match.group(1), match.group(2)


def parse_weapon(line: str) -> str | None:
    stripped = line.strip()
    if not stripped.startswith(("meleeweapon", "rangedweapon")):
        return None
    quoted = re.search(r'"([^"]+)"', stripped)
    if quoted:
        return quoted.group(1).strip()
    return None


def canvas_for_monster(huge: bool) -> int:
    return 128 if huge else 64


def subject_for_block(block: EntityBlock, *, include_descr: bool = False) -> str:
    if block.name:
        return build_sprite_subject(
            name=block.name,
            melee_weapon=block.melee_weapon,
            ranged_weapon=block.ranged_weapon,
            huge=block.huge,
            descr=block.descr,
            include_descr=include_descr,
        )
    return f"fantasy {block.kind}"


def slugify(text: str) -> str:
    slug = re.sub(r"[^a-zA-Z0-9]+", "_", text.strip().lower()).strip("_")
    return slug or "sprite"


def is_missing(path: Path, *, strict: bool = False) -> bool:
    if not path.is_file():
        return True
    if strict and path.stat().st_size == 0:
        return True
    return False


def scan_c5m(mod_file: Path, *, strict: bool = False) -> ScanResult:
    mod_file = mod_file.resolve()
    mod_root = mod_file.parent
    result = ScanResult(mod_file=mod_file, mod_root=mod_root)

    current: EntityBlock | None = None
    lines = mod_file.read_text(encoding="utf-8", errors="replace").splitlines()

    def flush_block() -> None:
        nonlocal current
        if current is None:
            return
        _collect_block(result, current)
        current = None

    for line_no, raw in enumerate(lines, start=1):
        stripped = raw.strip()
        if not stripped or stripped.startswith("#"):
            continue

        if stripped.startswith("newmonster"):
            flush_block()
            match = QUOTE_RE.match(stripped)
            name = match.group(2) if match else stripped.split(None, 1)[-1].strip('"')
            current = EntityBlock(kind="monster", name=name, line=line_no)
            continue

        if stripped.startswith("newitem"):
            flush_block()
            match = QUOTE_RE.match(stripped)
            name = match.group(2) if match else stripped.split(None, 1)[-1].strip('"')
            current = EntityBlock(kind="item", name=name, line=line_no)
            continue

        if stripped.startswith("selectterr") or stripped.startswith("newterr"):
            flush_block()
            parts = stripped.split()
            terr_id = parts[1] if len(parts) > 1 else "unknown"
            current = EntityBlock(kind="terrain", name=f"terrain {terr_id}", line=line_no)
            continue

        if current is None:
            continue

        quoted = parse_quoted_command(stripped)
        if quoted:
            cmd, value = quoted
            if cmd == "spr1":
                current.spr1 = value
            elif cmd == "spr2":
                current.spr2 = value
            elif cmd == "spr":
                current.spr = value
            elif cmd == "descr":
                current.descr = value
            elif cmd == "name":
                current.name = value
            elif cmd == "copyspr":
                current.copyspr = True
            continue

        token = TOKEN_RE.match(stripped)
        if not token:
            continue
        cmd = token.group(1)
        if cmd == "huge":
            current.huge = True
        elif cmd in ("meleeweapon", "rangedweapon"):
            weapon = parse_weapon(stripped)
            if weapon:
                if cmd == "meleeweapon":
                    current.melee_weapon = weapon
                else:
                    current.ranged_weapon = weapon

    flush_block()
    for rel_path in result.referenced_paths:
        abs_path = result.mod_root / rel_path.replace("/", "\\")
        if is_missing(abs_path, strict=strict):
            result.missing_paths.add(rel_path)
    _build_jobs_from_missing(result)
    return result


def _register_path(result: ScanResult, rel_path: str, meta: dict) -> None:
    if rel_path not in result.referenced_paths:
        result.referenced_paths[rel_path] = meta
    else:
        existing = result.referenced_paths[rel_path]
        if not existing.get("entity_name") and meta.get("entity_name"):
            existing["entity_name"] = meta["entity_name"]


def _collect_block(result: ScanResult, block: EntityBlock) -> None:
    if block.kind == "monster" and block.copyspr:
        return

    meta_base = {
        "entity_type": block.kind,
        "entity_name": block.name,
        "c5m_line": block.line,
        "huge": block.huge,
        "descr": block.descr,
        "melee_weapon": block.melee_weapon,
        "ranged_weapon": block.ranged_weapon,
    }

    if block.kind == "monster":
        if block.spr1:
            _register_path(
                result,
                block.spr1.replace("\\", "/"),
                {**meta_base, "sprite_role": "spr1", "paired_spr2_path": block.spr2},
            )
        if block.spr2 and block.spr2 != block.spr1:
            _register_path(
                result,
                block.spr2.replace("\\", "/"),
                {
                    **meta_base,
                    "sprite_role": "spr2",
                    "reference_path": block.spr1,
                },
            )
    elif block.spr:
        _register_path(
            result,
            block.spr.replace("\\", "/"),
            {**meta_base, "sprite_role": "spr1"},
        )


def _build_jobs_from_missing(result: ScanResult) -> None:
    for rel_path in sorted(result.missing_paths):
        meta = result.referenced_paths[rel_path]
        entity_type = meta["entity_type"]
        role = meta.get("sprite_role", "spr1")
        huge = bool(meta.get("huge", False))
        canvas = canvas_for_monster(huge) if entity_type == "monster" else 64
        if entity_type == "terrain":
            canvas = 64

        block = EntityBlock(
            kind=entity_type,
            name=meta.get("entity_name", ""),
            line=meta.get("c5m_line", 0),
            descr=meta.get("descr"),
            huge=huge,
            melee_weapon=meta.get("melee_weapon"),
            ranged_weapon=meta.get("ranged_weapon"),
        )
        subject = subject_for_block(block)
        attack_action = infer_attack_action(
            melee_weapon=meta.get("melee_weapon"),
            ranged_weapon=meta.get("ranged_weapon"),
        )

        job_id = f"{slugify(meta.get('entity_name', rel_path))}_{role}_{Path(rel_path).stem}"

        job = {
            "id": job_id,
            "entity_type": entity_type,
            "entity_name": meta.get("entity_name", ""),
            "c5m_line": meta.get("c5m_line"),
            "sprite_role": role,
            "target_path": rel_path,
            "target_abs": str((result.mod_root / rel_path).resolve()),
            "huge": huge,
            "canvas": canvas,
            "subject": subject,
            "attack_action": attack_action,
            "melee_weapon": meta.get("melee_weapon"),
            "ranged_weapon": meta.get("ranged_weapon"),
        }
        if meta.get("paired_spr2_path"):
            job["paired_spr2_path"] = meta["paired_spr2_path"]
        if meta.get("reference_path"):
            job["reference_path"] = meta["reference_path"]
            ref_abs = result.mod_root / meta["reference_path"]
            job["reference_abs"] = str(ref_abs.resolve())

        result.jobs.append(job)


def scan_summary(result: ScanResult) -> dict[str, int]:
    counts: dict[str, int] = {"spr1": 0, "spr2": 0, "item": 0, "terrain": 0, "total": len(result.jobs)}
    for job in result.jobs:
        role = job.get("sprite_role", "spr1")
        etype = job.get("entity_type", "monster")
        if role == "spr2":
            counts["spr2"] += 1
        elif etype == "item":
            counts["item"] += 1
        elif etype == "terrain":
            counts["terrain"] += 1
        else:
            counts["spr1"] += 1
    return counts


def write_scan_report(result: ScanResult, path: Path) -> None:
    entries = []
    for job in result.jobs:
        entries.append(
            {
                "state_key": job["id"],
                "label": f"{job['entity_name']} ({job['sprite_role']})",
                "prompt": job["target_path"],
                "status": f"line {job.get('c5m_line')} · {job.get('entity_type')}",
            }
        )
    counts = scan_summary(result)
    write_probe_index_html(
        path,
        title=f"Missing sprites — {result.mod_file.name}",
        subtitle=(
            f"{counts['total']} missing · spr1={counts['spr1']} spr2={counts['spr2']} "
            f"item={counts['item']} terrain={counts['terrain']}"
        ),
        entries=entries,
        id_key="state_key",
    )


def build_jobs_payload(result: ScanResult) -> dict:
    return {
        "mod_file": str(result.mod_file),
        "mod_root": str(result.mod_root),
        "scanned_at": probe_timestamp(),
        "missing_count": len(result.jobs),
        "summary": scan_summary(result),
        "jobs": result.jobs,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Scan a CoE5 mod .c5m for missing sprite files.")
    parser.add_argument("mod_file", type=Path, help="Path to mod .c5m file")
    parser.add_argument("--write", type=Path, default=None, help="Write jobs JSON to this path")
    parser.add_argument("--report", type=Path, default=None, help="Write HTML scan report")
    parser.add_argument("--strict", action="store_true", help="Treat zero-byte files as missing")
    args = parser.parse_args()

    result = scan_c5m(args.mod_file, strict=args.strict)
    payload = build_jobs_payload(result)
    counts = payload["summary"]

    print(f"Mod:     {result.mod_file}")
    print(f"Root:    {result.mod_root}")
    print(f"Missing: {counts['total']} (spr1={counts['spr1']} spr2={counts['spr2']} item={counts['item']} terrain={counts['terrain']})")

    for job in result.jobs[:20]:
        print(f"  [{job['sprite_role']}] {job['target_path']} — {job['entity_name']}")
    if len(result.jobs) > 20:
        print(f"  ... and {len(result.jobs) - 20} more")

    if args.write:
        save_jobs_json(args.write, payload)
        print(f"Wrote jobs: {args.write}")

    if args.report:
        write_scan_report(result, args.report)
        print(f"Wrote report: {args.report}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
