"""Canvas and ComfyUI latent size rules for COE5 sprites."""
from __future__ import annotations

from pathlib import Path

from PIL import Image

TINY_THRESHOLD = 36
HUGE_THRESHOLD = 96


def detect_canvas_from_control(image_path: Path | str, *, huge: bool = False) -> int:
    if huge:
        return 128
    path = Path(image_path)
    if not path.is_file():
        return 64
    with Image.open(path) as img:
        width, height = img.size
    longest = max(width, height)
    if longest <= TINY_THRESHOLD:
        return 32
    if longest >= HUGE_THRESHOLD:
        return 128
    return 64


def canvas_for_monster(*, huge: bool = False, control_path: Path | str | None = None) -> int:
    if control_path:
        return detect_canvas_from_control(control_path, huge=huge)
    return 128 if huge else 64


def generation_size_for_canvas(canvas: int, *, entity_type: str = "monster") -> tuple[int, int]:
    if entity_type == "terrain":
        return 1328, 1328
    if canvas <= 32:
        return 384, 384
    if canvas >= 128:
        return 512, 512
    return 512, 512


def generation_size_for_job(job: dict) -> tuple[int, int]:
    entity_type = job.get("entity_type", "monster")
    canvas = int(job.get("canvas", 64))
    return generation_size_for_canvas(canvas, entity_type=entity_type)
