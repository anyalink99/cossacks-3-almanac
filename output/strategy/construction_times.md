# Cossacks 3 — Construction & Repair Times

Время постройки (с нуля, новое здание) и ремонта (полностью повреждённое → полное HP) для каждого здания. Считает с разным числом крестьян одновременно.

**Формулы** (см. [`recon/building_mechanics.md`](../../recon/building_mechanics.md)):

- **Постройка**, время с N крестьянами: `buildtime_sec × 1.13 / N` (clamp на slot cap)
- **Ремонт**, время с N крестьянами: `maxhp / (20 × N / 0.406)` g-sec
- 1 цикл construct анимации = 13 frames / 32 fps = **0.406 g-sec**
- @ fast game speed real-time = g-sec / 1.4

**Slot caps** (грубая оценка периметра collision mask, см. recon §3.2):

- Walls/gates: **4** slots per segment (явно заданы в `wallcustom.cfg`)
- Towers: **8** slots
- Большие здания (cen/aca/ba2/por): **16** slots
- Прочие: **12** slots

Cap не из кода напрямую (там `_unit_CalcBuilderPoints` динамически обходит периметр), а оценка для практики. Hard cap движка: 30.

**Колонки:** время в формате `<g-sec>g (<real-sec>r fast)`. Для длинных — в минутах.

## alg

### Постройка с нуля

| sid | имя | buildtime_g | slot_cap | 1 builders | 2 builders | 5 builders | 10 builders | max builders |
|---|---|---|---|---|---|---|---|---|
| `algaca` | Minaret | 156g | 16 | 2.9m g (2.1m r) | 1.5m g (1.1m r) | 35g (25r) | 18g (13r) | 11g (8r) |
| `algart` | Artillery Depot | 246g | 12 | 4.6m g (3.3m r) | 2.3m g (1.7m r) | 56g (40r) | 28g (20r) | 23g (17r) |
| `algbar` | Barracks | 94g | 12 | 1.8m g (1.3m r) | 53g (38r) | 21g (15r) | 11g (8r) | 9g (6r) |
| `algbla` | Blacksmith | 109g | 12 | 2.1m g (1.5m r) | 1.0m g (0.7m r) | 25g (18r) | 12g (9r) | 10g (7r) |
| `algcen` | Town Hall | 156g | 16 | 2.9m g (2.1m r) | 1.5m g (1.1m r) | 35g (25r) | 18g (13r) | 11g (8r) |
| `algdip` | Diplomatic Center | 312g | 12 | 5.9m g (4.2m r) | 2.9m g (2.1m r) | 1.2m g (0.8m r) | 35g (25r) | 29g (21r) |
| `alghou` | Housing | 31g | 12 | 35g (25r) | 18g (13r) | 7g (5r) | 4g (3r) | 3g (2r) |
| `algsta` | Stable | 156g | 12 | 2.9m g (2.1m r) | 1.5m g (1.1m r) | 35g (25r) | 18g (13r) | 15g (11r) |
| `algtem` | Mosque | 94g | 12 | 1.8m g (1.3m r) | 53g (38r) | 21g (15r) | 11g (8r) | 9g (6r) |
| `eurcoa` | Mine | 94g | 12 | 1.8m g (1.3m r) | 53g (38r) | 21g (15r) | 11g (8r) | 9g (6r) |
| `eurgol` | Mine | 94g | 12 | 1.8m g (1.3m r) | 53g (38r) | 21g (15r) | 11g (8r) | 9g (6r) |
| `euriro` | Mine | 94g | 12 | 1.8m g (1.3m r) | 53g (38r) | 21g (15r) | 11g (8r) | 9g (6r) |
| `turmar` | Bazaar | 234g | 12 | 4.4m g (3.2m r) | 2.2m g (1.6m r) | 53g (38r) | 26g (19r) | 22g (16r) |
| `turmil` | Mill | 94g | 12 | 1.8m g (1.3m r) | 53g (38r) | 21g (15r) | 11g (8r) | 9g (6r) |
| `turpor` | Shipyard | 1562g | 16 | 29.4m g (21.0m r) | 14.7m g (10.5m r) | 5.9m g (4.2m r) | 2.9m g (2.1m r) | 1.8m g (1.3m r) |
| `tursga` | Gate | 120g | 4 | 2.3m g (1.6m r) | 1.1m g (0.8m r) | 34g (24r) | 34g (24r) | 34g (24r) |
| `tursto` | Storehouse | 31g | 12 | 35g (25r) | 18g (13r) | 7g (5r) | 4g (3r) | 3g (2r) |
| `turswa` | Wall | 120g | 4 | 2.3m g (1.6m r) | 1.1m g (0.8m r) | 34g (24r) | 34g (24r) | 34g (24r) |
| `turtow` | Tower | 984g | 8 | 18.5m g (13.2m r) | 9.3m g (6.6m r) | 3.7m g (2.6m r) | 2.3m g (1.7m r) | 2.3m g (1.7m r) |

### Полный ремонт (0 → max HP)

| sid | имя | maxhp | slot_cap | 1 builders | 2 builders | 5 builders | 10 builders | max builders |
|---|---|---|---|---|---|---|---|---|
| `algaca` | Minaret | 65000 | 16 | 22.0m g (15.7m r) | 11.0m g (7.9m r) | 4.4m g (3.1m r) | 2.2m g (1.6m r) | 1.4m g (1.0m r) |
| `algart` | Artillery Depot | 40000 | 12 | 13.5m g (9.7m r) | 6.8m g (4.8m r) | 2.7m g (1.9m r) | 1.4m g (1.0m r) | 1.1m g (0.8m r) |
| `algbar` | Barracks | 35000 | 12 | 11.8m g (8.5m r) | 5.9m g (4.2m r) | 2.4m g (1.7m r) | 1.2m g (0.8m r) | 59g (42r) |
| `algbla` | Blacksmith | 6500 | 12 | 2.2m g (1.6m r) | 1.1m g (0.8m r) | 26g (19r) | 13g (9r) | 11g (8r) |
| `algcen` | Town Hall | 5500 | 16 | 1.9m g (1.3m r) | 56g (40r) | 22g (16r) | 11g (8r) | 7g (5r) |
| `algdip` | Diplomatic Center | 5500 | 12 | 1.9m g (1.3m r) | 56g (40r) | 22g (16r) | 11g (8r) | 9g (7r) |
| `alghou` | Housing | 4300 | 12 | 1.5m g (1.0m r) | 44g (31r) | 17g (12r) | 9g (6r) | 7g (5r) |
| `algsta` | Stable | 55000 | 12 | 18.6m g (13.3m r) | 9.3m g (6.6m r) | 3.7m g (2.7m r) | 1.9m g (1.3m r) | 1.6m g (1.1m r) |
| `algtem` | Mosque | 5000 | 12 | 1.7m g (1.2m r) | 51g (36r) | 20g (15r) | 10g (7r) | 8g (6r) |
| `eurcoa` | Mine | 2500 | 12 | 51g (36r) | 25g (18r) | 10g (7r) | 5g (4r) | 4g (3r) |
| `eurgol` | Mine | 2500 | 12 | 51g (36r) | 25g (18r) | 10g (7r) | 5g (4r) | 4g (3r) |
| `euriro` | Mine | 2500 | 12 | 51g (36r) | 25g (18r) | 10g (7r) | 5g (4r) | 4g (3r) |
| `turmar` | Bazaar | 4500 | 12 | 1.5m g (1.1m r) | 46g (33r) | 18g (13r) | 9g (7r) | 8g (5r) |
| `turmil` | Mill | 20000 | 12 | 6.8m g (4.8m r) | 3.4m g (2.4m r) | 1.4m g (1.0m r) | 41g (29r) | 34g (24r) |
| `turpor` | Shipyard | 40000 | 16 | 13.5m g (9.7m r) | 6.8m g (4.8m r) | 2.7m g (1.9m r) | 1.4m g (1.0m r) | 51g (36r) |
| `tursga` | Gate | 50000 | 4 | 16.9m g (12.1m r) | 8.5m g (6.0m r) | 4.2m g (3.0m r) | 4.2m g (3.0m r) | 4.2m g (3.0m r) |
| `tursto` | Storehouse | 10000 | 12 | 3.4m g (2.4m r) | 1.7m g (1.2m r) | 41g (29r) | 20g (15r) | 17g (12r) |
| `turswa` | Wall | 50000 | 4 | 16.9m g (12.1m r) | 8.5m g (6.0m r) | 4.2m g (3.0m r) | 4.2m g (3.0m r) | 4.2m g (3.0m r) |
| `turtow` | Tower | 22500 | 8 | 7.6m g (5.4m r) | 3.8m g (2.7m r) | 1.5m g (1.1m r) | 57g (41r) | 57g (41r) |

## aus

### Постройка с нуля

| sid | имя | buildtime_g | slot_cap | 1 builders | 2 builders | 5 builders | 10 builders | max builders |
|---|---|---|---|---|---|---|---|---|
| `ausaca` | Academy | 625g | 16 | 11.8m g (8.4m r) | 5.9m g (4.2m r) | 2.4m g (1.7m r) | 1.2m g (0.8m r) | 44g (32r) |
| `ausart` | Artillery Depot | 246g | 12 | 4.6m g (3.3m r) | 2.3m g (1.7m r) | 56g (40r) | 28g (20r) | 23g (17r) |
| `ausba2` | Barracks, 18th century | 5625g | 16 | 105.9m g (75.7m r) | 53.0m g (37.8m r) | 21.2m g (15.1m r) | 10.6m g (7.6m r) | 6.6m g (4.7m r) |
| `ausbar` | Barracks, 17th century | 94g | 12 | 1.8m g (1.3m r) | 53g (38r) | 21g (15r) | 11g (8r) | 9g (6r) |
| `ausbla` | Blacksmith | 94g | 12 | 1.8m g (1.3m r) | 53g (38r) | 21g (15r) | 11g (8r) | 9g (6r) |
| `auscen` | Town Hall | 47g | 16 | 53g (38r) | 26g (19r) | 11g (8r) | 5g (4r) | 3g (2r) |
| `ausdip` | Diplomatic Center | 312g | 12 | 5.9m g (4.2m r) | 2.9m g (2.1m r) | 1.2m g (0.8m r) | 35g (25r) | 29g (21r) |
| `aushou` | Housing | 31g | 12 | 35g (25r) | 18g (13r) | 7g (5r) | 4g (3r) | 3g (2r) |
| `aussta` | Stable | 625g | 12 | 11.8m g (8.4m r) | 5.9m g (4.2m r) | 2.4m g (1.7m r) | 1.2m g (0.8m r) | 59g (42r) |
| `austem` | Cathedral | 156g | 12 | 2.9m g (2.1m r) | 1.5m g (1.1m r) | 35g (25r) | 18g (13r) | 15g (11r) |
| `eurcoa` | Mine | 94g | 12 | 1.8m g (1.3m r) | 53g (38r) | 21g (15r) | 11g (8r) | 9g (6r) |
| `eurgol` | Mine | 94g | 12 | 1.8m g (1.3m r) | 53g (38r) | 21g (15r) | 11g (8r) | 9g (6r) |
| `euriro` | Mine | 94g | 12 | 1.8m g (1.3m r) | 53g (38r) | 21g (15r) | 11g (8r) | 9g (6r) |
| `eurmar` | Market | 234g | 12 | 4.4m g (3.2m r) | 2.2m g (1.6m r) | 53g (38r) | 26g (19r) | 22g (16r) |
| `eurmil` | Mill | 94g | 12 | 1.8m g (1.3m r) | 53g (38r) | 21g (15r) | 11g (8r) | 9g (6r) |
| `eurpor` | Shipyard | 1562g | 16 | 29.4m g (21.0m r) | 14.7m g (10.5m r) | 5.9m g (4.2m r) | 2.9m g (2.1m r) | 1.8m g (1.3m r) |
| `eursga` | Gate | 90g | 4 | 1.7m g (1.2m r) | 51g (36r) | 25g (18r) | 25g (18r) | 25g (18r) |
| `eursto` | Storehouse | 31g | 12 | 35g (25r) | 18g (13r) | 7g (5r) | 4g (3r) | 3g (2r) |
| `eurswa` | Wall | 90g | 4 | 1.7m g (1.2m r) | 51g (36r) | 25g (18r) | 25g (18r) | 25g (18r) |
| `eurtow` | Tower | 1230g | 8 | 23.2m g (16.6m r) | 11.6m g (8.3m r) | 4.6m g (3.3m r) | 2.9m g (2.1m r) | 2.9m g (2.1m r) |

### Полный ремонт (0 → max HP)

| sid | имя | maxhp | slot_cap | 1 builders | 2 builders | 5 builders | 10 builders | max builders |
|---|---|---|---|---|---|---|---|---|
| `ausaca` | Academy | 65000 | 16 | 22.0m g (15.7m r) | 11.0m g (7.9m r) | 4.4m g (3.1m r) | 2.2m g (1.6m r) | 1.4m g (1.0m r) |
| `ausart` | Artillery Depot | 40000 | 12 | 13.5m g (9.7m r) | 6.8m g (4.8m r) | 2.7m g (1.9m r) | 1.4m g (1.0m r) | 1.1m g (0.8m r) |
| `ausba2` | Barracks, 18th century | 55000 | 16 | 18.6m g (13.3m r) | 9.3m g (6.6m r) | 3.7m g (2.7m r) | 1.9m g (1.3m r) | 1.2m g (0.8m r) |
| `ausbar` | Barracks, 17th century | 40000 | 12 | 13.5m g (9.7m r) | 6.8m g (4.8m r) | 2.7m g (1.9m r) | 1.4m g (1.0m r) | 1.1m g (0.8m r) |
| `ausbla` | Blacksmith | 5500 | 12 | 1.9m g (1.3m r) | 56g (40r) | 22g (16r) | 11g (8r) | 9g (7r) |
| `auscen` | Town Hall | 4000 | 16 | 1.4m g (1.0m r) | 41g (29r) | 16g (12r) | 8g (6r) | 5g (4r) |
| `ausdip` | Diplomatic Center | 4500 | 12 | 1.5m g (1.1m r) | 46g (33r) | 18g (13r) | 9g (7r) | 8g (5r) |
| `aushou` | Housing | 4000 | 12 | 1.4m g (1.0m r) | 41g (29r) | 16g (12r) | 8g (6r) | 7g (5r) |
| `aussta` | Stable | 20000 | 12 | 6.8m g (4.8m r) | 3.4m g (2.4m r) | 1.4m g (1.0m r) | 41g (29r) | 34g (24r) |
| `austem` | Cathedral | 4200 | 12 | 1.4m g (1.0m r) | 43g (30r) | 17g (12r) | 9g (6r) | 7g (5r) |
| `eurcoa` | Mine | 2500 | 12 | 51g (36r) | 25g (18r) | 10g (7r) | 5g (4r) | 4g (3r) |
| `eurgol` | Mine | 2500 | 12 | 51g (36r) | 25g (18r) | 10g (7r) | 5g (4r) | 4g (3r) |
| `euriro` | Mine | 2500 | 12 | 51g (36r) | 25g (18r) | 10g (7r) | 5g (4r) | 4g (3r) |
| `eurmar` | Market | 4000 | 12 | 1.4m g (1.0m r) | 41g (29r) | 16g (12r) | 8g (6r) | 7g (5r) |
| `eurmil` | Mill | 20000 | 12 | 6.8m g (4.8m r) | 3.4m g (2.4m r) | 1.4m g (1.0m r) | 41g (29r) | 34g (24r) |
| `eurpor` | Shipyard | 50000 | 16 | 16.9m g (12.1m r) | 8.5m g (6.0m r) | 3.4m g (2.4m r) | 1.7m g (1.2m r) | 1.1m g (0.8m r) |
| `eursga` | Gate | 50000 | 4 | 16.9m g (12.1m r) | 8.5m g (6.0m r) | 4.2m g (3.0m r) | 4.2m g (3.0m r) | 4.2m g (3.0m r) |
| `eursto` | Storehouse | 10000 | 12 | 3.4m g (2.4m r) | 1.7m g (1.2m r) | 41g (29r) | 20g (15r) | 17g (12r) |
| `eurswa` | Wall | 50000 | 4 | 16.9m g (12.1m r) | 8.5m g (6.0m r) | 4.2m g (3.0m r) | 4.2m g (3.0m r) | 4.2m g (3.0m r) |
| `eurtow` | Tower | 20000 | 8 | 6.8m g (4.8m r) | 3.4m g (2.4m r) | 1.4m g (1.0m r) | 51g (36r) | 51g (36r) |

## bav

### Постройка с нуля

| sid | имя | buildtime_g | slot_cap | 1 builders | 2 builders | 5 builders | 10 builders | max builders |
|---|---|---|---|---|---|---|---|---|
| `bavaca` | Academy | 625g | 16 | 11.8m g (8.4m r) | 5.9m g (4.2m r) | 2.4m g (1.7m r) | 1.2m g (0.8m r) | 44g (32r) |
| `bavart` | Artillery Depot | 246g | 12 | 4.6m g (3.3m r) | 2.3m g (1.7m r) | 56g (40r) | 28g (20r) | 23g (17r) |
| `bavba2` | Barracks, 18th century | 5625g | 16 | 105.9m g (75.7m r) | 53.0m g (37.8m r) | 21.2m g (15.1m r) | 10.6m g (7.6m r) | 6.6m g (4.7m r) |
| `bavbar` | Barracks, 17th century | 94g | 12 | 1.8m g (1.3m r) | 53g (38r) | 21g (15r) | 11g (8r) | 9g (6r) |
| `bavbla` | Blacksmith | 94g | 12 | 1.8m g (1.3m r) | 53g (38r) | 21g (15r) | 11g (8r) | 9g (6r) |
| `bavcen` | Town Hall | 156g | 16 | 2.9m g (2.1m r) | 1.5m g (1.1m r) | 35g (25r) | 18g (13r) | 11g (8r) |
| `bavdip` | Diplomatic Center | 312g | 12 | 5.9m g (4.2m r) | 2.9m g (2.1m r) | 1.2m g (0.8m r) | 35g (25r) | 29g (21r) |
| `bavhou` | Housing | 31g | 12 | 35g (25r) | 18g (13r) | 7g (5r) | 4g (3r) | 3g (2r) |
| `bavsta` | Stable | 625g | 12 | 11.8m g (8.4m r) | 5.9m g (4.2m r) | 2.4m g (1.7m r) | 1.2m g (0.8m r) | 59g (42r) |
| `bavtem` | Cathedral | 156g | 12 | 2.9m g (2.1m r) | 1.5m g (1.1m r) | 35g (25r) | 18g (13r) | 15g (11r) |
| `eurcoa` | Mine | 94g | 12 | 1.8m g (1.3m r) | 53g (38r) | 21g (15r) | 11g (8r) | 9g (6r) |
| `eurgol` | Mine | 94g | 12 | 1.8m g (1.3m r) | 53g (38r) | 21g (15r) | 11g (8r) | 9g (6r) |
| `euriro` | Mine | 94g | 12 | 1.8m g (1.3m r) | 53g (38r) | 21g (15r) | 11g (8r) | 9g (6r) |
| `eurmar` | Market | 234g | 12 | 4.4m g (3.2m r) | 2.2m g (1.6m r) | 53g (38r) | 26g (19r) | 22g (16r) |
| `eurmil` | Mill | 94g | 12 | 1.8m g (1.3m r) | 53g (38r) | 21g (15r) | 11g (8r) | 9g (6r) |
| `eurpor` | Shipyard | 1562g | 16 | 29.4m g (21.0m r) | 14.7m g (10.5m r) | 5.9m g (4.2m r) | 2.9m g (2.1m r) | 1.8m g (1.3m r) |
| `eursga` | Gate | 90g | 4 | 1.7m g (1.2m r) | 51g (36r) | 25g (18r) | 25g (18r) | 25g (18r) |
| `eursto` | Storehouse | 31g | 12 | 35g (25r) | 18g (13r) | 7g (5r) | 4g (3r) | 3g (2r) |
| `eurswa` | Wall | 90g | 4 | 1.7m g (1.2m r) | 51g (36r) | 25g (18r) | 25g (18r) | 25g (18r) |
| `eurtow` | Tower | 1230g | 8 | 23.2m g (16.6m r) | 11.6m g (8.3m r) | 4.6m g (3.3m r) | 2.9m g (2.1m r) | 2.9m g (2.1m r) |

### Полный ремонт (0 → max HP)

| sid | имя | maxhp | slot_cap | 1 builders | 2 builders | 5 builders | 10 builders | max builders |
|---|---|---|---|---|---|---|---|---|
| `bavaca` | Academy | 63000 | 16 | 21.3m g (15.2m r) | 10.7m g (7.6m r) | 4.3m g (3.0m r) | 2.1m g (1.5m r) | 1.3m g (1.0m r) |
| `bavart` | Artillery Depot | 40000 | 12 | 13.5m g (9.7m r) | 6.8m g (4.8m r) | 2.7m g (1.9m r) | 1.4m g (1.0m r) | 1.1m g (0.8m r) |
| `bavba2` | Barracks, 18th century | 55000 | 16 | 18.6m g (13.3m r) | 9.3m g (6.6m r) | 3.7m g (2.7m r) | 1.9m g (1.3m r) | 1.2m g (0.8m r) |
| `bavbar` | Barracks, 17th century | 40000 | 12 | 13.5m g (9.7m r) | 6.8m g (4.8m r) | 2.7m g (1.9m r) | 1.4m g (1.0m r) | 1.1m g (0.8m r) |
| `bavbla` | Blacksmith | 5500 | 12 | 1.9m g (1.3m r) | 56g (40r) | 22g (16r) | 11g (8r) | 9g (7r) |
| `bavcen` | Town Hall | 4000 | 16 | 1.4m g (1.0m r) | 41g (29r) | 16g (12r) | 8g (6r) | 5g (4r) |
| `bavdip` | Diplomatic Center | 4500 | 12 | 1.5m g (1.1m r) | 46g (33r) | 18g (13r) | 9g (7r) | 8g (5r) |
| `bavhou` | Housing | 4000 | 12 | 1.4m g (1.0m r) | 41g (29r) | 16g (12r) | 8g (6r) | 7g (5r) |
| `bavsta` | Stable | 20000 | 12 | 6.8m g (4.8m r) | 3.4m g (2.4m r) | 1.4m g (1.0m r) | 41g (29r) | 34g (24r) |
| `bavtem` | Cathedral | 4200 | 12 | 1.4m g (1.0m r) | 43g (30r) | 17g (12r) | 9g (6r) | 7g (5r) |
| `eurcoa` | Mine | 2500 | 12 | 51g (36r) | 25g (18r) | 10g (7r) | 5g (4r) | 4g (3r) |
| `eurgol` | Mine | 2500 | 12 | 51g (36r) | 25g (18r) | 10g (7r) | 5g (4r) | 4g (3r) |
| `euriro` | Mine | 2500 | 12 | 51g (36r) | 25g (18r) | 10g (7r) | 5g (4r) | 4g (3r) |
| `eurmar` | Market | 4000 | 12 | 1.4m g (1.0m r) | 41g (29r) | 16g (12r) | 8g (6r) | 7g (5r) |
| `eurmil` | Mill | 20000 | 12 | 6.8m g (4.8m r) | 3.4m g (2.4m r) | 1.4m g (1.0m r) | 41g (29r) | 34g (24r) |
| `eurpor` | Shipyard | 50000 | 16 | 16.9m g (12.1m r) | 8.5m g (6.0m r) | 3.4m g (2.4m r) | 1.7m g (1.2m r) | 1.1m g (0.8m r) |
| `eursga` | Gate | 50000 | 4 | 16.9m g (12.1m r) | 8.5m g (6.0m r) | 4.2m g (3.0m r) | 4.2m g (3.0m r) | 4.2m g (3.0m r) |
| `eursto` | Storehouse | 10000 | 12 | 3.4m g (2.4m r) | 1.7m g (1.2m r) | 41g (29r) | 20g (15r) | 17g (12r) |
| `eurswa` | Wall | 50000 | 4 | 16.9m g (12.1m r) | 8.5m g (6.0m r) | 4.2m g (3.0m r) | 4.2m g (3.0m r) | 4.2m g (3.0m r) |
| `eurtow` | Tower | 20000 | 8 | 6.8m g (4.8m r) | 3.4m g (2.4m r) | 1.4m g (1.0m r) | 51g (36r) | 51g (36r) |

## den

### Постройка с нуля

| sid | имя | buildtime_g | slot_cap | 1 builders | 2 builders | 5 builders | 10 builders | max builders |
|---|---|---|---|---|---|---|---|---|
| `denaca` | Academy | 625g | 16 | 11.8m g (8.4m r) | 5.9m g (4.2m r) | 2.4m g (1.7m r) | 1.2m g (0.8m r) | 44g (32r) |
| `denart` | Artillery Depot | 246g | 12 | 4.6m g (3.3m r) | 2.3m g (1.7m r) | 56g (40r) | 28g (20r) | 23g (17r) |
| `denba2` | Barracks, 18th century | 5625g | 16 | 105.9m g (75.7m r) | 53.0m g (37.8m r) | 21.2m g (15.1m r) | 10.6m g (7.6m r) | 6.6m g (4.7m r) |
| `denbar` | Barracks, 17th century | 94g | 12 | 1.8m g (1.3m r) | 53g (38r) | 21g (15r) | 11g (8r) | 9g (6r) |
| `denbla` | Blacksmith | 94g | 12 | 1.8m g (1.3m r) | 53g (38r) | 21g (15r) | 11g (8r) | 9g (6r) |
| `dencen` | Town Hall | 156g | 16 | 2.9m g (2.1m r) | 1.5m g (1.1m r) | 35g (25r) | 18g (13r) | 11g (8r) |
| `dendip` | Diplomatic Center | 312g | 12 | 5.9m g (4.2m r) | 2.9m g (2.1m r) | 1.2m g (0.8m r) | 35g (25r) | 29g (21r) |
| `denhou` | Housing | 31g | 12 | 35g (25r) | 18g (13r) | 7g (5r) | 4g (3r) | 3g (2r) |
| `densta` | Stable | 625g | 12 | 11.8m g (8.4m r) | 5.9m g (4.2m r) | 2.4m g (1.7m r) | 1.2m g (0.8m r) | 59g (42r) |
| `dentem` | Cathedral | 156g | 12 | 2.9m g (2.1m r) | 1.5m g (1.1m r) | 35g (25r) | 18g (13r) | 15g (11r) |
| `eurcoa` | Mine | 94g | 12 | 1.8m g (1.3m r) | 53g (38r) | 21g (15r) | 11g (8r) | 9g (6r) |
| `eurgol` | Mine | 94g | 12 | 1.8m g (1.3m r) | 53g (38r) | 21g (15r) | 11g (8r) | 9g (6r) |
| `euriro` | Mine | 94g | 12 | 1.8m g (1.3m r) | 53g (38r) | 21g (15r) | 11g (8r) | 9g (6r) |
| `eurmar` | Market | 234g | 12 | 4.4m g (3.2m r) | 2.2m g (1.6m r) | 53g (38r) | 26g (19r) | 22g (16r) |
| `eurmil` | Mill | 94g | 12 | 1.8m g (1.3m r) | 53g (38r) | 21g (15r) | 11g (8r) | 9g (6r) |
| `eurpor` | Shipyard | 1562g | 16 | 29.4m g (21.0m r) | 14.7m g (10.5m r) | 5.9m g (4.2m r) | 2.9m g (2.1m r) | 1.8m g (1.3m r) |
| `eursga` | Gate | 90g | 4 | 1.7m g (1.2m r) | 51g (36r) | 25g (18r) | 25g (18r) | 25g (18r) |
| `eursto` | Storehouse | 31g | 12 | 35g (25r) | 18g (13r) | 7g (5r) | 4g (3r) | 3g (2r) |
| `eurswa` | Wall | 90g | 4 | 1.7m g (1.2m r) | 51g (36r) | 25g (18r) | 25g (18r) | 25g (18r) |
| `eurtow` | Tower | 1230g | 8 | 23.2m g (16.6m r) | 11.6m g (8.3m r) | 4.6m g (3.3m r) | 2.9m g (2.1m r) | 2.9m g (2.1m r) |

### Полный ремонт (0 → max HP)

| sid | имя | maxhp | slot_cap | 1 builders | 2 builders | 5 builders | 10 builders | max builders |
|---|---|---|---|---|---|---|---|---|
| `denaca` | Academy | 63000 | 16 | 21.3m g (15.2m r) | 10.7m g (7.6m r) | 4.3m g (3.0m r) | 2.1m g (1.5m r) | 1.3m g (1.0m r) |
| `denart` | Artillery Depot | 40000 | 12 | 13.5m g (9.7m r) | 6.8m g (4.8m r) | 2.7m g (1.9m r) | 1.4m g (1.0m r) | 1.1m g (0.8m r) |
| `denba2` | Barracks, 18th century | 55000 | 16 | 18.6m g (13.3m r) | 9.3m g (6.6m r) | 3.7m g (2.7m r) | 1.9m g (1.3m r) | 1.2m g (0.8m r) |
| `denbar` | Barracks, 17th century | 40000 | 12 | 13.5m g (9.7m r) | 6.8m g (4.8m r) | 2.7m g (1.9m r) | 1.4m g (1.0m r) | 1.1m g (0.8m r) |
| `denbla` | Blacksmith | 5500 | 12 | 1.9m g (1.3m r) | 56g (40r) | 22g (16r) | 11g (8r) | 9g (7r) |
| `dencen` | Town Hall | 4030 | 16 | 1.4m g (1.0m r) | 41g (29r) | 16g (12r) | 8g (6r) | 5g (4r) |
| `dendip` | Diplomatic Center | 4500 | 12 | 1.5m g (1.1m r) | 46g (33r) | 18g (13r) | 9g (7r) | 8g (5r) |
| `denhou` | Housing | 4000 | 12 | 1.4m g (1.0m r) | 41g (29r) | 16g (12r) | 8g (6r) | 7g (5r) |
| `densta` | Stable | 20000 | 12 | 6.8m g (4.8m r) | 3.4m g (2.4m r) | 1.4m g (1.0m r) | 41g (29r) | 34g (24r) |
| `dentem` | Cathedral | 4200 | 12 | 1.4m g (1.0m r) | 43g (30r) | 17g (12r) | 9g (6r) | 7g (5r) |
| `eurcoa` | Mine | 2500 | 12 | 51g (36r) | 25g (18r) | 10g (7r) | 5g (4r) | 4g (3r) |
| `eurgol` | Mine | 2500 | 12 | 51g (36r) | 25g (18r) | 10g (7r) | 5g (4r) | 4g (3r) |
| `euriro` | Mine | 2500 | 12 | 51g (36r) | 25g (18r) | 10g (7r) | 5g (4r) | 4g (3r) |
| `eurmar` | Market | 4000 | 12 | 1.4m g (1.0m r) | 41g (29r) | 16g (12r) | 8g (6r) | 7g (5r) |
| `eurmil` | Mill | 20000 | 12 | 6.8m g (4.8m r) | 3.4m g (2.4m r) | 1.4m g (1.0m r) | 41g (29r) | 34g (24r) |
| `eurpor` | Shipyard | 50000 | 16 | 16.9m g (12.1m r) | 8.5m g (6.0m r) | 3.4m g (2.4m r) | 1.7m g (1.2m r) | 1.1m g (0.8m r) |
| `eursga` | Gate | 50000 | 4 | 16.9m g (12.1m r) | 8.5m g (6.0m r) | 4.2m g (3.0m r) | 4.2m g (3.0m r) | 4.2m g (3.0m r) |
| `eursto` | Storehouse | 10000 | 12 | 3.4m g (2.4m r) | 1.7m g (1.2m r) | 41g (29r) | 20g (15r) | 17g (12r) |
| `eurswa` | Wall | 50000 | 4 | 16.9m g (12.1m r) | 8.5m g (6.0m r) | 4.2m g (3.0m r) | 4.2m g (3.0m r) | 4.2m g (3.0m r) |
| `eurtow` | Tower | 20000 | 8 | 6.8m g (4.8m r) | 3.4m g (2.4m r) | 1.4m g (1.0m r) | 51g (36r) | 51g (36r) |

## eng

### Постройка с нуля

| sid | имя | buildtime_g | slot_cap | 1 builders | 2 builders | 5 builders | 10 builders | max builders |
|---|---|---|---|---|---|---|---|---|
| `engaca` | Academy | 625g | 16 | 11.8m g (8.4m r) | 5.9m g (4.2m r) | 2.4m g (1.7m r) | 1.2m g (0.8m r) | 44g (32r) |
| `engart` | Artillery Depot | 246g | 12 | 4.6m g (3.3m r) | 2.3m g (1.7m r) | 56g (40r) | 28g (20r) | 23g (17r) |
| `engba2` | Barracks, 18th century | 5625g | 16 | 105.9m g (75.7m r) | 53.0m g (37.8m r) | 21.2m g (15.1m r) | 10.6m g (7.6m r) | 6.6m g (4.7m r) |
| `engbar` | Barracks, 17th century | 94g | 12 | 1.8m g (1.3m r) | 53g (38r) | 21g (15r) | 11g (8r) | 9g (6r) |
| `engbla` | Blacksmith | 94g | 12 | 1.8m g (1.3m r) | 53g (38r) | 21g (15r) | 11g (8r) | 9g (6r) |
| `engcen` | Town Hall | 156g | 16 | 2.9m g (2.1m r) | 1.5m g (1.1m r) | 35g (25r) | 18g (13r) | 11g (8r) |
| `engdip` | Diplomatic Center | 312g | 12 | 5.9m g (4.2m r) | 2.9m g (2.1m r) | 1.2m g (0.8m r) | 35g (25r) | 29g (21r) |
| `enghou` | Housing | 31g | 12 | 35g (25r) | 18g (13r) | 7g (5r) | 4g (3r) | 3g (2r) |
| `engsta` | Stable | 375g | 12 | 7.1m g (5.0m r) | 3.5m g (2.5m r) | 1.4m g (1.0m r) | 42g (30r) | 35g (25r) |
| `engtem` | Cathedral | 156g | 12 | 2.9m g (2.1m r) | 1.5m g (1.1m r) | 35g (25r) | 18g (13r) | 15g (11r) |
| `eurcoa` | Mine | 94g | 12 | 1.8m g (1.3m r) | 53g (38r) | 21g (15r) | 11g (8r) | 9g (6r) |
| `eurgol` | Mine | 94g | 12 | 1.8m g (1.3m r) | 53g (38r) | 21g (15r) | 11g (8r) | 9g (6r) |
| `euriro` | Mine | 94g | 12 | 1.8m g (1.3m r) | 53g (38r) | 21g (15r) | 11g (8r) | 9g (6r) |
| `eurmar` | Market | 234g | 12 | 4.4m g (3.2m r) | 2.2m g (1.6m r) | 53g (38r) | 26g (19r) | 22g (16r) |
| `eurmil` | Mill | 94g | 12 | 1.8m g (1.3m r) | 53g (38r) | 21g (15r) | 11g (8r) | 9g (6r) |
| `eurpor` | Shipyard | 1562g | 16 | 29.4m g (21.0m r) | 14.7m g (10.5m r) | 5.9m g (4.2m r) | 2.9m g (2.1m r) | 1.8m g (1.3m r) |
| `eursga` | Gate | 90g | 4 | 1.7m g (1.2m r) | 51g (36r) | 25g (18r) | 25g (18r) | 25g (18r) |
| `eursto` | Storehouse | 31g | 12 | 35g (25r) | 18g (13r) | 7g (5r) | 4g (3r) | 3g (2r) |
| `eurswa` | Wall | 90g | 4 | 1.7m g (1.2m r) | 51g (36r) | 25g (18r) | 25g (18r) | 25g (18r) |
| `eurtow` | Tower | 1230g | 8 | 23.2m g (16.6m r) | 11.6m g (8.3m r) | 4.6m g (3.3m r) | 2.9m g (2.1m r) | 2.9m g (2.1m r) |

### Полный ремонт (0 → max HP)

| sid | имя | maxhp | slot_cap | 1 builders | 2 builders | 5 builders | 10 builders | max builders |
|---|---|---|---|---|---|---|---|---|
| `engaca` | Academy | 63000 | 16 | 21.3m g (15.2m r) | 10.7m g (7.6m r) | 4.3m g (3.0m r) | 2.1m g (1.5m r) | 1.3m g (1.0m r) |
| `engart` | Artillery Depot | 40000 | 12 | 13.5m g (9.7m r) | 6.8m g (4.8m r) | 2.7m g (1.9m r) | 1.4m g (1.0m r) | 1.1m g (0.8m r) |
| `engba2` | Barracks, 18th century | 55000 | 16 | 18.6m g (13.3m r) | 9.3m g (6.6m r) | 3.7m g (2.7m r) | 1.9m g (1.3m r) | 1.2m g (0.8m r) |
| `engbar` | Barracks, 17th century | 40000 | 12 | 13.5m g (9.7m r) | 6.8m g (4.8m r) | 2.7m g (1.9m r) | 1.4m g (1.0m r) | 1.1m g (0.8m r) |
| `engbla` | Blacksmith | 5500 | 12 | 1.9m g (1.3m r) | 56g (40r) | 22g (16r) | 11g (8r) | 9g (7r) |
| `engcen` | Town Hall | 4030 | 16 | 1.4m g (1.0m r) | 41g (29r) | 16g (12r) | 8g (6r) | 5g (4r) |
| `engdip` | Diplomatic Center | 4500 | 12 | 1.5m g (1.1m r) | 46g (33r) | 18g (13r) | 9g (7r) | 8g (5r) |
| `enghou` | Housing | 5000 | 12 | 1.7m g (1.2m r) | 51g (36r) | 20g (15r) | 10g (7r) | 8g (6r) |
| `engsta` | Stable | 25000 | 12 | 8.5m g (6.0m r) | 4.2m g (3.0m r) | 1.7m g (1.2m r) | 51g (36r) | 42g (30r) |
| `engtem` | Cathedral | 4200 | 12 | 1.4m g (1.0m r) | 43g (30r) | 17g (12r) | 9g (6r) | 7g (5r) |
| `eurcoa` | Mine | 2500 | 12 | 51g (36r) | 25g (18r) | 10g (7r) | 5g (4r) | 4g (3r) |
| `eurgol` | Mine | 2500 | 12 | 51g (36r) | 25g (18r) | 10g (7r) | 5g (4r) | 4g (3r) |
| `euriro` | Mine | 2500 | 12 | 51g (36r) | 25g (18r) | 10g (7r) | 5g (4r) | 4g (3r) |
| `eurmar` | Market | 4000 | 12 | 1.4m g (1.0m r) | 41g (29r) | 16g (12r) | 8g (6r) | 7g (5r) |
| `eurmil` | Mill | 20000 | 12 | 6.8m g (4.8m r) | 3.4m g (2.4m r) | 1.4m g (1.0m r) | 41g (29r) | 34g (24r) |
| `eurpor` | Shipyard | 50000 | 16 | 16.9m g (12.1m r) | 8.5m g (6.0m r) | 3.4m g (2.4m r) | 1.7m g (1.2m r) | 1.1m g (0.8m r) |
| `eursga` | Gate | 50000 | 4 | 16.9m g (12.1m r) | 8.5m g (6.0m r) | 4.2m g (3.0m r) | 4.2m g (3.0m r) | 4.2m g (3.0m r) |
| `eursto` | Storehouse | 10000 | 12 | 3.4m g (2.4m r) | 1.7m g (1.2m r) | 41g (29r) | 20g (15r) | 17g (12r) |
| `eurswa` | Wall | 50000 | 4 | 16.9m g (12.1m r) | 8.5m g (6.0m r) | 4.2m g (3.0m r) | 4.2m g (3.0m r) | 4.2m g (3.0m r) |
| `eurtow` | Tower | 20000 | 8 | 6.8m g (4.8m r) | 3.4m g (2.4m r) | 1.4m g (1.0m r) | 51g (36r) | 51g (36r) |

## fra

### Постройка с нуля

| sid | имя | buildtime_g | slot_cap | 1 builders | 2 builders | 5 builders | 10 builders | max builders |
|---|---|---|---|---|---|---|---|---|
| `eurcoa` | Mine | 94g | 12 | 1.8m g (1.3m r) | 53g (38r) | 21g (15r) | 11g (8r) | 9g (6r) |
| `eurgol` | Mine | 94g | 12 | 1.8m g (1.3m r) | 53g (38r) | 21g (15r) | 11g (8r) | 9g (6r) |
| `euriro` | Mine | 94g | 12 | 1.8m g (1.3m r) | 53g (38r) | 21g (15r) | 11g (8r) | 9g (6r) |
| `eurmar` | Market | 234g | 12 | 4.4m g (3.2m r) | 2.2m g (1.6m r) | 53g (38r) | 26g (19r) | 22g (16r) |
| `eurmil` | Mill | 94g | 12 | 1.8m g (1.3m r) | 53g (38r) | 21g (15r) | 11g (8r) | 9g (6r) |
| `eurpor` | Shipyard | 1562g | 16 | 29.4m g (21.0m r) | 14.7m g (10.5m r) | 5.9m g (4.2m r) | 2.9m g (2.1m r) | 1.8m g (1.3m r) |
| `eursga` | Gate | 90g | 4 | 1.7m g (1.2m r) | 51g (36r) | 25g (18r) | 25g (18r) | 25g (18r) |
| `eursto` | Storehouse | 31g | 12 | 35g (25r) | 18g (13r) | 7g (5r) | 4g (3r) | 3g (2r) |
| `eurswa` | Wall | 90g | 4 | 1.7m g (1.2m r) | 51g (36r) | 25g (18r) | 25g (18r) | 25g (18r) |
| `eurtow` | Tower | 1230g | 8 | 23.2m g (16.6m r) | 11.6m g (8.3m r) | 4.6m g (3.3m r) | 2.9m g (2.1m r) | 2.9m g (2.1m r) |
| `fraaca` | Academy | 625g | 16 | 11.8m g (8.4m r) | 5.9m g (4.2m r) | 2.4m g (1.7m r) | 1.2m g (0.8m r) | 44g (32r) |
| `fraart` | Artillery Depot | 246g | 12 | 4.6m g (3.3m r) | 2.3m g (1.7m r) | 56g (40r) | 28g (20r) | 23g (17r) |
| `fraba2` | Barracks, 18th century | 5625g | 16 | 105.9m g (75.7m r) | 53.0m g (37.8m r) | 21.2m g (15.1m r) | 10.6m g (7.6m r) | 6.6m g (4.7m r) |
| `frabar` | Barracks, 17th century | 94g | 12 | 1.8m g (1.3m r) | 53g (38r) | 21g (15r) | 11g (8r) | 9g (6r) |
| `frabla` | Blacksmith | 94g | 12 | 1.8m g (1.3m r) | 53g (38r) | 21g (15r) | 11g (8r) | 9g (6r) |
| `fracen` | Town Hall | 156g | 16 | 2.9m g (2.1m r) | 1.5m g (1.1m r) | 35g (25r) | 18g (13r) | 11g (8r) |
| `fradip` | Diplomatic Center | 312g | 12 | 5.9m g (4.2m r) | 2.9m g (2.1m r) | 1.2m g (0.8m r) | 35g (25r) | 29g (21r) |
| `frahou` | Housing | 31g | 12 | 35g (25r) | 18g (13r) | 7g (5r) | 4g (3r) | 3g (2r) |
| `frasta` | Stable | 625g | 12 | 11.8m g (8.4m r) | 5.9m g (4.2m r) | 2.4m g (1.7m r) | 1.2m g (0.8m r) | 59g (42r) |
| `fratem` | Cathedral | 312g | 12 | 5.9m g (4.2m r) | 2.9m g (2.1m r) | 1.2m g (0.8m r) | 35g (25r) | 29g (21r) |

### Полный ремонт (0 → max HP)

| sid | имя | maxhp | slot_cap | 1 builders | 2 builders | 5 builders | 10 builders | max builders |
|---|---|---|---|---|---|---|---|---|
| `eurcoa` | Mine | 2500 | 12 | 51g (36r) | 25g (18r) | 10g (7r) | 5g (4r) | 4g (3r) |
| `eurgol` | Mine | 2500 | 12 | 51g (36r) | 25g (18r) | 10g (7r) | 5g (4r) | 4g (3r) |
| `euriro` | Mine | 2500 | 12 | 51g (36r) | 25g (18r) | 10g (7r) | 5g (4r) | 4g (3r) |
| `eurmar` | Market | 4000 | 12 | 1.4m g (1.0m r) | 41g (29r) | 16g (12r) | 8g (6r) | 7g (5r) |
| `eurmil` | Mill | 20000 | 12 | 6.8m g (4.8m r) | 3.4m g (2.4m r) | 1.4m g (1.0m r) | 41g (29r) | 34g (24r) |
| `eurpor` | Shipyard | 50000 | 16 | 16.9m g (12.1m r) | 8.5m g (6.0m r) | 3.4m g (2.4m r) | 1.7m g (1.2m r) | 1.1m g (0.8m r) |
| `eursga` | Gate | 50000 | 4 | 16.9m g (12.1m r) | 8.5m g (6.0m r) | 4.2m g (3.0m r) | 4.2m g (3.0m r) | 4.2m g (3.0m r) |
| `eursto` | Storehouse | 10000 | 12 | 3.4m g (2.4m r) | 1.7m g (1.2m r) | 41g (29r) | 20g (15r) | 17g (12r) |
| `eurswa` | Wall | 50000 | 4 | 16.9m g (12.1m r) | 8.5m g (6.0m r) | 4.2m g (3.0m r) | 4.2m g (3.0m r) | 4.2m g (3.0m r) |
| `eurtow` | Tower | 20000 | 8 | 6.8m g (4.8m r) | 3.4m g (2.4m r) | 1.4m g (1.0m r) | 51g (36r) | 51g (36r) |
| `fraaca` | Academy | 63000 | 16 | 21.3m g (15.2m r) | 10.7m g (7.6m r) | 4.3m g (3.0m r) | 2.1m g (1.5m r) | 1.3m g (1.0m r) |
| `fraart` | Artillery Depot | 40000 | 12 | 13.5m g (9.7m r) | 6.8m g (4.8m r) | 2.7m g (1.9m r) | 1.4m g (1.0m r) | 1.1m g (0.8m r) |
| `fraba2` | Barracks, 18th century | 55000 | 16 | 18.6m g (13.3m r) | 9.3m g (6.6m r) | 3.7m g (2.7m r) | 1.9m g (1.3m r) | 1.2m g (0.8m r) |
| `frabar` | Barracks, 17th century | 40000 | 12 | 13.5m g (9.7m r) | 6.8m g (4.8m r) | 2.7m g (1.9m r) | 1.4m g (1.0m r) | 1.1m g (0.8m r) |
| `frabla` | Blacksmith | 5500 | 12 | 1.9m g (1.3m r) | 56g (40r) | 22g (16r) | 11g (8r) | 9g (7r) |
| `fracen` | Town Hall | 4500 | 16 | 1.5m g (1.1m r) | 46g (33r) | 18g (13r) | 9g (7r) | 6g (4r) |
| `fradip` | Diplomatic Center | 4500 | 12 | 1.5m g (1.1m r) | 46g (33r) | 18g (13r) | 9g (7r) | 8g (5r) |
| `frahou` | Housing | 4000 | 12 | 1.4m g (1.0m r) | 41g (29r) | 16g (12r) | 8g (6r) | 7g (5r) |
| `frasta` | Stable | 20000 | 12 | 6.8m g (4.8m r) | 3.4m g (2.4m r) | 1.4m g (1.0m r) | 41g (29r) | 34g (24r) |
| `fratem` | Cathedral | 6000 | 12 | 2.0m g (1.5m r) | 1.0m g (0.7m r) | 24g (17r) | 12g (9r) | 10g (7r) |

## hun

### Постройка с нуля

| sid | имя | buildtime_g | slot_cap | 1 builders | 2 builders | 5 builders | 10 builders | max builders |
|---|---|---|---|---|---|---|---|---|
| `eurcoa` | Mine | 94g | 12 | 1.8m g (1.3m r) | 53g (38r) | 21g (15r) | 11g (8r) | 9g (6r) |
| `eurgol` | Mine | 94g | 12 | 1.8m g (1.3m r) | 53g (38r) | 21g (15r) | 11g (8r) | 9g (6r) |
| `euriro` | Mine | 94g | 12 | 1.8m g (1.3m r) | 53g (38r) | 21g (15r) | 11g (8r) | 9g (6r) |
| `eurmar` | Market | 234g | 12 | 4.4m g (3.2m r) | 2.2m g (1.6m r) | 53g (38r) | 26g (19r) | 22g (16r) |
| `eurmil` | Mill | 94g | 12 | 1.8m g (1.3m r) | 53g (38r) | 21g (15r) | 11g (8r) | 9g (6r) |
| `eurpor` | Shipyard | 1562g | 16 | 29.4m g (21.0m r) | 14.7m g (10.5m r) | 5.9m g (4.2m r) | 2.9m g (2.1m r) | 1.8m g (1.3m r) |
| `eursga` | Gate | 90g | 4 | 1.7m g (1.2m r) | 51g (36r) | 25g (18r) | 25g (18r) | 25g (18r) |
| `eursto` | Storehouse | 31g | 12 | 35g (25r) | 18g (13r) | 7g (5r) | 4g (3r) | 3g (2r) |
| `eurswa` | Wall | 90g | 4 | 1.7m g (1.2m r) | 51g (36r) | 25g (18r) | 25g (18r) | 25g (18r) |
| `eurtow` | Tower | 1230g | 8 | 23.2m g (16.6m r) | 11.6m g (8.3m r) | 4.6m g (3.3m r) | 2.9m g (2.1m r) | 2.9m g (2.1m r) |
| `hunaca` | Academy | 625g | 16 | 11.8m g (8.4m r) | 5.9m g (4.2m r) | 2.4m g (1.7m r) | 1.2m g (0.8m r) | 44g (32r) |
| `hunart` | Artillery Depot | 246g | 12 | 4.6m g (3.3m r) | 2.3m g (1.7m r) | 56g (40r) | 28g (20r) | 23g (17r) |
| `hunba2` | Barracks, 18th century | 5625g | 16 | 105.9m g (75.7m r) | 53.0m g (37.8m r) | 21.2m g (15.1m r) | 10.6m g (7.6m r) | 6.6m g (4.7m r) |
| `hunbar` | Barracks, 17th century | 94g | 12 | 1.8m g (1.3m r) | 53g (38r) | 21g (15r) | 11g (8r) | 9g (6r) |
| `hunbla` | Blacksmith | 94g | 12 | 1.8m g (1.3m r) | 53g (38r) | 21g (15r) | 11g (8r) | 9g (6r) |
| `huncen` | Town Hall | 156g | 16 | 2.9m g (2.1m r) | 1.5m g (1.1m r) | 35g (25r) | 18g (13r) | 11g (8r) |
| `hundip` | Diplomatic Center | 312g | 12 | 5.9m g (4.2m r) | 2.9m g (2.1m r) | 1.2m g (0.8m r) | 35g (25r) | 29g (21r) |
| `hunhou` | Housing | 31g | 12 | 35g (25r) | 18g (13r) | 7g (5r) | 4g (3r) | 3g (2r) |
| `hunsta` | Stable | 625g | 12 | 11.8m g (8.4m r) | 5.9m g (4.2m r) | 2.4m g (1.7m r) | 1.2m g (0.8m r) | 59g (42r) |
| `huntem` | Cathedral | 156g | 12 | 2.9m g (2.1m r) | 1.5m g (1.1m r) | 35g (25r) | 18g (13r) | 15g (11r) |

### Полный ремонт (0 → max HP)

| sid | имя | maxhp | slot_cap | 1 builders | 2 builders | 5 builders | 10 builders | max builders |
|---|---|---|---|---|---|---|---|---|
| `eurcoa` | Mine | 2500 | 12 | 51g (36r) | 25g (18r) | 10g (7r) | 5g (4r) | 4g (3r) |
| `eurgol` | Mine | 2500 | 12 | 51g (36r) | 25g (18r) | 10g (7r) | 5g (4r) | 4g (3r) |
| `euriro` | Mine | 2500 | 12 | 51g (36r) | 25g (18r) | 10g (7r) | 5g (4r) | 4g (3r) |
| `eurmar` | Market | 4000 | 12 | 1.4m g (1.0m r) | 41g (29r) | 16g (12r) | 8g (6r) | 7g (5r) |
| `eurmil` | Mill | 20000 | 12 | 6.8m g (4.8m r) | 3.4m g (2.4m r) | 1.4m g (1.0m r) | 41g (29r) | 34g (24r) |
| `eurpor` | Shipyard | 50000 | 16 | 16.9m g (12.1m r) | 8.5m g (6.0m r) | 3.4m g (2.4m r) | 1.7m g (1.2m r) | 1.1m g (0.8m r) |
| `eursga` | Gate | 50000 | 4 | 16.9m g (12.1m r) | 8.5m g (6.0m r) | 4.2m g (3.0m r) | 4.2m g (3.0m r) | 4.2m g (3.0m r) |
| `eursto` | Storehouse | 10000 | 12 | 3.4m g (2.4m r) | 1.7m g (1.2m r) | 41g (29r) | 20g (15r) | 17g (12r) |
| `eurswa` | Wall | 50000 | 4 | 16.9m g (12.1m r) | 8.5m g (6.0m r) | 4.2m g (3.0m r) | 4.2m g (3.0m r) | 4.2m g (3.0m r) |
| `eurtow` | Tower | 20000 | 8 | 6.8m g (4.8m r) | 3.4m g (2.4m r) | 1.4m g (1.0m r) | 51g (36r) | 51g (36r) |
| `hunaca` | Academy | 63000 | 16 | 21.3m g (15.2m r) | 10.7m g (7.6m r) | 4.3m g (3.0m r) | 2.1m g (1.5m r) | 1.3m g (1.0m r) |
| `hunart` | Artillery Depot | 40000 | 12 | 13.5m g (9.7m r) | 6.8m g (4.8m r) | 2.7m g (1.9m r) | 1.4m g (1.0m r) | 1.1m g (0.8m r) |
| `hunba2` | Barracks, 18th century | 55000 | 16 | 18.6m g (13.3m r) | 9.3m g (6.6m r) | 3.7m g (2.7m r) | 1.9m g (1.3m r) | 1.2m g (0.8m r) |
| `hunbar` | Barracks, 17th century | 40000 | 12 | 13.5m g (9.7m r) | 6.8m g (4.8m r) | 2.7m g (1.9m r) | 1.4m g (1.0m r) | 1.1m g (0.8m r) |
| `hunbla` | Blacksmith | 5500 | 12 | 1.9m g (1.3m r) | 56g (40r) | 22g (16r) | 11g (8r) | 9g (7r) |
| `huncen` | Town Hall | 4000 | 16 | 1.4m g (1.0m r) | 41g (29r) | 16g (12r) | 8g (6r) | 5g (4r) |
| `hundip` | Diplomatic Center | 4500 | 12 | 1.5m g (1.1m r) | 46g (33r) | 18g (13r) | 9g (7r) | 8g (5r) |
| `hunhou` | Housing | 4000 | 12 | 1.4m g (1.0m r) | 41g (29r) | 16g (12r) | 8g (6r) | 7g (5r) |
| `hunsta` | Stable | 20000 | 12 | 6.8m g (4.8m r) | 3.4m g (2.4m r) | 1.4m g (1.0m r) | 41g (29r) | 34g (24r) |
| `huntem` | Cathedral | 4200 | 12 | 1.4m g (1.0m r) | 43g (30r) | 17g (12r) | 9g (6r) | 7g (5r) |

## net

### Постройка с нуля

| sid | имя | buildtime_g | slot_cap | 1 builders | 2 builders | 5 builders | 10 builders | max builders |
|---|---|---|---|---|---|---|---|---|
| `eurcoa` | Mine | 94g | 12 | 1.8m g (1.3m r) | 53g (38r) | 21g (15r) | 11g (8r) | 9g (6r) |
| `eurgol` | Mine | 94g | 12 | 1.8m g (1.3m r) | 53g (38r) | 21g (15r) | 11g (8r) | 9g (6r) |
| `euriro` | Mine | 94g | 12 | 1.8m g (1.3m r) | 53g (38r) | 21g (15r) | 11g (8r) | 9g (6r) |
| `eurmar` | Market | 234g | 12 | 4.4m g (3.2m r) | 2.2m g (1.6m r) | 53g (38r) | 26g (19r) | 22g (16r) |
| `eurmil` | Mill | 94g | 12 | 1.8m g (1.3m r) | 53g (38r) | 21g (15r) | 11g (8r) | 9g (6r) |
| `eurpor` | Shipyard | 1562g | 16 | 29.4m g (21.0m r) | 14.7m g (10.5m r) | 5.9m g (4.2m r) | 2.9m g (2.1m r) | 1.8m g (1.3m r) |
| `eursga` | Gate | 90g | 4 | 1.7m g (1.2m r) | 51g (36r) | 25g (18r) | 25g (18r) | 25g (18r) |
| `eursto` | Storehouse | 31g | 12 | 35g (25r) | 18g (13r) | 7g (5r) | 4g (3r) | 3g (2r) |
| `eurswa` | Wall | 90g | 4 | 1.7m g (1.2m r) | 51g (36r) | 25g (18r) | 25g (18r) | 25g (18r) |
| `eurtow` | Tower | 1230g | 8 | 23.2m g (16.6m r) | 11.6m g (8.3m r) | 4.6m g (3.3m r) | 2.9m g (2.1m r) | 2.9m g (2.1m r) |
| `netaca` | Academy | 625g | 16 | 11.8m g (8.4m r) | 5.9m g (4.2m r) | 2.4m g (1.7m r) | 1.2m g (0.8m r) | 44g (32r) |
| `netart` | Artillery Depot | 246g | 12 | 4.6m g (3.3m r) | 2.3m g (1.7m r) | 56g (40r) | 28g (20r) | 23g (17r) |
| `netba2` | Barracks, 18th century | 5625g | 16 | 105.9m g (75.7m r) | 53.0m g (37.8m r) | 21.2m g (15.1m r) | 10.6m g (7.6m r) | 6.6m g (4.7m r) |
| `netbar` | Barracks, 17th century | 94g | 12 | 1.8m g (1.3m r) | 53g (38r) | 21g (15r) | 11g (8r) | 9g (6r) |
| `netbla` | Blacksmith | 94g | 12 | 1.8m g (1.3m r) | 53g (38r) | 21g (15r) | 11g (8r) | 9g (6r) |
| `netcen` | Town Hall | 156g | 16 | 2.9m g (2.1m r) | 1.5m g (1.1m r) | 35g (25r) | 18g (13r) | 11g (8r) |
| `netdip` | Diplomatic Center | 312g | 12 | 5.9m g (4.2m r) | 2.9m g (2.1m r) | 1.2m g (0.8m r) | 35g (25r) | 29g (21r) |
| `nethou` | Housing | 31g | 12 | 35g (25r) | 18g (13r) | 7g (5r) | 4g (3r) | 3g (2r) |
| `netsta` | Stable | 625g | 12 | 11.8m g (8.4m r) | 5.9m g (4.2m r) | 2.4m g (1.7m r) | 1.2m g (0.8m r) | 59g (42r) |
| `nettem` | Cathedral | 156g | 12 | 2.9m g (2.1m r) | 1.5m g (1.1m r) | 35g (25r) | 18g (13r) | 15g (11r) |

### Полный ремонт (0 → max HP)

| sid | имя | maxhp | slot_cap | 1 builders | 2 builders | 5 builders | 10 builders | max builders |
|---|---|---|---|---|---|---|---|---|
| `eurcoa` | Mine | 2500 | 12 | 51g (36r) | 25g (18r) | 10g (7r) | 5g (4r) | 4g (3r) |
| `eurgol` | Mine | 2500 | 12 | 51g (36r) | 25g (18r) | 10g (7r) | 5g (4r) | 4g (3r) |
| `euriro` | Mine | 2500 | 12 | 51g (36r) | 25g (18r) | 10g (7r) | 5g (4r) | 4g (3r) |
| `eurmar` | Market | 4000 | 12 | 1.4m g (1.0m r) | 41g (29r) | 16g (12r) | 8g (6r) | 7g (5r) |
| `eurmil` | Mill | 20000 | 12 | 6.8m g (4.8m r) | 3.4m g (2.4m r) | 1.4m g (1.0m r) | 41g (29r) | 34g (24r) |
| `eurpor` | Shipyard | 50000 | 16 | 16.9m g (12.1m r) | 8.5m g (6.0m r) | 3.4m g (2.4m r) | 1.7m g (1.2m r) | 1.1m g (0.8m r) |
| `eursga` | Gate | 50000 | 4 | 16.9m g (12.1m r) | 8.5m g (6.0m r) | 4.2m g (3.0m r) | 4.2m g (3.0m r) | 4.2m g (3.0m r) |
| `eursto` | Storehouse | 10000 | 12 | 3.4m g (2.4m r) | 1.7m g (1.2m r) | 41g (29r) | 20g (15r) | 17g (12r) |
| `eurswa` | Wall | 50000 | 4 | 16.9m g (12.1m r) | 8.5m g (6.0m r) | 4.2m g (3.0m r) | 4.2m g (3.0m r) | 4.2m g (3.0m r) |
| `eurtow` | Tower | 20000 | 8 | 6.8m g (4.8m r) | 3.4m g (2.4m r) | 1.4m g (1.0m r) | 51g (36r) | 51g (36r) |
| `netaca` | Academy | 63000 | 16 | 21.3m g (15.2m r) | 10.7m g (7.6m r) | 4.3m g (3.0m r) | 2.1m g (1.5m r) | 1.3m g (1.0m r) |
| `netart` | Artillery Depot | 40000 | 12 | 13.5m g (9.7m r) | 6.8m g (4.8m r) | 2.7m g (1.9m r) | 1.4m g (1.0m r) | 1.1m g (0.8m r) |
| `netba2` | Barracks, 18th century | 55000 | 16 | 18.6m g (13.3m r) | 9.3m g (6.6m r) | 3.7m g (2.7m r) | 1.9m g (1.3m r) | 1.2m g (0.8m r) |
| `netbar` | Barracks, 17th century | 40000 | 12 | 13.5m g (9.7m r) | 6.8m g (4.8m r) | 2.7m g (1.9m r) | 1.4m g (1.0m r) | 1.1m g (0.8m r) |
| `netbla` | Blacksmith | 5500 | 12 | 1.9m g (1.3m r) | 56g (40r) | 22g (16r) | 11g (8r) | 9g (7r) |
| `netcen` | Town Hall | 4950 | 16 | 1.7m g (1.2m r) | 50g (36r) | 20g (14r) | 10g (7r) | 6g (4r) |
| `netdip` | Diplomatic Center | 4500 | 12 | 1.5m g (1.1m r) | 46g (33r) | 18g (13r) | 9g (7r) | 8g (5r) |
| `nethou` | Housing | 4500 | 12 | 1.5m g (1.1m r) | 46g (33r) | 18g (13r) | 9g (7r) | 8g (5r) |
| `netsta` | Stable | 20000 | 12 | 6.8m g (4.8m r) | 3.4m g (2.4m r) | 1.4m g (1.0m r) | 41g (29r) | 34g (24r) |
| `nettem` | Cathedral | 4200 | 12 | 1.4m g (1.0m r) | 43g (30r) | 17g (12r) | 9g (6r) | 7g (5r) |

## pie

### Постройка с нуля

| sid | имя | buildtime_g | slot_cap | 1 builders | 2 builders | 5 builders | 10 builders | max builders |
|---|---|---|---|---|---|---|---|---|
| `eurcoa` | Mine | 94g | 12 | 1.8m g (1.3m r) | 53g (38r) | 21g (15r) | 11g (8r) | 9g (6r) |
| `eurgol` | Mine | 94g | 12 | 1.8m g (1.3m r) | 53g (38r) | 21g (15r) | 11g (8r) | 9g (6r) |
| `euriro` | Mine | 94g | 12 | 1.8m g (1.3m r) | 53g (38r) | 21g (15r) | 11g (8r) | 9g (6r) |
| `eurmar` | Market | 234g | 12 | 4.4m g (3.2m r) | 2.2m g (1.6m r) | 53g (38r) | 26g (19r) | 22g (16r) |
| `eurmil` | Mill | 94g | 12 | 1.8m g (1.3m r) | 53g (38r) | 21g (15r) | 11g (8r) | 9g (6r) |
| `eurpor` | Shipyard | 1562g | 16 | 29.4m g (21.0m r) | 14.7m g (10.5m r) | 5.9m g (4.2m r) | 2.9m g (2.1m r) | 1.8m g (1.3m r) |
| `eursga` | Gate | 90g | 4 | 1.7m g (1.2m r) | 51g (36r) | 25g (18r) | 25g (18r) | 25g (18r) |
| `eursto` | Storehouse | 31g | 12 | 35g (25r) | 18g (13r) | 7g (5r) | 4g (3r) | 3g (2r) |
| `eurswa` | Wall | 90g | 4 | 1.7m g (1.2m r) | 51g (36r) | 25g (18r) | 25g (18r) | 25g (18r) |
| `eurtow` | Tower | 1230g | 8 | 23.2m g (16.6m r) | 11.6m g (8.3m r) | 4.6m g (3.3m r) | 2.9m g (2.1m r) | 2.9m g (2.1m r) |
| `pieaca` | Academy | 625g | 16 | 11.8m g (8.4m r) | 5.9m g (4.2m r) | 2.4m g (1.7m r) | 1.2m g (0.8m r) | 44g (32r) |
| `pieart` | Artillery Depot | 246g | 12 | 4.6m g (3.3m r) | 2.3m g (1.7m r) | 56g (40r) | 28g (20r) | 23g (17r) |
| `pieba2` | Barracks, 18th century | 5625g | 16 | 105.9m g (75.7m r) | 53.0m g (37.8m r) | 21.2m g (15.1m r) | 10.6m g (7.6m r) | 6.6m g (4.7m r) |
| `piebar` | Barracks, 17th century | 94g | 12 | 1.8m g (1.3m r) | 53g (38r) | 21g (15r) | 11g (8r) | 9g (6r) |
| `piebla` | Blacksmith | 94g | 12 | 1.8m g (1.3m r) | 53g (38r) | 21g (15r) | 11g (8r) | 9g (6r) |
| `piecen` | Town Hall | 156g | 16 | 2.9m g (2.1m r) | 1.5m g (1.1m r) | 35g (25r) | 18g (13r) | 11g (8r) |
| `piedip` | Diplomatic Center | 312g | 12 | 5.9m g (4.2m r) | 2.9m g (2.1m r) | 1.2m g (0.8m r) | 35g (25r) | 29g (21r) |
| `piehou` | Housing | 31g | 12 | 35g (25r) | 18g (13r) | 7g (5r) | 4g (3r) | 3g (2r) |
| `piesta` | Stable | 625g | 12 | 11.8m g (8.4m r) | 5.9m g (4.2m r) | 2.4m g (1.7m r) | 1.2m g (0.8m r) | 59g (42r) |
| `pietem` | Cathedral | 156g | 12 | 2.9m g (2.1m r) | 1.5m g (1.1m r) | 35g (25r) | 18g (13r) | 15g (11r) |

### Полный ремонт (0 → max HP)

| sid | имя | maxhp | slot_cap | 1 builders | 2 builders | 5 builders | 10 builders | max builders |
|---|---|---|---|---|---|---|---|---|
| `eurcoa` | Mine | 2500 | 12 | 51g (36r) | 25g (18r) | 10g (7r) | 5g (4r) | 4g (3r) |
| `eurgol` | Mine | 2500 | 12 | 51g (36r) | 25g (18r) | 10g (7r) | 5g (4r) | 4g (3r) |
| `euriro` | Mine | 2500 | 12 | 51g (36r) | 25g (18r) | 10g (7r) | 5g (4r) | 4g (3r) |
| `eurmar` | Market | 4000 | 12 | 1.4m g (1.0m r) | 41g (29r) | 16g (12r) | 8g (6r) | 7g (5r) |
| `eurmil` | Mill | 20000 | 12 | 6.8m g (4.8m r) | 3.4m g (2.4m r) | 1.4m g (1.0m r) | 41g (29r) | 34g (24r) |
| `eurpor` | Shipyard | 50000 | 16 | 16.9m g (12.1m r) | 8.5m g (6.0m r) | 3.4m g (2.4m r) | 1.7m g (1.2m r) | 1.1m g (0.8m r) |
| `eursga` | Gate | 50000 | 4 | 16.9m g (12.1m r) | 8.5m g (6.0m r) | 4.2m g (3.0m r) | 4.2m g (3.0m r) | 4.2m g (3.0m r) |
| `eursto` | Storehouse | 10000 | 12 | 3.4m g (2.4m r) | 1.7m g (1.2m r) | 41g (29r) | 20g (15r) | 17g (12r) |
| `eurswa` | Wall | 50000 | 4 | 16.9m g (12.1m r) | 8.5m g (6.0m r) | 4.2m g (3.0m r) | 4.2m g (3.0m r) | 4.2m g (3.0m r) |
| `eurtow` | Tower | 20000 | 8 | 6.8m g (4.8m r) | 3.4m g (2.4m r) | 1.4m g (1.0m r) | 51g (36r) | 51g (36r) |
| `pieaca` | Academy | 63000 | 16 | 21.3m g (15.2m r) | 10.7m g (7.6m r) | 4.3m g (3.0m r) | 2.1m g (1.5m r) | 1.3m g (1.0m r) |
| `pieart` | Artillery Depot | 40000 | 12 | 13.5m g (9.7m r) | 6.8m g (4.8m r) | 2.7m g (1.9m r) | 1.4m g (1.0m r) | 1.1m g (0.8m r) |
| `pieba2` | Barracks, 18th century | 55000 | 16 | 18.6m g (13.3m r) | 9.3m g (6.6m r) | 3.7m g (2.7m r) | 1.9m g (1.3m r) | 1.2m g (0.8m r) |
| `piebar` | Barracks, 17th century | 40000 | 12 | 13.5m g (9.7m r) | 6.8m g (4.8m r) | 2.7m g (1.9m r) | 1.4m g (1.0m r) | 1.1m g (0.8m r) |
| `piebla` | Blacksmith | 5500 | 12 | 1.9m g (1.3m r) | 56g (40r) | 22g (16r) | 11g (8r) | 9g (7r) |
| `piecen` | Town Hall | 4000 | 16 | 1.4m g (1.0m r) | 41g (29r) | 16g (12r) | 8g (6r) | 5g (4r) |
| `piedip` | Diplomatic Center | 4500 | 12 | 1.5m g (1.1m r) | 46g (33r) | 18g (13r) | 9g (7r) | 8g (5r) |
| `piehou` | Housing | 4000 | 12 | 1.4m g (1.0m r) | 41g (29r) | 16g (12r) | 8g (6r) | 7g (5r) |
| `piesta` | Stable | 20000 | 12 | 6.8m g (4.8m r) | 3.4m g (2.4m r) | 1.4m g (1.0m r) | 41g (29r) | 34g (24r) |
| `pietem` | Cathedral | 4200 | 12 | 1.4m g (1.0m r) | 43g (30r) | 17g (12r) | 9g (6r) | 7g (5r) |

## pol

### Постройка с нуля

| sid | имя | buildtime_g | slot_cap | 1 builders | 2 builders | 5 builders | 10 builders | max builders |
|---|---|---|---|---|---|---|---|---|
| `eurcoa` | Mine | 94g | 12 | 1.8m g (1.3m r) | 53g (38r) | 21g (15r) | 11g (8r) | 9g (6r) |
| `eurgol` | Mine | 94g | 12 | 1.8m g (1.3m r) | 53g (38r) | 21g (15r) | 11g (8r) | 9g (6r) |
| `euriro` | Mine | 94g | 12 | 1.8m g (1.3m r) | 53g (38r) | 21g (15r) | 11g (8r) | 9g (6r) |
| `eurmar` | Market | 234g | 12 | 4.4m g (3.2m r) | 2.2m g (1.6m r) | 53g (38r) | 26g (19r) | 22g (16r) |
| `eurmil` | Mill | 94g | 12 | 1.8m g (1.3m r) | 53g (38r) | 21g (15r) | 11g (8r) | 9g (6r) |
| `eurpor` | Shipyard | 1562g | 16 | 29.4m g (21.0m r) | 14.7m g (10.5m r) | 5.9m g (4.2m r) | 2.9m g (2.1m r) | 1.8m g (1.3m r) |
| `eursga` | Gate | 90g | 4 | 1.7m g (1.2m r) | 51g (36r) | 25g (18r) | 25g (18r) | 25g (18r) |
| `eurswa` | Wall | 90g | 4 | 1.7m g (1.2m r) | 51g (36r) | 25g (18r) | 25g (18r) | 25g (18r) |
| `eurtow` | Tower | 1230g | 8 | 23.2m g (16.6m r) | 11.6m g (8.3m r) | 4.6m g (3.3m r) | 2.9m g (2.1m r) | 2.9m g (2.1m r) |
| `polaca` | Academy | 625g | 16 | 11.8m g (8.4m r) | 5.9m g (4.2m r) | 2.4m g (1.7m r) | 1.2m g (0.8m r) | 44g (32r) |
| `polart` | Artillery Depot | 246g | 12 | 4.6m g (3.3m r) | 2.3m g (1.7m r) | 56g (40r) | 28g (20r) | 23g (17r) |
| `polba2` | Barracks, 18th century | 5625g | 16 | 105.9m g (75.7m r) | 53.0m g (37.8m r) | 21.2m g (15.1m r) | 10.6m g (7.6m r) | 6.6m g (4.7m r) |
| `polbar` | Barracks, 17th century | 94g | 12 | 1.8m g (1.3m r) | 53g (38r) | 21g (15r) | 11g (8r) | 9g (6r) |
| `polbla` | Blacksmith | 94g | 12 | 1.8m g (1.3m r) | 53g (38r) | 21g (15r) | 11g (8r) | 9g (6r) |
| `polcen` | Town Hall | 156g | 16 | 2.9m g (2.1m r) | 1.5m g (1.1m r) | 35g (25r) | 18g (13r) | 11g (8r) |
| `poldip` | Diplomatic Center | 312g | 12 | 5.9m g (4.2m r) | 2.9m g (2.1m r) | 1.2m g (0.8m r) | 35g (25r) | 29g (21r) |
| `polhou` | Housing | 31g | 12 | 35g (25r) | 18g (13r) | 7g (5r) | 4g (3r) | 3g (2r) |
| `polsta` | Stable | 625g | 12 | 11.8m g (8.4m r) | 5.9m g (4.2m r) | 2.4m g (1.7m r) | 1.2m g (0.8m r) | 59g (42r) |
| `poltem` | Cathedral | 156g | 12 | 2.9m g (2.1m r) | 1.5m g (1.1m r) | 35g (25r) | 18g (13r) | 15g (11r) |
| `russto` | Storehouse | 31g | 12 | 35g (25r) | 18g (13r) | 7g (5r) | 4g (3r) | 3g (2r) |

### Полный ремонт (0 → max HP)

| sid | имя | maxhp | slot_cap | 1 builders | 2 builders | 5 builders | 10 builders | max builders |
|---|---|---|---|---|---|---|---|---|
| `eurcoa` | Mine | 2500 | 12 | 51g (36r) | 25g (18r) | 10g (7r) | 5g (4r) | 4g (3r) |
| `eurgol` | Mine | 2500 | 12 | 51g (36r) | 25g (18r) | 10g (7r) | 5g (4r) | 4g (3r) |
| `euriro` | Mine | 2500 | 12 | 51g (36r) | 25g (18r) | 10g (7r) | 5g (4r) | 4g (3r) |
| `eurmar` | Market | 4000 | 12 | 1.4m g (1.0m r) | 41g (29r) | 16g (12r) | 8g (6r) | 7g (5r) |
| `eurmil` | Mill | 20000 | 12 | 6.8m g (4.8m r) | 3.4m g (2.4m r) | 1.4m g (1.0m r) | 41g (29r) | 34g (24r) |
| `eurpor` | Shipyard | 50000 | 16 | 16.9m g (12.1m r) | 8.5m g (6.0m r) | 3.4m g (2.4m r) | 1.7m g (1.2m r) | 1.1m g (0.8m r) |
| `eursga` | Gate | 50000 | 4 | 16.9m g (12.1m r) | 8.5m g (6.0m r) | 4.2m g (3.0m r) | 4.2m g (3.0m r) | 4.2m g (3.0m r) |
| `eurswa` | Wall | 50000 | 4 | 16.9m g (12.1m r) | 8.5m g (6.0m r) | 4.2m g (3.0m r) | 4.2m g (3.0m r) | 4.2m g (3.0m r) |
| `eurtow` | Tower | 20000 | 8 | 6.8m g (4.8m r) | 3.4m g (2.4m r) | 1.4m g (1.0m r) | 51g (36r) | 51g (36r) |
| `polaca` | Academy | 63000 | 16 | 21.3m g (15.2m r) | 10.7m g (7.6m r) | 4.3m g (3.0m r) | 2.1m g (1.5m r) | 1.3m g (1.0m r) |
| `polart` | Artillery Depot | 40000 | 12 | 13.5m g (9.7m r) | 6.8m g (4.8m r) | 2.7m g (1.9m r) | 1.4m g (1.0m r) | 1.1m g (0.8m r) |
| `polba2` | Barracks, 18th century | 55000 | 16 | 18.6m g (13.3m r) | 9.3m g (6.6m r) | 3.7m g (2.7m r) | 1.9m g (1.3m r) | 1.2m g (0.8m r) |
| `polbar` | Barracks, 17th century | 40000 | 12 | 13.5m g (9.7m r) | 6.8m g (4.8m r) | 2.7m g (1.9m r) | 1.4m g (1.0m r) | 1.1m g (0.8m r) |
| `polbla` | Blacksmith | 5500 | 12 | 1.9m g (1.3m r) | 56g (40r) | 22g (16r) | 11g (8r) | 9g (7r) |
| `polcen` | Town Hall | 4300 | 16 | 1.5m g (1.0m r) | 44g (31r) | 17g (12r) | 9g (6r) | 5g (4r) |
| `poldip` | Diplomatic Center | 4500 | 12 | 1.5m g (1.1m r) | 46g (33r) | 18g (13r) | 9g (7r) | 8g (5r) |
| `polhou` | Housing | 4100 | 12 | 1.4m g (1.0m r) | 42g (30r) | 17g (12r) | 8g (6r) | 7g (5r) |
| `polsta` | Stable | 20000 | 12 | 6.8m g (4.8m r) | 3.4m g (2.4m r) | 1.4m g (1.0m r) | 41g (29r) | 34g (24r) |
| `poltem` | Cathedral | 4200 | 12 | 1.4m g (1.0m r) | 43g (30r) | 17g (12r) | 9g (6r) | 7g (5r) |
| `russto` | Storehouse | 10000 | 12 | 3.4m g (2.4m r) | 1.7m g (1.2m r) | 41g (29r) | 20g (15r) | 17g (12r) |

## por

### Постройка с нуля

| sid | имя | buildtime_g | slot_cap | 1 builders | 2 builders | 5 builders | 10 builders | max builders |
|---|---|---|---|---|---|---|---|---|
| `eurcoa` | Mine | 94g | 12 | 1.8m g (1.3m r) | 53g (38r) | 21g (15r) | 11g (8r) | 9g (6r) |
| `eurgol` | Mine | 94g | 12 | 1.8m g (1.3m r) | 53g (38r) | 21g (15r) | 11g (8r) | 9g (6r) |
| `euriro` | Mine | 94g | 12 | 1.8m g (1.3m r) | 53g (38r) | 21g (15r) | 11g (8r) | 9g (6r) |
| `eurmil` | Mill | 94g | 12 | 1.8m g (1.3m r) | 53g (38r) | 21g (15r) | 11g (8r) | 9g (6r) |
| `eursga` | Gate | 90g | 4 | 1.7m g (1.2m r) | 51g (36r) | 25g (18r) | 25g (18r) | 25g (18r) |
| `eurswa` | Wall | 90g | 4 | 1.7m g (1.2m r) | 51g (36r) | 25g (18r) | 25g (18r) | 25g (18r) |
| `eurtow` | Tower | 1230g | 8 | 23.2m g (16.6m r) | 11.6m g (8.3m r) | 4.6m g (3.3m r) | 2.9m g (2.1m r) | 2.9m g (2.1m r) |
| `poraca` | Academy | 625g | 16 | 11.8m g (8.4m r) | 5.9m g (4.2m r) | 2.4m g (1.7m r) | 1.2m g (0.8m r) | 44g (32r) |
| `porart` | Artillery Depot | 246g | 12 | 4.6m g (3.3m r) | 2.3m g (1.7m r) | 56g (40r) | 28g (20r) | 23g (17r) |
| `porba2` | Barracks, 18th century | 5625g | 16 | 105.9m g (75.7m r) | 53.0m g (37.8m r) | 21.2m g (15.1m r) | 10.6m g (7.6m r) | 6.6m g (4.7m r) |
| `porbar` | Barracks, 17th century | 94g | 12 | 1.8m g (1.3m r) | 53g (38r) | 21g (15r) | 11g (8r) | 9g (6r) |
| `porbla` | Blacksmith | 94g | 12 | 1.8m g (1.3m r) | 53g (38r) | 21g (15r) | 11g (8r) | 9g (6r) |
| `porcen` | Town Hall | 156g | 16 | 2.9m g (2.1m r) | 1.5m g (1.1m r) | 35g (25r) | 18g (13r) | 11g (8r) |
| `pordip` | Diplomatic Center | 312g | 12 | 5.9m g (4.2m r) | 2.9m g (2.1m r) | 1.2m g (0.8m r) | 35g (25r) | 29g (21r) |
| `porhou` | Housing | 31g | 12 | 35g (25r) | 18g (13r) | 7g (5r) | 4g (3r) | 3g (2r) |
| `porpor` | Shipyard | 1562g | 16 | 29.4m g (21.0m r) | 14.7m g (10.5m r) | 5.9m g (4.2m r) | 2.9m g (2.1m r) | 1.8m g (1.3m r) |
| `porsta` | Stable | 625g | 12 | 11.8m g (8.4m r) | 5.9m g (4.2m r) | 2.4m g (1.7m r) | 1.2m g (0.8m r) | 59g (42r) |
| `portem` | Cathedral | 156g | 12 | 2.9m g (2.1m r) | 1.5m g (1.1m r) | 35g (25r) | 18g (13r) | 15g (11r) |
| `spamar` | Market | 156g | 12 | 2.9m g (2.1m r) | 1.5m g (1.1m r) | 35g (25r) | 18g (13r) | 15g (11r) |
| `spasto` | Storehouse | 31g | 12 | 35g (25r) | 18g (13r) | 7g (5r) | 4g (3r) | 3g (2r) |

### Полный ремонт (0 → max HP)

| sid | имя | maxhp | slot_cap | 1 builders | 2 builders | 5 builders | 10 builders | max builders |
|---|---|---|---|---|---|---|---|---|
| `eurcoa` | Mine | 2500 | 12 | 51g (36r) | 25g (18r) | 10g (7r) | 5g (4r) | 4g (3r) |
| `eurgol` | Mine | 2500 | 12 | 51g (36r) | 25g (18r) | 10g (7r) | 5g (4r) | 4g (3r) |
| `euriro` | Mine | 2500 | 12 | 51g (36r) | 25g (18r) | 10g (7r) | 5g (4r) | 4g (3r) |
| `eurmil` | Mill | 20000 | 12 | 6.8m g (4.8m r) | 3.4m g (2.4m r) | 1.4m g (1.0m r) | 41g (29r) | 34g (24r) |
| `eursga` | Gate | 50000 | 4 | 16.9m g (12.1m r) | 8.5m g (6.0m r) | 4.2m g (3.0m r) | 4.2m g (3.0m r) | 4.2m g (3.0m r) |
| `eurswa` | Wall | 50000 | 4 | 16.9m g (12.1m r) | 8.5m g (6.0m r) | 4.2m g (3.0m r) | 4.2m g (3.0m r) | 4.2m g (3.0m r) |
| `eurtow` | Tower | 20000 | 8 | 6.8m g (4.8m r) | 3.4m g (2.4m r) | 1.4m g (1.0m r) | 51g (36r) | 51g (36r) |
| `poraca` | Academy | 63000 | 16 | 21.3m g (15.2m r) | 10.7m g (7.6m r) | 4.3m g (3.0m r) | 2.1m g (1.5m r) | 1.3m g (1.0m r) |
| `porart` | Artillery Depot | 40000 | 12 | 13.5m g (9.7m r) | 6.8m g (4.8m r) | 2.7m g (1.9m r) | 1.4m g (1.0m r) | 1.1m g (0.8m r) |
| `porba2` | Barracks, 18th century | 55000 | 16 | 18.6m g (13.3m r) | 9.3m g (6.6m r) | 3.7m g (2.7m r) | 1.9m g (1.3m r) | 1.2m g (0.8m r) |
| `porbar` | Barracks, 17th century | 40000 | 12 | 13.5m g (9.7m r) | 6.8m g (4.8m r) | 2.7m g (1.9m r) | 1.4m g (1.0m r) | 1.1m g (0.8m r) |
| `porbla` | Blacksmith | 5500 | 12 | 1.9m g (1.3m r) | 56g (40r) | 22g (16r) | 11g (8r) | 9g (7r) |
| `porcen` | Town Hall | 4000 | 16 | 1.4m g (1.0m r) | 41g (29r) | 16g (12r) | 8g (6r) | 5g (4r) |
| `pordip` | Diplomatic Center | 4500 | 12 | 1.5m g (1.1m r) | 46g (33r) | 18g (13r) | 9g (7r) | 8g (5r) |
| `porhou` | Housing | 4000 | 12 | 1.4m g (1.0m r) | 41g (29r) | 16g (12r) | 8g (6r) | 7g (5r) |
| `porpor` | Shipyard | 50000 | 16 | 16.9m g (12.1m r) | 8.5m g (6.0m r) | 3.4m g (2.4m r) | 1.7m g (1.2m r) | 1.1m g (0.8m r) |
| `porsta` | Stable | 20000 | 12 | 6.8m g (4.8m r) | 3.4m g (2.4m r) | 1.4m g (1.0m r) | 41g (29r) | 34g (24r) |
| `portem` | Cathedral | 4200 | 12 | 1.4m g (1.0m r) | 43g (30r) | 17g (12r) | 9g (6r) | 7g (5r) |
| `spamar` | Market | 4000 | 12 | 1.4m g (1.0m r) | 41g (29r) | 16g (12r) | 8g (6r) | 7g (5r) |
| `spasto` | Storehouse | 10000 | 12 | 3.4m g (2.4m r) | 1.7m g (1.2m r) | 41g (29r) | 20g (15r) | 17g (12r) |

## pru

### Постройка с нуля

| sid | имя | buildtime_g | slot_cap | 1 builders | 2 builders | 5 builders | 10 builders | max builders |
|---|---|---|---|---|---|---|---|---|
| `eurcoa` | Mine | 94g | 12 | 1.8m g (1.3m r) | 53g (38r) | 21g (15r) | 11g (8r) | 9g (6r) |
| `eurgol` | Mine | 94g | 12 | 1.8m g (1.3m r) | 53g (38r) | 21g (15r) | 11g (8r) | 9g (6r) |
| `euriro` | Mine | 94g | 12 | 1.8m g (1.3m r) | 53g (38r) | 21g (15r) | 11g (8r) | 9g (6r) |
| `eurmar` | Market | 234g | 12 | 4.4m g (3.2m r) | 2.2m g (1.6m r) | 53g (38r) | 26g (19r) | 22g (16r) |
| `eurmil` | Mill | 94g | 12 | 1.8m g (1.3m r) | 53g (38r) | 21g (15r) | 11g (8r) | 9g (6r) |
| `eurpor` | Shipyard | 1562g | 16 | 29.4m g (21.0m r) | 14.7m g (10.5m r) | 5.9m g (4.2m r) | 2.9m g (2.1m r) | 1.8m g (1.3m r) |
| `eursga` | Gate | 90g | 4 | 1.7m g (1.2m r) | 51g (36r) | 25g (18r) | 25g (18r) | 25g (18r) |
| `eursto` | Storehouse | 31g | 12 | 35g (25r) | 18g (13r) | 7g (5r) | 4g (3r) | 3g (2r) |
| `eurswa` | Wall | 90g | 4 | 1.7m g (1.2m r) | 51g (36r) | 25g (18r) | 25g (18r) | 25g (18r) |
| `eurtow` | Tower | 1230g | 8 | 23.2m g (16.6m r) | 11.6m g (8.3m r) | 4.6m g (3.3m r) | 2.9m g (2.1m r) | 2.9m g (2.1m r) |
| `pruaca` | Academy | 625g | 16 | 11.8m g (8.4m r) | 5.9m g (4.2m r) | 2.4m g (1.7m r) | 1.2m g (0.8m r) | 44g (32r) |
| `pruart` | Artillery Depot | 246g | 12 | 4.6m g (3.3m r) | 2.3m g (1.7m r) | 56g (40r) | 28g (20r) | 23g (17r) |
| `pruba2` | Barracks, 18th century | 5625g | 16 | 105.9m g (75.7m r) | 53.0m g (37.8m r) | 21.2m g (15.1m r) | 10.6m g (7.6m r) | 6.6m g (4.7m r) |
| `prubar` | Barracks, 17th century | 94g | 12 | 1.8m g (1.3m r) | 53g (38r) | 21g (15r) | 11g (8r) | 9g (6r) |
| `prubla` | Blacksmith | 94g | 12 | 1.8m g (1.3m r) | 53g (38r) | 21g (15r) | 11g (8r) | 9g (6r) |
| `prucen` | Town Hall | 156g | 16 | 2.9m g (2.1m r) | 1.5m g (1.1m r) | 35g (25r) | 18g (13r) | 11g (8r) |
| `prudip` | Diplomatic Center | 312g | 12 | 5.9m g (4.2m r) | 2.9m g (2.1m r) | 1.2m g (0.8m r) | 35g (25r) | 29g (21r) |
| `pruhou` | Housing | 31g | 12 | 35g (25r) | 18g (13r) | 7g (5r) | 4g (3r) | 3g (2r) |
| `prusta` | Stable | 625g | 12 | 11.8m g (8.4m r) | 5.9m g (4.2m r) | 2.4m g (1.7m r) | 1.2m g (0.8m r) | 59g (42r) |
| `prutem` | Cathedral | 156g | 12 | 2.9m g (2.1m r) | 1.5m g (1.1m r) | 35g (25r) | 18g (13r) | 15g (11r) |

### Полный ремонт (0 → max HP)

| sid | имя | maxhp | slot_cap | 1 builders | 2 builders | 5 builders | 10 builders | max builders |
|---|---|---|---|---|---|---|---|---|
| `eurcoa` | Mine | 2500 | 12 | 51g (36r) | 25g (18r) | 10g (7r) | 5g (4r) | 4g (3r) |
| `eurgol` | Mine | 2500 | 12 | 51g (36r) | 25g (18r) | 10g (7r) | 5g (4r) | 4g (3r) |
| `euriro` | Mine | 2500 | 12 | 51g (36r) | 25g (18r) | 10g (7r) | 5g (4r) | 4g (3r) |
| `eurmar` | Market | 4000 | 12 | 1.4m g (1.0m r) | 41g (29r) | 16g (12r) | 8g (6r) | 7g (5r) |
| `eurmil` | Mill | 20000 | 12 | 6.8m g (4.8m r) | 3.4m g (2.4m r) | 1.4m g (1.0m r) | 41g (29r) | 34g (24r) |
| `eurpor` | Shipyard | 50000 | 16 | 16.9m g (12.1m r) | 8.5m g (6.0m r) | 3.4m g (2.4m r) | 1.7m g (1.2m r) | 1.1m g (0.8m r) |
| `eursga` | Gate | 50000 | 4 | 16.9m g (12.1m r) | 8.5m g (6.0m r) | 4.2m g (3.0m r) | 4.2m g (3.0m r) | 4.2m g (3.0m r) |
| `eursto` | Storehouse | 10000 | 12 | 3.4m g (2.4m r) | 1.7m g (1.2m r) | 41g (29r) | 20g (15r) | 17g (12r) |
| `eurswa` | Wall | 50000 | 4 | 16.9m g (12.1m r) | 8.5m g (6.0m r) | 4.2m g (3.0m r) | 4.2m g (3.0m r) | 4.2m g (3.0m r) |
| `eurtow` | Tower | 20000 | 8 | 6.8m g (4.8m r) | 3.4m g (2.4m r) | 1.4m g (1.0m r) | 51g (36r) | 51g (36r) |
| `pruaca` | Academy | 63000 | 16 | 21.3m g (15.2m r) | 10.7m g (7.6m r) | 4.3m g (3.0m r) | 2.1m g (1.5m r) | 1.3m g (1.0m r) |
| `pruart` | Artillery Depot | 40000 | 12 | 13.5m g (9.7m r) | 6.8m g (4.8m r) | 2.7m g (1.9m r) | 1.4m g (1.0m r) | 1.1m g (0.8m r) |
| `pruba2` | Barracks, 18th century | 55000 | 16 | 18.6m g (13.3m r) | 9.3m g (6.6m r) | 3.7m g (2.7m r) | 1.9m g (1.3m r) | 1.2m g (0.8m r) |
| `prubar` | Barracks, 17th century | 40000 | 12 | 13.5m g (9.7m r) | 6.8m g (4.8m r) | 2.7m g (1.9m r) | 1.4m g (1.0m r) | 1.1m g (0.8m r) |
| `prubla` | Blacksmith | 5500 | 12 | 1.9m g (1.3m r) | 56g (40r) | 22g (16r) | 11g (8r) | 9g (7r) |
| `prucen` | Town Hall | 4200 | 16 | 1.4m g (1.0m r) | 43g (30r) | 17g (12r) | 9g (6r) | 5g (4r) |
| `prudip` | Diplomatic Center | 4500 | 12 | 1.5m g (1.1m r) | 46g (33r) | 18g (13r) | 9g (7r) | 8g (5r) |
| `pruhou` | Housing | 4500 | 12 | 1.5m g (1.1m r) | 46g (33r) | 18g (13r) | 9g (7r) | 8g (5r) |
| `prusta` | Stable | 20000 | 12 | 6.8m g (4.8m r) | 3.4m g (2.4m r) | 1.4m g (1.0m r) | 41g (29r) | 34g (24r) |
| `prutem` | Cathedral | 4200 | 12 | 1.4m g (1.0m r) | 43g (30r) | 17g (12r) | 9g (6r) | 7g (5r) |

## rus

### Постройка с нуля

| sid | имя | buildtime_g | slot_cap | 1 builders | 2 builders | 5 builders | 10 builders | max builders |
|---|---|---|---|---|---|---|---|---|
| `eurcoa` | Mine | 94g | 12 | 1.8m g (1.3m r) | 53g (38r) | 21g (15r) | 11g (8r) | 9g (6r) |
| `eurgol` | Mine | 94g | 12 | 1.8m g (1.3m r) | 53g (38r) | 21g (15r) | 11g (8r) | 9g (6r) |
| `euriro` | Mine | 94g | 12 | 1.8m g (1.3m r) | 53g (38r) | 21g (15r) | 11g (8r) | 9g (6r) |
| `rusaca` | Academy | 844g | 16 | 15.9m g (11.4m r) | 7.9m g (5.7m r) | 3.2m g (2.3m r) | 1.6m g (1.1m r) | 60g (43r) |
| `rusart` | Artillery Depot | 246g | 12 | 4.6m g (3.3m r) | 2.3m g (1.7m r) | 56g (40r) | 28g (20r) | 23g (17r) |
| `rusba2` | Barracks, 18th century | 5625g | 16 | 105.9m g (75.7m r) | 53.0m g (37.8m r) | 21.2m g (15.1m r) | 10.6m g (7.6m r) | 6.6m g (4.7m r) |
| `rusbar` | Strelets Barracks | 78g | 12 | 1.5m g (1.1m r) | 44g (32r) | 18g (13r) | 9g (6r) | 7g (5r) |
| `rusbla` | Blacksmith | 94g | 12 | 1.8m g (1.3m r) | 53g (38r) | 21g (15r) | 11g (8r) | 9g (6r) |
| `ruscen` | Town Hall | 156g | 16 | 2.9m g (2.1m r) | 1.5m g (1.1m r) | 35g (25r) | 18g (13r) | 11g (8r) |
| `rusdip` | Diplomatic Center | 312g | 12 | 5.9m g (4.2m r) | 2.9m g (2.1m r) | 1.2m g (0.8m r) | 35g (25r) | 29g (21r) |
| `rushou` | Izba | 31g | 12 | 35g (25r) | 18g (13r) | 7g (5r) | 4g (3r) | 3g (2r) |
| `rusmar` | Market | 234g | 12 | 4.4m g (3.2m r) | 2.2m g (1.6m r) | 53g (38r) | 26g (19r) | 22g (16r) |
| `rusmil` | Mill | 94g | 12 | 1.8m g (1.3m r) | 53g (38r) | 21g (15r) | 11g (8r) | 9g (6r) |
| `ruspor` | Shipyard | 1562g | 16 | 29.4m g (21.0m r) | 14.7m g (10.5m r) | 5.9m g (4.2m r) | 2.9m g (2.1m r) | 1.8m g (1.3m r) |
| `russga` | Gate | 200g | 4 | 3.8m g (2.7m r) | 1.9m g (1.3m r) | 56g (40r) | 56g (40r) | 56g (40r) |
| `russta` | Stable | 375g | 12 | 7.1m g (5.0m r) | 3.5m g (2.5m r) | 1.4m g (1.0m r) | 42g (30r) | 35g (25r) |
| `russto` | Storehouse | 31g | 12 | 35g (25r) | 18g (13r) | 7g (5r) | 4g (3r) | 3g (2r) |
| `russwa` | Wall | 200g | 4 | 3.8m g (2.7m r) | 1.9m g (1.3m r) | 56g (40r) | 56g (40r) | 56g (40r) |
| `rustem` | Orthodox Cathedral | 156g | 12 | 2.9m g (2.1m r) | 1.5m g (1.1m r) | 35g (25r) | 18g (13r) | 15g (11r) |
| `rustow` | Tower | 1477g | 8 | 27.8m g (19.9m r) | 13.9m g (9.9m r) | 5.6m g (4.0m r) | 3.5m g (2.5m r) | 3.5m g (2.5m r) |

### Полный ремонт (0 → max HP)

| sid | имя | maxhp | slot_cap | 1 builders | 2 builders | 5 builders | 10 builders | max builders |
|---|---|---|---|---|---|---|---|---|
| `eurcoa` | Mine | 2500 | 12 | 51g (36r) | 25g (18r) | 10g (7r) | 5g (4r) | 4g (3r) |
| `eurgol` | Mine | 2500 | 12 | 51g (36r) | 25g (18r) | 10g (7r) | 5g (4r) | 4g (3r) |
| `euriro` | Mine | 2500 | 12 | 51g (36r) | 25g (18r) | 10g (7r) | 5g (4r) | 4g (3r) |
| `rusaca` | Academy | 65000 | 16 | 22.0m g (15.7m r) | 11.0m g (7.9m r) | 4.4m g (3.1m r) | 2.2m g (1.6m r) | 1.4m g (1.0m r) |
| `rusart` | Artillery Depot | 40000 | 12 | 13.5m g (9.7m r) | 6.8m g (4.8m r) | 2.7m g (1.9m r) | 1.4m g (1.0m r) | 1.1m g (0.8m r) |
| `rusba2` | Barracks, 18th century | 55000 | 16 | 18.6m g (13.3m r) | 9.3m g (6.6m r) | 3.7m g (2.7m r) | 1.9m g (1.3m r) | 1.2m g (0.8m r) |
| `rusbar` | Strelets Barracks | 25000 | 12 | 8.5m g (6.0m r) | 4.2m g (3.0m r) | 1.7m g (1.2m r) | 51g (36r) | 42g (30r) |
| `rusbla` | Blacksmith | 5500 | 12 | 1.9m g (1.3m r) | 56g (40r) | 22g (16r) | 11g (8r) | 9g (7r) |
| `ruscen` | Town Hall | 4050 | 16 | 1.4m g (1.0m r) | 41g (29r) | 16g (12r) | 8g (6r) | 5g (4r) |
| `rusdip` | Diplomatic Center | 6500 | 12 | 2.2m g (1.6m r) | 1.1m g (0.8m r) | 26g (19r) | 13g (9r) | 11g (8r) |
| `rushou` | Izba | 5000 | 12 | 1.7m g (1.2m r) | 51g (36r) | 20g (15r) | 10g (7r) | 8g (6r) |
| `rusmar` | Market | 4000 | 12 | 1.4m g (1.0m r) | 41g (29r) | 16g (12r) | 8g (6r) | 7g (5r) |
| `rusmil` | Mill | 15000 | 12 | 5.1m g (3.6m r) | 2.5m g (1.8m r) | 1.0m g (0.7m r) | 30g (22r) | 25g (18r) |
| `ruspor` | Shipyard | 45000 | 16 | 15.2m g (10.9m r) | 7.6m g (5.4m r) | 3.0m g (2.2m r) | 1.5m g (1.1m r) | 57g (41r) |
| `russga` | Gate | 50000 | 4 | 16.9m g (12.1m r) | 8.5m g (6.0m r) | 4.2m g (3.0m r) | 4.2m g (3.0m r) | 4.2m g (3.0m r) |
| `russta` | Stable | 25000 | 12 | 8.5m g (6.0m r) | 4.2m g (3.0m r) | 1.7m g (1.2m r) | 51g (36r) | 42g (30r) |
| `russto` | Storehouse | 10000 | 12 | 3.4m g (2.4m r) | 1.7m g (1.2m r) | 41g (29r) | 20g (15r) | 17g (12r) |
| `russwa` | Wall | 50000 | 4 | 16.9m g (12.1m r) | 8.5m g (6.0m r) | 4.2m g (3.0m r) | 4.2m g (3.0m r) | 4.2m g (3.0m r) |
| `rustem` | Orthodox Cathedral | 4500 | 12 | 1.5m g (1.1m r) | 46g (33r) | 18g (13r) | 9g (7r) | 8g (5r) |
| `rustow` | Tower | 21000 | 8 | 7.1m g (5.1m r) | 3.6m g (2.5m r) | 1.4m g (1.0m r) | 53g (38r) | 53g (38r) |

## sax

### Постройка с нуля

| sid | имя | buildtime_g | slot_cap | 1 builders | 2 builders | 5 builders | 10 builders | max builders |
|---|---|---|---|---|---|---|---|---|
| `eurcoa` | Mine | 94g | 12 | 1.8m g (1.3m r) | 53g (38r) | 21g (15r) | 11g (8r) | 9g (6r) |
| `eurgol` | Mine | 94g | 12 | 1.8m g (1.3m r) | 53g (38r) | 21g (15r) | 11g (8r) | 9g (6r) |
| `euriro` | Mine | 94g | 12 | 1.8m g (1.3m r) | 53g (38r) | 21g (15r) | 11g (8r) | 9g (6r) |
| `eurmar` | Market | 234g | 12 | 4.4m g (3.2m r) | 2.2m g (1.6m r) | 53g (38r) | 26g (19r) | 22g (16r) |
| `eurmil` | Mill | 94g | 12 | 1.8m g (1.3m r) | 53g (38r) | 21g (15r) | 11g (8r) | 9g (6r) |
| `eurpor` | Shipyard | 1562g | 16 | 29.4m g (21.0m r) | 14.7m g (10.5m r) | 5.9m g (4.2m r) | 2.9m g (2.1m r) | 1.8m g (1.3m r) |
| `eursga` | Gate | 90g | 4 | 1.7m g (1.2m r) | 51g (36r) | 25g (18r) | 25g (18r) | 25g (18r) |
| `eursto` | Storehouse | 31g | 12 | 35g (25r) | 18g (13r) | 7g (5r) | 4g (3r) | 3g (2r) |
| `eurswa` | Wall | 90g | 4 | 1.7m g (1.2m r) | 51g (36r) | 25g (18r) | 25g (18r) | 25g (18r) |
| `eurtow` | Tower | 1230g | 8 | 23.2m g (16.6m r) | 11.6m g (8.3m r) | 4.6m g (3.3m r) | 2.9m g (2.1m r) | 2.9m g (2.1m r) |
| `saxaca` | Academy | 625g | 16 | 11.8m g (8.4m r) | 5.9m g (4.2m r) | 2.4m g (1.7m r) | 1.2m g (0.8m r) | 44g (32r) |
| `saxart` | Artillery Depot | 246g | 12 | 4.6m g (3.3m r) | 2.3m g (1.7m r) | 56g (40r) | 28g (20r) | 23g (17r) |
| `saxba2` | Barracks, 18th century | 5625g | 16 | 105.9m g (75.7m r) | 53.0m g (37.8m r) | 21.2m g (15.1m r) | 10.6m g (7.6m r) | 6.6m g (4.7m r) |
| `saxbar` | Barracks, 17th century | 94g | 12 | 1.8m g (1.3m r) | 53g (38r) | 21g (15r) | 11g (8r) | 9g (6r) |
| `saxbla` | Blacksmith | 94g | 12 | 1.8m g (1.3m r) | 53g (38r) | 21g (15r) | 11g (8r) | 9g (6r) |
| `saxcen` | Town Hall | 156g | 16 | 2.9m g (2.1m r) | 1.5m g (1.1m r) | 35g (25r) | 18g (13r) | 11g (8r) |
| `saxdip` | Diplomatic Center | 312g | 12 | 5.9m g (4.2m r) | 2.9m g (2.1m r) | 1.2m g (0.8m r) | 35g (25r) | 29g (21r) |
| `saxhou` | Housing | 31g | 12 | 35g (25r) | 18g (13r) | 7g (5r) | 4g (3r) | 3g (2r) |
| `saxsta` | Stable | 625g | 12 | 11.8m g (8.4m r) | 5.9m g (4.2m r) | 2.4m g (1.7m r) | 1.2m g (0.8m r) | 59g (42r) |
| `saxtem` | Cathedral | 156g | 12 | 2.9m g (2.1m r) | 1.5m g (1.1m r) | 35g (25r) | 18g (13r) | 15g (11r) |

### Полный ремонт (0 → max HP)

| sid | имя | maxhp | slot_cap | 1 builders | 2 builders | 5 builders | 10 builders | max builders |
|---|---|---|---|---|---|---|---|---|
| `eurcoa` | Mine | 2500 | 12 | 51g (36r) | 25g (18r) | 10g (7r) | 5g (4r) | 4g (3r) |
| `eurgol` | Mine | 2500 | 12 | 51g (36r) | 25g (18r) | 10g (7r) | 5g (4r) | 4g (3r) |
| `euriro` | Mine | 2500 | 12 | 51g (36r) | 25g (18r) | 10g (7r) | 5g (4r) | 4g (3r) |
| `eurmar` | Market | 4000 | 12 | 1.4m g (1.0m r) | 41g (29r) | 16g (12r) | 8g (6r) | 7g (5r) |
| `eurmil` | Mill | 20000 | 12 | 6.8m g (4.8m r) | 3.4m g (2.4m r) | 1.4m g (1.0m r) | 41g (29r) | 34g (24r) |
| `eurpor` | Shipyard | 50000 | 16 | 16.9m g (12.1m r) | 8.5m g (6.0m r) | 3.4m g (2.4m r) | 1.7m g (1.2m r) | 1.1m g (0.8m r) |
| `eursga` | Gate | 50000 | 4 | 16.9m g (12.1m r) | 8.5m g (6.0m r) | 4.2m g (3.0m r) | 4.2m g (3.0m r) | 4.2m g (3.0m r) |
| `eursto` | Storehouse | 10000 | 12 | 3.4m g (2.4m r) | 1.7m g (1.2m r) | 41g (29r) | 20g (15r) | 17g (12r) |
| `eurswa` | Wall | 50000 | 4 | 16.9m g (12.1m r) | 8.5m g (6.0m r) | 4.2m g (3.0m r) | 4.2m g (3.0m r) | 4.2m g (3.0m r) |
| `eurtow` | Tower | 20000 | 8 | 6.8m g (4.8m r) | 3.4m g (2.4m r) | 1.4m g (1.0m r) | 51g (36r) | 51g (36r) |
| `saxaca` | Academy | 63000 | 16 | 21.3m g (15.2m r) | 10.7m g (7.6m r) | 4.3m g (3.0m r) | 2.1m g (1.5m r) | 1.3m g (1.0m r) |
| `saxart` | Artillery Depot | 40000 | 12 | 13.5m g (9.7m r) | 6.8m g (4.8m r) | 2.7m g (1.9m r) | 1.4m g (1.0m r) | 1.1m g (0.8m r) |
| `saxba2` | Barracks, 18th century | 55000 | 16 | 18.6m g (13.3m r) | 9.3m g (6.6m r) | 3.7m g (2.7m r) | 1.9m g (1.3m r) | 1.2m g (0.8m r) |
| `saxbar` | Barracks, 17th century | 40000 | 12 | 13.5m g (9.7m r) | 6.8m g (4.8m r) | 2.7m g (1.9m r) | 1.4m g (1.0m r) | 1.1m g (0.8m r) |
| `saxbla` | Blacksmith | 5500 | 12 | 1.9m g (1.3m r) | 56g (40r) | 22g (16r) | 11g (8r) | 9g (7r) |
| `saxcen` | Town Hall | 4000 | 16 | 1.4m g (1.0m r) | 41g (29r) | 16g (12r) | 8g (6r) | 5g (4r) |
| `saxdip` | Diplomatic Center | 4500 | 12 | 1.5m g (1.1m r) | 46g (33r) | 18g (13r) | 9g (7r) | 8g (5r) |
| `saxhou` | Housing | 4000 | 12 | 1.4m g (1.0m r) | 41g (29r) | 16g (12r) | 8g (6r) | 7g (5r) |
| `saxsta` | Stable | 20000 | 12 | 6.8m g (4.8m r) | 3.4m g (2.4m r) | 1.4m g (1.0m r) | 41g (29r) | 34g (24r) |
| `saxtem` | Cathedral | 4200 | 12 | 1.4m g (1.0m r) | 43g (30r) | 17g (12r) | 9g (6r) | 7g (5r) |

## sco

### Постройка с нуля

| sid | имя | buildtime_g | slot_cap | 1 builders | 2 builders | 5 builders | 10 builders | max builders |
|---|---|---|---|---|---|---|---|---|
| `eurcoa` | Mine | 94g | 12 | 1.8m g (1.3m r) | 53g (38r) | 21g (15r) | 11g (8r) | 9g (6r) |
| `eurgol` | Mine | 94g | 12 | 1.8m g (1.3m r) | 53g (38r) | 21g (15r) | 11g (8r) | 9g (6r) |
| `euriro` | Mine | 94g | 12 | 1.8m g (1.3m r) | 53g (38r) | 21g (15r) | 11g (8r) | 9g (6r) |
| `eurmar` | Market | 234g | 12 | 4.4m g (3.2m r) | 2.2m g (1.6m r) | 53g (38r) | 26g (19r) | 22g (16r) |
| `eurmil` | Mill | 94g | 12 | 1.8m g (1.3m r) | 53g (38r) | 21g (15r) | 11g (8r) | 9g (6r) |
| `eurpor` | Shipyard | 1562g | 16 | 29.4m g (21.0m r) | 14.7m g (10.5m r) | 5.9m g (4.2m r) | 2.9m g (2.1m r) | 1.8m g (1.3m r) |
| `eursga` | Gate | 90g | 4 | 1.7m g (1.2m r) | 51g (36r) | 25g (18r) | 25g (18r) | 25g (18r) |
| `eursto` | Storehouse | 31g | 12 | 35g (25r) | 18g (13r) | 7g (5r) | 4g (3r) | 3g (2r) |
| `eurswa` | Wall | 90g | 4 | 1.7m g (1.2m r) | 51g (36r) | 25g (18r) | 25g (18r) | 25g (18r) |
| `eurtow` | Tower | 1230g | 8 | 23.2m g (16.6m r) | 11.6m g (8.3m r) | 4.6m g (3.3m r) | 2.9m g (2.1m r) | 2.9m g (2.1m r) |
| `scoaca` | Academy | 625g | 16 | 11.8m g (8.4m r) | 5.9m g (4.2m r) | 2.4m g (1.7m r) | 1.2m g (0.8m r) | 44g (32r) |
| `scoart` | Artillery Depot | 246g | 12 | 4.6m g (3.3m r) | 2.3m g (1.7m r) | 56g (40r) | 28g (20r) | 23g (17r) |
| `scoba2` | Castle | 625g | 16 | 11.8m g (8.4m r) | 5.9m g (4.2m r) | 2.4m g (1.7m r) | 1.2m g (0.8m r) | 44g (32r) |
| `scobar` | Barracks, 17th century | 94g | 12 | 1.8m g (1.3m r) | 53g (38r) | 21g (15r) | 11g (8r) | 9g (6r) |
| `scobla` | Blacksmith | 94g | 12 | 1.8m g (1.3m r) | 53g (38r) | 21g (15r) | 11g (8r) | 9g (6r) |
| `scocen` | Town Hall | 156g | 16 | 2.9m g (2.1m r) | 1.5m g (1.1m r) | 35g (25r) | 18g (13r) | 11g (8r) |
| `scodip` | Diplomatic Center | 312g | 12 | 5.9m g (4.2m r) | 2.9m g (2.1m r) | 1.2m g (0.8m r) | 35g (25r) | 29g (21r) |
| `scohou` | Housing | 31g | 12 | 35g (25r) | 18g (13r) | 7g (5r) | 4g (3r) | 3g (2r) |
| `scosta` | Stable | 375g | 12 | 7.1m g (5.0m r) | 3.5m g (2.5m r) | 1.4m g (1.0m r) | 42g (30r) | 35g (25r) |
| `scotem` | Cathedral | 156g | 12 | 2.9m g (2.1m r) | 1.5m g (1.1m r) | 35g (25r) | 18g (13r) | 15g (11r) |

### Полный ремонт (0 → max HP)

| sid | имя | maxhp | slot_cap | 1 builders | 2 builders | 5 builders | 10 builders | max builders |
|---|---|---|---|---|---|---|---|---|
| `eurcoa` | Mine | 2500 | 12 | 51g (36r) | 25g (18r) | 10g (7r) | 5g (4r) | 4g (3r) |
| `eurgol` | Mine | 2500 | 12 | 51g (36r) | 25g (18r) | 10g (7r) | 5g (4r) | 4g (3r) |
| `euriro` | Mine | 2500 | 12 | 51g (36r) | 25g (18r) | 10g (7r) | 5g (4r) | 4g (3r) |
| `eurmar` | Market | 4000 | 12 | 1.4m g (1.0m r) | 41g (29r) | 16g (12r) | 8g (6r) | 7g (5r) |
| `eurmil` | Mill | 20000 | 12 | 6.8m g (4.8m r) | 3.4m g (2.4m r) | 1.4m g (1.0m r) | 41g (29r) | 34g (24r) |
| `eurpor` | Shipyard | 50000 | 16 | 16.9m g (12.1m r) | 8.5m g (6.0m r) | 3.4m g (2.4m r) | 1.7m g (1.2m r) | 1.1m g (0.8m r) |
| `eursga` | Gate | 50000 | 4 | 16.9m g (12.1m r) | 8.5m g (6.0m r) | 4.2m g (3.0m r) | 4.2m g (3.0m r) | 4.2m g (3.0m r) |
| `eursto` | Storehouse | 10000 | 12 | 3.4m g (2.4m r) | 1.7m g (1.2m r) | 41g (29r) | 20g (15r) | 17g (12r) |
| `eurswa` | Wall | 50000 | 4 | 16.9m g (12.1m r) | 8.5m g (6.0m r) | 4.2m g (3.0m r) | 4.2m g (3.0m r) | 4.2m g (3.0m r) |
| `eurtow` | Tower | 20000 | 8 | 6.8m g (4.8m r) | 3.4m g (2.4m r) | 1.4m g (1.0m r) | 51g (36r) | 51g (36r) |
| `scoaca` | Academy | 63000 | 16 | 21.3m g (15.2m r) | 10.7m g (7.6m r) | 4.3m g (3.0m r) | 2.1m g (1.5m r) | 1.3m g (1.0m r) |
| `scoart` | Artillery Depot | 40000 | 12 | 13.5m g (9.7m r) | 6.8m g (4.8m r) | 2.7m g (1.9m r) | 1.4m g (1.0m r) | 1.1m g (0.8m r) |
| `scoba2` | Castle | 40000 | 16 | 13.5m g (9.7m r) | 6.8m g (4.8m r) | 2.7m g (1.9m r) | 1.4m g (1.0m r) | 51g (36r) |
| `scobar` | Barracks, 17th century | 30000 | 12 | 10.2m g (7.3m r) | 5.1m g (3.6m r) | 2.0m g (1.5m r) | 1.0m g (0.7m r) | 51g (36r) |
| `scobla` | Blacksmith | 5500 | 12 | 1.9m g (1.3m r) | 56g (40r) | 22g (16r) | 11g (8r) | 9g (7r) |
| `scocen` | Town Hall | 4000 | 16 | 1.4m g (1.0m r) | 41g (29r) | 16g (12r) | 8g (6r) | 5g (4r) |
| `scodip` | Diplomatic Center | 4500 | 12 | 1.5m g (1.1m r) | 46g (33r) | 18g (13r) | 9g (7r) | 8g (5r) |
| `scohou` | Housing | 4000 | 12 | 1.4m g (1.0m r) | 41g (29r) | 16g (12r) | 8g (6r) | 7g (5r) |
| `scosta` | Stable | 25000 | 12 | 8.5m g (6.0m r) | 4.2m g (3.0m r) | 1.7m g (1.2m r) | 51g (36r) | 42g (30r) |
| `scotem` | Cathedral | 4200 | 12 | 1.4m g (1.0m r) | 43g (30r) | 17g (12r) | 9g (6r) | 7g (5r) |

## spa

### Постройка с нуля

| sid | имя | buildtime_g | slot_cap | 1 builders | 2 builders | 5 builders | 10 builders | max builders |
|---|---|---|---|---|---|---|---|---|
| `eurcoa` | Mine | 94g | 12 | 1.8m g (1.3m r) | 53g (38r) | 21g (15r) | 11g (8r) | 9g (6r) |
| `eurgol` | Mine | 94g | 12 | 1.8m g (1.3m r) | 53g (38r) | 21g (15r) | 11g (8r) | 9g (6r) |
| `euriro` | Mine | 94g | 12 | 1.8m g (1.3m r) | 53g (38r) | 21g (15r) | 11g (8r) | 9g (6r) |
| `eurmil` | Mill | 94g | 12 | 1.8m g (1.3m r) | 53g (38r) | 21g (15r) | 11g (8r) | 9g (6r) |
| `eurpor` | Shipyard | 1562g | 16 | 29.4m g (21.0m r) | 14.7m g (10.5m r) | 5.9m g (4.2m r) | 2.9m g (2.1m r) | 1.8m g (1.3m r) |
| `eursga` | Gate | 90g | 4 | 1.7m g (1.2m r) | 51g (36r) | 25g (18r) | 25g (18r) | 25g (18r) |
| `eurswa` | Wall | 90g | 4 | 1.7m g (1.2m r) | 51g (36r) | 25g (18r) | 25g (18r) | 25g (18r) |
| `eurtow` | Tower | 1230g | 8 | 23.2m g (16.6m r) | 11.6m g (8.3m r) | 4.6m g (3.3m r) | 2.9m g (2.1m r) | 2.9m g (2.1m r) |
| `spaaca` | Academy | 625g | 16 | 11.8m g (8.4m r) | 5.9m g (4.2m r) | 2.4m g (1.7m r) | 1.2m g (0.8m r) | 44g (32r) |
| `spaart` | Artillery Depot | 246g | 12 | 4.6m g (3.3m r) | 2.3m g (1.7m r) | 56g (40r) | 28g (20r) | 23g (17r) |
| `spaba2` | Barracks, 18th century | 5625g | 16 | 105.9m g (75.7m r) | 53.0m g (37.8m r) | 21.2m g (15.1m r) | 10.6m g (7.6m r) | 6.6m g (4.7m r) |
| `spabar` | Barracks, 17th century | 94g | 12 | 1.8m g (1.3m r) | 53g (38r) | 21g (15r) | 11g (8r) | 9g (6r) |
| `spabla` | Blacksmith | 94g | 12 | 1.8m g (1.3m r) | 53g (38r) | 21g (15r) | 11g (8r) | 9g (6r) |
| `spacen` | Town Hall | 156g | 16 | 2.9m g (2.1m r) | 1.5m g (1.1m r) | 35g (25r) | 18g (13r) | 11g (8r) |
| `spadip` | Diplomatic Center | 312g | 12 | 5.9m g (4.2m r) | 2.9m g (2.1m r) | 1.2m g (0.8m r) | 35g (25r) | 29g (21r) |
| `spahou` | Housing | 31g | 12 | 35g (25r) | 18g (13r) | 7g (5r) | 4g (3r) | 3g (2r) |
| `spamar` | Market | 156g | 12 | 2.9m g (2.1m r) | 1.5m g (1.1m r) | 35g (25r) | 18g (13r) | 15g (11r) |
| `spasta` | Stable | 625g | 12 | 11.8m g (8.4m r) | 5.9m g (4.2m r) | 2.4m g (1.7m r) | 1.2m g (0.8m r) | 59g (42r) |
| `spasto` | Storehouse | 31g | 12 | 35g (25r) | 18g (13r) | 7g (5r) | 4g (3r) | 3g (2r) |
| `spatem` | Cathedral | 156g | 12 | 2.9m g (2.1m r) | 1.5m g (1.1m r) | 35g (25r) | 18g (13r) | 15g (11r) |

### Полный ремонт (0 → max HP)

| sid | имя | maxhp | slot_cap | 1 builders | 2 builders | 5 builders | 10 builders | max builders |
|---|---|---|---|---|---|---|---|---|
| `eurcoa` | Mine | 2500 | 12 | 51g (36r) | 25g (18r) | 10g (7r) | 5g (4r) | 4g (3r) |
| `eurgol` | Mine | 2500 | 12 | 51g (36r) | 25g (18r) | 10g (7r) | 5g (4r) | 4g (3r) |
| `euriro` | Mine | 2500 | 12 | 51g (36r) | 25g (18r) | 10g (7r) | 5g (4r) | 4g (3r) |
| `eurmil` | Mill | 20000 | 12 | 6.8m g (4.8m r) | 3.4m g (2.4m r) | 1.4m g (1.0m r) | 41g (29r) | 34g (24r) |
| `eurpor` | Shipyard | 50000 | 16 | 16.9m g (12.1m r) | 8.5m g (6.0m r) | 3.4m g (2.4m r) | 1.7m g (1.2m r) | 1.1m g (0.8m r) |
| `eursga` | Gate | 50000 | 4 | 16.9m g (12.1m r) | 8.5m g (6.0m r) | 4.2m g (3.0m r) | 4.2m g (3.0m r) | 4.2m g (3.0m r) |
| `eurswa` | Wall | 50000 | 4 | 16.9m g (12.1m r) | 8.5m g (6.0m r) | 4.2m g (3.0m r) | 4.2m g (3.0m r) | 4.2m g (3.0m r) |
| `eurtow` | Tower | 20000 | 8 | 6.8m g (4.8m r) | 3.4m g (2.4m r) | 1.4m g (1.0m r) | 51g (36r) | 51g (36r) |
| `spaaca` | Academy | 63000 | 16 | 21.3m g (15.2m r) | 10.7m g (7.6m r) | 4.3m g (3.0m r) | 2.1m g (1.5m r) | 1.3m g (1.0m r) |
| `spaart` | Artillery Depot | 40000 | 12 | 13.5m g (9.7m r) | 6.8m g (4.8m r) | 2.7m g (1.9m r) | 1.4m g (1.0m r) | 1.1m g (0.8m r) |
| `spaba2` | Barracks, 18th century | 55000 | 16 | 18.6m g (13.3m r) | 9.3m g (6.6m r) | 3.7m g (2.7m r) | 1.9m g (1.3m r) | 1.2m g (0.8m r) |
| `spabar` | Barracks, 17th century | 40000 | 12 | 13.5m g (9.7m r) | 6.8m g (4.8m r) | 2.7m g (1.9m r) | 1.4m g (1.0m r) | 1.1m g (0.8m r) |
| `spabla` | Blacksmith | 5500 | 12 | 1.9m g (1.3m r) | 56g (40r) | 22g (16r) | 11g (8r) | 9g (7r) |
| `spacen` | Town Hall | 4250 | 16 | 1.4m g (1.0m r) | 43g (31r) | 17g (12r) | 9g (6r) | 5g (4r) |
| `spadip` | Diplomatic Center | 4500 | 12 | 1.5m g (1.1m r) | 46g (33r) | 18g (13r) | 9g (7r) | 8g (5r) |
| `spahou` | Housing | 4200 | 12 | 1.4m g (1.0m r) | 43g (30r) | 17g (12r) | 9g (6r) | 7g (5r) |
| `spamar` | Market | 4000 | 12 | 1.4m g (1.0m r) | 41g (29r) | 16g (12r) | 8g (6r) | 7g (5r) |
| `spasta` | Stable | 20000 | 12 | 6.8m g (4.8m r) | 3.4m g (2.4m r) | 1.4m g (1.0m r) | 41g (29r) | 34g (24r) |
| `spasto` | Storehouse | 10000 | 12 | 3.4m g (2.4m r) | 1.7m g (1.2m r) | 41g (29r) | 20g (15r) | 17g (12r) |
| `spatem` | Cathedral | 4200 | 12 | 1.4m g (1.0m r) | 43g (30r) | 17g (12r) | 9g (6r) | 7g (5r) |

## swe

### Постройка с нуля

| sid | имя | buildtime_g | slot_cap | 1 builders | 2 builders | 5 builders | 10 builders | max builders |
|---|---|---|---|---|---|---|---|---|
| `eurcoa` | Mine | 94g | 12 | 1.8m g (1.3m r) | 53g (38r) | 21g (15r) | 11g (8r) | 9g (6r) |
| `eurgol` | Mine | 94g | 12 | 1.8m g (1.3m r) | 53g (38r) | 21g (15r) | 11g (8r) | 9g (6r) |
| `euriro` | Mine | 94g | 12 | 1.8m g (1.3m r) | 53g (38r) | 21g (15r) | 11g (8r) | 9g (6r) |
| `eurmar` | Market | 234g | 12 | 4.4m g (3.2m r) | 2.2m g (1.6m r) | 53g (38r) | 26g (19r) | 22g (16r) |
| `eurmil` | Mill | 94g | 12 | 1.8m g (1.3m r) | 53g (38r) | 21g (15r) | 11g (8r) | 9g (6r) |
| `eurpor` | Shipyard | 1562g | 16 | 29.4m g (21.0m r) | 14.7m g (10.5m r) | 5.9m g (4.2m r) | 2.9m g (2.1m r) | 1.8m g (1.3m r) |
| `eursga` | Gate | 90g | 4 | 1.7m g (1.2m r) | 51g (36r) | 25g (18r) | 25g (18r) | 25g (18r) |
| `eursto` | Storehouse | 31g | 12 | 35g (25r) | 18g (13r) | 7g (5r) | 4g (3r) | 3g (2r) |
| `eurswa` | Wall | 90g | 4 | 1.7m g (1.2m r) | 51g (36r) | 25g (18r) | 25g (18r) | 25g (18r) |
| `eurtow` | Tower | 1230g | 8 | 23.2m g (16.6m r) | 11.6m g (8.3m r) | 4.6m g (3.3m r) | 2.9m g (2.1m r) | 2.9m g (2.1m r) |
| `sweaca` | Academy | 625g | 16 | 11.8m g (8.4m r) | 5.9m g (4.2m r) | 2.4m g (1.7m r) | 1.2m g (0.8m r) | 44g (32r) |
| `sweart` | Artillery Depot | 246g | 12 | 4.6m g (3.3m r) | 2.3m g (1.7m r) | 56g (40r) | 28g (20r) | 23g (17r) |
| `sweba2` | Barracks, 18th century | 5625g | 16 | 105.9m g (75.7m r) | 53.0m g (37.8m r) | 21.2m g (15.1m r) | 10.6m g (7.6m r) | 6.6m g (4.7m r) |
| `swebar` | Barracks, 17th century | 94g | 12 | 1.8m g (1.3m r) | 53g (38r) | 21g (15r) | 11g (8r) | 9g (6r) |
| `swebla` | Blacksmith | 94g | 12 | 1.8m g (1.3m r) | 53g (38r) | 21g (15r) | 11g (8r) | 9g (6r) |
| `swecen` | Town Hall | 156g | 16 | 2.9m g (2.1m r) | 1.5m g (1.1m r) | 35g (25r) | 18g (13r) | 11g (8r) |
| `swedip` | Diplomatic Center | 312g | 12 | 5.9m g (4.2m r) | 2.9m g (2.1m r) | 1.2m g (0.8m r) | 35g (25r) | 29g (21r) |
| `swehou` | Housing | 31g | 12 | 35g (25r) | 18g (13r) | 7g (5r) | 4g (3r) | 3g (2r) |
| `swesta` | Stable | 625g | 12 | 11.8m g (8.4m r) | 5.9m g (4.2m r) | 2.4m g (1.7m r) | 1.2m g (0.8m r) | 59g (42r) |
| `swetem` | Cathedral | 156g | 12 | 2.9m g (2.1m r) | 1.5m g (1.1m r) | 35g (25r) | 18g (13r) | 15g (11r) |

### Полный ремонт (0 → max HP)

| sid | имя | maxhp | slot_cap | 1 builders | 2 builders | 5 builders | 10 builders | max builders |
|---|---|---|---|---|---|---|---|---|
| `eurcoa` | Mine | 2500 | 12 | 51g (36r) | 25g (18r) | 10g (7r) | 5g (4r) | 4g (3r) |
| `eurgol` | Mine | 2500 | 12 | 51g (36r) | 25g (18r) | 10g (7r) | 5g (4r) | 4g (3r) |
| `euriro` | Mine | 2500 | 12 | 51g (36r) | 25g (18r) | 10g (7r) | 5g (4r) | 4g (3r) |
| `eurmar` | Market | 4000 | 12 | 1.4m g (1.0m r) | 41g (29r) | 16g (12r) | 8g (6r) | 7g (5r) |
| `eurmil` | Mill | 20000 | 12 | 6.8m g (4.8m r) | 3.4m g (2.4m r) | 1.4m g (1.0m r) | 41g (29r) | 34g (24r) |
| `eurpor` | Shipyard | 50000 | 16 | 16.9m g (12.1m r) | 8.5m g (6.0m r) | 3.4m g (2.4m r) | 1.7m g (1.2m r) | 1.1m g (0.8m r) |
| `eursga` | Gate | 50000 | 4 | 16.9m g (12.1m r) | 8.5m g (6.0m r) | 4.2m g (3.0m r) | 4.2m g (3.0m r) | 4.2m g (3.0m r) |
| `eursto` | Storehouse | 10000 | 12 | 3.4m g (2.4m r) | 1.7m g (1.2m r) | 41g (29r) | 20g (15r) | 17g (12r) |
| `eurswa` | Wall | 50000 | 4 | 16.9m g (12.1m r) | 8.5m g (6.0m r) | 4.2m g (3.0m r) | 4.2m g (3.0m r) | 4.2m g (3.0m r) |
| `eurtow` | Tower | 20000 | 8 | 6.8m g (4.8m r) | 3.4m g (2.4m r) | 1.4m g (1.0m r) | 51g (36r) | 51g (36r) |
| `sweaca` | Academy | 63000 | 16 | 21.3m g (15.2m r) | 10.7m g (7.6m r) | 4.3m g (3.0m r) | 2.1m g (1.5m r) | 1.3m g (1.0m r) |
| `sweart` | Artillery Depot | 40000 | 12 | 13.5m g (9.7m r) | 6.8m g (4.8m r) | 2.7m g (1.9m r) | 1.4m g (1.0m r) | 1.1m g (0.8m r) |
| `sweba2` | Barracks, 18th century | 55000 | 16 | 18.6m g (13.3m r) | 9.3m g (6.6m r) | 3.7m g (2.7m r) | 1.9m g (1.3m r) | 1.2m g (0.8m r) |
| `swebar` | Barracks, 17th century | 40000 | 12 | 13.5m g (9.7m r) | 6.8m g (4.8m r) | 2.7m g (1.9m r) | 1.4m g (1.0m r) | 1.1m g (0.8m r) |
| `swebla` | Blacksmith | 5500 | 12 | 1.9m g (1.3m r) | 56g (40r) | 22g (16r) | 11g (8r) | 9g (7r) |
| `swecen` | Town Hall | 5000 | 16 | 1.7m g (1.2m r) | 51g (36r) | 20g (15r) | 10g (7r) | 6g (5r) |
| `swedip` | Diplomatic Center | 4500 | 12 | 1.5m g (1.1m r) | 46g (33r) | 18g (13r) | 9g (7r) | 8g (5r) |
| `swehou` | Housing | 5000 | 12 | 1.7m g (1.2m r) | 51g (36r) | 20g (15r) | 10g (7r) | 8g (6r) |
| `swesta` | Stable | 20000 | 12 | 6.8m g (4.8m r) | 3.4m g (2.4m r) | 1.4m g (1.0m r) | 41g (29r) | 34g (24r) |
| `swetem` | Cathedral | 4200 | 12 | 1.4m g (1.0m r) | 43g (30r) | 17g (12r) | 9g (6r) | 7g (5r) |

## swi

### Постройка с нуля

| sid | имя | buildtime_g | slot_cap | 1 builders | 2 builders | 5 builders | 10 builders | max builders |
|---|---|---|---|---|---|---|---|---|
| `eurcoa` | Mine | 94g | 12 | 1.8m g (1.3m r) | 53g (38r) | 21g (15r) | 11g (8r) | 9g (6r) |
| `eurgol` | Mine | 94g | 12 | 1.8m g (1.3m r) | 53g (38r) | 21g (15r) | 11g (8r) | 9g (6r) |
| `euriro` | Mine | 94g | 12 | 1.8m g (1.3m r) | 53g (38r) | 21g (15r) | 11g (8r) | 9g (6r) |
| `eurmar` | Market | 234g | 12 | 4.4m g (3.2m r) | 2.2m g (1.6m r) | 53g (38r) | 26g (19r) | 22g (16r) |
| `eurmil` | Mill | 94g | 12 | 1.8m g (1.3m r) | 53g (38r) | 21g (15r) | 11g (8r) | 9g (6r) |
| `eurpor` | Shipyard | 1562g | 16 | 29.4m g (21.0m r) | 14.7m g (10.5m r) | 5.9m g (4.2m r) | 2.9m g (2.1m r) | 1.8m g (1.3m r) |
| `eursga` | Gate | 90g | 4 | 1.7m g (1.2m r) | 51g (36r) | 25g (18r) | 25g (18r) | 25g (18r) |
| `eursto` | Storehouse | 31g | 12 | 35g (25r) | 18g (13r) | 7g (5r) | 4g (3r) | 3g (2r) |
| `eurswa` | Wall | 90g | 4 | 1.7m g (1.2m r) | 51g (36r) | 25g (18r) | 25g (18r) | 25g (18r) |
| `eurtow` | Tower | 1230g | 8 | 23.2m g (16.6m r) | 11.6m g (8.3m r) | 4.6m g (3.3m r) | 2.9m g (2.1m r) | 2.9m g (2.1m r) |
| `swiaca` | Academy | 625g | 16 | 11.8m g (8.4m r) | 5.9m g (4.2m r) | 2.4m g (1.7m r) | 1.2m g (0.8m r) | 44g (32r) |
| `swiart` | Artillery Depot | 246g | 12 | 4.6m g (3.3m r) | 2.3m g (1.7m r) | 56g (40r) | 28g (20r) | 23g (17r) |
| `swiba2` | Barracks, 18th century | 5625g | 16 | 105.9m g (75.7m r) | 53.0m g (37.8m r) | 21.2m g (15.1m r) | 10.6m g (7.6m r) | 6.6m g (4.7m r) |
| `swibar` | Barracks, 17th century | 94g | 12 | 1.8m g (1.3m r) | 53g (38r) | 21g (15r) | 11g (8r) | 9g (6r) |
| `swibla` | Blacksmith | 94g | 12 | 1.8m g (1.3m r) | 53g (38r) | 21g (15r) | 11g (8r) | 9g (6r) |
| `swicen` | Town Hall | 156g | 16 | 2.9m g (2.1m r) | 1.5m g (1.1m r) | 35g (25r) | 18g (13r) | 11g (8r) |
| `swidip` | Diplomatic Center | 312g | 12 | 5.9m g (4.2m r) | 2.9m g (2.1m r) | 1.2m g (0.8m r) | 35g (25r) | 29g (21r) |
| `swihou` | Housing | 31g | 12 | 35g (25r) | 18g (13r) | 7g (5r) | 4g (3r) | 3g (2r) |
| `swista` | Stable | 625g | 12 | 11.8m g (8.4m r) | 5.9m g (4.2m r) | 2.4m g (1.7m r) | 1.2m g (0.8m r) | 59g (42r) |
| `switem` | Cathedral | 156g | 12 | 2.9m g (2.1m r) | 1.5m g (1.1m r) | 35g (25r) | 18g (13r) | 15g (11r) |

### Полный ремонт (0 → max HP)

| sid | имя | maxhp | slot_cap | 1 builders | 2 builders | 5 builders | 10 builders | max builders |
|---|---|---|---|---|---|---|---|---|
| `eurcoa` | Mine | 2500 | 12 | 51g (36r) | 25g (18r) | 10g (7r) | 5g (4r) | 4g (3r) |
| `eurgol` | Mine | 2500 | 12 | 51g (36r) | 25g (18r) | 10g (7r) | 5g (4r) | 4g (3r) |
| `euriro` | Mine | 2500 | 12 | 51g (36r) | 25g (18r) | 10g (7r) | 5g (4r) | 4g (3r) |
| `eurmar` | Market | 4000 | 12 | 1.4m g (1.0m r) | 41g (29r) | 16g (12r) | 8g (6r) | 7g (5r) |
| `eurmil` | Mill | 20000 | 12 | 6.8m g (4.8m r) | 3.4m g (2.4m r) | 1.4m g (1.0m r) | 41g (29r) | 34g (24r) |
| `eurpor` | Shipyard | 50000 | 16 | 16.9m g (12.1m r) | 8.5m g (6.0m r) | 3.4m g (2.4m r) | 1.7m g (1.2m r) | 1.1m g (0.8m r) |
| `eursga` | Gate | 50000 | 4 | 16.9m g (12.1m r) | 8.5m g (6.0m r) | 4.2m g (3.0m r) | 4.2m g (3.0m r) | 4.2m g (3.0m r) |
| `eursto` | Storehouse | 10000 | 12 | 3.4m g (2.4m r) | 1.7m g (1.2m r) | 41g (29r) | 20g (15r) | 17g (12r) |
| `eurswa` | Wall | 50000 | 4 | 16.9m g (12.1m r) | 8.5m g (6.0m r) | 4.2m g (3.0m r) | 4.2m g (3.0m r) | 4.2m g (3.0m r) |
| `eurtow` | Tower | 20000 | 8 | 6.8m g (4.8m r) | 3.4m g (2.4m r) | 1.4m g (1.0m r) | 51g (36r) | 51g (36r) |
| `swiaca` | Academy | 63000 | 16 | 21.3m g (15.2m r) | 10.7m g (7.6m r) | 4.3m g (3.0m r) | 2.1m g (1.5m r) | 1.3m g (1.0m r) |
| `swiart` | Artillery Depot | 40000 | 12 | 13.5m g (9.7m r) | 6.8m g (4.8m r) | 2.7m g (1.9m r) | 1.4m g (1.0m r) | 1.1m g (0.8m r) |
| `swiba2` | Barracks, 18th century | 55000 | 16 | 18.6m g (13.3m r) | 9.3m g (6.6m r) | 3.7m g (2.7m r) | 1.9m g (1.3m r) | 1.2m g (0.8m r) |
| `swibar` | Barracks, 17th century | 40000 | 12 | 13.5m g (9.7m r) | 6.8m g (4.8m r) | 2.7m g (1.9m r) | 1.4m g (1.0m r) | 1.1m g (0.8m r) |
| `swibla` | Blacksmith | 5500 | 12 | 1.9m g (1.3m r) | 56g (40r) | 22g (16r) | 11g (8r) | 9g (7r) |
| `swicen` | Town Hall | 4000 | 16 | 1.4m g (1.0m r) | 41g (29r) | 16g (12r) | 8g (6r) | 5g (4r) |
| `swidip` | Diplomatic Center | 4500 | 12 | 1.5m g (1.1m r) | 46g (33r) | 18g (13r) | 9g (7r) | 8g (5r) |
| `swihou` | Housing | 4000 | 12 | 1.4m g (1.0m r) | 41g (29r) | 16g (12r) | 8g (6r) | 7g (5r) |
| `swista` | Stable | 20000 | 12 | 6.8m g (4.8m r) | 3.4m g (2.4m r) | 1.4m g (1.0m r) | 41g (29r) | 34g (24r) |
| `switem` | Cathedral | 4200 | 12 | 1.4m g (1.0m r) | 43g (30r) | 17g (12r) | 9g (6r) | 7g (5r) |

## tur

### Постройка с нуля

| sid | имя | buildtime_g | slot_cap | 1 builders | 2 builders | 5 builders | 10 builders | max builders |
|---|---|---|---|---|---|---|---|---|
| `eurcoa` | Mine | 94g | 12 | 1.8m g (1.3m r) | 53g (38r) | 21g (15r) | 11g (8r) | 9g (6r) |
| `eurgol` | Mine | 94g | 12 | 1.8m g (1.3m r) | 53g (38r) | 21g (15r) | 11g (8r) | 9g (6r) |
| `euriro` | Mine | 94g | 12 | 1.8m g (1.3m r) | 53g (38r) | 21g (15r) | 11g (8r) | 9g (6r) |
| `turaca` | Minaret | 156g | 16 | 2.9m g (2.1m r) | 1.5m g (1.1m r) | 35g (25r) | 18g (13r) | 11g (8r) |
| `turart` | Artillery Depot | 246g | 12 | 4.6m g (3.3m r) | 2.3m g (1.7m r) | 56g (40r) | 28g (20r) | 23g (17r) |
| `turbar` | Barracks | 94g | 12 | 1.8m g (1.3m r) | 53g (38r) | 21g (15r) | 11g (8r) | 9g (6r) |
| `turbla` | Blacksmith | 109g | 12 | 2.1m g (1.5m r) | 1.0m g (0.7m r) | 25g (18r) | 12g (9r) | 10g (7r) |
| `turcen` | Town Hall | 156g | 16 | 2.9m g (2.1m r) | 1.5m g (1.1m r) | 35g (25r) | 18g (13r) | 11g (8r) |
| `turdip` | Diplomatic Center | 312g | 12 | 5.9m g (4.2m r) | 2.9m g (2.1m r) | 1.2m g (0.8m r) | 35g (25r) | 29g (21r) |
| `turhou` | Housing | 31g | 12 | 35g (25r) | 18g (13r) | 7g (5r) | 4g (3r) | 3g (2r) |
| `turmar` | Bazaar | 234g | 12 | 4.4m g (3.2m r) | 2.2m g (1.6m r) | 53g (38r) | 26g (19r) | 22g (16r) |
| `turmil` | Mill | 94g | 12 | 1.8m g (1.3m r) | 53g (38r) | 21g (15r) | 11g (8r) | 9g (6r) |
| `turpor` | Shipyard | 1562g | 16 | 29.4m g (21.0m r) | 14.7m g (10.5m r) | 5.9m g (4.2m r) | 2.9m g (2.1m r) | 1.8m g (1.3m r) |
| `tursga` | Gate | 120g | 4 | 2.3m g (1.6m r) | 1.1m g (0.8m r) | 34g (24r) | 34g (24r) | 34g (24r) |
| `tursta` | Stable | 156g | 12 | 2.9m g (2.1m r) | 1.5m g (1.1m r) | 35g (25r) | 18g (13r) | 15g (11r) |
| `tursto` | Storehouse | 31g | 12 | 35g (25r) | 18g (13r) | 7g (5r) | 4g (3r) | 3g (2r) |
| `turswa` | Wall | 120g | 4 | 2.3m g (1.6m r) | 1.1m g (0.8m r) | 34g (24r) | 34g (24r) | 34g (24r) |
| `turtem` | Mosque | 94g | 12 | 1.8m g (1.3m r) | 53g (38r) | 21g (15r) | 11g (8r) | 9g (6r) |
| `turtow` | Tower | 984g | 8 | 18.5m g (13.2m r) | 9.3m g (6.6m r) | 3.7m g (2.6m r) | 2.3m g (1.7m r) | 2.3m g (1.7m r) |

### Полный ремонт (0 → max HP)

| sid | имя | maxhp | slot_cap | 1 builders | 2 builders | 5 builders | 10 builders | max builders |
|---|---|---|---|---|---|---|---|---|
| `eurcoa` | Mine | 2500 | 12 | 51g (36r) | 25g (18r) | 10g (7r) | 5g (4r) | 4g (3r) |
| `eurgol` | Mine | 2500 | 12 | 51g (36r) | 25g (18r) | 10g (7r) | 5g (4r) | 4g (3r) |
| `euriro` | Mine | 2500 | 12 | 51g (36r) | 25g (18r) | 10g (7r) | 5g (4r) | 4g (3r) |
| `turaca` | Minaret | 65000 | 16 | 22.0m g (15.7m r) | 11.0m g (7.9m r) | 4.4m g (3.1m r) | 2.2m g (1.6m r) | 1.4m g (1.0m r) |
| `turart` | Artillery Depot | 40000 | 12 | 13.5m g (9.7m r) | 6.8m g (4.8m r) | 2.7m g (1.9m r) | 1.4m g (1.0m r) | 1.1m g (0.8m r) |
| `turbar` | Barracks | 35000 | 12 | 11.8m g (8.5m r) | 5.9m g (4.2m r) | 2.4m g (1.7m r) | 1.2m g (0.8m r) | 59g (42r) |
| `turbla` | Blacksmith | 6500 | 12 | 2.2m g (1.6m r) | 1.1m g (0.8m r) | 26g (19r) | 13g (9r) | 11g (8r) |
| `turcen` | Town Hall | 4000 | 16 | 1.4m g (1.0m r) | 41g (29r) | 16g (12r) | 8g (6r) | 5g (4r) |
| `turdip` | Diplomatic Center | 5500 | 12 | 1.9m g (1.3m r) | 56g (40r) | 22g (16r) | 11g (8r) | 9g (7r) |
| `turhou` | Housing | 4000 | 12 | 1.4m g (1.0m r) | 41g (29r) | 16g (12r) | 8g (6r) | 7g (5r) |
| `turmar` | Bazaar | 4500 | 12 | 1.5m g (1.1m r) | 46g (33r) | 18g (13r) | 9g (7r) | 8g (5r) |
| `turmil` | Mill | 20000 | 12 | 6.8m g (4.8m r) | 3.4m g (2.4m r) | 1.4m g (1.0m r) | 41g (29r) | 34g (24r) |
| `turpor` | Shipyard | 40000 | 16 | 13.5m g (9.7m r) | 6.8m g (4.8m r) | 2.7m g (1.9m r) | 1.4m g (1.0m r) | 51g (36r) |
| `tursga` | Gate | 50000 | 4 | 16.9m g (12.1m r) | 8.5m g (6.0m r) | 4.2m g (3.0m r) | 4.2m g (3.0m r) | 4.2m g (3.0m r) |
| `tursta` | Stable | 55000 | 12 | 18.6m g (13.3m r) | 9.3m g (6.6m r) | 3.7m g (2.7m r) | 1.9m g (1.3m r) | 1.6m g (1.1m r) |
| `tursto` | Storehouse | 10000 | 12 | 3.4m g (2.4m r) | 1.7m g (1.2m r) | 41g (29r) | 20g (15r) | 17g (12r) |
| `turswa` | Wall | 50000 | 4 | 16.9m g (12.1m r) | 8.5m g (6.0m r) | 4.2m g (3.0m r) | 4.2m g (3.0m r) | 4.2m g (3.0m r) |
| `turtem` | Mosque | 5000 | 12 | 1.7m g (1.2m r) | 51g (36r) | 20g (15r) | 10g (7r) | 8g (6r) |
| `turtow` | Tower | 22500 | 8 | 7.6m g (5.4m r) | 3.8m g (2.7m r) | 1.5m g (1.1m r) | 57g (41r) | 57g (41r) |

## ukr

### Постройка с нуля

| sid | имя | buildtime_g | slot_cap | 1 builders | 2 builders | 5 builders | 10 builders | max builders |
|---|---|---|---|---|---|---|---|---|
| `eurcoa` | Mine | 94g | 12 | 1.8m g (1.3m r) | 53g (38r) | 21g (15r) | 11g (8r) | 9g (6r) |
| `eurgol` | Mine | 94g | 12 | 1.8m g (1.3m r) | 53g (38r) | 21g (15r) | 11g (8r) | 9g (6r) |
| `euriro` | Mine | 94g | 12 | 1.8m g (1.3m r) | 53g (38r) | 21g (15r) | 11g (8r) | 9g (6r) |
| `rusmar` | Market | 234g | 12 | 4.4m g (3.2m r) | 2.2m g (1.6m r) | 53g (38r) | 26g (19r) | 22g (16r) |
| `rusmil` | Mill | 94g | 12 | 1.8m g (1.3m r) | 53g (38r) | 21g (15r) | 11g (8r) | 9g (6r) |
| `russto` | Storehouse | 31g | 12 | 35g (25r) | 18g (13r) | 7g (5r) | 4g (3r) | 3g (2r) |
| `ukraca` | Academy | 47g | 16 | 53g (38r) | 26g (19r) | 11g (8r) | 5g (4r) | 3g (2r) |
| `ukrart` | Artillery Depot | 246g | 12 | 4.6m g (3.3m r) | 2.3m g (1.7m r) | 56g (40r) | 28g (20r) | 23g (17r) |
| `ukrbar` | Cossack House | 94g | 12 | 1.8m g (1.3m r) | 53g (38r) | 21g (15r) | 11g (8r) | 9g (6r) |
| `ukrbla` | Blacksmith | 62g | 12 | 1.2m g (0.8m r) | 35g (25r) | 14g (10r) | 7g (5r) | 6g (4r) |
| `ukrcen` | Town Hall | 156g | 16 | 2.9m g (2.1m r) | 1.5m g (1.1m r) | 35g (25r) | 18g (13r) | 11g (8r) |
| `ukrdip` | Diplomatic Center | 312g | 12 | 5.9m g (4.2m r) | 2.9m g (2.1m r) | 1.2m g (0.8m r) | 35g (25r) | 29g (21r) |
| `ukrhou` | Hut | 31g | 12 | 35g (25r) | 18g (13r) | 7g (5r) | 4g (3r) | 3g (2r) |
| `ukrpor` | Shipyard | 1562g | 16 | 29.4m g (21.0m r) | 14.7m g (10.5m r) | 5.9m g (4.2m r) | 2.9m g (2.1m r) | 1.8m g (1.3m r) |
| `ukrsta` | Stable | 156g | 12 | 2.9m g (2.1m r) | 1.5m g (1.1m r) | 35g (25r) | 18g (13r) | 15g (11r) |
| `ukrtem` | Orthodox Cathedral | 156g | 12 | 2.9m g (2.1m r) | 1.5m g (1.1m r) | 35g (25r) | 18g (13r) | 15g (11r) |

### Полный ремонт (0 → max HP)

| sid | имя | maxhp | slot_cap | 1 builders | 2 builders | 5 builders | 10 builders | max builders |
|---|---|---|---|---|---|---|---|---|
| `eurcoa` | Mine | 2500 | 12 | 51g (36r) | 25g (18r) | 10g (7r) | 5g (4r) | 4g (3r) |
| `eurgol` | Mine | 2500 | 12 | 51g (36r) | 25g (18r) | 10g (7r) | 5g (4r) | 4g (3r) |
| `euriro` | Mine | 2500 | 12 | 51g (36r) | 25g (18r) | 10g (7r) | 5g (4r) | 4g (3r) |
| `rusmar` | Market | 4000 | 12 | 1.4m g (1.0m r) | 41g (29r) | 16g (12r) | 8g (6r) | 7g (5r) |
| `rusmil` | Mill | 15000 | 12 | 5.1m g (3.6m r) | 2.5m g (1.8m r) | 1.0m g (0.7m r) | 30g (22r) | 25g (18r) |
| `russto` | Storehouse | 10000 | 12 | 3.4m g (2.4m r) | 1.7m g (1.2m r) | 41g (29r) | 20g (15r) | 17g (12r) |
| `ukraca` | Academy | 65000 | 16 | 22.0m g (15.7m r) | 11.0m g (7.9m r) | 4.4m g (3.1m r) | 2.2m g (1.6m r) | 1.4m g (1.0m r) |
| `ukrart` | Artillery Depot | 40000 | 12 | 13.5m g (9.7m r) | 6.8m g (4.8m r) | 2.7m g (1.9m r) | 1.4m g (1.0m r) | 1.1m g (0.8m r) |
| `ukrbar` | Cossack House | 20000 | 12 | 6.8m g (4.8m r) | 3.4m g (2.4m r) | 1.4m g (1.0m r) | 41g (29r) | 34g (24r) |
| `ukrbla` | Blacksmith | 4500 | 12 | 1.5m g (1.1m r) | 46g (33r) | 18g (13r) | 9g (7r) | 8g (5r) |
| `ukrcen` | Town Hall | 5300 | 16 | 1.8m g (1.3m r) | 54g (38r) | 22g (15r) | 11g (8r) | 7g (5r) |
| `ukrdip` | Diplomatic Center | 5000 | 12 | 1.7m g (1.2m r) | 51g (36r) | 20g (15r) | 10g (7r) | 8g (6r) |
| `ukrhou` | Hut | 4150 | 12 | 1.4m g (1.0m r) | 42g (30r) | 17g (12r) | 8g (6r) | 7g (5r) |
| `ukrpor` | Shipyard | 45000 | 16 | 15.2m g (10.9m r) | 7.6m g (5.4m r) | 3.0m g (2.2m r) | 1.5m g (1.1m r) | 57g (41r) |
| `ukrsta` | Stable | 10000 | 12 | 3.4m g (2.4m r) | 1.7m g (1.2m r) | 41g (29r) | 20g (15r) | 17g (12r) |
| `ukrtem` | Orthodox Cathedral | 5300 | 12 | 1.8m g (1.3m r) | 54g (38r) | 22g (15r) | 11g (8r) | 9g (6r) |

## ven

### Постройка с нуля

| sid | имя | buildtime_g | slot_cap | 1 builders | 2 builders | 5 builders | 10 builders | max builders |
|---|---|---|---|---|---|---|---|---|
| `eurcoa` | Mine | 94g | 12 | 1.8m g (1.3m r) | 53g (38r) | 21g (15r) | 11g (8r) | 9g (6r) |
| `eurgol` | Mine | 94g | 12 | 1.8m g (1.3m r) | 53g (38r) | 21g (15r) | 11g (8r) | 9g (6r) |
| `euriro` | Mine | 94g | 12 | 1.8m g (1.3m r) | 53g (38r) | 21g (15r) | 11g (8r) | 9g (6r) |
| `eurmar` | Market | 234g | 12 | 4.4m g (3.2m r) | 2.2m g (1.6m r) | 53g (38r) | 26g (19r) | 22g (16r) |
| `eurmil` | Mill | 94g | 12 | 1.8m g (1.3m r) | 53g (38r) | 21g (15r) | 11g (8r) | 9g (6r) |
| `eurpor` | Shipyard | 1562g | 16 | 29.4m g (21.0m r) | 14.7m g (10.5m r) | 5.9m g (4.2m r) | 2.9m g (2.1m r) | 1.8m g (1.3m r) |
| `eursga` | Gate | 90g | 4 | 1.7m g (1.2m r) | 51g (36r) | 25g (18r) | 25g (18r) | 25g (18r) |
| `eursto` | Storehouse | 31g | 12 | 35g (25r) | 18g (13r) | 7g (5r) | 4g (3r) | 3g (2r) |
| `eurswa` | Wall | 90g | 4 | 1.7m g (1.2m r) | 51g (36r) | 25g (18r) | 25g (18r) | 25g (18r) |
| `eurtow` | Tower | 1230g | 8 | 23.2m g (16.6m r) | 11.6m g (8.3m r) | 4.6m g (3.3m r) | 2.9m g (2.1m r) | 2.9m g (2.1m r) |
| `venaca` | Academy | 625g | 16 | 11.8m g (8.4m r) | 5.9m g (4.2m r) | 2.4m g (1.7m r) | 1.2m g (0.8m r) | 44g (32r) |
| `venart` | Artillery Depot | 246g | 12 | 4.6m g (3.3m r) | 2.3m g (1.7m r) | 56g (40r) | 28g (20r) | 23g (17r) |
| `venba2` | Barracks, 18th century | 5625g | 16 | 105.9m g (75.7m r) | 53.0m g (37.8m r) | 21.2m g (15.1m r) | 10.6m g (7.6m r) | 6.6m g (4.7m r) |
| `venbar` | Barracks, 17th century | 94g | 12 | 1.8m g (1.3m r) | 53g (38r) | 21g (15r) | 11g (8r) | 9g (6r) |
| `venbla` | Blacksmith | 94g | 12 | 1.8m g (1.3m r) | 53g (38r) | 21g (15r) | 11g (8r) | 9g (6r) |
| `vencen` | Town Hall | 156g | 16 | 2.9m g (2.1m r) | 1.5m g (1.1m r) | 35g (25r) | 18g (13r) | 11g (8r) |
| `vendip` | Diplomatic Center | 312g | 12 | 5.9m g (4.2m r) | 2.9m g (2.1m r) | 1.2m g (0.8m r) | 35g (25r) | 29g (21r) |
| `venhou` | Housing | 31g | 12 | 35g (25r) | 18g (13r) | 7g (5r) | 4g (3r) | 3g (2r) |
| `vensta` | Stable | 625g | 12 | 11.8m g (8.4m r) | 5.9m g (4.2m r) | 2.4m g (1.7m r) | 1.2m g (0.8m r) | 59g (42r) |
| `ventem` | Cathedral | 156g | 12 | 2.9m g (2.1m r) | 1.5m g (1.1m r) | 35g (25r) | 18g (13r) | 15g (11r) |

### Полный ремонт (0 → max HP)

| sid | имя | maxhp | slot_cap | 1 builders | 2 builders | 5 builders | 10 builders | max builders |
|---|---|---|---|---|---|---|---|---|
| `eurcoa` | Mine | 2500 | 12 | 51g (36r) | 25g (18r) | 10g (7r) | 5g (4r) | 4g (3r) |
| `eurgol` | Mine | 2500 | 12 | 51g (36r) | 25g (18r) | 10g (7r) | 5g (4r) | 4g (3r) |
| `euriro` | Mine | 2500 | 12 | 51g (36r) | 25g (18r) | 10g (7r) | 5g (4r) | 4g (3r) |
| `eurmar` | Market | 4000 | 12 | 1.4m g (1.0m r) | 41g (29r) | 16g (12r) | 8g (6r) | 7g (5r) |
| `eurmil` | Mill | 20000 | 12 | 6.8m g (4.8m r) | 3.4m g (2.4m r) | 1.4m g (1.0m r) | 41g (29r) | 34g (24r) |
| `eurpor` | Shipyard | 50000 | 16 | 16.9m g (12.1m r) | 8.5m g (6.0m r) | 3.4m g (2.4m r) | 1.7m g (1.2m r) | 1.1m g (0.8m r) |
| `eursga` | Gate | 50000 | 4 | 16.9m g (12.1m r) | 8.5m g (6.0m r) | 4.2m g (3.0m r) | 4.2m g (3.0m r) | 4.2m g (3.0m r) |
| `eursto` | Storehouse | 10000 | 12 | 3.4m g (2.4m r) | 1.7m g (1.2m r) | 41g (29r) | 20g (15r) | 17g (12r) |
| `eurswa` | Wall | 50000 | 4 | 16.9m g (12.1m r) | 8.5m g (6.0m r) | 4.2m g (3.0m r) | 4.2m g (3.0m r) | 4.2m g (3.0m r) |
| `eurtow` | Tower | 20000 | 8 | 6.8m g (4.8m r) | 3.4m g (2.4m r) | 1.4m g (1.0m r) | 51g (36r) | 51g (36r) |
| `venaca` | Academy | 63000 | 16 | 21.3m g (15.2m r) | 10.7m g (7.6m r) | 4.3m g (3.0m r) | 2.1m g (1.5m r) | 1.3m g (1.0m r) |
| `venart` | Artillery Depot | 40000 | 12 | 13.5m g (9.7m r) | 6.8m g (4.8m r) | 2.7m g (1.9m r) | 1.4m g (1.0m r) | 1.1m g (0.8m r) |
| `venba2` | Barracks, 18th century | 55000 | 16 | 18.6m g (13.3m r) | 9.3m g (6.6m r) | 3.7m g (2.7m r) | 1.9m g (1.3m r) | 1.2m g (0.8m r) |
| `venbar` | Barracks, 17th century | 40000 | 12 | 13.5m g (9.7m r) | 6.8m g (4.8m r) | 2.7m g (1.9m r) | 1.4m g (1.0m r) | 1.1m g (0.8m r) |
| `venbla` | Blacksmith | 5500 | 12 | 1.9m g (1.3m r) | 56g (40r) | 22g (16r) | 11g (8r) | 9g (7r) |
| `vencen` | Town Hall | 5100 | 16 | 1.7m g (1.2m r) | 52g (37r) | 21g (15r) | 10g (7r) | 6g (5r) |
| `vendip` | Diplomatic Center | 4500 | 12 | 1.5m g (1.1m r) | 46g (33r) | 18g (13r) | 9g (7r) | 8g (5r) |
| `venhou` | Housing | 5000 | 12 | 1.7m g (1.2m r) | 51g (36r) | 20g (15r) | 10g (7r) | 8g (6r) |
| `vensta` | Stable | 20000 | 12 | 6.8m g (4.8m r) | 3.4m g (2.4m r) | 1.4m g (1.0m r) | 41g (29r) | 34g (24r) |
| `ventem` | Cathedral | 4200 | 12 | 1.4m g (1.0m r) | 43g (30r) | 17g (12r) | 9g (6r) | 7g (5r) |
