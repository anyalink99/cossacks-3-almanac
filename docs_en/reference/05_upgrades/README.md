<a id="улучшения"></a>
# Upgrades

[← Quick reference](../README.md)

Upgrades are grouped by the building where they are researched: Academy,
Blacksmith, Mill, Stable, Barracks, Mine, Tower, Wall, and Shipyard.
The canonical localized name is shown first; the internal code is secondary.

<a id="расшифровка-колонок"></a>
## Column guide

| Column | Meaning |
|---|---|
| **Upgrade** | Canonical name and internal code |
| **Nations** | Nations that can research it. A national variant with a different value appears in its own row. |
| **Effect** | What changes: damage, protection, gathering, construction time, and so on |
| **Value** | Size of the effect. For percentage effects, 50 means +50%. |
| **Food / Wood / Stone / Gold / Iron / Coal** | Research cost |
| **Time** | Research time in game seconds; the building is occupied during this period |

> One row represents one upgrade for one nation or a group of nations. When
> all nations share the same value, they are combined into one row.

<a id="содержание"></a>
## Contents

- [How upgrades combine](#математика-применения-порядок-и-комбинирование)
- [Mine upgrades](#апгрейды-шахт-eurgoleurcoaeuriro)
- [Academy (`aca`)](#aca--академия-исследования)
- [Mill (`mil`)](#mil--мельница-эффективность-еды)
- [Blacksmith (`bla`)](#bla--кузница-по-юнитам--урон-и-защита)
- [Stable (`sta`)](#sta--конюшня-по-юнитам--кавалерия)
- [Barracks, 17th century (`bar`)](#bar--казарма-17-в-по-юнитам)
- [Barracks, 18th century (`ba2`)](#ba2--казарма-18-в-по-юнитам)
- [Artillery Depot (`art`)](#art--артиллерийское-депо-апгрейды-пушек)
- [Town Hall (`cen`)](#cen--городской-центр-переход-эпохи)
- [Tower (`tow`)](#tow--башня-скорость-перезарядки)
- [Stone Wall (`swa`)](#swa--каменная-стена-постройка-ворот)
- [Palisade (`wwa`)](#wwa--палисад-постройка-ворот)
- [Shipyard (`por`)](#por--порт-лечение)
- [Ferry (`ferry`)](#ferry--транспорт-вместимость)

<a id="математика-применения-апгрейдов"></a>
<a id="математика-применения-порядок-и-комбинирование"></a>
<a id="как-складываются-улучшения"></a>
## How upgrades combine

In almost every case, research order **does not affect** a unit’s or
building’s final characteristics. The game stores bonuses separately and
recalculates the result from the same base value.

Rounding can occasionally change price, health, Fishing Boat capacity, or
speed by one point. See [How upgrades are applied](../../recon/world/economy/upgrades_application.md)
for the technical details. In ordinary play, upgrades can be researched in
any convenient order without changing the final damage or protection.

<a id="апгрейды-шахт-eurgoleurcoaeuriro"></a>
<a id="улучшения-шахт"></a>
## Mine upgrades

Universal for all nations (sid does not depend on nation). 6 levels × 3 types of mines.

| Upgrade | Level | Additional workers | Food | Gold |
|---|---:|---:|---:|---:|
| **Enlarge mines and build extensive railroad network for them (+5)** `eurcoa.1` | 2 | +5 | 1000 | 1250 |
| **Enlarge mines and build extensive railroad network for them (+8)** `eurcoa.2` | 3 | +8 | 5250 | 4950 |
| **Enlarge mines and build extensive railroad network for them (+10)** `eurcoa.3` | 4 | +10 | 12500 | 9250 |
| **Enlarge mines and build extensive railroad network for them (+12)** `eurcoa.4` | 5 | +12 | 15800 | 18500 |
| **Enlarge mines and build extensive railroad network for them (+15)** `eurcoa.5` | 6 | +15 | 19800 | 21050 |
| **Enlarge mines and build extensive railroad network for them (+40)** `eurcoa.6` | 7 | +40 | 50200 | 25950 |
| **Enlarge mines and build extensive railroad network for them (+5)** `eurgol.1` | 2 | +5 | 1000 | 1250 |
| **Enlarge mines and build extensive railroad network for them (+8)** `eurgol.2` | 3 | +8 | 5250 | 4950 |
| **Enlarge mines and build extensive railroad network for them (+10)** `eurgol.3` | 4 | +10 | 12500 | 9250 |
| **Enlarge mines and build extensive railroad network for them (+12)** `eurgol.4` | 5 | +12 | 15800 | 18500 |
| **Enlarge mines and build extensive railroad network for them (+15)** `eurgol.5` | 6 | +15 | 19800 | 21050 |
| **Enlarge mines and build extensive railroad network for them (+40)** `eurgol.6` | 7 | +40 | 50200 | 25950 |
| **Enlarge mines and build extensive railroad network for them (+5)** `euriro.1` | 2 | +5 | 1000 | 1250 |
| **Enlarge mines and build extensive railroad network for them (+8)** `euriro.2` | 3 | +8 | 5250 | 4950 |
| **Enlarge mines and build extensive railroad network for them (+10)** `euriro.3` | 4 | +10 | 12500 | 9250 |
| **Enlarge mines and build extensive railroad network for them (+12)** `euriro.4` | 5 | +12 | 15800 | 18500 |
| **Enlarge mines and build extensive railroad network for them (+15)** `euriro.5` | 6 | +15 | 19800 | 21050 |
| **Enlarge mines and build extensive railroad network for them (+40)** `euriro.6` | 7 | +40 | 50200 | 25950 |

<a id="aca--академия-исследования"></a>
<a id="академия-исследования-aca"></a>
## Academy (`aca`)

| Upgrade | Nations | Effect | Value | Price change | Food | Wood | Stone | Gold | Iron | Coal | Time |
|---|---|---|---:|---|---:|---:|---:|---:|---:|---:|---:|
| **Cultivate new cultures of wheat (harvesting +40%)** `ausaca.1` | all | +food eff % | 40 | — | 0 | 200 | 0 | 325 | 0 | 0 | 15.62 |
| **Cultivate new cultures of wheat (harvesting +40%)** `fraaca.1` | France | +food eff % | 40 | — | 0 | 190 | 0 | 315 | 0 | 0 | 15.62 |
| **Raise builders' salary (building construction time -75%)** `ausaca.10` | all | build time % | -7500000 | — | 0 | 0 | 0 | 6950 | 0 | 0 | 15.62 |
| **Raise builders' salary (building construction time -75%)** `ukraca.10` | Ukraine | build time % | -7500000 | — | 0 | 0 | 0 | 1750 | 0 | 0 | 15.62 |
| **Raise builders' salary (building construction time -75%)** `scoaca.10` | Scotland | build time % | -7500000 | — | 0 | 0 | 0 | 2650 | 0 | 0 | 15.62 |
| **Research new fortification grades (durability of walls and towers +80)** `ausaca.11` | Austria, Bavaria, Denmark, England, Hungary, Netherlands, Piedmont, Poland, Portugal, Prussia, Russia, Saxony, Scotland, Spain, Switzerland, Venice | +shield | 80 | — | 0 | 0 | 16200 | 1500 | 0 | 0 | 15.62 |
| **Research new fortification grades (durability of walls and towers +80)** `turaca.11` | Algeria, Turkey | +shield | 80 | — | 0 | 16200 | 0 | 1500 | 0 | 0 | 15.62 |
| **Research new fortification grades (durability of walls and towers +80)** `fraaca.11` | France | +shield | 80 | — | 0 | 0 | 16200 | 500 | 0 | 0 | 15.62 |
| **Research new fortification grades (durability of walls and towers +80)** `sweaca.11` | Sweden | +shield | 80 | — | 0 | 12200 | 16200 | 1100 | 0 | 0 | 15.62 |
| **Research new fortification grades (durability of walls and towers +80)** `ukraca.11` | Ukraine | — | — | — | — | — | — | — | — | — | — |
| **Improve firearms: rifled barrel (fire power +10%)** `ausaca.12` | all | +damage % | 10 | — | 0 | 0 | 0 | 0 | 5000 | 0 | 15.62 |
| **Improve firearms: rifled barrel (fire power +10%)** `algaca.12` | Algeria | — | — | — | — | — | — | — | — | — | — |
| **Research granular gunpowder (fire power +10%)** `ausaca.13` | all | +damage % | 10 | — | 0 | 0 | 0 | 4000 | 0 | 0 | 15.62 |
| **Research granular gunpowder (fire power +10%)** `algaca.13` | Algeria | — | — | — | — | — | — | — | — | — | — |
| **Research new sulphur purification methods (fire power +15%)** `ausaca.14` | all | +damage % | 15 | — | 0 | 0 | 0 | 7000 | 0 | 0 | 15.62 |
| **Research new sulphur purification methods (fire power +15%)** `algaca.14` | Algeria | — | — | — | — | — | — | — | — | — | — |
| **Research new nitre purification methods (fire power +25%)** `ausaca.15` | all | +damage % | 25 | — | 0 | 0 | 0 | 0 | 0 | 11000 | 15.62 |
| **Research new nitre purification methods (fire power +25%)** `algaca.15` | Algeria | — | — | — | — | — | — | — | — | — | — |
| **Research improved additions to gunpowder formula (artillery range +5%)** `ausaca.16` | all | range % | 5 | — | 0 | 0 | 0 | 2000 | 12150 | 0 | 15.62 |
| **Research improved additions to gunpowder formula (artillery range +5%)** `turaca.16` | Algeria, Turkey | range % | 5 | — | 0 | 0 | 0 | 2000 | 0 | 0 | 15.62 |
| **Design new barrel types: unicorn, carronade (artillery range +10%)** `ausaca.17` | all | range % | 10 | — | 0 | 0 | 3000 | 4550 | 19200 | 0 | 15.62 |
| **Design new barrel types: unicorn, carronade (artillery range +10%)** `turaca.17` | Algeria, Turkey | range % | 10 | — | 0 | 0 | 3000 | 4550 | 0 | 0 | 15.62 |
| **Design more durable gun carriage: Gribovalle system (artillery durability +50%)** `ausaca.18` | all | HP % | 50 | — | 0 | 0 | 0 | 500 | 3830 | 1500 | 15.62 |
| **Design multi-barrelled cannon** `ausaca.19` | Austria, Bavaria, Denmark, England, France, Hungary, Netherlands, Piedmont, Poland, Portugal, Prussia, Russia, Saxony, Spain, Sweden, Switzerland, Venice | enable unit | 0 | — | 0 | 0 | 0 | 1500 | 0 | 2500 | 15.62 |
| **Design multi-barrelled cannon** `ukraca.19` | Algeria, Scotland, Turkey, Ukraine | — | — | — | — | — | — | — | — | — | — |
| **Cultivate new cultures of rye (harvesting +50%)** `ausaca.2` | all | +food eff % | 50 | — | 0 | 2400 | 0 | 625 | 0 | 0 | 15.62 |
| **Cultivate new cultures of rye (harvesting +50%)** `turaca.2` | Algeria, Turkey | +food eff % | 50 | — | 0 | 400 | 0 | 522 | 0 | 0 | 15.62 |
| **Research new sighting devices for artillery (artillery accuracy +35%)** `ausaca.20` | all | accuracy % | -35 | — | 0 | 3540 | 0 | 2000 | 0 | 7250 | 15.62 |
| **Research new sighting devices for artillery (artillery accuracy +35%)** `fraaca.20` | France | accuracy % | -35 | — | 0 | 13540 | 0 | 1500 | 0 | 5950 | 15.62 |
| **Research new sighting devices for artillery (artillery accuracy +35%)** `pruaca.20` | Prussia | accuracy % | -35 | — | 0 | 23540 | 0 | 1900 | 0 | 4250 | 15.62 |
| **Finance artillery repair shops (repair all artillery)** `ausaca.21` | all | healing | 25 | — | 0 | 350 | 0 | 100 | 0 | 250 | 15.62 |
| **Develop geology (previously hidden deposits appear on the map)** `ausaca.22` | all | geology | 0 | — | 0 | 0 | 0 | 250 | 0 | 0 | 15.62 |
| **Develop mining (stone excavation efficiency +100%)** `ausaca.23` | all | +stone eff % | 100 | — | 0 | 0 | 0 | 1550 | 3000 | 0 | 15.62 |
| **Raise miners' salary (stone excavation efficiency +200%)** `ausaca.24` | all | +stone eff % | 200 | — | 4200 | 0 | 0 | 1550 | 0 | 12520 | 15.62 |
| **Design Montgolfier (reveals the whole map)** `ausaca.25` | Austria, Bavaria, Denmark, England, France, Hungary, Netherlands, Piedmont, Poland, Portugal, Prussia, Russia, Saxony, Spain, Sweden, Switzerland, Venice | balloon | 0 | — | 0 | 0 | 0 | 5750 | 0 | 0 | 15.62 |
| **Design Montgolfier (reveals the whole map)** `ukraca.25` | Scotland, Ukraine | balloon | 0 | — | 0 | 0 | 0 | 12750 | 0 | 0 | 15.62 |
| **Design Montgolfier (reveals the whole map)** `turaca.25` | Algeria, Turkey | — | — | — | — | — | — | — | — | — | — |
| **Develop medical science (heals all live units)** `ausaca.26` | all | healing | 50 | — | 0 | 0 | 0 | 200 | 0 | 200 | 31.25 |
| **Develop mathematics (artillery accuracy +35%)** `ausaca.27` | all | accuracy % | -35 | — | 0 | 9540 | 0 | 12000 | 0 | 65200 | 15.62 |
| **Develop mathematics (artillery accuracy +35%)** `fraaca.27` | France | accuracy % | -35 | — | 0 | 23580 | 0 | 9800 | 0 | 65400 | 15.62 |
| **Develop mathematics (artillery accuracy +35%)** `pruaca.27` | Prussia | accuracy % | -35 | — | 0 | 12540 | 0 | 8500 | 0 | 57200 | 15.62 |
| **Design new rigging types (ship speed +40%)** `ausaca.28` | Austria, Bavaria, Denmark, France, Hungary, Netherlands, Piedmont, Poland, Portugal, Prussia, Russia, Saxony, Scotland, Spain, Sweden, Switzerland, Venice | speed % | 40 | — | 0 | 65400 | 0 | 24050 | 0 | 0 | 15.62 |
| **Design new rigging types (ship speed +40%)** `turaca.28` | Algeria, Turkey | speed % | 40 | — | 0 | 0 | 0 | 1900 | 0 | 0 | 15.62 |
| **Design new rigging types (ship speed +40%)** `engaca.28` | England | speed % | 40 | — | 0 | 53400 | 0 | 22050 | 0 | 0 | 15.62 |
| **Design new rigging types (ship speed +40%)** `ukraca.28` | Ukraine | speed % | 40 | — | 0 | 0 | 0 | 900 | 0 | 0 | 15.62 |
| **Design new rib system and new hulls (battleship construction)** `ausaca.29` | all | enable unit | 0 | — | 0 | 32300 | 0 | 6800 | 9000 | 12800 | 15.62 |
| **Design new rib system and new hulls (battleship construction)** `engaca.29` | England | enable unit | 0 | — | 0 | 22300 | 0 | 6800 | 7500 | 13200 | 15.62 |
| **Design new rib system and new hulls (battleship construction)** `ukraca.29` | Ukraine | — | — | — | — | — | — | — | — | — | — |
| **Raise agriculturists' salary (harvesting +50%)** `ausaca.3` | all | +food eff % | 50 | — | 0 | 3600 | 0 | 850 | 0 | 0 | 15.62 |
| **Raise agriculturists' salary (harvesting +50%)** `turaca.3` | Turkey | +food eff % | 50 | — | 0 | 2400 | 0 | 850 | 0 | 0 | 15.62 |
| **Raise agriculturists' salary (harvesting +50%)** `algaca.3` | Algeria | +food eff % | 50 | — | 0 | 1240 | 0 | 850 | 0 | 0 | 15.62 |
| **Train carpenters (shipbuilding speed x10)** `ausaca.30` | all | build time % | -5000000 | — | 0 | 2300 | 42700 | 1150 | 0 | 0 | 15.62 |
| **Train carpenters (shipbuilding speed x10)** `turaca.30` | Algeria, Turkey | build time % | -5000000 | — | 0 | 0 | 42700 | 0 | 0 | 0 | 15.62 |
| **Design wheellock (rate of fire +30%)** `ausaca.31` | all | reload % | -30 | — | 0 | 0 | 6000 | 5500 | 4200 | 0 | 15.62 |
| **Design wheellock (rate of fire +30%)** `algaca.31` | Algeria | — | — | — | — | — | — | — | — | — | — |
| **Design flintlock (musket cost -50%)** `ausaca.32` | all | price % | 0 | gold -50% / iron -50% | 0 | 0 | 0 | 6050 | 0 | 7750 | 15.62 |
| **Design flintlock (musket cost -50%)** `ukraca.32` | Algeria, Turkey, Ukraine | — | — | — | — | — | — | — | — | — | — |
| **Design paper cartridge and iron ramrod (rate of fire +30%)** `ausaca.33` | all | reload % | -30 | — | 0 | 5000 | 0 | 5500 | 0 | 15200 | 15.62 |
| **Design paper cartridge and iron ramrod (rate of fire +30%)** `algaca.33` | Algeria | — | — | — | — | — | — | — | — | — | — |
| **Research improved steel grades for cuirasses (armoured soldier defence +2)** `ausaca.34` | all | +shield | 2 | — | 0 | 0 | 0 | 9750 | 0 | 0 | 15.62 |
| **Research improved steel grades for cuirasses (armoured soldier defence +2)** `ukraca.34` | Algeria, Ukraine | — | — | — | — | — | — | — | — | — | — |
| **Research improved steel grades for cuirasses (armoured soldier defence +2)** `turaca.34` | Turkey | +shield | 2 | — | 0 | 0 | 0 | 6950 | 0 | 0 | 15.62 |
| **Design bayonet: barrel-inserted, bayonet with a tube (cold steel weapons +5)** `ausaca.35` | all | +damage | 5 | — | 0 | 0 | 0 | 11500 | 0 | 0 | 15.62 |
| **Design bayonet: barrel-inserted, bayonet with a tube (cold steel weapons +5)** `ukraca.35` | Algeria, Turkey, Ukraine | — | — | — | — | — | — | — | — | — | — |
| **Research new steel grades (18c musketeer/grenadier melee attack efficiency +25%)** `ausaca.36` | all | +damage % | 25 | — | 0 | 0 | 0 | 19500 | 0 | 0 | 15.62 |
| **Research new steel grades (18c musketeer/grenadier melee attack efficiency +25%)** `ukraca.36` | Algeria, Turkey, Ukraine | — | — | — | — | — | — | — | — | — | — |
| **Carry out field melioration (field capacity +200%)** `ausaca.4` | all | +field HP % | 200 | — | 0 | 1000 | 0 | 475 | 0 | 0 | 15.62 |
| **Carry out field melioration (field capacity +200%)** `algaca.4` | Algeria | +field HP % | 200 | — | 0 | 700 | 0 | 475 | 0 | 0 | 15.62 |
| **Design new tackle and fishing nets (boat efficiency +100%)** `ausaca.5` | all | +fish eff % | 100 | — | 0 | 12400 | 0 | 2520 | 0 | 0 | 15.62 |
| **Design new tackle and fishing nets (boat efficiency +100%)** `fraaca.5` | France | +fish eff % | 100 | — | 0 | 13900 | 0 | 2420 | 0 | 0 | 15.62 |
| **Design new tackle and fishing nets (boat efficiency +100%)** `engaca.5` | England | +fish eff % | 100 | — | 0 | 12400 | 0 | 3520 | 0 | 0 | 15.62 |
| **Develop new woodworking methods (frigate building)** `ausaca.6` | Austria, Bavaria, Denmark, England, Hungary, Netherlands, Piedmont, Poland, Portugal, Prussia, Russia, Saxony, Scotland, Spain, Sweden, Switzerland, Venice | enable unit | 0 | — | 0 | 12400 | 0 | 7040 | 0 | 0 | 15.62 |
| **Develop new woodworking methods (xebec building)** `turaca.6` | Algeria, Turkey | enable unit | 0 | — | 0 | 9500 | 0 | 7040 | 0 | 0 | 15.62 |
| **Develop new woodworking methods (frigate building)** `fraaca.6` | France | enable unit | 0 | — | 0 | 13500 | 0 | 7250 | 0 | 0 | 15.62 |
| **Develop new woodworking methods (frigate building)** `ukraca.6` | Ukraine | — | — | — | — | — | — | — | — | — | — |
| **Build new shipyards for fishing boats (fishing boat cost -85%)** `ausaca.7` | all | price % | 0 | wood -85% | 0 | 7300 | 0 | 1220 | 0 | 0 | 15.62 |
| **Build new shipyards for fishing boats (fishing boat cost -85%)** `fraaca.7` | France | price % | 0 | wood -85% | 0 | 7800 | 0 | 1110 | 0 | 0 | 15.62 |
| **Design new woodworking tools (woodcutting efficiency +100%)** `ausaca.8` | all | +wood eff % | 100 | — | 5500 | 0 | 0 | 550 | 0 | 0 | 15.62 |
| **Use new construction materials (durability of buildings +85)** `ausaca.9` | all | +shield | 85 | — | 0 | 9400 | 7850 | 1150 | 0 | 0 | 15.62 |
| **Use new construction materials (durability of buildings +85)** `turaca.9` | Algeria, Turkey | +shield | 85 | — | 0 | 9400 | 0 | 1150 | 0 | 0 | 15.62 |
| **Use new construction materials (durability of buildings +85)** `ukraca.9` | Ukraine | +shield | 85 | — | 0 | 3200 | 7850 | 950 | 0 | 0 | 15.62 |

<a id="mil--мельница-эффективность-еды"></a>
<a id="мельница-эффективность-еды-mil"></a>
## Mill (`mil`)

| Upgrade | Nations | Effect | Value | Price change | Food | Wood | Stone | Gold | Iron | Coal | Time |
|---|---|---|---:|---|---:|---:|---:|---:|---:|---:|---:|
| **Improve grain crops treatment (harvesting +140%)** `eurmil.1` | all | +food eff % | 140 | — | 750 | 0 | 0 | 250 | 0 | 0 | 15.62 |
| **Improve grain crops treatment (harvesting +140%)** `turmil.1` | Algeria, Turkey | +food eff % | 140 | — | 600 | 0 | 0 | 250 | 0 | 0 | 15.62 |
| **Improve grain crops storage (harvesting +180%)** `eurmil.2` | Austria, Bavaria, Denmark, England, France, Hungary, Netherlands, Piedmont, Poland, Portugal, Prussia, Russia, Saxony, Spain, Sweden, Switzerland, Venice | +food eff % | 180 | — | 25600 | 0 | 0 | 3350 | 2000 | 0 | 15.62 |
| **Improve grain crops storage (harvesting +180%)** `rusmil.2` | Scotland, Ukraine | +food eff % | 180 | — | 5600 | 0 | 0 | 1350 | 1900 | 0 | 15.62 |

<a id="bla--кузница-по-юнитам--урон-и-защита"></a>
<a id="кузница-по-юнитам--урон-и-защита-bla"></a>
## Blacksmith (`bla`) — unit damage and protection

| Upgrade | Nations | Effect | Value | Price change | Food | Wood | Stone | Gold | Iron | Coal | Time |
|---|---|---|---:|---|---:|---:|---:|---:|---:|---:|---:|
| **Manufacture agricultural equipment (field capacity +100%)** `ausbla.1` | all | +field HP % | 100 | — | 0 | 400 | 0 | 90 | 0 | 0 | 15.62 |
| **Forge metal armature and gratings (building defence +50)** `ausbla.2` | all | +shield | 50 | — | 0 | 0 | 12320 | 350 | 900 | 0 | 15.62 |
| **Forge harnesses for horses (mounted units recruitment speed -33%)** `ausbla.3` | all | build time % | -3333333 | — | 0 | 0 | 0 | 3650 | 5300 | 8200 | 15.62 |
| **Forge harnesses for horses (mounted units recruitment speed -33%)** `engbla.3` | England | build time % | -3333333 | — | 0 | 0 | 0 | 3550 | 4100 | 6700 | 15.62 |
| **Forge harnesses for horses (mounted units recruitment speed -33%)** `prubla.3` | Prussia | build time % | -3333333 | — | 0 | 0 | 0 | 3650 | 4300 | 5200 | 15.62 |
| **Forge harnesses for horses (mounted units recruitment speed -33%)** `venbla.3` | Venice | build time % | -3333333 | — | 0 | 0 | 0 | 650 | 9800 | 530 | 15.62 |
| **Forge bayonets and broadswords for infantry (18c musketeer/grenadier melee attack +5)** `ausbla.4` | all | +damage | 5 | — | 0 | 1300 | 0 | 1500 | 900 | 5000 | 15.62 |
| **Forge bayonets and broadswords for infantry (18c musketeer/grenadier melee attack +5)** `ukrbla.4` | Algeria, Turkey, Ukraine | — | — | — | — | — | — | — | — | — | — |
| **Forge new types of broadswords and sabres (cavalry and sword clansman attack +5)** `ausbla.5` | all | +damage | 5 | — | 0 | 0 | 0 | 4000 | 7900 | 0 | 15.62 |
| **Forge new types of broadswords and sabres (cavalry and sword clansman attack +5)** `engbla.5` | England | +damage | 5 | — | 0 | 0 | 0 | 6550 | 7900 | 0 | 15.62 |
| **Forge new types of broadswords and sabres (cavalry and sword clansman attack +5)** `prubla.5` | Prussia | +damage | 5 | — | 0 | 0 | 0 | 9550 | 7900 | 0 | 15.62 |
| **Forge new cuirasses (armoured soldiers defence +2)** `ausbla.6` | all | +shield | 2 | — | 0 | 0 | 0 | 4950 | 10500 | 0 | 15.62 |
| **Forge new cuirasses (armoured soldiers defence +2)** `ukrbla.6` | Algeria, Ukraine | — | — | — | — | — | — | — | — | — | — |
| **Forge new cuirasses (armoured soldiers defence +2)** `turbla.6` | Turkey | +shield | 2 | — | 0 | 0 | 0 | 4950 | 10200 | 0 | 15.62 |

<a id="sta--конюшня-по-юнитам--кавалерия"></a>
<a id="конюшня-по-юнитам--кавалерия-sta"></a>
## Stable (`sta`) — cavalry

| Upgrade | Nations | Effect | Value | Price change | Food | Wood | Stone | Gold | Iron | Coal | Time |
|---|---|---|---:|---|---:|---:|---:|---:|---:|---:|---:|
| **Stable cossackdon damage +1 (lvl 2)** `russta.cossackdon.1.1` | Russia | damage | 1 | — | 2000 | 0 | 0 | 500 | 0 | 0 | 15.62 |
| **Stable cossackdon damage +1 (lvl 3)** `russta.cossackdon.1.2` | Russia | damage | 1 | — | 5000 | 0 | 0 | 800 | 0 | 0 | 15.62 |
| **Stable cossackdon damage +2 (lvl 4)** `russta.cossackdon.1.3` | Russia | damage | 2 | — | 10000 | 0 | 0 | 1200 | 0 | 0 | 15.62 |
| **Stable cossackdon damage +2 (lvl 5)** `russta.cossackdon.1.4` | Russia | damage | 2 | — | 20000 | 0 | 0 | 1300 | 0 | 0 | 15.62 |
| **Stable cossackdon damage +3 (lvl 6)** `russta.cossackdon.1.5` | Russia | damage | 3 | — | 30000 | 0 | 0 | 4000 | 0 | 0 | 15.62 |
| **Stable cossackdon damage +3 (lvl 7)** `russta.cossackdon.1.6` | Russia | damage | 3 | — | 20000 | 0 | 0 | 5000 | 0 | 0 | 15.62 |
| **Stable cossackdon protection +1 (lvl 2)** `russta.cossackdon.2.1` | Russia | protection | 1 | — | 2000 | 0 | 0 | 1350 | 0 | 0 | 15.62 |
| **Stable cossackdon protection +1 (lvl 3)** `russta.cossackdon.2.2` | Russia | protection | 1 | — | 1500 | 0 | 0 | 2100 | 0 | 0 | 15.62 |
| **Stable cossackdon protection +1 (lvl 4)** `russta.cossackdon.2.3` | Russia | protection | 1 | — | 5000 | 0 | 0 | 3300 | 0 | 0 | 15.62 |
| **Stable cossackdon protection +1 (lvl 5)** `russta.cossackdon.2.4` | Russia | protection | 1 | — | 10500 | 0 | 0 | 4400 | 0 | 0 | 15.62 |
| **Stable cossackdon protection +2 (lvl 6)** `russta.cossackdon.2.5` | Russia | protection | 2 | — | 12600 | 0 | 0 | 5500 | 0 | 0 | 15.62 |
| **Stable cossackdon protection +2 (lvl 7)** `russta.cossackdon.2.6` | Russia | protection | 2 | — | 40000 | 0 | 0 | 6000 | 0 | 0 | 15.62 |
| **Stable cossackregister damage +1 (lvl 2)** `ukrsta.cossackregister.1.1` | Ukraine | damage | 1 | — | 1000 | 0 | 0 | 3000 | 0 | 0 | 15.62 |
| **Stable cossackregister damage +2 (lvl 3)** `ukrsta.cossackregister.1.2` | Ukraine | damage | 2 | — | 2000 | 0 | 0 | 2000 | 0 | 0 | 15.62 |
| **Stable cossackregister damage +2 (lvl 4)** `ukrsta.cossackregister.1.3` | Ukraine | damage | 2 | — | 7100 | 0 | 0 | 8000 | 0 | 0 | 15.62 |
| **Stable cossackregister damage +2 (lvl 5)** `ukrsta.cossackregister.1.4` | Ukraine | damage | 2 | — | 2250 | 0 | 0 | 2000 | 0 | 0 | 15.62 |
| **Stable cossackregister damage +2 (lvl 6)** `ukrsta.cossackregister.1.5` | Ukraine | damage | 2 | — | 3030 | 0 | 0 | 5000 | 0 | 0 | 15.62 |
| **Stable cossackregister damage +1 (lvl 7)** `ukrsta.cossackregister.1.6` | Ukraine | damage | 1 | — | 7000 | 0 | 0 | 18000 | 0 | 0 | 15.62 |
| **Stable cossackregister protection +2 (lvl 2)** `ukrsta.cossackregister.2.1` | Ukraine | protection | 2 | — | 200 | 0 | 0 | 135 | 3000 | 0 | 15.62 |
| **Stable cossackregister protection +2 (lvl 3)** `ukrsta.cossackregister.2.2` | Ukraine | protection | 2 | — | 2000 | 0 | 0 | 100 | 5000 | 0 | 15.62 |
| **Stable cossackregister protection +2 (lvl 4)** `ukrsta.cossackregister.2.3` | Ukraine | protection | 2 | — | 65000 | 0 | 0 | 200 | 10000 | 0 | 15.62 |
| **Stable cossackregister protection +2 (lvl 5)** `ukrsta.cossackregister.2.4` | Ukraine | protection | 2 | — | 65000 | 0 | 0 | 300 | 4000 | 0 | 15.62 |
| **Stable cossackregister protection +2 (lvl 6)** `ukrsta.cossackregister.2.5` | Ukraine | protection | 2 | — | 65000 | 0 | 0 | 350 | 20000 | 0 | 15.62 |
| **Stable cossackregister protection +2 (lvl 7)** `ukrsta.cossackregister.2.6` | Ukraine | protection | 2 | — | 65000 | 0 | 0 | 1000 | 30000 | 0 | 15.62 |
| **Stable cossacksich damage +1 (lvl 2)** `ukrsta.cossacksich.1.1` | Ukraine | damage | 1 | — | 1000 | 0 | 0 | 3000 | 0 | 0 | 15.62 |
| **Stable cossacksich damage +2 (lvl 3)** `ukrsta.cossacksich.1.2` | Ukraine | damage | 2 | — | 2000 | 0 | 0 | 2000 | 0 | 0 | 15.62 |
| **Stable cossacksich damage +2 (lvl 4)** `ukrsta.cossacksich.1.3` | Ukraine | damage | 2 | — | 7100 | 0 | 0 | 8000 | 0 | 0 | 15.62 |
| **Stable cossacksich damage +1 (lvl 5)** `ukrsta.cossacksich.1.4` | Ukraine | damage | 1 | — | 2250 | 0 | 0 | 2000 | 0 | 0 | 15.62 |
| **Stable cossacksich damage +2 (lvl 6)** `ukrsta.cossacksich.1.5` | Ukraine | damage | 2 | — | 3030 | 0 | 0 | 4000 | 0 | 0 | 15.62 |
| **Stable cossacksich damage +2 (lvl 7)** `ukrsta.cossacksich.1.6` | Ukraine | damage | 2 | — | 7000 | 0 | 0 | 18000 | 0 | 0 | 15.62 |
| **Stable cossacksich protection +2 (lvl 2)** `ukrsta.cossacksich.2.1` | Ukraine | protection | 2 | — | 200 | 0 | 0 | 135 | 3000 | 0 | 15.62 |
| **Stable cossacksich protection +2 (lvl 3)** `ukrsta.cossacksich.2.2` | Ukraine | protection | 2 | — | 2000 | 0 | 0 | 100 | 5000 | 0 | 15.62 |
| **Stable cossacksich protection +2 (lvl 4)** `ukrsta.cossacksich.2.3` | Ukraine | protection | 2 | — | 44930 | 0 | 0 | 200 | 10000 | 0 | 15.62 |
| **Stable cossacksich protection +2 (lvl 5)** `ukrsta.cossacksich.2.4` | Ukraine | protection | 2 | — | 44930 | 0 | 0 | 300 | 4000 | 0 | 15.62 |
| **Stable cossacksich protection +2 (lvl 6)** `ukrsta.cossacksich.2.5` | Ukraine | protection | 2 | — | 44930 | 0 | 0 | 350 | 20000 | 0 | 15.62 |
| **Stable cossacksich protection +2 (lvl 7)** `ukrsta.cossacksich.2.6` | Ukraine | protection | 2 | — | 44930 | 0 | 0 | 1000 | 30000 | 0 | 15.62 |
| **Stable croat damage +1 (lvl 2)** `aussta.croat.1.1` | Austria | damage | 1 | — | 2000 | 0 | 0 | 500 | 0 | 0 | 15.62 |
| **Stable croat damage +2 (lvl 3)** `aussta.croat.1.2` | Austria | damage | 2 | — | 5000 | 0 | 0 | 800 | 0 | 0 | 15.62 |
| **Stable croat damage +2 (lvl 4)** `aussta.croat.1.3` | Austria | damage | 2 | — | 10000 | 0 | 0 | 1200 | 0 | 0 | 15.62 |
| **Stable croat damage +1 (lvl 5)** `aussta.croat.1.4` | Austria | damage | 1 | — | 20000 | 0 | 0 | 1300 | 0 | 0 | 15.62 |
| **Stable croat damage +2 (lvl 6)** `aussta.croat.1.5` | Austria | damage | 2 | — | 30000 | 0 | 0 | 3000 | 0 | 0 | 15.62 |
| **Stable croat damage +2 (lvl 7)** `aussta.croat.1.6` | Austria | damage | 2 | — | 20000 | 0 | 0 | 5000 | 0 | 0 | 15.62 |
| **Stable croat protection +1 (lvl 2)** `aussta.croat.2.1` | Austria | protection | 1 | — | 2000 | 0 | 0 | 1350 | 0 | 0 | 15.62 |
| **Stable croat protection +1 (lvl 3)** `aussta.croat.2.2` | Austria | protection | 1 | — | 1500 | 0 | 0 | 2100 | 0 | 0 | 15.62 |
| **Stable croat protection +2 (lvl 4)** `aussta.croat.2.3` | Austria | protection | 2 | — | 5000 | 0 | 0 | 2300 | 0 | 0 | 15.62 |
| **Stable croat protection +2 (lvl 5)** `aussta.croat.2.4` | Austria | protection | 2 | — | 10500 | 0 | 0 | 3400 | 0 | 0 | 15.62 |
| **Stable croat protection +3 (lvl 6)** `aussta.croat.2.5` | Austria | protection | 3 | — | 12600 | 0 | 0 | 4500 | 0 | 0 | 15.62 |
| **Stable croat protection +3 (lvl 7)** `aussta.croat.2.6` | Austria | protection | 3 | — | 40000 | 0 | 0 | 5000 | 0 | 0 | 15.62 |
| **Stable cuirassier damage +1 (lvl 2)** `aussta.cuirassier.1.1` | Austria, Piedmont, Poland, Russia, Spain, Switzerland, Venice | damage | 1 | — | 12000 | 0 | 0 | 600 | 0 | 0 | 15.62 |
| **Stable cuirassier damage +1 (lvl 2)** `swesta.cuirassier.1.1` | Bavaria, Portugal, Sweden | damage | 1 | — | 11000 | 0 | 0 | 1600 | 0 | 0 | 15.62 |
| **Stable cuirassier damage +1 (lvl 2)** `prusta.cuirassier.1.1` | Denmark, Hungary, Prussia | damage | 1 | — | 10000 | 0 | 0 | 200 | 0 | 0 | 15.62 |
| **Stable cuirassier damage +1 (lvl 2)** `frasta.cuirassier.1.1` | France, Netherlands | damage | 1 | — | 32000 | 0 | 0 | 600 | 0 | 0 | 15.62 |
| **Stable cuirassier damage +1 (lvl 2)** `engsta.cuirassier.1.1` | England | damage | 1 | — | 10000 | 0 | 0 | 900 | 0 | 0 | 15.62 |
| **Stable cuirassier damage +1 (lvl 3)** `aussta.cuirassier.1.2` | Austria, Piedmont, Poland, Russia, Spain, Switzerland, Venice | damage | 1 | — | 32000 | 0 | 0 | 1300 | 0 | 0 | 15.62 |
| **Stable cuirassier damage +1 (lvl 3)** `swesta.cuirassier.1.2` | Bavaria, Portugal, Sweden | damage | 1 | — | 33000 | 0 | 0 | 300 | 0 | 0 | 15.62 |
| **Stable cuirassier damage +1 (lvl 3)** `prusta.cuirassier.1.2` | Denmark, Hungary, Prussia | damage | 1 | — | 34000 | 0 | 0 | 1700 | 0 | 0 | 15.62 |
| **Stable cuirassier damage +1 (lvl 3)** `frasta.cuirassier.1.2` | France | damage | 1 | — | 12000 | 0 | 0 | 2200 | 0 | 0 | 15.62 |
| **Stable cuirassier damage +1 (lvl 3)** `engsta.cuirassier.1.2` | England | damage | 1 | — | 34000 | 0 | 0 | 1000 | 0 | 0 | 15.62 |
| **Stable cuirassier damage +1 (lvl 3)** `netsta.cuirassier.1.2` | Netherlands | damage | 1 | — | 12000 | 0 | 0 | 1300 | 0 | 0 | 15.62 |
| **Stable cuirassier damage +1 (lvl 4)** `aussta.cuirassier.1.3` | Austria, Piedmont, Poland, Russia, Spain, Switzerland, Venice | damage | 1 | — | 62000 | 0 | 0 | 2200 | 0 | 0 | 15.62 |
| **Stable cuirassier damage +1 (lvl 4)** `swesta.cuirassier.1.3` | Bavaria, Portugal, Sweden | damage | 1 | — | 64000 | 0 | 0 | 3200 | 0 | 0 | 15.62 |
| **Stable cuirassier damage +1 (lvl 4)** `prusta.cuirassier.1.3` | Denmark, Hungary, Prussia | damage | 1 | — | 64000 | 0 | 0 | 2100 | 0 | 0 | 15.62 |
| **Stable cuirassier damage +1 (lvl 4)** `frasta.cuirassier.1.3` | France | damage | 1 | — | 62000 | 0 | 0 | 1300 | 0 | 0 | 15.62 |
| **Stable cuirassier damage +1 (lvl 4)** `engsta.cuirassier.1.3` | England | damage | 1 | — | 42000 | 0 | 0 | 3200 | 0 | 0 | 15.62 |
| **Stable cuirassier damage +1 (lvl 4)** `netsta.cuirassier.1.3` | Netherlands | damage | 1 | — | 64000 | 0 | 0 | 2200 | 0 | 0 | 15.62 |
| **Stable cuirassier damage +2 (lvl 5)** `aussta.cuirassier.1.4` | Austria, England, Piedmont, Poland, Russia, Spain, Switzerland, Venice | damage | 2 | — | 61000 | 0 | 0 | 3150 | 0 | 0 | 15.62 |
| **Stable cuirassier damage +2 (lvl 5)** `swesta.cuirassier.1.4` | Bavaria, Portugal, Sweden | damage | 2 | — | 59000 | 0 | 0 | 2150 | 0 | 0 | 15.62 |
| **Stable cuirassier damage +2 (lvl 5)** `prusta.cuirassier.1.4` | Denmark, Hungary, Prussia | damage | 2 | — | 58000 | 0 | 0 | 4150 | 0 | 0 | 15.62 |
| **Stable cuirassier damage +2 (lvl 5)** `frasta.cuirassier.1.4` | France | damage | 2 | — | 57000 | 0 | 0 | 3150 | 0 | 0 | 15.62 |
| **Stable cuirassier damage +2 (lvl 5)** `netsta.cuirassier.1.4` | Netherlands | damage | 2 | — | 58000 | 0 | 0 | 3150 | 0 | 0 | 15.62 |
| **Stable cuirassier damage +2 (lvl 6)** `aussta.cuirassier.1.5` | Austria, Piedmont, Poland, Russia, Spain, Switzerland, Venice | damage | 2 | — | 57055 | 0 | 0 | 4100 | 0 | 0 | 15.62 |
| **Stable cuirassier damage +2 (lvl 6)** `swesta.cuirassier.1.5` | Bavaria, Portugal, Sweden | damage | 2 | — | 52055 | 0 | 0 | 5100 | 0 | 0 | 15.62 |
| **Stable cuirassier damage +2 (lvl 6)** `prusta.cuirassier.1.5` | Denmark, Hungary, Prussia | damage | 2 | — | 59055 | 0 | 0 | 3100 | 0 | 0 | 15.62 |
| **Stable cuirassier damage +2 (lvl 6)** `frasta.cuirassier.1.5` | France | damage | 2 | — | 61055 | 0 | 0 | 8100 | 0 | 0 | 15.62 |
| **Stable cuirassier damage +2 (lvl 6)** `engsta.cuirassier.1.5` | England | damage | 2 | — | 47055 | 0 | 0 | 4100 | 0 | 0 | 15.62 |
| **Stable cuirassier damage +2 (lvl 6)** `netsta.cuirassier.1.5` | Netherlands | damage | 2 | — | 59055 | 0 | 0 | 4100 | 0 | 0 | 15.62 |
| **Stable cuirassier damage +3 (lvl 7)** `aussta.cuirassier.1.6` | Austria, Piedmont, Poland, Russia, Spain, Switzerland, Venice | damage | 3 | — | 49050 | 0 | 0 | 8020 | 0 | 0 | 15.62 |
| **Stable cuirassier damage +3 (lvl 7)** `swesta.cuirassier.1.6` | Bavaria, Portugal, Sweden | damage | 3 | — | 54050 | 0 | 0 | 7020 | 0 | 0 | 15.62 |
| **Stable cuirassier damage +3 (lvl 7)** `prusta.cuirassier.1.6` | Denmark, Hungary, Prussia | damage | 3 | — | 47050 | 0 | 0 | 8150 | 0 | 0 | 15.62 |
| **Stable cuirassier damage +3 (lvl 7)** `frasta.cuirassier.1.6` | France | damage | 3 | — | 47150 | 0 | 0 | 4020 | 0 | 0 | 15.62 |
| **Stable cuirassier damage +3 (lvl 7)** `engsta.cuirassier.1.6` | England | damage | 3 | — | 59050 | 0 | 0 | 11020 | 0 | 0 | 15.62 |
| **Stable cuirassier damage +3 (lvl 7)** `netsta.cuirassier.1.6` | Netherlands | damage | 3 | — | 47050 | 0 | 0 | 8050 | 0 | 0 | 15.62 |
| **Stable cuirassier protection +2 (lvl 2)** `aussta.cuirassier.2.1` | Austria, Piedmont, Poland, Russia, Spain, Switzerland, Venice | protection | 2 | — | 1760 | 0 | 0 | 350 | 1000 | 0 | 15.62 |
| **Stable cuirassier protection +2 (lvl 2)** `swesta.cuirassier.2.1` | Bavaria, Portugal, Sweden | protection | 2 | — | 2505 | 0 | 0 | 350 | 1000 | 0 | 15.62 |
| **Stable cuirassier protection +2 (lvl 2)** `prusta.cuirassier.2.1` | Denmark, Hungary, Prussia | protection | 2 | — | 1520 | 0 | 0 | 450 | 1000 | 0 | 15.62 |
| **Stable cuirassier protection +2 (lvl 2)** `frasta.cuirassier.2.1` | France | protection | 2 | — | 1520 | 0 | 0 | 750 | 1000 | 0 | 15.62 |
| **Stable cuirassier protection +2 (lvl 2)** `engsta.cuirassier.2.1` | England | protection | 2 | — | 1260 | 0 | 0 | 350 | 200 | 0 | 15.62 |
| **Stable cuirassier protection +2 (lvl 2)** `netsta.cuirassier.2.1` | Netherlands | protection | 2 | — | 1250 | 0 | 0 | 450 | 1000 | 0 | 15.62 |
| **Stable cuirassier protection +3 (lvl 3)** `aussta.cuirassier.2.2` | Austria, Piedmont, Poland, Russia, Spain, Switzerland, Venice | protection | 3 | — | 3000 | 0 | 0 | 750 | 2000 | 0 | 15.62 |
| **Stable cuirassier protection +3 (lvl 3)** `swesta.cuirassier.2.2` | Bavaria, Portugal, Sweden | protection | 3 | — | 2000 | 0 | 0 | 300 | 2000 | 0 | 15.62 |
| **Stable cuirassier protection +3 (lvl 3)** `prusta.cuirassier.2.2` | Denmark, Hungary, Prussia | protection | 3 | — | 7000 | 0 | 0 | 750 | 2000 | 0 | 15.62 |
| **Stable cuirassier protection +3 (lvl 3)** `frasta.cuirassier.2.2` | France | protection | 3 | — | 3200 | 0 | 0 | 350 | 1950 | 0 | 15.62 |
| **Stable cuirassier protection +3 (lvl 3)** `engsta.cuirassier.2.2` | England | protection | 3 | — | 3500 | 0 | 0 | 750 | 2800 | 0 | 15.62 |
| **Stable cuirassier protection +3 (lvl 3)** `netsta.cuirassier.2.2` | Netherlands | protection | 3 | — | 2500 | 0 | 0 | 650 | 2000 | 0 | 15.62 |
| **Stable cuirassier protection +3 (lvl 4)** `aussta.cuirassier.2.3` | Austria, Piedmont, Poland, Russia, Spain, Switzerland, Venice | protection | 3 | — | 7600 | 0 | 0 | 300 | 3030 | 0 | 15.62 |
| **Stable cuirassier protection +3 (lvl 4)** `swesta.cuirassier.2.3` | Bavaria, Portugal, Sweden | protection | 3 | — | 5600 | 0 | 0 | 750 | 3030 | 0 | 15.62 |
| **Stable cuirassier protection +3 (lvl 4)** `prusta.cuirassier.2.3` | Denmark, Hungary, Prussia | protection | 3 | — | 3600 | 0 | 0 | 3300 | 3050 | 0 | 15.62 |
| **Stable cuirassier protection +3 (lvl 4)** `frasta.cuirassier.2.3` | France | protection | 3 | — | 7600 | 0 | 0 | 300 | 3110 | 0 | 15.62 |
| **Stable cuirassier protection +3 (lvl 4)** `engsta.cuirassier.2.3` | England | protection | 3 | — | 2600 | 0 | 0 | 900 | 2930 | 0 | 15.62 |
| **Stable cuirassier protection +3 (lvl 4)** `netsta.cuirassier.2.3` | Netherlands | protection | 3 | — | 4600 | 0 | 0 | 200 | 3050 | 0 | 15.62 |
| **Stable cuirassier protection +2 (lvl 5)** `aussta.cuirassier.2.4` | Austria, Piedmont, Poland, Russia, Spain, Switzerland, Venice | protection | 2 | — | 8700 | 0 | 0 | 6200 | 100 | 0 | 15.62 |
| **Stable cuirassier protection +2 (lvl 5)** `swesta.cuirassier.2.4` | Bavaria, Portugal, Sweden | protection | 2 | — | 10700 | 0 | 0 | 6100 | 100 | 0 | 15.62 |
| **Stable cuirassier protection +2 (lvl 5)** `prusta.cuirassier.2.4` | Denmark, Hungary, Prussia | protection | 2 | — | 8700 | 0 | 0 | 3200 | 200 | 0 | 15.62 |
| **Stable cuirassier protection +2 (lvl 5)** `frasta.cuirassier.2.4` | France | protection | 2 | — | 6200 | 0 | 0 | 6200 | 100 | 0 | 15.62 |
| **Stable cuirassier protection +2 (lvl 5)** `engsta.cuirassier.2.4` | England | protection | 2 | — | 12700 | 0 | 0 | 5600 | 200 | 0 | 15.62 |
| **Stable cuirassier protection +2 (lvl 5)** `netsta.cuirassier.2.4` | Netherlands | protection | 2 | — | 11700 | 0 | 0 | 6100 | 100 | 0 | 15.62 |
| **Stable cuirassier protection +1 (lvl 6)** `aussta.cuirassier.2.5` | Austria, Netherlands, Piedmont, Poland, Russia, Spain, Switzerland, Venice | protection | 1 | — | 8700 | 0 | 0 | 2350 | 5000 | 0 | 15.62 |
| **Stable cuirassier protection +1 (lvl 6)** `swesta.cuirassier.2.5` | Bavaria, Portugal, Sweden | protection | 1 | — | 8100 | 0 | 0 | 2150 | 5000 | 0 | 15.62 |
| **Stable cuirassier protection +1 (lvl 6)** `prusta.cuirassier.2.5` | Denmark, Hungary, Prussia | protection | 1 | — | 8700 | 0 | 0 | 2650 | 4300 | 0 | 15.62 |
| **Stable cuirassier protection +1 (lvl 6)** `frasta.cuirassier.2.5` | France | protection | 1 | — | 11700 | 0 | 0 | 4450 | 7000 | 0 | 15.62 |
| **Stable cuirassier protection +1 (lvl 6)** `engsta.cuirassier.2.5` | England | protection | 1 | — | 5700 | 0 | 0 | 1350 | 7000 | 0 | 15.62 |
| **Stable cuirassier protection +1 (lvl 7)** `aussta.cuirassier.2.6` | Austria, Netherlands, Piedmont, Poland, Russia, Spain, Switzerland, Venice | protection | 1 | — | 9700 | 0 | 0 | 4444 | 7060 | 0 | 15.62 |
| **Stable cuirassier protection +1 (lvl 7)** `swesta.cuirassier.2.6` | Bavaria, Portugal, Sweden | protection | 1 | — | 9200 | 0 | 0 | 4900 | 7060 | 0 | 15.62 |
| **Stable cuirassier protection +1 (lvl 7)** `prusta.cuirassier.2.6` | Denmark, Hungary, Prussia | protection | 1 | — | 11200 | 0 | 0 | 4700 | 6760 | 0 | 15.62 |
| **Stable cuirassier protection +1 (lvl 7)** `frasta.cuirassier.2.6` | France | protection | 1 | — | 9700 | 0 | 0 | 3244 | 5060 | 0 | 15.62 |
| **Stable cuirassier protection +1 (lvl 7)** `engsta.cuirassier.2.6` | England | protection | 1 | — | 12700 | 0 | 0 | 5424 | 5060 | 0 | 15.62 |
| **Stable dragoon damage +1 (lvl 2)** `aussta.dragoon.1.1` | Austria, Bavaria, France, Piedmont, Portugal, Spain, Sweden, Switzerland, Venice | damage | 1 | — | 500 | 0 | 0 | 150 | 0 | 0 | 15.62 |
| **Stable dragoon damage +1 (lvl 2)** `prusta.dragoon.1.1` | Denmark, Hungary, Netherlands, Prussia, Saxony | damage | 1 | — | 700 | 0 | 0 | 250 | 0 | 0 | 15.62 |
| **Stable dragoon damage +1 (lvl 2)** `engsta.dragoon.1.1` | England | damage | 1 | — | 400 | 0 | 0 | 150 | 0 | 0 | 15.62 |
| **Stable dragoon damage +1 (lvl 3)** `aussta.dragoon.1.2` | Austria, Bavaria, France, Piedmont, Portugal, Spain, Sweden, Switzerland, Venice | damage | 1 | — | 700 | 0 | 0 | 200 | 0 | 0 | 15.62 |
| **Stable dragoon damage +1 (lvl 3)** `prusta.dragoon.1.2` | Denmark, Hungary, Prussia, Saxony | damage | 1 | — | 500 | 0 | 0 | 100 | 0 | 0 | 15.62 |
| **Stable dragoon damage +1 (lvl 3)** `engsta.dragoon.1.2` | England | damage | 1 | — | 800 | 0 | 0 | 200 | 0 | 0 | 15.62 |
| **Stable dragoon damage +1 (lvl 3)** `netsta.dragoon.1.2` | Netherlands | damage | 1 | — | 600 | 0 | 0 | 100 | 0 | 0 | 15.62 |
| **Stable dragoon damage +2 (lvl 4)** `aussta.dragoon.1.3` | Austria, Bavaria, France, Piedmont, Portugal, Spain, Sweden, Switzerland, Venice | damage | 2 | — | 900 | 0 | 0 | 340 | 0 | 0 | 15.62 |
| **Stable dragoon damage +2 (lvl 4)** `prusta.dragoon.1.3` | Denmark, Hungary, Prussia, Saxony | damage | 2 | — | 900 | 0 | 0 | 640 | 0 | 0 | 15.62 |
| **Stable dragoon damage +2 (lvl 4)** `engsta.dragoon.1.3` | England | damage | 2 | — | 300 | 0 | 0 | 340 | 0 | 0 | 15.62 |
| **Stable dragoon damage +2 (lvl 4)** `netsta.dragoon.1.3` | Netherlands | damage | 2 | — | 800 | 0 | 0 | 540 | 0 | 0 | 15.62 |
| **Stable dragoon damage +1 (lvl 5)** `aussta.dragoon.1.4` | Austria, Bavaria, Denmark, England, France, Hungary, Netherlands, Piedmont, Portugal, Prussia, Saxony, Spain, Sweden, Switzerland, Venice | damage | 1 | — | 0 | 0 | 0 | 0 | 0 | 0 | 15.62 |
| **Stable dragoon damage +1 (lvl 6)** `aussta.dragoon.1.5` | Austria, Bavaria, Denmark, England, France, Hungary, Netherlands, Piedmont, Portugal, Prussia, Saxony, Spain, Sweden, Switzerland, Venice | damage | 1 | — | 0 | 0 | 0 | 0 | 0 | 0 | 15.62 |
| **Stable dragoon damage +3 (lvl 7)** `aussta.dragoon.1.6` | Austria, Bavaria, Denmark, England, France, Hungary, Netherlands, Piedmont, Portugal, Prussia, Saxony, Spain, Sweden, Switzerland, Venice | damage | 3 | — | 0 | 0 | 0 | 0 | 0 | 0 | 15.62 |
| **Stable dragoon protection +1 (lvl 2)** `aussta.dragoon.2.1` | Austria, Bavaria, France, Piedmont, Portugal, Spain, Sweden, Switzerland, Venice | protection | 1 | — | 900 | 0 | 0 | 150 | 0 | 0 | 15.62 |
| **Stable dragoon protection +1 (lvl 2)** `prusta.dragoon.2.1` | Denmark, Hungary, Prussia, Saxony | protection | 1 | — | 500 | 0 | 0 | 250 | 0 | 0 | 15.62 |
| **Stable dragoon protection +1 (lvl 2)** `engsta.dragoon.2.1` | England | protection | 1 | — | 1300 | 0 | 0 | 250 | 0 | 0 | 15.62 |
| **Stable dragoon protection +1 (lvl 2)** `netsta.dragoon.2.1` | Netherlands | protection | 1 | — | 400 | 0 | 0 | 250 | 0 | 0 | 15.62 |
| **Stable dragoon protection +2 (lvl 3)** `aussta.dragoon.2.2` | Austria, Bavaria, France, Piedmont, Portugal, Spain, Switzerland, Venice | protection | 2 | — | 6600 | 0 | 0 | 750 | 0 | 0 | 15.62 |
| **Stable dragoon protection +2 (lvl 3)** `prusta.dragoon.2.2` | Denmark, Hungary, Prussia, Saxony | protection | 2 | — | 6300 | 0 | 0 | 850 | 0 | 0 | 15.62 |
| **Stable dragoon protection +2 (lvl 3)** `engsta.dragoon.2.2` | England | protection | 2 | — | 5200 | 0 | 0 | 650 | 0 | 0 | 15.62 |
| **Stable dragoon protection +2 (lvl 3)** `swesta.dragoon.2.2` | Sweden | protection | 2 | — | 6600 | 0 | 0 | 650 | 0 | 0 | 15.62 |
| **Stable dragoon protection +2 (lvl 3)** `netsta.dragoon.2.2` | Netherlands | protection | 2 | — | 7600 | 0 | 0 | 550 | 0 | 0 | 15.62 |
| **Stable dragoon protection +2 (lvl 4)** `aussta.dragoon.2.3` | Austria, Bavaria, France, Piedmont, Portugal, Spain, Sweden, Switzerland, Venice | protection | 2 | — | 5000 | 0 | 0 | 1250 | 0 | 0 | 15.62 |
| **Stable dragoon protection +2 (lvl 4)** `prusta.dragoon.2.3` | Denmark, Hungary, Prussia, Saxony | protection | 2 | — | 4600 | 0 | 0 | 1350 | 0 | 0 | 15.62 |
| **Stable dragoon protection +2 (lvl 4)** `engsta.dragoon.2.3` | England | protection | 2 | — | 2000 | 0 | 0 | 1450 | 0 | 0 | 15.62 |
| **Stable dragoon protection +2 (lvl 4)** `netsta.dragoon.2.3` | Netherlands | protection | 2 | — | 4000 | 0 | 0 | 950 | 0 | 0 | 15.62 |
| **Stable dragoon protection +1 (lvl 5)** `aussta.dragoon.2.4` | Austria, Bavaria, France, Piedmont, Spain, Sweden, Switzerland, Venice | protection | 1 | — | 3000 | 0 | 0 | 700 | 0 | 0 | 15.62 |
| **Stable dragoon protection +1 (lvl 5)** `prusta.dragoon.2.4` | Denmark, Prussia, Saxony | protection | 1 | — | 2500 | 0 | 0 | 750 | 0 | 0 | 15.62 |
| **Stable dragoon protection +1 (lvl 5)** `engsta.dragoon.2.4` | England | protection | 1 | — | 6000 | 0 | 0 | 100 | 0 | 0 | 15.62 |
| **Stable dragoon protection +1 (lvl 5)** `netsta.dragoon.2.4` | Netherlands | protection | 1 | — | 4000 | 0 | 0 | 900 | 0 | 0 | 15.62 |
| **Stable dragoon protection +1 (lvl 5)** `porsta.dragoon.2.4` | Portugal | protection | 1 | — | 3000 | 0 | 0 | 600 | 0 | 0 | 15.62 |
| **Stable dragoon protection +1 (lvl 5)** `hunsta.dragoon.2.4` | Hungary | protection | 1 | — | 2500 | 0 | 0 | 700 | 0 | 0 | 15.62 |
| **Stable dragoon protection +2 (lvl 6)** `aussta.dragoon.2.5` | Austria, Bavaria, France, Piedmont, Portugal, Spain, Sweden, Switzerland, Venice | protection | 2 | — | 1000 | 0 | 0 | 2350 | 0 | 0 | 15.62 |
| **Stable dragoon protection +2 (lvl 6)** `prusta.dragoon.2.5` | Denmark, Hungary, Prussia, Saxony | protection | 2 | — | 800 | 0 | 0 | 2750 | 0 | 0 | 15.62 |
| **Stable dragoon protection +2 (lvl 6)** `engsta.dragoon.2.5` | England | protection | 2 | — | 1000 | 0 | 0 | 3250 | 0 | 0 | 15.62 |
| **Stable dragoon protection +2 (lvl 6)** `netsta.dragoon.2.5` | Netherlands | protection | 2 | — | 4000 | 0 | 0 | 2150 | 0 | 0 | 15.62 |
| **Stable dragoon protection +2 (lvl 7)** `spasta.dragoon.2.6` | Bavaria, Piedmont, Portugal, Spain, Sweden, Switzerland, Venice | protection | 2 | — | 6001 | 0 | 0 | 6000 | 0 | 0 | 15.62 |
| **Stable dragoon protection +2 (lvl 7)** `densta.dragoon.2.6` | Denmark, Hungary, Saxony | protection | 2 | — | 2001 | 0 | 0 | 8200 | 0 | 0 | 15.62 |
| **Stable dragoon protection +2 (lvl 7)** `aussta.dragoon.2.6` | Austria, France | protection | 2 | — | 6001 | 0 | 0 | 5000 | 0 | 0 | 15.62 |
| **Stable dragoon protection +2 (lvl 7)** `engsta.dragoon.2.6` | England | protection | 2 | — | 7001 | 0 | 0 | 4400 | 0 | 0 | 15.62 |
| **Stable dragoon protection +2 (lvl 7)** `prusta.dragoon.2.6` | Prussia | protection | 2 | — | 2001 | 0 | 0 | 7200 | 0 | 0 | 15.62 |
| **Stable dragoon protection +2 (lvl 7)** `netsta.dragoon.2.6` | Netherlands | protection | 2 | — | 3001 | 0 | 0 | 6200 | 0 | 0 | 15.62 |
| **Stable dragoon18 damage +2 (lvl 2)** `aussta.dragoon18.1.1` | Austria, Bavaria, Poland, Portugal, Russia, Spain, Sweden, Switzerland, Venice | damage | 2 | — | 2000 | 0 | 0 | 100 | 0 | 0 | 15.62 |
| **Stable dragoon18 damage +2 (lvl 2)** `prusta.dragoon18.1.1` | Denmark, Prussia, Saxony | damage | 2 | — | 4500 | 0 | 0 | 200 | 0 | 0 | 15.62 |
| **Stable dragoon18 damage +2 (lvl 2)** `engsta.dragoon18.1.1` | England | damage | 2 | — | 1000 | 0 | 0 | 200 | 0 | 0 | 15.62 |
| **Stable dragoon18 damage +2 (lvl 3)** `aussta.dragoon18.1.2` | Austria, Bavaria, Poland, Portugal, Russia, Spain, Sweden, Switzerland, Venice | damage | 2 | — | 9000 | 0 | 0 | 350 | 0 | 0 | 15.62 |
| **Stable dragoon18 damage +2 (lvl 3)** `prusta.dragoon18.1.2` | Denmark, Prussia, Saxony | damage | 2 | — | 5500 | 0 | 0 | 250 | 0 | 0 | 15.62 |
| **Stable dragoon18 damage +2 (lvl 3)** `engsta.dragoon18.1.2` | England | damage | 2 | — | 10200 | 0 | 0 | 250 | 0 | 0 | 15.62 |
| **Stable dragoon18 damage +4 (lvl 4)** `aussta.dragoon18.1.3` | Austria, Bavaria, Poland, Portugal, Russia, Spain, Sweden, Switzerland, Venice | damage | 4 | — | 12000 | 0 | 0 | 400 | 0 | 0 | 15.62 |
| **Stable dragoon18 damage +4 (lvl 4)** `prusta.dragoon18.1.3` | Denmark, Prussia, Saxony | damage | 4 | — | 22000 | 0 | 0 | 500 | 0 | 0 | 15.62 |
| **Stable dragoon18 damage +4 (lvl 4)** `engsta.dragoon18.1.3` | England | damage | 4 | — | 15200 | 0 | 0 | 200 | 0 | 0 | 15.62 |
| **Stable dragoon18 damage +2 (lvl 5)** `aussta.dragoon18.1.4` | Austria, Bavaria, Poland, Portugal, Russia, Spain, Sweden, Switzerland, Venice | damage | 2 | — | 23000 | 0 | 0 | 580 | 0 | 0 | 15.62 |
| **Stable dragoon18 damage +2 (lvl 5)** `prusta.dragoon18.1.4` | Denmark, Prussia, Saxony | damage | 2 | — | 13000 | 0 | 0 | 480 | 0 | 0 | 15.62 |
| **Stable dragoon18 damage +2 (lvl 5)** `engsta.dragoon18.1.4` | England | damage | 2 | — | 19850 | 0 | 0 | 280 | 0 | 0 | 15.62 |
| **Stable dragoon18 damage +2 (lvl 6)** `aussta.dragoon18.1.5` | Austria, Bavaria, Poland, Portugal, Russia, Spain, Sweden, Switzerland, Venice | damage | 2 | — | 32000 | 0 | 0 | 680 | 0 | 0 | 15.62 |
| **Stable dragoon18 damage +2 (lvl 6)** `prusta.dragoon18.1.5` | Denmark, Prussia, Saxony | damage | 2 | — | 42000 | 0 | 0 | 780 | 0 | 0 | 15.62 |
| **Stable dragoon18 damage +2 (lvl 6)** `engsta.dragoon18.1.5` | England | damage | 2 | — | 32000 | 0 | 0 | 1180 | 0 | 0 | 15.62 |
| **Stable dragoon18 damage +4 (lvl 7)** `aussta.dragoon18.1.6` | Austria, Bavaria, Poland, Portugal, Russia, Spain, Sweden, Switzerland, Venice | damage | 4 | — | 42000 | 0 | 0 | 780 | 0 | 0 | 15.62 |
| **Stable dragoon18 damage +4 (lvl 7)** `prusta.dragoon18.1.6` | Denmark, Prussia, Saxony | damage | 4 | — | 32000 | 0 | 0 | 680 | 0 | 0 | 15.62 |
| **Stable dragoon18 damage +4 (lvl 7)** `engsta.dragoon18.1.6` | England | damage | 4 | — | 32000 | 0 | 0 | 980 | 0 | 0 | 15.62 |
| **Stable dragoon18 protection +1 (lvl 2)** `aussta.dragoon18.2.1` | Austria, Poland, Russia, Spain, Switzerland, Venice | protection | 1 | — | 760 | 0 | 0 | 935 | 0 | 0 | 15.62 |
| **Stable dragoon18 protection +1 (lvl 2)** `swesta.dragoon18.2.1` | Bavaria, Portugal, Sweden | protection | 1 | — | 260 | 0 | 0 | 935 | 0 | 0 | 15.62 |
| **Stable dragoon18 protection +1 (lvl 2)** `prusta.dragoon18.2.1` | Denmark, Prussia, Saxony | protection | 1 | — | 750 | 0 | 0 | 935 | 0 | 0 | 15.62 |
| **Stable dragoon18 protection +1 (lvl 2)** `engsta.dragoon18.2.1` | England | protection | 1 | — | 250 | 0 | 0 | 999 | 0 | 0 | 15.62 |
| **Stable dragoon18 protection +1 (lvl 3)** `aussta.dragoon18.2.2` | Austria, Denmark, Poland, Prussia, Russia, Saxony, Spain, Switzerland, Venice | protection | 1 | — | 1260 | 0 | 0 | 1150 | 0 | 0 | 15.62 |
| **Stable dragoon18 protection +1 (lvl 3)** `swesta.dragoon18.2.2` | Bavaria, Portugal, Sweden | protection | 1 | — | 1460 | 0 | 0 | 1150 | 0 | 0 | 15.62 |
| **Stable dragoon18 protection +1 (lvl 3)** `engsta.dragoon18.2.2` | England | protection | 1 | — | 1360 | 0 | 0 | 1250 | 0 | 0 | 15.62 |
| **Stable dragoon18 protection +2 (lvl 4)** `aussta.dragoon18.2.3` | Austria, Poland, Russia, Spain, Switzerland, Venice | protection | 2 | — | 15600 | 0 | 0 | 2350 | 0 | 0 | 15.62 |
| **Stable dragoon18 protection +2 (lvl 4)** `swesta.dragoon18.2.3` | Bavaria, Portugal, Sweden | protection | 2 | — | 12600 | 0 | 0 | 3350 | 0 | 0 | 15.62 |
| **Stable dragoon18 protection +2 (lvl 4)** `prusta.dragoon18.2.3` | Denmark, Prussia, Saxony | protection | 2 | — | 10600 | 0 | 0 | 2350 | 0 | 0 | 15.62 |
| **Stable dragoon18 protection +2 (lvl 4)** `engsta.dragoon18.2.3` | England | protection | 2 | — | 17600 | 0 | 0 | 2150 | 0 | 0 | 15.62 |
| **Stable dragoon18 protection +1 (lvl 5)** `aussta.dragoon18.2.4` | Austria, Poland, Russia, Spain, Switzerland, Venice | protection | 1 | — | 17600 | 0 | 0 | 3350 | 0 | 0 | 15.62 |
| **Stable dragoon18 protection +1 (lvl 5)** `densta.dragoon18.2.4` | Denmark, Saxony | protection | 1 | — | 22600 | 0 | 0 | 5350 | 0 | 0 | 15.62 |
| **Stable dragoon18 protection +1 (lvl 5)** `porsta.dragoon18.2.4` | Bavaria, Portugal | protection | 1 | — | 19600 | 0 | 0 | 3350 | 0 | 0 | 15.62 |
| **Stable dragoon18 protection +1 (lvl 5)** `engsta.dragoon18.2.4` | England | protection | 1 | — | 15600 | 0 | 0 | 5350 | 0 | 0 | 15.62 |
| **Stable dragoon18 protection +1 (lvl 5)** `swesta.dragoon18.2.4` | Sweden | protection | 1 | — | 19600 | 0 | 0 | 2350 | 0 | 0 | 15.62 |
| **Stable dragoon18 protection +1 (lvl 5)** `prusta.dragoon18.2.4` | Prussia | protection | 1 | — | 22600 | 0 | 0 | 6350 | 0 | 0 | 15.62 |
| **Stable dragoon18 protection +2 (lvl 6)** `aussta.dragoon18.2.5` | Austria, Poland, Russia, Spain, Switzerland, Venice | protection | 2 | — | 19600 | 0 | 0 | 5350 | 0 | 0 | 15.62 |
| **Stable dragoon18 protection +2 (lvl 6)** `engsta.dragoon18.2.5` | Denmark, England, Saxony | protection | 2 | — | 19600 | 0 | 0 | 3350 | 0 | 0 | 15.62 |
| **Stable dragoon18 protection +2 (lvl 6)** `swesta.dragoon18.2.5` | Bavaria, Portugal, Sweden | protection | 2 | — | 12600 | 0 | 0 | 7350 | 0 | 0 | 15.62 |
| **Stable dragoon18 protection +2 (lvl 6)** `prusta.dragoon18.2.5` | Prussia | protection | 2 | — | 19600 | 0 | 0 | 4350 | 0 | 0 | 15.62 |
| **Stable dragoon18 protection +3 (lvl 7)** `aussta.dragoon18.2.6` | Austria, Poland, Russia, Spain, Switzerland, Venice | protection | 3 | — | 21760 | 0 | 0 | 9350 | 0 | 0 | 15.62 |
| **Stable dragoon18 protection +3 (lvl 7)** `prusta.dragoon18.2.6` | Denmark, Prussia, Saxony | protection | 3 | — | 15760 | 0 | 0 | 9350 | 0 | 0 | 15.62 |
| **Stable dragoon18 protection +3 (lvl 7)** `swesta.dragoon18.2.6` | Bavaria, Sweden | protection | 3 | — | 26760 | 0 | 0 | 7350 | 0 | 0 | 15.62 |
| **Stable dragoon18 protection +3 (lvl 7)** `engsta.dragoon18.2.6` | England | protection | 3 | — | 25760 | 0 | 0 | 8350 | 0 | 0 | 15.62 |
| **Stable dragoon18 protection +3 (lvl 7)** `porsta.dragoon18.2.6` | Portugal | protection | 3 | — | 26760 | 0 | 0 | 6350 | 0 | 0 | 15.62 |
| **Stable dragoon18fra damage +2 (lvl 2)** `frasta.dragoon18fra.1.1` | France | damage | 2 | — | 2000 | 0 | 0 | 100 | 0 | 0 | 15.62 |
| **Stable dragoon18fra damage +2 (lvl 3)** `frasta.dragoon18fra.1.2` | France | damage | 2 | — | 9000 | 0 | 0 | 350 | 0 | 0 | 15.62 |
| **Stable dragoon18fra damage +4 (lvl 4)** `frasta.dragoon18fra.1.3` | France | damage | 4 | — | 12000 | 0 | 0 | 400 | 0 | 0 | 15.62 |
| **Stable dragoon18fra damage +2 (lvl 5)** `frasta.dragoon18fra.1.4` | France | damage | 2 | — | 23000 | 0 | 0 | 580 | 0 | 0 | 15.62 |
| **Stable dragoon18fra damage +2 (lvl 6)** `frasta.dragoon18fra.1.5` | France | damage | 2 | — | 32000 | 0 | 0 | 680 | 0 | 0 | 15.62 |
| **Stable dragoon18fra damage +4 (lvl 7)** `frasta.dragoon18fra.1.6` | France | damage | 4 | — | 42000 | 0 | 0 | 780 | 0 | 0 | 15.62 |
| **Stable dragoon18fra protection +1 (lvl 2)** `frasta.dragoon18fra.2.1` | France | protection | 1 | — | 760 | 0 | 0 | 935 | 0 | 0 | 15.62 |
| **Stable dragoon18fra protection +2 (lvl 3)** `frasta.dragoon18fra.2.2` | France | protection | 2 | — | 1260 | 0 | 0 | 1150 | 0 | 0 | 15.62 |
| **Stable dragoon18fra protection +2 (lvl 4)** `frasta.dragoon18fra.2.3` | France | protection | 2 | — | 15600 | 0 | 0 | 2350 | 0 | 0 | 15.62 |
| **Stable dragoon18fra protection +1 (lvl 5)** `frasta.dragoon18fra.2.4` | France | protection | 1 | — | 17600 | 0 | 0 | 3350 | 0 | 0 | 15.62 |
| **Stable dragoon18fra protection +2 (lvl 6)** `frasta.dragoon18fra.2.5` | France | protection | 2 | — | 19600 | 0 | 0 | 5350 | 0 | 0 | 15.62 |
| **Stable dragoon18fra protection +2 (lvl 7)** `frasta.dragoon18fra.2.6` | France | protection | 2 | — | 21760 | 0 | 0 | 9350 | 0 | 0 | 15.62 |
| **Stable dragoon18net damage +1 (lvl 2)** `netsta.dragoon18net.1.1` | Netherlands | damage | 1 | — | 2000 | 0 | 0 | 100 | 0 | 0 | 15.62 |
| **Stable dragoon18net damage +2 (lvl 3)** `netsta.dragoon18net.1.2` | Netherlands | damage | 2 | — | 9000 | 0 | 0 | 350 | 0 | 0 | 15.62 |
| **Stable dragoon18net damage +3 (lvl 4)** `netsta.dragoon18net.1.3` | Netherlands | damage | 3 | — | 12000 | 0 | 0 | 400 | 0 | 0 | 15.62 |
| **Stable dragoon18net damage +1 (lvl 5)** `netsta.dragoon18net.1.4` | Netherlands | damage | 1 | — | 23000 | 0 | 0 | 580 | 0 | 0 | 15.62 |
| **Stable dragoon18net damage +2 (lvl 6)** `netsta.dragoon18net.1.5` | Netherlands | damage | 2 | — | 32000 | 0 | 0 | 680 | 0 | 0 | 15.62 |
| **Stable dragoon18net damage +3 (lvl 7)** `netsta.dragoon18net.1.6` | Netherlands | damage | 3 | — | 42000 | 0 | 0 | 780 | 0 | 0 | 15.62 |
| **Stable dragoon18net protection +1 (lvl 2)** `netsta.dragoon18net.2.1` | Netherlands | protection | 1 | — | 760 | 0 | 0 | 935 | 0 | 0 | 15.62 |
| **Stable dragoon18net protection +2 (lvl 3)** `netsta.dragoon18net.2.2` | Netherlands | protection | 2 | — | 1260 | 0 | 0 | 1150 | 0 | 0 | 15.62 |
| **Stable dragoon18net protection +2 (lvl 4)** `netsta.dragoon18net.2.3` | Netherlands | protection | 2 | — | 15600 | 0 | 0 | 2350 | 0 | 0 | 15.62 |
| **Stable dragoon18net protection +1 (lvl 5)** `netsta.dragoon18net.2.4` | Netherlands | protection | 1 | — | 17600 | 0 | 0 | 4350 | 0 | 0 | 15.62 |
| **Stable dragoon18net protection +2 (lvl 6)** `netsta.dragoon18net.2.5` | Netherlands | protection | 2 | — | 19600 | 0 | 0 | 5350 | 0 | 0 | 15.62 |
| **Stable dragoon18net protection +2 (lvl 7)** `netsta.dragoon18net.2.6` | Netherlands | protection | 2 | — | 21760 | 0 | 0 | 8350 | 0 | 0 | 15.62 |
| **Stable dragoon18pie damage +2 (lvl 2)** `piesta.dragoon18pie.1.1` | Piedmont | damage | 2 | — | 2000 | 0 | 0 | 100 | 0 | 0 | 15.62 |
| **Stable dragoon18pie damage +2 (lvl 3)** `piesta.dragoon18pie.1.2` | Piedmont | damage | 2 | — | 9000 | 0 | 0 | 350 | 0 | 0 | 15.62 |
| **Stable dragoon18pie damage +4 (lvl 4)** `piesta.dragoon18pie.1.3` | Piedmont | damage | 4 | — | 12000 | 0 | 0 | 400 | 0 | 0 | 15.62 |
| **Stable dragoon18pie damage +2 (lvl 5)** `piesta.dragoon18pie.1.4` | Piedmont | damage | 2 | — | 23000 | 0 | 0 | 580 | 0 | 0 | 15.62 |
| **Stable dragoon18pie damage +2 (lvl 6)** `piesta.dragoon18pie.1.5` | Piedmont | damage | 2 | — | 32000 | 0 | 0 | 680 | 0 | 0 | 15.62 |
| **Stable dragoon18pie damage +4 (lvl 7)** `piesta.dragoon18pie.1.6` | Piedmont | damage | 4 | — | 42000 | 0 | 0 | 780 | 0 | 0 | 15.62 |
| **Stable dragoon18pie protection +1 (lvl 2)** `piesta.dragoon18pie.2.1` | Piedmont | protection | 1 | — | 760 | 0 | 0 | 935 | 0 | 0 | 15.62 |
| **Stable dragoon18pie protection +1 (lvl 3)** `piesta.dragoon18pie.2.2` | Piedmont | protection | 1 | — | 1260 | 0 | 0 | 1150 | 0 | 0 | 15.62 |
| **Stable dragoon18pie protection +2 (lvl 4)** `piesta.dragoon18pie.2.3` | Piedmont | protection | 2 | — | 15600 | 0 | 0 | 2350 | 0 | 0 | 15.62 |
| **Stable dragoon18pie protection +1 (lvl 5)** `piesta.dragoon18pie.2.4` | Piedmont | protection | 1 | — | 17600 | 0 | 0 | 4350 | 0 | 0 | 15.62 |
| **Stable dragoon18pie protection +1 (lvl 6)** `piesta.dragoon18pie.2.5` | Piedmont | protection | 1 | — | 19600 | 0 | 0 | 5350 | 0 | 0 | 15.62 |
| **Stable dragoon18pie protection +2 (lvl 7)** `piesta.dragoon18pie.2.6` | Piedmont | protection | 2 | — | 21760 | 0 | 0 | 8350 | 0 | 0 | 15.62 |
| **Stable dragoonpol damage +1 (lvl 2)** `polsta.dragoonpol.1.1` | Poland | damage | 1 | — | 700 | 0 | 0 | 250 | 0 | 0 | 15.62 |
| **Stable dragoonpol damage +1 (lvl 3)** `polsta.dragoonpol.1.2` | Poland | damage | 1 | — | 500 | 0 | 0 | 200 | 0 | 0 | 15.62 |
| **Stable dragoonpol damage +2 (lvl 4)** `polsta.dragoonpol.1.3` | Poland | damage | 2 | — | 700 | 0 | 0 | 240 | 0 | 0 | 15.62 |
| **Stable dragoonpol damage +1 (lvl 5)** `polsta.dragoonpol.1.4` | Poland | damage | 1 | — | 0 | 0 | 0 | 0 | 0 | 0 | 15.62 |
| **Stable dragoonpol damage +1 (lvl 6)** `polsta.dragoonpol.1.5` | Poland | damage | 1 | — | 0 | 0 | 0 | 0 | 0 | 0 | 15.62 |
| **Stable dragoonpol damage +3 (lvl 7)** `polsta.dragoonpol.1.6` | Poland | damage | 3 | — | 0 | 0 | 0 | 0 | 0 | 0 | 15.62 |
| **Stable dragoonpol protection +1 (lvl 2)** `polsta.dragoonpol.2.1` | Poland | protection | 1 | — | 900 | 0 | 0 | 250 | 0 | 0 | 15.62 |
| **Stable dragoonpol protection +1 (lvl 3)** `polsta.dragoonpol.2.2` | Poland | protection | 1 | — | 6200 | 0 | 0 | 550 | 0 | 0 | 15.62 |
| **Stable dragoonpol protection +1 (lvl 4)** `polsta.dragoonpol.2.3` | Poland | protection | 1 | — | 5400 | 0 | 0 | 1150 | 0 | 0 | 15.62 |
| **Stable dragoonpol protection +1 (lvl 5)** `polsta.dragoonpol.2.4` | Poland | protection | 1 | — | 2000 | 0 | 0 | 800 | 0 | 0 | 15.62 |
| **Stable dragoonpol protection +2 (lvl 6)** `polsta.dragoonpol.2.5` | Poland | protection | 2 | — | 3000 | 0 | 0 | 2250 | 0 | 0 | 15.62 |
| **Stable dragoonpol protection +2 (lvl 7)** `polsta.dragoonpol.2.6` | Poland | protection | 2 | — | 5001 | 0 | 0 | 6100 | 0 | 0 | 15.62 |
| **Stable guardcavalrysax damage +2 (lvl 2)** `saxsta.guardcavalrysax.1.1` | Saxony | damage | 2 | — | 10000 | 0 | 0 | 200 | 0 | 0 | 15.62 |
| **Stable guardcavalrysax damage +2 (lvl 3)** `saxsta.guardcavalrysax.1.2` | Saxony | damage | 2 | — | 34000 | 0 | 0 | 1700 | 0 | 0 | 15.62 |
| **Stable guardcavalrysax damage +3 (lvl 4)** `saxsta.guardcavalrysax.1.3` | Saxony | damage | 3 | — | 64000 | 0 | 0 | 2100 | 0 | 0 | 15.62 |
| **Stable guardcavalrysax damage +1 (lvl 5)** `saxsta.guardcavalrysax.1.4` | Saxony | damage | 1 | — | 58000 | 0 | 0 | 4150 | 0 | 0 | 15.62 |
| **Stable guardcavalrysax damage +1 (lvl 6)** `saxsta.guardcavalrysax.1.5` | Saxony | damage | 1 | — | 59055 | 0 | 0 | 3100 | 0 | 0 | 15.62 |
| **Stable guardcavalrysax damage +1 (lvl 7)** `saxsta.guardcavalrysax.1.6` | Saxony | damage | 1 | — | 47050 | 0 | 0 | 8150 | 0 | 0 | 15.62 |
| **Stable guardcavalrysax protection +2 (lvl 2)** `saxsta.guardcavalrysax.2.1` | Saxony | protection | 2 | — | 1520 | 0 | 0 | 450 | 1000 | 0 | 15.62 |
| **Stable guardcavalrysax protection +2 (lvl 3)** `saxsta.guardcavalrysax.2.2` | Saxony | protection | 2 | — | 7000 | 0 | 0 | 750 | 2000 | 0 | 15.62 |
| **Stable guardcavalrysax protection +3 (lvl 4)** `saxsta.guardcavalrysax.2.3` | Saxony | protection | 3 | — | 3600 | 0 | 0 | 3300 | 3050 | 0 | 15.62 |
| **Stable guardcavalrysax protection +3 (lvl 5)** `saxsta.guardcavalrysax.2.4` | Saxony | protection | 3 | — | 8700 | 0 | 0 | 3200 | 200 | 0 | 15.62 |
| **Stable guardcavalrysax protection +1 (lvl 6)** `saxsta.guardcavalrysax.2.5` | Saxony | protection | 1 | — | 8700 | 0 | 0 | 2650 | 4300 | 0 | 15.62 |
| **Stable guardcavalrysax protection +1 (lvl 7)** `saxsta.guardcavalrysax.2.6` | Saxony | protection | 1 | — | 11200 | 0 | 0 | 4700 | 6760 | 0 | 15.62 |
| **Stable hackapell damage +1 (lvl 2)** `swesta.hackapell.1.1` | Sweden | damage | 1 | — | 2000 | 0 | 0 | 500 | 0 | 0 | 15.62 |
| **Stable hackapell damage +2 (lvl 3)** `swesta.hackapell.1.2` | Sweden | damage | 2 | — | 5000 | 0 | 0 | 800 | 0 | 0 | 15.62 |
| **Stable hackapell damage +2 (lvl 4)** `swesta.hackapell.1.3` | Sweden | damage | 2 | — | 10000 | 0 | 0 | 1200 | 0 | 0 | 15.62 |
| **Stable hackapell damage +1 (lvl 5)** `swesta.hackapell.1.4` | Sweden | damage | 1 | — | 20000 | 0 | 0 | 1300 | 0 | 0 | 15.62 |
| **Stable hackapell damage +2 (lvl 6)** `swesta.hackapell.1.5` | Sweden | damage | 2 | — | 30000 | 0 | 0 | 3000 | 0 | 0 | 15.62 |
| **Stable hackapell damage +2 (lvl 7)** `swesta.hackapell.1.6` | Sweden | damage | 2 | — | 20000 | 0 | 0 | 5000 | 0 | 0 | 15.62 |
| **Stable hackapell protection +1 (lvl 2)** `swesta.hackapell.2.1` | Sweden | protection | 1 | — | 2000 | 0 | 0 | 1350 | 0 | 0 | 15.62 |
| **Stable hackapell protection +2 (lvl 3)** `swesta.hackapell.2.2` | Sweden | protection | 2 | — | 1500 | 0 | 0 | 2100 | 0 | 0 | 15.62 |
| **Stable hackapell protection +2 (lvl 4)** `swesta.hackapell.2.3` | Sweden | protection | 2 | — | 5000 | 0 | 0 | 2300 | 0 | 0 | 15.62 |
| **Stable hackapell protection +1 (lvl 5)** `swesta.hackapell.2.4` | Sweden | protection | 1 | — | 10500 | 0 | 0 | 3400 | 0 | 0 | 15.62 |
| **Stable hackapell protection +2 (lvl 6)** `swesta.hackapell.2.5` | Sweden | protection | 2 | — | 12600 | 0 | 0 | 4500 | 0 | 0 | 15.62 |
| **Stable hackapell protection +2 (lvl 7)** `swesta.hackapell.2.6` | Sweden | protection | 2 | — | 40000 | 0 | 0 | 5000 | 0 | 0 | 15.62 |
| **Stable hetman damage +30 (lvl 2)** `ukrsta.hetman.1.1` | Ukraine | damage | 30 | — | 7000 | 0 | 0 | 18000 | 0 | 0 | 15.62 |
| **Stable hetman protection +10 (lvl 2)** `ukrsta.hetman.2.1` | Ukraine | protection | 10 | — | 44950 | 0 | 0 | 1000 | 20000 | 0 | 15.62 |
| **Stable hussar damage +1 (lvl 2)** `aussta.hussar.1.1` | Austria, Bavaria, Netherlands, Piedmont, Poland, Portugal, Russia, Spain, Venice | damage | 1 | — | 0 | 0 | 0 | 1800 | 1000 | 0 | 15.62 |
| **Stable hussar damage +1 (lvl 2)** `swesta.hussar.1.1` | Saxony, Sweden | damage | 1 | — | 0 | 0 | 0 | 1200 | 1500 | 0 | 15.62 |
| **Stable hussar damage +1 (lvl 2)** `frasta.hussar.1.1` | France | damage | 1 | — | 0 | 0 | 0 | 800 | 200 | 0 | 15.62 |
| **Stable hussar damage +1 (lvl 2)** `engsta.hussar.1.1` | England | damage | 1 | — | 0 | 0 | 0 | 1200 | 400 | 0 | 15.62 |
| **Stable hussar damage +1 (lvl 2)** `densta.hussar.1.1` | Denmark | damage | 1 | — | 0 | 0 | 0 | 2800 | 1600 | 0 | 15.62 |
| **Stable hussar damage +2 (lvl 3)** `aussta.hussar.1.2` | Austria, Bavaria, England, Netherlands, Piedmont, Poland, Portugal, Russia, Spain, Venice | damage | 2 | — | 0 | 0 | 0 | 3800 | 2000 | 0 | 15.62 |
| **Stable hussar damage +2 (lvl 3)** `swesta.hussar.1.2` | Saxony, Sweden | damage | 2 | — | 0 | 0 | 0 | 4400 | 1500 | 0 | 15.62 |
| **Stable hussar damage +2 (lvl 3)** `frasta.hussar.1.2` | France | damage | 2 | — | 0 | 0 | 0 | 4800 | 2800 | 0 | 15.62 |
| **Stable hussar damage +2 (lvl 3)** `densta.hussar.1.2` | Denmark | damage | 2 | — | 0 | 0 | 0 | 2800 | 1400 | 0 | 15.62 |
| **Stable hussar damage +3 (lvl 4)** `aussta.hussar.1.3` | Austria, Piedmont, Poland, Russia, Spain, Venice | damage | 3 | — | 20200 | 0 | 0 | 0 | 2000 | 0 | 15.62 |
| **Stable hussar damage +3 (lvl 4)** `netsta.hussar.1.3` | Bavaria, Netherlands, Portugal | damage | 3 | — | 20200 | 0 | 0 | 0 | 3000 | 0 | 15.62 |
| **Stable hussar damage +3 (lvl 4)** `frasta.hussar.1.3` | France | damage | 3 | — | 25200 | 0 | 0 | 0 | 2500 | 0 | 15.62 |
| **Stable hussar damage +3 (lvl 4)** `engsta.hussar.1.3` | England | damage | 3 | — | 10200 | 0 | 0 | 0 | 3000 | 0 | 15.62 |
| **Stable hussar damage +3 (lvl 4)** `swesta.hussar.1.3` | Sweden | damage | 3 | — | 10200 | 0 | 0 | 0 | 1500 | 0 | 15.62 |
| **Stable hussar damage +3 (lvl 4)** `densta.hussar.1.3` | Denmark | damage | 3 | — | 10200 | 0 | 0 | 0 | 4000 | 0 | 15.62 |
| **Stable hussar damage +3 (lvl 4)** `saxsta.hussar.1.3` | Saxony | damage | 3 | — | 10200 | 0 | 0 | 0 | 2500 | 0 | 15.62 |
| **Stable hussar damage +4 (lvl 5)** `aussta.hussar.1.4` | Austria, Bavaria, Netherlands, Piedmont, Poland, Portugal, Russia, Spain, Venice | damage | 4 | — | 32000 | 0 | 0 | 0 | 3000 | 0 | 15.62 |
| **Stable hussar damage +4 (lvl 5)** `engsta.hussar.1.4` | Denmark, England | damage | 4 | — | 42000 | 0 | 0 | 0 | 2000 | 0 | 15.62 |
| **Stable hussar damage +4 (lvl 5)** `swesta.hussar.1.4` | Saxony, Sweden | damage | 4 | — | 42000 | 0 | 0 | 0 | 3500 | 0 | 15.62 |
| **Stable hussar damage +4 (lvl 5)** `frasta.hussar.1.4` | France | damage | 4 | — | 27000 | 0 | 0 | 0 | 2500 | 0 | 15.62 |
| **Stable hussar damage +1 (lvl 6)** `aussta.hussar.1.5` | Austria, Bavaria, Netherlands, Piedmont, Poland, Portugal, Russia, Spain, Venice | damage | 1 | — | 49200 | 0 | 0 | 0 | 3500 | 0 | 15.62 |
| **Stable hussar damage +1 (lvl 6)** `swesta.hussar.1.5` | Denmark, Saxony, Sweden | damage | 1 | — | 29200 | 0 | 0 | 0 | 5500 | 0 | 15.62 |
| **Stable hussar damage +1 (lvl 6)** `frasta.hussar.1.5` | France | damage | 1 | — | 46200 | 0 | 0 | 0 | 4300 | 0 | 15.62 |
| **Stable hussar damage +1 (lvl 6)** `engsta.hussar.1.5` | England | damage | 1 | — | 49200 | 0 | 0 | 0 | 6500 | 0 | 15.62 |
| **Stable hussar damage +1 (lvl 7)** `aussta.hussar.1.6` | Austria, Bavaria, Netherlands, Piedmont, Poland, Portugal, Russia, Spain, Venice | damage | 1 | — | 20000 | 0 | 0 | 0 | 6000 | 0 | 15.62 |
| **Stable hussar damage +1 (lvl 7)** `swesta.hussar.1.6` | Saxony, Sweden | damage | 1 | — | 40000 | 0 | 0 | 0 | 4400 | 0 | 15.62 |
| **Stable hussar damage +1 (lvl 7)** `frasta.hussar.1.6` | France | damage | 1 | — | 21000 | 0 | 0 | 0 | 5200 | 0 | 15.62 |
| **Stable hussar damage +1 (lvl 7)** `engsta.hussar.1.6` | England | damage | 1 | — | 14000 | 0 | 0 | 0 | 2000 | 0 | 15.62 |
| **Stable hussar damage +1 (lvl 7)** `densta.hussar.1.6` | Denmark | damage | 1 | — | 40000 | 0 | 0 | 0 | 4000 | 0 | 15.62 |
| **Stable hussar protection +1 (lvl 2)** `aussta.hussar.2.1` | Austria, Bavaria, Netherlands, Piedmont, Poland, Portugal, Russia, Spain, Venice | protection | 1 | — | 1760 | 0 | 0 | 1350 | 0 | 0 | 15.62 |
| **Stable hussar protection +1 (lvl 2)** `swesta.hussar.2.1` | Saxony, Sweden | protection | 1 | — | 500 | 0 | 0 | 350 | 0 | 0 | 15.62 |
| **Stable hussar protection +1 (lvl 2)** `frasta.hussar.2.1` | France | protection | 1 | — | 760 | 0 | 0 | 1350 | 0 | 0 | 15.62 |
| **Stable hussar protection +1 (lvl 2)** `engsta.hussar.2.1` | England | protection | 1 | — | 1550 | 0 | 0 | 1150 | 0 | 0 | 15.62 |
| **Stable hussar protection +1 (lvl 2)** `densta.hussar.2.1` | Denmark | protection | 1 | — | 150 | 0 | 0 | 1250 | 0 | 0 | 15.62 |
| **Stable hussar protection +1 (lvl 3)** `aussta.hussar.2.2` | Austria, Bavaria, Netherlands, Piedmont, Poland, Portugal, Russia, Spain, Venice | protection | 1 | — | 1900 | 0 | 0 | 2350 | 0 | 0 | 15.62 |
| **Stable hussar protection +1 (lvl 3)** `swesta.hussar.2.2` | Saxony, Sweden | protection | 1 | — | 3900 | 0 | 0 | 3350 | 0 | 0 | 15.62 |
| **Stable hussar protection +1 (lvl 3)** `frasta.hussar.2.2` | France | protection | 1 | — | 2900 | 0 | 0 | 2350 | 0 | 0 | 15.62 |
| **Stable hussar protection +1 (lvl 3)** `engsta.hussar.2.2` | England | protection | 1 | — | 2150 | 0 | 0 | 2550 | 0 | 0 | 15.62 |
| **Stable hussar protection +1 (lvl 3)** `densta.hussar.2.2` | Denmark | protection | 1 | — | 3200 | 0 | 0 | 2450 | 0 | 0 | 15.62 |
| **Stable hussar protection +1 (lvl 4)** `aussta.hussar.2.3` | Austria, Bavaria, Netherlands, Piedmont, Poland, Portugal, Russia, Spain, Venice | protection | 1 | — | 1600 | 0 | 0 | 5350 | 0 | 0 | 15.62 |
| **Stable hussar protection +1 (lvl 4)** `swesta.hussar.2.3` | Saxony, Sweden | protection | 1 | — | 1100 | 0 | 0 | 5350 | 0 | 0 | 15.62 |
| **Stable hussar protection +1 (lvl 4)** `frasta.hussar.2.3` | France | protection | 1 | — | 4600 | 0 | 0 | 5350 | 0 | 0 | 15.62 |
| **Stable hussar protection +1 (lvl 4)** `engsta.hussar.2.3` | England | protection | 1 | — | 5600 | 0 | 0 | 4350 | 0 | 0 | 15.62 |
| **Stable hussar protection +1 (lvl 4)** `densta.hussar.2.3` | Denmark | protection | 1 | — | 3600 | 0 | 0 | 3350 | 0 | 0 | 15.62 |
| **Stable hussar protection +2 (lvl 5)** `aussta.hussar.2.4` | Austria, Bavaria, Netherlands, Piedmont, Poland, Portugal, Russia, Spain, Venice | protection | 2 | — | 8000 | 0 | 0 | 8350 | 0 | 0 | 15.62 |
| **Stable hussar protection +2 (lvl 5)** `swesta.hussar.2.4` | Saxony, Sweden | protection | 2 | — | 7800 | 0 | 0 | 8350 | 0 | 0 | 15.62 |
| **Stable hussar protection +2 (lvl 5)** `frasta.hussar.2.4` | France | protection | 2 | — | 4000 | 0 | 0 | 8350 | 0 | 0 | 15.62 |
| **Stable hussar protection +2 (lvl 5)** `engsta.hussar.2.4` | England | protection | 2 | — | 4000 | 0 | 0 | 9350 | 0 | 0 | 15.62 |
| **Stable hussar protection +2 (lvl 5)** `densta.hussar.2.4` | Denmark | protection | 2 | — | 6000 | 0 | 0 | 10350 | 0 | 0 | 15.62 |
| **Stable hussar protection +2 (lvl 6)** `aussta.hussar.2.5` | Austria, Bavaria, Netherlands, Piedmont, Poland, Portugal, Russia, Spain, Venice | protection | 2 | — | 2000 | 0 | 0 | 15350 | 0 | 0 | 15.62 |
| **Stable hussar protection +2 (lvl 6)** `swesta.hussar.2.5` | Saxony, Sweden | protection | 2 | — | 1700 | 0 | 0 | 17350 | 0 | 0 | 15.62 |
| **Stable hussar protection +2 (lvl 6)** `frasta.hussar.2.5` | France | protection | 2 | — | 7000 | 0 | 0 | 15350 | 0 | 0 | 15.62 |
| **Stable hussar protection +2 (lvl 6)** `engsta.hussar.2.5` | England | protection | 2 | — | 9000 | 0 | 0 | 13200 | 0 | 0 | 15.62 |
| **Stable hussar protection +2 (lvl 6)** `densta.hussar.2.5` | Denmark | protection | 2 | — | 9000 | 0 | 0 | 13350 | 0 | 0 | 15.62 |
| **Stable hussar protection +3 (lvl 7)** `aussta.hussar.2.6` | Austria, Bavaria, Netherlands, Piedmont, Poland, Portugal, Russia, Spain, Venice | protection | 3 | — | 56000 | 0 | 0 | 20150 | 0 | 0 | 15.62 |
| **Stable hussar protection +3 (lvl 7)** `swesta.hussar.2.6` | Saxony, Sweden | protection | 3 | — | 55200 | 0 | 0 | 17150 | 0 | 0 | 15.62 |
| **Stable hussar protection +3 (lvl 7)** `frasta.hussar.2.6` | France | protection | 3 | — | 51000 | 0 | 0 | 20150 | 0 | 0 | 15.62 |
| **Stable hussar protection +2 (lvl 7)** `engsta.hussar.2.6` | England | protection | 2 | — | 52000 | 0 | 0 | 19850 | 0 | 0 | 15.62 |
| **Stable hussar protection +3 (lvl 7)** `densta.hussar.2.6` | Denmark | protection | 3 | — | 48000 | 0 | 0 | 22150 | 0 | 0 | 15.62 |
| **Stable hussarhun damage +1 (lvl 2)** `hunsta.hussarhun.1.1` | Hungary | damage | 1 | — | 2000 | 0 | 0 | 500 | 0 | 0 | 15.62 |
| **Stable hussarhun damage +2 (lvl 3)** `hunsta.hussarhun.1.2` | Hungary | damage | 2 | — | 5000 | 0 | 0 | 800 | 0 | 0 | 15.62 |
| **Stable hussarhun damage +2 (lvl 4)** `hunsta.hussarhun.1.3` | Hungary | damage | 2 | — | 10000 | 0 | 0 | 1200 | 0 | 0 | 15.62 |
| **Stable hussarhun damage +3 (lvl 5)** `hunsta.hussarhun.1.4` | Hungary | damage | 3 | — | 20000 | 0 | 0 | 1300 | 0 | 0 | 15.62 |
| **Stable hussarhun damage +4 (lvl 6)** `hunsta.hussarhun.1.5` | Hungary | damage | 4 | — | 30000 | 0 | 0 | 3000 | 0 | 0 | 15.62 |
| **Stable hussarhun damage +5 (lvl 7)** `hunsta.hussarhun.1.6` | Hungary | damage | 5 | — | 20000 | 0 | 0 | 5000 | 0 | 0 | 15.62 |
| **Stable hussarhun protection +1 (lvl 2)** `hunsta.hussarhun.2.1` | Hungary | protection | 1 | — | 2000 | 0 | 0 | 1350 | 0 | 0 | 15.62 |
| **Stable hussarhun protection +1 (lvl 3)** `hunsta.hussarhun.2.2` | Hungary | protection | 1 | — | 1500 | 0 | 0 | 2100 | 0 | 0 | 15.62 |
| **Stable hussarhun protection +1 (lvl 4)** `hunsta.hussarhun.2.3` | Hungary | protection | 1 | — | 5000 | 0 | 0 | 2300 | 0 | 0 | 15.62 |
| **Stable hussarhun protection +2 (lvl 5)** `hunsta.hussarhun.2.4` | Hungary | protection | 2 | — | 10500 | 0 | 0 | 3400 | 0 | 0 | 15.62 |
| **Stable hussarhun protection +2 (lvl 6)** `hunsta.hussarhun.2.5` | Hungary | protection | 2 | — | 12600 | 0 | 0 | 4500 | 0 | 0 | 15.62 |
| **Stable hussarhun protection +3 (lvl 7)** `hunsta.hussarhun.2.6` | Hungary | protection | 3 | — | 40000 | 0 | 0 | 5000 | 0 | 0 | 15.62 |
| **Stable hussarpru damage +1 (lvl 2)** `prusta.hussarpru.1.1` | Prussia | damage | 1 | — | 0 | 0 | 0 | 2800 | 1600 | 0 | 15.62 |
| **Stable hussarpru damage +1 (lvl 3)** `prusta.hussarpru.1.2` | Prussia | damage | 1 | — | 0 | 0 | 0 | 2800 | 1400 | 0 | 15.62 |
| **Stable hussarpru damage +2 (lvl 4)** `prusta.hussarpru.1.3` | Prussia | damage | 2 | — | 10200 | 0 | 0 | 0 | 3000 | 0 | 15.62 |
| **Stable hussarpru damage +2 (lvl 5)** `prusta.hussarpru.1.4` | Prussia | damage | 2 | — | 42000 | 0 | 0 | 0 | 2000 | 0 | 15.62 |
| **Stable hussarpru damage +3 (lvl 6)** `prusta.hussarpru.1.5` | Prussia | damage | 3 | — | 29200 | 0 | 0 | 0 | 5500 | 0 | 15.62 |
| **Stable hussarpru damage +3 (lvl 7)** `prusta.hussarpru.1.6` | Prussia | damage | 3 | — | 40000 | 0 | 0 | 0 | 4000 | 0 | 15.62 |
| **Stable hussarpru protection +1 (lvl 2)** `prusta.hussarpru.2.1` | Prussia | protection | 1 | — | 150 | 0 | 0 | 1250 | 0 | 0 | 15.62 |
| **Stable hussarpru protection +1 (lvl 3)** `prusta.hussarpru.2.2` | Prussia | protection | 1 | — | 3200 | 0 | 0 | 2450 | 0 | 0 | 15.62 |
| **Stable hussarpru protection +1 (lvl 4)** `prusta.hussarpru.2.3` | Prussia | protection | 1 | — | 3600 | 0 | 0 | 3350 | 0 | 0 | 15.62 |
| **Stable hussarpru protection +2 (lvl 5)** `prusta.hussarpru.2.4` | Prussia | protection | 2 | — | 6000 | 0 | 0 | 10350 | 0 | 0 | 15.62 |
| **Stable hussarpru protection +2 (lvl 6)** `prusta.hussarpru.2.5` | Prussia | protection | 2 | — | 9000 | 0 | 0 | 13350 | 0 | 0 | 15.62 |
| **Stable hussarpru protection +3 (lvl 7)** `prusta.hussarpru.2.6` | Prussia | protection | 3 | — | 48000 | 0 | 0 | 22150 | 0 | 0 | 15.62 |
| **Stable hussarswi damage +2 (lvl 2)** `swista.hussarswi.1.1` | Switzerland | damage | 2 | — | 0 | 0 | 0 | 2800 | 1600 | 0 | 15.62 |
| **Stable hussarswi damage +2 (lvl 3)** `swista.hussarswi.1.2` | Switzerland | damage | 2 | — | 0 | 0 | 0 | 2800 | 1400 | 0 | 15.62 |
| **Stable hussarswi damage +2 (lvl 4)** `swista.hussarswi.1.3` | Switzerland | damage | 2 | — | 10200 | 0 | 0 | 0 | 3000 | 0 | 15.62 |
| **Stable hussarswi damage +2 (lvl 5)** `swista.hussarswi.1.4` | Switzerland | damage | 2 | — | 42000 | 0 | 0 | 0 | 2000 | 0 | 15.62 |
| **Stable hussarswi damage +2 (lvl 6)** `swista.hussarswi.1.5` | Switzerland | damage | 2 | — | 29200 | 0 | 0 | 0 | 5500 | 0 | 15.62 |
| **Stable hussarswi damage +2 (lvl 7)** `swista.hussarswi.1.6` | Switzerland | damage | 2 | — | 40000 | 0 | 0 | 0 | 4000 | 0 | 15.62 |
| **Stable hussarswi protection +1 (lvl 2)** `swista.hussarswi.2.1` | Switzerland | protection | 1 | — | 150 | 0 | 0 | 1250 | 0 | 0 | 15.62 |
| **Stable hussarswi protection +2 (lvl 3)** `swista.hussarswi.2.2` | Switzerland | protection | 2 | — | 3200 | 0 | 0 | 2450 | 0 | 0 | 15.62 |
| **Stable hussarswi protection +2 (lvl 4)** `swista.hussarswi.2.3` | Switzerland | protection | 2 | — | 3600 | 0 | 0 | 3350 | 0 | 0 | 15.62 |
| **Stable hussarswi protection +1 (lvl 5)** `swista.hussarswi.2.4` | Switzerland | protection | 1 | — | 6000 | 0 | 0 | 10350 | 0 | 0 | 15.62 |
| **Stable hussarswi protection +2 (lvl 6)** `swista.hussarswi.2.5` | Switzerland | protection | 2 | — | 9000 | 0 | 0 | 13350 | 0 | 0 | 15.62 |
| **Stable hussarswi protection +2 (lvl 7)** `swista.hussarswi.2.6` | Switzerland | protection | 2 | — | 48000 | 0 | 0 | 22150 | 0 | 0 | 15.62 |
| **Stable kingmusketeer damage +20 (lvl 2)** `frasta.kingmusketeer.1.1` | France | damage | 20 | — | 7000 | 0 | 0 | 2500 | 0 | 0 | 15.62 |
| **Stable kingmusketeer protection +12 (lvl 2)** `frasta.kingmusketeer.2.1` | France | protection | 12 | — | 2000 | 0 | 0 | 1350 | 0 | 0 | 15.62 |
| **Stable kingmusketeer protection +1 (lvl 3)** `frasta.kingmusketeer.2.2` | France | protection | 1 | — | 0 | 0 | 0 | 0 | 0 | 0 | 15.62 |
| **Stable kingmusketeer protection +2 (lvl 4)** `frasta.kingmusketeer.2.3` | France | protection | 2 | — | 0 | 0 | 0 | 0 | 0 | 0 | 15.62 |
| **Stable kingmusketeer protection +2 (lvl 5)** `frasta.kingmusketeer.2.4` | France | protection | 2 | — | 0 | 0 | 0 | 0 | 0 | 0 | 15.62 |
| **Stable kingmusketeer protection +2 (lvl 6)** `frasta.kingmusketeer.2.5` | France | protection | 2 | — | 0 | 0 | 0 | 0 | 0 | 0 | 15.62 |
| **Stable kingmusketeer protection +2 (lvl 7)** `frasta.kingmusketeer.2.6` | France | protection | 2 | — | 0 | 0 | 0 | 0 | 0 | 0 | 15.62 |
| **Stable lancersco damage +1 (lvl 2)** `scosta.lancersco.1.1` | Scotland | damage | 1 | — | 1000 | 0 | 0 | 3000 | 0 | 0 | 15.62 |
| **Stable lancersco damage +1 (lvl 3)** `scosta.lancersco.1.2` | Scotland | damage | 1 | — | 2000 | 0 | 0 | 2000 | 0 | 0 | 15.62 |
| **Stable lancersco damage +2 (lvl 4)** `scosta.lancersco.1.3` | Scotland | damage | 2 | — | 7100 | 0 | 0 | 8000 | 0 | 0 | 15.62 |
| **Stable lancersco damage +1 (lvl 5)** `scosta.lancersco.1.4` | Scotland | damage | 1 | — | 2250 | 0 | 0 | 2000 | 0 | 0 | 15.62 |
| **Stable lancersco damage +2 (lvl 6)** `scosta.lancersco.1.5` | Scotland | damage | 2 | — | 3030 | 0 | 0 | 5000 | 0 | 0 | 15.62 |
| **Stable lancersco damage +3 (lvl 7)** `scosta.lancersco.1.6` | Scotland | damage | 3 | — | 7000 | 0 | 0 | 18000 | 0 | 0 | 15.62 |
| **Stable lancersco protection +1 (lvl 2)** `scosta.lancersco.2.1` | Scotland | protection | 1 | — | 4000 | 0 | 0 | 1350 | 0 | 0 | 15.62 |
| **Stable lancersco protection +1 (lvl 3)** `scosta.lancersco.2.2` | Scotland | protection | 1 | — | 3500 | 0 | 0 | 2100 | 0 | 0 | 15.62 |
| **Stable lancersco protection +2 (lvl 4)** `scosta.lancersco.2.3` | Scotland | protection | 2 | — | 8000 | 0 | 0 | 3300 | 0 | 0 | 15.62 |
| **Stable lancersco protection +3 (lvl 5)** `scosta.lancersco.2.4` | Scotland | protection | 3 | — | 14500 | 0 | 0 | 4400 | 0 | 0 | 15.62 |
| **Stable lancersco protection +3 (lvl 6)** `scosta.lancersco.2.5` | Scotland | protection | 3 | — | 22600 | 0 | 0 | 5500 | 0 | 0 | 15.62 |
| **Stable lancersco protection +2 (lvl 7)** `scosta.lancersco.2.6` | Scotland | protection | 2 | — | 30000 | 0 | 0 | 6000 | 0 | 0 | 15.62 |
| **Stable lightcavalry damage +1 (lvl 2)** `hunsta.lightcavalry.1.1` | Hungary | damage | 1 | — | 4500 | 0 | 0 | 200 | 0 | 0 | 15.62 |
| **Stable lightcavalry damage +2 (lvl 3)** `hunsta.lightcavalry.1.2` | Hungary | damage | 2 | — | 5500 | 0 | 0 | 250 | 0 | 0 | 15.62 |
| **Stable lightcavalry damage +3 (lvl 4)** `hunsta.lightcavalry.1.3` | Hungary | damage | 3 | — | 22000 | 0 | 0 | 500 | 0 | 0 | 15.62 |
| **Stable lightcavalry damage +1 (lvl 5)** `hunsta.lightcavalry.1.4` | Hungary | damage | 1 | — | 13000 | 0 | 0 | 480 | 0 | 0 | 15.62 |
| **Stable lightcavalry damage +1 (lvl 6)** `hunsta.lightcavalry.1.5` | Hungary | damage | 1 | — | 42000 | 0 | 0 | 780 | 0 | 0 | 15.62 |
| **Stable lightcavalry damage +2 (lvl 7)** `hunsta.lightcavalry.1.6` | Hungary | damage | 2 | — | 32000 | 0 | 0 | 680 | 0 | 0 | 15.62 |
| **Stable lightcavalry protection +1 (lvl 2)** `hunsta.lightcavalry.2.1` | Hungary | protection | 1 | — | 750 | 0 | 0 | 935 | 0 | 0 | 15.62 |
| **Stable lightcavalry protection +1 (lvl 3)** `hunsta.lightcavalry.2.2` | Hungary | protection | 1 | — | 1260 | 0 | 0 | 1150 | 0 | 0 | 15.62 |
| **Stable lightcavalry protection +2 (lvl 4)** `hunsta.lightcavalry.2.3` | Hungary | protection | 2 | — | 10600 | 0 | 0 | 2350 | 0 | 0 | 15.62 |
| **Stable lightcavalry protection +1 (lvl 5)** `hunsta.lightcavalry.2.4` | Hungary | protection | 1 | — | 22600 | 0 | 0 | 5350 | 0 | 0 | 15.62 |
| **Stable lightcavalry protection +1 (lvl 6)** `hunsta.lightcavalry.2.5` | Hungary | protection | 1 | — | 19600 | 0 | 0 | 3350 | 0 | 0 | 15.62 |
| **Stable lightcavalry protection +2 (lvl 7)** `hunsta.lightcavalry.2.6` | Hungary | protection | 2 | — | 15760 | 0 | 0 | 9350 | 0 | 0 | 15.62 |
| **Stable mameluke damage +1 (lvl 2)** `algsta.mameluke.1.1` | Algeria | damage | 1 | — | 1000 | 0 | 0 | 500 | 0 | 0 | 15.62 |
| **Stable mameluke damage +1 (lvl 3)** `algsta.mameluke.1.2` | Algeria | damage | 1 | — | 2000 | 0 | 0 | 2000 | 0 | 0 | 15.62 |
| **Stable mameluke damage +1 (lvl 4)** `algsta.mameluke.1.3` | Algeria | damage | 1 | — | 7100 | 0 | 0 | 3500 | 0 | 0 | 15.62 |
| **Stable mameluke damage +1 (lvl 5)** `algsta.mameluke.1.4` | Algeria | damage | 1 | — | 2250 | 0 | 0 | 5000 | 0 | 0 | 15.62 |
| **Stable mameluke damage +1 (lvl 6)** `algsta.mameluke.1.5` | Algeria | damage | 1 | — | 3030 | 0 | 0 | 6500 | 0 | 0 | 15.62 |
| **Stable mameluke damage +2 (lvl 7)** `algsta.mameluke.1.6` | Algeria | damage | 2 | — | 7000 | 0 | 0 | 8000 | 0 | 0 | 15.62 |
| **Stable mameluke protection +1 (lvl 2)** `algsta.mameluke.2.1` | Algeria | protection | 1 | — | 200 | 0 | 0 | 135 | 1000 | 0 | 15.62 |
| **Stable mameluke protection +2 (lvl 3)** `algsta.mameluke.2.2` | Algeria | protection | 2 | — | 2000 | 0 | 0 | 100 | 1000 | 0 | 15.62 |
| **Stable mameluke protection +3 (lvl 4)** `algsta.mameluke.2.3` | Algeria | protection | 3 | — | 40000 | 0 | 0 | 200 | 4000 | 0 | 15.62 |
| **Stable mameluke protection +3 (lvl 5)** `algsta.mameluke.2.4` | Algeria | protection | 3 | — | 40000 | 0 | 0 | 300 | 6000 | 0 | 15.62 |
| **Stable mameluke protection +2 (lvl 6)** `algsta.mameluke.2.5` | Algeria | protection | 2 | — | 40000 | 0 | 0 | 350 | 8000 | 0 | 15.62 |
| **Stable mameluke protection +1 (lvl 7)** `algsta.mameluke.2.6` | Algeria | protection | 1 | — | 40000 | 0 | 0 | 1000 | 10000 | 0 | 15.62 |
| **Stable raidersco damage +1 (lvl 2)** `scosta.raidersco.1.1` | Scotland | damage | 1 | — | 2000 | 0 | 0 | 500 | 0 | 0 | 15.62 |
| **Stable raidersco damage +2 (lvl 3)** `scosta.raidersco.1.2` | Scotland | damage | 2 | — | 5000 | 0 | 0 | 800 | 0 | 0 | 15.62 |
| **Stable raidersco damage +2 (lvl 4)** `scosta.raidersco.1.3` | Scotland | damage | 2 | — | 10000 | 0 | 0 | 1200 | 0 | 0 | 15.62 |
| **Stable raidersco damage +3 (lvl 5)** `scosta.raidersco.1.4` | Scotland | damage | 3 | — | 2000 | 0 | 0 | 6000 | 0 | 0 | 15.62 |
| **Stable raidersco damage +3 (lvl 6)** `scosta.raidersco.1.5` | Scotland | damage | 3 | — | 8100 | 0 | 0 | 1000 | 0 | 0 | 15.62 |
| **Stable raidersco damage +1 (lvl 7)** `scosta.raidersco.1.6` | Scotland | damage | 1 | — | 20000 | 0 | 0 | 3000 | 0 | 0 | 15.62 |
| **Stable raidersco protection +1 (lvl 2)** `scosta.raidersco.2.1` | Scotland | protection | 1 | — | 500 | 0 | 0 | 50 | 0 | 0 | 15.62 |
| **Stable raidersco protection +2 (lvl 3)** `scosta.raidersco.2.2` | Scotland | protection | 2 | — | 1500 | 0 | 0 | 150 | 0 | 0 | 15.62 |
| **Stable raidersco protection +2 (lvl 4)** `scosta.raidersco.2.3` | Scotland | protection | 2 | — | 5625 | 0 | 0 | 560 | 0 | 0 | 15.62 |
| **Stable raidersco protection +2 (lvl 5)** `scosta.raidersco.2.4` | Scotland | protection | 2 | — | 16200 | 0 | 0 | 1080 | 0 | 0 | 15.62 |
| **Stable raidersco protection +2 (lvl 6)** `scosta.raidersco.2.5` | Scotland | protection | 2 | — | 16200 | 0 | 0 | 1080 | 0 | 0 | 15.62 |
| **Stable raidersco protection +1 (lvl 7)** `scosta.raidersco.2.6` | Scotland | protection | 1 | — | 15000 | 0 | 0 | 750 | 0 | 0 | 15.62 |
| **Stable reiter damage +1 (lvl 2)** `aussta.reiter.1.1` | Austria, Bavaria, Hungary, Netherlands, Piedmont, Portugal, Saxony, Spain, Switzerland, Venice | damage | 1 | — | 500 | 0 | 0 | 100 | 0 | 0 | 15.62 |
| **Stable reiter damage +1 (lvl 2)** `prusta.reiter.1.1` | Denmark, Prussia | damage | 1 | — | 800 | 0 | 0 | 100 | 0 | 0 | 15.62 |
| **Stable reiter damage +1 (lvl 2)** `frasta.reiter.1.1` | France | damage | 1 | — | 900 | 0 | 0 | 100 | 0 | 0 | 15.62 |
| **Stable reiter damage +1 (lvl 2)** `engsta.reiter.1.1` | England | damage | 1 | — | 400 | 0 | 0 | 50 | 0 | 0 | 15.62 |
| **Stable reiter damage +2 (lvl 3)** `aussta.reiter.1.2` | Austria, Hungary, Netherlands, Piedmont, Saxony, Spain, Switzerland, Venice | damage | 2 | — | 900 | 0 | 0 | 220 | 0 | 0 | 15.62 |
| **Stable reiter damage +2 (lvl 3)** `prusta.reiter.1.2` | Bavaria, Denmark, Portugal, Prussia | damage | 2 | — | 800 | 0 | 0 | 220 | 0 | 0 | 15.62 |
| **Stable reiter damage +2 (lvl 3)** `frasta.reiter.1.2` | France | damage | 2 | — | 500 | 0 | 0 | 280 | 0 | 0 | 15.62 |
| **Stable reiter damage +2 (lvl 3)** `engsta.reiter.1.2` | England | damage | 2 | — | 1000 | 0 | 0 | 270 | 0 | 0 | 15.62 |
| **Stable reiter damage +1 (lvl 4)** `aussta.reiter.1.3` | Austria, Hungary, Piedmont, Saxony, Spain, Switzerland, Venice | damage | 1 | — | 4400 | 0 | 0 | 280 | 0 | 0 | 15.62 |
| **Stable reiter damage +1 (lvl 4)** `prusta.reiter.1.3` | Bavaria, Denmark, Portugal, Prussia | damage | 1 | — | 2400 | 0 | 0 | 380 | 0 | 0 | 15.62 |
| **Stable reiter damage +1 (lvl 4)** `frasta.reiter.1.3` | France | damage | 1 | — | 4400 | 0 | 0 | 220 | 0 | 0 | 15.62 |
| **Stable reiter damage +1 (lvl 4)** `engsta.reiter.1.3` | England | damage | 1 | — | 4400 | 0 | 0 | 180 | 0 | 0 | 15.62 |
| **Stable reiter damage +1 (lvl 4)** `netsta.reiter.1.3` | Netherlands | damage | 1 | — | 4600 | 0 | 0 | 280 | 0 | 0 | 15.62 |
| **Stable reiter damage +1 (lvl 5)** `aussta.reiter.1.4` | Austria, Hungary, Piedmont, Saxony, Spain, Switzerland, Venice | damage | 1 | — | 2250 | 0 | 0 | 320 | 0 | 0 | 15.62 |
| **Stable reiter damage +1 (lvl 5)** `prusta.reiter.1.4` | Bavaria, Denmark, Portugal, Prussia | damage | 1 | — | 4250 | 0 | 0 | 220 | 0 | 0 | 15.62 |
| **Stable reiter damage +1 (lvl 5)** `frasta.reiter.1.4` | France | damage | 1 | — | 3050 | 0 | 0 | 320 | 0 | 0 | 15.62 |
| **Stable reiter damage +1 (lvl 5)** `engsta.reiter.1.4` | England | damage | 1 | — | 2750 | 0 | 0 | 420 | 0 | 0 | 15.62 |
| **Stable reiter damage +1 (lvl 5)** `netsta.reiter.1.4` | Netherlands | damage | 1 | — | 2050 | 0 | 0 | 220 | 0 | 0 | 15.62 |
| **Stable reiter damage +1 (lvl 6)** `aussta.reiter.1.5` | Austria, Hungary, Piedmont, Saxony, Spain, Switzerland, Venice | damage | 1 | — | 3030 | 0 | 0 | 600 | 0 | 0 | 15.62 |
| **Stable reiter damage +1 (lvl 6)** `prusta.reiter.1.5` | Bavaria, Denmark, Portugal, Prussia | damage | 1 | — | 4030 | 0 | 0 | 900 | 0 | 0 | 15.62 |
| **Stable reiter damage +1 (lvl 6)** `frasta.reiter.1.5` | France | damage | 1 | — | 2030 | 0 | 0 | 800 | 0 | 0 | 15.62 |
| **Stable reiter damage +1 (lvl 6)** `engsta.reiter.1.5` | England | damage | 1 | — | 2530 | 0 | 0 | 600 | 0 | 0 | 15.62 |
| **Stable reiter damage +1 (lvl 6)** `netsta.reiter.1.5` | Netherlands | damage | 1 | — | 3530 | 0 | 0 | 500 | 0 | 0 | 15.62 |
| **Stable reiter damage +1 (lvl 7)** `spasta.reiter.1.6` | Hungary, Piedmont, Saxony, Spain, Switzerland, Venice | damage | 1 | — | 7000 | 0 | 0 | 1800 | 0 | 0 | 15.62 |
| **Stable reiter damage +1 (lvl 7)** `prusta.reiter.1.6` | Bavaria, Denmark, Portugal, Prussia | damage | 1 | — | 6000 | 0 | 0 | 1600 | 0 | 0 | 15.62 |
| **Stable reiter damage +1 (lvl 7)** `aussta.reiter.1.6` | Austria | damage | 1 | — | 7500 | 0 | 0 | 1800 | 0 | 0 | 15.62 |
| **Stable reiter damage +1 (lvl 7)** `frasta.reiter.1.6` | France | damage | 1 | — | 7000 | 0 | 0 | 1600 | 0 | 0 | 15.62 |
| **Stable reiter damage +1 (lvl 7)** `engsta.reiter.1.6` | England | damage | 1 | — | 7500 | 0 | 0 | 1700 | 0 | 0 | 15.62 |
| **Stable reiter damage +1 (lvl 7)** `netsta.reiter.1.6` | Netherlands | damage | 1 | — | 6500 | 0 | 0 | 1900 | 0 | 0 | 15.62 |
| **Stable reiter protection +2 (lvl 2)** `aussta.reiter.2.1` | Austria, Hungary, Piedmont, Saxony, Spain, Switzerland, Venice | protection | 2 | — | 200 | 0 | 0 | 135 | 300 | 0 | 15.62 |
| **Stable reiter protection +2 (lvl 2)** `prusta.reiter.2.1` | Bavaria, Denmark, Portugal, Prussia | protection | 2 | — | 200 | 0 | 0 | 135 | 400 | 0 | 15.62 |
| **Stable reiter protection +2 (lvl 2)** `frasta.reiter.2.1` | France | protection | 2 | — | 600 | 0 | 0 | 135 | 400 | 0 | 15.62 |
| **Stable reiter protection +2 (lvl 2)** `engsta.reiter.2.1` | England | protection | 2 | — | 500 | 0 | 0 | 35 | 200 | 0 | 15.62 |
| **Stable reiter protection +2 (lvl 2)** `netsta.reiter.2.1` | Netherlands | protection | 2 | — | 250 | 0 | 0 | 55 | 300 | 0 | 15.62 |
| **Stable reiter protection +3 (lvl 3)** `aussta.reiter.2.2` | Austria, Hungary, Piedmont, Saxony, Spain, Switzerland, Venice | protection | 3 | — | 600 | 0 | 0 | 100 | 400 | 0 | 15.62 |
| **Stable reiter protection +3 (lvl 3)** `prusta.reiter.2.2` | Bavaria, Denmark, Portugal, Prussia | protection | 3 | — | 600 | 0 | 0 | 100 | 300 | 0 | 15.62 |
| **Stable reiter protection +3 (lvl 3)** `frasta.reiter.2.2` | France | protection | 3 | — | 200 | 0 | 0 | 200 | 300 | 0 | 15.62 |
| **Stable reiter protection +3 (lvl 3)** `engsta.reiter.2.2` | England | protection | 3 | — | 300 | 0 | 0 | 200 | 500 | 0 | 15.62 |
| **Stable reiter protection +3 (lvl 3)** `netsta.reiter.2.2` | Netherlands | protection | 3 | — | 550 | 0 | 0 | 200 | 400 | 0 | 15.62 |
| **Stable reiter protection +3 (lvl 4)** `aussta.reiter.2.3` | Austria, Bavaria, Denmark, Hungary, Piedmont, Portugal, Prussia, Saxony, Spain, Switzerland, Venice | protection | 3 | — | 800 | 0 | 0 | 200 | 560 | 0 | 15.62 |
| **Stable reiter protection +3 (lvl 4)** `frasta.reiter.2.3` | France | protection | 3 | — | 800 | 0 | 0 | 100 | 560 | 0 | 15.62 |
| **Stable reiter protection +3 (lvl 4)** `engsta.reiter.2.3` | England | protection | 3 | — | 950 | 0 | 0 | 200 | 620 | 0 | 15.62 |
| **Stable reiter protection +3 (lvl 4)** `netsta.reiter.2.3` | Netherlands | protection | 3 | — | 600 | 0 | 0 | 100 | 560 | 0 | 15.62 |
| **Stable reiter protection +2 (lvl 5)** `aussta.reiter.2.4` | Austria, Hungary, Piedmont, Saxony, Spain, Switzerland, Venice | protection | 2 | — | 1600 | 0 | 0 | 300 | 640 | 0 | 15.62 |
| **Stable reiter protection +2 (lvl 5)** `prusta.reiter.2.4` | Bavaria, Denmark, Portugal, Prussia | protection | 2 | — | 1600 | 0 | 0 | 300 | 340 | 0 | 15.62 |
| **Stable reiter protection +2 (lvl 5)** `frasta.reiter.2.4` | France | protection | 2 | — | 3200 | 0 | 0 | 300 | 300 | 0 | 15.62 |
| **Stable reiter protection +2 (lvl 5)** `engsta.reiter.2.4` | England | protection | 2 | — | 1450 | 0 | 0 | 300 | 540 | 0 | 15.62 |
| **Stable reiter protection +2 (lvl 5)** `netsta.reiter.2.4` | Netherlands | protection | 2 | — | 1800 | 0 | 0 | 500 | 640 | 0 | 15.62 |
| **Stable reiter protection +1 (lvl 6)** `aussta.reiter.2.5` | Austria, Hungary, Piedmont, Saxony, Spain, Switzerland, Venice | protection | 1 | — | 3200 | 0 | 0 | 350 | 300 | 0 | 15.62 |
| **Stable reiter protection +1 (lvl 6)** `prusta.reiter.2.5` | Bavaria, Denmark, Portugal, Prussia | protection | 1 | — | 2200 | 0 | 0 | 350 | 600 | 0 | 15.62 |
| **Stable reiter protection +1 (lvl 6)** `frasta.reiter.2.5` | France | protection | 1 | — | 1600 | 0 | 0 | 350 | 650 | 0 | 15.62 |
| **Stable reiter protection +1 (lvl 6)** `engsta.reiter.2.5` | England | protection | 1 | — | 6200 | 0 | 0 | 550 | 600 | 0 | 15.62 |
| **Stable reiter protection +1 (lvl 6)** `netsta.reiter.2.5` | Netherlands | protection | 1 | — | 5200 | 0 | 0 | 250 | 300 | 0 | 15.62 |
| **Stable reiter protection +1 (lvl 7)** `aussta.reiter.2.6` | Austria, Hungary, Piedmont, Saxony, Spain, Switzerland, Venice | protection | 1 | — | 16000 | 0 | 0 | 1000 | 5000 | 0 | 15.62 |
| **Stable reiter protection +1 (lvl 7)** `prusta.reiter.2.6` | Bavaria, Denmark, Portugal, Prussia | protection | 1 | — | 17000 | 0 | 0 | 950 | 5200 | 0 | 15.62 |
| **Stable reiter protection +1 (lvl 7)** `frasta.reiter.2.6` | France | protection | 1 | — | 15700 | 0 | 0 | 1000 | 5000 | 0 | 15.62 |
| **Stable reiter protection +1 (lvl 7)** `engsta.reiter.2.6` | England | protection | 1 | — | 12000 | 0 | 0 | 720 | 3730 | 0 | 15.62 |
| **Stable reiter protection +1 (lvl 7)** `netsta.reiter.2.6` | Netherlands | protection | 1 | — | 14000 | 0 | 0 | 990 | 5000 | 0 | 15.62 |
| **Stable reiterpol damage +1 (lvl 2)** `polsta.reiterpol.1.1` | Poland | damage | 1 | — | 2000 | 0 | 0 | 500 | 0 | 0 | 15.62 |
| **Stable reiterpol damage +1 (lvl 3)** `polsta.reiterpol.1.2` | Poland | damage | 1 | — | 5000 | 0 | 0 | 800 | 0 | 0 | 15.62 |
| **Stable reiterpol damage +1 (lvl 4)** `polsta.reiterpol.1.3` | Poland | damage | 1 | — | 10000 | 0 | 0 | 800 | 0 | 0 | 15.62 |
| **Stable reiterpol damage +2 (lvl 5)** `polsta.reiterpol.1.4` | Poland | damage | 2 | — | 20000 | 0 | 0 | 950 | 0 | 0 | 15.62 |
| **Stable reiterpol damage +2 (lvl 6)** `polsta.reiterpol.1.5` | Poland | damage | 2 | — | 30000 | 0 | 0 | 300 | 0 | 0 | 15.62 |
| **Stable reiterpol damage +3 (lvl 7)** `polsta.reiterpol.1.6` | Poland | damage | 3 | — | 20000 | 0 | 0 | 1500 | 0 | 0 | 15.62 |
| **Stable reiterpol protection +1 (lvl 2)** `polsta.reiterpol.2.1` | Poland | protection | 1 | — | 2000 | 0 | 0 | 900 | 0 | 0 | 15.62 |
| **Stable reiterpol protection +1 (lvl 3)** `polsta.reiterpol.2.2` | Poland | protection | 1 | — | 1500 | 0 | 0 | 850 | 0 | 0 | 15.62 |
| **Stable reiterpol protection +1 (lvl 4)** `polsta.reiterpol.2.3` | Poland | protection | 1 | — | 5000 | 0 | 0 | 950 | 0 | 0 | 15.62 |
| **Stable reiterpol protection +2 (lvl 5)** `polsta.reiterpol.2.4` | Poland | protection | 2 | — | 10500 | 0 | 0 | 400 | 0 | 0 | 15.62 |
| **Stable reiterpol protection +2 (lvl 6)** `polsta.reiterpol.2.5` | Poland | protection | 2 | — | 12600 | 0 | 0 | 1500 | 0 | 0 | 15.62 |
| **Stable reiterpol protection +3 (lvl 7)** `polsta.reiterpol.2.6` | Poland | protection | 3 | — | 40000 | 0 | 0 | 9000 | 0 | 0 | 15.62 |
| **Stable reiterswe damage +1 (lvl 2)** `swesta.reiterswe.1.1` | Sweden | damage | 1 | — | 500 | 0 | 0 | 100 | 0 | 0 | 15.62 |
| **Stable reiterswe damage +2 (lvl 3)** `swesta.reiterswe.1.2` | Sweden | damage | 2 | — | 900 | 0 | 0 | 220 | 0 | 0 | 15.62 |
| **Stable reiterswe damage +1 (lvl 4)** `swesta.reiterswe.1.3` | Sweden | damage | 1 | — | 4400 | 0 | 0 | 280 | 0 | 0 | 15.62 |
| **Stable reiterswe damage +1 (lvl 5)** `swesta.reiterswe.1.4` | Sweden | damage | 1 | — | 2250 | 0 | 0 | 320 | 0 | 0 | 15.62 |
| **Stable reiterswe damage +1 (lvl 6)** `swesta.reiterswe.1.5` | Sweden | damage | 1 | — | 3030 | 0 | 0 | 600 | 0 | 0 | 15.62 |
| **Stable reiterswe damage +1 (lvl 7)** `swesta.reiterswe.1.6` | Sweden | damage | 1 | — | 7000 | 0 | 0 | 1800 | 0 | 0 | 15.62 |
| **Stable reiterswe protection +1 (lvl 2)** `swesta.reiterswe.2.1` | Sweden | protection | 1 | — | 200 | 0 | 0 | 135 | 300 | 0 | 15.62 |
| **Stable reiterswe protection +1 (lvl 3)** `swesta.reiterswe.2.2` | Sweden | protection | 1 | — | 600 | 0 | 0 | 100 | 400 | 0 | 15.62 |
| **Stable reiterswe protection +2 (lvl 4)** `swesta.reiterswe.2.3` | Sweden | protection | 2 | — | 800 | 0 | 0 | 200 | 560 | 0 | 15.62 |
| **Stable reiterswe protection +2 (lvl 5)** `swesta.reiterswe.2.4` | Sweden | protection | 2 | — | 1600 | 0 | 0 | 300 | 640 | 0 | 15.62 |
| **Stable reiterswe protection +3 (lvl 6)** `swesta.reiterswe.2.5` | Sweden | protection | 3 | — | 3200 | 0 | 0 | 350 | 300 | 0 | 15.62 |
| **Stable reiterswe protection +2 (lvl 7)** `swesta.reiterswe.2.6` | Sweden | protection | 2 | — | 16000 | 0 | 0 | 1000 | 5000 | 0 | 15.62 |
| **Stable sipahi damage +1 (lvl 2)** `tursta.sipahi.1.1` | Turkey | damage | 1 | — | 500 | 0 | 0 | 100 | 0 | 0 | 15.62 |
| **Stable sipahi damage +2 (lvl 3)** `tursta.sipahi.1.2` | Turkey | damage | 2 | — | 900 | 0 | 0 | 220 | 0 | 0 | 15.62 |
| **Stable sipahi damage +1 (lvl 4)** `tursta.sipahi.1.3` | Turkey | damage | 1 | — | 4400 | 0 | 0 | 280 | 0 | 0 | 15.62 |
| **Stable sipahi damage +1 (lvl 5)** `tursta.sipahi.1.4` | Turkey | damage | 1 | — | 2250 | 0 | 0 | 320 | 0 | 0 | 15.62 |
| **Stable sipahi damage +1 (lvl 6)** `tursta.sipahi.1.5` | Turkey | damage | 1 | — | 3030 | 0 | 0 | 600 | 0 | 0 | 15.62 |
| **Stable sipahi damage +1 (lvl 7)** `tursta.sipahi.1.6` | Turkey | damage | 1 | — | 7000 | 0 | 0 | 1800 | 0 | 0 | 15.62 |
| **Stable sipahi protection +1 (lvl 2)** `tursta.sipahi.2.1` | Turkey | protection | 1 | — | 200 | 0 | 0 | 135 | 300 | 0 | 15.62 |
| **Stable sipahi protection +2 (lvl 3)** `tursta.sipahi.2.2` | Turkey | protection | 2 | — | 600 | 0 | 0 | 100 | 400 | 0 | 15.62 |
| **Stable sipahi protection +2 (lvl 4)** `tursta.sipahi.2.3` | Turkey | protection | 2 | — | 800 | 0 | 0 | 200 | 560 | 0 | 15.62 |
| **Stable sipahi protection +2 (lvl 5)** `tursta.sipahi.2.4` | Turkey | protection | 2 | — | 1600 | 0 | 0 | 300 | 640 | 0 | 15.62 |
| **Stable sipahi protection +2 (lvl 6)** `tursta.sipahi.2.5` | Turkey | protection | 2 | — | 3200 | 0 | 0 | 350 | 300 | 0 | 15.62 |
| **Stable sipahi protection +3 (lvl 7)** `tursta.sipahi.2.6` | Turkey | protection | 3 | — | 16000 | 0 | 0 | 1000 | 5000 | 0 | 15.62 |
| **Stable spakh damage +1 (lvl 2)** `tursta.spakh.1.1` | Turkey | damage | 1 | — | 1000 | 0 | 0 | 500 | 0 | 0 | 15.62 |
| **Stable spakh damage +1 (lvl 3)** `tursta.spakh.1.2` | Turkey | damage | 1 | — | 2000 | 0 | 0 | 2000 | 0 | 0 | 15.62 |
| **Stable spakh damage +2 (lvl 4)** `tursta.spakh.1.3` | Turkey | damage | 2 | — | 7100 | 0 | 0 | 3500 | 0 | 0 | 15.62 |
| **Stable spakh damage +1 (lvl 5)** `tursta.spakh.1.4` | Turkey | damage | 1 | — | 2250 | 0 | 0 | 5000 | 0 | 0 | 15.62 |
| **Stable spakh damage +1 (lvl 6)** `tursta.spakh.1.5` | Turkey | damage | 1 | — | 3030 | 0 | 0 | 6500 | 0 | 0 | 15.62 |
| **Stable spakh damage +1 (lvl 7)** `tursta.spakh.1.6` | Turkey | damage | 1 | — | 7000 | 0 | 0 | 8000 | 0 | 0 | 15.62 |
| **Stable spakh protection +1 (lvl 2)** `tursta.spakh.2.1` | Turkey | protection | 1 | — | 200 | 0 | 0 | 135 | 1000 | 0 | 15.62 |
| **Stable spakh protection +1 (lvl 3)** `tursta.spakh.2.2` | Turkey | protection | 1 | — | 2000 | 0 | 0 | 100 | 1000 | 0 | 15.62 |
| **Stable spakh protection +2 (lvl 4)** `tursta.spakh.2.3` | Turkey | protection | 2 | — | 40000 | 0 | 0 | 200 | 4000 | 0 | 15.62 |
| **Stable spakh protection +3 (lvl 5)** `tursta.spakh.2.4` | Turkey | protection | 3 | — | 40000 | 0 | 0 | 300 | 6000 | 0 | 15.62 |
| **Stable spakh protection +2 (lvl 6)** `tursta.spakh.2.5` | Turkey | protection | 2 | — | 40000 | 0 | 0 | 350 | 8000 | 0 | 15.62 |
| **Stable spakh protection +1 (lvl 7)** `tursta.spakh.2.6` | Turkey | protection | 1 | — | 40000 | 0 | 0 | 1000 | 10000 | 0 | 15.62 |
| **Stable tatar damage +2 (lvl 2)** `tursta.tatar.1.1` | Turkey | damage | 2 | — | 700 | 0 | 0 | 250 | 0 | 0 | 15.62 |
| **Stable tatar damage +2 (lvl 3)** `tursta.tatar.1.2` | Turkey | damage | 2 | — | 500 | 0 | 0 | 200 | 0 | 0 | 15.62 |
| **Stable tatar damage +2 (lvl 4)** `tursta.tatar.1.3` | Turkey | damage | 2 | — | 700 | 0 | 0 | 240 | 0 | 0 | 15.62 |
| **Stable tatar damage +3 (lvl 5)** `tursta.tatar.1.4` | Turkey | damage | 3 | — | 1200 | 0 | 0 | 900 | 0 | 0 | 15.62 |
| **Stable tatar damage +3 (lvl 6)** `tursta.tatar.1.5` | Turkey | damage | 3 | — | 1800 | 0 | 0 | 800 | 0 | 0 | 15.62 |
| **Stable tatar damage +3 (lvl 7)** `tursta.tatar.1.6` | Turkey | damage | 3 | — | 850 | 0 | 0 | 650 | 0 | 0 | 15.62 |
| **Stable tatar protection +1 (lvl 2)** `tursta.tatar.2.1` | Turkey | protection | 1 | — | 900 | 0 | 0 | 250 | 0 | 0 | 15.62 |
| **Stable tatar protection +1 (lvl 3)** `tursta.tatar.2.2` | Turkey | protection | 1 | — | 6200 | 0 | 0 | 1150 | 0 | 0 | 15.62 |
| **Stable tatar protection +2 (lvl 4)** `tursta.tatar.2.3` | Turkey | protection | 2 | — | 5400 | 0 | 0 | 2150 | 0 | 0 | 15.62 |
| **Stable tatar protection +1 (lvl 5)** `tursta.tatar.2.4` | Turkey | protection | 1 | — | 2000 | 0 | 0 | 1200 | 0 | 0 | 15.62 |
| **Stable tatar protection +1 (lvl 6)** `tursta.tatar.2.5` | Turkey | protection | 1 | — | 3000 | 0 | 0 | 4250 | 0 | 0 | 15.62 |
| **Stable tatar protection +2 (lvl 7)** `tursta.tatar.2.6` | Turkey | protection | 2 | — | 5001 | 0 | 0 | 8101 | 0 | 0 | 15.62 |
| **Stable vityaz damage +1 (lvl 2)** `russta.vityaz.1.1` | Russia | damage | 1 | — | 500 | 0 | 0 | 100 | 0 | 0 | 15.62 |
| **Stable vityaz damage +2 (lvl 3)** `russta.vityaz.1.2` | Russia | damage | 2 | — | 900 | 0 | 0 | 220 | 0 | 0 | 15.62 |
| **Stable vityaz damage +1 (lvl 4)** `russta.vityaz.1.3` | Russia | damage | 1 | — | 4400 | 0 | 0 | 280 | 0 | 0 | 15.62 |
| **Stable vityaz damage +1 (lvl 5)** `russta.vityaz.1.4` | Russia | damage | 1 | — | 2250 | 0 | 0 | 320 | 0 | 0 | 15.62 |
| **Stable vityaz damage +1 (lvl 6)** `russta.vityaz.1.5` | Russia | damage | 1 | — | 3030 | 0 | 0 | 600 | 0 | 0 | 15.62 |
| **Stable vityaz damage +1 (lvl 7)** `russta.vityaz.1.6` | Russia | damage | 1 | — | 7000 | 0 | 0 | 1800 | 0 | 0 | 15.62 |
| **Stable vityaz protection +2 (lvl 2)** `russta.vityaz.2.1` | Russia | protection | 2 | — | 200 | 0 | 0 | 135 | 300 | 0 | 15.62 |
| **Stable vityaz protection +3 (lvl 3)** `russta.vityaz.2.2` | Russia | protection | 3 | — | 600 | 0 | 0 | 100 | 400 | 0 | 15.62 |
| **Stable vityaz protection +3 (lvl 4)** `russta.vityaz.2.3` | Russia | protection | 3 | — | 800 | 0 | 0 | 200 | 560 | 0 | 15.62 |
| **Stable vityaz protection +2 (lvl 5)** `russta.vityaz.2.4` | Russia | protection | 2 | — | 1600 | 0 | 0 | 300 | 640 | 0 | 15.62 |
| **Stable vityaz protection +1 (lvl 6)** `russta.vityaz.2.5` | Russia | protection | 1 | — | 3200 | 0 | 0 | 350 | 300 | 0 | 15.62 |
| **Stable vityaz protection +1 (lvl 7)** `russta.vityaz.2.6` | Russia | protection | 1 | — | 16000 | 0 | 0 | 1000 | 5000 | 0 | 15.62 |
| **Stable wingedhussar damage +1 (lvl 2)** `polsta.wingedhussar.1.1` | Poland | damage | 1 | — | 400 | 0 | 0 | 200 | 0 | 0 | 15.62 |
| **Stable wingedhussar damage +2 (lvl 3)** `polsta.wingedhussar.1.2` | Poland | damage | 2 | — | 990 | 0 | 0 | 120 | 0 | 0 | 15.62 |
| **Stable wingedhussar damage +2 (lvl 4)** `polsta.wingedhussar.1.3` | Poland | damage | 2 | — | 2400 | 0 | 0 | 380 | 0 | 0 | 15.62 |
| **Stable wingedhussar damage +2 (lvl 5)** `polsta.wingedhussar.1.4` | Poland | damage | 2 | — | 4250 | 0 | 0 | 220 | 0 | 0 | 15.62 |
| **Stable wingedhussar damage +2 (lvl 6)** `polsta.wingedhussar.1.5` | Poland | damage | 2 | — | 7030 | 0 | 0 | 200 | 0 | 0 | 15.62 |
| **Stable wingedhussar damage +1 (lvl 7)** `polsta.wingedhussar.1.6` | Poland | damage | 1 | — | 3000 | 0 | 0 | 2200 | 0 | 0 | 15.62 |
| **Stable wingedhussar protection +2 (lvl 2)** `polsta.wingedhussar.2.1` | Poland | protection | 2 | — | 300 | 0 | 0 | 35 | 100 | 0 | 15.62 |
| **Stable wingedhussar protection +2 (lvl 3)** `polsta.wingedhussar.2.2` | Poland | protection | 2 | — | 500 | 0 | 0 | 200 | 600 | 0 | 15.62 |
| **Stable wingedhussar protection +2 (lvl 4)** `polsta.wingedhussar.2.3` | Poland | protection | 2 | — | 600 | 0 | 0 | 300 | 260 | 0 | 15.62 |
| **Stable wingedhussar protection +2 (lvl 5)** `polsta.wingedhussar.2.4` | Poland | protection | 2 | — | 1800 | 0 | 0 | 200 | 940 | 0 | 15.62 |
| **Stable wingedhussar protection +2 (lvl 6)** `polsta.wingedhussar.2.5` | Poland | protection | 2 | — | 2200 | 0 | 0 | 150 | 700 | 0 | 15.62 |
| **Stable wingedhussar protection +2 (lvl 7)** `polsta.wingedhussar.2.6` | Poland | protection | 2 | — | 17150 | 0 | 0 | 1200 | 4600 | 0 | 15.62 |

<a id="bar--казарма-17-в-по-юнитам"></a>
<a id="казарма-17-в-по-юнитам-bar"></a>
## Barracks, 17th century (`bar`)
| Upgrade | Nations | Effect | Value | Price change | Food | Wood | Stone | Gold | Iron | Coal | Time |
|---|---|---|---:|---|---:|---:|---:|---:|---:|---:|---:|
| **Barracks 17c archer damage +2 (lvl 2)** `algbar.archer.1.1` | Algeria | damage | 2 | — | 700 | 0 | 0 | 250 | 0 | 0 | 15.62 |
| **Barracks 17c archer damage +2 (lvl 3)** `algbar.archer.1.2` | Algeria | damage | 2 | — | 500 | 0 | 0 | 200 | 0 | 0 | 15.62 |
| **Barracks 17c archer damage +2 (lvl 4)** `algbar.archer.1.3` | Algeria | damage | 2 | — | 700 | 0 | 0 | 240 | 0 | 0 | 15.62 |
| **Barracks 17c archer damage +3 (lvl 5)** `algbar.archer.1.4` | Algeria | damage | 3 | — | 1200 | 0 | 0 | 900 | 0 | 0 | 15.62 |
| **Barracks 17c archer damage +3 (lvl 6)** `algbar.archer.1.5` | Algeria | damage | 3 | — | 1800 | 0 | 0 | 800 | 0 | 0 | 15.62 |
| **Barracks 17c archer damage +3 (lvl 7)** `algbar.archer.1.6` | Algeria | damage | 3 | — | 850 | 0 | 0 | 650 | 0 | 0 | 15.62 |
| **Barracks 17c archer protection +1 (lvl 2)** `algbar.archer.2.1` | Algeria | protection | 1 | — | 900 | 0 | 0 | 250 | 0 | 0 | 15.62 |
| **Barracks 17c archer protection +1 (lvl 3)** `algbar.archer.2.2` | Algeria | protection | 1 | — | 2200 | 0 | 0 | 550 | 0 | 0 | 15.62 |
| **Barracks 17c archer protection +2 (lvl 4)** `algbar.archer.2.3` | Algeria | protection | 2 | — | 3400 | 0 | 0 | 850 | 0 | 0 | 15.62 |
| **Barracks 17c archer protection +1 (lvl 5)** `algbar.archer.2.4` | Algeria | protection | 1 | — | 2000 | 0 | 0 | 400 | 0 | 0 | 15.62 |
| **Barracks 17c archer protection +1 (lvl 6)** `algbar.archer.2.5` | Algeria | protection | 1 | — | 3000 | 0 | 0 | 850 | 0 | 0 | 15.62 |
| **Barracks 17c archer protection +2 (lvl 7)** `algbar.archer.2.6` | Algeria | protection | 2 | — | 4000 | 0 | 0 | 1200 | 0 | 0 | 15.62 |
| **Barracks 17c archertur damage +2 (lvl 2)** `turbar.archertur.1.1` | Turkey | damage | 2 | — | 700 | 0 | 0 | 250 | 0 | 0 | 15.62 |
| **Barracks 17c archertur damage +2 (lvl 3)** `turbar.archertur.1.2` | Turkey | damage | 2 | — | 500 | 0 | 0 | 200 | 0 | 0 | 15.62 |
| **Barracks 17c archertur damage +2 (lvl 4)** `turbar.archertur.1.3` | Turkey | damage | 2 | — | 700 | 0 | 0 | 240 | 0 | 0 | 15.62 |
| **Barracks 17c archertur damage +3 (lvl 5)** `turbar.archertur.1.4` | Turkey | damage | 3 | — | 1200 | 0 | 0 | 900 | 0 | 0 | 15.62 |
| **Barracks 17c archertur damage +3 (lvl 6)** `turbar.archertur.1.5` | Turkey | damage | 3 | — | 1800 | 0 | 0 | 800 | 0 | 0 | 15.62 |
| **Barracks 17c archertur damage +3 (lvl 7)** `turbar.archertur.1.6` | Turkey | damage | 3 | — | 850 | 0 | 0 | 650 | 0 | 0 | 15.62 |
| **Barracks 17c archertur protection +1 (lvl 2)** `turbar.archertur.2.1` | Turkey | protection | 1 | — | 900 | 0 | 0 | 250 | 0 | 0 | 15.62 |
| **Barracks 17c archertur protection +2 (lvl 3)** `turbar.archertur.2.2` | Turkey | protection | 2 | — | 6200 | 0 | 0 | 1150 | 0 | 0 | 15.62 |
| **Barracks 17c archertur protection +2 (lvl 4)** `turbar.archertur.2.3` | Turkey | protection | 2 | — | 5400 | 0 | 0 | 2150 | 0 | 0 | 15.62 |
| **Barracks 17c archertur protection +1 (lvl 5)** `turbar.archertur.2.4` | Turkey | protection | 1 | — | 2000 | 0 | 0 | 1200 | 0 | 0 | 15.62 |
| **Barracks 17c archertur protection +2 (lvl 6)** `turbar.archertur.2.5` | Turkey | protection | 2 | — | 3000 | 0 | 0 | 4250 | 0 | 0 | 15.62 |
| **Barracks 17c archertur protection +2 (lvl 7)** `turbar.archertur.2.6` | Turkey | protection | 2 | — | 5001 | 0 | 0 | 8101 | 0 | 0 | 15.62 |
| **Barracks 17c bagpiper protection +10 (lvl 2)** `scobar.bagpiper.2.1` | Scotland | protection | 10 | — | 706 | 0 | 0 | 50 | 0 | 0 | 15.62 |
| **Barracks 17c drummer protection +12 (lvl 2)** `prubar.drummer.2.1` | Denmark, Hungary, Prussia, Saxony | protection | 12 | — | 1205 | 0 | 0 | 90 | 0 | 0 | 15.62 |
| **Barracks 17c drummer protection +12 (lvl 2)** `ausbar.drummer.2.1` | Austria, Spain, Venice | protection | 12 | — | 706 | 0 | 0 | 50 | 0 | 0 | 15.62 |
| **Barracks 17c drummer protection +12 (lvl 2)** `swebar.drummer.2.1` | Bavaria, Portugal, Sweden | protection | 12 | — | 905 | 0 | 0 | 25 | 0 | 0 | 15.62 |
| **Barracks 17c drummer protection +12 (lvl 2)** `frabar.drummer.2.1` | France, Piedmont | protection | 12 | — | 500 | 0 | 0 | 75 | 0 | 0 | 15.62 |
| **Barracks 17c drummer protection +12 (lvl 2)** `engbar.drummer.2.1` | England, Switzerland | protection | 12 | — | 670 | 0 | 0 | 45 | 0 | 0 | 15.62 |
| **Barracks 17c drummer protection +12 (lvl 2)** `polbar.drummer.2.1` | Poland | protection | 12 | — | 405 | 0 | 0 | 250 | 0 | 0 | 15.62 |
| **Barracks 17c drummer protection +12 (lvl 2)** `netbar.drummer.2.1` | Netherlands | protection | 12 | — | 845 | 0 | 0 | 95 | 0 | 0 | 15.62 |
| **Barracks 17c drummerrus protection +10 (lvl 2)** `rusbar.drummerrus.2.1` | Russia | protection | 10 | — | 706 | 0 | 0 | 50 | 0 | 0 | 15.62 |
| **Barracks 17c drummertur protection +10 (lvl 2)** `turbar.drummertur.2.1` | Algeria, Turkey | protection | 10 | — | 706 | 0 | 0 | 50 | 0 | 0 | 15.62 |
| **Barracks 17c gauduk damage +1 (lvl 2)** `hunbar.gauduk.1.1` | Hungary | damage | 1 | — | 500 | 0 | 0 | 125 | 0 | 0 | 15.62 |
| **Barracks 17c gauduk damage +1 (lvl 3)** `hunbar.gauduk.1.2` | Hungary | damage | 1 | — | 1250 | 0 | 0 | 275 | 0 | 0 | 15.62 |
| **Barracks 17c gauduk damage +2 (lvl 4)** `hunbar.gauduk.1.3` | Hungary | damage | 2 | — | 2500 | 0 | 0 | 650 | 0 | 0 | 15.62 |
| **Barracks 17c gauduk protection +1 (lvl 2)** `hunbar.gauduk.2.1` | Hungary | protection | 1 | — | 125 | 0 | 0 | 150 | 100 | 0 | 15.62 |
| **Barracks 17c gauduk protection +1 (lvl 3)** `hunbar.gauduk.2.2` | Hungary | protection | 1 | — | 375 | 0 | 0 | 100 | 200 | 0 | 15.62 |
| **Barracks 17c gauduk protection +2 (lvl 4)** `hunbar.gauduk.2.3` | Hungary | protection | 2 | — | 1570 | 0 | 0 | 300 | 450 | 0 | 15.62 |
| **Barracks 17c gauduk protection +1 (lvl 5)** `hunbar.gauduk.2.4` | Hungary | protection | 1 | — | 2556 | 0 | 0 | 350 | 400 | 0 | 15.62 |
| **Barracks 17c gauduk protection +1 (lvl 6)** `hunbar.gauduk.2.5` | Hungary | protection | 1 | — | 2060 | 0 | 0 | 450 | 100 | 0 | 15.62 |
| **Barracks 17c gauduk protection +2 (lvl 7)** `hunbar.gauduk.2.6` | Hungary | protection | 2 | — | 2700 | 0 | 0 | 950 | 600 | 0 | 15.62 |
| **Barracks 17c jannisary damage +1 (lvl 2)** `turbar.jannisary.1.1` | Turkey | damage | 1 | — | 2000 | 0 | 0 | 100 | 0 | 0 | 15.62 |
| **Barracks 17c jannisary damage +1 (lvl 3)** `turbar.jannisary.1.2` | Turkey | damage | 1 | — | 1000 | 0 | 0 | 300 | 0 | 0 | 15.62 |
| **Barracks 17c jannisary damage +2 (lvl 4)** `turbar.jannisary.1.3` | Turkey | damage | 2 | — | 500 | 0 | 0 | 700 | 0 | 0 | 15.62 |
| `turbar.jannisary.1.4` | Turkey | +damage | 1 | — | 5000 | 0 | 0 | 1600 | 0 | 0 | 15.62 |
| `turbar.jannisary.1.5` | Turkey | +damage | 2 | — | 7500 | 0 | 0 | 3200 | 0 | 0 | 15.62 |
| `turbar.jannisary.1.6` | Turkey | +damage | 3 | — | 10000 | 0 | 0 | 4800 | 0 | 0 | 15.62 |
| **Barracks 17c jannisary protection +1 (lvl 2)** `turbar.jannisary.2.1` | Turkey | protection | 1 | — | 170 | 0 | 0 | 50 | 100 | 0 | 15.62 |
| **Barracks 17c jannisary protection +2 (lvl 3)** `turbar.jannisary.2.2` | Turkey | protection | 2 | — | 405 | 0 | 0 | 150 | 200 | 0 | 15.62 |
| **Barracks 17c jannisary protection +2 (lvl 4)** `turbar.jannisary.2.3` | Turkey | protection | 2 | — | 1570 | 0 | 0 | 100 | 350 | 0 | 15.62 |
| **Barracks 17c jannisary protection +1 (lvl 5)** `turbar.jannisary.2.4` | Turkey | protection | 1 | — | 1556 | 0 | 0 | 550 | 100 | 0 | 15.62 |
| **Barracks 17c jannisary protection +2 (lvl 6)** `turbar.jannisary.2.5` | Turkey | protection | 2 | — | 1060 | 0 | 0 | 850 | 400 | 0 | 15.62 |
| **Barracks 17c jannisary protection +2 (lvl 7)** `turbar.jannisary.2.6` | Turkey | protection | 2 | — | 4700 | 0 | 0 | 450 | 700 | 0 | 15.62 |
| **Barracks 17c lightinfantry damage +1 (lvl 2)** `turbar.lightinfantry.1.1` | Algeria, Turkey | damage | 1 | — | 100 | 0 | 0 | 50 | 0 | 0 | 15.62 |
| **Barracks 17c lightinfantry damage +1 (lvl 3)** `turbar.lightinfantry.1.2` | Algeria, Turkey | damage | 1 | — | 1100 | 0 | 0 | 200 | 0 | 0 | 15.62 |
| **Barracks 17c lightinfantry damage +11300 (lvl 4)** `turbar.lightinfantry.1.3` | Turkey | damage | 11300 | — | 325 | 0 | 0 | 0 | 0 | 0 | 15.62 |
| **Barracks 17c lightinfantry damage +1 (lvl 4)** `algbar.lightinfantry.1.3` | Algeria | damage | 1 | — | 1300 | 0 | 0 | 325 | 0 | 0 | 15.62 |
| `turbar.lightinfantry.1.4` | Turkey | +damage | 1 | — | 3000 | 0 | 0 | 360 | 0 | 0 | 15.62 |
| `algbar.lightinfantry.1.4` | Algeria | +damage | 2 | — | 3000 | 0 | 0 | 360 | 0 | 0 | 15.62 |
| `turbar.lightinfantry.1.5` | Turkey | +damage | 1 | — | 4500 | 0 | 0 | 540 | 0 | 0 | 15.62 |
| `algbar.lightinfantry.1.5` | Algeria | +damage | 2 | — | 4500 | 0 | 0 | 540 | 0 | 0 | 15.62 |
| `turbar.lightinfantry.1.6` | Turkey | +damage | 2 | — | 9375 | 0 | 0 | 1125 | 0 | 0 | 15.62 |
| `algbar.lightinfantry.1.6` | Algeria | +damage | 3 | — | 9375 | 0 | 0 | 1125 | 0 | 0 | 15.62 |
| **Barracks 17c lightinfantry protection +1 (lvl 2)** `turbar.lightinfantry.2.1` | Algeria, Turkey | protection | 1 | — | 200 | 0 | 0 | 70 | 120 | 0 | 15.62 |
| **Barracks 17c lightinfantry protection +1 (lvl 3)** `turbar.lightinfantry.2.2` | Algeria, Turkey | protection | 1 | — | 6360 | 0 | 0 | 150 | 320 | 0 | 15.62 |
| **Barracks 17c lightinfantry protection +2 (lvl 4)** `turbar.lightinfantry.2.3` | Algeria, Turkey | protection | 2 | — | 506 | 0 | 0 | 250 | 420 | 0 | 15.62 |
| `turbar.lightinfantry.2.4` | Algeria, Turkey | +protection | 1 | — | 3600 | 0 | 0 | 600 | 0 | 0 | 15.62 |
| `turbar.lightinfantry.2.5` | Algeria, Turkey | +protection | 1 | — | 5400 | 0 | 0 | 900 | 0 | 0 | 15.62 |
| `turbar.lightinfantry.2.6` | Algeria, Turkey | +protection | 2 | — | 11250 | 0 | 0 | 1875 | 0 | 0 | 15.62 |
| **Barracks 17c musketeer damage +1 (lvl 2)** `prubar.musketeer.1.1` | Denmark, Piedmont, Prussia, Saxony, Switzerland, Venice | damage | 1 | — | 2000 | 0 | 0 | 100 | 0 | 0 | 15.62 |
| **Barracks 17c musketeer damage +1 (lvl 2)** `swebar.musketeer.1.1` | Bavaria, Portugal, Sweden | damage | 1 | — | 1000 | 0 | 0 | 200 | 0 | 0 | 15.62 |
| **Barracks 17c musketeer damage +1 (lvl 2)** `frabar.musketeer.1.1` | France | damage | 1 | — | 100 | 0 | 0 | 50 | 0 | 0 | 15.62 |
| **Barracks 17c musketeer damage +1 (lvl 2)** `engbar.musketeer.1.1` | England | damage | 1 | — | 1900 | 0 | 0 | 150 | 0 | 0 | 15.62 |
| **Barracks 17c musketeer damage +1 (lvl 3)** `engbar.musketeer.1.2` | Denmark, England, Piedmont, Prussia, Saxony, Switzerland, Venice | damage | 1 | — | 1000 | 0 | 0 | 300 | 0 | 0 | 15.62 |
| **Barracks 17c musketeer damage +1 (lvl 3)** `swebar.musketeer.1.2` | Bavaria, Portugal, Sweden | damage | 1 | — | 2000 | 0 | 0 | 200 | 0 | 0 | 15.62 |
| **Barracks 17c musketeer damage +1 (lvl 3)** `frabar.musketeer.1.2` | France | damage | 1 | — | 3000 | 0 | 0 | 500 | 0 | 0 | 15.62 |
| **Barracks 17c musketeer damage +2 (lvl 4)** `engbar.musketeer.1.3` | Denmark, England, Piedmont, Prussia, Saxony, Switzerland, Venice | damage | 2 | — | 500 | 0 | 0 | 700 | 0 | 0 | 15.62 |
| **Barracks 17c musketeer damage +2 (lvl 4)** `swebar.musketeer.1.3` | Bavaria, Portugal, Sweden | damage | 2 | — | 100 | 0 | 0 | 200 | 0 | 0 | 15.62 |
| **Barracks 17c musketeer damage +2 (lvl 4)** `frabar.musketeer.1.3` | France | damage | 2 | — | 2500 | 0 | 0 | 750 | 0 | 0 | 15.62 |
| **Barracks 17c musketeer protection +1 (lvl 2)** `prubar.musketeer.2.1` | Denmark, Piedmont, Prussia, Saxony, Switzerland, Venice | protection | 1 | — | 170 | 0 | 0 | 50 | 100 | 0 | 15.62 |
| **Barracks 17c musketeer protection +1 (lvl 2)** `swebar.musketeer.2.1` | Bavaria, Portugal, Sweden | protection | 1 | — | 450 | 0 | 0 | 550 | 300 | 0 | 15.62 |
| **Barracks 17c musketeer protection +1 (lvl 2)** `frabar.musketeer.2.1` | France | protection | 1 | — | 200 | 0 | 0 | 75 | 200 | 0 | 15.62 |
| **Barracks 17c musketeer protection +1 (lvl 2)** `engbar.musketeer.2.1` | England | protection | 1 | — | 220 | 0 | 0 | 50 | 100 | 0 | 15.62 |
| **Barracks 17c musketeer protection +2 (lvl 3)** `prubar.musketeer.2.2` | Denmark, Piedmont, Prussia, Saxony, Switzerland, Venice | protection | 2 | — | 405 | 0 | 0 | 150 | 200 | 0 | 15.62 |
| **Barracks 17c musketeer protection +2 (lvl 3)** `swebar.musketeer.2.2` | Bavaria, Portugal, Sweden | protection | 2 | — | 405 | 0 | 0 | 150 | 20 | 0 | 15.62 |
| **Barracks 17c musketeer protection +2 (lvl 3)** `frabar.musketeer.2.2` | France | protection | 2 | — | 705 | 0 | 0 | 250 | 250 | 0 | 15.62 |
| **Barracks 17c musketeer protection +2 (lvl 3)** `engbar.musketeer.2.2` | England | protection | 2 | — | 505 | 0 | 0 | 140 | 200 | 0 | 15.62 |
| **Barracks 17c musketeer protection +2 (lvl 4)** `prubar.musketeer.2.3` | Denmark, Piedmont, Prussia, Saxony, Switzerland, Venice | protection | 2 | — | 1570 | 0 | 0 | 100 | 350 | 0 | 15.62 |
| **Barracks 17c musketeer protection +2 (lvl 4)** `swebar.musketeer.2.3` | Bavaria, Portugal, Sweden | protection | 2 | — | 1570 | 0 | 0 | 100 | 290 | 0 | 15.62 |
| **Barracks 17c musketeer protection +2 (lvl 4)** `frabar.musketeer.2.3` | France | protection | 2 | — | 2560 | 0 | 0 | 300 | 450 | 0 | 15.62 |
| **Barracks 17c musketeer protection +2 (lvl 4)** `engbar.musketeer.2.3` | England | protection | 2 | — | 1670 | 0 | 0 | 100 | 350 | 0 | 15.62 |
| **Barracks 17c musketeer protection +1 (lvl 5)** `frabar.musketeer.2.4` | Denmark, France, Piedmont, Prussia, Saxony, Switzerland, Venice | protection | 1 | — | 1556 | 0 | 0 | 550 | 100 | 0 | 15.62 |
| **Barracks 17c musketeer protection +1 (lvl 5)** `swebar.musketeer.2.4` | Bavaria, Portugal, Sweden | protection | 1 | — | 1956 | 0 | 0 | 450 | 700 | 0 | 15.62 |
| **Barracks 17c musketeer protection +1 (lvl 5)** `engbar.musketeer.2.4` | England | protection | 1 | — | 1000 | 0 | 0 | 920 | 100 | 0 | 15.62 |
| **Barracks 17c musketeer protection +2 (lvl 6)** `frabar.musketeer.2.5` | Denmark, France, Piedmont, Prussia, Saxony, Switzerland, Venice | protection | 2 | — | 1060 | 0 | 0 | 850 | 400 | 0 | 15.62 |
| **Barracks 17c musketeer protection +2 (lvl 6)** `porbar.musketeer.2.5` | Bavaria, Portugal | protection | 2 | — | 1660 | 0 | 0 | 550 | 400 | 0 | 15.62 |
| **Barracks 17c musketeer protection +2 (lvl 6)** `engbar.musketeer.2.5` | England | protection | 2 | — | 1060 | 0 | 0 | 700 | 400 | 0 | 15.62 |
| **Barracks 17c musketeer protection +2 (lvl 6)** `swebar.musketeer.2.5` | Sweden | protection | 2 | — | 1660 | 0 | 0 | 650 | 400 | 0 | 15.62 |
| **Barracks 17c musketeer protection +2 (lvl 7)** `prubar.musketeer.2.6` | Denmark, Piedmont, Prussia, Saxony, Switzerland, Venice | protection | 2 | — | 3700 | 0 | 0 | 450 | 700 | 0 | 15.62 |
| **Barracks 17c musketeer protection +2 (lvl 7)** `frabar.musketeer.2.6` | France | protection | 2 | — | 3700 | 0 | 0 | 650 | 700 | 0 | 15.62 |
| **Barracks 17c musketeer protection +2 (lvl 7)** `engbar.musketeer.2.6` | England | protection | 2 | — | 3900 | 0 | 0 | 550 | 700 | 0 | 15.62 |
| **Barracks 17c musketeer protection +2 (lvl 7)** `swebar.musketeer.2.6` | Sweden | protection | 2 | — | 2700 | 0 | 0 | 650 | 100 | 0 | 15.62 |
| **Barracks 17c musketeer protection +2 (lvl 7)** `porbar.musketeer.2.6` | Portugal | protection | 2 | — | 2700 | 0 | 0 | 850 | 100 | 0 | 15.62 |
| **Barracks 17c musketeer protection +2 (lvl 7)** `bavbar.musketeer.2.6` | Bavaria | protection | 2 | — | 2700 | 0 | 0 | 750 | 100 | 0 | 15.62 |
| **Barracks 17c musketeeraus damage +1 (lvl 2)** `ausbar.musketeeraus.1.1` | Austria | damage | 1 | — | 2000 | 0 | 0 | 100 | 0 | 0 | 15.62 |
| **Barracks 17c musketeeraus damage +1 (lvl 3)** `ausbar.musketeeraus.1.2` | Austria | damage | 1 | — | 1000 | 0 | 0 | 300 | 0 | 0 | 15.62 |
| **Barracks 17c musketeeraus damage +2 (lvl 4)** `ausbar.musketeeraus.1.3` | Austria | damage | 2 | — | 500 | 0 | 0 | 700 | 0 | 0 | 15.62 |
| **Barracks 17c musketeeraus protection +1 (lvl 2)** `ausbar.musketeeraus.2.1` | Austria | protection | 1 | — | 170 | 0 | 0 | 50 | 100 | 0 | 15.62 |
| **Barracks 17c musketeeraus protection +1 (lvl 3)** `ausbar.musketeeraus.2.2` | Austria | protection | 1 | — | 405 | 0 | 0 | 150 | 200 | 0 | 15.62 |
| **Barracks 17c musketeeraus protection +1 (lvl 4)** `ausbar.musketeeraus.2.3` | Austria | protection | 1 | — | 1570 | 0 | 0 | 100 | 350 | 0 | 15.62 |
| **Barracks 17c musketeeraus protection +1 (lvl 5)** `ausbar.musketeeraus.2.4` | Austria | protection | 1 | — | 1556 | 0 | 0 | 550 | 100 | 0 | 15.62 |
| **Barracks 17c musketeeraus protection +1 (lvl 6)** `ausbar.musketeeraus.2.5` | Austria | protection | 1 | — | 1060 | 0 | 0 | 850 | 400 | 0 | 15.62 |
| **Barracks 17c musketeeraus protection +1 (lvl 7)** `ausbar.musketeeraus.2.6` | Austria | protection | 1 | — | 3700 | 0 | 0 | 750 | 700 | 0 | 15.62 |
| **Barracks 17c musketeernet damage +1 (lvl 2)** `netbar.musketeernet.1.1` | Netherlands | damage | 1 | — | 2000 | 0 | 0 | 100 | 0 | 0 | 15.62 |
| **Barracks 17c musketeernet damage +1 (lvl 3)** `netbar.musketeernet.1.2` | Netherlands | damage | 1 | — | 1000 | 0 | 0 | 300 | 0 | 0 | 15.62 |
| **Barracks 17c musketeernet damage +2 (lvl 4)** `netbar.musketeernet.1.3` | Netherlands | damage | 2 | — | 500 | 0 | 0 | 700 | 0 | 0 | 15.62 |
| **Barracks 17c musketeernet protection +1 (lvl 2)** `netbar.musketeernet.2.1` | Netherlands | protection | 1 | — | 170 | 0 | 0 | 50 | 100 | 0 | 15.62 |
| **Barracks 17c musketeernet protection +1 (lvl 3)** `netbar.musketeernet.2.2` | Netherlands | protection | 1 | — | 405 | 0 | 0 | 150 | 200 | 0 | 15.62 |
| **Barracks 17c musketeernet protection +2 (lvl 4)** `netbar.musketeernet.2.3` | Netherlands | protection | 2 | — | 1570 | 0 | 0 | 100 | 350 | 0 | 15.62 |
| **Barracks 17c musketeernet protection +1 (lvl 5)** `netbar.musketeernet.2.4` | Netherlands | protection | 1 | — | 1556 | 0 | 0 | 550 | 100 | 0 | 15.62 |
| **Barracks 17c musketeernet protection +1 (lvl 6)** `netbar.musketeernet.2.5` | Netherlands | protection | 1 | — | 1060 | 0 | 0 | 850 | 400 | 0 | 15.62 |
| **Barracks 17c musketeernet protection +2 (lvl 7)** `netbar.musketeernet.2.6` | Netherlands | protection | 2 | — | 3700 | 0 | 0 | 450 | 700 | 0 | 15.62 |
| **Barracks 17c musketeerpol damage +1 (lvl 2)** `polbar.musketeerpol.1.1` | Poland | damage | 1 | — | 500 | 0 | 0 | 125 | 0 | 0 | 15.62 |
| **Barracks 17c musketeerpol damage +1 (lvl 3)** `polbar.musketeerpol.1.2` | Poland | damage | 1 | — | 1250 | 0 | 0 | 275 | 0 | 0 | 15.62 |
| **Barracks 17c musketeerpol damage +2 (lvl 4)** `polbar.musketeerpol.1.3` | Poland | damage | 2 | — | 2500 | 0 | 0 | 650 | 0 | 0 | 15.62 |
| **Barracks 17c musketeerpol protection +1 (lvl 2)** `polbar.musketeerpol.2.1` | Poland | protection | 1 | — | 125 | 0 | 0 | 150 | 100 | 0 | 15.62 |
| **Barracks 17c musketeerpol protection +1 (lvl 3)** `polbar.musketeerpol.2.2` | Poland | protection | 1 | — | 375 | 0 | 0 | 100 | 200 | 0 | 15.62 |
| **Barracks 17c musketeerpol protection +2 (lvl 4)** `polbar.musketeerpol.2.3` | Poland | protection | 2 | — | 1570 | 0 | 0 | 300 | 450 | 0 | 15.62 |
| **Barracks 17c musketeerpol protection +1 (lvl 5)** `polbar.musketeerpol.2.4` | Poland | protection | 1 | — | 2556 | 0 | 0 | 350 | 400 | 0 | 15.62 |
| **Barracks 17c musketeerpol protection +1 (lvl 6)** `polbar.musketeerpol.2.5` | Poland | protection | 1 | — | 3060 | 0 | 0 | 650 | 100 | 0 | 15.62 |
| **Barracks 17c musketeerpol protection +2 (lvl 7)** `polbar.musketeerpol.2.6` | Poland | protection | 2 | — | 2700 | 0 | 0 | 750 | 600 | 0 | 15.62 |
| **Barracks 17c musketeersco damage +1 (lvl 2)** `scobar.musketeersco.1.1` | Scotland | damage | 1 | — | 2500 | 0 | 0 | 200 | 0 | 0 | 15.62 |
| **Barracks 17c musketeersco damage +1 (lvl 3)** `scobar.musketeersco.1.2` | Scotland | damage | 1 | — | 1500 | 0 | 0 | 400 | 0 | 0 | 15.62 |
| **Barracks 17c musketeersco damage +2 (lvl 4)** `scobar.musketeersco.1.3` | Scotland | damage | 2 | — | 500 | 0 | 0 | 800 | 0 | 0 | 15.62 |
| **Barracks 17c musketeersco protection +1 (lvl 2)** `scobar.musketeersco.2.1` | Scotland | protection | 1 | — | 250 | 0 | 0 | 30 | 0 | 0 | 15.62 |
| **Barracks 17c musketeersco protection +1 (lvl 3)** `scobar.musketeersco.2.2` | Scotland | protection | 1 | — | 500 | 0 | 0 | 400 | 60 | 0 | 15.62 |
| **Barracks 17c musketeersco protection +2 (lvl 4)** `scobar.musketeersco.2.3` | Scotland | protection | 2 | — | 875 | 0 | 0 | 225 | 0 | 0 | 15.62 |
| **Barracks 17c musketeersco protection +1 (lvl 5)** `scobar.musketeersco.2.4` | Scotland | protection | 1 | — | 4200 | 0 | 0 | 240 | 0 | 0 | 15.62 |
| **Barracks 17c musketeersco protection +1 (lvl 6)** `scobar.musketeersco.2.5` | Scotland | protection | 1 | — | 6300 | 0 | 0 | 360 | 0 | 0 | 15.62 |
| **Barracks 17c musketeersco protection +2 (lvl 7)** `scobar.musketeersco.2.6` | Scotland | protection | 2 | — | 13125 | 0 | 0 | 750 | 0 | 0 | 15.62 |
| **Barracks 17c musketeerspa damage +1 (lvl 2)** `spabar.musketeerspa.1.1` | Spain | damage | 1 | — | 2000 | 0 | 0 | 100 | 0 | 0 | 15.62 |
| **Barracks 17c musketeerspa damage +1 (lvl 3)** `spabar.musketeerspa.1.2` | Spain | damage | 1 | — | 1000 | 0 | 0 | 300 | 0 | 0 | 15.62 |
| **Barracks 17c musketeerspa damage +2 (lvl 4)** `spabar.musketeerspa.1.3` | Spain | damage | 2 | — | 500 | 0 | 0 | 700 | 0 | 0 | 15.62 |
| **Barracks 17c musketeerspa protection +1 (lvl 2)** `spabar.musketeerspa.2.1` | Spain | protection | 1 | — | 170 | 0 | 0 | 50 | 100 | 0 | 15.62 |
| **Barracks 17c musketeerspa protection +1 (lvl 3)** `spabar.musketeerspa.2.2` | Spain | protection | 1 | — | 405 | 0 | 0 | 150 | 200 | 0 | 15.62 |
| **Barracks 17c musketeerspa protection +1 (lvl 4)** `spabar.musketeerspa.2.3` | Spain | protection | 1 | — | 1570 | 0 | 0 | 100 | 350 | 0 | 15.62 |
| **Barracks 17c musketeerspa protection +1 (lvl 5)** `spabar.musketeerspa.2.4` | Spain | protection | 1 | — | 1556 | 0 | 0 | 550 | 100 | 0 | 15.62 |
| **Barracks 17c musketeerspa protection +1 (lvl 6)** `spabar.musketeerspa.2.5` | Spain | protection | 1 | — | 1060 | 0 | 0 | 850 | 400 | 0 | 15.62 |
| **Barracks 17c musketeerspa protection +1 (lvl 7)** `spabar.musketeerspa.2.6` | Spain | protection | 1 | — | 3700 | 0 | 0 | 650 | 700 | 0 | 15.62 |
| **Barracks 17c officer damage +20 (lvl 2)** `ausbar.officer.1.1` | Austria, Piedmont, Spain, Venice | damage | 20 | — | 100 | 0 | 0 | 50 | 0 | 0 | 15.62 |
| **Barracks 17c officer damage +20 (lvl 2)** `prubar.officer.1.1` | Denmark, Hungary, Prussia, Saxony | damage | 20 | — | 150 | 0 | 0 | 25 | 0 | 0 | 15.62 |
| **Barracks 17c officer damage +20 (lvl 2)** `swebar.officer.1.1` | Bavaria, Portugal, Sweden | damage | 20 | — | 800 | 0 | 0 | 150 | 0 | 0 | 15.62 |
| **Barracks 17c officer damage +20 (lvl 2)** `frabar.officer.1.1` | France, Switzerland | damage | 20 | — | 200 | 0 | 0 | 25 | 0 | 0 | 15.62 |
| **Barracks 17c officer damage +20 (lvl 2)** `engbar.officer.1.1` | England | damage | 20 | — | 250 | 0 | 0 | 75 | 0 | 0 | 15.62 |
| **Barracks 17c officer damage +20 (lvl 2)** `polbar.officer.1.1` | Poland | damage | 20 | — | 50 | 0 | 0 | 150 | 0 | 0 | 15.62 |
| **Barracks 17c officer damage +20 (lvl 2)** `netbar.officer.1.1` | Netherlands | damage | 20 | — | 500 | 0 | 0 | 25 | 0 | 0 | 15.62 |
| **Barracks 17c officer protection +6 (lvl 2)** `prubar.officer.2.1` | Denmark, Hungary, Prussia, Saxony, Switzerland | protection | 6 | — | 1650 | 0 | 0 | 395 | 0 | 0 | 15.62 |
| **Barracks 17c officer protection +6 (lvl 2)** `swebar.officer.2.1` | Bavaria, Piedmont, Portugal, Sweden | protection | 6 | — | 1050 | 0 | 0 | 350 | 0 | 0 | 15.62 |
| **Barracks 17c officer protection +6 (lvl 2)** `ausbar.officer.2.1` | Austria, Spain | protection | 6 | — | 1850 | 0 | 0 | 450 | 0 | 0 | 15.62 |
| **Barracks 17c officer protection +6 (lvl 2)** `frabar.officer.2.1` | France | protection | 6 | — | 1950 | 0 | 0 | 350 | 0 | 0 | 15.62 |
| **Barracks 17c officer protection +6 (lvl 2)** `engbar.officer.2.1` | England | protection | 6 | — | 1650 | 0 | 0 | 425 | 0 | 0 | 15.62 |
| **Barracks 17c officer protection +6 (lvl 2)** `polbar.officer.2.1` | Poland | protection | 6 | — | 1550 | 0 | 0 | 650 | 0 | 0 | 15.62 |
| **Barracks 17c officer protection +6 (lvl 2)** `venbar.officer.2.1` | Venice | protection | 6 | — | 1450 | 0 | 0 | 450 | 0 | 0 | 15.62 |
| **Barracks 17c officer protection +6 (lvl 2)** `netbar.officer.2.1` | Netherlands | protection | 6 | — | 1550 | 0 | 0 | 475 | 0 | 0 | 15.62 |
| **Barracks 17c officerrus damage +30 (lvl 2)** `rusbar.officerrus.1.1` | Russia | damage | 30 | — | 100 | 0 | 0 | 50 | 0 | 0 | 15.62 |
| **Barracks 17c officerrus protection +10 (lvl 2)** `rusbar.officerrus.2.1` | Russia | protection | 10 | — | 1850 | 0 | 0 | 450 | 0 | 0 | 15.62 |
| **Barracks 17c officersco damage +30 (lvl 2)** `scobar.officersco.1.1` | Scotland | damage | 30 | — | 250 | 0 | 0 | 75 | 0 | 0 | 15.62 |
| **Barracks 17c officersco protection +10 (lvl 2)** `scobar.officersco.2.1` | Scotland | protection | 10 | — | 1550 | 0 | 0 | 425 | 0 | 0 | 15.62 |
| **Barracks 17c officertur damage +20 (lvl 2)** `turbar.officertur.1.1` | Algeria, Turkey | damage | 20 | — | 1000 | 0 | 0 | 800 | 0 | 0 | 15.62 |
| **Barracks 17c officertur protection +10 (lvl 2)** `turbar.officertur.2.1` | Algeria, Turkey | protection | 10 | — | 1706 | 0 | 0 | 350 | 0 | 0 | 15.62 |
| **Barracks 17c pikeman damage +1 (lvl 2)** `ausbar.pikeman.1.1` | Austria, England, Piedmont, Spain, Venice | damage | 1 | — | 200 | 0 | 0 | 50 | 0 | 0 | 15.62 |
| **Barracks 17c pikeman damage +1 (lvl 2)** `swebar.pikeman.1.1` | Hungary, Saxony, Sweden | damage | 1 | — | 100 | 0 | 0 | 90 | 0 | 0 | 15.62 |
| **Barracks 17c pikeman damage +1 (lvl 2)** `prubar.pikeman.1.1` | Bavaria, Denmark, Prussia | damage | 1 | — | 3600 | 0 | 0 | 450 | 0 | 0 | 15.62 |
| **Barracks 17c pikeman damage +1 (lvl 2)** `frabar.pikeman.1.1` | France | damage | 1 | — | 100 | 0 | 0 | 25 | 0 | 0 | 15.62 |
| **Barracks 17c pikeman damage +1 (lvl 2)** `netbar.pikeman.1.1` | Netherlands | damage | 1 | — | 900 | 0 | 0 | 150 | 0 | 0 | 15.62 |
| **Barracks 17c pikeman damage +2 (lvl 3)** `ausbar.pikeman.1.2` | Austria, Bavaria, Denmark, Piedmont, Prussia, Spain, Venice | damage | 2 | — | 1300 | 0 | 0 | 300 | 0 | 0 | 15.62 |
| **Barracks 17c pikeman damage +2 (lvl 3)** `swebar.pikeman.1.2` | Hungary, Saxony, Sweden | damage | 2 | — | 300 | 0 | 0 | 450 | 0 | 0 | 15.62 |
| **Barracks 17c pikeman damage +2 (lvl 3)** `frabar.pikeman.1.2` | France | damage | 2 | — | 1400 | 0 | 0 | 325 | 0 | 0 | 15.62 |
| **Barracks 17c pikeman damage +2 (lvl 3)** `engbar.pikeman.1.2` | England | damage | 2 | — | 1250 | 0 | 0 | 310 | 0 | 0 | 15.62 |
| **Barracks 17c pikeman damage +2 (lvl 3)** `netbar.pikeman.1.2` | Netherlands | damage | 2 | — | 700 | 0 | 0 | 400 | 0 | 0 | 15.62 |
| **Barracks 17c pikeman damage +2 (lvl 4)** `ausbar.pikeman.1.3` | Austria, Piedmont, Spain, Venice | damage | 2 | — | 3600 | 0 | 0 | 450 | 0 | 0 | 15.62 |
| **Barracks 17c pikeman damage +2 (lvl 4)** `swebar.pikeman.1.3` | Hungary, Saxony, Sweden | damage | 2 | — | 4600 | 0 | 0 | 300 | 0 | 0 | 15.62 |
| **Barracks 17c pikeman damage +2 (lvl 4)** `prubar.pikeman.1.3` | Bavaria, Denmark, Prussia | damage | 2 | — | 200 | 0 | 0 | 50 | 0 | 0 | 15.62 |
| **Barracks 17c pikeman damage +2 (lvl 4)** `frabar.pikeman.1.3` | France | damage | 2 | — | 4600 | 0 | 0 | 650 | 0 | 0 | 15.62 |
| **Barracks 17c pikeman damage +2 (lvl 4)** `engbar.pikeman.1.3` | England | damage | 2 | — | 3900 | 0 | 0 | 650 | 0 | 0 | 15.62 |
| **Barracks 17c pikeman damage +2 (lvl 4)** `netbar.pikeman.1.3` | Netherlands | damage | 2 | — | 3100 | 0 | 0 | 250 | 0 | 0 | 15.62 |
| **Barracks 17c pikeman damage +1 (lvl 5)** `ausbar.pikeman.1.4` | Austria, England, Piedmont, Spain, Venice | damage | 1 | — | 7200 | 0 | 0 | 1850 | 0 | 0 | 15.62 |
| **Barracks 17c pikeman damage +1 (lvl 5)** `swebar.pikeman.1.4` | Hungary, Saxony, Sweden | damage | 1 | — | 9200 | 0 | 0 | 1250 | 0 | 0 | 15.62 |
| **Barracks 17c pikeman damage +1 (lvl 5)** `prubar.pikeman.1.4` | Bavaria, Denmark, Prussia | damage | 1 | — | 6800 | 0 | 0 | 1950 | 0 | 0 | 15.62 |
| **Barracks 17c pikeman damage +1 (lvl 5)** `frabar.pikeman.1.4` | France | damage | 1 | — | 6200 | 0 | 0 | 1650 | 0 | 0 | 15.62 |
| **Barracks 17c pikeman damage +1 (lvl 5)** `netbar.pikeman.1.4` | Netherlands | damage | 1 | — | 6700 | 0 | 0 | 1950 | 0 | 0 | 15.62 |
| **Barracks 17c pikeman damage +2 (lvl 6)** `ausbar.pikeman.1.5` | Austria, England, Netherlands, Piedmont, Spain, Venice | damage | 2 | — | 16030 | 0 | 0 | 2000 | 0 | 0 | 15.62 |
| **Barracks 17c pikeman damage +2 (lvl 6)** `swebar.pikeman.1.5` | Hungary, Saxony, Sweden | damage | 2 | — | 14030 | 0 | 0 | 2600 | 0 | 0 | 15.62 |
| **Barracks 17c pikeman damage +2 (lvl 6)** `prubar.pikeman.1.5` | Bavaria, Denmark, Prussia | damage | 2 | — | 15030 | 0 | 0 | 2300 | 0 | 0 | 15.62 |
| **Barracks 17c pikeman damage +2 (lvl 6)** `frabar.pikeman.1.5` | France | damage | 2 | — | 15300 | 0 | 0 | 2075 | 0 | 0 | 15.62 |
| `ausbar.pikeman.1.6` | Austria, Bavaria, Denmark, England, France, Hungary, Netherlands, Piedmont, Prussia, Saxony, Spain, Sweden, Venice | +damage | 2 | — | 15000 | 0 | 0 | 1875 | 0 | 0 | 15.62 |
| **Barracks 17c pikeman protection +1 (lvl 2)** `ausbar.pikeman.2.1` | Austria, Piedmont, Spain, Venice | protection | 1 | — | 150 | 0 | 0 | 50 | 0 | 0 | 15.62 |
| **Barracks 17c pikeman protection +1 (lvl 2)** `prubar.pikeman.2.1` | Denmark, Hungary, Prussia, Saxony | protection | 1 | — | 175 | 0 | 0 | 40 | 0 | 0 | 15.62 |
| **Barracks 17c pikeman protection +1 (lvl 2)** `swebar.pikeman.2.1` | Bavaria, Sweden | protection | 1 | — | 350 | 0 | 0 | 50 | 0 | 0 | 15.62 |
| **Barracks 17c pikeman protection +1 (lvl 2)** `frabar.pikeman.2.1` | France | protection | 1 | — | 350 | 0 | 0 | 90 | 0 | 0 | 15.62 |
| **Barracks 17c pikeman protection +1 (lvl 2)** `engbar.pikeman.2.1` | England | protection | 1 | — | 990 | 0 | 0 | 50 | 0 | 0 | 15.62 |
| **Barracks 17c pikeman protection +1 (lvl 2)** `netbar.pikeman.2.1` | Netherlands | protection | 1 | — | 250 | 0 | 0 | 150 | 0 | 0 | 15.62 |
| **Barracks 17c pikeman protection +1 (lvl 3)** `ausbar.pikeman.2.2` | Austria, Piedmont, Spain, Venice | protection | 1 | — | 900 | 0 | 0 | 175 | 0 | 0 | 15.62 |
| **Barracks 17c pikeman protection +1 (lvl 3)** `prubar.pikeman.2.2` | Denmark, Hungary, Prussia, Saxony | protection | 1 | — | 990 | 0 | 0 | 275 | 0 | 0 | 15.62 |
| **Barracks 17c pikeman protection +1 (lvl 3)** `swebar.pikeman.2.2` | Bavaria, Sweden | protection | 1 | — | 700 | 0 | 0 | 275 | 0 | 0 | 15.62 |
| **Barracks 17c pikeman protection +1 (lvl 3)** `frabar.pikeman.2.2` | France | protection | 1 | — | 1000 | 0 | 0 | 135 | 0 | 0 | 15.62 |
| **Barracks 17c pikeman protection +1 (lvl 3)** `engbar.pikeman.2.2` | England | protection | 1 | — | 200 | 0 | 0 | 175 | 0 | 0 | 15.62 |
| **Barracks 17c pikeman protection +1 (lvl 3)** `netbar.pikeman.2.2` | Netherlands | protection | 1 | — | 800 | 0 | 0 | 275 | 0 | 0 | 15.62 |
| **Barracks 17c pikeman protection +2 (lvl 4)** `ausbar.pikeman.2.3` | Austria, England, Piedmont, Spain, Venice | protection | 2 | — | 4500 | 0 | 0 | 300 | 0 | 0 | 15.62 |
| **Barracks 17c pikeman protection +2 (lvl 4)** `prubar.pikeman.2.3` | Denmark, Hungary, Prussia, Saxony | protection | 2 | — | 4700 | 0 | 0 | 280 | 0 | 0 | 15.62 |
| **Barracks 17c pikeman protection +2 (lvl 4)** `swebar.pikeman.2.3` | Bavaria, Sweden | protection | 2 | — | 2500 | 0 | 0 | 200 | 0 | 0 | 15.62 |
| **Barracks 17c pikeman protection +2 (lvl 4)** `frabar.pikeman.2.3` | France | protection | 2 | — | 4200 | 0 | 0 | 500 | 0 | 0 | 15.62 |
| **Barracks 17c pikeman protection +2 (lvl 4)** `netbar.pikeman.2.3` | Netherlands | protection | 2 | — | 4200 | 0 | 0 | 100 | 0 | 0 | 15.62 |
| **Barracks 17c pikeman protection +1 (lvl 5)** `ausbar.pikeman.2.4` | Austria, England, Piedmont, Spain, Venice | protection | 1 | — | 9005 | 0 | 0 | 507 | 0 | 0 | 15.62 |
| **Barracks 17c pikeman protection +1 (lvl 5)** `prubar.pikeman.2.4` | Hungary, Prussia, Saxony | protection | 1 | — | 9505 | 0 | 0 | 707 | 0 | 0 | 15.62 |
| **Barracks 17c pikeman protection +1 (lvl 5)** `swebar.pikeman.2.4` | Bavaria, Sweden | protection | 1 | — | 13005 | 0 | 0 | 997 | 0 | 0 | 15.62 |
| **Barracks 17c pikeman protection +1 (lvl 5)** `frabar.pikeman.2.4` | France | protection | 1 | — | 11075 | 0 | 0 | 310 | 0 | 0 | 15.62 |
| **Barracks 17c pikeman protection +1 (lvl 5)** `netbar.pikeman.2.4` | Netherlands | protection | 1 | — | 9305 | 0 | 0 | 707 | 0 | 0 | 15.62 |
| **Barracks 17c pikeman protection +1 (lvl 5)** `denbar.pikeman.2.4` | Denmark | protection | 1 | — | 9005 | 0 | 0 | 707 | 0 | 0 | 15.62 |
| **Barracks 17c pikeman protection +1 (lvl 6)** `ausbar.pikeman.2.5` | Austria, Piedmont, Spain, Venice | protection | 1 | — | 18010 | 0 | 0 | 3050 | 0 | 0 | 15.62 |
| **Barracks 17c pikeman protection +1 (lvl 6)** `prubar.pikeman.2.5` | Denmark, Hungary, Prussia, Saxony | protection | 1 | — | 17510 | 0 | 0 | 2950 | 0 | 0 | 15.62 |
| **Barracks 17c pikeman protection +1 (lvl 6)** `swebar.pikeman.2.5` | Bavaria, Sweden | protection | 1 | — | 16010 | 0 | 0 | 2550 | 0 | 0 | 15.62 |
| **Barracks 17c pikeman protection +1 (lvl 6)** `frabar.pikeman.2.5` | France | protection | 1 | — | 15050 | 0 | 0 | 3050 | 0 | 0 | 15.62 |
| **Barracks 17c pikeman protection +1 (lvl 6)** `engbar.pikeman.2.5` | England | protection | 1 | — | 17010 | 0 | 0 | 3050 | 0 | 0 | 15.62 |
| **Barracks 17c pikeman protection +1 (lvl 6)** `netbar.pikeman.2.5` | Netherlands | protection | 1 | — | 17890 | 0 | 0 | 2850 | 0 | 0 | 15.62 |
| `ausbar.pikeman.2.6` | Austria, Bavaria, Denmark, England, France, Hungary, Netherlands, Piedmont, Prussia, Saxony, Spain, Sweden, Venice | +protection | 2 | — | 11250 | 0 | 0 | 1500 | 0 | 0 | 15.62 |
| **Barracks 17c pikemanpol damage +1 (lvl 2)** `polbar.pikemanpol.1.1` | Poland | damage | 1 | — | 500 | 0 | 0 | 50 | 0 | 0 | 15.62 |
| **Barracks 17c pikemanpol damage +1 (lvl 3)** `polbar.pikemanpol.1.2` | Poland | damage | 1 | — | 1400 | 0 | 0 | 100 | 0 | 0 | 15.62 |
| **Barracks 17c pikemanpol damage +1 (lvl 4)** `polbar.pikemanpol.1.3` | Poland | damage | 1 | — | 3200 | 0 | 0 | 450 | 0 | 0 | 15.62 |
| **Barracks 17c pikemanpol damage +2 (lvl 5)** `polbar.pikemanpol.1.4` | Poland | damage | 2 | — | 8200 | 0 | 0 | 2220 | 0 | 0 | 15.62 |
| **Barracks 17c pikemanpol damage +2 (lvl 6)** `polbar.pikemanpol.1.5` | Poland | damage | 2 | — | 15030 | 0 | 0 | 1800 | 0 | 0 | 15.62 |
| `polbar.pikemanpol.1.6` | Poland | +damage | 3 | — | 22500 | 0 | 0 | 2800 | 0 | 0 | 15.62 |
| **Barracks 17c pikemanpol protection +1 (lvl 2)** `polbar.pikemanpol.2.1` | Poland | protection | 1 | — | 250 | 0 | 0 | 75 | 0 | 0 | 15.62 |
| **Barracks 17c pikemanpol protection +1 (lvl 3)** `polbar.pikemanpol.2.2` | Poland | protection | 1 | — | 800 | 0 | 0 | 150 | 0 | 0 | 15.62 |
| **Barracks 17c pikemanpol protection +2 (lvl 4)** `polbar.pikemanpol.2.3` | Poland | protection | 2 | — | 3500 | 0 | 0 | 225 | 0 | 0 | 15.62 |
| **Barracks 17c pikemanpol protection +2 (lvl 5)** `polbar.pikemanpol.2.4` | Poland | protection | 2 | — | 9005 | 0 | 0 | 407 | 0 | 0 | 15.62 |
| **Barracks 17c pikemanpol protection +4 (lvl 6)** `polbar.pikemanpol.2.5` | Poland | protection | 4 | — | 19010 | 0 | 0 | 2975 | 0 | 0 | 15.62 |
| `polbar.pikemanpol.2.6` | Poland | +protection | 3 | — | 15000 | 0 | 0 | 1000 | 0 | 0 | 15.62 |
| **Barracks 17c pikemanpor damage +1 (lvl 2)** `porbar.pikemanpor.1.1` | Portugal | damage | 1 | — | 3600 | 0 | 0 | 450 | 0 | 0 | 15.62 |
| **Barracks 17c pikemanpor damage +1 (lvl 3)** `porbar.pikemanpor.1.2` | Portugal | damage | 1 | — | 1300 | 0 | 0 | 300 | 0 | 0 | 15.62 |
| **Barracks 17c pikemanpor damage +2 (lvl 4)** `porbar.pikemanpor.1.3` | Portugal | damage | 2 | — | 200 | 0 | 0 | 50 | 0 | 0 | 15.62 |
| **Barracks 17c pikemanpor damage +1 (lvl 5)** `porbar.pikemanpor.1.4` | Portugal | damage | 1 | — | 6800 | 0 | 0 | 1950 | 0 | 0 | 15.62 |
| **Barracks 17c pikemanpor damage +2 (lvl 6)** `porbar.pikemanpor.1.5` | Portugal | damage | 2 | — | 15030 | 0 | 0 | 2300 | 0 | 0 | 15.62 |
| `porbar.pikemanpor.1.6` | Portugal | +damage | 3 | — | 15000 | 0 | 0 | 1875 | 0 | 0 | 15.62 |
| **Barracks 17c pikemanpor protection +1 (lvl 2)** `porbar.pikemanpor.2.1` | Portugal | protection | 1 | — | 350 | 0 | 0 | 50 | 0 | 0 | 15.62 |
| **Barracks 17c pikemanpor protection +1 (lvl 3)** `porbar.pikemanpor.2.2` | Portugal | protection | 1 | — | 700 | 0 | 0 | 275 | 0 | 0 | 15.62 |
| **Barracks 17c pikemanpor protection +2 (lvl 4)** `porbar.pikemanpor.2.3` | Portugal | protection | 2 | — | 2500 | 0 | 0 | 200 | 0 | 0 | 15.62 |
| **Barracks 17c pikemanpor protection +1 (lvl 5)** `porbar.pikemanpor.2.4` | Portugal | protection | 1 | — | 13005 | 0 | 0 | 997 | 0 | 0 | 15.62 |
| **Barracks 17c pikemanpor protection +2 (lvl 6)** `porbar.pikemanpor.2.5` | Portugal | protection | 2 | — | 16010 | 0 | 0 | 2550 | 0 | 0 | 15.62 |
| `porbar.pikemanpor.2.6` | Portugal | +protection | 3 | — | 11250 | 0 | 0 | 1500 | 0 | 0 | 15.62 |
| **Barracks 17c pikemanrus damage +1 (lvl 2)** `rusbar.pikemanrus.1.1` | Russia | damage | 1 | — | 200 | 0 | 0 | 50 | 0 | 0 | 15.62 |
| **Barracks 17c pikemanrus damage +2 (lvl 3)** `rusbar.pikemanrus.1.2` | Russia | damage | 2 | — | 1300 | 0 | 0 | 300 | 0 | 0 | 15.62 |
| **Barracks 17c pikemanrus damage +2 (lvl 4)** `rusbar.pikemanrus.1.3` | Russia | damage | 2 | — | 3600 | 0 | 0 | 450 | 0 | 0 | 15.62 |
| **Barracks 17c pikemanrus damage +1 (lvl 5)** `rusbar.pikemanrus.1.4` | Russia | damage | 1 | — | 7200 | 0 | 0 | 1850 | 0 | 0 | 15.62 |
| **Barracks 17c pikemanrus damage +2 (lvl 6)** `rusbar.pikemanrus.1.5` | Russia | damage | 2 | — | 16030 | 0 | 0 | 2000 | 0 | 0 | 15.62 |
| `rusbar.pikemanrus.1.6` | Russia | +damage | 2 | — | 15000 | 0 | 0 | 1875 | 0 | 0 | 15.62 |
| **Barracks 17c pikemanrus protection +1 (lvl 2)** `rusbar.pikemanrus.2.1` | Russia | protection | 1 | — | 150 | 0 | 0 | 50 | 0 | 0 | 15.62 |
| **Barracks 17c pikemanrus protection +1 (lvl 3)** `rusbar.pikemanrus.2.2` | Russia | protection | 1 | — | 900 | 0 | 0 | 175 | 0 | 0 | 15.62 |
| **Barracks 17c pikemanrus protection +2 (lvl 4)** `rusbar.pikemanrus.2.3` | Russia | protection | 2 | — | 4500 | 0 | 0 | 300 | 0 | 0 | 15.62 |
| **Barracks 17c pikemanrus protection +1 (lvl 5)** `rusbar.pikemanrus.2.4` | Russia | protection | 1 | — | 9005 | 0 | 0 | 507 | 0 | 0 | 15.62 |
| **Barracks 17c pikemanrus protection +1 (lvl 6)** `rusbar.pikemanrus.2.5` | Russia | protection | 1 | — | 18010 | 0 | 0 | 3050 | 0 | 0 | 15.62 |
| `rusbar.pikemanrus.2.6` | Russia | +protection | 2 | — | 11250 | 0 | 0 | 1500 | 0 | 0 | 15.62 |
| **Barracks 17c pikemansco damage +1 (lvl 2)** `scobar.pikemansco.1.1` | Scotland | damage | 1 | — | 250 | 0 | 0 | 70 | 0 | 0 | 15.62 |
| **Barracks 17c pikemansco damage +2 (lvl 3)** `scobar.pikemansco.1.2` | Scotland | damage | 2 | — | 750 | 0 | 0 | 210 | 0 | 0 | 15.62 |
| **Barracks 17c pikemansco damage +3 (lvl 4)** `scobar.pikemansco.1.3` | Scotland | damage | 3 | — | 2800 | 0 | 0 | 790 | 0 | 0 | 15.62 |
| **Barracks 17c pikemansco damage +1 (lvl 5)** `scobar.pikemansco.1.4` | Scotland | damage | 1 | — | 6000 | 0 | 0 | 750 | 0 | 0 | 15.62 |
| **Barracks 17c pikemansco damage +2 (lvl 6)** `scobar.pikemansco.1.5` | Scotland | damage | 2 | — | 10800 | 0 | 0 | 1350 | 0 | 0 | 15.62 |
| `scobar.pikemansco.1.6` | Scotland | +damage | 3 | — | 22500 | 0 | 0 | 2800 | 0 | 0 | 15.62 |
| **Barracks 17c pikemansco protection +1 (lvl 2)** `scobar.pikemansco.2.1` | Scotland | protection | 1 | — | 150 | 0 | 0 | 60 | 0 | 0 | 15.62 |
| **Barracks 17c pikemansco protection +2 (lvl 3)** `scobar.pikemansco.2.2` | Scotland | protection | 2 | — | 450 | 0 | 0 | 180 | 0 | 0 | 15.62 |
| **Barracks 17c pikemansco protection +3 (lvl 4)** `scobar.pikemansco.2.3` | Scotland | protection | 3 | — | 1690 | 0 | 0 | 675 | 0 | 0 | 15.62 |
| **Barracks 17c pikemansco protection +1 (lvl 5)** `scobar.pikemansco.2.4` | Scotland | protection | 1 | — | 4500 | 0 | 0 | 600 | 0 | 0 | 15.62 |
| **Barracks 17c pikemansco protection +2 (lvl 6)** `scobar.pikemansco.2.5` | Scotland | protection | 2 | — | 8100 | 0 | 0 | 1080 | 0 | 0 | 15.62 |
| `scobar.pikemansco.2.6` | Scotland | +protection | 3 | — | 16875 | 0 | 0 | 2250 | 0 | 0 | 15.62 |
| **Barracks 17c pikemanspa damage +1 (lvl 2)** `spabar.pikemanspa.1.1` | Spain | damage | 1 | — | 200 | 0 | 0 | 50 | 0 | 0 | 15.62 |
| **Barracks 17c pikemanspa damage +2 (lvl 3)** `spabar.pikemanspa.1.2` | Spain | damage | 2 | — | 1300 | 0 | 0 | 300 | 0 | 0 | 15.62 |
| **Barracks 17c pikemanspa damage +3 (lvl 4)** `spabar.pikemanspa.1.3` | Spain | damage | 3 | — | 3600 | 0 | 0 | 450 | 0 | 0 | 15.62 |
| **Barracks 17c pikemanspa damage +2 (lvl 5)** `spabar.pikemanspa.1.4` | Spain | damage | 2 | — | 7200 | 0 | 0 | 1850 | 0 | 0 | 15.62 |
| **Barracks 17c pikemanspa damage +1 (lvl 6)** `spabar.pikemanspa.1.5` | Spain | damage | 1 | — | 16030 | 0 | 0 | 2000 | 0 | 0 | 15.62 |
| **Barracks 17c pikemanspa damage +1 (lvl 7)** `spabar.pikemanspa.1.6` | Spain | damage | 1 | — | 15000 | 0 | 0 | 1875 | 0 | 0 | 15.62 |
| **Barracks 17c pikemanspa protection +1 (lvl 2)** `spabar.pikemanspa.2.1` | Spain | protection | 1 | — | 150 | 0 | 0 | 50 | 0 | 0 | 15.62 |
| **Barracks 17c pikemanspa protection +1 (lvl 3)** `spabar.pikemanspa.2.2` | Spain | protection | 1 | — | 900 | 0 | 0 | 175 | 0 | 0 | 15.62 |
| **Barracks 17c pikemanspa protection +2 (lvl 4)** `spabar.pikemanspa.2.3` | Spain | protection | 2 | — | 4500 | 0 | 0 | 300 | 0 | 0 | 15.62 |
| **Barracks 17c pikemanspa protection +1 (lvl 5)** `spabar.pikemanspa.2.4` | Spain | protection | 1 | — | 9005 | 0 | 0 | 507 | 0 | 0 | 15.62 |
| **Barracks 17c pikemanspa protection +1 (lvl 6)** `spabar.pikemanspa.2.5` | Spain | protection | 1 | — | 18010 | 0 | 0 | 3050 | 0 | 0 | 15.62 |
| **Barracks 17c pikemanspa protection +2 (lvl 7)** `spabar.pikemanspa.2.6` | Spain | protection | 2 | — | 16000 | 0 | 0 | 1000 | 0 | 0 | 15.62 |
| **Barracks 17c pikemanswi damage +2 (lvl 2)** `swibar.pikemanswi.1.1` | Switzerland | damage | 2 | — | 200 | 0 | 0 | 50 | 0 | 0 | 15.62 |
| **Barracks 17c pikemanswi damage +3 (lvl 3)** `swibar.pikemanswi.1.2` | Switzerland | damage | 3 | — | 1300 | 0 | 0 | 300 | 0 | 0 | 15.62 |
| **Barracks 17c pikemanswi damage +2 (lvl 4)** `swibar.pikemanswi.1.3` | Switzerland | damage | 2 | — | 3600 | 0 | 0 | 450 | 0 | 0 | 15.62 |
| **Barracks 17c pikemanswi damage +1 (lvl 5)** `swibar.pikemanswi.1.4` | Switzerland | damage | 1 | — | 7200 | 0 | 0 | 1850 | 0 | 0 | 15.62 |
| **Barracks 17c pikemanswi damage +1 (lvl 6)** `swibar.pikemanswi.1.5` | Switzerland | damage | 1 | — | 16030 | 0 | 0 | 2000 | 0 | 0 | 15.62 |
| `swibar.pikemanswi.1.6` | Switzerland | +damage | 1 | — | 15000 | 0 | 0 | 1875 | 0 | 0 | 15.62 |
| **Barracks 17c pikemanswi protection +2 (lvl 2)** `swibar.pikemanswi.2.1` | Switzerland | protection | 2 | — | 150 | 0 | 0 | 50 | 0 | 0 | 15.62 |
| **Barracks 17c pikemanswi protection +2 (lvl 3)** `swibar.pikemanswi.2.2` | Switzerland | protection | 2 | — | 900 | 0 | 0 | 175 | 0 | 0 | 15.62 |
| **Barracks 17c pikemanswi protection +1 (lvl 4)** `swibar.pikemanswi.2.3` | Switzerland | protection | 1 | — | 4500 | 0 | 0 | 300 | 0 | 0 | 15.62 |
| **Barracks 17c pikemanswi protection +1 (lvl 5)** `swibar.pikemanswi.2.4` | Switzerland | protection | 1 | — | 9005 | 0 | 0 | 507 | 0 | 0 | 15.62 |
| **Barracks 17c pikemanswi protection +1 (lvl 6)** `swibar.pikemanswi.2.5` | Switzerland | protection | 1 | — | 18010 | 0 | 0 | 3050 | 0 | 0 | 15.62 |
| `swibar.pikemanswi.2.6` | Switzerland | +protection | 1 | — | 11250 | 0 | 0 | 1500 | 0 | 0 | 15.62 |
| **Barracks 17c pikemantur damage +2 (lvl 2)** `turbar.pikemantur.1.1` | Algeria, Turkey | damage | 2 | — | 200 | 0 | 0 | 50 | 0 | 0 | 15.62 |
| **Barracks 17c pikemantur damage +2 (lvl 3)** `turbar.pikemantur.1.2` | Algeria, Turkey | damage | 2 | — | 600 | 0 | 0 | 300 | 0 | 0 | 15.62 |
| **Barracks 17c pikemantur damage +2 (lvl 4)** `turbar.pikemantur.1.3` | Algeria, Turkey | damage | 2 | — | 1200 | 0 | 0 | 450 | 0 | 0 | 15.62 |
| **Barracks 17c pikemantur damage +2 (lvl 5)** `turbar.pikemantur.1.4` | Algeria, Turkey | damage | 2 | — | 2200 | 0 | 0 | 1850 | 0 | 0 | 15.62 |
| **Barracks 17c pikemantur damage +2 (lvl 6)** `turbar.pikemantur.1.5` | Algeria, Turkey | damage | 2 | — | 16030 | 0 | 0 | 2000 | 0 | 0 | 15.62 |
| `turbar.pikemantur.1.6` | Algeria, Turkey | +damage | 2 | — | 18750 | 0 | 0 | 2350 | 0 | 0 | 15.62 |
| **Barracks 17c pikemantur protection +1 (lvl 2)** `turbar.pikemantur.2.1` | Algeria, Turkey | protection | 1 | — | 150 | 0 | 0 | 50 | 0 | 0 | 15.62 |
| **Barracks 17c pikemantur protection +2 (lvl 3)** `turbar.pikemantur.2.2` | Algeria, Turkey | protection | 2 | — | 900 | 0 | 0 | 175 | 0 | 0 | 15.62 |
| **Barracks 17c pikemantur protection +3 (lvl 4)** `turbar.pikemantur.2.3` | Algeria, Turkey | protection | 3 | — | 4500 | 0 | 0 | 300 | 0 | 0 | 15.62 |
| **Barracks 17c pikemantur protection +1 (lvl 5)** `turbar.pikemantur.2.4` | Algeria, Turkey | protection | 1 | — | 9005 | 0 | 0 | 507 | 0 | 0 | 15.62 |
| **Barracks 17c pikemantur protection +2 (lvl 6)** `turbar.pikemantur.2.5` | Algeria, Turkey | protection | 2 | — | 18010 | 0 | 0 | 3050 | 0 | 0 | 15.62 |
| `turbar.pikemantur.2.6` | Algeria, Turkey | +protection | 3 | — | 16875 | 0 | 0 | 2250 | 0 | 0 | 15.62 |
| **Barracks 17c roundshier damage +1 (lvl 2)** `ausbar.roundshier.1.1` | Austria | damage | 1 | — | 150 | 0 | 0 | 50 | 0 | 0 | 15.62 |
| **Barracks 17c roundshier damage +1 (lvl 3)** `ausbar.roundshier.1.2` | Austria | damage | 1 | — | 1500 | 0 | 0 | 200 | 0 | 0 | 15.62 |
| **Barracks 17c roundshier damage +2 (lvl 4)** `ausbar.roundshier.1.3` | Austria | damage | 2 | — | 1300 | 0 | 0 | 325 | 0 | 0 | 15.62 |
| `ausbar.roundshier.1.4` | Austria | +damage | 1 | — | 7500 | 0 | 0 | 900 | 0 | 0 | 15.62 |
| `ausbar.roundshier.1.5` | Austria | +damage | 1 | — | 9000 | 0 | 0 | 1080 | 0 | 0 | 15.62 |
| `ausbar.roundshier.1.6` | Austria | +damage | 2 | — | 18750 | 0 | 0 | 2250 | 0 | 0 | 15.62 |
| **Barracks 17c roundshier protection +1 (lvl 2)** `ausbar.roundshier.2.1` | Austria | protection | 1 | — | 200 | 0 | 0 | 70 | 120 | 0 | 15.62 |
| **Barracks 17c roundshier protection +2 (lvl 3)** `ausbar.roundshier.2.2` | Austria | protection | 2 | — | 4360 | 0 | 0 | 150 | 320 | 0 | 15.62 |
| **Barracks 17c roundshier protection +2 (lvl 4)** `ausbar.roundshier.2.3` | Austria | protection | 2 | — | 506 | 0 | 0 | 250 | 420 | 0 | 15.62 |
| `ausbar.roundshier.2.4` | Austria | +protection | 1 | — | 3750 | 0 | 0 | 450 | 0 | 0 | 15.62 |
| `ausbar.roundshier.2.5` | Austria | +protection | 1 | — | 6750 | 0 | 0 | 810 | 0 | 0 | 15.62 |
| `ausbar.roundshier.2.6` | Austria | +protection | 2 | — | 9375 | 0 | 0 | 1125 | 0 | 0 | 15.62 |
| **Barracks 17c serdiuk damage +2 (lvl 2)** `ukrbar.serdiuk.1.1` | Ukraine | damage | 2 | — | 5400 | 0 | 0 | 350 | 0 | 0 | 15.62 |
| **Barracks 17c serdiuk damage +2 (lvl 3)** `ukrbar.serdiuk.1.2` | Ukraine | damage | 2 | — | 22000 | 0 | 0 | 800 | 0 | 0 | 15.62 |
| **Barracks 17c serdiuk damage +2 (lvl 4)** `ukrbar.serdiuk.1.3` | Ukraine | damage | 2 | — | 32400 | 0 | 0 | 5800 | 0 | 0 | 15.62 |
| **Barracks 17c serdiuk damage +2 (lvl 5)** `ukrbar.serdiuk.1.4` | Ukraine | damage | 2 | — | 42010 | 0 | 0 | 6800 | 0 | 0 | 15.62 |
| **Barracks 17c serdiuk damage +2 (lvl 6)** `ukrbar.serdiuk.1.5` | Ukraine | damage | 2 | — | 52300 | 0 | 0 | 1800 | 7400 | 0 | 15.62 |
| `ukrbar.serdiuk.1.6` | Ukraine | +damage | 3 | — | 60000 | 0 | 0 | 8000 | 0 | 0 | 15.62 |
| **Barracks 17c serdiuk protection +1 (lvl 2)** `ukrbar.serdiuk.2.1` | Ukraine | protection | 1 | — | 200 | 0 | 0 | 40 | 0 | 0 | 15.62 |
| **Barracks 17c serdiuk protection +2 (lvl 3)** `ukrbar.serdiuk.2.2` | Ukraine | protection | 2 | — | 600 | 0 | 0 | 120 | 0 | 0 | 15.62 |
| **Barracks 17c serdiuk protection +2 (lvl 4)** `ukrbar.serdiuk.2.3` | Ukraine | protection | 2 | — | 1500 | 0 | 0 | 300 | 0 | 0 | 15.62 |
| **Barracks 17c serdiuk protection +1 (lvl 5)** `ukrbar.serdiuk.2.4` | Ukraine | protection | 1 | — | 3500 | 0 | 0 | 450 | 0 | 0 | 15.62 |
| **Barracks 17c serdiuk protection +2 (lvl 6)** `ukrbar.serdiuk.2.5` | Ukraine | protection | 2 | — | 8100 | 0 | 0 | 210 | 0 | 0 | 15.62 |
| `ukrbar.serdiuk.2.6` | Ukraine | +protection | 2 | — | 11250 | 0 | 0 | 1125 | 0 | 0 | 15.62 |
| **Barracks 17c strelet damage +1 (lvl 2)** `rusbar.strelet.1.1` | Russia | damage | 1 | — | 2000 | 0 | 0 | 100 | 0 | 0 | 15.62 |
| **Barracks 17c strelet damage +1 (lvl 3)** `rusbar.strelet.1.2` | Russia | damage | 1 | — | 1000 | 0 | 0 | 300 | 0 | 0 | 15.62 |
| **Barracks 17c strelet damage +2 (lvl 4)** `rusbar.strelet.1.3` | Russia | damage | 2 | — | 500 | 0 | 0 | 700 | 0 | 0 | 15.62 |
| **Barracks 17c strelet protection +3 (lvl 2)** `rusbar.strelet.2.1` | Russia | protection | 3 | — | 170 | 0 | 0 | 50 | 100 | 0 | 15.62 |
| **Barracks 17c strelet protection +3 (lvl 3)** `rusbar.strelet.2.2` | Russia | protection | 3 | — | 405 | 0 | 0 | 150 | 200 | 0 | 15.62 |
| **Barracks 17c strelet protection +2 (lvl 4)** `rusbar.strelet.2.3` | Russia | protection | 2 | — | 1570 | 0 | 0 | 100 | 350 | 0 | 15.62 |
| **Barracks 17c strelet protection +2 (lvl 5)** `rusbar.strelet.2.4` | Russia | protection | 2 | — | 1556 | 0 | 0 | 550 | 100 | 0 | 15.62 |
| **Barracks 17c strelet protection +1 (lvl 6)** `rusbar.strelet.2.5` | Russia | protection | 1 | — | 1060 | 0 | 0 | 850 | 400 | 0 | 15.62 |
| **Barracks 17c strelet protection +1 (lvl 7)** `rusbar.strelet.2.6` | Russia | protection | 1 | — | 3700 | 0 | 0 | 650 | 700 | 0 | 15.62 |

<a id="ba2--казарма-18-в-по-юнитам"></a>
<a id="казарма-18-в-по-юнитам-ba2"></a>
## Barracks, 18th century (`ba2`)

| Upgrade | Nations | Effect | Value | Price change | Food | Wood | Stone | Gold | Iron | Coal | Time |
|---|---|---|---:|---|---:|---:|---:|---:|---:|---:|---:|
| **Barracks 18c archersco damage +2 (lvl 2)** `scoba2.archersco.1.1` | Scotland | damage | 2 | — | 3000 | 0 | 0 | 360 | 0 | 0 | 15.62 |
| **Barracks 18c archersco damage +3 (lvl 3)** `scoba2.archersco.1.2` | Scotland | damage | 3 | — | 7500 | 0 | 0 | 700 | 0 | 0 | 15.62 |
| **Barracks 18c archersco damage +4 (lvl 4)** `scoba2.archersco.1.3` | Scotland | damage | 4 | — | 9750 | 0 | 0 | 1200 | 0 | 0 | 15.62 |
| **Barracks 18c archersco damage +2 (lvl 5)** `scoba2.archersco.1.4` | Scotland | damage | 2 | — | 18000 | 0 | 0 | 1800 | 0 | 0 | 15.62 |
| **Barracks 18c archersco damage +4 (lvl 6)** `scoba2.archersco.1.5` | Scotland | damage | 4 | — | 33200 | 0 | 0 | 4320 | 0 | 0 | 15.62 |
| **Barracks 18c archersco damage +5 (lvl 7)** `scoba2.archersco.1.6` | Scotland | damage | 5 | — | 55000 | 0 | 0 | 7550 | 0 | 0 | 15.62 |
| **Barracks 18c archersco protection +1 (lvl 2)** `scoba2.archersco.2.1` | Scotland | protection | 1 | — | 900 | 0 | 0 | 250 | 0 | 0 | 15.62 |
| **Barracks 18c archersco protection +2 (lvl 3)** `scoba2.archersco.2.2` | Scotland | protection | 2 | — | 2200 | 0 | 0 | 450 | 0 | 0 | 15.62 |
| **Barracks 18c archersco protection +3 (lvl 4)** `scoba2.archersco.2.3` | Scotland | protection | 3 | — | 5400 | 0 | 0 | 800 | 0 | 0 | 15.62 |
| **Barracks 18c archersco protection +3 (lvl 5)** `scoba2.archersco.2.4` | Scotland | protection | 3 | — | 12500 | 0 | 0 | 1000 | 0 | 0 | 15.62 |
| **Barracks 18c archersco protection +2 (lvl 6)** `scoba2.archersco.2.5` | Scotland | protection | 2 | — | 20000 | 0 | 0 | 1200 | 0 | 0 | 15.62 |
| **Barracks 18c archersco protection +1 (lvl 7)** `scoba2.archersco.2.6` | Scotland | protection | 1 | — | 16500 | 0 | 0 | 1875 | 0 | 0 | 15.62 |
| **Barracks 18c bagpiper protection +10 (lvl 2)** `engba2.bagpiper.2.1` | England | protection | 10 | — | 555 | 0 | 0 | 90 | 0 | 0 | 15.62 |
| **Barracks 18c chasseur damage +2 (lvl 2)** `fraba2.chasseur.1.1` | France | damage | 2 | — | 3000 | 0 | 0 | 750 | 0 | 0 | 15.62 |
| **Barracks 18c chasseur damage +2 (lvl 3)** `fraba2.chasseur.1.2` | France | damage | 2 | — | 4000 | 0 | 0 | 1100 | 0 | 0 | 15.62 |
| **Barracks 18c chasseur damage +2 (lvl 4)** `fraba2.chasseur.1.3` | France | damage | 2 | — | 7000 | 0 | 0 | 1800 | 0 | 0 | 15.62 |
| **Barracks 18c chasseur damage +2 (lvl 5)** `fraba2.chasseur.1.4` | France | damage | 2 | — | 12000 | 0 | 0 | 350 | 0 | 0 | 15.62 |
| **Barracks 18c chasseur damage +2 (lvl 6)** `fraba2.chasseur.1.5` | France | damage | 2 | — | 32020 | 0 | 0 | 850 | 0 | 0 | 15.62 |
| **Barracks 18c chasseur damage +2 (lvl 7)** `fraba2.chasseur.1.6` | France | damage | 2 | — | 45200 | 0 | 0 | 1330 | 0 | 0 | 15.62 |
| **Barracks 18c chasseur protection +1 (lvl 2)** `fraba2.chasseur.2.1` | France | protection | 1 | — | 3706 | 0 | 0 | 350 | 0 | 0 | 15.62 |
| **Barracks 18c chasseur protection +1 (lvl 3)** `fraba2.chasseur.2.2` | France | protection | 1 | — | 12060 | 0 | 0 | 1350 | 0 | 0 | 15.62 |
| **Barracks 18c chasseur protection +1 (lvl 4)** `fraba2.chasseur.2.3` | France | protection | 1 | — | 36706 | 0 | 0 | 2150 | 0 | 0 | 15.62 |
| **Barracks 18c chasseur protection +1 (lvl 5)** `fraba2.chasseur.2.4` | France | protection | 1 | — | 36706 | 0 | 0 | 3350 | 0 | 0 | 15.62 |
| **Barracks 18c chasseur protection +1 (lvl 6)** `fraba2.chasseur.2.5` | France | protection | 1 | — | 37060 | 0 | 0 | 1350 | 0 | 0 | 15.62 |
| **Barracks 18c chasseur protection +1 (lvl 7)** `fraba2.chasseur.2.6` | France | protection | 1 | — | 16706 | 0 | 0 | 1350 | 0 | 0 | 15.62 |
| **Barracks 18c drummer18 protection +15 (lvl 2)** `ausba2.drummer18.2.1` | Austria, Piedmont, Russia, Spain, Switzerland, Venice | protection | 15 | — | 706 | 0 | 0 | 50 | 0 | 0 | 15.62 |
| **Barracks 18c drummer18 protection +15 (lvl 2)** `pruba2.drummer18.2.1` | Denmark, Hungary, Prussia, Saxony | protection | 15 | — | 900 | 0 | 0 | 45 | 0 | 0 | 15.62 |
| **Barracks 18c drummer18 protection +15 (lvl 2)** `sweba2.drummer18.2.1` | Bavaria, Portugal, Sweden | protection | 15 | — | 205 | 0 | 0 | 90 | 0 | 0 | 15.62 |
| **Barracks 18c drummer18 protection +15 (lvl 2)** `fraba2.drummer18.2.1` | France | protection | 15 | — | 805 | 0 | 0 | 65 | 0 | 0 | 15.62 |
| **Barracks 18c drummer18 protection +15 (lvl 2)** `polba2.drummer18.2.1` | Poland | protection | 15 | — | 205 | 0 | 0 | 150 | 0 | 0 | 15.62 |
| **Barracks 18c drummer18 protection +15 (lvl 2)** `netba2.drummer18.2.1` | Netherlands | protection | 15 | — | 450 | 0 | 0 | 75 | 0 | 0 | 15.62 |
| **Barracks 18c grenadier damage +2 (lvl 2)** `ausba2.grenadier.1.1` | Austria, Netherlands, Piedmont, Portugal, Russia, Spain, Switzerland, Venice | damage | 2 | — | 2000 | 0 | 0 | 800 | 0 | 0 | 15.62 |
| **Barracks 18c grenadier damage +2 (lvl 2)** `fraba2.grenadier.1.1` | France | damage | 2 | — | 1800 | 0 | 0 | 800 | 0 | 0 | 15.62 |
| **Barracks 18c grenadier damage +2 (lvl 2)** `engba2.grenadier.1.1` | England | damage | 2 | — | 1000 | 0 | 0 | 1300 | 0 | 0 | 15.62 |
| **Barracks 18c grenadier damage +2 (lvl 2)** `polba2.grenadier.1.1` | Poland | damage | 2 | — | 3000 | 0 | 0 | 800 | 0 | 0 | 15.62 |
| **Barracks 18c grenadier damage +2 (lvl 2)** `sweba2.grenadier.1.1` | Sweden | damage | 2 | — | 1000 | 0 | 0 | 800 | 0 | 0 | 15.62 |
| **Barracks 18c grenadier damage +3 (lvl 3)** `ausba2.grenadier.1.2` | Austria, Netherlands, Piedmont, Portugal, Russia, Spain, Switzerland, Venice | damage | 3 | — | 12000 | 0 | 0 | 1800 | 0 | 0 | 15.62 |
| **Barracks 18c grenadier damage +3 (lvl 3)** `fraba2.grenadier.1.2` | France | damage | 3 | — | 11200 | 0 | 0 | 1750 | 0 | 0 | 15.62 |
| **Barracks 18c grenadier damage +3 (lvl 3)** `engba2.grenadier.1.2` | England | damage | 3 | — | 10000 | 0 | 0 | 1900 | 0 | 0 | 15.62 |
| **Barracks 18c grenadier damage +3 (lvl 3)** `polba2.grenadier.1.2` | Poland | damage | 3 | — | 11000 | 0 | 0 | 1800 | 0 | 0 | 15.62 |
| **Barracks 18c grenadier damage +3 (lvl 3)** `sweba2.grenadier.1.2` | Sweden | damage | 3 | — | 13000 | 0 | 0 | 1800 | 0 | 0 | 15.62 |
| **Barracks 18c grenadier damage +4 (lvl 4)** `ausba2.grenadier.1.3` | Austria, Netherlands, Piedmont, Portugal, Russia, Spain, Switzerland, Venice | damage | 4 | — | 32000 | 0 | 0 | 2800 | 0 | 0 | 15.62 |
| **Barracks 18c grenadier damage +4 (lvl 4)** `fraba2.grenadier.1.3` | France | damage | 4 | — | 33000 | 0 | 0 | 2900 | 0 | 0 | 15.62 |
| **Barracks 18c grenadier damage +4 (lvl 4)** `engba2.grenadier.1.3` | England | damage | 4 | — | 22000 | 0 | 0 | 2900 | 0 | 0 | 15.62 |
| **Barracks 18c grenadier damage +4 (lvl 4)** `polba2.grenadier.1.3` | Poland | damage | 4 | — | 31000 | 0 | 0 | 2800 | 0 | 0 | 15.62 |
| **Barracks 18c grenadier damage +4 (lvl 4)** `sweba2.grenadier.1.3` | Sweden | damage | 4 | — | 25000 | 0 | 0 | 1800 | 0 | 0 | 15.62 |
| **Barracks 18c grenadier damage +5 (lvl 5)** `ausba2.grenadier.1.4` | Austria, Netherlands, Piedmont, Portugal, Russia, Spain, Switzerland, Venice | damage | 5 | — | 42000 | 0 | 0 | 3800 | 0 | 0 | 15.62 |
| **Barracks 18c grenadier damage +5 (lvl 5)** `fraba2.grenadier.1.4` | France | damage | 5 | — | 42000 | 0 | 0 | 4800 | 0 | 0 | 15.62 |
| **Barracks 18c grenadier damage +5 (lvl 5)** `engba2.grenadier.1.4` | England | damage | 5 | — | 52000 | 0 | 0 | 3700 | 0 | 0 | 15.62 |
| **Barracks 18c grenadier damage +5 (lvl 5)** `polba2.grenadier.1.4` | Poland | damage | 5 | — | 43000 | 0 | 0 | 3800 | 0 | 0 | 15.62 |
| **Barracks 18c grenadier damage +5 (lvl 5)** `sweba2.grenadier.1.4` | Sweden | damage | 5 | — | 49000 | 0 | 0 | 4800 | 0 | 0 | 15.62 |
| **Barracks 18c grenadier damage +6 (lvl 6)** `ausba2.grenadier.1.5` | Austria, England, Netherlands, Piedmont, Portugal, Russia, Spain, Switzerland, Venice | damage | 6 | — | 52000 | 0 | 0 | 4800 | 0 | 0 | 15.62 |
| **Barracks 18c grenadier damage +6 (lvl 6)** `fraba2.grenadier.1.5` | France | damage | 6 | — | 52000 | 0 | 0 | 3800 | 0 | 0 | 15.62 |
| **Barracks 18c grenadier damage +6 (lvl 6)** `polba2.grenadier.1.5` | Poland | damage | 6 | — | 62000 | 0 | 0 | 4800 | 0 | 0 | 15.62 |
| **Barracks 18c grenadier damage +6 (lvl 6)** `sweba2.grenadier.1.5` | Sweden | damage | 6 | — | 54000 | 0 | 0 | 5800 | 0 | 0 | 15.62 |
| **Barracks 18c grenadier damage +1500 (lvl 7)** `ausba2.grenadier.1.6` | Austria, Netherlands, Piedmont, Portugal, Russia, Spain, Switzerland, Venice | damage | 1500 | — | 62000 | 0 | 0 | 15800 | 0 | 0 | 15.62 |
| **Barracks 18c grenadier damage +1500 (lvl 7)** `fraba2.grenadier.1.6` | France | damage | 1500 | — | 64010 | 0 | 0 | 15200 | 0 | 0 | 15.62 |
| **Barracks 18c grenadier damage +1500 (lvl 7)** `engba2.grenadier.1.6` | England | damage | 1500 | — | 60000 | 0 | 0 | 16000 | 0 | 0 | 15.62 |
| **Barracks 18c grenadier damage +1500 (lvl 7)** `polba2.grenadier.1.6` | Poland | damage | 1500 | — | 52000 | 0 | 0 | 15800 | 0 | 0 | 15.62 |
| **Barracks 18c grenadier damage +1500 (lvl 7)** `sweba2.grenadier.1.6` | Sweden | damage | 1500 | — | 60000 | 0 | 0 | 14590 | 0 | 0 | 15.62 |
| **Barracks 18c grenadier protection +1 (lvl 2)** `ausba2.grenadier.2.1` | Austria, Netherlands, Piedmont, Portugal, Russia, Spain, Switzerland, Venice | protection | 1 | — | 3706 | 0 | 0 | 350 | 0 | 0 | 15.62 |
| **Barracks 18c grenadier protection +1 (lvl 2)** `fraba2.grenadier.2.1` | France | protection | 1 | — | 3506 | 0 | 0 | 220 | 0 | 0 | 15.62 |
| **Barracks 18c grenadier protection +1 (lvl 2)** `engba2.grenadier.2.1` | England | protection | 1 | — | 3250 | 0 | 0 | 450 | 0 | 0 | 15.62 |
| **Barracks 18c grenadier protection +1 (lvl 2)** `polba2.grenadier.2.1` | Poland | protection | 1 | — | 4506 | 0 | 0 | 750 | 0 | 0 | 15.62 |
| **Barracks 18c grenadier protection +1 (lvl 2)** `sweba2.grenadier.2.1` | Sweden | protection | 1 | — | 7705 | 0 | 0 | 350 | 0 | 0 | 15.62 |
| **Barracks 18c grenadier protection +2 (lvl 3)** `ausba2.grenadier.2.2` | Austria, England, Netherlands, Piedmont, Portugal, Russia, Spain, Switzerland, Venice | protection | 2 | — | 11030 | 0 | 0 | 1350 | 0 | 0 | 15.62 |
| **Barracks 18c grenadier protection +2 (lvl 3)** `fraba2.grenadier.2.2` | France | protection | 2 | — | 11250 | 0 | 0 | 1450 | 0 | 0 | 15.62 |
| **Barracks 18c grenadier protection +2 (lvl 3)** `polba2.grenadier.2.2` | Poland | protection | 2 | — | 10130 | 0 | 0 | 950 | 0 | 0 | 15.62 |
| **Barracks 18c grenadier protection +2 (lvl 3)** `sweba2.grenadier.2.2` | Sweden | protection | 2 | — | 7030 | 0 | 0 | 1350 | 0 | 0 | 15.62 |
| **Barracks 18c grenadier protection +3 (lvl 4)** `ausba2.grenadier.2.3` | Austria, Netherlands, Piedmont, Portugal, Russia, Spain, Switzerland, Venice | protection | 3 | — | 35706 | 0 | 0 | 3000 | 0 | 0 | 15.62 |
| **Barracks 18c grenadier protection +3 (lvl 4)** `fraba2.grenadier.2.3` | France | protection | 3 | — | 37200 | 0 | 0 | 3300 | 0 | 0 | 15.62 |
| **Barracks 18c grenadier protection +3 (lvl 4)** `engba2.grenadier.2.3` | England | protection | 3 | — | 36200 | 0 | 0 | 2500 | 0 | 0 | 15.62 |
| **Barracks 18c grenadier protection +3 (lvl 4)** `polba2.grenadier.2.3` | Poland | protection | 3 | — | 25706 | 0 | 0 | 500 | 0 | 0 | 15.62 |
| **Barracks 18c grenadier protection +3 (lvl 4)** `sweba2.grenadier.2.3` | Sweden | protection | 3 | — | 21706 | 0 | 0 | 1000 | 0 | 0 | 15.62 |
| **Barracks 18c grenadier protection +1 (lvl 5)** `ausba2.grenadier.2.4` | Austria, Netherlands, Piedmont, Portugal, Russia, Spain, Switzerland, Venice | protection | 1 | — | 36556 | 0 | 0 | 3350 | 0 | 0 | 15.62 |
| **Barracks 18c grenadier protection +1 (lvl 5)** `fraba2.grenadier.2.4` | France | protection | 1 | — | 40400 | 0 | 0 | 3050 | 0 | 0 | 15.62 |
| **Barracks 18c grenadier protection +1 (lvl 5)** `engba2.grenadier.2.4` | England | protection | 1 | — | 16600 | 0 | 0 | 3650 | 0 | 0 | 15.62 |
| **Barracks 18c grenadier protection +1 (lvl 5)** `polba2.grenadier.2.4` | Poland | protection | 1 | — | 46556 | 0 | 0 | 1350 | 0 | 0 | 15.62 |
| **Barracks 18c grenadier protection +1 (lvl 5)** `sweba2.grenadier.2.4` | Sweden | protection | 1 | — | 22556 | 0 | 0 | 5350 | 0 | 0 | 15.62 |
| **Barracks 18c grenadier protection +2 (lvl 6)** `ausba2.grenadier.2.5` | Austria, Netherlands, Piedmont, Portugal, Russia, Spain, Switzerland, Venice | protection | 2 | — | 30060 | 0 | 0 | 1350 | 0 | 0 | 15.62 |
| **Barracks 18c grenadier protection +2 (lvl 6)** `fraba2.grenadier.2.5` | France | protection | 2 | — | 22060 | 0 | 0 | 350 | 0 | 0 | 15.62 |
| **Barracks 18c grenadier protection +2 (lvl 6)** `engba2.grenadier.2.5` | England | protection | 2 | — | 60060 | 0 | 0 | 1050 | 0 | 0 | 15.62 |
| **Barracks 18c grenadier protection +2 (lvl 6)** `polba2.grenadier.2.5` | Poland | protection | 2 | — | 50060 | 0 | 0 | 6050 | 0 | 0 | 15.62 |
| **Barracks 18c grenadier protection +2 (lvl 6)** `sweba2.grenadier.2.5` | Sweden | protection | 2 | — | 30060 | 0 | 0 | 1750 | 0 | 0 | 15.62 |
| **Barracks 18c grenadier protection +3 (lvl 7)** `ausba2.grenadier.2.6` | Austria, Netherlands, Piedmont, Portugal, Russia, Spain, Switzerland, Venice | protection | 3 | — | 64000 | 0 | 0 | 1350 | 0 | 0 | 15.62 |
| **Barracks 18c grenadier protection +3 (lvl 7)** `fraba2.grenadier.2.6` | France | protection | 3 | — | 63900 | 0 | 0 | 2350 | 0 | 0 | 15.62 |
| **Barracks 18c grenadier protection +3 (lvl 7)** `engba2.grenadier.2.6` | England | protection | 3 | — | 64000 | 0 | 0 | 1650 | 0 | 0 | 15.62 |
| **Barracks 18c grenadier protection +3 (lvl 7)** `polba2.grenadier.2.6` | Poland | protection | 3 | — | 44000 | 0 | 0 | 1650 | 0 | 0 | 15.62 |
| **Barracks 18c grenadier protection +3 (lvl 7)** `sweba2.grenadier.2.6` | Sweden | protection | 3 | — | 62000 | 0 | 0 | 950 | 0 | 0 | 15.62 |
| **Barracks 18c grenadierbav damage +2 (lvl 2)** `bavba2.grenadierbav.1.1` | Bavaria | damage | 2 | — | 1000 | 0 | 0 | 800 | 0 | 0 | 15.62 |
| **Barracks 18c grenadierbav damage +3 (lvl 3)** `bavba2.grenadierbav.1.2` | Bavaria | damage | 3 | — | 13000 | 0 | 0 | 2800 | 0 | 0 | 15.62 |
| **Barracks 18c grenadierbav damage +4 (lvl 4)** `bavba2.grenadierbav.1.3` | Bavaria | damage | 4 | — | 32000 | 0 | 0 | 1800 | 0 | 0 | 15.62 |
| **Barracks 18c grenadierbav damage +5 (lvl 5)** `bavba2.grenadierbav.1.4` | Bavaria | damage | 5 | — | 52000 | 0 | 0 | 4800 | 0 | 0 | 15.62 |
| **Barracks 18c grenadierbav damage +6 (lvl 6)** `bavba2.grenadierbav.1.5` | Bavaria | damage | 6 | — | 42000 | 0 | 0 | 3800 | 0 | 0 | 15.62 |
| **Barracks 18c grenadierbav damage +1500 (lvl 7)** `bavba2.grenadierbav.1.6` | Bavaria | damage | 1500 | — | 64000 | 0 | 0 | 14800 | 0 | 0 | 15.62 |
| **Barracks 18c grenadierbav protection +1 (lvl 2)** `bavba2.grenadierbav.2.1` | Bavaria | protection | 1 | — | 3205 | 0 | 0 | 375 | 0 | 0 | 15.62 |
| **Barracks 18c grenadierbav protection +2 (lvl 3)** `bavba2.grenadierbav.2.2` | Bavaria | protection | 2 | — | 11030 | 0 | 0 | 4350 | 0 | 0 | 15.62 |
| **Barracks 18c grenadierbav protection +3 (lvl 4)** `bavba2.grenadierbav.2.3` | Bavaria | protection | 3 | — | 36206 | 0 | 0 | 500 | 0 | 0 | 15.62 |
| **Barracks 18c grenadierbav protection +1 (lvl 5)** `bavba2.grenadierbav.2.4` | Bavaria | protection | 1 | — | 34950 | 0 | 0 | 1350 | 0 | 0 | 15.62 |
| **Barracks 18c grenadierbav protection +2 (lvl 6)** `bavba2.grenadierbav.2.5` | Bavaria | protection | 2 | — | 30060 | 0 | 0 | 2150 | 0 | 0 | 15.62 |
| **Barracks 18c grenadierbav protection +3 (lvl 7)** `bavba2.grenadierbav.2.6` | Bavaria | protection | 3 | — | 64000 | 0 | 0 | 2550 | 0 | 0 | 15.62 |
| **Barracks 18c grenadierden damage +3 (lvl 2)** `denba2.grenadierden.1.1` | Denmark | damage | 3 | — | 1000 | 0 | 0 | 800 | 0 | 0 | 15.62 |
| **Barracks 18c grenadierden damage +4 (lvl 3)** `denba2.grenadierden.1.2` | Denmark | damage | 4 | — | 13000 | 0 | 0 | 2800 | 0 | 0 | 15.62 |
| **Barracks 18c grenadierden damage +4 (lvl 4)** `denba2.grenadierden.1.3` | Denmark | damage | 4 | — | 32000 | 0 | 0 | 1800 | 0 | 0 | 15.62 |
| **Barracks 18c grenadierden damage +4 (lvl 5)** `denba2.grenadierden.1.4` | Denmark | damage | 4 | — | 52000 | 0 | 0 | 4800 | 0 | 0 | 15.62 |
| **Barracks 18c grenadierden damage +5 (lvl 6)** `denba2.grenadierden.1.5` | Denmark | damage | 5 | — | 42000 | 0 | 0 | 3800 | 0 | 0 | 15.62 |
| **Barracks 18c grenadierden damage +1500 (lvl 7)** `denba2.grenadierden.1.6` | Denmark | damage | 1500 | — | 64000 | 0 | 0 | 14800 | 0 | 0 | 15.62 |
| **Barracks 18c grenadierden protection +2 (lvl 2)** `denba2.grenadierden.2.1` | Denmark | protection | 2 | — | 3205 | 0 | 0 | 375 | 0 | 0 | 15.62 |
| **Barracks 18c grenadierden protection +3 (lvl 3)** `denba2.grenadierden.2.2` | Denmark | protection | 3 | — | 11030 | 0 | 0 | 4350 | 0 | 0 | 15.62 |
| **Barracks 18c grenadierden protection +3 (lvl 4)** `denba2.grenadierden.2.3` | Denmark | protection | 3 | — | 36206 | 0 | 0 | 500 | 0 | 0 | 15.62 |
| **Barracks 18c grenadierden protection +2 (lvl 5)** `denba2.grenadierden.2.4` | Denmark | protection | 2 | — | 34950 | 0 | 0 | 1350 | 0 | 0 | 15.62 |
| **Barracks 18c grenadierden protection +1 (lvl 6)** `denba2.grenadierden.2.5` | Denmark | protection | 1 | — | 30060 | 0 | 0 | 2150 | 0 | 0 | 15.62 |
| **Barracks 18c grenadierden protection +1 (lvl 7)** `denba2.grenadierden.2.6` | Denmark | protection | 1 | — | 64000 | 0 | 0 | 2550 | 0 | 0 | 15.62 |
| **Barracks 18c grenadierhun damage +6 (lvl 2)** `hunba2.grenadierhun.1.1` | Hungary | damage | 6 | — | 1000 | 0 | 0 | 800 | 0 | 0 | 15.62 |
| **Barracks 18c grenadierhun damage +5 (lvl 3)** `hunba2.grenadierhun.1.2` | Hungary | damage | 5 | — | 13000 | 0 | 0 | 1800 | 0 | 0 | 15.62 |
| **Barracks 18c grenadierhun damage +4 (lvl 4)** `hunba2.grenadierhun.1.3` | Hungary | damage | 4 | — | 25000 | 0 | 0 | 1800 | 0 | 0 | 15.62 |
| **Barracks 18c grenadierhun damage +3 (lvl 5)** `hunba2.grenadierhun.1.4` | Hungary | damage | 3 | — | 49000 | 0 | 0 | 4800 | 0 | 0 | 15.62 |
| **Barracks 18c grenadierhun damage +2 (lvl 6)** `hunba2.grenadierhun.1.5` | Hungary | damage | 2 | — | 54000 | 0 | 0 | 5800 | 0 | 0 | 15.62 |
| **Barracks 18c grenadierhun damage +1500 (lvl 7)** `hunba2.grenadierhun.1.6` | Hungary | damage | 1500 | — | 60000 | 0 | 0 | 14590 | 0 | 0 | 15.62 |
| **Barracks 18c grenadierhun protection +2 (lvl 2)** `hunba2.grenadierhun.2.1` | Hungary | protection | 2 | — | 7705 | 0 | 0 | 350 | 0 | 0 | 15.62 |
| **Barracks 18c grenadierhun protection +2 (lvl 3)** `hunba2.grenadierhun.2.2` | Hungary | protection | 2 | — | 7030 | 0 | 0 | 1350 | 0 | 0 | 15.62 |
| **Barracks 18c grenadierhun protection +2 (lvl 4)** `hunba2.grenadierhun.2.3` | Hungary | protection | 2 | — | 21706 | 0 | 0 | 1000 | 0 | 0 | 15.62 |
| **Barracks 18c grenadierhun protection +2 (lvl 5)** `hunba2.grenadierhun.2.4` | Hungary | protection | 2 | — | 22556 | 0 | 0 | 5350 | 0 | 0 | 15.62 |
| **Barracks 18c grenadierhun protection +2 (lvl 6)** `hunba2.grenadierhun.2.5` | Hungary | protection | 2 | — | 30060 | 0 | 0 | 1750 | 0 | 0 | 15.62 |
| **Barracks 18c grenadierhun protection +2 (lvl 7)** `hunba2.grenadierhun.2.6` | Hungary | protection | 2 | — | 62000 | 0 | 0 | 950 | 0 | 0 | 15.62 |
| **Barracks 18c grenadierpru damage +2 (lvl 2)** `pruba2.grenadierpru.1.1` | Prussia | damage | 2 | — | 1000 | 0 | 0 | 800 | 0 | 0 | 15.62 |
| **Barracks 18c grenadierpru damage +3 (lvl 3)** `pruba2.grenadierpru.1.2` | Prussia | damage | 3 | — | 13000 | 0 | 0 | 2800 | 0 | 0 | 15.62 |
| **Barracks 18c grenadierpru damage +4 (lvl 4)** `pruba2.grenadierpru.1.3` | Prussia | damage | 4 | — | 32000 | 0 | 0 | 1800 | 0 | 0 | 15.62 |
| **Barracks 18c grenadierpru damage +5 (lvl 5)** `pruba2.grenadierpru.1.4` | Prussia | damage | 5 | — | 52000 | 0 | 0 | 4800 | 0 | 0 | 15.62 |
| **Barracks 18c grenadierpru damage +6 (lvl 6)** `pruba2.grenadierpru.1.5` | Prussia | damage | 6 | — | 42000 | 0 | 0 | 3800 | 0 | 0 | 15.62 |
| **Barracks 18c grenadierpru damage +1500 (lvl 7)** `pruba2.grenadierpru.1.6` | Prussia | damage | 1500 | — | 64000 | 0 | 0 | 14800 | 0 | 0 | 15.62 |
| **Barracks 18c grenadierpru protection +1 (lvl 2)** `pruba2.grenadierpru.2.1` | Prussia | protection | 1 | — | 3205 | 0 | 0 | 375 | 0 | 0 | 15.62 |
| **Barracks 18c grenadierpru protection +2 (lvl 3)** `pruba2.grenadierpru.2.2` | Prussia | protection | 2 | — | 11030 | 0 | 0 | 4350 | 0 | 0 | 15.62 |
| **Barracks 18c grenadierpru protection +3 (lvl 4)** `pruba2.grenadierpru.2.3` | Prussia | protection | 3 | — | 36206 | 0 | 0 | 500 | 0 | 0 | 15.62 |
| **Barracks 18c grenadierpru protection +1 (lvl 5)** `pruba2.grenadierpru.2.4` | Prussia | protection | 1 | — | 34950 | 0 | 0 | 1350 | 0 | 0 | 15.62 |
| **Barracks 18c grenadierpru protection +2 (lvl 6)** `pruba2.grenadierpru.2.5` | Prussia | protection | 2 | — | 30060 | 0 | 0 | 2150 | 0 | 0 | 15.62 |
| **Barracks 18c grenadierpru protection +3 (lvl 7)** `pruba2.grenadierpru.2.6` | Prussia | protection | 3 | — | 64000 | 0 | 0 | 2550 | 0 | 0 | 15.62 |
| **Barracks 18c grenadiersax damage +2 (lvl 2)** `saxba2.grenadiersax.1.1` | Saxony | damage | 2 | — | 1000 | 0 | 0 | 800 | 0 | 0 | 15.62 |
| **Barracks 18c grenadiersax damage +3 (lvl 3)** `saxba2.grenadiersax.1.2` | Saxony | damage | 3 | — | 13000 | 0 | 0 | 1800 | 0 | 0 | 15.62 |
| **Barracks 18c grenadiersax damage +4 (lvl 4)** `saxba2.grenadiersax.1.3` | Saxony | damage | 4 | — | 25000 | 0 | 0 | 1800 | 0 | 0 | 15.62 |
| **Barracks 18c grenadiersax damage +5 (lvl 5)** `saxba2.grenadiersax.1.4` | Saxony | damage | 5 | — | 49000 | 0 | 0 | 4800 | 0 | 0 | 15.62 |
| **Barracks 18c grenadiersax damage +6 (lvl 6)** `saxba2.grenadiersax.1.5` | Saxony | damage | 6 | — | 54000 | 0 | 0 | 5800 | 0 | 0 | 15.62 |
| **Barracks 18c grenadiersax damage +1500 (lvl 7)** `saxba2.grenadiersax.1.6` | Saxony | damage | 1500 | — | 60000 | 0 | 0 | 14590 | 0 | 0 | 15.62 |
| **Barracks 18c grenadiersax protection +2 (lvl 2)** `saxba2.grenadiersax.2.1` | Saxony | protection | 2 | — | 7705 | 0 | 0 | 350 | 0 | 0 | 15.62 |
| **Barracks 18c grenadiersax protection +2 (lvl 3)** `saxba2.grenadiersax.2.2` | Saxony | protection | 2 | — | 7030 | 0 | 0 | 1350 | 0 | 0 | 15.62 |
| **Barracks 18c grenadiersax protection +2 (lvl 4)** `saxba2.grenadiersax.2.3` | Saxony | protection | 2 | — | 21706 | 0 | 0 | 1000 | 0 | 0 | 15.62 |
| **Barracks 18c grenadiersax protection +2 (lvl 5)** `saxba2.grenadiersax.2.4` | Saxony | protection | 2 | — | 22556 | 0 | 0 | 5350 | 0 | 0 | 15.62 |
| **Barracks 18c grenadiersax protection +2 (lvl 6)** `saxba2.grenadiersax.2.5` | Saxony | protection | 2 | — | 30060 | 0 | 0 | 1750 | 0 | 0 | 15.62 |
| **Barracks 18c grenadiersax protection +2 (lvl 7)** `saxba2.grenadiersax.2.6` | Saxony | protection | 2 | — | 62000 | 0 | 0 | 950 | 0 | 0 | 15.62 |
| **Barracks 18c highlander damage +1 (lvl 2)** `engba2.highlander.1.1` | England | damage | 1 | — | 4000 | 0 | 0 | 750 | 0 | 0 | 15.62 |
| **Barracks 18c highlander damage +2 (lvl 3)** `engba2.highlander.1.2` | England | damage | 2 | — | 3000 | 0 | 0 | 1100 | 0 | 0 | 15.62 |
| **Barracks 18c highlander damage +3 (lvl 4)** `engba2.highlander.1.3` | England | damage | 3 | — | 7500 | 0 | 0 | 1700 | 0 | 0 | 15.62 |
| **Barracks 18c highlander damage +1 (lvl 5)** `engba2.highlander.1.4` | England | damage | 1 | — | 11000 | 0 | 0 | 400 | 0 | 0 | 15.62 |
| **Barracks 18c highlander damage +1 (lvl 6)** `engba2.highlander.1.5` | England | damage | 1 | — | 27020 | 0 | 0 | 1150 | 0 | 0 | 15.62 |
| **Barracks 18c highlander damage +1 (lvl 7)** `engba2.highlander.1.6` | England | damage | 1 | — | 40200 | 0 | 0 | 1220 | 0 | 0 | 15.62 |
| **Barracks 18c highlander protection +2 (lvl 2)** `engba2.highlander.2.1` | England | protection | 2 | — | 3006 | 0 | 0 | 400 | 0 | 0 | 15.62 |
| **Barracks 18c highlander protection +2 (lvl 3)** `engba2.highlander.2.2` | England | protection | 2 | — | 10020 | 0 | 0 | 1550 | 0 | 0 | 15.62 |
| **Barracks 18c highlander protection +2 (lvl 4)** `engba2.highlander.2.3` | England | protection | 2 | — | 35706 | 0 | 0 | 1850 | 0 | 0 | 15.62 |
| `engba2.highlander.2.4` | England | +protection | 3 | — | 3600 | 0 | 0 | 600 | 0 | 0 | 15.62 |
| `engba2.highlander.2.5` | England | +protection | 3 | — | 5400 | 0 | 0 | 900 | 0 | 0 | 15.62 |
| `engba2.highlander.2.6` | England | +protection | 3 | — | 11250 | 0 | 0 | 1875 | 0 | 0 | 15.62 |
| **Barracks 18c jagerpor damage +1 (lvl 2)** `porba2.jagerpor.1.1` | Portugal | damage | 1 | — | 3000 | 0 | 0 | 750 | 0 | 0 | 15.62 |
| **Barracks 18c jagerpor damage +1 (lvl 3)** `porba2.jagerpor.1.2` | Portugal | damage | 1 | — | 4000 | 0 | 0 | 1100 | 0 | 0 | 15.62 |
| **Barracks 18c jagerpor damage +1 (lvl 4)** `porba2.jagerpor.1.3` | Portugal | damage | 1 | — | 7000 | 0 | 0 | 1800 | 0 | 0 | 15.62 |
| **Barracks 18c jagerpor damage +1 (lvl 5)** `porba2.jagerpor.1.4` | Portugal | damage | 1 | — | 12000 | 0 | 0 | 350 | 0 | 0 | 15.62 |
| **Barracks 18c jagerpor damage +1 (lvl 6)** `porba2.jagerpor.1.5` | Portugal | damage | 1 | — | 32020 | 0 | 0 | 850 | 0 | 0 | 15.62 |
| **Barracks 18c jagerpor damage +1 (lvl 7)** `porba2.jagerpor.1.6` | Portugal | damage | 1 | — | 45200 | 0 | 0 | 1330 | 0 | 0 | 15.62 |
| **Barracks 18c jagerpor protection +1 (lvl 2)** `porba2.jagerpor.2.1` | Portugal | protection | 1 | — | 3706 | 0 | 0 | 350 | 0 | 0 | 15.62 |
| **Barracks 18c jagerpor protection +1 (lvl 3)** `porba2.jagerpor.2.2` | Portugal | protection | 1 | — | 12060 | 0 | 0 | 1350 | 0 | 0 | 15.62 |
| **Barracks 18c jagerpor protection +1 (lvl 4)** `porba2.jagerpor.2.3` | Portugal | protection | 1 | — | 36706 | 0 | 0 | 2250 | 0 | 0 | 15.62 |
| **Barracks 18c jagerpor protection +1 (lvl 5)** `porba2.jagerpor.2.4` | Portugal | protection | 1 | — | 36706 | 0 | 0 | 3350 | 0 | 0 | 15.62 |
| **Barracks 18c jagerpor protection +1 (lvl 6)** `porba2.jagerpor.2.5` | Portugal | protection | 1 | — | 37060 | 0 | 0 | 1350 | 0 | 0 | 15.62 |
| **Barracks 18c jagerpor protection +1 (lvl 7)** `porba2.jagerpor.2.6` | Portugal | protection | 1 | — | 16706 | 0 | 0 | 1350 | 0 | 0 | 15.62 |
| **Barracks 18c jagerswi damage +3 (lvl 2)** `swiba2.jagerswi.1.1` | Switzerland | damage | 3 | — | 3000 | 0 | 0 | 750 | 0 | 0 | 15.62 |
| **Barracks 18c jagerswi damage +2 (lvl 3)** `swiba2.jagerswi.1.2` | Switzerland | damage | 2 | — | 4000 | 0 | 0 | 1100 | 0 | 0 | 15.62 |
| **Barracks 18c jagerswi damage +1 (lvl 4)** `swiba2.jagerswi.1.3` | Switzerland | damage | 1 | — | 7000 | 0 | 0 | 1800 | 0 | 0 | 15.62 |
| **Barracks 18c jagerswi damage +3 (lvl 5)** `swiba2.jagerswi.1.4` | Switzerland | damage | 3 | — | 12000 | 0 | 0 | 350 | 0 | 0 | 15.62 |
| **Barracks 18c jagerswi damage +2 (lvl 6)** `swiba2.jagerswi.1.5` | Switzerland | damage | 2 | — | 32020 | 0 | 0 | 850 | 0 | 0 | 15.62 |
| **Barracks 18c jagerswi damage +1 (lvl 7)** `swiba2.jagerswi.1.6` | Switzerland | damage | 1 | — | 45200 | 0 | 0 | 1330 | 0 | 0 | 15.62 |
| **Barracks 18c jagerswi protection +1 (lvl 2)** `swiba2.jagerswi.2.1` | Switzerland | protection | 1 | — | 3706 | 0 | 0 | 350 | 0 | 0 | 15.62 |
| **Barracks 18c jagerswi protection +1 (lvl 3)** `swiba2.jagerswi.2.2` | Switzerland | protection | 1 | — | 12060 | 0 | 0 | 1350 | 0 | 0 | 15.62 |
| **Barracks 18c jagerswi protection +1 (lvl 4)** `swiba2.jagerswi.2.3` | Switzerland | protection | 1 | — | 36706 | 0 | 0 | 2250 | 0 | 0 | 15.62 |
| **Barracks 18c jagerswi protection +1 (lvl 5)** `swiba2.jagerswi.2.4` | Switzerland | protection | 1 | — | 36706 | 0 | 0 | 3350 | 0 | 0 | 15.62 |
| **Barracks 18c jagerswi protection +1 (lvl 6)** `swiba2.jagerswi.2.5` | Switzerland | protection | 1 | — | 37060 | 0 | 0 | 1350 | 0 | 0 | 15.62 |
| **Barracks 18c jagerswi protection +1 (lvl 7)** `swiba2.jagerswi.2.6` | Switzerland | protection | 1 | — | 16706 | 0 | 0 | 1350 | 0 | 0 | 15.62 |
| **Barracks 18c musketeer18 damage +1 (lvl 2)** `ausba2.musketeer18.1.1` | Austria, Hungary, Piedmont, Portugal, Russia, Spain, Switzerland, Venice | damage | 1 | — | 1000 | 0 | 0 | 800 | 0 | 0 | 15.62 |
| **Barracks 18c musketeer18 damage +1 (lvl 2)** `fraba2.musketeer18.1.1` | France | damage | 1 | — | 500 | 0 | 0 | 200 | 0 | 0 | 15.62 |
| **Barracks 18c musketeer18 damage +1 (lvl 2)** `engba2.musketeer18.1.1` | England | damage | 1 | — | 1100 | 0 | 0 | 750 | 0 | 0 | 15.62 |
| **Barracks 18c musketeer18 damage +1 (lvl 2)** `polba2.musketeer18.1.1` | Poland | damage | 1 | — | 1000 | 0 | 0 | 100 | 0 | 0 | 15.62 |
| **Barracks 18c musketeer18 damage +1 (lvl 2)** `sweba2.musketeer18.1.1` | Sweden | damage | 1 | — | 9000 | 0 | 0 | 200 | 0 | 0 | 15.62 |
| **Barracks 18c musketeer18 damage +1 (lvl 2)** `netba2.musketeer18.1.1` | Netherlands | damage | 1 | — | 900 | 0 | 0 | 100 | 0 | 0 | 15.62 |
| **Barracks 18c musketeer18 damage +1 (lvl 3)** `ausba2.musketeer18.1.2` | Austria, Hungary, Piedmont, Portugal, Russia, Spain, Switzerland, Venice | damage | 1 | — | 1500 | 0 | 0 | 800 | 0 | 0 | 15.62 |
| **Barracks 18c musketeer18 damage +1 (lvl 3)** `fraba2.musketeer18.1.2` | France | damage | 1 | — | 2000 | 0 | 0 | 400 | 0 | 0 | 15.62 |
| **Barracks 18c musketeer18 damage +1 (lvl 3)** `engba2.musketeer18.1.2` | England | damage | 1 | — | 1670 | 0 | 0 | 850 | 0 | 0 | 15.62 |
| **Barracks 18c musketeer18 damage +1 (lvl 3)** `polba2.musketeer18.1.2` | Poland | damage | 1 | — | 2500 | 0 | 0 | 200 | 0 | 0 | 15.62 |
| **Barracks 18c musketeer18 damage +1 (lvl 3)** `sweba2.musketeer18.1.2` | Sweden | damage | 1 | — | 600 | 0 | 0 | 200 | 0 | 0 | 15.62 |
| **Barracks 18c musketeer18 damage +1 (lvl 3)** `netba2.musketeer18.1.2` | Netherlands | damage | 1 | — | 1600 | 0 | 0 | 200 | 0 | 0 | 15.62 |
| **Barracks 18c musketeer18 damage +2 (lvl 4)** `ausba2.musketeer18.1.3` | Austria, Hungary, Piedmont, Portugal, Russia, Spain, Switzerland, Venice | damage | 2 | — | 2000 | 0 | 0 | 800 | 0 | 0 | 15.62 |
| **Barracks 18c musketeer18 damage +2 (lvl 4)** `fraba2.musketeer18.1.3` | France | damage | 2 | — | 1200 | 0 | 0 | 1800 | 0 | 0 | 15.62 |
| **Barracks 18c musketeer18 damage +2 (lvl 4)** `engba2.musketeer18.1.3` | England | damage | 2 | — | 1900 | 0 | 0 | 200 | 0 | 0 | 15.62 |
| **Barracks 18c musketeer18 damage +2 (lvl 4)** `polba2.musketeer18.1.3` | Poland | damage | 2 | — | 1000 | 0 | 0 | 300 | 0 | 0 | 15.62 |
| **Barracks 18c musketeer18 damage +2 (lvl 4)** `sweba2.musketeer18.1.3` | Sweden | damage | 2 | — | 4000 | 0 | 0 | 100 | 0 | 0 | 15.62 |
| **Barracks 18c musketeer18 damage +2 (lvl 4)** `netba2.musketeer18.1.3` | Netherlands | damage | 2 | — | 1500 | 0 | 0 | 300 | 0 | 0 | 15.62 |
| **Barracks 18c musketeer18 damage +2 (lvl 5)** `ausba2.musketeer18.1.4` | Austria, Hungary, Piedmont, Portugal, Russia, Spain, Switzerland, Venice | damage | 2 | — | 2500 | 0 | 0 | 800 | 0 | 0 | 15.62 |
| **Barracks 18c musketeer18 damage +2 (lvl 5)** `fraba2.musketeer18.1.4` | France | damage | 2 | — | 3300 | 0 | 0 | 100 | 0 | 0 | 15.62 |
| **Barracks 18c musketeer18 damage +2 (lvl 5)** `engba2.musketeer18.1.4` | England | damage | 2 | — | 2340 | 0 | 0 | 1800 | 0 | 0 | 15.62 |
| **Barracks 18c musketeer18 damage +2 (lvl 5)** `polba2.musketeer18.1.4` | Poland | damage | 2 | — | 3500 | 0 | 0 | 400 | 0 | 0 | 15.62 |
| **Barracks 18c musketeer18 damage +2 (lvl 5)** `sweba2.musketeer18.1.4` | Sweden | damage | 2 | — | 500 | 0 | 0 | 2100 | 0 | 0 | 15.62 |
| **Barracks 18c musketeer18 damage +2 (lvl 5)** `netba2.musketeer18.1.4` | Netherlands | damage | 2 | — | 3100 | 0 | 0 | 2600 | 0 | 0 | 15.62 |
| **Barracks 18c musketeer18 damage +3 (lvl 6)** `ausba2.musketeer18.1.5` | Austria, Hungary, Piedmont, Portugal, Russia, Spain, Switzerland, Venice | damage | 3 | — | 3000 | 0 | 0 | 800 | 0 | 0 | 15.62 |
| **Barracks 18c musketeer18 damage +3 (lvl 6)** `fraba2.musketeer18.1.5` | France | damage | 3 | — | 1100 | 0 | 0 | 200 | 0 | 0 | 15.62 |
| **Barracks 18c musketeer18 damage +3 (lvl 6)** `engba2.musketeer18.1.5` | England | damage | 3 | — | 3000 | 0 | 0 | 900 | 0 | 0 | 15.62 |
| **Barracks 18c musketeer18 damage +3 (lvl 6)** `polba2.musketeer18.1.5` | Poland | damage | 3 | — | 2000 | 0 | 0 | 3800 | 0 | 0 | 15.62 |
| **Barracks 18c musketeer18 damage +3 (lvl 6)** `sweba2.musketeer18.1.5` | Sweden | damage | 3 | — | 3000 | 0 | 0 | 200 | 0 | 0 | 15.62 |
| **Barracks 18c musketeer18 damage +3 (lvl 6)** `netba2.musketeer18.1.5` | Netherlands | damage | 3 | — | 2900 | 0 | 0 | 200 | 0 | 0 | 15.62 |
| **Barracks 18c musketeer18 damage +3 (lvl 7)** `ausba2.musketeer18.1.6` | Austria, Hungary, Piedmont, Portugal, Russia, Spain, Switzerland, Venice | damage | 3 | — | 3500 | 0 | 0 | 800 | 0 | 0 | 15.62 |
| **Barracks 18c musketeer18 damage +3 (lvl 7)** `fraba2.musketeer18.1.6` | France | damage | 3 | — | 5500 | 0 | 0 | 2100 | 0 | 0 | 15.62 |
| **Barracks 18c musketeer18 damage +3 (lvl 7)** `engba2.musketeer18.1.6` | England | damage | 3 | — | 3500 | 0 | 0 | 700 | 0 | 0 | 15.62 |
| **Barracks 18c musketeer18 damage +3 (lvl 7)** `polba2.musketeer18.1.6` | Poland | damage | 3 | — | 3500 | 0 | 0 | 600 | 0 | 0 | 15.62 |
| **Barracks 18c musketeer18 damage +3 (lvl 7)** `sweba2.musketeer18.1.6` | Sweden | damage | 3 | — | 3500 | 0 | 0 | 1400 | 0 | 0 | 15.62 |
| **Barracks 18c musketeer18 damage +3 (lvl 7)** `netba2.musketeer18.1.6` | Netherlands | damage | 3 | — | 3200 | 0 | 0 | 1400 | 0 | 0 | 15.62 |
| **Barracks 18c musketeer18 protection +1 (lvl 2)** `ausba2.musketeer18.2.1` | Austria, Hungary, Piedmont, Portugal, Russia, Spain, Switzerland, Venice | protection | 1 | — | 3706 | 0 | 0 | 350 | 0 | 0 | 15.62 |
| **Barracks 18c musketeer18 protection +1 (lvl 2)** `fraba2.musketeer18.2.1` | France | protection | 1 | — | 3500 | 0 | 0 | 370 | 0 | 0 | 15.62 |
| **Barracks 18c musketeer18 protection +1 (lvl 2)** `engba2.musketeer18.2.1` | England | protection | 1 | — | 3750 | 0 | 0 | 370 | 0 | 0 | 15.62 |
| **Barracks 18c musketeer18 protection +1 (lvl 2)** `polba2.musketeer18.2.1` | Poland | protection | 1 | — | 5706 | 0 | 0 | 350 | 0 | 0 | 15.62 |
| **Barracks 18c musketeer18 protection +1 (lvl 2)** `sweba2.musketeer18.2.1` | Sweden | protection | 1 | — | 5706 | 0 | 0 | 750 | 0 | 0 | 15.62 |
| **Barracks 18c musketeer18 protection +1 (lvl 2)** `netba2.musketeer18.2.1` | Netherlands | protection | 1 | — | 3906 | 0 | 0 | 350 | 0 | 0 | 15.62 |
| **Barracks 18c musketeer18 protection +2 (lvl 3)** `ausba2.musketeer18.2.2` | Austria, Hungary, Piedmont, Portugal, Russia, Spain, Switzerland, Venice | protection | 2 | — | 11030 | 0 | 0 | 1350 | 0 | 0 | 15.62 |
| **Barracks 18c musketeer18 protection +2 (lvl 3)** `fraba2.musketeer18.2.2` | France | protection | 2 | — | 35030 | 0 | 0 | 1050 | 0 | 0 | 15.62 |
| **Barracks 18c musketeer18 protection +2 (lvl 3)** `engba2.musketeer18.2.2` | England | protection | 2 | — | 10020 | 0 | 0 | 1450 | 0 | 0 | 15.62 |
| **Barracks 18c musketeer18 protection +2 (lvl 3)** `polba2.musketeer18.2.2` | Poland | protection | 2 | — | 9030 | 0 | 0 | 4350 | 0 | 0 | 15.62 |
| **Barracks 18c musketeer18 protection +2 (lvl 3)** `sweba2.musketeer18.2.2` | Sweden | protection | 2 | — | 9030 | 0 | 0 | 1050 | 0 | 0 | 15.62 |
| **Barracks 18c musketeer18 protection +2 (lvl 3)** `netba2.musketeer18.2.2` | Netherlands | protection | 2 | — | 9030 | 0 | 0 | 1150 | 0 | 0 | 15.62 |
| **Barracks 18c musketeer18 protection +2 (lvl 4)** `ausba2.musketeer18.2.3` | Austria, Hungary, Piedmont, Portugal, Russia, Spain, Switzerland, Venice | protection | 2 | — | 35706 | 0 | 0 | 4000 | 0 | 0 | 15.62 |
| **Barracks 18c musketeer18 protection +2 (lvl 4)** `fraba2.musketeer18.2.3` | France | protection | 2 | — | 11706 | 0 | 0 | 4300 | 0 | 0 | 15.62 |
| **Barracks 18c musketeer18 protection +2 (lvl 4)** `engba2.musketeer18.2.3` | England | protection | 2 | — | 34200 | 0 | 0 | 3850 | 0 | 0 | 15.62 |
| **Barracks 18c musketeer18 protection +2 (lvl 4)** `polba2.musketeer18.2.3` | Poland | protection | 2 | — | 32706 | 0 | 0 | 1000 | 0 | 0 | 15.62 |
| **Barracks 18c musketeer18 protection +2 (lvl 4)** `sweba2.musketeer18.2.3` | Sweden | protection | 2 | — | 32706 | 0 | 0 | 2900 | 0 | 0 | 15.62 |
| **Barracks 18c musketeer18 protection +2 (lvl 4)** `netba2.musketeer18.2.3` | Netherlands | protection | 2 | — | 37706 | 0 | 0 | 4200 | 0 | 0 | 15.62 |
| **Barracks 18c musketeer18 protection +1 (lvl 5)** `ausba2.musketeer18.2.4` | Austria, Hungary, Piedmont, Portugal, Russia, Spain, Switzerland, Venice | protection | 1 | — | 36556 | 0 | 0 | 4350 | 0 | 0 | 15.62 |
| **Barracks 18c musketeer18 protection +1 (lvl 5)** `fraba2.musketeer18.2.4` | France | protection | 1 | — | 36700 | 0 | 0 | 4450 | 0 | 0 | 15.62 |
| **Barracks 18c musketeer18 protection +1 (lvl 5)** `engba2.musketeer18.2.4` | England | protection | 1 | — | 35000 | 0 | 0 | 2350 | 0 | 0 | 15.62 |
| **Barracks 18c musketeer18 protection +1 (lvl 5)** `polba2.musketeer18.2.4` | Poland | protection | 1 | — | 39556 | 0 | 0 | 2350 | 0 | 0 | 15.62 |
| **Barracks 18c musketeer18 protection +1 (lvl 5)** `sweba2.musketeer18.2.4` | Sweden | protection | 1 | — | 39556 | 0 | 0 | 5450 | 0 | 0 | 15.62 |
| **Barracks 18c musketeer18 protection +1 (lvl 5)** `netba2.musketeer18.2.4` | Netherlands | protection | 1 | — | 32556 | 0 | 0 | 3350 | 0 | 0 | 15.62 |
| **Barracks 18c musketeer18 protection +2 (lvl 6)** `ausba2.musketeer18.2.5` | Austria, Hungary, Piedmont, Portugal, Russia, Spain, Sweden, Switzerland, Venice | protection | 2 | — | 30060 | 0 | 0 | 1350 | 0 | 0 | 15.62 |
| **Barracks 18c musketeer18 protection +2 (lvl 6)** `fraba2.musketeer18.2.5` | France | protection | 2 | — | 30160 | 0 | 0 | 1550 | 0 | 0 | 15.62 |
| **Barracks 18c musketeer18 protection +2 (lvl 6)** `engba2.musketeer18.2.5` | England | protection | 2 | — | 31250 | 0 | 0 | 3350 | 0 | 0 | 15.62 |
| **Barracks 18c musketeer18 protection +2 (lvl 6)** `polba2.musketeer18.2.5` | Poland | protection | 2 | — | 27060 | 0 | 0 | 3350 | 0 | 0 | 15.62 |
| **Barracks 18c musketeer18 protection +2 (lvl 6)** `netba2.musketeer18.2.5` | Netherlands | protection | 2 | — | 34060 | 0 | 0 | 2350 | 0 | 0 | 15.62 |
| **Barracks 18c musketeer18 protection +2 (lvl 7)** `ausba2.musketeer18.2.6` | Austria, Hungary, Piedmont, Portugal, Russia, Spain, Sweden, Switzerland, Venice | protection | 2 | — | 37600 | 0 | 0 | 1350 | 0 | 0 | 15.62 |
| **Barracks 18c musketeer18 protection +2 (lvl 7)** `fraba2.musketeer18.2.6` | France | protection | 2 | — | 33600 | 0 | 0 | 1150 | 0 | 0 | 15.62 |
| **Barracks 18c musketeer18 protection +2 (lvl 7)** `engba2.musketeer18.2.6` | England | protection | 2 | — | 30570 | 0 | 0 | 1450 | 0 | 0 | 15.62 |
| **Barracks 18c musketeer18 protection +2 (lvl 7)** `polba2.musketeer18.2.6` | Poland | protection | 2 | — | 40600 | 0 | 0 | 1550 | 0 | 0 | 15.62 |
| **Barracks 18c musketeer18 protection +2 (lvl 7)** `netba2.musketeer18.2.6` | Netherlands | protection | 2 | — | 36500 | 0 | 0 | 1550 | 0 | 0 | 15.62 |
| **Barracks 18c musketeer18bav damage +1 (lvl 2)** `bavba2.musketeer18bav.1.1` | Bavaria | damage | 1 | — | 900 | 0 | 0 | 700 | 0 | 0 | 15.62 |
| **Barracks 18c musketeer18bav damage +1 (lvl 3)** `bavba2.musketeer18bav.1.2` | Bavaria | damage | 1 | — | 1600 | 0 | 0 | 800 | 0 | 0 | 15.62 |
| **Barracks 18c musketeer18bav damage +1 (lvl 4)** `bavba2.musketeer18bav.1.3` | Bavaria | damage | 1 | — | 2500 | 0 | 0 | 900 | 0 | 0 | 15.62 |
| **Barracks 18c musketeer18bav damage +1 (lvl 5)** `bavba2.musketeer18bav.1.4` | Bavaria | damage | 1 | — | 2000 | 0 | 0 | 600 | 0 | 0 | 15.62 |
| **Barracks 18c musketeer18bav damage +1 (lvl 6)** `bavba2.musketeer18bav.1.5` | Bavaria | damage | 1 | — | 3500 | 0 | 0 | 1000 | 0 | 0 | 15.62 |
| **Barracks 18c musketeer18bav damage +1 (lvl 7)** `bavba2.musketeer18bav.1.6` | Bavaria | damage | 1 | — | 3000 | 0 | 0 | 800 | 0 | 0 | 15.62 |
| **Barracks 18c musketeer18bav protection +1 (lvl 2)** `bavba2.musketeer18bav.2.1` | Bavaria | protection | 1 | — | 3500 | 0 | 0 | 350 | 0 | 0 | 15.62 |
| **Barracks 18c musketeer18bav protection +1 (lvl 3)** `bavba2.musketeer18bav.2.2` | Bavaria | protection | 1 | — | 11230 | 0 | 0 | 1350 | 0 | 0 | 15.62 |
| **Barracks 18c musketeer18bav protection +1 (lvl 4)** `bavba2.musketeer18bav.2.3` | Bavaria | protection | 1 | — | 35706 | 0 | 0 | 4000 | 0 | 0 | 15.62 |
| **Barracks 18c musketeer18bav protection +2 (lvl 5)** `bavba2.musketeer18bav.2.4` | Bavaria | protection | 2 | — | 36556 | 0 | 0 | 4350 | 0 | 0 | 15.62 |
| **Barracks 18c musketeer18bav protection +2 (lvl 6)** `bavba2.musketeer18bav.2.5` | Bavaria | protection | 2 | — | 30060 | 0 | 0 | 1350 | 0 | 0 | 15.62 |
| **Barracks 18c musketeer18bav protection +3 (lvl 7)** `bavba2.musketeer18bav.2.6` | Bavaria | protection | 3 | — | 37600 | 0 | 0 | 1350 | 0 | 0 | 15.62 |
| **Barracks 18c musketeer18den damage +1 (lvl 2)** `denba2.musketeer18den.1.1` | Denmark | damage | 1 | — | 900 | 0 | 0 | 700 | 0 | 0 | 15.62 |
| **Barracks 18c musketeer18den damage +1 (lvl 3)** `denba2.musketeer18den.1.2` | Denmark | damage | 1 | — | 1600 | 0 | 0 | 800 | 0 | 0 | 15.62 |
| **Barracks 18c musketeer18den damage +1 (lvl 4)** `denba2.musketeer18den.1.3` | Denmark | damage | 1 | — | 2500 | 0 | 0 | 900 | 0 | 0 | 15.62 |
| **Barracks 18c musketeer18den damage +1 (lvl 5)** `denba2.musketeer18den.1.4` | Denmark | damage | 1 | — | 2000 | 0 | 0 | 600 | 0 | 0 | 15.62 |
| **Barracks 18c musketeer18den damage +1 (lvl 6)** `denba2.musketeer18den.1.5` | Denmark | damage | 1 | — | 3500 | 0 | 0 | 1000 | 0 | 0 | 15.62 |
| **Barracks 18c musketeer18den damage +1 (lvl 7)** `denba2.musketeer18den.1.6` | Denmark | damage | 1 | — | 3000 | 0 | 0 | 800 | 0 | 0 | 15.62 |
| **Barracks 18c musketeer18den protection +1 (lvl 2)** `denba2.musketeer18den.2.1` | Denmark | protection | 1 | — | 3500 | 0 | 0 | 350 | 0 | 0 | 15.62 |
| **Barracks 18c musketeer18den protection +1 (lvl 3)** `denba2.musketeer18den.2.2` | Denmark | protection | 1 | — | 11230 | 0 | 0 | 1350 | 0 | 0 | 15.62 |
| **Barracks 18c musketeer18den protection +1 (lvl 4)** `denba2.musketeer18den.2.3` | Denmark | protection | 1 | — | 35706 | 0 | 0 | 4000 | 0 | 0 | 15.62 |
| **Barracks 18c musketeer18den protection +2 (lvl 5)** `denba2.musketeer18den.2.4` | Denmark | protection | 2 | — | 36556 | 0 | 0 | 4350 | 0 | 0 | 15.62 |
| **Barracks 18c musketeer18den protection +2 (lvl 6)** `denba2.musketeer18den.2.5` | Denmark | protection | 2 | — | 30060 | 0 | 0 | 1350 | 0 | 0 | 15.62 |
| **Barracks 18c musketeer18den protection +3 (lvl 7)** `denba2.musketeer18den.2.6` | Denmark | protection | 3 | — | 37600 | 0 | 0 | 1350 | 0 | 0 | 15.62 |
| **Barracks 18c musketeer18pru damage +1 (lvl 2)** `pruba2.musketeer18pru.1.1` | Prussia | damage | 1 | — | 900 | 0 | 0 | 700 | 0 | 0 | 15.62 |
| **Barracks 18c musketeer18pru damage +1 (lvl 3)** `pruba2.musketeer18pru.1.2` | Prussia | damage | 1 | — | 1600 | 0 | 0 | 800 | 0 | 0 | 15.62 |
| **Barracks 18c musketeer18pru damage +2 (lvl 4)** `pruba2.musketeer18pru.1.3` | Prussia | damage | 2 | — | 2500 | 0 | 0 | 900 | 0 | 0 | 15.62 |
| **Barracks 18c musketeer18pru damage +2 (lvl 5)** `pruba2.musketeer18pru.1.4` | Prussia | damage | 2 | — | 2000 | 0 | 0 | 600 | 0 | 0 | 15.62 |
| **Barracks 18c musketeer18pru damage +3 (lvl 6)** `pruba2.musketeer18pru.1.5` | Prussia | damage | 3 | — | 3500 | 0 | 0 | 1000 | 0 | 0 | 15.62 |
| **Barracks 18c musketeer18pru damage +3 (lvl 7)** `pruba2.musketeer18pru.1.6` | Prussia | damage | 3 | — | 3000 | 0 | 0 | 800 | 0 | 0 | 15.62 |
| **Barracks 18c musketeer18pru protection +1 (lvl 2)** `pruba2.musketeer18pru.2.1` | Prussia | protection | 1 | — | 3500 | 0 | 0 | 350 | 0 | 0 | 15.62 |
| **Barracks 18c musketeer18pru protection +2 (lvl 3)** `pruba2.musketeer18pru.2.2` | Prussia | protection | 2 | — | 11230 | 0 | 0 | 1350 | 0 | 0 | 15.62 |
| **Barracks 18c musketeer18pru protection +2 (lvl 4)** `pruba2.musketeer18pru.2.3` | Prussia | protection | 2 | — | 35706 | 0 | 0 | 4000 | 0 | 0 | 15.62 |
| **Barracks 18c musketeer18pru protection +1 (lvl 5)** `pruba2.musketeer18pru.2.4` | Prussia | protection | 1 | — | 36556 | 0 | 0 | 4350 | 0 | 0 | 15.62 |
| **Barracks 18c musketeer18pru protection +2 (lvl 6)** `pruba2.musketeer18pru.2.5` | Prussia | protection | 2 | — | 30060 | 0 | 0 | 1350 | 0 | 0 | 15.62 |
| **Barracks 18c musketeer18pru protection +2 (lvl 7)** `pruba2.musketeer18pru.2.6` | Prussia | protection | 2 | — | 37600 | 0 | 0 | 1350 | 0 | 0 | 15.62 |
| **Barracks 18c musketeer18sax damage +1 (lvl 2)** `saxba2.musketeer18sax.1.1` | Saxony | damage | 1 | — | 9000 | 0 | 0 | 200 | 0 | 0 | 15.62 |
| **Barracks 18c musketeer18sax damage +2 (lvl 3)** `saxba2.musketeer18sax.1.2` | Saxony | damage | 2 | — | 600 | 0 | 0 | 200 | 0 | 0 | 15.62 |
| **Barracks 18c musketeer18sax damage +2 (lvl 4)** `saxba2.musketeer18sax.1.3` | Saxony | damage | 2 | — | 4000 | 0 | 0 | 100 | 0 | 0 | 15.62 |
| **Barracks 18c musketeer18sax damage +1 (lvl 5)** `saxba2.musketeer18sax.1.4` | Saxony | damage | 1 | — | 500 | 0 | 0 | 2100 | 0 | 0 | 15.62 |
| **Barracks 18c musketeer18sax damage +2 (lvl 6)** `saxba2.musketeer18sax.1.5` | Saxony | damage | 2 | — | 3000 | 0 | 0 | 200 | 0 | 0 | 15.62 |
| **Barracks 18c musketeer18sax damage +2 (lvl 7)** `saxba2.musketeer18sax.1.6` | Saxony | damage | 2 | — | 3500 | 0 | 0 | 1400 | 0 | 0 | 15.62 |
| **Barracks 18c musketeer18sax protection +1 (lvl 2)** `saxba2.musketeer18sax.2.1` | Saxony | protection | 1 | — | 5706 | 0 | 0 | 750 | 0 | 0 | 15.62 |
| **Barracks 18c musketeer18sax protection +2 (lvl 3)** `saxba2.musketeer18sax.2.2` | Saxony | protection | 2 | — | 9030 | 0 | 0 | 1050 | 0 | 0 | 15.62 |
| **Barracks 18c musketeer18sax protection +2 (lvl 4)** `saxba2.musketeer18sax.2.3` | Saxony | protection | 2 | — | 32706 | 0 | 0 | 2900 | 0 | 0 | 15.62 |
| **Barracks 18c musketeer18sax protection +1 (lvl 5)** `saxba2.musketeer18sax.2.4` | Saxony | protection | 1 | — | 39556 | 0 | 0 | 5450 | 0 | 0 | 15.62 |
| **Barracks 18c musketeer18sax protection +2 (lvl 6)** `saxba2.musketeer18sax.2.5` | Saxony | protection | 2 | — | 30060 | 0 | 0 | 1350 | 0 | 0 | 15.62 |
| **Barracks 18c musketeer18sax protection +2 (lvl 7)** `saxba2.musketeer18sax.2.6` | Saxony | protection | 2 | — | 37600 | 0 | 0 | 1350 | 0 | 0 | 15.62 |
| **Barracks 18c officer18 damage +30 (lvl 2)** `ausba2.officer18.1.1` | Austria, Piedmont, Russia, Spain, Switzerland, Venice | damage | 30 | — | 1000 | 0 | 0 | 800 | 0 | 0 | 15.62 |
| **Barracks 18c officer18 damage +30 (lvl 2)** `pruba2.officer18.1.1` | Denmark, Hungary, Prussia, Saxony | damage | 30 | — | 1200 | 0 | 0 | 750 | 0 | 0 | 15.62 |
| **Barracks 18c officer18 damage +30 (lvl 2)** `sweba2.officer18.1.1` | Bavaria, Portugal, Sweden | damage | 30 | — | 200 | 0 | 0 | 910 | 0 | 0 | 15.62 |
| **Barracks 18c officer18 damage +30 (lvl 2)** `fraba2.officer18.1.1` | France | damage | 30 | — | 1200 | 0 | 0 | 700 | 0 | 0 | 15.62 |
| **Barracks 18c officer18 damage +30 (lvl 2)** `engba2.officer18.1.1` | England | damage | 30 | — | 800 | 0 | 0 | 950 | 0 | 0 | 15.62 |
| **Barracks 18c officer18 damage +30 (lvl 2)** `polba2.officer18.1.1` | Poland | damage | 30 | — | 2000 | 0 | 0 | 200 | 0 | 0 | 15.62 |
| **Barracks 18c officer18 damage +30 (lvl 2)** `netba2.officer18.1.1` | Netherlands | damage | 30 | — | 900 | 0 | 0 | 775 | 0 | 0 | 15.62 |
| **Barracks 18c officer18 protection +12 (lvl 2)** `ausba2.officer18.2.1` | Austria, Piedmont, Russia, Spain, Switzerland, Venice | protection | 12 | — | 1706 | 0 | 0 | 350 | 0 | 0 | 15.62 |
| **Barracks 18c officer18 protection +12 (lvl 2)** `pruba2.officer18.2.1` | Denmark, Hungary, Prussia, Saxony | protection | 12 | — | 1500 | 0 | 0 | 375 | 0 | 0 | 15.62 |
| **Barracks 18c officer18 protection +12 (lvl 2)** `sweba2.officer18.2.1` | Bavaria, Portugal, Sweden | protection | 12 | — | 305 | 0 | 0 | 950 | 0 | 0 | 15.62 |
| **Barracks 18c officer18 protection +12 (lvl 2)** `fraba2.officer18.2.1` | France | protection | 12 | — | 2105 | 0 | 0 | 450 | 0 | 0 | 15.62 |
| **Barracks 18c officer18 protection +12 (lvl 2)** `engba2.officer18.2.1` | England | protection | 12 | — | 2105 | 0 | 0 | 300 | 0 | 0 | 15.62 |
| **Barracks 18c officer18 protection +12 (lvl 2)** `polba2.officer18.2.1` | Poland | protection | 12 | — | 605 | 0 | 0 | 950 | 0 | 0 | 15.62 |
| **Barracks 18c officer18 protection +12 (lvl 2)** `netba2.officer18.2.1` | Netherlands | protection | 12 | — | 1606 | 0 | 0 | 650 | 0 | 0 | 15.62 |
| **Barracks 18c pandur damage +1 (lvl 2)** `ausba2.pandur.1.1` | Austria | damage | 1 | — | 3000 | 0 | 0 | 750 | 0 | 0 | 15.62 |
| **Barracks 18c pandur damage +1 (lvl 3)** `ausba2.pandur.1.2` | Austria | damage | 1 | — | 4000 | 0 | 0 | 1100 | 0 | 0 | 15.62 |
| **Barracks 18c pandur damage +2 (lvl 4)** `ausba2.pandur.1.3` | Austria | damage | 2 | — | 7000 | 0 | 0 | 1800 | 0 | 0 | 15.62 |
| **Barracks 18c pandur damage +1 (lvl 5)** `ausba2.pandur.1.4` | Austria | damage | 1 | — | 12000 | 0 | 0 | 350 | 0 | 0 | 15.62 |
| **Barracks 18c pandur damage +1 (lvl 6)** `ausba2.pandur.1.5` | Austria | damage | 1 | — | 32020 | 0 | 0 | 850 | 0 | 0 | 15.62 |
| **Barracks 18c pandur damage +2 (lvl 7)** `ausba2.pandur.1.6` | Austria | damage | 2 | — | 45200 | 0 | 0 | 1330 | 0 | 0 | 15.62 |
| **Barracks 18c pandur protection +1 (lvl 2)** `ausba2.pandur.2.1` | Austria | protection | 1 | — | 3706 | 0 | 0 | 350 | 0 | 0 | 15.62 |
| **Barracks 18c pandur protection +2 (lvl 3)** `ausba2.pandur.2.2` | Austria | protection | 2 | — | 12060 | 0 | 0 | 1350 | 0 | 0 | 15.62 |
| **Barracks 18c pandur protection +2 (lvl 4)** `ausba2.pandur.2.3` | Austria | protection | 2 | — | 36706 | 0 | 0 | 2250 | 0 | 0 | 15.62 |
| **Barracks 18c pandur protection +1 (lvl 5)** `ausba2.pandur.2.4` | Austria | protection | 1 | — | 36706 | 0 | 0 | 3350 | 0 | 0 | 15.62 |
| **Barracks 18c pandur protection +2 (lvl 6)** `ausba2.pandur.2.5` | Austria | protection | 2 | — | 37060 | 0 | 0 | 1350 | 0 | 0 | 15.62 |
| **Barracks 18c pandur protection +2 (lvl 7)** `ausba2.pandur.2.6` | Austria | protection | 2 | — | 16706 | 0 | 0 | 1350 | 0 | 0 | 15.62 |
| **Barracks 18c pandurhun damage +1 (lvl 2)** `hunba2.pandurhun.1.1` | Hungary | damage | 1 | — | 3000 | 0 | 0 | 750 | 0 | 0 | 15.62 |
| **Barracks 18c pandurhun damage +1 (lvl 3)** `hunba2.pandurhun.1.2` | Hungary | damage | 1 | — | 4000 | 0 | 0 | 1100 | 0 | 0 | 15.62 |
| **Barracks 18c pandurhun damage +2 (lvl 4)** `hunba2.pandurhun.1.3` | Hungary | damage | 2 | — | 7000 | 0 | 0 | 1800 | 0 | 0 | 15.62 |
| **Barracks 18c pandurhun damage +1 (lvl 5)** `hunba2.pandurhun.1.4` | Hungary | damage | 1 | — | 12000 | 0 | 0 | 350 | 0 | 0 | 15.62 |
| **Barracks 18c pandurhun damage +1 (lvl 6)** `hunba2.pandurhun.1.5` | Hungary | damage | 1 | — | 32020 | 0 | 0 | 850 | 0 | 0 | 15.62 |
| **Barracks 18c pandurhun damage +2 (lvl 7)** `hunba2.pandurhun.1.6` | Hungary | damage | 2 | — | 45200 | 0 | 0 | 1330 | 0 | 0 | 15.62 |
| **Barracks 18c pandurhun protection +1 (lvl 2)** `hunba2.pandurhun.2.1` | Hungary | protection | 1 | — | 3706 | 0 | 0 | 350 | 0 | 0 | 15.62 |
| **Barracks 18c pandurhun protection +1 (lvl 3)** `hunba2.pandurhun.2.2` | Hungary | protection | 1 | — | 12060 | 0 | 0 | 1350 | 0 | 0 | 15.62 |
| **Barracks 18c pandurhun protection +2 (lvl 4)** `hunba2.pandurhun.2.3` | Hungary | protection | 2 | — | 36706 | 0 | 0 | 2050 | 0 | 0 | 15.62 |
| **Barracks 18c pandurhun protection +1 (lvl 5)** `hunba2.pandurhun.2.4` | Hungary | protection | 1 | — | 36706 | 0 | 0 | 3350 | 0 | 0 | 15.62 |
| **Barracks 18c pandurhun protection +1 (lvl 6)** `hunba2.pandurhun.2.5` | Hungary | protection | 1 | — | 37060 | 0 | 0 | 1350 | 0 | 0 | 15.62 |
| **Barracks 18c pandurhun protection +2 (lvl 7)** `hunba2.pandurhun.2.6` | Hungary | protection | 2 | — | 16706 | 0 | 0 | 1350 | 0 | 0 | 15.62 |
| **Barracks 18c pikeman18 damage +2 (lvl 2)** `ausba2.pikeman18.1.1` | Austria, Bavaria, Denmark, England, France, Hungary, Netherlands, Piedmont, Poland, Portugal, Prussia, Russia, Saxony, Spain, Switzerland, Venice | damage | 2 | — | 2000 | 0 | 0 | 800 | 0 | 0 | 15.62 |
| **Barracks 18c pikeman18 damage +2 (lvl 3)** `ausba2.pikeman18.1.2` | Austria, Bavaria, Denmark, England, France, Hungary, Netherlands, Piedmont, Poland, Portugal, Prussia, Russia, Saxony, Spain, Switzerland, Venice | damage | 2 | — | 8000 | 0 | 0 | 1200 | 0 | 0 | 15.62 |
| **Barracks 18c pikeman18 damage +2 (lvl 4)** `ausba2.pikeman18.1.3` | Austria, Bavaria, Denmark, England, France, Hungary, Netherlands, Piedmont, Poland, Portugal, Prussia, Russia, Saxony, Spain, Switzerland, Venice | damage | 2 | — | 20000 | 0 | 0 | 2500 | 0 | 0 | 15.62 |
| **Barracks 18c pikeman18 damage +2 (lvl 5)** `ausba2.pikeman18.1.4` | Austria, Bavaria, Denmark, England, France, Hungary, Netherlands, Piedmont, Poland, Portugal, Prussia, Russia, Saxony, Spain, Switzerland, Venice | damage | 2 | — | 32000 | 0 | 0 | 2800 | 0 | 0 | 15.62 |
| **Barracks 18c pikeman18 damage +2 (lvl 6)** `ausba2.pikeman18.1.5` | Austria, Bavaria, Denmark, England, France, Hungary, Netherlands, Piedmont, Poland, Portugal, Prussia, Russia, Saxony, Spain, Switzerland, Venice | damage | 2 | — | 32000 | 0 | 0 | 3800 | 0 | 0 | 15.62 |
| **Barracks 18c pikeman18 damage +2 (lvl 7)** `ausba2.pikeman18.1.6` | Austria, Bavaria, Denmark, England, France, Hungary, Netherlands, Piedmont, Poland, Portugal, Prussia, Russia, Saxony, Spain, Switzerland, Venice | damage | 2 | — | 40500 | 0 | 0 | 4800 | 0 | 0 | 15.62 |
| **Barracks 18c pikeman18 protection +2 (lvl 2)** `ausba2.pikeman18.2.1` | Austria, Bavaria, Denmark, England, France, Hungary, Netherlands, Piedmont, Poland, Portugal, Prussia, Russia, Saxony, Spain, Switzerland, Venice | protection | 2 | — | 1500 | 0 | 0 | 500 | 0 | 0 | 15.62 |
| **Barracks 18c pikeman18 protection +3 (lvl 3)** `ausba2.pikeman18.2.2` | Austria, Bavaria, Denmark, England, France, Hungary, Netherlands, Piedmont, Poland, Portugal, Prussia, Russia, Saxony, Spain, Switzerland, Venice | protection | 3 | — | 7000 | 0 | 0 | 1500 | 0 | 0 | 15.62 |
| **Barracks 18c pikeman18 protection +2 (lvl 4)** `ausba2.pikeman18.2.3` | Austria, Bavaria, Denmark, England, France, Hungary, Netherlands, Piedmont, Poland, Portugal, Prussia, Russia, Saxony, Spain, Switzerland, Venice | protection | 2 | — | 37000 | 0 | 0 | 2000 | 0 | 0 | 15.62 |
| **Barracks 18c pikeman18 protection +3 (lvl 5)** `ausba2.pikeman18.2.4` | Austria, Bavaria, Denmark, England, France, Hungary, Netherlands, Piedmont, Poland, Portugal, Prussia, Russia, Saxony, Spain, Switzerland, Venice | protection | 3 | — | 37000 | 0 | 0 | 5500 | 0 | 0 | 15.62 |
| **Barracks 18c pikeman18 protection +2 (lvl 6)** `ausba2.pikeman18.2.5` | Austria, Bavaria, Denmark, England, France, Hungary, Netherlands, Piedmont, Poland, Portugal, Prussia, Russia, Saxony, Spain, Switzerland, Venice | protection | 2 | — | 37000 | 0 | 0 | 5500 | 0 | 0 | 15.62 |
| **Barracks 18c pikeman18 protection +3 (lvl 7)** `ausba2.pikeman18.2.6` | Austria, Bavaria, Denmark, England, France, Hungary, Netherlands, Piedmont, Poland, Portugal, Prussia, Russia, Saxony, Spain, Switzerland, Venice | protection | 3 | — | 64600 | 0 | 0 | 5500 | 0 | 0 | 15.62 |
| **Barracks 18c pikeman18swe damage +2 (lvl 2)** `sweba2.pikeman18swe.1.1` | Sweden | damage | 2 | — | 2000 | 0 | 0 | 800 | 0 | 0 | 15.62 |
| **Barracks 18c pikeman18swe damage +2 (lvl 3)** `sweba2.pikeman18swe.1.2` | Sweden | damage | 2 | — | 8000 | 0 | 0 | 1200 | 0 | 0 | 15.62 |
| **Barracks 18c pikeman18swe damage +2 (lvl 4)** `sweba2.pikeman18swe.1.3` | Sweden | damage | 2 | — | 20000 | 0 | 0 | 2500 | 0 | 0 | 15.62 |
| **Barracks 18c pikeman18swe damage +2 (lvl 5)** `sweba2.pikeman18swe.1.4` | Sweden | damage | 2 | — | 32000 | 0 | 0 | 2800 | 0 | 0 | 15.62 |
| **Barracks 18c pikeman18swe damage +2 (lvl 6)** `sweba2.pikeman18swe.1.5` | Sweden | damage | 2 | — | 32000 | 0 | 0 | 3800 | 0 | 0 | 15.62 |
| **Barracks 18c pikeman18swe damage +2 (lvl 7)** `sweba2.pikeman18swe.1.6` | Sweden | damage | 2 | — | 40500 | 0 | 0 | 4800 | 0 | 0 | 15.62 |
| **Barracks 18c pikeman18swe protection +2 (lvl 2)** `sweba2.pikeman18swe.2.1` | Sweden | protection | 2 | — | 1500 | 0 | 0 | 500 | 0 | 0 | 15.62 |
| **Barracks 18c pikeman18swe protection +3 (lvl 3)** `sweba2.pikeman18swe.2.2` | Sweden | protection | 3 | — | 7000 | 0 | 0 | 1500 | 0 | 0 | 15.62 |
| **Barracks 18c pikeman18swe protection +2 (lvl 4)** `sweba2.pikeman18swe.2.3` | Sweden | protection | 2 | — | 37000 | 0 | 0 | 2000 | 0 | 0 | 15.62 |
| **Barracks 18c pikeman18swe protection +3 (lvl 5)** `sweba2.pikeman18swe.2.4` | Sweden | protection | 3 | — | 37000 | 0 | 0 | 5500 | 0 | 0 | 15.62 |
| **Barracks 18c pikeman18swe protection +2 (lvl 6)** `sweba2.pikeman18swe.2.5` | Sweden | protection | 2 | — | 37000 | 0 | 0 | 5500 | 0 | 0 | 15.62 |
| **Barracks 18c pikeman18swe protection +3 (lvl 7)** `sweba2.pikeman18swe.2.6` | Sweden | protection | 3 | — | 64600 | 0 | 0 | 5500 | 0 | 0 | 15.62 |
| **Barracks 18c swordsmansco damage +2 (lvl 2)** `scoba2.swordsmansco.1.1` | Scotland | damage | 2 | — | 450 | 0 | 0 | 110 | 0 | 0 | 15.62 |
| **Barracks 18c swordsmansco damage +3 (lvl 3)** `scoba2.swordsmansco.1.2` | Scotland | damage | 3 | — | 900 | 0 | 0 | 220 | 0 | 0 | 15.62 |
| **Barracks 18c swordsmansco damage +4 (lvl 4)** `scoba2.swordsmansco.1.3` | Scotland | damage | 4 | — | 3350 | 0 | 0 | 850 | 0 | 0 | 15.62 |
| **Barracks 18c swordsmansco damage +5 (lvl 5)** `scoba2.swordsmansco.1.4` | Scotland | damage | 5 | — | 14400 | 0 | 0 | 2060 | 0 | 0 | 15.62 |
| **Barracks 18c swordsmansco damage +6 (lvl 6)** `scoba2.swordsmansco.1.5` | Scotland | damage | 6 | — | 37800 | 0 | 0 | 4525 | 0 | 0 | 15.62 |
| **Barracks 18c swordsmansco damage +10 (lvl 7)** `scoba2.swordsmansco.1.6` | Scotland | damage | 10 | — | 90000 | 0 | 0 | 8000 | 0 | 0 | 15.62 |
| **Barracks 18c swordsmansco protection +1 (lvl 2)** `scoba2.swordsmansco.2.1` | Scotland | protection | 1 | — | 200 | 0 | 0 | 75 | 0 | 0 | 15.62 |
| **Barracks 18c swordsmansco protection +2 (lvl 3)** `scoba2.swordsmansco.2.2` | Scotland | protection | 2 | — | 700 | 0 | 0 | 225 | 0 | 0 | 15.62 |
| **Barracks 18c swordsmansco protection +2 (lvl 4)** `scoba2.swordsmansco.2.3` | Scotland | protection | 2 | — | 2500 | 0 | 0 | 560 | 0 | 0 | 15.62 |
| **Barracks 18c swordsmansco protection +2 (lvl 5)** `scoba2.swordsmansco.2.4` | Scotland | protection | 2 | — | 7750 | 0 | 0 | 1125 | 0 | 0 | 15.62 |
| **Barracks 18c swordsmansco protection +3 (lvl 6)** `scoba2.swordsmansco.2.5` | Scotland | protection | 3 | — | 15800 | 0 | 0 | 1800 | 0 | 0 | 15.62 |
| **Barracks 18c swordsmansco protection +5 (lvl 7)** `scoba2.swordsmansco.2.6` | Scotland | protection | 5 | — | 36125 | 0 | 0 | 3350 | 0 | 0 | 15.62 |

<a id="art--артиллерийское-депо-апгрейды-пушек"></a>
<a id="артиллерийское-депо-апгрейды-пушек-art"></a>
## Artillery Depot (`art`) — cannon upgrades

| Upgrade | Nations | Effect | Value | Price change | Food | Wood | Stone | Gold | Iron | Coal | Time |
|---|---|---|---:|---|---:|---:|---:|---:|---:|---:|---:|
| `ausart.cannon.1.1` | all | price % | 35 | gold -25% / iron -25% / wood -25% | 0 | 1000 | 500 | 300 | 0 | 0 | 10.0 |
| `ausart.cannon.1.2` | all | price % | 35 | gold -25% / iron -25% / wood -25% | 0 | 3000 | 1000 | 500 | 0 | 0 | 10.0 |
| `ausart.cannon.1.3` | all | price % | 35 | gold -25% / iron -25% / wood -25% | 0 | 6000 | 2000 | 1000 | 0 | 0 | 10.0 |
| `ausart.cannon.1.4` | all | price % | 35 | gold -25% / iron -25% / wood -25% | 1760 | 0 | 0 | 350 | 0 | 0 | 15.62 |
| `ausart.cannon.1.5` | all | price % | 35 | gold -25% / iron -25% / wood -25% | 1760 | 0 | 0 | 350 | 0 | 0 | 15.62 |
| `ausart.cannon.1.6` | all | price % | 35 | gold -25% / iron -25% / wood -25% | 1760 | 0 | 0 | 350 | 0 | 0 | 15.62 |
| `ausart.cannon.2.1` | all | build time % | -2500000 | — | 0 | 0 | 0 | 500 | 1000 | 0 | 10.0 |
| `turart.cannon.2.1` | Algeria, Turkey | build time % | -2500000 | — | 0 | 0 | 0 | 950 | 1000 | 0 | 10.0 |
| `ausart.cannon.2.2` | all | build time % | -2500000 | — | 0 | 0 | 0 | 1000 | 2000 | 0 | 10.0 |
| `turart.cannon.2.2` | Algeria, Turkey | build time % | -2500000 | — | 0 | 0 | 0 | 150 | 2000 | 0 | 10.0 |
| `ausart.cannon.2.3` | all | build time % | -2500000 | — | 0 | 0 | 0 | 2000 | 3000 | 0 | 10.0 |
| `turart.cannon.2.3` | Algeria, Turkey | build time % | -2500000 | — | 0 | 0 | 0 | 250 | 3000 | 0 | 10.0 |
| `ausart.cannon.2.4` | all | build time % | -2000000 | — | 2560 | 0 | 0 | 0 | 0 | 0 | 15.62 |
| `turart.cannon.2.4` | Algeria, Turkey | build time % | -2000000 | — | 2560 | 0 | 0 | 1350 | 0 | 0 | 15.62 |
| `ausart.cannon.2.5` | all | build time % | -2000000 | — | 3560 | 0 | 0 | 0 | 0 | 0 | 15.62 |
| `turart.cannon.2.5` | Algeria, Turkey | build time % | -2000000 | — | 3560 | 0 | 0 | 2500 | 0 | 0 | 15.62 |
| `ausart.cannon.2.6` | all | build time % | -2000000 | — | 5560 | 0 | 0 | 0 | 0 | 0 | 15.62 |
| `turart.cannon.2.6` | Algeria, Turkey | build time % | -2000000 | — | 5560 | 0 | 0 | 3350 | 0 | 0 | 15.62 |
| `ausart.howitzer.1.1` | all | price % | 35 | gold -25% / iron -25% / wood -25% | 0 | 1000 | 500 | 300 | 0 | 0 | 10.0 |
| `ausart.howitzer.1.2` | all | price % | 35 | gold -25% / iron -25% / wood -25% | 0 | 3000 | 1000 | 500 | 0 | 0 | 10.0 |
| `ausart.howitzer.1.3` | all | price % | 35 | gold -25% / iron -25% / wood -25% | 0 | 6000 | 2000 | 1000 | 0 | 0 | 10.0 |
| `ausart.howitzer.1.4` | all | price % | 35 | gold -25% / iron -25% / wood -25% | 1760 | 0 | 0 | 350 | 0 | 0 | 15.62 |
| `ausart.howitzer.1.5` | all | price % | 35 | gold -25% / iron -25% / wood -25% | 1760 | 0 | 0 | 350 | 0 | 0 | 15.62 |
| `ausart.howitzer.1.6` | all | price % | 35 | gold -25% / iron -25% / wood -25% | 1760 | 0 | 0 | 350 | 0 | 0 | 15.62 |
| `ausart.howitzer.2.1` | all | build time % | -2500000 | — | 0 | 0 | 0 | 500 | 1000 | 0 | 10.0 |
| `turart.howitzer.2.1` | Algeria, Turkey | build time % | -2500000 | — | 0 | 0 | 0 | 350 | 1000 | 0 | 10.0 |
| `ausart.howitzer.2.2` | all | build time % | -2500000 | — | 0 | 0 | 0 | 1000 | 2000 | 0 | 10.0 |
| `turart.howitzer.2.2` | Algeria, Turkey | build time % | -2500000 | — | 0 | 0 | 0 | 450 | 2000 | 0 | 10.0 |
| `ausart.howitzer.2.3` | all | build time % | -2500000 | — | 0 | 0 | 0 | 2000 | 3000 | 0 | 10.0 |
| `turart.howitzer.2.3` | Algeria, Turkey | build time % | -2500000 | — | 0 | 0 | 0 | 550 | 3000 | 0 | 10.0 |
| `ausart.howitzer.2.4` | all | build time % | -2000000 | — | 2560 | 0 | 0 | 0 | 0 | 0 | 31.25 |
| `turart.howitzer.2.4` | Algeria, Turkey | build time % | -2000000 | — | 2560 | 0 | 0 | 1150 | 0 | 0 | 31.25 |
| `ausart.howitzer.2.5` | all | build time % | -2000000 | — | 3560 | 0 | 0 | 0 | 0 | 0 | 31.25 |
| `turart.howitzer.2.5` | Algeria, Turkey | build time % | -2000000 | — | 3560 | 0 | 0 | 3200 | 0 | 0 | 31.25 |
| `ausart.howitzer.2.6` | all | build time % | -2000000 | — | 5560 | 0 | 0 | 0 | 0 | 0 | 31.25 |
| `turart.howitzer.2.6` | Algeria, Turkey | build time % | -2000000 | — | 5560 | 0 | 0 | 4500 | 0 | 0 | 31.25 |

<a id="cen--городской-центр-переход-эпохи"></a>
<a id="городской-центр-переход-эпохи-cen"></a>
## Town Hall (`cen`) — advancing to the 18th century

| Upgrade | Nations | Effect | Value | Price change | Food | Wood | Stone | Gold | Iron | Coal | Time |
|---|---|---|---:|---|---:|---:|---:|---:|---:|---:|---:|
| **Progress to the 18th Century** `auscen.1` | Algeria, Austria, Bavaria, Hungary, Piedmont, Portugal, Russia, Saxony, Scotland, Spain, Switzerland, Turkey, Ukraine | enable unit | 0 | — | 30000 | 0 | 0 | 5000 | 2000 | 2000 | 9.38 |
| **Progress to the 18th Century** `prucen.1` | Denmark, Prussia | enable unit | 0 | — | 20000 | 0 | 0 | 6500 | 1100 | 1100 | 9.38 |
| **Progress to the 18th Century** `fracen.1` | France | enable unit | 0 | — | 40000 | 0 | 0 | 3500 | 4000 | 4000 | 9.38 |
| **Progress to the 18th Century** `engcen.1` | England | enable unit | 0 | — | 25000 | 0 | 0 | 5000 | 5500 | 5500 | 9.38 |
| **Progress to the 18th Century** `polcen.1` | Poland | enable unit | 0 | — | 30000 | 0 | 0 | 4800 | 2200 | 2200 | 9.38 |
| **Progress to the 18th Century** `swecen.1` | Sweden | enable unit | 0 | — | 37000 | 0 | 0 | 5500 | 1500 | 1500 | 9.38 |
| **Progress to the 18th Century** `vencen.1` | Venice | enable unit | 0 | — | 40000 | 0 | 0 | 3000 | 2500 | 2500 | 9.38 |
| **Progress to the 18th Century** `netcen.1` | Netherlands | enable unit | 0 | — | 33000 | 0 | 0 | 4800 | 1800 | 1800 | 9.38 |

<a id="tow--башня-скорость-перезарядки"></a>
<a id="башня-скорость-перезарядки-tow"></a>
## Tower (`tow`) — reload speed

| Upgrade | Nations | Effect | Value | Price change | Food | Wood | Stone | Gold | Iron | Coal | Time |
|---|---|---|---:|---|---:|---:|---:|---:|---:|---:|---:|
| **Increase number of defensive cannons (20%)** `eurtow.1` | all | single reload % | -20 | — | 0 | 0 | 0 | 250 | 0 | 0 | 31.25 |
| **Increase number of defensive cannons (20%)** `eurtow.2` | all | single reload % | -20 | — | 0 | 0 | 0 | 0 | 350 | 0 | 31.25 |
| **Increase number of defensive cannons (10%)** `eurtow.3` | all | single reload % | -10 | — | 0 | 0 | 0 | 0 | 0 | 400 | 31.25 |
| **Increase number of defensive cannons (10%)** `eurtow.4` | all | single reload % | -10 | — | 0 | 0 | 0 | 0 | 450 | 0 | 31.25 |
| **Increase number of defensive cannons (10%)** `eurtow.5` | all | single reload % | -10 | — | 0 | 0 | 0 | 0 | 0 | 500 | 31.25 |

<a id="swa--каменная-стена-постройка-ворот"></a>
<a id="каменная-стена-постройка-ворот-swa"></a>
## Stone Wall (`swa`) — building a gate

| Upgrade | Nations | Effect | Value | Price change | Food | Wood | Stone | Gold | Iron | Coal | Time |
|---|---|---|---:|---|---:|---:|---:|---:|---:|---:|---:|
| `eurswa.1` | all | build gate | 5 | — | 0 | 0 | 500 | 0 | 0 | 0 | 0.03 |

<a id="wwa--палисад-постройка-ворот"></a>
<a id="палисад-постройка-ворот-wwa"></a>
## Palisade (`wwa`) — building a gate

| Upgrade | Nations | Effect | Value | Price change | Food | Wood | Stone | Gold | Iron | Coal | Time |
|---|---|---|---:|---|---:|---:|---:|---:|---:|---:|---:|
| `ukrwwa.1` | all | build gate | 5 | — | 0 | 400 | 0 | 0 | 0 | 0 | 0.03 |

<a id="por--порт-лечение"></a>
<a id="порт-лечение-por"></a>
## Shipyard (`por`) — healing

| Upgrade | Nations | Effect | Value | Price change | Food | Wood | Stone | Gold | Iron | Coal | Time |
|---|---|---|---:|---|---:|---:|---:|---:|---:|---:|---:|
| **Train woodworkers (repair all ships)** `eurpor.1` | all | healing | 50 | — | 0 | 20000 | 0 | 1500 | 0 | 0 | 46.88 |
| **Train woodworkers (repair all ships)** `eurpor.1` | England | healing | 50 | — | 0 | 12000 | 0 | 500 | 0 | 0 | 46.88 |

<a id="ferry--транспорт-вместимость"></a>
<a id="транспорт-вместимость-ferry"></a>
## Ferry (`ferry`) — capacity

| Upgrade | Nations | Effect | Value | Price change | Food | Wood | Stone | Gold | Iron | Coal | Time |
|---|---|---|---:|---|---:|---:|---:|---:|---:|---:|---:|
| **Improve transport vessel design (+%value% capacity)** `ferry.1` | all | +building capacity | 200 | — | 1000 | 0 | 0 | 1250 | 0 | 0 | 15.62 |
