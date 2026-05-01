# 03. Здания

[← Index](README.md)

Здания делятся на **per-nation** (`<nat>+suffix`, например `auscen` = ратуша Австрии) и **common** (`<cluster>+suffix`, общие для группы наций: `eur`/`rus`/`tur`/`spa`/`ukr`/`por`).

Цены ниже — для **первого** экземпляра. Цена N-го здания того же типа = `floor(base × (costpercent/100)^(N-1))`. Готовые таблицы N=1..6 для всех зданий — в [`../reports/economy/scaling_prices.md`](../reports/economy/scaling_prices.md), генератор — [`compute/compute_scaling.py`](../../compute/compute_scaling.py).

## Расшифровка колонок

| Колонка | Значение |
|---|---|
| **Здание** | Локализованное имя + `sid` |
| **Нация / Нации** | Какие нации имеют это здание (для common-кластеров — список) |
| **HP** | Очки здоровья достроенного здания |
| **Время (g-сек)** | `buildtime` в игровых секундах. Для зданий хранится с множителем `gc_buildtime_modifier = 10`, т.е. `frames × 10/32`. С N строителями реальное время = `time × 1.13 / N`. См. [recon/world/economy/building_mechanics.md](../recon/world/economy/building_mechanics.md). |
| **cost%** | `costpercent` — множитель цены каждого следующего экземпляра. 100 = одинаковая, 300 = ×3 за второе. 0 = без масштабирования. |
| **F / W / S / G / I / C** | Цена в ресурсах: **Food / Wood / Stone / Gold / Iron / Coal**. |
| **ферма** | `farm` — на сколько единиц это здание поднимает лимит населения. |
| **производит** | Список `sid` юнитов, которых здание умеет создавать. |
| **Доп.** | Прочее: оружие башен, гарнизон, доход шахт. |

**Жирным** в таблицах ниже — отклонения от базового значения (мода по столбцу), чтобы быстро видеть, чем нация отличается от большинства.

## Жизненный цикл здания — кратко

Полный разбор стройки, ремонта, отмены и разрушения — в
[`../recon/world/economy/building_mechanics.md`](../recon/world/economy/building_mechanics.md).
Здесь — таблица ключевых констант для быстрого обзора.

| Этап | Ключевая величина | Заметка |
|---|---:|---|
| Прогресс стройки за один удар крестьянина | `delta = 0.359 / buildtime` | анимация `construct` = 13 кадров |
| Время стройки с N строителями | `buildtime × 1.13 / N` | 13 % накладных на координацию |
| Лимит строителей одновременно | `bbox_cols + bbox_rows` | Manhattan-периметр |
| Восстановление HP за один ремонт-удар | `gc_gameplay_repairhp = 20` | анимация `workfood` = 22 кадра ≈ 0.69 g-сек |
| HP-скорость одного ремонтника | ~ 29 HP / g-сек ≈ 41 HP / real-сек @ fast | штрафа 1.13× при N ремонтниках нет |
| Shield в стройке | `shield / 3` | здание уязвимо до завершения |
| Захват в стройке | возможен для **любого** sid | даже башню захватывают, пока строится |
| `gc_building_deathtime_0/1` | 30 g-сек на каждую стадию | 60 для шахт |
| Refund при отмене Foundation | **100 %** | через GUI-handler `_misc_GUICancelBuilding` |
| Refund при отмене заказа юнита | **100 %** от списанного | через `_unit_CancelUnitProduction` |
| Refund при OnDeath работающего здания | очередь заказов прокручивается обратно | оплаченные юниты и апгрейды возвращаются |

## Эпохальный переход: 17 → 18 век — таблица

Полный разбор пререквизитов, цепочки строительства и стратегии — в
[`../recon/world/economy/upgrades_application.md` §7.5](../recon/world/economy/upgrades_application.md).
Здесь — таблица стоимости `<nat>cen.1` по нациям.

### Цена `<nat>cen.1` (апгрейд перехода в 18 век)

| Нация | Food | Gold | Iron | Coal | Пререквизиты |
|---|---:|---:|---:|---:|---|
| Большинство (стандарт) | 30 000 | 5 000 | 2 000 | 2 000 | aca + tem + art |
| `fra` Франция | 40 000 | 3 500 | 4 000 | 2 000 | aca + tem + art |
| `eng` Англия | 25 000 | 5 000 | 5 500 | 2 000 | aca + tem + art |
| `pol` Польша | 30 000 | 4 800 | 2 200 | 2 000 | aca + tem + art |
| `ukr` / `tur` / `alg` | 30 000 | 5 000 | 2 000 | 2 000 | у этих наций отсутствует полный набор зданий → `ba2` недоступен |

`buildtime = 9.38 g-сек` (≈ 6.7 real-сек @ fast) — сам апгрейд
быстрый. Узкое место — собрать **Академию + Собор + Артиллерийское
депо** (~ 7 000 wood + 4 000 stone + 1 000 gold + ~36 real-мин при
одном строителе на каждое здание). Полная таблица всех апгрейдов —
в [05_upgrades.md → cen — Городской центр](05_upgrades.md#cen--городской центр-переход-эпохи).

**Заперты в 17 веке** (нет `<nat>ba2`): `tur`, `alg`, `ukr` — у
них отсутствуют `musketeer18`, `grenadier`, `dragoon18`. Они
компенсируют это уникальными юнитами 17 в. (Янычары, Мамлюки,
Козаки и т. п.).

## Содержание

**[Постройки по нациям](#постройки-по-нациям)**
  - [cen — Городской центр](#cen--городской-центр)
  - [hou — Дом](#hou--дом)
  - [bar — Казарма 17 в.](#bar--казарма-17-в)
  - [ba2 — Казарма 18 в.](#ba2--казарма-18-в)
  - [bla — Кузница](#bla--кузница)
  - [sta — Конюшня](#sta--конюшня)
  - [tem — Собор](#tem--собор)
  - [aca — Академия](#aca--академия)
  - [art — Артиллерийское депо](#art--артиллерийское-депо)
  - [dip — Дипломатический центр](#dip--дипломатический-центр)
**[Общие постройки (по кластерам)](#общие-постройки-по-кластерам)**
  - [mil — Мельница](#mil--мельница)
  - [sto — Склад](#sto--склад)
  - [mar — Рынок](#mar--рынок)
  - [por — Порт](#por--порт)
  - [tow — Башня](#tow--башня)
  - [gol — Золотая шахта](#gol--золотая-шахта)
  - [iro — Железная шахта](#iro--железная-шахта)
  - [coa — Угольная шахта](#coa--угольная-шахта)
  - [swa — Каменная стена](#swa--каменная-стена)
  - [sga — Каменные ворота](#sga--каменные-ворота)
**[Шахты — апгрейды (gol/iro/coa)](#шахты--апгрейды-golirocoa)**

## Постройки по нациям

Сводка: для каждого типа зданий — параметры по всем нациям (где они есть). **Жирным** — отклонения от базового значения (мода по столбцу).

### cen — Городской центр

| Здание | Нация | HP | Время (g-сек) | cost% | F | W | S | G | I | C | ферма | производит |
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

### hou — Дом

| Здание | Нация | HP | Время (g-сек) | cost% | F | W | S | G | I | C | ферма | производит |
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

### bar — Казарма 17 в.

| Здание | Нация | HP | Время (g-сек) | cost% | F | W | S | G | I | C | ферма | производит |
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

### ba2 — Казарма 18 в.

| Здание | Нация | HP | Время (g-сек) | cost% | F | W | S | G | I | C | ферма | производит |
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

### bla — Кузница

| Здание | Нация | HP | Время (g-сек) | cost% | F | W | S | G | I | C | ферма | производит |
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

### sta — Конюшня

| Здание | Нация | HP | Время (g-сек) | cost% | F | W | S | G | I | C | ферма | производит |
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

### tem — Собор

| Здание | Нация | HP | Время (g-сек) | cost% | F | W | S | G | I | C | ферма | производит |
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

### aca — Академия

| Здание | Нация | HP | Время (g-сек) | cost% | F | W | S | G | I | C | ферма | производит |
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

### art — Артиллерийское депо

| Здание | Нация | HP | Время (g-сек) | cost% | F | W | S | G | I | C | ферма | производит |
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

### dip — Дипломатический центр

| Здание | Нация | HP | Время (g-сек) | cost% | F | W | S | G | I | C | ферма | производит |
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

### mil — Мельница

| Здание (cluster) | Нации | HP | Время (g-сек) | cost% | F | W | S | G | I | C | Доп. |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| **Мельница** `eurmil` | aus, bav, den, eng, fra, hun, net, pie, pol, por, pru, sax, sco, spa, swe, swi, ven | 20000 | 93.75 | 200 | 0 | 30 | 150 | 0 | 0 | 0 | — |
| **Мельница** `rusmil` | rus, ukr | 15000 | 93.75 | 200 | 0 | 210 | 0 | 0 | 0 | 0 | — |
| **Мельница** `turmil` | alg, tur | 20000 | 93.75 | 200 | 0 | 30 | 150 | 0 | 0 | 0 | — |

### sto — Склад

| Здание (cluster) | Нации | HP | Время (g-сек) | cost% | F | W | S | G | I | C | Доп. |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| **Склад** `eursto` | aus, bav, den, eng, fra, hun, net, pie, pru, sax, sco, swe, swi, ven | 10000 | 31.25 | 150 | 0 | 50 | 20 | 0 | 0 | 0 | — |
| **Склад** `russto` | pol, rus, ukr | 10000 | 31.25 | 200 | 0 | 50 | 20 | 0 | 0 | 0 | — |
| **Склад** `spasto` | por, spa | 10000 | 31.25 | 150 | 0 | 20 | 20 | 0 | 0 | 0 | — |
| **Склад** `tursto` | alg, tur | 10000 | 31.25 | 200 | 0 | 30 | 10 | 0 | 0 | 0 | — |

### mar — Рынок

| Здание (cluster) | Нации | HP | Время (g-сек) | cost% | F | W | S | G | I | C | Доп. |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| **Рынок** `eurmar` | aus, bav, den, eng, fra, hun, net, pie, pol, pru, sax, sco, swe, swi, ven | 4000 | 234.38 | 2000 | 0 | 450 | 0 | 0 | 0 | 0 | — |
| **Рынок** `rusmar` | rus, ukr | 4000 | 234.38 | 2000 | 0 | 450 | 0 | 0 | 0 | 0 | — |
| **Рынок** `spamar` | por, spa | 4000 | 156.25 | 2000 | 0 | 450 | 0 | 0 | 0 | 0 | — |
| **Базар** `turmar` | alg, tur | 4500 | 234.38 | 1500 | 0 | 450 | 150 | 0 | 0 | 0 | — |

### por — Порт

| Здание (cluster) | Нации | HP | Время (g-сек) | cost% | F | W | S | G | I | C | Доп. |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| **Порт** `eurpor` | aus, bav, den, eng, fra, hun, net, pie, pol, pru, sax, sco, spa, swe, swi, ven | 50000 | 1562.5 | 150 | 0 | 1600 | 800 | 0 | 400 | 0 | — |
| **Порт** `porpor` | por | 50000 | 1562.5 | 150 | 0 | 1600 | 800 | 0 | 400 | 0 | урон 1000; дальн. 28.1t; содержание {"gold": 250} |
| **Порт** `ruspor` | rus | 45000 | 1562.5 | 150 | 0 | 1200 | 800 | 0 | 400 | 0 | — |
| **Порт** `turpor` | alg, tur | 40000 | 1562.5 | 150 | 0 | 800 | 800 | 0 | 400 | 0 | — |
| **Порт** `ukrpor` | ukr | 45000 | 1562.5 | 150 | 0 | 2000 | 0 | 0 | 0 | 0 | — |

### tow — Башня

| Здание (cluster) | Нации | HP | Время (g-сек) | cost% | F | W | S | G | I | C | Доп. |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| **Башня** `eurtow` | aus, bav, den, eng, fra, hun, net, pie, pol, por, pru, sax, sco, spa, swe, swi, ven | 20000 | 1230.31 | 120 | 0 | 100 | 100 | 150 | 0 | 0 | урон 1000; дальн. 28.1t; содержание {"gold": 500} |
| **Башня** `rustow` | rus | 21000 | 1476.56 | 125 | 0 | 100 | 100 | 150 | 0 | 0 | урон 1000; дальн. 28.1t; содержание {"gold": 500} |
| **Башня** `turtow` | alg, tur | 22500 | 984.38 | 125 | 0 | 150 | 90 | 100 | 0 | 0 | урон 1200; дальн. 30.0t; содержание {"gold": 500} |

#### Башня — кратко

Полный разбор стрельбы, обзора, гарнизона и стратегии — в
[`../recon/world/combat/towers.md`](../recon/world/combat/towers.md).
Краткие параметры базовой европейской башни (`eurtow`):

| Параметр | Значение | Замечание |
|---|---:|---|
| HP | 20 000 | rus 21 000, tur 22 500 |
| `vision` | 3 → 32 тайла FOW | меньше, чем у среднего гусара |
| `searchradius` | 1400 px = 26.25 t | радиус автозахвата цели |
| Урон | 1000 | `cannonball` |
| `weapon_pause` | 400 кадров = 12.5 g-сек | rus 9.4 g-сек, tur 15.6 g-сек |
| Дальность выстрела | 1500 px = 28.13 t | tur 30 t |
| Разброс | 100 px = 1.88 t | rus 125 |
| Стоимость выстрела | 10 iron + 30 coal | tur: 15 iron + 40 coal |
| Содержание | `consume[gold] = 500` → **0.8 gold / г-сек** (≈ 67 / real-мин @ fast) | формула `× 32 / 20000`, при `gold = 0` башня молча перестаёт стрелять |
| Захват | `bcapture = False` | башня **никогда** не захватывается после постройки |

5 уровней апгрейда `eurtow.1..5` снижают `weapon_pause` до
× 0.467 от базы → частота огня **× 2.14**. Полный список — в
[05_upgrades.md → tow](05_upgrades.md#tow--башня-скорость-перезарядки).
### gol — Золотая шахта

| Здание (cluster) | Нации | HP | Время (g-сек) | cost% | F | W | S | G | I | C | Доп. |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| **Шахта** `eurgol` | alg, aus, bav, den, eng, fra, hun, net, pie, pol, por, pru, rus, sax, sco, spa, swe, swi, tur, ukr, ven | 2500 | 93.75 | 0 | 0 | 100 | 100 | 0 | 0 | 0 | производит {"gold": 13}; крестьян 5 |

### iro — Железная шахта

| Здание (cluster) | Нации | HP | Время (g-сек) | cost% | F | W | S | G | I | C | Доп. |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| **Шахта** `euriro` | alg, aus, bav, den, eng, fra, hun, net, pie, pol, por, pru, rus, sax, sco, spa, swe, swi, tur, ukr, ven | 2500 | 93.75 | 0 | 0 | 100 | 100 | 0 | 0 | 0 | производит {"iron": 13}; крестьян 5 |

### coa — Угольная шахта

| Здание (cluster) | Нации | HP | Время (g-сек) | cost% | F | W | S | G | I | C | Доп. |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| **Шахта** `eurcoa` | alg, aus, bav, den, eng, fra, hun, net, pie, pol, por, pru, rus, sax, sco, spa, swe, swi, tur, ukr, ven | 2500 | 93.75 | 0 | 0 | 100 | 100 | 0 | 0 | 0 | производит {"coal": 13}; крестьян 5 |

### swa — Каменная стена

| Здание (cluster) | Нации | HP | Время (g-сек) | cost% | F | W | S | G | I | C | Доп. |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| **Стена** `eurswa` | aus, bav, den, eng, fra, hun, net, pie, pol, por, pru, sax, sco, spa, swe, swi, ven | 50000 | 90.0 | 0 | 0 | 0 | 50 | 0 | 0 | 0 | содержание {"stone": 250} |
| **Стена** `russwa` | rus | 50000 | 200.0 | 0 | 0 | 0 | 60 | 0 | 0 | 0 | содержание {"stone": 200} |
| **Стена** `turswa` | alg, tur | 50000 | 120.0 | 0 | 0 | 0 | 60 | 0 | 0 | 0 | содержание {"stone": 150} |

### sga — Каменные ворота

| Здание (cluster) | Нации | HP | Время (g-сек) | cost% | F | W | S | G | I | C | Доп. |
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