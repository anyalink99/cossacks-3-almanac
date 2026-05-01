# Структура `data/` в Cossacks 3

Что лежит в каждой подпапке игрового каталога (`Steam/steamapps/
common/Cossacks 3/data/`), какой там формат и кто это парсит.

## Сводка

| Папка | Файлов | Размер | Что внутри |
|---|---:|---:|---|
| `actors/` | 5 220 | 894 МиБ | 3D-модели юнитов и зданий (.actor, .tlf, .lib) |
| `animations/` | 282 | 0.5 МиБ | Анимационные треки (.aaf), libraries (.lib) |
| `brushes/` | 21 | 3.6 МиБ | Текстурные кисти для редактора карт |
| `cameras/` | 4 | 7 КиБ | Конфигурация камер |
| `cursors/` | 23 | 100 КиБ | Курсоры (.cur, .bmp) |
| `env/` | 92 | 9 МиБ | Environment (sky, fog, lighting presets) |
| `game/` | 11 | 1.9 МиБ | Геймплейные конфиги (.cfg) |
| `gen/` | 4 571 | 164 МиБ | **Генератор карт**: pattern masks, terrainmasks, region templates |
| `gui/` | 139 | 2.4 МиБ | UI-элементы (.aix, .cfg, .inc) |
| `hud/` | 180 | 153 МиБ | HUD-текстуры (значки, кнопки) |
| `images/` | 22 | 6.3 МиБ | Loading-экраны и пр. |
| `locale/` | 2 187 | 20 МиБ | Локализация на 7+ языков |
| `maps/` | 68 | 1.7 ГиБ | Готовые карты (`.map`, `.aix`) |
| `materials/` | 866 | 2.9 ГиБ | Материалы и текстуры (`.mat`, `.dds`) |
| `objects/` | 1 290 | 3.4 МиБ | Per-юнит/здание `.parser`-конфиги (см. ниже) |
| `pattern/` | 711 | 60 МиБ | **Pattern-файлы** для размещения объектов на карте (бинарные .pattern) |
| `pfx/` | 26 | 47 МиБ | Particles (огонь, дым, пыль) |
| `posteffects/` | 3 | 5 КиБ | Постпроцесс-шейдеры |
| `projects/` | 1 | 0.3 КиБ | (служебный) |
| `resources/` | 4 | 46 КиБ | `resource.lib` (локаль), `resource.dat` |
| `scripts/` | 222 | 4.3 МиБ | **DWS-скрипты + .parser-конфиги** (см. [`../scripts/structure.md`](../scripts/structure.md)) |
| `shaders/` | 109 | 0.3 МиБ | GLSL-шейдеры (.vert, .frag) |
| `sounds/` | 330 | 282 МиБ | OGG-звуки + конфиги |
| `terrain/` | 607 | 685 МиБ | Тайлы тёрейна (текстуры по сезонам) |
| `video/` | 1 | 0.1 КиБ | (только .lib-индекс — видео в DLC) |
| `water/` | 11 | 5 МиБ | Water shader assets |

**Всего:** ~7.7 ГиБ. Данные = ~94% размера игры.

## Что нас интересует для парсинга

Из всех 26 папок реально парсятся:

- `scripts/` — главный источник правды gameplay. См.
  [`../scripts/structure.md`](../scripts/structure.md).
- `objects/` — per-сущность `.parser`-конфиги (пример: каждый юнит
  имеет .parser-файл с настройками behaviour'ов и анимаций).
- `animations/` — `.aaf`-треки для frame-точного timing'а атак.
- `pattern/` — бинарные `.pattern` для генерации карт.
- `gen/` — terrainmasks для seed-системы карт (`gen/terrainmasks/
  land/4pl_*.tga` — ~230 базовых масок для 4-player Land).
- `locale/` — текстовые `.lng` и `.loc` файлы для русских названий
  юнитов/апгрейдов.
- `maps/` — готовые `.map` для Historical Battles (бинарные).

## scripts/

Самая главная папка для нас. Полностью разобрана в
[`../scripts/structure.md`](../scripts/structure.md). Ключевые
файлы:

- `dmscript.global` — глобальные `gc_*`-константы (.parser-формат).
- `dmscript.source` — начальное состояние глобальных vars.
- `lib/*.script` — 29 DWS-библиотек (unit, country, ai, gui, ...).
- `units/<sid>/*.parser` — per-unit конфиги.
- `gui/*.aix` — UI-описания.

## objects/

Содержит `.parser`-конфиги объектов (1 290 файлов). Структура:

```
objects/
├── *.objects       Корневые конфиги классов
├── *.lib           Индексы
├── *.prop          Свойства
└── ...
```

Каждый класс GameObject в C3 имеет `.objects`-конфиг со списком
behaviour'ов, анимаций, материалов. Парсит движок через
`ParserLoadFromFile` (нативная функция, есть в RTTI).

## animations/

Анимационные треки. Файлы:

- `<sid>.aaf` — Actor Animation File. Содержит timing'и каждого
  кадра: melee swing point, projectile-spawn frame, footstep'ы и
  т. п.
- `*.acl` — animation cycles libraries.
- `*.library` — индекс.

Парсится в [`../../parser/parse_animations.py`](../../parser/parse_animations.py)
→ [`../../derived/animations.json`](../../derived/animations.json).
1 382 anim-трека из 194 .aaf файлов.

## pattern/

Бинарные кисти для размещения групп объектов на карте. 711 файлов.
Используются генератором карт.

Полностью разобраны в
[`../../docs/recon/world/map_generation_pipeline.md`](../../docs/recon/world/map/map_generation_pipeline.md)
и
[`../../parser/parse_patterns.py`](../../parser/parse_patterns.py)
→ [`../../derived/pattern_inventory.json`](../../derived/pattern_inventory.json).

## gen/

Pipeline генерации карт. Содержит:

- `gen/terrainmasks/<terrain>/<count>pl_*.tga` — базовые маски для
  каждого типа terrain × player count. Например, для Land 4 игрока
  — ~230 шаблонов в `gen/terrainmasks/land/4pl_*.tga`.
- `gen/*.cfg` — generator.cfg c PatternList → 60 типов pattern'ов.
- `gen/*.bmp` — служебные битмапы.

Парсится в `parser/parse_generator_cfg.py`.

## locale/

Локализация. На каждый язык — папка с `.lng`/`.loc`-файлами:

```
locale/
├── english/
│   ├── units.txt        Названия юнитов и зданий
│   ├── upgrades.txt     Названия апгрейдов
│   └── ...
├── russian/
└── ...
```

Парсится в `parser/parse_locale.py` → `derived/canonical_terms.json`.
В `data.json` каждое имя сидует в поле `name_ru` (русское).

## maps/

Готовые карты (Historical Battles, кампанийные миссии). 68 файлов,
1.7 ГиБ. Бинарный формат `.map` — пока **не разобран**. Планов на
парсинг тоже нет (карты для скирмиша генерируются процедурно).

## actors/

3D-модели юнитов и зданий. 5 220 файлов, ~900 МиБ. Бинарные
форматы:

- `.actor` — модель + skeleton + materials.
- `.tlf` — Top-Level Frame (отдельная анимированная часть).
- `.osm`/`.oss` — внутренние индексы.

Не парсится — мы не работаем с 3D-данными.

## materials/

Материалы (шейдеры + текстуры). 2.9 ГиБ. `.mat`-файлы конфигурируют
binding текстур к шейдерам. `.dds` — собственно текстуры.

## sounds/

Звуковые эффекты. OGG-формат. 330 файлов, 282 МиБ.

## DLC

Помимо `data/`, в корне игры есть:

```
dlcs/
├── summer/        Летняя карта (Map data only)
└── winter/        Зимняя карта
```

DLC **не содержат** правил-оверрайдов — только дополнительные
карты. Все юниты/нации/апгрейды — в основном `data/`.

## Что не парсится (и не планируется)

- 3D-модели (`actors/`, `materials/`).
- Sprite-анимации в .actor (используются нативно движком).
- Шейдеры (`shaders/`).
- Звук (`sounds/`).
- HUD-текстуры (`hud/`).
- Maps (`maps/.map`-файлы).

## Где у нас точки парсинга

| Парсер | Что делает |
|---|---|
| [`../../parser/parse_units.py`](../../parser/parse_units.py) | `lib/unit.script` → юнит/здание-карта. |
| [`../../parser/parse_country.py`](../../parser/parse_country.py) | `lib/country.script` → нации и ростер. |
| [`../../parser/simulate_upgrades.py`](../../parser/simulate_upgrades.py) | `lib/country.script` инлайнит `SetUpgStruct`/`AddUpgradePack` → 4 000 строк апгрейдов. |
| [`../../parser/parse_animations.py`](../../parser/parse_animations.py) | `animations/*.aaf` → frame-точные timing'и. |
| [`../../parser/parse_patterns.py`](../../parser/parse_patterns.py) | `pattern/*.pattern` → бинарные шаблоны размещения. |
| [`../../parser/parse_generator_cfg.py`](../../parser/parse_generator_cfg.py) | `gen/generator.cfg` → 60 pattern types. |
| [`../../parser/parse_locale.py`](../../parser/parse_locale.py) | `locale/<lang>/*.txt` → канонические русские названия. |
| [`../../parser/build_data.py`](../../parser/build_data.py) | Собирает всё в `docs/data.json`. |
| [`../../parser/engine_recon/*.py`](../../parser/engine_recon/) | `cossacks.exe` → `derived/dws_native_signatures.json`. |
