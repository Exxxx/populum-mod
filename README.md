# Populum Mod

A Conquest of Elysium 5 mod that links classes together in a thematic, story-like fashion based loosely on French and Raven's Five Forms of Power and systems of government, connecting to social, political, and economic attributes.

## Summary

Populum increases the depth of economy management and expands the early and late game of the classes by introducing new options. You will find that many commander units, especially spell-casters, will have some ritual powers and in some circumstances may be able to change into other classes or units.

The classes have been re-flavored based on government types. Most of the classes can be thought of as paths branching away from the Monarchy (Baron), Republic (Senator), Minarchy (Witch), and other secondary classes pathing into even more niche variants. In some instances, there may not be a path back from some classes without capturing a terrain tile that permits a person on a particular path. Traditional class recruitment is minimal in Populum except for NPC classes. Recruitment is predominately through various ritual powers that people have. Recruitment offers depend on having certain people at certain locations. Not every class has been expanded and connected, especially newer classes released in CoE5. This is a work in progress.

### NPC Classes

Some classes are meant for the AI only and are tagged with an "(NPC)" at the end of the class name. It is not recommended to use these NPC classes as they are designed to be played by the AI with significant bonuses. These classes include: Goblin Emperor, Slave King, Independent Town, Bandit King, and the boss class called "Blood Tide," which is limited to one due to its unique boss. These classes were designed to be difficult early-game enemies and a mere nuisance to late-game players.

The NPC classes have their recommended difficulty built into the class name and are designed for the largest map size (enormous or custom larger). You may want to decrease an NPC's difficulty by one for 1–2 map size class reductions. For example, the Goblin Emperor on enormous+ is played on Emperor difficulty; reduce to King for a Huge map, Duke for Large, Marquis for Medium, and anything smaller set to Count.

## Features

- About 800 new rituals
- About 900 new units/variants
- Redesigned economy with unit upkeep and scaled income by ekistics (population)
- Redesigned and rebalanced combat mechanics, e.g., large and huge weapons with reach and differentiated bows with longer range
- Craft many items through rituals
- More units have special terrain stealth
- More terrain movement variation between units
- Smoothed and reduced the movement cost of many terrains
- Less inherent vision, more use for scouting and stealth
- More options to traverse water and faster water movement. Many water units will change into a watershape that floats on water, allowing faster movement
- More immortality options
- Overall increased hitpoint levels for lower HP units, and less or none for high HP units
- Shields provide an air shield effect
- Mounts will be regained on certain terrains linked to the mount. For example, unicorn riders can regain their mount in ancient forests and sacred groves only. Typical human horse mounts can be acquired in village-sized settlements or larger. Hoburgers gain mounts inside their settlements
- Other mass rebalances; for example, some units such as undead are immune to decay effects in Populum, and most mounted units will lose their mount after taking damage

## Installation

1. Use the [Steam Workshop](https://steamcommunity.com/sharedfiles/filedetails/?id=2775315657) to install.
2. Run Conquest of Elysium 5.
3. Select **Mods** and activate the Populum module.

**Uninstallation:** Use the unsubscribe button in the Steam Workshop.

## Content Warning

This mod contains content (textual and game mechanics, not imagery) that may make some people uncomfortable, including:

- Violence
- Kidnapping and abduction
- Enslavement
- Death or dying
- Pregnancy/Childbirth
- Mental illness
- Sexual Assault
- Abuse
- Animal cruelty or animal death
- Self-harm and suicide
- Eating disorders
- Racism
- Sexism and misogyny
- Classism

## Optional Modules

### Cheat Module

[Workshop cheat module for Populum](https://steamcommunity.com/sharedfiles/filedetails/?id=2775315658)

If you would like to play more freely, it is recommended you enable the CHEAT module. It comes with a teleporting "Director Tool" that also gives the first player on the list many resources.

*Note: You need to have both `populum.c5m` and `popCHEAT.c5m` activated at the same time.*

## Custom Maps

### Game of Thrones Map

The Game of Thrones map (`GOTcoe5.coem`) is a fixed starting location map due to the density of resources and lots of geographic choke-points. A list of starting locations is available in the map description (v2.06).

Thanks to Wankovich for the port from CoE4 to CoE5.

## Known Quirks

> Immortality is tied to the plane the monster becomes immortal on. Dying on another plane will result in permanent death.

## Technical Note

Populum's turn processing time should be more reasonable than previous versions given the reduction and removal of many events. Multiplayer games should always be hosted on the best CPU.

## Versioning and Compatibility

**1.0 is not compatible with earlier saved game versions.**

- [Change log 0.9 and older (to be updated)](https://docs.google.com/spreadsheets/d/1A-hHWlm9upzErIxri1FpvsxphE6p8dKdkk98Tplqq_c/edit?usp=sharing)
- [Previous Versions for CoE4](https://steamcommunity.com/app/403950/discussions/1/305510202671981080/)

## Links

- [Populum mod on GitHub](https://github.com/Exxxx/populum-mod)
- [Map of Populum Paths (old reference)](https://drive.google.com/open?id=19h6MOrRvle8WhzF8QrCkJ9l9ULZuMctE) — dotted lines indicate a connected person that is required to be present or may cast the ritual required

---

## Modding and Contributing

Forks and pull requests are welcome. Before editing, read the [CoE5 modding manual](https://illwinter.com/coe5/coe5modding.html). Run validation before submitting any change that adds, removes, or reorders `newritual` blocks.

### Prerequisites

- Python 3.11+
- Conquest of Elysium 5 (for in-game testing)

```bash
pip install -r py_tools/requirements.txt
```

### Repository layout

Open the `mods/` folder as the workspace (parent of `populum/`). Only `populum/` is published to Steam Workshop.

| Path | Purpose |
|------|---------|
| `populum/populum.c5m` | Main mod file (~90k lines) |
| `populum/pop/` | Sprites, banners, map tiles |
| `populum/GOTcoe5.coem` | Custom Game of Thrones map |
| `populum/readme.txt`, `populum/steam_descr.txt` | Steam Workshop text |
| `py_tools/` | Validation, lookup, and utility scripts |
| `tools/` | VS Code/Cursor syntax extension and grammar generator |
| `.vscode/` | Workspace settings and validation tasks |
| `.cursor/rules/` | Optional Cursor AI rules (same constraints as below) |

### Save compatibility (critical)

When updating existing content, **append only** new units, classes, rituals, weapons, and terrain at the **end** of their respective sections. Inserting definitions in the middle shuffles IDs and breaks saved games.

Appending `newritual` at the end is safe for save games but still shifts the global ritual index used by `gainrit` offsets on every line that points forward to a mod ritual. Always run gainrit validation after any `newritual` add, remove, or reorder.

Commands in `.c5m` files run top-to-bottom. Define weapons, monsters, and other prerequisites before referencing them.

### Required workflow after ritual changes

CoE5 resolves `gainrit <offset>` against the **global ritual list**: vanilla `newritual` entries first, then every Populum `newritual` in file order. Stale offsets grant the wrong ritual with no in-game error.

After any edit that adds, removes, or moves a `newritual` block:

```bash
python py_tools/validate_populum.py --fix --describe
```

- `--fix` — rewrite offsets to match trailing `# "Target Ritual"` comments (keep those comments accurate when editing)
- `--describe` — refresh describer comments after offset fixes or new `gainrit` lines

Validate only (no file writes):

```bash
python py_tools/validate_populum.py
```

In VS Code or Cursor: **Tasks → Run Test Task → Validate Populum (gainrit)** or **Validate Populum (fix + describe)**.

### Tool reference

| Tool | When to use |
|------|-------------|
| `py_tools/validate_populum.py` | Validate, fix, and describe all `gainrit` lines |
| `py_tools/gainrit_distance.py` | GUI: find offset between two ritual names |
| `py_tools/gainrit_describer.py` | Refresh `# "Target"` comments on `gainrit` lines |
| `py_tools/gainrit_validator.py` | Lower-level validate/fix (used by `validate_populum.py`) |
| `py_tools/extract_modding_manual.py` | Look up commands, search manual, show reference tables |
| `py_tools/pop_hp.py` | Bulk HP rebalance using Populum's scaling formula |
| `tools/generate_c5m_grammar.py` | Rebuild TextMate grammar after `c5m.xml` changes |

### Sprite art pipeline (`art_tools/`)

ComfyUI batch tools for generating missing `spr1` / `spr2` / item / terrain sprites. Requires ComfyUI at `http://127.0.0.1:8000` and the Qwen workflows in `art_tools/workflows/`.

```bash
# One-time: create venv and install deps
python -m venv art_tools/.venv
art_tools/.venv/Scripts/pip install -r art_tools/requirements.txt

# Windows (PowerShell) — use venv Python for all art_tools commands:
$env:ART_PY = "art_tools/.venv/Scripts/python.exe"

# 1. Probe art styles (pick winner in art_tools/coe5_probe_winners.json)
& $env:ART_PY art_tools/comfyui_probe_sprite_styles.py --resume

# 2. Scan mod for missing sprite files
& $env:ART_PY art_tools/comfyui_run_sprites.py --scan populum/populum.c5m

# 3. Generate missing sprites (Pass 1: all spr1/2512, then Pass 2: all spr2/Edit)
& $env:ART_PY art_tools/comfyui_run_sprites.py --jobs art_tools/generated/missing_sprites_jobs.json --resume

# Monster style tuning (vanilla controls in art/coe5_sprites/monster/)
& $env:ART_PY art_tools/monster_sprite_registry.py --refresh
& $env:ART_PY art_tools/monster_sprite_registry.py --lookup Spearman
& $env:ART_PY art_tools/monster_sprite_registry.py --lookup knight --pick 1
& $env:ART_PY art_tools/comfyui_probe_monster_tuning.py --families fidelity original --dry-run
& $env:ART_PY art_tools/comfyui_probe_monster_tuning.py --families fidelity original --resume
```

On Linux/macOS, use `art_tools/.venv/bin/python` instead of `Scripts/python.exe`.

VS Code/Cursor tasks: **Scan Populum missing sprites**, **Probe COE5 sprite styles (dry-run)**, **Probe monster style tuning (dry-run)**, **Run COE5 sprite batch (dry-run)**.

**Command lookup** (run from repo root):

```bash
python py_tools/extract_modding_manual.py lookup --command-index gainrit
python py_tools/extract_modding_manual.py command-index clear
python py_tools/extract_modding_manual.py search "area of effect"
python py_tools/extract_modding_manual.py table dmgtype
```

If `py_tools/references/coe5_modding_rules.json` is missing:

```bash
python py_tools/extract_modding_manual.py extract --command-index
```

Cross-check entity names in `py_tools/references/` (Monster, Ritual, Weapon, Class, etc.) before inventing duplicates. See `py_tools/references/README.md`.

### Editor setup

Pick one editor — all paths below use files included in this repo.

**VS Code / Cursor**

1. Install the Python extension (`ms-python.python`) if prompted.
2. Install the bundled c5m syntax extension: **Extensions → … → Install from VSIX…** → select `tools/vscode-c5m/c5m-1.0.0.vsix`. (This extension is not published to the marketplace.)
3. Open the `mods/` folder as the workspace. `.vscode/settings.json` associates `*.c5m` and `*.coem` with the c5m language.

**Notepad++**

Follow `py_tools/references/How to install CoE syntax highlighting for Notepad++.txt` using `py_tools/references/c5m.xml`.

**Cursor (optional)**

The `.cursor/rules/` directory encodes the same save-compatibility and validation rules for AI-assisted editing.

### Reference data

`py_tools/references/` holds read-only vanilla v5.33 snapshots and pre-built manual extracts so lookups work offline. Do not edit these as part of Populum changes.

To refresh after an Illwinter manual update:

```bash
python py_tools/extract_modding_manual.py extract --command-index --refresh
```

### Testing changes

Edits in `populum/` are picked up by CoE5 immediately after save. Enable the Populum mod in-game and restart if the mod list was open during editing.

---

## Acknowledgments

- Thanks to the Devs for making this game and fixing bugs that affect it and mod development.
- Thanks to the CoE5 modding community and those testing.
- Thanks to Colonel Dracula joins the Navy and Marlin for their work in extracting unit, ritual, and other data, making this project possible.
- Thanks to those who created mods and graphics integrated into Populum.
