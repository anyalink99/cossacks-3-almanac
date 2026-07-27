<a id="юниты"></a>
# Units

[← Quick reference](../README.md)

Units are grouped by role. For a row-by-row comparison of similar troops,
open [Unit comparisons](../compare/units/README.md).

<a id="расшифровка-колонок"></a>
## Column guide

| Column | Meaning |
|---|---|
| **Unit** | Canonical English name; the internal code is secondary |
| **Nations** | Nations that have this unit (“all” means almost every nation) |
| **Health** | Health when the unit is created |
| **Training time** | Game seconds. Divide by 1.4 for real time at Fast speed. |
| **Food / Gold / Iron** | Cost per unit. Wood, Stone, and Coal are omitted because most units require none. |
| **Damage** | Raw damage of the primary weapon before the target’s protection is subtracted. See [Combat](../02_combat/README.md). |
| **Range** | Maximum weapon range in cells; zero for melee attacks |
| **Reload** | Game seconds between shots. Melee attack rate comes from the attack animation. |
| **Pike / Sword / Bullet / Grapeshot / Arrow / Cannonball** | Protection against each weapon type. Higher protection means less incoming damage. |

An em dash means the value does not apply to that unit.

> **Primary weapon:** when a unit has several attacks—for example, bayonet
> and musket—the table shows the weapon with the greatest range. Exact weapon
> slots remain available in the detailed combat reports.

<a id="содержание"></a>
## Contents

- [Peasants](#крестьяне-8-вариантов) (8 options)
- [Pikemen (17th century)](#пикинёры-17-в-8-вариантов) (8 options)
- [Pikemen (18th century)](#пикинёры-18-в-2-варианта) (2 options)
- [Light Infantry](#лёгкая-пехота-5-вариантов) (5 options)
- [Musketeers (17th century)](#мушкетёры-17-в-10-вариантов) (10 options)
- [Musketeers (18th century)](#мушкетёры-18-в-5-вариантов) (5 options)
- [Grenadiers](#гренадёры-7-вариантов) (7 options)
- [Archers](#лучники-5-вариантов) (5 options)
- [Special infantry (18th century)](#особая-пехота-18-в-6-вариантов) (6 options)
- [Light Cavalry](#лёгкая-кавалерия-10-вариантов) (10 options)
- [Dragoons](#драгуны-7-вариантов) (7 options)
- [Heavy Cavalry](#тяжёлая-кавалерия-17-вариантов) (17 options)
- [Cannons](#пушки-3-варианта) (3 options)
- [Bombards and Howitzers](#мортиры-2-варианта) (2 options)
- [Fishing boats](#рыбацкие-лодки-1-вариант) (1 option)
- [Warships](#военные-корабли-8-вариантов) (8 options)
- [Officers](#офицеры-5-вариантов) (5 options)
- [Drummers and Bagpipers](#барабанщики-и-волынщики-5-вариантов) (5 options)
- [Priests](#священники-4-варианта) (4 options)
- [Miscellaneous and missions](#разное-и-миссии-1-вариант) (1 option)

<a id="крестьяне-8-вариантов"></a>
## Peasants (8 options)

| Unit | Nations | Health | Training time, game s | Food | Gold | Iron | Damage | Range, cells | Reload, s | Pike | Sword | Bullet | Grapeshot | Arrow | Cannonball |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| **Peasant** `peaaus` | Austria, Bavaria, Prussia, Saxony, Switzerland | 50 | 12.5 | 100 | 0 | 0 | 20 | 1.22 | 0.0 | — | — | — | — | — | — |
| **Peasant** `peaeng` | Denmark, England, France, Netherlands, Sweden | 50 | 12.5 | 100 | 0 | 0 | 20 | 1.22 | 0.0 | — | — | — | — | — | — |
| **Peasant** `peapol` | Hungary, Poland | 50 | 12.5 | 100 | 0 | 0 | 20 | 1.22 | 0.0 | — | — | — | — | — | — |
| **Serf** `pearus` | Russia | 50 | 12.5 | 100 | 0 | 0 | 20 | 1.22 | 0.0 | — | — | — | — | — | — |
| **Peasant** `peasco` | Scotland | 60 | 12.5 | 100 | 0 | 0 | 20 | 1.22 | 0.0 | — | — | — | — | — | — |
| **Peasant** `peaspa` | Piedmont, Portugal, Spain, Venice | 50 | 12.5 | 100 | 0 | 0 | 20 | 1.22 | 0.0 | — | — | — | — | — | — |
| **Peasant** `peatur` | Algeria, Turkey | 50 | 12.5 | 100 | 0 | 0 | 20 | 1.22 | 0.0 | — | — | — | — | — | — |
| **Peasant** `peaukr` | Ukraine | 75 | 11.25 | 100 | 0 | 0 | 20 | 1.22 | 0.0 | — | — | — | — | — | — |

<a id="пикинёры-17-в-8-вариантов"></a>
## Pikemen (17th century) (8 options)

| Unit | Nations | Health | Training time, game s | Food | Gold | Iron | Damage | Range, cells | Reload, s | Pike | Sword | Bullet | Grapeshot | Arrow | Cannonball |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| **Pikeman, 17th century** `pikeman` | Austria, Bavaria, Denmark, England, France, Hungary, Netherlands, Piedmont, Prussia, Saxony, Spain, Sweden, Venice | 90 | 4.5 | 25 | 3 | 20 | 8 | 1.88 | 0.0 | 3 | 2 | 4 | 210 | 6 | 40 |
| **Pikeman, 17th century** `pikemanpol` | Poland | 90 | 3.0 | 25 | 1 | 0 | 8 | 2.06 | 0.0 | 0 | 0 | 0 | 0 | 0 | 0 |
| **Pikeman, 17th century** `pikemanpor` | Portugal | 100 | 4.0 | 40 | 4 | 5 | 9 | 1.88 | 0.0 | 0 | 1 | 1 | 25 | 4 | 0 |
| **Spearman** `pikemanrus` | Russia | 85 | 5.5 | 45 | 4 | 15 | 8 | 1.69 | 0.0 | 2 | 1 | 4 | 140 | 4 | 25 |
| **Covenanter pikeman** `pikemansco` | Scotland | 100 | 4.0 | 35 | 2 | 0 | 9 | 1.88 | 0.0 | 0 | 0 | 0 | 0 | 0 | 0 |
| **Coselete** `pikemanspa` | Spain | 100 | 5.5 | 35 | 7 | 30 | 10 | 1.88 | 0.0 | 3 | 4 | 6 | 240 | 12 | 50 |
| **Pikeman, 17th century** `pikemanswi` | Switzerland | 90 | 5.0 | 40 | 6 | 20 | 10 | 1.88 | 0.0 | 3 | 3 | 6 | 220 | 6 | 45 |
| **Ottoman Pikeman** `pikemantur` | Algeria, Turkey | 95 | 5.5 | 55 | 5 | 0 | 9 | 2.06 | 0.0 | 0 | 0 | 0 | 0 | 0 | 0 |

<a id="пикинёры-18-в-2-варианта"></a>
## Pikemen (18th century) (2 options)

| Unit | Nations | Health | Training time, game s | Food | Gold | Iron | Damage | Range, cells | Reload, s | Pike | Sword | Bullet | Grapeshot | Arrow | Cannonball |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| **Pikeman, 18th century** `pikeman18` | Austria, Bavaria, Denmark, England, France, Hungary, Netherlands, Piedmont, Poland, Portugal, Prussia, Russia, Saxony, Spain, Switzerland, Venice | 85 | 1.25 | 30 | 2 | 0 | 9 | 1.88 | 0.0 | — | — | — | — | — | — |
| **Pikeman, 18th century** `pikeman18swe` | Sweden | 110 | 1.5 | 40 | 3 | 0 | 11 | 1.88 | 0.0 | — | — | — | — | — | — |

<a id="лёгкая-пехота-5-вариантов"></a>
## Light infantry (5 options)

| Unit | Nations | Health | Training time, game s | Food | Gold | Iron | Damage | Range, cells | Reload, s | Pike | Sword | Bullet | Grapeshot | Arrow | Cannonball |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| **Light Infantryman** `lightinfantry` | Algeria, Turkey | 55 | 1.0 | 25 | 0 | 1 | 5 | 0.94 | 0.0 | — | — | — | — | — | — |
| **Light Infantryman (mercenary)** `lightinfantrydip` | all | 50 | 1.25 | 0 | 4 | 0 | 16 | 0.94 | 0.0 | — | — | — | — | — | — |
| **Roundshier** `roundshier` | Austria | 100 | 4.0 | 20 | 3 | 25 | 6 | 1.13 | 0.0 | 3 | 3 | 7 | 225 | 16 | 80 |
| **Roundshier (mercenary)** `roundshierdip` | all | 75 | 1.5 | 0 | 12 | 0 | 6 | 1.13 | 0.0 | 5 | 3 | 8 | 225 | 17 | 80 |
| **Sword Clansman** `swordsmansco` | Scotland | 180 | 7.0 | 110 | 10 | 0 | 10 | 1.13 | 0.0 | 1 | 2 | 2 | 110 | 6 | 10 |

<a id="мушкетёры-17-в-10-вариантов"></a>
## Musketeers (17th century) (10 options)

| Unit | Nations | Health | Training time, game s | Food | Gold | Iron | Damage | Range, cells | Reload, s | Pike | Sword | Bullet | Grapeshot | Arrow | Cannonball |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| **Hajduk** `gauduk` | Hungary | 60 | 4.5 | 35 | 4 | 4 | 9 | 14.06 | 3.12 | — | — | — | — | — | — |
| **Janissary** `jannisary` | Turkey | 65 | 8.0 | 55 | 13 | 5 | 12 | 15.94 | 4.69 | — | — | — | — | — | — |
| **Musketeer, 17th century** `musketeer` | Bavaria, Denmark, England, France, Piedmont, Portugal, Prussia, Saxony, Sweden, Switzerland, Venice | 70 | 6.0 | 45 | 6 | 5 | 12 | 15.0 | 4.69 | — | — | — | — | — | — |
| **Musketeer, 17th century** `musketeeraus` | Austria | 55 | 6.5 | 35 | 9 | 15 | 12 | 15.0 | 5.0 | 2 | 2 | 5 | 165 | 5 | 35 |
| **Musketeer, 17th century** `musketeernet` | Netherlands | 65 | 5.0 | 50 | 8 | 4 | 10 | 15.0 | 3.75 | — | — | — | — | — | — |
| **Musketeer, 17th century** `musketeerpol` | Poland | 70 | 4.5 | 40 | 3 | 3 | 9 | 13.13 | 3.12 | — | — | — | — | — | — |
| **Covenanter musketeer** `musketeersco` | Scotland | 90 | 7.0 | 55 | 8 | 7 | 12 | 15.94 | 4.69 | — | — | — | — | — | — |
| **Musketeer, 17th century** `musketeerspa` | Spain | 85 | 7.5 | 40 | 12 | 20 | 15 | 15.94 | 5.94 | 3 | 2 | 5 | 210 | 7 | 40 |
| **Serdiuk** `serdiuk` | Ukraine | 85 | 11.0 | 60 | 11 | 5 | 12 | 16.88 | 4.06 | — | — | — | — | — | — |
| **Strelets** `strelet` | Russia | 85 | 8.5 | 70 | 7 | 9 | 12 | 13.13 | 4.69 | — | — | — | — | — | — |

<a id="мушкетёры-18-в-5-вариантов"></a>
## Musketeers (18th century) (5 options)

| Unit | Nations | Health | Training time, game s | Food | Gold | Iron | Damage | Range, cells | Reload, s | Pike | Sword | Bullet | Grapeshot | Arrow | Cannonball |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| **Musketeer, 18th century** `musketeer18` | Austria, England, France, Hungary, Netherlands, Piedmont, Poland, Portugal, Russia, Spain, Sweden, Switzerland, Venice | 100 | 4.5 | 50 | 40 | 40 | 16 | 16.88 | 4.69 | — | — | — | — | — | — |
| **Musketeer, 18th century** `musketeer18bav` | Bavaria | 100 | 5.0 | 60 | 55 | 35 | 22 | 17.81 | 5.94 | — | — | — | — | — | — |
| **Musketeer, 18th century** `musketeer18den` | Denmark | 100 | 5.5 | 50 | 80 | 40 | 29 | 16.88 | 5.94 | — | — | — | — | — | — |
| **Musketeer, 18th century** `musketeer18pru` | Prussia | 100 | 6.0 | 70 | 80 | 40 | 22 | 17.81 | 4.69 | — | — | — | — | — | — |
| **Musketeer, 18th century** `musketeer18sax` | Saxony | 90 | 4.5 | 40 | 45 | 40 | 19 | 16.88 | 4.38 | — | — | — | — | — | — |

<a id="гренадёры-7-вариантов"></a>
## Grenadiers (7 options)

| Unit | Nations | Health | Training time, game s | Food | Gold | Iron | Damage | Range, cells | Reload, s | Pike | Sword | Bullet | Grapeshot | Arrow | Cannonball |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| **Grenadier** `grenadier` | Austria, England, France, Netherlands, Piedmont, Poland, Portugal, Prussia, Russia, Spain, Sweden, Switzerland, Venice | 120 | 6.0 | 80 | 60 | 40 | 16 | 16.88 | 5.31 | — | — | — | — | — | — |
| **Grenadier** `grenadierbav` | Bavaria | 125 | 6.0 | 95 | 70 | 40 | 19 | 16.88 | 5.31 | — | — | — | — | — | — |
| **Grenadier** `grenadierden` | Denmark | 125 | 6.5 | 100 | 90 | 40 | 19 | 16.88 | 5.94 | — | — | — | — | — | — |
| **Grenadier (mercenary)** `grenadierdip` | all | 30 | 1.5 | 0 | 25 | 0 | 16 | 15.0 | 4.69 | — | — | — | — | — | — |
| **Grenadier** `grenadierhun` | Hungary | 125 | 6.5 | 90 | 80 | 40 | 16 | 16.88 | 5.31 | — | — | — | — | — | — |
| **Grenadier** `grenadierpru` | Prussia | 125 | 7.0 | 90 | 100 | 45 | 16 | 16.88 | 4.38 | — | — | — | — | — | — |
| **Grenadier** `grenadiersax` | Saxony | 100 | 6.0 | 50 | 60 | 40 | 19 | 17.81 | 5.31 | — | — | — | — | — | — |

<a id="лучники-5-вариантов"></a>
## Archers (5 options)

| Unit | Nations | Health | Training time, game s | Food | Gold | Iron | Damage | Range, cells | Reload, s | Pike | Sword | Bullet | Grapeshot | Arrow | Cannonball |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| **Archer** `archer` | Algeria | 40 | 1.5 | 20 | 1 | 0 | 15 | 15.0 | 2.34 | — | — | — | — | — | — |
| **Archer (mercenary)** `archerdip` | all | 20 | 1.25 | 0 | 15 | 0 | 100 | 14.06 | 0.78 | — | — | — | — | — | — |
| **Bow Clansman** `archersco` | Scotland | 150 | 6.0 | 80 | 7 | 0 | 150 | 18.75 | 4.38 | — | — | — | — | — | — |
| **Turkish archer** `archertur` | Turkey | 65 | 3.0 | 45 | 4 | 0 | 150 | 16.88 | 4.38 | — | — | — | — | — | — |
| **Turkish archer (mercenary)** `archerturdip` | all | 20 | 1.25 | 0 | 15 | 0 | 100 | 14.06 | 0.78 | — | — | — | — | — | — |

<a id="особая-пехота-18-в-6-вариантов"></a>
## Special infantry (18th century) (6 options)
| Unit | Nations | Health | Training time, game s | Food | Gold | Iron | Damage | Range, cells | Reload, s | Pike | Sword | Bullet | Grapeshot | Arrow | Cannonball |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| **Chasseur** `chasseur` | France | 75 | 7.5 | 50 | 45 | 15 | 20 | 19.69 | 5.94 | — | — | — | — | — | — |
| **Highlander** `highlander` | England | 130 | 6.5 | 90 | 25 | 10 | 16 | 15.94 | 5.0 | — | — | — | — | — | — |
| **Volunteer** `jagerpor` | Portugal | 50 | 2.25 | 30 | 2 | 5 | 10 | 15.0 | 5.94 | — | — | — | — | — | — |
| **Jaeger** `jagerswi` | Switzerland | 65 | 8.5 | 40 | 70 | 20 | 20 | 22.5 | 6.88 | — | — | — | — | — | — |
| **Pandur** `pandur` | Austria | 85 | 5.5 | 40 | 15 | 10 | 17 | 16.88 | 4.69 | — | — | — | — | — | — |
| **Szekely** `pandurhun` | Hungary | 75 | 6.5 | 30 | 25 | 10 | 19 | 18.75 | 5.0 | — | — | — | — | — | — |

<a id="лёгкая-кавалерия-10-вариантов"></a>
## Light cavalry (10 options)

| Unit | Nations | Health | Training time, game s | Food | Gold | Iron | Damage | Range, cells | Reload, s | Pike | Sword | Bullet | Grapeshot | Arrow | Cannonball |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| **Croat** `croat` | Austria | 260 | 15.75 | 80 | 6 | 2 | 9 | 1.22 | 0.0 | — | — | — | — | — | — |
| **Hetman** `hetman` | Ukraine | 320 | 16.5 | 150 | 150 | 10 | 70 | 1.22 | 0.0 | 0 | 1 | 3 | 75 | 3 | 15 |
| **Hussar** `hussar` | Austria, Bavaria, Denmark, England, France, Netherlands, Piedmont, Poland, Portugal, Russia, Saxony, Spain, Sweden, Venice | 230 | 15.0 | 70 | 20 | 2 | 12 | 1.22 | 0.0 | — | — | — | — | — | — |
| **Hussar** `hussarhun` | Hungary | 250 | 21.0 | 100 | 30 | 2 | 10 | 1.22 | 0.0 | — | — | — | — | — | — |
| **Hussar** `hussarpru` | Prussia | 240 | 11.25 | 80 | 15 | 2 | 9 | 1.22 | 0.0 | — | — | — | — | — | — |
| **Mounted Jaeger** `hussarswi` | Switzerland | 265 | 19.5 | 120 | 30 | 2 | 14 | 1.22 | 0.0 | — | — | — | — | — | — |
| **Lancer** `lancersco` | Scotland | 320 | 21.0 | 120 | 6 | 0 | 11 | 1.88 | 0.0 | 0 | 0 | 0 | 0 | 0 | 0 |
| **Light cavalry** `lightcavalry` | Hungary | 175 | 21.0 | 90 | 50 | 6 | 14 | 18.75 | 5.31 | — | — | — | — | — | — |
| **Light cavalry (mercenary)** `lightcavalrydip` | all | 100 | 2.0 | 0 | 120 | 0 | 18 | 15.0 | 2.25 | — | — | — | — | — | — |
| **Raider** `raidersco` | Scotland | 280 | 22.5 | 130 | 8 | 2 | 11 | 1.22 | 0.0 | — | — | — | — | — | — |

<a id="драгуны-7-вариантов"></a>
## Dragoons (7 options)

| Unit | Nations | Health | Training time, game s | Food | Gold | Iron | Damage | Range, cells | Reload, s | Pike | Sword | Bullet | Grapeshot | Arrow | Cannonball |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| **Dragoon, 17th century** `dragoon` | Austria, Bavaria, Denmark, England, France, Hungary, Netherlands, Piedmont, Poland, Portugal, Prussia, Saxony, Spain, Sweden, Switzerland, Venice | 220 | 15.0 | 90 | 7 | 5 | 15 | 15.0 | 5.62 | — | — | — | — | — | — |
| **Dragoon, 18th century** `dragoon18` | Austria, Bavaria, Denmark, England, Poland, Portugal, Prussia, Russia, Saxony, Spain, Sweden, Switzerland, Venice | 225 | 22.5 | 70 | 60 | 7 | 19 | 16.88 | 5.31 | — | — | — | — | — | — |
| **Dragoon, 18th century (mercenary)** `dragoon18dip` | all | 100 | 2.0 | 0 | 120 | 0 | 18 | 15.0 | 2.25 | — | — | — | — | — | — |
| **Dragoon, 18th century** `dragoon18fra` | France | 140 | 15.0 | 50 | 30 | 6 | 10 | 15.0 | 4.69 | — | — | — | — | — | — |
| **Dragoon, 18th century** `dragoon18net` | Netherlands | 320 | 24.0 | 100 | 70 | 7 | 17 | 15.94 | 5.0 | — | — | — | — | — | — |
| **Dragoon, 18th century** `dragoon18pie` | Piedmont | 200 | 20.25 | 60 | 65 | 7 | 19 | 16.88 | 5.0 | — | — | — | — | — | — |
| **Pospolite ruszenie** `dragoonpol` | Poland | 185 | 13.5 | 70 | 5 | 4 | 13 | 15.94 | 5.0 | — | — | — | — | — | — |

<a id="тяжёлая-кавалерия-17-вариантов"></a>
## Heavy cavalry (17 options)

| Unit | Nations | Health | Training time, game s | Food | Gold | Iron | Damage | Range, cells | Reload, s | Pike | Sword | Bullet | Grapeshot | Arrow | Cannonball |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| **Don Cossack** `cossackdon` | Russia | 220 | 13.5 | 100 | 0 | 0 | 13 | 1.88 | 0.0 | 0 | 0 | 0 | 0 | 0 | 0 |
| **Register Cossack** `cossackregister` | Ukraine | 250 | 10.5 | 70 | 15 | 0 | 12 | 1.88 | 0.0 | 0 | 0 | 0 | 0 | 0 | 0 |
| **Sich Cossack** `cossacksich` | Ukraine | 250 | 13.5 | 130 | 0 | 2 | 13 | 1.22 | 0.0 | — | — | — | — | — | — |
| **Sich Cossack (mercenary)** `cossacksichdip` | all | 150 | 2.5 | 0 | 60 | 0 | 8 | 1.22 | 0.0 | — | — | — | — | — | — |
| **Cuirassier** `cuirassier` | Austria, Bavaria, Denmark, England, France, Hungary, Netherlands, Piedmont, Poland, Portugal, Prussia, Russia, Saxony, Spain, Sweden, Switzerland, Venice | 300 | 22.5 | 120 | 35 | 25 | 14 | 1.22 | 0.0 | 2 | 4 | 10 | 160 | 5 | 80 |
| **Cavalry Guard** `guardcavalrysax` | Saxony | 320 | 24.0 | 140 | 50 | 20 | 15 | 1.22 | 0.0 | 2 | 5 | 9 | 150 | 9 | 70 |
| **Hakkapeliitta** `hackapell` | Sweden | 245 | 18.0 | 80 | 7 | 2 | 12 | 1.22 | 0.0 | — | — | — | — | — | — |
| **King's Musketeer** `kingmusketeer` | France | 280 | 27.0 | 100 | 100 | 8 | 43 | 13.13 | 6.88 | — | — | — | — | — | — |
| **Mameluke** `mameluke` | Algeria | 280 | 12.0 | 100 | 8 | 0 | 16 | 1.88 | 0.0 | 1 | 3 | 1 | 75 | 8 | 0 |
| **Reiter** `reiter` | Austria, Bavaria, Denmark, England, France, Hungary, Netherlands, Piedmont, Portugal, Prussia, Saxony, Spain, Switzerland, Venice | 300 | 24.0 | 120 | 10 | 40 | 15 | 1.22 | 0.0 | 2 | 6 | 6 | 190 | 15 | 40 |
| **Light Reiter** `reiterpol` | Poland | 190 | 8.25 | 60 | 5 | 2 | 9 | 1.22 | 0.0 | 0 | 0 | 0 | 0 | 0 | 0 |
| **Swedish Reiter** `reiterswe` | Sweden | 300 | 22.5 | 130 | 7 | 20 | 14 | 1.22 | 0.0 | 2 | 3 | 7 | 140 | 7 | 35 |
| **Heavy Sipahi** `sipahi` | Turkey | 360 | 18.0 | 130 | 20 | 70 | 15 | 1.22 | 0.0 | 3 | 7 | 4 | 225 | 24 | 60 |
| **Light Sipahi** `spakh` | Turkey | 230 | 9.0 | 80 | 6 | 5 | 15 | 1.88 | 0.0 | 0 | 1 | 0 | 10 | 2 | 0 |
| **Tatar** `tatar` | Turkey | 185 | 11.25 | 70 | 6 | 0 | 140 | 20.63 | 4.69 | — | — | — | — | — | — |
| **Vityaz** `vityaz` | Russia | 380 | 25.5 | 160 | 13 | 25 | 14 | 1.22 | 0.0 | 2 | 4 | 3 | 160 | 17 | 40 |
| **Winged Hussar** `wingedhussar` | Poland | 225 | 26.0 | 130 | 30 | 25 | 14 | 1.88 | 0.0 | 1 | 2 | 5 | 160 | 10 | 30 |

<a id="пушки-3-варианта"></a>
## Cannons (3 options)

| Unit | Nations | Health | Training time, game s | Food | Gold | Iron | Damage | Range, cells | Reload, s | Pike | Sword | Bullet | Grapeshot | Arrow | Cannonball |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| **Cannon** `cannon` | all | 9000 | 75.0 | 0 | 400 | 400 | 1800 | 40.5 | 10.94 | — | — | — | — | — | — |
| **Frame gun** `framegun` | Scotland | 3000 | 50.0 | 0 | 300 | 150 | 500 | 33.75 | 2.81 | — | — | — | — | — | — |
| **Multi-barrelled Cannon** `multicannon` | Austria, Bavaria, Denmark, England, France, Hungary, Netherlands, Piedmont, Poland, Portugal, Prussia, Russia, Saxony, Spain, Sweden, Switzerland, Venice | 2000 | 50.0 | 0 | 400 | 250 | 500 | 13.13 | 1.88 | — | — | — | — | — | — |

<a id="мортиры-2-варианта"></a>
## Bombards and Howitzers (2 options)

| Unit | Nations | Health | Training time, game s | Food | Gold | Iron | Damage | Range, cells | Reload, s | Pike | Sword | Bullet | Grapeshot | Arrow | Cannonball |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| **Howitzer** `howitzer` | all | 3000 | 94.0 | 0 | 350 | 300 | 4000 | 26.25 | 18.75 | — | — | — | — | — | — |
| **Bombard** `mortar` | all | 400 | 25.0 | 0 | 75 | 200 | 200 | 48.75 | 7.81 | — | — | — | — | — | — |

<a id="рыбацкие-лодки-1-вариант"></a>
## Fishing boats (1 option)

| Unit | Nations | Health | Training time, game s | Food | Gold | Iron | Damage | Range, cells | Reload, s | Pike | Sword | Bullet | Grapeshot | Arrow | Cannonball |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| **Boat** `fishboat` | all | 300 | 40.0 | 0 | 0 | 0 | — | — | — | — | — | — | — | — | — |

<a id="военные-корабли-8-вариантов"></a>
## Warships (8 options)
| Unit | Nations | Health | Training time, game s | Food | Gold | Iron | Damage | Range, cells | Reload, s | Pike | Sword | Bullet | Grapeshot | Arrow | Cannonball |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| **Ship of the Line** `battleship` | all | 90000 | 390.0 | 0 | 3200 | 700 | 1800 | 36.56 | 0.62 | — | — | — | — | — | — |
| **Chaika** `chaika` | Ukraine | 25000 | 40.0 | 0 | 600 | 200 | 1000 | 20.63 | 2.34 | — | — | — | — | — | — |
| **Ferry** `ferry` | all | 62000 | 56.0 | 0 | 50 | 100 | — | — | — | — | — | — | — | — | — |
| **Frigate** `frigate` | all | 50000 | 230.0 | 0 | 1100 | 600 | 1800 | 30.94 | 2.34 | — | — | — | — | — | — |
| **Galley** `galley` | all | 35000 | 50.0 | 0 | 900 | 800 | 1000 | 58.13 | 1.56 | — | — | — | — | — | — |
| **Xebec** `xebec` | Algeria, Turkey | 65000 | 230.0 | 0 | 1600 | 320 | 1800 | 31.88 | 1.56 | — | — | — | — | — | — |
| **Yacht** `yacht` | all | 31000 | 48.0 | 0 | 450 | 150 | 1000 | 20.63 | 10.94 | — | — | — | — | — | — |
| **Yacht** `yachttur` | Turkey | 35000 | 48.0 | 0 | 450 | 150 | 0 | 30.94 | 21.88 | — | — | — | — | — | — |

<a id="офицеры-5-вариантов"></a>
## Officers (5 options)

| Unit | Nations | Health | Training time, game s | Food | Gold | Iron | Damage | Range, cells | Reload, s | Pike | Sword | Bullet | Grapeshot | Arrow | Cannonball |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| **Officer, 17th century** `officer` | Austria, Bavaria, Denmark, England, France, Hungary, Netherlands, Piedmont, Poland, Portugal, Prussia, Saxony, Spain, Sweden, Switzerland, Venice | 125 | 10.0 | 50 | 150 | 30 | 30 | 1.22 | 0.0 | 2 | 2 | 5 | 200 | 10 | 30 |
| **Officer, 18th century** `officer18` | Austria, Bavaria, Denmark, England, France, Hungary, Netherlands, Piedmont, Poland, Portugal, Prussia, Russia, Saxony, Spain, Sweden, Switzerland, Venice | 125 | 6.0 | 50 | 200 | 10 | 50 | 1.22 | 0.0 | — | — | — | — | — | — |
| **Commander** `officerrus` | Russia | 125 | 12.5 | 100 | 125 | 5 | 40 | 1.22 | 0.0 | 0 | 0 | 0 | 0 | 0 | 0 |
| **Officer** `officersco` | Scotland | 150 | 10.0 | 130 | 130 | 10 | 40 | 1.22 | 0.0 | 0 | 0 | 0 | 0 | 0 | 0 |
| **Officer** `officertur` | Algeria, Turkey | 125 | 7.5 | 50 | 100 | 0 | 30 | 1.22 | 0.0 | 0 | 0 | 0 | 0 | 0 | 0 |

<a id="барабанщики-и-волынщики-5-вариантов"></a>
## Drummers and Bagpipers (5 options)

| Unit | Nations | Health | Training time, game s | Food | Gold | Iron | Damage | Range, cells | Reload, s | Pike | Sword | Bullet | Grapeshot | Arrow | Cannonball |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| **Bagpiper** `bagpiper` | England, Scotland | 150 | 7.0 | 120 | 20 | 0 | — | — | — | — | — | — | — | — | — |
| **Drummer, 17th century** `drummer` | Austria, Bavaria, Denmark, England, France, Hungary, Netherlands, Piedmont, Poland, Portugal, Prussia, Saxony, Spain, Sweden, Switzerland, Venice | 75 | 5.0 | 60 | 20 | 0 | — | — | — | — | — | — | — | — | — |
| **Drummer, 18th century** `drummer18` | Austria, Bavaria, Denmark, France, Hungary, Netherlands, Piedmont, Poland, Portugal, Prussia, Russia, Saxony, Spain, Sweden, Switzerland, Venice | 100 | 6.0 | 50 | 30 | 0 | — | — | — | — | — | — | — | — | — |
| **Drummer, 17th century** `drummerrus` | Russia | 100 | 6.0 | 90 | 15 | 0 | — | — | — | — | — | — | — | — | — |
| **Drummer, 17th century** `drummertur` | Algeria, Turkey | 50 | 4.0 | 30 | 15 | 0 | — | — | — | — | — | — | — | — | — |

<a id="священники-4-варианта"></a>
## Priests (4 options)

| Unit | Nations | Health | Training time, game s | Food | Gold | Iron | Damage | Range, cells | Reload, s | Pike | Sword | Bullet | Grapeshot | Arrow | Cannonball |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| **Mullah** `mullah` | Algeria, Turkey | 75 | 15.0 | 30 | 10 | 0 | 15 | 9.38 | 0.0 | — | — | — | — | — | — |
| **Padre** `padre` | Piedmont | 90 | 25.0 | 50 | 40 | 0 | 30 | 7.5 | 0.0 | — | — | — | — | — | — |
| **Pope** `pope` | Russia, Ukraine | 75 | 20.0 | 40 | 20 | 0 | 25 | 6.56 | 0.0 | — | — | — | — | — | — |
| **Priest** `priest` | Austria, Bavaria, Denmark, England, France, Hungary, Netherlands, Poland, Portugal, Prussia, Saxony, Scotland, Spain, Sweden, Switzerland, Venice | 100 | 20.0 | 60 | 25 | 0 | 20 | 7.5 | 0.0 | — | — | — | — | — | — |
<a id="разное-и-миссии-1-вариант"></a>
## Miscellaneous and missions (1 option)

| Unit | Nations | Health | Training time, game s | Food | Gold | Iron | Damage | Range, cells | Reload, s | Pike | Sword | Bullet | Grapeshot | Arrow | Cannonball |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| **Mission placeholder** `unitbox` | all | 100 | 3.12 | 100 | 0 | 0 | — | — | — | — | — | — | — | — | — |
