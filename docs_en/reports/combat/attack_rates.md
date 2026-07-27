<a id="cossacks-3--скорость-атаки-per-unit"></a>
<a id="скорость-атаки"></a>
# Attack Speed

[← Tables and calculations](../README.md)

<a id="модель"></a>
## Model

Cossacks 3 does not use a single “attacks per second” system. Instead:

- For ranged weapons, the cycle equals the reload time.
- For melee attacks, the cycle equals the attack-animation duration.
- Attacks per game second equal `1 / cycle duration`.
- On Fast, the real attack rate is 1.4 times higher.

A melee attack animation lasts between 11 and 33 frames depending on the
unit; the median is 15 frames.

<a id="1-скорость-атаки-по-юнитам"></a>
## §1. Unit attack speed

Each row represents one weapon used by a unit. Identical national variants are
grouped together.

**Cycle duration** is the time between attacks in game seconds. It is the
reload time for ranged weapons and the attack-animation duration for melee
weapons. A source marked **estimate** means that no readable animation was
available, so the median duration was used.

- **Attacks/game s** — attacks per game second = `1 / cycle_g`.
- **Attacks/real s at Fast** — the same rate multiplied by 1.4
  (`gc_settings_gamespeed_2`).

Ranged weapons appear first, followed by melee weapons. Within each group,
rows run from the fastest attack to the slowest.

| Unit | Weapon | Damage | Range, cells | Cycle, game s | Source | Attacks/game s | Attacks/real s at Fast | Nations |
| --- | --- | ---: | ---: | ---: | --- | ---: | ---: | --- |
| **Ship of the Line** (`battleship`) | Cannonball #0 | 1800 | 36.56 | 0.62 | reload | 1.61 | 2.26 | Algeria, Austria, Bavaria, Denmark… (+16) |
| **Archer (mercenary)** (`archerdip`) | Fire Arrow #1 | 100 | 14.06 | 0.78 | reload | 1.28 | 1.79 | all 21 nations |
| **Turkish archer (mercenary)** (`archerturdip`) | Fire Arrow #1 | 100 | 14.06 | 0.78 | reload | 1.28 | 1.79 | all 21 nations |
| **Galley** (`galley`) | Explosive shell #1 | 1000 | 58.13 | 1.56 | reload | 0.64 | 0.90 | Algeria, Austria, Bavaria, Denmark… (+16) |
| **Tatar** (`tatar`) | Arrow #0 | 15 | 20.63 | 1.56 | reload | 0.64 | 0.90 | Turkey |
| **Xebec** (`xebec`) | Cannonball #0 | 1800 | 31.88 | 1.56 | reload | 0.64 | 0.90 | Algeria, Turkey |
| **Multi-barrelled Cannon** (`multicannon`) | Grapeshot #0 | 500 | 13.13 | 1.88 | reload | 0.53 | 0.74 | Austria, Bavaria, Denmark, England… (+13) |
| **Dragoon, 18th century (mercenary)** (`dragoon18dip`) | Bullet #0 | 18 | 15.0 | 2.25 | reload | 0.44 | 0.62 | all 21 nations |
| **Light cavalry (mercenary)** (`lightcavalrydip`) | Bullet #0 | 18 | 15.0 | 2.25 | reload | 0.44 | 0.62 | all 21 nations |
| **Archer** (`archer`) | Arrow #0 | 15 | 15.0 | 2.34 | reload | 0.43 | 0.60 | Algeria |
| **Chaika** (`chaika`) | Cannonball #0 | 1000 | 20.63 | 2.34 | reload | 0.43 | 0.60 | Ukraine |
| **Frigate** (`frigate`) | Cannonball #0 | 1800 | 30.94 | 2.34 | reload | 0.43 | 0.60 | Austria, Bavaria, Denmark, England… (+14) |
| **Grenadier** (`grenadier`) | Explosive shell #2 | 110 | 9.38 | 2.34 | reload | 0.43 | 0.60 | Austria, England, France, Netherlands… (+9) |
| **Grenadier** (`grenadierbav`) | Explosive shell #2 | 110 | 9.38 | 2.34 | reload | 0.43 | 0.60 | Bavaria |
| **Grenadier** (`grenadierden`) | Explosive shell #2 | 110 | 9.38 | 2.34 | reload | 0.43 | 0.60 | Denmark |
| **Grenadier** (`grenadierpru`) | Explosive shell #2 | 110 | 9.38 | 2.34 | reload | 0.43 | 0.60 | Prussia |
| **Grenadier** (`grenadiersax`) | Explosive shell #2 | 110 | 9.38 | 2.34 | reload | 0.43 | 0.60 | Saxony |
| **Archer (mercenary)** (`archerdip`) | Arrow #0 | 25 | 13.13 | 2.50 | reload | 0.40 | 0.56 | all 21 nations |
| **Turkish archer (mercenary)** (`archerturdip`) | Arrow #0 | 25 | 13.13 | 2.50 | reload | 0.40 | 0.56 | all 21 nations |
| **Turkish archer** (`archertur`) | Arrow #0 | 20 | 16.88 | 2.66 | reload | 0.38 | 0.53 | Turkey |
| **Frame gun** (`framegun`) | Cannonball #0 | 500 | 33.75 | 2.81 | reload | 0.36 | 0.50 | Scotland |
| **Grenadier** (`grenadierhun`) | Explosive shell #2 | 110 | 11.25 | 2.81 | reload | 0.36 | 0.50 | Hungary |
| **Bow Clansman** (`archersco`) | Arrow #0 | 20 | 18.75 | 3.12 | reload | 0.32 | 0.45 | Scotland |
| **Hajduk** (`gauduk`) | Bullet #1 | 9 | 14.06 | 3.12 | reload | 0.32 | 0.45 | Hungary |
| **Grenadier (mercenary)** (`grenadierdip`) | Explosive shell #2 | 200 | 7.5 | 3.12 | reload | 0.32 | 0.45 | all 21 nations |
| **Musketeer, 17th century** (`musketeerpol`) | Bullet #1 | 9 | 13.13 | 3.12 | reload | 0.32 | 0.45 | Poland |
| **Musketeer, 17th century** (`musketeernet`) | Bullet #1 | 10 | 15.0 | 3.75 | reload | 0.27 | 0.37 | Netherlands |
| **Archer** (`archer`) | Fire Arrow #1 | 150 | 11.25 | 3.91 | reload | 0.26 | 0.36 | Algeria |
| **Serdiuk** (`serdiuk`) | Bullet #1 | 12 | 16.88 | 4.06 | reload | 0.25 | 0.34 | Ukraine |
| **Bow Clansman** (`archersco`) | Fire Arrow #1 | 150 | 18.75 | 4.38 | reload | 0.23 | 0.32 | Scotland |
| **Turkish archer** (`archertur`) | Fire Arrow #1 | 150 | 16.88 | 4.38 | reload | 0.23 | 0.32 | Turkey |
| **Grenadier** (`grenadierpru`) | Bullet #1 | 16 | 16.88 | 4.38 | reload | 0.23 | 0.32 | Prussia |
| **Musketeer, 18th century** (`musketeer18sax`) | Bullet #1 | 19 | 16.88 | 4.38 | reload | 0.23 | 0.32 | Saxony |
| **Dragoon, 18th century** (`dragoon18fra`) | Bullet #0 | 10 | 15.0 | 4.69 | reload | 0.21 | 0.30 | France |
| **Galley** (`galley`) | Cannonball #0 | 100 | 22.5 | 4.69 | reload | 0.21 | 0.30 | Algeria, Austria, Bavaria, Denmark … (+16) |
| **Grenadier (mercenary)** (`grenadierdip`) | Bullet #1 | 16 | 15.0 | 4.69 | reload | 0.21 | 0.30 | all 21 nations |
| **Janissary** (`jannisary`) | Bullet #1 | 12 | 15.94 | 4.69 | reload | 0.21 | 0.30 | Turkey |
| **Musketeer, 17th century** (`musketeer`) | Bullet #1 | 12 | 15.0 | 4.69 | reload | 0.21 | 0.30 | Bavaria, Denmark, England, France … (+7) |
| **Musketeer, 18th century** (`musketeer18`) | Bullet #1 | 16 | 16.88 | 4.69 | reload | 0.21 | 0.30 | Austria, England, France, Hungary … (+9) |
| **Musketeer, 18th century** (`musketeer18pru`) | Bullet #1 | 22 | 17.81 | 4.69 | reload | 0.21 | 0.30 | Prussia |
| **Covenanter musketeer** (`musketeersco`) | Bullet #1 | 12 | 15.94 | 4.69 | reload | 0.21 | 0.30 | Scotland |
| **Pandur** (`pandur`) | Bullet #1 | 17 | 16.88 | 4.69 | reload | 0.21 | 0.30 | Austria |
| **Strelets** (`strelet`) | Bullet #0 | 12 | 13.13 | 4.69 | reload | 0.21 | 0.30 | Russia |
| **Tatar** (`tatar`) | Fire Arrow #1 | 140 | 20.63 | 4.69 | reload | 0.21 | 0.30 | Turkey |
| **Dragoon, 18th century** (`dragoon18net`) | Bullet #0 | 17 | 15.94 | 5.00 | reload | 0.20 | 0.28 | Netherlands |
| **Dragoon, 18th century** (`dragoon18pie`) | Bullet #0 | 19 | 16.88 | 5.00 | reload | 0.20 | 0.28 | Piedmont |
| **Pospolite ruszenie** (`dragoonpol`) | Bullet #0 | 13 | 15.94 | 5.00 | reload | 0.20 | 0.28 | Poland |
| **Highlander** (`highlander`) | Bullet #1 | 16 | 15.94 | 5.00 | reload | 0.20 | 0.28 | England |
| **Musketeer, 17th century** (`musketeeraus`) | Bullet #0 | 12 | 15.0 | 5.00 | reload | 0.20 | 0.28 | Austria |
| **Szekely** (`pandurhun`) | Bullet #1 | 19 | 18.75 | 5.00 | reload | 0.20 | 0.28 | Hungary |
| **Dragoon, 18th century** (`dragoon18`) | Bullet #0 | 19 | 16.88 | 5.31 | reload | 0.19 | 0.26 | Austria, Bavaria, Denmark, England … (+9) |
| **Grenadier** (`grenadier`) | Bullet #1 | 16 | 16.88 | 5.31 | reload | 0.19 | 0.26 | Austria, England, France, Netherlands … (+9) |
| **Grenadier** (`grenadierbav`) | Bullet #1 | 19 | 16.88 | 5.31 | reload | 0.19 | 0.26 | Bavaria |
| **Grenadier** (`grenadierhun`) | Bullet #1 | 16 | 16.88 | 5.31 | reload | 0.19 | 0.26 | Hungary |
| **Grenadier** (`grenadiersax`) | Bullet #1 | 19 | 17.81 | 5.31 | reload | 0.19 | 0.26 | Saxony |
| **Light cavalry** (`lightcavalry`) | Bullet #0 | 14 | 18.75 | 5.31 | reload | 0.19 | 0.26 | Hungary |
| **Dragoon, 17th century** (`dragoon`) | Bullet #0 | 15 | 15.0 | 5.62 | reload | 0.18 | 0.25 | Austria, Bavaria, Denmark, England … (+12) |
| **Chasseur** (`chasseur`) | Bullet #1 | 20 | 19.69 | 5.94 | reload | 0.17 | 0.24 | France |
| **Grenadier** (`grenadierden`) | Bullet #1 | 19 | 16.88 | 5.94 | reload | 0.17 | 0.24 | Denmark |
| **Volunteer** (`jagerpor`) | Bullet #1 | 10 | 15.0 | 5.94 | reload | 0.17 | 0.24 | Portugal |
| **Musketeer, 18th century** (`musketeer18bav`) | Bullet #1 | 22 | 17.81 | 5.94 | reload | 0.17 | 0.24 | Bavaria |
| **Musketeer, 18th century** (`musketeer18den`) | Bullet #1 | 29 | 16.88 | 5.94 | reload | 0.17 | 0.24 | Denmark |
| **Musketeer, 17th century** (`musketeerspa`) | Bullet #0 | 15 | 15.94 | 5.94 | reload | 0.17 | 0.24 | Spain |
| **Jaeger** (`jagerswi`) | Bullet #1 | 20 | 22.5 | 6.88 | reload | 0.15 | 0.20 | Switzerland |
| **King's Musketeer** (`kingmusketeer`) | Bullet #0 | 43 | 13.13 | 6.88 | reload | 0.15 | 0.20 | France |
| **Bombard** (`mortar`) | Explosive shell #0 | 200 | 48.75 | 7.81 | reload | 0.13 | 0.18 | all 21 nations |
| **Cannon** (`cannon`) | Cannonball #0 | 1800 | 40.5 | 10.94 | reload | 0.09 | 0.13 | all 21 nations |
| **Yacht** (`yacht`) | Cannonball #0 | 1000 | 20.63 | 10.94 | reload | 0.09 | 0.13 | Austria, Bavaria, Denmark, England … (+14) |
| **Yacht** (`yachttur`) | Cannonball #0 | 30 | 18.75 | 12.50 | reload | 0.08 | 0.11 | Turkey |
| **Howitzer** (`howitzer`) | Cannonball #0 | 4000 | 26.25 | 18.75 | reload | 0.05 | 0.07 | all 21 nations |
| **Pikeman, 18th century** (`pikeman18`) | Pike #0 | 9 | 1.88 | 0.28 | animation | 3.56 | 4.98 | Austria, Bavaria, Denmark, England … (+12) |
| **Spearman** (`pikemanrus`) | Pike #0 | 8 | 1.69 | 0.31 | animation | 3.20 | 4.48 | Russia |
| **Pikeman, 18th century** (`pikeman18swe`) | Pike #0 | 11 | 1.88 | 0.38 | animation | 2.67 | 3.73 | Sweden |
| **Pikeman, 17th century** (`pikemanpol`) | Pike #0 | 8 | 2.06 | 0.38 | animation | 2.67 | 3.73 | Poland |
| **Pikeman, 17th century** (`pikemanpor`) | Pike #0 | 9 | 1.88 | 0.38 | animation | 2.67 | 3.73 | Portugal |
| **Ottoman Pikeman** (`pikemantur`) | Pike #0 | 9 | 2.06 | 0.38 | animation | 2.67 | 3.73 | Algeria, Turkey |
| **Roundshier** (`roundshier`) | Sword #0 | 6 | 1.13 | 0.38 | animation | 2.67 | 3.73 | Austria |
| **Heavy Sipahi** (`sipahi`) | Sword #0 | 15 | 1.22 | 0.38 | animation | 2.67 | 3.73 | Turkey |
| **Vityaz** (`vityaz`) | Pike #0 | 14 | 1.22 | 0.38 | animation | 2.67 | 3.73 | Russia |
| **Winged Hussar** (`wingedhussar`) | Pike #0 | 14 | 1.88 | 0.38 | animation | 2.67 | 3.73 | Poland |
| **Sich Cossack** (`cossacksich`) | Sword #0 | 13 | 1.22 | 0.41 | animation | 2.46 | 3.45 | Ukraine |
| **Sword Clansman** (`swordsmansco`) | Sword #0 | 10 | 1.13 | 0.41 | animation | 2.46 | 3.45 | Scotland |
| **Don Cossack** (`cossackdon`) | Pike #0 | 13 | 1.88 | 0.44 | animation | 2.29 | 3.20 | Russia |
| **Register Cossack** (`cossackregister`) | Pike #0 | 12 | 1.88 | 0.44 | animation | 2.29 | 3.20 | Ukraine |
| **Croat** (`croat`) | Sword #0 | 9 | 1.22 | 0.44 | animation | 2.29 | 3.20 | Austria |
| **Cuirassier** (`cuirassier`) | Pike #0 | 14 | 1.22 | 0.44 | animation | 2.29 | 3.20 | Austria, Bavaria, Denmark, England … (+13) |
| **Cavalry Guard** (`guardcavalrysax`) | Pike #0 | 15 | 1.22 | 0.44 | animation | 2.29 | 3.20 | Saxony |
| **Hakkapeliitta** (`hackapell`) | Pike #0 | 12 | 1.22 | 0.44 | animation | 2.29 | 3.20 | Sweden |
| **Hussar** (`hussar`) | Sword #0 | 12 | 1.22 | 0.44 | animation | 2.29 | 3.20 | Austria, Bavaria, Denmark, England … (+10) |
| **Hussar** (`hussarhun`) | Sword #0 | 10 | 1.22 | 0.44 | animation | 2.29 | 3.20 | Hungary |
| **Hussar** (`hussarpru`) | Sword #0 | 9 | 1.22 | 0.44 | animation | 2.29 | 3.20 | Prussia |
| **Mounted Jaeger** (`hussarswi`) | Sword #0 | 14 | 1.22 | 0.44 | animation | 2.29 | 3.20 | Switzerland |
| **Lancer** (`lancersco`) | Pike #0 | 11 | 1.88 | 0.44 | animation | 2.29 | 3.20 | Scotland |
| **Light Infantryman** (`lightinfantry`) | Sword #0 | 5 | 0.94 | 0.44 | animation | 2.29 | 3.20 | Algeria, Turkey |
| **Mameluke** (`mameluke`) | Pike #0 | 16 | 1.88 | 0.44 | animation | 2.29 | 3.20 | Algeria |
| **Musketeer, 18th century** (`musketeer18`) | Pike #0 | 10 | 1.22 | 0.44 | animation | 2.29 | 3.20 | Austria, England, France, Hungary … (+9) |
| **Officer, 17th century** (`officer`) | Pike #0 | 30 | 1.22 | 0.44 | animation | 2.29 | 3.20 | Austria, Bavaria, Denmark, England … (+12) |
| **Commander** (`officerrus`) | Pike #0 | 40 | 1.22 | 0.44 | animation | 2.29 | 3.20 | Russia |
| **Raider** (`raidersco`) | Sword #0 | 11 | 1.22 | 0.44 | animation | 2.29 | 3.20 | Scotland |
| **Reiter** (`reiter`) | Pike #0 | 15 | 1.22 | 0.44 | animation | 2.29 | 3.20 | Austria, Bavaria, Denmark, England … (+10) |
| **Light Reiter** (`reiterpol`) | Sword #0 | 9 | 1.22 | 0.44 | animation | 2.29 | 3.20 | Poland |
| **Swedish Reiter** (`reiterswe`) | Pike #0 | 14 | 1.22 | 0.44 | animation | 2.29 | 3.20 | Sweden |
| **Light Sipahi** (`spakh`) | Pike #0 | 15 | 1.88 | 0.44 | animation | 2.29 | 3.20 | Turkey |
| **Sich Cossack (mercenary)** (`cossacksichdip`) | Sword #0 | 8 | 1.22 | 0.47 | estimate | 2.13 | 2.99 | all 21 nations |
| **Grenadier (mercenary)** (`grenadierdip`) | Pike #0 | 30 | 1.5 | 0.47 | estimate | 2.13 | 2.99 | all 21 nations |
| **Hetman** (`hetman`) | Pike #0 | 70 | 1.22 | 0.47 | animation | 2.13 | 2.99 | Ukraine |
| **Light Infantryman (mercenary)** (`lightinfantrydip`) | Sword #0 | 16 | 0.94 | 0.47 | estimate | 2.13 | 2.99 | all 21 nations |
| **Pikeman, 17th century** (`pikeman`) | Pike #0 | 8 | 1.88 | 0.47 | animation | 2.13 | 2.99 | Austria, Bavaria, Denmark, England… (+8) |
| **Pikeman, 17th century** (`pikeman`) | Pike #0 | 10 | 1.88 | 0.47 | animation | 2.13 | 2.99 | Spain |
| **Covenanter pikeman** (`pikemansco`) | Pike #0 | 9 | 1.88 | 0.47 | animation | 2.13 | 2.99 | Scotland |
| **Coselete** (`pikemanspa`) | Pike #0 | 10 | 1.88 | 0.47 | animation | 2.13 | 2.99 | Spain |
| **Pikeman, 17th century** (`pikemanswi`) | Pike #0 | 10 | 1.88 | 0.47 | animation | 2.13 | 2.99 | Switzerland |
| **Roundshier (mercenary)** (`roundshierdip`) | Sword #0 | 6 | 1.13 | 0.47 | estimate | 2.13 | 2.99 | all 21 nations |
| **Grenadier** (`grenadier`) | Pike #0 | 18 | 1.5 | 0.50 | animation | 2.00 | 2.80 | Austria, England, France, Netherlands… (+9) |
| **Grenadier** (`grenadierbav`) | Pike #0 | 14 | 1.5 | 0.50 | animation | 2.00 | 2.80 | Bavaria |
| **Grenadier** (`grenadierden`) | Pike #0 | 22 | 1.5 | 0.50 | animation | 2.00 | 2.80 | Denmark |
| **Grenadier** (`grenadierhun`) | Pike #0 | 30 | 1.5 | 0.50 | animation | 2.00 | 2.80 | Hungary |
| **Grenadier** (`grenadierpru`) | Pike #0 | 18 | 1.5 | 0.50 | animation | 2.00 | 2.80 | Prussia |
| **Grenadier** (`grenadiersax`) | Pike #0 | 22 | 1.5 | 0.50 | animation | 2.00 | 2.80 | Saxony |
| **Musketeer, 18th century** (`musketeer18bav`) | Pike #0 | 5 | 1.59 | 0.53 | animation | 1.88 | 2.64 | Bavaria |
| **Musketeer, 18th century** (`musketeer18den`) | Pike #0 | 8 | 1.59 | 0.53 | animation | 1.88 | 2.64 | Denmark |
| **Musketeer, 18th century** (`musketeer18pru`) | Pike #0 | 10 | 1.59 | 0.53 | animation | 1.88 | 2.64 | Prussia |
| **Musketeer, 18th century** (`musketeer18sax`) | Pike #0 | 7 | 1.22 | 0.53 | animation | 1.88 | 2.64 | Saxony |
| **Officer, 18th century** (`officer18`) | Pike #0 | 50 | 1.22 | 0.56 | animation | 1.78 | 2.49 | Austria, Bavaria, Denmark, England… (+13) |
| **Officer** (`officersco`) | Pike #0 | 40 | 1.22 | 0.56 | animation | 1.78 | 2.49 | Scotland |
| **Officer** (`officertur`) | Pike #0 | 30 | 1.22 | 0.56 | animation | 1.78 | 2.49 | Algeria, Turkey |
| **Peasant** (`peaaus`) | Sword #0 | 20 | 1.22 | 0.56 | animation | 1.78 | 2.49 | Austria, Bavaria, Prussia, Saxony, Switzerland |
| **Peasant** (`peaeng`) | Sword #0 | 20 | 1.22 | 0.56 | animation | 1.78 | 2.49 | Denmark, England, France, Netherlands, Sweden |
| **Peasant** (`peapol`) | Sword #0 | 20 | 1.22 | 0.56 | animation | 1.78 | 2.49 | Hungary, Poland |
| **Serf** (`pearus`) | Sword #0 | 20 | 1.22 | 0.56 | animation | 1.78 | 2.49 | Russia |
| **Peasant** (`peasco`) | Sword #0 | 20 | 1.22 | 0.56 | animation | 1.78 | 2.49 | Scotland |
| **Peasant** (`peaspa`) | Sword #0 | 20 | 1.22 | 0.56 | animation | 1.78 | 2.49 | Piedmont, Portugal, Spain, Venice |
| **Peasant** (`peatur`) | Sword #0 | 20 | 1.22 | 0.56 | animation | 1.78 | 2.49 | Algeria, Turkey |
| **Peasant** (`peaukr`) | Sword #0 | 20 | 1.22 | 0.56 | animation | 1.78 | 2.49 | Ukraine |

<a id="2-сводка-по-типу-оружия"></a>
## §2. Summary by Weapon Type

This table shows the minimum, median, and maximum cycle duration for each
weapon type, making the overall spread of attack rates within a class easy
to compare.

| Weapon type | Variants | Fastest cycle, game s | Median | Slowest cycle | Maximum attacks/real s at Fast |
| --- | ---: | ---: | ---: | ---: | ---: |
| Arrow | 6 | 1.56 | 2.50 | 3.12 | 0.90 |
| Firearm | 38 | 2.25 | 5.00 | 6.88 | 0.62 |
| Grapeshot | 1 | 1.88 | 1.88 | 1.88 | 0.74 |
| Cannonball | 10 | 0.62 | 4.69 | 18.75 | 2.26 |
| Fire Arrow | 6 | 0.78 | 4.38 | 4.69 | 1.79 |
| Explosive shell | 9 | 1.56 | 2.34 | 7.81 | 0.90 |
| Pike | 41 | 0.28 | 0.44 | 0.56 | 4.98 |
| Sword | 23 | 0.38 | 0.44 | 0.56 | 3.73 |

<a id="3-замечания"></a>
## §3. Notes

- **Reload versus attack animation.** For ranged weapons, `pause` defines the
  full cycle and includes the firing animation. Melee weapons have
  `pause = 0`; their cycle is the duration of the `attack0` animation.
- **Fallback duration.** If a unit has no readable `.aaf` file or no
  `attack0` track, the calculation uses the median melee duration of
  15 frames, or about 0.4688 game seconds.
- **Units with several weapons.** Each weapon used by units such as
  Musketeers and Archers occupies a separate row; `#index` in the weapon
  column identifies the slot.
- **Healing is excluded.** A Priest's healing action is not treated as a
  combat attack.
- **Real versus game time.** Game logic uses game seconds. At Fast speed,
  divide a duration by 1.4 or multiply an attack rate by 1.4 to obtain the
  real-time value.
- **Reload upgrades.** `attpauseperc` upgrades (see
  [upgrades](../../reference/05_upgrades/README.md)) reduce ranged-weapon
  reload time only. Melee attack speed is tied to animation and does not
  change.
