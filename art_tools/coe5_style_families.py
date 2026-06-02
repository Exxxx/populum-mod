"""Style families for COE5 sprite tuning (fidelity vs original)."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

StyleFamily = Literal["fidelity", "original", "legacy"]

DEFAULT_FIDELITY_STYLE_ID = "coe5_fidelity_painted"
DEFAULT_ORIGINAL_STYLE_ID = "original_watercolor"

# Background is injected at prompt-build time from coe5_sprite_background (not baked in here).
_SINGLE = "exactly one character, simple low-detail silhouette, chunky pixel shapes"


@dataclass(frozen=True)
class StyleRecipe:
    id: str
    label: str
    style: str
    family: StyleFamily = "legacy"
    notes: str = ""


FIDELITY_CATALOG: list[StyleRecipe] = [
    StyleRecipe(
        "coe5_fidelity_painted",
        "Fidelity painted pixel",
        "1990s fantasy strategy RPG unit sprite, early 2000s painted pixel art, "
        f"soft dithered shading on chunky pixel forms, top-down oblique view, {_SINGLE}",
        family="fidelity",
        notes="Primary reproduction target",
    ),
    StyleRecipe(
        "coe5_fidelity_pixel",
        "Fidelity 16-bit pixel",
        "16-bit fantasy RPG battle sprite, limited palette, hard pixel edges, no anti-aliasing, "
        f"top-down oblique view, {_SINGLE}, crisp silhouette",
        family="fidelity",
    ),
    StyleRecipe(
        "coe5_fidelity_classic",
        "Fidelity classic pixel",
        "classic retro fantasy unit sprite, restrained palette, painterly pixel-era token, "
        f"top-down oblique view, {_SINGLE}, readable at 64 pixels",
        family="fidelity",
    ),
    StyleRecipe(
        "coe5_fidelity_restrained",
        "Fidelity restrained",
        "retro fantasy battle unit sprite, muted cohesive palette, simplified blocky forms, "
        f"top-down oblique view, {_SINGLE}, minimal detail",
        family="fidelity",
    ),
]

ORIGINAL_CATALOG: list[StyleRecipe] = [
    StyleRecipe(
        "original_watercolor",
        "Original watercolor",
        "tiny fantasy unit sprite as simple watercolor mark, soft edges, blocky shapes, "
        f"top-down oblique view, {_SINGLE}, readable silhouette",
        family="original",
    ),
    StyleRecipe(
        "original_ink_wash",
        "Original ink wash",
        "tiny fantasy unit sprite in bold ink wash, simple brush strokes, "
        f"top-down oblique view, {_SINGLE}, strong silhouette",
        family="original",
    ),
    StyleRecipe(
        "original_lowpoly",
        "Original low-poly",
        "tiny fantasy unit sprite as simple low-poly render, flat shaded facets, "
        f"top-down oblique view, {_SINGLE}, clean geometric forms",
        family="original",
    ),
    StyleRecipe(
        "original_grimdark",
        "Original grimdark",
        "dark fantasy unit sprite, high contrast, simple gritty texture, "
        f"top-down oblique view, {_SINGLE}, ominous silhouette",
        family="original",
    ),
]

LEGACY_CATALOG: list[StyleRecipe] = [
    StyleRecipe(
        "coe5_classic_pixel",
        "Classic 16-bit battle sprite",
        "SNES-era 16-bit fantasy battle sprite, limited palette, hard pixel edges, "
        f"top-down oblique view, {_SINGLE}, restrained color count",
        family="legacy",
        notes="SNES-era unit sprite look",
    ),
    StyleRecipe(
        "coe5_painted_pixel",
        "Painted pixel",
        "early 2000s painted pixel art fantasy battle sprite, soft shading on simple blocky forms, "
        f"top-down oblique view, {_SINGLE}",
        family="legacy",
        notes="Suggested default",
    ),
    StyleRecipe(
        "coe5_clean_hd_sprite",
        "Clean restrained sprite",
        "simple retro fantasy battle sprite, clean linework, controlled contrast, "
        f"top-down oblique view, {_SINGLE}, not hyperdetailed, chunky pixels",
        family="legacy",
    ),
    StyleRecipe(
        "coe5_illwinter_adjacent",
        "Restrained tactical sprite",
        "restrained palette fantasy battle unit sprite, top-down oblique view, "
        f"simplified blocky forms, {_SINGLE}, high readability at small size",
        family="legacy",
    ),
    StyleRecipe(
        "coe5_ink_outline",
        "Ink-outlined sprite",
        "fantasy battle sprite with heavy ink outlines, flat color regions, "
        f"limited palette, top-down oblique view, {_SINGLE}",
        family="legacy",
    ),
    StyleRecipe(
        "coe5_dithered_pixel",
        "Dithered retro sprite",
        "1990s PC RPG battle sprite, ordered dither shading, limited palette, "
        f"top-down oblique view, {_SINGLE}, crisp silhouette",
        family="legacy",
    ),
    StyleRecipe(
        "coe5_hand_painted",
        "Painted mini illustration",
        "painted fantasy mini illustration at tiny sprite scale, simple forms, "
        f"top-down oblique view, {_SINGLE}, readable silhouette",
        family="legacy",
    ),
    StyleRecipe(
        "coe5_low_saturation",
        "Low saturation tactical sprite",
        "desaturated fantasy battle unit sprite, muted earth-tone palette, "
        f"top-down oblique view, {_SINGLE}, strong silhouette readability",
        family="legacy",
    ),
]

STYLE_CATALOG: list[StyleRecipe] = FIDELITY_CATALOG + ORIGINAL_CATALOG + LEGACY_CATALOG
STYLE_BY_ID = {item.id: item for item in STYLE_CATALOG}
DEFAULT_STYLE_ID = "coe5_painted_pixel"


def styles_for_families(families: list[str] | None = None) -> list[StyleRecipe]:
    if not families:
        return list(STYLE_CATALOG)
    allowed = set(families)
    return [item for item in STYLE_CATALOG if item.family in allowed]


def style_ids_for_families(families: list[str] | None = None) -> list[str]:
    return [item.id for item in styles_for_families(families)]


def resolve_style_slot(style_id: str) -> tuple[str, str, str]:
    recipe = STYLE_BY_ID.get(style_id)
    if recipe is None:
        recipe = STYLE_BY_ID[DEFAULT_STYLE_ID]
    return recipe.style, recipe.id, recipe.label
