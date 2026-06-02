"""Chroma-key background config for sprite generation and post-processing."""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Literal

from PIL import Image

BgMode = Literal["chroma", "black", "auto"]

DEFAULT_BG_MODE: BgMode = "chroma"
GREEN_KEY_RGB: tuple[int, int, int] = (0, 255, 0)
MAGENTA_KEY_RGB: tuple[int, int, int] = (255, 0, 255)
DEFAULT_KEY_RGB = GREEN_KEY_RGB
DEFAULT_KEY_TOLERANCE = 40
DEFAULT_SPILL_SUPPRESS = 8

CHROMA_BG_PROMPT = (
    "solid flat vivid green background, uniform #00FF00, no scenery, no gradient"
)
BLACK_BG_PROMPT = (
    "solid pure black background filling entire canvas, no scenery, no gradient"
)


@dataclass(frozen=True)
class ChromaKeyConfig:
    rgb: tuple[int, int, int] = DEFAULT_KEY_RGB
    tolerance: int = DEFAULT_KEY_TOLERANCE
    spill_suppress: int = DEFAULT_SPILL_SUPPRESS
    sample_border: bool = True

    @classmethod
    def from_hex(cls, hex_color: str, *, tolerance: int = DEFAULT_KEY_TOLERANCE) -> ChromaKeyConfig:
        text = hex_color.strip().lstrip("#")
        if len(text) != 6:
            raise ValueError(f"key color must be 6 hex digits, got {hex_color!r}")
        rgb = tuple(int(text[i : i + 2], 16) for i in (0, 2, 4))
        return cls(rgb=rgb, tolerance=tolerance)


def parse_bg_mode(value: str) -> BgMode:
    mode = value.strip().lower()
    if mode not in ("chroma", "black", "auto"):
        raise ValueError(f"bg mode must be chroma, black, or auto (got {value!r})")
    return mode  # type: ignore[return-value]


def prompt_background_phrase(mode: BgMode = DEFAULT_BG_MODE) -> str:
    if mode == "black":
        return BLACK_BG_PROMPT
    return CHROMA_BG_PROMPT


def tuning_negative_extras(mode: BgMode = DEFAULT_BG_MODE) -> str:
    base = (
        "background scenery, landscape, sky, clouds, mountains, forest, trees, grass, ground plane, "
        "floor, horizon, environment, outdoor scene, indoor scene, gradient background, vignette, "
        "grey background, textured background, purple background, violet background, lavender background, "
        "multiple characters, two figures, duplicate character, tiny duplicate, scale reference, "
        "size comparison, crowd, group, collage, split screen, character sheet, "
        "border frame, rounded corners, UI chrome, photorealistic, hyperdetailed, 8k, cinematic lighting, "
        "smooth rendering, high resolution illustration, detailed painting, fine texture, anti-aliased"
    )
    if mode == "black":
        return f"{base}, colored background, blue background, magenta background, pink background, green background"
    return f"{base}, blue background, black background, magenta background"


def _border_pixels(img: Image.Image) -> list[tuple[int, int, int]]:
    rgba = img.convert("RGBA")
    width, height = rgba.size
    px = rgba.load()
    samples: list[tuple[int, int, int]] = []
    for x in range(width):
        samples.append(px[x, 0][:3])
        samples.append(px[x, height - 1][:3])
    for y in range(1, height - 1):
        samples.append(px[0, y][:3])
        samples.append(px[width - 1, y][:3])
    return samples


def _median_channel(values: list[int]) -> int:
    ordered = sorted(values)
    return ordered[len(ordered) // 2]


def detect_key_color_from_border(img: Image.Image) -> tuple[int, int, int]:
    samples = _border_pixels(img)
    if not samples:
        return DEFAULT_KEY_RGB
    rs = [s[0] for s in samples]
    gs = [s[1] for s in samples]
    bs = [s[2] for s in samples]
    return (_median_channel(rs), _median_channel(gs), _median_channel(bs))


def _color_distance(a: tuple[int, int, int], b: tuple[int, int, int]) -> int:
    return max(abs(a[0] - b[0]), abs(a[1] - b[1]), abs(a[2] - b[2]))


def _is_near_black_rgb(r: int, g: int, b: int, *, threshold: int = 40) -> bool:
    return max(r, g, b) <= threshold


def _is_purple_heavy_rgb(r: int, g: int, b: int) -> bool:
    return r >= 70 and b >= 70 and g <= min(r, b) * 0.55


def control_is_purple_heavy(control_path: Path | str) -> bool:
    """True when control art uses substantial purple/magenta (prefer green chroma key)."""
    path = Path(control_path)
    if not path.is_file():
        return False
    with Image.open(path) as img:
        rgba = img.convert("RGBA")
        px = rgba.load()
        width, height = rgba.size
        purple = 0
        total = 0
        for y in range(height):
            for x in range(width):
                r, g, b, a = px[x, y]
                if a < 16 or _is_near_black_rgb(r, g, b):
                    continue
                total += 1
                if _is_purple_heavy_rgb(r, g, b):
                    purple += 1
        if total < 8:
            return False
        return purple / total >= 0.12


def border_matches_key(
    img: Image.Image,
    config: ChromaKeyConfig,
    *,
    match_ratio: float = 0.55,
) -> bool:
    samples = _border_pixels(img)
    if not samples:
        return False
    hits = sum(1 for rgb in samples if _color_distance(rgb, config.rgb) <= config.tolerance)
    return hits / len(samples) >= match_ratio


def resolve_bg_mode(img: Image.Image, mode: BgMode, config: ChromaKeyConfig) -> BgMode:
    if mode != "auto":
        return mode
    if border_matches_key(img, config):
        return "chroma"
    return "black"


def chroma_config_from_args(args: object) -> ChromaKeyConfig:
    tolerance = int(getattr(args, "key_tolerance", DEFAULT_KEY_TOLERANCE))
    hex_color = getattr(args, "key_color", None)
    if hex_color:
        return ChromaKeyConfig.from_hex(str(hex_color), tolerance=tolerance)
    return ChromaKeyConfig(tolerance=tolerance)


def chroma_config_for_probe(args: object, control_path: Path | str | None = None) -> ChromaKeyConfig:
    config = chroma_config_from_args(args)
    if getattr(args, "key_color", None):
        return config
    if control_path and control_is_purple_heavy(control_path):
        return ChromaKeyConfig(rgb=GREEN_KEY_RGB, tolerance=config.tolerance)
    return config


def add_bg_cli_args(parser) -> None:
    parser.add_argument(
        "--bg-mode",
        choices=("chroma", "black", "auto"),
        default=DEFAULT_BG_MODE,
        help="Generation background and post-process keying mode (default: chroma)",
    )
    parser.add_argument(
        "--key-color",
        default=None,
        metavar="RRGGBB",
        help="Chroma key color hex (default: 00FF00 green)",
    )
    parser.add_argument(
        "--key-tolerance",
        type=int,
        default=DEFAULT_KEY_TOLERANCE,
        help="Per-channel tolerance for chroma key removal (default: 40)",
    )
    parser.add_argument(
        "--debug-mask",
        action="store_true",
        help="Save chroma key mask PNG alongside processed sprites",
    )
