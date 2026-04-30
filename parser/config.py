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
DOCS_DIR = PROJECT_ROOT / "docs"

# Layout (reorganized 2026-04-29):
#
#   docs/
#   ├── README.md                navigation + project overview
#   ├── data.json                master unified data (input for all downstream)
#   ├── derived/                 machine-readable JSON datasets
#   │   ├── animations.json, builder_slots.json, tech_tree.json,
#   │   ├── pattern_*.json, replay_ground_truth.json
#   ├── reference/               canonical reference chapters (generated)
#   │   ├── 01_economy.md … 07_naval.md
#   │   ├── nations/<nat>.md (×21 + README)
#   │   └── compare/<class>.md
#   ├── recon/                   deep-mechanics docs (handwritten)
#   │   └── ai_behavior.md, capture_mechanics.md, …
#   ├── reports/                 derived computational reports, grouped by topic
#   │   ├── combat/   combat_stats, counter_matrix, attack_rates, vision_radii
#   │   ├── economy/  builder_slots, construction_times, efficiency_upgrades,
#   │   │             production_rates, scaling_prices
#   │   ├── tech/     tech_tree
#   │   ├── map/      map_resources, map_predictions_validation, starting_layout
#   │   └── nations/  overview
#   └── simulations/             economy simulator outputs (sim_*.{csv,md})
#
DATA_JSON = DOCS_DIR / "data.json"
DERIVED_DIR = DOCS_DIR / "derived"
REFERENCE_DIR = DOCS_DIR / "reference"
RECON_DIR = DOCS_DIR / "recon"
REPORTS_DIR = DOCS_DIR / "reports"
SIM_DIR = DOCS_DIR / "simulations"

# Topical sub-dirs of docs/reports/.
REPORTS_COMBAT_DIR  = REPORTS_DIR / "combat"
REPORTS_ECONOMY_DIR = REPORTS_DIR / "economy"
REPORTS_TECH_DIR    = REPORTS_DIR / "tech"
REPORTS_MAP_DIR     = REPORTS_DIR / "map"
REPORTS_NATIONS_DIR = REPORTS_DIR / "nations"

# Backwards-compat aliases (some old imports may still reference these names).
OUTPUT_DIR = DOCS_DIR
STRATEGY_DIR = REPORTS_DIR

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
RESOURCE_NAMES_RU = {
    "food": "еда", "wood": "дерево", "stone": "камень",
    "gold": "золото", "iron": "железо", "coal": "уголь",
}

WEAPON_KIND_NAMES = {
    "gc_obj_weapon_kind_pike": "pike",
    "gc_obj_weapon_kind_sword": "sword",
    "gc_obj_weapon_kind_bullet": "bullet",
    "gc_obj_weapon_kind_arrow": "arrow",
    "gc_obj_weapon_kind_cannonball": "cannonball",
    "gc_obj_weapon_kind_cannister": "cannister",
}

# Russian labels for `gc_obj_weapon_kind_*` taken from
# `data/locale/ru/gui.txt @unitpanel.hint.damage.weaponkind.*` (verified 2026-04-30).
WEAPON_KIND_RU = {
    "sword":      "меч",          # gui.weaponkind.0 = "Атака мечом"
    "pike":       "пика",         # gui.weaponkind.1 = "Атака пикой"
    "bullet":     "пуля",         # gui.weaponkind.2 = "Сила выстрела"
    "arrow":      "стрелы",       # gui.weaponkind.3 = "Стрелы"
    "cannonball": "ядро",         # gui.weaponkind.4 = "Урон от ядер"
    "cannister":  "картечь",      # gui.weaponkind.5 = "Урон от картечи"
    "firearrow":  "огненная стрела",  # gui.weaponkind.6 = "Огненные стрелы"
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


# Upgrade type decoder (dmscript.global:737-764).
# Tuple: (numeric_id, short_label_en, description_en, short_label_ru).
UPG_TYPE_DECODE = {
    "gc_upg_type_none": (0, "—", "", "—"),
    "gc_upg_type_lifeperc": (1, "HP %", "Health % bonus", "+HP %"),
    "gc_upg_type_damage": (2, "+damage", "Adds flat damage to specific weapon kind", "+урон"),
    "gc_upg_type_damageperc": (3, "+damage %", "Damage % bonus", "+урон %"),
    "gc_upg_type_protection": (4, "+protection", "Adds flat protection vs weapon kinds", "+защита"),
    "gc_upg_type_shield": (5, "+shield", "Shield bonus (negates damage up to N)", "+щит"),
    "gc_upg_type_enableunit": (6, "enable unit", "Unlocks a unit/building", "разблокировка"),
    "gc_upg_type_effectfood": (7, "+food eff %", "Adds X% to food extraction efficiency", "+эффект. еды %"),
    "gc_upg_type_effectfoodperc": (8, "+food eff %", "Adds X% to food extraction efficiency", "+эффект. еды %"),
    "gc_upg_type_effectwood": (9, "+wood eff %", "Adds X% to wood extraction efficiency", "+эффект. дерева %"),
    "gc_upg_type_effectwoodperc": (10, "+wood eff %", "Adds X% to wood extraction efficiency", "+эффект. дерева %"),
    "gc_upg_type_effectstone": (11, "+stone eff %", "Adds X% to stone extraction efficiency", "+эффект. камня %"),
    "gc_upg_type_effectstoneperc": (12, "+stone eff %", "Adds X% to stone extraction efficiency", "+эффект. камня %"),
    "gc_upg_type_priceperc": (13, "price %", "Modifies unit/building price by %", "цена %"),
    "gc_upg_type_buildtimeperc": (14, "build time %", "Modifies build time by %", "время постройки %"),
    "gc_upg_type_attpauseperc": (15, "reload %", "Modifies attack pause (lower = faster)", "перезарядка %"),
    "gc_upg_type_attrangeperc": (16, "range %", "Modifies attack range %", "дальность %"),
    "gc_upg_type_attdispertionperc": (17, "accuracy %", "Modifies dispersion (lower = more accurate)", "точность %"),
    "gc_upg_type_healing": (18, "healing", "Heals all units (one-time)", "лечение"),
    "gc_upg_type_fishingperc": (19, "+fish eff %", "Increases boat fish capacity", "+рыбалка %"),
    "gc_upg_type_geology": (20, "geology", "Reveals hidden mineral deposits", "геология"),
    "gc_upg_type_balloon": (21, "balloon", "Reveals whole map (Montgolfier)", "монгольфьер"),
    "gc_upg_type_speedperc": (22, "speed %", "Movement speed %", "скорость %"),
    "gc_upg_type_fieldlifeperc": (23, "+field HP %", "Adds X to fieldlife (HP/hit reduction)", "+живучесть поля"),
    "gc_upg_type_single_inside": (24, "+building capacity", "Increases building peasant capacity", "+вместимость здания"),
    "gc_upg_type_single_inside_mine": (25, "+mine workers", "Adds X workers to mine capacity (per mine)", "+рабочих в шахту"),
    "gc_upg_type_single_attpauseperc": (26, "single reload %", "Per-building attack pause %", "перезарядка здания %"),
    "gc_upg_type_single_buildgate": (27, "build gate", "Allows wall→gate conversion", "ворота из стены"),
}


def decode_upg_type(itype_str, lang: str = "en") -> tuple[str, str]:
    """Return (short_name, description) for a gc_upg_type_* identifier or numeric ID.

    lang='ru' returns the Russian short label; description stays English.
    """
    if not itype_str:
        return ("", "")
    s = str(itype_str).strip()
    short_idx = 3 if lang == "ru" else 1
    if s in UPG_TYPE_DECODE:
        tup = UPG_TYPE_DECODE[s]
        return (tup[short_idx], tup[2])
    try:
        n = int(s)
        for name, tup in UPG_TYPE_DECODE.items():
            if tup[0] == n:
                return (tup[short_idx], tup[2])
    except (ValueError, TypeError):
        pass
    return (s, "")  # unknown


# Object usage decoder (dmscript.global:307-339).
# Tuple: (numeric_id, label_en, label_ru).
USAGE_DECODE = {
    "gc_obj_usage_none":          (0,  "—",                  "—"),
    "gc_obj_usage_mill":          (1,  "Mill",               "Мельница"),
    "gc_obj_usage_farm":          (2,  "Housing/Farm",       "Дом"),
    "gc_obj_usage_center":        (3,  "Town Hall",          "Городской центр"),
    "gc_obj_usage_storage":       (4,  "Storehouse",         "Склад"),
    "gc_obj_usage_tower":         (5,  "Tower",              "Башня"),
    "gc_obj_usage_field":         (6,  "Field",              "Поле"),
    "gc_obj_usage_mine":          (7,  "Mine",               "Шахта"),
    "gc_obj_usage_fasthorse":     (8,  "Light Cavalry",      "Лёгкая кавалерия"),
    "gc_obj_usage_mortar":        (9,  "Mortar",             "Мортира"),
    "gc_obj_usage_cannon":        (10, "Cannon",             "Пушка"),
    "gc_obj_usage_grenadier":     (11, "Grenadier",          "Гренадёр"),
    "gc_obj_usage_hardwall":      (12, "Stone Wall/Gate",    "Каменная стена/ворота"),
    "gc_obj_usage_weakwall":      (13, "Wood Wall/Gate",     "Деревянная стена/ворота"),
    "gc_obj_usage_battleship":    (14, "Battleship",         "Линейный корабль"),
    "gc_obj_usage_weak":          (15, "Weak unit",          "Слабый юнит"),
    "gc_obj_usage_fisher":        (16, "Fishing Boat",       "Рыбацкая лодка"),
    "gc_obj_usage_artdepo":       (17, "Artillery Depot",    "Артиллерийское депо"),
    "gc_obj_usage_supermortar":   (18, "Super Mortar",       "Сверхмортира"),
    "gc_obj_usage_port":          (19, "Shipyard",           "Порт"),
    "gc_obj_usage_lightinfantry": (20, "Light Infantry",     "Лёгкая пехота"),
    "gc_obj_usage_shooter":       (21, "Shooter",            "Стрелок"),
    "gc_obj_usage_hardhorse":     (22, "Heavy Cavalry",      "Тяжёлая кавалерия"),
    "gc_obj_usage_peasant":       (23, "Peasant",            "Крестьянин"),
    "gc_obj_usage_horseshooter":  (24, "Mounted Shooter",    "Конный стрелок"),
    "gc_obj_usage_frigate":       (25, "Frigate",            "Фрегат"),
    "gc_obj_usage_galley":        (26, "Galley",             "Галера"),
    "gc_obj_usage_yacht":         (27, "Yacht",              "Яхта"),
    "gc_obj_usage_xebec":         (28, "Xebec",              "Шебека"),
    "gc_obj_usage_transport":     (29, "Transport",          "Транспорт"),
    "gc_obj_usage_archer":        (30, "Archer",             "Лучник"),
    "gc_obj_usage_mcannon":       (31, "Multi-cannon",       "Многоствольная пушка"),
    "gc_obj_usage_dipcenter":     (32, "Diplomatic Center",  "Дипломатический центр"),
}

# Map English `usage_short` (as stored in data.json) → Russian label.
USAGE_RU = {tup[1]: tup[2] for tup in USAGE_DECODE.values()}


def decode_usage(usage_str, lang: str = "en") -> str:
    """Convert gc_obj_usage_* identifier (or numeric ID) to human-readable name.

    lang='ru' returns the Russian label.
    """
    if not usage_str:
        return ""
    s = str(usage_str).strip()
    idx = 2 if lang == "ru" else 1
    if s in USAGE_DECODE:
        return USAGE_DECODE[s][idx]
    try:
        n = int(s)
        for name, tup in USAGE_DECODE.items():
            if tup[0] == n:
                return tup[idx]
    except (ValueError, TypeError):
        pass
    return s


def usage_ru(usage_short: str | None) -> str:
    """Translate an English `usage_short` (as stored in data.json) to Russian.
    Falls back to the input when no mapping exists."""
    if not usage_short:
        return "—"
    return USAGE_RU.get(usage_short, usage_short)


# =============================================================================
# Russian display names — single source of truth
# =============================================================================
# Loaded from `docs/derived/canonical_terms.json` (generated from game locale by
# `parser/build_canonical_terms.py`). All writers and compute scripts that emit
# Russian text MUST use these maps — never hard-code translations.

NATION_NAMES_RU: dict[str, str] = {}
NATION_NAMES_EN: dict[str, str] = {}
BUILDING_NAMES_RU: dict[str, str] = {}  # by suffix: 'cen' → 'Городской центр'
BUILDING_NAMES_EN: dict[str, str] = {}

_CANON_FALLBACK_NATIONS_RU = {
    "aus": "Австрия", "fra": "Франция", "eng": "Англия", "spa": "Испания",
    "rus": "Россия",  "ukr": "Украина", "pol": "Польша", "swe": "Швеция",
    "pru": "Пруссия", "ven": "Венеция", "tur": "Турция", "alg": "Алжир",
    "net": "Нидерланды", "den": "Дания", "por": "Португалия", "pie": "Пьемонт",
    "sax": "Саксония", "bav": "Бавария", "hun": "Венгрия", "swi": "Швейцария",
    "sco": "Шотландия",
}
_CANON_FALLBACK_NATIONS_EN = {
    "aus": "Austria", "fra": "France", "eng": "England", "spa": "Spain",
    "rus": "Russia", "ukr": "Ukraine", "pol": "Poland", "swe": "Sweden",
    "pru": "Prussia", "ven": "Venice", "tur": "Turkey", "alg": "Algeria",
    "net": "Netherlands", "den": "Denmark", "por": "Portugal", "pie": "Piedmont",
    "sax": "Saxony", "bav": "Bavaria", "hun": "Hungary", "swi": "Switzerland",
    "sco": "Scotland",
}
_CANON_FALLBACK_BUILDINGS_RU = {
    "cen": "Городской центр", "bar": "Казарма 17в.", "ba2": "Казарма 18в.",
    "aca": "Академия", "art": "Артиллерийское депо", "bla": "Кузница",
    "dip": "Дипломатический центр", "hou": "Дом", "sta": "Конюшня",
    "tem": "Собор",
    "mar": "Рынок", "mil": "Мельница", "por": "Порт", "sto": "Склад",
    "tow": "Башня", "coa": "Шахта", "gol": "Шахта", "iro": "Шахта",
    "sga": "Каменные ворота", "wga": "Деревянные ворота",
    "swa": "Стена", "wwa": "Частокол",
}


def _load_canonical_terms() -> None:
    """Populate NATION_NAMES_*, BUILDING_NAMES_* from canonical_terms.json.

    Falls back to the hardcoded constants above when the file is missing
    (e.g., before the first run of `parser/build_canonical_terms.py`).
    """
    global NATION_NAMES_RU, NATION_NAMES_EN
    global BUILDING_NAMES_RU, BUILDING_NAMES_EN
    NATION_NAMES_RU = dict(_CANON_FALLBACK_NATIONS_RU)
    NATION_NAMES_EN = dict(_CANON_FALLBACK_NATIONS_EN)
    BUILDING_NAMES_RU = dict(_CANON_FALLBACK_BUILDINGS_RU)
    BUILDING_NAMES_EN = {}

    canon_path = DERIVED_DIR / "canonical_terms.json"
    if not canon_path.exists():
        return
    try:
        canon = json.loads(canon_path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return

    for sid, names in (canon.get("nations") or {}).items():
        if names.get("ru"):
            NATION_NAMES_RU[sid] = names["ru"]
        if names.get("en"):
            NATION_NAMES_EN[sid] = names["en"]
    for suffix, names in (canon.get("buildings") or {}).items():
        if names.get("ru"):
            BUILDING_NAMES_RU[suffix] = names["ru"]
        if names.get("en"):
            BUILDING_NAMES_EN[suffix] = names["en"]


_load_canonical_terms()


def nation_ru(sid: str) -> str:
    """Russian name for a nation sid; falls back to the sid itself."""
    return NATION_NAMES_RU.get(sid, sid)


def nation_en(sid: str) -> str:
    """English name for a nation sid; falls back to the sid itself."""
    return NATION_NAMES_EN.get(sid, sid)


def nation_label(sid: str, *, en: bool = True, ru: bool = True) -> str:
    """`AUS — Австрия` style header label. Use in cheatsheet headings."""
    parts = [sid.upper()]
    if en and sid in NATION_NAMES_EN:
        parts.append(NATION_NAMES_EN[sid])
    if ru and sid in NATION_NAMES_RU:
        ru_name = NATION_NAMES_RU[sid]
        if en and sid in NATION_NAMES_EN:
            return f"{sid.upper()} — {NATION_NAMES_EN[sid]} ({ru_name})"
        return f"{sid.upper()} — {ru_name}"
    return parts[0]


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
# Empirical guesses — UNVERIFIED in scripts (see recon/peasant_extraction.md §9)
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
