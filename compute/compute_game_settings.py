"""Extract all lobby/game settings from dmscript.global + locale.

Two outputs:
  1. `derived/game_settings.json` — machine-readable, consumed by the editor.
  2. `docs/reports/map/lobby_settings.md` — human-readable reference table set.

Source-of-truth for the *behavior* of each option: `docs/recon/game_settings.md`
(handwritten reverse-engineering of the engine's reaction to each value).

Run after game patch:
    python compute/compute_game_settings.py

JSON schema (`game_settings.json`) — list of `{value, label_en, label_ru, ...}`
per category (`mapsize`, `terraintype`, `relieftype`, `resourcestart`,
`resourcemines`, `season`, `startingunits`, `balloon`, `cannons`, `peacetime`,
`century18`, `capture`, `marketdip`, `teams`, `limit`, `gamespeed`,
`adviserassistant`, `difficulty`) plus `defaults` from `initmap.inc:29-31`.
"""
from __future__ import annotations
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "parser"))
from citations import Citations
from config import DM_GLOBAL, LOCALE, DERIVED_DIR, REPORTS_MAP_DIR

# Module-level citations registry — populated during render_lobby_md().
cites = Citations()
from parse_locale import parse_locale_file


def _loc(loc, key):
    v = loc.get(key, "")
    return v.split("\n", 1)[0].strip() if v else ""


def build_settings():
    en = parse_locale_file(LOCALE / "en" / "gui.txt")
    ru = parse_locale_file(LOCALE / "ru" / "gui.txt")

    def pair(key):
        return {"label_en": _loc(en, key), "label_ru": _loc(ru, key)}

    out = {}

    # ─── gen.mapsize (no locale, hardcoded) ────────────────────────────
    out["mapsize"] = [
        {"value": 0, "tiles": 320, "label_en": "Standard",  "label_ru": "Стандартная"},
        {"value": 1, "tiles": 480, "label_en": "Big",       "label_ru": "Большая"},
        {"value": 2, "tiles": 640, "label_en": "Huge",      "label_ru": "Огромная"},
        {"value": 3, "tiles": 256, "label_en": "Tiny",      "label_ru": "Маленькая"},
    ]

    # ─── gen.terraintype ───────────────────────────────────────────────
    out["terraintype"] = [
        {"value": v, **pair(f"randommap.terraintype.{v}")} for v in range(10)
    ]

    # ─── gen.relieftype ────────────────────────────────────────────────
    out["relieftype"] = [
        {"value": v, **pair(f"randommap.relieftype.{v}")} for v in range(6)
    ]

    # ─── gen.resourcestart ─────────────────────────────────────────────
    AMOUNTS = {0: 1000, 1: 4000, 2: 5000, 3: 1000000}
    out["resourcestart"] = [
        {"value": v, "amount": AMOUNTS[v], **pair(f"randommap.initialresources.{v}")}
        for v in range(4)
    ]

    # ─── gen.resourcemines ─────────────────────────────────────────────
    out["resourcemines"] = [
        {"value": v, **pair(f"randommap.minerals.{v}")} for v in range(3)
    ]

    # ─── gen.season ────────────────────────────────────────────────────
    out["season"] = [
        {"value": 0, "label_ru": "Лето",     "label_en": "Summer"},
        {"value": 1, "label_ru": "Осень",    "label_en": "Autumn"},
        {"value": 2, "label_ru": "Зима",     "label_en": "Winter"},
        {"value": 3, "label_ru": "Пустыня",  "label_en": "Desert"},
    ]

    # ─── additional.startingunits ──────────────────────────────────────
    SU_KEYS = [
        (0,  "default"),
        (1,  "armysmall"),
        (2,  "armymedium"),
        (3,  "armylarge"),
        (4,  "peasantslot"),
        (5,  "differentnations"),
        (6,  "towers"),
        (7,  "cannons"),
        (8,  "cannonsandhowitzers"),
        (9,  "barrack18"),
        (10, "barrack17"),
        (11, "village"),
        (12, "logcabins"),
        (13, "union"),
    ]
    # Russian fallbacks for keys missing in locale
    SU_RU_FALLBACK = {
        "barrack17": "Казарма 17 в.",
        "village":   "Деревня",
        "logcabins": "Срубы",
        "union":     "Уния",
    }
    out["startingunits"] = []
    for v, k in SU_KEYS:
        info = pair(f"randommap.settings.startingunits.{k}")
        if not info["label_ru"]:
            info["label_ru"] = SU_RU_FALLBACK.get(k, k)
        if not info["label_en"]:
            info["label_en"] = k.replace("_", " ").title()
        out["startingunits"].append({"value": v, **info})

    # ─── additional.balloon ────────────────────────────────────────────
    out["balloon"] = [
        {"value": 0, **pair("randommap.settings.balloon.default")},
        {"value": 1, **pair("randommap.settings.balloon.no")},
        {"value": 2, **pair("randommap.settings.balloon.with")},
    ]

    # ─── additional.cannons ────────────────────────────────────────────
    out["cannons"] = [
        {"value": 0, **pair("randommap.settings.cannons.default")},
        {"value": 1, **pair("randommap.settings.cannons.nocannonstowerswalls")},
        {"value": 2, **pair("randommap.settings.cannons.expensivecannons")},
    ]

    # ─── additional.peacetime ──────────────────────────────────────────
    PEACETIME_MIN = {0: 0, 1: 10, 2: 20, 3: 30, 4: 45, 5: 60, 6: 90, 7: 120, 8: 180, 9: 240, 11: 15}
    PEACETIME_LOC_KEY = {0: "default", 1: "10", 2: "20", 3: "30", 4: "45", 5: "60",
                         6: "90", 7: "120", 8: "180", 9: "240", 11: "15"}
    out["peacetime"] = []
    for v, key in PEACETIME_LOC_KEY.items():
        m = PEACETIME_MIN[v]
        info = pair(f"randommap.settings.peacetime.{key}")
        out["peacetime"].append({
            "value": v,
            "minutes_g": m,
            "gsec": m * 60,
            **info,
        })
    out["peacetime"].sort(key=lambda x: x["value"])

    # ─── additional.century18 ──────────────────────────────────────────
    out["century18"] = [
        {"value": 0, **pair("randommap.settings.century18.default")},
        {"value": 1, **pair("randommap.settings.century18.no")},
        {"value": 2, **pair("randommap.settings.century18.with")},
    ]

    # ─── additional.capture ────────────────────────────────────────────
    out["capture"] = [
        {"value": 0, **pair("randommap.settings.capture.default")},
        {"value": 1, **pair("randommap.settings.capture.nopeasants")},
        {"value": 2, **pair("randommap.settings.capture.nocenterspeasants")},
        {"value": 3, **pair("randommap.settings.capture.onlyartillery")},
    ]

    # ─── additional.marketdip ──────────────────────────────────────────
    MD_KEYS = ["default", "nodip", "nomarket", "noboth"]
    out["marketdip"] = [
        {"value": v, **pair(f"randommap.settings.marketdip.{k}")} for v, k in enumerate(MD_KEYS)
    ]
    # value 4 = expensivemercs (locale not always present — fallback)
    em = pair("randommap.settings.marketdip.expensivemercs")
    if not em["label_en"]: em["label_en"] = "Expensive Mercenaries"
    if not em["label_ru"]: em["label_ru"] = "Дорогие наёмники"
    out["marketdip"].append({"value": 4, **em})

    # ─── additional.teams ──────────────────────────────────────────────
    out["teams"] = [
        {"value": 0, **pair("randommap.settings.teams.default")},
        {"value": 1, **pair("randommap.settings.teams.nearby")},
    ]

    # ─── additional.limit ──────────────────────────────────────────────
    LIMIT_UNITS = {0: None, 1: 500, 2: 750, 3: 1000, 4: 1500, 5: 2200, 6: 3000, 7: 5000, 8: 8000}
    out["limit"] = []
    for v, units in LIMIT_UNITS.items():
        if v == 0:
            info = pair("randommap.settings.limit.default")
            label_en = info["label_en"] or "Map default"
            label_ru = info["label_ru"] or "Без явного лимита"
        else:
            label_en = f"{units} units"
            label_ru = f"{units} юнитов"
        out["limit"].append({"value": v, "units": units, "label_en": label_en, "label_ru": label_ru})

    # ─── additional.gamespeed ──────────────────────────────────────────
    out["gamespeed"] = [
        {"value": 0, "ticks_per_sec": 7,  "factor": 0.7, "label_ru": "Медленно",  "label_en": "Slow"},
        {"value": 1, "ticks_per_sec": 10, "factor": 1.0, "label_ru": "Нормально", "label_en": "Normal"},
        {"value": 2, "ticks_per_sec": 14, "factor": 1.4, "label_ru": "Быстро",    "label_en": "Fast"},
    ]

    # ─── additional.adviserassistant ───────────────────────────────────
    out["adviserassistant"] = [
        {"value": 0, **pair("randommap.settings.adviserassistant.default")},
        {"value": 1, **pair("randommap.settings.adviserassistant.without")},
    ]

    # ─── difficulty ────────────────────────────────────────────────────
    out["difficulty"] = [
        {"value": 0, "koef": 0.30, "label_ru": "Легко",       "label_en": "Easy"},
        {"value": 1, "koef": 0.50, "label_ru": "Нормально",   "label_en": "Normal"},
        {"value": 2, "koef": 0.75, "label_ru": "Сложно",      "label_en": "Hard"},
        {"value": 3, "koef": 1.00, "label_ru": "Очень сложно","label_en": "Very Hard"},
        {"value": 4, "koef": 1.25, "label_ru": "Невозможно",  "label_en": "Impossible"},
    ]

    # ─── defaults from initmap.inc:29-31 ───────────────────────────────
    out["defaults"] = {
        "gen": {
            "mapsize": 0,           # не задано в initmap.inc; default = stand. ?
            "terraintype": 0,       # Land
            "relieftype": 3,        # Highlands (initmap.inc:29)
            "resourcestart": 2,     # Thousands / 5000 (initmap.inc:30)
            "resourcemines": 1,     # Medium (initmap.inc:31)
            "season": 0,            # Summer
        },
        "additional": {
            "startingunits": 0,     # Default
            "balloon": 0,
            "cannons": 0,
            "peacetime": 0,         # No peace time
            "century18": 0,
            "capture": 0,
            "marketdip": 0,
            "teams": 0,
            "limit": 0,             # map default
            "gamespeed": 2,         # Fast
            "adviserassistant": 0,
        },
    }

    return out


# =============================================================================
# Markdown rendering — `docs/reports/map/lobby_settings.md`
# =============================================================================

def _intro_lines(cites: Citations) -> list[str]:
    """Top-of-document text. Uses module-level `cites` for the one citation."""
    settings_cite = cites.cite("lib/classes.script:85-88",
                                label="определение `TMapSettings` (`gMap.settings`)")
    return [
        "# Настройки лобби — справочник значений",
        "",
        "**Производный отчёт.** Считается из локали игры и `dmscript.global` скриптом",
        "[`compute/compute_game_settings.py`](../../../compute/compute_game_settings.py).",
        "Регенерация: `python compute/compute_game_settings.py`.",
        "",
        "Все названия опций — **из локали игры** (`data/locale/ru/gui.txt`,",
        "`data/locale/en/gui.txt`). Если в игре написано «Высокогорье» — здесь тоже",
        "«Высокогорье». Машинная версия для редакторов и инструментов —",
        "[`derived/game_settings.json`](../../../derived/game_settings.json).",
        "",
        "Поведение каждой опции в движке (что происходит после выбора) — в",
        "[`docs/recon/world/map/game_settings.md`](../../recon/world/map/game_settings.md).",
        "",
        "## Структура",
        "",
        f"Все опции лобби живут в `gMap.settings` {settings_cite}:",
        "",
        "- `gMap.settings.gen` — параметры **генератора карты** (как карта рисуется).",
        "- `gMap.settings.additional` — **правила игры** (peacetime, лимит населения,",
        "  захват, скорость и т. д.).",
    ]


def _section(title: str, key: str, settings: dict, *, columns: list[tuple[str, str]]) -> list[str]:
    """Render one settings table.

    `columns` is a list of `(header, attribute)` pairs. Special attributes:
      `value`     — integer enum value
      `label_en`  — English label
      `label_ru`  — Russian label
      anything else is fetched via `row.get(attribute)`.
    """
    rows = settings.get(key) or []
    if not rows:
        return []
    L = [f"### {title}", ""]
    headers = [c[0] for c in columns]
    L.append("| " + " | ".join(headers) + " |")
    L.append("| " + " | ".join(":---:" if h == "Значение" else "---" for h in headers) + " |")
    for row in rows:
        cells: list[str] = []
        for _, attr in columns:
            v = row.get(attr)
            if v is None:
                cells.append("—")
            else:
                cells.append(str(v))
        L.append("| " + " | ".join(cells) + " |")
    L.append("")
    return L


def render_lobby_md(settings: dict) -> list[str]:
    L = _intro_lines(cites)
    L.append("")

    # ─── gen ───────────────────────────────────────────────────────────────
    L += ["## Генератор карты — `gMap.settings.gen`", ""]
    L += _section(
        "`mapsize` — размер карты",
        "mapsize", settings,
        columns=[("Значение", "value"), ("Размер, тайлы", "tiles"),
                 ("Английский лейбл", "label_en"), ("Русский лейбл", "label_ru")],
    )
    mapsize_cite = cites.cite("lib/miscext2.script:19-26",
                              label="хардкод размеров `mapsize` в тайлах")
    L += [
        f"Размер карты — квадрат `tiles × tiles`. UI игры лейблов не "
        f"показывает (значения зашиты {mapsize_cite}).",
        "",
    ]
    L += _section(
        "`terraintype` — тип ландшафта и воды",
        "terraintype", settings,
        columns=[("Значение", "value"),
                 ("Английский лейбл", "label_en"), ("Русский лейбл", "label_ru")],
    )
    maritime_cite = cites.cite("lib/misc.script:5466",
                               label="`_misc_HasMaritime` — проверка terrain-морских опций")
    L += [
        f"Лейблы из `gui.txt @randommap.terraintype.*`. Значения `2..4` "
        f"(`Полуострова` / `Острова` / `Континенты`) проверяются движком "
        f"в `_misc_HasMaritime` {maritime_cite} — на этих картах есть "
        f"«морские» воды, доступ к ним требует порта.",
        "",
    ]
    L += _section(
        "`relieftype` — рельеф",
        "relieftype", settings,
        columns=[("Значение", "value"),
                 ("Английский лейбл", "label_en"), ("Русский лейбл", "label_ru")],
    )
    initmap29_cite = cites.cite("common.inc/initmap.inc:29",
                                 label="дефолт `relieftype = 3` (Highlands)")
    L += [
        f"По умолчанию `relieftype = 3` («Высокогорье») {initmap29_cite}.",
        "",
    ]
    L += _section(
        "`resourcestart` — стартовые ресурсы у игроков",
        "resourcestart", settings,
        columns=[("Значение", "value"), ("На каждый ресурс", "amount"),
                 ("Английский лейбл", "label_en"), ("Русский лейбл", "label_ru")],
    )
    initmap30_cite = cites.cite("common.inc/initmap.inc:30",
                                 label="дефолт `resourcestart = 2` (Thousands)")
    L += [
        f"Все 6 ресурсов (food / wood / stone / gold / iron / coal) получают "
        f"одинаковое стартовое количество. По умолчанию = 2 («Тысячи», 5 000 "
        f"каждого) {initmap30_cite}.",
        "",
    ]
    L += _section(
        "`resourcemines` — плотность месторождений",
        "resourcemines", settings,
        columns=[("Значение", "value"),
                 ("Английский лейбл", "label_en"), ("Русский лейбл", "label_ru")],
    )
    initmap31_cite = cites.cite("common.inc/initmap.inc:31",
                                 label="дефолт `resourcemines = 1` (Medium)")
    L += [
        f"По умолчанию `resourcemines = 1` («Средне») {initmap31_cite}. "
        f"Конкретные числа шахт за уровень — в "
        f"[`map_resources.md`](map_resources.md) и в "
        f"[`recon/world/map/map_generation_pipeline.md`](../../recon/world/map/map_generation_pipeline.md).",
        "",
    ]
    L += _section(
        "`season` — сезон",
        "season", settings,
        columns=[("Значение", "value"),
                 ("Английский лейбл", "label_en"), ("Русский лейбл", "label_ru")],
    )
    desert_cite = cites.cite("common.inc/dogenerate.inc:4",
                              label="форсирование `bDesert := True` при `season = 3`")
    L += [
        f"Лейблов в `gui.txt` нет — UI хардкодит. Единственный механический "
        f"эффект — `season = 3` («Пустыня») форсит `bDesert = True` "
        f"{desert_cite}; engine использует другой набор pattern-типов "
        f"(`desert_*` вместо обычных лесов и камней).",
        "",
    ]

    # ─── additional ────────────────────────────────────────────────────────
    L += ["## Правила игры — `gMap.settings.additional`", ""]

    L += _section(
        "`startingunits` — стартовая армия",
        "startingunits", settings,
        columns=[("Значение", "value"),
                 ("Английский лейбл", "label_en"), ("Русский лейбл", "label_ru")],
    )
    csp_cite = cites.cite("common.inc/dogenerate.inc:1231-1281",
                           label="`CreateStartPointPeasants` — расстановка 18 крестьян 6×3")
    L += [
        f"Конкретный набор юнитов на каждый вариант — в "
        f"`data/game/var/startingsettings.cfg` (`addresources`, `countries`).",
        "",
        f"> Независимо от выбора движок всегда вызывает "
        f"`CreateStartPointPeasants` {csp_cite} и размещает **18 крестьян** "
        f"в сетке 6×3 вокруг стартовой точки. Даже на `startingunits = 0` "
        f"(«По умолчанию») у игрока сразу 18 крестьян.",
        "",
    ]

    L += _section(
        "`balloon` — монгольфьеры",
        "balloon", settings,
        columns=[("Значение", "value"),
                 ("Английский лейбл", "label_en"), ("Русский лейбл", "label_ru")],
    )
    L += [
        "Монгольфьер — особый юнит, открывающий обзор на большой высоте.",
        "",
    ]

    L += _section(
        "`cannons` — пушки, башни и стены",
        "cannons", settings,
        columns=[("Значение", "value"),
                 ("Английский лейбл", "label_en"), ("Русский лейбл", "label_ru")],
    )
    L += [
        "Опция «Дорогие пушки» поднимает цены пушек через апгрейд — точные "
        "множители читать в `country.script` (раздел артиллерийских апгрейдов).",
        "",
    ]

    L += _section(
        "`peacetime` — время мира",
        "peacetime", settings,
        columns=[("Значение", "value"), ("Минут (игр.)", "minutes_g"),
                 ("g-секунд", "gsec"),
                 ("Английский лейбл", "label_en"), ("Русский лейбл", "label_ru")],
    )
    L += [
        "Минуты — **игровые**. На скорости fast (`gamespeed = 2`, ×1.4) одна "
        "игровая минута = 60 / 1.4 ≈ 42.9 реальных секунд: 10-минутный мир "
        "длится ≈ 7 реальных минут. Значение `value = 11` (15 минут) лежит "
        "между `1` и `2` — историческая неровность; movement к концу таблицы.",
        "",
        "Подробности механики (как движок блокирует поиск врагов, ничейные "
        "ячейки, переход от мира к войне) — в "
        "[`recon/world/map/game_settings.md`](../../recon/world/map/game_settings.md#peacetime--как-устроен-мир).",
        "",
    ]

    L += _section(
        "`century18` — переход в 18 век",
        "century18", settings,
        columns=[("Значение", "value"),
                 ("Английский лейбл", "label_en"), ("Русский лейбл", "label_ru")],
    )
    L += [
        "На 17 в.-only нациях (Украина, Турция, Алжир) опция «Сразу» бесполезна — "
        "у них нет апгрейда `<nat>cen.1` («Переход в 18 век»).",
        "",
    ]

    L += _section(
        "`capture` — правила захвата",
        "capture", settings,
        columns=[("Значение", "value"),
                 ("Английский лейбл", "label_en"), ("Русский лейбл", "label_ru")],
    )
    L += [
        "Геометрия захвата (радиусы, кто захватывается, кто нет) — в "
        "[`recon/world/economy/capture_mechanics.md`](../../recon/world/economy/capture_mechanics.md).",
        "",
    ]

    L += _section(
        "`marketdip` — рынок и дипцентр",
        "marketdip", settings,
        columns=[("Значение", "value"),
                 ("Английский лейбл", "label_en"), ("Русский лейбл", "label_ru")],
    )
    L += [
        "Опция `value = 4` («Дорогие наёмники») умножает цену найма в дипцентре "
        "на `gc_gameplay_expensivemercskoef = 3`. Подробности про наёмников — в "
        "[`recon/systems/mercenaries_diplomacy.md`](../../recon/systems/mercenaries_diplomacy.md).",
        "",
    ]

    L += _section(
        "`teams` — расположение союзников",
        "teams", settings,
        columns=[("Значение", "value"),
                 ("Английский лейбл", "label_en"), ("Русский лейбл", "label_ru")],
    )
    L += [
        "При `teams = 1` команда стартует в соседних позициях, а не "
        "разбросанной по карте.",
        "",
    ]

    L += _section(
        "`limit` — лимит населения",
        "limit", settings,
        columns=[("Значение", "value"), ("Юнитов", "units"),
                 ("Английский лейбл", "label_en"), ("Русский лейбл", "label_ru")],
    )
    L += [
        "Это **глобальный потолок поверх** локального лимита, считаемого по "
        "зданиям: `pop_cap = cen × 100 + bar × 150 + ba2 × 250 + hou × 25`. "
        "Глобальный потолок никогда не превышается, даже если ферм-бонус "
        "позволяет больше.",
        "",
    ]

    L += _section(
        "`gamespeed` — скорость партии",
        "gamespeed", settings,
        columns=[("Значение", "value"), ("Тиков/реальная секунда", "ticks_per_sec"),
                 ("Множитель к норме", "factor"),
                 ("Английский лейбл", "label_en"), ("Русский лейбл", "label_ru")],
    )
    L += [
        "`gc_time_to_frames = 32` для всех скоростей (32 кадра в одной игровой "
        "секунде) — меняется только real-time-фактор. Слот `value = 3` (×2.0) "
        "был, но в текущей версии закомментирован.",
        "",
    ]

    L += _section(
        "`adviserassistant` — помощник",
        "adviserassistant", settings,
        columns=[("Значение", "value"),
                 ("Английский лейбл", "label_en"), ("Русский лейбл", "label_ru")],
    )
    L += [
        "Контекстные подсказки в углу экрана. Не влияет на симуляцию — только UI.",
        "",
    ]

    # ─── difficulty ────────────────────────────────────────────────────────
    L += ["## Сложность ИИ — `gc_player_difficulty_*`", ""]
    L += _section(
        "`difficulty` — сложность",
        "difficulty", settings,
        columns=[("Значение", "value"), ("Множитель скорости", "koef"),
                 ("Английский лейбл", "label_en"), ("Русский лейбл", "label_ru")],
    )
    L += [
        "Только AI-игроки. «Преимущество» сложности — это множитель к скорости "
        "постройки/найма (`koef`), стартовых ресурсов AI **не получает** ни на "
        "какой сложности. Поведение AI разобрано в "
        "[`recon/systems/ai_behavior.md`](../../recon/systems/ai_behavior.md).",
        "",
    ]

    # ─── defaults ──────────────────────────────────────────────────────────
    defaults = settings.get("defaults") or {}
    if defaults:
        defaults_cite = cites.cite("common.inc/initmap.inc:29-31",
                                    label="дефолты блока `gen` (relieftype, resourcestart, resourcemines)")
        L += [
            "## Значения по умолчанию",
            "",
            f"Из {defaults_cite} (для `gen`) и общего поведения движка (для "
            f"`additional`):",
            "",
            "| Поле | Значение по умолчанию |",
            "| --- | --- |",
        ]
        for section_name in ("gen", "additional"):
            section = defaults.get(section_name) or {}
            for k, v in section.items():
                L.append(f"| `settings.{section_name}.{k}` | `{v}` |")
        L.append("")

    L += [
        "---",
        "",
        "**См. также:**",
        "",
        "- [`docs/recon/world/map/game_settings.md`](../../recon/world/map/game_settings.md) — поведение "
        "движка по каждой опции (peacetime, peace mode, captureradius, …).",
        "- [`derived/game_settings.json`](../../../derived/game_settings.json) — "
        "то же самое в машинно-читаемом виде.",
        "- [`docs/recon/world/map/map_generation_pipeline.md`](../../recon/world/map/map_generation_pipeline.md) — "
        "что именно делает генератор карты с этими значениями.",
        "",
    ]
    L += cites.render()
    return L


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    settings = build_settings()
    DERIVED_DIR.mkdir(parents=True, exist_ok=True)
    REPORTS_MAP_DIR.mkdir(parents=True, exist_ok=True)

    json_path = DERIVED_DIR / "game_settings.json"
    json_path.write_text(json.dumps(settings, ensure_ascii=False, indent=2), encoding="utf-8")
    total = sum(len(v) for v in settings.values() if isinstance(v, list))
    print(f"Wrote {json_path} ({total} enum values across {len(settings) - 1} categories)")

    md_path = REPORTS_MAP_DIR / "lobby_settings.md"
    md_path.write_text("\n".join(render_lobby_md(settings)), encoding="utf-8")
    print(f"Wrote {md_path} ({md_path.stat().st_size:,} bytes)")


if __name__ == "__main__":
    main()
