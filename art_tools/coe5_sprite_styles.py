"""Style catalog for COE5 sprite style probes."""
from __future__ import annotations

# Re-export unified catalog from style families module.
from coe5_style_families import (
    DEFAULT_STYLE_ID,
    FIDELITY_CATALOG,
    LEGACY_CATALOG,
    ORIGINAL_CATALOG,
    STYLE_BY_ID,
    STYLE_CATALOG,
    StyleRecipe,
    resolve_style_slot,
    style_ids_for_families,
    styles_for_families,
)

__all__ = [
    "DEFAULT_STYLE_ID",
    "FIDELITY_CATALOG",
    "LEGACY_CATALOG",
    "ORIGINAL_CATALOG",
    "STYLE_BY_ID",
    "STYLE_CATALOG",
    "StyleRecipe",
    "build_style_probe_variations",
    "resolve_style_slot",
    "style_ids_for_families",
    "styles_for_families",
]


def build_style_probe_variations(
    *,
    archetype_id: str,
    subject: str,
    canvas: int,
    huge: bool,
    entity_type: str,
    style_ids: list[str] | None = None,
) -> list[dict]:
    from coe5_sprite_prompts import build_item_prompt, build_spr1_prompt, build_terrain_prompt

    ids = style_ids or [item.id for item in STYLE_CATALOG]
    variations: list[dict] = []
    for sid in ids:
        recipe = STYLE_BY_ID.get(sid)
        if recipe is None:
            continue
        if entity_type == "terrain":
            prompt = build_terrain_prompt(subject=subject, style=sid)
        elif entity_type == "item":
            prompt = build_item_prompt(subject=subject, canvas=canvas, style=sid)
        else:
            prompt = build_spr1_prompt(subject=subject, canvas=canvas, huge=huge, style=sid)
        variations.append(
            {
                "style_id": sid,
                "archetype_id": archetype_id,
                "state_key": f"{sid}__{archetype_id}",
                "label": f"{recipe.label} · {archetype_id}",
                "prompt": prompt,
                "canvas": canvas,
                "huge": huge,
                "entity_type": entity_type,
            }
        )
    return variations
