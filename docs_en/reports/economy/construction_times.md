<a id="cossacks-3--время-постройки-и-ремонта"></a>
<a id="время-строительства-и-ремонта"></a>
# Cossacks 3 - Time to build and repair

[← Tables and calculations](../README.md)

Construction time (from scratch, new building) and repair (totally damaged → full HP) for each building. It is calculated for different numbers of peasants.

**Formulas** (see [`recon/world/economy/building_mechanics.md`](../../recon/world/economy/building_mechanics.md)):

- **Building**, time with N peasants: `buildtime_sec × 1.13 / N` (limited by slot cap)
- **Repair**, time with N peasants: `maxhp / (20 × N / 0.406)` g-sec
- 1 animation cycle construct = 13 frames / 32 fps = **0.406 g-sec**
- At fast speed: real-time = g-sec / 1.4

**Slot caps** (exact simulation of `_unit_CalcBuilderPoints` for each building, see [`builder_slots.md`](builder_slots.md)):

- Cap depends on the **perimeter of the collision mask** of a particular building - for different nations the same category (for example, an 18th century barracks) can have from 19 to 30 slots.
- Walls/gates: **4** slots per segment (value from `wallcustom.cfg`, for sids not in `builder_slots.json`).
- Hard engine limit: `gc_MaxBuilderCount = 30`.

**Columns:** time in `<g-sec>g (<real-sec>r fast)` format. For long-term values - in minutes.

<a id="alg--algeria-алжир"></a>
<a id="алжир-alg"></a>
## Algeria (`alg`)
<a id="постройка-с-нуля"></a>
### Building from scratch

| sid | name | buildtime_g | slot_cap | 1 is building. | 2 is building. | 5 is building. | 10 is building. | Max. builds. |
|---|---|---|---|---|---|---|---|---|
| `algaca` | Minaret | 156g | 25 | 2.9m g (2.1m r) | 1.5m g (1.1m r) | 35g (25r) | 18g (13r) | 7g (5r) |
| `algart` | Artillery Depot | 246g | 24 | 4.6m g (3.3m r) | 2.3m g (1.7m r) | 56g (40r) | 28g (20r) | 12g (8r) |
| `algbar` | Barracks | 94g | 23 | 1.8m g (1.3m r) | 53g (38r) | 21g (15r) | 11g (8r) | 5g (3r) |
| `algbla` | Blacksmith | 109g | 15 | 2.1m g (1.5m r) | 1.0m g (0.7m r) | 25g (18r) | 12g (9r) | 8g (6r) |
| `algcen` | Town Hall | 156g | 21 | 2.9m g (2.1m r) | 1.5m g (1.1m r) | 35g (25r) | 18g (13r) | 8g (6r) |
| `algdip` | Diplomatic Center | 312g | 18 | 5.9m g (4.2m r) | 2.9m g (2.1m r) | 1.2m g (0.8m r) | 35g (25r) | 20g (14r) |
| `alghou` | Housing | 31g | 16 | 35g (25r) | 18g (13r) | 7g (5r) | 4g (3r) | 2g (2r) |
| `algsta` | Stable | 156g | 22 | 2.9m g (2.1m r) | 1.5m g (1.1m r) | 35g (25r) | 18g (13r) | 8g (6r) |
| `algtem` | Mosque | 94g | 30 | 1.8m g (1.3m r) | 53g (38r) | 21g (15r) | 11g (8r) | 4g (3r) |
| `eurcoa` | Mine | 94g | 16 | 1.8m g (1.3m r) | 53g (38r) | 21g (15r) | 11g (8r) | 7g (5r) |
| `eurgol` | Mine | 94g | 16 | 1.8m g (1.3m r) | 53g (38r) | 21g (15r) | 11g (8r) | 7g (5r) |
| `euriro` | Mine | 94g | 16 | 1.8m g (1.3m r) | 53g (38r) | 21g (15r) | 11g (8r) | 7g (5r) |
| `turmar` | Bazaar | 234g | 19 | 4.4m g (3.2m r) | 2.2m g (1.6m r) | 53g (38r) | 26g (19r) | 14g (10r) |
| `turmil` | Mill | 94g | 16 | 1.8m g (1.3m r) | 53g (38r) | 21g (15r) | 11g (8r) | 7g (5r) |
| `turpor` | Shipyard | 1562g | 30 | 29.4m g (21.0m r) | 14.7m g (10.5m r) | 5.9m g (4.2m r) | 2.9m g (2.1m r) | 59g (42r) |
| `tursga` | Gate | 120g | 13 | 2.3m g (1.6m r) | 1.1m g (0.8m r) | 27g (19r) | 14g (10r) | 10g (7r) |
| `tursto` | Storehouse | 31g | 8 | 35g (25r) | 18g (13r) | 7g (5r) | 4g (3r) | 4g (3r) |
| `turswa` | Wall | 120g | 4 | 2.3m g (1.6m r) | 1.1m g (0.8m r) | 34g (24r) | 34g (24r) | 34g (24r) |
| `turtow` | Tower | 984g | 14 | 18.5m g (13.2m r) | 9.3m g (6.6m r) | 3.7m g (2.6m r) | 1.9m g (1.3m r) | 1.3m g (0.9m r) |
| `ukrwga` | Gate | 6g | 13 | 6g (5r) | 3g (2r) | 1g (1r) | 1g (0r) | 0g (0r) |
| `ukrwwa` | Palisade | 6g | 4 | 6g (5r) | 3g (2r) | 2g (1r) | 2g (1r) | 2g (1r) |

<a id="полный-ремонт"></a>
### Full repair (0 → max HP)
| sid | name | maxhp | slot_cap | 1 is building. | 2 is building. | 5 is building. | 10 is building. | Max. builds. |
|---|---|---|---|---|---|---|---|---|
| `algaca` | Minaret | 65000 | 25 | 22.0m g (15.7m r) | 11.0m g (7.9m r) | 4.4m g (3.1m r) | 2.2m g (1.6m r) | 53g (38r) |
| `algart` | Artillery Depot | 40000 | 24 | 13.5m g (9.7m r) | 6.8m g (4.8m r) | 2.7m g (1.9m r) | 1.4m g (1.0m r) | 34g (24r) |
| `algbar` | Barracks | 35000 | 23 | 11.8m g (8.5m r) | 5.9m g (4.2m r) | 2.4m g (1.7m r) | 1.2m g (0.8m r) | 31g (22r) |
| `algbla` | Blacksmith | 6500 | 15 | 2.2m g (1.6m r) | 1.1m g (0.8m r) | 26g (19r) | 13g (9r) | 9g (6r) |
| `algcen` | Town Hall | 5500 | 21 | 1.9m g (1.3m r) | 56g (40r) | 22g (16r) | 11g (8r) | 5g (4r) |
| `algdip` | Diplomatic Center | 5500 | 18 | 1.9m g (1.3m r) | 56g (40r) | 22g (16r) | 11g (8r) | 6g (4r) |
| `alghou` | Housing | 4300 | 16 | 1.5m g (1.0m r) | 44g (31r) | 17g (12r) | 9g (6r) | 5g (4r) |
| `algsta` | Stable | 55000 | 22 | 18.6m g (13.3m r) | 9.3m g (6.6m r) | 3.7m g (2.7m r) | 1.9m g (1.3m r) | 51g (36r) |
| `algtem` | Mosque | 5000 | 30 | 1.7m g (1.2m r) | 51g (36r) | 20g (15r) | 10g (7r) | 3g (2r) |
| `eurcoa` | Mine | 2500 | 16 | 51g (36r) | 25g (18r) | 10g (7r) | 5g (4r) | 3g (2r) |
| `eurgol` | Mine | 2500 | 16 | 51g (36r) | 25g (18r) | 10g (7r) | 5g (4r) | 3g (2r) |
| `euriro` | Mine | 2500 | 16 | 51g (36r) | 25g (18r) | 10g (7r) | 5g (4r) | 3g (2r) |
| `turmar` | Bazaar | 4500 | 19 | 1.5m g (1.1m r) | 46g (33r) | 18g (13r) | 9g (7r) | 5g (3r) |
| `turmil` | Mill | 20000 | 16 | 6.8m g (4.8m r) | 3.4m g (2.4m r) | 1.4m g (1.0m r) | 41g (29r) | 25g (18r) |
| `turpor` | Shipyard | 40000 | 30 | 13.5m g (9.7m r) | 6.8m g (4.8m r) | 2.7m g (1.9m r) | 1.4m g (1.0m r) | 27g (19r) |
| `tursga` | Gate | 32000 | 13 | 10.8m g (7.7m r) | 5.4m g (3.9m r) | 2.2m g (1.5m r) | 1.1m g (0.8m r) | 50g (36r) |
| `tursto` | Storehouse | 10000 | 8 | 3.4m g (2.4m r) | 1.7m g (1.2m r) | 41g (29r) | 25g (18r) | 25g (18r) |
| `turswa` | Wall | 50000 | 4 | 16.9m g (12.1m r) | 8.5m g (6.0m r) | 4.2m g (3.0m r) | 4.2m g (3.0m r) | 4.2m g (3.0m r) |
| `turtow` | Tower | 22500 | 14 | 7.6m g (5.4m r) | 3.8m g (2.7m r) | 1.5m g (1.1m r) | 46g (33r) | 33g (23r) |
| `ukrwga` | Gate | 1500 | 13 | 30g (22r) | 15g (11r) | 6g (4r) | 3g (2r) | 2g (2r) |
| `ukrwwa` | Palisade | 1500 | 4 | 30g (22r) | 15g (11r) | 8g (5r) | 8g (5r) | 8g (5r) |

<a id="aus--austria-австрия"></a>
<a id="австрия-aus"></a>
## Austria (`aus`)
<a id="постройка-с-нуля-1"></a>
### Building from scratch

| sid | name | buildtime_g | slot_cap | 1 is building. | 2 is building. | 5 is building. | 10 is building. | Max. builds. |
|---|---|---|---|---|---|---|---|---|
| `ausaca` | Academy | 625g | 26 | 11.8m g (8.4m r) | 5.9m g (4.2m r) | 2.4m g (1.7m r) | 1.2m g (0.8m r) | 27g (19r) |
| `ausart` | Artillery Depot | 246g | 22 | 4.6m g (3.3m r) | 2.3m g (1.7m r) | 56g (40r) | 28g (20r) | 13g (9r) |
| `ausba2` | Barracks, 18th century | 5625g | 29 | 105.9m g (75.7m r) | 53.0m g (37.8m r) | 21.2m g (15.1m r) | 10.6m g (7.6m r) | 3.7m g (2.6m r) |
| `ausbar` | Barracks, 17th century | 94g | 25 | 1.8m g (1.3m r) | 53g (38r) | 21g (15r) | 11g (8r) | 4g (3r) |
| `ausbla` | Blacksmith | 94g | 17 | 1.8m g (1.3m r) | 53g (38r) | 21g (15r) | 11g (8r) | 6g (4r) |
| `auscen` | Town Hall | 47g | 23 | 53g (38r) | 26g (19r) | 11g (8r) | 5g (4r) | 2g (2r) |
| `ausdip` | Diplomatic Center | 312g | 24 | 5.9m g (4.2m r) | 2.9m g (2.1m r) | 1.2m g (0.8m r) | 35g (25r) | 15g (11r) |
| `aushou` | Housing | 31g | 15 | 35g (25r) | 18g (13r) | 7g (5r) | 4g (3r) | 2g (2r) |
| `aussta` | Stable | 625g | 21 | 11.8m g (8.4m r) | 5.9m g (4.2m r) | 2.4m g (1.7m r) | 1.2m g (0.8m r) | 34g (24r) |
| `austem` | Cathedral | 156g | 28 | 2.9m g (2.1m r) | 1.5m g (1.1m r) | 35g (25r) | 18g (13r) | 6g (5r) |
| `eurcoa` | Mine | 94g | 16 | 1.8m g (1.3m r) | 53g (38r) | 21g (15r) | 11g (8r) | 7g (5r) |
| `eurgol` | Mine | 94g | 16 | 1.8m g (1.3m r) | 53g (38r) | 21g (15r) | 11g (8r) | 7g (5r) |
| `euriro` | Mine | 94g | 16 | 1.8m g (1.3m r) | 53g (38r) | 21g (15r) | 11g (8r) | 7g (5r) |
| `eurmar` | Market | 234g | 25 | 4.4m g (3.2m r) | 2.2m g (1.6m r) | 53g (38r) | 26g (19r) | 11g (8r) |
| `eurmil` | Mill | 94g | 10 | 1.8m g (1.3m r) | 53g (38r) | 21g (15r) | 11g (8r) | 11g (8r) |
| `eurpor` | Shipyard | 1562g | 30 | 29.4m g (21.0m r) | 14.7m g (10.5m r) | 5.9m g (4.2m r) | 2.9m g (2.1m r) | 59g (42r) |
| `eursga` | Gate | 90g | 13 | 1.7m g (1.2m r) | 51g (36r) | 20g (15r) | 10g (7r) | 8g (6r) |
| `eursto` | Storehouse | 31g | 9 | 35g (25r) | 18g (13r) | 7g (5r) | 4g (3r) | 4g (3r) |
| `eurswa` | Wall | 90g | 4 | 1.7m g (1.2m r) | 51g (36r) | 25g (18r) | 25g (18r) | 25g (18r) |
| `eurtow` | Tower | 1230g | 10 | 23.2m g (16.6m r) | 11.6m g (8.3m r) | 4.6m g (3.3m r) | 2.3m g (1.7m r) | 2.3m g (1.7m r) |
| `ukrwga` | Gate | 6g | 13 | 6g (5r) | 3g (2r) | 1g (1r) | 1g (0r) | 0g (0r) |
| `ukrwwa` | Palisade | 6g | 4 | 6g (5r) | 3g (2r) | 2g (1r) | 2g (1r) | 2g (1r) |

<a id="полный-ремонт-0--max-hp"></a>
<a id="полный-ремонт-1"></a>
### Full repair (0 → max HP)

| sid | name | maxhp | slot_cap | 1 is building. | 2 is building. | 5 is building. | 10 is building. | Max. builds. |
|---|---|---|---|---|---|---|---|---|
| `ausaca` | Academy | 65000 | 26 | 22.0m g (15.7m r) | 11.0m g (7.9m r) | 4.4m g (3.1m r) | 2.2m g (1.6m r) | 51g (36r) |
| `ausart` | Artillery Depot | 40000 | 22 | 13.5m g (9.7m r) | 6.8m g (4.8m r) | 2.7m g (1.9m r) | 1.4m g (1.0m r) | 37g (26r) |
| `ausba2` | Barracks, 18th century | 55000 | 29 | 18.6m g (13.3m r) | 9.3m g (6.6m r) | 3.7m g (2.7m r) | 1.9m g (1.3m r) | 39g (28r) |
| `ausbar` | Barracks, 17th century | 40000 | 25 | 13.5m g (9.7m r) | 6.8m g (4.8m r) | 2.7m g (1.9m r) | 1.4m g (1.0m r) | 32g (23r) |
| `ausbla` | Blacksmith | 5500 | 17 | 1.9m g (1.3m r) | 56g (40r) | 22g (16r) | 11g (8r) | 7g (5r) |
| `auscen` | Town Hall | 4000 | 23 | 1.4m g (1.0m r) | 41g (29r) | 16g (12r) | 8g (6r) | 4g (3r) |
| `ausdip` | Diplomatic Center | 4500 | 24 | 1.5m g (1.1m r) | 46g (33r) | 18g (13r) | 9g (7r) | 4g (3r) |
| `aushou` | Housing | 4000 | 15 | 1.4m g (1.0m r) | 41g (29r) | 16g (12r) | 8g (6r) | 5g (4r) |
| `aussta` | Stable | 20000 | 21 | 6.8m g (4.8m r) | 3.4m g (2.4m r) | 1.4m g (1.0m r) | 41g (29r) | 19g (14r) |
| `austem` | Cathedral | 4200 | 28 | 1.4m g (1.0m r) | 43g (30r) | 17g (12r) | 9g (6r) | 3g (2r) |
| `eurcoa` | Mine | 2500 | 16 | 51g (36r) | 25g (18r) | 10g (7r) | 5g (4r) | 3g (2r) |
| `eurgol` | Mine | 2500 | 16 | 51g (36r) | 25g (18r) | 10g (7r) | 5g (4r) | 3g (2r) |
| `euriro` | Mine | 2500 | 16 | 51g (36r) | 25g (18r) | 10g (7r) | 5g (4r) | 3g (2r) |
| `eurmar` | Market | 4000 | 25 | 1.4m g (1.0m r) | 41g (29r) | 16g (12r) | 8g (6r) | 3g (2r) |
| `eurmil` | Mill | 20000 | 10 | 6.8m g (4.8m r) | 3.4m g (2.4m r) | 1.4m g (1.0m r) | 41g (29r) | 41g (29r) |
| `eurpor` | Shipyard | 50000 | 30 | 16.9m g (12.1m r) | 8.5m g (6.0m r) | 3.4m g (2.4m r) | 1.7m g (1.2m r) | 34g (24r) |
| `eursga` | Gate | 32000 | 13 | 10.8m g (7.7m r) | 5.4m g (3.9m r) | 2.2m g (1.5m r) | 1.1m g (0.8m r) | 50g (36r) |
| `eursto` | Storehouse | 10000 | 9 | 3.4m g (2.4m r) | 1.7m g (1.2m r) | 41g (29r) | 23g (16r) | 23g (16r) |
| `eurswa` | Wall | 50000 | 4 | 16.9m g (12.1m r) | 8.5m g (6.0m r) | 4.2m g (3.0m r) | 4.2m g (3.0m r) | 4.2m g (3.0m r) |
| `eurtow` | Tower | 20000 | 10 | 6.8m g (4.8m r) | 3.4m g (2.4m r) | 1.4m g (1.0m r) | 41g (29r) | 41g (29r) |
| `ukrwga` | Gate | 1500 | 13 | 30g (22r) | 15g (11r) | 6g (4r) | 3g (2r) | 2g (2r) |
| `ukrwwa` | Palisade | 1500 | 4 | 30g (22r) | 15g (11r) | 8g (5r) | 8g (5r) | 8g (5r) |

<a id="bav--bavaria-бавария"></a>
<a id="бавария-bav"></a>
## Bavaria (`bav`)
<a id="постройка-с-нуля-2"></a>
### Building from scratch

| sid | name | buildtime_g | slot_cap | 1 is building. | 2 is building. | 5 is building. | 10 is building. | Max. builds. |
|---|---|---|---|---|---|---|---|---|
| `bavaca` | Academy | 625g | 22 | 11.8m g (8.4m r) | 5.9m g (4.2m r) | 2.4m g (1.7m r) | 1.2m g (0.8m r) | 32g (23r) |
| `bavart` | Artillery Depot | 246g | 20 | 4.6m g (3.3m r) | 2.3m g (1.7m r) | 56g (40r) | 28g (20r) | 14g (10r) |
| `bavba2` | Barracks, 18th century | 5625g | 23 | 105.9m g (75.7m r) | 53.0m g (37.8m r) | 21.2m g (15.1m r) | 10.6m g (7.6m r) | 4.6m g (3.3m r) |
| `bavbar` | Barracks, 17th century | 94g | 23 | 1.8m g (1.3m r) | 53g (38r) | 21g (15r) | 11g (8r) | 5g (3r) |
| `bavbla` | Blacksmith | 94g | 16 | 1.8m g (1.3m r) | 53g (38r) | 21g (15r) | 11g (8r) | 7g (5r) |
| `bavcen` | Town Hall | 156g | 21 | 2.9m g (2.1m r) | 1.5m g (1.1m r) | 35g (25r) | 18g (13r) | 8g (6r) |
| `bavdip` | Diplomatic Center | 312g | 18 | 5.9m g (4.2m r) | 2.9m g (2.1m r) | 1.2m g (0.8m r) | 35g (25r) | 20g (14r) |
| `bavhou` | Housing | 31g | 16 | 35g (25r) | 18g (13r) | 7g (5r) | 4g (3r) | 2g (2r) |
| `bavsta` | Stable | 625g | 21 | 11.8m g (8.4m r) | 5.9m g (4.2m r) | 2.4m g (1.7m r) | 1.2m g (0.8m r) | 34g (24r) |
| `bavtem` | Cathedral | 156g | 22 | 2.9m g (2.1m r) | 1.5m g (1.1m r) | 35g (25r) | 18g (13r) | 8g (6r) |
| `eurcoa` | Mine | 94g | 16 | 1.8m g (1.3m r) | 53g (38r) | 21g (15r) | 11g (8r) | 7g (5r) |
| `eurgol` | Mine | 94g | 16 | 1.8m g (1.3m r) | 53g (38r) | 21g (15r) | 11g (8r) | 7g (5r) |
| `euriro` | Mine | 94g | 16 | 1.8m g (1.3m r) | 53g (38r) | 21g (15r) | 11g (8r) | 7g (5r) |
| `eurmar` | Market | 234g | 25 | 4.4m g (3.2m r) | 2.2m g (1.6m r) | 53g (38r) | 26g (19r) | 11g (8r) |
| `eurmil` | Mill | 94g | 10 | 1.8m g (1.3m r) | 53g (38r) | 21g (15r) | 11g (8r) | 11g (8r) |
| `eurpor` | Shipyard | 1562g | 30 | 29.4m g (21.0m r) | 14.7m g (10.5m r) | 5.9m g (4.2m r) | 2.9m g (2.1m r) | 59g (42r) |
| `eursga` | Gate | 90g | 13 | 1.7m g (1.2m r) | 51g (36r) | 20g (15r) | 10g (7r) | 8g (6r) |
| `eursto` | Storehouse | 31g | 9 | 35g (25r) | 18g (13r) | 7g (5r) | 4g (3r) | 4g (3r) |
| `eurswa` | Wall | 90g | 4 | 1.7m g (1.2m r) | 51g (36r) | 25g (18r) | 25g (18r) | 25g (18r) |
| `eurtow` | Tower | 1230g | 10 | 23.2m g (16.6m r) | 11.6m g (8.3m r) | 4.6m g (3.3m r) | 2.3m g (1.7m r) | 2.3m g (1.7m r) |
| `ukrwga` | Gate | 6g | 13 | 6g (5r) | 3g (2r) | 1g (1r) | 1g (0r) | 0g (0r) |
| `ukrwwa` | Palisade | 6g | 4 | 6g (5r) | 3g (2r) | 2g (1r) | 2g (1r) | 2g (1r) |

<a id="полный-ремонт-0--max-hp-1"></a>
<a id="полный-ремонт-2"></a>
### Full repair (0 → max HP)

| sid | name | maxhp | slot_cap | 1 is building. | 2 is building. | 5 is building. | 10 is building. | Max. builds. |
|---|---|---|---|---|---|---|---|---|
| `bavaca` | Academy | 63000 | 22 | 21.3m g (15.2m r) | 10.7m g (7.6m r) | 4.3m g (3.0m r) | 2.1m g (1.5m r) | 58g (42r) |
| `bavart` | Artillery Depot | 40000 | 20 | 13.5m g (9.7m r) | 6.8m g (4.8m r) | 2.7m g (1.9m r) | 1.4m g (1.0m r) | 41g (29r) |
| `bavba2` | Barracks, 18th century | 55000 | 23 | 18.6m g (13.3m r) | 9.3m g (6.6m r) | 3.7m g (2.7m r) | 1.9m g (1.3m r) | 49g (35r) |
| `bavbar` | Barracks, 17th century | 40000 | 23 | 13.5m g (9.7m r) | 6.8m g (4.8m r) | 2.7m g (1.9m r) | 1.4m g (1.0m r) | 35g (25r) |
| `bavbla` | Blacksmith | 5500 | 16 | 1.9m g (1.3m r) | 56g (40r) | 22g (16r) | 11g (8r) | 7g (5r) |
| `bavcen` | Town Hall | 4000 | 21 | 1.4m g (1.0m r) | 41g (29r) | 16g (12r) | 8g (6r) | 4g (3r) |
| `bavdip` | Diplomatic Center | 4500 | 18 | 1.5m g (1.1m r) | 46g (33r) | 18g (13r) | 9g (7r) | 5g (4r) |
| `bavhou` | Housing | 4000 | 16 | 1.4m g (1.0m r) | 41g (29r) | 16g (12r) | 8g (6r) | 5g (4r) |
| `bavsta` | Stable | 20000 | 21 | 6.8m g (4.8m r) | 3.4m g (2.4m r) | 1.4m g (1.0m r) | 41g (29r) | 19g (14r) |
| `bavtem` | Cathedral | 4200 | 22 | 1.4m g (1.0m r) | 43g (30r) | 17g (12r) | 9g (6r) | 4g (3r) |
| `eurcoa` | Mine | 2500 | 16 | 51g (36r) | 25g (18r) | 10g (7r) | 5g (4r) | 3g (2r) |
| `eurgol` | Mine | 2500 | 16 | 51g (36r) | 25g (18r) | 10g (7r) | 5g (4r) | 3g (2r) |
| `euriro` | Mine | 2500 | 16 | 51g (36r) | 25g (18r) | 10g (7r) | 5g (4r) | 3g (2r) |
| `eurmar` | Market | 4000 | 25 | 1.4m g (1.0m r) | 41g (29r) | 16g (12r) | 8g (6r) | 3g (2r) |
| `eurmil` | Mill | 20000 | 10 | 6.8m g (4.8m r) | 3.4m g (2.4m r) | 1.4m g (1.0m r) | 41g (29r) | 41g (29r) |
| `eurpor` | Shipyard | 50000 | 30 | 16.9m g (12.1m r) | 8.5m g (6.0m r) | 3.4m g (2.4m r) | 1.7m g (1.2m r) | 34g (24r) |
| `eursga` | Gate | 32000 | 13 | 10.8m g (7.7m r) | 5.4m g (3.9m r) | 2.2m g (1.5m r) | 1.1m g (0.8m r) | 50g (36r) |
| `eursto` | Storehouse | 10000 | 9 | 3.4m g (2.4m r) | 1.7m g (1.2m r) | 41g (29r) | 23g (16r) | 23g (16r) |
| `eurswa` | Wall | 50000 | 4 | 16.9m g (12.1m r) | 8.5m g (6.0m r) | 4.2m g (3.0m r) | 4.2m g (3.0m r) | 4.2m g (3.0m r) |
| `eurtow` | Tower | 20000 | 10 | 6.8m g (4.8m r) | 3.4m g (2.4m r) | 1.4m g (1.0m r) | 41g (29r) | 41g (29r) |
| `ukrwga` | Gate | 1500 | 13 | 30g (22r) | 15g (11r) | 6g (4r) | 3g (2r) | 2g (2r) |
| `ukrwwa` | Palisade | 1500 | 4 | 30g (22r) | 15g (11r) | 8g (5r) | 8g (5r) | 8g (5r) |

<a id="den--denmark-дания"></a>
<a id="дания-den"></a>
## Denmark (`den`)
<a id="постройка-с-нуля-3"></a>
### Building from scratch

| sid | name | buildtime_g | slot_cap | 1 is building. | 2 is building. | 5 is building. | 10 is building. | Max. builds. |
|---|---|---|---|---|---|---|---|---|
| `denaca` | Academy | 625g | 17 | 11.8m g (8.4m r) | 5.9m g (4.2m r) | 2.4m g (1.7m r) | 1.2m g (0.8m r) | 42g (30r) |
| `denart` | Artillery Depot | 246g | 20 | 4.6m g (3.3m r) | 2.3m g (1.7m r) | 56g (40r) | 28g (20r) | 14g (10r) |
| `denba2` | Barracks, 18th century | 5625g | 22 | 105.9m g (75.7m r) | 53.0m g (37.8m r) | 21.2m g (15.1m r) | 10.6m g (7.6m r) | 4.8m g (3.4m r) |
| `denbar` | Barracks, 17th century | 94g | 20 | 1.8m g (1.3m r) | 53g (38r) | 21g (15r) | 11g (8r) | 5g (4r) |
| `denbla` | Blacksmith | 94g | 16 | 1.8m g (1.3m r) | 53g (38r) | 21g (15r) | 11g (8r) | 7g (5r) |
| `dencen` | Town Hall | 156g | 20 | 2.9m g (2.1m r) | 1.5m g (1.1m r) | 35g (25r) | 18g (13r) | 9g (6r) |
| `dendip` | Diplomatic Center | 312g | 21 | 5.9m g (4.2m r) | 2.9m g (2.1m r) | 1.2m g (0.8m r) | 35g (25r) | 17g (12r) |
| `denhou` | Housing | 31g | 13 | 35g (25r) | 18g (13r) | 7g (5r) | 4g (3r) | 3g (2r) |
| `densta` | Stable | 625g | 20 | 11.8m g (8.4m r) | 5.9m g (4.2m r) | 2.4m g (1.7m r) | 1.2m g (0.8m r) | 35g (25r) |
| `dentem` | Cathedral | 156g | 22 | 2.9m g (2.1m r) | 1.5m g (1.1m r) | 35g (25r) | 18g (13r) | 8g (6r) |
| `eurcoa` | Mine | 94g | 16 | 1.8m g (1.3m r) | 53g (38r) | 21g (15r) | 11g (8r) | 7g (5r) |
| `eurgol` | Mine | 94g | 16 | 1.8m g (1.3m r) | 53g (38r) | 21g (15r) | 11g (8r) | 7g (5r) |
| `euriro` | Mine | 94g | 16 | 1.8m g (1.3m r) | 53g (38r) | 21g (15r) | 11g (8r) | 7g (5r) |
| `eurmar` | Market | 234g | 25 | 4.4m g (3.2m r) | 2.2m g (1.6m r) | 53g (38r) | 26g (19r) | 11g (8r) |
| `eurmil` | Mill | 94g | 10 | 1.8m g (1.3m r) | 53g (38r) | 21g (15r) | 11g (8r) | 11g (8r) |
| `eurpor` | Shipyard | 1562g | 30 | 29.4m g (21.0m r) | 14.7m g (10.5m r) | 5.9m g (4.2m r) | 2.9m g (2.1m r) | 59g (42r) |
| `eursga` | Gate | 90g | 13 | 1.7m g (1.2m r) | 51g (36r) | 20g (15r) | 10g (7r) | 8g (6r) |
| `eursto` | Storehouse | 31g | 9 | 35g (25r) | 18g (13r) | 7g (5r) | 4g (3r) | 4g (3r) |
| `eurswa` | Wall | 90g | 4 | 1.7m g (1.2m r) | 51g (36r) | 25g (18r) | 25g (18r) | 25g (18r) |
| `eurtow` | Tower | 1230g | 10 | 23.2m g (16.6m r) | 11.6m g (8.3m r) | 4.6m g (3.3m r) | 2.3m g (1.7m r) | 2.3m g (1.7m r) |
| `ukrwga` | Gate | 6g | 13 | 6g (5r) | 3g (2r) | 1g (1r) | 1g (0r) | 0g (0r) |
| `ukrwwa` | Palisade | 6g | 4 | 6g (5r) | 3g (2r) | 2g (1r) | 2g (1r) | 2g (1r) |

<a id="полный-ремонт-0--max-hp-2"></a>
<a id="полный-ремонт-3"></a>
### Full repair (0 → max HP)

| sid | name | maxhp | slot_cap | 1 is building. | 2 is building. | 5 is building. | 10 is building. | Max. builds. |
|---|---|---|---|---|---|---|---|---|
| `denaca` | Academy | 63000 | 17 | 21.3m g (15.2m r) | 10.7m g (7.6m r) | 4.3m g (3.0m r) | 2.1m g (1.5m r) | 1.3m g (0.9m r) |
| `denart` | Artillery Depot | 40000 | 20 | 13.5m g (9.7m r) | 6.8m g (4.8m r) | 2.7m g (1.9m r) | 1.4m g (1.0m r) | 41g (29r) |
| `denba2` | Barracks, 18th century | 55000 | 22 | 18.6m g (13.3m r) | 9.3m g (6.6m r) | 3.7m g (2.7m r) | 1.9m g (1.3m r) | 51g (36r) |
| `denbar` | Barracks, 17th century | 40000 | 20 | 13.5m g (9.7m r) | 6.8m g (4.8m r) | 2.7m g (1.9m r) | 1.4m g (1.0m r) | 41g (29r) |
| `denbla` | Blacksmith | 5500 | 16 | 1.9m g (1.3m r) | 56g (40r) | 22g (16r) | 11g (8r) | 7g (5r) |
| `dencen` | Town Hall | 4030 | 20 | 1.4m g (1.0m r) | 41g (29r) | 16g (12r) | 8g (6r) | 4g (3r) |
| `dendip` | Diplomatic Center | 4500 | 21 | 1.5m g (1.1m r) | 46g (33r) | 18g (13r) | 9g (7r) | 4g (3r) |
| `denhou` | Housing | 4000 | 13 | 1.4m g (1.0m r) | 41g (29r) | 16g (12r) | 8g (6r) | 6g (4r) |
| `densta` | Stable | 20000 | 20 | 6.8m g (4.8m r) | 3.4m g (2.4m r) | 1.4m g (1.0m r) | 41g (29r) | 20g (15r) |
| `dentem` | Cathedral | 4200 | 22 | 1.4m g (1.0m r) | 43g (30r) | 17g (12r) | 9g (6r) | 4g (3r) |
| `eurcoa` | Mine | 2500 | 16 | 51g (36r) | 25g (18r) | 10g (7r) | 5g (4r) | 3g (2r) |
| `eurgol` | Mine | 2500 | 16 | 51g (36r) | 25g (18r) | 10g (7r) | 5g (4r) | 3g (2r) |
| `euriro` | Mine | 2500 | 16 | 51g (36r) | 25g (18r) | 10g (7r) | 5g (4r) | 3g (2r) |
| `eurmar` | Market | 4000 | 25 | 1.4m g (1.0m r) | 41g (29r) | 16g (12r) | 8g (6r) | 3g (2r) |
| `eurmil` | Mill | 20000 | 10 | 6.8m g (4.8m r) | 3.4m g (2.4m r) | 1.4m g (1.0m r) | 41g (29r) | 41g (29r) |
| `eurpor` | Shipyard | 50000 | 30 | 16.9m g (12.1m r) | 8.5m g (6.0m r) | 3.4m g (2.4m r) | 1.7m g (1.2m r) | 34g (24r) |
| `eursga` | Gate | 32000 | 13 | 10.8m g (7.7m r) | 5.4m g (3.9m r) | 2.2m g (1.5m r) | 1.1m g (0.8m r) | 50g (36r) |
| `eursto` | Storehouse | 10000 | 9 | 3.4m g (2.4m r) | 1.7m g (1.2m r) | 41g (29r) | 23g (16r) | 23g (16r) |
| `eurswa` | Wall | 50000 | 4 | 16.9m g (12.1m r) | 8.5m g (6.0m r) | 4.2m g (3.0m r) | 4.2m g (3.0m r) | 4.2m g (3.0m r) |
| `eurtow` | Tower | 20000 | 10 | 6.8m g (4.8m r) | 3.4m g (2.4m r) | 1.4m g (1.0m r) | 41g (29r) | 41g (29r) |
| `ukrwga` | Gate | 1500 | 13 | 30g (22r) | 15g (11r) | 6g (4r) | 3g (2r) | 2g (2r) |
| `ukrwwa` | Palisade | 1500 | 4 | 30g (22r) | 15g (11r) | 8g (5r) | 8g (5r) | 8g (5r) |

<a id="eng--england-англия"></a>
<a id="англия-eng"></a>
## England (`eng`)
<a id="постройка-с-нуля-4"></a>
### Building from scratch

| sid | name | buildtime_g | slot_cap | 1 is building. | 2 is building. | 5 is building. | 10 is building. | Max. builds. |
|---|---|---|---|---|---|---|---|---|
| `engaca` | Academy | 625g | 23 | 11.8m g (8.4m r) | 5.9m g (4.2m r) | 2.4m g (1.7m r) | 1.2m g (0.8m r) | 31g (22r) |
| `engart` | Artillery Depot | 246g | 22 | 4.6m g (3.3m r) | 2.3m g (1.7m r) | 56g (40r) | 28g (20r) | 13g (9r) |
| `engba2` | Barracks, 18th century | 5625g | 23 | 105.9m g (75.7m r) | 53.0m g (37.8m r) | 21.2m g (15.1m r) | 10.6m g (7.6m r) | 4.6m g (3.3m r) |
| `engbar` | Barracks, 17th century | 94g | 22 | 1.8m g (1.3m r) | 53g (38r) | 21g (15r) | 11g (8r) | 5g (3r) |
| `engbla` | Blacksmith | 94g | 16 | 1.8m g (1.3m r) | 53g (38r) | 21g (15r) | 11g (8r) | 7g (5r) |
| `engcen` | Town Hall | 156g | 23 | 2.9m g (2.1m r) | 1.5m g (1.1m r) | 35g (25r) | 18g (13r) | 8g (5r) |
| `engdip` | Diplomatic Center | 312g | 16 | 5.9m g (4.2m r) | 2.9m g (2.1m r) | 1.2m g (0.8m r) | 35g (25r) | 22g (16r) |
| `enghou` | Housing | 31g | 15 | 35g (25r) | 18g (13r) | 7g (5r) | 4g (3r) | 2g (2r) |
| `engsta` | Stable | 375g | 22 | 7.1m g (5.0m r) | 3.5m g (2.5m r) | 1.4m g (1.0m r) | 42g (30r) | 19g (14r) |
| `engtem` | Cathedral | 156g | 24 | 2.9m g (2.1m r) | 1.5m g (1.1m r) | 35g (25r) | 18g (13r) | 7g (5r) |
| `eurcoa` | Mine | 94g | 16 | 1.8m g (1.3m r) | 53g (38r) | 21g (15r) | 11g (8r) | 7g (5r) |
| `eurgol` | Mine | 94g | 16 | 1.8m g (1.3m r) | 53g (38r) | 21g (15r) | 11g (8r) | 7g (5r) |
| `euriro` | Mine | 94g | 16 | 1.8m g (1.3m r) | 53g (38r) | 21g (15r) | 11g (8r) | 7g (5r) |
| `eurmar` | Market | 234g | 25 | 4.4m g (3.2m r) | 2.2m g (1.6m r) | 53g (38r) | 26g (19r) | 11g (8r) |
| `eurmil` | Mill | 94g | 10 | 1.8m g (1.3m r) | 53g (38r) | 21g (15r) | 11g (8r) | 11g (8r) |
| `eurpor` | Shipyard | 1562g | 30 | 29.4m g (21.0m r) | 14.7m g (10.5m r) | 5.9m g (4.2m r) | 2.9m g (2.1m r) | 59g (42r) |
| `eursga` | Gate | 90g | 13 | 1.7m g (1.2m r) | 51g (36r) | 20g (15r) | 10g (7r) | 8g (6r) |
| `eursto` | Storehouse | 31g | 9 | 35g (25r) | 18g (13r) | 7g (5r) | 4g (3r) | 4g (3r) |
| `eurswa` | Wall | 90g | 4 | 1.7m g (1.2m r) | 51g (36r) | 25g (18r) | 25g (18r) | 25g (18r) |
| `eurtow` | Tower | 1230g | 10 | 23.2m g (16.6m r) | 11.6m g (8.3m r) | 4.6m g (3.3m r) | 2.3m g (1.7m r) | 2.3m g (1.7m r) |
| `ukrwga` | Gate | 6g | 13 | 6g (5r) | 3g (2r) | 1g (1r) | 1g (0r) | 0g (0r) |
| `ukrwwa` | Palisade | 6g | 4 | 6g (5r) | 3g (2r) | 2g (1r) | 2g (1r) | 2g (1r) |

<a id="полный-ремонт-0--max-hp-3"></a>
<a id="полный-ремонт-4"></a>
### Full repair (0 → max HP)

| sid | name | maxhp | slot_cap | 1 is building. | 2 is building. | 5 is building. | 10 is building. | Max. builds. |
|---|---|---|---|---|---|---|---|---|
| `engaca` | Academy | 63000 | 23 | 21.3m g (15.2m r) | 10.7m g (7.6m r) | 4.3m g (3.0m r) | 2.1m g (1.5m r) | 56g (40r) |
| `engart` | Artillery Depot | 40000 | 22 | 13.5m g (9.7m r) | 6.8m g (4.8m r) | 2.7m g (1.9m r) | 1.4m g (1.0m r) | 37g (26r) |
| `engba2` | Barracks, 18th century | 55000 | 23 | 18.6m g (13.3m r) | 9.3m g (6.6m r) | 3.7m g (2.7m r) | 1.9m g (1.3m r) | 49g (35r) |
| `engbar` | Barracks, 17th century | 40000 | 22 | 13.5m g (9.7m r) | 6.8m g (4.8m r) | 2.7m g (1.9m r) | 1.4m g (1.0m r) | 37g (26r) |
| `engbla` | Blacksmith | 5500 | 16 | 1.9m g (1.3m r) | 56g (40r) | 22g (16r) | 11g (8r) | 7g (5r) |
| `engcen` | Town Hall | 4030 | 23 | 1.4m g (1.0m r) | 41g (29r) | 16g (12r) | 8g (6r) | 4g (3r) |
| `engdip` | Diplomatic Center | 4500 | 16 | 1.5m g (1.1m r) | 46g (33r) | 18g (13r) | 9g (7r) | 6g (4r) |
| `enghou` | Housing | 5000 | 15 | 1.7m g (1.2m r) | 51g (36r) | 20g (15r) | 10g (7r) | 7g (5r) |
| `engsta` | Stable | 25000 | 22 | 8.5m g (6.0m r) | 4.2m g (3.0m r) | 1.7m g (1.2m r) | 51g (36r) | 23g (16r) |
| `engtem` | Cathedral | 4200 | 24 | 1.4m g (1.0m r) | 43g (30r) | 17g (12r) | 9g (6r) | 4g (3r) |
| `eurcoa` | Mine | 2500 | 16 | 51g (36r) | 25g (18r) | 10g (7r) | 5g (4r) | 3g (2r) |
| `eurgol` | Mine | 2500 | 16 | 51g (36r) | 25g (18r) | 10g (7r) | 5g (4r) | 3g (2r) |
| `euriro` | Mine | 2500 | 16 | 51g (36r) | 25g (18r) | 10g (7r) | 5g (4r) | 3g (2r) |
| `eurmar` | Market | 4000 | 25 | 1.4m g (1.0m r) | 41g (29r) | 16g (12r) | 8g (6r) | 3g (2r) |
| `eurmil` | Mill | 20000 | 10 | 6.8m g (4.8m r) | 3.4m g (2.4m r) | 1.4m g (1.0m r) | 41g (29r) | 41g (29r) |
| `eurpor` | Shipyard | 50000 | 30 | 16.9m g (12.1m r) | 8.5m g (6.0m r) | 3.4m g (2.4m r) | 1.7m g (1.2m r) | 34g (24r) |
| `eursga` | Gate | 32000 | 13 | 10.8m g (7.7m r) | 5.4m g (3.9m r) | 2.2m g (1.5m r) | 1.1m g (0.8m r) | 50g (36r) |
| `eursto` | Storehouse | 10000 | 9 | 3.4m g (2.4m r) | 1.7m g (1.2m r) | 41g (29r) | 23g (16r) | 23g (16r) |
| `eurswa` | Wall | 50000 | 4 | 16.9m g (12.1m r) | 8.5m g (6.0m r) | 4.2m g (3.0m r) | 4.2m g (3.0m r) | 4.2m g (3.0m r) |
| `eurtow` | Tower | 20000 | 10 | 6.8m g (4.8m r) | 3.4m g (2.4m r) | 1.4m g (1.0m r) | 41g (29r) | 41g (29r) |
| `ukrwga` | Gate | 1500 | 13 | 30g (22r) | 15g (11r) | 6g (4r) | 3g (2r) | 2g (2r) |
| `ukrwwa` | Palisade | 1500 | 4 | 30g (22r) | 15g (11r) | 8g (5r) | 8g (5r) | 8g (5r) |

<a id="fra--france-франция"></a>
<a id="франция-fra"></a>
## France (`fra`)
<a id="постройка-с-нуля-5"></a>
### Building from scratch

| sid | name | buildtime_g | slot_cap | 1 is building. | 2 is building. | 5 is building. | 10 is building. | Max. builds. |
|---|---|---|---|---|---|---|---|---|
| `eurcoa` | Mine | 94g | 16 | 1.8m g (1.3m r) | 53g (38r) | 21g (15r) | 11g (8r) | 7g (5r) |
| `eurgol` | Mine | 94g | 16 | 1.8m g (1.3m r) | 53g (38r) | 21g (15r) | 11g (8r) | 7g (5r) |
| `euriro` | Mine | 94g | 16 | 1.8m g (1.3m r) | 53g (38r) | 21g (15r) | 11g (8r) | 7g (5r) |
| `eurmar` | Market | 234g | 25 | 4.4m g (3.2m r) | 2.2m g (1.6m r) | 53g (38r) | 26g (19r) | 11g (8r) |
| `eurmil` | Mill | 94g | 10 | 1.8m g (1.3m r) | 53g (38r) | 21g (15r) | 11g (8r) | 11g (8r) |
| `eurpor` | Shipyard | 1562g | 30 | 29.4m g (21.0m r) | 14.7m g (10.5m r) | 5.9m g (4.2m r) | 2.9m g (2.1m r) | 59g (42r) |
| `eursga` | Gate | 90g | 13 | 1.7m g (1.2m r) | 51g (36r) | 20g (15r) | 10g (7r) | 8g (6r) |
| `eursto` | Storehouse | 31g | 9 | 35g (25r) | 18g (13r) | 7g (5r) | 4g (3r) | 4g (3r) |
| `eurswa` | Wall | 90g | 4 | 1.7m g (1.2m r) | 51g (36r) | 25g (18r) | 25g (18r) | 25g (18r) |
| `eurtow` | Tower | 1230g | 10 | 23.2m g (16.6m r) | 11.6m g (8.3m r) | 4.6m g (3.3m r) | 2.3m g (1.7m r) | 2.3m g (1.7m r) |
| `fraaca` | Academy | 625g | 24 | 11.8m g (8.4m r) | 5.9m g (4.2m r) | 2.4m g (1.7m r) | 1.2m g (0.8m r) | 29g (21r) |
| `fraart` | Artillery Depot | 246g | 24 | 4.6m g (3.3m r) | 2.3m g (1.7m r) | 56g (40r) | 28g (20r) | 12g (8r) |
| `fraba2` | Barracks, 18th century | 5625g | 29 | 105.9m g (75.7m r) | 53.0m g (37.8m r) | 21.2m g (15.1m r) | 10.6m g (7.6m r) | 3.7m g (2.6m r) |
| `frabar` | Barracks, 17th century | 94g | 16 | 1.8m g (1.3m r) | 53g (38r) | 21g (15r) | 11g (8r) | 7g (5r) |
| `frabla` | Blacksmith | 94g | 13 | 1.8m g (1.3m r) | 53g (38r) | 21g (15r) | 11g (8r) | 8g (6r) |
| `fracen` | Town Hall | 156g | 27 | 2.9m g (2.1m r) | 1.5m g (1.1m r) | 35g (25r) | 18g (13r) | 7g (5r) |
| `fradip` | Diplomatic Center | 312g | 18 | 5.9m g (4.2m r) | 2.9m g (2.1m r) | 1.2m g (0.8m r) | 35g (25r) | 20g (14r) |
| `frahou` | Housing | 31g | 10 | 35g (25r) | 18g (13r) | 7g (5r) | 4g (3r) | 4g (3r) |
| `frasta` | Stable | 625g | 22 | 11.8m g (8.4m r) | 5.9m g (4.2m r) | 2.4m g (1.7m r) | 1.2m g (0.8m r) | 32g (23r) |
| `fratem` | Cathedral | 312g | 30 | 5.9m g (4.2m r) | 2.9m g (2.1m r) | 1.2m g (0.8m r) | 35g (25r) | 12g (8r) |
| `ukrwga` | Gate | 6g | 13 | 6g (5r) | 3g (2r) | 1g (1r) | 1g (0r) | 0g (0r) |
| `ukrwwa` | Palisade | 6g | 4 | 6g (5r) | 3g (2r) | 2g (1r) | 2g (1r) | 2g (1r) |

<a id="полный-ремонт-0--max-hp-4"></a>
<a id="полный-ремонт-5"></a>
### Full repair (0 → max HP)

| sid | name | maxhp | slot_cap | 1 is building. | 2 is building. | 5 is building. | 10 is building. | Max. builds. |
|---|---|---|---|---|---|---|---|---|
| `eurcoa` | Mine | 2500 | 16 | 51g (36r) | 25g (18r) | 10g (7r) | 5g (4r) | 3g (2r) |
| `eurgol` | Mine | 2500 | 16 | 51g (36r) | 25g (18r) | 10g (7r) | 5g (4r) | 3g (2r) |
| `euriro` | Mine | 2500 | 16 | 51g (36r) | 25g (18r) | 10g (7r) | 5g (4r) | 3g (2r) |
| `eurmar` | Market | 4000 | 25 | 1.4m g (1.0m r) | 41g (29r) | 16g (12r) | 8g (6r) | 3g (2r) |
| `eurmil` | Mill | 20000 | 10 | 6.8m g (4.8m r) | 3.4m g (2.4m r) | 1.4m g (1.0m r) | 41g (29r) | 41g (29r) |
| `eurpor` | Shipyard | 50000 | 30 | 16.9m g (12.1m r) | 8.5m g (6.0m r) | 3.4m g (2.4m r) | 1.7m g (1.2m r) | 34g (24r) |
| `eursga` | Gate | 32000 | 13 | 10.8m g (7.7m r) | 5.4m g (3.9m r) | 2.2m g (1.5m r) | 1.1m g (0.8m r) | 50g (36r) |
| `eursto` | Storehouse | 10000 | 9 | 3.4m g (2.4m r) | 1.7m g (1.2m r) | 41g (29r) | 23g (16r) | 23g (16r) |
| `eurswa` | Wall | 50000 | 4 | 16.9m g (12.1m r) | 8.5m g (6.0m r) | 4.2m g (3.0m r) | 4.2m g (3.0m r) | 4.2m g (3.0m r) |
| `eurtow` | Tower | 20000 | 10 | 6.8m g (4.8m r) | 3.4m g (2.4m r) | 1.4m g (1.0m r) | 41g (29r) | 41g (29r) |
| `fraaca` | Academy | 63000 | 24 | 21.3m g (15.2m r) | 10.7m g (7.6m r) | 4.3m g (3.0m r) | 2.1m g (1.5m r) | 53g (38r) |
| `fraart` | Artillery Depot | 40000 | 24 | 13.5m g (9.7m r) | 6.8m g (4.8m r) | 2.7m g (1.9m r) | 1.4m g (1.0m r) | 34g (24r) |
| `fraba2` | Barracks, 18th century | 55000 | 29 | 18.6m g (13.3m r) | 9.3m g (6.6m r) | 3.7m g (2.7m r) | 1.9m g (1.3m r) | 39g (28r) |
| `frabar` | Barracks, 17th century | 40000 | 16 | 13.5m g (9.7m r) | 6.8m g (4.8m r) | 2.7m g (1.9m r) | 1.4m g (1.0m r) | 51g (36r) |
| `frabla` | Blacksmith | 5500 | 13 | 1.9m g (1.3m r) | 56g (40r) | 22g (16r) | 11g (8r) | 9g (6r) |
| `fracen` | Town Hall | 4500 | 27 | 1.5m g (1.1m r) | 46g (33r) | 18g (13r) | 9g (7r) | 3g (2r) |
| `fradip` | Diplomatic Center | 4500 | 18 | 1.5m g (1.1m r) | 46g (33r) | 18g (13r) | 9g (7r) | 5g (4r) |
| `frahou` | Housing | 4000 | 10 | 1.4m g (1.0m r) | 41g (29r) | 16g (12r) | 8g (6r) | 8g (6r) |
| `frasta` | Stable | 20000 | 22 | 6.8m g (4.8m r) | 3.4m g (2.4m r) | 1.4m g (1.0m r) | 41g (29r) | 18g (13r) |
| `fratem` | Cathedral | 6000 | 30 | 2.0m g (1.5m r) | 1.0m g (0.7m r) | 24g (17r) | 12g (9r) | 4g (3r) |
| `ukrwga` | Gate | 1500 | 13 | 30g (22r) | 15g (11r) | 6g (4r) | 3g (2r) | 2g (2r) |
| `ukrwwa` | Palisade | 1500 | 4 | 30g (22r) | 15g (11r) | 8g (5r) | 8g (5r) | 8g (5r) |

<a id="hun--hungary-венгрия"></a>
<a id="венгрия-hun"></a>
## Hungary (`hun`)
<a id="постройка-с-нуля-6"></a>
### Building from scratch

| sid | name | buildtime_g | slot_cap | 1 is building. | 2 is building. | 5 is building. | 10 is building. | Max. builds. |
|---|---|---|---|---|---|---|---|---|
| `eurcoa` | Mine | 94g | 16 | 1.8m g (1.3m r) | 53g (38r) | 21g (15r) | 11g (8r) | 7g (5r) |
| `eurgol` | Mine | 94g | 16 | 1.8m g (1.3m r) | 53g (38r) | 21g (15r) | 11g (8r) | 7g (5r) |
| `euriro` | Mine | 94g | 16 | 1.8m g (1.3m r) | 53g (38r) | 21g (15r) | 11g (8r) | 7g (5r) |
| `eurmar` | Market | 234g | 25 | 4.4m g (3.2m r) | 2.2m g (1.6m r) | 53g (38r) | 26g (19r) | 11g (8r) |
| `eurmil` | Mill | 94g | 10 | 1.8m g (1.3m r) | 53g (38r) | 21g (15r) | 11g (8r) | 11g (8r) |
| `eurpor` | Shipyard | 1562g | 30 | 29.4m g (21.0m r) | 14.7m g (10.5m r) | 5.9m g (4.2m r) | 2.9m g (2.1m r) | 59g (42r) |
| `eursga` | Gate | 90g | 13 | 1.7m g (1.2m r) | 51g (36r) | 20g (15r) | 10g (7r) | 8g (6r) |
| `eursto` | Storehouse | 31g | 9 | 35g (25r) | 18g (13r) | 7g (5r) | 4g (3r) | 4g (3r) |
| `eurswa` | Wall | 90g | 4 | 1.7m g (1.2m r) | 51g (36r) | 25g (18r) | 25g (18r) | 25g (18r) |
| `eurtow` | Tower | 1230g | 10 | 23.2m g (16.6m r) | 11.6m g (8.3m r) | 4.6m g (3.3m r) | 2.3m g (1.7m r) | 2.3m g (1.7m r) |
| `hunaca` | Academy | 625g | 19 | 11.8m g (8.4m r) | 5.9m g (4.2m r) | 2.4m g (1.7m r) | 1.2m g (0.8m r) | 37g (27r) |
| `hunart` | Artillery Depot | 246g | 18 | 4.6m g (3.3m r) | 2.3m g (1.7m r) | 56g (40r) | 28g (20r) | 15g (11r) |
| `hunba2` | Barracks, 18th century | 5625g | 26 | 105.9m g (75.7m r) | 53.0m g (37.8m r) | 21.2m g (15.1m r) | 10.6m g (7.6m r) | 4.1m g (2.9m r) |
| `hunbar` | Barracks, 17th century | 94g | 22 | 1.8m g (1.3m r) | 53g (38r) | 21g (15r) | 11g (8r) | 5g (3r) |
| `hunbla` | Blacksmith | 94g | 13 | 1.8m g (1.3m r) | 53g (38r) | 21g (15r) | 11g (8r) | 8g (6r) |
| `huncen` | Town Hall | 156g | 22 | 2.9m g (2.1m r) | 1.5m g (1.1m r) | 35g (25r) | 18g (13r) | 8g (6r) |
| `hundip` | Diplomatic Center | 312g | 18 | 5.9m g (4.2m r) | 2.9m g (2.1m r) | 1.2m g (0.8m r) | 35g (25r) | 20g (14r) |
| `hunhou` | Housing | 31g | 14 | 35g (25r) | 18g (13r) | 7g (5r) | 4g (3r) | 3g (2r) |
| `hunsta` | Stable | 625g | 19 | 11.8m g (8.4m r) | 5.9m g (4.2m r) | 2.4m g (1.7m r) | 1.2m g (0.8m r) | 37g (27r) |
| `huntem` | Cathedral | 156g | 28 | 2.9m g (2.1m r) | 1.5m g (1.1m r) | 35g (25r) | 18g (13r) | 6g (5r) |
| `ukrwga` | Gate | 6g | 13 | 6g (5r) | 3g (2r) | 1g (1r) | 1g (0r) | 0g (0r) |
| `ukrwwa` | Palisade | 6g | 4 | 6g (5r) | 3g (2r) | 2g (1r) | 2g (1r) | 2g (1r) |

<a id="полный-ремонт-0--max-hp-5"></a>
<a id="полный-ремонт-6"></a>
### Full repair (0 → max HP)

| sid | name | maxhp | slot_cap | 1 is building. | 2 is building. | 5 is building. | 10 is building. | Max. builds. |
|---|---|---|---|---|---|---|---|---|
| `eurcoa` | Mine | 2500 | 16 | 51g (36r) | 25g (18r) | 10g (7r) | 5g (4r) | 3g (2r) |
| `eurgol` | Mine | 2500 | 16 | 51g (36r) | 25g (18r) | 10g (7r) | 5g (4r) | 3g (2r) |
| `euriro` | Mine | 2500 | 16 | 51g (36r) | 25g (18r) | 10g (7r) | 5g (4r) | 3g (2r) |
| `eurmar` | Market | 4000 | 25 | 1.4m g (1.0m r) | 41g (29r) | 16g (12r) | 8g (6r) | 3g (2r) |
| `eurmil` | Mill | 20000 | 10 | 6.8m g (4.8m r) | 3.4m g (2.4m r) | 1.4m g (1.0m r) | 41g (29r) | 41g (29r) |
| `eurpor` | Shipyard | 50000 | 30 | 16.9m g (12.1m r) | 8.5m g (6.0m r) | 3.4m g (2.4m r) | 1.7m g (1.2m r) | 34g (24r) |
| `eursga` | Gate | 32000 | 13 | 10.8m g (7.7m r) | 5.4m g (3.9m r) | 2.2m g (1.5m r) | 1.1m g (0.8m r) | 50g (36r) |
| `eursto` | Storehouse | 10000 | 9 | 3.4m g (2.4m r) | 1.7m g (1.2m r) | 41g (29r) | 23g (16r) | 23g (16r) |
| `eurswa` | Wall | 50000 | 4 | 16.9m g (12.1m r) | 8.5m g (6.0m r) | 4.2m g (3.0m r) | 4.2m g (3.0m r) | 4.2m g (3.0m r) |
| `eurtow` | Tower | 20000 | 10 | 6.8m g (4.8m r) | 3.4m g (2.4m r) | 1.4m g (1.0m r) | 41g (29r) | 41g (29r) |
| `hunaca` | Academy | 63000 | 19 | 21.3m g (15.2m r) | 10.7m g (7.6m r) | 4.3m g (3.0m r) | 2.1m g (1.5m r) | 1.1m g (0.8m r) |
| `hunart` | Artillery Depot | 40000 | 18 | 13.5m g (9.7m r) | 6.8m g (4.8m r) | 2.7m g (1.9m r) | 1.4m g (1.0m r) | 45g (32r) |
| `hunba2` | Barracks, 18th century | 55000 | 26 | 18.6m g (13.3m r) | 9.3m g (6.6m r) | 3.7m g (2.7m r) | 1.9m g (1.3m r) | 43g (31r) |
| `hunbar` | Barracks, 17th century | 40000 | 22 | 13.5m g (9.7m r) | 6.8m g (4.8m r) | 2.7m g (1.9m r) | 1.4m g (1.0m r) | 37g (26r) |
| `hunbla` | Blacksmith | 5500 | 13 | 1.9m g (1.3m r) | 56g (40r) | 22g (16r) | 11g (8r) | 9g (6r) |
| `huncen` | Town Hall | 4000 | 22 | 1.4m g (1.0m r) | 41g (29r) | 16g (12r) | 8g (6r) | 4g (3r) |
| `hundip` | Diplomatic Center | 4500 | 18 | 1.5m g (1.1m r) | 46g (33r) | 18g (13r) | 9g (7r) | 5g (4r) |
| `hunhou` | Housing | 4000 | 14 | 1.4m g (1.0m r) | 41g (29r) | 16g (12r) | 8g (6r) | 6g (4r) |
| `hunsta` | Stable | 20000 | 19 | 6.8m g (4.8m r) | 3.4m g (2.4m r) | 1.4m g (1.0m r) | 41g (29r) | 21g (15r) |
| `huntem` | Cathedral | 4200 | 28 | 1.4m g (1.0m r) | 43g (30r) | 17g (12r) | 9g (6r) | 3g (2r) |
| `ukrwga` | Gate | 1500 | 13 | 30g (22r) | 15g (11r) | 6g (4r) | 3g (2r) | 2g (2r) |
| `ukrwwa` | Palisade | 1500 | 4 | 30g (22r) | 15g (11r) | 8g (5r) | 8g (5r) | 8g (5r) |

<a id="net--netherlands-нидерланды"></a>
<a id="нидерланды-net"></a>
## Netherlands (`net`)
<a id="постройка-с-нуля-7"></a>
### Building from scratch

| sid | name | buildtime_g | slot_cap | 1 is building. | 2 is building. | 5 is building. | 10 is building. | Max. builds. |
|---|---|---|---|---|---|---|---|---|
| `eurcoa` | Mine | 94g | 16 | 1.8m g (1.3m r) | 53g (38r) | 21g (15r) | 11g (8r) | 7g (5r) |
| `eurgol` | Mine | 94g | 16 | 1.8m g (1.3m r) | 53g (38r) | 21g (15r) | 11g (8r) | 7g (5r) |
| `euriro` | Mine | 94g | 16 | 1.8m g (1.3m r) | 53g (38r) | 21g (15r) | 11g (8r) | 7g (5r) |
| `eurmar` | Market | 234g | 25 | 4.4m g (3.2m r) | 2.2m g (1.6m r) | 53g (38r) | 26g (19r) | 11g (8r) |
| `eurmil` | Mill | 94g | 10 | 1.8m g (1.3m r) | 53g (38r) | 21g (15r) | 11g (8r) | 11g (8r) |
| `eurpor` | Shipyard | 1562g | 30 | 29.4m g (21.0m r) | 14.7m g (10.5m r) | 5.9m g (4.2m r) | 2.9m g (2.1m r) | 59g (42r) |
| `eursga` | Gate | 90g | 13 | 1.7m g (1.2m r) | 51g (36r) | 20g (15r) | 10g (7r) | 8g (6r) |
| `eursto` | Storehouse | 31g | 9 | 35g (25r) | 18g (13r) | 7g (5r) | 4g (3r) | 4g (3r) |
| `eurswa` | Wall | 90g | 4 | 1.7m g (1.2m r) | 51g (36r) | 25g (18r) | 25g (18r) | 25g (18r) |
| `eurtow` | Tower | 1230g | 10 | 23.2m g (16.6m r) | 11.6m g (8.3m r) | 4.6m g (3.3m r) | 2.3m g (1.7m r) | 2.3m g (1.7m r) |
| `netaca` | Academy | 625g | 18 | 11.8m g (8.4m r) | 5.9m g (4.2m r) | 2.4m g (1.7m r) | 1.2m g (0.8m r) | 39g (28r) |
| `netart` | Artillery Depot | 246g | 20 | 4.6m g (3.3m r) | 2.3m g (1.7m r) | 56g (40r) | 28g (20r) | 14g (10r) |
| `netba2` | Barracks, 18th century | 5625g | 21 | 105.9m g (75.7m r) | 53.0m g (37.8m r) | 21.2m g (15.1m r) | 10.6m g (7.6m r) | 5.0m g (3.6m r) |
| `netbar` | Barracks, 17th century | 94g | 20 | 1.8m g (1.3m r) | 53g (38r) | 21g (15r) | 11g (8r) | 5g (4r) |
| `netbla` | Blacksmith | 94g | 14 | 1.8m g (1.3m r) | 53g (38r) | 21g (15r) | 11g (8r) | 8g (5r) |
| `netcen` | Town Hall | 156g | 19 | 2.9m g (2.1m r) | 1.5m g (1.1m r) | 35g (25r) | 18g (13r) | 9g (7r) |
| `netdip` | Diplomatic Center | 312g | 18 | 5.9m g (4.2m r) | 2.9m g (2.1m r) | 1.2m g (0.8m r) | 35g (25r) | 20g (14r) |
| `nethou` | Housing | 31g | 13 | 35g (25r) | 18g (13r) | 7g (5r) | 4g (3r) | 3g (2r) |
| `netsta` | Stable | 625g | 18 | 11.8m g (8.4m r) | 5.9m g (4.2m r) | 2.4m g (1.7m r) | 1.2m g (0.8m r) | 39g (28r) |
| `nettem` | Cathedral | 156g | 21 | 2.9m g (2.1m r) | 1.5m g (1.1m r) | 35g (25r) | 18g (13r) | 8g (6r) |
| `ukrwga` | Gate | 6g | 13 | 6g (5r) | 3g (2r) | 1g (1r) | 1g (0r) | 0g (0r) |
| `ukrwwa` | Palisade | 6g | 4 | 6g (5r) | 3g (2r) | 2g (1r) | 2g (1r) | 2g (1r) |

<a id="полный-ремонт-0--max-hp-6"></a>
<a id="полный-ремонт-7"></a>
### Full repair (0 → max HP)

| sid | name | maxhp | slot_cap | 1 is building. | 2 is building. | 5 is building. | 10 is building. | Max. builds. |
|---|---|---|---|---|---|---|---|---|
| `eurcoa` | Mine | 2500 | 16 | 51g (36r) | 25g (18r) | 10g (7r) | 5g (4r) | 3g (2r) |
| `eurgol` | Mine | 2500 | 16 | 51g (36r) | 25g (18r) | 10g (7r) | 5g (4r) | 3g (2r) |
| `euriro` | Mine | 2500 | 16 | 51g (36r) | 25g (18r) | 10g (7r) | 5g (4r) | 3g (2r) |
| `eurmar` | Market | 4000 | 25 | 1.4m g (1.0m r) | 41g (29r) | 16g (12r) | 8g (6r) | 3g (2r) |
| `eurmil` | Mill | 20000 | 10 | 6.8m g (4.8m r) | 3.4m g (2.4m r) | 1.4m g (1.0m r) | 41g (29r) | 41g (29r) |
| `eurpor` | Shipyard | 50000 | 30 | 16.9m g (12.1m r) | 8.5m g (6.0m r) | 3.4m g (2.4m r) | 1.7m g (1.2m r) | 34g (24r) |
| `eursga` | Gate | 32000 | 13 | 10.8m g (7.7m r) | 5.4m g (3.9m r) | 2.2m g (1.5m r) | 1.1m g (0.8m r) | 50g (36r) |
| `eursto` | Storehouse | 10000 | 9 | 3.4m g (2.4m r) | 1.7m g (1.2m r) | 41g (29r) | 23g (16r) | 23g (16r) |
| `eurswa` | Wall | 50000 | 4 | 16.9m g (12.1m r) | 8.5m g (6.0m r) | 4.2m g (3.0m r) | 4.2m g (3.0m r) | 4.2m g (3.0m r) |
| `eurtow` | Tower | 20000 | 10 | 6.8m g (4.8m r) | 3.4m g (2.4m r) | 1.4m g (1.0m r) | 41g (29r) | 41g (29r) |
| `netaca` | Academy | 63000 | 18 | 21.3m g (15.2m r) | 10.7m g (7.6m r) | 4.3m g (3.0m r) | 2.1m g (1.5m r) | 1.2m g (0.8m r) |
| `netart` | Artillery Depot | 40000 | 20 | 13.5m g (9.7m r) | 6.8m g (4.8m r) | 2.7m g (1.9m r) | 1.4m g (1.0m r) | 41g (29r) |
| `netba2` | Barracks, 18th century | 55000 | 21 | 18.6m g (13.3m r) | 9.3m g (6.6m r) | 3.7m g (2.7m r) | 1.9m g (1.3m r) | 53g (38r) |
| `netbar` | Barracks, 17th century | 40000 | 20 | 13.5m g (9.7m r) | 6.8m g (4.8m r) | 2.7m g (1.9m r) | 1.4m g (1.0m r) | 41g (29r) |
| `netbla` | Blacksmith | 5500 | 14 | 1.9m g (1.3m r) | 56g (40r) | 22g (16r) | 11g (8r) | 8g (6r) |
| `netcen` | Town Hall | 4950 | 19 | 1.7m g (1.2m r) | 50g (36r) | 20g (14r) | 10g (7r) | 5g (4r) |
| `netdip` | Diplomatic Center | 4500 | 18 | 1.5m g (1.1m r) | 46g (33r) | 18g (13r) | 9g (7r) | 5g (4r) |
| `nethou` | Housing | 4500 | 13 | 1.5m g (1.1m r) | 46g (33r) | 18g (13r) | 9g (7r) | 7g (5r) |
| `netsta` | Stable | 20000 | 18 | 6.8m g (4.8m r) | 3.4m g (2.4m r) | 1.4m g (1.0m r) | 41g (29r) | 23g (16r) |
| `nettem` | Cathedral | 4200 | 21 | 1.4m g (1.0m r) | 43g (30r) | 17g (12r) | 9g (6r) | 4g (3r) |
| `ukrwga` | Gate | 1500 | 13 | 30g (22r) | 15g (11r) | 6g (4r) | 3g (2r) | 2g (2r) |
| `ukrwwa` | Palisade | 1500 | 4 | 30g (22r) | 15g (11r) | 8g (5r) | 8g (5r) | 8g (5r) |

<a id="pie--piedmont-пьемонт"></a>
<a id="пьемонт-pie"></a>
## Piedmont (`pie`)
<a id="постройка-с-нуля-8"></a>
### Building from scratch

| sid | name | buildtime_g | slot_cap | 1 is building. | 2 is building. | 5 is building. | 10 is building. | Max. builds. |
|---|---|---|---|---|---|---|---|---|
| `eurcoa` | Mine | 94g | 16 | 1.8m g (1.3m r) | 53g (38r) | 21g (15r) | 11g (8r) | 7g (5r) |
| `eurgol` | Mine | 94g | 16 | 1.8m g (1.3m r) | 53g (38r) | 21g (15r) | 11g (8r) | 7g (5r) |
| `euriro` | Mine | 94g | 16 | 1.8m g (1.3m r) | 53g (38r) | 21g (15r) | 11g (8r) | 7g (5r) |
| `eurmar` | Market | 234g | 25 | 4.4m g (3.2m r) | 2.2m g (1.6m r) | 53g (38r) | 26g (19r) | 11g (8r) |
| `eurmil` | Mill | 94g | 10 | 1.8m g (1.3m r) | 53g (38r) | 21g (15r) | 11g (8r) | 11g (8r) |
| `eurpor` | Shipyard | 1562g | 30 | 29.4m g (21.0m r) | 14.7m g (10.5m r) | 5.9m g (4.2m r) | 2.9m g (2.1m r) | 59g (42r) |
| `eursga` | Gate | 90g | 13 | 1.7m g (1.2m r) | 51g (36r) | 20g (15r) | 10g (7r) | 8g (6r) |
| `eursto` | Storehouse | 31g | 9 | 35g (25r) | 18g (13r) | 7g (5r) | 4g (3r) | 4g (3r) |
| `eurswa` | Wall | 90g | 4 | 1.7m g (1.2m r) | 51g (36r) | 25g (18r) | 25g (18r) | 25g (18r) |
| `eurtow` | Tower | 1230g | 10 | 23.2m g (16.6m r) | 11.6m g (8.3m r) | 4.6m g (3.3m r) | 2.3m g (1.7m r) | 2.3m g (1.7m r) |
| `pieaca` | Academy | 625g | 22 | 11.8m g (8.4m r) | 5.9m g (4.2m r) | 2.4m g (1.7m r) | 1.2m g (0.8m r) | 32g (23r) |
| `pieart` | Artillery Depot | 246g | 19 | 4.6m g (3.3m r) | 2.3m g (1.7m r) | 56g (40r) | 28g (20r) | 15g (10r) |
| `pieba2` | Barracks, 18th century | 5625g | 22 | 105.9m g (75.7m r) | 53.0m g (37.8m r) | 21.2m g (15.1m r) | 10.6m g (7.6m r) | 4.8m g (3.4m r) |
| `piebar` | Barracks, 17th century | 94g | 24 | 1.8m g (1.3m r) | 53g (38r) | 21g (15r) | 11g (8r) | 4g (3r) |
| `piebla` | Blacksmith | 94g | 16 | 1.8m g (1.3m r) | 53g (38r) | 21g (15r) | 11g (8r) | 7g (5r) |
| `piecen` | Town Hall | 156g | 24 | 2.9m g (2.1m r) | 1.5m g (1.1m r) | 35g (25r) | 18g (13r) | 7g (5r) |
| `piedip` | Diplomatic Center | 312g | 16 | 5.9m g (4.2m r) | 2.9m g (2.1m r) | 1.2m g (0.8m r) | 35g (25r) | 22g (16r) |
| `piehou` | Housing | 31g | 13 | 35g (25r) | 18g (13r) | 7g (5r) | 4g (3r) | 3g (2r) |
| `piesta` | Stable | 625g | 24 | 11.8m g (8.4m r) | 5.9m g (4.2m r) | 2.4m g (1.7m r) | 1.2m g (0.8m r) | 29g (21r) |
| `pietem` | Cathedral | 156g | 20 | 2.9m g (2.1m r) | 1.5m g (1.1m r) | 35g (25r) | 18g (13r) | 9g (6r) |
| `ukrwga` | Gate | 6g | 13 | 6g (5r) | 3g (2r) | 1g (1r) | 1g (0r) | 0g (0r) |
| `ukrwwa` | Palisade | 6g | 4 | 6g (5r) | 3g (2r) | 2g (1r) | 2g (1r) | 2g (1r) |

<a id="полный-ремонт-0--max-hp-7"></a>
<a id="полный-ремонт-8"></a>
### Full repair (0 → max HP)

| sid | name | maxhp | slot_cap | 1 is building. | 2 is building. | 5 is building. | 10 is building. | Max. builds. |
|---|---|---|---|---|---|---|---|---|
| `eurcoa` | Mine | 2500 | 16 | 51g (36r) | 25g (18r) | 10g (7r) | 5g (4r) | 3g (2r) |
| `eurgol` | Mine | 2500 | 16 | 51g (36r) | 25g (18r) | 10g (7r) | 5g (4r) | 3g (2r) |
| `euriro` | Mine | 2500 | 16 | 51g (36r) | 25g (18r) | 10g (7r) | 5g (4r) | 3g (2r) |
| `eurmar` | Market | 4000 | 25 | 1.4m g (1.0m r) | 41g (29r) | 16g (12r) | 8g (6r) | 3g (2r) |
| `eurmil` | Mill | 20000 | 10 | 6.8m g (4.8m r) | 3.4m g (2.4m r) | 1.4m g (1.0m r) | 41g (29r) | 41g (29r) |
| `eurpor` | Shipyard | 50000 | 30 | 16.9m g (12.1m r) | 8.5m g (6.0m r) | 3.4m g (2.4m r) | 1.7m g (1.2m r) | 34g (24r) |
| `eursga` | Gate | 32000 | 13 | 10.8m g (7.7m r) | 5.4m g (3.9m r) | 2.2m g (1.5m r) | 1.1m g (0.8m r) | 50g (36r) |
| `eursto` | Storehouse | 10000 | 9 | 3.4m g (2.4m r) | 1.7m g (1.2m r) | 41g (29r) | 23g (16r) | 23g (16r) |
| `eurswa` | Wall | 50000 | 4 | 16.9m g (12.1m r) | 8.5m g (6.0m r) | 4.2m g (3.0m r) | 4.2m g (3.0m r) | 4.2m g (3.0m r) |
| `eurtow` | Tower | 20000 | 10 | 6.8m g (4.8m r) | 3.4m g (2.4m r) | 1.4m g (1.0m r) | 41g (29r) | 41g (29r) |
| `pieaca` | Academy | 63000 | 22 | 21.3m g (15.2m r) | 10.7m g (7.6m r) | 4.3m g (3.0m r) | 2.1m g (1.5m r) | 58g (42r) |
| `pieart` | Artillery Depot | 40000 | 19 | 13.5m g (9.7m r) | 6.8m g (4.8m r) | 2.7m g (1.9m r) | 1.4m g (1.0m r) | 43g (31r) |
| `pieba2` | Barracks, 18th century | 55000 | 22 | 18.6m g (13.3m r) | 9.3m g (6.6m r) | 3.7m g (2.7m r) | 1.9m g (1.3m r) | 51g (36r) |
| `piebar` | Barracks, 17th century | 40000 | 24 | 13.5m g (9.7m r) | 6.8m g (4.8m r) | 2.7m g (1.9m r) | 1.4m g (1.0m r) | 34g (24r) |
| `piebla` | Blacksmith | 5500 | 16 | 1.9m g (1.3m r) | 56g (40r) | 22g (16r) | 11g (8r) | 7g (5r) |
| `piecen` | Town Hall | 4000 | 24 | 1.4m g (1.0m r) | 41g (29r) | 16g (12r) | 8g (6r) | 3g (2r) |
| `piedip` | Diplomatic Center | 4500 | 16 | 1.5m g (1.1m r) | 46g (33r) | 18g (13r) | 9g (7r) | 6g (4r) |
| `piehou` | Housing | 4000 | 13 | 1.4m g (1.0m r) | 41g (29r) | 16g (12r) | 8g (6r) | 6g (4r) |
| `piesta` | Stable | 20000 | 24 | 6.8m g (4.8m r) | 3.4m g (2.4m r) | 1.4m g (1.0m r) | 41g (29r) | 17g (12r) |
| `pietem` | Cathedral | 4200 | 20 | 1.4m g (1.0m r) | 43g (30r) | 17g (12r) | 9g (6r) | 4g (3r) |
| `ukrwga` | Gate | 1500 | 13 | 30g (22r) | 15g (11r) | 6g (4r) | 3g (2r) | 2g (2r) |
| `ukrwwa` | Palisade | 1500 | 4 | 30g (22r) | 15g (11r) | 8g (5r) | 8g (5r) | 8g (5r) |

<a id="pol--poland-польша"></a>
<a id="польша-pol"></a>
## Poland (`pol`)
<a id="постройка-с-нуля-9"></a>
### Building from scratch

| sid | name | buildtime_g | slot_cap | 1 is building. | 2 is building. | 5 is building. | 10 is building. | Max. builds. |
|---|---|---|---|---|---|---|---|---|
| `eurcoa` | Mine | 94g | 16 | 1.8m g (1.3m r) | 53g (38r) | 21g (15r) | 11g (8r) | 7g (5r) |
| `eurgol` | Mine | 94g | 16 | 1.8m g (1.3m r) | 53g (38r) | 21g (15r) | 11g (8r) | 7g (5r) |
| `euriro` | Mine | 94g | 16 | 1.8m g (1.3m r) | 53g (38r) | 21g (15r) | 11g (8r) | 7g (5r) |
| `eurmar` | Market | 234g | 25 | 4.4m g (3.2m r) | 2.2m g (1.6m r) | 53g (38r) | 26g (19r) | 11g (8r) |
| `eurmil` | Mill | 94g | 10 | 1.8m g (1.3m r) | 53g (38r) | 21g (15r) | 11g (8r) | 11g (8r) |
| `eurpor` | Shipyard | 1562g | 30 | 29.4m g (21.0m r) | 14.7m g (10.5m r) | 5.9m g (4.2m r) | 2.9m g (2.1m r) | 59g (42r) |
| `eursga` | Gate | 90g | 13 | 1.7m g (1.2m r) | 51g (36r) | 20g (15r) | 10g (7r) | 8g (6r) |
| `eurswa` | Wall | 90g | 4 | 1.7m g (1.2m r) | 51g (36r) | 25g (18r) | 25g (18r) | 25g (18r) |
| `eurtow` | Tower | 1230g | 10 | 23.2m g (16.6m r) | 11.6m g (8.3m r) | 4.6m g (3.3m r) | 2.3m g (1.7m r) | 2.3m g (1.7m r) |
| `polaca` | Academy | 625g | 18 | 11.8m g (8.4m r) | 5.9m g (4.2m r) | 2.4m g (1.7m r) | 1.2m g (0.8m r) | 39g (28r) |
| `polart` | Artillery Depot | 246g | 19 | 4.6m g (3.3m r) | 2.3m g (1.7m r) | 56g (40r) | 28g (20r) | 15g (10r) |
| `polba2` | Barracks, 18th century | 5625g | 25 | 105.9m g (75.7m r) | 53.0m g (37.8m r) | 21.2m g (15.1m r) | 10.6m g (7.6m r) | 4.2m g (3.0m r) |
| `polbar` | Barracks, 17th century | 94g | 27 | 1.8m g (1.3m r) | 53g (38r) | 21g (15r) | 11g (8r) | 4g (3r) |
| `polbla` | Blacksmith | 94g | 18 | 1.8m g (1.3m r) | 53g (38r) | 21g (15r) | 11g (8r) | 6g (4r) |
| `polcen` | Town Hall | 156g | 18 | 2.9m g (2.1m r) | 1.5m g (1.1m r) | 35g (25r) | 18g (13r) | 10g (7r) |
| `poldip` | Diplomatic Center | 312g | 16 | 5.9m g (4.2m r) | 2.9m g (2.1m r) | 1.2m g (0.8m r) | 35g (25r) | 22g (16r) |
| `polhou` | Housing | 31g | 17 | 35g (25r) | 18g (13r) | 7g (5r) | 4g (3r) | 2g (1r) |
| `polsta` | Stable | 625g | 26 | 11.8m g (8.4m r) | 5.9m g (4.2m r) | 2.4m g (1.7m r) | 1.2m g (0.8m r) | 27g (19r) |
| `poltem` | Cathedral | 156g | 22 | 2.9m g (2.1m r) | 1.5m g (1.1m r) | 35g (25r) | 18g (13r) | 8g (6r) |
| `russto` | Storehouse | 31g | 8 | 35g (25r) | 18g (13r) | 7g (5r) | 4g (3r) | 4g (3r) |
| `ukrwga` | Gate | 6g | 13 | 6g (5r) | 3g (2r) | 1g (1r) | 1g (0r) | 0g (0r) |
| `ukrwwa` | Palisade | 6g | 4 | 6g (5r) | 3g (2r) | 2g (1r) | 2g (1r) | 2g (1r) |

<a id="полный-ремонт-0--max-hp-8"></a>
<a id="полный-ремонт-9"></a>
### Full repair (0 → max HP)

| sid | name | maxhp | slot_cap | 1 is building. | 2 is building. | 5 is building. | 10 is building. | Max. builds. |
|---|---|---|---|---|---|---|---|---|
| `eurcoa` | Mine | 2500 | 16 | 51g (36r) | 25g (18r) | 10g (7r) | 5g (4r) | 3g (2r) |
| `eurgol` | Mine | 2500 | 16 | 51g (36r) | 25g (18r) | 10g (7r) | 5g (4r) | 3g (2r) |
| `euriro` | Mine | 2500 | 16 | 51g (36r) | 25g (18r) | 10g (7r) | 5g (4r) | 3g (2r) |
| `eurmar` | Market | 4000 | 25 | 1.4m g (1.0m r) | 41g (29r) | 16g (12r) | 8g (6r) | 3g (2r) |
| `eurmil` | Mill | 20000 | 10 | 6.8m g (4.8m r) | 3.4m g (2.4m r) | 1.4m g (1.0m r) | 41g (29r) | 41g (29r) |
| `eurpor` | Shipyard | 50000 | 30 | 16.9m g (12.1m r) | 8.5m g (6.0m r) | 3.4m g (2.4m r) | 1.7m g (1.2m r) | 34g (24r) |
| `eursga` | Gate | 32000 | 13 | 10.8m g (7.7m r) | 5.4m g (3.9m r) | 2.2m g (1.5m r) | 1.1m g (0.8m r) | 50g (36r) |
| `eurswa` | Wall | 50000 | 4 | 16.9m g (12.1m r) | 8.5m g (6.0m r) | 4.2m g (3.0m r) | 4.2m g (3.0m r) | 4.2m g (3.0m r) |
| `eurtow` | Tower | 20000 | 10 | 6.8m g (4.8m r) | 3.4m g (2.4m r) | 1.4m g (1.0m r) | 41g (29r) | 41g (29r) |
| `polaca` | Academy | 63000 | 18 | 21.3m g (15.2m r) | 10.7m g (7.6m r) | 4.3m g (3.0m r) | 2.1m g (1.5m r) | 1.2m g (0.8m r) |
| `polart` | Artillery Depot | 40000 | 19 | 13.5m g (9.7m r) | 6.8m g (4.8m r) | 2.7m g (1.9m r) | 1.4m g (1.0m r) | 43g (31r) |
| `polba2` | Barracks, 18th century | 55000 | 25 | 18.6m g (13.3m r) | 9.3m g (6.6m r) | 3.7m g (2.7m r) | 1.9m g (1.3m r) | 45g (32r) |
| `polbar` | Barracks, 17th century | 40000 | 27 | 13.5m g (9.7m r) | 6.8m g (4.8m r) | 2.7m g (1.9m r) | 1.4m g (1.0m r) | 30g (21r) |
| `polbla` | Blacksmith | 5500 | 18 | 1.9m g (1.3m r) | 56g (40r) | 22g (16r) | 11g (8r) | 6g (4r) |
| `polcen` | Town Hall | 4300 | 18 | 1.5m g (1.0m r) | 44g (31r) | 17g (12r) | 9g (6r) | 5g (3r) |
| `poldip` | Diplomatic Center | 4500 | 16 | 1.5m g (1.1m r) | 46g (33r) | 18g (13r) | 9g (7r) | 6g (4r) |
| `polhou` | Housing | 4100 | 17 | 1.4m g (1.0m r) | 42g (30r) | 17g (12r) | 8g (6r) | 5g (3r) |
| `polsta` | Stable | 20000 | 26 | 6.8m g (4.8m r) | 3.4m g (2.4m r) | 1.4m g (1.0m r) | 41g (29r) | 16g (11r) |
| `poltem` | Cathedral | 4200 | 22 | 1.4m g (1.0m r) | 43g (30r) | 17g (12r) | 9g (6r) | 4g (3r) |
| `russto` | Storehouse | 10000 | 8 | 3.4m g (2.4m r) | 1.7m g (1.2m r) | 41g (29r) | 25g (18r) | 25g (18r) |
| `ukrwga` | Gate | 1500 | 13 | 30g (22r) | 15g (11r) | 6g (4r) | 3g (2r) | 2g (2r) |
| `ukrwwa` | Palisade | 1500 | 4 | 30g (22r) | 15g (11r) | 8g (5r) | 8g (5r) | 8g (5r) |

<a id="por--portugal-португалия"></a>
<a id="португалия-por"></a>
## Portugal (`por`)
<a id="постройка-с-нуля-10"></a>
### Building from scratch

| sid | name | buildtime_g | slot_cap | 1 is building. | 2 is building. | 5 is building. | 10 is building. | Max. builds. |
|---|---|---|---|---|---|---|---|---|
| `eurcoa` | Mine | 94g | 16 | 1.8m g (1.3m r) | 53g (38r) | 21g (15r) | 11g (8r) | 7g (5r) |
| `eurgol` | Mine | 94g | 16 | 1.8m g (1.3m r) | 53g (38r) | 21g (15r) | 11g (8r) | 7g (5r) |
| `euriro` | Mine | 94g | 16 | 1.8m g (1.3m r) | 53g (38r) | 21g (15r) | 11g (8r) | 7g (5r) |
| `eurmil` | Mill | 94g | 10 | 1.8m g (1.3m r) | 53g (38r) | 21g (15r) | 11g (8r) | 11g (8r) |
| `eursga` | Gate | 90g | 13 | 1.7m g (1.2m r) | 51g (36r) | 20g (15r) | 10g (7r) | 8g (6r) |
| `eurswa` | Wall | 90g | 4 | 1.7m g (1.2m r) | 51g (36r) | 25g (18r) | 25g (18r) | 25g (18r) |
| `eurtow` | Tower | 1230g | 10 | 23.2m g (16.6m r) | 11.6m g (8.3m r) | 4.6m g (3.3m r) | 2.3m g (1.7m r) | 2.3m g (1.7m r) |
| `poraca` | Academy | 625g | 16 | 11.8m g (8.4m r) | 5.9m g (4.2m r) | 2.4m g (1.7m r) | 1.2m g (0.8m r) | 44g (32r) |
| `porart` | Artillery Depot | 246g | 22 | 4.6m g (3.3m r) | 2.3m g (1.7m r) | 56g (40r) | 28g (20r) | 13g (9r) |
| `porba2` | Barracks, 18th century | 5625g | 24 | 105.9m g (75.7m r) | 53.0m g (37.8m r) | 21.2m g (15.1m r) | 10.6m g (7.6m r) | 4.4m g (3.2m r) |
| `porbar` | Barracks, 17th century | 94g | 22 | 1.8m g (1.3m r) | 53g (38r) | 21g (15r) | 11g (8r) | 5g (3r) |
| `porbla` | Blacksmith | 94g | 15 | 1.8m g (1.3m r) | 53g (38r) | 21g (15r) | 11g (8r) | 7g (5r) |
| `porcen` | Town Hall | 156g | 21 | 2.9m g (2.1m r) | 1.5m g (1.1m r) | 35g (25r) | 18g (13r) | 8g (6r) |
| `pordip` | Diplomatic Center | 312g | 18 | 5.9m g (4.2m r) | 2.9m g (2.1m r) | 1.2m g (0.8m r) | 35g (25r) | 20g (14r) |
| `porhou` | Housing | 31g | 13 | 35g (25r) | 18g (13r) | 7g (5r) | 4g (3r) | 3g (2r) |
| `porpor` | Shipyard | 1562g | 21 | 29.4m g (21.0m r) | 14.7m g (10.5m r) | 5.9m g (4.2m r) | 2.9m g (2.1m r) | 1.4m g (1.0m r) |
| `porsta` | Stable | 625g | 24 | 11.8m g (8.4m r) | 5.9m g (4.2m r) | 2.4m g (1.7m r) | 1.2m g (0.8m r) | 29g (21r) |
| `portem` | Cathedral | 156g | 25 | 2.9m g (2.1m r) | 1.5m g (1.1m r) | 35g (25r) | 18g (13r) | 7g (5r) |
| `spamar` | Market | 156g | 24 | 2.9m g (2.1m r) | 1.5m g (1.1m r) | 35g (25r) | 18g (13r) | 7g (5r) |
| `spasto` | Storehouse | 31g | 7 | 35g (25r) | 18g (13r) | 7g (5r) | 5g (4r) | 5g (4r) |
| `ukrwga` | Gate | 6g | 13 | 6g (5r) | 3g (2r) | 1g (1r) | 1g (0r) | 0g (0r) |
| `ukrwwa` | Palisade | 6g | 4 | 6g (5r) | 3g (2r) | 2g (1r) | 2g (1r) | 2g (1r) |

<a id="полный-ремонт-0--max-hp-9"></a>
<a id="полный-ремонт-10"></a>
### Full repair (0 → max HP)

| sid | name | maxhp | slot_cap | 1 is building. | 2 is building. | 5 is building. | 10 is building. | Max. builds. |
|---|---|---|---|---|---|---|---|---|
| `eurcoa` | Mine | 2500 | 16 | 51g (36r) | 25g (18r) | 10g (7r) | 5g (4r) | 3g (2r) |
| `eurgol` | Mine | 2500 | 16 | 51g (36r) | 25g (18r) | 10g (7r) | 5g (4r) | 3g (2r) |
| `euriro` | Mine | 2500 | 16 | 51g (36r) | 25g (18r) | 10g (7r) | 5g (4r) | 3g (2r) |
| `eurmil` | Mill | 20000 | 10 | 6.8m g (4.8m r) | 3.4m g (2.4m r) | 1.4m g (1.0m r) | 41g (29r) | 41g (29r) |
| `eursga` | Gate | 32000 | 13 | 10.8m g (7.7m r) | 5.4m g (3.9m r) | 2.2m g (1.5m r) | 1.1m g (0.8m r) | 50g (36r) |
| `eurswa` | Wall | 50000 | 4 | 16.9m g (12.1m r) | 8.5m g (6.0m r) | 4.2m g (3.0m r) | 4.2m g (3.0m r) | 4.2m g (3.0m r) |
| `eurtow` | Tower | 20000 | 10 | 6.8m g (4.8m r) | 3.4m g (2.4m r) | 1.4m g (1.0m r) | 41g (29r) | 41g (29r) |
| `poraca` | Academy | 63000 | 16 | 21.3m g (15.2m r) | 10.7m g (7.6m r) | 4.3m g (3.0m r) | 2.1m g (1.5m r) | 1.3m g (1.0m r) |
| `porart` | Artillery Depot | 40000 | 22 | 13.5m g (9.7m r) | 6.8m g (4.8m r) | 2.7m g (1.9m r) | 1.4m g (1.0m r) | 37g (26r) |
| `porba2` | Barracks, 18th century | 55000 | 24 | 18.6m g (13.3m r) | 9.3m g (6.6m r) | 3.7m g (2.7m r) | 1.9m g (1.3m r) | 47g (33r) |
| `porbar` | Barracks, 17th century | 40000 | 22 | 13.5m g (9.7m r) | 6.8m g (4.8m r) | 2.7m g (1.9m r) | 1.4m g (1.0m r) | 37g (26r) |
| `porbla` | Blacksmith | 5500 | 15 | 1.9m g (1.3m r) | 56g (40r) | 22g (16r) | 11g (8r) | 7g (5r) |
| `porcen` | Town Hall | 4000 | 21 | 1.4m g (1.0m r) | 41g (29r) | 16g (12r) | 8g (6r) | 4g (3r) |
| `pordip` | Diplomatic Center | 4500 | 18 | 1.5m g (1.1m r) | 46g (33r) | 18g (13r) | 9g (7r) | 5g (4r) |
| `porhou` | Housing | 4000 | 13 | 1.4m g (1.0m r) | 41g (29r) | 16g (12r) | 8g (6r) | 6g (4r) |
| `porpor` | Shipyard | 50000 | 21 | 16.9m g (12.1m r) | 8.5m g (6.0m r) | 3.4m g (2.4m r) | 1.7m g (1.2m r) | 48g (35r) |
| `porsta` | Stable | 20000 | 24 | 6.8m g (4.8m r) | 3.4m g (2.4m r) | 1.4m g (1.0m r) | 41g (29r) | 17g (12r) |
| `portem` | Cathedral | 4200 | 25 | 1.4m g (1.0m r) | 43g (30r) | 17g (12r) | 9g (6r) | 3g (2r) |
| `spamar` | Market | 4000 | 24 | 1.4m g (1.0m r) | 41g (29r) | 16g (12r) | 8g (6r) | 3g (2r) |
| `spasto` | Storehouse | 10000 | 7 | 3.4m g (2.4m r) | 1.7m g (1.2m r) | 41g (29r) | 29g (21r) | 29g (21r) |
| `ukrwga` | Gate | 1500 | 13 | 30g (22r) | 15g (11r) | 6g (4r) | 3g (2r) | 2g (2r) |
| `ukrwwa` | Palisade | 1500 | 4 | 30g (22r) | 15g (11r) | 8g (5r) | 8g (5r) | 8g (5r) |

<a id="pru--prussia-пруссия"></a>
<a id="пруссия-pru"></a>
## Prussia (`pru`)
<a id="постройка-с-нуля-11"></a>
### Building from scratch

| sid | name | buildtime_g | slot_cap | 1 is building. | 2 is building. | 5 is building. | 10 is building. | Max. builds. |
|---|---|---|---|---|---|---|---|---|
| `eurcoa` | Mine | 94g | 16 | 1.8m g (1.3m r) | 53g (38r) | 21g (15r) | 11g (8r) | 7g (5r) |
| `eurgol` | Mine | 94g | 16 | 1.8m g (1.3m r) | 53g (38r) | 21g (15r) | 11g (8r) | 7g (5r) |
| `euriro` | Mine | 94g | 16 | 1.8m g (1.3m r) | 53g (38r) | 21g (15r) | 11g (8r) | 7g (5r) |
| `eurmar` | Market | 234g | 25 | 4.4m g (3.2m r) | 2.2m g (1.6m r) | 53g (38r) | 26g (19r) | 11g (8r) |
| `eurmil` | Mill | 94g | 10 | 1.8m g (1.3m r) | 53g (38r) | 21g (15r) | 11g (8r) | 11g (8r) |
| `eurpor` | Shipyard | 1562g | 30 | 29.4m g (21.0m r) | 14.7m g (10.5m r) | 5.9m g (4.2m r) | 2.9m g (2.1m r) | 59g (42r) |
| `eursga` | Gate | 90g | 13 | 1.7m g (1.2m r) | 51g (36r) | 20g (15r) | 10g (7r) | 8g (6r) |
| `eursto` | Storehouse | 31g | 9 | 35g (25r) | 18g (13r) | 7g (5r) | 4g (3r) | 4g (3r) |
| `eurswa` | Wall | 90g | 4 | 1.7m g (1.2m r) | 51g (36r) | 25g (18r) | 25g (18r) | 25g (18r) |
| `eurtow` | Tower | 1230g | 10 | 23.2m g (16.6m r) | 11.6m g (8.3m r) | 4.6m g (3.3m r) | 2.3m g (1.7m r) | 2.3m g (1.7m r) |
| `pruaca` | Academy | 625g | 18 | 11.8m g (8.4m r) | 5.9m g (4.2m r) | 2.4m g (1.7m r) | 1.2m g (0.8m r) | 39g (28r) |
| `pruart` | Artillery Depot | 246g | 22 | 4.6m g (3.3m r) | 2.3m g (1.7m r) | 56g (40r) | 28g (20r) | 13g (9r) |
| `pruba2` | Barracks, 18th century | 5625g | 22 | 105.9m g (75.7m r) | 53.0m g (37.8m r) | 21.2m g (15.1m r) | 10.6m g (7.6m r) | 4.8m g (3.4m r) |
| `prubar` | Barracks, 17th century | 94g | 18 | 1.8m g (1.3m r) | 53g (38r) | 21g (15r) | 11g (8r) | 6g (4r) |
| `prubla` | Blacksmith | 94g | 14 | 1.8m g (1.3m r) | 53g (38r) | 21g (15r) | 11g (8r) | 8g (5r) |
| `prucen` | Town Hall | 156g | 20 | 2.9m g (2.1m r) | 1.5m g (1.1m r) | 35g (25r) | 18g (13r) | 9g (6r) |
| `prudip` | Diplomatic Center | 312g | 19 | 5.9m g (4.2m r) | 2.9m g (2.1m r) | 1.2m g (0.8m r) | 35g (25r) | 19g (13r) |
| `pruhou` | Housing | 31g | 12 | 35g (25r) | 18g (13r) | 7g (5r) | 4g (3r) | 3g (2r) |
| `prusta` | Stable | 625g | 19 | 11.8m g (8.4m r) | 5.9m g (4.2m r) | 2.4m g (1.7m r) | 1.2m g (0.8m r) | 37g (27r) |
| `prutem` | Cathedral | 156g | 25 | 2.9m g (2.1m r) | 1.5m g (1.1m r) | 35g (25r) | 18g (13r) | 7g (5r) |
| `ukrwga` | Gate | 6g | 13 | 6g (5r) | 3g (2r) | 1g (1r) | 1g (0r) | 0g (0r) |
| `ukrwwa` | Palisade | 6g | 4 | 6g (5r) | 3g (2r) | 2g (1r) | 2g (1r) | 2g (1r) |

<a id="полный-ремонт-0--max-hp-10"></a>
<a id="полный-ремонт-11"></a>
### Full repair (0 → max HP)

| sid | name | maxhp | slot_cap | 1 is building. | 2 is building. | 5 is building. | 10 is building. | Max. builds. |
|---|---|---|---|---|---|---|---|---|
| `eurcoa` | Mine | 2500 | 16 | 51g (36r) | 25g (18r) | 10g (7r) | 5g (4r) | 3g (2r) |
| `eurgol` | Mine | 2500 | 16 | 51g (36r) | 25g (18r) | 10g (7r) | 5g (4r) | 3g (2r) |
| `euriro` | Mine | 2500 | 16 | 51g (36r) | 25g (18r) | 10g (7r) | 5g (4r) | 3g (2r) |
| `eurmar` | Market | 4000 | 25 | 1.4m g (1.0m r) | 41g (29r) | 16g (12r) | 8g (6r) | 3g (2r) |
| `eurmil` | Mill | 20000 | 10 | 6.8m g (4.8m r) | 3.4m g (2.4m r) | 1.4m g (1.0m r) | 41g (29r) | 41g (29r) |
| `eurpor` | Shipyard | 50000 | 30 | 16.9m g (12.1m r) | 8.5m g (6.0m r) | 3.4m g (2.4m r) | 1.7m g (1.2m r) | 34g (24r) |
| `eursga` | Gate | 32000 | 13 | 10.8m g (7.7m r) | 5.4m g (3.9m r) | 2.2m g (1.5m r) | 1.1m g (0.8m r) | 50g (36r) |
| `eursto` | Storehouse | 10000 | 9 | 3.4m g (2.4m r) | 1.7m g (1.2m r) | 41g (29r) | 23g (16r) | 23g (16r) |
| `eurswa` | Wall | 50000 | 4 | 16.9m g (12.1m r) | 8.5m g (6.0m r) | 4.2m g (3.0m r) | 4.2m g (3.0m r) | 4.2m g (3.0m r) |
| `eurtow` | Tower | 20000 | 10 | 6.8m g (4.8m r) | 3.4m g (2.4m r) | 1.4m g (1.0m r) | 41g (29r) | 41g (29r) |
| `pruaca` | Academy | 63000 | 18 | 21.3m g (15.2m r) | 10.7m g (7.6m r) | 4.3m g (3.0m r) | 2.1m g (1.5m r) | 1.2m g (0.8m r) |
| `pruart` | Artillery Depot | 40000 | 22 | 13.5m g (9.7m r) | 6.8m g (4.8m r) | 2.7m g (1.9m r) | 1.4m g (1.0m r) | 37g (26r) |
| `pruba2` | Barracks, 18th century | 55000 | 22 | 18.6m g (13.3m r) | 9.3m g (6.6m r) | 3.7m g (2.7m r) | 1.9m g (1.3m r) | 51g (36r) |
| `prubar` | Barracks, 17th century | 40000 | 18 | 13.5m g (9.7m r) | 6.8m g (4.8m r) | 2.7m g (1.9m r) | 1.4m g (1.0m r) | 45g (32r) |
| `prubla` | Blacksmith | 5500 | 14 | 1.9m g (1.3m r) | 56g (40r) | 22g (16r) | 11g (8r) | 8g (6r) |
| `prucen` | Town Hall | 4200 | 20 | 1.4m g (1.0m r) | 43g (30r) | 17g (12r) | 9g (6r) | 4g (3r) |
| `prudip` | Diplomatic Center | 4500 | 19 | 1.5m g (1.1m r) | 46g (33r) | 18g (13r) | 9g (7r) | 5g (3r) |
| `pruhou` | Housing | 4500 | 12 | 1.5m g (1.1m r) | 46g (33r) | 18g (13r) | 9g (7r) | 8g (5r) |
| `prusta` | Stable | 20000 | 19 | 6.8m g (4.8m r) | 3.4m g (2.4m r) | 1.4m g (1.0m r) | 41g (29r) | 21g (15r) |
| `prutem` | Cathedral | 4200 | 25 | 1.4m g (1.0m r) | 43g (30r) | 17g (12r) | 9g (6r) | 3g (2r) |
| `ukrwga` | Gate | 1500 | 13 | 30g (22r) | 15g (11r) | 6g (4r) | 3g (2r) | 2g (2r) |
| `ukrwwa` | Palisade | 1500 | 4 | 30g (22r) | 15g (11r) | 8g (5r) | 8g (5r) | 8g (5r) |

<a id="rus--russia-россия"></a>
<a id="россия-rus"></a>
## Russia (`rus`)
<a id="постройка-с-нуля-12"></a>
### Building from scratch

| sid | name | buildtime_g | slot_cap | 1 is building. | 2 is building. | 5 is building. | 10 is building. | Max. builds. |
|---|---|---|---|---|---|---|---|---|
| `eurcoa` | Mine | 94g | 16 | 1.8m g (1.3m r) | 53g (38r) | 21g (15r) | 11g (8r) | 7g (5r) |
| `eurgol` | Mine | 94g | 16 | 1.8m g (1.3m r) | 53g (38r) | 21g (15r) | 11g (8r) | 7g (5r) |
| `euriro` | Mine | 94g | 16 | 1.8m g (1.3m r) | 53g (38r) | 21g (15r) | 11g (8r) | 7g (5r) |
| `rusaca` | Academy | 844g | 25 | 15.9m g (11.4m r) | 7.9m g (5.7m r) | 3.2m g (2.3m r) | 1.6m g (1.1m r) | 38g (27r) |
| `rusart` | Artillery Depot | 246g | 24 | 4.6m g (3.3m r) | 2.3m g (1.7m r) | 56g (40r) | 28g (20r) | 12g (8r) |
| `rusba2` | Barracks, 18th century | 5625g | 30 | 105.9m g (75.7m r) | 53.0m g (37.8m r) | 21.2m g (15.1m r) | 10.6m g (7.6m r) | 3.5m g (2.5m r) |
| `rusbar` | Strelets Barracks | 78g | 23 | 1.5m g (1.1m r) | 44g (32r) | 18g (13r) | 9g (6r) | 4g (3r) |
| `rusbla` | Blacksmith | 94g | 15 | 1.8m g (1.3m r) | 53g (38r) | 21g (15r) | 11g (8r) | 7g (5r) |
| `ruscen` | Town Hall | 156g | 24 | 2.9m g (2.1m r) | 1.5m g (1.1m r) | 35g (25r) | 18g (13r) | 7g (5r) |
| `rusdip` | Diplomatic Center | 312g | 18 | 5.9m g (4.2m r) | 2.9m g (2.1m r) | 1.2m g (0.8m r) | 35g (25r) | 20g (14r) |
| `rushou` | Izba | 31g | 17 | 35g (25r) | 18g (13r) | 7g (5r) | 4g (3r) | 2g (1r) |
| `rusmar` | Market | 234g | 23 | 4.4m g (3.2m r) | 2.2m g (1.6m r) | 53g (38r) | 26g (19r) | 12g (8r) |
| `rusmil` | Mill | 94g | 7 | 1.8m g (1.3m r) | 53g (38r) | 21g (15r) | 15g (11r) | 15g (11r) |
| `ruspor` | Shipyard | 1562g | 27 | 29.4m g (21.0m r) | 14.7m g (10.5m r) | 5.9m g (4.2m r) | 2.9m g (2.1m r) | 1.1m g (0.8m r) |
| `russga` | Gate | 200g | 13 | 3.8m g (2.7m r) | 1.9m g (1.3m r) | 45g (32r) | 23g (16r) | 17g (12r) |
| `russta` | Stable | 375g | 22 | 7.1m g (5.0m r) | 3.5m g (2.5m r) | 1.4m g (1.0m r) | 42g (30r) | 19g (14r) |
| `russto` | Storehouse | 31g | 8 | 35g (25r) | 18g (13r) | 7g (5r) | 4g (3r) | 4g (3r) |
| `russwa` | Wall | 200g | 4 | 3.8m g (2.7m r) | 1.9m g (1.3m r) | 56g (40r) | 56g (40r) | 56g (40r) |
| `rustem` | Orthodox Cathedral | 156g | 30 | 2.9m g (2.1m r) | 1.5m g (1.1m r) | 35g (25r) | 18g (13r) | 6g (4r) |
| `rustow` | Tower | 1477g | 10 | 27.8m g (19.9m r) | 13.9m g (9.9m r) | 5.6m g (4.0m r) | 2.8m g (2.0m r) | 2.8m g (2.0m r) |
| `ukrwga` | Gate | 6g | 13 | 6g (5r) | 3g (2r) | 1g (1r) | 1g (0r) | 0g (0r) |
| `ukrwwa` | Palisade | 6g | 4 | 6g (5r) | 3g (2r) | 2g (1r) | 2g (1r) | 2g (1r) |

<a id="полный-ремонт-0--max-hp-11"></a>
<a id="полный-ремонт-12"></a>
### Full repair (0 → max HP)

| sid | name | maxhp | slot_cap | 1 is building. | 2 is building. | 5 is building. | 10 is building. | Max. builds. |
|---|---|---|---|---|---|---|---|---|
| `eurcoa` | Mine | 2500 | 16 | 51g (36r) | 25g (18r) | 10g (7r) | 5g (4r) | 3g (2r) |
| `eurgol` | Mine | 2500 | 16 | 51g (36r) | 25g (18r) | 10g (7r) | 5g (4r) | 3g (2r) |
| `euriro` | Mine | 2500 | 16 | 51g (36r) | 25g (18r) | 10g (7r) | 5g (4r) | 3g (2r) |
| `rusaca` | Academy | 65000 | 25 | 22.0m g (15.7m r) | 11.0m g (7.9m r) | 4.4m g (3.1m r) | 2.2m g (1.6m r) | 53g (38r) |
| `rusart` | Artillery Depot | 40000 | 24 | 13.5m g (9.7m r) | 6.8m g (4.8m r) | 2.7m g (1.9m r) | 1.4m g (1.0m r) | 34g (24r) |
| `rusba2` | Barracks, 18th century | 55000 | 30 | 18.6m g (13.3m r) | 9.3m g (6.6m r) | 3.7m g (2.7m r) | 1.9m g (1.3m r) | 37g (27r) |
| `rusbar` | Strelets Barracks | 25000 | 23 | 8.5m g (6.0m r) | 4.2m g (3.0m r) | 1.7m g (1.2m r) | 51g (36r) | 22g (16r) |
| `rusbla` | Blacksmith | 5500 | 15 | 1.9m g (1.3m r) | 56g (40r) | 22g (16r) | 11g (8r) | 7g (5r) |
| `ruscen` | Town Hall | 4050 | 24 | 1.4m g (1.0m r) | 41g (29r) | 16g (12r) | 8g (6r) | 3g (2r) |
| `rusdip` | Diplomatic Center | 6500 | 18 | 2.2m g (1.6m r) | 1.1m g (0.8m r) | 26g (19r) | 13g (9r) | 7g (5r) |
| `rushou` | Izba | 5000 | 17 | 1.7m g (1.2m r) | 51g (36r) | 20g (15r) | 10g (7r) | 6g (4r) |
| `rusmar` | Market | 4000 | 23 | 1.4m g (1.0m r) | 41g (29r) | 16g (12r) | 8g (6r) | 4g (3r) |
| `rusmil` | Mill | 15000 | 7 | 5.1m g (3.6m r) | 2.5m g (1.8m r) | 1.0m g (0.7m r) | 44g (31r) | 44g (31r) |
| `ruspor` | Shipyard | 45000 | 27 | 15.2m g (10.9m r) | 7.6m g (5.4m r) | 3.0m g (2.2m r) | 1.5m g (1.1m r) | 34g (24r) |
| `russga` | Gate | 32000 | 13 | 10.8m g (7.7m r) | 5.4m g (3.9m r) | 2.2m g (1.5m r) | 1.1m g (0.8m r) | 50g (36r) |
| `russta` | Stable | 25000 | 22 | 8.5m g (6.0m r) | 4.2m g (3.0m r) | 1.7m g (1.2m r) | 51g (36r) | 23g (16r) |
| `russto` | Storehouse | 10000 | 8 | 3.4m g (2.4m r) | 1.7m g (1.2m r) | 41g (29r) | 25g (18r) | 25g (18r) |
| `russwa` | Wall | 50000 | 4 | 16.9m g (12.1m r) | 8.5m g (6.0m r) | 4.2m g (3.0m r) | 4.2m g (3.0m r) | 4.2m g (3.0m r) |
| `rustem` | Orthodox Cathedral | 4500 | 30 | 1.5m g (1.1m r) | 46g (33r) | 18g (13r) | 9g (7r) | 3g (2r) |
| `rustow` | Tower | 21000 | 10 | 7.1m g (5.1m r) | 3.6m g (2.5m r) | 1.4m g (1.0m r) | 43g (30r) | 43g (30r) |
| `ukrwga` | Gate | 1500 | 13 | 30g (22r) | 15g (11r) | 6g (4r) | 3g (2r) | 2g (2r) |
| `ukrwwa` | Palisade | 1500 | 4 | 30g (22r) | 15g (11r) | 8g (5r) | 8g (5r) | 8g (5r) |

<a id="sax--saxony-саксония"></a>
<a id="саксония-sax"></a>
## Saxony (`sax`)
<a id="постройка-с-нуля-13"></a>
### Building from scratch

| sid | name | buildtime_g | slot_cap | 1 is building. | 2 is building. | 5 is building. | 10 is building. | Max. builds. |
|---|---|---|---|---|---|---|---|---|
| `eurcoa` | Mine | 94g | 16 | 1.8m g (1.3m r) | 53g (38r) | 21g (15r) | 11g (8r) | 7g (5r) |
| `eurgol` | Mine | 94g | 16 | 1.8m g (1.3m r) | 53g (38r) | 21g (15r) | 11g (8r) | 7g (5r) |
| `euriro` | Mine | 94g | 16 | 1.8m g (1.3m r) | 53g (38r) | 21g (15r) | 11g (8r) | 7g (5r) |
| `eurmar` | Market | 234g | 25 | 4.4m g (3.2m r) | 2.2m g (1.6m r) | 53g (38r) | 26g (19r) | 11g (8r) |
| `eurmil` | Mill | 94g | 10 | 1.8m g (1.3m r) | 53g (38r) | 21g (15r) | 11g (8r) | 11g (8r) |
| `eurpor` | Shipyard | 1562g | 30 | 29.4m g (21.0m r) | 14.7m g (10.5m r) | 5.9m g (4.2m r) | 2.9m g (2.1m r) | 59g (42r) |
| `eursga` | Gate | 90g | 13 | 1.7m g (1.2m r) | 51g (36r) | 20g (15r) | 10g (7r) | 8g (6r) |
| `eursto` | Storehouse | 31g | 9 | 35g (25r) | 18g (13r) | 7g (5r) | 4g (3r) | 4g (3r) |
| `eurswa` | Wall | 90g | 4 | 1.7m g (1.2m r) | 51g (36r) | 25g (18r) | 25g (18r) | 25g (18r) |
| `eurtow` | Tower | 1230g | 10 | 23.2m g (16.6m r) | 11.6m g (8.3m r) | 4.6m g (3.3m r) | 2.3m g (1.7m r) | 2.3m g (1.7m r) |
| `saxaca` | Academy | 625g | 19 | 11.8m g (8.4m r) | 5.9m g (4.2m r) | 2.4m g (1.7m r) | 1.2m g (0.8m r) | 37g (27r) |
| `saxart` | Artillery Depot | 246g | 19 | 4.6m g (3.3m r) | 2.3m g (1.7m r) | 56g (40r) | 28g (20r) | 15g (10r) |
| `saxba2` | Barracks, 18th century | 5625g | 20 | 105.9m g (75.7m r) | 53.0m g (37.8m r) | 21.2m g (15.1m r) | 10.6m g (7.6m r) | 5.3m g (3.8m r) |
| `saxbar` | Barracks, 17th century | 94g | 20 | 1.8m g (1.3m r) | 53g (38r) | 21g (15r) | 11g (8r) | 5g (4r) |
| `saxbla` | Blacksmith | 94g | 14 | 1.8m g (1.3m r) | 53g (38r) | 21g (15r) | 11g (8r) | 8g (5r) |
| `saxcen` | Town Hall | 156g | 21 | 2.9m g (2.1m r) | 1.5m g (1.1m r) | 35g (25r) | 18g (13r) | 8g (6r) |
| `saxdip` | Diplomatic Center | 312g | 17 | 5.9m g (4.2m r) | 2.9m g (2.1m r) | 1.2m g (0.8m r) | 35g (25r) | 21g (15r) |
| `saxhou` | Housing | 31g | 13 | 35g (25r) | 18g (13r) | 7g (5r) | 4g (3r) | 3g (2r) |
| `saxsta` | Stable | 625g | 19 | 11.8m g (8.4m r) | 5.9m g (4.2m r) | 2.4m g (1.7m r) | 1.2m g (0.8m r) | 37g (27r) |
| `saxtem` | Cathedral | 156g | 26 | 2.9m g (2.1m r) | 1.5m g (1.1m r) | 35g (25r) | 18g (13r) | 7g (5r) |
| `ukrwga` | Gate | 6g | 13 | 6g (5r) | 3g (2r) | 1g (1r) | 1g (0r) | 0g (0r) |
| `ukrwwa` | Palisade | 6g | 4 | 6g (5r) | 3g (2r) | 2g (1r) | 2g (1r) | 2g (1r) |

<a id="полный-ремонт-0--max-hp-12"></a>
<a id="полный-ремонт-13"></a>
### Full repair (0 → max HP)

| sid | name | maxhp | slot_cap | 1 is building. | 2 is building. | 5 is building. | 10 is building. | Max. builds. |
|---|---|---|---|---|---|---|---|---|
| `eurcoa` | Mine | 2500 | 16 | 51g (36r) | 25g (18r) | 10g (7r) | 5g (4r) | 3g (2r) |
| `eurgol` | Mine | 2500 | 16 | 51g (36r) | 25g (18r) | 10g (7r) | 5g (4r) | 3g (2r) |
| `euriro` | Mine | 2500 | 16 | 51g (36r) | 25g (18r) | 10g (7r) | 5g (4r) | 3g (2r) |
| `eurmar` | Market | 4000 | 25 | 1.4m g (1.0m r) | 41g (29r) | 16g (12r) | 8g (6r) | 3g (2r) |
| `eurmil` | Mill | 20000 | 10 | 6.8m g (4.8m r) | 3.4m g (2.4m r) | 1.4m g (1.0m r) | 41g (29r) | 41g (29r) |
| `eurpor` | Shipyard | 50000 | 30 | 16.9m g (12.1m r) | 8.5m g (6.0m r) | 3.4m g (2.4m r) | 1.7m g (1.2m r) | 34g (24r) |
| `eursga` | Gate | 32000 | 13 | 10.8m g (7.7m r) | 5.4m g (3.9m r) | 2.2m g (1.5m r) | 1.1m g (0.8m r) | 50g (36r) |
| `eursto` | Storehouse | 10000 | 9 | 3.4m g (2.4m r) | 1.7m g (1.2m r) | 41g (29r) | 23g (16r) | 23g (16r) |
| `eurswa` | Wall | 50000 | 4 | 16.9m g (12.1m r) | 8.5m g (6.0m r) | 4.2m g (3.0m r) | 4.2m g (3.0m r) | 4.2m g (3.0m r) |
| `eurtow` | Tower | 20000 | 10 | 6.8m g (4.8m r) | 3.4m g (2.4m r) | 1.4m g (1.0m r) | 41g (29r) | 41g (29r) |
| `saxaca` | Academy | 63000 | 19 | 21.3m g (15.2m r) | 10.7m g (7.6m r) | 4.3m g (3.0m r) | 2.1m g (1.5m r) | 1.1m g (0.8m r) |
| `saxart` | Artillery Depot | 40000 | 19 | 13.5m g (9.7m r) | 6.8m g (4.8m r) | 2.7m g (1.9m r) | 1.4m g (1.0m r) | 43g (31r) |
| `saxba2` | Barracks, 18th century | 55000 | 20 | 18.6m g (13.3m r) | 9.3m g (6.6m r) | 3.7m g (2.7m r) | 1.9m g (1.3m r) | 56g (40r) |
| `saxbar` | Barracks, 17th century | 40000 | 20 | 13.5m g (9.7m r) | 6.8m g (4.8m r) | 2.7m g (1.9m r) | 1.4m g (1.0m r) | 41g (29r) |
| `saxbla` | Blacksmith | 5500 | 14 | 1.9m g (1.3m r) | 56g (40r) | 22g (16r) | 11g (8r) | 8g (6r) |
| `saxcen` | Town Hall | 4000 | 21 | 1.4m g (1.0m r) | 41g (29r) | 16g (12r) | 8g (6r) | 4g (3r) |
| `saxdip` | Diplomatic Center | 4500 | 17 | 1.5m g (1.1m r) | 46g (33r) | 18g (13r) | 9g (7r) | 5g (4r) |
| `saxhou` | Housing | 4000 | 13 | 1.4m g (1.0m r) | 41g (29r) | 16g (12r) | 8g (6r) | 6g (4r) |
| `saxsta` | Stable | 20000 | 19 | 6.8m g (4.8m r) | 3.4m g (2.4m r) | 1.4m g (1.0m r) | 41g (29r) | 21g (15r) |
| `saxtem` | Cathedral | 4200 | 26 | 1.4m g (1.0m r) | 43g (30r) | 17g (12r) | 9g (6r) | 3g (2r) |
| `ukrwga` | Gate | 1500 | 13 | 30g (22r) | 15g (11r) | 6g (4r) | 3g (2r) | 2g (2r) |
| `ukrwwa` | Palisade | 1500 | 4 | 30g (22r) | 15g (11r) | 8g (5r) | 8g (5r) | 8g (5r) |

<a id="sco--scotland-шотландия"></a>
<a id="шотландия-sco"></a>
## Scotland (`sco`)
<a id="постройка-с-нуля-14"></a>
### Building from scratch

| sid | name | buildtime_g | slot_cap | 1 is building. | 2 is building. | 5 is building. | 10 is building. | Max. builds. |
|---|---|---|---|---|---|---|---|---|
| `eurcoa` | Mine | 94g | 16 | 1.8m g (1.3m r) | 53g (38r) | 21g (15r) | 11g (8r) | 7g (5r) |
| `eurgol` | Mine | 94g | 16 | 1.8m g (1.3m r) | 53g (38r) | 21g (15r) | 11g (8r) | 7g (5r) |
| `euriro` | Mine | 94g | 16 | 1.8m g (1.3m r) | 53g (38r) | 21g (15r) | 11g (8r) | 7g (5r) |
| `eurmar` | Market | 234g | 25 | 4.4m g (3.2m r) | 2.2m g (1.6m r) | 53g (38r) | 26g (19r) | 11g (8r) |
| `eurmil` | Mill | 94g | 10 | 1.8m g (1.3m r) | 53g (38r) | 21g (15r) | 11g (8r) | 11g (8r) |
| `eurpor` | Shipyard | 1562g | 30 | 29.4m g (21.0m r) | 14.7m g (10.5m r) | 5.9m g (4.2m r) | 2.9m g (2.1m r) | 59g (42r) |
| `eursga` | Gate | 90g | 13 | 1.7m g (1.2m r) | 51g (36r) | 20g (15r) | 10g (7r) | 8g (6r) |
| `eursto` | Storehouse | 31g | 9 | 35g (25r) | 18g (13r) | 7g (5r) | 4g (3r) | 4g (3r) |
| `eurswa` | Wall | 90g | 4 | 1.7m g (1.2m r) | 51g (36r) | 25g (18r) | 25g (18r) | 25g (18r) |
| `eurtow` | Tower | 1230g | 10 | 23.2m g (16.6m r) | 11.6m g (8.3m r) | 4.6m g (3.3m r) | 2.3m g (1.7m r) | 2.3m g (1.7m r) |
| `scoaca` | Academy | 625g | 20 | 11.8m g (8.4m r) | 5.9m g (4.2m r) | 2.4m g (1.7m r) | 1.2m g (0.8m r) | 35g (25r) |
| `scoart` | Artillery Depot | 246g | 21 | 4.6m g (3.3m r) | 2.3m g (1.7m r) | 56g (40r) | 28g (20r) | 13g (9r) |
| `scoba2` | Castle | 625g | 30 | 11.8m g (8.4m r) | 5.9m g (4.2m r) | 2.4m g (1.7m r) | 1.2m g (0.8m r) | 24g (17r) |
| `scobar` | Barracks, 17th century | 94g | 23 | 1.8m g (1.3m r) | 53g (38r) | 21g (15r) | 11g (8r) | 5g (3r) |
| `scobla` | Blacksmith | 94g | 16 | 1.8m g (1.3m r) | 53g (38r) | 21g (15r) | 11g (8r) | 7g (5r) |
| `scocen` | Town Hall | 156g | 28 | 2.9m g (2.1m r) | 1.5m g (1.1m r) | 35g (25r) | 18g (13r) | 6g (5r) |
| `scodip` | Diplomatic Center | 312g | 19 | 5.9m g (4.2m r) | 2.9m g (2.1m r) | 1.2m g (0.8m r) | 35g (25r) | 19g (13r) |
| `scohou` | Housing | 31g | 14 | 35g (25r) | 18g (13r) | 7g (5r) | 4g (3r) | 3g (2r) |
| `scosta` | Stable | 375g | 20 | 7.1m g (5.0m r) | 3.5m g (2.5m r) | 1.4m g (1.0m r) | 42g (30r) | 21g (15r) |
| `scotem` | Cathedral | 156g | 22 | 2.9m g (2.1m r) | 1.5m g (1.1m r) | 35g (25r) | 18g (13r) | 8g (6r) |
| `ukrwga` | Gate | 6g | 13 | 6g (5r) | 3g (2r) | 1g (1r) | 1g (0r) | 0g (0r) |
| `ukrwwa` | Palisade | 6g | 4 | 6g (5r) | 3g (2r) | 2g (1r) | 2g (1r) | 2g (1r) |

<a id="полный-ремонт-0--max-hp-13"></a>
<a id="полный-ремонт-14"></a>
### Full repair (0 → max HP)

| sid | name | maxhp | slot_cap | 1 is building. | 2 is building. | 5 is building. | 10 is building. | Max. builds. |
|---|---|---|---|---|---|---|---|---|
| `eurcoa` | Mine | 2500 | 16 | 51g (36r) | 25g (18r) | 10g (7r) | 5g (4r) | 3g (2r) |
| `eurgol` | Mine | 2500 | 16 | 51g (36r) | 25g (18r) | 10g (7r) | 5g (4r) | 3g (2r) |
| `euriro` | Mine | 2500 | 16 | 51g (36r) | 25g (18r) | 10g (7r) | 5g (4r) | 3g (2r) |
| `eurmar` | Market | 4000 | 25 | 1.4m g (1.0m r) | 41g (29r) | 16g (12r) | 8g (6r) | 3g (2r) |
| `eurmil` | Mill | 20000 | 10 | 6.8m g (4.8m r) | 3.4m g (2.4m r) | 1.4m g (1.0m r) | 41g (29r) | 41g (29r) |
| `eurpor` | Shipyard | 50000 | 30 | 16.9m g (12.1m r) | 8.5m g (6.0m r) | 3.4m g (2.4m r) | 1.7m g (1.2m r) | 34g (24r) |
| `eursga` | Gate | 32000 | 13 | 10.8m g (7.7m r) | 5.4m g (3.9m r) | 2.2m g (1.5m r) | 1.1m g (0.8m r) | 50g (36r) |
| `eursto` | Storehouse | 10000 | 9 | 3.4m g (2.4m r) | 1.7m g (1.2m r) | 41g (29r) | 23g (16r) | 23g (16r) |
| `eurswa` | Wall | 50000 | 4 | 16.9m g (12.1m r) | 8.5m g (6.0m r) | 4.2m g (3.0m r) | 4.2m g (3.0m r) | 4.2m g (3.0m r) |
| `eurtow` | Tower | 20000 | 10 | 6.8m g (4.8m r) | 3.4m g (2.4m r) | 1.4m g (1.0m r) | 41g (29r) | 41g (29r) |
| `scoaca` | Academy | 63000 | 20 | 21.3m g (15.2m r) | 10.7m g (7.6m r) | 4.3m g (3.0m r) | 2.1m g (1.5m r) | 1.1m g (0.8m r) |
| `scoart` | Artillery Depot | 40000 | 21 | 13.5m g (9.7m r) | 6.8m g (4.8m r) | 2.7m g (1.9m r) | 1.4m g (1.0m r) | 39g (28r) |
| `scoba2` | Castle | 40000 | 30 | 13.5m g (9.7m r) | 6.8m g (4.8m r) | 2.7m g (1.9m r) | 1.4m g (1.0m r) | 27g (19r) |
| `scobar` | Barracks, 17th century | 30000 | 23 | 10.2m g (7.3m r) | 5.1m g (3.6m r) | 2.0m g (1.5m r) | 1.0m g (0.7m r) | 26g (19r) |
| `scobla` | Blacksmith | 5500 | 16 | 1.9m g (1.3m r) | 56g (40r) | 22g (16r) | 11g (8r) | 7g (5r) |
| `scocen` | Town Hall | 4000 | 28 | 1.4m g (1.0m r) | 41g (29r) | 16g (12r) | 8g (6r) | 3g (2r) |
| `scodip` | Diplomatic Center | 4500 | 19 | 1.5m g (1.1m r) | 46g (33r) | 18g (13r) | 9g (7r) | 5g (3r) |
| `scohou` | Housing | 4000 | 14 | 1.4m g (1.0m r) | 41g (29r) | 16g (12r) | 8g (6r) | 6g (4r) |
| `scosta` | Stable | 25000 | 20 | 8.5m g (6.0m r) | 4.2m g (3.0m r) | 1.7m g (1.2m r) | 51g (36r) | 25g (18r) |
| `scotem` | Cathedral | 4200 | 22 | 1.4m g (1.0m r) | 43g (30r) | 17g (12r) | 9g (6r) | 4g (3r) |
| `ukrwga` | Gate | 1500 | 13 | 30g (22r) | 15g (11r) | 6g (4r) | 3g (2r) | 2g (2r) |
| `ukrwwa` | Palisade | 1500 | 4 | 30g (22r) | 15g (11r) | 8g (5r) | 8g (5r) | 8g (5r) |

<a id="spa--spain-испания"></a>
<a id="испания-spa"></a>
## Spain (`spa`)
<a id="постройка-с-нуля-15"></a>
### Building from scratch

| sid | name | buildtime_g | slot_cap | 1 is building. | 2 is building. | 5 is building. | 10 is building. | Max. builds. |
|---|---|---|---|---|---|---|---|---|
| `eurcoa` | Mine | 94g | 16 | 1.8m g (1.3m r) | 53g (38r) | 21g (15r) | 11g (8r) | 7g (5r) |
| `eurgol` | Mine | 94g | 16 | 1.8m g (1.3m r) | 53g (38r) | 21g (15r) | 11g (8r) | 7g (5r) |
| `euriro` | Mine | 94g | 16 | 1.8m g (1.3m r) | 53g (38r) | 21g (15r) | 11g (8r) | 7g (5r) |
| `eurmil` | Mill | 94g | 10 | 1.8m g (1.3m r) | 53g (38r) | 21g (15r) | 11g (8r) | 11g (8r) |
| `eurpor` | Shipyard | 1562g | 30 | 29.4m g (21.0m r) | 14.7m g (10.5m r) | 5.9m g (4.2m r) | 2.9m g (2.1m r) | 59g (42r) |
| `eursga` | Gate | 90g | 13 | 1.7m g (1.2m r) | 51g (36r) | 20g (15r) | 10g (7r) | 8g (6r) |
| `eurswa` | Wall | 90g | 4 | 1.7m g (1.2m r) | 51g (36r) | 25g (18r) | 25g (18r) | 25g (18r) |
| `eurtow` | Tower | 1230g | 10 | 23.2m g (16.6m r) | 11.6m g (8.3m r) | 4.6m g (3.3m r) | 2.3m g (1.7m r) | 2.3m g (1.7m r) |
| `spaaca` | Academy | 625g | 26 | 11.8m g (8.4m r) | 5.9m g (4.2m r) | 2.4m g (1.7m r) | 1.2m g (0.8m r) | 27g (19r) |
| `spaart` | Artillery Depot | 246g | 23 | 4.6m g (3.3m r) | 2.3m g (1.7m r) | 56g (40r) | 28g (20r) | 12g (9r) |
| `spaba2` | Barracks, 18th century | 5625g | 26 | 105.9m g (75.7m r) | 53.0m g (37.8m r) | 21.2m g (15.1m r) | 10.6m g (7.6m r) | 4.1m g (2.9m r) |
| `spabar` | Barracks, 17th century | 94g | 18 | 1.8m g (1.3m r) | 53g (38r) | 21g (15r) | 11g (8r) | 6g (4r) |
| `spabla` | Blacksmith | 94g | 13 | 1.8m g (1.3m r) | 53g (38r) | 21g (15r) | 11g (8r) | 8g (6r) |
| `spacen` | Town Hall | 156g | 24 | 2.9m g (2.1m r) | 1.5m g (1.1m r) | 35g (25r) | 18g (13r) | 7g (5r) |
| `spadip` | Diplomatic Center | 312g | 21 | 5.9m g (4.2m r) | 2.9m g (2.1m r) | 1.2m g (0.8m r) | 35g (25r) | 17g (12r) |
| `spahou` | Housing | 31g | 14 | 35g (25r) | 18g (13r) | 7g (5r) | 4g (3r) | 3g (2r) |
| `spamar` | Market | 156g | 24 | 2.9m g (2.1m r) | 1.5m g (1.1m r) | 35g (25r) | 18g (13r) | 7g (5r) |
| `spasta` | Stable | 625g | 21 | 11.8m g (8.4m r) | 5.9m g (4.2m r) | 2.4m g (1.7m r) | 1.2m g (0.8m r) | 34g (24r) |
| `spasto` | Storehouse | 31g | 7 | 35g (25r) | 18g (13r) | 7g (5r) | 5g (4r) | 5g (4r) |
| `spatem` | Cathedral | 156g | 30 | 2.9m g (2.1m r) | 1.5m g (1.1m r) | 35g (25r) | 18g (13r) | 6g (4r) |
| `ukrwga` | Gate | 6g | 13 | 6g (5r) | 3g (2r) | 1g (1r) | 1g (0r) | 0g (0r) |
| `ukrwwa` | Palisade | 6g | 4 | 6g (5r) | 3g (2r) | 2g (1r) | 2g (1r) | 2g (1r) |

<a id="полный-ремонт-0--max-hp-14"></a>
<a id="полный-ремонт-15"></a>
### Full repair (0 → max HP)

| sid | name | maxhp | slot_cap | 1 is building. | 2 is building. | 5 is building. | 10 is building. | Max. builds. |
|---|---|---|---|---|---|---|---|---|
| `eurcoa` | Mine | 2500 | 16 | 51g (36r) | 25g (18r) | 10g (7r) | 5g (4r) | 3g (2r) |
| `eurgol` | Mine | 2500 | 16 | 51g (36r) | 25g (18r) | 10g (7r) | 5g (4r) | 3g (2r) |
| `euriro` | Mine | 2500 | 16 | 51g (36r) | 25g (18r) | 10g (7r) | 5g (4r) | 3g (2r) |
| `eurmil` | Mill | 20000 | 10 | 6.8m g (4.8m r) | 3.4m g (2.4m r) | 1.4m g (1.0m r) | 41g (29r) | 41g (29r) |
| `eurpor` | Shipyard | 50000 | 30 | 16.9m g (12.1m r) | 8.5m g (6.0m r) | 3.4m g (2.4m r) | 1.7m g (1.2m r) | 34g (24r) |
| `eursga` | Gate | 32000 | 13 | 10.8m g (7.7m r) | 5.4m g (3.9m r) | 2.2m g (1.5m r) | 1.1m g (0.8m r) | 50g (36r) |
| `eurswa` | Wall | 50000 | 4 | 16.9m g (12.1m r) | 8.5m g (6.0m r) | 4.2m g (3.0m r) | 4.2m g (3.0m r) | 4.2m g (3.0m r) |
| `eurtow` | Tower | 20000 | 10 | 6.8m g (4.8m r) | 3.4m g (2.4m r) | 1.4m g (1.0m r) | 41g (29r) | 41g (29r) |
| `spaaca` | Academy | 63000 | 26 | 21.3m g (15.2m r) | 10.7m g (7.6m r) | 4.3m g (3.0m r) | 2.1m g (1.5m r) | 49g (35r) |
| `spaart` | Artillery Depot | 40000 | 23 | 13.5m g (9.7m r) | 6.8m g (4.8m r) | 2.7m g (1.9m r) | 1.4m g (1.0m r) | 35g (25r) |
| `spaba2` | Barracks, 18th century | 55000 | 26 | 18.6m g (13.3m r) | 9.3m g (6.6m r) | 3.7m g (2.7m r) | 1.9m g (1.3m r) | 43g (31r) |
| `spabar` | Barracks, 17th century | 40000 | 18 | 13.5m g (9.7m r) | 6.8m g (4.8m r) | 2.7m g (1.9m r) | 1.4m g (1.0m r) | 45g (32r) |
| `spabla` | Blacksmith | 5500 | 13 | 1.9m g (1.3m r) | 56g (40r) | 22g (16r) | 11g (8r) | 9g (6r) |
| `spacen` | Town Hall | 4250 | 24 | 1.4m g (1.0m r) | 43g (31r) | 17g (12r) | 9g (6r) | 4g (3r) |
| `spadip` | Diplomatic Center | 4500 | 21 | 1.5m g (1.1m r) | 46g (33r) | 18g (13r) | 9g (7r) | 4g (3r) |
| `spahou` | Housing | 4200 | 14 | 1.4m g (1.0m r) | 43g (30r) | 17g (12r) | 9g (6r) | 6g (4r) |
| `spamar` | Market | 4000 | 24 | 1.4m g (1.0m r) | 41g (29r) | 16g (12r) | 8g (6r) | 3g (2r) |
| `spasta` | Stable | 20000 | 21 | 6.8m g (4.8m r) | 3.4m g (2.4m r) | 1.4m g (1.0m r) | 41g (29r) | 19g (14r) |
| `spasto` | Storehouse | 10000 | 7 | 3.4m g (2.4m r) | 1.7m g (1.2m r) | 41g (29r) | 29g (21r) | 29g (21r) |
| `spatem` | Cathedral | 4200 | 30 | 1.4m g (1.0m r) | 43g (30r) | 17g (12r) | 9g (6r) | 3g (2r) |
| `ukrwga` | Gate | 1500 | 13 | 30g (22r) | 15g (11r) | 6g (4r) | 3g (2r) | 2g (2r) |
| `ukrwwa` | Palisade | 1500 | 4 | 30g (22r) | 15g (11r) | 8g (5r) | 8g (5r) | 8g (5r) |

<a id="swe--sweden-швеция"></a>
<a id="швеция-swe"></a>
## Sweden (`swe`)
<a id="постройка-с-нуля-16"></a>
### Building from scratch

| sid | name | buildtime_g | slot_cap | 1 is building. | 2 is building. | 5 is building. | 10 is building. | Max. builds. |
|---|---|---|---|---|---|---|---|---|
| `eurcoa` | Mine | 94g | 16 | 1.8m g (1.3m r) | 53g (38r) | 21g (15r) | 11g (8r) | 7g (5r) |
| `eurgol` | Mine | 94g | 16 | 1.8m g (1.3m r) | 53g (38r) | 21g (15r) | 11g (8r) | 7g (5r) |
| `euriro` | Mine | 94g | 16 | 1.8m g (1.3m r) | 53g (38r) | 21g (15r) | 11g (8r) | 7g (5r) |
| `eurmar` | Market | 234g | 25 | 4.4m g (3.2m r) | 2.2m g (1.6m r) | 53g (38r) | 26g (19r) | 11g (8r) |
| `eurmil` | Mill | 94g | 10 | 1.8m g (1.3m r) | 53g (38r) | 21g (15r) | 11g (8r) | 11g (8r) |
| `eurpor` | Shipyard | 1562g | 30 | 29.4m g (21.0m r) | 14.7m g (10.5m r) | 5.9m g (4.2m r) | 2.9m g (2.1m r) | 59g (42r) |
| `eursga` | Gate | 90g | 13 | 1.7m g (1.2m r) | 51g (36r) | 20g (15r) | 10g (7r) | 8g (6r) |
| `eursto` | Storehouse | 31g | 9 | 35g (25r) | 18g (13r) | 7g (5r) | 4g (3r) | 4g (3r) |
| `eurswa` | Wall | 90g | 4 | 1.7m g (1.2m r) | 51g (36r) | 25g (18r) | 25g (18r) | 25g (18r) |
| `eurtow` | Tower | 1230g | 10 | 23.2m g (16.6m r) | 11.6m g (8.3m r) | 4.6m g (3.3m r) | 2.3m g (1.7m r) | 2.3m g (1.7m r) |
| `sweaca` | Academy | 625g | 18 | 11.8m g (8.4m r) | 5.9m g (4.2m r) | 2.4m g (1.7m r) | 1.2m g (0.8m r) | 39g (28r) |
| `sweart` | Artillery Depot | 246g | 20 | 4.6m g (3.3m r) | 2.3m g (1.7m r) | 56g (40r) | 28g (20r) | 14g (10r) |
| `sweba2` | Barracks, 18th century | 5625g | 27 | 105.9m g (75.7m r) | 53.0m g (37.8m r) | 21.2m g (15.1m r) | 10.6m g (7.6m r) | 3.9m g (2.8m r) |
| `swebar` | Barracks, 17th century | 94g | 25 | 1.8m g (1.3m r) | 53g (38r) | 21g (15r) | 11g (8r) | 4g (3r) |
| `swebla` | Blacksmith | 94g | 16 | 1.8m g (1.3m r) | 53g (38r) | 21g (15r) | 11g (8r) | 7g (5r) |
| `swecen` | Town Hall | 156g | 27 | 2.9m g (2.1m r) | 1.5m g (1.1m r) | 35g (25r) | 18g (13r) | 7g (5r) |
| `swedip` | Diplomatic Center | 312g | 17 | 5.9m g (4.2m r) | 2.9m g (2.1m r) | 1.2m g (0.8m r) | 35g (25r) | 21g (15r) |
| `swehou` | Housing | 31g | 15 | 35g (25r) | 18g (13r) | 7g (5r) | 4g (3r) | 2g (2r) |
| `swesta` | Stable | 625g | 21 | 11.8m g (8.4m r) | 5.9m g (4.2m r) | 2.4m g (1.7m r) | 1.2m g (0.8m r) | 34g (24r) |
| `swetem` | Cathedral | 156g | 23 | 2.9m g (2.1m r) | 1.5m g (1.1m r) | 35g (25r) | 18g (13r) | 8g (5r) |
| `ukrwga` | Gate | 6g | 13 | 6g (5r) | 3g (2r) | 1g (1r) | 1g (0r) | 0g (0r) |
| `ukrwwa` | Palisade | 6g | 4 | 6g (5r) | 3g (2r) | 2g (1r) | 2g (1r) | 2g (1r) |

<a id="полный-ремонт-0--max-hp-15"></a>
<a id="полный-ремонт-16"></a>
### Full repair (0 → max HP)

| sid | name | maxhp | slot_cap | 1 is building. | 2 is building. | 5 is building. | 10 is building. | Max. builds. |
|---|---|---|---|---|---|---|---|---|
| `eurcoa` | Mine | 2500 | 16 | 51g (36r) | 25g (18r) | 10g (7r) | 5g (4r) | 3g (2r) |
| `eurgol` | Mine | 2500 | 16 | 51g (36r) | 25g (18r) | 10g (7r) | 5g (4r) | 3g (2r) |
| `euriro` | Mine | 2500 | 16 | 51g (36r) | 25g (18r) | 10g (7r) | 5g (4r) | 3g (2r) |
| `eurmar` | Market | 4000 | 25 | 1.4m g (1.0m r) | 41g (29r) | 16g (12r) | 8g (6r) | 3g (2r) |
| `eurmil` | Mill | 20000 | 10 | 6.8m g (4.8m r) | 3.4m g (2.4m r) | 1.4m g (1.0m r) | 41g (29r) | 41g (29r) |
| `eurpor` | Shipyard | 50000 | 30 | 16.9m g (12.1m r) | 8.5m g (6.0m r) | 3.4m g (2.4m r) | 1.7m g (1.2m r) | 34g (24r) |
| `eursga` | Gate | 32000 | 13 | 10.8m g (7.7m r) | 5.4m g (3.9m r) | 2.2m g (1.5m r) | 1.1m g (0.8m r) | 50g (36r) |
| `eursto` | Storehouse | 10000 | 9 | 3.4m g (2.4m r) | 1.7m g (1.2m r) | 41g (29r) | 23g (16r) | 23g (16r) |
| `eurswa` | Wall | 50000 | 4 | 16.9m g (12.1m r) | 8.5m g (6.0m r) | 4.2m g (3.0m r) | 4.2m g (3.0m r) | 4.2m g (3.0m r) |
| `eurtow` | Tower | 20000 | 10 | 6.8m g (4.8m r) | 3.4m g (2.4m r) | 1.4m g (1.0m r) | 41g (29r) | 41g (29r) |
| `sweaca` | Academy | 63000 | 18 | 21.3m g (15.2m r) | 10.7m g (7.6m r) | 4.3m g (3.0m r) | 2.1m g (1.5m r) | 1.2m g (0.8m r) |
| `sweart` | Artillery Depot | 40000 | 20 | 13.5m g (9.7m r) | 6.8m g (4.8m r) | 2.7m g (1.9m r) | 1.4m g (1.0m r) | 41g (29r) |
| `sweba2` | Barracks, 18th century | 55000 | 27 | 18.6m g (13.3m r) | 9.3m g (6.6m r) | 3.7m g (2.7m r) | 1.9m g (1.3m r) | 41g (30r) |
| `swebar` | Barracks, 17th century | 40000 | 25 | 13.5m g (9.7m r) | 6.8m g (4.8m r) | 2.7m g (1.9m r) | 1.4m g (1.0m r) | 32g (23r) |
| `swebla` | Blacksmith | 5500 | 16 | 1.9m g (1.3m r) | 56g (40r) | 22g (16r) | 11g (8r) | 7g (5r) |
| `swecen` | Town Hall | 5000 | 27 | 1.7m g (1.2m r) | 51g (36r) | 20g (15r) | 10g (7r) | 4g (3r) |
| `swedip` | Diplomatic Center | 4500 | 17 | 1.5m g (1.1m r) | 46g (33r) | 18g (13r) | 9g (7r) | 5g (4r) |
| `swehou` | Housing | 5000 | 15 | 1.7m g (1.2m r) | 51g (36r) | 20g (15r) | 10g (7r) | 7g (5r) |
| `swesta` | Stable | 20000 | 21 | 6.8m g (4.8m r) | 3.4m g (2.4m r) | 1.4m g (1.0m r) | 41g (29r) | 19g (14r) |
| `swetem` | Cathedral | 4200 | 23 | 1.4m g (1.0m r) | 43g (30r) | 17g (12r) | 9g (6r) | 4g (3r) |
| `ukrwga` | Gate | 1500 | 13 | 30g (22r) | 15g (11r) | 6g (4r) | 3g (2r) | 2g (2r) |
| `ukrwwa` | Palisade | 1500 | 4 | 30g (22r) | 15g (11r) | 8g (5r) | 8g (5r) | 8g (5r) |

<a id="swi--switzerland-швейцария"></a>
<a id="швейцария-swi"></a>
## Switzerland (`swi`)
<a id="постройка-с-нуля-17"></a>
### Building from scratch

| sid | name | buildtime_g | slot_cap | 1 is building. | 2 is building. | 5 is building. | 10 is building. | Max. builds. |
|---|---|---|---|---|---|---|---|---|
| `eurcoa` | Mine | 94g | 16 | 1.8m g (1.3m r) | 53g (38r) | 21g (15r) | 11g (8r) | 7g (5r) |
| `eurgol` | Mine | 94g | 16 | 1.8m g (1.3m r) | 53g (38r) | 21g (15r) | 11g (8r) | 7g (5r) |
| `euriro` | Mine | 94g | 16 | 1.8m g (1.3m r) | 53g (38r) | 21g (15r) | 11g (8r) | 7g (5r) |
| `eurmar` | Market | 234g | 25 | 4.4m g (3.2m r) | 2.2m g (1.6m r) | 53g (38r) | 26g (19r) | 11g (8r) |
| `eurmil` | Mill | 94g | 10 | 1.8m g (1.3m r) | 53g (38r) | 21g (15r) | 11g (8r) | 11g (8r) |
| `eurpor` | Shipyard | 1562g | 30 | 29.4m g (21.0m r) | 14.7m g (10.5m r) | 5.9m g (4.2m r) | 2.9m g (2.1m r) | 59g (42r) |
| `eursga` | Gate | 90g | 13 | 1.7m g (1.2m r) | 51g (36r) | 20g (15r) | 10g (7r) | 8g (6r) |
| `eursto` | Storehouse | 31g | 9 | 35g (25r) | 18g (13r) | 7g (5r) | 4g (3r) | 4g (3r) |
| `eurswa` | Wall | 90g | 4 | 1.7m g (1.2m r) | 51g (36r) | 25g (18r) | 25g (18r) | 25g (18r) |
| `eurtow` | Tower | 1230g | 10 | 23.2m g (16.6m r) | 11.6m g (8.3m r) | 4.6m g (3.3m r) | 2.3m g (1.7m r) | 2.3m g (1.7m r) |
| `swiaca` | Academy | 625g | 22 | 11.8m g (8.4m r) | 5.9m g (4.2m r) | 2.4m g (1.7m r) | 1.2m g (0.8m r) | 32g (23r) |
| `swiart` | Artillery Depot | 246g | 20 | 4.6m g (3.3m r) | 2.3m g (1.7m r) | 56g (40r) | 28g (20r) | 14g (10r) |
| `swiba2` | Barracks, 18th century | 5625g | 22 | 105.9m g (75.7m r) | 53.0m g (37.8m r) | 21.2m g (15.1m r) | 10.6m g (7.6m r) | 4.8m g (3.4m r) |
| `swibar` | Barracks, 17th century | 94g | 23 | 1.8m g (1.3m r) | 53g (38r) | 21g (15r) | 11g (8r) | 5g (3r) |
| `swibla` | Blacksmith | 94g | 17 | 1.8m g (1.3m r) | 53g (38r) | 21g (15r) | 11g (8r) | 6g (4r) |
| `swicen` | Town Hall | 156g | 23 | 2.9m g (2.1m r) | 1.5m g (1.1m r) | 35g (25r) | 18g (13r) | 8g (5r) |
| `swidip` | Diplomatic Center | 312g | 18 | 5.9m g (4.2m r) | 2.9m g (2.1m r) | 1.2m g (0.8m r) | 35g (25r) | 20g (14r) |
| `swihou` | Housing | 31g | 11 | 35g (25r) | 18g (13r) | 7g (5r) | 4g (3r) | 3g (2r) |
| `swista` | Stable | 625g | 18 | 11.8m g (8.4m r) | 5.9m g (4.2m r) | 2.4m g (1.7m r) | 1.2m g (0.8m r) | 39g (28r) |
| `switem` | Cathedral | 156g | 21 | 2.9m g (2.1m r) | 1.5m g (1.1m r) | 35g (25r) | 18g (13r) | 8g (6r) |
| `ukrwga` | Gate | 6g | 13 | 6g (5r) | 3g (2r) | 1g (1r) | 1g (0r) | 0g (0r) |
| `ukrwwa` | Palisade | 6g | 4 | 6g (5r) | 3g (2r) | 2g (1r) | 2g (1r) | 2g (1r) |

<a id="полный-ремонт-0--max-hp-16"></a>
<a id="полный-ремонт-17"></a>
### Full repair (0 → max HP)

| sid | name | maxhp | slot_cap | 1 is building. | 2 is building. | 5 is building. | 10 is building. | Max. builds. |
|---|---|---|---|---|---|---|---|---|
| `eurcoa` | Mine | 2500 | 16 | 51g (36r) | 25g (18r) | 10g (7r) | 5g (4r) | 3g (2r) |
| `eurgol` | Mine | 2500 | 16 | 51g (36r) | 25g (18r) | 10g (7r) | 5g (4r) | 3g (2r) |
| `euriro` | Mine | 2500 | 16 | 51g (36r) | 25g (18r) | 10g (7r) | 5g (4r) | 3g (2r) |
| `eurmar` | Market | 4000 | 25 | 1.4m g (1.0m r) | 41g (29r) | 16g (12r) | 8g (6r) | 3g (2r) |
| `eurmil` | Mill | 20000 | 10 | 6.8m g (4.8m r) | 3.4m g (2.4m r) | 1.4m g (1.0m r) | 41g (29r) | 41g (29r) |
| `eurpor` | Shipyard | 50000 | 30 | 16.9m g (12.1m r) | 8.5m g (6.0m r) | 3.4m g (2.4m r) | 1.7m g (1.2m r) | 34g (24r) |
| `eursga` | Gate | 32000 | 13 | 10.8m g (7.7m r) | 5.4m g (3.9m r) | 2.2m g (1.5m r) | 1.1m g (0.8m r) | 50g (36r) |
| `eursto` | Storehouse | 10000 | 9 | 3.4m g (2.4m r) | 1.7m g (1.2m r) | 41g (29r) | 23g (16r) | 23g (16r) |
| `eurswa` | Wall | 50000 | 4 | 16.9m g (12.1m r) | 8.5m g (6.0m r) | 4.2m g (3.0m r) | 4.2m g (3.0m r) | 4.2m g (3.0m r) |
| `eurtow` | Tower | 20000 | 10 | 6.8m g (4.8m r) | 3.4m g (2.4m r) | 1.4m g (1.0m r) | 41g (29r) | 41g (29r) |
| `swiaca` | Academy | 63000 | 22 | 21.3m g (15.2m r) | 10.7m g (7.6m r) | 4.3m g (3.0m r) | 2.1m g (1.5m r) | 58g (42r) |
| `swiart` | Artillery Depot | 40000 | 20 | 13.5m g (9.7m r) | 6.8m g (4.8m r) | 2.7m g (1.9m r) | 1.4m g (1.0m r) | 41g (29r) |
| `swiba2` | Barracks, 18th century | 55000 | 22 | 18.6m g (13.3m r) | 9.3m g (6.6m r) | 3.7m g (2.7m r) | 1.9m g (1.3m r) | 51g (36r) |
| `swibar` | Barracks, 17th century | 40000 | 23 | 13.5m g (9.7m r) | 6.8m g (4.8m r) | 2.7m g (1.9m r) | 1.4m g (1.0m r) | 35g (25r) |
| `swibla` | Blacksmith | 5500 | 17 | 1.9m g (1.3m r) | 56g (40r) | 22g (16r) | 11g (8r) | 7g (5r) |
| `swicen` | Town Hall | 4000 | 23 | 1.4m g (1.0m r) | 41g (29r) | 16g (12r) | 8g (6r) | 4g (3r) |
| `swidip` | Diplomatic Center | 4500 | 18 | 1.5m g (1.1m r) | 46g (33r) | 18g (13r) | 9g (7r) | 5g (4r) |
| `swihou` | Housing | 4000 | 11 | 1.4m g (1.0m r) | 41g (29r) | 16g (12r) | 8g (6r) | 7g (5r) |
| `swista` | Stable | 20000 | 18 | 6.8m g (4.8m r) | 3.4m g (2.4m r) | 1.4m g (1.0m r) | 41g (29r) | 23g (16r) |
| `switem` | Cathedral | 4200 | 21 | 1.4m g (1.0m r) | 43g (30r) | 17g (12r) | 9g (6r) | 4g (3r) |
| `ukrwga` | Gate | 1500 | 13 | 30g (22r) | 15g (11r) | 6g (4r) | 3g (2r) | 2g (2r) |
| `ukrwwa` | Palisade | 1500 | 4 | 30g (22r) | 15g (11r) | 8g (5r) | 8g (5r) | 8g (5r) |

<a id="tur--turkey-турция"></a>
<a id="турция-tur"></a>
## Turkey (`tur`)
<a id="постройка-с-нуля-18"></a>
### Building from scratch

| sid | name | buildtime_g | slot_cap | 1 is building. | 2 is building. | 5 is building. | 10 is building. | Max. builds. |
|---|---|---|---|---|---|---|---|---|
| `eurcoa` | Mine | 94g | 16 | 1.8m g (1.3m r) | 53g (38r) | 21g (15r) | 11g (8r) | 7g (5r) |
| `eurgol` | Mine | 94g | 16 | 1.8m g (1.3m r) | 53g (38r) | 21g (15r) | 11g (8r) | 7g (5r) |
| `euriro` | Mine | 94g | 16 | 1.8m g (1.3m r) | 53g (38r) | 21g (15r) | 11g (8r) | 7g (5r) |
| `turaca` | Minaret | 156g | 6 | 2.9m g (2.1m r) | 1.5m g (1.1m r) | 35g (25r) | 29g (21r) | 29g (21r) |
| `turart` | Artillery Depot | 246g | 28 | 4.6m g (3.3m r) | 2.3m g (1.7m r) | 56g (40r) | 28g (20r) | 10g (7r) |
| `turbar` | Barracks | 94g | 22 | 1.8m g (1.3m r) | 53g (38r) | 21g (15r) | 11g (8r) | 5g (3r) |
| `turbla` | Blacksmith | 109g | 15 | 2.1m g (1.5m r) | 1.0m g (0.7m r) | 25g (18r) | 12g (9r) | 8g (6r) |
| `turcen` | Town Hall | 156g | 22 | 2.9m g (2.1m r) | 1.5m g (1.1m r) | 35g (25r) | 18g (13r) | 8g (6r) |
| `turdip` | Diplomatic Center | 312g | 22 | 5.9m g (4.2m r) | 2.9m g (2.1m r) | 1.2m g (0.8m r) | 35g (25r) | 16g (11r) |
| `turhou` | Housing | 31g | 14 | 35g (25r) | 18g (13r) | 7g (5r) | 4g (3r) | 3g (2r) |
| `turmar` | Bazaar | 234g | 19 | 4.4m g (3.2m r) | 2.2m g (1.6m r) | 53g (38r) | 26g (19r) | 14g (10r) |
| `turmil` | Mill | 94g | 16 | 1.8m g (1.3m r) | 53g (38r) | 21g (15r) | 11g (8r) | 7g (5r) |
| `turpor` | Shipyard | 1562g | 30 | 29.4m g (21.0m r) | 14.7m g (10.5m r) | 5.9m g (4.2m r) | 2.9m g (2.1m r) | 59g (42r) |
| `tursga` | Gate | 120g | 13 | 2.3m g (1.6m r) | 1.1m g (0.8m r) | 27g (19r) | 14g (10r) | 10g (7r) |
| `tursta` | Stable | 156g | 25 | 2.9m g (2.1m r) | 1.5m g (1.1m r) | 35g (25r) | 18g (13r) | 7g (5r) |
| `tursto` | Storehouse | 31g | 8 | 35g (25r) | 18g (13r) | 7g (5r) | 4g (3r) | 4g (3r) |
| `turswa` | Wall | 120g | 4 | 2.3m g (1.6m r) | 1.1m g (0.8m r) | 34g (24r) | 34g (24r) | 34g (24r) |
| `turtem` | Mosque | 94g | 22 | 1.8m g (1.3m r) | 53g (38r) | 21g (15r) | 11g (8r) | 5g (3r) |
| `turtow` | Tower | 984g | 14 | 18.5m g (13.2m r) | 9.3m g (6.6m r) | 3.7m g (2.6m r) | 1.9m g (1.3m r) | 1.3m g (0.9m r) |
| `ukrwga` | Gate | 6g | 13 | 6g (5r) | 3g (2r) | 1g (1r) | 1g (0r) | 0g (0r) |
| `ukrwwa` | Palisade | 6g | 4 | 6g (5r) | 3g (2r) | 2g (1r) | 2g (1r) | 2g (1r) |

<a id="полный-ремонт-0--max-hp-17"></a>
<a id="полный-ремонт-18"></a>
### Full repair (0 → max HP)

| sid | name | maxhp | slot_cap | 1 is building. | 2 is building. | 5 is building. | 10 is building. | Max. builds. |
|---|---|---|---|---|---|---|---|---|
| `eurcoa` | Mine | 2500 | 16 | 51g (36r) | 25g (18r) | 10g (7r) | 5g (4r) | 3g (2r) |
| `eurgol` | Mine | 2500 | 16 | 51g (36r) | 25g (18r) | 10g (7r) | 5g (4r) | 3g (2r) |
| `euriro` | Mine | 2500 | 16 | 51g (36r) | 25g (18r) | 10g (7r) | 5g (4r) | 3g (2r) |
| `turaca` | Minaret | 65000 | 6 | 22.0m g (15.7m r) | 11.0m g (7.9m r) | 4.4m g (3.1m r) | 3.7m g (2.6m r) | 3.7m g (2.6m r) |
| `turart` | Artillery Depot | 40000 | 28 | 13.5m g (9.7m r) | 6.8m g (4.8m r) | 2.7m g (1.9m r) | 1.4m g (1.0m r) | 29g (21r) |
| `turbar` | Barracks | 35000 | 22 | 11.8m g (8.5m r) | 5.9m g (4.2m r) | 2.4m g (1.7m r) | 1.2m g (0.8m r) | 32g (23r) |
| `turbla` | Blacksmith | 6500 | 15 | 2.2m g (1.6m r) | 1.1m g (0.8m r) | 26g (19r) | 13g (9r) | 9g (6r) |
| `turcen` | Town Hall | 4000 | 22 | 1.4m g (1.0m r) | 41g (29r) | 16g (12r) | 8g (6r) | 4g (3r) |
| `turdip` | Diplomatic Center | 5500 | 22 | 1.9m g (1.3m r) | 56g (40r) | 22g (16r) | 11g (8r) | 5g (4r) |
| `turhou` | Housing | 4000 | 14 | 1.4m g (1.0m r) | 41g (29r) | 16g (12r) | 8g (6r) | 6g (4r) |
| `turmar` | Bazaar | 4500 | 19 | 1.5m g (1.1m r) | 46g (33r) | 18g (13r) | 9g (7r) | 5g (3r) |
| `turmil` | Mill | 20000 | 16 | 6.8m g (4.8m r) | 3.4m g (2.4m r) | 1.4m g (1.0m r) | 41g (29r) | 25g (18r) |
| `turpor` | Shipyard | 40000 | 30 | 13.5m g (9.7m r) | 6.8m g (4.8m r) | 2.7m g (1.9m r) | 1.4m g (1.0m r) | 27g (19r) |
| `tursga` | Gate | 32000 | 13 | 10.8m g (7.7m r) | 5.4m g (3.9m r) | 2.2m g (1.5m r) | 1.1m g (0.8m r) | 50g (36r) |
| `tursta` | Stable | 55000 | 25 | 18.6m g (13.3m r) | 9.3m g (6.6m r) | 3.7m g (2.7m r) | 1.9m g (1.3m r) | 45g (32r) |
| `tursto` | Storehouse | 10000 | 8 | 3.4m g (2.4m r) | 1.7m g (1.2m r) | 41g (29r) | 25g (18r) | 25g (18r) |
| `turswa` | Wall | 50000 | 4 | 16.9m g (12.1m r) | 8.5m g (6.0m r) | 4.2m g (3.0m r) | 4.2m g (3.0m r) | 4.2m g (3.0m r) |
| `turtem` | Mosque | 5000 | 22 | 1.7m g (1.2m r) | 51g (36r) | 20g (15r) | 10g (7r) | 5g (3r) |
| `turtow` | Tower | 22500 | 14 | 7.6m g (5.4m r) | 3.8m g (2.7m r) | 1.5m g (1.1m r) | 46g (33r) | 33g (23r) |
| `ukrwga` | Gate | 1500 | 13 | 30g (22r) | 15g (11r) | 6g (4r) | 3g (2r) | 2g (2r) |
| `ukrwwa` | Palisade | 1500 | 4 | 30g (22r) | 15g (11r) | 8g (5r) | 8g (5r) | 8g (5r) |

<a id="ukr--ukraine-украина"></a>
<a id="украина-ukr"></a>
## Ukraine (`ukr`)
<a id="постройка-с-нуля-19"></a>
### Building from scratch

| sid | name | buildtime_g | slot_cap | 1 is building. | 2 is building. | 5 is building. | 10 is building. | Max. builds. |
|---|---|---|---|---|---|---|---|---|
| `eurcoa` | Mine | 94g | 16 | 1.8m g (1.3m r) | 53g (38r) | 21g (15r) | 11g (8r) | 7g (5r) |
| `eurgol` | Mine | 94g | 16 | 1.8m g (1.3m r) | 53g (38r) | 21g (15r) | 11g (8r) | 7g (5r) |
| `euriro` | Mine | 94g | 16 | 1.8m g (1.3m r) | 53g (38r) | 21g (15r) | 11g (8r) | 7g (5r) |
| `rusmar` | Market | 234g | 23 | 4.4m g (3.2m r) | 2.2m g (1.6m r) | 53g (38r) | 26g (19r) | 12g (8r) |
| `rusmil` | Mill | 94g | 7 | 1.8m g (1.3m r) | 53g (38r) | 21g (15r) | 15g (11r) | 15g (11r) |
| `russto` | Storehouse | 31g | 8 | 35g (25r) | 18g (13r) | 7g (5r) | 4g (3r) | 4g (3r) |
| `ukraca` | Academy | 47g | 30 | 53g (38r) | 26g (19r) | 11g (8r) | 5g (4r) | 2g (1r) |
| `ukrart` | Artillery Depot | 246g | 30 | 4.6m g (3.3m r) | 2.3m g (1.7m r) | 56g (40r) | 28g (20r) | 9g (7r) |
| `ukrbar` | Cossack House | 94g | 23 | 1.8m g (1.3m r) | 53g (38r) | 21g (15r) | 11g (8r) | 5g (3r) |
| `ukrbla` | Blacksmith | 62g | 19 | 1.2m g (0.8m r) | 35g (25r) | 14g (10r) | 7g (5r) | 4g (3r) |
| `ukrcen` | Town Hall | 156g | 29 | 2.9m g (2.1m r) | 1.5m g (1.1m r) | 35g (25r) | 18g (13r) | 6g (4r) |
| `ukrdip` | Diplomatic Center | 312g | 22 | 5.9m g (4.2m r) | 2.9m g (2.1m r) | 1.2m g (0.8m r) | 35g (25r) | 16g (11r) |
| `ukrhou` | Hut | 31g | 16 | 35g (25r) | 18g (13r) | 7g (5r) | 4g (3r) | 2g (2r) |
| `ukrpor` | Shipyard | 1562g | 30 | 29.4m g (21.0m r) | 14.7m g (10.5m r) | 5.9m g (4.2m r) | 2.9m g (2.1m r) | 59g (42r) |
| `ukrsta` | Stable | 156g | 26 | 2.9m g (2.1m r) | 1.5m g (1.1m r) | 35g (25r) | 18g (13r) | 7g (5r) |
| `ukrtem` | Orthodox Cathedral | 156g | 30 | 2.9m g (2.1m r) | 1.5m g (1.1m r) | 35g (25r) | 18g (13r) | 6g (4r) |
| `ukrwga` | Gate | 8g | 13 | 9g (7r) | 5g (3r) | 2g (1r) | 1g (1r) | 1g (1r) |
| `ukrwwa` | Palisade | 8g | 4 | 9g (7r) | 5g (3r) | 2g (2r) | 2g (2r) | 2g (2r) |

<a id="полный-ремонт-0--max-hp-18"></a>
<a id="полный-ремонт-19"></a>
### Full repair (0 → max HP)

| sid | name | maxhp | slot_cap | 1 is building. | 2 is building. | 5 is building. | 10 is building. | Max. builds. |
|---|---|---|---|---|---|---|---|---|
| `eurcoa` | Mine | 2500 | 16 | 51g (36r) | 25g (18r) | 10g (7r) | 5g (4r) | 3g (2r) |
| `eurgol` | Mine | 2500 | 16 | 51g (36r) | 25g (18r) | 10g (7r) | 5g (4r) | 3g (2r) |
| `euriro` | Mine | 2500 | 16 | 51g (36r) | 25g (18r) | 10g (7r) | 5g (4r) | 3g (2r) |
| `rusmar` | Market | 4000 | 23 | 1.4m g (1.0m r) | 41g (29r) | 16g (12r) | 8g (6r) | 4g (3r) |
| `rusmil` | Mill | 15000 | 7 | 5.1m g (3.6m r) | 2.5m g (1.8m r) | 1.0m g (0.7m r) | 44g (31r) | 44g (31r) |
| `russto` | Storehouse | 10000 | 8 | 3.4m g (2.4m r) | 1.7m g (1.2m r) | 41g (29r) | 25g (18r) | 25g (18r) |
| `ukraca` | Academy | 65000 | 30 | 22.0m g (15.7m r) | 11.0m g (7.9m r) | 4.4m g (3.1m r) | 2.2m g (1.6m r) | 44g (31r) |
| `ukrart` | Artillery Depot | 40000 | 30 | 13.5m g (9.7m r) | 6.8m g (4.8m r) | 2.7m g (1.9m r) | 1.4m g (1.0m r) | 27g (19r) |
| `ukrbar` | Cossack House | 20000 | 23 | 6.8m g (4.8m r) | 3.4m g (2.4m r) | 1.4m g (1.0m r) | 41g (29r) | 18g (13r) |
| `ukrbla` | Blacksmith | 4500 | 19 | 1.5m g (1.1m r) | 46g (33r) | 18g (13r) | 9g (7r) | 5g (3r) |
| `ukrcen` | Town Hall | 5300 | 29 | 1.8m g (1.3m r) | 54g (38r) | 22g (15r) | 11g (8r) | 4g (3r) |
| `ukrdip` | Diplomatic Center | 5000 | 22 | 1.7m g (1.2m r) | 51g (36r) | 20g (15r) | 10g (7r) | 5g (3r) |
| `ukrhou` | Hut | 4150 | 16 | 1.4m g (1.0m r) | 42g (30r) | 17g (12r) | 8g (6r) | 5g (4r) |
| `ukrpor` | Shipyard | 45000 | 30 | 15.2m g (10.9m r) | 7.6m g (5.4m r) | 3.0m g (2.2m r) | 1.5m g (1.1m r) | 30g (22r) |
| `ukrsta` | Stable | 10000 | 26 | 3.4m g (2.4m r) | 1.7m g (1.2m r) | 41g (29r) | 20g (15r) | 8g (6r) |
| `ukrtem` | Orthodox Cathedral | 5300 | 30 | 1.8m g (1.3m r) | 54g (38r) | 22g (15r) | 11g (8r) | 4g (3r) |
| `ukrwga` | Gate | 2500 | 13 | 51g (36r) | 25g (18r) | 10g (7r) | 5g (4r) | 4g (3r) |
| `ukrwwa` | Palisade | 2500 | 4 | 51g (36r) | 25g (18r) | 13g (9r) | 13g (9r) | 13g (9r) |

<a id="ven--venice-венеция"></a>
<a id="венеция-ven"></a>
## Venice (`ven`)
<a id="постройка-с-нуля-20"></a>
### Building from scratch

| sid | name | buildtime_g | slot_cap | 1 is building. | 2 is building. | 5 is building. | 10 is building. | Max. builds. |
|---|---|---|---|---|---|---|---|---|
| `eurcoa` | Mine | 94g | 16 | 1.8m g (1.3m r) | 53g (38r) | 21g (15r) | 11g (8r) | 7g (5r) |
| `eurgol` | Mine | 94g | 16 | 1.8m g (1.3m r) | 53g (38r) | 21g (15r) | 11g (8r) | 7g (5r) |
| `euriro` | Mine | 94g | 16 | 1.8m g (1.3m r) | 53g (38r) | 21g (15r) | 11g (8r) | 7g (5r) |
| `eurmar` | Market | 234g | 25 | 4.4m g (3.2m r) | 2.2m g (1.6m r) | 53g (38r) | 26g (19r) | 11g (8r) |
| `eurmil` | Mill | 94g | 10 | 1.8m g (1.3m r) | 53g (38r) | 21g (15r) | 11g (8r) | 11g (8r) |
| `eurpor` | Shipyard | 1562g | 30 | 29.4m g (21.0m r) | 14.7m g (10.5m r) | 5.9m g (4.2m r) | 2.9m g (2.1m r) | 59g (42r) |
| `eursga` | Gate | 90g | 13 | 1.7m g (1.2m r) | 51g (36r) | 20g (15r) | 10g (7r) | 8g (6r) |
| `eursto` | Storehouse | 31g | 9 | 35g (25r) | 18g (13r) | 7g (5r) | 4g (3r) | 4g (3r) |
| `eurswa` | Wall | 90g | 4 | 1.7m g (1.2m r) | 51g (36r) | 25g (18r) | 25g (18r) | 25g (18r) |
| `eurtow` | Tower | 1230g | 10 | 23.2m g (16.6m r) | 11.6m g (8.3m r) | 4.6m g (3.3m r) | 2.3m g (1.7m r) | 2.3m g (1.7m r) |
| `ukrwga` | Gate | 6g | 13 | 6g (5r) | 3g (2r) | 1g (1r) | 1g (0r) | 0g (0r) |
| `ukrwwa` | Palisade | 6g | 4 | 6g (5r) | 3g (2r) | 2g (1r) | 2g (1r) | 2g (1r) |
| `venaca` | Academy | 625g | 22 | 11.8m g (8.4m r) | 5.9m g (4.2m r) | 2.4m g (1.7m r) | 1.2m g (0.8m r) | 32g (23r) |
| `venart` | Artillery Depot | 246g | 20 | 4.6m g (3.3m r) | 2.3m g (1.7m r) | 56g (40r) | 28g (20r) | 14g (10r) |
| `venba2` | Barracks, 18th century | 5625g | 19 | 105.9m g (75.7m r) | 53.0m g (37.8m r) | 21.2m g (15.1m r) | 10.6m g (7.6m r) | 5.6m g (4.0m r) |
| `venbar` | Barracks, 17th century | 94g | 23 | 1.8m g (1.3m r) | 53g (38r) | 21g (15r) | 11g (8r) | 5g (3r) |
| `venbla` | Blacksmith | 94g | 16 | 1.8m g (1.3m r) | 53g (38r) | 21g (15r) | 11g (8r) | 7g (5r) |
| `vencen` | Town Hall | 156g | 28 | 2.9m g (2.1m r) | 1.5m g (1.1m r) | 35g (25r) | 18g (13r) | 6g (5r) |
| `vendip` | Diplomatic Center | 312g | 18 | 5.9m g (4.2m r) | 2.9m g (2.1m r) | 1.2m g (0.8m r) | 35g (25r) | 20g (14r) |
| `venhou` | Housing | 31g | 10 | 35g (25r) | 18g (13r) | 7g (5r) | 4g (3r) | 4g (3r) |
| `vensta` | Stable | 625g | 19 | 11.8m g (8.4m r) | 5.9m g (4.2m r) | 2.4m g (1.7m r) | 1.2m g (0.8m r) | 37g (27r) |
| `ventem` | Cathedral | 156g | 30 | 2.9m g (2.1m r) | 1.5m g (1.1m r) | 35g (25r) | 18g (13r) | 6g (4r) |

<a id="полный-ремонт-0--max-hp-19"></a>
<a id="полный-ремонт-20"></a>
### Full repair (0 → max HP)

| sid | name | maxhp | slot_cap | 1 is building. | 2 is building. | 5 is building. | 10 is building. | Max. builds. |
|---|---|---|---|---|---|---|---|---|
| `eurcoa` | Mine | 2500 | 16 | 51g (36r) | 25g (18r) | 10g (7r) | 5g (4r) | 3g (2r) |
| `eurgol` | Mine | 2500 | 16 | 51g (36r) | 25g (18r) | 10g (7r) | 5g (4r) | 3g (2r) |
| `euriro` | Mine | 2500 | 16 | 51g (36r) | 25g (18r) | 10g (7r) | 5g (4r) | 3g (2r) |
| `eurmar` | Market | 4000 | 25 | 1.4m g (1.0m r) | 41g (29r) | 16g (12r) | 8g (6r) | 3g (2r) |
| `eurmil` | Mill | 20000 | 10 | 6.8m g (4.8m r) | 3.4m g (2.4m r) | 1.4m g (1.0m r) | 41g (29r) | 41g (29r) |
| `eurpor` | Shipyard | 50000 | 30 | 16.9m g (12.1m r) | 8.5m g (6.0m r) | 3.4m g (2.4m r) | 1.7m g (1.2m r) | 34g (24r) |
| `eursga` | Gate | 32000 | 13 | 10.8m g (7.7m r) | 5.4m g (3.9m r) | 2.2m g (1.5m r) | 1.1m g (0.8m r) | 50g (36r) |
| `eursto` | Storehouse | 10000 | 9 | 3.4m g (2.4m r) | 1.7m g (1.2m r) | 41g (29r) | 23g (16r) | 23g (16r) |
| `eurswa` | Wall | 50000 | 4 | 16.9m g (12.1m r) | 8.5m g (6.0m r) | 4.2m g (3.0m r) | 4.2m g (3.0m r) | 4.2m g (3.0m r) |
| `eurtow` | Tower | 20000 | 10 | 6.8m g (4.8m r) | 3.4m g (2.4m r) | 1.4m g (1.0m r) | 41g (29r) | 41g (29r) |
| `ukrwga` | Gate | 1500 | 13 | 30g (22r) | 15g (11r) | 6g (4r) | 3g (2r) | 2g (2r) |
| `ukrwwa` | Palisade | 1500 | 4 | 30g (22r) | 15g (11r) | 8g (5r) | 8g (5r) | 8g (5r) |
| `venaca` | Academy | 63000 | 22 | 21.3m g (15.2m r) | 10.7m g (7.6m r) | 4.3m g (3.0m r) | 2.1m g (1.5m r) | 58g (42r) |
| `venart` | Artillery Depot | 40000 | 20 | 13.5m g (9.7m r) | 6.8m g (4.8m r) | 2.7m g (1.9m r) | 1.4m g (1.0m r) | 41g (29r) |
| `venba2` | Barracks, 18th century | 55000 | 19 | 18.6m g (13.3m r) | 9.3m g (6.6m r) | 3.7m g (2.7m r) | 1.9m g (1.3m r) | 59g (42r) |
| `venbar` | Barracks, 17th century | 40000 | 23 | 13.5m g (9.7m r) | 6.8m g (4.8m r) | 2.7m g (1.9m r) | 1.4m g (1.0m r) | 35g (25r) |
| `venbla` | Blacksmith | 5500 | 16 | 1.9m g (1.3m r) | 56g (40r) | 22g (16r) | 11g (8r) | 7g (5r) |
| `vencen` | Town Hall | 5100 | 28 | 1.7m g (1.2m r) | 52g (37r) | 21g (15r) | 10g (7r) | 4g (3r) |
| `vendip` | Diplomatic Center | 4500 | 18 | 1.5m g (1.1m r) | 46g (33r) | 18g (13r) | 9g (7r) | 5g (4r) |
| `venhou` | Housing | 5000 | 10 | 1.7m g (1.2m r) | 51g (36r) | 20g (15r) | 10g (7r) | 10g (7r) |
| `vensta` | Stable | 20000 | 19 | 6.8m g (4.8m r) | 3.4m g (2.4m r) | 1.4m g (1.0m r) | 41g (29r) | 21g (15r) |
| `ventem` | Cathedral | 4200 | 30 | 1.4m g (1.0m r) | 43g (30r) | 17g (12r) | 9g (6r) | 3g (2r) |
