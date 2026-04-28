# 03. Здания

[← Index](README.md)

Здания делятся на **per-nation** (`<nat>+suffix`, например `auscen`) и **common** (`<cluster>+suffix`, общие для группы наций — `eur`/`rus`/`tur`/`spa`/`ukr`/`por`).

Цены ниже — для **первого** экземпляра. Цена N-го здания того же типа = `floor(base × (costpercent/100)^(N-1))`. **Готовые таблицы N=1..6 для всех зданий → [`derived/scaling_prices.md`](derived/scaling_prices.md)**.

**Производный документ** генерируется отдельным скриптом [`parser/compute_scaling.py`](../../parser/compute_scaling.py).

## Содержание

**[Per-nation здания](#per-nation-здания)**
  - [cen — Town Hall](#cen-—-town-hall)
  - [hou — Housing](#hou-—-housing)
  - [bar — Barracks 17c](#bar-—-barracks-17c)
  - [ba2 — Barracks 18c](#ba2-—-barracks-18c)
  - [bla — Blacksmith](#bla-—-blacksmith)
  - [sta — Stable](#sta-—-stable)
  - [tem — Cathedral](#tem-—-cathedral)
  - [aca — Academy](#aca-—-academy)
  - [art — Artillery Depot](#art-—-artillery-depot)
  - [dip — Diplomatic Center](#dip-—-diplomatic-center)
**[Common здания (по кластерам)](#common-здания-по-кластерам)**
  - [mil — Mill](#mil-—-mill)
  - [sto — Storehouse](#sto-—-storehouse)
  - [mar — Market](#mar-—-market)
  - [por — Shipyard](#por-—-shipyard)
  - [tow — Tower](#tow-—-tower)
  - [gol — Gold Mine](#gol-—-gold-mine)
  - [iro — Iron Mine](#iro-—-iron-mine)
  - [coa — Coal Mine](#coa-—-coal-mine)
  - [swa — Stone Wall](#swa-—-stone-wall)
  - [sga — Stone Gate](#sga-—-stone-gate)
**[Шахты — апгрейды (gol/iro/coa)](#шахты--апгрейды-goliroсoa)**

## Per-nation здания

Сводка: для каждого типа зданий — параметры по всем нациям (где они есть). **Жирным** — отклонения от baseline (mode of column).

### cen — Town Hall

| Здание | Нация | HP | Time (s) | cost% | F | W | S | G | I | C | farm | produces |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| **Town Hall** `algcen` | alg | **5500** | 156.25 | 300 | 0 | **450** | 700 | 0 | 0 | 0 | **50** | peaaus, peaeng, peapol, pearus, peasco (+3) |
| **Town Hall** `auscen` | aus | 4000 | **46.88** | 300 | 0 | 700 | 700 | 0 | 0 | 0 | 100 | peaaus, peaeng, peapol, pearus, peasco (+3) |
| **Town Hall** `bavcen` | bav | 4000 | 156.25 | 300 | 0 | 700 | 700 | 0 | 0 | 0 | 100 | peaaus, peaeng, peapol, pearus, peasco (+3) |
| **Town Hall** `dencen` | den | **4030** | 156.25 | 300 | 0 | 700 | 700 | 0 | 0 | 0 | 100 | peaaus, peaeng, peapol, pearus, peasco (+3) |
| **Town Hall** `engcen` | eng | **4030** | 156.25 | 300 | 0 | 700 | 700 | 0 | 0 | 0 | 100 | peaaus, peaeng, peapol, pearus, peasco (+3) |
| **Town Hall** `fracen` | fra | **4500** | 156.25 | 300 | 0 | 700 | 700 | 0 | 0 | 0 | 100 | peaaus, peaeng, peapol, pearus, peasco (+3) |
| **Town Hall** `huncen` | hun | 4000 | 156.25 | 300 | 0 | 700 | 700 | 0 | 0 | 0 | 100 | peaaus, peaeng, peapol, pearus, peasco (+3) |
| **Town Hall** `netcen` | net | **4950** | 156.25 | 300 | 0 | 700 | 700 | 0 | 0 | 0 | 100 | peaaus, peaeng, peapol, pearus, peasco (+3) |
| **Town Hall** `piecen` | pie | 4000 | 156.25 | 300 | 0 | 700 | 700 | 0 | 0 | 0 | 100 | peaaus, peaeng, peapol, pearus, peasco (+3) |
| **Town Hall** `polcen` | pol | **4300** | 156.25 | 300 | 0 | 700 | 700 | 0 | 0 | 0 | 100 | peaaus, peaeng, peapol, pearus, peasco (+3) |
| **Town Hall** `porcen` | por | 4000 | 156.25 | 300 | 0 | 700 | 700 | 0 | 0 | 0 | 100 | peaaus, peaeng, peapol, pearus, peasco (+3) |
| **Town Hall** `prucen` | pru | **4200** | 156.25 | 300 | 0 | 700 | 700 | 0 | 0 | 0 | 100 | peaaus, peaeng, peapol, pearus, peasco (+3) |
| **Town Hall** `ruscen` | rus | **4050** | 156.25 | 300 | 0 | **680** | 700 | 0 | 0 | 0 | **75** | peaaus, peaeng, peapol, pearus, peasco (+3) |
| **Town Hall** `saxcen` | sax | 4000 | 156.25 | 300 | 0 | 700 | 700 | 0 | 0 | 0 | 100 | peaaus, peaeng, peapol, pearus, peasco (+3) |
| **Town Hall** `scocen` | sco | 4000 | 156.25 | 300 | 0 | 700 | 700 | 0 | 0 | 0 | 100 | peaaus, peaeng, peapol, pearus, peasco (+3) |
| **Town Hall** `spacen` | spa | **4250** | 156.25 | 300 | 0 | 700 | 700 | 0 | 0 | 0 | 100 | peaaus, peaeng, peapol, pearus, peasco (+3) |
| **Town Hall** `swecen` | swe | **5000** | 156.25 | 300 | 0 | 700 | 700 | 0 | 0 | 0 | 100 | peaaus, peaeng, peapol, pearus, peasco (+3) |
| **Town Hall** `swicen` | swi | 4000 | 156.25 | 300 | 0 | 700 | 700 | 0 | 0 | 0 | 100 | peaaus, peaeng, peapol, pearus, peasco (+3) |
| **Town Hall** `turcen` | tur | 4000 | 156.25 | 300 | 0 | **600** | **500** | 0 | 0 | 0 | 100 | peaaus, peaeng, peapol, pearus, peasco (+3) |
| **Town Hall** `ukrcen` | ukr | **5300** | 156.25 | **400** | 0 | 700 | **0** | 0 | 0 | 0 | **200** | peaaus, peaeng, peapol, pearus, peasco (+3) |
| **Town Hall** `vencen` | ven | **5100** | 156.25 | 300 | 0 | 700 | 700 | 0 | 0 | 0 | 100 | peaaus, peaeng, peapol, pearus, peasco (+3) |

### hou — Housing

| Здание | Нация | HP | Time (s) | cost% | F | W | S | G | I | C | farm | produces |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| **Housing** `alghou` | alg | **4300** | 31.25 | 104 | 0 | 100 | 100 | 0 | 0 | 0 | 25 | — |
| **Housing** `aushou` | aus | 4000 | 31.25 | 104 | 0 | 100 | 100 | 0 | 0 | 0 | 25 | — |
| **Housing** `bavhou` | bav | 4000 | 31.25 | 104 | 0 | 100 | 100 | 0 | 0 | 0 | 25 | — |
| **Housing** `denhou` | den | 4000 | 31.25 | 104 | 0 | 100 | 100 | 0 | 0 | 0 | 25 | — |
| **Housing** `enghou` | eng | **5000** | 31.25 | 104 | 0 | 100 | 100 | 0 | 0 | 0 | 25 | — |
| **Housing** `frahou` | fra | 4000 | 31.25 | 104 | 0 | 100 | 100 | 0 | 0 | 0 | 25 | — |
| **Housing** `hunhou` | hun | 4000 | 31.25 | 104 | 0 | 100 | 100 | 0 | 0 | 0 | 25 | — |
| **Housing** `nethou` | net | **4500** | 31.25 | 104 | 0 | 100 | 100 | 0 | 0 | 0 | 25 | — |
| **Housing** `piehou` | pie | 4000 | 31.25 | 104 | 0 | 100 | 100 | 0 | 0 | 0 | 25 | — |
| **Housing** `polhou` | pol | **4100** | 31.25 | 104 | 0 | 100 | 100 | 0 | 0 | 0 | 25 | — |
| **Housing** `porhou` | por | 4000 | 31.25 | 104 | 0 | 100 | 100 | 0 | 0 | 0 | 25 | — |
| **Housing** `pruhou` | pru | **4500** | 31.25 | 104 | 0 | 100 | 100 | 0 | 0 | 0 | 25 | — |
| **Izba** `rushou` | rus | **5000** | 31.25 | 104 | 0 | **120** | **0** | 0 | 0 | 0 | 25 | — |
| **Housing** `saxhou` | sax | 4000 | 31.25 | 104 | 0 | 100 | 100 | 0 | 0 | 0 | 25 | — |
| **Housing** `scohou` | sco | 4000 | 31.25 | 104 | 0 | 100 | 100 | 0 | 0 | 0 | 25 | — |
| **Housing** `spahou` | spa | **4200** | 31.25 | 104 | 0 | 100 | 100 | 0 | 0 | 0 | 25 | — |
| **Housing** `swehou` | swe | **5000** | 31.25 | 104 | 0 | 100 | 100 | 0 | 0 | 0 | 25 | — |
| **Housing** `swihou` | swi | 4000 | 31.25 | 104 | 0 | 100 | 100 | 0 | 0 | 0 | 25 | — |
| **Housing** `turhou` | tur | 4000 | 31.25 | **106** | 0 | 100 | 100 | 0 | 0 | 0 | 25 | — |
| **Hut** `ukrhou` | ukr | **4150** | 31.25 | **105** | 0 | **120** | **0** | 0 | 0 | 0 | 25 | — |
| **Housing** `venhou` | ven | **5000** | 31.25 | 104 | 0 | 100 | 100 | 0 | 0 | 0 | 25 | — |

### bar — Barracks 17c

| Здание | Нация | HP | Time (s) | cost% | F | W | S | G | I | C | farm | produces |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| **Barracks** `algbar` | alg | **35000** | 93.75 | 500 | 0 | **400** | **400** | **0** | 0 | 0 | **50** | archer, archertur, drummer, drummerrus, drummertur (+24) |
| **Barracks, 17th century** `ausbar` | aus | 40000 | 93.75 | 500 | 0 | 100 | 100 | 500 | 0 | 0 | 150 | archer, archertur, drummer, drummerrus, drummertur (+24) |
| **Barracks, 17th century** `bavbar` | bav | 40000 | 93.75 | 500 | 0 | 100 | 100 | 500 | 0 | 0 | 150 | archer, archertur, drummer, drummerrus, drummertur (+24) |
| **Barracks, 17th century** `denbar` | den | 40000 | 93.75 | 500 | 0 | 100 | 100 | 500 | 0 | 0 | 150 | archer, archertur, drummer, drummerrus, drummertur (+24) |
| **Barracks, 17th century** `engbar` | eng | 40000 | 93.75 | 500 | 0 | 100 | 100 | 500 | 0 | 0 | 150 | archer, archertur, drummer, drummerrus, drummertur (+24) |
| **Barracks, 17th century** `frabar` | fra | 40000 | 93.75 | 500 | 0 | 100 | 100 | 500 | 0 | 0 | 150 | archer, archertur, drummer, drummerrus, drummertur (+24) |
| **Barracks, 17th century** `hunbar` | hun | 40000 | 93.75 | 500 | 0 | 100 | 100 | 500 | 0 | 0 | 150 | archer, archertur, drummer, drummerrus, drummertur (+24) |
| **Barracks, 17th century** `netbar` | net | 40000 | 93.75 | 500 | 0 | 100 | 100 | 500 | 0 | 0 | 150 | archer, archertur, drummer, drummerrus, drummertur (+24) |
| **Barracks, 17th century** `piebar` | pie | 40000 | 93.75 | 500 | 0 | 100 | 100 | 500 | 0 | 0 | 150 | archer, archertur, drummer, drummerrus, drummertur (+24) |
| **Barracks, 17th century** `polbar` | pol | 40000 | 93.75 | 500 | 0 | 100 | 100 | 500 | 0 | 0 | 150 | archer, archertur, drummer, drummerrus, drummertur (+24) |
| **Barracks, 17th century** `porbar` | por | 40000 | 93.75 | 500 | 0 | 100 | 100 | 500 | 0 | 0 | 150 | archer, archertur, drummer, drummerrus, drummertur (+24) |
| **Barracks, 17th century** `prubar` | pru | 40000 | 93.75 | 500 | 0 | 100 | 100 | 500 | 0 | 0 | 150 | archer, archertur, drummer, drummerrus, drummertur (+24) |
| **Strelets Barracks** `rusbar` | rus | **25000** | **78.12** | **300** | 0 | **200** | **20** | **0** | 0 | 0 | **25** | archer, archertur, drummer, drummerrus, drummertur (+24) |
| **Barracks, 17th century** `saxbar` | sax | 40000 | 93.75 | 500 | 0 | 100 | 100 | 500 | 0 | 0 | 150 | archer, archertur, drummer, drummerrus, drummertur (+24) |
| **Barracks, 17th century** `scobar` | sco | **30000** | 93.75 | 500 | 0 | 100 | 100 | 500 | 0 | 0 | 150 | archer, archertur, bagpiper, drummer, drummerrus (+25) |
| **Barracks, 17th century** `spabar` | spa | 40000 | 93.75 | 500 | 0 | 100 | 100 | 500 | 0 | 0 | 150 | archer, archertur, drummer, drummerrus, drummertur (+24) |
| **Barracks, 17th century** `swebar` | swe | 40000 | 93.75 | 500 | 0 | 100 | 100 | 500 | 0 | 0 | 150 | archer, archertur, drummer, drummerrus, drummertur (+24) |
| **Barracks, 17th century** `swibar` | swi | 40000 | 93.75 | 500 | 0 | 100 | 100 | 500 | 0 | 0 | 150 | archer, archertur, drummer, drummerrus, drummertur (+24) |
| **Barracks** `turbar` | tur | **35000** | 93.75 | 500 | 0 | **400** | **400** | **0** | 0 | 0 | **50** | archer, archertur, drummer, drummerrus, drummertur (+24) |
| **Cossack House** `ukrbar` | ukr | **20000** | 93.75 | **300** | 0 | **150** | **150** | **0** | 0 | 0 | **75** | archer, archertur, drummer, drummerrus, drummertur (+24) |
| **Barracks, 17th century** `venbar` | ven | 40000 | 93.75 | 500 | 0 | 100 | 100 | 500 | 0 | 0 | 150 | archer, archertur, drummer, drummerrus, drummertur (+24) |

### ba2 — Barracks 18c

| Здание | Нация | HP | Time (s) | cost% | F | W | S | G | I | C | farm | produces |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| **Barracks, 18th century** `ausba2` | aus | 55000 | 5625.0 | 200 | 0 | 1700 | 2950 | 4000 | 0 | 0 | 250 | archersco, bagpiper, chasseur, drummer18, grenadier (+19) |
| **Barracks, 18th century** `bavba2` | bav | 55000 | 5625.0 | 200 | 0 | 1700 | 2950 | 4000 | 0 | 0 | 250 | archersco, bagpiper, chasseur, drummer18, grenadier (+19) |
| **Barracks, 18th century** `denba2` | den | 55000 | 5625.0 | 200 | 0 | 1700 | 2950 | 4000 | 0 | 0 | 250 | archersco, bagpiper, chasseur, drummer18, grenadier (+19) |
| **Barracks, 18th century** `engba2` | eng | 55000 | 5625.0 | 200 | 0 | 1700 | 2950 | 4000 | 0 | 0 | 250 | archersco, bagpiper, chasseur, drummer18, grenadier (+19) |
| **Barracks, 18th century** `fraba2` | fra | 55000 | 5625.0 | 200 | 0 | 1700 | 2950 | 4000 | 0 | 0 | 250 | archersco, bagpiper, chasseur, drummer18, grenadier (+19) |
| **Barracks, 18th century** `hunba2` | hun | 55000 | 5625.0 | 200 | 0 | 1700 | 2950 | 4000 | 0 | 0 | 250 | archersco, bagpiper, chasseur, drummer18, grenadier (+19) |
| **Barracks, 18th century** `netba2` | net | 55000 | 5625.0 | 200 | 0 | 1700 | 2950 | 4000 | 0 | 0 | 250 | archersco, bagpiper, chasseur, drummer18, grenadier (+19) |
| **Barracks, 18th century** `pieba2` | pie | 55000 | 5625.0 | 200 | 0 | 1700 | 2950 | 4000 | 0 | 0 | 250 | archersco, bagpiper, chasseur, drummer18, grenadier (+19) |
| **Barracks, 18th century** `polba2` | pol | 55000 | 5625.0 | 200 | 0 | 1700 | 2950 | 4000 | 0 | 0 | 250 | archersco, bagpiper, chasseur, drummer18, grenadier (+19) |
| **Barracks, 18th century** `porba2` | por | 55000 | 5625.0 | 200 | 0 | 1700 | 2950 | 4000 | 0 | 0 | 250 | archersco, bagpiper, chasseur, drummer18, grenadier (+19) |
| **Barracks, 18th century** `pruba2` | pru | 55000 | 5625.0 | 200 | 0 | 1700 | 2950 | 4000 | 0 | 0 | 250 | archersco, bagpiper, chasseur, drummer18, grenadier (+19) |
| **Barracks, 18th century** `rusba2` | rus | 55000 | 5625.0 | 200 | 0 | 1700 | 2950 | 4000 | 0 | 0 | 250 | archersco, bagpiper, chasseur, drummer18, grenadier (+19) |
| **Barracks, 18th century** `saxba2` | sax | 55000 | 5625.0 | 200 | 0 | 1700 | 2950 | 4000 | 0 | 0 | 250 | archersco, bagpiper, chasseur, drummer18, grenadier (+19) |
| **Castle** `scoba2` | sco | **40000** | **625.0** | **250** | 0 | **640** | **2400** | **2400** | 0 | 0 | **150** | archersco, chasseur, drummer18, grenadier, grenadierbav (+18) |
| **Barracks, 18th century** `spaba2` | spa | 55000 | 5625.0 | 200 | 0 | 1700 | 2950 | 4000 | 0 | 0 | 250 | archersco, bagpiper, chasseur, drummer18, grenadier (+19) |
| **Barracks, 18th century** `sweba2` | swe | 55000 | 5625.0 | 200 | 0 | 1700 | 2950 | 4000 | 0 | 0 | 250 | archersco, bagpiper, chasseur, drummer18, grenadier (+19) |
| **Barracks, 18th century** `swiba2` | swi | 55000 | 5625.0 | 200 | 0 | 1700 | 2950 | 4000 | 0 | 0 | 250 | archersco, bagpiper, chasseur, drummer18, grenadier (+19) |
| **Barracks, 18th century** `venba2` | ven | 55000 | 5625.0 | 200 | 0 | 1700 | 2950 | 4000 | 0 | 0 | 250 | archersco, bagpiper, chasseur, drummer18, grenadier (+19) |

### bla — Blacksmith

| Здание | Нация | HP | Time (s) | cost% | F | W | S | G | I | C | farm | produces |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| **Blacksmith** `algbla` | alg | **6500** | **109.38** | 400 | 0 | 100 | 30 | 0 | 640 | 0 | 0 | — |
| **Blacksmith** `ausbla` | aus | 5500 | 93.75 | 400 | 0 | 100 | 30 | 0 | 640 | 0 | 0 | — |
| **Blacksmith** `bavbla` | bav | 5500 | 93.75 | 400 | 0 | 100 | 30 | 0 | 640 | 0 | 0 | — |
| **Blacksmith** `denbla` | den | 5500 | 93.75 | 400 | 0 | 100 | 30 | 0 | 640 | 0 | 0 | — |
| **Blacksmith** `engbla` | eng | 5500 | 93.75 | 400 | 0 | 100 | 30 | 0 | 640 | 0 | 0 | — |
| **Blacksmith** `frabla` | fra | 5500 | 93.75 | **600** | 0 | 100 | 30 | 0 | 640 | 0 | 0 | — |
| **Blacksmith** `hunbla` | hun | 5500 | 93.75 | 400 | 0 | 100 | 30 | 0 | 640 | 0 | 0 | — |
| **Blacksmith** `netbla` | net | 5500 | 93.75 | 400 | 0 | 100 | 30 | 0 | 640 | 0 | 0 | — |
| **Blacksmith** `piebla` | pie | 5500 | 93.75 | 400 | 0 | 100 | 30 | 0 | 640 | 0 | 0 | — |
| **Blacksmith** `polbla` | pol | 5500 | 93.75 | 400 | 0 | 100 | 30 | 0 | 640 | 0 | 0 | — |
| **Blacksmith** `porbla` | por | 5500 | 93.75 | 400 | 0 | 100 | 30 | 0 | 640 | 0 | 0 | — |
| **Blacksmith** `prubla` | pru | 5500 | 93.75 | 400 | 0 | 100 | 30 | 0 | 640 | 0 | 0 | — |
| **Blacksmith** `rusbla` | rus | 5500 | 93.75 | 400 | 0 | 100 | 30 | 0 | 640 | 0 | 0 | — |
| **Blacksmith** `saxbla` | sax | 5500 | 93.75 | 400 | 0 | 100 | 30 | 0 | 640 | 0 | 0 | — |
| **Blacksmith** `scobla` | sco | 5500 | 93.75 | 400 | 0 | 100 | 30 | 0 | 640 | 0 | 0 | — |
| **Blacksmith** `spabla` | spa | 5500 | 93.75 | 400 | 0 | 100 | 30 | 0 | 640 | 0 | 0 | — |
| **Blacksmith** `swebla` | swe | 5500 | 93.75 | 400 | 0 | 100 | 30 | 0 | 640 | 0 | 0 | — |
| **Blacksmith** `swibla` | swi | 5500 | 93.75 | 400 | 0 | 100 | 30 | 0 | 640 | 0 | 0 | — |
| **Blacksmith** `turbla` | tur | **6500** | **109.38** | 400 | 0 | 100 | 30 | 0 | 640 | 0 | 0 | — |
| **Blacksmith** `ukrbla` | ukr | **4500** | **62.5** | 400 | 0 | 100 | 30 | 0 | 640 | 0 | 0 | — |
| **Blacksmith** `venbla` | ven | 5500 | 93.75 | 400 | 0 | 100 | 30 | 0 | 640 | 0 | 0 | — |

### sta — Stable

| Здание | Нация | HP | Time (s) | cost% | F | W | S | G | I | C | farm | produces |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| **Stable** `algsta` | alg | **55000** | **156.25** | **700** | 0 | **1000** | **2200** | **0** | 0 | 0 | 0 | cossackdon, cossackregister, cossacksich, croat, cuirassier (+25) |
| **Stable** `aussta` | aus | 20000 | 625.0 | 200 | 0 | 2500 | 100 | 600 | 0 | 0 | 0 | cossackdon, cossackregister, cossacksich, croat, cuirassier (+25) |
| **Stable** `bavsta` | bav | 20000 | 625.0 | 200 | 0 | 2500 | 100 | 600 | 0 | 0 | 0 | cossackdon, cossackregister, cossacksich, croat, cuirassier (+25) |
| **Stable** `densta` | den | 20000 | 625.0 | 200 | 0 | 2500 | 100 | 600 | 0 | 0 | 0 | cossackdon, cossackregister, cossacksich, croat, cuirassier (+25) |
| **Stable** `engsta` | eng | **25000** | **375.0** | 200 | 0 | **2350** | **0** | **800** | 0 | 0 | 0 | cossackdon, cossackregister, cossacksich, croat, cuirassier (+25) |
| **Stable** `frasta` | fra | 20000 | 625.0 | 200 | 0 | 2500 | 100 | 600 | 0 | 0 | 0 | cossackdon, cossackregister, cossacksich, croat, cuirassier (+25) |
| **Stable** `hunsta` | hun | 20000 | 625.0 | 200 | 0 | 2500 | 100 | 600 | 0 | 0 | 0 | cossackdon, cossackregister, cossacksich, croat, cuirassier (+26) |
| **Stable** `netsta` | net | 20000 | 625.0 | 200 | 0 | 2500 | 100 | 600 | 0 | 0 | 0 | cossackdon, cossackregister, cossacksich, croat, cuirassier (+25) |
| **Stable** `piesta` | pie | 20000 | 625.0 | 200 | 0 | 2500 | 100 | 600 | 0 | 0 | 0 | cossackdon, cossackregister, cossacksich, croat, cuirassier (+25) |
| **Stable** `polsta` | pol | 20000 | 625.0 | 200 | 0 | 2500 | 100 | 600 | 0 | 0 | 0 | cossackdon, cossackregister, cossacksich, croat, cuirassier (+25) |
| **Stable** `porsta` | por | 20000 | 625.0 | 200 | 0 | 2500 | 100 | 600 | 0 | 0 | 0 | cossackdon, cossackregister, cossacksich, croat, cuirassier (+25) |
| **Stable** `prusta` | pru | 20000 | 625.0 | 200 | 0 | 2500 | 100 | 600 | 0 | 0 | 0 | cossackdon, cossackregister, cossacksich, croat, cuirassier (+25) |
| **Stable** `russta` | rus | **25000** | **375.0** | 200 | 0 | **7950** | **0** | **550** | 0 | 0 | 0 | cossackdon, cossackregister, cossacksich, croat, cuirassier (+25) |
| **Stable** `saxsta` | sax | 20000 | 625.0 | 200 | 0 | 2500 | 100 | 600 | 0 | 0 | 0 | cossackdon, cossackregister, cossacksich, croat, cuirassier (+25) |
| **Stable** `scosta` | sco | **25000** | **375.0** | 200 | 0 | **2350** | **0** | **800** | 0 | 0 | 0 | cossackdon, cossackregister, cossacksich, croat, cuirassier (+25) |
| **Stable** `spasta` | spa | 20000 | 625.0 | 200 | 0 | 2500 | 100 | 600 | 0 | 0 | 0 | cossackdon, cossackregister, cossacksich, croat, cuirassier (+25) |
| **Stable** `swesta` | swe | 20000 | 625.0 | 200 | 0 | 2500 | 100 | 600 | 0 | 0 | 0 | cossackdon, cossackregister, cossacksich, croat, cuirassier (+25) |
| **Stable** `swista` | swi | 20000 | 625.0 | 200 | 0 | 2500 | 100 | 600 | 0 | 0 | 0 | cossackdon, cossackregister, cossacksich, croat, cuirassier (+25) |
| **Stable** `tursta` | tur | **55000** | **156.25** | **700** | 0 | **1000** | **2600** | **0** | 0 | 0 | 0 | cossackdon, cossackregister, cossacksich, croat, cuirassier (+25) |
| **Stable** `ukrsta` | ukr | **10000** | **156.25** | **300** | 0 | **3200** | **850** | **850** | 0 | 0 | 0 | cossackdon, cossackregister, cossacksich, croat, cuirassier (+25) |
| **Stable** `vensta` | ven | 20000 | 625.0 | 200 | 0 | 2500 | 100 | 600 | 0 | 0 | 0 | cossackdon, cossackregister, cossacksich, croat, cuirassier (+25) |

### tem — Cathedral

| Здание | Нация | HP | Time (s) | cost% | F | W | S | G | I | C | farm | produces |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| **Mosque** `algtem` | alg | **5000** | **93.75** | 300 | 0 | 1000 | 1200 | 0 | 500 | 0 | 0 | mullah, padre, pope, priest |
| **Cathedral** `austem` | aus | 4200 | 156.25 | 300 | 0 | 1000 | 1200 | 0 | 500 | 0 | 0 | mullah, padre, pope, priest |
| **Cathedral** `bavtem` | bav | 4200 | 156.25 | 300 | 0 | 1000 | 1200 | 0 | 500 | 0 | 0 | mullah, padre, pope, priest |
| **Cathedral** `dentem` | den | 4200 | 156.25 | 300 | 0 | 1000 | 1200 | 0 | 500 | 0 | 0 | mullah, padre, pope, priest |
| **Cathedral** `engtem` | eng | 4200 | 156.25 | 300 | 0 | 1000 | 1200 | 0 | 500 | 0 | 0 | mullah, padre, pope, priest |
| **Cathedral** `fratem` | fra | **6000** | **312.5** | 300 | 0 | **1100** | **2000** | 0 | **600** | 0 | 0 | mullah, padre, pope, priest |
| **Cathedral** `huntem` | hun | 4200 | 156.25 | 300 | 0 | 1000 | 1200 | 0 | 500 | 0 | 0 | mullah, padre, pope, priest |
| **Cathedral** `nettem` | net | 4200 | 156.25 | 300 | 0 | 1000 | 1200 | 0 | 500 | 0 | 0 | mullah, padre, pope, priest |
| **Cathedral** `pietem` | pie | 4200 | 156.25 | 300 | 0 | 1000 | 1200 | 0 | 500 | 0 | 0 | mullah, padre, pope, priest |
| **Cathedral** `poltem` | pol | 4200 | 156.25 | 300 | 0 | 1000 | 1200 | 0 | 500 | 0 | 0 | mullah, padre, pope, priest |
| **Cathedral** `portem` | por | 4200 | 156.25 | 300 | 0 | 1000 | 1200 | 0 | 500 | 0 | 0 | mullah, padre, pope, priest |
| **Cathedral** `prutem` | pru | 4200 | 156.25 | 300 | 0 | 1000 | 1200 | 0 | 500 | 0 | 0 | mullah, padre, pope, priest |
| **Orthodox Cathedral** `rustem` | rus | **4500** | 156.25 | 300 | 0 | **1150** | **1650** | **100** | 500 | 0 | 0 | mullah, padre, pope, priest |
| **Cathedral** `saxtem` | sax | 4200 | 156.25 | 300 | 0 | 1000 | 1200 | 0 | 500 | 0 | 0 | mullah, padre, pope, priest |
| **Cathedral** `scotem` | sco | 4200 | 156.25 | 300 | 0 | 1000 | 1200 | 0 | 500 | 0 | 0 | mullah, padre, pope, priest |
| **Cathedral** `spatem` | spa | 4200 | 156.25 | 300 | 0 | 1000 | 1200 | 0 | 500 | 0 | 0 | mullah, padre, pope, priest |
| **Cathedral** `swetem` | swe | 4200 | 156.25 | 300 | 0 | 1000 | 1200 | 0 | 500 | 0 | 0 | mullah, padre, pope, priest |
| **Cathedral** `switem` | swi | 4200 | 156.25 | 300 | 0 | 1000 | 1200 | 0 | 500 | 0 | 0 | mullah, padre, pope, priest |
| **Mosque** `turtem` | tur | **5000** | **93.75** | 300 | 0 | 1000 | 1200 | 0 | 500 | 0 | 0 | mullah, padre, pope, priest |
| **Orthodox Cathedral** `ukrtem` | ukr | **5300** | 156.25 | 300 | 0 | **1100** | **1400** | 0 | **300** | 0 | 0 | mullah, padre, pope, priest |
| **Cathedral** `ventem` | ven | 4200 | 156.25 | 300 | 0 | 1000 | 1200 | 0 | 500 | 0 | 0 | mullah, padre, pope, priest |

### aca — Academy

| Здание | Нация | HP | Time (s) | cost% | F | W | S | G | I | C | farm | produces |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| **Minaret** `algaca` | alg | **65000** | **156.25** | 300 | 0 | **1450** | 1100 | 0 | 0 | 0 | 0 | — |
| **Academy** `ausaca` | aus | **65000** | 625.0 | 300 | 0 | 1250 | 1100 | 0 | 0 | 0 | 0 | — |
| **Academy** `bavaca` | bav | 63000 | 625.0 | 300 | 0 | 1250 | 1100 | 0 | 0 | 0 | 0 | — |
| **Academy** `denaca` | den | 63000 | 625.0 | 300 | 0 | **1450** | **900** | 0 | 0 | 0 | 0 | — |
| **Academy** `engaca` | eng | 63000 | 625.0 | 300 | 0 | **1150** | **1200** | 0 | 0 | 0 | 0 | — |
| **Academy** `fraaca` | fra | 63000 | 625.0 | 300 | 0 | 1250 | 1100 | 0 | 0 | 0 | 0 | — |
| **Academy** `hunaca` | hun | 63000 | 625.0 | 300 | 0 | 1250 | 1100 | 0 | 0 | 0 | 0 | — |
| **Academy** `netaca` | net | 63000 | 625.0 | 300 | 0 | **1050** | **1230** | 0 | 0 | 0 | 0 | — |
| **Academy** `pieaca` | pie | 63000 | 625.0 | 300 | 0 | 1250 | 1100 | 0 | 0 | 0 | 0 | — |
| **Academy** `polaca` | pol | 63000 | 625.0 | 300 | 0 | **950** | **800** | 0 | 0 | 0 | 0 | — |
| **Academy** `poraca` | por | 63000 | 625.0 | 300 | 0 | 1250 | 1100 | 0 | 0 | 0 | 0 | — |
| **Academy** `pruaca` | pru | 63000 | 625.0 | 300 | 0 | **1200** | **1150** | 0 | 0 | 0 | 0 | — |
| **Academy** `rusaca` | rus | **65000** | **843.75** | 300 | 0 | 1250 | **1300** | 0 | 0 | 0 | 0 | — |
| **Academy** `saxaca` | sax | 63000 | 625.0 | 300 | 0 | 1250 | 1100 | 0 | 0 | 0 | 0 | — |
| **Academy** `scoaca` | sco | 63000 | 625.0 | 300 | 0 | 1250 | 1100 | 0 | 0 | 0 | 0 | — |
| **Academy** `spaaca` | spa | 63000 | 625.0 | 300 | 0 | **1350** | **1000** | 0 | 0 | 0 | 0 | — |
| **Academy** `sweaca` | swe | 63000 | 625.0 | 300 | 0 | **1350** | **1000** | 0 | 0 | 0 | 0 | — |
| **Academy** `swiaca` | swi | 63000 | 625.0 | 300 | 0 | 1250 | 1100 | 0 | 0 | 0 | 0 | — |
| **Minaret** `turaca` | tur | **65000** | **156.25** | 300 | 0 | **1450** | 1100 | 0 | 0 | 0 | 0 | — |
| **Academy** `ukraca` | ukr | **65000** | **46.88** | 300 | 0 | **1350** | **1200** | 0 | 0 | 0 | 0 | — |
| **Academy** `venaca` | ven | 63000 | 625.0 | 300 | 0 | **1090** | **1260** | 0 | 0 | 0 | 0 | — |

### art — Artillery Depot

| Здание | Нация | HP | Time (s) | cost% | F | W | S | G | I | C | farm | produces |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| **Artillery Depot** `algart` | alg | 40000 | 245.94 | 200 | 0 | 100 | 1000 | 0 | 0 | 1400 | 0 | cannon, framegun, howitzer, mortar, multicannon |
| **Artillery Depot** `ausart` | aus | 40000 | 245.94 | 200 | 0 | 100 | 1000 | 0 | 0 | 1400 | 0 | cannon, framegun, howitzer, mortar, multicannon |
| **Artillery Depot** `bavart` | bav | 40000 | 245.94 | 200 | 0 | 100 | 1000 | 0 | 0 | 1400 | 0 | cannon, framegun, howitzer, mortar, multicannon |
| **Artillery Depot** `denart` | den | 40000 | 245.94 | 200 | 0 | 100 | 1000 | 0 | 0 | 1400 | 0 | cannon, framegun, howitzer, mortar, multicannon |
| **Artillery Depot** `engart` | eng | 40000 | 245.94 | 200 | 0 | 100 | 1000 | 0 | 0 | 1400 | 0 | cannon, framegun, howitzer, mortar, multicannon |
| **Artillery Depot** `fraart` | fra | 40000 | 245.94 | 200 | 0 | 100 | 1000 | 0 | 0 | 1400 | 0 | cannon, framegun, howitzer, mortar, multicannon |
| **Artillery Depot** `hunart` | hun | 40000 | 245.94 | 200 | 0 | 100 | 1000 | 0 | 0 | 1400 | 0 | cannon, framegun, howitzer, mortar, multicannon |
| **Artillery Depot** `netart` | net | 40000 | 245.94 | 200 | 0 | 100 | 1000 | 0 | 0 | 1400 | 0 | cannon, framegun, howitzer, mortar, multicannon |
| **Artillery Depot** `pieart` | pie | 40000 | 245.94 | 200 | 0 | 100 | 1000 | 0 | 0 | 1400 | 0 | cannon, framegun, howitzer, mortar, multicannon |
| **Artillery Depot** `polart` | pol | 40000 | 245.94 | 200 | 0 | 100 | 1000 | 0 | 0 | 1400 | 0 | cannon, framegun, howitzer, mortar, multicannon |
| **Artillery Depot** `porart` | por | 40000 | 245.94 | 200 | 0 | 100 | 1000 | 0 | 0 | 1400 | 0 | cannon, framegun, howitzer, mortar, multicannon |
| **Artillery Depot** `pruart` | pru | 40000 | 245.94 | 200 | 0 | 100 | 1000 | 0 | 0 | 1400 | 0 | cannon, framegun, howitzer, mortar, multicannon |
| **Artillery Depot** `rusart` | rus | 40000 | 245.94 | 200 | 0 | 100 | 1000 | 0 | 0 | 1400 | 0 | cannon, framegun, howitzer, mortar, multicannon |
| **Artillery Depot** `saxart` | sax | 40000 | 245.94 | 200 | 0 | 100 | 1000 | 0 | 0 | 1400 | 0 | cannon, framegun, howitzer, mortar, multicannon |
| **Artillery Depot** `scoart` | sco | 40000 | 245.94 | 200 | 0 | 100 | 1000 | 0 | 0 | 1400 | 0 | cannon, framegun, howitzer, mortar, multicannon |
| **Artillery Depot** `spaart` | spa | 40000 | 245.94 | 200 | 0 | 100 | 1000 | 0 | 0 | 1400 | 0 | cannon, framegun, howitzer, mortar, multicannon |
| **Artillery Depot** `sweart` | swe | 40000 | 245.94 | 200 | 0 | 100 | 1000 | 0 | 0 | 1400 | 0 | cannon, framegun, howitzer, mortar, multicannon |
| **Artillery Depot** `swiart` | swi | 40000 | 245.94 | 200 | 0 | 100 | 1000 | 0 | 0 | 1400 | 0 | cannon, framegun, howitzer, mortar, multicannon |
| **Artillery Depot** `turart` | tur | 40000 | 245.94 | 200 | 0 | **500** | **1200** | 0 | 0 | 1400 | 0 | cannon, framegun, howitzer, mortar, multicannon |
| **Artillery Depot** `ukrart` | ukr | 40000 | 245.94 | 200 | 0 | **4250** | **4400** | **100** | 0 | 1400 | 0 | cannon, framegun, howitzer, mortar, multicannon |
| **Artillery Depot** `venart` | ven | 40000 | 245.94 | 200 | 0 | 100 | 1000 | 0 | 0 | 1400 | 0 | cannon, framegun, howitzer, mortar, multicannon |

### dip — Diplomatic Center

| Здание | Нация | HP | Time (s) | cost% | F | W | S | G | I | C | farm | produces |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| **Diplomatic Center** `algdip` | alg | **5500** | 312.5 | 100 | 0 | **4600** | **2020** | 0 | 0 | 0 | 0 | archerdip, archerturdip, cossacksichdip, dragoon18dip, grenadierdip (+3) |
| **Diplomatic Center** `ausdip` | aus | 4500 | 312.5 | 100 | 0 | 4900 | 1700 | 0 | 0 | 0 | 0 | archerdip, archerturdip, cossacksichdip, dragoon18dip, grenadierdip (+3) |
| **Diplomatic Center** `bavdip` | bav | 4500 | 312.5 | 100 | 0 | 4900 | 1700 | 0 | 0 | 0 | 0 | archerdip, archerturdip, cossacksichdip, dragoon18dip, grenadierdip (+3) |
| **Diplomatic Center** `dendip` | den | 4500 | 312.5 | 100 | 0 | 4900 | 1700 | 0 | 0 | 0 | 0 | archerdip, archerturdip, cossacksichdip, dragoon18dip, grenadierdip (+3) |
| **Diplomatic Center** `engdip` | eng | 4500 | 312.5 | 100 | 0 | 4900 | 1700 | 0 | 0 | 0 | 0 | archerdip, archerturdip, cossacksichdip, dragoon18dip, grenadierdip (+3) |
| **Diplomatic Center** `fradip` | fra | 4500 | 312.5 | 100 | 0 | 4900 | 1700 | 0 | 0 | 0 | 0 | archerdip, archerturdip, cossacksichdip, dragoon18dip, grenadierdip (+3) |
| **Diplomatic Center** `hundip` | hun | 4500 | 312.5 | 100 | 0 | 4900 | 1700 | 0 | 0 | 0 | 0 | archerdip, archerturdip, cossacksichdip, dragoon18dip, grenadierdip (+3) |
| **Diplomatic Center** `netdip` | net | 4500 | 312.5 | 100 | 0 | 4900 | 1700 | 0 | 0 | 0 | 0 | archerdip, archerturdip, cossacksichdip, dragoon18dip, grenadierdip (+3) |
| **Diplomatic Center** `piedip` | pie | 4500 | 312.5 | 100 | 0 | 4900 | 1700 | 0 | 0 | 0 | 0 | archerdip, archerturdip, cossacksichdip, dragoon18dip, grenadierdip (+3) |
| **Diplomatic Center** `poldip` | pol | 4500 | 312.5 | 100 | 0 | 4900 | 1700 | 0 | 0 | 0 | 0 | archerdip, archerturdip, cossacksichdip, dragoon18dip, grenadierdip (+3) |
| **Diplomatic Center** `pordip` | por | 4500 | 312.5 | 100 | 0 | 4900 | 1700 | 0 | 0 | 0 | 0 | archerdip, archerturdip, cossacksichdip, dragoon18dip, grenadierdip (+3) |
| **Diplomatic Center** `prudip` | pru | 4500 | 312.5 | 100 | 0 | 4900 | 1700 | 0 | 0 | 0 | 0 | archerdip, archerturdip, cossacksichdip, dragoon18dip, grenadierdip (+3) |
| **Diplomatic Center** `rusdip` | rus | **6500** | 312.5 | 100 | 0 | **7900** | **3700** | 0 | 0 | 0 | 0 | archerdip, archerturdip, cossacksichdip, dragoon18dip, grenadierdip (+3) |
| **Diplomatic Center** `saxdip` | sax | 4500 | 312.5 | 100 | 0 | 4900 | 1700 | 0 | 0 | 0 | 0 | archerdip, archerturdip, cossacksichdip, dragoon18dip, grenadierdip (+3) |
| **Diplomatic Center** `scodip` | sco | 4500 | 312.5 | 100 | 0 | 4900 | 1700 | 0 | 0 | 0 | 0 | archerdip, archerturdip, cossacksichdip, dragoon18dip, grenadierdip (+3) |
| **Diplomatic Center** `spadip` | spa | 4500 | 312.5 | 100 | 0 | 4900 | 1700 | 0 | 0 | 0 | 0 | archerdip, archerturdip, cossacksichdip, dragoon18dip, grenadierdip (+3) |
| **Diplomatic Center** `swedip` | swe | 4500 | 312.5 | 100 | 0 | 4900 | 1700 | 0 | 0 | 0 | 0 | archerdip, archerturdip, cossacksichdip, dragoon18dip, grenadierdip (+3) |
| **Diplomatic Center** `swidip` | swi | 4500 | 312.5 | 100 | 0 | 4900 | 1700 | 0 | 0 | 0 | 0 | archerdip, archerturdip, cossacksichdip, dragoon18dip, grenadierdip (+3) |
| **Diplomatic Center** `turdip` | tur | **5500** | 312.5 | 100 | 0 | **4600** | **2020** | 0 | 0 | 0 | 0 | archerdip, archerturdip, cossacksichdip, dragoon18dip, grenadierdip (+3) |
| **Diplomatic Center** `ukrdip` | ukr | **5000** | 312.5 | 100 | 0 | **3900** | **2700** | 0 | 0 | 0 | 0 | archerdip, archerturdip, cossacksichdip, dragoon18dip, grenadierdip (+3) |
| **Diplomatic Center** `vendip` | ven | 4500 | 312.5 | 100 | 0 | 4900 | 1700 | 0 | 0 | 0 | 0 | archerdip, archerturdip, cossacksichdip, dragoon18dip, grenadierdip (+3) |

## Common здания (по кластерам)

### mil — Mill

| Здание (cluster) | Нации | HP | Time (s) | cost% | F | W | S | G | I | C | Доп. |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| **Mill** `eurmil` | aus, bav, den, eng, fra, hun, net, pie, pol, por, pru, sax, sco, spa, swe, swi, ven | 20000 | 93.75 | 200 | 0 | 30 | 150 | 0 | 0 | 0 | — |
| **Mill** `rusmil` | rus, ukr | 15000 | 93.75 | 200 | 0 | 210 | 0 | 0 | 0 | 0 | — |
| **Mill** `turmil` | alg, tur | 20000 | 93.75 | 200 | 0 | 30 | 150 | 0 | 0 | 0 | — |

### sto — Storehouse

| Здание (cluster) | Нации | HP | Time (s) | cost% | F | W | S | G | I | C | Доп. |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| **Storehouse** `eursto` | aus, bav, den, eng, fra, hun, net, pie, pru, sax, sco, swe, swi, ven | 10000 | 31.25 | 150 | 0 | 50 | 20 | 0 | 0 | 0 | — |
| **Storehouse** `russto` | pol, rus, ukr | 10000 | 31.25 | 200 | 0 | 50 | 20 | 0 | 0 | 0 | — |
| **Storehouse** `spasto` | por, spa | 10000 | 31.25 | 150 | 0 | 20 | 20 | 0 | 0 | 0 | — |
| **Storehouse** `tursto` | alg, tur | 10000 | 31.25 | 200 | 0 | 30 | 10 | 0 | 0 | 0 | — |

### mar — Market

| Здание (cluster) | Нации | HP | Time (s) | cost% | F | W | S | G | I | C | Доп. |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| **Market** `eurmar` | aus, bav, den, eng, fra, hun, net, pie, pol, pru, sax, sco, swe, swi, ven | 4000 | 234.38 | 2000 | 0 | 450 | 0 | 0 | 0 | 0 | — |
| **Market** `rusmar` | rus, ukr | 4000 | 234.38 | 2000 | 0 | 450 | 0 | 0 | 0 | 0 | — |
| **Market** `spamar` | por, spa | 4000 | 156.25 | 2000 | 0 | 450 | 0 | 0 | 0 | 0 | — |
| **Bazaar** `turmar` | alg, tur | 4500 | 234.38 | 1500 | 0 | 450 | 150 | 0 | 0 | 0 | — |

### por — Shipyard

| Здание (cluster) | Нации | HP | Time (s) | cost% | F | W | S | G | I | C | Доп. |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| **Shipyard** `eurpor` | aus, bav, den, eng, fra, hun, net, pie, pol, pru, sax, sco, spa, swe, swi, ven | 50000 | 1562.5 | 150 | 0 | 1600 | 800 | 0 | 400 | 0 | — |
| **Shipyard** `porpor` | por | 50000 | 1562.5 | 150 | 0 | 1600 | 800 | 0 | 400 | 0 | dmg 1000; range 28.1t; upkeep {"gold": 250} |
| **Shipyard** `ruspor` | rus | 45000 | 1562.5 | 150 | 0 | 1200 | 800 | 0 | 400 | 0 | — |
| **Shipyard** `turpor` | alg, tur | 40000 | 1562.5 | 150 | 0 | 800 | 800 | 0 | 400 | 0 | — |
| **Shipyard** `ukrpor` | ukr | 45000 | 1562.5 | 150 | 0 | 2000 | 0 | 0 | 0 | 0 | — |

### tow — Tower

| Здание (cluster) | Нации | HP | Time (s) | cost% | F | W | S | G | I | C | Доп. |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| **Tower** `eurtow` | aus, bav, den, eng, fra, hun, net, pie, pol, por, pru, sax, sco, spa, swe, swi, ven | 20000 | 1230.31 | 120 | 0 | 100 | 100 | 150 | 0 | 0 | dmg 1000; range 28.1t; upkeep {"gold": 500} |
| **Tower** `rustow` | rus | 21000 | 1476.56 | 125 | 0 | 100 | 100 | 150 | 0 | 0 | dmg 1000; range 28.1t; upkeep {"gold": 500} |
| **Tower** `turtow` | alg, tur | 22500 | 984.38 | 125 | 0 | 150 | 90 | 100 | 0 | 0 | dmg 1200; range 30.0t; upkeep {"gold": 500} |

### gol — Gold Mine

| Здание (cluster) | Нации | HP | Time (s) | cost% | F | W | S | G | I | C | Доп. |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| **Mine** `eurgol` | alg, aus, bav, den, eng, fra, hun, net, pie, pol, por, pru, rus, sax, sco, spa, swe, swi, tur, ukr, ven | 2500 | 93.75 | 0 | 0 | 100 | 100 | 0 | 0 | 0 | produce {"gold": 13}; peasants 5 |

### iro — Iron Mine

| Здание (cluster) | Нации | HP | Time (s) | cost% | F | W | S | G | I | C | Доп. |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| **Mine** `euriro` | alg, aus, bav, den, eng, fra, hun, net, pie, pol, por, pru, rus, sax, sco, spa, swe, swi, tur, ukr, ven | 2500 | 93.75 | 0 | 0 | 100 | 100 | 0 | 0 | 0 | produce {"iron": 13}; peasants 5 |

### coa — Coal Mine

| Здание (cluster) | Нации | HP | Time (s) | cost% | F | W | S | G | I | C | Доп. |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| **Mine** `eurcoa` | alg, aus, bav, den, eng, fra, hun, net, pie, pol, por, pru, rus, sax, sco, spa, swe, swi, tur, ukr, ven | 2500 | 93.75 | 0 | 0 | 100 | 100 | 0 | 0 | 0 | produce {"coal": 13}; peasants 5 |

### swa — Stone Wall

| Здание (cluster) | Нации | HP | Time (s) | cost% | F | W | S | G | I | C | Доп. |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| **Wall** `eurswa` | aus, bav, den, eng, fra, hun, net, pie, pol, por, pru, sax, sco, spa, swe, swi, ven | 50000 | 90.0 | 0 | 0 | 0 | 50 | 0 | 0 | 0 | upkeep {"stone": 250} |
| **Wall** `russwa` | rus | 50000 | 200.0 | 0 | 0 | 0 | 60 | 0 | 0 | 0 | upkeep {"stone": 200} |
| **Wall** `turswa` | alg, tur | 50000 | 120.0 | 0 | 0 | 0 | 60 | 0 | 0 | 0 | upkeep {"stone": 150} |

### sga — Stone Gate

| Здание (cluster) | Нации | HP | Time (s) | cost% | F | W | S | G | I | C | Доп. |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| **Gate** `eursga` | aus, bav, den, eng, fra, hun, net, pie, pol, por, pru, sax, sco, spa, swe, swi, ven | 50000 | 90.0 | 0 | 0 | 0 | 50 | 0 | 0 | 0 | upkeep {"stone": 250} |
| **Gate** `russga` | rus | 50000 | 200.0 | 0 | 0 | 0 | 60 | 0 | 0 | 0 | upkeep {"stone": 200} |
| **Gate** `tursga` | alg, tur | 50000 | 120.0 | 0 | 0 | 0 | 60 | 0 | 0 | 0 | upkeep {"stone": 150} |

## Шахты — апгрейды (gol/iro/coa)

Каждая шахта начинается с `peasantabsorber=5`. 6 апгрейдов накопительно доводят до **95 крестьян** на шахту.

| Уровень | +Воркеров | Food | Gold | Накопительно |
|---|---:|---:|---:|---:|
| `eurgol.1` | +5 | 1000 | 1250 | 10 |
| `eurgol.2` | +8 | 5250 | 4950 | 18 |
| `eurgol.3` | +10 | 12500 | 9250 | 28 |
| `eurgol.4` | +12 | 15800 | 18500 | 40 |
| `eurgol.5` | +15 | 19800 | 21050 | 55 |
| `eurgol.6` | +40 | 50200 | 25950 | 95 |