<a id="cossacks-3--слоты-строителей-у-зданий"></a>
<a id="максимальное-число-строителей"></a>
# Cossacks 3 - Builder slots near buildings

[← Tables and calculations](../README.md)

How many peasants can build a building at the same time? Counted from `collisionmaskproperty.Mask` of each `.prop` file in `data/objects/buildings/` according to a rule empirically consistent with the game.

**Formula** (see [construction and repair](../../recon/world/economy/building_mechanics.md), section about slots):

- For normal buildings - exact bypass of the perimeter `_unit_CalcBuilderPoints` [^1] using the top-left component of the collision mask. For convex shapes, the result is `bbox_cols + bbox_rows` (Manhattan-perimeter); for non-convex (arches, crosses) walker gives more.
- If the mask is **torn into several linear** “support” strips 1×N (warehouses) - the engine behaves as if the bbox union of all the strips is filled with solid material. We use `bbox_cols + bbox_rows` joins (see the “method” column).
- Hard engine limit: `gc_MaxBuilderCount = 30`.

**Empirically confirmed** (peasant score in game):

| sid | prediction | in game | note |
|---|---|---|---|
| `polcen` (Polish GC) | 18 | 18 ✓ | convex rhombus |
| `ruscen` (Russian GC) | 24 | 24 ✓ | convex |
| `swecen` (Swedish GC) | **27** | **27 ✓** | **non-convex** (arch with two legs) |
| `eurmil` (European mill) | 10 | 10 ✓ | convex |
| `rusmil` (Russian mill) | 7 | 7 ✓ | convex |
| `polbla` (Polish forge) | 18 | 18 ✓ | convex |
| `polba2` (Polish barracks 18th century) | 25 | 25 ✓ | convex |
| `tursto` (Turkish warehouse) | 8 | 8 ✓ | walker by large component |
| `spasto` (Spanish warehouse) | 7 | 7 ✓ | walker on large component, orphan ignored (blank left side visible) |
| `russto` (Russian warehouse) | 8 | 8 ✓ | bbox_union rule for linear supports |
| `eursto` (European warehouse) | 9 | 8 | known discrepancy −1 |

**Walker is also correct on non-convex** (`swecen` confirmed this empirically: 27 = walker, not 24 = bbox_perim). Movement along the inner dents of the arch adds +3 slots relative to the convex bbox. A total of 5 single-component non-convex buildings: `scocen` (+4), `swecen` (+3), `portem` (+2), `bavhou` (+1), `ukrtem` (+1) - for them the walker gives more slots than bbox-perim.

**Table columns:**

- `bbox` — dimensions of a rectangle covering all filled cells of the mask (in half-tile cells).
- `cells` - total number of filled cells.
- `components` — the number of unrelated components in the mask (for most = 1).
- `method` - `walker` (exact bypass) or `bbox_union` (rule for linear “supports”).
- `slots` — the total number of simultaneous builders (after cap=30).

**Gates** (`*sga`, `*wga`, `*sga_*`, `*wga_*`) appear as **instant** custom upgrade `gc_upg_type_single_buildgate` on the selected wall segment: the new gate object immediately becomes `bbuilt = True, hp = maxhp` via fast-path `if (bwall) and (upglevel>0) then hp := maxhp` to `_unit_ControlBuildProgress`. Peasants are not involved in the construction of the gate. The slots in the tables below refer to the wall segments themselves and are used to repair them.

<a id="городские-центры-cen"></a>
<a id="городские-центры"></a>
## Town Halls (cen)

| sid | bbox | cells | comp. | method | slots |
|---|---|---:|---:|---|---:|
| `polcen` | 9x9 | 51 | 1 | walker | **18** |
| `netcen` | 11x8 | 49 | 1 | walker | **19** |
| `dencen` | 11x9 | 47 | 1 | walker | **20** |
| `prucen` | 10x10 | 67 | 1 | walker | **20** |
| `algcen` | 11x10 | 67 | 1 | walker | **21** |
| `bavcen` | 11x10 | 57 | 1 | walker | **21** |
| `porcen` | 11x10 | 63 | 1 | walker | **21** |
| `saxcen` | 11x10 | 68 | 1 | walker | **21** |
| `huncen` | 11x11 | 72 | 1 | walker | **22** |
| `turcen` | 12x10 | 75 | 1 | walker | **22** |
| `auscen` | 13x10 | 78 | 1 | walker | **23** |
| `engcen` | 12x11 | 100 | 1 | walker | **23** |
| `swicen` | 12x11 | 77 | 1 | walker | **23** |
| `piecen` | 12x12 | 65 | 1 | walker | **24** |
| `ruscen` | 11x13 | 81 | 1 | walker | **24** |
| `spacen` | 12x12 | 110 | 1 | walker | **24** |
| `fracen` | 14x13 | 108 | 1 | walker | **27** |
| `swecen` | 15x9 | 72 | 1 | walker | **27** |
| `scocen` | 14x10 | 72 | 1 | walker | **28** |
| `vencen` | 15x13 | 111 | 1 | walker | **28** |
| `ukrcen` | 15x14 | 124 | 1 | walker | **29** |

<a id="склады-sto"></a>
<a id="склады"></a>
## Storehouses (sto)

| sid | bbox | cells | comp. | method | slots |
|---|---|---:|---:|---|---:|
| `spasto` | 7x4 | 11 | 2 | walker | **7** |
| `russto` | 5x3 | 5 | 2 | bbox_union | **8** |
| `tursto` | 4x4 | 8 | 1 | walker | **8** |
| `eursto` | 6x3 | 5 | 2 | bbox_union | **9** |

<a id="мельницы-mil"></a>
<a id="мельницы"></a>
## Mills (mil)

| sid | bbox | cells | comp. | method | slots |
|---|---|---:|---:|---|---:|
| `rusmil` | 4x3 | 11 | 1 | walker | **7** |
| `eurmil` | 5x5 | 13 | 1 | walker | **10** |
| `turmil` | 8x8 | 41 | 1 | walker | **16** |

<a id="дома-hou"></a>
<a id="дома"></a>
## Housing (hou)

| sid | bbox | cells | comp. | method | slots |
|---|---|---:|---:|---|---:|
| `frahou` | 5x5 | 17 | 1 | walker | **10** |
| `venhou` | 5x5 | 13 | 1 | walker | **10** |
| `swihou` | 6x5 | 24 | 1 | walker | **11** |
| `pruhou` | 6x6 | 26 | 1 | walker | **12** |
| `denhou` | 7x6 | 25 | 1 | walker | **13** |
| `nethou` | 7x6 | 27 | 1 | walker | **13** |
| `piehou` | 6x7 | 26 | 1 | walker | **13** |
| `porhou` | 6x7 | 25 | 1 | walker | **13** |
| `saxhou` | 7x6 | 29 | 1 | walker | **13** |
| `hunhou` | 7x7 | 29 | 1 | walker | **14** |
| `scohou` | 7x7 | 34 | 1 | walker | **14** |
| `spahou` | 8x6 | 34 | 1 | walker | **14** |
| `turhou` | 7x7 | 31 | 1 | walker | **14** |
| `aushou` | 9x6 | 33 | 1 | walker | **15** |
| `enghou` | 8x7 | 35 | 1 | walker | **15** |
| `swehou` | 8x7 | 27 | 1 | walker | **15** |
| `alghou` | 8x8 | 45 | 1 | walker | **16** |
| `bavhou` | 10x5 | 35 | 1 | walker | **16** |
| `ukrhou` | 8x8 | 45 | 1 | walker | **16** |
| `polhou` | 10x7 | 48 | 1 | walker | **17** |
| `rushou` | 9x8 | 45 | 1 | walker | **17** |

<a id="конюшни-sta"></a>
<a id="конюшни"></a>
## Stables (sta)

| sid | bbox | cells | comp. | method | slots |
|---|---|---:|---:|---|---:|
| `netsta` | 10x8 | 52 | 1 | walker | **18** |
| `swista` | 10x8 | 55 | 1 | walker | **18** |
| `hunsta` | 10x9 | 58 | 1 | walker | **19** |
| `prusta` | 9x10 | 59 | 1 | walker | **19** |
| `saxsta` | 10x9 | 58 | 1 | walker | **19** |
| `vensta` | 10x9 | 57 | 1 | walker | **19** |
| `densta` | 10x10 | 60 | 1 | walker | **20** |
| `scosta` | 10x10 | 61 | 1 | walker | **20** |
| `aussta` | 13x8 | 66 | 1 | walker | **21** |
| `bavsta` | 12x9 | 64 | 1 | walker | **21** |
| `spasta` | 11x10 | 62 | 1 | walker | **21** |
| `swesta` | 12x9 | 71 | 1 | walker | **21** |
| `engsta` | 11x11 | 76 | 1 | walker | **22** |
| `frasta` | 11x11 | 79 | 1 | walker | **22** |
| `russta` | 11x11 | 79 | 1 | walker | **22** |
| `piesta` | 12x12 | 78 | 1 | walker | **24** |
| `porsta` | 13x11 | 78 | 1 | walker | **24** |
| `tursta` | 13x12 | 99 | 1 | walker | **25** |
| `polsta` | 13x13 | 94 | 1 | walker | **26** |
| `ukrsta` | 13x13 | 97 | 1 | walker | **26** |

<a id="базары-mar"></a>
<a id="рынки"></a>
## Markets (mar)

| sid | bbox | cells | comp. | method | slots |
|---|---|---:|---:|---|---:|
| `turmar` | 11x8 | 55 | 1 | walker | **19** |
| `rusmar` | 11x12 | 80 | 1 | walker | **23** |
| `spamar` | 11x13 | 82 | 1 | walker | **24** |
| `eurmar` | 14x11 | 83 | 1 | walker | **25** |

<a id="дипломатические-центры-dip"></a>
<a id="дипломатические-центры"></a>
## Diplomatic centers (dip)

| sid | bbox | cells | comp. | method | slots |
|---|---|---:|---:|---|---:|
| `engdip` | 9x7 | 40 | 1 | walker | **16** |
| `piedip` | 8x8 | 37 | 1 | walker | **16** |
| `poldip` | 8x8 | 45 | 1 | walker | **16** |
| `saxdip` | 8x9 | 40 | 1 | walker | **17** |
| `swedip` | 9x8 | 37 | 1 | walker | **17** |
| `bavdip` | 9x9 | 50 | 1 | walker | **18** |
| `fradip` | 9x9 | 49 | 1 | walker | **18** |
| `hundip` | 9x9 | 53 | 1 | walker | **18** |
| `netdip` | 9x9 | 45 | 1 | walker | **18** |
| `pordip` | 9x9 | 56 | 1 | walker | **18** |
| `rusdip` | 9x9 | 53 | 1 | walker | **18** |
| `swidip` | 9x9 | 44 | 1 | walker | **18** |
| `vendip` | 9x9 | 43 | 1 | walker | **18** |
| `prudip` | 10x9 | 52 | 1 | walker | **19** |
| `scodip` | 10x9 | 49 | 1 | walker | **19** |
| `dendip` | 11x10 | 58 | 1 | walker | **21** |
| `spadip` | 11x10 | 65 | 1 | walker | **21** |
| `turdip` | 12x10 | 71 | 1 | walker | **22** |
| `ukrdip` | 11x11 | 53 | 1 | walker | **22** |
| `ausdip` | 12x12 | 76 | 1 | walker | **24** |

<a id="храмы-tem"></a>
<a id="храмы"></a>
## Temples (tem)

| sid | bbox | cells | comp. | method | slots |
|---|---|---:|---:|---|---:|
| `pietem` | 10x10 | 64 | 1 | walker | **20** |
| `nettem` | 11x10 | 69 | 1 | walker | **21** |
| `switem` | 11x10 | 67 | 1 | walker | **21** |
| `bavtem` | 11x11 | 81 | 1 | walker | **22** |
| `dentem` | 11x11 | 73 | 1 | walker | **22** |
| `poltem` | 11x11 | 91 | 1 | walker | **22** |
| `scotem` | 11x11 | 77 | 1 | walker | **22** |
| `turtem` | 11x11 | 71 | 1 | walker | **22** |
| `swetem` | 12x11 | 75 | 1 | walker | **23** |
| `engtem` | 12x12 | 97 | 1 | walker | **24** |
| `portem` | 12x11 | 85 | 1 | walker | **25** |
| `prutem` | 12x13 | 99 | 1 | walker | **25** |
| `saxtem` | 13x13 | 90 | 1 | walker | **26** |
| `austem` | 15x13 | 134 | 1 | walker | **28** |
| `huntem` | 14x14 | 113 | 1 | walker | **28** |
| `fratem` | 15x15 | 124 | 1 | walker | **30** |
| `rustem` | 16x15 | 156 | 1 | walker | **30** |
| `spatem` | 18x18 | 183 | 1 | walker | **30** |
| `ukrtem` | 21x15 | 173 | 1 | walker | **30** |
| `ventem` | 18x18 | 191 | 1 | walker | **30** |

<a id="казармы-17-в-bar"></a>
<a id="казармы-xvii-века"></a>
## 17th-century Barracks (bar)

| sid | bbox | cells | comp. | method | slots |
|---|---|---:|---:|---|---:|
| `frabar` | 9x7 | 37 | 1 | walker | **16** |
| `prubar` | 9x9 | 52 | 1 | walker | **18** |
| `spabar` | 9x9 | 55 | 1 | walker | **18** |
| `denbar` | 12x8 | 63 | 1 | walker | **20** |
| `netbar` | 11x9 | 66 | 1 | walker | **20** |
| `saxbar` | 10x10 | 67 | 1 | walker | **20** |
| `engbar` | 12x10 | 73 | 1 | walker | **22** |
| `hunbar` | 11x11 | 72 | 1 | walker | **22** |
| `porbar` | 11x11 | 73 | 1 | walker | **22** |
| `turbar` | 11x11 | 84 | 1 | walker | **22** |
| `bavbar` | 12x11 | 68 | 1 | walker | **23** |
| `rusbar` | 11x12 | 73 | 1 | walker | **23** |
| `scobar` | 12x11 | 76 | 1 | walker | **23** |
| `swibar` | 12x11 | 86 | 1 | walker | **23** |
| `ukrbar` | 13x10 | 78 | 1 | walker | **23** |
| `venbar` | 11x12 | 81 | 1 | walker | **23** |
| `piebar` | 12x12 | 68 | 1 | walker | **24** |
| `ausbar` | 13x12 | 90 | 1 | walker | **25** |
| `swebar` | 13x12 | 96 | 1 | walker | **25** |
| `polbar` | 14x13 | 113 | 1 | walker | **27** |

<a id="казармы-18-в-ba2"></a>
<a id="казармы-xviii-века"></a>
## 18th-century Barracks (ba2)

| sid | bbox | cells | comp. | method | slots |
|---|---|---:|---:|---|---:|
| `venba2` | 10x9 | 58 | 1 | walker | **19** |
| `saxba2` | 11x9 | 59 | 1 | walker | **20** |
| `netba2` | 11x10 | 69 | 1 | walker | **21** |
| `denba2` | 11x11 | 63 | 1 | walker | **22** |
| `pieba2` | 11x11 | 65 | 1 | walker | **22** |
| `pruba2` | 11x11 | 91 | 1 | walker | **22** |
| `swiba2` | 11x11 | 63 | 1 | walker | **22** |
| `bavba2` | 12x11 | 73 | 1 | walker | **23** |
| `engba2` | 12x11 | 65 | 1 | walker | **23** |
| `porba2` | 12x12 | 86 | 1 | walker | **24** |
| `polba2` | 13x12 | 87 | 1 | walker | **25** |
| `hunba2` | 13x13 | 101 | 1 | walker | **26** |
| `spaba2` | 13x13 | 103 | 1 | walker | **26** |
| `sweba2` | 14x13 | 108 | 1 | walker | **27** |
| `ausba2` | 15x14 | 129 | 1 | walker | **29** |
| `fraba2` | 15x14 | 112 | 1 | walker | **29** |
| `rusba2` | 16x16 | 133 | 1 | walker | **30** |
| `scoba2` | 15x15 | 123 | 1 | walker | **30** |

<a id="кузницы-bla"></a>
<a id="кузницы"></a>
## Blacksmiths (bla)

| sid | bbox | cells | comp. | method | slots |
|---|---|---:|---:|---|---:|
| `frabla` | 6x7 | 23 | 1 | walker | **13** |
| `hunbla` | 6x7 | 28 | 1 | walker | **13** |
| `spabla` | 7x6 | 24 | 1 | walker | **13** |
| `netbla` | 8x6 | 37 | 1 | walker | **14** |
| `prubla` | 8x6 | 29 | 1 | walker | **14** |
| `saxbla` | 8x6 | 32 | 1 | walker | **14** |
| `porbla` | 9x6 | 35 | 1 | walker | **15** |
| `rusbla` | 8x7 | 38 | 1 | walker | **15** |
| `turbla` | 8x7 | 45 | 1 | walker | **15** |
| `bavbla` | 9x7 | 38 | 1 | walker | **16** |
| `denbla` | 9x7 | 33 | 1 | walker | **16** |
| `engbla` | 9x7 | 38 | 1 | walker | **16** |
| `piebla` | 9x7 | 41 | 1 | walker | **16** |
| `scobla` | 9x7 | 32 | 1 | walker | **16** |
| `swebla` | 10x6 | 47 | 1 | walker | **16** |
| `venbla` | 8x8 | 43 | 1 | walker | **16** |
| `ausbla` | 10x7 | 41 | 1 | walker | **17** |
| `swibla` | 8x9 | 48 | 1 | walker | **17** |
| `polbla` | 10x8 | 48 | 1 | walker | **18** |
| `ukrbla` | 10x9 | 54 | 1 | walker | **19** |

<a id="академии-aca"></a>
<a id="академии"></a>
## Academies (aca)

| sid | bbox | cells | comp. | method | slots |
|---|---|---:|---:|---|---:|
| `turaca` | 3x3 | 9 | 1 | walker | **6** |
| `poraca` | 8x8 | 41 | 1 | walker | **16** |
| `denaca` | 9x8 | 47 | 1 | walker | **17** |
| `netaca` | 9x9 | 39 | 1 | walker | **18** |
| `polaca` | 9x9 | 51 | 1 | walker | **18** |
| `pruaca` | 10x8 | 50 | 1 | walker | **18** |
| `sweaca` | 9x9 | 49 | 1 | walker | **18** |
| `hunaca` | 10x9 | 56 | 1 | walker | **19** |
| `saxaca` | 10x9 | 56 | 1 | walker | **19** |
| `scoaca` | 11x9 | 58 | 1 | walker | **20** |
| `bavaca` | 13x9 | 68 | 1 | walker | **22** |
| `pieaca` | 11x11 | 79 | 1 | walker | **22** |
| `swiaca` | 11x11 | 71 | 1 | walker | **22** |
| `venaca` | 11x11 | 59 | 1 | walker | **22** |
| `engaca` | 12x11 | 76 | 1 | walker | **23** |
| `fraaca` | 13x11 | 65 | 1 | walker | **24** |
| `rusaca` | 12x13 | 80 | 1 | walker | **25** |
| `ausaca` | 13x13 | 67 | 1 | walker | **26** |
| `spaaca` | 13x13 | 97 | 1 | walker | **26** |
| `ukraca` | 17x17 | 121 | 1 | walker | **30** |

<a id="артиллерийские-депо-art"></a>
<a id="артиллерийские-депо"></a>
## Artillery depots (art)

| sid | bbox | cells | comp. | method | slots |
|---|---|---:|---:|---|---:|
| `hunart` | 10x8 | 55 | 1 | walker | **18** |
| `pieart` | 11x8 | 62 | 1 | walker | **19** |
| `polart` | 10x9 | 65 | 1 | walker | **19** |
| `saxart` | 10x9 | 54 | 1 | walker | **19** |
| `bavart` | 11x9 | 61 | 1 | walker | **20** |
| `denart` | 12x8 | 58 | 1 | walker | **20** |
| `netart` | 11x9 | 62 | 1 | walker | **20** |
| `sweart` | 11x9 | 56 | 1 | walker | **20** |
| `swiart` | 11x9 | 66 | 1 | walker | **20** |
| `venart` | 11x9 | 71 | 1 | walker | **20** |
| `scoart` | 12x9 | 59 | 1 | walker | **21** |
| `ausart` | 12x10 | 71 | 1 | walker | **22** |
| `engart` | 12x10 | 66 | 1 | walker | **22** |
| `porart` | 12x10 | 63 | 1 | walker | **22** |
| `pruart` | 11x11 | 68 | 1 | walker | **22** |
| `spaart` | 11x12 | 90 | 1 | walker | **23** |
| `fraart` | 12x12 | 85 | 1 | walker | **24** |
| `rusart` | 14x10 | 75 | 1 | walker | **24** |
| `turart` | 14x14 | 110 | 1 | walker | **28** |
| `ukrart` | 17x14 | 141 | 1 | walker | **30** |

<a id="порты-por"></a>
<a id="порты"></a>
## Shipyards (por)

| sid | bbox | cells | comp. | method | slots |
|---|---|---:|---:|---|---:|
| `porpor` | 10x11 | 80 | 1 | walker | **21** |
| `ruspor` | 14x13 | 124 | 1 | walker | **27** |
| `eurpor` | 14x16 | 129 | 1 | walker | **30** |
| `turpor` | 16x14 | 146 | 1 | walker | **30** |
| `ukrpor` | 15x21 | 188 | 1 | walker | **30** |

<a id="башни-tow"></a>
<a id="башни"></a>
## Towers (tow)

| sid | bbox | cells | comp. | method | slots |
|---|---|---:|---:|---|---:|
| `eurtow` | 5x5 | 21 | 1 | walker | **10** |
| `rustow` | 5x5 | 21 | 1 | walker | **10** |
| `turtow` | 7x7 | 37 | 1 | walker | **14** |

<a id="шахты-golirocoa"></a>
<a id="шахты"></a>
## Mines (gol/iro/coa)

| sid | bbox | cells | comp. | method | slots |
|---|---|---:|---:|---|---:|
| `eurgol` | 8x8 | 52 | 1 | walker | **16** |
| `euriro` | 8x8 | 52 | 1 | walker | **16** |
| `eurcoa` | 8x8 | 52 | 1 | walker | **16** |

<a id="стены-swawwa"></a>
<a id="стены"></a>
## Walls (swa/wwa)

| sid | bbox | cells | comp. | method | slots |
|---|---|---:|---:|---|---:|
| `eurswa` | 2x2 | 4 | 1 | walker | **4** |
| `russwa` | 2x2 | 4 | 1 | walker | **4** |
| `turswa` | 2x2 | 4 | 1 | walker | **4** |
| `ukrwwa` | 2x2 | 4 | 1 | walker | **4** |
| `eurwwa` | 6x7 | 30 | 1 | walker | **13** |

<a id="ворота-sgawga"></a>
<a id="ворота"></a>
## Gate (sga/wga)

| sid | bbox | cells | comp. | method | slots |
|---|---|---:|---:|---|---:|
| `eursga` | 6x7 | 30 | 1 | walker | **13** |
| `eurwga` | 6x7 | 30 | 1 | walker | **13** |

<a id="прочие-миссиисегменты-стенмосты"></a>
## Other (missions/wall segments/bridges)

| sid | bbox | cells | comp. | method | slots |
|---|---|---:|---:|---|---:|
| `eursga_14` | 6x2 | 4 | 2 | bbox_union | **8** |
| `eursga_15` | 2x6 | 4 | 2 | bbox_union | **8** |
| `eursga_16` | 8x8 | 22 | 2 | walker | **7** |
| `eursga_17` | 8x9 | 24 | 2 | walker | **8** |
| `eurswa_01` | 2x2 | 4 | 1 | walker | **4** |
| `eurswa_02` | 2x2 | 4 | 1 | walker | **4** |
| `eurswa_03` | 4x4 | 8 | 1 | walker | **8** |
| `eurswa_04` | 4x4 | 8 | 1 | walker | **8** |
| `eurswa_05` | 2x2 | 4 | 1 | walker | **4** |
| `eurswa_06` | 3x3 | 6 | 1 | walker | **6** |
| `eurswa_07` | 3x3 | 6 | 1 | walker | **6** |
| `eurswa_08` | 3x3 | 6 | 1 | walker | **6** |
| `eurswa_09` | 3x3 | 6 | 1 | walker | **6** |
| `eurswa_10` | 3x3 | 6 | 1 | walker | **6** |
| `eurswa_11` | 3x3 | 6 | 1 | walker | **6** |
| `eurswa_12` | 3x3 | 6 | 1 | walker | **6** |
| `eurswa_13` | 3x3 | 6 | 1 | walker | **6** |
| `eurswa_45gate` | 2x2 | 4 | 1 | walker | **4** |
| `eurswa_45v1` | 2x2 | 4 | 1 | walker | **4** |
| `eurswa_45v2` | 2x2 | 4 | 1 | walker | **4** |
| `eurswa_gate` | 2x2 | 4 | 1 | walker | **4** |
| `eurswa_tower` | 2x2 | 4 | 1 | walker | **4** |
| `eurswa_turn` | 2x2 | 4 | 1 | walker | **4** |
| `eurswa_turnmirror` | 2x2 | 4 | 1 | walker | **4** |
| `eurswa_v1` | 2x2 | 4 | 1 | walker | **4** |
| `eurswa_v2` | 2x2 | 4 | 1 | walker | **4** |
| `g_45left` | 2x2 | 4 | 1 | walker | **4** |
| `g_45right` | 2x2 | 4 | 1 | walker | **4** |
| `misblg` | 8x8 | 35 | 1 | walker | **16** |
| `misblg2` | 8x8 | 33 | 1 | walker | **16** |
| `misbridge1` | 2x2 | 4 | 1 | walker | **4** |
| `misbridge1a` | 2x2 | 4 | 1 | walker | **4** |
| `misbridge2` | 2x2 | 4 | 1 | walker | **4** |
| `misbridge2a` | 2x2 | 4 | 1 | walker | **4** |
| `misbridge3` | 2x2 | 4 | 1 | walker | **4** |
| `misbridge3a` | 2x2 | 4 | 1 | walker | **4** |
| `misbridge4` | 2x2 | 4 | 1 | walker | **4** |
| `misbridge4a` | 2x2 | 4 | 1 | walker | **4** |
| `miscauldron` | 2x2 | 3 | 1 | walker | **4** |
| `mischest1` | 2x3 | 4 | 1 | walker | **5** |
| `mischest2` | 2x2 | 3 | 1 | walker | **4** |
| `miscommandcenter` | 18x13 | 125 | 1 | walker | **30** |
| `mistent` | 12x8 | 47 | 1 | walker | **20** |
| `miswel1` | 2x2 | 4 | 1 | walker | **4** |
| `miswel2` | 3x2 | 6 | 1 | walker | **5** |
| `miswel3` | 2x3 | 4 | 1 | walker | **5** |
| `misyurt` | 6×8 | 31 | 1 | walker | **14** |
| `russga_14` | 6×2 | 4 | 2 | bbox_union | **8** |
| `russga_15` | 2×6 | 4 | 2 | bbox_union | **8** |
| `russga_16` | 8×8 | 22 | 2 | walker | **7** |
| `russga_17` | 8×9 | 24 | 2 | walker | **8** |
| `russwa_01` | 2×2 | 4 | 1 | walker | **4** |
| `russwa_02` | 2×2 | 4 | 1 | walker | **4** |
| `russwa_03` | 4×4 | 8 | 1 | walker | **8** |
| `russwa_04` | 4×4 | 8 | 1 | walker | **8** |
| `russwa_05` | 2×2 | 4 | 1 | walker | **4** |
| `russwa_06` | 3×3 | 6 | 1 | walker | **6** |
| `russwa_07` | 3×3 | 6 | 1 | walker | **6** |
| `russwa_08` | 3×3 | 6 | 1 | walker | **6** |
| `russwa_09` | 3×3 | 6 | 1 | walker | **6** |
| `russwa_10` | 3×3 | 6 | 1 | walker | **6** |
| `russwa_11` | 3×3 | 6 | 1 | walker | **6** |
| `russwa_12` | 3×3 | 6 | 1 | walker | **6** |
| `russwa_13` | 3×3 | 6 | 1 | walker | **6** |
| `russwa_45gate` | 2×2 | 4 | 1 | walker | **4** |
| `russwa_45v1` | 2×2 | 4 | 1 | walker | **4** |
| `russwa_45v2` | 2×2 | 4 | 1 | walker | **4** |
| `russwa_gate` | 2×2 | 4 | 1 | walker | **4** |
| `russwa_tower` | 2×2 | 4 | 1 | walker | **4** |
| `russwa_turn` | 2×2 | 4 | 1 | walker | **4** |
| `russwa_turnmirror` | 2×2 | 4 | 1 | walker | **4** |
| `russwa_v1` | 2×2 | 4 | 1 | walker | **4** |
| `russwa_v2` | 2×2 | 4 | 1 | walker | **4** |
| `tursga_14` | 6×2 | 4 | 2 | bbox_union | **8** |
| `tursga_15` | 2×6 | 4 | 2 | bbox_union | **8** |
| `tursga_16` | 8×8 | 22 | 2 | walker | **7** |
| `tursga_17` | 8×9 | 24 | 2 | walker | **8** |
| `turswa_01` | 2×2 | 4 | 1 | walker | **4** |
| `turswa_02` | 2×2 | 4 | 1 | walker | **4** |
| `turswa_03` | 4×4 | 8 | 1 | walker | **8** |
| `turswa_04` | 4×4 | 8 | 1 | walker | **8** |
| `turswa_05` | 2×2 | 4 | 1 | walker | **4** |
| `turswa_06` | 3×3 | 6 | 1 | walker | **6** |
| `turswa_07` | 3×3 | 6 | 1 | walker | **6** |
| `turswa_08` | 3×3 | 6 | 1 | walker | **6** |
| `turswa_09` | 3×3 | 6 | 1 | walker | **6** |
| `turswa_10` | 3×3 | 6 | 1 | walker | **6** |
| `turswa_11` | 3×3 | 6 | 1 | walker | **6** |
| `turswa_12` | 3×3 | 6 | 1 | walker | **6** |
| `turswa_13` | 3×3 | 6 | 1 | walker | **6** |
| `turswa_45gate` | 2×2 | 4 | 1 | walker | **4** |
| `turswa_45v1` | 2×2 | 4 | 1 | walker | **4** |
| `turswa_45v2` | 2×2 | 4 | 1 | walker | **4** |
| `turswa_gate` | 2×2 | 4 | 1 | walker | **4** |
| `turswa_tower` | 2×2 | 4 | 1 | walker | **4** |
| `turswa_turn` | 2×2 | 4 | 1 | walker | **4** |
| `turswa_turnmirror` | 2×2 | 4 | 1 | walker | **4** |
| `turswa_v1` | 2×2 | 4 | 1 | walker | **4** |
| `turswa_v2` | 2×2 | 4 | 1 | walker | **4** |
| `ukrwga_14` | 6×2 | 4 | 2 | bbox_union | **8** |
| `ukrwga_15` | 2×6 | 4 | 2 | bbox_union | **8** |
| `ukrwga_16` | 8×16 | 28 | 4 | walker | **6** |
| `ukrwga_17` | 8×8 | 11 | 2 | walker | **6** |
| `ukrwwa_01` | 2×2 | 4 | 1 | walker | **4** |
| `ukrwwa_02` | 2×2 | 4 | 1 | walker | **4** |
| `ukrwwa_03` | 4×4 | 8 | 1 | walker | **8** |
| `ukrwwa_04` | 4×4 | 8 | 1 | walker | **8** |
| `ukrwwa_05` | 2×2 | 4 | 1 | walker | **4** |
| `ukrwwa_06` | 3×3 | 6 | 1 | walker | **6** |
| `ukrwwa_07` | 3×3 | 6 | 1 | walker | **6** |
| `ukrwwa_08` | 3×3 | 6 | 1 | walker | **6** |
| `ukrwwa_09` | 3×3 | 6 | 1 | walker | **6** |
| `ukrwwa_10` | 3×3 | 6 | 1 | walker | **6** |
| `ukrwwa_11` | 3×3 | 6 | 1 | walker | **6** |
| `ukrwwa_12` | 3×3 | 6 | 1 | walker | **6** |
| `ukrwwa_13` | 3×3 | 6 | 1 | walker | **6** |
| `ukrwwa_45gate` | 2×2 | 4 | 1 | walker | **4** |
| `ukrwwa_45v1` | 2×2 | 4 | 1 | walker | **4** |
| `ukrwwa_45v2` | 2×2 | 4 | 1 | walker | **4** |
| `ukrwwa_gate` | 2×2 | 4 | 1 | walker | **4** |
| `ukrwwa_tower` | 2x2 | 4 | 1 | walker | **4** |
| `ukrwwa_turn` | 2x2 | 4 | 1 | walker | **4** |
| `ukrwwa_turnmirror` | 2x2 | 4 | 1 | walker | **4** |
| `ukrwwa_v1` | 2x2 | 4 | 1 | walker | **4** |
| `ukrwwa_v2` | 2x2 | 4 | 1 | walker | **4** |


<a id="источники"></a>
## Sources

All links are relative to `data/scripts/` in the Cossacks 3 installation.

[^1]: `_unit_CalcBuilderPoints` - `lib/unit.script:8702-9006`.
