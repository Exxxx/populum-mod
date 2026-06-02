#!/usr/bin/env python3
"""Probe COE5 sprite art styles across anchor archetypes via ComfyUI."""
from __future__ import annotations

import argparse
import sys
import uuid
from pathlib import Path

from coe5_probe_common import (
    GracefulStop,
    StopController,
    probe_timestamp,
    run_probe_batch,
    write_manifest,
    write_probe_index_html,
)
from coe5_probe_paths import PROBE_STYLES_ROOT
from coe5_probe_state import (
    ProbeBatchState,
    delete_state,
    load_probe_state,
    reset_probe_outputs,
    save_probe_state,
)
from coe5_sprite_archetypes import ARCHETYPE_CATALOG, ARCHETYPE_BY_ID
from coe5_sprite_styles import DEFAULT_STYLE_ID, STYLE_CATALOG, build_style_probe_variations
from comfyui_client import (
    DEFAULT_COMFYUI_URL,
    WORKFLOW_TXT2IMG,
    load_workflow,
    run_txt2img_generation,
)

TOOLS_DIR = Path(__file__).resolve().parent


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate COE5 sprite style probe matrix via ComfyUI.")
    parser.add_argument("--url", default=DEFAULT_COMFYUI_URL)
    parser.add_argument("--workflow", type=Path, default=WORKFLOW_TXT2IMG)
    parser.add_argument("--output-dir", type=Path, default=PROBE_STYLES_ROOT)
    parser.add_argument("--archetypes", nargs="+", default=None, help="Archetype ids to probe")
    parser.add_argument("--styles", nargs="+", default=None, help="Style ids to probe")
    parser.add_argument("--limit", type=int, default=len(STYLE_CATALOG))
    parser.add_argument("--seed", type=int, default=None)
    parser.add_argument("--poll", type=float, default=2.0)
    parser.add_argument("--timeout", type=float, default=900.0)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--resume", action="store_true")
    parser.add_argument("--reset", action="store_true")
    parser.add_argument("--reset-all", action="store_true")
    parser.add_argument("--status", action="store_true")
    parser.add_argument("--list", action="store_true")
    return parser.parse_args()


def build_all_variations(args: argparse.Namespace) -> list[dict]:
    archetype_ids = args.archetypes or [a.id for a in ARCHETYPE_CATALOG]
    style_ids = args.styles or [item.id for item in STYLE_CATALOG[: args.limit]]
    variations: list[dict] = []
    for aid in archetype_ids:
        archetype = ARCHETYPE_BY_ID.get(aid)
        if archetype is None:
            continue
        variations.extend(
            build_style_probe_variations(
                archetype_id=archetype.id,
                subject=archetype.subject,
                canvas=archetype.canvas,
                huge=archetype.huge,
                entity_type=archetype.entity_type,
                style_ids=style_ids,
            )
        )
    return variations


def main() -> int:
    args = parse_args()

    if args.list:
        print("Styles:")
        for item in STYLE_CATALOG:
            note = f" ({item.notes})" if item.notes else ""
            print(f"  {item.id}\t{item.label}{note}")
        print("\nArchetypes:")
        for item in ARCHETYPE_CATALOG:
            print(f"  {item.id}\t{item.label} [{item.entity_type} {item.canvas}px]")
        print(f"\nDefault style: {DEFAULT_STYLE_ID}")
        return 0

    batch_root = args.output_dir.resolve()
    state_path = batch_root / "probe_state.json"

    if args.status or args.reset or args.reset_all:
        if args.status:
            existing = load_probe_state(state_path)
            if existing is None:
                print(f"No state at {state_path}")
                return 1
            print(f"State:  {state_path}")
            print(f"Status: {existing.status}")
            print(f"Done:   {len(existing.completed)}/{len(existing.variation_ids)}")
            return 0
        if args.reset_all:
            removed = reset_probe_outputs(batch_root)
            delete_state(state_path)
            print(f"Reset all: removed {removed} file(s)")
        elif args.reset:
            delete_state(state_path)
            print(f"Reset state: {state_path}")
        return 0

    variations = build_all_variations(args)
    variation_ids = [v["state_key"] for v in variations]

    existing = load_probe_state(state_path)
    if existing and not args.resume and not args.reset:
        print(f"Batch state exists: {state_path}\nUse --resume or --reset.", file=sys.stderr)
        return 2

    if args.resume:
        if existing is None:
            print("error: --resume but no probe_state.json", file=sys.stderr)
            return 2
        state = existing
        state.status = "running"
    else:
        state = ProbeBatchState(
            probe_type="sprite_styles",
            status="running",
            batch_root=str(batch_root),
            variation_ids=variation_ids,
            dry_run=args.dry_run,
        )
        save_probe_state(state)

    batch_root.mkdir(parents=True, exist_ok=True)
    print(f"Variations: {len(variations)}  Output: {batch_root}")

    workflow_template = None if args.dry_run else load_workflow(args.workflow)
    client_id = str(uuid.uuid4())
    stop_controller = StopController()
    if not args.dry_run:
        stop_controller.install()

    skip_ids = set(state.completed)
    archetype_by_id = ARCHETYPE_BY_ID

    def run_one(variation: dict, var_dir: Path, prefix: str):
        archetype = archetype_by_id.get(variation["archetype_id"])
        width = archetype.gen_width if archetype else 512
        height = archetype.gen_height if archetype else 512
        return run_txt2img_generation(
            base_url=args.url,
            workflow_template=workflow_template,
            client_id=client_id,
            prompt=variation["prompt"],
            filename_prefix=prefix,
            output_dir=var_dir,
            width=width,
            height=height,
            seed=args.seed,
            poll_seconds=args.poll,
            timeout_seconds=args.timeout,
        )

    def on_entry_done(entry: dict) -> None:
        if args.dry_run:
            return
        key = entry.get("state_key", "")
        if entry.get("status") in ("ok", "skipped"):
            state.mark_ok(key)
        elif entry.get("status") == "error":
            state.mark_failed(key)
        save_probe_state(state)

    stopped_early = False
    try:
        entries, failures, stopped_early = run_probe_batch(
            variations=variations,
            output_root=batch_root,
            run_one=run_one,
            dry_run=args.dry_run,
            skip_ids=skip_ids,
            stop_controller=stop_controller,
            on_entry_done=on_entry_done,
        )
    finally:
        if not args.dry_run:
            stop_controller.restore()

    if args.dry_run:
        delete_state(state_path)
    elif not stopped_early:
        state.status = "completed" if not failures else "completed_with_errors"
        save_probe_state(state)

    manifest = {
        "probe_type": "sprite_styles",
        "generated_at": probe_timestamp(),
        "default_style_id": DEFAULT_STYLE_ID,
        "variations": entries,
    }
    write_manifest(batch_root / "manifest.json", manifest)
    write_probe_index_html(
        batch_root / "index.html",
        title="COE5 sprite style probe",
        subtitle=f"{len(entries)} style×archetype variations · update coe5_probe_winners.json after review",
        entries=entries,
    )

    print(f"\nGallery: {batch_root / 'index.html'}")
    if stopped_early:
        print("\nStopped — run with --resume to continue.", file=sys.stderr)
        return 130
    if failures:
        print(f"Failed ({len(failures)}): {', '.join(failures)}", file=sys.stderr)
        return 1
    ok = sum(1 for e in entries if e.get("status") in ("ok", "skipped"))
    print(f"Done — {ok}/{len(entries)} succeeded")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
