# Cossacks 3 — Efficiency upgrades per nation

**Производный** файл (расчётный, не извлечение). Считается из `output/data.json` скриптом [`compute/compute_efficiency_upgrades.py`](../../../compute/compute_efficiency_upgrades.py).

## Что это

Каждый апгрейд `gc_upg_type_effect{food,wood,stone}[perc]` **аддитивно** прибавляет `value` к `resefficiency[res]` ([`player.script:1812+`](<C:/Program Files (x86)/Steam/steamapps/common/Cossacks 3/data/scripts/lib/player.script>)).
База = 100. Формула добычи на удар: `delivered = floor(portion × eff / 100)`, где `portion` = 45/28/40 для food/wood/stone (`unit.script:9551-9555`).

`gc_upg_type_fieldlifeperc` аддитивно прибавляет к `objbase.fieldlife` поля. Снижает урон/удар по полю на `100 / (1 + fieldlife/100)` — повышает выход за один цикл и уменьшает частоту перезапусков.

## Сводка по нациям (cumulative peaks)

Сумма всех значений в линейке = пик для нации, если исследовать ВСЕ соответствующие апгрейды. На практике некоторые апгрейды эксклюзивны (один building с .1..6 лестницей), но скрипт суммирует всё — это **верхняя граница**.

| Нация | food eff % | wood eff % | stone eff % | fieldlife % | Σ апгрейдов |
| --- | ---: | ---: | ---: | ---: | ---: |
| alg | +280 | +100 | +300 | +300 | 9 |
| aus | +460 | +100 | +300 | +300 | 10 |
| bav | +460 | +100 | +300 | +300 | 10 |
| den | +460 | +100 | +300 | +300 | 10 |
| eng | +460 | +100 | +300 | +300 | 10 |
| fra | +460 | +100 | +300 | +300 | 10 |
| hun | +460 | +100 | +300 | +300 | 10 |
| net | +460 | +100 | +300 | +300 | 10 |
| pie | +460 | +100 | +300 | +300 | 10 |
| pol | +460 | +100 | +300 | +300 | 10 |
| por | +460 | +100 | +300 | +300 | 10 |
| pru | +460 | +100 | +300 | +300 | 10 |
| rus | +460 | +100 | +300 | +300 | 10 |
| sax | +460 | +100 | +300 | +300 | 10 |
| sco | +460 | +100 | +300 | +300 | 10 |
| spa | +460 | +100 | +300 | +300 | 10 |
| swe | +460 | +100 | +300 | +300 | 10 |
| swi | +460 | +100 | +300 | +300 | 10 |
| tur | +280 | +100 | +300 | +300 | 9 |
| ukr | +460 | +100 | +300 | +300 | 10 |
| ven | +460 | +100 | +300 | +300 | 10 |

**Best-in-class peaks across all nations:**
- Food efficiency: **+460** — aus, bav, den, … (19 nations tied)
- Wood efficiency: **+100** — alg, aus, bav, … (21 nations tied)
- Stone efficiency: **+300** — alg, aus, bav, … (21 nations tied)
- Field HP (fieldlife): **+300** — alg, aus, bav, … (21 nations tied)

**Cheapest food-eff progression (cumulative gold for ALL food-eff upgrades):**

| Нация | total gold | total food | total wood |
| --- | ---: | ---: | ---: |
| alg | 1947 | 600 | 1840 |
| tur | 1947 | 600 | 3000 |
| sco | 3400 | 6350 | 6200 |
| ukr | 3400 | 6350 | 6200 |
| fra | 5390 | 26350 | 6190 |
| aus | 5400 | 26350 | 6200 |
| bav | 5400 | 26350 | 6200 |
| den | 5400 | 26350 | 6200 |
| eng | 5400 | 26350 | 6200 |
| hun | 5400 | 26350 | 6200 |
| net | 5400 | 26350 | 6200 |
| pie | 5400 | 26350 | 6200 |
| pol | 5400 | 26350 | 6200 |
| por | 5400 | 26350 | 6200 |
| pru | 5400 | 26350 | 6200 |
| rus | 5400 | 26350 | 6200 |
| sax | 5400 | 26350 | 6200 |
| spa | 5400 | 26350 | 6200 |
| swe | 5400 | 26350 | 6200 |
| swi | 5400 | 26350 | 6200 |
| ven | 5400 | 26350 | 6200 |

## Подробно по нациям

Каждая ячейка cost — стоимость **этого** апгрейда (не суммарная).

### alg

#### Food efficiency

| sid | lvl | +value | time (g-s) | cost | prereqs |
| --- | ---: | ---: | ---: | --- | --- |
| `algaca.1` | 1 | +40 | 15.62 | W200 G325 | — |
| `algaca.2` | 1 | +50 | 15.62 | W400 G522 | — |
| `algaca.3` | 1 | +50 | 15.62 | W1240 G850 | — |
| `algbar.1` | 1 | +140 | 15.62 | F600 G250 | — |

_Cumulative peak: +280_

#### Wood efficiency

| sid | lvl | +value | time (g-s) | cost | prereqs |
| --- | ---: | ---: | ---: | --- | --- |
| `algaca.8` | 1 | +100 | 15.62 | F5500 G550 | algbla |

_Cumulative peak: +100_

#### Stone efficiency

| sid | lvl | +value | time (g-s) | cost | prereqs |
| --- | ---: | ---: | ---: | --- | --- |
| `algaca.23` | 1 | +100 | 15.62 | G1550 I3000 | — |
| `algaca.24` | 1 | +200 | 15.62 | F4200 G1550 C12520 | — |

_Cumulative peak: +300_

#### Field HP (fieldlife)

| sid | lvl | +value | time (g-s) | cost | prereqs |
| --- | ---: | ---: | ---: | --- | --- |
| `algaca.4` | 1 | +200 | 15.62 | W700 G475 | — |
| `algbla.1` | 1 | +100 | 15.62 | W400 G90 | — |

_Cumulative peak: +300_


### aus

#### Food efficiency

| sid | lvl | +value | time (g-s) | cost | prereqs |
| --- | ---: | ---: | ---: | --- | --- |
| `ausaca.1` | 1 | +40 | 15.62 | W200 G325 | — |
| `ausaca.2` | 1 | +50 | 15.62 | W2400 G625 | — |
| `ausaca.3` | 1 | +50 | 15.62 | W3600 G850 | — |
| `ausbar.1` | 1 | +140 | 15.62 | F750 G250 | — |
| `ausbar.2` | 2 | +180 | 15.62 | F25600 G3350 I2000 | req0 |

_Cumulative peak: +460_

#### Wood efficiency

| sid | lvl | +value | time (g-s) | cost | prereqs |
| --- | ---: | ---: | ---: | --- | --- |
| `ausaca.8` | 1 | +100 | 15.62 | F5500 G550 | ausbla |

_Cumulative peak: +100_

#### Stone efficiency

| sid | lvl | +value | time (g-s) | cost | prereqs |
| --- | ---: | ---: | ---: | --- | --- |
| `ausaca.23` | 1 | +100 | 15.62 | G1550 I3000 | — |
| `ausaca.24` | 1 | +200 | 15.62 | F4200 G1550 C12520 | — |

_Cumulative peak: +300_

#### Field HP (fieldlife)

| sid | lvl | +value | time (g-s) | cost | prereqs |
| --- | ---: | ---: | ---: | --- | --- |
| `ausaca.4` | 1 | +200 | 15.62 | W1000 G475 | — |
| `ausbla.1` | 1 | +100 | 15.62 | W400 G90 | — |

_Cumulative peak: +300_


### bav

#### Food efficiency

| sid | lvl | +value | time (g-s) | cost | prereqs |
| --- | ---: | ---: | ---: | --- | --- |
| `bavaca.1` | 1 | +40 | 15.62 | W200 G325 | — |
| `bavaca.2` | 1 | +50 | 15.62 | W2400 G625 | — |
| `bavaca.3` | 1 | +50 | 15.62 | W3600 G850 | — |
| `bavbar.1` | 1 | +140 | 15.62 | F750 G250 | — |
| `bavbar.2` | 2 | +180 | 15.62 | F25600 G3350 I2000 | req0 |

_Cumulative peak: +460_

#### Wood efficiency

| sid | lvl | +value | time (g-s) | cost | prereqs |
| --- | ---: | ---: | ---: | --- | --- |
| `bavaca.8` | 1 | +100 | 15.62 | F5500 G550 | bavbla |

_Cumulative peak: +100_

#### Stone efficiency

| sid | lvl | +value | time (g-s) | cost | prereqs |
| --- | ---: | ---: | ---: | --- | --- |
| `bavaca.23` | 1 | +100 | 15.62 | G1550 I3000 | — |
| `bavaca.24` | 1 | +200 | 15.62 | F4200 G1550 C12520 | — |

_Cumulative peak: +300_

#### Field HP (fieldlife)

| sid | lvl | +value | time (g-s) | cost | prereqs |
| --- | ---: | ---: | ---: | --- | --- |
| `bavaca.4` | 1 | +200 | 15.62 | W1000 G475 | — |
| `bavbla.1` | 1 | +100 | 15.62 | W400 G90 | — |

_Cumulative peak: +300_


### den

#### Food efficiency

| sid | lvl | +value | time (g-s) | cost | prereqs |
| --- | ---: | ---: | ---: | --- | --- |
| `denaca.1` | 1 | +40 | 15.62 | W200 G325 | — |
| `denaca.2` | 1 | +50 | 15.62 | W2400 G625 | — |
| `denaca.3` | 1 | +50 | 15.62 | W3600 G850 | — |
| `denbar.1` | 1 | +140 | 15.62 | F750 G250 | — |
| `denbar.2` | 2 | +180 | 15.62 | F25600 G3350 I2000 | req0 |

_Cumulative peak: +460_

#### Wood efficiency

| sid | lvl | +value | time (g-s) | cost | prereqs |
| --- | ---: | ---: | ---: | --- | --- |
| `denaca.8` | 1 | +100 | 15.62 | F5500 G550 | denbla |

_Cumulative peak: +100_

#### Stone efficiency

| sid | lvl | +value | time (g-s) | cost | prereqs |
| --- | ---: | ---: | ---: | --- | --- |
| `denaca.23` | 1 | +100 | 15.62 | G1550 I3000 | — |
| `denaca.24` | 1 | +200 | 15.62 | F4200 G1550 C12520 | — |

_Cumulative peak: +300_

#### Field HP (fieldlife)

| sid | lvl | +value | time (g-s) | cost | prereqs |
| --- | ---: | ---: | ---: | --- | --- |
| `denaca.4` | 1 | +200 | 15.62 | W1000 G475 | — |
| `denbla.1` | 1 | +100 | 15.62 | W400 G90 | — |

_Cumulative peak: +300_


### eng

#### Food efficiency

| sid | lvl | +value | time (g-s) | cost | prereqs |
| --- | ---: | ---: | ---: | --- | --- |
| `engaca.1` | 1 | +40 | 15.62 | W200 G325 | — |
| `engaca.2` | 1 | +50 | 15.62 | W2400 G625 | — |
| `engaca.3` | 1 | +50 | 15.62 | W3600 G850 | — |
| `engba2.1` | 1 | +140 | 15.62 | F750 G250 | — |
| `engba2.2` | 2 | +180 | 15.62 | F25600 G3350 I2000 | req0 |

_Cumulative peak: +460_

#### Wood efficiency

| sid | lvl | +value | time (g-s) | cost | prereqs |
| --- | ---: | ---: | ---: | --- | --- |
| `engaca.8` | 1 | +100 | 15.62 | F5500 G550 | engbla |

_Cumulative peak: +100_

#### Stone efficiency

| sid | lvl | +value | time (g-s) | cost | prereqs |
| --- | ---: | ---: | ---: | --- | --- |
| `engaca.23` | 1 | +100 | 15.62 | G1550 I3000 | — |
| `engaca.24` | 1 | +200 | 15.62 | F4200 G1550 C12520 | — |

_Cumulative peak: +300_

#### Field HP (fieldlife)

| sid | lvl | +value | time (g-s) | cost | prereqs |
| --- | ---: | ---: | ---: | --- | --- |
| `engaca.4` | 1 | +200 | 15.62 | W1000 G475 | — |
| `engbla.1` | 1 | +100 | 15.62 | W400 G90 | — |

_Cumulative peak: +300_


### fra

#### Food efficiency

| sid | lvl | +value | time (g-s) | cost | prereqs |
| --- | ---: | ---: | ---: | --- | --- |
| `fraaca.1` | 1 | +40 | 15.62 | W190 G315 | — |
| `fraaca.2` | 1 | +50 | 15.62 | W2400 G625 | — |
| `fraaca.3` | 1 | +50 | 15.62 | W3600 G850 | — |
| `frabar.1` | 1 | +140 | 15.62 | F750 G250 | — |
| `frabar.2` | 2 | +180 | 15.62 | F25600 G3350 I2000 | req0 |

_Cumulative peak: +460_

#### Wood efficiency

| sid | lvl | +value | time (g-s) | cost | prereqs |
| --- | ---: | ---: | ---: | --- | --- |
| `fraaca.8` | 1 | +100 | 15.62 | F5500 G550 | frabla |

_Cumulative peak: +100_

#### Stone efficiency

| sid | lvl | +value | time (g-s) | cost | prereqs |
| --- | ---: | ---: | ---: | --- | --- |
| `fraaca.23` | 1 | +100 | 15.62 | G1550 I3000 | — |
| `fraaca.24` | 1 | +200 | 15.62 | F4200 G1550 C12520 | — |

_Cumulative peak: +300_

#### Field HP (fieldlife)

| sid | lvl | +value | time (g-s) | cost | prereqs |
| --- | ---: | ---: | ---: | --- | --- |
| `fraaca.4` | 1 | +200 | 15.62 | W1000 G475 | — |
| `frabla.1` | 1 | +100 | 15.62 | W400 G90 | — |

_Cumulative peak: +300_


### hun

#### Food efficiency

| sid | lvl | +value | time (g-s) | cost | prereqs |
| --- | ---: | ---: | ---: | --- | --- |
| `hunaca.1` | 1 | +40 | 15.62 | W200 G325 | — |
| `hunaca.2` | 1 | +50 | 15.62 | W2400 G625 | — |
| `hunaca.3` | 1 | +50 | 15.62 | W3600 G850 | — |
| `hunbar.1` | 1 | +140 | 15.62 | F750 G250 | — |
| `hunbar.2` | 2 | +180 | 15.62 | F25600 G3350 I2000 | req0 |

_Cumulative peak: +460_

#### Wood efficiency

| sid | lvl | +value | time (g-s) | cost | prereqs |
| --- | ---: | ---: | ---: | --- | --- |
| `hunaca.8` | 1 | +100 | 15.62 | F5500 G550 | hunbla |

_Cumulative peak: +100_

#### Stone efficiency

| sid | lvl | +value | time (g-s) | cost | prereqs |
| --- | ---: | ---: | ---: | --- | --- |
| `hunaca.23` | 1 | +100 | 15.62 | G1550 I3000 | — |
| `hunaca.24` | 1 | +200 | 15.62 | F4200 G1550 C12520 | — |

_Cumulative peak: +300_

#### Field HP (fieldlife)

| sid | lvl | +value | time (g-s) | cost | prereqs |
| --- | ---: | ---: | ---: | --- | --- |
| `hunaca.4` | 1 | +200 | 15.62 | W1000 G475 | — |
| `hunbla.1` | 1 | +100 | 15.62 | W400 G90 | — |

_Cumulative peak: +300_


### net

#### Food efficiency

| sid | lvl | +value | time (g-s) | cost | prereqs |
| --- | ---: | ---: | ---: | --- | --- |
| `netaca.1` | 1 | +40 | 15.62 | W200 G325 | — |
| `netaca.2` | 1 | +50 | 15.62 | W2400 G625 | — |
| `netaca.3` | 1 | +50 | 15.62 | W3600 G850 | — |
| `netbar.1` | 1 | +140 | 15.62 | F750 G250 | — |
| `netbar.2` | 2 | +180 | 15.62 | F25600 G3350 I2000 | req0 |

_Cumulative peak: +460_

#### Wood efficiency

| sid | lvl | +value | time (g-s) | cost | prereqs |
| --- | ---: | ---: | ---: | --- | --- |
| `netaca.8` | 1 | +100 | 15.62 | F5500 G550 | netbla |

_Cumulative peak: +100_

#### Stone efficiency

| sid | lvl | +value | time (g-s) | cost | prereqs |
| --- | ---: | ---: | ---: | --- | --- |
| `netaca.23` | 1 | +100 | 15.62 | G1550 I3000 | — |
| `netaca.24` | 1 | +200 | 15.62 | F4200 G1550 C12520 | — |

_Cumulative peak: +300_

#### Field HP (fieldlife)

| sid | lvl | +value | time (g-s) | cost | prereqs |
| --- | ---: | ---: | ---: | --- | --- |
| `netaca.4` | 1 | +200 | 15.62 | W1000 G475 | — |
| `netbla.1` | 1 | +100 | 15.62 | W400 G90 | — |

_Cumulative peak: +300_


### pie

#### Food efficiency

| sid | lvl | +value | time (g-s) | cost | prereqs |
| --- | ---: | ---: | ---: | --- | --- |
| `pieaca.1` | 1 | +40 | 15.62 | W200 G325 | — |
| `pieaca.2` | 1 | +50 | 15.62 | W2400 G625 | — |
| `pieaca.3` | 1 | +50 | 15.62 | W3600 G850 | — |
| `piebar.1` | 1 | +140 | 15.62 | F750 G250 | — |
| `piebar.2` | 2 | +180 | 15.62 | F25600 G3350 I2000 | req0 |

_Cumulative peak: +460_

#### Wood efficiency

| sid | lvl | +value | time (g-s) | cost | prereqs |
| --- | ---: | ---: | ---: | --- | --- |
| `pieaca.8` | 1 | +100 | 15.62 | F5500 G550 | piebla |

_Cumulative peak: +100_

#### Stone efficiency

| sid | lvl | +value | time (g-s) | cost | prereqs |
| --- | ---: | ---: | ---: | --- | --- |
| `pieaca.23` | 1 | +100 | 15.62 | G1550 I3000 | — |
| `pieaca.24` | 1 | +200 | 15.62 | F4200 G1550 C12520 | — |

_Cumulative peak: +300_

#### Field HP (fieldlife)

| sid | lvl | +value | time (g-s) | cost | prereqs |
| --- | ---: | ---: | ---: | --- | --- |
| `pieaca.4` | 1 | +200 | 15.62 | W1000 G475 | — |
| `piebla.1` | 1 | +100 | 15.62 | W400 G90 | — |

_Cumulative peak: +300_


### pol

#### Food efficiency

| sid | lvl | +value | time (g-s) | cost | prereqs |
| --- | ---: | ---: | ---: | --- | --- |
| `polaca.1` | 1 | +40 | 15.62 | W200 G325 | — |
| `polaca.2` | 1 | +50 | 15.62 | W2400 G625 | — |
| `polaca.3` | 1 | +50 | 15.62 | W3600 G850 | — |
| `polbar.1` | 1 | +140 | 15.62 | F750 G250 | — |
| `polbar.2` | 2 | +180 | 15.62 | F25600 G3350 I2000 | req0 |

_Cumulative peak: +460_

#### Wood efficiency

| sid | lvl | +value | time (g-s) | cost | prereqs |
| --- | ---: | ---: | ---: | --- | --- |
| `polaca.8` | 1 | +100 | 15.62 | F5500 G550 | polbla |

_Cumulative peak: +100_

#### Stone efficiency

| sid | lvl | +value | time (g-s) | cost | prereqs |
| --- | ---: | ---: | ---: | --- | --- |
| `polaca.23` | 1 | +100 | 15.62 | G1550 I3000 | — |
| `polaca.24` | 1 | +200 | 15.62 | F4200 G1550 C12520 | — |

_Cumulative peak: +300_

#### Field HP (fieldlife)

| sid | lvl | +value | time (g-s) | cost | prereqs |
| --- | ---: | ---: | ---: | --- | --- |
| `polaca.4` | 1 | +200 | 15.62 | W1000 G475 | — |
| `polbla.1` | 1 | +100 | 15.62 | W400 G90 | — |

_Cumulative peak: +300_


### por

#### Food efficiency

| sid | lvl | +value | time (g-s) | cost | prereqs |
| --- | ---: | ---: | ---: | --- | --- |
| `poraca.1` | 1 | +40 | 15.62 | W200 G325 | — |
| `poraca.2` | 1 | +50 | 15.62 | W2400 G625 | — |
| `poraca.3` | 1 | +50 | 15.62 | W3600 G850 | — |
| `porbar.1` | 1 | +140 | 15.62 | F750 G250 | — |
| `porbar.2` | 2 | +180 | 15.62 | F25600 G3350 I2000 | req0 |

_Cumulative peak: +460_

#### Wood efficiency

| sid | lvl | +value | time (g-s) | cost | prereqs |
| --- | ---: | ---: | ---: | --- | --- |
| `poraca.8` | 1 | +100 | 15.62 | F5500 G550 | porbla |

_Cumulative peak: +100_

#### Stone efficiency

| sid | lvl | +value | time (g-s) | cost | prereqs |
| --- | ---: | ---: | ---: | --- | --- |
| `poraca.23` | 1 | +100 | 15.62 | G1550 I3000 | — |
| `poraca.24` | 1 | +200 | 15.62 | F4200 G1550 C12520 | — |

_Cumulative peak: +300_

#### Field HP (fieldlife)

| sid | lvl | +value | time (g-s) | cost | prereqs |
| --- | ---: | ---: | ---: | --- | --- |
| `poraca.4` | 1 | +200 | 15.62 | W1000 G475 | — |
| `porbla.1` | 1 | +100 | 15.62 | W400 G90 | — |

_Cumulative peak: +300_


### pru

#### Food efficiency

| sid | lvl | +value | time (g-s) | cost | prereqs |
| --- | ---: | ---: | ---: | --- | --- |
| `pruaca.1` | 1 | +40 | 15.62 | W200 G325 | — |
| `pruaca.2` | 1 | +50 | 15.62 | W2400 G625 | — |
| `pruaca.3` | 1 | +50 | 15.62 | W3600 G850 | — |
| `prubar.1` | 1 | +140 | 15.62 | F750 G250 | — |
| `prubar.2` | 2 | +180 | 15.62 | F25600 G3350 I2000 | req0 |

_Cumulative peak: +460_

#### Wood efficiency

| sid | lvl | +value | time (g-s) | cost | prereqs |
| --- | ---: | ---: | ---: | --- | --- |
| `pruaca.8` | 1 | +100 | 15.62 | F5500 G550 | prubla |

_Cumulative peak: +100_

#### Stone efficiency

| sid | lvl | +value | time (g-s) | cost | prereqs |
| --- | ---: | ---: | ---: | --- | --- |
| `pruaca.23` | 1 | +100 | 15.62 | G1550 I3000 | — |
| `pruaca.24` | 1 | +200 | 15.62 | F4200 G1550 C12520 | — |

_Cumulative peak: +300_

#### Field HP (fieldlife)

| sid | lvl | +value | time (g-s) | cost | prereqs |
| --- | ---: | ---: | ---: | --- | --- |
| `pruaca.4` | 1 | +200 | 15.62 | W1000 G475 | — |
| `prubla.1` | 1 | +100 | 15.62 | W400 G90 | — |

_Cumulative peak: +300_


### rus

#### Food efficiency

| sid | lvl | +value | time (g-s) | cost | prereqs |
| --- | ---: | ---: | ---: | --- | --- |
| `rusaca.1` | 1 | +40 | 15.62 | W200 G325 | — |
| `rusaca.2` | 1 | +50 | 15.62 | W2400 G625 | — |
| `rusaca.3` | 1 | +50 | 15.62 | W3600 G850 | — |
| `rusbar.1` | 1 | +140 | 15.62 | F750 G250 | — |
| `rusbar.2` | 2 | +180 | 15.62 | F25600 G3350 I2000 | req0 |

_Cumulative peak: +460_

#### Wood efficiency

| sid | lvl | +value | time (g-s) | cost | prereqs |
| --- | ---: | ---: | ---: | --- | --- |
| `rusaca.8` | 1 | +100 | 15.62 | F5500 G550 | rusbla |

_Cumulative peak: +100_

#### Stone efficiency

| sid | lvl | +value | time (g-s) | cost | prereqs |
| --- | ---: | ---: | ---: | --- | --- |
| `rusaca.23` | 1 | +100 | 15.62 | G1550 I3000 | — |
| `rusaca.24` | 1 | +200 | 15.62 | F4200 G1550 C12520 | — |

_Cumulative peak: +300_

#### Field HP (fieldlife)

| sid | lvl | +value | time (g-s) | cost | prereqs |
| --- | ---: | ---: | ---: | --- | --- |
| `rusaca.4` | 1 | +200 | 15.62 | W1000 G475 | — |
| `rusbla.1` | 1 | +100 | 15.62 | W400 G90 | — |

_Cumulative peak: +300_


### sax

#### Food efficiency

| sid | lvl | +value | time (g-s) | cost | prereqs |
| --- | ---: | ---: | ---: | --- | --- |
| `saxaca.1` | 1 | +40 | 15.62 | W200 G325 | — |
| `saxaca.2` | 1 | +50 | 15.62 | W2400 G625 | — |
| `saxaca.3` | 1 | +50 | 15.62 | W3600 G850 | — |
| `saxbar.1` | 1 | +140 | 15.62 | F750 G250 | — |
| `saxbar.2` | 2 | +180 | 15.62 | F25600 G3350 I2000 | req0 |

_Cumulative peak: +460_

#### Wood efficiency

| sid | lvl | +value | time (g-s) | cost | prereqs |
| --- | ---: | ---: | ---: | --- | --- |
| `saxaca.8` | 1 | +100 | 15.62 | F5500 G550 | saxbla |

_Cumulative peak: +100_

#### Stone efficiency

| sid | lvl | +value | time (g-s) | cost | prereqs |
| --- | ---: | ---: | ---: | --- | --- |
| `saxaca.23` | 1 | +100 | 15.62 | G1550 I3000 | — |
| `saxaca.24` | 1 | +200 | 15.62 | F4200 G1550 C12520 | — |

_Cumulative peak: +300_

#### Field HP (fieldlife)

| sid | lvl | +value | time (g-s) | cost | prereqs |
| --- | ---: | ---: | ---: | --- | --- |
| `saxaca.4` | 1 | +200 | 15.62 | W1000 G475 | — |
| `saxbla.1` | 1 | +100 | 15.62 | W400 G90 | — |

_Cumulative peak: +300_


### sco

#### Food efficiency

| sid | lvl | +value | time (g-s) | cost | prereqs |
| --- | ---: | ---: | ---: | --- | --- |
| `scoaca.1` | 1 | +40 | 15.62 | W200 G325 | — |
| `scoaca.2` | 1 | +50 | 15.62 | W2400 G625 | — |
| `scoaca.3` | 1 | +50 | 15.62 | W3600 G850 | — |
| `scobar.1` | 1 | +140 | 15.62 | F750 G250 | — |
| `scobar.2` | 2 | +180 | 15.62 | F5600 G1350 I1900 | req0 |

_Cumulative peak: +460_

#### Wood efficiency

| sid | lvl | +value | time (g-s) | cost | prereqs |
| --- | ---: | ---: | ---: | --- | --- |
| `scoaca.8` | 1 | +100 | 15.62 | F5500 G550 | scobla |

_Cumulative peak: +100_

#### Stone efficiency

| sid | lvl | +value | time (g-s) | cost | prereqs |
| --- | ---: | ---: | ---: | --- | --- |
| `scoaca.23` | 1 | +100 | 15.62 | G1550 I3000 | — |
| `scoaca.24` | 1 | +200 | 15.62 | F4200 G1550 C12520 | — |

_Cumulative peak: +300_

#### Field HP (fieldlife)

| sid | lvl | +value | time (g-s) | cost | prereqs |
| --- | ---: | ---: | ---: | --- | --- |
| `scoaca.4` | 1 | +200 | 15.62 | W1000 G475 | — |
| `scobla.1` | 1 | +100 | 15.62 | W400 G90 | — |

_Cumulative peak: +300_


### spa

#### Food efficiency

| sid | lvl | +value | time (g-s) | cost | prereqs |
| --- | ---: | ---: | ---: | --- | --- |
| `spaaca.1` | 1 | +40 | 15.62 | W200 G325 | — |
| `spaaca.2` | 1 | +50 | 15.62 | W2400 G625 | — |
| `spaaca.3` | 1 | +50 | 15.62 | W3600 G850 | — |
| `spabar.1` | 1 | +140 | 15.62 | F750 G250 | — |
| `spabar.2` | 2 | +180 | 15.62 | F25600 G3350 I2000 | req0 |

_Cumulative peak: +460_

#### Wood efficiency

| sid | lvl | +value | time (g-s) | cost | prereqs |
| --- | ---: | ---: | ---: | --- | --- |
| `spaaca.8` | 1 | +100 | 15.62 | F5500 G550 | spabla |

_Cumulative peak: +100_

#### Stone efficiency

| sid | lvl | +value | time (g-s) | cost | prereqs |
| --- | ---: | ---: | ---: | --- | --- |
| `spaaca.23` | 1 | +100 | 15.62 | G1550 I3000 | — |
| `spaaca.24` | 1 | +200 | 15.62 | F4200 G1550 C12520 | — |

_Cumulative peak: +300_

#### Field HP (fieldlife)

| sid | lvl | +value | time (g-s) | cost | prereqs |
| --- | ---: | ---: | ---: | --- | --- |
| `spaaca.4` | 1 | +200 | 15.62 | W1000 G475 | — |
| `spabla.1` | 1 | +100 | 15.62 | W400 G90 | — |

_Cumulative peak: +300_


### swe

#### Food efficiency

| sid | lvl | +value | time (g-s) | cost | prereqs |
| --- | ---: | ---: | ---: | --- | --- |
| `sweaca.1` | 1 | +40 | 15.62 | W200 G325 | — |
| `sweaca.2` | 1 | +50 | 15.62 | W2400 G625 | — |
| `sweaca.3` | 1 | +50 | 15.62 | W3600 G850 | — |
| `swebar.1` | 1 | +140 | 15.62 | F750 G250 | — |
| `swebar.2` | 2 | +180 | 15.62 | F25600 G3350 I2000 | req0 |

_Cumulative peak: +460_

#### Wood efficiency

| sid | lvl | +value | time (g-s) | cost | prereqs |
| --- | ---: | ---: | ---: | --- | --- |
| `sweaca.8` | 1 | +100 | 15.62 | F5500 G550 | swebla |

_Cumulative peak: +100_

#### Stone efficiency

| sid | lvl | +value | time (g-s) | cost | prereqs |
| --- | ---: | ---: | ---: | --- | --- |
| `sweaca.23` | 1 | +100 | 15.62 | G1550 I3000 | — |
| `sweaca.24` | 1 | +200 | 15.62 | F4200 G1550 C12520 | — |

_Cumulative peak: +300_

#### Field HP (fieldlife)

| sid | lvl | +value | time (g-s) | cost | prereqs |
| --- | ---: | ---: | ---: | --- | --- |
| `sweaca.4` | 1 | +200 | 15.62 | W1000 G475 | — |
| `swebla.1` | 1 | +100 | 15.62 | W400 G90 | — |

_Cumulative peak: +300_


### swi

#### Food efficiency

| sid | lvl | +value | time (g-s) | cost | prereqs |
| --- | ---: | ---: | ---: | --- | --- |
| `swiaca.1` | 1 | +40 | 15.62 | W200 G325 | — |
| `swiaca.2` | 1 | +50 | 15.62 | W2400 G625 | — |
| `swiaca.3` | 1 | +50 | 15.62 | W3600 G850 | — |
| `swibar.1` | 1 | +140 | 15.62 | F750 G250 | — |
| `swibar.2` | 2 | +180 | 15.62 | F25600 G3350 I2000 | req0 |

_Cumulative peak: +460_

#### Wood efficiency

| sid | lvl | +value | time (g-s) | cost | prereqs |
| --- | ---: | ---: | ---: | --- | --- |
| `swiaca.8` | 1 | +100 | 15.62 | F5500 G550 | swibla |

_Cumulative peak: +100_

#### Stone efficiency

| sid | lvl | +value | time (g-s) | cost | prereqs |
| --- | ---: | ---: | ---: | --- | --- |
| `swiaca.23` | 1 | +100 | 15.62 | G1550 I3000 | — |
| `swiaca.24` | 1 | +200 | 15.62 | F4200 G1550 C12520 | — |

_Cumulative peak: +300_

#### Field HP (fieldlife)

| sid | lvl | +value | time (g-s) | cost | prereqs |
| --- | ---: | ---: | ---: | --- | --- |
| `swiaca.4` | 1 | +200 | 15.62 | W1000 G475 | — |
| `swibla.1` | 1 | +100 | 15.62 | W400 G90 | — |

_Cumulative peak: +300_


### tur

#### Food efficiency

| sid | lvl | +value | time (g-s) | cost | prereqs |
| --- | ---: | ---: | ---: | --- | --- |
| `turaca.1` | 1 | +40 | 15.62 | W200 G325 | — |
| `turaca.2` | 1 | +50 | 15.62 | W400 G522 | — |
| `turaca.3` | 1 | +50 | 15.62 | W2400 G850 | — |
| `tursta.1` | 1 | +140 | 15.62 | F600 G250 | — |

_Cumulative peak: +280_

#### Wood efficiency

| sid | lvl | +value | time (g-s) | cost | prereqs |
| --- | ---: | ---: | ---: | --- | --- |
| `turaca.8` | 1 | +100 | 15.62 | F5500 G550 | turbla |

_Cumulative peak: +100_

#### Stone efficiency

| sid | lvl | +value | time (g-s) | cost | prereqs |
| --- | ---: | ---: | ---: | --- | --- |
| `turaca.23` | 1 | +100 | 15.62 | G1550 I3000 | — |
| `turaca.24` | 1 | +200 | 15.62 | F4200 G1550 C12520 | — |

_Cumulative peak: +300_

#### Field HP (fieldlife)

| sid | lvl | +value | time (g-s) | cost | prereqs |
| --- | ---: | ---: | ---: | --- | --- |
| `turaca.4` | 1 | +200 | 15.62 | W1000 G475 | — |
| `turbla.1` | 1 | +100 | 15.62 | W400 G90 | — |

_Cumulative peak: +300_


### ukr

#### Food efficiency

| sid | lvl | +value | time (g-s) | cost | prereqs |
| --- | ---: | ---: | ---: | --- | --- |
| `ukraca.1` | 1 | +40 | 15.62 | W200 G325 | — |
| `ukraca.2` | 1 | +50 | 15.62 | W2400 G625 | — |
| `ukraca.3` | 1 | +50 | 15.62 | W3600 G850 | — |
| `ukrbar.1` | 1 | +140 | 15.62 | F750 G250 | — |
| `ukrbar.2` | 2 | +180 | 15.62 | F5600 G1350 I1900 | req0 |

_Cumulative peak: +460_

#### Wood efficiency

| sid | lvl | +value | time (g-s) | cost | prereqs |
| --- | ---: | ---: | ---: | --- | --- |
| `ukraca.8` | 1 | +100 | 15.62 | F5500 G550 | ukrbla |

_Cumulative peak: +100_

#### Stone efficiency

| sid | lvl | +value | time (g-s) | cost | prereqs |
| --- | ---: | ---: | ---: | --- | --- |
| `ukraca.23` | 1 | +100 | 15.62 | G1550 I3000 | — |
| `ukraca.24` | 1 | +200 | 15.62 | F4200 G1550 C12520 | — |

_Cumulative peak: +300_

#### Field HP (fieldlife)

| sid | lvl | +value | time (g-s) | cost | prereqs |
| --- | ---: | ---: | ---: | --- | --- |
| `ukraca.4` | 1 | +200 | 15.62 | W1000 G475 | — |
| `ukrbla.1` | 1 | +100 | 15.62 | W400 G90 | — |

_Cumulative peak: +300_


### ven

#### Food efficiency

| sid | lvl | +value | time (g-s) | cost | prereqs |
| --- | ---: | ---: | ---: | --- | --- |
| `venaca.1` | 1 | +40 | 15.62 | W200 G325 | — |
| `venaca.2` | 1 | +50 | 15.62 | W2400 G625 | — |
| `venaca.3` | 1 | +50 | 15.62 | W3600 G850 | — |
| `venbar.1` | 1 | +140 | 15.62 | F750 G250 | — |
| `venbar.2` | 2 | +180 | 15.62 | F25600 G3350 I2000 | req0 |

_Cumulative peak: +460_

#### Wood efficiency

| sid | lvl | +value | time (g-s) | cost | prereqs |
| --- | ---: | ---: | ---: | --- | --- |
| `venaca.8` | 1 | +100 | 15.62 | F5500 G550 | venbla |

_Cumulative peak: +100_

#### Stone efficiency

| sid | lvl | +value | time (g-s) | cost | prereqs |
| --- | ---: | ---: | ---: | --- | --- |
| `venaca.23` | 1 | +100 | 15.62 | G1550 I3000 | — |
| `venaca.24` | 1 | +200 | 15.62 | F4200 G1550 C12520 | — |

_Cumulative peak: +300_

#### Field HP (fieldlife)

| sid | lvl | +value | time (g-s) | cost | prereqs |
| --- | ---: | ---: | ---: | --- | --- |
| `venaca.4` | 1 | +200 | 15.62 | W1000 G475 | — |
| `venbla.1` | 1 | +100 | 15.62 | W400 G90 | — |

_Cumulative peak: +300_


---

Сгенерировано из `output/data.json`. Для перегенерации:

```
python compute/compute_efficiency_upgrades.py
```