"""Persistent state for resumable COE5 sprite probe and batch runs."""
from __future__ import annotations

import json
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


STATE_VERSION = 1


def timestamp() -> str:
    return datetime.now(timezone.utc).isoformat()


@dataclass
class ProbeBatchState:
    probe_type: str
    status: str
    batch_root: str
    variation_ids: list[str]
    dry_run: bool
    created_at: str = field(default_factory=timestamp)
    updated_at: str = field(default_factory=timestamp)
    completed: list[str] = field(default_factory=list)
    failed: list[str] = field(default_factory=list)
    stopped_reason: str | None = None

    @property
    def path(self) -> Path:
        return Path(self.batch_root) / "probe_state.json"

    def mark_ok(self, key: str) -> None:
        if key not in self.completed:
            self.completed.append(key)
        if key in self.failed:
            self.failed.remove(key)
        self.updated_at = timestamp()

    def mark_failed(self, key: str) -> None:
        if key not in self.failed:
            self.failed.append(key)
        self.updated_at = timestamp()

    def to_dict(self) -> dict[str, Any]:
        return {
            "version": STATE_VERSION,
            "probe_type": self.probe_type,
            "status": self.status,
            "batch_root": self.batch_root,
            "variation_ids": self.variation_ids,
            "dry_run": self.dry_run,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "completed": self.completed,
            "failed": self.failed,
            "stopped_reason": self.stopped_reason,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> ProbeBatchState:
        return cls(
            probe_type=data["probe_type"],
            status=data["status"],
            batch_root=data["batch_root"],
            variation_ids=list(data.get("variation_ids", [])),
            dry_run=bool(data.get("dry_run", False)),
            created_at=data.get("created_at", timestamp()),
            updated_at=data.get("updated_at", timestamp()),
            completed=list(data.get("completed", [])),
            failed=list(data.get("failed", [])),
            stopped_reason=data.get("stopped_reason"),
        )


@dataclass
class BatchRunState:
    jobs_path: str
    status: str
    phase: str | None
    dry_run: bool
    created_at: str = field(default_factory=timestamp)
    updated_at: str = field(default_factory=timestamp)
    completed: list[str] = field(default_factory=list)
    failed: list[str] = field(default_factory=list)
    stopped_reason: str | None = None

    @property
    def path(self) -> Path:
        return Path(self.jobs_path).with_name("batch_state.json")

    def mark_ok(self, job_id: str) -> None:
        if job_id not in self.completed:
            self.completed.append(job_id)
        if job_id in self.failed:
            self.failed.remove(job_id)
        self.updated_at = timestamp()

    def mark_failed(self, job_id: str) -> None:
        if job_id not in self.failed:
            self.failed.append(job_id)
        self.updated_at = timestamp()

    def to_dict(self) -> dict[str, Any]:
        return {
            "version": STATE_VERSION,
            "jobs_path": self.jobs_path,
            "status": self.status,
            "phase": self.phase,
            "dry_run": self.dry_run,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "completed": self.completed,
            "failed": self.failed,
            "stopped_reason": self.stopped_reason,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> BatchRunState:
        return cls(
            jobs_path=data["jobs_path"],
            status=data["status"],
            phase=data.get("phase"),
            dry_run=bool(data.get("dry_run", False)),
            created_at=data.get("created_at", timestamp()),
            updated_at=data.get("updated_at", timestamp()),
            completed=list(data.get("completed", [])),
            failed=list(data.get("failed", [])),
            stopped_reason=data.get("stopped_reason"),
        )


def load_probe_state(path: Path) -> ProbeBatchState | None:
    if not path.is_file():
        return None
    data = json.loads(path.read_text(encoding="utf-8"))
    if data.get("version") != STATE_VERSION:
        raise ValueError(f"Unsupported probe state version in {path}")
    return ProbeBatchState.from_dict(data)


def save_probe_state(state: ProbeBatchState) -> None:
    path = state.path
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(".json.tmp")
    tmp.write_text(json.dumps(state.to_dict(), indent=2) + "\n", encoding="utf-8")
    tmp.replace(path)


def load_batch_state(path: Path) -> BatchRunState | None:
    if not path.is_file():
        return None
    data = json.loads(path.read_text(encoding="utf-8"))
    if data.get("version") != STATE_VERSION:
        raise ValueError(f"Unsupported batch state version in {path}")
    return BatchRunState.from_dict(data)


def save_batch_state(state: BatchRunState) -> None:
    path = state.path
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(".json.tmp")
    tmp.write_text(json.dumps(state.to_dict(), indent=2) + "\n", encoding="utf-8")
    tmp.replace(path)


def delete_state(path: Path) -> bool:
    if path.is_file():
        path.unlink()
        return True
    return False


def reset_probe_outputs(root: Path) -> int:
    removed = 0
    if not root.is_dir():
        return 0
    for pattern in ("**/*.webp", "**/*.png", "**/manifest.json", "**/index.html"):
        for file in root.glob(pattern):
            file.unlink(missing_ok=True)
            removed += 1
    return removed
