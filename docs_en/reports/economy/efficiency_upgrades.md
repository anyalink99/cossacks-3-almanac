<a id="улучшения-добычи-по-нациям"></a>
# Resource Gathering Upgrades

[← Tables and calculations](../README.md)

<a id="что-это"></a>
<a id="как-складываются-бонусы"></a>
## How the Bonuses Stack

Food, wood, and stone upgrades add their percentage bonuses together [^1].
Gathering starts at 100% efficiency. The game multiplies the amount
collected per action by the resulting efficiency and rounds down [^2].

Field-durability upgrades also stack additively. More durable fields last
longer, reducing how often Peasants must sow a replacement.

<a id="сводка-по-нациям-кумулятивные-пики"></a>
<a id="максимальный-бонус-по-нациям"></a>
## Maximum Bonus by Nation

Each row adds every relevant upgrade available to the nation and therefore
shows its theoretical maximum. Actual progress is reached one upgrade at a
time through the normal research chain.

| Nation | Food bonus, % | Wood bonus, % | Stone bonus, % | Field durability, % | Upgrades |
| --- | ---: | ---: | ---: | ---: | ---: |
| Algeria | +280 | +100 | +300 | +300 | 9 |
| Austria | +460 | +100 | +300 | +300 | 10 |
| Bavaria | +460 | +100 | +300 | +300 | 10 |
| Denmark | +460 | +100 | +300 | +300 | 10 |
| England | +460 | +100 | +300 | +300 | 10 |
| France | +460 | +100 | +300 | +300 | 10 |
| Hungary | +460 | +100 | +300 | +300 | 10 |
| Netherlands | +460 | +100 | +300 | +300 | 10 |
| Piedmont | +460 | +100 | +300 | +300 | 10 |
| Poland | +460 | +100 | +300 | +300 | 10 |
| Portugal | +460 | +100 | +300 | +300 | 10 |
| Prussia | +460 | +100 | +300 | +300 | 10 |
| Russia | +460 | +100 | +300 | +300 | 10 |
| Saxony | +460 | +100 | +300 | +300 | 10 |
| Scotland | +460 | +100 | +300 | +300 | 10 |
| Spain | +460 | +100 | +300 | +300 | 10 |
| Sweden | +460 | +100 | +300 | +300 | 10 |
| Switzerland | +460 | +100 | +300 | +300 | 10 |
| Turkey | +280 | +100 | +300 | +300 | 9 |
| Ukraine | +460 | +100 | +300 | +300 | 10 |
| Venice | +460 | +100 | +300 | +300 | 10 |

**Maximum values:**

- Food efficiency: **+460%** for 19 nations
- Wood efficiency: **+100%** for every nation
- Stone efficiency: **+300%** for every nation
- Field durability: **+300%** for every nation

The following table compares the total cost of completing the entire food
efficiency chain.

<a id="стоимость-всей-цепочки-улучшений-еды"></a>
## Total Cost of the Food Upgrade Chain

| Nation | Gold | Food | Wood |
| --- | ---: | ---: | ---: |
| **Algeria** (`alg`) | 1947 | 600 | 1840 |
| **Turkey** (`tur`) | 1947 | 600 | 3000 |
| **Scotland** (`sco`) | 3400 | 6350 | 6200 |
| **Ukraine** (`ukr`) | 3400 | 6350 | 6200 |
| **France** (`fra`) | 5390 | 26350 | 6190 |
| **Austria** (`aus`) | 5400 | 26350 | 6200 |
| **Bavaria** (`bav`) | 5400 | 26350 | 6200 |
| **Denmark** (`den`) | 5400 | 26350 | 6200 |
| **England** (`eng`) | 5400 | 26350 | 6200 |
| **Hungary** (`hun`) | 5400 | 26350 | 6200 |
| **Netherlands** (`net`) | 5400 | 26350 | 6200 |
| **Piedmont** (`pie`) | 5400 | 26350 | 6200 |
| **Poland** (`pol`) | 5400 | 26350 | 6200 |
| **Portugal** (`por`) | 5400 | 26350 | 6200 |
| **Prussia** (`pru`) | 5400 | 26350 | 6200 |
| **Russia** (`rus`) | 5400 | 26350 | 6200 |
| **Saxony** (`sax`) | 5400 | 26350 | 6200 |
| **Spain** (`spa`) | 5400 | 26350 | 6200 |
| **Sweden** (`swe`) | 5400 | 26350 | 6200 |
| **Switzerland** (`swi`) | 5400 | 26350 | 6200 |
| **Venice** (`ven`) | 5400 | 26350 | 6200 |

<a id="подробно-по-нациям"></a>
## Detail by nation

Each cost cell is the cost of **this** upgrade (not total).

<a id="alg--algeria-алжир"></a>
<a id="алжир-alg"></a>
### Algeria (`alg`)
<a id="эффективность-еды"></a>
<a id="добыча-еды"></a>
#### Food efficiency

| Upgrade | Upgrade ID | Stage | Bonus | Research time, game s | Cost | Requirements |
| --- | --- | ---: | ---: | ---: | --- | --- |
| Cultivate new cultures of wheat (harvesting +40%) | `algaca.1` | 1 | +40% | 15.62 | wood 200 · gold 325 | — |
| Cultivate new cultures of rye (harvesting +50%) | `algaca.2` | 1 | +50% | 15.62 | wood 400 · gold 522 | — |
| Raise agriculturists' salary (harvesting +50%) | `algaca.3` | 1 | +50% | 15.62 | wood 1240 · gold 850 | — |
| Improve grain crops treatment (harvesting +140%) | `turmil.1` | 1 | +140% | 15.62 | food 600 · gold 250 | — |

_Cumulative peak: +280_

<a id="добыча-дерева"></a>
#### Tree efficiency

| Upgrade | Upgrade ID | Stage | Bonus | Research time, game s | Cost | Requirements |
| --- | --- | ---: | ---: | ---: | --- | --- |
| Design new woodworking tools (woodcutting efficiency +100%) | `algaca.8` | 1 | +100% | 15.62 | food 5500 · gold 550 | Blacksmith (`algbla`) |

_Cumulative peak: +100_

<a id="добыча-камня"></a>
#### Stone efficiency

| Upgrade | Upgrade ID | Stage | Bonus | Research time, game s | Cost | Requirements |
| --- | --- | ---: | ---: | ---: | --- | --- |
| Develop mining (stone excavation efficiency +100%) | `algaca.23` | 1 | +100% | 15.62 | gold 1550 · iron 3000 | — |
| Raise miners' salary (stone excavation efficiency +200%) | `algaca.24` | 1 | +200% | 15.62 | food 4200 · gold 1550 · coal 12520 | — |

_Cumulative peak: +300_

<a id="прочность-полей"></a>
#### Field durability

| Upgrade | Upgrade ID | Stage | Bonus | Research time, game s | Cost | Requirements |
| --- | --- | ---: | ---: | ---: | --- | --- |
| Carry out field melioration (field capacity +200%) | `algaca.4` | 1 | +200% | 15.62 | wood 700 · gold 475 | — |
| Manufacture agricultural equipment (field capacity +100%) | `algbla.1` | 1 | +100% | 15.62 | wood 400 · gold 90 | — |

_Cumulative peak: +300_


<a id="aus--austria-австрия"></a>
<a id="австрия-aus"></a>
### Austria (`aus`)
<a id="добыча-еды-1"></a>
#### Food efficiency

| Upgrade | Upgrade ID | Stage | Bonus | Research time, game s | Cost | Requirements |
| --- | --- | ---: | ---: | ---: | --- | --- |
| Cultivate new cultures of wheat (harvesting +40%) | `ausaca.1` | 1 | +40% | 15.62 | wood 200 · gold 325 | — |
| Cultivate new cultures of rye (harvesting +50%) | `ausaca.2` | 1 | +50% | 15.62 | wood 2400 · gold 625 | — |
| Raise agriculturists' salary (harvesting +50%) | `ausaca.3` | 1 | +50% | 15.62 | wood 3600 · gold 850 | — |
| Improve grain crops treatment (harvesting +140%) | `eurmil.1` | 1 | +140% | 15.62 | food 750 · gold 250 | — |
| Improve grain crops storage (harvesting +180%) | `eurmil.2` | 2 | +180% | 15.62 | food 25600 · gold 3350 · iron 2000 | Previous upgrade |

_Cumulative peak: +460_

<a id="добыча-дерева-1"></a>
#### Tree efficiency

| Upgrade | Upgrade ID | Stage | Bonus | Research time, game s | Cost | Requirements |
| --- | --- | ---: | ---: | ---: | --- | --- |
| Design new woodworking tools (woodcutting efficiency +100%) | `ausaca.8` | 1 | +100% | 15.62 | food 5500 · gold 550 | Blacksmith (`ausbla`) |

_Cumulative peak: +100_

<a id="добыча-камня-1"></a>
#### Stone efficiency

| Upgrade | Upgrade ID | Stage | Bonus | Research time, game s | Cost | Requirements |
| --- | --- | ---: | ---: | ---: | --- | --- |
| Develop mining (stone excavation efficiency +100%) | `ausaca.23` | 1 | +100% | 15.62 | gold 1550 · iron 3000 | — |
| Raise miners' salary (stone excavation efficiency +200%) | `ausaca.24` | 1 | +200% | 15.62 | food 4200 · gold 1550 · coal 12520 | — |

_Cumulative peak: +300_

<a id="прочность-полей-1"></a>
#### Field durability

| Upgrade | Upgrade ID | Stage | Bonus | Research time, game s | Cost | Requirements |
| --- | --- | ---: | ---: | ---: | --- | --- |
| Carry out field melioration (field capacity +200%) | `ausaca.4` | 1 | +200% | 15.62 | wood 1000 · gold 475 | — |
| Manufacture agricultural equipment (field capacity +100%) | `ausbla.1` | 1 | +100% | 15.62 | wood 400 · gold 90 | — |

_Cumulative peak: +300_


<a id="bav--bavaria-бавария"></a>
<a id="бавария-bav"></a>
### Bavaria (`bav`)
<a id="добыча-еды-2"></a>
#### Food efficiency

| Upgrade | Upgrade ID | Stage | Bonus | Research time, game s | Cost | Requirements |
| --- | --- | ---: | ---: | ---: | --- | --- |
| Cultivate new cultures of wheat (harvesting +40%) | `bavaca.1` | 1 | +40% | 15.62 | wood 200 · gold 325 | — |
| Cultivate new cultures of rye (harvesting +50%) | `bavaca.2` | 1 | +50% | 15.62 | wood 2400 · gold 625 | — |
| Raise agriculturists' salary (harvesting +50%) | `bavaca.3` | 1 | +50% | 15.62 | wood 3600 · gold 850 | — |
| Improve grain crops treatment (harvesting +140%) | `eurmil.1` | 1 | +140% | 15.62 | food 750 · gold 250 | — |
| Improve grain crops storage (harvesting +180%) | `eurmil.2` | 2 | +180% | 15.62 | food 25600 · gold 3350 · iron 2000 | Previous upgrade |

_Cumulative peak: +460_

<a id="добыча-дерева-2"></a>
#### Tree efficiency

| Upgrade | Upgrade ID | Stage | Bonus | Research time, game s | Cost | Requirements |
| --- | --- | ---: | ---: | ---: | --- | --- |
| Design new woodworking tools (woodcutting efficiency +100%) | `bavaca.8` | 1 | +100% | 15.62 | food 5500 · gold 550 | Blacksmith (`bavbla`) |

_Cumulative peak: +100_

<a id="добыча-камня-2"></a>
#### Stone efficiency

| Upgrade | Upgrade ID | Stage | Bonus | Research time, game s | Cost | Requirements |
| --- | --- | ---: | ---: | ---: | --- | --- |
| Develop mining (stone excavation efficiency +100%) | `bavaca.23` | 1 | +100% | 15.62 | gold 1550 · iron 3000 | — |
| Raise miners' salary (stone excavation efficiency +200%) | `bavaca.24` | 1 | +200% | 15.62 | food 4200 · gold 1550 · coal 12520 | — |

_Cumulative peak: +300_

<a id="прочность-полей-2"></a>
#### Field durability

| Upgrade | Upgrade ID | Stage | Bonus | Research time, game s | Cost | Requirements |
| --- | --- | ---: | ---: | ---: | --- | --- |
| Carry out field melioration (field capacity +200%) | `bavaca.4` | 1 | +200% | 15.62 | wood 1000 · gold 475 | — |
| Manufacture agricultural equipment (field capacity +100%) | `bavbla.1` | 1 | +100% | 15.62 | wood 400 · gold 90 | — |

_Cumulative peak: +300_


<a id="den--denmark-дания"></a>
<a id="дания-den"></a>
### Denmark (`den`)
<a id="добыча-еды-3"></a>
#### Food efficiency

| Upgrade | Upgrade ID | Stage | Bonus | Research time, game s | Cost | Requirements |
| --- | --- | ---: | ---: | ---: | --- | --- |
| Cultivate new cultures of wheat (harvesting +40%) | `denaca.1` | 1 | +40% | 15.62 | wood 200 · gold 325 | — |
| Cultivate new cultures of rye (harvesting +50%) | `denaca.2` | 1 | +50% | 15.62 | wood 2400 · gold 625 | — |
| Raise agriculturists' salary (harvesting +50%) | `denaca.3` | 1 | +50% | 15.62 | wood 3600 · gold 850 | — |
| Improve grain crops treatment (harvesting +140%) | `eurmil.1` | 1 | +140% | 15.62 | food 750 · gold 250 | — |
| Improve grain crops storage (harvesting +180%) | `eurmil.2` | 2 | +180% | 15.62 | food 25600 · gold 3350 · iron 2000 | Previous upgrade |
_Cumulative peak: +460_

<a id="эффективность-дерева"></a>
<a id="добыча-дерева-3"></a>
#### Tree efficiency

| Upgrade | Upgrade ID | Stage | Bonus | Research time, game s | Cost | Requirements |
| --- | --- | ---: | ---: | ---: | --- | --- |
| Design new woodworking tools (woodcutting efficiency +100%) | `denaca.8` | 1 | +100% | 15.62 | food 5500 · gold 550 | Blacksmith (`denbla`) |

_Cumulative peak: +100_

<a id="эффективность-камня"></a>
<a id="добыча-камня-3"></a>
#### Stone efficiency

| Upgrade | Upgrade ID | Stage | Bonus | Research time, game s | Cost | Requirements |
| --- | --- | ---: | ---: | ---: | --- | --- |
| Develop mining (stone excavation efficiency +100%) | `denaca.23` | 1 | +100% | 15.62 | gold 1550 · iron 3000 | — |
| Raise miners' salary (stone excavation efficiency +200%) | `denaca.24` | 1 | +200% | 15.62 | food 4200 · gold 1550 · coal 12520 | — |

_Cumulative peak: +300_

<a id="прочность-полей-3"></a>
#### Field durability

| Upgrade | Upgrade ID | Stage | Bonus | Research time, game s | Cost | Requirements |
| --- | --- | ---: | ---: | ---: | --- | --- |
| Carry out field melioration (field capacity +200%) | `denaca.4` | 1 | +200% | 15.62 | wood 1000 · gold 475 | — |
| Manufacture agricultural equipment (field capacity +100%) | `denbla.1` | 1 | +100% | 15.62 | wood 400 · gold 90 | — |

_Cumulative peak: +300_


<a id="eng--england-англия"></a>
<a id="англия-eng"></a>
### England (`eng`)
<a id="эффективность-еды-1"></a>
<a id="добыча-еды-4"></a>
#### Food efficiency

| Upgrade | Upgrade ID | Stage | Bonus | Research time, game s | Cost | Requirements |
| --- | --- | ---: | ---: | ---: | --- | --- |
| Cultivate new cultures of wheat (harvesting +40%) | `engaca.1` | 1 | +40% | 15.62 | wood 200 · gold 325 | — |
| Cultivate new cultures of rye (harvesting +50%) | `engaca.2` | 1 | +50% | 15.62 | wood 2400 · gold 625 | — |
| Raise agriculturists' salary (harvesting +50%) | `engaca.3` | 1 | +50% | 15.62 | wood 3600 · gold 850 | — |
| Improve grain crops treatment (harvesting +140%) | `eurmil.1` | 1 | +140% | 15.62 | food 750 · gold 250 | — |
| Improve grain crops storage (harvesting +180%) | `eurmil.2` | 2 | +180% | 15.62 | food 25600 · gold 3350 · iron 2000 | Previous upgrade |

_Cumulative peak: +460_

<a id="эффективность-дерева-1"></a>
<a id="добыча-дерева-4"></a>
#### Tree efficiency

| Upgrade | Upgrade ID | Stage | Bonus | Research time, game s | Cost | Requirements |
| --- | --- | ---: | ---: | ---: | --- | --- |
| Design new woodworking tools (woodcutting efficiency +100%) | `engaca.8` | 1 | +100% | 15.62 | food 5500 · gold 550 | Blacksmith (`engbla`) |

_Cumulative peak: +100_

<a id="эффективность-камня-1"></a>
<a id="добыча-камня-4"></a>
#### Stone efficiency

| Upgrade | Upgrade ID | Stage | Bonus | Research time, game s | Cost | Requirements |
| --- | --- | ---: | ---: | ---: | --- | --- |
| Develop mining (stone excavation efficiency +100%) | `engaca.23` | 1 | +100% | 15.62 | gold 1550 · iron 3000 | — |
| Raise miners' salary (stone excavation efficiency +200%) | `engaca.24` | 1 | +200% | 15.62 | food 4200 · gold 1550 · coal 12520 | — |

_Cumulative peak: +300_

<a id="прочность-полей-4"></a>
#### Field durability

| Upgrade | Upgrade ID | Stage | Bonus | Research time, game s | Cost | Requirements |
| --- | --- | ---: | ---: | ---: | --- | --- |
| Carry out field melioration (field capacity +200%) | `engaca.4` | 1 | +200% | 15.62 | wood 1000 · gold 475 | — |
| Manufacture agricultural equipment (field capacity +100%) | `engbla.1` | 1 | +100% | 15.62 | wood 400 · gold 90 | — |

_Cumulative peak: +300_


<a id="fra--france-франция"></a>
<a id="франция-fra"></a>
### France (`fra`)
<a id="эффективность-еды-2"></a>
<a id="добыча-еды-5"></a>
#### Food efficiency

| Upgrade | Upgrade ID | Stage | Bonus | Research time, game s | Cost | Requirements |
| --- | --- | ---: | ---: | ---: | --- | --- |
| Improve grain crops treatment (harvesting +140%) | `eurmil.1` | 1 | +140% | 15.62 | food 750 · gold 250 | — |
| Improve grain crops storage (harvesting +180%) | `eurmil.2` | 2 | +180% | 15.62 | food 25600 · gold 3350 · iron 2000 | Previous upgrade |
| Cultivate new cultures of wheat (harvesting +40%) | `fraaca.1` | 1 | +40% | 15.62 | wood 190 · gold 315 | — |
| Cultivate new cultures of rye (harvesting +50%) | `fraaca.2` | 1 | +50% | 15.62 | wood 2400 · gold 625 | — |
| Raise agriculturists' salary (harvesting +50%) | `fraaca.3` | 1 | +50% | 15.62 | wood 3600 · gold 850 | — |

_Cumulative peak: +460_

<a id="эффективность-дерева-2"></a>
<a id="добыча-дерева-5"></a>
#### Tree efficiency

| Upgrade | Upgrade ID | Stage | Bonus | Research time, game s | Cost | Requirements |
| --- | --- | ---: | ---: | ---: | --- | --- |
| Design new woodworking tools (woodcutting efficiency +100%) | `fraaca.8` | 1 | +100% | 15.62 | food 5500 · gold 550 | Blacksmith (`frabla`) |

_Cumulative peak: +100_

<a id="эффективность-камня-2"></a>
<a id="добыча-камня-5"></a>
#### Stone efficiency

| Upgrade | Upgrade ID | Stage | Bonus | Research time, game s | Cost | Requirements |
| --- | --- | ---: | ---: | ---: | --- | --- |
| Develop mining (stone excavation efficiency +100%) | `fraaca.23` | 1 | +100% | 15.62 | gold 1550 · iron 3000 | — |
| Raise miners' salary (stone excavation efficiency +200%) | `fraaca.24` | 1 | +200% | 15.62 | food 4200 · gold 1550 · coal 12520 | — |

_Cumulative peak: +300_

<a id="прочность-полей-5"></a>
#### Field durability

| Upgrade | Upgrade ID | Stage | Bonus | Research time, game s | Cost | Requirements |
| --- | --- | ---: | ---: | ---: | --- | --- |
| Carry out field melioration (field capacity +200%) | `fraaca.4` | 1 | +200% | 15.62 | wood 1000 · gold 475 | — |
| Manufacture agricultural equipment (field capacity +100%) | `frabla.1` | 1 | +100% | 15.62 | wood 400 · gold 90 | — |

_Cumulative peak: +300_


<a id="hun--hungary-венгрия"></a>
<a id="венгрия-hun"></a>
### Hungary (`hun`)
<a id="эффективность-еды-3"></a>
<a id="добыча-еды-6"></a>
#### Food efficiency

| Upgrade | Upgrade ID | Stage | Bonus | Research time, game s | Cost | Requirements |
| --- | --- | ---: | ---: | ---: | --- | --- |
| Improve grain crops treatment (harvesting +140%) | `eurmil.1` | 1 | +140% | 15.62 | food 750 · gold 250 | — |
| Improve grain crops storage (harvesting +180%) | `eurmil.2` | 2 | +180% | 15.62 | food 25600 · gold 3350 · iron 2000 | Previous upgrade |
| Cultivate new cultures of wheat (harvesting +40%) | `hunaca.1` | 1 | +40% | 15.62 | wood 200 · gold 325 | — |
| Cultivate new cultures of rye (harvesting +50%) | `hunaca.2` | 1 | +50% | 15.62 | wood 2400 · gold 625 | — |
| Raise agriculturists' salary (harvesting +50%) | `hunaca.3` | 1 | +50% | 15.62 | wood 3600 · gold 850 | — |

_Cumulative peak: +460_

<a id="эффективность-дерева-3"></a>
<a id="добыча-дерева-6"></a>
#### Tree efficiency

| Upgrade | Upgrade ID | Stage | Bonus | Research time, game s | Cost | Requirements |
| --- | --- | ---: | ---: | ---: | --- | --- |
| Design new woodworking tools (woodcutting efficiency +100%) | `hunaca.8` | 1 | +100% | 15.62 | food 5500 · gold 550 | Blacksmith (`hunbla`) |

_Cumulative peak: +100_

<a id="добыча-камня-6"></a>
#### Stone efficiency

| Upgrade | Upgrade ID | Stage | Bonus | Research time, game s | Cost | Requirements |
| --- | --- | ---: | ---: | ---: | --- | --- |
| Develop mining (stone excavation efficiency +100%) | `hunaca.23` | 1 | +100% | 15.62 | gold 1550 · iron 3000 | — |
| Raise miners' salary (stone excavation efficiency +200%) | `hunaca.24` | 1 | +200% | 15.62 | food 4200 · gold 1550 · coal 12520 | — |

_Cumulative peak: +300_

<a id="прочность-полей-6"></a>
#### Field durability

| Upgrade | Upgrade ID | Stage | Bonus | Research time, game s | Cost | Requirements |
| --- | --- | ---: | ---: | ---: | --- | --- |
| Carry out field melioration (field capacity +200%) | `hunaca.4` | 1 | +200% | 15.62 | wood 1000 · gold 475 | — |
| Manufacture agricultural equipment (field capacity +100%) | `hunbla.1` | 1 | +100% | 15.62 | wood 400 · gold 90 | — |

_Cumulative peak: +300_


<a id="net--netherlands-нидерланды"></a>
<a id="нидерланды-net"></a>
### Netherlands (`net`)
<a id="добыча-еды-7"></a>
#### Food efficiency

| Upgrade | Upgrade ID | Stage | Bonus | Research time, game s | Cost | Requirements |
| --- | --- | ---: | ---: | ---: | --- | --- |
| Improve grain crops treatment (harvesting +140%) | `eurmil.1` | 1 | +140% | 15.62 | food 750 · gold 250 | — |
| Improve grain crops storage (harvesting +180%) | `eurmil.2` | 2 | +180% | 15.62 | food 25600 · gold 3350 · iron 2000 | Previous upgrade |
| Cultivate new cultures of wheat (harvesting +40%) | `netaca.1` | 1 | +40% | 15.62 | wood 200 · gold 325 | — |
| Cultivate new cultures of rye (harvesting +50%) | `netaca.2` | 1 | +50% | 15.62 | wood 2400 · gold 625 | — |
| Raise agriculturists' salary (harvesting +50%) | `netaca.3` | 1 | +50% | 15.62 | wood 3600 · gold 850 | — |

_Cumulative peak: +460_

<a id="добыча-дерева-7"></a>
#### Tree efficiency

| Upgrade | Upgrade ID | Stage | Bonus | Research time, game s | Cost | Requirements |
| --- | --- | ---: | ---: | ---: | --- | --- |
| Design new woodworking tools (woodcutting efficiency +100%) | `netaca.8` | 1 | +100% | 15.62 | food 5500 · gold 550 | Blacksmith (`netbla`) |

_Cumulative peak: +100_

<a id="добыча-камня-7"></a>
#### Stone efficiency

| Upgrade | Upgrade ID | Stage | Bonus | Research time, game s | Cost | Requirements |
| --- | --- | ---: | ---: | ---: | --- | --- |
| Develop mining (stone excavation efficiency +100%) | `netaca.23` | 1 | +100% | 15.62 | gold 1550 · iron 3000 | — |
| Raise miners' salary (stone excavation efficiency +200%) | `netaca.24` | 1 | +200% | 15.62 | food 4200 · gold 1550 · coal 12520 | — |

_Cumulative peak: +300_

<a id="прочность-полей-7"></a>
#### Field durability

| Upgrade | Upgrade ID | Stage | Bonus | Research time, game s | Cost | Requirements |
| --- | --- | ---: | ---: | ---: | --- | --- |
| Carry out field melioration (field capacity +200%) | `netaca.4` | 1 | +200% | 15.62 | wood 1000 · gold 475 | — |
| Manufacture agricultural equipment (field capacity +100%) | `netbla.1` | 1 | +100% | 15.62 | wood 400 · gold 90 | — |

_Cumulative peak: +300_


<a id="pie--piedmont-пьемонт"></a>
<a id="пьемонт-pie"></a>
### Piedmont (`pie`)
<a id="добыча-еды-8"></a>
#### Food efficiency

| Upgrade | Upgrade ID | Stage | Bonus | Research time, game s | Cost | Requirements |
| --- | --- | ---: | ---: | ---: | --- | --- |
| Improve grain crops treatment (harvesting +140%) | `eurmil.1` | 1 | +140% | 15.62 | food 750 · gold 250 | — |
| Improve grain crops storage (harvesting +180%) | `eurmil.2` | 2 | +180% | 15.62 | food 25600 · gold 3350 · iron 2000 | Previous upgrade |
| Cultivate new cultures of wheat (harvesting +40%) | `pieaca.1` | 1 | +40% | 15.62 | wood 200 · gold 325 | — |
| Cultivate new cultures of rye (harvesting +50%) | `pieaca.2` | 1 | +50% | 15.62 | wood 2400 · gold 625 | — |
| Raise agriculturists' salary (harvesting +50%) | `pieaca.3` | 1 | +50% | 15.62 | wood 3600 · gold 850 | — |

_Cumulative peak: +460_

<a id="добыча-дерева-8"></a>
#### Tree efficiency

| Upgrade | Upgrade ID | Stage | Bonus | Research time, game s | Cost | Requirements |
| --- | --- | ---: | ---: | ---: | --- | --- |
| Design new woodworking tools (woodcutting efficiency +100%) | `pieaca.8` | 1 | +100% | 15.62 | food 5500 · gold 550 | Blacksmith (`piebla`) |

_Cumulative peak: +100_

<a id="добыча-камня-8"></a>
#### Stone efficiency

| Upgrade | Upgrade ID | Stage | Bonus | Research time, game s | Cost | Requirements |
| --- | --- | ---: | ---: | ---: | --- | --- |
| Develop mining (stone excavation efficiency +100%) | `pieaca.23` | 1 | +100% | 15.62 | gold 1550 · iron 3000 | — |
| Raise miners' salary (stone excavation efficiency +200%) | `pieaca.24` | 1 | +200% | 15.62 | food 4200 · gold 1550 · coal 12520 | — |

_Cumulative peak: +300_

<a id="прочность-полей-8"></a>
#### Field durability

| Upgrade | Upgrade ID | Stage | Bonus | Research time, game s | Cost | Requirements |
| --- | --- | ---: | ---: | ---: | --- | --- |
| Carry out field melioration (field capacity +200%) | `pieaca.4` | 1 | +200% | 15.62 | wood 1000 · gold 475 | — |
| Manufacture agricultural equipment (field capacity +100%) | `piebla.1` | 1 | +100% | 15.62 | wood 400 · gold 90 | — |

_Cumulative peak: +300_


<a id="pol--poland-польша"></a>
<a id="польша-pol"></a>
### Poland (`pol`)
<a id="добыча-еды-9"></a>
#### Food efficiency

| Upgrade | Upgrade ID | Stage | Bonus | Research time, game s | Cost | Requirements |
| --- | --- | ---: | ---: | ---: | --- | --- |
| Improve grain crops treatment (harvesting +140%) | `eurmil.1` | 1 | +140% | 15.62 | food 750 · gold 250 | — |
| Improve grain crops storage (harvesting +180%) | `eurmil.2` | 2 | +180% | 15.62 | food 25600 · gold 3350 · iron 2000 | Previous upgrade |
| Cultivate new cultures of wheat (harvesting +40%) | `polaca.1` | 1 | +40% | 15.62 | wood 200 · gold 325 | — |
| Cultivate new cultures of rye (harvesting +50%) | `polaca.2` | 1 | +50% | 15.62 | wood 2400 · gold 625 | — |
| Raise agriculturists' salary (harvesting +50%) | `polaca.3` | 1 | +50% | 15.62 | wood 3600 · gold 850 | — |

_Cumulative peak: +460_

<a id="добыча-дерева-9"></a>
#### Tree efficiency

| Upgrade | Upgrade ID | Stage | Bonus | Research time, game s | Cost | Requirements |
| --- | --- | ---: | ---: | ---: | --- | --- |
| Design new woodworking tools (woodcutting efficiency +100%) | `polaca.8` | 1 | +100% | 15.62 | food 5500 · gold 550 | Blacksmith (`polbla`) |

_Cumulative peak: +100_

<a id="добыча-камня-9"></a>
#### Stone efficiency
| Upgrade | Upgrade ID | Stage | Bonus | Research time, game s | Cost | Requirements |
| --- | --- | ---: | ---: | ---: | --- | --- |
| Develop mining (stone excavation efficiency +100%) | `polaca.23` | 1 | +100% | 15.62 | gold 1550 · iron 3000 | — |
| Raise miners' salary (stone excavation efficiency +200%) | `polaca.24` | 1 | +200% | 15.62 | food 4200 · gold 1550 · coal 12520 | — |

_Cumulative peak: +300_

<a id="прочность-полей-9"></a>
#### Field durability

| Upgrade | Upgrade ID | Stage | Bonus | Research time, game s | Cost | Requirements |
| --- | --- | ---: | ---: | ---: | --- | --- |
| Carry out field melioration (field capacity +200%) | `polaca.4` | 1 | +200% | 15.62 | wood 1000 · gold 475 | — |
| Manufacture agricultural equipment (field capacity +100%) | `polbla.1` | 1 | +100% | 15.62 | wood 400 · gold 90 | — |

_Cumulative peak: +300_


<a id="por--portugal-португалия"></a>
<a id="португалия-por"></a>
### Portugal (`por`)
<a id="эффективность-еды-4"></a>
<a id="добыча-еды-10"></a>
#### Food efficiency

| Upgrade | Upgrade ID | Stage | Bonus | Research time, game s | Cost | Requirements |
| --- | --- | ---: | ---: | ---: | --- | --- |
| Improve grain crops treatment (harvesting +140%) | `eurmil.1` | 1 | +140% | 15.62 | food 750 · gold 250 | — |
| Improve grain crops storage (harvesting +180%) | `eurmil.2` | 2 | +180% | 15.62 | food 25600 · gold 3350 · iron 2000 | Previous upgrade |
| Cultivate new cultures of wheat (harvesting +40%) | `poraca.1` | 1 | +40% | 15.62 | wood 200 · gold 325 | — |
| Cultivate new cultures of rye (harvesting +50%) | `poraca.2` | 1 | +50% | 15.62 | wood 2400 · gold 625 | — |
| Raise agriculturists' salary (harvesting +50%) | `poraca.3` | 1 | +50% | 15.62 | wood 3600 · gold 850 | — |

_Cumulative peak: +460_

<a id="эффективность-дерева-4"></a>
<a id="добыча-дерева-10"></a>
#### Tree efficiency

| Upgrade | Upgrade ID | Stage | Bonus | Research time, game s | Cost | Requirements |
| --- | --- | ---: | ---: | ---: | --- | --- |
| Design new woodworking tools (woodcutting efficiency +100%) | `poraca.8` | 1 | +100% | 15.62 | food 5500 · gold 550 | Blacksmith (`porbla`) |

_Cumulative peak: +100_

<a id="эффективность-камня-3"></a>
<a id="добыча-камня-10"></a>
#### Stone efficiency

| Upgrade | Upgrade ID | Stage | Bonus | Research time, game s | Cost | Requirements |
| --- | --- | ---: | ---: | ---: | --- | --- |
| Develop mining (stone excavation efficiency +100%) | `poraca.23` | 1 | +100% | 15.62 | gold 1550 · iron 3000 | — |
| Raise miners' salary (stone excavation efficiency +200%) | `poraca.24` | 1 | +200% | 15.62 | food 4200 · gold 1550 · coal 12520 | — |

_Cumulative peak: +300_

<a id="прочность-полей-10"></a>
#### Field durability

| Upgrade | Upgrade ID | Stage | Bonus | Research time, game s | Cost | Requirements |
| --- | --- | ---: | ---: | ---: | --- | --- |
| Carry out field melioration (field capacity +200%) | `poraca.4` | 1 | +200% | 15.62 | wood 1000 · gold 475 | — |
| Manufacture agricultural equipment (field capacity +100%) | `porbla.1` | 1 | +100% | 15.62 | wood 400 · gold 90 | — |

_Cumulative peak: +300_


<a id="pru--prussia-пруссия"></a>
<a id="пруссия-pru"></a>
### Prussia (`pru`)
<a id="эффективность-еды-5"></a>
<a id="добыча-еды-11"></a>
#### Food efficiency

| Upgrade | Upgrade ID | Stage | Bonus | Research time, game s | Cost | Requirements |
| --- | --- | ---: | ---: | ---: | --- | --- |
| Improve grain crops treatment (harvesting +140%) | `eurmil.1` | 1 | +140% | 15.62 | food 750 · gold 250 | — |
| Improve grain crops storage (harvesting +180%) | `eurmil.2` | 2 | +180% | 15.62 | food 25600 · gold 3350 · iron 2000 | Previous upgrade |
| Cultivate new cultures of wheat (harvesting +40%) | `pruaca.1` | 1 | +40% | 15.62 | wood 200 · gold 325 | — |
| Cultivate new cultures of rye (harvesting +50%) | `pruaca.2` | 1 | +50% | 15.62 | wood 2400 · gold 625 | — |
| Raise agriculturists' salary (harvesting +50%) | `pruaca.3` | 1 | +50% | 15.62 | wood 3600 · gold 850 | — |

_Cumulative peak: +460_

<a id="эффективность-дерева-5"></a>
<a id="добыча-дерева-11"></a>
#### Tree efficiency

| Upgrade | Upgrade ID | Stage | Bonus | Research time, game s | Cost | Requirements |
| --- | --- | ---: | ---: | ---: | --- | --- |
| Design new woodworking tools (woodcutting efficiency +100%) | `pruaca.8` | 1 | +100% | 15.62 | food 5500 · gold 550 | Blacksmith (`prubla`) |

_Cumulative peak: +100_

<a id="эффективность-камня-4"></a>
<a id="добыча-камня-11"></a>
#### Stone efficiency

| Upgrade | Upgrade ID | Stage | Bonus | Research time, game s | Cost | Requirements |
| --- | --- | ---: | ---: | ---: | --- | --- |
| Develop mining (stone excavation efficiency +100%) | `pruaca.23` | 1 | +100% | 15.62 | gold 1550 · iron 3000 | — |
| Raise miners' salary (stone excavation efficiency +200%) | `pruaca.24` | 1 | +200% | 15.62 | food 4200 · gold 1550 · coal 12520 | — |

_Cumulative peak: +300_

<a id="прочность-полей-11"></a>
#### Field durability

| Upgrade | Upgrade ID | Stage | Bonus | Research time, game s | Cost | Requirements |
| --- | --- | ---: | ---: | ---: | --- | --- |
| Carry out field melioration (field capacity +200%) | `pruaca.4` | 1 | +200% | 15.62 | wood 1000 · gold 475 | — |
| Manufacture agricultural equipment (field capacity +100%) | `prubla.1` | 1 | +100% | 15.62 | wood 400 · gold 90 | — |

_Cumulative peak: +300_


<a id="rus--russia-россия"></a>
<a id="россия-rus"></a>
### Russia (`rus`)
<a id="эффективность-еды-6"></a>
<a id="добыча-еды-12"></a>
#### Food efficiency

| Upgrade | Upgrade ID | Stage | Bonus | Research time, game s | Cost | Requirements |
| --- | --- | ---: | ---: | ---: | --- | --- |
| Cultivate new cultures of wheat (harvesting +40%) | `rusaca.1` | 1 | +40% | 15.62 | wood 200 · gold 325 | — |
| Cultivate new cultures of rye (harvesting +50%) | `rusaca.2` | 1 | +50% | 15.62 | wood 2400 · gold 625 | — |
| Raise agriculturists' salary (harvesting +50%) | `rusaca.3` | 1 | +50% | 15.62 | wood 3600 · gold 850 | — |
| Improve grain crops treatment (harvesting +140%) | `rusmil.1` | 1 | +140% | 15.62 | food 750 · gold 250 | — |
| Improve grain crops storage (harvesting +180%) | `rusmil.2` | 2 | +180% | 15.62 | food 25600 · gold 3350 · iron 2000 | Previous upgrade |

_Cumulative peak: +460_

<a id="эффективность-дерева-6"></a>
<a id="добыча-дерева-12"></a>
#### Tree efficiency

| Upgrade | Upgrade ID | Stage | Bonus | Research time, game s | Cost | Requirements |
| --- | --- | ---: | ---: | ---: | --- | --- |
| Design new woodworking tools (woodcutting efficiency +100%) | `rusaca.8` | 1 | +100% | 15.62 | food 5500 · gold 550 | Blacksmith (`rusbla`) |

_Cumulative peak: +100_

<a id="эффективность-камня-5"></a>
<a id="добыча-камня-12"></a>
#### Stone efficiency

| Upgrade | Upgrade ID | Stage | Bonus | Research time, game s | Cost | Requirements |
| --- | --- | ---: | ---: | ---: | --- | --- |
| Develop mining (stone excavation efficiency +100%) | `rusaca.23` | 1 | +100% | 15.62 | gold 1550 · iron 3000 | — |
| Raise miners' salary (stone excavation efficiency +200%) | `rusaca.24` | 1 | +200% | 15.62 | food 4200 · gold 1550 · coal 12520 | — |

_Cumulative peak: +300_

<a id="прочность-полей-12"></a>
#### Field durability

| Upgrade | Upgrade ID | Stage | Bonus | Research time, game s | Cost | Requirements |
| --- | --- | ---: | ---: | ---: | --- | --- |
| Carry out field melioration (field capacity +200%) | `rusaca.4` | 1 | +200% | 15.62 | wood 1000 · gold 475 | — |
| Manufacture agricultural equipment (field capacity +100%) | `rusbla.1` | 1 | +100% | 15.62 | wood 400 · gold 90 | — |

_Cumulative peak: +300_


<a id="sax--saxony-саксония"></a>
<a id="саксония-sax"></a>
### Saxony (`sax`)
<a id="добыча-еды-13"></a>
#### Food efficiency

| Upgrade | Upgrade ID | Stage | Bonus | Research time, game s | Cost | Requirements |
| --- | --- | ---: | ---: | ---: | --- | --- |
| Improve grain crops treatment (harvesting +140%) | `eurmil.1` | 1 | +140% | 15.62 | food 750 · gold 250 | — |
| Improve grain crops storage (harvesting +180%) | `eurmil.2` | 2 | +180% | 15.62 | food 25600 · gold 3350 · iron 2000 | Previous upgrade |
| Cultivate new cultures of wheat (harvesting +40%) | `saxaca.1` | 1 | +40% | 15.62 | wood 200 · gold 325 | — |
| Cultivate new cultures of rye (harvesting +50%) | `saxaca.2` | 1 | +50% | 15.62 | wood 2400 · gold 625 | — |
| Raise agriculturists' salary (harvesting +50%) | `saxaca.3` | 1 | +50% | 15.62 | wood 3600 · gold 850 | — |

_Cumulative peak: +460_

<a id="добыча-дерева-13"></a>
#### Tree efficiency

| Upgrade | Upgrade ID | Stage | Bonus | Research time, game s | Cost | Requirements |
| --- | --- | ---: | ---: | ---: | --- | --- |
| Design new woodworking tools (woodcutting efficiency +100%) | `saxaca.8` | 1 | +100% | 15.62 | food 5500 · gold 550 | Blacksmith (`saxbla`) |

_Cumulative peak: +100_

<a id="добыча-камня-13"></a>
#### Stone efficiency

| Upgrade | Upgrade ID | Stage | Bonus | Research time, game s | Cost | Requirements |
| --- | --- | ---: | ---: | ---: | --- | --- |
| Develop mining (stone excavation efficiency +100%) | `saxaca.23` | 1 | +100% | 15.62 | gold 1550 · iron 3000 | — |
| Raise miners' salary (stone excavation efficiency +200%) | `saxaca.24` | 1 | +200% | 15.62 | food 4200 · gold 1550 · coal 12520 | — |

_Cumulative peak: +300_

<a id="прочность-полей-13"></a>
#### Field durability

| Upgrade | Upgrade ID | Stage | Bonus | Research time, game s | Cost | Requirements |
| --- | --- | ---: | ---: | ---: | --- | --- |
| Carry out field melioration (field capacity +200%) | `saxaca.4` | 1 | +200% | 15.62 | wood 1000 · gold 475 | — |
| Manufacture agricultural equipment (field capacity +100%) | `saxbla.1` | 1 | +100% | 15.62 | wood 400 · gold 90 | — |

_Cumulative peak: +300_


<a id="sco--scotland-шотландия"></a>
<a id="шотландия-sco"></a>
### Scotland (`sco`)
<a id="добыча-еды-14"></a>
#### Food efficiency

| Upgrade | Upgrade ID | Stage | Bonus | Research time, game s | Cost | Requirements |
| --- | --- | ---: | ---: | ---: | --- | --- |
| Improve grain crops treatment (harvesting +140%) | `eurmil.1` | 1 | +140% | 15.62 | food 750 · gold 250 | — |
| Improve grain crops storage (harvesting +180%) | `eurmil.2` | 2 | +180% | 15.62 | food 5600 · gold 1350 · iron 1900 | Previous upgrade |
| Cultivate new cultures of wheat (harvesting +40%) | `scoaca.1` | 1 | +40% | 15.62 | wood 200 · gold 325 | — |
| Cultivate new cultures of rye (harvesting +50%) | `scoaca.2` | 1 | +50% | 15.62 | wood 2400 · gold 625 | — |
| Raise agriculturists' salary (harvesting +50%) | `scoaca.3` | 1 | +50% | 15.62 | wood 3600 · gold 850 | — |

_Cumulative peak: +460_

<a id="добыча-дерева-14"></a>
#### Tree efficiency

| Upgrade | Upgrade ID | Stage | Bonus | Research time, game s | Cost | Requirements |
| --- | --- | ---: | ---: | ---: | --- | --- |
| Design new woodworking tools (woodcutting efficiency +100%) | `scoaca.8` | 1 | +100% | 15.62 | food 5500 · gold 550 | Blacksmith (`scobla`) |

_Cumulative peak: +100_

<a id="добыча-камня-14"></a>
#### Stone efficiency

| Upgrade | Upgrade ID | Stage | Bonus | Research time, game s | Cost | Requirements |
| --- | --- | ---: | ---: | ---: | --- | --- |
| Develop mining (stone excavation efficiency +100%) | `scoaca.23` | 1 | +100% | 15.62 | gold 1550 · iron 3000 | — |
| Raise miners' salary (stone excavation efficiency +200%) | `scoaca.24` | 1 | +200% | 15.62 | food 4200 · gold 1550 · coal 12520 | — |

_Cumulative peak: +300_

<a id="прочность-полей-14"></a>
#### Field durability

| Upgrade | Upgrade ID | Stage | Bonus | Research time, game s | Cost | Requirements |
| --- | --- | ---: | ---: | ---: | --- | --- |
| Carry out field melioration (field capacity +200%) | `scoaca.4` | 1 | +200% | 15.62 | wood 1000 · gold 475 | — |
| Manufacture agricultural equipment (field capacity +100%) | `scobla.1` | 1 | +100% | 15.62 | wood 400 · gold 90 | — |

_Cumulative peak: +300_


<a id="spa--spain-испания"></a>
<a id="испания-spa"></a>
### Spain (`spa`)
<a id="добыча-еды-15"></a>
#### Food efficiency

| Upgrade | Upgrade ID | Stage | Bonus | Research time, game s | Cost | Requirements |
| --- | --- | ---: | ---: | ---: | --- | --- |
| Improve grain crops treatment (harvesting +140%) | `eurmil.1` | 1 | +140% | 15.62 | food 750 · gold 250 | — |
| Improve grain crops storage (harvesting +180%) | `eurmil.2` | 2 | +180% | 15.62 | food 25600 · gold 3350 · iron 2000 | Previous upgrade |
| Cultivate new cultures of wheat (harvesting +40%) | `spaaca.1` | 1 | +40% | 15.62 | wood 200 · gold 325 | — |
| Cultivate new cultures of rye (harvesting +50%) | `spaaca.2` | 1 | +50% | 15.62 | wood 2400 · gold 625 | — |
| Raise agriculturists' salary (harvesting +50%) | `spaaca.3` | 1 | +50% | 15.62 | wood 3600 · gold 850 | — |

_Cumulative peak: +460_

<a id="добыча-дерева-15"></a>
#### Tree efficiency

| Upgrade | Upgrade ID | Stage | Bonus | Research time, game s | Cost | Requirements |
| --- | --- | ---: | ---: | ---: | --- | --- |
| Design new woodworking tools (woodcutting efficiency +100%) | `spaaca.8` | 1 | +100% | 15.62 | food 5500 · gold 550 | Blacksmith (`spabla`) |

_Cumulative peak: +100_

<a id="добыча-камня-15"></a>
#### Stone efficiency

| Upgrade | Upgrade ID | Stage | Bonus | Research time, game s | Cost | Requirements |
| --- | --- | ---: | ---: | ---: | --- | --- |
| Develop mining (stone excavation efficiency +100%) | `spaaca.23` | 1 | +100% | 15.62 | gold 1550 · iron 3000 | — |
| Raise miners' salary (stone excavation efficiency +200%) | `spaaca.24` | 1 | +200% | 15.62 | food 4200 · gold 1550 · coal 12520 | — |

_Cumulative peak: +300_

<a id="прочность-полей-15"></a>
#### Field durability
| Upgrade | Upgrade ID | Stage | Bonus | Research time, game s | Cost | Requirements |
| --- | --- | ---: | ---: | ---: | --- | --- |
| Carry out field melioration (field capacity +200%) | `spaaca.4` | 1 | +200% | 15.62 | wood 1000 · gold 475 | — |
| Manufacture agricultural equipment (field capacity +100%) | `spabla.1` | 1 | +100% | 15.62 | wood 400 · gold 90 | — |

_Cumulative peak: +300_


<a id="swe--sweden-швеция"></a>
<a id="швеция-swe"></a>
### Sweden (`swe`)
<a id="добыча-еды-16"></a>
#### Food efficiency

| Upgrade | Upgrade ID | Stage | Bonus | Research time, game s | Cost | Requirements |
| --- | --- | ---: | ---: | ---: | --- | --- |
| Improve grain crops treatment (harvesting +140%) | `eurmil.1` | 1 | +140% | 15.62 | food 750 · gold 250 | — |
| Improve grain crops storage (harvesting +180%) | `eurmil.2` | 2 | +180% | 15.62 | food 25600 · gold 3350 · iron 2000 | Previous upgrade |
| Cultivate new cultures of wheat (harvesting +40%) | `sweaca.1` | 1 | +40% | 15.62 | wood 200 · gold 325 | — |
| Cultivate new cultures of rye (harvesting +50%) | `sweaca.2` | 1 | +50% | 15.62 | wood 2400 · gold 625 | — |
| Raise agriculturists' salary (harvesting +50%) | `sweaca.3` | 1 | +50% | 15.62 | wood 3600 · gold 850 | — |

_Cumulative peak: +460_

<a id="добыча-дерева-16"></a>
#### Tree efficiency

| Upgrade | Upgrade ID | Stage | Bonus | Research time, game s | Cost | Requirements |
| --- | --- | ---: | ---: | ---: | --- | --- |
| Design new woodworking tools (woodcutting efficiency +100%) | `sweaca.8` | 1 | +100% | 15.62 | food 5500 · gold 550 | Blacksmith (`swebla`) |

_Cumulative peak: +100_

<a id="добыча-камня-16"></a>
#### Stone efficiency

| Upgrade | Upgrade ID | Stage | Bonus | Research time, game s | Cost | Requirements |
| --- | --- | ---: | ---: | ---: | --- | --- |
| Develop mining (stone excavation efficiency +100%) | `sweaca.23` | 1 | +100% | 15.62 | gold 1550 · iron 3000 | — |
| Raise miners' salary (stone excavation efficiency +200%) | `sweaca.24` | 1 | +200% | 15.62 | food 4200 · gold 1550 · coal 12520 | — |

_Cumulative peak: +300_

<a id="прочность-полей-16"></a>
#### Field durability

| Upgrade | Upgrade ID | Stage | Bonus | Research time, game s | Cost | Requirements |
| --- | --- | ---: | ---: | ---: | --- | --- |
| Carry out field melioration (field capacity +200%) | `sweaca.4` | 1 | +200% | 15.62 | wood 1000 · gold 475 | — |
| Manufacture agricultural equipment (field capacity +100%) | `swebla.1` | 1 | +100% | 15.62 | wood 400 · gold 90 | — |

_Cumulative peak: +300_


<a id="swi--switzerland-швейцария"></a>
<a id="швейцария-swi"></a>
### Switzerland (`swi`)
<a id="добыча-еды-17"></a>
#### Food efficiency

| Upgrade | Upgrade ID | Stage | Bonus | Research time, game s | Cost | Requirements |
| --- | --- | ---: | ---: | ---: | --- | --- |
| Improve grain crops treatment (harvesting +140%) | `eurmil.1` | 1 | +140% | 15.62 | food 750 · gold 250 | — |
| Improve grain crops storage (harvesting +180%) | `eurmil.2` | 2 | +180% | 15.62 | food 25600 · gold 3350 · iron 2000 | Previous upgrade |
| Cultivate new cultures of wheat (harvesting +40%) | `swiaca.1` | 1 | +40% | 15.62 | wood 200 · gold 325 | — |
| Cultivate new cultures of rye (harvesting +50%) | `swiaca.2` | 1 | +50% | 15.62 | wood 2400 · gold 625 | — |
| Raise agriculturists' salary (harvesting +50%) | `swiaca.3` | 1 | +50% | 15.62 | wood 3600 · gold 850 | — |

_Cumulative peak: +460_

<a id="добыча-дерева-17"></a>
#### Tree efficiency

| Upgrade | Upgrade ID | Stage | Bonus | Research time, game s | Cost | Requirements |
| --- | --- | ---: | ---: | ---: | --- | --- |
| Design new woodworking tools (woodcutting efficiency +100%) | `swiaca.8` | 1 | +100% | 15.62 | food 5500 · gold 550 | Blacksmith (`swibla`) |

_Cumulative peak: +100_

<a id="добыча-камня-17"></a>
#### Stone efficiency

| Upgrade | Upgrade ID | Stage | Bonus | Research time, game s | Cost | Requirements |
| --- | --- | ---: | ---: | ---: | --- | --- |
| Develop mining (stone excavation efficiency +100%) | `swiaca.23` | 1 | +100% | 15.62 | gold 1550 · iron 3000 | — |
| Raise miners' salary (stone excavation efficiency +200%) | `swiaca.24` | 1 | +200% | 15.62 | food 4200 · gold 1550 · coal 12520 | — |

_Cumulative peak: +300_

<a id="прочность-полей-17"></a>
#### Field durability

| Upgrade | Upgrade ID | Stage | Bonus | Research time, game s | Cost | Requirements |
| --- | --- | ---: | ---: | ---: | --- | --- |
| Carry out field melioration (field capacity +200%) | `swiaca.4` | 1 | +200% | 15.62 | wood 1000 · gold 475 | — |
| Manufacture agricultural equipment (field capacity +100%) | `swibla.1` | 1 | +100% | 15.62 | wood 400 · gold 90 | — |

_Cumulative peak: +300_


<a id="tur--turkey-турция"></a>
<a id="турция-tur"></a>
### Turkey (`tur`)
<a id="добыча-еды-18"></a>
#### Food efficiency

| Upgrade | Upgrade ID | Stage | Bonus | Research time, game s | Cost | Requirements |
| --- | --- | ---: | ---: | ---: | --- | --- |
| Cultivate new cultures of wheat (harvesting +40%) | `turaca.1` | 1 | +40% | 15.62 | wood 200 · gold 325 | — |
| Cultivate new cultures of rye (harvesting +50%) | `turaca.2` | 1 | +50% | 15.62 | wood 400 · gold 522 | — |
| Raise agriculturists' salary (harvesting +50%) | `turaca.3` | 1 | +50% | 15.62 | wood 2400 · gold 850 | — |
| Improve grain crops treatment (harvesting +140%) | `turmil.1` | 1 | +140% | 15.62 | food 600 · gold 250 | — |

_Cumulative peak: +280_

<a id="добыча-дерева-18"></a>
#### Tree efficiency

| Upgrade | Upgrade ID | Stage | Bonus | Research time, game s | Cost | Requirements |
| --- | --- | ---: | ---: | ---: | --- | --- |
| Design new woodworking tools (woodcutting efficiency +100%) | `turaca.8` | 1 | +100% | 15.62 | food 5500 · gold 550 | Blacksmith (`turbla`) |

_Cumulative peak: +100_

<a id="добыча-камня-18"></a>
#### Stone efficiency

| Upgrade | Upgrade ID | Stage | Bonus | Research time, game s | Cost | Requirements |
| --- | --- | ---: | ---: | ---: | --- | --- |
| Develop mining (stone excavation efficiency +100%) | `turaca.23` | 1 | +100% | 15.62 | gold 1550 · iron 3000 | — |
| Raise miners' salary (stone excavation efficiency +200%) | `turaca.24` | 1 | +200% | 15.62 | food 4200 · gold 1550 · coal 12520 | — |

_Cumulative peak: +300_

<a id="прочность-полей-18"></a>
#### Field durability

| Upgrade | Upgrade ID | Stage | Bonus | Research time, game s | Cost | Requirements |
| --- | --- | ---: | ---: | ---: | --- | --- |
| Carry out field melioration (field capacity +200%) | `turaca.4` | 1 | +200% | 15.62 | wood 1000 · gold 475 | — |
| Manufacture agricultural equipment (field capacity +100%) | `turbla.1` | 1 | +100% | 15.62 | wood 400 · gold 90 | — |
_Cumulative peak: +300_


<a id="ukr--ukraine-украина"></a>
<a id="украина-ukr"></a>
### Ukraine (`ukr`)
<a id="добыча-еды-19"></a>
#### Food efficiency

| Upgrade | Upgrade ID | Stage | Bonus | Research time, game s | Cost | Requirements |
| --- | --- | ---: | ---: | ---: | --- | --- |
| Improve grain crops treatment (harvesting +140%) | `rusmil.1` | 1 | +140% | 15.62 | food 750 · gold 250 | — |
| Improve grain crops storage (harvesting +180%) | `rusmil.2` | 2 | +180% | 15.62 | food 5600 · gold 1350 · iron 1900 | Previous upgrade |
| Cultivate new cultures of wheat (harvesting +40%) | `ukraca.1` | 1 | +40% | 15.62 | wood 200 · gold 325 | — |
| Cultivate new cultures of rye (harvesting +50%) | `ukraca.2` | 1 | +50% | 15.62 | wood 2400 · gold 625 | — |
| Raise agriculturists' salary (harvesting +50%) | `ukraca.3` | 1 | +50% | 15.62 | wood 3600 · gold 850 | — |

_Cumulative peak: +460_

<a id="добыча-дерева-19"></a>
#### Tree efficiency

| Upgrade | Upgrade ID | Stage | Bonus | Research time, game s | Cost | Requirements |
| --- | --- | ---: | ---: | ---: | --- | --- |
| Design new woodworking tools (woodcutting efficiency +100%) | `ukraca.8` | 1 | +100% | 15.62 | food 5500 · gold 550 | Blacksmith (`ukrbla`) |

_Cumulative peak: +100_

<a id="добыча-камня-19"></a>
#### Stone efficiency

| Upgrade | Upgrade ID | Stage | Bonus | Research time, game s | Cost | Requirements |
| --- | --- | ---: | ---: | ---: | --- | --- |
| Develop mining (stone excavation efficiency +100%) | `ukraca.23` | 1 | +100% | 15.62 | gold 1550 · iron 3000 | — |
| Raise miners' salary (stone excavation efficiency +200%) | `ukraca.24` | 1 | +200% | 15.62 | food 4200 · gold 1550 · coal 12520 | — |

_Cumulative peak: +300_

<a id="прочность-полей-19"></a>
#### Field durability

| Upgrade | Upgrade ID | Stage | Bonus | Research time, game s | Cost | Requirements |
| --- | --- | ---: | ---: | ---: | --- | --- |
| Carry out field melioration (field capacity +200%) | `ukraca.4` | 1 | +200% | 15.62 | wood 1000 · gold 475 | — |
| Manufacture agricultural equipment (field capacity +100%) | `ukrbla.1` | 1 | +100% | 15.62 | wood 400 · gold 90 | — |

_Cumulative peak: +300_


<a id="ven--venice-венеция"></a>
<a id="венеция-ven"></a>
### Venice (`ven`)
<a id="добыча-еды-20"></a>
#### Food efficiency

| Upgrade | Upgrade ID | Stage | Bonus | Research time, game s | Cost | Requirements |
| --- | --- | ---: | ---: | ---: | --- | --- |
| Improve grain crops treatment (harvesting +140%) | `eurmil.1` | 1 | +140% | 15.62 | food 750 · gold 250 | — |
| Improve grain crops storage (harvesting +180%) | `eurmil.2` | 2 | +180% | 15.62 | food 25600 · gold 3350 · iron 2000 | Previous upgrade |
| Cultivate new cultures of wheat (harvesting +40%) | `venaca.1` | 1 | +40% | 15.62 | wood 200 · gold 325 | — |
| Cultivate new cultures of rye (harvesting +50%) | `venaca.2` | 1 | +50% | 15.62 | wood 2400 · gold 625 | — |
| Raise agriculturists' salary (harvesting +50%) | `venaca.3` | 1 | +50% | 15.62 | wood 3600 · gold 850 | — |

_Cumulative peak: +460_

<a id="добыча-дерева-20"></a>
#### Tree efficiency

| Upgrade | Upgrade ID | Stage | Bonus | Research time, game s | Cost | Requirements |
| --- | --- | ---: | ---: | ---: | --- | --- |
| Design new woodworking tools (woodcutting efficiency +100%) | `venaca.8` | 1 | +100% | 15.62 | food 5500 · gold 550 | Blacksmith (`venbla`) |

_Cumulative peak: +100_

<a id="добыча-камня-20"></a>
#### Stone efficiency

| Upgrade | Upgrade ID | Stage | Bonus | Research time, game s | Cost | Requirements |
| --- | --- | ---: | ---: | ---: | --- | --- |
| Develop mining (stone excavation efficiency +100%) | `venaca.23` | 1 | +100% | 15.62 | gold 1550 · iron 3000 | — |
| Raise miners' salary (stone excavation efficiency +200%) | `venaca.24` | 1 | +200% | 15.62 | food 4200 · gold 1550 · coal 12520 | — |

_Cumulative peak: +300_

<a id="прочность-полей-20"></a>
#### Field durability

| Upgrade | Upgrade ID | Stage | Bonus | Research time, game s | Cost | Requirements |
| --- | --- | ---: | ---: | ---: | --- | --- |
| Carry out field melioration (field capacity +200%) | `venaca.4` | 1 | +200% | 15.62 | wood 1000 · gold 475 | — |
| Manufacture agricultural equipment (field capacity +100%) | `venbla.1` | 1 | +100% | 15.62 | wood 400 · gold 90 | — |

_Cumulative peak: +300_



<a id="источники"></a>
## Sources

All links are relative to `data/scripts/` in the Cossacks 3 installation.

[^1]: Applying `gc_upg_type_effect*perc` to `resefficiency[res]` —
      `lib/player.script:1812+`.

[^2]: Gathering formula `delivered = floor(portion × efficiency / 100)` —
      `lib/unit.script:9551-9555`.
