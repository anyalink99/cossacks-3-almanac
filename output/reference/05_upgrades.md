# 05. Апгрейды

[← Index](README.md)

Апгрейды сгруппированы по **месту** (academy/blacksmith/mill/stable/barracks/mine/tower/wall/...). Каждый апгрейд — `<nat><place>.<unit>.<itype>.<level>` (per-unit, в кузнице/конюшне/казарме), `<nat><place>.<level>` (один на нацию, в академии/мельнице/town hall), или `<cluster><place>.<level>` (общие для кластера: tower/wall/shipyard).

`itype_short` колонка декодирует raw `gc_upg_type_*` в человеческие термины.

## Содержание

- [Mine upgrades (eurgol/eurcoa/euriro)](#mine-upgrades-eurgoleurcoaeuriro)
- [aca — Academy (research)](#aca-—-academy-research)
- [bla — Blacksmith (per-unit damage/protection)](#bla-—-blacksmith-per-unit-damageprotection)
- [sta — Stable (cavalry per-unit)](#sta-—-stable-cavalry-per-unit)
- [bar — Barracks 17c (per-unit upgrades)](#bar-—-barracks-17c-per-unit-upgrades)
- [ba2 — Barracks 18c (per-unit upgrades)](#ba2-—-barracks-18c-per-unit-upgrades)
- [art — Artillery Depot (cannon upgrades)](#art-—-artillery-depot-cannon-upgrades)
- [cen — Town Hall (era transition)](#cen-—-town-hall-era-transition)
- [tow — Tower (reload speed)](#tow-—-tower-reload-speed)
- [swa — Stone Wall (build gate)](#swa-—-stone-wall-build-gate)
- [wwa — Palisade (build gate)](#wwa-—-palisade-build-gate)
- [por — Shipyard (healing)](#por-—-shipyard-healing)
- [ferry — Ferry (capacity)](#ferry-—-ferry-capacity)

## Mine upgrades (eurgol/eurcoa/euriro)

Универсальные для всех наций (sid не зависит от нации). 6 уровней × 3 типа шахты.

| Апгрейд | level | +workers | F | G |
|---|---:|---:|---:|---:|
| `eurcoa.1` | 2 | +5 | 1000 | 1250 |
| `eurcoa.2` | 3 | +8 | 5250 | 4950 |
| `eurcoa.3` | 4 | +10 | 12500 | 9250 |
| `eurcoa.4` | 5 | +12 | 15800 | 18500 |
| `eurcoa.5` | 6 | +15 | 19800 | 21050 |
| `eurcoa.6` | 7 | +40 | 50200 | 25950 |
| `eurgol.1` | 2 | +5 | 1000 | 1250 |
| `eurgol.2` | 3 | +8 | 5250 | 4950 |
| `eurgol.3` | 4 | +10 | 12500 | 9250 |
| `eurgol.4` | 5 | +12 | 15800 | 18500 |
| `eurgol.5` | 6 | +15 | 19800 | 21050 |
| `eurgol.6` | 7 | +40 | 50200 | 25950 |
| `euriro.1` | 2 | +5 | 1000 | 1250 |
| `euriro.2` | 3 | +8 | 5250 | 4950 |
| `euriro.3` | 4 | +10 | 12500 | 9250 |
| `euriro.4` | 5 | +12 | 15800 | 18500 |
| `euriro.5` | 6 | +15 | 19800 | 21050 |
| `euriro.6` | 7 | +40 | 50200 | 25950 |

## aca — Academy (research)

Каждая запись — одна нация. Если значение одинаковое для всех 21 нации, показано одной строкой с `nation=all`. Если есть per-nation override (через `_country_ModifyUpgrade`), показаны отдельно.

| Апгрейд | nations | itype | val | F | W | S | G | I | C | time |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| **Cultivate new cultures of wheat (harvesting +40%)** `ausaca.1` | all | +food eff % | 40 | 0 | 200 | 0 | 325 | 0 | 0 | 15.62 |
| **Cultivate new cultures of wheat (harvesting +40%)** `fraaca.1` | fra | +food eff % | 40 | 0 | 190 | 0 | 315 | 0 | 0 | 15.62 |
| **Raise builders' salary (building construction time -75%)** `ausaca.10` | all | build time % | -7500000 | 0 | 0 | 0 | 6950 | 0 | 0 | 15.62 |
| **Raise builders' salary (building construction time -75%)** `ukraca.10` | ukr | build time % | -7500000 | 0 | 0 | 0 | 1750 | 0 | 0 | 15.62 |
| **Raise builders' salary (building construction time -75%)** `scoaca.10` | sco | build time % | -7500000 | 0 | 0 | 0 | 2650 | 0 | 0 | 15.62 |
| **Research new fortification grades (durability of walls and towers +80)** `ausaca.11` | aus,bav,den,eng,hun,net,pie,pol,por,pru,rus,sax,sco,spa,swi,ven | +shield | 80 | 0 | 0 | 16200 | 1500 | 0 | 0 | 15.62 |
| **Research new fortification grades (durability of walls and towers +80)** `turaca.11` | alg,tur | +shield | 80 | 0 | 16200 | 0 | 1500 | 0 | 0 | 15.62 |
| **Research new fortification grades (durability of walls and towers +80)** `fraaca.11` | fra | +shield | 80 | 0 | 0 | 16200 | 500 | 0 | 0 | 15.62 |
| **Research new fortification grades (durability of walls and towers +80)** `sweaca.11` | swe | +shield | 80 | 0 | 12200 | 16200 | 1100 | 0 | 0 | 15.62 |
| **Research new fortification grades %color(FFAA00)%(durability of walls and towers +80)** `ukraca.11` | ukr | — | — | — | — | — | — | — | — | — |
| **Improve firearms: rifled barrel (fire power +10%)** `ausaca.12` | all | +damage % | 10 | 0 | 0 | 0 | 0 | 5000 | 0 | 15.62 |
| **Improve firearms: rifled barrel %color(FFAA00)%(fire power +10%)** `algaca.12` | alg | — | — | — | — | — | — | — | — | — |
| **Research granular gunpowder (fire power +10%)** `ausaca.13` | all | +damage % | 10 | 0 | 0 | 0 | 4000 | 0 | 0 | 15.62 |
| **Research granular gunpowder %color(FFAA00)%(fire power +10%)** `algaca.13` | alg | — | — | — | — | — | — | — | — | — |
| **Research new sulphur purification methods (fire power +15%)** `ausaca.14` | all | +damage % | 15 | 0 | 0 | 0 | 7000 | 0 | 0 | 15.62 |
| **Research new sulphur purification methods %color(FFAA00)%(fire power +15%)** `algaca.14` | alg | — | — | — | — | — | — | — | — | — |
| **Research new nitre purification methods (fire power +25%)** `ausaca.15` | all | +damage % | 25 | 0 | 0 | 0 | 0 | 0 | 11000 | 15.62 |
| **Research new nitre purification methods %color(FFAA00)%(fire power +25%)** `algaca.15` | alg | — | — | — | — | — | — | — | — | — |
| **Research improved additions to gunpowder formula (artillery range +5%)** `ausaca.16` | all | range % | 5 | 0 | 0 | 0 | 2000 | 12150 | 0 | 15.62 |
| **Research improved additions to gunpowder formula (artillery range +5%)** `turaca.16` | alg,tur | range % | 5 | 0 | 0 | 0 | 2000 | 0 | 0 | 15.62 |
| **Design new barrel types: unicorn, carronade (artillery range +10%)** `ausaca.17` | all | range % | 10 | 0 | 0 | 3000 | 4550 | 19200 | 0 | 15.62 |
| **Design new barrel types: unicorn, carronade (artillery range +10%)** `turaca.17` | alg,tur | range % | 10 | 0 | 0 | 3000 | 4550 | 0 | 0 | 15.62 |
| **Design more durable gun carriage: Gribovalle system (artillery durability +50%)** `ausaca.18` | all | HP % | 50 | 0 | 0 | 0 | 500 | 3830 | 1500 | 15.62 |
| **Design multi-barrelled cannon** `ausaca.19` | aus,bav,den,eng,fra,hun,net,pie,pol,por,pru,rus,sax,spa,swe,swi,ven | enable unit | 0 | 0 | 0 | 0 | 1500 | 0 | 2500 | 15.62 |
| **%color(FFAA00)%Design multi-barrelled cannon** `ukraca.19` | alg,sco,tur,ukr | — | — | — | — | — | — | — | — | — |
| **Cultivate new cultures of rye (harvesting +50%)** `ausaca.2` | all | +food eff % | 50 | 0 | 2400 | 0 | 625 | 0 | 0 | 15.62 |
| **Cultivate new cultures of rye (harvesting +50%)** `turaca.2` | alg,tur | +food eff % | 50 | 0 | 400 | 0 | 522 | 0 | 0 | 15.62 |
| **Research new sighting devices for artillery (artillery accuracy +35%)** `ausaca.20` | all | accuracy % | -35 | 0 | 3540 | 0 | 2000 | 0 | 7250 | 15.62 |
| **Research new sighting devices for artillery (artillery accuracy +35%)** `fraaca.20` | fra | accuracy % | -35 | 0 | 13540 | 0 | 1500 | 0 | 5950 | 15.62 |
| **Research new sighting devices for artillery (artillery accuracy +35%)** `pruaca.20` | pru | accuracy % | -35 | 0 | 23540 | 0 | 1900 | 0 | 4250 | 15.62 |
| **Finance artillery repair shops (repair all artillery)** `ausaca.21` | all | healing | 25 | 0 | 350 | 0 | 100 | 0 | 250 | 15.62 |
| **Develop geology (previously hidden deposits appear on the map)** `ausaca.22` | all | geology | 0 | 0 | 0 | 0 | 250 | 0 | 0 | 15.62 |
| **Develop mining (stone excavation efficiency +100%)** `ausaca.23` | all | +stone eff % | 100 | 0 | 0 | 0 | 1550 | 3000 | 0 | 15.62 |
| **Raise miners' salary (stone excavation efficiency +200%)** `ausaca.24` | all | +stone eff % | 200 | 4200 | 0 | 0 | 1550 | 0 | 12520 | 15.62 |
| **Design Montgolfier (reveals the whole map)** `ausaca.25` | aus,bav,den,eng,fra,hun,net,pie,pol,por,pru,rus,sax,spa,swe,swi,ven | balloon | 0 | 0 | 0 | 0 | 5750 | 0 | 0 | 15.62 |
| **Design Montgolfier (reveals the whole map)** `ukraca.25` | sco,ukr | balloon | 0 | 0 | 0 | 0 | 12750 | 0 | 0 | 15.62 |
| **Design Montgolfier %color(FFAA00)%(reveals the whole map)** `turaca.25` | alg,tur | — | — | — | — | — | — | — | — | — |
| **Develop medical science (heals all live units)** `ausaca.26` | all | healing | 50 | 0 | 0 | 0 | 200 | 0 | 200 | 31.25 |
| **Develop mathematics (artillery accuracy +35%)** `ausaca.27` | all | accuracy % | -35 | 0 | 9540 | 0 | 12000 | 0 | 65200 | 15.62 |
| **Develop mathematics (artillery accuracy +35%)** `fraaca.27` | fra | accuracy % | -35 | 0 | 23580 | 0 | 9800 | 0 | 65400 | 15.62 |
| **Develop mathematics (artillery accuracy +35%)** `pruaca.27` | pru | accuracy % | -35 | 0 | 12540 | 0 | 8500 | 0 | 57200 | 15.62 |
| **Design new rigging types (ship speed +40%)** `ausaca.28` | aus,bav,den,fra,hun,net,pie,pol,por,pru,rus,sax,sco,spa,swe,swi,ven | speed % | 40 | 0 | 65400 | 0 | 24050 | 0 | 0 | 15.62 |
| **Design new rigging types (ship speed +40%)** `turaca.28` | alg,tur | speed % | 40 | 0 | 0 | 0 | 1900 | 0 | 0 | 15.62 |
| **Design new rigging types (ship speed +40%)** `engaca.28` | eng | speed % | 40 | 0 | 53400 | 0 | 22050 | 0 | 0 | 15.62 |
| **Design new rigging types (ship speed +40%)** `ukraca.28` | ukr | speed % | 40 | 0 | 0 | 0 | 900 | 0 | 0 | 15.62 |
| **Design new rib system and new hulls (battleship construction)** `ausaca.29` | all | enable unit | 0 | 0 | 32300 | 0 | 6800 | 9000 | 12800 | 15.62 |
| **Design new rib system and new hulls (battleship construction)** `engaca.29` | eng | enable unit | 0 | 0 | 22300 | 0 | 6800 | 7500 | 13200 | 15.62 |
| **Design new rib system and new hulls %color(FFAA00)%(battleship construction)** `ukraca.29` | ukr | — | — | — | — | — | — | — | — | — |
| **Raise agriculturists' salary (harvesting +50%)** `ausaca.3` | all | +food eff % | 50 | 0 | 3600 | 0 | 850 | 0 | 0 | 15.62 |
| **Raise agriculturists' salary (harvesting +50%)** `turaca.3` | tur | +food eff % | 50 | 0 | 2400 | 0 | 850 | 0 | 0 | 15.62 |
| **Raise agriculturists' salary (harvesting +50%)** `algaca.3` | alg | +food eff % | 50 | 0 | 1240 | 0 | 850 | 0 | 0 | 15.62 |
| **Train carpenters (shipbuilding speed x10)** `ausaca.30` | all | build time % | -5000000 | 0 | 2300 | 42700 | 1150 | 0 | 0 | 15.62 |
| **Train carpenters (shipbuilding speed x10)** `turaca.30` | alg,tur | build time % | -5000000 | 0 | 0 | 42700 | 0 | 0 | 0 | 15.62 |
| **Design wheellock (rate of fire +30%)** `ausaca.31` | all | reload % | -30 | 0 | 0 | 6000 | 5500 | 4200 | 0 | 15.62 |
| **Design wheellock %color(FFAA00)%(rate of fire +30%)** `algaca.31` | alg | — | — | — | — | — | — | — | — | — |
| **Design flintlock (musket cost -50%)** `ausaca.32` | all | price % | 0 | 0 | 0 | 0 | 6050 | 0 | 7750 | 15.62 |
| **Design flintlock %color(FFAA00)%(musket cost -50%)** `ukraca.32` | alg,tur,ukr | — | — | — | — | — | — | — | — | — |
| **Design paper cartridge and iron ramrod (rate of fire +30%)** `ausaca.33` | all | reload % | -30 | 0 | 5000 | 0 | 5500 | 0 | 15200 | 15.62 |
| **Design paper cartridge and iron ramrod %color(FFAA00)%(rate of fire +30%)** `algaca.33` | alg | — | — | — | — | — | — | — | — | — |
| **Research improved steel grades for cuirasses (armoured soldier defence +2)** `ausaca.34` | all | +shield | 2 | 0 | 0 | 0 | 9750 | 0 | 0 | 15.62 |
| **Research improved steel grades for cuirasses %color(FFAA00)%(armoured soldier defence +2)** `ukraca.34` | alg,ukr | — | — | — | — | — | — | — | — | — |
| **Research improved steel grades for cuirasses (armoured soldier defence +2)** `turaca.34` | tur | +shield | 2 | 0 | 0 | 0 | 6950 | 0 | 0 | 15.62 |
| **Design bayonet: barrel-inserted, bayonet with a tube (cold steel weapons +5)** `ausaca.35` | all | +damage | 5 | 0 | 0 | 0 | 11500 | 0 | 0 | 15.62 |
| **Design bayonet: barrel-inserted, bayonet with a tube %color(FFAA00)%(cold steel weapons +5)** `ukraca.35` | alg,tur,ukr | — | — | — | — | — | — | — | — | — |
| **Research new steel grades (18c musketeer/grenadier melee attack efficiency +25%)** `ausaca.36` | all | +damage % | 25 | 0 | 0 | 0 | 19500 | 0 | 0 | 15.62 |
| **Research new steel grades %color(FFAA00)%(18c musketeer/grenadier melee attack efficiency +25%)** `ukraca.36` | alg,tur,ukr | — | — | — | — | — | — | — | — | — |
| **Carry out field melioration (field capacity +200%)** `ausaca.4` | all | +field HP % | 200 | 0 | 1000 | 0 | 475 | 0 | 0 | 15.62 |
| **Carry out field melioration (field capacity +200%)** `algaca.4` | alg | +field HP % | 200 | 0 | 700 | 0 | 475 | 0 | 0 | 15.62 |
| **Design new tackle and fishing nets (boat efficiency +100%)** `ausaca.5` | all | +fish eff % | 100 | 0 | 12400 | 0 | 2520 | 0 | 0 | 15.62 |
| **Design new tackle and fishing nets (boat efficiency +100%)** `fraaca.5` | fra | +fish eff % | 100 | 0 | 13900 | 0 | 2420 | 0 | 0 | 15.62 |
| **Design new tackle and fishing nets (boat efficiency +100%)** `engaca.5` | eng | +fish eff % | 100 | 0 | 12400 | 0 | 3520 | 0 | 0 | 15.62 |
| **Develop new woodworking methods (frigate building)** `ausaca.6` | aus,bav,den,eng,hun,net,pie,pol,por,pru,rus,sax,sco,spa,swe,swi,ven | enable unit | 0 | 0 | 12400 | 0 | 7040 | 0 | 0 | 15.62 |
| **Develop new woodworking methods (xebec building)** `turaca.6` | alg,tur | enable unit | 0 | 0 | 9500 | 0 | 7040 | 0 | 0 | 15.62 |
| **Develop new woodworking methods (frigate building)** `fraaca.6` | fra | enable unit | 0 | 0 | 13500 | 0 | 7250 | 0 | 0 | 15.62 |
| **Develop new woodworking methods %color(FFAA00)%(frigate building)** `ukraca.6` | ukr | — | — | — | — | — | — | — | — | — |
| **Build new shipyards for fishing boats (fishing boat cost -85%)** `ausaca.7` | all | price % | 0 | 0 | 7300 | 0 | 1220 | 0 | 0 | 15.62 |
| **Build new shipyards for fishing boats (fishing boat cost -85%)** `fraaca.7` | fra | price % | 0 | 0 | 7800 | 0 | 1110 | 0 | 0 | 15.62 |
| **Design new woodworking tools (woodcutting efficiency +100%)** `ausaca.8` | all | +wood eff % | 100 | 5500 | 0 | 0 | 550 | 0 | 0 | 15.62 |
| **Use new construction materials (durability of buildings +85)** `ausaca.9` | all | +shield | 85 | 0 | 9400 | 7850 | 1150 | 0 | 0 | 15.62 |
| **Use new construction materials (durability of buildings +85)** `turaca.9` | alg,tur | +shield | 85 | 0 | 9400 | 0 | 1150 | 0 | 0 | 15.62 |
| **Use new construction materials (durability of buildings +85)** `ukraca.9` | ukr | +shield | 85 | 0 | 3200 | 7850 | 950 | 0 | 0 | 15.62 |

## bla — Blacksmith (per-unit damage/protection)

Каждая запись — одна нация. Если значение одинаковое для всех 21 нации, показано одной строкой с `nation=all`. Если есть per-nation override (через `_country_ModifyUpgrade`), показаны отдельно.

| Апгрейд | nations | itype | val | F | W | S | G | I | C | time |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| **Manufacture agricultural equipment (field capacity +100%)** `ausbla.1` | all | +field HP % | 100 | 0 | 400 | 0 | 90 | 0 | 0 | 15.62 |
| **Forge metal armature and gratings (building defence +50)** `ausbla.2` | all | +shield | 50 | 0 | 0 | 12320 | 350 | 900 | 0 | 15.62 |
| **Forge harnesses for horses (mounted units recruitment speed -33%)** `ausbla.3` | all | build time % | -3333333 | 0 | 0 | 0 | 3650 | 5300 | 8200 | 15.62 |
| **Forge harnesses for horses (mounted units recruitment speed -33%)** `engbla.3` | eng | build time % | -3333333 | 0 | 0 | 0 | 3550 | 4100 | 6700 | 15.62 |
| **Forge harnesses for horses (mounted units recruitment speed -33%)** `prubla.3` | pru | build time % | -3333333 | 0 | 0 | 0 | 3650 | 4300 | 5200 | 15.62 |
| **Forge harnesses for horses (mounted units recruitment speed -33%)** `venbla.3` | ven | build time % | -3333333 | 0 | 0 | 0 | 650 | 9800 | 530 | 15.62 |
| **Forge bayonets and broadswords for infantry (18c musketeer/grenadier melee attack +5)** `ausbla.4` | all | +damage | 5 | 0 | 1300 | 0 | 1500 | 900 | 5000 | 15.62 |
| **Forge bayonets and broadswords for infantry %color(FFAA00)%(18c musketeer/grenadier melee attack +5)** `ukrbla.4` | alg,tur,ukr | — | — | — | — | — | — | — | — | — |
| **Forge new types of broadswords and sabres (cavalry and sword clansman attack +5)** `ausbla.5` | all | +damage | 5 | 0 | 0 | 0 | 4000 | 7900 | 0 | 15.62 |
| **Forge new types of broadswords and sabres (cavalry and sword clansman attack +5)** `engbla.5` | eng | +damage | 5 | 0 | 0 | 0 | 6550 | 7900 | 0 | 15.62 |
| **Forge new types of broadswords and sabres (cavalry and sword clansman attack +5)** `prubla.5` | pru | +damage | 5 | 0 | 0 | 0 | 9550 | 7900 | 0 | 15.62 |
| **Forge new cuirasses (armoured soldiers defence +2)** `ausbla.6` | all | +shield | 2 | 0 | 0 | 0 | 4950 | 10500 | 0 | 15.62 |
| **Forge new cuirasses %color(FFAA00)%(armoured soldiers defence +2)** `ukrbla.6` | alg,ukr | — | — | — | — | — | — | — | — | — |
| **Forge new cuirasses (armoured soldiers defence +2)** `turbla.6` | tur | +shield | 2 | 0 | 0 | 0 | 4950 | 10200 | 0 | 15.62 |

## sta — Stable (cavalry per-unit)

Каждая запись — одна нация. Если значение одинаковое для всех 21 нации, показано одной строкой с `nation=all`. Если есть per-nation override (через `_country_ModifyUpgrade`), показаны отдельно.

| Апгрейд | nations | itype | val | F | W | S | G | I | C | time |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `tursta.1` | tur | +food eff % | 140 | 600 | 0 | 0 | 250 | 0 | 0 | 15.62 |
| **Stable cossackdon protection +1 (lvl 2)** `russta.cossackdon.2.1` | rus | protection | 1 | 2000 | 0 | 0 | 1350 | 0 | 0 | 15.62 |
| **Stable cossackdon protection +1 (lvl 3)** `russta.cossackdon.2.2` | rus | protection | 1 | 1500 | 0 | 0 | 2100 | 0 | 0 | 15.62 |
| **Stable cossackdon protection +1 (lvl 4)** `russta.cossackdon.2.3` | rus | protection | 1 | 5000 | 0 | 0 | 3300 | 0 | 0 | 15.62 |
| **Stable cossackdon protection +1 (lvl 5)** `russta.cossackdon.2.4` | rus | protection | 1 | 10500 | 0 | 0 | 4400 | 0 | 0 | 15.62 |
| **Stable cossackdon protection +2 (lvl 6)** `russta.cossackdon.2.5` | rus | protection | 2 | 12600 | 0 | 0 | 5500 | 0 | 0 | 15.62 |
| **Stable cossackdon protection +2 (lvl 7)** `russta.cossackdon.2.6` | rus | protection | 2 | 40000 | 0 | 0 | 6000 | 0 | 0 | 15.62 |
| **Stable cossackregister protection +2 (lvl 2)** `ukrsta.cossackregister.2.1` | ukr | protection | 2 | 200 | 0 | 0 | 135 | 3000 | 0 | 15.62 |
| **Stable cossackregister protection +2 (lvl 3)** `ukrsta.cossackregister.2.2` | ukr | protection | 2 | 2000 | 0 | 0 | 100 | 5000 | 0 | 15.62 |
| **Stable cossackregister protection +2 (lvl 4)** `ukrsta.cossackregister.2.3` | ukr | protection | 2 | 65000 | 0 | 0 | 200 | 10000 | 0 | 15.62 |
| **Stable cossackregister protection +2 (lvl 5)** `ukrsta.cossackregister.2.4` | ukr | protection | 2 | 65000 | 0 | 0 | 300 | 4000 | 0 | 15.62 |
| **Stable cossackregister protection +2 (lvl 6)** `ukrsta.cossackregister.2.5` | ukr | protection | 2 | 65000 | 0 | 0 | 350 | 20000 | 0 | 15.62 |
| **Stable cossackregister protection +2 (lvl 7)** `ukrsta.cossackregister.2.6` | ukr | protection | 2 | 65000 | 0 | 0 | 1000 | 30000 | 0 | 15.62 |
| **Stable cossacksich protection +2 (lvl 2)** `ukrsta.cossacksich.2.1` | ukr | protection | 2 | 200 | 0 | 0 | 135 | 3000 | 0 | 15.62 |
| **Stable cossacksich protection +2 (lvl 3)** `ukrsta.cossacksich.2.2` | ukr | protection | 2 | 2000 | 0 | 0 | 100 | 5000 | 0 | 15.62 |
| **Stable cossacksich protection +2 (lvl 4)** `ukrsta.cossacksich.2.3` | ukr | protection | 2 | 44930 | 0 | 0 | 200 | 10000 | 0 | 15.62 |
| **Stable cossacksich protection +2 (lvl 5)** `ukrsta.cossacksich.2.4` | ukr | protection | 2 | 44930 | 0 | 0 | 300 | 4000 | 0 | 15.62 |
| **Stable cossacksich protection +2 (lvl 6)** `ukrsta.cossacksich.2.5` | ukr | protection | 2 | 44930 | 0 | 0 | 350 | 20000 | 0 | 15.62 |
| **Stable cossacksich protection +2 (lvl 7)** `ukrsta.cossacksich.2.6` | ukr | protection | 2 | 44930 | 0 | 0 | 1000 | 30000 | 0 | 15.62 |
| **Stable croat protection +1 (lvl 2)** `aussta.croat.2.1` | aus | protection | 1 | 2000 | 0 | 0 | 1350 | 0 | 0 | 15.62 |
| **Stable croat protection +1 (lvl 3)** `aussta.croat.2.2` | aus | protection | 1 | 1500 | 0 | 0 | 2100 | 0 | 0 | 15.62 |
| **Stable croat protection +2 (lvl 4)** `aussta.croat.2.3` | aus | protection | 2 | 5000 | 0 | 0 | 2300 | 0 | 0 | 15.62 |
| **Stable croat protection +2 (lvl 5)** `aussta.croat.2.4` | aus | protection | 2 | 10500 | 0 | 0 | 3400 | 0 | 0 | 15.62 |
| **Stable croat protection +3 (lvl 6)** `aussta.croat.2.5` | aus | protection | 3 | 12600 | 0 | 0 | 4500 | 0 | 0 | 15.62 |
| **Stable croat protection +3 (lvl 7)** `aussta.croat.2.6` | aus | protection | 3 | 40000 | 0 | 0 | 5000 | 0 | 0 | 15.62 |
| **Stable cuirassier damage +1 (lvl 2)** `aussta.cuirassier.1.1` | aus,pie,pol,rus,spa,swi,ven | damage | 1 | 12000 | 0 | 0 | 600 | 0 | 0 | 15.62 |
| **Stable cuirassier damage +1 (lvl 2)** `swesta.cuirassier.1.1` | bav,por,swe | damage | 1 | 11000 | 0 | 0 | 1600 | 0 | 0 | 15.62 |
| **Stable cuirassier damage +1 (lvl 2)** `prusta.cuirassier.1.1` | den,hun,pru | damage | 1 | 10000 | 0 | 0 | 200 | 0 | 0 | 15.62 |
| **Stable cuirassier damage +1 (lvl 2)** `frasta.cuirassier.1.1` | fra,net | damage | 1 | 32000 | 0 | 0 | 600 | 0 | 0 | 15.62 |
| **Stable cuirassier damage +1 (lvl 2)** `engsta.cuirassier.1.1` | eng | damage | 1 | 10000 | 0 | 0 | 900 | 0 | 0 | 15.62 |
| **Stable cuirassier damage +1 (lvl 3)** `aussta.cuirassier.1.2` | aus,pie,pol,rus,spa,swi,ven | damage | 1 | 32000 | 0 | 0 | 1300 | 0 | 0 | 15.62 |
| **Stable cuirassier damage +1 (lvl 3)** `swesta.cuirassier.1.2` | bav,por,swe | damage | 1 | 33000 | 0 | 0 | 300 | 0 | 0 | 15.62 |
| **Stable cuirassier damage +1 (lvl 3)** `prusta.cuirassier.1.2` | den,hun,pru | damage | 1 | 34000 | 0 | 0 | 1700 | 0 | 0 | 15.62 |
| **Stable cuirassier damage +1 (lvl 3)** `frasta.cuirassier.1.2` | fra | damage | 1 | 12000 | 0 | 0 | 2200 | 0 | 0 | 15.62 |
| **Stable cuirassier damage +1 (lvl 3)** `engsta.cuirassier.1.2` | eng | damage | 1 | 34000 | 0 | 0 | 1000 | 0 | 0 | 15.62 |
| **Stable cuirassier damage +1 (lvl 3)** `netsta.cuirassier.1.2` | net | damage | 1 | 12000 | 0 | 0 | 1300 | 0 | 0 | 15.62 |
| **Stable cuirassier damage +1 (lvl 4)** `aussta.cuirassier.1.3` | aus,pie,pol,rus,spa,swi,ven | damage | 1 | 62000 | 0 | 0 | 2200 | 0 | 0 | 15.62 |
| **Stable cuirassier damage +1 (lvl 4)** `swesta.cuirassier.1.3` | bav,por,swe | damage | 1 | 64000 | 0 | 0 | 3200 | 0 | 0 | 15.62 |
| **Stable cuirassier damage +1 (lvl 4)** `prusta.cuirassier.1.3` | den,hun,pru | damage | 1 | 64000 | 0 | 0 | 2100 | 0 | 0 | 15.62 |
| **Stable cuirassier damage +1 (lvl 4)** `frasta.cuirassier.1.3` | fra | damage | 1 | 62000 | 0 | 0 | 1300 | 0 | 0 | 15.62 |
| **Stable cuirassier damage +1 (lvl 4)** `engsta.cuirassier.1.3` | eng | damage | 1 | 42000 | 0 | 0 | 3200 | 0 | 0 | 15.62 |
| **Stable cuirassier damage +1 (lvl 4)** `netsta.cuirassier.1.3` | net | damage | 1 | 64000 | 0 | 0 | 2200 | 0 | 0 | 15.62 |
| **Stable cuirassier damage +2 (lvl 5)** `aussta.cuirassier.1.4` | aus,eng,pie,pol,rus,spa,swi,ven | damage | 2 | 61000 | 0 | 0 | 3150 | 0 | 0 | 15.62 |
| **Stable cuirassier damage +2 (lvl 5)** `swesta.cuirassier.1.4` | bav,por,swe | damage | 2 | 59000 | 0 | 0 | 2150 | 0 | 0 | 15.62 |
| **Stable cuirassier damage +2 (lvl 5)** `prusta.cuirassier.1.4` | den,hun,pru | damage | 2 | 58000 | 0 | 0 | 4150 | 0 | 0 | 15.62 |
| **Stable cuirassier damage +2 (lvl 5)** `frasta.cuirassier.1.4` | fra | damage | 2 | 57000 | 0 | 0 | 3150 | 0 | 0 | 15.62 |
| **Stable cuirassier damage +2 (lvl 5)** `netsta.cuirassier.1.4` | net | damage | 2 | 58000 | 0 | 0 | 3150 | 0 | 0 | 15.62 |
| **Stable cuirassier damage +2 (lvl 6)** `aussta.cuirassier.1.5` | aus,pie,pol,rus,spa,swi,ven | damage | 2 | 57055 | 0 | 0 | 4100 | 0 | 0 | 15.62 |
| **Stable cuirassier damage +2 (lvl 6)** `swesta.cuirassier.1.5` | bav,por,swe | damage | 2 | 52055 | 0 | 0 | 5100 | 0 | 0 | 15.62 |
| **Stable cuirassier damage +2 (lvl 6)** `prusta.cuirassier.1.5` | den,hun,pru | damage | 2 | 59055 | 0 | 0 | 3100 | 0 | 0 | 15.62 |
| **Stable cuirassier damage +2 (lvl 6)** `frasta.cuirassier.1.5` | fra | damage | 2 | 61055 | 0 | 0 | 8100 | 0 | 0 | 15.62 |
| **Stable cuirassier damage +2 (lvl 6)** `engsta.cuirassier.1.5` | eng | damage | 2 | 47055 | 0 | 0 | 4100 | 0 | 0 | 15.62 |
| **Stable cuirassier damage +2 (lvl 6)** `netsta.cuirassier.1.5` | net | damage | 2 | 59055 | 0 | 0 | 4100 | 0 | 0 | 15.62 |
| **Stable cuirassier damage +3 (lvl 7)** `aussta.cuirassier.1.6` | aus,pie,pol,rus,spa,swi,ven | damage | 3 | 49050 | 0 | 0 | 8020 | 0 | 0 | 15.62 |
| **Stable cuirassier damage +3 (lvl 7)** `swesta.cuirassier.1.6` | bav,por,swe | damage | 3 | 54050 | 0 | 0 | 7020 | 0 | 0 | 15.62 |
| **Stable cuirassier damage +3 (lvl 7)** `prusta.cuirassier.1.6` | den,hun,pru | damage | 3 | 47050 | 0 | 0 | 8150 | 0 | 0 | 15.62 |
| **Stable cuirassier damage +3 (lvl 7)** `frasta.cuirassier.1.6` | fra | damage | 3 | 47150 | 0 | 0 | 4020 | 0 | 0 | 15.62 |
| **Stable cuirassier damage +3 (lvl 7)** `engsta.cuirassier.1.6` | eng | damage | 3 | 59050 | 0 | 0 | 11020 | 0 | 0 | 15.62 |
| **Stable cuirassier damage +3 (lvl 7)** `netsta.cuirassier.1.6` | net | damage | 3 | 47050 | 0 | 0 | 8050 | 0 | 0 | 15.62 |
| **Stable cuirassier protection +2 (lvl 2)** `aussta.cuirassier.2.1` | aus,pie,pol,rus,spa,swi,ven | protection | 2 | 1760 | 0 | 0 | 350 | 1000 | 0 | 15.62 |
| **Stable cuirassier protection +2 (lvl 2)** `swesta.cuirassier.2.1` | bav,por,swe | protection | 2 | 2505 | 0 | 0 | 350 | 1000 | 0 | 15.62 |
| **Stable cuirassier protection +2 (lvl 2)** `prusta.cuirassier.2.1` | den,hun,pru | protection | 2 | 1520 | 0 | 0 | 450 | 1000 | 0 | 15.62 |
| **Stable cuirassier protection +2 (lvl 2)** `frasta.cuirassier.2.1` | fra | protection | 2 | 1520 | 0 | 0 | 750 | 1000 | 0 | 15.62 |
| **Stable cuirassier protection +2 (lvl 2)** `engsta.cuirassier.2.1` | eng | protection | 2 | 1260 | 0 | 0 | 350 | 200 | 0 | 15.62 |
| **Stable cuirassier protection +2 (lvl 2)** `netsta.cuirassier.2.1` | net | protection | 2 | 1250 | 0 | 0 | 450 | 1000 | 0 | 15.62 |
| **Stable cuirassier protection +3 (lvl 3)** `aussta.cuirassier.2.2` | aus,pie,pol,rus,spa,swi,ven | protection | 3 | 3000 | 0 | 0 | 750 | 2000 | 0 | 15.62 |
| **Stable cuirassier protection +3 (lvl 3)** `swesta.cuirassier.2.2` | bav,por,swe | protection | 3 | 2000 | 0 | 0 | 300 | 2000 | 0 | 15.62 |
| **Stable cuirassier protection +3 (lvl 3)** `prusta.cuirassier.2.2` | den,hun,pru | protection | 3 | 7000 | 0 | 0 | 750 | 2000 | 0 | 15.62 |
| **Stable cuirassier protection +3 (lvl 3)** `frasta.cuirassier.2.2` | fra | protection | 3 | 3200 | 0 | 0 | 350 | 1950 | 0 | 15.62 |
| **Stable cuirassier protection +3 (lvl 3)** `engsta.cuirassier.2.2` | eng | protection | 3 | 3500 | 0 | 0 | 750 | 2800 | 0 | 15.62 |
| **Stable cuirassier protection +3 (lvl 3)** `netsta.cuirassier.2.2` | net | protection | 3 | 2500 | 0 | 0 | 650 | 2000 | 0 | 15.62 |
| **Stable cuirassier protection +3 (lvl 4)** `aussta.cuirassier.2.3` | aus,pie,pol,rus,spa,swi,ven | protection | 3 | 7600 | 0 | 0 | 300 | 3030 | 0 | 15.62 |
| **Stable cuirassier protection +3 (lvl 4)** `swesta.cuirassier.2.3` | bav,por,swe | protection | 3 | 5600 | 0 | 0 | 750 | 3030 | 0 | 15.62 |
| **Stable cuirassier protection +3 (lvl 4)** `prusta.cuirassier.2.3` | den,hun,pru | protection | 3 | 3600 | 0 | 0 | 3300 | 3050 | 0 | 15.62 |
| **Stable cuirassier protection +3 (lvl 4)** `frasta.cuirassier.2.3` | fra | protection | 3 | 7600 | 0 | 0 | 300 | 3110 | 0 | 15.62 |
| **Stable cuirassier protection +3 (lvl 4)** `engsta.cuirassier.2.3` | eng | protection | 3 | 2600 | 0 | 0 | 900 | 2930 | 0 | 15.62 |
| **Stable cuirassier protection +3 (lvl 4)** `netsta.cuirassier.2.3` | net | protection | 3 | 4600 | 0 | 0 | 200 | 3050 | 0 | 15.62 |
| **Stable cuirassier protection +2 (lvl 5)** `aussta.cuirassier.2.4` | aus,pie,pol,rus,spa,swi,ven | protection | 2 | 8700 | 0 | 0 | 6200 | 100 | 0 | 15.62 |
| **Stable cuirassier protection +2 (lvl 5)** `swesta.cuirassier.2.4` | bav,por,swe | protection | 2 | 10700 | 0 | 0 | 6100 | 100 | 0 | 15.62 |
| **Stable cuirassier protection +2 (lvl 5)** `prusta.cuirassier.2.4` | den,hun,pru | protection | 2 | 8700 | 0 | 0 | 3200 | 200 | 0 | 15.62 |
| **Stable cuirassier protection +2 (lvl 5)** `frasta.cuirassier.2.4` | fra | protection | 2 | 6200 | 0 | 0 | 6200 | 100 | 0 | 15.62 |
| **Stable cuirassier protection +2 (lvl 5)** `engsta.cuirassier.2.4` | eng | protection | 2 | 12700 | 0 | 0 | 5600 | 200 | 0 | 15.62 |
| **Stable cuirassier protection +2 (lvl 5)** `netsta.cuirassier.2.4` | net | protection | 2 | 11700 | 0 | 0 | 6100 | 100 | 0 | 15.62 |
| **Stable cuirassier protection +1 (lvl 6)** `aussta.cuirassier.2.5` | aus,net,pie,pol,rus,spa,swi,ven | protection | 1 | 8700 | 0 | 0 | 2350 | 5000 | 0 | 15.62 |
| **Stable cuirassier protection +1 (lvl 6)** `swesta.cuirassier.2.5` | bav,por,swe | protection | 1 | 8100 | 0 | 0 | 2150 | 5000 | 0 | 15.62 |
| **Stable cuirassier protection +1 (lvl 6)** `prusta.cuirassier.2.5` | den,hun,pru | protection | 1 | 8700 | 0 | 0 | 2650 | 4300 | 0 | 15.62 |
| **Stable cuirassier protection +1 (lvl 6)** `frasta.cuirassier.2.5` | fra | protection | 1 | 11700 | 0 | 0 | 4450 | 7000 | 0 | 15.62 |
| **Stable cuirassier protection +1 (lvl 6)** `engsta.cuirassier.2.5` | eng | protection | 1 | 5700 | 0 | 0 | 1350 | 7000 | 0 | 15.62 |
| **Stable cuirassier protection +1 (lvl 7)** `aussta.cuirassier.2.6` | aus,net,pie,pol,rus,spa,swi,ven | protection | 1 | 9700 | 0 | 0 | 4444 | 7060 | 0 | 15.62 |
| **Stable cuirassier protection +1 (lvl 7)** `swesta.cuirassier.2.6` | bav,por,swe | protection | 1 | 9200 | 0 | 0 | 4900 | 7060 | 0 | 15.62 |
| **Stable cuirassier protection +1 (lvl 7)** `prusta.cuirassier.2.6` | den,hun,pru | protection | 1 | 11200 | 0 | 0 | 4700 | 6760 | 0 | 15.62 |
| **Stable cuirassier protection +1 (lvl 7)** `frasta.cuirassier.2.6` | fra | protection | 1 | 9700 | 0 | 0 | 3244 | 5060 | 0 | 15.62 |
| **Stable cuirassier protection +1 (lvl 7)** `engsta.cuirassier.2.6` | eng | protection | 1 | 12700 | 0 | 0 | 5424 | 5060 | 0 | 15.62 |
| **Stable dragoon damage +1 (lvl 2)** `aussta.dragoon.1.1` | aus,bav,fra,pie,por,spa,swe,swi,ven | damage | 1 | 500 | 0 | 0 | 150 | 0 | 0 | 15.62 |
| **Stable dragoon damage +1 (lvl 2)** `prusta.dragoon.1.1` | den,hun,net,pru,sax | damage | 1 | 700 | 0 | 0 | 250 | 0 | 0 | 15.62 |
| **Stable dragoon damage +1 (lvl 2)** `engsta.dragoon.1.1` | eng | damage | 1 | 400 | 0 | 0 | 150 | 0 | 0 | 15.62 |
| **Stable dragoon damage +1 (lvl 3)** `aussta.dragoon.1.2` | aus,bav,fra,pie,por,spa,swe,swi,ven | damage | 1 | 700 | 0 | 0 | 200 | 0 | 0 | 15.62 |
| **Stable dragoon damage +1 (lvl 3)** `prusta.dragoon.1.2` | den,hun,pru,sax | damage | 1 | 500 | 0 | 0 | 100 | 0 | 0 | 15.62 |
| **Stable dragoon damage +1 (lvl 3)** `engsta.dragoon.1.2` | eng | damage | 1 | 800 | 0 | 0 | 200 | 0 | 0 | 15.62 |
| **Stable dragoon damage +1 (lvl 3)** `netsta.dragoon.1.2` | net | damage | 1 | 600 | 0 | 0 | 100 | 0 | 0 | 15.62 |
| **Stable dragoon damage +2 (lvl 4)** `aussta.dragoon.1.3` | aus,bav,fra,pie,por,spa,swe,swi,ven | damage | 2 | 900 | 0 | 0 | 340 | 0 | 0 | 15.62 |
| **Stable dragoon damage +2 (lvl 4)** `prusta.dragoon.1.3` | den,hun,pru,sax | damage | 2 | 900 | 0 | 0 | 640 | 0 | 0 | 15.62 |
| **Stable dragoon damage +2 (lvl 4)** `engsta.dragoon.1.3` | eng | damage | 2 | 300 | 0 | 0 | 340 | 0 | 0 | 15.62 |
| **Stable dragoon damage +2 (lvl 4)** `netsta.dragoon.1.3` | net | damage | 2 | 800 | 0 | 0 | 540 | 0 | 0 | 15.62 |
| **Stable dragoon damage +1 (lvl 5)** `aussta.dragoon.1.4` | aus,bav,den,eng,fra,hun,net,pie,por,pru,sax,spa,swe,swi,ven | damage | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 15.62 |
| **Stable dragoon damage +1 (lvl 6)** `aussta.dragoon.1.5` | aus,bav,den,eng,fra,hun,net,pie,por,pru,sax,spa,swe,swi,ven | damage | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 15.62 |
| **Stable dragoon damage +3 (lvl 7)** `aussta.dragoon.1.6` | aus,bav,den,eng,fra,hun,net,pie,por,pru,sax,spa,swe,swi,ven | damage | 3 | 0 | 0 | 0 | 0 | 0 | 0 | 15.62 |
| **Stable dragoon protection +1 (lvl 2)** `aussta.dragoon.2.1` | aus,bav,fra,pie,por,spa,swe,swi,ven | protection | 1 | 900 | 0 | 0 | 150 | 0 | 0 | 15.62 |
| **Stable dragoon protection +1 (lvl 2)** `prusta.dragoon.2.1` | den,hun,pru,sax | protection | 1 | 500 | 0 | 0 | 250 | 0 | 0 | 15.62 |
| **Stable dragoon protection +1 (lvl 2)** `engsta.dragoon.2.1` | eng | protection | 1 | 1300 | 0 | 0 | 250 | 0 | 0 | 15.62 |
| **Stable dragoon protection +1 (lvl 2)** `netsta.dragoon.2.1` | net | protection | 1 | 400 | 0 | 0 | 250 | 0 | 0 | 15.62 |
| **Stable dragoon protection +2 (lvl 3)** `aussta.dragoon.2.2` | aus,bav,fra,pie,por,spa,swi,ven | protection | 2 | 6600 | 0 | 0 | 750 | 0 | 0 | 15.62 |
| **Stable dragoon protection +2 (lvl 3)** `prusta.dragoon.2.2` | den,hun,pru,sax | protection | 2 | 6300 | 0 | 0 | 850 | 0 | 0 | 15.62 |
| **Stable dragoon protection +2 (lvl 3)** `engsta.dragoon.2.2` | eng | protection | 2 | 5200 | 0 | 0 | 650 | 0 | 0 | 15.62 |
| **Stable dragoon protection +2 (lvl 3)** `swesta.dragoon.2.2` | swe | protection | 2 | 6600 | 0 | 0 | 650 | 0 | 0 | 15.62 |
| **Stable dragoon protection +2 (lvl 3)** `netsta.dragoon.2.2` | net | protection | 2 | 7600 | 0 | 0 | 550 | 0 | 0 | 15.62 |
| **Stable dragoon protection +2 (lvl 4)** `aussta.dragoon.2.3` | aus,bav,fra,pie,por,spa,swe,swi,ven | protection | 2 | 5000 | 0 | 0 | 1250 | 0 | 0 | 15.62 |
| **Stable dragoon protection +2 (lvl 4)** `prusta.dragoon.2.3` | den,hun,pru,sax | protection | 2 | 4600 | 0 | 0 | 1350 | 0 | 0 | 15.62 |
| **Stable dragoon protection +2 (lvl 4)** `engsta.dragoon.2.3` | eng | protection | 2 | 2000 | 0 | 0 | 1450 | 0 | 0 | 15.62 |
| **Stable dragoon protection +2 (lvl 4)** `netsta.dragoon.2.3` | net | protection | 2 | 4000 | 0 | 0 | 950 | 0 | 0 | 15.62 |
| **Stable dragoon protection +1 (lvl 5)** `aussta.dragoon.2.4` | aus,bav,fra,pie,spa,swe,swi,ven | protection | 1 | 3000 | 0 | 0 | 700 | 0 | 0 | 15.62 |
| **Stable dragoon protection +1 (lvl 5)** `prusta.dragoon.2.4` | den,pru,sax | protection | 1 | 2500 | 0 | 0 | 750 | 0 | 0 | 15.62 |
| **Stable dragoon protection +1 (lvl 5)** `engsta.dragoon.2.4` | eng | protection | 1 | 6000 | 0 | 0 | 100 | 0 | 0 | 15.62 |
| **Stable dragoon protection +1 (lvl 5)** `netsta.dragoon.2.4` | net | protection | 1 | 4000 | 0 | 0 | 900 | 0 | 0 | 15.62 |
| **Stable dragoon protection +1 (lvl 5)** `porsta.dragoon.2.4` | por | protection | 1 | 3000 | 0 | 0 | 600 | 0 | 0 | 15.62 |
| **Stable dragoon protection +1 (lvl 5)** `hunsta.dragoon.2.4` | hun | protection | 1 | 2500 | 0 | 0 | 700 | 0 | 0 | 15.62 |
| **Stable dragoon protection +2 (lvl 6)** `aussta.dragoon.2.5` | aus,bav,fra,pie,por,spa,swe,swi,ven | protection | 2 | 1000 | 0 | 0 | 2350 | 0 | 0 | 15.62 |
| **Stable dragoon protection +2 (lvl 6)** `prusta.dragoon.2.5` | den,hun,pru,sax | protection | 2 | 800 | 0 | 0 | 2750 | 0 | 0 | 15.62 |
| **Stable dragoon protection +2 (lvl 6)** `engsta.dragoon.2.5` | eng | protection | 2 | 1000 | 0 | 0 | 3250 | 0 | 0 | 15.62 |
| **Stable dragoon protection +2 (lvl 6)** `netsta.dragoon.2.5` | net | protection | 2 | 4000 | 0 | 0 | 2150 | 0 | 0 | 15.62 |
| **Stable dragoon protection +2 (lvl 7)** `spasta.dragoon.2.6` | bav,pie,por,spa,swe,swi,ven | protection | 2 | 6001 | 0 | 0 | 6000 | 0 | 0 | 15.62 |
| **Stable dragoon protection +2 (lvl 7)** `densta.dragoon.2.6` | den,hun,sax | protection | 2 | 2001 | 0 | 0 | 8200 | 0 | 0 | 15.62 |
| **Stable dragoon protection +2 (lvl 7)** `aussta.dragoon.2.6` | aus,fra | protection | 2 | 6001 | 0 | 0 | 5000 | 0 | 0 | 15.62 |
| **Stable dragoon protection +2 (lvl 7)** `engsta.dragoon.2.6` | eng | protection | 2 | 7001 | 0 | 0 | 4400 | 0 | 0 | 15.62 |
| **Stable dragoon protection +2 (lvl 7)** `prusta.dragoon.2.6` | pru | protection | 2 | 2001 | 0 | 0 | 7200 | 0 | 0 | 15.62 |
| **Stable dragoon protection +2 (lvl 7)** `netsta.dragoon.2.6` | net | protection | 2 | 3001 | 0 | 0 | 6200 | 0 | 0 | 15.62 |
| **Stable dragoon18 damage +2 (lvl 2)** `aussta.dragoon18.1.1` | aus,bav,pol,por,rus,spa,swe,swi,ven | damage | 2 | 2000 | 0 | 0 | 100 | 0 | 0 | 15.62 |
| **Stable dragoon18 damage +2 (lvl 2)** `prusta.dragoon18.1.1` | den,pru,sax | damage | 2 | 4500 | 0 | 0 | 200 | 0 | 0 | 15.62 |
| **Stable dragoon18 damage +2 (lvl 2)** `engsta.dragoon18.1.1` | eng | damage | 2 | 1000 | 0 | 0 | 200 | 0 | 0 | 15.62 |
| **Stable dragoon18 damage +2 (lvl 3)** `aussta.dragoon18.1.2` | aus,bav,pol,por,rus,spa,swe,swi,ven | damage | 2 | 9000 | 0 | 0 | 350 | 0 | 0 | 15.62 |
| **Stable dragoon18 damage +2 (lvl 3)** `prusta.dragoon18.1.2` | den,pru,sax | damage | 2 | 5500 | 0 | 0 | 250 | 0 | 0 | 15.62 |
| **Stable dragoon18 damage +2 (lvl 3)** `engsta.dragoon18.1.2` | eng | damage | 2 | 10200 | 0 | 0 | 250 | 0 | 0 | 15.62 |
| **Stable dragoon18 damage +4 (lvl 4)** `aussta.dragoon18.1.3` | aus,bav,pol,por,rus,spa,swe,swi,ven | damage | 4 | 12000 | 0 | 0 | 400 | 0 | 0 | 15.62 |
| **Stable dragoon18 damage +4 (lvl 4)** `prusta.dragoon18.1.3` | den,pru,sax | damage | 4 | 22000 | 0 | 0 | 500 | 0 | 0 | 15.62 |
| **Stable dragoon18 damage +4 (lvl 4)** `engsta.dragoon18.1.3` | eng | damage | 4 | 15200 | 0 | 0 | 200 | 0 | 0 | 15.62 |
| **Stable dragoon18 damage +2 (lvl 5)** `aussta.dragoon18.1.4` | aus,bav,pol,por,rus,spa,swe,swi,ven | damage | 2 | 23000 | 0 | 0 | 580 | 0 | 0 | 15.62 |
| **Stable dragoon18 damage +2 (lvl 5)** `prusta.dragoon18.1.4` | den,pru,sax | damage | 2 | 13000 | 0 | 0 | 480 | 0 | 0 | 15.62 |
| **Stable dragoon18 damage +2 (lvl 5)** `engsta.dragoon18.1.4` | eng | damage | 2 | 19850 | 0 | 0 | 280 | 0 | 0 | 15.62 |
| **Stable dragoon18 damage +2 (lvl 6)** `aussta.dragoon18.1.5` | aus,bav,pol,por,rus,spa,swe,swi,ven | damage | 2 | 32000 | 0 | 0 | 680 | 0 | 0 | 15.62 |
| **Stable dragoon18 damage +2 (lvl 6)** `prusta.dragoon18.1.5` | den,pru,sax | damage | 2 | 42000 | 0 | 0 | 780 | 0 | 0 | 15.62 |
| **Stable dragoon18 damage +2 (lvl 6)** `engsta.dragoon18.1.5` | eng | damage | 2 | 32000 | 0 | 0 | 1180 | 0 | 0 | 15.62 |
| **Stable dragoon18 damage +4 (lvl 7)** `aussta.dragoon18.1.6` | aus,bav,pol,por,rus,spa,swe,swi,ven | damage | 4 | 42000 | 0 | 0 | 780 | 0 | 0 | 15.62 |
| **Stable dragoon18 damage +4 (lvl 7)** `prusta.dragoon18.1.6` | den,pru,sax | damage | 4 | 32000 | 0 | 0 | 680 | 0 | 0 | 15.62 |
| **Stable dragoon18 damage +4 (lvl 7)** `engsta.dragoon18.1.6` | eng | damage | 4 | 32000 | 0 | 0 | 980 | 0 | 0 | 15.62 |
| **Stable dragoon18 protection +1 (lvl 2)** `aussta.dragoon18.2.1` | aus,pol,rus,spa,swi,ven | protection | 1 | 760 | 0 | 0 | 935 | 0 | 0 | 15.62 |
| **Stable dragoon18 protection +1 (lvl 2)** `swesta.dragoon18.2.1` | bav,por,swe | protection | 1 | 260 | 0 | 0 | 935 | 0 | 0 | 15.62 |
| **Stable dragoon18 protection +1 (lvl 2)** `prusta.dragoon18.2.1` | den,pru,sax | protection | 1 | 750 | 0 | 0 | 935 | 0 | 0 | 15.62 |
| **Stable dragoon18 protection +1 (lvl 2)** `engsta.dragoon18.2.1` | eng | protection | 1 | 250 | 0 | 0 | 999 | 0 | 0 | 15.62 |
| **Stable dragoon18 protection +1 (lvl 3)** `aussta.dragoon18.2.2` | aus,den,pol,pru,rus,sax,spa,swi,ven | protection | 1 | 1260 | 0 | 0 | 1150 | 0 | 0 | 15.62 |
| **Stable dragoon18 protection +1 (lvl 3)** `swesta.dragoon18.2.2` | bav,por,swe | protection | 1 | 1460 | 0 | 0 | 1150 | 0 | 0 | 15.62 |
| **Stable dragoon18 protection +1 (lvl 3)** `engsta.dragoon18.2.2` | eng | protection | 1 | 1360 | 0 | 0 | 1250 | 0 | 0 | 15.62 |
| **Stable dragoon18 protection +2 (lvl 4)** `aussta.dragoon18.2.3` | aus,pol,rus,spa,swi,ven | protection | 2 | 15600 | 0 | 0 | 2350 | 0 | 0 | 15.62 |
| **Stable dragoon18 protection +2 (lvl 4)** `swesta.dragoon18.2.3` | bav,por,swe | protection | 2 | 12600 | 0 | 0 | 3350 | 0 | 0 | 15.62 |
| **Stable dragoon18 protection +2 (lvl 4)** `prusta.dragoon18.2.3` | den,pru,sax | protection | 2 | 10600 | 0 | 0 | 2350 | 0 | 0 | 15.62 |
| **Stable dragoon18 protection +2 (lvl 4)** `engsta.dragoon18.2.3` | eng | protection | 2 | 17600 | 0 | 0 | 2150 | 0 | 0 | 15.62 |
| **Stable dragoon18 protection +1 (lvl 5)** `aussta.dragoon18.2.4` | aus,pol,rus,spa,swi,ven | protection | 1 | 17600 | 0 | 0 | 3350 | 0 | 0 | 15.62 |
| **Stable dragoon18 protection +1 (lvl 5)** `densta.dragoon18.2.4` | den,sax | protection | 1 | 22600 | 0 | 0 | 5350 | 0 | 0 | 15.62 |
| **Stable dragoon18 protection +1 (lvl 5)** `porsta.dragoon18.2.4` | bav,por | protection | 1 | 19600 | 0 | 0 | 3350 | 0 | 0 | 15.62 |
| **Stable dragoon18 protection +1 (lvl 5)** `engsta.dragoon18.2.4` | eng | protection | 1 | 15600 | 0 | 0 | 5350 | 0 | 0 | 15.62 |
| **Stable dragoon18 protection +1 (lvl 5)** `swesta.dragoon18.2.4` | swe | protection | 1 | 19600 | 0 | 0 | 2350 | 0 | 0 | 15.62 |
| **Stable dragoon18 protection +1 (lvl 5)** `prusta.dragoon18.2.4` | pru | protection | 1 | 22600 | 0 | 0 | 6350 | 0 | 0 | 15.62 |
| **Stable dragoon18 protection +2 (lvl 6)** `aussta.dragoon18.2.5` | aus,pol,rus,spa,swi,ven | protection | 2 | 19600 | 0 | 0 | 5350 | 0 | 0 | 15.62 |
| **Stable dragoon18 protection +2 (lvl 6)** `engsta.dragoon18.2.5` | den,eng,sax | protection | 2 | 19600 | 0 | 0 | 3350 | 0 | 0 | 15.62 |
| **Stable dragoon18 protection +2 (lvl 6)** `swesta.dragoon18.2.5` | bav,por,swe | protection | 2 | 12600 | 0 | 0 | 7350 | 0 | 0 | 15.62 |
| **Stable dragoon18 protection +2 (lvl 6)** `prusta.dragoon18.2.5` | pru | protection | 2 | 19600 | 0 | 0 | 4350 | 0 | 0 | 15.62 |
| **Stable dragoon18 protection +3 (lvl 7)** `aussta.dragoon18.2.6` | aus,pol,rus,spa,swi,ven | protection | 3 | 21760 | 0 | 0 | 9350 | 0 | 0 | 15.62 |
| **Stable dragoon18 protection +3 (lvl 7)** `prusta.dragoon18.2.6` | den,pru,sax | protection | 3 | 15760 | 0 | 0 | 9350 | 0 | 0 | 15.62 |
| **Stable dragoon18 protection +3 (lvl 7)** `swesta.dragoon18.2.6` | bav,swe | protection | 3 | 26760 | 0 | 0 | 7350 | 0 | 0 | 15.62 |
| **Stable dragoon18 protection +3 (lvl 7)** `engsta.dragoon18.2.6` | eng | protection | 3 | 25760 | 0 | 0 | 8350 | 0 | 0 | 15.62 |
| **Stable dragoon18 protection +3 (lvl 7)** `porsta.dragoon18.2.6` | por | protection | 3 | 26760 | 0 | 0 | 6350 | 0 | 0 | 15.62 |
| **Stable dragoon18fra damage +2 (lvl 2)** `frasta.dragoon18fra.1.1` | fra | damage | 2 | 2000 | 0 | 0 | 100 | 0 | 0 | 15.62 |
| **Stable dragoon18fra damage +2 (lvl 3)** `frasta.dragoon18fra.1.2` | fra | damage | 2 | 9000 | 0 | 0 | 350 | 0 | 0 | 15.62 |
| **Stable dragoon18fra damage +4 (lvl 4)** `frasta.dragoon18fra.1.3` | fra | damage | 4 | 12000 | 0 | 0 | 400 | 0 | 0 | 15.62 |
| **Stable dragoon18fra damage +2 (lvl 5)** `frasta.dragoon18fra.1.4` | fra | damage | 2 | 23000 | 0 | 0 | 580 | 0 | 0 | 15.62 |
| **Stable dragoon18fra damage +2 (lvl 6)** `frasta.dragoon18fra.1.5` | fra | damage | 2 | 32000 | 0 | 0 | 680 | 0 | 0 | 15.62 |
| **Stable dragoon18fra damage +4 (lvl 7)** `frasta.dragoon18fra.1.6` | fra | damage | 4 | 42000 | 0 | 0 | 780 | 0 | 0 | 15.62 |
| **Stable dragoon18fra protection +1 (lvl 2)** `frasta.dragoon18fra.2.1` | fra | protection | 1 | 760 | 0 | 0 | 935 | 0 | 0 | 15.62 |
| **Stable dragoon18fra protection +2 (lvl 3)** `frasta.dragoon18fra.2.2` | fra | protection | 2 | 1260 | 0 | 0 | 1150 | 0 | 0 | 15.62 |
| **Stable dragoon18fra protection +2 (lvl 4)** `frasta.dragoon18fra.2.3` | fra | protection | 2 | 15600 | 0 | 0 | 2350 | 0 | 0 | 15.62 |
| **Stable dragoon18fra protection +1 (lvl 5)** `frasta.dragoon18fra.2.4` | fra | protection | 1 | 17600 | 0 | 0 | 3350 | 0 | 0 | 15.62 |
| **Stable dragoon18fra protection +2 (lvl 6)** `frasta.dragoon18fra.2.5` | fra | protection | 2 | 19600 | 0 | 0 | 5350 | 0 | 0 | 15.62 |
| **Stable dragoon18fra protection +2 (lvl 7)** `frasta.dragoon18fra.2.6` | fra | protection | 2 | 21760 | 0 | 0 | 9350 | 0 | 0 | 15.62 |
| **Stable dragoon18net damage +1 (lvl 2)** `netsta.dragoon18net.1.1` | net | damage | 1 | 2000 | 0 | 0 | 100 | 0 | 0 | 15.62 |
| **Stable dragoon18net damage +2 (lvl 3)** `netsta.dragoon18net.1.2` | net | damage | 2 | 9000 | 0 | 0 | 350 | 0 | 0 | 15.62 |
| **Stable dragoon18net damage +3 (lvl 4)** `netsta.dragoon18net.1.3` | net | damage | 3 | 12000 | 0 | 0 | 400 | 0 | 0 | 15.62 |
| **Stable dragoon18net damage +1 (lvl 5)** `netsta.dragoon18net.1.4` | net | damage | 1 | 23000 | 0 | 0 | 580 | 0 | 0 | 15.62 |
| **Stable dragoon18net damage +2 (lvl 6)** `netsta.dragoon18net.1.5` | net | damage | 2 | 32000 | 0 | 0 | 680 | 0 | 0 | 15.62 |
| **Stable dragoon18net damage +3 (lvl 7)** `netsta.dragoon18net.1.6` | net | damage | 3 | 42000 | 0 | 0 | 780 | 0 | 0 | 15.62 |
| **Stable dragoon18net protection +1 (lvl 2)** `netsta.dragoon18net.2.1` | net | protection | 1 | 760 | 0 | 0 | 935 | 0 | 0 | 15.62 |
| **Stable dragoon18net protection +2 (lvl 3)** `netsta.dragoon18net.2.2` | net | protection | 2 | 1260 | 0 | 0 | 1150 | 0 | 0 | 15.62 |
| **Stable dragoon18net protection +2 (lvl 4)** `netsta.dragoon18net.2.3` | net | protection | 2 | 15600 | 0 | 0 | 2350 | 0 | 0 | 15.62 |
| **Stable dragoon18net protection +1 (lvl 5)** `netsta.dragoon18net.2.4` | net | protection | 1 | 17600 | 0 | 0 | 4350 | 0 | 0 | 15.62 |
| **Stable dragoon18net protection +2 (lvl 6)** `netsta.dragoon18net.2.5` | net | protection | 2 | 19600 | 0 | 0 | 5350 | 0 | 0 | 15.62 |
| **Stable dragoon18net protection +2 (lvl 7)** `netsta.dragoon18net.2.6` | net | protection | 2 | 21760 | 0 | 0 | 8350 | 0 | 0 | 15.62 |
| **Stable dragoon18pie damage +2 (lvl 2)** `piesta.dragoon18pie.1.1` | pie | damage | 2 | 2000 | 0 | 0 | 100 | 0 | 0 | 15.62 |
| **Stable dragoon18pie damage +2 (lvl 3)** `piesta.dragoon18pie.1.2` | pie | damage | 2 | 9000 | 0 | 0 | 350 | 0 | 0 | 15.62 |
| **Stable dragoon18pie damage +4 (lvl 4)** `piesta.dragoon18pie.1.3` | pie | damage | 4 | 12000 | 0 | 0 | 400 | 0 | 0 | 15.62 |
| **Stable dragoon18pie damage +2 (lvl 5)** `piesta.dragoon18pie.1.4` | pie | damage | 2 | 23000 | 0 | 0 | 580 | 0 | 0 | 15.62 |
| **Stable dragoon18pie damage +2 (lvl 6)** `piesta.dragoon18pie.1.5` | pie | damage | 2 | 32000 | 0 | 0 | 680 | 0 | 0 | 15.62 |
| **Stable dragoon18pie damage +4 (lvl 7)** `piesta.dragoon18pie.1.6` | pie | damage | 4 | 42000 | 0 | 0 | 780 | 0 | 0 | 15.62 |
| **Stable dragoon18pie protection +1 (lvl 2)** `piesta.dragoon18pie.2.1` | pie | protection | 1 | 760 | 0 | 0 | 935 | 0 | 0 | 15.62 |
| **Stable dragoon18pie protection +1 (lvl 3)** `piesta.dragoon18pie.2.2` | pie | protection | 1 | 1260 | 0 | 0 | 1150 | 0 | 0 | 15.62 |
| **Stable dragoon18pie protection +2 (lvl 4)** `piesta.dragoon18pie.2.3` | pie | protection | 2 | 15600 | 0 | 0 | 2350 | 0 | 0 | 15.62 |
| **Stable dragoon18pie protection +1 (lvl 5)** `piesta.dragoon18pie.2.4` | pie | protection | 1 | 17600 | 0 | 0 | 4350 | 0 | 0 | 15.62 |
| **Stable dragoon18pie protection +1 (lvl 6)** `piesta.dragoon18pie.2.5` | pie | protection | 1 | 19600 | 0 | 0 | 5350 | 0 | 0 | 15.62 |
| **Stable dragoon18pie protection +2 (lvl 7)** `piesta.dragoon18pie.2.6` | pie | protection | 2 | 21760 | 0 | 0 | 8350 | 0 | 0 | 15.62 |
| **Stable dragoonpol damage +1 (lvl 2)** `polsta.dragoonpol.1.1` | pol | damage | 1 | 700 | 0 | 0 | 250 | 0 | 0 | 15.62 |
| **Stable dragoonpol damage +1 (lvl 3)** `polsta.dragoonpol.1.2` | pol | damage | 1 | 500 | 0 | 0 | 200 | 0 | 0 | 15.62 |
| **Stable dragoonpol damage +2 (lvl 4)** `polsta.dragoonpol.1.3` | pol | damage | 2 | 700 | 0 | 0 | 240 | 0 | 0 | 15.62 |
| **Stable dragoonpol damage +1 (lvl 5)** `polsta.dragoonpol.1.4` | pol | damage | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 15.62 |
| **Stable dragoonpol damage +1 (lvl 6)** `polsta.dragoonpol.1.5` | pol | damage | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 15.62 |
| **Stable dragoonpol damage +3 (lvl 7)** `polsta.dragoonpol.1.6` | pol | damage | 3 | 0 | 0 | 0 | 0 | 0 | 0 | 15.62 |
| **Stable dragoonpol protection +1 (lvl 2)** `polsta.dragoonpol.2.1` | pol | protection | 1 | 900 | 0 | 0 | 250 | 0 | 0 | 15.62 |
| **Stable dragoonpol protection +1 (lvl 3)** `polsta.dragoonpol.2.2` | pol | protection | 1 | 6200 | 0 | 0 | 550 | 0 | 0 | 15.62 |
| **Stable dragoonpol protection +1 (lvl 4)** `polsta.dragoonpol.2.3` | pol | protection | 1 | 5400 | 0 | 0 | 1150 | 0 | 0 | 15.62 |
| **Stable dragoonpol protection +1 (lvl 5)** `polsta.dragoonpol.2.4` | pol | protection | 1 | 2000 | 0 | 0 | 800 | 0 | 0 | 15.62 |
| **Stable dragoonpol protection +2 (lvl 6)** `polsta.dragoonpol.2.5` | pol | protection | 2 | 3000 | 0 | 0 | 2250 | 0 | 0 | 15.62 |
| **Stable dragoonpol protection +2 (lvl 7)** `polsta.dragoonpol.2.6` | pol | protection | 2 | 5001 | 0 | 0 | 6100 | 0 | 0 | 15.62 |
| **Stable guardcavalrysax damage +2 (lvl 2)** `saxsta.guardcavalrysax.1.1` | sax | damage | 2 | 10000 | 0 | 0 | 200 | 0 | 0 | 15.62 |
| **Stable guardcavalrysax damage +2 (lvl 3)** `saxsta.guardcavalrysax.1.2` | sax | damage | 2 | 34000 | 0 | 0 | 1700 | 0 | 0 | 15.62 |
| **Stable guardcavalrysax damage +3 (lvl 4)** `saxsta.guardcavalrysax.1.3` | sax | damage | 3 | 64000 | 0 | 0 | 2100 | 0 | 0 | 15.62 |
| **Stable guardcavalrysax damage +1 (lvl 5)** `saxsta.guardcavalrysax.1.4` | sax | damage | 1 | 58000 | 0 | 0 | 4150 | 0 | 0 | 15.62 |
| **Stable guardcavalrysax damage +1 (lvl 6)** `saxsta.guardcavalrysax.1.5` | sax | damage | 1 | 59055 | 0 | 0 | 3100 | 0 | 0 | 15.62 |
| **Stable guardcavalrysax damage +1 (lvl 7)** `saxsta.guardcavalrysax.1.6` | sax | damage | 1 | 47050 | 0 | 0 | 8150 | 0 | 0 | 15.62 |
| **Stable guardcavalrysax protection +2 (lvl 2)** `saxsta.guardcavalrysax.2.1` | sax | protection | 2 | 1520 | 0 | 0 | 450 | 1000 | 0 | 15.62 |
| **Stable guardcavalrysax protection +2 (lvl 3)** `saxsta.guardcavalrysax.2.2` | sax | protection | 2 | 7000 | 0 | 0 | 750 | 2000 | 0 | 15.62 |
| **Stable guardcavalrysax protection +3 (lvl 4)** `saxsta.guardcavalrysax.2.3` | sax | protection | 3 | 3600 | 0 | 0 | 3300 | 3050 | 0 | 15.62 |
| **Stable guardcavalrysax protection +3 (lvl 5)** `saxsta.guardcavalrysax.2.4` | sax | protection | 3 | 8700 | 0 | 0 | 3200 | 200 | 0 | 15.62 |
| **Stable guardcavalrysax protection +1 (lvl 6)** `saxsta.guardcavalrysax.2.5` | sax | protection | 1 | 8700 | 0 | 0 | 2650 | 4300 | 0 | 15.62 |
| **Stable guardcavalrysax protection +1 (lvl 7)** `saxsta.guardcavalrysax.2.6` | sax | protection | 1 | 11200 | 0 | 0 | 4700 | 6760 | 0 | 15.62 |
| **Stable hackapell damage +1 (lvl 2)** `swesta.hackapell.1.1` | swe | damage | 1 | 2000 | 0 | 0 | 500 | 0 | 0 | 15.62 |
| **Stable hackapell damage +2 (lvl 3)** `swesta.hackapell.1.2` | swe | damage | 2 | 5000 | 0 | 0 | 800 | 0 | 0 | 15.62 |
| **Stable hackapell damage +2 (lvl 4)** `swesta.hackapell.1.3` | swe | damage | 2 | 10000 | 0 | 0 | 1200 | 0 | 0 | 15.62 |
| **Stable hackapell damage +1 (lvl 5)** `swesta.hackapell.1.4` | swe | damage | 1 | 20000 | 0 | 0 | 1300 | 0 | 0 | 15.62 |
| **Stable hackapell damage +2 (lvl 6)** `swesta.hackapell.1.5` | swe | damage | 2 | 30000 | 0 | 0 | 3000 | 0 | 0 | 15.62 |
| **Stable hackapell damage +2 (lvl 7)** `swesta.hackapell.1.6` | swe | damage | 2 | 20000 | 0 | 0 | 5000 | 0 | 0 | 15.62 |
| **Stable hackapell protection +1 (lvl 2)** `swesta.hackapell.2.1` | swe | protection | 1 | 2000 | 0 | 0 | 1350 | 0 | 0 | 15.62 |
| **Stable hackapell protection +2 (lvl 3)** `swesta.hackapell.2.2` | swe | protection | 2 | 1500 | 0 | 0 | 2100 | 0 | 0 | 15.62 |
| **Stable hackapell protection +2 (lvl 4)** `swesta.hackapell.2.3` | swe | protection | 2 | 5000 | 0 | 0 | 2300 | 0 | 0 | 15.62 |
| **Stable hackapell protection +1 (lvl 5)** `swesta.hackapell.2.4` | swe | protection | 1 | 10500 | 0 | 0 | 3400 | 0 | 0 | 15.62 |
| **Stable hackapell protection +2 (lvl 6)** `swesta.hackapell.2.5` | swe | protection | 2 | 12600 | 0 | 0 | 4500 | 0 | 0 | 15.62 |
| **Stable hackapell protection +2 (lvl 7)** `swesta.hackapell.2.6` | swe | protection | 2 | 40000 | 0 | 0 | 5000 | 0 | 0 | 15.62 |
| **Stable hetman damage +30 (lvl 2)** `ukrsta.hetman.1.1` | ukr | damage | 30 | 7000 | 0 | 0 | 18000 | 0 | 0 | 15.62 |
| **Stable hetman protection +10 (lvl 2)** `ukrsta.hetman.2.1` | ukr | protection | 10 | 44950 | 0 | 0 | 1000 | 20000 | 0 | 15.62 |
| **Stable hussar damage +1 (lvl 2)** `aussta.hussar.1.1` | aus,bav,net,pie,pol,por,rus,spa,ven | damage | 1 | 0 | 0 | 0 | 1800 | 1000 | 0 | 15.62 |
| **Stable hussar damage +1 (lvl 2)** `swesta.hussar.1.1` | sax,swe | damage | 1 | 0 | 0 | 0 | 1200 | 1500 | 0 | 15.62 |
| **Stable hussar damage +1 (lvl 2)** `frasta.hussar.1.1` | fra | damage | 1 | 0 | 0 | 0 | 800 | 200 | 0 | 15.62 |
| **Stable hussar damage +1 (lvl 2)** `engsta.hussar.1.1` | eng | damage | 1 | 0 | 0 | 0 | 1200 | 400 | 0 | 15.62 |
| **Stable hussar damage +1 (lvl 2)** `densta.hussar.1.1` | den | damage | 1 | 0 | 0 | 0 | 2800 | 1600 | 0 | 15.62 |
| **Stable hussar damage +2 (lvl 3)** `aussta.hussar.1.2` | aus,bav,eng,net,pie,pol,por,rus,spa,ven | damage | 2 | 0 | 0 | 0 | 3800 | 2000 | 0 | 15.62 |
| **Stable hussar damage +2 (lvl 3)** `swesta.hussar.1.2` | sax,swe | damage | 2 | 0 | 0 | 0 | 4400 | 1500 | 0 | 15.62 |
| **Stable hussar damage +2 (lvl 3)** `frasta.hussar.1.2` | fra | damage | 2 | 0 | 0 | 0 | 4800 | 2800 | 0 | 15.62 |
| **Stable hussar damage +2 (lvl 3)** `densta.hussar.1.2` | den | damage | 2 | 0 | 0 | 0 | 2800 | 1400 | 0 | 15.62 |
| **Stable hussar damage +3 (lvl 4)** `aussta.hussar.1.3` | aus,pie,pol,rus,spa,ven | damage | 3 | 20200 | 0 | 0 | 0 | 2000 | 0 | 15.62 |
| **Stable hussar damage +3 (lvl 4)** `netsta.hussar.1.3` | bav,net,por | damage | 3 | 20200 | 0 | 0 | 0 | 3000 | 0 | 15.62 |
| **Stable hussar damage +3 (lvl 4)** `frasta.hussar.1.3` | fra | damage | 3 | 25200 | 0 | 0 | 0 | 2500 | 0 | 15.62 |
| **Stable hussar damage +3 (lvl 4)** `engsta.hussar.1.3` | eng | damage | 3 | 10200 | 0 | 0 | 0 | 3000 | 0 | 15.62 |
| **Stable hussar damage +3 (lvl 4)** `swesta.hussar.1.3` | swe | damage | 3 | 10200 | 0 | 0 | 0 | 1500 | 0 | 15.62 |
| **Stable hussar damage +3 (lvl 4)** `densta.hussar.1.3` | den | damage | 3 | 10200 | 0 | 0 | 0 | 4000 | 0 | 15.62 |
| **Stable hussar damage +3 (lvl 4)** `saxsta.hussar.1.3` | sax | damage | 3 | 10200 | 0 | 0 | 0 | 2500 | 0 | 15.62 |
| **Stable hussar damage +4 (lvl 5)** `aussta.hussar.1.4` | aus,bav,net,pie,pol,por,rus,spa,ven | damage | 4 | 32000 | 0 | 0 | 0 | 3000 | 0 | 15.62 |
| **Stable hussar damage +4 (lvl 5)** `engsta.hussar.1.4` | den,eng | damage | 4 | 42000 | 0 | 0 | 0 | 2000 | 0 | 15.62 |
| **Stable hussar damage +4 (lvl 5)** `swesta.hussar.1.4` | sax,swe | damage | 4 | 42000 | 0 | 0 | 0 | 3500 | 0 | 15.62 |
| **Stable hussar damage +4 (lvl 5)** `frasta.hussar.1.4` | fra | damage | 4 | 27000 | 0 | 0 | 0 | 2500 | 0 | 15.62 |
| **Stable hussar damage +1 (lvl 6)** `aussta.hussar.1.5` | aus,bav,net,pie,pol,por,rus,spa,ven | damage | 1 | 49200 | 0 | 0 | 0 | 3500 | 0 | 15.62 |
| **Stable hussar damage +1 (lvl 6)** `swesta.hussar.1.5` | den,sax,swe | damage | 1 | 29200 | 0 | 0 | 0 | 5500 | 0 | 15.62 |
| **Stable hussar damage +1 (lvl 6)** `frasta.hussar.1.5` | fra | damage | 1 | 46200 | 0 | 0 | 0 | 4300 | 0 | 15.62 |
| **Stable hussar damage +1 (lvl 6)** `engsta.hussar.1.5` | eng | damage | 1 | 49200 | 0 | 0 | 0 | 6500 | 0 | 15.62 |
| **Stable hussar damage +1 (lvl 7)** `aussta.hussar.1.6` | aus,bav,net,pie,pol,por,rus,spa,ven | damage | 1 | 20000 | 0 | 0 | 0 | 6000 | 0 | 15.62 |
| **Stable hussar damage +1 (lvl 7)** `swesta.hussar.1.6` | sax,swe | damage | 1 | 40000 | 0 | 0 | 0 | 4400 | 0 | 15.62 |
| **Stable hussar damage +1 (lvl 7)** `frasta.hussar.1.6` | fra | damage | 1 | 21000 | 0 | 0 | 0 | 5200 | 0 | 15.62 |
| **Stable hussar damage +1 (lvl 7)** `engsta.hussar.1.6` | eng | damage | 1 | 14000 | 0 | 0 | 0 | 2000 | 0 | 15.62 |
| **Stable hussar damage +1 (lvl 7)** `densta.hussar.1.6` | den | damage | 1 | 40000 | 0 | 0 | 0 | 4000 | 0 | 15.62 |
| **Stable hussar protection +1 (lvl 2)** `aussta.hussar.2.1` | aus,bav,net,pie,pol,por,rus,spa,ven | protection | 1 | 1760 | 0 | 0 | 1350 | 0 | 0 | 15.62 |
| **Stable hussar protection +1 (lvl 2)** `swesta.hussar.2.1` | sax,swe | protection | 1 | 500 | 0 | 0 | 350 | 0 | 0 | 15.62 |
| **Stable hussar protection +1 (lvl 2)** `frasta.hussar.2.1` | fra | protection | 1 | 760 | 0 | 0 | 1350 | 0 | 0 | 15.62 |
| **Stable hussar protection +1 (lvl 2)** `engsta.hussar.2.1` | eng | protection | 1 | 1550 | 0 | 0 | 1150 | 0 | 0 | 15.62 |
| **Stable hussar protection +1 (lvl 2)** `densta.hussar.2.1` | den | protection | 1 | 150 | 0 | 0 | 1250 | 0 | 0 | 15.62 |
| **Stable hussar protection +1 (lvl 3)** `aussta.hussar.2.2` | aus,bav,net,pie,pol,por,rus,spa,ven | protection | 1 | 1900 | 0 | 0 | 2350 | 0 | 0 | 15.62 |
| **Stable hussar protection +1 (lvl 3)** `swesta.hussar.2.2` | sax,swe | protection | 1 | 3900 | 0 | 0 | 3350 | 0 | 0 | 15.62 |
| **Stable hussar protection +1 (lvl 3)** `frasta.hussar.2.2` | fra | protection | 1 | 2900 | 0 | 0 | 2350 | 0 | 0 | 15.62 |
| **Stable hussar protection +1 (lvl 3)** `engsta.hussar.2.2` | eng | protection | 1 | 2150 | 0 | 0 | 2550 | 0 | 0 | 15.62 |
| **Stable hussar protection +1 (lvl 3)** `densta.hussar.2.2` | den | protection | 1 | 3200 | 0 | 0 | 2450 | 0 | 0 | 15.62 |
| **Stable hussar protection +1 (lvl 4)** `aussta.hussar.2.3` | aus,bav,net,pie,pol,por,rus,spa,ven | protection | 1 | 1600 | 0 | 0 | 5350 | 0 | 0 | 15.62 |
| **Stable hussar protection +1 (lvl 4)** `swesta.hussar.2.3` | sax,swe | protection | 1 | 1100 | 0 | 0 | 5350 | 0 | 0 | 15.62 |
| **Stable hussar protection +1 (lvl 4)** `frasta.hussar.2.3` | fra | protection | 1 | 4600 | 0 | 0 | 5350 | 0 | 0 | 15.62 |
| **Stable hussar protection +1 (lvl 4)** `engsta.hussar.2.3` | eng | protection | 1 | 5600 | 0 | 0 | 4350 | 0 | 0 | 15.62 |
| **Stable hussar protection +1 (lvl 4)** `densta.hussar.2.3` | den | protection | 1 | 3600 | 0 | 0 | 3350 | 0 | 0 | 15.62 |
| **Stable hussar protection +2 (lvl 5)** `aussta.hussar.2.4` | aus,bav,net,pie,pol,por,rus,spa,ven | protection | 2 | 8000 | 0 | 0 | 8350 | 0 | 0 | 15.62 |
| **Stable hussar protection +2 (lvl 5)** `swesta.hussar.2.4` | sax,swe | protection | 2 | 7800 | 0 | 0 | 8350 | 0 | 0 | 15.62 |
| **Stable hussar protection +2 (lvl 5)** `frasta.hussar.2.4` | fra | protection | 2 | 4000 | 0 | 0 | 8350 | 0 | 0 | 15.62 |
| **Stable hussar protection +2 (lvl 5)** `engsta.hussar.2.4` | eng | protection | 2 | 4000 | 0 | 0 | 9350 | 0 | 0 | 15.62 |
| **Stable hussar protection +2 (lvl 5)** `densta.hussar.2.4` | den | protection | 2 | 6000 | 0 | 0 | 10350 | 0 | 0 | 15.62 |
| **Stable hussar protection +2 (lvl 6)** `aussta.hussar.2.5` | aus,bav,net,pie,pol,por,rus,spa,ven | protection | 2 | 2000 | 0 | 0 | 15350 | 0 | 0 | 15.62 |
| **Stable hussar protection +2 (lvl 6)** `swesta.hussar.2.5` | sax,swe | protection | 2 | 1700 | 0 | 0 | 17350 | 0 | 0 | 15.62 |
| **Stable hussar protection +2 (lvl 6)** `frasta.hussar.2.5` | fra | protection | 2 | 7000 | 0 | 0 | 15350 | 0 | 0 | 15.62 |
| **Stable hussar protection +2 (lvl 6)** `engsta.hussar.2.5` | eng | protection | 2 | 9000 | 0 | 0 | 13200 | 0 | 0 | 15.62 |
| **Stable hussar protection +2 (lvl 6)** `densta.hussar.2.5` | den | protection | 2 | 9000 | 0 | 0 | 13350 | 0 | 0 | 15.62 |
| **Stable hussar protection +3 (lvl 7)** `aussta.hussar.2.6` | aus,bav,net,pie,pol,por,rus,spa,ven | protection | 3 | 56000 | 0 | 0 | 20150 | 0 | 0 | 15.62 |
| **Stable hussar protection +3 (lvl 7)** `swesta.hussar.2.6` | sax,swe | protection | 3 | 55200 | 0 | 0 | 17150 | 0 | 0 | 15.62 |
| **Stable hussar protection +3 (lvl 7)** `frasta.hussar.2.6` | fra | protection | 3 | 51000 | 0 | 0 | 20150 | 0 | 0 | 15.62 |
| **Stable hussar protection +2 (lvl 7)** `engsta.hussar.2.6` | eng | protection | 2 | 52000 | 0 | 0 | 19850 | 0 | 0 | 15.62 |
| **Stable hussar protection +3 (lvl 7)** `densta.hussar.2.6` | den | protection | 3 | 48000 | 0 | 0 | 22150 | 0 | 0 | 15.62 |
| **Stable hussarhun protection +1 (lvl 2)** `hunsta.hussarhun.2.1` | hun | protection | 1 | 2000 | 0 | 0 | 1350 | 0 | 0 | 15.62 |
| **Stable hussarhun protection +1 (lvl 3)** `hunsta.hussarhun.2.2` | hun | protection | 1 | 1500 | 0 | 0 | 2100 | 0 | 0 | 15.62 |
| **Stable hussarhun protection +1 (lvl 4)** `hunsta.hussarhun.2.3` | hun | protection | 1 | 5000 | 0 | 0 | 2300 | 0 | 0 | 15.62 |
| **Stable hussarhun protection +2 (lvl 5)** `hunsta.hussarhun.2.4` | hun | protection | 2 | 10500 | 0 | 0 | 3400 | 0 | 0 | 15.62 |
| **Stable hussarhun protection +2 (lvl 6)** `hunsta.hussarhun.2.5` | hun | protection | 2 | 12600 | 0 | 0 | 4500 | 0 | 0 | 15.62 |
| **Stable hussarhun protection +3 (lvl 7)** `hunsta.hussarhun.2.6` | hun | protection | 3 | 40000 | 0 | 0 | 5000 | 0 | 0 | 15.62 |
| **Stable hussarpru damage +1 (lvl 2)** `prusta.hussarpru.1.1` | pru | damage | 1 | 0 | 0 | 0 | 2800 | 1600 | 0 | 15.62 |
| **Stable hussarpru damage +1 (lvl 3)** `prusta.hussarpru.1.2` | pru | damage | 1 | 0 | 0 | 0 | 2800 | 1400 | 0 | 15.62 |
| **Stable hussarpru damage +2 (lvl 4)** `prusta.hussarpru.1.3` | pru | damage | 2 | 10200 | 0 | 0 | 0 | 3000 | 0 | 15.62 |
| **Stable hussarpru damage +2 (lvl 5)** `prusta.hussarpru.1.4` | pru | damage | 2 | 42000 | 0 | 0 | 0 | 2000 | 0 | 15.62 |
| **Stable hussarpru damage +3 (lvl 6)** `prusta.hussarpru.1.5` | pru | damage | 3 | 29200 | 0 | 0 | 0 | 5500 | 0 | 15.62 |
| **Stable hussarpru damage +3 (lvl 7)** `prusta.hussarpru.1.6` | pru | damage | 3 | 40000 | 0 | 0 | 0 | 4000 | 0 | 15.62 |
| **Stable hussarpru protection +1 (lvl 2)** `prusta.hussarpru.2.1` | pru | protection | 1 | 150 | 0 | 0 | 1250 | 0 | 0 | 15.62 |
| **Stable hussarpru protection +1 (lvl 3)** `prusta.hussarpru.2.2` | pru | protection | 1 | 3200 | 0 | 0 | 2450 | 0 | 0 | 15.62 |
| **Stable hussarpru protection +1 (lvl 4)** `prusta.hussarpru.2.3` | pru | protection | 1 | 3600 | 0 | 0 | 3350 | 0 | 0 | 15.62 |
| **Stable hussarpru protection +2 (lvl 5)** `prusta.hussarpru.2.4` | pru | protection | 2 | 6000 | 0 | 0 | 10350 | 0 | 0 | 15.62 |
| **Stable hussarpru protection +2 (lvl 6)** `prusta.hussarpru.2.5` | pru | protection | 2 | 9000 | 0 | 0 | 13350 | 0 | 0 | 15.62 |
| **Stable hussarpru protection +3 (lvl 7)** `prusta.hussarpru.2.6` | pru | protection | 3 | 48000 | 0 | 0 | 22150 | 0 | 0 | 15.62 |
| **Stable hussarswi damage +2 (lvl 2)** `swista.hussarswi.1.1` | swi | damage | 2 | 0 | 0 | 0 | 2800 | 1600 | 0 | 15.62 |
| **Stable hussarswi damage +2 (lvl 3)** `swista.hussarswi.1.2` | swi | damage | 2 | 0 | 0 | 0 | 2800 | 1400 | 0 | 15.62 |
| **Stable hussarswi damage +2 (lvl 4)** `swista.hussarswi.1.3` | swi | damage | 2 | 10200 | 0 | 0 | 0 | 3000 | 0 | 15.62 |
| **Stable hussarswi damage +2 (lvl 5)** `swista.hussarswi.1.4` | swi | damage | 2 | 42000 | 0 | 0 | 0 | 2000 | 0 | 15.62 |
| **Stable hussarswi damage +2 (lvl 6)** `swista.hussarswi.1.5` | swi | damage | 2 | 29200 | 0 | 0 | 0 | 5500 | 0 | 15.62 |
| **Stable hussarswi damage +2 (lvl 7)** `swista.hussarswi.1.6` | swi | damage | 2 | 40000 | 0 | 0 | 0 | 4000 | 0 | 15.62 |
| **Stable hussarswi protection +1 (lvl 2)** `swista.hussarswi.2.1` | swi | protection | 1 | 150 | 0 | 0 | 1250 | 0 | 0 | 15.62 |
| **Stable hussarswi protection +2 (lvl 3)** `swista.hussarswi.2.2` | swi | protection | 2 | 3200 | 0 | 0 | 2450 | 0 | 0 | 15.62 |
| **Stable hussarswi protection +2 (lvl 4)** `swista.hussarswi.2.3` | swi | protection | 2 | 3600 | 0 | 0 | 3350 | 0 | 0 | 15.62 |
| **Stable hussarswi protection +1 (lvl 5)** `swista.hussarswi.2.4` | swi | protection | 1 | 6000 | 0 | 0 | 10350 | 0 | 0 | 15.62 |
| **Stable hussarswi protection +2 (lvl 6)** `swista.hussarswi.2.5` | swi | protection | 2 | 9000 | 0 | 0 | 13350 | 0 | 0 | 15.62 |
| **Stable hussarswi protection +2 (lvl 7)** `swista.hussarswi.2.6` | swi | protection | 2 | 48000 | 0 | 0 | 22150 | 0 | 0 | 15.62 |
| **Stable kingmusketeer damage +20 (lvl 2)** `frasta.kingmusketeer.1.1` | fra | damage | 20 | 7000 | 0 | 0 | 2500 | 0 | 0 | 15.62 |
| **Stable kingmusketeer protection +12 (lvl 2)** `frasta.kingmusketeer.2.1` | fra | protection | 12 | 2000 | 0 | 0 | 1350 | 0 | 0 | 15.62 |
| **Stable kingmusketeer protection +1 (lvl 3)** `frasta.kingmusketeer.2.2` | fra | protection | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 15.62 |
| **Stable kingmusketeer protection +2 (lvl 4)** `frasta.kingmusketeer.2.3` | fra | protection | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 15.62 |
| **Stable kingmusketeer protection +2 (lvl 5)** `frasta.kingmusketeer.2.4` | fra | protection | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 15.62 |
| **Stable kingmusketeer protection +2 (lvl 6)** `frasta.kingmusketeer.2.5` | fra | protection | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 15.62 |
| **Stable kingmusketeer protection +2 (lvl 7)** `frasta.kingmusketeer.2.6` | fra | protection | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 15.62 |
| **Stable lancersco protection +1 (lvl 2)** `scosta.lancersco.2.1` | sco | protection | 1 | 4000 | 0 | 0 | 1350 | 0 | 0 | 15.62 |
| **Stable lancersco protection +1 (lvl 3)** `scosta.lancersco.2.2` | sco | protection | 1 | 3500 | 0 | 0 | 2100 | 0 | 0 | 15.62 |
| **Stable lancersco protection +2 (lvl 4)** `scosta.lancersco.2.3` | sco | protection | 2 | 8000 | 0 | 0 | 3300 | 0 | 0 | 15.62 |
| **Stable lancersco protection +3 (lvl 5)** `scosta.lancersco.2.4` | sco | protection | 3 | 14500 | 0 | 0 | 4400 | 0 | 0 | 15.62 |
| **Stable lancersco protection +3 (lvl 6)** `scosta.lancersco.2.5` | sco | protection | 3 | 22600 | 0 | 0 | 5500 | 0 | 0 | 15.62 |
| **Stable lancersco protection +2 (lvl 7)** `scosta.lancersco.2.6` | sco | protection | 2 | 30000 | 0 | 0 | 6000 | 0 | 0 | 15.62 |
| **Stable lightcavalry damage +1 (lvl 2)** `hunsta.lightcavalry.1.1` | hun | damage | 1 | 4500 | 0 | 0 | 200 | 0 | 0 | 15.62 |
| **Stable lightcavalry damage +2 (lvl 3)** `hunsta.lightcavalry.1.2` | hun | damage | 2 | 5500 | 0 | 0 | 250 | 0 | 0 | 15.62 |
| **Stable lightcavalry damage +3 (lvl 4)** `hunsta.lightcavalry.1.3` | hun | damage | 3 | 22000 | 0 | 0 | 500 | 0 | 0 | 15.62 |
| **Stable lightcavalry damage +1 (lvl 5)** `hunsta.lightcavalry.1.4` | hun | damage | 1 | 13000 | 0 | 0 | 480 | 0 | 0 | 15.62 |
| **Stable lightcavalry damage +1 (lvl 6)** `hunsta.lightcavalry.1.5` | hun | damage | 1 | 42000 | 0 | 0 | 780 | 0 | 0 | 15.62 |
| **Stable lightcavalry damage +2 (lvl 7)** `hunsta.lightcavalry.1.6` | hun | damage | 2 | 32000 | 0 | 0 | 680 | 0 | 0 | 15.62 |
| **Stable lightcavalry protection +1 (lvl 2)** `hunsta.lightcavalry.2.1` | hun | protection | 1 | 750 | 0 | 0 | 935 | 0 | 0 | 15.62 |
| **Stable lightcavalry protection +1 (lvl 3)** `hunsta.lightcavalry.2.2` | hun | protection | 1 | 1260 | 0 | 0 | 1150 | 0 | 0 | 15.62 |
| **Stable lightcavalry protection +2 (lvl 4)** `hunsta.lightcavalry.2.3` | hun | protection | 2 | 10600 | 0 | 0 | 2350 | 0 | 0 | 15.62 |
| **Stable lightcavalry protection +1 (lvl 5)** `hunsta.lightcavalry.2.4` | hun | protection | 1 | 22600 | 0 | 0 | 5350 | 0 | 0 | 15.62 |
| **Stable lightcavalry protection +1 (lvl 6)** `hunsta.lightcavalry.2.5` | hun | protection | 1 | 19600 | 0 | 0 | 3350 | 0 | 0 | 15.62 |
| **Stable lightcavalry protection +2 (lvl 7)** `hunsta.lightcavalry.2.6` | hun | protection | 2 | 15760 | 0 | 0 | 9350 | 0 | 0 | 15.62 |
| **Stable mameluke protection +1 (lvl 2)** `algsta.mameluke.2.1` | alg | protection | 1 | 200 | 0 | 0 | 135 | 1000 | 0 | 15.62 |
| **Stable mameluke protection +2 (lvl 3)** `algsta.mameluke.2.2` | alg | protection | 2 | 2000 | 0 | 0 | 100 | 1000 | 0 | 15.62 |
| **Stable mameluke protection +3 (lvl 4)** `algsta.mameluke.2.3` | alg | protection | 3 | 40000 | 0 | 0 | 200 | 4000 | 0 | 15.62 |
| **Stable mameluke protection +3 (lvl 5)** `algsta.mameluke.2.4` | alg | protection | 3 | 40000 | 0 | 0 | 300 | 6000 | 0 | 15.62 |
| **Stable mameluke protection +2 (lvl 6)** `algsta.mameluke.2.5` | alg | protection | 2 | 40000 | 0 | 0 | 350 | 8000 | 0 | 15.62 |
| **Stable mameluke protection +1 (lvl 7)** `algsta.mameluke.2.6` | alg | protection | 1 | 40000 | 0 | 0 | 1000 | 10000 | 0 | 15.62 |
| **Stable raidersco protection +1 (lvl 2)** `scosta.raidersco.2.1` | sco | protection | 1 | 500 | 0 | 0 | 50 | 0 | 0 | 15.62 |
| **Stable raidersco protection +2 (lvl 3)** `scosta.raidersco.2.2` | sco | protection | 2 | 1500 | 0 | 0 | 150 | 0 | 0 | 15.62 |
| **Stable raidersco protection +2 (lvl 4)** `scosta.raidersco.2.3` | sco | protection | 2 | 5625 | 0 | 0 | 560 | 0 | 0 | 15.62 |
| **Stable raidersco protection +2 (lvl 5)** `scosta.raidersco.2.4` | sco | protection | 2 | 16200 | 0 | 0 | 1080 | 0 | 0 | 15.62 |
| **Stable raidersco protection +2 (lvl 6)** `scosta.raidersco.2.5` | sco | protection | 2 | 16200 | 0 | 0 | 1080 | 0 | 0 | 15.62 |
| **Stable raidersco protection +1 (lvl 7)** `scosta.raidersco.2.6` | sco | protection | 1 | 15000 | 0 | 0 | 750 | 0 | 0 | 15.62 |
| **Stable reiter damage +1 (lvl 2)** `aussta.reiter.1.1` | aus,bav,hun,net,pie,por,sax,spa,swi,ven | damage | 1 | 500 | 0 | 0 | 100 | 0 | 0 | 15.62 |
| **Stable reiter damage +1 (lvl 2)** `prusta.reiter.1.1` | den,pru | damage | 1 | 800 | 0 | 0 | 100 | 0 | 0 | 15.62 |
| **Stable reiter damage +1 (lvl 2)** `frasta.reiter.1.1` | fra | damage | 1 | 900 | 0 | 0 | 100 | 0 | 0 | 15.62 |
| **Stable reiter damage +1 (lvl 2)** `engsta.reiter.1.1` | eng | damage | 1 | 400 | 0 | 0 | 50 | 0 | 0 | 15.62 |
| **Stable reiter damage +2 (lvl 3)** `aussta.reiter.1.2` | aus,hun,net,pie,sax,spa,swi,ven | damage | 2 | 900 | 0 | 0 | 220 | 0 | 0 | 15.62 |
| **Stable reiter damage +2 (lvl 3)** `prusta.reiter.1.2` | bav,den,por,pru | damage | 2 | 800 | 0 | 0 | 220 | 0 | 0 | 15.62 |
| **Stable reiter damage +2 (lvl 3)** `frasta.reiter.1.2` | fra | damage | 2 | 500 | 0 | 0 | 280 | 0 | 0 | 15.62 |
| **Stable reiter damage +2 (lvl 3)** `engsta.reiter.1.2` | eng | damage | 2 | 1000 | 0 | 0 | 270 | 0 | 0 | 15.62 |
| **Stable reiter damage +1 (lvl 4)** `aussta.reiter.1.3` | aus,hun,pie,sax,spa,swi,ven | damage | 1 | 4400 | 0 | 0 | 280 | 0 | 0 | 15.62 |
| **Stable reiter damage +1 (lvl 4)** `prusta.reiter.1.3` | bav,den,por,pru | damage | 1 | 2400 | 0 | 0 | 380 | 0 | 0 | 15.62 |
| **Stable reiter damage +1 (lvl 4)** `frasta.reiter.1.3` | fra | damage | 1 | 4400 | 0 | 0 | 220 | 0 | 0 | 15.62 |
| **Stable reiter damage +1 (lvl 4)** `engsta.reiter.1.3` | eng | damage | 1 | 4400 | 0 | 0 | 180 | 0 | 0 | 15.62 |
| **Stable reiter damage +1 (lvl 4)** `netsta.reiter.1.3` | net | damage | 1 | 4600 | 0 | 0 | 280 | 0 | 0 | 15.62 |
| **Stable reiter damage +1 (lvl 5)** `aussta.reiter.1.4` | aus,hun,pie,sax,spa,swi,ven | damage | 1 | 2250 | 0 | 0 | 320 | 0 | 0 | 15.62 |
| **Stable reiter damage +1 (lvl 5)** `prusta.reiter.1.4` | bav,den,por,pru | damage | 1 | 4250 | 0 | 0 | 220 | 0 | 0 | 15.62 |
| **Stable reiter damage +1 (lvl 5)** `frasta.reiter.1.4` | fra | damage | 1 | 3050 | 0 | 0 | 320 | 0 | 0 | 15.62 |
| **Stable reiter damage +1 (lvl 5)** `engsta.reiter.1.4` | eng | damage | 1 | 2750 | 0 | 0 | 420 | 0 | 0 | 15.62 |
| **Stable reiter damage +1 (lvl 5)** `netsta.reiter.1.4` | net | damage | 1 | 2050 | 0 | 0 | 220 | 0 | 0 | 15.62 |
| **Stable reiter damage +1 (lvl 6)** `aussta.reiter.1.5` | aus,hun,pie,sax,spa,swi,ven | damage | 1 | 3030 | 0 | 0 | 600 | 0 | 0 | 15.62 |
| **Stable reiter damage +1 (lvl 6)** `prusta.reiter.1.5` | bav,den,por,pru | damage | 1 | 4030 | 0 | 0 | 900 | 0 | 0 | 15.62 |
| **Stable reiter damage +1 (lvl 6)** `frasta.reiter.1.5` | fra | damage | 1 | 2030 | 0 | 0 | 800 | 0 | 0 | 15.62 |
| **Stable reiter damage +1 (lvl 6)** `engsta.reiter.1.5` | eng | damage | 1 | 2530 | 0 | 0 | 600 | 0 | 0 | 15.62 |
| **Stable reiter damage +1 (lvl 6)** `netsta.reiter.1.5` | net | damage | 1 | 3530 | 0 | 0 | 500 | 0 | 0 | 15.62 |
| **Stable reiter damage +1 (lvl 7)** `spasta.reiter.1.6` | hun,pie,sax,spa,swi,ven | damage | 1 | 7000 | 0 | 0 | 1800 | 0 | 0 | 15.62 |
| **Stable reiter damage +1 (lvl 7)** `prusta.reiter.1.6` | bav,den,por,pru | damage | 1 | 6000 | 0 | 0 | 1600 | 0 | 0 | 15.62 |
| **Stable reiter damage +1 (lvl 7)** `aussta.reiter.1.6` | aus | damage | 1 | 7500 | 0 | 0 | 1800 | 0 | 0 | 15.62 |
| **Stable reiter damage +1 (lvl 7)** `frasta.reiter.1.6` | fra | damage | 1 | 7000 | 0 | 0 | 1600 | 0 | 0 | 15.62 |
| **Stable reiter damage +1 (lvl 7)** `engsta.reiter.1.6` | eng | damage | 1 | 7500 | 0 | 0 | 1700 | 0 | 0 | 15.62 |
| **Stable reiter damage +1 (lvl 7)** `netsta.reiter.1.6` | net | damage | 1 | 6500 | 0 | 0 | 1900 | 0 | 0 | 15.62 |
| **Stable reiter protection +2 (lvl 2)** `aussta.reiter.2.1` | aus,hun,pie,sax,spa,swi,ven | protection | 2 | 200 | 0 | 0 | 135 | 300 | 0 | 15.62 |
| **Stable reiter protection +2 (lvl 2)** `prusta.reiter.2.1` | bav,den,por,pru | protection | 2 | 200 | 0 | 0 | 135 | 400 | 0 | 15.62 |
| **Stable reiter protection +2 (lvl 2)** `frasta.reiter.2.1` | fra | protection | 2 | 600 | 0 | 0 | 135 | 400 | 0 | 15.62 |
| **Stable reiter protection +2 (lvl 2)** `engsta.reiter.2.1` | eng | protection | 2 | 500 | 0 | 0 | 35 | 200 | 0 | 15.62 |
| **Stable reiter protection +2 (lvl 2)** `netsta.reiter.2.1` | net | protection | 2 | 250 | 0 | 0 | 55 | 300 | 0 | 15.62 |
| **Stable reiter protection +3 (lvl 3)** `aussta.reiter.2.2` | aus,hun,pie,sax,spa,swi,ven | protection | 3 | 600 | 0 | 0 | 100 | 400 | 0 | 15.62 |
| **Stable reiter protection +3 (lvl 3)** `prusta.reiter.2.2` | bav,den,por,pru | protection | 3 | 600 | 0 | 0 | 100 | 300 | 0 | 15.62 |
| **Stable reiter protection +3 (lvl 3)** `frasta.reiter.2.2` | fra | protection | 3 | 200 | 0 | 0 | 200 | 300 | 0 | 15.62 |
| **Stable reiter protection +3 (lvl 3)** `engsta.reiter.2.2` | eng | protection | 3 | 300 | 0 | 0 | 200 | 500 | 0 | 15.62 |
| **Stable reiter protection +3 (lvl 3)** `netsta.reiter.2.2` | net | protection | 3 | 550 | 0 | 0 | 200 | 400 | 0 | 15.62 |
| **Stable reiter protection +3 (lvl 4)** `aussta.reiter.2.3` | aus,bav,den,hun,pie,por,pru,sax,spa,swi,ven | protection | 3 | 800 | 0 | 0 | 200 | 560 | 0 | 15.62 |
| **Stable reiter protection +3 (lvl 4)** `frasta.reiter.2.3` | fra | protection | 3 | 800 | 0 | 0 | 100 | 560 | 0 | 15.62 |
| **Stable reiter protection +3 (lvl 4)** `engsta.reiter.2.3` | eng | protection | 3 | 950 | 0 | 0 | 200 | 620 | 0 | 15.62 |
| **Stable reiter protection +3 (lvl 4)** `netsta.reiter.2.3` | net | protection | 3 | 600 | 0 | 0 | 100 | 560 | 0 | 15.62 |
| **Stable reiter protection +2 (lvl 5)** `aussta.reiter.2.4` | aus,hun,pie,sax,spa,swi,ven | protection | 2 | 1600 | 0 | 0 | 300 | 640 | 0 | 15.62 |
| **Stable reiter protection +2 (lvl 5)** `prusta.reiter.2.4` | bav,den,por,pru | protection | 2 | 1600 | 0 | 0 | 300 | 340 | 0 | 15.62 |
| **Stable reiter protection +2 (lvl 5)** `frasta.reiter.2.4` | fra | protection | 2 | 3200 | 0 | 0 | 300 | 300 | 0 | 15.62 |
| **Stable reiter protection +2 (lvl 5)** `engsta.reiter.2.4` | eng | protection | 2 | 1450 | 0 | 0 | 300 | 540 | 0 | 15.62 |
| **Stable reiter protection +2 (lvl 5)** `netsta.reiter.2.4` | net | protection | 2 | 1800 | 0 | 0 | 500 | 640 | 0 | 15.62 |
| **Stable reiter protection +1 (lvl 6)** `aussta.reiter.2.5` | aus,hun,pie,sax,spa,swi,ven | protection | 1 | 3200 | 0 | 0 | 350 | 300 | 0 | 15.62 |
| **Stable reiter protection +1 (lvl 6)** `prusta.reiter.2.5` | bav,den,por,pru | protection | 1 | 2200 | 0 | 0 | 350 | 600 | 0 | 15.62 |
| **Stable reiter protection +1 (lvl 6)** `frasta.reiter.2.5` | fra | protection | 1 | 1600 | 0 | 0 | 350 | 650 | 0 | 15.62 |
| **Stable reiter protection +1 (lvl 6)** `engsta.reiter.2.5` | eng | protection | 1 | 6200 | 0 | 0 | 550 | 600 | 0 | 15.62 |
| **Stable reiter protection +1 (lvl 6)** `netsta.reiter.2.5` | net | protection | 1 | 5200 | 0 | 0 | 250 | 300 | 0 | 15.62 |
| **Stable reiter protection +1 (lvl 7)** `aussta.reiter.2.6` | aus,hun,pie,sax,spa,swi,ven | protection | 1 | 16000 | 0 | 0 | 1000 | 5000 | 0 | 15.62 |
| **Stable reiter protection +1 (lvl 7)** `prusta.reiter.2.6` | bav,den,por,pru | protection | 1 | 17000 | 0 | 0 | 950 | 5200 | 0 | 15.62 |
| **Stable reiter protection +1 (lvl 7)** `frasta.reiter.2.6` | fra | protection | 1 | 15700 | 0 | 0 | 1000 | 5000 | 0 | 15.62 |
| **Stable reiter protection +1 (lvl 7)** `engsta.reiter.2.6` | eng | protection | 1 | 12000 | 0 | 0 | 720 | 3730 | 0 | 15.62 |
| **Stable reiter protection +1 (lvl 7)** `netsta.reiter.2.6` | net | protection | 1 | 14000 | 0 | 0 | 990 | 5000 | 0 | 15.62 |
| **Stable reiterpol damage +1 (lvl 2)** `polsta.reiterpol.1.1` | pol | damage | 1 | 2000 | 0 | 0 | 500 | 0 | 0 | 15.62 |
| **Stable reiterpol damage +1 (lvl 3)** `polsta.reiterpol.1.2` | pol | damage | 1 | 5000 | 0 | 0 | 800 | 0 | 0 | 15.62 |
| **Stable reiterpol damage +1 (lvl 4)** `polsta.reiterpol.1.3` | pol | damage | 1 | 10000 | 0 | 0 | 800 | 0 | 0 | 15.62 |
| **Stable reiterpol damage +2 (lvl 5)** `polsta.reiterpol.1.4` | pol | damage | 2 | 20000 | 0 | 0 | 950 | 0 | 0 | 15.62 |
| **Stable reiterpol damage +2 (lvl 6)** `polsta.reiterpol.1.5` | pol | damage | 2 | 30000 | 0 | 0 | 300 | 0 | 0 | 15.62 |
| **Stable reiterpol damage +3 (lvl 7)** `polsta.reiterpol.1.6` | pol | damage | 3 | 20000 | 0 | 0 | 1500 | 0 | 0 | 15.62 |
| **Stable reiterpol protection +1 (lvl 2)** `polsta.reiterpol.2.1` | pol | protection | 1 | 2000 | 0 | 0 | 900 | 0 | 0 | 15.62 |
| **Stable reiterpol protection +1 (lvl 3)** `polsta.reiterpol.2.2` | pol | protection | 1 | 1500 | 0 | 0 | 850 | 0 | 0 | 15.62 |
| **Stable reiterpol protection +1 (lvl 4)** `polsta.reiterpol.2.3` | pol | protection | 1 | 5000 | 0 | 0 | 950 | 0 | 0 | 15.62 |
| **Stable reiterpol protection +2 (lvl 5)** `polsta.reiterpol.2.4` | pol | protection | 2 | 10500 | 0 | 0 | 400 | 0 | 0 | 15.62 |
| **Stable reiterpol protection +2 (lvl 6)** `polsta.reiterpol.2.5` | pol | protection | 2 | 12600 | 0 | 0 | 1500 | 0 | 0 | 15.62 |
| **Stable reiterpol protection +3 (lvl 7)** `polsta.reiterpol.2.6` | pol | protection | 3 | 40000 | 0 | 0 | 9000 | 0 | 0 | 15.62 |
| **Stable reiterswe damage +1 (lvl 2)** `swesta.reiterswe.1.1` | swe | damage | 1 | 500 | 0 | 0 | 100 | 0 | 0 | 15.62 |
| **Stable reiterswe damage +2 (lvl 3)** `swesta.reiterswe.1.2` | swe | damage | 2 | 900 | 0 | 0 | 220 | 0 | 0 | 15.62 |
| **Stable reiterswe damage +1 (lvl 4)** `swesta.reiterswe.1.3` | swe | damage | 1 | 4400 | 0 | 0 | 280 | 0 | 0 | 15.62 |
| **Stable reiterswe damage +1 (lvl 5)** `swesta.reiterswe.1.4` | swe | damage | 1 | 2250 | 0 | 0 | 320 | 0 | 0 | 15.62 |
| **Stable reiterswe damage +1 (lvl 6)** `swesta.reiterswe.1.5` | swe | damage | 1 | 3030 | 0 | 0 | 600 | 0 | 0 | 15.62 |
| **Stable reiterswe damage +1 (lvl 7)** `swesta.reiterswe.1.6` | swe | damage | 1 | 7000 | 0 | 0 | 1800 | 0 | 0 | 15.62 |
| **Stable reiterswe protection +1 (lvl 2)** `swesta.reiterswe.2.1` | swe | protection | 1 | 200 | 0 | 0 | 135 | 300 | 0 | 15.62 |
| **Stable reiterswe protection +1 (lvl 3)** `swesta.reiterswe.2.2` | swe | protection | 1 | 600 | 0 | 0 | 100 | 400 | 0 | 15.62 |
| **Stable reiterswe protection +2 (lvl 4)** `swesta.reiterswe.2.3` | swe | protection | 2 | 800 | 0 | 0 | 200 | 560 | 0 | 15.62 |
| **Stable reiterswe protection +2 (lvl 5)** `swesta.reiterswe.2.4` | swe | protection | 2 | 1600 | 0 | 0 | 300 | 640 | 0 | 15.62 |
| **Stable reiterswe protection +3 (lvl 6)** `swesta.reiterswe.2.5` | swe | protection | 3 | 3200 | 0 | 0 | 350 | 300 | 0 | 15.62 |
| **Stable reiterswe protection +2 (lvl 7)** `swesta.reiterswe.2.6` | swe | protection | 2 | 16000 | 0 | 0 | 1000 | 5000 | 0 | 15.62 |
| **Stable sipahi damage +1 (lvl 2)** `tursta.sipahi.1.1` | tur | damage | 1 | 500 | 0 | 0 | 100 | 0 | 0 | 15.62 |
| **Stable sipahi damage +2 (lvl 3)** `tursta.sipahi.1.2` | tur | damage | 2 | 900 | 0 | 0 | 220 | 0 | 0 | 15.62 |
| **Stable sipahi damage +1 (lvl 4)** `tursta.sipahi.1.3` | tur | damage | 1 | 4400 | 0 | 0 | 280 | 0 | 0 | 15.62 |
| **Stable sipahi damage +1 (lvl 5)** `tursta.sipahi.1.4` | tur | damage | 1 | 2250 | 0 | 0 | 320 | 0 | 0 | 15.62 |
| **Stable sipahi damage +1 (lvl 6)** `tursta.sipahi.1.5` | tur | damage | 1 | 3030 | 0 | 0 | 600 | 0 | 0 | 15.62 |
| **Stable sipahi damage +1 (lvl 7)** `tursta.sipahi.1.6` | tur | damage | 1 | 7000 | 0 | 0 | 1800 | 0 | 0 | 15.62 |
| **Stable sipahi protection +1 (lvl 2)** `tursta.sipahi.2.1` | tur | protection | 1 | 200 | 0 | 0 | 135 | 300 | 0 | 15.62 |
| **Stable sipahi protection +2 (lvl 3)** `tursta.sipahi.2.2` | tur | protection | 2 | 600 | 0 | 0 | 100 | 400 | 0 | 15.62 |
| **Stable sipahi protection +2 (lvl 4)** `tursta.sipahi.2.3` | tur | protection | 2 | 800 | 0 | 0 | 200 | 560 | 0 | 15.62 |
| **Stable sipahi protection +2 (lvl 5)** `tursta.sipahi.2.4` | tur | protection | 2 | 1600 | 0 | 0 | 300 | 640 | 0 | 15.62 |
| **Stable sipahi protection +2 (lvl 6)** `tursta.sipahi.2.5` | tur | protection | 2 | 3200 | 0 | 0 | 350 | 300 | 0 | 15.62 |
| **Stable sipahi protection +3 (lvl 7)** `tursta.sipahi.2.6` | tur | protection | 3 | 16000 | 0 | 0 | 1000 | 5000 | 0 | 15.62 |
| **Stable spakh protection +1 (lvl 2)** `tursta.spakh.2.1` | tur | protection | 1 | 200 | 0 | 0 | 135 | 1000 | 0 | 15.62 |
| **Stable spakh protection +1 (lvl 3)** `tursta.spakh.2.2` | tur | protection | 1 | 2000 | 0 | 0 | 100 | 1000 | 0 | 15.62 |
| **Stable spakh protection +2 (lvl 4)** `tursta.spakh.2.3` | tur | protection | 2 | 40000 | 0 | 0 | 200 | 4000 | 0 | 15.62 |
| **Stable spakh protection +3 (lvl 5)** `tursta.spakh.2.4` | tur | protection | 3 | 40000 | 0 | 0 | 300 | 6000 | 0 | 15.62 |
| **Stable spakh protection +2 (lvl 6)** `tursta.spakh.2.5` | tur | protection | 2 | 40000 | 0 | 0 | 350 | 8000 | 0 | 15.62 |
| **Stable spakh protection +1 (lvl 7)** `tursta.spakh.2.6` | tur | protection | 1 | 40000 | 0 | 0 | 1000 | 10000 | 0 | 15.62 |
| **Stable tatar damage +2 (lvl 2)** `tursta.tatar.1.1` | tur | damage | 2 | 700 | 0 | 0 | 250 | 0 | 0 | 15.62 |
| **Stable tatar damage +2 (lvl 3)** `tursta.tatar.1.2` | tur | damage | 2 | 500 | 0 | 0 | 200 | 0 | 0 | 15.62 |
| **Stable tatar damage +2 (lvl 4)** `tursta.tatar.1.3` | tur | damage | 2 | 700 | 0 | 0 | 240 | 0 | 0 | 15.62 |
| **Stable tatar damage +3 (lvl 5)** `tursta.tatar.1.4` | tur | damage | 3 | 1200 | 0 | 0 | 900 | 0 | 0 | 15.62 |
| **Stable tatar damage +3 (lvl 6)** `tursta.tatar.1.5` | tur | damage | 3 | 1800 | 0 | 0 | 800 | 0 | 0 | 15.62 |
| **Stable tatar damage +3 (lvl 7)** `tursta.tatar.1.6` | tur | damage | 3 | 850 | 0 | 0 | 650 | 0 | 0 | 15.62 |
| **Stable tatar protection +1 (lvl 2)** `tursta.tatar.2.1` | tur | protection | 1 | 900 | 0 | 0 | 250 | 0 | 0 | 15.62 |
| **Stable tatar protection +1 (lvl 3)** `tursta.tatar.2.2` | tur | protection | 1 | 6200 | 0 | 0 | 1150 | 0 | 0 | 15.62 |
| **Stable tatar protection +2 (lvl 4)** `tursta.tatar.2.3` | tur | protection | 2 | 5400 | 0 | 0 | 2150 | 0 | 0 | 15.62 |
| **Stable tatar protection +1 (lvl 5)** `tursta.tatar.2.4` | tur | protection | 1 | 2000 | 0 | 0 | 1200 | 0 | 0 | 15.62 |
| **Stable tatar protection +1 (lvl 6)** `tursta.tatar.2.5` | tur | protection | 1 | 3000 | 0 | 0 | 4250 | 0 | 0 | 15.62 |
| **Stable tatar protection +2 (lvl 7)** `tursta.tatar.2.6` | tur | protection | 2 | 5001 | 0 | 0 | 8101 | 0 | 0 | 15.62 |
| **Stable vityaz damage +1 (lvl 2)** `russta.vityaz.1.1` | rus | damage | 1 | 500 | 0 | 0 | 100 | 0 | 0 | 15.62 |
| **Stable vityaz damage +2 (lvl 3)** `russta.vityaz.1.2` | rus | damage | 2 | 900 | 0 | 0 | 220 | 0 | 0 | 15.62 |
| **Stable vityaz damage +1 (lvl 4)** `russta.vityaz.1.3` | rus | damage | 1 | 4400 | 0 | 0 | 280 | 0 | 0 | 15.62 |
| **Stable vityaz damage +1 (lvl 5)** `russta.vityaz.1.4` | rus | damage | 1 | 2250 | 0 | 0 | 320 | 0 | 0 | 15.62 |
| **Stable vityaz damage +1 (lvl 6)** `russta.vityaz.1.5` | rus | damage | 1 | 3030 | 0 | 0 | 600 | 0 | 0 | 15.62 |
| **Stable vityaz damage +1 (lvl 7)** `russta.vityaz.1.6` | rus | damage | 1 | 7000 | 0 | 0 | 1800 | 0 | 0 | 15.62 |
| **Stable vityaz protection +2 (lvl 2)** `russta.vityaz.2.1` | rus | protection | 2 | 200 | 0 | 0 | 135 | 300 | 0 | 15.62 |
| **Stable vityaz protection +3 (lvl 3)** `russta.vityaz.2.2` | rus | protection | 3 | 600 | 0 | 0 | 100 | 400 | 0 | 15.62 |
| **Stable vityaz protection +3 (lvl 4)** `russta.vityaz.2.3` | rus | protection | 3 | 800 | 0 | 0 | 200 | 560 | 0 | 15.62 |
| **Stable vityaz protection +2 (lvl 5)** `russta.vityaz.2.4` | rus | protection | 2 | 1600 | 0 | 0 | 300 | 640 | 0 | 15.62 |
| **Stable vityaz protection +1 (lvl 6)** `russta.vityaz.2.5` | rus | protection | 1 | 3200 | 0 | 0 | 350 | 300 | 0 | 15.62 |
| **Stable vityaz protection +1 (lvl 7)** `russta.vityaz.2.6` | rus | protection | 1 | 16000 | 0 | 0 | 1000 | 5000 | 0 | 15.62 |
| **Stable wingedhussar damage +1 (lvl 2)** `polsta.wingedhussar.1.1` | pol | damage | 1 | 400 | 0 | 0 | 200 | 0 | 0 | 15.62 |
| **Stable wingedhussar damage +2 (lvl 3)** `polsta.wingedhussar.1.2` | pol | damage | 2 | 990 | 0 | 0 | 120 | 0 | 0 | 15.62 |
| **Stable wingedhussar damage +2 (lvl 4)** `polsta.wingedhussar.1.3` | pol | damage | 2 | 2400 | 0 | 0 | 380 | 0 | 0 | 15.62 |
| **Stable wingedhussar damage +2 (lvl 5)** `polsta.wingedhussar.1.4` | pol | damage | 2 | 4250 | 0 | 0 | 220 | 0 | 0 | 15.62 |
| **Stable wingedhussar damage +2 (lvl 6)** `polsta.wingedhussar.1.5` | pol | damage | 2 | 7030 | 0 | 0 | 200 | 0 | 0 | 15.62 |
| **Stable wingedhussar damage +1 (lvl 7)** `polsta.wingedhussar.1.6` | pol | damage | 1 | 3000 | 0 | 0 | 2200 | 0 | 0 | 15.62 |
| **Stable wingedhussar protection +2 (lvl 2)** `polsta.wingedhussar.2.1` | pol | protection | 2 | 300 | 0 | 0 | 35 | 100 | 0 | 15.62 |
| **Stable wingedhussar protection +2 (lvl 3)** `polsta.wingedhussar.2.2` | pol | protection | 2 | 500 | 0 | 0 | 200 | 600 | 0 | 15.62 |
| **Stable wingedhussar protection +2 (lvl 4)** `polsta.wingedhussar.2.3` | pol | protection | 2 | 600 | 0 | 0 | 300 | 260 | 0 | 15.62 |
| **Stable wingedhussar protection +2 (lvl 5)** `polsta.wingedhussar.2.4` | pol | protection | 2 | 1800 | 0 | 0 | 200 | 940 | 0 | 15.62 |
| **Stable wingedhussar protection +2 (lvl 6)** `polsta.wingedhussar.2.5` | pol | protection | 2 | 2200 | 0 | 0 | 150 | 700 | 0 | 15.62 |
| **Stable wingedhussar protection +2 (lvl 7)** `polsta.wingedhussar.2.6` | pol | protection | 2 | 17150 | 0 | 0 | 1200 | 4600 | 0 | 15.62 |

## bar — Barracks 17c (per-unit upgrades)

Каждая запись — одна нация. Если значение одинаковое для всех 21 нации, показано одной строкой с `nation=all`. Если есть per-nation override (через `_country_ModifyUpgrade`), показаны отдельно.

| Апгрейд | nations | itype | val | F | W | S | G | I | C | time |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `ausbar.1` | all | +food eff % | 140 | 750 | 0 | 0 | 250 | 0 | 0 | 15.62 |
| `algbar.1` | alg | +food eff % | 140 | 600 | 0 | 0 | 250 | 0 | 0 | 15.62 |
| `ausbar.2` | aus,bav,den,fra,hun,net,pie,pol,por,pru,rus,sax,spa,swe,swi,ven | +food eff % | 180 | 25600 | 0 | 0 | 3350 | 2000 | 0 | 15.62 |
| `ukrbar.2` | sco,ukr | +food eff % | 180 | 5600 | 0 | 0 | 1350 | 1900 | 0 | 15.62 |
| **Barracks 17c archer damage +2 (lvl 2)** `algbar.archer.1.1` | alg | damage | 2 | 700 | 0 | 0 | 250 | 0 | 0 | 15.62 |
| **Barracks 17c archer damage +2 (lvl 3)** `algbar.archer.1.2` | alg | damage | 2 | 500 | 0 | 0 | 200 | 0 | 0 | 15.62 |
| **Barracks 17c archer damage +2 (lvl 4)** `algbar.archer.1.3` | alg | damage | 2 | 700 | 0 | 0 | 240 | 0 | 0 | 15.62 |
| **Barracks 17c archer damage +3 (lvl 5)** `algbar.archer.1.4` | alg | damage | 3 | 1200 | 0 | 0 | 900 | 0 | 0 | 15.62 |
| **Barracks 17c archer damage +3 (lvl 6)** `algbar.archer.1.5` | alg | damage | 3 | 1800 | 0 | 0 | 800 | 0 | 0 | 15.62 |
| **Barracks 17c archer damage +3 (lvl 7)** `algbar.archer.1.6` | alg | damage | 3 | 850 | 0 | 0 | 650 | 0 | 0 | 15.62 |
| **Barracks 17c archer protection +1 (lvl 2)** `algbar.archer.2.1` | alg | protection | 1 | 900 | 0 | 0 | 250 | 0 | 0 | 15.62 |
| **Barracks 17c archer protection +1 (lvl 3)** `algbar.archer.2.2` | alg | protection | 1 | 2200 | 0 | 0 | 550 | 0 | 0 | 15.62 |
| **Barracks 17c archer protection +2 (lvl 4)** `algbar.archer.2.3` | alg | protection | 2 | 3400 | 0 | 0 | 850 | 0 | 0 | 15.62 |
| **Barracks 17c archer protection +1 (lvl 5)** `algbar.archer.2.4` | alg | protection | 1 | 2000 | 0 | 0 | 400 | 0 | 0 | 15.62 |
| **Barracks 17c archer protection +1 (lvl 6)** `algbar.archer.2.5` | alg | protection | 1 | 3000 | 0 | 0 | 850 | 0 | 0 | 15.62 |
| **Barracks 17c archer protection +2 (lvl 7)** `algbar.archer.2.6` | alg | protection | 2 | 4000 | 0 | 0 | 1200 | 0 | 0 | 15.62 |
| **Barracks 17c archertur damage +2 (lvl 2)** `turbar.archertur.1.1` | tur | damage | 2 | 700 | 0 | 0 | 250 | 0 | 0 | 15.62 |
| **Barracks 17c archertur damage +2 (lvl 3)** `turbar.archertur.1.2` | tur | damage | 2 | 500 | 0 | 0 | 200 | 0 | 0 | 15.62 |
| **Barracks 17c archertur damage +2 (lvl 4)** `turbar.archertur.1.3` | tur | damage | 2 | 700 | 0 | 0 | 240 | 0 | 0 | 15.62 |
| **Barracks 17c archertur damage +3 (lvl 5)** `turbar.archertur.1.4` | tur | damage | 3 | 1200 | 0 | 0 | 900 | 0 | 0 | 15.62 |
| **Barracks 17c archertur damage +3 (lvl 6)** `turbar.archertur.1.5` | tur | damage | 3 | 1800 | 0 | 0 | 800 | 0 | 0 | 15.62 |
| **Barracks 17c archertur damage +3 (lvl 7)** `turbar.archertur.1.6` | tur | damage | 3 | 850 | 0 | 0 | 650 | 0 | 0 | 15.62 |
| **Barracks 17c archertur protection +1 (lvl 2)** `turbar.archertur.2.1` | tur | protection | 1 | 900 | 0 | 0 | 250 | 0 | 0 | 15.62 |
| **Barracks 17c archertur protection +2 (lvl 3)** `turbar.archertur.2.2` | tur | protection | 2 | 6200 | 0 | 0 | 1150 | 0 | 0 | 15.62 |
| **Barracks 17c archertur protection +2 (lvl 4)** `turbar.archertur.2.3` | tur | protection | 2 | 5400 | 0 | 0 | 2150 | 0 | 0 | 15.62 |
| **Barracks 17c archertur protection +1 (lvl 5)** `turbar.archertur.2.4` | tur | protection | 1 | 2000 | 0 | 0 | 1200 | 0 | 0 | 15.62 |
| **Barracks 17c archertur protection +2 (lvl 6)** `turbar.archertur.2.5` | tur | protection | 2 | 3000 | 0 | 0 | 4250 | 0 | 0 | 15.62 |
| **Barracks 17c archertur protection +2 (lvl 7)** `turbar.archertur.2.6` | tur | protection | 2 | 5001 | 0 | 0 | 8101 | 0 | 0 | 15.62 |
| **Barracks 17c bagpiper protection +10 (lvl 2)** `scobar.bagpiper.2.1` | sco | protection | 10 | 706 | 0 | 0 | 50 | 0 | 0 | 15.62 |
| **Barracks 17c drummer protection +12 (lvl 2)** `prubar.drummer.2.1` | den,hun,pru,sax | protection | 12 | 1205 | 0 | 0 | 90 | 0 | 0 | 15.62 |
| **Barracks 17c drummer protection +12 (lvl 2)** `ausbar.drummer.2.1` | aus,spa,ven | protection | 12 | 706 | 0 | 0 | 50 | 0 | 0 | 15.62 |
| **Barracks 17c drummer protection +12 (lvl 2)** `swebar.drummer.2.1` | bav,por,swe | protection | 12 | 905 | 0 | 0 | 25 | 0 | 0 | 15.62 |
| **Barracks 17c drummer protection +12 (lvl 2)** `frabar.drummer.2.1` | fra,pie | protection | 12 | 500 | 0 | 0 | 75 | 0 | 0 | 15.62 |
| **Barracks 17c drummer protection +12 (lvl 2)** `engbar.drummer.2.1` | eng,swi | protection | 12 | 670 | 0 | 0 | 45 | 0 | 0 | 15.62 |
| **Barracks 17c drummer protection +12 (lvl 2)** `polbar.drummer.2.1` | pol | protection | 12 | 405 | 0 | 0 | 250 | 0 | 0 | 15.62 |
| **Barracks 17c drummer protection +12 (lvl 2)** `netbar.drummer.2.1` | net | protection | 12 | 845 | 0 | 0 | 95 | 0 | 0 | 15.62 |
| **Barracks 17c drummerrus protection +10 (lvl 2)** `rusbar.drummerrus.2.1` | rus | protection | 10 | 706 | 0 | 0 | 50 | 0 | 0 | 15.62 |
| **Barracks 17c drummertur protection +10 (lvl 2)** `turbar.drummertur.2.1` | alg,tur | protection | 10 | 706 | 0 | 0 | 50 | 0 | 0 | 15.62 |
| **Barracks 17c gauduk damage +1 (lvl 2)** `hunbar.gauduk.1.1` | hun | damage | 1 | 500 | 0 | 0 | 125 | 0 | 0 | 15.62 |
| **Barracks 17c gauduk damage +1 (lvl 3)** `hunbar.gauduk.1.2` | hun | damage | 1 | 1250 | 0 | 0 | 275 | 0 | 0 | 15.62 |
| **Barracks 17c gauduk damage +2 (lvl 4)** `hunbar.gauduk.1.3` | hun | damage | 2 | 2500 | 0 | 0 | 650 | 0 | 0 | 15.62 |
| **Barracks 17c gauduk protection +1 (lvl 2)** `hunbar.gauduk.2.1` | hun | protection | 1 | 125 | 0 | 0 | 150 | 100 | 0 | 15.62 |
| **Barracks 17c gauduk protection +1 (lvl 3)** `hunbar.gauduk.2.2` | hun | protection | 1 | 375 | 0 | 0 | 100 | 200 | 0 | 15.62 |
| **Barracks 17c gauduk protection +2 (lvl 4)** `hunbar.gauduk.2.3` | hun | protection | 2 | 1570 | 0 | 0 | 300 | 450 | 0 | 15.62 |
| **Barracks 17c gauduk protection +1 (lvl 5)** `hunbar.gauduk.2.4` | hun | protection | 1 | 2556 | 0 | 0 | 350 | 400 | 0 | 15.62 |
| **Barracks 17c gauduk protection +1 (lvl 6)** `hunbar.gauduk.2.5` | hun | protection | 1 | 2060 | 0 | 0 | 450 | 100 | 0 | 15.62 |
| **Barracks 17c gauduk protection +2 (lvl 7)** `hunbar.gauduk.2.6` | hun | protection | 2 | 2700 | 0 | 0 | 950 | 600 | 0 | 15.62 |
| **Barracks 17c jannisary damage +1 (lvl 2)** `turbar.jannisary.1.1` | tur | damage | 1 | 2000 | 0 | 0 | 100 | 0 | 0 | 15.62 |
| **Barracks 17c jannisary damage +1 (lvl 3)** `turbar.jannisary.1.2` | tur | damage | 1 | 1000 | 0 | 0 | 300 | 0 | 0 | 15.62 |
| **Barracks 17c jannisary damage +2 (lvl 4)** `turbar.jannisary.1.3` | tur | damage | 2 | 500 | 0 | 0 | 700 | 0 | 0 | 15.62 |
| `turbar.jannisary.1.4` | tur | +damage | 1 | 5000 | 0 | 0 | 1600 | 0 | 0 | 15.62 |
| `turbar.jannisary.1.5` | tur | +damage | 2 | 7500 | 0 | 0 | 3200 | 0 | 0 | 15.62 |
| `turbar.jannisary.1.6` | tur | +damage | 3 | 10000 | 0 | 0 | 4800 | 0 | 0 | 15.62 |
| **Barracks 17c jannisary protection +1 (lvl 2)** `turbar.jannisary.2.1` | tur | protection | 1 | 170 | 0 | 0 | 50 | 100 | 0 | 15.62 |
| **Barracks 17c jannisary protection +2 (lvl 3)** `turbar.jannisary.2.2` | tur | protection | 2 | 405 | 0 | 0 | 150 | 200 | 0 | 15.62 |
| **Barracks 17c jannisary protection +2 (lvl 4)** `turbar.jannisary.2.3` | tur | protection | 2 | 1570 | 0 | 0 | 100 | 350 | 0 | 15.62 |
| **Barracks 17c jannisary protection +1 (lvl 5)** `turbar.jannisary.2.4` | tur | protection | 1 | 1556 | 0 | 0 | 550 | 100 | 0 | 15.62 |
| **Barracks 17c jannisary protection +2 (lvl 6)** `turbar.jannisary.2.5` | tur | protection | 2 | 1060 | 0 | 0 | 850 | 400 | 0 | 15.62 |
| **Barracks 17c jannisary protection +2 (lvl 7)** `turbar.jannisary.2.6` | tur | protection | 2 | 4700 | 0 | 0 | 450 | 700 | 0 | 15.62 |
| **Barracks 17c lightinfantry damage +1 (lvl 2)** `turbar.lightinfantry.1.1` | alg,tur | damage | 1 | 100 | 0 | 0 | 50 | 0 | 0 | 15.62 |
| **Barracks 17c lightinfantry damage +1 (lvl 3)** `turbar.lightinfantry.1.2` | alg,tur | damage | 1 | 1100 | 0 | 0 | 200 | 0 | 0 | 15.62 |
| **Barracks 17c lightinfantry damage +11300 (lvl 4)** `turbar.lightinfantry.1.3` | tur | damage | 11300 | 325 | 0 | 0 | 0 | 0 | 0 | 15.62 |
| **Barracks 17c lightinfantry damage +1 (lvl 4)** `algbar.lightinfantry.1.3` | alg | damage | 1 | 1300 | 0 | 0 | 325 | 0 | 0 | 15.62 |
| `turbar.lightinfantry.1.4` | tur | +damage | 1 | 3000 | 0 | 0 | 360 | 0 | 0 | 15.62 |
| `algbar.lightinfantry.1.4` | alg | +damage | 2 | 3000 | 0 | 0 | 360 | 0 | 0 | 15.62 |
| `turbar.lightinfantry.1.5` | tur | +damage | 1 | 4500 | 0 | 0 | 540 | 0 | 0 | 15.62 |
| `algbar.lightinfantry.1.5` | alg | +damage | 2 | 4500 | 0 | 0 | 540 | 0 | 0 | 15.62 |
| `turbar.lightinfantry.1.6` | tur | +damage | 2 | 9375 | 0 | 0 | 1125 | 0 | 0 | 15.62 |
| `algbar.lightinfantry.1.6` | alg | +damage | 3 | 9375 | 0 | 0 | 1125 | 0 | 0 | 15.62 |
| **Barracks 17c lightinfantry protection +1 (lvl 2)** `turbar.lightinfantry.2.1` | alg,tur | protection | 1 | 200 | 0 | 0 | 70 | 120 | 0 | 15.62 |
| **Barracks 17c lightinfantry protection +1 (lvl 3)** `turbar.lightinfantry.2.2` | alg,tur | protection | 1 | 6360 | 0 | 0 | 150 | 320 | 0 | 15.62 |
| **Barracks 17c lightinfantry protection +2 (lvl 4)** `turbar.lightinfantry.2.3` | alg,tur | protection | 2 | 506 | 0 | 0 | 250 | 420 | 0 | 15.62 |
| `turbar.lightinfantry.2.4` | alg,tur | +protection | 1 | 3600 | 0 | 0 | 600 | 0 | 0 | 15.62 |
| `turbar.lightinfantry.2.5` | alg,tur | +protection | 1 | 5400 | 0 | 0 | 900 | 0 | 0 | 15.62 |
| `turbar.lightinfantry.2.6` | alg,tur | +protection | 2 | 11250 | 0 | 0 | 1875 | 0 | 0 | 15.62 |
| **Barracks 17c musketeer damage +1 (lvl 2)** `prubar.musketeer.1.1` | den,pie,pru,sax,swi,ven | damage | 1 | 2000 | 0 | 0 | 100 | 0 | 0 | 15.62 |
| **Barracks 17c musketeer damage +1 (lvl 2)** `swebar.musketeer.1.1` | bav,por,swe | damage | 1 | 1000 | 0 | 0 | 200 | 0 | 0 | 15.62 |
| **Barracks 17c musketeer damage +1 (lvl 2)** `frabar.musketeer.1.1` | fra | damage | 1 | 100 | 0 | 0 | 50 | 0 | 0 | 15.62 |
| **Barracks 17c musketeer damage +1 (lvl 2)** `engbar.musketeer.1.1` | eng | damage | 1 | 1900 | 0 | 0 | 150 | 0 | 0 | 15.62 |
| **Barracks 17c musketeer damage +1 (lvl 3)** `engbar.musketeer.1.2` | den,eng,pie,pru,sax,swi,ven | damage | 1 | 1000 | 0 | 0 | 300 | 0 | 0 | 15.62 |
| **Barracks 17c musketeer damage +1 (lvl 3)** `swebar.musketeer.1.2` | bav,por,swe | damage | 1 | 2000 | 0 | 0 | 200 | 0 | 0 | 15.62 |
| **Barracks 17c musketeer damage +1 (lvl 3)** `frabar.musketeer.1.2` | fra | damage | 1 | 3000 | 0 | 0 | 500 | 0 | 0 | 15.62 |
| **Barracks 17c musketeer damage +2 (lvl 4)** `engbar.musketeer.1.3` | den,eng,pie,pru,sax,swi,ven | damage | 2 | 500 | 0 | 0 | 700 | 0 | 0 | 15.62 |
| **Barracks 17c musketeer damage +2 (lvl 4)** `swebar.musketeer.1.3` | bav,por,swe | damage | 2 | 100 | 0 | 0 | 200 | 0 | 0 | 15.62 |
| **Barracks 17c musketeer damage +2 (lvl 4)** `frabar.musketeer.1.3` | fra | damage | 2 | 2500 | 0 | 0 | 750 | 0 | 0 | 15.62 |
| **Barracks 17c musketeer protection +1 (lvl 2)** `prubar.musketeer.2.1` | den,pie,pru,sax,swi,ven | protection | 1 | 170 | 0 | 0 | 50 | 100 | 0 | 15.62 |
| **Barracks 17c musketeer protection +1 (lvl 2)** `swebar.musketeer.2.1` | bav,por,swe | protection | 1 | 450 | 0 | 0 | 550 | 300 | 0 | 15.62 |
| **Barracks 17c musketeer protection +1 (lvl 2)** `frabar.musketeer.2.1` | fra | protection | 1 | 200 | 0 | 0 | 75 | 200 | 0 | 15.62 |
| **Barracks 17c musketeer protection +1 (lvl 2)** `engbar.musketeer.2.1` | eng | protection | 1 | 220 | 0 | 0 | 50 | 100 | 0 | 15.62 |
| **Barracks 17c musketeer protection +2 (lvl 3)** `prubar.musketeer.2.2` | den,pie,pru,sax,swi,ven | protection | 2 | 405 | 0 | 0 | 150 | 200 | 0 | 15.62 |
| **Barracks 17c musketeer protection +2 (lvl 3)** `swebar.musketeer.2.2` | bav,por,swe | protection | 2 | 405 | 0 | 0 | 150 | 20 | 0 | 15.62 |
| **Barracks 17c musketeer protection +2 (lvl 3)** `frabar.musketeer.2.2` | fra | protection | 2 | 705 | 0 | 0 | 250 | 250 | 0 | 15.62 |
| **Barracks 17c musketeer protection +2 (lvl 3)** `engbar.musketeer.2.2` | eng | protection | 2 | 505 | 0 | 0 | 140 | 200 | 0 | 15.62 |
| **Barracks 17c musketeer protection +2 (lvl 4)** `prubar.musketeer.2.3` | den,pie,pru,sax,swi,ven | protection | 2 | 1570 | 0 | 0 | 100 | 350 | 0 | 15.62 |
| **Barracks 17c musketeer protection +2 (lvl 4)** `swebar.musketeer.2.3` | bav,por,swe | protection | 2 | 1570 | 0 | 0 | 100 | 290 | 0 | 15.62 |
| **Barracks 17c musketeer protection +2 (lvl 4)** `frabar.musketeer.2.3` | fra | protection | 2 | 2560 | 0 | 0 | 300 | 450 | 0 | 15.62 |
| **Barracks 17c musketeer protection +2 (lvl 4)** `engbar.musketeer.2.3` | eng | protection | 2 | 1670 | 0 | 0 | 100 | 350 | 0 | 15.62 |
| **Barracks 17c musketeer protection +1 (lvl 5)** `frabar.musketeer.2.4` | den,fra,pie,pru,sax,swi,ven | protection | 1 | 1556 | 0 | 0 | 550 | 100 | 0 | 15.62 |
| **Barracks 17c musketeer protection +1 (lvl 5)** `swebar.musketeer.2.4` | bav,por,swe | protection | 1 | 1956 | 0 | 0 | 450 | 700 | 0 | 15.62 |
| **Barracks 17c musketeer protection +1 (lvl 5)** `engbar.musketeer.2.4` | eng | protection | 1 | 1000 | 0 | 0 | 920 | 100 | 0 | 15.62 |
| **Barracks 17c musketeer protection +2 (lvl 6)** `frabar.musketeer.2.5` | den,fra,pie,pru,sax,swi,ven | protection | 2 | 1060 | 0 | 0 | 850 | 400 | 0 | 15.62 |
| **Barracks 17c musketeer protection +2 (lvl 6)** `porbar.musketeer.2.5` | bav,por | protection | 2 | 1660 | 0 | 0 | 550 | 400 | 0 | 15.62 |
| **Barracks 17c musketeer protection +2 (lvl 6)** `engbar.musketeer.2.5` | eng | protection | 2 | 1060 | 0 | 0 | 700 | 400 | 0 | 15.62 |
| **Barracks 17c musketeer protection +2 (lvl 6)** `swebar.musketeer.2.5` | swe | protection | 2 | 1660 | 0 | 0 | 650 | 400 | 0 | 15.62 |
| **Barracks 17c musketeer protection +2 (lvl 7)** `prubar.musketeer.2.6` | den,pie,pru,sax,swi,ven | protection | 2 | 3700 | 0 | 0 | 450 | 700 | 0 | 15.62 |
| **Barracks 17c musketeer protection +2 (lvl 7)** `frabar.musketeer.2.6` | fra | protection | 2 | 3700 | 0 | 0 | 650 | 700 | 0 | 15.62 |
| **Barracks 17c musketeer protection +2 (lvl 7)** `engbar.musketeer.2.6` | eng | protection | 2 | 3900 | 0 | 0 | 550 | 700 | 0 | 15.62 |
| **Barracks 17c musketeer protection +2 (lvl 7)** `swebar.musketeer.2.6` | swe | protection | 2 | 2700 | 0 | 0 | 650 | 100 | 0 | 15.62 |
| **Barracks 17c musketeer protection +2 (lvl 7)** `porbar.musketeer.2.6` | por | protection | 2 | 2700 | 0 | 0 | 850 | 100 | 0 | 15.62 |
| **Barracks 17c musketeer protection +2 (lvl 7)** `bavbar.musketeer.2.6` | bav | protection | 2 | 2700 | 0 | 0 | 750 | 100 | 0 | 15.62 |
| **Barracks 17c musketeeraus damage +1 (lvl 2)** `ausbar.musketeeraus.1.1` | aus | damage | 1 | 2000 | 0 | 0 | 100 | 0 | 0 | 15.62 |
| **Barracks 17c musketeeraus damage +1 (lvl 3)** `ausbar.musketeeraus.1.2` | aus | damage | 1 | 1000 | 0 | 0 | 300 | 0 | 0 | 15.62 |
| **Barracks 17c musketeeraus damage +2 (lvl 4)** `ausbar.musketeeraus.1.3` | aus | damage | 2 | 500 | 0 | 0 | 700 | 0 | 0 | 15.62 |
| **Barracks 17c musketeeraus protection +1 (lvl 2)** `ausbar.musketeeraus.2.1` | aus | protection | 1 | 170 | 0 | 0 | 50 | 100 | 0 | 15.62 |
| **Barracks 17c musketeeraus protection +1 (lvl 3)** `ausbar.musketeeraus.2.2` | aus | protection | 1 | 405 | 0 | 0 | 150 | 200 | 0 | 15.62 |
| **Barracks 17c musketeeraus protection +1 (lvl 4)** `ausbar.musketeeraus.2.3` | aus | protection | 1 | 1570 | 0 | 0 | 100 | 350 | 0 | 15.62 |
| **Barracks 17c musketeeraus protection +1 (lvl 5)** `ausbar.musketeeraus.2.4` | aus | protection | 1 | 1556 | 0 | 0 | 550 | 100 | 0 | 15.62 |
| **Barracks 17c musketeeraus protection +1 (lvl 6)** `ausbar.musketeeraus.2.5` | aus | protection | 1 | 1060 | 0 | 0 | 850 | 400 | 0 | 15.62 |
| **Barracks 17c musketeeraus protection +1 (lvl 7)** `ausbar.musketeeraus.2.6` | aus | protection | 1 | 3700 | 0 | 0 | 750 | 700 | 0 | 15.62 |
| **Barracks 17c musketeernet damage +1 (lvl 2)** `netbar.musketeernet.1.1` | net | damage | 1 | 2000 | 0 | 0 | 100 | 0 | 0 | 15.62 |
| **Barracks 17c musketeernet damage +1 (lvl 3)** `netbar.musketeernet.1.2` | net | damage | 1 | 1000 | 0 | 0 | 300 | 0 | 0 | 15.62 |
| **Barracks 17c musketeernet damage +2 (lvl 4)** `netbar.musketeernet.1.3` | net | damage | 2 | 500 | 0 | 0 | 700 | 0 | 0 | 15.62 |
| **Barracks 17c musketeernet protection +1 (lvl 2)** `netbar.musketeernet.2.1` | net | protection | 1 | 170 | 0 | 0 | 50 | 100 | 0 | 15.62 |
| **Barracks 17c musketeernet protection +1 (lvl 3)** `netbar.musketeernet.2.2` | net | protection | 1 | 405 | 0 | 0 | 150 | 200 | 0 | 15.62 |
| **Barracks 17c musketeernet protection +2 (lvl 4)** `netbar.musketeernet.2.3` | net | protection | 2 | 1570 | 0 | 0 | 100 | 350 | 0 | 15.62 |
| **Barracks 17c musketeernet protection +1 (lvl 5)** `netbar.musketeernet.2.4` | net | protection | 1 | 1556 | 0 | 0 | 550 | 100 | 0 | 15.62 |
| **Barracks 17c musketeernet protection +1 (lvl 6)** `netbar.musketeernet.2.5` | net | protection | 1 | 1060 | 0 | 0 | 850 | 400 | 0 | 15.62 |
| **Barracks 17c musketeernet protection +2 (lvl 7)** `netbar.musketeernet.2.6` | net | protection | 2 | 3700 | 0 | 0 | 450 | 700 | 0 | 15.62 |
| **Barracks 17c musketeerpol damage +1 (lvl 2)** `polbar.musketeerpol.1.1` | pol | damage | 1 | 500 | 0 | 0 | 125 | 0 | 0 | 15.62 |
| **Barracks 17c musketeerpol damage +1 (lvl 3)** `polbar.musketeerpol.1.2` | pol | damage | 1 | 1250 | 0 | 0 | 275 | 0 | 0 | 15.62 |
| **Barracks 17c musketeerpol damage +2 (lvl 4)** `polbar.musketeerpol.1.3` | pol | damage | 2 | 2500 | 0 | 0 | 650 | 0 | 0 | 15.62 |
| **Barracks 17c musketeerpol protection +1 (lvl 2)** `polbar.musketeerpol.2.1` | pol | protection | 1 | 125 | 0 | 0 | 150 | 100 | 0 | 15.62 |
| **Barracks 17c musketeerpol protection +1 (lvl 3)** `polbar.musketeerpol.2.2` | pol | protection | 1 | 375 | 0 | 0 | 100 | 200 | 0 | 15.62 |
| **Barracks 17c musketeerpol protection +2 (lvl 4)** `polbar.musketeerpol.2.3` | pol | protection | 2 | 1570 | 0 | 0 | 300 | 450 | 0 | 15.62 |
| **Barracks 17c musketeerpol protection +1 (lvl 5)** `polbar.musketeerpol.2.4` | pol | protection | 1 | 2556 | 0 | 0 | 350 | 400 | 0 | 15.62 |
| **Barracks 17c musketeerpol protection +1 (lvl 6)** `polbar.musketeerpol.2.5` | pol | protection | 1 | 3060 | 0 | 0 | 650 | 100 | 0 | 15.62 |
| **Barracks 17c musketeerpol protection +2 (lvl 7)** `polbar.musketeerpol.2.6` | pol | protection | 2 | 2700 | 0 | 0 | 750 | 600 | 0 | 15.62 |
| **Barracks 17c musketeersco damage +1 (lvl 2)** `scobar.musketeersco.1.1` | sco | damage | 1 | 2500 | 0 | 0 | 200 | 0 | 0 | 15.62 |
| **Barracks 17c musketeersco damage +1 (lvl 3)** `scobar.musketeersco.1.2` | sco | damage | 1 | 1500 | 0 | 0 | 400 | 0 | 0 | 15.62 |
| **Barracks 17c musketeersco damage +2 (lvl 4)** `scobar.musketeersco.1.3` | sco | damage | 2 | 500 | 0 | 0 | 800 | 0 | 0 | 15.62 |
| **Barracks 17c musketeersco protection +1 (lvl 2)** `scobar.musketeersco.2.1` | sco | protection | 1 | 250 | 0 | 0 | 30 | 0 | 0 | 15.62 |
| **Barracks 17c musketeersco protection +1 (lvl 3)** `scobar.musketeersco.2.2` | sco | protection | 1 | 500 | 0 | 0 | 400 | 60 | 0 | 15.62 |
| **Barracks 17c musketeersco protection +2 (lvl 4)** `scobar.musketeersco.2.3` | sco | protection | 2 | 875 | 0 | 0 | 225 | 0 | 0 | 15.62 |
| **Barracks 17c musketeersco protection +1 (lvl 5)** `scobar.musketeersco.2.4` | sco | protection | 1 | 4200 | 0 | 0 | 240 | 0 | 0 | 15.62 |
| **Barracks 17c musketeersco protection +1 (lvl 6)** `scobar.musketeersco.2.5` | sco | protection | 1 | 6300 | 0 | 0 | 360 | 0 | 0 | 15.62 |
| **Barracks 17c musketeersco protection +2 (lvl 7)** `scobar.musketeersco.2.6` | sco | protection | 2 | 13125 | 0 | 0 | 750 | 0 | 0 | 15.62 |
| **Barracks 17c musketeerspa damage +1 (lvl 2)** `spabar.musketeerspa.1.1` | spa | damage | 1 | 2000 | 0 | 0 | 100 | 0 | 0 | 15.62 |
| **Barracks 17c musketeerspa damage +1 (lvl 3)** `spabar.musketeerspa.1.2` | spa | damage | 1 | 1000 | 0 | 0 | 300 | 0 | 0 | 15.62 |
| **Barracks 17c musketeerspa damage +2 (lvl 4)** `spabar.musketeerspa.1.3` | spa | damage | 2 | 500 | 0 | 0 | 700 | 0 | 0 | 15.62 |
| **Barracks 17c musketeerspa protection +1 (lvl 2)** `spabar.musketeerspa.2.1` | spa | protection | 1 | 170 | 0 | 0 | 50 | 100 | 0 | 15.62 |
| **Barracks 17c musketeerspa protection +1 (lvl 3)** `spabar.musketeerspa.2.2` | spa | protection | 1 | 405 | 0 | 0 | 150 | 200 | 0 | 15.62 |
| **Barracks 17c musketeerspa protection +1 (lvl 4)** `spabar.musketeerspa.2.3` | spa | protection | 1 | 1570 | 0 | 0 | 100 | 350 | 0 | 15.62 |
| **Barracks 17c musketeerspa protection +1 (lvl 5)** `spabar.musketeerspa.2.4` | spa | protection | 1 | 1556 | 0 | 0 | 550 | 100 | 0 | 15.62 |
| **Barracks 17c musketeerspa protection +1 (lvl 6)** `spabar.musketeerspa.2.5` | spa | protection | 1 | 1060 | 0 | 0 | 850 | 400 | 0 | 15.62 |
| **Barracks 17c musketeerspa protection +1 (lvl 7)** `spabar.musketeerspa.2.6` | spa | protection | 1 | 3700 | 0 | 0 | 650 | 700 | 0 | 15.62 |
| **Barracks 17c officer damage +20 (lvl 2)** `ausbar.officer.1.1` | aus,pie,spa,ven | damage | 20 | 100 | 0 | 0 | 50 | 0 | 0 | 15.62 |
| **Barracks 17c officer damage +20 (lvl 2)** `prubar.officer.1.1` | den,hun,pru,sax | damage | 20 | 150 | 0 | 0 | 25 | 0 | 0 | 15.62 |
| **Barracks 17c officer damage +20 (lvl 2)** `swebar.officer.1.1` | bav,por,swe | damage | 20 | 800 | 0 | 0 | 150 | 0 | 0 | 15.62 |
| **Barracks 17c officer damage +20 (lvl 2)** `frabar.officer.1.1` | fra,swi | damage | 20 | 200 | 0 | 0 | 25 | 0 | 0 | 15.62 |
| **Barracks 17c officer damage +20 (lvl 2)** `engbar.officer.1.1` | eng | damage | 20 | 250 | 0 | 0 | 75 | 0 | 0 | 15.62 |
| **Barracks 17c officer damage +20 (lvl 2)** `polbar.officer.1.1` | pol | damage | 20 | 50 | 0 | 0 | 150 | 0 | 0 | 15.62 |
| **Barracks 17c officer damage +20 (lvl 2)** `netbar.officer.1.1` | net | damage | 20 | 500 | 0 | 0 | 25 | 0 | 0 | 15.62 |
| **Barracks 17c officer protection +6 (lvl 2)** `prubar.officer.2.1` | den,hun,pru,sax,swi | protection | 6 | 1650 | 0 | 0 | 395 | 0 | 0 | 15.62 |
| **Barracks 17c officer protection +6 (lvl 2)** `swebar.officer.2.1` | bav,pie,por,swe | protection | 6 | 1050 | 0 | 0 | 350 | 0 | 0 | 15.62 |
| **Barracks 17c officer protection +6 (lvl 2)** `ausbar.officer.2.1` | aus,spa | protection | 6 | 1850 | 0 | 0 | 450 | 0 | 0 | 15.62 |
| **Barracks 17c officer protection +6 (lvl 2)** `frabar.officer.2.1` | fra | protection | 6 | 1950 | 0 | 0 | 350 | 0 | 0 | 15.62 |
| **Barracks 17c officer protection +6 (lvl 2)** `engbar.officer.2.1` | eng | protection | 6 | 1650 | 0 | 0 | 425 | 0 | 0 | 15.62 |
| **Barracks 17c officer protection +6 (lvl 2)** `polbar.officer.2.1` | pol | protection | 6 | 1550 | 0 | 0 | 650 | 0 | 0 | 15.62 |
| **Barracks 17c officer protection +6 (lvl 2)** `venbar.officer.2.1` | ven | protection | 6 | 1450 | 0 | 0 | 450 | 0 | 0 | 15.62 |
| **Barracks 17c officer protection +6 (lvl 2)** `netbar.officer.2.1` | net | protection | 6 | 1550 | 0 | 0 | 475 | 0 | 0 | 15.62 |
| **Barracks 17c officerrus damage +30 (lvl 2)** `rusbar.officerrus.1.1` | rus | damage | 30 | 100 | 0 | 0 | 50 | 0 | 0 | 15.62 |
| **Barracks 17c officerrus protection +10 (lvl 2)** `rusbar.officerrus.2.1` | rus | protection | 10 | 1850 | 0 | 0 | 450 | 0 | 0 | 15.62 |
| **Barracks 17c officersco damage +30 (lvl 2)** `scobar.officersco.1.1` | sco | damage | 30 | 250 | 0 | 0 | 75 | 0 | 0 | 15.62 |
| **Barracks 17c officersco protection +10 (lvl 2)** `scobar.officersco.2.1` | sco | protection | 10 | 1550 | 0 | 0 | 425 | 0 | 0 | 15.62 |
| **Barracks 17c officertur damage +20 (lvl 2)** `turbar.officertur.1.1` | alg,tur | damage | 20 | 1000 | 0 | 0 | 800 | 0 | 0 | 15.62 |
| **Barracks 17c officertur protection +10 (lvl 2)** `turbar.officertur.2.1` | alg,tur | protection | 10 | 1706 | 0 | 0 | 350 | 0 | 0 | 15.62 |
| **Barracks 17c pikeman damage +1 (lvl 2)** `ausbar.pikeman.1.1` | aus,eng,pie,spa,ven | damage | 1 | 200 | 0 | 0 | 50 | 0 | 0 | 15.62 |
| **Barracks 17c pikeman damage +1 (lvl 2)** `swebar.pikeman.1.1` | hun,sax,swe | damage | 1 | 100 | 0 | 0 | 90 | 0 | 0 | 15.62 |
| **Barracks 17c pikeman damage +1 (lvl 2)** `prubar.pikeman.1.1` | bav,den,pru | damage | 1 | 3600 | 0 | 0 | 450 | 0 | 0 | 15.62 |
| **Barracks 17c pikeman damage +1 (lvl 2)** `frabar.pikeman.1.1` | fra | damage | 1 | 100 | 0 | 0 | 25 | 0 | 0 | 15.62 |
| **Barracks 17c pikeman damage +1 (lvl 2)** `netbar.pikeman.1.1` | net | damage | 1 | 900 | 0 | 0 | 150 | 0 | 0 | 15.62 |
| **Barracks 17c pikeman damage +2 (lvl 3)** `ausbar.pikeman.1.2` | aus,bav,den,pie,pru,spa,ven | damage | 2 | 1300 | 0 | 0 | 300 | 0 | 0 | 15.62 |
| **Barracks 17c pikeman damage +2 (lvl 3)** `swebar.pikeman.1.2` | hun,sax,swe | damage | 2 | 300 | 0 | 0 | 450 | 0 | 0 | 15.62 |
| **Barracks 17c pikeman damage +2 (lvl 3)** `frabar.pikeman.1.2` | fra | damage | 2 | 1400 | 0 | 0 | 325 | 0 | 0 | 15.62 |
| **Barracks 17c pikeman damage +2 (lvl 3)** `engbar.pikeman.1.2` | eng | damage | 2 | 1250 | 0 | 0 | 310 | 0 | 0 | 15.62 |
| **Barracks 17c pikeman damage +2 (lvl 3)** `netbar.pikeman.1.2` | net | damage | 2 | 700 | 0 | 0 | 400 | 0 | 0 | 15.62 |
| **Barracks 17c pikeman damage +2 (lvl 4)** `ausbar.pikeman.1.3` | aus,pie,spa,ven | damage | 2 | 3600 | 0 | 0 | 450 | 0 | 0 | 15.62 |
| **Barracks 17c pikeman damage +2 (lvl 4)** `swebar.pikeman.1.3` | hun,sax,swe | damage | 2 | 4600 | 0 | 0 | 300 | 0 | 0 | 15.62 |
| **Barracks 17c pikeman damage +2 (lvl 4)** `prubar.pikeman.1.3` | bav,den,pru | damage | 2 | 200 | 0 | 0 | 50 | 0 | 0 | 15.62 |
| **Barracks 17c pikeman damage +2 (lvl 4)** `frabar.pikeman.1.3` | fra | damage | 2 | 4600 | 0 | 0 | 650 | 0 | 0 | 15.62 |
| **Barracks 17c pikeman damage +2 (lvl 4)** `engbar.pikeman.1.3` | eng | damage | 2 | 3900 | 0 | 0 | 650 | 0 | 0 | 15.62 |
| **Barracks 17c pikeman damage +2 (lvl 4)** `netbar.pikeman.1.3` | net | damage | 2 | 3100 | 0 | 0 | 250 | 0 | 0 | 15.62 |
| **Barracks 17c pikeman damage +1 (lvl 5)** `ausbar.pikeman.1.4` | aus,eng,pie,spa,ven | damage | 1 | 7200 | 0 | 0 | 1850 | 0 | 0 | 15.62 |
| **Barracks 17c pikeman damage +1 (lvl 5)** `swebar.pikeman.1.4` | hun,sax,swe | damage | 1 | 9200 | 0 | 0 | 1250 | 0 | 0 | 15.62 |
| **Barracks 17c pikeman damage +1 (lvl 5)** `prubar.pikeman.1.4` | bav,den,pru | damage | 1 | 6800 | 0 | 0 | 1950 | 0 | 0 | 15.62 |
| **Barracks 17c pikeman damage +1 (lvl 5)** `frabar.pikeman.1.4` | fra | damage | 1 | 6200 | 0 | 0 | 1650 | 0 | 0 | 15.62 |
| **Barracks 17c pikeman damage +1 (lvl 5)** `netbar.pikeman.1.4` | net | damage | 1 | 6700 | 0 | 0 | 1950 | 0 | 0 | 15.62 |
| **Barracks 17c pikeman damage +2 (lvl 6)** `ausbar.pikeman.1.5` | aus,eng,net,pie,spa,ven | damage | 2 | 16030 | 0 | 0 | 2000 | 0 | 0 | 15.62 |
| **Barracks 17c pikeman damage +2 (lvl 6)** `swebar.pikeman.1.5` | hun,sax,swe | damage | 2 | 14030 | 0 | 0 | 2600 | 0 | 0 | 15.62 |
| **Barracks 17c pikeman damage +2 (lvl 6)** `prubar.pikeman.1.5` | bav,den,pru | damage | 2 | 15030 | 0 | 0 | 2300 | 0 | 0 | 15.62 |
| **Barracks 17c pikeman damage +2 (lvl 6)** `frabar.pikeman.1.5` | fra | damage | 2 | 15300 | 0 | 0 | 2075 | 0 | 0 | 15.62 |
| `ausbar.pikeman.1.6` | aus,bav,den,eng,fra,hun,net,pie,pru,sax,spa,swe,ven | +damage | 2 | 15000 | 0 | 0 | 1875 | 0 | 0 | 15.62 |
| **Barracks 17c pikeman protection +1 (lvl 2)** `ausbar.pikeman.2.1` | aus,pie,spa,ven | protection | 1 | 150 | 0 | 0 | 50 | 0 | 0 | 15.62 |
| **Barracks 17c pikeman protection +1 (lvl 2)** `prubar.pikeman.2.1` | den,hun,pru,sax | protection | 1 | 175 | 0 | 0 | 40 | 0 | 0 | 15.62 |
| **Barracks 17c pikeman protection +1 (lvl 2)** `swebar.pikeman.2.1` | bav,swe | protection | 1 | 350 | 0 | 0 | 50 | 0 | 0 | 15.62 |
| **Barracks 17c pikeman protection +1 (lvl 2)** `frabar.pikeman.2.1` | fra | protection | 1 | 350 | 0 | 0 | 90 | 0 | 0 | 15.62 |
| **Barracks 17c pikeman protection +1 (lvl 2)** `engbar.pikeman.2.1` | eng | protection | 1 | 990 | 0 | 0 | 50 | 0 | 0 | 15.62 |
| **Barracks 17c pikeman protection +1 (lvl 2)** `netbar.pikeman.2.1` | net | protection | 1 | 250 | 0 | 0 | 150 | 0 | 0 | 15.62 |
| **Barracks 17c pikeman protection +1 (lvl 3)** `ausbar.pikeman.2.2` | aus,pie,spa,ven | protection | 1 | 900 | 0 | 0 | 175 | 0 | 0 | 15.62 |
| **Barracks 17c pikeman protection +1 (lvl 3)** `prubar.pikeman.2.2` | den,hun,pru,sax | protection | 1 | 990 | 0 | 0 | 275 | 0 | 0 | 15.62 |
| **Barracks 17c pikeman protection +1 (lvl 3)** `swebar.pikeman.2.2` | bav,swe | protection | 1 | 700 | 0 | 0 | 275 | 0 | 0 | 15.62 |
| **Barracks 17c pikeman protection +1 (lvl 3)** `frabar.pikeman.2.2` | fra | protection | 1 | 1000 | 0 | 0 | 135 | 0 | 0 | 15.62 |
| **Barracks 17c pikeman protection +1 (lvl 3)** `engbar.pikeman.2.2` | eng | protection | 1 | 200 | 0 | 0 | 175 | 0 | 0 | 15.62 |
| **Barracks 17c pikeman protection +1 (lvl 3)** `netbar.pikeman.2.2` | net | protection | 1 | 800 | 0 | 0 | 275 | 0 | 0 | 15.62 |
| **Barracks 17c pikeman protection +2 (lvl 4)** `ausbar.pikeman.2.3` | aus,eng,pie,spa,ven | protection | 2 | 4500 | 0 | 0 | 300 | 0 | 0 | 15.62 |
| **Barracks 17c pikeman protection +2 (lvl 4)** `prubar.pikeman.2.3` | den,hun,pru,sax | protection | 2 | 4700 | 0 | 0 | 280 | 0 | 0 | 15.62 |
| **Barracks 17c pikeman protection +2 (lvl 4)** `swebar.pikeman.2.3` | bav,swe | protection | 2 | 2500 | 0 | 0 | 200 | 0 | 0 | 15.62 |
| **Barracks 17c pikeman protection +2 (lvl 4)** `frabar.pikeman.2.3` | fra | protection | 2 | 4200 | 0 | 0 | 500 | 0 | 0 | 15.62 |
| **Barracks 17c pikeman protection +2 (lvl 4)** `netbar.pikeman.2.3` | net | protection | 2 | 4200 | 0 | 0 | 100 | 0 | 0 | 15.62 |
| **Barracks 17c pikeman protection +1 (lvl 5)** `ausbar.pikeman.2.4` | aus,eng,pie,spa,ven | protection | 1 | 9005 | 0 | 0 | 507 | 0 | 0 | 15.62 |
| **Barracks 17c pikeman protection +1 (lvl 5)** `prubar.pikeman.2.4` | hun,pru,sax | protection | 1 | 9505 | 0 | 0 | 707 | 0 | 0 | 15.62 |
| **Barracks 17c pikeman protection +1 (lvl 5)** `swebar.pikeman.2.4` | bav,swe | protection | 1 | 13005 | 0 | 0 | 997 | 0 | 0 | 15.62 |
| **Barracks 17c pikeman protection +1 (lvl 5)** `frabar.pikeman.2.4` | fra | protection | 1 | 11075 | 0 | 0 | 310 | 0 | 0 | 15.62 |
| **Barracks 17c pikeman protection +1 (lvl 5)** `netbar.pikeman.2.4` | net | protection | 1 | 9305 | 0 | 0 | 707 | 0 | 0 | 15.62 |
| **Barracks 17c pikeman protection +1 (lvl 5)** `denbar.pikeman.2.4` | den | protection | 1 | 9005 | 0 | 0 | 707 | 0 | 0 | 15.62 |
| **Barracks 17c pikeman protection +1 (lvl 6)** `ausbar.pikeman.2.5` | aus,pie,spa,ven | protection | 1 | 18010 | 0 | 0 | 3050 | 0 | 0 | 15.62 |
| **Barracks 17c pikeman protection +1 (lvl 6)** `prubar.pikeman.2.5` | den,hun,pru,sax | protection | 1 | 17510 | 0 | 0 | 2950 | 0 | 0 | 15.62 |
| **Barracks 17c pikeman protection +1 (lvl 6)** `swebar.pikeman.2.5` | bav,swe | protection | 1 | 16010 | 0 | 0 | 2550 | 0 | 0 | 15.62 |
| **Barracks 17c pikeman protection +1 (lvl 6)** `frabar.pikeman.2.5` | fra | protection | 1 | 15050 | 0 | 0 | 3050 | 0 | 0 | 15.62 |
| **Barracks 17c pikeman protection +1 (lvl 6)** `engbar.pikeman.2.5` | eng | protection | 1 | 17010 | 0 | 0 | 3050 | 0 | 0 | 15.62 |
| **Barracks 17c pikeman protection +1 (lvl 6)** `netbar.pikeman.2.5` | net | protection | 1 | 17890 | 0 | 0 | 2850 | 0 | 0 | 15.62 |
| `ausbar.pikeman.2.6` | aus,bav,den,eng,fra,hun,net,pie,pru,sax,spa,swe,ven | +protection | 2 | 11250 | 0 | 0 | 1500 | 0 | 0 | 15.62 |
| **Barracks 17c pikemanpol damage +1 (lvl 2)** `polbar.pikemanpol.1.1` | pol | damage | 1 | 500 | 0 | 0 | 50 | 0 | 0 | 15.62 |
| **Barracks 17c pikemanpol damage +1 (lvl 3)** `polbar.pikemanpol.1.2` | pol | damage | 1 | 1400 | 0 | 0 | 100 | 0 | 0 | 15.62 |
| **Barracks 17c pikemanpol damage +1 (lvl 4)** `polbar.pikemanpol.1.3` | pol | damage | 1 | 3200 | 0 | 0 | 450 | 0 | 0 | 15.62 |
| **Barracks 17c pikemanpol damage +2 (lvl 5)** `polbar.pikemanpol.1.4` | pol | damage | 2 | 8200 | 0 | 0 | 2220 | 0 | 0 | 15.62 |
| **Barracks 17c pikemanpol damage +2 (lvl 6)** `polbar.pikemanpol.1.5` | pol | damage | 2 | 15030 | 0 | 0 | 1800 | 0 | 0 | 15.62 |
| `polbar.pikemanpol.1.6` | pol | +damage | 3 | 22500 | 0 | 0 | 2800 | 0 | 0 | 15.62 |
| **Barracks 17c pikemanpol protection +1 (lvl 2)** `polbar.pikemanpol.2.1` | pol | protection | 1 | 250 | 0 | 0 | 75 | 0 | 0 | 15.62 |
| **Barracks 17c pikemanpol protection +1 (lvl 3)** `polbar.pikemanpol.2.2` | pol | protection | 1 | 800 | 0 | 0 | 150 | 0 | 0 | 15.62 |
| **Barracks 17c pikemanpol protection +2 (lvl 4)** `polbar.pikemanpol.2.3` | pol | protection | 2 | 3500 | 0 | 0 | 225 | 0 | 0 | 15.62 |
| **Barracks 17c pikemanpol protection +2 (lvl 5)** `polbar.pikemanpol.2.4` | pol | protection | 2 | 9005 | 0 | 0 | 407 | 0 | 0 | 15.62 |
| **Barracks 17c pikemanpol protection +4 (lvl 6)** `polbar.pikemanpol.2.5` | pol | protection | 4 | 19010 | 0 | 0 | 2975 | 0 | 0 | 15.62 |
| `polbar.pikemanpol.2.6` | pol | +protection | 3 | 15000 | 0 | 0 | 1000 | 0 | 0 | 15.62 |
| **Barracks 17c pikemanpor damage +1 (lvl 2)** `porbar.pikemanpor.1.1` | por | damage | 1 | 3600 | 0 | 0 | 450 | 0 | 0 | 15.62 |
| **Barracks 17c pikemanpor damage +1 (lvl 3)** `porbar.pikemanpor.1.2` | por | damage | 1 | 1300 | 0 | 0 | 300 | 0 | 0 | 15.62 |
| **Barracks 17c pikemanpor damage +2 (lvl 4)** `porbar.pikemanpor.1.3` | por | damage | 2 | 200 | 0 | 0 | 50 | 0 | 0 | 15.62 |
| **Barracks 17c pikemanpor damage +1 (lvl 5)** `porbar.pikemanpor.1.4` | por | damage | 1 | 6800 | 0 | 0 | 1950 | 0 | 0 | 15.62 |
| **Barracks 17c pikemanpor damage +2 (lvl 6)** `porbar.pikemanpor.1.5` | por | damage | 2 | 15030 | 0 | 0 | 2300 | 0 | 0 | 15.62 |
| `porbar.pikemanpor.1.6` | por | +damage | 3 | 15000 | 0 | 0 | 1875 | 0 | 0 | 15.62 |
| **Barracks 17c pikemanpor protection +1 (lvl 2)** `porbar.pikemanpor.2.1` | por | protection | 1 | 350 | 0 | 0 | 50 | 0 | 0 | 15.62 |
| **Barracks 17c pikemanpor protection +1 (lvl 3)** `porbar.pikemanpor.2.2` | por | protection | 1 | 700 | 0 | 0 | 275 | 0 | 0 | 15.62 |
| **Barracks 17c pikemanpor protection +2 (lvl 4)** `porbar.pikemanpor.2.3` | por | protection | 2 | 2500 | 0 | 0 | 200 | 0 | 0 | 15.62 |
| **Barracks 17c pikemanpor protection +1 (lvl 5)** `porbar.pikemanpor.2.4` | por | protection | 1 | 13005 | 0 | 0 | 997 | 0 | 0 | 15.62 |
| **Barracks 17c pikemanpor protection +2 (lvl 6)** `porbar.pikemanpor.2.5` | por | protection | 2 | 16010 | 0 | 0 | 2550 | 0 | 0 | 15.62 |
| `porbar.pikemanpor.2.6` | por | +protection | 3 | 11250 | 0 | 0 | 1500 | 0 | 0 | 15.62 |
| **Barracks 17c pikemanrus damage +1 (lvl 2)** `rusbar.pikemanrus.1.1` | rus | damage | 1 | 200 | 0 | 0 | 50 | 0 | 0 | 15.62 |
| **Barracks 17c pikemanrus damage +2 (lvl 3)** `rusbar.pikemanrus.1.2` | rus | damage | 2 | 1300 | 0 | 0 | 300 | 0 | 0 | 15.62 |
| **Barracks 17c pikemanrus damage +2 (lvl 4)** `rusbar.pikemanrus.1.3` | rus | damage | 2 | 3600 | 0 | 0 | 450 | 0 | 0 | 15.62 |
| **Barracks 17c pikemanrus damage +1 (lvl 5)** `rusbar.pikemanrus.1.4` | rus | damage | 1 | 7200 | 0 | 0 | 1850 | 0 | 0 | 15.62 |
| **Barracks 17c pikemanrus damage +2 (lvl 6)** `rusbar.pikemanrus.1.5` | rus | damage | 2 | 16030 | 0 | 0 | 2000 | 0 | 0 | 15.62 |
| `rusbar.pikemanrus.1.6` | rus | +damage | 2 | 15000 | 0 | 0 | 1875 | 0 | 0 | 15.62 |
| **Barracks 17c pikemanrus protection +1 (lvl 2)** `rusbar.pikemanrus.2.1` | rus | protection | 1 | 150 | 0 | 0 | 50 | 0 | 0 | 15.62 |
| **Barracks 17c pikemanrus protection +1 (lvl 3)** `rusbar.pikemanrus.2.2` | rus | protection | 1 | 900 | 0 | 0 | 175 | 0 | 0 | 15.62 |
| **Barracks 17c pikemanrus protection +2 (lvl 4)** `rusbar.pikemanrus.2.3` | rus | protection | 2 | 4500 | 0 | 0 | 300 | 0 | 0 | 15.62 |
| **Barracks 17c pikemanrus protection +1 (lvl 5)** `rusbar.pikemanrus.2.4` | rus | protection | 1 | 9005 | 0 | 0 | 507 | 0 | 0 | 15.62 |
| **Barracks 17c pikemanrus protection +1 (lvl 6)** `rusbar.pikemanrus.2.5` | rus | protection | 1 | 18010 | 0 | 0 | 3050 | 0 | 0 | 15.62 |
| `rusbar.pikemanrus.2.6` | rus | +protection | 2 | 11250 | 0 | 0 | 1500 | 0 | 0 | 15.62 |
| **Barracks 17c pikemansco damage +1 (lvl 2)** `scobar.pikemansco.1.1` | sco | damage | 1 | 250 | 0 | 0 | 70 | 0 | 0 | 15.62 |
| **Barracks 17c pikemansco damage +2 (lvl 3)** `scobar.pikemansco.1.2` | sco | damage | 2 | 750 | 0 | 0 | 210 | 0 | 0 | 15.62 |
| **Barracks 17c pikemansco damage +3 (lvl 4)** `scobar.pikemansco.1.3` | sco | damage | 3 | 2800 | 0 | 0 | 790 | 0 | 0 | 15.62 |
| **Barracks 17c pikemansco damage +1 (lvl 5)** `scobar.pikemansco.1.4` | sco | damage | 1 | 6000 | 0 | 0 | 750 | 0 | 0 | 15.62 |
| **Barracks 17c pikemansco damage +2 (lvl 6)** `scobar.pikemansco.1.5` | sco | damage | 2 | 10800 | 0 | 0 | 1350 | 0 | 0 | 15.62 |
| `scobar.pikemansco.1.6` | sco | +damage | 3 | 22500 | 0 | 0 | 2800 | 0 | 0 | 15.62 |
| **Barracks 17c pikemansco protection +1 (lvl 2)** `scobar.pikemansco.2.1` | sco | protection | 1 | 150 | 0 | 0 | 60 | 0 | 0 | 15.62 |
| **Barracks 17c pikemansco protection +2 (lvl 3)** `scobar.pikemansco.2.2` | sco | protection | 2 | 450 | 0 | 0 | 180 | 0 | 0 | 15.62 |
| **Barracks 17c pikemansco protection +3 (lvl 4)** `scobar.pikemansco.2.3` | sco | protection | 3 | 1690 | 0 | 0 | 675 | 0 | 0 | 15.62 |
| **Barracks 17c pikemansco protection +1 (lvl 5)** `scobar.pikemansco.2.4` | sco | protection | 1 | 4500 | 0 | 0 | 600 | 0 | 0 | 15.62 |
| **Barracks 17c pikemansco protection +2 (lvl 6)** `scobar.pikemansco.2.5` | sco | protection | 2 | 8100 | 0 | 0 | 1080 | 0 | 0 | 15.62 |
| `scobar.pikemansco.2.6` | sco | +protection | 3 | 16875 | 0 | 0 | 2250 | 0 | 0 | 15.62 |
| **Barracks 17c pikemanspa damage +1 (lvl 2)** `spabar.pikemanspa.1.1` | spa | damage | 1 | 200 | 0 | 0 | 50 | 0 | 0 | 15.62 |
| **Barracks 17c pikemanspa damage +2 (lvl 3)** `spabar.pikemanspa.1.2` | spa | damage | 2 | 1300 | 0 | 0 | 300 | 0 | 0 | 15.62 |
| **Barracks 17c pikemanspa damage +3 (lvl 4)** `spabar.pikemanspa.1.3` | spa | damage | 3 | 3600 | 0 | 0 | 450 | 0 | 0 | 15.62 |
| **Barracks 17c pikemanspa damage +2 (lvl 5)** `spabar.pikemanspa.1.4` | spa | damage | 2 | 7200 | 0 | 0 | 1850 | 0 | 0 | 15.62 |
| **Barracks 17c pikemanspa damage +1 (lvl 6)** `spabar.pikemanspa.1.5` | spa | damage | 1 | 16030 | 0 | 0 | 2000 | 0 | 0 | 15.62 |
| **Barracks 17c pikemanspa damage +1 (lvl 7)** `spabar.pikemanspa.1.6` | spa | damage | 1 | 15000 | 0 | 0 | 1875 | 0 | 0 | 15.62 |
| **Barracks 17c pikemanspa protection +1 (lvl 2)** `spabar.pikemanspa.2.1` | spa | protection | 1 | 150 | 0 | 0 | 50 | 0 | 0 | 15.62 |
| **Barracks 17c pikemanspa protection +1 (lvl 3)** `spabar.pikemanspa.2.2` | spa | protection | 1 | 900 | 0 | 0 | 175 | 0 | 0 | 15.62 |
| **Barracks 17c pikemanspa protection +2 (lvl 4)** `spabar.pikemanspa.2.3` | spa | protection | 2 | 4500 | 0 | 0 | 300 | 0 | 0 | 15.62 |
| **Barracks 17c pikemanspa protection +1 (lvl 5)** `spabar.pikemanspa.2.4` | spa | protection | 1 | 9005 | 0 | 0 | 507 | 0 | 0 | 15.62 |
| **Barracks 17c pikemanspa protection +1 (lvl 6)** `spabar.pikemanspa.2.5` | spa | protection | 1 | 18010 | 0 | 0 | 3050 | 0 | 0 | 15.62 |
| **Barracks 17c pikemanspa protection +2 (lvl 7)** `spabar.pikemanspa.2.6` | spa | protection | 2 | 16000 | 0 | 0 | 1000 | 0 | 0 | 15.62 |
| **Barracks 17c pikemanswi damage +2 (lvl 2)** `swibar.pikemanswi.1.1` | swi | damage | 2 | 200 | 0 | 0 | 50 | 0 | 0 | 15.62 |
| **Barracks 17c pikemanswi damage +3 (lvl 3)** `swibar.pikemanswi.1.2` | swi | damage | 3 | 1300 | 0 | 0 | 300 | 0 | 0 | 15.62 |
| **Barracks 17c pikemanswi damage +2 (lvl 4)** `swibar.pikemanswi.1.3` | swi | damage | 2 | 3600 | 0 | 0 | 450 | 0 | 0 | 15.62 |
| **Barracks 17c pikemanswi damage +1 (lvl 5)** `swibar.pikemanswi.1.4` | swi | damage | 1 | 7200 | 0 | 0 | 1850 | 0 | 0 | 15.62 |
| **Barracks 17c pikemanswi damage +1 (lvl 6)** `swibar.pikemanswi.1.5` | swi | damage | 1 | 16030 | 0 | 0 | 2000 | 0 | 0 | 15.62 |
| `swibar.pikemanswi.1.6` | swi | +damage | 1 | 15000 | 0 | 0 | 1875 | 0 | 0 | 15.62 |
| **Barracks 17c pikemanswi protection +2 (lvl 2)** `swibar.pikemanswi.2.1` | swi | protection | 2 | 150 | 0 | 0 | 50 | 0 | 0 | 15.62 |
| **Barracks 17c pikemanswi protection +2 (lvl 3)** `swibar.pikemanswi.2.2` | swi | protection | 2 | 900 | 0 | 0 | 175 | 0 | 0 | 15.62 |
| **Barracks 17c pikemanswi protection +1 (lvl 4)** `swibar.pikemanswi.2.3` | swi | protection | 1 | 4500 | 0 | 0 | 300 | 0 | 0 | 15.62 |
| **Barracks 17c pikemanswi protection +1 (lvl 5)** `swibar.pikemanswi.2.4` | swi | protection | 1 | 9005 | 0 | 0 | 507 | 0 | 0 | 15.62 |
| **Barracks 17c pikemanswi protection +1 (lvl 6)** `swibar.pikemanswi.2.5` | swi | protection | 1 | 18010 | 0 | 0 | 3050 | 0 | 0 | 15.62 |
| `swibar.pikemanswi.2.6` | swi | +protection | 1 | 11250 | 0 | 0 | 1500 | 0 | 0 | 15.62 |
| **Barracks 17c pikemantur damage +2 (lvl 2)** `turbar.pikemantur.1.1` | alg,tur | damage | 2 | 200 | 0 | 0 | 50 | 0 | 0 | 15.62 |
| **Barracks 17c pikemantur damage +2 (lvl 3)** `turbar.pikemantur.1.2` | alg,tur | damage | 2 | 600 | 0 | 0 | 300 | 0 | 0 | 15.62 |
| **Barracks 17c pikemantur damage +2 (lvl 4)** `turbar.pikemantur.1.3` | alg,tur | damage | 2 | 1200 | 0 | 0 | 450 | 0 | 0 | 15.62 |
| **Barracks 17c pikemantur damage +2 (lvl 5)** `turbar.pikemantur.1.4` | alg,tur | damage | 2 | 2200 | 0 | 0 | 1850 | 0 | 0 | 15.62 |
| **Barracks 17c pikemantur damage +2 (lvl 6)** `turbar.pikemantur.1.5` | alg,tur | damage | 2 | 16030 | 0 | 0 | 2000 | 0 | 0 | 15.62 |
| `turbar.pikemantur.1.6` | alg,tur | +damage | 2 | 18750 | 0 | 0 | 2350 | 0 | 0 | 15.62 |
| **Barracks 17c pikemantur protection +1 (lvl 2)** `turbar.pikemantur.2.1` | alg,tur | protection | 1 | 150 | 0 | 0 | 50 | 0 | 0 | 15.62 |
| **Barracks 17c pikemantur protection +2 (lvl 3)** `turbar.pikemantur.2.2` | alg,tur | protection | 2 | 900 | 0 | 0 | 175 | 0 | 0 | 15.62 |
| **Barracks 17c pikemantur protection +3 (lvl 4)** `turbar.pikemantur.2.3` | alg,tur | protection | 3 | 4500 | 0 | 0 | 300 | 0 | 0 | 15.62 |
| **Barracks 17c pikemantur protection +1 (lvl 5)** `turbar.pikemantur.2.4` | alg,tur | protection | 1 | 9005 | 0 | 0 | 507 | 0 | 0 | 15.62 |
| **Barracks 17c pikemantur protection +2 (lvl 6)** `turbar.pikemantur.2.5` | alg,tur | protection | 2 | 18010 | 0 | 0 | 3050 | 0 | 0 | 15.62 |
| `turbar.pikemantur.2.6` | alg,tur | +protection | 3 | 16875 | 0 | 0 | 2250 | 0 | 0 | 15.62 |
| **Barracks 17c roundshier damage +1 (lvl 2)** `ausbar.roundshier.1.1` | aus | damage | 1 | 150 | 0 | 0 | 50 | 0 | 0 | 15.62 |
| **Barracks 17c roundshier damage +1 (lvl 3)** `ausbar.roundshier.1.2` | aus | damage | 1 | 1500 | 0 | 0 | 200 | 0 | 0 | 15.62 |
| **Barracks 17c roundshier damage +2 (lvl 4)** `ausbar.roundshier.1.3` | aus | damage | 2 | 1300 | 0 | 0 | 325 | 0 | 0 | 15.62 |
| `ausbar.roundshier.1.4` | aus | +damage | 1 | 7500 | 0 | 0 | 900 | 0 | 0 | 15.62 |
| `ausbar.roundshier.1.5` | aus | +damage | 1 | 9000 | 0 | 0 | 1080 | 0 | 0 | 15.62 |
| `ausbar.roundshier.1.6` | aus | +damage | 2 | 18750 | 0 | 0 | 2250 | 0 | 0 | 15.62 |
| **Barracks 17c roundshier protection +1 (lvl 2)** `ausbar.roundshier.2.1` | aus | protection | 1 | 200 | 0 | 0 | 70 | 120 | 0 | 15.62 |
| **Barracks 17c roundshier protection +2 (lvl 3)** `ausbar.roundshier.2.2` | aus | protection | 2 | 4360 | 0 | 0 | 150 | 320 | 0 | 15.62 |
| **Barracks 17c roundshier protection +2 (lvl 4)** `ausbar.roundshier.2.3` | aus | protection | 2 | 506 | 0 | 0 | 250 | 420 | 0 | 15.62 |
| `ausbar.roundshier.2.4` | aus | +protection | 1 | 3750 | 0 | 0 | 450 | 0 | 0 | 15.62 |
| `ausbar.roundshier.2.5` | aus | +protection | 1 | 6750 | 0 | 0 | 810 | 0 | 0 | 15.62 |
| `ausbar.roundshier.2.6` | aus | +protection | 2 | 9375 | 0 | 0 | 1125 | 0 | 0 | 15.62 |
| **Barracks 17c serdiuk damage +2 (lvl 2)** `ukrbar.serdiuk.1.1` | ukr | damage | 2 | 5400 | 0 | 0 | 350 | 0 | 0 | 15.62 |
| **Barracks 17c serdiuk damage +2 (lvl 3)** `ukrbar.serdiuk.1.2` | ukr | damage | 2 | 22000 | 0 | 0 | 800 | 0 | 0 | 15.62 |
| **Barracks 17c serdiuk damage +2 (lvl 4)** `ukrbar.serdiuk.1.3` | ukr | damage | 2 | 32400 | 0 | 0 | 5800 | 0 | 0 | 15.62 |
| **Barracks 17c serdiuk damage +2 (lvl 5)** `ukrbar.serdiuk.1.4` | ukr | damage | 2 | 42010 | 0 | 0 | 6800 | 0 | 0 | 15.62 |
| **Barracks 17c serdiuk damage +2 (lvl 6)** `ukrbar.serdiuk.1.5` | ukr | damage | 2 | 52300 | 0 | 0 | 1800 | 7400 | 0 | 15.62 |
| `ukrbar.serdiuk.1.6` | ukr | +damage | 3 | 60000 | 0 | 0 | 8000 | 0 | 0 | 15.62 |
| **Barracks 17c serdiuk protection +1 (lvl 2)** `ukrbar.serdiuk.2.1` | ukr | protection | 1 | 200 | 0 | 0 | 40 | 0 | 0 | 15.62 |
| **Barracks 17c serdiuk protection +2 (lvl 3)** `ukrbar.serdiuk.2.2` | ukr | protection | 2 | 600 | 0 | 0 | 120 | 0 | 0 | 15.62 |
| **Barracks 17c serdiuk protection +2 (lvl 4)** `ukrbar.serdiuk.2.3` | ukr | protection | 2 | 1500 | 0 | 0 | 300 | 0 | 0 | 15.62 |
| **Barracks 17c serdiuk protection +1 (lvl 5)** `ukrbar.serdiuk.2.4` | ukr | protection | 1 | 3500 | 0 | 0 | 450 | 0 | 0 | 15.62 |
| **Barracks 17c serdiuk protection +2 (lvl 6)** `ukrbar.serdiuk.2.5` | ukr | protection | 2 | 8100 | 0 | 0 | 210 | 0 | 0 | 15.62 |
| `ukrbar.serdiuk.2.6` | ukr | +protection | 2 | 11250 | 0 | 0 | 1125 | 0 | 0 | 15.62 |
| **Barracks 17c strelet damage +1 (lvl 2)** `rusbar.strelet.1.1` | rus | damage | 1 | 2000 | 0 | 0 | 100 | 0 | 0 | 15.62 |
| **Barracks 17c strelet damage +1 (lvl 3)** `rusbar.strelet.1.2` | rus | damage | 1 | 1000 | 0 | 0 | 300 | 0 | 0 | 15.62 |
| **Barracks 17c strelet damage +2 (lvl 4)** `rusbar.strelet.1.3` | rus | damage | 2 | 500 | 0 | 0 | 700 | 0 | 0 | 15.62 |
| **Barracks 17c strelet protection +3 (lvl 2)** `rusbar.strelet.2.1` | rus | protection | 3 | 170 | 0 | 0 | 50 | 100 | 0 | 15.62 |
| **Barracks 17c strelet protection +3 (lvl 3)** `rusbar.strelet.2.2` | rus | protection | 3 | 405 | 0 | 0 | 150 | 200 | 0 | 15.62 |
| **Barracks 17c strelet protection +2 (lvl 4)** `rusbar.strelet.2.3` | rus | protection | 2 | 1570 | 0 | 0 | 100 | 350 | 0 | 15.62 |
| **Barracks 17c strelet protection +2 (lvl 5)** `rusbar.strelet.2.4` | rus | protection | 2 | 1556 | 0 | 0 | 550 | 100 | 0 | 15.62 |
| **Barracks 17c strelet protection +1 (lvl 6)** `rusbar.strelet.2.5` | rus | protection | 1 | 1060 | 0 | 0 | 850 | 400 | 0 | 15.62 |
| **Barracks 17c strelet protection +1 (lvl 7)** `rusbar.strelet.2.6` | rus | protection | 1 | 3700 | 0 | 0 | 650 | 700 | 0 | 15.62 |

## ba2 — Barracks 18c (per-unit upgrades)

Каждая запись — одна нация. Если значение одинаковое для всех 21 нации, показано одной строкой с `nation=all`. Если есть per-nation override (через `_country_ModifyUpgrade`), показаны отдельно.

| Апгрейд | nations | itype | val | F | W | S | G | I | C | time |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `engba2.1` | eng | +food eff % | 140 | 750 | 0 | 0 | 250 | 0 | 0 | 15.62 |
| `engba2.2` | eng | +food eff % | 180 | 25600 | 0 | 0 | 3350 | 2000 | 0 | 15.62 |
| **Barracks 18c archersco damage +2 (lvl 2)** `scoba2.archersco.1.1` | sco | damage | 2 | 3000 | 0 | 0 | 360 | 0 | 0 | 15.62 |
| **Barracks 18c archersco damage +3 (lvl 3)** `scoba2.archersco.1.2` | sco | damage | 3 | 7500 | 0 | 0 | 700 | 0 | 0 | 15.62 |
| **Barracks 18c archersco damage +4 (lvl 4)** `scoba2.archersco.1.3` | sco | damage | 4 | 9750 | 0 | 0 | 1200 | 0 | 0 | 15.62 |
| **Barracks 18c archersco damage +2 (lvl 5)** `scoba2.archersco.1.4` | sco | damage | 2 | 18000 | 0 | 0 | 1800 | 0 | 0 | 15.62 |
| **Barracks 18c archersco damage +4 (lvl 6)** `scoba2.archersco.1.5` | sco | damage | 4 | 33200 | 0 | 0 | 4320 | 0 | 0 | 15.62 |
| **Barracks 18c archersco damage +5 (lvl 7)** `scoba2.archersco.1.6` | sco | damage | 5 | 55000 | 0 | 0 | 7550 | 0 | 0 | 15.62 |
| **Barracks 18c archersco protection +1 (lvl 2)** `scoba2.archersco.2.1` | sco | protection | 1 | 900 | 0 | 0 | 250 | 0 | 0 | 15.62 |
| **Barracks 18c archersco protection +2 (lvl 3)** `scoba2.archersco.2.2` | sco | protection | 2 | 2200 | 0 | 0 | 450 | 0 | 0 | 15.62 |
| **Barracks 18c archersco protection +3 (lvl 4)** `scoba2.archersco.2.3` | sco | protection | 3 | 5400 | 0 | 0 | 800 | 0 | 0 | 15.62 |
| **Barracks 18c archersco protection +3 (lvl 5)** `scoba2.archersco.2.4` | sco | protection | 3 | 12500 | 0 | 0 | 1000 | 0 | 0 | 15.62 |
| **Barracks 18c archersco protection +2 (lvl 6)** `scoba2.archersco.2.5` | sco | protection | 2 | 20000 | 0 | 0 | 1200 | 0 | 0 | 15.62 |
| **Barracks 18c archersco protection +1 (lvl 7)** `scoba2.archersco.2.6` | sco | protection | 1 | 16500 | 0 | 0 | 1875 | 0 | 0 | 15.62 |
| **Barracks 18c bagpiper protection +10 (lvl 2)** `engba2.bagpiper.2.1` | eng | protection | 10 | 555 | 0 | 0 | 90 | 0 | 0 | 15.62 |
| **Barracks 18c chasseur damage +2 (lvl 2)** `fraba2.chasseur.1.1` | fra | damage | 2 | 3000 | 0 | 0 | 750 | 0 | 0 | 15.62 |
| **Barracks 18c chasseur damage +2 (lvl 3)** `fraba2.chasseur.1.2` | fra | damage | 2 | 4000 | 0 | 0 | 1100 | 0 | 0 | 15.62 |
| **Barracks 18c chasseur damage +2 (lvl 4)** `fraba2.chasseur.1.3` | fra | damage | 2 | 7000 | 0 | 0 | 1800 | 0 | 0 | 15.62 |
| **Barracks 18c chasseur damage +2 (lvl 5)** `fraba2.chasseur.1.4` | fra | damage | 2 | 12000 | 0 | 0 | 350 | 0 | 0 | 15.62 |
| **Barracks 18c chasseur damage +2 (lvl 6)** `fraba2.chasseur.1.5` | fra | damage | 2 | 32020 | 0 | 0 | 850 | 0 | 0 | 15.62 |
| **Barracks 18c chasseur damage +2 (lvl 7)** `fraba2.chasseur.1.6` | fra | damage | 2 | 45200 | 0 | 0 | 1330 | 0 | 0 | 15.62 |
| **Barracks 18c chasseur protection +1 (lvl 2)** `fraba2.chasseur.2.1` | fra | protection | 1 | 3706 | 0 | 0 | 350 | 0 | 0 | 15.62 |
| **Barracks 18c chasseur protection +1 (lvl 3)** `fraba2.chasseur.2.2` | fra | protection | 1 | 12060 | 0 | 0 | 1350 | 0 | 0 | 15.62 |
| **Barracks 18c chasseur protection +1 (lvl 4)** `fraba2.chasseur.2.3` | fra | protection | 1 | 36706 | 0 | 0 | 2150 | 0 | 0 | 15.62 |
| **Barracks 18c chasseur protection +1 (lvl 5)** `fraba2.chasseur.2.4` | fra | protection | 1 | 36706 | 0 | 0 | 3350 | 0 | 0 | 15.62 |
| **Barracks 18c chasseur protection +1 (lvl 6)** `fraba2.chasseur.2.5` | fra | protection | 1 | 37060 | 0 | 0 | 1350 | 0 | 0 | 15.62 |
| **Barracks 18c chasseur protection +1 (lvl 7)** `fraba2.chasseur.2.6` | fra | protection | 1 | 16706 | 0 | 0 | 1350 | 0 | 0 | 15.62 |
| **Barracks 18c drummer18 protection +15 (lvl 2)** `ausba2.drummer18.2.1` | aus,pie,rus,spa,swi,ven | protection | 15 | 706 | 0 | 0 | 50 | 0 | 0 | 15.62 |
| **Barracks 18c drummer18 protection +15 (lvl 2)** `pruba2.drummer18.2.1` | den,hun,pru,sax | protection | 15 | 900 | 0 | 0 | 45 | 0 | 0 | 15.62 |
| **Barracks 18c drummer18 protection +15 (lvl 2)** `sweba2.drummer18.2.1` | bav,por,swe | protection | 15 | 205 | 0 | 0 | 90 | 0 | 0 | 15.62 |
| **Barracks 18c drummer18 protection +15 (lvl 2)** `fraba2.drummer18.2.1` | fra | protection | 15 | 805 | 0 | 0 | 65 | 0 | 0 | 15.62 |
| **Barracks 18c drummer18 protection +15 (lvl 2)** `polba2.drummer18.2.1` | pol | protection | 15 | 205 | 0 | 0 | 150 | 0 | 0 | 15.62 |
| **Barracks 18c drummer18 protection +15 (lvl 2)** `netba2.drummer18.2.1` | net | protection | 15 | 450 | 0 | 0 | 75 | 0 | 0 | 15.62 |
| **Barracks 18c grenadier damage +2 (lvl 2)** `ausba2.grenadier.1.1` | aus,net,pie,por,rus,spa,swi,ven | damage | 2 | 2000 | 0 | 0 | 800 | 0 | 0 | 15.62 |
| **Barracks 18c grenadier damage +2 (lvl 2)** `fraba2.grenadier.1.1` | fra | damage | 2 | 1800 | 0 | 0 | 800 | 0 | 0 | 15.62 |
| **Barracks 18c grenadier damage +2 (lvl 2)** `engba2.grenadier.1.1` | eng | damage | 2 | 1000 | 0 | 0 | 1300 | 0 | 0 | 15.62 |
| **Barracks 18c grenadier damage +2 (lvl 2)** `polba2.grenadier.1.1` | pol | damage | 2 | 3000 | 0 | 0 | 800 | 0 | 0 | 15.62 |
| **Barracks 18c grenadier damage +2 (lvl 2)** `sweba2.grenadier.1.1` | swe | damage | 2 | 1000 | 0 | 0 | 800 | 0 | 0 | 15.62 |
| **Barracks 18c grenadier damage +3 (lvl 3)** `ausba2.grenadier.1.2` | aus,net,pie,por,rus,spa,swi,ven | damage | 3 | 12000 | 0 | 0 | 1800 | 0 | 0 | 15.62 |
| **Barracks 18c grenadier damage +3 (lvl 3)** `fraba2.grenadier.1.2` | fra | damage | 3 | 11200 | 0 | 0 | 1750 | 0 | 0 | 15.62 |
| **Barracks 18c grenadier damage +3 (lvl 3)** `engba2.grenadier.1.2` | eng | damage | 3 | 10000 | 0 | 0 | 1900 | 0 | 0 | 15.62 |
| **Barracks 18c grenadier damage +3 (lvl 3)** `polba2.grenadier.1.2` | pol | damage | 3 | 11000 | 0 | 0 | 1800 | 0 | 0 | 15.62 |
| **Barracks 18c grenadier damage +3 (lvl 3)** `sweba2.grenadier.1.2` | swe | damage | 3 | 13000 | 0 | 0 | 1800 | 0 | 0 | 15.62 |
| **Barracks 18c grenadier damage +4 (lvl 4)** `ausba2.grenadier.1.3` | aus,net,pie,por,rus,spa,swi,ven | damage | 4 | 32000 | 0 | 0 | 2800 | 0 | 0 | 15.62 |
| **Barracks 18c grenadier damage +4 (lvl 4)** `fraba2.grenadier.1.3` | fra | damage | 4 | 33000 | 0 | 0 | 2900 | 0 | 0 | 15.62 |
| **Barracks 18c grenadier damage +4 (lvl 4)** `engba2.grenadier.1.3` | eng | damage | 4 | 22000 | 0 | 0 | 2900 | 0 | 0 | 15.62 |
| **Barracks 18c grenadier damage +4 (lvl 4)** `polba2.grenadier.1.3` | pol | damage | 4 | 31000 | 0 | 0 | 2800 | 0 | 0 | 15.62 |
| **Barracks 18c grenadier damage +4 (lvl 4)** `sweba2.grenadier.1.3` | swe | damage | 4 | 25000 | 0 | 0 | 1800 | 0 | 0 | 15.62 |
| **Barracks 18c grenadier damage +5 (lvl 5)** `ausba2.grenadier.1.4` | aus,net,pie,por,rus,spa,swi,ven | damage | 5 | 42000 | 0 | 0 | 3800 | 0 | 0 | 15.62 |
| **Barracks 18c grenadier damage +5 (lvl 5)** `fraba2.grenadier.1.4` | fra | damage | 5 | 42000 | 0 | 0 | 4800 | 0 | 0 | 15.62 |
| **Barracks 18c grenadier damage +5 (lvl 5)** `engba2.grenadier.1.4` | eng | damage | 5 | 52000 | 0 | 0 | 3700 | 0 | 0 | 15.62 |
| **Barracks 18c grenadier damage +5 (lvl 5)** `polba2.grenadier.1.4` | pol | damage | 5 | 43000 | 0 | 0 | 3800 | 0 | 0 | 15.62 |
| **Barracks 18c grenadier damage +5 (lvl 5)** `sweba2.grenadier.1.4` | swe | damage | 5 | 49000 | 0 | 0 | 4800 | 0 | 0 | 15.62 |
| **Barracks 18c grenadier damage +6 (lvl 6)** `ausba2.grenadier.1.5` | aus,eng,net,pie,por,rus,spa,swi,ven | damage | 6 | 52000 | 0 | 0 | 4800 | 0 | 0 | 15.62 |
| **Barracks 18c grenadier damage +6 (lvl 6)** `fraba2.grenadier.1.5` | fra | damage | 6 | 52000 | 0 | 0 | 3800 | 0 | 0 | 15.62 |
| **Barracks 18c grenadier damage +6 (lvl 6)** `polba2.grenadier.1.5` | pol | damage | 6 | 62000 | 0 | 0 | 4800 | 0 | 0 | 15.62 |
| **Barracks 18c grenadier damage +6 (lvl 6)** `sweba2.grenadier.1.5` | swe | damage | 6 | 54000 | 0 | 0 | 5800 | 0 | 0 | 15.62 |
| **Barracks 18c grenadier damage +1500 (lvl 7)** `ausba2.grenadier.1.6` | aus,net,pie,por,rus,spa,swi,ven | damage | 1500 | 62000 | 0 | 0 | 15800 | 0 | 0 | 15.62 |
| **Barracks 18c grenadier damage +1500 (lvl 7)** `fraba2.grenadier.1.6` | fra | damage | 1500 | 64010 | 0 | 0 | 15200 | 0 | 0 | 15.62 |
| **Barracks 18c grenadier damage +1500 (lvl 7)** `engba2.grenadier.1.6` | eng | damage | 1500 | 60000 | 0 | 0 | 16000 | 0 | 0 | 15.62 |
| **Barracks 18c grenadier damage +1500 (lvl 7)** `polba2.grenadier.1.6` | pol | damage | 1500 | 52000 | 0 | 0 | 15800 | 0 | 0 | 15.62 |
| **Barracks 18c grenadier damage +1500 (lvl 7)** `sweba2.grenadier.1.6` | swe | damage | 1500 | 60000 | 0 | 0 | 14590 | 0 | 0 | 15.62 |
| **Barracks 18c grenadier protection +1 (lvl 2)** `ausba2.grenadier.2.1` | aus,net,pie,por,rus,spa,swi,ven | protection | 1 | 3706 | 0 | 0 | 350 | 0 | 0 | 15.62 |
| **Barracks 18c grenadier protection +1 (lvl 2)** `fraba2.grenadier.2.1` | fra | protection | 1 | 3506 | 0 | 0 | 220 | 0 | 0 | 15.62 |
| **Barracks 18c grenadier protection +1 (lvl 2)** `engba2.grenadier.2.1` | eng | protection | 1 | 3250 | 0 | 0 | 450 | 0 | 0 | 15.62 |
| **Barracks 18c grenadier protection +1 (lvl 2)** `polba2.grenadier.2.1` | pol | protection | 1 | 4506 | 0 | 0 | 750 | 0 | 0 | 15.62 |
| **Barracks 18c grenadier protection +1 (lvl 2)** `sweba2.grenadier.2.1` | swe | protection | 1 | 7705 | 0 | 0 | 350 | 0 | 0 | 15.62 |
| **Barracks 18c grenadier protection +2 (lvl 3)** `ausba2.grenadier.2.2` | aus,eng,net,pie,por,rus,spa,swi,ven | protection | 2 | 11030 | 0 | 0 | 1350 | 0 | 0 | 15.62 |
| **Barracks 18c grenadier protection +2 (lvl 3)** `fraba2.grenadier.2.2` | fra | protection | 2 | 11250 | 0 | 0 | 1450 | 0 | 0 | 15.62 |
| **Barracks 18c grenadier protection +2 (lvl 3)** `polba2.grenadier.2.2` | pol | protection | 2 | 10130 | 0 | 0 | 950 | 0 | 0 | 15.62 |
| **Barracks 18c grenadier protection +2 (lvl 3)** `sweba2.grenadier.2.2` | swe | protection | 2 | 7030 | 0 | 0 | 1350 | 0 | 0 | 15.62 |
| **Barracks 18c grenadier protection +3 (lvl 4)** `ausba2.grenadier.2.3` | aus,net,pie,por,rus,spa,swi,ven | protection | 3 | 35706 | 0 | 0 | 3000 | 0 | 0 | 15.62 |
| **Barracks 18c grenadier protection +3 (lvl 4)** `fraba2.grenadier.2.3` | fra | protection | 3 | 37200 | 0 | 0 | 3300 | 0 | 0 | 15.62 |
| **Barracks 18c grenadier protection +3 (lvl 4)** `engba2.grenadier.2.3` | eng | protection | 3 | 36200 | 0 | 0 | 2500 | 0 | 0 | 15.62 |
| **Barracks 18c grenadier protection +3 (lvl 4)** `polba2.grenadier.2.3` | pol | protection | 3 | 25706 | 0 | 0 | 500 | 0 | 0 | 15.62 |
| **Barracks 18c grenadier protection +3 (lvl 4)** `sweba2.grenadier.2.3` | swe | protection | 3 | 21706 | 0 | 0 | 1000 | 0 | 0 | 15.62 |
| **Barracks 18c grenadier protection +1 (lvl 5)** `ausba2.grenadier.2.4` | aus,net,pie,por,rus,spa,swi,ven | protection | 1 | 36556 | 0 | 0 | 3350 | 0 | 0 | 15.62 |
| **Barracks 18c grenadier protection +1 (lvl 5)** `fraba2.grenadier.2.4` | fra | protection | 1 | 40400 | 0 | 0 | 3050 | 0 | 0 | 15.62 |
| **Barracks 18c grenadier protection +1 (lvl 5)** `engba2.grenadier.2.4` | eng | protection | 1 | 16600 | 0 | 0 | 3650 | 0 | 0 | 15.62 |
| **Barracks 18c grenadier protection +1 (lvl 5)** `polba2.grenadier.2.4` | pol | protection | 1 | 46556 | 0 | 0 | 1350 | 0 | 0 | 15.62 |
| **Barracks 18c grenadier protection +1 (lvl 5)** `sweba2.grenadier.2.4` | swe | protection | 1 | 22556 | 0 | 0 | 5350 | 0 | 0 | 15.62 |
| **Barracks 18c grenadier protection +2 (lvl 6)** `ausba2.grenadier.2.5` | aus,net,pie,por,rus,spa,swi,ven | protection | 2 | 30060 | 0 | 0 | 1350 | 0 | 0 | 15.62 |
| **Barracks 18c grenadier protection +2 (lvl 6)** `fraba2.grenadier.2.5` | fra | protection | 2 | 22060 | 0 | 0 | 350 | 0 | 0 | 15.62 |
| **Barracks 18c grenadier protection +2 (lvl 6)** `engba2.grenadier.2.5` | eng | protection | 2 | 60060 | 0 | 0 | 1050 | 0 | 0 | 15.62 |
| **Barracks 18c grenadier protection +2 (lvl 6)** `polba2.grenadier.2.5` | pol | protection | 2 | 50060 | 0 | 0 | 6050 | 0 | 0 | 15.62 |
| **Barracks 18c grenadier protection +2 (lvl 6)** `sweba2.grenadier.2.5` | swe | protection | 2 | 30060 | 0 | 0 | 1750 | 0 | 0 | 15.62 |
| **Barracks 18c grenadier protection +3 (lvl 7)** `ausba2.grenadier.2.6` | aus,net,pie,por,rus,spa,swi,ven | protection | 3 | 64000 | 0 | 0 | 1350 | 0 | 0 | 15.62 |
| **Barracks 18c grenadier protection +3 (lvl 7)** `fraba2.grenadier.2.6` | fra | protection | 3 | 63900 | 0 | 0 | 2350 | 0 | 0 | 15.62 |
| **Barracks 18c grenadier protection +3 (lvl 7)** `engba2.grenadier.2.6` | eng | protection | 3 | 64000 | 0 | 0 | 1650 | 0 | 0 | 15.62 |
| **Barracks 18c grenadier protection +3 (lvl 7)** `polba2.grenadier.2.6` | pol | protection | 3 | 44000 | 0 | 0 | 1650 | 0 | 0 | 15.62 |
| **Barracks 18c grenadier protection +3 (lvl 7)** `sweba2.grenadier.2.6` | swe | protection | 3 | 62000 | 0 | 0 | 950 | 0 | 0 | 15.62 |
| **Barracks 18c grenadierbav damage +2 (lvl 2)** `bavba2.grenadierbav.1.1` | bav | damage | 2 | 1000 | 0 | 0 | 800 | 0 | 0 | 15.62 |
| **Barracks 18c grenadierbav damage +3 (lvl 3)** `bavba2.grenadierbav.1.2` | bav | damage | 3 | 13000 | 0 | 0 | 2800 | 0 | 0 | 15.62 |
| **Barracks 18c grenadierbav damage +4 (lvl 4)** `bavba2.grenadierbav.1.3` | bav | damage | 4 | 32000 | 0 | 0 | 1800 | 0 | 0 | 15.62 |
| **Barracks 18c grenadierbav damage +5 (lvl 5)** `bavba2.grenadierbav.1.4` | bav | damage | 5 | 52000 | 0 | 0 | 4800 | 0 | 0 | 15.62 |
| **Barracks 18c grenadierbav damage +6 (lvl 6)** `bavba2.grenadierbav.1.5` | bav | damage | 6 | 42000 | 0 | 0 | 3800 | 0 | 0 | 15.62 |
| **Barracks 18c grenadierbav damage +1500 (lvl 7)** `bavba2.grenadierbav.1.6` | bav | damage | 1500 | 64000 | 0 | 0 | 14800 | 0 | 0 | 15.62 |
| **Barracks 18c grenadierbav protection +1 (lvl 2)** `bavba2.grenadierbav.2.1` | bav | protection | 1 | 3205 | 0 | 0 | 375 | 0 | 0 | 15.62 |
| **Barracks 18c grenadierbav protection +2 (lvl 3)** `bavba2.grenadierbav.2.2` | bav | protection | 2 | 11030 | 0 | 0 | 4350 | 0 | 0 | 15.62 |
| **Barracks 18c grenadierbav protection +3 (lvl 4)** `bavba2.grenadierbav.2.3` | bav | protection | 3 | 36206 | 0 | 0 | 500 | 0 | 0 | 15.62 |
| **Barracks 18c grenadierbav protection +1 (lvl 5)** `bavba2.grenadierbav.2.4` | bav | protection | 1 | 34950 | 0 | 0 | 1350 | 0 | 0 | 15.62 |
| **Barracks 18c grenadierbav protection +2 (lvl 6)** `bavba2.grenadierbav.2.5` | bav | protection | 2 | 30060 | 0 | 0 | 2150 | 0 | 0 | 15.62 |
| **Barracks 18c grenadierbav protection +3 (lvl 7)** `bavba2.grenadierbav.2.6` | bav | protection | 3 | 64000 | 0 | 0 | 2550 | 0 | 0 | 15.62 |
| **Barracks 18c grenadierden damage +3 (lvl 2)** `denba2.grenadierden.1.1` | den | damage | 3 | 1000 | 0 | 0 | 800 | 0 | 0 | 15.62 |
| **Barracks 18c grenadierden damage +4 (lvl 3)** `denba2.grenadierden.1.2` | den | damage | 4 | 13000 | 0 | 0 | 2800 | 0 | 0 | 15.62 |
| **Barracks 18c grenadierden damage +4 (lvl 4)** `denba2.grenadierden.1.3` | den | damage | 4 | 32000 | 0 | 0 | 1800 | 0 | 0 | 15.62 |
| **Barracks 18c grenadierden damage +4 (lvl 5)** `denba2.grenadierden.1.4` | den | damage | 4 | 52000 | 0 | 0 | 4800 | 0 | 0 | 15.62 |
| **Barracks 18c grenadierden damage +5 (lvl 6)** `denba2.grenadierden.1.5` | den | damage | 5 | 42000 | 0 | 0 | 3800 | 0 | 0 | 15.62 |
| **Barracks 18c grenadierden damage +1500 (lvl 7)** `denba2.grenadierden.1.6` | den | damage | 1500 | 64000 | 0 | 0 | 14800 | 0 | 0 | 15.62 |
| **Barracks 18c grenadierden protection +2 (lvl 2)** `denba2.grenadierden.2.1` | den | protection | 2 | 3205 | 0 | 0 | 375 | 0 | 0 | 15.62 |
| **Barracks 18c grenadierden protection +3 (lvl 3)** `denba2.grenadierden.2.2` | den | protection | 3 | 11030 | 0 | 0 | 4350 | 0 | 0 | 15.62 |
| **Barracks 18c grenadierden protection +3 (lvl 4)** `denba2.grenadierden.2.3` | den | protection | 3 | 36206 | 0 | 0 | 500 | 0 | 0 | 15.62 |
| **Barracks 18c grenadierden protection +2 (lvl 5)** `denba2.grenadierden.2.4` | den | protection | 2 | 34950 | 0 | 0 | 1350 | 0 | 0 | 15.62 |
| **Barracks 18c grenadierden protection +1 (lvl 6)** `denba2.grenadierden.2.5` | den | protection | 1 | 30060 | 0 | 0 | 2150 | 0 | 0 | 15.62 |
| **Barracks 18c grenadierden protection +1 (lvl 7)** `denba2.grenadierden.2.6` | den | protection | 1 | 64000 | 0 | 0 | 2550 | 0 | 0 | 15.62 |
| **Barracks 18c grenadierhun damage +6 (lvl 2)** `hunba2.grenadierhun.1.1` | hun | damage | 6 | 1000 | 0 | 0 | 800 | 0 | 0 | 15.62 |
| **Barracks 18c grenadierhun damage +5 (lvl 3)** `hunba2.grenadierhun.1.2` | hun | damage | 5 | 13000 | 0 | 0 | 1800 | 0 | 0 | 15.62 |
| **Barracks 18c grenadierhun damage +4 (lvl 4)** `hunba2.grenadierhun.1.3` | hun | damage | 4 | 25000 | 0 | 0 | 1800 | 0 | 0 | 15.62 |
| **Barracks 18c grenadierhun damage +3 (lvl 5)** `hunba2.grenadierhun.1.4` | hun | damage | 3 | 49000 | 0 | 0 | 4800 | 0 | 0 | 15.62 |
| **Barracks 18c grenadierhun damage +2 (lvl 6)** `hunba2.grenadierhun.1.5` | hun | damage | 2 | 54000 | 0 | 0 | 5800 | 0 | 0 | 15.62 |
| **Barracks 18c grenadierhun damage +1500 (lvl 7)** `hunba2.grenadierhun.1.6` | hun | damage | 1500 | 60000 | 0 | 0 | 14590 | 0 | 0 | 15.62 |
| **Barracks 18c grenadierhun protection +2 (lvl 2)** `hunba2.grenadierhun.2.1` | hun | protection | 2 | 7705 | 0 | 0 | 350 | 0 | 0 | 15.62 |
| **Barracks 18c grenadierhun protection +2 (lvl 3)** `hunba2.grenadierhun.2.2` | hun | protection | 2 | 7030 | 0 | 0 | 1350 | 0 | 0 | 15.62 |
| **Barracks 18c grenadierhun protection +2 (lvl 4)** `hunba2.grenadierhun.2.3` | hun | protection | 2 | 21706 | 0 | 0 | 1000 | 0 | 0 | 15.62 |
| **Barracks 18c grenadierhun protection +2 (lvl 5)** `hunba2.grenadierhun.2.4` | hun | protection | 2 | 22556 | 0 | 0 | 5350 | 0 | 0 | 15.62 |
| **Barracks 18c grenadierhun protection +2 (lvl 6)** `hunba2.grenadierhun.2.5` | hun | protection | 2 | 30060 | 0 | 0 | 1750 | 0 | 0 | 15.62 |
| **Barracks 18c grenadierhun protection +2 (lvl 7)** `hunba2.grenadierhun.2.6` | hun | protection | 2 | 62000 | 0 | 0 | 950 | 0 | 0 | 15.62 |
| **Barracks 18c grenadierpru damage +2 (lvl 2)** `pruba2.grenadierpru.1.1` | pru | damage | 2 | 1000 | 0 | 0 | 800 | 0 | 0 | 15.62 |
| **Barracks 18c grenadierpru damage +3 (lvl 3)** `pruba2.grenadierpru.1.2` | pru | damage | 3 | 13000 | 0 | 0 | 2800 | 0 | 0 | 15.62 |
| **Barracks 18c grenadierpru damage +4 (lvl 4)** `pruba2.grenadierpru.1.3` | pru | damage | 4 | 32000 | 0 | 0 | 1800 | 0 | 0 | 15.62 |
| **Barracks 18c grenadierpru damage +5 (lvl 5)** `pruba2.grenadierpru.1.4` | pru | damage | 5 | 52000 | 0 | 0 | 4800 | 0 | 0 | 15.62 |
| **Barracks 18c grenadierpru damage +6 (lvl 6)** `pruba2.grenadierpru.1.5` | pru | damage | 6 | 42000 | 0 | 0 | 3800 | 0 | 0 | 15.62 |
| **Barracks 18c grenadierpru damage +1500 (lvl 7)** `pruba2.grenadierpru.1.6` | pru | damage | 1500 | 64000 | 0 | 0 | 14800 | 0 | 0 | 15.62 |
| **Barracks 18c grenadierpru protection +1 (lvl 2)** `pruba2.grenadierpru.2.1` | pru | protection | 1 | 3205 | 0 | 0 | 375 | 0 | 0 | 15.62 |
| **Barracks 18c grenadierpru protection +2 (lvl 3)** `pruba2.grenadierpru.2.2` | pru | protection | 2 | 11030 | 0 | 0 | 4350 | 0 | 0 | 15.62 |
| **Barracks 18c grenadierpru protection +3 (lvl 4)** `pruba2.grenadierpru.2.3` | pru | protection | 3 | 36206 | 0 | 0 | 500 | 0 | 0 | 15.62 |
| **Barracks 18c grenadierpru protection +1 (lvl 5)** `pruba2.grenadierpru.2.4` | pru | protection | 1 | 34950 | 0 | 0 | 1350 | 0 | 0 | 15.62 |
| **Barracks 18c grenadierpru protection +2 (lvl 6)** `pruba2.grenadierpru.2.5` | pru | protection | 2 | 30060 | 0 | 0 | 2150 | 0 | 0 | 15.62 |
| **Barracks 18c grenadierpru protection +3 (lvl 7)** `pruba2.grenadierpru.2.6` | pru | protection | 3 | 64000 | 0 | 0 | 2550 | 0 | 0 | 15.62 |
| **Barracks 18c grenadiersax damage +2 (lvl 2)** `saxba2.grenadiersax.1.1` | sax | damage | 2 | 1000 | 0 | 0 | 800 | 0 | 0 | 15.62 |
| **Barracks 18c grenadiersax damage +3 (lvl 3)** `saxba2.grenadiersax.1.2` | sax | damage | 3 | 13000 | 0 | 0 | 1800 | 0 | 0 | 15.62 |
| **Barracks 18c grenadiersax damage +4 (lvl 4)** `saxba2.grenadiersax.1.3` | sax | damage | 4 | 25000 | 0 | 0 | 1800 | 0 | 0 | 15.62 |
| **Barracks 18c grenadiersax damage +5 (lvl 5)** `saxba2.grenadiersax.1.4` | sax | damage | 5 | 49000 | 0 | 0 | 4800 | 0 | 0 | 15.62 |
| **Barracks 18c grenadiersax damage +6 (lvl 6)** `saxba2.grenadiersax.1.5` | sax | damage | 6 | 54000 | 0 | 0 | 5800 | 0 | 0 | 15.62 |
| **Barracks 18c grenadiersax damage +1500 (lvl 7)** `saxba2.grenadiersax.1.6` | sax | damage | 1500 | 60000 | 0 | 0 | 14590 | 0 | 0 | 15.62 |
| **Barracks 18c grenadiersax protection +2 (lvl 2)** `saxba2.grenadiersax.2.1` | sax | protection | 2 | 7705 | 0 | 0 | 350 | 0 | 0 | 15.62 |
| **Barracks 18c grenadiersax protection +2 (lvl 3)** `saxba2.grenadiersax.2.2` | sax | protection | 2 | 7030 | 0 | 0 | 1350 | 0 | 0 | 15.62 |
| **Barracks 18c grenadiersax protection +2 (lvl 4)** `saxba2.grenadiersax.2.3` | sax | protection | 2 | 21706 | 0 | 0 | 1000 | 0 | 0 | 15.62 |
| **Barracks 18c grenadiersax protection +2 (lvl 5)** `saxba2.grenadiersax.2.4` | sax | protection | 2 | 22556 | 0 | 0 | 5350 | 0 | 0 | 15.62 |
| **Barracks 18c grenadiersax protection +2 (lvl 6)** `saxba2.grenadiersax.2.5` | sax | protection | 2 | 30060 | 0 | 0 | 1750 | 0 | 0 | 15.62 |
| **Barracks 18c grenadiersax protection +2 (lvl 7)** `saxba2.grenadiersax.2.6` | sax | protection | 2 | 62000 | 0 | 0 | 950 | 0 | 0 | 15.62 |
| **Barracks 18c highlander damage +1 (lvl 2)** `engba2.highlander.1.1` | eng | damage | 1 | 4000 | 0 | 0 | 750 | 0 | 0 | 15.62 |
| **Barracks 18c highlander damage +2 (lvl 3)** `engba2.highlander.1.2` | eng | damage | 2 | 3000 | 0 | 0 | 1100 | 0 | 0 | 15.62 |
| **Barracks 18c highlander damage +3 (lvl 4)** `engba2.highlander.1.3` | eng | damage | 3 | 7500 | 0 | 0 | 1700 | 0 | 0 | 15.62 |
| **Barracks 18c highlander damage +1 (lvl 5)** `engba2.highlander.1.4` | eng | damage | 1 | 11000 | 0 | 0 | 400 | 0 | 0 | 15.62 |
| **Barracks 18c highlander damage +1 (lvl 6)** `engba2.highlander.1.5` | eng | damage | 1 | 27020 | 0 | 0 | 1150 | 0 | 0 | 15.62 |
| **Barracks 18c highlander damage +1 (lvl 7)** `engba2.highlander.1.6` | eng | damage | 1 | 40200 | 0 | 0 | 1220 | 0 | 0 | 15.62 |
| **Barracks 18c highlander protection +2 (lvl 2)** `engba2.highlander.2.1` | eng | protection | 2 | 3006 | 0 | 0 | 400 | 0 | 0 | 15.62 |
| **Barracks 18c highlander protection +2 (lvl 3)** `engba2.highlander.2.2` | eng | protection | 2 | 10020 | 0 | 0 | 1550 | 0 | 0 | 15.62 |
| **Barracks 18c highlander protection +2 (lvl 4)** `engba2.highlander.2.3` | eng | protection | 2 | 35706 | 0 | 0 | 1850 | 0 | 0 | 15.62 |
| `engba2.highlander.2.4` | eng | +protection | 3 | 3600 | 0 | 0 | 600 | 0 | 0 | 15.62 |
| `engba2.highlander.2.5` | eng | +protection | 3 | 5400 | 0 | 0 | 900 | 0 | 0 | 15.62 |
| `engba2.highlander.2.6` | eng | +protection | 3 | 11250 | 0 | 0 | 1875 | 0 | 0 | 15.62 |
| **Barracks 18c jagerpor damage +1 (lvl 2)** `porba2.jagerpor.1.1` | por | damage | 1 | 3000 | 0 | 0 | 750 | 0 | 0 | 15.62 |
| **Barracks 18c jagerpor damage +1 (lvl 3)** `porba2.jagerpor.1.2` | por | damage | 1 | 4000 | 0 | 0 | 1100 | 0 | 0 | 15.62 |
| **Barracks 18c jagerpor damage +1 (lvl 4)** `porba2.jagerpor.1.3` | por | damage | 1 | 7000 | 0 | 0 | 1800 | 0 | 0 | 15.62 |
| **Barracks 18c jagerpor damage +1 (lvl 5)** `porba2.jagerpor.1.4` | por | damage | 1 | 12000 | 0 | 0 | 350 | 0 | 0 | 15.62 |
| **Barracks 18c jagerpor damage +1 (lvl 6)** `porba2.jagerpor.1.5` | por | damage | 1 | 32020 | 0 | 0 | 850 | 0 | 0 | 15.62 |
| **Barracks 18c jagerpor damage +1 (lvl 7)** `porba2.jagerpor.1.6` | por | damage | 1 | 45200 | 0 | 0 | 1330 | 0 | 0 | 15.62 |
| **Barracks 18c jagerpor protection +1 (lvl 2)** `porba2.jagerpor.2.1` | por | protection | 1 | 3706 | 0 | 0 | 350 | 0 | 0 | 15.62 |
| **Barracks 18c jagerpor protection +1 (lvl 3)** `porba2.jagerpor.2.2` | por | protection | 1 | 12060 | 0 | 0 | 1350 | 0 | 0 | 15.62 |
| **Barracks 18c jagerpor protection +1 (lvl 4)** `porba2.jagerpor.2.3` | por | protection | 1 | 36706 | 0 | 0 | 2250 | 0 | 0 | 15.62 |
| **Barracks 18c jagerpor protection +1 (lvl 5)** `porba2.jagerpor.2.4` | por | protection | 1 | 36706 | 0 | 0 | 3350 | 0 | 0 | 15.62 |
| **Barracks 18c jagerpor protection +1 (lvl 6)** `porba2.jagerpor.2.5` | por | protection | 1 | 37060 | 0 | 0 | 1350 | 0 | 0 | 15.62 |
| **Barracks 18c jagerpor protection +1 (lvl 7)** `porba2.jagerpor.2.6` | por | protection | 1 | 16706 | 0 | 0 | 1350 | 0 | 0 | 15.62 |
| **Barracks 18c jagerswi damage +3 (lvl 2)** `swiba2.jagerswi.1.1` | swi | damage | 3 | 3000 | 0 | 0 | 750 | 0 | 0 | 15.62 |
| **Barracks 18c jagerswi damage +2 (lvl 3)** `swiba2.jagerswi.1.2` | swi | damage | 2 | 4000 | 0 | 0 | 1100 | 0 | 0 | 15.62 |
| **Barracks 18c jagerswi damage +1 (lvl 4)** `swiba2.jagerswi.1.3` | swi | damage | 1 | 7000 | 0 | 0 | 1800 | 0 | 0 | 15.62 |
| **Barracks 18c jagerswi damage +3 (lvl 5)** `swiba2.jagerswi.1.4` | swi | damage | 3 | 12000 | 0 | 0 | 350 | 0 | 0 | 15.62 |
| **Barracks 18c jagerswi damage +2 (lvl 6)** `swiba2.jagerswi.1.5` | swi | damage | 2 | 32020 | 0 | 0 | 850 | 0 | 0 | 15.62 |
| **Barracks 18c jagerswi damage +1 (lvl 7)** `swiba2.jagerswi.1.6` | swi | damage | 1 | 45200 | 0 | 0 | 1330 | 0 | 0 | 15.62 |
| **Barracks 18c jagerswi protection +1 (lvl 2)** `swiba2.jagerswi.2.1` | swi | protection | 1 | 3706 | 0 | 0 | 350 | 0 | 0 | 15.62 |
| **Barracks 18c jagerswi protection +1 (lvl 3)** `swiba2.jagerswi.2.2` | swi | protection | 1 | 12060 | 0 | 0 | 1350 | 0 | 0 | 15.62 |
| **Barracks 18c jagerswi protection +1 (lvl 4)** `swiba2.jagerswi.2.3` | swi | protection | 1 | 36706 | 0 | 0 | 2250 | 0 | 0 | 15.62 |
| **Barracks 18c jagerswi protection +1 (lvl 5)** `swiba2.jagerswi.2.4` | swi | protection | 1 | 36706 | 0 | 0 | 3350 | 0 | 0 | 15.62 |
| **Barracks 18c jagerswi protection +1 (lvl 6)** `swiba2.jagerswi.2.5` | swi | protection | 1 | 37060 | 0 | 0 | 1350 | 0 | 0 | 15.62 |
| **Barracks 18c jagerswi protection +1 (lvl 7)** `swiba2.jagerswi.2.6` | swi | protection | 1 | 16706 | 0 | 0 | 1350 | 0 | 0 | 15.62 |
| **Barracks 18c musketeer18 damage +1 (lvl 2)** `ausba2.musketeer18.1.1` | aus,hun,pie,por,rus,spa,swi,ven | damage | 1 | 1000 | 0 | 0 | 800 | 0 | 0 | 15.62 |
| **Barracks 18c musketeer18 damage +1 (lvl 2)** `fraba2.musketeer18.1.1` | fra | damage | 1 | 500 | 0 | 0 | 200 | 0 | 0 | 15.62 |
| **Barracks 18c musketeer18 damage +1 (lvl 2)** `engba2.musketeer18.1.1` | eng | damage | 1 | 1100 | 0 | 0 | 750 | 0 | 0 | 15.62 |
| **Barracks 18c musketeer18 damage +1 (lvl 2)** `polba2.musketeer18.1.1` | pol | damage | 1 | 1000 | 0 | 0 | 100 | 0 | 0 | 15.62 |
| **Barracks 18c musketeer18 damage +1 (lvl 2)** `sweba2.musketeer18.1.1` | swe | damage | 1 | 9000 | 0 | 0 | 200 | 0 | 0 | 15.62 |
| **Barracks 18c musketeer18 damage +1 (lvl 2)** `netba2.musketeer18.1.1` | net | damage | 1 | 900 | 0 | 0 | 100 | 0 | 0 | 15.62 |
| **Barracks 18c musketeer18 damage +1 (lvl 3)** `ausba2.musketeer18.1.2` | aus,hun,pie,por,rus,spa,swi,ven | damage | 1 | 1500 | 0 | 0 | 800 | 0 | 0 | 15.62 |
| **Barracks 18c musketeer18 damage +1 (lvl 3)** `fraba2.musketeer18.1.2` | fra | damage | 1 | 2000 | 0 | 0 | 400 | 0 | 0 | 15.62 |
| **Barracks 18c musketeer18 damage +1 (lvl 3)** `engba2.musketeer18.1.2` | eng | damage | 1 | 1670 | 0 | 0 | 850 | 0 | 0 | 15.62 |
| **Barracks 18c musketeer18 damage +1 (lvl 3)** `polba2.musketeer18.1.2` | pol | damage | 1 | 2500 | 0 | 0 | 200 | 0 | 0 | 15.62 |
| **Barracks 18c musketeer18 damage +1 (lvl 3)** `sweba2.musketeer18.1.2` | swe | damage | 1 | 600 | 0 | 0 | 200 | 0 | 0 | 15.62 |
| **Barracks 18c musketeer18 damage +1 (lvl 3)** `netba2.musketeer18.1.2` | net | damage | 1 | 1600 | 0 | 0 | 200 | 0 | 0 | 15.62 |
| **Barracks 18c musketeer18 damage +2 (lvl 4)** `ausba2.musketeer18.1.3` | aus,hun,pie,por,rus,spa,swi,ven | damage | 2 | 2000 | 0 | 0 | 800 | 0 | 0 | 15.62 |
| **Barracks 18c musketeer18 damage +2 (lvl 4)** `fraba2.musketeer18.1.3` | fra | damage | 2 | 1200 | 0 | 0 | 1800 | 0 | 0 | 15.62 |
| **Barracks 18c musketeer18 damage +2 (lvl 4)** `engba2.musketeer18.1.3` | eng | damage | 2 | 1900 | 0 | 0 | 200 | 0 | 0 | 15.62 |
| **Barracks 18c musketeer18 damage +2 (lvl 4)** `polba2.musketeer18.1.3` | pol | damage | 2 | 1000 | 0 | 0 | 300 | 0 | 0 | 15.62 |
| **Barracks 18c musketeer18 damage +2 (lvl 4)** `sweba2.musketeer18.1.3` | swe | damage | 2 | 4000 | 0 | 0 | 100 | 0 | 0 | 15.62 |
| **Barracks 18c musketeer18 damage +2 (lvl 4)** `netba2.musketeer18.1.3` | net | damage | 2 | 1500 | 0 | 0 | 300 | 0 | 0 | 15.62 |
| **Barracks 18c musketeer18 damage +2 (lvl 5)** `ausba2.musketeer18.1.4` | aus,hun,pie,por,rus,spa,swi,ven | damage | 2 | 2500 | 0 | 0 | 800 | 0 | 0 | 15.62 |
| **Barracks 18c musketeer18 damage +2 (lvl 5)** `fraba2.musketeer18.1.4` | fra | damage | 2 | 3300 | 0 | 0 | 100 | 0 | 0 | 15.62 |
| **Barracks 18c musketeer18 damage +2 (lvl 5)** `engba2.musketeer18.1.4` | eng | damage | 2 | 2340 | 0 | 0 | 1800 | 0 | 0 | 15.62 |
| **Barracks 18c musketeer18 damage +2 (lvl 5)** `polba2.musketeer18.1.4` | pol | damage | 2 | 3500 | 0 | 0 | 400 | 0 | 0 | 15.62 |
| **Barracks 18c musketeer18 damage +2 (lvl 5)** `sweba2.musketeer18.1.4` | swe | damage | 2 | 500 | 0 | 0 | 2100 | 0 | 0 | 15.62 |
| **Barracks 18c musketeer18 damage +2 (lvl 5)** `netba2.musketeer18.1.4` | net | damage | 2 | 3100 | 0 | 0 | 2600 | 0 | 0 | 15.62 |
| **Barracks 18c musketeer18 damage +3 (lvl 6)** `ausba2.musketeer18.1.5` | aus,hun,pie,por,rus,spa,swi,ven | damage | 3 | 3000 | 0 | 0 | 800 | 0 | 0 | 15.62 |
| **Barracks 18c musketeer18 damage +3 (lvl 6)** `fraba2.musketeer18.1.5` | fra | damage | 3 | 1100 | 0 | 0 | 200 | 0 | 0 | 15.62 |
| **Barracks 18c musketeer18 damage +3 (lvl 6)** `engba2.musketeer18.1.5` | eng | damage | 3 | 3000 | 0 | 0 | 900 | 0 | 0 | 15.62 |
| **Barracks 18c musketeer18 damage +3 (lvl 6)** `polba2.musketeer18.1.5` | pol | damage | 3 | 2000 | 0 | 0 | 3800 | 0 | 0 | 15.62 |
| **Barracks 18c musketeer18 damage +3 (lvl 6)** `sweba2.musketeer18.1.5` | swe | damage | 3 | 3000 | 0 | 0 | 200 | 0 | 0 | 15.62 |
| **Barracks 18c musketeer18 damage +3 (lvl 6)** `netba2.musketeer18.1.5` | net | damage | 3 | 2900 | 0 | 0 | 200 | 0 | 0 | 15.62 |
| **Barracks 18c musketeer18 damage +3 (lvl 7)** `ausba2.musketeer18.1.6` | aus,hun,pie,por,rus,spa,swi,ven | damage | 3 | 3500 | 0 | 0 | 800 | 0 | 0 | 15.62 |
| **Barracks 18c musketeer18 damage +3 (lvl 7)** `fraba2.musketeer18.1.6` | fra | damage | 3 | 5500 | 0 | 0 | 2100 | 0 | 0 | 15.62 |
| **Barracks 18c musketeer18 damage +3 (lvl 7)** `engba2.musketeer18.1.6` | eng | damage | 3 | 3500 | 0 | 0 | 700 | 0 | 0 | 15.62 |
| **Barracks 18c musketeer18 damage +3 (lvl 7)** `polba2.musketeer18.1.6` | pol | damage | 3 | 3500 | 0 | 0 | 600 | 0 | 0 | 15.62 |
| **Barracks 18c musketeer18 damage +3 (lvl 7)** `sweba2.musketeer18.1.6` | swe | damage | 3 | 3500 | 0 | 0 | 1400 | 0 | 0 | 15.62 |
| **Barracks 18c musketeer18 damage +3 (lvl 7)** `netba2.musketeer18.1.6` | net | damage | 3 | 3200 | 0 | 0 | 1400 | 0 | 0 | 15.62 |
| **Barracks 18c musketeer18 protection +1 (lvl 2)** `ausba2.musketeer18.2.1` | aus,hun,pie,por,rus,spa,swi,ven | protection | 1 | 3706 | 0 | 0 | 350 | 0 | 0 | 15.62 |
| **Barracks 18c musketeer18 protection +1 (lvl 2)** `fraba2.musketeer18.2.1` | fra | protection | 1 | 3500 | 0 | 0 | 370 | 0 | 0 | 15.62 |
| **Barracks 18c musketeer18 protection +1 (lvl 2)** `engba2.musketeer18.2.1` | eng | protection | 1 | 3750 | 0 | 0 | 370 | 0 | 0 | 15.62 |
| **Barracks 18c musketeer18 protection +1 (lvl 2)** `polba2.musketeer18.2.1` | pol | protection | 1 | 5706 | 0 | 0 | 350 | 0 | 0 | 15.62 |
| **Barracks 18c musketeer18 protection +1 (lvl 2)** `sweba2.musketeer18.2.1` | swe | protection | 1 | 5706 | 0 | 0 | 750 | 0 | 0 | 15.62 |
| **Barracks 18c musketeer18 protection +1 (lvl 2)** `netba2.musketeer18.2.1` | net | protection | 1 | 3906 | 0 | 0 | 350 | 0 | 0 | 15.62 |
| **Barracks 18c musketeer18 protection +2 (lvl 3)** `ausba2.musketeer18.2.2` | aus,hun,pie,por,rus,spa,swi,ven | protection | 2 | 11030 | 0 | 0 | 1350 | 0 | 0 | 15.62 |
| **Barracks 18c musketeer18 protection +2 (lvl 3)** `fraba2.musketeer18.2.2` | fra | protection | 2 | 35030 | 0 | 0 | 1050 | 0 | 0 | 15.62 |
| **Barracks 18c musketeer18 protection +2 (lvl 3)** `engba2.musketeer18.2.2` | eng | protection | 2 | 10020 | 0 | 0 | 1450 | 0 | 0 | 15.62 |
| **Barracks 18c musketeer18 protection +2 (lvl 3)** `polba2.musketeer18.2.2` | pol | protection | 2 | 9030 | 0 | 0 | 4350 | 0 | 0 | 15.62 |
| **Barracks 18c musketeer18 protection +2 (lvl 3)** `sweba2.musketeer18.2.2` | swe | protection | 2 | 9030 | 0 | 0 | 1050 | 0 | 0 | 15.62 |
| **Barracks 18c musketeer18 protection +2 (lvl 3)** `netba2.musketeer18.2.2` | net | protection | 2 | 9030 | 0 | 0 | 1150 | 0 | 0 | 15.62 |
| **Barracks 18c musketeer18 protection +2 (lvl 4)** `ausba2.musketeer18.2.3` | aus,hun,pie,por,rus,spa,swi,ven | protection | 2 | 35706 | 0 | 0 | 4000 | 0 | 0 | 15.62 |
| **Barracks 18c musketeer18 protection +2 (lvl 4)** `fraba2.musketeer18.2.3` | fra | protection | 2 | 11706 | 0 | 0 | 4300 | 0 | 0 | 15.62 |
| **Barracks 18c musketeer18 protection +2 (lvl 4)** `engba2.musketeer18.2.3` | eng | protection | 2 | 34200 | 0 | 0 | 3850 | 0 | 0 | 15.62 |
| **Barracks 18c musketeer18 protection +2 (lvl 4)** `polba2.musketeer18.2.3` | pol | protection | 2 | 32706 | 0 | 0 | 1000 | 0 | 0 | 15.62 |
| **Barracks 18c musketeer18 protection +2 (lvl 4)** `sweba2.musketeer18.2.3` | swe | protection | 2 | 32706 | 0 | 0 | 2900 | 0 | 0 | 15.62 |
| **Barracks 18c musketeer18 protection +2 (lvl 4)** `netba2.musketeer18.2.3` | net | protection | 2 | 37706 | 0 | 0 | 4200 | 0 | 0 | 15.62 |
| **Barracks 18c musketeer18 protection +1 (lvl 5)** `ausba2.musketeer18.2.4` | aus,hun,pie,por,rus,spa,swi,ven | protection | 1 | 36556 | 0 | 0 | 4350 | 0 | 0 | 15.62 |
| **Barracks 18c musketeer18 protection +1 (lvl 5)** `fraba2.musketeer18.2.4` | fra | protection | 1 | 36700 | 0 | 0 | 4450 | 0 | 0 | 15.62 |
| **Barracks 18c musketeer18 protection +1 (lvl 5)** `engba2.musketeer18.2.4` | eng | protection | 1 | 35000 | 0 | 0 | 2350 | 0 | 0 | 15.62 |
| **Barracks 18c musketeer18 protection +1 (lvl 5)** `polba2.musketeer18.2.4` | pol | protection | 1 | 39556 | 0 | 0 | 2350 | 0 | 0 | 15.62 |
| **Barracks 18c musketeer18 protection +1 (lvl 5)** `sweba2.musketeer18.2.4` | swe | protection | 1 | 39556 | 0 | 0 | 5450 | 0 | 0 | 15.62 |
| **Barracks 18c musketeer18 protection +1 (lvl 5)** `netba2.musketeer18.2.4` | net | protection | 1 | 32556 | 0 | 0 | 3350 | 0 | 0 | 15.62 |
| **Barracks 18c musketeer18 protection +2 (lvl 6)** `ausba2.musketeer18.2.5` | aus,hun,pie,por,rus,spa,swe,swi,ven | protection | 2 | 30060 | 0 | 0 | 1350 | 0 | 0 | 15.62 |
| **Barracks 18c musketeer18 protection +2 (lvl 6)** `fraba2.musketeer18.2.5` | fra | protection | 2 | 30160 | 0 | 0 | 1550 | 0 | 0 | 15.62 |
| **Barracks 18c musketeer18 protection +2 (lvl 6)** `engba2.musketeer18.2.5` | eng | protection | 2 | 31250 | 0 | 0 | 3350 | 0 | 0 | 15.62 |
| **Barracks 18c musketeer18 protection +2 (lvl 6)** `polba2.musketeer18.2.5` | pol | protection | 2 | 27060 | 0 | 0 | 3350 | 0 | 0 | 15.62 |
| **Barracks 18c musketeer18 protection +2 (lvl 6)** `netba2.musketeer18.2.5` | net | protection | 2 | 34060 | 0 | 0 | 2350 | 0 | 0 | 15.62 |
| **Barracks 18c musketeer18 protection +2 (lvl 7)** `ausba2.musketeer18.2.6` | aus,hun,pie,por,rus,spa,swe,swi,ven | protection | 2 | 37600 | 0 | 0 | 1350 | 0 | 0 | 15.62 |
| **Barracks 18c musketeer18 protection +2 (lvl 7)** `fraba2.musketeer18.2.6` | fra | protection | 2 | 33600 | 0 | 0 | 1150 | 0 | 0 | 15.62 |
| **Barracks 18c musketeer18 protection +2 (lvl 7)** `engba2.musketeer18.2.6` | eng | protection | 2 | 30570 | 0 | 0 | 1450 | 0 | 0 | 15.62 |
| **Barracks 18c musketeer18 protection +2 (lvl 7)** `polba2.musketeer18.2.6` | pol | protection | 2 | 40600 | 0 | 0 | 1550 | 0 | 0 | 15.62 |
| **Barracks 18c musketeer18 protection +2 (lvl 7)** `netba2.musketeer18.2.6` | net | protection | 2 | 36500 | 0 | 0 | 1550 | 0 | 0 | 15.62 |
| **Barracks 18c musketeer18bav damage +1 (lvl 2)** `bavba2.musketeer18bav.1.1` | bav | damage | 1 | 900 | 0 | 0 | 700 | 0 | 0 | 15.62 |
| **Barracks 18c musketeer18bav damage +1 (lvl 3)** `bavba2.musketeer18bav.1.2` | bav | damage | 1 | 1600 | 0 | 0 | 800 | 0 | 0 | 15.62 |
| **Barracks 18c musketeer18bav damage +1 (lvl 4)** `bavba2.musketeer18bav.1.3` | bav | damage | 1 | 2500 | 0 | 0 | 900 | 0 | 0 | 15.62 |
| **Barracks 18c musketeer18bav damage +1 (lvl 5)** `bavba2.musketeer18bav.1.4` | bav | damage | 1 | 2000 | 0 | 0 | 600 | 0 | 0 | 15.62 |
| **Barracks 18c musketeer18bav damage +1 (lvl 6)** `bavba2.musketeer18bav.1.5` | bav | damage | 1 | 3500 | 0 | 0 | 1000 | 0 | 0 | 15.62 |
| **Barracks 18c musketeer18bav damage +1 (lvl 7)** `bavba2.musketeer18bav.1.6` | bav | damage | 1 | 3000 | 0 | 0 | 800 | 0 | 0 | 15.62 |
| **Barracks 18c musketeer18bav protection +1 (lvl 2)** `bavba2.musketeer18bav.2.1` | bav | protection | 1 | 3500 | 0 | 0 | 350 | 0 | 0 | 15.62 |
| **Barracks 18c musketeer18bav protection +1 (lvl 3)** `bavba2.musketeer18bav.2.2` | bav | protection | 1 | 11230 | 0 | 0 | 1350 | 0 | 0 | 15.62 |
| **Barracks 18c musketeer18bav protection +1 (lvl 4)** `bavba2.musketeer18bav.2.3` | bav | protection | 1 | 35706 | 0 | 0 | 4000 | 0 | 0 | 15.62 |
| **Barracks 18c musketeer18bav protection +2 (lvl 5)** `bavba2.musketeer18bav.2.4` | bav | protection | 2 | 36556 | 0 | 0 | 4350 | 0 | 0 | 15.62 |
| **Barracks 18c musketeer18bav protection +2 (lvl 6)** `bavba2.musketeer18bav.2.5` | bav | protection | 2 | 30060 | 0 | 0 | 1350 | 0 | 0 | 15.62 |
| **Barracks 18c musketeer18bav protection +3 (lvl 7)** `bavba2.musketeer18bav.2.6` | bav | protection | 3 | 37600 | 0 | 0 | 1350 | 0 | 0 | 15.62 |
| **Barracks 18c musketeer18den damage +1 (lvl 2)** `denba2.musketeer18den.1.1` | den | damage | 1 | 900 | 0 | 0 | 700 | 0 | 0 | 15.62 |
| **Barracks 18c musketeer18den damage +1 (lvl 3)** `denba2.musketeer18den.1.2` | den | damage | 1 | 1600 | 0 | 0 | 800 | 0 | 0 | 15.62 |
| **Barracks 18c musketeer18den damage +1 (lvl 4)** `denba2.musketeer18den.1.3` | den | damage | 1 | 2500 | 0 | 0 | 900 | 0 | 0 | 15.62 |
| **Barracks 18c musketeer18den damage +1 (lvl 5)** `denba2.musketeer18den.1.4` | den | damage | 1 | 2000 | 0 | 0 | 600 | 0 | 0 | 15.62 |
| **Barracks 18c musketeer18den damage +1 (lvl 6)** `denba2.musketeer18den.1.5` | den | damage | 1 | 3500 | 0 | 0 | 1000 | 0 | 0 | 15.62 |
| **Barracks 18c musketeer18den damage +1 (lvl 7)** `denba2.musketeer18den.1.6` | den | damage | 1 | 3000 | 0 | 0 | 800 | 0 | 0 | 15.62 |
| **Barracks 18c musketeer18den protection +1 (lvl 2)** `denba2.musketeer18den.2.1` | den | protection | 1 | 3500 | 0 | 0 | 350 | 0 | 0 | 15.62 |
| **Barracks 18c musketeer18den protection +1 (lvl 3)** `denba2.musketeer18den.2.2` | den | protection | 1 | 11230 | 0 | 0 | 1350 | 0 | 0 | 15.62 |
| **Barracks 18c musketeer18den protection +1 (lvl 4)** `denba2.musketeer18den.2.3` | den | protection | 1 | 35706 | 0 | 0 | 4000 | 0 | 0 | 15.62 |
| **Barracks 18c musketeer18den protection +2 (lvl 5)** `denba2.musketeer18den.2.4` | den | protection | 2 | 36556 | 0 | 0 | 4350 | 0 | 0 | 15.62 |
| **Barracks 18c musketeer18den protection +2 (lvl 6)** `denba2.musketeer18den.2.5` | den | protection | 2 | 30060 | 0 | 0 | 1350 | 0 | 0 | 15.62 |
| **Barracks 18c musketeer18den protection +3 (lvl 7)** `denba2.musketeer18den.2.6` | den | protection | 3 | 37600 | 0 | 0 | 1350 | 0 | 0 | 15.62 |
| **Barracks 18c musketeer18pru damage +1 (lvl 2)** `pruba2.musketeer18pru.1.1` | pru | damage | 1 | 900 | 0 | 0 | 700 | 0 | 0 | 15.62 |
| **Barracks 18c musketeer18pru damage +1 (lvl 3)** `pruba2.musketeer18pru.1.2` | pru | damage | 1 | 1600 | 0 | 0 | 800 | 0 | 0 | 15.62 |
| **Barracks 18c musketeer18pru damage +2 (lvl 4)** `pruba2.musketeer18pru.1.3` | pru | damage | 2 | 2500 | 0 | 0 | 900 | 0 | 0 | 15.62 |
| **Barracks 18c musketeer18pru damage +2 (lvl 5)** `pruba2.musketeer18pru.1.4` | pru | damage | 2 | 2000 | 0 | 0 | 600 | 0 | 0 | 15.62 |
| **Barracks 18c musketeer18pru damage +3 (lvl 6)** `pruba2.musketeer18pru.1.5` | pru | damage | 3 | 3500 | 0 | 0 | 1000 | 0 | 0 | 15.62 |
| **Barracks 18c musketeer18pru damage +3 (lvl 7)** `pruba2.musketeer18pru.1.6` | pru | damage | 3 | 3000 | 0 | 0 | 800 | 0 | 0 | 15.62 |
| **Barracks 18c musketeer18pru protection +1 (lvl 2)** `pruba2.musketeer18pru.2.1` | pru | protection | 1 | 3500 | 0 | 0 | 350 | 0 | 0 | 15.62 |
| **Barracks 18c musketeer18pru protection +2 (lvl 3)** `pruba2.musketeer18pru.2.2` | pru | protection | 2 | 11230 | 0 | 0 | 1350 | 0 | 0 | 15.62 |
| **Barracks 18c musketeer18pru protection +2 (lvl 4)** `pruba2.musketeer18pru.2.3` | pru | protection | 2 | 35706 | 0 | 0 | 4000 | 0 | 0 | 15.62 |
| **Barracks 18c musketeer18pru protection +1 (lvl 5)** `pruba2.musketeer18pru.2.4` | pru | protection | 1 | 36556 | 0 | 0 | 4350 | 0 | 0 | 15.62 |
| **Barracks 18c musketeer18pru protection +2 (lvl 6)** `pruba2.musketeer18pru.2.5` | pru | protection | 2 | 30060 | 0 | 0 | 1350 | 0 | 0 | 15.62 |
| **Barracks 18c musketeer18pru protection +2 (lvl 7)** `pruba2.musketeer18pru.2.6` | pru | protection | 2 | 37600 | 0 | 0 | 1350 | 0 | 0 | 15.62 |
| **Barracks 18c musketeer18sax damage +1 (lvl 2)** `saxba2.musketeer18sax.1.1` | sax | damage | 1 | 9000 | 0 | 0 | 200 | 0 | 0 | 15.62 |
| **Barracks 18c musketeer18sax damage +2 (lvl 3)** `saxba2.musketeer18sax.1.2` | sax | damage | 2 | 600 | 0 | 0 | 200 | 0 | 0 | 15.62 |
| **Barracks 18c musketeer18sax damage +2 (lvl 4)** `saxba2.musketeer18sax.1.3` | sax | damage | 2 | 4000 | 0 | 0 | 100 | 0 | 0 | 15.62 |
| **Barracks 18c musketeer18sax damage +1 (lvl 5)** `saxba2.musketeer18sax.1.4` | sax | damage | 1 | 500 | 0 | 0 | 2100 | 0 | 0 | 15.62 |
| **Barracks 18c musketeer18sax damage +2 (lvl 6)** `saxba2.musketeer18sax.1.5` | sax | damage | 2 | 3000 | 0 | 0 | 200 | 0 | 0 | 15.62 |
| **Barracks 18c musketeer18sax damage +2 (lvl 7)** `saxba2.musketeer18sax.1.6` | sax | damage | 2 | 3500 | 0 | 0 | 1400 | 0 | 0 | 15.62 |
| **Barracks 18c musketeer18sax protection +1 (lvl 2)** `saxba2.musketeer18sax.2.1` | sax | protection | 1 | 5706 | 0 | 0 | 750 | 0 | 0 | 15.62 |
| **Barracks 18c musketeer18sax protection +2 (lvl 3)** `saxba2.musketeer18sax.2.2` | sax | protection | 2 | 9030 | 0 | 0 | 1050 | 0 | 0 | 15.62 |
| **Barracks 18c musketeer18sax protection +2 (lvl 4)** `saxba2.musketeer18sax.2.3` | sax | protection | 2 | 32706 | 0 | 0 | 2900 | 0 | 0 | 15.62 |
| **Barracks 18c musketeer18sax protection +1 (lvl 5)** `saxba2.musketeer18sax.2.4` | sax | protection | 1 | 39556 | 0 | 0 | 5450 | 0 | 0 | 15.62 |
| **Barracks 18c musketeer18sax protection +2 (lvl 6)** `saxba2.musketeer18sax.2.5` | sax | protection | 2 | 30060 | 0 | 0 | 1350 | 0 | 0 | 15.62 |
| **Barracks 18c musketeer18sax protection +2 (lvl 7)** `saxba2.musketeer18sax.2.6` | sax | protection | 2 | 37600 | 0 | 0 | 1350 | 0 | 0 | 15.62 |
| **Barracks 18c officer18 damage +30 (lvl 2)** `ausba2.officer18.1.1` | aus,pie,rus,spa,swi,ven | damage | 30 | 1000 | 0 | 0 | 800 | 0 | 0 | 15.62 |
| **Barracks 18c officer18 damage +30 (lvl 2)** `pruba2.officer18.1.1` | den,hun,pru,sax | damage | 30 | 1200 | 0 | 0 | 750 | 0 | 0 | 15.62 |
| **Barracks 18c officer18 damage +30 (lvl 2)** `sweba2.officer18.1.1` | bav,por,swe | damage | 30 | 200 | 0 | 0 | 910 | 0 | 0 | 15.62 |
| **Barracks 18c officer18 damage +30 (lvl 2)** `fraba2.officer18.1.1` | fra | damage | 30 | 1200 | 0 | 0 | 700 | 0 | 0 | 15.62 |
| **Barracks 18c officer18 damage +30 (lvl 2)** `engba2.officer18.1.1` | eng | damage | 30 | 800 | 0 | 0 | 950 | 0 | 0 | 15.62 |
| **Barracks 18c officer18 damage +30 (lvl 2)** `polba2.officer18.1.1` | pol | damage | 30 | 2000 | 0 | 0 | 200 | 0 | 0 | 15.62 |
| **Barracks 18c officer18 damage +30 (lvl 2)** `netba2.officer18.1.1` | net | damage | 30 | 900 | 0 | 0 | 775 | 0 | 0 | 15.62 |
| **Barracks 18c officer18 protection +12 (lvl 2)** `ausba2.officer18.2.1` | aus,pie,rus,spa,swi,ven | protection | 12 | 1706 | 0 | 0 | 350 | 0 | 0 | 15.62 |
| **Barracks 18c officer18 protection +12 (lvl 2)** `pruba2.officer18.2.1` | den,hun,pru,sax | protection | 12 | 1500 | 0 | 0 | 375 | 0 | 0 | 15.62 |
| **Barracks 18c officer18 protection +12 (lvl 2)** `sweba2.officer18.2.1` | bav,por,swe | protection | 12 | 305 | 0 | 0 | 950 | 0 | 0 | 15.62 |
| **Barracks 18c officer18 protection +12 (lvl 2)** `fraba2.officer18.2.1` | fra | protection | 12 | 2105 | 0 | 0 | 450 | 0 | 0 | 15.62 |
| **Barracks 18c officer18 protection +12 (lvl 2)** `engba2.officer18.2.1` | eng | protection | 12 | 2105 | 0 | 0 | 300 | 0 | 0 | 15.62 |
| **Barracks 18c officer18 protection +12 (lvl 2)** `polba2.officer18.2.1` | pol | protection | 12 | 605 | 0 | 0 | 950 | 0 | 0 | 15.62 |
| **Barracks 18c officer18 protection +12 (lvl 2)** `netba2.officer18.2.1` | net | protection | 12 | 1606 | 0 | 0 | 650 | 0 | 0 | 15.62 |
| **Barracks 18c pandur damage +1 (lvl 2)** `ausba2.pandur.1.1` | aus | damage | 1 | 3000 | 0 | 0 | 750 | 0 | 0 | 15.62 |
| **Barracks 18c pandur damage +1 (lvl 3)** `ausba2.pandur.1.2` | aus | damage | 1 | 4000 | 0 | 0 | 1100 | 0 | 0 | 15.62 |
| **Barracks 18c pandur damage +2 (lvl 4)** `ausba2.pandur.1.3` | aus | damage | 2 | 7000 | 0 | 0 | 1800 | 0 | 0 | 15.62 |
| **Barracks 18c pandur damage +1 (lvl 5)** `ausba2.pandur.1.4` | aus | damage | 1 | 12000 | 0 | 0 | 350 | 0 | 0 | 15.62 |
| **Barracks 18c pandur damage +1 (lvl 6)** `ausba2.pandur.1.5` | aus | damage | 1 | 32020 | 0 | 0 | 850 | 0 | 0 | 15.62 |
| **Barracks 18c pandur damage +2 (lvl 7)** `ausba2.pandur.1.6` | aus | damage | 2 | 45200 | 0 | 0 | 1330 | 0 | 0 | 15.62 |
| **Barracks 18c pandur protection +1 (lvl 2)** `ausba2.pandur.2.1` | aus | protection | 1 | 3706 | 0 | 0 | 350 | 0 | 0 | 15.62 |
| **Barracks 18c pandur protection +2 (lvl 3)** `ausba2.pandur.2.2` | aus | protection | 2 | 12060 | 0 | 0 | 1350 | 0 | 0 | 15.62 |
| **Barracks 18c pandur protection +2 (lvl 4)** `ausba2.pandur.2.3` | aus | protection | 2 | 36706 | 0 | 0 | 2250 | 0 | 0 | 15.62 |
| **Barracks 18c pandur protection +1 (lvl 5)** `ausba2.pandur.2.4` | aus | protection | 1 | 36706 | 0 | 0 | 3350 | 0 | 0 | 15.62 |
| **Barracks 18c pandur protection +2 (lvl 6)** `ausba2.pandur.2.5` | aus | protection | 2 | 37060 | 0 | 0 | 1350 | 0 | 0 | 15.62 |
| **Barracks 18c pandur protection +2 (lvl 7)** `ausba2.pandur.2.6` | aus | protection | 2 | 16706 | 0 | 0 | 1350 | 0 | 0 | 15.62 |
| **Barracks 18c pandurhun damage +1 (lvl 2)** `hunba2.pandurhun.1.1` | hun | damage | 1 | 3000 | 0 | 0 | 750 | 0 | 0 | 15.62 |
| **Barracks 18c pandurhun damage +1 (lvl 3)** `hunba2.pandurhun.1.2` | hun | damage | 1 | 4000 | 0 | 0 | 1100 | 0 | 0 | 15.62 |
| **Barracks 18c pandurhun damage +2 (lvl 4)** `hunba2.pandurhun.1.3` | hun | damage | 2 | 7000 | 0 | 0 | 1800 | 0 | 0 | 15.62 |
| **Barracks 18c pandurhun damage +1 (lvl 5)** `hunba2.pandurhun.1.4` | hun | damage | 1 | 12000 | 0 | 0 | 350 | 0 | 0 | 15.62 |
| **Barracks 18c pandurhun damage +1 (lvl 6)** `hunba2.pandurhun.1.5` | hun | damage | 1 | 32020 | 0 | 0 | 850 | 0 | 0 | 15.62 |
| **Barracks 18c pandurhun damage +2 (lvl 7)** `hunba2.pandurhun.1.6` | hun | damage | 2 | 45200 | 0 | 0 | 1330 | 0 | 0 | 15.62 |
| **Barracks 18c pandurhun protection +1 (lvl 2)** `hunba2.pandurhun.2.1` | hun | protection | 1 | 3706 | 0 | 0 | 350 | 0 | 0 | 15.62 |
| **Barracks 18c pandurhun protection +1 (lvl 3)** `hunba2.pandurhun.2.2` | hun | protection | 1 | 12060 | 0 | 0 | 1350 | 0 | 0 | 15.62 |
| **Barracks 18c pandurhun protection +2 (lvl 4)** `hunba2.pandurhun.2.3` | hun | protection | 2 | 36706 | 0 | 0 | 2050 | 0 | 0 | 15.62 |
| **Barracks 18c pandurhun protection +1 (lvl 5)** `hunba2.pandurhun.2.4` | hun | protection | 1 | 36706 | 0 | 0 | 3350 | 0 | 0 | 15.62 |
| **Barracks 18c pandurhun protection +1 (lvl 6)** `hunba2.pandurhun.2.5` | hun | protection | 1 | 37060 | 0 | 0 | 1350 | 0 | 0 | 15.62 |
| **Barracks 18c pandurhun protection +2 (lvl 7)** `hunba2.pandurhun.2.6` | hun | protection | 2 | 16706 | 0 | 0 | 1350 | 0 | 0 | 15.62 |
| **Barracks 18c pikeman18 damage +2 (lvl 2)** `ausba2.pikeman18.1.1` | aus,bav,den,eng,fra,hun,net,pie,pol,por,pru,rus,sax,spa,swi,ven | damage | 2 | 2000 | 0 | 0 | 800 | 0 | 0 | 15.62 |
| **Barracks 18c pikeman18 damage +2 (lvl 3)** `ausba2.pikeman18.1.2` | aus,bav,den,eng,fra,hun,net,pie,pol,por,pru,rus,sax,spa,swi,ven | damage | 2 | 8000 | 0 | 0 | 1200 | 0 | 0 | 15.62 |
| **Barracks 18c pikeman18 damage +2 (lvl 4)** `ausba2.pikeman18.1.3` | aus,bav,den,eng,fra,hun,net,pie,pol,por,pru,rus,sax,spa,swi,ven | damage | 2 | 20000 | 0 | 0 | 2500 | 0 | 0 | 15.62 |
| **Barracks 18c pikeman18 damage +2 (lvl 5)** `ausba2.pikeman18.1.4` | aus,bav,den,eng,fra,hun,net,pie,pol,por,pru,rus,sax,spa,swi,ven | damage | 2 | 32000 | 0 | 0 | 2800 | 0 | 0 | 15.62 |
| **Barracks 18c pikeman18 damage +2 (lvl 6)** `ausba2.pikeman18.1.5` | aus,bav,den,eng,fra,hun,net,pie,pol,por,pru,rus,sax,spa,swi,ven | damage | 2 | 32000 | 0 | 0 | 3800 | 0 | 0 | 15.62 |
| **Barracks 18c pikeman18 damage +2 (lvl 7)** `ausba2.pikeman18.1.6` | aus,bav,den,eng,fra,hun,net,pie,pol,por,pru,rus,sax,spa,swi,ven | damage | 2 | 40500 | 0 | 0 | 4800 | 0 | 0 | 15.62 |
| **Barracks 18c pikeman18 protection +2 (lvl 2)** `ausba2.pikeman18.2.1` | aus,bav,den,eng,fra,hun,net,pie,pol,por,pru,rus,sax,spa,swi,ven | protection | 2 | 1500 | 0 | 0 | 500 | 0 | 0 | 15.62 |
| **Barracks 18c pikeman18 protection +3 (lvl 3)** `ausba2.pikeman18.2.2` | aus,bav,den,eng,fra,hun,net,pie,pol,por,pru,rus,sax,spa,swi,ven | protection | 3 | 7000 | 0 | 0 | 1500 | 0 | 0 | 15.62 |
| **Barracks 18c pikeman18 protection +2 (lvl 4)** `ausba2.pikeman18.2.3` | aus,bav,den,eng,fra,hun,net,pie,pol,por,pru,rus,sax,spa,swi,ven | protection | 2 | 37000 | 0 | 0 | 2000 | 0 | 0 | 15.62 |
| **Barracks 18c pikeman18 protection +3 (lvl 5)** `ausba2.pikeman18.2.4` | aus,bav,den,eng,fra,hun,net,pie,pol,por,pru,rus,sax,spa,swi,ven | protection | 3 | 37000 | 0 | 0 | 5500 | 0 | 0 | 15.62 |
| **Barracks 18c pikeman18 protection +2 (lvl 6)** `ausba2.pikeman18.2.5` | aus,bav,den,eng,fra,hun,net,pie,pol,por,pru,rus,sax,spa,swi,ven | protection | 2 | 37000 | 0 | 0 | 5500 | 0 | 0 | 15.62 |
| **Barracks 18c pikeman18 protection +3 (lvl 7)** `ausba2.pikeman18.2.6` | aus,bav,den,eng,fra,hun,net,pie,pol,por,pru,rus,sax,spa,swi,ven | protection | 3 | 64600 | 0 | 0 | 5500 | 0 | 0 | 15.62 |
| **Barracks 18c pikeman18swe damage +2 (lvl 2)** `sweba2.pikeman18swe.1.1` | swe | damage | 2 | 2000 | 0 | 0 | 800 | 0 | 0 | 15.62 |
| **Barracks 18c pikeman18swe damage +2 (lvl 3)** `sweba2.pikeman18swe.1.2` | swe | damage | 2 | 8000 | 0 | 0 | 1200 | 0 | 0 | 15.62 |
| **Barracks 18c pikeman18swe damage +2 (lvl 4)** `sweba2.pikeman18swe.1.3` | swe | damage | 2 | 20000 | 0 | 0 | 2500 | 0 | 0 | 15.62 |
| **Barracks 18c pikeman18swe damage +2 (lvl 5)** `sweba2.pikeman18swe.1.4` | swe | damage | 2 | 32000 | 0 | 0 | 2800 | 0 | 0 | 15.62 |
| **Barracks 18c pikeman18swe damage +2 (lvl 6)** `sweba2.pikeman18swe.1.5` | swe | damage | 2 | 32000 | 0 | 0 | 3800 | 0 | 0 | 15.62 |
| **Barracks 18c pikeman18swe damage +2 (lvl 7)** `sweba2.pikeman18swe.1.6` | swe | damage | 2 | 40500 | 0 | 0 | 4800 | 0 | 0 | 15.62 |
| **Barracks 18c pikeman18swe protection +2 (lvl 2)** `sweba2.pikeman18swe.2.1` | swe | protection | 2 | 1500 | 0 | 0 | 500 | 0 | 0 | 15.62 |
| **Barracks 18c pikeman18swe protection +3 (lvl 3)** `sweba2.pikeman18swe.2.2` | swe | protection | 3 | 7000 | 0 | 0 | 1500 | 0 | 0 | 15.62 |
| **Barracks 18c pikeman18swe protection +2 (lvl 4)** `sweba2.pikeman18swe.2.3` | swe | protection | 2 | 37000 | 0 | 0 | 2000 | 0 | 0 | 15.62 |
| **Barracks 18c pikeman18swe protection +3 (lvl 5)** `sweba2.pikeman18swe.2.4` | swe | protection | 3 | 37000 | 0 | 0 | 5500 | 0 | 0 | 15.62 |
| **Barracks 18c pikeman18swe protection +2 (lvl 6)** `sweba2.pikeman18swe.2.5` | swe | protection | 2 | 37000 | 0 | 0 | 5500 | 0 | 0 | 15.62 |
| **Barracks 18c pikeman18swe protection +3 (lvl 7)** `sweba2.pikeman18swe.2.6` | swe | protection | 3 | 64600 | 0 | 0 | 5500 | 0 | 0 | 15.62 |
| **Barracks 18c swordsmansco damage +2 (lvl 2)** `scoba2.swordsmansco.1.1` | sco | damage | 2 | 450 | 0 | 0 | 110 | 0 | 0 | 15.62 |
| **Barracks 18c swordsmansco damage +3 (lvl 3)** `scoba2.swordsmansco.1.2` | sco | damage | 3 | 900 | 0 | 0 | 220 | 0 | 0 | 15.62 |
| **Barracks 18c swordsmansco damage +4 (lvl 4)** `scoba2.swordsmansco.1.3` | sco | damage | 4 | 3350 | 0 | 0 | 850 | 0 | 0 | 15.62 |
| **Barracks 18c swordsmansco damage +5 (lvl 5)** `scoba2.swordsmansco.1.4` | sco | damage | 5 | 14400 | 0 | 0 | 2060 | 0 | 0 | 15.62 |
| **Barracks 18c swordsmansco damage +6 (lvl 6)** `scoba2.swordsmansco.1.5` | sco | damage | 6 | 37800 | 0 | 0 | 4525 | 0 | 0 | 15.62 |
| **Barracks 18c swordsmansco damage +10 (lvl 7)** `scoba2.swordsmansco.1.6` | sco | damage | 10 | 90000 | 0 | 0 | 8000 | 0 | 0 | 15.62 |
| **Barracks 18c swordsmansco protection +1 (lvl 2)** `scoba2.swordsmansco.2.1` | sco | protection | 1 | 200 | 0 | 0 | 75 | 0 | 0 | 15.62 |
| **Barracks 18c swordsmansco protection +2 (lvl 3)** `scoba2.swordsmansco.2.2` | sco | protection | 2 | 700 | 0 | 0 | 225 | 0 | 0 | 15.62 |
| **Barracks 18c swordsmansco protection +2 (lvl 4)** `scoba2.swordsmansco.2.3` | sco | protection | 2 | 2500 | 0 | 0 | 560 | 0 | 0 | 15.62 |
| **Barracks 18c swordsmansco protection +2 (lvl 5)** `scoba2.swordsmansco.2.4` | sco | protection | 2 | 7750 | 0 | 0 | 1125 | 0 | 0 | 15.62 |
| **Barracks 18c swordsmansco protection +3 (lvl 6)** `scoba2.swordsmansco.2.5` | sco | protection | 3 | 15800 | 0 | 0 | 1800 | 0 | 0 | 15.62 |
| **Barracks 18c swordsmansco protection +5 (lvl 7)** `scoba2.swordsmansco.2.6` | sco | protection | 5 | 36125 | 0 | 0 | 3350 | 0 | 0 | 15.62 |

## art — Artillery Depot (cannon upgrades)

Каждая запись — одна нация. Если значение одинаковое для всех 21 нации, показано одной строкой с `nation=all`. Если есть per-nation override (через `_country_ModifyUpgrade`), показаны отдельно.

| Апгрейд | nations | itype | val | F | W | S | G | I | C | time |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `ausart.cannon.1.1` | all | price % | — | 0 | 1000 | 500 | 300 | 0 | 0 | 10.0 |
| `ausart.cannon.1.2` | all | price % | — | 0 | 3000 | 1000 | 500 | 0 | 0 | 10.0 |
| `ausart.cannon.1.3` | all | price % | — | 0 | 6000 | 2000 | 1000 | 0 | 0 | 10.0 |
| `ausart.cannon.1.4` | all | price % | — | 1760 | 0 | 0 | 350 | 0 | 0 | 15.62 |
| `ausart.cannon.1.5` | all | price % | — | 1760 | 0 | 0 | 350 | 0 | 0 | 15.62 |
| `ausart.cannon.1.6` | all | price % | — | 1760 | 0 | 0 | 350 | 0 | 0 | 15.62 |
| `ausart.cannon.2.1` | all | build time % | -2500000 | 0 | 0 | 0 | 500 | 1000 | 0 | 10.0 |
| `turart.cannon.2.1` | alg,tur | build time % | -2500000 | 0 | 0 | 0 | 950 | 1000 | 0 | 10.0 |
| `ausart.cannon.2.2` | all | build time % | -2500000 | 0 | 0 | 0 | 1000 | 2000 | 0 | 10.0 |
| `turart.cannon.2.2` | alg,tur | build time % | -2500000 | 0 | 0 | 0 | 150 | 2000 | 0 | 10.0 |
| `ausart.cannon.2.3` | all | build time % | -2500000 | 0 | 0 | 0 | 2000 | 3000 | 0 | 10.0 |
| `turart.cannon.2.3` | alg,tur | build time % | -2500000 | 0 | 0 | 0 | 250 | 3000 | 0 | 10.0 |
| `ausart.cannon.2.4` | all | build time % | -2000000 | 2560 | 0 | 0 | 0 | 0 | 0 | 15.62 |
| `turart.cannon.2.4` | alg,tur | build time % | -2000000 | 2560 | 0 | 0 | 1350 | 0 | 0 | 15.62 |
| `ausart.cannon.2.5` | all | build time % | -2000000 | 3560 | 0 | 0 | 0 | 0 | 0 | 15.62 |
| `turart.cannon.2.5` | alg,tur | build time % | -2000000 | 3560 | 0 | 0 | 2500 | 0 | 0 | 15.62 |
| `ausart.cannon.2.6` | all | build time % | -2000000 | 5560 | 0 | 0 | 0 | 0 | 0 | 15.62 |
| `turart.cannon.2.6` | alg,tur | build time % | -2000000 | 5560 | 0 | 0 | 3350 | 0 | 0 | 15.62 |
| `ausart.howitzer.1.1` | all | price % | — | 0 | 1000 | 500 | 300 | 0 | 0 | 10.0 |
| `ausart.howitzer.1.2` | all | price % | — | 0 | 3000 | 1000 | 500 | 0 | 0 | 10.0 |
| `ausart.howitzer.1.3` | all | price % | — | 0 | 6000 | 2000 | 1000 | 0 | 0 | 10.0 |
| `ausart.howitzer.1.4` | all | price % | — | 1760 | 0 | 0 | 350 | 0 | 0 | 15.62 |
| `ausart.howitzer.1.5` | all | price % | — | 1760 | 0 | 0 | 350 | 0 | 0 | 15.62 |
| `ausart.howitzer.1.6` | all | price % | — | 1760 | 0 | 0 | 350 | 0 | 0 | 15.62 |
| `ausart.howitzer.2.1` | all | build time % | -2500000 | 0 | 0 | 0 | 500 | 1000 | 0 | 10.0 |
| `turart.howitzer.2.1` | alg,tur | build time % | -2500000 | 0 | 0 | 0 | 350 | 1000 | 0 | 10.0 |
| `ausart.howitzer.2.2` | all | build time % | -2500000 | 0 | 0 | 0 | 1000 | 2000 | 0 | 10.0 |
| `turart.howitzer.2.2` | alg,tur | build time % | -2500000 | 0 | 0 | 0 | 450 | 2000 | 0 | 10.0 |
| `ausart.howitzer.2.3` | all | build time % | -2500000 | 0 | 0 | 0 | 2000 | 3000 | 0 | 10.0 |
| `turart.howitzer.2.3` | alg,tur | build time % | -2500000 | 0 | 0 | 0 | 550 | 3000 | 0 | 10.0 |
| `ausart.howitzer.2.4` | all | build time % | -2000000 | 2560 | 0 | 0 | 0 | 0 | 0 | 31.25 |
| `turart.howitzer.2.4` | alg,tur | build time % | -2000000 | 2560 | 0 | 0 | 1150 | 0 | 0 | 31.25 |
| `ausart.howitzer.2.5` | all | build time % | -2000000 | 3560 | 0 | 0 | 0 | 0 | 0 | 31.25 |
| `turart.howitzer.2.5` | alg,tur | build time % | -2000000 | 3560 | 0 | 0 | 3200 | 0 | 0 | 31.25 |
| `ausart.howitzer.2.6` | all | build time % | -2000000 | 5560 | 0 | 0 | 0 | 0 | 0 | 31.25 |
| `turart.howitzer.2.6` | alg,tur | build time % | -2000000 | 5560 | 0 | 0 | 4500 | 0 | 0 | 31.25 |

## cen — Town Hall (era transition)

Каждая запись — одна нация. Если значение одинаковое для всех 21 нации, показано одной строкой с `nation=all`. Если есть per-nation override (через `_country_ModifyUpgrade`), показаны отдельно.

| Апгрейд | nations | itype | val | F | W | S | G | I | C | time |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `auscen.1` | alg,aus,bav,hun,pie,por,rus,sax,sco,spa,swi,tur,ukr | enable unit | 0 | 30000 | 0 | 0 | 5000 | 2000 | 2000 | 9.38 |
| `prucen.1` | den,pru | enable unit | 0 | 20000 | 0 | 0 | 6500 | 1100 | 1100 | 9.38 |
| `fracen.1` | fra | enable unit | 0 | 40000 | 0 | 0 | 3500 | 4000 | 4000 | 9.38 |
| `engcen.1` | eng | enable unit | 0 | 25000 | 0 | 0 | 5000 | 5500 | 5500 | 9.38 |
| `polcen.1` | pol | enable unit | 0 | 30000 | 0 | 0 | 4800 | 2200 | 2200 | 9.38 |
| `swecen.1` | swe | enable unit | 0 | 37000 | 0 | 0 | 5500 | 1500 | 1500 | 9.38 |
| `vencen.1` | ven | enable unit | 0 | 40000 | 0 | 0 | 3000 | 2500 | 2500 | 9.38 |
| `netcen.1` | net | enable unit | 0 | 33000 | 0 | 0 | 4800 | 1800 | 1800 | 9.38 |

## tow — Tower (reload speed)

Каждая запись — одна нация. Если значение одинаковое для всех 21 нации, показано одной строкой с `nation=all`. Если есть per-nation override (через `_country_ModifyUpgrade`), показаны отдельно.

| Апгрейд | nations | itype | val | F | W | S | G | I | C | time |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `eurtow.1` | all | single reload % | -20 | 0 | 0 | 0 | 250 | 0 | 0 | 31.25 |
| `eurtow.2` | all | single reload % | -20 | 0 | 0 | 0 | 0 | 350 | 0 | 31.25 |
| `eurtow.3` | all | single reload % | -10 | 0 | 0 | 0 | 0 | 0 | 400 | 31.25 |
| `eurtow.4` | all | single reload % | -10 | 0 | 0 | 0 | 0 | 450 | 0 | 31.25 |
| `eurtow.5` | all | single reload % | -10 | 0 | 0 | 0 | 0 | 0 | 500 | 31.25 |

## swa — Stone Wall (build gate)

Каждая запись — одна нация. Если значение одинаковое для всех 21 нации, показано одной строкой с `nation=all`. Если есть per-nation override (через `_country_ModifyUpgrade`), показаны отдельно.

| Апгрейд | nations | itype | val | F | W | S | G | I | C | time |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `eurswa.1` | all | build gate | 5 | 0 | 0 | 500 | 0 | 0 | 0 | 0.03 |

## wwa — Palisade (build gate)

Каждая запись — одна нация. Если значение одинаковое для всех 21 нации, показано одной строкой с `nation=all`. Если есть per-nation override (через `_country_ModifyUpgrade`), показаны отдельно.

| Апгрейд | nations | itype | val | F | W | S | G | I | C | time |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `ukrwwa.1` | all | build gate | 5 | 0 | 400 | 0 | 0 | 0 | 0 | 0.03 |

## por — Shipyard (healing)

Каждая запись — одна нация. Если значение одинаковое для всех 21 нации, показано одной строкой с `nation=all`. Если есть per-nation override (через `_country_ModifyUpgrade`), показаны отдельно.

| Апгрейд | nations | itype | val | F | W | S | G | I | C | time |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `eurpor.1` | all | healing | 50 | 0 | 20000 | 0 | 1500 | 0 | 0 | 46.88 |
| `eurpor.1` | eng | healing | 50 | 0 | 12000 | 0 | 500 | 0 | 0 | 46.88 |

## ferry — Ferry (capacity)

Каждая запись — одна нация. Если значение одинаковое для всех 21 нации, показано одной строкой с `nation=all`. Если есть per-nation override (через `_country_ModifyUpgrade`), показаны отдельно.

| Апгрейд | nations | itype | val | F | W | S | G | I | C | time |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| **Improve transport vessel design (+%value% capacity)** `ferry.1` | all | +building capacity | 200 | 1000 | 0 | 0 | 1250 | 0 | 0 | 15.62 |
