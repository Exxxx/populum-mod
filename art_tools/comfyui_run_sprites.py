#!/usr/bin/env python3
"""Scan mod files for missing sprites and run two-pass ComfyUI batch generation."""
from __future__ import annotations

import argparse
import sys
import uuid
from pathlib import Path

from c5m_sprite_scanner import build_jobs_payload, scan_c5m, scan_summary, write_scan_report
from coe5_probe_common import GracefulStop, StopController, probe_timestamp
from coe5_probe_paths import BATCH_ROOT
from coe5_probe_state import BatchRunState, delete_state, load_batch_state, save_batch_state
from coe5_sprite_jobs import (
    DEFAULT_JOBS_PATH,
    apply_job_filters,
    filter_jobs_for_phase,
    load_jobs_json,
    pass_for_job,
    save_jobs_json,
)
from coe5_sprite_background import add_bg_cli_args, chroma_config_from_args
from coe5_sprite_prompts import build_prompt_for_job, build_tuning_negative_prompt, generation_size_for_job, load_winners
from comfyui_client import (
    DEFAULT_COMFYUI_URL,
    WORKFLOW_EDIT,
    WORKFLOW_TXT2IMG,
    load_workflow,
    run_edit_generation,
    run_txt2img_generation,
)
from sprite_processor import process_and_export

TOOLS_DIR = Path(__file__).resolve().parent


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Scan and generate missing COE5 mod sprites via ComfyUI.")
    parser.add_argument("--scan", type=Path, default=None, help="Scan this .c5m mod file for missing sprites")
    parser.add_argument("--jobs", type=Path, default=None, help="Jobs JSON (default: generated/missing_sprites_jobs.json)")
    parser.add_argument("--write-jobs", type=Path, default=DEFAULT_JOBS_PATH)
    parser.add_argument("--url", default=DEFAULT_COMFYUI_URL)
    parser.add_argument("--workflow-txt2img", type=Path, default=WORKFLOW_TXT2IMG)
    parser.add_argument("--workflow-edit", type=Path, default=WORKFLOW_EDIT)
    parser.add_argument("--phase", choices=("spr1", "spr2"), default=None)
    parser.add_argument("--skip-spr2", action="store_true")
    parser.add_argument("--entity-type", choices=("monster", "item", "terrain"), default=None)
    parser.add_argument("--ids", nargs="+", default=None)
    parser.add_argument("--limit", type=int, default=None)
    parser.add_argument("--test", action="store_true", help="Run at most 2 jobs per pass")
    parser.add_argument("--seed", type=int, default=None)
    parser.add_argument("--poll", type=float, default=2.0)
    parser.add_argument("--timeout", type=float, default=900.0)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--resume", action="store_true")
    parser.add_argument("--force", action="store_true")
    parser.add_argument("--staging", action="store_true", help="Write finals to art_tools/generated/batch/final/")
    parser.add_argument("--strict", action="store_true", help="Treat zero-byte sprite files as missing when scanning")
    parser.add_argument("--report", type=Path, default=None, help="HTML report path for --scan")
    add_bg_cli_args(parser)
    return parser.parse_args()


def resolve_output_path(job: dict, *, staging: bool) -> Path:
    if staging:
        role = job.get("sprite_role", "spr1")
        ext = Path(job["target_path"]).suffix or ".tga"
        return BATCH_ROOT / "final" / f"{job['id']}_{role}{ext}"
    return Path(job["target_abs"])


def resolve_reference_path(job: dict, mod_root: Path) -> Path:
    ref = job.get("reference_abs")
    if ref:
        return Path(ref)
    rel = job.get("reference_path")
    if rel:
        return mod_root / rel.replace("/", "\\")
    paired = job.get("paired_spr2_path")
    spr1_path = Path(job["target_path"])
    if job.get("sprite_role") == "spr2" and paired:
        guess = spr1_path.parent / spr1_path.name.replace("02", "01")
        return mod_root / str(guess).replace("/", "\\")
    raise ValueError(f"Job {job.get('id')} missing reference_path for spr2")


def validate_spr2_prerequisites(jobs: list[dict], mod_root: Path) -> list[str]:
    missing_refs: list[str] = []
    for job in jobs:
        if pass_for_job(job) != "spr2":
            continue
        try:
            ref = resolve_reference_path(job, mod_root)
        except ValueError as exc:
            missing_refs.append(str(exc))
            continue
        if not ref.is_file():
            missing_refs.append(f"{job['id']}: reference missing {ref}")
    return missing_refs


def run_pass(
    *,
    pass_name: str,
    jobs: list[dict],
    args: argparse.Namespace,
    state: BatchRunState | None,
    mod_root: Path,
    winners: dict,
    txt2img_template: dict | None,
    edit_template: dict | None,
    stop_controller: StopController | None,
) -> tuple[int, int, bool]:
    client_id = str(uuid.uuid4())
    completed = 0
    failed = 0
    stopped_early = False
    skip_ids = set(state.completed) if state else set()

    print(f"\n=== Pass: {pass_name} ({len(jobs)} jobs) ===")

    for index, job in enumerate(jobs, start=1):
        if stop_controller:
            try:
                stop_controller.check()
            except GracefulStop:
                stopped_early = True
                break

        job_id = job["id"]
        if job_id in skip_ids and not args.force:
            print(f"[{index}/{len(jobs)}] skip (completed): {job_id}")
            completed += 1
            continue

        dest = resolve_output_path(job, staging=args.staging)
        if dest.is_file() and not args.force:
            print(f"[{index}/{len(jobs)}] skip (exists): {dest}")
            if state:
                state.mark_ok(job_id)
                save_batch_state(state)
            completed += 1
            continue

        prompt = build_prompt_for_job(job, winners, bg_mode=args.bg_mode)
        role = pass_for_job(job)
        print(f"[{index}/{len(jobs)}] {job_id} -> {dest.name}")
        print(f"  prompt: {prompt[:120]}...")

        if args.dry_run:
            continue

        inter_dir = BATCH_ROOT / "intermediate"
        inter_dir.mkdir(parents=True, exist_ok=True)
        inter_path = inter_dir / f"{job_id}.png"

        try:
            if role == "spr2":
                ref_path = resolve_reference_path(job, mod_root)
                if not ref_path.is_file():
                    raise FileNotFoundError(f"spr2 reference missing: {ref_path}")
                saved = run_edit_generation(
                    base_url=args.url,
                    workflow_template=edit_template,
                    client_id=client_id,
                    prompt=prompt,
                    reference_path=ref_path,
                    output_dir=inter_dir,
                    output_name=job_id,
                    seed=args.seed,
                    poll_seconds=args.poll,
                    timeout_seconds=args.timeout,
                )
            else:
                width, height = generation_size_for_job(job)
                saved = run_txt2img_generation(
                    base_url=args.url,
                    workflow_template=txt2img_template,
                    client_id=client_id,
                    prompt=prompt,
                    filename_prefix=job_id,
                    output_dir=inter_dir,
                    width=width,
                    height=height,
                    seed=args.seed,
                    poll_seconds=args.poll,
                    timeout_seconds=args.timeout,
                )
                if saved and saved.suffix.lower() == ".webp":
                    inter_path = saved

            if saved is None:
                raise RuntimeError("ComfyUI returned no output image")
            if saved != inter_path and saved.is_file():
                inter_path = saved

            entity_type = job.get("entity_type", "monster")
            canvas = int(job.get("canvas", 64))
            export_bg_mode = "black" if role == "spr2" else args.bg_mode
            chroma_config = chroma_config_from_args(args)
            debug_mask = None
            if args.debug_mask and export_bg_mode != "black":
                debug_mask = dest.with_name(f"{dest.stem}_keymask.png")
            process_and_export(
                inter_path,
                dest,
                entity_type=entity_type,
                canvas=canvas,
                bg_mode=export_bg_mode,
                chroma_config=chroma_config,
                debug_mask_path=debug_mask,
            )
            print(f"  wrote {dest}")
            if state:
                state.mark_ok(job_id)
                save_batch_state(state)
            completed += 1
        except (OSError, TimeoutError, RuntimeError, ValueError) as exc:
            print(f"  ERROR: {exc}")
            if state:
                state.mark_failed(job_id)
                save_batch_state(state)
            failed += 1

    return completed, failed, stopped_early


def main() -> int:
    args = parse_args()

    if args.scan:
        result = scan_c5m(args.scan, strict=args.strict)
        payload = build_jobs_payload(result)
        counts = scan_summary(result)
        print(f"Scanned: {result.mod_file}")
        print(
            f"Missing: {counts['total']} "
            f"(spr1={counts['spr1']} spr2={counts['spr2']} item={counts['item']} terrain={counts['terrain']})"
        )
        if not args.dry_run:
            save_jobs_json(args.write_jobs, payload)
            print(f"Wrote jobs: {args.write_jobs}")
        report_path = args.report or args.write_jobs.with_name("missing_sprites_report.html")
        if not args.dry_run:
            write_scan_report(result, report_path)
            print(f"Report: {report_path}")
        if args.dry_run:
            for job in result.jobs[:10]:
                print(f"  [{job['sprite_role']}] {job['target_path']}")
        return 0

    jobs_path = args.jobs or DEFAULT_JOBS_PATH
    if not jobs_path.is_file():
        print(f"Jobs file not found: {jobs_path}\nRun with --scan populum/populum.c5m first.", file=sys.stderr)
        return 2

    payload = load_jobs_json(jobs_path)
    jobs = payload.get("jobs", [])
    mod_root = Path(payload.get("mod_root", "."))

    jobs = apply_job_filters(jobs, ids=args.ids, entity_type=args.entity_type, limit=args.limit)
    if args.test:
        spr1_jobs = filter_jobs_for_phase(jobs, "spr1")[:2]
        spr2_jobs = filter_jobs_for_phase(jobs, "spr2")[:2]
        jobs = spr1_jobs + spr2_jobs

    phase = None
    if args.skip_spr2 or args.phase == "spr1":
        phase = "spr1"
    elif args.phase == "spr2":
        phase = "spr2"

    pass1_jobs = filter_jobs_for_phase(jobs, "spr1") if phase in (None, "spr1") else []
    pass2_jobs = filter_jobs_for_phase(jobs, "spr2") if phase in (None, "spr2") and not args.skip_spr2 else []

    if pass2_jobs:
        missing_refs = validate_spr2_prerequisites(pass2_jobs, mod_root)
        if missing_refs and phase == "spr2":
            print("Cannot run spr2 pass — missing references:", file=sys.stderr)
            for line in missing_refs[:20]:
                print(f"  {line}", file=sys.stderr)
            return 1

    state_path = jobs_path.with_name("batch_state.json")
    state: BatchRunState | None = None
    if not args.dry_run:
        existing = load_batch_state(state_path)
        if existing and not args.resume:
            print(f"Batch state exists: {state_path}\nUse --resume or delete state.", file=sys.stderr)
            return 2
        state = existing or BatchRunState(
            jobs_path=str(jobs_path.resolve()),
            status="running",
            phase=phase,
            dry_run=False,
        )
        state.status = "running"
        save_batch_state(state)

    winners = load_winners()
    txt2img_template = None if args.dry_run else load_workflow(args.workflow_txt2img)
    edit_template = None if args.dry_run else load_workflow(args.workflow_edit)

    stop_controller = StopController()
    if not args.dry_run:
        stop_controller.install()

    total_failed = 0
    stopped_early = False
    try:
        if pass1_jobs:
            _, failed, stopped = run_pass(
                pass_name="spr1 (Qwen Image 2512)",
                jobs=pass1_jobs,
                args=args,
                state=state,
                mod_root=mod_root,
                winners=winners,
                txt2img_template=txt2img_template,
                edit_template=edit_template,
                stop_controller=stop_controller,
            )
            total_failed += failed
            stopped_early = stopped_early or stopped

        if pass2_jobs and not stopped_early:
            if phase is None:
                missing_refs = validate_spr2_prerequisites(pass2_jobs, mod_root)
                if missing_refs:
                    print("\nSkipping spr2 pass — unresolved references:", file=sys.stderr)
                    for line in missing_refs[:10]:
                        print(f"  {line}", file=sys.stderr)
                else:
                    _, failed, stopped = run_pass(
                        pass_name="spr2 (Qwen Image Edit 2509)",
                        jobs=pass2_jobs,
                        args=args,
                        state=state,
                        mod_root=mod_root,
                        winners=winners,
                        txt2img_template=txt2img_template,
                        edit_template=edit_template,
                        stop_controller=stop_controller,
                    )
                    total_failed += failed
                    stopped_early = stopped_early or stopped
            else:
                _, failed, stopped = run_pass(
                    pass_name="spr2 (Qwen Image Edit 2509)",
                    jobs=pass2_jobs,
                    args=args,
                    state=state,
                    mod_root=mod_root,
                    winners=winners,
                    txt2img_template=txt2img_template,
                    edit_template=edit_template,
                    stop_controller=stop_controller,
                )
                total_failed += failed
                stopped_early = stopped_early or stopped
    finally:
        if not args.dry_run:
            stop_controller.restore()
            if state:
                state.status = "stopped" if stopped_early else ("completed" if not total_failed else "completed_with_errors")
                save_batch_state(state)

    if stopped_early:
        print("\nStopped — run with --resume to continue.", file=sys.stderr)
        return 130
    if total_failed:
        print(f"\nFinished with {total_failed} failure(s)", file=sys.stderr)
        return 1
    print(f"\nDone at {probe_timestamp()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
