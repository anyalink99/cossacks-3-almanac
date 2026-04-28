# Austria (`aus`)
_Австрия_

[← Index](../README.md) · [← Все нации](README.md)

## Кластер

- **Common cluster:** `eur` (mill/sto/mar/tow используют `eur+suffix`)
- **Peasant:** `peaaus`
- **Кластерная пехота:** `eur` cluster

## Уникальные юниты (4)

| Юнит | usage | HP | dmg | reload | range (t) |
|---|---|---:|---:|---:|---:|
| **Кроат** / Croat `croat` | Light Cavalry | 260 | 9 | 0.0 | 1.22 |
| **Мушкетер 17в.** / Musketeer, 17th century `musketeeraus` | Shooter | 55 | 12 | 5.0 | 15.0 |
| **Пандур** / Pandur `pandur` | Shooter | 85 | 17 | 4.69 | 16.88 |
| **Рундашир** / Roundshier `roundshier` | Light Infantry | 100 | 6 | 0.0 | 1.13 |

## Здания

### Per-nation (10)

> **Жирным** — значения, отличающиеся от baseline (mode по всем нациям) для того же типа здания.

| Здание | HP | Time | cost% | F | W | S | G | I | C | farm | produces |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| **Академия** / Academy `ausaca` | **65000** | 625.0 | 300 | 0 | 1250 | 1100 | 0 | 0 | 0 | 0 | — |
| **Артиллерийское депо** / Artillery Depot `ausart` | 40000 | 245.94 | 200 | 0 | 100 | 1000 | 0 | 0 | 1400 | 0 | cannon, framegun, howitzer, mortar, multicannon |
| **Казарма 18в.** / Barracks, 18th century `ausba2` | 55000 | 5625.0 | 200 | 0 | 1700 | 2950 | 4000 | 0 | 0 | 250 | archersco, bagpiper, chasseur, drummer18, grenadier (+19) |
| **Казарма 17в.** / Barracks, 17th century `ausbar` | 40000 | 93.75 | 500 | 0 | 100 | 100 | 500 | 0 | 0 | 150 | archer, archertur, drummer, drummerrus, drummertur (+24) |
| **Кузница** / Blacksmith `ausbla` | 5500 | 93.75 | 400 | 0 | 100 | 30 | 0 | 640 | 0 | 0 | — |
| **Городской центр** / Town Hall `auscen` | 4000 | **46.88** | 300 | 0 | 700 | 700 | 0 | 0 | 0 | 100 | peaaus, peaeng, peapol, pearus, peasco (+3) |
| **Дипломатический центр** / Diplomatic Center `ausdip` | 4500 | 312.5 | 100 | 0 | 4900 | 1700 | 0 | 0 | 0 | 0 | archerdip, archerturdip, cossacksichdip, dragoon18dip, grenadierdip (+3) |
| **Дом** / Housing `aushou` | 4000 | 31.25 | 104 | 0 | 100 | 100 | 0 | 0 | 0 | 25 | — |
| **Конюшня** / Stable `aussta` | 20000 | 625.0 | 200 | 0 | 2500 | 100 | 600 | 0 | 0 | 0 | cossackdon, cossackregister, cossacksich, croat, cuirassier (+25) |
| **Собор** / Cathedral `austem` | 4200 | 156.25 | 300 | 0 | 1000 | 1200 | 0 | 500 | 0 | 0 | mullah, padre, pope, priest |

### Common cluster (10)

| Здание | HP | Time | cost% | F | W | S | G | I | C | Доп. |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| **Шахта** / Mine `eurcoa` | 2500 | 93.75 | 0 | 0 | 100 | 100 | 0 | 0 | 0 | produce {"coal": 13}; +5 workers |
| **Шахта** / Mine `eurgol` | 2500 | 93.75 | 0 | 0 | 100 | 100 | 0 | 0 | 0 | produce {"gold": 13}; +5 workers |
| **Шахта** / Mine `euriro` | 2500 | 93.75 | 0 | 0 | 100 | 100 | 0 | 0 | 0 | produce {"iron": 13}; +5 workers |
| **Рынок** / Market `eurmar` | 4000 | 234.38 | 2000 | 0 | 450 | 0 | 0 | 0 | 0 | — |
| **Мельница** / Mill `eurmil` | 20000 | 93.75 | 200 | 0 | 30 | 150 | 0 | 0 | 0 | — |
| **Порт** / Shipyard `eurpor` | 50000 | 1562.5 | 150 | 0 | 1600 | 800 | 0 | 400 | 0 | — |
| **Каменные ворота** / Gate `eursga` | 50000 | 90.0 | 0 | 0 | 0 | 50 | 0 | 0 | 0 | upkeep {"stone": 250} |
| **Склад** / Storehouse `eursto` | 10000 | 31.25 | 150 | 0 | 50 | 20 | 0 | 0 | 0 | — |
| **Стена** / Wall `eurswa` | 50000 | 90.0 | 0 | 0 | 0 | 50 | 0 | 0 | 0 | upkeep {"stone": 250} |
| **Башня** / Tower `eurtow` | 20000 | 1230.31 | 120 | 0 | 100 | 100 | 150 | 0 | 0 | dmg 1000; upkeep {"gold": 500} |

## Юниты по классам

### Peasant

| Юнит | HP | Time | F | G | I | dmg | rng (t) | reload | uniqueness |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| **Крестьянин** / Peasant `peaaus` | 50 | 12.5 | 100 | 0 | 0 | 20 | 1.22 | 0.0 | shared (5n) |

### Pikemen 17c

| Юнит | HP | Time | F | G | I | dmg | rng (t) | reload | uniqueness |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| **Пикинер 17в.** / Pikeman, 17th century `pikeman` | 90 | 4.5 | 25 | 3 | 20 | 8 | 1.88 | 0.0 | shared (13n) |

### Pikemen 18c

| Юнит | HP | Time | F | G | I | dmg | rng (t) | reload | uniqueness |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| **Пикинер 18в.** / Pikeman, 18th century `pikeman18` | 85 | 1.25 | 30 | 2 | 0 | 9 | 1.88 | 0.0 | shared (16n) |

### Light Infantry

| Юнит | HP | Time | F | G | I | dmg | rng (t) | reload | uniqueness |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| **Легкий пехотинец  (наемник)** / Light Infantryman (mercenary) `lightinfantrydip` | 55 | 1.0 | 25 | 0 | 1 | 5 | 0.94 | 0.0 | common |
| **Рундашир** / Roundshier `roundshier` | 100 | 4.0 | 20 | 3 | 25 | 6 | 1.13 | 0.0 | unique |
| **Рундашир  (наемник)** / Roundshier (mercenary) `roundshierdip` | 100 | 4.0 | 20 | 3 | 25 | 6 | 1.13 | 0.0 | common |

### Musketeers 17c

| Юнит | HP | Time | F | G | I | dmg | rng (t) | reload | uniqueness |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| **Мушкетер 17в.** / Musketeer, 17th century `musketeeraus` | 55 | 6.5 | 35 | 9 | 15 | 12 | 15.0 | 5.0 | unique |

### Musketeers 18c

| Юнит | HP | Time | F | G | I | dmg | rng (t) | reload | uniqueness |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| **Мушкетер 18в.** / Musketeer, 18th century `musketeer18` | 100 | 4.5 | 50 | 40 | 40 | 10 | 1.22 | 0.0 | shared (13n) |

### Grenadiers

| Юнит | HP | Time | F | G | I | dmg | rng (t) | reload | uniqueness |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| **Гренадер** / Grenadier `grenadier` | 120 | 6.0 | 80 | 60 | 40 | 18 | 1.5 | 0.0 | shared (13n) |
| **Гренадер  (наемник)** / Grenadier (mercenary) `grenadierdip` | 120 | 6.0 | 80 | 60 | 40 | 18 | 1.5 | 0.0 | common |

### Archers

| Юнит | HP | Time | F | G | I | dmg | rng (t) | reload | uniqueness |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| **Лучник  (наемник)** / Archer (mercenary) `archerdip` | 40 | 1.5 | 20 | 1 | 0 | 15 | 15.0 | 2.34 | common |
| **Турецкий лучник (наемник)** / Turkish archer (mercenary) `archerturdip` | 40 | 1.5 | 20 | 1 | 0 | 15 | 15.0 | 2.34 | common |

### 18c special infantry

| Юнит | HP | Time | F | G | I | dmg | rng (t) | reload | uniqueness |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| **Пандур** / Pandur `pandur` | 85 | 6.0 | 40 | 15 | 10 | 17 | 16.88 | 4.69 | unique |

### Light Cavalry

| Юнит | HP | Time | F | G | I | dmg | rng (t) | reload | uniqueness |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| **Кроат** / Croat `croat` | 260 | 15.75 | 80 | 6 | 2 | 9 | 1.22 | 0.0 | unique |
| **Гусар** / Hussar `hussar` | 230 | 15.0 | 70 | 20 | 2 | 12 | 1.22 | 0.0 | shared (14n) |
| **Легкий кавалерист (наемник)** / Light cavalry (mercenary) `lightcavalrydip` | 225 | 22.5 | 70 | 60 | 7 | 19 | 16.88 | 5.31 | common |

### Dragoons

| Юнит | HP | Time | F | G | I | dmg | rng (t) | reload | uniqueness |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| **Драгун 17в.** / Dragoon, 17th century `dragoon` | 220 | 15.0 | 90 | 7 | 5 | 15 | 15.0 | 5.62 | shared (16n) |
| **Драгун 18в.** / Dragoon, 18th century `dragoon18` | 225 | 22.5 | 70 | 60 | 7 | 19 | 16.88 | 5.31 | shared (13n) |
| **Драгун 18в.  (наемник)** / Dragoon, 18th century (mercenary) `dragoon18dip` | 225 | 22.5 | 70 | 60 | 7 | 19 | 16.88 | 5.31 | common |

### Heavy Cavalry

| Юнит | HP | Time | F | G | I | dmg | rng (t) | reload | uniqueness |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| **Сечевой козак  (наемник)** / Sich Cossack (mercenary) `cossacksichdip` | 250 | 13.5 | 130 | 0 | 2 | 13 | 1.22 | 0.0 | common |
| **Кирасир** / Cuirassier `cuirassier` | 300 | 22.5 | 120 | 35 | 25 | 14 | 1.22 | 0.0 | shared (17n) |
| **Рейтар** / Reiter `reiter` | 300 | 24.0 | 120 | 10 | 40 | 15 | 1.22 | 0.0 | shared (14n) |

### Cannons

| Юнит | HP | Time | F | G | I | dmg | rng (t) | reload | uniqueness |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| **Пушка** / Cannon `cannon` | 9000 | 75.0 | 0 | 400 | 400 | 1800 | 40.5 | 10.94 | common |
| **Многоствольное орудие** / Multi-barrelled Cannon `multicannon` | 2000 | 50.0 | 0 | 400 | 250 | 500 | 13.13 | 1.88 | shared (17n) |

### Mortars

| Юнит | HP | Time | F | G | I | dmg | rng (t) | reload | uniqueness |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| **Гаубица** / Howitzer `howitzer` | 3000 | 94.0 | 0 | 350 | 300 | 4000 | 26.25 | 18.75 | common |
| **Мортира** / Bombard `mortar` | 400 | 25.0 | 0 | 75 | 200 | 200 | 48.75 | 7.81 | common |

### Fishing Boat

| Юнит | HP | Time | F | G | I | dmg | rng (t) | reload | uniqueness |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| **Рыбацкая лодка** / Boat `fishboat` | 300 | 40.0 | 0 | 0 | 0 | — | — | — | common |

### Warships

| Юнит | HP | Time | F | G | I | dmg | rng (t) | reload | uniqueness |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| **Линейный корабль** / Ship of the Line `battleship` | 90000 | 390.0 | 0 | 3200 | 700 | 1800 | 36.56 | 0.62 | common |
| **Транспорт** / Ferry `ferry` | 62000 | 56.0 | 0 | 50 | 100 | — | — | — | common |
| **Фрегат** / Frigate `frigate` | 50000 | 230.0 | 0 | 1100 | 600 | 1800 | 30.94 | 2.34 | common |
| **Галера** / Galley `galley` | 35000 | 50.0 | 0 | 900 | 800 | 100 | 22.5 | 4.69 | common |
| **Яхта** / Yacht `yacht` | 31000 | 48.0 | 0 | 450 | 150 | 1000 | 20.63 | 10.94 | common |

### Officer

| Юнит | HP | Time | F | G | I | dmg | rng (t) | reload | uniqueness |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| **Офицер 17в.** / Officer, 17th century `officer` | 125 | 10.0 | 50 | 150 | 30 | 30 | 1.22 | 0.0 | shared (16n) |
| **Офицер 18в.** / Officer, 18th century `officer18` | 125 | 6.0 | 50 | 200 | 10 | 50 | 1.22 | 0.0 | shared (17n) |

### Drummer / Bagpiper

| Юнит | HP | Time | F | G | I | dmg | rng (t) | reload | uniqueness |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| **Барабанщик 17в.** / Drummer, 17th century `drummer` | 75 | 6.0 | 50 | 30 | 0 | — | — | — | shared (16n) |
| **Барабанщик 18в.** / Drummer, 18th century `drummer18` | 75 | 6.0 | 50 | 30 | 0 | — | — | — | shared (16n) |

### Priest

| Юнит | HP | Time | F | G | I | dmg | rng (t) | reload | uniqueness |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| **Капеллан** / Priest `priest` | 100 | 15.0 | 30 | 10 | 0 | 15 | 9.38 | 0.0 | shared (16n) |

### Misc / mission

| Юнит | HP | Time | F | G | I | dmg | rng (t) | reload | uniqueness |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| `unitbox` | 100 | 3.12 | 100 | 0 | 0 | — | — | — | common |

## Офицеры (11 групп)

Каждый офицер ведёт строй из своих юнитов. Формации стандартные: **LINE / SQUARE / KARE × 15/36/72/120/196/400**.

| officer | drummer | юниты |
|---|---|---|
| `roundshierdip` | `roundshierdip` | roundshierdip |
| `grenadierdip` | `grenadierdip` | grenadierdip |
| `officer` | `drummer` | pikemanpol, roundshier, musketeer, musketeeraus, musketeerpol, musketeerspa, grenadierdip, roundshierdip (+5) |
| `officerrus` | `drummerrus` | pikemanrus, strelet, grenadierdip, roundshierdip |
| `officertur` | `drummertur` | pikemantur, lightinfantry, archer, archertur, jannisary, grenadierdip, roundshierdip |
| `officer18` | `drummer18` | pikeman18, pikeman18swe, pandur, chasseur, highlander, musketeer18, musketeer18pru, grenadier (+11) |
| `officer18` | `bagpiper` | pikeman18, pikeman18swe, pandur, chasseur, highlander, musketeer18, musketeer18pru, grenadier (+7) |
| `officersco` | `bagpiper` | pikemansco, musketeersco, grenadierdip, roundshierdip |
| `serdiuk` | `serdiuk` | serdiuk |
| `archersco` | `archersco` | archersco |
| `swordsmansco` | `swordsmansco` | swordsmansco |

## Апгрейды (249)

Полный список — в [05_upgrades.md](../05_upgrades.md).

По местам:

- **aca** (aca): 36
- **bla** (bla): 6
- **sta** (sta): 66
- **bar** (bar): 38
- **ba2** (ba2): 51
- **art** (art): 24
- **cen** (cen): 1
- **mines** (Mine): 18