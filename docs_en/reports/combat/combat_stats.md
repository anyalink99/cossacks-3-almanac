<a id="боевые-характеристики"></a>
# Combat Statistics

[← Tables and calculations](../README.md)

<a id="формула-урона"></a>
## Damage formula

The game subtracts armor and protection against the relevant weapon type
from base damage [^1]. The result is never lower than one:
```
applied_damage = max(1, base_damage + squad_bonus - target.protection[weapon_kind])
target.hp     -= applied_damage
```
At Fast speed, real damage per second is 1.4 times the damage per game
second.

<a id="1-сводная-таблица-боевых-юнитов"></a>
## §1. Summary table of combat units

Each row represents one unique set of characteristics. **Nations** shows
where that variant is available; `all 21` means every nation. National
variants with different values occupy separate rows.

The table includes health, internal speed, primary weapon, damage per game
second, real damage per second at Fast speed, weapon-specific protection,
and general armor. If a unit has several weapons, the one with the
**highest damage-to-reload ratio** is shown.

| Unit | Nations | Role | Health | Internal speed | Primary weapon | Damage/game s | Damage/real s at Fast | Protection |
| --- | --- | --- | ---: | ---: | --- | ---: | ---: | --- |
| **Tatar** (`tatar`) | **Turkey** (`tur`) | Archer | 185 | 32 | 140d / 4.69s / 20.63t [Fire Arrow] | 29.85 | 41.79 | — |
| **Bow Clansman** (`archersco`) | **Scotland** (`sco`) | Archer | 150 | 32 | 150d / 4.38s / 18.75t [Fire Arrow] | 34.25 | 47.95 | — |
| **Turkish archer** (`archertur`) | **Turkey** (`tur`) | Archer | 65 | 32 | 150d / 4.38s / 16.88t [Fire Arrow] | 34.25 | 47.95 | — |
| **Archer** (`archer`) | **Algeria** (`alg`) | Archer | 40 | 32 | 150d / 3.91s / 11.25t [Fire Arrow] | 38.36 | 53.7 | — |
| **Archer (mercenary)** (`archerdip`) | all 21 | Archer | 20 | 32 | 100d / 0.78s / 14.06t [Fire Arrow] | 128.21 | 179.49 | — |
| **Turkish archer (mercenary)** (`archerturdip`) | all 21 | Archer | 20 | 32 | 100d / 0.78s / 14.06t [Fire Arrow] | 128.21 | 179.49 | — |
| **Cannon** (`cannon`) | all 21 | Artillery | 9000 | 20 | 1800d / 10.94s / 40.5t [Cannonball] | 164.53 | 230.34 | General armor=75 |
| **Frame gun** (`framegun`) | **Scotland** (`sco`) | Artillery | 3000 | 20 | 500d / 2.81s / 33.75t [Cannonball] | 177.94 | 249.12 | General armor=50 |
| **Grenadier** (`grenadierbav`) | **Bavaria** (`bav`) | Grenadier | 125 | 32 | 110d / 2.34s / 9.38t [Explosive shell] | 47.01 | 65.81 | — |
| **Grenadier** (`grenadierden`) | **Denmark** (`den`) | Grenadier | 125 | 32 | 110d / 2.34s / 9.38t [Explosive shell] | 47.01 | 65.81 | — |
| **Grenadier** (`grenadierhun`) | **Hungary** (`hun`) | Grenadier | 125 | 32 | 110d / 2.81s / 11.25t [Explosive shell] | 39.15 | 54.81 | — |
| **Grenadier** (`grenadierpru`) | **Prussia** (`pru`) | Grenadier | 125 | 32 | 110d / 2.34s / 9.38t [Explosive shell] | 47.01 | 65.81 | — |
| **Grenadier** (`grenadier`) | **Austria** (`aus`) | Grenadier | 120 | 32 | 110d / 2.34s / 9.38t [Explosive shell] | 47.01 | 65.81 | — |
| **Grenadier** (`grenadiersax`) | **Saxony** (`sax`) | Grenadier | 100 | 32 | 110d / 2.34s / 9.38t [Explosive shell] | 47.01 | 65.81 | — |
| **Grenadier (mercenary)** (`grenadierdip`) | all 21 | Grenadier | 30 | 32 | 200d / 3.12s / 7.5t [Explosive shell] | 64.1 | 89.74 | — |
| **Vityaz** (`vityaz`) | **Russia** (`rus`) | Heavy Cavalry | 380 | 56 | 14d / 0 (melee) / 1.22t [Pike] | — | — | Pike=2, Sword=4, Firearm=3, Grapeshot=160, Arrow=17, Cannonball=40 |
| **Heavy Sipahi** (`sipahi`) | **Turkey** (`tur`) | Heavy Cavalry | 360 | 56 | 15d / 0 (melee) / 1.22t [Sword] | — | — | Pike=3, Sword=7, Firearm=4, Grapeshot=225, Arrow=24, Cannonball=60 |
| **Cavalry Guard** (`guardcavalrysax`) | **Saxony** (`sax`) | Heavy Cavalry | 320 | 56 | 15d / 0 (melee) / 1.22t [Pike] | — | — | Pike=2, Sword=5, Firearm=9, Grapeshot=150, Arrow=9, Cannonball=70 |
| **Hetman** (`hetman`) | **Ukraine** (`ukr`) | Heavy Cavalry | 320 | 56 | 70d / 0 (melee) / 1.22t [Pike] | — | — | Sword=1, Firearm=3, Grapeshot=75, Arrow=3, Cannonball=15 |
| **Lancer** (`lancersco`) | **Scotland** (`sco`) | Heavy Cavalry | 320 | 56 | 11d / 0 (melee) / 1.88t [Pike] | — | — | — |
| **Cuirassier** (`cuirassier`) | **Austria** (`aus`) | Heavy Cavalry | 300 | 56 | 14d / 0 (melee) / 1.22t [Pike] | — | — | Pike=2, Sword=4, Firearm=10, Grapeshot=160, Arrow=5, Cannonball=80 |
| **Reiter** (`reiter`) | **Austria** (`aus`) | Heavy Cavalry | 300 | 56 | 15d / 0 (melee) / 1.22t [Pike] | — | — | Pike=2, Sword=6, Firearm=6, Grapeshot=190, Arrow=15, Cannonball=40 |
| **Swedish Reiter** (`reiterswe`) | **Sweden** (`swe`) | Heavy Cavalry | 300 | 56 | 14d / 0 (melee) / 1.22t [Pike] | — | — | Pike=2, Sword=3, Firearm=7, Grapeshot=140, Arrow=7, Cannonball=35 |
| **Mameluke** (`mameluke`) | **Algeria** (`alg`) | Heavy Cavalry | 280 | 56 | 16d / 0 (melee) / 1.88t [Pike] | — | — | Pike=1, Sword=3, Firearm=1, Grapeshot=75, Arrow=8 |
| **Register Cossack** (`cossackregister`) | **Ukraine** (`ukr`) | Heavy Cavalry | 250 | 56 | 12d / 0 (melee) / 1.88t [Pike] | — | — | — |
| **Light Sipahi** (`spakh`) | **Turkey** (`tur`) | Heavy Cavalry | 230 | 56 | 15d / 0 (melee) / 1.88t [Pike] | — | — | Sword=1, Grapeshot=10, Arrow=2 |
| **Don Cossack** (`cossackdon`) | **Russia** (`rus`) | Heavy Cavalry | 220 | 56 | 13d / 0 (melee) / 1.88t [Pike] | — | — | — |
| **Light Reiter** (`reiterpol`) | **Poland** (`pol`) | Heavy Cavalry | 190 | 56 | 9d / 0 (melee) / 1.22t [Sword] | — | — | — |
| **Raider** (`raidersco`) | **Scotland** (`sco`) | Light Cavalry | 280 | 96 | 11d / 0 (melee) / 1.22t [Sword] | — | — | — |
| **Mounted Jaeger** (`hussarswi`) | **Switzerland** (`swi`) | Light Cavalry | 265 | 96 | 14d / 0 (melee) / 1.22t [Sword] | — | — | — |
| **Croat** (`croat`) | **Austria** (`aus`) | Light Cavalry | 260 | 96 | 9d / 0 (melee) / 1.22t [Sword] | — | — | — |
| **Sich Cossack** (`cossacksich`) | **Ukraine** (`ukr`) | Light Cavalry | 250 | 96 | 13d / 0 (melee) / 1.22t [Sword] | — | — | — |
| **Hussar** (`hussarhun`) | **Hungary** (`hun`) | Light Cavalry | 250 | 96 | 10d / 0 (melee) / 1.22t [Sword] | — | — | — |
| **Hakkapeliitta** (`hackapell`) | **Sweden** (`swe`) | Light Cavalry | 245 | 96 | 12d / 0 (melee) / 1.22t [Pike] | — | — | — |
| **Hussar** (`hussarpru`) | **Prussia** (`pru`) | Light Cavalry | 240 | 96 | 9d / 0 (melee) / 1.22t [Sword] | — | — | — |
| **Hussar** (`hussar`) | **Austria** (`aus`) | Light Cavalry | 230 | 96 | 12d / 0 (melee) / 1.22t [Sword] | — | — | — |
| **Winged Hussar** (`wingedhussar`) | **Poland** (`pol`) | Light Cavalry | 225 | 96 | 14d / 0 (melee) / 1.88t [Pike] | — | — | Pike=1, Sword=2, Firearm=5, Grapeshot=160, Arrow=10, Cannonball=30 |
| **Sich Cossack (mercenary)** (`cossacksichdip`) | all 21 | Light Cavalry | 150 | 96 | 8d / 0 (melee) / 1.22t [Sword] | — | — | — |
| **Sword Clansman** (`swordsmansco`) | **Scotland** (`sco`) | Light Infantry | 180 | 32 | 10d / 0 (melee) / 1.13t [Sword] | — | — | Pike=1, Sword=2, Firearm=2, Grapeshot=110, Arrow=6, Cannonball=10 |
| **Bagpiper** (`bagpiper`) | **England** (`eng`) | Light Infantry | 150 | 32 | — | — | — | — |
| **Officer** (`officersco`) | **Scotland** (`sco`) | Light Infantry | 150 | 32 | 40d / 0 (melee) / 1.22t [Pike] | — | — | — |
| **Officer, 17th century** (`officer`) | **Austria** (`aus`) | Light Infantry | 125 | 32 | 30d / 0 (melee) / 1.22t [Pike] | — | — | Pike=2, Sword=2, Firearm=5, Grapeshot=200, Arrow=10, Cannonball=30 |
| **Officer, 18th century** (`officer18`) | **Austria** (`aus`) | Light Infantry | 125 | 32 | 50d / 0 (melee) / 1.22t [Pike] | — | — | — |
| **Commander** (`officerrus`) | **Russia** (`rus`) | Light Infantry | 125 | 32 | 40d / 0 (melee) / 1.22t [Pike] | — | — | — |
| **Officer** (`officertur`) | **Algeria** (`alg`) | Light Infantry | 125 | 32 | 30d / 0 (melee) / 1.22t [Pike] | — | — | — |
| **Pikeman, 18th century** (`pikeman18swe`) | **Sweden** (`swe`) | Light Infantry | 110 | 32 | 11d / 0 (melee) / 1.88t [Pike] | — | — | — |
| **Drummer, 18th century** (`drummer18`) | **Austria** (`aus`) | Light Infantry | 100 | 32 | — | — | — | — |
| **Drummer, 17th century** (`drummerrus`) | **Russia** (`rus`) | Light Infantry | 100 | 32 | — | — | — | — |
| **Pikeman, 17th century** (`pikeman`) | **Spain** (`spa`) | Light Infantry | 100 | 32 | 10d / 0 (melee) / 1.88t [Pike] | — | — | Pike=3, Sword=4, Firearm=6, Grapeshot=240, Arrow=12, Cannonball=50 |
| **Pikeman, 17th century** (`pikemanpor`) | **Portugal** (`por`) | Light Infantry | 100 | 32 | 9d / 0 (melee) / 1.88t [Pike] | — | — | Sword=1, Firearm=1, Grapeshot=25, Arrow=4 |
| **Covenanter pikeman** (`pikemansco`) | **Scotland** (`sco`) | Light Infantry | 100 | 32 | 9d / 0 (melee) / 1.88t [Pike] | — | — | — |
| **Coselete** (`pikemanspa`) | **Spain** (`spa`) | Light Infantry | 100 | 32 | 10d / 0 (melee) / 1.88t [Pike] | — | — | Pike=3, Sword=4, Firearm=6, Grapeshot=240, Arrow=12, Cannonball=50 |
| **Priest** (`priest`) | **Austria** (`aus`) | Light Infantry | 100 | 32 | — | — | — | — |
| **Roundshier** (`roundshier`) | **Austria** (`aus`) | Light Infantry | 100 | 32 | 6d / 0 (melee) / 1.13t [Sword] | — | — | Pike=3, Sword=3, Firearm=7, Grapeshot=225, Arrow=16, Cannonball=80 |
| **Ottoman Pikeman** (`pikemantur`) | **Algeria** (`alg`) | Light Infantry | 95 | 32 | 9d / 0 (melee) / 2.06t [Pike] | — | — | — |
| **Padre** (`padre`) | **Piedmont** (`pie`) | Light Infantry | 90 | 32 | — | — | — | — |
| **Pikeman, 17th century** (`pikeman`) | **Austria** (`aus`) | Light Infantry | 90 | 32 | 8d / 0 (melee) / 1.88t [Pike] | — | — | Pike=3, Sword=2, Firearm=4, Grapeshot=210, Arrow=6, Cannonball=40 |
| **Pikeman, 17th century** (`pikemanpol`) | **Poland** (`pol`) | Light Infantry | 90 | 32 | 8d / 0 (melee) / 2.06t [Pike] | — | — | — |
| **Pikeman, 17th century** (`pikemanswi`) | **Switzerland** (`swi`) | Light Infantry | 90 | 32 | 10d / 0 (melee) / 1.88t [Pike] | — | — | Pike=3, Sword=3, Firearm=6, Grapeshot=220, Arrow=6, Cannonball=45 |
| **Pikeman, 18th century** (`pikeman18`) | **Austria** (`aus`) | Light Infantry | 85 | 32 | 9d / 0 (melee) / 1.88t [Pike] | — | — | — |
| **Spearman** (`pikemanrus`) | **Russia** (`rus`) | Light Infantry | 85 | 32 | 8d / 0 (melee) / 1.69t [Pike] | — | — | Pike=2, Sword=1, Firearm=4, Grapeshot=140, Arrow=4, Cannonball=25 |
| **Drummer, 17th century** (`drummer`) | **Austria** (`aus`) | Light Infantry | 75 | 32 | — | — | — | — |
| **Mullah** (`mullah`) | **Algeria** (`alg`) | Light Infantry | 75 | 32 | — | — | — | — |
| **Pope** (`pope`) | **Russia** (`rus`) | Light Infantry | 75 | 32 | — | — | — | — |
| **Roundshier (mercenary)** (`roundshierdip`) | all 21 | Light Infantry | 75 | 32 | 6d / 0 (melee) / 1.13t [Sword] | — | — | Pike=5, Sword=3, Firearm=8, Grapeshot=225, Arrow=17, Cannonball=80 |
| **Light Infantryman** (`lightinfantry`) | **Algeria** (`alg`) | Light Infantry | 55 | 32 | 5d / 0 (melee) / 0.94t [Sword] | — | — | — |
| **Drummer, 17th century** (`drummertur`) | **Algeria** (`alg`) | Light Infantry | 50 | 32 | — | — | — | — |
| **Light Infantryman (mercenary)** (`lightinfantrydip`) | all 21 | Light Infantry | 50 | 32 | 16d / 0 (melee) / 0.94t [Sword] | — | — | — |
| **Howitzer** (`howitzer`) | all 21 | Artillery | 3000 | 20 | 4000d / 18.75s / 26.25t [Cannonball] | 213.33 | 298.66 | General armor=75 |
| **Dragoon, 18th century** (`dragoon18net`) | **Netherlands** (`net`) | Mounted Ranged Unit | 320 | 56 | 17d / 5.0s / 15.94t [Firearm] | 3.4 | 4.76 | — |
| **King's Musketeer** (`kingmusketeer`) | **France** (`fra`) | Mounted Ranged Unit | 280 | 56 | 43d / 6.88s / 13.13t [Firearm] | 6.25 | 8.75 | — |
| **Dragoon, 18th century** (`dragoon18`) | **Austria** (`aus`) | Mounted Ranged Unit | 225 | 56 | 19d / 5.31s / 16.88t [Firearm] | 3.58 | 5.01 | — |
| **Dragoon, 17th century** (`dragoon`) | **Austria** (`aus`) | Mounted Ranged Unit | 220 | 56 | 15d / 5.62s / 15.0t [Firearm] | 2.67 | 3.74 | — |
| **Dragoon, 18th century** (`dragoon18pie`) | **Piedmont** (`pie`) | Mounted Ranged Unit | 200 | 56 | 19d / 5.0s / 16.88t [Firearm] | 3.8 | 5.32 | — |
| **Pospolite ruszenie** (`dragoonpol`) | **Poland** (`pol`) | Mounted Ranged Unit | 185 | 56 | 13d / 5.0s / 15.94t [Firearm] | 2.6 | 3.64 | — |
| **Light cavalry** (`lightcavalry`) | **Hungary** (`hun`) | Mounted Ranged Unit | 175 | 56 | 14d / 5.31s / 18.75t [Firearm] | 2.64 | 3.7 | — |
| **Dragoon, 18th century** (`dragoon18fra`) | **France** (`fra`) | Mounted Ranged Unit | 140 | 56 | 10d / 4.69s / 15.0t [Firearm] | 2.13 | 2.98 | — |
| **Multi-barrelled Cannon** (`multicannon`) | **Austria** (`aus`) | Artillery | 2000 | 16 | 500d / 1.88s / 13.13t [Grapeshot] | 265.96 | 372.34 | General armor=50 |
| **Highlander** (`highlander`) | **England** (`eng`) | Ranged Infantry | 130 | 32 | 16d / 5.0s / 15.94t [Firearm] | 3.2 | 4.48 | — |
| **Dragoon, 18th century (mercenary)** (`dragoon18dip`) | all 21 | Ranged Infantry | 100 | 56 | 18d / 2.25s / 15.0t [Firearm] | 8.0 | 11.2 | — |
| **Light cavalry (mercenary)** (`lightcavalrydip`) | all 21 | Ranged Infantry | 100 | 56 | 18d / 2.25s / 15.0t [Firearm] | 8.0 | 11.2 | — |
| **Musketeer, 18th century** (`musketeer18`) | **Austria** (`aus`) | Ranged Infantry | 100 | 32 | 16d / 4.69s / 16.88t [Firearm] | 3.41 | 4.77 | — |
| **Musketeer, 18th century** (`musketeer18bav`) | **Bavaria** (`bav`) | Ranged Infantry | 100 | 32 | 22d / 5.94s / 17.81t [Firearm] | 3.7 | 5.18 | — |
| **Musketeer, 18th century** (`musketeer18den`) | **Denmark** (`den`) | Ranged Infantry | 100 | 32 | 29d / 5.94s / 16.88t [Firearm] | 4.88 | 6.83 | — |
| **Musketeer, 18th century** (`musketeer18pru`) | **Prussia** (`pru`) | Ranged Infantry | 100 | 32 | 22d / 4.69s / 17.81t [Firearm] | 4.69 | 6.57 | — |
| **Musketeer, 18th century** (`musketeer18sax`) | **Saxony** (`sax`) | Ranged Infantry | 90 | 32 | 19d / 4.38s / 16.88t [Firearm] | 4.34 | 6.08 | — |
| **Covenanter musketeer** (`musketeersco`) | **Scotland** (`sco`) | Ranged Infantry | 90 | 32 | 12d / 4.69s / 15.94t [Firearm] | 2.56 | 3.58 | — |
| **Musketeer, 17th century** (`musketeerspa`) | **Spain** (`spa`) | Ranged Infantry | 85 | 32 | 15d / 5.94s / 15.94t [Firearm] | 2.53 | 3.54 | Pike=3, Sword=2, Firearm=5, Grapeshot=210, Arrow=7, Cannonball=40 |
| **Pandur** (`pandur`) | **Austria** (`aus`) | Ranged Infantry | 85 | 32 | 17d / 4.69s / 16.88t [Firearm] | 3.62 | 5.07 | — |
| **Serdiuk** (`serdiuk`) | **Ukraine** (`ukr`) | Ranged Infantry | 85 | 32 | 12d / 4.06s / 16.88t [Firearm] | 2.96 | 4.14 | — |
| **Strelets** (`strelet`) | **Russia** (`rus`) | Ranged Infantry | 85 | 32 | 12d / 4.69s / 13.13t [Firearm] | 2.56 | 3.58 | — |
| **Chasseur** (`chasseur`) | **France** (`fra`) | Ranged Infantry | 75 | 32 | 20d / 5.94s / 19.69t [Firearm] | 3.37 | 4.72 | — |
| **Szekely** (`pandurhun`) | **Hungary** (`hun`) | Ranged Infantry | 75 | 32 | 19d / 5.0s / 18.75t [Firearm] | 3.8 | 5.32 | — |
| **Musketeer, 17th century** (`musketeer`) | **Bavaria** (`bav`) | Ranged Infantry | 70 | 32 | 12d / 4.69s / 15.0t [Firearm] | 2.56 | 3.58 | — |
| **Musketeer, 17th century** (`musketeerpol`) | **Poland** (`pol`) | Ranged Infantry | 70 | 32 | 9d / 3.12s / 13.13t [Firearm] | 2.88 | 4.03 | — |
| **Jaeger** (`jagerswi`) | **Switzerland** (`swi`) | Ranged Infantry | 65 | 32 | 20d / 6.88s / 22.5t [Firearm] | 2.91 | 4.07 | — |
| **Janissary** (`jannisary`) | **Turkey** (`tur`) | Ranged Infantry | 65 | 32 | 12d / 4.69s / 15.94t [Firearm] | 2.56 | 3.58 | — |
| **Musketeer, 17th century** (`musketeernet`) | **Netherlands** (`net`) | Ranged Infantry | 65 | 32 | 10d / 3.75s / 15.0t [Firearm] | 2.67 | 3.74 | — |
| **Hajduk** (`gauduk`) | **Hungary** (`hun`) | Ranged Infantry | 60 | 32 | 9d/3.12s/14.06t [Firearm] | 2.88 | 4.03 | — |
| **Musketeer, 17th century** (`musketeeraus`) | **Austria** (`aus`) | Ranged Infantry | 55 | 32 | 12d / 5.0s / 15.0t [Firearm] | 2.4 | 3.36 | Pike=2, Sword=2, Firearm=5, Grapeshot=165, Arrow=5, Cannonball=35 |
| **Volunteer** (`jagerpor`) | **Portugal** (`por`) | Ranged Infantry | 50 | 32 | 10d / 5.94s / 15.0t [Firearm] | 1.68 | 2.35 | — |
| **Bombard** (`mortar`) | all 21 | Artillery | 400 | 24 | 200d / 7.81s / 48.75t [Explosive shell] | 25.61 | 35.85 | General armor=25 |

<a id="2-рейтинг-dps--боевые-юниты"></a>
<a id="2-рейтинг-урона-в-секунду"></a>
## §2. Damage-per-Second Ranking

This ranking includes combat units with ranged weapons. Melee attacks are
excluded because their rate is determined by the attack animation. The
real-time value at Fast speed is 1.4 times the game-time value.

| # | Unit | Nations | Role | Health | Weapon type | Damage | Reload, game s | Range, cells | Damage/game s | Damage/real s at Fast |
| ---: | --- | --- | --- | ---: | --- | ---: | ---: | ---: | ---: | ---: |
| 1 | **Multi-barrelled Cannon** (`multicannon`) | **Austria** (`aus`) | Multi-barrelled Cannon | 2000 | canister | 500 | 1.88 | 13.13 | 265.96 | 372.34 |
| 2 | **Howitzer** (`howitzer`) | all 21 | Mortar | 3000 | Cannonball | 4000 | 18.75 | 26.25 | 213.33 | 298.66 |
| 3 | **Frame gun** (`framegun`) | **Scotland** (`sco`) | Artillery | 3000 | Cannonball | 500 | 2.81 | 33.75 | 177.94 | 249.12 |
| 4 | **Cannon** (`cannon`) | all 21 | Artillery | 9000 | Cannonball | 1800 | 10.94 | 40.5 | 164.53 | 230.34 |
| 5 | **Archer (mercenary)** (`archerdip`) | all 21 | Archer | 20 | Fire Arrow | 100 | 0.78 | 14.06 | 128.21 | 179.49 |
| 6 | **Turkish archer (mercenary)** (`archerturdip`) | all 21 | Archer | 20 | Fire Arrow | 100 | 0.78 | 14.06 | 128.21 | 179.49 |
| 7 | **Grenadier (mercenary)** (`grenadierdip`) | all 21 | Grenadier | 30 | Explosive shell | 200 | 3.12 | 7.5 | 64.1 | 89.74 |
| 8 | **Grenadier** (`grenadier`) | **Austria** (`aus`) | Grenadier | 120 | Explosive shell | 110 | 2.34 | 9.38 | 47.01 | 65.81 |
| 9 | **Grenadier** (`grenadierpru`) | **Prussia** (`pru`) | Grenadier | 125 | Explosive shell | 110 | 2.34 | 9.38 | 47.01 | 65.81 |
| 10 | **Grenadier** (`grenadierden`) | **Denmark** (`den`) | Grenadier | 125 | Explosive shell | 110 | 2.34 | 9.38 | 47.01 | 65.81 |
| 11 | **Grenadier** (`grenadiersax`) | **Saxony** (`sax`) | Grenadier | 100 | Explosive shell | 110 | 2.34 | 9.38 | 47.01 | 65.81 |
| 12 | **Grenadier** (`grenadierbav`) | **Bavaria** (`bav`) | Grenadier | 125 | Explosive shell | 110 | 2.34 | 9.38 | 47.01 | 65.81 |
| 13 | **Grenadier** (`grenadierhun`) | **Hungary** (`hun`) | Grenadier | 125 | Explosive shell | 110 | 2.81 | 11.25 | 39.15 | 54.81 |
| 14 | **Archer** (`archer`) | **Algeria** (`alg`) | Archer | 40 | Fire Arrow | 150 | 3.91 | 11.25 | 38.36 | 53.7 |
| 15 | **Turkish archer** (`archertur`) | **Turkey** (`tur`) | Archer | 65 | Fire Arrow | 150 | 4.38 | 16.88 | 34.25 | 47.95 |
| 16 | **Bow Clansman** (`archersco`) | **Scotland** (`sco`) | Archer | 150 | Fire Arrow | 150 | 4.38 | 18.75 | 34.25 | 47.95 |
| 17 | **Tatar** (`tatar`) | **Turkey** (`tur`) | Archer | 185 | Fire Arrow | 140 | 4.69 | 20.63 | 29.85 | 41.79 |
| 18 | **Bombard** (`mortar`) | all 21 | Artillery | 400 | Explosive shell | 200 | 7.81 | 48.75 | 25.61 | 35.85 |
| 19 | **Dragoon, 18th century (mercenary)** (`dragoon18dip`) | all 21 | Ranged Infantry | 100 | Firearm | 18 | 2.25 | 15.0 | 8.0 | 11.2 |
| 20 | **Light cavalry (mercenary)** (`lightcavalrydip`) | all 21 | Ranged Infantry | 100 | Firearm | 18 | 2.25 | 15.0 | 8.0 | 11.2 |
| 21 | **King's Musketeer** (`kingmusketeer`) | **France** (`fra`) | Mounted Ranged Unit | 280 | Firearm | 43 | 6.88 | 13.13 | 6.25 | 8.75 |
| 22 | **Musketeer, 18th century** (`musketeer18den`) | **Denmark** (`den`) | Ranged Infantry | 100 | Firearm | 29 | 5.94 | 16.88 | 4.88 | 6.83 |
| 23 | **Musketeer, 18th century** (`musketeer18pru`) | **Prussia** (`pru`) | Ranged Infantry | 100 | Firearm | 22 | 4.69 | 17.81 | 4.69 | 6.57 |
| 24 | **Musketeer, 18th century** (`musketeer18sax`) | **Saxony** (`sax`) | Ranged Infantry | 90 | Firearm | 19 | 4.38 | 16.88 | 4.34 | 6.08 |
| 25 | **Dragoon, 18th century** (`dragoon18pie`) | **Piedmont** (`pie`) | Mounted Ranged Unit | 200 | Firearm | 19 | 5.0 | 16.88 | 3.8 | 5.32 |
| 26 | **Szekely** (`pandurhun`) | **Hungary** (`hun`) | Ranged Infantry | 75 | Firearm | 19 | 5.0 | 18.75 | 3.8 | 5.32 |
| 27 | **Musketeer, 18th century** (`musketeer18bav`) | **Bavaria** (`bav`) | Ranged Infantry | 100 | Firearm | 22 | 5.94 | 17.81 | 3.7 | 5.18 |
| 28 | **Pandur** (`pandur`) | **Austria** (`aus`) | Ranged Infantry | 85 | Firearm | 17 | 4.69 | 16.88 | 3.62 | 5.07 |
| 29 | **Dragoon, 18th century** (`dragoon18`) | **Austria** (`aus`) | Mounted Ranged Unit | 225 | Firearm | 19 | 5.31 | 16.88 | 3.58 | 5.01 |
| 30 | **Musketeer, 18th century** (`musketeer18`) | **Austria** (`aus`) | Ranged Infantry | 100 | Firearm | 16 | 4.69 | 16.88 | 3.41 | 4.77 |
| 31 | **Dragoon, 18th century** (`dragoon18net`) | **Netherlands** (`net`) | Mounted Ranged Unit | 320 | Firearm | 17 | 5.0 | 15.94 | 3.4 | 4.76 |
| 32 | **Chasseur** (`chasseur`) | **France** (`fra`) | Ranged Infantry | 75 | Firearm | 20 | 5.94 | 19.69 | 3.37 | 4.72 |
| 33 | **Highlander** (`highlander`) | **England** (`eng`) | Ranged Infantry | 130 | Firearm | 16 | 5.0 | 15.94 | 3.2 | 4.48 |
| 34 | **Serdiuk** (`serdiuk`) | **Ukraine** (`ukr`) | Ranged Infantry | 85 | Firearm | 12 | 4.06 | 16.88 | 2.96 | 4.14 |
| 35 | **Jaeger** (`jagerswi`) | **Switzerland** (`swi`) | Ranged Infantry | 65 | Firearm | 20 | 6.88 | 22.5 | 2.91 | 4.07 |
| 36 | **Musketeer, 17th century** (`musketeerpol`) | **Poland** (`pol`) | Ranged Infantry | 70 | Firearm | 9 | 3.12 | 13.13 | 2.88 | 4.03 |
| 37 | **Hajduk** (`gauduk`) | **Hungary** (`hun`) | Ranged Infantry | 60 | Firearm | 9 | 3.12 | 14.06 | 2.88 | 4.03 |
| 38 | **Dragoon, 17th century** (`dragoon`) | **Austria** (`aus`) | Mounted Ranged Unit | 220 | Firearm | 15 | 5.62 | 15.0 | 2.67 | 3.74 |
| 39 | **Musketeer, 17th century** (`musketeernet`) | **Netherlands** (`net`) | Ranged Infantry | 65 | Firearm | 10 | 3.75 | 15.0 | 2.67 | 3.74 |
| 40 | **Light cavalry** (`lightcavalry`) | **Hungary** (`hun`) | Mounted Ranged Unit | 175 | Firearm | 14 | 5.31 | 18.75 | 2.64 | 3.7 |
| 41 | **Pospolite ruszenie** (`dragoonpol`) | **Poland** (`pol`) | Mounted Ranged Unit | 185 | Firearm | 13 | 5.0 | 15.94 | 2.6 | 3.64 |
| 42 | **Musketeer, 17th century** (`musketeer`) | **Bavaria** (`bav`) | Ranged Infantry | 70 | Firearm | 12 | 4.69 | 15.0 | 2.56 | 3.58 |
| 43 | **Strelets** (`strelet`) | **Russia** (`rus`) | Ranged Infantry | 85 | Firearm | 12 | 4.69 | 13.13 | 2.56 | 3.58 |
| 44 | **Janissary** (`jannisary`) | **Turkey** (`tur`) | Ranged Infantry | 65 | Firearm | 12 | 4.69 | 15.94 | 2.56 | 3.58 |
| 45 | **Covenanter musketeer** (`musketeersco`) | **Scotland** (`sco`) | Ranged Infantry | 90 | Firearm | 12 | 4.69 | 15.94 | 2.56 | 3.58 |
| 46 | **Musketeer, 17th century** (`musketeerspa`) | **Spain** (`spa`) | Ranged Infantry | 85 | Firearm | 15 | 5.94 | 15.94 | 2.53 | 3.54 |
| 47 | **Musketeer, 17th century** (`musketeeraus`) | **Austria** (`aus`) | Ranged Infantry | 55 | Firearm | 12 | 5.0 | 15.0 | 2.4 | 3.36 |
| 48 | **Dragoon, 18th century** (`dragoon18fra`) | **France** (`fra`) | Mounted Ranged Unit | 140 | Firearm | 10 | 4.69 | 15.0 | 2.13 | 2.98 |
| 49 | **Volunteer** (`jagerpor`) | **Portugal** (`por`) | Ranged Infantry | 50 | Firearm | 10 | 5.94 | 15.0 | 1.68 | 2.35 |

<a id="3-effective-hp--против-эталонной-атаки-10-единиц-урона-по-типу"></a>
<a id="3-живучесть-против-атаки-силой-10"></a>
## §3. Survivability against a 10-Damage Attack

The table shows how many hits a unit survives when struck by a weapon with
base damage 10. Results scale proportionally for stronger or weaker attacks
while damage remains above protection. Even when protection absorbs the
entire attack, the engine still removes at least one health point [^2].

Only units with at least one non-zero protection value are included.

| Unit | Nations | Role | Health | General armor | Hits: pike | Sword | Bullet | Grapeshot | Arrow | Cannonball |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| **Vityaz** (`vityaz`) | **Russia** (`rus`) | Heavy Cavalry | 380 | — | 47.5 | 63.3 | 54.3 | 380.0 | 380.0 | 380.0 |
| **Heavy Sipahi** (`sipahi`) | **Turkey** (`tur`) | Heavy Cavalry | 360 | — | 51.4 | 120.0 | 60.0 | 360.0 | 360.0 | 360.0 |
| **Cavalry Guard** (`guardcavalrysax`) | **Saxony** (`sax`) | Heavy Cavalry | 320 | — | 40.0 | 64.0 | 320.0 | 320.0 | 320.0 | 320.0 |
| **Hetman** (`hetman`) | **Ukraine** (`ukr`) | Heavy Cavalry | 320 | — | 32.0 | 35.6 | 45.7 | 320.0 | 45.7 | 320.0 |
| **Cuirassier** (`cuirassier`) | **Austria** (`aus`) | Heavy Cavalry | 300 | — | 37.5 | 50.0 | 300.0 | 300.0 | 60.0 | 300.0 |
| **Reiter** (`reiter`) | **Austria** (`aus`) | Heavy Cavalry | 300 | — | 37.5 | 75.0 | 75.0 | 300.0 | 300.0 | 300.0 |
| **Swedish Reiter** (`reiterswe`) | **Sweden** (`swe`) | Heavy Cavalry | 300 | — | 37.5 | 42.9 | 100.0 | 300.0 | 100.0 | 300.0 |
| **Mameluke** (`mameluke`) | **Algeria** (`alg`) | Heavy Cavalry | 280 | — | 31.1 | 40.0 | 31.1 | 280.0 | 140.0 | 28.0 |
| **Light Sipahi** (`spakh`) | **Turkey** (`tur`) | Heavy Cavalry | 230 | — | 23.0 | 25.6 | 23.0 | 230.0 | 28.8 | 23.0 |
| **Winged Hussar** (`wingedhussar`) | **Poland** (`pol`) | Light Cavalry | 225 | — | 25.0 | 28.1 | 45.0 | 225.0 | 225.0 | 225.0 |
| **Sword Clansman** (`swordsmansco`) | **Scotland** (`sco`) | Light Infantry | 180 | — | 20.0 | 22.5 | 22.5 | 180.0 | 45.0 | 180.0 |
| **Officer, 17th century** (`officer`) | **Austria** (`aus`) | Light Infantry | 125 | — | 15.6 | 15.6 | 25.0 | 125.0 | 125.0 | 125.0 |
| **Pikeman, 17th century** (`pikeman`) | **Spain** (`spa`) | Light Infantry | 100 | — | 14.3 | 16.7 | 25.0 | 100.0 | 100.0 | 100.0 |
| **Pikeman, 17th century** (`pikemanpor`) | **Portugal** (`por`) | Light Infantry | 100 | — | 10.0 | 11.1 | 11.1 | 100.0 | 16.7 | 10.0 |
| **Coselete** (`pikemanspa`) | **Spain** (`spa`) | Light Infantry | 100 | — | 14.3 | 16.7 | 25.0 | 100.0 | 100.0 | 100.0 |
| **Roundshier** (`roundshier`) | **Austria** (`aus`) | Light Infantry | 100 | — | 14.3 | 14.3 | 33.3 | 100.0 | 100.0 | 100.0 |
| **Pikeman, 17th century** (`pikeman`) | **Austria** (`aus`) | Light Infantry | 90 | — | 12.9 | 11.2 | 15.0 | 90.0 | 22.5 | 90.0 |
| **Pikeman, 17th century** (`pikemanswi`) | **Switzerland** (`swi`) | Light Infantry | 90 | — | 12.9 | 12.9 | 22.5 | 90.0 | 22.5 | 90.0 |
| **Spearman** (`pikemanrus`) | **Russia** (`rus`) | Light Infantry | 85 | — | 10.6 | 9.4 | 14.2 | 85.0 | 14.2 | 85.0 |
| **Roundshier (mercenary)** (`roundshierdip`) | all 21 | Light Infantry | 75 | — | 15.0 | 10.7 | 37.5 | 75.0 | 75.0 | 75.0 |
| **Musketeer, 17th century** (`musketeerspa`) | **Spain** (`spa`) | Ranged Infantry | 85 | — | 12.1 | 10.6 | 17.0 | 85.0 | 28.3 | 85.0 |
| **Musketeer, 17th century** (`musketeeraus`) | **Austria** (`aus`) | Ranged Infantry | 55 | — | 6.9 | 6.9 | 11.0 | 55.0 | 11.0 | 55.0 |

<a id="4-замечания-и-оговорки"></a>
## §4. Notes and Limitations

- **Melee attacks** are omitted from the damage-per-second ranking. Their
  damage is triggered by a frame of the attack animation
  (`onaclanimationreachedwork`), with a cycle of roughly 25–32 frames, or
  about one hit per game second.
- **Formation bonuses** are omitted. `fAddDamage`, `fAddShield`, and
  `fAddShieldHold` depend on formation and state rather than on the unit
  itself, so the table compares base values against base values.
- **Mortar blasts and Fire Arrows** are separate weapon types without
  matching protection fields. They contribute to damage per second but do
  not appear in §3.
- **A Priest's healing weapon** is excluded because it is not an attack.
- **Infantry speed 32** is the engine's default value. The assignment
  `gc_obj_speed_peasant = 40` is commented out [^3], so the speed column
  reports declared constants [^4] rather than empirically measured movement.
- **Real time.** Multiply the game-time damage-per-second value by 1.4 for
  Fast speed. At Normal speed, no conversion is required.

---

<a id="источники"></a>
## Sources

All links are relative to `data/scripts/` in the Cossacks 3 installation.

[^1]: `_misc_DoDamage` — protection subtraction and the headshot branch —
      `lib/miscext2.script:380, 434`.

[^2]: Minimum-damage rule (`damage = 1`) —
      `lib/miscext2.script:381`.

[^3]: Commented-out `objbase.speed := gc_obj_speed_peasant` —
      `lib/unit.script:1192`.

[^4]: `gc_obj_speed_*` constants — `dmscript.global:603-620`.
