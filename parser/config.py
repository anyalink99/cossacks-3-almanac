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

# Canonical paths used by all writers
DATA_JSON = OUTPUT_DIR / "data.json"
REFERENCE_DIR = OUTPUT_DIR / "reference"
DERIVED_DIR = REFERENCE_DIR / "derived"
STRATEGY_DIR = OUTPUT_DIR / "strategy"

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
