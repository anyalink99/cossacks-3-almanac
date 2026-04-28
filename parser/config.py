import json
import os
from pathlib import Path

# Steam install root for Cossacks 3. Override with env var COSSACKS3_PATH if your install is elsewhere.
GAME_ROOT = Path(os.environ.get(
    "COSSACKS3_PATH",
    r"C:\Program Files (x86)\Steam\steamapps\common\Cossacks 3",
))
SCRIPTS = GAME_ROOT / "data" / "scripts"
LIB = SCRIPTS / "lib"
LOCALE = GAME_ROOT / "data" / "locale"

UNIT_SCRIPT = LIB / "unit.script"
COUNTRY_SCRIPT = LIB / "country.script"
DM_GLOBAL = SCRIPTS / "dmscript.global"
PLAYER_SCRIPT = LIB / "player.script"
WEAPON_SCRIPT = LIB / "weapon.script"

# Repository paths (resolved relative to this file: parser/config.py → repo root).
PROJECT_ROOT = Path(__file__).resolve().parent.parent
OUTPUT_DIR = PROJECT_ROOT / "output"
RECON_DIR = PROJECT_ROOT / "recon"

# Canonical paths used by all writers.
#
# Layout (cleaned up 2026-04-29):
#   output/
#   ├── data.json              master unified data (input for downstream)
#   ├── derived/               machine-readable JSON for tooling
#   │   ├── animations.json
#   │   ├── builder_slots.json
#   │   ├── pattern_*.json
#   │   └── tech_tree.json
#   ├── reference/             human-readable docs + auto-generated MD reports
#   │   ├── README.md, 01_economy.md, ...   (curated)
#   │   └── reports/                          (auto-generated)
#   │       └── combat_stats.md, counter_matrix.md, map_resources.md, ...
#   └── strategy/              strategy/sim outputs (MD)
#       ├── construction_times.md, production_rates.md, tech_tree.md, ...
#       └── sim/
DATA_JSON = OUTPUT_DIR / "data.json"
DERIVED_DIR = OUTPUT_DIR / "derived"             # JSON only
REFERENCE_DIR = OUTPUT_DIR / "reference"         # MD only
REPORTS_DIR = REFERENCE_DIR / "reports"          # auto-generated MD
STRATEGY_DIR = OUTPUT_DIR / "strategy"           # MD only

# Nation table from country.script:7-41
NATION_ID_TO_SID = {
    0: "aus", 1: "fra", 2: "eng", 3: "spa", 4: "rus", 5: "ukr",
    6: "pol", 7: "swe", 8: "pru", 9: "ven", 10: "tur", 11: "alg",
    12: "mis", 13: "net", 14: "den", 15: "por", 16: "pie", 17: "sax",
    18: "bav", 19: "hun", 20: "swi", 21: "sco", 22: "tat", 23: "lit",
}
NATION_SID_TO_ID = {v: k for k, v in NATION_ID_TO_SID.items()}

# Playable nations (have locale entries; mis/tat/lit excluded)
PLAYABLE_NATIONS = [
    "aus", "fra", "eng", "spa", "rus", "ukr", "pol", "swe", "pru", "ven",
    "tur", "alg", "net", "den", "por", "pie", "sax", "bav", "hun", "swi", "sco",
]
assert len(PLAYABLE_NATIONS) == 21

# Per-nation cluster prefix for each common building (from country.script:2832-2859).
# Different building types map to different clusters.
def _commonname(nat: str) -> str:
    if nat in ("rus", "ukr"):
        return "rus"
    if nat in ("tur", "alg"):
        return "tur"
    return "eur"


def building_cluster(nat: str, suffix: str) -> str:
    """Return the cluster prefix used for the given building suffix on this nation.

    suffix is one of: mil, sto, mar, por, tow, gol, iro, coa, swa, sga, wga, wwa.
    Returns the prefix string (e.g., 'eur', 'rus', 'spa', 'tur', 'ukr', 'por').
    """
    com = _commonname(nat)
    if suffix == "sto":
        if nat == "pol": return "rus"
        if nat in ("spa", "por"): return "spa"
        return com
    if suffix == "mar":
        if nat in ("spa", "por"): return "spa"
        return com
    if suffix == "por":  # shipyard
        if nat == "por": return "por"
        if nat == "ukr": return "ukr"
        return com
    if suffix in ("gol", "iro", "coa"):
        return "eur"  # mines are always eur-prefixed
    if suffix == "wwa" or suffix == "wga":
        return "ukr"  # wood walls/gates always ukr-prefixed
    if suffix == "swa" or suffix == "sga":
        # stone walls follow common cluster (eur/rus/tur), ukr has no stone walls
        return com
    return com  # mil, tow, etc.


# Legacy / convenience: nation→primary cluster name (the value of `commonName` in script)
NATION_TO_COMMON_CLUSTER = {nat: _commonname(nat) for nat in PLAYABLE_NATIONS}

RESOURCES = ["food", "wood", "stone", "gold", "iron", "coal"]
RESOURCE_INDEX = {r: i + 1 for i, r in enumerate(RESOURCES)}  # 1..6 (matches gc_resource_type_*)

WEAPON_KIND_NAMES = {
    "gc_obj_weapon_kind_pike": "pike",
    "gc_obj_weapon_kind_sword": "sword",
    "gc_obj_weapon_kind_bullet": "bullet",
    "gc_obj_weapon_kind_arrow": "arrow",
    "gc_obj_weapon_kind_cannonball": "cannonball",
    "gc_obj_weapon_kind_cannister": "cannister",
}

# px / tile (dmscript.global:172)
PIXELS_TO_TILE = 53.3333333


def px_to_tiles(px: int | float | None) -> float | None:
    if px is None:
        return None
    try:
        return round(float(px) / PIXELS_TO_TILE, 2)
    except (TypeError, ValueError):
        return None


# Upgrade type decoder (dmscript.global:737-764)
UPG_TYPE_DECODE = {
    "gc_upg_type_none": (0, "—", ""),
    "gc_upg_type_lifeperc": (1, "HP %", "Health % bonus"),
    "gc_upg_type_damage": (2, "+damage", "Adds flat damage to specific weapon kind"),
    "gc_upg_type_damageperc": (3, "+damage %", "Damage % bonus"),
    "gc_upg_type_protection": (4, "+protection", "Adds flat protection vs weapon kinds"),
    "gc_upg_type_shield": (5, "+shield", "Shield bonus (negates damage up to N)"),
    "gc_upg_type_enableunit": (6, "enable unit", "Unlocks a unit/building"),
    "gc_upg_type_effectfood": (7, "+food eff %", "Adds X% to food extraction efficiency"),
    "gc_upg_type_effectfoodperc": (8, "+food eff %", "Adds X% to food extraction efficiency"),
    "gc_upg_type_effectwood": (9, "+wood eff %", "Adds X% to wood extraction efficiency"),
    "gc_upg_type_effectwoodperc": (10, "+wood eff %", "Adds X% to wood extraction efficiency"),
    "gc_upg_type_effectstone": (11, "+stone eff %", "Adds X% to stone extraction efficiency"),
    "gc_upg_type_effectstoneperc": (12, "+stone eff %", "Adds X% to stone extraction efficiency"),
    "gc_upg_type_priceperc": (13, "price %", "Modifies unit/building price by %"),
    "gc_upg_type_buildtimeperc": (14, "build time %", "Modifies build time by %"),
    "gc_upg_type_attpauseperc": (15, "reload %", "Modifies attack pause (lower = faster)"),
    "gc_upg_type_attrangeperc": (16, "range %", "Modifies attack range %"),
    "gc_upg_type_attdispertionperc": (17, "accuracy %", "Modifies dispersion (lower = more accurate)"),
    "gc_upg_type_healing": (18, "healing", "Heals all units (one-time)"),
    "gc_upg_type_fishingperc": (19, "+fish eff %", "Increases boat fish capacity"),
    "gc_upg_type_geology": (20, "geology", "Reveals hidden mineral deposits"),
    "gc_upg_type_balloon": (21, "balloon", "Reveals whole map (Montgolfier)"),
    "gc_upg_type_speedperc": (22, "speed %", "Movement speed %"),
    "gc_upg_type_fieldlifeperc": (23, "+field HP %", "Adds X to fieldlife (HP/hit reduction)"),
    "gc_upg_type_single_inside": (24, "+building capacity", "Increases building peasant capacity"),
    "gc_upg_type_single_inside_mine": (25, "+mine workers", "Adds X workers to mine capacity (per mine)"),
    "gc_upg_type_single_attpauseperc": (26, "single reload %", "Per-building attack pause %"),
    "gc_upg_type_single_buildgate": (27, "build gate", "Allows wall→gate conversion"),
}


def decode_upg_type(itype_str) -> tuple[str, str]:
    """Return (short_name, description) for a gc_upg_type_* identifier or numeric ID."""
    if not itype_str:
        return ("", "")
    s = str(itype_str).strip()
    if s in UPG_TYPE_DECODE:
        _, short, desc = UPG_TYPE_DECODE[s]
        return (short, desc)
    try:
        n = int(s)
        for name, (i, short, desc) in UPG_TYPE_DECODE.items():
            if i == n:
                return (short, desc)
    except (ValueError, TypeError):
        pass
    return (s, "")  # unknown


# Object usage decoder (dmscript.global:307-339)
USAGE_DECODE = {
    "gc_obj_usage_none":          (0, "—"),
    "gc_obj_usage_mill":          (1, "Mill"),
    "gc_obj_usage_farm":          (2, "Housing/Farm"),
    "gc_obj_usage_center":        (3, "Town Hall"),
    "gc_obj_usage_storage":       (4, "Storehouse"),
    "gc_obj_usage_tower":         (5, "Tower"),
    "gc_obj_usage_field":         (6, "Field"),
    "gc_obj_usage_mine":          (7, "Mine"),
    "gc_obj_usage_fasthorse":     (8, "Light Cavalry"),
    "gc_obj_usage_mortar":        (9, "Mortar"),
    "gc_obj_usage_cannon":        (10, "Cannon"),
    "gc_obj_usage_grenadier":     (11, "Grenadier"),
    "gc_obj_usage_hardwall":      (12, "Stone Wall/Gate"),
    "gc_obj_usage_weakwall":      (13, "Wood Wall/Gate"),
    "gc_obj_usage_battleship":    (14, "Battleship"),
    "gc_obj_usage_weak":          (15, "Weak unit"),
    "gc_obj_usage_fisher":        (16, "Fishing Boat"),
    "gc_obj_usage_artdepo":       (17, "Artillery Depot"),
    "gc_obj_usage_supermortar":   (18, "Super Mortar"),
    "gc_obj_usage_port":          (19, "Shipyard"),
    "gc_obj_usage_lightinfantry": (20, "Light Infantry"),
    "gc_obj_usage_shooter":       (21, "Shooter"),
    "gc_obj_usage_hardhorse":     (22, "Heavy Cavalry"),
    "gc_obj_usage_peasant":       (23, "Peasant"),
    "gc_obj_usage_horseshooter":  (24, "Mounted Shooter"),
    "gc_obj_usage_frigate":       (25, "Frigate"),
    "gc_obj_usage_galley":        (26, "Galley"),
    "gc_obj_usage_yacht":         (27, "Yacht"),
    "gc_obj_usage_xebec":         (28, "Xebec"),
    "gc_obj_usage_transport":     (29, "Transport"),
    "gc_obj_usage_archer":        (30, "Archer"),
    "gc_obj_usage_mcannon":       (31, "Multi-cannon"),
    "gc_obj_usage_dipcenter":     (32, "Diplomatic Center"),
}


def decode_usage(usage_str) -> str:
    """Convert gc_obj_usage_* identifier (or numeric ID) to human-readable name."""
    if not usage_str:
        return ""
    s = str(usage_str).strip()
    if s in USAGE_DECODE:
        return USAGE_DECODE[s][1]
    try:
        n = int(s)
        for name, (i, short) in USAGE_DECODE.items():
            if i == n:
                return short
    except (ValueError, TypeError):
        pass
    return s


# =============================================================================
# Animation timings
# =============================================================================
# Engine timing: each frame = 1 / gc_time_to_frames game-second (dmscript.global:175).
ANIM_FRAMES_PER_GAMESEC = 32  # gc_time_to_frames

# Frame counts for peasant work animations — VERIFIED in
# data/animations/aaf/peaaus.aaf (all peasant nations share the same animation file).
PEASANT_ANIM_FRAMES = {
    "construct":  13,  # frames 186-198 (= one builder hammer swing on a foundation)
    "workfood":   22,  # frames 278-299 (= one chop on a field/sheaf)
    "workwood":   18,  # frames 237-254 (= one chop on a tree; reused for melee attack0)
    "workstone":  18,  # frames 217-234
    "attack0":    18,  # frames 237-254 (peasant melee = workwood reused)
}
PEASANT_ANIM_SEC = {k: round(v / ANIM_FRAMES_PER_GAMESEC, 4)
                    for k, v in PEASANT_ANIM_FRAMES.items()}
# E.g. PEASANT_ANIM_SEC["construct"] = 0.4063

# Soldier melee swing length is per-unit (varies 11..33 frames across 84 units;
# median 15). When `weapon.pause = 0` ("fires every animation cycle") use
# `melee_swing_sec(unit_sid)` to get the unit's actual attack0 length, falling
# back to the median when the .aaf file is missing or doesn't expose attack0.
MELEE_SWING_FALLBACK_FRAMES = 15  # median across all melee units in data/animations/aaf
MELEE_SWING_FALLBACK_SEC = round(MELEE_SWING_FALLBACK_FRAMES / ANIM_FRAMES_PER_GAMESEC, 4)
# 0.4688 g-sec

ANIMATIONS_JSON = DERIVED_DIR / "animations.json"
_animations_cache: dict | None = None


def _load_animations() -> dict:
    global _animations_cache
    if _animations_cache is None:
        if ANIMATIONS_JSON.exists():
            _animations_cache = json.loads(ANIMATIONS_JSON.read_text(encoding="utf-8"))
        else:
            _animations_cache = {}
    return _animations_cache


def get_anim_sec(unit_sid: str, anim_name: str) -> float | None:
    """Return animation length in game-seconds for given unit + anim, or None.

    Frame range in animations.json is INCLUSIVE: length = end - start + 1.
    Outliers (>=100 frames) are filtered as those usually represent compound tracks.
    """
    tracks = _load_animations().get(unit_sid)
    if not tracks or anim_name not in tracks:
        return None
    s, e = tracks[anim_name]
    n = e - s + 1
    if n <= 0 or n >= 100:
        return None
    return round(n / ANIM_FRAMES_PER_GAMESEC, 4)


def melee_swing_sec(unit_sid: str) -> float:
    """Per-unit melee swing duration in g-sec; falls back to median across all units."""
    return get_anim_sec(unit_sid, "attack0") or MELEE_SWING_FALLBACK_SEC

# =============================================================================
# Empirical guesses — UNVERIFIED in scripts (see recon/empirical_tests.md)
# =============================================================================
# Above-ground extraction overhead — fraction of work-cycle time wasted walking
# between resource node and storehouse. Depends on map layout; not derived from code.
WALK_OVERHEAD_GUESS = 0.30
# Mine extraction overhead — peasants stay inside the mine, so less travel.
MINE_OVERHEAD_GUESS = 0.05

# =============================================================================
# Field mechanics (env.inc/initial.inc:75-103, env.inc/nothing.inc:30-87,
# unit.script:1692, unit.script:6470)
# =============================================================================
FIELD_GOLD_COST = 5            # objbase.price[gold] for unit 'field' (unit.script:1692)
FIELD_MAX_HP = 25000           # gc_FieldMaxHP, dmscript.global:128
FIELD_GROW_TIME_SEC = 4 * 21.875   # cFieldGrowTime: spawn → mature (87.5 g-sec)
FIELD_REST_TIME_SEC = 21.875       # cFieldRestTime: dead → rebirth (g-sec)
FIELD_REGEN_INTERVAL_SEC = 31.25   # cFieldRestartTime: regen tick interval
FIELD_REGEN_PER_TICK_MAX = 2500    # +floor(MaxHP × random × 0.1) per tick when at stage_0
FIELDS_PER_MILL = 49           # 7×7 grid in _unit_DoSeedWheat (unit.script:6475-6476)

# =============================================================================
# Population cap (building.inc/doprogressorders.inc:142-152, dmscript.global:1090-1097)
# =============================================================================
GC_MAX_OBJ_COUNT = 32000       # engine-wide, all players combined
MAP_SETTINGS_LIMIT = {         # gc_mapsettings_limit_1..8 (selectable in lobby)
    1: 500, 2: 750, 3: 1000, 4: 1500,
    5: 2200, 6: 3000, 7: 5000, 8: 8000,
}
# Farm slots per building (cen=100, bar=150, ba2=250, hou=25; sum + map limit clamp)
# These are in data.json per-building b['farm']; loaded at runtime.

# =============================================================================
# Mine peasantabsorber cap (unit.script:2315, control.script:506-513)
# =============================================================================
MINE_BASE_PEASANTABSORBER = 5
# Per-mine bonus from 6 upgrades (gol/iro/coa.1..6): +5/+8/+10/+12/+15/+40
# Cumulative: 5 base → 10 → 18 → 28 → 40 → 55 → 95
MINE_UPGRADE_BONUSES = [5, 8, 10, 12, 15, 40]
MINE_MAX_PEASANTABSORBER = MINE_BASE_PEASANTABSORBER + sum(MINE_UPGRADE_BONUSES)  # 95

# =============================================================================
# Formation bonuses (data/game/var/formations.cfg)
# =============================================================================
# Most "LINE*" plain formations: 0 bonus. Tactical formations (LINE15+, SQUARE*,
# KARE*) give +2/+2 walk and +7/+7 hold. Triangles +1/+1 always.
# These are FLAT bonuses (added to damage/shield), not multipliers — meaningful
# only for low-damage units (e.g. pikeman damage=20 +7 hold = +35%).
FORMATION_BONUS_TACTICAL = {"walk": (2, 2), "hold": (7, 7)}  # (damage, shield)
FORMATION_BONUS_TRIANGLE = {"walk": (1, 1), "hold": (1, 1)}
FORMATION_BONUS_LINE400 = {"walk": (3, 3), "hold": (7, 7)}


# Object base speed table (dmscript.global:603-620). Abstract units (NOT tiles/sec).
# Used as relative-speed indicator between unit classes.
OBJ_SPEED_TABLE = {
    "default":      32,
    "peasant":      40,
    "hardhorse":    56,
    "fasthorse":    96,
    "cannon":       20,
    "mortar":       24,
    "howitzer":     20,
    "multicannon":  16,
    "fishboat":     16,
    "ferry":        28,
    "yacht":        40,
    "yachttur":     70,
    "chaika":       55,
    "galley":       40,
    "frigate":      30,
    "xebec":        28,
    "battleship":   16,
}
