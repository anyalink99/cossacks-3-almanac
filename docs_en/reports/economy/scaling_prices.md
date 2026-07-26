# Cossacks 3 – Building prices for the Nth instance

**Derived** file (calculated, not extracted). Considered from `data.json` script [`compute/compute_scaling.py`](../../../compute/compute_scaling.py).

## Formula

Price calculation - in `_unit_GetCostByID` [^1]:
```
costmodifier   = pow(costpercent / 100, count)         // count = уже у игрока
final_price[r] = floor(base_price[r] * costmodifier)   // отдельно для F/W/S/G/I/C
```
Where `count` is `gPlayer[plInd].counter.all[cid][unitID]`. The counter is incremented when [^2] is created and **decremented** when [^3] is destroyed - the center was demolished, the next one is cheaper again.

## Special cases

- `costpercent = 0` or `100` → no scaling, price is constant.
- For **mercenaries** (`bmercenary=True`), the counter is combined with a paired unit (`archerdip ↔ archerturdip`, `dragoon18dip ↔ lightcavalrydip`), and the modifier is limited above by the value **×2**. There are no mercenaries in this table - only buildings.
- For non-mercenaries, the modifier is limited from above to **×20000**. At N≤6 this limit never triggers (even for barracks with `costpercent=500`: 5⁵ = 3125 < 20000).
- **Round down (floor)** for each resource independently. For expensive buildings with `costpercent=104`, this results in stepped growth rather than smooth growth.

## Columns N=1..6

`N=1` — cost of the **first** copy (count=0, modifier=1, price = base). `N=2` - second (count=1), etc. Each cell is the total cost in the format `F<food> W<wood> S<stone> G<gold> I<iron> C<coal>` (zero resources are hidden).

## 1. Buildings by nation

Each nation has its own set. sid is formed as `<nat><suffix>`. Grouped by building type, all 21 nations in one table per type.

### 1.1 `cen` — Town Hall

| Nation | sid | Name | cost% | N=1 | N=2 | N=3 | N=4 | N=5 | N=6 | Note |
| --- | --- | --- | ---: | --- | --- | --- | --- | --- | --- | --- |
| alg | `algcen` | Town Hall | 300 | W450 S700 | W1350 S2100 | W4050 S6300 | W12150 S18900 | W36450 S56700 | W109350 S170100 | ×3 for each already built |
| aus | `auscen` | Town Hall | 300 | W700 S700 | W2100 S2100 | W6300 S6300 | W18900 S18900 | W56700 S56700 | W170100 S170100 | ×3 for each already built |
| bav | `bavcen` | Town Hall | 300 | W700 S700 | W2100 S2100 | W6300 S6300 | W18900 S18900 | W56700 S56700 | W170100 S170100 | ×3 for each already built |
| den | `dencen` | Town Hall | 300 | W700 S700 | W2100 S2100 | W6300 S6300 | W18900 S18900 | W56700 S56700 | W170100 S170100 | ×3 for each already built |
| eng | `engcen` | Town Hall | 300 | W700 S700 | W2100 S2100 | W6300 S6300 | W18900 S18900 | W56700 S56700 | W170100 S170100 | ×3 for each already built |
| fra | `fracen` | Town Hall | 300 | W700 S700 | W2100 S2100 | W6300 S6300 | W18900 S18900 | W56700 S56700 | W170100 S170100 | ×3 for each already built |
| hun | `huncen` | Town Hall | 300 | W700 S700 | W2100 S2100 | W6300 S6300 | W18900 S18900 | W56700 S56700 | W170100 S170100 | ×3 for each already built |
| net | `netcen` | Town Hall | 300 | W700 S700 | W2100 S2100 | W6300 S6300 | W18900 S18900 | W56700 S56700 | W170100 S170100 | ×3 for each already built |
| pie | `piecen` | Town Hall | 300 | W700 S700 | W2100 S2100 | W6300 S6300 | W18900 S18900 | W56700 S56700 | W170100 S170100 | ×3 for each already built |
| pol | `polcen` | Town Hall | 300 | W700 S700 | W2100 S2100 | W6300 S6300 | W18900 S18900 | W56700 S56700 | W170100 S170100 | ×3 for each already built |
| por | `porcen` | Town Hall | 300 | W700 S700 | W2100 S2100 | W6300 S6300 | W18900 S18900 | W56700 S56700 | W170100 S170100 | ×3 for each already built |
| pru | `prucen` | Town Hall | 300 | W700 S700 | W2100 S2100 | W6300 S6300 | W18900 S18900 | W56700 S56700 | W170100 S170100 | ×3 for each already built |
| rus | `ruscen` | Town Hall | 300 | W680 S700 | W2040 S2100 | W6120 S6300 | W18360 S18900 | W55080 S56700 | W165240 S170100 | ×3 for each already built |
| sax | `saxcen` | Town Hall | 300 | W700 S700 | W2100 S2100 | W6300 S6300 | W18900 S18900 | W56700 S56700 | W170100 S170100 | ×3 for each already built |
| sco | `scocen` | Town Hall | 300 | W700 S700 | W2100 S2100 | W6300 S6300 | W18900 S18900 | W56700 S56700 | W170100 S170100 | ×3 for each already built |
| spa | `spacen` | Town Hall | 300 | W700 S700 | W2100 S2100 | W6300 S6300 | W18900 S18900 | W56700 S56700 | W170100 S170100 | ×3 for each already built |
| swe | `swecen` | Town Hall | 300 | W700 S700 | W2100 S2100 | W6300 S6300 | W18900 S18900 | W56700 S56700 | W170100 S170100 | ×3 for each already built |
| swi | `swicen` | Town Hall | 300 | W700 S700 | W2100 S2100 | W6300 S6300 | W18900 S18900 | W56700 S56700 | W170100 S170100 | ×3 for each already built |
| tur | `turcen` | Town Hall | 300 | W600 S500 | W1800 S1500 | W5400 S4500 | W16200 S13500 | W48600 S40500 | W145800 S121500 | ×3 for each already built |
| ukr | `ukrcen` | Town Hall | 400 | W700 | W2800 | W11200 | W44800 | W179200 | W716800 | ×4 for each already built |
| ven | `vencen` | Town Hall | 300 | W700 S700 | W2100 S2100 | W6300 S6300 | W18900 S18900 | W56700 S56700 | W170100 S170100 | ×3 for each already built |

<a id="12-hou--дом"></a>
### 1.2 `hou` — Housing

| Nation | sid | Name | cost% | N=1 | N=2 | N=3 | N=4 | N=5 | N=6 | Note |
| --- | --- | --- | ---: | --- | --- | --- | --- | --- | --- | --- |
| alg | `alghou` | Housing | 104 | W100 S100 | W104 S104 | W108 S108 | W112 S112 | W116 S116 | W121 S121 | ×1.04 for each already built |
| aus | `aushou` | Housing | 104 | W100 S100 | W104 S104 | W108 S108 | W112 S112 | W116 S116 | W121 S121 | ×1.04 for each already built |
| bav | `bavhou` | Housing | 104 | W100 S100 | W104 S104 | W108 S108 | W112 S112 | W116 S116 | W121 S121 | ×1.04 for each already built |
| den | `denhou` | Housing | 104 | W100 S100 | W104 S104 | W108 S108 | W112 S112 | W116 S116 | W121 S121 | ×1.04 for each already built |
| eng | `enghou` | Housing | 104 | W100 S100 | W104 S104 | W108 S108 | W112 S112 | W116 S116 | W121 S121 | ×1.04 for each already built |
| fra | `frahou` | Housing | 104 | W100 S100 | W104 S104 | W108 S108 | W112 S112 | W116 S116 | W121 S121 | ×1.04 for each already built |
| hun | `hunhou` | Housing | 104 | W100 S100 | W104 S104 | W108 S108 | W112 S112 | W116 S116 | W121 S121 | ×1.04 for each already built |
| net | `nethou` | Housing | 104 | W100 S100 | W104 S104 | W108 S108 | W112 S112 | W116 S116 | W121 S121 | ×1.04 for each already built |
| pie | `piehou` | Housing | 104 | W100 S100 | W104 S104 | W108 S108 | W112 S112 | W116 S116 | W121 S121 | ×1.04 for each already built |
| pol | `polhou` | Housing | 104 | W100 S100 | W104 S104 | W108 S108 | W112 S112 | W116 S116 | W121 S121 | ×1.04 for each already built |
| por | `porhou` | Housing | 104 | W100 S100 | W104 S104 | W108 S108 | W112 S112 | W116 S116 | W121 S121 | ×1.04 for each already built |
| pru | `pruhou` | Housing | 104 | W100 S100 | W104 S104 | W108 S108 | W112 S112 | W116 S116 | W121 S121 | ×1.04 for each already built |
| rus | `rushou` | Izba | 104 | W120 | W124 | W129 | W134 | W140 | W145 | ×1.04 for each already built |
| sax | `saxhou` | Housing | 104 | W100 S100 | W104 S104 | W108 S108 | W112 S112 | W116 S116 | W121 S121 | ×1.04 for each already built |
| sco | `scohou` | Housing | 104 | W100 S100 | W104 S104 | W108 S108 | W112 S112 | W116 S116 | W121 S121 | ×1.04 for each already built |
| spa | `spahou` | Housing | 104 | W100 S100 | W104 S104 | W108 S108 | W112 S112 | W116 S116 | W121 S121 | ×1.04 for each already built |
| swe | `swehou` | Housing | 104 | W100 S100 | W104 S104 | W108 S108 | W112 S112 | W116 S116 | W121 S121 | ×1.04 for each already built |
| swi | `swihou` | Housing | 104 | W100 S100 | W104 S104 | W108 S108 | W112 S112 | W116 S116 | W121 S121 | ×1.04 for each already built |
| tur | `turhou` | Housing | 106 | W100 S100 | W106 S106 | W112 S112 | W119 S119 | W126 S126 | W133 S133 | ×1.06 for each already built |
| ukr | `ukrhou` | Hut | 105 | W120 | W126 | W132 | W138 | W145 | W153 | ×1.05 for each already built |
| ven | `venhou` | Housing | 104 | W100 S100 | W104 S104 | W108 S108 | W112 S112 | W116 S116 | W121 S121 | ×1.04 for each already built |

<a id="13-bar--казарма-17-в"></a>
### 1.3 `bar` - Barracks 17th century.

| Nation | sid | Name | cost% | N=1 | N=2 | N=3 | N=4 | N=5 | N=6 | Note |
| --- | --- | --- | ---: | --- | --- | --- | --- | --- | --- | --- |
| alg | `algbar` | Barracks | 500 | W400 S400 | W2000 S2000 | W10000 S10000 | W50000 S50000 | W250000 S250000 | W1250000 S1250000 | ×5 for each already built |
| aus | `ausbar` | Barracks, 17th century | 500 | W100 S100 G500 | W500 S500 G2500 | W2500 S2500 G12500 | W12500 S12500 G62500 | W62500 S62500 G312500 | W312500 S312500 G1562500 | ×5 for each already built |
| bav | `bavbar` | Barracks, 17th century | 500 | W100 S100 G500 | W500 S500 G2500 | W2500 S2500 G12500 | W12500 S12500 G62500 | W62500 S62500 G312500 | W312500 S312500 G1562500 | ×5 for each already built |
| den | `denbar` | Barracks, 17th century | 500 | W100 S100 G500 | W500 S500 G2500 | W2500 S2500 G12500 | W12500 S12500 G62500 | W62500 S62500 G312500 | W312500 S312500 G1562500 | ×5 for each already built |
| eng | `engbar` | Barracks, 17th century | 500 | W100 S100 G500 | W500 S500 G2500 | W2500 S2500 G12500 | W12500 S12500 G62500 | W62500 S62500 G312500 | W312500 S312500 G1562500 | ×5 for each already built |
| fra | `frabar` | Barracks, 17th century | 500 | W100 S100 G500 | W500 S500 G2500 | W2500 S2500 G12500 | W12500 S12500 G62500 | W62500 S62500 G312500 | W312500 S312500 G1562500 | ×5 for each already built |
| hun | `hunbar` | Barracks, 17th century | 500 | W100 S100 G500 | W500 S500 G2500 | W2500 S2500 G12500 | W12500 S12500 G62500 | W62500 S62500 G312500 | W312500 S312500 G1562500 | ×5 for each already built |
| net | `netbar` | Barracks, 17th century | 500 | W100 S100 G500 | W500 S500 G2500 | W2500 S2500 G12500 | W12500 S12500 G62500 | W62500 S62500 G312500 | W312500 S312500 G1562500 | ×5 for each already built |
| pie | `piebar` | Barracks, 17th century | 500 | W100 S100 G500 | W500 S500 G2500 | W2500 S2500 G12500 | W12500 S12500 G62500 | W62500 S62500 G312500 | W312500 S312500 G1562500 | ×5 for each already built |
| pol | `polbar` | Barracks, 17th century | 500 | W100 S100 G500 | W500 S500 G2500 | W2500 S2500 G12500 | W12500 S12500 G62500 | W62500 S62500 G312500 | W312500 S312500 G1562500 | ×5 for each already built |
| por | `porbar` | Barracks, 17th century | 500 | W100 S100 G500 | W500 S500 G2500 | W2500 S2500 G12500 | W12500 S12500 G62500 | W62500 S62500 G312500 | W312500 S312500 G1562500 | ×5 for each already built |
| pru | `prubar` | Barracks, 17th century | 500 | W100 S100 G500 | W500 S500 G2500 | W2500 S2500 G12500 | W12500 S12500 G62500 | W62500 S62500 G312500 | W312500 S312500 G1562500 | ×5 for each already built |
| rus | `rusbar` | Strelets Barracks | 300 | W200 S20 | W600 S60 | W1800 S180 | W5400 S540 | W16200 S1620 | W48600 S4860 | ×3 for each already built |
| sax | `saxbar` | Barracks, 17th century | 500 | W100 S100 G500 | W500 S500 G2500 | W2500 S2500 G12500 | W12500 S12500 G62500 | W62500 S62500 G312500 | W312500 S312500 G1562500 | ×5 for each already built |
| sco | `scobar` | Barracks, 17th century | 500 | W100 S100 G500 | W500 S500 G2500 | W2500 S2500 G12500 | W12500 S12500 G62500 | W62500 S62500 G312500 | W312500 S312500 G1562500 | ×5 for each already built |
| spa | `spabar` | Barracks, 17th century | 500 | W100 S100 G500 | W500 S500 G2500 | W2500 S2500 G12500 | W12500 S12500 G62500 | W62500 S62500 G312500 | W312500 S312500 G1562500 | ×5 for each already built |
| swe | `swebar` | Barracks, 17th century | 500 | W100 S100 G500 | W500 S500 G2500 | W2500 S2500 G12500 | W12500 S12500 G62500 | W62500 S62500 G312500 | W312500 S312500 G1562500 | ×5 for each already built |
| swi | `swibar` | Barracks, 17th century | 500 | W100 S100 G500 | W500 S500 G2500 | W2500 S2500 G12500 | W12500 S12500 G62500 | W62500 S62500 G312500 | W312500 S312500 G1562500 | ×5 for each already built |
| tur | `turbar` | Barracks | 500 | W400 S400 | W2000 S2000 | W10000 S10000 | W50000 S50000 | W250000 S250000 | W1250000 S1250000 | ×5 for each already built |
| ukr | `ukrbar` | Cossack House | 300 | W150 S150 | W450 S450 | W1350 S1350 | W4050 S4050 | W12150 S12150 | W36450 S36450 | ×3 for each already built |
| ven | `venbar` | Barracks, 17th century | 500 | W100 S100 G500 | W500 S500 G2500 | W2500 S2500 G12500 | W12500 S12500 G62500 | W62500 S62500 G312500 | W312500 S312500 G1562500 | ×5 for each already built |

<a id="14-ba2--казарма-18-в"></a>
### 1.4 `ba2` - Barracks 18th century.

| Nation | sid | Name | cost% | N=1 | N=2 | N=3 | N=4 | N=5 | N=6 | Note |
| --- | --- | --- | ---: | --- | --- | --- | --- | --- | --- | --- |
| aus | `ausba2` | Barracks, 18th century | 200 | W1700 S2950 G4000 | W3400 S5900 G8000 | W6800 S11800 G16000 | W13600 S23600 G32000 | W27200 S47200 G64000 | W54400 S94400 G128000 | ×2 for each already built |
| bav | `bavba2` | Barracks, 18th century | 200 | W1700 S2950 G4000 | W3400 S5900 G8000 | W6800 S11800 G16000 | W13600 S23600 G32000 | W27200 S47200 G64000 | W54400 S94400 G128000 | ×2 for each already built |
| den | `denba2` | Barracks, 18th century | 200 | W1700 S2950 G4000 | W3400 S5900 G8000 | W6800 S11800 G16000 | W13600 S23600 G32000 | W27200 S47200 G64000 | W54400 S94400 G128000 | ×2 for each already built |
| eng | `engba2` | Barracks, 18th century | 200 | W1700 S2950 G4000 | W3400 S5900 G8000 | W6800 S11800 G16000 | W13600 S23600 G32000 | W27200 S47200 G64000 | W54400 S94400 G128000 | ×2 for each already built |
| fra | `fraba2` | Barracks, 18th century | 200 | W1700 S2950 G4000 | W3400 S5900 G8000 | W6800 S11800 G16000 | W13600 S23600 G32000 | W27200 S47200 G64000 | W54400 S94400 G128000 | ×2 for each already built |
| hun | `hunba2` | Barracks, 18th century | 200 | W1700 S2950 G4000 | W3400 S5900 G8000 | W6800 S11800 G16000 | W13600 S23600 G32000 | W27200 S47200 G64000 | W54400 S94400 G128000 | ×2 for each already built |
| net | `netba2` | Barracks, 18th century | 200 | W1700 S2950 G4000 | W3400 S5900 G8000 | W6800 S11800 G16000 | W13600 S23600 G32000 | W27200 S47200 G64000 | W54400 S94400 G128000 | ×2 for each already built |
| pie | `pieba2` | Barracks, 18th century | 200 | W1700 S2950 G4000 | W3400 S5900 G8000 | W6800 S11800 G16000 | W13600 S23600 G32000 | W27200 S47200 G64000 | W54400 S94400 G128000 | ×2 for each already built |
| pol | `polba2` | Barracks, 18th century | 200 | W1700 S2950 G4000 | W3400 S5900 G8000 | W6800 S11800 G16000 | W13600 S23600 G32000 | W27200 S47200 G64000 | W54400 S94400 G128000 | ×2 for each already built |
| por | `porba2` | Barracks, 18th century | 200 | W1700 S2950 G4000 | W3400 S5900 G8000 | W6800 S11800 G16000 | W13600 S23600 G32000 | W27200 S47200 G64000 | W54400 S94400 G128000 | ×2 for each already built |
| pru | `pruba2` | Barracks, 18th century | 200 | W1700 S2950 G4000 | W3400 S5900 G8000 | W6800 S11800 G16000 | W13600 S23600 G32000 | W27200 S47200 G64000 | W54400 S94400 G128000 | ×2 for each already built |
| rus | `rusba2` | Barracks, 18th century | 200 | W1700 S2950 G4000 | W3400 S5900 G8000 | W6800 S11800 G16000 | W13600 S23600 G32000 | W27200 S47200 G64000 | W54400 S94400 G128000 | ×2 for each already built |
| sax | `saxba2` | Barracks, 18th century | 200 | W1700 S2950 G4000 | W3400 S5900 G8000 | W6800 S11800 G16000 | W13600 S23600 G32000 | W27200 S47200 G64000 | W54400 S94400 G128000 | ×2 for each already built |
| sco | `scoba2` | Castle | 250 | W640 S2400 G2400 | W1600 S6000 G6000 | W4000 S15000 G15000 | W10000 S37500 G37500 | W25000 S93750 G93750 | W62500 S234375 G234375 | ×2.5 for each already built |
| spa | `spaba2` | Barracks, 18th century | 200 | W1700 S2950 G4000 | W3400 S5900 G8000 | W6800 S11800 G16000 | W13600 S23600 G32000 | W27200 S47200 G64000 | W54400 S94400 G128000 | ×2 for each already built |
| swe | `sweba2` | Barracks, 18th century | 200 | W1700 S2950 G4000 | W3400 S5900 G8000 | W6800 S11800 G16000 | W13600 S23600 G32000 | W27200 S47200 G64000 | W54400 S94400 G128000 | ×2 for each already built |
| swi | `swiba2` | Barracks, 18th century | 200 | W1700 S2950 G4000 | W3400 S5900 G8000 | W6800 S11800 G16000 | W13600 S23600 G32000 | W27200 S47200 G64000 | W54400 S94400 G128000 | ×2 for each already built |
| ven | `venba2` | Barracks, 18th century | 200 | W1700 S2950 G4000 | W3400 S5900 G8000 | W6800 S11800 G16000 | W13600 S23600 G32000 | W27200 S47200 G64000 | W54400 S94400 G128000 | ×2 for each already built |

<a id="15-bla--кузница"></a>
### 1.5 `bla` — Blacksmith

| Nation | sid | Name | cost% | N=1 | N=2 | N=3 | N=4 | N=5 | N=6 | Note |
| --- | --- | --- | ---: | --- | --- | --- | --- | --- | --- | --- |
| alg | `algbla` | Blacksmith | 400 | W100 S30 I640 | W400 S120 I2560 | W1600 S480 I10240 | W6400 S1920 I40960 | W25600 S7680 I163840 | W102400 S30720 I655360 | ×4 for each already built |
| aus | `ausbla` | Blacksmith | 400 | W100 S30 I640 | W400 S120 I2560 | W1600 S480 I10240 | W6400 S1920 I40960 | W25600 S7680 I163840 | W102400 S30720 I655360 | ×4 for each already built |
| bav | `bavbla` | Blacksmith | 400 | W100 S30 I640 | W400 S120 I2560 | W1600 S480 I10240 | W6400 S1920 I40960 | W25600 S7680 I163840 | W102400 S30720 I655360 | ×4 for each already built |
| den | `denbla` | Blacksmith | 400 | W100 S30 I640 | W400 S120 I2560 | W1600 S480 I10240 | W6400 S1920 I40960 | W25600 S7680 I163840 | W102400 S30720 I655360 | ×4 for each already built |
| eng | `engbla` | Blacksmith | 400 | W100 S30 I640 | W400 S120 I2560 | W1600 S480 I10240 | W6400 S1920 I40960 | W25600 S7680 I163840 | W102400 S30720 I655360 | ×4 for each already built |
| fra | `frabla` | Blacksmith | 600 | W100 S30 I640 | W600 S180 I3840 | W3600 S1080 I23040 | W21600 S6480 I138240 | W129600 S38880 I829440 | W777600 S233280 I4976640 | ×6 for each already built |
| hun | `hunbla` | Blacksmith | 400 | W100 S30 I640 | W400 S120 I2560 | W1600 S480 I10240 | W6400 S1920 I40960 | W25600 S7680 I163840 | W102400 S30720 I655360 | ×4 for each already built |
| net | `netbla` | Blacksmith | 400 | W100 S30 I640 | W400 S120 I2560 | W1600 S480 I10240 | W6400 S1920 I40960 | W25600 S7680 I163840 | W102400 S30720 I655360 | ×4 for each already built |
| pie | `piebla` | Blacksmith | 400 | W100 S30 I640 | W400 S120 I2560 | W1600 S480 I10240 | W6400 S1920 I40960 | W25600 S7680 I163840 | W102400 S30720 I655360 | ×4 for each already built |
| pol | `polbla` | Blacksmith | 400 | W100 S30 I640 | W400 S120 I2560 | W1600 S480 I10240 | W6400 S1920 I40960 | W25600 S7680 I163840 | W102400 S30720 I655360 | ×4 for each already built |
| por | `porbla` | Blacksmith | 400 | W100 S30 I640 | W400 S120 I2560 | W1600 S480 I10240 | W6400 S1920 I40960 | W25600 S7680 I163840 | W102400 S30720 I655360 | ×4 for each already built |
| pru | `prubla` | Blacksmith | 400 | W100 S30 I640 | W400 S120 I2560 | W1600 S480 I10240 | W6400 S1920 I40960 | W25600 S7680 I163840 | W102400 S30720 I655360 | ×4 for each already built |
| rus | `rusbla` | Blacksmith | 400 | W100 S30 I640 | W400 S120 I2560 | W1600 S480 I10240 | W6400 S1920 I40960 | W25600 S7680 I163840 | W102400 S30720 I655360 | ×4 for each already built |
| sax | `saxbla` | Blacksmith | 400 | W100 S30 I640 | W400 S120 I2560 | W1600 S480 I10240 | W6400 S1920 I40960 | W25600 S7680 I163840 | W102400 S30720 I655360 | ×4 for each already built |
| sco | `scobla` | Blacksmith | 400 | W100 S30 I640 | W400 S120 I2560 | W1600 S480 I10240 | W6400 S1920 I40960 | W25600 S7680 I163840 | W102400 S30720 I655360 | ×4 for each already built |
| spa | `spabla` | Blacksmith | 400 | W100 S30 I640 | W400 S120 I2560 | W1600 S480 I10240 | W6400 S1920 I40960 | W25600 S7680 I163840 | W102400 S30720 I655360 | ×4 for each already built |
| swe | `swebla` | Blacksmith | 400 | W100 S30 I640 | W400 S120 I2560 | W1600 S480 I10240 | W6400 S1920 I40960 | W25600 S7680 I163840 | W102400 S30720 I655360 | ×4 for each already built |
| swi | `swibla` | Blacksmith | 400 | W100 S30 I640 | W400 S120 I2560 | W1600 S480 I10240 | W6400 S1920 I40960 | W25600 S7680 I163840 | W102400 S30720 I655360 | ×4 for each already built |
| tur | `turbla` | Blacksmith | 400 | W100 S30 I640 | W400 S120 I2560 | W1600 S480 I10240 | W6400 S1920 I40960 | W25600 S7680 I163840 | W102400 S30720 I655360 | ×4 for each already built |
| ukr | `ukrbla` | Blacksmith | 400 | W100 S30 I640 | W400 S120 I2560 | W1600 S480 I10240 | W6400 S1920 I40960 | W25600 S7680 I163840 | W102400 S30720 I655360 | ×4 for each already built |
| ven | `venbla` | Blacksmith | 400 | W100 S30 I640 | W400 S120 I2560 | W1600 S480 I10240 | W6400 S1920 I40960 | W25600 S7680 I163840 | W102400 S30720 I655360 | ×4 for each already built |

<a id="16-sta--конюшня"></a>
### 1.6 `sta` - Stable

| Nation | sid | Name | cost% | N=1 | N=2 | N=3 | N=4 | N=5 | N=6 | Note |
| --- | --- | --- | ---: | --- | --- | --- | --- | --- | --- | --- |
| alg | `algsta` | Stable | 700 | W1000 S2200 | W7000 S15400 | W49000 S107800 | W343000 S754600 | W2401000 S5282200 | W16807000 S36975400 | ×7 for each already built |
| aus | `aussta` | Stable | 200 | W2500 S100 G600 | W5000 S200 G1200 | W10000 S400 G2400 | W20000 S800 G4800 | W40000 S1600 G9600 | W80000 S3200 G19200 | ×2 for each already built |
| bav | `bavsta` | Stable | 200 | W2500 S100 G600 | W5000 S200 G1200 | W10000 S400 G2400 | W20000 S800 G4800 | W40000 S1600 G9600 | W80000 S3200 G19200 | ×2 for each already built |
| den | `densta` | Stable | 200 | W2500 S100 G600 | W5000 S200 G1200 | W10000 S400 G2400 | W20000 S800 G4800 | W40000 S1600 G9600 | W80000 S3200 G19200 | ×2 for each already built |
| eng | `engsta` | Stable | 200 | W2350 G800 | W4700 G1600 | W9400 G3200 | W18800 G6400 | W37600 G12800 | W75200 G25600 | ×2 for each already built |
| fra | `frasta` | Stable | 200 | W2500 S100 G600 | W5000 S200 G1200 | W10000 S400 G2400 | W20000 S800 G4800 | W40000 S1600 G9600 | W80000 S3200 G19200 | ×2 for each already built |
| hun | `hunsta` | Stable | 200 | W2500 S100 G600 | W5000 S200 G1200 | W10000 S400 G2400 | W20000 S800 G4800 | W40000 S1600 G9600 | W80000 S3200 G19200 | ×2 for each already built |
| net | `netsta` | Stable | 200 | W2500 S100 G600 | W5000 S200 G1200 | W10000 S400 G2400 | W20000 S800 G4800 | W40000 S1600 G9600 | W80000 S3200 G19200 | ×2 for each already built |
| pie | `piesta` | Stable | 200 | W2500 S100 G600 | W5000 S200 G1200 | W10000 S400 G2400 | W20000 S800 G4800 | W40000 S1600 G9600 | W80000 S3200 G19200 | ×2 for each already built |
| pol | `polsta` | Stable | 200 | W2500 S100 G600 | W5000 S200 G1200 | W10000 S400 G2400 | W20000 S800 G4800 | W40000 S1600 G9600 | W80000 S3200 G19200 | ×2 for each already built |
| por | `porsta` | Stable | 200 | W2500 S100 G600 | W5000 S200 G1200 | W10000 S400 G2400 | W20000 S800 G4800 | W40000 S1600 G9600 | W80000 S3200 G19200 | ×2 for each already built |
| pru | `prusta` | Stable | 200 | W2500 S100 G600 | W5000 S200 G1200 | W10000 S400 G2400 | W20000 S800 G4800 | W40000 S1600 G9600 | W80000 S3200 G19200 | ×2 for each already built |
| rus | `russta` | Stable | 200 | W7950 G550 | W15900 G1100 | W31800 G2200 | W63600 G4400 | W127200 G8800 | W254400 G17600 | ×2 for each already built |
| sax | `saxsta` | Stable | 200 | W2500 S100 G600 | W5000 S200 G1200 | W10000 S400 G2400 | W20000 S800 G4800 | W40000 S1600 G9600 | W80000 S3200 G19200 | ×2 for each already built |
| sco | `scosta` | Stable | 200 | W2350 G800 | W4700 G1600 | W9400 G3200 | W18800 G6400 | W37600 G12800 | W75200 G25600 | ×2 for each already built |
| spa | `spasta` | Stable | 200 | W2500 S100 G600 | W5000 S200 G1200 | W10000 S400 G2400 | W20000 S800 G4800 | W40000 S1600 G9600 | W80000 S3200 G19200 | ×2 for each already built |
| swe | `swesta` | Stable | 200 | W2500 S100 G600 | W5000 S200 G1200 | W10000 S400 G2400 | W20000 S800 G4800 | W40000 S1600 G9600 | W80000 S3200 G19200 | ×2 for each already built |
| swi | `swista` | Stable | 200 | W2500 S100 G600 | W5000 S200 G1200 | W10000 S400 G2400 | W20000 S800 G4800 | W40000 S1600 G9600 | W80000 S3200 G19200 | ×2 for each already built |
| tur | `tursta` | Stable | 700 | W1000 S2600 | W7000 S18200 | W49000 S127400 | W343000 S891800 | W2401000 S6242600 | W16807000 S43698200 | ×7 for each already built |
| ukr | `ukrsta` | Stable | 300 | W3200 S850 G850 | W9600 S2550 G2550 | W28800 S7650 G7650 | W86400 S22950 G22950 | W259200 S68850 G68850 | W777600 S206550 G206550 | ×3 for each already built |
| ven | `vensta` | Stable | 200 | W2500 S100 G600 | W5000 S200 G1200 | W10000 S400 G2400 | W20000 S800 G4800 | W40000 S1600 G9600 | W80000 S3200 G19200 | ×2 for each already built |

<a id="17-tem--собор"></a>
### 1.7 `tem` - Cathedral

| Nation | sid | Name | cost% | N=1 | N=2 | N=3 | N=4 | N=5 | N=6 | Note |
| --- | --- | --- | ---: | --- | --- | --- | --- | --- | --- | --- |
| alg | `algtem` | Mosque | 300 | W1000 S1200 I500 | W3000 S3600 I1500 | W9000 S10800 I4500 | W27000 S32400 I13500 | W81000 S97200 I40500 | W243000 S291600 I121500 | ×3 for each already built |
| aus | `austem` | Cathedral | 300 | W1000 S1200 I500 | W3000 S3600 I1500 | W9000 S10800 I4500 | W27000 S32400 I13500 | W81000 S97200 I40500 | W243000 S291600 I121500 | ×3 for each already built |
| bav | `bavtem` | Cathedral | 300 | W1000 S1200 I500 | W3000 S3600 I1500 | W9000 S10800 I4500 | W27000 S32400 I13500 | W81000 S97200 I40500 | W243000 S291600 I121500 | ×3 for each already built |
| den | `dentem` | Cathedral | 300 | W1000 S1200 I500 | W3000 S3600 I1500 | W9000 S10800 I4500 | W27000 S32400 I13500 | W81000 S97200 I40500 | W243000 S291600 I121500 | ×3 for each already built |
| eng | `engtem` | Cathedral | 300 | W1000 S1200 I500 | W3000 S3600 I1500 | W9000 S10800 I4500 | W27000 S32400 I13500 | W81000 S97200 I40500 | W243000 S291600 I121500 | ×3 for each already built |
| fra | `fratem` | Cathedral | 300 | W1100 S2000 I600 | W3300 S6000 I1800 | W9900 S18000 I5400 | W29700 S54000 I16200 | W89100 S162000 I48600 | W267300 S486000 I145800 | ×3 for each already built |
| hun | `huntem` | Cathedral | 300 | W1000 S1200 I500 | W3000 S3600 I1500 | W9000 S10800 I4500 | W27000 S32400 I13500 | W81000 S97200 I40500 | W243000 S291600 I121500 | ×3 for each already built |
| net | `nettem` | Cathedral | 300 | W1000 S1200 I500 | W3000 S3600 I1500 | W9000 S10800 I4500 | W27000 S32400 I13500 | W81000 S97200 I40500 | W243000 S291600 I121500 | ×3 for each already built |
| pie | `pietem` | Cathedral | 300 | W1000 S1200 I500 | W3000 S3600 I1500 | W9000 S10800 I4500 | W27000 S32400 I13500 | W81000 S97200 I40500 | W243000 S291600 I121500 | ×3 for each already built |
| pol | `poltem` | Cathedral | 300 | W1000 S1200 I500 | W3000 S3600 I1500 | W9000 S10800 I4500 | W27000 S32400 I13500 | W81000 S97200 I40500 | W243000 S291600 I121500 | ×3 for each already built |
| por | `portem` | Cathedral | 300 | W1000 S1200 I500 | W3000 S3600 I1500 | W9000 S10800 I4500 | W27000 S32400 I13500 | W81000 S97200 I40500 | W243000 S291600 I121500 | ×3 for each already built |
| pru | `prutem` | Cathedral | 300 | W1000 S1200 I500 | W3000 S3600 I1500 | W9000 S10800 I4500 | W27000 S32400 I13500 | W81000 S97200 I40500 | W243000 S291600 I121500 | ×3 for each already built |
| rus | `rustem` | Orthodox Cathedral | 300 | W1150 S1650 G100 I500 | W3450 S4950 G300 I1500 | W10350 S14850 G900 I4500 | W31050 S44550 G2700 I13500 | W93150 S133650 G8100 I40500 | W279450 S400950 G24300 I121500 | ×3 for each already built |
| sax | `saxtem` | Cathedral | 300 | W1000 S1200 I500 | W3000 S3600 I1500 | W9000 S10800 I4500 | W27000 S32400 I13500 | W81000 S97200 I40500 | W243000 S291600 I121500 | ×3 for each already built |
| sco | `scotem` | Cathedral | 300 | W1000 S1200 I500 | W3000 S3600 I1500 | W9000 S10800 I4500 | W27000 S32400 I13500 | W81000 S97200 I40500 | W243000 S291600 I121500 | ×3 for each already built |
| spa | `spatem` | Cathedral | 300 | W1000 S1200 I500 | W3000 S3600 I1500 | W9000 S10800 I4500 | W27000 S32400 I13500 | W81000 S97200 I40500 | W243000 S291600 I121500 | ×3 for each already built |
| swe | `swetem` | Cathedral | 300 | W1000 S1200 I500 | W3000 S3600 I1500 | W9000 S10800 I4500 | W27000 S32400 I13500 | W81000 S97200 I40500 | W243000 S291600 I121500 | ×3 for each already built |
| swi | `switem` | Cathedral | 300 | W1000 S1200 I500 | W3000 S3600 I1500 | W9000 S10800 I4500 | W27000 S32400 I13500 | W81000 S97200 I40500 | W243000 S291600 I121500 | ×3 for each already built |
| tur | `turtem` | Mosque | 300 | W1000 S1200 I500 | W3000 S3600 I1500 | W9000 S10800 I4500 | W27000 S32400 I13500 | W81000 S97200 I40500 | W243000 S291600 I121500 | ×3 for each already built |
| ukr | `ukrtem` | Orthodox Cathedral | 300 | W1100 S1400 I300 | W3300 S4200 I900 | W9900 S12600 I2700 | W29700 S37800 I8100 | W89100 S113400 I24300 | W267300 S340200 I72900 | ×3 for each already built |
| ven | `ventem` | Cathedral | 300 | W1000 S1200 I500 | W3000 S3600 I1500 | W9000 S10800 I4500 | W27000 S32400 I13500 | W81000 S97200 I40500 | W243000 S291600 I121500 | ×3 for each already built |

<a id="18-aca--академия"></a>
### 1.8 `aca` — Academy

| Nation | sid | Name | cost% | N=1 | N=2 | N=3 | N=4 | N=5 | N=6 | Note |
| --- | --- | --- | ---: | --- | --- | --- | --- | --- | --- | --- |
| alg | `algaca` | Minaret | 300 | W1450 S1100 | W4350 S3300 | W13050 S9900 | W39150 S29700 | W117450 S89100 | W352350 S267300 | ×3 for each already built |
| aus | `ausaca` | Academy | 300 | W1250 S1100 | W3750 S3300 | W11250 S9900 | W33750 S29700 | W101250 S89100 | W303750 S267300 | ×3 for each already built |
| bav | `bavaca` | Academy | 300 | W1250 S1100 | W3750 S3300 | W11250 S9900 | W33750 S29700 | W101250 S89100 | W303750 S267300 | ×3 for each already built |
| den | `denaca` | Academy | 300 | W1450 S900 | W4350 S2700 | W13050 S8100 | W39150 S24300 | W117450 S72900 | W352350 S218700 | ×3 for each already built |
| eng | `engaca` | Academy | 300 | W1150 S1200 | W3450 S3600 | W10350 S10800 | W31050 S32400 | W93150 S97200 | W279450 S291600 | ×3 for each already built |
| fra | `fraaca` | Academy | 300 | W1250 S1100 | W3750 S3300 | W11250 S9900 | W33750 S29700 | W101250 S89100 | W303750 S267300 | ×3 for each already built |
| hun | `hunaca` | Academy | 300 | W1250 S1100 | W3750 S3300 | W11250 S9900 | W33750 S29700 | W101250 S89100 | W303750 S267300 | ×3 for each already built |
| net | `netaca` | Academy | 300 | W1050 S1230 | W3150 S3690 | W9450 S11070 | W28350 S33210 | W85050 S99630 | W255150 S298890 | ×3 for each already built |
| pie | `pieaca` | Academy | 300 | W1250 S1100 | W3750 S3300 | W11250 S9900 | W33750 S29700 | W101250 S89100 | W303750 S267300 | ×3 for each already built |
| pol | `polaca` | Academy | 300 | W950 S800 | W2850 S2400 | W8550 S7200 | W25650 S21600 | W76950 S64800 | W230850 S194400 | ×3 for each already built |
| por | `poraca` | Academy | 300 | W1250 S1100 | W3750 S3300 | W11250 S9900 | W33750 S29700 | W101250 S89100 | W303750 S267300 | ×3 for each already built |
| pru | `pruaca` | Academy | 300 | W1200 S1150 | W3600 S3450 | W10800 S10350 | W32400 S31050 | W97200 S93150 | W291600 S279450 | ×3 for each already built |
| rus | `rusaca` | Academy | 300 | W1250 S1300 | W3750 S3900 | W11250 S11700 | W33750 S35100 | W101250 S105300 | W303750 S315900 | ×3 for each already built |
| sax | `saxaca` | Academy | 300 | W1250 S1100 | W3750 S3300 | W11250 S9900 | W33750 S29700 | W101250 S89100 | W303750 S267300 | ×3 for each already built |
| sco | `scoaca` | Academy | 300 | W1250 S1100 | W3750 S3300 | W11250 S9900 | W33750 S29700 | W101250 S89100 | W303750 S267300 | ×3 for each already built |
| spa | `spaaca` | Academy | 300 | W1350 S1000 | W4050 S3000 | W12150 S9000 | W36450 S27000 | W109350 S81000 | W328050 S243000 | ×3 for each already built |
| swe | `sweaca` | Academy | 300 | W1350 S1000 | W4050 S3000 | W12150 S9000 | W36450 S27000 | W109350 S81000 | W328050 S243000 | ×3 for each already built |
| swi | `swiaca` | Academy | 300 | W1250 S1100 | W3750 S3300 | W11250 S9900 | W33750 S29700 | W101250 S89100 | W303750 S267300 | ×3 for each already built |
| tur | `turaca` | Minaret | 300 | W1450 S1100 | W4350 S3300 | W13050 S9900 | W39150 S29700 | W117450 S89100 | W352350 S267300 | ×3 for each already built |
| ukr | `ukraca` | Academy | 300 | W1350 S1200 | W4050 S3600 | W12150 S10800 | W36450 S32400 | W109350 S97200 | W328050 S291600 | ×3 for each already built |
| ven | `venaca` | Academy | 300 | W1090 S1260 | W3270 S3780 | W9810 S11340 | W29430 S34020 | W88290 S102060 | W264870 S306180 | ×3 for each already built |

<a id="19-art--артиллерийское-депо"></a>
### 1.9 `art` — Artillery Depot

| Nation | sid | Name | cost% | N=1 | N=2 | N=3 | N=4 | N=5 | N=6 | Note |
| --- | --- | --- | ---: | --- | --- | --- | --- | --- | --- | --- |
| alg | `algart` | Artillery Depot | 200 | W100 S1000 C1400 | W200 S2000 C2800 | W400 S4000 C5600 | W800 S8000 C11200 | W1600 S16000 C22400 | W3200 S32000 C44800 | ×2 for each already built |
| aus | `ausart` | Artillery Depot | 200 | W100 S1000 C1400 | W200 S2000 C2800 | W400 S4000 C5600 | W800 S8000 C11200 | W1600 S16000 C22400 | W3200 S32000 C44800 | ×2 for each already built |
| bav | `bavart` | Artillery Depot | 200 | W100 S1000 C1400 | W200 S2000 C2800 | W400 S4000 C5600 | W800 S8000 C11200 | W1600 S16000 C22400 | W3200 S32000 C44800 | ×2 for each already built |
| den | `denart` | Artillery Depot | 200 | W100 S1000 C1400 | W200 S2000 C2800 | W400 S4000 C5600 | W800 S8000 C11200 | W1600 S16000 C22400 | W3200 S32000 C44800 | ×2 for each already built |
| eng | `engart` | Artillery Depot | 200 | W100 S1000 C1400 | W200 S2000 C2800 | W400 S4000 C5600 | W800 S8000 C11200 | W1600 S16000 C22400 | W3200 S32000 C44800 | ×2 for each already built |
| fra | `fraart` | Artillery Depot | 200 | W100 S1000 C1400 | W200 S2000 C2800 | W400 S4000 C5600 | W800 S8000 C11200 | W1600 S16000 C22400 | W3200 S32000 C44800 | ×2 for each already built |
| hun | `hunart` | Artillery Depot | 200 | W100 S1000 C1400 | W200 S2000 C2800 | W400 S4000 C5600 | W800 S8000 C11200 | W1600 S16000 C22400 | W3200 S32000 C44800 | ×2 for each already built |
| net | `netart` | Artillery Depot | 200 | W100 S1000 C1400 | W200 S2000 C2800 | W400 S4000 C5600 | W800 S8000 C11200 | W1600 S16000 C22400 | W3200 S32000 C44800 | ×2 for each already built |
| pie | `pieart` | Artillery Depot | 200 | W100 S1000 C1400 | W200 S2000 C2800 | W400 S4000 C5600 | W800 S8000 C11200 | W1600 S16000 C22400 | W3200 S32000 C44800 | ×2 for each already built |
| pol | `polart` | Artillery Depot | 200 | W100 S1000 C1400 | W200 S2000 C2800 | W400 S4000 C5600 | W800 S8000 C11200 | W1600 S16000 C22400 | W3200 S32000 C44800 | ×2 for each already built |
| por | `porart` | Artillery Depot | 200 | W100 S1000 C1400 | W200 S2000 C2800 | W400 S4000 C5600 | W800 S8000 C11200 | W1600 S16000 C22400 | W3200 S32000 C44800 | ×2 for each already built |
| pru | `pruart` | Artillery Depot | 200 | W100 S1000 C1400 | W200 S2000 C2800 | W400 S4000 C5600 | W800 S8000 C11200 | W1600 S16000 C22400 | W3200 S32000 C44800 | ×2 for each already built |
| rus | `rusart` | Artillery Depot | 200 | W100 S1000 C1400 | W200 S2000 C2800 | W400 S4000 C5600 | W800 S8000 C11200 | W1600 S16000 C22400 | W3200 S32000 C44800 | ×2 for each already built |
| sax | `saxart` | Artillery Depot | 200 | W100 S1000 C1400 | W200 S2000 C2800 | W400 S4000 C5600 | W800 S8000 C11200 | W1600 S16000 C22400 | W3200 S32000 C44800 | ×2 for each already built |
| sco | `scoart` | Artillery Depot | 200 | W100 S1000 C1400 | W200 S2000 C2800 | W400 S4000 C5600 | W800 S8000 C11200 | W1600 S16000 C22400 | W3200 S32000 C44800 | ×2 for each already built |
| spa | `spaart` | Artillery Depot | 200 | W100 S1000 C1400 | W200 S2000 C2800 | W400 S4000 C5600 | W800 S8000 C11200 | W1600 S16000 C22400 | W3200 S32000 C44800 | ×2 for each already built |
| swe | `sweart` | Artillery Depot | 200 | W100 S1000 C1400 | W200 S2000 C2800 | W400 S4000 C5600 | W800 S8000 C11200 | W1600 S16000 C22400 | W3200 S32000 C44800 | ×2 for each already built |
| swi | `swiart` | Artillery Depot | 200 | W100 S1000 C1400 | W200 S2000 C2800 | W400 S4000 C5600 | W800 S8000 C11200 | W1600 S16000 C22400 | W3200 S32000 C44800 | ×2 for each already built |
| tur | `turart` | Artillery Depot | 200 | W500 S1200 C1400 | W1000 S2400 C2800 | W2000 S4800 C5600 | W4000 S9600 C11200 | W8000 S19200 C22400 | W16000 S38400 C44800 | ×2 for each already built |
| ukr | `ukrart` | Artillery Depot | 200 | W4250 S4400 G100 C1400 | W8500 S8800 G200 C2800 | W17000 S17600 G400 C5600 | W34000 S35200 G800 C11200 | W68000 S70400 G1600 C22400 | W136000 S140800 G3200 C44800 | ×2 for each already built |
| ven | `venart` | Artillery Depot | 200 | W100 S1000 C1400 | W200 S2000 C2800 | W400 S4000 C5600 | W800 S8000 C11200 | W1600 S16000 C22400 | W3200 S32000 C44800 | ×2 for each already built |

<a id="110-dip--дипломатический-центр"></a>
### 1.10 `dip` — Diplomatic Center

| Nation | sid | Name | cost% | N=1 | N=2 | N=3 | N=4 | N=5 | N=6 | Note |
| --- | --- | --- | ---: | --- | --- | --- | --- | --- | --- | --- |
| alg | `algdip` | Diplomatic Center | 100 | W4600 S2020 | W4600 S2020 | W4600 S2020 | W4600 S2020 | W4600 S2020 | W4600 S2020 | not scalable (`costpercent` = 0/100) |
| aus | `ausdip` | Diplomatic Center | 100 | W4900 S1700 | W4900 S1700 | W4900 S1700 | W4900 S1700 | W4900 S1700 | W4900 S1700 | not scalable (`costpercent` = 0/100) |
| bav | `bavdip` | Diplomatic Center | 100 | W4900 S1700 | W4900 S1700 | W4900 S1700 | W4900 S1700 | W4900 S1700 | W4900 S1700 | not scalable (`costpercent` = 0/100) |
| den | `dendip` | Diplomatic Center | 100 | W4900 S1700 | W4900 S1700 | W4900 S1700 | W4900 S1700 | W4900 S1700 | W4900 S1700 | not scalable (`costpercent` = 0/100) |
| eng | `engdip` | Diplomatic Center | 100 | W4900 S1700 | W4900 S1700 | W4900 S1700 | W4900 S1700 | W4900 S1700 | W4900 S1700 | not scalable (`costpercent` = 0/100) |
| fra | `fradip` | Diplomatic Center | 100 | W4900 S1700 | W4900 S1700 | W4900 S1700 | W4900 S1700 | W4900 S1700 | W4900 S1700 | not scalable (`costpercent` = 0/100) |
| hun | `hundip` | Diplomatic Center | 100 | W4900 S1700 | W4900 S1700 | W4900 S1700 | W4900 S1700 | W4900 S1700 | W4900 S1700 | not scalable (`costpercent` = 0/100) |
| net | `netdip` | Diplomatic Center | 100 | W4900 S1700 | W4900 S1700 | W4900 S1700 | W4900 S1700 | W4900 S1700 | W4900 S1700 | not scalable (`costpercent` = 0/100) |
| pie | `piedip` | Diplomatic Center | 100 | W4900 S1700 | W4900 S1700 | W4900 S1700 | W4900 S1700 | W4900 S1700 | W4900 S1700 | not scalable (`costpercent` = 0/100) |
| pol | `poldip` | Diplomatic Center | 100 | W4900 S1700 | W4900 S1700 | W4900 S1700 | W4900 S1700 | W4900 S1700 | W4900 S1700 | not scalable (`costpercent` = 0/100) |
| por | `pordip` | Diplomatic Center | 100 | W4900 S1700 | W4900 S1700 | W4900 S1700 | W4900 S1700 | W4900 S1700 | W4900 S1700 | not scalable (`costpercent` = 0/100) |
| pru | `prudip` | Diplomatic Center | 100 | W4900 S1700 | W4900 S1700 | W4900 S1700 | W4900 S1700 | W4900 S1700 | W4900 S1700 | not scalable (`costpercent` = 0/100) |
| rus | `rusdip` | Diplomatic Center | 100 | W7900 S3700 | W7900 S3700 | W7900 S3700 | W7900 S3700 | W7900 S3700 | W7900 S3700 | not scalable (`costpercent` = 0/100) |
| sax | `saxdip` | Diplomatic Center | 100 | W4900 S1700 | W4900 S1700 | W4900 S1700 | W4900 S1700 | W4900 S1700 | W4900 S1700 | not scalable (`costpercent` = 0/100) |
| sco | `scodip` | Diplomatic Center | 100 | W4900 S1700 | W4900 S1700 | W4900 S1700 | W4900 S1700 | W4900 S1700 | W4900 S1700 | not scalable (`costpercent` = 0/100) |
| spa | `spadip` | Diplomatic Center | 100 | W4900 S1700 | W4900 S1700 | W4900 S1700 | W4900 S1700 | W4900 S1700 | W4900 S1700 | not scalable (`costpercent` = 0/100) |
| swe | `swedip` | Diplomatic Center | 100 | W4900 S1700 | W4900 S1700 | W4900 S1700 | W4900 S1700 | W4900 S1700 | W4900 S1700 | not scalable (`costpercent` = 0/100) |
| swi | `swidip` | Diplomatic Center | 100 | W4900 S1700 | W4900 S1700 | W4900 S1700 | W4900 S1700 | W4900 S1700 | W4900 S1700 | not scalable (`costpercent` = 0/100) |
| tur | `turdip` | Diplomatic Center | 100 | W4600 S2020 | W4600 S2020 | W4600 S2020 | W4600 S2020 | W4600 S2020 | W4600 S2020 | not scalable (`costpercent` = 0/100) |
| ukr | `ukrdip` | Diplomatic Center | 100 | W3900 S2700 | W3900 S2700 | W3900 S2700 | W3900 S2700 | W3900 S2700 | W3900 S2700 | not scalable (`costpercent` = 0/100) |
| ven | `vendip` | Diplomatic Center | 100 | W4900 S1700 | W4900 S1700 | W4900 S1700 | W4900 S1700 | W4900 S1700 | W4900 S1700 | not scalable (`costpercent` = 0/100) |

<a id="2-общие-постройки-по-кластерам"></a>
## 2. Common buildings (by clusters)

sid is formed as `<cluster><suffix>` - common for a group of nations. One sid is usually used by several nations - they are listed in the column.

<a id="21-mil--мельница"></a>
### 2.1 `mil` — Mill

| sid | Use nations | Name | cost% | N=1 | N=2 | N=3 | N=4 | N=5 | N=6 | Note |
| --- | --- | --- | ---: | --- | --- | --- | --- | --- | --- | --- |
| `eurmil` | aus, bav, den, eng, fra, hun, net, pie, pol, por, pru, sax, sco, spa, swe, swi, ven | Mill | 200 | W30 S150 | W60 S300 | W120 S600 | W240 S1200 | W480 S2400 | W960 S4800 | ×2 for each already built |
| `rusmil` | rus, ukr | Mill | 200 | W210 | W420 | W840 | W1680 | W3360 | W6720 | ×2 for each already built |
| `turmil` | alg, tur | Mill | 200 | W30 S150 | W60 S300 | W120 S600 | W240 S1200 | W480 S2400 | W960 S4800 | ×2 for each already built |

<a id="22-sto--склад"></a>
### 2.2 `sto` — Storehouse

| sid | Use nations | Name | cost% | N=1 | N=2 | N=3 | N=4 | N=5 | N=6 | Note |
| --- | --- | --- | ---: | --- | --- | --- | --- | --- | --- | --- |
| `eursto` | aus, bav, den, eng, fra, hun, net, pie, pru, sax, sco, swe, swi, ven | Storehouse | 150 | W50 S20 | W75 S30 | W112 S45 | W168 S67 | W253 S101 | W379 S151 | ×1.5 for each already built |
| `russto` | pol, rus, ukr | Storehouse | 200 | W50 S20 | W100 S40 | W200 S80 | W400 S160 | W800 S320 | W1600 S640 | ×2 for each already built |
| `spasto` | por, spa | Storehouse | 150 | W20 S20 | W30 S30 | W45 S45 | W67 S67 | W101 S101 | W151 S151 | ×1.5 for each already built |
| `tursto` | alg, tur | Storehouse | 200 | W30 S10 | W60 S20 | W120 S40 | W240 S80 | W480 S160 | W960 S320 | ×2 for each already built |

<a id="23-mar--рынок"></a>
### 2.3 `mar` — Market

| sid | Use nations | Name | cost% | N=1 | N=2 | N=3 | N=4 | N=5 | N=6 | Note |
| --- | --- | --- | ---: | --- | --- | --- | --- | --- | --- | --- |
| `eurmar` | aus, bav, den, eng, fra, hun, net, pie, pol, pru, sax, sco, swe, swi, ven | Market | 2000 | W450 | W9000 | W180000 | W3600000 | W9000000 | W9000000 | ×20 for each already built |
| `rusmar` | rus, ukr | Market | 2000 | W450 | W9000 | W180000 | W3600000 | W9000000 | W9000000 | ×20 for each already built |
| `spamar` | por, spa | Market | 2000 | W450 | W9000 | W180000 | W3600000 | W9000000 | W9000000 | ×20 for each already built |
| `turmar` | alg, tur | Bazaar | 1500 | W450 S150 | W6750 S2250 | W101250 S33750 | W1518750 S506250 | W9000000 S3000000 | W9000000 S3000000 | ×15 for each already built |

### 2.4 `por` — Shipyard

| sid | Use nations | Name | cost% | N=1 | N=2 | N=3 | N=4 | N=5 | N=6 | Note |
| --- | --- | --- | ---: | --- | --- | --- | --- | --- | --- | --- |
| `eurpor` | aus, bav, den, eng, fra, hun, net, pie, pol, pru, sax, sco, spa, swe, swi, ven | Shipyard | 150 | W1600 S800 I400 | W2400 S1200 I600 | W3600 S1800 I900 | W5400 S2700 I1350 | W8100 S4050 I2025 | W12150 S6075 I3037 | ×1.5 for each already built |
| `porpor` | por | Shipyard | 150 | W1600 S800 I400 | W2400 S1200 I600 | W3600 S1800 I900 | W5400 S2700 I1350 | W8100 S4050 I2025 | W12150 S6075 I3037 | ×1.5 for each already built |
| `ruspor` | rus | Shipyard | 150 | W1200 S800 I400 | W1800 S1200 I600 | W2700 S1800 I900 | W4050 S2700 I1350 | W6075 S4050 I2025 | W9112 S6075 I3037 | ×1.5 for each already built |
| `turpor` | alg, tur | Shipyard | 150 | W800 S800 I400 | W1200 S1200 I600 | W1800 S1800 I900 | W2700 S2700 I1350 | W4050 S4050 I2025 | W6075 S6075 I3037 | ×1.5 for each already built |
| `ukrpor` | ukr | Shipyard | 150 | W2000 | W3000 | W4500 | W6750 | W10125 | W15187 | ×1.5 for each already built |

### 2.5 `tow` — Tower

| sid | Use nations | Name | cost% | N=1 | N=2 | N=3 | N=4 | N=5 | N=6 | Note |
| --- | --- | --- | ---: | --- | --- | --- | --- | --- | --- | --- |
| `eurtow` | aus, bav, den, eng, fra, hun, net, pie, pol, por, pru, sax, sco, spa, swe, swi, ven | Tower | 120 | W100 S100 G150 | W120 S120 G180 | W144 S144 G216 | W172 S172 G259 | W207 S207 G311 | W248 S248 G373 | ×1.2 for each already built |
| `rustow` | rus | Tower | 125 | W100 S100 G150 | W125 S125 G187 | W156 S156 G234 | W195 S195 G292 | W244 S244 G366 | W305 S305 G457 | ×1.25 for each already built |
| `turtow` | alg, tur | Tower | 125 | W150 S90 G100 | W187 S112 G125 | W234 S140 G156 | W292 S175 G195 | W366 S219 G244 | W457 S274 G305 | ×1.25 for each already built |

### 2.6 `gol` - Gold Mine

| sid | Use nations | Name | cost% | N=1 | N=2 | N=3 | N=4 | N=5 | N=6 | Note |
| --- | --- | --- | ---: | --- | --- | --- | --- | --- | --- | --- |
| `eurgol` | alg, aus, bav, den, eng, fra, hun, net, pie, pol, por, pru, rus, sax, sco, spa, swe, swi, tur, ukr, ven | Mine | 0 | W100 S100 | W100 S100 | W100 S100 | W100 S100 | W100 S100 | W100 S100 | not scalable (`costpercent` = 0/100) |

### 2.7 `iro` - Iron Mine

| sid | Use nations | Name | cost% | N=1 | N=2 | N=3 | N=4 | N=5 | N=6 | Note |
| --- | --- | --- | ---: | --- | --- | --- | --- | --- | --- | --- |
| `euriro` | alg, aus, bav, den, eng, fra, hun, net, pie, pol, por, pru, rus, sax, sco, spa, swe, swi, tur, ukr, ven | Mine | 0 | W100 S100 | W100 S100 | W100 S100 | W100 S100 | W100 S100 | W100 S100 | not scalable (`costpercent` = 0/100) |

### 2.8 `coa` - Coal mine

| sid | Use nations | Name | cost% | N=1 | N=2 | N=3 | N=4 | N=5 | N=6 | Note |
| --- | --- | --- | ---: | --- | --- | --- | --- | --- | --- | --- |
| `eurcoa` | alg, aus, bav, den, eng, fra, hun, net, pie, pol, por, pru, rus, sax, sco, spa, swe, swi, tur, ukr, ven | Mine | 0 | W100 S100 | W100 S100 | W100 S100 | W100 S100 | W100 S100 | W100 S100 | not scalable (`costpercent` = 0/100) |

### 2.9 `swa` - Stone wall
| sid | Use nations | Name | cost% | N=1 | N=2 | N=3 | N=4 | N=5 | N=6 | Note |
| --- | --- | --- | ---: | --- | --- | --- | --- | --- | --- | --- |
| `eurswa` | aus, bav, den, eng, fra, hun, net, pie, pol, por, pru, sax, sco, spa, swe, swi, ven | Wall | 0 | S50 | S50 | S50 | S50 | S50 | S50 | not scalable (`costpercent` = 0/100) |
| `russwa` | rus | Wall | 0 | S60 | S60 | S60 | S60 | S60 | S60 | not scalable (`costpercent` = 0/100) |
| `turswa` | alg, tur | Wall | 0 | S60 | S60 | S60 | S60 | S60 | S60 | not scalable (`costpercent` = 0/100) |

### 2.10 `sga` — Gate

| sid | Use nations | Name | cost% | N=1 | N=2 | N=3 | N=4 | N=5 | N=6 | Note |
| --- | --- | --- | ---: | --- | --- | --- | --- | --- | --- | --- |
| `eursga` | aus, bav, den, eng, fra, hun, net, pie, pol, por, pru, sax, sco, spa, swe, swi, ven | Gate | 0 | S50 | S50 | S50 | S50 | S50 | S50 | not scalable (`costpercent` = 0/100) |
| `russga` | rus | Gate | 0 | S60 | S60 | S60 | S60 | S60 | S60 | not scalable (`costpercent` = 0/100) |
| `tursga` | alg, tur | Gate | 0 | S60 | S60 | S60 | S60 | S60 | S60 | not scalable (`costpercent` = 0/100) |

### 2.11 `wga` — Gate

| sid | Use nations | Name | cost% | N=1 | N=2 | N=3 | N=4 | N=5 | N=6 | Note |
| --- | --- | --- | ---: | --- | --- | --- | --- | --- | --- | --- |
| `ukrwga` | alg, aus, bav, den, eng, fra, hun, net, pie, pol, por, pru, rus, sax, sco, spa, swe, swi, tur, ukr, ven | Gate | 0 | W10 | W10 | W10 | W10 | W10 | W10 | not scalable (`costpercent` = 0/100) |

### 2.12 `wwa` - Palisade

| sid | Use nations | Name | cost% | N=1 | N=2 | N=3 | N=4 | N=5 | N=6 | Note |
| --- | --- | --- | ---: | --- | --- | --- | --- | --- | --- | --- |
| `ukrwwa` | alg, aus, bav, den, eng, fra, hun, net, pie, pol, por, pru, rus, sax, sco, spa, swe, swi, tur, ukr, ven | Palisade | 0 | W10 | W10 | W10 | W10 | W10 | W10 | not scalable (`costpercent` = 0/100) |


## Sources

All links are relative to `data/scripts/` in the Cossacks 3 installation.

[^1]: `_unit_GetCostByID` - calculation of the price of the Nth copy - `lib/unit.script:5650-5689`.

[^2]: `counter.all[cid][unitID]` increment when creating - `lib/unit.script:3847`.

[^3]: `counter.all[cid][unitID]` decrement upon destruction - `lib/unit.script:3969`.

---

Generated from `data.json`. For regeneration:
```
python compute/compute_scaling.py
```