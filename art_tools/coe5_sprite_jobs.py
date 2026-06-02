"""Job catalog datatypes for COE5 sprite batch generation."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

TOOLS_DIR = Path(__file__).resolve().parent
DEFAULT_JOBS_PATH = TOOLS_DIR / "generated" / "missing_sprites_jobs.json"


def load_jobs_json(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if "jobs" not in data:
        raise ValueError(f"Jobs file missing 'jobs' list: {path}")
    return data


def save_jobs_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def pass_for_job(job: dict[str, Any]) -> str:
    role = job.get("sprite_role", "spr1")
    if role == "spr2":
        return "spr2"
    return "spr1"


def filter_jobs_for_phase(jobs: list[dict[str, Any]], phase: str | None) -> list[dict[str, Any]]:
    if phase is None:
        return sorted(jobs, key=lambda j: (pass_for_job(j), j.get("id", "")))
    if phase == "spr1":
        return sorted([j for j in jobs if pass_for_job(j) == "spr1"], key=lambda j: j.get("id", ""))
    if phase == "spr2":
        return sorted([j for j in jobs if pass_for_job(j) == "spr2"], key=lambda j: j.get("id", ""))
    raise ValueError(f"Unknown phase: {phase}")


def apply_job_filters(
    jobs: list[dict[str, Any]],
    *,
    ids: list[str] | None = None,
    entity_type: str | None = None,
    limit: int | None = None,
) -> list[dict[str, Any]]:
    filtered = jobs
    if entity_type:
        filtered = [j for j in filtered if j.get("entity_type") == entity_type]
    if ids:
        id_set = set(ids)
        filtered = [j for j in filtered if j.get("id") in id_set]
    if limit is not None:
        filtered = filtered[:limit]
    return filtered
