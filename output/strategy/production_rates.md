# Cossacks 3 — Production Rates

Сколько юнитов в минуту даёт **одно здание**, при бесперебойной очереди и без farm/resource ограничений.

**Mechanism** ([units/building.inc/doprogressorders.inc:120-373](C:/Program%20Files%20(x86)/Steam/steamapps/common/Cossacks%203/data/scripts/units/building.inc/doprogressorders.inc)):
- Здание имеет ОДНУ очередь (`orders[0]`). Параллельной постройки **нет**.
- Прогресс: `progress += deltatime / unit.buildtime`. При `progress ≥ 1` юнит спавнится, прогресс сбрасывается.
- Cost списывается **upfront** при старте каждого юнита.
- Если упёрлись в farm cap или unit cap — производство **встало**, прогресс не идёт.

**Формулы:**
- `rate_per_g_sec = 1 / unit.buildtime_sec`
- `rate_per_real_sec_fast = rate_per_g_sec × 1.4`
- `units_per_real_min_fast = rate_per_real_sec_fast × 60`

Сгруппировано по нациям. Для каждого здания — список юнитов которых оно может производить.

## alg

### `algart` — Artillery Depot

| Юнит | имя | buildtime (g-sec) | rate (units/g-min) | rate (units/real-min @ fast) | F | G | I | farm | upkeep food |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `cannon` | Cannon | 75.00 | 0.8 | **1.1** | 0 | 400 | 400 | 1 | — |
| `howitzer` | Howitzer | 94.00 | 0.6 | **0.9** | 0 | 350 | 300 | 1 | — |
| `mortar` | Bombard | 25.00 | 2.4 | **3.4** | 0 | 75 | 200 | 1 | — |

### `algbar` — Barracks

| Юнит | имя | buildtime (g-sec) | rate (units/g-min) | rate (units/real-min @ fast) | F | G | I | farm | upkeep food |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `archer` | Archer | 1.50 | 40.0 | **56.0** | 20 | 1 | 0 | 1 | — |
| `drummertur` | Drummer, 17th century | 4.00 | 15.0 | **21.0** | 30 | 15 | 0 | 1 | — |
| `lightinfantry` | Light Infantryman | 1.00 | 60.0 | **84.0** | 25 | 0 | 1 | 1 | — |
| `officertur` | Officer | 7.50 | 8.0 | **11.2** | 50 | 100 | 0 | 1 | — |
| `pikemantur` | Ottoman Pikeman | 5.50 | 10.9 | **15.3** | 55 | 5 | 0 | 1 | — |

### `algcen` — Town Hall

| Юнит | имя | buildtime (g-sec) | rate (units/g-min) | rate (units/real-min @ fast) | F | G | I | farm | upkeep food |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `peatur` | Peasant | 12.50 | 4.8 | **6.7** | 100 | 0 | 0 | 1 | 28 |

### `algdip` — Diplomatic Center

| Юнит | имя | buildtime (g-sec) | rate (units/g-min) | rate (units/real-min @ fast) | F | G | I | farm | upkeep food |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `archerdip` | Archer (mercenary) | 1.50 | 40.0 | **56.0** | 20 | 1 | 0 | 1 | — |
| `archerturdip` | Turkish archer (mercenary) | 1.50 | 40.0 | **56.0** | 20 | 1 | 0 | 1 | — |
| `cossacksichdip` | Sich Cossack (mercenary) | 16.50 | 3.6 | **5.1** | 75 | 2 | 5 | 1 | — |
| `dragoon18dip` | Dragoon, 18th century (mercenary) | 15.00 | 4.0 | **5.6** | 90 | 7 | 5 | 1 | floor(gc_obj_foodperunit*2) |
| `grenadierdip` | Grenadier (mercenary) | 6.00 | 10.0 | **14.0** | 80 | 60 | 40 | 1 | floor(gc_obj_foodperunit*1.2) |
| `lightcavalrydip` | Light cavalry (mercenary) | 15.00 | 4.0 | **5.6** | 90 | 7 | 5 | 1 | floor(gc_obj_foodperunit*2) |
| `lightinfantrydip` | Light Infantryman (mercenary) | 1.00 | 60.0 | **84.0** | 25 | 0 | 1 | 1 | — |
| `roundshierdip` | Roundshier (mercenary) | 4.00 | 15.0 | **21.0** | 20 | 3 | 25 | 1 | — |

### `algsta` — Stable

| Юнит | имя | buildtime (g-sec) | rate (units/g-min) | rate (units/real-min @ fast) | F | G | I | farm | upkeep food |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `mameluke` | Mameluke | 24.00 | 2.5 | **3.5** | 120 | 10 | 40 | 1 | floor(gc_obj_foodperunit*2.5) |

### `algtem` — Mosque

| Юнит | имя | buildtime (g-sec) | rate (units/g-min) | rate (units/real-min @ fast) | F | G | I | farm | upkeep food |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `mullah` | Mullah | 15.00 | 4.0 | **5.6** | 30 | 10 | 0 | 1 | — |

### `turmil` — Mill

| Юнит | имя | buildtime (g-sec) | rate (units/g-min) | rate (units/real-min @ fast) | F | G | I | farm | upkeep food |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|

### `turpor` — Shipyard

| Юнит | имя | buildtime (g-sec) | rate (units/g-min) | rate (units/real-min @ fast) | F | G | I | farm | upkeep food |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `battleship` | Ship of the Line | 230.00 | 0.3 | **0.4** | 0 | 1100 | 600 | 1 | — |
| `ferry` | Ferry | 56.00 | 1.1 | **1.5** | 0 | 50 | 100 | 1 | — |
| `fishboat` | Boat | 40.00 | 1.5 | **2.1** | 0 | 0 | 0 | 1 | — |
| `galley` | Galley | 50.00 | 1.2 | **1.7** | 0 | 900 | 800 | 1 | — |
| `xebec` | Xebec | 230.00 | 0.3 | **0.4** | 0 | 1100 | 600 | 1 | — |

## aus

### `ausart` — Artillery Depot

| Юнит | имя | buildtime (g-sec) | rate (units/g-min) | rate (units/real-min @ fast) | F | G | I | farm | upkeep food |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `cannon` | Cannon | 75.00 | 0.8 | **1.1** | 0 | 400 | 400 | 1 | — |
| `howitzer` | Howitzer | 94.00 | 0.6 | **0.9** | 0 | 350 | 300 | 1 | — |
| `mortar` | Bombard | 25.00 | 2.4 | **3.4** | 0 | 75 | 200 | 1 | — |
| `multicannon` | Multi-barrelled Cannon | 50.00 | 1.2 | **1.7** | 0 | 400 | 250 | 1 | — |

### `ausba2` — Barracks, 18th century

| Юнит | имя | buildtime (g-sec) | rate (units/g-min) | rate (units/real-min @ fast) | F | G | I | farm | upkeep food |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `drummer18` | Drummer, 18th century | 6.00 | 10.0 | **14.0** | 50 | 30 | 0 | 1 | — |
| `grenadier` | Grenadier | 6.00 | 10.0 | **14.0** | 80 | 60 | 40 | 1 | floor(gc_obj_foodperunit*1.2) |
| `musketeer18` | Musketeer, 18th century | 4.50 | 13.3 | **18.7** | 50 | 40 | 40 | 1 | — |
| `officer18` | Officer, 18th century | 6.00 | 10.0 | **14.0** | 50 | 200 | 10 | 1 | — |
| `pandur` | Pandur | 6.00 | 10.0 | **14.0** | 45 | 6 | 5 | 1 | — |
| `pikeman18` | Pikeman, 18th century | 1.25 | 48.0 | **67.2** | 30 | 2 | 0 | 1 | — |

### `ausbar` — Barracks, 17th century

| Юнит | имя | buildtime (g-sec) | rate (units/g-min) | rate (units/real-min @ fast) | F | G | I | farm | upkeep food |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `drummer` | Drummer, 17th century | 6.00 | 10.0 | **14.0** | 50 | 30 | 0 | 1 | — |
| `musketeeraus` | Musketeer, 17th century | 18.75 | 3.2 | **4.5** | 45 | 6 | 10 | 1 | — |
| `officer` | Officer, 17th century | 10.00 | 6.0 | **8.4** | 50 | 150 | 30 | 1 | — |
| `pikeman` | Pikeman, 17th century | 4.50 | 13.3 | **18.7** | 25 | 3 | 20 | 1 | — |
| `roundshier` | Roundshier | 4.00 | 15.0 | **21.0** | 20 | 3 | 25 | 1 | — |

### `auscen` — Town Hall

| Юнит | имя | buildtime (g-sec) | rate (units/g-min) | rate (units/real-min @ fast) | F | G | I | farm | upkeep food |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `peaaus` | Peasant | 12.50 | 4.8 | **6.7** | 100 | 0 | 0 | 1 | 32 |

### `ausdip` — Diplomatic Center

| Юнит | имя | buildtime (g-sec) | rate (units/g-min) | rate (units/real-min @ fast) | F | G | I | farm | upkeep food |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `archerdip` | Archer (mercenary) | 1.50 | 40.0 | **56.0** | 20 | 1 | 0 | 1 | — |
| `archerturdip` | Turkish archer (mercenary) | 1.50 | 40.0 | **56.0** | 20 | 1 | 0 | 1 | — |
| `cossacksichdip` | Sich Cossack (mercenary) | 16.50 | 3.6 | **5.1** | 75 | 2 | 5 | 1 | — |
| `dragoon18dip` | Dragoon, 18th century (mercenary) | 15.00 | 4.0 | **5.6** | 90 | 7 | 5 | 1 | floor(gc_obj_foodperunit*2) |
| `grenadierdip` | Grenadier (mercenary) | 6.00 | 10.0 | **14.0** | 80 | 60 | 40 | 1 | floor(gc_obj_foodperunit*1.2) |
| `lightcavalrydip` | Light cavalry (mercenary) | 15.00 | 4.0 | **5.6** | 90 | 7 | 5 | 1 | floor(gc_obj_foodperunit*2) |
| `lightinfantrydip` | Light Infantryman (mercenary) | 1.00 | 60.0 | **84.0** | 25 | 0 | 1 | 1 | — |
| `roundshierdip` | Roundshier (mercenary) | 4.00 | 15.0 | **21.0** | 20 | 3 | 25 | 1 | — |

### `aussta` — Stable

| Юнит | имя | buildtime (g-sec) | rate (units/g-min) | rate (units/real-min @ fast) | F | G | I | farm | upkeep food |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `croat` | Croat | 16.50 | 3.6 | **5.1** | 75 | 2 | 5 | 1 | — |
| `cuirassier` | Cuirassier | 24.00 | 2.5 | **3.5** | 120 | 10 | 40 | 1 | floor(gc_obj_foodperunit*2.5) |
| `dragoon` | Dragoon, 17th century | 15.00 | 4.0 | **5.6** | 90 | 7 | 5 | 1 | floor(gc_obj_foodperunit*2) |
| `dragoon18` | Dragoon, 18th century | 15.00 | 4.0 | **5.6** | 90 | 7 | 5 | 1 | floor(gc_obj_foodperunit*2) |
| `hussar` | Hussar | 16.50 | 3.6 | **5.1** | 75 | 2 | 5 | 1 | — |
| `reiter` | Reiter | 24.00 | 2.5 | **3.5** | 120 | 10 | 40 | 1 | floor(gc_obj_foodperunit*2.5) |

### `austem` — Cathedral

| Юнит | имя | buildtime (g-sec) | rate (units/g-min) | rate (units/real-min @ fast) | F | G | I | farm | upkeep food |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `priest` | Priest | 15.00 | 4.0 | **5.6** | 30 | 10 | 0 | 1 | — |

### `eurmil` — Mill

| Юнит | имя | buildtime (g-sec) | rate (units/g-min) | rate (units/real-min @ fast) | F | G | I | farm | upkeep food |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|

### `eurpor` — Shipyard

| Юнит | имя | buildtime (g-sec) | rate (units/g-min) | rate (units/real-min @ fast) | F | G | I | farm | upkeep food |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `battleship` | Ship of the Line | 230.00 | 0.3 | **0.4** | 0 | 1100 | 600 | 1 | — |
| `ferry` | Ferry | 56.00 | 1.1 | **1.5** | 0 | 50 | 100 | 1 | — |
| `fishboat` | Boat | 40.00 | 1.5 | **2.1** | 0 | 0 | 0 | 1 | — |
| `frigate` | Frigate | 230.00 | 0.3 | **0.4** | 0 | 1100 | 600 | 1 | — |
| `galley` | Galley | 50.00 | 1.2 | **1.7** | 0 | 900 | 800 | 1 | — |
| `yacht` | Yacht | 48.00 | 1.2 | **1.8** | 0 | 450 | 150 | 1 | — |

## bav

### `bavart` — Artillery Depot

| Юнит | имя | buildtime (g-sec) | rate (units/g-min) | rate (units/real-min @ fast) | F | G | I | farm | upkeep food |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `cannon` | Cannon | 75.00 | 0.8 | **1.1** | 0 | 400 | 400 | 1 | — |
| `howitzer` | Howitzer | 94.00 | 0.6 | **0.9** | 0 | 350 | 300 | 1 | — |
| `mortar` | Bombard | 25.00 | 2.4 | **3.4** | 0 | 75 | 200 | 1 | — |
| `multicannon` | Multi-barrelled Cannon | 50.00 | 1.2 | **1.7** | 0 | 400 | 250 | 1 | — |

### `bavba2` — Barracks, 18th century

| Юнит | имя | buildtime (g-sec) | rate (units/g-min) | rate (units/real-min @ fast) | F | G | I | farm | upkeep food |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `drummer18` | Drummer, 18th century | 6.00 | 10.0 | **14.0** | 50 | 30 | 0 | 1 | — |
| `grenadierbav` | Grenadier | 6.00 | 10.0 | **14.0** | 80 | 60 | 40 | 1 | floor(gc_obj_foodperunit*1.2) |
| `musketeer18bav` | Musketeer, 18th century | 5.00 | 12.0 | **16.8** | 60 | 55 | 35 | 1 | — |
| `officer18` | Officer, 18th century | 6.00 | 10.0 | **14.0** | 50 | 200 | 10 | 1 | — |
| `pikeman18` | Pikeman, 18th century | 1.25 | 48.0 | **67.2** | 30 | 2 | 0 | 1 | — |

### `bavbar` — Barracks, 17th century

| Юнит | имя | buildtime (g-sec) | rate (units/g-min) | rate (units/real-min @ fast) | F | G | I | farm | upkeep food |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `drummer` | Drummer, 17th century | 6.00 | 10.0 | **14.0** | 50 | 30 | 0 | 1 | — |
| `musketeer` | Musketeer, 17th century | 6.00 | 10.0 | **14.0** | 45 | 6 | 5 | 1 | — |
| `officer` | Officer, 17th century | 10.00 | 6.0 | **8.4** | 50 | 150 | 30 | 1 | — |
| `pikeman` | Pikeman, 17th century | 4.50 | 13.3 | **18.7** | 25 | 3 | 20 | 1 | — |

### `bavcen` — Town Hall

| Юнит | имя | buildtime (g-sec) | rate (units/g-min) | rate (units/real-min @ fast) | F | G | I | farm | upkeep food |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `peaaus` | Peasant | 12.50 | 4.8 | **6.7** | 100 | 0 | 0 | 1 | 32 |

### `bavdip` — Diplomatic Center

| Юнит | имя | buildtime (g-sec) | rate (units/g-min) | rate (units/real-min @ fast) | F | G | I | farm | upkeep food |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `archerdip` | Archer (mercenary) | 1.50 | 40.0 | **56.0** | 20 | 1 | 0 | 1 | — |
| `archerturdip` | Turkish archer (mercenary) | 1.50 | 40.0 | **56.0** | 20 | 1 | 0 | 1 | — |
| `cossacksichdip` | Sich Cossack (mercenary) | 16.50 | 3.6 | **5.1** | 75 | 2 | 5 | 1 | — |
| `dragoon18dip` | Dragoon, 18th century (mercenary) | 15.00 | 4.0 | **5.6** | 90 | 7 | 5 | 1 | floor(gc_obj_foodperunit*2) |
| `grenadierdip` | Grenadier (mercenary) | 6.00 | 10.0 | **14.0** | 80 | 60 | 40 | 1 | floor(gc_obj_foodperunit*1.2) |
| `lightcavalrydip` | Light cavalry (mercenary) | 15.00 | 4.0 | **5.6** | 90 | 7 | 5 | 1 | floor(gc_obj_foodperunit*2) |
| `lightinfantrydip` | Light Infantryman (mercenary) | 1.00 | 60.0 | **84.0** | 25 | 0 | 1 | 1 | — |
| `roundshierdip` | Roundshier (mercenary) | 4.00 | 15.0 | **21.0** | 20 | 3 | 25 | 1 | — |

### `bavsta` — Stable

| Юнит | имя | buildtime (g-sec) | rate (units/g-min) | rate (units/real-min @ fast) | F | G | I | farm | upkeep food |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `cuirassier` | Cuirassier | 24.00 | 2.5 | **3.5** | 120 | 10 | 40 | 1 | floor(gc_obj_foodperunit*2.5) |
| `dragoon` | Dragoon, 17th century | 15.00 | 4.0 | **5.6** | 90 | 7 | 5 | 1 | floor(gc_obj_foodperunit*2) |
| `dragoon18` | Dragoon, 18th century | 15.00 | 4.0 | **5.6** | 90 | 7 | 5 | 1 | floor(gc_obj_foodperunit*2) |
| `hussar` | Hussar | 16.50 | 3.6 | **5.1** | 75 | 2 | 5 | 1 | — |
| `reiter` | Reiter | 24.00 | 2.5 | **3.5** | 120 | 10 | 40 | 1 | floor(gc_obj_foodperunit*2.5) |

### `bavtem` — Cathedral

| Юнит | имя | buildtime (g-sec) | rate (units/g-min) | rate (units/real-min @ fast) | F | G | I | farm | upkeep food |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `priest` | Priest | 15.00 | 4.0 | **5.6** | 30 | 10 | 0 | 1 | — |

### `eurmil` — Mill

| Юнит | имя | buildtime (g-sec) | rate (units/g-min) | rate (units/real-min @ fast) | F | G | I | farm | upkeep food |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|

### `eurpor` — Shipyard

| Юнит | имя | buildtime (g-sec) | rate (units/g-min) | rate (units/real-min @ fast) | F | G | I | farm | upkeep food |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `battleship` | Ship of the Line | 230.00 | 0.3 | **0.4** | 0 | 1100 | 600 | 1 | — |
| `ferry` | Ferry | 56.00 | 1.1 | **1.5** | 0 | 50 | 100 | 1 | — |
| `fishboat` | Boat | 40.00 | 1.5 | **2.1** | 0 | 0 | 0 | 1 | — |
| `frigate` | Frigate | 230.00 | 0.3 | **0.4** | 0 | 1100 | 600 | 1 | — |
| `galley` | Galley | 50.00 | 1.2 | **1.7** | 0 | 900 | 800 | 1 | — |
| `yacht` | Yacht | 48.00 | 1.2 | **1.8** | 0 | 450 | 150 | 1 | — |

## den

### `denart` — Artillery Depot

| Юнит | имя | buildtime (g-sec) | rate (units/g-min) | rate (units/real-min @ fast) | F | G | I | farm | upkeep food |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `cannon` | Cannon | 75.00 | 0.8 | **1.1** | 0 | 400 | 400 | 1 | — |
| `howitzer` | Howitzer | 94.00 | 0.6 | **0.9** | 0 | 350 | 300 | 1 | — |
| `mortar` | Bombard | 25.00 | 2.4 | **3.4** | 0 | 75 | 200 | 1 | — |
| `multicannon` | Multi-barrelled Cannon | 50.00 | 1.2 | **1.7** | 0 | 400 | 250 | 1 | — |

### `denba2` — Barracks, 18th century

| Юнит | имя | buildtime (g-sec) | rate (units/g-min) | rate (units/real-min @ fast) | F | G | I | farm | upkeep food |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `drummer18` | Drummer, 18th century | 6.00 | 10.0 | **14.0** | 50 | 30 | 0 | 1 | — |
| `grenadierden` | Grenadier | 6.00 | 10.0 | **14.0** | 80 | 60 | 40 | 1 | floor(gc_obj_foodperunit*1.2) |
| `musketeer18den` | Musketeer, 18th century | 5.50 | 10.9 | **15.3** | 50 | 80 | 40 | 1 | — |
| `officer18` | Officer, 18th century | 6.00 | 10.0 | **14.0** | 50 | 200 | 10 | 1 | — |
| `pikeman18` | Pikeman, 18th century | 1.25 | 48.0 | **67.2** | 30 | 2 | 0 | 1 | — |

### `denbar` — Barracks, 17th century

| Юнит | имя | buildtime (g-sec) | rate (units/g-min) | rate (units/real-min @ fast) | F | G | I | farm | upkeep food |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `drummer` | Drummer, 17th century | 6.00 | 10.0 | **14.0** | 50 | 30 | 0 | 1 | — |
| `musketeer` | Musketeer, 17th century | 6.00 | 10.0 | **14.0** | 45 | 6 | 5 | 1 | — |
| `officer` | Officer, 17th century | 10.00 | 6.0 | **8.4** | 50 | 150 | 30 | 1 | — |
| `pikeman` | Pikeman, 17th century | 4.50 | 13.3 | **18.7** | 25 | 3 | 20 | 1 | — |

### `dencen` — Town Hall

| Юнит | имя | buildtime (g-sec) | rate (units/g-min) | rate (units/real-min @ fast) | F | G | I | farm | upkeep food |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `peaeng` | Peasant | 12.50 | 4.8 | **6.7** | 100 | 0 | 0 | 1 | 32 |

### `dendip` — Diplomatic Center

| Юнит | имя | buildtime (g-sec) | rate (units/g-min) | rate (units/real-min @ fast) | F | G | I | farm | upkeep food |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `archerdip` | Archer (mercenary) | 1.50 | 40.0 | **56.0** | 20 | 1 | 0 | 1 | — |
| `archerturdip` | Turkish archer (mercenary) | 1.50 | 40.0 | **56.0** | 20 | 1 | 0 | 1 | — |
| `cossacksichdip` | Sich Cossack (mercenary) | 16.50 | 3.6 | **5.1** | 75 | 2 | 5 | 1 | — |
| `dragoon18dip` | Dragoon, 18th century (mercenary) | 15.00 | 4.0 | **5.6** | 90 | 7 | 5 | 1 | floor(gc_obj_foodperunit*2) |
| `grenadierdip` | Grenadier (mercenary) | 6.00 | 10.0 | **14.0** | 80 | 60 | 40 | 1 | floor(gc_obj_foodperunit*1.2) |
| `lightcavalrydip` | Light cavalry (mercenary) | 15.00 | 4.0 | **5.6** | 90 | 7 | 5 | 1 | floor(gc_obj_foodperunit*2) |
| `lightinfantrydip` | Light Infantryman (mercenary) | 1.00 | 60.0 | **84.0** | 25 | 0 | 1 | 1 | — |
| `roundshierdip` | Roundshier (mercenary) | 4.00 | 15.0 | **21.0** | 20 | 3 | 25 | 1 | — |

### `densta` — Stable

| Юнит | имя | buildtime (g-sec) | rate (units/g-min) | rate (units/real-min @ fast) | F | G | I | farm | upkeep food |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `cuirassier` | Cuirassier | 24.00 | 2.5 | **3.5** | 120 | 10 | 40 | 1 | floor(gc_obj_foodperunit*2.5) |
| `dragoon` | Dragoon, 17th century | 15.00 | 4.0 | **5.6** | 90 | 7 | 5 | 1 | floor(gc_obj_foodperunit*2) |
| `dragoon18` | Dragoon, 18th century | 15.00 | 4.0 | **5.6** | 90 | 7 | 5 | 1 | floor(gc_obj_foodperunit*2) |
| `hussar` | Hussar | 16.50 | 3.6 | **5.1** | 75 | 2 | 5 | 1 | — |
| `reiter` | Reiter | 24.00 | 2.5 | **3.5** | 120 | 10 | 40 | 1 | floor(gc_obj_foodperunit*2.5) |

### `dentem` — Cathedral

| Юнит | имя | buildtime (g-sec) | rate (units/g-min) | rate (units/real-min @ fast) | F | G | I | farm | upkeep food |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `priest` | Priest | 15.00 | 4.0 | **5.6** | 30 | 10 | 0 | 1 | — |

### `eurmil` — Mill

| Юнит | имя | buildtime (g-sec) | rate (units/g-min) | rate (units/real-min @ fast) | F | G | I | farm | upkeep food |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|

### `eurpor` — Shipyard

| Юнит | имя | buildtime (g-sec) | rate (units/g-min) | rate (units/real-min @ fast) | F | G | I | farm | upkeep food |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `battleship` | Ship of the Line | 230.00 | 0.3 | **0.4** | 0 | 1100 | 600 | 1 | — |
| `ferry` | Ferry | 56.00 | 1.1 | **1.5** | 0 | 50 | 100 | 1 | — |
| `fishboat` | Boat | 40.00 | 1.5 | **2.1** | 0 | 0 | 0 | 1 | — |
| `frigate` | Frigate | 230.00 | 0.3 | **0.4** | 0 | 1100 | 600 | 1 | — |
| `galley` | Galley | 50.00 | 1.2 | **1.7** | 0 | 900 | 800 | 1 | — |
| `yacht` | Yacht | 48.00 | 1.2 | **1.8** | 0 | 450 | 150 | 1 | — |

## eng

### `engart` — Artillery Depot

| Юнит | имя | buildtime (g-sec) | rate (units/g-min) | rate (units/real-min @ fast) | F | G | I | farm | upkeep food |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `cannon` | Cannon | 75.00 | 0.8 | **1.1** | 0 | 400 | 400 | 1 | — |
| `howitzer` | Howitzer | 94.00 | 0.6 | **0.9** | 0 | 350 | 300 | 1 | — |
| `mortar` | Bombard | 25.00 | 2.4 | **3.4** | 0 | 75 | 200 | 1 | — |
| `multicannon` | Multi-barrelled Cannon | 50.00 | 1.2 | **1.7** | 0 | 400 | 250 | 1 | — |

### `engba2` — Barracks, 18th century

| Юнит | имя | buildtime (g-sec) | rate (units/g-min) | rate (units/real-min @ fast) | F | G | I | farm | upkeep food |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `bagpiper` | Bagpiper | 6.00 | 10.0 | **14.0** | 50 | 30 | 0 | 1 | — |
| `grenadier` | Grenadier | 6.00 | 10.0 | **14.0** | 80 | 60 | 40 | 1 | floor(gc_obj_foodperunit*1.2) |
| `highlander` | Highlander | 6.00 | 10.0 | **14.0** | 45 | 6 | 5 | 1 | — |
| `musketeer18` | Musketeer, 18th century | 4.50 | 13.3 | **18.7** | 50 | 40 | 40 | 1 | — |
| `officer18` | Officer, 18th century | 6.00 | 10.0 | **14.0** | 50 | 200 | 10 | 1 | — |
| `pikeman18` | Pikeman, 18th century | 1.25 | 48.0 | **67.2** | 30 | 2 | 0 | 1 | — |

### `engbar` — Barracks, 17th century

| Юнит | имя | buildtime (g-sec) | rate (units/g-min) | rate (units/real-min @ fast) | F | G | I | farm | upkeep food |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `drummer` | Drummer, 17th century | 6.00 | 10.0 | **14.0** | 50 | 30 | 0 | 1 | — |
| `musketeer` | Musketeer, 17th century | 6.00 | 10.0 | **14.0** | 45 | 6 | 5 | 1 | — |
| `officer` | Officer, 17th century | 10.00 | 6.0 | **8.4** | 50 | 150 | 30 | 1 | — |
| `pikeman` | Pikeman, 17th century | 4.50 | 13.3 | **18.7** | 25 | 3 | 20 | 1 | — |

### `engcen` — Town Hall

| Юнит | имя | buildtime (g-sec) | rate (units/g-min) | rate (units/real-min @ fast) | F | G | I | farm | upkeep food |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `peaeng` | Peasant | 12.50 | 4.8 | **6.7** | 100 | 0 | 0 | 1 | 32 |

### `engdip` — Diplomatic Center

| Юнит | имя | buildtime (g-sec) | rate (units/g-min) | rate (units/real-min @ fast) | F | G | I | farm | upkeep food |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `archerdip` | Archer (mercenary) | 1.50 | 40.0 | **56.0** | 20 | 1 | 0 | 1 | — |
| `archerturdip` | Turkish archer (mercenary) | 1.50 | 40.0 | **56.0** | 20 | 1 | 0 | 1 | — |
| `cossacksichdip` | Sich Cossack (mercenary) | 16.50 | 3.6 | **5.1** | 75 | 2 | 5 | 1 | — |
| `dragoon18dip` | Dragoon, 18th century (mercenary) | 15.00 | 4.0 | **5.6** | 90 | 7 | 5 | 1 | floor(gc_obj_foodperunit*2) |
| `grenadierdip` | Grenadier (mercenary) | 6.00 | 10.0 | **14.0** | 80 | 60 | 40 | 1 | floor(gc_obj_foodperunit*1.2) |
| `lightcavalrydip` | Light cavalry (mercenary) | 15.00 | 4.0 | **5.6** | 90 | 7 | 5 | 1 | floor(gc_obj_foodperunit*2) |
| `lightinfantrydip` | Light Infantryman (mercenary) | 1.00 | 60.0 | **84.0** | 25 | 0 | 1 | 1 | — |
| `roundshierdip` | Roundshier (mercenary) | 4.00 | 15.0 | **21.0** | 20 | 3 | 25 | 1 | — |

### `engsta` — Stable

| Юнит | имя | buildtime (g-sec) | rate (units/g-min) | rate (units/real-min @ fast) | F | G | I | farm | upkeep food |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `cuirassier` | Cuirassier | 24.00 | 2.5 | **3.5** | 120 | 10 | 40 | 1 | floor(gc_obj_foodperunit*2.5) |
| `dragoon` | Dragoon, 17th century | 15.00 | 4.0 | **5.6** | 90 | 7 | 5 | 1 | floor(gc_obj_foodperunit*2) |
| `dragoon18` | Dragoon, 18th century | 15.00 | 4.0 | **5.6** | 90 | 7 | 5 | 1 | floor(gc_obj_foodperunit*2) |
| `hussar` | Hussar | 16.50 | 3.6 | **5.1** | 75 | 2 | 5 | 1 | — |
| `reiter` | Reiter | 24.00 | 2.5 | **3.5** | 120 | 10 | 40 | 1 | floor(gc_obj_foodperunit*2.5) |

### `engtem` — Cathedral

| Юнит | имя | buildtime (g-sec) | rate (units/g-min) | rate (units/real-min @ fast) | F | G | I | farm | upkeep food |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `priest` | Priest | 15.00 | 4.0 | **5.6** | 30 | 10 | 0 | 1 | — |

### `eurmil` — Mill

| Юнит | имя | buildtime (g-sec) | rate (units/g-min) | rate (units/real-min @ fast) | F | G | I | farm | upkeep food |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|

### `eurpor` — Shipyard

| Юнит | имя | buildtime (g-sec) | rate (units/g-min) | rate (units/real-min @ fast) | F | G | I | farm | upkeep food |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `battleship` | Ship of the Line | 230.00 | 0.3 | **0.4** | 0 | 1100 | 600 | 1 | — |
| `ferry` | Ferry | 56.00 | 1.1 | **1.5** | 0 | 50 | 100 | 1 | — |
| `fishboat` | Boat | 40.00 | 1.5 | **2.1** | 0 | 0 | 0 | 1 | — |
| `frigate` | Frigate | 230.00 | 0.3 | **0.4** | 0 | 1100 | 600 | 1 | — |
| `galley` | Galley | 50.00 | 1.2 | **1.7** | 0 | 900 | 800 | 1 | — |
| `yacht` | Yacht | 48.00 | 1.2 | **1.8** | 0 | 450 | 150 | 1 | — |

## fra

### `eurmil` — Mill

| Юнит | имя | buildtime (g-sec) | rate (units/g-min) | rate (units/real-min @ fast) | F | G | I | farm | upkeep food |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|

### `eurpor` — Shipyard

| Юнит | имя | buildtime (g-sec) | rate (units/g-min) | rate (units/real-min @ fast) | F | G | I | farm | upkeep food |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `battleship` | Ship of the Line | 230.00 | 0.3 | **0.4** | 0 | 1100 | 600 | 1 | — |
| `ferry` | Ferry | 56.00 | 1.1 | **1.5** | 0 | 50 | 100 | 1 | — |
| `fishboat` | Boat | 40.00 | 1.5 | **2.1** | 0 | 0 | 0 | 1 | — |
| `frigate` | Frigate | 230.00 | 0.3 | **0.4** | 0 | 1100 | 600 | 1 | — |
| `galley` | Galley | 50.00 | 1.2 | **1.7** | 0 | 900 | 800 | 1 | — |
| `yacht` | Yacht | 48.00 | 1.2 | **1.8** | 0 | 450 | 150 | 1 | — |

### `fraart` — Artillery Depot

| Юнит | имя | buildtime (g-sec) | rate (units/g-min) | rate (units/real-min @ fast) | F | G | I | farm | upkeep food |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `cannon` | Cannon | 75.00 | 0.8 | **1.1** | 0 | 400 | 400 | 1 | — |
| `howitzer` | Howitzer | 94.00 | 0.6 | **0.9** | 0 | 350 | 300 | 1 | — |
| `mortar` | Bombard | 25.00 | 2.4 | **3.4** | 0 | 75 | 200 | 1 | — |
| `multicannon` | Multi-barrelled Cannon | 50.00 | 1.2 | **1.7** | 0 | 400 | 250 | 1 | — |

### `fraba2` — Barracks, 18th century

| Юнит | имя | buildtime (g-sec) | rate (units/g-min) | rate (units/real-min @ fast) | F | G | I | farm | upkeep food |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `chasseur` | Chasseur | 6.00 | 10.0 | **14.0** | 45 | 6 | 5 | 1 | — |
| `drummer18` | Drummer, 18th century | 6.00 | 10.0 | **14.0** | 50 | 30 | 0 | 1 | — |
| `grenadier` | Grenadier | 6.00 | 10.0 | **14.0** | 80 | 60 | 40 | 1 | floor(gc_obj_foodperunit*1.2) |
| `musketeer18` | Musketeer, 18th century | 4.50 | 13.3 | **18.7** | 50 | 40 | 40 | 1 | — |
| `officer18` | Officer, 18th century | 6.00 | 10.0 | **14.0** | 50 | 200 | 10 | 1 | — |
| `pikeman18` | Pikeman, 18th century | 1.25 | 48.0 | **67.2** | 30 | 2 | 0 | 1 | — |

### `frabar` — Barracks, 17th century

| Юнит | имя | buildtime (g-sec) | rate (units/g-min) | rate (units/real-min @ fast) | F | G | I | farm | upkeep food |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `drummer` | Drummer, 17th century | 6.00 | 10.0 | **14.0** | 50 | 30 | 0 | 1 | — |
| `musketeer` | Musketeer, 17th century | 6.00 | 10.0 | **14.0** | 45 | 6 | 5 | 1 | — |
| `officer` | Officer, 17th century | 10.00 | 6.0 | **8.4** | 50 | 150 | 30 | 1 | — |
| `pikeman` | Pikeman, 17th century | 4.50 | 13.3 | **18.7** | 25 | 3 | 20 | 1 | — |

### `fracen` — Town Hall

| Юнит | имя | buildtime (g-sec) | rate (units/g-min) | rate (units/real-min @ fast) | F | G | I | farm | upkeep food |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `peaeng` | Peasant | 12.50 | 4.8 | **6.7** | 100 | 0 | 0 | 1 | 32 |

### `fradip` — Diplomatic Center

| Юнит | имя | buildtime (g-sec) | rate (units/g-min) | rate (units/real-min @ fast) | F | G | I | farm | upkeep food |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `archerdip` | Archer (mercenary) | 1.50 | 40.0 | **56.0** | 20 | 1 | 0 | 1 | — |
| `archerturdip` | Turkish archer (mercenary) | 1.50 | 40.0 | **56.0** | 20 | 1 | 0 | 1 | — |
| `cossacksichdip` | Sich Cossack (mercenary) | 16.50 | 3.6 | **5.1** | 75 | 2 | 5 | 1 | — |
| `dragoon18dip` | Dragoon, 18th century (mercenary) | 15.00 | 4.0 | **5.6** | 90 | 7 | 5 | 1 | floor(gc_obj_foodperunit*2) |
| `grenadierdip` | Grenadier (mercenary) | 6.00 | 10.0 | **14.0** | 80 | 60 | 40 | 1 | floor(gc_obj_foodperunit*1.2) |
| `lightcavalrydip` | Light cavalry (mercenary) | 15.00 | 4.0 | **5.6** | 90 | 7 | 5 | 1 | floor(gc_obj_foodperunit*2) |
| `lightinfantrydip` | Light Infantryman (mercenary) | 1.00 | 60.0 | **84.0** | 25 | 0 | 1 | 1 | — |
| `roundshierdip` | Roundshier (mercenary) | 4.00 | 15.0 | **21.0** | 20 | 3 | 25 | 1 | — |

### `frasta` — Stable

| Юнит | имя | buildtime (g-sec) | rate (units/g-min) | rate (units/real-min @ fast) | F | G | I | farm | upkeep food |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `cuirassier` | Cuirassier | 24.00 | 2.5 | **3.5** | 120 | 10 | 40 | 1 | floor(gc_obj_foodperunit*2.5) |
| `dragoon` | Dragoon, 17th century | 15.00 | 4.0 | **5.6** | 90 | 7 | 5 | 1 | floor(gc_obj_foodperunit*2) |
| `dragoon18fra` | Dragoon, 18th century | 15.00 | 4.0 | **5.6** | 90 | 7 | 5 | 1 | floor(gc_obj_foodperunit*2) |
| `hussar` | Hussar | 16.50 | 3.6 | **5.1** | 75 | 2 | 5 | 1 | — |
| `kingmusketeer` | King's Musketeer | 15.00 | 4.0 | **5.6** | 90 | 7 | 5 | 1 | floor(gc_obj_foodperunit*2) |
| `reiter` | Reiter | 24.00 | 2.5 | **3.5** | 120 | 10 | 40 | 1 | floor(gc_obj_foodperunit*2.5) |

### `fratem` — Cathedral

| Юнит | имя | buildtime (g-sec) | rate (units/g-min) | rate (units/real-min @ fast) | F | G | I | farm | upkeep food |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `priest` | Priest | 15.00 | 4.0 | **5.6** | 30 | 10 | 0 | 1 | — |

## hun

### `eurmil` — Mill

| Юнит | имя | buildtime (g-sec) | rate (units/g-min) | rate (units/real-min @ fast) | F | G | I | farm | upkeep food |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|

### `eurpor` — Shipyard

| Юнит | имя | buildtime (g-sec) | rate (units/g-min) | rate (units/real-min @ fast) | F | G | I | farm | upkeep food |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `battleship` | Ship of the Line | 230.00 | 0.3 | **0.4** | 0 | 1100 | 600 | 1 | — |
| `ferry` | Ferry | 56.00 | 1.1 | **1.5** | 0 | 50 | 100 | 1 | — |
| `fishboat` | Boat | 40.00 | 1.5 | **2.1** | 0 | 0 | 0 | 1 | — |
| `frigate` | Frigate | 230.00 | 0.3 | **0.4** | 0 | 1100 | 600 | 1 | — |
| `galley` | Galley | 50.00 | 1.2 | **1.7** | 0 | 900 | 800 | 1 | — |
| `yacht` | Yacht | 48.00 | 1.2 | **1.8** | 0 | 450 | 150 | 1 | — |

### `hunart` — Artillery Depot

| Юнит | имя | buildtime (g-sec) | rate (units/g-min) | rate (units/real-min @ fast) | F | G | I | farm | upkeep food |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `cannon` | Cannon | 75.00 | 0.8 | **1.1** | 0 | 400 | 400 | 1 | — |
| `howitzer` | Howitzer | 94.00 | 0.6 | **0.9** | 0 | 350 | 300 | 1 | — |
| `mortar` | Bombard | 25.00 | 2.4 | **3.4** | 0 | 75 | 200 | 1 | — |
| `multicannon` | Multi-barrelled Cannon | 50.00 | 1.2 | **1.7** | 0 | 400 | 250 | 1 | — |

### `hunba2` — Barracks, 18th century

| Юнит | имя | buildtime (g-sec) | rate (units/g-min) | rate (units/real-min @ fast) | F | G | I | farm | upkeep food |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `drummer18` | Drummer, 18th century | 6.00 | 10.0 | **14.0** | 50 | 30 | 0 | 1 | — |
| `grenadierhun` | Grenadier | 6.00 | 10.0 | **14.0** | 80 | 60 | 40 | 1 | floor(gc_obj_foodperunit*1.2) |
| `musketeer18` | Musketeer, 18th century | 4.50 | 13.3 | **18.7** | 50 | 40 | 40 | 1 | — |
| `officer18` | Officer, 18th century | 6.00 | 10.0 | **14.0** | 50 | 200 | 10 | 1 | — |
| `pandurhun` | Szekely | 6.00 | 10.0 | **14.0** | 45 | 6 | 5 | 1 | — |
| `pikeman18` | Pikeman, 18th century | 1.25 | 48.0 | **67.2** | 30 | 2 | 0 | 1 | — |

### `hunbar` — Barracks, 17th century

| Юнит | имя | buildtime (g-sec) | rate (units/g-min) | rate (units/real-min @ fast) | F | G | I | farm | upkeep food |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `drummer` | Drummer, 17th century | 6.00 | 10.0 | **14.0** | 50 | 30 | 0 | 1 | — |
| `gauduk` | Hajduk | 6.00 | 10.0 | **14.0** | 45 | 6 | 5 | 1 | — |
| `officer` | Officer, 17th century | 10.00 | 6.0 | **8.4** | 50 | 150 | 30 | 1 | — |
| `pikeman` | Pikeman, 17th century | 4.50 | 13.3 | **18.7** | 25 | 3 | 20 | 1 | — |

### `huncen` — Town Hall

| Юнит | имя | buildtime (g-sec) | rate (units/g-min) | rate (units/real-min @ fast) | F | G | I | farm | upkeep food |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `peapol` | Peasant | 12.50 | 4.8 | **6.7** | 100 | 0 | 0 | 1 | 32 |

### `hundip` — Diplomatic Center

| Юнит | имя | buildtime (g-sec) | rate (units/g-min) | rate (units/real-min @ fast) | F | G | I | farm | upkeep food |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `archerdip` | Archer (mercenary) | 1.50 | 40.0 | **56.0** | 20 | 1 | 0 | 1 | — |
| `archerturdip` | Turkish archer (mercenary) | 1.50 | 40.0 | **56.0** | 20 | 1 | 0 | 1 | — |
| `cossacksichdip` | Sich Cossack (mercenary) | 16.50 | 3.6 | **5.1** | 75 | 2 | 5 | 1 | — |
| `dragoon18dip` | Dragoon, 18th century (mercenary) | 15.00 | 4.0 | **5.6** | 90 | 7 | 5 | 1 | floor(gc_obj_foodperunit*2) |
| `grenadierdip` | Grenadier (mercenary) | 6.00 | 10.0 | **14.0** | 80 | 60 | 40 | 1 | floor(gc_obj_foodperunit*1.2) |
| `lightcavalrydip` | Light cavalry (mercenary) | 15.00 | 4.0 | **5.6** | 90 | 7 | 5 | 1 | floor(gc_obj_foodperunit*2) |
| `lightinfantrydip` | Light Infantryman (mercenary) | 1.00 | 60.0 | **84.0** | 25 | 0 | 1 | 1 | — |
| `roundshierdip` | Roundshier (mercenary) | 4.00 | 15.0 | **21.0** | 20 | 3 | 25 | 1 | — |

### `hunsta` — Stable

| Юнит | имя | buildtime (g-sec) | rate (units/g-min) | rate (units/real-min @ fast) | F | G | I | farm | upkeep food |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `cuirassier` | Cuirassier | 24.00 | 2.5 | **3.5** | 120 | 10 | 40 | 1 | floor(gc_obj_foodperunit*2.5) |
| `dragoon` | Dragoon, 17th century | 15.00 | 4.0 | **5.6** | 90 | 7 | 5 | 1 | floor(gc_obj_foodperunit*2) |
| `hussarhun` | Hussar | 16.50 | 3.6 | **5.1** | 75 | 2 | 5 | 1 | — |
| `lightcavalry` | Light cavalry | 15.00 | 4.0 | **5.6** | 90 | 7 | 5 | 1 | floor(gc_obj_foodperunit*2) |
| `reiter` | Reiter | 24.00 | 2.5 | **3.5** | 120 | 10 | 40 | 1 | floor(gc_obj_foodperunit*2.5) |

### `huntem` — Cathedral

| Юнит | имя | buildtime (g-sec) | rate (units/g-min) | rate (units/real-min @ fast) | F | G | I | farm | upkeep food |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `priest` | Priest | 15.00 | 4.0 | **5.6** | 30 | 10 | 0 | 1 | — |

## net

### `eurmil` — Mill

| Юнит | имя | buildtime (g-sec) | rate (units/g-min) | rate (units/real-min @ fast) | F | G | I | farm | upkeep food |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|

### `eurpor` — Shipyard

| Юнит | имя | buildtime (g-sec) | rate (units/g-min) | rate (units/real-min @ fast) | F | G | I | farm | upkeep food |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `battleship` | Ship of the Line | 230.00 | 0.3 | **0.4** | 0 | 1100 | 600 | 1 | — |
| `ferry` | Ferry | 56.00 | 1.1 | **1.5** | 0 | 50 | 100 | 1 | — |
| `fishboat` | Boat | 40.00 | 1.5 | **2.1** | 0 | 0 | 0 | 1 | — |
| `frigate` | Frigate | 230.00 | 0.3 | **0.4** | 0 | 1100 | 600 | 1 | — |
| `galley` | Galley | 50.00 | 1.2 | **1.7** | 0 | 900 | 800 | 1 | — |
| `yacht` | Yacht | 48.00 | 1.2 | **1.8** | 0 | 450 | 150 | 1 | — |

### `netart` — Artillery Depot

| Юнит | имя | buildtime (g-sec) | rate (units/g-min) | rate (units/real-min @ fast) | F | G | I | farm | upkeep food |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `cannon` | Cannon | 75.00 | 0.8 | **1.1** | 0 | 400 | 400 | 1 | — |
| `howitzer` | Howitzer | 94.00 | 0.6 | **0.9** | 0 | 350 | 300 | 1 | — |
| `mortar` | Bombard | 25.00 | 2.4 | **3.4** | 0 | 75 | 200 | 1 | — |
| `multicannon` | Multi-barrelled Cannon | 50.00 | 1.2 | **1.7** | 0 | 400 | 250 | 1 | — |

### `netba2` — Barracks, 18th century

| Юнит | имя | buildtime (g-sec) | rate (units/g-min) | rate (units/real-min @ fast) | F | G | I | farm | upkeep food |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `drummer18` | Drummer, 18th century | 6.00 | 10.0 | **14.0** | 50 | 30 | 0 | 1 | — |
| `grenadier` | Grenadier | 6.00 | 10.0 | **14.0** | 80 | 60 | 40 | 1 | floor(gc_obj_foodperunit*1.2) |
| `musketeer18` | Musketeer, 18th century | 4.50 | 13.3 | **18.7** | 50 | 40 | 40 | 1 | — |
| `officer18` | Officer, 18th century | 6.00 | 10.0 | **14.0** | 50 | 200 | 10 | 1 | — |
| `pikeman18` | Pikeman, 18th century | 1.25 | 48.0 | **67.2** | 30 | 2 | 0 | 1 | — |

### `netbar` — Barracks, 17th century

| Юнит | имя | buildtime (g-sec) | rate (units/g-min) | rate (units/real-min @ fast) | F | G | I | farm | upkeep food |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `drummer` | Drummer, 17th century | 6.00 | 10.0 | **14.0** | 50 | 30 | 0 | 1 | — |
| `musketeernet` | Musketeer, 17th century | 6.00 | 10.0 | **14.0** | 45 | 6 | 5 | 1 | — |
| `officer` | Officer, 17th century | 10.00 | 6.0 | **8.4** | 50 | 150 | 30 | 1 | — |
| `pikeman` | Pikeman, 17th century | 4.50 | 13.3 | **18.7** | 25 | 3 | 20 | 1 | — |

### `netcen` — Town Hall

| Юнит | имя | buildtime (g-sec) | rate (units/g-min) | rate (units/real-min @ fast) | F | G | I | farm | upkeep food |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `peaeng` | Peasant | 12.50 | 4.8 | **6.7** | 100 | 0 | 0 | 1 | 32 |

### `netdip` — Diplomatic Center

| Юнит | имя | buildtime (g-sec) | rate (units/g-min) | rate (units/real-min @ fast) | F | G | I | farm | upkeep food |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `archerdip` | Archer (mercenary) | 1.50 | 40.0 | **56.0** | 20 | 1 | 0 | 1 | — |
| `archerturdip` | Turkish archer (mercenary) | 1.50 | 40.0 | **56.0** | 20 | 1 | 0 | 1 | — |
| `cossacksichdip` | Sich Cossack (mercenary) | 16.50 | 3.6 | **5.1** | 75 | 2 | 5 | 1 | — |
| `dragoon18dip` | Dragoon, 18th century (mercenary) | 15.00 | 4.0 | **5.6** | 90 | 7 | 5 | 1 | floor(gc_obj_foodperunit*2) |
| `grenadierdip` | Grenadier (mercenary) | 6.00 | 10.0 | **14.0** | 80 | 60 | 40 | 1 | floor(gc_obj_foodperunit*1.2) |
| `lightcavalrydip` | Light cavalry (mercenary) | 15.00 | 4.0 | **5.6** | 90 | 7 | 5 | 1 | floor(gc_obj_foodperunit*2) |
| `lightinfantrydip` | Light Infantryman (mercenary) | 1.00 | 60.0 | **84.0** | 25 | 0 | 1 | 1 | — |
| `roundshierdip` | Roundshier (mercenary) | 4.00 | 15.0 | **21.0** | 20 | 3 | 25 | 1 | — |

### `netsta` — Stable

| Юнит | имя | buildtime (g-sec) | rate (units/g-min) | rate (units/real-min @ fast) | F | G | I | farm | upkeep food |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `cuirassier` | Cuirassier | 24.00 | 2.5 | **3.5** | 120 | 10 | 40 | 1 | floor(gc_obj_foodperunit*2.5) |
| `dragoon` | Dragoon, 17th century | 15.00 | 4.0 | **5.6** | 90 | 7 | 5 | 1 | floor(gc_obj_foodperunit*2) |
| `dragoon18net` | Dragoon, 18th century | 15.00 | 4.0 | **5.6** | 90 | 7 | 5 | 1 | floor(gc_obj_foodperunit*2) |
| `hussar` | Hussar | 16.50 | 3.6 | **5.1** | 75 | 2 | 5 | 1 | — |
| `reiter` | Reiter | 24.00 | 2.5 | **3.5** | 120 | 10 | 40 | 1 | floor(gc_obj_foodperunit*2.5) |

### `nettem` — Cathedral

| Юнит | имя | buildtime (g-sec) | rate (units/g-min) | rate (units/real-min @ fast) | F | G | I | farm | upkeep food |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `priest` | Priest | 15.00 | 4.0 | **5.6** | 30 | 10 | 0 | 1 | — |

## pie

### `eurmil` — Mill

| Юнит | имя | buildtime (g-sec) | rate (units/g-min) | rate (units/real-min @ fast) | F | G | I | farm | upkeep food |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|

### `eurpor` — Shipyard

| Юнит | имя | buildtime (g-sec) | rate (units/g-min) | rate (units/real-min @ fast) | F | G | I | farm | upkeep food |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `battleship` | Ship of the Line | 230.00 | 0.3 | **0.4** | 0 | 1100 | 600 | 1 | — |
| `ferry` | Ferry | 56.00 | 1.1 | **1.5** | 0 | 50 | 100 | 1 | — |
| `fishboat` | Boat | 40.00 | 1.5 | **2.1** | 0 | 0 | 0 | 1 | — |
| `frigate` | Frigate | 230.00 | 0.3 | **0.4** | 0 | 1100 | 600 | 1 | — |
| `galley` | Galley | 50.00 | 1.2 | **1.7** | 0 | 900 | 800 | 1 | — |
| `yacht` | Yacht | 48.00 | 1.2 | **1.8** | 0 | 450 | 150 | 1 | — |

### `pieart` — Artillery Depot

| Юнит | имя | buildtime (g-sec) | rate (units/g-min) | rate (units/real-min @ fast) | F | G | I | farm | upkeep food |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `cannon` | Cannon | 75.00 | 0.8 | **1.1** | 0 | 400 | 400 | 1 | — |
| `howitzer` | Howitzer | 94.00 | 0.6 | **0.9** | 0 | 350 | 300 | 1 | — |
| `mortar` | Bombard | 25.00 | 2.4 | **3.4** | 0 | 75 | 200 | 1 | — |
| `multicannon` | Multi-barrelled Cannon | 50.00 | 1.2 | **1.7** | 0 | 400 | 250 | 1 | — |

### `pieba2` — Barracks, 18th century

| Юнит | имя | buildtime (g-sec) | rate (units/g-min) | rate (units/real-min @ fast) | F | G | I | farm | upkeep food |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `drummer18` | Drummer, 18th century | 6.00 | 10.0 | **14.0** | 50 | 30 | 0 | 1 | — |
| `grenadier` | Grenadier | 6.00 | 10.0 | **14.0** | 80 | 60 | 40 | 1 | floor(gc_obj_foodperunit*1.2) |
| `musketeer18` | Musketeer, 18th century | 4.50 | 13.3 | **18.7** | 50 | 40 | 40 | 1 | — |
| `officer18` | Officer, 18th century | 6.00 | 10.0 | **14.0** | 50 | 200 | 10 | 1 | — |
| `pikeman18` | Pikeman, 18th century | 1.25 | 48.0 | **67.2** | 30 | 2 | 0 | 1 | — |

### `piebar` — Barracks, 17th century

| Юнит | имя | buildtime (g-sec) | rate (units/g-min) | rate (units/real-min @ fast) | F | G | I | farm | upkeep food |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `drummer` | Drummer, 17th century | 6.00 | 10.0 | **14.0** | 50 | 30 | 0 | 1 | — |
| `musketeer` | Musketeer, 17th century | 6.00 | 10.0 | **14.0** | 45 | 6 | 5 | 1 | — |
| `officer` | Officer, 17th century | 10.00 | 6.0 | **8.4** | 50 | 150 | 30 | 1 | — |
| `pikeman` | Pikeman, 17th century | 4.50 | 13.3 | **18.7** | 25 | 3 | 20 | 1 | — |

### `piecen` — Town Hall

| Юнит | имя | buildtime (g-sec) | rate (units/g-min) | rate (units/real-min @ fast) | F | G | I | farm | upkeep food |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `peaspa` | Peasant | 12.50 | 4.8 | **6.7** | 100 | 0 | 0 | 1 | 32 |

### `piedip` — Diplomatic Center

| Юнит | имя | buildtime (g-sec) | rate (units/g-min) | rate (units/real-min @ fast) | F | G | I | farm | upkeep food |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `archerdip` | Archer (mercenary) | 1.50 | 40.0 | **56.0** | 20 | 1 | 0 | 1 | — |
| `archerturdip` | Turkish archer (mercenary) | 1.50 | 40.0 | **56.0** | 20 | 1 | 0 | 1 | — |
| `cossacksichdip` | Sich Cossack (mercenary) | 16.50 | 3.6 | **5.1** | 75 | 2 | 5 | 1 | — |
| `dragoon18dip` | Dragoon, 18th century (mercenary) | 15.00 | 4.0 | **5.6** | 90 | 7 | 5 | 1 | floor(gc_obj_foodperunit*2) |
| `grenadierdip` | Grenadier (mercenary) | 6.00 | 10.0 | **14.0** | 80 | 60 | 40 | 1 | floor(gc_obj_foodperunit*1.2) |
| `lightcavalrydip` | Light cavalry (mercenary) | 15.00 | 4.0 | **5.6** | 90 | 7 | 5 | 1 | floor(gc_obj_foodperunit*2) |
| `lightinfantrydip` | Light Infantryman (mercenary) | 1.00 | 60.0 | **84.0** | 25 | 0 | 1 | 1 | — |
| `roundshierdip` | Roundshier (mercenary) | 4.00 | 15.0 | **21.0** | 20 | 3 | 25 | 1 | — |

### `piesta` — Stable

| Юнит | имя | buildtime (g-sec) | rate (units/g-min) | rate (units/real-min @ fast) | F | G | I | farm | upkeep food |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `cuirassier` | Cuirassier | 24.00 | 2.5 | **3.5** | 120 | 10 | 40 | 1 | floor(gc_obj_foodperunit*2.5) |
| `dragoon` | Dragoon, 17th century | 15.00 | 4.0 | **5.6** | 90 | 7 | 5 | 1 | floor(gc_obj_foodperunit*2) |
| `dragoon18pie` | Dragoon, 18th century | 15.00 | 4.0 | **5.6** | 90 | 7 | 5 | 1 | floor(gc_obj_foodperunit*2) |
| `hussar` | Hussar | 16.50 | 3.6 | **5.1** | 75 | 2 | 5 | 1 | — |
| `reiter` | Reiter | 24.00 | 2.5 | **3.5** | 120 | 10 | 40 | 1 | floor(gc_obj_foodperunit*2.5) |

### `pietem` — Cathedral

| Юнит | имя | buildtime (g-sec) | rate (units/g-min) | rate (units/real-min @ fast) | F | G | I | farm | upkeep food |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `padre` | Padre | 15.00 | 4.0 | **5.6** | 30 | 10 | 0 | 1 | — |

## pol

### `eurmil` — Mill

| Юнит | имя | buildtime (g-sec) | rate (units/g-min) | rate (units/real-min @ fast) | F | G | I | farm | upkeep food |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|

### `eurpor` — Shipyard

| Юнит | имя | buildtime (g-sec) | rate (units/g-min) | rate (units/real-min @ fast) | F | G | I | farm | upkeep food |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `battleship` | Ship of the Line | 230.00 | 0.3 | **0.4** | 0 | 1100 | 600 | 1 | — |
| `ferry` | Ferry | 56.00 | 1.1 | **1.5** | 0 | 50 | 100 | 1 | — |
| `fishboat` | Boat | 40.00 | 1.5 | **2.1** | 0 | 0 | 0 | 1 | — |
| `frigate` | Frigate | 230.00 | 0.3 | **0.4** | 0 | 1100 | 600 | 1 | — |
| `galley` | Galley | 50.00 | 1.2 | **1.7** | 0 | 900 | 800 | 1 | — |
| `yacht` | Yacht | 48.00 | 1.2 | **1.8** | 0 | 450 | 150 | 1 | — |

### `polart` — Artillery Depot

| Юнит | имя | buildtime (g-sec) | rate (units/g-min) | rate (units/real-min @ fast) | F | G | I | farm | upkeep food |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `cannon` | Cannon | 75.00 | 0.8 | **1.1** | 0 | 400 | 400 | 1 | — |
| `howitzer` | Howitzer | 94.00 | 0.6 | **0.9** | 0 | 350 | 300 | 1 | — |
| `mortar` | Bombard | 25.00 | 2.4 | **3.4** | 0 | 75 | 200 | 1 | — |
| `multicannon` | Multi-barrelled Cannon | 50.00 | 1.2 | **1.7** | 0 | 400 | 250 | 1 | — |

### `polba2` — Barracks, 18th century

| Юнит | имя | buildtime (g-sec) | rate (units/g-min) | rate (units/real-min @ fast) | F | G | I | farm | upkeep food |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `drummer18` | Drummer, 18th century | 6.00 | 10.0 | **14.0** | 50 | 30 | 0 | 1 | — |
| `grenadier` | Grenadier | 6.00 | 10.0 | **14.0** | 80 | 60 | 40 | 1 | floor(gc_obj_foodperunit*1.2) |
| `musketeer18` | Musketeer, 18th century | 4.50 | 13.3 | **18.7** | 50 | 40 | 40 | 1 | — |
| `officer18` | Officer, 18th century | 6.00 | 10.0 | **14.0** | 50 | 200 | 10 | 1 | — |
| `pikeman18` | Pikeman, 18th century | 1.25 | 48.0 | **67.2** | 30 | 2 | 0 | 1 | — |

### `polbar` — Barracks, 17th century

| Юнит | имя | buildtime (g-sec) | rate (units/g-min) | rate (units/real-min @ fast) | F | G | I | farm | upkeep food |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `drummer` | Drummer, 17th century | 6.00 | 10.0 | **14.0** | 50 | 30 | 0 | 1 | — |
| `musketeerpol` | Musketeer, 17th century | 6.00 | 10.0 | **14.0** | 45 | 6 | 5 | 1 | — |
| `officer` | Officer, 17th century | 10.00 | 6.0 | **8.4** | 50 | 150 | 30 | 1 | — |
| `pikemanpol` | Pikeman, 17th century | 3.00 | 20.0 | **28.0** | 25 | 1 | 0 | 1 | — |

### `polcen` — Town Hall

| Юнит | имя | buildtime (g-sec) | rate (units/g-min) | rate (units/real-min @ fast) | F | G | I | farm | upkeep food |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `peapol` | Peasant | 12.50 | 4.8 | **6.7** | 100 | 0 | 0 | 1 | 32 |

### `poldip` — Diplomatic Center

| Юнит | имя | buildtime (g-sec) | rate (units/g-min) | rate (units/real-min @ fast) | F | G | I | farm | upkeep food |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `archerdip` | Archer (mercenary) | 1.50 | 40.0 | **56.0** | 20 | 1 | 0 | 1 | — |
| `archerturdip` | Turkish archer (mercenary) | 1.50 | 40.0 | **56.0** | 20 | 1 | 0 | 1 | — |
| `cossacksichdip` | Sich Cossack (mercenary) | 16.50 | 3.6 | **5.1** | 75 | 2 | 5 | 1 | — |
| `dragoon18dip` | Dragoon, 18th century (mercenary) | 15.00 | 4.0 | **5.6** | 90 | 7 | 5 | 1 | floor(gc_obj_foodperunit*2) |
| `grenadierdip` | Grenadier (mercenary) | 6.00 | 10.0 | **14.0** | 80 | 60 | 40 | 1 | floor(gc_obj_foodperunit*1.2) |
| `lightcavalrydip` | Light cavalry (mercenary) | 15.00 | 4.0 | **5.6** | 90 | 7 | 5 | 1 | floor(gc_obj_foodperunit*2) |
| `lightinfantrydip` | Light Infantryman (mercenary) | 1.00 | 60.0 | **84.0** | 25 | 0 | 1 | 1 | — |
| `roundshierdip` | Roundshier (mercenary) | 4.00 | 15.0 | **21.0** | 20 | 3 | 25 | 1 | — |

### `polsta` — Stable

| Юнит | имя | buildtime (g-sec) | rate (units/g-min) | rate (units/real-min @ fast) | F | G | I | farm | upkeep food |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `cuirassier` | Cuirassier | 24.00 | 2.5 | **3.5** | 120 | 10 | 40 | 1 | floor(gc_obj_foodperunit*2.5) |
| `dragoon` | Dragoon, 17th century | 15.00 | 4.0 | **5.6** | 90 | 7 | 5 | 1 | floor(gc_obj_foodperunit*2) |
| `dragoon18` | Dragoon, 18th century | 15.00 | 4.0 | **5.6** | 90 | 7 | 5 | 1 | floor(gc_obj_foodperunit*2) |
| `dragoonpol` | Pospolite ruszenie | 15.00 | 4.0 | **5.6** | 90 | 7 | 5 | 1 | floor(gc_obj_foodperunit*2) |
| `hussar` | Hussar | 16.50 | 3.6 | **5.1** | 75 | 2 | 5 | 1 | — |
| `reiterpol` | Light Reiter | 24.00 | 2.5 | **3.5** | 120 | 10 | 40 | 1 | floor(gc_obj_foodperunit*2.5) |
| `wingedhussar` | Winged Hussar | 16.50 | 3.6 | **5.1** | 75 | 2 | 5 | 1 | — |

### `poltem` — Cathedral

| Юнит | имя | buildtime (g-sec) | rate (units/g-min) | rate (units/real-min @ fast) | F | G | I | farm | upkeep food |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `priest` | Priest | 15.00 | 4.0 | **5.6** | 30 | 10 | 0 | 1 | — |

## por

### `eurmil` — Mill

| Юнит | имя | buildtime (g-sec) | rate (units/g-min) | rate (units/real-min @ fast) | F | G | I | farm | upkeep food |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|

### `porart` — Artillery Depot

| Юнит | имя | buildtime (g-sec) | rate (units/g-min) | rate (units/real-min @ fast) | F | G | I | farm | upkeep food |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `cannon` | Cannon | 75.00 | 0.8 | **1.1** | 0 | 400 | 400 | 1 | — |
| `howitzer` | Howitzer | 94.00 | 0.6 | **0.9** | 0 | 350 | 300 | 1 | — |
| `mortar` | Bombard | 25.00 | 2.4 | **3.4** | 0 | 75 | 200 | 1 | — |
| `multicannon` | Multi-barrelled Cannon | 50.00 | 1.2 | **1.7** | 0 | 400 | 250 | 1 | — |

### `porba2` — Barracks, 18th century

| Юнит | имя | buildtime (g-sec) | rate (units/g-min) | rate (units/real-min @ fast) | F | G | I | farm | upkeep food |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `drummer18` | Drummer, 18th century | 6.00 | 10.0 | **14.0** | 50 | 30 | 0 | 1 | — |
| `grenadier` | Grenadier | 6.00 | 10.0 | **14.0** | 80 | 60 | 40 | 1 | floor(gc_obj_foodperunit*1.2) |
| `jagerpor` | Volunteer | 6.00 | 10.0 | **14.0** | 45 | 6 | 5 | 1 | — |
| `musketeer18` | Musketeer, 18th century | 4.50 | 13.3 | **18.7** | 50 | 40 | 40 | 1 | — |
| `officer18` | Officer, 18th century | 6.00 | 10.0 | **14.0** | 50 | 200 | 10 | 1 | — |
| `pikeman18` | Pikeman, 18th century | 1.25 | 48.0 | **67.2** | 30 | 2 | 0 | 1 | — |

### `porbar` — Barracks, 17th century

| Юнит | имя | buildtime (g-sec) | rate (units/g-min) | rate (units/real-min @ fast) | F | G | I | farm | upkeep food |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `drummer` | Drummer, 17th century | 6.00 | 10.0 | **14.0** | 50 | 30 | 0 | 1 | — |
| `musketeer` | Musketeer, 17th century | 6.00 | 10.0 | **14.0** | 45 | 6 | 5 | 1 | — |
| `officer` | Officer, 17th century | 10.00 | 6.0 | **8.4** | 50 | 150 | 30 | 1 | — |
| `pikemanpor` | Pikeman, 17th century | 4.00 | 15.0 | **21.0** | 40 | 4 | 5 | 1 | — |

### `porcen` — Town Hall

| Юнит | имя | buildtime (g-sec) | rate (units/g-min) | rate (units/real-min @ fast) | F | G | I | farm | upkeep food |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `peaspa` | Peasant | 12.50 | 4.8 | **6.7** | 100 | 0 | 0 | 1 | 32 |

### `pordip` — Diplomatic Center

| Юнит | имя | buildtime (g-sec) | rate (units/g-min) | rate (units/real-min @ fast) | F | G | I | farm | upkeep food |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `archerdip` | Archer (mercenary) | 1.50 | 40.0 | **56.0** | 20 | 1 | 0 | 1 | — |
| `archerturdip` | Turkish archer (mercenary) | 1.50 | 40.0 | **56.0** | 20 | 1 | 0 | 1 | — |
| `cossacksichdip` | Sich Cossack (mercenary) | 16.50 | 3.6 | **5.1** | 75 | 2 | 5 | 1 | — |
| `dragoon18dip` | Dragoon, 18th century (mercenary) | 15.00 | 4.0 | **5.6** | 90 | 7 | 5 | 1 | floor(gc_obj_foodperunit*2) |
| `grenadierdip` | Grenadier (mercenary) | 6.00 | 10.0 | **14.0** | 80 | 60 | 40 | 1 | floor(gc_obj_foodperunit*1.2) |
| `lightcavalrydip` | Light cavalry (mercenary) | 15.00 | 4.0 | **5.6** | 90 | 7 | 5 | 1 | floor(gc_obj_foodperunit*2) |
| `lightinfantrydip` | Light Infantryman (mercenary) | 1.00 | 60.0 | **84.0** | 25 | 0 | 1 | 1 | — |
| `roundshierdip` | Roundshier (mercenary) | 4.00 | 15.0 | **21.0** | 20 | 3 | 25 | 1 | — |

### `porpor` — Shipyard

| Юнит | имя | buildtime (g-sec) | rate (units/g-min) | rate (units/real-min @ fast) | F | G | I | farm | upkeep food |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `battleship` | Ship of the Line | 230.00 | 0.3 | **0.4** | 0 | 1100 | 600 | 1 | — |
| `ferry` | Ferry | 56.00 | 1.1 | **1.5** | 0 | 50 | 100 | 1 | — |
| `fishboat` | Boat | 40.00 | 1.5 | **2.1** | 0 | 0 | 0 | 1 | — |
| `frigate` | Frigate | 230.00 | 0.3 | **0.4** | 0 | 1100 | 600 | 1 | — |
| `galley` | Galley | 50.00 | 1.2 | **1.7** | 0 | 900 | 800 | 1 | — |
| `yacht` | Yacht | 48.00 | 1.2 | **1.8** | 0 | 450 | 150 | 1 | — |

### `porsta` — Stable

| Юнит | имя | buildtime (g-sec) | rate (units/g-min) | rate (units/real-min @ fast) | F | G | I | farm | upkeep food |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `cuirassier` | Cuirassier | 24.00 | 2.5 | **3.5** | 120 | 10 | 40 | 1 | floor(gc_obj_foodperunit*2.5) |
| `dragoon` | Dragoon, 17th century | 15.00 | 4.0 | **5.6** | 90 | 7 | 5 | 1 | floor(gc_obj_foodperunit*2) |
| `dragoon18` | Dragoon, 18th century | 15.00 | 4.0 | **5.6** | 90 | 7 | 5 | 1 | floor(gc_obj_foodperunit*2) |
| `hussar` | Hussar | 16.50 | 3.6 | **5.1** | 75 | 2 | 5 | 1 | — |
| `reiter` | Reiter | 24.00 | 2.5 | **3.5** | 120 | 10 | 40 | 1 | floor(gc_obj_foodperunit*2.5) |

### `portem` — Cathedral

| Юнит | имя | buildtime (g-sec) | rate (units/g-min) | rate (units/real-min @ fast) | F | G | I | farm | upkeep food |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `priest` | Priest | 15.00 | 4.0 | **5.6** | 30 | 10 | 0 | 1 | — |

## pru

### `eurmil` — Mill

| Юнит | имя | buildtime (g-sec) | rate (units/g-min) | rate (units/real-min @ fast) | F | G | I | farm | upkeep food |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|

### `eurpor` — Shipyard

| Юнит | имя | buildtime (g-sec) | rate (units/g-min) | rate (units/real-min @ fast) | F | G | I | farm | upkeep food |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `battleship` | Ship of the Line | 230.00 | 0.3 | **0.4** | 0 | 1100 | 600 | 1 | — |
| `ferry` | Ferry | 56.00 | 1.1 | **1.5** | 0 | 50 | 100 | 1 | — |
| `fishboat` | Boat | 40.00 | 1.5 | **2.1** | 0 | 0 | 0 | 1 | — |
| `frigate` | Frigate | 230.00 | 0.3 | **0.4** | 0 | 1100 | 600 | 1 | — |
| `galley` | Galley | 50.00 | 1.2 | **1.7** | 0 | 900 | 800 | 1 | — |
| `yacht` | Yacht | 48.00 | 1.2 | **1.8** | 0 | 450 | 150 | 1 | — |

### `pruart` — Artillery Depot

| Юнит | имя | buildtime (g-sec) | rate (units/g-min) | rate (units/real-min @ fast) | F | G | I | farm | upkeep food |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `cannon` | Cannon | 75.00 | 0.8 | **1.1** | 0 | 400 | 400 | 1 | — |
| `howitzer` | Howitzer | 94.00 | 0.6 | **0.9** | 0 | 350 | 300 | 1 | — |
| `mortar` | Bombard | 25.00 | 2.4 | **3.4** | 0 | 75 | 200 | 1 | — |
| `multicannon` | Multi-barrelled Cannon | 50.00 | 1.2 | **1.7** | 0 | 400 | 250 | 1 | — |

### `pruba2` — Barracks, 18th century

| Юнит | имя | buildtime (g-sec) | rate (units/g-min) | rate (units/real-min @ fast) | F | G | I | farm | upkeep food |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `drummer18` | Drummer, 18th century | 6.00 | 10.0 | **14.0** | 50 | 30 | 0 | 1 | — |
| `grenadier` | Grenadier | 6.00 | 10.0 | **14.0** | 80 | 60 | 40 | 1 | floor(gc_obj_foodperunit*1.2) |
| `grenadierpru` | Grenadier | 6.00 | 10.0 | **14.0** | 80 | 60 | 40 | 1 | floor(gc_obj_foodperunit*1.2) |
| `musketeer18pru` | Musketeer, 18th century | 6.00 | 10.0 | **14.0** | 70 | 80 | 40 | 1 | — |
| `officer18` | Officer, 18th century | 6.00 | 10.0 | **14.0** | 50 | 200 | 10 | 1 | — |
| `pikeman18` | Pikeman, 18th century | 1.25 | 48.0 | **67.2** | 30 | 2 | 0 | 1 | — |

### `prubar` — Barracks, 17th century

| Юнит | имя | buildtime (g-sec) | rate (units/g-min) | rate (units/real-min @ fast) | F | G | I | farm | upkeep food |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `drummer` | Drummer, 17th century | 6.00 | 10.0 | **14.0** | 50 | 30 | 0 | 1 | — |
| `musketeer` | Musketeer, 17th century | 6.00 | 10.0 | **14.0** | 45 | 6 | 5 | 1 | — |
| `officer` | Officer, 17th century | 10.00 | 6.0 | **8.4** | 50 | 150 | 30 | 1 | — |
| `pikeman` | Pikeman, 17th century | 4.50 | 13.3 | **18.7** | 25 | 3 | 20 | 1 | — |

### `prucen` — Town Hall

| Юнит | имя | buildtime (g-sec) | rate (units/g-min) | rate (units/real-min @ fast) | F | G | I | farm | upkeep food |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `peaaus` | Peasant | 12.50 | 4.8 | **6.7** | 100 | 0 | 0 | 1 | 32 |

### `prudip` — Diplomatic Center

| Юнит | имя | buildtime (g-sec) | rate (units/g-min) | rate (units/real-min @ fast) | F | G | I | farm | upkeep food |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `archerdip` | Archer (mercenary) | 1.50 | 40.0 | **56.0** | 20 | 1 | 0 | 1 | — |
| `archerturdip` | Turkish archer (mercenary) | 1.50 | 40.0 | **56.0** | 20 | 1 | 0 | 1 | — |
| `cossacksichdip` | Sich Cossack (mercenary) | 16.50 | 3.6 | **5.1** | 75 | 2 | 5 | 1 | — |
| `dragoon18dip` | Dragoon, 18th century (mercenary) | 15.00 | 4.0 | **5.6** | 90 | 7 | 5 | 1 | floor(gc_obj_foodperunit*2) |
| `grenadierdip` | Grenadier (mercenary) | 6.00 | 10.0 | **14.0** | 80 | 60 | 40 | 1 | floor(gc_obj_foodperunit*1.2) |
| `lightcavalrydip` | Light cavalry (mercenary) | 15.00 | 4.0 | **5.6** | 90 | 7 | 5 | 1 | floor(gc_obj_foodperunit*2) |
| `lightinfantrydip` | Light Infantryman (mercenary) | 1.00 | 60.0 | **84.0** | 25 | 0 | 1 | 1 | — |
| `roundshierdip` | Roundshier (mercenary) | 4.00 | 15.0 | **21.0** | 20 | 3 | 25 | 1 | — |

### `prusta` — Stable

| Юнит | имя | buildtime (g-sec) | rate (units/g-min) | rate (units/real-min @ fast) | F | G | I | farm | upkeep food |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `cuirassier` | Cuirassier | 24.00 | 2.5 | **3.5** | 120 | 10 | 40 | 1 | floor(gc_obj_foodperunit*2.5) |
| `dragoon` | Dragoon, 17th century | 15.00 | 4.0 | **5.6** | 90 | 7 | 5 | 1 | floor(gc_obj_foodperunit*2) |
| `dragoon18` | Dragoon, 18th century | 15.00 | 4.0 | **5.6** | 90 | 7 | 5 | 1 | floor(gc_obj_foodperunit*2) |
| `hussarpru` | Hussar | 16.50 | 3.6 | **5.1** | 75 | 2 | 5 | 1 | — |
| `reiter` | Reiter | 24.00 | 2.5 | **3.5** | 120 | 10 | 40 | 1 | floor(gc_obj_foodperunit*2.5) |

### `prutem` — Cathedral

| Юнит | имя | buildtime (g-sec) | rate (units/g-min) | rate (units/real-min @ fast) | F | G | I | farm | upkeep food |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `priest` | Priest | 15.00 | 4.0 | **5.6** | 30 | 10 | 0 | 1 | — |

## rus

### `rusart` — Artillery Depot

| Юнит | имя | buildtime (g-sec) | rate (units/g-min) | rate (units/real-min @ fast) | F | G | I | farm | upkeep food |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `cannon` | Cannon | 75.00 | 0.8 | **1.1** | 0 | 400 | 400 | 1 | — |
| `howitzer` | Howitzer | 94.00 | 0.6 | **0.9** | 0 | 350 | 300 | 1 | — |
| `mortar` | Bombard | 25.00 | 2.4 | **3.4** | 0 | 75 | 200 | 1 | — |
| `multicannon` | Multi-barrelled Cannon | 50.00 | 1.2 | **1.7** | 0 | 400 | 250 | 1 | — |

### `rusba2` — Barracks, 18th century

| Юнит | имя | buildtime (g-sec) | rate (units/g-min) | rate (units/real-min @ fast) | F | G | I | farm | upkeep food |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `drummer18` | Drummer, 18th century | 6.00 | 10.0 | **14.0** | 90 | 15 | 0 | 1 | — |
| `grenadier` | Grenadier | 6.00 | 10.0 | **14.0** | 80 | 60 | 40 | 1 | floor(gc_obj_foodperunit*1.2) |
| `musketeer18` | Musketeer, 18th century | 4.50 | 13.3 | **18.7** | 50 | 40 | 40 | 1 | — |
| `officer18` | Officer, 18th century | 6.00 | 10.0 | **14.0** | 50 | 200 | 10 | 1 | — |
| `pikeman18` | Pikeman, 18th century | 1.25 | 48.0 | **67.2** | 30 | 2 | 0 | 1 | — |

### `rusbar` — Strelets Barracks

| Юнит | имя | buildtime (g-sec) | rate (units/g-min) | rate (units/real-min @ fast) | F | G | I | farm | upkeep food |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `drummerrus` | Drummer, 17th century | 6.00 | 10.0 | **14.0** | 90 | 15 | 0 | 1 | — |
| `officerrus` | Commander | 12.50 | 4.8 | **6.7** | 100 | 125 | 5 | 1 | — |
| `pikemanrus` | Spearman | 5.50 | 10.9 | **15.3** | 45 | 4 | 15 | 1 | — |
| `strelet` | Strelets | 18.75 | 3.2 | **4.5** | 45 | 6 | 10 | 1 | — |

### `ruscen` — Town Hall

| Юнит | имя | buildtime (g-sec) | rate (units/g-min) | rate (units/real-min @ fast) | F | G | I | farm | upkeep food |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `pearus` | Serf | 12.50 | 4.8 | **6.7** | 100 | 0 | 0 | 1 | 26 |

### `rusdip` — Diplomatic Center

| Юнит | имя | buildtime (g-sec) | rate (units/g-min) | rate (units/real-min @ fast) | F | G | I | farm | upkeep food |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `archerdip` | Archer (mercenary) | 1.50 | 40.0 | **56.0** | 20 | 1 | 0 | 1 | — |
| `archerturdip` | Turkish archer (mercenary) | 1.50 | 40.0 | **56.0** | 20 | 1 | 0 | 1 | — |
| `cossacksichdip` | Sich Cossack (mercenary) | 16.50 | 3.6 | **5.1** | 75 | 2 | 5 | 1 | — |
| `dragoon18dip` | Dragoon, 18th century (mercenary) | 15.00 | 4.0 | **5.6** | 90 | 7 | 5 | 1 | floor(gc_obj_foodperunit*2) |
| `grenadierdip` | Grenadier (mercenary) | 6.00 | 10.0 | **14.0** | 80 | 60 | 40 | 1 | floor(gc_obj_foodperunit*1.2) |
| `lightcavalrydip` | Light cavalry (mercenary) | 15.00 | 4.0 | **5.6** | 90 | 7 | 5 | 1 | floor(gc_obj_foodperunit*2) |
| `lightinfantrydip` | Light Infantryman (mercenary) | 1.00 | 60.0 | **84.0** | 25 | 0 | 1 | 1 | — |
| `roundshierdip` | Roundshier (mercenary) | 4.00 | 15.0 | **21.0** | 20 | 3 | 25 | 1 | — |

### `rusmil` — Mill

| Юнит | имя | buildtime (g-sec) | rate (units/g-min) | rate (units/real-min @ fast) | F | G | I | farm | upkeep food |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|

### `ruspor` — Shipyard

| Юнит | имя | buildtime (g-sec) | rate (units/g-min) | rate (units/real-min @ fast) | F | G | I | farm | upkeep food |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `battleship` | Ship of the Line | 230.00 | 0.3 | **0.4** | 0 | 1100 | 600 | 1 | — |
| `ferry` | Ferry | 56.00 | 1.1 | **1.5** | 0 | 50 | 100 | 1 | — |
| `fishboat` | Boat | 40.00 | 1.5 | **2.1** | 0 | 0 | 0 | 1 | — |
| `frigate` | Frigate | 230.00 | 0.3 | **0.4** | 0 | 1100 | 600 | 1 | — |
| `galley` | Galley | 50.00 | 1.2 | **1.7** | 0 | 900 | 800 | 1 | — |
| `yacht` | Yacht | 48.00 | 1.2 | **1.8** | 0 | 450 | 150 | 1 | — |

### `russta` — Stable

| Юнит | имя | buildtime (g-sec) | rate (units/g-min) | rate (units/real-min @ fast) | F | G | I | farm | upkeep food |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `cossackdon` | Don Cossack | 24.00 | 2.5 | **3.5** | 120 | 10 | 40 | 1 | floor(gc_obj_foodperunit*2.5) |
| `cuirassier` | Cuirassier | 24.00 | 2.5 | **3.5** | 120 | 10 | 40 | 1 | floor(gc_obj_foodperunit*2.5) |
| `dragoon18` | Dragoon, 18th century | 15.00 | 4.0 | **5.6** | 90 | 7 | 5 | 1 | floor(gc_obj_foodperunit*2) |
| `hussar` | Hussar | 16.50 | 3.6 | **5.1** | 75 | 2 | 5 | 1 | — |
| `vityaz` | Vityaz | 24.00 | 2.5 | **3.5** | 120 | 10 | 40 | 1 | floor(gc_obj_foodperunit*2.5) |

### `rustem` — Orthodox Cathedral

| Юнит | имя | buildtime (g-sec) | rate (units/g-min) | rate (units/real-min @ fast) | F | G | I | farm | upkeep food |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `pope` | Pope | 15.00 | 4.0 | **5.6** | 30 | 10 | 0 | 1 | — |

## sax

### `eurmil` — Mill

| Юнит | имя | buildtime (g-sec) | rate (units/g-min) | rate (units/real-min @ fast) | F | G | I | farm | upkeep food |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|

### `eurpor` — Shipyard

| Юнит | имя | buildtime (g-sec) | rate (units/g-min) | rate (units/real-min @ fast) | F | G | I | farm | upkeep food |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `battleship` | Ship of the Line | 230.00 | 0.3 | **0.4** | 0 | 1100 | 600 | 1 | — |
| `ferry` | Ferry | 56.00 | 1.1 | **1.5** | 0 | 50 | 100 | 1 | — |
| `fishboat` | Boat | 40.00 | 1.5 | **2.1** | 0 | 0 | 0 | 1 | — |
| `frigate` | Frigate | 230.00 | 0.3 | **0.4** | 0 | 1100 | 600 | 1 | — |
| `galley` | Galley | 50.00 | 1.2 | **1.7** | 0 | 900 | 800 | 1 | — |
| `yacht` | Yacht | 48.00 | 1.2 | **1.8** | 0 | 450 | 150 | 1 | — |

### `saxart` — Artillery Depot

| Юнит | имя | buildtime (g-sec) | rate (units/g-min) | rate (units/real-min @ fast) | F | G | I | farm | upkeep food |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `cannon` | Cannon | 75.00 | 0.8 | **1.1** | 0 | 400 | 400 | 1 | — |
| `howitzer` | Howitzer | 94.00 | 0.6 | **0.9** | 0 | 350 | 300 | 1 | — |
| `mortar` | Bombard | 25.00 | 2.4 | **3.4** | 0 | 75 | 200 | 1 | — |
| `multicannon` | Multi-barrelled Cannon | 50.00 | 1.2 | **1.7** | 0 | 400 | 250 | 1 | — |

### `saxba2` — Barracks, 18th century

| Юнит | имя | buildtime (g-sec) | rate (units/g-min) | rate (units/real-min @ fast) | F | G | I | farm | upkeep food |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `drummer18` | Drummer, 18th century | 6.00 | 10.0 | **14.0** | 50 | 30 | 0 | 1 | — |
| `grenadiersax` | Grenadier | 6.00 | 10.0 | **14.0** | 80 | 60 | 40 | 1 | floor(gc_obj_foodperunit*1.2) |
| `musketeer18sax` | Musketeer, 18th century | 4.50 | 13.3 | **18.7** | 40 | 45 | 40 | 1 | — |
| `officer18` | Officer, 18th century | 6.00 | 10.0 | **14.0** | 50 | 200 | 10 | 1 | — |
| `pikeman18` | Pikeman, 18th century | 1.25 | 48.0 | **67.2** | 30 | 2 | 0 | 1 | — |

### `saxbar` — Barracks, 17th century

| Юнит | имя | buildtime (g-sec) | rate (units/g-min) | rate (units/real-min @ fast) | F | G | I | farm | upkeep food |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `drummer` | Drummer, 17th century | 6.00 | 10.0 | **14.0** | 50 | 30 | 0 | 1 | — |
| `musketeer` | Musketeer, 17th century | 6.00 | 10.0 | **14.0** | 45 | 6 | 5 | 1 | — |
| `officer` | Officer, 17th century | 10.00 | 6.0 | **8.4** | 50 | 150 | 30 | 1 | — |
| `pikeman` | Pikeman, 17th century | 4.50 | 13.3 | **18.7** | 25 | 3 | 20 | 1 | — |

### `saxcen` — Town Hall

| Юнит | имя | buildtime (g-sec) | rate (units/g-min) | rate (units/real-min @ fast) | F | G | I | farm | upkeep food |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `peaaus` | Peasant | 12.50 | 4.8 | **6.7** | 100 | 0 | 0 | 1 | 32 |

### `saxdip` — Diplomatic Center

| Юнит | имя | buildtime (g-sec) | rate (units/g-min) | rate (units/real-min @ fast) | F | G | I | farm | upkeep food |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `archerdip` | Archer (mercenary) | 1.50 | 40.0 | **56.0** | 20 | 1 | 0 | 1 | — |
| `archerturdip` | Turkish archer (mercenary) | 1.50 | 40.0 | **56.0** | 20 | 1 | 0 | 1 | — |
| `cossacksichdip` | Sich Cossack (mercenary) | 16.50 | 3.6 | **5.1** | 75 | 2 | 5 | 1 | — |
| `dragoon18dip` | Dragoon, 18th century (mercenary) | 15.00 | 4.0 | **5.6** | 90 | 7 | 5 | 1 | floor(gc_obj_foodperunit*2) |
| `grenadierdip` | Grenadier (mercenary) | 6.00 | 10.0 | **14.0** | 80 | 60 | 40 | 1 | floor(gc_obj_foodperunit*1.2) |
| `lightcavalrydip` | Light cavalry (mercenary) | 15.00 | 4.0 | **5.6** | 90 | 7 | 5 | 1 | floor(gc_obj_foodperunit*2) |
| `lightinfantrydip` | Light Infantryman (mercenary) | 1.00 | 60.0 | **84.0** | 25 | 0 | 1 | 1 | — |
| `roundshierdip` | Roundshier (mercenary) | 4.00 | 15.0 | **21.0** | 20 | 3 | 25 | 1 | — |

### `saxsta` — Stable

| Юнит | имя | buildtime (g-sec) | rate (units/g-min) | rate (units/real-min @ fast) | F | G | I | farm | upkeep food |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `cuirassier` | Cuirassier | 24.00 | 2.5 | **3.5** | 120 | 10 | 40 | 1 | floor(gc_obj_foodperunit*2.5) |
| `dragoon` | Dragoon, 17th century | 15.00 | 4.0 | **5.6** | 90 | 7 | 5 | 1 | floor(gc_obj_foodperunit*2) |
| `dragoon18` | Dragoon, 18th century | 15.00 | 4.0 | **5.6** | 90 | 7 | 5 | 1 | floor(gc_obj_foodperunit*2) |
| `guardcavalrysax` | Cavalry Guard | 24.00 | 2.5 | **3.5** | 120 | 10 | 40 | 1 | floor(gc_obj_foodperunit*2.5) |
| `hussar` | Hussar | 16.50 | 3.6 | **5.1** | 75 | 2 | 5 | 1 | — |
| `reiter` | Reiter | 24.00 | 2.5 | **3.5** | 120 | 10 | 40 | 1 | floor(gc_obj_foodperunit*2.5) |

### `saxtem` — Cathedral

| Юнит | имя | buildtime (g-sec) | rate (units/g-min) | rate (units/real-min @ fast) | F | G | I | farm | upkeep food |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `priest` | Priest | 15.00 | 4.0 | **5.6** | 30 | 10 | 0 | 1 | — |

## sco

### `eurmil` — Mill

| Юнит | имя | buildtime (g-sec) | rate (units/g-min) | rate (units/real-min @ fast) | F | G | I | farm | upkeep food |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|

### `eurpor` — Shipyard

| Юнит | имя | buildtime (g-sec) | rate (units/g-min) | rate (units/real-min @ fast) | F | G | I | farm | upkeep food |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `battleship` | Ship of the Line | 230.00 | 0.3 | **0.4** | 0 | 1100 | 600 | 1 | — |
| `ferry` | Ferry | 56.00 | 1.1 | **1.5** | 0 | 50 | 100 | 1 | — |
| `fishboat` | Boat | 40.00 | 1.5 | **2.1** | 0 | 0 | 0 | 1 | — |
| `frigate` | Frigate | 230.00 | 0.3 | **0.4** | 0 | 1100 | 600 | 1 | — |
| `yacht` | Yacht | 48.00 | 1.2 | **1.8** | 0 | 450 | 150 | 1 | — |

### `scoart` — Artillery Depot

| Юнит | имя | buildtime (g-sec) | rate (units/g-min) | rate (units/real-min @ fast) | F | G | I | farm | upkeep food |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `cannon` | Cannon | 75.00 | 0.8 | **1.1** | 0 | 400 | 400 | 1 | — |
| `framegun` | Frame gun | 50.00 | 1.2 | **1.7** | 0 | 300 | 150 | 1 | — |
| `howitzer` | Howitzer | 94.00 | 0.6 | **0.9** | 0 | 350 | 300 | 1 | — |
| `mortar` | Bombard | 25.00 | 2.4 | **3.4** | 0 | 75 | 200 | 1 | — |

### `scoba2` — Castle

| Юнит | имя | buildtime (g-sec) | rate (units/g-min) | rate (units/real-min @ fast) | F | G | I | farm | upkeep food |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `archersco` | Bow Clansman | 6.00 | 10.0 | **14.0** | 80 | 7 | 0 | 1 | floor(gc_obj_foodperunit*1.33) |
| `swordsmansco` | Sword Clansman | 7.00 | 8.6 | **12.0** | 110 | 10 | 0 | 1 | floor(gc_obj_foodperunit*1.5) |

### `scobar` — Barracks, 17th century

| Юнит | имя | buildtime (g-sec) | rate (units/g-min) | rate (units/real-min @ fast) | F | G | I | farm | upkeep food |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `bagpiper` | Bagpiper | 6.00 | 10.0 | **14.0** | 50 | 30 | 0 | 1 | — |
| `musketeersco` | Covenanter musketeer | 6.00 | 10.0 | **14.0** | 45 | 6 | 5 | 1 | — |
| `officersco` | Officer | 10.00 | 6.0 | **8.4** | 130 | 130 | 10 | 1 | — |
| `pikemansco` | Covenanter pikeman | 4.00 | 15.0 | **21.0** | 35 | 2 | 0 | 1 | — |

### `scocen` — Town Hall

| Юнит | имя | buildtime (g-sec) | rate (units/g-min) | rate (units/real-min @ fast) | F | G | I | farm | upkeep food |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `peasco` | Peasant | 12.50 | 4.8 | **6.7** | 100 | 0 | 0 | 1 | 32 |

### `scodip` — Diplomatic Center

| Юнит | имя | buildtime (g-sec) | rate (units/g-min) | rate (units/real-min @ fast) | F | G | I | farm | upkeep food |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `archerdip` | Archer (mercenary) | 6.00 | 10.0 | **14.0** | 80 | 7 | 0 | 1 | floor(gc_obj_foodperunit*1.33) |
| `archerturdip` | Turkish archer (mercenary) | 6.00 | 10.0 | **14.0** | 80 | 7 | 0 | 1 | floor(gc_obj_foodperunit*1.33) |
| `cossacksichdip` | Sich Cossack (mercenary) | 16.50 | 3.6 | **5.1** | 75 | 2 | 5 | 1 | — |
| `dragoon18dip` | Dragoon, 18th century (mercenary) | 15.00 | 4.0 | **5.6** | 90 | 7 | 5 | 1 | floor(gc_obj_foodperunit*2) |
| `grenadierdip` | Grenadier (mercenary) | 6.00 | 10.0 | **14.0** | 80 | 60 | 40 | 1 | floor(gc_obj_foodperunit*1.2) |
| `lightcavalrydip` | Light cavalry (mercenary) | 15.00 | 4.0 | **5.6** | 90 | 7 | 5 | 1 | floor(gc_obj_foodperunit*2) |
| `lightinfantrydip` | Light Infantryman (mercenary) | 1.00 | 60.0 | **84.0** | 25 | 0 | 1 | 1 | — |
| `roundshierdip` | Roundshier (mercenary) | 7.00 | 8.6 | **12.0** | 110 | 10 | 0 | 1 | floor(gc_obj_foodperunit*1.5) |

### `scosta` — Stable

| Юнит | имя | buildtime (g-sec) | rate (units/g-min) | rate (units/real-min @ fast) | F | G | I | farm | upkeep food |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `lancersco` | Lancer | 24.00 | 2.5 | **3.5** | 120 | 10 | 40 | 1 | floor(gc_obj_foodperunit*2.5) |
| `raidersco` | Raider | 16.50 | 3.6 | **5.1** | 75 | 2 | 5 | 1 | — |

### `scotem` — Cathedral

| Юнит | имя | buildtime (g-sec) | rate (units/g-min) | rate (units/real-min @ fast) | F | G | I | farm | upkeep food |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `priest` | Priest | 15.00 | 4.0 | **5.6** | 30 | 10 | 0 | 1 | — |

## spa

### `eurmil` — Mill

| Юнит | имя | buildtime (g-sec) | rate (units/g-min) | rate (units/real-min @ fast) | F | G | I | farm | upkeep food |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|

### `eurpor` — Shipyard

| Юнит | имя | buildtime (g-sec) | rate (units/g-min) | rate (units/real-min @ fast) | F | G | I | farm | upkeep food |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `battleship` | Ship of the Line | 230.00 | 0.3 | **0.4** | 0 | 1100 | 600 | 1 | — |
| `ferry` | Ferry | 56.00 | 1.1 | **1.5** | 0 | 50 | 100 | 1 | — |
| `fishboat` | Boat | 40.00 | 1.5 | **2.1** | 0 | 0 | 0 | 1 | — |
| `frigate` | Frigate | 230.00 | 0.3 | **0.4** | 0 | 1100 | 600 | 1 | — |
| `galley` | Galley | 50.00 | 1.2 | **1.7** | 0 | 900 | 800 | 1 | — |
| `yacht` | Yacht | 48.00 | 1.2 | **1.8** | 0 | 450 | 150 | 1 | — |

### `spaart` — Artillery Depot

| Юнит | имя | buildtime (g-sec) | rate (units/g-min) | rate (units/real-min @ fast) | F | G | I | farm | upkeep food |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `cannon` | Cannon | 75.00 | 0.8 | **1.1** | 0 | 400 | 400 | 1 | — |
| `howitzer` | Howitzer | 94.00 | 0.6 | **0.9** | 0 | 350 | 300 | 1 | — |
| `mortar` | Bombard | 25.00 | 2.4 | **3.4** | 0 | 75 | 200 | 1 | — |
| `multicannon` | Multi-barrelled Cannon | 50.00 | 1.2 | **1.7** | 0 | 400 | 250 | 1 | — |

### `spaba2` — Barracks, 18th century

| Юнит | имя | buildtime (g-sec) | rate (units/g-min) | rate (units/real-min @ fast) | F | G | I | farm | upkeep food |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `drummer18` | Drummer, 18th century | 6.00 | 10.0 | **14.0** | 50 | 30 | 0 | 1 | — |
| `grenadier` | Grenadier | 6.00 | 10.0 | **14.0** | 80 | 60 | 40 | 1 | floor(gc_obj_foodperunit*1.2) |
| `musketeer18` | Musketeer, 18th century | 4.50 | 13.3 | **18.7** | 50 | 40 | 40 | 1 | — |
| `officer18` | Officer, 18th century | 6.00 | 10.0 | **14.0** | 50 | 200 | 10 | 1 | — |
| `pikeman18` | Pikeman, 18th century | 1.25 | 48.0 | **67.2** | 30 | 2 | 0 | 1 | — |

### `spabar` — Barracks, 17th century

| Юнит | имя | buildtime (g-sec) | rate (units/g-min) | rate (units/real-min @ fast) | F | G | I | farm | upkeep food |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `drummer` | Drummer, 17th century | 6.00 | 10.0 | **14.0** | 50 | 30 | 0 | 1 | — |
| `musketeerspa` | Musketeer, 17th century | 18.75 | 3.2 | **4.5** | 45 | 6 | 10 | 1 | — |
| `officer` | Officer, 17th century | 10.00 | 6.0 | **8.4** | 50 | 150 | 30 | 1 | — |
| `pikeman` | Pikeman, 17th century | 5.50 | 10.9 | **15.3** | 35 | 7 | 30 | 1 | — |
| `pikemanspa` | Coselete | 5.50 | 10.9 | **15.3** | 35 | 7 | 30 | 1 | — |

### `spacen` — Town Hall

| Юнит | имя | buildtime (g-sec) | rate (units/g-min) | rate (units/real-min @ fast) | F | G | I | farm | upkeep food |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `peaspa` | Peasant | 12.50 | 4.8 | **6.7** | 100 | 0 | 0 | 1 | 32 |

### `spadip` — Diplomatic Center

| Юнит | имя | buildtime (g-sec) | rate (units/g-min) | rate (units/real-min @ fast) | F | G | I | farm | upkeep food |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `archerdip` | Archer (mercenary) | 1.50 | 40.0 | **56.0** | 20 | 1 | 0 | 1 | — |
| `archerturdip` | Turkish archer (mercenary) | 1.50 | 40.0 | **56.0** | 20 | 1 | 0 | 1 | — |
| `cossacksichdip` | Sich Cossack (mercenary) | 16.50 | 3.6 | **5.1** | 75 | 2 | 5 | 1 | — |
| `dragoon18dip` | Dragoon, 18th century (mercenary) | 15.00 | 4.0 | **5.6** | 90 | 7 | 5 | 1 | floor(gc_obj_foodperunit*2) |
| `grenadierdip` | Grenadier (mercenary) | 6.00 | 10.0 | **14.0** | 80 | 60 | 40 | 1 | floor(gc_obj_foodperunit*1.2) |
| `lightcavalrydip` | Light cavalry (mercenary) | 15.00 | 4.0 | **5.6** | 90 | 7 | 5 | 1 | floor(gc_obj_foodperunit*2) |
| `lightinfantrydip` | Light Infantryman (mercenary) | 1.00 | 60.0 | **84.0** | 25 | 0 | 1 | 1 | — |
| `roundshierdip` | Roundshier (mercenary) | 4.00 | 15.0 | **21.0** | 20 | 3 | 25 | 1 | — |

### `spasta` — Stable

| Юнит | имя | buildtime (g-sec) | rate (units/g-min) | rate (units/real-min @ fast) | F | G | I | farm | upkeep food |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `cuirassier` | Cuirassier | 24.00 | 2.5 | **3.5** | 120 | 10 | 40 | 1 | floor(gc_obj_foodperunit*2.5) |
| `dragoon` | Dragoon, 17th century | 15.00 | 4.0 | **5.6** | 90 | 7 | 5 | 1 | floor(gc_obj_foodperunit*2) |
| `dragoon18` | Dragoon, 18th century | 15.00 | 4.0 | **5.6** | 90 | 7 | 5 | 1 | floor(gc_obj_foodperunit*2) |
| `hussar` | Hussar | 16.50 | 3.6 | **5.1** | 75 | 2 | 5 | 1 | — |
| `reiter` | Reiter | 24.00 | 2.5 | **3.5** | 120 | 10 | 40 | 1 | floor(gc_obj_foodperunit*2.5) |

### `spatem` — Cathedral

| Юнит | имя | buildtime (g-sec) | rate (units/g-min) | rate (units/real-min @ fast) | F | G | I | farm | upkeep food |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `priest` | Priest | 15.00 | 4.0 | **5.6** | 30 | 10 | 0 | 1 | — |

## swe

### `eurmil` — Mill

| Юнит | имя | buildtime (g-sec) | rate (units/g-min) | rate (units/real-min @ fast) | F | G | I | farm | upkeep food |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|

### `eurpor` — Shipyard

| Юнит | имя | buildtime (g-sec) | rate (units/g-min) | rate (units/real-min @ fast) | F | G | I | farm | upkeep food |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `battleship` | Ship of the Line | 230.00 | 0.3 | **0.4** | 0 | 1100 | 600 | 1 | — |
| `ferry` | Ferry | 56.00 | 1.1 | **1.5** | 0 | 50 | 100 | 1 | — |
| `fishboat` | Boat | 40.00 | 1.5 | **2.1** | 0 | 0 | 0 | 1 | — |
| `frigate` | Frigate | 230.00 | 0.3 | **0.4** | 0 | 1100 | 600 | 1 | — |
| `galley` | Galley | 50.00 | 1.2 | **1.7** | 0 | 900 | 800 | 1 | — |
| `yacht` | Yacht | 48.00 | 1.2 | **1.8** | 0 | 450 | 150 | 1 | — |

### `sweart` — Artillery Depot

| Юнит | имя | buildtime (g-sec) | rate (units/g-min) | rate (units/real-min @ fast) | F | G | I | farm | upkeep food |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `cannon` | Cannon | 75.00 | 0.8 | **1.1** | 0 | 400 | 400 | 1 | — |
| `howitzer` | Howitzer | 94.00 | 0.6 | **0.9** | 0 | 350 | 300 | 1 | — |
| `mortar` | Bombard | 25.00 | 2.4 | **3.4** | 0 | 75 | 200 | 1 | — |
| `multicannon` | Multi-barrelled Cannon | 50.00 | 1.2 | **1.7** | 0 | 400 | 250 | 1 | — |

### `sweba2` — Barracks, 18th century

| Юнит | имя | buildtime (g-sec) | rate (units/g-min) | rate (units/real-min @ fast) | F | G | I | farm | upkeep food |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `drummer18` | Drummer, 18th century | 6.00 | 10.0 | **14.0** | 50 | 30 | 0 | 1 | — |
| `grenadier` | Grenadier | 6.00 | 10.0 | **14.0** | 80 | 60 | 40 | 1 | floor(gc_obj_foodperunit*1.2) |
| `musketeer18` | Musketeer, 18th century | 4.50 | 13.3 | **18.7** | 50 | 40 | 40 | 1 | — |
| `officer18` | Officer, 18th century | 6.00 | 10.0 | **14.0** | 50 | 200 | 10 | 1 | — |
| `pikeman18swe` | Pikeman, 18th century | 1.50 | 40.0 | **56.0** | 40 | 3 | 0 | 1 | — |

### `swebar` — Barracks, 17th century

| Юнит | имя | buildtime (g-sec) | rate (units/g-min) | rate (units/real-min @ fast) | F | G | I | farm | upkeep food |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `drummer` | Drummer, 17th century | 6.00 | 10.0 | **14.0** | 50 | 30 | 0 | 1 | — |
| `musketeer` | Musketeer, 17th century | 6.00 | 10.0 | **14.0** | 45 | 6 | 5 | 1 | — |
| `officer` | Officer, 17th century | 10.00 | 6.0 | **8.4** | 50 | 150 | 30 | 1 | — |
| `pikeman` | Pikeman, 17th century | 4.50 | 13.3 | **18.7** | 25 | 3 | 20 | 1 | — |

### `swecen` — Town Hall

| Юнит | имя | buildtime (g-sec) | rate (units/g-min) | rate (units/real-min @ fast) | F | G | I | farm | upkeep food |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `peaeng` | Peasant | 12.50 | 4.8 | **6.7** | 100 | 0 | 0 | 1 | 32 |

### `swedip` — Diplomatic Center

| Юнит | имя | buildtime (g-sec) | rate (units/g-min) | rate (units/real-min @ fast) | F | G | I | farm | upkeep food |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `archerdip` | Archer (mercenary) | 1.50 | 40.0 | **56.0** | 20 | 1 | 0 | 1 | — |
| `archerturdip` | Turkish archer (mercenary) | 1.50 | 40.0 | **56.0** | 20 | 1 | 0 | 1 | — |
| `cossacksichdip` | Sich Cossack (mercenary) | 16.50 | 3.6 | **5.1** | 75 | 2 | 5 | 1 | — |
| `dragoon18dip` | Dragoon, 18th century (mercenary) | 15.00 | 4.0 | **5.6** | 90 | 7 | 5 | 1 | floor(gc_obj_foodperunit*2) |
| `grenadierdip` | Grenadier (mercenary) | 6.00 | 10.0 | **14.0** | 80 | 60 | 40 | 1 | floor(gc_obj_foodperunit*1.2) |
| `lightcavalrydip` | Light cavalry (mercenary) | 15.00 | 4.0 | **5.6** | 90 | 7 | 5 | 1 | floor(gc_obj_foodperunit*2) |
| `lightinfantrydip` | Light Infantryman (mercenary) | 1.00 | 60.0 | **84.0** | 25 | 0 | 1 | 1 | — |
| `roundshierdip` | Roundshier (mercenary) | 4.00 | 15.0 | **21.0** | 20 | 3 | 25 | 1 | — |

### `swesta` — Stable

| Юнит | имя | buildtime (g-sec) | rate (units/g-min) | rate (units/real-min @ fast) | F | G | I | farm | upkeep food |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `cuirassier` | Cuirassier | 24.00 | 2.5 | **3.5** | 120 | 10 | 40 | 1 | floor(gc_obj_foodperunit*2.5) |
| `dragoon` | Dragoon, 17th century | 15.00 | 4.0 | **5.6** | 90 | 7 | 5 | 1 | floor(gc_obj_foodperunit*2) |
| `dragoon18` | Dragoon, 18th century | 15.00 | 4.0 | **5.6** | 90 | 7 | 5 | 1 | floor(gc_obj_foodperunit*2) |
| `hackapell` | Hakkapeliitta | 16.50 | 3.6 | **5.1** | 75 | 2 | 5 | 1 | — |
| `hussar` | Hussar | 16.50 | 3.6 | **5.1** | 75 | 2 | 5 | 1 | — |
| `reiterswe` | Swedish Reiter | 24.00 | 2.5 | **3.5** | 120 | 10 | 40 | 1 | floor(gc_obj_foodperunit*2.5) |

### `swetem` — Cathedral

| Юнит | имя | buildtime (g-sec) | rate (units/g-min) | rate (units/real-min @ fast) | F | G | I | farm | upkeep food |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `priest` | Priest | 15.00 | 4.0 | **5.6** | 30 | 10 | 0 | 1 | — |

## swi

### `eurmil` — Mill

| Юнит | имя | buildtime (g-sec) | rate (units/g-min) | rate (units/real-min @ fast) | F | G | I | farm | upkeep food |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|

### `eurpor` — Shipyard

| Юнит | имя | buildtime (g-sec) | rate (units/g-min) | rate (units/real-min @ fast) | F | G | I | farm | upkeep food |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `battleship` | Ship of the Line | 230.00 | 0.3 | **0.4** | 0 | 1100 | 600 | 1 | — |
| `ferry` | Ferry | 56.00 | 1.1 | **1.5** | 0 | 50 | 100 | 1 | — |
| `fishboat` | Boat | 40.00 | 1.5 | **2.1** | 0 | 0 | 0 | 1 | — |
| `frigate` | Frigate | 230.00 | 0.3 | **0.4** | 0 | 1100 | 600 | 1 | — |
| `galley` | Galley | 50.00 | 1.2 | **1.7** | 0 | 900 | 800 | 1 | — |
| `yacht` | Yacht | 48.00 | 1.2 | **1.8** | 0 | 450 | 150 | 1 | — |

### `swiart` — Artillery Depot

| Юнит | имя | buildtime (g-sec) | rate (units/g-min) | rate (units/real-min @ fast) | F | G | I | farm | upkeep food |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `cannon` | Cannon | 75.00 | 0.8 | **1.1** | 0 | 400 | 400 | 1 | — |
| `howitzer` | Howitzer | 94.00 | 0.6 | **0.9** | 0 | 350 | 300 | 1 | — |
| `mortar` | Bombard | 25.00 | 2.4 | **3.4** | 0 | 75 | 200 | 1 | — |
| `multicannon` | Multi-barrelled Cannon | 50.00 | 1.2 | **1.7** | 0 | 400 | 250 | 1 | — |

### `swiba2` — Barracks, 18th century

| Юнит | имя | buildtime (g-sec) | rate (units/g-min) | rate (units/real-min @ fast) | F | G | I | farm | upkeep food |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `drummer18` | Drummer, 18th century | 6.00 | 10.0 | **14.0** | 50 | 30 | 0 | 1 | — |
| `grenadier` | Grenadier | 6.00 | 10.0 | **14.0** | 80 | 60 | 40 | 1 | floor(gc_obj_foodperunit*1.2) |
| `jagerswi` | Jaeger | 6.00 | 10.0 | **14.0** | 45 | 6 | 5 | 1 | — |
| `musketeer18` | Musketeer, 18th century | 4.50 | 13.3 | **18.7** | 50 | 40 | 40 | 1 | — |
| `officer18` | Officer, 18th century | 6.00 | 10.0 | **14.0** | 50 | 200 | 10 | 1 | — |
| `pikeman18` | Pikeman, 18th century | 1.25 | 48.0 | **67.2** | 30 | 2 | 0 | 1 | — |

### `swibar` — Barracks, 17th century

| Юнит | имя | buildtime (g-sec) | rate (units/g-min) | rate (units/real-min @ fast) | F | G | I | farm | upkeep food |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `drummer` | Drummer, 17th century | 6.00 | 10.0 | **14.0** | 50 | 30 | 0 | 1 | — |
| `musketeer` | Musketeer, 17th century | 6.00 | 10.0 | **14.0** | 45 | 6 | 5 | 1 | — |
| `officer` | Officer, 17th century | 10.00 | 6.0 | **8.4** | 50 | 150 | 30 | 1 | — |
| `pikemanswi` | Pikeman, 17th century | 5.00 | 12.0 | **16.8** | 40 | 6 | 20 | 1 | — |

### `swicen` — Town Hall

| Юнит | имя | buildtime (g-sec) | rate (units/g-min) | rate (units/real-min @ fast) | F | G | I | farm | upkeep food |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `peaaus` | Peasant | 12.50 | 4.8 | **6.7** | 100 | 0 | 0 | 1 | 32 |

### `swidip` — Diplomatic Center

| Юнит | имя | buildtime (g-sec) | rate (units/g-min) | rate (units/real-min @ fast) | F | G | I | farm | upkeep food |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `archerdip` | Archer (mercenary) | 1.50 | 40.0 | **56.0** | 20 | 1 | 0 | 1 | — |
| `archerturdip` | Turkish archer (mercenary) | 1.50 | 40.0 | **56.0** | 20 | 1 | 0 | 1 | — |
| `cossacksichdip` | Sich Cossack (mercenary) | 16.50 | 3.6 | **5.1** | 75 | 2 | 5 | 1 | — |
| `dragoon18dip` | Dragoon, 18th century (mercenary) | 15.00 | 4.0 | **5.6** | 90 | 7 | 5 | 1 | floor(gc_obj_foodperunit*2) |
| `grenadierdip` | Grenadier (mercenary) | 6.00 | 10.0 | **14.0** | 80 | 60 | 40 | 1 | floor(gc_obj_foodperunit*1.2) |
| `lightcavalrydip` | Light cavalry (mercenary) | 15.00 | 4.0 | **5.6** | 90 | 7 | 5 | 1 | floor(gc_obj_foodperunit*2) |
| `lightinfantrydip` | Light Infantryman (mercenary) | 1.00 | 60.0 | **84.0** | 25 | 0 | 1 | 1 | — |
| `roundshierdip` | Roundshier (mercenary) | 4.00 | 15.0 | **21.0** | 20 | 3 | 25 | 1 | — |

### `swista` — Stable

| Юнит | имя | buildtime (g-sec) | rate (units/g-min) | rate (units/real-min @ fast) | F | G | I | farm | upkeep food |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `cuirassier` | Cuirassier | 24.00 | 2.5 | **3.5** | 120 | 10 | 40 | 1 | floor(gc_obj_foodperunit*2.5) |
| `dragoon` | Dragoon, 17th century | 15.00 | 4.0 | **5.6** | 90 | 7 | 5 | 1 | floor(gc_obj_foodperunit*2) |
| `dragoon18` | Dragoon, 18th century | 15.00 | 4.0 | **5.6** | 90 | 7 | 5 | 1 | floor(gc_obj_foodperunit*2) |
| `hussarswi` | Mounted Jaeger | 16.50 | 3.6 | **5.1** | 75 | 2 | 5 | 1 | — |
| `reiter` | Reiter | 24.00 | 2.5 | **3.5** | 120 | 10 | 40 | 1 | floor(gc_obj_foodperunit*2.5) |

### `switem` — Cathedral

| Юнит | имя | buildtime (g-sec) | rate (units/g-min) | rate (units/real-min @ fast) | F | G | I | farm | upkeep food |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `priest` | Priest | 15.00 | 4.0 | **5.6** | 30 | 10 | 0 | 1 | — |

## tur

### `turart` — Artillery Depot

| Юнит | имя | buildtime (g-sec) | rate (units/g-min) | rate (units/real-min @ fast) | F | G | I | farm | upkeep food |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `cannon` | Cannon | 75.00 | 0.8 | **1.1** | 0 | 400 | 400 | 1 | — |
| `howitzer` | Howitzer | 94.00 | 0.6 | **0.9** | 0 | 350 | 300 | 1 | — |
| `mortar` | Bombard | 25.00 | 2.4 | **3.4** | 0 | 75 | 200 | 1 | — |

### `turbar` — Barracks

| Юнит | имя | buildtime (g-sec) | rate (units/g-min) | rate (units/real-min @ fast) | F | G | I | farm | upkeep food |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `archertur` | Turkish archer | 3.00 | 20.0 | **28.0** | 45 | 4 | 0 | 1 | — |
| `drummertur` | Drummer, 17th century | 4.00 | 15.0 | **21.0** | 30 | 15 | 0 | 1 | — |
| `jannisary` | Janissary | 6.00 | 10.0 | **14.0** | 45 | 6 | 5 | 1 | — |
| `lightinfantry` | Light Infantryman | 1.00 | 60.0 | **84.0** | 25 | 0 | 1 | 1 | — |
| `officertur` | Officer | 7.50 | 8.0 | **11.2** | 50 | 100 | 0 | 1 | — |
| `pikemantur` | Ottoman Pikeman | 5.50 | 10.9 | **15.3** | 55 | 5 | 0 | 1 | — |

### `turcen` — Town Hall

| Юнит | имя | buildtime (g-sec) | rate (units/g-min) | rate (units/real-min @ fast) | F | G | I | farm | upkeep food |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `peatur` | Peasant | 12.50 | 4.8 | **6.7** | 100 | 0 | 0 | 1 | 28 |

### `turdip` — Diplomatic Center

| Юнит | имя | buildtime (g-sec) | rate (units/g-min) | rate (units/real-min @ fast) | F | G | I | farm | upkeep food |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `archerdip` | Archer (mercenary) | 3.00 | 20.0 | **28.0** | 45 | 4 | 0 | 1 | — |
| `archerturdip` | Turkish archer (mercenary) | 3.00 | 20.0 | **28.0** | 45 | 4 | 0 | 1 | — |
| `cossacksichdip` | Sich Cossack (mercenary) | 16.50 | 3.6 | **5.1** | 75 | 2 | 5 | 1 | — |
| `dragoon18dip` | Dragoon, 18th century (mercenary) | 15.00 | 4.0 | **5.6** | 90 | 7 | 5 | 1 | floor(gc_obj_foodperunit*2) |
| `grenadierdip` | Grenadier (mercenary) | 6.00 | 10.0 | **14.0** | 80 | 60 | 40 | 1 | floor(gc_obj_foodperunit*1.2) |
| `lightcavalrydip` | Light cavalry (mercenary) | 15.00 | 4.0 | **5.6** | 90 | 7 | 5 | 1 | floor(gc_obj_foodperunit*2) |
| `lightinfantrydip` | Light Infantryman (mercenary) | 1.00 | 60.0 | **84.0** | 25 | 0 | 1 | 1 | — |
| `roundshierdip` | Roundshier (mercenary) | 4.00 | 15.0 | **21.0** | 20 | 3 | 25 | 1 | — |

### `turmil` — Mill

| Юнит | имя | buildtime (g-sec) | rate (units/g-min) | rate (units/real-min @ fast) | F | G | I | farm | upkeep food |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|

### `turpor` — Shipyard

| Юнит | имя | buildtime (g-sec) | rate (units/g-min) | rate (units/real-min @ fast) | F | G | I | farm | upkeep food |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `battleship` | Ship of the Line | 230.00 | 0.3 | **0.4** | 0 | 1100 | 600 | 1 | — |
| `ferry` | Ferry | 56.00 | 1.1 | **1.5** | 0 | 50 | 100 | 1 | — |
| `fishboat` | Boat | 40.00 | 1.5 | **2.1** | 0 | 0 | 0 | 1 | — |
| `galley` | Galley | 50.00 | 1.2 | **1.7** | 0 | 900 | 800 | 1 | — |
| `xebec` | Xebec | 230.00 | 0.3 | **0.4** | 0 | 1100 | 600 | 1 | — |
| `yachttur` | Yacht | 48.00 | 1.2 | **1.8** | 0 | 450 | 150 | 1 | — |

### `tursta` — Stable

| Юнит | имя | buildtime (g-sec) | rate (units/g-min) | rate (units/real-min @ fast) | F | G | I | farm | upkeep food |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `sipahi` | Heavy Sipahi | 24.00 | 2.5 | **3.5** | 120 | 10 | 40 | 1 | floor(gc_obj_foodperunit*2.5) |
| `spakh` | Light Sipahi | 24.00 | 2.5 | **3.5** | 120 | 10 | 40 | 1 | floor(gc_obj_foodperunit*2.5) |
| `tatar` | Tatar | 11.25 | 5.3 | **7.5** | 70 | 6 | 0 | 1 | floor(gc_obj_foodperunit*2) |

### `turtem` — Mosque

| Юнит | имя | buildtime (g-sec) | rate (units/g-min) | rate (units/real-min @ fast) | F | G | I | farm | upkeep food |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `mullah` | Mullah | 15.00 | 4.0 | **5.6** | 30 | 10 | 0 | 1 | — |

## ukr

### `rusmil` — Mill

| Юнит | имя | buildtime (g-sec) | rate (units/g-min) | rate (units/real-min @ fast) | F | G | I | farm | upkeep food |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|

### `ukrart` — Artillery Depot

| Юнит | имя | buildtime (g-sec) | rate (units/g-min) | rate (units/real-min @ fast) | F | G | I | farm | upkeep food |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `cannon` | Cannon | 75.00 | 0.8 | **1.1** | 0 | 400 | 400 | 1 | — |
| `howitzer` | Howitzer | 94.00 | 0.6 | **0.9** | 0 | 350 | 300 | 1 | — |
| `mortar` | Bombard | 25.00 | 2.4 | **3.4** | 0 | 75 | 200 | 1 | — |

### `ukrbar` — Cossack House

| Юнит | имя | buildtime (g-sec) | rate (units/g-min) | rate (units/real-min @ fast) | F | G | I | farm | upkeep food |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `serdiuk` | Serdiuk | 6.00 | 10.0 | **14.0** | 45 | 6 | 5 | 1 | — |

### `ukrcen` — Town Hall

| Юнит | имя | buildtime (g-sec) | rate (units/g-min) | rate (units/real-min @ fast) | F | G | I | farm | upkeep food |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `peaukr` | Peasant | 11.25 | 5.3 | **7.5** | 100 | 0 | 0 | 1 | 32 |

### `ukrdip` — Diplomatic Center

| Юнит | имя | buildtime (g-sec) | rate (units/g-min) | rate (units/real-min @ fast) | F | G | I | farm | upkeep food |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `archerdip` | Archer (mercenary) | 1.50 | 40.0 | **56.0** | 20 | 1 | 0 | 1 | — |
| `archerturdip` | Turkish archer (mercenary) | 1.50 | 40.0 | **56.0** | 20 | 1 | 0 | 1 | — |
| `cossacksichdip` | Sich Cossack (mercenary) | 16.50 | 3.6 | **5.1** | 75 | 2 | 5 | 1 | — |
| `dragoon18dip` | Dragoon, 18th century (mercenary) | 15.00 | 4.0 | **5.6** | 90 | 7 | 5 | 1 | floor(gc_obj_foodperunit*2) |
| `grenadierdip` | Grenadier (mercenary) | 6.00 | 10.0 | **14.0** | 80 | 60 | 40 | 1 | floor(gc_obj_foodperunit*1.2) |
| `lightcavalrydip` | Light cavalry (mercenary) | 15.00 | 4.0 | **5.6** | 90 | 7 | 5 | 1 | floor(gc_obj_foodperunit*2) |
| `lightinfantrydip` | Light Infantryman (mercenary) | 1.00 | 60.0 | **84.0** | 25 | 0 | 1 | 1 | — |
| `roundshierdip` | Roundshier (mercenary) | 4.00 | 15.0 | **21.0** | 20 | 3 | 25 | 1 | — |

### `ukrpor` — Shipyard

| Юнит | имя | buildtime (g-sec) | rate (units/g-min) | rate (units/real-min @ fast) | F | G | I | farm | upkeep food |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `chaika` | — | 230.00 | 0.3 | **0.4** | 0 | 1100 | 600 | 1 | — |
| `ferry` | Ferry | 56.00 | 1.1 | **1.5** | 0 | 50 | 100 | 1 | — |
| `fishboat` | Boat | 40.00 | 1.5 | **2.1** | 0 | 0 | 0 | 1 | — |
| `galley` | Galley | 50.00 | 1.2 | **1.7** | 0 | 900 | 800 | 1 | — |

### `ukrsta` — Stable

| Юнит | имя | buildtime (g-sec) | rate (units/g-min) | rate (units/real-min @ fast) | F | G | I | farm | upkeep food |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `cossackregister` | Register Cossack | 24.00 | 2.5 | **3.5** | 120 | 10 | 40 | 1 | floor(gc_obj_foodperunit*2.5) |
| `cossacksich` | Sich Cossack | 16.50 | 3.6 | **5.1** | 75 | 2 | 5 | 1 | — |
| `hetman` | Hetman | 24.00 | 2.5 | **3.5** | 120 | 10 | 40 | 1 | floor(gc_obj_foodperunit*2.5) |

### `ukrtem` — Orthodox Cathedral

| Юнит | имя | buildtime (g-sec) | rate (units/g-min) | rate (units/real-min @ fast) | F | G | I | farm | upkeep food |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `pope` | Pope | 15.00 | 4.0 | **5.6** | 30 | 10 | 0 | 1 | — |

## ven

### `eurmil` — Mill

| Юнит | имя | buildtime (g-sec) | rate (units/g-min) | rate (units/real-min @ fast) | F | G | I | farm | upkeep food |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|

### `eurpor` — Shipyard

| Юнит | имя | buildtime (g-sec) | rate (units/g-min) | rate (units/real-min @ fast) | F | G | I | farm | upkeep food |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `battleship` | Ship of the Line | 230.00 | 0.3 | **0.4** | 0 | 1100 | 600 | 1 | — |
| `ferry` | Ferry | 56.00 | 1.1 | **1.5** | 0 | 50 | 100 | 1 | — |
| `fishboat` | Boat | 40.00 | 1.5 | **2.1** | 0 | 0 | 0 | 1 | — |
| `frigate` | Frigate | 230.00 | 0.3 | **0.4** | 0 | 1100 | 600 | 1 | — |
| `galley` | Galley | 50.00 | 1.2 | **1.7** | 0 | 900 | 800 | 1 | — |
| `yacht` | Yacht | 48.00 | 1.2 | **1.8** | 0 | 450 | 150 | 1 | — |

### `venart` — Artillery Depot

| Юнит | имя | buildtime (g-sec) | rate (units/g-min) | rate (units/real-min @ fast) | F | G | I | farm | upkeep food |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `cannon` | Cannon | 75.00 | 0.8 | **1.1** | 0 | 400 | 400 | 1 | — |
| `howitzer` | Howitzer | 94.00 | 0.6 | **0.9** | 0 | 350 | 300 | 1 | — |
| `mortar` | Bombard | 25.00 | 2.4 | **3.4** | 0 | 75 | 200 | 1 | — |
| `multicannon` | Multi-barrelled Cannon | 50.00 | 1.2 | **1.7** | 0 | 400 | 250 | 1 | — |

### `venba2` — Barracks, 18th century

| Юнит | имя | buildtime (g-sec) | rate (units/g-min) | rate (units/real-min @ fast) | F | G | I | farm | upkeep food |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `drummer18` | Drummer, 18th century | 6.00 | 10.0 | **14.0** | 50 | 30 | 0 | 1 | — |
| `grenadier` | Grenadier | 6.00 | 10.0 | **14.0** | 80 | 60 | 40 | 1 | floor(gc_obj_foodperunit*1.2) |
| `musketeer18` | Musketeer, 18th century | 4.50 | 13.3 | **18.7** | 50 | 40 | 40 | 1 | — |
| `officer18` | Officer, 18th century | 6.00 | 10.0 | **14.0** | 50 | 200 | 10 | 1 | — |
| `pikeman18` | Pikeman, 18th century | 1.25 | 48.0 | **67.2** | 30 | 2 | 0 | 1 | — |

### `venbar` — Barracks, 17th century

| Юнит | имя | buildtime (g-sec) | rate (units/g-min) | rate (units/real-min @ fast) | F | G | I | farm | upkeep food |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `drummer` | Drummer, 17th century | 6.00 | 10.0 | **14.0** | 50 | 30 | 0 | 1 | — |
| `musketeer` | Musketeer, 17th century | 6.00 | 10.0 | **14.0** | 45 | 6 | 5 | 1 | — |
| `officer` | Officer, 17th century | 10.00 | 6.0 | **8.4** | 50 | 150 | 30 | 1 | — |
| `pikeman` | Pikeman, 17th century | 4.50 | 13.3 | **18.7** | 25 | 3 | 20 | 1 | — |

### `vencen` — Town Hall

| Юнит | имя | buildtime (g-sec) | rate (units/g-min) | rate (units/real-min @ fast) | F | G | I | farm | upkeep food |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `peaspa` | Peasant | 12.50 | 4.8 | **6.7** | 100 | 0 | 0 | 1 | 32 |

### `vendip` — Diplomatic Center

| Юнит | имя | buildtime (g-sec) | rate (units/g-min) | rate (units/real-min @ fast) | F | G | I | farm | upkeep food |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `archerdip` | Archer (mercenary) | 1.50 | 40.0 | **56.0** | 20 | 1 | 0 | 1 | — |
| `archerturdip` | Turkish archer (mercenary) | 1.50 | 40.0 | **56.0** | 20 | 1 | 0 | 1 | — |
| `cossacksichdip` | Sich Cossack (mercenary) | 16.50 | 3.6 | **5.1** | 75 | 2 | 5 | 1 | — |
| `dragoon18dip` | Dragoon, 18th century (mercenary) | 15.00 | 4.0 | **5.6** | 90 | 7 | 5 | 1 | floor(gc_obj_foodperunit*2) |
| `grenadierdip` | Grenadier (mercenary) | 6.00 | 10.0 | **14.0** | 80 | 60 | 40 | 1 | floor(gc_obj_foodperunit*1.2) |
| `lightcavalrydip` | Light cavalry (mercenary) | 15.00 | 4.0 | **5.6** | 90 | 7 | 5 | 1 | floor(gc_obj_foodperunit*2) |
| `lightinfantrydip` | Light Infantryman (mercenary) | 1.00 | 60.0 | **84.0** | 25 | 0 | 1 | 1 | — |
| `roundshierdip` | Roundshier (mercenary) | 4.00 | 15.0 | **21.0** | 20 | 3 | 25 | 1 | — |

### `vensta` — Stable

| Юнит | имя | buildtime (g-sec) | rate (units/g-min) | rate (units/real-min @ fast) | F | G | I | farm | upkeep food |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `cuirassier` | Cuirassier | 24.00 | 2.5 | **3.5** | 120 | 10 | 40 | 1 | floor(gc_obj_foodperunit*2.5) |
| `dragoon` | Dragoon, 17th century | 15.00 | 4.0 | **5.6** | 90 | 7 | 5 | 1 | floor(gc_obj_foodperunit*2) |
| `dragoon18` | Dragoon, 18th century | 15.00 | 4.0 | **5.6** | 90 | 7 | 5 | 1 | floor(gc_obj_foodperunit*2) |
| `hussar` | Hussar | 16.50 | 3.6 | **5.1** | 75 | 2 | 5 | 1 | — |
| `reiter` | Reiter | 24.00 | 2.5 | **3.5** | 120 | 10 | 40 | 1 | floor(gc_obj_foodperunit*2.5) |

### `ventem` — Cathedral

| Юнит | имя | buildtime (g-sec) | rate (units/g-min) | rate (units/real-min @ fast) | F | G | I | farm | upkeep food |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `priest` | Priest | 15.00 | 4.0 | **5.6** | 30 | 10 | 0 | 1 | — |

---

## Замечания

1. **farm = 1 для каждого юнита** — каждый юнит занимает 1 слот популяции (контролируется `gPlayer.farm`). Зданиям, увеличивающим лимит — `cen=+100, hou=+25, bar=+150, ba2=+250` и т.д.
2. **upkeep food** — потребление еды/g-sec, делится на 32 для игр-секунды (см. `gc_obj_foodperunit`). Стандарт = 32 для пехоты, 26 для рус крестьян, 40+ для тяжёлой кавалерии.
3. **При нехватке farm production стоит** — здание попытается списать ресурс, но units не выйдет, прогресс заморожен.
4. **N зданий = N×rate.** 5 бараков пехотных = 5 × ~13 musketeer/min @ fast = ~65 musketeer/min.