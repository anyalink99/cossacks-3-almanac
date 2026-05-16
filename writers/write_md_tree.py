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
                    usage_ru)

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
    out = []
    A = out.append
    e = data["economy"]
    A("# Справочник по Cossacks 3\n")
    banner = _version_banner(data)
    if banner:
        A(banner + "\n")
    A("Структурированный справочник по игре. Все числа извлечены напрямую из "
      "её скриптов (`unit.script`, `country.script`, `dmscript.global`, "
      "файлы локали) и лежат в [`../data.json`](../data.json); этот каталог "
      "— человеко-читаемый рендер.\n")
    A("Что внутри:\n")
    A("- **7 глав по темам** — экономика, бой, здания, юниты, апгрейды, "
      "рынок, флот.")
    A("- **Справки по нациям** — отдельная страница на каждую из 21 "
      "играбельных, с уникальными юнитами, аномалиями и доступом к 18 веку.")
    A("- **Сравнения** — таблицы бок о бок по классам юнитов (все "
      "пикинёры, все мушкетёры 18 в. и т. д.).")
    A("- **Шпаргалка по формулам** ниже на этой странице, плюс глоссарий "
      "ключевых игровых тегов.")
    A("\n---\n")

    # ─── Навигация ─────────────────────────────────────────────────────
    A("## Навигация\n")
    A("**Главы по темам:**\n")
    A("| Глава | О чём |")
    A("|---|---|")
    A("| [01. Экономика](01_economy/README.md) | Добыча ресурсов: формулы, `eff`, шахты, поля, голод и upkeep, рыбалка. |")
    A("| [02. Бой и движение](02_combat/README.md) | Бой: формула урона, хедшот, формации, рассеяние, AoE, скорости, контр-матрица. |")
    A("| [03. Здания](03_buildings/README.md) | Все здания (национальные и общие), цены, footprint. |")
    A("| [04. Юниты](04_units/README.md) | Все юниты по классам — пехота, кавалерия, артиллерия, корабли. |")
    A("| [05. Апгрейды](05_upgrades/README.md) | Все апгрейды, сгруппированы по месту исследования. |")
    A("| [06. Рынок](06_market/README.md) | Рынок: курсы обмена, преимущество первого хода, деградация цен. |")
    A("| [07. Морской флот](07_naval/README.md) | Морской флот: порт, корабли, транспорт, рыболов, DLC-юниты. |")
    A("")
    A("**Указатели по объектам:**\n")
    A("- [`nations/`](nations/README.md) — по одной справке на каждую "
      "из 21 наций (что у неё уникального).")
    A("- [`compare/`](compare/README.md) — сравнения юнитов одного класса "
      "бок о бок (все мушкетёры 17 в., все драгуны и т. д.).")
    A("- [`../reports/map/lobby_settings.md`](../reports/map/lobby_settings.md) "
      "— все опции лобби с каноничными русскими названиями. Поведение "
      "движка по каждой опции — в "
      "[`../recon/world/map/game_settings.md`](../recon/world/map/game_settings.md).")
    A("")
    A("**Где искать остальное:**\n")
    A("| Каталог | Что внутри |")
    A("|---|---|")
    A("| [`../reports/`](../reports/README.md) | Производные расчёты: DPS, EHP, counter matrix, scaling, tech tree, production rates, builder slots, construction times, ресурсы карты. |")
    A("| [`../recon/`](../recon/README.md) | Handwritten reverse-engineering механик: добыча, постройка, RNG, тики, server sync, генерация карт. |")
    A("| [`../../derived/`](../../derived/README.md) | Машинно-читаемые JSON-датасеты (`tech_tree.json`, `canonical_terms.json` и др.). |")
    A("| [`../architecture.md`](../architecture.md) | Поток данных в проекте: что из чего рождается. |")
    A("| [`../data.json`](../data.json) | Мастер-структура (~4.7 МБ). Вход для всех writer'ов и compute-скриптов. |")
    A("\n---\n")

    # ─── Шпаргалка по формулам ─────────────────────────────────────────
    A("## Шпаргалка по формулам\n")
    A("Канонические формулы, на которые опираются все остальные числа. "
      "Если что-то в таблицах ниже расходится с твоими ожиданиями — "
      "сначала проверь эту шпаргалку: расхождение в правом столбце "
      "обычно объясняется одной из формул здесь.\n")

    A("### Добыча ресурсов\n")
    A("| Ресурс | Порция / рейс | Ударов до сдачи | Идеальный rate (1 крестьянин, `eff = 100`, без дороги) |")
    A("|---|---:|---:|---:|")
    A(f"| food | **{e['resource_portion_food']}** | {e['hits_needed_food']} | ≈ 2.97 / g-сек |")
    A(f"| wood | **{e['resource_portion_wood']}** | {e['hits_needed_wood']} | ≈ 3.56 / g-сек |")
    A(f"| stone | **{e['resource_portion_stone']}** | {e['hits_needed_stone']} | ≈ 3.56 / g-сек |")
    A(f"| gold / iron / coal | **{e['resource_portion_others']}** (хардкод) | n/a | через шахту: 1.664 на крестьянина в g-сек (без апгрейдов) |")
    A("")
    A("`delivered = floor(portion × eff / 100)`. `eff` стартует со 100; "
      "апгрейды (`mill.X`, `aca.X`, `bla.X`) добавляются **аддитивно**. "
      "Подробности — [глава «Экономика»](01_economy/README.md).\n")

    A("### Урон в бою\n")
    A("```")
    A("applied = max(1, weapon.damage")
    A("                 − target.shield                # / 3, если здание ещё строится")
    A("                 − target.protection[weapon.kind]")
    A("                 + бонусы отряда (LINE / SQUARE / KARE: +2..+7)")
    A("                 + HEADSHOT: +floor(uniqrnd × 500), 5% шанс для arrow / bullet")
    A("                                                по не-зданиям, кроме fasthorse в движении)")
    A("```")
    A("Минимум 1 HP проходит всегда. Подробности — "
      "[`recon/world/combat/combat_damage_pipeline.md` §3](../recon/world/combat/combat_damage_pipeline.md). "
      "Источник: `miscext2.script:_misc_DoDamage`.\n")

    A("### Цены и время\n")
    A("- **N-й экземпляр здания того же типа:** "
      "`cost(N) = floor(base × (costpercent / 100)^(N-1))`. "
      "Готовые таблицы N = 1..6 — в "
      "[`../reports/economy/scaling_prices.md`](../reports/economy/scaling_prices.md).")
    A("- **Время постройки с N строителями:** "
      "`buildtime_sec × 1.13 / N`. Лимит N — builder slots здания (см. "
      "[`../reports/economy/builder_slots.md`](../reports/economy/builder_slots.md)).")
    A("- **Real-time на скорости fast:** `real_sec = g-sec / 1.4`. "
      "Скорости: slow = 7, normal = 10, fast = 14 тиков на реальную секунду.")
    A("- **`buildtime` зданий хранится с множителем 10:** "
      "`g-sec = frames × 10 / 32`, у юнитов — `frames / 32`. "
      "В `data.json` поле `building.buildtime_sec` уже учитывает ×10.\n")

    A("### Ключевые константы\n")
    A(f"- `gc_time_to_frames = {e['time_to_frames']}` — 32 кадра в одной игровой секунде.")
    A(f"- `gc_pixels_to_tile = {e['pixels_to_tile']:.4f}` — перевод `weapon.range` из пикселей в тайлы (например, 800 px = 15 тайлов).")
    A(f"- Лимиты карты: **{e['max_obj_count']}** объектов всего, **{e['max_player_count']}** игроков.")
    A(f"- Поле: HP = **{e['field_max_hp']}**. Шахта без апгрейдов — 5 крестьян, 1.664 ресурса / g-сек на каждого.")
    A("\n---\n")

    # ─── Глоссарий ─────────────────────────────────────────────────────
    out.extend(render_template("reference/readme/glossary.md"))
    A("\n---\n")

    # ─── Что в данных ──────────────────────────────────────────────────
    sanity = data.get("sanity_checks", [])
    n_pass = sum(1 for c in sanity if c["pass"])
    A("## Что в данных\n")
    A("Источник всех чисел — `data.json`, генерируется "
      "`python parser/build_data.py`. После каждой регенерации прогоняются "
      "автоматические проверки.\n")
    A("| Что | Сколько |")
    A("|---|---:|")
    A(f"| Sanity checks (PASS / всего) | **{n_pass} / {len(sanity)}** |")
    A(f"| Играбельных наций | {len(data['nations'])} |")
    A(f"| Зданий (`sid` × нация) | {len(data['buildings'])} |")
    A(f"| Юнитов | {len(data['units'])} |")
    A(f"| Апгрейдов с полностью разрешёнными `cost / value / itype / prereqs` | {len(data['upgrades'])} |")
    A(f"| Групп офицеров и формаций | {len(data.get('officers', []))} |")
    A("")
    A("Известные парсерные пробелы и расхождения с внешними гайдами — в "
      "[`../known_issues.md`](../known_issues.md).")

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
        "| Дип-центр | Нации | HP | Wood | Stone | Gold |",
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
        nat_str = ", ".join(nats) if len(nats) <= 6 else (
            ", ".join(nats[:5]) + f" … (+{len(nats) - 5})"
        )
        L.append(
            f"| {name_cell_short(rep)} ({label}) | {nat_str} | "
            f"{fmt(rep.get('hp'))} | {fmt(rep.get('wood'))} | "
            f"{fmt(rep.get('stone'))} | {fmt(rep.get('gold'))} |"
        )
    return "\n".join(L)


def _mercenary_weapons_summary(unit: dict) -> str:
    """Кратко: `arrow 25 / firearrow 100`. Промежуточные паузы и cost не
    нужны в этой обзорной таблице — они в `02_combat/README.md → Стоимость
    одного выстрела` и в `compute_combat_stats.py`."""
    parts: list[str] = []
    for w in (unit.get("weapons") or []):
        kind = w.get("kind") or "?"
        damage = w.get("damage")
        if damage is None:
            continue
        rmax = w.get("radiusmax_tiles")
        if rmax is not None and rmax > 1.5:
            parts.append(f"{kind} {damage} (range {rmax} t)")
        else:
            parts.append(f"{kind} {damage}")
    return " / ".join(parts) if parts else "—"


def _mercenaries_table(units: list[dict]) -> str:
    """Таблица 8 наёмников: HP, buildtime в g-сек, gold-цена и upkeep,
    `costpercent`, краткое описание оружия. Все цифры — из data.json."""
    by_sid: dict[str, dict] = {}
    for u in units:
        # Любой представитель — наёмники одинаковы у всех наций.
        by_sid.setdefault(u["sid"], u)
    L = [
        "| Наёмник | HP | bt, g-сек | gold (цена) | gold/тик upkeep | costpercent | Оружие |",
        "| --- | ---: | ---: | ---: | ---: | ---: | --- |",
    ]
    for sid in MERCENARY_SIDS:
        u = by_sid.get(sid)
        if u is None:
            continue
        gold_cost = u.get("gold")
        consume_gold = (u.get("consume") or {}).get("gold") or "—"
        cp = u.get("costpercent")
        cp_str = f"{cp}" if cp is not None else "100"
        L.append(
            f"| {name_cell_short(u)} | {fmt(u.get('hp'))} "
            f"| {fmt(u.get('buildtime_sec'))} | **{fmt(gold_cost)}** "
            f"| {consume_gold} | {cp_str} | {_mercenary_weapons_summary(u)} |"
        )
    return "\n".join(L)


def write_economy(data: dict) -> None:
    out = []
    A = out.append
    e = data["economy"]
    A("# 01. Экономика\n")
    A("[← Index](README.md)\n")
    out.extend(render_template("reference/01_economy/recon_refs.md"))
    A("")
    out.extend(render_template("reference/01_economy/summary.md"))
    A("")
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
    A("Все опции лобби (стартовые ресурсы, время мира, лимит населения, переход в 18 век, сложность ИИ и т. д.) — таблицы в [`docs/reports/map/lobby_settings.md`](../reports/map/lobby_settings.md), поведение движка — в [`docs/recon/world/map/game_settings.md`](../recon/world/map/game_settings.md).\n")
    A("## Базовые порции и hits\n")
    A("| Ресурс | Базовая порция | Hits | Источник |")
    A("|---|---:|---:|---|")
    A(f"| food | **{e['resource_portion_food']}** | {e['hits_needed_food']} | dmscript.global:799,804 |")
    A(f"| wood | **{e['resource_portion_wood']}** | {e['hits_needed_wood']} | dmscript.global:800,805 |")
    A(f"| stone | **{e['resource_portion_stone']}** | {e['hits_needed_stone']} | dmscript.global:801,806 |")
    A(f"| gold/iron/coal/прочее | **{e['resource_portion_others']}** | n/a | unit.script:9551 (хардкод) |")
    A("")
    out.extend(render_template("reference/01_economy/extraction_formula.md"))
    A("")
    out.extend(render_template("reference/01_economy/mines_intro.md"))
    A("")
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
      f"{cumulative * 1.664:.1f} ресурса в g-сек = {cumulative * 99.84:.0f} в g-мин**.\n")
    total_food_cost = sum(u['food'] for u in mine_ups)
    total_gold_cost = sum(u['gold'] for u in mine_ups)
    A(f"**Стоимость полной прокачки одной шахты:** F{total_food_cost:,} + G{total_gold_cost:,}.\n")
    out.extend(render_template("reference/01_economy/fields_intro.md"))
    A("")
    A(f"HP поля = `gc_FieldMaxHP = {e['field_max_hp']}`. Урон полю за удар: `resdec = max(1, floor(100 / (1 + fieldlife / 100)))`.\n")
    A("| fieldlife | resdec/удар | Макс. ударов | Макс. food при eff=100 |")
    A("|---:|---:|---:|---:|")
    for fl in (0, 100, 200, 300, 500):
        resdec = max(1, 100 // (1 + fl // 100))
        max_hits = e['field_max_hp'] // resdec
        max_food = max_hits * e['resource_portion_food'] // e['hits_needed_food']
        A(f"| {fl} | {resdec} | {max_hits} | {max_food} |")
    A("\nАпгрейды fieldlife: `aca.4` (+200), `bla.1` (+100). Сумма = 300 → ~2045 food / поле.\n")
    out.extend(render_template("reference/01_economy/fishing.md"))
    A("")
    out.extend(render_template(
        "reference/01_economy/famine_rebellion.md",
        dip_buildings_table=_dip_buildings_table(data["buildings"]),
        mercenaries_table=_mercenaries_table(data["units"]),
    ))
    A("")
    A("## Sanity\n")
    A(f"Sanity checks: **{sum(1 for c in data.get('sanity_checks', []) if c['pass'])}/"
      f"{len(data.get('sanity_checks', []))}** PASS. См. xlsx → лист `Sanity_checks`.\n")
    write_md(TREE_ROOT / "01_economy" / "README.md", out)


# ---------- 02_combat.md ----------

def write_combat(data: dict) -> None:
    out = []
    A = out.append
    e = data["economy"]
    A("# 02. Бой и движение\n")
    A("[← Index](README.md)\n")
    out.extend(render_template("reference/02_combat/main.md"))
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
    A(f"### Матрица контр-эффективности — TTK в g-сек\n")
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
      "показано одной строкой с `nation = all`. Если у нации своё значение — она в отдельной строке.\n")
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
            if len(nations) >= 18:
                nat_str = "all"
            elif len(nations) == 1:
                nat_str = nations[0]
            else:
                nat_str = ", ".join(sorted(set(nations)))
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
    A("# 03. Здания\n")
    A("[← Index](README.md)\n")
    A("Здания делятся на **per-nation** (`<nat>+suffix`, например `auscen` = ратуша Австрии) "
      "и **common** (`<cluster>+suffix`, общие для группы наций: `eur`/`rus`/`tur`/`spa`/`ukr`/`por`).\n")
    A("Цены ниже — для **первого** экземпляра. Цена N-го здания того же типа = "
      "`floor(base × (costpercent/100)^(N-1))`. Готовые таблицы N=1..6 для всех зданий — "
      "в [`../reports/economy/scaling_prices.md`](../reports/economy/scaling_prices.md), генератор — "
      "[`compute/compute_scaling.py`](../../compute/compute_scaling.py).\n")
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
            label = f"{suf} — {PER_NAT_NAMES.get(suf, suf)}"
            anchor = heading_anchor(label)
            A(f"  - [{label}](#{anchor})")
    A("**[Общие постройки (по кластерам)](#общие-постройки-по-кластерам)**")
    for suf in ["mil", "sto", "mar", "por", "tow", "gol", "iro", "coa", "swa", "sga", "wga", "wwa"]:
        if by_suffix_c.get(suf):
            label = f"{suf} — {COMMON_NAMES.get(suf, suf)}"
            anchor = heading_anchor(label)
            A(f"  - [{label}](#{anchor})")
    mines_label = "Шахты — апгрейды (gol/iro/coa)"
    A(f"**[{mines_label}](#{heading_anchor(mines_label)})**")
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
        A("| Здание | Нация | HP | Время (g-сек) | cost% | F | W | S | G | I | C | ферма | производит |")
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
        A("| Здание (cluster) | Нации | HP | Время (g-сек) | cost% | F | W | S | G | I | C | Доп. |")
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
        if suf == "tow":
            out.extend(render_template("reference/03_buildings/tow_combat.md"))
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
    write_md(TREE_ROOT / "03_buildings" / "README.md", out)


# ---------- 04_units.md ----------

def write_units(data: dict) -> None:
    out = []
    A = out.append
    A("# 04. Юниты\n")
    A("[← Index](README.md)\n")
    A("Все юниты сгруппированы по классу. Для параллельного сравнения внутри класса см. "
      "[compare/](compare/README.md).\n")
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
        A("| Юнит | нации | HP | Время (g-сек) | F | G | I | урон | дальн. (тайл.) | перезарядка | пика | меч | пуля | картечь | стрела | ядро |")
        A("|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|")
        for sid in sorted(by_sid.keys()):
            entries = by_sid[sid]
            u = entries[0]
            w0 = primary_weapon(u)
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
    write_md(TREE_ROOT / "04_units" / "README.md", out)


# ---------- 05_upgrades.md ----------

def write_upgrades(data: dict) -> None:
    out = []
    A = out.append
    A("# 05. Апгрейды\n")
    A("[← Index](README.md)\n")
    A("Апгрейды сгруппированы по **месту** исследования: academy / blacksmith / mill / stable / barracks / mine / tower / wall / ...\n")
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
    A("- [Математика применения: порядок и комбинирование]"
      f"(#{heading_anchor('Математика применения: порядок и комбинирование')})")
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

    out.extend(render_template("reference/05_upgrades/order_math.md"))
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
        A("| Апгрейд | Нации | itype | val | % по ресурсам | F | W | S | G | I | C | Время |")
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
                if nat_count >= 18:
                    nat_str = "all"
                elif nat_count == 1:
                    nat_str = group[0]["nation"]
                else:
                    nat_str = ",".join(sorted(g["nation"] for g in group))
                pcts = first.get("resource_pcts") or {}
                if pcts:
                    pcts_str = " / ".join(f"{k} {v:+d}%" for k, v in sorted(pcts.items()))
                else:
                    pcts_str = "—"
                A(f"| {name_cell_short(first)} | {nat_str} "
                  f"| {first.get('itype_short') or '—'} | {fmt(first['value'])} "
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
    A("| Ресурс | buy_min | buy_def | buy_max | sell_min | sell_def | sell_max |")
    A("|---|---:|---:|---:|---:|---:|---:|")
    rates = data.get("market_rates", {})
    for res, vals in rates.items():
        if res.startswith("_"):
            continue
        A(f"| {res} | {vals['buycostmin']:.0f} | {vals['buycostdef']:.2f} | {vals['buycostmax']:.0f} "
          f"| {vals['sellcostmin']:.2f} | {vals['sellcostdef']:.2f} | {vals['sellcostmax']:.2f} |")
    A("")
    out.extend(render_template("reference/06_market/mechanics.md"))
    A("")
    A("### Примеры обменов на дефолтном курсе\n")
    A("Сколько Y получишь за 100 единиц X на свежем рынке. После пары сделок цифры сместятся к худшему.\n")
    A("| Продаёшь | Получаешь | Чего | По формуле |")
    A("|---|---:|---|---|")
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
            A(f"| {amount} {sell} | **{received}** | {buy} | floor({amount} × {sd:.2f} / {bd:.2f}) |")
    A("")
    A("### Численный пример сдвига курса\n")
    A("Что произойдёт с курсом после **одного** обмена 5000 food → wood на свежем рынке "
      "(food.sellcost = 15.20, wood.buycost = 50.00):\n")
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
        A(f"- Получено wood: `floor(5000 × 15.20 / 50.00) = {bought_wood}`.")
        A(f"- `wood.buycost`: 50.00 → **{new_wood_buy:.3f}** "
          f"(сдвиг на {(new_wood_buy - 50) / 50 * 100:+.2f}%, к buycostmax = 60).")
        A(f"- `wood.sellcost`: 30.00 → **{new_wood_sell:.3f}** "
          f"(к sellcostmax = 40).")
        A(f"- `food.sellcost`: 15.20 → **{new_food_sell:.3f}** "
          f"(сдвиг на {(new_food_sell - 15.20) / 15.20 * 100:+.2f}%, к sellcostmin = 10.64). Догоняющий получит за свою еду меньше дерева.")
        A(f"- `food.buycost`: 25.00 → **{new_food_buy:.3f}** "
          f"(к buycostmin = 20). Зато купить food теперь чуть дешевле.")
        A("")
    A("Цены возвращаются к стандартным значениям со скоростью ≈ 2.5%/g-сек отклонения в обе стороны. "
      "Полупериод — около 28 g-секунд (≈ 20 real-сек @ fast). Через минуту-две большая часть "
      "сдвига откатится — но если торгуешь часто или крупными партиями, курс хронически «болеет».\n")
    out.extend(render_template("reference/06_market/strategy.md"))
    write_md(TREE_ROOT / "06_market" / "README.md", out)


# ---------- 07_naval.md ----------

# Каталог морских юнитов: sid + русский класс. Порядок управляет таблицами
# в шаблоне `reference/07_naval/main.md`. Цифры (HP / speed / cost / weapons)
# подтягиваются из `data.json`.
NAVAL_SHIPS: list[tuple[str, str]] = [
    ("fishboat",  "Рыбачья лодка"),
    ("ferry",     "Транспорт"),
    ("yacht",     "Лёгкий стрелок"),
    ("chaika",    "Лёгкий стрелок (ukr)"),
    ("yachttur",  "Лёгкий стрелок (tur)"),
    ("galley",    "Артиллерийский"),
    ("frigate",   "Тяжёлый стрелок"),
    ("xebec",     "Тяжёлый стрелок (alg/tur)"),
    ("battleship", "Линейный корабль"),
]


def _naval_cost_str(u: dict) -> str:
    """Сжатая запись цены: `450 G / 900 W / 150 I / 200 C` — пропускаем нулевые."""
    parts: list[str] = []
    for res, label in (("food", "F"), ("wood", "W"), ("stone", "S"),
                       ("gold", "G"), ("iron", "I"), ("coal", "C")):
        v = u.get(res)
        if v:
            parts.append(f"{v} {label}")
    return " / ".join(parts) if parts else "—"


def _naval_shot_cost_str(cost: dict | None) -> str:
    """Стоимость одного выстрела: `4 I + 9 C` (или `—` если ничего не тратится)."""
    if not cost:
        return "—"
    parts: list[str] = []
    for res, label in (("iron", "I"), ("coal", "C"), ("wood", "W"),
                       ("stone", "S"), ("gold", "G"), ("food", "F")):
        v = cost.get(res)
        if v:
            parts.append(f"{v} {label}")
    return " + ".join(parts) if parts else "—"


def _vision_tiles(vision_field: int | None) -> int:
    """Радиус FOW в тайлах — `floor(20 + 4 × vision)` из `_unit_GetVision`."""
    return 20 + 4 * (vision_field or 0)


def _naval_catalog_table(by_sid: dict[str, dict]) -> str:
    L = [
        "| Корабль | Класс | HP | Speed | Vision (t) | Search (t) | Цена | Buildtime g-сек |",
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
        "| Корабль | № | dmg | pause (g-сек) | range (t) | kind | cost / выстрел |",
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
                f"| {w.get('kind') or '—'} | {_naval_shot_cost_str(w.get('cost'))} |"
            )
    return "\n".join(L)


def _naval_ferry_block(ferry: dict) -> str:
    bt = ferry.get("buildtime_sec") or 0
    real_sec = round(bt / 1.4, 1) if bt else "—"
    return "\n".join([
        "```",
        f"HP        = {fmt(ferry.get('hp'))}",
        f"speed     = {fmt(ferry.get('speed'))}",
        f"transport = {fmt(ferry.get('transport'))}    (количество «слотов» под пехоту/кавалерию)",
        f"buildtime = {fmt(bt)} g-сек ({real_sec} real-сек @ fast)",
        f"cost      = {_naval_cost_str(ferry)}",
        "оружие    = нет (не атакует)",
        f"vision    = {_vision_tiles(ferry.get('vision'))} t",
        "```",
    ])


def _naval_fishboat_block(fb: dict) -> str:
    return "\n".join([
        "```",
        f"HP            = {fmt(fb.get('hp'))}",
        f"speed         = {fmt(fb.get('speed'))}",
        f"fishingmax    = {fmt(fb.get('fishingmax'))}    (ёмкость накопителя food)",
        f"fishingspeed  = {fmt(fb.get('fishingspeed'))}      (frames на единицу food)",
        f"buildtime     = {fmt(fb.get('buildtime_sec'))} g-сек",
        f"cost          = {_naval_cost_str(fb)}",
        "```",
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
        A("| Здание | HP | Время (g-сек) | cost% | F | W | S | G | I | C | ферма | производит |")
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
        A("| Здание | HP | Время (g-сек) | cost% | F | W | S | G | I | C | Доп. |")
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
            A("| Юнит | HP | Время (g-сек) | F | G | I | урон | дальн. (тайл.) | перезарядка | уникальность |")
            A("|---|---:|---:|---:|---:|---:|---:|---:|---:|---|")
            for u in sorted(units, key=lambda x: x["sid"]):
                w0 = primary_weapon(u)
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
        A(f"Полный список — в [главе «Апгрейды»](../05_upgrades/README.md).\n")
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
    import shutil
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
        "[← compare/](../README.md) · [← Index](../../README.md)\n",
        "См. [списком в compare/README.md](../README.md#unitsreadmemd--сравнения-юнитов).",
    ])
    write_md(cmp_buildings / "README.md", [
        "# Сравнения зданий\n",
        "[← compare/](../README.md) · [← Index](../../README.md)\n",
        "См. [списком в compare/README.md](../README.md#buildingsreadmemd--сравнения-зданий).",
    ])
    write_md(cmp_weapons / "README.md", [
        "# Каталог оружия\n",
        "[← compare/](../README.md) · [← Index](../../README.md)\n",
        "Не «сравнение по нациям», а **каталог типов оружия и снарядов** "
        "(`weaponsid` из `weapon.script`) с характеристиками и списком носителей. "
        "Здесь только проектильные параметры; стрелковые статы юнитов смотри в [units/](../units/README.md).",
    ])

    def write_unit_compare(filename: str, classes: list[str], title: str, intro: str) -> None:
        out = []
        A = out.append
        A(f"# {title}\n")
        A("[← units/](README.md) · [← compare/](../README.md) · [← Index](../../README.md)\n")
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
            "hp": "HP", "buildtime_sec": "Время (g-сек)",
            "food": "F", "gold": "G", "iron": "I",
            "consume_food": "апкип F (raw)",
            "consume_gold": "апкип G (raw)",
            "speed": "speed",
            "damage": "урон", "radiusmax_tiles": "дальность (тайл.)",
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
        A("> **Апкип**: `consume × 32 / 20000` за игр-секунду (raw consume — в скобках). "
          "**Speed**: единицы движка `t/g-сек × 50/1.5` (peasant=32, infantry=24, "
          "fasthorse=96, cannon≈22).\n")

        A("| Юнит | Нация | HP | Время (g-сек) | F | G | I | апкип F | апкип G | speed | урон | дальн. (тайл.) | перезарядка (с) | пика | меч | пуля | картечь | стрела | ядро | уникальность |")
        A("|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|")
        def _upkeep_cell(raw):
            if raw is None or raw == 0:
                return "—"
            per_sec = raw * 32 / 20000
            return f"{per_sec:.4f} ({raw})"
        for r in flat_rows:
            A(f"| {name_cell_short(r)} | {r['nation']} "
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
              f"| {r['uniqueness'] or '—'} |")
        write_md(cmp_units / filename, out)

    write_unit_compare("pikemen.md", ["Pikemen 17c"], "Пикинёры (17 в.)",
                        "Базовая пехота ближнего боя с пиками. Эффективна против кавалерии — высокая защита от картечи.")
    write_unit_compare("pikemen18.md", ["Pikemen 18c"], "Пикинёры (18 в.)",
                        "Поздние пикинёры с улучшенной бронёй.")
    write_unit_compare("light_infantry.md", ["Light Infantry"], "Лёгкая пехота",
                        "Лёгкая пехота с мечом или саблей. Дешевле пикинёров, но слабее против кавалерии.")
    write_unit_compare("musketeers17.md", ["Musketeers 17c"], "Мушкетёры (17 в.)",
                        "Стрелки с пулевым оружием. У каждой нации свой вариант: Стрелец (rus), Янычар (tur), Сердюк (ukr).")
    write_unit_compare("musketeers18.md", ["Musketeers 18c"], "Мушкетёры (18 в.)",
                        "Поздние мушкетёры — выше урон, лучше броня.")
    write_unit_compare("special_infantry_18c.md", ["18c special infantry"], "Особая пехота (18 в.)",
                        "Уникальные национальные стрелки 18 в., строящиеся в той же казарме 18 в., "
                        "что и `musketeer18` — Хайлендер (sco), Пандур (aus), Секей (hun), Шассёр (fra), "
                        "Йегер (por/swi). Альтернатива базовому мушкетёру: чаще быстрее или с особым уроном, "
                        "но в среднем дешевле и слабее по HP.")
    write_unit_compare("grenadiers.md", ["Grenadiers"], "Гренадёры",
                        "Гранаты плюс мушкет. Эффективны против зданий и башен.")
    write_unit_compare("archers.md", ["Archers"], "Лучники",
                        "Лук и стрелы. Выгоднее всего против тяжёлой пехоты с низкой защитой от стрел.")
    write_unit_compare("light_cavalry.md", ["Light Cavalry"], "Лёгкая кавалерия",
                        "Лёгкая конница с саблей или копьём; `fasthorse speed = 96`.")
    write_unit_compare("dragoons.md", ["Dragoons"], "Драгуны",
                        "Конные стрелки. Основная тактика — «ударь и отойди».")
    write_unit_compare("heavy_cavalry.md", ["Heavy Cavalry"], "Тяжёлая кавалерия",
                        "Reiter, Cuirassier, Vityaz, Winged Hussar — таран.")
    write_unit_compare("siege.md", ["Cannons", "Mortars"], "Артиллерия",
                        "Пушка (ядро + картечь), мортира (для разрушения зданий). `speed = 20..24`.")
    write_unit_compare("ships.md", ["Fishing Boat", "Warships"], "Корабли",
                        "Морские юниты. Рыбацкая лодка добывает рыбу; военные корабли ведут морской бой.")
    write_unit_compare("peasants.md", ["Peasant"], "Крестьяне",
                        "8 типов крестьян (`peaaus` / `peaeng` / `peapol` / `pearus` / `peaspa` / "
                        "`peatur` / `peaukr` / `peasco`) — отличаются внешним видом и стартовыми HP.")
    write_unit_compare("officers.md", ["Officer"], "Офицеры",
                        "Офицер — командир отряда (squad leader), нанимается в казармах. "
                        "Пять национальных вариантов (`officer` / `officer18` / `officerrus` / `officersco` / `officertur`); "
                        "статы заметно расходятся по стоимости, времени найма и урону.")
    write_unit_compare("drummers.md", ["Drummer / Bagpiper"], "Барабанщики и волынщик",
                        "Музыкант — второй обязательный «якорь» отряда после офицера (`drummer` / `drummer18` / "
                        "`drummerrus` / `drummertur` / `bagpiper`). Без атаки. У `rus` и `tur` варианты ощутимо "
                        "отличаются по HP/стоимости от базового шаблона.")

    # Priests need a heal-specific table (different columns than the generic
    # damage/range/protection layout): heal radius/amount + gold upkeep matter.
    out = []
    A = out.append
    A("# Жрецы\n")
    A("[← units/](README.md) · [← compare/](../README.md) · [← Index](../../README.md)\n")
    A("Жрец — единственный юнит с лечебной способностью (`weapon.kind = heal`). "
      "Четыре национальных sid'а — `priest` (католический шаблон), `pope` (Россия/Украина), "
      "`mullah` (Турция/Алжир), `padre` (Пьемонт). У всех `pause = 0` (heal-«выстрел» инициируется "
      "целью без перезарядки), но **дальность** и **сила хила за такт** различаются. Также различен "
      "потребляемый золотой апкип (`consume.gold` за игр-секунду по правилу `consume × 32 / 20000`).\n")
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
    A("| Юнит | Sid | HP | Время (g-сек) | F | G | Хил/такт | Радиус хила (тайл.) | Золото-апкип (за такт = 1 игр-сек) | Используют нации |")
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
          f"| {', '.join(nations_with)} |")
    A("")
    A("> **Pause = 0**: жрец начинает «качать» здоровье цели сразу после выбора, без cooldown'а "
      "между тактами. Реальный темп лечения = `Хил/такт × тики_в_секунду` (см. "
      "[ticks_and_subticks.md](../../../../internals/engine/ticks_and_subticks.md) — heal-такт "
      "управляется тем же `gc_time_to_frames` циклом).\n")
    A("> **Источник статов**: `unit.script:1151-1188` — общий блок `'priest','pope','mullah','padre'` "
      "плюс `if (objprop.sid='X') then begin … end` цепочка для пер-sid override'ов.")
    write_md(cmp_units / "priests.md", out)

    # Weapons catalog (projectile-level data)
    out = []
    A = out.append
    A("# Каталог оружия (projectile-level)\n")
    A("[← weapons/](README.md) · [← compare/](../README.md) · [← Index](../../README.md)\n")
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
    write_md(cmp_weapons / "projectiles.md", out)

    def write_building_compare(filename: str, sid_suffix: str, title: str, intro: str,
                                kind: str = "per-nation") -> None:
        out = []
        A = out.append
        A(f"# {title}\n")
        A("[← buildings/](README.md) · [← compare/](../README.md) · [← Index](../../README.md)\n")
        A(intro + "\n")
        rows = sorted([b for b in data["buildings"]
                       if b["sid"].endswith(sid_suffix) and b["kind"] == kind],
                      key=lambda x: x["nation"])
        baseline_cols = ["hp", "buildtime_sec", "costpercent", "wood", "stone", "gold", "farm"]
        baselines = compute_baselines(rows, baseline_cols)
        BLD_LABELS = {
            "hp": "HP", "buildtime_sec": "Время (g-сек)",
            "costpercent": "cost%", "wood": "W", "stone": "S",
            "gold": "G", "farm": "ферма",
        }
        A("> **Базовые значения** (мода по столбцу): "
          + ", ".join(f"{BLD_LABELS.get(k, k)} = {v}" for k, v in baselines.items()
                       if v is not None) + ".")
        A("> **Жирным** в таблице ниже — отклонения от этих значений.\n")
        A("| Здание | Нация | HP | Время (g-сек) | cost% | W | S | G | ферма | производит |")
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
        write_md(cmp_buildings / filename, out)

    write_building_compare("town_halls.md", "cen", "Ратуши (Town Halls)",
                            "Главные здания всех 21 нации. Австрийская строится за 4.69 секунды "
                            "(исключение). Украинская даёт +200 farm (макс), Российская — +75 (мин).")

    # Barracks needs two sections (17c + 18c) — special-case
    out = []
    A = out.append
    A("# Казармы (17 в. и 18 в.)\n")
    A("[← buildings/](README.md) · [← compare/](../README.md) · [← Index](../../README.md)\n")
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
        A("| Здание | Нация | HP | Время (g-сек) | cost% | W | S | G | ферма | производит |")
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
    write_md(cmp_buildings / "barracks.md", out)

    # New per-nation building compares (gap fill: aca/art/bla/dip/hou/sta/tem).
    # All seven are unique per-nation buildings in the same vein as town_halls/barracks.
    write_building_compare("academies.md", "aca", "Академии",
                            "Академия — здание апгрейдов общего профиля. Один вариант на нацию.")
    write_building_compare("artillery_depots.md", "art", "Артиллерийские депо",
                            "Тренируют пушки/мортиры. Производственный список варьируется (например, "
                            "у Алжира нет multicannon).")
    write_building_compare("blacksmiths.md", "bla", "Кузницы",
                            "Кузница — апгрейды защиты пехоты и оружия. Стоимость и время заметно "
                            "различаются по нациям.")
    write_building_compare("diplomatic_centers.md", "dip", "Дипломатические центры",
                            "Тренируют наёмников. Производственный список общий (наёмники-юниты), но "
                            "стоимость постройки сильно варьирует.")
    write_building_compare("houses.md", "hou", "Дома",
                            "Дом увеличивает лимит population (`farm`). Базовая farm одинакова (25), "
                            "цена и HP различаются.")
    write_building_compare("stables.md", "sta", "Конюшни",
                            "Тренируют кавалерию. У большинства наций — общий пул юнитов, у `rus`/`ukr` "
                            "уникальные тяжёлые всадники.")
    write_building_compare("temples.md", "tem", "Соборы / Церкви / Мечети",
                            "Тренируют жреца (`priest`/`pope`/`mullah`/`padre`). Разная стоимость и "
                            "время постройки. См. также [units/priests.md](../units/priests.md) — "
                            "сравнение самих жрецов.")

    # Common-cluster buildings (mill/market/storehouse/port/towers/mines/walls) live in
    # 4-5 cluster variants (eur/rus/tur/ukr/sco). Useful to compare cluster-vs-cluster.
    write_building_compare("mills.md", "mil", "Мельницы",
                            "Поле-фабрика: где можно строить поля. Один вариант на cluster (eur/rus/tur/ukr/sco).",
                            kind="common")
    write_building_compare("markets.md", "mar", "Рынки",
                            "Точка обмена ресурсов и закупа. Один вариант на cluster.",
                            kind="common")
    write_building_compare("storehouses.md", "sto", "Склады",
                            "Точка сдачи дерева/камня. Один вариант на cluster.",
                            kind="common")
    write_building_compare("ports.md", "por", "Порты",
                            "Корабельная верфь и точка сдачи рыбы. Один вариант на cluster.",
                            kind="common")
    write_building_compare("towers.md", "tow", "Башни",
                            "Оборонительная башня с пушкой. Один вариант на cluster.",
                            kind="common")

    # Mines: 3 resource types (coa/gol/iro) × cluster — group all into one page.
    out = []
    A = out.append
    A("# Шахты\n")
    A("[← buildings/](README.md) · [← compare/](../README.md) · [← Index](../../README.md)\n")
    A("Шахты добывают `coal` / `gold` / `iron`. Скрипт случайно использует `commonsid+'X'` "
      "для всех cluster'ов (eur/rus/tur/ukr/sco), но статы — общие: парсер surface'ит только "
      "`eur*` версию, потому что все cluster'ы наследуют одинаковые HP/цену/rate. "
      "Cluster-специфичных шахт **нет** — это единая модель для всех наций.\n")
    rows = sorted([b for b in data["buildings"]
                   if b["sid"].endswith(("coa","gol","iro")) and b["kind"] == "common"],
                  key=lambda x: (x["sid"], x["nation"]))
    seen = set()
    rows = [b for b in rows if not (b["sid"] in seen or seen.add(b["sid"]))]
    baseline_cols = ["hp", "buildtime_sec", "wood", "stone", "gold"]
    baselines = compute_baselines(rows, baseline_cols)
    A("| Здание | Cluster | Ресурс | HP | Время (g-сек) | W | S | G | rate (за такт) | Доп. рабочих |")
    A("|---|---|---|---:|---:|---:|---:|---:|---:|---:|")
    for b in rows:
        produce = b.get("produce") or {}
        res, rate = next(iter(produce.items()), ("—", "—"))
        A(f"| {name_cell_short(b)} | {b['sid'][:3]} | {res} "
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
    """Write output/README.md — single entry-point listing every artifact."""
    out = []
    A = out.append
    A("# Cossacks 3 — каталог артефактов\n")
    banner = _version_banner(data)
    if banner:
        A(banner + "\n")
    A("Все сгенерированные файлы для справочника по игре. Главная точка входа.\n")
    out.extend(render_template("output_readme.md"))
    A("")
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
