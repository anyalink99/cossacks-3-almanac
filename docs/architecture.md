# Архитектура проекта

Как данные двигаются от файлов игры до markdown-справочника. Полезно
прочитать перед тем как добавлять новый отчёт или править генератор.

## Поток данных

```
┌─────────────────────────────────────────────────────────────────┐
│ Cossacks 3 install (read-only):                                 │
│   data/scripts/*.script, *.global, *.inc       (Pascal-подобный)│
│   data/locale/{ru,en,...}/*.txt                (cp1251)         │
│   data/animations/aaf/*.aaf                    (анимации)       │
│   data/pattern/*.pattern                       (паттерны карт)  │
│   data/game/var/*.cfg                          (формации, …)    │
└─────────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│ parser/ — извлечение из файлов игры в JSON                      │
│                                                                 │
│   parser/build_data.py            (оркестратор)                 │
│     ├── parse_units.py            → unit / building / weapon    │
│     ├── parse_country.py          → upgrade / officer / squad   │
│     ├── parse_locale.py           → name_en / name_ru           │
│     ├── extract_constants.py      → gc_*-константы              │
│     └── simulate_upgrades.py      → 4429 апгрейдов с prereqs    │
│                                                                 │
│   parser/build_canonical_terms.py → canonical_terms.json        │
│   parser/parse_animations.py      → animations.json             │
│   parser/parse_pattern_inventory  → pattern_*.json              │
│   parser/parse_replay_aggregates  → replay_ground_truth.json    │
│   parser/parse_generator_cfg.py   → pattern_types.json          │
└─────────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│ docs/data.json + docs/derived/*.json                            │
│                                                                 │
│   data.json              мастер-структура (~4.7 МБ):            │
│     - 21 нация, 414 зданий, 714 юнитов, 4429 апгрейдов          │
│   derived/*.json         специализированные датасеты            │
│     (см. docs/derived/README.md)                                │
└─────────────────────────────────────────────────────────────────┘
                            │
            ┌───────────────┴───────────────┐
            ▼                               ▼
┌──────────────────────────┐   ┌──────────────────────────────────┐
│ writers/ — рендер MD     │   │ compute/ — производные расчёты   │
│                          │   │                                   │
│ write_md_tree.py         │   │ Бой:                              │
│   → docs/reference/      │   │   compute_combat_stats           │
│      01_economy.md       │   │   compute_counter_matrix          │
│      02_combat.md        │   │   compute_attack_rates            │
│      …                   │   │   compute_vision                  │
│      nations/×21         │   │ Экономика:                        │
│      compare/×16         │   │   compute_scaling                 │
│   + templates/*.md       │   │   compute_efficiency_upgrades     │
│   + docs/data.json       │   │   compute_construction_times      │
│                          │   │   compute_builder_slots           │
│ diff_snapshots.py        │   │ Тех-дерево:                       │
│   → diff.md              │   │   build_tech_tree                 │
│   между двумя data.json  │   │     → tech_tree.json + 2 отчёта  │
│                          │   │ Карта:                            │
│                          │   │   compute_game_settings           │
│                          │   │     → game_settings.json + md     │
│                          │   │   compute_map_resources           │
│                          │   │   extract_starting_layout         │
│                          │   │   validate_map_predictions        │
│                          │   │ Нации:                            │
│                          │   │   compute_nations_overview        │
└──────────────────────────┘   └──────────────────────────────────┘
            │                               │
            └───────────────┬───────────────┘
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│ docs/reference/ + docs/reports/ + docs/known_issues.md           │
│ (markdown для людей; рендерится прямо на GitHub)                │
└─────────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│ simulator/ — runtime симулятор экономики                        │
│                                                                 │
│   simulate_economy.py reads docs/data.json + tech_tree.json +   │
│   build_orders/<name>.json → docs/simulations/sim_<name>.{csv,md}│
└─────────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│ editor/ — браузерный редактор билдов                            │
│                                                                 │
│   index.html + js/* загружают docs/{data, derived/*}.json,      │
│   запускают simulator через Pyodide                              │
└─────────────────────────────────────────────────────────────────┘
```

## Принципы

1. **Один источник правды на каждом уровне:**
   - Игровые файлы — read-only.
   - `docs/data.json` — единственный «общий» датасет, его читают все генераторы
     (writers + compute + simulator + editor).
   - `docs/derived/*.json` — узкоспециализированные срезы для конкретных
     потребителей.
2. **Идемпотентность.** `python scripts/regen.py all` перегенерирует всё с
   нуля, без побочных эффектов. После патча игры — один запуск.
3. **Никаких ручных правок в auto-generated md.** Всё, что генерится,
   перезаписывается. Если нужно поменять формулировку — правь шаблон в
   `writers/templates/` либо текст в `compute/<скрипт>.py`. Списки исключений:
   - `docs/recon/*.md` — handwritten reverse-engineering, правится руками.
   - `docs/known_issues*.md` — handwritten списки.
   - `docs/architecture.md` (этот файл) — handwritten.
   - `docs/derived/README.md` — handwritten.
   - `docs/README.md` — handwritten + блок-копия из шаблона.
4. **Канонические русские термины — из локали игры.** Никогда не выдумывай
   перевод. Если в игре написано «Высокогорье» — пиши «Высокогорье». Канон
   живёт в `docs/derived/canonical_terms.json` (генерится из
   `data/locale/{ru,en}/`); writers и compute импортируют его через
   `parser/config.py` (`NATION_NAMES_RU`, `USAGE_RU`, `BUILDING_NAMES_RU`,
   `WEAPON_KIND_RU`, `decode_usage(s, lang='ru')`, `nation_label(sid)`).
5. **Sanity checks.** `parser/build_data.py` гоняет 112 авто-проверок на
   каждом запуске. Любая регрессия после патча сразу видна.

## Где что лежит

### Код

| Папка | Назначение |
|---|---|
| `parser/` | Чтение файлов игры → JSON (`data.json`, `derived/*.json`). |
| `compute/` | Производные расчёты на основе JSON → markdown-отчёты в `docs/reports/`. |
| `writers/` | Рендер канонической справки `docs/reference/` + diff между снапшотами. |
| `simulator/` | Runtime симулятор экономики (build orders → таймлайны). |
| `editor/` | Браузерный редактор билдов (HTML + JS + Pyodide). |
| `mods/` | Игровые моды (каждый — `build.py` патчер + сборка). |
| `scripts/` | Pipeline-runner (`regen.py`). |

### Документация

| Папка | Что внутри | Источник |
|---|---|---|
| `docs/reference/` | Каноническая справка: 7 глав, 21 нация, 16 сравнений. | Auto-gen (`writers/write_md_tree.py` + `templates/`). |
| `docs/reports/` | Производные расчёты по темам: combat / economy / tech / map / nations. | Auto-gen (`compute/*.py`). |
| `docs/recon/` | Глубокое RE механик движка (скриптов нет, всё руками). | **Handwritten.** |
| `docs/simulations/` | Таймлайны экономики по конкретным build order'ам. | Auto-gen (`simulator/simulate_economy.py`). |
| `docs/derived/` | Машинно-читаемые JSON для editor / тулзы. | Auto-gen (`parser/*.py`, `compute/compute_game_settings.py`, `compute/build_tech_tree.py`). |
| `docs/known_issues*.md` | Парсерные пробелы, расхождения, открытые вопросы. | **Handwritten.** Архив — `known_issues_archive.md`. |
| `docs/architecture.md` | Этот файл. | **Handwritten.** |

## Расширение pipeline

### Добавить новый отчёт

1. Создай `compute/compute_<topic>.py` по образцу соседних (`compute_*.py`).
2. Добавь его в `scripts/regen.py` в подходящий target (`reports-*`).
3. Если отчёт связан с одним из 5 готовых разделов
   (`combat / economy / tech / map / nations`) — пиши в
   `docs/reports/<раздел>/<имя>.md`. Если новый раздел — заведи папку и
   добавь в `docs/reports/README.md`.
4. Если отчёт нужно показать в [`docs/README.md`](README.md), внеси его в
   список (этот файл не auto-gen).

### Добавить новый JSON-датасет

1. Создай парсер в `parser/parse_<X>.py` или extractor в
   `compute/compute_<X>.py` (если зависит только от `data.json`).
2. Эмить в `docs/derived/<имя>.json`.
3. Опиши датасет в `docs/derived/README.md`.
4. Добавь в `scripts/regen.py` (target `derived` или соответствующий
   `reports-*`).

### Добавить нацию (теоретически)

Не предусмотрено: список наций зашит в локали игры (`data/locale/*/units.txt`)
и в `country.script`. После патча с новой нацией нужно расширить
`PLAYABLE_NATIONS` в `parser/config.py`, перепрогнать
`parser/build_canonical_terms.py` и `parser/build_data.py`.

## Регенерация — порядок зависимостей

```
parser/build_data.py            ← читает игру, эмитит data.json
parser/build_canonical_terms.py ← читает локаль, эмитит canonical_terms.json
parser/parse_animations.py      ← независим (читает .aaf)
parser/parse_generator_cfg.py   ← независим (читает .cfg)
parser/parse_pattern_inventory  ← после parse_generator_cfg
parser/parse_replay_aggregates  ← после parse_pattern_inventory

writers/write_md_tree.py        ← после data.json + canonical_terms.json
compute/compute_*.py            ← после data.json (+ derived/*.json для частных)
compute/compute_game_settings   ← независим (читает локаль напрямую)
compute/build_tech_tree.py      ← после data.json
compute/validate_map_predictions← после replay_ground_truth + compute_map_resources
simulator/simulate_economy.py   ← после tech_tree.json
```

Все зависимости разрешает `scripts/regen.py` через декларативный список
target'ов и алиасов. Запуск:

```bash
python scripts/regen.py all              # полный круг
python scripts/regen.py reference        # только writers/
python scripts/regen.py reports-combat   # только combat-отчёты
python scripts/regen.py help             # все targets
```

Аналогично через `make`: `make all`, `make reports`, `make sanity`, и т. д.
