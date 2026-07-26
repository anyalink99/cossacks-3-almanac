# Cossacks 3 — Слоты строителей у зданий

Сколько крестьян могут одновременно строить здание. Считается из `collisionmaskproperty.Mask` каждого `.prop` файла в `data/objects/buildings/` по правилу, эмпирически согласованному с игрой.

**Формула** (см. [`recon/world/economy/building_mechanics.md`](../../recon/world/economy/building_mechanics.md), раздел про слоты):

- Для нормальных зданий — точный обход периметра `_unit_CalcBuilderPoints` [^1] по верхне-левой компоненте collision mask. Для выпуклых форм результат равен `bbox_cols + bbox_rows` (Manhattan-периметр); для non-convex (арки, кресты) walker даёт больше.
- Если маска **разорвана на несколько линейных** «опорных» планок 1×N (склады) — движок ведёт себя так, будто bbox-объединение всех планок заполнено сплошняком. Используем `bbox_cols + bbox_rows` объединения (см. колонку «метод»).
- Жёсткий лимит движка: `gc_MaxBuilderCount = 30`.

**Эмпирически подтверждено** (счёт крестьян в игре):

| sid | предсказание | в игре | примечание |
|---|---|---|---|
| `polcen` (польский ГЦ) | 18 | 18 ✓ | выпуклый ромб |
| `ruscen` (русский ГЦ) | 24 | 24 ✓ | выпуклый |
| `swecen` (шведский ГЦ) | **27** | **27 ✓** | **non-convex** (арка с двумя ногами) |
| `eurmil` (европейская мельница) | 10 | 10 ✓ | выпуклый |
| `rusmil` (русская мельница) | 7 | 7 ✓ | выпуклый |
| `polbla` (польская кузница) | 18 | 18 ✓ | выпуклый |
| `polba2` (польская казарма 18 в.) | 25 | 25 ✓ | выпуклый |
| `tursto` (турецкий склад) | 8 | 8 ✓ | walker по большой компоненте |
| `spasto` (испанский склад) | 7 | 7 ✓ | walker по большой компоненте, орфан игнорируется (видна пустая левая сторона) |
| `russto` (русский склад) | 8 | 8 ✓ | правило bbox_union для линейных опор |
| `eursto` (европейский склад) | 9 | 8 | известное расхождение −1 |

**Walker корректен и на non-convex** (`swecen` подтвердил это эмпирически: 27 = walker, не 24 = bbox_perim). Movement по внутренним вмятинам арки добавляет +3 слота относительно выпуклого bbox. Всего 5 single-component non-convex зданий: `scocen` (+4), `swecen` (+3), `portem` (+2), `bavhou` (+1), `ukrtem` (+1) — для них walker даёт больше слотов, чем bbox-perim.

**Колонки таблиц:**

- `bbox` — размеры прямоугольника, охватывающего все заполненные ячейки маски (в half-tile клетках).
- `cells` — общее число заполненных ячеек.
- `комп.` — число несвязанных компонент в маске (для большинства = 1).
- `метод` — `walker` (точный обход) или `bbox_union` (правило для линейных «опор»).
- `слоты` — итоговое число одновременных строителей (после cap=30).

**Ворота** (`*sga`, `*wga`, `*sga_*`, `*wga_*`) появляются как **моментальный** индивидуальный апгрейд `gc_upg_type_single_buildgate` на выбранном сегменте стены: новый объект ворот сразу становится `bbuilt = True, hp = maxhp` через fast-path `if (bwall) and (upglevel>0) then hp := maxhp` в `_unit_ControlBuildProgress`. Крестьяне в постройку ворот не вовлечены. Слоты в таблицах ниже относятся к самим сегментам стены и используются для их ремонта.

## Городские центры (cen)

| sid | bbox | cells | комп. | метод | слоты |
|---|---|---:|---:|---|---:|
| `polcen` | 9×9 | 51 | 1 | walker | **18** |
| `netcen` | 11×8 | 49 | 1 | walker | **19** |
| `dencen` | 11×9 | 47 | 1 | walker | **20** |
| `prucen` | 10×10 | 67 | 1 | walker | **20** |
| `algcen` | 11×10 | 67 | 1 | walker | **21** |
| `bavcen` | 11×10 | 57 | 1 | walker | **21** |
| `porcen` | 11×10 | 63 | 1 | walker | **21** |
| `saxcen` | 11×10 | 68 | 1 | walker | **21** |
| `huncen` | 11×11 | 72 | 1 | walker | **22** |
| `turcen` | 12×10 | 75 | 1 | walker | **22** |
| `auscen` | 13×10 | 78 | 1 | walker | **23** |
| `engcen` | 12×11 | 100 | 1 | walker | **23** |
| `swicen` | 12×11 | 77 | 1 | walker | **23** |
| `piecen` | 12×12 | 65 | 1 | walker | **24** |
| `ruscen` | 11×13 | 81 | 1 | walker | **24** |
| `spacen` | 12×12 | 110 | 1 | walker | **24** |
| `fracen` | 14×13 | 108 | 1 | walker | **27** |
| `swecen` | 15×9 | 72 | 1 | walker | **27** |
| `scocen` | 14×10 | 72 | 1 | walker | **28** |
| `vencen` | 15×13 | 111 | 1 | walker | **28** |
| `ukrcen` | 15×14 | 124 | 1 | walker | **29** |

## Склады (sto)

| sid | bbox | cells | комп. | метод | слоты |
|---|---|---:|---:|---|---:|
| `spasto` | 7×4 | 11 | 2 | walker | **7** |
| `russto` | 5×3 | 5 | 2 | bbox_union | **8** |
| `tursto` | 4×4 | 8 | 1 | walker | **8** |
| `eursto` | 6×3 | 5 | 2 | bbox_union | **9** |

## Мельницы (mil)

| sid | bbox | cells | комп. | метод | слоты |
|---|---|---:|---:|---|---:|
| `rusmil` | 4×3 | 11 | 1 | walker | **7** |
| `eurmil` | 5×5 | 13 | 1 | walker | **10** |
| `turmil` | 8×8 | 41 | 1 | walker | **16** |

## Дома (hou)

| sid | bbox | cells | комп. | метод | слоты |
|---|---|---:|---:|---|---:|
| `frahou` | 5×5 | 17 | 1 | walker | **10** |
| `venhou` | 5×5 | 13 | 1 | walker | **10** |
| `swihou` | 6×5 | 24 | 1 | walker | **11** |
| `pruhou` | 6×6 | 26 | 1 | walker | **12** |
| `denhou` | 7×6 | 25 | 1 | walker | **13** |
| `nethou` | 7×6 | 27 | 1 | walker | **13** |
| `piehou` | 6×7 | 26 | 1 | walker | **13** |
| `porhou` | 6×7 | 25 | 1 | walker | **13** |
| `saxhou` | 7×6 | 29 | 1 | walker | **13** |
| `hunhou` | 7×7 | 29 | 1 | walker | **14** |
| `scohou` | 7×7 | 34 | 1 | walker | **14** |
| `spahou` | 8×6 | 34 | 1 | walker | **14** |
| `turhou` | 7×7 | 31 | 1 | walker | **14** |
| `aushou` | 9×6 | 33 | 1 | walker | **15** |
| `enghou` | 8×7 | 35 | 1 | walker | **15** |
| `swehou` | 8×7 | 27 | 1 | walker | **15** |
| `alghou` | 8×8 | 45 | 1 | walker | **16** |
| `bavhou` | 10×5 | 35 | 1 | walker | **16** |
| `ukrhou` | 8×8 | 45 | 1 | walker | **16** |
| `polhou` | 10×7 | 48 | 1 | walker | **17** |
| `rushou` | 9×8 | 45 | 1 | walker | **17** |

## Конюшни (sta)

| sid | bbox | cells | комп. | метод | слоты |
|---|---|---:|---:|---|---:|
| `netsta` | 10×8 | 52 | 1 | walker | **18** |
| `swista` | 10×8 | 55 | 1 | walker | **18** |
| `hunsta` | 10×9 | 58 | 1 | walker | **19** |
| `prusta` | 9×10 | 59 | 1 | walker | **19** |
| `saxsta` | 10×9 | 58 | 1 | walker | **19** |
| `vensta` | 10×9 | 57 | 1 | walker | **19** |
| `densta` | 10×10 | 60 | 1 | walker | **20** |
| `scosta` | 10×10 | 61 | 1 | walker | **20** |
| `aussta` | 13×8 | 66 | 1 | walker | **21** |
| `bavsta` | 12×9 | 64 | 1 | walker | **21** |
| `spasta` | 11×10 | 62 | 1 | walker | **21** |
| `swesta` | 12×9 | 71 | 1 | walker | **21** |
| `engsta` | 11×11 | 76 | 1 | walker | **22** |
| `frasta` | 11×11 | 79 | 1 | walker | **22** |
| `russta` | 11×11 | 79 | 1 | walker | **22** |
| `piesta` | 12×12 | 78 | 1 | walker | **24** |
| `porsta` | 13×11 | 78 | 1 | walker | **24** |
| `tursta` | 13×12 | 99 | 1 | walker | **25** |
| `polsta` | 13×13 | 94 | 1 | walker | **26** |
| `ukrsta` | 13×13 | 97 | 1 | walker | **26** |

## Базары (mar)

| sid | bbox | cells | комп. | метод | слоты |
|---|---|---:|---:|---|---:|
| `turmar` | 11×8 | 55 | 1 | walker | **19** |
| `rusmar` | 11×12 | 80 | 1 | walker | **23** |
| `spamar` | 11×13 | 82 | 1 | walker | **24** |
| `eurmar` | 14×11 | 83 | 1 | walker | **25** |

## Дипломатические центры (dip)

| sid | bbox | cells | комп. | метод | слоты |
|---|---|---:|---:|---|---:|
| `engdip` | 9×7 | 40 | 1 | walker | **16** |
| `piedip` | 8×8 | 37 | 1 | walker | **16** |
| `poldip` | 8×8 | 45 | 1 | walker | **16** |
| `saxdip` | 8×9 | 40 | 1 | walker | **17** |
| `swedip` | 9×8 | 37 | 1 | walker | **17** |
| `bavdip` | 9×9 | 50 | 1 | walker | **18** |
| `fradip` | 9×9 | 49 | 1 | walker | **18** |
| `hundip` | 9×9 | 53 | 1 | walker | **18** |
| `netdip` | 9×9 | 45 | 1 | walker | **18** |
| `pordip` | 9×9 | 56 | 1 | walker | **18** |
| `rusdip` | 9×9 | 53 | 1 | walker | **18** |
| `swidip` | 9×9 | 44 | 1 | walker | **18** |
| `vendip` | 9×9 | 43 | 1 | walker | **18** |
| `prudip` | 10×9 | 52 | 1 | walker | **19** |
| `scodip` | 10×9 | 49 | 1 | walker | **19** |
| `dendip` | 11×10 | 58 | 1 | walker | **21** |
| `spadip` | 11×10 | 65 | 1 | walker | **21** |
| `turdip` | 12×10 | 71 | 1 | walker | **22** |
| `ukrdip` | 11×11 | 53 | 1 | walker | **22** |
| `ausdip` | 12×12 | 76 | 1 | walker | **24** |

## Храмы (tem)

| sid | bbox | cells | комп. | метод | слоты |
|---|---|---:|---:|---|---:|
| `pietem` | 10×10 | 64 | 1 | walker | **20** |
| `nettem` | 11×10 | 69 | 1 | walker | **21** |
| `switem` | 11×10 | 67 | 1 | walker | **21** |
| `bavtem` | 11×11 | 81 | 1 | walker | **22** |
| `dentem` | 11×11 | 73 | 1 | walker | **22** |
| `poltem` | 11×11 | 91 | 1 | walker | **22** |
| `scotem` | 11×11 | 77 | 1 | walker | **22** |
| `turtem` | 11×11 | 71 | 1 | walker | **22** |
| `swetem` | 12×11 | 75 | 1 | walker | **23** |
| `engtem` | 12×12 | 97 | 1 | walker | **24** |
| `portem` | 12×11 | 85 | 1 | walker | **25** |
| `prutem` | 12×13 | 99 | 1 | walker | **25** |
| `saxtem` | 13×13 | 90 | 1 | walker | **26** |
| `austem` | 15×13 | 134 | 1 | walker | **28** |
| `huntem` | 14×14 | 113 | 1 | walker | **28** |
| `fratem` | 15×15 | 124 | 1 | walker | **30** |
| `rustem` | 16×15 | 156 | 1 | walker | **30** |
| `spatem` | 18×18 | 183 | 1 | walker | **30** |
| `ukrtem` | 21×15 | 173 | 1 | walker | **30** |
| `ventem` | 18×18 | 191 | 1 | walker | **30** |

## Казармы 17 в. (bar)

| sid | bbox | cells | комп. | метод | слоты |
|---|---|---:|---:|---|---:|
| `frabar` | 9×7 | 37 | 1 | walker | **16** |
| `prubar` | 9×9 | 52 | 1 | walker | **18** |
| `spabar` | 9×9 | 55 | 1 | walker | **18** |
| `denbar` | 12×8 | 63 | 1 | walker | **20** |
| `netbar` | 11×9 | 66 | 1 | walker | **20** |
| `saxbar` | 10×10 | 67 | 1 | walker | **20** |
| `engbar` | 12×10 | 73 | 1 | walker | **22** |
| `hunbar` | 11×11 | 72 | 1 | walker | **22** |
| `porbar` | 11×11 | 73 | 1 | walker | **22** |
| `turbar` | 11×11 | 84 | 1 | walker | **22** |
| `bavbar` | 12×11 | 68 | 1 | walker | **23** |
| `rusbar` | 11×12 | 73 | 1 | walker | **23** |
| `scobar` | 12×11 | 76 | 1 | walker | **23** |
| `swibar` | 12×11 | 86 | 1 | walker | **23** |
| `ukrbar` | 13×10 | 78 | 1 | walker | **23** |
| `venbar` | 11×12 | 81 | 1 | walker | **23** |
| `piebar` | 12×12 | 68 | 1 | walker | **24** |
| `ausbar` | 13×12 | 90 | 1 | walker | **25** |
| `swebar` | 13×12 | 96 | 1 | walker | **25** |
| `polbar` | 14×13 | 113 | 1 | walker | **27** |

## Казармы 18 в. (ba2)

| sid | bbox | cells | комп. | метод | слоты |
|---|---|---:|---:|---|---:|
| `venba2` | 10×9 | 58 | 1 | walker | **19** |
| `saxba2` | 11×9 | 59 | 1 | walker | **20** |
| `netba2` | 11×10 | 69 | 1 | walker | **21** |
| `denba2` | 11×11 | 63 | 1 | walker | **22** |
| `pieba2` | 11×11 | 65 | 1 | walker | **22** |
| `pruba2` | 11×11 | 91 | 1 | walker | **22** |
| `swiba2` | 11×11 | 63 | 1 | walker | **22** |
| `bavba2` | 12×11 | 73 | 1 | walker | **23** |
| `engba2` | 12×11 | 65 | 1 | walker | **23** |
| `porba2` | 12×12 | 86 | 1 | walker | **24** |
| `polba2` | 13×12 | 87 | 1 | walker | **25** |
| `hunba2` | 13×13 | 101 | 1 | walker | **26** |
| `spaba2` | 13×13 | 103 | 1 | walker | **26** |
| `sweba2` | 14×13 | 108 | 1 | walker | **27** |
| `ausba2` | 15×14 | 129 | 1 | walker | **29** |
| `fraba2` | 15×14 | 112 | 1 | walker | **29** |
| `rusba2` | 16×16 | 133 | 1 | walker | **30** |
| `scoba2` | 15×15 | 123 | 1 | walker | **30** |

## Кузницы (bla)

| sid | bbox | cells | комп. | метод | слоты |
|---|---|---:|---:|---|---:|
| `frabla` | 6×7 | 23 | 1 | walker | **13** |
| `hunbla` | 6×7 | 28 | 1 | walker | **13** |
| `spabla` | 7×6 | 24 | 1 | walker | **13** |
| `netbla` | 8×6 | 37 | 1 | walker | **14** |
| `prubla` | 8×6 | 29 | 1 | walker | **14** |
| `saxbla` | 8×6 | 32 | 1 | walker | **14** |
| `porbla` | 9×6 | 35 | 1 | walker | **15** |
| `rusbla` | 8×7 | 38 | 1 | walker | **15** |
| `turbla` | 8×7 | 45 | 1 | walker | **15** |
| `bavbla` | 9×7 | 38 | 1 | walker | **16** |
| `denbla` | 9×7 | 33 | 1 | walker | **16** |
| `engbla` | 9×7 | 38 | 1 | walker | **16** |
| `piebla` | 9×7 | 41 | 1 | walker | **16** |
| `scobla` | 9×7 | 32 | 1 | walker | **16** |
| `swebla` | 10×6 | 47 | 1 | walker | **16** |
| `venbla` | 8×8 | 43 | 1 | walker | **16** |
| `ausbla` | 10×7 | 41 | 1 | walker | **17** |
| `swibla` | 8×9 | 48 | 1 | walker | **17** |
| `polbla` | 10×8 | 48 | 1 | walker | **18** |
| `ukrbla` | 10×9 | 54 | 1 | walker | **19** |

## Академии (aca)

| sid | bbox | cells | комп. | метод | слоты |
|---|---|---:|---:|---|---:|
| `turaca` | 3×3 | 9 | 1 | walker | **6** |
| `poraca` | 8×8 | 41 | 1 | walker | **16** |
| `denaca` | 9×8 | 47 | 1 | walker | **17** |
| `netaca` | 9×9 | 39 | 1 | walker | **18** |
| `polaca` | 9×9 | 51 | 1 | walker | **18** |
| `pruaca` | 10×8 | 50 | 1 | walker | **18** |
| `sweaca` | 9×9 | 49 | 1 | walker | **18** |
| `hunaca` | 10×9 | 56 | 1 | walker | **19** |
| `saxaca` | 10×9 | 56 | 1 | walker | **19** |
| `scoaca` | 11×9 | 58 | 1 | walker | **20** |
| `bavaca` | 13×9 | 68 | 1 | walker | **22** |
| `pieaca` | 11×11 | 79 | 1 | walker | **22** |
| `swiaca` | 11×11 | 71 | 1 | walker | **22** |
| `venaca` | 11×11 | 59 | 1 | walker | **22** |
| `engaca` | 12×11 | 76 | 1 | walker | **23** |
| `fraaca` | 13×11 | 65 | 1 | walker | **24** |
| `rusaca` | 12×13 | 80 | 1 | walker | **25** |
| `ausaca` | 13×13 | 67 | 1 | walker | **26** |
| `spaaca` | 13×13 | 97 | 1 | walker | **26** |
| `ukraca` | 17×17 | 121 | 1 | walker | **30** |

## Артиллерийские депо (art)

| sid | bbox | cells | комп. | метод | слоты |
|---|---|---:|---:|---|---:|
| `hunart` | 10×8 | 55 | 1 | walker | **18** |
| `pieart` | 11×8 | 62 | 1 | walker | **19** |
| `polart` | 10×9 | 65 | 1 | walker | **19** |
| `saxart` | 10×9 | 54 | 1 | walker | **19** |
| `bavart` | 11×9 | 61 | 1 | walker | **20** |
| `denart` | 12×8 | 58 | 1 | walker | **20** |
| `netart` | 11×9 | 62 | 1 | walker | **20** |
| `sweart` | 11×9 | 56 | 1 | walker | **20** |
| `swiart` | 11×9 | 66 | 1 | walker | **20** |
| `venart` | 11×9 | 71 | 1 | walker | **20** |
| `scoart` | 12×9 | 59 | 1 | walker | **21** |
| `ausart` | 12×10 | 71 | 1 | walker | **22** |
| `engart` | 12×10 | 66 | 1 | walker | **22** |
| `porart` | 12×10 | 63 | 1 | walker | **22** |
| `pruart` | 11×11 | 68 | 1 | walker | **22** |
| `spaart` | 11×12 | 90 | 1 | walker | **23** |
| `fraart` | 12×12 | 85 | 1 | walker | **24** |
| `rusart` | 14×10 | 75 | 1 | walker | **24** |
| `turart` | 14×14 | 110 | 1 | walker | **28** |
| `ukrart` | 17×14 | 141 | 1 | walker | **30** |

## Порты (por)

| sid | bbox | cells | комп. | метод | слоты |
|---|---|---:|---:|---|---:|
| `porpor` | 10×11 | 80 | 1 | walker | **21** |
| `ruspor` | 14×13 | 124 | 1 | walker | **27** |
| `eurpor` | 14×16 | 129 | 1 | walker | **30** |
| `turpor` | 16×14 | 146 | 1 | walker | **30** |
| `ukrpor` | 15×21 | 188 | 1 | walker | **30** |

## Башни (tow)

| sid | bbox | cells | комп. | метод | слоты |
|---|---|---:|---:|---|---:|
| `eurtow` | 5×5 | 21 | 1 | walker | **10** |
| `rustow` | 5×5 | 21 | 1 | walker | **10** |
| `turtow` | 7×7 | 37 | 1 | walker | **14** |

## Шахты (gol/iro/coa)

| sid | bbox | cells | комп. | метод | слоты |
|---|---|---:|---:|---|---:|
| `eurgol` | 8×8 | 52 | 1 | walker | **16** |
| `euriro` | 8×8 | 52 | 1 | walker | **16** |
| `eurcoa` | 8×8 | 52 | 1 | walker | **16** |

## Стены (swa/wwa)

| sid | bbox | cells | комп. | метод | слоты |
|---|---|---:|---:|---|---:|
| `eurswa` | 2×2 | 4 | 1 | walker | **4** |
| `russwa` | 2×2 | 4 | 1 | walker | **4** |
| `turswa` | 2×2 | 4 | 1 | walker | **4** |
| `ukrwwa` | 2×2 | 4 | 1 | walker | **4** |
| `eurwwa` | 6×7 | 30 | 1 | walker | **13** |

## Ворота (sga/wga)

| sid | bbox | cells | комп. | метод | слоты |
|---|---|---:|---:|---|---:|
| `eursga` | 6×7 | 30 | 1 | walker | **13** |
| `eurwga` | 6×7 | 30 | 1 | walker | **13** |

## Прочие (миссии/сегменты стен/мосты)

| sid | bbox | cells | комп. | метод | слоты |
|---|---|---:|---:|---|---:|
| `eursga_14` | 6×2 | 4 | 2 | bbox_union | **8** |
| `eursga_15` | 2×6 | 4 | 2 | bbox_union | **8** |
| `eursga_16` | 8×8 | 22 | 2 | walker | **7** |
| `eursga_17` | 8×9 | 24 | 2 | walker | **8** |
| `eurswa_01` | 2×2 | 4 | 1 | walker | **4** |
| `eurswa_02` | 2×2 | 4 | 1 | walker | **4** |
| `eurswa_03` | 4×4 | 8 | 1 | walker | **8** |
| `eurswa_04` | 4×4 | 8 | 1 | walker | **8** |
| `eurswa_05` | 2×2 | 4 | 1 | walker | **4** |
| `eurswa_06` | 3×3 | 6 | 1 | walker | **6** |
| `eurswa_07` | 3×3 | 6 | 1 | walker | **6** |
| `eurswa_08` | 3×3 | 6 | 1 | walker | **6** |
| `eurswa_09` | 3×3 | 6 | 1 | walker | **6** |
| `eurswa_10` | 3×3 | 6 | 1 | walker | **6** |
| `eurswa_11` | 3×3 | 6 | 1 | walker | **6** |
| `eurswa_12` | 3×3 | 6 | 1 | walker | **6** |
| `eurswa_13` | 3×3 | 6 | 1 | walker | **6** |
| `eurswa_45gate` | 2×2 | 4 | 1 | walker | **4** |
| `eurswa_45v1` | 2×2 | 4 | 1 | walker | **4** |
| `eurswa_45v2` | 2×2 | 4 | 1 | walker | **4** |
| `eurswa_gate` | 2×2 | 4 | 1 | walker | **4** |
| `eurswa_tower` | 2×2 | 4 | 1 | walker | **4** |
| `eurswa_turn` | 2×2 | 4 | 1 | walker | **4** |
| `eurswa_turnmirror` | 2×2 | 4 | 1 | walker | **4** |
| `eurswa_v1` | 2×2 | 4 | 1 | walker | **4** |
| `eurswa_v2` | 2×2 | 4 | 1 | walker | **4** |
| `g_45left` | 2×2 | 4 | 1 | walker | **4** |
| `g_45right` | 2×2 | 4 | 1 | walker | **4** |
| `misblg` | 8×8 | 35 | 1 | walker | **16** |
| `misblg2` | 8×8 | 33 | 1 | walker | **16** |
| `misbridge1` | 2×2 | 4 | 1 | walker | **4** |
| `misbridge1a` | 2×2 | 4 | 1 | walker | **4** |
| `misbridge2` | 2×2 | 4 | 1 | walker | **4** |
| `misbridge2a` | 2×2 | 4 | 1 | walker | **4** |
| `misbridge3` | 2×2 | 4 | 1 | walker | **4** |
| `misbridge3a` | 2×2 | 4 | 1 | walker | **4** |
| `misbridge4` | 2×2 | 4 | 1 | walker | **4** |
| `misbridge4a` | 2×2 | 4 | 1 | walker | **4** |
| `miscauldron` | 2×2 | 3 | 1 | walker | **4** |
| `mischest1` | 2×3 | 4 | 1 | walker | **5** |
| `mischest2` | 2×2 | 3 | 1 | walker | **4** |
| `miscommandcenter` | 18×13 | 125 | 1 | walker | **30** |
| `mistent` | 12×8 | 47 | 1 | walker | **20** |
| `miswel1` | 2×2 | 4 | 1 | walker | **4** |
| `miswel2` | 3×2 | 6 | 1 | walker | **5** |
| `miswel3` | 2×3 | 4 | 1 | walker | **5** |
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
| `ukrwwa_tower` | 2×2 | 4 | 1 | walker | **4** |
| `ukrwwa_turn` | 2×2 | 4 | 1 | walker | **4** |
| `ukrwwa_turnmirror` | 2×2 | 4 | 1 | walker | **4** |
| `ukrwwa_v1` | 2×2 | 4 | 1 | walker | **4** |
| `ukrwwa_v2` | 2×2 | 4 | 1 | walker | **4** |


## Источники

Все ссылки относительно `data/scripts/` в установке Cossacks 3.

[^1]: `_unit_CalcBuilderPoints` — `lib/unit.script:8702-9006`.
