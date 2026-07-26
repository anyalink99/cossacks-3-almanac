# Cossacks 3 mods

[English](README.en.md) · **Русский**

Папка для модов, разработанных в этом репозитории. Каждый мод — отдельная подпапка по имени мода. Моды редактируют игровые скрипты через скриптовый mod-loader C3 (`mods/`, `mods.ini`, `modman.exe`) — без DLL injection и без правки `cossacks.exe`.

## Текущие моды

| Мод | Что делает | Status |
|---|---|---|
| [Deterministic Cossacks](Deterministic%20Cossacks/) | Заменяет 10 `random` в hot-path добычи и боя на детерминированные `SetRandomKey + random` для воспроизводимой добычи и одинаковых боевых исходов при Save/Load и в multiplayer | работает, ждёт эмпирической валидации |

## Конвенция структуры мода

Каждый мод в `mods/<Mod Name>/` имеет вид:

```
mods/<Mod Name>/
├── README.md          ← обоснование, install, тест-протокол, ограничения
├── build.py           ← патчер: читает оригиналы из <game>/data/, применяет патчи, выдаёт мод-папку
├── .gitignore         ← как минимум: build/, __pycache__/
├── src/
│   └── mod.ini        ← metadata template для C3 mod-loader (не для Steam Workshop)
└── build/             ← результат сборки, .gitignore'нут
    └── <Mod Name>/
        ├── mod.ini
        └── data/...   ← структура повторяет <game>/data/
```

`build.py` импортирует `parser.config` для канонического пути к игре (`COSSACKS3_PATH` env var → default Steam path). Это даёт единую точку конфигурации между парсером и модами.

## Как добавить новый мод

1. Скопировать `Deterministic Cossacks/` как шаблон, переименовать.
2. В `build.py` обновить `MOD_NAME` и список `PATCHES` (каждый patch — `file`, `name`, `expected_line`, `original`, `replacement`).
3. В `src/mod.ini` обновить `title`, `description`, `contentfolder`.
4. В `README.md` описать что патчится и зачем, со ссылками на recon-документы которые обосновывают изменения.
5. Запустить `python "mods/<Mod Name>/build.py"` — патчер проверит что все `original` строки уникально находятся в файлах.
6. Установить через `--install` или вручную (см. README мода).

## Совместимость с патчами игры

Моды копируют **целые файлы** из `<game>/data/scripts/lib/` (по 250-560 KB), потому что C3 mod-loader не умеет патчить отдельные функции — он только оверрайдит файлы целиком. Это значит:

- После обновления игры `lib/{misc,unit}.script` могут получить новые строки → старая версия мода **затрёт** их обратно к pre-update.
- `build.py` использует **точное совпадение текста** для каждого patch site, не line numbers. Если строка осталась без изменений, патч найдётся даже при сдвиге номера. Если строка изменилась — `build.py` падает с ошибкой `original line not found`, и мод нужно обновить вручную.
- Workflow после игрового патча: `python parser/build_data.py` (проверить что данные парсятся) → `python "mods/<Mod>/build.py"` (rebuild). Если падает — обновить `original` строки в patch'ах.

## Совместимость нескольких модов

Если два мода патчат **разные** файлы (e.g. `misc.script` и `weapon.script`) — они уживаются. Если **тот же** файл — последний загруженный в `mods.ini` побеждает (за этим следит C3 mod-loader). Текущая ситуация: только один мод, проблема пока не стоит.
