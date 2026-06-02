"""Anchor subjects for COE5 sprite style probes."""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class SpriteArchetype:
    id: str
    label: str
    subject: str
    entity_type: str  # monster | item | terrain
    canvas: int
    huge: bool = False
    gen_width: int = 512
    gen_height: int = 512


ARCHETYPE_CATALOG: list[SpriteArchetype] = [
    SpriteArchetype(
        "human_soldier",
        "Human soldier",
        "human soldier in leather armor with sword and shield",
        "monster",
        64,
    ),
    SpriteArchetype(
        "centaur_melee",
        "Centaur melee",
        "centaur warrior with bow and quiver, horse hindquarters",
        "monster",
        64,
    ),
    SpriteArchetype(
        "huge_dragon",
        "Huge dragon",
        "massive red dragon with spread wings and long tail",
        "monster",
        128,
        huge=True,
    ),
    SpriteArchetype(
        "magic_sword_item",
        "Magic sword item",
        "ornate enchanted longsword with glowing runes",
        "item",
        64,
    ),
    SpriteArchetype(
        "forest_terrain",
        "Forest terrain tile",
        "dense temperate forest floor with moss, leaf litter, and dappled green tones",
        "terrain",
        64,
        gen_width=1328,
        gen_height=1328,
    ),
]

ARCHETYPE_BY_ID = {item.id: item for item in ARCHETYPE_CATALOG}
