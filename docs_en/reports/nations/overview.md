<a id="сравнение-наций--общий-обзор"></a>
# Comparison of nations - general overview

**Derived report.** Counted from [`data.json`](../../../data.json) by script [`compute/compute_nations_overview.py`](../../../compute/compute_nations_overview.py). Regeneration: `python compute/compute_nations_overview.py`.

Side-by-side comparison of all 21 nations. For details on a specific nation - [`reference/nations/<nat>.md`](../../reference/nations/README.md).

<a id="1-размер-ростера-и-эпохальный-доступ"></a>
## §1. Roster size and Mythic access

How many different unit-sids are available to the nation (`?` - miss/test units, Drummer/Officer/Priest, etc. are classified separately). Column **18c** - Does the nation have 18th-century Barracks? (`<nat>ba2`); if not, the nation is locked in the 17th century. era.

| Nation | Total units | Combat | Strelkov | Cavalry | Grenadiers | Ships | 18th century |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | :---: |
| **alg** Algeria | 25 | 18 | 2 | 2 | 1 | 5 | ❌ |
| **aus** Austria | 38 | 30 | 5 | 7 | 2 | 6 | ✅ |
| **bav** Bavaria | 35 | 27 | 4 | 6 | 2 | 6 | ✅ |
| **den** Denmark | 35 | 27 | 4 | 6 | 2 | 6 | ✅ |
| **eng** England | 36 | 28 | 5 | 6 | 2 | 6 | ✅ |
| **fra** France | 37 | 29 | 5 | 7 | 2 | 6 | ✅ |
| **hun** Hungary | 36 | 28 | 5 | 6 | 2 | 6 | ✅ |
| **net** Netherlands | 35 | 27 | 4 | 6 | 2 | 6 | ✅ |
| **pie** Piedmont | 35 | 27 | 4 | 6 | 2 | 6 | ✅ |
| **pol** Poland | 37 | 29 | 4 | 8 | 2 | 6 | ✅ |
| **por** Portugal | 36 | 28 | 5 | 6 | 2 | 6 | ✅ |
| **pru** Prussia | 36 | 28 | 4 | 6 | 3 | 6 | ✅ |
| **eng** Russia | 35 | 27 | 4 | 6 | 2 | 6 | ✅ |
| **sax** Saxony | 36 | 28 | 4 | 7 | 2 | 6 | ✅ |
| **sco** Scotland | 28 | 21 | 3 | 3 | 1 | 5 | ✅ |
| **spa** Spain | 36 | 28 | 4 | 6 | 2 | 6 | ✅ |
| **swe** Sweden | 36 | 28 | 4 | 7 | 2 | 6 | ✅ |
| **swi** Switzerland | 36 | 28 | 5 | 6 | 2 | 6 | ✅ |
| **tur** Turkey | 29 | 21 | 3 | 3 | 1 | 6 | ❌ |
| **ukr** Ukraine | 22 | 16 | 3 | 4 | 1 | 4 | ❌ |
| **ven** Venice | 35 | 27 | 4 | 6 | 2 | 6 | ✅ |

<a id="2-покрытие-стандартных-построек"></a>
## §2. Covering standard buildings

`✅` = nation has this building, `❌` = nation does not have it. Full catalog of buildings - [03_buildings/README.md](../../reference/03_buildings/README.md).

| Nation | Town Hall | Housing | Mill | Storehouse | Tower | Stone wall/gate | Mine | Shipyard | Diplomatic Center |
| --- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **alg** Algeria | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| **aus** Austria | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| **bav** Bavaria | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| **den** Denmark | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| **eng** England | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| **fra** France | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| **hun** Hungary | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| **net** Netherlands | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| **pie** Piedmont | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| **pol** Poland | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| **por** Portugal | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| **pru** Prussia | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| **eng** Russia | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| **sax** Saxony | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| **sco** Scotland | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| **spa** Spain | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| **swe** Sweden | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| **swi** Switzerland | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| **tur** Turkey | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| **ukr** Ukraine | ✅ | ✅ | ✅ | ✅ | ❌ | ❌ | ✅ | ✅ | ✅ |
| **ven** Venice | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |

**Notable Omissions:**

- **ukr** Ukraine - no: Tower, Stone wall/gate

<a id="3-уникальные-юниты-по-нациям"></a>
## §3. Unique units by nation
Units with `sid`, which is found only in one nation (excluding mercenaries from `<nat>dip`). These are “feature” units with which the nation is associated. Mercenary sid (`<unit>dip`) - separately in §5.

| Nation | Unique `sid` (class HP) |
| --- | --- |
| **alg** Algeria | `mameluke` _Mameluke_ (Heavy cavalry, HP=280)<br>`archer` _Archer_ (Archer, HP=40) |
| **aus** Austria | `croat` _Croat_ (Light cavalry, HP=260)<br>`roundshier` _Roundshier_ (Light infantry, HP=100)<br>`pandur` _Pandur_ (Shooter, HP=85)<br>`musketeeraus` _Musketeer, 17th century_ (Shooter, HP=55) |
| **bav** Bavaria | `grenadierbav` _Grenadier_ (Grenadier, HP=125)<br>`musketeer18bav` _Musketeer, 18th century_ (Gunner, HP=100) |
| **den** Denmark | `grenadierden` _Grenadier_ (Grenadier, HP=125)<br>`musketeer18den` _Musketeer, 18th century_ (Gunner, HP=100) |
| **eng** England | `highlander` _Highlander_ (Shooter, HP=130) |
| **fra** France | `kingmusketeer` _King's Musketeer_ (Horse Rifleman, HP=280)<br>`dragoon18fra` _Dragoon, 18th century_ (Horse Rifleman, HP=140)<br>`chasseur` _Chasseur_ (Shooter, HP=75) |
| **hun** Hungary | `hussarhun` _Hussar_ (Light Cavalry, HP=250)<br>`lightcavalry` _Light cavalry_ (Horse Rifleman, HP=175)<br>`grenadierhun` _Grenadier_ (Grenadier, HP=125)<br>`pandurhun` _Szekely_ (Gunner, HP=75)<br>`gauduk` _Hajduk_ (Shooter, HP=60) |
| **net** Netherlands | `dragoon18net` _Dragoon, 18th century_ (Horse Rifleman, HP=320)<br>`musketeernet` _Musketeer, 17th century_ (Rifleman, HP=65) |
| **pie** Piedmont | `dragoon18pie` _Dragoon, 18th century_ (Horse Rifleman, HP=200)<br>`padre` _Padre_ (Light Infantry, HP=90) |
| **pol** Poland | `wingedhussar` _Winged Hussar_ (Light cavalry, HP=225)<br>`reiterpol` _Light Reiter_ (Heavy cavalry, HP=190)<br>`dragoonpol` _Pospolite ruszenie_ (Horse Rifleman, HP=185)<br>`pikemanpol` _Pikeman, 17th century_ (Light Infantry, HP=90)<br>`musketeerpol` _Musketeer, 17th century_ (Shooter, HP=70) |
| **por** Portugal | `pikemanpor` _Pikeman, 17th century_ (Light Infantry, HP=100)<br>`jagerpor` _Volunteer_ (Rifleman, HP=50) |
| **pru** Prussia | `hussarpru` _Hussar_ (Light Cavalry, HP=240)<br>`grenadierpru` _Grenadier_ (Grenadier, HP=125)<br>`musketeer18pru` _Musketeer, 18th century_ (Shooter, HP=100) |
| **eng** Russia | `vityaz` _Vityaz_ (Heavy cavalry, HP=380)<br>`cossackdon` _Don Cossack_ (Heavy cavalry, HP=220)<br>`officerrus` _Commander_ (Light Infantry, HP=125)<br>`drummerrus` _Drummer, 17th century_ (Light Infantry, HP=100)<br>`pikemanrus` _Spearman_ (Light Infantry, HP=85)<br>`strelet` _Strelets_ (Rifleman, HP=85)<br>`pearus` _Serf_ (Peasant, HP=50) |
| **sax** Saxony | `guardcavalrysax` _Cavalry Guard_ (Heavy cavalry, HP=320)<br>`grenadiersax` _Grenadier_ (Grenadier, HP=100)<br>`musketeer18sax` _Musketeer, 18th century_ (Shooter, HP=90) |
| **sco** Scotland | `framegun` _Frame gun_ (Cannon, HP=3000)<br>`lancersco` _Lancer_ (Heavy cavalry, HP=320)<br>`raidersco` _Raider_ (Light cavalry, HP=280)<br>`swordsmansco` _Sword Clansman_ (Light infantry, HP=180)<br>`archersco` _Bow Clansman_ (Archer, HP=150)<br>`officersco` _Officer_ (Light infantry, HP=150)<br>`pikemansco` _Covenanter pikeman_ (Light infantry, HP=100)<br>`musketeersco` _Covenanter musketeer_ (Rifleman, HP=90)<br>`peasco` _Peasant_ (Peasant, HP=60) |
| **spa** Spain | `pikemanspa` _Coselete_ (Light Infantry, HP=100)<br>`musketeerspa` _Musketeer, 17th century_ (Rifleman, HP=85) |
| **swe** Sweden | `reiterswe` _Swedish Reiter_ (Heavy cavalry, HP=300)<br>`hackapell` _Hakkapeliitta_ (Light cavalry, HP=245)<br>`pikeman18swe` _Pikeman, 18th century_ (Light Infantry, HP=110) |
| **swi** Switzerland | `hussarswi` _Mounted Jaeger_ (Light cavalry, HP=265)<br>`pikemanswi` _Pikeman, 17th century_ (Light infantry, HP=90)<br>`jagerswi` _Chasseur_ (Shooter, HP=65) |
| **tur** Turkey | `yachttur` _Yacht_ (Yacht, HP=35000)<br>`sipahi` _Heavy Sipahi_ (Heavy cavalry, HP=360)<br>`spakh` _Light Sipahi_ (Heavy cavalry, HP=230)<br>`tatar` _Tatar_ (Archer, HP=185)<br>`archertur` _Turkish archer_ (Archer, HP=65)<br>`jannisary` _Janissary_ (Shooter, HP=65) |
| **ukr** Ukraine | `chaika` _chaika_ (Yacht, HP=25000)<br>`hetman` _Hetman_ (Heavy cavalry, HP=320)<br>`cossackregister` _Register Cossack_ (Heavy cavalry, HP=250)<br>`cossacksich` _Sich Cossack_ (Light cavalry, HP=250)<br>`serdiuk` _Serdiuk_ (Rifleman, HP=85)<br>`peaukr` _Peasant_ (Peasant, HP=75) |

**No unique non-mercenary units:** **ven** Venice - use only the general roster.

<a id="4-стат-аномалии-на-одинаковых-юнитах"></a>
## §4. Stat anomalies on “identical” units

The same unit class (`usage_short`) may have different HP/damage/armor among different nations - these are hidden balance differences. Here are categories where the spread of HP between nations is ≥ 20%.

| Class | Min HP (nation · sid) | Max HP (nation · sid) | Scatter |
| --- | --- | --- | ---: |
| Archer | **alg** Algeria · `archer` (40) | **tur** Turkey · `tatar` (185) | +362% |
| Light Infantry | **alg** Algeria · `drummertur` (50) | **sco** Scotland · `swordsmansco` (180) | +260% |
| Cannon | **sco** Scotland · `framegun` (3000) | **ven** Venice · `cannon` (9000) | +200% |
| Shooter | **por** Portugal · `jagerpor` (50) | **eng** England · `highlander` (130) | +160% |
| Horse Rifleman | **fra** France · `dragoon18fra` (140) | **net** Netherlands · `dragoon18net` (320) | +129% |
| Heavy Cavalry | **pol** Poland · `reiterpol` (190) | **eng** Russia · `vityaz` (380) | +100% |
| Yacht | **ukr** Ukraine · `chaika` (25000) | **tur** Turkey · `yachttur` (35000) | +40% |
| Frigate | **aus** Austria · `frigate` (50000) | **tur** Turkey · `xebec` (65000) | +30% |
| Grenadier | **sax** Saxony · `grenadiersax` (100) | **pru** Prussia · `grenadierpru` (125) | +25% |
| Light Cavalry | **pol** Poland · `wingedhussar` (225) | **sco** Scotland · `raidersco` (280) | +24% |

<a id="5-доступные-наёмники-через-дипломатический-центр"></a>
## §5. Available mercenaries (via diplomatic center)

Units trained in `<nat>dip` (Diplomatic Center). Most have the suffix `dip` to `sid`. The cost is only gold (without food/wood/stone), they train without barracks prerequisites. All mercenaries consume gold-upkeep (`consume.gold > 0`); units with the flag `bmercenary=True` (in the current balance only `battleship`) are subject to Rebellion at `gold=0` (see [01_economy/README.md](../../reference/01_economy/README.md#famine-голод-и-rebellion-восстание)).

| `sid` | Class | HP | Max. damage | Merc? | Nations |
| --- | --- | ---: | ---: | :---: | --- |
| `archerdip` | Archer | 20 | 100 | ✅ | all 21 nations |
| `archerturdip` | Archer | 20 | 100 | ✅ | all 21 nations |
| `grenadierdip` | Grenadier | 30 | 200 | ✅ | all 21 nations |
| `cossacksichdip` | Light Cavalry | 150 | 8 | ✅ | all 21 nations |
| `lightinfantrydip` | Light Infantry | 50 | 16 | ✅ | all 21 nations |
| `roundshierdip` | Light Infantry | 75 | 6 | ✅ | all 21 nations |
| `dragoon18dip` | Shooter | 100 | 18 | ✅ | all 21 nations |
| `lightcavalrydip` | Shooter | 100 | 18 | ✅ | all 21 nations |

<a id="6-вариант-рынка"></a>
## §6. Market option
Market - common building (see [03_buildings/README.md → mar](../../reference/03_buildings/README.md#mar--market)). For 21 nations there are 4 building options (`eurmar` / `rusmar` / `spamar` / `turmar`), differing in HP, price and construction time. These are **building options only** - market rates are global and the same for all players in the match, regardless of which `mar` is built (see [06_market/README.md](../../reference/06_market/README.md#курсы--глобальные-их-видят-все-игроки)).

| Cluster | Nations |
| --- | --- |
| `eurmar` | **aus** Austria, **bav** Bavaria, **den** Denmark, **eng** England, **fra** France, **hun** Hungary, **net** Netherlands, **pie** Piedmont, **pol** Poland, **pru** Prussia, **sax** Saxony, **sco** Scotland, **swe** Sweden, **swi** Switzerland, **ven** Venice |
| `rusmar` | **rus** Russia, **ukr** Ukraine |
| `spamar` | **por** Portugal, **spa** Spain |
| `turmar` | **alg** Algeria, **tur** Turkey |
