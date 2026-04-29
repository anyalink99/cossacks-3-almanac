# 03. Здания

[← Index](README.md)

Здания делятся на **per-nation** (`<nat>+suffix`, например `auscen` = ратуша Австрии) и **common** (`<cluster>+suffix`, общие для группы наций: `eur`/`rus`/`tur`/`spa`/`ukr`/`por`).

Цены ниже — для **первого** экземпляра. Цена N-го здания того же типа = `floor(base × (costpercent/100)^(N-1))`. Готовые таблицы N=1..6 для всех зданий — в [`../reports/scaling_prices.md`](../reports/scaling_prices.md), генератор — [`compute/compute_scaling.py`](../../compute/compute_scaling.py).

## Расшифровка колонок

| Колонка | Значение |
|---|---|
| **Здание** | Локализованное имя + `sid` |
| **Нация / Нации** | Какие нации имеют это здание (для common-кластеров — список) |
| **HP** | Очки здоровья достроенного здания |
| **Время (с)** | `buildtime` в game-секундах. Для зданий хранится с множителем `gc_buildtime_modifier=10` (т.е. `frames × 10/32`). С N строителями: `time × 1.13 / N`. См. [recon/building_mechanics.md](../../recon/building_mechanics.md). |
| **cost%** | `costpercent` — множитель цены каждого следующего экземпляра. 100 = одинаковая, 300 = ×3 за второе. 0 = без масштабирования. |
| **F / W / S / G / I / C** | Цена в ресурсах: **Food / Wood / Stone / Gold / Iron / Coal**. |
| **ферма** | `farm` — на сколько единиц это здание поднимает лимит населения. |
| **производит** | Список `sid` юнитов, которых здание умеет создавать. |
| **Доп.** | Прочее: оружие башен, гарнизон, доход шахт. |

**Жирным** в таблицах ниже — отклонения от базового значения (мода по столбцу), чтобы быстро видеть, чем нация отличается от большинства.

## Содержание

**[Постройки по нациям](#постройки-по-нациям)**
  - [cen — Town Hall](#cen--town-hall)
  - [hou — Housing](#hou--housing)
  - [bar — Barracks 17c](#bar--barracks-17c)
  - [ba2 — Barracks 18c](#ba2--barracks-18c)
  - [bla — Blacksmith](#bla--blacksmith)
  - [sta — Stable](#sta--stable)
  - [tem — Cathedral](#tem--cathedral)
  - [aca — Academy](#aca--academy)
  - [art — Artillery Depot](#art--artillery-depot)
  - [dip — Diplomatic Center](#dip--diplomatic-center)
**[Общие постройки (по кластерам)](#общие-постройки-по-кластерам)**
  - [mil — Mill](#mil--mill)
  - [sto — Storehouse](#sto--storehouse)
  - [mar — Market](#mar--market)
  - [por — Shipyard](#por--shipyard)
  - [tow — Tower](#tow--tower)
  - [gol — Gold Mine](#gol--gold-mine)
  - [iro — Iron Mine](#iro--iron-mine)
  - [coa — Coal Mine](#coa--coal-mine)
  - [swa — Stone Wall](#swa--stone-wall)
  - [sga — Stone Gate](#sga--stone-gate)
**[Шахты — апгрейды (gol/iro/coa)](#шахты--апгрейды-golirocoa)**

## Постройки по нациям

Сводка: для каждого типа зданий — параметры по всем нациям (где они есть). **Жирным** — отклонения от базового значения (мода по столбцу).

### cen — Town Hall

| Здание | Нация | HP | Время (с) | cost% | F | W | S | G | I | C | ферма | производит |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| **Городской центр** `algcen` | alg | **5500** | 156.25 | 300 | 0 | **450** | 700 | 0 | 0 | 0 | **50** | peaaus, peaeng, peapol, pearus, peasco (+3) |
| **Городской центр** `auscen` | aus | 4000 | **46.88** | 300 | 0 | 700 | 700 | 0 | 0 | 0 | 100 | peaaus, peaeng, peapol, pearus, peasco (+3) |
| **Городской центр** `bavcen` | bav | 4000 | 156.25 | 300 | 0 | 700 | 700 | 0 | 0 | 0 | 100 | peaaus, peaeng, peapol, pearus, peasco (+3) |
| **Городской центр** `dencen` | den | **4030** | 156.25 | 300 | 0 | 700 | 700 | 0 | 0 | 0 | 100 | peaaus, peaeng, peapol, pearus, peasco (+3) |
| **Городской центр** `engcen` | eng | **4030** | 156.25 | 300 | 0 | 700 | 700 | 0 | 0 | 0 | 100 | peaaus, peaeng, peapol, pearus, peasco (+3) |
| **Городской центр** `fracen` | fra | **4500** | 156.25 | 300 | 0 | 700 | 700 | 0 | 0 | 0 | 100 | peaaus, peaeng, peapol, pearus, peasco (+3) |
| **Городской центр** `huncen` | hun | 4000 | 156.25 | 300 | 0 | 700 | 700 | 0 | 0 | 0 | 100 | peaaus, peaeng, peapol, pearus, peasco (+3) |
| **Городской центр** `netcen` | net | **4950** | 156.25 | 300 | 0 | 700 | 700 | 0 | 0 | 0 | 100 | peaaus, peaeng, peapol, pearus, peasco (+3) |
| **Городской центр** `piecen` | pie | 4000 | 156.25 | 300 | 0 | 700 | 700 | 0 | 0 | 0 | 100 | peaaus, peaeng, peapol, pearus, peasco (+3) |
| **Городской центр** `polcen` | pol | **4300** | 156.25 | 300 | 0 | 700 | 700 | 0 | 0 | 0 | 100 | peaaus, peaeng, peapol, pearus, peasco (+3) |
| **Городской центр** `porcen` | por | 4000 | 156.25 | 300 | 0 | 700 | 700 | 0 | 0 | 0 | 100 | peaaus, peaeng, peapol, pearus, peasco (+3) |
| **Городской центр** `prucen` | pru | **4200** | 156.25 | 300 | 0 | 700 | 700 | 0 | 0 | 0 | 100 | peaaus, peaeng, peapol, pearus, peasco (+3) |
| **Городской центр** `ruscen` | rus | **4050** | 156.25 | 300 | 0 | **680** | 700 | 0 | 0 | 0 | **75** | peaaus, peaeng, peapol, pearus, peasco (+3) |
| **Городской центр** `saxcen` | sax | 4000 | 156.25 | 300 | 0 | 700 | 700 | 0 | 0 | 0 | 100 | peaaus, peaeng, peapol, pearus, peasco (+3) |
| **Городской центр** `scocen` | sco | 4000 | 156.25 | 300 | 0 | 700 | 700 | 0 | 0 | 0 | 100 | peaaus, peaeng, peapol, pearus, peasco (+3) |
| **Городской центр** `spacen` | spa | **4250** | 156.25 | 300 | 0 | 700 | 700 | 0 | 0 | 0 | 100 | peaaus, peaeng, peapol, pearus, peasco (+3) |
| **Городской центр** `swecen` | swe | **5000** | 156.25 | 300 | 0 | 700 | 700 | 0 | 0 | 0 | 100 | peaaus, peaeng, peapol, pearus, peasco (+3) |
| **Городской центр** `swicen` | swi | 4000 | 156.25 | 300 | 0 | 700 | 700 | 0 | 0 | 0 | 100 | peaaus, peaeng, peapol, pearus, peasco (+3) |
| **Городской центр** `turcen` | tur | 4000 | 156.25 | 300 | 0 | **600** | **500** | 0 | 0 | 0 | 100 | peaaus, peaeng, peapol, pearus, peasco (+3) |
| **Городской центр** `ukrcen` | ukr | **5300** | 156.25 | **400** | 0 | 700 | **0** | 0 | 0 | 0 | **200** | peaaus, peaeng, peapol, pearus, peasco (+3) |
| **Городской центр** `vencen` | ven | **5100** | 156.25 | 300 | 0 | 700 | 700 | 0 | 0 | 0 | 100 | peaaus, peaeng, peapol, pearus, peasco (+3) |

### hou — Housing

| Здание | Нация | HP | Время (с) | cost% | F | W | S | G | I | C | ферма | производит |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| **Дом** `alghou` | alg | **4300** | 31.25 | 104 | 0 | 100 | 100 | 0 | 0 | 0 | 25 | — |
| **Дом** `aushou` | aus | 4000 | 31.25 | 104 | 0 | 100 | 100 | 0 | 0 | 0 | 25 | — |
| **Дом** `bavhou` | bav | 4000 | 31.25 | 104 | 0 | 100 | 100 | 0 | 0 | 0 | 25 | — |
| **Дом** `denhou` | den | 4000 | 31.25 | 104 | 0 | 100 | 100 | 0 | 0 | 0 | 25 | — |
| **Дом** `enghou` | eng | **5000** | 31.25 | 104 | 0 | 100 | 100 | 0 | 0 | 0 | 25 | — |
| **Дом** `frahou` | fra | 4000 | 31.25 | 104 | 0 | 100 | 100 | 0 | 0 | 0 | 25 | — |
| **Дом** `hunhou` | hun | 4000 | 31.25 | 104 | 0 | 100 | 100 | 0 | 0 | 0 | 25 | — |
| **Дом** `nethou` | net | **4500** | 31.25 | 104 | 0 | 100 | 100 | 0 | 0 | 0 | 25 | — |
| **Дом** `piehou` | pie | 4000 | 31.25 | 104 | 0 | 100 | 100 | 0 | 0 | 0 | 25 | — |
| **Дом** `polhou` | pol | **4100** | 31.25 | 104 | 0 | 100 | 100 | 0 | 0 | 0 | 25 | — |
| **Дом** `porhou` | por | 4000 | 31.25 | 104 | 0 | 100 | 100 | 0 | 0 | 0 | 25 | — |
| **Дом** `pruhou` | pru | **4500** | 31.25 | 104 | 0 | 100 | 100 | 0 | 0 | 0 | 25 | — |
| **Изба** `rushou` | rus | **5000** | 31.25 | 104 | 0 | **120** | **0** | 0 | 0 | 0 | 25 | — |
| **Дом** `saxhou` | sax | 4000 | 31.25 | 104 | 0 | 100 | 100 | 0 | 0 | 0 | 25 | — |
| **Дом** `scohou` | sco | 4000 | 31.25 | 104 | 0 | 100 | 100 | 0 | 0 | 0 | 25 | — |
| **Дом** `spahou` | spa | **4200** | 31.25 | 104 | 0 | 100 | 100 | 0 | 0 | 0 | 25 | — |
| **Дом** `swehou` | swe | **5000** | 31.25 | 104 | 0 | 100 | 100 | 0 | 0 | 0 | 25 | — |
| **Дом** `swihou` | swi | 4000 | 31.25 | 104 | 0 | 100 | 100 | 0 | 0 | 0 | 25 | — |
| **Дом** `turhou` | tur | 4000 | 31.25 | **106** | 0 | 100 | 100 | 0 | 0 | 0 | 25 | — |
| **Хижина** `ukrhou` | ukr | **4150** | 31.25 | **105** | 0 | **120** | **0** | 0 | 0 | 0 | 25 | — |
| **Дом** `venhou` | ven | **5000** | 31.25 | 104 | 0 | 100 | 100 | 0 | 0 | 0 | 25 | — |

### bar — Barracks 17c

| Здание | Нация | HP | Время (с) | cost% | F | W | S | G | I | C | ферма | производит |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| **Казарма** `algbar` | alg | **35000** | 93.75 | 500 | 0 | **400** | **400** | **0** | 0 | 0 | **50** | archer, archertur, drummer, drummerrus, drummertur (+24) |
| **Казарма 17в.** `ausbar` | aus | 40000 | 93.75 | 500 | 0 | 100 | 100 | 500 | 0 | 0 | 150 | archer, archertur, drummer, drummerrus, drummertur (+24) |
| **Казарма 17в.** `bavbar` | bav | 40000 | 93.75 | 500 | 0 | 100 | 100 | 500 | 0 | 0 | 150 | archer, archertur, drummer, drummerrus, drummertur (+24) |
| **Казарма 17в.** `denbar` | den | 40000 | 93.75 | 500 | 0 | 100 | 100 | 500 | 0 | 0 | 150 | archer, archertur, drummer, drummerrus, drummertur (+24) |
| **Казарма 17в.** `engbar` | eng | 40000 | 93.75 | 500 | 0 | 100 | 100 | 500 | 0 | 0 | 150 | archer, archertur, drummer, drummerrus, drummertur (+24) |
| **Казарма 17в.** `frabar` | fra | 40000 | 93.75 | 500 | 0 | 100 | 100 | 500 | 0 | 0 | 150 | archer, archertur, drummer, drummerrus, drummertur (+24) |
| **Казарма 17в.** `hunbar` | hun | 40000 | 93.75 | 500 | 0 | 100 | 100 | 500 | 0 | 0 | 150 | archer, archertur, drummer, drummerrus, drummertur (+24) |
| **Казарма 17в.** `netbar` | net | 40000 | 93.75 | 500 | 0 | 100 | 100 | 500 | 0 | 0 | 150 | archer, archertur, drummer, drummerrus, drummertur (+24) |
| **Казарма 17в.** `piebar` | pie | 40000 | 93.75 | 500 | 0 | 100 | 100 | 500 | 0 | 0 | 150 | archer, archertur, drummer, drummerrus, drummertur (+24) |
| **Казарма 17в.** `polbar` | pol | 40000 | 93.75 | 500 | 0 | 100 | 100 | 500 | 0 | 0 | 150 | archer, archertur, drummer, drummerrus, drummertur (+24) |
| **Казарма 17в.** `porbar` | por | 40000 | 93.75 | 500 | 0 | 100 | 100 | 500 | 0 | 0 | 150 | archer, archertur, drummer, drummerrus, drummertur (+24) |
| **Казарма 17в.** `prubar` | pru | 40000 | 93.75 | 500 | 0 | 100 | 100 | 500 | 0 | 0 | 150 | archer, archertur, drummer, drummerrus, drummertur (+24) |
| **Стрелецкая казарма** `rusbar` | rus | **25000** | **78.12** | **300** | 0 | **200** | **20** | **0** | 0 | 0 | **25** | archer, archertur, drummer, drummerrus, drummertur (+24) |
| **Казарма 17в.** `saxbar` | sax | 40000 | 93.75 | 500 | 0 | 100 | 100 | 500 | 0 | 0 | 150 | archer, archertur, drummer, drummerrus, drummertur (+24) |
| **Казарма 17в.** `scobar` | sco | **30000** | 93.75 | 500 | 0 | 100 | 100 | 500 | 0 | 0 | 150 | archer, archertur, bagpiper, drummer, drummerrus (+25) |
| **Казарма 17в.** `spabar` | spa | 40000 | 93.75 | 500 | 0 | 100 | 100 | 500 | 0 | 0 | 150 | archer, archertur, drummer, drummerrus, drummertur (+24) |
| **Казарма 17в.** `swebar` | swe | 40000 | 93.75 | 500 | 0 | 100 | 100 | 500 | 0 | 0 | 150 | archer, archertur, drummer, drummerrus, drummertur (+24) |
| **Казарма 17в.** `swibar` | swi | 40000 | 93.75 | 500 | 0 | 100 | 100 | 500 | 0 | 0 | 150 | archer, archertur, drummer, drummerrus, drummertur (+24) |
| **Казарма** `turbar` | tur | **35000** | 93.75 | 500 | 0 | **400** | **400** | **0** | 0 | 0 | **50** | archer, archertur, drummer, drummerrus, drummertur (+24) |
| **Козацкий дом** `ukrbar` | ukr | **20000** | 93.75 | **300** | 0 | **150** | **150** | **0** | 0 | 0 | **75** | archer, archertur, drummer, drummerrus, drummertur (+24) |
| **Казарма 17в.** `venbar` | ven | 40000 | 93.75 | 500 | 0 | 100 | 100 | 500 | 0 | 0 | 150 | archer, archertur, drummer, drummerrus, drummertur (+24) |

### ba2 — Barracks 18c

| Здание | Нация | HP | Время (с) | cost% | F | W | S | G | I | C | ферма | производит |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| **Казарма 18в.** `ausba2` | aus | 55000 | 5625.0 | 200 | 0 | 1700 | 2950 | 4000 | 0 | 0 | 250 | archersco, bagpiper, chasseur, drummer18, grenadier (+19) |
| **Казарма 18в.** `bavba2` | bav | 55000 | 5625.0 | 200 | 0 | 1700 | 2950 | 4000 | 0 | 0 | 250 | archersco, bagpiper, chasseur, drummer18, grenadier (+19) |
| **Казарма 18в.** `denba2` | den | 55000 | 5625.0 | 200 | 0 | 1700 | 2950 | 4000 | 0 | 0 | 250 | archersco, bagpiper, chasseur, drummer18, grenadier (+19) |
| **Казарма 18в.** `engba2` | eng | 55000 | 5625.0 | 200 | 0 | 1700 | 2950 | 4000 | 0 | 0 | 250 | archersco, bagpiper, chasseur, drummer18, grenadier (+19) |
| **Казарма 18в.** `fraba2` | fra | 55000 | 5625.0 | 200 | 0 | 1700 | 2950 | 4000 | 0 | 0 | 250 | archersco, bagpiper, chasseur, drummer18, grenadier (+19) |
| **Казарма 18в.** `hunba2` | hun | 55000 | 5625.0 | 200 | 0 | 1700 | 2950 | 4000 | 0 | 0 | 250 | archersco, bagpiper, chasseur, drummer18, grenadier (+19) |
| **Казарма 18в.** `netba2` | net | 55000 | 5625.0 | 200 | 0 | 1700 | 2950 | 4000 | 0 | 0 | 250 | archersco, bagpiper, chasseur, drummer18, grenadier (+19) |
| **Казарма 18в.** `pieba2` | pie | 55000 | 5625.0 | 200 | 0 | 1700 | 2950 | 4000 | 0 | 0 | 250 | archersco, bagpiper, chasseur, drummer18, grenadier (+19) |
| **Казарма 18в.** `polba2` | pol | 55000 | 5625.0 | 200 | 0 | 1700 | 2950 | 4000 | 0 | 0 | 250 | archersco, bagpiper, chasseur, drummer18, grenadier (+19) |
| **Казарма 18в.** `porba2` | por | 55000 | 5625.0 | 200 | 0 | 1700 | 2950 | 4000 | 0 | 0 | 250 | archersco, bagpiper, chasseur, drummer18, grenadier (+19) |
| **Казарма 18в.** `pruba2` | pru | 55000 | 5625.0 | 200 | 0 | 1700 | 2950 | 4000 | 0 | 0 | 250 | archersco, bagpiper, chasseur, drummer18, grenadier (+19) |
| **Казарма 18в.** `rusba2` | rus | 55000 | 5625.0 | 200 | 0 | 1700 | 2950 | 4000 | 0 | 0 | 250 | archersco, bagpiper, chasseur, drummer18, grenadier (+19) |
| **Казарма 18в.** `saxba2` | sax | 55000 | 5625.0 | 200 | 0 | 1700 | 2950 | 4000 | 0 | 0 | 250 | archersco, bagpiper, chasseur, drummer18, grenadier (+19) |
| **Замок** `scoba2` | sco | **40000** | **625.0** | **250** | 0 | **640** | **2400** | **2400** | 0 | 0 | **150** | archersco, chasseur, drummer18, grenadier, grenadierbav (+18) |
| **Казарма 18в.** `spaba2` | spa | 55000 | 5625.0 | 200 | 0 | 1700 | 2950 | 4000 | 0 | 0 | 250 | archersco, bagpiper, chasseur, drummer18, grenadier (+19) |
| **Казарма 18в.** `sweba2` | swe | 55000 | 5625.0 | 200 | 0 | 1700 | 2950 | 4000 | 0 | 0 | 250 | archersco, bagpiper, chasseur, drummer18, grenadier (+19) |
| **Казарма 18в.** `swiba2` | swi | 55000 | 5625.0 | 200 | 0 | 1700 | 2950 | 4000 | 0 | 0 | 250 | archersco, bagpiper, chasseur, drummer18, grenadier (+19) |
| **Казарма 18в.** `venba2` | ven | 55000 | 5625.0 | 200 | 0 | 1700 | 2950 | 4000 | 0 | 0 | 250 | archersco, bagpiper, chasseur, drummer18, grenadier (+19) |

### bla — Blacksmith

| Здание | Нация | HP | Время (с) | cost% | F | W | S | G | I | C | ферма | производит |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| **Кузница** `algbla` | alg | **6500** | **109.38** | 400 | 0 | 100 | 30 | 0 | 640 | 0 | 0 | — |
| **Кузница** `ausbla` | aus | 5500 | 93.75 | 400 | 0 | 100 | 30 | 0 | 640 | 0 | 0 | — |
| **Кузница** `bavbla` | bav | 5500 | 93.75 | 400 | 0 | 100 | 30 | 0 | 640 | 0 | 0 | — |
| **Кузница** `denbla` | den | 5500 | 93.75 | 400 | 0 | 100 | 30 | 0 | 640 | 0 | 0 | — |
| **Кузница** `engbla` | eng | 5500 | 93.75 | 400 | 0 | 100 | 30 | 0 | 640 | 0 | 0 | — |
| **Кузница** `frabla` | fra | 5500 | 93.75 | **600** | 0 | 100 | 30 | 0 | 640 | 0 | 0 | — |
| **Кузница** `hunbla` | hun | 5500 | 93.75 | 400 | 0 | 100 | 30 | 0 | 640 | 0 | 0 | — |
| **Кузница** `netbla` | net | 5500 | 93.75 | 400 | 0 | 100 | 30 | 0 | 640 | 0 | 0 | — |
| **Кузница** `piebla` | pie | 5500 | 93.75 | 400 | 0 | 100 | 30 | 0 | 640 | 0 | 0 | — |
| **Кузница** `polbla` | pol | 5500 | 93.75 | 400 | 0 | 100 | 30 | 0 | 640 | 0 | 0 | — |
| **Кузница** `porbla` | por | 5500 | 93.75 | 400 | 0 | 100 | 30 | 0 | 640 | 0 | 0 | — |
| **Кузница** `prubla` | pru | 5500 | 93.75 | 400 | 0 | 100 | 30 | 0 | 640 | 0 | 0 | — |
| **Кузница** `rusbla` | rus | 5500 | 93.75 | 400 | 0 | 100 | 30 | 0 | 640 | 0 | 0 | — |
| **Кузница** `saxbla` | sax | 5500 | 93.75 | 400 | 0 | 100 | 30 | 0 | 640 | 0 | 0 | — |
| **Кузница** `scobla` | sco | 5500 | 93.75 | 400 | 0 | 100 | 30 | 0 | 640 | 0 | 0 | — |
| **Кузница** `spabla` | spa | 5500 | 93.75 | 400 | 0 | 100 | 30 | 0 | 640 | 0 | 0 | — |
| **Кузница** `swebla` | swe | 5500 | 93.75 | 400 | 0 | 100 | 30 | 0 | 640 | 0 | 0 | — |
| **Кузница** `swibla` | swi | 5500 | 93.75 | 400 | 0 | 100 | 30 | 0 | 640 | 0 | 0 | — |
| **Кузница** `turbla` | tur | **6500** | **109.38** | 400 | 0 | 100 | 30 | 0 | 640 | 0 | 0 | — |
| **Кузница** `ukrbla` | ukr | **4500** | **62.5** | 400 | 0 | 100 | 30 | 0 | 640 | 0 | 0 | — |
| **Кузница** `venbla` | ven | 5500 | 93.75 | 400 | 0 | 100 | 30 | 0 | 640 | 0 | 0 | — |

### sta — Stable

| Здание | Нация | HP | Время (с) | cost% | F | W | S | G | I | C | ферма | производит |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| **Конюшня** `algsta` | alg | **55000** | **156.25** | **700** | 0 | **1000** | **2200** | **0** | 0 | 0 | 0 | cossackdon, cossackregister, cossacksich, croat, cuirassier (+25) |
| **Конюшня** `aussta` | aus | 20000 | 625.0 | 200 | 0 | 2500 | 100 | 600 | 0 | 0 | 0 | cossackdon, cossackregister, cossacksich, croat, cuirassier (+25) |
| **Конюшня** `bavsta` | bav | 20000 | 625.0 | 200 | 0 | 2500 | 100 | 600 | 0 | 0 | 0 | cossackdon, cossackregister, cossacksich, croat, cuirassier (+25) |
| **Конюшня** `densta` | den | 20000 | 625.0 | 200 | 0 | 2500 | 100 | 600 | 0 | 0 | 0 | cossackdon, cossackregister, cossacksich, croat, cuirassier (+25) |
| **Конюшня** `engsta` | eng | **25000** | **375.0** | 200 | 0 | **2350** | **0** | **800** | 0 | 0 | 0 | cossackdon, cossackregister, cossacksich, croat, cuirassier (+25) |
| **Конюшня** `frasta` | fra | 20000 | 625.0 | 200 | 0 | 2500 | 100 | 600 | 0 | 0 | 0 | cossackdon, cossackregister, cossacksich, croat, cuirassier (+25) |
| **Конюшня** `hunsta` | hun | 20000 | 625.0 | 200 | 0 | 2500 | 100 | 600 | 0 | 0 | 0 | cossackdon, cossackregister, cossacksich, croat, cuirassier (+26) |
| **Конюшня** `netsta` | net | 20000 | 625.0 | 200 | 0 | 2500 | 100 | 600 | 0 | 0 | 0 | cossackdon, cossackregister, cossacksich, croat, cuirassier (+25) |
| **Конюшня** `piesta` | pie | 20000 | 625.0 | 200 | 0 | 2500 | 100 | 600 | 0 | 0 | 0 | cossackdon, cossackregister, cossacksich, croat, cuirassier (+25) |
| **Конюшня** `polsta` | pol | 20000 | 625.0 | 200 | 0 | 2500 | 100 | 600 | 0 | 0 | 0 | cossackdon, cossackregister, cossacksich, croat, cuirassier (+25) |
| **Конюшня** `porsta` | por | 20000 | 625.0 | 200 | 0 | 2500 | 100 | 600 | 0 | 0 | 0 | cossackdon, cossackregister, cossacksich, croat, cuirassier (+25) |
| **Конюшня** `prusta` | pru | 20000 | 625.0 | 200 | 0 | 2500 | 100 | 600 | 0 | 0 | 0 | cossackdon, cossackregister, cossacksich, croat, cuirassier (+25) |
| **Конюшня** `russta` | rus | **25000** | **375.0** | 200 | 0 | **7950** | **0** | **550** | 0 | 0 | 0 | cossackdon, cossackregister, cossacksich, croat, cuirassier (+25) |
| **Конюшня** `saxsta` | sax | 20000 | 625.0 | 200 | 0 | 2500 | 100 | 600 | 0 | 0 | 0 | cossackdon, cossackregister, cossacksich, croat, cuirassier (+25) |
| **Конюшня** `scosta` | sco | **25000** | **375.0** | 200 | 0 | **2350** | **0** | **800** | 0 | 0 | 0 | cossackdon, cossackregister, cossacksich, croat, cuirassier (+25) |
| **Конюшня** `spasta` | spa | 20000 | 625.0 | 200 | 0 | 2500 | 100 | 600 | 0 | 0 | 0 | cossackdon, cossackregister, cossacksich, croat, cuirassier (+25) |
| **Конюшня** `swesta` | swe | 20000 | 625.0 | 200 | 0 | 2500 | 100 | 600 | 0 | 0 | 0 | cossackdon, cossackregister, cossacksich, croat, cuirassier (+25) |
| **Конюшня** `swista` | swi | 20000 | 625.0 | 200 | 0 | 2500 | 100 | 600 | 0 | 0 | 0 | cossackdon, cossackregister, cossacksich, croat, cuirassier (+25) |
| **Конюшня** `tursta` | tur | **55000** | **156.25** | **700** | 0 | **1000** | **2600** | **0** | 0 | 0 | 0 | cossackdon, cossackregister, cossacksich, croat, cuirassier (+25) |
| **Конюшня** `ukrsta` | ukr | **10000** | **156.25** | **300** | 0 | **3200** | **850** | **850** | 0 | 0 | 0 | cossackdon, cossackregister, cossacksich, croat, cuirassier (+25) |
| **Конюшня** `vensta` | ven | 20000 | 625.0 | 200 | 0 | 2500 | 100 | 600 | 0 | 0 | 0 | cossackdon, cossackregister, cossacksich, croat, cuirassier (+25) |

### tem — Cathedral

| Здание | Нация | HP | Время (с) | cost% | F | W | S | G | I | C | ферма | производит |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| **Мечеть** `algtem` | alg | **5000** | **93.75** | 300 | 0 | 1000 | 1200 | 0 | 500 | 0 | 0 | mullah, padre, pope, priest |
| **Собор** `austem` | aus | 4200 | 156.25 | 300 | 0 | 1000 | 1200 | 0 | 500 | 0 | 0 | mullah, padre, pope, priest |
| **Собор** `bavtem` | bav | 4200 | 156.25 | 300 | 0 | 1000 | 1200 | 0 | 500 | 0 | 0 | mullah, padre, pope, priest |
| **Собор** `dentem` | den | 4200 | 156.25 | 300 | 0 | 1000 | 1200 | 0 | 500 | 0 | 0 | mullah, padre, pope, priest |
| **Собор** `engtem` | eng | 4200 | 156.25 | 300 | 0 | 1000 | 1200 | 0 | 500 | 0 | 0 | mullah, padre, pope, priest |
| **Собор** `fratem` | fra | **6000** | **312.5** | 300 | 0 | **1100** | **2000** | 0 | **600** | 0 | 0 | mullah, padre, pope, priest |
| **Собор** `huntem` | hun | 4200 | 156.25 | 300 | 0 | 1000 | 1200 | 0 | 500 | 0 | 0 | mullah, padre, pope, priest |
| **Собор** `nettem` | net | 4200 | 156.25 | 300 | 0 | 1000 | 1200 | 0 | 500 | 0 | 0 | mullah, padre, pope, priest |
| **Собор** `pietem` | pie | 4200 | 156.25 | 300 | 0 | 1000 | 1200 | 0 | 500 | 0 | 0 | mullah, padre, pope, priest |
| **Собор** `poltem` | pol | 4200 | 156.25 | 300 | 0 | 1000 | 1200 | 0 | 500 | 0 | 0 | mullah, padre, pope, priest |
| **Собор** `portem` | por | 4200 | 156.25 | 300 | 0 | 1000 | 1200 | 0 | 500 | 0 | 0 | mullah, padre, pope, priest |
| **Собор** `prutem` | pru | 4200 | 156.25 | 300 | 0 | 1000 | 1200 | 0 | 500 | 0 | 0 | mullah, padre, pope, priest |
| **Православная церковь** `rustem` | rus | **4500** | 156.25 | 300 | 0 | **1150** | **1650** | **100** | 500 | 0 | 0 | mullah, padre, pope, priest |
| **Собор** `saxtem` | sax | 4200 | 156.25 | 300 | 0 | 1000 | 1200 | 0 | 500 | 0 | 0 | mullah, padre, pope, priest |
| **Собор** `scotem` | sco | 4200 | 156.25 | 300 | 0 | 1000 | 1200 | 0 | 500 | 0 | 0 | mullah, padre, pope, priest |
| **Собор** `spatem` | spa | 4200 | 156.25 | 300 | 0 | 1000 | 1200 | 0 | 500 | 0 | 0 | mullah, padre, pope, priest |
| **Собор** `swetem` | swe | 4200 | 156.25 | 300 | 0 | 1000 | 1200 | 0 | 500 | 0 | 0 | mullah, padre, pope, priest |
| **Собор** `switem` | swi | 4200 | 156.25 | 300 | 0 | 1000 | 1200 | 0 | 500 | 0 | 0 | mullah, padre, pope, priest |
| **Мечеть** `turtem` | tur | **5000** | **93.75** | 300 | 0 | 1000 | 1200 | 0 | 500 | 0 | 0 | mullah, padre, pope, priest |
| **Православная церковь** `ukrtem` | ukr | **5300** | 156.25 | 300 | 0 | **1100** | **1400** | 0 | **300** | 0 | 0 | mullah, padre, pope, priest |
| **Собор** `ventem` | ven | 4200 | 156.25 | 300 | 0 | 1000 | 1200 | 0 | 500 | 0 | 0 | mullah, padre, pope, priest |

### aca — Academy

| Здание | Нация | HP | Время (с) | cost% | F | W | S | G | I | C | ферма | производит |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| **Минарет** `algaca` | alg | **65000** | **156.25** | 300 | 0 | **1450** | 1100 | 0 | 0 | 0 | 0 | — |
| **Академия** `ausaca` | aus | **65000** | 625.0 | 300 | 0 | 1250 | 1100 | 0 | 0 | 0 | 0 | — |
| **Академия** `bavaca` | bav | 63000 | 625.0 | 300 | 0 | 1250 | 1100 | 0 | 0 | 0 | 0 | — |
| **Академия** `denaca` | den | 63000 | 625.0 | 300 | 0 | **1450** | **900** | 0 | 0 | 0 | 0 | — |
| **Академия** `engaca` | eng | 63000 | 625.0 | 300 | 0 | **1150** | **1200** | 0 | 0 | 0 | 0 | — |
| **Академия** `fraaca` | fra | 63000 | 625.0 | 300 | 0 | 1250 | 1100 | 0 | 0 | 0 | 0 | — |
| **Академия** `hunaca` | hun | 63000 | 625.0 | 300 | 0 | 1250 | 1100 | 0 | 0 | 0 | 0 | — |
| **Академия** `netaca` | net | 63000 | 625.0 | 300 | 0 | **1050** | **1230** | 0 | 0 | 0 | 0 | — |
| **Академия** `pieaca` | pie | 63000 | 625.0 | 300 | 0 | 1250 | 1100 | 0 | 0 | 0 | 0 | — |
| **Академия** `polaca` | pol | 63000 | 625.0 | 300 | 0 | **950** | **800** | 0 | 0 | 0 | 0 | — |
| **Академия** `poraca` | por | 63000 | 625.0 | 300 | 0 | 1250 | 1100 | 0 | 0 | 0 | 0 | — |
| **Академия** `pruaca` | pru | 63000 | 625.0 | 300 | 0 | **1200** | **1150** | 0 | 0 | 0 | 0 | — |
| **Академия** `rusaca` | rus | **65000** | **843.75** | 300 | 0 | 1250 | **1300** | 0 | 0 | 0 | 0 | — |
| **Академия** `saxaca` | sax | 63000 | 625.0 | 300 | 0 | 1250 | 1100 | 0 | 0 | 0 | 0 | — |
| **Академия** `scoaca` | sco | 63000 | 625.0 | 300 | 0 | 1250 | 1100 | 0 | 0 | 0 | 0 | — |
| **Академия** `spaaca` | spa | 63000 | 625.0 | 300 | 0 | **1350** | **1000** | 0 | 0 | 0 | 0 | — |
| **Академия** `sweaca` | swe | 63000 | 625.0 | 300 | 0 | **1350** | **1000** | 0 | 0 | 0 | 0 | — |
| **Академия** `swiaca` | swi | 63000 | 625.0 | 300 | 0 | 1250 | 1100 | 0 | 0 | 0 | 0 | — |
| **Минарет** `turaca` | tur | **65000** | **156.25** | 300 | 0 | **1450** | 1100 | 0 | 0 | 0 | 0 | — |
| **Академия** `ukraca` | ukr | **65000** | **46.88** | 300 | 0 | **1350** | **1200** | 0 | 0 | 0 | 0 | — |
| **Академия** `venaca` | ven | 63000 | 625.0 | 300 | 0 | **1090** | **1260** | 0 | 0 | 0 | 0 | — |

### art — Artillery Depot

| Здание | Нация | HP | Время (с) | cost% | F | W | S | G | I | C | ферма | производит |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| **Артиллерийское депо** `algart` | alg | 40000 | 245.94 | 200 | 0 | 100 | 1000 | 0 | 0 | 1400 | 0 | cannon, framegun, howitzer, mortar, multicannon |
| **Артиллерийское депо** `ausart` | aus | 40000 | 245.94 | 200 | 0 | 100 | 1000 | 0 | 0 | 1400 | 0 | cannon, framegun, howitzer, mortar, multicannon |
| **Артиллерийское депо** `bavart` | bav | 40000 | 245.94 | 200 | 0 | 100 | 1000 | 0 | 0 | 1400 | 0 | cannon, framegun, howitzer, mortar, multicannon |
| **Артиллерийское депо** `denart` | den | 40000 | 245.94 | 200 | 0 | 100 | 1000 | 0 | 0 | 1400 | 0 | cannon, framegun, howitzer, mortar, multicannon |
| **Артиллерийское депо** `engart` | eng | 40000 | 245.94 | 200 | 0 | 100 | 1000 | 0 | 0 | 1400 | 0 | cannon, framegun, howitzer, mortar, multicannon |
| **Артиллерийское депо** `fraart` | fra | 40000 | 245.94 | 200 | 0 | 100 | 1000 | 0 | 0 | 1400 | 0 | cannon, framegun, howitzer, mortar, multicannon |
| **Артиллерийское депо** `hunart` | hun | 40000 | 245.94 | 200 | 0 | 100 | 1000 | 0 | 0 | 1400 | 0 | cannon, framegun, howitzer, mortar, multicannon |
| **Артиллерийское депо** `netart` | net | 40000 | 245.94 | 200 | 0 | 100 | 1000 | 0 | 0 | 1400 | 0 | cannon, framegun, howitzer, mortar, multicannon |
| **Артиллерийское депо** `pieart` | pie | 40000 | 245.94 | 200 | 0 | 100 | 1000 | 0 | 0 | 1400 | 0 | cannon, framegun, howitzer, mortar, multicannon |
| **Артиллерийское депо** `polart` | pol | 40000 | 245.94 | 200 | 0 | 100 | 1000 | 0 | 0 | 1400 | 0 | cannon, framegun, howitzer, mortar, multicannon |
| **Артиллерийское депо** `porart` | por | 40000 | 245.94 | 200 | 0 | 100 | 1000 | 0 | 0 | 1400 | 0 | cannon, framegun, howitzer, mortar, multicannon |
| **Артиллерийское депо** `pruart` | pru | 40000 | 245.94 | 200 | 0 | 100 | 1000 | 0 | 0 | 1400 | 0 | cannon, framegun, howitzer, mortar, multicannon |
| **Артиллерийское депо** `rusart` | rus | 40000 | 245.94 | 200 | 0 | 100 | 1000 | 0 | 0 | 1400 | 0 | cannon, framegun, howitzer, mortar, multicannon |
| **Артиллерийское депо** `saxart` | sax | 40000 | 245.94 | 200 | 0 | 100 | 1000 | 0 | 0 | 1400 | 0 | cannon, framegun, howitzer, mortar, multicannon |
| **Артиллерийское депо** `scoart` | sco | 40000 | 245.94 | 200 | 0 | 100 | 1000 | 0 | 0 | 1400 | 0 | cannon, framegun, howitzer, mortar, multicannon |
| **Артиллерийское депо** `spaart` | spa | 40000 | 245.94 | 200 | 0 | 100 | 1000 | 0 | 0 | 1400 | 0 | cannon, framegun, howitzer, mortar, multicannon |
| **Артиллерийское депо** `sweart` | swe | 40000 | 245.94 | 200 | 0 | 100 | 1000 | 0 | 0 | 1400 | 0 | cannon, framegun, howitzer, mortar, multicannon |
| **Артиллерийское депо** `swiart` | swi | 40000 | 245.94 | 200 | 0 | 100 | 1000 | 0 | 0 | 1400 | 0 | cannon, framegun, howitzer, mortar, multicannon |
| **Артиллерийское депо** `turart` | tur | 40000 | 245.94 | 200 | 0 | **500** | **1200** | 0 | 0 | 1400 | 0 | cannon, framegun, howitzer, mortar, multicannon |
| **Артиллерийское депо** `ukrart` | ukr | 40000 | 245.94 | 200 | 0 | **4250** | **4400** | **100** | 0 | 1400 | 0 | cannon, framegun, howitzer, mortar, multicannon |
| **Артиллерийское депо** `venart` | ven | 40000 | 245.94 | 200 | 0 | 100 | 1000 | 0 | 0 | 1400 | 0 | cannon, framegun, howitzer, mortar, multicannon |

### dip — Diplomatic Center

| Здание | Нация | HP | Время (с) | cost% | F | W | S | G | I | C | ферма | производит |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| **Дипломатический центр** `algdip` | alg | **5500** | 312.5 | 100 | 0 | **4600** | **2020** | 0 | 0 | 0 | 0 | archerdip, archerturdip, cossacksichdip, dragoon18dip, grenadierdip (+3) |
| **Дипломатический центр** `ausdip` | aus | 4500 | 312.5 | 100 | 0 | 4900 | 1700 | 0 | 0 | 0 | 0 | archerdip, archerturdip, cossacksichdip, dragoon18dip, grenadierdip (+3) |
| **Дипломатический центр** `bavdip` | bav | 4500 | 312.5 | 100 | 0 | 4900 | 1700 | 0 | 0 | 0 | 0 | archerdip, archerturdip, cossacksichdip, dragoon18dip, grenadierdip (+3) |
| **Дипломатический центр** `dendip` | den | 4500 | 312.5 | 100 | 0 | 4900 | 1700 | 0 | 0 | 0 | 0 | archerdip, archerturdip, cossacksichdip, dragoon18dip, grenadierdip (+3) |
| **Дипломатический центр** `engdip` | eng | 4500 | 312.5 | 100 | 0 | 4900 | 1700 | 0 | 0 | 0 | 0 | archerdip, archerturdip, cossacksichdip, dragoon18dip, grenadierdip (+3) |
| **Дипломатический центр** `fradip` | fra | 4500 | 312.5 | 100 | 0 | 4900 | 1700 | 0 | 0 | 0 | 0 | archerdip, archerturdip, cossacksichdip, dragoon18dip, grenadierdip (+3) |
| **Дипломатический центр** `hundip` | hun | 4500 | 312.5 | 100 | 0 | 4900 | 1700 | 0 | 0 | 0 | 0 | archerdip, archerturdip, cossacksichdip, dragoon18dip, grenadierdip (+3) |
| **Дипломатический центр** `netdip` | net | 4500 | 312.5 | 100 | 0 | 4900 | 1700 | 0 | 0 | 0 | 0 | archerdip, archerturdip, cossacksichdip, dragoon18dip, grenadierdip (+3) |
| **Дипломатический центр** `piedip` | pie | 4500 | 312.5 | 100 | 0 | 4900 | 1700 | 0 | 0 | 0 | 0 | archerdip, archerturdip, cossacksichdip, dragoon18dip, grenadierdip (+3) |
| **Дипломатический центр** `poldip` | pol | 4500 | 312.5 | 100 | 0 | 4900 | 1700 | 0 | 0 | 0 | 0 | archerdip, archerturdip, cossacksichdip, dragoon18dip, grenadierdip (+3) |
| **Дипломатический центр** `pordip` | por | 4500 | 312.5 | 100 | 0 | 4900 | 1700 | 0 | 0 | 0 | 0 | archerdip, archerturdip, cossacksichdip, dragoon18dip, grenadierdip (+3) |
| **Дипломатический центр** `prudip` | pru | 4500 | 312.5 | 100 | 0 | 4900 | 1700 | 0 | 0 | 0 | 0 | archerdip, archerturdip, cossacksichdip, dragoon18dip, grenadierdip (+3) |
| **Дипломатический центр** `rusdip` | rus | **6500** | 312.5 | 100 | 0 | **7900** | **3700** | 0 | 0 | 0 | 0 | archerdip, archerturdip, cossacksichdip, dragoon18dip, grenadierdip (+3) |
| **Дипломатический центр** `saxdip` | sax | 4500 | 312.5 | 100 | 0 | 4900 | 1700 | 0 | 0 | 0 | 0 | archerdip, archerturdip, cossacksichdip, dragoon18dip, grenadierdip (+3) |
| **Дипломатический центр** `scodip` | sco | 4500 | 312.5 | 100 | 0 | 4900 | 1700 | 0 | 0 | 0 | 0 | archerdip, archerturdip, cossacksichdip, dragoon18dip, grenadierdip (+3) |
| **Дипломатический центр** `spadip` | spa | 4500 | 312.5 | 100 | 0 | 4900 | 1700 | 0 | 0 | 0 | 0 | archerdip, archerturdip, cossacksichdip, dragoon18dip, grenadierdip (+3) |
| **Дипломатический центр** `swedip` | swe | 4500 | 312.5 | 100 | 0 | 4900 | 1700 | 0 | 0 | 0 | 0 | archerdip, archerturdip, cossacksichdip, dragoon18dip, grenadierdip (+3) |
| **Дипломатический центр** `swidip` | swi | 4500 | 312.5 | 100 | 0 | 4900 | 1700 | 0 | 0 | 0 | 0 | archerdip, archerturdip, cossacksichdip, dragoon18dip, grenadierdip (+3) |
| **Дипломатический центр** `turdip` | tur | **5500** | 312.5 | 100 | 0 | **4600** | **2020** | 0 | 0 | 0 | 0 | archerdip, archerturdip, cossacksichdip, dragoon18dip, grenadierdip (+3) |
| **Дипломатический центр** `ukrdip` | ukr | **5000** | 312.5 | 100 | 0 | **3900** | **2700** | 0 | 0 | 0 | 0 | archerdip, archerturdip, cossacksichdip, dragoon18dip, grenadierdip (+3) |
| **Дипломатический центр** `vendip` | ven | 4500 | 312.5 | 100 | 0 | 4900 | 1700 | 0 | 0 | 0 | 0 | archerdip, archerturdip, cossacksichdip, dragoon18dip, grenadierdip (+3) |

## Общие постройки (по кластерам)

### mil — Mill

| Здание (cluster) | Нации | HP | Время (с) | cost% | F | W | S | G | I | C | Доп. |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| **Мельница** `eurmil` | aus, bav, den, eng, fra, hun, net, pie, pol, por, pru, sax, sco, spa, swe, swi, ven | 20000 | 93.75 | 200 | 0 | 30 | 150 | 0 | 0 | 0 | — |
| **Мельница** `rusmil` | rus, ukr | 15000 | 93.75 | 200 | 0 | 210 | 0 | 0 | 0 | 0 | — |
| **Мельница** `turmil` | alg, tur | 20000 | 93.75 | 200 | 0 | 30 | 150 | 0 | 0 | 0 | — |

### sto — Storehouse

| Здание (cluster) | Нации | HP | Время (с) | cost% | F | W | S | G | I | C | Доп. |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| **Склад** `eursto` | aus, bav, den, eng, fra, hun, net, pie, pru, sax, sco, swe, swi, ven | 10000 | 31.25 | 150 | 0 | 50 | 20 | 0 | 0 | 0 | — |
| **Склад** `russto` | pol, rus, ukr | 10000 | 31.25 | 200 | 0 | 50 | 20 | 0 | 0 | 0 | — |
| **Склад** `spasto` | por, spa | 10000 | 31.25 | 150 | 0 | 20 | 20 | 0 | 0 | 0 | — |
| **Склад** `tursto` | alg, tur | 10000 | 31.25 | 200 | 0 | 30 | 10 | 0 | 0 | 0 | — |

### mar — Market

| Здание (cluster) | Нации | HP | Время (с) | cost% | F | W | S | G | I | C | Доп. |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| **Рынок** `eurmar` | aus, bav, den, eng, fra, hun, net, pie, pol, pru, sax, sco, swe, swi, ven | 4000 | 234.38 | 2000 | 0 | 450 | 0 | 0 | 0 | 0 | — |
| **Рынок** `rusmar` | rus, ukr | 4000 | 234.38 | 2000 | 0 | 450 | 0 | 0 | 0 | 0 | — |
| **Рынок** `spamar` | por, spa | 4000 | 156.25 | 2000 | 0 | 450 | 0 | 0 | 0 | 0 | — |
| **Базар** `turmar` | alg, tur | 4500 | 234.38 | 1500 | 0 | 450 | 150 | 0 | 0 | 0 | — |

### por — Shipyard

| Здание (cluster) | Нации | HP | Время (с) | cost% | F | W | S | G | I | C | Доп. |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| **Порт** `eurpor` | aus, bav, den, eng, fra, hun, net, pie, pol, pru, sax, sco, spa, swe, swi, ven | 50000 | 1562.5 | 150 | 0 | 1600 | 800 | 0 | 400 | 0 | — |
| **Порт** `porpor` | por | 50000 | 1562.5 | 150 | 0 | 1600 | 800 | 0 | 400 | 0 | урон 1000; дальн. 28.1t; содержание {"gold": 250} |
| **Порт** `ruspor` | rus | 45000 | 1562.5 | 150 | 0 | 1200 | 800 | 0 | 400 | 0 | — |
| **Порт** `turpor` | alg, tur | 40000 | 1562.5 | 150 | 0 | 800 | 800 | 0 | 400 | 0 | — |
| **Порт** `ukrpor` | ukr | 45000 | 1562.5 | 150 | 0 | 2000 | 0 | 0 | 0 | 0 | — |

### tow — Tower

| Здание (cluster) | Нации | HP | Время (с) | cost% | F | W | S | G | I | C | Доп. |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| **Башня** `eurtow` | aus, bav, den, eng, fra, hun, net, pie, pol, por, pru, sax, sco, spa, swe, swi, ven | 20000 | 1230.31 | 120 | 0 | 100 | 100 | 150 | 0 | 0 | урон 1000; дальн. 28.1t; содержание {"gold": 500} |
| **Башня** `rustow` | rus | 21000 | 1476.56 | 125 | 0 | 100 | 100 | 150 | 0 | 0 | урон 1000; дальн. 28.1t; содержание {"gold": 500} |
| **Башня** `turtow` | alg, tur | 22500 | 984.38 | 125 | 0 | 150 | 90 | 100 | 0 | 0 | урон 1200; дальн. 30.0t; содержание {"gold": 500} |

### gol — Gold Mine

| Здание (cluster) | Нации | HP | Время (с) | cost% | F | W | S | G | I | C | Доп. |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| **Шахта** `eurgol` | alg, aus, bav, den, eng, fra, hun, net, pie, pol, por, pru, rus, sax, sco, spa, swe, swi, tur, ukr, ven | 2500 | 93.75 | 0 | 0 | 100 | 100 | 0 | 0 | 0 | производит {"gold": 13}; крестьян 5 |

### iro — Iron Mine

| Здание (cluster) | Нации | HP | Время (с) | cost% | F | W | S | G | I | C | Доп. |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| **Шахта** `euriro` | alg, aus, bav, den, eng, fra, hun, net, pie, pol, por, pru, rus, sax, sco, spa, swe, swi, tur, ukr, ven | 2500 | 93.75 | 0 | 0 | 100 | 100 | 0 | 0 | 0 | производит {"iron": 13}; крестьян 5 |

### coa — Coal Mine

| Здание (cluster) | Нации | HP | Время (с) | cost% | F | W | S | G | I | C | Доп. |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| **Шахта** `eurcoa` | alg, aus, bav, den, eng, fra, hun, net, pie, pol, por, pru, rus, sax, sco, spa, swe, swi, tur, ukr, ven | 2500 | 93.75 | 0 | 0 | 100 | 100 | 0 | 0 | 0 | производит {"coal": 13}; крестьян 5 |

### swa — Stone Wall

| Здание (cluster) | Нации | HP | Время (с) | cost% | F | W | S | G | I | C | Доп. |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| **Стена** `eurswa` | aus, bav, den, eng, fra, hun, net, pie, pol, por, pru, sax, sco, spa, swe, swi, ven | 50000 | 90.0 | 0 | 0 | 0 | 50 | 0 | 0 | 0 | содержание {"stone": 250} |
| **Стена** `russwa` | rus | 50000 | 200.0 | 0 | 0 | 0 | 60 | 0 | 0 | 0 | содержание {"stone": 200} |
| **Стена** `turswa` | alg, tur | 50000 | 120.0 | 0 | 0 | 0 | 60 | 0 | 0 | 0 | содержание {"stone": 150} |

### sga — Stone Gate

| Здание (cluster) | Нации | HP | Время (с) | cost% | F | W | S | G | I | C | Доп. |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| **Каменные ворота** `eursga` | aus, bav, den, eng, fra, hun, net, pie, pol, por, pru, sax, sco, spa, swe, swi, ven | 50000 | 90.0 | 0 | 0 | 0 | 50 | 0 | 0 | 0 | содержание {"stone": 250} |
| **Каменные ворота** `russga` | rus | 50000 | 200.0 | 0 | 0 | 0 | 60 | 0 | 0 | 0 | содержание {"stone": 200} |
| **Каменные ворота** `tursga` | alg, tur | 50000 | 120.0 | 0 | 0 | 0 | 60 | 0 | 0 | 0 | содержание {"stone": 150} |

## Шахты — апгрейды (gol/iro/coa)

Каждая шахта начинается с `peasantabsorber=5`. 6 апгрейдов накопительно доводят до **95 крестьян** на шахту.

| Уровень | +работников | Еда | Золото | Накопительно |
|---|---:|---:|---:|---:|
| `eurgol.1` | +5 | 1000 | 1250 | 10 |
| `eurgol.2` | +8 | 5250 | 4950 | 18 |
| `eurgol.3` | +10 | 12500 | 9250 | 28 |
| `eurgol.4` | +12 | 15800 | 18500 | 40 |
| `eurgol.5` | +15 | 19800 | 21050 | 55 |
| `eurgol.6` | +40 | 50200 | 25950 | 95 |