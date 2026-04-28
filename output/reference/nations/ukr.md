# Ukraine (`ukr`)
_Украина_

[← Index](../README.md) · [← Все нации](README.md)

## Кластер

- **Common cluster:** `rus` (mill/sto/mar/tow используют `rus+suffix`)
- **Peasant:** `peaukr`
- **Кластерная пехота:** `rus` cluster

## Уникальные юниты (6)

| Юнит | usage | HP | dmg | reload | range (t) |
|---|---|---:|---:|---:|---:|
| `chaika` | Frigate | 50000 | 1800 | 2.34 | 30.94 |
| **Реестровый козак** / Register Cossack `cossackregister` | Heavy Cavalry | 300 | 15 | 0.0 | 1.22 |
| **Сечевой козак** / Sich Cossack `cossacksich` | Light Cavalry | 230 | 9 | 0.0 | 1.22 |
| **Гетьман** / Hetman `hetman` | Heavy Cavalry | 300 | 15 | 0.0 | 1.22 |
| **Крестьянин** / Peasant `peaukr` | Peasant | 75 | 20 | 0.0 | 1.22 |
| **Сердюк** / Serdiuk `serdiuk` | Shooter | 70 | — | — | — |

## Здания

### Per-nation (9)

> **Жирным** — значения, отличающиеся от baseline (mode по всем нациям) для того же типа здания.

| Здание | HP | Time | cost% | F | W | S | G | I | C | farm | produces |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| **Академия** / Academy `ukraca` | **65000** | **46.88** | 300 | 0 | **1350** | **1200** | 0 | 0 | 0 | 0 | — |
| **Артиллерийское депо** / Artillery Depot `ukrart` | 40000 | 245.94 | 200 | 0 | **4250** | **4400** | **100** | 0 | 1400 | 0 | cannon, framegun, howitzer, mortar, multicannon |
| **Козацкий дом** / Cossack House `ukrbar` | **20000** | 93.75 | **300** | 0 | **150** | **150** | **0** | 0 | 0 | **75** | archer, archertur, drummer, drummerrus, drummertur (+24) |
| **Кузница** / Blacksmith `ukrbla` | **4500** | **62.5** | 400 | 0 | 100 | 30 | 0 | 640 | 0 | 0 | — |
| **Городской центр** / Town Hall `ukrcen` | **5300** | 156.25 | **400** | 0 | 700 | **0** | 0 | 0 | 0 | **200** | peaaus, peaeng, peapol, pearus, peasco (+3) |
| **Дипломатический центр** / Diplomatic Center `ukrdip` | **5000** | 312.5 | 100 | 0 | **3900** | **2700** | 0 | 0 | 0 | 0 | archerdip, archerturdip, cossacksichdip, dragoon18dip, grenadierdip (+3) |
| **Хижина** / Hut `ukrhou` | **4150** | 31.25 | **105** | 0 | **120** | **0** | 0 | 0 | 0 | 25 | — |
| **Конюшня** / Stable `ukrsta` | **10000** | **156.25** | **300** | 0 | **3200** | **850** | **850** | 0 | 0 | 0 | cossackdon, cossackregister, cossacksich, croat, cuirassier (+25) |
| **Православная церковь** / Orthodox Cathedral `ukrtem` | **5300** | 156.25 | 300 | 0 | **1100** | **1400** | 0 | **300** | 0 | 0 | mullah, padre, pope, priest |

### Common cluster (7)

| Здание | HP | Time | cost% | F | W | S | G | I | C | Доп. |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| **Шахта** / Mine `eurcoa` | 2500 | 93.75 | 0 | 0 | 100 | 100 | 0 | 0 | 0 | produce {"coal": 13}; +5 workers |
| **Шахта** / Mine `eurgol` | 2500 | 93.75 | 0 | 0 | 100 | 100 | 0 | 0 | 0 | produce {"gold": 13}; +5 workers |
| **Шахта** / Mine `euriro` | 2500 | 93.75 | 0 | 0 | 100 | 100 | 0 | 0 | 0 | produce {"iron": 13}; +5 workers |
| **Рынок** / Market `rusmar` | 4000 | 234.38 | 2000 | 0 | 450 | 0 | 0 | 0 | 0 | — |
| **Мельница** / Mill `rusmil` | 15000 | 93.75 | 200 | 0 | 210 | 0 | 0 | 0 | 0 | — |
| **Склад** / Storehouse `russto` | 10000 | 31.25 | 200 | 0 | 50 | 20 | 0 | 0 | 0 | — |
| **Порт** / Shipyard `ukrpor` | 45000 | 1562.5 | 150 | 0 | 2000 | 0 | 0 | 0 | 0 | — |

## Юниты по классам

### Peasant

| Юнит | HP | Time | F | G | I | dmg | rng (t) | reload | uniqueness |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| **Крестьянин** / Peasant `peaukr` | 75 | 11.25 | 100 | 0 | 0 | 20 | 1.22 | 0.0 | unique |

### Light Infantry

| Юнит | HP | Time | F | G | I | dmg | rng (t) | reload | uniqueness |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| **Легкий пехотинец  (наемник)** / Light Infantryman (mercenary) `lightinfantrydip` | 55 | 1.0 | 25 | 0 | 1 | 5 | 0.94 | 0.0 | common |
| **Рундашир  (наемник)** / Roundshier (mercenary) `roundshierdip` | 100 | 4.0 | 20 | 3 | 25 | 6 | 1.13 | 0.0 | common |

### Musketeers 17c

| Юнит | HP | Time | F | G | I | dmg | rng (t) | reload | uniqueness |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| **Сердюк** / Serdiuk `serdiuk` | 70 | 6.0 | 45 | 6 | 5 | — | — | — | unique |

### Grenadiers

| Юнит | HP | Time | F | G | I | dmg | rng (t) | reload | uniqueness |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| **Гренадер  (наемник)** / Grenadier (mercenary) `grenadierdip` | 120 | 6.0 | 80 | 60 | 40 | 18 | 1.5 | 0.0 | common |

### Archers

| Юнит | HP | Time | F | G | I | dmg | rng (t) | reload | uniqueness |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| **Лучник  (наемник)** / Archer (mercenary) `archerdip` | 40 | 1.5 | 20 | 1 | 0 | 15 | 15.0 | 2.34 | common |
| **Турецкий лучник (наемник)** / Turkish archer (mercenary) `archerturdip` | 40 | 1.5 | 20 | 1 | 0 | 15 | 15.0 | 2.34 | common |

### Light Cavalry

| Юнит | HP | Time | F | G | I | dmg | rng (t) | reload | uniqueness |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| **Гетьман** / Hetman `hetman` | 300 | 24.0 | 120 | 10 | 40 | 15 | 1.22 | 0.0 | unique |
| **Легкий кавалерист (наемник)** / Light cavalry (mercenary) `lightcavalrydip` | 220 | 15.0 | 90 | 7 | 5 | 15 | 15.0 | 5.62 | common |

### Dragoons

| Юнит | HP | Time | F | G | I | dmg | rng (t) | reload | uniqueness |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| **Драгун 18в.  (наемник)** / Dragoon, 18th century (mercenary) `dragoon18dip` | 220 | 15.0 | 90 | 7 | 5 | 15 | 15.0 | 5.62 | common |

### Heavy Cavalry

| Юнит | HP | Time | F | G | I | dmg | rng (t) | reload | uniqueness |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| **Реестровый козак** / Register Cossack `cossackregister` | 300 | 24.0 | 120 | 10 | 40 | 15 | 1.22 | 0.0 | unique |
| **Сечевой козак** / Sich Cossack `cossacksich` | 230 | 16.5 | 75 | 2 | 5 | 9 | 1.22 | 0.0 | unique |
| **Сечевой козак  (наемник)** / Sich Cossack (mercenary) `cossacksichdip` | 230 | 16.5 | 75 | 2 | 5 | 9 | 1.22 | 0.0 | common |

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
| `chaika` | 50000 | 230.0 | 0 | 1100 | 600 | 1800 | 30.94 | 2.34 | unique |
| **Транспорт** / Ferry `ferry` | 62000 | 56.0 | 0 | 50 | 100 | — | — | — | common |
| **Галера** / Galley `galley` | 35000 | 50.0 | 0 | 900 | 800 | 100 | 22.5 | 4.69 | common |

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

## Апгрейды (115)

Полный список — в [05_upgrades.md](../05_upgrades.md).

По местам:

- **aca** (aca): 36
- **bla** (bla): 6
- **sta** (sta): 14
- **bar** (bar): 14
- **art** (art): 24
- **cen** (cen): 1
- **mines** (Mine): 18