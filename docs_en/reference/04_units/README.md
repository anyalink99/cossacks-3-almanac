#04. Units

[← Index](README.md)

All units are grouped by class. For side-by-side comparison within a class, see [compare/](../compare/README.md).

<a id="расшифровка-колонок"></a>
## Column decoding

| Column | Meaning |
|---|---|
| **Unit** | Localized name + `sid` (internal ID from `unit.script`) |
| **nations** | List of nations that have this unit (`all` = available to everyone) |
| **HP** | Health points when created |
| **Time (g-sec)** | `buildtime` in game seconds (1 game-sec = 32 frames; for real-sec @ fast divide by 1.4) |
| **F/G/I** | Unit Price: **Food/Gold/Iron**. Wood/Stone/Coal for units almost always = 0, therefore they are hidden. |
| **damage** | `weapon.damage` of the main weapon (see below) - raw damage of one shot/hit BEFORE deducting the target's defense. The full formula is in [02_combat/README.md](../02_combat/README.md). |
| **distant (tile)** | Weapon radius in tiles (`weapon.radiusmax / 53.33`). 0 for melee. |
| **recharge** | `weapon.pause` in seconds between shots (0 for melee - where the pace is set by animation). |
| **pike / sword / bullet / buckshot / arrow / cannonball** | **Protection** of a unit from the corresponding type of weapon (`prot_pike` / `prot_sword` / `prot_bullet` / `prot_cannister` / `prot_arrow` / `prot_cannonball`). The higher it is, the less incoming damage. |

“—” in any column = the field is missing for this unit (for example, melee has no range).

> **Which weapon is shown.** For units with several weapon slots (musketeer18 = bayonet + musket; grenadier = bayonet + musket + grenade; cannon = cannonball + buckshot) the weapon with the maximum range is selected. This gives a more informative picture than weapon[0], which often = short bayonet.

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
- [Mortars](#мортиры-2-варианта) (2 options)
- [Fishing boats](#рыбацкие-лодки-1-вариант) (1 option)
- [Warships](#военные-корабли-8-вариантов) (8 options)
- [Officers](#офицеры-5-вариантов) (5 options)
- [Drummer, 17th century and bagpipers](#барабанщики-и-волынщики-5-вариантов) (5 options)
- [Priests](#священники-4-варианта) (4 options)
- [Miscellaneous and missions](#разное-и-миссии-1-вариант) (1 option)

<a id="крестьяне-8-вариантов"></a>
## Peasants (8 options)

| Unit | nations | HP | Time (g-sec) | F | G | I | damage | far (tile) | recharge | peak | sword | bullet | buckshot | arrow | core |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| **Peasant** `peaaus` | aus,bav,pru,sax,swi | 50 | 12.5 | 100 | 0 | 0 | 20 | 1.22 | 0.0 | — | — | — | — | — | — |
| **Peasant** `peaeng` | den,eng,fra,net,swe | 50 | 12.5 | 100 | 0 | 0 | 20 | 1.22 | 0.0 | — | — | — | — | — | — |
| **Peasant** `peapol` | hun,pol | 50 | 12.5 | 100 | 0 | 0 | 20 | 1.22 | 0.0 | — | — | — | — | — | — |
| **Serf** `pearus` | rus | 50 | 12.5 | 100 | 0 | 0 | 20 | 1.22 | 0.0 | — | — | — | — | — | — |
| **Peasant** `peasco` | sco | 60 | 12.5 | 100 | 0 | 0 | 20 | 1.22 | 0.0 | — | — | — | — | — | — |
| **Peasant** `peaspa` | pie,por,spa,ven | 50 | 12.5 | 100 | 0 | 0 | 20 | 1.22 | 0.0 | — | — | — | — | — | — |
| **Peasant** `peatur` | alg,tur | 50 | 12.5 | 100 | 0 | 0 | 20 | 1.22 | 0.0 | — | — | — | — | — | — |
| **Peasant** `peaukr` | ukr | 75 | 11.25 | 100 | 0 | 0 | 20 | 1.22 | 0.0 | — | — | — | — | — | — |

<a id="пикинёры-17-в-8-вариантов"></a>
## Pikemen (17th century) (8 options)

| Unit | nations | HP | Time (g-sec) | F | G | I | damage | far (tile) | recharge | peak | sword | bullet | buckshot | arrow | core |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| **Pikeman, 17th century** `pikeman` | aus,bav,den,eng,fra,hun,net,pie,pru,sax,spa,swe,ven | 90 | 4.5 | 25 | 3 | 20 | 8 | 1.88 | 0.0 | 3 | 2 | 4 | 210 | 6 | 40 |
| **Pikeman, 17th century** `pikemanpol` | pol | 90 | 3.0 | 25 | 1 | 0 | 8 | 2.06 | 0.0 | 0 | 0 | 0 | 0 | 0 | 0 |
| **Pikeman, 17th century** `pikemanpor` | por | 100 | 4.0 | 40 | 4 | 5 | 9 | 1.88 | 0.0 | 0 | 1 | 1 | 25 | 4 | 0 |
| **Spearman** `pikemanrus` | rus | 85 | 5.5 | 45 | 4 | 15 | 8 | 1.69 | 0.0 | 2 | 1 | 4 | 140 | 4 | 25 |
| **Covenanter pikeman** `pikemansco` | sco | 100 | 4.0 | 35 | 2 | 0 | 9 | 1.88 | 0.0 | 0 | 0 | 0 | 0 | 0 | 0 |
| **Coselete** `pikemanspa` | spa | 100 | 5.5 | 35 | 7 | 30 | 10 | 1.88 | 0.0 | 3 | 4 | 6 | 240 | 12 | 50 |
| **Pikeman, 17th century** `pikemanswi` | swi | 90 | 5.0 | 40 | 6 | 20 | 10 | 1.88 | 0.0 | 3 | 3 | 6 | 220 | 6 | 45 |
| **Ottoman Pikeman** `pikemantur` | alg,tur | 95 | 5.5 | 55 | 5 | 0 | 9 | 2.06 | 0.0 | 0 | 0 | 0 | 0 | 0 | 0 |

<a id="пикинёры-18-в-2-варианта"></a>
## Pikemen (18th century) (2 options)

| Unit | nations | HP | Time (g-sec) | F | G | I | damage | far (tile) | recharge | peak | sword | bullet | buckshot | arrow | core |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| **Pikeman, 18th century** `pikeman18` | aus,bav,den,eng,fra,hun,net,pie,pol,por,pru,rus,sax,spa,swi,ven | 85 | 1.25 | 30 | 2 | 0 | 9 | 1.88 | 0.0 | — | — | — | — | — | — |
| **Pikeman, 18th century** `pikeman18swe` | swe | 110 | 1.5 | 40 | 3 | 0 | 11 | 1.88 | 0.0 | — | — | — | — | — | — |

<a id="лёгкая-пехота-5-вариантов"></a>
## Light infantry (5 options)

| Unit | nations | HP | Time (g-sec) | F | G | I | damage | far (tile) | recharge | peak | sword | bullet | buckshot | arrow | core |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| **Light Infantryman** `lightinfantry` | alg,tur | 55 | 1.0 | 25 | 0 | 1 | 5 | 0.94 | 0.0 | — | — | — | — | — | — |
| **Light Infantryman (mercenary)** `lightinfantrydip` | all | 50 | 1.25 | 0 | 4 | 0 | 16 | 0.94 | 0.0 | — | — | — | — | — | — |
| **Roundshier** `roundshier` | aus | 100 | 4.0 | 20 | 3 | 25 | 6 | 1.13 | 0.0 | 3 | 3 | 7 | 225 | 16 | 80 |
| **Roundshier (mercenary)** `roundshierdip` | all | 75 | 1.5 | 0 | 12 | 0 | 6 | 1.13 | 0.0 | 5 | 3 | 8 | 225 | 17 | 80 |
| **Sword Clansman** `swordsmansco` | sco | 180 | 7.0 | 110 | 10 | 0 | 10 | 1.13 | 0.0 | 1 | 2 | 2 | 110 | 6 | 10 |

<a id="мушкетёры-17-в-10-вариантов"></a>
## Musketeers (17th century) (10 options)

| Unit | nations | HP | Time (g-sec) | F | G | I | damage | far (tile) | recharge | peak | sword | bullet | buckshot | arrow | core |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| **Hajduk** `gauduk` | hun | 60 | 4.5 | 35 | 4 | 4 | 9 | 14.06 | 3.12 | — | — | — | — | — | — |
| **Janissary** `jannisary` | tur | 65 | 8.0 | 55 | 13 | 5 | 12 | 15.94 | 4.69 | — | — | — | — | — | — |
| **Musketeer, 17th century** `musketeer` | bav,den,eng,fra,pie,por,pru,sax,swe,swi,ven | 70 | 6.0 | 45 | 6 | 5 | 12 | 15.0 | 4.69 | — | — | — | — | — | — |
| **Musketeer, 17th century** `musketeeraus` | aus | 55 | 6.5 | 35 | 9 | 15 | 12 | 15.0 | 5.0 | 2 | 2 | 5 | 165 | 5 | 35 |
| **Musketeer, 17th century** `musketeernet` | net | 65 | 5.0 | 50 | 8 | 4 | 10 | 15.0 | 3.75 | — | — | — | — | — | — |
| **Musketeer, 17th century** `musketeerpol` | pol | 70 | 4.5 | 40 | 3 | 3 | 9 | 13.13 | 3.12 | — | — | — | — | — | — |
| **Covenanter musketeer** `musketeersco` | sco | 90 | 7.0 | 55 | 8 | 7 | 12 | 15.94 | 4.69 | — | — | — | — | — | — |
| **Musketeer, 17th century** `musketeerspa` | spa | 85 | 7.5 | 40 | 12 | 20 | 15 | 15.94 | 5.94 | 3 | 2 | 5 | 210 | 7 | 40 |
| **Serdiuk** `serdiuk` | ukr | 85 | 11.0 | 60 | 11 | 5 | 12 | 16.88 | 4.06 | — | — | — | — | — | — |
| **Strelets** `strelet` | rus | 85 | 8.5 | 70 | 7 | 9 | 12 | 13.13 | 4.69 | — | — | — | — | — | — |

## Musketeers (18th century) (5 options)

| Unit | nations | HP | Time (g-sec) | F | G | I | damage | far (tile) | recharge | peak | sword | bullet | buckshot | arrow | core |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| **Musketeer, 18th century** `musketeer18` | aus,eng,fra,hun,net,pie,pol,por,rus,spa,swe,swi,ven | 100 | 4.5 | 50 | 40 | 40 | 16 | 16.88 | 4.69 | — | — | — | — | — | — |
| **Musketeer, 18th century** `musketeer18bav` | bav | 100 | 5.0 | 60 | 55 | 35 | 22 | 17.81 | 5.94 | — | — | — | — | — | — |
| **Musketeer, 18th century** `musketeer18den` | den | 100 | 5.5 | 50 | 80 | 40 | 29 | 16.88 | 5.94 | — | — | — | — | — | — |
| **Musketeer, 18th century** `musketeer18pru` | pru | 100 | 6.0 | 70 | 80 | 40 | 22 | 17.81 | 4.69 | — | — | — | — | — | — |
| **Musketeer, 18th century** `musketeer18sax` | sax | 90 | 4.5 | 40 | 45 | 40 | 19 | 16.88 | 4.38 | — | — | — | — | — | — |

## Grenadiers (7 options)

| Unit | nations | HP | Time (g-sec) | F | G | I | damage | far (tile) | recharge | peak | sword | bullet | buckshot | arrow | core |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| **Grenadier** `grenadier` | aus,eng,fra,net,pie,pol,por,pru,rus,spa,swe,swi,ven | 120 | 6.0 | 80 | 60 | 40 | 16 | 16.88 | 5.31 | — | — | — | — | — | — |
| **Grenadier** `grenadierbav` | bav | 125 | 6.0 | 95 | 70 | 40 | 19 | 16.88 | 5.31 | — | — | — | — | — | — |
| **Grenadier** `grenadierden` | den | 125 | 6.5 | 100 | 90 | 40 | 19 | 16.88 | 5.94 | — | — | — | — | — | — |
| **Grenadier (mercenary)** `grenadierdip` | all | 30 | 1.5 | 0 | 25 | 0 | 16 | 15.0 | 4.69 | — | — | — | — | — | — |
| **Grenadier** `grenadierhun` | hun | 125 | 6.5 | 90 | 80 | 40 | 16 | 16.88 | 5.31 | — | — | — | — | — | — |
| **Grenadier** `grenadierpru` | pru | 125 | 7.0 | 90 | 100 | 45 | 16 | 16.88 | 4.38 | — | — | — | — | — | — |
| **Grenadier** `grenadiersax` | sax | 100 | 6.0 | 50 | 60 | 40 | 19 | 17.81 | 5.31 | — | — | — | — | — | — |

## Archer (5 options)

| Unit | nations | HP | Time (g-sec) | F | G | I | damage | far (tile) | recharge | peak | sword | bullet | buckshot | arrow | core |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| **Archer** `archer` | alg | 40 | 1.5 | 20 | 1 | 0 | 15 | 15.0 | 2.34 | — | — | — | — | — | — |
| **Archer (mercenary)** `archerdip` | all | 20 | 1.25 | 0 | 15 | 0 | 100 | 14.06 | 0.78 | — | — | — | — | — | — |
| **Bow Clansman** `archersco` | sco | 150 | 6.0 | 80 | 7 | 0 | 150 | 18.75 | 4.38 | — | — | — | — | — | — |
| **Turkish archer** `archertur` | tur | 65 | 3.0 | 45 | 4 | 0 | 150 | 16.88 | 4.38 | — | — | — | — | — | — |
| **Turkish archer (mercenary)** `archerturdip` | all | 20 | 1.25 | 0 | 15 | 0 | 100 | 14.06 | 0.78 | — | — | — | — | — | — |

## Special infantry (18th century) (6 options)
| Unit | nations | HP | Time (g-sec) | F | G | I | damage | far (tile) | recharge | peak | sword | bullet | buckshot | arrow | core |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| **Chasseur** `chasseur` | fra | 75 | 7.5 | 50 | 45 | 15 | 20 | 19.69 | 5.94 | — | — | — | — | — | — |
| **Highlander** `highlander` | eng | 130 | 6.5 | 90 | 25 | 10 | 16 | 15.94 | 5.0 | — | — | — | — | — | — |
| **Volunteer** `jagerpor` | por | 50 | 2.25 | 30 | 2 | 5 | 10 | 15.0 | 5.94 | — | — | — | — | — | — |
| **Chasseur** `jagerswi` | swi | 65 | 8.5 | 40 | 70 | 20 | 20 | 22.5 | 6.88 | — | — | — | — | — | — |
| **Pandur** `pandur` | aus | 85 | 5.5 | 40 | 15 | 10 | 17 | 16.88 | 4.69 | — | — | — | — | — | — |
| **Szekely** `pandurhun` | hun | 75 | 6.5 | 30 | 25 | 10 | 19 | 18.75 | 5.0 | — | — | — | — | — | — |

<a id="лёгкая-кавалерия-10-вариантов"></a>
## Light cavalry (10 options)

| Unit | nations | HP | Time (g-sec) | F | G | I | damage | far (tile) | recharge | peak | sword | bullet | buckshot | arrow | core |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| **Croat** `croat` | aus | 260 | 15.75 | 80 | 6 | 2 | 9 | 1.22 | 0.0 | — | — | — | — | — | — |
| **Hetman** `hetman` | ukr | 320 | 16.5 | 150 | 150 | 10 | 70 | 1.22 | 0.0 | 0 | 1 | 3 | 75 | 3 | 15 |
| **Hussar** `hussar` | aus,bav,den,eng,fra,net,pie,pol,por,rus,sax,spa,swe,ven | 230 | 15.0 | 70 | 20 | 2 | 12 | 1.22 | 0.0 | — | — | — | — | — | — |
| **Hussar** `hussarhun` | hun | 250 | 21.0 | 100 | 30 | 2 | 10 | 1.22 | 0.0 | — | — | — | — | — | — |
| **Hussar** `hussarpru` | pru | 240 | 11.25 | 80 | 15 | 2 | 9 | 1.22 | 0.0 | — | — | — | — | — | — |
| **Mounted Jaeger** `hussarswi` | swi | 265 | 19.5 | 120 | 30 | 2 | 14 | 1.22 | 0.0 | — | — | — | — | — | — |
| **Lancer** `lancersco` | sco | 320 | 21.0 | 120 | 6 | 0 | 11 | 1.88 | 0.0 | 0 | 0 | 0 | 0 | 0 | 0 |
| **Light cavalry** `lightcavalry` | hun | 175 | 21.0 | 90 | 50 | 6 | 14 | 18.75 | 5.31 | — | — | — | — | — | — |
| **Light cavalry (mercenary)** `lightcavalrydip` | all | 100 | 2.0 | 0 | 120 | 0 | 18 | 15.0 | 2.25 | — | — | — | — | — | — |
| **Raider** `raidersco` | sco | 280 | 22.5 | 130 | 8 | 2 | 11 | 1.22 | 0.0 | — | — | — | — | — | — |

<a id="драгуны-7-вариантов"></a>
## Dragoons (7 options)

| Unit | nations | HP | Time (g-sec) | F | G | I | damage | far (tile) | recharge | peak | sword | bullet | buckshot | arrow | core |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| **Dragoon, 17th century** `dragoon` | aus,bav,den,eng,fra,hun,net,pie,pol,por,pru,sax,spa,swe,swi,ven | 220 | 15.0 | 90 | 7 | 5 | 15 | 15.0 | 5.62 | — | — | — | — | — | — |
| **Dragoon, 18th century** `dragoon18` | aus,bav,den,eng,pol,por,pru,rus,sax,spa,swe,swi,ven | 225 | 22.5 | 70 | 60 | 7 | 19 | 16.88 | 5.31 | — | — | — | — | — | — |
| **Dragoon, 18th century (mercenary)** `dragoon18dip` | all | 100 | 2.0 | 0 | 120 | 0 | 18 | 15.0 | 2.25 | — | — | — | — | — | — |
| **Dragoon, 18th century** `dragoon18fra` | fra | 140 | 15.0 | 50 | 30 | 6 | 10 | 15.0 | 4.69 | — | — | — | — | — | — |
| **Dragoon, 18th century** `dragoon18net` | net | 320 | 24.0 | 100 | 70 | 7 | 17 | 15.94 | 5.0 | — | — | — | — | — | — |
| **Dragoon, 18th century** `dragoon18pie` | pie | 200 | 20.25 | 60 | 65 | 7 | 19 | 16.88 | 5.0 | — | — | — | — | — | — |
| **Pospolite ruszenie** `dragoonpol` | pol | 185 | 13.5 | 70 | 5 | 4 | 13 | 15.94 | 5.0 | — | — | — | — | — | — |

<a id="тяжёлая-кавалерия-17-вариантов"></a>
## Heavy cavalry (17 options)

| Unit | nations | HP | Time (g-sec) | F | G | I | damage | far (tile) | recharge | peak | sword | bullet | buckshot | arrow | core |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| **Don Cossack** `cossackdon` | rus | 220 | 13.5 | 100 | 0 | 0 | 13 | 1.88 | 0.0 | 0 | 0 | 0 | 0 | 0 | 0 |
| **Register Cossack** `cossackregister` | ukr | 250 | 10.5 | 70 | 15 | 0 | 12 | 1.88 | 0.0 | 0 | 0 | 0 | 0 | 0 | 0 |
| **Sich Cossack** `cossacksich` | ukr | 250 | 13.5 | 130 | 0 | 2 | 13 | 1.22 | 0.0 | — | — | — | — | — | — |
| **Sich Cossack (mercenary)** `cossacksichdip` | all | 150 | 2.5 | 0 | 60 | 0 | 8 | 1.22 | 0.0 | — | — | — | — | — | — |
| **Cuirassier** `cuirassier` | aus,bav,den,eng,fra,hun,net,pie,pol,por,pru,rus,sax,spa,swe,swi,ven | 300 | 22.5 | 120 | 35 | 25 | 14 | 1.22 | 0.0 | 2 | 4 | 10 | 160 | 5 | 80 |
| **Cavalry Guard** `guardcavalrysax` | sax | 320 | 24.0 | 140 | 50 | 20 | 15 | 1.22 | 0.0 | 2 | 5 | 9 | 150 | 9 | 70 |
| **Hakkapeliitta** `hackapell` | swe | 245 | 18.0 | 80 | 7 | 2 | 12 | 1.22 | 0.0 | — | — | — | — | — | — |
| **King's Musketeer** `kingmusketeer` | fra | 280 | 27.0 | 100 | 100 | 8 | 43 | 13.13 | 6.88 | — | — | — | — | — | — |
| **Mameluke** `mameluke` | alg | 280 | 12.0 | 100 | 8 | 0 | 16 | 1.88 | 0.0 | 1 | 3 | 1 | 75 | 8 | 0 |
| **Reiter** `reiter` | aus,bav,den,eng,fra,hun,net,pie,por,pru,sax,spa,swi,ven | 300 | 24.0 | 120 | 10 | 40 | 15 | 1.22 | 0.0 | 2 | 6 | 6 | 190 | 15 | 40 |
| **Light Reiter** `reiterpol` | pol | 190 | 8.25 | 60 | 5 | 2 | 9 | 1.22 | 0.0 | 0 | 0 | 0 | 0 | 0 | 0 |
| **Swedish Reiter** `reiterswe` | swe | 300 | 22.5 | 130 | 7 | 20 | 14 | 1.22 | 0.0 | 2 | 3 | 7 | 140 | 7 | 35 |
| **Heavy Sipahi** `sipahi` | tur | 360 | 18.0 | 130 | 20 | 70 | 15 | 1.22 | 0.0 | 3 | 7 | 4 | 225 | 24 | 60 |
| **Light Sipahi** `spakh` | tur | 230 | 9.0 | 80 | 6 | 5 | 15 | 1.88 | 0.0 | 0 | 1 | 0 | 10 | 2 | 0 |
| **Tatar** `tatar` | tur | 185 | 11.25 | 70 | 6 | 0 | 140 | 20.63 | 4.69 | — | — | — | — | — | — |
| **Vityaz** `vityaz` | rus | 380 | 25.5 | 160 | 13 | 25 | 14 | 1.22 | 0.0 | 2 | 4 | 3 | 160 | 17 | 40 |
| **Winged Hussar** `wingedhussar` | pol | 225 | 26.0 | 130 | 30 | 25 | 14 | 1.88 | 0.0 | 1 | 2 | 5 | 160 | 10 | 30 |

## Cannons (3 options)

| Unit | nations | HP | Time (g-sec) | F | G | I | damage | far (tile) | recharge | peak | sword | bullet | buckshot | arrow | core |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| **Cannon** `cannon` | all | 9000 | 75.0 | 0 | 400 | 400 | 1800 | 40.5 | 10.94 | — | — | — | — | — | — |
| **Frame gun** `framegun` | sco | 3000 | 50.0 | 0 | 300 | 150 | 500 | 33.75 | 2.81 | — | — | — | — | — | — |
| **Multi-barrelled Cannon** `multicannon` | aus,bav,den,eng,fra,hun,net,pie,pol,por,pru,rus,sax,spa,swe,swi,ven | 2000 | 50.0 | 0 | 400 | 250 | 500 | 13.13 | 1.88 | — | — | — | — | — | — |

## Mortars (2 options)

| Unit | nations | HP | Time (g-sec) | F | G | I | damage | far (tile) | recharge | peak | sword | bullet | buckshot | arrow | core |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| **Howitzer** `howitzer` | all | 3000 | 94.0 | 0 | 350 | 300 | 4000 | 26.25 | 18.75 | — | — | — | — | — | — |
| **Bombard** `mortar` | all | 400 | 25.0 | 0 | 75 | 200 | 200 | 48.75 | 7.81 | — | — | — | — | — | — |

## Fishing boats (1 option)

| Unit | nations | HP | Time (g-sec) | F | G | I | damage | far (tile) | recharge | peak | sword | bullet | buckshot | arrow | core |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| **Boat** `fishboat` | all | 300 | 40.0 | 0 | 0 | 0 | — | — | — | — | — | — | — | — | — |

## Warships (8 options)
| Unit | nations | HP | Time (g-sec) | F | G | I | damage | far (tile) | recharge | peak | sword | bullet | buckshot | arrow | core |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| **Ship of the Line** `battleship` | all | 90000 | 390.0 | 0 | 3200 | 700 | 1800 | 36.56 | 0.62 | — | — | — | — | — | — |
| `chaika` | ukr | 25000 | 40.0 | 0 | 600 | 200 | 1000 | 20.63 | 2.34 | — | — | — | — | — | — |
| **Ferry** `ferry` | all | 62000 | 56.0 | 0 | 50 | 100 | — | — | — | — | — | — | — | — | — |
| **Frigate** `frigate` | all | 50000 | 230.0 | 0 | 1100 | 600 | 1800 | 30.94 | 2.34 | — | — | — | — | — | — |
| **Galley** `galley` | all | 35000 | 50.0 | 0 | 900 | 800 | 1000 | 58.13 | 1.56 | — | — | — | — | — | — |
| **Xebec** `xebec` | alg,tur | 65000 | 230.0 | 0 | 1600 | 320 | 1800 | 31.88 | 1.56 | — | — | — | — | — | — |
| **Yacht** `yacht` | all | 31000 | 48.0 | 0 | 450 | 150 | 1000 | 20.63 | 10.94 | — | — | — | — | — | — |
| **Yacht** `yachttur` | tur | 35000 | 48.0 | 0 | 450 | 150 | 0 | 30.94 | 21.88 | — | — | — | — | — | — |

## Officers (5 options)

| Unit | nations | HP | Time (g-sec) | F | G | I | damage | far (tile) | recharge | peak | sword | bullet | buckshot | arrow | core |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| **Officer, 17th century** `officer` | aus,bav,den,eng,fra,hun,net,pie,pol,por,pru,sax,spa,swe,swi,ven | 125 | 10.0 | 50 | 150 | 30 | 30 | 1.22 | 0.0 | 2 | 2 | 5 | 200 | 10 | 30 |
| **Officer, 18th century** `officer18` | aus,bav,den,eng,fra,hun,net,pie,pol,por,pru,rus,sax,spa,swe,swi,ven | 125 | 6.0 | 50 | 200 | 10 | 50 | 1.22 | 0.0 | — | — | — | — | — | — |
| **Commander** `officerrus` | rus | 125 | 12.5 | 100 | 125 | 5 | 40 | 1.22 | 0.0 | 0 | 0 | 0 | 0 | 0 | 0 |
| **Officer** `officersco` | sco | 150 | 10.0 | 130 | 130 | 10 | 40 | 1.22 | 0.0 | 0 | 0 | 0 | 0 | 0 | 0 |
| **Officer** `officertur` | alg,tur | 125 | 7.5 | 50 | 100 | 0 | 30 | 1.22 | 0.0 | 0 | 0 | 0 | 0 | 0 | 0 |

## Drummer, 17th century and bagpipers (5 options)

| Unit | nations | HP | Time (g-sec) | F | G | I | damage | far (tile) | recharge | peak | sword | bullet | buckshot | arrow | core |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| **Bagpiper** `bagpiper` | eng,sco | 150 | 7.0 | 120 | 20 | 0 | — | — | — | — | — | — | — | — | — |
| **Drummer, 17th century** `drummer` | aus,bav,den,eng,fra,hun,net,pie,pol,por,pru,sax,spa,swe,swi,ven | 75 | 5.0 | 60 | 20 | 0 | — | — | — | — | — | — | — | — | — |
| **Drummer, 18th century** `drummer18` | aus,bav,den,fra,hun,net,pie,pol,por,pru,rus,sax,spa,swe,swi,ven | 100 | 6.0 | 50 | 30 | 0 | — | — | — | — | — | — | — | — | — |
| **Drummer, 17th century** `drummerrus` | rus | 100 | 6.0 | 90 | 15 | 0 | — | — | — | — | — | — | — | — | — |
| **Drummer, 17th century** `drummertur` | alg,tur | 50 | 4.0 | 30 | 15 | 0 | — | — | — | — | — | — | — | — | — |

## Priests (4 options)

| Unit | nations | HP | Time (g-sec) | F | G | I | damage | far (tile) | recharge | peak | sword | bullet | buckshot | arrow | core |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| **Mullah** `mullah` | alg,tur | 75 | 15.0 | 30 | 10 | 0 | 15 | 9.38 | 0.0 | — | — | — | — | — | — |
| **Padre** `padre` | pie | 90 | 25.0 | 50 | 40 | 0 | 30 | 7.5 | 0.0 | — | — | — | — | — | — |
| **Pope** `pope` | rus,ukr | 75 | 20.0 | 40 | 20 | 0 | 25 | 6.56 | 0.0 | — | — | — | — | — | — |
| **Priest** `priest` | aus,bav,den,eng,fra,hun,net,pol,por,pru,sax,sco,spa,swe,swi,ven | 100 | 20.0 | 60 | 25 | 0 | 20 | 7.5 | 0.0 | — | — | — | — | — | — |
<a id="разное-и-миссии-1-вариант"></a>
## Miscellaneous and missions (1 option)

| Unit | nations | HP | Time (g-sec) | F | G | I | damage | far (tile) | recharge | peak | sword | bullet | buckshot | arrow | core |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `unitbox` | all | 100 | 3.12 | 100 | 0 | 0 | — | — | — | — | — | — | — | — | — |
