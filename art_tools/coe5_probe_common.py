"""Shared helpers for COE5 sprite ComfyUI probe runs."""
from __future__ import annotations

import json
import signal
from datetime import datetime, timezone
from pathlib import Path
from typing import Callable

from coe5_probe_paths import find_existing_probe_image


class GracefulStop(Exception):
    """Raised when the user requests a graceful shutdown (Ctrl+C)."""


class StopController:
    def __init__(self) -> None:
        self.requested = False
        self.reason = "interrupt"
        self._previous_handler = None

    def install(self) -> None:
        def _handler(signum, frame):  # noqa: ARG001
            if not self.requested:
                self.requested = True
                self.reason = "SIGINT"
                print("\nStop requested — finishing current image, then saving state...", flush=True)
            else:
                print("\nForce quit.", flush=True)
                raise KeyboardInterrupt

        try:
            self._previous_handler = signal.signal(signal.SIGINT, _handler)
        except (ValueError, OSError):
            pass

    def restore(self) -> None:
        if self._previous_handler is not None:
            try:
                signal.signal(signal.SIGINT, self._previous_handler)
            except (ValueError, OSError):
                pass

    def check(self) -> None:
        if self.requested:
            raise GracefulStop(self.reason)


def probe_timestamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def write_manifest(path: Path, payload: dict) -> None:
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def write_probe_index_html(
    path: Path,
    *,
    title: str,
    subtitle: str,
    entries: list[dict],
    id_key: str = "state_key",
    label_key: str = "label",
) -> None:
    rows = []
    for entry in entries:
        file_name = entry.get("output_file")
        img = f'<img src="{file_name}" alt="{entry.get(id_key, "")}">' if file_name else "<em>not generated</em>"
        meta_parts = []
        if entry.get("style_id"):
            meta_parts.append(f"style: {entry['style_id']}")
        if entry.get("archetype_id"):
            meta_parts.append(f"archetype: {entry['archetype_id']}")
        if entry.get("status"):
            meta_parts.append(f"status: {entry['status']}")
        meta = f"<p><em>{' · '.join(meta_parts)}</em></p>" if meta_parts else ""
        rows.append(
            f"""
            <section>
              <h2>{entry.get(id_key, '')} — {entry.get(label_key, '')}</h2>
              {meta}
              {img}
              <p><code>{entry.get("prompt", "")}</code></p>
            </section>
            """
        )
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>{title}</title>
  <style>
    body {{ font-family: sans-serif; max-width: 980px; margin: 2rem auto; padding: 0 1rem; }}
    img {{ max-width: 320px; height: auto; border: 1px solid #ccc; image-rendering: pixelated; }}
    section {{ margin-bottom: 2.5rem; padding-bottom: 1.5rem; border-bottom: 1px solid #eee; }}
    code {{ display: block; white-space: pre-wrap; font-size: 0.85rem; color: #333; }}
  </style>
</head>
<body>
  <h1>{title}</h1>
  <p>{subtitle}</p>
  {"".join(rows)}
</body>
</html>
"""
    path.write_text(html, encoding="utf-8")


def run_probe_batch(
    *,
    variations: list[dict],
    output_root: Path,
    run_one: Callable[..., Path | None],
    dry_run: bool,
    skip_ids: set[str] | None = None,
    stop_controller: StopController | None = None,
    on_entry_done: Callable[[dict], None] | None = None,
) -> tuple[list[dict], list[str], bool]:
    manifest_entries: list[dict] = []
    failures: list[str] = []
    skip_ids = skip_ids or set()
    stopped_early = False

    for index, variation in enumerate(variations, start=1):
        if stop_controller:
            try:
                stop_controller.check()
            except GracefulStop:
                stopped_early = True
                break

        state_key = variation.get("state_key") or variation.get("style_id", f"var_{index}")
        style_id = variation.get("style_id", "unknown")
        archetype_id = variation.get("archetype_id", "unknown")
        var_dir = output_root / style_id
        prefix = f"{archetype_id}"

        print(f"[{index}/{len(variations)}] {state_key} - {variation.get('label', '')}")

        entry = {
            **variation,
            "filename_prefix": prefix,
            "output_file": f"{style_id}/{prefix}.webp",
            "status": "dry_run" if dry_run else "pending",
        }

        if dry_run:
            print(f"  file: {var_dir / f'{prefix}.webp'}")
            print(f"  prompt: {variation['prompt'][:140]}...")
            manifest_entries.append(entry)
            continue

        var_dir.mkdir(parents=True, exist_ok=True)
        existing = find_existing_probe_image(var_dir, prefix)
        if state_key in skip_ids or existing is not None:
            entry["output_file"] = f"{style_id}/{existing.name}" if existing else entry["output_file"]
            entry["status"] = "skipped"
            print(f"  skip (already done): {entry['output_file']}")
            manifest_entries.append(entry)
            if on_entry_done:
                on_entry_done(entry)
            continue

        try:
            saved = run_one(variation, var_dir, prefix)
            if saved:
                entry["output_file"] = f"{style_id}/{saved.name}"
                entry["status"] = "ok"
                print(f"  saved {saved}")
            else:
                entry["status"] = "missing_output"
                print("  warning: output file not found")
        except GracefulStop:
            stopped_early = True
            entry["status"] = "stopped"
            manifest_entries.append(entry)
            break
        except (OSError, TimeoutError, RuntimeError) as exc:
            entry["status"] = "error"
            entry["error"] = str(exc)
            failures.append(state_key)
            print(f"  ERROR: {exc}")

        manifest_entries.append(entry)
        if on_entry_done:
            on_entry_done(entry)

    return manifest_entries, failures, stopped_early
