# Russia (`rus`)
_Россия_

[← Index](../README.md) · [← Все нации](README.md)

## Кластер

- **Common cluster:** `rus` (mill/sto/mar/tow используют `rus+suffix`)
- **Peasant:** `pearus`
- **Кластерная пехота:** `rus` cluster

## Уникальные юниты (7)

| Юнит | usage | HP | dmg | reload | range (t) |
|---|---|---:|---:|---:|---:|
| **Донской козак** / Don Cossack `cossackdon` | Heavy Cavalry | 220 | 13 | 0.0 | 1.88 |
| **Барабанщик 17в.** / Drummer, 17th century `drummerrus` | Light Infantry | 100 | — | — | — |
| **Командир** / Commander `officerrus` | Light Infantry | 125 | 40 | 0.0 | 1.22 |
| **Крепостной** / Serf `pearus` | Peasant | 50 | 20 | 0.0 | 1.22 |
| **Копейщик** / Spearman `pikemanrus` | Light Infantry | 85 | 8 | 0.0 | 1.69 |
| **Стрелец** / Strelets `strelet` | Shooter | 85 | 12 | 4.69 | 13.13 |
| **Витязь** / Vityaz `vityaz` | Heavy Cavalry | 380 | 14 | 0.0 | 1.22 |

## Здания

### Per-nation (10)

> **Жирным** — значения, отличающиеся от baseline (mode по всем нациям) для того же типа здания.

| Здание | HP | Time | cost% | F | W | S | G | I | C | farm | produces |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| **Академия** / Academy `rusaca` | **65000** | **843.75** | 300 | 0 | 1250 | **1300** | 0 | 0 | 0 | 0 | — |
| **Артиллерийское депо** / Artillery Depot `rusart` | 40000 | 245.94 | 200 | 0 | 100 | 1000 | 0 | 0 | 1400 | 0 | cannon, framegun, howitzer, mortar, multicannon |
| **Казарма 18в.** / Barracks, 18th century `rusba2` | 55000 | 5625.0 | 200 | 0 | 1700 | 2950 | 4000 | 0 | 0 | 250 | archersco, bagpiper, chasseur, drummer18, grenadier (+19) |
| **Стрелецкая казарма** / Strelets Barracks `rusbar` | **25000** | **78.12** | **300** | 0 | **200** | **20** | **0** | 0 | 0 | **25** | archer, archertur, drummer, drummerrus, drummertur (+24) |
| **Кузница** / Blacksmith `rusbla` | 5500 | 93.75 | 400 | 0 | 100 | 30 | 0 | 640 | 0 | 0 | — |
| **Городской центр** / Town Hall `ruscen` | **4050** | 156.25 | 300 | 0 | **680** | 700 | 0 | 0 | 0 | **75** | peaaus, peaeng, peapol, pearus, peasco (+3) |
| **Дипломатический центр** / Diplomatic Center `rusdip` | **6500** | 312.5 | 100 | 0 | **7900** | **3700** | 0 | 0 | 0 | 0 | archerdip, archerturdip, cossacksichdip, dragoon18dip, grenadierdip (+3) |
| **Изба** / Izba `rushou` | **5000** | 31.25 | 104 | 0 | **120** | **0** | 0 | 0 | 0 | 25 | — |
| **Конюшня** / Stable `russta` | **25000** | **375.0** | 200 | 0 | **7950** | **0** | **550** | 0 | 0 | 0 | cossackdon, cossackregister, cossacksich, croat, cuirassier (+25) |
| **Православная церковь** / Orthodox Cathedral `rustem` | **4500** | 156.25 | 300 | 0 | **1150** | **1650** | **100** | 500 | 0 | 0 | mullah, padre, pope, priest |

### Common cluster (10)

| Здание | HP | Time | cost% | F | W | S | G | I | C | Доп. |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| **Шахта** / Mine `eurcoa` | 2500 | 93.75 | 0 | 0 | 100 | 100 | 0 | 0 | 0 | produce {"coal": 13}; +5 workers |
| **Шахта** / Mine `eurgol` | 2500 | 93.75 | 0 | 0 | 100 | 100 | 0 | 0 | 0 | produce {"gold": 13}; +5 workers |
| **Шахта** / Mine `euriro` | 2500 | 93.75 | 0 | 0 | 100 | 100 | 0 | 0 | 0 | produce {"iron": 13}; +5 workers |
| **Рынок** / Market `rusmar` | 4000 | 234.38 | 2000 | 0 | 450 | 0 | 0 | 0 | 0 | — |
| **Мельница** / Mill `rusmil` | 15000 | 93.75 | 200 | 0 | 210 | 0 | 0 | 0 | 0 | — |
| **Порт** / Shipyard `ruspor` | 45000 | 1562.5 | 150 | 0 | 1200 | 800 | 0 | 400 | 0 | — |
| **Каменные ворота** / Gate `russga` | 50000 | 200.0 | 0 | 0 | 0 | 60 | 0 | 0 | 0 | upkeep {"stone": 200} |
| **Склад** / Storehouse `russto` | 10000 | 31.25 | 200 | 0 | 50 | 20 | 0 | 0 | 0 | — |
| **Стена** / Wall `russwa` | 50000 | 200.0 | 0 | 0 | 0 | 60 | 0 | 0 | 0 | upkeep {"stone": 200} |
| **Башня** / Tower `rustow` | 21000 | 1476.56 | 125 | 0 | 100 | 100 | 150 | 0 | 0 | dmg 1000; upkeep {"gold": 500} |

## Юниты по классам

### Peasant

| Юнит | HP | Time | F | G | I | dmg | rng (t) | reload | uniqueness |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| **Крепостной** / Serf `pearus` | 50 | 12.5 | 100 | 0 | 0 | 20 | 1.22 | 0.0 | unique |

### Pikemen 17c

| Юнит | HP | Time | F | G | I | dmg | rng (t) | reload | uniqueness |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| **Копейщик** / Spearman `pikemanrus` | 85 | 5.5 | 45 | 4 | 15 | 8 | 1.69 | 0.0 | unique |

### Pikemen 18c

| Юнит | HP | Time | F | G | I | dmg | rng (t) | reload | uniqueness |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| **Пикинер 18в.** / Pikeman, 18th century `pikeman18` | 85 | 1.25 | 30 | 2 | 0 | 9 | 1.88 | 0.0 | shared (16n) |

### Light Infantry

| Юнит | HP | Time | F | G | I | dmg | rng (t) | reload | uniqueness |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| **Легкий пехотинец  (наемник)** / Light Infantryman (mercenary) `lightinfantrydip` | 55 | 1.0 | 25 | 0 | 1 | 5 | 0.94 | 0.0 | common |
| **Рундашир  (наемник)** / Roundshier (mercenary) `roundshierdip` | 100 | 4.0 | 20 | 3 | 25 | 6 | 1.13 | 0.0 | common |

### Musketeers 17c

| Юнит | HP | Time | F | G | I | dmg | rng (t) | reload | uniqueness |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| **Стрелец** / Strelets `strelet` | 85 | 8.5 | 70 | 7 | 9 | 12 | 13.13 | 4.69 | unique |

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

### Light Cavalry

| Юнит | HP | Time | F | G | I | dmg | rng (t) | reload | uniqueness |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| **Гусар** / Hussar `hussar` | 230 | 15.0 | 70 | 20 | 2 | 12 | 1.22 | 0.0 | shared (14n) |
| **Легкий кавалерист (наемник)** / Light cavalry (mercenary) `lightcavalrydip` | 225 | 22.5 | 70 | 60 | 7 | 19 | 16.88 | 5.31 | common |

### Dragoons

| Юнит | HP | Time | F | G | I | dmg | rng (t) | reload | uniqueness |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| **Драгун 18в.** / Dragoon, 18th century `dragoon18` | 225 | 22.5 | 70 | 60 | 7 | 19 | 16.88 | 5.31 | shared (13n) |
| **Драгун 18в.  (наемник)** / Dragoon, 18th century (mercenary) `dragoon18dip` | 225 | 22.5 | 70 | 60 | 7 | 19 | 16.88 | 5.31 | common |

### Heavy Cavalry

| Юнит | HP | Time | F | G | I | dmg | rng (t) | reload | uniqueness |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| **Донской козак** / Don Cossack `cossackdon` | 220 | 13.5 | 100 | 0 | 0 | 13 | 1.88 | 0.0 | unique |
| **Сечевой козак  (наемник)** / Sich Cossack (mercenary) `cossacksichdip` | 250 | 13.5 | 130 | 0 | 2 | 13 | 1.22 | 0.0 | common |
| **Кирасир** / Cuirassier `cuirassier` | 300 | 22.5 | 120 | 35 | 25 | 14 | 1.22 | 0.0 | shared (17n) |
| **Витязь** / Vityaz `vityaz` | 380 | 25.5 | 160 | 13 | 25 | 14 | 1.22 | 0.0 | unique |

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
| **Офицер 18в.** / Officer, 18th century `officer18` | 125 | 6.0 | 50 | 200 | 10 | 50 | 1.22 | 0.0 | shared (17n) |
| **Командир** / Commander `officerrus` | 125 | 12.5 | 100 | 125 | 5 | 40 | 1.22 | 0.0 | unique |

### Drummer / Bagpiper

| Юнит | HP | Time | F | G | I | dmg | rng (t) | reload | uniqueness |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| **Барабанщик 18в.** / Drummer, 18th century `drummer18` | 100 | 6.0 | 90 | 15 | 0 | — | — | — | shared (16n) |
| **Барабанщик 17в.** / Drummer, 17th century `drummerrus` | 100 | 6.0 | 90 | 15 | 0 | — | — | — | unique |

### Priest

| Юнит | HP | Time | F | G | I | dmg | rng (t) | reload | uniqueness |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| **Поп** / Pope `pope` | 100 | 15.0 | 30 | 10 | 0 | 15 | 9.38 | 0.0 | semi-unique (2n) |

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

## Апгрейды (213)

Полный список — в [05_upgrades.md](../05_upgrades.md).

По местам:

- **aca** (aca): 36
- **bla** (bla): 6
- **sta** (sta): 54
- **bar** (bar): 26
- **ba2** (ba2): 39
- **art** (art): 24
- **cen** (cen): 1
- **mines** (Mine): 18