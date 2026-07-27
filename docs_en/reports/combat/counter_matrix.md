<a id="cossacks-3--counter-unit-matrix"></a>
<a id="кто-кого-побеждает"></a>
# One-on-One Unit Comparison

[← Tables and calculations](../README.md)

This is an approximate comparison of selected, representative units in a
one-on-one fight. It is calculated from their characteristics rather than
simulating the movement of entire formations.

<a id="метод"></a>
## Method
```text
effective_damage = max(1, attacker.damage − defender.protection[attacker.kind])
game_dps         = effective_damage / attacker.pause_sec       # melee: / attack0_sec from .aaf
real_dps_fast    = game_dps × 1.4
ttk_real_fast    = defender.hp / real_dps_fast
```
The damage formula comes from `_misc_DoDamage` [^1]. Results are converted
to real time at Fast speed (×1.4). The assumptions and limitations are
listed below.

<a id="время-победы-в-поединке"></a>
## Time to Win the Duel

Each cell shows how many real seconds at Fast speed **one** attacker needs
to defeat **one** defender. Protection against the attacker's weapon is
included; formation bonuses, movement, and range are not. An artillery
shell may strike several units in battle, but the table counts damage to
one target only.

**How to read the table:** lower values favor the attacker. `m̃` marks a
melee result whose attack rate comes from the unit's animation. `—` means
that the unit has no suitable weapon or health value.

| # | Attacker | D1 | D2 | D3 | D4 | D5 | D6 | D7 | D8 | D9 | D10 | D11 | D12 | D13 | D14 | D15 | D16 | D17 | D18 | D19 | D20 | D21 | D22 |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| A1 | Pikeman, 17th century | 6.0m̃ | 3.8m̃ | 2.9m̃ | 3.6m̃ | 3.1m̃ | 5.4m̃ | 3.6m̃ | 2.7m̃ | 1.7m̃ | 7.7m̃ | 3.6m̃ | 4.2m̃ | 5.0m̃ | 5.2m̃ | 9.6m̃ | 16.7m̃ | 16.7m̃ | 9.2m̃ | 24.1m̃ | 9.2m̃ | 376.7m̃ | 16.7m̃ |
| A2 | Pikeman, 17th century (Poland) | 4.8m̃ | 3.0m̃ | 2.3m̃ | 2.8m̃ | 2.5m̃ | 4.4m̃ | 2.8m̃ | 2.2m̃ | 1.3m̃ | 6.2m̃ | 2.8m̃ | 3.3m̃ | 4.0m̃ | 4.2m̃ | 7.7m̃ | 13.4m̃ | 13.4m̃ | 7.4m̃ | 19.3m̃ | 7.4m̃ | 301.3m̃ | 13.4m̃ |
| A3 | Musketeer, 17th century | 37.7 | 25.1 | 19.5 | 23.7 | 20.9 | 36.3 | 23.7 | 18.1 | 11.2 | 51.6 | 23.7 | 27.9 | 33.5 | 34.9 | 64.2 | 502.5 | 167.5 | 61.4 | 150.8 | 61.4 | 2512.5 | 111.7 |
| A4 | Strelets | 37.7 | 25.1 | 19.5 | 23.7 | 20.9 | 36.3 | 23.7 | 18.1 | 11.2 | 51.6 | 23.7 | 27.9 | 33.5 | 34.9 | 64.2 | 502.5 | 167.5 | 61.4 | 150.8 | 61.4 | 2512.5 | 111.7 |
| A5 | Chasseur | 23.9 | 19.1 | 14.9 | 18.0 | 15.9 | 27.6 | 18.0 | 13.8 | 8.5 | 39.2 | 18.0 | 21.2 | 25.5 | 26.5 | 48.8 | 127.3 | 90.9 | 46.7 | 95.5 | 46.7 | 1909.3 | 84.9 |
| A6 | Highlander | 26.8 | 20.1 | 15.6 | 19.0 | 16.7 | 29.0 | 19.0 | 14.5 | 8.9 | 41.3 | 19.0 | 22.3 | 26.8 | 27.9 | 51.3 | 178.6 | 107.1 | 49.1 | 107.1 | 49.1 | 2008.9 | 89.3 |
| A7 | Pandur | 23.2 | 17.7 | 13.8 | 16.8 | 14.8 | 25.6 | 16.8 | 12.8 | 7.9 | 36.5 | 16.8 | 19.7 | 23.6 | 24.6 | 45.3 | 143.6 | 91.4 | 43.4 | 92.8 | 43.4 | 1773.5 | 78.8 |
| A8 | Janissary | 37.7 | 25.1 | 19.5 | 23.7 | 20.9 | 36.3 | 23.7 | 18.1 | 11.2 | 51.6 | 23.7 | 27.9 | 33.5 | 34.9 | 64.2 | 502.5 | 167.5 | 61.4 | 150.8 | 61.4 | 2512.5 | 111.7 |
| A9 | Archer | 1.7 | 1.7 | 1.3 | 1.6 | 1.4 | 2.4 | 1.6 | 1.2 | 0.7 | 3.4 | 1.6 | 1.9 | 2.2 | 2.3 | 4.3 | 5.6 | 5.6 | 4.1 | 6.7 | 4.1 | 167.6 | 7.4 |
| A10 | Tatar | 2.2 | 2.2 | 1.7 | 2.0 | 1.8 | 3.1 | 2.0 | 1.6 | 1.0 | 4.4 | 2.0 | 2.4 | 2.9 | 3.0 | 5.5 | 7.2 | 7.2 | 5.3 | 8.6 | 5.3 | 215.4 | 9.6 |
| A11 | Pikeman, 18th century | 3.0m̃ | 2.0m̃ | 1.6m̃ | 1.9m̃ | 1.7m̃ | 2.9m̃ | 1.9m̃ | 1.5m̃ | 0.9m̃ | 4.1m̃ | 1.9m̃ | 2.2m̃ | 2.7m̃ | 2.8m̃ | 5.1m̃ | 8.6m̃ | 8.6m̃ | 4.9m̃ | 12.1m̃ | 4.9m̃ | 200.9m̃ | 8.9m̃ |
| A12 | Musketeer, 18th century | 25.1 | 18.8 | 14.7 | 17.8 | 15.7 | 27.2 | 17.8 | 13.6 | 8.4 | 38.7 | 17.8 | 20.9 | 25.1 | 26.2 | 48.2 | 167.5 | 100.5 | 46.1 | 100.5 | 46.1 | 1884.4 | 83.8 |
| A13 | Grenadier (Austria) | 1.4 | 1.4 | 1.1 | 1.3 | 1.1 | 2.0 | 1.3 | 1.0 | 0.6 | 2.8 | 1.3 | 1.5 | 1.8 | 1.9 | 3.5 | 4.6 | 4.6 | 3.3 | 5.5 | 3.3 | 136.8 | 6.1 |
| A14 | Grenadier (Prussia) | 1.4 | 1.4 | 1.1 | 1.3 | 1.1 | 2.0 | 1.3 | 1.0 | 0.6 | 2.8 | 1.3 | 1.5 | 1.8 | 1.9 | 3.5 | 4.6 | 4.6 | 3.3 | 5.5 | 3.3 | 136.8 | 6.1 |
| A15 | Hussar | 2.8m̃ | 2.3m̃ | 1.8m | 2.2m̃ | 2.0m̃ | 3.4m̃ | 2.2m̃ | 1.7m̃ | 1.0m̃ | 4.8m̃ | 2.2m̃ | 2.6m̃ | 3.1m̃ | 3.3m̃ | 6.0m̃ | 11.7m̃ | 15.6m̃ | 5.7m̃ | 22.5m̃ | 5.7m̃ | 234.4m̃ | 10.4m̃ |
| A16 | Cuirassier | 2.6m̃ | 2.0m̃ | 1.6m̃ | 1.9m̃ | 1.7m̃ | 2.9m̃ | 1.9m̃ | 1.5m̃ | 0.9m̃ | 4.1m̃ | 1.9m̃ | 2.2m̃ | 2.7m̃ | 2.8m̃ | 5.1m̃ | 7.8m | 7.8m | 4.9m̃ | 10.2m̃ | 4.9m̃ | 200.9m̃ | 8.9m̃ |
| A17 | Reiter | 2.3m̃ | 1.9m̃ | 1.5m̃ | 1.8m | 1.6m̃ | 2.7m̃ | 1.8m | 1.4m̃ | 0.8m̃ | 3.9m̃ | 1.8m | 2.1m̃ | 2.5m̃ | 2.6m̃ | 4.8m̃ | 7.2m̃ | 7.2m̃ | 4.6m̃ | 9.4m̃ | 4.6m̃ | 187.5m̃ | 8.3m̃ |
| A18 | Dragoon, 17th century | 32.8 | 24.1 | 18.7 | 22.7 | 20.1 | 34.8 | 22.7 | 17.4 | 10.7 | 49.5 | 22.7 | 26.8 | 32.1 | 33.5 | 61.6 | 240.9 | 133.8 | 58.9 | 131.4 | 58.9 | 2408.6 | 107.0 |
| A19 | Heavy Sipahi | 1.9m̃ | 1.6m̃ | 1.2m̃ | 1.5m̃ | 1.3m̃ | 2.3m̃ | 1.5m̃ | 1.2m̃ | 0.7m̃ | 3.3m̃ | 1.5m̃ | 1.8m | 2.1m̃ | 2.2m̃ | 4.1m̃ | 7.3m̃ | 8.9m̃ | 3.9m̃ | 12.1m̃ | 3.9m̃ | 160.7m̃ | 7.1m̃ |
| A20 | Don Cossack | 2.8m̃ | 2.2m̃ | 1.7m̃ | 2.0m̃ | 1.8m | 3.1m̃ | 2.0m̃ | 1.6m̃ | 1.0m̃ | 4.4m̃ | 2.0m̃ | 2.4m̃ | 2.9m̃ | 3.0m̃ | 5.5m̃ | 8.5m̃ | 8.5m̃ | 5.3m̃ | 11.2m̃ | 5.3m̃ | 216.3m̃ | 9.6m̃ |
| A21 | Cannon | 0.4 | 0.4 | 0.3 | 0.4 | 0.3 | 0.6 | 0.4 | 0.3 | 0.2 | 0.8 | 0.4 | 0.4 | 0.5 | 0.5 | 1.0 | 1.4 | 1.3 | 1.0 | 1.6 | 1.0 | 39.1 | 1.7 |
| A22 | Bombard | 2.5 | 2.5 | 2.0 | 2.4 | 2.1 | 3.6 | 2.4 | 1.8 | 1.1 | 5.2 | 2.4 | 2.8 | 3.3 | 3.5 | 6.4 | 8.4 | 8.4 | 6.1 | 10.0 | 6.1 | 251.0 | 11.2 |

**Legend** (D# = defender column = same unit as A# row):

| # | Unit | Internal ID · Nation | Health | Protection (pike / sword / bullet / grapeshot / arrow / cannonball) |
| ---: | --- | --- | ---: | --- |
| 1 | Pikeman, 17th century | `pikeman` · Austria | 90 | 3/2/4/210/6/40 |
| 2 | Pikeman, 17th century (Poland) | `pikemanpol` · Poland | 90 | 0/0/0/0/0/0 |
| 3 | Musketeer, 17th century | `musketeer` · France | 70 | 0/0/0/0/0/0 |
| 4 | Strelets | `strelet` · Russia | 85 | 0/0/0/0/0/0 |
| 5 | Chasseur | `chasseur` · France | 75 | 0/0/0/0/0/0 |
| 6 | Highlander | `highlander` · England | 130 | 0/0/0/0/0/0 |
| 7 | Pandur | `pandur` · Austria | 85 | 0/0/0/0/0/0 |
| 8 | Janissary | `jannisary` · Turkey | 65 | 0/0/0/0/0/0 |
| 9 | Archer | `archer` · Algeria | 40 | 0/0/0/0/0/0 |
| 10 | Tatar | `tatar` · Turkey | 185 | 0/0/0/0/0/0 |
| 11 | Pikeman, 18th century | `pikeman18` · Austria | 85 | 0/0/0/0/0/0 |
| 12 | Musketeer, 18th century | `musketeer18` · Austria | 100 | 0/0/0/0/0/0 |
| 13 | Grenadier (Austria) | `grenadier` · Austria | 120 | 0/0/0/0/0/0 |
| 14 | Grenadier (Prussia) | `grenadierpru` · Prussia | 125 | 0/0/0/0/0/0 |
| 15 | Hussar | `hussar` · Austria | 230 | 0/0/0/0/0/0 |
| 16 | Cuirassier | `cuirassier` · Austria | 300 | 2/4/10/160/5/80 |
| 17 | Reiter | `reiter` · Austria | 300 | 2/6/6/190/15/40 |
| 18 | Dragoon, 17th century | `dragoon` · Austria | 220 | 0/0/0/0/0/0 |
| 19 | Heavy Sipahi | `sipahi` · Turkey | 360 | 3/7/4/225/24/60 |
| 20 | Don Cossack | `cossackdon` · Russia | 220 | 0/0/0/0/0/0 |
| 21 | Cannon | `cannon` · Austria | 9000 | 0/0/0/0/0/0 |
| 22 | Bombard | `mortar` · Austria | 400 | 0/0/0/0/0/0 |

<a id="матрица-эффективного-dps-real-sec--fast"></a>
<a id="урон-в-секунду-по-каждому-защитнику"></a>
## Damage per Second against Each Defender

This matrix shows the real damage per second at Fast speed after the
defender's protection is applied. Melee attack rates come from each unit's
attack animation; where it is unavailable, the calculation uses the median
duration of 0.4688 game seconds. Since time to win equals health divided by
damage per second, this is the same comparison viewed from the attacker's
side. Values near 1 mean that protection absorbs almost all base damage.

| Attacker | D1 | D2 | D3 | D4 | D5 | D6 | D7 | D8 | D9 | D10 | D11 | D12 | D13 | D14 | D15 | D16 | D17 | D18 | D19 | D20 | D21 | D22 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| A1 · Pikeman, 17th century | 14.9m̃ | 23.9m | 23.9m | 23.9m | 23.9m | 23.9m | 23.9m | 23.9m | 23.9m | 23.9m | 23.9m | 23.9m | 23.9m | 23.9m | 23.9m | 17.9m | 17.9m | 23.9m | 14.9m̃ | 23.9m | 23.9m | 23.9m |
| A2 · Pikeman, 17th century (Poland) | 18.7m | 29.9m̃ | 29.9m̃ | 29.9m̃ | 29.9m̃ | 29.9m̃ | 29.9m̃ | 29.9m̃ | 29.9m̃ | 29.9m̃ | 29.9m̃ | 29.9m̃ | 29.9m̃ | 29.9m̃ | 29.9m̃ | 22.4m̃ | 22.4m̃ | 29.9m̃ | 18.7m | 29.9m̃ | 29.9m̃ | 29.9m̃ |
| A3 · Musketeer, 17th century | 2.4 | 3.6 | 3.6 | 3.6 | 3.6 | 3.6 | 3.6 | 3.6 | 3.6 | 3.6 | 3.6 | 3.6 | 3.6 | 3.6 | 3.6 | 0.6 | 1.8 | 3.6 | 2.4 | 3.6 | 3.6 | 3.6 |
| A4 · Strelets | 2.4 | 3.6 | 3.6 | 3.6 | 3.6 | 3.6 | 3.6 | 3.6 | 3.6 | 3.6 | 3.6 | 3.6 | 3.6 | 3.6 | 3.6 | 0.6 | 1.8 | 3.6 | 2.4 | 3.6 | 3.6 | 3.6 |
| A5 · Chasseur | 3.8 | 4.7 | 4.7 | 4.7 | 4.7 | 4.7 | 4.7 | 4.7 | 4.7 | 4.7 | 4.7 | 4.7 | 4.7 | 4.7 | 4.7 | 2.4 | 3.3 | 4.7 | 3.8 | 4.7 | 4.7 | 4.7 |
| A6 · Highlander | 3.4 | 4.5 | 4.5 | 4.5 | 4.5 | 4.5 | 4.5 | 4.5 | 4.5 | 4.5 | 4.5 | 4.5 | 4.5 | 4.5 | 4.5 | 1.7 | 2.8 | 4.5 | 3.4 | 4.5 | 4.5 | 4.5 |
| A7 · Pandur | 3.9 | 5.1 | 5.1 | 5.1 | 5.1 | 5.1 | 5.1 | 5.1 | 5.1 | 5.1 | 5.1 | 5.1 | 5.1 | 5.1 | 5.1 | 2.1 | 3.3 | 5.1 | 3.9 | 5.1 | 5.1 | 5.1 |
| A8 · Janissary | 2.4 | 3.6 | 3.6 | 3.6 | 3.6 | 3.6 | 3.6 | 3.6 | 3.6 | 3.6 | 3.6 | 3.6 | 3.6 | 3.6 | 3.6 | 0.6 | 1.8 | 3.6 | 2.4 | 3.6 | 3.6 | 3.6 |
| A9 · Archer | 53.7 | 53.7 | 53.7 | 53.7 | 53.7 | 53.7 | 53.7 | 53.7 | 53.7 | 53.7 | 53.7 | 53.7 | 53.7 | 53.7 | 53.7 | 53.7 | 53.7 | 53.7 | 53.7 | 53.7 | 53.7 | 53.7 |
| A10 · Tatar | 41.8 | 41.8 | 41.8 | 41.8 | 41.8 | 41.8 | 41.8 | 41.8 | 41.8 | 41.8 | 41.8 | 41.8 | 41.8 | 41.8 | 41.8 | 41.8 | 41.8 | 41.8 | 41.8 | 41.8 | 41.8 | 41.8 |
| A11 · Pikeman, 18th century | 29.9m̃ | 44.8m̃ | 44.8m̃ | 44.8m̃ | 44.8m̃ | 44.8m̃ | 44.8m̃ | 44.8m̃ | 44.8m̃ | 44.8m̃ | 44.8m̃ | 44.8m̃ | 44.8m̃ | 44.8m̃ | 44.8m̃ | 34.9m̃ | 34.9m̃ | 44.8m̃ | 29.9m̃ | 44.8m̃ | 44.8m̃ | 44.8m̃ |
| A12 · Musketeer, 18th century | 3.6 | 4.8 | 4.8 | 4.8 | 4.8 | 4.8 | 4.8 | 4.8 | 4.8 | 4.8 | 4.8 | 4.8 | 4.8 | 4.8 | 4.8 | 1.8 | 3.0 | 4.8 | 3.6 | 4.8 | 4.8 | 4.8 |
| A13 · Grenadier (Austria) | 65.8 | 65.8 | 65.8 | 65.8 | 65.8 | 65.8 | 65.8 | 65.8 | 65.8 | 65.8 | 65.8 | 65.8 | 65.8 | 65.8 | 65.8 | 65.8 | 65.8 | 65.8 | 65.8 | 65.8 | 65.8 | 65.8 |
| A14 · Grenadier (Prussia) | 65.8 | 65.8 | 65.8 | 65.8 | 65.8 | 65.8 | 65.8 | 65.8 | 65.8 | 65.8 | 65.8 | 65.8 | 65.8 | 65.8 | 65.8 | 65.8 | 65.8 | 65.8 | 65.8 | 65.8 | 65.8 | 65.8 |
| A15 · Hussar | 32.0m̃ | 38.4m̃ | 38.4m̃ | 38.4m̃ | 38.4m̃ | 38.4m̃ | 38.4m̃ | 38.4m̃ | 38.4m̃ | 38.4m̃ | 38.4m̃ | 38.4m̃ | 38.4m̃ | 38.4m̃ | 38.4m̃ | 25.6m̃ | 19.2m̃ | 38.4m̃ | 16.0m̃ | 38.4m̃ | 38.4m̃ | 38.4m̃ |
| A16 · Cuirassier | 35.2m̃ | 44.8m̃ | 44.8m̃ | 44.8m̃ | 44.8m̃ | 44.8m̃ | 44.8m̃ | 44.8m̃ | 44.8m̃ | 44.8m̃ | 44.8m̃ | 44.8m̃ | 44.8m̃ | 44.8m̃ | 44.8m̃ | 38.4m̃ | 38.4m̃ | 44.8m̃ | 35.2m̃ | 44.8m̃ | 44.8m̃ | 44.8m̃ |
| A17 · Reiter | 38.4m̃ | 48.0m̃ | 48.0m̃ | 48.0m̃ | 48.0m̃ | 48.0m̃ | 48.0m̃ | 48.0m̃ | 48.0m̃ | 48.0m̃ | 48.0m̃ | 48.0m̃ | 48.0m̃ | 48.0m̃ | 48.0m̃ | 41.6m̃ | 41.6m̃ | 48.0m̃ | 38.4m̃ | 48.0m̃ | 48.0m̃ | 48.0m̃ |
| A18 · Dragoon, 17th century | 2.7 | 3.7 | 3.7 | 3.7 | 3.7 | 3.7 | 3.7 | 3.7 | 3.7 | 3.7 | 3.7 | 3.7 | 3.7 | 3.7 | 3.7 | 1.2 | 2.2 | 3.7 | 2.7 | 3.7 | 3.7 | 3.7 |
| A19 · Heavy Sipahi | 48.5m̃ | 56.0m̃ | 56.0m̃ | 56.0m̃ | 56.0m̃ | 56.0m̃ | 56.0m̃ | 56.0m̃ | 56.0m̃ | 56.0m̃ | 56.0m̃ | 56.0m̃ | 56.0m̃ | 56.0m̃ | 56.0m̃ | 41.1m̃ | 33.6m̃ | 56.0m̃ | 29.9m̃ | 56.0m̃ | 56.0m̃ | 56.0m̃ |
| A20 · Don Cossack | 32.0m̃ | 41.6m̃ | 41.6m̃ | 41.6m̃ | 41.6m̃ | 41.6m̃ | 41.6m̃ | 41.6m̃ | 41.6m̃ | 41.6m̃ | 41.6m̃ | 41.6m̃ | 41.6m̃ | 41.6m̃ | 41.6m̃ | 35.2m̃ | 35.2m̃ | 41.6m̃ | 32.0m̃ | 41.6m̃ | 41.6m̃ | 41.6m̃ |
| A21 · Cannon | 225.2 | 230.3 | 230.3 | 230.3 | 230.3 | 230.3 | 230.3 | 230.3 | 230.3 | 230.3 | 230.3 | 230.3 | 230.3 | 230.3 | 230.3 | 220.1 | 225.2 | 230.3 | 222.7 | 230.3 | 230.3 | 230.3 |
| A22 · Bombard | 35.9 | 35.9 | 35.9 | 35.9 | 35.9 | 35.9 | 35.9 | 35.9 | 35.9 | 35.9 | 35.9 | 35.9 | 35.9 | 35.9 | 35.9 | 35.9 | 35.9 | 35.9 | 35.9 | 35.9 | 35.9 | 35.9 |

<a id="оговорки"></a>
## Limitations

- **Formation bonuses** are omitted. An aggressive formation can add up to
  50% damage, while a defensive formation can add up to 50 protection.
- **Range** is omitted. Ranged infantry often fires before cavalry can
  close the distance, so a real engagement depends on more than the values
  in these tables.
- **Movement** is not simulated. A heavy cavalryman may reach a Musketeer
  during the reload interval and completely change the result.
- **Melee attack rate** comes from each unit's `attack0` animation, normally
  11–33 frames. If that animation is unavailable, the calculation uses the
  median of 15 frames, or 0.4688 game seconds. These results are marked
  `m̃`.
- **Area damage** is applied to one target only. In a dense formation, a
  cannonball or Bombard blast may hit several units.
- **Minimum damage** is one point even when protection exceeds base damage
  [^1]. Armor therefore cannot make a unit invulnerable, although a duel
  may last hundreds of seconds.
- **18th-century units** require the advance to the new century and the
  appropriate building. They are included for comparison even though they
  appear only after substantial economic development.


<a id="источники"></a>
## Sources

All links are relative to `data/scripts/` in the Cossacks 3 installation.

[^1]: `_misc_DoDamage` — damage application —
      `lib/miscext2.script:380, 434`.
