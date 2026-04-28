# Каталог оружия (projectile-level)

[← compare/](README.md) · [← Index](../README.md)

Все уникальные `weaponsid` (типы снарядов и метательного оружия) с их параметрами и юнитами-носителями. Один `weaponsid` может использоваться разными юнитами с разными статами (damage/pause варьируются), но **kind, dispersion, projectile-id универсальны** — они задаются в самом weapon-объекте (см. `weapon.script`).

В колонке `dmg` показан **диапазон** значений среди юнитов-носителей (`min..max` если разные, иначе одно число). То же для `reload (s)`.

| weaponsid | kind | dmg | reload (s) | range (t) | cost (per shot) | Юниты-носители |
|---|---|---|---:|---:|---|---|
| `DIMMORT1` | cannonball | 4000 | 18.75 | 26.25 | {"coal": 100, "iron": 20} | howitzer |
| `DIMMORT2` | mortarball | 200 | 7.81 | 48.75 | {"coal": 30, "iron": 20} | mortar |
| `DIMMORT2KOR` | mortarball | 1000 | 1.56 | 58.13 | {"coal": 9, "iron": 4} | galley |
| `NUCLGRE` | mortarball | 110 | 2.34 | 9.38 | — | grenadier, grenadierbav, grenadierden, grenadierdip, grenadierhun, grenadierpru (+1) |
| `OSTRELA` | firearrow | 140..150 | 3.91..4.69 | 11.25..20.63 | {"wood": 1}, {"wood": 2} | archer, archerdip, archersco, archertur, archerturdip, tatar |
| `PPOINTT` | cannonball | 1800 | 10.94 | 40.5 | {"coal": 40, "iron": 20} | cannon |
| `PPOINTTFRAME` | cannonball | 500 | 2.81 | 33.75 | {"coal": 40, "iron": 30} | framegun |
| `PPOINTTKOR` | cannonball | 100..1800 | 2.34..10.94 | 20.63..30.94 | {"coal": 35, "iron": 25}, {"coal": 9, "iron": 4} | battleship, chaika, frigate, galley, xebec, yacht (+1) |
| `PSMPOINTT` | cannister | 500 | 1.88 | 13.13 | {"coal": 30, "iron": 40} | multicannon |
| `PSMPOINTTPUS` | cannister | 0 | 10.94 | 8.44 | {"coal": 21, "iron": 24} | cannon |
| `SHOTMUSKET` | bullet | 9..29 | 2.81..5.94 | 15.0..17.81 | {"coal": 3, "iron": 2}, {"coal": 3, "iron": 3}, {"coal": 4, "iron": 2}, {"coal": 4, "iron": 3}, {"coal": 5, "iron": 4} | dragoon, dragoon18, dragoon18dip, dragoon18fra, dragoon18net, dragoon18pie (+19) |
| `STRELA` | arrow | 15..20 | 1.56..3.12 | 15.0..20.63 | {"wood": 1}, {"wood": 2} | archer, archerdip, archersco, archertur, archerturdip, tatar |

## Заметки

- **`SHOTMUSKET`** — стандартный мушкетный выстрел. Используется большинством мушкетёров и драгунов. Стрелец имеет больший урон (9 vs 8) при таком же снаряде.
- **`STRELA`** / **`OSTRELA`** — обычная стрела и зажигательная. Зажигательная (OSTRELA, kind=`firearrow`) — второй weapon slot у лучников.
- **`PPOINTTKOR`** — корабельное ядро (используется фрегатом, ксебеком, баттлшипом, чайкой, галерой, яхтой).
- **`PPOINTT`** vs **`PPOINTTFRAME`** — стандартное пушечное ядро vs framegun-ядро.
- **`PSMPOINTTPUS`** / **`PSMPOINTT`** — картечь для cannon / multi-cannon.
- **`DIMMORT1`** / **`DIMMORT2`** / **`DIMMORT2KOR`** — мортирные снаряды (1 = howitzer, 2 = mortar, 2KOR = корабельная мортира галеры).
- **`NUCLGRE`** — гранадирная граната.
- **`PPOINTTTOW`** — башенно-портовое ядро (используется зданиями `tow` и `por` с пушками; не выводится в этой таблице — см. лист `Buildings` в xlsx).

Источник определений: `data/scripts/lib/weapon.script` (функция `_weapon_AddWeapon`). Дополнительные параметры (gravity, propagation, fxshot) есть в скрипте, но в этот лист не выгружены — см. raw файл при необходимости.