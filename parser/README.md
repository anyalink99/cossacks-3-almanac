# `parser/` — извлечение данных из игры

[English](README.en.md) · **Русский**

Скрипты в этой папке делают **только парсинг**: читают `.script`/`.global` файлы Cossacks 3
и собирают единый JSON-снапшот в `data.json`. Все скрипты идемпотентны: после
игрового патча перезапускаешь pipeline — все артефакты обновляются.

Производные расчёты, writers и симулятор живут в соседних папках:
[`../compute/`](../compute/), [`../writers/`](../writers/), [`../simulator/`](../simulator/).

Внутри парсера:
- [`engine_recon/`](engine_recon/) — экстракторы из `cossacks.exe` (DWS native API,
  primitives, exe-strings); пишут в `../derived/` напрямую и питают [`../internals/`](../internals/).
- [`debug/`](debug/) — dev-скрипты для отладки шагов парсинга.

## Pipeline

```
              ┌───────────────────────────┐
              │  Game files (Steam)       │
              │  data/scripts/lib/*.script│
              │  data/scripts/dmscript.*  │
              │  data/locale/<lang>/*.txt │
              └──────────────┬────────────┘
                             │
                             ▼
                ┌─────────────────────────┐
                │  parser/build_data.py   │  ← extracts EVERYTHING
                │  (orchestrator)         │
                └────┬────────────────────┘
                     │
                     ▼
              ┌──────────────────┐
              │  data.json       │  ← single source of truth (~4.7 MB, top-level)
              └────┬─────────────┘
                   │
   ┌───────────────┼─────────────────────────┐
   ▼               ▼                         ▼
writers/        compute/                  simulator/
write_md_tree   compute_scaling           simulate_economy
                compute_map_resources
                compute_tech_tree
                compute_construction_times

  parser/engine_recon/ → ../derived/{dws_native_signatures, engine_primitives, exe_strings}.json
                       (питает internals/engine/*; не зависит от data.json)
```

## Файлы (`parser/`)

### Парсеры (вход: game files; выход: JSON-friendly dicts)

| Файл | Что делает |
|---|---|
| **`config.py`** | Пути, таблица 21 нации, маппинги (cluster→prefix, usage_short, upg_type, speed_table). `GAME_ROOT` берётся из env-переменной `COSSACKS3_PATH` (fallback — стандартный Steam-путь). |
| **`extract_constants.py`** | Парсит `dmscript.global` → `{gc_name: {raw, value}}`. ~1463 константы. |
| **`parse_locale.py`** | UTF-8 / CP1251 авто-детект; шаблоны `%nat%`/`%com%`/`%include%`. EN+RU. |
| **`parse_country.py`** | Recursive-descent Pascal-парсер. Извлекает per-nation roster (members, upgrades, fixed_produces) через симуляцию `if (aus)`/`case cid` для каждой из 21 нации. Инлайнит `_country_InitUnitsUpgrades`. |
| **`parse_units.py`** | Text-based balanced-block walker. Парсит `_unit_InitBase` — три case-блока (units / common buildings / per-nation buildings) с per-nation/per-cluster overrides. |
| **`simulate_upgrades.py`** | Symbolic Pascal executor для `_country_InitUnitsUpgrades` и `_country_Init`. Трекает `member`/`upgplace`, инлайнит `SetUpgStruct*` + `AddUpgradePack`, разворачивает `for i:=1 to 3 do` (mine upgrades). Эмитит ~3000 fully-resolved upgrade rows. |

### Инструменты replay'ев

| Файл | Что делает |
|---|---|
| **`parse_replay.py`** | Разбирает OSWMap13 header/footer, lobby settings, игроков и `PatternList`. В `--json` возвращает точные `n/x/y`-координаты размещённых паттернов и metadata карты из футера. |
| **`parse_replay_events.py`** | Декодирует entry/sub-package поток в JSON-таймлайн команд и state-sync событий. |
| **`parse_replay_aggregates.py`** | Строит агрегаты по каталогу replay'ев для эмпирической проверки формата. |
| **`replay_to_build_order.py`** | Преобразует декодированные события в последовательность строительства/производства. |

### Orchestrator (вход: парсеры; выход: единый dict)

| Файл | Что делает |
|---|---|
| **`build_data.py`** | Зовёт все парсеры, склеивает в единый `dict`, дописывает версионный stamp, market rates, officers, sanity_checks (112 авто-утверждений). Сохраняет в `data.json`. |

## Как запускать

### После патча игры (полная регенерация)

Все команды — из корня проекта:

```bash
python parser/build_data.py                   # → data.json (источник правды)
python writers/write_md_tree.py               # → docs/reference/ + docs/README.md
python compute/compute_scaling.py             # → docs/reports/economy/scaling_prices.md
python compute/compute_map_resources.py       # → docs/reports/map/map_resources.md
python parser/build_tech_graph.py             # → derived/tech_tree.json
python compute/compute_tech_tree.py           # → docs/reports/tech/tech_tree.md + production_rates.md
python compute/compute_construction_times.py  # → docs/reports/economy/construction_times.md
```

Удобнее — один runner: `python scripts/regen.py all` (полный круг ~4 мин)
или точечно `python scripts/regen.py reports-economy` / `reference` / `derived`.

Все writer/compute-скрипты читают только из `data.json` (кроме `compute/compute_map_resources.py`,
который ходит ещё в game files за map gen densities). Поэтому достаточно один раз обновить
data.json — потом writers выполняются за <30 сек суммарно.

### Diff между снапшотами

```bash
python parser/build_data.py                                       # текущий
cp data.json /tmp/data_old.json
# … patch the game …
python parser/build_data.py                                       # новый
python writers/diff_snapshots.py /tmp/data_old.json data.json
```

## Sanity checks

`build_data.py` выводит результат **112 автопроверок** в конце:
- 10 проверок на `gc_*` константы (time_to_frames=32, hits_needed_*, base portions)
- 5 проверок на количество (≥21 нации, ≥410 зданий, ≥700 юнитов, ≥4000 улучшений)
- 21 проверка building counts по каждой нации (≥15 зданий)
- 49 проверок наличия Town Hall + Barracks 17c у каждой нации
- 4 проверки mine upgrade chain (5+5+8+10+12+15+40 = 95 workers, total cost 104550 food + 80950 gold)
- 15 проверок отдельных юнитов (уникальность Стрельца, Янычара и Витязя; у Стрельца 85 здоровья, 12 урона, дальность 13,13 клетки и мушкет)
- 4 проверки trained_in mappings
- 3 проверки market default rates
- 1 проверка pixels_to_tile=53.33

После патча игры регрессии в данных будут видны через `FAIL` в этом списке.

## Архитектура парсеров

### Подход

Pascal-скрипты игры — **исполняемый код**, не данные. Чтобы извлечь параметры,
мы делаем **символьное исполнение**: парсим в AST, оцениваем условия (`if (aus)`,
`case cid of _aus`) для каждой нации отдельно, инлайним вспомогательные процедуры
(`SetUpgStructFoodGold`, `AddUpgradePack`).

### Ключевые трюки

1. **Pre-substitution** (`_presubstitute`): csid → 'aus', commonName → 'eur',
   blacksmith → 'ausbla', tmptype → ctypeProtection. Делается per-nation **до** парсинга.

2. **Class/record/object/type keyword recognition**: без них `extract_proc_body`
   обрывается на `type T = class … end;` и возвращает огрызок процедуры.

3. **Pascal-to-Python operator translation**: `<>` → `!=`, `=` → `==`. Без этого
   `if (member<>'')` всегда True (eval падает, fallback на True), и эмитятся
   ложные апгрейды.

4. **For-loop unrolling**: `for i := 1 to 3 do … case i of 1:'gol'; 2:'iro'; 3:'coa'`
   разворачивается в 3 итерации. Используется для mine upgrades.

5. **Last-write-wins dedup**: соответствует поведению игры (`_country_AddUpgrade`
   с тем же sid перезаписывает предыдущий).

## Каталоги выходов

- [`../docs/README.md`](../docs/README.md) — индекс справочника для игрока
  (reference, recon, reports).
- [`../derived/README.md`](../derived/README.md) — каталог JSON-датасетов
  (включая engine-RE дампы из `parser/engine_recon/`).
- [`../internals/README.md`](../internals/README.md) — техническая
  документация движка / скриптов / `data/`-каталога.
