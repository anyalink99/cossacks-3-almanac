<a id="cossacks-3--слоты-строителей-у-зданий"></a>
<a id="максимальное-число-строителей"></a>
# Maximum Number of Builders

[← Tables and calculations](../README.md)

The shape of a building determines how many Peasants can work on it at the
same time. The values below are calculated from each building's collision
mask and checked against in-game observations.

See [Construction and repair](../../recon/world/economy/building_mechanics.md)
for the underlying mechanic.

- For an ordinary building, the game walks around the collision-mask
  perimeter [^1]. Concave shapes such as arches can therefore accept more
  builders than a simple bounding rectangle suggests.
- Some Storehouses use several narrow support strips. For these, the
  calculation treats the combined bounding area as solid.
- No building can accept more than **30 builders**.

**Compared with in-game Peasant counts:**

| Building | Predicted builders | Observed in game | Notes |
|---|---|---|---|
| Polish Town Hall (`polcen`) | 18 | 18 ✓ | convex rhombus |
| Russian Town Hall (`ruscen`) | 24 | 24 ✓ | convex |
| Swedish Town Hall (`swecen`) | **27** | **27 ✓** | **concave** arch |
| European Mill (`eurmil`) | 10 | 10 ✓ | convex |
| Russian Mill (`rusmil`) | 7 | 7 ✓ | convex |
| Polish Blacksmith (`polbla`) | 18 | 18 ✓ | convex |
| Polish 18th-century Barracks (`polba2`) | 25 | 25 ✓ | convex |
| Turkish Storehouse (`tursto`) | 8 | 8 ✓ | largest component |
| Spanish Storehouse (`spasto`) | 7 | 7 ✓ | detached cell ignored |
| Russian Storehouse (`russto`) | 8 | 8 ✓ | combined support strips |
| European Storehouse (`eursto`) | 9 | 8 | known difference of one |

The Swedish Town Hall confirms that concave edges matter: following its
arch gives 27 slots rather than the 24 predicted by a rectangular outline.
The same effect appears in the Scottish Town Hall, Piedmontese Cathedral,
Bavarian Housing, and Ukrainian Orthodox Cathedral.

**Table columns:**

- **Bounding box** — dimensions of the smallest rectangle containing the mask, in
  collision-mask cells.
- **Mask cells** — number of filled cells.
- **Components** — number of separate parts of the mask.
- **Method** — perimeter walk or combined bounding area.
- **Builder limit** — maximum simultaneous builders, after the limit of 30 is applied.

**Gates are created instantly** by upgrading a selected wall segment.
Peasants do not construct the new Gate. The values shown for these objects
therefore describe how many Peasants can repair the wall or Gate afterwards.

<a id="городские-центры-cen"></a>
<a id="городские-центры"></a>
## Town Halls (cen)

| Building | Building ID | Bounding box | Mask cells | Components | Method | Builder limit |
| --- | --- | --- | ---: | ---: | --- | ---: |
| Town Hall | `polcen` | 9×9 | 51 | 1 | Perimeter | **18** |
| Town Hall | `netcen` | 11×8 | 49 | 1 | Perimeter | **19** |
| Town Hall | `dencen` | 11×9 | 47 | 1 | Perimeter | **20** |
| Town Hall | `prucen` | 10×10 | 67 | 1 | Perimeter | **20** |
| Town Hall | `algcen` | 11×10 | 67 | 1 | Perimeter | **21** |
| Town Hall | `bavcen` | 11×10 | 57 | 1 | Perimeter | **21** |
| Town Hall | `porcen` | 11×10 | 63 | 1 | Perimeter | **21** |
| Town Hall | `saxcen` | 11×10 | 68 | 1 | Perimeter | **21** |
| Town Hall | `huncen` | 11×11 | 72 | 1 | Perimeter | **22** |
| Town Hall | `turcen` | 12×10 | 75 | 1 | Perimeter | **22** |
| Town Hall | `auscen` | 13×10 | 78 | 1 | Perimeter | **23** |
| Town Hall | `engcen` | 12×11 | 100 | 1 | Perimeter | **23** |
| Town Hall | `swicen` | 12×11 | 77 | 1 | Perimeter | **23** |
| Town Hall | `piecen` | 12×12 | 65 | 1 | Perimeter | **24** |
| Town Hall | `ruscen` | 11×13 | 81 | 1 | Perimeter | **24** |
| Town Hall | `spacen` | 12×12 | 110 | 1 | Perimeter | **24** |
| Town Hall | `fracen` | 14×13 | 108 | 1 | Perimeter | **27** |
| Town Hall | `swecen` | 15×9 | 72 | 1 | Perimeter | **27** |
| Town Hall | `scocen` | 14×10 | 72 | 1 | Perimeter | **28** |
| Town Hall | `vencen` | 15×13 | 111 | 1 | Perimeter | **28** |
| Town Hall | `ukrcen` | 15×14 | 124 | 1 | Perimeter | **29** |

<a id="склады-sto"></a>
<a id="склады"></a>
## Storehouses (sto)

| Building | Building ID | Bounding box | Mask cells | Components | Method | Builder limit |
| --- | --- | --- | ---: | ---: | --- | ---: |
| Storehouse | `spasto` | 7×4 | 11 | 2 | Perimeter | **7** |
| Storehouse | `russto` | 5×3 | 5 | 2 | Combined area | **8** |
| Storehouse | `tursto` | 4×4 | 8 | 1 | Perimeter | **8** |
| Storehouse | `eursto` | 6×3 | 5 | 2 | Combined area | **9** |

<a id="мельницы-mil"></a>
<a id="мельницы"></a>
## Mills (mil)

| Building | Building ID | Bounding box | Mask cells | Components | Method | Builder limit |
| --- | --- | --- | ---: | ---: | --- | ---: |
| Mill | `rusmil` | 4×3 | 11 | 1 | Perimeter | **7** |
| Mill | `eurmil` | 5×5 | 13 | 1 | Perimeter | **10** |
| Mill | `turmil` | 8×8 | 41 | 1 | Perimeter | **16** |

<a id="дома-hou"></a>
<a id="дома"></a>
## Housing (hou)

| Building | Building ID | Bounding box | Mask cells | Components | Method | Builder limit |
| --- | --- | --- | ---: | ---: | --- | ---: |
| Housing | `frahou` | 5×5 | 17 | 1 | Perimeter | **10** |
| Housing | `venhou` | 5×5 | 13 | 1 | Perimeter | **10** |
| Housing | `swihou` | 6×5 | 24 | 1 | Perimeter | **11** |
| Housing | `pruhou` | 6×6 | 26 | 1 | Perimeter | **12** |
| Housing | `denhou` | 7×6 | 25 | 1 | Perimeter | **13** |
| Housing | `nethou` | 7×6 | 27 | 1 | Perimeter | **13** |
| Housing | `piehou` | 6×7 | 26 | 1 | Perimeter | **13** |
| Housing | `porhou` | 6×7 | 25 | 1 | Perimeter | **13** |
| Housing | `saxhou` | 7×6 | 29 | 1 | Perimeter | **13** |
| Housing | `hunhou` | 7×7 | 29 | 1 | Perimeter | **14** |
| Housing | `scohou` | 7×7 | 34 | 1 | Perimeter | **14** |
| Housing | `spahou` | 8×6 | 34 | 1 | Perimeter | **14** |
| Housing | `turhou` | 7×7 | 31 | 1 | Perimeter | **14** |
| Housing | `aushou` | 9×6 | 33 | 1 | Perimeter | **15** |
| Housing | `enghou` | 8×7 | 35 | 1 | Perimeter | **15** |
| Housing | `swehou` | 8×7 | 27 | 1 | Perimeter | **15** |
| Housing | `alghou` | 8×8 | 45 | 1 | Perimeter | **16** |
| Housing | `bavhou` | 10×5 | 35 | 1 | Perimeter | **16** |
| Hut | `ukrhou` | 8×8 | 45 | 1 | Perimeter | **16** |
| Housing | `polhou` | 10×7 | 48 | 1 | Perimeter | **17** |
| Izba | `rushou` | 9×8 | 45 | 1 | Perimeter | **17** |

<a id="конюшни-sta"></a>
<a id="конюшни"></a>
## Stables (sta)

| Building | Building ID | Bounding box | Mask cells | Components | Method | Builder limit |
| --- | --- | --- | ---: | ---: | --- | ---: |
| Stable | `netsta` | 10×8 | 52 | 1 | Perimeter | **18** |
| Stable | `swista` | 10×8 | 55 | 1 | Perimeter | **18** |
| Stable | `hunsta` | 10×9 | 58 | 1 | Perimeter | **19** |
| Stable | `prusta` | 9×10 | 59 | 1 | Perimeter | **19** |
| Stable | `saxsta` | 10×9 | 58 | 1 | Perimeter | **19** |
| Stable | `vensta` | 10×9 | 57 | 1 | Perimeter | **19** |
| Stable | `densta` | 10×10 | 60 | 1 | Perimeter | **20** |
| Stable | `scosta` | 10×10 | 61 | 1 | Perimeter | **20** |
| Stable | `aussta` | 13×8 | 66 | 1 | Perimeter | **21** |
| Stable | `bavsta` | 12×9 | 64 | 1 | Perimeter | **21** |
| Stable | `spasta` | 11×10 | 62 | 1 | Perimeter | **21** |
| Stable | `swesta` | 12×9 | 71 | 1 | Perimeter | **21** |
| Stable | `engsta` | 11×11 | 76 | 1 | Perimeter | **22** |
| Stable | `frasta` | 11×11 | 79 | 1 | Perimeter | **22** |
| Stable | `russta` | 11×11 | 79 | 1 | Perimeter | **22** |
| Stable | `piesta` | 12×12 | 78 | 1 | Perimeter | **24** |
| Stable | `porsta` | 13×11 | 78 | 1 | Perimeter | **24** |
| Stable | `tursta` | 13×12 | 99 | 1 | Perimeter | **25** |
| Stable | `polsta` | 13×13 | 94 | 1 | Perimeter | **26** |
| Stable | `ukrsta` | 13×13 | 97 | 1 | Perimeter | **26** |

<a id="базары-mar"></a>
<a id="рынки"></a>
## Markets (mar)

| Building | Building ID | Bounding box | Mask cells | Components | Method | Builder limit |
| --- | --- | --- | ---: | ---: | --- | ---: |
| Bazaar | `turmar` | 11×8 | 55 | 1 | Perimeter | **19** |
| Market | `rusmar` | 11×12 | 80 | 1 | Perimeter | **23** |
| Market | `spamar` | 11×13 | 82 | 1 | Perimeter | **24** |
| Market | `eurmar` | 14×11 | 83 | 1 | Perimeter | **25** |

<a id="дипломатические-центры-dip"></a>
<a id="дипломатические-центры"></a>
## Diplomatic Centers (dip)

| Building | Building ID | Bounding box | Mask cells | Components | Method | Builder limit |
| --- | --- | --- | ---: | ---: | --- | ---: |
| Diplomatic Center | `engdip` | 9×7 | 40 | 1 | Perimeter | **16** |
| Diplomatic Center | `piedip` | 8×8 | 37 | 1 | Perimeter | **16** |
| Diplomatic Center | `poldip` | 8×8 | 45 | 1 | Perimeter | **16** |
| Diplomatic Center | `saxdip` | 8×9 | 40 | 1 | Perimeter | **17** |
| Diplomatic Center | `swedip` | 9×8 | 37 | 1 | Perimeter | **17** |
| Diplomatic Center | `bavdip` | 9×9 | 50 | 1 | Perimeter | **18** |
| Diplomatic Center | `fradip` | 9×9 | 49 | 1 | Perimeter | **18** |
| Diplomatic Center | `hundip` | 9×9 | 53 | 1 | Perimeter | **18** |
| Diplomatic Center | `netdip` | 9×9 | 45 | 1 | Perimeter | **18** |
| Diplomatic Center | `pordip` | 9×9 | 56 | 1 | Perimeter | **18** |
| Diplomatic Center | `rusdip` | 9×9 | 53 | 1 | Perimeter | **18** |
| Diplomatic Center | `swidip` | 9×9 | 44 | 1 | Perimeter | **18** |
| Diplomatic Center | `vendip` | 9×9 | 43 | 1 | Perimeter | **18** |
| Diplomatic Center | `prudip` | 10×9 | 52 | 1 | Perimeter | **19** |
| Diplomatic Center | `scodip` | 10×9 | 49 | 1 | Perimeter | **19** |
| Diplomatic Center | `dendip` | 11×10 | 58 | 1 | Perimeter | **21** |
| Diplomatic Center | `spadip` | 11×10 | 65 | 1 | Perimeter | **21** |
| Diplomatic Center | `turdip` | 12×10 | 71 | 1 | Perimeter | **22** |
| Diplomatic Center | `ukrdip` | 11×11 | 53 | 1 | Perimeter | **22** |
| Diplomatic Center | `ausdip` | 12×12 | 76 | 1 | Perimeter | **24** |

<a id="храмы-tem"></a>
<a id="храмы"></a>
## Temples (tem)

| Building | Building ID | Bounding box | Mask cells | Components | Method | Builder limit |
| --- | --- | --- | ---: | ---: | --- | ---: |
| Cathedral | `pietem` | 10×10 | 64 | 1 | Perimeter | **20** |
| Cathedral | `nettem` | 11×10 | 69 | 1 | Perimeter | **21** |
| Cathedral | `switem` | 11×10 | 67 | 1 | Perimeter | **21** |
| Cathedral | `bavtem` | 11×11 | 81 | 1 | Perimeter | **22** |
| Cathedral | `dentem` | 11×11 | 73 | 1 | Perimeter | **22** |
| Cathedral | `poltem` | 11×11 | 91 | 1 | Perimeter | **22** |
| Cathedral | `scotem` | 11×11 | 77 | 1 | Perimeter | **22** |
| Mosque | `turtem` | 11×11 | 71 | 1 | Perimeter | **22** |
| Cathedral | `swetem` | 12×11 | 75 | 1 | Perimeter | **23** |
| Cathedral | `engtem` | 12×12 | 97 | 1 | Perimeter | **24** |
| Cathedral | `portem` | 12×11 | 85 | 1 | Perimeter | **25** |
| Cathedral | `prutem` | 12×13 | 99 | 1 | Perimeter | **25** |
| Cathedral | `saxtem` | 13×13 | 90 | 1 | Perimeter | **26** |
| Cathedral | `austem` | 15×13 | 134 | 1 | Perimeter | **28** |
| Cathedral | `huntem` | 14×14 | 113 | 1 | Perimeter | **28** |
| Cathedral | `fratem` | 15×15 | 124 | 1 | Perimeter | **30** |
| Orthodox Cathedral | `rustem` | 16×15 | 156 | 1 | Perimeter | **30** |
| Cathedral | `spatem` | 18×18 | 183 | 1 | Perimeter | **30** |
| Orthodox Cathedral | `ukrtem` | 21×15 | 173 | 1 | Perimeter | **30** |
| Cathedral | `ventem` | 18×18 | 191 | 1 | Perimeter | **30** |

<a id="казармы-17-в-bar"></a>
<a id="казармы-xvii-века"></a>
## 17th-century Barracks (bar)

| Building | Building ID | Bounding box | Mask cells | Components | Method | Builder limit |
| --- | --- | --- | ---: | ---: | --- | ---: |
| Barracks, 17th century | `frabar` | 9×7 | 37 | 1 | Perimeter | **16** |
| Barracks, 17th century | `prubar` | 9×9 | 52 | 1 | Perimeter | **18** |
| Barracks, 17th century | `spabar` | 9×9 | 55 | 1 | Perimeter | **18** |
| Barracks, 17th century | `denbar` | 12×8 | 63 | 1 | Perimeter | **20** |
| Barracks, 17th century | `netbar` | 11×9 | 66 | 1 | Perimeter | **20** |
| Barracks, 17th century | `saxbar` | 10×10 | 67 | 1 | Perimeter | **20** |
| Barracks, 17th century | `engbar` | 12×10 | 73 | 1 | Perimeter | **22** |
| Barracks, 17th century | `hunbar` | 11×11 | 72 | 1 | Perimeter | **22** |
| Barracks, 17th century | `porbar` | 11×11 | 73 | 1 | Perimeter | **22** |
| Barracks | `turbar` | 11×11 | 84 | 1 | Perimeter | **22** |
| Barracks, 17th century | `bavbar` | 12×11 | 68 | 1 | Perimeter | **23** |
| Strelets Barracks | `rusbar` | 11×12 | 73 | 1 | Perimeter | **23** |
| Barracks, 17th century | `scobar` | 12×11 | 76 | 1 | Perimeter | **23** |
| Barracks, 17th century | `swibar` | 12×11 | 86 | 1 | Perimeter | **23** |
| Cossack House | `ukrbar` | 13×10 | 78 | 1 | Perimeter | **23** |
| Barracks, 17th century | `venbar` | 11×12 | 81 | 1 | Perimeter | **23** |
| Barracks, 17th century | `piebar` | 12×12 | 68 | 1 | Perimeter | **24** |
| Barracks, 17th century | `ausbar` | 13×12 | 90 | 1 | Perimeter | **25** |
| Barracks, 17th century | `swebar` | 13×12 | 96 | 1 | Perimeter | **25** |
| Barracks, 17th century | `polbar` | 14×13 | 113 | 1 | Perimeter | **27** |

<a id="казармы-18-в-ba2"></a>
<a id="казармы-xviii-века"></a>
## 18th-century Barracks (ba2)

| Building | Building ID | Bounding box | Mask cells | Components | Method | Builder limit |
| --- | --- | --- | ---: | ---: | --- | ---: |
| Barracks, 18th century | `venba2` | 10×9 | 58 | 1 | Perimeter | **19** |
| Barracks, 18th century | `saxba2` | 11×9 | 59 | 1 | Perimeter | **20** |
| Barracks, 18th century | `netba2` | 11×10 | 69 | 1 | Perimeter | **21** |
| Barracks, 18th century | `denba2` | 11×11 | 63 | 1 | Perimeter | **22** |
| Barracks, 18th century | `pieba2` | 11×11 | 65 | 1 | Perimeter | **22** |
| Barracks, 18th century | `pruba2` | 11×11 | 91 | 1 | Perimeter | **22** |
| Barracks, 18th century | `swiba2` | 11×11 | 63 | 1 | Perimeter | **22** |
| Barracks, 18th century | `bavba2` | 12×11 | 73 | 1 | Perimeter | **23** |
| Barracks, 18th century | `engba2` | 12×11 | 65 | 1 | Perimeter | **23** |
| Barracks, 18th century | `porba2` | 12×12 | 86 | 1 | Perimeter | **24** |
| Barracks, 18th century | `polba2` | 13×12 | 87 | 1 | Perimeter | **25** |
| Barracks, 18th century | `hunba2` | 13×13 | 101 | 1 | Perimeter | **26** |
| Barracks, 18th century | `spaba2` | 13×13 | 103 | 1 | Perimeter | **26** |
| Barracks, 18th century | `sweba2` | 14×13 | 108 | 1 | Perimeter | **27** |
| Barracks, 18th century | `ausba2` | 15×14 | 129 | 1 | Perimeter | **29** |
| Barracks, 18th century | `fraba2` | 15×14 | 112 | 1 | Perimeter | **29** |
| Barracks, 18th century | `rusba2` | 16×16 | 133 | 1 | Perimeter | **30** |
| Castle | `scoba2` | 15×15 | 123 | 1 | Perimeter | **30** |

<a id="кузницы-bla"></a>
<a id="кузницы"></a>
## Blacksmiths (bla)

| Building | Building ID | Bounding box | Mask cells | Components | Method | Builder limit |
| --- | --- | --- | ---: | ---: | --- | ---: |
| Blacksmith | `frabla` | 6×7 | 23 | 1 | Perimeter | **13** |
| Blacksmith | `hunbla` | 6×7 | 28 | 1 | Perimeter | **13** |
| Blacksmith | `spabla` | 7×6 | 24 | 1 | Perimeter | **13** |
| Blacksmith | `netbla` | 8×6 | 37 | 1 | Perimeter | **14** |
| Blacksmith | `prubla` | 8×6 | 29 | 1 | Perimeter | **14** |
| Blacksmith | `saxbla` | 8×6 | 32 | 1 | Perimeter | **14** |
| Blacksmith | `porbla` | 9×6 | 35 | 1 | Perimeter | **15** |
| Blacksmith | `rusbla` | 8×7 | 38 | 1 | Perimeter | **15** |
| Blacksmith | `turbla` | 8×7 | 45 | 1 | Perimeter | **15** |
| Blacksmith | `bavbla` | 9×7 | 38 | 1 | Perimeter | **16** |
| Blacksmith | `denbla` | 9×7 | 33 | 1 | Perimeter | **16** |
| Blacksmith | `engbla` | 9×7 | 38 | 1 | Perimeter | **16** |
| Blacksmith | `piebla` | 9×7 | 41 | 1 | Perimeter | **16** |
| Blacksmith | `scobla` | 9×7 | 32 | 1 | Perimeter | **16** |
| Blacksmith | `swebla` | 10×6 | 47 | 1 | Perimeter | **16** |
| Blacksmith | `venbla` | 8×8 | 43 | 1 | Perimeter | **16** |
| Blacksmith | `ausbla` | 10×7 | 41 | 1 | Perimeter | **17** |
| Blacksmith | `swibla` | 8×9 | 48 | 1 | Perimeter | **17** |
| Blacksmith | `polbla` | 10×8 | 48 | 1 | Perimeter | **18** |
| Blacksmith | `ukrbla` | 10×9 | 54 | 1 | Perimeter | **19** |

<a id="академии-aca"></a>
<a id="академии"></a>
## Academies (aca)

| Building | Building ID | Bounding box | Mask cells | Components | Method | Builder limit |
| --- | --- | --- | ---: | ---: | --- | ---: |
| Minaret | `turaca` | 3×3 | 9 | 1 | Perimeter | **6** |
| Academy | `poraca` | 8×8 | 41 | 1 | Perimeter | **16** |
| Academy | `denaca` | 9×8 | 47 | 1 | Perimeter | **17** |
| Academy | `netaca` | 9×9 | 39 | 1 | Perimeter | **18** |
| Academy | `polaca` | 9×9 | 51 | 1 | Perimeter | **18** |
| Academy | `pruaca` | 10×8 | 50 | 1 | Perimeter | **18** |
| Academy | `sweaca` | 9×9 | 49 | 1 | Perimeter | **18** |
| Academy | `hunaca` | 10×9 | 56 | 1 | Perimeter | **19** |
| Academy | `saxaca` | 10×9 | 56 | 1 | Perimeter | **19** |
| Academy | `scoaca` | 11×9 | 58 | 1 | Perimeter | **20** |
| Academy | `bavaca` | 13×9 | 68 | 1 | Perimeter | **22** |
| Academy | `pieaca` | 11×11 | 79 | 1 | Perimeter | **22** |
| Academy | `swiaca` | 11×11 | 71 | 1 | Perimeter | **22** |
| Academy | `venaca` | 11×11 | 59 | 1 | Perimeter | **22** |
| Academy | `engaca` | 12×11 | 76 | 1 | Perimeter | **23** |
| Academy | `fraaca` | 13×11 | 65 | 1 | Perimeter | **24** |
| Academy | `rusaca` | 12×13 | 80 | 1 | Perimeter | **25** |
| Academy | `ausaca` | 13×13 | 67 | 1 | Perimeter | **26** |
| Academy | `spaaca` | 13×13 | 97 | 1 | Perimeter | **26** |
| Academy | `ukraca` | 17×17 | 121 | 1 | Perimeter | **30** |

<a id="артиллерийские-депо-art"></a>
<a id="артиллерийские-депо"></a>
## Artillery Depots (art)

| Building | Building ID | Bounding box | Mask cells | Components | Method | Builder limit |
| --- | --- | --- | ---: | ---: | --- | ---: |
| Artillery Depot | `hunart` | 10×8 | 55 | 1 | Perimeter | **18** |
| Artillery Depot | `pieart` | 11×8 | 62 | 1 | Perimeter | **19** |
| Artillery Depot | `polart` | 10×9 | 65 | 1 | Perimeter | **19** |
| Artillery Depot | `saxart` | 10×9 | 54 | 1 | Perimeter | **19** |
| Artillery Depot | `bavart` | 11×9 | 61 | 1 | Perimeter | **20** |
| Artillery Depot | `denart` | 12×8 | 58 | 1 | Perimeter | **20** |
| Artillery Depot | `netart` | 11×9 | 62 | 1 | Perimeter | **20** |
| Artillery Depot | `sweart` | 11×9 | 56 | 1 | Perimeter | **20** |
| Artillery Depot | `swiart` | 11×9 | 66 | 1 | Perimeter | **20** |
| Artillery Depot | `venart` | 11×9 | 71 | 1 | Perimeter | **20** |
| Artillery Depot | `scoart` | 12×9 | 59 | 1 | Perimeter | **21** |
| Artillery Depot | `ausart` | 12×10 | 71 | 1 | Perimeter | **22** |
| Artillery Depot | `engart` | 12×10 | 66 | 1 | Perimeter | **22** |
| Artillery Depot | `porart` | 12×10 | 63 | 1 | Perimeter | **22** |
| Artillery Depot | `pruart` | 11×11 | 68 | 1 | Perimeter | **22** |
| Artillery Depot | `spaart` | 11×12 | 90 | 1 | Perimeter | **23** |
| Artillery Depot | `fraart` | 12×12 | 85 | 1 | Perimeter | **24** |
| Artillery Depot | `rusart` | 14×10 | 75 | 1 | Perimeter | **24** |
| Artillery Depot | `turart` | 14×14 | 110 | 1 | Perimeter | **28** |
| Artillery Depot | `ukrart` | 17×14 | 141 | 1 | Perimeter | **30** |

<a id="порты-por"></a>
<a id="порты"></a>
## Shipyards (por)

| Building | Building ID | Bounding box | Mask cells | Components | Method | Builder limit |
| --- | --- | --- | ---: | ---: | --- | ---: |
| Shipyard | `porpor` | 10×11 | 80 | 1 | Perimeter | **21** |
| Shipyard | `ruspor` | 14×13 | 124 | 1 | Perimeter | **27** |
| Shipyard | `eurpor` | 14×16 | 129 | 1 | Perimeter | **30** |
| Shipyard | `turpor` | 16×14 | 146 | 1 | Perimeter | **30** |
| Shipyard | `ukrpor` | 15×21 | 188 | 1 | Perimeter | **30** |

<a id="башни-tow"></a>
<a id="башни"></a>
## Towers (tow)

| Building | Building ID | Bounding box | Mask cells | Components | Method | Builder limit |
| --- | --- | --- | ---: | ---: | --- | ---: |
| Tower | `eurtow` | 5×5 | 21 | 1 | Perimeter | **10** |
| Tower | `rustow` | 5×5 | 21 | 1 | Perimeter | **10** |
| Tower | `turtow` | 7×7 | 37 | 1 | Perimeter | **14** |

<a id="шахты-golirocoa"></a>
<a id="шахты"></a>
## Mines (gol/iro/coa)

| Building | Building ID | Bounding box | Mask cells | Components | Method | Builder limit |
| --- | --- | --- | ---: | ---: | --- | ---: |
| Mine | `eurgol` | 8×8 | 52 | 1 | Perimeter | **16** |
| Mine | `euriro` | 8×8 | 52 | 1 | Perimeter | **16** |
| Mine | `eurcoa` | 8×8 | 52 | 1 | Perimeter | **16** |

<a id="стены-swawwa"></a>
<a id="стены"></a>
## Walls (swa/wwa)

| Building | Building ID | Bounding box | Mask cells | Components | Method | Builder limit |
| --- | --- | --- | ---: | ---: | --- | ---: |
| Wall | `eurswa` | 2×2 | 4 | 1 | Perimeter | **4** |
| Wall | `russwa` | 2×2 | 4 | 1 | Perimeter | **4** |
| Wall | `turswa` | 2×2 | 4 | 1 | Perimeter | **4** |
| Palisade | `ukrwwa` | 2×2 | 4 | 1 | Perimeter | **4** |
| Palisade | `eurwwa` | 6×7 | 30 | 1 | Perimeter | **13** |

<a id="ворота-sgawga"></a>
<a id="ворота"></a>
## Gate (sga/wga)

| Building | Building ID | Bounding box | Mask cells | Components | Method | Builder limit |
| --- | --- | --- | ---: | ---: | --- | ---: |
| Gate | `eursga` | 6×7 | 30 | 1 | Perimeter | **13** |
| Gate | `eurwga` | 6×7 | 30 | 1 | Perimeter | **13** |

<a id="прочие-миссиисегменты-стенмосты"></a>
## Other (missions/wall segments/bridges)

| Building | Building ID | Bounding box | Mask cells | Components | Method | Builder limit |
| --- | --- | --- | ---: | ---: | --- | ---: |
| Gate segment | `eursga_14` | 6×2 | 4 | 2 | Combined area | **8** |
| Gate segment | `eursga_15` | 2×6 | 4 | 2 | Combined area | **8** |
| Gate segment | `eursga_16` | 8×8 | 22 | 2 | Perimeter | **7** |
| Gate segment | `eursga_17` | 8×9 | 24 | 2 | Perimeter | **8** |
| Wall segment | `eurswa_01` | 2×2 | 4 | 1 | Perimeter | **4** |
| Wall segment | `eurswa_02` | 2×2 | 4 | 1 | Perimeter | **4** |
| Wall segment | `eurswa_03` | 4×4 | 8 | 1 | Perimeter | **8** |
| Wall segment | `eurswa_04` | 4×4 | 8 | 1 | Perimeter | **8** |
| Wall segment | `eurswa_05` | 2×2 | 4 | 1 | Perimeter | **4** |
| Wall segment | `eurswa_06` | 3×3 | 6 | 1 | Perimeter | **6** |
| Wall segment | `eurswa_07` | 3×3 | 6 | 1 | Perimeter | **6** |
| Wall segment | `eurswa_08` | 3×3 | 6 | 1 | Perimeter | **6** |
| Wall segment | `eurswa_09` | 3×3 | 6 | 1 | Perimeter | **6** |
| Wall segment | `eurswa_10` | 3×3 | 6 | 1 | Perimeter | **6** |
| Wall segment | `eurswa_11` | 3×3 | 6 | 1 | Perimeter | **6** |
| Wall segment | `eurswa_12` | 3×3 | 6 | 1 | Perimeter | **6** |
| Wall segment | `eurswa_13` | 3×3 | 6 | 1 | Perimeter | **6** |
| Wall segment | `eurswa_45gate` | 2×2 | 4 | 1 | Perimeter | **4** |
| Wall segment | `eurswa_45v1` | 2×2 | 4 | 1 | Perimeter | **4** |
| Wall segment | `eurswa_45v2` | 2×2 | 4 | 1 | Perimeter | **4** |
| Wall segment | `eurswa_gate` | 2×2 | 4 | 1 | Perimeter | **4** |
| Wall segment | `eurswa_tower` | 2×2 | 4 | 1 | Perimeter | **4** |
| Wall segment | `eurswa_turn` | 2×2 | 4 | 1 | Perimeter | **4** |
| Wall segment | `eurswa_turnmirror` | 2×2 | 4 | 1 | Perimeter | **4** |
| Wall segment | `eurswa_v1` | 2×2 | 4 | 1 | Perimeter | **4** |
| Wall segment | `eurswa_v2` | 2×2 | 4 | 1 | Perimeter | **4** |
| Gate segment | `g_45left` | 2×2 | 4 | 1 | Perimeter | **4** |
| Gate segment | `g_45right` | 2×2 | 4 | 1 | Perimeter | **4** |
| Log Cabin | `misblg` | 8×8 | 35 | 1 | Perimeter | **16** |
| Log Cabin | `misblg2` | 8×8 | 33 | 1 | Perimeter | **16** |
| Bridge | `misbridge1` | 2×2 | 4 | 1 | Perimeter | **4** |
| Bridge | `misbridge1a` | 2×2 | 4 | 1 | Perimeter | **4** |
| Bridge | `misbridge2` | 2×2 | 4 | 1 | Perimeter | **4** |
| Bridge | `misbridge2a` | 2×2 | 4 | 1 | Perimeter | **4** |
| Bridge | `misbridge3` | 2×2 | 4 | 1 | Perimeter | **4** |
| Bridge | `misbridge3a` | 2×2 | 4 | 1 | Perimeter | **4** |
| Bridge | `misbridge4` | 2×2 | 4 | 1 | Perimeter | **4** |
| Bridge | `misbridge4a` | 2×2 | 4 | 1 | Perimeter | **4** |
| Cauldron | `miscauldron` | 2×2 | 3 | 1 | Perimeter | **4** |
| Chest | `mischest1` | 2×3 | 4 | 1 | Perimeter | **5** |
| Chest | `mischest2` | 2×2 | 3 | 1 | Perimeter | **4** |
| Command Center | `miscommandcenter` | 18×13 | 125 | 1 | Perimeter | **30** |
| Tent | `mistent` | 12×8 | 47 | 1 | Perimeter | **20** |
| Well | `miswel1` | 2×2 | 4 | 1 | Perimeter | **4** |
| Well | `miswel2` | 3×2 | 6 | 1 | Perimeter | **5** |
| Well | `miswel3` | 2×3 | 4 | 1 | Perimeter | **5** |
| Yurt | `misyurt` | 6×8 | 31 | 1 | Perimeter | **14** |
| Gate segment | `russga_14` | 6×2 | 4 | 2 | Combined area | **8** |
| Gate segment | `russga_15` | 2×6 | 4 | 2 | Combined area | **8** |
| Gate segment | `russga_16` | 8×8 | 22 | 2 | Perimeter | **7** |
| Gate segment | `russga_17` | 8×9 | 24 | 2 | Perimeter | **8** |
| Wall segment | `russwa_01` | 2×2 | 4 | 1 | Perimeter | **4** |
| Wall segment | `russwa_02` | 2×2 | 4 | 1 | Perimeter | **4** |
| Wall segment | `russwa_03` | 4×4 | 8 | 1 | Perimeter | **8** |
| Wall segment | `russwa_04` | 4×4 | 8 | 1 | Perimeter | **8** |
| Wall segment | `russwa_05` | 2×2 | 4 | 1 | Perimeter | **4** |
| Wall segment | `russwa_06` | 3×3 | 6 | 1 | Perimeter | **6** |
| Wall segment | `russwa_07` | 3×3 | 6 | 1 | Perimeter | **6** |
| Wall segment | `russwa_08` | 3×3 | 6 | 1 | Perimeter | **6** |
| Wall segment | `russwa_09` | 3×3 | 6 | 1 | Perimeter | **6** |
| Wall segment | `russwa_10` | 3×3 | 6 | 1 | Perimeter | **6** |
| Wall segment | `russwa_11` | 3×3 | 6 | 1 | Perimeter | **6** |
| Wall segment | `russwa_12` | 3×3 | 6 | 1 | Perimeter | **6** |
| Wall segment | `russwa_13` | 3×3 | 6 | 1 | Perimeter | **6** |
| Wall segment | `russwa_45gate` | 2×2 | 4 | 1 | Perimeter | **4** |
| Wall segment | `russwa_45v1` | 2×2 | 4 | 1 | Perimeter | **4** |
| Wall segment | `russwa_45v2` | 2×2 | 4 | 1 | Perimeter | **4** |
| Wall segment | `russwa_gate` | 2×2 | 4 | 1 | Perimeter | **4** |
| Wall segment | `russwa_tower` | 2×2 | 4 | 1 | Perimeter | **4** |
| Wall segment | `russwa_turn` | 2×2 | 4 | 1 | Perimeter | **4** |
| Wall segment | `russwa_turnmirror` | 2×2 | 4 | 1 | Perimeter | **4** |
| Wall segment | `russwa_v1` | 2×2 | 4 | 1 | Perimeter | **4** |
| Wall segment | `russwa_v2` | 2×2 | 4 | 1 | Perimeter | **4** |
| Gate segment | `tursga_14` | 6×2 | 4 | 2 | Combined area | **8** |
| Gate segment | `tursga_15` | 2×6 | 4 | 2 | Combined area | **8** |
| Gate segment | `tursga_16` | 8×8 | 22 | 2 | Perimeter | **7** |
| Gate segment | `tursga_17` | 8×9 | 24 | 2 | Perimeter | **8** |
| Wall segment | `turswa_01` | 2×2 | 4 | 1 | Perimeter | **4** |
| Wall segment | `turswa_02` | 2×2 | 4 | 1 | Perimeter | **4** |
| Wall segment | `turswa_03` | 4×4 | 8 | 1 | Perimeter | **8** |
| Wall segment | `turswa_04` | 4×4 | 8 | 1 | Perimeter | **8** |
| Wall segment | `turswa_05` | 2×2 | 4 | 1 | Perimeter | **4** |
| Wall segment | `turswa_06` | 3×3 | 6 | 1 | Perimeter | **6** |
| Wall segment | `turswa_07` | 3×3 | 6 | 1 | Perimeter | **6** |
| Wall segment | `turswa_08` | 3×3 | 6 | 1 | Perimeter | **6** |
| Wall segment | `turswa_09` | 3×3 | 6 | 1 | Perimeter | **6** |
| Wall segment | `turswa_10` | 3×3 | 6 | 1 | Perimeter | **6** |
| Wall segment | `turswa_11` | 3×3 | 6 | 1 | Perimeter | **6** |
| Wall segment | `turswa_12` | 3×3 | 6 | 1 | Perimeter | **6** |
| Wall segment | `turswa_13` | 3×3 | 6 | 1 | Perimeter | **6** |
| Wall segment | `turswa_45gate` | 2×2 | 4 | 1 | Perimeter | **4** |
| Wall segment | `turswa_45v1` | 2×2 | 4 | 1 | Perimeter | **4** |
| Wall segment | `turswa_45v2` | 2×2 | 4 | 1 | Perimeter | **4** |
| Wall segment | `turswa_gate` | 2×2 | 4 | 1 | Perimeter | **4** |
| Wall segment | `turswa_tower` | 2×2 | 4 | 1 | Perimeter | **4** |
| Wall segment | `turswa_turn` | 2×2 | 4 | 1 | Perimeter | **4** |
| Wall segment | `turswa_turnmirror` | 2×2 | 4 | 1 | Perimeter | **4** |
| Wall segment | `turswa_v1` | 2×2 | 4 | 1 | Perimeter | **4** |
| Wall segment | `turswa_v2` | 2×2 | 4 | 1 | Perimeter | **4** |
| Gate segment | `ukrwga_14` | 6×2 | 4 | 2 | Combined area | **8** |
| Gate segment | `ukrwga_15` | 2×6 | 4 | 2 | Combined area | **8** |
| Gate segment | `ukrwga_16` | 8×16 | 28 | 4 | Perimeter | **6** |
| Gate segment | `ukrwga_17` | 8×8 | 11 | 2 | Perimeter | **6** |
| Palisade segment | `ukrwwa_01` | 2×2 | 4 | 1 | Perimeter | **4** |
| Palisade segment | `ukrwwa_02` | 2×2 | 4 | 1 | Perimeter | **4** |
| Palisade segment | `ukrwwa_03` | 4×4 | 8 | 1 | Perimeter | **8** |
| Palisade segment | `ukrwwa_04` | 4×4 | 8 | 1 | Perimeter | **8** |
| Palisade segment | `ukrwwa_05` | 2×2 | 4 | 1 | Perimeter | **4** |
| Palisade segment | `ukrwwa_06` | 3×3 | 6 | 1 | Perimeter | **6** |
| Palisade segment | `ukrwwa_07` | 3×3 | 6 | 1 | Perimeter | **6** |
| Palisade segment | `ukrwwa_08` | 3×3 | 6 | 1 | Perimeter | **6** |
| Palisade segment | `ukrwwa_09` | 3×3 | 6 | 1 | Perimeter | **6** |
| Palisade segment | `ukrwwa_10` | 3×3 | 6 | 1 | Perimeter | **6** |
| Palisade segment | `ukrwwa_11` | 3×3 | 6 | 1 | Perimeter | **6** |
| Palisade segment | `ukrwwa_12` | 3×3 | 6 | 1 | Perimeter | **6** |
| Palisade segment | `ukrwwa_13` | 3×3 | 6 | 1 | Perimeter | **6** |
| Palisade segment | `ukrwwa_45gate` | 2×2 | 4 | 1 | Perimeter | **4** |
| Palisade segment | `ukrwwa_45v1` | 2×2 | 4 | 1 | Perimeter | **4** |
| Palisade segment | `ukrwwa_45v2` | 2×2 | 4 | 1 | Perimeter | **4** |
| Palisade segment | `ukrwwa_gate` | 2×2 | 4 | 1 | Perimeter | **4** |
| Palisade segment | `ukrwwa_tower` | 2×2 | 4 | 1 | Perimeter | **4** |
| Palisade segment | `ukrwwa_turn` | 2×2 | 4 | 1 | Perimeter | **4** |
| Palisade segment | `ukrwwa_turnmirror` | 2×2 | 4 | 1 | Perimeter | **4** |
| Palisade segment | `ukrwwa_v1` | 2×2 | 4 | 1 | Perimeter | **4** |
| Palisade segment | `ukrwwa_v2` | 2×2 | 4 | 1 | Perimeter | **4** |


<a id="источники"></a>
## Sources

All links are relative to `data/scripts/` in the Cossacks 3 installation.

[^1]: `_unit_CalcBuilderPoints` — `lib/unit.script:8702-9006`.
