"""Output path helpers for COE5 sprite probes."""
from __future__ import annotations

from pathlib import Path

TOOLS_DIR = Path(__file__).resolve().parent
GENERATED_DIR = TOOLS_DIR / "generated"
PROBE_STYLES_ROOT = GENERATED_DIR / "probes" / "styles"
BATCH_ROOT = GENERATED_DIR / "batch"


def find_existing_probe_image(output_dir: Path, prefix: str) -> Path | None:
    for ext in (".webp", ".png", ".jpg", ".jpeg"):
        exact = output_dir / f"{prefix}{ext}"
        if exact.is_file():
            return exact
        matches = sorted(output_dir.glob(f"{prefix}*{ext}"))
        if matches:
            return matches[-1]
    return None
