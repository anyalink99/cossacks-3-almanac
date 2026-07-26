<a id="улучшения-добычи-по-нациям"></a>
# Cossacks 3 — Efficiency upgrades per nation

[← Tables and calculations](../README.md)

**Derived** file (calculated, not extracted). Considered from `data.json` script [`compute/compute_efficiency_upgrades.py`](../../../compute/compute_efficiency_upgrades.py).

<a id="что-это"></a>
<a id="как-складываются-бонусы"></a>
## What is this

Each upgrade `gc_upg_type_effect{food,wood,stone}[perc]` **additively** adds `value` to `resefficiency[res]` [^1]. Base = 100. The formula for loot per hit is: `delivered = floor(portion × eff / 100)`, where `portion` = 45/28/40 for food/wood/stone [^2].

`gc_upg_type_fieldlifeperc` additively adds fields to `objbase.fieldlife`. Reduces field damage/impact by `100 / (1 + fieldlife/100)` - increases output per cycle and reduces restart frequency.

<a id="сводка-по-нациям-кумулятивные-пики"></a>
<a id="максимальный-бонус-по-нациям"></a>
## Summary by nation (cumulative peaks)

The sum of all values in the line = the peak for the nation, if you examine ALL relevant upgrades. In practice, some upgrades are exclusive (one building with .1..6 steps), but the script summarizes everything - this is the **upper limit**.

| Nation | food eff % | wood eff % | stone eff % | fieldlife % | Σ upgrades |
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

**Top picks for all nations:**
- Food efficiency: **+460** — aus, bav, den, … (19 nations tied)
- Tree efficiency: **+100** — alg, aus, bav, … (21 nations tied)
- Stone effectiveness: **+300** — alg, aus, bav, … (21 nations tied)
- HP of fields (fieldlife): **+300** — alg, aus, bav, … (21 nations tied)

**Cheapest food-eff progression (total gold for ALL food-eff upgrades):**

| Nation | total gold | total food | total wood |
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
<a id="стоимость-всей-цепочки-улучшений-еды"></a>
## Detail by nation

Each cost cell is the cost of **this** upgrade (not total).

<a id="alg--algeria-алжир"></a>
<a id="алжир-alg"></a>
### Algeria (`alg`)
<a id="эффективность-еды"></a>
<a id="добыча-еды"></a>
#### Food efficiency

| sid | lvl | +value | time (g-s) | cost | prereqs |
| --- | ---: | ---: | ---: | --- | --- |
| `algaca.1` | 1 | +40 | 15.62 | W200 G325 | — |
| `algaca.2` | 1 | +50 | 15.62 | W400 G522 | — |
| `algaca.3` | 1 | +50 | 15.62 | W1240 G850 | — |
| `turmil.1` | 1 | +140 | 15.62 | F600 G250 | — |

_Cumulative peak: +280_

<a id="добыча-дерева"></a>
#### Tree efficiency

| sid | lvl | +value | time (g-s) | cost | prereqs |
| --- | ---: | ---: | ---: | --- | --- |
| `algaca.8` | 1 | +100 | 15.62 | F5500 G550 | algbla |

_Cumulative peak: +100_

<a id="добыча-камня"></a>
#### Efficiency of the stone

| sid | lvl | +value | time (g-s) | cost | prereqs |
| --- | ---: | ---: | ---: | --- | --- |
| `algaca.23` | 1 | +100 | 15.62 | G1550 I3000 | — |
| `algaca.24` | 1 | +200 | 15.62 | F4200 G1550 C12520 | — |

_Cumulative peak: +300_

####HP fields (fieldlife)

| sid | lvl | +value | time (g-s) | cost | prereqs |
| --- | ---: | ---: | ---: | --- | --- |
| `algaca.4` | 1 | +200 | 15.62 | W700 G475 | — |
| `algbla.1` | 1 | +100 | 15.62 | W400 G90 | — |

_Cumulative peak: +300_


<a id="aus--austria-австрия"></a>
<a id="австрия-aus"></a>
### Austria (`aus`)
#### Food efficiency

| sid | lvl | +value | time (g-s) | cost | prereqs |
| --- | ---: | ---: | ---: | --- | --- |
| `ausaca.1` | 1 | +40 | 15.62 | W200 G325 | — |
| `ausaca.2` | 1 | +50 | 15.62 | W2400 G625 | — |
| `ausaca.3` | 1 | +50 | 15.62 | W3600 G850 | — |
| `eurmil.1` | 1 | +140 | 15.62 | F750 G250 | — |
| `eurmil.2` | 2 | +180 | 15.62 | F25600 G3350 I2000 | req0 |

_Cumulative peak: +460_

#### Tree efficiency

| sid | lvl | +value | time (g-s) | cost | prereqs |
| --- | ---: | ---: | ---: | --- | --- |
| `ausaca.8` | 1 | +100 | 15.62 | F5500 G550 | ausbla |

_Cumulative peak: +100_

#### Efficiency of the stone

| sid | lvl | +value | time (g-s) | cost | prereqs |
| --- | ---: | ---: | ---: | --- | --- |
| `ausaca.23` | 1 | +100 | 15.62 | G1550 I3000 | — |
| `ausaca.24` | 1 | +200 | 15.62 | F4200 G1550 C12520 | — |

_Cumulative peak: +300_

####HP fields (fieldlife)

| sid | lvl | +value | time (g-s) | cost | prereqs |
| --- | ---: | ---: | ---: | --- | --- |
| `ausaca.4` | 1 | +200 | 15.62 | W1000 G475 | — |
| `ausbla.1` | 1 | +100 | 15.62 | W400 G90 | — |

_Cumulative peak: +300_


<a id="bav--bavaria-бавария"></a>
<a id="бавария-bav"></a>
### Bavaria (`bav`)
#### Food efficiency

| sid | lvl | +value | time (g-s) | cost | prereqs |
| --- | ---: | ---: | ---: | --- | --- |
| `bavaca.1` | 1 | +40 | 15.62 | W200 G325 | — |
| `bavaca.2` | 1 | +50 | 15.62 | W2400 G625 | — |
| `bavaca.3` | 1 | +50 | 15.62 | W3600 G850 | — |
| `eurmil.1` | 1 | +140 | 15.62 | F750 G250 | — |
| `eurmil.2` | 2 | +180 | 15.62 | F25600 G3350 I2000 | req0 |

_Cumulative peak: +460_

#### Tree efficiency

| sid | lvl | +value | time (g-s) | cost | prereqs |
| --- | ---: | ---: | ---: | --- | --- |
| `bavaca.8` | 1 | +100 | 15.62 | F5500 G550 | bavbla |

_Cumulative peak: +100_

#### Efficiency of the stone

| sid | lvl | +value | time (g-s) | cost | prereqs |
| --- | ---: | ---: | ---: | --- | --- |
| `bavaca.23` | 1 | +100 | 15.62 | G1550 I3000 | — |
| `bavaca.24` | 1 | +200 | 15.62 | F4200 G1550 C12520 | — |

_Cumulative peak: +300_

####HP fields (fieldlife)

| sid | lvl | +value | time (g-s) | cost | prereqs |
| --- | ---: | ---: | ---: | --- | --- |
| `bavaca.4` | 1 | +200 | 15.62 | W1000 G475 | — |
| `bavbla.1` | 1 | +100 | 15.62 | W400 G90 | — |

_Cumulative peak: +300_


<a id="den--denmark-дания"></a>
<a id="дания-den"></a>
### Denmark (`den`)
#### Food efficiency

| sid | lvl | +value | time (g-s) | cost | prereqs |
| --- | ---: | ---: | ---: | --- | --- |
| `denaca.1` | 1 | +40 | 15.62 | W200 G325 | — |
| `denaca.2` | 1 | +50 | 15.62 | W2400 G625 | — |
| `denaca.3` | 1 | +50 | 15.62 | W3600 G850 | — |
| `eurmil.1` | 1 | +140 | 15.62 | F750 G250 | — |
| `eurmil.2` | 2 | +180 | 15.62 | F25600 G3350 I2000 | req0 |
_Cumulative peak: +460_

<a id="эффективность-дерева"></a>
#### Tree efficiency

| sid | lvl | +value | time (g-s) | cost | prereqs |
| --- | ---: | ---: | ---: | --- | --- |
| `denaca.8` | 1 | +100 | 15.62 | F5500 G550 | denbla |

_Cumulative peak: +100_

<a id="эффективность-камня"></a>
#### Efficiency of the stone

| sid | lvl | +value | time (g-s) | cost | prereqs |
| --- | ---: | ---: | ---: | --- | --- |
| `denaca.23` | 1 | +100 | 15.62 | G1550 I3000 | — |
| `denaca.24` | 1 | +200 | 15.62 | F4200 G1550 C12520 | — |

_Cumulative peak: +300_

####HP fields (fieldlife)

| sid | lvl | +value | time (g-s) | cost | prereqs |
| --- | ---: | ---: | ---: | --- | --- |
| `denaca.4` | 1 | +200 | 15.62 | W1000 G475 | — |
| `denbla.1` | 1 | +100 | 15.62 | W400 G90 | — |

_Cumulative peak: +300_


<a id="eng--england-англия"></a>
<a id="англия-eng"></a>
### England (`eng`)
<a id="эффективность-еды"></a>
#### Food efficiency

| sid | lvl | +value | time (g-s) | cost | prereqs |
| --- | ---: | ---: | ---: | --- | --- |
| `engaca.1` | 1 | +40 | 15.62 | W200 G325 | — |
| `engaca.2` | 1 | +50 | 15.62 | W2400 G625 | — |
| `engaca.3` | 1 | +50 | 15.62 | W3600 G850 | — |
| `eurmil.1` | 1 | +140 | 15.62 | F750 G250 | — |
| `eurmil.2` | 2 | +180 | 15.62 | F25600 G3350 I2000 | req0 |

_Cumulative peak: +460_

<a id="эффективность-дерева"></a>
#### Tree efficiency

| sid | lvl | +value | time (g-s) | cost | prereqs |
| --- | ---: | ---: | ---: | --- | --- |
| `engaca.8` | 1 | +100 | 15.62 | F5500 G550 | engbla |

_Cumulative peak: +100_

<a id="эффективность-камня"></a>
#### Efficiency of the stone

| sid | lvl | +value | time (g-s) | cost | prereqs |
| --- | ---: | ---: | ---: | --- | --- |
| `engaca.23` | 1 | +100 | 15.62 | G1550 I3000 | — |
| `engaca.24` | 1 | +200 | 15.62 | F4200 G1550 C12520 | — |

_Cumulative peak: +300_

####HP fields (fieldlife)

| sid | lvl | +value | time (g-s) | cost | prereqs |
| --- | ---: | ---: | ---: | --- | --- |
| `engaca.4` | 1 | +200 | 15.62 | W1000 G475 | — |
| `engbla.1` | 1 | +100 | 15.62 | W400 G90 | — |

_Cumulative peak: +300_


<a id="fra--france-франция"></a>
<a id="франция-fra"></a>
### France (`fra`)
<a id="эффективность-еды"></a>
#### Food efficiency

| sid | lvl | +value | time (g-s) | cost | prereqs |
| --- | ---: | ---: | ---: | --- | --- |
| `eurmil.1` | 1 | +140 | 15.62 | F750 G250 | — |
| `eurmil.2` | 2 | +180 | 15.62 | F25600 G3350 I2000 | req0 |
| `fraaca.1` | 1 | +40 | 15.62 | W190 G315 | — |
| `fraaca.2` | 1 | +50 | 15.62 | W2400 G625 | — |
| `fraaca.3` | 1 | +50 | 15.62 | W3600 G850 | — |

_Cumulative peak: +460_

<a id="эффективность-дерева"></a>
#### Tree efficiency

| sid | lvl | +value | time (g-s) | cost | prereqs |
| --- | ---: | ---: | ---: | --- | --- |
| `fraaca.8` | 1 | +100 | 15.62 | F5500 G550 | frabla |

_Cumulative peak: +100_

<a id="эффективность-камня"></a>
#### Efficiency of the stone

| sid | lvl | +value | time (g-s) | cost | prereqs |
| --- | ---: | ---: | ---: | --- | --- |
| `fraaca.23` | 1 | +100 | 15.62 | G1550 I3000 | — |
| `fraaca.24` | 1 | +200 | 15.62 | F4200 G1550 C12520 | — |

_Cumulative peak: +300_

####HP fields (fieldlife)

| sid | lvl | +value | time (g-s) | cost | prereqs |
| --- | ---: | ---: | ---: | --- | --- |
| `fraaca.4` | 1 | +200 | 15.62 | W1000 G475 | — |
| `frabla.1` | 1 | +100 | 15.62 | W400 G90 | — |

_Cumulative peak: +300_


<a id="hun--hungary-венгрия"></a>
<a id="венгрия-hun"></a>
### Hungary (`hun`)
<a id="эффективность-еды"></a>
#### Food efficiency

| sid | lvl | +value | time (g-s) | cost | prereqs |
| --- | ---: | ---: | ---: | --- | --- |
| `eurmil.1` | 1 | +140 | 15.62 | F750 G250 | — |
| `eurmil.2` | 2 | +180 | 15.62 | F25600 G3350 I2000 | req0 |
| `hunaca.1` | 1 | +40 | 15.62 | W200 G325 | — |
| `hunaca.2` | 1 | +50 | 15.62 | W2400 G625 | — |
| `hunaca.3` | 1 | +50 | 15.62 | W3600 G850 | — |

_Cumulative peak: +460_

<a id="эффективность-дерева"></a>
#### Tree efficiency

| sid | lvl | +value | time (g-s) | cost | prereqs |
| --- | ---: | ---: | ---: | --- | --- |
| `hunaca.8` | 1 | +100 | 15.62 | F5500 G550 | hunbla |

_Cumulative peak: +100_

#### Efficiency of the stone

| sid | lvl | +value | time (g-s) | cost | prereqs |
| --- | ---: | ---: | ---: | --- | --- |
| `hunaca.23` | 1 | +100 | 15.62 | G1550 I3000 | — |
| `hunaca.24` | 1 | +200 | 15.62 | F4200 G1550 C12520 | — |

_Cumulative peak: +300_

####HP fields (fieldlife)

| sid | lvl | +value | time (g-s) | cost | prereqs |
| --- | ---: | ---: | ---: | --- | --- |
| `hunaca.4` | 1 | +200 | 15.62 | W1000 G475 | — |
| `hunbla.1` | 1 | +100 | 15.62 | W400 G90 | — |

_Cumulative peak: +300_


<a id="net--netherlands-нидерланды"></a>
<a id="нидерланды-net"></a>
### Netherlands (`net`)
#### Food efficiency

| sid | lvl | +value | time (g-s) | cost | prereqs |
| --- | ---: | ---: | ---: | --- | --- |
| `eurmil.1` | 1 | +140 | 15.62 | F750 G250 | — |
| `eurmil.2` | 2 | +180 | 15.62 | F25600 G3350 I2000 | req0 |
| `netaca.1` | 1 | +40 | 15.62 | W200 G325 | — |
| `netaca.2` | 1 | +50 | 15.62 | W2400 G625 | — |
| `netaca.3` | 1 | +50 | 15.62 | W3600 G850 | — |

_Cumulative peak: +460_

#### Tree efficiency

| sid | lvl | +value | time (g-s) | cost | prereqs |
| --- | ---: | ---: | ---: | --- | --- |
| `netaca.8` | 1 | +100 | 15.62 | F5500 G550 | netbla |

_Cumulative peak: +100_

#### Efficiency of the stone

| sid | lvl | +value | time (g-s) | cost | prereqs |
| --- | ---: | ---: | ---: | --- | --- |
| `netaca.23` | 1 | +100 | 15.62 | G1550 I3000 | — |
| `netaca.24` | 1 | +200 | 15.62 | F4200 G1550 C12520 | — |

_Cumulative peak: +300_

####HP fields (fieldlife)

| sid | lvl | +value | time (g-s) | cost | prereqs |
| --- | ---: | ---: | ---: | --- | --- |
| `netaca.4` | 1 | +200 | 15.62 | W1000 G475 | — |
| `netbla.1` | 1 | +100 | 15.62 | W400 G90 | — |

_Cumulative peak: +300_


<a id="pie--piedmont-пьемонт"></a>
<a id="пьемонт-pie"></a>
### Piedmont (`pie`)
#### Food efficiency

| sid | lvl | +value | time (g-s) | cost | prereqs |
| --- | ---: | ---: | ---: | --- | --- |
| `eurmil.1` | 1 | +140 | 15.62 | F750 G250 | — |
| `eurmil.2` | 2 | +180 | 15.62 | F25600 G3350 I2000 | req0 |
| `pieaca.1` | 1 | +40 | 15.62 | W200 G325 | — |
| `pieaca.2` | 1 | +50 | 15.62 | W2400 G625 | — |
| `pieaca.3` | 1 | +50 | 15.62 | W3600 G850 | — |

_Cumulative peak: +460_

#### Tree efficiency

| sid | lvl | +value | time (g-s) | cost | prereqs |
| --- | ---: | ---: | ---: | --- | --- |
| `pieaca.8` | 1 | +100 | 15.62 | F5500 G550 | piebla |

_Cumulative peak: +100_

#### Efficiency of the stone

| sid | lvl | +value | time (g-s) | cost | prereqs |
| --- | ---: | ---: | ---: | --- | --- |
| `pieaca.23` | 1 | +100 | 15.62 | G1550 I3000 | — |
| `pieaca.24` | 1 | +200 | 15.62 | F4200 G1550 C12520 | — |

_Cumulative peak: +300_

####HP fields (fieldlife)

| sid | lvl | +value | time (g-s) | cost | prereqs |
| --- | ---: | ---: | ---: | --- | --- |
| `pieaca.4` | 1 | +200 | 15.62 | W1000 G475 | — |
| `piebla.1` | 1 | +100 | 15.62 | W400 G90 | — |

_Cumulative peak: +300_


<a id="pol--poland-польша"></a>
<a id="польша-pol"></a>
### Poland (`pol`)
#### Food efficiency

| sid | lvl | +value | time (g-s) | cost | prereqs |
| --- | ---: | ---: | ---: | --- | --- |
| `eurmil.1` | 1 | +140 | 15.62 | F750 G250 | — |
| `eurmil.2` | 2 | +180 | 15.62 | F25600 G3350 I2000 | req0 |
| `polaca.1` | 1 | +40 | 15.62 | W200 G325 | — |
| `polaca.2` | 1 | +50 | 15.62 | W2400 G625 | — |
| `polaca.3` | 1 | +50 | 15.62 | W3600 G850 | — |

_Cumulative peak: +460_

#### Tree efficiency

| sid | lvl | +value | time (g-s) | cost | prereqs |
| --- | ---: | ---: | ---: | --- | --- |
| `polaca.8` | 1 | +100 | 15.62 | F5500 G550 | polbla |

_Cumulative peak: +100_

#### Efficiency of the stone
| sid | lvl | +value | time (g-s) | cost | prereqs |
| --- | ---: | ---: | ---: | --- | --- |
| `polaca.23` | 1 | +100 | 15.62 | G1550 I3000 | — |
| `polaca.24` | 1 | +200 | 15.62 | F4200 G1550 C12520 | — |

_Cumulative peak: +300_

####HP fields (fieldlife)

| sid | lvl | +value | time (g-s) | cost | prereqs |
| --- | ---: | ---: | ---: | --- | --- |
| `polaca.4` | 1 | +200 | 15.62 | W1000 G475 | — |
| `polbla.1` | 1 | +100 | 15.62 | W400 G90 | — |

_Cumulative peak: +300_


<a id="por--portugal-португалия"></a>
<a id="португалия-por"></a>
### Portugal (`por`)
<a id="эффективность-еды"></a>
#### Food efficiency

| sid | lvl | +value | time (g-s) | cost | prereqs |
| --- | ---: | ---: | ---: | --- | --- |
| `eurmil.1` | 1 | +140 | 15.62 | F750 G250 | — |
| `eurmil.2` | 2 | +180 | 15.62 | F25600 G3350 I2000 | req0 |
| `poraca.1` | 1 | +40 | 15.62 | W200 G325 | — |
| `poraca.2` | 1 | +50 | 15.62 | W2400 G625 | — |
| `poraca.3` | 1 | +50 | 15.62 | W3600 G850 | — |

_Cumulative peak: +460_

<a id="эффективность-дерева"></a>
#### Tree efficiency

| sid | lvl | +value | time (g-s) | cost | prereqs |
| --- | ---: | ---: | ---: | --- | --- |
| `poraca.8` | 1 | +100 | 15.62 | F5500 G550 | porbla |

_Cumulative peak: +100_

<a id="эффективность-камня"></a>
#### Efficiency of the stone

| sid | lvl | +value | time (g-s) | cost | prereqs |
| --- | ---: | ---: | ---: | --- | --- |
| `poraca.23` | 1 | +100 | 15.62 | G1550 I3000 | — |
| `poraca.24` | 1 | +200 | 15.62 | F4200 G1550 C12520 | — |

_Cumulative peak: +300_

####HP fields (fieldlife)

| sid | lvl | +value | time (g-s) | cost | prereqs |
| --- | ---: | ---: | ---: | --- | --- |
| `poraca.4` | 1 | +200 | 15.62 | W1000 G475 | — |
| `porbla.1` | 1 | +100 | 15.62 | W400 G90 | — |

_Cumulative peak: +300_


<a id="pru--prussia-пруссия"></a>
<a id="пруссия-pru"></a>
### Prussia (`pru`)
<a id="эффективность-еды"></a>
#### Food efficiency

| sid | lvl | +value | time (g-s) | cost | prereqs |
| --- | ---: | ---: | ---: | --- | --- |
| `eurmil.1` | 1 | +140 | 15.62 | F750 G250 | — |
| `eurmil.2` | 2 | +180 | 15.62 | F25600 G3350 I2000 | req0 |
| `pruaca.1` | 1 | +40 | 15.62 | W200 G325 | — |
| `pruaca.2` | 1 | +50 | 15.62 | W2400 G625 | — |
| `pruaca.3` | 1 | +50 | 15.62 | W3600 G850 | — |

_Cumulative peak: +460_

<a id="эффективность-дерева"></a>
#### Tree efficiency

| sid | lvl | +value | time (g-s) | cost | prereqs |
| --- | ---: | ---: | ---: | --- | --- |
| `pruaca.8` | 1 | +100 | 15.62 | F5500 G550 | prubla |

_Cumulative peak: +100_

<a id="эффективность-камня"></a>
#### Efficiency of the stone

| sid | lvl | +value | time (g-s) | cost | prereqs |
| --- | ---: | ---: | ---: | --- | --- |
| `pruaca.23` | 1 | +100 | 15.62 | G1550 I3000 | — |
| `pruaca.24` | 1 | +200 | 15.62 | F4200 G1550 C12520 | — |

_Cumulative peak: +300_

####HP fields (fieldlife)

| sid | lvl | +value | time (g-s) | cost | prereqs |
| --- | ---: | ---: | ---: | --- | --- |
| `pruaca.4` | 1 | +200 | 15.62 | W1000 G475 | — |
| `prubla.1` | 1 | +100 | 15.62 | W400 G90 | — |

_Cumulative peak: +300_


<a id="rus--russia-россия"></a>
<a id="россия-rus"></a>
### Russia (`rus`)
<a id="эффективность-еды"></a>
#### Food efficiency

| sid | lvl | +value | time (g-s) | cost | prereqs |
| --- | ---: | ---: | ---: | --- | --- |
| `rusaca.1` | 1 | +40 | 15.62 | W200 G325 | — |
| `rusaca.2` | 1 | +50 | 15.62 | W2400 G625 | — |
| `rusaca.3` | 1 | +50 | 15.62 | W3600 G850 | — |
| `rusmil.1` | 1 | +140 | 15.62 | F750 G250 | — |
| `rusmil.2` | 2 | +180 | 15.62 | F25600 G3350 I2000 | req0 |

_Cumulative peak: +460_

<a id="эффективность-дерева"></a>
#### Tree efficiency

| sid | lvl | +value | time (g-s) | cost | prereqs |
| --- | ---: | ---: | ---: | --- | --- |
| `rusaca.8` | 1 | +100 | 15.62 | F5500 G550 | rusbla |

_Cumulative peak: +100_

<a id="эффективность-камня"></a>
#### Efficiency of the stone

| sid | lvl | +value | time (g-s) | cost | prereqs |
| --- | ---: | ---: | ---: | --- | --- |
| `rusaca.23` | 1 | +100 | 15.62 | G1550 I3000 | — |
| `rusaca.24` | 1 | +200 | 15.62 | F4200 G1550 C12520 | — |

_Cumulative peak: +300_

####HP fields (fieldlife)

| sid | lvl | +value | time (g-s) | cost | prereqs |
| --- | ---: | ---: | ---: | --- | --- |
| `rusaca.4` | 1 | +200 | 15.62 | W1000 G475 | — |
| `rusbla.1` | 1 | +100 | 15.62 | W400 G90 | — |

_Cumulative peak: +300_


<a id="sax--saxony-саксония"></a>
<a id="саксония-sax"></a>
### Saxony (`sax`)
#### Food efficiency

| sid | lvl | +value | time (g-s) | cost | prereqs |
| --- | ---: | ---: | ---: | --- | --- |
| `eurmil.1` | 1 | +140 | 15.62 | F750 G250 | — |
| `eurmil.2` | 2 | +180 | 15.62 | F25600 G3350 I2000 | req0 |
| `saxaca.1` | 1 | +40 | 15.62 | W200 G325 | — |
| `saxaca.2` | 1 | +50 | 15.62 | W2400 G625 | — |
| `saxaca.3` | 1 | +50 | 15.62 | W3600 G850 | — |

_Cumulative peak: +460_

#### Tree efficiency

| sid | lvl | +value | time (g-s) | cost | prereqs |
| --- | ---: | ---: | ---: | --- | --- |
| `saxaca.8` | 1 | +100 | 15.62 | F5500 G550 | saxbla |

_Cumulative peak: +100_

#### Efficiency of the stone

| sid | lvl | +value | time (g-s) | cost | prereqs |
| --- | ---: | ---: | ---: | --- | --- |
| `saxaca.23` | 1 | +100 | 15.62 | G1550 I3000 | — |
| `saxaca.24` | 1 | +200 | 15.62 | F4200 G1550 C12520 | — |

_Cumulative peak: +300_

####HP fields (fieldlife)

| sid | lvl | +value | time (g-s) | cost | prereqs |
| --- | ---: | ---: | ---: | --- | --- |
| `saxaca.4` | 1 | +200 | 15.62 | W1000 G475 | — |
| `saxbla.1` | 1 | +100 | 15.62 | W400 G90 | — |

_Cumulative peak: +300_


<a id="sco--scotland-шотландия"></a>
<a id="шотландия-sco"></a>
### Scotland (`sco`)
#### Food efficiency

| sid | lvl | +value | time (g-s) | cost | prereqs |
| --- | ---: | ---: | ---: | --- | --- |
| `eurmil.1` | 1 | +140 | 15.62 | F750 G250 | — |
| `eurmil.2` | 2 | +180 | 15.62 | F5600 G1350 I1900 | req0 |
| `scoaca.1` | 1 | +40 | 15.62 | W200 G325 | — |
| `scoaca.2` | 1 | +50 | 15.62 | W2400 G625 | — |
| `scoaca.3` | 1 | +50 | 15.62 | W3600 G850 | — |

_Cumulative peak: +460_

#### Tree efficiency

| sid | lvl | +value | time (g-s) | cost | prereqs |
| --- | ---: | ---: | ---: | --- | --- |
| `scoaca.8` | 1 | +100 | 15.62 | F5500 G550 | scobla |

_Cumulative peak: +100_

#### Efficiency of the stone

| sid | lvl | +value | time (g-s) | cost | prereqs |
| --- | ---: | ---: | ---: | --- | --- |
| `scoaca.23` | 1 | +100 | 15.62 | G1550 I3000 | — |
| `scoaca.24` | 1 | +200 | 15.62 | F4200 G1550 C12520 | — |

_Cumulative peak: +300_

####HP fields (fieldlife)

| sid | lvl | +value | time (g-s) | cost | prereqs |
| --- | ---: | ---: | ---: | --- | --- |
| `scoaca.4` | 1 | +200 | 15.62 | W1000 G475 | — |
| `scobla.1` | 1 | +100 | 15.62 | W400 G90 | — |

_Cumulative peak: +300_


<a id="spa--spain-испания"></a>
<a id="испания-spa"></a>
### Spain (`spa`)
#### Food efficiency

| sid | lvl | +value | time (g-s) | cost | prereqs |
| --- | ---: | ---: | ---: | --- | --- |
| `eurmil.1` | 1 | +140 | 15.62 | F750 G250 | — |
| `eurmil.2` | 2 | +180 | 15.62 | F25600 G3350 I2000 | req0 |
| `spaaca.1` | 1 | +40 | 15.62 | W200 G325 | — |
| `spaaca.2` | 1 | +50 | 15.62 | W2400 G625 | — |
| `spaaca.3` | 1 | +50 | 15.62 | W3600 G850 | — |

_Cumulative peak: +460_

#### Tree efficiency

| sid | lvl | +value | time (g-s) | cost | prereqs |
| --- | ---: | ---: | ---: | --- | --- |
| `spaaca.8` | 1 | +100 | 15.62 | F5500 G550 | spabla |

_Cumulative peak: +100_

#### Efficiency of the stone

| sid | lvl | +value | time (g-s) | cost | prereqs |
| --- | ---: | ---: | ---: | --- | --- |
| `spaaca.23` | 1 | +100 | 15.62 | G1550 I3000 | — |
| `spaaca.24` | 1 | +200 | 15.62 | F4200 G1550 C12520 | — |

_Cumulative peak: +300_

####HP fields (fieldlife)
| sid | lvl | +value | time (g-s) | cost | prereqs |
| --- | ---: | ---: | ---: | --- | --- |
| `spaaca.4` | 1 | +200 | 15.62 | W1000 G475 | — |
| `spabla.1` | 1 | +100 | 15.62 | W400 G90 | — |

_Cumulative peak: +300_


<a id="swe--sweden-швеция"></a>
<a id="швеция-swe"></a>
### Sweden (`swe`)
#### Food efficiency

| sid | lvl | +value | time (g-s) | cost | prereqs |
| --- | ---: | ---: | ---: | --- | --- |
| `eurmil.1` | 1 | +140 | 15.62 | F750 G250 | — |
| `eurmil.2` | 2 | +180 | 15.62 | F25600 G3350 I2000 | req0 |
| `sweaca.1` | 1 | +40 | 15.62 | W200 G325 | — |
| `sweaca.2` | 1 | +50 | 15.62 | W2400 G625 | — |
| `sweaca.3` | 1 | +50 | 15.62 | W3600 G850 | — |

_Cumulative peak: +460_

#### Tree efficiency

| sid | lvl | +value | time (g-s) | cost | prereqs |
| --- | ---: | ---: | ---: | --- | --- |
| `sweaca.8` | 1 | +100 | 15.62 | F5500 G550 | swebla |

_Cumulative peak: +100_

#### Efficiency of the stone

| sid | lvl | +value | time (g-s) | cost | prereqs |
| --- | ---: | ---: | ---: | --- | --- |
| `sweaca.23` | 1 | +100 | 15.62 | G1550 I3000 | — |
| `sweaca.24` | 1 | +200 | 15.62 | F4200 G1550 C12520 | — |

_Cumulative peak: +300_

####HP fields (fieldlife)

| sid | lvl | +value | time (g-s) | cost | prereqs |
| --- | ---: | ---: | ---: | --- | --- |
| `sweaca.4` | 1 | +200 | 15.62 | W1000 G475 | — |
| `swebla.1` | 1 | +100 | 15.62 | W400 G90 | — |

_Cumulative peak: +300_


<a id="swi--switzerland-швейцария"></a>
<a id="швейцария-swi"></a>
### Switzerland (`swi`)
#### Food efficiency

| sid | lvl | +value | time (g-s) | cost | prereqs |
| --- | ---: | ---: | ---: | --- | --- |
| `eurmil.1` | 1 | +140 | 15.62 | F750 G250 | — |
| `eurmil.2` | 2 | +180 | 15.62 | F25600 G3350 I2000 | req0 |
| `swiaca.1` | 1 | +40 | 15.62 | W200 G325 | — |
| `swiaca.2` | 1 | +50 | 15.62 | W2400 G625 | — |
| `swiaca.3` | 1 | +50 | 15.62 | W3600 G850 | — |

_Cumulative peak: +460_

#### Tree efficiency

| sid | lvl | +value | time (g-s) | cost | prereqs |
| --- | ---: | ---: | ---: | --- | --- |
| `swiaca.8` | 1 | +100 | 15.62 | F5500 G550 | swibla |

_Cumulative peak: +100_

#### Efficiency of the stone

| sid | lvl | +value | time (g-s) | cost | prereqs |
| --- | ---: | ---: | ---: | --- | --- |
| `swiaca.23` | 1 | +100 | 15.62 | G1550 I3000 | — |
| `swiaca.24` | 1 | +200 | 15.62 | F4200 G1550 C12520 | — |

_Cumulative peak: +300_

####HP fields (fieldlife)

| sid | lvl | +value | time (g-s) | cost | prereqs |
| --- | ---: | ---: | ---: | --- | --- |
| `swiaca.4` | 1 | +200 | 15.62 | W1000 G475 | — |
| `swibla.1` | 1 | +100 | 15.62 | W400 G90 | — |

_Cumulative peak: +300_


<a id="tur--turkey-турция"></a>
<a id="турция-tur"></a>
### Turkey (`tur`)
#### Food efficiency

| sid | lvl | +value | time (g-s) | cost | prereqs |
| --- | ---: | ---: | ---: | --- | --- |
| `turaca.1` | 1 | +40 | 15.62 | W200 G325 | — |
| `turaca.2` | 1 | +50 | 15.62 | W400 G522 | — |
| `turaca.3` | 1 | +50 | 15.62 | W2400 G850 | — |
| `turmil.1` | 1 | +140 | 15.62 | F600 G250 | — |

_Cumulative peak: +280_

#### Tree efficiency

| sid | lvl | +value | time (g-s) | cost | prereqs |
| --- | ---: | ---: | ---: | --- | --- |
| `turaca.8` | 1 | +100 | 15.62 | F5500 G550 | turbla |

_Cumulative peak: +100_

#### Efficiency of the stone

| sid | lvl | +value | time (g-s) | cost | prereqs |
| --- | ---: | ---: | ---: | --- | --- |
| `turaca.23` | 1 | +100 | 15.62 | G1550 I3000 | — |
| `turaca.24` | 1 | +200 | 15.62 | F4200 G1550 C12520 | — |

_Cumulative peak: +300_

####HP fields (fieldlife)

| sid | lvl | +value | time (g-s) | cost | prereqs |
| --- | ---: | ---: | ---: | --- | --- |
| `turaca.4` | 1 | +200 | 15.62 | W1000 G475 | — |
| `turbla.1` | 1 | +100 | 15.62 | W400 G90 | — |
_Cumulative peak: +300_


<a id="ukr--ukraine-украина"></a>
<a id="украина-ukr"></a>
### Ukraine (`ukr`)
#### Food efficiency

| sid | lvl | +value | time (g-s) | cost | prereqs |
| --- | ---: | ---: | ---: | --- | --- |
| `rusmil.1` | 1 | +140 | 15.62 | F750 G250 | — |
| `rusmil.2` | 2 | +180 | 15.62 | F5600 G1350 I1900 | req0 |
| `ukraca.1` | 1 | +40 | 15.62 | W200 G325 | — |
| `ukraca.2` | 1 | +50 | 15.62 | W2400 G625 | — |
| `ukraca.3` | 1 | +50 | 15.62 | W3600 G850 | — |

_Cumulative peak: +460_

#### Tree efficiency

| sid | lvl | +value | time (g-s) | cost | prereqs |
| --- | ---: | ---: | ---: | --- | --- |
| `ukraca.8` | 1 | +100 | 15.62 | F5500 G550 | ukrbla |

_Cumulative peak: +100_

#### Efficiency of the stone

| sid | lvl | +value | time (g-s) | cost | prereqs |
| --- | ---: | ---: | ---: | --- | --- |
| `ukraca.23` | 1 | +100 | 15.62 | G1550 I3000 | — |
| `ukraca.24` | 1 | +200 | 15.62 | F4200 G1550 C12520 | — |

_Cumulative peak: +300_

####HP fields (fieldlife)

| sid | lvl | +value | time (g-s) | cost | prereqs |
| --- | ---: | ---: | ---: | --- | --- |
| `ukraca.4` | 1 | +200 | 15.62 | W1000 G475 | — |
| `ukrbla.1` | 1 | +100 | 15.62 | W400 G90 | — |

_Cumulative peak: +300_


<a id="ven--venice-венеция"></a>
<a id="венеция-ven"></a>
### Venice (`ven`)
#### Food efficiency

| sid | lvl | +value | time (g-s) | cost | prereqs |
| --- | ---: | ---: | ---: | --- | --- |
| `eurmil.1` | 1 | +140 | 15.62 | F750 G250 | — |
| `eurmil.2` | 2 | +180 | 15.62 | F25600 G3350 I2000 | req0 |
| `venaca.1` | 1 | +40 | 15.62 | W200 G325 | — |
| `venaca.2` | 1 | +50 | 15.62 | W2400 G625 | — |
| `venaca.3` | 1 | +50 | 15.62 | W3600 G850 | — |

_Cumulative peak: +460_

#### Tree efficiency

| sid | lvl | +value | time (g-s) | cost | prereqs |
| --- | ---: | ---: | ---: | --- | --- |
| `venaca.8` | 1 | +100 | 15.62 | F5500 G550 | venbla |

_Cumulative peak: +100_

#### Efficiency of the stone

| sid | lvl | +value | time (g-s) | cost | prereqs |
| --- | ---: | ---: | ---: | --- | --- |
| `venaca.23` | 1 | +100 | 15.62 | G1550 I3000 | — |
| `venaca.24` | 1 | +200 | 15.62 | F4200 G1550 C12520 | — |

_Cumulative peak: +300_

####HP fields (fieldlife)

| sid | lvl | +value | time (g-s) | cost | prereqs |
| --- | ---: | ---: | ---: | --- | --- |
| `venaca.4` | 1 | +200 | 15.62 | W1000 G475 | — |
| `venbla.1` | 1 | +100 | 15.62 | W400 G90 | — |

_Cumulative peak: +300_



<a id="источники"></a>
## Sources

All links are relative to `data/scripts/` in the Cossacks 3 installation.

[^1]: Applying `gc_upg_type_effect*perc` to `resefficiency[res]` - `lib/player.script:1812+`.

[^2]: formula `delivered = floor(portion × eff / 100)` - `lib/unit.script:9551-9555`.
