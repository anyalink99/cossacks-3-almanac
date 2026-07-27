"""Generate a structured markdown tree under docs/reference/.

Tree:
    reference/
    ├── README.md                  # TL;DR + index + key formulas
    ├── 01_economy/README.md       # extraction, portions, eff, mines, fields
    ├── 02_combat/README.md        # damage formula, speeds, formations
    ├── 03_buildings/README.md     # all buildings (overview tables per type)
    ├── 04_units/README.md         # all units grouped by class
    ├── 05_upgrades/README.md      # all upgrades grouped by place
    ├── 06_market/README.md        # trade rates + examples
    ├── 07_naval/README.md         # naval fleet, port, transports, fishing
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
                    MELEE_SWING_FALLBACK_SEC, melee_swing_sec,
                    USAGE_RU, NATION_NAMES_RU, NATION_NAMES_EN, nation_ru, nation_label,
                    usage_ru, WEAPON_KIND_RU, decode_upg_type, unit_ru)

DATA_PATH = DATA_JSON
TREE_ROOT = REFERENCE_DIR
RESOURCE_NAMES_RU = {
    "food": "еда",
    "wood": "дерево",
    "stone": "камень",
    "gold": "золото",
    "iron": "железо",
    "coal": "уголь",
}
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


def nations_ru(values: list[str] | set[str], *, all_threshold: int = 18) -> str:
    """Format nation codes as canonical Russian names for reader-facing tables."""
    unique = sorted(set(values))
    if len(unique) >= all_threshold:
        return "все"
    return ", ".join(nation_ru(value) for value in unique)


def resource_values_ru(values: dict | None) -> str:
    """Format a resource mapping without exposing English field names."""
    if not values:
        return "—"
    return ", ".join(
        f"{RESOURCE_NAMES_RU.get(key, key)} {value}"
        for key, value in values.items()
        if value not in (None, 0)
    ) or "—"


def upgrade_value_ru(upgrade: dict) -> str:
    """Convert encoded upgrade values into the units shown to players."""
    value = upgrade.get("value")
    if value is None:
        return "—"
    if upgrade.get("itype") == "gc_upg_type_buildtimeperc":
        percent = float(value) / 100000
        return f"{percent:g}%"
    return fmt(value)


def write_md(path: Path, lines: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")


TEMPLATES_DIR = Path(__file__).parent / "templates"


def render_template(name: str, **subs: object) -> list[str]:
    """Load `writers/templates/<name>`, apply `str.format(**subs)` if subs given,
    and return as a list of lines (compatible with the `out: list[str]` accumulator).

    Templates may contain `{var}` placeholders. To include literal `{` / `}` in
    template text (rare — almost only in code blocks), double them: `{{` / `}}`.
    Templates with no `{...}` placeholders can be loaded with `render_template(name)`.
    """
    text = (TEMPLATES_DIR / name).read_text(encoding="utf-8")
    if subs:
        text = text.format(**subs)
    return text.splitlines()


def primary_weapon(unit: dict) -> dict:
    """Pick the weapon to display in unit summary tables.

    Many 18c units have multiple weapons (musketeer18 = bayonet[0] + musket[1];
    grenadier = bayonet + musket + grenade). `weapons[0]` is often the bayonet,
    which underrepresents the unit. Heuristic: pick the weapon with maximum
    `radiusmax_tiles` (engagement range), tie-broken by `damage`. Returns {}
    for unarmed units.
    """
    ws = unit.get("weapons") or []
    if not ws:
        return {}
    return max(ws, key=lambda w: (w.get("radiusmax_tiles") or 0,
                                   w.get("damage") or 0))


def plural_ru(n: int, one: str, few: str, many: str) -> str:
    """Russian numeric agreement: 1 вариант / 2-4 варианта / 5+, 11-14 вариантов.

    Examples: plural_ru(1,'вариант','варианта','вариантов') → 'вариант'.
    """
    n_abs = abs(n) % 100
    if 11 <= n_abs <= 14:
        return many
    n1 = n_abs % 10
    if n1 == 1:
        return one
    if 2 <= n1 <= 4:
        return few
    return many


def heading_anchor(text: str) -> str:
    """Convert heading text to a slug for cross-linking — matches the algorithm
    GitHub-flavored Markdown uses to auto-id headings.

    GitHub's algorithm (kramdown / jekyll-toc):
      1. lowercase
      2. strip everything except letters/digits/spaces/hyphens/underscores
         (so parens, dots, slashes, em-dashes are removed without leaving a space)
      3. replace each space with a single hyphen — does NOT collapse multiple
         consecutive spaces, so headers like "A / B" produce "a--b" because
         the slash is removed but the spaces around it stay.

    Headers in this writer should avoid `/` and other punctuation that has
    spaces on both sides — use «и» / «,» instead.
    """
    s = text.lower()
    s = re.sub(r"[^\w\s\-]", "", s, flags=re.UNICODE)
    s = s.replace(" ", "-")
    return s


# ---------- formatting helpers ----------

def name_cell_short(item: dict) -> str:
    """Compact name cell for compare/ tables: `**RU name** ` `sid` `; falls back to EN if RU missing."""
    name_ru = (item.get("name_ru") or "").strip()
    name_en = (item.get("name_en") or "").strip()
    sid = item.get("sid", "")
    display = unit_ru(sid, name_ru or name_en)
    if display:
        return f"**{display}** `{sid}`"
    return f"`{sid}`"


def name_ru_en(item: dict) -> str:
    """Russian name from locale, fallback to English, fallback to em-dash."""
    ru = (item.get("name_ru") or "").strip()
    en = (item.get("name_en") or "").strip()
    return unit_ru(str(item.get("sid") or ""), ru or en or "—")


def name_cell_full(item: dict) -> str:
    """Canonical Russian name first, technical SID second."""
    return name_cell_short(item)


def upgrade_member_sid(item: dict) -> str | None:
    """Return the upgraded unit SID even for access-control fallback rows."""
    member = str(item.get("member") or "").strip()
    if member:
        return member
    match = re.match(
        r"^[a-z0-9]+\.([a-z0-9]+)\.[12]\.\d+$",
        str(item.get("sid") or ""),
    )
    return match.group(1) if match else None


def upgrade_display_name_ru(item: dict) -> str:
    """Reader-facing upgrade name without raw unit IDs or English effect words."""
    member = upgrade_member_sid(item)
    effect_match = re.search(r"\.([12])\.(\d+)$", str(item.get("sid") or ""))
    if member and effect_match:
        effect = "урон" if effect_match.group(1) == "1" else "защита"
        value = item.get("value")
        value_text = f"+{value}" if isinstance(value, (int, float)) and value >= 0 else fmt(value)
        level = item.get("level")
        return f"{unit_ru(member)}: {effect} {value_text} (уровень {level})"
    return name_ru_en(item).replace("%value%", fmt(item.get("value")))


def upgrade_name_cell(item: dict) -> str:
    """Canonical localized upgrade name first, technical SID second."""
    return f"**{upgrade_display_name_ru(item)}** `{item.get('sid', '')}`"


def uniqueness_ru(value: str | None) -> str:
    """Translate parser uniqueness labels for reader-facing tables."""
    if not value:
        return "—"
    exact = {
        "unique": "только у этой нации",
        "common": "общий для большинства",
    }
    if value in exact:
        return exact[value]
    match = re.fullmatch(r"semi-unique \((\d+)n\)", value)
    if match:
        return f"у {match.group(1)} наций"
    match = re.fullmatch(r"shared \((\d+)n\)", value)
    if match:
        return f"у {match.group(1)} наций"
    return value


def canonical_sid_labels(data: dict) -> dict[str, str]:
    """Return a best-effort SID → canonical Russian game label mapping."""
    labels: dict[str, str] = {}
    for category in ("units", "buildings", "upgrades"):
        for item in data.get(category, []):
            sid = str(item.get("sid") or "")
            fallback = (
                str(item.get("name_ru") or "").strip()
                or str(item.get("name_en") or "").strip()
            )
            label = unit_ru(sid, fallback)
            if sid and label:
                labels.setdefault(sid, label)
    return labels


def canonical_sid_text(
    sid: str,
    labels: dict[str, str],
    *,
    show_sid: bool = True,
) -> str:
    """Render a canonical label first and retain the technical SID second."""
    label = labels.get(sid)
    if not label:
        return f"`{sid}`"
    return f"**{label}** (`{sid}`)" if show_sid else label


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
    "Drummer / Bagpiper":    "Барабанщики и волынщики",
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
    "Misc / mission":        "Разное и миссии",
    "Other":                 "Прочее",
}

# `USAGE_RU` (English `usage_short` → Russian) is imported from `parser/config.py`
# so this writer and all `compute/*.py` reports stay in lock-step.


def cls_ru(cls: str) -> str:
    """Russian label for a `classify_unit()` class key. Falls back to the key."""
    return CLASS_RU.get(cls, cls)


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
    """Write the compact reader-facing reference landing page."""
    write_md(
        TREE_ROOT / "README.md",
        render_template("reference/main.md"),
    )


def write_readme_legacy(data: dict) -> None:
    """Former combined reference and engine-field glossary."""
    out = []
    A = out.append
    e = data["economy"]
    A("# Краткий справочник Cossacks 3\n")
    A("[← Главная энциклопедии](../README.md)\n")
    A("Здесь собраны основные игровые числа и формулы. Для быстрого ответа "
      "выберите тему, нацию или сравнение; внутренние идентификаторы показаны "
      "вторым планом и нужны только для точного различения объектов.\n")
    A("\n---\n")

    # ─── Навигация ─────────────────────────────────────────────────────
    A("## Разделы справочника\n")
    A("| Тема | Что можно узнать |")
    A("|---|---|")
    A("| [Экономика](01_economy/README.md) | Добыча ресурсов, шахты, поля, рыбалка, голод и содержание армии. |")
    A("| [Бой и движение](02_combat/README.md) | Урон, защита, дальность, скорость, построения и эффективность разных войск. |")
    A("| [Здания](03_buildings/README.md) | Цена, прочность, время строительства, вместимость и доступное производство. |")
    A("| [Юниты](04_units/README.md) | Цена, здоровье, время найма, оружие и защита всех классов войск. |")
    A("| [Улучшения](05_upgrades/README.md) | Место исследования, стоимость и эффект каждого улучшения. |")
    A("| [Рынок](06_market/README.md) | Курсы обмена, их изменение после сделок и постепенное восстановление. |")
    A("| [Флот](07_naval/README.md) | Порты, боевые корабли, транспорт и рыбацкие лодки. |")
    A("")
    A("Дополнительно: [справки по 21 нации](nations/README.md), "
      "[сравнения похожих юнитов и зданий](compare/README.md), "
      "[настройки матча](../reports/map/lobby_settings.md) и "
      "[дерево развития](../reports/tech/tech_tree.md).\n")
    A("")
    A("**Если готового числа недостаточно:**\n")
    A("| Раздел | Что внутри |")
    A("|---|---|")
    A("| [Как устроена игра](../recon/README.md) | Подробные разборы скрытых правил и поведения игры. |")
    A("| [Таблицы и расчёты](../reports/README.md) | Расширенные сравнения урона, времени, цен и национальных отличий. |")
    A("\n---\n")

    # ─── Шпаргалка по формулам ─────────────────────────────────────────
    A("## Шпаргалка по формулам\n")
    A("Канонические формулы, на которые опираются все остальные числа. "
      "Если что-то в таблицах ниже расходится с твоими ожиданиями — "
      "сначала проверь эту шпаргалку: расхождение в правом столбце "
      "обычно объясняется одной из формул здесь.\n")

    A("### Добыча ресурсов\n")
    A("| Ресурс | Порция за рейс | Ударов до сдачи | Идеальная скорость одного крестьянина без дороги |")
    A("|---|---:|---:|---:|")
    A(f"| Еда | **{e['resource_portion_food']}** | {e['hits_needed_food']} | ≈ 2,97 за игровую секунду |")
    A(f"| Дерево | **{e['resource_portion_wood']}** | {e['hits_needed_wood']} | ≈ 3,56 за игровую секунду |")
    A(f"| Камень | **{e['resource_portion_stone']}** | {e['hits_needed_stone']} | ≈ 3,56 за игровую секунду |")
    A(f"| Золото, железо или уголь | **{e['resource_portion_others']}** | — | через шахту: 1,664 на крестьянина за игровую секунду без улучшений |")
    A("")
    A("Выданный ресурс = базовая порция × эффективность добычи. Начальная "
      "эффективность равна 100 %, а бонусы улучшений складываются. Точная "
      "формула: `floor(portion × eff / 100)`. "
      "Подробности — [глава «Экономика»](01_economy/README.md).\n")

    A("### Урон в бою\n")
    A("```")
    A("итоговый урон = max(1, базовый урон оружия")
    A("                       − общий показатель брони цели")
    A("                       − защита цели от этого типа оружия")
    A("                       + бонус построения")
    A("                       + возможный бонус критического попадания)")
    A("```")
    A("Минимум 1 HP проходит всегда. Подробности — "
      "[в разборе расчёта урона, §3](../recon/world/combat/combat_damage_pipeline.md). "
      "Источник: `miscext2.script:_misc_DoDamage`.\n")

    A("### Цены и время\n")
    A("- **N-й экземпляр здания того же типа:** "
      "`cost(N) = floor(base × (costpercent / 100)^(N-1))`. "
      "Готовые таблицы N = 1..6 — в "
      "[расчёте роста цен](../reports/economy/scaling_prices.md).")
    A("- **Время постройки с N строителями:** "
      "`базовое время × 1,13 / N`. У каждого здания есть предел числа "
      "одновременно работающих крестьян (см. "
      "[пределы числа строителей](../reports/economy/builder_slots.md)).")
    A("- **Реальное время на скорости «Быстро»:** игровое время нужно "
      "разделить на 1,4. Например, 140 игровых секунд проходят за 100 реальных.\n")

    A("### Ключевые константы\n")
    A(f"- `gc_time_to_frames = {e['time_to_frames']}` — 32 кадра в одной игровой секунде.")
    A(f"- `gc_pixels_to_tile = {e['pixels_to_tile']:.4f}` — перевод `weapon.range` из пикселей в клетки (например, 800 px = 15 клеток).")
    A(f"- Лимиты карты: **{e['max_obj_count']}** объектов всего, **{e['max_player_count']}** игроков.")
    A(f"- Поле: HP = **{e['field_max_hp']}**. Шахта без апгрейдов — 5 крестьян, 1.664 ресурса / игр. с на каждого.")
    A("\n---\n")

    # ─── Глоссарий ─────────────────────────────────────────────────────
    out.extend(render_template("reference/readme/glossary.md"))
    A("\n---\n")

    A("## Откуда взяты сведения\n")
    A("Названия объектов взяты из русской локализации игры. Характеристики и "
      "формулы сверяются с игровыми данными и скриптами; спорные или ещё не "
      "проверенные выводы явно помечаются в тексте. Технические подробности "
      "извлечения данных находятся в "
      "[Internals](../../internals/README.md).")

    write_md(TREE_ROOT / "README.md", out)


# ---------- 01_economy.md ----------

# Mercenary unit sids — фиксированный порядок (по возрастанию gold-цены).
# Все наёмники доступны всем нациям, поэтому достаточно одного представителя.
MERCENARY_SIDS: list[str] = [
    "lightinfantrydip",
    "roundshierdip",
    "archerdip",
    "archerturdip",
    "grenadierdip",
    "cossacksichdip",
    "dragoon18dip",
    "lightcavalrydip",
]

# Cluster prefixes для дип-центров. Один и тот же объект (например, `ausdip` и
# `fradip`) имеет идентичные статы — фигуру дип-кластеров определяет код в
# `unit.script:2451-2459`.
DIP_CLUSTERS: list[tuple[list[str], str]] = [
    (["aus", "fra", "eng", "spa", "pol", "swe", "pru", "ven",
      "net", "den", "por", "pie", "sax", "bav", "hun", "swi", "sco"],
     "default"),
    (["rus"],          "rus"),
    (["ukr"],          "ukr"),
    (["tur", "alg"],   "tur / alg"),
]


def _dip_buildings_table(buildings: list[dict]) -> str:
    """Сгруппированная таблица Дипломатических центров: по 1 строке на кластер
    с одинаковыми статами. Имена тянутся из локали."""
    by_sid = {b["sid"]: b for b in buildings}
    L = [
        "| Вариант здания | Нации | Здоровье | Дерево | Камень | Золото |",
        "| --- | --- | ---: | ---: | ---: | ---: |",
    ]
    for nats, label in DIP_CLUSTERS:
        # Берём представителя — первая нация кластера, у которой есть `<nat>dip`.
        rep = None
        for nat in nats:
            b = by_sid.get(f"{nat}dip")
            if b is not None:
                rep = b
                break
        if rep is None:
            continue
        nat_names = [nation_ru(nat) for nat in nats]
        nat_str = ", ".join(nat_names) if len(nat_names) <= 6 else (
            ", ".join(nat_names[:5]) + f" … (+{len(nat_names) - 5})"
        )
        L.append(
            f"| {name_cell_short(rep)} | {nat_str} | "
            f"{fmt(rep.get('hp'))} | {fmt(rep.get('wood'))} | "
            f"{fmt(rep.get('stone'))} | {fmt(rep.get('gold'))} |"
        )
    return "\n".join(L)


def _mercenary_weapons_summary(unit: dict) -> str:
    """Краткое читательское описание оружия наёмника."""
    parts: list[str] = []
    for w in (unit.get("weapons") or []):
        kind = WEAPON_KIND_RU.get(w.get("kind"), w.get("kind") or "?")
        damage = w.get("damage")
        if damage is None:
            continue
        rmax = w.get("radiusmax_tiles")
        if rmax is not None and rmax > 1.5:
            parts.append(f"{kind}: {damage}, дальность {rmax}")
        else:
            parts.append(f"{kind} {damage}")
    return " / ".join(parts) if parts else "—"


def _mercenaries_table(units: list[dict]) -> str:
    """Читательская таблица характеристик наёмников."""
    by_sid: dict[str, dict] = {}
    for u in units:
        # Любой представитель — наёмники одинаковы у всех наций.
        by_sid.setdefault(u["sid"], u)
    L = [
        "| Наёмник | Здоровье | Время найма, игровых секунд | Золото | Расход золота | Оружие |",
        "| --- | ---: | ---: | ---: | ---: | --- |",
    ]
    for sid in MERCENARY_SIDS:
        u = by_sid.get(sid)
        if u is None:
            continue
        gold_cost = u.get("gold")
        consume_gold = (u.get("consume") or {}).get("gold") or "—"
        L.append(
            f"| {name_cell_short(u)} | {fmt(u.get('hp'))} "
            f"| {fmt(u.get('buildtime_sec'))} | **{fmt(gold_cost)}** "
            f"| {consume_gold} | {_mercenary_weapons_summary(u)} |"
        )
    return "\n".join(L)


def write_economy(data: dict) -> None:
    out = []
    A = out.append
    e = data["economy"]
    A("# Экономика\n")
    A("[← Краткий справочник](../README.md)\n")
    out.extend(render_template("reference/01_economy/summary.md"))
    A("")
    A("## Сколько крестьянин приносит за рейс\n")
    A("| Ресурс | Базовая порция | Ударов до сдачи |")
    A("|---|---:|---:|")
    A(f"| Еда | **{e['resource_portion_food']}** | {e['hits_needed_food']} |")
    A(f"| Дерево | **{e['resource_portion_wood']}** | {e['hits_needed_wood']} |")
    A(f"| Камень | **{e['resource_portion_stone']}** | {e['hits_needed_stone']} |")
    A(f"| Золото, железо или уголь | **{e['resource_portion_others']}** | добываются внутри шахты |")
    A("")
    out.extend(render_template("reference/01_economy/extraction_formula.md"))
    A("")
    out.extend(render_template("reference/01_economy/mines_intro.md"))
    A("")
    A("| Улучшение | Дополнительных мест | Еда | Золото | Всего мест |")
    A("|---|---:|---:|---:|---:|")
    cumulative = 5
    mine_ups = sorted([u for u in data["upgrades"]
                       if u["sid"].startswith("eurgol.") and u["nation"] == "aus"],
                       key=lambda x: x["sid"])
    for u in mine_ups:
        cumulative += u.get("value") or 0
        A(f"| {name_cell_short(u)} | +{u['value']} | {u['food']} | {u['gold']} | {cumulative} |")
    A(f"\n**Итого:** 5 базовых мест + 6 улучшений = **{cumulative} крестьян в шахте**, "
      f"или до {cumulative * 1.664:.1f} ресурса за игровую секунду "
      f"({cumulative * 99.84:.0f} за игровую минуту).\n")
    total_food_cost = sum(u['food'] for u in mine_ups)
    total_gold_cost = sum(u['gold'] for u in mine_ups)
    A(f"**Стоимость всех улучшений одной шахты:** {total_food_cost:,} еды и "
      f"{total_gold_cost:,} золота.\n")
    out.extend(render_template("reference/01_economy/fields_intro.md"))
    A("")
    A(f"Базовая прочность поля — **{e['field_max_hp']}**. Улучшения увеличивают "
      "число ударов, которое выдерживает поле, поэтому с него можно собрать больше еды.\n")
    A("| Бонус прочности | Урон полю за удар | Максимум ударов | Еды без улучшений добычи |")
    A("|---:|---:|---:|---:|")
    for fl in (0, 100, 200, 300, 500):
        resdec = max(1, 100 // (1 + fl // 100))
        max_hits = e['field_max_hp'] // resdec
        max_food = max_hits * e['resource_portion_food'] // e['hits_needed_food']
        A(f"| {fl} | {resdec} | {max_hits} | {max_food} |")
    A("\nДва улучшения прочности дают суммарный бонус 300: полностью "
      "обработанное поле приносит около **2045 еды** вместо базовых 495.\n")
    out.extend(render_template("reference/01_economy/fishing.md"))
    A("")
    out.extend(render_template(
        "reference/01_economy/famine_rebellion.md",
        dip_buildings_table=_dip_buildings_table(data["buildings"]),
        mercenaries_table=_mercenaries_table(data["units"]),
    ))
    A("")
    out.extend(render_template("reference/01_economy/recon_refs.md"))
    write_md(TREE_ROOT / "01_economy" / "README.md", out)


# ---------- 02_combat.md ----------

def write_combat(data: dict) -> None:
    """Write the reader-facing combat chapter.

    Detailed generated matrices remain available under ``docs/reports``; the
    encyclopedia chapter explains the mechanics and routes readers to them.
    """
    write_md(
        TREE_ROOT / "02_combat" / "README.md",
        render_template("reference/02_combat/main.md"),
    )


def write_combat_legacy(data: dict) -> None:
    """Former all-in-one combat report kept as generator reference."""
    out = []
    A = out.append
    e = data["economy"]
    A("# Бой и движение\n")
    A("[← Краткий справочник](../README.md)\n")
    out.extend(render_template("reference/02_combat/main.md"))
    A("## Скорости юнитов\n")
    A("Базовые `gc_obj_speed_*` из `dmscript.global:603-620`. **Абстрактные единицы** (не tiles/sec). "
      "Реальная скорость в клетках/сек зависит от animation `walkInterval`, `walkintervalfactor` "
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
        "battleship": "линейный корабль — самый медленный военный корабль",
        "chaika": "украинская чайка — мобильная",
        "ferry": "транспорт",
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
    A("Полные таблицы офицеров → секции в [nations/](../nations/README.md) для каждой нации.\n")
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
        with_dmg = [u for u in units if primary_weapon(u).get("damage")]
        if not with_dmg:
            return None
        with_dmg.sort(key=lambda x: primary_weapon(x).get("damage") or 0)
        median = with_dmg[len(with_dmg) // 2]
        w = primary_weapon(median)
        pause = w.get("pause_sec")
        if pause in (None, 0, 0.0):
            pause = melee_swing_sec(median["sid"])
        return {
            "name": (median.get("name_ru") or median.get("name_en") or median["sid"]),
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
            "name": (median.get("name_ru") or median.get("name_en") or median["sid"]),
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
    A(f"### Матрица контр-эффективности — TTK в игр. с\n")
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
      "[главе «Апгрейды»](../05_upgrades/README.md)). Цены даны для базовой нации (отличаются по "
      "нациям — см. [главу «Апгрейды»](../05_upgrades/README.md)).\n")
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
        place = "Академия" if "aca" in u["sid"] else "Мельница"
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
    A("Полный список — в [главе «Апгрейды»](../05_upgrades/README.md) (~4500 строк, по местам).\n")
    A("## Стоимость одного выстрела\n")
    A("Многие огнестрельные юниты, башни и корабли тратят `iron` / `coal` / `gold` за каждый выстрел "
      "(независимо от цены постройки самого юнита). Это отдельный налог, помимо `consume[gold]` и `food upkeep`.\n")
    A("Строки сгруппированы по `(sid, оружие)`: если значения одинаковы для всех наций, "
      "показано одной строкой со значением «все нации». Если у нации своё "
      "значение — она вынесена в отдельную строку.\n")
    A("| Юнит | Нации | weapon | урон | перезарядка (с) | shots/min | iron / выстрел | coal / выстрел | gold / выстрел |")
    A("|---|---|---|---:|---:|---:|---:|---:|---:|")
    # Collect (sid, weapon_id_or_kind) → list of (nation, item, damage, pause, shots, iron, coal, gold).
    # `item` нужен, чтобы рендерить имя через `name_cell_short` — берём первое
    # попавшееся представление каждого sid'а (имя у одного sid'а одинаково).
    grouped: dict[tuple[str, str], list[tuple]] = defaultdict(list)
    items_by_sid: dict[str, dict] = {}
    for u in data["units"]:
        items_by_sid.setdefault(u["sid"], u)
        for w in (u["weapons"] or []):
            cost = w.get("cost") or {}
            if cost:
                shots = round(60 / w["pause_sec"], 1) if w.get("pause_sec") else None
                key = (u["sid"], w["weaponsid"] or w["kind"] or "?")
                grouped[key].append((u["nation"], u, w.get("damage"), w.get("pause_sec"), shots,
                                      cost.get("iron"), cost.get("coal"), cost.get("gold")))
    for b in data["buildings"]:
        items_by_sid.setdefault(b["sid"], b)
        cost = b.get("weapon_cost") or {}
        if cost:
            pause_sec = (round(b["weapon_pause_frames"]/32, 2) if b["weapon_pause_frames"] else None)
            shots = (round(60 / pause_sec, 1) if pause_sec else None)
            key = (b["sid"], b["weapon_kind"] or "?")
            grouped[key].append((b["nation"], b, b["weapon_damage"], pause_sec, shots,
                                  cost.get("iron"), cost.get("coal"), cost.get("gold")))
    # For each (sid, weapon), bucket entries by (damage, pause, shots, iron, coal, gold) signature.
    for (sid, weapon) in sorted(grouped.keys()):
        entries = grouped[(sid, weapon)]
        sig: dict[tuple, list[str]] = defaultdict(list)
        for nation, _item, damage, pause, shots, iron, coal, gold in entries:
            sig[(damage, pause, shots, iron, coal, gold)].append(nation)
        # Sort buckets by size desc so the most common variant comes first.
        rep_item = items_by_sid.get(sid) or {}
        name_cell = name_cell_short(rep_item) if rep_item else f"`{sid}`"
        for stats, nations in sorted(sig.items(), key=lambda kv: -len(kv[1])):
            damage, pause, shots, iron, coal, gold = stats
            nat_str = nations_ru(nations)
            A(f"| {name_cell} | {nat_str} | `{weapon}` | {fmt(damage)} | {fmt(pause)} "
              f"| {fmt(shots)} | {fmt(iron)} | {fmt(coal)} | {fmt(gold)} |")
    write_md(TREE_ROOT / "02_combat" / "README.md", out)


# ---------- 03_buildings.md ----------

PER_NAT_NAMES = {
    "cen": "Городской центр", "hou": "Дом",
    "bar": "Казарма 17 в.", "ba2": "Казарма 18 в.",
    "bla": "Кузница", "sta": "Конюшня", "tem": "Собор",
    "aca": "Академия", "art": "Артиллерийское депо", "dip": "Дипломатический центр",
}
COMMON_NAMES = {
    "mil": "Мельница", "sto": "Склад", "mar": "Рынок", "por": "Порт",
    "tow": "Башня", "gol": "Золотая шахта", "iro": "Железная шахта", "coa": "Угольная шахта",
    "swa": "Каменная стена", "sga": "Каменные ворота",
    "wga": "Деревянные ворота", "wwa": "Палисад",
}


def write_buildings(data: dict) -> None:
    out = []
    A = out.append
    sid_labels = canonical_sid_labels(data)
    A("# Здания\n")
    A("[← Краткий справочник](../README.md)\n")
    A("Часть зданий имеет отдельный вариант для каждой нации, а внешний вид "
      "остальных зависит от архитектурной группы. Каноническое название всегда "
      "показано первым; внутренний код рядом нужен только для точной сверки.\n")
    A("Цены ниже — для **первого** экземпляра. Цена N-го здания того же типа = "
      "базовая цена с учётом накопительного роста. Готовые таблицы для первых "
      "шести экземпляров находятся в разделе "
      "[«Цена следующих зданий»](../../reports/economy/scaling_prices.md).\n")
    out.extend(render_template("reference/03_buildings/legend.md"))
    A("")
    out.extend(render_template("reference/03_buildings/lifecycle.md"))
    A("")
    out.extend(render_template("reference/03_buildings/era_progression.md"))
    A("")
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
            label = f"{PER_NAT_NAMES.get(suf, suf)} (`{suf}`)"
            anchor = heading_anchor(label)
            A(f"  - [{label}](#{anchor})")
    A("**[Общие постройки (по архитектурным группам)](#общие-постройки-по-архитектурным-группам)**")
    for suf in ["mil", "sto", "mar", "por", "tow", "gol", "iro", "coa", "swa", "sga", "wga", "wwa"]:
        if by_suffix_c.get(suf):
            label = f"{COMMON_NAMES.get(suf, suf)} (`{suf}`)"
            anchor = heading_anchor(label)
            A(f"  - [{label}](#{anchor})")
    mines_label = "Улучшения шахт"
    A(f"**[{mines_label}](#{heading_anchor(mines_label)})**")
    A("")
    A("## Постройки по нациям\n")
    A("Сводка: для каждого типа зданий — параметры по всем нациям (где они есть). "
      "**Жирным** — отклонения от базового значения (мода по столбцу).\n")
    for suf in ["cen", "hou", "bar", "ba2", "bla", "sta", "tem", "aca", "art", "dip"]:
        rows = sorted(by_suffix_pn.get(suf, []), key=lambda x: x["nation"])
        if not rows:
            continue
        A(f"### {PER_NAT_NAMES.get(suf, suf)} (`{suf}`)\n")
        baseline_cols = ["hp", "buildtime_sec", "costpercent",
                          "food", "wood", "stone", "gold", "iron", "coal", "farm"]
        baselines = compute_baselines(rows, baseline_cols)
        A("| Здание | Нация | Здоровье | Время строительства, игр. с | Рост цены, % | Еда | Дерево | Камень | Золото | Железо | Уголь | Места населения | Производит |")
        A("|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|")
        for b in rows:
            produces = b.get("produces") or []
            prod_str = ", ".join(
                canonical_sid_text(sid, sid_labels, show_sid=False)
                for sid in produces[:5]
            ) + (f" (+{len(produces)-5})" if len(produces) > 5 else "")
            A(f"| {name_cell_short(b)} | {nation_ru(b['nation'])} "
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
    A("## Общие постройки (по архитектурным группам)\n")
    for suf in ["mil", "sto", "mar", "por", "tow", "gol", "iro", "coa", "swa", "sga", "wga", "wwa"]:
        rows = by_suffix_c.get(suf, [])
        if not rows:
            continue
        by_sid = defaultdict(list)
        for b in rows:
            by_sid[b["sid"]].append(b)
        A(f"### {COMMON_NAMES.get(suf, suf)} (`{suf}`)\n")
        A("| Здание | Нации | Здоровье | Время строительства, игр. с | Рост цены, % | Еда | Дерево | Камень | Золото | Железо | Уголь | Особенности |")
        A("|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|")
        for sid in sorted(by_sid.keys()):
            entries = by_sid[sid]
            nats = nations_ru([b["nation"] for b in entries])
            b = entries[0]
            extra = []
            if b["weapon_damage"]:
                extra.append(f"урон {b['weapon_damage']}")
                if b["weapon_radiusmax"]:
                    extra.append(f"дальн. {round(b['weapon_radiusmax']/53.3333, 1)}t")
            if b["consume"]:
                extra.append(f"содержание: {resource_values_ru(b['consume'])}")
            if b["produce"]:
                extra.append(f"добывает: {resource_values_ru(b['produce'])}")
            if b["peasantabsorber"]:
                extra.append(f"крестьян {b['peasantabsorber']}")
            extra_str = "; ".join(extra) if extra else "—"
            A(f"| {name_cell_short(b)} | {nats} | {fmt(b['hp'])} | {fmt(b['buildtime_sec'])} "
              f"| {fmt(b['costpercent'])} | {fmt(b['food'])} | {fmt(b['wood'])} "
              f"| {fmt(b['stone'])} | {fmt(b['gold'])} | {fmt(b['iron'])} "
              f"| {fmt(b['coal'])} | {extra_str} |")
        A("")
        if suf == "tow":
            out.extend(render_template("reference/03_buildings/tow_combat.md"))
    A("## Улучшения шахт\n")
    A("Каждая шахта вмещает пять рабочих. Шесть улучшений накопительно доводят предел до "
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
    write_md(TREE_ROOT / "03_buildings" / "README.md", out)


# ---------- 04_units.md ----------

def write_units(data: dict) -> None:
    out = []
    A = out.append
    A("# Юниты\n")
    A("[← Краткий справочник](../README.md)\n")
    A("Все юниты сгруппированы по роли. Чтобы сопоставить похожие войска "
      "строка к строке, откройте [раздел сравнений](../compare/README.md).\n")
    out.extend(render_template("reference/04_units/legend.md"))
    A("")
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
        n = len(by_sid)
        word = plural_ru(n, "вариант", "варианта", "вариантов")
        anchor = heading_anchor(f"{cls_label} {n} {word}")
        A(f"- [{cls_label}](#{anchor}) ({n} {word})")
    A("")

    for cls in classes_with_content:
        units = by_class[cls]
        by_sid = defaultdict(list)
        for u in units:
            by_sid[u["sid"]].append(u)
        n = len(by_sid)
        word = plural_ru(n, "вариант", "варианта", "вариантов")
        A(f"## {cls_ru(cls)} ({n} {word})\n")
        A("| Юнит | Нации | Здоровье | Время найма (игр. с) | Е | З | Ж | Урон | Дальность (клетки) | Перезарядка | Пика | Меч | Пуля | Картечь | Стрела | Ядро |")
        A("|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|")
        for sid in sorted(by_sid.keys()):
            entries = by_sid[sid]
            u = entries[0]
            w0 = primary_weapon(u)
            nat_count = len(entries)
            nat_str = nations_ru([e["nation"] for e in entries])
            A(f"| {name_cell_short(u)} | {nat_str} "
              f"| {fmt(u['hp'])} | {fmt(u['buildtime_sec'])} "
              f"| {fmt(u['food'])} | {fmt(u['gold'])} | {fmt(u['iron'])} "
              f"| {fmt(w0.get('damage'))} | {fmt(w0.get('radiusmax_tiles'))} | {fmt(w0.get('pause_sec'))} "
              f"| {fmt(u['prot_pike'])} | {fmt(u['prot_sword'])} | {fmt(u['prot_bullet'])} "
              f"| {fmt(u['prot_cannister'])} | {fmt(u['prot_arrow'])} | {fmt(u['prot_cannonball'])} |")
        A("")
    write_md(TREE_ROOT / "04_units" / "README.md", out)


# ---------- 05_upgrades.md ----------

def write_upgrades(data: dict) -> None:
    out = []
    A = out.append
    A("# Улучшения\n")
    A("[← Краткий справочник](../README.md)\n")
    A("Улучшения сгруппированы по зданию, в котором их исследуют: Академия, "
      "Кузница, Мельница, Конюшня, Казарма, шахта, Башня, стена и Порт. "
      "Каноническое название показано первым, внутренний код — после него.\n")
    out.extend(render_template("reference/05_upgrades/legend.md"))
    A("")
    # TOC will be inserted here after we know which places have content; we build it below

    PLACE_NAMES = {
        # per-nation places (`<nat><place>.<...>`)
        "aca": "Академия (исследования)",
        "bla": "Кузница (по юнитам — урон и защита)",
        "bar": "Казарма 17 в. (по юнитам)",
        "ba2": "Казарма 18 в. (по юнитам)",
        "sta": "Конюшня (по юнитам — кавалерия)",
        "mil": "Мельница (эффективность еды)",
        "art": "Артиллерийское депо (апгрейды пушек)",
        "tem": "Собор (апгрейды священников)",
        "cen": "Городской центр (переход эпохи)",
        "dip": "Дипломатический центр",
        # common-building places (`<cluster><place>.<...>`)
        "tow": "Башня (скорость перезарядки)",
        "swa": "Каменная стена (постройка ворот)",
        "wwa": "Палисад (постройка ворот)",
        "por": "Порт (лечение)",
        # bare-name common buildings (no cluster prefix)
        "ferry": "Транспорт (вместимость)",
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
    A("- [Как складываются улучшения]"
      f"(#{heading_anchor('Как складываются улучшения')})")
    for place in PLACE_ORDER:
        if not by_place.get(place):
            continue
        if place == "mines":
            label = "Улучшения шахт"
        else:
            label = f"{PLACE_NAMES.get(place, place)} (`{place}`)"
        anchor = heading_anchor(label)
        A(f"- [{label}](#{anchor})")
    A("")

    out.extend(render_template("reference/05_upgrades/order_math.md"))
    A("")

    A("## Улучшения шахт\n")
    A("Одинаковы для всех наций: по шесть уровней для золотых, железных и угольных шахт.\n")
    mine_ups = [u for u in by_place.get("mines", []) if u["nation"] == "aus"]
    mine_ups.sort(key=lambda x: x["sid"])
    A("| Улучшение | Уровень | Доп. рабочих | Еда | Золото |")
    A("|---|---:|---:|---:|---:|")
    for u in mine_ups:
        A(f"| {upgrade_name_cell(u)} | {fmt(u['level'])} | +{u['value']} | {u['food']} | {u['gold']} |")
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
        A(f"## {PLACE_NAMES.get(place, place)} (`{place}`)\n")
        A("| Улучшение | Нации | Эффект | Значение | Изменение цены | Еда | Дерево | Камень | Золото | Железо | Уголь | Время, игр. с |")
        A("|---|---|---|---:|---|---:|---:|---:|---:|---:|---:|---:|")
        for stripped in sorted(by_stripped.keys()):
            entries = by_stripped[stripped]
            sig: dict[tuple, list[dict]] = defaultdict(list)
            for e in entries:
                # Include resource_pcts in the dedup key so per-nation differences in
                # priceperc % don't collapse incorrectly into one row.
                pcts = e.get("resource_pcts") or {}
                pcts_key = tuple(sorted(pcts.items()))
                key = (e.get("value"), e["food"], e["wood"], e["stone"],
                        e["gold"], e["iron"], e["coal"], pcts_key)
                sig[key].append(e)
            for key, group in sorted(sig.items(), key=lambda kv: -len(kv[1])):
                first = group[0]
                nat_count = len(group)
                nat_str = nations_ru([g["nation"] for g in group])
                pcts = first.get("resource_pcts") or {}
                if pcts:
                    pcts_str = " / ".join(
                        f"{RESOURCE_NAMES_RU.get(k, k)} {v:+d}%"
                        for k, v in sorted(pcts.items())
                    )
                else:
                    pcts_str = "—"
                effect_ru, _ = decode_upg_type(first.get("itype"), lang="ru")
                A(f"| {upgrade_name_cell(first)} | {nat_str} "
                  f"| {effect_ru or '—'} | {upgrade_value_ru(first)} "
                  f"| {pcts_str} "
                  f"| {fmt(first['food'])} | {fmt(first['wood'])} | {fmt(first['stone'])} "
                  f"| {fmt(first['gold'])} | {fmt(first['iron'])} | {fmt(first['coal'])} "
                  f"| {fmt(first['time_sec'])} |")
        A("")
    write_md(TREE_ROOT / "05_upgrades" / "README.md", out)


# ---------- 06_market.md ----------

def write_market(data: dict) -> None:
    out = []
    A = out.append
    out.extend(render_template("reference/06_market/intro.md"))
    A("")
    A("| Ресурс | Покупка: минимум | Покупка: начальный | Покупка: максимум | "
      "Продажа: минимум | Продажа: начальный | Продажа: максимум |")
    A("|---|---:|---:|---:|---:|---:|---:|")
    rates = data.get("market_rates", {})
    for res, vals in rates.items():
        if res.startswith("_"):
            continue
        A(f"| {RESOURCE_NAMES_RU.get(res, res).capitalize()} | "
          f"{vals['buycostmin']:.0f} | {vals['buycostdef']:.2f} | {vals['buycostmax']:.0f} "
          f"| {vals['sellcostmin']:.2f} | {vals['sellcostdef']:.2f} | {vals['sellcostmax']:.2f} |")
    A("")
    out.extend(render_template("reference/06_market/mechanics.md"))
    A("")
    A("### Примеры обменов на начальном курсе\n")
    A("Сколько можно получить за 100 единиц на ещё не использованном рынке. "
      "После крупных сделок значения изменятся.\n")
    A("| Продаёте | Получаете | Расчёт |")
    A("|---|---:|---|")
    examples = [
        ("food", "wood", 100), ("food", "gold", 100),
        ("gold", "wood", 100), ("gold", "food", 100),
        ("iron", "food", 100), ("wood", "stone", 100),
    ]
    for sell, buy, amount in examples:
        sd = rates.get(sell, {}).get("sellcostdef", 0)
        bd = rates.get(buy, {}).get("buycostdef", 0)
        if bd:
            received = int(amount * sd / bd)
            sell_name = RESOURCE_NAMES_RU.get(sell, sell)
            buy_name = RESOURCE_NAMES_RU.get(buy, buy)
            A(f"| {amount} {sell_name} | **{received} {buy_name}** | "
              f"{amount} × {sd:.2f} / {bd:.2f} |")
    A("")
    A("### Численный пример сдвига курса\n")
    A("Что произойдёт после **одного** обмена 5000 еды на дерево при начальном курсе:\n")
    food = rates.get("food", {})
    wood = rates.get("wood", {})
    if food and wood:
        amount = 5000
        bought_wood = int(amount * food.get("sellcostdef", 0) / wood.get("buycostdef", 1))
        weight_buy = bought_wood * 0.00002
        weight_sell = amount * 0.00002
        new_wood_buy = (wood["buycostdef"] + wood["buycostmax"] * weight_buy) / (1 + weight_buy)
        new_wood_sell = (wood["sellcostdef"] + wood["sellcostmax"] * weight_buy) / (1 + weight_buy)
        new_food_sell = (food["sellcostdef"] + food["sellcostmin"] * weight_sell) / (1 + weight_sell)
        new_food_buy = (food["buycostdef"] + food["buycostmin"] * weight_sell) / (1 + weight_sell)
        A(f"- Получено дерева: **{bought_wood}**.")
        A(f"- Курс покупки дерева: 50.00 → **{new_wood_buy:.3f}** "
          f"({(new_wood_buy - 50) / 50 * 100:+.2f}%).")
        A(f"- Курс продажи дерева: 30.00 → **{new_wood_sell:.3f}**.")
        A(f"- Курс продажи еды: 15.20 → **{new_food_sell:.3f}** "
          f"({(new_food_sell - 15.20) / 15.20 * 100:+.2f}%). "
          "Следующий игрок получит за еду меньше дерева.")
        A(f"- Курс покупки еды: 25.00 → **{new_food_buy:.3f}**. "
          "Покупать еду при этом становится немного дешевле.")
        A("")
    A("За игровую секунду исчезает примерно 2,5% отклонения. Половина сдвига "
      "уходит примерно за 28 игровых секунд, или 20 реальных секунд на скорости "
      "«Быстро». Частые крупные сделки не дают курсу восстановиться.\n")
    out.extend(render_template("reference/06_market/strategy.md"))
    write_md(TREE_ROOT / "06_market" / "README.md", out)


# ---------- 07_naval.md ----------

# Каталог морских юнитов: sid + русский класс. Порядок управляет таблицами
# в шаблоне `reference/07_naval/main.md`. Цифры (HP / speed / cost / weapons)
# подтягиваются из `data.json`.
NAVAL_SHIPS: list[tuple[str, str]] = [
    ("fishboat",  "Рыбацкая лодка"),
    ("ferry",     "Транспорт"),
    ("yacht",     "Лёгкий стрелок"),
    ("chaika",    "Украинский лёгкий корабль"),
    ("yachttur",  "Турецкий лёгкий корабль"),
    ("galley",    "Артиллерийский"),
    ("frigate",   "Тяжёлый стрелок"),
    ("xebec",     "Алжирский и турецкий тяжёлый корабль"),
    ("battleship", "Линейный корабль"),
]


def _naval_cost_str(u: dict) -> str:
    """Сжатая запись цены: `450 G / 900 W / 150 I / 200 C` — пропускаем нулевые."""
    parts: list[str] = []
    for res, label in (("food", "еды"), ("wood", "дерева"), ("stone", "камня"),
                       ("gold", "золота"), ("iron", "железа"), ("coal", "угля")):
        v = u.get(res)
        if v:
            parts.append(f"{v} {label}")
    return " / ".join(parts) if parts else "—"


def _naval_shot_cost_str(cost: dict | None) -> str:
    """Стоимость одного выстрела: `4 I + 9 C` (или `—` если ничего не тратится)."""
    if not cost:
        return "—"
    parts: list[str] = []
    for res, label in (("iron", "железа"), ("coal", "угля"), ("wood", "дерева"),
                       ("stone", "камня"), ("gold", "золота"), ("food", "еды")):
        v = cost.get(res)
        if v:
            parts.append(f"{v} {label}")
    return " + ".join(parts) if parts else "—"


def _vision_tiles(vision_field: int | None) -> int:
    """Радиус FOW в клетках — `floor(20 + 4 × vision)` из `_unit_GetVision`."""
    return 20 + 4 * (vision_field or 0)


def _naval_catalog_table(by_sid: dict[str, dict]) -> str:
    L = [
        "| Корабль | Роль | Здоровье | Скорость | Обзор (клетки) | Поиск цели (клетки) | Цена | Время постройки (игр. с) |",
        "| --- | --- | ---: | ---: | ---: | ---: | --- | ---: |",
    ]
    for sid, cls in NAVAL_SHIPS:
        u = by_sid.get(sid)
        if u is None:
            continue
        sr = u.get("searchradius_tiles") or 0
        sr_str = f"{sr}" if sr else "—"
        L.append(
            f"| {name_cell_short(u)} | {cls} | {fmt(u.get('hp'))} | {fmt(u.get('speed'))} "
            f"| {_vision_tiles(u.get('vision'))} | {sr_str} | {_naval_cost_str(u)} "
            f"| {fmt(u.get('buildtime_sec'))} |"
        )
    return "\n".join(L)


def _naval_combat_table(by_sid: dict[str, dict]) -> str:
    L = [
        "| Корабль | Оружие | Урон | Перезарядка (игр. с) | Дальность (клетки) | Тип урона | Цена выстрела |",
        "| --- | :---: | ---: | ---: | ---: | --- | --- |",
    ]
    for sid, _cls in NAVAL_SHIPS:
        u = by_sid.get(sid)
        if u is None:
            continue
        weapons = u.get("weapons") or []
        if not weapons:
            continue
        for i, w in enumerate(weapons):
            ship_cell = name_cell_short(u) if i == 0 else " "
            idx = w.get("index", i)
            L.append(
                f"| {ship_cell} | {idx} | {fmt(w.get('damage'))} "
                f"| {fmt(w.get('pause_sec'))} | {fmt(w.get('radiusmax_tiles'))} "
                f"| {WEAPON_KIND_RU.get(w.get('kind'), w.get('kind') or '—')} "
                f"| {_naval_shot_cost_str(w.get('cost'))} |"
            )
    return "\n".join(L)


def _naval_ferry_block(ferry: dict) -> str:
    bt = ferry.get("buildtime_sec") or 0
    real_sec = round(bt / 1.4, 1) if bt else "—"
    return "\n".join([
        "| Параметр | Значение |",
        "| --- | ---: |",
        f"| Здоровье | {fmt(ferry.get('hp'))} |",
        f"| Скорость | {fmt(ferry.get('speed'))} |",
        f"| Вместимость | {fmt(ferry.get('transport'))} |",
        f"| Время постройки | {fmt(bt)} игровой секунды "
        f"({real_sec} реальной на скорости «Быстро») |",
        f"| Цена | {_naval_cost_str(ferry)} |",
        "| Оружие | нет |",
        f"| Радиус обзора | {_vision_tiles(ferry.get('vision'))} клетки |",
    ])


def _naval_fishboat_block(fb: dict) -> str:
    return "\n".join([
        "| Параметр | Значение |",
        "| --- | ---: |",
        f"| Здоровье | {fmt(fb.get('hp'))} |",
        f"| Скорость | {fmt(fb.get('speed'))} |",
        f"| Еды за рейс | {fmt(fb.get('fishingmax'))} |",
        f"| Интервал добычи одной еды | {fmt(fb.get('fishingspeed'))} кадров |",
        f"| Время постройки | {fmt(fb.get('buildtime_sec'))} игровой секунды |",
        f"| Цена | {_naval_cost_str(fb)} |",
    ])


def write_naval(data: dict) -> None:
    by_sid: dict[str, dict] = {}
    for u in data["units"]:
        # Брать первое попавшееся представление каждого sid'а: морские юниты
        # одинаковы у всех наций, у которых они есть, поэтому первый ОК.
        by_sid.setdefault(u["sid"], u)

    catalog_table = _naval_catalog_table(by_sid)
    combat_table = _naval_combat_table(by_sid)
    ferry_block = _naval_ferry_block(by_sid.get("ferry") or {})
    fishboat_block = _naval_fishboat_block(by_sid.get("fishboat") or {})

    out = render_template(
        "reference/07_naval/main.md",
        catalog_table=catalog_table,
        combat_table=combat_table,
        ferry_block=ferry_block,
        fishboat_block=fishboat_block,
    )
    write_md(TREE_ROOT / "07_naval" / "README.md", out)


# ---------- nations/ ----------

def write_nations(data: dict) -> None:
    nations_dir = TREE_ROOT / "nations"
    nations_dir.mkdir(parents=True, exist_ok=True)

    sid_labels = canonical_sid_labels(data)
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
    out = render_template("reference/nations/readme_intro.md")
    A = out.append
    A("")
    A("| Нация | Код | Доступ к XVIII веку | Уникальные юниты |")
    A("|---|---|:---:|---|")

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
        unique_str = ", ".join(
            canonical_sid_text(sid, sid_labels, show_sid=False)
            for sid in unique_filter[:5]
        ) + (f" (+{len(unique_filter)-5})" if len(unique_filter) > 5 else "")
        has_18c = any(
            building["nation"] == nat and building["sid"].endswith("ba2")
            for building in data["buildings"]
        )
        A(f"| [**{ru}**]({nat}.md) | `{nat}` | {'✓' if has_18c else '—'} "
          f"| {unique_str or '—'} |")
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
        A(f"# {ru}")
        A(f"_{en} · внутренний код `{nat}`_\n")
        A("[← Все нации](README.md) · [← Краткий справочник](../README.md)\n")
        A("## Общие особенности\n")
        cluster = _commonname(nat)
        peasant_sid = cluster_peasant.get(nat, "?")
        A(f"- **Базовый крестьянин:** "
          f"{canonical_sid_text(peasant_sid, sid_labels)}.")
        A("- Мельница, склад, рынок и башня используют один из общих "
          f"архитектурных наборов игры (техническая группа `{cluster}`).")
        A("")
        # Uniques
        unique_units = sorted(sid for sid, nations in sid_to_nations.items()
                              if nations == {nat})
        A(f"## Уникальные юниты ({len(unique_units)})\n")
        if unique_units:
            A("| Юнит | Роль | Здоровье | Урон | Перезарядка | Дальность, клеток |")
            A("|---|---|---:|---:|---:|---:|")
            for sid in unique_units:
                rows = [u for u in units_by_nation[nat] if u["sid"] == sid]
                if rows:
                    u = rows[0]
                    w0 = primary_weapon(u)
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
        A("| Здание | Здоровье | Время строительства, игр. с | Рост цены, % | Еда | Дерево | Камень | Золото | Железо | Уголь | Места населения | Производит |")
        A("|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|")
        for b in per_nat_b:
            suf = b["sid"][len(nat):]
            base = suffix_baselines.get(suf, {})
            produces = b.get("produces") or []
            prod_str = ", ".join(
                canonical_sid_text(sid, sid_labels, show_sid=False)
                for sid in produces[:5]
            ) + (f" (+{len(produces)-5})" if len(produces) > 5 else "")
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
        A(f"### Общие здания архитектурной группы ({len(common_b)})\n")
        A("| Здание | Здоровье | Время строительства, игр. с | Рост цены, % | Еда | Дерево | Камень | Золото | Железо | Уголь | Особенности |")
        A("|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|")
        for b in common_b:
            extra = []
            if b["weapon_damage"]: extra.append(f"урон {b['weapon_damage']}")
            if b["consume"]: extra.append(f"содержание: {resource_values_ru(b['consume'])}")
            if b["produce"]: extra.append(f"добывает: {resource_values_ru(b['produce'])}")
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
            A("| Юнит | Здоровье | Время найма, игр. с | Еда | Золото | Железо | Урон | Дальность, клеток | Перезарядка | Распространённость |")
            A("|---|---:|---:|---:|---:|---:|---:|---:|---:|---|")
            for u in sorted(units, key=lambda x: x["sid"]):
                w0 = primary_weapon(u)
                A(f"| {name_cell_full(u)} | {fmt(u['hp'])} | {fmt(u['buildtime_sec'])} "
                  f"| {fmt(u['food'])} | {fmt(u['gold'])} | {fmt(u['iron'])} "
                  f"| {fmt(w0.get('damage'))} | {fmt(w0.get('radiusmax_tiles'))} | {fmt(w0.get('pause_sec'))} "
                  f"| {uniqueness_ru(u.get('uniqueness'))} |")
            A("")
        # Officers
        offs = officers_by_nation.get(nat, [])
        A(f"## Офицеры ({len(offs)} групп)\n")
        if offs:
            A("Каждый офицер формирует отряд из определённых типов войск. "
              "Доступны линия и каре на 15, 36, 72, 120, 196 или 400 бойцов.\n")
            A("| Офицер | Барабанщик | Войска в отряде |")
            A("|---|---|---|")
            for o in offs:
                units = o.get("units", [])
                unit_str = ", ".join(
                    canonical_sid_text(sid, sid_labels, show_sid=False)
                    for sid in units[:8]
                ) + (f" (+{len(units)-8})" if len(units) > 8 else "")
                A(
                    f"| {canonical_sid_text(o['officersid'], sid_labels)} "
                    f"| {canonical_sid_text(o['drummersid'], sid_labels)} "
                    f"| {unit_str or '—'} |"
                )
        A("")
        # Upgrades summary
        ups = upgrades_by_nation.get(nat, [])
        A(f"## Улучшения ({len(ups)})\n")
        A("Полный список — в [главе «Улучшения»](../05_upgrades/README.md).\n")
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
                    place_name = (
                        "Шахты" if p == "mines"
                        else PER_NAT_NAMES.get(p) or COMMON_NAMES.get(p) or p
                    )
                    A(f"- **{place_name}** (`{p}`): {place_counts[p]}")
        write_md(nations_dir / f"{nat}.md", out)


# ---------- compare/ ----------

def write_compare(data: dict) -> None:
    import shutil
    sid_labels = canonical_sid_labels(data)
    cmp_dir = TREE_ROOT / "compare"
    # Wipe & recreate to drop any stale at-root files from the old flat layout.
    if cmp_dir.exists():
        shutil.rmtree(cmp_dir)
    cmp_dir.mkdir(parents=True, exist_ok=True)
    cmp_units = cmp_dir / "units"
    cmp_units.mkdir(parents=True, exist_ok=True)
    cmp_buildings = cmp_dir / "buildings"
    cmp_buildings.mkdir(parents=True, exist_ok=True)
    cmp_weapons = cmp_dir / "weapons"
    cmp_weapons.mkdir(parents=True, exist_ok=True)

    by_class = defaultdict(list)
    for u in data["units"]:
        cls = classify_unit(u["sid"], u.get("usage_short", ""))
        by_class[cls].append(u)

    # Top-level index dispatches into units/ and buildings/.
    out = render_template("reference/compare/readme.md")
    write_md(cmp_dir / "README.md", out)

    # Per-subfolder README's so back-links from individual files resolve cleanly.
    write_md(cmp_units / "README.md", [
        "# Сравнения юнитов\n",
        "[← Все сравнения](../README.md) · [← Краткий справочник](../../README.md)\n",
        "Выберите нужный класс в [общем списке сравнений](../README.md#юниты).",
    ])
    write_md(cmp_buildings / "README.md", [
        "# Сравнения зданий\n",
        "[← Все сравнения](../README.md) · [← Краткий справочник](../../README.md)\n",
        "Выберите нужный тип в [общем списке сравнений](../README.md#здания).",
    ])
    write_md(cmp_weapons / "README.md", [
        "# Оружие и снаряды\n",
        "[← Все сравнения](../README.md) · [← Краткий справочник](../../README.md)\n",
        "Характеристики стрел, ядер, гранат и других снарядов со списком "
        "использующих их войск. Параметры самих юнитов находятся в "
        "[сравнениях юнитов](../units/README.md).",
    ])

    def write_unit_compare(filename: str, classes: list[str], title: str, intro: str) -> None:
        out = []
        A = out.append
        A(f"# {title}\n")
        A("[← Сравнения юнитов](README.md) · [← Все сравнения](../README.md) · [← Краткий справочник](../../README.md)\n")
        A(intro + "\n")
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
            w0 = primary_weapon(u)
            consume = u.get("consume") or {}
            flat = {
                "sid": u["sid"], "nation": u["nation"],
                "name_en": u.get("name_en") or "",
                "name_ru": u.get("name_ru") or "",
                "hp": u.get("hp"), "buildtime_sec": u.get("buildtime_sec"),
                "food": u.get("food"), "gold": u.get("gold"), "iron": u.get("iron"),
                "wood": u.get("wood"), "stone": u.get("stone"), "coal": u.get("coal"),
                "consume_food": consume.get("food"),
                "consume_gold": consume.get("gold"),
                "speed": u.get("speed"),
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
                          "consume_food", "consume_gold", "speed",
                          "damage", "radiusmax_tiles", "pause_sec",
                          "prot_pike", "prot_sword", "prot_bullet",
                          "prot_cannister", "prot_arrow", "prot_cannonball"]
        baselines = compute_baselines(flat_rows, baseline_cols)

        # Friendly labels for the baseline summary (col_key → human label)
        BASELINE_LABELS = {
            "hp": "здоровье", "buildtime_sec": "время найма (игр. с)",
            "food": "еда", "gold": "золото", "iron": "железо",
            "consume_food": "расход еды (служебное значение)",
            "consume_gold": "расход золота (служебное значение)",
            "speed": "скорость",
            "damage": "урон", "radiusmax_tiles": "дальность (клетки)",
            "pause_sec": "перезарядка (с)",
            "prot_pike": "пика", "prot_sword": "меч", "prot_bullet": "пуля",
            "prot_cannister": "картечь", "prot_arrow": "стрела",
            "prot_cannonball": "ядро",
        }

        A("> **Базовые значения** (мода по столбцу — что считается «обычным» в этом классе): "
          + ", ".join(f"{BASELINE_LABELS.get(k, k)} = {v}"
                       for k, v in baselines.items() if v is not None) + ".")
        A("> **Жирным** в таблице ниже — отклонения от этих базовых значений. "
          "Так сразу видно, какой юнит «особенный» в каждой колонке.\n")
        A("> **Содержание** указано в ресурсе за игровую секунду; служебное "
          "значение из файлов игры приведено в скобках. **Скорость** дана в "
          "единицах движка: чем число больше, тем юнит быстрее.\n")

        A("| Юнит | Нация | Здоровье | Время найма, игр. с | Еда | Золото | Железо | Еда/игр. с | Золото/игр. с | Скорость | Урон | Дальность, клеток | Перезарядка, с | Пика | Меч | Пуля | Картечь | Стрела | Ядро | Распространённость |")
        A("|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|")
        def _upkeep_cell(raw):
            if raw is None or raw == 0:
                return "—"
            per_sec = raw * 32 / 20000
            return f"{per_sec:.4f} ({raw})"
        for r in flat_rows:
            A(f"| {name_cell_short(r)} | {nation_ru(r['nation'])} "
              f"| {bold_if(r['hp'], baselines['hp'])} "
              f"| {bold_if(r['buildtime_sec'], baselines['buildtime_sec'])} "
              f"| {bold_if(r['food'], baselines['food'])} "
              f"| {bold_if(r['gold'], baselines['gold'])} "
              f"| {bold_if(r['iron'], baselines['iron'])} "
              f"| {_upkeep_cell(r['consume_food'])} "
              f"| {_upkeep_cell(r['consume_gold'])} "
              f"| {bold_if(r['speed'], baselines['speed'])} "
              f"| {bold_if(r['damage'], baselines['damage'])} "
              f"| {bold_if(r['radiusmax_tiles'], baselines['radiusmax_tiles'])} "
              f"| {bold_if(r['pause_sec'], baselines['pause_sec'])} "
              f"| {bold_if(r['prot_pike'], baselines['prot_pike'])} "
              f"| {bold_if(r['prot_sword'], baselines['prot_sword'])} "
              f"| {bold_if(r['prot_bullet'], baselines['prot_bullet'])} "
              f"| {bold_if(r['prot_cannister'], baselines['prot_cannister'])} "
              f"| {bold_if(r['prot_arrow'], baselines['prot_arrow'])} "
              f"| {bold_if(r['prot_cannonball'], baselines['prot_cannonball'])} "
              f"| {uniqueness_ru(r['uniqueness'])} |")
        write_md(cmp_units / filename, out)

    write_unit_compare("pikemen.md", ["Pikemen 17c"], "Пикинёры (17 в.)",
                        "Базовая пехота ближнего боя с пиками. Эффективна против кавалерии — высокая защита от картечи.")
    write_unit_compare("pikemen18.md", ["Pikemen 18c"], "Пикинёры (18 в.)",
                        "Поздние пикинёры с улучшенной бронёй.")
    write_unit_compare("light_infantry.md", ["Light Infantry"], "Лёгкая пехота",
                        "Лёгкая пехота с мечом или саблей. Дешевле пикинёров, но слабее против кавалерии.")
    write_unit_compare("musketeers17.md", ["Musketeers 17c"], "Мушкетёры (17 в.)",
                        "Стрелки с пулевым оружием. У России это Стрелец, у Турции — Янычар, у Украины — Сердюк.")
    write_unit_compare("musketeers18.md", ["Musketeers 18c"], "Мушкетёры (18 в.)",
                        "Поздние мушкетёры — выше урон, лучше броня.")
    write_unit_compare("special_infantry_18c.md", ["18c special infantry"], "Особая пехота (18 в.)",
                        "Уникальные национальные стрелки 18 в., строящиеся в той же казарме 18 в., "
                        "что и обычный мушкетёр: Хайлендер у Шотландии, Пандур у Австрии, "
                        "Секей у Венгрии, Шассёр у Франции, Йегер у Португалии и Швейцарии. "
                        "Обычно они быстрее или наносят особый урон, но уступают в здоровье.")
    write_unit_compare("grenadiers.md", ["Grenadiers"], "Гренадёры",
                        "Гранаты плюс мушкет. Эффективны против зданий и башен.")
    write_unit_compare("archers.md", ["Archers"], "Лучники",
                        "Лук и стрелы. Выгоднее всего против тяжёлой пехоты с низкой защитой от стрел.")
    write_unit_compare("light_cavalry.md", ["Light Cavalry"], "Лёгкая кавалерия",
                        "Лёгкая конница с саблей или копьём. Это один из самых быстрых классов в игре.")
    write_unit_compare("dragoons.md", ["Dragoons"], "Драгуны",
                        "Конные стрелки. Основная тактика — «ударь и отойди».")
    write_unit_compare("heavy_cavalry.md", ["Heavy Cavalry"], "Тяжёлая кавалерия",
                        "Рейтары, кирасиры, витязи и крылатые гусары — ударная конница для прорыва строя.")
    write_unit_compare("siege.md", ["Cannons", "Mortars"], "Артиллерия",
                        "Пушка стреляет ядрами и картечью, мортира предназначена прежде всего для разрушения зданий.")
    write_unit_compare("ships.md", ["Fishing Boat", "Warships"], "Корабли",
                        "Морские юниты. Рыбацкая лодка добывает рыбу; военные корабли ведут морской бой.")
    write_unit_compare("peasants.md", ["Peasant"], "Крестьяне",
                        "Восемь национальных вариантов отличаются внешним видом и начальным запасом здоровья.")
    write_unit_compare("officers.md", ["Officer"], "Офицеры",
                        "Офицер командует отрядом и нанимается в казармах. "
                        "Национальные варианты заметно различаются стоимостью, временем найма и уроном.")
    write_unit_compare("drummers.md", ["Drummer / Bagpiper"], "Барабанщики и волынщик",
                        "Музыкант — второй обязательный участник отряда после офицера. Он не атакует. "
                        "Российский и турецкий варианты заметно отличаются здоровьем и стоимостью.")

    # Priests need a heal-specific table (different columns than the generic
    # damage/range/protection layout): heal radius/amount + gold upkeep matter.
    out = []
    A = out.append
    A("# Священники\n")
    A("[← Сравнения юнитов](README.md) · [← Все сравнения](../README.md) · [← Краткий справочник](../../README.md)\n")
    A("Священники — единственный тип юнитов, способный лечить союзников. Католический священник, "
      "православный священник, мулла и падре различаются дальностью, силой лечения и "
      "расходом золота на содержание. Технические идентификаторы приведены только для справки.\n")
    rows = []
    seen = set()
    for u in sorted(data["units"], key=lambda x: (x["sid"], x["nation"])):
        if u["sid"] not in ("priest", "pope", "mullah", "padre"):
            continue
        key = u["sid"]
        if key in seen:
            continue
        seen.add(key)
        rows.append(u)
    A("| Юнит | Код | Здоровье | Время найма, игр. с | Еда | Золото | Лечение за такт | Дальность лечения, клеток | Золото на содержание | Нации |")
    A("|---|---|---:|---:|---:|---:|---:|---:|---:|---|")
    for u in rows:
        w0 = primary_weapon(u)
        nations_with = sorted({r["nation"] for r in data["units"] if r["sid"] == u["sid"]})
        consume_gold = (u.get("consume") or {}).get("gold")
        upkeep_per_sec = (consume_gold * 32 / 20000) if consume_gold else None
        A(f"| **{u.get('name_ru') or u['sid']}** | `{u['sid']}` "
          f"| {u.get('hp')} "
          f"| {u.get('buildtime_sec')} "
          f"| {u.get('food')} "
          f"| {u.get('gold')} "
          f"| {w0.get('damage')} "
          f"| {w0.get('radiusmax_tiles')} "
          f"| {consume_gold} (≈ {upkeep_per_sec:.4f}/г-сек) "
          f"| {', '.join(nation_ru(nat) for nat in nations_with)} |")
    A("")
    A("> **Перезарядка равна нулю:** жрец начинает лечить сразу после выбора цели. "
      "Реальный темп лечения равен силе лечения за такт, умноженной на число тактов в секунду (см. "
      "[описание тактов и подтактов](../../../../internals/engine/ticks_and_subticks.md) — такт лечения "
      "управляется тем же `gc_time_to_frames` циклом).\n")
    A("> **Источник характеристик:** `unit.script:1151-1188`. Игра задаёт "
      "общую основу для священников, а затем отдельно меняет параметры "
      "Священника, Пастора, Муллы и Падре.")
    write_md(cmp_units / "priests.md", out)

    # Weapons catalog (projectile-level data)
    out = []
    A = out.append
    A("# Оружие и снаряды\n")
    A("[← Оружие и снаряды](README.md) · [← Все сравнения](../README.md) · [← Краткий справочник](../../README.md)\n")
    A("Уникальные типы снарядов и метательного оружия, их характеристики и использующие "
      "их юниты. Один снаряд может наносить разный урон у разных юнитов, поэтому таблица "
      "показывает диапазон значений. Служебные идентификаторы сохранены для точной сверки.\n")

    # Aggregate per weaponsid
    weapons: dict[str, list[dict]] = defaultdict(list)
    for u in data["units"]:
        for w in (u.get("weapons") or []):
            wid = w.get("weaponsid")
            if not wid:
                continue
            weapons[wid].append({
                "unit": u["sid"],
                "unit_name": unit_ru(
                    u["sid"],
                    u.get("name_ru") or u.get("name_en") or u["sid"],
                ),
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

    A("| Код снаряда | Тип | Урон | Перезарядка, с | Дальность, клеток | Цена выстрела | Использующие юниты |")
    A("|---|---|---|---:|---:|---|---|")
    for wid in sorted(weapons.keys()):
        uses = weapons[wid]
        # Aggregate
        raw_kind = uses[0]["kind"] or "—"
        kind = WEAPON_KIND_RU.get(raw_kind, raw_kind)
        dmgs = sorted(set(u["dmg"] for u in uses if u["dmg"] is not None))
        pauses = sorted(set(u["pause_sec"] for u in uses if u["pause_sec"] is not None))
        ranges = sorted(set(u["rng_tiles"] for u in uses if u["rng_tiles"] is not None))
        # cost typically uniform per weaponsid
        costs: set[str] = set()
        for u in uses:
            if u["cost"]:
                costs.add(resource_values_ru(u["cost"]))
        cost_str = ", ".join(sorted(costs)) if costs else "—"
        unit_labels = sorted(set(
            f"{u['unit_name']} (`{u['unit']}`)" for u in uses
        ))
        units_str = ", ".join(unit_labels[:6]) + (f" (+{len(unit_labels)-6})" if len(unit_labels) > 6 else "")
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
      "тип «огненная стрела») — второе оружие лучников.")
    A("- **`PPOINTTKOR`** — корабельное ядро (используется фрегатом, шебекой, линейным кораблём, чайкой, "
      "галерой, яхтой).")
    A("- **`PPOINTT`** и **`PPOINTTFRAME`** — ядра обычной пушки и рибадекина.")
    A("- **`PSMPOINTTPUS`** и **`PSMPOINTT`** — картечь обычной пушки и многоствольного орудия.")
    A("- **`DIMMORT1`**, **`DIMMORT2`** и **`DIMMORT2KOR`** — снаряды гаубицы, "
      "мортиры и корабельной мортиры галеры.")
    A("- **`NUCLGRE`** — граната гренадера.")
    A("- **`PPOINTTTOW`** — ядро башни или порта; в таблицу юнитов оно не входит.")
    A("\nИсточник определений: `data/scripts/lib/weapon.script` (функция `_weapon_AddWeapon`). "
      "Дополнительные параметры полёта и визуальных эффектов находятся в скрипте оружия.")
    write_md(cmp_weapons / "projectiles.md", out)

    def write_building_compare(filename: str, sid_suffix: str, title: str, intro: str,
                                kind: str = "per-nation") -> None:
        out = []
        A = out.append
        A(f"# {title}\n")
        A("[← Сравнения зданий](README.md) · [← Все сравнения](../README.md) · [← Краткий справочник](../../README.md)\n")
        A(intro + "\n")
        rows = sorted([b for b in data["buildings"]
                       if b["sid"].endswith(sid_suffix) and b["kind"] == kind],
                      key=lambda x: x["nation"])
        baseline_cols = ["hp", "buildtime_sec", "costpercent", "wood", "stone", "gold", "farm"]
        baselines = compute_baselines(rows, baseline_cols)
        BLD_LABELS = {
            "hp": "здоровье", "buildtime_sec": "время строительства (игр. с)",
            "costpercent": "рост цены", "wood": "дерево", "stone": "камень",
            "gold": "золото", "farm": "места населения",
        }
        A("> **Базовые значения** (мода по столбцу): "
          + ", ".join(f"{BLD_LABELS.get(k, k)} = {v}" for k, v in baselines.items()
                       if v is not None) + ".")
        A("> **Жирным** в таблице ниже — отклонения от этих значений.\n")
        A("| Здание | Нация | Здоровье | Время строительства, игр. с | Рост цены, % | Дерево | Камень | Золото | Места населения | Производит |")
        A("|---|---|---:|---:|---:|---:|---:|---:|---:|---|")
        for b in rows:
            produces = b.get("produces") or []
            prod_str = ", ".join(
                canonical_sid_text(sid, sid_labels, show_sid=False)
                for sid in produces[:6]
            ) + (f" (+{len(produces)-6})" if len(produces) > 6 else "")
            A(f"| {name_cell_short(b)} | {nation_ru(b['nation'])} "
              f"| {bold_if(b['hp'], baselines['hp'])} "
              f"| {bold_if(b['buildtime_sec'], baselines['buildtime_sec'])} "
              f"| {bold_if(b['costpercent'], baselines['costpercent'])} "
              f"| {bold_if(b['wood'], baselines['wood'])} "
              f"| {bold_if(b['stone'], baselines['stone'])} "
              f"| {bold_if(b['gold'], baselines['gold'])} "
              f"| {bold_if(b['farm'], baselines['farm'])} "
              f"| {prod_str or '—'} |")
        write_md(cmp_buildings / filename, out)

    write_building_compare("town_halls.md", "cen", "Ратуши",
                            "Главные здания всех 21 нации. Австрийская строится за 4.69 секунды "
                            "(исключение). Украинская даёт 200 мест населения, Российская — 75.")

    # Barracks needs two sections (17c + 18c) — special-case
    out = []
    A = out.append
    A("# Казармы (17 в. и 18 в.)\n")
    A("[← Сравнения зданий](README.md) · [← Все сравнения](../README.md) · [← Краткий справочник](../../README.md)\n")
    A("Казармы тренируют пехоту. У России — Стрелецкая казарма; у Украины — Казацкий дом.\n")
    A("> **Жирным** — отклонения от базовых значений.\n")
    for sid_suffix, title, note in [
        ("bar", "Казарма 17 в.", ""),
        ("ba2", "Казарма 18 в.", "Есть не у всех наций: её нет у Украины, Турции и Алжира."),
    ]:
        A(f"## {title}\n")
        if note:
            A(note + "\n")
        rows = sorted([b for b in data["buildings"]
                       if b["sid"].endswith(sid_suffix) and b["kind"] == "per-nation"],
                      key=lambda x: x["nation"])
        baseline_cols = ["hp", "buildtime_sec", "costpercent", "wood", "stone", "gold", "farm"]
        baselines = compute_baselines(rows, baseline_cols)
        A("| Здание | Нация | Здоровье | Время строительства, игр. с | Рост цены, % | Дерево | Камень | Золото | Места населения | Производит |")
        A("|---|---|---:|---:|---:|---:|---:|---:|---:|---|")
        for b in rows:
            produces = b.get("produces") or []
            prod_str = ", ".join(
                canonical_sid_text(sid, sid_labels, show_sid=False)
                for sid in produces[:5]
            ) + (f" (+{len(produces)-5})" if len(produces) > 5 else "")
            A(f"| {name_cell_short(b)} | {nation_ru(b['nation'])} "
              f"| {bold_if(b['hp'], baselines['hp'])} "
              f"| {bold_if(b['buildtime_sec'], baselines['buildtime_sec'])} "
              f"| {bold_if(b['costpercent'], baselines['costpercent'])} "
              f"| {bold_if(b['wood'], baselines['wood'])} "
              f"| {bold_if(b['stone'], baselines['stone'])} "
              f"| {bold_if(b['gold'], baselines['gold'])} "
              f"| {bold_if(b['farm'], baselines['farm'])} "
              f"| {prod_str or '—'} |")
        A("")
    write_md(cmp_buildings / "barracks.md", out)

    # New per-nation building compares (gap fill: aca/art/bla/dip/hou/sta/tem).
    # All seven are unique per-nation buildings in the same vein as town_halls/barracks.
    write_building_compare("academies.md", "aca", "Академии",
                            "Академия — здание апгрейдов общего профиля. Один вариант на нацию.")
    write_building_compare("artillery_depots.md", "art", "Артиллерийские депо",
                            "Тренируют пушки/мортиры. Производственный список варьируется (например, "
                            "у Алжира нет многоствольного орудия).")
    write_building_compare("blacksmiths.md", "bla", "Кузницы",
                            "Кузница — апгрейды защиты пехоты и оружия. Стоимость и время заметно "
                            "различаются по нациям.")
    write_building_compare("diplomatic_centers.md", "dip", "Дипломатические центры",
                            "Тренируют наёмников. Производственный список общий (наёмники-юниты), но "
                            "стоимость постройки сильно варьирует.")
    write_building_compare("houses.md", "hou", "Дома",
                            "Дом увеличивает предел населения. Базовое значение одинаково — 25 мест, "
                            "но цена и здоровье различаются.")
    write_building_compare("stables.md", "sta", "Конюшни",
                            "Тренируют кавалерию. У большинства наций — общий набор юнитов, у России и Украины "
                            "уникальные тяжёлые всадники.")
    write_building_compare("temples.md", "tem", "Соборы / Церкви / Мечети",
                            "Тренируют священника, православного священника, муллу или падре. Разная стоимость и "
                            "время постройки. См. также [сравнение священников](../units/priests.md) — "
                            "сравнение самих жрецов.")

    # Common-cluster buildings (mill/market/storehouse/port/towers/mines/walls) live in
    # 4-5 cluster variants (eur/rus/tur/ukr/sco). Useful to compare cluster-vs-cluster.
    write_building_compare("mills.md", "mil", "Мельницы",
                            "Рядом с мельницей можно строить поля. Внешний вид зависит от архитектурной группы.",
                            kind="common")
    write_building_compare("markets.md", "mar", "Рынки",
                            "Здание для обмена ресурсов. Внешний вид зависит от архитектурной группы.",
                            kind="common")
    write_building_compare("storehouses.md", "sto", "Склады",
                            "Место сдачи дерева и камня. Внешний вид зависит от архитектурной группы.",
                            kind="common")
    write_building_compare("ports.md", "por", "Порты",
                            "Корабельная верфь и место сдачи рыбы. Внешний вид зависит от архитектурной группы.",
                            kind="common")
    write_building_compare("towers.md", "tow", "Башни",
                            "Оборонительная башня с пушкой. Внешний вид зависит от архитектурной группы.",
                            kind="common")

    # Mines: 3 resource types (coa/gol/iro) × cluster — group all into one page.
    out = []
    A = out.append
    A("# Шахты\n")
    A("[← Сравнения зданий](README.md) · [← Все сравнения](../README.md) · [← Краткий справочник](../../README.md)\n")
    A("Шахты добывают уголь, золото и железо. Характеристики у всех "
      "архитектурных вариантов одинаковы, поэтому в таблице показана одна общая модель.\n")
    rows = sorted([b for b in data["buildings"]
                   if b["sid"].endswith(("coa","gol","iro")) and b["kind"] == "common"],
                  key=lambda x: (x["sid"], x["nation"]))
    seen = set()
    rows = [b for b in rows if not (b["sid"] in seen or seen.add(b["sid"]))]
    baseline_cols = ["hp", "buildtime_sec", "wood", "stone", "gold"]
    baselines = compute_baselines(rows, baseline_cols)
    A("| Здание | Архитектурная группа | Ресурс | Здоровье | Время строительства, игр. с | Дерево | Камень | Золото | Добыча за такт | Базовых мест |")
    A("|---|---|---|---:|---:|---:|---:|---:|---:|---:|")
    for b in rows:
        produce = b.get("produce") or {}
        res, rate = next(iter(produce.items()), ("—", "—"))
        cluster_name = {
            "eur": "европейская",
            "rus": "русская",
            "tur": "турецкая",
            "ukr": "украинская",
            "spa": "испанская",
            "por": "португальская",
        }.get(b["sid"][:3], b["sid"][:3])
        A(f"| {name_cell_short(b)} | {cluster_name} | "
          f"{RESOURCE_NAMES_RU.get(res, res)} "
          f"| {bold_if(b['hp'], baselines['hp'])} "
          f"| {bold_if(b['buildtime_sec'], baselines['buildtime_sec'])} "
          f"| {bold_if(b['wood'], baselines['wood'])} "
          f"| {bold_if(b['stone'], baselines['stone'])} "
          f"| {bold_if(b['gold'], baselines['gold'])} "
          f"| {rate} "
          f"| {b.get('peasantabsorber') or '—'} |")
    write_md(cmp_buildings / "mines.md", out)


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
    """Write docs/README.md — reader-facing encyclopedia home page."""
    out = []
    A = out.append
    A("# Энциклопедия Cossacks 3\n")
    A("[English](../docs_en/README.md) · **Русский**\n")
    out.extend(render_template("output_readme.md"))

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
    print("  01_economy/README.md", flush=True)
    write_combat(data)
    print("  02_combat/README.md", flush=True)
    write_buildings(data)
    print("  03_buildings/README.md", flush=True)
    write_units(data)
    print("  04_units/README.md", flush=True)
    write_upgrades(data)
    print("  05_upgrades/README.md", flush=True)
    write_market(data)
    print("  06_market/README.md", flush=True)
    write_naval(data)
    print("  07_naval/README.md", flush=True)
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
