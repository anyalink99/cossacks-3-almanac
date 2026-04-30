# Машинно-читаемые JSON-датасеты

Здесь — все JSON-файлы для инструментов: редактора билдов, симулятора,
внешних анализаторов. Все генерируются. **Не редактировать руками** — будут
перезаписаны при следующей регенерации.

## Каталог

| Файл | Что внутри | Откуда |
|---|---|---|
| [`canonical_terms.json`](canonical_terms.json) | Каноничные русские названия из локали игры: 21 нация, 22 здания, 7 типов оружия, 5 уровней сложности, 79 настроек лобби, 9 типов тренировок офицеров, 75 апгрейдов, 148 юнитов, 6 ресурсов. **Единый источник правды** для всех writer'ов и compute-скриптов. | [`parser/build_canonical_terms.py`](../../parser/build_canonical_terms.py) |
| [`game_settings.json`](game_settings.json) | Все опции лобби (`mapsize`, `terraintype`, `relieftype`, `peacetime`, `gamespeed` и т. д.) — 95 значений в 18 категориях, с английскими и русскими лейблами + значениями по умолчанию из `initmap.inc`. Используется браузерным редактором для построения dropdown'ов. | [`compute/compute_game_settings.py`](../../compute/compute_game_settings.py) |
| [`tech_tree.json`](tech_tree.json) | Граф зависимостей зданий, юнитов и апгрейдов: для каждого `sid` — список prereq'ов с типами (`[B]` здание, `[U]` юнит, `[T]` апгрейд) + базовая цена и время. Используется симулятором экономики и редактором. | [`compute/build_tech_tree.py`](../../compute/build_tech_tree.py) |
| [`builder_slots.json`](builder_slots.json) | Сколько крестьян одновременно может строить каждое здание. Считается обходом периметра collision-маски с шагом `gc_BuilderDist = 1.0`. Используется в [`reports/economy/builder_slots.md`](../reports/economy/builder_slots.md) и в редакторе. | [`compute/compute_builder_slots.py`](../../compute/compute_builder_slots.py) |
| [`animations.json`](animations.json) | База анимационных кадров для каждого юнита: `{sid: {anim_name: [start_frame, end_frame]}, ...}` — извлекается из `<game>/data/animations/aaf/*.aaf`. Длина одного кадра = 1 / 32 игровой секунды. Используется для расчёта реальной скорости melee-атак. | [`parser/parse_animations.py`](../../parser/parse_animations.py) |
| [`pattern_types.json`](pattern_types.json) | Карта pattern-типов из `data/game/var/generator.cfg`: какие конкретные `.pattern` файлы относятся к каждой категории (`forests_pine_big`, `stones`, `mng/mni/mnc` и т. д.) с весами `Freq`. | [`parser/parse_generator_cfg.py`](../../parser/parse_generator_cfg.py) |
| [`pattern_inventory.json`](pattern_inventory.json) | Per-pattern статистика: для каждого `.pattern` файла — размеры, число mask-клеток, число объектов. | [`parser/parse_pattern_inventory.py`](../../parser/parse_pattern_inventory.py) |
| [`pattern_type_stats.json`](pattern_type_stats.json) | Per-type агрегаты: median / min / max mask-клеток по типу паттерна (для калибровки модели подсчёта леса/камней). | [`parser/parse_pattern_inventory.py`](../../parser/parse_pattern_inventory.py) |
| [`replay_ground_truth.json`](replay_ground_truth.json) | Эмпирический ground truth из реплеев: для каждого `.rep`/`.map` — настройки партии + точные кластеры паттернов, размещённые движком. Используется для калибровки [`compute_map_resources`](../../compute/compute_map_resources.py) против реальности. | [`parser/parse_replay_aggregates.py`](../../parser/parse_replay_aggregates.py) |

## Как использовать

### Из редактора (browser)

```javascript
fetch("../docs/derived/canonical_terms.json").then(r => r.json())
fetch("../docs/derived/game_settings.json").then(r => r.json())
fetch("../docs/derived/tech_tree.json").then(r => r.json())
fetch("../docs/derived/builder_slots.json").then(r => r.json())
```

См. [`editor/js/data_loader.js`](../../editor/js/data_loader.js).

### Из Python (writer / compute / simulator)

```python
import json
from pathlib import Path
DERIVED = Path(__file__).resolve().parent.parent / "docs" / "derived"
canon = json.loads((DERIVED / "canonical_terms.json").read_text(encoding="utf-8"))
```

Лучше — через готовые утилиты в [`parser/config.py`](../../parser/config.py)
(`NATION_NAMES_RU`, `USAGE_RU`, `BUILDING_NAMES_RU`, `WEAPON_KIND_RU`,
`nation_ru()`, `nation_label()`, `usage_ru()`, `decode_upg_type(s, lang='ru')`).

### Регенерация

После патча игры:

```bash
python scripts/regen.py derived          # все JSON в этой папке
# или поодиночке:
python parser/build_canonical_terms.py
python parser/parse_animations.py
python parser/parse_generator_cfg.py
python parser/parse_pattern_inventory.py
python parser/parse_replay_aggregates.py
python compute/compute_game_settings.py
python compute/build_tech_tree.py
python compute/compute_builder_slots.py
```

Полный pipeline — `python scripts/regen.py all` (чуть больше 4 минут).

## Где не лежит

- **Сырые данные** — в [`../data.json`](../data.json) (мастер-структура,
  ~4.7 МБ; читают все генераторы).
- **Готовая для людей справка** — в [`../reference/`](../reference/),
  [`../reports/`](../reports/), [`../recon/`](../recon/).
- **Схема архитектуры** — в [`../architecture.md`](../architecture.md).
