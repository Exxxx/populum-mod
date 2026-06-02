"""Post-process generated sprites into CoE5-ready TGA/PNG assets."""
from __future__ import annotations

from collections import deque
from pathlib import Path

from PIL import Image

from coe5_sprite_background import (
    BgMode,
    ChromaKeyConfig,
    DEFAULT_BG_MODE,
    DEFAULT_KEY_RGB,
    detect_key_color_from_border,
    resolve_bg_mode,
)


def _is_near_black(r: int, g: int, b: int, *, threshold: int = 40) -> bool:
    return max(r, g, b) <= threshold


def _is_magenta_purple_spill(r: int, g: int, b: int) -> bool:
    """Stray magenta/violet backgrounds from confused chroma or purple prompts."""
    return r >= 70 and b >= 70 and g <= min(r, b) * 0.55


def _color_close(a: tuple[int, int, int], b: tuple[int, int, int], tolerance: int) -> bool:
    return max(abs(a[0] - b[0]), abs(a[1] - b[1]), abs(a[2] - b[2])) <= tolerance


def _border_seeds(width: int, height: int) -> list[tuple[int, int]]:
    seeds: list[tuple[int, int]] = []
    for x in range(width):
        seeds.append((x, 0))
        seeds.append((x, height - 1))
    for y in range(1, height - 1):
        seeds.append((0, y))
        seeds.append((width - 1, y))
    return seeds


def _pixel_matches_key(
    r: int,
    g: int,
    b: int,
    a: int,
    *,
    key_rgb: tuple[int, int, int],
    tolerance: int,
    black_fallback: bool,
    chroma_spill: bool = False,
) -> bool:
    if a < 16:
        return True
    if _color_close((r, g, b), key_rgb, tolerance):
        return True
    if chroma_spill and _is_magenta_purple_spill(r, g, b):
        return True
    if black_fallback and _is_near_black(r, g, b):
        return True
    return False


def _flood_key_mask(
    rgba: Image.Image,
    *,
    key_rgb: tuple[int, int, int],
    tolerance: int,
    black_fallback: bool = False,
    chroma_spill: bool = False,
) -> list[list[bool]]:
    """Mark edge-connected pixels matching the key color (and optional near-black)."""
    width, height = rgba.size
    px = rgba.load()
    visited = [[False] * width for _ in range(height)]
    background = [[False] * width for _ in range(height)]

    for sx, sy in _border_seeds(width, height):
        if visited[sx][sy]:
            continue
        r, g, b, a = px[sx, sy]
        if not _pixel_matches_key(
            r, g, b, a, key_rgb=key_rgb, tolerance=tolerance, black_fallback=black_fallback, chroma_spill=chroma_spill
        ):
            continue

        queue: deque[tuple[int, int]] = deque([(sx, sy)])
        visited[sx][sy] = True
        background[sx][sy] = True
        while queue:
            x, y = queue.popleft()
            for nx, ny in ((x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)):
                if nx < 0 or ny < 0 or nx >= width or ny >= height or visited[nx][ny]:
                    continue
                nr, ng, nb, na = px[nx, ny]
                if _pixel_matches_key(
                    nr, ng, nb, na, key_rgb=key_rgb, tolerance=tolerance, black_fallback=black_fallback, chroma_spill=chroma_spill
                ):
                    visited[nx][ny] = True
                    background[nx][ny] = True
                    queue.append((nx, ny))
    return background


def _largest_foreground_mask(
    rgba: Image.Image,
    background: list[list[bool]],
    *,
    key_rgb: tuple[int, int, int],
    tolerance: int,
) -> list[list[bool]] | None:
    width, height = rgba.size
    px = rgba.load()
    visited = [[False] * width for _ in range(height)]
    best: list[tuple[int, int]] = []

    def is_foreground(x: int, y: int) -> bool:
        if background[x][y]:
            return False
        r, g, b, a = px[x, y]
        if a < 16:
            return False
        return True

    for sx in range(width):
        for sy in range(height):
            if visited[sx][sy] or not is_foreground(sx, sy):
                visited[sx][sy] = True
                continue

            component: list[tuple[int, int]] = []
            queue: deque[tuple[int, int]] = deque([(sx, sy)])
            visited[sx][sy] = True
            while queue:
                x, y = queue.popleft()
                component.append((x, y))
                for nx, ny in ((x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)):
                    if nx < 0 or ny < 0 or nx >= width or ny >= height or visited[nx][ny]:
                        continue
                    if not is_foreground(nx, ny):
                        visited[nx][ny] = True
                        continue
                    visited[nx][ny] = True
                    queue.append((nx, ny))

            if len(component) > len(best):
                best = component

    if not best:
        return None

    keep = [[False] * width for _ in range(height)]
    for x, y in best:
        keep[x][y] = True
    return keep


def _apply_background_removal(
    rgba: Image.Image,
    background: list[list[bool]],
    keep: list[list[bool]] | None,
    *,
    key_rgb: tuple[int, int, int],
    tolerance: int,
    to_black: bool,
) -> Image.Image:
    width, height = rgba.size
    px = rgba.load()
    transparent = (0, 0, 0, 0)
    black_opaque = (0, 0, 0, 255)

    for x in range(width):
        for y in range(height):
            remove = background[x][y]
            if not remove and keep is not None and not keep[x][y]:
                remove = True
            if remove:
                px[x, y] = black_opaque if to_black else transparent
    return rgba


def chroma_key_background(
    img: Image.Image,
    config: ChromaKeyConfig | None = None,
    *,
    to_black: bool = False,
) -> tuple[Image.Image, list[list[bool]]]:
    """Remove chroma-key background; return RGBA and the key mask."""
    config = config or ChromaKeyConfig()
    rgba = img.convert("RGBA")
    key_rgb = detect_key_color_from_border(rgba) if config.sample_border else config.rgb
    background = _flood_key_mask(
        rgba,
        key_rgb=key_rgb,
        tolerance=config.tolerance,
        black_fallback=False,
    )
    keep = _largest_foreground_mask(rgba, background, key_rgb=key_rgb, tolerance=config.tolerance)
    cleaned = _apply_background_removal(
        rgba,
        background,
        keep,
        key_rgb=key_rgb,
        tolerance=config.tolerance,
        to_black=to_black,
    )
    return cleaned, background


def flatten_sprite_background(img: Image.Image) -> Image.Image:
    """Remove generated scenery/halos; strip black or stray magenta/violet backgrounds."""
    rgba = img.convert("RGBA")
    border_rgb = detect_key_color_from_border(rgba)
    if _is_magenta_purple_spill(*border_rgb):
        key_rgb = border_rgb
        tolerance = 48
        black_fallback = False
    else:
        key_rgb = (0, 0, 0)
        tolerance = 52
        black_fallback = True

    background = _flood_key_mask(
        rgba,
        key_rgb=key_rgb,
        tolerance=tolerance,
        black_fallback=black_fallback,
        chroma_spill=True,
    )
    keep = _largest_foreground_mask(rgba, background, key_rgb=key_rgb, tolerance=tolerance)
    return _apply_background_removal(
        rgba,
        background,
        keep,
        key_rgb=key_rgb,
        tolerance=tolerance,
        to_black=True,
    )


def remove_background(
    img: Image.Image,
    *,
    mode: BgMode = DEFAULT_BG_MODE,
    config: ChromaKeyConfig | None = None,
) -> Image.Image:
    config = config or ChromaKeyConfig()
    resolved = resolve_bg_mode(img, mode, config)
    if resolved == "chroma":
        cleaned, _ = chroma_key_background(img, config, to_black=False)
        return cleaned
    return flatten_sprite_background(img)


def save_key_mask(mask: list[list[bool]], dest: Path) -> Path:
    height = len(mask)
    width = len(mask[0]) if height else 0
    out = Image.new("RGBA", (width, height), (0, 0, 0, 255))
    px = out.load()
    for y in range(height):
        for x in range(width):
            if mask[x][y]:
                px[x, y] = (255, 0, 255, 255)
    dest.parent.mkdir(parents=True, exist_ok=True)
    out.save(dest, format="PNG")
    return dest


def _alpha_bbox(img: Image.Image) -> tuple[int, int, int, int] | None:
    rgba = img.convert("RGBA")
    alpha = rgba.split()[3]
    return alpha.getbbox()


def _content_bbox(
    img: Image.Image,
    *,
    key_rgb: tuple[int, int, int] = DEFAULT_KEY_RGB,
    key_tolerance: int = 40,
) -> tuple[int, int, int, int] | None:
    rgba = img.convert("RGBA")
    px = rgba.load()
    width, height = rgba.size
    min_x, min_y = width, height
    max_x, max_y = -1, -1
    for y in range(height):
        for x in range(width):
            r, g, b, a = px[x, y]
            if a < 16:
                continue
            if _color_close((r, g, b), key_rgb, key_tolerance):
                continue
            if r < 8 and g < 8 and b < 8:
                continue
            min_x = min(min_x, x)
            min_y = min(min_y, y)
            max_x = max(max_x, x)
            max_y = max(max_y, y)
    if max_x < min_x or max_y < min_y:
        return None
    return min_x, min_y, max_x + 1, max_y + 1


def bounding_box(img: Image.Image, *, key_rgb: tuple[int, int, int] = DEFAULT_KEY_RGB) -> tuple[int, int, int, int] | None:
    return _content_bbox(img, key_rgb=key_rgb) or _alpha_bbox(img)


def framing_score(img: Image.Image) -> float:
    box = bounding_box(img)
    if box is None:
        return 0.0
    _, _, _, bottom = box
    height = img.height
    foot_gap = height - bottom
    target_gap = 2
    gap_score = max(0.0, 1.0 - abs(foot_gap - target_gap) / max(height * 0.25, 1))
    fill_ratio = ((box[2] - box[0]) * (box[3] - box[1])) / max(img.width * img.height, 1)
    size_score = 1.0 - abs(fill_ratio - 0.55)
    return max(0.0, min(1.0, (gap_score + size_score) / 2))


def _fit_on_canvas(
    img: Image.Image,
    canvas: int,
    *,
    max_content: int | None = None,
    foot_padding_px: int = 2,
    bottom_align: bool = False,
    resample: Image.Resampling = Image.Resampling.LANCZOS,
) -> Image.Image:
    rgba = img.convert("RGBA")
    box = bounding_box(rgba)
    if box is None:
        out = Image.new("RGBA", (canvas, canvas), (0, 0, 0, 0))
        return out

    cropped = rgba.crop(box)
    cw, ch = cropped.size
    limit = max_content or int(canvas * 0.9)
    scale = min(limit / max(cw, 1), limit / max(ch, 1), 1.0)
    new_w = max(1, int(cw * scale))
    new_h = max(1, int(ch * scale))
    resized = cropped.resize((new_w, new_h), resample)

    out = Image.new("RGBA", (canvas, canvas), (0, 0, 0, 255))
    x = (canvas - new_w) // 2
    if bottom_align:
        y = canvas - new_h - foot_padding_px
        y = max(0, y)
    else:
        y = (canvas - new_h) // 2
    out.paste(resized, (x, y), resized)
    return out


def process_monster_sprite(
    img: Image.Image,
    canvas: int,
    *,
    bg_mode: BgMode = DEFAULT_BG_MODE,
    chroma_config: ChromaKeyConfig | None = None,
    debug_mask_path: Path | None = None,
) -> Image.Image:
    config = chroma_config or ChromaKeyConfig()
    resolved = resolve_bg_mode(img, bg_mode, config)
    if resolved == "chroma":
        cleaned, mask = chroma_key_background(img, config, to_black=False)
        if debug_mask_path is not None:
            save_key_mask(mask, debug_mask_path)
    else:
        cleaned = flatten_sprite_background(img)
    return _fit_on_canvas(cleaned, canvas, foot_padding_px=2, bottom_align=True, resample=Image.Resampling.NEAREST)


def process_item_sprite(
    img: Image.Image,
    canvas: int,
    *,
    bg_mode: BgMode = DEFAULT_BG_MODE,
    chroma_config: ChromaKeyConfig | None = None,
) -> Image.Image:
    cleaned = remove_background(img, mode=bg_mode, config=chroma_config)
    return _fit_on_canvas(cleaned, canvas, max_content=40, bottom_align=False)


def process_terrain_sprite(img: Image.Image, canvas: int | None = None) -> Image.Image:
    if canvas is None:
        return img.convert("RGBA")
    return img.convert("RGBA").resize((canvas, canvas), Image.Resampling.LANCZOS)


def export_sprite(
    img: Image.Image,
    dest: Path,
    *,
    entity_type: str = "monster",
    canvas: int = 64,
    bg_mode: BgMode = DEFAULT_BG_MODE,
    chroma_config: ChromaKeyConfig | None = None,
    debug_mask_path: Path | None = None,
) -> Path:
    if entity_type == "item":
        processed = process_item_sprite(img, canvas, bg_mode=bg_mode, chroma_config=chroma_config)
    elif entity_type == "terrain":
        processed = process_terrain_sprite(img, canvas if canvas != 64 else None)
    else:
        processed = process_monster_sprite(
            img,
            canvas,
            bg_mode=bg_mode,
            chroma_config=chroma_config,
            debug_mask_path=debug_mask_path,
        )

    dest.parent.mkdir(parents=True, exist_ok=True)
    suffix = dest.suffix.lower()
    if suffix == ".png":
        processed.save(dest, format="PNG")
    else:
        processed.save(dest, format="TGA")
    return dest


def process_and_export(
    source: Path,
    dest: Path,
    *,
    entity_type: str,
    canvas: int,
    bg_mode: BgMode = DEFAULT_BG_MODE,
    chroma_config: ChromaKeyConfig | None = None,
    debug_mask_path: Path | None = None,
) -> tuple[Path, float]:
    img = Image.open(source)
    score = framing_score(img)
    export_sprite(
        img,
        dest,
        entity_type=entity_type,
        canvas=canvas,
        bg_mode=bg_mode,
        chroma_config=chroma_config,
        debug_mask_path=debug_mask_path,
    )
    return dest, score
