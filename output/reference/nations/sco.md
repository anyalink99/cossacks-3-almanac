# Scotland (`sco`)
_Шотландия_

[← Index](../README.md) · [← Все нации](README.md)

## Кластер

- **Common cluster:** `eur` (mill/sto/mar/tow используют `eur+suffix`)
- **Peasant:** `peasco`
- **Кластерная пехота:** `eur` cluster

## Уникальные юниты (9)

| Юнит | usage | HP | dmg | reload | range (t) |
|---|---|---:|---:|---:|---:|
| **Лучник кланов** / Bow Clansman `archersco` | Archer | 150 | 20 | 3.12 | 18.75 |
| **Рибадекин** / Frame gun `framegun` | Cannon | 3000 | 500 | 2.81 | 33.75 |
| **Лансер** / Lancer `lancersco` | Heavy Cavalry | 320 | 11 | 0.0 | 1.88 |
| **Мушкетер Ковенанта** / Covenanter musketeer `musketeersco` | Shooter | 90 | 12 | 4.69 | 15.94 |
| **Офицер** / Officer `officersco` | Light Infantry | 150 | 40 | 0.0 | 1.22 |
| **Крестьянин** / Peasant `peasco` | Peasant | 60 | 20 | 0.0 | 1.22 |
| **Пикинер Ковенанта** / Covenanter pikeman `pikemansco` | Light Infantry | 100 | 9 | 0.0 | 1.88 |
| **Рейдер** / Raider `raidersco` | Light Cavalry | 280 | 11 | 0.0 | 1.22 |
| **Мечник кланов** / Sword Clansman `swordsmansco` | Light Infantry | 180 | 10 | 0.0 | 1.13 |

## Здания

### Per-nation (10)

> **Жирным** — значения, отличающиеся от baseline (mode по всем нациям) для того же типа здания.

| Здание | HP | Time | cost% | F | W | S | G | I | C | farm | produces |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| **Академия** / Academy `scoaca` | 63000 | 625.0 | 300 | 0 | 1250 | 1100 | 0 | 0 | 0 | 0 | — |
| **Артиллерийское депо** / Artillery Depot `scoart` | 40000 | 245.94 | 200 | 0 | 100 | 1000 | 0 | 0 | 1400 | 0 | cannon, framegun, howitzer, mortar, multicannon |
| **Замок** / Castle `scoba2` | **40000** | **625.0** | **250** | 0 | **640** | **2400** | **2400** | 0 | 0 | **150** | archersco, chasseur, drummer18, grenadier, grenadierbav (+18) |
| **Казарма 17в.** / Barracks, 17th century `scobar` | **30000** | 93.75 | 500 | 0 | 100 | 100 | 500 | 0 | 0 | 150 | archer, archertur, bagpiper, drummer, drummerrus (+25) |
| **Кузница** / Blacksmith `scobla` | 5500 | 93.75 | 400 | 0 | 100 | 30 | 0 | 640 | 0 | 0 | — |
| **Городской центр** / Town Hall `scocen` | 4000 | 156.25 | 300 | 0 | 700 | 700 | 0 | 0 | 0 | 100 | peaaus, peaeng, peapol, pearus, peasco (+3) |
| **Дипломатический центр** / Diplomatic Center `scodip` | 4500 | 312.5 | 100 | 0 | 4900 | 1700 | 0 | 0 | 0 | 0 | archerdip, archerturdip, cossacksichdip, dragoon18dip, grenadierdip (+3) |
| **Дом** / Housing `scohou` | 4000 | 31.25 | 104 | 0 | 100 | 100 | 0 | 0 | 0 | 25 | — |
| **Конюшня** / Stable `scosta` | **25000** | **375.0** | 200 | 0 | **2350** | **0** | **800** | 0 | 0 | 0 | cossackdon, cossackregister, cossacksich, croat, cuirassier (+25) |
| **Собор** / Cathedral `scotem` | 4200 | 156.25 | 300 | 0 | 1000 | 1200 | 0 | 500 | 0 | 0 | mullah, padre, pope, priest |

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
| **Крестьянин** / Peasant `peasco` | 60 | 12.5 | 100 | 0 | 0 | 20 | 1.22 | 0.0 | unique |

### Pikemen 17c

| Юнит | HP | Time | F | G | I | dmg | rng (t) | reload | uniqueness |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| **Пикинер Ковенанта** / Covenanter pikeman `pikemansco` | 100 | 4.0 | 35 | 2 | 0 | 9 | 1.88 | 0.0 | unique |

### Light Infantry

| Юнит | HP | Time | F | G | I | dmg | rng (t) | reload | uniqueness |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| **Легкий пехотинец  (наемник)** / Light Infantryman (mercenary) `lightinfantrydip` | 55 | 1.0 | 25 | 0 | 1 | 5 | 0.94 | 0.0 | common |
| **Рундашир  (наемник)** / Roundshier (mercenary) `roundshierdip` | 180 | 7.0 | 110 | 10 | 0 | 10 | 1.13 | 0.0 | common |
| **Мечник кланов** / Sword Clansman `swordsmansco` | 180 | 7.0 | 110 | 10 | 0 | 10 | 1.13 | 0.0 | unique |

### Musketeers 17c

| Юнит | HP | Time | F | G | I | dmg | rng (t) | reload | uniqueness |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| **Мушкетер Ковенанта** / Covenanter musketeer `musketeersco` | 90 | 7.0 | 55 | 8 | 7 | 12 | 15.94 | 4.69 | unique |

### Grenadiers

| Юнит | HP | Time | F | G | I | dmg | rng (t) | reload | uniqueness |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| **Гренадер  (наемник)** / Grenadier (mercenary) `grenadierdip` | 120 | 6.0 | 80 | 60 | 40 | 18 | 1.5 | 0.0 | common |

### Archers

| Юнит | HP | Time | F | G | I | dmg | rng (t) | reload | uniqueness |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| **Лучник  (наемник)** / Archer (mercenary) `archerdip` | 150 | 6.0 | 80 | 7 | 0 | 20 | 18.75 | 3.12 | common |
| **Лучник кланов** / Bow Clansman `archersco` | 150 | 6.0 | 80 | 7 | 0 | 20 | 18.75 | 3.12 | unique |
| **Турецкий лучник (наемник)** / Turkish archer (mercenary) `archerturdip` | 150 | 6.0 | 80 | 7 | 0 | 20 | 18.75 | 3.12 | common |

### Light Cavalry

| Юнит | HP | Time | F | G | I | dmg | rng (t) | reload | uniqueness |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| **Лансер** / Lancer `lancersco` | 320 | 21.0 | 120 | 6 | 0 | 11 | 1.88 | 0.0 | unique |
| **Легкий кавалерист (наемник)** / Light cavalry (mercenary) `lightcavalrydip` | 225 | 22.5 | 70 | 60 | 7 | 19 | 16.88 | 5.31 | common |
| **Рейдер** / Raider `raidersco` | 280 | 22.5 | 130 | 8 | 2 | 11 | 1.22 | 0.0 | unique |

### Dragoons

| Юнит | HP | Time | F | G | I | dmg | rng (t) | reload | uniqueness |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| **Драгун 18в.  (наемник)** / Dragoon, 18th century (mercenary) `dragoon18dip` | 225 | 22.5 | 70 | 60 | 7 | 19 | 16.88 | 5.31 | common |

### Heavy Cavalry

| Юнит | HP | Time | F | G | I | dmg | rng (t) | reload | uniqueness |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| **Сечевой козак  (наемник)** / Sich Cossack (mercenary) `cossacksichdip` | 250 | 13.5 | 130 | 0 | 2 | 13 | 1.22 | 0.0 | common |

### Cannons

| Юнит | HP | Time | F | G | I | dmg | rng (t) | reload | uniqueness |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| **Пушка** / Cannon `cannon` | 9000 | 75.0 | 0 | 400 | 400 | 1800 | 40.5 | 10.94 | common |
| **Рибадекин** / Frame gun `framegun` | 3000 | 50.0 | 0 | 300 | 150 | 500 | 33.75 | 2.81 | unique |

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
| **Яхта** / Yacht `yacht` | 31000 | 48.0 | 0 | 450 | 150 | 1000 | 20.63 | 10.94 | common |

### Officer

| Юнит | HP | Time | F | G | I | dmg | rng (t) | reload | uniqueness |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| **Офицер** / Officer `officersco` | 150 | 10.0 | 130 | 130 | 10 | 40 | 1.22 | 0.0 | unique |

### Drummer / Bagpiper

| Юнит | HP | Time | F | G | I | dmg | rng (t) | reload | uniqueness |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| **Волынщик** / Bagpiper `bagpiper` | 75 | 6.0 | 50 | 30 | 0 | — | — | — | semi-unique (2n) |

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

## Апгрейды (156)

Полный список — в [05_upgrades.md](../05_upgrades.md).

По местам:

- **aca** (aca): 36
- **bla** (bla): 6
- **sta** (sta): 12
- **bar** (bar): 26
- **ba2** (ba2): 24
- **art** (art): 24
- **cen** (cen): 1
- **mines** (Mine): 18