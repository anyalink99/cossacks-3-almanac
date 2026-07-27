<a id="cossacks-3--цены-зданий-по-n-му-экземпляру"></a>
<a id="цена-каждого-следующего-здания"></a>
# Cost of Each Additional Building

[← Tables and calculations](../README.md)

<a id="формула"></a>
## Formula

The game calculates the price in `_unit_GetCostByID` [^1]:

```text
costmodifier   = pow(costpercent / 100, count)         // count = already owned
final_price[r] = floor(base_price[r] * costmodifier)   // calculated separately for F/W/S/G/I/C
```

The counter rises when a building is created [^2] and falls when one is
destroyed [^3]. Demolishing a Town Hall can therefore make the next Town
Hall cheaper again.

<a id="особые-случаи"></a>
## Special cases

- A scaling value of 0% or 100% means that the price remains constant.
- Mercenary prices use a related counter and are capped at twice the base
  price. They are not included in these building tables.
- Other prices are capped at 20,000 times their base value. None of the
  first six buildings reaches that cap.
- Every resource is rounded down separately, so small percentage increases
  produce visible steps rather than a perfectly smooth curve.

<a id="колонки-n16"></a>
<a id="как-читать-таблицы"></a>
## How to Read the Tables

`N=1` is the first building at its base price, `N=2` is the second, and so
on. Costs use the abbreviations F (food), W (wood), S (stone), G (gold),
I (iron), and C (coal). Resources with a zero cost are omitted.

<a id="1-постройки-по-нациям"></a>
<a id="национальные-варианты-зданий"></a>
## 1. Buildings by nation

National building identifiers combine a nation prefix with a building
suffix. The tables group all national versions of each building type.

<a id="11-cen--городской-центр"></a>
<a id="городской-центр-cen"></a>
### 1.1 Town Hall (`cen`)

| Nation | Building ID | Building | Price growth, % | 1st | 2nd | 3rd | 4th | 5th | 6th | Rule |
| --- | --- | --- | ---: | --- | --- | --- | --- | --- | --- | --- |
| Algeria | `algcen` | Town Hall | 300 | W450 S700 | W1350 S2100 | W4050 S6300 | W12150 S18900 | W36450 S56700 | W109350 S170100 | ×3 for each already built |
| Austria | `auscen` | Town Hall | 300 | W700 S700 | W2100 S2100 | W6300 S6300 | W18900 S18900 | W56700 S56700 | W170100 S170100 | ×3 for each already built |
| Bavaria | `bavcen` | Town Hall | 300 | W700 S700 | W2100 S2100 | W6300 S6300 | W18900 S18900 | W56700 S56700 | W170100 S170100 | ×3 for each already built |
| Denmark | `dencen` | Town Hall | 300 | W700 S700 | W2100 S2100 | W6300 S6300 | W18900 S18900 | W56700 S56700 | W170100 S170100 | ×3 for each already built |
| England | `engcen` | Town Hall | 300 | W700 S700 | W2100 S2100 | W6300 S6300 | W18900 S18900 | W56700 S56700 | W170100 S170100 | ×3 for each already built |
| France | `fracen` | Town Hall | 300 | W700 S700 | W2100 S2100 | W6300 S6300 | W18900 S18900 | W56700 S56700 | W170100 S170100 | ×3 for each already built |
| Hungary | `huncen` | Town Hall | 300 | W700 S700 | W2100 S2100 | W6300 S6300 | W18900 S18900 | W56700 S56700 | W170100 S170100 | ×3 for each already built |
| Netherlands | `netcen` | Town Hall | 300 | W700 S700 | W2100 S2100 | W6300 S6300 | W18900 S18900 | W56700 S56700 | W170100 S170100 | ×3 for each already built |
| Piedmont | `piecen` | Town Hall | 300 | W700 S700 | W2100 S2100 | W6300 S6300 | W18900 S18900 | W56700 S56700 | W170100 S170100 | ×3 for each already built |
| Poland | `polcen` | Town Hall | 300 | W700 S700 | W2100 S2100 | W6300 S6300 | W18900 S18900 | W56700 S56700 | W170100 S170100 | ×3 for each already built |
| Portugal | `porcen` | Town Hall | 300 | W700 S700 | W2100 S2100 | W6300 S6300 | W18900 S18900 | W56700 S56700 | W170100 S170100 | ×3 for each already built |
| Prussia | `prucen` | Town Hall | 300 | W700 S700 | W2100 S2100 | W6300 S6300 | W18900 S18900 | W56700 S56700 | W170100 S170100 | ×3 for each already built |
| Russia | `ruscen` | Town Hall | 300 | W680 S700 | W2040 S2100 | W6120 S6300 | W18360 S18900 | W55080 S56700 | W165240 S170100 | ×3 for each already built |
| Saxony | `saxcen` | Town Hall | 300 | W700 S700 | W2100 S2100 | W6300 S6300 | W18900 S18900 | W56700 S56700 | W170100 S170100 | ×3 for each already built |
| Scotland | `scocen` | Town Hall | 300 | W700 S700 | W2100 S2100 | W6300 S6300 | W18900 S18900 | W56700 S56700 | W170100 S170100 | ×3 for each already built |
| Spain | `spacen` | Town Hall | 300 | W700 S700 | W2100 S2100 | W6300 S6300 | W18900 S18900 | W56700 S56700 | W170100 S170100 | ×3 for each already built |
| Sweden | `swecen` | Town Hall | 300 | W700 S700 | W2100 S2100 | W6300 S6300 | W18900 S18900 | W56700 S56700 | W170100 S170100 | ×3 for each already built |
| Switzerland | `swicen` | Town Hall | 300 | W700 S700 | W2100 S2100 | W6300 S6300 | W18900 S18900 | W56700 S56700 | W170100 S170100 | ×3 for each already built |
| Turkey | `turcen` | Town Hall | 300 | W600 S500 | W1800 S1500 | W5400 S4500 | W16200 S13500 | W48600 S40500 | W145800 S121500 | ×3 for each already built |
| Ukraine | `ukrcen` | Town Hall | 400 | W700 | W2800 | W11200 | W44800 | W179200 | W716800 | ×4 for each already built |
| Venice | `vencen` | Town Hall | 300 | W700 S700 | W2100 S2100 | W6300 S6300 | W18900 S18900 | W56700 S56700 | W170100 S170100 | ×3 for each already built |

<a id="12-hou--дом"></a>
<a id="дом-hou"></a>
### 1.2 Housing (`hou`)

| Nation | Building ID | Building | Price growth, % | 1st | 2nd | 3rd | 4th | 5th | 6th | Rule |
| --- | --- | --- | ---: | --- | --- | --- | --- | --- | --- | --- |
| Algeria | `alghou` | Housing | 104 | W100 S100 | W104 S104 | W108 S108 | W112 S112 | W116 S116 | W121 S121 | ×1.04 for each already built |
| Austria | `aushou` | Housing | 104 | W100 S100 | W104 S104 | W108 S108 | W112 S112 | W116 S116 | W121 S121 | ×1.04 for each already built |
| Bavaria | `bavhou` | Housing | 104 | W100 S100 | W104 S104 | W108 S108 | W112 S112 | W116 S116 | W121 S121 | ×1.04 for each already built |
| Denmark | `denhou` | Housing | 104 | W100 S100 | W104 S104 | W108 S108 | W112 S112 | W116 S116 | W121 S121 | ×1.04 for each already built |
| England | `enghou` | Housing | 104 | W100 S100 | W104 S104 | W108 S108 | W112 S112 | W116 S116 | W121 S121 | ×1.04 for each already built |
| France | `frahou` | Housing | 104 | W100 S100 | W104 S104 | W108 S108 | W112 S112 | W116 S116 | W121 S121 | ×1.04 for each already built |
| Hungary | `hunhou` | Housing | 104 | W100 S100 | W104 S104 | W108 S108 | W112 S112 | W116 S116 | W121 S121 | ×1.04 for each already built |
| Netherlands | `nethou` | Housing | 104 | W100 S100 | W104 S104 | W108 S108 | W112 S112 | W116 S116 | W121 S121 | ×1.04 for each already built |
| Piedmont | `piehou` | Housing | 104 | W100 S100 | W104 S104 | W108 S108 | W112 S112 | W116 S116 | W121 S121 | ×1.04 for each already built |
| Poland | `polhou` | Housing | 104 | W100 S100 | W104 S104 | W108 S108 | W112 S112 | W116 S116 | W121 S121 | ×1.04 for each already built |
| Portugal | `porhou` | Housing | 104 | W100 S100 | W104 S104 | W108 S108 | W112 S112 | W116 S116 | W121 S121 | ×1.04 for each already built |
| Prussia | `pruhou` | Housing | 104 | W100 S100 | W104 S104 | W108 S108 | W112 S112 | W116 S116 | W121 S121 | ×1.04 for each already built |
| Russia | `rushou` | Izba | 104 | W120 | W124 | W129 | W134 | W140 | W145 | ×1.04 for each already built |
| Saxony | `saxhou` | Housing | 104 | W100 S100 | W104 S104 | W108 S108 | W112 S112 | W116 S116 | W121 S121 | ×1.04 for each already built |
| Scotland | `scohou` | Housing | 104 | W100 S100 | W104 S104 | W108 S108 | W112 S112 | W116 S116 | W121 S121 | ×1.04 for each already built |
| Spain | `spahou` | Housing | 104 | W100 S100 | W104 S104 | W108 S108 | W112 S112 | W116 S116 | W121 S121 | ×1.04 for each already built |
| Sweden | `swehou` | Housing | 104 | W100 S100 | W104 S104 | W108 S108 | W112 S112 | W116 S116 | W121 S121 | ×1.04 for each already built |
| Switzerland | `swihou` | Housing | 104 | W100 S100 | W104 S104 | W108 S108 | W112 S112 | W116 S116 | W121 S121 | ×1.04 for each already built |
| Turkey | `turhou` | Housing | 106 | W100 S100 | W106 S106 | W112 S112 | W119 S119 | W126 S126 | W133 S133 | ×1.06 for each already built |
| Ukraine | `ukrhou` | Hut | 105 | W120 | W126 | W132 | W138 | W145 | W153 | ×1.05 for each already built |
| Venice | `venhou` | Housing | 104 | W100 S100 | W104 S104 | W108 S108 | W112 S112 | W116 S116 | W121 S121 | ×1.04 for each already built |

<a id="13-bar--казарма-17-в"></a>
<a id="казарма-17-в-bar"></a>
### 1.3 Barracks, 17th century (`bar`)

| Nation | Building ID | Building | Price growth, % | 1st | 2nd | 3rd | 4th | 5th | 6th | Rule |
| --- | --- | --- | ---: | --- | --- | --- | --- | --- | --- | --- |
| Algeria | `algbar` | Barracks | 500 | W400 S400 | W2000 S2000 | W10000 S10000 | W50000 S50000 | W250000 S250000 | W1250000 S1250000 | ×5 for each already built |
| Austria | `ausbar` | Barracks, 17th century | 500 | W100 S100 G500 | W500 S500 G2500 | W2500 S2500 G12500 | W12500 S12500 G62500 | W62500 S62500 G312500 | W312500 S312500 G1562500 | ×5 for each already built |
| Bavaria | `bavbar` | Barracks, 17th century | 500 | W100 S100 G500 | W500 S500 G2500 | W2500 S2500 G12500 | W12500 S12500 G62500 | W62500 S62500 G312500 | W312500 S312500 G1562500 | ×5 for each already built |
| Denmark | `denbar` | Barracks, 17th century | 500 | W100 S100 G500 | W500 S500 G2500 | W2500 S2500 G12500 | W12500 S12500 G62500 | W62500 S62500 G312500 | W312500 S312500 G1562500 | ×5 for each already built |
| England | `engbar` | Barracks, 17th century | 500 | W100 S100 G500 | W500 S500 G2500 | W2500 S2500 G12500 | W12500 S12500 G62500 | W62500 S62500 G312500 | W312500 S312500 G1562500 | ×5 for each already built |
| France | `frabar` | Barracks, 17th century | 500 | W100 S100 G500 | W500 S500 G2500 | W2500 S2500 G12500 | W12500 S12500 G62500 | W62500 S62500 G312500 | W312500 S312500 G1562500 | ×5 for each already built |
| Hungary | `hunbar` | Barracks, 17th century | 500 | W100 S100 G500 | W500 S500 G2500 | W2500 S2500 G12500 | W12500 S12500 G62500 | W62500 S62500 G312500 | W312500 S312500 G1562500 | ×5 for each already built |
| Netherlands | `netbar` | Barracks, 17th century | 500 | W100 S100 G500 | W500 S500 G2500 | W2500 S2500 G12500 | W12500 S12500 G62500 | W62500 S62500 G312500 | W312500 S312500 G1562500 | ×5 for each already built |
| Piedmont | `piebar` | Barracks, 17th century | 500 | W100 S100 G500 | W500 S500 G2500 | W2500 S2500 G12500 | W12500 S12500 G62500 | W62500 S62500 G312500 | W312500 S312500 G1562500 | ×5 for each already built |
| Poland | `polbar` | Barracks, 17th century | 500 | W100 S100 G500 | W500 S500 G2500 | W2500 S2500 G12500 | W12500 S12500 G62500 | W62500 S62500 G312500 | W312500 S312500 G1562500 | ×5 for each already built |
| Portugal | `porbar` | Barracks, 17th century | 500 | W100 S100 G500 | W500 S500 G2500 | W2500 S2500 G12500 | W12500 S12500 G62500 | W62500 S62500 G312500 | W312500 S312500 G1562500 | ×5 for each already built |
| Prussia | `prubar` | Barracks, 17th century | 500 | W100 S100 G500 | W500 S500 G2500 | W2500 S2500 G12500 | W12500 S12500 G62500 | W62500 S62500 G312500 | W312500 S312500 G1562500 | ×5 for each already built |
| Russia | `rusbar` | Strelets Barracks | 300 | W200 S20 | W600 S60 | W1800 S180 | W5400 S540 | W16200 S1620 | W48600 S4860 | ×3 for each already built |
| Saxony | `saxbar` | Barracks, 17th century | 500 | W100 S100 G500 | W500 S500 G2500 | W2500 S2500 G12500 | W12500 S12500 G62500 | W62500 S62500 G312500 | W312500 S312500 G1562500 | ×5 for each already built |
| Scotland | `scobar` | Barracks, 17th century | 500 | W100 S100 G500 | W500 S500 G2500 | W2500 S2500 G12500 | W12500 S12500 G62500 | W62500 S62500 G312500 | W312500 S312500 G1562500 | ×5 for each already built |
| Spain | `spabar` | Barracks, 17th century | 500 | W100 S100 G500 | W500 S500 G2500 | W2500 S2500 G12500 | W12500 S12500 G62500 | W62500 S62500 G312500 | W312500 S312500 G1562500 | ×5 for each already built |
| Sweden | `swebar` | Barracks, 17th century | 500 | W100 S100 G500 | W500 S500 G2500 | W2500 S2500 G12500 | W12500 S12500 G62500 | W62500 S62500 G312500 | W312500 S312500 G1562500 | ×5 for each already built |
| Switzerland | `swibar` | Barracks, 17th century | 500 | W100 S100 G500 | W500 S500 G2500 | W2500 S2500 G12500 | W12500 S12500 G62500 | W62500 S62500 G312500 | W312500 S312500 G1562500 | ×5 for each already built |
| Turkey | `turbar` | Barracks | 500 | W400 S400 | W2000 S2000 | W10000 S10000 | W50000 S50000 | W250000 S250000 | W1250000 S1250000 | ×5 for each already built |
| Ukraine | `ukrbar` | Cossack House | 300 | W150 S150 | W450 S450 | W1350 S1350 | W4050 S4050 | W12150 S12150 | W36450 S36450 | ×3 for each already built |
| Venice | `venbar` | Barracks, 17th century | 500 | W100 S100 G500 | W500 S500 G2500 | W2500 S2500 G12500 | W12500 S12500 G62500 | W62500 S62500 G312500 | W312500 S312500 G1562500 | ×5 for each already built |

<a id="14-ba2--казарма-18-в"></a>
<a id="казарма-18-в-ba2"></a>
### 1.4 Barracks, 18th century (`ba2`)

| Nation | Building ID | Building | Price growth, % | 1st | 2nd | 3rd | 4th | 5th | 6th | Rule |
| --- | --- | --- | ---: | --- | --- | --- | --- | --- | --- | --- |
| Austria | `ausba2` | Barracks, 18th century | 200 | W1700 S2950 G4000 | W3400 S5900 G8000 | W6800 S11800 G16000 | W13600 S23600 G32000 | W27200 S47200 G64000 | W54400 S94400 G128000 | ×2 for each already built |
| Bavaria | `bavba2` | Barracks, 18th century | 200 | W1700 S2950 G4000 | W3400 S5900 G8000 | W6800 S11800 G16000 | W13600 S23600 G32000 | W27200 S47200 G64000 | W54400 S94400 G128000 | ×2 for each already built |
| Denmark | `denba2` | Barracks, 18th century | 200 | W1700 S2950 G4000 | W3400 S5900 G8000 | W6800 S11800 G16000 | W13600 S23600 G32000 | W27200 S47200 G64000 | W54400 S94400 G128000 | ×2 for each already built |
| England | `engba2` | Barracks, 18th century | 200 | W1700 S2950 G4000 | W3400 S5900 G8000 | W6800 S11800 G16000 | W13600 S23600 G32000 | W27200 S47200 G64000 | W54400 S94400 G128000 | ×2 for each already built |
| France | `fraba2` | Barracks, 18th century | 200 | W1700 S2950 G4000 | W3400 S5900 G8000 | W6800 S11800 G16000 | W13600 S23600 G32000 | W27200 S47200 G64000 | W54400 S94400 G128000 | ×2 for each already built |
| Hungary | `hunba2` | Barracks, 18th century | 200 | W1700 S2950 G4000 | W3400 S5900 G8000 | W6800 S11800 G16000 | W13600 S23600 G32000 | W27200 S47200 G64000 | W54400 S94400 G128000 | ×2 for each already built |
| Netherlands | `netba2` | Barracks, 18th century | 200 | W1700 S2950 G4000 | W3400 S5900 G8000 | W6800 S11800 G16000 | W13600 S23600 G32000 | W27200 S47200 G64000 | W54400 S94400 G128000 | ×2 for each already built |
| Piedmont | `pieba2` | Barracks, 18th century | 200 | W1700 S2950 G4000 | W3400 S5900 G8000 | W6800 S11800 G16000 | W13600 S23600 G32000 | W27200 S47200 G64000 | W54400 S94400 G128000 | ×2 for each already built |
| Poland | `polba2` | Barracks, 18th century | 200 | W1700 S2950 G4000 | W3400 S5900 G8000 | W6800 S11800 G16000 | W13600 S23600 G32000 | W27200 S47200 G64000 | W54400 S94400 G128000 | ×2 for each already built |
| Portugal | `porba2` | Barracks, 18th century | 200 | W1700 S2950 G4000 | W3400 S5900 G8000 | W6800 S11800 G16000 | W13600 S23600 G32000 | W27200 S47200 G64000 | W54400 S94400 G128000 | ×2 for each already built |
| Prussia | `pruba2` | Barracks, 18th century | 200 | W1700 S2950 G4000 | W3400 S5900 G8000 | W6800 S11800 G16000 | W13600 S23600 G32000 | W27200 S47200 G64000 | W54400 S94400 G128000 | ×2 for each already built |
| Russia | `rusba2` | Barracks, 18th century | 200 | W1700 S2950 G4000 | W3400 S5900 G8000 | W6800 S11800 G16000 | W13600 S23600 G32000 | W27200 S47200 G64000 | W54400 S94400 G128000 | ×2 for each already built |
| Saxony | `saxba2` | Barracks, 18th century | 200 | W1700 S2950 G4000 | W3400 S5900 G8000 | W6800 S11800 G16000 | W13600 S23600 G32000 | W27200 S47200 G64000 | W54400 S94400 G128000 | ×2 for each already built |
| Scotland | `scoba2` | Castle | 250 | W640 S2400 G2400 | W1600 S6000 G6000 | W4000 S15000 G15000 | W10000 S37500 G37500 | W25000 S93750 G93750 | W62500 S234375 G234375 | ×2.5 for each already built |
| Spain | `spaba2` | Barracks, 18th century | 200 | W1700 S2950 G4000 | W3400 S5900 G8000 | W6800 S11800 G16000 | W13600 S23600 G32000 | W27200 S47200 G64000 | W54400 S94400 G128000 | ×2 for each already built |
| Sweden | `sweba2` | Barracks, 18th century | 200 | W1700 S2950 G4000 | W3400 S5900 G8000 | W6800 S11800 G16000 | W13600 S23600 G32000 | W27200 S47200 G64000 | W54400 S94400 G128000 | ×2 for each already built |
| Switzerland | `swiba2` | Barracks, 18th century | 200 | W1700 S2950 G4000 | W3400 S5900 G8000 | W6800 S11800 G16000 | W13600 S23600 G32000 | W27200 S47200 G64000 | W54400 S94400 G128000 | ×2 for each already built |
| Venice | `venba2` | Barracks, 18th century | 200 | W1700 S2950 G4000 | W3400 S5900 G8000 | W6800 S11800 G16000 | W13600 S23600 G32000 | W27200 S47200 G64000 | W54400 S94400 G128000 | ×2 for each already built |

<a id="15-bla--кузница"></a>
<a id="кузница-bla"></a>
### 1.5 Blacksmith (`bla`)

| Nation | Building ID | Building | Price growth, % | 1st | 2nd | 3rd | 4th | 5th | 6th | Rule |
| --- | --- | --- | ---: | --- | --- | --- | --- | --- | --- | --- |
| Algeria | `algbla` | Blacksmith | 400 | W100 S30 I640 | W400 S120 I2560 | W1600 S480 I10240 | W6400 S1920 I40960 | W25600 S7680 I163840 | W102400 S30720 I655360 | ×4 for each already built |
| Austria | `ausbla` | Blacksmith | 400 | W100 S30 I640 | W400 S120 I2560 | W1600 S480 I10240 | W6400 S1920 I40960 | W25600 S7680 I163840 | W102400 S30720 I655360 | ×4 for each already built |
| Bavaria | `bavbla` | Blacksmith | 400 | W100 S30 I640 | W400 S120 I2560 | W1600 S480 I10240 | W6400 S1920 I40960 | W25600 S7680 I163840 | W102400 S30720 I655360 | ×4 for each already built |
| Denmark | `denbla` | Blacksmith | 400 | W100 S30 I640 | W400 S120 I2560 | W1600 S480 I10240 | W6400 S1920 I40960 | W25600 S7680 I163840 | W102400 S30720 I655360 | ×4 for each already built |
| England | `engbla` | Blacksmith | 400 | W100 S30 I640 | W400 S120 I2560 | W1600 S480 I10240 | W6400 S1920 I40960 | W25600 S7680 I163840 | W102400 S30720 I655360 | ×4 for each already built |
| France | `frabla` | Blacksmith | 600 | W100 S30 I640 | W600 S180 I3840 | W3600 S1080 I23040 | W21600 S6480 I138240 | W129600 S38880 I829440 | W777600 S233280 I4976640 | ×6 for each already built |
| Hungary | `hunbla` | Blacksmith | 400 | W100 S30 I640 | W400 S120 I2560 | W1600 S480 I10240 | W6400 S1920 I40960 | W25600 S7680 I163840 | W102400 S30720 I655360 | ×4 for each already built |
| Netherlands | `netbla` | Blacksmith | 400 | W100 S30 I640 | W400 S120 I2560 | W1600 S480 I10240 | W6400 S1920 I40960 | W25600 S7680 I163840 | W102400 S30720 I655360 | ×4 for each already built |
| Piedmont | `piebla` | Blacksmith | 400 | W100 S30 I640 | W400 S120 I2560 | W1600 S480 I10240 | W6400 S1920 I40960 | W25600 S7680 I163840 | W102400 S30720 I655360 | ×4 for each already built |
| Poland | `polbla` | Blacksmith | 400 | W100 S30 I640 | W400 S120 I2560 | W1600 S480 I10240 | W6400 S1920 I40960 | W25600 S7680 I163840 | W102400 S30720 I655360 | ×4 for each already built |
| Portugal | `porbla` | Blacksmith | 400 | W100 S30 I640 | W400 S120 I2560 | W1600 S480 I10240 | W6400 S1920 I40960 | W25600 S7680 I163840 | W102400 S30720 I655360 | ×4 for each already built |
| Prussia | `prubla` | Blacksmith | 400 | W100 S30 I640 | W400 S120 I2560 | W1600 S480 I10240 | W6400 S1920 I40960 | W25600 S7680 I163840 | W102400 S30720 I655360 | ×4 for each already built |
| Russia | `rusbla` | Blacksmith | 400 | W100 S30 I640 | W400 S120 I2560 | W1600 S480 I10240 | W6400 S1920 I40960 | W25600 S7680 I163840 | W102400 S30720 I655360 | ×4 for each already built |
| Saxony | `saxbla` | Blacksmith | 400 | W100 S30 I640 | W400 S120 I2560 | W1600 S480 I10240 | W6400 S1920 I40960 | W25600 S7680 I163840 | W102400 S30720 I655360 | ×4 for each already built |
| Scotland | `scobla` | Blacksmith | 400 | W100 S30 I640 | W400 S120 I2560 | W1600 S480 I10240 | W6400 S1920 I40960 | W25600 S7680 I163840 | W102400 S30720 I655360 | ×4 for each already built |
| Spain | `spabla` | Blacksmith | 400 | W100 S30 I640 | W400 S120 I2560 | W1600 S480 I10240 | W6400 S1920 I40960 | W25600 S7680 I163840 | W102400 S30720 I655360 | ×4 for each already built |
| Sweden | `swebla` | Blacksmith | 400 | W100 S30 I640 | W400 S120 I2560 | W1600 S480 I10240 | W6400 S1920 I40960 | W25600 S7680 I163840 | W102400 S30720 I655360 | ×4 for each already built |
| Switzerland | `swibla` | Blacksmith | 400 | W100 S30 I640 | W400 S120 I2560 | W1600 S480 I10240 | W6400 S1920 I40960 | W25600 S7680 I163840 | W102400 S30720 I655360 | ×4 for each already built |
| Turkey | `turbla` | Blacksmith | 400 | W100 S30 I640 | W400 S120 I2560 | W1600 S480 I10240 | W6400 S1920 I40960 | W25600 S7680 I163840 | W102400 S30720 I655360 | ×4 for each already built |
| Ukraine | `ukrbla` | Blacksmith | 400 | W100 S30 I640 | W400 S120 I2560 | W1600 S480 I10240 | W6400 S1920 I40960 | W25600 S7680 I163840 | W102400 S30720 I655360 | ×4 for each already built |
| Venice | `venbla` | Blacksmith | 400 | W100 S30 I640 | W400 S120 I2560 | W1600 S480 I10240 | W6400 S1920 I40960 | W25600 S7680 I163840 | W102400 S30720 I655360 | ×4 for each already built |

<a id="16-sta--конюшня"></a>
<a id="конюшня-sta"></a>
### 1.6 Stable (`sta`)

| Nation | Building ID | Building | Price growth, % | 1st | 2nd | 3rd | 4th | 5th | 6th | Rule |
| --- | --- | --- | ---: | --- | --- | --- | --- | --- | --- | --- |
| Algeria | `algsta` | Stable | 700 | W1000 S2200 | W7000 S15400 | W49000 S107800 | W343000 S754600 | W2401000 S5282200 | W16807000 S36975400 | ×7 for each already built |
| Austria | `aussta` | Stable | 200 | W2500 S100 G600 | W5000 S200 G1200 | W10000 S400 G2400 | W20000 S800 G4800 | W40000 S1600 G9600 | W80000 S3200 G19200 | ×2 for each already built |
| Bavaria | `bavsta` | Stable | 200 | W2500 S100 G600 | W5000 S200 G1200 | W10000 S400 G2400 | W20000 S800 G4800 | W40000 S1600 G9600 | W80000 S3200 G19200 | ×2 for each already built |
| Denmark | `densta` | Stable | 200 | W2500 S100 G600 | W5000 S200 G1200 | W10000 S400 G2400 | W20000 S800 G4800 | W40000 S1600 G9600 | W80000 S3200 G19200 | ×2 for each already built |
| England | `engsta` | Stable | 200 | W2350 G800 | W4700 G1600 | W9400 G3200 | W18800 G6400 | W37600 G12800 | W75200 G25600 | ×2 for each already built |
| France | `frasta` | Stable | 200 | W2500 S100 G600 | W5000 S200 G1200 | W10000 S400 G2400 | W20000 S800 G4800 | W40000 S1600 G9600 | W80000 S3200 G19200 | ×2 for each already built |
| Hungary | `hunsta` | Stable | 200 | W2500 S100 G600 | W5000 S200 G1200 | W10000 S400 G2400 | W20000 S800 G4800 | W40000 S1600 G9600 | W80000 S3200 G19200 | ×2 for each already built |
| Netherlands | `netsta` | Stable | 200 | W2500 S100 G600 | W5000 S200 G1200 | W10000 S400 G2400 | W20000 S800 G4800 | W40000 S1600 G9600 | W80000 S3200 G19200 | ×2 for each already built |
| Piedmont | `piesta` | Stable | 200 | W2500 S100 G600 | W5000 S200 G1200 | W10000 S400 G2400 | W20000 S800 G4800 | W40000 S1600 G9600 | W80000 S3200 G19200 | ×2 for each already built |
| Poland | `polsta` | Stable | 200 | W2500 S100 G600 | W5000 S200 G1200 | W10000 S400 G2400 | W20000 S800 G4800 | W40000 S1600 G9600 | W80000 S3200 G19200 | ×2 for each already built |
| Portugal | `porsta` | Stable | 200 | W2500 S100 G600 | W5000 S200 G1200 | W10000 S400 G2400 | W20000 S800 G4800 | W40000 S1600 G9600 | W80000 S3200 G19200 | ×2 for each already built |
| Prussia | `prusta` | Stable | 200 | W2500 S100 G600 | W5000 S200 G1200 | W10000 S400 G2400 | W20000 S800 G4800 | W40000 S1600 G9600 | W80000 S3200 G19200 | ×2 for each already built |
| Russia | `russta` | Stable | 200 | W7950 G550 | W15900 G1100 | W31800 G2200 | W63600 G4400 | W127200 G8800 | W254400 G17600 | ×2 for each already built |
| Saxony | `saxsta` | Stable | 200 | W2500 S100 G600 | W5000 S200 G1200 | W10000 S400 G2400 | W20000 S800 G4800 | W40000 S1600 G9600 | W80000 S3200 G19200 | ×2 for each already built |
| Scotland | `scosta` | Stable | 200 | W2350 G800 | W4700 G1600 | W9400 G3200 | W18800 G6400 | W37600 G12800 | W75200 G25600 | ×2 for each already built |
| Spain | `spasta` | Stable | 200 | W2500 S100 G600 | W5000 S200 G1200 | W10000 S400 G2400 | W20000 S800 G4800 | W40000 S1600 G9600 | W80000 S3200 G19200 | ×2 for each already built |
| Sweden | `swesta` | Stable | 200 | W2500 S100 G600 | W5000 S200 G1200 | W10000 S400 G2400 | W20000 S800 G4800 | W40000 S1600 G9600 | W80000 S3200 G19200 | ×2 for each already built |
| Switzerland | `swista` | Stable | 200 | W2500 S100 G600 | W5000 S200 G1200 | W10000 S400 G2400 | W20000 S800 G4800 | W40000 S1600 G9600 | W80000 S3200 G19200 | ×2 for each already built |
| Turkey | `tursta` | Stable | 700 | W1000 S2600 | W7000 S18200 | W49000 S127400 | W343000 S891800 | W2401000 S6242600 | W16807000 S43698200 | ×7 for each already built |
| Ukraine | `ukrsta` | Stable | 300 | W3200 S850 G850 | W9600 S2550 G2550 | W28800 S7650 G7650 | W86400 S22950 G22950 | W259200 S68850 G68850 | W777600 S206550 G206550 | ×3 for each already built |
| Venice | `vensta` | Stable | 200 | W2500 S100 G600 | W5000 S200 G1200 | W10000 S400 G2400 | W20000 S800 G4800 | W40000 S1600 G9600 | W80000 S3200 G19200 | ×2 for each already built |

<a id="17-tem--собор"></a>
<a id="собор-tem"></a>
### 1.7 Cathedral (`tem`)

| Nation | Building ID | Building | Price growth, % | 1st | 2nd | 3rd | 4th | 5th | 6th | Rule |
| --- | --- | --- | ---: | --- | --- | --- | --- | --- | --- | --- |
| Algeria | `algtem` | Mosque | 300 | W1000 S1200 I500 | W3000 S3600 I1500 | W9000 S10800 I4500 | W27000 S32400 I13500 | W81000 S97200 I40500 | W243000 S291600 I121500 | ×3 for each already built |
| Austria | `austem` | Cathedral | 300 | W1000 S1200 I500 | W3000 S3600 I1500 | W9000 S10800 I4500 | W27000 S32400 I13500 | W81000 S97200 I40500 | W243000 S291600 I121500 | ×3 for each already built |
| Bavaria | `bavtem` | Cathedral | 300 | W1000 S1200 I500 | W3000 S3600 I1500 | W9000 S10800 I4500 | W27000 S32400 I13500 | W81000 S97200 I40500 | W243000 S291600 I121500 | ×3 for each already built |
| Denmark | `dentem` | Cathedral | 300 | W1000 S1200 I500 | W3000 S3600 I1500 | W9000 S10800 I4500 | W27000 S32400 I13500 | W81000 S97200 I40500 | W243000 S291600 I121500 | ×3 for each already built |
| England | `engtem` | Cathedral | 300 | W1000 S1200 I500 | W3000 S3600 I1500 | W9000 S10800 I4500 | W27000 S32400 I13500 | W81000 S97200 I40500 | W243000 S291600 I121500 | ×3 for each already built |
| France | `fratem` | Cathedral | 300 | W1100 S2000 I600 | W3300 S6000 I1800 | W9900 S18000 I5400 | W29700 S54000 I16200 | W89100 S162000 I48600 | W267300 S486000 I145800 | ×3 for each already built |
| Hungary | `huntem` | Cathedral | 300 | W1000 S1200 I500 | W3000 S3600 I1500 | W9000 S10800 I4500 | W27000 S32400 I13500 | W81000 S97200 I40500 | W243000 S291600 I121500 | ×3 for each already built |
| Netherlands | `nettem` | Cathedral | 300 | W1000 S1200 I500 | W3000 S3600 I1500 | W9000 S10800 I4500 | W27000 S32400 I13500 | W81000 S97200 I40500 | W243000 S291600 I121500 | ×3 for each already built |
| Piedmont | `pietem` | Cathedral | 300 | W1000 S1200 I500 | W3000 S3600 I1500 | W9000 S10800 I4500 | W27000 S32400 I13500 | W81000 S97200 I40500 | W243000 S291600 I121500 | ×3 for each already built |
| Poland | `poltem` | Cathedral | 300 | W1000 S1200 I500 | W3000 S3600 I1500 | W9000 S10800 I4500 | W27000 S32400 I13500 | W81000 S97200 I40500 | W243000 S291600 I121500 | ×3 for each already built |
| Portugal | `portem` | Cathedral | 300 | W1000 S1200 I500 | W3000 S3600 I1500 | W9000 S10800 I4500 | W27000 S32400 I13500 | W81000 S97200 I40500 | W243000 S291600 I121500 | ×3 for each already built |
| Prussia | `prutem` | Cathedral | 300 | W1000 S1200 I500 | W3000 S3600 I1500 | W9000 S10800 I4500 | W27000 S32400 I13500 | W81000 S97200 I40500 | W243000 S291600 I121500 | ×3 for each already built |
| Russia | `rustem` | Orthodox Cathedral | 300 | W1150 S1650 G100 I500 | W3450 S4950 G300 I1500 | W10350 S14850 G900 I4500 | W31050 S44550 G2700 I13500 | W93150 S133650 G8100 I40500 | W279450 S400950 G24300 I121500 | ×3 for each already built |
| Saxony | `saxtem` | Cathedral | 300 | W1000 S1200 I500 | W3000 S3600 I1500 | W9000 S10800 I4500 | W27000 S32400 I13500 | W81000 S97200 I40500 | W243000 S291600 I121500 | ×3 for each already built |
| Scotland | `scotem` | Cathedral | 300 | W1000 S1200 I500 | W3000 S3600 I1500 | W9000 S10800 I4500 | W27000 S32400 I13500 | W81000 S97200 I40500 | W243000 S291600 I121500 | ×3 for each already built |
| Spain | `spatem` | Cathedral | 300 | W1000 S1200 I500 | W3000 S3600 I1500 | W9000 S10800 I4500 | W27000 S32400 I13500 | W81000 S97200 I40500 | W243000 S291600 I121500 | ×3 for each already built |
| Sweden | `swetem` | Cathedral | 300 | W1000 S1200 I500 | W3000 S3600 I1500 | W9000 S10800 I4500 | W27000 S32400 I13500 | W81000 S97200 I40500 | W243000 S291600 I121500 | ×3 for each already built |
| Switzerland | `switem` | Cathedral | 300 | W1000 S1200 I500 | W3000 S3600 I1500 | W9000 S10800 I4500 | W27000 S32400 I13500 | W81000 S97200 I40500 | W243000 S291600 I121500 | ×3 for each already built |
| Turkey | `turtem` | Mosque | 300 | W1000 S1200 I500 | W3000 S3600 I1500 | W9000 S10800 I4500 | W27000 S32400 I13500 | W81000 S97200 I40500 | W243000 S291600 I121500 | ×3 for each already built |
| Ukraine | `ukrtem` | Orthodox Cathedral | 300 | W1100 S1400 I300 | W3300 S4200 I900 | W9900 S12600 I2700 | W29700 S37800 I8100 | W89100 S113400 I24300 | W267300 S340200 I72900 | ×3 for each already built |
| Venice | `ventem` | Cathedral | 300 | W1000 S1200 I500 | W3000 S3600 I1500 | W9000 S10800 I4500 | W27000 S32400 I13500 | W81000 S97200 I40500 | W243000 S291600 I121500 | ×3 for each already built |

<a id="18-aca--академия"></a>
<a id="академия-aca"></a>
### 1.8 Academy (`aca`)

| Nation | Building ID | Building | Price growth, % | 1st | 2nd | 3rd | 4th | 5th | 6th | Rule |
| --- | --- | --- | ---: | --- | --- | --- | --- | --- | --- | --- |
| Algeria | `algaca` | Minaret | 300 | W1450 S1100 | W4350 S3300 | W13050 S9900 | W39150 S29700 | W117450 S89100 | W352350 S267300 | ×3 for each already built |
| Austria | `ausaca` | Academy | 300 | W1250 S1100 | W3750 S3300 | W11250 S9900 | W33750 S29700 | W101250 S89100 | W303750 S267300 | ×3 for each already built |
| Bavaria | `bavaca` | Academy | 300 | W1250 S1100 | W3750 S3300 | W11250 S9900 | W33750 S29700 | W101250 S89100 | W303750 S267300 | ×3 for each already built |
| Denmark | `denaca` | Academy | 300 | W1450 S900 | W4350 S2700 | W13050 S8100 | W39150 S24300 | W117450 S72900 | W352350 S218700 | ×3 for each already built |
| England | `engaca` | Academy | 300 | W1150 S1200 | W3450 S3600 | W10350 S10800 | W31050 S32400 | W93150 S97200 | W279450 S291600 | ×3 for each already built |
| France | `fraaca` | Academy | 300 | W1250 S1100 | W3750 S3300 | W11250 S9900 | W33750 S29700 | W101250 S89100 | W303750 S267300 | ×3 for each already built |
| Hungary | `hunaca` | Academy | 300 | W1250 S1100 | W3750 S3300 | W11250 S9900 | W33750 S29700 | W101250 S89100 | W303750 S267300 | ×3 for each already built |
| Netherlands | `netaca` | Academy | 300 | W1050 S1230 | W3150 S3690 | W9450 S11070 | W28350 S33210 | W85050 S99630 | W255150 S298890 | ×3 for each already built |
| Piedmont | `pieaca` | Academy | 300 | W1250 S1100 | W3750 S3300 | W11250 S9900 | W33750 S29700 | W101250 S89100 | W303750 S267300 | ×3 for each already built |
| Poland | `polaca` | Academy | 300 | W950 S800 | W2850 S2400 | W8550 S7200 | W25650 S21600 | W76950 S64800 | W230850 S194400 | ×3 for each already built |
| Portugal | `poraca` | Academy | 300 | W1250 S1100 | W3750 S3300 | W11250 S9900 | W33750 S29700 | W101250 S89100 | W303750 S267300 | ×3 for each already built |
| Prussia | `pruaca` | Academy | 300 | W1200 S1150 | W3600 S3450 | W10800 S10350 | W32400 S31050 | W97200 S93150 | W291600 S279450 | ×3 for each already built |
| Russia | `rusaca` | Academy | 300 | W1250 S1300 | W3750 S3900 | W11250 S11700 | W33750 S35100 | W101250 S105300 | W303750 S315900 | ×3 for each already built |
| Saxony | `saxaca` | Academy | 300 | W1250 S1100 | W3750 S3300 | W11250 S9900 | W33750 S29700 | W101250 S89100 | W303750 S267300 | ×3 for each already built |
| Scotland | `scoaca` | Academy | 300 | W1250 S1100 | W3750 S3300 | W11250 S9900 | W33750 S29700 | W101250 S89100 | W303750 S267300 | ×3 for each already built |
| Spain | `spaaca` | Academy | 300 | W1350 S1000 | W4050 S3000 | W12150 S9000 | W36450 S27000 | W109350 S81000 | W328050 S243000 | ×3 for each already built |
| Sweden | `sweaca` | Academy | 300 | W1350 S1000 | W4050 S3000 | W12150 S9000 | W36450 S27000 | W109350 S81000 | W328050 S243000 | ×3 for each already built |
| Switzerland | `swiaca` | Academy | 300 | W1250 S1100 | W3750 S3300 | W11250 S9900 | W33750 S29700 | W101250 S89100 | W303750 S267300 | ×3 for each already built |
| Turkey | `turaca` | Minaret | 300 | W1450 S1100 | W4350 S3300 | W13050 S9900 | W39150 S29700 | W117450 S89100 | W352350 S267300 | ×3 for each already built |
| Ukraine | `ukraca` | Academy | 300 | W1350 S1200 | W4050 S3600 | W12150 S10800 | W36450 S32400 | W109350 S97200 | W328050 S291600 | ×3 for each already built |
| Venice | `venaca` | Academy | 300 | W1090 S1260 | W3270 S3780 | W9810 S11340 | W29430 S34020 | W88290 S102060 | W264870 S306180 | ×3 for each already built |

<a id="19-art--артиллерийское-депо"></a>
<a id="артиллерийское-депо-art"></a>
### 1.9 Artillery Depot (`art`)

| Nation | Building ID | Building | Price growth, % | 1st | 2nd | 3rd | 4th | 5th | 6th | Rule |
| --- | --- | --- | ---: | --- | --- | --- | --- | --- | --- | --- |
| Algeria | `algart` | Artillery Depot | 200 | W100 S1000 C1400 | W200 S2000 C2800 | W400 S4000 C5600 | W800 S8000 C11200 | W1600 S16000 C22400 | W3200 S32000 C44800 | ×2 for each already built |
| Austria | `ausart` | Artillery Depot | 200 | W100 S1000 C1400 | W200 S2000 C2800 | W400 S4000 C5600 | W800 S8000 C11200 | W1600 S16000 C22400 | W3200 S32000 C44800 | ×2 for each already built |
| Bavaria | `bavart` | Artillery Depot | 200 | W100 S1000 C1400 | W200 S2000 C2800 | W400 S4000 C5600 | W800 S8000 C11200 | W1600 S16000 C22400 | W3200 S32000 C44800 | ×2 for each already built |
| Denmark | `denart` | Artillery Depot | 200 | W100 S1000 C1400 | W200 S2000 C2800 | W400 S4000 C5600 | W800 S8000 C11200 | W1600 S16000 C22400 | W3200 S32000 C44800 | ×2 for each already built |
| England | `engart` | Artillery Depot | 200 | W100 S1000 C1400 | W200 S2000 C2800 | W400 S4000 C5600 | W800 S8000 C11200 | W1600 S16000 C22400 | W3200 S32000 C44800 | ×2 for each already built |
| France | `fraart` | Artillery Depot | 200 | W100 S1000 C1400 | W200 S2000 C2800 | W400 S4000 C5600 | W800 S8000 C11200 | W1600 S16000 C22400 | W3200 S32000 C44800 | ×2 for each already built |
| Hungary | `hunart` | Artillery Depot | 200 | W100 S1000 C1400 | W200 S2000 C2800 | W400 S4000 C5600 | W800 S8000 C11200 | W1600 S16000 C22400 | W3200 S32000 C44800 | ×2 for each already built |
| Netherlands | `netart` | Artillery Depot | 200 | W100 S1000 C1400 | W200 S2000 C2800 | W400 S4000 C5600 | W800 S8000 C11200 | W1600 S16000 C22400 | W3200 S32000 C44800 | ×2 for each already built |
| Piedmont | `pieart` | Artillery Depot | 200 | W100 S1000 C1400 | W200 S2000 C2800 | W400 S4000 C5600 | W800 S8000 C11200 | W1600 S16000 C22400 | W3200 S32000 C44800 | ×2 for each already built |
| Poland | `polart` | Artillery Depot | 200 | W100 S1000 C1400 | W200 S2000 C2800 | W400 S4000 C5600 | W800 S8000 C11200 | W1600 S16000 C22400 | W3200 S32000 C44800 | ×2 for each already built |
| Portugal | `porart` | Artillery Depot | 200 | W100 S1000 C1400 | W200 S2000 C2800 | W400 S4000 C5600 | W800 S8000 C11200 | W1600 S16000 C22400 | W3200 S32000 C44800 | ×2 for each already built |
| Prussia | `pruart` | Artillery Depot | 200 | W100 S1000 C1400 | W200 S2000 C2800 | W400 S4000 C5600 | W800 S8000 C11200 | W1600 S16000 C22400 | W3200 S32000 C44800 | ×2 for each already built |
| Russia | `rusart` | Artillery Depot | 200 | W100 S1000 C1400 | W200 S2000 C2800 | W400 S4000 C5600 | W800 S8000 C11200 | W1600 S16000 C22400 | W3200 S32000 C44800 | ×2 for each already built |
| Saxony | `saxart` | Artillery Depot | 200 | W100 S1000 C1400 | W200 S2000 C2800 | W400 S4000 C5600 | W800 S8000 C11200 | W1600 S16000 C22400 | W3200 S32000 C44800 | ×2 for each already built |
| Scotland | `scoart` | Artillery Depot | 200 | W100 S1000 C1400 | W200 S2000 C2800 | W400 S4000 C5600 | W800 S8000 C11200 | W1600 S16000 C22400 | W3200 S32000 C44800 | ×2 for each already built |
| Spain | `spaart` | Artillery Depot | 200 | W100 S1000 C1400 | W200 S2000 C2800 | W400 S4000 C5600 | W800 S8000 C11200 | W1600 S16000 C22400 | W3200 S32000 C44800 | ×2 for each already built |
| Sweden | `sweart` | Artillery Depot | 200 | W100 S1000 C1400 | W200 S2000 C2800 | W400 S4000 C5600 | W800 S8000 C11200 | W1600 S16000 C22400 | W3200 S32000 C44800 | ×2 for each already built |
| Switzerland | `swiart` | Artillery Depot | 200 | W100 S1000 C1400 | W200 S2000 C2800 | W400 S4000 C5600 | W800 S8000 C11200 | W1600 S16000 C22400 | W3200 S32000 C44800 | ×2 for each already built |
| Turkey | `turart` | Artillery Depot | 200 | W500 S1200 C1400 | W1000 S2400 C2800 | W2000 S4800 C5600 | W4000 S9600 C11200 | W8000 S19200 C22400 | W16000 S38400 C44800 | ×2 for each already built |
| Ukraine | `ukrart` | Artillery Depot | 200 | W4250 S4400 G100 C1400 | W8500 S8800 G200 C2800 | W17000 S17600 G400 C5600 | W34000 S35200 G800 C11200 | W68000 S70400 G1600 C22400 | W136000 S140800 G3200 C44800 | ×2 for each already built |
| Venice | `venart` | Artillery Depot | 200 | W100 S1000 C1400 | W200 S2000 C2800 | W400 S4000 C5600 | W800 S8000 C11200 | W1600 S16000 C22400 | W3200 S32000 C44800 | ×2 for each already built |

<a id="110-dip--дипломатический-центр"></a>
<a id="дипломатический-центр-dip"></a>
### 1.10 Diplomatic Center (`dip`)

| Nation | Building ID | Building | Price growth, % | 1st | 2nd | 3rd | 4th | 5th | 6th | Rule |
| --- | --- | --- | ---: | --- | --- | --- | --- | --- | --- | --- |
| Algeria | `algdip` | Diplomatic Center | 100 | W4600 S2020 | W4600 S2020 | W4600 S2020 | W4600 S2020 | W4600 S2020 | W4600 S2020 | price remains constant |
| Austria | `ausdip` | Diplomatic Center | 100 | W4900 S1700 | W4900 S1700 | W4900 S1700 | W4900 S1700 | W4900 S1700 | W4900 S1700 | price remains constant |
| Bavaria | `bavdip` | Diplomatic Center | 100 | W4900 S1700 | W4900 S1700 | W4900 S1700 | W4900 S1700 | W4900 S1700 | W4900 S1700 | price remains constant |
| Denmark | `dendip` | Diplomatic Center | 100 | W4900 S1700 | W4900 S1700 | W4900 S1700 | W4900 S1700 | W4900 S1700 | W4900 S1700 | price remains constant |
| England | `engdip` | Diplomatic Center | 100 | W4900 S1700 | W4900 S1700 | W4900 S1700 | W4900 S1700 | W4900 S1700 | W4900 S1700 | price remains constant |
| France | `fradip` | Diplomatic Center | 100 | W4900 S1700 | W4900 S1700 | W4900 S1700 | W4900 S1700 | W4900 S1700 | W4900 S1700 | price remains constant |
| Hungary | `hundip` | Diplomatic Center | 100 | W4900 S1700 | W4900 S1700 | W4900 S1700 | W4900 S1700 | W4900 S1700 | W4900 S1700 | price remains constant |
| Netherlands | `netdip` | Diplomatic Center | 100 | W4900 S1700 | W4900 S1700 | W4900 S1700 | W4900 S1700 | W4900 S1700 | W4900 S1700 | price remains constant |
| Piedmont | `piedip` | Diplomatic Center | 100 | W4900 S1700 | W4900 S1700 | W4900 S1700 | W4900 S1700 | W4900 S1700 | W4900 S1700 | price remains constant |
| Poland | `poldip` | Diplomatic Center | 100 | W4900 S1700 | W4900 S1700 | W4900 S1700 | W4900 S1700 | W4900 S1700 | W4900 S1700 | price remains constant |
| Portugal | `pordip` | Diplomatic Center | 100 | W4900 S1700 | W4900 S1700 | W4900 S1700 | W4900 S1700 | W4900 S1700 | W4900 S1700 | price remains constant |
| Prussia | `prudip` | Diplomatic Center | 100 | W4900 S1700 | W4900 S1700 | W4900 S1700 | W4900 S1700 | W4900 S1700 | W4900 S1700 | price remains constant |
| Russia | `rusdip` | Diplomatic Center | 100 | W7900 S3700 | W7900 S3700 | W7900 S3700 | W7900 S3700 | W7900 S3700 | W7900 S3700 | price remains constant |
| Saxony | `saxdip` | Diplomatic Center | 100 | W4900 S1700 | W4900 S1700 | W4900 S1700 | W4900 S1700 | W4900 S1700 | W4900 S1700 | price remains constant |
| Scotland | `scodip` | Diplomatic Center | 100 | W4900 S1700 | W4900 S1700 | W4900 S1700 | W4900 S1700 | W4900 S1700 | W4900 S1700 | price remains constant |
| Spain | `spadip` | Diplomatic Center | 100 | W4900 S1700 | W4900 S1700 | W4900 S1700 | W4900 S1700 | W4900 S1700 | W4900 S1700 | price remains constant |
| Sweden | `swedip` | Diplomatic Center | 100 | W4900 S1700 | W4900 S1700 | W4900 S1700 | W4900 S1700 | W4900 S1700 | W4900 S1700 | price remains constant |
| Switzerland | `swidip` | Diplomatic Center | 100 | W4900 S1700 | W4900 S1700 | W4900 S1700 | W4900 S1700 | W4900 S1700 | W4900 S1700 | price remains constant |
| Turkey | `turdip` | Diplomatic Center | 100 | W4600 S2020 | W4600 S2020 | W4600 S2020 | W4600 S2020 | W4600 S2020 | W4600 S2020 | price remains constant |
| Ukraine | `ukrdip` | Diplomatic Center | 100 | W3900 S2700 | W3900 S2700 | W3900 S2700 | W3900 S2700 | W3900 S2700 | W3900 S2700 | price remains constant |
| Venice | `vendip` | Diplomatic Center | 100 | W4900 S1700 | W4900 S1700 | W4900 S1700 | W4900 S1700 | W4900 S1700 | W4900 S1700 | price remains constant |

<a id="2-общие-постройки-по-кластерам"></a>
<a id="общие-варианты-зданий"></a>
## 2. Common buildings (by clusters)

Several nations can share the same architectural version of a building.
The relevant nations are listed together.

<a id="21-mil--мельница"></a>
<a id="мельница-mil"></a>
### 2.1 Mill (`mil`)

| Building | Building ID | Nations | Price growth, % | 1st | 2nd | 3rd | 4th | 5th | 6th | Rule |
| --- | --- | --- | ---: | --- | --- | --- | --- | --- | --- | --- |
| Mill | `eurmil` | Austria, Bavaria, Denmark, England, France, Hungary, Netherlands, Piedmont, Poland, Portugal, Prussia, Saxony, Scotland, Spain, Sweden, Switzerland, Venice | 200 | W30 S150 | W60 S300 | W120 S600 | W240 S1200 | W480 S2400 | W960 S4800 | ×2 for each already built |
| Mill | `rusmil` | Russia, Ukraine | 200 | W210 | W420 | W840 | W1680 | W3360 | W6720 | ×2 for each already built |
| Mill | `turmil` | Algeria, Turkey | 200 | W30 S150 | W60 S300 | W120 S600 | W240 S1200 | W480 S2400 | W960 S4800 | ×2 for each already built |

<a id="22-sto--склад"></a>
<a id="склад-sto"></a>
### 2.2 Storehouse (`sto`)

| Building | Building ID | Nations | Price growth, % | 1st | 2nd | 3rd | 4th | 5th | 6th | Rule |
| --- | --- | --- | ---: | --- | --- | --- | --- | --- | --- | --- |
| Storehouse | `eursto` | Austria, Bavaria, Denmark, England, France, Hungary, Netherlands, Piedmont, Prussia, Saxony, Scotland, Sweden, Switzerland, Venice | 150 | W50 S20 | W75 S30 | W112 S45 | W168 S67 | W253 S101 | W379 S151 | ×1.5 for each already built |
| Storehouse | `russto` | Poland, Russia, Ukraine | 200 | W50 S20 | W100 S40 | W200 S80 | W400 S160 | W800 S320 | W1600 S640 | ×2 for each already built |
| Storehouse | `spasto` | Portugal, Spain | 150 | W20 S20 | W30 S30 | W45 S45 | W67 S67 | W101 S101 | W151 S151 | ×1.5 for each already built |
| Storehouse | `tursto` | Algeria, Turkey | 200 | W30 S10 | W60 S20 | W120 S40 | W240 S80 | W480 S160 | W960 S320 | ×2 for each already built |

<a id="23-mar--рынок"></a>
<a id="рынок-mar"></a>
### 2.3 Market (`mar`)

| Building | Building ID | Nations | Price growth, % | 1st | 2nd | 3rd | 4th | 5th | 6th | Rule |
| --- | --- | --- | ---: | --- | --- | --- | --- | --- | --- | --- |
| Market | `eurmar` | Austria, Bavaria, Denmark, England, France, Hungary, Netherlands, Piedmont, Poland, Prussia, Saxony, Scotland, Sweden, Switzerland, Venice | 2000 | W450 | W9000 | W180000 | W3600000 | W9000000 | W9000000 | ×20 for each already built |
| Market | `rusmar` | Russia, Ukraine | 2000 | W450 | W9000 | W180000 | W3600000 | W9000000 | W9000000 | ×20 for each already built |
| Market | `spamar` | Portugal, Spain | 2000 | W450 | W9000 | W180000 | W3600000 | W9000000 | W9000000 | ×20 for each already built |
| Bazaar | `turmar` | Algeria, Turkey | 1500 | W450 S150 | W6750 S2250 | W101250 S33750 | W1518750 S506250 | W9000000 S3000000 | W9000000 S3000000 | ×15 for each already built |

<a id="24-por--порт"></a>
<a id="порт-por"></a>
### 2.4 Shipyard (`por`)

| Building | Building ID | Nations | Price growth, % | 1st | 2nd | 3rd | 4th | 5th | 6th | Rule |
| --- | --- | --- | ---: | --- | --- | --- | --- | --- | --- | --- |
| Shipyard | `eurpor` | Austria, Bavaria, Denmark, England, France, Hungary, Netherlands, Piedmont, Poland, Prussia, Saxony, Scotland, Spain, Sweden, Switzerland, Venice | 150 | W1600 S800 I400 | W2400 S1200 I600 | W3600 S1800 I900 | W5400 S2700 I1350 | W8100 S4050 I2025 | W12150 S6075 I3037 | ×1.5 for each already built |
| Shipyard | `porpor` | Portugal | 150 | W1600 S800 I400 | W2400 S1200 I600 | W3600 S1800 I900 | W5400 S2700 I1350 | W8100 S4050 I2025 | W12150 S6075 I3037 | ×1.5 for each already built |
| Shipyard | `ruspor` | Russia | 150 | W1200 S800 I400 | W1800 S1200 I600 | W2700 S1800 I900 | W4050 S2700 I1350 | W6075 S4050 I2025 | W9112 S6075 I3037 | ×1.5 for each already built |
| Shipyard | `turpor` | Algeria, Turkey | 150 | W800 S800 I400 | W1200 S1200 I600 | W1800 S1800 I900 | W2700 S2700 I1350 | W4050 S4050 I2025 | W6075 S6075 I3037 | ×1.5 for each already built |
| Shipyard | `ukrpor` | Ukraine | 150 | W2000 | W3000 | W4500 | W6750 | W10125 | W15187 | ×1.5 for each already built |

<a id="25-tow--башня"></a>
<a id="башня-tow"></a>
### 2.5 Tower (`tow`)

| Building | Building ID | Nations | Price growth, % | 1st | 2nd | 3rd | 4th | 5th | 6th | Rule |
| --- | --- | --- | ---: | --- | --- | --- | --- | --- | --- | --- |
| Tower | `eurtow` | Austria, Bavaria, Denmark, England, France, Hungary, Netherlands, Piedmont, Poland, Portugal, Prussia, Saxony, Scotland, Spain, Sweden, Switzerland, Venice | 120 | W100 S100 G150 | W120 S120 G180 | W144 S144 G216 | W172 S172 G259 | W207 S207 G311 | W248 S248 G373 | ×1.2 for each already built |
| Tower | `rustow` | Russia | 125 | W100 S100 G150 | W125 S125 G187 | W156 S156 G234 | W195 S195 G292 | W244 S244 G366 | W305 S305 G457 | ×1.25 for each already built |
| Tower | `turtow` | Algeria, Turkey | 125 | W150 S90 G100 | W187 S112 G125 | W234 S140 G156 | W292 S175 G195 | W366 S219 G244 | W457 S274 G305 | ×1.25 for each already built |

<a id="26-gol--золотая-шахта"></a>
<a id="золотая-шахта-gol"></a>
### 2.6 Gold Mine (`gol`)

| Building | Building ID | Nations | Price growth, % | 1st | 2nd | 3rd | 4th | 5th | 6th | Rule |
| --- | --- | --- | ---: | --- | --- | --- | --- | --- | --- | --- |
| Mine | `eurgol` | Algeria, Austria, Bavaria, Denmark, England, France, Hungary, Netherlands, Piedmont, Poland, Portugal, Prussia, Russia, Saxony, Scotland, Spain, Sweden, Switzerland, Turkey, Ukraine, Venice | 0 | W100 S100 | W100 S100 | W100 S100 | W100 S100 | W100 S100 | W100 S100 | price remains constant |

<a id="27-iro--железная-шахта"></a>
<a id="железная-шахта-iro"></a>
### 2.7 Iron Mine (`iro`)

| Building | Building ID | Nations | Price growth, % | 1st | 2nd | 3rd | 4th | 5th | 6th | Rule |
| --- | --- | --- | ---: | --- | --- | --- | --- | --- | --- | --- |
| Mine | `euriro` | Algeria, Austria, Bavaria, Denmark, England, France, Hungary, Netherlands, Piedmont, Poland, Portugal, Prussia, Russia, Saxony, Scotland, Spain, Sweden, Switzerland, Turkey, Ukraine, Venice | 0 | W100 S100 | W100 S100 | W100 S100 | W100 S100 | W100 S100 | W100 S100 | price remains constant |

<a id="28-coa--угольная-шахта"></a>
<a id="угольная-шахта-coa"></a>
### 2.8 Coal Mine (`coa`)

| Building | Building ID | Nations | Price growth, % | 1st | 2nd | 3rd | 4th | 5th | 6th | Rule |
| --- | --- | --- | ---: | --- | --- | --- | --- | --- | --- | --- |
| Mine | `eurcoa` | Algeria, Austria, Bavaria, Denmark, England, France, Hungary, Netherlands, Piedmont, Poland, Portugal, Prussia, Russia, Saxony, Scotland, Spain, Sweden, Switzerland, Turkey, Ukraine, Venice | 0 | W100 S100 | W100 S100 | W100 S100 | W100 S100 | W100 S100 | W100 S100 | price remains constant |

<a id="29-swa--каменная-стена"></a>
<a id="каменная-стена-swa"></a>
### 2.9 Stone Wall (`swa`)
| Building | Building ID | Nations | Price growth, % | 1st | 2nd | 3rd | 4th | 5th | 6th | Rule |
| --- | --- | --- | ---: | --- | --- | --- | --- | --- | --- | --- |
| Wall | `eurswa` | Austria, Bavaria, Denmark, England, France, Hungary, Netherlands, Piedmont, Poland, Portugal, Prussia, Saxony, Scotland, Spain, Sweden, Switzerland, Venice | 0 | S50 | S50 | S50 | S50 | S50 | S50 | price remains constant |
| Wall | `russwa` | Russia | 0 | S60 | S60 | S60 | S60 | S60 | S60 | price remains constant |
| Wall | `turswa` | Algeria, Turkey | 0 | S60 | S60 | S60 | S60 | S60 | S60 | price remains constant |

<a id="210-sga--каменные-ворота"></a>
<a id="каменные-ворота-sga"></a>
### 2.10 Gate (`sga`)

| Building | Building ID | Nations | Price growth, % | 1st | 2nd | 3rd | 4th | 5th | 6th | Rule |
| --- | --- | --- | ---: | --- | --- | --- | --- | --- | --- | --- |
| Gate | `eursga` | Austria, Bavaria, Denmark, England, France, Hungary, Netherlands, Piedmont, Poland, Portugal, Prussia, Saxony, Scotland, Spain, Sweden, Switzerland, Venice | 0 | S50 | S50 | S50 | S50 | S50 | S50 | price remains constant |
| Gate | `russga` | Russia | 0 | S60 | S60 | S60 | S60 | S60 | S60 | price remains constant |
| Gate | `tursga` | Algeria, Turkey | 0 | S60 | S60 | S60 | S60 | S60 | S60 | price remains constant |

<a id="211-wga--деревянные-ворота"></a>
<a id="деревянные-ворота-wga"></a>
### 2.11 Gate (`wga`)

| Building | Building ID | Nations | Price growth, % | 1st | 2nd | 3rd | 4th | 5th | 6th | Rule |
| --- | --- | --- | ---: | --- | --- | --- | --- | --- | --- | --- |
| Gate | `ukrwga` | Algeria, Austria, Bavaria, Denmark, England, France, Hungary, Netherlands, Piedmont, Poland, Portugal, Prussia, Russia, Saxony, Scotland, Spain, Sweden, Switzerland, Turkey, Ukraine, Venice | 0 | W10 | W10 | W10 | W10 | W10 | W10 | price remains constant |

<a id="212-wwa--палисад"></a>
<a id="палисад-wwa"></a>
### 2.12 Palisade (`wwa`)

| Building | Building ID | Nations | Price growth, % | 1st | 2nd | 3rd | 4th | 5th | 6th | Rule |
| --- | --- | --- | ---: | --- | --- | --- | --- | --- | --- | --- |
| Palisade | `ukrwwa` | Algeria, Austria, Bavaria, Denmark, England, France, Hungary, Netherlands, Piedmont, Poland, Portugal, Prussia, Russia, Saxony, Scotland, Spain, Sweden, Switzerland, Turkey, Ukraine, Venice | 0 | W10 | W10 | W10 | W10 | W10 | W10 | price remains constant |


<a id="источники"></a>
## Sources

All links are relative to `data/scripts/` in the Cossacks 3 installation.

[^1]: `_unit_GetCostByID` — price of the next copy —
      `lib/unit.script:5650-5689`.

[^2]: Incrementing `counter.all[cid][unitID]` on creation —
      `lib/unit.script:3847`.

[^3]: Decrementing `counter.all[cid][unitID]` on destruction —
      `lib/unit.script:3969`.
