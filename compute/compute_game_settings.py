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
    return [
        "# Настройки матча",
        "",
        "[← Таблицы и расчёты](../README.md)",
        "",
        "Канонические русские названия всех параметров лобби и краткое описание",
        "их действия. Внутренний номер нужен только для сопоставления с реплеями",
        "и файлами игры; английское название показано вторым.",
        "",
        "Подробное объяснение скрытого поведения находится в статье",
        "[«Как настройки влияют на игру»](../../recon/world/map/game_settings.md).",
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
    L += ["## Карта и природные ресурсы", ""]
    L += _section(
        "Размер карты (`mapsize`)",
        "mapsize", settings,
        columns=[("Значение", "value"), ("Размер, тайлы", "tiles"),
                 ("Русское название", "label_ru"), ("Английское название", "label_en")],
    )
    mapsize_cite = cites.cite("lib/miscext2.script:19-26",
                              label="хардкод размеров `mapsize` в тайлах")
    L += [
        f"Карта всегда квадратная; размер в тайлах задан непосредственно игрой "
        f"{mapsize_cite}.",
        "",
    ]
    L += _section(
        "Тип ландшафта и воды (`terraintype`)",
        "terraintype", settings,
        columns=[("Значение", "value"),
                 ("Русское название", "label_ru"), ("Английское название", "label_en")],
    )
    maritime_cite = cites.cite("lib/misc.script:5466",
                               label="`_misc_HasMaritime` — проверка terrain-морских опций")
    L += [
        f"На полуостровах, островах и континентах есть морская вода, доступ "
        f"к которой требует порта {maritime_cite}.",
        "",
    ]
    L += _section(
        "Рельеф (`relieftype`)",
        "relieftype", settings,
        columns=[("Значение", "value"),
                 ("Русское название", "label_ru"), ("Английское название", "label_en")],
    )
    initmap29_cite = cites.cite("common.inc/initmap.inc:29",
                                 label="дефолт `relieftype = 3` (Highlands)")
    L += [
        f"По умолчанию `relieftype = 3` («Высокогорье») {initmap29_cite}.",
        "",
    ]
    L += _section(
        "Стартовые ресурсы (`resourcestart`)",
        "resourcestart", settings,
        columns=[("Значение", "value"), ("На каждый ресурс", "amount"),
                 ("Русское название", "label_ru"), ("Английское название", "label_en")],
    )
    initmap30_cite = cites.cite("common.inc/initmap.inc:30",
                                 label="дефолт `resourcestart = 2` (Thousands)")
    L += [
        f"Еда, дерево, камень, золото, железо и уголь получают "
        f"одинаковое стартовое количество. По умолчанию = 2 («Тысячи», 5 000 "
        f"каждого) {initmap30_cite}.",
        "",
    ]
    L += _section(
        "Количество месторождений (`resourcemines`)",
        "resourcemines", settings,
        columns=[("Значение", "value"),
                 ("Русское название", "label_ru"), ("Английское название", "label_en")],
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
        "Сезон (`season`)",
        "season", settings,
        columns=[("Значение", "value"),
                 ("Русское название", "label_ru"), ("Английское название", "label_en")],
    )
    desert_cite = cites.cite("common.inc/dogenerate.inc:4",
                              label="форсирование `bDesert := True` при `season = 3`")
    L += [
        f"Вариант «Пустыня» использует отдельный набор пустынных лесов и камней "
        f"{desert_cite}.",
        "",
    ]

    # ─── additional ────────────────────────────────────────────────────────
    L += ["## Правила партии", ""]

    L += _section(
        "Стартовая армия (`startingunits`)",
        "startingunits", settings,
        columns=[("Значение", "value"),
                 ("Русское название", "label_ru"), ("Английское название", "label_en")],
    )
    csp_cite = cites.cite("common.inc/dogenerate.inc:1231-1281",
                           label="`CreateStartPointPeasants` — расстановка 18 крестьян 6×3")
    L += [
        f"> Независимо от выбора игрок получает **18 крестьян** сеткой 6×3 "
        f"вокруг стартовой точки {csp_cite}.",
        "",
    ]

    L += _section(
        "Монгольфьеры (`balloon`)",
        "balloon", settings,
        columns=[("Значение", "value"),
                 ("Русское название", "label_ru"), ("Английское название", "label_en")],
    )
    L += [
        "Монгольфьер — особый юнит, открывающий обзор на большой высоте.",
        "",
    ]

    L += _section(
        "Пушки, башни и стены (`cannons`)",
        "cannons", settings,
        columns=[("Значение", "value"),
                 ("Русское название", "label_ru"), ("Английское название", "label_en")],
    )
    L += [
        "Опция «Дорогие пушки» поднимает цены пушек через апгрейд — точные "
        "множители читать в `country.script` (раздел артиллерийских апгрейдов).",
        "",
    ]

    L += _section(
        "Время мира (`peacetime`)",
        "peacetime", settings,
        columns=[("Значение", "value"), ("Минут (игр.)", "minutes_g"),
                 ("g-секунд", "gsec"),
                 ("Русское название", "label_ru"), ("Английское название", "label_en")],
    )
    L += [
        "Минуты — **игровые**. На скорости «Быстро» (×1,4) одна "
        "игровая минута = 60 / 1.4 ≈ 42.9 реальных секунд: 10-минутный мир "
        "длится примерно 7 реальных минут.",
        "",
        "Подробности механики (как движок блокирует поиск врагов, ничейные "
        "ячейки, переход от мира к войне) — в "
        "[`recon/world/map/game_settings.md`](../../recon/world/map/game_settings.md#peacetime--как-устроен-мир).",
        "",
    ]

    L += _section(
        "Переход в XVIII век (`century18`)",
        "century18", settings,
        columns=[("Значение", "value"),
                 ("Русское название", "label_ru"), ("Английское название", "label_en")],
    )
    L += [
        "Для Украины, Турции и Алжира вариант «Сразу» ничего не меняет: "
        "эти нации не могут перейти в XVIII век.",
        "",
    ]

    L += _section(
        "Правила захвата (`capture`)",
        "capture", settings,
        columns=[("Значение", "value"),
                 ("Русское название", "label_ru"), ("Английское название", "label_en")],
    )
    L += [
        "Геометрия захвата (радиусы, кто захватывается, кто нет) — в "
        "[`recon/world/economy/capture_mechanics.md`](../../recon/world/economy/capture_mechanics.md).",
        "",
    ]

    L += _section(
        "Рынок и дипломатический центр (`marketdip`)",
        "marketdip", settings,
        columns=[("Значение", "value"),
                 ("Русское название", "label_ru"), ("Английское название", "label_en")],
    )
    L += [
        "Вариант «Дорогие наёмники» утраивает цену найма. Подробности — в "
        "[`recon/systems/mercenaries_diplomacy.md`](../../recon/systems/mercenaries_diplomacy.md).",
        "",
    ]

    L += _section(
        "Расположение союзников (`teams`)",
        "teams", settings,
        columns=[("Значение", "value"),
                 ("Русское название", "label_ru"), ("Английское название", "label_en")],
    )
    L += [
        "При `teams = 1` команда стартует в соседних позициях, а не "
        "разбросанной по карте.",
        "",
    ]

    L += _section(
        "Лимит населения (`limit`)",
        "limit", settings,
        columns=[("Значение", "value"), ("Юнитов", "units"),
                 ("Русское название", "label_ru"), ("Английское название", "label_en")],
    )
    L += [
        "Это общий потолок поверх мест населения, которые дают городские центры, "
        "казармы и дома. Потолок никогда не превышается, даже если здания "
        "позволяет больше.",
        "",
    ]

    L += _section(
        "Скорость партии (`gamespeed`)",
        "gamespeed", settings,
        columns=[("Значение", "value"), ("Тиков/реальная секунда", "ticks_per_sec"),
                 ("Множитель к норме", "factor"),
                 ("Русское название", "label_ru"), ("Английское название", "label_en")],
    )
    L += [
        "Одна игровая секунда всегда содержит 32 кадра симуляции; меняется "
        "только её длительность в реальном времени.",
        "",
    ]

    L += _section(
        "Помощник (`adviserassistant`)",
        "adviserassistant", settings,
        columns=[("Значение", "value"),
                 ("Русское название", "label_ru"), ("Английское название", "label_en")],
    )
    L += [
        "Контекстные подсказки в углу экрана. Не влияет на симуляцию — только UI.",
        "",
    ]

    # ─── difficulty ────────────────────────────────────────────────────────
    L += ["## Сложность компьютера", ""]
    L += _section(
        "Сложность (`difficulty`)",
        "difficulty", settings,
        columns=[("Значение", "value"), ("Множитель скорости", "koef"),
                 ("Русское название", "label_ru"), ("Английское название", "label_en")],
    )
    L += [
        "Сложность меняет скорость строительства и найма компьютерного игрока. "
        "Дополнительных стартовых ресурсов он не получает. Поведение компьютера разобрано в "
        "[`recon/systems/ai_behavior.md`](../../recon/systems/ai_behavior.md).",
        "",
    ]

    # ─── defaults ──────────────────────────────────────────────────────────
    defaults = settings.get("defaults") or {}
    if False and defaults:
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
