<a id="cossacks-3--vision-и-searchradius"></a>
<a id="радиус-обзора-и-обнаружения-целей"></a>
# Cossacks 3 – Vision and searchradius

[← Tables and calculations](../README.md)

Cossacks 3 has two concentric radii of "awareness":

- **vision** — fog-of-war (FOW) deployment radius. How many tiles around the unit are open to the owner on the minimap and game screen.
- **searchradius** — radius of **target detection for auto-attack**. Used in `bartprepare` / `_unit_SearchTarget`. Infantry **do not attack** an enemy outside this circle, even if it is visible through FOW.

<a id="формула"></a>
## Formula

View radius in tiles = `floor(20 + 4 × vision)`, where `vision` is a field in `objprop`, INTEGER (usually 0..8); calculation - in `_unit_GetVision` [^1].

| `vision` | tiles | Who is a typical carrier |
| ---: | ---: | --- |
| 0 | **20** | Default minimum (peasant fallback) |
| 1 | **24** | Most of the infantry, artillery, turret without upgrades |
| 2 | **28** | Light infantry, medium vigilance cavalry |
| 3 | **32** | Dragoons, medium cavalry, tower with upgrade |
| 4 | **36** | Scouts, reconnaissance, ukr-peasant |
| 5 | **40** | Hussar prussian, dragoon18 piedmontese |
| 7 | **48** | Hetman (top heavy cavalry review) |
| 8 | **52** | Drummer/Bagpiper, ships (Battleship/Frigate) |

<a id="1-полная-таблица-vision-fow-и-searchradius-target-acquisition-по-юнитам"></a>
<a id="обзор-и-автоматическое-обнаружение-целей-у-юнитов"></a>
## §1. Full table: vision (FOW) and searchradius (target acquisition) by units

Grouping: one row per unique set `(sid, vision, searchradius_tiles)`. Column **searchradius** - pause `weapon[0].radiusmax_tiles` (or 0 if there is no weapon / melee=0).

| usage | sid | vision | fov tiles | searchradius(tiles) | nations |
| --- | --- | ---: | ---: | ---: | --- |
| Battleship | `battleship` | 8 | **52** | 31.5 | alg, aus, bav, den, eng, fra... (+14) |
| Frigate | `frigate` | 8 | **52** | 33.75 | aus, bav, den, eng, fra, hun... (+12) |
| Frigate | `xebec` | 8 | **52** | 33.75 | Algeria, Turkey |
| Light Infantry | `drummer18` | 8 | **52** | — | aus, bav, den, fra, hun, net… (+9) |
| Heavy Cavalry | `hetman` | 7 | **48** | 11.25 | Ukraine |
| Light Infantry | `drummertur` | 7 | **48** | — | Algeria, Turkey |
| Light Infantry | `drummer` | 6 | **44** | — | aus, bav, den, eng, fra, hun… (+10) |
| Light Cavalry | `hussarpru` | 5 | **40** | 15.0 | Prussia |
| Light Infantry | `bagpiper` | 5 | **40** | — | England, Scotland |
| Light Infantry | `drummer18` | 5 | **40** | — | Russia |
| Light Infantry | `drummerrus` | 5 | **40** | — | Russia |
| Mounted Shooter | `dragoon18pie` | 5 | **40** | 16.88 | Piedmont |
| Archer | `tatar` | 4 | **36** | 20.63 | Turkey |
| Light Cavalry | `hussarswi` | 4 | **36** | 13.13 | Switzerland |
| Light Infantry | `officer18` | 4 | **36** | 9.38 | aus, bav, den, eng, fra, hun... (+11) |
| Mounted Shooter | `kingmusketeer` | 4 | **36** | 13.13 | France |
| Peasant | `peaukr` | 4 | **36** | 5.63 | Ukraine |
| Shooter | `chasseur` | 4 | **36** | 19.69 | France |
| Shooter | `jagerswi` | 4 | **36** | 22.5 | Switzerland |
| Yacht | `chaika` | 4 | **36** | 19.69 | Ukraine |
| Heavy Cavalry | `cossackdon` | 3 | **32** | 16.88 | Russia |
| Heavy Cavalry | `cossackregister` | 3 | **32** | 11.25 | Ukraine |
| Heavy Cavalry | `cuirassier` | 3 | **32** | 13.13 | aus, bav, den, eng, fra, hun... (+11) |
| Heavy Cavalry | `guardcavalrysax` | 3 | **32** | 11.25 | Saxony |
| Heavy Cavalry | `mameluke` | 3 | **32** | 11.25 | Algeria |
| Heavy Cavalry | `reiterpol` | 3 | **32** | 13.13 | Poland |
| Heavy Cavalry | `spakh` | 3 | **32** | 11.25 | Turkey |
| Light Cavalry | `cossacksich` | 3 | **32** | 15.0 | Ukraine |
| Light Cavalry | `hackapell` | 3 | **32** | 15.0 | Sweden |
| Light Cavalry | `hussar` | 3 | **32** | 13.13 | aus, bav, den, eng, fra, net... (+8) |
| Light Cavalry | `hussarhun` | 3 | **32** | 16.88 | Hungary |
| Light Infantry | `officertur` | 3 | **32** | 9.38 | Algeria, Turkey |
| Mounted Shooter | `dragoon` | 3 | **32** | 15.0 | aus, bav, den, eng, fra, hun … (+10) |
| Mounted Shooter | `dragoon18` | 3 | **32** | 16.88 | aus, bav, den, eng, pol, por … (+7) |
| Mounted Shooter | `dragoon18net` | 3 | **32** | 15.94 | Netherlands |
| Peasant | `pearus` | 3 | **32** | 9.38 | Russia |
| Shooter | `pandurhun` | 3 | **32** | 18.75 | Hungary |
| Yacht | `yacht` | 3 | **32** | 19.69 | aus, bav, den, eng, fra, hun … (+12) |
| Yacht | `yachttur` | 3 | **32** | 19.69 | Turkey |
| Archer | `archer` | 2 | **28** | 15.0 | Algeria |
| Archer | `archersco` | 2 | **28** | 18.75 | Scotland |
| Galley | `galley` | 2 | **28** | 20.63 | alg, aus, bav, den, eng, fra … (+14) |
| Grenadier | `grenadier` | 2 | **28** | 16.88 | aus, eng, fra, net, pie, pol … (+7) |
| Grenadier | `grenadierbav` | 2 | **28** | 16.88 | Bavaria |
| Grenadier | `grenadierden` | 2 | **28** | 16.88 | Denmark |
| Grenadier | `grenadierhun` | 2 | **28** | 18.75 | Hungary |
| Grenadier | `grenadierpru` | 2 | **28** | 16.88 | Prussia |
| Grenadier | `grenadiersax` | 2 | **28** | 17.81 | Saxony |
| Heavy Cavalry | `lancersco` | 2 | **28** | 11.25 | Scotland |
| Heavy Cavalry | `reiterswe` | 2 | **28** | 11.25 | Sweden |
| Heavy Cavalry | `sipahi` | 2 | **28** | 9.38 | Turkey |
| Heavy Cavalry | `vityaz` | 2 | **28** | 9.38 | Russia |
| Light Cavalry | `croat` | 2 | **28** | 13.13 | Austria |
| Light Cavalry | `raidersco` | 2 | **28** | 18.75 | Scotland |
| Light Cavalry | `wingedhussar` | 2 | **28** | 11.25 | Poland |
| Light Infantry | `lightinfantry` | 2 | **28** | 13.13 | Algeria, Turkey |
| Light Infantry | `officer` | 2 | **28** | 9.38 | aus, bav, den, eng, fra, hun … (+10) |
| Light Infantry | `officersco` | 2 | **28** | 9.38 | Scotland |
| Light Infantry | `pikeman18` | 2 | **28** | 13.13 | aus, bav, den, eng, fra, hun … (+10) |
| Light Infantry | `pikemansco` | 2 | **28** | 13.13 | Scotland |
| Light Infantry | `roundshierdip` | 2 | **28** | 13.13 | Scotland |
| Light Infantry | `swordsmansco` | 2 | **28** | 15.0 | Scotland |
| Mounted Shooter | `dragoon18fra` | 2 | **28** | 15.0 | France |
| Mounted Shooter | `dragoonpol` | 2 | **28** | 15.94 | Poland |
| Mounted Shooter | `lightcavalry` | 2 | **28** | 18.75 | Hungary |
| Shooter | `gauduk` | 2 | **28** | 14.06 | Hungary |
| Shooter | `musketeer` | 2 | **28** | 15.0 | bav, den, eng, fra, pie, por … (+5) |
| Shooter | `musketeer18` | 2 | **28** | 16.88 | aus, eng, fra, hun, net, pie … (+7) |
| Shooter | `musketeer18bav` | 2 | **28** | 17.81 | Bavaria |
| Shooter | `musketeer18den` | 2 | **28** | 16.88 | Denmark |
| Shooter | `musketeer18pru` | 2 | **28** | 17.81 | Prussia |
| Shooter | `musketeer18sax` | 2 | **28** | 16.88 | Saxony |
| Shooter | `musketeernet` | 2 | **28** | 15.0 | Netherlands |
| Shooter | `musketeersco` | 2 | **28** | 15.94 | Scotland |
| Shooter | `pandur` | 2 | **28** | 16.88 | Austria |
| Shooter | `serdiuk` | 2 | **28** | 16.88 | Ukraine |
| ? | `unitbox` | 1 | **24** | — | all |
| Archer | `archerdip` | 1 | **24** | 12.19 | all |
| Archer | `archertur` | 1 | **24** | 16.88 | Turkey |
| Archer | `archerturdip` | 1 | **24** | 12.19 | all |
| Cannon | `cannon` | 1 | **24** | 9.38 | all |
| Cannon | `framegun` | 1 | **24** | 22.5 | Scotland |
| Fishing Boat | `fishboat` | 1 | **24** | — | all |
| Grenadier | `grenadierdip` | 1 | **24** | 15.0 | all |
| Heavy Cavalry | `reiter` | 1 | **24** | 9.38 | aus, bav, den, eng, fra, hun … (+8) |
| Light Cavalry | `cossacksichdip` | 1 | **24** | 13.13 | all |
| Light Infantry | `lightinfantrydip` | 1 | **24** | 13.13 | all |
| Light Infantry | `mullah` | 1 | **24** | 9.38 | Algeria, Turkey |
| Light Infantry | `officerrus` | 1 | **24** | 9.38 | Russia |
| Light Infantry | `padre` | 1 | **24** | 7.5 | Piedmont |
| Light Infantry | `pikeman` | 1 | **24** | 13.13 | aus, bav, den, eng, fra, hun… (+7) |
| Light Infantry | `pikeman18swe` | 1 | **24** | 13.13 | Sweden |
| Light Infantry | `pikemanpol` | 1 | **24** | 13.13 | Poland |
| Light Infantry | `pikemanpor` | 1 | **24** | 13.13 | Portugal |
| Light Infantry | `pikemanrus` | 1 | **24** | 15.0 | Russia |
| Light Infantry | `pikemanspa` | 1 | **24** | 13.13 | Spain |
| Light Infantry | `pikemanswi` | 1 | **24** | 13.13 | Switzerland |
| Light Infantry | `pikemantur` | 1 | **24** | 13.13 | Algeria, Turkey |
| Light Infantry | `pope` | 1 | **24** | 9.38 | Russia, Ukraine |
| Light Infantry | `priest` | 1 | **24** | 7.5 | aus, bav, den, eng, fra, hun… (+10) |
| Light Infantry | `roundshier` | 1 | **24** | 11.25 | Austria |
| Light Infantry | `roundshierdip` | 1 | **24** | 13.13 | alg, aus, bav, den, eng, fra... (+14) |
| Mortar | `howitzer` | 1 | **24** | 18.75 | all |
| Multi-cannon | `multicannon` | 1 | **24** | 13.13 | aus, bav, den, eng, fra, hun... (+11) |
| Peasant | `peaaus` | 1 | **24** | 5.63 | Austria, Bavaria, Prussia, Saxony, Switzerland |
| Peasant | `peaeng` | 1 | **24** | 5.63 | Denmark, England, France, Netherlands, Sweden |
| Peasant | `peapol` | 1 | **24** | 5.63 | Hungary, Poland |
| Peasant | `peasco` | 1 | **24** | 7.5 | Scotland |
| Peasant | `peaspa` | 1 | **24** | 5.63 | Piedmont, Portugal, Spain, Venice |
| Peasant | `peatur` | 1 | **24** | 5.63 | Algeria, Turkey |
| Shooter | `dragoon18dip` | 1 | **24** | 15.94 | all |
| Shooter | `highlander` | 1 | **24** | 15.94 | England |
| Shooter | `jagerpor` | 1 | **24** | 15.0 | Portugal |
| Shooter | `jannisary` | 1 | **24** | 15.94 | Turkey |
| Shooter | `lightcavalrydip` | 1 | **24** | 15.94 | all |
| Shooter | `musketeeraus` | 1 | **24** | 15.94 | Austria |
| Shooter | `musketeerpol` | 1 | **24** | 13.13 | Poland |
| Shooter | `musketeerspa` | 1 | **24** | 15.94 | Spain |
| Shooter | `strelet` | 1 | **24** | 13.13 | Russia |
| Super Mortar | `mortar` | 1 | **24** | — | all |
| Transport | `ferry` | 1 | **24** | — | all |

<a id="2-vision-у-зданий"></a>
<a id="обзор-у-зданий"></a>
## §2. Vision near buildings

Unlike units, most buildings do not have `vision=0` or a field specified - visibility is provided by an “insert” from the FOW callback on the building itself (engine native). Here are those whose vision is clearly registered.

| usage | sid | vision | fov tiles | nation |
| --- | --- | ---: | ---: | --- |
| Tower | `eurtow` | 3 | **32** | Austria |
| Tower | `rustow` | 3 | **32** | Russia |
| Tower | `turtow` | 3 | **32** | Algeria |
| Shipyard | `porpor` | 3 | **32** | Portugal |

<a id="3-замечания"></a>
<a id="что-важно-учитывать"></a>
## §3. Notes

- **Vision > searchradius** for all units except mortars (mortar/super mortar) and towers with empty `searchradius`. This means: the unit **sees** the enemy before it can **detect it as a target**.
- **Default `vision=0`** still gives 20 vision tiles - the minimum circle for a unit to see the environment at all.
- **Drummer/Bagpiper** have `vision=8` ⇒ **52 vision tiles**, but do not attack (`searchradius=0`). This is the best "pure scout" in the game.
- **Ships** (Battleship/Frigate) `vision=8` - needed for sea patrols, far beyond the artillery range.
- **Hetman** (Ukraine) `vision=7` - the most alert cavalry unit on the shore.
- **Vision is not upgradeable.** There is no entry for `visionperc` or `+vision` in `efficiency_upgrades.md`.


<a id="источники"></a>
## Sources

All links are relative to `data/scripts/` in the Cossacks 3 installation.

[^1]: `_unit_GetVision` - `lib/unit.script:11565`.
