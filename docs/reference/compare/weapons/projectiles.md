# Каталог оружия (projectile-level)

[← weapons/](README.md) · [← compare/](../README.md) · [← Index](../../README.md)

Все уникальные `weaponsid` (типы снарядов и метательного оружия) с их параметрами и юнитами-носителями. Один `weaponsid` может использоваться разными юнитами с разными статами (damage/pause варьируются), но **kind, dispersion, projectile-id универсальны** — они задаются в самом объекте weapon (см. `weapon.script`).

В колонке `dmg` показан **диапазон** значений среди юнитов-носителей (`min..max`, если разные, иначе одно число). То же для `reload (s)`.

| weaponsid | kind | dmg | reload (s) | range (t) | cost (per shot) | Юниты-носители |
|---|---|---|---:|---:|---|---|
| `DIMMORT1` | cannonball | 4000 | 18.75 | 26.25 | {"coal": 100, "iron": 20} | howitzer |
| `DIMMORT2` | mortarball | 200 | 7.81 | 48.75 | {"coal": 30, "iron": 20} | mortar |
| `DIMMORT2KOR` | mortarball | 1000 | 1.56 | 58.13 | {"coal": 9, "iron": 4} | galley |
| `NUCLGRE` | mortarball | 110..200 | 2.34..3.12 | 7.5..11.25 | — | grenadier, grenadierbav, grenadierden, grenadierdip, grenadierhun, grenadierpru (+1) |
| `OSTRELA` | firearrow | 100..150 | 0.78..4.69 | 11.25..20.63 | {"wood": 1}, {"wood": 2} | archer, archerdip, archersco, archertur, archerturdip, tatar |
| `PPOINTT` | cannonball | 1800 | 10.94 | 40.5 | {"coal": 40, "iron": 20} | cannon |
| `PPOINTTFRAME` | cannonball | 500 | 2.81 | 33.75 | {"coal": 40, "iron": 30} | framegun |
| `PPOINTTKOR` | cannonball | 0..1800 | 0.62..21.88 | 18.75..36.56 | {"coal": 15, "iron": 5}, {"coal": 35, "iron": 25}, {"coal": 9, "iron": 4} | battleship, chaika, frigate, galley, xebec, yacht (+1) |
| `PSMPOINTT` | cannister | 500 | 1.88 | 13.13 | {"coal": 30, "iron": 40} | multicannon |
| `PSMPOINTTPUS` | cannister | 0 | 10.94 | 8.44 | {"coal": 21, "iron": 24} | cannon |
| `SHOTMUSKET` | bullet | 9..43 | 2.25..6.88 | 13.13..22.5 | {"coal": 10, "iron": 6}, {"coal": 2, "iron": 1}, {"coal": 3, "iron": 1}, {"coal": 3, "iron": 2}, {"coal": 3, "iron": 3}, {"coal": 4, "iron": 2}, {"coal": 4, "iron": 3}, {"coal": 5, "iron": 2}, {"coal": 5, "iron": 3}, {"coal": 5, "iron": 4}, {"coal": 6, "iron": 3}, {"coal": 7, "iron": 3}, {"coal": 8, "iron": 4}, {"coal": 8, "iron": 5}, {"coal": 9, "iron": 4} | chasseur, dragoon, dragoon18, dragoon18dip, dragoon18fra, dragoon18net (+32) |
| `STRELA` | arrow | 15..25 | 1.56..3.12 | 13.13..20.63 | {"wood": 1}, {"wood": 2} | archer, archerdip, archersco, archertur, archerturdip, tatar |

## Заметки

- **`SHOTMUSKET`** — стандартный мушкетный выстрел. Используется большинством мушкетёров и драгунов. Стрелец имеет больший урон (9 против 8) при таком же снаряде.
- **`STRELA`** / **`OSTRELA`** — обычная стрела и зажигательная. Зажигательная (OSTRELA, kind=`firearrow`) — второй слот оружия у лучников.
- **`PPOINTTKOR`** — корабельное ядро (используется фрегатом, ксебеком, баттлшипом, чайкой, галерой, яхтой).
- **`PPOINTT`** vs **`PPOINTTFRAME`** — стандартное пушечное ядро против ядра framegun.
- **`PSMPOINTTPUS`** / **`PSMPOINTT`** — картечь для cannon / multi-cannon.
- **`DIMMORT1`** / **`DIMMORT2`** / **`DIMMORT2KOR`** — мортирные снаряды (1 = howitzer, 2 = mortar, 2KOR = корабельная мортира галеры).
- **`NUCLGRE`** — гранадирная граната.
- **`PPOINTTTOW`** — башенно-портовое ядро (используется зданиями `tow` и `por` с пушками; не выводится в этой таблице — см. лист `Buildings` в xlsx).

Источник определений: `data/scripts/lib/weapon.script` (функция `_weapon_AddWeapon`). Дополнительные параметры (gravity, propagation, fxshot) есть в скрипте, но в этот лист не выгружены — см. исходный файл при необходимости.