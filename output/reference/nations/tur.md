# Turkey (`tur`)
_Турция_

[← Index](../README.md) · [← Все нации](README.md)

## Кластер

- **Common cluster:** `tur` (mill/sto/mar/tow используют `tur+suffix`)
- **Peasant:** `peatur`
- **Кластерная пехота:** `tur` cluster

## Уникальные юниты (6)

| Юнит | usage | HP | dmg | reload | range (t) |
|---|---|---:|---:|---:|---:|
| **Турецкий лучник** / Turkish archer `archertur` | Archer | 65 | 20 | 2.66 | 16.88 |
| **Янычар** / Janissary `jannisary` | Shooter | 65 | 12 | 4.69 | 15.94 |
| **Тяжелый сипах** / Heavy Sipahi `sipahi` | Heavy Cavalry | 360 | 15 | 0.0 | 1.22 |
| **Легкий сипах** / Light Sipahi `spakh` | Heavy Cavalry | 230 | 15 | 0.0 | 1.88 |
| **Татарин** / Tatar `tatar` | Archer | 185 | 15 | 1.56 | 20.63 |
| **Турецкая яхта** / Yacht `yachttur` | Yacht | 31000 | 1000 | 10.94 | 20.63 |

## Здания

### Per-nation (9)

> **Жирным** — значения, отличающиеся от baseline (mode по всем нациям) для того же типа здания.

| Здание | HP | Time | cost% | F | W | S | G | I | C | farm | produces |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| **Минарет** / Minaret `turaca` | **65000** | **156.25** | 300 | 0 | **1450** | 1100 | 0 | 0 | 0 | 0 | — |
| **Артиллерийское депо** / Artillery Depot `turart` | 40000 | 245.94 | 200 | 0 | **500** | **1200** | 0 | 0 | 1400 | 0 | cannon, framegun, howitzer, mortar, multicannon |
| **Казарма** / Barracks `turbar` | **35000** | 93.75 | 500 | 0 | **400** | **400** | **0** | 0 | 0 | **50** | archer, archertur, drummer, drummerrus, drummertur (+24) |
| **Кузница** / Blacksmith `turbla` | **6500** | **109.38** | 400 | 0 | 100 | 30 | 0 | 640 | 0 | 0 | — |
| **Городской центр** / Town Hall `turcen` | 4000 | 156.25 | 300 | 0 | **600** | **500** | 0 | 0 | 0 | 100 | peaaus, peaeng, peapol, pearus, peasco (+3) |
| **Дипломатический центр** / Diplomatic Center `turdip` | **5500** | 312.5 | 100 | 0 | **4600** | **2020** | 0 | 0 | 0 | 0 | archerdip, archerturdip, cossacksichdip, dragoon18dip, grenadierdip (+3) |
| **Дом** / Housing `turhou` | 4000 | 31.25 | **106** | 0 | 100 | 100 | 0 | 0 | 0 | 25 | — |
| **Конюшня** / Stable `tursta` | **55000** | **156.25** | **700** | 0 | **1000** | **2600** | **0** | 0 | 0 | 0 | cossackdon, cossackregister, cossacksich, croat, cuirassier (+25) |
| **Мечеть** / Mosque `turtem` | **5000** | **93.75** | 300 | 0 | 1000 | 1200 | 0 | 500 | 0 | 0 | mullah, padre, pope, priest |

### Common cluster (10)

| Здание | HP | Time | cost% | F | W | S | G | I | C | Доп. |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| **Шахта** / Mine `eurcoa` | 2500 | 93.75 | 0 | 0 | 100 | 100 | 0 | 0 | 0 | produce {"coal": 13}; +5 workers |
| **Шахта** / Mine `eurgol` | 2500 | 93.75 | 0 | 0 | 100 | 100 | 0 | 0 | 0 | produce {"gold": 13}; +5 workers |
| **Шахта** / Mine `euriro` | 2500 | 93.75 | 0 | 0 | 100 | 100 | 0 | 0 | 0 | produce {"iron": 13}; +5 workers |
| **Базар** / Bazaar `turmar` | 4500 | 234.38 | 1500 | 0 | 450 | 150 | 0 | 0 | 0 | — |
| **Мельница** / Mill `turmil` | 20000 | 93.75 | 200 | 0 | 30 | 150 | 0 | 0 | 0 | — |
| **Порт** / Shipyard `turpor` | 40000 | 1562.5 | 150 | 0 | 800 | 800 | 0 | 400 | 0 | — |
| **Каменные ворота** / Gate `tursga` | 50000 | 120.0 | 0 | 0 | 0 | 60 | 0 | 0 | 0 | upkeep {"stone": 150} |
| **Склад** / Storehouse `tursto` | 10000 | 31.25 | 200 | 0 | 30 | 10 | 0 | 0 | 0 | — |
| **Стена** / Wall `turswa` | 50000 | 120.0 | 0 | 0 | 0 | 60 | 0 | 0 | 0 | upkeep {"stone": 150} |
| **Башня** / Tower `turtow` | 22500 | 984.38 | 125 | 0 | 150 | 90 | 100 | 0 | 0 | dmg 1200; upkeep {"gold": 500} |

## Юниты по классам

### Peasant

| Юнит | HP | Time | F | G | I | dmg | rng (t) | reload | uniqueness |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| **Крестьянин** / Peasant `peatur` | 50 | 12.5 | 100 | 0 | 0 | 20 | 1.22 | 0.0 | semi-unique (2n) |

### Pikemen 17c

| Юнит | HP | Time | F | G | I | dmg | rng (t) | reload | uniqueness |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| **Турецкий пикинер** / Ottoman Pikeman `pikemantur` | 95 | 5.5 | 55 | 5 | 0 | 9 | 2.06 | 0.0 | semi-unique (2n) |

### Light Infantry

| Юнит | HP | Time | F | G | I | dmg | rng (t) | reload | uniqueness |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| **Легкий пехотинец** / Light Infantryman `lightinfantry` | 55 | 1.0 | 25 | 0 | 1 | 5 | 0.94 | 0.0 | semi-unique (2n) |
| **Легкий пехотинец  (наемник)** / Light Infantryman (mercenary) `lightinfantrydip` | 55 | 1.0 | 25 | 0 | 1 | 5 | 0.94 | 0.0 | common |
| **Рундашир  (наемник)** / Roundshier (mercenary) `roundshierdip` | 100 | 4.0 | 20 | 3 | 25 | 6 | 1.13 | 0.0 | common |

### Musketeers 17c

| Юнит | HP | Time | F | G | I | dmg | rng (t) | reload | uniqueness |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| **Янычар** / Janissary `jannisary` | 65 | 8.0 | 55 | 13 | 5 | 12 | 15.94 | 4.69 | unique |

### Grenadiers

| Юнит | HP | Time | F | G | I | dmg | rng (t) | reload | uniqueness |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| **Гренадер  (наемник)** / Grenadier (mercenary) `grenadierdip` | 120 | 6.0 | 80 | 60 | 40 | 18 | 1.5 | 0.0 | common |

### Archers

| Юнит | HP | Time | F | G | I | dmg | rng (t) | reload | uniqueness |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| **Лучник  (наемник)** / Archer (mercenary) `archerdip` | 65 | 3.0 | 45 | 4 | 0 | 20 | 16.88 | 2.66 | common |
| **Турецкий лучник** / Turkish archer `archertur` | 65 | 3.0 | 45 | 4 | 0 | 20 | 16.88 | 2.66 | unique |
| **Турецкий лучник (наемник)** / Turkish archer (mercenary) `archerturdip` | 65 | 3.0 | 45 | 4 | 0 | 20 | 16.88 | 2.66 | common |

### Light Cavalry

| Юнит | HP | Time | F | G | I | dmg | rng (t) | reload | uniqueness |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| **Легкий кавалерист (наемник)** / Light cavalry (mercenary) `lightcavalrydip` | 225 | 22.5 | 70 | 60 | 7 | 19 | 16.88 | 5.31 | common |

### Dragoons

| Юнит | HP | Time | F | G | I | dmg | rng (t) | reload | uniqueness |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| **Драгун 18в.  (наемник)** / Dragoon, 18th century (mercenary) `dragoon18dip` | 225 | 22.5 | 70 | 60 | 7 | 19 | 16.88 | 5.31 | common |

### Heavy Cavalry

| Юнит | HP | Time | F | G | I | dmg | rng (t) | reload | uniqueness |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| **Сечевой козак  (наемник)** / Sich Cossack (mercenary) `cossacksichdip` | 250 | 13.5 | 130 | 0 | 2 | 13 | 1.22 | 0.0 | common |
| **Тяжелый сипах** / Heavy Sipahi `sipahi` | 360 | 18.0 | 130 | 20 | 70 | 15 | 1.22 | 0.0 | unique |
| **Легкий сипах** / Light Sipahi `spakh` | 230 | 9.0 | 80 | 6 | 5 | 15 | 1.88 | 0.0 | unique |
| **Татарин** / Tatar `tatar` | 185 | 11.25 | 70 | 6 | 0 | 15 | 20.63 | 1.56 | unique |

### Cannons

| Юнит | HP | Time | F | G | I | dmg | rng (t) | reload | uniqueness |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| **Пушка** / Cannon `cannon` | 9000 | 75.0 | 0 | 400 | 400 | 1800 | 40.5 | 10.94 | common |

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
| **Галера** / Galley `galley` | 35000 | 50.0 | 0 | 900 | 800 | 100 | 22.5 | 4.69 | common |
| **Шебека** / Xebec `xebec` | 65000 | 230.0 | 0 | 1600 | 320 | 1800 | 31.88 | 1.56 | semi-unique (2n) |
| **Турецкая яхта** / Yacht `yachttur` | 31000 | 48.0 | 0 | 450 | 150 | 1000 | 20.63 | 10.94 | unique |

### Officer

| Юнит | HP | Time | F | G | I | dmg | rng (t) | reload | uniqueness |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| **Офицер** / Officer `officertur` | 125 | 7.5 | 50 | 100 | 0 | 30 | 1.22 | 0.0 | semi-unique (2n) |

### Drummer / Bagpiper

| Юнит | HP | Time | F | G | I | dmg | rng (t) | reload | uniqueness |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| **Барабанщик** / Drummer, 17th century `drummertur` | 50 | 4.0 | 30 | 15 | 0 | — | — | — | semi-unique (2n) |

### Priest

| Юнит | HP | Time | F | G | I | dmg | rng (t) | reload | uniqueness |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| **Мулла** / Mullah `mullah` | 100 | 15.0 | 30 | 10 | 0 | 15 | 9.38 | 0.0 | semi-unique (2n) |

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

## Апгрейды (175)

Полный список — в [05_upgrades.md](../05_upgrades.md).

По местам:

- **aca** (aca): 36
- **bla** (bla): 6
- **sta** (sta): 31
- **bar** (bar): 51
- **art** (art): 24
- **cen** (cen): 1
- **mines** (Mine): 18