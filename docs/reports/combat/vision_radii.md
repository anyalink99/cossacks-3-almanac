# Cossacks 3 — Vision и searchradius

**Производный** отчёт. Считается из `docs/data.json` скриптом [`compute/compute_vision.py`](../../compute/compute_vision.py).

Cossacks 3 имеет два концентрических радиуса «осведомлённости»:

- **vision** — радиус развёртывания fog-of-war (FOW). Сколько тайлов вокруг юнита открыты на миникарте и игровом экране для владельца.
- **searchradius** — радиус **обнаружения цели для авто-атаки**. Используется в `bartprepare` / `_unit_SearchTarget`. Пехота **не атакует** врага вне этого круга, даже если он виден через FOW.

## Формула

Радиус обзора в тайлах = `floor(20 + 4 × vision)`, где `vision` — поле в `objprop`, ЦЕЛОЕ число (обычно 0..8); вычисление — в `_unit_GetVision` [^1].

| `vision` | tiles | Кто типичный носитель |
| ---: | ---: | --- |
| 0 | **20** | Default minimum (peasant fallback) |
| 1 | **24** | Бо́льшая часть пехоты, артиллерия, башня без апгрейдов |
| 2 | **28** | Лёгкая пехота, конница средней зоркости |
| 3 | **32** | Драгуны, средняя кавалерия, башня с апгрейдом |
| 4 | **36** | Скауты, разведка, ukr-крестьянин |
| 5 | **40** | Hussar prussian, dragoon18 piedmontese |
| 7 | **48** | Hetman (топ-обзор среди тяжёлой кавалерии) |
| 8 | **52** | Drummer/Bagpiper, корабли (Battleship/Frigate) |

## §1. Полная таблица: vision (FOW) и searchradius (target acquisition) по юнитам

Группировка: одна строка на уникальный набор `(sid, vision, searchradius_tiles)`. Колонка **searchradius** — pause `weapon[0].radiusmax_tiles` (или 0 если оружие нет / melee=0).

| usage | sid | vision | fov tiles | searchradius (tiles) | nations |
| --- | --- | ---: | ---: | ---: | --- |
| Battleship | `battleship` | 8 | **52** | 31.5 | alg, aus, bav, den, eng, fra … (+14) |
| Frigate | `frigate` | 8 | **52** | 33.75 | aus, bav, den, eng, fra, hun … (+12) |
| Frigate | `xebec` | 8 | **52** | 33.75 | alg, tur |
| Light Infantry | `bagpiper` | 8 | **52** | — | eng, sco |
| Light Infantry | `drummer` | 8 | **52** | — | aus, bav, den, eng, fra, hun … (+10) |
| Light Infantry | `drummer18` | 8 | **52** | — | aus, bav, den, fra, hun, net … (+9) |
| Heavy Cavalry | `hetman` | 7 | **48** | 11.25 | ukr |
| Light Infantry | `drummertur` | 7 | **48** | — | alg, tur |
| Light Cavalry | `hussarpru` | 5 | **40** | 15.0 | pru |
| Light Infantry | `drummer18` | 5 | **40** | — | rus |
| Light Infantry | `drummerrus` | 5 | **40** | — | rus |
| Mounted Shooter | `dragoon18pie` | 5 | **40** | 16.88 | pie |
| Archer | `tatar` | 4 | **36** | 20.63 | tur |
| Light Cavalry | `hussarswi` | 4 | **36** | 13.13 | swi |
| Light Infantry | `officer18` | 4 | **36** | 9.38 | aus, bav, den, eng, fra, hun … (+11) |
| Mounted Shooter | `kingmusketeer` | 4 | **36** | 13.13 | fra |
| Peasant | `peaukr` | 4 | **36** | 5.63 | ukr |
| Shooter | `chasseur` | 4 | **36** | 19.69 | fra |
| Shooter | `jagerswi` | 4 | **36** | 22.5 | swi |
| Yacht | `chaika` | 4 | **36** | 19.69 | ukr |
| Heavy Cavalry | `cossackdon` | 3 | **32** | 16.88 | rus |
| Heavy Cavalry | `cossackregister` | 3 | **32** | 11.25 | ukr |
| Heavy Cavalry | `cuirassier` | 3 | **32** | 13.13 | aus, bav, den, eng, fra, hun … (+11) |
| Heavy Cavalry | `guardcavalrysax` | 3 | **32** | 11.25 | sax |
| Heavy Cavalry | `mameluke` | 3 | **32** | 11.25 | alg |
| Heavy Cavalry | `reiterpol` | 3 | **32** | 13.13 | pol |
| Heavy Cavalry | `spakh` | 3 | **32** | 11.25 | tur |
| Light Cavalry | `cossacksich` | 3 | **32** | 15.0 | ukr |
| Light Cavalry | `hackapell` | 3 | **32** | 15.0 | swe |
| Light Cavalry | `hussar` | 3 | **32** | 13.13 | aus, bav, den, eng, fra, net … (+8) |
| Light Cavalry | `hussarhun` | 3 | **32** | 16.88 | hun |
| Light Infantry | `officertur` | 3 | **32** | 9.38 | alg, tur |
| Mounted Shooter | `dragoon` | 3 | **32** | 15.0 | aus, bav, den, eng, fra, hun … (+10) |
| Mounted Shooter | `dragoon18` | 3 | **32** | 16.88 | aus, bav, den, eng, pol, por … (+7) |
| Mounted Shooter | `dragoon18net` | 3 | **32** | 15.94 | net |
| Peasant | `pearus` | 3 | **32** | 9.38 | rus |
| Shooter | `pandurhun` | 3 | **32** | 18.75 | hun |
| Yacht | `yacht` | 3 | **32** | 19.69 | aus, bav, den, eng, fra, hun … (+12) |
| Yacht | `yachttur` | 3 | **32** | 19.69 | tur |
| Archer | `archer` | 2 | **28** | 15.0 | alg |
| Archer | `archersco` | 2 | **28** | 18.75 | sco |
| Galley | `galley` | 2 | **28** | 20.63 | alg, aus, bav, den, eng, fra … (+14) |
| Grenadier | `grenadier` | 2 | **28** | 16.88 | aus, eng, fra, net, pie, pol … (+7) |
| Grenadier | `grenadierbav` | 2 | **28** | 16.88 | bav |
| Grenadier | `grenadierden` | 2 | **28** | 16.88 | den |
| Grenadier | `grenadierhun` | 2 | **28** | 18.75 | hun |
| Grenadier | `grenadierpru` | 2 | **28** | 16.88 | pru |
| Grenadier | `grenadiersax` | 2 | **28** | 17.81 | sax |
| Heavy Cavalry | `lancersco` | 2 | **28** | 11.25 | sco |
| Heavy Cavalry | `reiterswe` | 2 | **28** | 11.25 | swe |
| Heavy Cavalry | `sipahi` | 2 | **28** | 9.38 | tur |
| Heavy Cavalry | `vityaz` | 2 | **28** | 9.38 | rus |
| Light Cavalry | `croat` | 2 | **28** | 13.13 | aus |
| Light Cavalry | `raidersco` | 2 | **28** | 18.75 | sco |
| Light Cavalry | `wingedhussar` | 2 | **28** | 11.25 | pol |
| Light Infantry | `lightinfantry` | 2 | **28** | 13.13 | alg, tur |
| Light Infantry | `officer` | 2 | **28** | 9.38 | aus, bav, den, eng, fra, hun … (+10) |
| Light Infantry | `officersco` | 2 | **28** | 9.38 | sco |
| Light Infantry | `pikeman18` | 2 | **28** | 13.13 | aus, bav, den, eng, fra, hun … (+10) |
| Light Infantry | `pikemansco` | 2 | **28** | 13.13 | sco |
| Light Infantry | `roundshierdip` | 2 | **28** | 13.13 | sco |
| Light Infantry | `swordsmansco` | 2 | **28** | 15.0 | sco |
| Mounted Shooter | `dragoon18fra` | 2 | **28** | 15.0 | fra |
| Mounted Shooter | `dragoonpol` | 2 | **28** | 15.94 | pol |
| Mounted Shooter | `lightcavalry` | 2 | **28** | 18.75 | hun |
| Shooter | `gauduk` | 2 | **28** | 14.06 | hun |
| Shooter | `musketeer` | 2 | **28** | 15.0 | bav, den, eng, fra, pie, por … (+5) |
| Shooter | `musketeer18` | 2 | **28** | 16.88 | aus, eng, fra, hun, net, pie … (+7) |
| Shooter | `musketeer18bav` | 2 | **28** | 17.81 | bav |
| Shooter | `musketeer18den` | 2 | **28** | 16.88 | den |
| Shooter | `musketeer18pru` | 2 | **28** | 17.81 | pru |
| Shooter | `musketeer18sax` | 2 | **28** | 16.88 | sax |
| Shooter | `musketeernet` | 2 | **28** | 15.0 | net |
| Shooter | `musketeersco` | 2 | **28** | 15.94 | sco |
| Shooter | `pandur` | 2 | **28** | 16.88 | aus |
| Shooter | `serdiuk` | 2 | **28** | 16.88 | ukr |
| ? | `unitbox` | 1 | **24** | — | all |
| Archer | `archerdip` | 1 | **24** | 12.19 | all |
| Archer | `archertur` | 1 | **24** | 16.88 | tur |
| Archer | `archerturdip` | 1 | **24** | 12.19 | all |
| Cannon | `cannon` | 1 | **24** | 9.38 | all |
| Cannon | `framegun` | 1 | **24** | 22.5 | sco |
| Fishing Boat | `fishboat` | 1 | **24** | — | all |
| Grenadier | `grenadierdip` | 1 | **24** | 15.0 | all |
| Heavy Cavalry | `reiter` | 1 | **24** | 9.38 | aus, bav, den, eng, fra, hun … (+8) |
| Light Cavalry | `cossacksichdip` | 1 | **24** | 13.13 | all |
| Light Infantry | `lightinfantrydip` | 1 | **24** | 13.13 | all |
| Light Infantry | `mullah` | 1 | **24** | 9.38 | alg, tur |
| Light Infantry | `officerrus` | 1 | **24** | 9.38 | rus |
| Light Infantry | `padre` | 1 | **24** | 9.38 | pie |
| Light Infantry | `pikeman` | 1 | **24** | 13.13 | aus, bav, den, eng, fra, hun … (+7) |
| Light Infantry | `pikeman18swe` | 1 | **24** | 13.13 | swe |
| Light Infantry | `pikemanpol` | 1 | **24** | 13.13 | pol |
| Light Infantry | `pikemanpor` | 1 | **24** | 13.13 | por |
| Light Infantry | `pikemanrus` | 1 | **24** | 15.0 | rus |
| Light Infantry | `pikemanspa` | 1 | **24** | 13.13 | spa |
| Light Infantry | `pikemanswi` | 1 | **24** | 13.13 | swi |
| Light Infantry | `pikemantur` | 1 | **24** | 13.13 | alg, tur |
| Light Infantry | `pope` | 1 | **24** | 9.38 | rus, ukr |
| Light Infantry | `priest` | 1 | **24** | 9.38 | aus, bav, den, eng, fra, hun … (+10) |
| Light Infantry | `roundshier` | 1 | **24** | 11.25 | aus |
| Light Infantry | `roundshierdip` | 1 | **24** | 13.13 | alg, aus, bav, den, eng, fra … (+14) |
| Mortar | `howitzer` | 1 | **24** | 18.75 | all |
| Multi-cannon | `multicannon` | 1 | **24** | 13.13 | aus, bav, den, eng, fra, hun … (+11) |
| Peasant | `peaaus` | 1 | **24** | 5.63 | aus, bav, pru, sax, swi |
| Peasant | `peaeng` | 1 | **24** | 5.63 | den, eng, fra, net, swe |
| Peasant | `peapol` | 1 | **24** | 5.63 | hun, pol |
| Peasant | `peasco` | 1 | **24** | 7.5 | sco |
| Peasant | `peaspa` | 1 | **24** | 5.63 | pie, por, spa, ven |
| Peasant | `peatur` | 1 | **24** | 5.63 | alg, tur |
| Shooter | `dragoon18dip` | 1 | **24** | 15.94 | all |
| Shooter | `highlander` | 1 | **24** | 15.94 | eng |
| Shooter | `jagerpor` | 1 | **24** | 15.0 | por |
| Shooter | `jannisary` | 1 | **24** | 15.94 | tur |
| Shooter | `lightcavalrydip` | 1 | **24** | 15.94 | all |
| Shooter | `musketeeraus` | 1 | **24** | 15.94 | aus |
| Shooter | `musketeerpol` | 1 | **24** | 13.13 | pol |
| Shooter | `musketeerspa` | 1 | **24** | 15.94 | spa |
| Shooter | `strelet` | 1 | **24** | 13.13 | rus |
| Super Mortar | `mortar` | 1 | **24** | — | all |
| Transport | `ferry` | 1 | **24** | — | all |

## §2. Vision у зданий

В отличие от юнитов, у большинства зданий `vision=0` или поле не задано — обзор обеспечивается «врезкой» из FOW callback'а на самом здании (engine native). Здесь — те, у кого vision явно прописан.

| usage | sid | vision | fov tiles | nation |
| --- | --- | ---: | ---: | --- |
| Башня | `eurtow` | 3 | **32** | aus |
| Башня | `rustow` | 3 | **32** | rus |
| Башня | `turtow` | 3 | **32** | alg |
| Порт | `porpor` | 3 | **32** | por |

## §3. Замечания

- **Vision > searchradius** для всех юнитов кроме мортир (mortar/super mortar) и башен с пустым `searchradius`. Это значит: юнит **видит** врага раньше, чем может **обнаружить как цель**.
- **Default `vision=0`** даёт всё ещё 20 тайлов обзора — минимальный круг, чтобы юнит вообще видел окружение.
- **Drummer/Bagpiper** имеют `vision=8` ⇒ **52 тайла обзора**, при этом не атакуют (`searchradius=0`). Это лучший «чистый скаут» в игре.
- **Корабли** (Battleship/Frigate) `vision=8` — нужен для морских патрулей, далеко за пределы artillery range.
- **Hetman** (Ukraine) `vision=7` — самый зоркий конный юнит на берегу.
- **Vision не апгрейдится.** В `efficiency_upgrades.md` нет записи на `visionperc` или `+vision`.


## Источники

Все ссылки относительно `data/scripts/` в установке Cossacks 3.

[^1]: `_unit_GetVision` — `lib/unit.script:11565`.

---

Перегенерация: `python compute/compute_vision.py`