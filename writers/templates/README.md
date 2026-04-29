# Templates — статичная проза writer'ов

Здесь живут все статичные текстовые блоки, которые писатели в `writers/` склеивают с computed-таблицами (генерируемыми из `output/data.json`). Идея: Python отвечает только за сборку и расчёты, прозу правят прямо в `.md`.

## Как использовать

В `writers/write_md_tree.py` и `writers/write_md.py` есть helper `render_template(name, **subs)`:

```python
out.extend(render_template("reference/01_economy/famine_rebellion.md"))
# или с подстановкой переменных:
out.extend(render_template("foo.md", time_to_frames=32, ...))
```

Шаблоны загружаются по относительному пути от `writers/templates/`. Если в шаблоне нужны вычисленные значения — используй `{var}` плейсхолдеры; они заполняются через `str.format(**subs)`. Если плейсхолдеры не нужны — `subs` можно опустить.

## Структура

```
templates/
├── README.md                  ← этот файл
├── output_readme.md           ← для output/README.md (каталог артефактов)
│
├── reference/                 ← все блоки для output/reference/*
│   ├── readme/                ← главный README справочника
│   │   ├── glossary.md        ← глоссарий игровых тегов (sid, eff, bnohungry, …)
│   │   └── principles.md      ← четыре принципа справочника
│   │
│   ├── 01_economy/            ← блоки для 01_economy.md
│   │   ├── recon_refs.md      ← блок «Глубокие исследования по этой главе»
│   │   ├── summary.md         ← Резюме
│   │   ├── extraction_formula.md
│   │   ├── mines_intro.md     ← интро + расчёт + заголовок таблицы прокачки
│   │   ├── fields_intro.md    ← заголовок секции «Поле»
│   │   ├── fishing.md         ← Корабли — fishing
│   │   └── famine_rebellion.md ← Famine + Rebellion (~80 строк)
│   │
│   ├── 02_combat/
│   │   └── main.md            ← гигантский блок: TOC + формула урона + headshot +
│   │                              формации + AoE + high ground + score + standground +
│   │                              runaway + friendly fire + weapon switching +
│   │                              standtime + addradius + capture + healing + shield/3 +
│   │                              AI reaction + officers myth + «Чего нет в игре» +
│   │                              dispertion + uniqrnd + типы оружия (~510 строк)
│   │
│   ├── 03_buildings/
│   │   └── legend.md          ← расшифровка колонок таблиц зданий
│   │
│   ├── 04_units/
│   │   └── legend.md          ← расшифровка колонок таблиц юнитов
│   │
│   ├── 05_upgrades/
│   │   ├── legend.md          ← структура sid + расшифровка колонок таблиц апгрейдов
│   │   └── order_math.md      ← как _player_ApplyUpgrade аккумулирует апгрейды (порядок безразличен)
│   │
│   ├── 06_market/
│   │   ├── intro.md           ← заголовок + TL;DR
│   │   ├── mechanics.md       ← глобальные курсы, формулы пересчёта
│   │   └── strategy.md        ← практические выводы + источники
│   │
│   ├── compare/
│   │   └── readme.md          ← compare/README.md (индекс side-by-side таблиц)
│   │
│   └── nations/
│       └── readme_intro.md    ← заголовок nations/README.md
│
└── legacy/                    ← блоки для устаревшего output/cossacks3_reference.md
    ├── header_banner.md       ← deprecation-баннер + общий TOC монолита
    ├── section_4_buildings_intro.md
    ├── section_4_2_common_intro.md
    ├── section_5_units_intro.md
    ├── section_5b_ships.md
    ├── section_5b_ships_notes.md
    ├── section_5c_mines_intro.md
    ├── section_5c_mines_outro.md
    ├── section_6a_combat.md
    ├── section_6b_speed_intro.md
    ├── section_6b_speed_outro.md
    ├── section_6c_officers_intro.md
    ├── section_6d_market.md
    ├── section_6d_market_examples.md
    ├── section_combat_costs_intro.md
    ├── section_7_upgrades_intro.md
    ├── section_8_gaps_outro.md
    └── footer.md
```

## Когда что добавлять / править

- **Любой длинный статичный кусок прозы (> ~5 строк), который сейчас живёт в Python через `A("…")` / `A(f"…")`** — кандидат на вынос. Особенно если он не зависит от `data` (значений из `data.json`).
- **Если кусок зависит от вычисленных значений** — оставь в Python и не выноси, либо используй `{var}` плейсхолдеры в шаблоне и передай через `render_template(name, var=...)`.
- **Имена файлов** — в нижнем регистре, словами через `_`. Префикс по главе там, где это полезно (`section_5b_*` для монолита).
- **Каждая `.md` папка соответствует одной выходной главе или странице.** Если блок относится к нескольким — клади в общее место (например, `reference/readme/`).

## Что генерируется чем

| Output | Writer | Шаблоны |
|---|---|---|
| `output/README.md` | `write_md_tree.py:write_top_inventory` | `output_readme.md` |
| `output/reference/README.md` | `write_md_tree.py:write_readme` | `reference/readme/glossary.md`, `reference/readme/principles.md` |
| `output/reference/01_economy.md` | `write_md_tree.py:write_economy` | `reference/01_economy/*.md` |
| `output/reference/02_combat.md` | `write_md_tree.py:write_combat` | `reference/02_combat/main.md` |
| `output/reference/03_buildings.md` | `write_md_tree.py:write_buildings` | `reference/03_buildings/legend.md` |
| `output/reference/04_units.md` | `write_md_tree.py:write_units` | `reference/04_units/legend.md` |
| `output/reference/05_upgrades.md` | `write_md_tree.py:write_upgrades` | `reference/05_upgrades/{legend,order_math}.md` |
| `output/reference/06_market.md` | `write_md_tree.py:write_market` | `reference/06_market/{intro,mechanics,strategy}.md` |
| `output/reference/nations/README.md` | `write_md_tree.py:write_nations` | `reference/nations/readme_intro.md` |
| `output/reference/compare/README.md` | `write_md_tree.py:write_compare` | `reference/compare/readme.md` |
| `output/cossacks3_reference.md` (legacy) | `write_md.py:main` | `legacy/*.md` |
