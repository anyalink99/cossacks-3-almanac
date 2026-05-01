# Форматы файлов в `data/`

Краткий справочник по бинарным и текстовым форматам, которые
встречаются в `data/`. Для каждого — указание на наш парсер
(если есть) и кратко суть.

## `.script` — DWS source

Текст в `cp1251`, синтаксис Object Pascal с DWS-расширениями. См.
[`../scripts/structure.md`](../scripts/structure.md) — там полная
информация про структуру и парсинг.

## `.parser` / `.global` / `.source` / `.inc` — текстовый конфиг

Иерархический key-value формат, native-парсер в exe. Используется
в:

- `data/scripts/dmscript.global` — глобальные `gc_*`-константы.
- `data/scripts/dmscript.source` — начальное состояние глобальных vars.
- `data/scripts/units/<sid>/<sid>.parser` — конфиг юнитов.
- `data/objects/*.parser` — конфиг classes объектов.
- `data/gen/generator.cfg` — параметры генератора карт.

### Синтаксис

```
section.begin
   Code : struct.begin
      [*] = ;gc_ResCount = 7;
      [*] = ;gc_statetag_essential_none = 1 shl 0;
      ...
   end;
end;
```

Или более простая форма (объекты):

```
gameobject begin
   classname = "Peasant"
   hp = 50
   actor = "actors/peasant.actor"
end;
```

### Парсер

Native-функции в exe (см. [`../engine/native_api.md`](../engine/native_api.md)):
- `ParserCreate(name : String) : Integer` — создать parser-handle.
- `ParserLoadFromFile(filename : String) : Boolean` — загрузить с диска.
- `ParserSelectByHandleByKey(parserhnd, key : String) : Integer` — навигация по ключу.
- `ParserGetIntValueByKeyByHandle(parserhnd, key : String) : Integer`,
  `ParserGetFloatValueByKeyByHandle`, `ParserGetValueByKeyByHandle` — чтение.
- `ParserSetIntValueByKeyByHandle` (и аналоги) — запись.

В нашем коде встречаются прямые regex-парсеры
(`parser/parse_country.py`, `parser/parse_units.py`) — мы не
эмулируем native parser полностью, только нужные нам подмножества.

## `.aaf` — Actor Animation File

Текст (в `data/animations/aaf/*.aaf`) с описанием анимационных
треков юнита/здания. Каждый трек — диапазон кадров.

### Структура

```
"walk", 1, 24,
"attack0", 32, 46,
"workfood", 278, 299,
...
```

Формат: `"имя_трека", start_frame, end_frame`. 1 кадр = 1/32 игровой
секунды (`gc_time_to_frames = 32`).

### Парсер

[`parser/parse_animations.py`](../../parser/parse_animations.py) →
[`derived/animations.json`](../../derived/animations.json). 1 382
трека из 194 .aaf файлов. Используется для расчёта реального DPS:
`melee_swing_sec(sid)` берёт точку удара в кадрах атаки и переводит
в g-секунды.

## `.pattern` — бинарный шаблон размещения

Кисти-«штампы» для генератора карт: лес, скальные массивы, поля,
группы декораций. 711 файлов в `data/pattern/`.

### Формат

Полная разборка в начале
[`parser/parse_patterns.py`](../../parser/parse_patterns.py). Кратко:

```
offset    layout
0         u32 width                  // ширина mask'и в углах тайла
4         u32 height                 //
8         u8[w*h] mask               // битмаска размещения объектов
8+C       f32[w*h] heightmap         // hilliness
...       padding
...       rec[cells] (24 байта)      // на каждую занятую ячейку:
                                     //   u32 variant_id, f32 scale_x/y/z,
                                     //   f32 reserved, u32 flags
...       u8[cells*16] reserved
```

### Парсер

[`parser/parse_patterns.py`](../../parser/parse_patterns.py) +
[`parser/parse_pattern_inventory.py`](../../parser/parse_pattern_inventory.py)
→ [`derived/pattern_inventory.json`](../../derived/pattern_inventory.json),
[`derived/pattern_types.json`](../../derived/pattern_types.json),
[`derived/pattern_type_stats.json`](../../derived/pattern_type_stats.json).

100% файлов парсятся. Используется в калибровке
[`compute/compute_map_resources.py`](../../compute/compute_map_resources.py)
для оценки числа деревьев на карте.

## `.tga` — TrueVision Targa (терреин-маски)

Стандартный 24/32-bit Targa-формат. В C3 используется для
терреин-масок генератора карт:

- `data/gen/terrainmasks/<terrain>/<n>pl_*.tga` — для каждого типа
  ландшафта × числа игроков. ~230 базовых для Land 4-player.

Не парсится у нас (используется только движок).

## `.bmp` — Windows Bitmap

Стандартный BMP. Используется для:

- `data/gen/*.bmp` — служебные битмапы генератора.
- `data/brushes/*.bmp` — кисти редактора.

Не парсится у нас.

## `.dds` — DirectDraw Surface (текстуры)

Стандартный DDS-формат (DXT-сжатые текстуры). В `data/materials/`
и `data/terrain/`. Не парсится.

## `.actor` / `.tlf` — 3D-модели

Бинарный формат GSC-движка. 3D-меши, скелеты, материалы. Не
разобран у нас и не планируется (мы не работаем с 3D-данными).

## `.lib` — индексы / манифесты

Универсальный формат-обёртка GSC. Содержит список ресурсов и
указатели на них. Например:
- `data/animations/animations.lib` — индекс anim-файлов.
- `data/actors/*.lib` — индекс модели (с meta).

Не разбираем — обходим напрямую через `rglob('*.aaf')` и т.д.

## `.aix` — бинарный AI-конфиг

Используется в:
- `data/scripts/common.aix` — общие AI-константы.
- `data/maps/*.aix` — AI-конфиги для встроенных карт.
- `data/gui/*.aix` — UI-конфиги.

Формат не разобран как байт-структура, но **редактор встроен в
`editor.exe`** через классы `TAIXEditor`, `TAIXEditorState`,
`TAIXArgsEditor`, `TAIXVarsEditor` (см.
[`../engine/rtti_class_map.md` §16](../engine/rtti_class_map.md)).
По именам — это структура «переменные + аргументы». Точные
байты — только декомпиляция RTTI-методов этих классов.

Не критично для gameplay: AI-логика описана в `lib/ai.script` и
через `AIRegion*`-API (см. [`../engine/native_api.md` §2.6](../engine/native_api.md)).

## `.lng` / `.loc` — локализация

`.loc` — текстовый «иерархический» формат, аналог `.parser`:

```
language begin
   russian begin
      muskrussia18 = Мушкетёр (Россия, XVIII в.)
      ...
   end;
end;
```

`.lng` — обёртка для `.loc` (старый формат, унаследован от Cossacks 1).

### Парсер

[`parser/parse_locale.py`](../../parser/parse_locale.py) →
[`derived/canonical_terms.json`](../../derived/canonical_terms.json) и
полея `name_ru` в `data.json`.

## `.ogg` / `.snd` — звук

Стандартные OGG Vorbis. `.snd` — индекс. Не парсятся.

## `.map` — готовые карты (Historical Battles)

Бинарный формат GSC. 68 файлов в `data/maps/`. Не разобран —
скирмиш-карты генерируются процедурно, поэтому формат `.map` нам не
нужен.

## `.cfg` — текстовые конфиги

Простой `key = value` формат. В `data/game/*.cfg`,
`data/cameras/*.cfg`, `data/sounds/*.cfg`. Парсится regex'ом по
месту использования.

## Сводка: что мы парсим vs что нет

| Формат | Парсим | Где | Зачем |
|---|---|---|---|
| `.script` | ✓ | parser/parse_units.py, country.py, simulate_upgrades.py | Главный источник правды gameplay. |
| `.parser` (units) | ✓ | parser/parse_units.py (regex) | Свойства юнитов и зданий. |
| `.aaf` | ✓ | parser/parse_animations.py | Frame-точные timing'и атак. |
| `.pattern` | ✓ | parser/parse_patterns.py | Шаблоны размещения объектов. |
| `.tga` (terrainmasks) | (косвенно) | compute/compute_map_resources.py | Калибровка ресурсов карт. |
| `.lng`/`.loc` | ✓ | parser/parse_locale.py | Русские названия. |
| `.cfg` (generator) | ✓ | parser/parse_generator_cfg.py | PatternList → 60 типов. |
| Replay (`.gold`?) | ✓ | parser/parse_replay.py | Sniff replay-файла для validation. |
| `.actor` / `.tlf` / `.dds` | ✗ | — | 3D-данные нам не нужны. |
| `.aix` (AI) | ✗ | — | AI описан в скриптах, бинарь не критичен. |
| `.map` | ✗ | — | Скирмиш карты процедурные. |
