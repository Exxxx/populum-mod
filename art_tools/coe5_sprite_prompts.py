"""Layered prompt assembly for COE5 sprite generation."""
from __future__ import annotations

import json
import re
from pathlib import Path

from coe5_sprite_background import (
    BgMode,
    DEFAULT_BG_MODE,
    prompt_background_phrase,
    tuning_negative_extras,
)

TOOLS_DIR = Path(__file__).resolve().parent
WINNERS_PATH = TOOLS_DIR / "coe5_probe_winners.json"

SPRITE_NEGATIVE_PROMPT = (
    "过度光滑，画面具有AI感。构图混乱。文字模糊，扭曲，水印，文字，标签"
)

SPRITE_TUNING_NEGATIVE_PROMPT = (
    f"{SPRITE_NEGATIVE_PROMPT}, {tuning_negative_extras(DEFAULT_BG_MODE)}"
)


def build_tuning_negative_prompt(bg_mode: BgMode = DEFAULT_BG_MODE) -> str:
    return f"{SPRITE_NEGATIVE_PROMPT}, {tuning_negative_extras(bg_mode)}"

# Exact weapon names from Monster Data → prompt-safe text (None = omit wielding phrase).
WEAPON_EXACT_REWRITES: dict[str, str | None] = {
    "fist": None,
}

# Regex rewrites applied to weapon names before they enter prompts.
WEAPON_PATTERN_REWRITES: list[tuple[re.Pattern[str], str | None]] = [
    (re.compile(r"thunder\s+fist", re.I), "thunder magic"),
    (re.compile(r"tail\s+sweep", re.I), "tail attack"),
    (re.compile(r"\bfist\b", re.I), None),
]


def sanitize_weapon_for_prompt(weapon: str | None) -> str | None:
    """Return weapon text safe for Qwen prompts, or None to skip a wielding phrase."""
    if not weapon:
        return None
    text = weapon.strip()
    if not text:
        return None

    lower = text.lower()
    if lower in WEAPON_EXACT_REWRITES:
        return WEAPON_EXACT_REWRITES[lower]

    for pattern, replacement in WEAPON_PATTERN_REWRITES:
        if pattern.search(text):
            if replacement is None:
                return None
            return pattern.sub(replacement, text)

    return text


def build_sprite_subject(
    *,
    name: str,
    melee_weapon: str | None = None,
    ranged_weapon: str | None = None,
    huge: bool = False,
    descr: str | None = None,
    include_descr: bool = False,
) -> str:
    """Short visual subject for sprite prompts — name and gear only by default."""
    parts = [name.strip()]

    melee = sanitize_weapon_for_prompt(melee_weapon)
    if melee_weapon:
        if melee is None:
            parts.append("unarmed fighter")
        else:
            parts.append(f"wielding {melee}")
    elif ranged_weapon:
        ranged = sanitize_weapon_for_prompt(ranged_weapon)
        if ranged:
            parts.append(f"using {ranged}")

    if huge:
        parts.append("huge creature")
    if include_descr and descr:
        parts.append(descr.strip())
    return ", ".join(parts)


def sprite_composition_constraints(bg_mode: BgMode = DEFAULT_BG_MODE) -> str:
    return (
        "exactly one character only, single isolated figure, no duplicate figures, no size comparison, "
        "simple low-detail game sprite, limited color palette, no scenery"
    )


def foot_padding_constraint(canvas: int = 64) -> str:
    target_h = int(canvas * 0.85)
    return (
        f"standing character about {target_h} pixels tall with 2 pixels empty space below the figure base, "
        "character anchored near bottom center of canvas"
    )


def composition_block(canvas: int, bg_mode: BgMode = DEFAULT_BG_MODE, *, huge: bool = False) -> str:
    """Single composition clause: canvas size, background, framing, and isolation."""
    gen_bg = prompt_background_phrase(bg_mode)
    huge_bit = ", large creature proportions" if (canvas >= 128 or huge) else ""
    return (
        f"{small_canvas_constraints(canvas)}{huge_bit}, {gen_bg}, "
        f"{foot_padding_constraint(canvas)}, one isolated character, top-down oblique view, no scenery"
    )

TERRAIN_BASE_STYLE = (
    "High-fidelity 16-bit JRPG vertical aerial pixel art for world map, "
    "large scale, same scale across entire frame, ground surface, edge-to-edge, "
    "minimal anti-aliasing, retro, rich saturated cohesive color palette"
)

WEAPON_ATTACK_ACTIONS: dict[str, str] = {
    "sword": "swinging sword in a battle attack",
    "bow": "bow drawn ready to shoot arrow",
    "crossbow": "aiming crossbow ready to shoot bolt",
    "spear": "thrusting spear forward",
    "javelin": "throwing javelin",
    "hoof": "rear kick attack pose",
    "claw": "slashing with claws",
    "bite": "lunging with a biting attack",
    "tail": "tail swipe attack arc",
    "fire": "breathing fire in attack pose",
    "spell": "spellcasting pose",
    "whip": "cracking whip in attack motion",
    "axe": "swinging axe overhead",
    "mace": "swinging mace in attack pose",
    "staff": "staff strike attack pose",
    "default": "dynamic melee attack pose",
}


def load_winners(path: Path | None = None) -> dict:
    winners_path = path or WINNERS_PATH
    if not winners_path.is_file():
        return {"style_id": "coe5_painted_pixel"}
    return json.loads(winners_path.read_text(encoding="utf-8"))


def resolve_style(style_id: str | None = None, winners: dict | None = None) -> tuple[str, str]:
    from coe5_style_families import STYLE_BY_ID, DEFAULT_STYLE_ID

    winners = winners or load_winners()
    sid = style_id or winners.get("style_id") or DEFAULT_STYLE_ID
    recipe = STYLE_BY_ID.get(sid)
    if recipe is None:
        recipe = STYLE_BY_ID[DEFAULT_STYLE_ID]
        sid = DEFAULT_STYLE_ID
    return recipe.style, sid


def size_hint(canvas: int, *, huge: bool = False) -> str:
    if canvas >= 128 or huge:
        return (
            "128 by 128 pixel canvas, low resolution pixel art, chunky pixels, "
            "large creature proportions, no fine detail, no smooth gradients"
        )
    if canvas <= 32:
        return "32 by 32 pixel canvas, tiny retro sprite, chunky pixels, minimal detail"
    return (
        "64 by 64 pixel canvas, low resolution retro game sprite, chunky pixels, "
        "minimal detail, no smooth gradients"
    )


def small_canvas_constraints(canvas: int) -> str:
    if canvas >= 128:
        return (
            "low resolution 128x128 pixel art sprite, chunky blocky pixels, simple shapes, "
            "limited color palette, readable at thumbnail size, no illustration detail"
        )
    if canvas <= 32:
        return (
            "low resolution 32x32 pixel art sprite, chunky blocky pixels, very simple shapes, "
            "minimal colors, icon-sized readability"
        )
    return (
        "low resolution 64x64 pixel art sprite, chunky blocky pixels, simple shapes, "
        "SNES-era sprite density, limited color palette"
    )


def item_size_constraint() -> str:
    return "single object no larger than 40 by 40 pixels centered in canvas with black padding"


def infer_attack_action(
    *,
    attack_action: str | None = None,
    melee_weapon: str | None = None,
    ranged_weapon: str | None = None,
) -> str:
    if attack_action:
        return attack_action
    weapon = (melee_weapon or ranged_weapon or "").lower()
    for key, action in WEAPON_ATTACK_ACTIONS.items():
        if key in weapon:
            return action
    return WEAPON_ATTACK_ACTIONS["default"]


def build_spr1_prompt(
    *,
    subject: str,
    canvas: int = 64,
    huge: bool = False,
    style: str | None = None,
    winners: dict | None = None,
    bg_mode: BgMode = DEFAULT_BG_MODE,
) -> str:
    style_text, _ = resolve_style(style, winners)
    return (
        f"{style_text}, {subject}, {composition_block(canvas, bg_mode, huge=huge)}, "
        "no text, no watermark."
    )


def build_spr2_prompt(
    *,
    attack_action: str,
    canvas: int = 64,
    huge: bool = False,
) -> str:
    return (
        f"Same character as the reference image, {attack_action}, "
        f"dynamic battle attack pose, weapon attack motion, "
        f"preserve colors armor and proportions from reference, "
        f"{size_hint(canvas, huge=huge)}, solid black background, no text."
    )


def build_item_prompt(
    *,
    subject: str,
    canvas: int = 64,
    style: str | None = None,
    winners: dict | None = None,
    bg_mode: BgMode = DEFAULT_BG_MODE,
) -> str:
    style_text, _ = resolve_style(style, winners)
    gen_bg = prompt_background_phrase(bg_mode)
    return (
        f"{style_text}, {subject}, centered magic item icon, single object, "
        f"{gen_bg}, generous empty padding, {item_size_constraint()}, "
        f"no text, no character."
    )


def build_terrain_prompt(
    *,
    subject: str,
    style: str | None = None,
    winners: dict | None = None,
) -> str:
    style_text, _ = resolve_style(style, winners)
    return (
        f"{TERRAIN_BASE_STYLE}, {style_text}, {subject}, "
        f"full-frame terrain tile, cohesive palette, no text, no watermark."
    )


def build_monster_tuning_prompt(
    *,
    record: object,
    style_id: str,
    canvas: int | None = None,
    bg_mode: BgMode = DEFAULT_BG_MODE,
) -> str:
    """Build spr1 tuning prompt from a MonsterRecord and style recipe."""
    from coe5_style_families import STYLE_BY_ID, DEFAULT_STYLE_ID
    from monster_sprite_registry import MonsterRecord

    if not isinstance(record, MonsterRecord):
        raise TypeError("record must be a MonsterRecord")

    recipe = STYLE_BY_ID.get(style_id)
    if recipe is None:
        recipe = STYLE_BY_ID[DEFAULT_STYLE_ID]

    c = canvas if canvas is not None else record.canvas
    subject = record.subject_for_tuning()
    return (
        f"{recipe.style}, {subject}, {composition_block(c, bg_mode, huge=record.huge)}, "
        "no text, no watermark."
    )


def build_monster_tuning_edit_prompt(
    *,
    record: object,
    style_id: str,
    canvas: int | None = None,
    bg_mode: BgMode = DEFAULT_BG_MODE,
) -> str:
    """Shorter edit prompt: style transfer while preserving control silhouette."""
    from coe5_style_families import STYLE_BY_ID, DEFAULT_STYLE_ID
    from monster_sprite_registry import MonsterRecord

    if not isinstance(record, MonsterRecord):
        raise TypeError("record must be a MonsterRecord")

    recipe = STYLE_BY_ID.get(style_id)
    if recipe is None:
        recipe = STYLE_BY_ID[DEFAULT_STYLE_ID]

    c = canvas if canvas is not None else record.canvas
    subject = record.subject_for_tuning()
    return (
        f"{recipe.style}, same character as reference image, {subject}, "
        "preserve silhouette proportions armor and colors from reference, "
        f"{composition_block(c, bg_mode, huge=record.huge)}, no text, no watermark."
    )


def build_prompt_for_job(job: dict, winners: dict | None = None, *, bg_mode: BgMode = DEFAULT_BG_MODE) -> str:
    role = job.get("sprite_role", "spr1")
    canvas = int(job.get("canvas", 64))
    huge = bool(job.get("huge", False))
    subject = job.get("subject") or job.get("entity_name") or "fantasy sprite"

    if role == "spr2":
        action = infer_attack_action(
            attack_action=job.get("attack_action"),
            melee_weapon=job.get("melee_weapon"),
            ranged_weapon=job.get("ranged_weapon"),
        )
        return build_spr2_prompt(attack_action=action, canvas=canvas, huge=huge)

    entity_type = job.get("entity_type", "monster")
    if entity_type == "item":
        return build_item_prompt(subject=subject, canvas=canvas, winners=winners, bg_mode=bg_mode)
    if entity_type == "terrain":
        return build_terrain_prompt(subject=subject, winners=winners)
    return build_spr1_prompt(subject=subject, canvas=canvas, huge=huge, winners=winners, bg_mode=bg_mode)


def generation_size_for_job(job: dict) -> tuple[int, int]:
    """Return ComfyUI latent width/height before post-process downscale."""
    from coe5_sprite_sizes import generation_size_for_job as _size_for_job

    return _size_for_job(job)
