"""Generate a structured markdown tree under output/reference/.

Tree:
    reference/
    ├── README.md                  # TL;DR + index + key formulas
    ├── 01_economy.md              # extraction, portions, eff, mines, fields
    ├── 02_combat.md               # damage formula, speeds, formations
    ├── 03_buildings.md            # all buildings (overview tables per type)
    ├── 04_units.md                # all units grouped by class
    ├── 05_upgrades.md             # all upgrades grouped by place
    ├── 06_market.md               # trade rates + examples
    ├── nations/
    │   ├── README.md              # nation overview + comparison table
    │   └── <nat>.md × 21          # per-nation cheatsheets
    └── compare/
        ├── README.md
        ├── pikemen.md / musketeers.md / cavalry.md / siege.md
        ├── ships.md / peasants.md / town_halls.md / barracks.md
"""
from __future__ import annotations
import sys, json, re
sys.stdout.reconfigure(encoding="utf-8")
from pathlib import Path
from collections import defaultdict

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "parser"))
from config import (OUTPUT_DIR, PLAYABLE_NATIONS, _commonname, DATA_JSON, REFERENCE_DIR,
                    MELEE_SWING_FALLBACK_SEC, melee_swing_sec)

DATA_PATH = DATA_JSON
TREE_ROOT = REFERENCE_DIR


# ---------- helpers ----------

def fmt(v, default="—"):
    if v is None or v == "":
        return default
    if v == 0 and isinstance(v, int):
        return "0"
    return str(v)


def fmt_cost(row, keys=("food", "wood", "stone", "gold", "iron", "coal")):
    parts = []
    for k in keys:
        v = row.get(k)
        if v not in (None, 0):
            parts.append(f"{k[0].upper()}{v}")
    return " ".join(parts) if parts else "—"


def write_md(path: Path, lines: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")


def heading_anchor(text: str) -> str:
    """Convert heading text to a slug for cross-linking (GitHub-flavored MD style)."""
    s = text.lower()
    s = re.sub(r"[^\w\s\-—.()]+", "", s)
    s = re.sub(r"\s+", "-", s.strip())
    s = s.replace("(", "").replace(")", "").replace(".", "")
    return s


# ---------- formatting helpers ----------

def name_cell_short(item: dict) -> str:
    """Compact name cell for compare/ tables: `**RU name** ` `sid` `; falls back to EN if RU missing."""
    name_ru = (item.get("name_ru") or "").strip()
    name_en = (item.get("name_en") or "").strip()
    sid = item.get("sid", "")
    display = name_ru or name_en
    if display:
        return f"**{display}** `{sid}`"
    return f"`{sid}`"


def name_ru_en(item: dict) -> str:
    """Russian name from locale, fallback to English, fallback to em-dash."""
    ru = (item.get("name_ru") or "").strip()
    en = (item.get("name_en") or "").strip()
    return ru or en or "—"


def name_cell_full(item: dict) -> str:
    """Full name cell for nation cheatsheets: shows RU + EN + sid.
    Format: **<RU>** / <EN> · `<sid>`. Falls back if a name is empty."""
    sid = item.get("sid", "")
    en = (item.get("name_en") or "").strip()
    ru = (item.get("name_ru") or "").strip()
    parts = []
    if ru and ru != en:
        parts.append(f"**{ru}**")
        if en:
            parts.append(f"/ {en}")
    elif en:
        parts.append(f"**{en}**")
    parts.append(f"`{sid}`")
    return " ".join(parts)


def compute_baselines(rows: list[dict], cols: list[str]) -> dict:
    """For each column, compute the mode (most common value).
    Used to highlight per-row deviations in compare/ tables."""
    from collections import Counter
    out = {}
    for col in cols:
        vals = [r.get(col) for r in rows if r.get(col) is not None]
        if not vals:
            out[col] = None
            continue
        c = Counter(vals)
        # Mode = most common; tie-breaker keeps the first encountered
        out[col] = c.most_common(1)[0][0]
    return out


def bold_if(value, baseline) -> str:
    """Format value, bolding it if it differs from baseline.
    Empty/None values are rendered as '—' without bold."""
    if value is None or value == "":
        return "—"
    s = str(value)
    if baseline is not None and value != baseline:
        return f"**{s}**"
    return s


def make_toc(headings: list[tuple[int, str]]) -> list[str]:
    """Build a TOC: list of (level, heading_text). Returns markdown lines.
    Level 2 = top-level entry, level 3 = sub-bullet."""
    out = []
    for lvl, text in headings:
        anchor = heading_anchor(text)
        indent = "  " * (lvl - 2) if lvl > 2 else ""
        out.append(f"{indent}- [{text}](#{anchor})")
    return out


# ---------- unit classification ----------

# Map of internal class keys → user-facing Russian labels. Internal keys stay
# English (used as dict keys in lookups), but anything rendered to MD goes
# through CLASS_RU.
CLASS_RU = {
    "Peasant":               "Крестьяне",
    "Officer":               "Офицеры",
    "Drummer / Bagpiper":    "Барабанщики / волынщики",
    "Priest":                "Священники",
    "Pikemen 17c":           "Пикинёры (17 в.)",
    "Pikemen 18c":           "Пикинёры (18 в.)",
    "Musketeers 17c":        "Мушкетёры (17 в.)",
    "Musketeers 18c":        "Мушкетёры (18 в.)",
    "Grenadiers":            "Гренадёры",
    "Light Infantry":        "Лёгкая пехота",
    "Archers":               "Лучники",
    "18c special infantry":  "Особая пехота (18 в.)",
    "Light Cavalry":         "Лёгкая кавалерия",
    "Dragoons":              "Драгуны",
    "Heavy Cavalry":         "Тяжёлая кавалерия",
    "Cannons":               "Пушки",
    "Mortars":               "Мортиры",
    "Fishing Boat":          "Рыбацкие лодки",
    "Warships":              "Военные корабли",
    "Misc / mission":        "Прочее / миссии",
    "Other":                 "Прочее",
}

# Map of `usage_short` (from data.json — values that come from the game's
# `gc_obj_usage_*` constants) → Russian label for in-table display.
USAGE_RU = {
    "Peasant":          "Крестьянин",
    "Officer":          "Офицер",
    "Priest":           "Священник",
    "Drummer":          "Барабанщик",
    "Bagpiper":         "Волынщик",
    "Pikeman":          "Пикинёр",
    "Musketeer":        "Мушкетёр",
    "Grenadier":        "Гренадёр",
    "Archer":           "Лучник",
    "Light Infantry":   "Лёгкая пехота",
    "Light Infantryman": "Лёгкий пехотинец",
    "Shooter":          "Стрелок",
    "Light Cavalry":    "Лёгкая кавалерия",
    "Heavy Cavalry":    "Тяжёлая кавалерия",
    "Mounted Shooter":  "Конный стрелок",
    "Dragoon":          "Драгун",
    "Cannon":           "Пушка",
    "Mortar":           "Мортира",
    "Super Mortar":     "Сверхмортира",
    "Multi-cannon":     "Многоствольная пушка",
    "Fisher":           "Рыболов",
    "Fishing Boat":     "Рыбацкая лодка",
    "Yacht":            "Яхта",
    "Galley":           "Галера",
    "Frigate":          "Фрегат",
    "Xebec":            "Шебека",
    "Battleship":       "Линейный корабль",
    "Ferry":            "Паром",
}


def cls_ru(cls: str) -> str:
    """Russian label for a classify_unit() class key. Falls back to the key."""
    return CLASS_RU.get(cls, cls)


def usage_ru(usage_short: str | None) -> str:
    """Russian label for a unit's usage_short. Falls back to the input."""
    if not usage_short:
        return "—"
    return USAGE_RU.get(usage_short, usage_short)


def classify_unit(sid: str, usage_short: str) -> str:
    """Return a coarse class for grouping in compare/ and 04_units.md."""
    s = sid.lower()
    if s.startswith("pea"):
        return "Peasant"
    if s in ("officer", "officerrus", "officertur", "officersco", "officer18"):
        return "Officer"
    if s in ("drummer", "drummerrus", "drummertur", "drummer18", "bagpiper"):
        return "Drummer / Bagpiper"
    if s in ("priest", "padre", "pope", "mullah"):
        return "Priest"
    if s.startswith("pikeman18"):
        return "Pikemen 18c"
    if s.startswith("pikeman"):
        return "Pikemen 17c"
    if s.startswith("musketeer18"):
        return "Musketeers 18c"
    if s.startswith("musketeer") or s in ("strelet","jannisary","serdiuk","gauduk"):
        return "Musketeers 17c"
    if s.startswith("grenadier"):
        return "Grenadiers"
    if s in ("lightinfantry","lightinfantrydip","roundshier","roundshierdip","swordsmansco"):
        return "Light Infantry"
    if s.startswith("archer"):
        return "Archers"
    if s in ("highlander","pandur","pandurhun","chasseur","jagerpor","jagerswi"):
        return "18c special infantry"
    if s in ("hussar","hussarpru","hussarhun","hussarswi","hussar18","hetman","croat",
              "lightcavalry","lightcavalrydip","raidersco","lancersco"):
        return "Light Cavalry"
    if s in ("dragoon","dragoonpol","dragoon18","dragoon18fra","dragoon18net","dragoon18pie","dragoon18dip"):
        return "Dragoons"
    if s in ("reiter","reiterpol","reiterswe","kingmusketeer","wingedhussar","vityaz",
              "cossacksich","cossacksichdip","cossackdon","cossackregister",
              "spakh","mameluke","tatar","sipahi","cuirassier","guardcavalrysax","hackapell"):
        return "Heavy Cavalry"
    if s in ("cannon","framegun","multicannon"):
        return "Cannons"
    if s in ("mortar","howitzer","supermortar"):
        return "Mortars"
    if s in ("fishboat",):
        return "Fishing Boat"
    if s in ("yacht","yachttur","galley","frigate","xebec","battleship","chaika","brigantine","galleon","ferry","sloop"):
        return "Warships"
    if s in ("misdonkey","misflagman","misgeneral","mistrader","unitbox","field","null"):
        return "Misc / mission"
    if usage_short:
        return f"Other ({usage_short})"
    return "Other"


# ---------- README.md ----------

def write_readme(data: dict) -> None:
    out = []
    A = out.append
    e = data["economy"]
    A("# Cossacks 3 Reference\n")
    banner = _version_banner(data)
    if banner:
        A(banner + "\n")
    A("Полный справочник по экономике, юнитам, зданиям и апгрейдам игры Cossacks 3, "
      "извлечённый напрямую из файлов игры в "
      "`C:\\Program Files (x86)\\Steam\\steamapps\\common\\Cossacks 3\\data\\scripts\\`.\n")
    A("Парсер: `parser/` (запусти `python parser/build_data.py && "
      "python writers/write_md_tree.py` после патча игры).\n")
    A("---\n")
    A("## TL;DR — главные цифры\n")
    A(f"- **Время:** `gc_time_to_frames = {e['time_to_frames']}` (32 кадра / игр-сек). "
      f"Game speeds: slow=`{e['gamespeed_slow']}`, normal=`{e['gamespeed_normal']}`, fast=`{e['gamespeed_fast']}` тиков/сек.")
    A(f"- **Pixels-to-tile:** `{e['pixels_to_tile']:.4f}`. Радиус 800 px = 15 тайлов.")
    A(f"- **Лимиты:** {e['max_obj_count']} объектов на карте, {e['max_player_count']} игроков.")
    A(f"- **Поле:** HP = {e['field_max_hp']}. Шахта (база): 5 крестьян → 1.664 ресурса/игр-сек на крестьянина.")
    A("")
    A("### Базовая добыча\n")
    A("| Ресурс | Порция за рейс | Hits перед сдачей | Real rate (1 крестьянин, eff=100) |")
    A("|---|---:|---:|---:|")
    A(f"| food (еда) | **{e['resource_portion_food']}** | {e['hits_needed_food']} | "
      f"≈ 2.97 / игр-сек (без дороги к складу) |")
    A(f"| wood | **{e['resource_portion_wood']}** | {e['hits_needed_wood']} | ≈ 3.56 / игр-сек |")
    A(f"| stone | **{e['resource_portion_stone']}** | {e['hits_needed_stone']} | ≈ 3.56 / игр-сек |")
    A(f"| gold/iron/coal | **{e['resource_portion_others']}** (хардкод) | n/a | через шахту: 1.664 / крестьянин / игр-сек |")
    A("")
    A("**Формула:** `delivered = (portion × eff) / 100`  (целочисл. деление). "
      "`eff` стартует со 100, апгрейды добавляют **аддитивно**.\n")
    A("### Боевая формула\n")
    A("```")
    A("applied = max(1, weapon.damage")
    A("                 - target.shield               # /3 if target is being built")
    A("                 - target.protection[kind]")
    A("                 + squad bonuses")
    A("                 + HEADSHOT: +floor(uniqrnd × 500) at 5% chance (arrow/bullet vs non-buildings))")
    A("```")
    A("**Минимум 1 хп**. Хедшот = 5% шанс на каждый bullet/arrow выстрел против любого "
      "юнита (кроме light-cavalry-в-движении) даёт **до +499** бонусного урона. См. подробности "
      "в [02_combat.md → Хедшот](02_combat.md#хедшот-критический-удар--главная-скрытая-механика). "
      "Источник: `miscext2.script:_misc_DoDamage`.\n")
    A("### Цена N-го здания того же типа\n")
    A("`cost(N) = floor(base_cost × (costpercent/100)^(N-1))`. См. "
      "[derived/scaling_prices.md](derived/scaling_prices.md).\n")
    A("---\n")
    A("## Где что искать\n")
    A("### Главы справочника (этот каталог)\n")
    A("| Хочу узнать… | Открой |")
    A("|---|---|")
    A("| Формулы добычи и цикл крестьянина | [01_economy.md](01_economy.md) |")
    A("| Формула урона, защиты, скорости, формации | [02_combat.md](02_combat.md) |")
    A("| Все здания (общие + per-nation) | [03_buildings.md](03_buildings.md) |")
    A("| Все юниты по классам | [04_units.md](04_units.md) |")
    A("| Все апгрейды по местам | [05_upgrades.md](05_upgrades.md) |")
    A("| Курсы рынка и примеры обмена | [06_market.md](06_market.md) |")
    A("| Что уникального у нации X | [nations/](nations/README.md) |")
    A("| Сравнить юнитов одного класса | [compare/](compare/README.md) |")
    A("")
    A("### Производные файлы (расчётные, на основе data.json)\n")
    A("В подкаталоге [`derived/`](derived/):\n")
    A("| Файл | Что внутри |")
    A("|---|---|")
    A("| [derived/scaling_prices.md](derived/scaling_prices.md) | Стоимости 2-го, 3-го, …N-го здания. Формула `cost(N) = floor(base × (costpercent/100)^(N-1))` |")
    A("| [derived/map_resources.md](derived/map_resources.md) | Подсчёт ресурсов на карте Tiny (256×256) + Highlands + Rich: ~109 больших деревьев, ~115 средних, ~72 маленьких; ~33 камня; до 12 шахт на игрока |")
    A("")
    A("### Сырой источник\n")
    A("| Файл | Что |")
    A("|---|---|")
    A("| [../data.json](../data.json) | Сырой JSON (~4.7 MB) — вход для всех writer-скриптов. Регенерируется через `python parser/build_data.py`. |")
    A("")
    A("### Глубокие исследования (recon/)\n")
    A("| Файл | Тема |")
    A("|---|---|")
    A("| [../../recon/peasant_extraction.md](../../recon/peasant_extraction.md) | Полный разбор механики добычи: цикл крестьянина, animation frames, walk speed, fieldlife регенерация, спавн ресурсов |")
    A("| [../../recon/extraction_formulas.md](../../recon/extraction_formulas.md) | Краткая формульная сводка для расчётов (game-time vs real-time, fast×1.4) |")
    A("| [../../recon/empirical_tests.md](../../recon/empirical_tests.md) | Открытые вопросы для эмпирической проверки (скорость крестьянина, animation frame rate, brised флаг для пней) |")
    A("| [../../recon/step1_findings.md](../../recon/step1_findings.md) | Исторический recon: исходное обнаружение структуры файлов игры (можно пропустить) |")
    A("")
    A("## Расхождения с заметками из промпта\n")
    A("(детали в [01_economy.md#discrepancies](01_economy.md))")
    A("| Факт | Заметки | Файл |")
    A("|---|---|---|")
    for d in data.get("discrepancies", []):
        A(f"| {d['fact']} | {d['user_note']} | **{d['file_value']}** |")
    A("")
    sanity = data.get("sanity_checks", [])
    n_pass = sum(1 for c in sanity if c["pass"])
    A(f"## Sanity checks: **{n_pass}/{len(sanity)} PASS**\n")
    A("Полный список и категории — в xlsx-листе `Sanity_checks` или [01_economy.md](01_economy.md#sanity).\n")
    A("---\n")
    A("## Стат по объёмам\n")
    A(f"- **Нации:** {len(data['nations'])}")
    A(f"- **Здания:** {len(data['buildings'])} строк (sid×nation)")
    A(f"- **Юниты:** {len(data['units'])} строк")
    A(f"- **Апгрейды:** {len(data['upgrades'])} строк")
    A(f"- **Офицеры/формации:** {len(data.get('officers', []))} групп")
    A("")
    A("## Принципы справочника\n")
    A("1. **Источник истины — файлы игры.** Если что-то расходится с внешними калькуляторами/гайдами — "
      "доверяй файлу. Расхождения задокументированы в `discrepancies`.")
    A("2. **Идемпотентность.** `python build_data.py && python write_xlsx.py && python write_md_tree.py` "
      "перегенерирует всё с нуля.")
    A("3. **Sanity checks.** 100+ автопроверок ловят регрессии после игровых патчей.")
    A("4. **Нет ручных правок.** Если хочешь подкрутить — правь скрипты в `parser/`, не сами md.")

    write_md(TREE_ROOT / "README.md", out)


# ---------- 01_economy.md ----------

def write_economy(data: dict) -> None:
    out = []
    A = out.append
    e = data["economy"]
    A("# 01. Экономика\n")
    A("[← Index](README.md)\n")
    A("> **Глубокие исследования по этой главе:**\n"
      "> - [`../../recon/peasant_extraction.md`](../../recon/peasant_extraction.md) — "
      "полный разбор цикла крестьянина, animation frames, walk speed, fieldlife регенерация\n"
      "> - [`../../recon/extraction_formulas.md`](../../recon/extraction_formulas.md) — "
      "формульная сводка для расчётов (game-time vs real-time)\n"
      "> - [`derived/map_resources.md`](derived/map_resources.md) — подсчёт "
      "ресурсов на карте Tiny+Highlands+Rich (~109 больших деревьев, ~33 камня, до 12 шахт/игрок)\n"
      "> - [`../../recon/empirical_tests.md`](../../recon/empirical_tests.md) — "
      "открытые вопросы для эмпирической проверки (скорость крестьянина, frame rate)\n")
    A("\n## Резюме\n")
    A("Один крестьянин за рейс приносит `delivered = (portion × eff) / 100`. Eff стартует со 100, "
      "апгрейды накапливаются аддитивно. Шахты работают по другой схеме: каждый крестьянин внутри "
      "добавляет 13 к `gPlayer.counter.resincome`, реальная скорость = 1.664 ресурса/игр-сек.\n")
    A("## Глобальные константы\n")
    A("| Параметр | Значение | Источник |")
    A("|---|---:|---|")
    A(f"| `gc_time_to_frames` | {e['time_to_frames']} | dmscript.global:175 |")
    A(f"| `gc_pixels_to_tile` | {e['pixels_to_tile']:.4f} | dmscript.global:172 |")
    A(f"| `gc_settings_gamespeed_0` (slow) | {e['gamespeed_slow']} тиков/сек | dmscript.global:1027 |")
    A(f"| `gc_settings_gamespeed_1` (normal) | {e['gamespeed_normal']} | dmscript.global:1028 |")
    A(f"| `gc_settings_gamespeed_2` (fast) | {e['gamespeed_fast']} | dmscript.global:1029 |")
    A(f"| `gc_MaxObjCount` | {e['max_obj_count']} | dmscript.global:110 |")
    A(f"| `gc_MaxPlayerCount` | {e['max_player_count']} | dmscript.global:97 |")
    A(f"| `gc_FieldMaxHP` | {e['field_max_hp']} | dmscript.global:128 |")
    A(f"| `gc_obj_foodperunit` | {e['food_per_unit_upkeep']} food / юнит | dmscript.global:808 |")
    A(f"| Default `eff` | {e['default_eff_percent']}% | player.script:109 |")
    A("")
    A("## Базовые порции и hits\n")
    A("| Ресурс | Базовая порция | Hits | Источник |")
    A("|---|---:|---:|---|")
    A(f"| food | **{e['resource_portion_food']}** | {e['hits_needed_food']} | dmscript.global:799,804 |")
    A(f"| wood | **{e['resource_portion_wood']}** | {e['hits_needed_wood']} | dmscript.global:800,805 |")
    A(f"| stone | **{e['resource_portion_stone']}** | {e['hits_needed_stone']} | dmscript.global:801,806 |")
    A(f"| gold/iron/coal/прочее | **{e['resource_portion_others']}** | n/a | unit.script:9551 (хардкод) |")
    A("")
    A("## Формула добычи\n")
    A("```")
    A("delivered = (base_portion × eff) / 100   # integer division")
    A("```")
    A("Пример: с апгрейдами academy.1 (+40% food) и mill.1 (+140% food) → `eff = 100 + 40 + 140 = 280`. "
      "Крестьянин приносит `45 × 280 / 100 = 126` еды за рейс (вместо базовых 45).\n")
    A("Все апгрейды eff — в `player.script:1813-1828`. Список → [05_upgrades.md](05_upgrades.md#economy-eff).\n")
    A("## Шахты (gold/iron/coal)\n")
    A("Шахта: HP=2500, buildtime=300 frames=9.38s, цена W100/S100, `peasantabsorber=5` (5 крестьян макс. база). "
      "Каждый крестьянин внутри добавляет к `produce[restype] = 13`.\n")
    A("**Расчёт:**\n")
    A("```")
    A("bank_per_sec = 13 × 32 = 416  # (per peasant per game-sec)")
    A("real_per_sec = 416 / 250 ≈ 1.664  # ресурса в игр-секунду")
    A("real_per_min = 99.84  # ≈ 100 ресурса/игр-мин/крестьянин")
    A("```")
    A("**Полная прокачка одной шахты** (6 апгрейдов):\n")
    A("| Уровень | +работников | F | G | Накопительно |")
    A("|---:|---:|---:|---:|---:|")
    cumulative = 5
    mine_ups = sorted([u for u in data["upgrades"]
                       if u["sid"].startswith("eurgol.") and u["nation"] == "aus"],
                       key=lambda x: x["sid"])
    for u in mine_ups:
        cumulative += u.get("value") or 0
        A(f"| {u['sid']} | +{u['value']} | {u['food']} | {u['gold']} | {cumulative} |")
    A(f"\n**Итого:** 5 базовых + 6 апгрейдов = **{cumulative} крестьян/шахта = "
      f"{cumulative * 1.664:.1f} ресурса/игр-сек = {cumulative * 99.84:.0f} / игр-мин**.\n")
    total_food_cost = sum(u['food'] for u in mine_ups)
    total_gold_cost = sum(u['gold'] for u in mine_ups)
    A(f"**Стоимость полной прокачки одной шахты:** F{total_food_cost:,} + G{total_gold_cost:,}.\n")
    A("## Поле (food, fieldlife, регенерация)\n")
    A(f"HP поля = `gc_FieldMaxHP = {e['field_max_hp']}`. Урон полю за удар: `resdec = max(1, floor(100/(1+fieldlife/100)))`.\n")
    A("| fieldlife | resdec/удар | Макс. ударов | Макс. food при eff=100 |")
    A("|---:|---:|---:|---:|")
    for fl in (0, 100, 200, 300, 500):
        resdec = max(1, 100 // (1 + fl // 100))
        max_hits = e['field_max_hp'] // resdec
        max_food = max_hits * e['resource_portion_food'] // e['hits_needed_food']
        A(f"| {fl} | {resdec} | {max_hits} | {max_food} |")
    A("\nАпгрейды fieldlife: `aca.4` (+200), `bla.1` (+100). Сумма = 300 → ~2045 food/поле.\n")
    A("## Корабли — fishing\n")
    A("`fishboat`: HP=300, цена W600, `fishingmax=1000` (база), `fishingspeed = 50/4 = 12` тиков на одну рыбу. "
      "Апгрейд `aca.5` (`+100% boat efficiency`) удваивает грузоподъёмность → **2000 food/рейс**. "
      "Апгрейд `aca.7` (`-85% fishing boat cost`) удешевляет постройку.\n")
    A("Полный список кораблей → [compare/ships.md](compare/ships.md).\n")
    A("## Famine (голод) и Rebellion (восстание)\n")
    A("Источник: [`unit.inc/nothing.inc:445-505`](file:///C:/Program%20Files%20(x86)/Steam/steamapps/common/Cossacks%203/data/scripts/units/unit.inc/nothing.inc), "
      "[`player.script:280-322`](file:///C:/Program%20Files%20(x86)/Steam/steamapps/common/Cossacks%203/data/scripts/lib/player.script)\n")
    A("**Upkeep:** все юниты без флага `bnohungry` потребляют food. Скорость потребления:\n")
    A("```")
    A("food_per_g_sec = consume × time_to_frames / 20000")
    A("                = consume × 32 / 20000  =  consume × 0.0016")
    A("```")
    A("Для типичного юнита `consume=30` (food per unit, `gc_obj_foodperunit=30`): "
      "**0.048 food/игр-сек = 2.88 food/игр-мин на юнит**.\n")
    A("**Famine flag** (`bfamine=True`): срабатывает когда `food=0` И есть consume>0.\n")
    A("При famine **юниты без `bnohungry` начинают умирать рандомно**. Шанс смерти "
      "за тик зависит от **сложности игрока** (`gPlayer.difficulty`):\n")
    A("| Difficulty | Шанс смерти за тик | Ожидаемое время до смерти 1 юнита |")
    A("|---|---:|---|")
    A("| 0 (easy) | `RandomInt < 5` ≈ 0.0076% | очень медленно (часы) |")
    A("| 1 (normal) | `RandomInt < 12` ≈ 0.018% | ~часы |")
    A("| 2+ (hard / very hard / impossible) | **`RandomInt < 50` ≈ 0.076%** | **минуты** (4-10× быстрее normal) |")
    A("\n**Кто иммунен к famine** (`bnohungry=True`):")
    A("- Все здания (`bbuilding=True`)")
    A("- Все наёмники (`bmercenary=True`) — у них свой триггер (см. Rebellion)")
    A("- Большинство peasant'ов (но НЕ все — `peatur` не имеет bnohungry)")
    A("- Корабли")
    A("- Officers / drummers / priests")
    A("\n**Famine также отключается** если игрок не задал в профиле `gProfile.bFamine=True` (опция).\n")
    A("---\n")
    A("**Rebellion flag** (`brebellion=True`): срабатывает когда `gold=0` И `consume[gold] > income[gold]`.\n")
    A("При rebellion **наёмники массово переходят на сторону нейтрала**:\n")
    A("| Difficulty | Шанс перехода за тик |")
    A("|---|---:|")
    A("| 0 (easy) | `RandomInt < 100` ≈ 0.15% |")
    A("| 1 (normal) | `RandomInt < 200` ≈ 0.3% |")
    A("| 2+ (hard+) | **`RandomInt < 6000` ≈ 9.2%** — буквально за секунды теряешь весь наёмный контингент |")
    A("\n**Стратегические выводы:**")
    A("- На **hard и выше** keeping food и gold > 0 — критически важно. Даже короткий простой = "
      "массовая смерть/дезертирство.")
    A("- На easy famine практически бутафория, можно играть без mill optimization.")
    A("- **Наёмники (`<unit>dip` суффикс) тратят gold упкип** — поэтому держать большую diplomatic "
      "армию = высокий gold income required.\n")
    A("---\n")
    A("**Гольд upkeep юнитов** (`consume[gold]`): в основном у стрелковых башен (port, tower) "
      "и наёмников. Стандартный pikeman/musketeer **gold НЕ потребляет** (только при стрельбе — "
      "weapon.cost[gold]).\n")
    A("## Discrepancies (расхождения с промпт-заметками)\n")
    A("| Факт | Заметки | В файле | Источник | Вердикт |")
    A("|---|---|---|---|---|")
    for d in data.get("discrepancies", []):
        A(f"| {d['fact']} | {d['user_note']} | **{d['file_value']}** | "
          f"{d['source']} | {d['verdict']} |")
    A("")
    A("## Sanity\n")
    A(f"Sanity checks: **{sum(1 for c in data.get('sanity_checks', []) if c['pass'])}/"
      f"{len(data.get('sanity_checks', []))}** PASS. См. xlsx → лист `Sanity_checks`.\n")
    write_md(TREE_ROOT / "01_economy.md", out)


# ---------- 02_combat.md ----------

def write_combat(data: dict) -> None:
    out = []
    A = out.append
    e = data["economy"]
    A("# 02. Бой и движение\n")
    A("[← Index](README.md)\n")
    A("## Содержание\n")
    A("- [Формула урона (полная)](#формула-урона)")
    A("- [Хедшот — критический удар](#хедшот-критический-удар--главная-скрытая-механика)")
    A("- [Формационные бонусы (LINE/SQUARE/KARE)](#формационные-бонусы)")
    A("- [Рассеяние выстрелов](#рассеяние--почему-выстрелы-промахиваются)")
    A("- [uniqrnd — индивидуальное случайное число юнита](#uniqrnd--индивидуальное-случайное-число-юнита)")
    A("- [AoE damage cap](#aoe-damage-cap--как-кучкование-защищает)")
    A("- [Высокая позиция (high ground)](#высокая-позиция-high-ground)")
    A("- [Score multipliers](#score-за-убийство)")
    A("- [Standground / bartprepare — режимы атаки](#standground--bartprepare--режимы-атаки)")
    A("- [RunAway — автоматический отход стрелков](#runaway--автоматический-отход-стрелков)")
    A("- [Дружественный огонь](#дружественный-огонь)")
    A("- [Переключение оружия по дистанции (картечь, штык, огненные стрелы)](#переключение-оружия-по-дистанции)")
    A("- [Штраф к дальности при движении (standtime)](#штраф-к-дальности-при-движении)")
    A("- [Бонус к дальности в покое (addradius)](#бонус-к-дальности-в-покое)")
    A("- [Захват юнитов](#захват-юнитов)")
    A("- [Лечение священниками](#лечение-священниками)")
    A("- [Shield /3 при недостроенном здании](#shield-3-при-недостроенном-здании)")
    A("- [Реакция ИИ — отряд переходит в атаку от одного удара](#реакция-ии--отряд-переходит-в-атаку-от-одного-удара)")
    A("- [Офицеры — миф о боевой ауре](#офицеры--миф-о-боевой-ауре)")
    A("- [Чего НЕТ в игре](#чего-нет-в-игре-подтверждённое-отсутствие)")
    A("- [Свойства формулы урона](#свойства-формулы-урона)")
    A("- [Типы оружия](#типы-оружия-gc_obj_weapon_kind_)")
    A("- [Скорости юнитов](#скорости-юнитов)")
    A("- [Офицеры и формации](#офицеры-и-формации)")
    A("- [Матрица контр-эффективности (приближённый TTK)](#матрица-контр-эффективности-приближённый-ttk)")
    A("- [Перекрёстная таблица: апгрейды × характеристики](#перекрёстная-таблица-апгрейды--характеристики)")
    A("- [Стоимость одного выстрела](#стоимость-одного-выстрела)")
    A("")
    A("## Формула урона\n")
    A("```")
    A("damage = weapon.damage")
    A("")
    A("# 1. Anti-headshot для мобильной кавалерии")
    A("if (target.usage == fasthorse AND target is on the move")
    A("    AND weapon.kind in {arrow, bullet}):")
    A("    damage -= 5  # 'penalty' shot — лёгкая кавалерия на ходу труднее ловится")
    A("")
    A("# 2. Shield (одно из главных свойств танков)")
    A("if (target.bbuilt):")
    A("    damage -= target.shield")
    A("else:  # ещё строится")
    A("    damage -= target.shield // 3")
    A("")
    A("# 3. Squad shield bonus (формация)")
    A("if (target in formation):")
    A("    damage -= squad.fAddShieldHold  (если hold-mode)")
    A("    damage -= squad.fAddShield      (иначе)")
    A("")
    A("# 4. Squad damage bonus у атакующего (формация)")
    A("if (attacker in formation AND weapon.kind != firearrow):")
    A("    damage += squad.fAddDamageHold  (если hold-mode)")
    A("    damage += squad.fAddDamage      (иначе)")
    A("")
    A("# 5. Protection")
    A("damage -= target.protection[weapon.kind]")
    A("")
    A("# 6. HEADSHOT — критический удар")
    A("bCanHeadShot = (weapon.kind in {arrow, bullet}) AND (target NOT building)")
    A("bHeadShot = bCanHeadShot AND (random < 0.05)  AND (NOT fast-cavalry-on-the-move)")
    A("if bHeadShot:")
    A("    damage += floor(attacker.uniqrnd * 500)  # +0..+499 hp бонусного урона!")
    A("")
    A("damage = max(1, damage)  # минимум 1 хп")
    A("target.hp -= damage")
    A("```")
    A("Источник: `miscext2.script:_misc_DoDamage` (строки 274-510).\n")
    A("### Хедшот (критический удар) — главная скрытая механика\n")
    A("**5% шанс на каждый выстрел** добавить `floor(uniqrnd × 500)` урона. "
      "Где `uniqrnd` — фиксированное случайное число юнита-стрелка [0..1].\n")
    A("**Ключевые свойства:**\n")
    A("- Работает только для **arrow** и **bullet** оружия.")
    A("- НЕ работает по **зданиям**.")
    A("- НЕ работает по **light cavalry на ходу** (`usage=fasthorse + state=walk`) — у них наоборот -5 dmg штраф.")
    A("- `uniqrnd` **зафиксирован при спавне** юнита-стрелка → у каждого индивидуального "
      "мушкетёра свой урон от хедшота. В отряде из 36 мушкетёров будут «снайперы» "
      "(uniqrnd≈0.9 → +450 урона) и «мазилы» (uniqrnd≈0.05 → +25 урона).")
    A("- Среднее ожидаемое: `0.05 × 250 = 12.5` дополнительного урона на выстрел "
      "(выровненный по случайным uniqrnd ~0.5).")
    A("")
    A("**Пример:** мушкетёр стреляет в Reiter (282 hp). Обычный урон — 6 hp. "
      "На случайном выстреле (5%) случается хедшот, и тот же мушкетёр (uniqrnd≈0.252) "
      "наносит `6 + floor(0.252 × 500) = 6 + 126 = 132 hp`. Reiter падает с 282 → 150 hp.\n")
    A("**Почему это важно для стратегии:**\n")
    A("- Стрелковые отряды против Heavy Cavalry/Light Infantry статистически окупаются "
      "сильно лучше чем формула урона показывает.")
    A("- Light Cavalry **в движении** иммунна к хедшоту → главный counter к стрелковому отряду.")
    A("- C1 имел 4% шанс мгновенного убийства (комментарий в коде); в C3 механика была ребалансирована "
      "в текущий вариант. Комментарий упоминает 2%, но в реальном коде осталось `<0.05` = **5%**.")
    A("")
    A("### Формационные бонусы\n")
    A("Источник: [`data/game/var/formations.cfg`](file:///C:/Program%20Files%20(x86)/Steam/steamapps/common/Cossacks%203/data/game/var/formations.cfg)\n")
    A("Юниты в строю получают **+урон / +shield** к каждому выстрелу/попаданию. "
      "В **hold-mode** (приказ «Стоять») бонусы значительно больше:\n")
    A("| Формация | размер | regular dmg/shield | **hold-mode dmg/shield** |")
    A("|---|---:|---:|---:|")
    A("| LINE / SQUARE / KARE | 15-196 | +2 / +2 | **+7 / +7** |")
    A("| LINE / SQUARE / KARE | **400** | **+3 / +3** | **+7 / +7** |")
    A("| Cavalry (PRUS, SHER, TRI) | любой | +1 / +1 | +1 / +1 |")
    A("")
    A("**Ключевое:** мушкетёр с base damage 6 → **в формации LINE в hold-mode наносит 13 урона** "
      "за выстрел (6 + 7 hold). И принимает -7 от каждого входящего попадания (поверх защиты).\n")
    A("**Что это значит для боя:**")
    A("- Стрелковые отряды **в hold-mode на формации** = **+117% к урону** (с 6 до 13).")
    A("- Без формации (рассыпная) — никаких бонусов.")
    A("- Кавалерийские формации (треугольник, клин) дают только +1/+1 — формация для них не главное.")
    A("- **firearrow** (зажигательная стрела) НЕ получает отрядный бонус к урону.")
    A("")
    A("### AoE damage cap — как кучкование защищает\n")
    A("Источник: [`miscext2.script:_misc_DoRoundDamage:576`](file:///C:/Program%20Files%20(x86)/Steam/steamapps/common/Cossacks%203/data/scripts/lib/miscext2.script)\n")
    A("Взрывы (cannon, mortar, gun, grenade) попадают по всем юнитам в радиусе `r`, **но "
      "только первые N получают урон**:\n")
    A("```")
    A("count = floor(1 + (r / 0.35)²)")
    A("```")
    A("| Оружие | radius | максимум юнитов под взрыв |")
    A("|---|---:|---:|")
    A("| Cannon (ядро) | ~1 t | **9** |")
    A("| Mortar (бомба) | ~2 t | **33** |")
    A("| Grenade (граната) | ~0.5 t | **3** |")
    A("| Howitzer | ~1 t | **9** |")
    A("\n**Стратегический вывод:** **плотная толпа защищена** — 50 юнитов в одной точке "
      "теряют максимум 9 от ядра, остальные нетронуты. Растянутая линия страдает гораздо больше.\n")
    A("Стрелы с зажигалкой (`barrow`) имеют другую логику: урон всем в радиусе если "
      "юнитов в области <= 300; иначе только тем, кто внутри строгого `r`.\n")
    A("### Высокая позиция (high ground)\n")
    A("Источник: [`unit.script:5469, 7272`](file:///C:/Program%20Files%20(x86)/Steam/steamapps/common/Cossacks%203/data/scripts/lib/unit.script)\n")
    A("Если стрелковый юнит стоит на возвышенности (Y > 0), его **search distance** увеличивается:\n")
    A("```")
    A("searchdist += goHeight × 2  (только для ranged юнитов: minsearchdist > melee_radius)")
    A("```")
    A("- `goHeight` — Y-координата юнита в тайлах (высота над уровнем 0).")
    A("- Бонус **только к радиусу обнаружения** (видят дальше / открывают огонь раньше).")
    A("- Сам выстрел (`radiusmax`) технически тот же, но если враг ещё не в радиусе атаки, "
      "юнит начинает движение и выстрелит как только цель войдёт в radius. На практике "
      "**мушкетёры с холма стреляют по атакующим раньше** = больше выстрелов до ближнего боя.")
    A("- Не работает на юнитов ближнего боя (pikemen в ближнем бою остаются в нём).")
    A("- Холмы создаются параметром `relief` при генерации карты (Highlands map даёт максимум гор).")
    A("")
    A("### Score за убийство\n")
    A("Источник: [`miscext2.script:445-461`](file:///C:/Program%20Files%20(x86)/Steam/steamapps/common/Cossacks%203/data/scripts/lib/miscext2.script)\n")
    A("- За убийство юнита: **score += target.score × 2**")
    A("- За убийство **наёмника-внутри-дип-центра**, юнита-в-транспорте, и т.п.: **score += inside_unit.score × 3**")
    A("- Эти бонусы складываются (1 ракетой убил наёмника в дип-центре + само здание = score за оба)")
    A("")
    A("### Standground / bartprepare — режимы атаки\n")
    A("Источник: [`unit.script:7259-7286`](file:///C:/Program%20Files%20(x86)/Steam/steamapps/common/Cossacks%203/data/scripts/lib/unit.script), "
      "[`player.script:2456-2463`](file:///C:/Program%20Files%20(x86)/Steam/steamapps/common/Cossacks%203/data/scripts/lib/player.script)\n")
    A("**Главный механизм:** дальность авто-обнаружения врага (`maxsearchdist`) "
      "**радикально различается** в режимах standground и обычном:\n")
    A("```")
    A("if (bstandground AND order != move):")
    A("    maxsearchdist := MIN(searchradius, GetMaxAttackRadius)   # полная дальность оружия")
    A("else:")
    A("    maxsearchdist := minsearchdist + 0.375                    # почти melee (!)")
    A("```")
    A("**Что это значит на практике:**\n")
    A("- **Без standground** мушкетёр (radiusmax≈9 t) обнаруживает врага только когда тот "
      "входит в **0.375 t от minsearchdist** — то есть подходит вплотную. Получается **1-2 выстрела** "
      "и сразу ближний бой. Это объясняет почему стрелковые юниты «стоят и не стреляют» по дальним целям.")
    A("- **С standground** обнаружение работает на полную `searchradius` (1500-2400 px ≈ 28-45 t). "
      "Мушкетёр стреляет по любому врагу в радиусе обзора — успевает 5-10 выстрелов до ближнего боя.")
    A("- **Standground также отключает RunAway** (см. ниже): юнит держит позицию, не пытается отступать.")
    A("- **Приказ движения стирает standground**: если юниту приказали идти куда-то, он не стреляет даже "
      "если bstandground=True (см. условие `order != move` в коде).")
    A("")
    A("**bartprepare** (artillery preparation) — флаг для **артиллерии, башен и портов**. "
      "Установлен на `cannon`, `howitzer`, `framegun`, `multicannon`, `tow` (towers), `port` (shipyards). "
      "При получении `attackpoint`-приказа (по площади) такие юниты:\n")
    A("- Принудительно выключают `bstandground` → переходят в обычный режим обнаружения")
    A("- Принудительно включают `bsearchenemy` → активно сканируют цели вокруг точки")
    A("- Получают приказ `attackpoint(trgx, trgz)` с задержкой подготовки (`attackdelay/attackmaxdelay`)")
    A("")
    A("**Стратегические выводы:**\n")
    A("- **Всегда ставь стрелков в standground** при обороне или подготовленной засаде. Без него "
      "мушкетёры сделают 1-2 выстрела вместо 5-10.")
    A("- **При продвижении** (`bstandground=False`) стрелки отходят (RunAway) — это иногда плюс "
      "(не дают подойти), иногда минус (тормозят свой же штурм).")
    A("- **Артиллерию лучше отдавать командой attackpoint** (Ctrl+ЛКМ) — `bartprepare` правильно настраивает "
      "режимы. Если просто переместить пушку и ждать — она в режиме движения НЕ откроет огонь.")
    A("")
    A("### RunAway — автоматический отход стрелков\n")
    A("Источник: [`unit.script:7363-7369`](file:///C:/Program%20Files%20(x86)/Steam/steamapps/common/Cossacks%203/data/scripts/lib/unit.script)\n")
    A("Если у стрелкового юнита (`minsearchdist > 0`, т.е. min range > 0) враг входит в "
      "**мёртвую зону** (между 0 и `minsearchdist`), юнит автоматически отступает:\n")
    A("```")
    A("if (cell_search_found_no_target AND враг_в_minsearchdist):")
    A("    if (NOT bstandground)")
    A("       AND (standtime=0 OR standtime > gc_unit_runawaydelay (1.3 sec)")
    A("            OR (player_is_human AND difficulty <= normal)):")
    A("        DoRunAway(toward_safe_direction, distance=gc_unit_runawaydist (3.5 t))")
    A("```")
    A("**Условия отступления (все должны выполниться):**\n")
    A("- Юнит **не в standground**.")
    A("- Юнит либо только что подошёл (`standtime=0`), либо стоит уже >1.3 сек, либо игрок-человек "
      "на easy/normal сложности (поблажка для новичков).")
    A("- Враг — в `minsearchdist` зоне.")
    A("\n**Эффект:** стрелок отступает на 3.5 тайла от врага, пытаясь восстановить дистанцию для выстрела. "
      "Это создаёт классический **паттерн отхода** мушкетёров: подошёл → стрельнул → отступил → стрельнул.\n")
    A("**Когда RunAway ВЫКЛЮЧЕН:**\n")
    A("- В `standground` (явный приказ держать позицию).")
    A("- ИИ-противник на hard+ — продолжает стрелять до самого ближнего боя, не отступает (опасный нюанс).")
    A("- При сложности hard+ игрок-человек: ИИ отходит как обычно, но игрок-человек на hard+ тоже не получает "
      "поблажку RunAway.")
    A("\n**Стратегические выводы:**\n")
    A("- Для отступательной тактики (отход с обстрелом) — **сними standground** и работай "
      "по уязвимой кавалерии/пехоте.")
    A("- Для удержания позиции (например, на холме) — **standground обязателен**, иначе мушкетёры "
      "разбегутся при подходе ближнего боя.")
    A("- Лёгкая кавалерия может **догнать отходящих мушкетёров** (fasthorse=96 против default=32 → ~3× быстрее).\n")
    A("### Дружественный огонь\n")
    A("Источник: [`miscext2.script:_misc_DoDamage:274`](file:///C:/Program%20Files%20(x86)/Steam/steamapps/common/Cossacks%203/data/scripts/lib/miscext2.script), "
      "[`weapon.script:482-492`](file:///C:/Program%20Files%20(x86)/Steam/steamapps/common/Cossacks%203/data/scripts/lib/weapon.script), "
      "[`unit.script:7686-7714`](file:///C:/Program%20Files%20(x86)/Steam/steamapps/common/Cossacks%203/data/scripts/lib/unit.script)\n")
    A("**Дружественный огонь ВКЛЮЧЁН для большинства снарядов.** В функции `_misc_DoDamage` "
      "**нет проверки на сторону/владельца** — урон применяется к любому объекту, попавшему под траекторию.\n")
    A("**Что попадает по своим:**\n")
    A("- Стрелы лучников (`STRELA`, `OSTRELA` fire arrows)")
    A("- Пули мушкетов (`SHOTMUSKET`)")
    A("- Гранаты (`NUCLGRE`)")
    A("- Артиллерия (`PSMPOINTTPUS`, `DIMMORT1`, `DIMMORT2NEW`, `PSMPOINTT`, `DIMMORT2KOR`)")
    A("- AoE взрывы (картечь, ядра, бомбы) — поражают **всё в радиусе**, включая своих "
      "(`_misc_DoRoundDamage` без фильтра по стороне).")
    A("\n**Что НЕ ранит союзников:**\n")
    A("- **Корабли** — есть отдельная защита `// prevent ships from friendly fire` "
      "в weapon.script. Торговцы и боевые корабли одного игрока не топят друг друга.")
    A("- Башни и пушки с `bcheckfriendonline=True` (по умолчанию ON) — **не выстрелят, "
      "если на линии огня стоит дружественное здание** (см. `_misc_IsBuildingInRay`). "
      "Но это про блокировку выстрела, а не про урон при пролёте.")
    A("\n**Список оружия с явно ОТКЛЮЧЁННОЙ проверкой `bcheckfriendonline`** "
      "(стреляют сквозь свои здания, не блокируются):\n")
    A("`STRELA`, `OSTRELA`, `SHOTMUSKET`, `SHOTBLOCKHOUSE`, `NUCLGRE`, `PSMPOINTTPUS`, "
      "`DIMMORT1`, `DIMMORT2NEW`, `PSMPOINTT`, `DIMMORT2KOR` — то есть **все стрелы, мушкетные пули "
      "и почти вся артиллерия**.\n")
    A("**Стратегические выводы:**\n")
    A("- **Не ставь свою пехоту на линию огня артиллерии** — ядро/бомба прошьёт строй и взорвётся "
      "среди своих.")
    A("- **Лучники и мушкетёры стреляют сквозь свои ряды** — стой во второй линии без проблем, "
      "но **бомба в массу твоих юнитов = твои потери**.")
    A("- **Башни без прямой линии огня** через здания не выстрелят (если их weapon `bcheckfriendonline=True`), "
      "но снаряд при выстреле уже не различает свой/чужой.\n")
    A("### Переключение оружия по дистанции\n")
    A("Источник: [`unit.script:_unit_GetWeaponToAttackIndex:6376-6451`](file:///C:/Program%20Files%20(x86)/Steam/steamapps/common/Cossacks%203/data/scripts/lib/unit.script)\n")
    A("Многие юниты имеют **несколько слотов оружия** (`weapon[0]`, `weapon[1]`, ...). Игра автоматически "
      "выбирает нужный слот по дистанции до цели — каждое оружие имеет `radiusmin..radiusmax`. "
      "Если враг вошёл в близкий диапазон — выбирается оружие с маленьким `radiusmin`, иначе — дальнее.\n")
    A("Дополнительно учитывается `attmask`: если у цели `mmask` совпадает с `weapon[i].attmask` "
      "(материал брони), это оружие приоритетнее. Поэтому fire arrows выбираются для построек "
      "(их attmask содержит `gc_obj_material_building`).\n")
    A("**Главные пары:**\n")
    A("**1. Cannon (пушка) — ядро против картечи:**\n")
    A("| Слот | Тип | dmg | Pause | Range (px) | Когда стреляет |")
    A("|---|---|---:|---:|---|---|")
    A("| `weapon[0]` PPOINTT | cannonball (ядро) | 1800 | 350 | **550-2160** | дистанция ≥ 550 px (~10.3 t) |")
    A("| `weapon[1]` PSMPOINTTPUS | cannister (картечь) | AoE по `gWeapons[]` | 350 | **0-450** | враг ближе 450 px (~8.4 t) |")
    A("\n**Это значит:** если пехота подошла на ~8 тайлов к пушке — она автоматически переходит в "
      "картечный режим. **Картечь — массовый урон по толпе** (AoE). Поэтому гасить пушку «навалом пехоты» "
      "= получить картечь в упор. **Атаковать пушку нужно растянутой линией** (не больше 9 в радиусе AoE — "
      "см. AoE damage cap).\n")
    A("**2. Musketeer 18c — пуля против штыка (bayonet):**\n")
    A("| Слот | Тип | dmg | Pause | Range (px) | Когда стреляет |")
    A("|---|---|---:|---:|---|---|")
    A("| `weapon[0]` (bayonet) | pike | 5-10 (по нации) | **0** (мгновенно) | **35-65** (~0.66-1.22 t) | в упор |")
    A("| `weapon[1]` SHOTMUSKET | bullet | 16-29 (по нации) | 140-190 | **400-900** (~7.5-16.9 t) | дальше 7.5 t |")
    A("\n**Стратегический смысл:** мушкетёр после выстрела не беспомощен в ближнем бою — у него **штык** "
      "с pause=0 (бьёт каждый цикл анимации). Атаковать перезаряжающихся мушкетёров кавалерией = "
      "получить штыковой бой. Прусские мушкетёры (dmg штыка 10) сильнее в ближнем бою чем баварские (5).\n")
    A("**Прокачки штыка** идут отдельно от прокачек пули — `bla.musketeer18.1.X` качает урон bullet, "
      "штык остаётся базовый.\n")
    A("**3. Archer — обычная стрела против огненной (firearrow):**\n")
    A("| Слот | Тип | dmg | Pause | Range (px) | Dispertion | Особенности |")
    A("|---|---|---:|---:|---|---:|---|")
    A("| `weapon[0]` STRELA | arrow | 15 | 75 | 400-800 | 175 px | основная стрельба |")
    A("| `weapon[1]` OSTRELA | firearrow | **150** | 125 | 400-600 | 200 px | attmask = building+wood+woodwall |")
    A("\n**Огненные стрелы — главное оружие лучников против построек.** Урон 150 (×10 от обычной), "
      "но: ниже скорострельность (-40%), хуже точность (+14% дисп.), не получают **отрядный бонус к урону** "
      "(см. секцию Хедшот/Формула урона). Игра автоматически переключает лучника на OSTRELA когда "
      "цель — здание/wood/палисад. **Лучники — лучший анти-билдинг стрелковый юнит** (если успевают подойти).\n")
    A("**4. Другие multi-weapon юниты** (поищи `weapon[1]` в их sid):\n")
    A("- **Янычар (jannisary)** — пуля + сабля ближнего боя.")
    A("- **Стрелец** — пищаль + бердыш ближнего боя.")
    A("- **Егерь / драгун** — пуля + сабля.")
    A("- **Конные стрелки** (drabant, конный стрелец) — пуля + сабля верхом.")
    A("\nВо всех случаях работа одинакова: близко — оружие ближнего боя, далеко — стрелковое. **Разница перезарядок:** "
      "например мушкетёр перезаряжается 150 кадров пулю и 0 штык — значит **сразу после выстрела** "
      "может ткнуть штыком если враг близко (а потом перезарядка пули продолжится в фоне).\n")
    A("### Штраф к дальности при движении\n")
    A("Источник: [`unit.script:8011-8023`](file:///C:/Program%20Files%20(x86)/Steam/steamapps/common/Cossacks%203/data/scripts/lib/unit.script), "
      "константа `gc_obj_maxattackradiusdisp = 3` (`dmscript.global:116`)\n")
    A("Юнит, который только что двигался (`standtime < 0.25 sec`), теряет в дальности:\n")
    A("```")
    A("if (standtime < 0.25) AND (weapon.kind != cannister):")
    A("    if (NOT bArtillery):")
    A("        radiusmax -= 3 × uniqrnd          # пехота: до -3 тайла")
    A("    else:")
    A("        radiusmax -= 3 × uniqrnd × 0.5    # артиллерия: до -1.5 тайла")
    A("```")
    A("**uniqrnd** — индивидуальный коэффициент юнита (см. секцию uniqrnd выше) ∈ [0..1]. "
      "Так что у разных стрелков в отряде штраф разный: «снайперы» (низкий uniqrnd) теряют меньше, "
      "«мазилы» (высокий uniqrnd) — почти весь штраф.\n")
    A("**Стратегические выводы:**\n")
    A("- **Стрелок в движении не выстрелит на полную дальность** — нужно ~0.25 сек постоять. "
      "Это объясняет почему мушкетёры «промахиваются» по дальним целям при подходе.")
    A("- **Картечь не штрафуется** — пушка может бить картечью даже на ходу (но в реальности "
      "пушка `bartillery` всё равно `bstandground=True` по умолчанию).")
    A("- **Артиллерия штрафуется в 2 раза меньше** — мортира/пушка после короткого movement готова "
      "стрелять почти на полную дальность.")
    A("- В сочетании с RunAway создаёт **отход — пауза — выстрел**: мушкетёр отбежал на 3.5 t, ждёт "
      "0.25 сек чтобы вернуть полную дальность, стреляет, и снова отходит.\n")
    A("### Бонус к дальности в покое\n")
    A("Источник: [`unit.script:8026-8028`](file:///C:/Program%20Files%20(x86)/Steam/steamapps/common/Cossacks%203/data/scripts/lib/unit.script)\n")
    A("Если юнит в состоянии **idle** (флаг `gc_statetag_move_idle`), он получает бонус к дальности:\n")
    A("```")
    A("rbonus += weapon[i].addradius   # обычно _misc_PixelsToTiles(32) = ~0.6 тайла")
    A("```")
    A("**Кому даётся:** мушкетёрам, лучникам, пушкам — у всех `addradius = 32 px = 0.6 t`. Для слабых стен "
      "(`gc_obj_usage_weakwall`) — дополнительно **+0.36 тайла** rbonus.\n")
    A("**Эффект:** стационарная защита (например, гарнизон на холме в standground) стреляет на "
      "**~0.6 t дальше** чем тот же отряд в движении. Мелочь, но в сочетании с high-ground (см. выше) "
      "и устранением movement penalty получается заметный буст эффективной дальности обороны.\n")
    A("### Захват юнитов\n")
    A("Источник: [`unit.script:7289-7307`](file:///C:/Program%20Files%20(x86)/Steam/steamapps/common/Cossacks%203/data/scripts/lib/unit.script)\n")
    A("Военные юниты могут **захватывать** мирные/нейтральные юниты противника (не убивая). "
      "Каждый scan tick (раз в ~0.5 сек) с шансом **5%** проверяется условие захвата:\n")
    A("```")
    A("if (random < 0.05) AND (target.bcapture=True) AND (NOT target.bbuilding)")
    A("    AND (NOT attacker.bcapture)  # сам не захватываемый")
    A("    AND (NOT attacker.media=water)")
    A("    AND (target.orderlist.count < cMinCaptureOrdListCount)  # цель «занята делом»")
    A("    AND (path_distance(attacker, target) <= attacker.searchradius):")
    A("        attacker.OrderMove(target.position)")
    A("        attacker.SetOrderTrg(target)  # фиксируется на захват")
    A("```")
    A("**Кто может захватывать (`bcancapture=True`):** все военные юниты-некрестьяне.\n")
    A("**Кого можно захватить (`bcapture=True`):**\n")
    A("- Большинство **крестьян** (peasant, peabav, peaaus, ...) — кроме `Ukrainian` и `Scottish` "
      "(их крестьяне `bcapture := False` явно).")
    A("- **Артиллерия** (`cannon`, `howitzer`, `mortar`, `multicannon`, `framegun`) — `bcapture := True` "
      "при определении ([unit.script:1721](file:///C:/Program%20Files%20(x86)/Steam/steamapps/common/Cossacks%203/data/scripts/lib/unit.script)).")
    A("- **Здания** (`bbuilding=True`) тоже захватываются (но через отдельный механизм — пехота окружает).")
    A("\n**Стратегические выводы:**\n")
    A("- **Захваченная пушка переходит на твою сторону полностью** — со всеми прокачками атакующей нации! "
      "Это очень мощный экономический эффект.")
    A("- **Защищай пушки пехотой** — пехота противника в радиусе захвата может «увести» пушку без боя.")
    A("- **Украинские/шотландские крестьяне иммунны к захвату** — сильное национальное преимущество "
      "(не теряешь экономику от соседа-кавалериста).")
    A("- **5% шанс на тик** — захват не мгновенный, нужно несколько секунд возле цели. "
      "За 5-7 сек шанс ~25-30% завершить попытку.\n")
    A("### Лечение священниками\n")
    A("Источник: [`unit.script:1151-1188`](file:///C:/Program%20Files%20(x86)/Steam/steamapps/common/Cossacks%203/data/scripts/lib/unit.script), "
      "формула в [`miscext2.script:371-398`](file:///C:/Program%20Files%20(x86)/Steam/steamapps/common/Cossacks%203/data/scripts/lib/miscext2.script)\n")
    A("Священники (`priest`, `pope`, `mullah`, `padre`) лечат союзных юнитов. Используют псевдо-оружие "
      "`gc_obj_weapon_kind_heal`. Формула:\n")
    A("```")
    A("target.hp += weapon.damage      # БЕЗ shield, БЕЗ protection!")
    A("target.hp = min(target.hp, target.maxhp)")
    A("```")
    A("**Heal pause = 0** — лечат каждый цикл анимации (~0.7 сек), пока цель не полное HP.\n")
    A("| Юнит | heal/удар | дальн. (px / tiles) | Где доступен |")
    A("|---|---:|---|---|")
    A("| Priest | 20 | 0-400 / 7.5 t | большинство европейских наций |")
    A("| Pope | 25 | 0-350 / 6.6 t | Папская область / Венеция |")
    A("| Mullah | 15 | 0-500 / **9.4 t** | Турция / Алжир (самый дальний heal) |")
    A("| Padre | 30 | 0-400 / 7.5 t | Испания / Португалия (самый сильный heal) |")
    A("\n**Стратегические выводы:**\n")
    A("- **Heal игнорирует броню** — лечит на полное значение независимо от того, кто-кого защитного.")
    A("- **Несколько священников лечат одну цель параллельно** — рейтер с 282 HP лечится 4 священниками "
      "= +80 HP/цикл = ~115 HP/сек. Можно держать тяжёлую кавалерию вечно.")
    A("- **Mullah имеет самую большую дальность** (9.4 t) — лечит из второй линии, недосягаем для ближнего боя.")
    A("- **Padre самый эффективный** (30/удар) — испанско-португальская армия очень живуча.")
    A("- Священники сами **уязвимы** (низкий HP, нет брони) — главный таргет для рейдов.\n")
    A("### Shield /3 при недостроенном здании\n")
    A("Источник: [`miscext2.script:339-342`](file:///C:/Program%20Files%20(x86)/Steam/steamapps/common/Cossacks%203/data/scripts/lib/miscext2.script)\n")
    A("При расчёте урона: если здание **ещё строится** (`bbuilt=False`), его shield делится на 3:\n")
    A("```")
    A("if (target.bbuilt):  damage -= shield        # достроено: полный shield")
    A("else:                 damage -= shield // 3   # стройка: 1/3 shield")
    A("```")
    A("**Стратегический смысл:** **сноси здания пока они строятся**. Например, башня на стройке имеет "
      "shield ~33 (вместо 100), и каждый удар по ней проходит почти полностью. Контр-стройка "
      "(атака на возводимое здание противника) гораздо эффективнее чем атака готового.\n")
    A("Касается ТОЛЬКО зданий — юниты не имеют состояния «строится».\n")
    A("### Реакция ИИ — отряд переходит в атаку от одного удара\n")
    A("Источник: [`miscext2.script:406-417`](file:///C:/Program%20Files%20(x86)/Steam/steamapps/common/Cossacks%203/data/scripts/lib/miscext2.script)\n")
    A("Любой не-артиллерийский юнит ИИ, **получивший урон**, переключает свой отряд (`squad`) в "
      "`fAgressive=True` и обновляет `fLastBattleTime`.\n")
    A("**Эффект:** один поражающий выстрел/удар по отряду ИИ переводит его в боевой режим. "
      "ИИ начинает контратаковать, преследовать, искать врага активно.\n")
    A("**Стратегические выводы:**\n")
    A("- **Поклёвывание ИИ** (один лучник в крестьянина) **активирует реакцию всего отряда ИИ**. "
      "Может быть полезно: отвлекаешь лучником, основная сила атакует с другой стороны.")
    A("- ИИ на артиллерии (пушки/мортиры) — НЕ переключается (особый случай в коде).")
    A("- Если хочешь скрытно собрать ресурсы рядом с ИИ — **не атакуй вообще**, иначе вся армия "
      "зашевелится.\n")
    A("### Офицеры — миф о боевой ауре\n")
    A("Источник: [`player.script:810-858`](file:///C:/Program%20Files%20(x86)/Steam/steamapps/common/Cossacks%203/data/scripts/lib/player.script), "
      "[`unit.script:163-164`](file:///C:/Program%20Files%20(x86)/Steam/steamapps/common/Cossacks%203/data/scripts/lib/unit.script)\n")
    A("**В игре НЕТ персонального бонуса-ауры от офицера.** Офицеры/барабанщики занимают слоты "
      "`maskOfficers` в формационной сетке, но в коде **нет** проверок типа "
      "`if (officer in radius) then damage += X`.\n")
    A("**Что реально даёт офицер:**\n")
    A("- Без офицера **нельзя сформировать отряд** — а без отряда нет `fAddDamage` / `fAddShield` "
      "(см. секцию Формационные бонусы).")
    A("- Офицер ходит в составе строя и держит формацию.")
    A("- При смерти офицера отряд **рассыпается** → теряет все формационные бонусы (это и есть "
      "«потеря ауры» которую ощущают игроки).")
    A("\n**Стратегический вывод:** **убийство офицера = убийство всех бонусов отряда**. "
      "Если в LINE-формации все мушкетёры имели +7 hold dmg / +7 hold shield — после смерти "
      "офицера это всё пропадает мгновенно. **Офицеры — снайперская цель №1.**\n")
    A("### Чего НЕТ в игре (подтверждённое отсутствие)\n")
    A("После проверки `unit.script`, `weapon.script`, `miscext2.script`, `player.script`:\n")
    A("- **НЕТ бонуса за кавалерийский натиск.** Кавалерия не получает бонусного урона на разгоне или при "
      "первом ударе. Поиск `bcharging`/`firsthit`/`chargebonus` ничего не находит. "
      "Урон кавалерии = базовый урон оружия.")
    A("- **НЕТ отдельного типа урона против лошадей.** Пикинёры не имеют умножителя «×N против кавалерии». "
      "Эффективность пикинёра против рейтара — это просто `weapon.damage(pike)` против "
      "`target.protection[pike]` где у кавалерии эта защита обычно низкая.")
    A("- **НЕТ ауры барабанщика.** Барабанщик — просто слот в формации (формальное наполнение). "
      "Не даёт +урон, +скорость, +мораль.")
    A("- **НЕТ особой траектории у гранатомёта.** Гранатомёт использует обычный AoE-конвейер (тип cannonball с "
      "радиусом взрыва). Никаких специальных эффектов траектории нет.")
    A("- **НЕТ скрытности/невидимости.** Все юниты видны если в зоне обзора игрока. Нет флага `bstealth`.")
    A("\n**Что это меняет:** **формация — единственный способ умножить урон**. Никаких скрытых "
      "бонусов от позиции (кроме high-ground / standground). Прокачки + формация + тип оружия "
      "против типа брони — это вся боевая математика.\n")
    A("### Свойства формулы урона\n")
    A("- `protection` и `shield` уменьшают урон **аддитивно** (не процентно).")
    A("- **Минимум 1 хп** урона: даже если `protection > damage + bonuses`, пройдёт 1 hp.")
    A("- Shield применяется ВСЕГДА (включая поверх protection). Танки с shield эффективнее тяжёлой защиты.")
    A("- При постройке здания shield делится на 3.")
    A("- `firearrow` (зажигательная стрела лучников) НЕ получает отрядный бонус к урону.\n")
    A("### Рассеяние — почему выстрелы промахиваются\n")
    A("Источник: [`weapon.script:_weapon_CalcShotDispertion:625`](file:///C:/Program%20Files%20(x86)/Steam/steamapps/common/Cossacks%203/data/scripts/lib/weapon.script)\n")
    A("При каждом выстреле снаряд **рассеивается** относительно цели:\n")
    A("```")
    A("maxdisp = dist × disp × 0.0267   # в тайлах")
    A("shot_x = target_x + (1 - random*2) × maxdisp")
    A("shot_z = target_z + (1 - random*2) × maxdisp")
    A("```")
    A("Где `dist` — дистанция до цели (тайлы), `disp` — `weapon.dispertion` (тайлы, после "
      "_misc_PixelsToTiles). **Чем дальше — тем больше рассеяние** (линейно).\n")
    A("**Базовые значения dispertion** (из unit.script):")
    A("| Оружие | dispertion (px / tiles) | На 15 t отклонение |")
    A("|---|---:|---:|")
    A("| Strelet (SHOTMUSKET, base) | 200 / 3.75 | **±1.50 t** |")
    A("| Archer (STRELA) | 175 / 3.28 | ±1.31 t |")
    A("| Archer (OSTRELA fire) | 200 / 3.75 | ±1.50 t |")
    A("| Musketeer base | 250 / 4.69 | ±1.88 t |")
    A("| Cannon (PPOINTT) | ~250 / 4.69 | ±1.88 t |")
    A("| Tower (PPOINTTTOW) | ~100 / 1.88 | ±0.75 t |")
    A("| Yacht/galley (PPOINTTKOR) | 25 / 0.47 | ±0.19 t |")
    A("\n**Шанс попасть в юнит размером 1×1 t** на дистанции d:\n")
    A("- Если 2×maxdisp ≤ 1 → ~100% попадание")
    A("- Если 2×maxdisp > 1 → шанс ≈ 1 / (2×maxdisp) попасть точно в нужный квадрат")
    A("\nПример: мушкетёр (disp=3.75) на 15 t → maxdisp=1.50, окно ±1.50 = 3.00 → шанс попасть "
      "в 1×1 цель ≈ 1/3 = **~33%** одним выстрелом. Это означает что **TTK в матрице контр-эффективности ниже "
      "реального в 3 раза для дальних пуль/стрел**.\n")
    A("**Апгрейды dispertion** — только для **артиллерии**:")
    A("- `aca.20` (Research new sighting devices for artillery): **-35% dispersion**")
    A("- `aca.27` (Develop mathematics): **-35% dispersion** (накапливается с aca.20)")
    A("- ⚠ Для **мушкетёров и лучников** прямого dispersion-апгрейда нет.")
    A("")
    A("### uniqrnd — индивидуальное случайное число юнита\n")
    A("При спавне каждый юнит получает `uniqrnd ∈ [0..1]` ([`unit.script:2726`](file:///C:/Program%20Files%20(x86)/Steam/steamapps/common/Cossacks%203/data/scripts/lib/unit.script)). "
      "Это **зафиксированное** число, остаётся неизменным до смерти. "
      "Используется в **4 механиках одновременно**:\n")
    A("| # | Где применяется | Эффект |")
    A("|---:|---|---|")
    A("| 1 | Бонус хедшота | `+floor(uniqrnd × 500)` дополнительного урона при крите |")
    A("| 2 | Эффективная max range | `radiusmax -= uniqrnd × 3` тайла. Каждый стрелок стреляет чуть на разную дистанцию (асинхронные залпы) |")
    A("| 3 | Search timing | `nextSearch = now + uniqrnd × 0.15 + 0.3` сек. Юниты не сканируют синхронно |")
    A("| 4 | Multiplayer sync seed | `SetRandomKey(floor(uniqrnd × MaxInt))` для синхронизации |")
    A("\nЭффекты — это **компромисс**, встроенный в каждого юнита: высокий uniqrnd → большие криты, "
      "но меньшая дальность. Низкий → дальше стреляет, но слабее криты.\n")
    A("В C3 разработчики **специально расширили base range на +100 px** для лучников (`unit.script:999` "
      "комментарий: `// c3 added range +100 cause of uniqrnd range dispertion`) — компенсировать "
      "uniqrnd usage #2.\n")
    A("## Типы оружия (gc_obj_weapon_kind_*)\n")
    A("| Kind | Описание | Носители |")
    A("|---|---|---|")
    A("| `pike` | Длинное копьё/пика | Pikemen, Pikeman18 |")
    A("| `sword` | Меч/сабля | Light infantry, swordsmen, кавалерия в ближнем бою |")
    A("| `bullet` | Пуля огнестрела | Musketeer, Strelet, Janissary, Dragoon, etc. |")
    A("| `arrow` | Стрела/болт | Archer (`SHOTLU` ammo) |")
    A("| `cannonball` | Пушечное ядро | Cannon, Tower, Frigate (single shot) |")
    A("| `cannister` | Картечь | Cannon close-range, multi-cannon |")
    A("\nКаждый юнит имеет `protection[kind]` отдельно по каждому типу — см. колонки `prot_*` в [04_units.md](04_units.md).\n")
    A("## Скорости юнитов\n")
    A("Базовые `gc_obj_speed_*` из `dmscript.global:603-620`. **Абстрактные единицы** (не tiles/sec). "
      "Реальная скорость в тайлах/сек зависит от animation `walkInterval`, `walkintervalfactor` "
      "и game speed. Для перевода нужен эмпирический замер.\n")
    A("| Класс | Speed | Заметка |")
    A("|---|---:|---|")
    speed_table = e.get("obj_speed_table_abstract_units", {})
    notes = {
        "default": "пехота, артиллерия и многие юниты по умолчанию",
        "peasant": "крестьянин — быстрее обычной пехоты",
        "hardhorse": "тяжёлая кавалерия (Reiter, Cuirassier, Vityaz)",
        "fasthorse": "лёгкая кавалерия (Hussar, Lancer, Cossack) — самые быстрые",
        "cannon": "пушка — медленная",
        "mortar": "мортира — чуть быстрее пушки",
        "fishboat": "рыбацкая лодка",
        "yacht": "яхта (стрелковый корабль)",
        "yachttur": "турецкая яхта (быстрее стандартной)",
        "frigate": "фрегат",
        "battleship": "баттлшип — самый медленный военный корабль",
        "chaika": "украинская чайка — мобильная",
        "ferry": "паром (transport)",
    }
    for k in ["default","peasant","hardhorse","fasthorse","cannon","mortar","howitzer",
              "multicannon","fishboat","ferry","yacht","yachttur","chaika","galley",
              "frigate","xebec","battleship"]:
        if k in speed_table:
            A(f"| {k} | {speed_table[k]} | {notes.get(k, '')} |")
    A("\n**Закон:** относительные значения. fasthorse(96) ≈ ×3 от cannon(20). "
      "peasant(40) посередине. Самые медленные — battleship/multicannon (16).\n")
    A("## Офицеры и формации\n")
    A("Каждая нация имеет N групп офицеров. Один офицер ведёт **строй** определённых юнитов "
      "(чаще пехота/кавалерия одного класса). Формации стандартные для всех:\n")
    A("**LINE / SQUARE / KARE × 15 / 36 / 72 / 120 / 196 / 400 юнитов.**\n")
    A("Чем больше формация, тем сильнее бонусы (атака, защита, мораль).\n")
    A("Полные таблицы офицеров → секции в [nations/](nations/README.md) для каждой нации.\n")
    # Counter matrix
    A("## Матрица контр-эффективности (приближённый TTK)\n")
    A("Для каждой пары (атакующий класс, защищающийся класс) — **приближённое время убийства** "
      "(time-to-kill, TTK) в **игровых секундах** при 1v1, без учёта формаций, движения, "
      "промахов и shield-бонусов отрядов.\n")
    A("Расчёт: для атакующего берём **репрезентативного юнита класса** (медианный по урону); "
      "для защитника — медианный по HP. Применяется формула урона:\n")
    A("```\napplied = max(1, weapon.dmg - target.shield - target.protection[weapon.kind])\n"
      "DPS = applied / weapon.pause_sec\n"
      "TTK = target.HP / DPS\n```\n")
    A("⚠ Цифры ориентировочные. Реальный TTK будет выше из-за: дороги к цели, "
      "подготовки выстрела (`bartprepare`), формационных бонусов (отрядный щит, формация LINE/SQUARE/KARE), "
      "movement penalty к accuracy, fast-cavalry headshot bonus.\n")

    # Build counter matrix
    BATTLE_CLASSES = [
        "Peasant", "Pikemen 17c", "Pikemen 18c", "Light Infantry",
        "Musketeers 17c", "Musketeers 18c", "Grenadiers", "Archers",
        "Light Cavalry", "Dragoons", "Heavy Cavalry",
        "Cannons", "Mortars",
    ]
    by_class_full: dict[str, list[dict]] = defaultdict(list)
    for u in data["units"]:
        cls = classify_unit(u["sid"], u.get("usage_short", ""))
        if cls in BATTLE_CLASSES:
            by_class_full[cls].append(u)

    # For each class, compute median attacker stats (damage, pause, kind) and median defender stats (hp, shield, protection).
    # Melee swing rate (when weapon.pause_sec = 0) comes from each unit's own
    # attack0 animation length via melee_swing_sec(sid) — see config.py.
    def median_unit_for_attack(cls: str) -> dict | None:
        units = by_class_full.get(cls, [])
        with_dmg = [u for u in units if u.get("weapons") and u["weapons"][0].get("damage")]
        if not with_dmg:
            return None
        with_dmg.sort(key=lambda x: x["weapons"][0]["damage"])
        median = with_dmg[len(with_dmg) // 2]
        w = median["weapons"][0]
        pause = w.get("pause_sec")
        if pause in (None, 0, 0.0):
            pause = melee_swing_sec(median["sid"])
        return {
            "name": median.get("name_en") or median["sid"],
            "sid": median["sid"],
            "damage": w.get("damage"),
            "pause_sec": pause,
            "kind": w.get("kind"),
        }

    def median_unit_for_defense(cls: str) -> dict | None:
        units = [u for u in by_class_full.get(cls, []) if u.get("hp")]
        if not units:
            return None
        units.sort(key=lambda x: x["hp"])
        median = units[len(units) // 2]
        return {
            "name": median.get("name_en") or median["sid"],
            "sid": median["sid"],
            "hp": median.get("hp") or 1,
            "shield": median.get("shield") or 0,
            "prot_pike": median.get("prot_pike") or 0,
            "prot_sword": median.get("prot_sword") or 0,
            "prot_bullet": median.get("prot_bullet") or 0,
            "prot_arrow": median.get("prot_arrow") or 0,
            "prot_cannister": median.get("prot_cannister") or 0,
            "prot_cannonball": median.get("prot_cannonball") or 0,
        }

    attackers = {cls: median_unit_for_attack(cls) for cls in BATTLE_CLASSES}
    defenders = {cls: median_unit_for_defense(cls) for cls in BATTLE_CLASSES}

    # Header
    short_names = {
        "Peasant": "Pea", "Pikemen 17c": "Pik17", "Pikemen 18c": "Pik18",
        "Light Infantry": "LtInf", "Musketeers 17c": "Mus17", "Musketeers 18c": "Mus18",
        "Grenadiers": "Gren", "Archers": "Arch", "Light Cavalry": "LtCav",
        "Dragoons": "Drag", "Heavy Cavalry": "HvCav", "Cannons": "Cnn", "Mortars": "Mor",
    }
    A("**Медианные представители классов** (использованы для расчёта):\n")
    A("| Класс | Атакующий-репрезентант | урон | перезарядка (с) | тип | Защитник-репрезентант | HP | shield |")
    A("|---|---|---:|---:|---|---|---:|---:|")
    for cls in BATTLE_CLASSES:
        a = attackers[cls]
        d = defenders[cls]
        a_str = f"`{a['sid']}` ({a['name']})" if a else "—"
        d_str = f"`{d['sid']}` ({d['name']})" if d else "—"
        A(f"| {cls} | {a_str} | {fmt(a['damage']) if a else '—'} "
          f"| {fmt(a['pause_sec']) if a else '—'} | {a['kind'] if a else '—'} "
          f"| {d_str} | {fmt(d['hp']) if d else '—'} | {fmt(d['shield']) if d else '—'} |")
    A("")
    A(f"### Матрица контр-эффективности — TTK в игр-сек\n")
    A("Строки = **атакующий**. Колонки = **защищающийся**. Ячейка = TTK (game-sec). "
      "Зелёные/низкие = атакующий быстро убивает; красные/высокие = защитник долго стоит.\n")
    header = "| Atk \\ Def | " + " | ".join(short_names[c] for c in BATTLE_CLASSES) + " |"
    sep = "|---|" + "---:|" * len(BATTLE_CLASSES)
    A(header)
    A(sep)
    for atk_cls in BATTLE_CLASSES:
        a = attackers[atk_cls]
        if not a or a["damage"] is None or not a["pause_sec"]:
            row = f"| **{short_names[atk_cls]}** ({atk_cls}) | " + " | ".join("—" for _ in BATTLE_CLASSES) + " |"
            A(row)
            continue
        cells = []
        for def_cls in BATTLE_CLASSES:
            d = defenders[def_cls]
            if not d:
                cells.append("—")
                continue
            kind = a["kind"] or "bullet"
            prot_key = f"prot_{kind}"
            prot = d.get(prot_key, 0) or 0
            applied = max(1, a["damage"] - d["shield"] - prot)
            dps = applied / a["pause_sec"]
            ttk = d["hp"] / dps
            # Format: short
            if ttk < 1:
                cells.append(f"**{ttk:.1f}**")
            elif ttk < 10:
                cells.append(f"{ttk:.1f}")
            elif ttk < 100:
                cells.append(f"{ttk:.0f}")
            else:
                cells.append(f"_{ttk:.0f}_")  # very long = italic
        row = f"| **{short_names[atk_cls]}** ({atk_cls}) | " + " | ".join(cells) + " |"
        A(row)
    A("")
    A("**Чтение:** жирным — быстро убивает (TTK <1 сек), курсивом — почти не убивает (TTK >100 сек).\n")
    # Now: miss-adjusted TTK for ranged shooters
    A("### Матрица контр-эффективности с поправкой на промахи (пули/стрелы)\n")
    A("Для bullet/arrow атакующих TTK выше из-за **рассеяния**: на дистанции 15 t мушкетёр "
      "попадает только ~33% выстрелов (см. секцию Рассеяние). Здесь TTK умножен на коэффициент "
      "промахов:\n")
    A("```")
    A("hit_chance(dist) = min(1.0, 1 / (2 × maxdisp))")
    A("                 = min(1.0, 1 / (2 × dist × disp × 0.0267))")
    A("real_TTK = ideal_TTK / hit_chance")
    A("```")
    A("Считаю на дистанции 12 t (типичная дистанция боя стрелков), с базовым рассеянием=200 px/3.75 t. "
      "Для ближнего боя (cannon/mortar в ближнем бою?) дистанция 6 t как запасное значение. Ниже — относительный TTK для "
      "стрелков (только строки: Mus17, Mus18, Arch, Drag, LtCav (если стрельба)):\n")
    A("| Atk \\ Def | Pea | Pik17 | LtInf | Mus17 | Gren | Arch | LtCav | HvCav |")
    A("|---|---:|---:|---:|---:|---:|---:|---:|---:|")
    # Compute miss-adjusted TTK
    DIST_RANGED = 12.0  # типичная дистанция мушкета
    DIST_MELEE = 0.5    # melee — почти 100% попадание
    DEFAULT_DISP_TILES = 3.75  # ~200px
    SHORT_TARGETS = ["Peasant", "Pikemen 17c", "Light Infantry", "Musketeers 17c",
                      "Grenadiers", "Archers", "Light Cavalry", "Heavy Cavalry"]
    SHORT_TARGET_LABELS = {"Peasant":"Pea", "Pikemen 17c":"Pik17", "Light Infantry":"LtInf",
                            "Musketeers 17c":"Mus17", "Grenadiers":"Gren", "Archers":"Arch",
                            "Light Cavalry":"LtCav", "Heavy Cavalry":"HvCav"}
    for atk_cls in ["Musketeers 17c", "Musketeers 18c", "Grenadiers", "Archers",
                     "Light Cavalry", "Dragoons"]:
        a = attackers.get(atk_cls)
        if not a or not a.get("damage") or not a.get("pause_sec") or not a.get("kind"):
            continue
        is_ranged = a["kind"] in ("bullet", "arrow")
        dist = DIST_RANGED if is_ranged else DIST_MELEE
        maxdisp = dist * DEFAULT_DISP_TILES * 0.0267
        hit_chance = min(1.0, 1.0 / max(2 * maxdisp, 0.01))
        cells = []
        for def_cls in SHORT_TARGETS:
            d = defenders.get(def_cls)
            if not d:
                cells.append("—")
                continue
            kind = a["kind"]
            prot_key = f"prot_{kind}"
            prot = d.get(prot_key, 0) or 0
            applied = max(1, a["damage"] - d["shield"] - prot)
            dps = applied / a["pause_sec"]
            ideal_ttk = d["hp"] / dps
            real_ttk = ideal_ttk / hit_chance
            if real_ttk < 5:
                cells.append(f"{real_ttk:.1f}")
            elif real_ttk < 60:
                cells.append(f"{real_ttk:.0f}")
            else:
                cells.append(f"_{real_ttk:.0f}_")
        label = short_names.get(atk_cls, atk_cls)
        row = (f"| **{label}** ({atk_cls}, hit≈{int(hit_chance*100)}%) | "
                + " | ".join(cells) + " |")
        A(row)
    A("\n**Что добавилось** относительно идеального TTK:")
    A("- Стрелки на дистанции 12 t **попадают ~50%** выстрелов → TTK ×2.")
    A("- Лучники с disp 175 px (немного лучше) — попадают чуть чаще.")
    A("- На большой дистанции (15-17 t у мушкета) — TTK еще +30-50%.")
    A("- В **hold-mode формации** урон +7 (с 6 до 13) → TTK падает в ~2 раза. "
      "С учётом промахов — формация компенсирует рассеяние примерно как раз.")
    A("- **На холме** мушкетёры начинают стрелять на 2-4 t дальше → +1-2 выстрела до того, "
      "как враг подойдёт. Эффективный TTK снижается на ~10-30% за счёт лишних залпов.")
    A("")
    A("**Примеры выводов** (на данных стандартной защиты):")
    A("- **Пушки / мортиры** против пехоты — TTK <1 (полный убой одним выстрелом за выстрел).")
    A("- **Пикинёры** против тяжёлой кавалерии — TTK высокий, потому что у кавалерии есть prot_pike. "
      "Но в формации пикинёр даёт значительно больше DPS.")
    A("- **Мушкетёры** против пехоты с prot_bullet=4-6 — TTK ~10-15 сек, реалистично.")
    A("- **Лёгкая кавалерия** против пушек — низкий TTK (cannon без брони, легко убивается).\n")
    A("## Перекрёстная таблица: апгрейды × характеристики\n")
    A("Какой апгрейд на что влияет. Сводка по `itype` (расшифровано в "
      "[05_upgrades.md](05_upgrades.md)). Цены даны для базовой нации (отличаются по "
      "нациям — см. [05_upgrades.md](05_upgrades.md)).\n")
    A("**Подсказки по нотации:** `aca.X` = academy.X, `bla.<unit>.1.X` = blacksmith damage X-уровня для юнита. "
      "`mil.X` = mill.X. Названия — из локали (en).\n")
    A("### Глобальные апгрейды (academy, mill)\n")
    # Build comprehensive aca/mil upgrade table
    sample_nat = "aus"
    aca_ups: list[dict] = []
    for u in data["upgrades"]:
        if u["nation"] != sample_nat: continue
        sid = u["sid"]
        if not (sid.startswith(f"{sample_nat}aca.") or sid.startswith(f"{sample_nat}mil.")):
            continue
        if u.get("itype_short") in ("—", "", None):
            continue
        aca_ups.append(u)
    aca_ups.sort(key=lambda x: (x["sid"].split(".")[0], int(x["sid"].rsplit(".", 1)[-1]) if x["sid"].rsplit(".", 1)[-1].isdigit() else 99))
    A("| Апгрейд | Эффект | val | Стоимость (F/W/S/G/I/C) | Что улучшает |")
    A("|---|---|---:|---|---|")
    for u in aca_ups:
        place = "Academy" if "aca" in u["sid"] else "Mill"
        eff = u.get("itype_short") or "—"
        val = u.get("value")
        f = u.get("food") or 0; w = u.get("wood") or 0; s = u.get("stone") or 0
        g = u.get("gold") or 0; ir = u.get("iron") or 0; c = u.get("coal") or 0
        cost = f"F{f}/W{w}/S{s}/G{g}/I{ir}/C{c}"
        # Strip aus prefix for display
        sid_short = u["sid"].replace("aus", "")
        name_short = (u.get("name_en") or "").split(" %include")[0][:60]
        A(f"| `{sid_short}` ({place}) | **{eff}** | {val} | {cost} | {name_short} |")
    A("\n**Стек апгрейдов по эффектам** (накопительно):\n")
    A("- **+food extraction**: `mil.1` (+140%? note: mill upgrade values vary) + `aca.1` (+40%) + "
      "`aca.2` (+50%) + `aca.3` (+50%). Eff может выйти на 100+140+40+50+50 = **380%**.")
    A("- **+wood extraction**: `aca.8` (+100%). Удваивает wood/trip.")
    A("- **+stone extraction**: `aca.23` (+100%) + `aca.24` (+200%). До 100+100+200 = **400% eff**.")
    A("- **+fishing**: `aca.5` (+100%). Удваивает `fishingmax` лодки → 1000→2000.")
    A("- **+field HP** (`fieldlife`): `aca.4` (+200) + `bla.1` (+100). Меняет урон полю с 100/удар "
      "до 25/удар → +4× food per field.")
    A("- **+firearm damage %**: `aca.12` (+10) + `aca.13` (+10) + `aca.14` (+15) + `aca.15` (+25) = "
      "**+60% урона** для всех bullet/arrow юнитов.")
    A("- **+artillery range %**: `aca.16` (+5) + `aca.17` (+10) = **+15% range**.")
    A("- **+artillery accuracy %**: `aca.20` (-35%) + `aca.27` (-35%) = **-70% рассеяния** "
      "(почти точные выстрелы).")
    A("- **+artillery durability %**: `aca.18` (+50%).")
    A("- **+firearm reload %**: `aca.31` (-30%) + `aca.33` (-30%) = **-60% к перезарядке** "
      "(скорость стрельбы +250%). Применяется ко **ВСЕМ стрелкам с пулевым оружием** — мушкетёрам, "
      "стрельцам, янычарам, драгунам и пр. (через `garr_UnitsShooters` / `garr_UnitsBayonet`), "
      "не только артиллерии.")
    A("- **+building shield**: `aca.9` (+85, всех зданий) + `aca.11` (+80, walls/towers).")
    A("- **+building speed**: `aca.10` (-75% buildtime).")
    A("- **+ship speed**: `aca.28` (+40%).")
    A("- **Разовые эффекты**: `aca.21` (лечит артиллерию), `aca.22` (геология — открывает шахты), "
      "`aca.25` (Монгольфьер — открывает карту), `aca.26` (лечит всех юнитов), `aca.30` (×10 скорость постройки кораблей), "
      "`aca.32` (-50% стоимость мушкетов).")
    A("- **Открывают юниты**: `aca.6` (фрегат), `aca.19` (многоствольная пушка), `aca.29` (линейный корабль).")
    A("")
    A("### Поюнитные апгрейды (blacksmith / barracks / stable)\n")
    A("Кузница (`bla`), бараки (`bar`/`ba2`), конюшня (`sta`) содержат **поюнитные апгрейды урона и защиты** "
      "(5 уровней + специальный 7-й уровень). Формат sid: "
      "`<nat><place>.<unit>.<itype>.<level>` где itype=1 (damage) или 2 (protection).\n")
    A("Пример полного стека для **rusbar.pikemanrus** (Russian Spearman):")
    A("- 5 уровней damage (`.1.1` … `.1.5`): +1, +2, +2, +1, +2 = **+8 к урону**")
    A("- 5 уровней protection (`.2.1` … `.2.5`): +1, +1, +2, +1, +1 = **+6 к защите** (pike, sword, arrow)")
    A("- Level 7 unique (`.1.6` / `.2.6`): +2 к урону / +2 к защите (переопределение для rus)")
    A("- **Полный стек: +10 к урону / +8 к защите** на полностью прокачанном русском пикинёре.")
    A("")
    A("Полный список — в [05_upgrades.md](05_upgrades.md) (~4500 строк, по местам).\n")
    A("## Стоимость одного выстрела\n")
    A("Многие огнестрельные юниты и башни/корабли тратят `iron`/`coal`/`gold` за каждый выстрел.\n")
    A("| sid | nation | weapon | урон | перезарядка (с) | shots/min | iron/выстрел | coal/выстрел | gold/выстрел |")
    A("|---|---|---|---:|---:|---:|---:|---:|---:|")
    rows = []
    for u in data["units"]:
        for w in (u["weapons"] or []):
            cost = w.get("cost") or {}
            if cost:
                shots = round(60 / w["pause_sec"], 1) if w.get("pause_sec") else None
                rows.append((u["sid"], u["nation"], w["weaponsid"] or w["kind"] or "?",
                              w.get("damage"), w.get("pause_sec"), shots,
                              cost.get("iron"), cost.get("coal"), cost.get("gold")))
    for b in data["buildings"]:
        cost = b.get("weapon_cost") or {}
        if cost:
            pause_sec = (round(b["weapon_pause_frames"]/32, 2) if b["weapon_pause_frames"] else None)
            shots = (round(60 / pause_sec, 1) if pause_sec else None)
            rows.append((b["sid"], b["nation"], b["weapon_kind"] or "?",
                          b["weapon_damage"], pause_sec, shots,
                          cost.get("iron"), cost.get("coal"), cost.get("gold")))
    rows.sort()
    seen = set()
    for r in rows:
        if (r[0], r[1]) in seen:
            continue
        seen.add((r[0], r[1]))
        A(f"| `{r[0]}` | {r[1]} | `{r[2]}` | {fmt(r[3])} | {fmt(r[4])} | {fmt(r[5])} "
          f"| {fmt(r[6])} | {fmt(r[7])} | {fmt(r[8])} |")
    write_md(TREE_ROOT / "02_combat.md", out)


# ---------- 03_buildings.md ----------

PER_NAT_NAMES = {
    "cen": "Town Hall", "hou": "Housing", "bar": "Barracks 17c", "ba2": "Barracks 18c",
    "bla": "Blacksmith", "sta": "Stable", "tem": "Cathedral",
    "aca": "Academy", "art": "Artillery Depot", "dip": "Diplomatic Center",
}
COMMON_NAMES = {
    "mil": "Mill", "sto": "Storehouse", "mar": "Market", "por": "Shipyard",
    "tow": "Tower", "gol": "Gold Mine", "iro": "Iron Mine", "coa": "Coal Mine",
    "swa": "Stone Wall", "sga": "Stone Gate", "wga": "Wood Gate", "wwa": "Palisade",
}


def write_buildings(data: dict) -> None:
    out = []
    A = out.append
    A("# 03. Здания\n")
    A("[← Index](README.md)\n")
    A("Здания делятся на **per-nation** (`<nat>+suffix`, например `auscen`) и **common** "
      "(`<cluster>+suffix`, общие для группы наций — `eur`/`rus`/`tur`/`spa`/`ukr`/`por`).\n")
    A("Цены ниже — для **первого** экземпляра. Цена N-го здания того же типа = "
      "`floor(base × (costpercent/100)^(N-1))`. **Готовые таблицы N=1..6 для всех зданий "
      "→ [`derived/scaling_prices.md`](derived/scaling_prices.md)**.\n")
    A("**Производный документ** генерируется отдельным скриптом "
      "[`parser/compute_scaling.py`](../../parser/compute_scaling.py).\n")
    # TOC
    A("## Содержание\n")
    by_suffix_pn = defaultdict(list)
    for b in data["buildings"]:
        if b["kind"] != "per-nation":
            continue
        suf = b["sid"][len(b["nation"]):]
        by_suffix_pn[suf].append(b)
    by_suffix_c = defaultdict(list)
    for b in data["buildings"]:
        if b["kind"] != "common":
            continue
        suf = b["sid"][3:]
        by_suffix_c[suf].append(b)
    A("**[Постройки по нациям](#постройки-по-нациям)**")
    for suf in ["cen", "hou", "bar", "ba2", "bla", "sta", "tem", "aca", "art", "dip"]:
        if by_suffix_pn.get(suf):
            label = f"{suf} — {PER_NAT_NAMES.get(suf, suf)}"
            anchor = heading_anchor(label)
            A(f"  - [{label}](#{anchor})")
    A("**[Общие постройки (по кластерам)](#общие-постройки-по-кластерам)**")
    for suf in ["mil", "sto", "mar", "por", "tow", "gol", "iro", "coa", "swa", "sga", "wga", "wwa"]:
        if by_suffix_c.get(suf):
            label = f"{suf} — {COMMON_NAMES.get(suf, suf)}"
            anchor = heading_anchor(label)
            A(f"  - [{label}](#{anchor})")
    A("**[Шахты — апгрейды (gol/iro/coa)](#шахты--апгрейды-goliroсoa)**")
    A("")
    A("## Постройки по нациям\n")
    A("Сводка: для каждого типа зданий — параметры по всем нациям (где они есть). "
      "**Жирным** — отклонения от базового значения (мода по столбцу).\n")
    for suf in ["cen", "hou", "bar", "ba2", "bla", "sta", "tem", "aca", "art", "dip"]:
        rows = sorted(by_suffix_pn.get(suf, []), key=lambda x: x["nation"])
        if not rows:
            continue
        A(f"### {suf} — {PER_NAT_NAMES.get(suf, suf)}\n")
        baseline_cols = ["hp", "buildtime_sec", "costpercent",
                          "food", "wood", "stone", "gold", "iron", "coal", "farm"]
        baselines = compute_baselines(rows, baseline_cols)
        A("| Здание | Нация | HP | Время (с) | cost% | F | W | S | G | I | C | ферма | производит |")
        A("|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|")
        for b in rows:
            produces = b.get("produces") or []
            prod_str = ", ".join(produces[:5]) + (f" (+{len(produces)-5})" if len(produces) > 5 else "")
            A(f"| {name_cell_short(b)} | {b['nation']} "
              f"| {bold_if(b['hp'], baselines['hp'])} "
              f"| {bold_if(b['buildtime_sec'], baselines['buildtime_sec'])} "
              f"| {bold_if(b['costpercent'], baselines['costpercent'])} "
              f"| {bold_if(b['food'], baselines['food'])} "
              f"| {bold_if(b['wood'], baselines['wood'])} "
              f"| {bold_if(b['stone'], baselines['stone'])} "
              f"| {bold_if(b['gold'], baselines['gold'])} "
              f"| {bold_if(b['iron'], baselines['iron'])} "
              f"| {bold_if(b['coal'], baselines['coal'])} "
              f"| {bold_if(b['farm'], baselines['farm'])} "
              f"| {prod_str or '—'} |")
        A("")
    A("## Общие постройки (по кластерам)\n")
    for suf in ["mil", "sto", "mar", "por", "tow", "gol", "iro", "coa", "swa", "sga", "wga", "wwa"]:
        rows = by_suffix_c.get(suf, [])
        if not rows:
            continue
        by_sid = defaultdict(list)
        for b in rows:
            by_sid[b["sid"]].append(b)
        A(f"### {suf} — {COMMON_NAMES.get(suf, suf)}\n")
        A("| Здание (cluster) | Нации | HP | Время (с) | cost% | F | W | S | G | I | C | Доп. |")
        A("|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|")
        for sid in sorted(by_sid.keys()):
            entries = by_sid[sid]
            nats = ", ".join(sorted(b["nation"] for b in entries))
            b = entries[0]
            extra = []
            if b["weapon_damage"]:
                extra.append(f"урон {b['weapon_damage']}")
                if b["weapon_radiusmax"]:
                    extra.append(f"дальн. {round(b['weapon_radiusmax']/53.3333, 1)}t")
            if b["consume"]:
                extra.append(f"содержание {json.dumps(b['consume'])}")
            if b["produce"]:
                extra.append(f"производит {json.dumps(b['produce'])}")
            if b["peasantabsorber"]:
                extra.append(f"крестьян {b['peasantabsorber']}")
            extra_str = "; ".join(extra) if extra else "—"
            A(f"| {name_cell_short(b)} | {nats} | {fmt(b['hp'])} | {fmt(b['buildtime_sec'])} "
              f"| {fmt(b['costpercent'])} | {fmt(b['food'])} | {fmt(b['wood'])} "
              f"| {fmt(b['stone'])} | {fmt(b['gold'])} | {fmt(b['iron'])} "
              f"| {fmt(b['coal'])} | {extra_str} |")
        A("")
    A("## Шахты — апгрейды (gol/iro/coa)\n")
    A("Каждая шахта начинается с `peasantabsorber=5`. 6 апгрейдов накопительно доводят до "
      "**95 крестьян** на шахту.\n")
    mine_ups = sorted([u for u in data["upgrades"]
                       if u["sid"].startswith("eurgol.") and u["nation"] == "aus"],
                       key=lambda x: x["sid"])
    A("| Уровень | +работников | Еда | Золото | Накопительно |")
    A("|---|---:|---:|---:|---:|")
    cum = 5
    for u in mine_ups:
        cum += u.get("value") or 0
        A(f"| `{u['sid']}` | +{u['value']} | {u['food']} | {u['gold']} | {cum} |")
    write_md(TREE_ROOT / "03_buildings.md", out)


# ---------- 04_units.md ----------

def write_units(data: dict) -> None:
    out = []
    A = out.append
    A("# 04. Юниты\n")
    A("[← Index](README.md)\n")
    A("Все юниты сгруппированы по классу. Для параллельного сравнения внутри класса см. "
      "[compare/](compare/README.md).\n")
    by_class = defaultdict(list)
    for u in data["units"]:
        cls = classify_unit(u["sid"], u.get("usage_short", ""))
        by_class[cls].append(u)
    class_order = [
        "Peasant",
        "Pikemen 17c", "Pikemen 18c",
        "Light Infantry", "Musketeers 17c", "Musketeers 18c",
        "Grenadiers", "Archers", "18c special infantry",
        "Light Cavalry", "Dragoons", "Heavy Cavalry",
        "Cannons", "Mortars",
        "Fishing Boat", "Warships",
        "Officer", "Drummer / Bagpiper", "Priest",
        "Misc / mission", "Other",
    ]
    # Build list of classes with content (preserving order)
    classes_with_content = []
    seen_classes = set()
    for cls in class_order + sorted(c for c in by_class if c not in class_order):
        if cls in seen_classes:
            continue
        seen_classes.add(cls)
        if by_class.get(cls):
            classes_with_content.append(cls)

    # Generate TOC
    A("## Содержание\n")
    for cls in classes_with_content:
        units = by_class[cls]
        by_sid = defaultdict(list)
        for u in units:
            by_sid[u["sid"]].append(u)
        cls_label = cls_ru(cls)
        anchor = heading_anchor(f"{cls_label} {len(by_sid)} вариантов")
        A(f"- [{cls_label}](#{anchor}) ({len(by_sid)} вариантов)")
    A("")

    for cls in classes_with_content:
        units = by_class[cls]
        by_sid = defaultdict(list)
        for u in units:
            by_sid[u["sid"]].append(u)
        A(f"## {cls_ru(cls)} ({len(by_sid)} вариантов)\n")
        A("| Юнит | нации | HP | Время | F | G | I | урон | дальн. (тайл.) | перезарядка | пика | меч | пуля | картечь | стрела | ядро |")
        A("|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|")
        for sid in sorted(by_sid.keys()):
            entries = by_sid[sid]
            u = entries[0]
            w0 = (u["weapons"] or [{}])[0]
            nat_count = len(entries)
            if nat_count >= 18:
                nat_str = "all"
            elif nat_count == 1:
                nat_str = entries[0]["nation"]
            else:
                nat_str = ",".join(sorted(set(e["nation"] for e in entries)))
            A(f"| {name_cell_short(u)} | {nat_str} "
              f"| {fmt(u['hp'])} | {fmt(u['buildtime_sec'])} "
              f"| {fmt(u['food'])} | {fmt(u['gold'])} | {fmt(u['iron'])} "
              f"| {fmt(w0.get('damage'))} | {fmt(w0.get('radiusmax_tiles'))} | {fmt(w0.get('pause_sec'))} "
              f"| {fmt(u['prot_pike'])} | {fmt(u['prot_sword'])} | {fmt(u['prot_bullet'])} "
              f"| {fmt(u['prot_cannister'])} | {fmt(u['prot_arrow'])} | {fmt(u['prot_cannonball'])} |")
        A("")
    write_md(TREE_ROOT / "04_units.md", out)


# ---------- 05_upgrades.md ----------

def write_upgrades(data: dict) -> None:
    out = []
    A = out.append
    A("# 05. Апгрейды\n")
    A("[← Index](README.md)\n")
    A("Апгрейды сгруппированы по **месту** (academy/blacksmith/mill/stable/barracks/mine/tower/wall/...). "
      "Каждый апгрейд — `<nat><place>.<unit>.<itype>.<level>` (поюнитные, в кузнице/конюшне/казарме), "
      "`<nat><place>.<level>` (один на нацию, в академии/мельнице/ратуше), "
      "или `<cluster><place>.<level>` (общие для кластера: tower/wall/shipyard).\n")
    A("Колонка `itype_short` расшифровывает raw `gc_upg_type_*` в человеческие термины.\n")
    # TOC will be inserted here after we know which places have content; we build it below

    PLACE_NAMES = {
        # per-nation places (`<nat><place>.<...>`)
        "aca": "Академия (исследования)",
        "bla": "Кузница (поюнитные урон/защита)",
        "bar": "Бараки 17 в. (поюнитные апгрейды)",
        "ba2": "Бараки 18 в. (поюнитные апгрейды)",
        "sta": "Конюшня (поюнитные кавалерийские)",
        "mil": "Мельница (эффективность еды)",
        "art": "Арт-склад (апгрейды пушек)",
        "tem": "Собор (апгрейды священников)",
        "cen": "Ратуша (переход эпохи)",
        "dip": "Дипцентр",
        # common-building places (`<cluster><place>.<...>`)
        "tow": "Башня (скорость перезарядки)",
        "swa": "Каменная стена (постройка ворот)",
        "wwa": "Палисад (постройка ворот)",
        "por": "Верфь (лечение)",
        # bare-name common buildings (no cluster prefix)
        "ferry": "Паром (вместимость)",
    }
    MINE_PLACES = {"eurgol", "eurcoa", "euriro"}
    # Cluster prefixes that appear before common-building suffixes (config.building_cluster).
    CLUSTER_PREFIXES = {"eur", "rus", "tur", "ukr", "spa", "por"}
    STRIP_PREFIXES = set(PLAYABLE_NATIONS) | CLUSTER_PREFIXES

    # Group by place. Try `<3-letter-prefix><place>.<...>` first (prefix ∈ playable
    # nation or cluster), fall back to bare `<place>.<...>` (e.g. `ferry.1`).
    # Note: `ba2` contains a digit, so we match literal place suffixes instead of `[a-z]+`.
    def _classify(sid: str) -> str | None:
        if sid in MINE_PLACES or any(sid.startswith(p + ".") for p in MINE_PLACES):
            return "mines"
        if len(sid) >= 3 and sid[:3] in STRIP_PREFIXES:
            for place in PLACE_NAMES:
                if sid[3:].startswith(place + ".") or sid[3:] == place:
                    return place
        for place in PLACE_NAMES:
            if sid.startswith(place + ".") or sid == place:
                return place
        return None

    by_place: dict[str, list[dict]] = defaultdict(list)
    for u in data["upgrades"]:
        place = _classify(u["sid"])
        by_place[place if place else "_other"].append(u)

    # Build TOC of places that have content
    PLACE_ORDER = ["mines", "aca", "mil", "bla", "sta", "bar", "ba2", "art", "tem",
                   "cen", "dip", "tow", "swa", "wwa", "por", "ferry"]
    A("## Содержание\n")
    for place in PLACE_ORDER:
        if not by_place.get(place):
            continue
        if place == "mines":
            label = "Апгрейды шахт (eurgol/eurcoa/euriro)"
        else:
            label = f"{place} — {PLACE_NAMES.get(place, place)}"
        anchor = heading_anchor(label)
        A(f"- [{label}](#{anchor})")
    A("")

    A("## Апгрейды шахт (eurgol/eurcoa/euriro)\n")
    A("Универсальные для всех наций (sid не зависит от нации). 6 уровней × 3 типа шахты.\n")
    mine_ups = [u for u in by_place.get("mines", []) if u["nation"] == "aus"]
    mine_ups.sort(key=lambda x: x["sid"])
    A("| Апгрейд | уровень | +работников | F | G |")
    A("|---|---:|---:|---:|---:|")
    for u in mine_ups:
        A(f"| {name_cell_short(u)} | {fmt(u['level'])} | +{u['value']} | {u['food']} | {u['gold']} |")
    A("")

    for place in [p for p in PLACE_ORDER if p != "mines"]:
        ups = by_place.get(place, [])
        if not ups:
            continue
        # Dedupe by stripped-sid (cross-nation/cross-cluster)
        by_stripped: dict[str, list[dict]] = defaultdict(list)
        for u in ups:
            # Strip nation OR cluster prefix
            stripped = u["sid"]
            for pref in STRIP_PREFIXES:
                if stripped.startswith(pref) and stripped[len(pref):].startswith(place):
                    stripped = stripped[len(pref):]
                    break
            by_stripped[stripped].append(u)
        A(f"## {place} — {PLACE_NAMES.get(place, place)}\n")
        A("Каждая запись — одна нация. Если значение одинаковое для всех 21 нации, показано одной строкой "
          "с `nation=all`. Если есть пер-национальное переопределение (через `_country_ModifyUpgrade`), показаны отдельно.\n")
        A("| Апгрейд | нации | itype | val | F | W | S | G | I | C | время |")
        A("|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|")
        for stripped in sorted(by_stripped.keys()):
            entries = by_stripped[stripped]
            sig: dict[tuple, list[dict]] = defaultdict(list)
            for e in entries:
                key = (e.get("value"), e["food"], e["wood"], e["stone"],
                        e["gold"], e["iron"], e["coal"])
                sig[key].append(e)
            for key, group in sorted(sig.items(), key=lambda kv: -len(kv[1])):
                first = group[0]
                nat_count = len(group)
                if nat_count >= 18:
                    nat_str = "all"
                elif nat_count == 1:
                    nat_str = group[0]["nation"]
                else:
                    nat_str = ",".join(sorted(g["nation"] for g in group))
                A(f"| {name_cell_short(first)} | {nat_str} "
                  f"| {first.get('itype_short') or '—'} | {fmt(first['value'])} "
                  f"| {fmt(first['food'])} | {fmt(first['wood'])} | {fmt(first['stone'])} "
                  f"| {fmt(first['gold'])} | {fmt(first['iron'])} | {fmt(first['coal'])} "
                  f"| {fmt(first['time_sec'])} |")
        A("")
    write_md(TREE_ROOT / "05_upgrades.md", out)


# ---------- 06_market.md ----------

def write_market(data: dict) -> None:
    out = []
    A = out.append
    A("# 06. Рынок\n")
    A("[← Index](README.md)\n")
    A("## Курсы обмена\n")
    A("Каждый ресурс имеет диапазон цен **buy** (когда покупаешь его) и **sell** (когда продаёшь). "
      "После сделки цены **сдвигаются**: покупка двигает `buycost` к `buycostmax`, продажа двигает "
      "`sellcost` к `sellcostmin`. Поэтому **повторные операции с одним ресурсом дают всё хуже курс**.\n")
    A("| Ресурс | buy_min | buy_def | buy_max | sell_min | sell_def | sell_max |")
    A("|---|---:|---:|---:|---:|---:|---:|")
    for res, vals in data.get("market_rates", {}).items():
        if res.startswith("_"): continue
        A(f"| {res} | {vals['buycostmin']:.0f} | {vals['buycostdef']:.2f} | {vals['buycostmax']:.0f} "
          f"| {vals['sellcostmin']:.2f} | {vals['sellcostdef']:.2f} | {vals['sellcostmax']:.2f} |")
    A("")
    A("## Формула обмена\n")
    A("```")
    A("received_Y = sold_X * sellcost[X] / buycost[Y]")
    A("```")
    A("\n## Примеры (при default ценах)\n")
    rates = data.get("market_rates", {})
    examples = [
        ("food", "wood", 100), ("food", "gold", 100),
        ("gold", "wood", 100), ("gold", "food", 100),
        ("iron", "food", 100), ("wood", "stone", 100),
    ]
    A("| Sell | Получишь | Buy | По формуле |")
    A("|---|---:|---|---|")
    for sell, buy, amount in examples:
        sd = rates.get(sell, {}).get("sellcostdef", 0)
        bd = rates.get(buy, {}).get("buycostdef", 0)
        if bd:
            received = round(amount * sd / bd, 1)
            A(f"| {amount} {sell} | **{received}** | {buy} | "
              f"{amount} × {sd:.2f} / {bd:.2f} |")
    A("")
    A("## Деградация\n")
    A("После каждой сделки `buycost` растёт к `buycostmax`, `sellcost` падает к `sellcostmin`. "
      "Скорость восстановления — `gc_economy_time = 0.0001 × time_to_frames = 0.0032`/тик. "
      "В UI это выглядит как «курс становится хуже после многих обменов и медленно восстанавливается».\n")
    A("Источник: `res.script:_res_InitEconomy` (lines 178-249), "
      "`res.script:_res_MarketTradeResources` (lines 320-344).\n")
    write_md(TREE_ROOT / "06_market.md", out)


# ---------- nations/ ----------

def write_nations(data: dict) -> None:
    nations_dir = TREE_ROOT / "nations"
    nations_dir.mkdir(parents=True, exist_ok=True)

    nation_name = {n["sid"]: (n["name_en"] or n["sid"]) for n in data["nations"]}
    nation_name_ru = {n["sid"]: (n["name_ru"] or n["sid"]) for n in data["nations"]}
    cluster_peasant = {
        "aus": "peaaus", "fra": "peaeng", "eng": "peaeng", "spa": "peaspa", "rus": "pearus",
        "ukr": "peaukr", "pol": "peapol", "swe": "peaeng", "pru": "peaaus", "ven": "peaspa",
        "tur": "peatur", "alg": "peatur", "net": "peaeng", "den": "peaeng", "por": "peaspa",
        "pie": "peaspa", "sax": "peaaus", "bav": "peaaus", "hun": "peapol", "swi": "peaaus",
        "sco": "peasco",
    }

    # Index page
    out = []
    A = out.append
    A("# Нации\n")
    A("[← Index](../README.md)\n")
    A("Полный список 21 доступной нации. Каждая ссылка — отдельная справка "
      "с уникальными юнитами, зданиями, апгрейдами и зависимостями.\n")
    A("| ID | sid | англ. | рус. | кластер | крестьянин | уникальные юниты |")
    A("|---:|---|---|---|---|---|---|")

    # Compute uniques per nation
    sid_to_nations: dict[str, set[str]] = {}
    for u in data["units"]:
        sid_to_nations.setdefault(u["sid"], set()).add(u["nation"])

    for i, nat in enumerate(PLAYABLE_NATIONS):
        en = nation_name.get(nat, nat)
        ru = nation_name_ru.get(nat, nat)
        unique_units = sorted(sid for sid, nations in sid_to_nations.items()
                              if nations == {nat})
        # filter out priests/officers/peasants
        unique_filter = [u for u in unique_units
                         if not u.startswith("pea") and not u.startswith("officer")
                         and not u.startswith("drummer") and u not in ("priest","padre","pope","mullah")]
        unique_str = ", ".join(unique_filter[:5]) + (f" (+{len(unique_filter)-5})"
                                                       if len(unique_filter) > 5 else "")
        A(f"| {i} | [`{nat}`]({nat}.md) | {en} | {ru} | `{_commonname(nat)}` | "
          f"`{cluster_peasant.get(nat, '?')}` | {unique_str or '—'} |")
    A("")
    write_md(nations_dir / "README.md", out)

    # Per-nation files
    units_by_nation = defaultdict(list)
    for u in data["units"]:
        units_by_nation[u["nation"]].append(u)
    builds_by_nation = defaultdict(list)
    for b in data["buildings"]:
        builds_by_nation[b["nation"]].append(b)
    upgrades_by_nation = defaultdict(list)
    for u in data["upgrades"]:
        upgrades_by_nation[u["nation"]].append(u)
    officers_by_nation = defaultdict(list)
    for o in data.get("officers", []):
        officers_by_nation[o["nation"]].append(o)

    for nat in PLAYABLE_NATIONS:
        out = []
        A = out.append
        en = nation_name.get(nat, nat)
        ru = nation_name_ru.get(nat, nat)
        A(f"# {en} (`{nat}`)")
        A(f"_{ru}_\n")
        A(f"[← Index](../README.md) · [← Все нации](README.md)\n")
        A("## Кластер\n")
        cluster = _commonname(nat)
        A(f"- **Общий кластер:** `{cluster}` (mill/sto/mar/tow используют суффикс `{cluster}+`)")
        A(f"- **Peasant:** `{cluster_peasant.get(nat, '?')}`")
        A(f"- **Кластерная пехота:** кластер `{cluster}`")
        A("")
        # Uniques
        unique_units = sorted(sid for sid, nations in sid_to_nations.items()
                              if nations == {nat})
        A(f"## Уникальные юниты ({len(unique_units)})\n")
        if unique_units:
            A("| Юнит | роль | HP | урон | перезарядка | дальн. (тайл.) |")
            A("|---|---|---:|---:|---:|---:|")
            for sid in unique_units:
                rows = [u for u in units_by_nation[nat] if u["sid"] == sid]
                if rows:
                    u = rows[0]
                    w0 = (u["weapons"] or [{}])[0]
                    A(f"| {name_cell_full(u)} | {usage_ru(u.get('usage_short'))} "
                      f"| {fmt(u['hp'])} | {fmt(w0.get('damage'))} | {fmt(w0.get('pause_sec'))} "
                      f"| {fmt(w0.get('radiusmax_tiles'))} |")
        else:
            A("(нет уникальных юнитов)")
        A("")
        # Buildings
        A("## Здания\n")
        bldgs = sorted(builds_by_nation[nat], key=lambda x: (x["kind"], x["sid"]))
        per_nat_b = [b for b in bldgs if b["kind"] == "per-nation"]
        common_b = [b for b in bldgs if b["kind"] == "common"]
        # Per-nation buildings: bold values that differ from the cross-nation baseline
        # of the same suffix (so e.g. Austria's fast Town Hall lights up).
        # Build cross-nation baselines per suffix.
        suffix_baselines: dict[str, dict] = {}
        for b in per_nat_b:
            suf = b["sid"][len(nat):]
            if suf not in suffix_baselines:
                same_suffix_rows = [bb for bb in data["buildings"]
                                    if bb["kind"] == "per-nation" and bb["sid"].endswith(suf)]
                suffix_baselines[suf] = compute_baselines(
                    same_suffix_rows,
                    ["hp", "buildtime_sec", "costpercent", "food", "wood", "stone",
                     "gold", "iron", "coal", "farm"])
        A(f"### Уникальные для нации ({len(per_nat_b)})\n")
        A("> **Жирным** — значения, отличающиеся от базовых (мода по всем нациям) "
          "для того же типа здания.\n")
        A("| Здание | HP | Время | cost% | F | W | S | G | I | C | ферма | производит |")
        A("|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|")
        for b in per_nat_b:
            suf = b["sid"][len(nat):]
            base = suffix_baselines.get(suf, {})
            produces = b.get("produces") or []
            prod_str = ", ".join(produces[:5]) + (f" (+{len(produces)-5})" if len(produces) > 5 else "")
            A(f"| {name_cell_full(b)} "
              f"| {bold_if(b['hp'], base.get('hp'))} "
              f"| {bold_if(b['buildtime_sec'], base.get('buildtime_sec'))} "
              f"| {bold_if(b['costpercent'], base.get('costpercent'))} "
              f"| {bold_if(b['food'], base.get('food'))} "
              f"| {bold_if(b['wood'], base.get('wood'))} "
              f"| {bold_if(b['stone'], base.get('stone'))} "
              f"| {bold_if(b['gold'], base.get('gold'))} "
              f"| {bold_if(b['iron'], base.get('iron'))} "
              f"| {bold_if(b['coal'], base.get('coal'))} "
              f"| {bold_if(b['farm'], base.get('farm'))} "
              f"| {prod_str or '—'} |")
        A("")
        A(f"### Общий кластер ({len(common_b)})\n")
        A("| Здание | HP | Время | cost% | F | W | S | G | I | C | Доп. |")
        A("|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|")
        for b in common_b:
            extra = []
            if b["weapon_damage"]: extra.append(f"урон {b['weapon_damage']}")
            if b["consume"]: extra.append(f"содержание {json.dumps(b['consume'])}")
            if b["produce"]: extra.append(f"производит {json.dumps(b['produce'])}")
            if b["peasantabsorber"]: extra.append(f"+{b['peasantabsorber']} работников")
            extra_str = "; ".join(extra) if extra else "—"
            A(f"| {name_cell_full(b)} | {fmt(b['hp'])} | {fmt(b['buildtime_sec'])} "
              f"| {fmt(b['costpercent'])} | {fmt(b['food'])} | {fmt(b['wood'])} | {fmt(b['stone'])} "
              f"| {fmt(b['gold'])} | {fmt(b['iron'])} | {fmt(b['coal'])} | {extra_str} |")
        A("")
        # Units by class
        A("## Юниты по классам\n")
        by_class = defaultdict(list)
        for u in units_by_nation[nat]:
            cls = classify_unit(u["sid"], u.get("usage_short", ""))
            by_class[cls].append(u)
        class_order = [
            "Peasant",
            "Pikemen 17c", "Pikemen 18c", "Light Infantry", "Musketeers 17c", "Musketeers 18c",
            "Grenadiers", "Archers", "18c special infantry",
            "Light Cavalry", "Dragoons", "Heavy Cavalry",
            "Cannons", "Mortars", "Fishing Boat", "Warships",
            "Officer", "Drummer / Bagpiper", "Priest",
        ]
        seen = set()
        for cls in class_order + sorted(c for c in by_class if c not in class_order):
            if cls in seen:
                continue
            seen.add(cls)
            units = by_class.get(cls, [])
            if not units:
                continue
            A(f"### {cls_ru(cls)}\n")
            A("| Юнит | HP | Время | F | G | I | урон | дальн. (тайл.) | перезарядка | уникальность |")
            A("|---|---:|---:|---:|---:|---:|---:|---:|---:|---|")
            for u in sorted(units, key=lambda x: x["sid"]):
                w0 = (u["weapons"] or [{}])[0]
                A(f"| {name_cell_full(u)} | {fmt(u['hp'])} | {fmt(u['buildtime_sec'])} "
                  f"| {fmt(u['food'])} | {fmt(u['gold'])} | {fmt(u['iron'])} "
                  f"| {fmt(w0.get('damage'))} | {fmt(w0.get('radiusmax_tiles'))} | {fmt(w0.get('pause_sec'))} "
                  f"| {u.get('uniqueness') or '—'} |")
            A("")
        # Officers
        offs = officers_by_nation.get(nat, [])
        A(f"## Офицеры ({len(offs)} групп)\n")
        if offs:
            A("Каждый офицер ведёт строй из своих юнитов. Формации стандартные: "
              "**LINE / SQUARE / KARE × 15/36/72/120/196/400**.\n")
            A("| офицер | барабанщик | юниты |")
            A("|---|---|---|")
            for o in offs:
                units = o.get("units", [])
                unit_str = ", ".join(units[:8]) + (f" (+{len(units)-8})" if len(units) > 8 else "")
                A(f"| `{o['officersid']}` | `{o['drummersid']}` | {unit_str or '—'} |")
        A("")
        # Upgrades summary
        ups = upgrades_by_nation.get(nat, [])
        A(f"## Апгрейды ({len(ups)})\n")
        A(f"Полный список — в [05_upgrades.md](../05_upgrades.md).\n")
        # Show counts by place
        place_counts = defaultdict(int)
        for u in ups:
            sid = u["sid"]
            for p in ("aca", "bla", "sta", "bar", "ba2", "mil", "art", "tem", "cen", "dip"):
                if sid.startswith(nat + p):
                    place_counts[p] += 1
                    break
            else:
                if any(sid.startswith(s) for s in ("eurgol.", "eurcoa.", "euriro.")):
                    place_counts["mines"] += 1
        if place_counts:
            A("По зданиям:\n")
            for p in ("aca", "mil", "bla", "sta", "bar", "ba2", "art", "tem", "cen", "dip", "mines"):
                if place_counts.get(p):
                    A(f"- **{p}** ({PER_NAT_NAMES.get(p) or COMMON_NAMES.get(p) or 'Mine' if p == 'mines' else p}): {place_counts[p]}")
        write_md(nations_dir / f"{nat}.md", out)


# ---------- compare/ ----------

def write_compare(data: dict) -> None:
    cmp_dir = TREE_ROOT / "compare"
    cmp_dir.mkdir(parents=True, exist_ok=True)

    by_class = defaultdict(list)
    for u in data["units"]:
        cls = classify_unit(u["sid"], u.get("usage_short", ""))
        by_class[cls].append(u)

    # Index
    out = []
    A = out.append
    A("# Сравнения\n")
    A("[← Index](../README.md)\n")
    A("Параллельные таблицы юнитов одного класса по всем нациям. Помогает выбирать пика-против-пики, "
      "стрельца-против-стрельца и т.д.\n")
    A("| Файл | Что сравнивает |")
    A("|---|---|")
    A("| [pikemen.md](pikemen.md) | Все 17c пикинеры |")
    A("| [pikemen18.md](pikemen18.md) | Все 18c пикинеры |")
    A("| [light_infantry.md](light_infantry.md) | Light Infantry / swordsmen |")
    A("| [musketeers17.md](musketeers17.md) | Все 17c мушкетёры (Musketeer/Strelet/Janissary) |")
    A("| [musketeers18.md](musketeers18.md) | Все 18c мушкетёры |")
    A("| [grenadiers.md](grenadiers.md) | Гренадёры |")
    A("| [archers.md](archers.md) | Лучники |")
    A("| [light_cavalry.md](light_cavalry.md) | Лёгкая кавалерия (Hussar, Lancer, Cossack) |")
    A("| [dragoons.md](dragoons.md) | Драгуны |")
    A("| [heavy_cavalry.md](heavy_cavalry.md) | Тяжёлая кавалерия |")
    A("| [siege.md](siege.md) | Артиллерия (пушки, мортиры) |")
    A("| [ships.md](ships.md) | Корабли (рыбацкие, военные, transport) |")
    A("| [town_halls.md](town_halls.md) | Town Halls по всем нациям |")
    A("| [barracks.md](barracks.md) | Barracks 17c и 18c |")
    A("| [peasants.md](peasants.md) | 8 типов крестьян |")
    A("| [weapons.md](weapons.md) | Каталог уникальных weaponsid (снаряды, стрелы, ядра, гранаты) с stats и носителями |")
    A("")
    write_md(cmp_dir / "README.md", out)

    def write_unit_compare(filename: str, classes: list[str], title: str, intro: str) -> None:
        out = []
        A = out.append
        A(f"# {title}\n")
        A("[← compare/](README.md) · [← Index](../README.md)\n")
        A(intro + "\n")
        A("> **Жирным** выделены значения, отличающиеся от базовых (мода по столбцу). "
          "Так сразу видно, какой из юнитов «особенный» в этой колонке.\n")
        # Collect rows
        rows = []
        for cls in classes:
            for u in by_class.get(cls, []):
                rows.append(u)
        # Flatten weapons[0] into top-level for column access
        flat_rows = []
        seen = set()
        for u in sorted(rows, key=lambda x: (x["sid"], x["nation"])):
            key = (u["sid"], u["nation"])
            if key in seen:
                continue
            seen.add(key)
            w0 = (u["weapons"] or [{}])[0]
            flat = {
                "sid": u["sid"], "nation": u["nation"],
                "name_en": u.get("name_en") or "",
                "name_ru": u.get("name_ru") or "",
                "hp": u.get("hp"), "buildtime_sec": u.get("buildtime_sec"),
                "food": u.get("food"), "gold": u.get("gold"), "iron": u.get("iron"),
                "wood": u.get("wood"), "stone": u.get("stone"), "coal": u.get("coal"),
                "damage": w0.get("damage"),
                "radiusmax_tiles": w0.get("radiusmax_tiles"),
                "pause_sec": w0.get("pause_sec"),
                "prot_pike": u.get("prot_pike"),
                "prot_sword": u.get("prot_sword"),
                "prot_bullet": u.get("prot_bullet"),
                "prot_cannister": u.get("prot_cannister"),
                "prot_arrow": u.get("prot_arrow"),
                "prot_cannonball": u.get("prot_cannonball"),
                "uniqueness": u.get("uniqueness") or "",
            }
            flat_rows.append(flat)

        # Compute baselines (mode) for each numeric column
        baseline_cols = ["hp", "buildtime_sec", "food", "gold", "iron",
                          "damage", "radiusmax_tiles", "pause_sec",
                          "prot_pike", "prot_sword", "prot_bullet",
                          "prot_cannister", "prot_arrow", "prot_cannonball"]
        baselines = compute_baselines(flat_rows, baseline_cols)

        A("| Юнит | Нация | HP | Время | F | G | I | урон | дальн. (тайл.) | перезарядка | пика | меч | пуля | картечь | стрела | ядро | уникальность |")
        A("|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|")
        for r in flat_rows:
            A(f"| {name_cell_short(r)} | {r['nation']} "
              f"| {bold_if(r['hp'], baselines['hp'])} "
              f"| {bold_if(r['buildtime_sec'], baselines['buildtime_sec'])} "
              f"| {bold_if(r['food'], baselines['food'])} "
              f"| {bold_if(r['gold'], baselines['gold'])} "
              f"| {bold_if(r['iron'], baselines['iron'])} "
              f"| {bold_if(r['damage'], baselines['damage'])} "
              f"| {bold_if(r['radiusmax_tiles'], baselines['radiusmax_tiles'])} "
              f"| {bold_if(r['pause_sec'], baselines['pause_sec'])} "
              f"| {bold_if(r['prot_pike'], baselines['prot_pike'])} "
              f"| {bold_if(r['prot_sword'], baselines['prot_sword'])} "
              f"| {bold_if(r['prot_bullet'], baselines['prot_bullet'])} "
              f"| {bold_if(r['prot_cannister'], baselines['prot_cannister'])} "
              f"| {bold_if(r['prot_arrow'], baselines['prot_arrow'])} "
              f"| {bold_if(r['prot_cannonball'], baselines['prot_cannonball'])} "
              f"| {r['uniqueness'] or '—'} |")
        # Footer with baseline reminder
        A("")
        A("**Базовые значения (мода по столбцу):** "
          + ", ".join(f"{k}={v}" for k, v in baselines.items()
                       if v is not None) + ".")
        write_md(cmp_dir / filename, out)

    write_unit_compare("pikemen.md", ["Pikemen 17c"], "Пикинеры 17 век",
                        "Базовая пехота ближнего боя с пиками. Эффективна против кавалерии (высокая защита от cannister).")
    write_unit_compare("pikemen18.md", ["Pikemen 18c"], "Пикинеры 18 век",
                        "Поздние пикинеры с улучшенной бронёй.")
    write_unit_compare("light_infantry.md", ["Light Infantry"], "Лёгкая пехота",
                        "Лёгкая пехота с мечом/саблей. Дешевле пикинеров, слабее против кавалерии.")
    write_unit_compare("musketeers17.md", ["Musketeers 17c"], "Мушкетёры 17 век",
                        "Стрелки с пулевым оружием. У каждой нации свой вариант. Стрелец (rus), Янычар (tur), Сердюк (ukr).")
    write_unit_compare("musketeers18.md", ["Musketeers 18c"], "Мушкетёры 18 век",
                        "Поздние мушкетёры — выше урон, лучше броня.")
    write_unit_compare("grenadiers.md", ["Grenadiers"], "Гренадёры",
                        "Метатели гранат + мушкет. Против зданий и башен.")
    write_unit_compare("archers.md", ["Archers"], "Лучники",
                        "Лук/стрелы. Выгоднее против тяжёлой пехоты с низкой защитой от стрел.")
    write_unit_compare("light_cavalry.md", ["Light Cavalry"], "Лёгкая кавалерия",
                        "Лёгкая конница с саблей/копьём, fasthorse speed=96.")
    write_unit_compare("dragoons.md", ["Dragoons"], "Драгуны",
                        "Конные стрелки. Тактика «ударь и беги».")
    write_unit_compare("heavy_cavalry.md", ["Heavy Cavalry"], "Тяжёлая кавалерия",
                        "Reiter, Cuirassier, Vityaz, Winged Hussar — таран.")
    write_unit_compare("siege.md", ["Cannons", "Mortars"], "Артиллерия",
                        "Пушка (cannonball/cannister), мортира (против зданий). Speed=20-24.")
    write_unit_compare("ships.md", ["Fishing Boat", "Warships"], "Корабли",
                        "Морские юниты. Рыбацкая лодка для еды, военные корабли — для морского боя.")
    write_unit_compare("peasants.md", ["Peasant"], "Крестьяне",
                        "8 типов крестьян (peaaus/peaeng/peapol/pearus/peaspa/peatur/peaukr/peasco). "
                        "Различия во внешности и стартовых HP.")

    # Weapons catalog (projectile-level data)
    out = []
    A = out.append
    A("# Каталог оружия (projectile-level)\n")
    A("[← compare/](README.md) · [← Index](../README.md)\n")
    A("Все уникальные `weaponsid` (типы снарядов и метательного оружия) с их параметрами и "
      "юнитами-носителями. Один `weaponsid` может использоваться разными юнитами с разными "
      "статами (damage/pause варьируются), но **kind, dispersion, projectile-id универсальны** — "
      "они задаются в самом объекте weapon (см. `weapon.script`).\n")
    A("В колонке `dmg` показан **диапазон** значений среди юнитов-носителей "
      "(`min..max`, если разные, иначе одно число). То же для `reload (s)`.\n")

    # Aggregate per weaponsid
    weapons: dict[str, list[dict]] = defaultdict(list)
    for u in data["units"]:
        for w in (u.get("weapons") or []):
            wid = w.get("weaponsid")
            if not wid:
                continue
            weapons[wid].append({
                "unit": u["sid"],
                "nation": u["nation"],
                "kind": w.get("kind"),
                "dmg": w.get("damage"),
                "pause_sec": w.get("pause_sec"),
                "rng_tiles": w.get("radiusmax_tiles"),
                "cost": w.get("cost") or {},
            })
    # Also include building-mounted weapons (towers, ports)
    for b in data["buildings"]:
        wid = None
        # buildings flattened weapon0 only
        if b.get("weapon_damage"):
            # We don't store weaponsid in flat building dict — but it lives in raw data,
            # try to detect by usage_short
            kind = b.get("weapon_kind")
            wid = "(building tower/port)"  # placeholder bucket
        # Skip building rollup — keep weapons table unit-only for clarity

    A("| weaponsid | kind | dmg | reload (s) | range (t) | cost (per shot) | Юниты-носители |")
    A("|---|---|---|---:|---:|---|---|")
    for wid in sorted(weapons.keys()):
        uses = weapons[wid]
        # Aggregate
        kind = uses[0]["kind"] or "—"
        dmgs = sorted(set(u["dmg"] for u in uses if u["dmg"] is not None))
        pauses = sorted(set(u["pause_sec"] for u in uses if u["pause_sec"] is not None))
        ranges = sorted(set(u["rng_tiles"] for u in uses if u["rng_tiles"] is not None))
        # cost typically uniform per weaponsid
        costs = set()
        for u in uses:
            if u["cost"]:
                costs.add(json.dumps(u["cost"], sort_keys=True))
        cost_str = ", ".join(sorted(costs)) if costs else "—"
        unit_sids = sorted(set(u["unit"] for u in uses))
        units_str = ", ".join(unit_sids[:6]) + (f" (+{len(unit_sids)-6})" if len(unit_sids) > 6 else "")
        def rng_str(vs):
            if not vs:
                return "—"
            if len(vs) == 1:
                return str(vs[0])
            return f"{vs[0]}..{vs[-1]}"
        A(f"| `{wid}` | {kind} | {rng_str(dmgs)} | {rng_str(pauses)} | {rng_str(ranges)} "
          f"| {cost_str} | {units_str} |")
    A("")
    A("## Заметки\n")
    A("- **`SHOTMUSKET`** — стандартный мушкетный выстрел. Используется большинством мушкетёров и "
      "драгунов. Стрелец имеет больший урон (9 против 8) при таком же снаряде.")
    A("- **`STRELA`** / **`OSTRELA`** — обычная стрела и зажигательная. Зажигательная (OSTRELA, "
      "kind=`firearrow`) — второй слот оружия у лучников.")
    A("- **`PPOINTTKOR`** — корабельное ядро (используется фрегатом, ксебеком, баттлшипом, чайкой, "
      "галерой, яхтой).")
    A("- **`PPOINTT`** vs **`PPOINTTFRAME`** — стандартное пушечное ядро против ядра framegun.")
    A("- **`PSMPOINTTPUS`** / **`PSMPOINTT`** — картечь для cannon / multi-cannon.")
    A("- **`DIMMORT1`** / **`DIMMORT2`** / **`DIMMORT2KOR`** — мортирные снаряды (1 = howitzer, "
      "2 = mortar, 2KOR = корабельная мортира галеры).")
    A("- **`NUCLGRE`** — гранадирная граната.")
    A("- **`PPOINTTTOW`** — башенно-портовое ядро (используется зданиями `tow` и `por` с пушками; "
      "не выводится в этой таблице — см. лист `Buildings` в xlsx).")
    A("\nИсточник определений: `data/scripts/lib/weapon.script` (функция `_weapon_AddWeapon`). "
      "Дополнительные параметры (gravity, propagation, fxshot) есть в скрипте, но в этот лист "
      "не выгружены — см. исходный файл при необходимости.")
    write_md(cmp_dir / "weapons.md", out)

    def write_building_compare(filename: str, sid_suffix: str, title: str, intro: str) -> None:
        out = []
        A = out.append
        A(f"# {title}\n")
        A("[← compare/](README.md) · [← Index](../README.md)\n")
        A(intro + "\n")
        A("> **Жирным** — отклонения от базовых значений (мода по столбцу).\n")
        rows = sorted([b for b in data["buildings"]
                       if b["sid"].endswith(sid_suffix) and b["kind"] == "per-nation"],
                      key=lambda x: x["nation"])
        baseline_cols = ["hp", "buildtime_sec", "costpercent", "wood", "stone", "gold", "farm"]
        baselines = compute_baselines(rows, baseline_cols)
        A("| Здание | Нация | HP | Время (с) | cost% | W | S | G | ферма | производит |")
        A("|---|---|---:|---:|---:|---:|---:|---:|---:|---|")
        for b in rows:
            produces = b.get("produces") or []
            prod_str = ", ".join(produces[:6]) + (f" (+{len(produces)-6})" if len(produces) > 6 else "")
            A(f"| {name_cell_short(b)} | {b['nation']} "
              f"| {bold_if(b['hp'], baselines['hp'])} "
              f"| {bold_if(b['buildtime_sec'], baselines['buildtime_sec'])} "
              f"| {bold_if(b['costpercent'], baselines['costpercent'])} "
              f"| {bold_if(b['wood'], baselines['wood'])} "
              f"| {bold_if(b['stone'], baselines['stone'])} "
              f"| {bold_if(b['gold'], baselines['gold'])} "
              f"| {bold_if(b['farm'], baselines['farm'])} "
              f"| {prod_str or '—'} |")
        A("")
        A("**Базовые значения:** " + ", ".join(f"{k}={v}" for k, v in baselines.items()
                                          if v is not None))
        write_md(cmp_dir / filename, out)

    write_building_compare("town_halls.md", "cen", "Ратуши (Town Halls)",
                            "Главные здания всех 21 нации. Австрийская строится за 4.69 секунды "
                            "(исключение). Украинская даёт +200 farm (макс), Российская — +75 (мин).")

    # Barracks needs two sections (17c + 18c) — special-case
    out = []
    A = out.append
    A("# Казармы (17 в. и 18 в.)\n")
    A("[← compare/](README.md) · [← Index](../README.md)\n")
    A("Казармы тренируют пехоту. У России — Стрелецкая казарма; у Украины — Казацкий дом.\n")
    A("> **Жирным** — отклонения от базовых значений.\n")
    for sid_suffix, title, note in [
        ("bar", "Казарма 17 в. (`<nat>bar`)", ""),
        ("ba2", "Казарма 18 в. (`<nat>ba2`)", "Не у всех наций (нет у `ukr`/`tur`/`alg`)."),
    ]:
        A(f"## {title}\n")
        if note:
            A(note + "\n")
        rows = sorted([b for b in data["buildings"]
                       if b["sid"].endswith(sid_suffix) and b["kind"] == "per-nation"],
                      key=lambda x: x["nation"])
        baseline_cols = ["hp", "buildtime_sec", "costpercent", "wood", "stone", "gold", "farm"]
        baselines = compute_baselines(rows, baseline_cols)
        A("| Здание | Нация | HP | Время | cost% | W | S | G | ферма | производит |")
        A("|---|---|---:|---:|---:|---:|---:|---:|---:|---|")
        for b in rows:
            produces = b.get("produces") or []
            prod_str = ", ".join(produces[:5]) + (f" (+{len(produces)-5})" if len(produces) > 5 else "")
            A(f"| {name_cell_short(b)} | {b['nation']} "
              f"| {bold_if(b['hp'], baselines['hp'])} "
              f"| {bold_if(b['buildtime_sec'], baselines['buildtime_sec'])} "
              f"| {bold_if(b['costpercent'], baselines['costpercent'])} "
              f"| {bold_if(b['wood'], baselines['wood'])} "
              f"| {bold_if(b['stone'], baselines['stone'])} "
              f"| {bold_if(b['gold'], baselines['gold'])} "
              f"| {bold_if(b['farm'], baselines['farm'])} "
              f"| {prod_str or '—'} |")
        A("")
    write_md(cmp_dir / "barracks.md", out)


# ---------- main ----------

def _version_banner(data: dict) -> str:
    """Return a one-line version banner for inclusion at the top of files."""
    v = data.get("version", {})
    if not v:
        return ""
    extracted = v.get("extracted_at_local", "?")
    mtimes = v.get("game_files_mtime", {})
    unit_mtime = mtimes.get("unit.script", "?")
    return (f"_Extracted **{extracted}** (local) from game files "
            f"(unit.script mtime: {unit_mtime})._")


def write_top_inventory(data: dict) -> None:
    """Write output/README.md — single entry-point listing every artifact."""
    out = []
    A = out.append
    A("# Cossacks 3 — каталог артефактов\n")
    banner = _version_banner(data)
    if banner:
        A(banner + "\n")
    A("Все сгенерированные файлы для справочника по игре. Главная точка входа.\n")
    A("## Начни здесь\n")
    A("**[reference/README.md](reference/README.md)** — структурированный справочник: "
      "формулы, главы, 21 нация, 16 сравнений, derived-расчёты.\n")
    A("## Структура `output/`\n")
    A("```")
    A("output/")
    A("├── README.md              ← этот файл (каталог)")
    A("├── data.json              ← сырой источник правды (~4.7 MB)")
    A("├── reference/             ← справочник по игре (~50 файлов)")
    A("│   ├── README.md          ← TL;DR + index по справочнику")
    A("│   ├── 01_economy.md … 06_market.md  ← главы по темам")
    A("│   ├── nations/           ← 21 cheatsheet по нациям")
    A("│   ├── compare/           ← 16 side-by-side сравнений")
    A("│   └── derived/           ← расчётные файлы")
    A("│       ├── scaling_prices.md      ← цены N-го здания")
    A("│       └── map_resources.md       ← ресурсы на карте")
    A("└── strategy/              ← strategy stack (планирование экономики)")
    A("    ├── README.md          ← вход в strategy: что есть, как использовать")
    A("    ├── tech_tree.{md,json}        ← граф зависимостей")
    A("    ├── production_rates.md        ← units/min для каждого здания")
    A("    └── sim/                       ← output симулятора (sim_*.csv/md)")
    A("```")
    A("")
    A("## Reference (главное)\n")
    A("[**reference/**](reference/) — структурированный справочник по игре. "
      "Открывай нужный файл напрямую, или начни с [reference/README.md](reference/README.md):\n")
    A("- **Главы:** [01_economy](reference/01_economy.md), [02_combat](reference/02_combat.md), "
      "[03_buildings](reference/03_buildings.md), [04_units](reference/04_units.md), "
      "[05_upgrades](reference/05_upgrades.md), [06_market](reference/06_market.md)")
    A("- **Нации:** [reference/nations/](reference/nations/README.md) — по одному cheatsheet на нацию")
    A("- **Сравнения:** [reference/compare/](reference/compare/README.md) — pikemen/musketeers/cavalry/ships/weapons и др. side-by-side")
    A("- **Derived:** [reference/derived/](reference/reports/) — scaling_prices (цена N-го здания) и map_resources (подсчёт на карте)")
    A("")
    A("## Strategy stack\n")
    A("Файлы для планирования и симуляции экономики — в подкаталоге [`strategy/`](strategy/):\n")
    A("| Файл | Что внутри | Скрипт |")
    A("|---|---|---|")
    A("| [strategy/README.md](strategy/README.md) | **Точка входа в strategy**: как использовать | — |")
    A("| [strategy/tech_tree.md](strategy/tech_tree.md) / [.json](derived/tech_tree.json) | Граф зависимостей зданий/юнитов/апгрейдов | `parser/build_tech_tree.py` |")
    A("| [strategy/production_rates.md](strategy/production_rates.md) | units/min для каждого здания × юнита | то же |")
    A("| [strategy/sim/](strategy/sim/) | Output симулятора (`sim_*.csv/md`) | `parser/simulate_economy.py` |")
    A("")
    A("Build orders (вход для симулятора): [`../build_orders/`](../build_orders/)\n")
    A("## Сырой JSON\n")
    A("[`data.json`](data.json) — единый источник правды, выход `parser/build_data.py`. "
      "Все writer-скрипты читают отсюда. После патча игры регенерируется.\n")
    A("## Глубокие исследования (`../recon/`)\n")
    A("Не справочник, а research notes и черновики:\n")
    A("- [`../recon/peasant_extraction.md`](../recon/peasant_extraction.md) — полный разбор механики добычи")
    A("- [`../recon/extraction_formulas.md`](../recon/extraction_formulas.md) — формульная сводка")
    A("- [`../recon/empirical_tests.md`](../recon/empirical_tests.md) — открытые вопросы для in-game замеров")
    A("- [`../recon/step1_findings.md`](../recon/step1_findings.md) — исторический recon файлов игры")
    A("- [`../recon/visual_editor_roadmap.md`](../recon/visual_editor_roadmap.md) — план визуального редактора стратегий")
    A("")
    A("## Регенерация\n")
    A("После патча игры или изменений в скриптах:\n")
    A("```")
    A("python parser/build_data.py                 # → output/data.json (источник правды)")
    A("python writers/write_md_tree.py             # → output/reference/ + output/README.md")
    A("python compute/compute_scaling.py           # → output/reference/reports/scaling_prices.md")
    A("python compute/compute_map_resources.py     # → output/reference/reports/map_resources.md")
    A("python compute/build_tech_tree.py           # → output/strategy/tech_tree.{md,json}, production_rates.md")
    A("python simulator/simulate_economy.py <build_order.json>  # → output/strategy/sim/sim_<name>.{csv,md}")
    A("```")
    A("Все writer-скрипты читают только из `data.json` — кроме `build_data.py`, "
      "который читает напрямую из файлов игры.\n")
    A("## Стат\n")
    f = data
    A(f"- Нации: **{len(f['nations'])}**")
    A(f"- Здания: **{len(f['buildings'])}** строк (sid×nation)")
    A(f"- Юниты: **{len(f['units'])}** строк")
    A(f"- Апгрейды: **{len(f['upgrades'])}** строк (с полными cost/value/itype)")
    A(f"- Офицеры: **{len(f.get('officers', []))}** групп")
    sanity = f.get("sanity_checks", [])
    n_pass = sum(1 for c in sanity if c["pass"])
    A(f"- Sanity checks: **{n_pass}/{len(sanity)}** PASS")

    write_md(OUTPUT_DIR / "README.md", out)


def main():
    data = json.loads(DATA_PATH.read_text(encoding="utf-8"))
    TREE_ROOT.mkdir(parents=True, exist_ok=True)
    print(f"Writing tree under {TREE_ROOT}…", flush=True)
    write_top_inventory(data)
    print(f"  README.md (top-level)", flush=True)
    write_readme(data)
    print("  README.md", flush=True)
    write_economy(data)
    print("  01_economy.md", flush=True)
    write_combat(data)
    print("  02_combat.md", flush=True)
    write_buildings(data)
    print("  03_buildings.md", flush=True)
    write_units(data)
    print("  04_units.md", flush=True)
    write_upgrades(data)
    print("  05_upgrades.md", flush=True)
    write_market(data)
    print("  06_market.md", flush=True)
    write_nations(data)
    print(f"  nations/ ({len(PLAYABLE_NATIONS) + 1} files)", flush=True)
    write_compare(data)
    print(f"  compare/ (~15 files)", flush=True)

    # Inventory
    files = list(TREE_ROOT.rglob("*.md"))
    print(f"\nDone. {len(files)} files, total "
          f"{sum(f.stat().st_size for f in files):,} bytes")
    by_size = sorted(files, key=lambda f: f.stat().st_size, reverse=True)
    print("Largest files:")
    for f in by_size[:8]:
        print(f"  {f.relative_to(TREE_ROOT)}: {f.stat().st_size:,} bytes")


if __name__ == "__main__":
    main()
