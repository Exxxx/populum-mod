#!/usr/bin/env python3
"""Batch monster style tuning probe against vanilla control sprites."""
from __future__ import annotations

import argparse
import json
import shutil
import sys
import uuid
from pathlib import Path

from coe5_probe_common import GracefulStop, StopController, probe_timestamp
from coe5_probe_gallery import write_tiled_comparison_html, write_tiled_manifest
from coe5_probe_paths import GENERATED_DIR
from coe5_probe_state import ProbeBatchState, delete_state, load_probe_state, reset_probe_outputs, save_probe_state
from coe5_sprite_background import BgMode, add_bg_cli_args, chroma_config_for_probe
from coe5_sprite_prompts import (
    build_monster_tuning_edit_prompt,
    build_monster_tuning_prompt,
    build_tuning_negative_prompt,
)
from coe5_sprite_sizes import canvas_for_monster, generation_size_for_canvas
from coe5_style_families import STYLE_BY_ID, style_ids_for_families
from comfyui_client import (
    DEFAULT_COMFYUI_URL,
    WORKFLOW_EDIT,
    WORKFLOW_TXT2IMG,
    load_workflow,
    run_edit_generation,
    run_txt2img_generation,
)
from monster_sprite_registry import (
    DEFAULT_CONTROLS_DIR,
    ControlEntry,
    load_registry,
    lookup_by_query,
    resolve_control_path,
    resolve_sprite_record,
)
from sprite_processor import process_and_export

TOOLS_DIR = Path(__file__).resolve().parent
DEFAULT_TUNING_ROOT = GENERATED_DIR / "probes" / "monster_tuning"
DEFAULT_CONTROLS_JSON = TOOLS_DIR / "coe5_tuning_controls.json"
GenerationMode = str


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Probe monster sprite styles against vanilla controls.")
    parser.add_argument("--controls", type=Path, default=DEFAULT_CONTROLS_DIR)
    parser.add_argument("--controls-json", type=Path, default=DEFAULT_CONTROLS_JSON)
    parser.add_argument("--sprites", nargs="+", type=int, default=None, help="Sprite numbers to probe")
    parser.add_argument(
        "--lookup",
        metavar="QUERY",
        default=None,
        help='Resolve sprite from name or number (e.g. "Storm Titan", "1018")',
    )
    parser.add_argument(
        "--pick",
        type=int,
        default=None,
        help="Pick one result from a text search list (use with --lookup TEXT)",
    )
    parser.add_argument("--families", nargs="+", choices=("fidelity", "original", "legacy"), default=["fidelity", "original"])
    parser.add_argument("--styles", nargs="+", default=None, help="Explicit style ids")
    parser.add_argument(
        "--mode",
        choices=("txt2img", "edit"),
        default="txt2img",
        help="txt2img: text-only generation; edit: style transfer from control PNG",
    )
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_TUNING_ROOT)
    parser.add_argument("--url", default=DEFAULT_COMFYUI_URL)
    parser.add_argument("--workflow", type=Path, default=WORKFLOW_TXT2IMG)
    parser.add_argument("--workflow-edit", type=Path, default=WORKFLOW_EDIT)
    parser.add_argument("--seed", type=int, default=None)
    parser.add_argument("--poll", type=float, default=2.0)
    parser.add_argument("--timeout", type=float, default=900.0)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--resume", action="store_true")
    parser.add_argument("--reset", action="store_true")
    parser.add_argument("--reset-all", action="store_true")
    parser.add_argument("--refresh-registry", action="store_true")
    parser.add_argument("--keep-raw", action="store_true", help="Save ComfyUI output before post-process as {style}_raw.png")
    parser.add_argument("--list", action="store_true")
    add_bg_cli_args(parser)
    return parser.parse_args()


def load_sprite_numbers(args: argparse.Namespace, registry: dict) -> list[int]:
    if args.lookup is not None:
        mode, record, matches = lookup_by_query(
            args.lookup,
            registry,
            pick=args.pick,
            spr1_only=True,
        )
        if mode == "none":
            raise SystemExit(f'No registry matches for "{args.lookup}"')
        if mode == "multi":
            from monster_sprite_registry import format_search_results

            print(f'Matches for "{args.lookup}":\n')
            print(format_search_results(matches))
            raise SystemExit(f"\n{len(matches)} matches. Re-run with --pick N.")
        assert record is not None
        return [record.sprite_number]
    if args.sprites:
        return args.sprites
    if args.controls_json.is_file():
        data = json.loads(args.controls_json.read_text(encoding="utf-8"))
        return list(data.get("sprite_numbers", []))
    return [0, 1002, 1018, 2006]


def resolve_controls(args: argparse.Namespace, registry: dict) -> list[ControlEntry]:
    entries: list[ControlEntry] = []
    for sn in load_sprite_numbers(args, registry):
        path = resolve_control_path(sn, args.controls)
        record, resolve_warnings = resolve_sprite_record(sn, registry)
        warnings: list[str] = list(resolve_warnings)
        if path is None:
            warnings.append("control file missing")
        if record is None:
            warnings.append("no registry match")
        elif record.sprite_role == "spr2":
            warnings.append("spr2 control — consider spr1 for tuning")
        entries.append(
            ControlEntry(
                sprite_number=sn,
                path=path or (args.controls / f"{sn:04d}.tga"),
                record=record,
                mapped=record is not None and path is not None,
                warnings=warnings,
            )
        )
    return entries


def build_variations(
    controls: list[ControlEntry],
    style_ids: list[str],
    registry: dict,
    *,
    bg_mode: BgMode = "chroma",
    generation_mode: str = "txt2img",
) -> list[dict]:
    variations: list[dict] = []
    for control in controls:
        if control.record is None:
            continue
        record = control.record
        canvas = canvas_for_monster(huge=record.huge, control_path=control.path if control.path.is_file() else None)
        for sid in style_ids:
            recipe = STYLE_BY_ID.get(sid)
            if recipe is None:
                continue
            if generation_mode == "edit":
                prompt = build_monster_tuning_edit_prompt(record=record, style_id=sid, canvas=canvas, bg_mode=bg_mode)
            else:
                prompt = build_monster_tuning_prompt(record=record, style_id=sid, canvas=canvas, bg_mode=bg_mode)
            state_key = f"{record.sprite_number}__{sid}__{generation_mode}"
            variations.append(
                {
                    "state_key": state_key,
                    "style_id": sid,
                    "style_label": recipe.label,
                    "style_family": recipe.family,
                    "sprite_number": record.sprite_number,
                    "monster_name": record.name,
                    "control_path": str(control.path) if control.path else None,
                    "prompt": prompt,
                    "canvas": canvas,
                    "huge": record.huge,
                    "generation_mode": generation_mode,
                    "label": f"{record.name} · {recipe.label}",
                }
            )
    return variations


def main() -> int:
    args = parse_args()

    if args.list:
        from coe5_style_families import STYLE_CATALOG

        print("Families: fidelity, original, legacy")
        for item in STYLE_CATALOG:
            print(f"  {item.id}\t[{item.family}]\t{item.label}")
        return 0

    batch_root = args.output_dir.resolve()
    state_path = batch_root / "probe_state.json"

    if args.reset or args.reset_all:
        if args.reset_all:
            removed = reset_probe_outputs(batch_root)
            delete_state(state_path)
            print(f"Reset all: removed {removed} file(s)")
        else:
            delete_state(state_path)
            print(f"Reset state: {state_path}")
        if not args.dry_run and not args.resume:
            return 0

    registry = load_registry(refresh=args.refresh_registry)
    style_ids = args.styles or style_ids_for_families(args.families)
    controls = resolve_controls(args, registry)

    print(
        f"Controls: {len(controls)}  Styles: {len(style_ids)}  Mode: {args.mode}  Output: {batch_root}"
    )
    for c in controls:
        name = c.record.name if c.record else "?"
        warn = f"  WARN: {', '.join(c.warnings)}" if c.warnings else ""
        print(f"  sprite {c.sprite_number:5d}  {name}{warn}")

    variations = build_variations(
        controls,
        style_ids,
        registry,
        bg_mode=args.bg_mode,
        generation_mode=args.mode,
    )
    if not variations:
        print("No variations to run (check controls + registry).", file=sys.stderr)
        return 2

    existing = load_probe_state(state_path)
    if existing and not args.resume and not args.reset and not args.dry_run:
        print(f"State exists: {state_path}\nUse --resume or --reset.", file=sys.stderr)
        return 2

    if args.resume and existing:
        state = existing
        state.status = "running"
    else:
        state = ProbeBatchState(
            probe_type="monster_tuning",
            status="running",
            batch_root=str(batch_root),
            variation_ids=[v["state_key"] for v in variations],
            dry_run=args.dry_run,
        )
        if not args.dry_run:
            save_probe_state(state)

    workflow_template = None if args.dry_run else load_workflow(args.workflow)
    edit_template = None if args.dry_run or args.mode != "edit" else load_workflow(args.workflow_edit)
    client_id = str(uuid.uuid4())
    stop_controller = StopController()
    if not args.dry_run:
        stop_controller.install()

    skip_ids = set(state.completed)
    style_columns = [{"id": "control", "label": "Control"}]
    for sid in style_ids:
        recipe = STYLE_BY_ID.get(sid)
        style_columns.append({"id": sid, "label": recipe.label if recipe else sid})

    rows_by_sprite: dict[int, dict] = {}
    failures: list[str] = []
    stopped_early = False

    for index, var in enumerate(variations, start=1):
        if stop_controller:
            try:
                stop_controller.check()
            except GracefulStop:
                stopped_early = True
                break

        state_key = var["state_key"]
        sn = var["sprite_number"]
        sid = var["style_id"]
        sprite_dir = batch_root / str(sn)
        out_name = f"{sid}.webp"
        out_path = sprite_dir / out_name

        if sn not in rows_by_sprite:
            control_rel = None
            cp = var.get("control_path")
            if cp and Path(cp).is_file():
                control_rel = Path(f"../{sn}/control{Path(cp).suffix}").as_posix()
            rows_by_sprite[sn] = {
                "sprite_number": sn,
                "label": var["monster_name"],
                "cells": {
                    "control": {
                        "image": control_rel,
                        "prompt": "vanilla control reference",
                        "status": "control",
                    }
                },
            }

        print(f"[{index}/{len(variations)}] {state_key}")

        if args.dry_run:
            prompt = var["prompt"]
            print(f"  prompt ({len(prompt)} chars): {prompt[:120]}...")
            rows_by_sprite[sn]["cells"][sid] = {"prompt": prompt, "status": "dry_run"}
            continue

        sprite_dir.mkdir(parents=True, exist_ok=True)

        cp = var.get("control_path")
        if cp and Path(cp).is_file():
            control_dest = sprite_dir / f"control{Path(cp).suffix.lower()}"
            if not control_dest.is_file():
                control_dest.write_bytes(Path(cp).read_bytes())
            rows_by_sprite[sn]["cells"]["control"]["image"] = f"{sn}/{control_dest.name}"

        if state_key in skip_ids and out_path.is_file():
            print(f"  skip (done): {out_path.name}")
            rows_by_sprite[sn]["cells"][sid] = {
                "image": f"{sn}/{out_name}",
                "prompt": var["prompt"],
                "status": "skipped",
            }
            continue

        width, height = generation_size_for_canvas(var["canvas"])
        try:
            inter_dir = batch_root / "_intermediate"
            inter_dir.mkdir(parents=True, exist_ok=True)
            prefix = state_key.replace("__", "_")

            if args.mode == "edit":
                ref_path = Path(cp) if cp else None
                if ref_path is None or not ref_path.is_file():
                    raise FileNotFoundError(f"edit mode requires control file for sprite {sn}")
                saved = run_edit_generation(
                    base_url=args.url,
                    workflow_template=edit_template,
                    client_id=client_id,
                    prompt=var["prompt"],
                    reference_path=ref_path,
                    output_dir=inter_dir,
                    output_name=prefix,
                    seed=args.seed,
                    poll_seconds=args.poll,
                    timeout_seconds=args.timeout,
                )
            else:
                saved = run_txt2img_generation(
                    base_url=args.url,
                    workflow_template=workflow_template,
                    client_id=client_id,
                    prompt=var["prompt"],
                    filename_prefix=prefix,
                    output_dir=inter_dir,
                    width=width,
                    height=height,
                    seed=args.seed,
                    poll_seconds=args.poll,
                    timeout_seconds=args.timeout,
                    negative=build_tuning_negative_prompt(args.bg_mode),
                )
            if saved is None:
                raise RuntimeError("ComfyUI returned no output")

            png_path = sprite_dir / f"{sid}.png"
            if args.keep_raw:
                raw_path = sprite_dir / f"{sid}_raw.png"
                shutil.copy2(saved, raw_path)
                print(f"  raw {raw_path.name}")

            chroma_config = chroma_config_for_probe(args, cp)
            debug_mask = png_path.with_name(f"{sid}_keymask.png") if args.debug_mask else None
            process_and_export(
                saved,
                png_path,
                entity_type="monster",
                canvas=var["canvas"],
                bg_mode=args.bg_mode,
                chroma_config=chroma_config,
                debug_mask_path=debug_mask,
            )
            rows_by_sprite[sn]["cells"][sid] = {
                "image": f"{sn}/{png_path.name}",
                "prompt": var["prompt"],
                "status": "ok",
            }
            state.mark_ok(state_key)
            save_probe_state(state)
            print(f"  saved {png_path}")
        except (OSError, TimeoutError, RuntimeError) as exc:
            failures.append(state_key)
            rows_by_sprite[sn]["cells"][sid] = {
                "prompt": var["prompt"],
                "status": f"error: {exc}",
            }
            state.mark_failed(state_key)
            save_probe_state(state)
            print(f"  ERROR: {exc}")

    if not args.dry_run:
        stop_controller.restore()
        if not stopped_early:
            state.status = "completed" if not failures else "completed_with_errors"
            save_probe_state(state)

    rows = [rows_by_sprite[k] for k in sorted(rows_by_sprite)]
    batch_root.mkdir(parents=True, exist_ok=True)
    manifest = {
        "probe_type": "monster_tuning",
        "generated_at": probe_timestamp(),
        "families": args.families,
        "style_ids": style_ids,
        "generation_mode": args.mode,
        "rows": rows,
    }
    write_tiled_manifest(batch_root / "manifest.json", manifest)
    write_tiled_comparison_html(
        batch_root / "index.html",
        title="Monster style tuning probe",
        subtitle=f"{len(rows)} controls × {len(style_ids)} styles · mode: {args.mode} · families: {', '.join(args.families)}",
        style_columns=style_columns,
        rows=rows,
    )

    print(f"\nGallery: {batch_root / 'index.html'}")
    if stopped_early:
        print("Stopped — run with --resume to continue.", file=sys.stderr)
        return 130
    if failures:
        print(f"Failed ({len(failures)}): {', '.join(failures[:5])}", file=sys.stderr)
        return 1
    print("Done.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
