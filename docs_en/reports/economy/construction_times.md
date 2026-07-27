<a id="cossacks-3--время-постройки-и-ремонта"></a>
<a id="время-строительства-и-ремонта"></a>
# Construction and Repair Times

[← Tables and calculations](../README.md)

The tables compare the time needed to construct a new building and to repair
a completely damaged one. Results are shown for several numbers of Peasants.

**Formulas** (see [construction and repair](../../recon/world/economy/building_mechanics.md)):

- **Construction with N Peasants:** `buildtime_sec × 1.13 / N`, subject to
  the building's builder limit.
- **Repair with N Peasants:** `maxhp / (20 × N / 0.406)` game seconds.
- One construction animation cycle lasts 13 frames, or **0.406 game
  seconds**.
- At Fast speed, divide game time by 1.4 to obtain real time.

**Slot caps** (exact simulation of `_unit_CalcBuilderPoints` for each building, see [builder limits](builder_slots.md)):

- The limit depends on the building's collision-mask perimeter. National
  versions of the same building can therefore accept different numbers of
  builders.
- A wall segment accepts **four** builders.
- The engine never allows more than **30**.

Each duration explicitly distinguishes game time from real time at Fast speed.
Long durations are shown in minutes.

<a id="alg--algeria-алжир"></a>
<a id="алжир-alg"></a>
## Algeria (`alg`)
<a id="постройка-с-нуля"></a>
### Building from scratch

| Building | Base build time, game s | Builder limit | 1 Peasant | 2 Peasants | 5 Peasants | 10 Peasants | At slot limit |
| --- | --- | --- | --- | --- | --- | --- | --- |
| **Minaret** (`algaca`) | 156 | 25 | 2.9 game min (2.1 real min) | 1.5 game min (1.1 real min) | 35 game s (25 real s) | 18 game s (13 real s) | 7 game s (5 real s) |
| **Artillery Depot** (`algart`) | 246 | 24 | 4.6 game min (3.3 real min) | 2.3 game min (1.7 real min) | 56 game s (40 real s) | 28 game s (20 real s) | 12 game s (8 real s) |
| **Barracks** (`algbar`) | 94 | 23 | 1.8 game min (1.3 real min) | 53 game s (38 real s) | 21 game s (15 real s) | 11 game s (8 real s) | 5 game s (3 real s) |
| **Blacksmith** (`algbla`) | 109 | 15 | 2.1 game min (1.5 real min) | 1.0 game min (0.7 real min) | 25 game s (18 real s) | 12 game s (9 real s) | 8 game s (6 real s) |
| **Town Hall** (`algcen`) | 156 | 21 | 2.9 game min (2.1 real min) | 1.5 game min (1.1 real min) | 35 game s (25 real s) | 18 game s (13 real s) | 8 game s (6 real s) |
| **Diplomatic Center** (`algdip`) | 312 | 18 | 5.9 game min (4.2 real min) | 2.9 game min (2.1 real min) | 1.2 game min (0.8 real min) | 35 game s (25 real s) | 20 game s (14 real s) |
| **Housing** (`alghou`) | 31 | 16 | 35 game s (25 real s) | 18 game s (13 real s) | 7 game s (5 real s) | 4 game s (3 real s) | 2 game s (2 real s) |
| **Stable** (`algsta`) | 156 | 22 | 2.9 game min (2.1 real min) | 1.5 game min (1.1 real min) | 35 game s (25 real s) | 18 game s (13 real s) | 8 game s (6 real s) |
| **Mosque** (`algtem`) | 94 | 30 | 1.8 game min (1.3 real min) | 53 game s (38 real s) | 21 game s (15 real s) | 11 game s (8 real s) | 4 game s (3 real s) |
| **Mine** (`eurcoa`) | 94 | 16 | 1.8 game min (1.3 real min) | 53 game s (38 real s) | 21 game s (15 real s) | 11 game s (8 real s) | 7 game s (5 real s) |
| **Mine** (`eurgol`) | 94 | 16 | 1.8 game min (1.3 real min) | 53 game s (38 real s) | 21 game s (15 real s) | 11 game s (8 real s) | 7 game s (5 real s) |
| **Mine** (`euriro`) | 94 | 16 | 1.8 game min (1.3 real min) | 53 game s (38 real s) | 21 game s (15 real s) | 11 game s (8 real s) | 7 game s (5 real s) |
| **Bazaar** (`turmar`) | 234 | 19 | 4.4 game min (3.2 real min) | 2.2 game min (1.6 real min) | 53 game s (38 real s) | 26 game s (19 real s) | 14 game s (10 real s) |
| **Mill** (`turmil`) | 94 | 16 | 1.8 game min (1.3 real min) | 53 game s (38 real s) | 21 game s (15 real s) | 11 game s (8 real s) | 7 game s (5 real s) |
| **Shipyard** (`turpor`) | 1562 | 30 | 29.4 game min (21.0 real min) | 14.7 game min (10.5 real min) | 5.9 game min (4.2 real min) | 2.9 game min (2.1 real min) | 59 game s (42 real s) |
| **Gate** (`tursga`) | 120 | 13 | 2.3 game min (1.6 real min) | 1.1 game min (0.8 real min) | 27 game s (19 real s) | 14 game s (10 real s) | 10 game s (7 real s) |
| **Storehouse** (`tursto`) | 31 | 8 | 35 game s (25 real s) | 18 game s (13 real s) | 7 game s (5 real s) | 4 game s (3 real s) | 4 game s (3 real s) |
| **Wall** (`turswa`) | 120 | 4 | 2.3 game min (1.6 real min) | 1.1 game min (0.8 real min) | 34 game s (24 real s) | 34 game s (24 real s) | 34 game s (24 real s) |
| **Tower** (`turtow`) | 984 | 14 | 18.5 game min (13.2 real min) | 9.3 game min (6.6 real min) | 3.7 game min (2.6 real min) | 1.9 game min (1.3 real min) | 1.3 game min (0.9 real min) |
| **Gate** (`ukrwga`) | 6 | 13 | 6 game s (5 real s) | 3 game s (2 real s) | 1 game s (1 real s) | 1 game s (0 real s) | 0 game s (0 real s) |
| **Palisade** (`ukrwwa`) | 6 | 4 | 6 game s (5 real s) | 3 game s (2 real s) | 2 game s (1 real s) | 2 game s (1 real s) | 2 game s (1 real s) |

<a id="полный-ремонт"></a>
### Full repair (0 → max HP)
| Building | Maximum health | Builder limit | 1 Peasant | 2 Peasants | 5 Peasants | 10 Peasants | At slot limit |
| --- | --- | --- | --- | --- | --- | --- | --- |
| **Minaret** (`algaca`) | 65000 | 25 | 22.0 game min (15.7 real min) | 11.0 game min (7.9 real min) | 4.4 game min (3.1 real min) | 2.2 game min (1.6 real min) | 53 game s (38 real s) |
| **Artillery Depot** (`algart`) | 40000 | 24 | 13.5 game min (9.7 real min) | 6.8 game min (4.8 real min) | 2.7 game min (1.9 real min) | 1.4 game min (1.0 real min) | 34 game s (24 real s) |
| **Barracks** (`algbar`) | 35000 | 23 | 11.8 game min (8.5 real min) | 5.9 game min (4.2 real min) | 2.4 game min (1.7 real min) | 1.2 game min (0.8 real min) | 31 game s (22 real s) |
| **Blacksmith** (`algbla`) | 6500 | 15 | 2.2 game min (1.6 real min) | 1.1 game min (0.8 real min) | 26 game s (19 real s) | 13 game s (9 real s) | 9 game s (6 real s) |
| **Town Hall** (`algcen`) | 5500 | 21 | 1.9 game min (1.3 real min) | 56 game s (40 real s) | 22 game s (16 real s) | 11 game s (8 real s) | 5 game s (4 real s) |
| **Diplomatic Center** (`algdip`) | 5500 | 18 | 1.9 game min (1.3 real min) | 56 game s (40 real s) | 22 game s (16 real s) | 11 game s (8 real s) | 6 game s (4 real s) |
| **Housing** (`alghou`) | 4300 | 16 | 1.5 game min (1.0 real min) | 44 game s (31 real s) | 17 game s (12 real s) | 9 game s (6 real s) | 5 game s (4 real s) |
| **Stable** (`algsta`) | 55000 | 22 | 18.6 game min (13.3 real min) | 9.3 game min (6.6 real min) | 3.7 game min (2.7 real min) | 1.9 game min (1.3 real min) | 51 game s (36 real s) |
| **Mosque** (`algtem`) | 5000 | 30 | 1.7 game min (1.2 real min) | 51 game s (36 real s) | 20 game s (15 real s) | 10 game s (7 real s) | 3 game s (2 real s) |
| **Mine** (`eurcoa`) | 2500 | 16 | 51 game s (36 real s) | 25 game s (18 real s) | 10 game s (7 real s) | 5 game s (4 real s) | 3 game s (2 real s) |
| **Mine** (`eurgol`) | 2500 | 16 | 51 game s (36 real s) | 25 game s (18 real s) | 10 game s (7 real s) | 5 game s (4 real s) | 3 game s (2 real s) |
| **Mine** (`euriro`) | 2500 | 16 | 51 game s (36 real s) | 25 game s (18 real s) | 10 game s (7 real s) | 5 game s (4 real s) | 3 game s (2 real s) |
| **Bazaar** (`turmar`) | 4500 | 19 | 1.5 game min (1.1 real min) | 46 game s (33 real s) | 18 game s (13 real s) | 9 game s (7 real s) | 5 game s (3 real s) |
| **Mill** (`turmil`) | 20000 | 16 | 6.8 game min (4.8 real min) | 3.4 game min (2.4 real min) | 1.4 game min (1.0 real min) | 41 game s (29 real s) | 25 game s (18 real s) |
| **Shipyard** (`turpor`) | 40000 | 30 | 13.5 game min (9.7 real min) | 6.8 game min (4.8 real min) | 2.7 game min (1.9 real min) | 1.4 game min (1.0 real min) | 27 game s (19 real s) |
| **Gate** (`tursga`) | 32000 | 13 | 10.8 game min (7.7 real min) | 5.4 game min (3.9 real min) | 2.2 game min (1.5 real min) | 1.1 game min (0.8 real min) | 50 game s (36 real s) |
| **Storehouse** (`tursto`) | 10000 | 8 | 3.4 game min (2.4 real min) | 1.7 game min (1.2 real min) | 41 game s (29 real s) | 25 game s (18 real s) | 25 game s (18 real s) |
| **Wall** (`turswa`) | 50000 | 4 | 16.9 game min (12.1 real min) | 8.5 game min (6.0 real min) | 4.2 game min (3.0 real min) | 4.2 game min (3.0 real min) | 4.2 game min (3.0 real min) |
| **Tower** (`turtow`) | 22500 | 14 | 7.6 game min (5.4 real min) | 3.8 game min (2.7 real min) | 1.5 game min (1.1 real min) | 46 game s (33 real s) | 33 game s (23 real s) |
| **Gate** (`ukrwga`) | 1500 | 13 | 30 game s (22 real s) | 15 game s (11 real s) | 6 game s (4 real s) | 3 game s (2 real s) | 2 game s (2 real s) |
| **Palisade** (`ukrwwa`) | 1500 | 4 | 30 game s (22 real s) | 15 game s (11 real s) | 8 game s (5 real s) | 8 game s (5 real s) | 8 game s (5 real s) |

<a id="aus--austria-австрия"></a>
<a id="австрия-aus"></a>
## Austria (`aus`)
<a id="постройка-с-нуля-1"></a>
### Building from scratch

| Building | Base build time, game s | Builder limit | 1 Peasant | 2 Peasants | 5 Peasants | 10 Peasants | At slot limit |
| --- | --- | --- | --- | --- | --- | --- | --- |
| **Academy** (`ausaca`) | 625 | 26 | 11.8 game min (8.4 real min) | 5.9 game min (4.2 real min) | 2.4 game min (1.7 real min) | 1.2 game min (0.8 real min) | 27 game s (19 real s) |
| **Artillery Depot** (`ausart`) | 246 | 22 | 4.6 game min (3.3 real min) | 2.3 game min (1.7 real min) | 56 game s (40 real s) | 28 game s (20 real s) | 13 game s (9 real s) |
| **Barracks, 18th century** (`ausba2`) | 5625 | 29 | 105.9 game min (75.7 real min) | 53.0 game min (37.8 real min) | 21.2 game min (15.1 real min) | 10.6 game min (7.6 real min) | 3.7 game min (2.6 real min) |
| **Barracks, 17th century** (`ausbar`) | 94 | 25 | 1.8 game min (1.3 real min) | 53 game s (38 real s) | 21 game s (15 real s) | 11 game s (8 real s) | 4 game s (3 real s) |
| **Blacksmith** (`ausbla`) | 94 | 17 | 1.8 game min (1.3 real min) | 53 game s (38 real s) | 21 game s (15 real s) | 11 game s (8 real s) | 6 game s (4 real s) |
| **Town Hall** (`auscen`) | 47 | 23 | 53 game s (38 real s) | 26 game s (19 real s) | 11 game s (8 real s) | 5 game s (4 real s) | 2 game s (2 real s) |
| **Diplomatic Center** (`ausdip`) | 312 | 24 | 5.9 game min (4.2 real min) | 2.9 game min (2.1 real min) | 1.2 game min (0.8 real min) | 35 game s (25 real s) | 15 game s (11 real s) |
| **Housing** (`aushou`) | 31 | 15 | 35 game s (25 real s) | 18 game s (13 real s) | 7 game s (5 real s) | 4 game s (3 real s) | 2 game s (2 real s) |
| **Stable** (`aussta`) | 625 | 21 | 11.8 game min (8.4 real min) | 5.9 game min (4.2 real min) | 2.4 game min (1.7 real min) | 1.2 game min (0.8 real min) | 34 game s (24 real s) |
| **Cathedral** (`austem`) | 156 | 28 | 2.9 game min (2.1 real min) | 1.5 game min (1.1 real min) | 35 game s (25 real s) | 18 game s (13 real s) | 6 game s (5 real s) |
| **Mine** (`eurcoa`) | 94 | 16 | 1.8 game min (1.3 real min) | 53 game s (38 real s) | 21 game s (15 real s) | 11 game s (8 real s) | 7 game s (5 real s) |
| **Mine** (`eurgol`) | 94 | 16 | 1.8 game min (1.3 real min) | 53 game s (38 real s) | 21 game s (15 real s) | 11 game s (8 real s) | 7 game s (5 real s) |
| **Mine** (`euriro`) | 94 | 16 | 1.8 game min (1.3 real min) | 53 game s (38 real s) | 21 game s (15 real s) | 11 game s (8 real s) | 7 game s (5 real s) |
| **Market** (`eurmar`) | 234 | 25 | 4.4 game min (3.2 real min) | 2.2 game min (1.6 real min) | 53 game s (38 real s) | 26 game s (19 real s) | 11 game s (8 real s) |
| **Mill** (`eurmil`) | 94 | 10 | 1.8 game min (1.3 real min) | 53 game s (38 real s) | 21 game s (15 real s) | 11 game s (8 real s) | 11 game s (8 real s) |
| **Shipyard** (`eurpor`) | 1562 | 30 | 29.4 game min (21.0 real min) | 14.7 game min (10.5 real min) | 5.9 game min (4.2 real min) | 2.9 game min (2.1 real min) | 59 game s (42 real s) |
| **Gate** (`eursga`) | 90 | 13 | 1.7 game min (1.2 real min) | 51 game s (36 real s) | 20 game s (15 real s) | 10 game s (7 real s) | 8 game s (6 real s) |
| **Storehouse** (`eursto`) | 31 | 9 | 35 game s (25 real s) | 18 game s (13 real s) | 7 game s (5 real s) | 4 game s (3 real s) | 4 game s (3 real s) |
| **Wall** (`eurswa`) | 90 | 4 | 1.7 game min (1.2 real min) | 51 game s (36 real s) | 25 game s (18 real s) | 25 game s (18 real s) | 25 game s (18 real s) |
| **Tower** (`eurtow`) | 1230 | 10 | 23.2 game min (16.6 real min) | 11.6 game min (8.3 real min) | 4.6 game min (3.3 real min) | 2.3 game min (1.7 real min) | 2.3 game min (1.7 real min) |
| **Gate** (`ukrwga`) | 6 | 13 | 6 game s (5 real s) | 3 game s (2 real s) | 1 game s (1 real s) | 1 game s (0 real s) | 0 game s (0 real s) |
| **Palisade** (`ukrwwa`) | 6 | 4 | 6 game s (5 real s) | 3 game s (2 real s) | 2 game s (1 real s) | 2 game s (1 real s) | 2 game s (1 real s) |

<a id="полный-ремонт-0--max-hp"></a>
<a id="полный-ремонт-1"></a>
### Full repair (0 → max HP)

| Building | Maximum health | Builder limit | 1 Peasant | 2 Peasants | 5 Peasants | 10 Peasants | At slot limit |
| --- | --- | --- | --- | --- | --- | --- | --- |
| **Academy** (`ausaca`) | 65000 | 26 | 22.0 game min (15.7 real min) | 11.0 game min (7.9 real min) | 4.4 game min (3.1 real min) | 2.2 game min (1.6 real min) | 51 game s (36 real s) |
| **Artillery Depot** (`ausart`) | 40000 | 22 | 13.5 game min (9.7 real min) | 6.8 game min (4.8 real min) | 2.7 game min (1.9 real min) | 1.4 game min (1.0 real min) | 37 game s (26 real s) |
| **Barracks, 18th century** (`ausba2`) | 55000 | 29 | 18.6 game min (13.3 real min) | 9.3 game min (6.6 real min) | 3.7 game min (2.7 real min) | 1.9 game min (1.3 real min) | 39 game s (28 real s) |
| **Barracks, 17th century** (`ausbar`) | 40000 | 25 | 13.5 game min (9.7 real min) | 6.8 game min (4.8 real min) | 2.7 game min (1.9 real min) | 1.4 game min (1.0 real min) | 32 game s (23 real s) |
| **Blacksmith** (`ausbla`) | 5500 | 17 | 1.9 game min (1.3 real min) | 56 game s (40 real s) | 22 game s (16 real s) | 11 game s (8 real s) | 7 game s (5 real s) |
| **Town Hall** (`auscen`) | 4000 | 23 | 1.4 game min (1.0 real min) | 41 game s (29 real s) | 16 game s (12 real s) | 8 game s (6 real s) | 4 game s (3 real s) |
| **Diplomatic Center** (`ausdip`) | 4500 | 24 | 1.5 game min (1.1 real min) | 46 game s (33 real s) | 18 game s (13 real s) | 9 game s (7 real s) | 4 game s (3 real s) |
| **Housing** (`aushou`) | 4000 | 15 | 1.4 game min (1.0 real min) | 41 game s (29 real s) | 16 game s (12 real s) | 8 game s (6 real s) | 5 game s (4 real s) |
| **Stable** (`aussta`) | 20000 | 21 | 6.8 game min (4.8 real min) | 3.4 game min (2.4 real min) | 1.4 game min (1.0 real min) | 41 game s (29 real s) | 19 game s (14 real s) |
| **Cathedral** (`austem`) | 4200 | 28 | 1.4 game min (1.0 real min) | 43 game s (30 real s) | 17 game s (12 real s) | 9 game s (6 real s) | 3 game s (2 real s) |
| **Mine** (`eurcoa`) | 2500 | 16 | 51 game s (36 real s) | 25 game s (18 real s) | 10 game s (7 real s) | 5 game s (4 real s) | 3 game s (2 real s) |
| **Mine** (`eurgol`) | 2500 | 16 | 51 game s (36 real s) | 25 game s (18 real s) | 10 game s (7 real s) | 5 game s (4 real s) | 3 game s (2 real s) |
| **Mine** (`euriro`) | 2500 | 16 | 51 game s (36 real s) | 25 game s (18 real s) | 10 game s (7 real s) | 5 game s (4 real s) | 3 game s (2 real s) |
| **Market** (`eurmar`) | 4000 | 25 | 1.4 game min (1.0 real min) | 41 game s (29 real s) | 16 game s (12 real s) | 8 game s (6 real s) | 3 game s (2 real s) |
| **Mill** (`eurmil`) | 20000 | 10 | 6.8 game min (4.8 real min) | 3.4 game min (2.4 real min) | 1.4 game min (1.0 real min) | 41 game s (29 real s) | 41 game s (29 real s) |
| **Shipyard** (`eurpor`) | 50000 | 30 | 16.9 game min (12.1 real min) | 8.5 game min (6.0 real min) | 3.4 game min (2.4 real min) | 1.7 game min (1.2 real min) | 34 game s (24 real s) |
| **Gate** (`eursga`) | 32000 | 13 | 10.8 game min (7.7 real min) | 5.4 game min (3.9 real min) | 2.2 game min (1.5 real min) | 1.1 game min (0.8 real min) | 50 game s (36 real s) |
| **Storehouse** (`eursto`) | 10000 | 9 | 3.4 game min (2.4 real min) | 1.7 game min (1.2 real min) | 41 game s (29 real s) | 23 game s (16 real s) | 23 game s (16 real s) |
| **Wall** (`eurswa`) | 50000 | 4 | 16.9 game min (12.1 real min) | 8.5 game min (6.0 real min) | 4.2 game min (3.0 real min) | 4.2 game min (3.0 real min) | 4.2 game min (3.0 real min) |
| **Tower** (`eurtow`) | 20000 | 10 | 6.8 game min (4.8 real min) | 3.4 game min (2.4 real min) | 1.4 game min (1.0 real min) | 41 game s (29 real s) | 41 game s (29 real s) |
| **Gate** (`ukrwga`) | 1500 | 13 | 30 game s (22 real s) | 15 game s (11 real s) | 6 game s (4 real s) | 3 game s (2 real s) | 2 game s (2 real s) |
| **Palisade** (`ukrwwa`) | 1500 | 4 | 30 game s (22 real s) | 15 game s (11 real s) | 8 game s (5 real s) | 8 game s (5 real s) | 8 game s (5 real s) |

<a id="bav--bavaria-бавария"></a>
<a id="бавария-bav"></a>
## Bavaria (`bav`)
<a id="постройка-с-нуля-2"></a>
### Building from scratch

| Building | Base build time, game s | Builder limit | 1 Peasant | 2 Peasants | 5 Peasants | 10 Peasants | At slot limit |
| --- | --- | --- | --- | --- | --- | --- | --- |
| **Academy** (`bavaca`) | 625 | 22 | 11.8 game min (8.4 real min) | 5.9 game min (4.2 real min) | 2.4 game min (1.7 real min) | 1.2 game min (0.8 real min) | 32 game s (23 real s) |
| **Artillery Depot** (`bavart`) | 246 | 20 | 4.6 game min (3.3 real min) | 2.3 game min (1.7 real min) | 56 game s (40 real s) | 28 game s (20 real s) | 14 game s (10 real s) |
| **Barracks, 18th century** (`bavba2`) | 5625 | 23 | 105.9 game min (75.7 real min) | 53.0 game min (37.8 real min) | 21.2 game min (15.1 real min) | 10.6 game min (7.6 real min) | 4.6 game min (3.3 real min) |
| **Barracks, 17th century** (`bavbar`) | 94 | 23 | 1.8 game min (1.3 real min) | 53 game s (38 real s) | 21 game s (15 real s) | 11 game s (8 real s) | 5 game s (3 real s) |
| **Blacksmith** (`bavbla`) | 94 | 16 | 1.8 game min (1.3 real min) | 53 game s (38 real s) | 21 game s (15 real s) | 11 game s (8 real s) | 7 game s (5 real s) |
| **Town Hall** (`bavcen`) | 156 | 21 | 2.9 game min (2.1 real min) | 1.5 game min (1.1 real min) | 35 game s (25 real s) | 18 game s (13 real s) | 8 game s (6 real s) |
| **Diplomatic Center** (`bavdip`) | 312 | 18 | 5.9 game min (4.2 real min) | 2.9 game min (2.1 real min) | 1.2 game min (0.8 real min) | 35 game s (25 real s) | 20 game s (14 real s) |
| **Housing** (`bavhou`) | 31 | 16 | 35 game s (25 real s) | 18 game s (13 real s) | 7 game s (5 real s) | 4 game s (3 real s) | 2 game s (2 real s) |
| **Stable** (`bavsta`) | 625 | 21 | 11.8 game min (8.4 real min) | 5.9 game min (4.2 real min) | 2.4 game min (1.7 real min) | 1.2 game min (0.8 real min) | 34 game s (24 real s) |
| **Cathedral** (`bavtem`) | 156 | 22 | 2.9 game min (2.1 real min) | 1.5 game min (1.1 real min) | 35 game s (25 real s) | 18 game s (13 real s) | 8 game s (6 real s) |
| **Mine** (`eurcoa`) | 94 | 16 | 1.8 game min (1.3 real min) | 53 game s (38 real s) | 21 game s (15 real s) | 11 game s (8 real s) | 7 game s (5 real s) |
| **Mine** (`eurgol`) | 94 | 16 | 1.8 game min (1.3 real min) | 53 game s (38 real s) | 21 game s (15 real s) | 11 game s (8 real s) | 7 game s (5 real s) |
| **Mine** (`euriro`) | 94 | 16 | 1.8 game min (1.3 real min) | 53 game s (38 real s) | 21 game s (15 real s) | 11 game s (8 real s) | 7 game s (5 real s) |
| **Market** (`eurmar`) | 234 | 25 | 4.4 game min (3.2 real min) | 2.2 game min (1.6 real min) | 53 game s (38 real s) | 26 game s (19 real s) | 11 game s (8 real s) |
| **Mill** (`eurmil`) | 94 | 10 | 1.8 game min (1.3 real min) | 53 game s (38 real s) | 21 game s (15 real s) | 11 game s (8 real s) | 11 game s (8 real s) |
| **Shipyard** (`eurpor`) | 1562 | 30 | 29.4 game min (21.0 real min) | 14.7 game min (10.5 real min) | 5.9 game min (4.2 real min) | 2.9 game min (2.1 real min) | 59 game s (42 real s) |
| **Gate** (`eursga`) | 90 | 13 | 1.7 game min (1.2 real min) | 51 game s (36 real s) | 20 game s (15 real s) | 10 game s (7 real s) | 8 game s (6 real s) |
| **Storehouse** (`eursto`) | 31 | 9 | 35 game s (25 real s) | 18 game s (13 real s) | 7 game s (5 real s) | 4 game s (3 real s) | 4 game s (3 real s) |
| **Wall** (`eurswa`) | 90 | 4 | 1.7 game min (1.2 real min) | 51 game s (36 real s) | 25 game s (18 real s) | 25 game s (18 real s) | 25 game s (18 real s) |
| **Tower** (`eurtow`) | 1230 | 10 | 23.2 game min (16.6 real min) | 11.6 game min (8.3 real min) | 4.6 game min (3.3 real min) | 2.3 game min (1.7 real min) | 2.3 game min (1.7 real min) |
| **Gate** (`ukrwga`) | 6 | 13 | 6 game s (5 real s) | 3 game s (2 real s) | 1 game s (1 real s) | 1 game s (0 real s) | 0 game s (0 real s) |
| **Palisade** (`ukrwwa`) | 6 | 4 | 6 game s (5 real s) | 3 game s (2 real s) | 2 game s (1 real s) | 2 game s (1 real s) | 2 game s (1 real s) |

<a id="полный-ремонт-0--max-hp-1"></a>
<a id="полный-ремонт-2"></a>
### Full repair (0 → max HP)

| Building | Maximum health | Builder limit | 1 Peasant | 2 Peasants | 5 Peasants | 10 Peasants | At slot limit |
| --- | --- | --- | --- | --- | --- | --- | --- |
| **Academy** (`bavaca`) | 63000 | 22 | 21.3 game min (15.2 real min) | 10.7 game min (7.6 real min) | 4.3 game min (3.0 real min) | 2.1 game min (1.5 real min) | 58 game s (42 real s) |
| **Artillery Depot** (`bavart`) | 40000 | 20 | 13.5 game min (9.7 real min) | 6.8 game min (4.8 real min) | 2.7 game min (1.9 real min) | 1.4 game min (1.0 real min) | 41 game s (29 real s) |
| **Barracks, 18th century** (`bavba2`) | 55000 | 23 | 18.6 game min (13.3 real min) | 9.3 game min (6.6 real min) | 3.7 game min (2.7 real min) | 1.9 game min (1.3 real min) | 49 game s (35 real s) |
| **Barracks, 17th century** (`bavbar`) | 40000 | 23 | 13.5 game min (9.7 real min) | 6.8 game min (4.8 real min) | 2.7 game min (1.9 real min) | 1.4 game min (1.0 real min) | 35 game s (25 real s) |
| **Blacksmith** (`bavbla`) | 5500 | 16 | 1.9 game min (1.3 real min) | 56 game s (40 real s) | 22 game s (16 real s) | 11 game s (8 real s) | 7 game s (5 real s) |
| **Town Hall** (`bavcen`) | 4000 | 21 | 1.4 game min (1.0 real min) | 41 game s (29 real s) | 16 game s (12 real s) | 8 game s (6 real s) | 4 game s (3 real s) |
| **Diplomatic Center** (`bavdip`) | 4500 | 18 | 1.5 game min (1.1 real min) | 46 game s (33 real s) | 18 game s (13 real s) | 9 game s (7 real s) | 5 game s (4 real s) |
| **Housing** (`bavhou`) | 4000 | 16 | 1.4 game min (1.0 real min) | 41 game s (29 real s) | 16 game s (12 real s) | 8 game s (6 real s) | 5 game s (4 real s) |
| **Stable** (`bavsta`) | 20000 | 21 | 6.8 game min (4.8 real min) | 3.4 game min (2.4 real min) | 1.4 game min (1.0 real min) | 41 game s (29 real s) | 19 game s (14 real s) |
| **Cathedral** (`bavtem`) | 4200 | 22 | 1.4 game min (1.0 real min) | 43 game s (30 real s) | 17 game s (12 real s) | 9 game s (6 real s) | 4 game s (3 real s) |
| **Mine** (`eurcoa`) | 2500 | 16 | 51 game s (36 real s) | 25 game s (18 real s) | 10 game s (7 real s) | 5 game s (4 real s) | 3 game s (2 real s) |
| **Mine** (`eurgol`) | 2500 | 16 | 51 game s (36 real s) | 25 game s (18 real s) | 10 game s (7 real s) | 5 game s (4 real s) | 3 game s (2 real s) |
| **Mine** (`euriro`) | 2500 | 16 | 51 game s (36 real s) | 25 game s (18 real s) | 10 game s (7 real s) | 5 game s (4 real s) | 3 game s (2 real s) |
| **Market** (`eurmar`) | 4000 | 25 | 1.4 game min (1.0 real min) | 41 game s (29 real s) | 16 game s (12 real s) | 8 game s (6 real s) | 3 game s (2 real s) |
| **Mill** (`eurmil`) | 20000 | 10 | 6.8 game min (4.8 real min) | 3.4 game min (2.4 real min) | 1.4 game min (1.0 real min) | 41 game s (29 real s) | 41 game s (29 real s) |
| **Shipyard** (`eurpor`) | 50000 | 30 | 16.9 game min (12.1 real min) | 8.5 game min (6.0 real min) | 3.4 game min (2.4 real min) | 1.7 game min (1.2 real min) | 34 game s (24 real s) |
| **Gate** (`eursga`) | 32000 | 13 | 10.8 game min (7.7 real min) | 5.4 game min (3.9 real min) | 2.2 game min (1.5 real min) | 1.1 game min (0.8 real min) | 50 game s (36 real s) |
| **Storehouse** (`eursto`) | 10000 | 9 | 3.4 game min (2.4 real min) | 1.7 game min (1.2 real min) | 41 game s (29 real s) | 23 game s (16 real s) | 23 game s (16 real s) |
| **Wall** (`eurswa`) | 50000 | 4 | 16.9 game min (12.1 real min) | 8.5 game min (6.0 real min) | 4.2 game min (3.0 real min) | 4.2 game min (3.0 real min) | 4.2 game min (3.0 real min) |
| **Tower** (`eurtow`) | 20000 | 10 | 6.8 game min (4.8 real min) | 3.4 game min (2.4 real min) | 1.4 game min (1.0 real min) | 41 game s (29 real s) | 41 game s (29 real s) |
| **Gate** (`ukrwga`) | 1500 | 13 | 30 game s (22 real s) | 15 game s (11 real s) | 6 game s (4 real s) | 3 game s (2 real s) | 2 game s (2 real s) |
| **Palisade** (`ukrwwa`) | 1500 | 4 | 30 game s (22 real s) | 15 game s (11 real s) | 8 game s (5 real s) | 8 game s (5 real s) | 8 game s (5 real s) |

<a id="den--denmark-дания"></a>
<a id="дания-den"></a>
## Denmark (`den`)
<a id="постройка-с-нуля-3"></a>
### Building from scratch

| Building | Base build time, game s | Builder limit | 1 Peasant | 2 Peasants | 5 Peasants | 10 Peasants | At slot limit |
| --- | --- | --- | --- | --- | --- | --- | --- |
| **Academy** (`denaca`) | 625 | 17 | 11.8 game min (8.4 real min) | 5.9 game min (4.2 real min) | 2.4 game min (1.7 real min) | 1.2 game min (0.8 real min) | 42 game s (30 real s) |
| **Artillery Depot** (`denart`) | 246 | 20 | 4.6 game min (3.3 real min) | 2.3 game min (1.7 real min) | 56 game s (40 real s) | 28 game s (20 real s) | 14 game s (10 real s) |
| **Barracks, 18th century** (`denba2`) | 5625 | 22 | 105.9 game min (75.7 real min) | 53.0 game min (37.8 real min) | 21.2 game min (15.1 real min) | 10.6 game min (7.6 real min) | 4.8 game min (3.4 real min) |
| **Barracks, 17th century** (`denbar`) | 94 | 20 | 1.8 game min (1.3 real min) | 53 game s (38 real s) | 21 game s (15 real s) | 11 game s (8 real s) | 5 game s (4 real s) |
| **Blacksmith** (`denbla`) | 94 | 16 | 1.8 game min (1.3 real min) | 53 game s (38 real s) | 21 game s (15 real s) | 11 game s (8 real s) | 7 game s (5 real s) |
| **Town Hall** (`dencen`) | 156 | 20 | 2.9 game min (2.1 real min) | 1.5 game min (1.1 real min) | 35 game s (25 real s) | 18 game s (13 real s) | 9 game s (6 real s) |
| **Diplomatic Center** (`dendip`) | 312 | 21 | 5.9 game min (4.2 real min) | 2.9 game min (2.1 real min) | 1.2 game min (0.8 real min) | 35 game s (25 real s) | 17 game s (12 real s) |
| **Housing** (`denhou`) | 31 | 13 | 35 game s (25 real s) | 18 game s (13 real s) | 7 game s (5 real s) | 4 game s (3 real s) | 3 game s (2 real s) |
| **Stable** (`densta`) | 625 | 20 | 11.8 game min (8.4 real min) | 5.9 game min (4.2 real min) | 2.4 game min (1.7 real min) | 1.2 game min (0.8 real min) | 35 game s (25 real s) |
| **Cathedral** (`dentem`) | 156 | 22 | 2.9 game min (2.1 real min) | 1.5 game min (1.1 real min) | 35 game s (25 real s) | 18 game s (13 real s) | 8 game s (6 real s) |
| **Mine** (`eurcoa`) | 94 | 16 | 1.8 game min (1.3 real min) | 53 game s (38 real s) | 21 game s (15 real s) | 11 game s (8 real s) | 7 game s (5 real s) |
| **Mine** (`eurgol`) | 94 | 16 | 1.8 game min (1.3 real min) | 53 game s (38 real s) | 21 game s (15 real s) | 11 game s (8 real s) | 7 game s (5 real s) |
| **Mine** (`euriro`) | 94 | 16 | 1.8 game min (1.3 real min) | 53 game s (38 real s) | 21 game s (15 real s) | 11 game s (8 real s) | 7 game s (5 real s) |
| **Market** (`eurmar`) | 234 | 25 | 4.4 game min (3.2 real min) | 2.2 game min (1.6 real min) | 53 game s (38 real s) | 26 game s (19 real s) | 11 game s (8 real s) |
| **Mill** (`eurmil`) | 94 | 10 | 1.8 game min (1.3 real min) | 53 game s (38 real s) | 21 game s (15 real s) | 11 game s (8 real s) | 11 game s (8 real s) |
| **Shipyard** (`eurpor`) | 1562 | 30 | 29.4 game min (21.0 real min) | 14.7 game min (10.5 real min) | 5.9 game min (4.2 real min) | 2.9 game min (2.1 real min) | 59 game s (42 real s) |
| **Gate** (`eursga`) | 90 | 13 | 1.7 game min (1.2 real min) | 51 game s (36 real s) | 20 game s (15 real s) | 10 game s (7 real s) | 8 game s (6 real s) |
| **Storehouse** (`eursto`) | 31 | 9 | 35 game s (25 real s) | 18 game s (13 real s) | 7 game s (5 real s) | 4 game s (3 real s) | 4 game s (3 real s) |
| **Wall** (`eurswa`) | 90 | 4 | 1.7 game min (1.2 real min) | 51 game s (36 real s) | 25 game s (18 real s) | 25 game s (18 real s) | 25 game s (18 real s) |
| **Tower** (`eurtow`) | 1230 | 10 | 23.2 game min (16.6 real min) | 11.6 game min (8.3 real min) | 4.6 game min (3.3 real min) | 2.3 game min (1.7 real min) | 2.3 game min (1.7 real min) |
| **Gate** (`ukrwga`) | 6 | 13 | 6 game s (5 real s) | 3 game s (2 real s) | 1 game s (1 real s) | 1 game s (0 real s) | 0 game s (0 real s) |
| **Palisade** (`ukrwwa`) | 6 | 4 | 6 game s (5 real s) | 3 game s (2 real s) | 2 game s (1 real s) | 2 game s (1 real s) | 2 game s (1 real s) |

<a id="полный-ремонт-0--max-hp-2"></a>
<a id="полный-ремонт-3"></a>
### Full repair (0 → max HP)

| Building | Maximum health | Builder limit | 1 Peasant | 2 Peasants | 5 Peasants | 10 Peasants | At slot limit |
| --- | --- | --- | --- | --- | --- | --- | --- |
| **Academy** (`denaca`) | 63000 | 17 | 21.3 game min (15.2 real min) | 10.7 game min (7.6 real min) | 4.3 game min (3.0 real min) | 2.1 game min (1.5 real min) | 1.3 game min (0.9 real min) |
| **Artillery Depot** (`denart`) | 40000 | 20 | 13.5 game min (9.7 real min) | 6.8 game min (4.8 real min) | 2.7 game min (1.9 real min) | 1.4 game min (1.0 real min) | 41 game s (29 real s) |
| **Barracks, 18th century** (`denba2`) | 55000 | 22 | 18.6 game min (13.3 real min) | 9.3 game min (6.6 real min) | 3.7 game min (2.7 real min) | 1.9 game min (1.3 real min) | 51 game s (36 real s) |
| **Barracks, 17th century** (`denbar`) | 40000 | 20 | 13.5 game min (9.7 real min) | 6.8 game min (4.8 real min) | 2.7 game min (1.9 real min) | 1.4 game min (1.0 real min) | 41 game s (29 real s) |
| **Blacksmith** (`denbla`) | 5500 | 16 | 1.9 game min (1.3 real min) | 56 game s (40 real s) | 22 game s (16 real s) | 11 game s (8 real s) | 7 game s (5 real s) |
| **Town Hall** (`dencen`) | 4030 | 20 | 1.4 game min (1.0 real min) | 41 game s (29 real s) | 16 game s (12 real s) | 8 game s (6 real s) | 4 game s (3 real s) |
| **Diplomatic Center** (`dendip`) | 4500 | 21 | 1.5 game min (1.1 real min) | 46 game s (33 real s) | 18 game s (13 real s) | 9 game s (7 real s) | 4 game s (3 real s) |
| **Housing** (`denhou`) | 4000 | 13 | 1.4 game min (1.0 real min) | 41 game s (29 real s) | 16 game s (12 real s) | 8 game s (6 real s) | 6 game s (4 real s) |
| **Stable** (`densta`) | 20000 | 20 | 6.8 game min (4.8 real min) | 3.4 game min (2.4 real min) | 1.4 game min (1.0 real min) | 41 game s (29 real s) | 20 game s (15 real s) |
| **Cathedral** (`dentem`) | 4200 | 22 | 1.4 game min (1.0 real min) | 43 game s (30 real s) | 17 game s (12 real s) | 9 game s (6 real s) | 4 game s (3 real s) |
| **Mine** (`eurcoa`) | 2500 | 16 | 51 game s (36 real s) | 25 game s (18 real s) | 10 game s (7 real s) | 5 game s (4 real s) | 3 game s (2 real s) |
| **Mine** (`eurgol`) | 2500 | 16 | 51 game s (36 real s) | 25 game s (18 real s) | 10 game s (7 real s) | 5 game s (4 real s) | 3 game s (2 real s) |
| **Mine** (`euriro`) | 2500 | 16 | 51 game s (36 real s) | 25 game s (18 real s) | 10 game s (7 real s) | 5 game s (4 real s) | 3 game s (2 real s) |
| **Market** (`eurmar`) | 4000 | 25 | 1.4 game min (1.0 real min) | 41 game s (29 real s) | 16 game s (12 real s) | 8 game s (6 real s) | 3 game s (2 real s) |
| **Mill** (`eurmil`) | 20000 | 10 | 6.8 game min (4.8 real min) | 3.4 game min (2.4 real min) | 1.4 game min (1.0 real min) | 41 game s (29 real s) | 41 game s (29 real s) |
| **Shipyard** (`eurpor`) | 50000 | 30 | 16.9 game min (12.1 real min) | 8.5 game min (6.0 real min) | 3.4 game min (2.4 real min) | 1.7 game min (1.2 real min) | 34 game s (24 real s) |
| **Gate** (`eursga`) | 32000 | 13 | 10.8 game min (7.7 real min) | 5.4 game min (3.9 real min) | 2.2 game min (1.5 real min) | 1.1 game min (0.8 real min) | 50 game s (36 real s) |
| **Storehouse** (`eursto`) | 10000 | 9 | 3.4 game min (2.4 real min) | 1.7 game min (1.2 real min) | 41 game s (29 real s) | 23 game s (16 real s) | 23 game s (16 real s) |
| **Wall** (`eurswa`) | 50000 | 4 | 16.9 game min (12.1 real min) | 8.5 game min (6.0 real min) | 4.2 game min (3.0 real min) | 4.2 game min (3.0 real min) | 4.2 game min (3.0 real min) |
| **Tower** (`eurtow`) | 20000 | 10 | 6.8 game min (4.8 real min) | 3.4 game min (2.4 real min) | 1.4 game min (1.0 real min) | 41 game s (29 real s) | 41 game s (29 real s) |
| **Gate** (`ukrwga`) | 1500 | 13 | 30 game s (22 real s) | 15 game s (11 real s) | 6 game s (4 real s) | 3 game s (2 real s) | 2 game s (2 real s) |
| **Palisade** (`ukrwwa`) | 1500 | 4 | 30 game s (22 real s) | 15 game s (11 real s) | 8 game s (5 real s) | 8 game s (5 real s) | 8 game s (5 real s) |

<a id="eng--england-англия"></a>
<a id="англия-eng"></a>
## England (`eng`)
<a id="постройка-с-нуля-4"></a>
### Building from scratch

| Building | Base build time, game s | Builder limit | 1 Peasant | 2 Peasants | 5 Peasants | 10 Peasants | At slot limit |
| --- | --- | --- | --- | --- | --- | --- | --- |
| **Academy** (`engaca`) | 625 | 23 | 11.8 game min (8.4 real min) | 5.9 game min (4.2 real min) | 2.4 game min (1.7 real min) | 1.2 game min (0.8 real min) | 31 game s (22 real s) |
| **Artillery Depot** (`engart`) | 246 | 22 | 4.6 game min (3.3 real min) | 2.3 game min (1.7 real min) | 56 game s (40 real s) | 28 game s (20 real s) | 13 game s (9 real s) |
| **Barracks, 18th century** (`engba2`) | 5625 | 23 | 105.9 game min (75.7 real min) | 53.0 game min (37.8 real min) | 21.2 game min (15.1 real min) | 10.6 game min (7.6 real min) | 4.6 game min (3.3 real min) |
| **Barracks, 17th century** (`engbar`) | 94 | 22 | 1.8 game min (1.3 real min) | 53 game s (38 real s) | 21 game s (15 real s) | 11 game s (8 real s) | 5 game s (3 real s) |
| **Blacksmith** (`engbla`) | 94 | 16 | 1.8 game min (1.3 real min) | 53 game s (38 real s) | 21 game s (15 real s) | 11 game s (8 real s) | 7 game s (5 real s) |
| **Town Hall** (`engcen`) | 156 | 23 | 2.9 game min (2.1 real min) | 1.5 game min (1.1 real min) | 35 game s (25 real s) | 18 game s (13 real s) | 8 game s (5 real s) |
| **Diplomatic Center** (`engdip`) | 312 | 16 | 5.9 game min (4.2 real min) | 2.9 game min (2.1 real min) | 1.2 game min (0.8 real min) | 35 game s (25 real s) | 22 game s (16 real s) |
| **Housing** (`enghou`) | 31 | 15 | 35 game s (25 real s) | 18 game s (13 real s) | 7 game s (5 real s) | 4 game s (3 real s) | 2 game s (2 real s) |
| **Stable** (`engsta`) | 375 | 22 | 7.1 game min (5.0 real min) | 3.5 game min (2.5 real min) | 1.4 game min (1.0 real min) | 42 game s (30 real s) | 19 game s (14 real s) |
| **Cathedral** (`engtem`) | 156 | 24 | 2.9 game min (2.1 real min) | 1.5 game min (1.1 real min) | 35 game s (25 real s) | 18 game s (13 real s) | 7 game s (5 real s) |
| **Mine** (`eurcoa`) | 94 | 16 | 1.8 game min (1.3 real min) | 53 game s (38 real s) | 21 game s (15 real s) | 11 game s (8 real s) | 7 game s (5 real s) |
| **Mine** (`eurgol`) | 94 | 16 | 1.8 game min (1.3 real min) | 53 game s (38 real s) | 21 game s (15 real s) | 11 game s (8 real s) | 7 game s (5 real s) |
| **Mine** (`euriro`) | 94 | 16 | 1.8 game min (1.3 real min) | 53 game s (38 real s) | 21 game s (15 real s) | 11 game s (8 real s) | 7 game s (5 real s) |
| **Market** (`eurmar`) | 234 | 25 | 4.4 game min (3.2 real min) | 2.2 game min (1.6 real min) | 53 game s (38 real s) | 26 game s (19 real s) | 11 game s (8 real s) |
| **Mill** (`eurmil`) | 94 | 10 | 1.8 game min (1.3 real min) | 53 game s (38 real s) | 21 game s (15 real s) | 11 game s (8 real s) | 11 game s (8 real s) |
| **Shipyard** (`eurpor`) | 1562 | 30 | 29.4 game min (21.0 real min) | 14.7 game min (10.5 real min) | 5.9 game min (4.2 real min) | 2.9 game min (2.1 real min) | 59 game s (42 real s) |
| **Gate** (`eursga`) | 90 | 13 | 1.7 game min (1.2 real min) | 51 game s (36 real s) | 20 game s (15 real s) | 10 game s (7 real s) | 8 game s (6 real s) |
| **Storehouse** (`eursto`) | 31 | 9 | 35 game s (25 real s) | 18 game s (13 real s) | 7 game s (5 real s) | 4 game s (3 real s) | 4 game s (3 real s) |
| **Wall** (`eurswa`) | 90 | 4 | 1.7 game min (1.2 real min) | 51 game s (36 real s) | 25 game s (18 real s) | 25 game s (18 real s) | 25 game s (18 real s) |
| **Tower** (`eurtow`) | 1230 | 10 | 23.2 game min (16.6 real min) | 11.6 game min (8.3 real min) | 4.6 game min (3.3 real min) | 2.3 game min (1.7 real min) | 2.3 game min (1.7 real min) |
| **Gate** (`ukrwga`) | 6 | 13 | 6 game s (5 real s) | 3 game s (2 real s) | 1 game s (1 real s) | 1 game s (0 real s) | 0 game s (0 real s) |
| **Palisade** (`ukrwwa`) | 6 | 4 | 6 game s (5 real s) | 3 game s (2 real s) | 2 game s (1 real s) | 2 game s (1 real s) | 2 game s (1 real s) |

<a id="полный-ремонт-0--max-hp-3"></a>
<a id="полный-ремонт-4"></a>
### Full repair (0 → max HP)

| Building | Maximum health | Builder limit | 1 Peasant | 2 Peasants | 5 Peasants | 10 Peasants | At slot limit |
| --- | --- | --- | --- | --- | --- | --- | --- |
| **Academy** (`engaca`) | 63000 | 23 | 21.3 game min (15.2 real min) | 10.7 game min (7.6 real min) | 4.3 game min (3.0 real min) | 2.1 game min (1.5 real min) | 56 game s (40 real s) |
| **Artillery Depot** (`engart`) | 40000 | 22 | 13.5 game min (9.7 real min) | 6.8 game min (4.8 real min) | 2.7 game min (1.9 real min) | 1.4 game min (1.0 real min) | 37 game s (26 real s) |
| **Barracks, 18th century** (`engba2`) | 55000 | 23 | 18.6 game min (13.3 real min) | 9.3 game min (6.6 real min) | 3.7 game min (2.7 real min) | 1.9 game min (1.3 real min) | 49 game s (35 real s) |
| **Barracks, 17th century** (`engbar`) | 40000 | 22 | 13.5 game min (9.7 real min) | 6.8 game min (4.8 real min) | 2.7 game min (1.9 real min) | 1.4 game min (1.0 real min) | 37 game s (26 real s) |
| **Blacksmith** (`engbla`) | 5500 | 16 | 1.9 game min (1.3 real min) | 56 game s (40 real s) | 22 game s (16 real s) | 11 game s (8 real s) | 7 game s (5 real s) |
| **Town Hall** (`engcen`) | 4030 | 23 | 1.4 game min (1.0 real min) | 41 game s (29 real s) | 16 game s (12 real s) | 8 game s (6 real s) | 4 game s (3 real s) |
| **Diplomatic Center** (`engdip`) | 4500 | 16 | 1.5 game min (1.1 real min) | 46 game s (33 real s) | 18 game s (13 real s) | 9 game s (7 real s) | 6 game s (4 real s) |
| **Housing** (`enghou`) | 5000 | 15 | 1.7 game min (1.2 real min) | 51 game s (36 real s) | 20 game s (15 real s) | 10 game s (7 real s) | 7 game s (5 real s) |
| **Stable** (`engsta`) | 25000 | 22 | 8.5 game min (6.0 real min) | 4.2 game min (3.0 real min) | 1.7 game min (1.2 real min) | 51 game s (36 real s) | 23 game s (16 real s) |
| **Cathedral** (`engtem`) | 4200 | 24 | 1.4 game min (1.0 real min) | 43 game s (30 real s) | 17 game s (12 real s) | 9 game s (6 real s) | 4 game s (3 real s) |
| **Mine** (`eurcoa`) | 2500 | 16 | 51 game s (36 real s) | 25 game s (18 real s) | 10 game s (7 real s) | 5 game s (4 real s) | 3 game s (2 real s) |
| **Mine** (`eurgol`) | 2500 | 16 | 51 game s (36 real s) | 25 game s (18 real s) | 10 game s (7 real s) | 5 game s (4 real s) | 3 game s (2 real s) |
| **Mine** (`euriro`) | 2500 | 16 | 51 game s (36 real s) | 25 game s (18 real s) | 10 game s (7 real s) | 5 game s (4 real s) | 3 game s (2 real s) |
| **Market** (`eurmar`) | 4000 | 25 | 1.4 game min (1.0 real min) | 41 game s (29 real s) | 16 game s (12 real s) | 8 game s (6 real s) | 3 game s (2 real s) |
| **Mill** (`eurmil`) | 20000 | 10 | 6.8 game min (4.8 real min) | 3.4 game min (2.4 real min) | 1.4 game min (1.0 real min) | 41 game s (29 real s) | 41 game s (29 real s) |
| **Shipyard** (`eurpor`) | 50000 | 30 | 16.9 game min (12.1 real min) | 8.5 game min (6.0 real min) | 3.4 game min (2.4 real min) | 1.7 game min (1.2 real min) | 34 game s (24 real s) |
| **Gate** (`eursga`) | 32000 | 13 | 10.8 game min (7.7 real min) | 5.4 game min (3.9 real min) | 2.2 game min (1.5 real min) | 1.1 game min (0.8 real min) | 50 game s (36 real s) |
| **Storehouse** (`eursto`) | 10000 | 9 | 3.4 game min (2.4 real min) | 1.7 game min (1.2 real min) | 41 game s (29 real s) | 23 game s (16 real s) | 23 game s (16 real s) |
| **Wall** (`eurswa`) | 50000 | 4 | 16.9 game min (12.1 real min) | 8.5 game min (6.0 real min) | 4.2 game min (3.0 real min) | 4.2 game min (3.0 real min) | 4.2 game min (3.0 real min) |
| **Tower** (`eurtow`) | 20000 | 10 | 6.8 game min (4.8 real min) | 3.4 game min (2.4 real min) | 1.4 game min (1.0 real min) | 41 game s (29 real s) | 41 game s (29 real s) |
| **Gate** (`ukrwga`) | 1500 | 13 | 30 game s (22 real s) | 15 game s (11 real s) | 6 game s (4 real s) | 3 game s (2 real s) | 2 game s (2 real s) |
| **Palisade** (`ukrwwa`) | 1500 | 4 | 30 game s (22 real s) | 15 game s (11 real s) | 8 game s (5 real s) | 8 game s (5 real s) | 8 game s (5 real s) |

<a id="fra--france-франция"></a>
<a id="франция-fra"></a>
## France (`fra`)
<a id="постройка-с-нуля-5"></a>
### Building from scratch

| Building | Base build time, game s | Builder limit | 1 Peasant | 2 Peasants | 5 Peasants | 10 Peasants | At slot limit |
| --- | --- | --- | --- | --- | --- | --- | --- |
| **Mine** (`eurcoa`) | 94 | 16 | 1.8 game min (1.3 real min) | 53 game s (38 real s) | 21 game s (15 real s) | 11 game s (8 real s) | 7 game s (5 real s) |
| **Mine** (`eurgol`) | 94 | 16 | 1.8 game min (1.3 real min) | 53 game s (38 real s) | 21 game s (15 real s) | 11 game s (8 real s) | 7 game s (5 real s) |
| **Mine** (`euriro`) | 94 | 16 | 1.8 game min (1.3 real min) | 53 game s (38 real s) | 21 game s (15 real s) | 11 game s (8 real s) | 7 game s (5 real s) |
| **Market** (`eurmar`) | 234 | 25 | 4.4 game min (3.2 real min) | 2.2 game min (1.6 real min) | 53 game s (38 real s) | 26 game s (19 real s) | 11 game s (8 real s) |
| **Mill** (`eurmil`) | 94 | 10 | 1.8 game min (1.3 real min) | 53 game s (38 real s) | 21 game s (15 real s) | 11 game s (8 real s) | 11 game s (8 real s) |
| **Shipyard** (`eurpor`) | 1562 | 30 | 29.4 game min (21.0 real min) | 14.7 game min (10.5 real min) | 5.9 game min (4.2 real min) | 2.9 game min (2.1 real min) | 59 game s (42 real s) |
| **Gate** (`eursga`) | 90 | 13 | 1.7 game min (1.2 real min) | 51 game s (36 real s) | 20 game s (15 real s) | 10 game s (7 real s) | 8 game s (6 real s) |
| **Storehouse** (`eursto`) | 31 | 9 | 35 game s (25 real s) | 18 game s (13 real s) | 7 game s (5 real s) | 4 game s (3 real s) | 4 game s (3 real s) |
| **Wall** (`eurswa`) | 90 | 4 | 1.7 game min (1.2 real min) | 51 game s (36 real s) | 25 game s (18 real s) | 25 game s (18 real s) | 25 game s (18 real s) |
| **Tower** (`eurtow`) | 1230 | 10 | 23.2 game min (16.6 real min) | 11.6 game min (8.3 real min) | 4.6 game min (3.3 real min) | 2.3 game min (1.7 real min) | 2.3 game min (1.7 real min) |
| **Academy** (`fraaca`) | 625 | 24 | 11.8 game min (8.4 real min) | 5.9 game min (4.2 real min) | 2.4 game min (1.7 real min) | 1.2 game min (0.8 real min) | 29 game s (21 real s) |
| **Artillery Depot** (`fraart`) | 246 | 24 | 4.6 game min (3.3 real min) | 2.3 game min (1.7 real min) | 56 game s (40 real s) | 28 game s (20 real s) | 12 game s (8 real s) |
| **Barracks, 18th century** (`fraba2`) | 5625 | 29 | 105.9 game min (75.7 real min) | 53.0 game min (37.8 real min) | 21.2 game min (15.1 real min) | 10.6 game min (7.6 real min) | 3.7 game min (2.6 real min) |
| **Barracks, 17th century** (`frabar`) | 94 | 16 | 1.8 game min (1.3 real min) | 53 game s (38 real s) | 21 game s (15 real s) | 11 game s (8 real s) | 7 game s (5 real s) |
| **Blacksmith** (`frabla`) | 94 | 13 | 1.8 game min (1.3 real min) | 53 game s (38 real s) | 21 game s (15 real s) | 11 game s (8 real s) | 8 game s (6 real s) |
| **Town Hall** (`fracen`) | 156 | 27 | 2.9 game min (2.1 real min) | 1.5 game min (1.1 real min) | 35 game s (25 real s) | 18 game s (13 real s) | 7 game s (5 real s) |
| **Diplomatic Center** (`fradip`) | 312 | 18 | 5.9 game min (4.2 real min) | 2.9 game min (2.1 real min) | 1.2 game min (0.8 real min) | 35 game s (25 real s) | 20 game s (14 real s) |
| **Housing** (`frahou`) | 31 | 10 | 35 game s (25 real s) | 18 game s (13 real s) | 7 game s (5 real s) | 4 game s (3 real s) | 4 game s (3 real s) |
| **Stable** (`frasta`) | 625 | 22 | 11.8 game min (8.4 real min) | 5.9 game min (4.2 real min) | 2.4 game min (1.7 real min) | 1.2 game min (0.8 real min) | 32 game s (23 real s) |
| **Cathedral** (`fratem`) | 312 | 30 | 5.9 game min (4.2 real min) | 2.9 game min (2.1 real min) | 1.2 game min (0.8 real min) | 35 game s (25 real s) | 12 game s (8 real s) |
| **Gate** (`ukrwga`) | 6 | 13 | 6 game s (5 real s) | 3 game s (2 real s) | 1 game s (1 real s) | 1 game s (0 real s) | 0 game s (0 real s) |
| **Palisade** (`ukrwwa`) | 6 | 4 | 6 game s (5 real s) | 3 game s (2 real s) | 2 game s (1 real s) | 2 game s (1 real s) | 2 game s (1 real s) |

<a id="полный-ремонт-0--max-hp-4"></a>
<a id="полный-ремонт-5"></a>
### Full repair (0 → max HP)

| Building | Maximum health | Builder limit | 1 Peasant | 2 Peasants | 5 Peasants | 10 Peasants | At slot limit |
| --- | --- | --- | --- | --- | --- | --- | --- |
| **Mine** (`eurcoa`) | 2500 | 16 | 51 game s (36 real s) | 25 game s (18 real s) | 10 game s (7 real s) | 5 game s (4 real s) | 3 game s (2 real s) |
| **Mine** (`eurgol`) | 2500 | 16 | 51 game s (36 real s) | 25 game s (18 real s) | 10 game s (7 real s) | 5 game s (4 real s) | 3 game s (2 real s) |
| **Mine** (`euriro`) | 2500 | 16 | 51 game s (36 real s) | 25 game s (18 real s) | 10 game s (7 real s) | 5 game s (4 real s) | 3 game s (2 real s) |
| **Market** (`eurmar`) | 4000 | 25 | 1.4 game min (1.0 real min) | 41 game s (29 real s) | 16 game s (12 real s) | 8 game s (6 real s) | 3 game s (2 real s) |
| **Mill** (`eurmil`) | 20000 | 10 | 6.8 game min (4.8 real min) | 3.4 game min (2.4 real min) | 1.4 game min (1.0 real min) | 41 game s (29 real s) | 41 game s (29 real s) |
| **Shipyard** (`eurpor`) | 50000 | 30 | 16.9 game min (12.1 real min) | 8.5 game min (6.0 real min) | 3.4 game min (2.4 real min) | 1.7 game min (1.2 real min) | 34 game s (24 real s) |
| **Gate** (`eursga`) | 32000 | 13 | 10.8 game min (7.7 real min) | 5.4 game min (3.9 real min) | 2.2 game min (1.5 real min) | 1.1 game min (0.8 real min) | 50 game s (36 real s) |
| **Storehouse** (`eursto`) | 10000 | 9 | 3.4 game min (2.4 real min) | 1.7 game min (1.2 real min) | 41 game s (29 real s) | 23 game s (16 real s) | 23 game s (16 real s) |
| **Wall** (`eurswa`) | 50000 | 4 | 16.9 game min (12.1 real min) | 8.5 game min (6.0 real min) | 4.2 game min (3.0 real min) | 4.2 game min (3.0 real min) | 4.2 game min (3.0 real min) |
| **Tower** (`eurtow`) | 20000 | 10 | 6.8 game min (4.8 real min) | 3.4 game min (2.4 real min) | 1.4 game min (1.0 real min) | 41 game s (29 real s) | 41 game s (29 real s) |
| **Academy** (`fraaca`) | 63000 | 24 | 21.3 game min (15.2 real min) | 10.7 game min (7.6 real min) | 4.3 game min (3.0 real min) | 2.1 game min (1.5 real min) | 53 game s (38 real s) |
| **Artillery Depot** (`fraart`) | 40000 | 24 | 13.5 game min (9.7 real min) | 6.8 game min (4.8 real min) | 2.7 game min (1.9 real min) | 1.4 game min (1.0 real min) | 34 game s (24 real s) |
| **Barracks, 18th century** (`fraba2`) | 55000 | 29 | 18.6 game min (13.3 real min) | 9.3 game min (6.6 real min) | 3.7 game min (2.7 real min) | 1.9 game min (1.3 real min) | 39 game s (28 real s) |
| **Barracks, 17th century** (`frabar`) | 40000 | 16 | 13.5 game min (9.7 real min) | 6.8 game min (4.8 real min) | 2.7 game min (1.9 real min) | 1.4 game min (1.0 real min) | 51 game s (36 real s) |
| **Blacksmith** (`frabla`) | 5500 | 13 | 1.9 game min (1.3 real min) | 56 game s (40 real s) | 22 game s (16 real s) | 11 game s (8 real s) | 9 game s (6 real s) |
| **Town Hall** (`fracen`) | 4500 | 27 | 1.5 game min (1.1 real min) | 46 game s (33 real s) | 18 game s (13 real s) | 9 game s (7 real s) | 3 game s (2 real s) |
| **Diplomatic Center** (`fradip`) | 4500 | 18 | 1.5 game min (1.1 real min) | 46 game s (33 real s) | 18 game s (13 real s) | 9 game s (7 real s) | 5 game s (4 real s) |
| **Housing** (`frahou`) | 4000 | 10 | 1.4 game min (1.0 real min) | 41 game s (29 real s) | 16 game s (12 real s) | 8 game s (6 real s) | 8 game s (6 real s) |
| **Stable** (`frasta`) | 20000 | 22 | 6.8 game min (4.8 real min) | 3.4 game min (2.4 real min) | 1.4 game min (1.0 real min) | 41 game s (29 real s) | 18 game s (13 real s) |
| **Cathedral** (`fratem`) | 6000 | 30 | 2.0 game min (1.5 real min) | 1.0 game min (0.7 real min) | 24 game s (17 real s) | 12 game s (9 real s) | 4 game s (3 real s) |
| **Gate** (`ukrwga`) | 1500 | 13 | 30 game s (22 real s) | 15 game s (11 real s) | 6 game s (4 real s) | 3 game s (2 real s) | 2 game s (2 real s) |
| **Palisade** (`ukrwwa`) | 1500 | 4 | 30 game s (22 real s) | 15 game s (11 real s) | 8 game s (5 real s) | 8 game s (5 real s) | 8 game s (5 real s) |

<a id="hun--hungary-венгрия"></a>
<a id="венгрия-hun"></a>
## Hungary (`hun`)
<a id="постройка-с-нуля-6"></a>
### Building from scratch

| Building | Base build time, game s | Builder limit | 1 Peasant | 2 Peasants | 5 Peasants | 10 Peasants | At slot limit |
| --- | --- | --- | --- | --- | --- | --- | --- |
| **Mine** (`eurcoa`) | 94 | 16 | 1.8 game min (1.3 real min) | 53 game s (38 real s) | 21 game s (15 real s) | 11 game s (8 real s) | 7 game s (5 real s) |
| **Mine** (`eurgol`) | 94 | 16 | 1.8 game min (1.3 real min) | 53 game s (38 real s) | 21 game s (15 real s) | 11 game s (8 real s) | 7 game s (5 real s) |
| **Mine** (`euriro`) | 94 | 16 | 1.8 game min (1.3 real min) | 53 game s (38 real s) | 21 game s (15 real s) | 11 game s (8 real s) | 7 game s (5 real s) |
| **Market** (`eurmar`) | 234 | 25 | 4.4 game min (3.2 real min) | 2.2 game min (1.6 real min) | 53 game s (38 real s) | 26 game s (19 real s) | 11 game s (8 real s) |
| **Mill** (`eurmil`) | 94 | 10 | 1.8 game min (1.3 real min) | 53 game s (38 real s) | 21 game s (15 real s) | 11 game s (8 real s) | 11 game s (8 real s) |
| **Shipyard** (`eurpor`) | 1562 | 30 | 29.4 game min (21.0 real min) | 14.7 game min (10.5 real min) | 5.9 game min (4.2 real min) | 2.9 game min (2.1 real min) | 59 game s (42 real s) |
| **Gate** (`eursga`) | 90 | 13 | 1.7 game min (1.2 real min) | 51 game s (36 real s) | 20 game s (15 real s) | 10 game s (7 real s) | 8 game s (6 real s) |
| **Storehouse** (`eursto`) | 31 | 9 | 35 game s (25 real s) | 18 game s (13 real s) | 7 game s (5 real s) | 4 game s (3 real s) | 4 game s (3 real s) |
| **Wall** (`eurswa`) | 90 | 4 | 1.7 game min (1.2 real min) | 51 game s (36 real s) | 25 game s (18 real s) | 25 game s (18 real s) | 25 game s (18 real s) |
| **Tower** (`eurtow`) | 1230 | 10 | 23.2 game min (16.6 real min) | 11.6 game min (8.3 real min) | 4.6 game min (3.3 real min) | 2.3 game min (1.7 real min) | 2.3 game min (1.7 real min) |
| **Academy** (`hunaca`) | 625 | 19 | 11.8 game min (8.4 real min) | 5.9 game min (4.2 real min) | 2.4 game min (1.7 real min) | 1.2 game min (0.8 real min) | 37 game s (27 real s) |
| **Artillery Depot** (`hunart`) | 246 | 18 | 4.6 game min (3.3 real min) | 2.3 game min (1.7 real min) | 56 game s (40 real s) | 28 game s (20 real s) | 15 game s (11 real s) |
| **Barracks, 18th century** (`hunba2`) | 5625 | 26 | 105.9 game min (75.7 real min) | 53.0 game min (37.8 real min) | 21.2 game min (15.1 real min) | 10.6 game min (7.6 real min) | 4.1 game min (2.9 real min) |
| **Barracks, 17th century** (`hunbar`) | 94 | 22 | 1.8 game min (1.3 real min) | 53 game s (38 real s) | 21 game s (15 real s) | 11 game s (8 real s) | 5 game s (3 real s) |
| **Blacksmith** (`hunbla`) | 94 | 13 | 1.8 game min (1.3 real min) | 53 game s (38 real s) | 21 game s (15 real s) | 11 game s (8 real s) | 8 game s (6 real s) |
| **Town Hall** (`huncen`) | 156 | 22 | 2.9 game min (2.1 real min) | 1.5 game min (1.1 real min) | 35 game s (25 real s) | 18 game s (13 real s) | 8 game s (6 real s) |
| **Diplomatic Center** (`hundip`) | 312 | 18 | 5.9 game min (4.2 real min) | 2.9 game min (2.1 real min) | 1.2 game min (0.8 real min) | 35 game s (25 real s) | 20 game s (14 real s) |
| **Housing** (`hunhou`) | 31 | 14 | 35 game s (25 real s) | 18 game s (13 real s) | 7 game s (5 real s) | 4 game s (3 real s) | 3 game s (2 real s) |
| **Stable** (`hunsta`) | 625 | 19 | 11.8 game min (8.4 real min) | 5.9 game min (4.2 real min) | 2.4 game min (1.7 real min) | 1.2 game min (0.8 real min) | 37 game s (27 real s) |
| **Cathedral** (`huntem`) | 156 | 28 | 2.9 game min (2.1 real min) | 1.5 game min (1.1 real min) | 35 game s (25 real s) | 18 game s (13 real s) | 6 game s (5 real s) |
| **Gate** (`ukrwga`) | 6 | 13 | 6 game s (5 real s) | 3 game s (2 real s) | 1 game s (1 real s) | 1 game s (0 real s) | 0 game s (0 real s) |
| **Palisade** (`ukrwwa`) | 6 | 4 | 6 game s (5 real s) | 3 game s (2 real s) | 2 game s (1 real s) | 2 game s (1 real s) | 2 game s (1 real s) |

<a id="полный-ремонт-0--max-hp-5"></a>
<a id="полный-ремонт-6"></a>
### Full repair (0 → max HP)

| Building | Maximum health | Builder limit | 1 Peasant | 2 Peasants | 5 Peasants | 10 Peasants | At slot limit |
| --- | --- | --- | --- | --- | --- | --- | --- |
| **Mine** (`eurcoa`) | 2500 | 16 | 51 game s (36 real s) | 25 game s (18 real s) | 10 game s (7 real s) | 5 game s (4 real s) | 3 game s (2 real s) |
| **Mine** (`eurgol`) | 2500 | 16 | 51 game s (36 real s) | 25 game s (18 real s) | 10 game s (7 real s) | 5 game s (4 real s) | 3 game s (2 real s) |
| **Mine** (`euriro`) | 2500 | 16 | 51 game s (36 real s) | 25 game s (18 real s) | 10 game s (7 real s) | 5 game s (4 real s) | 3 game s (2 real s) |
| **Market** (`eurmar`) | 4000 | 25 | 1.4 game min (1.0 real min) | 41 game s (29 real s) | 16 game s (12 real s) | 8 game s (6 real s) | 3 game s (2 real s) |
| **Mill** (`eurmil`) | 20000 | 10 | 6.8 game min (4.8 real min) | 3.4 game min (2.4 real min) | 1.4 game min (1.0 real min) | 41 game s (29 real s) | 41 game s (29 real s) |
| **Shipyard** (`eurpor`) | 50000 | 30 | 16.9 game min (12.1 real min) | 8.5 game min (6.0 real min) | 3.4 game min (2.4 real min) | 1.7 game min (1.2 real min) | 34 game s (24 real s) |
| **Gate** (`eursga`) | 32000 | 13 | 10.8 game min (7.7 real min) | 5.4 game min (3.9 real min) | 2.2 game min (1.5 real min) | 1.1 game min (0.8 real min) | 50 game s (36 real s) |
| **Storehouse** (`eursto`) | 10000 | 9 | 3.4 game min (2.4 real min) | 1.7 game min (1.2 real min) | 41 game s (29 real s) | 23 game s (16 real s) | 23 game s (16 real s) |
| **Wall** (`eurswa`) | 50000 | 4 | 16.9 game min (12.1 real min) | 8.5 game min (6.0 real min) | 4.2 game min (3.0 real min) | 4.2 game min (3.0 real min) | 4.2 game min (3.0 real min) |
| **Tower** (`eurtow`) | 20000 | 10 | 6.8 game min (4.8 real min) | 3.4 game min (2.4 real min) | 1.4 game min (1.0 real min) | 41 game s (29 real s) | 41 game s (29 real s) |
| **Academy** (`hunaca`) | 63000 | 19 | 21.3 game min (15.2 real min) | 10.7 game min (7.6 real min) | 4.3 game min (3.0 real min) | 2.1 game min (1.5 real min) | 1.1 game min (0.8 real min) |
| **Artillery Depot** (`hunart`) | 40000 | 18 | 13.5 game min (9.7 real min) | 6.8 game min (4.8 real min) | 2.7 game min (1.9 real min) | 1.4 game min (1.0 real min) | 45 game s (32 real s) |
| **Barracks, 18th century** (`hunba2`) | 55000 | 26 | 18.6 game min (13.3 real min) | 9.3 game min (6.6 real min) | 3.7 game min (2.7 real min) | 1.9 game min (1.3 real min) | 43 game s (31 real s) |
| **Barracks, 17th century** (`hunbar`) | 40000 | 22 | 13.5 game min (9.7 real min) | 6.8 game min (4.8 real min) | 2.7 game min (1.9 real min) | 1.4 game min (1.0 real min) | 37 game s (26 real s) |
| **Blacksmith** (`hunbla`) | 5500 | 13 | 1.9 game min (1.3 real min) | 56 game s (40 real s) | 22 game s (16 real s) | 11 game s (8 real s) | 9 game s (6 real s) |
| **Town Hall** (`huncen`) | 4000 | 22 | 1.4 game min (1.0 real min) | 41 game s (29 real s) | 16 game s (12 real s) | 8 game s (6 real s) | 4 game s (3 real s) |
| **Diplomatic Center** (`hundip`) | 4500 | 18 | 1.5 game min (1.1 real min) | 46 game s (33 real s) | 18 game s (13 real s) | 9 game s (7 real s) | 5 game s (4 real s) |
| **Housing** (`hunhou`) | 4000 | 14 | 1.4 game min (1.0 real min) | 41 game s (29 real s) | 16 game s (12 real s) | 8 game s (6 real s) | 6 game s (4 real s) |
| **Stable** (`hunsta`) | 20000 | 19 | 6.8 game min (4.8 real min) | 3.4 game min (2.4 real min) | 1.4 game min (1.0 real min) | 41 game s (29 real s) | 21 game s (15 real s) |
| **Cathedral** (`huntem`) | 4200 | 28 | 1.4 game min (1.0 real min) | 43 game s (30 real s) | 17 game s (12 real s) | 9 game s (6 real s) | 3 game s (2 real s) |
| **Gate** (`ukrwga`) | 1500 | 13 | 30 game s (22 real s) | 15 game s (11 real s) | 6 game s (4 real s) | 3 game s (2 real s) | 2 game s (2 real s) |
| **Palisade** (`ukrwwa`) | 1500 | 4 | 30 game s (22 real s) | 15 game s (11 real s) | 8 game s (5 real s) | 8 game s (5 real s) | 8 game s (5 real s) |

<a id="net--netherlands-нидерланды"></a>
<a id="нидерланды-net"></a>
## Netherlands (`net`)
<a id="постройка-с-нуля-7"></a>
### Building from scratch

| Building | Base build time, game s | Builder limit | 1 Peasant | 2 Peasants | 5 Peasants | 10 Peasants | At slot limit |
| --- | --- | --- | --- | --- | --- | --- | --- |
| **Mine** (`eurcoa`) | 94 | 16 | 1.8 game min (1.3 real min) | 53 game s (38 real s) | 21 game s (15 real s) | 11 game s (8 real s) | 7 game s (5 real s) |
| **Mine** (`eurgol`) | 94 | 16 | 1.8 game min (1.3 real min) | 53 game s (38 real s) | 21 game s (15 real s) | 11 game s (8 real s) | 7 game s (5 real s) |
| **Mine** (`euriro`) | 94 | 16 | 1.8 game min (1.3 real min) | 53 game s (38 real s) | 21 game s (15 real s) | 11 game s (8 real s) | 7 game s (5 real s) |
| **Market** (`eurmar`) | 234 | 25 | 4.4 game min (3.2 real min) | 2.2 game min (1.6 real min) | 53 game s (38 real s) | 26 game s (19 real s) | 11 game s (8 real s) |
| **Mill** (`eurmil`) | 94 | 10 | 1.8 game min (1.3 real min) | 53 game s (38 real s) | 21 game s (15 real s) | 11 game s (8 real s) | 11 game s (8 real s) |
| **Shipyard** (`eurpor`) | 1562 | 30 | 29.4 game min (21.0 real min) | 14.7 game min (10.5 real min) | 5.9 game min (4.2 real min) | 2.9 game min (2.1 real min) | 59 game s (42 real s) |
| **Gate** (`eursga`) | 90 | 13 | 1.7 game min (1.2 real min) | 51 game s (36 real s) | 20 game s (15 real s) | 10 game s (7 real s) | 8 game s (6 real s) |
| **Storehouse** (`eursto`) | 31 | 9 | 35 game s (25 real s) | 18 game s (13 real s) | 7 game s (5 real s) | 4 game s (3 real s) | 4 game s (3 real s) |
| **Wall** (`eurswa`) | 90 | 4 | 1.7 game min (1.2 real min) | 51 game s (36 real s) | 25 game s (18 real s) | 25 game s (18 real s) | 25 game s (18 real s) |
| **Tower** (`eurtow`) | 1230 | 10 | 23.2 game min (16.6 real min) | 11.6 game min (8.3 real min) | 4.6 game min (3.3 real min) | 2.3 game min (1.7 real min) | 2.3 game min (1.7 real min) |
| **Academy** (`netaca`) | 625 | 18 | 11.8 game min (8.4 real min) | 5.9 game min (4.2 real min) | 2.4 game min (1.7 real min) | 1.2 game min (0.8 real min) | 39 game s (28 real s) |
| **Artillery Depot** (`netart`) | 246 | 20 | 4.6 game min (3.3 real min) | 2.3 game min (1.7 real min) | 56 game s (40 real s) | 28 game s (20 real s) | 14 game s (10 real s) |
| **Barracks, 18th century** (`netba2`) | 5625 | 21 | 105.9 game min (75.7 real min) | 53.0 game min (37.8 real min) | 21.2 game min (15.1 real min) | 10.6 game min (7.6 real min) | 5.0 game min (3.6 real min) |
| **Barracks, 17th century** (`netbar`) | 94 | 20 | 1.8 game min (1.3 real min) | 53 game s (38 real s) | 21 game s (15 real s) | 11 game s (8 real s) | 5 game s (4 real s) |
| **Blacksmith** (`netbla`) | 94 | 14 | 1.8 game min (1.3 real min) | 53 game s (38 real s) | 21 game s (15 real s) | 11 game s (8 real s) | 8 game s (5 real s) |
| **Town Hall** (`netcen`) | 156 | 19 | 2.9 game min (2.1 real min) | 1.5 game min (1.1 real min) | 35 game s (25 real s) | 18 game s (13 real s) | 9 game s (7 real s) |
| **Diplomatic Center** (`netdip`) | 312 | 18 | 5.9 game min (4.2 real min) | 2.9 game min (2.1 real min) | 1.2 game min (0.8 real min) | 35 game s (25 real s) | 20 game s (14 real s) |
| **Housing** (`nethou`) | 31 | 13 | 35 game s (25 real s) | 18 game s (13 real s) | 7 game s (5 real s) | 4 game s (3 real s) | 3 game s (2 real s) |
| **Stable** (`netsta`) | 625 | 18 | 11.8 game min (8.4 real min) | 5.9 game min (4.2 real min) | 2.4 game min (1.7 real min) | 1.2 game min (0.8 real min) | 39 game s (28 real s) |
| **Cathedral** (`nettem`) | 156 | 21 | 2.9 game min (2.1 real min) | 1.5 game min (1.1 real min) | 35 game s (25 real s) | 18 game s (13 real s) | 8 game s (6 real s) |
| **Gate** (`ukrwga`) | 6 | 13 | 6 game s (5 real s) | 3 game s (2 real s) | 1 game s (1 real s) | 1 game s (0 real s) | 0 game s (0 real s) |
| **Palisade** (`ukrwwa`) | 6 | 4 | 6 game s (5 real s) | 3 game s (2 real s) | 2 game s (1 real s) | 2 game s (1 real s) | 2 game s (1 real s) |

<a id="полный-ремонт-0--max-hp-6"></a>
<a id="полный-ремонт-7"></a>
### Full repair (0 → max HP)

| Building | Maximum health | Builder limit | 1 Peasant | 2 Peasants | 5 Peasants | 10 Peasants | At slot limit |
| --- | --- | --- | --- | --- | --- | --- | --- |
| **Mine** (`eurcoa`) | 2500 | 16 | 51 game s (36 real s) | 25 game s (18 real s) | 10 game s (7 real s) | 5 game s (4 real s) | 3 game s (2 real s) |
| **Mine** (`eurgol`) | 2500 | 16 | 51 game s (36 real s) | 25 game s (18 real s) | 10 game s (7 real s) | 5 game s (4 real s) | 3 game s (2 real s) |
| **Mine** (`euriro`) | 2500 | 16 | 51 game s (36 real s) | 25 game s (18 real s) | 10 game s (7 real s) | 5 game s (4 real s) | 3 game s (2 real s) |
| **Market** (`eurmar`) | 4000 | 25 | 1.4 game min (1.0 real min) | 41 game s (29 real s) | 16 game s (12 real s) | 8 game s (6 real s) | 3 game s (2 real s) |
| **Mill** (`eurmil`) | 20000 | 10 | 6.8 game min (4.8 real min) | 3.4 game min (2.4 real min) | 1.4 game min (1.0 real min) | 41 game s (29 real s) | 41 game s (29 real s) |
| **Shipyard** (`eurpor`) | 50000 | 30 | 16.9 game min (12.1 real min) | 8.5 game min (6.0 real min) | 3.4 game min (2.4 real min) | 1.7 game min (1.2 real min) | 34 game s (24 real s) |
| **Gate** (`eursga`) | 32000 | 13 | 10.8 game min (7.7 real min) | 5.4 game min (3.9 real min) | 2.2 game min (1.5 real min) | 1.1 game min (0.8 real min) | 50 game s (36 real s) |
| **Storehouse** (`eursto`) | 10000 | 9 | 3.4 game min (2.4 real min) | 1.7 game min (1.2 real min) | 41 game s (29 real s) | 23 game s (16 real s) | 23 game s (16 real s) |
| **Wall** (`eurswa`) | 50000 | 4 | 16.9 game min (12.1 real min) | 8.5 game min (6.0 real min) | 4.2 game min (3.0 real min) | 4.2 game min (3.0 real min) | 4.2 game min (3.0 real min) |
| **Tower** (`eurtow`) | 20000 | 10 | 6.8 game min (4.8 real min) | 3.4 game min (2.4 real min) | 1.4 game min (1.0 real min) | 41 game s (29 real s) | 41 game s (29 real s) |
| **Academy** (`netaca`) | 63000 | 18 | 21.3 game min (15.2 real min) | 10.7 game min (7.6 real min) | 4.3 game min (3.0 real min) | 2.1 game min (1.5 real min) | 1.2 game min (0.8 real min) |
| **Artillery Depot** (`netart`) | 40000 | 20 | 13.5 game min (9.7 real min) | 6.8 game min (4.8 real min) | 2.7 game min (1.9 real min) | 1.4 game min (1.0 real min) | 41 game s (29 real s) |
| **Barracks, 18th century** (`netba2`) | 55000 | 21 | 18.6 game min (13.3 real min) | 9.3 game min (6.6 real min) | 3.7 game min (2.7 real min) | 1.9 game min (1.3 real min) | 53 game s (38 real s) |
| **Barracks, 17th century** (`netbar`) | 40000 | 20 | 13.5 game min (9.7 real min) | 6.8 game min (4.8 real min) | 2.7 game min (1.9 real min) | 1.4 game min (1.0 real min) | 41 game s (29 real s) |
| **Blacksmith** (`netbla`) | 5500 | 14 | 1.9 game min (1.3 real min) | 56 game s (40 real s) | 22 game s (16 real s) | 11 game s (8 real s) | 8 game s (6 real s) |
| **Town Hall** (`netcen`) | 4950 | 19 | 1.7 game min (1.2 real min) | 50 game s (36 real s) | 20 game s (14 real s) | 10 game s (7 real s) | 5 game s (4 real s) |
| **Diplomatic Center** (`netdip`) | 4500 | 18 | 1.5 game min (1.1 real min) | 46 game s (33 real s) | 18 game s (13 real s) | 9 game s (7 real s) | 5 game s (4 real s) |
| **Housing** (`nethou`) | 4500 | 13 | 1.5 game min (1.1 real min) | 46 game s (33 real s) | 18 game s (13 real s) | 9 game s (7 real s) | 7 game s (5 real s) |
| **Stable** (`netsta`) | 20000 | 18 | 6.8 game min (4.8 real min) | 3.4 game min (2.4 real min) | 1.4 game min (1.0 real min) | 41 game s (29 real s) | 23 game s (16 real s) |
| **Cathedral** (`nettem`) | 4200 | 21 | 1.4 game min (1.0 real min) | 43 game s (30 real s) | 17 game s (12 real s) | 9 game s (6 real s) | 4 game s (3 real s) |
| **Gate** (`ukrwga`) | 1500 | 13 | 30 game s (22 real s) | 15 game s (11 real s) | 6 game s (4 real s) | 3 game s (2 real s) | 2 game s (2 real s) |
| **Palisade** (`ukrwwa`) | 1500 | 4 | 30 game s (22 real s) | 15 game s (11 real s) | 8 game s (5 real s) | 8 game s (5 real s) | 8 game s (5 real s) |

<a id="pie--piedmont-пьемонт"></a>
<a id="пьемонт-pie"></a>
## Piedmont (`pie`)
<a id="постройка-с-нуля-8"></a>
### Building from scratch

| Building | Base build time, game s | Builder limit | 1 Peasant | 2 Peasants | 5 Peasants | 10 Peasants | At slot limit |
| --- | --- | --- | --- | --- | --- | --- | --- |
| **Mine** (`eurcoa`) | 94 | 16 | 1.8 game min (1.3 real min) | 53 game s (38 real s) | 21 game s (15 real s) | 11 game s (8 real s) | 7 game s (5 real s) |
| **Mine** (`eurgol`) | 94 | 16 | 1.8 game min (1.3 real min) | 53 game s (38 real s) | 21 game s (15 real s) | 11 game s (8 real s) | 7 game s (5 real s) |
| **Mine** (`euriro`) | 94 | 16 | 1.8 game min (1.3 real min) | 53 game s (38 real s) | 21 game s (15 real s) | 11 game s (8 real s) | 7 game s (5 real s) |
| **Market** (`eurmar`) | 234 | 25 | 4.4 game min (3.2 real min) | 2.2 game min (1.6 real min) | 53 game s (38 real s) | 26 game s (19 real s) | 11 game s (8 real s) |
| **Mill** (`eurmil`) | 94 | 10 | 1.8 game min (1.3 real min) | 53 game s (38 real s) | 21 game s (15 real s) | 11 game s (8 real s) | 11 game s (8 real s) |
| **Shipyard** (`eurpor`) | 1562 | 30 | 29.4 game min (21.0 real min) | 14.7 game min (10.5 real min) | 5.9 game min (4.2 real min) | 2.9 game min (2.1 real min) | 59 game s (42 real s) |
| **Gate** (`eursga`) | 90 | 13 | 1.7 game min (1.2 real min) | 51 game s (36 real s) | 20 game s (15 real s) | 10 game s (7 real s) | 8 game s (6 real s) |
| **Storehouse** (`eursto`) | 31 | 9 | 35 game s (25 real s) | 18 game s (13 real s) | 7 game s (5 real s) | 4 game s (3 real s) | 4 game s (3 real s) |
| **Wall** (`eurswa`) | 90 | 4 | 1.7 game min (1.2 real min) | 51 game s (36 real s) | 25 game s (18 real s) | 25 game s (18 real s) | 25 game s (18 real s) |
| **Tower** (`eurtow`) | 1230 | 10 | 23.2 game min (16.6 real min) | 11.6 game min (8.3 real min) | 4.6 game min (3.3 real min) | 2.3 game min (1.7 real min) | 2.3 game min (1.7 real min) |
| **Academy** (`pieaca`) | 625 | 22 | 11.8 game min (8.4 real min) | 5.9 game min (4.2 real min) | 2.4 game min (1.7 real min) | 1.2 game min (0.8 real min) | 32 game s (23 real s) |
| **Artillery Depot** (`pieart`) | 246 | 19 | 4.6 game min (3.3 real min) | 2.3 game min (1.7 real min) | 56 game s (40 real s) | 28 game s (20 real s) | 15 game s (10 real s) |
| **Barracks, 18th century** (`pieba2`) | 5625 | 22 | 105.9 game min (75.7 real min) | 53.0 game min (37.8 real min) | 21.2 game min (15.1 real min) | 10.6 game min (7.6 real min) | 4.8 game min (3.4 real min) |
| **Barracks, 17th century** (`piebar`) | 94 | 24 | 1.8 game min (1.3 real min) | 53 game s (38 real s) | 21 game s (15 real s) | 11 game s (8 real s) | 4 game s (3 real s) |
| **Blacksmith** (`piebla`) | 94 | 16 | 1.8 game min (1.3 real min) | 53 game s (38 real s) | 21 game s (15 real s) | 11 game s (8 real s) | 7 game s (5 real s) |
| **Town Hall** (`piecen`) | 156 | 24 | 2.9 game min (2.1 real min) | 1.5 game min (1.1 real min) | 35 game s (25 real s) | 18 game s (13 real s) | 7 game s (5 real s) |
| **Diplomatic Center** (`piedip`) | 312 | 16 | 5.9 game min (4.2 real min) | 2.9 game min (2.1 real min) | 1.2 game min (0.8 real min) | 35 game s (25 real s) | 22 game s (16 real s) |
| **Housing** (`piehou`) | 31 | 13 | 35 game s (25 real s) | 18 game s (13 real s) | 7 game s (5 real s) | 4 game s (3 real s) | 3 game s (2 real s) |
| **Stable** (`piesta`) | 625 | 24 | 11.8 game min (8.4 real min) | 5.9 game min (4.2 real min) | 2.4 game min (1.7 real min) | 1.2 game min (0.8 real min) | 29 game s (21 real s) |
| **Cathedral** (`pietem`) | 156 | 20 | 2.9 game min (2.1 real min) | 1.5 game min (1.1 real min) | 35 game s (25 real s) | 18 game s (13 real s) | 9 game s (6 real s) |
| **Gate** (`ukrwga`) | 6 | 13 | 6 game s (5 real s) | 3 game s (2 real s) | 1 game s (1 real s) | 1 game s (0 real s) | 0 game s (0 real s) |
| **Palisade** (`ukrwwa`) | 6 | 4 | 6 game s (5 real s) | 3 game s (2 real s) | 2 game s (1 real s) | 2 game s (1 real s) | 2 game s (1 real s) |

<a id="полный-ремонт-0--max-hp-7"></a>
<a id="полный-ремонт-8"></a>
### Full repair (0 → max HP)

| Building | Maximum health | Builder limit | 1 Peasant | 2 Peasants | 5 Peasants | 10 Peasants | At slot limit |
| --- | --- | --- | --- | --- | --- | --- | --- |
| **Mine** (`eurcoa`) | 2500 | 16 | 51 game s (36 real s) | 25 game s (18 real s) | 10 game s (7 real s) | 5 game s (4 real s) | 3 game s (2 real s) |
| **Mine** (`eurgol`) | 2500 | 16 | 51 game s (36 real s) | 25 game s (18 real s) | 10 game s (7 real s) | 5 game s (4 real s) | 3 game s (2 real s) |
| **Mine** (`euriro`) | 2500 | 16 | 51 game s (36 real s) | 25 game s (18 real s) | 10 game s (7 real s) | 5 game s (4 real s) | 3 game s (2 real s) |
| **Market** (`eurmar`) | 4000 | 25 | 1.4 game min (1.0 real min) | 41 game s (29 real s) | 16 game s (12 real s) | 8 game s (6 real s) | 3 game s (2 real s) |
| **Mill** (`eurmil`) | 20000 | 10 | 6.8 game min (4.8 real min) | 3.4 game min (2.4 real min) | 1.4 game min (1.0 real min) | 41 game s (29 real s) | 41 game s (29 real s) |
| **Shipyard** (`eurpor`) | 50000 | 30 | 16.9 game min (12.1 real min) | 8.5 game min (6.0 real min) | 3.4 game min (2.4 real min) | 1.7 game min (1.2 real min) | 34 game s (24 real s) |
| **Gate** (`eursga`) | 32000 | 13 | 10.8 game min (7.7 real min) | 5.4 game min (3.9 real min) | 2.2 game min (1.5 real min) | 1.1 game min (0.8 real min) | 50 game s (36 real s) |
| **Storehouse** (`eursto`) | 10000 | 9 | 3.4 game min (2.4 real min) | 1.7 game min (1.2 real min) | 41 game s (29 real s) | 23 game s (16 real s) | 23 game s (16 real s) |
| **Wall** (`eurswa`) | 50000 | 4 | 16.9 game min (12.1 real min) | 8.5 game min (6.0 real min) | 4.2 game min (3.0 real min) | 4.2 game min (3.0 real min) | 4.2 game min (3.0 real min) |
| **Tower** (`eurtow`) | 20000 | 10 | 6.8 game min (4.8 real min) | 3.4 game min (2.4 real min) | 1.4 game min (1.0 real min) | 41 game s (29 real s) | 41 game s (29 real s) |
| **Academy** (`pieaca`) | 63000 | 22 | 21.3 game min (15.2 real min) | 10.7 game min (7.6 real min) | 4.3 game min (3.0 real min) | 2.1 game min (1.5 real min) | 58 game s (42 real s) |
| **Artillery Depot** (`pieart`) | 40000 | 19 | 13.5 game min (9.7 real min) | 6.8 game min (4.8 real min) | 2.7 game min (1.9 real min) | 1.4 game min (1.0 real min) | 43 game s (31 real s) |
| **Barracks, 18th century** (`pieba2`) | 55000 | 22 | 18.6 game min (13.3 real min) | 9.3 game min (6.6 real min) | 3.7 game min (2.7 real min) | 1.9 game min (1.3 real min) | 51 game s (36 real s) |
| **Barracks, 17th century** (`piebar`) | 40000 | 24 | 13.5 game min (9.7 real min) | 6.8 game min (4.8 real min) | 2.7 game min (1.9 real min) | 1.4 game min (1.0 real min) | 34 game s (24 real s) |
| **Blacksmith** (`piebla`) | 5500 | 16 | 1.9 game min (1.3 real min) | 56 game s (40 real s) | 22 game s (16 real s) | 11 game s (8 real s) | 7 game s (5 real s) |
| **Town Hall** (`piecen`) | 4000 | 24 | 1.4 game min (1.0 real min) | 41 game s (29 real s) | 16 game s (12 real s) | 8 game s (6 real s) | 3 game s (2 real s) |
| **Diplomatic Center** (`piedip`) | 4500 | 16 | 1.5 game min (1.1 real min) | 46 game s (33 real s) | 18 game s (13 real s) | 9 game s (7 real s) | 6 game s (4 real s) |
| **Housing** (`piehou`) | 4000 | 13 | 1.4 game min (1.0 real min) | 41 game s (29 real s) | 16 game s (12 real s) | 8 game s (6 real s) | 6 game s (4 real s) |
| **Stable** (`piesta`) | 20000 | 24 | 6.8 game min (4.8 real min) | 3.4 game min (2.4 real min) | 1.4 game min (1.0 real min) | 41 game s (29 real s) | 17 game s (12 real s) |
| **Cathedral** (`pietem`) | 4200 | 20 | 1.4 game min (1.0 real min) | 43 game s (30 real s) | 17 game s (12 real s) | 9 game s (6 real s) | 4 game s (3 real s) |
| **Gate** (`ukrwga`) | 1500 | 13 | 30 game s (22 real s) | 15 game s (11 real s) | 6 game s (4 real s) | 3 game s (2 real s) | 2 game s (2 real s) |
| **Palisade** (`ukrwwa`) | 1500 | 4 | 30 game s (22 real s) | 15 game s (11 real s) | 8 game s (5 real s) | 8 game s (5 real s) | 8 game s (5 real s) |

<a id="pol--poland-польша"></a>
<a id="польша-pol"></a>
## Poland (`pol`)
<a id="постройка-с-нуля-9"></a>
### Building from scratch

| Building | Base build time, game s | Builder limit | 1 Peasant | 2 Peasants | 5 Peasants | 10 Peasants | At slot limit |
| --- | --- | --- | --- | --- | --- | --- | --- |
| **Mine** (`eurcoa`) | 94 | 16 | 1.8 game min (1.3 real min) | 53 game s (38 real s) | 21 game s (15 real s) | 11 game s (8 real s) | 7 game s (5 real s) |
| **Mine** (`eurgol`) | 94 | 16 | 1.8 game min (1.3 real min) | 53 game s (38 real s) | 21 game s (15 real s) | 11 game s (8 real s) | 7 game s (5 real s) |
| **Mine** (`euriro`) | 94 | 16 | 1.8 game min (1.3 real min) | 53 game s (38 real s) | 21 game s (15 real s) | 11 game s (8 real s) | 7 game s (5 real s) |
| **Market** (`eurmar`) | 234 | 25 | 4.4 game min (3.2 real min) | 2.2 game min (1.6 real min) | 53 game s (38 real s) | 26 game s (19 real s) | 11 game s (8 real s) |
| **Mill** (`eurmil`) | 94 | 10 | 1.8 game min (1.3 real min) | 53 game s (38 real s) | 21 game s (15 real s) | 11 game s (8 real s) | 11 game s (8 real s) |
| **Shipyard** (`eurpor`) | 1562 | 30 | 29.4 game min (21.0 real min) | 14.7 game min (10.5 real min) | 5.9 game min (4.2 real min) | 2.9 game min (2.1 real min) | 59 game s (42 real s) |
| **Gate** (`eursga`) | 90 | 13 | 1.7 game min (1.2 real min) | 51 game s (36 real s) | 20 game s (15 real s) | 10 game s (7 real s) | 8 game s (6 real s) |
| **Wall** (`eurswa`) | 90 | 4 | 1.7 game min (1.2 real min) | 51 game s (36 real s) | 25 game s (18 real s) | 25 game s (18 real s) | 25 game s (18 real s) |
| **Tower** (`eurtow`) | 1230 | 10 | 23.2 game min (16.6 real min) | 11.6 game min (8.3 real min) | 4.6 game min (3.3 real min) | 2.3 game min (1.7 real min) | 2.3 game min (1.7 real min) |
| **Academy** (`polaca`) | 625 | 18 | 11.8 game min (8.4 real min) | 5.9 game min (4.2 real min) | 2.4 game min (1.7 real min) | 1.2 game min (0.8 real min) | 39 game s (28 real s) |
| **Artillery Depot** (`polart`) | 246 | 19 | 4.6 game min (3.3 real min) | 2.3 game min (1.7 real min) | 56 game s (40 real s) | 28 game s (20 real s) | 15 game s (10 real s) |
| **Barracks, 18th century** (`polba2`) | 5625 | 25 | 105.9 game min (75.7 real min) | 53.0 game min (37.8 real min) | 21.2 game min (15.1 real min) | 10.6 game min (7.6 real min) | 4.2 game min (3.0 real min) |
| **Barracks, 17th century** (`polbar`) | 94 | 27 | 1.8 game min (1.3 real min) | 53 game s (38 real s) | 21 game s (15 real s) | 11 game s (8 real s) | 4 game s (3 real s) |
| **Blacksmith** (`polbla`) | 94 | 18 | 1.8 game min (1.3 real min) | 53 game s (38 real s) | 21 game s (15 real s) | 11 game s (8 real s) | 6 game s (4 real s) |
| **Town Hall** (`polcen`) | 156 | 18 | 2.9 game min (2.1 real min) | 1.5 game min (1.1 real min) | 35 game s (25 real s) | 18 game s (13 real s) | 10 game s (7 real s) |
| **Diplomatic Center** (`poldip`) | 312 | 16 | 5.9 game min (4.2 real min) | 2.9 game min (2.1 real min) | 1.2 game min (0.8 real min) | 35 game s (25 real s) | 22 game s (16 real s) |
| **Housing** (`polhou`) | 31 | 17 | 35 game s (25 real s) | 18 game s (13 real s) | 7 game s (5 real s) | 4 game s (3 real s) | 2 game s (1 real s) |
| **Stable** (`polsta`) | 625 | 26 | 11.8 game min (8.4 real min) | 5.9 game min (4.2 real min) | 2.4 game min (1.7 real min) | 1.2 game min (0.8 real min) | 27 game s (19 real s) |
| **Cathedral** (`poltem`) | 156 | 22 | 2.9 game min (2.1 real min) | 1.5 game min (1.1 real min) | 35 game s (25 real s) | 18 game s (13 real s) | 8 game s (6 real s) |
| **Storehouse** (`russto`) | 31 | 8 | 35 game s (25 real s) | 18 game s (13 real s) | 7 game s (5 real s) | 4 game s (3 real s) | 4 game s (3 real s) |
| **Gate** (`ukrwga`) | 6 | 13 | 6 game s (5 real s) | 3 game s (2 real s) | 1 game s (1 real s) | 1 game s (0 real s) | 0 game s (0 real s) |
| **Palisade** (`ukrwwa`) | 6 | 4 | 6 game s (5 real s) | 3 game s (2 real s) | 2 game s (1 real s) | 2 game s (1 real s) | 2 game s (1 real s) |

<a id="полный-ремонт-0--max-hp-8"></a>
<a id="полный-ремонт-9"></a>
### Full repair (0 → max HP)

| Building | Maximum health | Builder limit | 1 Peasant | 2 Peasants | 5 Peasants | 10 Peasants | At slot limit |
| --- | --- | --- | --- | --- | --- | --- | --- |
| **Mine** (`eurcoa`) | 2500 | 16 | 51 game s (36 real s) | 25 game s (18 real s) | 10 game s (7 real s) | 5 game s (4 real s) | 3 game s (2 real s) |
| **Mine** (`eurgol`) | 2500 | 16 | 51 game s (36 real s) | 25 game s (18 real s) | 10 game s (7 real s) | 5 game s (4 real s) | 3 game s (2 real s) |
| **Mine** (`euriro`) | 2500 | 16 | 51 game s (36 real s) | 25 game s (18 real s) | 10 game s (7 real s) | 5 game s (4 real s) | 3 game s (2 real s) |
| **Market** (`eurmar`) | 4000 | 25 | 1.4 game min (1.0 real min) | 41 game s (29 real s) | 16 game s (12 real s) | 8 game s (6 real s) | 3 game s (2 real s) |
| **Mill** (`eurmil`) | 20000 | 10 | 6.8 game min (4.8 real min) | 3.4 game min (2.4 real min) | 1.4 game min (1.0 real min) | 41 game s (29 real s) | 41 game s (29 real s) |
| **Shipyard** (`eurpor`) | 50000 | 30 | 16.9 game min (12.1 real min) | 8.5 game min (6.0 real min) | 3.4 game min (2.4 real min) | 1.7 game min (1.2 real min) | 34 game s (24 real s) |
| **Gate** (`eursga`) | 32000 | 13 | 10.8 game min (7.7 real min) | 5.4 game min (3.9 real min) | 2.2 game min (1.5 real min) | 1.1 game min (0.8 real min) | 50 game s (36 real s) |
| **Wall** (`eurswa`) | 50000 | 4 | 16.9 game min (12.1 real min) | 8.5 game min (6.0 real min) | 4.2 game min (3.0 real min) | 4.2 game min (3.0 real min) | 4.2 game min (3.0 real min) |
| **Tower** (`eurtow`) | 20000 | 10 | 6.8 game min (4.8 real min) | 3.4 game min (2.4 real min) | 1.4 game min (1.0 real min) | 41 game s (29 real s) | 41 game s (29 real s) |
| **Academy** (`polaca`) | 63000 | 18 | 21.3 game min (15.2 real min) | 10.7 game min (7.6 real min) | 4.3 game min (3.0 real min) | 2.1 game min (1.5 real min) | 1.2 game min (0.8 real min) |
| **Artillery Depot** (`polart`) | 40000 | 19 | 13.5 game min (9.7 real min) | 6.8 game min (4.8 real min) | 2.7 game min (1.9 real min) | 1.4 game min (1.0 real min) | 43 game s (31 real s) |
| **Barracks, 18th century** (`polba2`) | 55000 | 25 | 18.6 game min (13.3 real min) | 9.3 game min (6.6 real min) | 3.7 game min (2.7 real min) | 1.9 game min (1.3 real min) | 45 game s (32 real s) |
| **Barracks, 17th century** (`polbar`) | 40000 | 27 | 13.5 game min (9.7 real min) | 6.8 game min (4.8 real min) | 2.7 game min (1.9 real min) | 1.4 game min (1.0 real min) | 30 game s (21 real s) |
| **Blacksmith** (`polbla`) | 5500 | 18 | 1.9 game min (1.3 real min) | 56 game s (40 real s) | 22 game s (16 real s) | 11 game s (8 real s) | 6 game s (4 real s) |
| **Town Hall** (`polcen`) | 4300 | 18 | 1.5 game min (1.0 real min) | 44 game s (31 real s) | 17 game s (12 real s) | 9 game s (6 real s) | 5 game s (3 real s) |
| **Diplomatic Center** (`poldip`) | 4500 | 16 | 1.5 game min (1.1 real min) | 46 game s (33 real s) | 18 game s (13 real s) | 9 game s (7 real s) | 6 game s (4 real s) |
| **Housing** (`polhou`) | 4100 | 17 | 1.4 game min (1.0 real min) | 42 game s (30 real s) | 17 game s (12 real s) | 8 game s (6 real s) | 5 game s (3 real s) |
| **Stable** (`polsta`) | 20000 | 26 | 6.8 game min (4.8 real min) | 3.4 game min (2.4 real min) | 1.4 game min (1.0 real min) | 41 game s (29 real s) | 16 game s (11 real s) |
| **Cathedral** (`poltem`) | 4200 | 22 | 1.4 game min (1.0 real min) | 43 game s (30 real s) | 17 game s (12 real s) | 9 game s (6 real s) | 4 game s (3 real s) |
| **Storehouse** (`russto`) | 10000 | 8 | 3.4 game min (2.4 real min) | 1.7 game min (1.2 real min) | 41 game s (29 real s) | 25 game s (18 real s) | 25 game s (18 real s) |
| **Gate** (`ukrwga`) | 1500 | 13 | 30 game s (22 real s) | 15 game s (11 real s) | 6 game s (4 real s) | 3 game s (2 real s) | 2 game s (2 real s) |
| **Palisade** (`ukrwwa`) | 1500 | 4 | 30 game s (22 real s) | 15 game s (11 real s) | 8 game s (5 real s) | 8 game s (5 real s) | 8 game s (5 real s) |

<a id="por--portugal-португалия"></a>
<a id="португалия-por"></a>
## Portugal (`por`)
<a id="постройка-с-нуля-10"></a>
### Building from scratch

| Building | Base build time, game s | Builder limit | 1 Peasant | 2 Peasants | 5 Peasants | 10 Peasants | At slot limit |
| --- | --- | --- | --- | --- | --- | --- | --- |
| **Mine** (`eurcoa`) | 94 | 16 | 1.8 game min (1.3 real min) | 53 game s (38 real s) | 21 game s (15 real s) | 11 game s (8 real s) | 7 game s (5 real s) |
| **Mine** (`eurgol`) | 94 | 16 | 1.8 game min (1.3 real min) | 53 game s (38 real s) | 21 game s (15 real s) | 11 game s (8 real s) | 7 game s (5 real s) |
| **Mine** (`euriro`) | 94 | 16 | 1.8 game min (1.3 real min) | 53 game s (38 real s) | 21 game s (15 real s) | 11 game s (8 real s) | 7 game s (5 real s) |
| **Mill** (`eurmil`) | 94 | 10 | 1.8 game min (1.3 real min) | 53 game s (38 real s) | 21 game s (15 real s) | 11 game s (8 real s) | 11 game s (8 real s) |
| **Gate** (`eursga`) | 90 | 13 | 1.7 game min (1.2 real min) | 51 game s (36 real s) | 20 game s (15 real s) | 10 game s (7 real s) | 8 game s (6 real s) |
| **Wall** (`eurswa`) | 90 | 4 | 1.7 game min (1.2 real min) | 51 game s (36 real s) | 25 game s (18 real s) | 25 game s (18 real s) | 25 game s (18 real s) |
| **Tower** (`eurtow`) | 1230 | 10 | 23.2 game min (16.6 real min) | 11.6 game min (8.3 real min) | 4.6 game min (3.3 real min) | 2.3 game min (1.7 real min) | 2.3 game min (1.7 real min) |
| **Academy** (`poraca`) | 625 | 16 | 11.8 game min (8.4 real min) | 5.9 game min (4.2 real min) | 2.4 game min (1.7 real min) | 1.2 game min (0.8 real min) | 44 game s (32 real s) |
| **Artillery Depot** (`porart`) | 246 | 22 | 4.6 game min (3.3 real min) | 2.3 game min (1.7 real min) | 56 game s (40 real s) | 28 game s (20 real s) | 13 game s (9 real s) |
| **Barracks, 18th century** (`porba2`) | 5625 | 24 | 105.9 game min (75.7 real min) | 53.0 game min (37.8 real min) | 21.2 game min (15.1 real min) | 10.6 game min (7.6 real min) | 4.4 game min (3.2 real min) |
| **Barracks, 17th century** (`porbar`) | 94 | 22 | 1.8 game min (1.3 real min) | 53 game s (38 real s) | 21 game s (15 real s) | 11 game s (8 real s) | 5 game s (3 real s) |
| **Blacksmith** (`porbla`) | 94 | 15 | 1.8 game min (1.3 real min) | 53 game s (38 real s) | 21 game s (15 real s) | 11 game s (8 real s) | 7 game s (5 real s) |
| **Town Hall** (`porcen`) | 156 | 21 | 2.9 game min (2.1 real min) | 1.5 game min (1.1 real min) | 35 game s (25 real s) | 18 game s (13 real s) | 8 game s (6 real s) |
| **Diplomatic Center** (`pordip`) | 312 | 18 | 5.9 game min (4.2 real min) | 2.9 game min (2.1 real min) | 1.2 game min (0.8 real min) | 35 game s (25 real s) | 20 game s (14 real s) |
| **Housing** (`porhou`) | 31 | 13 | 35 game s (25 real s) | 18 game s (13 real s) | 7 game s (5 real s) | 4 game s (3 real s) | 3 game s (2 real s) |
| **Shipyard** (`porpor`) | 1562 | 21 | 29.4 game min (21.0 real min) | 14.7 game min (10.5 real min) | 5.9 game min (4.2 real min) | 2.9 game min (2.1 real min) | 1.4 game min (1.0 real min) |
| **Stable** (`porsta`) | 625 | 24 | 11.8 game min (8.4 real min) | 5.9 game min (4.2 real min) | 2.4 game min (1.7 real min) | 1.2 game min (0.8 real min) | 29 game s (21 real s) |
| **Cathedral** (`portem`) | 156 | 25 | 2.9 game min (2.1 real min) | 1.5 game min (1.1 real min) | 35 game s (25 real s) | 18 game s (13 real s) | 7 game s (5 real s) |
| **Market** (`spamar`) | 156 | 24 | 2.9 game min (2.1 real min) | 1.5 game min (1.1 real min) | 35 game s (25 real s) | 18 game s (13 real s) | 7 game s (5 real s) |
| **Storehouse** (`spasto`) | 31 | 7 | 35 game s (25 real s) | 18 game s (13 real s) | 7 game s (5 real s) | 5 game s (4 real s) | 5 game s (4 real s) |
| **Gate** (`ukrwga`) | 6 | 13 | 6 game s (5 real s) | 3 game s (2 real s) | 1 game s (1 real s) | 1 game s (0 real s) | 0 game s (0 real s) |
| **Palisade** (`ukrwwa`) | 6 | 4 | 6 game s (5 real s) | 3 game s (2 real s) | 2 game s (1 real s) | 2 game s (1 real s) | 2 game s (1 real s) |

<a id="полный-ремонт-0--max-hp-9"></a>
<a id="полный-ремонт-10"></a>
### Full repair (0 → max HP)

| Building | Maximum health | Builder limit | 1 Peasant | 2 Peasants | 5 Peasants | 10 Peasants | At slot limit |
| --- | --- | --- | --- | --- | --- | --- | --- |
| **Mine** (`eurcoa`) | 2500 | 16 | 51 game s (36 real s) | 25 game s (18 real s) | 10 game s (7 real s) | 5 game s (4 real s) | 3 game s (2 real s) |
| **Mine** (`eurgol`) | 2500 | 16 | 51 game s (36 real s) | 25 game s (18 real s) | 10 game s (7 real s) | 5 game s (4 real s) | 3 game s (2 real s) |
| **Mine** (`euriro`) | 2500 | 16 | 51 game s (36 real s) | 25 game s (18 real s) | 10 game s (7 real s) | 5 game s (4 real s) | 3 game s (2 real s) |
| **Mill** (`eurmil`) | 20000 | 10 | 6.8 game min (4.8 real min) | 3.4 game min (2.4 real min) | 1.4 game min (1.0 real min) | 41 game s (29 real s) | 41 game s (29 real s) |
| **Gate** (`eursga`) | 32000 | 13 | 10.8 game min (7.7 real min) | 5.4 game min (3.9 real min) | 2.2 game min (1.5 real min) | 1.1 game min (0.8 real min) | 50 game s (36 real s) |
| **Wall** (`eurswa`) | 50000 | 4 | 16.9 game min (12.1 real min) | 8.5 game min (6.0 real min) | 4.2 game min (3.0 real min) | 4.2 game min (3.0 real min) | 4.2 game min (3.0 real min) |
| **Tower** (`eurtow`) | 20000 | 10 | 6.8 game min (4.8 real min) | 3.4 game min (2.4 real min) | 1.4 game min (1.0 real min) | 41 game s (29 real s) | 41 game s (29 real s) |
| **Academy** (`poraca`) | 63000 | 16 | 21.3 game min (15.2 real min) | 10.7 game min (7.6 real min) | 4.3 game min (3.0 real min) | 2.1 game min (1.5 real min) | 1.3 game min (1.0 real min) |
| **Artillery Depot** (`porart`) | 40000 | 22 | 13.5 game min (9.7 real min) | 6.8 game min (4.8 real min) | 2.7 game min (1.9 real min) | 1.4 game min (1.0 real min) | 37 game s (26 real s) |
| **Barracks, 18th century** (`porba2`) | 55000 | 24 | 18.6 game min (13.3 real min) | 9.3 game min (6.6 real min) | 3.7 game min (2.7 real min) | 1.9 game min (1.3 real min) | 47 game s (33 real s) |
| **Barracks, 17th century** (`porbar`) | 40000 | 22 | 13.5 game min (9.7 real min) | 6.8 game min (4.8 real min) | 2.7 game min (1.9 real min) | 1.4 game min (1.0 real min) | 37 game s (26 real s) |
| **Blacksmith** (`porbla`) | 5500 | 15 | 1.9 game min (1.3 real min) | 56 game s (40 real s) | 22 game s (16 real s) | 11 game s (8 real s) | 7 game s (5 real s) |
| **Town Hall** (`porcen`) | 4000 | 21 | 1.4 game min (1.0 real min) | 41 game s (29 real s) | 16 game s (12 real s) | 8 game s (6 real s) | 4 game s (3 real s) |
| **Diplomatic Center** (`pordip`) | 4500 | 18 | 1.5 game min (1.1 real min) | 46 game s (33 real s) | 18 game s (13 real s) | 9 game s (7 real s) | 5 game s (4 real s) |
| **Housing** (`porhou`) | 4000 | 13 | 1.4 game min (1.0 real min) | 41 game s (29 real s) | 16 game s (12 real s) | 8 game s (6 real s) | 6 game s (4 real s) |
| **Shipyard** (`porpor`) | 50000 | 21 | 16.9 game min (12.1 real min) | 8.5 game min (6.0 real min) | 3.4 game min (2.4 real min) | 1.7 game min (1.2 real min) | 48 game s (35 real s) |
| **Stable** (`porsta`) | 20000 | 24 | 6.8 game min (4.8 real min) | 3.4 game min (2.4 real min) | 1.4 game min (1.0 real min) | 41 game s (29 real s) | 17 game s (12 real s) |
| **Cathedral** (`portem`) | 4200 | 25 | 1.4 game min (1.0 real min) | 43 game s (30 real s) | 17 game s (12 real s) | 9 game s (6 real s) | 3 game s (2 real s) |
| **Market** (`spamar`) | 4000 | 24 | 1.4 game min (1.0 real min) | 41 game s (29 real s) | 16 game s (12 real s) | 8 game s (6 real s) | 3 game s (2 real s) |
| **Storehouse** (`spasto`) | 10000 | 7 | 3.4 game min (2.4 real min) | 1.7 game min (1.2 real min) | 41 game s (29 real s) | 29 game s (21 real s) | 29 game s (21 real s) |
| **Gate** (`ukrwga`) | 1500 | 13 | 30 game s (22 real s) | 15 game s (11 real s) | 6 game s (4 real s) | 3 game s (2 real s) | 2 game s (2 real s) |
| **Palisade** (`ukrwwa`) | 1500 | 4 | 30 game s (22 real s) | 15 game s (11 real s) | 8 game s (5 real s) | 8 game s (5 real s) | 8 game s (5 real s) |

<a id="pru--prussia-пруссия"></a>
<a id="пруссия-pru"></a>
## Prussia (`pru`)
<a id="постройка-с-нуля-11"></a>
### Building from scratch

| Building | Base build time, game s | Builder limit | 1 Peasant | 2 Peasants | 5 Peasants | 10 Peasants | At slot limit |
| --- | --- | --- | --- | --- | --- | --- | --- |
| **Mine** (`eurcoa`) | 94 | 16 | 1.8 game min (1.3 real min) | 53 game s (38 real s) | 21 game s (15 real s) | 11 game s (8 real s) | 7 game s (5 real s) |
| **Mine** (`eurgol`) | 94 | 16 | 1.8 game min (1.3 real min) | 53 game s (38 real s) | 21 game s (15 real s) | 11 game s (8 real s) | 7 game s (5 real s) |
| **Mine** (`euriro`) | 94 | 16 | 1.8 game min (1.3 real min) | 53 game s (38 real s) | 21 game s (15 real s) | 11 game s (8 real s) | 7 game s (5 real s) |
| **Market** (`eurmar`) | 234 | 25 | 4.4 game min (3.2 real min) | 2.2 game min (1.6 real min) | 53 game s (38 real s) | 26 game s (19 real s) | 11 game s (8 real s) |
| **Mill** (`eurmil`) | 94 | 10 | 1.8 game min (1.3 real min) | 53 game s (38 real s) | 21 game s (15 real s) | 11 game s (8 real s) | 11 game s (8 real s) |
| **Shipyard** (`eurpor`) | 1562 | 30 | 29.4 game min (21.0 real min) | 14.7 game min (10.5 real min) | 5.9 game min (4.2 real min) | 2.9 game min (2.1 real min) | 59 game s (42 real s) |
| **Gate** (`eursga`) | 90 | 13 | 1.7 game min (1.2 real min) | 51 game s (36 real s) | 20 game s (15 real s) | 10 game s (7 real s) | 8 game s (6 real s) |
| **Storehouse** (`eursto`) | 31 | 9 | 35 game s (25 real s) | 18 game s (13 real s) | 7 game s (5 real s) | 4 game s (3 real s) | 4 game s (3 real s) |
| **Wall** (`eurswa`) | 90 | 4 | 1.7 game min (1.2 real min) | 51 game s (36 real s) | 25 game s (18 real s) | 25 game s (18 real s) | 25 game s (18 real s) |
| **Tower** (`eurtow`) | 1230 | 10 | 23.2 game min (16.6 real min) | 11.6 game min (8.3 real min) | 4.6 game min (3.3 real min) | 2.3 game min (1.7 real min) | 2.3 game min (1.7 real min) |
| **Academy** (`pruaca`) | 625 | 18 | 11.8 game min (8.4 real min) | 5.9 game min (4.2 real min) | 2.4 game min (1.7 real min) | 1.2 game min (0.8 real min) | 39 game s (28 real s) |
| **Artillery Depot** (`pruart`) | 246 | 22 | 4.6 game min (3.3 real min) | 2.3 game min (1.7 real min) | 56 game s (40 real s) | 28 game s (20 real s) | 13 game s (9 real s) |
| **Barracks, 18th century** (`pruba2`) | 5625 | 22 | 105.9 game min (75.7 real min) | 53.0 game min (37.8 real min) | 21.2 game min (15.1 real min) | 10.6 game min (7.6 real min) | 4.8 game min (3.4 real min) |
| **Barracks, 17th century** (`prubar`) | 94 | 18 | 1.8 game min (1.3 real min) | 53 game s (38 real s) | 21 game s (15 real s) | 11 game s (8 real s) | 6 game s (4 real s) |
| **Blacksmith** (`prubla`) | 94 | 14 | 1.8 game min (1.3 real min) | 53 game s (38 real s) | 21 game s (15 real s) | 11 game s (8 real s) | 8 game s (5 real s) |
| **Town Hall** (`prucen`) | 156 | 20 | 2.9 game min (2.1 real min) | 1.5 game min (1.1 real min) | 35 game s (25 real s) | 18 game s (13 real s) | 9 game s (6 real s) |
| **Diplomatic Center** (`prudip`) | 312 | 19 | 5.9 game min (4.2 real min) | 2.9 game min (2.1 real min) | 1.2 game min (0.8 real min) | 35 game s (25 real s) | 19 game s (13 real s) |
| **Housing** (`pruhou`) | 31 | 12 | 35 game s (25 real s) | 18 game s (13 real s) | 7 game s (5 real s) | 4 game s (3 real s) | 3 game s (2 real s) |
| **Stable** (`prusta`) | 625 | 19 | 11.8 game min (8.4 real min) | 5.9 game min (4.2 real min) | 2.4 game min (1.7 real min) | 1.2 game min (0.8 real min) | 37 game s (27 real s) |
| **Cathedral** (`prutem`) | 156 | 25 | 2.9 game min (2.1 real min) | 1.5 game min (1.1 real min) | 35 game s (25 real s) | 18 game s (13 real s) | 7 game s (5 real s) |
| **Gate** (`ukrwga`) | 6 | 13 | 6 game s (5 real s) | 3 game s (2 real s) | 1 game s (1 real s) | 1 game s (0 real s) | 0 game s (0 real s) |
| **Palisade** (`ukrwwa`) | 6 | 4 | 6 game s (5 real s) | 3 game s (2 real s) | 2 game s (1 real s) | 2 game s (1 real s) | 2 game s (1 real s) |

<a id="полный-ремонт-0--max-hp-10"></a>
<a id="полный-ремонт-11"></a>
### Full repair (0 → max HP)

| Building | Maximum health | Builder limit | 1 Peasant | 2 Peasants | 5 Peasants | 10 Peasants | At slot limit |
| --- | --- | --- | --- | --- | --- | --- | --- |
| **Mine** (`eurcoa`) | 2500 | 16 | 51 game s (36 real s) | 25 game s (18 real s) | 10 game s (7 real s) | 5 game s (4 real s) | 3 game s (2 real s) |
| **Mine** (`eurgol`) | 2500 | 16 | 51 game s (36 real s) | 25 game s (18 real s) | 10 game s (7 real s) | 5 game s (4 real s) | 3 game s (2 real s) |
| **Mine** (`euriro`) | 2500 | 16 | 51 game s (36 real s) | 25 game s (18 real s) | 10 game s (7 real s) | 5 game s (4 real s) | 3 game s (2 real s) |
| **Market** (`eurmar`) | 4000 | 25 | 1.4 game min (1.0 real min) | 41 game s (29 real s) | 16 game s (12 real s) | 8 game s (6 real s) | 3 game s (2 real s) |
| **Mill** (`eurmil`) | 20000 | 10 | 6.8 game min (4.8 real min) | 3.4 game min (2.4 real min) | 1.4 game min (1.0 real min) | 41 game s (29 real s) | 41 game s (29 real s) |
| **Shipyard** (`eurpor`) | 50000 | 30 | 16.9 game min (12.1 real min) | 8.5 game min (6.0 real min) | 3.4 game min (2.4 real min) | 1.7 game min (1.2 real min) | 34 game s (24 real s) |
| **Gate** (`eursga`) | 32000 | 13 | 10.8 game min (7.7 real min) | 5.4 game min (3.9 real min) | 2.2 game min (1.5 real min) | 1.1 game min (0.8 real min) | 50 game s (36 real s) |
| **Storehouse** (`eursto`) | 10000 | 9 | 3.4 game min (2.4 real min) | 1.7 game min (1.2 real min) | 41 game s (29 real s) | 23 game s (16 real s) | 23 game s (16 real s) |
| **Wall** (`eurswa`) | 50000 | 4 | 16.9 game min (12.1 real min) | 8.5 game min (6.0 real min) | 4.2 game min (3.0 real min) | 4.2 game min (3.0 real min) | 4.2 game min (3.0 real min) |
| **Tower** (`eurtow`) | 20000 | 10 | 6.8 game min (4.8 real min) | 3.4 game min (2.4 real min) | 1.4 game min (1.0 real min) | 41 game s (29 real s) | 41 game s (29 real s) |
| **Academy** (`pruaca`) | 63000 | 18 | 21.3 game min (15.2 real min) | 10.7 game min (7.6 real min) | 4.3 game min (3.0 real min) | 2.1 game min (1.5 real min) | 1.2 game min (0.8 real min) |
| **Artillery Depot** (`pruart`) | 40000 | 22 | 13.5 game min (9.7 real min) | 6.8 game min (4.8 real min) | 2.7 game min (1.9 real min) | 1.4 game min (1.0 real min) | 37 game s (26 real s) |
| **Barracks, 18th century** (`pruba2`) | 55000 | 22 | 18.6 game min (13.3 real min) | 9.3 game min (6.6 real min) | 3.7 game min (2.7 real min) | 1.9 game min (1.3 real min) | 51 game s (36 real s) |
| **Barracks, 17th century** (`prubar`) | 40000 | 18 | 13.5 game min (9.7 real min) | 6.8 game min (4.8 real min) | 2.7 game min (1.9 real min) | 1.4 game min (1.0 real min) | 45 game s (32 real s) |
| **Blacksmith** (`prubla`) | 5500 | 14 | 1.9 game min (1.3 real min) | 56 game s (40 real s) | 22 game s (16 real s) | 11 game s (8 real s) | 8 game s (6 real s) |
| **Town Hall** (`prucen`) | 4200 | 20 | 1.4 game min (1.0 real min) | 43 game s (30 real s) | 17 game s (12 real s) | 9 game s (6 real s) | 4 game s (3 real s) |
| **Diplomatic Center** (`prudip`) | 4500 | 19 | 1.5 game min (1.1 real min) | 46 game s (33 real s) | 18 game s (13 real s) | 9 game s (7 real s) | 5 game s (3 real s) |
| **Housing** (`pruhou`) | 4500 | 12 | 1.5 game min (1.1 real min) | 46 game s (33 real s) | 18 game s (13 real s) | 9 game s (7 real s) | 8 game s (5 real s) |
| **Stable** (`prusta`) | 20000 | 19 | 6.8 game min (4.8 real min) | 3.4 game min (2.4 real min) | 1.4 game min (1.0 real min) | 41 game s (29 real s) | 21 game s (15 real s) |
| **Cathedral** (`prutem`) | 4200 | 25 | 1.4 game min (1.0 real min) | 43 game s (30 real s) | 17 game s (12 real s) | 9 game s (6 real s) | 3 game s (2 real s) |
| **Gate** (`ukrwga`) | 1500 | 13 | 30 game s (22 real s) | 15 game s (11 real s) | 6 game s (4 real s) | 3 game s (2 real s) | 2 game s (2 real s) |
| **Palisade** (`ukrwwa`) | 1500 | 4 | 30 game s (22 real s) | 15 game s (11 real s) | 8 game s (5 real s) | 8 game s (5 real s) | 8 game s (5 real s) |

<a id="rus--russia-россия"></a>
<a id="россия-rus"></a>
## Russia (`rus`)
<a id="постройка-с-нуля-12"></a>
### Building from scratch

| Building | Base build time, game s | Builder limit | 1 Peasant | 2 Peasants | 5 Peasants | 10 Peasants | At slot limit |
| --- | --- | --- | --- | --- | --- | --- | --- |
| **Mine** (`eurcoa`) | 94 | 16 | 1.8 game min (1.3 real min) | 53 game s (38 real s) | 21 game s (15 real s) | 11 game s (8 real s) | 7 game s (5 real s) |
| **Mine** (`eurgol`) | 94 | 16 | 1.8 game min (1.3 real min) | 53 game s (38 real s) | 21 game s (15 real s) | 11 game s (8 real s) | 7 game s (5 real s) |
| **Mine** (`euriro`) | 94 | 16 | 1.8 game min (1.3 real min) | 53 game s (38 real s) | 21 game s (15 real s) | 11 game s (8 real s) | 7 game s (5 real s) |
| **Academy** (`rusaca`) | 844 | 25 | 15.9 game min (11.4 real min) | 7.9 game min (5.7 real min) | 3.2 game min (2.3 real min) | 1.6 game min (1.1 real min) | 38 game s (27 real s) |
| **Artillery Depot** (`rusart`) | 246 | 24 | 4.6 game min (3.3 real min) | 2.3 game min (1.7 real min) | 56 game s (40 real s) | 28 game s (20 real s) | 12 game s (8 real s) |
| **Barracks, 18th century** (`rusba2`) | 5625 | 30 | 105.9 game min (75.7 real min) | 53.0 game min (37.8 real min) | 21.2 game min (15.1 real min) | 10.6 game min (7.6 real min) | 3.5 game min (2.5 real min) |
| **Strelets Barracks** (`rusbar`) | 78 | 23 | 1.5 game min (1.1 real min) | 44 game s (32 real s) | 18 game s (13 real s) | 9 game s (6 real s) | 4 game s (3 real s) |
| **Blacksmith** (`rusbla`) | 94 | 15 | 1.8 game min (1.3 real min) | 53 game s (38 real s) | 21 game s (15 real s) | 11 game s (8 real s) | 7 game s (5 real s) |
| **Town Hall** (`ruscen`) | 156 | 24 | 2.9 game min (2.1 real min) | 1.5 game min (1.1 real min) | 35 game s (25 real s) | 18 game s (13 real s) | 7 game s (5 real s) |
| **Diplomatic Center** (`rusdip`) | 312 | 18 | 5.9 game min (4.2 real min) | 2.9 game min (2.1 real min) | 1.2 game min (0.8 real min) | 35 game s (25 real s) | 20 game s (14 real s) |
| **Izba** (`rushou`) | 31 | 17 | 35 game s (25 real s) | 18 game s (13 real s) | 7 game s (5 real s) | 4 game s (3 real s) | 2 game s (1 real s) |
| **Market** (`rusmar`) | 234 | 23 | 4.4 game min (3.2 real min) | 2.2 game min (1.6 real min) | 53 game s (38 real s) | 26 game s (19 real s) | 12 game s (8 real s) |
| **Mill** (`rusmil`) | 94 | 7 | 1.8 game min (1.3 real min) | 53 game s (38 real s) | 21 game s (15 real s) | 15 game s (11 real s) | 15 game s (11 real s) |
| **Shipyard** (`ruspor`) | 1562 | 27 | 29.4 game min (21.0 real min) | 14.7 game min (10.5 real min) | 5.9 game min (4.2 real min) | 2.9 game min (2.1 real min) | 1.1 game min (0.8 real min) |
| **Gate** (`russga`) | 200 | 13 | 3.8 game min (2.7 real min) | 1.9 game min (1.3 real min) | 45 game s (32 real s) | 23 game s (16 real s) | 17 game s (12 real s) |
| **Stable** (`russta`) | 375 | 22 | 7.1 game min (5.0 real min) | 3.5 game min (2.5 real min) | 1.4 game min (1.0 real min) | 42 game s (30 real s) | 19 game s (14 real s) |
| **Storehouse** (`russto`) | 31 | 8 | 35 game s (25 real s) | 18 game s (13 real s) | 7 game s (5 real s) | 4 game s (3 real s) | 4 game s (3 real s) |
| **Wall** (`russwa`) | 200 | 4 | 3.8 game min (2.7 real min) | 1.9 game min (1.3 real min) | 56 game s (40 real s) | 56 game s (40 real s) | 56 game s (40 real s) |
| **Orthodox Cathedral** (`rustem`) | 156 | 30 | 2.9 game min (2.1 real min) | 1.5 game min (1.1 real min) | 35 game s (25 real s) | 18 game s (13 real s) | 6 game s (4 real s) |
| **Tower** (`rustow`) | 1477 | 10 | 27.8 game min (19.9 real min) | 13.9 game min (9.9 real min) | 5.6 game min (4.0 real min) | 2.8 game min (2.0 real min) | 2.8 game min (2.0 real min) |
| **Gate** (`ukrwga`) | 6 | 13 | 6 game s (5 real s) | 3 game s (2 real s) | 1 game s (1 real s) | 1 game s (0 real s) | 0 game s (0 real s) |
| **Palisade** (`ukrwwa`) | 6 | 4 | 6 game s (5 real s) | 3 game s (2 real s) | 2 game s (1 real s) | 2 game s (1 real s) | 2 game s (1 real s) |

<a id="полный-ремонт-0--max-hp-11"></a>
<a id="полный-ремонт-12"></a>
### Full repair (0 → max HP)

| Building | Maximum health | Builder limit | 1 Peasant | 2 Peasants | 5 Peasants | 10 Peasants | At slot limit |
| --- | --- | --- | --- | --- | --- | --- | --- |
| **Mine** (`eurcoa`) | 2500 | 16 | 51 game s (36 real s) | 25 game s (18 real s) | 10 game s (7 real s) | 5 game s (4 real s) | 3 game s (2 real s) |
| **Mine** (`eurgol`) | 2500 | 16 | 51 game s (36 real s) | 25 game s (18 real s) | 10 game s (7 real s) | 5 game s (4 real s) | 3 game s (2 real s) |
| **Mine** (`euriro`) | 2500 | 16 | 51 game s (36 real s) | 25 game s (18 real s) | 10 game s (7 real s) | 5 game s (4 real s) | 3 game s (2 real s) |
| **Academy** (`rusaca`) | 65000 | 25 | 22.0 game min (15.7 real min) | 11.0 game min (7.9 real min) | 4.4 game min (3.1 real min) | 2.2 game min (1.6 real min) | 53 game s (38 real s) |
| **Artillery Depot** (`rusart`) | 40000 | 24 | 13.5 game min (9.7 real min) | 6.8 game min (4.8 real min) | 2.7 game min (1.9 real min) | 1.4 game min (1.0 real min) | 34 game s (24 real s) |
| **Barracks, 18th century** (`rusba2`) | 55000 | 30 | 18.6 game min (13.3 real min) | 9.3 game min (6.6 real min) | 3.7 game min (2.7 real min) | 1.9 game min (1.3 real min) | 37 game s (27 real s) |
| **Strelets Barracks** (`rusbar`) | 25000 | 23 | 8.5 game min (6.0 real min) | 4.2 game min (3.0 real min) | 1.7 game min (1.2 real min) | 51 game s (36 real s) | 22 game s (16 real s) |
| **Blacksmith** (`rusbla`) | 5500 | 15 | 1.9 game min (1.3 real min) | 56 game s (40 real s) | 22 game s (16 real s) | 11 game s (8 real s) | 7 game s (5 real s) |
| **Town Hall** (`ruscen`) | 4050 | 24 | 1.4 game min (1.0 real min) | 41 game s (29 real s) | 16 game s (12 real s) | 8 game s (6 real s) | 3 game s (2 real s) |
| **Diplomatic Center** (`rusdip`) | 6500 | 18 | 2.2 game min (1.6 real min) | 1.1 game min (0.8 real min) | 26 game s (19 real s) | 13 game s (9 real s) | 7 game s (5 real s) |
| **Izba** (`rushou`) | 5000 | 17 | 1.7 game min (1.2 real min) | 51 game s (36 real s) | 20 game s (15 real s) | 10 game s (7 real s) | 6 game s (4 real s) |
| **Market** (`rusmar`) | 4000 | 23 | 1.4 game min (1.0 real min) | 41 game s (29 real s) | 16 game s (12 real s) | 8 game s (6 real s) | 4 game s (3 real s) |
| **Mill** (`rusmil`) | 15000 | 7 | 5.1 game min (3.6 real min) | 2.5 game min (1.8 real min) | 1.0 game min (0.7 real min) | 44 game s (31 real s) | 44 game s (31 real s) |
| **Shipyard** (`ruspor`) | 45000 | 27 | 15.2 game min (10.9 real min) | 7.6 game min (5.4 real min) | 3.0 game min (2.2 real min) | 1.5 game min (1.1 real min) | 34 game s (24 real s) |
| **Gate** (`russga`) | 32000 | 13 | 10.8 game min (7.7 real min) | 5.4 game min (3.9 real min) | 2.2 game min (1.5 real min) | 1.1 game min (0.8 real min) | 50 game s (36 real s) |
| **Stable** (`russta`) | 25000 | 22 | 8.5 game min (6.0 real min) | 4.2 game min (3.0 real min) | 1.7 game min (1.2 real min) | 51 game s (36 real s) | 23 game s (16 real s) |
| **Storehouse** (`russto`) | 10000 | 8 | 3.4 game min (2.4 real min) | 1.7 game min (1.2 real min) | 41 game s (29 real s) | 25 game s (18 real s) | 25 game s (18 real s) |
| **Wall** (`russwa`) | 50000 | 4 | 16.9 game min (12.1 real min) | 8.5 game min (6.0 real min) | 4.2 game min (3.0 real min) | 4.2 game min (3.0 real min) | 4.2 game min (3.0 real min) |
| **Orthodox Cathedral** (`rustem`) | 4500 | 30 | 1.5 game min (1.1 real min) | 46 game s (33 real s) | 18 game s (13 real s) | 9 game s (7 real s) | 3 game s (2 real s) |
| **Tower** (`rustow`) | 21000 | 10 | 7.1 game min (5.1 real min) | 3.6 game min (2.5 real min) | 1.4 game min (1.0 real min) | 43 game s (30 real s) | 43 game s (30 real s) |
| **Gate** (`ukrwga`) | 1500 | 13 | 30 game s (22 real s) | 15 game s (11 real s) | 6 game s (4 real s) | 3 game s (2 real s) | 2 game s (2 real s) |
| **Palisade** (`ukrwwa`) | 1500 | 4 | 30 game s (22 real s) | 15 game s (11 real s) | 8 game s (5 real s) | 8 game s (5 real s) | 8 game s (5 real s) |

<a id="sax--saxony-саксония"></a>
<a id="саксония-sax"></a>
## Saxony (`sax`)
<a id="постройка-с-нуля-13"></a>
### Building from scratch

| Building | Base build time, game s | Builder limit | 1 Peasant | 2 Peasants | 5 Peasants | 10 Peasants | At slot limit |
| --- | --- | --- | --- | --- | --- | --- | --- |
| **Mine** (`eurcoa`) | 94 | 16 | 1.8 game min (1.3 real min) | 53 game s (38 real s) | 21 game s (15 real s) | 11 game s (8 real s) | 7 game s (5 real s) |
| **Mine** (`eurgol`) | 94 | 16 | 1.8 game min (1.3 real min) | 53 game s (38 real s) | 21 game s (15 real s) | 11 game s (8 real s) | 7 game s (5 real s) |
| **Mine** (`euriro`) | 94 | 16 | 1.8 game min (1.3 real min) | 53 game s (38 real s) | 21 game s (15 real s) | 11 game s (8 real s) | 7 game s (5 real s) |
| **Market** (`eurmar`) | 234 | 25 | 4.4 game min (3.2 real min) | 2.2 game min (1.6 real min) | 53 game s (38 real s) | 26 game s (19 real s) | 11 game s (8 real s) |
| **Mill** (`eurmil`) | 94 | 10 | 1.8 game min (1.3 real min) | 53 game s (38 real s) | 21 game s (15 real s) | 11 game s (8 real s) | 11 game s (8 real s) |
| **Shipyard** (`eurpor`) | 1562 | 30 | 29.4 game min (21.0 real min) | 14.7 game min (10.5 real min) | 5.9 game min (4.2 real min) | 2.9 game min (2.1 real min) | 59 game s (42 real s) |
| **Gate** (`eursga`) | 90 | 13 | 1.7 game min (1.2 real min) | 51 game s (36 real s) | 20 game s (15 real s) | 10 game s (7 real s) | 8 game s (6 real s) |
| **Storehouse** (`eursto`) | 31 | 9 | 35 game s (25 real s) | 18 game s (13 real s) | 7 game s (5 real s) | 4 game s (3 real s) | 4 game s (3 real s) |
| **Wall** (`eurswa`) | 90 | 4 | 1.7 game min (1.2 real min) | 51 game s (36 real s) | 25 game s (18 real s) | 25 game s (18 real s) | 25 game s (18 real s) |
| **Tower** (`eurtow`) | 1230 | 10 | 23.2 game min (16.6 real min) | 11.6 game min (8.3 real min) | 4.6 game min (3.3 real min) | 2.3 game min (1.7 real min) | 2.3 game min (1.7 real min) |
| **Academy** (`saxaca`) | 625 | 19 | 11.8 game min (8.4 real min) | 5.9 game min (4.2 real min) | 2.4 game min (1.7 real min) | 1.2 game min (0.8 real min) | 37 game s (27 real s) |
| **Artillery Depot** (`saxart`) | 246 | 19 | 4.6 game min (3.3 real min) | 2.3 game min (1.7 real min) | 56 game s (40 real s) | 28 game s (20 real s) | 15 game s (10 real s) |
| **Barracks, 18th century** (`saxba2`) | 5625 | 20 | 105.9 game min (75.7 real min) | 53.0 game min (37.8 real min) | 21.2 game min (15.1 real min) | 10.6 game min (7.6 real min) | 5.3 game min (3.8 real min) |
| **Barracks, 17th century** (`saxbar`) | 94 | 20 | 1.8 game min (1.3 real min) | 53 game s (38 real s) | 21 game s (15 real s) | 11 game s (8 real s) | 5 game s (4 real s) |
| **Blacksmith** (`saxbla`) | 94 | 14 | 1.8 game min (1.3 real min) | 53 game s (38 real s) | 21 game s (15 real s) | 11 game s (8 real s) | 8 game s (5 real s) |
| **Town Hall** (`saxcen`) | 156 | 21 | 2.9 game min (2.1 real min) | 1.5 game min (1.1 real min) | 35 game s (25 real s) | 18 game s (13 real s) | 8 game s (6 real s) |
| **Diplomatic Center** (`saxdip`) | 312 | 17 | 5.9 game min (4.2 real min) | 2.9 game min (2.1 real min) | 1.2 game min (0.8 real min) | 35 game s (25 real s) | 21 game s (15 real s) |
| **Housing** (`saxhou`) | 31 | 13 | 35 game s (25 real s) | 18 game s (13 real s) | 7 game s (5 real s) | 4 game s (3 real s) | 3 game s (2 real s) |
| **Stable** (`saxsta`) | 625 | 19 | 11.8 game min (8.4 real min) | 5.9 game min (4.2 real min) | 2.4 game min (1.7 real min) | 1.2 game min (0.8 real min) | 37 game s (27 real s) |
| **Cathedral** (`saxtem`) | 156 | 26 | 2.9 game min (2.1 real min) | 1.5 game min (1.1 real min) | 35 game s (25 real s) | 18 game s (13 real s) | 7 game s (5 real s) |
| **Gate** (`ukrwga`) | 6 | 13 | 6 game s (5 real s) | 3 game s (2 real s) | 1 game s (1 real s) | 1 game s (0 real s) | 0 game s (0 real s) |
| **Palisade** (`ukrwwa`) | 6 | 4 | 6 game s (5 real s) | 3 game s (2 real s) | 2 game s (1 real s) | 2 game s (1 real s) | 2 game s (1 real s) |

<a id="полный-ремонт-0--max-hp-12"></a>
<a id="полный-ремонт-13"></a>
### Full repair (0 → max HP)

| Building | Maximum health | Builder limit | 1 Peasant | 2 Peasants | 5 Peasants | 10 Peasants | At slot limit |
| --- | --- | --- | --- | --- | --- | --- | --- |
| **Mine** (`eurcoa`) | 2500 | 16 | 51 game s (36 real s) | 25 game s (18 real s) | 10 game s (7 real s) | 5 game s (4 real s) | 3 game s (2 real s) |
| **Mine** (`eurgol`) | 2500 | 16 | 51 game s (36 real s) | 25 game s (18 real s) | 10 game s (7 real s) | 5 game s (4 real s) | 3 game s (2 real s) |
| **Mine** (`euriro`) | 2500 | 16 | 51 game s (36 real s) | 25 game s (18 real s) | 10 game s (7 real s) | 5 game s (4 real s) | 3 game s (2 real s) |
| **Market** (`eurmar`) | 4000 | 25 | 1.4 game min (1.0 real min) | 41 game s (29 real s) | 16 game s (12 real s) | 8 game s (6 real s) | 3 game s (2 real s) |
| **Mill** (`eurmil`) | 20000 | 10 | 6.8 game min (4.8 real min) | 3.4 game min (2.4 real min) | 1.4 game min (1.0 real min) | 41 game s (29 real s) | 41 game s (29 real s) |
| **Shipyard** (`eurpor`) | 50000 | 30 | 16.9 game min (12.1 real min) | 8.5 game min (6.0 real min) | 3.4 game min (2.4 real min) | 1.7 game min (1.2 real min) | 34 game s (24 real s) |
| **Gate** (`eursga`) | 32000 | 13 | 10.8 game min (7.7 real min) | 5.4 game min (3.9 real min) | 2.2 game min (1.5 real min) | 1.1 game min (0.8 real min) | 50 game s (36 real s) |
| **Storehouse** (`eursto`) | 10000 | 9 | 3.4 game min (2.4 real min) | 1.7 game min (1.2 real min) | 41 game s (29 real s) | 23 game s (16 real s) | 23 game s (16 real s) |
| **Wall** (`eurswa`) | 50000 | 4 | 16.9 game min (12.1 real min) | 8.5 game min (6.0 real min) | 4.2 game min (3.0 real min) | 4.2 game min (3.0 real min) | 4.2 game min (3.0 real min) |
| **Tower** (`eurtow`) | 20000 | 10 | 6.8 game min (4.8 real min) | 3.4 game min (2.4 real min) | 1.4 game min (1.0 real min) | 41 game s (29 real s) | 41 game s (29 real s) |
| **Academy** (`saxaca`) | 63000 | 19 | 21.3 game min (15.2 real min) | 10.7 game min (7.6 real min) | 4.3 game min (3.0 real min) | 2.1 game min (1.5 real min) | 1.1 game min (0.8 real min) |
| **Artillery Depot** (`saxart`) | 40000 | 19 | 13.5 game min (9.7 real min) | 6.8 game min (4.8 real min) | 2.7 game min (1.9 real min) | 1.4 game min (1.0 real min) | 43 game s (31 real s) |
| **Barracks, 18th century** (`saxba2`) | 55000 | 20 | 18.6 game min (13.3 real min) | 9.3 game min (6.6 real min) | 3.7 game min (2.7 real min) | 1.9 game min (1.3 real min) | 56 game s (40 real s) |
| **Barracks, 17th century** (`saxbar`) | 40000 | 20 | 13.5 game min (9.7 real min) | 6.8 game min (4.8 real min) | 2.7 game min (1.9 real min) | 1.4 game min (1.0 real min) | 41 game s (29 real s) |
| **Blacksmith** (`saxbla`) | 5500 | 14 | 1.9 game min (1.3 real min) | 56 game s (40 real s) | 22 game s (16 real s) | 11 game s (8 real s) | 8 game s (6 real s) |
| **Town Hall** (`saxcen`) | 4000 | 21 | 1.4 game min (1.0 real min) | 41 game s (29 real s) | 16 game s (12 real s) | 8 game s (6 real s) | 4 game s (3 real s) |
| **Diplomatic Center** (`saxdip`) | 4500 | 17 | 1.5 game min (1.1 real min) | 46 game s (33 real s) | 18 game s (13 real s) | 9 game s (7 real s) | 5 game s (4 real s) |
| **Housing** (`saxhou`) | 4000 | 13 | 1.4 game min (1.0 real min) | 41 game s (29 real s) | 16 game s (12 real s) | 8 game s (6 real s) | 6 game s (4 real s) |
| **Stable** (`saxsta`) | 20000 | 19 | 6.8 game min (4.8 real min) | 3.4 game min (2.4 real min) | 1.4 game min (1.0 real min) | 41 game s (29 real s) | 21 game s (15 real s) |
| **Cathedral** (`saxtem`) | 4200 | 26 | 1.4 game min (1.0 real min) | 43 game s (30 real s) | 17 game s (12 real s) | 9 game s (6 real s) | 3 game s (2 real s) |
| **Gate** (`ukrwga`) | 1500 | 13 | 30 game s (22 real s) | 15 game s (11 real s) | 6 game s (4 real s) | 3 game s (2 real s) | 2 game s (2 real s) |
| **Palisade** (`ukrwwa`) | 1500 | 4 | 30 game s (22 real s) | 15 game s (11 real s) | 8 game s (5 real s) | 8 game s (5 real s) | 8 game s (5 real s) |

<a id="sco--scotland-шотландия"></a>
<a id="шотландия-sco"></a>
## Scotland (`sco`)
<a id="постройка-с-нуля-14"></a>
### Building from scratch

| Building | Base build time, game s | Builder limit | 1 Peasant | 2 Peasants | 5 Peasants | 10 Peasants | At slot limit |
| --- | --- | --- | --- | --- | --- | --- | --- |
| **Mine** (`eurcoa`) | 94 | 16 | 1.8 game min (1.3 real min) | 53 game s (38 real s) | 21 game s (15 real s) | 11 game s (8 real s) | 7 game s (5 real s) |
| **Mine** (`eurgol`) | 94 | 16 | 1.8 game min (1.3 real min) | 53 game s (38 real s) | 21 game s (15 real s) | 11 game s (8 real s) | 7 game s (5 real s) |
| **Mine** (`euriro`) | 94 | 16 | 1.8 game min (1.3 real min) | 53 game s (38 real s) | 21 game s (15 real s) | 11 game s (8 real s) | 7 game s (5 real s) |
| **Market** (`eurmar`) | 234 | 25 | 4.4 game min (3.2 real min) | 2.2 game min (1.6 real min) | 53 game s (38 real s) | 26 game s (19 real s) | 11 game s (8 real s) |
| **Mill** (`eurmil`) | 94 | 10 | 1.8 game min (1.3 real min) | 53 game s (38 real s) | 21 game s (15 real s) | 11 game s (8 real s) | 11 game s (8 real s) |
| **Shipyard** (`eurpor`) | 1562 | 30 | 29.4 game min (21.0 real min) | 14.7 game min (10.5 real min) | 5.9 game min (4.2 real min) | 2.9 game min (2.1 real min) | 59 game s (42 real s) |
| **Gate** (`eursga`) | 90 | 13 | 1.7 game min (1.2 real min) | 51 game s (36 real s) | 20 game s (15 real s) | 10 game s (7 real s) | 8 game s (6 real s) |
| **Storehouse** (`eursto`) | 31 | 9 | 35 game s (25 real s) | 18 game s (13 real s) | 7 game s (5 real s) | 4 game s (3 real s) | 4 game s (3 real s) |
| **Wall** (`eurswa`) | 90 | 4 | 1.7 game min (1.2 real min) | 51 game s (36 real s) | 25 game s (18 real s) | 25 game s (18 real s) | 25 game s (18 real s) |
| **Tower** (`eurtow`) | 1230 | 10 | 23.2 game min (16.6 real min) | 11.6 game min (8.3 real min) | 4.6 game min (3.3 real min) | 2.3 game min (1.7 real min) | 2.3 game min (1.7 real min) |
| **Academy** (`scoaca`) | 625 | 20 | 11.8 game min (8.4 real min) | 5.9 game min (4.2 real min) | 2.4 game min (1.7 real min) | 1.2 game min (0.8 real min) | 35 game s (25 real s) |
| **Artillery Depot** (`scoart`) | 246 | 21 | 4.6 game min (3.3 real min) | 2.3 game min (1.7 real min) | 56 game s (40 real s) | 28 game s (20 real s) | 13 game s (9 real s) |
| **Castle** (`scoba2`) | 625 | 30 | 11.8 game min (8.4 real min) | 5.9 game min (4.2 real min) | 2.4 game min (1.7 real min) | 1.2 game min (0.8 real min) | 24 game s (17 real s) |
| **Barracks, 17th century** (`scobar`) | 94 | 23 | 1.8 game min (1.3 real min) | 53 game s (38 real s) | 21 game s (15 real s) | 11 game s (8 real s) | 5 game s (3 real s) |
| **Blacksmith** (`scobla`) | 94 | 16 | 1.8 game min (1.3 real min) | 53 game s (38 real s) | 21 game s (15 real s) | 11 game s (8 real s) | 7 game s (5 real s) |
| **Town Hall** (`scocen`) | 156 | 28 | 2.9 game min (2.1 real min) | 1.5 game min (1.1 real min) | 35 game s (25 real s) | 18 game s (13 real s) | 6 game s (5 real s) |
| **Diplomatic Center** (`scodip`) | 312 | 19 | 5.9 game min (4.2 real min) | 2.9 game min (2.1 real min) | 1.2 game min (0.8 real min) | 35 game s (25 real s) | 19 game s (13 real s) |
| **Housing** (`scohou`) | 31 | 14 | 35 game s (25 real s) | 18 game s (13 real s) | 7 game s (5 real s) | 4 game s (3 real s) | 3 game s (2 real s) |
| **Stable** (`scosta`) | 375 | 20 | 7.1 game min (5.0 real min) | 3.5 game min (2.5 real min) | 1.4 game min (1.0 real min) | 42 game s (30 real s) | 21 game s (15 real s) |
| **Cathedral** (`scotem`) | 156 | 22 | 2.9 game min (2.1 real min) | 1.5 game min (1.1 real min) | 35 game s (25 real s) | 18 game s (13 real s) | 8 game s (6 real s) |
| **Gate** (`ukrwga`) | 6 | 13 | 6 game s (5 real s) | 3 game s (2 real s) | 1 game s (1 real s) | 1 game s (0 real s) | 0 game s (0 real s) |
| **Palisade** (`ukrwwa`) | 6 | 4 | 6 game s (5 real s) | 3 game s (2 real s) | 2 game s (1 real s) | 2 game s (1 real s) | 2 game s (1 real s) |

<a id="полный-ремонт-0--max-hp-13"></a>
<a id="полный-ремонт-14"></a>
### Full repair (0 → max HP)

| Building | Maximum health | Builder limit | 1 Peasant | 2 Peasants | 5 Peasants | 10 Peasants | At slot limit |
| --- | --- | --- | --- | --- | --- | --- | --- |
| **Mine** (`eurcoa`) | 2500 | 16 | 51 game s (36 real s) | 25 game s (18 real s) | 10 game s (7 real s) | 5 game s (4 real s) | 3 game s (2 real s) |
| **Mine** (`eurgol`) | 2500 | 16 | 51 game s (36 real s) | 25 game s (18 real s) | 10 game s (7 real s) | 5 game s (4 real s) | 3 game s (2 real s) |
| **Mine** (`euriro`) | 2500 | 16 | 51 game s (36 real s) | 25 game s (18 real s) | 10 game s (7 real s) | 5 game s (4 real s) | 3 game s (2 real s) |
| **Market** (`eurmar`) | 4000 | 25 | 1.4 game min (1.0 real min) | 41 game s (29 real s) | 16 game s (12 real s) | 8 game s (6 real s) | 3 game s (2 real s) |
| **Mill** (`eurmil`) | 20000 | 10 | 6.8 game min (4.8 real min) | 3.4 game min (2.4 real min) | 1.4 game min (1.0 real min) | 41 game s (29 real s) | 41 game s (29 real s) |
| **Shipyard** (`eurpor`) | 50000 | 30 | 16.9 game min (12.1 real min) | 8.5 game min (6.0 real min) | 3.4 game min (2.4 real min) | 1.7 game min (1.2 real min) | 34 game s (24 real s) |
| **Gate** (`eursga`) | 32000 | 13 | 10.8 game min (7.7 real min) | 5.4 game min (3.9 real min) | 2.2 game min (1.5 real min) | 1.1 game min (0.8 real min) | 50 game s (36 real s) |
| **Storehouse** (`eursto`) | 10000 | 9 | 3.4 game min (2.4 real min) | 1.7 game min (1.2 real min) | 41 game s (29 real s) | 23 game s (16 real s) | 23 game s (16 real s) |
| **Wall** (`eurswa`) | 50000 | 4 | 16.9 game min (12.1 real min) | 8.5 game min (6.0 real min) | 4.2 game min (3.0 real min) | 4.2 game min (3.0 real min) | 4.2 game min (3.0 real min) |
| **Tower** (`eurtow`) | 20000 | 10 | 6.8 game min (4.8 real min) | 3.4 game min (2.4 real min) | 1.4 game min (1.0 real min) | 41 game s (29 real s) | 41 game s (29 real s) |
| **Academy** (`scoaca`) | 63000 | 20 | 21.3 game min (15.2 real min) | 10.7 game min (7.6 real min) | 4.3 game min (3.0 real min) | 2.1 game min (1.5 real min) | 1.1 game min (0.8 real min) |
| **Artillery Depot** (`scoart`) | 40000 | 21 | 13.5 game min (9.7 real min) | 6.8 game min (4.8 real min) | 2.7 game min (1.9 real min) | 1.4 game min (1.0 real min) | 39 game s (28 real s) |
| **Castle** (`scoba2`) | 40000 | 30 | 13.5 game min (9.7 real min) | 6.8 game min (4.8 real min) | 2.7 game min (1.9 real min) | 1.4 game min (1.0 real min) | 27 game s (19 real s) |
| **Barracks, 17th century** (`scobar`) | 30000 | 23 | 10.2 game min (7.3 real min) | 5.1 game min (3.6 real min) | 2.0 game min (1.5 real min) | 1.0 game min (0.7 real min) | 26 game s (19 real s) |
| **Blacksmith** (`scobla`) | 5500 | 16 | 1.9 game min (1.3 real min) | 56 game s (40 real s) | 22 game s (16 real s) | 11 game s (8 real s) | 7 game s (5 real s) |
| **Town Hall** (`scocen`) | 4000 | 28 | 1.4 game min (1.0 real min) | 41 game s (29 real s) | 16 game s (12 real s) | 8 game s (6 real s) | 3 game s (2 real s) |
| **Diplomatic Center** (`scodip`) | 4500 | 19 | 1.5 game min (1.1 real min) | 46 game s (33 real s) | 18 game s (13 real s) | 9 game s (7 real s) | 5 game s (3 real s) |
| **Housing** (`scohou`) | 4000 | 14 | 1.4 game min (1.0 real min) | 41 game s (29 real s) | 16 game s (12 real s) | 8 game s (6 real s) | 6 game s (4 real s) |
| **Stable** (`scosta`) | 25000 | 20 | 8.5 game min (6.0 real min) | 4.2 game min (3.0 real min) | 1.7 game min (1.2 real min) | 51 game s (36 real s) | 25 game s (18 real s) |
| **Cathedral** (`scotem`) | 4200 | 22 | 1.4 game min (1.0 real min) | 43 game s (30 real s) | 17 game s (12 real s) | 9 game s (6 real s) | 4 game s (3 real s) |
| **Gate** (`ukrwga`) | 1500 | 13 | 30 game s (22 real s) | 15 game s (11 real s) | 6 game s (4 real s) | 3 game s (2 real s) | 2 game s (2 real s) |
| **Palisade** (`ukrwwa`) | 1500 | 4 | 30 game s (22 real s) | 15 game s (11 real s) | 8 game s (5 real s) | 8 game s (5 real s) | 8 game s (5 real s) |

<a id="spa--spain-испания"></a>
<a id="испания-spa"></a>
## Spain (`spa`)
<a id="постройка-с-нуля-15"></a>
### Building from scratch

| Building | Base build time, game s | Builder limit | 1 Peasant | 2 Peasants | 5 Peasants | 10 Peasants | At slot limit |
| --- | --- | --- | --- | --- | --- | --- | --- |
| **Mine** (`eurcoa`) | 94 | 16 | 1.8 game min (1.3 real min) | 53 game s (38 real s) | 21 game s (15 real s) | 11 game s (8 real s) | 7 game s (5 real s) |
| **Mine** (`eurgol`) | 94 | 16 | 1.8 game min (1.3 real min) | 53 game s (38 real s) | 21 game s (15 real s) | 11 game s (8 real s) | 7 game s (5 real s) |
| **Mine** (`euriro`) | 94 | 16 | 1.8 game min (1.3 real min) | 53 game s (38 real s) | 21 game s (15 real s) | 11 game s (8 real s) | 7 game s (5 real s) |
| **Mill** (`eurmil`) | 94 | 10 | 1.8 game min (1.3 real min) | 53 game s (38 real s) | 21 game s (15 real s) | 11 game s (8 real s) | 11 game s (8 real s) |
| **Shipyard** (`eurpor`) | 1562 | 30 | 29.4 game min (21.0 real min) | 14.7 game min (10.5 real min) | 5.9 game min (4.2 real min) | 2.9 game min (2.1 real min) | 59 game s (42 real s) |
| **Gate** (`eursga`) | 90 | 13 | 1.7 game min (1.2 real min) | 51 game s (36 real s) | 20 game s (15 real s) | 10 game s (7 real s) | 8 game s (6 real s) |
| **Wall** (`eurswa`) | 90 | 4 | 1.7 game min (1.2 real min) | 51 game s (36 real s) | 25 game s (18 real s) | 25 game s (18 real s) | 25 game s (18 real s) |
| **Tower** (`eurtow`) | 1230 | 10 | 23.2 game min (16.6 real min) | 11.6 game min (8.3 real min) | 4.6 game min (3.3 real min) | 2.3 game min (1.7 real min) | 2.3 game min (1.7 real min) |
| **Academy** (`spaaca`) | 625 | 26 | 11.8 game min (8.4 real min) | 5.9 game min (4.2 real min) | 2.4 game min (1.7 real min) | 1.2 game min (0.8 real min) | 27 game s (19 real s) |
| **Artillery Depot** (`spaart`) | 246 | 23 | 4.6 game min (3.3 real min) | 2.3 game min (1.7 real min) | 56 game s (40 real s) | 28 game s (20 real s) | 12 game s (9 real s) |
| **Barracks, 18th century** (`spaba2`) | 5625 | 26 | 105.9 game min (75.7 real min) | 53.0 game min (37.8 real min) | 21.2 game min (15.1 real min) | 10.6 game min (7.6 real min) | 4.1 game min (2.9 real min) |
| **Barracks, 17th century** (`spabar`) | 94 | 18 | 1.8 game min (1.3 real min) | 53 game s (38 real s) | 21 game s (15 real s) | 11 game s (8 real s) | 6 game s (4 real s) |
| **Blacksmith** (`spabla`) | 94 | 13 | 1.8 game min (1.3 real min) | 53 game s (38 real s) | 21 game s (15 real s) | 11 game s (8 real s) | 8 game s (6 real s) |
| **Town Hall** (`spacen`) | 156 | 24 | 2.9 game min (2.1 real min) | 1.5 game min (1.1 real min) | 35 game s (25 real s) | 18 game s (13 real s) | 7 game s (5 real s) |
| **Diplomatic Center** (`spadip`) | 312 | 21 | 5.9 game min (4.2 real min) | 2.9 game min (2.1 real min) | 1.2 game min (0.8 real min) | 35 game s (25 real s) | 17 game s (12 real s) |
| **Housing** (`spahou`) | 31 | 14 | 35 game s (25 real s) | 18 game s (13 real s) | 7 game s (5 real s) | 4 game s (3 real s) | 3 game s (2 real s) |
| **Market** (`spamar`) | 156 | 24 | 2.9 game min (2.1 real min) | 1.5 game min (1.1 real min) | 35 game s (25 real s) | 18 game s (13 real s) | 7 game s (5 real s) |
| **Stable** (`spasta`) | 625 | 21 | 11.8 game min (8.4 real min) | 5.9 game min (4.2 real min) | 2.4 game min (1.7 real min) | 1.2 game min (0.8 real min) | 34 game s (24 real s) |
| **Storehouse** (`spasto`) | 31 | 7 | 35 game s (25 real s) | 18 game s (13 real s) | 7 game s (5 real s) | 5 game s (4 real s) | 5 game s (4 real s) |
| **Cathedral** (`spatem`) | 156 | 30 | 2.9 game min (2.1 real min) | 1.5 game min (1.1 real min) | 35 game s (25 real s) | 18 game s (13 real s) | 6 game s (4 real s) |
| **Gate** (`ukrwga`) | 6 | 13 | 6 game s (5 real s) | 3 game s (2 real s) | 1 game s (1 real s) | 1 game s (0 real s) | 0 game s (0 real s) |
| **Palisade** (`ukrwwa`) | 6 | 4 | 6 game s (5 real s) | 3 game s (2 real s) | 2 game s (1 real s) | 2 game s (1 real s) | 2 game s (1 real s) |

<a id="полный-ремонт-0--max-hp-14"></a>
<a id="полный-ремонт-15"></a>
### Full repair (0 → max HP)

| Building | Maximum health | Builder limit | 1 Peasant | 2 Peasants | 5 Peasants | 10 Peasants | At slot limit |
| --- | --- | --- | --- | --- | --- | --- | --- |
| **Mine** (`eurcoa`) | 2500 | 16 | 51 game s (36 real s) | 25 game s (18 real s) | 10 game s (7 real s) | 5 game s (4 real s) | 3 game s (2 real s) |
| **Mine** (`eurgol`) | 2500 | 16 | 51 game s (36 real s) | 25 game s (18 real s) | 10 game s (7 real s) | 5 game s (4 real s) | 3 game s (2 real s) |
| **Mine** (`euriro`) | 2500 | 16 | 51 game s (36 real s) | 25 game s (18 real s) | 10 game s (7 real s) | 5 game s (4 real s) | 3 game s (2 real s) |
| **Mill** (`eurmil`) | 20000 | 10 | 6.8 game min (4.8 real min) | 3.4 game min (2.4 real min) | 1.4 game min (1.0 real min) | 41 game s (29 real s) | 41 game s (29 real s) |
| **Shipyard** (`eurpor`) | 50000 | 30 | 16.9 game min (12.1 real min) | 8.5 game min (6.0 real min) | 3.4 game min (2.4 real min) | 1.7 game min (1.2 real min) | 34 game s (24 real s) |
| **Gate** (`eursga`) | 32000 | 13 | 10.8 game min (7.7 real min) | 5.4 game min (3.9 real min) | 2.2 game min (1.5 real min) | 1.1 game min (0.8 real min) | 50 game s (36 real s) |
| **Wall** (`eurswa`) | 50000 | 4 | 16.9 game min (12.1 real min) | 8.5 game min (6.0 real min) | 4.2 game min (3.0 real min) | 4.2 game min (3.0 real min) | 4.2 game min (3.0 real min) |
| **Tower** (`eurtow`) | 20000 | 10 | 6.8 game min (4.8 real min) | 3.4 game min (2.4 real min) | 1.4 game min (1.0 real min) | 41 game s (29 real s) | 41 game s (29 real s) |
| **Academy** (`spaaca`) | 63000 | 26 | 21.3 game min (15.2 real min) | 10.7 game min (7.6 real min) | 4.3 game min (3.0 real min) | 2.1 game min (1.5 real min) | 49 game s (35 real s) |
| **Artillery Depot** (`spaart`) | 40000 | 23 | 13.5 game min (9.7 real min) | 6.8 game min (4.8 real min) | 2.7 game min (1.9 real min) | 1.4 game min (1.0 real min) | 35 game s (25 real s) |
| **Barracks, 18th century** (`spaba2`) | 55000 | 26 | 18.6 game min (13.3 real min) | 9.3 game min (6.6 real min) | 3.7 game min (2.7 real min) | 1.9 game min (1.3 real min) | 43 game s (31 real s) |
| **Barracks, 17th century** (`spabar`) | 40000 | 18 | 13.5 game min (9.7 real min) | 6.8 game min (4.8 real min) | 2.7 game min (1.9 real min) | 1.4 game min (1.0 real min) | 45 game s (32 real s) |
| **Blacksmith** (`spabla`) | 5500 | 13 | 1.9 game min (1.3 real min) | 56 game s (40 real s) | 22 game s (16 real s) | 11 game s (8 real s) | 9 game s (6 real s) |
| **Town Hall** (`spacen`) | 4250 | 24 | 1.4 game min (1.0 real min) | 43 game s (31 real s) | 17 game s (12 real s) | 9 game s (6 real s) | 4 game s (3 real s) |
| **Diplomatic Center** (`spadip`) | 4500 | 21 | 1.5 game min (1.1 real min) | 46 game s (33 real s) | 18 game s (13 real s) | 9 game s (7 real s) | 4 game s (3 real s) |
| **Housing** (`spahou`) | 4200 | 14 | 1.4 game min (1.0 real min) | 43 game s (30 real s) | 17 game s (12 real s) | 9 game s (6 real s) | 6 game s (4 real s) |
| **Market** (`spamar`) | 4000 | 24 | 1.4 game min (1.0 real min) | 41 game s (29 real s) | 16 game s (12 real s) | 8 game s (6 real s) | 3 game s (2 real s) |
| **Stable** (`spasta`) | 20000 | 21 | 6.8 game min (4.8 real min) | 3.4 game min (2.4 real min) | 1.4 game min (1.0 real min) | 41 game s (29 real s) | 19 game s (14 real s) |
| **Storehouse** (`spasto`) | 10000 | 7 | 3.4 game min (2.4 real min) | 1.7 game min (1.2 real min) | 41 game s (29 real s) | 29 game s (21 real s) | 29 game s (21 real s) |
| **Cathedral** (`spatem`) | 4200 | 30 | 1.4 game min (1.0 real min) | 43 game s (30 real s) | 17 game s (12 real s) | 9 game s (6 real s) | 3 game s (2 real s) |
| **Gate** (`ukrwga`) | 1500 | 13 | 30 game s (22 real s) | 15 game s (11 real s) | 6 game s (4 real s) | 3 game s (2 real s) | 2 game s (2 real s) |
| **Palisade** (`ukrwwa`) | 1500 | 4 | 30 game s (22 real s) | 15 game s (11 real s) | 8 game s (5 real s) | 8 game s (5 real s) | 8 game s (5 real s) |

<a id="swe--sweden-швеция"></a>
<a id="швеция-swe"></a>
## Sweden (`swe`)
<a id="постройка-с-нуля-16"></a>
### Building from scratch

| Building | Base build time, game s | Builder limit | 1 Peasant | 2 Peasants | 5 Peasants | 10 Peasants | At slot limit |
| --- | --- | --- | --- | --- | --- | --- | --- |
| **Mine** (`eurcoa`) | 94 | 16 | 1.8 game min (1.3 real min) | 53 game s (38 real s) | 21 game s (15 real s) | 11 game s (8 real s) | 7 game s (5 real s) |
| **Mine** (`eurgol`) | 94 | 16 | 1.8 game min (1.3 real min) | 53 game s (38 real s) | 21 game s (15 real s) | 11 game s (8 real s) | 7 game s (5 real s) |
| **Mine** (`euriro`) | 94 | 16 | 1.8 game min (1.3 real min) | 53 game s (38 real s) | 21 game s (15 real s) | 11 game s (8 real s) | 7 game s (5 real s) |
| **Market** (`eurmar`) | 234 | 25 | 4.4 game min (3.2 real min) | 2.2 game min (1.6 real min) | 53 game s (38 real s) | 26 game s (19 real s) | 11 game s (8 real s) |
| **Mill** (`eurmil`) | 94 | 10 | 1.8 game min (1.3 real min) | 53 game s (38 real s) | 21 game s (15 real s) | 11 game s (8 real s) | 11 game s (8 real s) |
| **Shipyard** (`eurpor`) | 1562 | 30 | 29.4 game min (21.0 real min) | 14.7 game min (10.5 real min) | 5.9 game min (4.2 real min) | 2.9 game min (2.1 real min) | 59 game s (42 real s) |
| **Gate** (`eursga`) | 90 | 13 | 1.7 game min (1.2 real min) | 51 game s (36 real s) | 20 game s (15 real s) | 10 game s (7 real s) | 8 game s (6 real s) |
| **Storehouse** (`eursto`) | 31 | 9 | 35 game s (25 real s) | 18 game s (13 real s) | 7 game s (5 real s) | 4 game s (3 real s) | 4 game s (3 real s) |
| **Wall** (`eurswa`) | 90 | 4 | 1.7 game min (1.2 real min) | 51 game s (36 real s) | 25 game s (18 real s) | 25 game s (18 real s) | 25 game s (18 real s) |
| **Tower** (`eurtow`) | 1230 | 10 | 23.2 game min (16.6 real min) | 11.6 game min (8.3 real min) | 4.6 game min (3.3 real min) | 2.3 game min (1.7 real min) | 2.3 game min (1.7 real min) |
| **Academy** (`sweaca`) | 625 | 18 | 11.8 game min (8.4 real min) | 5.9 game min (4.2 real min) | 2.4 game min (1.7 real min) | 1.2 game min (0.8 real min) | 39 game s (28 real s) |
| **Artillery Depot** (`sweart`) | 246 | 20 | 4.6 game min (3.3 real min) | 2.3 game min (1.7 real min) | 56 game s (40 real s) | 28 game s (20 real s) | 14 game s (10 real s) |
| **Barracks, 18th century** (`sweba2`) | 5625 | 27 | 105.9 game min (75.7 real min) | 53.0 game min (37.8 real min) | 21.2 game min (15.1 real min) | 10.6 game min (7.6 real min) | 3.9 game min (2.8 real min) |
| **Barracks, 17th century** (`swebar`) | 94 | 25 | 1.8 game min (1.3 real min) | 53 game s (38 real s) | 21 game s (15 real s) | 11 game s (8 real s) | 4 game s (3 real s) |
| **Blacksmith** (`swebla`) | 94 | 16 | 1.8 game min (1.3 real min) | 53 game s (38 real s) | 21 game s (15 real s) | 11 game s (8 real s) | 7 game s (5 real s) |
| **Town Hall** (`swecen`) | 156 | 27 | 2.9 game min (2.1 real min) | 1.5 game min (1.1 real min) | 35 game s (25 real s) | 18 game s (13 real s) | 7 game s (5 real s) |
| **Diplomatic Center** (`swedip`) | 312 | 17 | 5.9 game min (4.2 real min) | 2.9 game min (2.1 real min) | 1.2 game min (0.8 real min) | 35 game s (25 real s) | 21 game s (15 real s) |
| **Housing** (`swehou`) | 31 | 15 | 35 game s (25 real s) | 18 game s (13 real s) | 7 game s (5 real s) | 4 game s (3 real s) | 2 game s (2 real s) |
| **Stable** (`swesta`) | 625 | 21 | 11.8 game min (8.4 real min) | 5.9 game min (4.2 real min) | 2.4 game min (1.7 real min) | 1.2 game min (0.8 real min) | 34 game s (24 real s) |
| **Cathedral** (`swetem`) | 156 | 23 | 2.9 game min (2.1 real min) | 1.5 game min (1.1 real min) | 35 game s (25 real s) | 18 game s (13 real s) | 8 game s (5 real s) |
| **Gate** (`ukrwga`) | 6 | 13 | 6 game s (5 real s) | 3 game s (2 real s) | 1 game s (1 real s) | 1 game s (0 real s) | 0 game s (0 real s) |
| **Palisade** (`ukrwwa`) | 6 | 4 | 6 game s (5 real s) | 3 game s (2 real s) | 2 game s (1 real s) | 2 game s (1 real s) | 2 game s (1 real s) |

<a id="полный-ремонт-0--max-hp-15"></a>
<a id="полный-ремонт-16"></a>
### Full repair (0 → max HP)

| Building | Maximum health | Builder limit | 1 Peasant | 2 Peasants | 5 Peasants | 10 Peasants | At slot limit |
| --- | --- | --- | --- | --- | --- | --- | --- |
| **Mine** (`eurcoa`) | 2500 | 16 | 51 game s (36 real s) | 25 game s (18 real s) | 10 game s (7 real s) | 5 game s (4 real s) | 3 game s (2 real s) |
| **Mine** (`eurgol`) | 2500 | 16 | 51 game s (36 real s) | 25 game s (18 real s) | 10 game s (7 real s) | 5 game s (4 real s) | 3 game s (2 real s) |
| **Mine** (`euriro`) | 2500 | 16 | 51 game s (36 real s) | 25 game s (18 real s) | 10 game s (7 real s) | 5 game s (4 real s) | 3 game s (2 real s) |
| **Market** (`eurmar`) | 4000 | 25 | 1.4 game min (1.0 real min) | 41 game s (29 real s) | 16 game s (12 real s) | 8 game s (6 real s) | 3 game s (2 real s) |
| **Mill** (`eurmil`) | 20000 | 10 | 6.8 game min (4.8 real min) | 3.4 game min (2.4 real min) | 1.4 game min (1.0 real min) | 41 game s (29 real s) | 41 game s (29 real s) |
| **Shipyard** (`eurpor`) | 50000 | 30 | 16.9 game min (12.1 real min) | 8.5 game min (6.0 real min) | 3.4 game min (2.4 real min) | 1.7 game min (1.2 real min) | 34 game s (24 real s) |
| **Gate** (`eursga`) | 32000 | 13 | 10.8 game min (7.7 real min) | 5.4 game min (3.9 real min) | 2.2 game min (1.5 real min) | 1.1 game min (0.8 real min) | 50 game s (36 real s) |
| **Storehouse** (`eursto`) | 10000 | 9 | 3.4 game min (2.4 real min) | 1.7 game min (1.2 real min) | 41 game s (29 real s) | 23 game s (16 real s) | 23 game s (16 real s) |
| **Wall** (`eurswa`) | 50000 | 4 | 16.9 game min (12.1 real min) | 8.5 game min (6.0 real min) | 4.2 game min (3.0 real min) | 4.2 game min (3.0 real min) | 4.2 game min (3.0 real min) |
| **Tower** (`eurtow`) | 20000 | 10 | 6.8 game min (4.8 real min) | 3.4 game min (2.4 real min) | 1.4 game min (1.0 real min) | 41 game s (29 real s) | 41 game s (29 real s) |
| **Academy** (`sweaca`) | 63000 | 18 | 21.3 game min (15.2 real min) | 10.7 game min (7.6 real min) | 4.3 game min (3.0 real min) | 2.1 game min (1.5 real min) | 1.2 game min (0.8 real min) |
| **Artillery Depot** (`sweart`) | 40000 | 20 | 13.5 game min (9.7 real min) | 6.8 game min (4.8 real min) | 2.7 game min (1.9 real min) | 1.4 game min (1.0 real min) | 41 game s (29 real s) |
| **Barracks, 18th century** (`sweba2`) | 55000 | 27 | 18.6 game min (13.3 real min) | 9.3 game min (6.6 real min) | 3.7 game min (2.7 real min) | 1.9 game min (1.3 real min) | 41 game s (30 real s) |
| **Barracks, 17th century** (`swebar`) | 40000 | 25 | 13.5 game min (9.7 real min) | 6.8 game min (4.8 real min) | 2.7 game min (1.9 real min) | 1.4 game min (1.0 real min) | 32 game s (23 real s) |
| **Blacksmith** (`swebla`) | 5500 | 16 | 1.9 game min (1.3 real min) | 56 game s (40 real s) | 22 game s (16 real s) | 11 game s (8 real s) | 7 game s (5 real s) |
| **Town Hall** (`swecen`) | 5000 | 27 | 1.7 game min (1.2 real min) | 51 game s (36 real s) | 20 game s (15 real s) | 10 game s (7 real s) | 4 game s (3 real s) |
| **Diplomatic Center** (`swedip`) | 4500 | 17 | 1.5 game min (1.1 real min) | 46 game s (33 real s) | 18 game s (13 real s) | 9 game s (7 real s) | 5 game s (4 real s) |
| **Housing** (`swehou`) | 5000 | 15 | 1.7 game min (1.2 real min) | 51 game s (36 real s) | 20 game s (15 real s) | 10 game s (7 real s) | 7 game s (5 real s) |
| **Stable** (`swesta`) | 20000 | 21 | 6.8 game min (4.8 real min) | 3.4 game min (2.4 real min) | 1.4 game min (1.0 real min) | 41 game s (29 real s) | 19 game s (14 real s) |
| **Cathedral** (`swetem`) | 4200 | 23 | 1.4 game min (1.0 real min) | 43 game s (30 real s) | 17 game s (12 real s) | 9 game s (6 real s) | 4 game s (3 real s) |
| **Gate** (`ukrwga`) | 1500 | 13 | 30 game s (22 real s) | 15 game s (11 real s) | 6 game s (4 real s) | 3 game s (2 real s) | 2 game s (2 real s) |
| **Palisade** (`ukrwwa`) | 1500 | 4 | 30 game s (22 real s) | 15 game s (11 real s) | 8 game s (5 real s) | 8 game s (5 real s) | 8 game s (5 real s) |

<a id="swi--switzerland-швейцария"></a>
<a id="швейцария-swi"></a>
## Switzerland (`swi`)
<a id="постройка-с-нуля-17"></a>
### Building from scratch

| Building | Base build time, game s | Builder limit | 1 Peasant | 2 Peasants | 5 Peasants | 10 Peasants | At slot limit |
| --- | --- | --- | --- | --- | --- | --- | --- |
| **Mine** (`eurcoa`) | 94 | 16 | 1.8 game min (1.3 real min) | 53 game s (38 real s) | 21 game s (15 real s) | 11 game s (8 real s) | 7 game s (5 real s) |
| **Mine** (`eurgol`) | 94 | 16 | 1.8 game min (1.3 real min) | 53 game s (38 real s) | 21 game s (15 real s) | 11 game s (8 real s) | 7 game s (5 real s) |
| **Mine** (`euriro`) | 94 | 16 | 1.8 game min (1.3 real min) | 53 game s (38 real s) | 21 game s (15 real s) | 11 game s (8 real s) | 7 game s (5 real s) |
| **Market** (`eurmar`) | 234 | 25 | 4.4 game min (3.2 real min) | 2.2 game min (1.6 real min) | 53 game s (38 real s) | 26 game s (19 real s) | 11 game s (8 real s) |
| **Mill** (`eurmil`) | 94 | 10 | 1.8 game min (1.3 real min) | 53 game s (38 real s) | 21 game s (15 real s) | 11 game s (8 real s) | 11 game s (8 real s) |
| **Shipyard** (`eurpor`) | 1562 | 30 | 29.4 game min (21.0 real min) | 14.7 game min (10.5 real min) | 5.9 game min (4.2 real min) | 2.9 game min (2.1 real min) | 59 game s (42 real s) |
| **Gate** (`eursga`) | 90 | 13 | 1.7 game min (1.2 real min) | 51 game s (36 real s) | 20 game s (15 real s) | 10 game s (7 real s) | 8 game s (6 real s) |
| **Storehouse** (`eursto`) | 31 | 9 | 35 game s (25 real s) | 18 game s (13 real s) | 7 game s (5 real s) | 4 game s (3 real s) | 4 game s (3 real s) |
| **Wall** (`eurswa`) | 90 | 4 | 1.7 game min (1.2 real min) | 51 game s (36 real s) | 25 game s (18 real s) | 25 game s (18 real s) | 25 game s (18 real s) |
| **Tower** (`eurtow`) | 1230 | 10 | 23.2 game min (16.6 real min) | 11.6 game min (8.3 real min) | 4.6 game min (3.3 real min) | 2.3 game min (1.7 real min) | 2.3 game min (1.7 real min) |
| **Academy** (`swiaca`) | 625 | 22 | 11.8 game min (8.4 real min) | 5.9 game min (4.2 real min) | 2.4 game min (1.7 real min) | 1.2 game min (0.8 real min) | 32 game s (23 real s) |
| **Artillery Depot** (`swiart`) | 246 | 20 | 4.6 game min (3.3 real min) | 2.3 game min (1.7 real min) | 56 game s (40 real s) | 28 game s (20 real s) | 14 game s (10 real s) |
| **Barracks, 18th century** (`swiba2`) | 5625 | 22 | 105.9 game min (75.7 real min) | 53.0 game min (37.8 real min) | 21.2 game min (15.1 real min) | 10.6 game min (7.6 real min) | 4.8 game min (3.4 real min) |
| **Barracks, 17th century** (`swibar`) | 94 | 23 | 1.8 game min (1.3 real min) | 53 game s (38 real s) | 21 game s (15 real s) | 11 game s (8 real s) | 5 game s (3 real s) |
| **Blacksmith** (`swibla`) | 94 | 17 | 1.8 game min (1.3 real min) | 53 game s (38 real s) | 21 game s (15 real s) | 11 game s (8 real s) | 6 game s (4 real s) |
| **Town Hall** (`swicen`) | 156 | 23 | 2.9 game min (2.1 real min) | 1.5 game min (1.1 real min) | 35 game s (25 real s) | 18 game s (13 real s) | 8 game s (5 real s) |
| **Diplomatic Center** (`swidip`) | 312 | 18 | 5.9 game min (4.2 real min) | 2.9 game min (2.1 real min) | 1.2 game min (0.8 real min) | 35 game s (25 real s) | 20 game s (14 real s) |
| **Housing** (`swihou`) | 31 | 11 | 35 game s (25 real s) | 18 game s (13 real s) | 7 game s (5 real s) | 4 game s (3 real s) | 3 game s (2 real s) |
| **Stable** (`swista`) | 625 | 18 | 11.8 game min (8.4 real min) | 5.9 game min (4.2 real min) | 2.4 game min (1.7 real min) | 1.2 game min (0.8 real min) | 39 game s (28 real s) |
| **Cathedral** (`switem`) | 156 | 21 | 2.9 game min (2.1 real min) | 1.5 game min (1.1 real min) | 35 game s (25 real s) | 18 game s (13 real s) | 8 game s (6 real s) |
| **Gate** (`ukrwga`) | 6 | 13 | 6 game s (5 real s) | 3 game s (2 real s) | 1 game s (1 real s) | 1 game s (0 real s) | 0 game s (0 real s) |
| **Palisade** (`ukrwwa`) | 6 | 4 | 6 game s (5 real s) | 3 game s (2 real s) | 2 game s (1 real s) | 2 game s (1 real s) | 2 game s (1 real s) |

<a id="полный-ремонт-0--max-hp-16"></a>
<a id="полный-ремонт-17"></a>
### Full repair (0 → max HP)

| Building | Maximum health | Builder limit | 1 Peasant | 2 Peasants | 5 Peasants | 10 Peasants | At slot limit |
| --- | --- | --- | --- | --- | --- | --- | --- |
| **Mine** (`eurcoa`) | 2500 | 16 | 51 game s (36 real s) | 25 game s (18 real s) | 10 game s (7 real s) | 5 game s (4 real s) | 3 game s (2 real s) |
| **Mine** (`eurgol`) | 2500 | 16 | 51 game s (36 real s) | 25 game s (18 real s) | 10 game s (7 real s) | 5 game s (4 real s) | 3 game s (2 real s) |
| **Mine** (`euriro`) | 2500 | 16 | 51 game s (36 real s) | 25 game s (18 real s) | 10 game s (7 real s) | 5 game s (4 real s) | 3 game s (2 real s) |
| **Market** (`eurmar`) | 4000 | 25 | 1.4 game min (1.0 real min) | 41 game s (29 real s) | 16 game s (12 real s) | 8 game s (6 real s) | 3 game s (2 real s) |
| **Mill** (`eurmil`) | 20000 | 10 | 6.8 game min (4.8 real min) | 3.4 game min (2.4 real min) | 1.4 game min (1.0 real min) | 41 game s (29 real s) | 41 game s (29 real s) |
| **Shipyard** (`eurpor`) | 50000 | 30 | 16.9 game min (12.1 real min) | 8.5 game min (6.0 real min) | 3.4 game min (2.4 real min) | 1.7 game min (1.2 real min) | 34 game s (24 real s) |
| **Gate** (`eursga`) | 32000 | 13 | 10.8 game min (7.7 real min) | 5.4 game min (3.9 real min) | 2.2 game min (1.5 real min) | 1.1 game min (0.8 real min) | 50 game s (36 real s) |
| **Storehouse** (`eursto`) | 10000 | 9 | 3.4 game min (2.4 real min) | 1.7 game min (1.2 real min) | 41 game s (29 real s) | 23 game s (16 real s) | 23 game s (16 real s) |
| **Wall** (`eurswa`) | 50000 | 4 | 16.9 game min (12.1 real min) | 8.5 game min (6.0 real min) | 4.2 game min (3.0 real min) | 4.2 game min (3.0 real min) | 4.2 game min (3.0 real min) |
| **Tower** (`eurtow`) | 20000 | 10 | 6.8 game min (4.8 real min) | 3.4 game min (2.4 real min) | 1.4 game min (1.0 real min) | 41 game s (29 real s) | 41 game s (29 real s) |
| **Academy** (`swiaca`) | 63000 | 22 | 21.3 game min (15.2 real min) | 10.7 game min (7.6 real min) | 4.3 game min (3.0 real min) | 2.1 game min (1.5 real min) | 58 game s (42 real s) |
| **Artillery Depot** (`swiart`) | 40000 | 20 | 13.5 game min (9.7 real min) | 6.8 game min (4.8 real min) | 2.7 game min (1.9 real min) | 1.4 game min (1.0 real min) | 41 game s (29 real s) |
| **Barracks, 18th century** (`swiba2`) | 55000 | 22 | 18.6 game min (13.3 real min) | 9.3 game min (6.6 real min) | 3.7 game min (2.7 real min) | 1.9 game min (1.3 real min) | 51 game s (36 real s) |
| **Barracks, 17th century** (`swibar`) | 40000 | 23 | 13.5 game min (9.7 real min) | 6.8 game min (4.8 real min) | 2.7 game min (1.9 real min) | 1.4 game min (1.0 real min) | 35 game s (25 real s) |
| **Blacksmith** (`swibla`) | 5500 | 17 | 1.9 game min (1.3 real min) | 56 game s (40 real s) | 22 game s (16 real s) | 11 game s (8 real s) | 7 game s (5 real s) |
| **Town Hall** (`swicen`) | 4000 | 23 | 1.4 game min (1.0 real min) | 41 game s (29 real s) | 16 game s (12 real s) | 8 game s (6 real s) | 4 game s (3 real s) |
| **Diplomatic Center** (`swidip`) | 4500 | 18 | 1.5 game min (1.1 real min) | 46 game s (33 real s) | 18 game s (13 real s) | 9 game s (7 real s) | 5 game s (4 real s) |
| **Housing** (`swihou`) | 4000 | 11 | 1.4 game min (1.0 real min) | 41 game s (29 real s) | 16 game s (12 real s) | 8 game s (6 real s) | 7 game s (5 real s) |
| **Stable** (`swista`) | 20000 | 18 | 6.8 game min (4.8 real min) | 3.4 game min (2.4 real min) | 1.4 game min (1.0 real min) | 41 game s (29 real s) | 23 game s (16 real s) |
| **Cathedral** (`switem`) | 4200 | 21 | 1.4 game min (1.0 real min) | 43 game s (30 real s) | 17 game s (12 real s) | 9 game s (6 real s) | 4 game s (3 real s) |
| **Gate** (`ukrwga`) | 1500 | 13 | 30 game s (22 real s) | 15 game s (11 real s) | 6 game s (4 real s) | 3 game s (2 real s) | 2 game s (2 real s) |
| **Palisade** (`ukrwwa`) | 1500 | 4 | 30 game s (22 real s) | 15 game s (11 real s) | 8 game s (5 real s) | 8 game s (5 real s) | 8 game s (5 real s) |

<a id="tur--turkey-турция"></a>
<a id="турция-tur"></a>
## Turkey (`tur`)
<a id="постройка-с-нуля-18"></a>
### Building from scratch

| Building | Base build time, game s | Builder limit | 1 Peasant | 2 Peasants | 5 Peasants | 10 Peasants | At slot limit |
| --- | --- | --- | --- | --- | --- | --- | --- |
| **Mine** (`eurcoa`) | 94 | 16 | 1.8 game min (1.3 real min) | 53 game s (38 real s) | 21 game s (15 real s) | 11 game s (8 real s) | 7 game s (5 real s) |
| **Mine** (`eurgol`) | 94 | 16 | 1.8 game min (1.3 real min) | 53 game s (38 real s) | 21 game s (15 real s) | 11 game s (8 real s) | 7 game s (5 real s) |
| **Mine** (`euriro`) | 94 | 16 | 1.8 game min (1.3 real min) | 53 game s (38 real s) | 21 game s (15 real s) | 11 game s (8 real s) | 7 game s (5 real s) |
| **Minaret** (`turaca`) | 156 | 6 | 2.9 game min (2.1 real min) | 1.5 game min (1.1 real min) | 35 game s (25 real s) | 29 game s (21 real s) | 29 game s (21 real s) |
| **Artillery Depot** (`turart`) | 246 | 28 | 4.6 game min (3.3 real min) | 2.3 game min (1.7 real min) | 56 game s (40 real s) | 28 game s (20 real s) | 10 game s (7 real s) |
| **Barracks** (`turbar`) | 94 | 22 | 1.8 game min (1.3 real min) | 53 game s (38 real s) | 21 game s (15 real s) | 11 game s (8 real s) | 5 game s (3 real s) |
| **Blacksmith** (`turbla`) | 109 | 15 | 2.1 game min (1.5 real min) | 1.0 game min (0.7 real min) | 25 game s (18 real s) | 12 game s (9 real s) | 8 game s (6 real s) |
| **Town Hall** (`turcen`) | 156 | 22 | 2.9 game min (2.1 real min) | 1.5 game min (1.1 real min) | 35 game s (25 real s) | 18 game s (13 real s) | 8 game s (6 real s) |
| **Diplomatic Center** (`turdip`) | 312 | 22 | 5.9 game min (4.2 real min) | 2.9 game min (2.1 real min) | 1.2 game min (0.8 real min) | 35 game s (25 real s) | 16 game s (11 real s) |
| **Housing** (`turhou`) | 31 | 14 | 35 game s (25 real s) | 18 game s (13 real s) | 7 game s (5 real s) | 4 game s (3 real s) | 3 game s (2 real s) |
| **Bazaar** (`turmar`) | 234 | 19 | 4.4 game min (3.2 real min) | 2.2 game min (1.6 real min) | 53 game s (38 real s) | 26 game s (19 real s) | 14 game s (10 real s) |
| **Mill** (`turmil`) | 94 | 16 | 1.8 game min (1.3 real min) | 53 game s (38 real s) | 21 game s (15 real s) | 11 game s (8 real s) | 7 game s (5 real s) |
| **Shipyard** (`turpor`) | 1562 | 30 | 29.4 game min (21.0 real min) | 14.7 game min (10.5 real min) | 5.9 game min (4.2 real min) | 2.9 game min (2.1 real min) | 59 game s (42 real s) |
| **Gate** (`tursga`) | 120 | 13 | 2.3 game min (1.6 real min) | 1.1 game min (0.8 real min) | 27 game s (19 real s) | 14 game s (10 real s) | 10 game s (7 real s) |
| **Stable** (`tursta`) | 156 | 25 | 2.9 game min (2.1 real min) | 1.5 game min (1.1 real min) | 35 game s (25 real s) | 18 game s (13 real s) | 7 game s (5 real s) |
| **Storehouse** (`tursto`) | 31 | 8 | 35 game s (25 real s) | 18 game s (13 real s) | 7 game s (5 real s) | 4 game s (3 real s) | 4 game s (3 real s) |
| **Wall** (`turswa`) | 120 | 4 | 2.3 game min (1.6 real min) | 1.1 game min (0.8 real min) | 34 game s (24 real s) | 34 game s (24 real s) | 34 game s (24 real s) |
| **Mosque** (`turtem`) | 94 | 22 | 1.8 game min (1.3 real min) | 53 game s (38 real s) | 21 game s (15 real s) | 11 game s (8 real s) | 5 game s (3 real s) |
| **Tower** (`turtow`) | 984 | 14 | 18.5 game min (13.2 real min) | 9.3 game min (6.6 real min) | 3.7 game min (2.6 real min) | 1.9 game min (1.3 real min) | 1.3 game min (0.9 real min) |
| **Gate** (`ukrwga`) | 6 | 13 | 6 game s (5 real s) | 3 game s (2 real s) | 1 game s (1 real s) | 1 game s (0 real s) | 0 game s (0 real s) |
| **Palisade** (`ukrwwa`) | 6 | 4 | 6 game s (5 real s) | 3 game s (2 real s) | 2 game s (1 real s) | 2 game s (1 real s) | 2 game s (1 real s) |

<a id="полный-ремонт-0--max-hp-17"></a>
<a id="полный-ремонт-18"></a>
### Full repair (0 → max HP)

| Building | Maximum health | Builder limit | 1 Peasant | 2 Peasants | 5 Peasants | 10 Peasants | At slot limit |
| --- | --- | --- | --- | --- | --- | --- | --- |
| **Mine** (`eurcoa`) | 2500 | 16 | 51 game s (36 real s) | 25 game s (18 real s) | 10 game s (7 real s) | 5 game s (4 real s) | 3 game s (2 real s) |
| **Mine** (`eurgol`) | 2500 | 16 | 51 game s (36 real s) | 25 game s (18 real s) | 10 game s (7 real s) | 5 game s (4 real s) | 3 game s (2 real s) |
| **Mine** (`euriro`) | 2500 | 16 | 51 game s (36 real s) | 25 game s (18 real s) | 10 game s (7 real s) | 5 game s (4 real s) | 3 game s (2 real s) |
| **Minaret** (`turaca`) | 65000 | 6 | 22.0 game min (15.7 real min) | 11.0 game min (7.9 real min) | 4.4 game min (3.1 real min) | 3.7 game min (2.6 real min) | 3.7 game min (2.6 real min) |
| **Artillery Depot** (`turart`) | 40000 | 28 | 13.5 game min (9.7 real min) | 6.8 game min (4.8 real min) | 2.7 game min (1.9 real min) | 1.4 game min (1.0 real min) | 29 game s (21 real s) |
| **Barracks** (`turbar`) | 35000 | 22 | 11.8 game min (8.5 real min) | 5.9 game min (4.2 real min) | 2.4 game min (1.7 real min) | 1.2 game min (0.8 real min) | 32 game s (23 real s) |
| **Blacksmith** (`turbla`) | 6500 | 15 | 2.2 game min (1.6 real min) | 1.1 game min (0.8 real min) | 26 game s (19 real s) | 13 game s (9 real s) | 9 game s (6 real s) |
| **Town Hall** (`turcen`) | 4000 | 22 | 1.4 game min (1.0 real min) | 41 game s (29 real s) | 16 game s (12 real s) | 8 game s (6 real s) | 4 game s (3 real s) |
| **Diplomatic Center** (`turdip`) | 5500 | 22 | 1.9 game min (1.3 real min) | 56 game s (40 real s) | 22 game s (16 real s) | 11 game s (8 real s) | 5 game s (4 real s) |
| **Housing** (`turhou`) | 4000 | 14 | 1.4 game min (1.0 real min) | 41 game s (29 real s) | 16 game s (12 real s) | 8 game s (6 real s) | 6 game s (4 real s) |
| **Bazaar** (`turmar`) | 4500 | 19 | 1.5 game min (1.1 real min) | 46 game s (33 real s) | 18 game s (13 real s) | 9 game s (7 real s) | 5 game s (3 real s) |
| **Mill** (`turmil`) | 20000 | 16 | 6.8 game min (4.8 real min) | 3.4 game min (2.4 real min) | 1.4 game min (1.0 real min) | 41 game s (29 real s) | 25 game s (18 real s) |
| **Shipyard** (`turpor`) | 40000 | 30 | 13.5 game min (9.7 real min) | 6.8 game min (4.8 real min) | 2.7 game min (1.9 real min) | 1.4 game min (1.0 real min) | 27 game s (19 real s) |
| **Gate** (`tursga`) | 32000 | 13 | 10.8 game min (7.7 real min) | 5.4 game min (3.9 real min) | 2.2 game min (1.5 real min) | 1.1 game min (0.8 real min) | 50 game s (36 real s) |
| **Stable** (`tursta`) | 55000 | 25 | 18.6 game min (13.3 real min) | 9.3 game min (6.6 real min) | 3.7 game min (2.7 real min) | 1.9 game min (1.3 real min) | 45 game s (32 real s) |
| **Storehouse** (`tursto`) | 10000 | 8 | 3.4 game min (2.4 real min) | 1.7 game min (1.2 real min) | 41 game s (29 real s) | 25 game s (18 real s) | 25 game s (18 real s) |
| **Wall** (`turswa`) | 50000 | 4 | 16.9 game min (12.1 real min) | 8.5 game min (6.0 real min) | 4.2 game min (3.0 real min) | 4.2 game min (3.0 real min) | 4.2 game min (3.0 real min) |
| **Mosque** (`turtem`) | 5000 | 22 | 1.7 game min (1.2 real min) | 51 game s (36 real s) | 20 game s (15 real s) | 10 game s (7 real s) | 5 game s (3 real s) |
| **Tower** (`turtow`) | 22500 | 14 | 7.6 game min (5.4 real min) | 3.8 game min (2.7 real min) | 1.5 game min (1.1 real min) | 46 game s (33 real s) | 33 game s (23 real s) |
| **Gate** (`ukrwga`) | 1500 | 13 | 30 game s (22 real s) | 15 game s (11 real s) | 6 game s (4 real s) | 3 game s (2 real s) | 2 game s (2 real s) |
| **Palisade** (`ukrwwa`) | 1500 | 4 | 30 game s (22 real s) | 15 game s (11 real s) | 8 game s (5 real s) | 8 game s (5 real s) | 8 game s (5 real s) |

<a id="ukr--ukraine-украина"></a>
<a id="украина-ukr"></a>
## Ukraine (`ukr`)
<a id="постройка-с-нуля-19"></a>
### Building from scratch

| Building | Base build time, game s | Builder limit | 1 Peasant | 2 Peasants | 5 Peasants | 10 Peasants | At slot limit |
| --- | --- | --- | --- | --- | --- | --- | --- |
| **Mine** (`eurcoa`) | 94 | 16 | 1.8 game min (1.3 real min) | 53 game s (38 real s) | 21 game s (15 real s) | 11 game s (8 real s) | 7 game s (5 real s) |
| **Mine** (`eurgol`) | 94 | 16 | 1.8 game min (1.3 real min) | 53 game s (38 real s) | 21 game s (15 real s) | 11 game s (8 real s) | 7 game s (5 real s) |
| **Mine** (`euriro`) | 94 | 16 | 1.8 game min (1.3 real min) | 53 game s (38 real s) | 21 game s (15 real s) | 11 game s (8 real s) | 7 game s (5 real s) |
| **Market** (`rusmar`) | 234 | 23 | 4.4 game min (3.2 real min) | 2.2 game min (1.6 real min) | 53 game s (38 real s) | 26 game s (19 real s) | 12 game s (8 real s) |
| **Mill** (`rusmil`) | 94 | 7 | 1.8 game min (1.3 real min) | 53 game s (38 real s) | 21 game s (15 real s) | 15 game s (11 real s) | 15 game s (11 real s) |
| **Storehouse** (`russto`) | 31 | 8 | 35 game s (25 real s) | 18 game s (13 real s) | 7 game s (5 real s) | 4 game s (3 real s) | 4 game s (3 real s) |
| **Academy** (`ukraca`) | 47 | 30 | 53 game s (38 real s) | 26 game s (19 real s) | 11 game s (8 real s) | 5 game s (4 real s) | 2 game s (1 real s) |
| **Artillery Depot** (`ukrart`) | 246 | 30 | 4.6 game min (3.3 real min) | 2.3 game min (1.7 real min) | 56 game s (40 real s) | 28 game s (20 real s) | 9 game s (7 real s) |
| **Cossack House** (`ukrbar`) | 94 | 23 | 1.8 game min (1.3 real min) | 53 game s (38 real s) | 21 game s (15 real s) | 11 game s (8 real s) | 5 game s (3 real s) |
| **Blacksmith** (`ukrbla`) | 62 | 19 | 1.2 game min (0.8 real min) | 35 game s (25 real s) | 14 game s (10 real s) | 7 game s (5 real s) | 4 game s (3 real s) |
| **Town Hall** (`ukrcen`) | 156 | 29 | 2.9 game min (2.1 real min) | 1.5 game min (1.1 real min) | 35 game s (25 real s) | 18 game s (13 real s) | 6 game s (4 real s) |
| **Diplomatic Center** (`ukrdip`) | 312 | 22 | 5.9 game min (4.2 real min) | 2.9 game min (2.1 real min) | 1.2 game min (0.8 real min) | 35 game s (25 real s) | 16 game s (11 real s) |
| **Hut** (`ukrhou`) | 31 | 16 | 35 game s (25 real s) | 18 game s (13 real s) | 7 game s (5 real s) | 4 game s (3 real s) | 2 game s (2 real s) |
| **Shipyard** (`ukrpor`) | 1562 | 30 | 29.4 game min (21.0 real min) | 14.7 game min (10.5 real min) | 5.9 game min (4.2 real min) | 2.9 game min (2.1 real min) | 59 game s (42 real s) |
| **Stable** (`ukrsta`) | 156 | 26 | 2.9 game min (2.1 real min) | 1.5 game min (1.1 real min) | 35 game s (25 real s) | 18 game s (13 real s) | 7 game s (5 real s) |
| **Orthodox Cathedral** (`ukrtem`) | 156 | 30 | 2.9 game min (2.1 real min) | 1.5 game min (1.1 real min) | 35 game s (25 real s) | 18 game s (13 real s) | 6 game s (4 real s) |
| **Gate** (`ukrwga`) | 8 | 13 | 9 game s (7 real s) | 5 game s (3 real s) | 2 game s (1 real s) | 1 game s (1 real s) | 1 game s (1 real s) |
| **Palisade** (`ukrwwa`) | 8 | 4 | 9 game s (7 real s) | 5 game s (3 real s) | 2 game s (2 real s) | 2 game s (2 real s) | 2 game s (2 real s) |

<a id="полный-ремонт-0--max-hp-18"></a>
<a id="полный-ремонт-19"></a>
### Full repair (0 → max HP)

| Building | Maximum health | Builder limit | 1 Peasant | 2 Peasants | 5 Peasants | 10 Peasants | At slot limit |
| --- | --- | --- | --- | --- | --- | --- | --- |
| **Mine** (`eurcoa`) | 2500 | 16 | 51 game s (36 real s) | 25 game s (18 real s) | 10 game s (7 real s) | 5 game s (4 real s) | 3 game s (2 real s) |
| **Mine** (`eurgol`) | 2500 | 16 | 51 game s (36 real s) | 25 game s (18 real s) | 10 game s (7 real s) | 5 game s (4 real s) | 3 game s (2 real s) |
| **Mine** (`euriro`) | 2500 | 16 | 51 game s (36 real s) | 25 game s (18 real s) | 10 game s (7 real s) | 5 game s (4 real s) | 3 game s (2 real s) |
| **Market** (`rusmar`) | 4000 | 23 | 1.4 game min (1.0 real min) | 41 game s (29 real s) | 16 game s (12 real s) | 8 game s (6 real s) | 4 game s (3 real s) |
| **Mill** (`rusmil`) | 15000 | 7 | 5.1 game min (3.6 real min) | 2.5 game min (1.8 real min) | 1.0 game min (0.7 real min) | 44 game s (31 real s) | 44 game s (31 real s) |
| **Storehouse** (`russto`) | 10000 | 8 | 3.4 game min (2.4 real min) | 1.7 game min (1.2 real min) | 41 game s (29 real s) | 25 game s (18 real s) | 25 game s (18 real s) |
| **Academy** (`ukraca`) | 65000 | 30 | 22.0 game min (15.7 real min) | 11.0 game min (7.9 real min) | 4.4 game min (3.1 real min) | 2.2 game min (1.6 real min) | 44 game s (31 real s) |
| **Artillery Depot** (`ukrart`) | 40000 | 30 | 13.5 game min (9.7 real min) | 6.8 game min (4.8 real min) | 2.7 game min (1.9 real min) | 1.4 game min (1.0 real min) | 27 game s (19 real s) |
| **Cossack House** (`ukrbar`) | 20000 | 23 | 6.8 game min (4.8 real min) | 3.4 game min (2.4 real min) | 1.4 game min (1.0 real min) | 41 game s (29 real s) | 18 game s (13 real s) |
| **Blacksmith** (`ukrbla`) | 4500 | 19 | 1.5 game min (1.1 real min) | 46 game s (33 real s) | 18 game s (13 real s) | 9 game s (7 real s) | 5 game s (3 real s) |
| **Town Hall** (`ukrcen`) | 5300 | 29 | 1.8 game min (1.3 real min) | 54 game s (38 real s) | 22 game s (15 real s) | 11 game s (8 real s) | 4 game s (3 real s) |
| **Diplomatic Center** (`ukrdip`) | 5000 | 22 | 1.7 game min (1.2 real min) | 51 game s (36 real s) | 20 game s (15 real s) | 10 game s (7 real s) | 5 game s (3 real s) |
| **Hut** (`ukrhou`) | 4150 | 16 | 1.4 game min (1.0 real min) | 42 game s (30 real s) | 17 game s (12 real s) | 8 game s (6 real s) | 5 game s (4 real s) |
| **Shipyard** (`ukrpor`) | 45000 | 30 | 15.2 game min (10.9 real min) | 7.6 game min (5.4 real min) | 3.0 game min (2.2 real min) | 1.5 game min (1.1 real min) | 30 game s (22 real s) |
| **Stable** (`ukrsta`) | 10000 | 26 | 3.4 game min (2.4 real min) | 1.7 game min (1.2 real min) | 41 game s (29 real s) | 20 game s (15 real s) | 8 game s (6 real s) |
| **Orthodox Cathedral** (`ukrtem`) | 5300 | 30 | 1.8 game min (1.3 real min) | 54 game s (38 real s) | 22 game s (15 real s) | 11 game s (8 real s) | 4 game s (3 real s) |
| **Gate** (`ukrwga`) | 2500 | 13 | 51 game s (36 real s) | 25 game s (18 real s) | 10 game s (7 real s) | 5 game s (4 real s) | 4 game s (3 real s) |
| **Palisade** (`ukrwwa`) | 2500 | 4 | 51 game s (36 real s) | 25 game s (18 real s) | 13 game s (9 real s) | 13 game s (9 real s) | 13 game s (9 real s) |

<a id="ven--venice-венеция"></a>
<a id="венеция-ven"></a>
## Venice (`ven`)
<a id="постройка-с-нуля-20"></a>
### Building from scratch

| Building | Base build time, game s | Builder limit | 1 Peasant | 2 Peasants | 5 Peasants | 10 Peasants | At slot limit |
| --- | --- | --- | --- | --- | --- | --- | --- |
| **Mine** (`eurcoa`) | 94 | 16 | 1.8 game min (1.3 real min) | 53 game s (38 real s) | 21 game s (15 real s) | 11 game s (8 real s) | 7 game s (5 real s) |
| **Mine** (`eurgol`) | 94 | 16 | 1.8 game min (1.3 real min) | 53 game s (38 real s) | 21 game s (15 real s) | 11 game s (8 real s) | 7 game s (5 real s) |
| **Mine** (`euriro`) | 94 | 16 | 1.8 game min (1.3 real min) | 53 game s (38 real s) | 21 game s (15 real s) | 11 game s (8 real s) | 7 game s (5 real s) |
| **Market** (`eurmar`) | 234 | 25 | 4.4 game min (3.2 real min) | 2.2 game min (1.6 real min) | 53 game s (38 real s) | 26 game s (19 real s) | 11 game s (8 real s) |
| **Mill** (`eurmil`) | 94 | 10 | 1.8 game min (1.3 real min) | 53 game s (38 real s) | 21 game s (15 real s) | 11 game s (8 real s) | 11 game s (8 real s) |
| **Shipyard** (`eurpor`) | 1562 | 30 | 29.4 game min (21.0 real min) | 14.7 game min (10.5 real min) | 5.9 game min (4.2 real min) | 2.9 game min (2.1 real min) | 59 game s (42 real s) |
| **Gate** (`eursga`) | 90 | 13 | 1.7 game min (1.2 real min) | 51 game s (36 real s) | 20 game s (15 real s) | 10 game s (7 real s) | 8 game s (6 real s) |
| **Storehouse** (`eursto`) | 31 | 9 | 35 game s (25 real s) | 18 game s (13 real s) | 7 game s (5 real s) | 4 game s (3 real s) | 4 game s (3 real s) |
| **Wall** (`eurswa`) | 90 | 4 | 1.7 game min (1.2 real min) | 51 game s (36 real s) | 25 game s (18 real s) | 25 game s (18 real s) | 25 game s (18 real s) |
| **Tower** (`eurtow`) | 1230 | 10 | 23.2 game min (16.6 real min) | 11.6 game min (8.3 real min) | 4.6 game min (3.3 real min) | 2.3 game min (1.7 real min) | 2.3 game min (1.7 real min) |
| **Gate** (`ukrwga`) | 6 | 13 | 6 game s (5 real s) | 3 game s (2 real s) | 1 game s (1 real s) | 1 game s (0 real s) | 0 game s (0 real s) |
| **Palisade** (`ukrwwa`) | 6 | 4 | 6 game s (5 real s) | 3 game s (2 real s) | 2 game s (1 real s) | 2 game s (1 real s) | 2 game s (1 real s) |
| **Academy** (`venaca`) | 625 | 22 | 11.8 game min (8.4 real min) | 5.9 game min (4.2 real min) | 2.4 game min (1.7 real min) | 1.2 game min (0.8 real min) | 32 game s (23 real s) |
| **Artillery Depot** (`venart`) | 246 | 20 | 4.6 game min (3.3 real min) | 2.3 game min (1.7 real min) | 56 game s (40 real s) | 28 game s (20 real s) | 14 game s (10 real s) |
| **Barracks, 18th century** (`venba2`) | 5625 | 19 | 105.9 game min (75.7 real min) | 53.0 game min (37.8 real min) | 21.2 game min (15.1 real min) | 10.6 game min (7.6 real min) | 5.6 game min (4.0 real min) |
| **Barracks, 17th century** (`venbar`) | 94 | 23 | 1.8 game min (1.3 real min) | 53 game s (38 real s) | 21 game s (15 real s) | 11 game s (8 real s) | 5 game s (3 real s) |
| **Blacksmith** (`venbla`) | 94 | 16 | 1.8 game min (1.3 real min) | 53 game s (38 real s) | 21 game s (15 real s) | 11 game s (8 real s) | 7 game s (5 real s) |
| **Town Hall** (`vencen`) | 156 | 28 | 2.9 game min (2.1 real min) | 1.5 game min (1.1 real min) | 35 game s (25 real s) | 18 game s (13 real s) | 6 game s (5 real s) |
| **Diplomatic Center** (`vendip`) | 312 | 18 | 5.9 game min (4.2 real min) | 2.9 game min (2.1 real min) | 1.2 game min (0.8 real min) | 35 game s (25 real s) | 20 game s (14 real s) |
| **Housing** (`venhou`) | 31 | 10 | 35 game s (25 real s) | 18 game s (13 real s) | 7 game s (5 real s) | 4 game s (3 real s) | 4 game s (3 real s) |
| **Stable** (`vensta`) | 625 | 19 | 11.8 game min (8.4 real min) | 5.9 game min (4.2 real min) | 2.4 game min (1.7 real min) | 1.2 game min (0.8 real min) | 37 game s (27 real s) |
| **Cathedral** (`ventem`) | 156 | 30 | 2.9 game min (2.1 real min) | 1.5 game min (1.1 real min) | 35 game s (25 real s) | 18 game s (13 real s) | 6 game s (4 real s) |

<a id="полный-ремонт-0--max-hp-19"></a>
<a id="полный-ремонт-20"></a>
### Full repair (0 → max HP)

| Building | Maximum health | Builder limit | 1 Peasant | 2 Peasants | 5 Peasants | 10 Peasants | At slot limit |
| --- | --- | --- | --- | --- | --- | --- | --- |
| **Mine** (`eurcoa`) | 2500 | 16 | 51 game s (36 real s) | 25 game s (18 real s) | 10 game s (7 real s) | 5 game s (4 real s) | 3 game s (2 real s) |
| **Mine** (`eurgol`) | 2500 | 16 | 51 game s (36 real s) | 25 game s (18 real s) | 10 game s (7 real s) | 5 game s (4 real s) | 3 game s (2 real s) |
| **Mine** (`euriro`) | 2500 | 16 | 51 game s (36 real s) | 25 game s (18 real s) | 10 game s (7 real s) | 5 game s (4 real s) | 3 game s (2 real s) |
| **Market** (`eurmar`) | 4000 | 25 | 1.4 game min (1.0 real min) | 41 game s (29 real s) | 16 game s (12 real s) | 8 game s (6 real s) | 3 game s (2 real s) |
| **Mill** (`eurmil`) | 20000 | 10 | 6.8 game min (4.8 real min) | 3.4 game min (2.4 real min) | 1.4 game min (1.0 real min) | 41 game s (29 real s) | 41 game s (29 real s) |
| **Shipyard** (`eurpor`) | 50000 | 30 | 16.9 game min (12.1 real min) | 8.5 game min (6.0 real min) | 3.4 game min (2.4 real min) | 1.7 game min (1.2 real min) | 34 game s (24 real s) |
| **Gate** (`eursga`) | 32000 | 13 | 10.8 game min (7.7 real min) | 5.4 game min (3.9 real min) | 2.2 game min (1.5 real min) | 1.1 game min (0.8 real min) | 50 game s (36 real s) |
| **Storehouse** (`eursto`) | 10000 | 9 | 3.4 game min (2.4 real min) | 1.7 game min (1.2 real min) | 41 game s (29 real s) | 23 game s (16 real s) | 23 game s (16 real s) |
| **Wall** (`eurswa`) | 50000 | 4 | 16.9 game min (12.1 real min) | 8.5 game min (6.0 real min) | 4.2 game min (3.0 real min) | 4.2 game min (3.0 real min) | 4.2 game min (3.0 real min) |
| **Tower** (`eurtow`) | 20000 | 10 | 6.8 game min (4.8 real min) | 3.4 game min (2.4 real min) | 1.4 game min (1.0 real min) | 41 game s (29 real s) | 41 game s (29 real s) |
| **Gate** (`ukrwga`) | 1500 | 13 | 30 game s (22 real s) | 15 game s (11 real s) | 6 game s (4 real s) | 3 game s (2 real s) | 2 game s (2 real s) |
| **Palisade** (`ukrwwa`) | 1500 | 4 | 30 game s (22 real s) | 15 game s (11 real s) | 8 game s (5 real s) | 8 game s (5 real s) | 8 game s (5 real s) |
| **Academy** (`venaca`) | 63000 | 22 | 21.3 game min (15.2 real min) | 10.7 game min (7.6 real min) | 4.3 game min (3.0 real min) | 2.1 game min (1.5 real min) | 58 game s (42 real s) |
| **Artillery Depot** (`venart`) | 40000 | 20 | 13.5 game min (9.7 real min) | 6.8 game min (4.8 real min) | 2.7 game min (1.9 real min) | 1.4 game min (1.0 real min) | 41 game s (29 real s) |
| **Barracks, 18th century** (`venba2`) | 55000 | 19 | 18.6 game min (13.3 real min) | 9.3 game min (6.6 real min) | 3.7 game min (2.7 real min) | 1.9 game min (1.3 real min) | 59 game s (42 real s) |
| **Barracks, 17th century** (`venbar`) | 40000 | 23 | 13.5 game min (9.7 real min) | 6.8 game min (4.8 real min) | 2.7 game min (1.9 real min) | 1.4 game min (1.0 real min) | 35 game s (25 real s) |
| **Blacksmith** (`venbla`) | 5500 | 16 | 1.9 game min (1.3 real min) | 56 game s (40 real s) | 22 game s (16 real s) | 11 game s (8 real s) | 7 game s (5 real s) |
| **Town Hall** (`vencen`) | 5100 | 28 | 1.7 game min (1.2 real min) | 52 game s (37 real s) | 21 game s (15 real s) | 10 game s (7 real s) | 4 game s (3 real s) |
| **Diplomatic Center** (`vendip`) | 4500 | 18 | 1.5 game min (1.1 real min) | 46 game s (33 real s) | 18 game s (13 real s) | 9 game s (7 real s) | 5 game s (4 real s) |
| **Housing** (`venhou`) | 5000 | 10 | 1.7 game min (1.2 real min) | 51 game s (36 real s) | 20 game s (15 real s) | 10 game s (7 real s) | 10 game s (7 real s) |
| **Stable** (`vensta`) | 20000 | 19 | 6.8 game min (4.8 real min) | 3.4 game min (2.4 real min) | 1.4 game min (1.0 real min) | 41 game s (29 real s) | 21 game s (15 real s) |
| **Cathedral** (`ventem`) | 4200 | 30 | 1.4 game min (1.0 real min) | 43 game s (30 real s) | 17 game s (12 real s) | 9 game s (6 real s) | 3 game s (2 real s) |
