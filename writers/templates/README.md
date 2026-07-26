# Templates — статичная проза writer'ов

[English](README.en.md) · **Русский**

Здесь живут все статичные текстовые блоки, которые писатели в `writers/` склеивают с computed-таблицами (генерируемыми из `data.json`). Идея: Python отвечает только за сборку и расчёты, прозу правят прямо в `.md`.

## Как использовать

В `writers/write_md_tree.py` есть helper `render_template(name, **subs)`:

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
├── output_readme.md           ← для docs/README.md (каталог артефактов)
│
└── reference/                 ← все блоки для docs/reference/*
    ├── readme/                ← главный README справочника
    │   └── glossary.md        ← глоссарий игровых тегов (sid, eff, bnohungry, …)
    │
    ├── 01_economy/            ← блоки для 01_economy/README.md
    │   ├── recon_refs.md      ← блок «Глубокие исследования по этой главе»
    │   ├── summary.md         ← Резюме
    │   ├── extraction_formula.md
    │   ├── mines_intro.md     ← интро + заголовок таблицы прокачки
    │   ├── fields_intro.md    ← заголовок секции «Поле»
    │   ├── fishing.md         ← Корабли — fishing
    │   └── famine_rebellion.md ← Famine + Rebellion
    │
    ├── 02_combat/
    │   └── main.md            ← вступление главы + типы оружия + ссылки на recon
    │                             (бóльшая часть прозы вынесена в docs/recon/world/combat/)
    │
    ├── 03_buildings/
    │   ├── legend.md          ← расшифровка колонок таблиц зданий
    │   ├── era_progression.md ← переход эпох (ссылка на recon)
    │   ├── lifecycle.md       ← lifecycle: postroika / repair / destruction (ссылка на recon)
    │   └── tow_combat.md      ← пушки на стенах: numeric-параметры башни (ссылка на recon)
    │
    ├── 04_units/
    │   └── legend.md          ← расшифровка колонок таблиц юнитов
    │
    ├── 05_upgrades/
    │   ├── legend.md          ← структура sid + расшифровка колонок таблиц апгрейдов
    │   └── order_math.md      ← вступление + ссылка на recon (упрощённая версия)
    │
    ├── 06_market/
    │   ├── intro.md           ← заголовок + TL;DR
    │   ├── mechanics.md       ← глобальные курсы, формулы пересчёта
    │   └── strategy.md        ← практические выводы + источники
    │
    ├── 07_naval/
    │   └── main.md            ← вступление главы по флоту (числа — auto-gen из data.json)
    │
    ├── compare/
    │   └── readme.md          ← compare/README.md (индекс side-by-side таблиц)
    │
    └── nations/
        └── readme_intro.md    ← заголовок nations/README.md
```

## Когда что добавлять / править

- **Любой длинный статичный кусок прозы (> ~5 строк), который сейчас живёт в Python через `A("…")` / `A(f"…")`** — кандидат на вынос. Особенно если он не зависит от `data` (значений из `data.json`).
- **Если кусок зависит от вычисленных значений** — оставь в Python и не выноси, либо используй `{var}` плейсхолдеры в шаблоне и передай через `render_template(name, var=...)`.
- **Имена файлов** — в нижнем регистре, словами через `_`. Префикс по главе там, где это полезно (`section_5b_*` для монолита).
- **Каждая `.md` папка соответствует одной выходной главе или странице.** Если блок относится к нескольким — клади в общее место (например, `reference/readme/`).

## Что генерируется чем

| Output | Writer | Шаблоны |
|---|---|---|
| `docs/README.md` | `write_md_tree.py:write_top_inventory` | `output_readme.md` |
| `docs/reference/README.md` | `write_md_tree.py:write_readme` | `reference/readme/glossary.md` |
| `docs/reference/01_economy/README.md` | `write_md_tree.py:write_economy` | `reference/01_economy/*.md` |
| `docs/reference/02_combat/README.md` | `write_md_tree.py:write_combat` | `reference/02_combat/main.md` |
| `docs/reference/03_buildings/README.md` | `write_md_tree.py:write_buildings` | `reference/03_buildings/{legend,era_progression,lifecycle,tow_combat}.md` |
| `docs/reference/04_units/README.md` | `write_md_tree.py:write_units` | `reference/04_units/legend.md` |
| `docs/reference/05_upgrades/README.md` | `write_md_tree.py:write_upgrades` | `reference/05_upgrades/{legend,order_math}.md` |
| `docs/reference/06_market/README.md` | `write_md_tree.py:write_market` | `reference/06_market/{intro,mechanics,strategy}.md` |
| `docs/reference/07_naval/README.md` | `write_md_tree.py:write_naval` | `reference/07_naval/main.md` |
| `docs/reference/nations/README.md` | `write_md_tree.py:write_nations` | `reference/nations/readme_intro.md` |
| `docs/reference/compare/README.md` | `write_md_tree.py:write_compare` | `reference/compare/readme.md` |
