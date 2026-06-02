"""Tiled HTML comparison gallery for COE5 sprite probes."""
from __future__ import annotations

import html
import json
from pathlib import Path


def write_tiled_comparison_html(
    path: Path,
    *,
    title: str,
    subtitle: str,
    style_columns: list[dict],
    rows: list[dict],
    cell_display_px: int = 128,
) -> None:
    """Write grid: rows = monsters, columns = control + style variants.

    style_columns: [{"id": "control", "label": "Control"}, {"id": "style_id", "label": "..."}, ...]
    rows: [{
        "sprite_number": 1018,
        "label": "Knight",
        "cells": {
            "control": {"image": "rel/path.png", "prompt": "...", "status": "ok"},
            "style_id": {...},
        }
    }]
    """
    headers = "".join(f"<th>{html.escape(col['label'])}</th>" for col in style_columns)

    body_rows = []
    for row in rows:
        label = html.escape(row.get("label", ""))
        sn = row.get("sprite_number", "?")
        cells = row.get("cells", {})
        tds = []
        for col in style_columns:
            cid = col["id"]
            cell = cells.get(cid, {})
            img_path = cell.get("image")
            prompt = cell.get("prompt", "")
            status = cell.get("status", "")
            if img_path:
                img_tag = (
                    f'<img src="{html.escape(img_path)}" alt="{html.escape(cid)}" '
                    f'width="{cell_display_px}" height="{cell_display_px}">'
                )
            else:
                img_tag = f'<em>{html.escape(status or "missing")}</em>'
            prompt_block = (
                f'<details><summary>prompt</summary>'
                f'<code>{html.escape(prompt)}</code></details>'
                if prompt
                else ""
            )
            tds.append(
                f"<td><div class=\"cell\">{img_tag}{prompt_block}</div></td>"
            )
        body_rows.append(
            f"<tr><th class=\"rowhead\">#{sn}<br>{label}</th>{''.join(tds)}</tr>"
        )

    doc = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>{html.escape(title)}</title>
  <style>
    body {{ font-family: sans-serif; margin: 1.5rem; }}
    h1 {{ margin-bottom: 0.25rem; }}
    .subtitle {{ color: #555; margin-bottom: 1.5rem; }}
    table {{ border-collapse: collapse; }}
    th, td {{ border: 1px solid #ccc; padding: 0.5rem; vertical-align: top; }}
    th.rowhead {{ text-align: left; min-width: 6rem; background: #f7f7f7; }}
    thead th {{ background: #eee; position: sticky; top: 0; }}
    img {{ image-rendering: pixelated; image-rendering: crisp-edges; background: #111; }}
    .cell {{ display: flex; flex-direction: column; align-items: center; gap: 0.35rem; }}
    code {{ display: block; white-space: pre-wrap; font-size: 0.75rem; max-width: {cell_display_px + 40}px; color: #333; }}
    details summary {{ cursor: pointer; font-size: 0.8rem; color: #666; }}
  </style>
</head>
<body>
  <h1>{html.escape(title)}</h1>
  <p class="subtitle">{html.escape(subtitle)}</p>
  <table>
    <thead><tr><th>Monster</th>{headers}</tr></thead>
    <tbody>
      {''.join(body_rows)}
    </tbody>
  </table>
</body>
</html>
"""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(doc, encoding="utf-8")


def write_tiled_manifest(path: Path, payload: dict) -> None:
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
