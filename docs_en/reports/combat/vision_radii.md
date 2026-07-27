<a id="cossacks-3--vision-и-searchradius"></a>
<a id="радиус-обзора-и-обнаружения-целей"></a>
# Vision and Automatic Target Detection

[← Tables and calculations](../README.md)

Cossacks 3 uses two separate awareness ranges:

- **Vision range** controls how far a unit reveals the map through the fog
  of war.
- **Automatic target-detection range** controls how far away the unit can
  acquire an enemy on its own. An enemy may therefore be visible without
  provoking an automatic attack.

<a id="формула"></a>
## Formula

Vision range = **20 + 4 × the internal vision level** [^1]. The level is
normally between 0 and 8.

| Internal vision | Vision, cells | Typical units |
| ---: | ---: | --- |
| 0 | **20** | Default minimum (peasant fallback) |
| 1 | **24** | Most infantry, artillery, and an unupgraded Tower |
| 2 | **28** | Light infantry, medium vigilance cavalry |
| 3 | **32** | Dragoons, medium cavalry, tower with upgrade |
| 4 | **36** | Scouts and the Ukrainian Peasant |
| 5 | **40** | Prussian Hussar and Piedmontese Dragoon |
| 7 | **48** | Hetman |
| 8 | **52** | Drummers, Bagpiper, Ship of the Line, and Frigate |

<a id="1-полная-таблица-vision-fow-и-searchradius-target-acquisition-по-юнитам"></a>
<a id="обзор-и-автоматическое-обнаружение-целей-у-юнитов"></a>
## §1. Unit Vision and Automatic Target Detection

Each row represents one distinct combination of unit, vision range, and
automatic target-detection range. A dash means that the unit has no
applicable ranged weapon.

| Unit | Internal ID | Internal vision | Vision, cells | Target detection, cells | Nations |
| --- | --- | ---: | ---: | ---: | --- |
| Ship of the Line | `battleship` | 8 | **52** | 31.5 | Algeria, Austria, Bavaria, Denmark, England, France... (+14) |
| Frigate | `frigate` | 8 | **52** | 33.75 | Austria, Bavaria, Denmark, England, France, Hungary... (+12) |
| Xebec | `xebec` | 8 | **52** | 33.75 | Algeria, Turkey |
| Drummer, 18th century | `drummer18` | 8 | **52** | — | Austria, Bavaria, Denmark, France, Hungary, Netherlands… (+9) |
| Hetman | `hetman` | 7 | **48** | 11.25 | Ukraine |
| Drummer, 17th century | `drummertur` | 7 | **48** | — | Algeria, Turkey |
| Drummer, 17th century | `drummer` | 6 | **44** | — | Austria, Bavaria, Denmark, England, France, Hungary… (+10) |
| Hussar | `hussarpru` | 5 | **40** | 15.0 | Prussia |
| Bagpiper | `bagpiper` | 5 | **40** | — | England, Scotland |
| Drummer, 18th century | `drummer18` | 5 | **40** | — | Russia |
| Drummer, 17th century | `drummerrus` | 5 | **40** | — | Russia |
| Dragoon, 18th century | `dragoon18pie` | 5 | **40** | 16.88 | Piedmont |
| Tatar | `tatar` | 4 | **36** | 20.63 | Turkey |
| Mounted Jaeger | `hussarswi` | 4 | **36** | 13.13 | Switzerland |
| Officer, 18th century | `officer18` | 4 | **36** | 9.38 | Austria, Bavaria, Denmark, England, France, Hungary... (+11) |
| King's Musketeer | `kingmusketeer` | 4 | **36** | 13.13 | France |
| Peasant | `peaukr` | 4 | **36** | 5.63 | Ukraine |
| Chasseur | `chasseur` | 4 | **36** | 19.69 | France |
| Jaeger | `jagerswi` | 4 | **36** | 22.5 | Switzerland |
| Chaika | `chaika` | 4 | **36** | 19.69 | Ukraine |
| Don Cossack | `cossackdon` | 3 | **32** | 16.88 | Russia |
| Register Cossack | `cossackregister` | 3 | **32** | 11.25 | Ukraine |
| Cuirassier | `cuirassier` | 3 | **32** | 13.13 | Austria, Bavaria, Denmark, England, France, Hungary... (+11) |
| Cavalry Guard | `guardcavalrysax` | 3 | **32** | 11.25 | Saxony |
| Mameluke | `mameluke` | 3 | **32** | 11.25 | Algeria |
| Light Reiter | `reiterpol` | 3 | **32** | 13.13 | Poland |
| Light Sipahi | `spakh` | 3 | **32** | 11.25 | Turkey |
| Sich Cossack | `cossacksich` | 3 | **32** | 15.0 | Ukraine |
| Hakkapeliitta | `hackapell` | 3 | **32** | 15.0 | Sweden |
| Hussar | `hussar` | 3 | **32** | 13.13 | Austria, Bavaria, Denmark, England, France, Netherlands... (+8) |
| Hussar | `hussarhun` | 3 | **32** | 16.88 | Hungary |
| Officer | `officertur` | 3 | **32** | 9.38 | Algeria, Turkey |
| Dragoon, 17th century | `dragoon` | 3 | **32** | 15.0 | Austria, Bavaria, Denmark, England, France, Hungary … (+10) |
| Dragoon, 18th century | `dragoon18` | 3 | **32** | 16.88 | Austria, Bavaria, Denmark, England, Poland, Portugal … (+7) |
| Dragoon, 18th century | `dragoon18net` | 3 | **32** | 15.94 | Netherlands |
| Serf | `pearus` | 3 | **32** | 9.38 | Russia |
| Szekely | `pandurhun` | 3 | **32** | 18.75 | Hungary |
| Yacht | `yacht` | 3 | **32** | 19.69 | Austria, Bavaria, Denmark, England, France, Hungary … (+12) |
| Yacht | `yachttur` | 3 | **32** | 19.69 | Turkey |
| Archer | `archer` | 2 | **28** | 15.0 | Algeria |
| Bow Clansman | `archersco` | 2 | **28** | 18.75 | Scotland |
| Galley | `galley` | 2 | **28** | 20.63 | Algeria, Austria, Bavaria, Denmark, England, France … (+14) |
| Grenadier | `grenadier` | 2 | **28** | 16.88 | Austria, England, France, Netherlands, Piedmont, Poland … (+7) |
| Grenadier | `grenadierbav` | 2 | **28** | 16.88 | Bavaria |
| Grenadier | `grenadierden` | 2 | **28** | 16.88 | Denmark |
| Grenadier | `grenadierhun` | 2 | **28** | 18.75 | Hungary |
| Grenadier | `grenadierpru` | 2 | **28** | 16.88 | Prussia |
| Grenadier | `grenadiersax` | 2 | **28** | 17.81 | Saxony |
| Lancer | `lancersco` | 2 | **28** | 11.25 | Scotland |
| Swedish Reiter | `reiterswe` | 2 | **28** | 11.25 | Sweden |
| Heavy Sipahi | `sipahi` | 2 | **28** | 9.38 | Turkey |
| Vityaz | `vityaz` | 2 | **28** | 9.38 | Russia |
| Croat | `croat` | 2 | **28** | 13.13 | Austria |
| Raider | `raidersco` | 2 | **28** | 18.75 | Scotland |
| Winged Hussar | `wingedhussar` | 2 | **28** | 11.25 | Poland |
| Light Infantryman | `lightinfantry` | 2 | **28** | 13.13 | Algeria, Turkey |
| Officer, 17th century | `officer` | 2 | **28** | 9.38 | Austria, Bavaria, Denmark, England, France, Hungary … (+10) |
| Officer | `officersco` | 2 | **28** | 9.38 | Scotland |
| Pikeman, 18th century | `pikeman18` | 2 | **28** | 13.13 | Austria, Bavaria, Denmark, England, France, Hungary … (+10) |
| Covenanter pikeman | `pikemansco` | 2 | **28** | 13.13 | Scotland |
| Roundshier (mercenary) | `roundshierdip` | 2 | **28** | 13.13 | Scotland |
| Sword Clansman | `swordsmansco` | 2 | **28** | 15.0 | Scotland |
| Dragoon, 18th century | `dragoon18fra` | 2 | **28** | 15.0 | France |
| Pospolite ruszenie | `dragoonpol` | 2 | **28** | 15.94 | Poland |
| Light cavalry | `lightcavalry` | 2 | **28** | 18.75 | Hungary |
| Hajduk | `gauduk` | 2 | **28** | 14.06 | Hungary |
| Musketeer, 17th century | `musketeer` | 2 | **28** | 15.0 | Bavaria, Denmark, England, France, Piedmont, Portugal … (+5) |
| Musketeer, 18th century | `musketeer18` | 2 | **28** | 16.88 | Austria, England, France, Hungary, Netherlands, Piedmont … (+7) |
| Musketeer, 18th century | `musketeer18bav` | 2 | **28** | 17.81 | Bavaria |
| Musketeer, 18th century | `musketeer18den` | 2 | **28** | 16.88 | Denmark |
| Musketeer, 18th century | `musketeer18pru` | 2 | **28** | 17.81 | Prussia |
| Musketeer, 18th century | `musketeer18sax` | 2 | **28** | 16.88 | Saxony |
| Musketeer, 17th century | `musketeernet` | 2 | **28** | 15.0 | Netherlands |
| Covenanter musketeer | `musketeersco` | 2 | **28** | 15.94 | Scotland |
| Pandur | `pandur` | 2 | **28** | 16.88 | Austria |
| Serdiuk | `serdiuk` | 2 | **28** | 16.88 | Ukraine |
| Test object | `unitbox` | 1 | **24** | — | all 21 nations |
| Archer (mercenary) | `archerdip` | 1 | **24** | 12.19 | all 21 nations |
| Turkish archer | `archertur` | 1 | **24** | 16.88 | Turkey |
| Turkish archer (mercenary) | `archerturdip` | 1 | **24** | 12.19 | all 21 nations |
| Cannon | `cannon` | 1 | **24** | 9.38 | all 21 nations |
| Frame gun | `framegun` | 1 | **24** | 22.5 | Scotland |
| Boat | `fishboat` | 1 | **24** | — | all 21 nations |
| Grenadier (mercenary) | `grenadierdip` | 1 | **24** | 15.0 | all 21 nations |
| Reiter | `reiter` | 1 | **24** | 9.38 | Austria, Bavaria, Denmark, England, France, Hungary … (+8) |
| Sich Cossack (mercenary) | `cossacksichdip` | 1 | **24** | 13.13 | all 21 nations |
| Light Infantryman (mercenary) | `lightinfantrydip` | 1 | **24** | 13.13 | all 21 nations |
| Mullah | `mullah` | 1 | **24** | 9.38 | Algeria, Turkey |
| Commander | `officerrus` | 1 | **24** | 9.38 | Russia |
| Padre | `padre` | 1 | **24** | 7.5 | Piedmont |
| Pikeman, 17th century | `pikeman` | 1 | **24** | 13.13 | Austria, Bavaria, Denmark, England, France, Hungary… (+7) |
| Pikeman, 18th century | `pikeman18swe` | 1 | **24** | 13.13 | Sweden |
| Pikeman, 17th century | `pikemanpol` | 1 | **24** | 13.13 | Poland |
| Pikeman, 17th century | `pikemanpor` | 1 | **24** | 13.13 | Portugal |
| Spearman | `pikemanrus` | 1 | **24** | 15.0 | Russia |
| Coselete | `pikemanspa` | 1 | **24** | 13.13 | Spain |
| Pikeman, 17th century | `pikemanswi` | 1 | **24** | 13.13 | Switzerland |
| Ottoman Pikeman | `pikemantur` | 1 | **24** | 13.13 | Algeria, Turkey |
| Pope | `pope` | 1 | **24** | 9.38 | Russia, Ukraine |
| Priest | `priest` | 1 | **24** | 7.5 | Austria, Bavaria, Denmark, England, France, Hungary… (+10) |
| Roundshier | `roundshier` | 1 | **24** | 11.25 | Austria |
| Roundshier (mercenary) | `roundshierdip` | 1 | **24** | 13.13 | Algeria, Austria, Bavaria, Denmark, England, France... (+14) |
| Howitzer | `howitzer` | 1 | **24** | 18.75 | all 21 nations |
| Multi-barrelled Cannon | `multicannon` | 1 | **24** | 13.13 | Austria, Bavaria, Denmark, England, France, Hungary... (+11) |
| Peasant | `peaaus` | 1 | **24** | 5.63 | Austria, Bavaria, Prussia, Saxony, Switzerland |
| Peasant | `peaeng` | 1 | **24** | 5.63 | Denmark, England, France, Netherlands, Sweden |
| Peasant | `peapol` | 1 | **24** | 5.63 | Hungary, Poland |
| Peasant | `peasco` | 1 | **24** | 7.5 | Scotland |
| Peasant | `peaspa` | 1 | **24** | 5.63 | Piedmont, Portugal, Spain, Venice |
| Peasant | `peatur` | 1 | **24** | 5.63 | Algeria, Turkey |
| Dragoon, 18th century (mercenary) | `dragoon18dip` | 1 | **24** | 15.94 | all 21 nations |
| Highlander | `highlander` | 1 | **24** | 15.94 | England |
| Volunteer | `jagerpor` | 1 | **24** | 15.0 | Portugal |
| Janissary | `jannisary` | 1 | **24** | 15.94 | Turkey |
| Light cavalry (mercenary) | `lightcavalrydip` | 1 | **24** | 15.94 | all 21 nations |
| Musketeer, 17th century | `musketeeraus` | 1 | **24** | 15.94 | Austria |
| Musketeer, 17th century | `musketeerpol` | 1 | **24** | 13.13 | Poland |
| Musketeer, 17th century | `musketeerspa` | 1 | **24** | 15.94 | Spain |
| Strelets | `strelet` | 1 | **24** | 13.13 | Russia |
| Bombard | `mortar` | 1 | **24** | — | all 21 nations |
| Ferry | `ferry` | 1 | **24** | — | all 21 nations |

<a id="2-vision-у-зданий"></a>
<a id="обзор-у-зданий"></a>
## §2. Building Vision

Most buildings do not declare their vision in the same way as units. The
table lists the buildings for which a vision value is explicitly available.

| Building | Internal ID | Internal vision | Vision, cells | Nation |
| --- | --- | ---: | ---: | --- |
| Tower | `eurtow` | 3 | **32** | Austria |
| Tower | `rustow` | 3 | **32** | Russia |
| Tower | `turtow` | 3 | **32** | Algeria |
| Shipyard | `porpor` | 3 | **32** | Portugal |

<a id="3-замечания"></a>
<a id="что-важно-учитывать"></a>
## §3. Notes

- **Vision normally exceeds automatic target-detection range.** A unit
  therefore sees an enemy before it acquires that enemy as a target.
- **An internal vision value of zero still reveals 20 cells.** This is the
  minimum vision range for a unit.
- **Drummers and the Bagpiper are exceptional scouts.** They can reveal
  52 cells despite having no attack.
- **The Ship of the Line and Frigate also reveal 52 cells,** well beyond
  artillery range.
- **The Ukrainian Hetman reveals 48 cells,** the greatest range among
  cavalry units.
- **Vision cannot be upgraded.**


<a id="источники"></a>
## Sources

All links are relative to `data/scripts/` in the Cossacks 3 installation.

[^1]: `_unit_GetVision` — `lib/unit.script:11565`.
