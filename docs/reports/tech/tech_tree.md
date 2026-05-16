# Cossacks 3 — Tech Tree (по нациям)

Граф зависимостей: что нужно построить или исследовать перед чем. Извлечено из `_country_AddFixedProduceWithAccessControl` и `_country_AddUpgradeWithAccessControl` (параметры `req0`..`req7`). Источник истины — [`derived/tech_tree.json`](../../derived/tech_tree.json).

**Условные обозначения:**
- `[B]` — здание, `[U]` — юнит, `[T]` — апгрейд (technology, исследование)
- `→ X, Y` — для разблокировки нужны X и Y одновременно
- Для зданий показана базовая цена (см. [`scaling_prices.md`](../economy/scaling_prices.md) для N>1)

## Граф зданий (Австрия как репрезентативный пример)

Граф показывает зависимости постройки одного здания от другого. Сплошные стрелки — `prereqs` из `country.script`, пунктирные — связь «здание → его апгрейд» (например, `auscen → auscen.1`, переход в 18 век). У других наций граф структурно идентичен — отличаются только нация-специфичные имена `<nat>cen`, `<nat>bar` и т. д.

```mermaid
graph LR
    ausaca["Академия<br/><code>ausaca</code>"]
    ausart["Артдепо<br/><code>ausart</code>"]
    ausba2["Казарма 18<br/><code>ausba2</code>"]
    ausbar["Казарма 17<br/><code>ausbar</code>"]
    ausbla["Кузница<br/><code>ausbla</code>"]
    auscen["Город. центр<br/><code>auscen</code>"]
    ausdip["Диппцентр<br/><code>ausdip</code>"]
    aushou["Дом<br/><code>aushou</code>"]
    aussta["Конюшня<br/><code>aussta</code>"]
    austem["Собор<br/><code>austem</code>"]
    eurcoa["Шахта (coal)<br/><code>eurcoa</code>"]
    eurgol["Шахта (gold)<br/><code>eurgol</code>"]
    euriro["Шахта (iron)<br/><code>euriro</code>"]
    eurmar["Рынок<br/><code>eurmar</code>"]
    eurmil["Мельница<br/><code>eurmil</code>"]
    eurpor["Порт<br/><code>eurpor</code>"]
    eursga["Кам. ворота<br/><code>eursga</code>"]
    eursto["Склад<br/><code>eursto</code>"]
    eurswa["Стена<br/><code>eurswa</code>"]
    eurtow["Башня<br/><code>eurtow</code>"]
    ukrwga["Дер. ворота<br/><code>ukrwga</code>"]
    ukrwwa["Палисад<br/><code>ukrwwa</code>"]
    ausbar --> ausaca
    ausaca --> ausart
    auscen_1{"auscen.1<br/>(апгрейд)"}
    auscen_1 --> ausba2
    auscen -.-> auscen_1
    ausbla --> ausbar
    auscen --> ausbla
    ausaca --> ausdip
    auscen --> aushou
    ausbla --> aussta
    auscen --> austem
    eurmil --> eurmar
    eursto --> eurmar
    eurmar --> eurpor
    auscen --> eursto
    eursto --> eurswa
    eursto --> eurtow
    eursto --> ukrwwa
```

## Содержание

| Нация | Здания | Юниты | Ключевые апгрейды |
|---|---|---|---|
| **[ALG — Algeria (Алжир)](#alg--algeria-алжир)** | [здания](#alg--здания) | [юниты](#alg--юниты) | [апгрейды](#alg--ключевые-апгрейды-с-зависимостями) |
| **[AUS — Austria (Австрия)](#aus--austria-австрия)** | [здания](#aus--здания) | [юниты](#aus--юниты) | [апгрейды](#aus--ключевые-апгрейды-с-зависимостями) |
| **[BAV — Bavaria (Бавария)](#bav--bavaria-бавария)** | [здания](#bav--здания) | [юниты](#bav--юниты) | [апгрейды](#bav--ключевые-апгрейды-с-зависимостями) |
| **[DEN — Denmark (Дания)](#den--denmark-дания)** | [здания](#den--здания) | [юниты](#den--юниты) | [апгрейды](#den--ключевые-апгрейды-с-зависимостями) |
| **[ENG — England (Англия)](#eng--england-англия)** | [здания](#eng--здания) | [юниты](#eng--юниты) | [апгрейды](#eng--ключевые-апгрейды-с-зависимостями) |
| **[FRA — France (Франция)](#fra--france-франция)** | [здания](#fra--здания) | [юниты](#fra--юниты) | [апгрейды](#fra--ключевые-апгрейды-с-зависимостями) |
| **[HUN — Hungary (Венгрия)](#hun--hungary-венгрия)** | [здания](#hun--здания) | [юниты](#hun--юниты) | [апгрейды](#hun--ключевые-апгрейды-с-зависимостями) |
| **[NET — Netherlands (Нидерланды)](#net--netherlands-нидерланды)** | [здания](#net--здания) | [юниты](#net--юниты) | [апгрейды](#net--ключевые-апгрейды-с-зависимостями) |
| **[PIE — Piedmont (Пьемонт)](#pie--piedmont-пьемонт)** | [здания](#pie--здания) | [юниты](#pie--юниты) | [апгрейды](#pie--ключевые-апгрейды-с-зависимостями) |
| **[POL — Poland (Польша)](#pol--poland-польша)** | [здания](#pol--здания) | [юниты](#pol--юниты) | [апгрейды](#pol--ключевые-апгрейды-с-зависимостями) |
| **[POR — Portugal (Португалия)](#por--portugal-португалия)** | [здания](#por--здания) | [юниты](#por--юниты) | [апгрейды](#por--ключевые-апгрейды-с-зависимостями) |
| **[PRU — Prussia (Пруссия)](#pru--prussia-пруссия)** | [здания](#pru--здания) | [юниты](#pru--юниты) | [апгрейды](#pru--ключевые-апгрейды-с-зависимостями) |
| **[RUS — Russia (Россия)](#rus--russia-россия)** | [здания](#rus--здания) | [юниты](#rus--юниты) | [апгрейды](#rus--ключевые-апгрейды-с-зависимостями) |
| **[SAX — Saxony (Саксония)](#sax--saxony-саксония)** | [здания](#sax--здания) | [юниты](#sax--юниты) | [апгрейды](#sax--ключевые-апгрейды-с-зависимостями) |
| **[SCO — Scotland (Шотландия)](#sco--scotland-шотландия)** | [здания](#sco--здания) | [юниты](#sco--юниты) | [апгрейды](#sco--ключевые-апгрейды-с-зависимостями) |
| **[SPA — Spain (Испания)](#spa--spain-испания)** | [здания](#spa--здания) | [юниты](#spa--юниты) | [апгрейды](#spa--ключевые-апгрейды-с-зависимостями) |
| **[SWE — Sweden (Швеция)](#swe--sweden-швеция)** | [здания](#swe--здания) | [юниты](#swe--юниты) | [апгрейды](#swe--ключевые-апгрейды-с-зависимостями) |
| **[SWI — Switzerland (Швейцария)](#swi--switzerland-швейцария)** | [здания](#swi--здания) | [юниты](#swi--юниты) | [апгрейды](#swi--ключевые-апгрейды-с-зависимостями) |
| **[TUR — Turkey (Турция)](#tur--turkey-турция)** | [здания](#tur--здания) | [юниты](#tur--юниты) | [апгрейды](#tur--ключевые-апгрейды-с-зависимостями) |
| **[UKR — Ukraine (Украина)](#ukr--ukraine-украина)** | [здания](#ukr--здания) | [юниты](#ukr--юниты) | [апгрейды](#ukr--ключевые-апгрейды-с-зависимостями) |
| **[VEN — Venice (Венеция)](#ven--venice-венеция)** | [здания](#ven--здания) | [юниты](#ven--юниты) | [апгрейды](#ven--ключевые-апгрейды-с-зависимостями) |

## ALG — Algeria (Алжир)

### `alg` — здания

| sid | имя | Время (g-сек) | цена | ферма | требует |
|---|---|---:|---|---:|---|
| `algaca` | Минарет | 156.2 | W1450 S1100 | — | [B] `algbar` |
| `algart` | Артиллерийское депо | 245.9 | W100 S1000 C1400 | — | [B] `algaca` |
| `algbar` | Казарма | 93.8 | W400 S400 | 50 | [B] `algbla` |
| `algbla` | Кузница | 109.4 | W100 S30 I640 | — | [B] `algcen` |
| `algcen` | Городской центр | 156.2 | W450 S700 | 50 | — |
| `algdip` | Дипломатический центр | 312.5 | W4600 S2020 | — | [B] `algaca` |
| `alghou` | Дом | 31.2 | W100 S100 | 25 | [B] `algcen` |
| `algsta` | Конюшня | 156.2 | W1000 S2200 | — | [B] `algbla` |
| `algtem` | Мечеть | 93.8 | W1000 S1200 I500 | — | [B] `algcen` |
| `eurcoa` | Шахта | 93.8 | W100 S100 | — | — |
| `eurgol` | Шахта | 93.8 | W100 S100 | — | — |
| `euriro` | Шахта | 93.8 | W100 S100 | — | — |
| `turmar` | Базар | 234.4 | W450 S150 | — | [B] `turmil`, [B] `tursto` |
| `turmil` | Мельница | 93.8 | W30 S150 | — | — |
| `turpor` | Порт | 1562.5 | W800 S800 I400 | — | [B] `turmar` |
| `tursga` | Каменные ворота | 120.0 | S60 | — | — |
| `tursto` | Склад | 31.2 | W30 S10 | — | [B] `algcen` |
| `turswa` | Стена | 120.0 | S60 | — | [B] `tursto` |
| `turtow` | Башня | 984.4 | W150 S90 G100 | — | [B] `tursto` |
| `ukrwga` | Деревянные ворота | 5.6 | W10 | — | — |
| `ukrwwa` | Частокол | 5.6 | W10 | — | [B] `tursto` |

### `alg` — юниты

| sid | имя | Время (g-сек) | цена | тренируется в | требует |
|---|---|---:|---|---|---|
| `archer` | Лучник | 1.50 | F20 W2 G1 | algbar | — |
| `archerdip` | Лучник (наемник) | 1.25 | G15 | algdip | [B] `algaca`, [B] `algcen` |
| `archerturdip` | Турецкий лучник (наемник) | 1.25 | G15 | algdip | [B] `algaca`, [B] `algcen` |
| `battleship` | Линейный корабль | 390.00 | W9000 G3200 I700 C6500 | turpor | [T] `algaca.29`, [B] `algart` |
| `cannon` | Пушка | 75.00 | W250 G400 I400 | algart | [B] `algbla` |
| `cossacksichdip` | Сечевой козак (наемник) | 2.50 | G60 | algdip | [B] `algaca`, [B] `algcen` |
| `dragoon18dip` | Драгун 18в. (наемник) | 2.00 | G120 | algdip | [B] `algaca`, [B] `algcen` |
| `drummertur` | Барабанщик | 4.00 | F30 G15 | algbar | [B] `algaca` |
| `ferry` | Транспорт | 56.00 | W300 G50 I100 | turpor | [B] `algart` |
| `fishboat` | Рыбацкая лодка | 40.00 | W600 | turpor | — |
| `galley` | Галера | 50.00 | W9500 G900 I800 | turpor | [B] `algart` |
| `grenadierdip` | Гренадер (наемник) | 1.50 | G25 | algdip | [B] `algaca`, [B] `algcen` |
| `howitzer` | Гаубица | 94.00 | W250 G350 I300 | algart | [B] `algbla` |
| `lightcavalrydip` | Легкий кавалерист (наемник) | 2.00 | G120 | algdip | [B] `algaca`, [B] `algcen` |
| `lightinfantry` | Легкий пехотинец | 1.00 | F25 I1 | algbar | — |
| `lightinfantrydip` | Легкий пехотинец (наемник) | 1.25 | G4 | algdip | [B] `algaca`, [B] `algcen` |
| `mameluke` | Мамлюк | 12.00 | F100 W5 G8 | algsta | — |
| `mortar` | Мортира | 25.00 | W100 G75 I200 | algart | [B] `algbla` |
| `mullah` | Мулла | 15.00 | F30 G10 | algtem | — |
| `officertur` | Офицер | 7.50 | F50 G100 | algbar | [B] `algaca` |
| `peatur` | Крестьянин | 12.50 | F100 | algcen | — |
| `pikemantur` | Турецкий пикинер | 5.50 | F55 G5 | algbar | [B] `algbla` |
| `roundshierdip` | Рундашир (наемник) | 1.50 | G12 | algdip | [B] `algaca`, [B] `algcen` |
| `unitbox` | — | 3.12 | F100 | — | — |
| `xebec` | Шебека | 230.00 | W7000 G1600 I320 C960 | turpor | [T] `algaca.6`, [B] `algart` |

### `alg` — ключевые апгрейды (с зависимостями)

| sid | имя | Время (g-сек) | цена | требует |
|---|---|---:|---|---|
| `algaca.16` | Исследовать новые добавки в порох (дальность стрельбы артиллерии +5%) | 15.6 | G2000 | [B] `algart` |
| `algaca.17` | Разработать новые виды стволов: единорог, карронада (дальность стрельбы артиллерии +10%) | 15.6 | S3000 G4550 | [B] `algart` |
| `algaca.18` | Разработать более прочный лафет для орудий: система Грибоваля (прочность пушек +50%) | 15.6 | G500 I3830 C1500 | [B] `algart` |
| `algaca.20` | Разработать новые прицельные системы для пушек (меткость стрельбы артиллерии +35%) | 15.6 | W3540 G2000 C7250 | [B] `algart` |
| `algaca.21` | Выделить деньги на ремонтные мастерские для пушек (отремонтировать все пушки) | 15.6 | W350 G100 C250 | [B] `algart` |
| `algaca.27` | Развивать математику (меткость выстрела орудий +35%) | 15.6 | W9540 G12000 C65200 | [B] `algart` |
| `algaca.28` | Разработать новые парусные системы (скорость кораблей +40%) | 15.6 | G1900 | [B] `turpor` |
| `algaca.29` | Разработать новую систему шпангоутов и корпуса корабля (условие для постройки линейных кораблей) | 15.6 | W32300 G6800 I9000 C12800 | [B] `turpor` |
| `algaca.30` | Обучить плотников (скорость постройки кораблей увеличивается в 10 раз) | 15.6 | S42700 | [B] `turpor` |
| `algaca.5` | Разработать новые снасти и сети для ловли рыбы (эффективность рыбацких лодок +100%) | 15.6 | W12400 G2520 | [B] `turpor` |
| `algaca.6` | Разработать новые методы древообработки (условие для постройки шебек) | 15.6 | W9500 G7040 | [B] `turpor` |
| `algaca.7` | Построить новые верфи для рыбацких лодок (стоимость рыбацкой лодки -85%) | 15.6 | W7300 G1220 | [B] `turpor` |
| `algaca.8` | Разработать новые инструменты для древообработки (эффективность добычи дерева +100%) | 15.6 | F5500 G550 | [B] `algbla` |
| `algart.cannon.1.1` | — | 10.0 | W1000 S500 G300 | [B] `algbla` |
| `algart.cannon.1.2` | — | 10.0 | W3000 S1000 G500 | [B] `algbla` |
| `algart.cannon.1.3` | — | 10.0 | W6000 S2000 G1000 | [B] `algbla` |
| `algart.cannon.1.4` | — | 15.6 | F1760 G350 | [B] `algbla` |
| `algart.cannon.1.5` | — | 15.6 | F1760 G350 | [B] `algbla` |
| `algart.cannon.1.6` | — | 15.6 | F1760 G350 | [B] `algbla` |
| `algart.cannon.2.1` | — | 10.0 | G950 I1000 | [B] `algbla` |
| `algart.cannon.2.2` | — | 10.0 | G150 I2000 | [B] `algbla` |
| `algart.cannon.2.3` | — | 10.0 | G250 I3000 | [B] `algbla` |
| `algart.cannon.2.4` | — | 15.6 | F2560 G1350 | [B] `algbla` |
| `algart.cannon.2.5` | — | 15.6 | F3560 G2500 | [B] `algbla` |
| `algart.cannon.2.6` | — | 15.6 | F5560 G3350 | [B] `algbla` |
| `algart.howitzer.1.1` | — | 10.0 | W1000 S500 G300 | [B] `algbla` |
| `algart.howitzer.1.2` | — | 10.0 | W3000 S1000 G500 | [B] `algbla` |
| `algart.howitzer.1.3` | — | 10.0 | W6000 S2000 G1000 | [B] `algbla` |
| `algart.howitzer.1.4` | — | 15.6 | F1760 G350 | [B] `algbla` |
| `algart.howitzer.1.5` | — | 15.6 | F1760 G350 | [B] `algbla` |
| `algart.howitzer.1.6` | — | 15.6 | F1760 G350 | [B] `algbla` |
| `algart.howitzer.2.1` | — | 10.0 | G350 I1000 | [B] `algbla` |
| `algart.howitzer.2.2` | — | 10.0 | G450 I2000 | [B] `algbla` |
| `algart.howitzer.2.3` | — | 10.0 | G550 I3000 | [B] `algbla` |
| `algart.howitzer.2.4` | — | 31.2 | F2560 G1150 | [B] `algbla` |
| `algart.howitzer.2.5` | — | 31.2 | F3560 G3200 | [B] `algbla` |
| `algart.howitzer.2.6` | — | 31.2 | F5560 G4500 | [B] `algbla` |
| `algbar.lightinfantry.1.4` | — | 15.6 | F3000 G360 | [B] `algbla` |
| `algbar.lightinfantry.1.5` | — | 15.6 | F4500 G540 | [B] `algbla` |
| `algbar.lightinfantry.1.6` | — | 15.6 | F9375 G1125 | [B] `algbla` |
| `algbar.lightinfantry.2.4` | — | 15.6 | F3600 G600 | [B] `algbla` |
| `algbar.lightinfantry.2.5` | — | 15.6 | F5400 G900 | [B] `algbla` |
| `algbar.lightinfantry.2.6` | — | 15.6 | F11250 G1875 | [B] `algbla` |
| `algbar.pikemantur.1.6` | — | 15.6 | F18750 G2350 | [B] `algbla` |
| `algbar.pikemantur.2.6` | — | 15.6 | F16875 G2250 | [B] `algbla` |
| `turpor.1` | — | 46.9 | W20000 G1500 | [B] `algart` |
| `turtow.1` | — | 31.2 | G250 | [B] `algart` |
| `turtow.2` | — | 31.2 | I350 | [B] `algart` |
| `turtow.3` | — | 31.2 | C400 | [B] `algart` |
| `turtow.4` | — | 31.2 | I450 | [B] `algart` |
| `turtow.5` | — | 31.2 | C500 | [B] `algart` |

[↑ к содержанию](#содержание)

## AUS — Austria (Австрия)

### `aus` — здания

| sid | имя | Время (g-сек) | цена | ферма | требует |
|---|---|---:|---|---:|---|
| `ausaca` | Академия | 625.0 | W1250 S1100 | — | [B] `ausbar` |
| `ausart` | Артиллерийское депо | 245.9 | W100 S1000 C1400 | — | [B] `ausaca` |
| `ausba2` | Казарма 18в. | 5625.0 | W1700 S2950 G4000 | 250 | [T] `auscen.1` |
| `ausbar` | Казарма 17в. | 93.8 | W100 S100 G500 | 150 | [B] `ausbla` |
| `ausbla` | Кузница | 93.8 | W100 S30 I640 | — | [B] `auscen` |
| `auscen` | Городской центр | 46.9 | W700 S700 | 100 | — |
| `ausdip` | Дипломатический центр | 312.5 | W4900 S1700 | — | [B] `ausaca` |
| `aushou` | Дом | 31.2 | W100 S100 | 25 | [B] `auscen` |
| `aussta` | Конюшня | 625.0 | W2500 S100 G600 | — | [B] `ausbla` |
| `austem` | Собор | 156.2 | W1000 S1200 I500 | — | [B] `auscen` |
| `eurcoa` | Шахта | 93.8 | W100 S100 | — | — |
| `eurgol` | Шахта | 93.8 | W100 S100 | — | — |
| `euriro` | Шахта | 93.8 | W100 S100 | — | — |
| `eurmar` | Рынок | 234.4 | W450 | — | [B] `eurmil`, [B] `eursto` |
| `eurmil` | Мельница | 93.8 | W30 S150 | — | — |
| `eurpor` | Порт | 1562.5 | W1600 S800 I400 | — | [B] `eurmar` |
| `eursga` | Каменные ворота | 90.0 | S50 | — | — |
| `eursto` | Склад | 31.2 | W50 S20 | — | [B] `auscen` |
| `eurswa` | Стена | 90.0 | S50 | — | [B] `eursto` |
| `eurtow` | Башня | 1230.3 | W100 S100 G150 | — | [B] `eursto` |
| `ukrwga` | Деревянные ворота | 5.6 | W10 | — | — |
| `ukrwwa` | Частокол | 5.6 | W10 | — | [B] `eursto` |

### `aus` — юниты

| sid | имя | Время (g-сек) | цена | тренируется в | требует |
|---|---|---:|---|---|---|
| `archerdip` | Лучник (наемник) | 1.25 | G15 | ausdip | [B] `ausaca`, [B] `auscen` |
| `archerturdip` | Турецкий лучник (наемник) | 1.25 | G15 | ausdip | [B] `ausaca`, [B] `auscen` |
| `battleship` | Линейный корабль | 390.00 | W9000 G3200 I700 C6500 | eurpor | [T] `ausaca.29`, [B] `ausart` |
| `cannon` | Пушка | 75.00 | W250 G400 I400 | ausart | [B] `ausbla` |
| `cossacksichdip` | Сечевой козак (наемник) | 2.50 | G60 | ausdip | [B] `ausaca`, [B] `auscen` |
| `croat` | Кроат | 15.75 | F80 G6 I2 | aussta | [B] `ausbla` |
| `cuirassier` | Кирасир | 22.50 | F120 G35 I25 | aussta | [B] `ausbla`, [T] `auscen.1` |
| `dragoon` | Драгун 17в. | 15.00 | F90 G7 I5 | aussta | [B] `ausbla` |
| `dragoon18` | Драгун 18в. | 22.50 | F70 G60 I7 | aussta | [B] `ausbla`, [T] `auscen.1` |
| `dragoon18dip` | Драгун 18в. (наемник) | 2.00 | G120 | ausdip | [B] `ausaca`, [B] `auscen` |
| `drummer` | Барабанщик 17в. | 5.00 | F60 G20 | ausbar | [B] `ausaca` |
| `drummer18` | Барабанщик 18в. | 6.00 | F50 G30 | ausba2 | [B] `ausaca` |
| `ferry` | Транспорт | 56.00 | W300 G50 I100 | eurpor | [B] `ausart` |
| `fishboat` | Рыбацкая лодка | 40.00 | W600 | eurpor | — |
| `frigate` | Фрегат | 230.00 | W5000 G1100 I600 C800 | eurpor | [T] `ausaca.6`, [B] `ausart` |
| `galley` | Галера | 50.00 | W9500 G900 I800 | eurpor | [B] `ausart` |
| `grenadier` | Гренадер | 6.00 | F80 G60 I40 | ausba2 | [B] `ausbla` |
| `grenadierdip` | Гренадер (наемник) | 1.50 | G25 | ausdip | [B] `ausaca`, [B] `auscen` |
| `howitzer` | Гаубица | 94.00 | W250 G350 I300 | ausart | [B] `ausbla` |
| `hussar` | Гусар | 15.00 | F70 G20 I2 | aussta | [B] `ausbla`, [T] `auscen.1` |
| `lightcavalrydip` | Легкий кавалерист (наемник) | 2.00 | G120 | ausdip | [B] `ausaca`, [B] `auscen` |
| `lightinfantrydip` | Легкий пехотинец (наемник) | 1.25 | G4 | ausdip | [B] `ausaca`, [B] `auscen` |
| `mortar` | Мортира | 25.00 | W100 G75 I200 | ausart | [B] `ausbla` |
| `multicannon` | Многоствольное орудие | 50.00 | W200 G400 I250 | ausart | [T] `ausaca.19`, [B] `ausbla` |
| `musketeer18` | Мушкетер 18в. | 4.50 | F50 G40 I40 | ausba2 | [B] `ausbla` |
| `musketeeraus` | Мушкетер 17в. | 6.50 | F35 G9 I15 | ausbar | [B] `ausbla` |
| `officer` | Офицер 17в. | 10.00 | F50 G150 I30 | ausbar | [B] `ausaca` |
| `officer18` | Офицер 18в. | 6.00 | F50 G200 I10 | ausba2 | [B] `ausaca` |
| `pandur` | Пандур | 5.50 | F40 G15 I10 | ausba2 | [B] `ausbla` |
| `peaaus` | Крестьянин | 12.50 | F100 | auscen | — |
| `pikeman` | Пикинер 17в. | 4.50 | F25 G3 I20 | ausbar | [B] `ausbla` |
| `pikeman18` | Пикинер 18в. | 1.25 | F30 G2 | ausba2 | — |
| `priest` | Капеллан | 20.00 | F60 G25 | austem | — |
| `reiter` | Рейтар | 24.00 | F120 G10 I40 | aussta | [B] `ausbla` |
| `roundshier` | Рундашир | 4.00 | F20 G3 I25 | ausbar | [B] `ausbla` |
| `roundshierdip` | Рундашир (наемник) | 1.50 | G12 | ausdip | [B] `ausaca`, [B] `auscen` |
| `unitbox` | — | 3.12 | F100 | — | — |
| `yacht` | Яхта | 48.00 | W900 G450 I150 C200 | eurpor | [B] `ausart` |

### `aus` — ключевые апгрейды (с зависимостями)

| sid | имя | Время (g-сек) | цена | требует |
|---|---|---:|---|---|
| `ausaca.12` | Улучшить стрелковое оружие: нарезной ствол (сила выстрела +10%) | 15.6 | I5000 | [B] `ausbla` |
| `ausaca.13` | Исследовать гранулированный порох (сила выстрела +10%) | 15.6 | G4000 | [B] `ausbla` |
| `ausaca.14` | Исследовать новые методы очистки серы (сила выстрела +15%) | 15.6 | G7000 | [B] `ausbla` |
| `ausaca.15` | Исследовать новые методы очистки селитры (сила выстрела +25%) | 15.6 | C11000 | [B] `ausbla` |
| `ausaca.16` | Исследовать новые добавки в порох (дальность стрельбы артиллерии +5%) | 15.6 | G2000 I12150 | [B] `ausart` |
| `ausaca.17` | Разработать новые виды стволов: единорог, карронада (дальность стрельбы артиллерии +10%) | 15.6 | S3000 G4550 I19200 | [B] `ausart` |
| `ausaca.18` | Разработать более прочный лафет для орудий: система Грибоваля (прочность пушек +50%) | 15.6 | G500 I3830 C1500 | [B] `ausart` |
| `ausaca.19` | Разработать многоствольное орудие | 15.6 | G1500 C2500 | [B] `ausart` |
| `ausaca.20` | Разработать новые прицельные системы для пушек (меткость стрельбы артиллерии +35%) | 15.6 | W3540 G2000 C7250 | [B] `ausart` |
| `ausaca.21` | Выделить деньги на ремонтные мастерские для пушек (отремонтировать все пушки) | 15.6 | W350 G100 C250 | [B] `ausart` |
| `ausaca.25` | Разработать монгольфьер (открывает всю карту) | 15.6 | G5750 | [T] `auscen.1` |
| `ausaca.27` | Развивать математику (меткость выстрела орудий +35%) | 15.6 | W9540 G12000 C65200 | [B] `ausart` |
| `ausaca.28` | Разработать новые парусные системы (скорость кораблей +40%) | 15.6 | W65400 G24050 | [B] `eurpor` |
| `ausaca.29` | Разработать новую систему шпангоутов и корпуса корабля (условие для постройки линейных кораблей) | 15.6 | W32300 G6800 I9000 C12800 | [B] `eurpor` |
| `ausaca.30` | Обучить плотников (скорость постройки кораблей увеличивается в 10 раз) | 15.6 | W2300 S42700 G1150 | [B] `eurpor` |
| `ausaca.32` | Разработать кремниевый замок к ружьям (цена мушкета -50%) | 15.6 | G6050 C7750 | [T] `auscen.1` |
| `ausaca.34` | Разработать новые сорта стали для кирас (защита солдат в доспехах +2) | 15.6 | G9750 | [B] `ausbla` |
| `ausaca.35` | Разработать штык: вставляемый в ствол багинет, штык с трубкой (сила удара холодного оружия +5) | 15.6 | G11500 | [T] `auscen.1`, [B] `ausbla` |
| `ausaca.36` | Разработать новые сорта стали (эффективность рукопашной атаки мушкетера 18 века и гренадера +25%) | 15.6 | G19500 | [T] `auscen.1`, [B] `ausbla` |
| `ausaca.5` | Разработать новые снасти и сети для ловли рыбы (эффективность рыбацких лодок +100%) | 15.6 | W12400 G2520 | [B] `eurpor` |
| `ausaca.6` | Разработать новые методы древообработки (условие для постройки фрегатов) | 15.6 | W12400 G7040 | [B] `eurpor` |
| `ausaca.7` | Построить новые верфи для рыбацких лодок (стоимость рыбацкой лодки -85%) | 15.6 | W7300 G1220 | [B] `eurpor` |
| `ausaca.8` | Разработать новые инструменты для древообработки (эффективность добычи дерева +100%) | 15.6 | F5500 G550 | [B] `ausbla` |
| `ausart.cannon.1.1` | — | 10.0 | W1000 S500 G300 | [B] `ausbla` |
| `ausart.cannon.1.2` | — | 10.0 | W3000 S1000 G500 | [B] `ausbla` |
| `ausart.cannon.1.3` | — | 10.0 | W6000 S2000 G1000 | [B] `ausbla` |
| `ausart.cannon.1.4` | — | 15.6 | F1760 G350 | [B] `ausbla` |
| `ausart.cannon.1.5` | — | 15.6 | F1760 G350 | [B] `ausbla` |
| `ausart.cannon.1.6` | — | 15.6 | F1760 G350 | [B] `ausbla` |
| `ausart.cannon.2.1` | — | 10.0 | G500 I1000 | [B] `ausbla` |
| `ausart.cannon.2.2` | — | 10.0 | G1000 I2000 | [B] `ausbla` |
| `ausart.cannon.2.3` | — | 10.0 | G2000 I3000 | [B] `ausbla` |
| `ausart.cannon.2.4` | — | 15.6 | F2560 | [B] `ausbla` |
| `ausart.cannon.2.5` | — | 15.6 | F3560 | [B] `ausbla` |
| `ausart.cannon.2.6` | — | 15.6 | F5560 | [B] `ausbla` |
| `ausart.howitzer.1.1` | — | 10.0 | W1000 S500 G300 | [B] `ausbla` |
| `ausart.howitzer.1.2` | — | 10.0 | W3000 S1000 G500 | [B] `ausbla` |
| `ausart.howitzer.1.3` | — | 10.0 | W6000 S2000 G1000 | [B] `ausbla` |
| `ausart.howitzer.1.4` | — | 15.6 | F1760 G350 | [B] `ausbla` |
| `ausart.howitzer.1.5` | — | 15.6 | F1760 G350 | [B] `ausbla` |
| `ausart.howitzer.1.6` | — | 15.6 | F1760 G350 | [B] `ausbla` |
| `ausart.howitzer.2.1` | — | 10.0 | G500 I1000 | [B] `ausbla` |
| `ausart.howitzer.2.2` | — | 10.0 | G1000 I2000 | [B] `ausbla` |
| `ausart.howitzer.2.3` | — | 10.0 | G2000 I3000 | [B] `ausbla` |
| `ausart.howitzer.2.4` | — | 31.2 | F2560 | [B] `ausbla` |
| `ausart.howitzer.2.5` | — | 31.2 | F3560 | [B] `ausbla` |
| `ausart.howitzer.2.6` | — | 31.2 | F5560 | [B] `ausbla` |
| `ausbar.pikeman.1.6` | — | 15.6 | F15000 G1875 | [B] `ausbla` |
| `ausbar.pikeman.2.6` | — | 15.6 | F11250 G1500 | [B] `ausbla` |
| `ausbar.roundshier.1.4` | — | 15.6 | F7500 G900 | [B] `ausbla` |
| `ausbar.roundshier.1.5` | — | 15.6 | F9000 G1080 | [B] `ausbla` |
| `ausbar.roundshier.1.6` | — | 15.6 | F18750 G2250 | [B] `ausbla` |
| `ausbar.roundshier.2.4` | — | 15.6 | F3750 G450 | [B] `ausbla` |
| `ausbar.roundshier.2.5` | — | 15.6 | F6750 G810 | [B] `ausbla` |
| `ausbar.roundshier.2.6` | — | 15.6 | F9375 G1125 | [B] `ausbla` |
| `ausbla.4` | Выковать штыки и тесаки для пехоты (сила удара мушкетера 18 века и гренадера +5) | 15.6 | W1300 G1500 I900 C5000 | [T] `auscen.1` |
| `auscen.1` | — | 9.4 | F30000 G5000 I2000 C2000 | [B] `ausaca`, [B] `austem`, [B] `ausart` |
| `eurcoa.4` | — | 9.4 | F15800 G18500 | [T] `auscen.1` |
| `eurcoa.5` | — | 9.4 | F19800 G21050 | [T] `auscen.1` |
| `eurcoa.6` | — | 9.4 | F50200 G25950 | [T] `auscen.1` |
| `eurgol.4` | — | 9.4 | F15800 G18500 | [T] `auscen.1` |
| `eurgol.5` | — | 9.4 | F19800 G21050 | [T] `auscen.1` |
| `eurgol.6` | — | 9.4 | F50200 G25950 | [T] `auscen.1` |
| `euriro.4` | — | 9.4 | F15800 G18500 | [T] `auscen.1` |
| `euriro.5` | — | 9.4 | F19800 G21050 | [T] `auscen.1` |
| `euriro.6` | — | 9.4 | F50200 G25950 | [T] `auscen.1` |
| `eurpor.1` | — | 46.9 | W20000 G1500 | [B] `ausart` |
| `eurtow.1` | — | 31.2 | G250 | [B] `ausart` |
| `eurtow.2` | — | 31.2 | I350 | [B] `ausart` |
| `eurtow.3` | — | 31.2 | C400 | [B] `ausart` |
| `eurtow.4` | — | 31.2 | I450 | [B] `ausart` |
| `eurtow.5` | — | 31.2 | C500 | [B] `ausart` |
| `ferry.1` | Усовершенствовать конструкцию транспортного судна (+%value% посадочных мест) | 15.6 | F1000 G1250 | [T] `auscen.1` |

[↑ к содержанию](#содержание)

## BAV — Bavaria (Бавария)

### `bav` — здания

| sid | имя | Время (g-сек) | цена | ферма | требует |
|---|---|---:|---|---:|---|
| `bavaca` | Академия | 625.0 | W1250 S1100 | — | [B] `bavbar` |
| `bavart` | Артиллерийское депо | 245.9 | W100 S1000 C1400 | — | [B] `bavaca` |
| `bavba2` | Казарма 18в. | 5625.0 | W1700 S2950 G4000 | 250 | [T] `bavcen.1` |
| `bavbar` | Казарма 17в. | 93.8 | W100 S100 G500 | 150 | [B] `bavbla` |
| `bavbla` | Кузница | 93.8 | W100 S30 I640 | — | [B] `bavcen` |
| `bavcen` | Городской центр | 156.2 | W700 S700 | 100 | — |
| `bavdip` | Дипломатический центр | 312.5 | W4900 S1700 | — | [B] `bavaca` |
| `bavhou` | Дом | 31.2 | W100 S100 | 25 | [B] `bavcen` |
| `bavsta` | Конюшня | 625.0 | W2500 S100 G600 | — | [B] `bavbla` |
| `bavtem` | Собор | 156.2 | W1000 S1200 I500 | — | [B] `bavcen` |
| `eurcoa` | Шахта | 93.8 | W100 S100 | — | — |
| `eurgol` | Шахта | 93.8 | W100 S100 | — | — |
| `euriro` | Шахта | 93.8 | W100 S100 | — | — |
| `eurmar` | Рынок | 234.4 | W450 | — | [B] `eurmil`, [B] `eursto` |
| `eurmil` | Мельница | 93.8 | W30 S150 | — | — |
| `eurpor` | Порт | 1562.5 | W1600 S800 I400 | — | [B] `eurmar` |
| `eursga` | Каменные ворота | 90.0 | S50 | — | — |
| `eursto` | Склад | 31.2 | W50 S20 | — | [B] `bavcen` |
| `eurswa` | Стена | 90.0 | S50 | — | [B] `eursto` |
| `eurtow` | Башня | 1230.3 | W100 S100 G150 | — | [B] `eursto` |
| `ukrwga` | Деревянные ворота | 5.6 | W10 | — | — |
| `ukrwwa` | Частокол | 5.6 | W10 | — | [B] `eursto` |

### `bav` — юниты

| sid | имя | Время (g-сек) | цена | тренируется в | требует |
|---|---|---:|---|---|---|
| `archerdip` | Лучник (наемник) | 1.25 | G15 | bavdip | [B] `bavaca`, [B] `bavcen` |
| `archerturdip` | Турецкий лучник (наемник) | 1.25 | G15 | bavdip | [B] `bavaca`, [B] `bavcen` |
| `battleship` | Линейный корабль | 390.00 | W9000 G3200 I700 C6500 | eurpor | [T] `bavaca.29`, [B] `bavart` |
| `cannon` | Пушка | 75.00 | W250 G400 I400 | bavart | [B] `bavbla` |
| `cossacksichdip` | Сечевой козак (наемник) | 2.50 | G60 | bavdip | [B] `bavaca`, [B] `bavcen` |
| `cuirassier` | Кирасир | 22.50 | F120 G35 I25 | bavsta | [B] `bavbla`, [T] `bavcen.1` |
| `dragoon` | Драгун 17в. | 15.00 | F90 G7 I5 | bavsta | [B] `bavbla` |
| `dragoon18` | Драгун 18в. | 22.50 | F70 G60 I7 | bavsta | [B] `bavbla`, [T] `bavcen.1` |
| `dragoon18dip` | Драгун 18в. (наемник) | 2.00 | G120 | bavdip | [B] `bavaca`, [B] `bavcen` |
| `drummer` | Барабанщик 17в. | 5.00 | F60 G20 | bavbar | [B] `bavaca` |
| `drummer18` | Барабанщик 18в. | 6.00 | F50 G30 | bavba2 | [B] `bavaca` |
| `ferry` | Транспорт | 56.00 | W300 G50 I100 | eurpor | [B] `bavart` |
| `fishboat` | Рыбацкая лодка | 40.00 | W600 | eurpor | — |
| `frigate` | Фрегат | 230.00 | W5000 G1100 I600 C800 | eurpor | [T] `bavaca.6`, [B] `bavart` |
| `galley` | Галера | 50.00 | W9500 G900 I800 | eurpor | [B] `bavart` |
| `grenadierbav` | Гренадер | 6.00 | F95 G70 I40 | bavba2 | [B] `bavbla` |
| `grenadierdip` | Гренадер (наемник) | 1.50 | G25 | bavdip | [B] `bavaca`, [B] `bavcen` |
| `howitzer` | Гаубица | 94.00 | W250 G350 I300 | bavart | [B] `bavbla` |
| `hussar` | Гусар | 15.00 | F70 G20 I2 | bavsta | [B] `bavbla`, [T] `bavcen.1` |
| `lightcavalrydip` | Легкий кавалерист (наемник) | 2.00 | G120 | bavdip | [B] `bavaca`, [B] `bavcen` |
| `lightinfantrydip` | Легкий пехотинец (наемник) | 1.25 | G4 | bavdip | [B] `bavaca`, [B] `bavcen` |
| `mortar` | Мортира | 25.00 | W100 G75 I200 | bavart | [B] `bavbla` |
| `multicannon` | Многоствольное орудие | 50.00 | W200 G400 I250 | bavart | [T] `bavaca.19`, [B] `bavbla` |
| `musketeer` | Мушкетер 17в. | 6.00 | F45 G6 I5 | bavbar | [B] `bavbla` |
| `musketeer18bav` | Мушкетер 18в. | 5.00 | F60 G55 I35 | bavba2 | [B] `bavbla` |
| `officer` | Офицер 17в. | 10.00 | F50 G150 I30 | bavbar | [B] `bavaca` |
| `officer18` | Офицер 18в. | 6.00 | F50 G200 I10 | bavba2 | [B] `bavaca` |
| `peaaus` | Крестьянин | 12.50 | F100 | bavcen | — |
| `pikeman` | Пикинер 17в. | 4.50 | F25 G3 I20 | bavbar | [B] `bavbla` |
| `pikeman18` | Пикинер 18в. | 1.25 | F30 G2 | bavba2 | — |
| `priest` | Капеллан | 20.00 | F60 G25 | bavtem | — |
| `reiter` | Рейтар | 24.00 | F120 G10 I40 | bavsta | [B] `bavbla` |
| `roundshierdip` | Рундашир (наемник) | 1.50 | G12 | bavdip | [B] `bavaca`, [B] `bavcen` |
| `unitbox` | — | 3.12 | F100 | — | — |
| `yacht` | Яхта | 48.00 | W900 G450 I150 C200 | eurpor | [B] `bavart` |

### `bav` — ключевые апгрейды (с зависимостями)

| sid | имя | Время (g-сек) | цена | требует |
|---|---|---:|---|---|
| `bavaca.12` | Улучшить стрелковое оружие: нарезной ствол (сила выстрела +10%) | 15.6 | I5000 | [B] `bavbla` |
| `bavaca.13` | Исследовать гранулированный порох (сила выстрела +10%) | 15.6 | G4000 | [B] `bavbla` |
| `bavaca.14` | Исследовать новые методы очистки серы (сила выстрела +15%) | 15.6 | G7000 | [B] `bavbla` |
| `bavaca.15` | Исследовать новые методы очистки селитры (сила выстрела +25%) | 15.6 | C11000 | [B] `bavbla` |
| `bavaca.16` | Исследовать новые добавки в порох (дальность стрельбы артиллерии +5%) | 15.6 | G2000 I12150 | [B] `bavart` |
| `bavaca.17` | Разработать новые виды стволов: единорог, карронада (дальность стрельбы артиллерии +10%) | 15.6 | S3000 G4550 I19200 | [B] `bavart` |
| `bavaca.18` | Разработать более прочный лафет для орудий: система Грибоваля (прочность пушек +50%) | 15.6 | G500 I3830 C1500 | [B] `bavart` |
| `bavaca.19` | Разработать многоствольное орудие | 15.6 | G1500 C2500 | [B] `bavart` |
| `bavaca.20` | Разработать новые прицельные системы для пушек (меткость стрельбы артиллерии +35%) | 15.6 | W3540 G2000 C7250 | [B] `bavart` |
| `bavaca.21` | Выделить деньги на ремонтные мастерские для пушек (отремонтировать все пушки) | 15.6 | W350 G100 C250 | [B] `bavart` |
| `bavaca.25` | Разработать монгольфьер (открывает всю карту) | 15.6 | G5750 | [T] `bavcen.1` |
| `bavaca.27` | Развивать математику (меткость выстрела орудий +35%) | 15.6 | W9540 G12000 C65200 | [B] `bavart` |
| `bavaca.28` | Разработать новые парусные системы (скорость кораблей +40%) | 15.6 | W65400 G24050 | [B] `eurpor` |
| `bavaca.29` | Разработать новую систему шпангоутов и корпуса корабля (условие для постройки линейных кораблей) | 15.6 | W32300 G6800 I9000 C12800 | [B] `eurpor` |
| `bavaca.30` | Обучить плотников (скорость постройки кораблей увеличивается в 10 раз) | 15.6 | W2300 S42700 G1150 | [B] `eurpor` |
| `bavaca.32` | Разработать кремниевый замок к ружьям (цена мушкета -50%) | 15.6 | G6050 C7750 | [T] `bavcen.1` |
| `bavaca.34` | Разработать новые сорта стали для кирас (защита солдат в доспехах +2) | 15.6 | G9750 | [B] `bavbla` |
| `bavaca.35` | Разработать штык: вставляемый в ствол багинет, штык с трубкой (сила удара холодного оружия +5) | 15.6 | G11500 | [T] `bavcen.1`, [B] `bavbla` |
| `bavaca.36` | Разработать новые сорта стали (эффективность рукопашной атаки мушкетера 18 века и гренадера +25%) | 15.6 | G19500 | [T] `bavcen.1`, [B] `bavbla` |
| `bavaca.5` | Разработать новые снасти и сети для ловли рыбы (эффективность рыбацких лодок +100%) | 15.6 | W12400 G2520 | [B] `eurpor` |
| `bavaca.6` | Разработать новые методы древообработки (условие для постройки фрегатов) | 15.6 | W12400 G7040 | [B] `eurpor` |
| `bavaca.7` | Построить новые верфи для рыбацких лодок (стоимость рыбацкой лодки -85%) | 15.6 | W7300 G1220 | [B] `eurpor` |
| `bavaca.8` | Разработать новые инструменты для древообработки (эффективность добычи дерева +100%) | 15.6 | F5500 G550 | [B] `bavbla` |
| `bavart.cannon.1.1` | — | 10.0 | W1000 S500 G300 | [B] `bavbla` |
| `bavart.cannon.1.2` | — | 10.0 | W3000 S1000 G500 | [B] `bavbla` |
| `bavart.cannon.1.3` | — | 10.0 | W6000 S2000 G1000 | [B] `bavbla` |
| `bavart.cannon.1.4` | — | 15.6 | F1760 G350 | [B] `bavbla` |
| `bavart.cannon.1.5` | — | 15.6 | F1760 G350 | [B] `bavbla` |
| `bavart.cannon.1.6` | — | 15.6 | F1760 G350 | [B] `bavbla` |
| `bavart.cannon.2.1` | — | 10.0 | G500 I1000 | [B] `bavbla` |
| `bavart.cannon.2.2` | — | 10.0 | G1000 I2000 | [B] `bavbla` |
| `bavart.cannon.2.3` | — | 10.0 | G2000 I3000 | [B] `bavbla` |
| `bavart.cannon.2.4` | — | 15.6 | F2560 | [B] `bavbla` |
| `bavart.cannon.2.5` | — | 15.6 | F3560 | [B] `bavbla` |
| `bavart.cannon.2.6` | — | 15.6 | F5560 | [B] `bavbla` |
| `bavart.howitzer.1.1` | — | 10.0 | W1000 S500 G300 | [B] `bavbla` |
| `bavart.howitzer.1.2` | — | 10.0 | W3000 S1000 G500 | [B] `bavbla` |
| `bavart.howitzer.1.3` | — | 10.0 | W6000 S2000 G1000 | [B] `bavbla` |
| `bavart.howitzer.1.4` | — | 15.6 | F1760 G350 | [B] `bavbla` |
| `bavart.howitzer.1.5` | — | 15.6 | F1760 G350 | [B] `bavbla` |
| `bavart.howitzer.1.6` | — | 15.6 | F1760 G350 | [B] `bavbla` |
| `bavart.howitzer.2.1` | — | 10.0 | G500 I1000 | [B] `bavbla` |
| `bavart.howitzer.2.2` | — | 10.0 | G1000 I2000 | [B] `bavbla` |
| `bavart.howitzer.2.3` | — | 10.0 | G2000 I3000 | [B] `bavbla` |
| `bavart.howitzer.2.4` | — | 31.2 | F2560 | [B] `bavbla` |
| `bavart.howitzer.2.5` | — | 31.2 | F3560 | [B] `bavbla` |
| `bavart.howitzer.2.6` | — | 31.2 | F5560 | [B] `bavbla` |
| `bavbar.pikeman.1.6` | — | 15.6 | F15000 G1875 | [B] `bavbla` |
| `bavbar.pikeman.2.6` | — | 15.6 | F11250 G1500 | [B] `bavbla` |
| `bavbla.4` | Выковать штыки и тесаки для пехоты (сила удара мушкетера 18 века и гренадера +5) | 15.6 | W1300 G1500 I900 C5000 | [T] `bavcen.1` |
| `bavcen.1` | — | 9.4 | F30000 G5000 I2000 C2000 | [B] `bavaca`, [B] `bavtem`, [B] `bavart` |
| `eurcoa.4` | — | 9.4 | F15800 G18500 | [T] `bavcen.1` |
| `eurcoa.5` | — | 9.4 | F19800 G21050 | [T] `bavcen.1` |
| `eurcoa.6` | — | 9.4 | F50200 G25950 | [T] `bavcen.1` |
| `eurgol.4` | — | 9.4 | F15800 G18500 | [T] `bavcen.1` |
| `eurgol.5` | — | 9.4 | F19800 G21050 | [T] `bavcen.1` |
| `eurgol.6` | — | 9.4 | F50200 G25950 | [T] `bavcen.1` |
| `euriro.4` | — | 9.4 | F15800 G18500 | [T] `bavcen.1` |
| `euriro.5` | — | 9.4 | F19800 G21050 | [T] `bavcen.1` |
| `euriro.6` | — | 9.4 | F50200 G25950 | [T] `bavcen.1` |
| `eurpor.1` | — | 46.9 | W20000 G1500 | [B] `bavart` |
| `eurtow.1` | — | 31.2 | G250 | [B] `bavart` |
| `eurtow.2` | — | 31.2 | I350 | [B] `bavart` |
| `eurtow.3` | — | 31.2 | C400 | [B] `bavart` |
| `eurtow.4` | — | 31.2 | I450 | [B] `bavart` |
| `eurtow.5` | — | 31.2 | C500 | [B] `bavart` |
| `ferry.1` | Усовершенствовать конструкцию транспортного судна (+%value% посадочных мест) | 15.6 | F1000 G1250 | [T] `bavcen.1` |

[↑ к содержанию](#содержание)

## DEN — Denmark (Дания)

### `den` — здания

| sid | имя | Время (g-сек) | цена | ферма | требует |
|---|---|---:|---|---:|---|
| `denaca` | Академия | 625.0 | W1450 S900 | — | [B] `denbar` |
| `denart` | Артиллерийское депо | 245.9 | W100 S1000 C1400 | — | [B] `denaca` |
| `denba2` | Казарма 18в. | 5625.0 | W1700 S2950 G4000 | 250 | [T] `dencen.1` |
| `denbar` | Казарма 17в. | 93.8 | W100 S100 G500 | 150 | [B] `denbla` |
| `denbla` | Кузница | 93.8 | W100 S30 I640 | — | [B] `dencen` |
| `dencen` | Городской центр | 156.2 | W700 S700 | 100 | — |
| `dendip` | Дипломатический центр | 312.5 | W4900 S1700 | — | [B] `denaca` |
| `denhou` | Дом | 31.2 | W100 S100 | 25 | [B] `dencen` |
| `densta` | Конюшня | 625.0 | W2500 S100 G600 | — | [B] `denbla` |
| `dentem` | Собор | 156.2 | W1000 S1200 I500 | — | [B] `dencen` |
| `eurcoa` | Шахта | 93.8 | W100 S100 | — | — |
| `eurgol` | Шахта | 93.8 | W100 S100 | — | — |
| `euriro` | Шахта | 93.8 | W100 S100 | — | — |
| `eurmar` | Рынок | 234.4 | W450 | — | [B] `eurmil`, [B] `eursto` |
| `eurmil` | Мельница | 93.8 | W30 S150 | — | — |
| `eurpor` | Порт | 1562.5 | W1600 S800 I400 | — | [B] `eurmar` |
| `eursga` | Каменные ворота | 90.0 | S50 | — | — |
| `eursto` | Склад | 31.2 | W50 S20 | — | [B] `dencen` |
| `eurswa` | Стена | 90.0 | S50 | — | [B] `eursto` |
| `eurtow` | Башня | 1230.3 | W100 S100 G150 | — | [B] `eursto` |
| `ukrwga` | Деревянные ворота | 5.6 | W10 | — | — |
| `ukrwwa` | Частокол | 5.6 | W10 | — | [B] `eursto` |

### `den` — юниты

| sid | имя | Время (g-сек) | цена | тренируется в | требует |
|---|---|---:|---|---|---|
| `archerdip` | Лучник (наемник) | 1.25 | G15 | dendip | [B] `denaca`, [B] `dencen` |
| `archerturdip` | Турецкий лучник (наемник) | 1.25 | G15 | dendip | [B] `denaca`, [B] `dencen` |
| `battleship` | Линейный корабль | 390.00 | W9000 G3200 I700 C6500 | eurpor | [T] `denaca.29`, [B] `denart` |
| `cannon` | Пушка | 75.00 | W250 G400 I400 | denart | [B] `denbla` |
| `cossacksichdip` | Сечевой козак (наемник) | 2.50 | G60 | dendip | [B] `denaca`, [B] `dencen` |
| `cuirassier` | Кирасир | 22.50 | F120 G35 I25 | densta | [B] `denbla`, [T] `dencen.1` |
| `dragoon` | Драгун 17в. | 15.00 | F90 G7 I5 | densta | [B] `denbla` |
| `dragoon18` | Драгун 18в. | 22.50 | F70 G60 I7 | densta | [B] `denbla`, [T] `dencen.1` |
| `dragoon18dip` | Драгун 18в. (наемник) | 2.00 | G120 | dendip | [B] `denaca`, [B] `dencen` |
| `drummer` | Барабанщик 17в. | 5.00 | F60 G20 | denbar | [B] `denaca` |
| `drummer18` | Барабанщик 18в. | 6.00 | F50 G30 | denba2 | [B] `denaca` |
| `ferry` | Транспорт | 56.00 | W300 G50 I100 | eurpor | [B] `denart` |
| `fishboat` | Рыбацкая лодка | 40.00 | W600 | eurpor | — |
| `frigate` | Фрегат | 230.00 | W5000 G1100 I600 C800 | eurpor | [T] `denaca.6`, [B] `denart` |
| `galley` | Галера | 50.00 | W9500 G900 I800 | eurpor | [B] `denart` |
| `grenadierden` | Гренадер | 6.50 | F100 G90 I40 | denba2 | [B] `denbla` |
| `grenadierdip` | Гренадер (наемник) | 1.50 | G25 | dendip | [B] `denaca`, [B] `dencen` |
| `howitzer` | Гаубица | 94.00 | W250 G350 I300 | denart | [B] `denbla` |
| `hussar` | Гусар | 15.00 | F70 G20 I2 | densta | [B] `denbla`, [T] `dencen.1` |
| `lightcavalrydip` | Легкий кавалерист (наемник) | 2.00 | G120 | dendip | [B] `denaca`, [B] `dencen` |
| `lightinfantrydip` | Легкий пехотинец (наемник) | 1.25 | G4 | dendip | [B] `denaca`, [B] `dencen` |
| `mortar` | Мортира | 25.00 | W100 G75 I200 | denart | [B] `denbla` |
| `multicannon` | Многоствольное орудие | 50.00 | W200 G400 I250 | denart | [T] `denaca.19`, [B] `denbla` |
| `musketeer` | Мушкетер 17в. | 6.00 | F45 G6 I5 | denbar | [B] `denbla` |
| `musketeer18den` | Мушкетер 18в. | 5.50 | F50 G80 I40 | denba2 | [B] `denbla` |
| `officer` | Офицер 17в. | 10.00 | F50 G150 I30 | denbar | [B] `denaca` |
| `officer18` | Офицер 18в. | 6.00 | F50 G200 I10 | denba2 | [B] `denaca` |
| `peaeng` | Крестьянин | 12.50 | F100 | dencen | — |
| `pikeman` | Пикинер 17в. | 4.50 | F25 G3 I20 | denbar | [B] `denbla` |
| `pikeman18` | Пикинер 18в. | 1.25 | F30 G2 | denba2 | — |
| `priest` | Капеллан | 20.00 | F60 G25 | dentem | — |
| `reiter` | Рейтар | 24.00 | F120 G10 I40 | densta | [B] `denbla` |
| `roundshierdip` | Рундашир (наемник) | 1.50 | G12 | dendip | [B] `denaca`, [B] `dencen` |
| `unitbox` | — | 3.12 | F100 | — | — |
| `yacht` | Яхта | 48.00 | W900 G450 I150 C200 | eurpor | [B] `denart` |

### `den` — ключевые апгрейды (с зависимостями)

| sid | имя | Время (g-сек) | цена | требует |
|---|---|---:|---|---|
| `denaca.12` | Улучшить стрелковое оружие: нарезной ствол (сила выстрела +10%) | 15.6 | I5000 | [B] `denbla` |
| `denaca.13` | Исследовать гранулированный порох (сила выстрела +10%) | 15.6 | G4000 | [B] `denbla` |
| `denaca.14` | Исследовать новые методы очистки серы (сила выстрела +15%) | 15.6 | G7000 | [B] `denbla` |
| `denaca.15` | Исследовать новые методы очистки селитры (сила выстрела +25%) | 15.6 | C11000 | [B] `denbla` |
| `denaca.16` | Исследовать новые добавки в порох (дальность стрельбы артиллерии +5%) | 15.6 | G2000 I12150 | [B] `denart` |
| `denaca.17` | Разработать новые виды стволов: единорог, карронада (дальность стрельбы артиллерии +10%) | 15.6 | S3000 G4550 I19200 | [B] `denart` |
| `denaca.18` | Разработать более прочный лафет для орудий: система Грибоваля (прочность пушек +50%) | 15.6 | G500 I3830 C1500 | [B] `denart` |
| `denaca.19` | Разработать многоствольное орудие | 15.6 | G1500 C2500 | [B] `denart` |
| `denaca.20` | Разработать новые прицельные системы для пушек (меткость стрельбы артиллерии +35%) | 15.6 | W3540 G2000 C7250 | [B] `denart` |
| `denaca.21` | Выделить деньги на ремонтные мастерские для пушек (отремонтировать все пушки) | 15.6 | W350 G100 C250 | [B] `denart` |
| `denaca.25` | Разработать монгольфьер (открывает всю карту) | 15.6 | G5750 | [T] `dencen.1` |
| `denaca.27` | Развивать математику (меткость выстрела орудий +35%) | 15.6 | W9540 G12000 C65200 | [B] `denart` |
| `denaca.28` | Разработать новые парусные системы (скорость кораблей +40%) | 15.6 | W65400 G24050 | [B] `eurpor` |
| `denaca.29` | Разработать новую систему шпангоутов и корпуса корабля (условие для постройки линейных кораблей) | 15.6 | W32300 G6800 I9000 C12800 | [B] `eurpor` |
| `denaca.30` | Обучить плотников (скорость постройки кораблей увеличивается в 10 раз) | 15.6 | W2300 S42700 G1150 | [B] `eurpor` |
| `denaca.32` | Разработать кремниевый замок к ружьям (цена мушкета -50%) | 15.6 | G6050 C7750 | [T] `dencen.1` |
| `denaca.34` | Разработать новые сорта стали для кирас (защита солдат в доспехах +2) | 15.6 | G9750 | [B] `denbla` |
| `denaca.35` | Разработать штык: вставляемый в ствол багинет, штык с трубкой (сила удара холодного оружия +5) | 15.6 | G11500 | [T] `dencen.1`, [B] `denbla` |
| `denaca.36` | Разработать новые сорта стали (эффективность рукопашной атаки мушкетера 18 века и гренадера +25%) | 15.6 | G19500 | [T] `dencen.1`, [B] `denbla` |
| `denaca.5` | Разработать новые снасти и сети для ловли рыбы (эффективность рыбацких лодок +100%) | 15.6 | W12400 G2520 | [B] `eurpor` |
| `denaca.6` | Разработать новые методы древообработки (условие для постройки фрегатов) | 15.6 | W12400 G7040 | [B] `eurpor` |
| `denaca.7` | Построить новые верфи для рыбацких лодок (стоимость рыбацкой лодки -85%) | 15.6 | W7300 G1220 | [B] `eurpor` |
| `denaca.8` | Разработать новые инструменты для древообработки (эффективность добычи дерева +100%) | 15.6 | F5500 G550 | [B] `denbla` |
| `denart.cannon.1.1` | — | 10.0 | W1000 S500 G300 | [B] `denbla` |
| `denart.cannon.1.2` | — | 10.0 | W3000 S1000 G500 | [B] `denbla` |
| `denart.cannon.1.3` | — | 10.0 | W6000 S2000 G1000 | [B] `denbla` |
| `denart.cannon.1.4` | — | 15.6 | F1760 G350 | [B] `denbla` |
| `denart.cannon.1.5` | — | 15.6 | F1760 G350 | [B] `denbla` |
| `denart.cannon.1.6` | — | 15.6 | F1760 G350 | [B] `denbla` |
| `denart.cannon.2.1` | — | 10.0 | G500 I1000 | [B] `denbla` |
| `denart.cannon.2.2` | — | 10.0 | G1000 I2000 | [B] `denbla` |
| `denart.cannon.2.3` | — | 10.0 | G2000 I3000 | [B] `denbla` |
| `denart.cannon.2.4` | — | 15.6 | F2560 | [B] `denbla` |
| `denart.cannon.2.5` | — | 15.6 | F3560 | [B] `denbla` |
| `denart.cannon.2.6` | — | 15.6 | F5560 | [B] `denbla` |
| `denart.howitzer.1.1` | — | 10.0 | W1000 S500 G300 | [B] `denbla` |
| `denart.howitzer.1.2` | — | 10.0 | W3000 S1000 G500 | [B] `denbla` |
| `denart.howitzer.1.3` | — | 10.0 | W6000 S2000 G1000 | [B] `denbla` |
| `denart.howitzer.1.4` | — | 15.6 | F1760 G350 | [B] `denbla` |
| `denart.howitzer.1.5` | — | 15.6 | F1760 G350 | [B] `denbla` |
| `denart.howitzer.1.6` | — | 15.6 | F1760 G350 | [B] `denbla` |
| `denart.howitzer.2.1` | — | 10.0 | G500 I1000 | [B] `denbla` |
| `denart.howitzer.2.2` | — | 10.0 | G1000 I2000 | [B] `denbla` |
| `denart.howitzer.2.3` | — | 10.0 | G2000 I3000 | [B] `denbla` |
| `denart.howitzer.2.4` | — | 31.2 | F2560 | [B] `denbla` |
| `denart.howitzer.2.5` | — | 31.2 | F3560 | [B] `denbla` |
| `denart.howitzer.2.6` | — | 31.2 | F5560 | [B] `denbla` |
| `denbar.pikeman.1.6` | — | 15.6 | F15000 G1875 | [B] `denbla` |
| `denbar.pikeman.2.6` | — | 15.6 | F11250 G1500 | [B] `denbla` |
| `denbla.4` | Выковать штыки и тесаки для пехоты (сила удара мушкетера 18 века и гренадера +5) | 15.6 | W1300 G1500 I900 C5000 | [T] `dencen.1` |
| `dencen.1` | — | 9.4 | F20000 G6500 I1100 C1100 | [B] `denaca`, [B] `dentem`, [B] `denart` |
| `eurcoa.4` | — | 9.4 | F15800 G18500 | [T] `dencen.1` |
| `eurcoa.5` | — | 9.4 | F19800 G21050 | [T] `dencen.1` |
| `eurcoa.6` | — | 9.4 | F50200 G25950 | [T] `dencen.1` |
| `eurgol.4` | — | 9.4 | F15800 G18500 | [T] `dencen.1` |
| `eurgol.5` | — | 9.4 | F19800 G21050 | [T] `dencen.1` |
| `eurgol.6` | — | 9.4 | F50200 G25950 | [T] `dencen.1` |
| `euriro.4` | — | 9.4 | F15800 G18500 | [T] `dencen.1` |
| `euriro.5` | — | 9.4 | F19800 G21050 | [T] `dencen.1` |
| `euriro.6` | — | 9.4 | F50200 G25950 | [T] `dencen.1` |
| `eurpor.1` | — | 46.9 | W20000 G1500 | [B] `denart` |
| `eurtow.1` | — | 31.2 | G250 | [B] `denart` |
| `eurtow.2` | — | 31.2 | I350 | [B] `denart` |
| `eurtow.3` | — | 31.2 | C400 | [B] `denart` |
| `eurtow.4` | — | 31.2 | I450 | [B] `denart` |
| `eurtow.5` | — | 31.2 | C500 | [B] `denart` |
| `ferry.1` | Усовершенствовать конструкцию транспортного судна (+%value% посадочных мест) | 15.6 | F1000 G1250 | [T] `dencen.1` |

[↑ к содержанию](#содержание)

## ENG — England (Англия)

### `eng` — здания

| sid | имя | Время (g-сек) | цена | ферма | требует |
|---|---|---:|---|---:|---|
| `engaca` | Академия | 625.0 | W1150 S1200 | — | [B] `engbar` |
| `engart` | Артиллерийское депо | 245.9 | W100 S1000 C1400 | — | [B] `engaca` |
| `engba2` | Казарма 18в. | 5625.0 | W1700 S2950 G4000 | 250 | [T] `engcen.1` |
| `engbar` | Казарма 17в. | 93.8 | W100 S100 G500 | 150 | [B] `engbla` |
| `engbla` | Кузница | 93.8 | W100 S30 I640 | — | [B] `engcen` |
| `engcen` | Городской центр | 156.2 | W700 S700 | 100 | — |
| `engdip` | Дипломатический центр | 312.5 | W4900 S1700 | — | [B] `engaca` |
| `enghou` | Дом | 31.2 | W100 S100 | 25 | [B] `engcen` |
| `engsta` | Конюшня | 375.0 | W2350 G800 | — | [B] `engbla` |
| `engtem` | Собор | 156.2 | W1000 S1200 I500 | — | [B] `engcen` |
| `eurcoa` | Шахта | 93.8 | W100 S100 | — | — |
| `eurgol` | Шахта | 93.8 | W100 S100 | — | — |
| `euriro` | Шахта | 93.8 | W100 S100 | — | — |
| `eurmar` | Рынок | 234.4 | W450 | — | [B] `eurmil`, [B] `eursto` |
| `eurmil` | Мельница | 93.8 | W30 S150 | — | — |
| `eurpor` | Порт | 1562.5 | W1600 S800 I400 | — | [B] `eurmar` |
| `eursga` | Каменные ворота | 90.0 | S50 | — | — |
| `eursto` | Склад | 31.2 | W50 S20 | — | [B] `engcen` |
| `eurswa` | Стена | 90.0 | S50 | — | [B] `eursto` |
| `eurtow` | Башня | 1230.3 | W100 S100 G150 | — | [B] `eursto` |
| `ukrwga` | Деревянные ворота | 5.6 | W10 | — | — |
| `ukrwwa` | Частокол | 5.6 | W10 | — | [B] `eursto` |

### `eng` — юниты

| sid | имя | Время (g-сек) | цена | тренируется в | требует |
|---|---|---:|---|---|---|
| `archerdip` | Лучник (наемник) | 1.25 | G15 | engdip | [B] `engaca`, [B] `engcen` |
| `archerturdip` | Турецкий лучник (наемник) | 1.25 | G15 | engdip | [B] `engaca`, [B] `engcen` |
| `bagpiper` | Волынщик | 7.00 | F120 G20 | engba2 | [B] `engaca` |
| `battleship` | Линейный корабль | 390.00 | W9000 G3200 I700 C6500 | eurpor | [T] `engaca.29`, [B] `engart` |
| `cannon` | Пушка | 75.00 | W250 G400 I400 | engart | [B] `engbla` |
| `cossacksichdip` | Сечевой козак (наемник) | 2.50 | G60 | engdip | [B] `engaca`, [B] `engcen` |
| `cuirassier` | Кирасир | 22.50 | F120 G35 I25 | engsta | [B] `engbla`, [T] `engcen.1` |
| `dragoon` | Драгун 17в. | 15.00 | F90 G7 I5 | engsta | [B] `engbla` |
| `dragoon18` | Драгун 18в. | 22.50 | F70 G60 I7 | engsta | [B] `engbla`, [T] `engcen.1` |
| `dragoon18dip` | Драгун 18в. (наемник) | 2.00 | G120 | engdip | [B] `engaca`, [B] `engcen` |
| `drummer` | Барабанщик 17в. | 5.00 | F60 G20 | engbar | [B] `engaca` |
| `ferry` | Транспорт | 56.00 | W300 G50 I100 | eurpor | [B] `engart` |
| `fishboat` | Рыбацкая лодка | 40.00 | W600 | eurpor | — |
| `frigate` | Фрегат | 230.00 | W5000 G1100 I600 C800 | eurpor | [T] `engaca.6`, [B] `engart` |
| `galley` | Галера | 50.00 | W9500 G900 I800 | eurpor | [B] `engart` |
| `grenadier` | Гренадер | 6.00 | F80 G60 I40 | engba2 | [B] `engbla` |
| `grenadierdip` | Гренадер (наемник) | 1.50 | G25 | engdip | [B] `engaca`, [B] `engcen` |
| `highlander` | Шотландский стрелок | 6.50 | F90 G25 I10 | engba2 | [B] `engbla` |
| `howitzer` | Гаубица | 94.00 | W250 G350 I300 | engart | [B] `engbla` |
| `hussar` | Гусар | 15.00 | F70 G20 I2 | engsta | [B] `engbla`, [T] `engcen.1` |
| `lightcavalrydip` | Легкий кавалерист (наемник) | 2.00 | G120 | engdip | [B] `engaca`, [B] `engcen` |
| `lightinfantrydip` | Легкий пехотинец (наемник) | 1.25 | G4 | engdip | [B] `engaca`, [B] `engcen` |
| `mortar` | Мортира | 25.00 | W100 G75 I200 | engart | [B] `engbla` |
| `multicannon` | Многоствольное орудие | 50.00 | W200 G400 I250 | engart | [T] `engaca.19`, [B] `engbla` |
| `musketeer` | Мушкетер 17в. | 6.00 | F45 G6 I5 | engbar | [B] `engbla` |
| `musketeer18` | Мушкетер 18в. | 4.50 | F50 G40 I40 | engba2 | [B] `engbla` |
| `officer` | Офицер 17в. | 10.00 | F50 G150 I30 | engbar | [B] `engaca` |
| `officer18` | Офицер 18в. | 6.00 | F50 G200 I10 | engba2 | [B] `engaca` |
| `peaeng` | Крестьянин | 12.50 | F100 | engcen | — |
| `pikeman` | Пикинер 17в. | 4.50 | F25 G3 I20 | engbar | [B] `engbla` |
| `pikeman18` | Пикинер 18в. | 1.25 | F30 G2 | engba2 | — |
| `priest` | Капеллан | 20.00 | F60 G25 | engtem | — |
| `reiter` | Рейтар | 24.00 | F120 G10 I40 | engsta | [B] `engbla` |
| `roundshierdip` | Рундашир (наемник) | 1.50 | G12 | engdip | [B] `engaca`, [B] `engcen` |
| `unitbox` | — | 3.12 | F100 | — | — |
| `yacht` | Яхта | 48.00 | W900 G450 I150 C200 | eurpor | [B] `engart` |

### `eng` — ключевые апгрейды (с зависимостями)

| sid | имя | Время (g-сек) | цена | требует |
|---|---|---:|---|---|
| `engaca.12` | Улучшить стрелковое оружие: нарезной ствол (сила выстрела +10%) | 15.6 | I5000 | [B] `engbla` |
| `engaca.13` | Исследовать гранулированный порох (сила выстрела +10%) | 15.6 | G4000 | [B] `engbla` |
| `engaca.14` | Исследовать новые методы очистки серы (сила выстрела +15%) | 15.6 | G7000 | [B] `engbla` |
| `engaca.15` | Исследовать новые методы очистки селитры (сила выстрела +25%) | 15.6 | C11000 | [B] `engbla` |
| `engaca.16` | Исследовать новые добавки в порох (дальность стрельбы артиллерии +5%) | 15.6 | G2000 I12150 | [B] `engart` |
| `engaca.17` | Разработать новые виды стволов: единорог, карронада (дальность стрельбы артиллерии +10%) | 15.6 | S3000 G4550 I19200 | [B] `engart` |
| `engaca.18` | Разработать более прочный лафет для орудий: система Грибоваля (прочность пушек +50%) | 15.6 | G500 I3830 C1500 | [B] `engart` |
| `engaca.19` | Разработать многоствольное орудие | 15.6 | G1500 C2500 | [B] `engart` |
| `engaca.20` | Разработать новые прицельные системы для пушек (меткость стрельбы артиллерии +35%) | 15.6 | W3540 G2000 C7250 | [B] `engart` |
| `engaca.21` | Выделить деньги на ремонтные мастерские для пушек (отремонтировать все пушки) | 15.6 | W350 G100 C250 | [B] `engart` |
| `engaca.25` | Разработать монгольфьер (открывает всю карту) | 15.6 | G5750 | [T] `engcen.1` |
| `engaca.27` | Развивать математику (меткость выстрела орудий +35%) | 15.6 | W9540 G12000 C65200 | [B] `engart` |
| `engaca.28` | Разработать новые парусные системы (скорость кораблей +40%) | 15.6 | W53400 G22050 | [B] `eurpor` |
| `engaca.29` | Разработать новую систему шпангоутов и корпуса корабля (условие для постройки линейных кораблей) | 15.6 | W22300 G6800 I7500 C13200 | [B] `eurpor` |
| `engaca.30` | Обучить плотников (скорость постройки кораблей увеличивается в 10 раз) | 15.6 | W2300 S42700 G1150 | [B] `eurpor` |
| `engaca.32` | Разработать кремниевый замок к ружьям (цена мушкета -50%) | 15.6 | G6050 C7750 | [T] `engcen.1` |
| `engaca.34` | Разработать новые сорта стали для кирас (защита солдат в доспехах +2) | 15.6 | G9750 | [B] `engbla` |
| `engaca.35` | Разработать штык: вставляемый в ствол багинет, штык с трубкой (сила удара холодного оружия +5) | 15.6 | G11500 | [T] `engcen.1`, [B] `engbla` |
| `engaca.36` | Разработать новые сорта стали (эффективность рукопашной атаки мушкетера 18 века и гренадера +25%) | 15.6 | G19500 | [T] `engcen.1`, [B] `engbla` |
| `engaca.5` | Разработать новые снасти и сети для ловли рыбы (эффективность рыбацких лодок +100%) | 15.6 | W12400 G3520 | [B] `eurpor` |
| `engaca.6` | Разработать новые методы древообработки (условие для постройки фрегатов) | 15.6 | W12400 G7040 | [B] `eurpor` |
| `engaca.7` | Построить новые верфи для рыбацких лодок (стоимость рыбацкой лодки -85%) | 15.6 | W7300 G1220 | [B] `eurpor` |
| `engaca.8` | Разработать новые инструменты для древообработки (эффективность добычи дерева +100%) | 15.6 | F5500 G550 | [B] `engbla` |
| `engart.cannon.1.1` | — | 10.0 | W1000 S500 G300 | [B] `engbla` |
| `engart.cannon.1.2` | — | 10.0 | W3000 S1000 G500 | [B] `engbla` |
| `engart.cannon.1.3` | — | 10.0 | W6000 S2000 G1000 | [B] `engbla` |
| `engart.cannon.1.4` | — | 15.6 | F1760 G350 | [B] `engbla` |
| `engart.cannon.1.5` | — | 15.6 | F1760 G350 | [B] `engbla` |
| `engart.cannon.1.6` | — | 15.6 | F1760 G350 | [B] `engbla` |
| `engart.cannon.2.1` | — | 10.0 | G500 I1000 | [B] `engbla` |
| `engart.cannon.2.2` | — | 10.0 | G1000 I2000 | [B] `engbla` |
| `engart.cannon.2.3` | — | 10.0 | G2000 I3000 | [B] `engbla` |
| `engart.cannon.2.4` | — | 15.6 | F2560 | [B] `engbla` |
| `engart.cannon.2.5` | — | 15.6 | F3560 | [B] `engbla` |
| `engart.cannon.2.6` | — | 15.6 | F5560 | [B] `engbla` |
| `engart.howitzer.1.1` | — | 10.0 | W1000 S500 G300 | [B] `engbla` |
| `engart.howitzer.1.2` | — | 10.0 | W3000 S1000 G500 | [B] `engbla` |
| `engart.howitzer.1.3` | — | 10.0 | W6000 S2000 G1000 | [B] `engbla` |
| `engart.howitzer.1.4` | — | 15.6 | F1760 G350 | [B] `engbla` |
| `engart.howitzer.1.5` | — | 15.6 | F1760 G350 | [B] `engbla` |
| `engart.howitzer.1.6` | — | 15.6 | F1760 G350 | [B] `engbla` |
| `engart.howitzer.2.1` | — | 10.0 | G500 I1000 | [B] `engbla` |
| `engart.howitzer.2.2` | — | 10.0 | G1000 I2000 | [B] `engbla` |
| `engart.howitzer.2.3` | — | 10.0 | G2000 I3000 | [B] `engbla` |
| `engart.howitzer.2.4` | — | 31.2 | F2560 | [B] `engbla` |
| `engart.howitzer.2.5` | — | 31.2 | F3560 | [B] `engbla` |
| `engart.howitzer.2.6` | — | 31.2 | F5560 | [B] `engbla` |
| `engba2.highlander.2.4` | — | 15.6 | F3600 G600 | [B] `engbla` |
| `engba2.highlander.2.5` | — | 15.6 | F5400 G900 | [B] `engbla` |
| `engba2.highlander.2.6` | — | 15.6 | F11250 G1875 | [B] `engbla` |
| `engbar.pikeman.1.6` | — | 15.6 | F15000 G1875 | [B] `engbla` |
| `engbar.pikeman.2.6` | — | 15.6 | F11250 G1500 | [B] `engbla` |
| `engbla.4` | Выковать штыки и тесаки для пехоты (сила удара мушкетера 18 века и гренадера +5) | 15.6 | W1300 G1500 I900 C5000 | [T] `engcen.1` |
| `engcen.1` | — | 9.4 | F25000 G5000 I5500 C5500 | [B] `engaca`, [B] `engtem`, [B] `engart` |
| `eurcoa.4` | — | 9.4 | F15800 G18500 | [T] `engcen.1` |
| `eurcoa.5` | — | 9.4 | F19800 G21050 | [T] `engcen.1` |
| `eurcoa.6` | — | 9.4 | F50200 G25950 | [T] `engcen.1` |
| `eurgol.4` | — | 9.4 | F15800 G18500 | [T] `engcen.1` |
| `eurgol.5` | — | 9.4 | F19800 G21050 | [T] `engcen.1` |
| `eurgol.6` | — | 9.4 | F50200 G25950 | [T] `engcen.1` |
| `euriro.4` | — | 9.4 | F15800 G18500 | [T] `engcen.1` |
| `euriro.5` | — | 9.4 | F19800 G21050 | [T] `engcen.1` |
| `euriro.6` | — | 9.4 | F50200 G25950 | [T] `engcen.1` |
| `eurpor.1` | — | 46.9 | W12000 G500 | [B] `engart` |
| `eurtow.1` | — | 31.2 | G250 | [B] `engart` |
| `eurtow.2` | — | 31.2 | I350 | [B] `engart` |
| `eurtow.3` | — | 31.2 | C400 | [B] `engart` |
| `eurtow.4` | — | 31.2 | I450 | [B] `engart` |
| `eurtow.5` | — | 31.2 | C500 | [B] `engart` |
| `ferry.1` | Усовершенствовать конструкцию транспортного судна (+%value% посадочных мест) | 15.6 | F1000 G1250 | [T] `engcen.1` |

[↑ к содержанию](#содержание)

## FRA — France (Франция)

### `fra` — здания

| sid | имя | Время (g-сек) | цена | ферма | требует |
|---|---|---:|---|---:|---|
| `eurcoa` | Шахта | 93.8 | W100 S100 | — | — |
| `eurgol` | Шахта | 93.8 | W100 S100 | — | — |
| `euriro` | Шахта | 93.8 | W100 S100 | — | — |
| `eurmar` | Рынок | 234.4 | W450 | — | [B] `eurmil`, [B] `eursto` |
| `eurmil` | Мельница | 93.8 | W30 S150 | — | — |
| `eurpor` | Порт | 1562.5 | W1600 S800 I400 | — | [B] `eurmar` |
| `eursga` | Каменные ворота | 90.0 | S50 | — | — |
| `eursto` | Склад | 31.2 | W50 S20 | — | [B] `fracen` |
| `eurswa` | Стена | 90.0 | S50 | — | [B] `eursto` |
| `eurtow` | Башня | 1230.3 | W100 S100 G150 | — | [B] `eursto` |
| `fraaca` | Академия | 625.0 | W1250 S1100 | — | [B] `frabar` |
| `fraart` | Артиллерийское депо | 245.9 | W100 S1000 C1400 | — | [B] `fraaca` |
| `fraba2` | Казарма 18в. | 5625.0 | W1700 S2950 G4000 | 250 | [T] `fracen.1` |
| `frabar` | Казарма 17в. | 93.8 | W100 S100 G500 | 150 | [B] `frabla` |
| `frabla` | Кузница | 93.8 | W100 S30 I640 | — | [B] `fracen` |
| `fracen` | Городской центр | 156.2 | W700 S700 | 100 | — |
| `fradip` | Дипломатический центр | 312.5 | W4900 S1700 | — | [B] `fraaca` |
| `frahou` | Дом | 31.2 | W100 S100 | 25 | [B] `fracen` |
| `frasta` | Конюшня | 625.0 | W2500 S100 G600 | — | [B] `frabla` |
| `fratem` | Собор | 312.5 | W1100 S2000 I600 | — | [B] `fracen` |
| `ukrwga` | Деревянные ворота | 5.6 | W10 | — | — |
| `ukrwwa` | Частокол | 5.6 | W10 | — | [B] `eursto` |

### `fra` — юниты

| sid | имя | Время (g-сек) | цена | тренируется в | требует |
|---|---|---:|---|---|---|
| `archerdip` | Лучник (наемник) | 1.25 | G15 | fradip | [B] `fraaca`, [B] `fracen` |
| `archerturdip` | Турецкий лучник (наемник) | 1.25 | G15 | fradip | [B] `fraaca`, [B] `fracen` |
| `battleship` | Линейный корабль | 390.00 | W9000 G3200 I700 C6500 | eurpor | [T] `fraaca.29`, [B] `fraart` |
| `cannon` | Пушка | 75.00 | W250 G400 I400 | fraart | [B] `frabla` |
| `chasseur` | Егерь | 7.50 | F50 G45 I15 | fraba2 | [B] `frabla` |
| `cossacksichdip` | Сечевой козак (наемник) | 2.50 | G60 | fradip | [B] `fraaca`, [B] `fracen` |
| `cuirassier` | Кирасир | 22.50 | F120 G35 I25 | frasta | [B] `frabla`, [T] `fracen.1` |
| `dragoon` | Драгун 17в. | 15.00 | F90 G7 I5 | frasta | [B] `frabla` |
| `dragoon18dip` | Драгун 18в. (наемник) | 2.00 | G120 | fradip | [B] `fraaca`, [B] `fracen` |
| `dragoon18fra` | Драгун 18в. | 15.00 | F50 G30 I6 | frasta | [B] `frabla`, [T] `fracen.1` |
| `drummer` | Барабанщик 17в. | 5.00 | F60 G20 | frabar | [B] `fraaca` |
| `drummer18` | Барабанщик 18в. | 6.00 | F50 G30 | fraba2 | [B] `fraaca` |
| `ferry` | Транспорт | 56.00 | W300 G50 I100 | eurpor | [B] `fraart` |
| `fishboat` | Рыбацкая лодка | 40.00 | W600 | eurpor | — |
| `frigate` | Фрегат | 230.00 | W5000 G1100 I600 C800 | eurpor | [T] `fraaca.6`, [B] `fraart` |
| `galley` | Галера | 50.00 | W9500 G900 I800 | eurpor | [B] `fraart` |
| `grenadier` | Гренадер | 6.00 | F80 G60 I40 | fraba2 | [B] `frabla` |
| `grenadierdip` | Гренадер (наемник) | 1.50 | G25 | fradip | [B] `fraaca`, [B] `fracen` |
| `howitzer` | Гаубица | 94.00 | W250 G350 I300 | fraart | [B] `frabla` |
| `hussar` | Гусар | 15.00 | F70 G20 I2 | frasta | [B] `frabla`, [T] `fracen.1` |
| `kingmusketeer` | Королевский мушкетер | 27.00 | F100 G100 I8 | frasta | [B] `frabla` |
| `lightcavalrydip` | Легкий кавалерист (наемник) | 2.00 | G120 | fradip | [B] `fraaca`, [B] `fracen` |
| `lightinfantrydip` | Легкий пехотинец (наемник) | 1.25 | G4 | fradip | [B] `fraaca`, [B] `fracen` |
| `mortar` | Мортира | 25.00 | W100 G75 I200 | fraart | [B] `frabla` |
| `multicannon` | Многоствольное орудие | 50.00 | W200 G400 I250 | fraart | [T] `fraaca.19`, [B] `frabla` |
| `musketeer` | Мушкетер 17в. | 6.00 | F45 G6 I5 | frabar | [B] `frabla` |
| `musketeer18` | Мушкетер 18в. | 4.50 | F50 G40 I40 | fraba2 | [B] `frabla` |
| `officer` | Офицер 17в. | 10.00 | F50 G150 I30 | frabar | [B] `fraaca` |
| `officer18` | Офицер 18в. | 6.00 | F50 G200 I10 | fraba2 | [B] `fraaca` |
| `peaeng` | Крестьянин | 12.50 | F100 | fracen | — |
| `pikeman` | Пикинер 17в. | 4.50 | F25 G3 I20 | frabar | [B] `frabla` |
| `pikeman18` | Пикинер 18в. | 1.25 | F30 G2 | fraba2 | — |
| `priest` | Капеллан | 20.00 | F60 G25 | fratem | — |
| `reiter` | Рейтар | 24.00 | F120 G10 I40 | frasta | [B] `frabla` |
| `roundshierdip` | Рундашир (наемник) | 1.50 | G12 | fradip | [B] `fraaca`, [B] `fracen` |
| `unitbox` | — | 3.12 | F100 | — | — |
| `yacht` | Яхта | 48.00 | W900 G450 I150 C200 | eurpor | [B] `fraart` |

### `fra` — ключевые апгрейды (с зависимостями)

| sid | имя | Время (g-сек) | цена | требует |
|---|---|---:|---|---|
| `eurcoa.4` | — | 9.4 | F15800 G18500 | [T] `fracen.1` |
| `eurcoa.5` | — | 9.4 | F19800 G21050 | [T] `fracen.1` |
| `eurcoa.6` | — | 9.4 | F50200 G25950 | [T] `fracen.1` |
| `eurgol.4` | — | 9.4 | F15800 G18500 | [T] `fracen.1` |
| `eurgol.5` | — | 9.4 | F19800 G21050 | [T] `fracen.1` |
| `eurgol.6` | — | 9.4 | F50200 G25950 | [T] `fracen.1` |
| `euriro.4` | — | 9.4 | F15800 G18500 | [T] `fracen.1` |
| `euriro.5` | — | 9.4 | F19800 G21050 | [T] `fracen.1` |
| `euriro.6` | — | 9.4 | F50200 G25950 | [T] `fracen.1` |
| `eurpor.1` | — | 46.9 | W20000 G1500 | [B] `fraart` |
| `eurtow.1` | — | 31.2 | G250 | [B] `fraart` |
| `eurtow.2` | — | 31.2 | I350 | [B] `fraart` |
| `eurtow.3` | — | 31.2 | C400 | [B] `fraart` |
| `eurtow.4` | — | 31.2 | I450 | [B] `fraart` |
| `eurtow.5` | — | 31.2 | C500 | [B] `fraart` |
| `ferry.1` | Усовершенствовать конструкцию транспортного судна (+%value% посадочных мест) | 15.6 | F1000 G1250 | [T] `fracen.1` |
| `fraaca.12` | Улучшить стрелковое оружие: нарезной ствол (сила выстрела +10%) | 15.6 | I5000 | [B] `frabla` |
| `fraaca.13` | Исследовать гранулированный порох (сила выстрела +10%) | 15.6 | G4000 | [B] `frabla` |
| `fraaca.14` | Исследовать новые методы очистки серы (сила выстрела +15%) | 15.6 | G7000 | [B] `frabla` |
| `fraaca.15` | Исследовать новые методы очистки селитры (сила выстрела +25%) | 15.6 | C11000 | [B] `frabla` |
| `fraaca.16` | Исследовать новые добавки в порох (дальность стрельбы артиллерии +5%) | 15.6 | G2000 I12150 | [B] `fraart` |
| `fraaca.17` | Разработать новые виды стволов: единорог, карронада (дальность стрельбы артиллерии +10%) | 15.6 | S3000 G4550 I19200 | [B] `fraart` |
| `fraaca.18` | Разработать более прочный лафет для орудий: система Грибоваля (прочность пушек +50%) | 15.6 | G500 I3830 C1500 | [B] `fraart` |
| `fraaca.19` | Разработать многоствольное орудие | 15.6 | G1500 C2500 | [B] `fraart` |
| `fraaca.20` | Разработать новые прицельные системы для пушек (меткость стрельбы артиллерии +35%) | 15.6 | W13540 G1500 C5950 | [B] `fraart` |
| `fraaca.21` | Выделить деньги на ремонтные мастерские для пушек (отремонтировать все пушки) | 15.6 | W350 G100 C250 | [B] `fraart` |
| `fraaca.25` | Разработать монгольфьер (открывает всю карту) | 15.6 | G5750 | [T] `fracen.1` |
| `fraaca.27` | Развивать математику (меткость выстрела орудий +35%) | 15.6 | W23580 G9800 C65400 | [B] `fraart` |
| `fraaca.28` | Разработать новые парусные системы (скорость кораблей +40%) | 15.6 | W65400 G24050 | [B] `eurpor` |
| `fraaca.29` | Разработать новую систему шпангоутов и корпуса корабля (условие для постройки линейных кораблей) | 15.6 | W32300 G6800 I9000 C12800 | [B] `eurpor` |
| `fraaca.30` | Обучить плотников (скорость постройки кораблей увеличивается в 10 раз) | 15.6 | W2300 S42700 G1150 | [B] `eurpor` |
| `fraaca.32` | Разработать кремниевый замок к ружьям (цена мушкета -50%) | 15.6 | G6050 C7750 | [T] `fracen.1` |
| `fraaca.34` | Разработать новые сорта стали для кирас (защита солдат в доспехах +2) | 15.6 | G9750 | [B] `frabla` |
| `fraaca.35` | Разработать штык: вставляемый в ствол багинет, штык с трубкой (сила удара холодного оружия +5) | 15.6 | G11500 | [T] `fracen.1`, [B] `frabla` |
| `fraaca.36` | Разработать новые сорта стали (эффективность рукопашной атаки мушкетера 18 века и гренадера +25%) | 15.6 | G19500 | [T] `fracen.1`, [B] `frabla` |
| `fraaca.5` | Разработать новые снасти и сети для ловли рыбы (эффективность рыбацких лодок +100%) | 15.6 | W13900 G2420 | [B] `eurpor` |
| `fraaca.6` | Разработать новые методы древообработки (условие для постройки фрегатов) | 15.6 | W13500 G7250 | [B] `eurpor` |
| `fraaca.7` | Построить новые верфи для рыбацких лодок (стоимость рыбацкой лодки -85%) | 15.6 | W7800 G1110 | [B] `eurpor` |
| `fraaca.8` | Разработать новые инструменты для древообработки (эффективность добычи дерева +100%) | 15.6 | F5500 G550 | [B] `frabla` |
| `fraart.cannon.1.1` | — | 10.0 | W1000 S500 G300 | [B] `frabla` |
| `fraart.cannon.1.2` | — | 10.0 | W3000 S1000 G500 | [B] `frabla` |
| `fraart.cannon.1.3` | — | 10.0 | W6000 S2000 G1000 | [B] `frabla` |
| `fraart.cannon.1.4` | — | 15.6 | F1760 G350 | [B] `frabla` |
| `fraart.cannon.1.5` | — | 15.6 | F1760 G350 | [B] `frabla` |
| `fraart.cannon.1.6` | — | 15.6 | F1760 G350 | [B] `frabla` |
| `fraart.cannon.2.1` | — | 10.0 | G500 I1000 | [B] `frabla` |
| `fraart.cannon.2.2` | — | 10.0 | G1000 I2000 | [B] `frabla` |
| `fraart.cannon.2.3` | — | 10.0 | G2000 I3000 | [B] `frabla` |
| `fraart.cannon.2.4` | — | 15.6 | F2560 | [B] `frabla` |
| `fraart.cannon.2.5` | — | 15.6 | F3560 | [B] `frabla` |
| `fraart.cannon.2.6` | — | 15.6 | F5560 | [B] `frabla` |
| `fraart.howitzer.1.1` | — | 10.0 | W1000 S500 G300 | [B] `frabla` |
| `fraart.howitzer.1.2` | — | 10.0 | W3000 S1000 G500 | [B] `frabla` |
| `fraart.howitzer.1.3` | — | 10.0 | W6000 S2000 G1000 | [B] `frabla` |
| `fraart.howitzer.1.4` | — | 15.6 | F1760 G350 | [B] `frabla` |
| `fraart.howitzer.1.5` | — | 15.6 | F1760 G350 | [B] `frabla` |
| `fraart.howitzer.1.6` | — | 15.6 | F1760 G350 | [B] `frabla` |
| `fraart.howitzer.2.1` | — | 10.0 | G500 I1000 | [B] `frabla` |
| `fraart.howitzer.2.2` | — | 10.0 | G1000 I2000 | [B] `frabla` |
| `fraart.howitzer.2.3` | — | 10.0 | G2000 I3000 | [B] `frabla` |
| `fraart.howitzer.2.4` | — | 31.2 | F2560 | [B] `frabla` |
| `fraart.howitzer.2.5` | — | 31.2 | F3560 | [B] `frabla` |
| `fraart.howitzer.2.6` | — | 31.2 | F5560 | [B] `frabla` |
| `frabar.pikeman.1.6` | — | 15.6 | F15000 G1875 | [B] `frabla` |
| `frabar.pikeman.2.6` | — | 15.6 | F11250 G1500 | [B] `frabla` |
| `frabla.4` | Выковать штыки и тесаки для пехоты (сила удара мушкетера 18 века и гренадера +5) | 15.6 | W1300 G1500 I900 C5000 | [T] `fracen.1` |
| `fracen.1` | — | 9.4 | F40000 G3500 I4000 C4000 | [B] `fraaca`, [B] `fratem`, [B] `fraart` |

[↑ к содержанию](#содержание)

## HUN — Hungary (Венгрия)

### `hun` — здания

| sid | имя | Время (g-сек) | цена | ферма | требует |
|---|---|---:|---|---:|---|
| `eurcoa` | Шахта | 93.8 | W100 S100 | — | — |
| `eurgol` | Шахта | 93.8 | W100 S100 | — | — |
| `euriro` | Шахта | 93.8 | W100 S100 | — | — |
| `eurmar` | Рынок | 234.4 | W450 | — | [B] `eurmil`, [B] `eursto` |
| `eurmil` | Мельница | 93.8 | W30 S150 | — | — |
| `eurpor` | Порт | 1562.5 | W1600 S800 I400 | — | [B] `eurmar` |
| `eursga` | Каменные ворота | 90.0 | S50 | — | — |
| `eursto` | Склад | 31.2 | W50 S20 | — | [B] `huncen` |
| `eurswa` | Стена | 90.0 | S50 | — | [B] `eursto` |
| `eurtow` | Башня | 1230.3 | W100 S100 G150 | — | [B] `eursto` |
| `hunaca` | Академия | 625.0 | W1250 S1100 | — | [B] `hunbar` |
| `hunart` | Артиллерийское депо | 245.9 | W100 S1000 C1400 | — | [B] `hunaca` |
| `hunba2` | Казарма 18в. | 5625.0 | W1700 S2950 G4000 | 250 | [T] `huncen.1` |
| `hunbar` | Казарма 17в. | 93.8 | W100 S100 G500 | 150 | [B] `hunbla` |
| `hunbla` | Кузница | 93.8 | W100 S30 I640 | — | [B] `huncen` |
| `huncen` | Городской центр | 156.2 | W700 S700 | 100 | — |
| `hundip` | Дипломатический центр | 312.5 | W4900 S1700 | — | [B] `hunaca` |
| `hunhou` | Дом | 31.2 | W100 S100 | 25 | [B] `huncen` |
| `hunsta` | Конюшня | 625.0 | W2500 S100 G600 | — | [B] `hunbla` |
| `huntem` | Собор | 156.2 | W1000 S1200 I500 | — | [B] `huncen` |
| `ukrwga` | Деревянные ворота | 5.6 | W10 | — | — |
| `ukrwwa` | Частокол | 5.6 | W10 | — | [B] `eursto` |

### `hun` — юниты

| sid | имя | Время (g-сек) | цена | тренируется в | требует |
|---|---|---:|---|---|---|
| `archerdip` | Лучник (наемник) | 1.25 | G15 | hundip | [B] `hunaca`, [B] `huncen` |
| `archerturdip` | Турецкий лучник (наемник) | 1.25 | G15 | hundip | [B] `hunaca`, [B] `huncen` |
| `battleship` | Линейный корабль | 390.00 | W9000 G3200 I700 C6500 | eurpor | [T] `hunaca.29`, [B] `hunart` |
| `cannon` | Пушка | 75.00 | W250 G400 I400 | hunart | [B] `hunbla` |
| `cossacksichdip` | Сечевой козак (наемник) | 2.50 | G60 | hundip | [B] `hunaca`, [B] `huncen` |
| `cuirassier` | Кирасир | 22.50 | F120 G35 I25 | hunsta | [B] `hunbla`, [T] `huncen.1` |
| `dragoon` | Драгун 17в. | 15.00 | F90 G7 I5 | hunsta | [B] `hunbla` |
| `dragoon18dip` | Драгун 18в. (наемник) | 2.00 | G120 | hundip | [B] `hunaca`, [B] `huncen` |
| `drummer` | Барабанщик 17в. | 5.00 | F60 G20 | hunbar | [B] `hunaca` |
| `drummer18` | Барабанщик 18в. | 6.00 | F50 G30 | hunba2 | [B] `hunaca` |
| `ferry` | Транспорт | 56.00 | W300 G50 I100 | eurpor | [B] `hunart` |
| `fishboat` | Рыбацкая лодка | 40.00 | W600 | eurpor | — |
| `frigate` | Фрегат | 230.00 | W5000 G1100 I600 C800 | eurpor | [T] `hunaca.6`, [B] `hunart` |
| `galley` | Галера | 50.00 | W9500 G900 I800 | eurpor | [B] `hunart` |
| `gauduk` | Гайдук | 4.50 | F35 G4 I4 | hunbar | [B] `hunbla` |
| `grenadierdip` | Гренадер (наемник) | 1.50 | G25 | hundip | [B] `hunaca`, [B] `huncen` |
| `grenadierhun` | Гренадер | 6.50 | F90 G80 I40 | hunba2 | [B] `hunbla` |
| `howitzer` | Гаубица | 94.00 | W250 G350 I300 | hunart | [B] `hunbla` |
| `hussarhun` | Гусар | 21.00 | F100 G30 I2 | hunsta | [B] `hunbla` |
| `lightcavalry` | Легкий кавалерист | 21.00 | F90 G50 I6 | hunsta | [B] `hunbla`, [T] `huncen.1` |
| `lightcavalrydip` | Легкий кавалерист (наемник) | 2.00 | G120 | hundip | [B] `hunaca`, [B] `huncen` |
| `lightinfantrydip` | Легкий пехотинец (наемник) | 1.25 | G4 | hundip | [B] `hunaca`, [B] `huncen` |
| `mortar` | Мортира | 25.00 | W100 G75 I200 | hunart | [B] `hunbla` |
| `multicannon` | Многоствольное орудие | 50.00 | W200 G400 I250 | hunart | [T] `hunaca.19`, [B] `hunbla` |
| `musketeer18` | Мушкетер 18в. | 4.50 | F50 G40 I40 | hunba2 | [B] `hunbla` |
| `officer` | Офицер 17в. | 10.00 | F50 G150 I30 | hunbar | [B] `hunaca` |
| `officer18` | Офицер 18в. | 6.00 | F50 G200 I10 | hunba2 | [B] `hunaca` |
| `pandurhun` | Секей | 6.50 | F30 G25 I10 | hunba2 | [B] `hunbla` |
| `peapol` | Крестьянин | 12.50 | F100 | huncen | — |
| `pikeman` | Пикинер 17в. | 4.50 | F25 G3 I20 | hunbar | [B] `hunbla` |
| `pikeman18` | Пикинер 18в. | 1.25 | F30 G2 | hunba2 | — |
| `priest` | Капеллан | 20.00 | F60 G25 | huntem | — |
| `reiter` | Рейтар | 24.00 | F120 G10 I40 | hunsta | [B] `hunbla` |
| `roundshierdip` | Рундашир (наемник) | 1.50 | G12 | hundip | [B] `hunaca`, [B] `huncen` |
| `unitbox` | — | 3.12 | F100 | — | — |
| `yacht` | Яхта | 48.00 | W900 G450 I150 C200 | eurpor | [B] `hunart` |

### `hun` — ключевые апгрейды (с зависимостями)

| sid | имя | Время (g-сек) | цена | требует |
|---|---|---:|---|---|
| `eurcoa.4` | — | 9.4 | F15800 G18500 | [T] `huncen.1` |
| `eurcoa.5` | — | 9.4 | F19800 G21050 | [T] `huncen.1` |
| `eurcoa.6` | — | 9.4 | F50200 G25950 | [T] `huncen.1` |
| `eurgol.4` | — | 9.4 | F15800 G18500 | [T] `huncen.1` |
| `eurgol.5` | — | 9.4 | F19800 G21050 | [T] `huncen.1` |
| `eurgol.6` | — | 9.4 | F50200 G25950 | [T] `huncen.1` |
| `euriro.4` | — | 9.4 | F15800 G18500 | [T] `huncen.1` |
| `euriro.5` | — | 9.4 | F19800 G21050 | [T] `huncen.1` |
| `euriro.6` | — | 9.4 | F50200 G25950 | [T] `huncen.1` |
| `eurpor.1` | — | 46.9 | W20000 G1500 | [B] `hunart` |
| `eurtow.1` | — | 31.2 | G250 | [B] `hunart` |
| `eurtow.2` | — | 31.2 | I350 | [B] `hunart` |
| `eurtow.3` | — | 31.2 | C400 | [B] `hunart` |
| `eurtow.4` | — | 31.2 | I450 | [B] `hunart` |
| `eurtow.5` | — | 31.2 | C500 | [B] `hunart` |
| `ferry.1` | Усовершенствовать конструкцию транспортного судна (+%value% посадочных мест) | 15.6 | F1000 G1250 | [T] `huncen.1` |
| `hunaca.12` | Улучшить стрелковое оружие: нарезной ствол (сила выстрела +10%) | 15.6 | I5000 | [B] `hunbla` |
| `hunaca.13` | Исследовать гранулированный порох (сила выстрела +10%) | 15.6 | G4000 | [B] `hunbla` |
| `hunaca.14` | Исследовать новые методы очистки серы (сила выстрела +15%) | 15.6 | G7000 | [B] `hunbla` |
| `hunaca.15` | Исследовать новые методы очистки селитры (сила выстрела +25%) | 15.6 | C11000 | [B] `hunbla` |
| `hunaca.16` | Исследовать новые добавки в порох (дальность стрельбы артиллерии +5%) | 15.6 | G2000 I12150 | [B] `hunart` |
| `hunaca.17` | Разработать новые виды стволов: единорог, карронада (дальность стрельбы артиллерии +10%) | 15.6 | S3000 G4550 I19200 | [B] `hunart` |
| `hunaca.18` | Разработать более прочный лафет для орудий: система Грибоваля (прочность пушек +50%) | 15.6 | G500 I3830 C1500 | [B] `hunart` |
| `hunaca.19` | Разработать многоствольное орудие | 15.6 | G1500 C2500 | [B] `hunart` |
| `hunaca.20` | Разработать новые прицельные системы для пушек (меткость стрельбы артиллерии +35%) | 15.6 | W3540 G2000 C7250 | [B] `hunart` |
| `hunaca.21` | Выделить деньги на ремонтные мастерские для пушек (отремонтировать все пушки) | 15.6 | W350 G100 C250 | [B] `hunart` |
| `hunaca.25` | Разработать монгольфьер (открывает всю карту) | 15.6 | G5750 | [T] `huncen.1` |
| `hunaca.27` | Развивать математику (меткость выстрела орудий +35%) | 15.6 | W9540 G12000 C65200 | [B] `hunart` |
| `hunaca.28` | Разработать новые парусные системы (скорость кораблей +40%) | 15.6 | W65400 G24050 | [B] `eurpor` |
| `hunaca.29` | Разработать новую систему шпангоутов и корпуса корабля (условие для постройки линейных кораблей) | 15.6 | W32300 G6800 I9000 C12800 | [B] `eurpor` |
| `hunaca.30` | Обучить плотников (скорость постройки кораблей увеличивается в 10 раз) | 15.6 | W2300 S42700 G1150 | [B] `eurpor` |
| `hunaca.32` | Разработать кремниевый замок к ружьям (цена мушкета -50%) | 15.6 | G6050 C7750 | [T] `huncen.1` |
| `hunaca.34` | Разработать новые сорта стали для кирас (защита солдат в доспехах +2) | 15.6 | G9750 | [B] `hunbla` |
| `hunaca.35` | Разработать штык: вставляемый в ствол багинет, штык с трубкой (сила удара холодного оружия +5) | 15.6 | G11500 | [T] `huncen.1`, [B] `hunbla` |
| `hunaca.36` | Разработать новые сорта стали (эффективность рукопашной атаки мушкетера 18 века и гренадера +25%) | 15.6 | G19500 | [T] `huncen.1`, [B] `hunbla` |
| `hunaca.5` | Разработать новые снасти и сети для ловли рыбы (эффективность рыбацких лодок +100%) | 15.6 | W12400 G2520 | [B] `eurpor` |
| `hunaca.6` | Разработать новые методы древообработки (условие для постройки фрегатов) | 15.6 | W12400 G7040 | [B] `eurpor` |
| `hunaca.7` | Построить новые верфи для рыбацких лодок (стоимость рыбацкой лодки -85%) | 15.6 | W7300 G1220 | [B] `eurpor` |
| `hunaca.8` | Разработать новые инструменты для древообработки (эффективность добычи дерева +100%) | 15.6 | F5500 G550 | [B] `hunbla` |
| `hunart.cannon.1.1` | — | 10.0 | W1000 S500 G300 | [B] `hunbla` |
| `hunart.cannon.1.2` | — | 10.0 | W3000 S1000 G500 | [B] `hunbla` |
| `hunart.cannon.1.3` | — | 10.0 | W6000 S2000 G1000 | [B] `hunbla` |
| `hunart.cannon.1.4` | — | 15.6 | F1760 G350 | [B] `hunbla` |
| `hunart.cannon.1.5` | — | 15.6 | F1760 G350 | [B] `hunbla` |
| `hunart.cannon.1.6` | — | 15.6 | F1760 G350 | [B] `hunbla` |
| `hunart.cannon.2.1` | — | 10.0 | G500 I1000 | [B] `hunbla` |
| `hunart.cannon.2.2` | — | 10.0 | G1000 I2000 | [B] `hunbla` |
| `hunart.cannon.2.3` | — | 10.0 | G2000 I3000 | [B] `hunbla` |
| `hunart.cannon.2.4` | — | 15.6 | F2560 | [B] `hunbla` |
| `hunart.cannon.2.5` | — | 15.6 | F3560 | [B] `hunbla` |
| `hunart.cannon.2.6` | — | 15.6 | F5560 | [B] `hunbla` |
| `hunart.howitzer.1.1` | — | 10.0 | W1000 S500 G300 | [B] `hunbla` |
| `hunart.howitzer.1.2` | — | 10.0 | W3000 S1000 G500 | [B] `hunbla` |
| `hunart.howitzer.1.3` | — | 10.0 | W6000 S2000 G1000 | [B] `hunbla` |
| `hunart.howitzer.1.4` | — | 15.6 | F1760 G350 | [B] `hunbla` |
| `hunart.howitzer.1.5` | — | 15.6 | F1760 G350 | [B] `hunbla` |
| `hunart.howitzer.1.6` | — | 15.6 | F1760 G350 | [B] `hunbla` |
| `hunart.howitzer.2.1` | — | 10.0 | G500 I1000 | [B] `hunbla` |
| `hunart.howitzer.2.2` | — | 10.0 | G1000 I2000 | [B] `hunbla` |
| `hunart.howitzer.2.3` | — | 10.0 | G2000 I3000 | [B] `hunbla` |
| `hunart.howitzer.2.4` | — | 31.2 | F2560 | [B] `hunbla` |
| `hunart.howitzer.2.5` | — | 31.2 | F3560 | [B] `hunbla` |
| `hunart.howitzer.2.6` | — | 31.2 | F5560 | [B] `hunbla` |
| `hunbar.pikeman.1.6` | — | 15.6 | F15000 G1875 | [B] `hunbla` |
| `hunbar.pikeman.2.6` | — | 15.6 | F11250 G1500 | [B] `hunbla` |
| `hunbla.4` | Выковать штыки и тесаки для пехоты (сила удара мушкетера 18 века и гренадера +5) | 15.6 | W1300 G1500 I900 C5000 | [T] `huncen.1` |
| `huncen.1` | — | 9.4 | F30000 G5000 I2000 C2000 | [B] `hunaca`, [B] `huntem`, [B] `hunart` |

[↑ к содержанию](#содержание)

## NET — Netherlands (Нидерланды)

### `net` — здания

| sid | имя | Время (g-сек) | цена | ферма | требует |
|---|---|---:|---|---:|---|
| `eurcoa` | Шахта | 93.8 | W100 S100 | — | — |
| `eurgol` | Шахта | 93.8 | W100 S100 | — | — |
| `euriro` | Шахта | 93.8 | W100 S100 | — | — |
| `eurmar` | Рынок | 234.4 | W450 | — | [B] `eurmil`, [B] `eursto` |
| `eurmil` | Мельница | 93.8 | W30 S150 | — | — |
| `eurpor` | Порт | 1562.5 | W1600 S800 I400 | — | [B] `eurmar` |
| `eursga` | Каменные ворота | 90.0 | S50 | — | — |
| `eursto` | Склад | 31.2 | W50 S20 | — | [B] `netcen` |
| `eurswa` | Стена | 90.0 | S50 | — | [B] `eursto` |
| `eurtow` | Башня | 1230.3 | W100 S100 G150 | — | [B] `eursto` |
| `netaca` | Академия | 625.0 | W1050 S1230 | — | [B] `netbar` |
| `netart` | Артиллерийское депо | 245.9 | W100 S1000 C1400 | — | [B] `netaca` |
| `netba2` | Казарма 18в. | 5625.0 | W1700 S2950 G4000 | 250 | [T] `netcen.1` |
| `netbar` | Казарма 17в. | 93.8 | W100 S100 G500 | 150 | [B] `netbla` |
| `netbla` | Кузница | 93.8 | W100 S30 I640 | — | [B] `netcen` |
| `netcen` | Городской центр | 156.2 | W700 S700 | 100 | — |
| `netdip` | Дипломатический центр | 312.5 | W4900 S1700 | — | [B] `netaca` |
| `nethou` | Дом | 31.2 | W100 S100 | 25 | [B] `netcen` |
| `netsta` | Конюшня | 625.0 | W2500 S100 G600 | — | [B] `netbla` |
| `nettem` | Собор | 156.2 | W1000 S1200 I500 | — | [B] `netcen` |
| `ukrwga` | Деревянные ворота | 5.6 | W10 | — | — |
| `ukrwwa` | Частокол | 5.6 | W10 | — | [B] `eursto` |

### `net` — юниты

| sid | имя | Время (g-сек) | цена | тренируется в | требует |
|---|---|---:|---|---|---|
| `archerdip` | Лучник (наемник) | 1.25 | G15 | netdip | [B] `netaca`, [B] `netcen` |
| `archerturdip` | Турецкий лучник (наемник) | 1.25 | G15 | netdip | [B] `netaca`, [B] `netcen` |
| `battleship` | Линейный корабль | 390.00 | W9000 G3200 I700 C6500 | eurpor | [T] `netaca.29`, [B] `netart` |
| `cannon` | Пушка | 75.00 | W250 G400 I400 | netart | [B] `netbla` |
| `cossacksichdip` | Сечевой козак (наемник) | 2.50 | G60 | netdip | [B] `netaca`, [B] `netcen` |
| `cuirassier` | Кирасир | 22.50 | F120 G35 I25 | netsta | [B] `netbla`, [T] `netcen.1` |
| `dragoon` | Драгун 17в. | 15.00 | F90 G7 I5 | netsta | [B] `netbla` |
| `dragoon18dip` | Драгун 18в. (наемник) | 2.00 | G120 | netdip | [B] `netaca`, [B] `netcen` |
| `dragoon18net` | Драгун 18в. | 24.00 | F100 G70 I7 | netsta | [B] `netbla`, [T] `netcen.1` |
| `drummer` | Барабанщик 17в. | 5.00 | F60 G20 | netbar | [B] `netaca` |
| `drummer18` | Барабанщик 18в. | 6.00 | F50 G30 | netba2 | [B] `netaca` |
| `ferry` | Транспорт | 56.00 | W300 G50 I100 | eurpor | [B] `netart` |
| `fishboat` | Рыбацкая лодка | 40.00 | W600 | eurpor | — |
| `frigate` | Фрегат | 230.00 | W5000 G1100 I600 C800 | eurpor | [T] `netaca.6`, [B] `netart` |
| `galley` | Галера | 50.00 | W9500 G900 I800 | eurpor | [B] `netart` |
| `grenadier` | Гренадер | 6.00 | F80 G60 I40 | netba2 | [B] `netbla` |
| `grenadierdip` | Гренадер (наемник) | 1.50 | G25 | netdip | [B] `netaca`, [B] `netcen` |
| `howitzer` | Гаубица | 94.00 | W250 G350 I300 | netart | [B] `netbla` |
| `hussar` | Гусар | 15.00 | F70 G20 I2 | netsta | [B] `netbla`, [T] `netcen.1` |
| `lightcavalrydip` | Легкий кавалерист (наемник) | 2.00 | G120 | netdip | [B] `netaca`, [B] `netcen` |
| `lightinfantrydip` | Легкий пехотинец (наемник) | 1.25 | G4 | netdip | [B] `netaca`, [B] `netcen` |
| `mortar` | Мортира | 25.00 | W100 G75 I200 | netart | [B] `netbla` |
| `multicannon` | Многоствольное орудие | 50.00 | W200 G400 I250 | netart | [T] `netaca.19`, [B] `netbla` |
| `musketeer18` | Мушкетер 18в. | 4.50 | F50 G40 I40 | netba2 | [B] `netbla` |
| `musketeernet` | Мушкетер 17в. | 5.00 | F50 G8 I4 | netbar | [B] `netbla` |
| `officer` | Офицер 17в. | 10.00 | F50 G150 I30 | netbar | [B] `netaca` |
| `officer18` | Офицер 18в. | 6.00 | F50 G200 I10 | netba2 | [B] `netaca` |
| `peaeng` | Крестьянин | 12.50 | F100 | netcen | — |
| `pikeman` | Пикинер 17в. | 4.50 | F25 G3 I20 | netbar | [B] `netbla` |
| `pikeman18` | Пикинер 18в. | 1.25 | F30 G2 | netba2 | — |
| `priest` | Капеллан | 20.00 | F60 G25 | nettem | — |
| `reiter` | Рейтар | 24.00 | F120 G10 I40 | netsta | [B] `netbla` |
| `roundshierdip` | Рундашир (наемник) | 1.50 | G12 | netdip | [B] `netaca`, [B] `netcen` |
| `unitbox` | — | 3.12 | F100 | — | — |
| `yacht` | Яхта | 48.00 | W900 G450 I150 C200 | eurpor | [B] `netart` |

### `net` — ключевые апгрейды (с зависимостями)

| sid | имя | Время (g-сек) | цена | требует |
|---|---|---:|---|---|
| `eurcoa.4` | — | 9.4 | F15800 G18500 | [T] `netcen.1` |
| `eurcoa.5` | — | 9.4 | F19800 G21050 | [T] `netcen.1` |
| `eurcoa.6` | — | 9.4 | F50200 G25950 | [T] `netcen.1` |
| `eurgol.4` | — | 9.4 | F15800 G18500 | [T] `netcen.1` |
| `eurgol.5` | — | 9.4 | F19800 G21050 | [T] `netcen.1` |
| `eurgol.6` | — | 9.4 | F50200 G25950 | [T] `netcen.1` |
| `euriro.4` | — | 9.4 | F15800 G18500 | [T] `netcen.1` |
| `euriro.5` | — | 9.4 | F19800 G21050 | [T] `netcen.1` |
| `euriro.6` | — | 9.4 | F50200 G25950 | [T] `netcen.1` |
| `eurpor.1` | — | 46.9 | W20000 G1500 | [B] `netart` |
| `eurtow.1` | — | 31.2 | G250 | [B] `netart` |
| `eurtow.2` | — | 31.2 | I350 | [B] `netart` |
| `eurtow.3` | — | 31.2 | C400 | [B] `netart` |
| `eurtow.4` | — | 31.2 | I450 | [B] `netart` |
| `eurtow.5` | — | 31.2 | C500 | [B] `netart` |
| `ferry.1` | Усовершенствовать конструкцию транспортного судна (+%value% посадочных мест) | 15.6 | F1000 G1250 | [T] `netcen.1` |
| `netaca.12` | Улучшить стрелковое оружие: нарезной ствол (сила выстрела +10%) | 15.6 | I5000 | [B] `netbla` |
| `netaca.13` | Исследовать гранулированный порох (сила выстрела +10%) | 15.6 | G4000 | [B] `netbla` |
| `netaca.14` | Исследовать новые методы очистки серы (сила выстрела +15%) | 15.6 | G7000 | [B] `netbla` |
| `netaca.15` | Исследовать новые методы очистки селитры (сила выстрела +25%) | 15.6 | C11000 | [B] `netbla` |
| `netaca.16` | Исследовать новые добавки в порох (дальность стрельбы артиллерии +5%) | 15.6 | G2000 I12150 | [B] `netart` |
| `netaca.17` | Разработать новые виды стволов: единорог, карронада (дальность стрельбы артиллерии +10%) | 15.6 | S3000 G4550 I19200 | [B] `netart` |
| `netaca.18` | Разработать более прочный лафет для орудий: система Грибоваля (прочность пушек +50%) | 15.6 | G500 I3830 C1500 | [B] `netart` |
| `netaca.19` | Разработать многоствольное орудие | 15.6 | G1500 C2500 | [B] `netart` |
| `netaca.20` | Разработать новые прицельные системы для пушек (меткость стрельбы артиллерии +35%) | 15.6 | W3540 G2000 C7250 | [B] `netart` |
| `netaca.21` | Выделить деньги на ремонтные мастерские для пушек (отремонтировать все пушки) | 15.6 | W350 G100 C250 | [B] `netart` |
| `netaca.25` | Разработать монгольфьер (открывает всю карту) | 15.6 | G5750 | [T] `netcen.1` |
| `netaca.27` | Развивать математику (меткость выстрела орудий +35%) | 15.6 | W9540 G12000 C65200 | [B] `netart` |
| `netaca.28` | Разработать новые парусные системы (скорость кораблей +40%) | 15.6 | W65400 G24050 | [B] `eurpor` |
| `netaca.29` | Разработать новую систему шпангоутов и корпуса корабля (условие для постройки линейных кораблей) | 15.6 | W32300 G6800 I9000 C12800 | [B] `eurpor` |
| `netaca.30` | Обучить плотников (скорость постройки кораблей увеличивается в 10 раз) | 15.6 | W2300 S42700 G1150 | [B] `eurpor` |
| `netaca.32` | Разработать кремниевый замок к ружьям (цена мушкета -50%) | 15.6 | G6050 C7750 | [T] `netcen.1` |
| `netaca.34` | Разработать новые сорта стали для кирас (защита солдат в доспехах +2) | 15.6 | G9750 | [B] `netbla` |
| `netaca.35` | Разработать штык: вставляемый в ствол багинет, штык с трубкой (сила удара холодного оружия +5) | 15.6 | G11500 | [T] `netcen.1`, [B] `netbla` |
| `netaca.36` | Разработать новые сорта стали (эффективность рукопашной атаки мушкетера 18 века и гренадера +25%) | 15.6 | G19500 | [T] `netcen.1`, [B] `netbla` |
| `netaca.5` | Разработать новые снасти и сети для ловли рыбы (эффективность рыбацких лодок +100%) | 15.6 | W12400 G2520 | [B] `eurpor` |
| `netaca.6` | Разработать новые методы древообработки (условие для постройки фрегатов) | 15.6 | W12400 G7040 | [B] `eurpor` |
| `netaca.7` | Построить новые верфи для рыбацких лодок (стоимость рыбацкой лодки -85%) | 15.6 | W7300 G1220 | [B] `eurpor` |
| `netaca.8` | Разработать новые инструменты для древообработки (эффективность добычи дерева +100%) | 15.6 | F5500 G550 | [B] `netbla` |
| `netart.cannon.1.1` | — | 10.0 | W1000 S500 G300 | [B] `netbla` |
| `netart.cannon.1.2` | — | 10.0 | W3000 S1000 G500 | [B] `netbla` |
| `netart.cannon.1.3` | — | 10.0 | W6000 S2000 G1000 | [B] `netbla` |
| `netart.cannon.1.4` | — | 15.6 | F1760 G350 | [B] `netbla` |
| `netart.cannon.1.5` | — | 15.6 | F1760 G350 | [B] `netbla` |
| `netart.cannon.1.6` | — | 15.6 | F1760 G350 | [B] `netbla` |
| `netart.cannon.2.1` | — | 10.0 | G500 I1000 | [B] `netbla` |
| `netart.cannon.2.2` | — | 10.0 | G1000 I2000 | [B] `netbla` |
| `netart.cannon.2.3` | — | 10.0 | G2000 I3000 | [B] `netbla` |
| `netart.cannon.2.4` | — | 15.6 | F2560 | [B] `netbla` |
| `netart.cannon.2.5` | — | 15.6 | F3560 | [B] `netbla` |
| `netart.cannon.2.6` | — | 15.6 | F5560 | [B] `netbla` |
| `netart.howitzer.1.1` | — | 10.0 | W1000 S500 G300 | [B] `netbla` |
| `netart.howitzer.1.2` | — | 10.0 | W3000 S1000 G500 | [B] `netbla` |
| `netart.howitzer.1.3` | — | 10.0 | W6000 S2000 G1000 | [B] `netbla` |
| `netart.howitzer.1.4` | — | 15.6 | F1760 G350 | [B] `netbla` |
| `netart.howitzer.1.5` | — | 15.6 | F1760 G350 | [B] `netbla` |
| `netart.howitzer.1.6` | — | 15.6 | F1760 G350 | [B] `netbla` |
| `netart.howitzer.2.1` | — | 10.0 | G500 I1000 | [B] `netbla` |
| `netart.howitzer.2.2` | — | 10.0 | G1000 I2000 | [B] `netbla` |
| `netart.howitzer.2.3` | — | 10.0 | G2000 I3000 | [B] `netbla` |
| `netart.howitzer.2.4` | — | 31.2 | F2560 | [B] `netbla` |
| `netart.howitzer.2.5` | — | 31.2 | F3560 | [B] `netbla` |
| `netart.howitzer.2.6` | — | 31.2 | F5560 | [B] `netbla` |
| `netbar.pikeman.1.6` | — | 15.6 | F15000 G1875 | [B] `netbla` |
| `netbar.pikeman.2.6` | — | 15.6 | F11250 G1500 | [B] `netbla` |
| `netbla.4` | Выковать штыки и тесаки для пехоты (сила удара мушкетера 18 века и гренадера +5) | 15.6 | W1300 G1500 I900 C5000 | [T] `netcen.1` |
| `netcen.1` | — | 9.4 | F33000 G4800 I1800 C1800 | [B] `netaca`, [B] `nettem`, [B] `netart` |

[↑ к содержанию](#содержание)

## PIE — Piedmont (Пьемонт)

### `pie` — здания

| sid | имя | Время (g-сек) | цена | ферма | требует |
|---|---|---:|---|---:|---|
| `eurcoa` | Шахта | 93.8 | W100 S100 | — | — |
| `eurgol` | Шахта | 93.8 | W100 S100 | — | — |
| `euriro` | Шахта | 93.8 | W100 S100 | — | — |
| `eurmar` | Рынок | 234.4 | W450 | — | [B] `eurmil`, [B] `eursto` |
| `eurmil` | Мельница | 93.8 | W30 S150 | — | — |
| `eurpor` | Порт | 1562.5 | W1600 S800 I400 | — | [B] `eurmar` |
| `eursga` | Каменные ворота | 90.0 | S50 | — | — |
| `eursto` | Склад | 31.2 | W50 S20 | — | [B] `piecen` |
| `eurswa` | Стена | 90.0 | S50 | — | [B] `eursto` |
| `eurtow` | Башня | 1230.3 | W100 S100 G150 | — | [B] `eursto` |
| `pieaca` | Академия | 625.0 | W1250 S1100 | — | [B] `piebar` |
| `pieart` | Артиллерийское депо | 245.9 | W100 S1000 C1400 | — | [B] `pieaca` |
| `pieba2` | Казарма 18в. | 5625.0 | W1700 S2950 G4000 | 250 | [T] `piecen.1` |
| `piebar` | Казарма 17в. | 93.8 | W100 S100 G500 | 150 | [B] `piebla` |
| `piebla` | Кузница | 93.8 | W100 S30 I640 | — | [B] `piecen` |
| `piecen` | Городской центр | 156.2 | W700 S700 | 100 | — |
| `piedip` | Дипломатический центр | 312.5 | W4900 S1700 | — | [B] `pieaca` |
| `piehou` | Дом | 31.2 | W100 S100 | 25 | [B] `piecen` |
| `piesta` | Конюшня | 625.0 | W2500 S100 G600 | — | [B] `piebla` |
| `pietem` | Собор | 156.2 | W1000 S1200 I500 | — | [B] `piecen` |
| `ukrwga` | Деревянные ворота | 5.6 | W10 | — | — |
| `ukrwwa` | Частокол | 5.6 | W10 | — | [B] `eursto` |

### `pie` — юниты

| sid | имя | Время (g-сек) | цена | тренируется в | требует |
|---|---|---:|---|---|---|
| `archerdip` | Лучник (наемник) | 1.25 | G15 | piedip | [B] `pieaca`, [B] `piecen` |
| `archerturdip` | Турецкий лучник (наемник) | 1.25 | G15 | piedip | [B] `pieaca`, [B] `piecen` |
| `battleship` | Линейный корабль | 390.00 | W9000 G3200 I700 C6500 | eurpor | [T] `pieaca.29`, [B] `pieart` |
| `cannon` | Пушка | 75.00 | W250 G400 I400 | pieart | [B] `piebla` |
| `cossacksichdip` | Сечевой козак (наемник) | 2.50 | G60 | piedip | [B] `pieaca`, [B] `piecen` |
| `cuirassier` | Кирасир | 22.50 | F120 G35 I25 | piesta | [B] `piebla`, [T] `piecen.1` |
| `dragoon` | Драгун 17в. | 15.00 | F90 G7 I5 | piesta | [B] `piebla` |
| `dragoon18dip` | Драгун 18в. (наемник) | 2.00 | G120 | piedip | [B] `pieaca`, [B] `piecen` |
| `dragoon18pie` | Драгун 18в. | 20.25 | F60 G65 I7 | piesta | [B] `piebla`, [T] `piecen.1` |
| `drummer` | Барабанщик 17в. | 5.00 | F60 G20 | piebar | [B] `pieaca` |
| `drummer18` | Барабанщик 18в. | 6.00 | F50 G30 | pieba2 | [B] `pieaca` |
| `ferry` | Транспорт | 56.00 | W300 G50 I100 | eurpor | [B] `pieart` |
| `fishboat` | Рыбацкая лодка | 40.00 | W600 | eurpor | — |
| `frigate` | Фрегат | 230.00 | W5000 G1100 I600 C800 | eurpor | [T] `pieaca.6`, [B] `pieart` |
| `galley` | Галера | 50.00 | W9500 G900 I800 | eurpor | [B] `pieart` |
| `grenadier` | Гренадер | 6.00 | F80 G60 I40 | pieba2 | [B] `piebla` |
| `grenadierdip` | Гренадер (наемник) | 1.50 | G25 | piedip | [B] `pieaca`, [B] `piecen` |
| `howitzer` | Гаубица | 94.00 | W250 G350 I300 | pieart | [B] `piebla` |
| `hussar` | Гусар | 15.00 | F70 G20 I2 | piesta | [B] `piebla`, [T] `piecen.1` |
| `lightcavalrydip` | Легкий кавалерист (наемник) | 2.00 | G120 | piedip | [B] `pieaca`, [B] `piecen` |
| `lightinfantrydip` | Легкий пехотинец (наемник) | 1.25 | G4 | piedip | [B] `pieaca`, [B] `piecen` |
| `mortar` | Мортира | 25.00 | W100 G75 I200 | pieart | [B] `piebla` |
| `multicannon` | Многоствольное орудие | 50.00 | W200 G400 I250 | pieart | [T] `pieaca.19`, [B] `piebla` |
| `musketeer` | Мушкетер 17в. | 6.00 | F45 G6 I5 | piebar | [B] `piebla` |
| `musketeer18` | Мушкетер 18в. | 4.50 | F50 G40 I40 | pieba2 | [B] `piebla` |
| `officer` | Офицер 17в. | 10.00 | F50 G150 I30 | piebar | [B] `pieaca` |
| `officer18` | Офицер 18в. | 6.00 | F50 G200 I10 | pieba2 | [B] `pieaca` |
| `padre` | Падре | 25.00 | F50 G40 | pietem | — |
| `peaspa` | Крестьянин | 12.50 | F100 | piecen | — |
| `pikeman` | Пикинер 17в. | 4.50 | F25 G3 I20 | piebar | [B] `piebla` |
| `pikeman18` | Пикинер 18в. | 1.25 | F30 G2 | pieba2 | — |
| `reiter` | Рейтар | 24.00 | F120 G10 I40 | piesta | [B] `piebla` |
| `roundshierdip` | Рундашир (наемник) | 1.50 | G12 | piedip | [B] `pieaca`, [B] `piecen` |
| `unitbox` | — | 3.12 | F100 | — | — |
| `yacht` | Яхта | 48.00 | W900 G450 I150 C200 | eurpor | [B] `pieart` |

### `pie` — ключевые апгрейды (с зависимостями)

| sid | имя | Время (g-сек) | цена | требует |
|---|---|---:|---|---|
| `eurcoa.4` | — | 9.4 | F15800 G18500 | [T] `piecen.1` |
| `eurcoa.5` | — | 9.4 | F19800 G21050 | [T] `piecen.1` |
| `eurcoa.6` | — | 9.4 | F50200 G25950 | [T] `piecen.1` |
| `eurgol.4` | — | 9.4 | F15800 G18500 | [T] `piecen.1` |
| `eurgol.5` | — | 9.4 | F19800 G21050 | [T] `piecen.1` |
| `eurgol.6` | — | 9.4 | F50200 G25950 | [T] `piecen.1` |
| `euriro.4` | — | 9.4 | F15800 G18500 | [T] `piecen.1` |
| `euriro.5` | — | 9.4 | F19800 G21050 | [T] `piecen.1` |
| `euriro.6` | — | 9.4 | F50200 G25950 | [T] `piecen.1` |
| `eurpor.1` | — | 46.9 | W20000 G1500 | [B] `pieart` |
| `eurtow.1` | — | 31.2 | G250 | [B] `pieart` |
| `eurtow.2` | — | 31.2 | I350 | [B] `pieart` |
| `eurtow.3` | — | 31.2 | C400 | [B] `pieart` |
| `eurtow.4` | — | 31.2 | I450 | [B] `pieart` |
| `eurtow.5` | — | 31.2 | C500 | [B] `pieart` |
| `ferry.1` | Усовершенствовать конструкцию транспортного судна (+%value% посадочных мест) | 15.6 | F1000 G1250 | [T] `piecen.1` |
| `pieaca.12` | Улучшить стрелковое оружие: нарезной ствол (сила выстрела +10%) | 15.6 | I5000 | [B] `piebla` |
| `pieaca.13` | Исследовать гранулированный порох (сила выстрела +10%) | 15.6 | G4000 | [B] `piebla` |
| `pieaca.14` | Исследовать новые методы очистки серы (сила выстрела +15%) | 15.6 | G7000 | [B] `piebla` |
| `pieaca.15` | Исследовать новые методы очистки селитры (сила выстрела +25%) | 15.6 | C11000 | [B] `piebla` |
| `pieaca.16` | Исследовать новые добавки в порох (дальность стрельбы артиллерии +5%) | 15.6 | G2000 I12150 | [B] `pieart` |
| `pieaca.17` | Разработать новые виды стволов: единорог, карронада (дальность стрельбы артиллерии +10%) | 15.6 | S3000 G4550 I19200 | [B] `pieart` |
| `pieaca.18` | Разработать более прочный лафет для орудий: система Грибоваля (прочность пушек +50%) | 15.6 | G500 I3830 C1500 | [B] `pieart` |
| `pieaca.19` | Разработать многоствольное орудие | 15.6 | G1500 C2500 | [B] `pieart` |
| `pieaca.20` | Разработать новые прицельные системы для пушек (меткость стрельбы артиллерии +35%) | 15.6 | W3540 G2000 C7250 | [B] `pieart` |
| `pieaca.21` | Выделить деньги на ремонтные мастерские для пушек (отремонтировать все пушки) | 15.6 | W350 G100 C250 | [B] `pieart` |
| `pieaca.25` | Разработать монгольфьер (открывает всю карту) | 15.6 | G5750 | [T] `piecen.1` |
| `pieaca.27` | Развивать математику (меткость выстрела орудий +35%) | 15.6 | W9540 G12000 C65200 | [B] `pieart` |
| `pieaca.28` | Разработать новые парусные системы (скорость кораблей +40%) | 15.6 | W65400 G24050 | [B] `eurpor` |
| `pieaca.29` | Разработать новую систему шпангоутов и корпуса корабля (условие для постройки линейных кораблей) | 15.6 | W32300 G6800 I9000 C12800 | [B] `eurpor` |
| `pieaca.30` | Обучить плотников (скорость постройки кораблей увеличивается в 10 раз) | 15.6 | W2300 S42700 G1150 | [B] `eurpor` |
| `pieaca.32` | Разработать кремниевый замок к ружьям (цена мушкета -50%) | 15.6 | G6050 C7750 | [T] `piecen.1` |
| `pieaca.34` | Разработать новые сорта стали для кирас (защита солдат в доспехах +2) | 15.6 | G9750 | [B] `piebla` |
| `pieaca.35` | Разработать штык: вставляемый в ствол багинет, штык с трубкой (сила удара холодного оружия +5) | 15.6 | G11500 | [T] `piecen.1`, [B] `piebla` |
| `pieaca.36` | Разработать новые сорта стали (эффективность рукопашной атаки мушкетера 18 века и гренадера +25%) | 15.6 | G19500 | [T] `piecen.1`, [B] `piebla` |
| `pieaca.5` | Разработать новые снасти и сети для ловли рыбы (эффективность рыбацких лодок +100%) | 15.6 | W12400 G2520 | [B] `eurpor` |
| `pieaca.6` | Разработать новые методы древообработки (условие для постройки фрегатов) | 15.6 | W12400 G7040 | [B] `eurpor` |
| `pieaca.7` | Построить новые верфи для рыбацких лодок (стоимость рыбацкой лодки -85%) | 15.6 | W7300 G1220 | [B] `eurpor` |
| `pieaca.8` | Разработать новые инструменты для древообработки (эффективность добычи дерева +100%) | 15.6 | F5500 G550 | [B] `piebla` |
| `pieart.cannon.1.1` | — | 10.0 | W1000 S500 G300 | [B] `piebla` |
| `pieart.cannon.1.2` | — | 10.0 | W3000 S1000 G500 | [B] `piebla` |
| `pieart.cannon.1.3` | — | 10.0 | W6000 S2000 G1000 | [B] `piebla` |
| `pieart.cannon.1.4` | — | 15.6 | F1760 G350 | [B] `piebla` |
| `pieart.cannon.1.5` | — | 15.6 | F1760 G350 | [B] `piebla` |
| `pieart.cannon.1.6` | — | 15.6 | F1760 G350 | [B] `piebla` |
| `pieart.cannon.2.1` | — | 10.0 | G500 I1000 | [B] `piebla` |
| `pieart.cannon.2.2` | — | 10.0 | G1000 I2000 | [B] `piebla` |
| `pieart.cannon.2.3` | — | 10.0 | G2000 I3000 | [B] `piebla` |
| `pieart.cannon.2.4` | — | 15.6 | F2560 | [B] `piebla` |
| `pieart.cannon.2.5` | — | 15.6 | F3560 | [B] `piebla` |
| `pieart.cannon.2.6` | — | 15.6 | F5560 | [B] `piebla` |
| `pieart.howitzer.1.1` | — | 10.0 | W1000 S500 G300 | [B] `piebla` |
| `pieart.howitzer.1.2` | — | 10.0 | W3000 S1000 G500 | [B] `piebla` |
| `pieart.howitzer.1.3` | — | 10.0 | W6000 S2000 G1000 | [B] `piebla` |
| `pieart.howitzer.1.4` | — | 15.6 | F1760 G350 | [B] `piebla` |
| `pieart.howitzer.1.5` | — | 15.6 | F1760 G350 | [B] `piebla` |
| `pieart.howitzer.1.6` | — | 15.6 | F1760 G350 | [B] `piebla` |
| `pieart.howitzer.2.1` | — | 10.0 | G500 I1000 | [B] `piebla` |
| `pieart.howitzer.2.2` | — | 10.0 | G1000 I2000 | [B] `piebla` |
| `pieart.howitzer.2.3` | — | 10.0 | G2000 I3000 | [B] `piebla` |
| `pieart.howitzer.2.4` | — | 31.2 | F2560 | [B] `piebla` |
| `pieart.howitzer.2.5` | — | 31.2 | F3560 | [B] `piebla` |
| `pieart.howitzer.2.6` | — | 31.2 | F5560 | [B] `piebla` |
| `piebar.pikeman.1.6` | — | 15.6 | F15000 G1875 | [B] `piebla` |
| `piebar.pikeman.2.6` | — | 15.6 | F11250 G1500 | [B] `piebla` |
| `piebla.4` | Выковать штыки и тесаки для пехоты (сила удара мушкетера 18 века и гренадера +5) | 15.6 | W1300 G1500 I900 C5000 | [T] `piecen.1` |
| `piecen.1` | — | 9.4 | F30000 G5000 I2000 C2000 | [B] `pieaca`, [B] `pietem`, [B] `pieart` |

[↑ к содержанию](#содержание)

## POL — Poland (Польша)

### `pol` — здания

| sid | имя | Время (g-сек) | цена | ферма | требует |
|---|---|---:|---|---:|---|
| `eurcoa` | Шахта | 93.8 | W100 S100 | — | — |
| `eurgol` | Шахта | 93.8 | W100 S100 | — | — |
| `euriro` | Шахта | 93.8 | W100 S100 | — | — |
| `eurmar` | Рынок | 234.4 | W450 | — | [B] `eurmil`, [B] `russto` |
| `eurmil` | Мельница | 93.8 | W30 S150 | — | — |
| `eurpor` | Порт | 1562.5 | W1600 S800 I400 | — | [B] `eurmar` |
| `eursga` | Каменные ворота | 90.0 | S50 | — | — |
| `eurswa` | Стена | 90.0 | S50 | — | [B] `russto` |
| `eurtow` | Башня | 1230.3 | W100 S100 G150 | — | [B] `russto` |
| `polaca` | Академия | 625.0 | W950 S800 | — | [B] `polbar` |
| `polart` | Артиллерийское депо | 245.9 | W100 S1000 C1400 | — | [B] `polaca` |
| `polba2` | Казарма 18в. | 5625.0 | W1700 S2950 G4000 | 250 | [T] `polcen.1` |
| `polbar` | Казарма 17в. | 93.8 | W100 S100 G500 | 150 | [B] `polbla` |
| `polbla` | Кузница | 93.8 | W100 S30 I640 | — | [B] `polcen` |
| `polcen` | Городской центр | 156.2 | W700 S700 | 100 | — |
| `poldip` | Дипломатический центр | 312.5 | W4900 S1700 | — | [B] `polaca` |
| `polhou` | Дом | 31.2 | W100 S100 | 25 | [B] `polcen` |
| `polsta` | Конюшня | 625.0 | W2500 S100 G600 | — | [B] `polbla` |
| `poltem` | Собор | 156.2 | W1000 S1200 I500 | — | [B] `polcen` |
| `russto` | Склад | 31.2 | W50 S20 | — | [B] `polcen` |
| `ukrwga` | Деревянные ворота | 5.6 | W10 | — | — |
| `ukrwwa` | Частокол | 5.6 | W10 | — | [B] `russto` |

### `pol` — юниты

| sid | имя | Время (g-сек) | цена | тренируется в | требует |
|---|---|---:|---|---|---|
| `archerdip` | Лучник (наемник) | 1.25 | G15 | poldip | [B] `polaca`, [B] `polcen` |
| `archerturdip` | Турецкий лучник (наемник) | 1.25 | G15 | poldip | [B] `polaca`, [B] `polcen` |
| `battleship` | Линейный корабль | 390.00 | W9000 G3200 I700 C6500 | eurpor | [T] `polaca.29`, [B] `polart` |
| `cannon` | Пушка | 75.00 | W250 G400 I400 | polart | [B] `polbla` |
| `cossacksichdip` | Сечевой козак (наемник) | 2.50 | G60 | poldip | [B] `polaca`, [B] `polcen` |
| `cuirassier` | Кирасир | 22.50 | F120 G35 I25 | polsta | [B] `polbla`, [T] `polcen.1` |
| `dragoon` | Драгун 17в. | 15.00 | F90 G7 I5 | polsta | [B] `polbla` |
| `dragoon18` | Драгун 18в. | 22.50 | F70 G60 I7 | polsta | [B] `polbla`, [T] `polcen.1` |
| `dragoon18dip` | Драгун 18в. (наемник) | 2.00 | G120 | poldip | [B] `polaca`, [B] `polcen` |
| `dragoonpol` | Посполитое рушение | 13.50 | F70 G5 I4 | polsta | [B] `polbla` |
| `drummer` | Барабанщик 17в. | 5.00 | F60 G20 | polbar | [B] `polaca` |
| `drummer18` | Барабанщик 18в. | 6.00 | F50 G30 | polba2 | [B] `polaca` |
| `ferry` | Транспорт | 56.00 | W300 G50 I100 | eurpor | [B] `polart` |
| `fishboat` | Рыбацкая лодка | 40.00 | W600 | eurpor | — |
| `frigate` | Фрегат | 230.00 | W5000 G1100 I600 C800 | eurpor | [T] `polaca.6`, [B] `polart` |
| `galley` | Галера | 50.00 | W9500 G900 I800 | eurpor | [B] `polart` |
| `grenadier` | Гренадер | 6.00 | F80 G60 I40 | polba2 | [B] `polbla` |
| `grenadierdip` | Гренадер (наемник) | 1.50 | G25 | poldip | [B] `polaca`, [B] `polcen` |
| `howitzer` | Гаубица | 94.00 | W250 G350 I300 | polart | [B] `polbla` |
| `hussar` | Гусар | 15.00 | F70 G20 I2 | polsta | [B] `polbla`, [T] `polcen.1` |
| `lightcavalrydip` | Легкий кавалерист (наемник) | 2.00 | G120 | poldip | [B] `polaca`, [B] `polcen` |
| `lightinfantrydip` | Легкий пехотинец (наемник) | 1.25 | G4 | poldip | [B] `polaca`, [B] `polcen` |
| `mortar` | Мортира | 25.00 | W100 G75 I200 | polart | [B] `polbla` |
| `multicannon` | Многоствольное орудие | 50.00 | W200 G400 I250 | polart | [T] `polaca.19`, [B] `polbla` |
| `musketeer18` | Мушкетер 18в. | 4.50 | F50 G40 I40 | polba2 | [B] `polbla` |
| `musketeerpol` | Мушкетер 17в. | 4.50 | F40 G3 I3 | polbar | [B] `polbla` |
| `officer` | Офицер 17в. | 10.00 | F50 G150 I30 | polbar | [B] `polaca` |
| `officer18` | Офицер 18в. | 6.00 | F50 G200 I10 | polba2 | [B] `polaca` |
| `peapol` | Крестьянин | 12.50 | F100 | polcen | — |
| `pikeman18` | Пикинер 18в. | 1.25 | F30 G2 | polba2 | — |
| `pikemanpol` | Пикинер 17в. | 3.00 | F25 G1 | polbar | [B] `polbla` |
| `priest` | Капеллан | 20.00 | F60 G25 | poltem | — |
| `reiterpol` | Легкий рейтар | 8.25 | F60 G5 I2 | polsta | [B] `polbla` |
| `roundshierdip` | Рундашир (наемник) | 1.50 | G12 | poldip | [B] `polaca`, [B] `polcen` |
| `unitbox` | — | 3.12 | F100 | — | — |
| `wingedhussar` | Крылатый гусар | 26.00 | F130 G30 I25 | polsta | [B] `polbla` |
| `yacht` | Яхта | 48.00 | W900 G450 I150 C200 | eurpor | [B] `polart` |

### `pol` — ключевые апгрейды (с зависимостями)

| sid | имя | Время (g-сек) | цена | требует |
|---|---|---:|---|---|
| `eurcoa.4` | — | 9.4 | F15800 G18500 | [T] `polcen.1` |
| `eurcoa.5` | — | 9.4 | F19800 G21050 | [T] `polcen.1` |
| `eurcoa.6` | — | 9.4 | F50200 G25950 | [T] `polcen.1` |
| `eurgol.4` | — | 9.4 | F15800 G18500 | [T] `polcen.1` |
| `eurgol.5` | — | 9.4 | F19800 G21050 | [T] `polcen.1` |
| `eurgol.6` | — | 9.4 | F50200 G25950 | [T] `polcen.1` |
| `euriro.4` | — | 9.4 | F15800 G18500 | [T] `polcen.1` |
| `euriro.5` | — | 9.4 | F19800 G21050 | [T] `polcen.1` |
| `euriro.6` | — | 9.4 | F50200 G25950 | [T] `polcen.1` |
| `eurpor.1` | — | 46.9 | W20000 G1500 | [B] `polart` |
| `eurtow.1` | — | 31.2 | G250 | [B] `polart` |
| `eurtow.2` | — | 31.2 | I350 | [B] `polart` |
| `eurtow.3` | — | 31.2 | C400 | [B] `polart` |
| `eurtow.4` | — | 31.2 | I450 | [B] `polart` |
| `eurtow.5` | — | 31.2 | C500 | [B] `polart` |
| `ferry.1` | Усовершенствовать конструкцию транспортного судна (+%value% посадочных мест) | 15.6 | F1000 G1250 | [T] `polcen.1` |
| `polaca.12` | Улучшить стрелковое оружие: нарезной ствол (сила выстрела +10%) | 15.6 | I5000 | [B] `polbla` |
| `polaca.13` | Исследовать гранулированный порох (сила выстрела +10%) | 15.6 | G4000 | [B] `polbla` |
| `polaca.14` | Исследовать новые методы очистки серы (сила выстрела +15%) | 15.6 | G7000 | [B] `polbla` |
| `polaca.15` | Исследовать новые методы очистки селитры (сила выстрела +25%) | 15.6 | C11000 | [B] `polbla` |
| `polaca.16` | Исследовать новые добавки в порох (дальность стрельбы артиллерии +5%) | 15.6 | G2000 I12150 | [B] `polart` |
| `polaca.17` | Разработать новые виды стволов: единорог, карронада (дальность стрельбы артиллерии +10%) | 15.6 | S3000 G4550 I19200 | [B] `polart` |
| `polaca.18` | Разработать более прочный лафет для орудий: система Грибоваля (прочность пушек +50%) | 15.6 | G500 I3830 C1500 | [B] `polart` |
| `polaca.19` | Разработать многоствольное орудие | 15.6 | G1500 C2500 | [B] `polart` |
| `polaca.20` | Разработать новые прицельные системы для пушек (меткость стрельбы артиллерии +35%) | 15.6 | W3540 G2000 C7250 | [B] `polart` |
| `polaca.21` | Выделить деньги на ремонтные мастерские для пушек (отремонтировать все пушки) | 15.6 | W350 G100 C250 | [B] `polart` |
| `polaca.25` | Разработать монгольфьер (открывает всю карту) | 15.6 | G5750 | [T] `polcen.1` |
| `polaca.27` | Развивать математику (меткость выстрела орудий +35%) | 15.6 | W9540 G12000 C65200 | [B] `polart` |
| `polaca.28` | Разработать новые парусные системы (скорость кораблей +40%) | 15.6 | W65400 G24050 | [B] `eurpor` |
| `polaca.29` | Разработать новую систему шпангоутов и корпуса корабля (условие для постройки линейных кораблей) | 15.6 | W32300 G6800 I9000 C12800 | [B] `eurpor` |
| `polaca.30` | Обучить плотников (скорость постройки кораблей увеличивается в 10 раз) | 15.6 | W2300 S42700 G1150 | [B] `eurpor` |
| `polaca.32` | Разработать кремниевый замок к ружьям (цена мушкета -50%) | 15.6 | G6050 C7750 | [T] `polcen.1` |
| `polaca.34` | Разработать новые сорта стали для кирас (защита солдат в доспехах +2) | 15.6 | G9750 | [B] `polbla` |
| `polaca.35` | Разработать штык: вставляемый в ствол багинет, штык с трубкой (сила удара холодного оружия +5) | 15.6 | G11500 | [T] `polcen.1`, [B] `polbla` |
| `polaca.36` | Разработать новые сорта стали (эффективность рукопашной атаки мушкетера 18 века и гренадера +25%) | 15.6 | G19500 | [T] `polcen.1`, [B] `polbla` |
| `polaca.5` | Разработать новые снасти и сети для ловли рыбы (эффективность рыбацких лодок +100%) | 15.6 | W12400 G2520 | [B] `eurpor` |
| `polaca.6` | Разработать новые методы древообработки (условие для постройки фрегатов) | 15.6 | W12400 G7040 | [B] `eurpor` |
| `polaca.7` | Построить новые верфи для рыбацких лодок (стоимость рыбацкой лодки -85%) | 15.6 | W7300 G1220 | [B] `eurpor` |
| `polaca.8` | Разработать новые инструменты для древообработки (эффективность добычи дерева +100%) | 15.6 | F5500 G550 | [B] `polbla` |
| `polart.cannon.1.1` | — | 10.0 | W1000 S500 G300 | [B] `polbla` |
| `polart.cannon.1.2` | — | 10.0 | W3000 S1000 G500 | [B] `polbla` |
| `polart.cannon.1.3` | — | 10.0 | W6000 S2000 G1000 | [B] `polbla` |
| `polart.cannon.1.4` | — | 15.6 | F1760 G350 | [B] `polbla` |
| `polart.cannon.1.5` | — | 15.6 | F1760 G350 | [B] `polbla` |
| `polart.cannon.1.6` | — | 15.6 | F1760 G350 | [B] `polbla` |
| `polart.cannon.2.1` | — | 10.0 | G500 I1000 | [B] `polbla` |
| `polart.cannon.2.2` | — | 10.0 | G1000 I2000 | [B] `polbla` |
| `polart.cannon.2.3` | — | 10.0 | G2000 I3000 | [B] `polbla` |
| `polart.cannon.2.4` | — | 15.6 | F2560 | [B] `polbla` |
| `polart.cannon.2.5` | — | 15.6 | F3560 | [B] `polbla` |
| `polart.cannon.2.6` | — | 15.6 | F5560 | [B] `polbla` |
| `polart.howitzer.1.1` | — | 10.0 | W1000 S500 G300 | [B] `polbla` |
| `polart.howitzer.1.2` | — | 10.0 | W3000 S1000 G500 | [B] `polbla` |
| `polart.howitzer.1.3` | — | 10.0 | W6000 S2000 G1000 | [B] `polbla` |
| `polart.howitzer.1.4` | — | 15.6 | F1760 G350 | [B] `polbla` |
| `polart.howitzer.1.5` | — | 15.6 | F1760 G350 | [B] `polbla` |
| `polart.howitzer.1.6` | — | 15.6 | F1760 G350 | [B] `polbla` |
| `polart.howitzer.2.1` | — | 10.0 | G500 I1000 | [B] `polbla` |
| `polart.howitzer.2.2` | — | 10.0 | G1000 I2000 | [B] `polbla` |
| `polart.howitzer.2.3` | — | 10.0 | G2000 I3000 | [B] `polbla` |
| `polart.howitzer.2.4` | — | 31.2 | F2560 | [B] `polbla` |
| `polart.howitzer.2.5` | — | 31.2 | F3560 | [B] `polbla` |
| `polart.howitzer.2.6` | — | 31.2 | F5560 | [B] `polbla` |
| `polbar.pikemanpol.1.6` | — | 15.6 | F22500 G2800 | [B] `polbla` |
| `polbar.pikemanpol.2.6` | — | 15.6 | F15000 G1000 | [B] `polbla` |
| `polbla.4` | Выковать штыки и тесаки для пехоты (сила удара мушкетера 18 века и гренадера +5) | 15.6 | W1300 G1500 I900 C5000 | [T] `polcen.1` |
| `polcen.1` | — | 9.4 | F30000 G4800 I2200 C2200 | [B] `polaca`, [B] `poltem`, [B] `polart` |

[↑ к содержанию](#содержание)

## POR — Portugal (Португалия)

### `por` — здания

| sid | имя | Время (g-сек) | цена | ферма | требует |
|---|---|---:|---|---:|---|
| `eurcoa` | Шахта | 93.8 | W100 S100 | — | — |
| `eurgol` | Шахта | 93.8 | W100 S100 | — | — |
| `euriro` | Шахта | 93.8 | W100 S100 | — | — |
| `eurmil` | Мельница | 93.8 | W30 S150 | — | — |
| `eursga` | Каменные ворота | 90.0 | S50 | — | — |
| `eurswa` | Стена | 90.0 | S50 | — | [B] `spasto` |
| `eurtow` | Башня | 1230.3 | W100 S100 G150 | — | [B] `spasto` |
| `poraca` | Академия | 625.0 | W1250 S1100 | — | [B] `porbar` |
| `porart` | Артиллерийское депо | 245.9 | W100 S1000 C1400 | — | [B] `poraca` |
| `porba2` | Казарма 18в. | 5625.0 | W1700 S2950 G4000 | 250 | [T] `porcen.1` |
| `porbar` | Казарма 17в. | 93.8 | W100 S100 G500 | 150 | [B] `porbla` |
| `porbla` | Кузница | 93.8 | W100 S30 I640 | — | [B] `porcen` |
| `porcen` | Городской центр | 156.2 | W700 S700 | 100 | — |
| `pordip` | Дипломатический центр | 312.5 | W4900 S1700 | — | [B] `poraca` |
| `porhou` | Дом | 31.2 | W100 S100 | 25 | [B] `porcen` |
| `porpor` | Порт | 1562.5 | W1600 S800 I400 | — | [B] `spamar` |
| `porsta` | Конюшня | 625.0 | W2500 S100 G600 | — | [B] `porbla` |
| `portem` | Собор | 156.2 | W1000 S1200 I500 | — | [B] `porcen` |
| `spamar` | Рынок | 156.2 | W450 | — | [B] `eurmil`, [B] `spasto` |
| `spasto` | Склад | 31.2 | W20 S20 | — | [B] `porcen` |
| `ukrwga` | Деревянные ворота | 5.6 | W10 | — | — |
| `ukrwwa` | Частокол | 5.6 | W10 | — | [B] `spasto` |

### `por` — юниты

| sid | имя | Время (g-сек) | цена | тренируется в | требует |
|---|---|---:|---|---|---|
| `archerdip` | Лучник (наемник) | 1.25 | G15 | pordip | [B] `poraca`, [B] `porcen` |
| `archerturdip` | Турецкий лучник (наемник) | 1.25 | G15 | pordip | [B] `poraca`, [B] `porcen` |
| `battleship` | Линейный корабль | 390.00 | W9000 G3200 I700 C6500 | porpor | [T] `poraca.29`, [B] `porart` |
| `cannon` | Пушка | 75.00 | W250 G400 I400 | porart | [B] `porbla` |
| `cossacksichdip` | Сечевой козак (наемник) | 2.50 | G60 | pordip | [B] `poraca`, [B] `porcen` |
| `cuirassier` | Кирасир | 22.50 | F120 G35 I25 | porsta | [B] `porbla`, [T] `porcen.1` |
| `dragoon` | Драгун 17в. | 15.00 | F90 G7 I5 | porsta | [B] `porbla` |
| `dragoon18` | Драгун 18в. | 22.50 | F70 G60 I7 | porsta | [B] `porbla`, [T] `porcen.1` |
| `dragoon18dip` | Драгун 18в. (наемник) | 2.00 | G120 | pordip | [B] `poraca`, [B] `porcen` |
| `drummer` | Барабанщик 17в. | 5.00 | F60 G20 | porbar | [B] `poraca` |
| `drummer18` | Барабанщик 18в. | 6.00 | F50 G30 | porba2 | [B] `poraca` |
| `ferry` | Транспорт | 56.00 | W300 G50 I100 | porpor | [B] `porart` |
| `fishboat` | Рыбацкая лодка | 40.00 | W600 | porpor | — |
| `frigate` | Фрегат | 230.00 | W5000 G1100 I600 C800 | porpor | [T] `poraca.6`, [B] `porart` |
| `galley` | Галера | 50.00 | W9500 G900 I800 | porpor | [B] `porart` |
| `grenadier` | Гренадер | 6.00 | F80 G60 I40 | porba2 | [B] `porbla` |
| `grenadierdip` | Гренадер (наемник) | 1.50 | G25 | pordip | [B] `poraca`, [B] `porcen` |
| `howitzer` | Гаубица | 94.00 | W250 G350 I300 | porart | [B] `porbla` |
| `hussar` | Гусар | 15.00 | F70 G20 I2 | porsta | [B] `porbla`, [T] `porcen.1` |
| `jagerpor` | Доброволец | 2.25 | F30 G2 I5 | porba2 | [B] `porbla` |
| `lightcavalrydip` | Легкий кавалерист (наемник) | 2.00 | G120 | pordip | [B] `poraca`, [B] `porcen` |
| `lightinfantrydip` | Легкий пехотинец (наемник) | 1.25 | G4 | pordip | [B] `poraca`, [B] `porcen` |
| `mortar` | Мортира | 25.00 | W100 G75 I200 | porart | [B] `porbla` |
| `multicannon` | Многоствольное орудие | 50.00 | W200 G400 I250 | porart | [T] `poraca.19`, [B] `porbla` |
| `musketeer` | Мушкетер 17в. | 6.00 | F45 G6 I5 | porbar | [B] `porbla` |
| `musketeer18` | Мушкетер 18в. | 4.50 | F50 G40 I40 | porba2 | [B] `porbla` |
| `officer` | Офицер 17в. | 10.00 | F50 G150 I30 | porbar | [B] `poraca` |
| `officer18` | Офицер 18в. | 6.00 | F50 G200 I10 | porba2 | [B] `poraca` |
| `peaspa` | Крестьянин | 12.50 | F100 | porcen | — |
| `pikeman18` | Пикинер 18в. | 1.25 | F30 G2 | porba2 | — |
| `pikemanpor` | Пикинер 17в. | 4.00 | F40 G4 I5 | porbar | [B] `porbla` |
| `priest` | Капеллан | 20.00 | F60 G25 | portem | — |
| `reiter` | Рейтар | 24.00 | F120 G10 I40 | porsta | [B] `porbla` |
| `roundshierdip` | Рундашир (наемник) | 1.50 | G12 | pordip | [B] `poraca`, [B] `porcen` |
| `unitbox` | — | 3.12 | F100 | — | — |
| `yacht` | Яхта | 48.00 | W900 G450 I150 C200 | porpor | [B] `porart` |

### `por` — ключевые апгрейды (с зависимостями)

| sid | имя | Время (g-сек) | цена | требует |
|---|---|---:|---|---|
| `eurcoa.4` | — | 9.4 | F15800 G18500 | [T] `porcen.1` |
| `eurcoa.5` | — | 9.4 | F19800 G21050 | [T] `porcen.1` |
| `eurcoa.6` | — | 9.4 | F50200 G25950 | [T] `porcen.1` |
| `eurgol.4` | — | 9.4 | F15800 G18500 | [T] `porcen.1` |
| `eurgol.5` | — | 9.4 | F19800 G21050 | [T] `porcen.1` |
| `eurgol.6` | — | 9.4 | F50200 G25950 | [T] `porcen.1` |
| `euriro.4` | — | 9.4 | F15800 G18500 | [T] `porcen.1` |
| `euriro.5` | — | 9.4 | F19800 G21050 | [T] `porcen.1` |
| `euriro.6` | — | 9.4 | F50200 G25950 | [T] `porcen.1` |
| `eurtow.1` | — | 31.2 | G250 | [B] `porart` |
| `eurtow.2` | — | 31.2 | I350 | [B] `porart` |
| `eurtow.3` | — | 31.2 | C400 | [B] `porart` |
| `eurtow.4` | — | 31.2 | I450 | [B] `porart` |
| `eurtow.5` | — | 31.2 | C500 | [B] `porart` |
| `ferry.1` | Усовершенствовать конструкцию транспортного судна (+%value% посадочных мест) | 15.6 | F1000 G1250 | [T] `porcen.1` |
| `poraca.12` | Улучшить стрелковое оружие: нарезной ствол (сила выстрела +10%) | 15.6 | I5000 | [B] `porbla` |
| `poraca.13` | Исследовать гранулированный порох (сила выстрела +10%) | 15.6 | G4000 | [B] `porbla` |
| `poraca.14` | Исследовать новые методы очистки серы (сила выстрела +15%) | 15.6 | G7000 | [B] `porbla` |
| `poraca.15` | Исследовать новые методы очистки селитры (сила выстрела +25%) | 15.6 | C11000 | [B] `porbla` |
| `poraca.16` | Исследовать новые добавки в порох (дальность стрельбы артиллерии +5%) | 15.6 | G2000 I12150 | [B] `porart` |
| `poraca.17` | Разработать новые виды стволов: единорог, карронада (дальность стрельбы артиллерии +10%) | 15.6 | S3000 G4550 I19200 | [B] `porart` |
| `poraca.18` | Разработать более прочный лафет для орудий: система Грибоваля (прочность пушек +50%) | 15.6 | G500 I3830 C1500 | [B] `porart` |
| `poraca.19` | Разработать многоствольное орудие | 15.6 | G1500 C2500 | [B] `porart` |
| `poraca.20` | Разработать новые прицельные системы для пушек (меткость стрельбы артиллерии +35%) | 15.6 | W3540 G2000 C7250 | [B] `porart` |
| `poraca.21` | Выделить деньги на ремонтные мастерские для пушек (отремонтировать все пушки) | 15.6 | W350 G100 C250 | [B] `porart` |
| `poraca.25` | Разработать монгольфьер (открывает всю карту) | 15.6 | G5750 | [T] `porcen.1` |
| `poraca.27` | Развивать математику (меткость выстрела орудий +35%) | 15.6 | W9540 G12000 C65200 | [B] `porart` |
| `poraca.28` | Разработать новые парусные системы (скорость кораблей +40%) | 15.6 | W65400 G24050 | [B] `porpor` |
| `poraca.29` | Разработать новую систему шпангоутов и корпуса корабля (условие для постройки линейных кораблей) | 15.6 | W32300 G6800 I9000 C12800 | [B] `porpor` |
| `poraca.30` | Обучить плотников (скорость постройки кораблей увеличивается в 10 раз) | 15.6 | W2300 S42700 G1150 | [B] `porpor` |
| `poraca.32` | Разработать кремниевый замок к ружьям (цена мушкета -50%) | 15.6 | G6050 C7750 | [T] `porcen.1` |
| `poraca.34` | Разработать новые сорта стали для кирас (защита солдат в доспехах +2) | 15.6 | G9750 | [B] `porbla` |
| `poraca.35` | Разработать штык: вставляемый в ствол багинет, штык с трубкой (сила удара холодного оружия +5) | 15.6 | G11500 | [T] `porcen.1`, [B] `porbla` |
| `poraca.36` | Разработать новые сорта стали (эффективность рукопашной атаки мушкетера 18 века и гренадера +25%) | 15.6 | G19500 | [T] `porcen.1`, [B] `porbla` |
| `poraca.5` | Разработать новые снасти и сети для ловли рыбы (эффективность рыбацких лодок +100%) | 15.6 | W12400 G2520 | [B] `porpor` |
| `poraca.6` | Разработать новые методы древообработки (условие для постройки фрегатов) | 15.6 | W12400 G7040 | [B] `porpor` |
| `poraca.7` | Построить новые верфи для рыбацких лодок (стоимость рыбацкой лодки -85%) | 15.6 | W7300 G1220 | [B] `porpor` |
| `poraca.8` | Разработать новые инструменты для древообработки (эффективность добычи дерева +100%) | 15.6 | F5500 G550 | [B] `porbla` |
| `porart.cannon.1.1` | — | 10.0 | W1000 S500 G300 | [B] `porbla` |
| `porart.cannon.1.2` | — | 10.0 | W3000 S1000 G500 | [B] `porbla` |
| `porart.cannon.1.3` | — | 10.0 | W6000 S2000 G1000 | [B] `porbla` |
| `porart.cannon.1.4` | — | 15.6 | F1760 G350 | [B] `porbla` |
| `porart.cannon.1.5` | — | 15.6 | F1760 G350 | [B] `porbla` |
| `porart.cannon.1.6` | — | 15.6 | F1760 G350 | [B] `porbla` |
| `porart.cannon.2.1` | — | 10.0 | G500 I1000 | [B] `porbla` |
| `porart.cannon.2.2` | — | 10.0 | G1000 I2000 | [B] `porbla` |
| `porart.cannon.2.3` | — | 10.0 | G2000 I3000 | [B] `porbla` |
| `porart.cannon.2.4` | — | 15.6 | F2560 | [B] `porbla` |
| `porart.cannon.2.5` | — | 15.6 | F3560 | [B] `porbla` |
| `porart.cannon.2.6` | — | 15.6 | F5560 | [B] `porbla` |
| `porart.howitzer.1.1` | — | 10.0 | W1000 S500 G300 | [B] `porbla` |
| `porart.howitzer.1.2` | — | 10.0 | W3000 S1000 G500 | [B] `porbla` |
| `porart.howitzer.1.3` | — | 10.0 | W6000 S2000 G1000 | [B] `porbla` |
| `porart.howitzer.1.4` | — | 15.6 | F1760 G350 | [B] `porbla` |
| `porart.howitzer.1.5` | — | 15.6 | F1760 G350 | [B] `porbla` |
| `porart.howitzer.1.6` | — | 15.6 | F1760 G350 | [B] `porbla` |
| `porart.howitzer.2.1` | — | 10.0 | G500 I1000 | [B] `porbla` |
| `porart.howitzer.2.2` | — | 10.0 | G1000 I2000 | [B] `porbla` |
| `porart.howitzer.2.3` | — | 10.0 | G2000 I3000 | [B] `porbla` |
| `porart.howitzer.2.4` | — | 31.2 | F2560 | [B] `porbla` |
| `porart.howitzer.2.5` | — | 31.2 | F3560 | [B] `porbla` |
| `porart.howitzer.2.6` | — | 31.2 | F5560 | [B] `porbla` |
| `porbar.pikemanpor.1.6` | — | 15.6 | F15000 G1875 | [B] `porbla` |
| `porbar.pikemanpor.2.6` | — | 15.6 | F11250 G1500 | [B] `porbla` |
| `porbla.4` | Выковать штыки и тесаки для пехоты (сила удара мушкетера 18 века и гренадера +5) | 15.6 | W1300 G1500 I900 C5000 | [T] `porcen.1` |
| `porcen.1` | — | 9.4 | F30000 G5000 I2000 C2000 | [B] `poraca`, [B] `portem`, [B] `porart` |
| `porpor.1` | — | 46.9 | W20000 G1500 | [B] `porart` |

[↑ к содержанию](#содержание)

## PRU — Prussia (Пруссия)

### `pru` — здания

| sid | имя | Время (g-сек) | цена | ферма | требует |
|---|---|---:|---|---:|---|
| `eurcoa` | Шахта | 93.8 | W100 S100 | — | — |
| `eurgol` | Шахта | 93.8 | W100 S100 | — | — |
| `euriro` | Шахта | 93.8 | W100 S100 | — | — |
| `eurmar` | Рынок | 234.4 | W450 | — | [B] `eurmil`, [B] `eursto` |
| `eurmil` | Мельница | 93.8 | W30 S150 | — | — |
| `eurpor` | Порт | 1562.5 | W1600 S800 I400 | — | [B] `eurmar` |
| `eursga` | Каменные ворота | 90.0 | S50 | — | — |
| `eursto` | Склад | 31.2 | W50 S20 | — | [B] `prucen` |
| `eurswa` | Стена | 90.0 | S50 | — | [B] `eursto` |
| `eurtow` | Башня | 1230.3 | W100 S100 G150 | — | [B] `eursto` |
| `pruaca` | Академия | 625.0 | W1200 S1150 | — | [B] `prubar` |
| `pruart` | Артиллерийское депо | 245.9 | W100 S1000 C1400 | — | [B] `pruaca` |
| `pruba2` | Казарма 18в. | 5625.0 | W1700 S2950 G4000 | 250 | [T] `prucen.1` |
| `prubar` | Казарма 17в. | 93.8 | W100 S100 G500 | 150 | [B] `prubla` |
| `prubla` | Кузница | 93.8 | W100 S30 I640 | — | [B] `prucen` |
| `prucen` | Городской центр | 156.2 | W700 S700 | 100 | — |
| `prudip` | Дипломатический центр | 312.5 | W4900 S1700 | — | [B] `pruaca` |
| `pruhou` | Дом | 31.2 | W100 S100 | 25 | [B] `prucen` |
| `prusta` | Конюшня | 625.0 | W2500 S100 G600 | — | [B] `prubla` |
| `prutem` | Собор | 156.2 | W1000 S1200 I500 | — | [B] `prucen` |
| `ukrwga` | Деревянные ворота | 5.6 | W10 | — | — |
| `ukrwwa` | Частокол | 5.6 | W10 | — | [B] `eursto` |

### `pru` — юниты

| sid | имя | Время (g-сек) | цена | тренируется в | требует |
|---|---|---:|---|---|---|
| `archerdip` | Лучник (наемник) | 1.25 | G15 | prudip | [B] `pruaca`, [B] `prucen` |
| `archerturdip` | Турецкий лучник (наемник) | 1.25 | G15 | prudip | [B] `pruaca`, [B] `prucen` |
| `battleship` | Линейный корабль | 390.00 | W9000 G3200 I700 C6500 | eurpor | [T] `pruaca.29`, [B] `pruart` |
| `cannon` | Пушка | 75.00 | W250 G400 I400 | pruart | [B] `prubla` |
| `cossacksichdip` | Сечевой козак (наемник) | 2.50 | G60 | prudip | [B] `pruaca`, [B] `prucen` |
| `cuirassier` | Кирасир | 22.50 | F120 G35 I25 | prusta | [B] `prubla`, [T] `prucen.1` |
| `dragoon` | Драгун 17в. | 15.00 | F90 G7 I5 | prusta | [B] `prubla` |
| `dragoon18` | Драгун 18в. | 22.50 | F70 G60 I7 | prusta | [B] `prubla`, [T] `prucen.1` |
| `dragoon18dip` | Драгун 18в. (наемник) | 2.00 | G120 | prudip | [B] `pruaca`, [B] `prucen` |
| `drummer` | Барабанщик 17в. | 5.00 | F60 G20 | prubar | [B] `pruaca` |
| `drummer18` | Барабанщик 18в. | 6.00 | F50 G30 | pruba2 | [B] `pruaca` |
| `ferry` | Транспорт | 56.00 | W300 G50 I100 | eurpor | [B] `pruart` |
| `fishboat` | Рыбацкая лодка | 40.00 | W600 | eurpor | — |
| `frigate` | Фрегат | 230.00 | W5000 G1100 I600 C800 | eurpor | [T] `pruaca.6`, [B] `pruart` |
| `galley` | Галера | 50.00 | W9500 G900 I800 | eurpor | [B] `pruart` |
| `grenadier` | Гренадер | 6.00 | F80 G60 I40 | pruba2 | [B] `prubla` |
| `grenadierdip` | Гренадер (наемник) | 1.50 | G25 | prudip | [B] `pruaca`, [B] `prucen` |
| `grenadierpru` | Гренадер | 7.00 | F90 G100 I45 | pruba2 | [B] `prubla` |
| `howitzer` | Гаубица | 94.00 | W250 G350 I300 | pruart | [B] `prubla` |
| `hussarpru` | Гусар | 11.25 | F80 G15 I2 | prusta | [B] `prubla`, [T] `prucen.1` |
| `lightcavalrydip` | Легкий кавалерист (наемник) | 2.00 | G120 | prudip | [B] `pruaca`, [B] `prucen` |
| `lightinfantrydip` | Легкий пехотинец (наемник) | 1.25 | G4 | prudip | [B] `pruaca`, [B] `prucen` |
| `mortar` | Мортира | 25.00 | W100 G75 I200 | pruart | [B] `prubla` |
| `multicannon` | Многоствольное орудие | 50.00 | W200 G400 I250 | pruart | [T] `pruaca.19`, [B] `prubla` |
| `musketeer` | Мушкетер 17в. | 6.00 | F45 G6 I5 | prubar | [B] `prubla` |
| `musketeer18pru` | Мушкетер 18в. | 6.00 | F70 G80 I40 | pruba2 | [B] `prubla` |
| `officer` | Офицер 17в. | 10.00 | F50 G150 I30 | prubar | [B] `pruaca` |
| `officer18` | Офицер 18в. | 6.00 | F50 G200 I10 | pruba2 | [B] `pruaca` |
| `peaaus` | Крестьянин | 12.50 | F100 | prucen | — |
| `pikeman` | Пикинер 17в. | 4.50 | F25 G3 I20 | prubar | [B] `prubla` |
| `pikeman18` | Пикинер 18в. | 1.25 | F30 G2 | pruba2 | — |
| `priest` | Капеллан | 20.00 | F60 G25 | prutem | — |
| `reiter` | Рейтар | 24.00 | F120 G10 I40 | prusta | [B] `prubla` |
| `roundshierdip` | Рундашир (наемник) | 1.50 | G12 | prudip | [B] `pruaca`, [B] `prucen` |
| `unitbox` | — | 3.12 | F100 | — | — |
| `yacht` | Яхта | 48.00 | W900 G450 I150 C200 | eurpor | [B] `pruart` |

### `pru` — ключевые апгрейды (с зависимостями)

| sid | имя | Время (g-сек) | цена | требует |
|---|---|---:|---|---|
| `eurcoa.4` | — | 9.4 | F15800 G18500 | [T] `prucen.1` |
| `eurcoa.5` | — | 9.4 | F19800 G21050 | [T] `prucen.1` |
| `eurcoa.6` | — | 9.4 | F50200 G25950 | [T] `prucen.1` |
| `eurgol.4` | — | 9.4 | F15800 G18500 | [T] `prucen.1` |
| `eurgol.5` | — | 9.4 | F19800 G21050 | [T] `prucen.1` |
| `eurgol.6` | — | 9.4 | F50200 G25950 | [T] `prucen.1` |
| `euriro.4` | — | 9.4 | F15800 G18500 | [T] `prucen.1` |
| `euriro.5` | — | 9.4 | F19800 G21050 | [T] `prucen.1` |
| `euriro.6` | — | 9.4 | F50200 G25950 | [T] `prucen.1` |
| `eurpor.1` | — | 46.9 | W20000 G1500 | [B] `pruart` |
| `eurtow.1` | — | 31.2 | G250 | [B] `pruart` |
| `eurtow.2` | — | 31.2 | I350 | [B] `pruart` |
| `eurtow.3` | — | 31.2 | C400 | [B] `pruart` |
| `eurtow.4` | — | 31.2 | I450 | [B] `pruart` |
| `eurtow.5` | — | 31.2 | C500 | [B] `pruart` |
| `ferry.1` | Усовершенствовать конструкцию транспортного судна (+%value% посадочных мест) | 15.6 | F1000 G1250 | [T] `prucen.1` |
| `pruaca.12` | Улучшить стрелковое оружие: нарезной ствол (сила выстрела +10%) | 15.6 | I5000 | [B] `prubla` |
| `pruaca.13` | Исследовать гранулированный порох (сила выстрела +10%) | 15.6 | G4000 | [B] `prubla` |
| `pruaca.14` | Исследовать новые методы очистки серы (сила выстрела +15%) | 15.6 | G7000 | [B] `prubla` |
| `pruaca.15` | Исследовать новые методы очистки селитры (сила выстрела +25%) | 15.6 | C11000 | [B] `prubla` |
| `pruaca.16` | Исследовать новые добавки в порох (дальность стрельбы артиллерии +5%) | 15.6 | G2000 I12150 | [B] `pruart` |
| `pruaca.17` | Разработать новые виды стволов: единорог, карронада (дальность стрельбы артиллерии +10%) | 15.6 | S3000 G4550 I19200 | [B] `pruart` |
| `pruaca.18` | Разработать более прочный лафет для орудий: система Грибоваля (прочность пушек +50%) | 15.6 | G500 I3830 C1500 | [B] `pruart` |
| `pruaca.19` | Разработать многоствольное орудие | 15.6 | G1500 C2500 | [B] `pruart` |
| `pruaca.20` | Разработать новые прицельные системы для пушек (меткость стрельбы артиллерии +35%) | 15.6 | W23540 G1900 C4250 | [B] `pruart` |
| `pruaca.21` | Выделить деньги на ремонтные мастерские для пушек (отремонтировать все пушки) | 15.6 | W350 G100 C250 | [B] `pruart` |
| `pruaca.25` | Разработать монгольфьер (открывает всю карту) | 15.6 | G5750 | [T] `prucen.1` |
| `pruaca.27` | Развивать математику (меткость выстрела орудий +35%) | 15.6 | W12540 G8500 C57200 | [B] `pruart` |
| `pruaca.28` | Разработать новые парусные системы (скорость кораблей +40%) | 15.6 | W65400 G24050 | [B] `eurpor` |
| `pruaca.29` | Разработать новую систему шпангоутов и корпуса корабля (условие для постройки линейных кораблей) | 15.6 | W32300 G6800 I9000 C12800 | [B] `eurpor` |
| `pruaca.30` | Обучить плотников (скорость постройки кораблей увеличивается в 10 раз) | 15.6 | W2300 S42700 G1150 | [B] `eurpor` |
| `pruaca.32` | Разработать кремниевый замок к ружьям (цена мушкета -50%) | 15.6 | G6050 C7750 | [T] `prucen.1` |
| `pruaca.34` | Разработать новые сорта стали для кирас (защита солдат в доспехах +2) | 15.6 | G9750 | [B] `prubla` |
| `pruaca.35` | Разработать штык: вставляемый в ствол багинет, штык с трубкой (сила удара холодного оружия +5) | 15.6 | G11500 | [T] `prucen.1`, [B] `prubla` |
| `pruaca.36` | Разработать новые сорта стали (эффективность рукопашной атаки мушкетера 18 века и гренадера +25%) | 15.6 | G19500 | [T] `prucen.1`, [B] `prubla` |
| `pruaca.5` | Разработать новые снасти и сети для ловли рыбы (эффективность рыбацких лодок +100%) | 15.6 | W12400 G2520 | [B] `eurpor` |
| `pruaca.6` | Разработать новые методы древообработки (условие для постройки фрегатов) | 15.6 | W12400 G7040 | [B] `eurpor` |
| `pruaca.7` | Построить новые верфи для рыбацких лодок (стоимость рыбацкой лодки -85%) | 15.6 | W7300 G1220 | [B] `eurpor` |
| `pruaca.8` | Разработать новые инструменты для древообработки (эффективность добычи дерева +100%) | 15.6 | F5500 G550 | [B] `prubla` |
| `pruart.cannon.1.1` | — | 10.0 | W1000 S500 G300 | [B] `prubla` |
| `pruart.cannon.1.2` | — | 10.0 | W3000 S1000 G500 | [B] `prubla` |
| `pruart.cannon.1.3` | — | 10.0 | W6000 S2000 G1000 | [B] `prubla` |
| `pruart.cannon.1.4` | — | 15.6 | F1760 G350 | [B] `prubla` |
| `pruart.cannon.1.5` | — | 15.6 | F1760 G350 | [B] `prubla` |
| `pruart.cannon.1.6` | — | 15.6 | F1760 G350 | [B] `prubla` |
| `pruart.cannon.2.1` | — | 10.0 | G500 I1000 | [B] `prubla` |
| `pruart.cannon.2.2` | — | 10.0 | G1000 I2000 | [B] `prubla` |
| `pruart.cannon.2.3` | — | 10.0 | G2000 I3000 | [B] `prubla` |
| `pruart.cannon.2.4` | — | 15.6 | F2560 | [B] `prubla` |
| `pruart.cannon.2.5` | — | 15.6 | F3560 | [B] `prubla` |
| `pruart.cannon.2.6` | — | 15.6 | F5560 | [B] `prubla` |
| `pruart.howitzer.1.1` | — | 10.0 | W1000 S500 G300 | [B] `prubla` |
| `pruart.howitzer.1.2` | — | 10.0 | W3000 S1000 G500 | [B] `prubla` |
| `pruart.howitzer.1.3` | — | 10.0 | W6000 S2000 G1000 | [B] `prubla` |
| `pruart.howitzer.1.4` | — | 15.6 | F1760 G350 | [B] `prubla` |
| `pruart.howitzer.1.5` | — | 15.6 | F1760 G350 | [B] `prubla` |
| `pruart.howitzer.1.6` | — | 15.6 | F1760 G350 | [B] `prubla` |
| `pruart.howitzer.2.1` | — | 10.0 | G500 I1000 | [B] `prubla` |
| `pruart.howitzer.2.2` | — | 10.0 | G1000 I2000 | [B] `prubla` |
| `pruart.howitzer.2.3` | — | 10.0 | G2000 I3000 | [B] `prubla` |
| `pruart.howitzer.2.4` | — | 31.2 | F2560 | [B] `prubla` |
| `pruart.howitzer.2.5` | — | 31.2 | F3560 | [B] `prubla` |
| `pruart.howitzer.2.6` | — | 31.2 | F5560 | [B] `prubla` |
| `prubar.pikeman.1.6` | — | 15.6 | F15000 G1875 | [B] `prubla` |
| `prubar.pikeman.2.6` | — | 15.6 | F11250 G1500 | [B] `prubla` |
| `prubla.4` | Выковать штыки и тесаки для пехоты (сила удара мушкетера 18 века и гренадера +5) | 15.6 | W1300 G1500 I900 C5000 | [T] `prucen.1` |
| `prucen.1` | — | 9.4 | F20000 G6500 I1100 C1100 | [B] `pruaca`, [B] `prutem`, [B] `pruart` |

[↑ к содержанию](#содержание)

## RUS — Russia (Россия)

### `rus` — здания

| sid | имя | Время (g-сек) | цена | ферма | требует |
|---|---|---:|---|---:|---|
| `eurcoa` | Шахта | 93.8 | W100 S100 | — | — |
| `eurgol` | Шахта | 93.8 | W100 S100 | — | — |
| `euriro` | Шахта | 93.8 | W100 S100 | — | — |
| `rusaca` | Академия | 843.8 | W1250 S1300 | — | [B] `rusbar` |
| `rusart` | Артиллерийское депо | 245.9 | W100 S1000 C1400 | — | [B] `rusaca` |
| `rusba2` | Казарма 18в. | 5625.0 | W1700 S2950 G4000 | 250 | [T] `ruscen.1` |
| `rusbar` | Стрелецкая казарма | 78.1 | W200 S20 | 25 | [B] `rusbla` |
| `rusbla` | Кузница | 93.8 | W100 S30 I640 | — | [B] `ruscen` |
| `ruscen` | Городской центр | 156.2 | W680 S700 | 75 | — |
| `rusdip` | Дипломатический центр | 312.5 | W7900 S3700 | — | [B] `rusaca` |
| `rushou` | Изба | 31.2 | W120 | 25 | [B] `ruscen` |
| `rusmar` | Рынок | 234.4 | W450 | — | [B] `rusmil`, [B] `russto` |
| `rusmil` | Мельница | 93.8 | W210 | — | — |
| `ruspor` | Порт | 1562.5 | W1200 S800 I400 | — | [B] `rusmar` |
| `russga` | Каменные ворота | 200.0 | S60 | — | — |
| `russta` | Конюшня | 375.0 | W7950 G550 | — | [B] `rusbla` |
| `russto` | Склад | 31.2 | W50 S20 | — | [B] `ruscen` |
| `russwa` | Стена | 200.0 | S60 | — | [B] `russto` |
| `rustem` | Православная церковь | 156.2 | W1150 S1650 G100 I500 | — | [B] `ruscen` |
| `rustow` | Башня | 1476.6 | W100 S100 G150 | — | [B] `russto` |
| `ukrwga` | Деревянные ворота | 5.6 | W10 | — | — |
| `ukrwwa` | Частокол | 5.6 | W10 | — | [B] `russto` |

### `rus` — юниты

| sid | имя | Время (g-сек) | цена | тренируется в | требует |
|---|---|---:|---|---|---|
| `archerdip` | Лучник (наемник) | 1.25 | G15 | rusdip | [B] `rusaca`, [B] `ruscen` |
| `archerturdip` | Турецкий лучник (наемник) | 1.25 | G15 | rusdip | [B] `rusaca`, [B] `ruscen` |
| `battleship` | Линейный корабль | 390.00 | W9000 G3200 I700 C6500 | ruspor | [T] `rusaca.29`, [B] `rusart` |
| `cannon` | Пушка | 75.00 | W250 G400 I400 | rusart | [B] `rusbla` |
| `cossackdon` | Донской козак | 13.50 | F100 W1 | russta | — |
| `cossacksichdip` | Сечевой козак (наемник) | 2.50 | G60 | rusdip | [B] `rusaca`, [B] `ruscen` |
| `cuirassier` | Кирасир | 22.50 | F120 G35 I25 | russta | [B] `rusbla`, [T] `ruscen.1` |
| `dragoon18` | Драгун 18в. | 22.50 | F70 G60 I7 | russta | [B] `rusbla`, [T] `ruscen.1` |
| `dragoon18dip` | Драгун 18в. (наемник) | 2.00 | G120 | rusdip | [B] `rusaca`, [B] `ruscen` |
| `drummer18` | Барабанщик 18в. | 6.00 | F90 G15 | rusba2 | [B] `rusaca` |
| `drummerrus` | Барабанщик 17в. | 6.00 | F90 G15 | rusbar | [B] `rusaca` |
| `ferry` | Транспорт | 56.00 | W300 G50 I100 | ruspor | [B] `rusart` |
| `fishboat` | Рыбацкая лодка | 40.00 | W600 | ruspor | — |
| `frigate` | Фрегат | 230.00 | W5000 G1100 I600 C800 | ruspor | [T] `rusaca.6`, [B] `rusart` |
| `galley` | Галера | 50.00 | W9500 G900 I800 | ruspor | [B] `rusart` |
| `grenadier` | Гренадер | 6.00 | F80 G60 I40 | rusba2 | [B] `rusbla` |
| `grenadierdip` | Гренадер (наемник) | 1.50 | G25 | rusdip | [B] `rusaca`, [B] `ruscen` |
| `howitzer` | Гаубица | 94.00 | W250 G350 I300 | rusart | [B] `rusbla` |
| `hussar` | Гусар | 15.00 | F70 G20 I2 | russta | [B] `rusbla`, [T] `ruscen.1` |
| `lightcavalrydip` | Легкий кавалерист (наемник) | 2.00 | G120 | rusdip | [B] `rusaca`, [B] `ruscen` |
| `lightinfantrydip` | Легкий пехотинец (наемник) | 1.25 | G4 | rusdip | [B] `rusaca`, [B] `ruscen` |
| `mortar` | Мортира | 25.00 | W100 G75 I200 | rusart | [B] `rusbla` |
| `multicannon` | Многоствольное орудие | 50.00 | W200 G400 I250 | rusart | [T] `rusaca.19`, [B] `rusbla` |
| `musketeer18` | Мушкетер 18в. | 4.50 | F50 G40 I40 | rusba2 | [B] `rusbla` |
| `officer18` | Офицер 18в. | 6.00 | F50 G200 I10 | rusba2 | [B] `rusaca` |
| `officerrus` | Командир | 12.50 | F100 G125 I5 | rusbar | [B] `rusaca` |
| `pearus` | Крепостной | 12.50 | F100 | ruscen | — |
| `pikeman18` | Пикинер 18в. | 1.25 | F30 G2 | rusba2 | — |
| `pikemanrus` | Копейщик | 5.50 | F45 G4 I15 | rusbar | [B] `rusbla` |
| `pope` | Поп | 20.00 | F40 G20 | rustem | — |
| `roundshierdip` | Рундашир (наемник) | 1.50 | G12 | rusdip | [B] `rusaca`, [B] `ruscen` |
| `strelet` | Стрелец | 8.50 | F70 G7 I9 | rusbar | [B] `rusbla` |
| `unitbox` | — | 3.12 | F100 | — | — |
| `vityaz` | Витязь | 25.50 | F160 G13 I25 | russta | [B] `rusbla` |
| `yacht` | Яхта | 48.00 | W900 G450 I150 C200 | ruspor | [B] `rusart` |

### `rus` — ключевые апгрейды (с зависимостями)

| sid | имя | Время (g-сек) | цена | требует |
|---|---|---:|---|---|
| `eurcoa.4` | — | 9.4 | F15800 G18500 | [T] `ruscen.1` |
| `eurcoa.5` | — | 9.4 | F19800 G21050 | [T] `ruscen.1` |
| `eurcoa.6` | — | 9.4 | F50200 G25950 | [T] `ruscen.1` |
| `eurgol.4` | — | 9.4 | F15800 G18500 | [T] `ruscen.1` |
| `eurgol.5` | — | 9.4 | F19800 G21050 | [T] `ruscen.1` |
| `eurgol.6` | — | 9.4 | F50200 G25950 | [T] `ruscen.1` |
| `euriro.4` | — | 9.4 | F15800 G18500 | [T] `ruscen.1` |
| `euriro.5` | — | 9.4 | F19800 G21050 | [T] `ruscen.1` |
| `euriro.6` | — | 9.4 | F50200 G25950 | [T] `ruscen.1` |
| `ferry.1` | Усовершенствовать конструкцию транспортного судна (+%value% посадочных мест) | 15.6 | F1000 G1250 | [T] `ruscen.1` |
| `rusaca.12` | Улучшить стрелковое оружие: нарезной ствол (сила выстрела +10%) | 15.6 | I5000 | [B] `rusbla` |
| `rusaca.13` | Исследовать гранулированный порох (сила выстрела +10%) | 15.6 | G4000 | [B] `rusbla` |
| `rusaca.14` | Исследовать новые методы очистки серы (сила выстрела +15%) | 15.6 | G7000 | [B] `rusbla` |
| `rusaca.15` | Исследовать новые методы очистки селитры (сила выстрела +25%) | 15.6 | C11000 | [B] `rusbla` |
| `rusaca.16` | Исследовать новые добавки в порох (дальность стрельбы артиллерии +5%) | 15.6 | G2000 I12150 | [B] `rusart` |
| `rusaca.17` | Разработать новые виды стволов: единорог, карронада (дальность стрельбы артиллерии +10%) | 15.6 | S3000 G4550 I19200 | [B] `rusart` |
| `rusaca.18` | Разработать более прочный лафет для орудий: система Грибоваля (прочность пушек +50%) | 15.6 | G500 I3830 C1500 | [B] `rusart` |
| `rusaca.19` | Разработать многоствольное орудие | 15.6 | G1500 C2500 | [B] `rusart` |
| `rusaca.20` | Разработать новые прицельные системы для пушек (меткость стрельбы артиллерии +35%) | 15.6 | W3540 G2000 C7250 | [B] `rusart` |
| `rusaca.21` | Выделить деньги на ремонтные мастерские для пушек (отремонтировать все пушки) | 15.6 | W350 G100 C250 | [B] `rusart` |
| `rusaca.25` | Разработать монгольфьер (открывает всю карту) | 15.6 | G5750 | [T] `ruscen.1` |
| `rusaca.27` | Развивать математику (меткость выстрела орудий +35%) | 15.6 | W9540 G12000 C65200 | [B] `rusart` |
| `rusaca.28` | Разработать новые парусные системы (скорость кораблей +40%) | 15.6 | W65400 G24050 | [B] `ruspor` |
| `rusaca.29` | Разработать новую систему шпангоутов и корпуса корабля (условие для постройки линейных кораблей) | 15.6 | W32300 G6800 I9000 C12800 | [B] `ruspor` |
| `rusaca.30` | Обучить плотников (скорость постройки кораблей увеличивается в 10 раз) | 15.6 | W2300 S42700 G1150 | [B] `ruspor` |
| `rusaca.32` | Разработать кремниевый замок к ружьям (цена мушкета -50%) | 15.6 | G6050 C7750 | [T] `ruscen.1` |
| `rusaca.34` | Разработать новые сорта стали для кирас (защита солдат в доспехах +2) | 15.6 | G9750 | [B] `rusbla` |
| `rusaca.35` | Разработать штык: вставляемый в ствол багинет, штык с трубкой (сила удара холодного оружия +5) | 15.6 | G11500 | [T] `ruscen.1`, [B] `rusbla` |
| `rusaca.36` | Разработать новые сорта стали (эффективность рукопашной атаки мушкетера 18 века и гренадера +25%) | 15.6 | G19500 | [T] `ruscen.1`, [B] `rusbla` |
| `rusaca.5` | Разработать новые снасти и сети для ловли рыбы (эффективность рыбацких лодок +100%) | 15.6 | W12400 G2520 | [B] `ruspor` |
| `rusaca.6` | Разработать новые методы древообработки (условие для постройки фрегатов) | 15.6 | W12400 G7040 | [B] `ruspor` |
| `rusaca.7` | Построить новые верфи для рыбацких лодок (стоимость рыбацкой лодки -85%) | 15.6 | W7300 G1220 | [B] `ruspor` |
| `rusaca.8` | Разработать новые инструменты для древообработки (эффективность добычи дерева +100%) | 15.6 | F5500 G550 | [B] `rusbla` |
| `rusart.cannon.1.1` | — | 10.0 | W1000 S500 G300 | [B] `rusbla` |
| `rusart.cannon.1.2` | — | 10.0 | W3000 S1000 G500 | [B] `rusbla` |
| `rusart.cannon.1.3` | — | 10.0 | W6000 S2000 G1000 | [B] `rusbla` |
| `rusart.cannon.1.4` | — | 15.6 | F1760 G350 | [B] `rusbla` |
| `rusart.cannon.1.5` | — | 15.6 | F1760 G350 | [B] `rusbla` |
| `rusart.cannon.1.6` | — | 15.6 | F1760 G350 | [B] `rusbla` |
| `rusart.cannon.2.1` | — | 10.0 | G500 I1000 | [B] `rusbla` |
| `rusart.cannon.2.2` | — | 10.0 | G1000 I2000 | [B] `rusbla` |
| `rusart.cannon.2.3` | — | 10.0 | G2000 I3000 | [B] `rusbla` |
| `rusart.cannon.2.4` | — | 15.6 | F2560 | [B] `rusbla` |
| `rusart.cannon.2.5` | — | 15.6 | F3560 | [B] `rusbla` |
| `rusart.cannon.2.6` | — | 15.6 | F5560 | [B] `rusbla` |
| `rusart.howitzer.1.1` | — | 10.0 | W1000 S500 G300 | [B] `rusbla` |
| `rusart.howitzer.1.2` | — | 10.0 | W3000 S1000 G500 | [B] `rusbla` |
| `rusart.howitzer.1.3` | — | 10.0 | W6000 S2000 G1000 | [B] `rusbla` |
| `rusart.howitzer.1.4` | — | 15.6 | F1760 G350 | [B] `rusbla` |
| `rusart.howitzer.1.5` | — | 15.6 | F1760 G350 | [B] `rusbla` |
| `rusart.howitzer.1.6` | — | 15.6 | F1760 G350 | [B] `rusbla` |
| `rusart.howitzer.2.1` | — | 10.0 | G500 I1000 | [B] `rusbla` |
| `rusart.howitzer.2.2` | — | 10.0 | G1000 I2000 | [B] `rusbla` |
| `rusart.howitzer.2.3` | — | 10.0 | G2000 I3000 | [B] `rusbla` |
| `rusart.howitzer.2.4` | — | 31.2 | F2560 | [B] `rusbla` |
| `rusart.howitzer.2.5` | — | 31.2 | F3560 | [B] `rusbla` |
| `rusart.howitzer.2.6` | — | 31.2 | F5560 | [B] `rusbla` |
| `rusbar.pikemanrus.1.6` | — | 15.6 | F15000 G1875 | [B] `rusbla` |
| `rusbar.pikemanrus.2.6` | — | 15.6 | F11250 G1500 | [B] `rusbla` |
| `rusbla.4` | Выковать штыки и тесаки для пехоты (сила удара мушкетера 18 века и гренадера +5) | 15.6 | W1300 G1500 I900 C5000 | [T] `ruscen.1` |
| `ruscen.1` | — | 9.4 | F30000 G5000 I2000 C2000 | [B] `rusaca`, [B] `rustem`, [B] `rusart` |
| `ruspor.1` | — | 46.9 | W20000 G1500 | [B] `rusart` |
| `rustow.1` | — | 31.2 | G250 | [B] `rusart` |
| `rustow.2` | — | 31.2 | I350 | [B] `rusart` |
| `rustow.3` | — | 31.2 | C400 | [B] `rusart` |
| `rustow.4` | — | 31.2 | I450 | [B] `rusart` |
| `rustow.5` | — | 31.2 | C500 | [B] `rusart` |

[↑ к содержанию](#содержание)

## SAX — Saxony (Саксония)

### `sax` — здания

| sid | имя | Время (g-сек) | цена | ферма | требует |
|---|---|---:|---|---:|---|
| `eurcoa` | Шахта | 93.8 | W100 S100 | — | — |
| `eurgol` | Шахта | 93.8 | W100 S100 | — | — |
| `euriro` | Шахта | 93.8 | W100 S100 | — | — |
| `eurmar` | Рынок | 234.4 | W450 | — | [B] `eurmil`, [B] `eursto` |
| `eurmil` | Мельница | 93.8 | W30 S150 | — | — |
| `eurpor` | Порт | 1562.5 | W1600 S800 I400 | — | [B] `eurmar` |
| `eursga` | Каменные ворота | 90.0 | S50 | — | — |
| `eursto` | Склад | 31.2 | W50 S20 | — | [B] `saxcen` |
| `eurswa` | Стена | 90.0 | S50 | — | [B] `eursto` |
| `eurtow` | Башня | 1230.3 | W100 S100 G150 | — | [B] `eursto` |
| `saxaca` | Академия | 625.0 | W1250 S1100 | — | [B] `saxbar` |
| `saxart` | Артиллерийское депо | 245.9 | W100 S1000 C1400 | — | [B] `saxaca` |
| `saxba2` | Казарма 18в. | 5625.0 | W1700 S2950 G4000 | 250 | [T] `saxcen.1` |
| `saxbar` | Казарма 17в. | 93.8 | W100 S100 G500 | 150 | [B] `saxbla` |
| `saxbla` | Кузница | 93.8 | W100 S30 I640 | — | [B] `saxcen` |
| `saxcen` | Городской центр | 156.2 | W700 S700 | 100 | — |
| `saxdip` | Дипломатический центр | 312.5 | W4900 S1700 | — | [B] `saxaca` |
| `saxhou` | Дом | 31.2 | W100 S100 | 25 | [B] `saxcen` |
| `saxsta` | Конюшня | 625.0 | W2500 S100 G600 | — | [B] `saxbla` |
| `saxtem` | Собор | 156.2 | W1000 S1200 I500 | — | [B] `saxcen` |
| `ukrwga` | Деревянные ворота | 5.6 | W10 | — | — |
| `ukrwwa` | Частокол | 5.6 | W10 | — | [B] `eursto` |

### `sax` — юниты

| sid | имя | Время (g-сек) | цена | тренируется в | требует |
|---|---|---:|---|---|---|
| `archerdip` | Лучник (наемник) | 1.25 | G15 | saxdip | [B] `saxaca`, [B] `saxcen` |
| `archerturdip` | Турецкий лучник (наемник) | 1.25 | G15 | saxdip | [B] `saxaca`, [B] `saxcen` |
| `battleship` | Линейный корабль | 390.00 | W9000 G3200 I700 C6500 | eurpor | [T] `saxaca.29`, [B] `saxart` |
| `cannon` | Пушка | 75.00 | W250 G400 I400 | saxart | [B] `saxbla` |
| `cossacksichdip` | Сечевой козак (наемник) | 2.50 | G60 | saxdip | [B] `saxaca`, [B] `saxcen` |
| `cuirassier` | Кирасир | 22.50 | F120 G35 I25 | saxsta | [B] `saxbla`, [T] `saxcen.1` |
| `dragoon` | Драгун 17в. | 15.00 | F90 G7 I5 | saxsta | [B] `saxbla` |
| `dragoon18` | Драгун 18в. | 22.50 | F70 G60 I7 | saxsta | [B] `saxbla`, [T] `saxcen.1` |
| `dragoon18dip` | Драгун 18в. (наемник) | 2.00 | G120 | saxdip | [B] `saxaca`, [B] `saxcen` |
| `drummer` | Барабанщик 17в. | 5.00 | F60 G20 | saxbar | [B] `saxaca` |
| `drummer18` | Барабанщик 18в. | 6.00 | F50 G30 | saxba2 | [B] `saxaca` |
| `ferry` | Транспорт | 56.00 | W300 G50 I100 | eurpor | [B] `saxart` |
| `fishboat` | Рыбацкая лодка | 40.00 | W600 | eurpor | — |
| `frigate` | Фрегат | 230.00 | W5000 G1100 I600 C800 | eurpor | [T] `saxaca.6`, [B] `saxart` |
| `galley` | Галера | 50.00 | W9500 G900 I800 | eurpor | [B] `saxart` |
| `grenadierdip` | Гренадер (наемник) | 1.50 | G25 | saxdip | [B] `saxaca`, [B] `saxcen` |
| `grenadiersax` | Гренадер | 6.00 | F50 G60 I40 | saxba2 | [B] `saxbla` |
| `guardcavalrysax` | Гвардейский кавалерист | 24.00 | F140 G50 I20 | saxsta | [B] `saxbla`, [T] `saxcen.1` |
| `howitzer` | Гаубица | 94.00 | W250 G350 I300 | saxart | [B] `saxbla` |
| `hussar` | Гусар | 15.00 | F70 G20 I2 | saxsta | [B] `saxbla`, [T] `saxcen.1` |
| `lightcavalrydip` | Легкий кавалерист (наемник) | 2.00 | G120 | saxdip | [B] `saxaca`, [B] `saxcen` |
| `lightinfantrydip` | Легкий пехотинец (наемник) | 1.25 | G4 | saxdip | [B] `saxaca`, [B] `saxcen` |
| `mortar` | Мортира | 25.00 | W100 G75 I200 | saxart | [B] `saxbla` |
| `multicannon` | Многоствольное орудие | 50.00 | W200 G400 I250 | saxart | [T] `saxaca.19`, [B] `saxbla` |
| `musketeer` | Мушкетер 17в. | 6.00 | F45 G6 I5 | saxbar | [B] `saxbla` |
| `musketeer18sax` | Мушкетер 18в. | 4.50 | F40 G45 I40 | saxba2 | [B] `saxbla` |
| `officer` | Офицер 17в. | 10.00 | F50 G150 I30 | saxbar | [B] `saxaca` |
| `officer18` | Офицер 18в. | 6.00 | F50 G200 I10 | saxba2 | [B] `saxaca` |
| `peaaus` | Крестьянин | 12.50 | F100 | saxcen | — |
| `pikeman` | Пикинер 17в. | 4.50 | F25 G3 I20 | saxbar | [B] `saxbla` |
| `pikeman18` | Пикинер 18в. | 1.25 | F30 G2 | saxba2 | — |
| `priest` | Капеллан | 20.00 | F60 G25 | saxtem | — |
| `reiter` | Рейтар | 24.00 | F120 G10 I40 | saxsta | [B] `saxbla` |
| `roundshierdip` | Рундашир (наемник) | 1.50 | G12 | saxdip | [B] `saxaca`, [B] `saxcen` |
| `unitbox` | — | 3.12 | F100 | — | — |
| `yacht` | Яхта | 48.00 | W900 G450 I150 C200 | eurpor | [B] `saxart` |

### `sax` — ключевые апгрейды (с зависимостями)

| sid | имя | Время (g-сек) | цена | требует |
|---|---|---:|---|---|
| `eurcoa.4` | — | 9.4 | F15800 G18500 | [T] `saxcen.1` |
| `eurcoa.5` | — | 9.4 | F19800 G21050 | [T] `saxcen.1` |
| `eurcoa.6` | — | 9.4 | F50200 G25950 | [T] `saxcen.1` |
| `eurgol.4` | — | 9.4 | F15800 G18500 | [T] `saxcen.1` |
| `eurgol.5` | — | 9.4 | F19800 G21050 | [T] `saxcen.1` |
| `eurgol.6` | — | 9.4 | F50200 G25950 | [T] `saxcen.1` |
| `euriro.4` | — | 9.4 | F15800 G18500 | [T] `saxcen.1` |
| `euriro.5` | — | 9.4 | F19800 G21050 | [T] `saxcen.1` |
| `euriro.6` | — | 9.4 | F50200 G25950 | [T] `saxcen.1` |
| `eurpor.1` | — | 46.9 | W20000 G1500 | [B] `saxart` |
| `eurtow.1` | — | 31.2 | G250 | [B] `saxart` |
| `eurtow.2` | — | 31.2 | I350 | [B] `saxart` |
| `eurtow.3` | — | 31.2 | C400 | [B] `saxart` |
| `eurtow.4` | — | 31.2 | I450 | [B] `saxart` |
| `eurtow.5` | — | 31.2 | C500 | [B] `saxart` |
| `ferry.1` | Усовершенствовать конструкцию транспортного судна (+%value% посадочных мест) | 15.6 | F1000 G1250 | [T] `saxcen.1` |
| `saxaca.12` | Улучшить стрелковое оружие: нарезной ствол (сила выстрела +10%) | 15.6 | I5000 | [B] `saxbla` |
| `saxaca.13` | Исследовать гранулированный порох (сила выстрела +10%) | 15.6 | G4000 | [B] `saxbla` |
| `saxaca.14` | Исследовать новые методы очистки серы (сила выстрела +15%) | 15.6 | G7000 | [B] `saxbla` |
| `saxaca.15` | Исследовать новые методы очистки селитры (сила выстрела +25%) | 15.6 | C11000 | [B] `saxbla` |
| `saxaca.16` | Исследовать новые добавки в порох (дальность стрельбы артиллерии +5%) | 15.6 | G2000 I12150 | [B] `saxart` |
| `saxaca.17` | Разработать новые виды стволов: единорог, карронада (дальность стрельбы артиллерии +10%) | 15.6 | S3000 G4550 I19200 | [B] `saxart` |
| `saxaca.18` | Разработать более прочный лафет для орудий: система Грибоваля (прочность пушек +50%) | 15.6 | G500 I3830 C1500 | [B] `saxart` |
| `saxaca.19` | Разработать многоствольное орудие | 15.6 | G1500 C2500 | [B] `saxart` |
| `saxaca.20` | Разработать новые прицельные системы для пушек (меткость стрельбы артиллерии +35%) | 15.6 | W3540 G2000 C7250 | [B] `saxart` |
| `saxaca.21` | Выделить деньги на ремонтные мастерские для пушек (отремонтировать все пушки) | 15.6 | W350 G100 C250 | [B] `saxart` |
| `saxaca.25` | Разработать монгольфьер (открывает всю карту) | 15.6 | G5750 | [T] `saxcen.1` |
| `saxaca.27` | Развивать математику (меткость выстрела орудий +35%) | 15.6 | W9540 G12000 C65200 | [B] `saxart` |
| `saxaca.28` | Разработать новые парусные системы (скорость кораблей +40%) | 15.6 | W65400 G24050 | [B] `eurpor` |
| `saxaca.29` | Разработать новую систему шпангоутов и корпуса корабля (условие для постройки линейных кораблей) | 15.6 | W32300 G6800 I9000 C12800 | [B] `eurpor` |
| `saxaca.30` | Обучить плотников (скорость постройки кораблей увеличивается в 10 раз) | 15.6 | W2300 S42700 G1150 | [B] `eurpor` |
| `saxaca.32` | Разработать кремниевый замок к ружьям (цена мушкета -50%) | 15.6 | G6050 C7750 | [T] `saxcen.1` |
| `saxaca.34` | Разработать новые сорта стали для кирас (защита солдат в доспехах +2) | 15.6 | G9750 | [B] `saxbla` |
| `saxaca.35` | Разработать штык: вставляемый в ствол багинет, штык с трубкой (сила удара холодного оружия +5) | 15.6 | G11500 | [T] `saxcen.1`, [B] `saxbla` |
| `saxaca.36` | Разработать новые сорта стали (эффективность рукопашной атаки мушкетера 18 века и гренадера +25%) | 15.6 | G19500 | [T] `saxcen.1`, [B] `saxbla` |
| `saxaca.5` | Разработать новые снасти и сети для ловли рыбы (эффективность рыбацких лодок +100%) | 15.6 | W12400 G2520 | [B] `eurpor` |
| `saxaca.6` | Разработать новые методы древообработки (условие для постройки фрегатов) | 15.6 | W12400 G7040 | [B] `eurpor` |
| `saxaca.7` | Построить новые верфи для рыбацких лодок (стоимость рыбацкой лодки -85%) | 15.6 | W7300 G1220 | [B] `eurpor` |
| `saxaca.8` | Разработать новые инструменты для древообработки (эффективность добычи дерева +100%) | 15.6 | F5500 G550 | [B] `saxbla` |
| `saxart.cannon.1.1` | — | 10.0 | W1000 S500 G300 | [B] `saxbla` |
| `saxart.cannon.1.2` | — | 10.0 | W3000 S1000 G500 | [B] `saxbla` |
| `saxart.cannon.1.3` | — | 10.0 | W6000 S2000 G1000 | [B] `saxbla` |
| `saxart.cannon.1.4` | — | 15.6 | F1760 G350 | [B] `saxbla` |
| `saxart.cannon.1.5` | — | 15.6 | F1760 G350 | [B] `saxbla` |
| `saxart.cannon.1.6` | — | 15.6 | F1760 G350 | [B] `saxbla` |
| `saxart.cannon.2.1` | — | 10.0 | G500 I1000 | [B] `saxbla` |
| `saxart.cannon.2.2` | — | 10.0 | G1000 I2000 | [B] `saxbla` |
| `saxart.cannon.2.3` | — | 10.0 | G2000 I3000 | [B] `saxbla` |
| `saxart.cannon.2.4` | — | 15.6 | F2560 | [B] `saxbla` |
| `saxart.cannon.2.5` | — | 15.6 | F3560 | [B] `saxbla` |
| `saxart.cannon.2.6` | — | 15.6 | F5560 | [B] `saxbla` |
| `saxart.howitzer.1.1` | — | 10.0 | W1000 S500 G300 | [B] `saxbla` |
| `saxart.howitzer.1.2` | — | 10.0 | W3000 S1000 G500 | [B] `saxbla` |
| `saxart.howitzer.1.3` | — | 10.0 | W6000 S2000 G1000 | [B] `saxbla` |
| `saxart.howitzer.1.4` | — | 15.6 | F1760 G350 | [B] `saxbla` |
| `saxart.howitzer.1.5` | — | 15.6 | F1760 G350 | [B] `saxbla` |
| `saxart.howitzer.1.6` | — | 15.6 | F1760 G350 | [B] `saxbla` |
| `saxart.howitzer.2.1` | — | 10.0 | G500 I1000 | [B] `saxbla` |
| `saxart.howitzer.2.2` | — | 10.0 | G1000 I2000 | [B] `saxbla` |
| `saxart.howitzer.2.3` | — | 10.0 | G2000 I3000 | [B] `saxbla` |
| `saxart.howitzer.2.4` | — | 31.2 | F2560 | [B] `saxbla` |
| `saxart.howitzer.2.5` | — | 31.2 | F3560 | [B] `saxbla` |
| `saxart.howitzer.2.6` | — | 31.2 | F5560 | [B] `saxbla` |
| `saxbar.pikeman.1.6` | — | 15.6 | F15000 G1875 | [B] `saxbla` |
| `saxbar.pikeman.2.6` | — | 15.6 | F11250 G1500 | [B] `saxbla` |
| `saxbla.4` | Выковать штыки и тесаки для пехоты (сила удара мушкетера 18 века и гренадера +5) | 15.6 | W1300 G1500 I900 C5000 | [T] `saxcen.1` |
| `saxcen.1` | — | 9.4 | F30000 G5000 I2000 C2000 | [B] `saxaca`, [B] `saxtem`, [B] `saxart` |

[↑ к содержанию](#содержание)

## SCO — Scotland (Шотландия)

### `sco` — здания

| sid | имя | Время (g-сек) | цена | ферма | требует |
|---|---|---:|---|---:|---|
| `eurcoa` | Шахта | 93.8 | W100 S100 | — | — |
| `eurgol` | Шахта | 93.8 | W100 S100 | — | — |
| `euriro` | Шахта | 93.8 | W100 S100 | — | — |
| `eurmar` | Рынок | 234.4 | W450 | — | [B] `eurmil`, [B] `eursto` |
| `eurmil` | Мельница | 93.8 | W30 S150 | — | — |
| `eurpor` | Порт | 1562.5 | W1600 S800 I400 | — | [B] `eurmar` |
| `eursga` | Каменные ворота | 90.0 | S50 | — | — |
| `eursto` | Склад | 31.2 | W50 S20 | — | [B] `scocen` |
| `eurswa` | Стена | 90.0 | S50 | — | [B] `eursto` |
| `eurtow` | Башня | 1230.3 | W100 S100 G150 | — | [B] `eursto` |
| `scoaca` | Академия | 625.0 | W1250 S1100 | — | [B] `scobar` |
| `scoart` | Артиллерийское депо | 245.9 | W100 S1000 C1400 | — | [B] `scoaca` |
| `scoba2` | Замок | 625.0 | W640 S2400 G2400 | 150 | [B] `scobla` |
| `scobar` | Казарма 17в. | 93.8 | W100 S100 G500 | 150 | [B] `scobla` |
| `scobla` | Кузница | 93.8 | W100 S30 I640 | — | [B] `scocen` |
| `scocen` | Городской центр | 156.2 | W700 S700 | 100 | — |
| `scodip` | Дипломатический центр | 312.5 | W4900 S1700 | — | [B] `scoaca` |
| `scohou` | Дом | 31.2 | W100 S100 | 25 | [B] `scocen` |
| `scosta` | Конюшня | 375.0 | W2350 G800 | — | [B] `scobla` |
| `scotem` | Собор | 156.2 | W1000 S1200 I500 | — | [B] `scocen` |
| `ukrwga` | Деревянные ворота | 5.6 | W10 | — | — |
| `ukrwwa` | Частокол | 5.6 | W10 | — | [B] `eursto` |

### `sco` — юниты

| sid | имя | Время (g-сек) | цена | тренируется в | требует |
|---|---|---:|---|---|---|
| `archerdip` | Лучник (наемник) | 1.25 | G15 | scodip | [B] `scoaca`, [B] `scocen` |
| `archersco` | Лучник кланов | 6.00 | F80 W5 G7 | scoba2 | [B] `scobla` |
| `archerturdip` | Турецкий лучник (наемник) | 1.25 | G15 | scodip | [B] `scoaca`, [B] `scocen` |
| `bagpiper` | Волынщик | 7.00 | F120 G20 | scobar | [B] `scoaca` |
| `battleship` | Линейный корабль | 390.00 | W9000 G3200 I700 C6500 | eurpor | [T] `scoaca.29`, [B] `scoart` |
| `cannon` | Пушка | 75.00 | W250 G400 I400 | scoart | [B] `scobla` |
| `cossacksichdip` | Сечевой козак (наемник) | 2.50 | G60 | scodip | [B] `scoaca`, [B] `scocen` |
| `dragoon18dip` | Драгун 18в. (наемник) | 2.00 | G120 | scodip | [B] `scoaca`, [B] `scocen` |
| `ferry` | Транспорт | 56.00 | W300 G50 I100 | eurpor | [B] `scoart` |
| `fishboat` | Рыбацкая лодка | 40.00 | W600 | eurpor | — |
| `framegun` | Рибадекин | 50.00 | W200 G300 I150 | scoart | [B] `scobla` |
| `frigate` | Фрегат | 230.00 | W5000 G1100 I600 C800 | eurpor | [T] `scoaca.6`, [B] `scoart` |
| `grenadierdip` | Гренадер (наемник) | 1.50 | G25 | scodip | [B] `scoaca`, [B] `scocen` |
| `howitzer` | Гаубица | 94.00 | W250 G350 I300 | scoart | [B] `scobla` |
| `lancersco` | Лансер | 21.00 | F120 G6 | scosta | [B] `scobla` |
| `lightcavalrydip` | Легкий кавалерист (наемник) | 2.00 | G120 | scodip | [B] `scoaca`, [B] `scocen` |
| `lightinfantrydip` | Легкий пехотинец (наемник) | 1.25 | G4 | scodip | [B] `scoaca`, [B] `scocen` |
| `mortar` | Мортира | 25.00 | W100 G75 I200 | scoart | [B] `scobla` |
| `musketeersco` | Мушкетер Ковенанта | 7.00 | F55 G8 I7 | scobar | [B] `scobla` |
| `officersco` | Офицер | 10.00 | F130 G130 I10 | scobar | [B] `scoaca` |
| `peasco` | Крестьянин | 12.50 | F100 | scocen | — |
| `pikemansco` | Пикинер Ковенанта | 4.00 | F35 G2 | scobar | [B] `scobla` |
| `priest` | Капеллан | 20.00 | F60 G25 | scotem | — |
| `raidersco` | Рейдер | 22.50 | F130 G8 I2 | scosta | [B] `scobla` |
| `roundshierdip` | Рундашир (наемник) | 1.50 | G12 | scodip | [B] `scoaca`, [B] `scocen` |
| `swordsmansco` | Мечник кланов | 7.00 | F110 W5 G10 | scoba2 | [B] `scobla` |
| `unitbox` | — | 3.12 | F100 | — | — |
| `yacht` | Яхта | 48.00 | W900 G450 I150 C200 | eurpor | [B] `scoart` |

### `sco` — ключевые апгрейды (с зависимостями)

| sid | имя | Время (g-сек) | цена | требует |
|---|---|---:|---|---|
| `eurcoa.4` | — | 9.4 | F15800 G18500 | [T] `scocen.1` |
| `eurcoa.5` | — | 9.4 | F19800 G21050 | [T] `scocen.1` |
| `eurcoa.6` | — | 9.4 | F50200 G25950 | [T] `scocen.1` |
| `eurgol.4` | — | 9.4 | F15800 G18500 | [T] `scocen.1` |
| `eurgol.5` | — | 9.4 | F19800 G21050 | [T] `scocen.1` |
| `eurgol.6` | — | 9.4 | F50200 G25950 | [T] `scocen.1` |
| `euriro.4` | — | 9.4 | F15800 G18500 | [T] `scocen.1` |
| `euriro.5` | — | 9.4 | F19800 G21050 | [T] `scocen.1` |
| `euriro.6` | — | 9.4 | F50200 G25950 | [T] `scocen.1` |
| `eurpor.1` | — | 46.9 | W20000 G1500 | [B] `scoart` |
| `eurtow.1` | — | 31.2 | G250 | [B] `scoart` |
| `eurtow.2` | — | 31.2 | I350 | [B] `scoart` |
| `eurtow.3` | — | 31.2 | C400 | [B] `scoart` |
| `eurtow.4` | — | 31.2 | I450 | [B] `scoart` |
| `eurtow.5` | — | 31.2 | C500 | [B] `scoart` |
| `ferry.1` | Усовершенствовать конструкцию транспортного судна (+%value% посадочных мест) | 15.6 | F1000 G1250 | [T] `scocen.1` |
| `scoaca.12` | Улучшить стрелковое оружие: нарезной ствол (сила выстрела +10%) | 15.6 | I5000 | [B] `scobla` |
| `scoaca.13` | Исследовать гранулированный порох (сила выстрела +10%) | 15.6 | G4000 | [B] `scobla` |
| `scoaca.14` | Исследовать новые методы очистки серы (сила выстрела +15%) | 15.6 | G7000 | [B] `scobla` |
| `scoaca.15` | Исследовать новые методы очистки селитры (сила выстрела +25%) | 15.6 | C11000 | [B] `scobla` |
| `scoaca.16` | Исследовать новые добавки в порох (дальность стрельбы артиллерии +5%) | 15.6 | G2000 I12150 | [B] `scoart` |
| `scoaca.17` | Разработать новые виды стволов: единорог, карронада (дальность стрельбы артиллерии +10%) | 15.6 | S3000 G4550 I19200 | [B] `scoart` |
| `scoaca.18` | Разработать более прочный лафет для орудий: система Грибоваля (прочность пушек +50%) | 15.6 | G500 I3830 C1500 | [B] `scoart` |
| `scoaca.20` | Разработать новые прицельные системы для пушек (меткость стрельбы артиллерии +35%) | 15.6 | W3540 G2000 C7250 | [B] `scoart` |
| `scoaca.21` | Выделить деньги на ремонтные мастерские для пушек (отремонтировать все пушки) | 15.6 | W350 G100 C250 | [B] `scoart` |
| `scoaca.27` | Развивать математику (меткость выстрела орудий +35%) | 15.6 | W9540 G12000 C65200 | [B] `scoart` |
| `scoaca.28` | Разработать новые парусные системы (скорость кораблей +40%) | 15.6 | W65400 G24050 | [B] `eurpor` |
| `scoaca.29` | Разработать новую систему шпангоутов и корпуса корабля (условие для постройки линейных кораблей) | 15.6 | W32300 G6800 I9000 C12800 | [B] `eurpor` |
| `scoaca.30` | Обучить плотников (скорость постройки кораблей увеличивается в 10 раз) | 15.6 | W2300 S42700 G1150 | [B] `eurpor` |
| `scoaca.32` | Разработать кремниевый замок к ружьям (цена мушкета -50%) | 15.6 | G6050 C7750 | [T] `scocen.1` |
| `scoaca.34` | Разработать новые сорта стали для кирас (защита солдат в доспехах +2) | 15.6 | G9750 | [B] `scobla` |
| `scoaca.35` | Разработать штык: вставляемый в ствол багинет, штык с трубкой (сила удара холодного оружия +5) | 15.6 | G11500 | [T] `scocen.1`, [B] `scobla` |
| `scoaca.36` | Разработать новые сорта стали (эффективность рукопашной атаки мушкетера 18 века и гренадера +25%) | 15.6 | G19500 | [T] `scocen.1`, [B] `scobla` |
| `scoaca.5` | Разработать новые снасти и сети для ловли рыбы (эффективность рыбацких лодок +100%) | 15.6 | W12400 G2520 | [B] `eurpor` |
| `scoaca.6` | Разработать новые методы древообработки (условие для постройки фрегатов) | 15.6 | W12400 G7040 | [B] `eurpor` |
| `scoaca.7` | Построить новые верфи для рыбацких лодок (стоимость рыбацкой лодки -85%) | 15.6 | W7300 G1220 | [B] `eurpor` |
| `scoaca.8` | Разработать новые инструменты для древообработки (эффективность добычи дерева +100%) | 15.6 | F5500 G550 | [B] `scobla` |
| `scoart.cannon.1.1` | — | 10.0 | W1000 S500 G300 | [B] `scobla` |
| `scoart.cannon.1.2` | — | 10.0 | W3000 S1000 G500 | [B] `scobla` |
| `scoart.cannon.1.3` | — | 10.0 | W6000 S2000 G1000 | [B] `scobla` |
| `scoart.cannon.1.4` | — | 15.6 | F1760 G350 | [B] `scobla` |
| `scoart.cannon.1.5` | — | 15.6 | F1760 G350 | [B] `scobla` |
| `scoart.cannon.1.6` | — | 15.6 | F1760 G350 | [B] `scobla` |
| `scoart.cannon.2.1` | — | 10.0 | G500 I1000 | [B] `scobla` |
| `scoart.cannon.2.2` | — | 10.0 | G1000 I2000 | [B] `scobla` |
| `scoart.cannon.2.3` | — | 10.0 | G2000 I3000 | [B] `scobla` |
| `scoart.cannon.2.4` | — | 15.6 | F2560 | [B] `scobla` |
| `scoart.cannon.2.5` | — | 15.6 | F3560 | [B] `scobla` |
| `scoart.cannon.2.6` | — | 15.6 | F5560 | [B] `scobla` |
| `scoart.howitzer.1.1` | — | 10.0 | W1000 S500 G300 | [B] `scobla` |
| `scoart.howitzer.1.2` | — | 10.0 | W3000 S1000 G500 | [B] `scobla` |
| `scoart.howitzer.1.3` | — | 10.0 | W6000 S2000 G1000 | [B] `scobla` |
| `scoart.howitzer.1.4` | — | 15.6 | F1760 G350 | [B] `scobla` |
| `scoart.howitzer.1.5` | — | 15.6 | F1760 G350 | [B] `scobla` |
| `scoart.howitzer.1.6` | — | 15.6 | F1760 G350 | [B] `scobla` |
| `scoart.howitzer.2.1` | — | 10.0 | G500 I1000 | [B] `scobla` |
| `scoart.howitzer.2.2` | — | 10.0 | G1000 I2000 | [B] `scobla` |
| `scoart.howitzer.2.3` | — | 10.0 | G2000 I3000 | [B] `scobla` |
| `scoart.howitzer.2.4` | — | 31.2 | F2560 | [B] `scobla` |
| `scoart.howitzer.2.5` | — | 31.2 | F3560 | [B] `scobla` |
| `scoart.howitzer.2.6` | — | 31.2 | F5560 | [B] `scobla` |
| `scobar.pikemansco.1.6` | — | 15.6 | F22500 G2800 | [B] `scobla` |
| `scobar.pikemansco.2.6` | — | 15.6 | F16875 G2250 | [B] `scobla` |
| `scobla.4` | Выковать штыки и тесаки для пехоты (сила удара мушкетера 18 века и гренадера +5) | 15.6 | W1300 G1500 I900 C5000 | [T] `scocen.1` |
| `scocen.1` | — | 9.4 | F30000 G5000 I2000 C2000 | [B] `scoaca`, [B] `scotem`, [B] `scoart` |

[↑ к содержанию](#содержание)

## SPA — Spain (Испания)

### `spa` — здания

| sid | имя | Время (g-сек) | цена | ферма | требует |
|---|---|---:|---|---:|---|
| `eurcoa` | Шахта | 93.8 | W100 S100 | — | — |
| `eurgol` | Шахта | 93.8 | W100 S100 | — | — |
| `euriro` | Шахта | 93.8 | W100 S100 | — | — |
| `eurmil` | Мельница | 93.8 | W30 S150 | — | — |
| `eurpor` | Порт | 1562.5 | W1600 S800 I400 | — | [B] `spamar` |
| `eursga` | Каменные ворота | 90.0 | S50 | — | — |
| `eurswa` | Стена | 90.0 | S50 | — | [B] `spasto` |
| `eurtow` | Башня | 1230.3 | W100 S100 G150 | — | [B] `spasto` |
| `spaaca` | Академия | 625.0 | W1350 S1000 | — | [B] `spabar` |
| `spaart` | Артиллерийское депо | 245.9 | W100 S1000 C1400 | — | [B] `spaaca` |
| `spaba2` | Казарма 18в. | 5625.0 | W1700 S2950 G4000 | 250 | [T] `spacen.1` |
| `spabar` | Казарма 17в. | 93.8 | W100 S100 G500 | 150 | [B] `spabla` |
| `spabla` | Кузница | 93.8 | W100 S30 I640 | — | [B] `spacen` |
| `spacen` | Городской центр | 156.2 | W700 S700 | 100 | — |
| `spadip` | Дипломатический центр | 312.5 | W4900 S1700 | — | [B] `spaaca` |
| `spahou` | Дом | 31.2 | W100 S100 | 25 | [B] `spacen` |
| `spamar` | Рынок | 156.2 | W450 | — | [B] `eurmil`, [B] `spasto` |
| `spasta` | Конюшня | 625.0 | W2500 S100 G600 | — | [B] `spabla` |
| `spasto` | Склад | 31.2 | W20 S20 | — | [B] `spacen` |
| `spatem` | Собор | 156.2 | W1000 S1200 I500 | — | [B] `spacen` |
| `ukrwga` | Деревянные ворота | 5.6 | W10 | — | — |
| `ukrwwa` | Частокол | 5.6 | W10 | — | [B] `spasto` |

### `spa` — юниты

| sid | имя | Время (g-сек) | цена | тренируется в | требует |
|---|---|---:|---|---|---|
| `archerdip` | Лучник (наемник) | 1.25 | G15 | spadip | [B] `spaaca`, [B] `spacen` |
| `archerturdip` | Турецкий лучник (наемник) | 1.25 | G15 | spadip | [B] `spaaca`, [B] `spacen` |
| `battleship` | Линейный корабль | 390.00 | W9000 G3200 I700 C6500 | eurpor | [T] `spaaca.29`, [B] `spaart` |
| `cannon` | Пушка | 75.00 | W250 G400 I400 | spaart | [B] `spabla` |
| `cossacksichdip` | Сечевой козак (наемник) | 2.50 | G60 | spadip | [B] `spaaca`, [B] `spacen` |
| `cuirassier` | Кирасир | 22.50 | F120 G35 I25 | spasta | [B] `spabla`, [T] `spacen.1` |
| `dragoon` | Драгун 17в. | 15.00 | F90 G7 I5 | spasta | [B] `spabla` |
| `dragoon18` | Драгун 18в. | 22.50 | F70 G60 I7 | spasta | [B] `spabla`, [T] `spacen.1` |
| `dragoon18dip` | Драгун 18в. (наемник) | 2.00 | G120 | spadip | [B] `spaaca`, [B] `spacen` |
| `drummer` | Барабанщик 17в. | 5.00 | F60 G20 | spabar | [B] `spaaca` |
| `drummer18` | Барабанщик 18в. | 6.00 | F50 G30 | spaba2 | [B] `spaaca` |
| `ferry` | Транспорт | 56.00 | W300 G50 I100 | eurpor | [B] `spaart` |
| `fishboat` | Рыбацкая лодка | 40.00 | W600 | eurpor | — |
| `frigate` | Фрегат | 230.00 | W5000 G1100 I600 C800 | eurpor | [T] `spaaca.6`, [B] `spaart` |
| `galley` | Галера | 50.00 | W9500 G900 I800 | eurpor | [B] `spaart` |
| `grenadier` | Гренадер | 6.00 | F80 G60 I40 | spaba2 | [B] `spabla` |
| `grenadierdip` | Гренадер (наемник) | 1.50 | G25 | spadip | [B] `spaaca`, [B] `spacen` |
| `howitzer` | Гаубица | 94.00 | W250 G350 I300 | spaart | [B] `spabla` |
| `hussar` | Гусар | 15.00 | F70 G20 I2 | spasta | [B] `spabla`, [T] `spacen.1` |
| `lightcavalrydip` | Легкий кавалерист (наемник) | 2.00 | G120 | spadip | [B] `spaaca`, [B] `spacen` |
| `lightinfantrydip` | Легкий пехотинец (наемник) | 1.25 | G4 | spadip | [B] `spaaca`, [B] `spacen` |
| `mortar` | Мортира | 25.00 | W100 G75 I200 | spaart | [B] `spabla` |
| `multicannon` | Многоствольное орудие | 50.00 | W200 G400 I250 | spaart | [T] `spaaca.19`, [B] `spabla` |
| `musketeer18` | Мушкетер 18в. | 4.50 | F50 G40 I40 | spaba2 | [B] `spabla` |
| `musketeerspa` | Мушкетер 17в. | 7.50 | F40 G12 I20 | spabar | [B] `spabla` |
| `officer` | Офицер 17в. | 10.00 | F50 G150 I30 | spabar | [B] `spaaca` |
| `officer18` | Офицер 18в. | 6.00 | F50 G200 I10 | spaba2 | [B] `spaaca` |
| `peaspa` | Крестьянин | 12.50 | F100 | spacen | — |
| `pikeman` | Пикинер 17в. | 5.50 | F35 G7 I30 | spabar | [B] `spabla` |
| `pikeman18` | Пикинер 18в. | 1.25 | F30 G2 | spaba2 | — |
| `pikemanspa` | Коселет | 5.50 | F35 G7 I30 | spabar | [B] `spabla` |
| `priest` | Капеллан | 20.00 | F60 G25 | spatem | — |
| `reiter` | Рейтар | 24.00 | F120 G10 I40 | spasta | [B] `spabla` |
| `roundshierdip` | Рундашир (наемник) | 1.50 | G12 | spadip | [B] `spaaca`, [B] `spacen` |
| `unitbox` | — | 3.12 | F100 | — | — |
| `yacht` | Яхта | 48.00 | W900 G450 I150 C200 | eurpor | [B] `spaart` |

### `spa` — ключевые апгрейды (с зависимостями)

| sid | имя | Время (g-сек) | цена | требует |
|---|---|---:|---|---|
| `eurcoa.4` | — | 9.4 | F15800 G18500 | [T] `spacen.1` |
| `eurcoa.5` | — | 9.4 | F19800 G21050 | [T] `spacen.1` |
| `eurcoa.6` | — | 9.4 | F50200 G25950 | [T] `spacen.1` |
| `eurgol.4` | — | 9.4 | F15800 G18500 | [T] `spacen.1` |
| `eurgol.5` | — | 9.4 | F19800 G21050 | [T] `spacen.1` |
| `eurgol.6` | — | 9.4 | F50200 G25950 | [T] `spacen.1` |
| `euriro.4` | — | 9.4 | F15800 G18500 | [T] `spacen.1` |
| `euriro.5` | — | 9.4 | F19800 G21050 | [T] `spacen.1` |
| `euriro.6` | — | 9.4 | F50200 G25950 | [T] `spacen.1` |
| `eurpor.1` | — | 46.9 | W20000 G1500 | [B] `spaart` |
| `eurtow.1` | — | 31.2 | G250 | [B] `spaart` |
| `eurtow.2` | — | 31.2 | I350 | [B] `spaart` |
| `eurtow.3` | — | 31.2 | C400 | [B] `spaart` |
| `eurtow.4` | — | 31.2 | I450 | [B] `spaart` |
| `eurtow.5` | — | 31.2 | C500 | [B] `spaart` |
| `ferry.1` | Усовершенствовать конструкцию транспортного судна (+%value% посадочных мест) | 15.6 | F1000 G1250 | [T] `spacen.1` |
| `spaaca.12` | Улучшить стрелковое оружие: нарезной ствол (сила выстрела +10%) | 15.6 | I5000 | [B] `spabla` |
| `spaaca.13` | Исследовать гранулированный порох (сила выстрела +10%) | 15.6 | G4000 | [B] `spabla` |
| `spaaca.14` | Исследовать новые методы очистки серы (сила выстрела +15%) | 15.6 | G7000 | [B] `spabla` |
| `spaaca.15` | Исследовать новые методы очистки селитры (сила выстрела +25%) | 15.6 | C11000 | [B] `spabla` |
| `spaaca.16` | Исследовать новые добавки в порох (дальность стрельбы артиллерии +5%) | 15.6 | G2000 I12150 | [B] `spaart` |
| `spaaca.17` | Разработать новые виды стволов: единорог, карронада (дальность стрельбы артиллерии +10%) | 15.6 | S3000 G4550 I19200 | [B] `spaart` |
| `spaaca.18` | Разработать более прочный лафет для орудий: система Грибоваля (прочность пушек +50%) | 15.6 | G500 I3830 C1500 | [B] `spaart` |
| `spaaca.19` | Разработать многоствольное орудие | 15.6 | G1500 C2500 | [B] `spaart` |
| `spaaca.20` | Разработать новые прицельные системы для пушек (меткость стрельбы артиллерии +35%) | 15.6 | W3540 G2000 C7250 | [B] `spaart` |
| `spaaca.21` | Выделить деньги на ремонтные мастерские для пушек (отремонтировать все пушки) | 15.6 | W350 G100 C250 | [B] `spaart` |
| `spaaca.25` | Разработать монгольфьер (открывает всю карту) | 15.6 | G5750 | [T] `spacen.1` |
| `spaaca.27` | Развивать математику (меткость выстрела орудий +35%) | 15.6 | W9540 G12000 C65200 | [B] `spaart` |
| `spaaca.28` | Разработать новые парусные системы (скорость кораблей +40%) | 15.6 | W65400 G24050 | [B] `eurpor` |
| `spaaca.29` | Разработать новую систему шпангоутов и корпуса корабля (условие для постройки линейных кораблей) | 15.6 | W32300 G6800 I9000 C12800 | [B] `eurpor` |
| `spaaca.30` | Обучить плотников (скорость постройки кораблей увеличивается в 10 раз) | 15.6 | W2300 S42700 G1150 | [B] `eurpor` |
| `spaaca.32` | Разработать кремниевый замок к ружьям (цена мушкета -50%) | 15.6 | G6050 C7750 | [T] `spacen.1` |
| `spaaca.34` | Разработать новые сорта стали для кирас (защита солдат в доспехах +2) | 15.6 | G9750 | [B] `spabla` |
| `spaaca.35` | Разработать штык: вставляемый в ствол багинет, штык с трубкой (сила удара холодного оружия +5) | 15.6 | G11500 | [T] `spacen.1`, [B] `spabla` |
| `spaaca.36` | Разработать новые сорта стали (эффективность рукопашной атаки мушкетера 18 века и гренадера +25%) | 15.6 | G19500 | [T] `spacen.1`, [B] `spabla` |
| `spaaca.5` | Разработать новые снасти и сети для ловли рыбы (эффективность рыбацких лодок +100%) | 15.6 | W12400 G2520 | [B] `eurpor` |
| `spaaca.6` | Разработать новые методы древообработки (условие для постройки фрегатов) | 15.6 | W12400 G7040 | [B] `eurpor` |
| `spaaca.7` | Построить новые верфи для рыбацких лодок (стоимость рыбацкой лодки -85%) | 15.6 | W7300 G1220 | [B] `eurpor` |
| `spaaca.8` | Разработать новые инструменты для древообработки (эффективность добычи дерева +100%) | 15.6 | F5500 G550 | [B] `spabla` |
| `spaart.cannon.1.1` | — | 10.0 | W1000 S500 G300 | [B] `spabla` |
| `spaart.cannon.1.2` | — | 10.0 | W3000 S1000 G500 | [B] `spabla` |
| `spaart.cannon.1.3` | — | 10.0 | W6000 S2000 G1000 | [B] `spabla` |
| `spaart.cannon.1.4` | — | 15.6 | F1760 G350 | [B] `spabla` |
| `spaart.cannon.1.5` | — | 15.6 | F1760 G350 | [B] `spabla` |
| `spaart.cannon.1.6` | — | 15.6 | F1760 G350 | [B] `spabla` |
| `spaart.cannon.2.1` | — | 10.0 | G500 I1000 | [B] `spabla` |
| `spaart.cannon.2.2` | — | 10.0 | G1000 I2000 | [B] `spabla` |
| `spaart.cannon.2.3` | — | 10.0 | G2000 I3000 | [B] `spabla` |
| `spaart.cannon.2.4` | — | 15.6 | F2560 | [B] `spabla` |
| `spaart.cannon.2.5` | — | 15.6 | F3560 | [B] `spabla` |
| `spaart.cannon.2.6` | — | 15.6 | F5560 | [B] `spabla` |
| `spaart.howitzer.1.1` | — | 10.0 | W1000 S500 G300 | [B] `spabla` |
| `spaart.howitzer.1.2` | — | 10.0 | W3000 S1000 G500 | [B] `spabla` |
| `spaart.howitzer.1.3` | — | 10.0 | W6000 S2000 G1000 | [B] `spabla` |
| `spaart.howitzer.1.4` | — | 15.6 | F1760 G350 | [B] `spabla` |
| `spaart.howitzer.1.5` | — | 15.6 | F1760 G350 | [B] `spabla` |
| `spaart.howitzer.1.6` | — | 15.6 | F1760 G350 | [B] `spabla` |
| `spaart.howitzer.2.1` | — | 10.0 | G500 I1000 | [B] `spabla` |
| `spaart.howitzer.2.2` | — | 10.0 | G1000 I2000 | [B] `spabla` |
| `spaart.howitzer.2.3` | — | 10.0 | G2000 I3000 | [B] `spabla` |
| `spaart.howitzer.2.4` | — | 31.2 | F2560 | [B] `spabla` |
| `spaart.howitzer.2.5` | — | 31.2 | F3560 | [B] `spabla` |
| `spaart.howitzer.2.6` | — | 31.2 | F5560 | [B] `spabla` |
| `spabar.pikeman.1.6` | — | 15.6 | F15000 G1875 | [B] `spabla` |
| `spabar.pikeman.2.6` | — | 15.6 | F11250 G1500 | [B] `spabla` |
| `spabla.4` | Выковать штыки и тесаки для пехоты (сила удара мушкетера 18 века и гренадера +5) | 15.6 | W1300 G1500 I900 C5000 | [T] `spacen.1` |
| `spacen.1` | — | 9.4 | F30000 G5000 I2000 C2000 | [B] `spaaca`, [B] `spatem`, [B] `spaart` |

[↑ к содержанию](#содержание)

## SWE — Sweden (Швеция)

### `swe` — здания

| sid | имя | Время (g-сек) | цена | ферма | требует |
|---|---|---:|---|---:|---|
| `eurcoa` | Шахта | 93.8 | W100 S100 | — | — |
| `eurgol` | Шахта | 93.8 | W100 S100 | — | — |
| `euriro` | Шахта | 93.8 | W100 S100 | — | — |
| `eurmar` | Рынок | 234.4 | W450 | — | [B] `eurmil`, [B] `eursto` |
| `eurmil` | Мельница | 93.8 | W30 S150 | — | — |
| `eurpor` | Порт | 1562.5 | W1600 S800 I400 | — | [B] `eurmar` |
| `eursga` | Каменные ворота | 90.0 | S50 | — | — |
| `eursto` | Склад | 31.2 | W50 S20 | — | [B] `swecen` |
| `eurswa` | Стена | 90.0 | S50 | — | [B] `eursto` |
| `eurtow` | Башня | 1230.3 | W100 S100 G150 | — | [B] `eursto` |
| `sweaca` | Академия | 625.0 | W1350 S1000 | — | [B] `swebar` |
| `sweart` | Артиллерийское депо | 245.9 | W100 S1000 C1400 | — | [B] `sweaca` |
| `sweba2` | Казарма 18в. | 5625.0 | W1700 S2950 G4000 | 250 | [T] `swecen.1` |
| `swebar` | Казарма 17в. | 93.8 | W100 S100 G500 | 150 | [B] `swebla` |
| `swebla` | Кузница | 93.8 | W100 S30 I640 | — | [B] `swecen` |
| `swecen` | Городской центр | 156.2 | W700 S700 | 100 | — |
| `swedip` | Дипломатический центр | 312.5 | W4900 S1700 | — | [B] `sweaca` |
| `swehou` | Дом | 31.2 | W100 S100 | 25 | [B] `swecen` |
| `swesta` | Конюшня | 625.0 | W2500 S100 G600 | — | [B] `swebla` |
| `swetem` | Собор | 156.2 | W1000 S1200 I500 | — | [B] `swecen` |
| `ukrwga` | Деревянные ворота | 5.6 | W10 | — | — |
| `ukrwwa` | Частокол | 5.6 | W10 | — | [B] `eursto` |

### `swe` — юниты

| sid | имя | Время (g-сек) | цена | тренируется в | требует |
|---|---|---:|---|---|---|
| `archerdip` | Лучник (наемник) | 1.25 | G15 | swedip | [B] `sweaca`, [B] `swecen` |
| `archerturdip` | Турецкий лучник (наемник) | 1.25 | G15 | swedip | [B] `sweaca`, [B] `swecen` |
| `battleship` | Линейный корабль | 390.00 | W9000 G3200 I700 C6500 | eurpor | [T] `sweaca.29`, [B] `sweart` |
| `cannon` | Пушка | 75.00 | W250 G400 I400 | sweart | [B] `swebla` |
| `cossacksichdip` | Сечевой козак (наемник) | 2.50 | G60 | swedip | [B] `sweaca`, [B] `swecen` |
| `cuirassier` | Кирасир | 22.50 | F120 G35 I25 | swesta | [B] `swebla`, [T] `swecen.1` |
| `dragoon` | Драгун 17в. | 15.00 | F90 G7 I5 | swesta | [B] `swebla` |
| `dragoon18` | Драгун 18в. | 22.50 | F70 G60 I7 | swesta | [B] `swebla`, [T] `swecen.1` |
| `dragoon18dip` | Драгун 18в. (наемник) | 2.00 | G120 | swedip | [B] `sweaca`, [B] `swecen` |
| `drummer` | Барабанщик 17в. | 5.00 | F60 G20 | swebar | [B] `sweaca` |
| `drummer18` | Барабанщик 18в. | 6.00 | F50 G30 | sweba2 | [B] `sweaca` |
| `ferry` | Транспорт | 56.00 | W300 G50 I100 | eurpor | [B] `sweart` |
| `fishboat` | Рыбацкая лодка | 40.00 | W600 | eurpor | — |
| `frigate` | Фрегат | 230.00 | W5000 G1100 I600 C800 | eurpor | [T] `sweaca.6`, [B] `sweart` |
| `galley` | Галера | 50.00 | W9500 G900 I800 | eurpor | [B] `sweart` |
| `grenadier` | Гренадер | 6.00 | F80 G60 I40 | sweba2 | [B] `swebla` |
| `grenadierdip` | Гренадер (наемник) | 1.50 | G25 | swedip | [B] `sweaca`, [B] `swecen` |
| `hackapell` | Гаккапелит | 18.00 | F80 G7 I2 | swesta | [B] `swebla` |
| `howitzer` | Гаубица | 94.00 | W250 G350 I300 | sweart | [B] `swebla` |
| `hussar` | Гусар | 15.00 | F70 G20 I2 | swesta | [B] `swebla`, [T] `swecen.1` |
| `lightcavalrydip` | Легкий кавалерист (наемник) | 2.00 | G120 | swedip | [B] `sweaca`, [B] `swecen` |
| `lightinfantrydip` | Легкий пехотинец (наемник) | 1.25 | G4 | swedip | [B] `sweaca`, [B] `swecen` |
| `mortar` | Мортира | 25.00 | W100 G75 I200 | sweart | [B] `swebla` |
| `multicannon` | Многоствольное орудие | 50.00 | W200 G400 I250 | sweart | [T] `sweaca.19`, [B] `swebla` |
| `musketeer` | Мушкетер 17в. | 6.00 | F45 G6 I5 | swebar | [B] `swebla` |
| `musketeer18` | Мушкетер 18в. | 4.50 | F50 G40 I40 | sweba2 | [B] `swebla` |
| `officer` | Офицер 17в. | 10.00 | F50 G150 I30 | swebar | [B] `sweaca` |
| `officer18` | Офицер 18в. | 6.00 | F50 G200 I10 | sweba2 | [B] `sweaca` |
| `peaeng` | Крестьянин | 12.50 | F100 | swecen | — |
| `pikeman` | Пикинер 17в. | 4.50 | F25 G3 I20 | swebar | [B] `swebla` |
| `pikeman18swe` | Пикинер 18в. | 1.50 | F40 G3 | sweba2 | — |
| `priest` | Капеллан | 20.00 | F60 G25 | swetem | — |
| `reiterswe` | Шведский рейтар | 22.50 | F130 G7 I20 | swesta | [B] `swebla` |
| `roundshierdip` | Рундашир (наемник) | 1.50 | G12 | swedip | [B] `sweaca`, [B] `swecen` |
| `unitbox` | — | 3.12 | F100 | — | — |
| `yacht` | Яхта | 48.00 | W900 G450 I150 C200 | eurpor | [B] `sweart` |

### `swe` — ключевые апгрейды (с зависимостями)

| sid | имя | Время (g-сек) | цена | требует |
|---|---|---:|---|---|
| `eurcoa.4` | — | 9.4 | F15800 G18500 | [T] `swecen.1` |
| `eurcoa.5` | — | 9.4 | F19800 G21050 | [T] `swecen.1` |
| `eurcoa.6` | — | 9.4 | F50200 G25950 | [T] `swecen.1` |
| `eurgol.4` | — | 9.4 | F15800 G18500 | [T] `swecen.1` |
| `eurgol.5` | — | 9.4 | F19800 G21050 | [T] `swecen.1` |
| `eurgol.6` | — | 9.4 | F50200 G25950 | [T] `swecen.1` |
| `euriro.4` | — | 9.4 | F15800 G18500 | [T] `swecen.1` |
| `euriro.5` | — | 9.4 | F19800 G21050 | [T] `swecen.1` |
| `euriro.6` | — | 9.4 | F50200 G25950 | [T] `swecen.1` |
| `eurpor.1` | — | 46.9 | W20000 G1500 | [B] `sweart` |
| `eurtow.1` | — | 31.2 | G250 | [B] `sweart` |
| `eurtow.2` | — | 31.2 | I350 | [B] `sweart` |
| `eurtow.3` | — | 31.2 | C400 | [B] `sweart` |
| `eurtow.4` | — | 31.2 | I450 | [B] `sweart` |
| `eurtow.5` | — | 31.2 | C500 | [B] `sweart` |
| `ferry.1` | Усовершенствовать конструкцию транспортного судна (+%value% посадочных мест) | 15.6 | F1000 G1250 | [T] `swecen.1` |
| `sweaca.12` | Улучшить стрелковое оружие: нарезной ствол (сила выстрела +10%) | 15.6 | I5000 | [B] `swebla` |
| `sweaca.13` | Исследовать гранулированный порох (сила выстрела +10%) | 15.6 | G4000 | [B] `swebla` |
| `sweaca.14` | Исследовать новые методы очистки серы (сила выстрела +15%) | 15.6 | G7000 | [B] `swebla` |
| `sweaca.15` | Исследовать новые методы очистки селитры (сила выстрела +25%) | 15.6 | C11000 | [B] `swebla` |
| `sweaca.16` | Исследовать новые добавки в порох (дальность стрельбы артиллерии +5%) | 15.6 | G2000 I12150 | [B] `sweart` |
| `sweaca.17` | Разработать новые виды стволов: единорог, карронада (дальность стрельбы артиллерии +10%) | 15.6 | S3000 G4550 I19200 | [B] `sweart` |
| `sweaca.18` | Разработать более прочный лафет для орудий: система Грибоваля (прочность пушек +50%) | 15.6 | G500 I3830 C1500 | [B] `sweart` |
| `sweaca.19` | Разработать многоствольное орудие | 15.6 | G1500 C2500 | [B] `sweart` |
| `sweaca.20` | Разработать новые прицельные системы для пушек (меткость стрельбы артиллерии +35%) | 15.6 | W3540 G2000 C7250 | [B] `sweart` |
| `sweaca.21` | Выделить деньги на ремонтные мастерские для пушек (отремонтировать все пушки) | 15.6 | W350 G100 C250 | [B] `sweart` |
| `sweaca.25` | Разработать монгольфьер (открывает всю карту) | 15.6 | G5750 | [T] `swecen.1` |
| `sweaca.27` | Развивать математику (меткость выстрела орудий +35%) | 15.6 | W9540 G12000 C65200 | [B] `sweart` |
| `sweaca.28` | Разработать новые парусные системы (скорость кораблей +40%) | 15.6 | W65400 G24050 | [B] `eurpor` |
| `sweaca.29` | Разработать новую систему шпангоутов и корпуса корабля (условие для постройки линейных кораблей) | 15.6 | W32300 G6800 I9000 C12800 | [B] `eurpor` |
| `sweaca.30` | Обучить плотников (скорость постройки кораблей увеличивается в 10 раз) | 15.6 | W2300 S42700 G1150 | [B] `eurpor` |
| `sweaca.32` | Разработать кремниевый замок к ружьям (цена мушкета -50%) | 15.6 | G6050 C7750 | [T] `swecen.1` |
| `sweaca.34` | Разработать новые сорта стали для кирас (защита солдат в доспехах +2) | 15.6 | G9750 | [B] `swebla` |
| `sweaca.35` | Разработать штык: вставляемый в ствол багинет, штык с трубкой (сила удара холодного оружия +5) | 15.6 | G11500 | [T] `swecen.1`, [B] `swebla` |
| `sweaca.36` | Разработать новые сорта стали (эффективность рукопашной атаки мушкетера 18 века и гренадера +25%) | 15.6 | G19500 | [T] `swecen.1`, [B] `swebla` |
| `sweaca.5` | Разработать новые снасти и сети для ловли рыбы (эффективность рыбацких лодок +100%) | 15.6 | W12400 G2520 | [B] `eurpor` |
| `sweaca.6` | Разработать новые методы древообработки (условие для постройки фрегатов) | 15.6 | W12400 G7040 | [B] `eurpor` |
| `sweaca.7` | Построить новые верфи для рыбацких лодок (стоимость рыбацкой лодки -85%) | 15.6 | W7300 G1220 | [B] `eurpor` |
| `sweaca.8` | Разработать новые инструменты для древообработки (эффективность добычи дерева +100%) | 15.6 | F5500 G550 | [B] `swebla` |
| `sweart.cannon.1.1` | — | 10.0 | W1000 S500 G300 | [B] `swebla` |
| `sweart.cannon.1.2` | — | 10.0 | W3000 S1000 G500 | [B] `swebla` |
| `sweart.cannon.1.3` | — | 10.0 | W6000 S2000 G1000 | [B] `swebla` |
| `sweart.cannon.1.4` | — | 15.6 | F1760 G350 | [B] `swebla` |
| `sweart.cannon.1.5` | — | 15.6 | F1760 G350 | [B] `swebla` |
| `sweart.cannon.1.6` | — | 15.6 | F1760 G350 | [B] `swebla` |
| `sweart.cannon.2.1` | — | 10.0 | G500 I1000 | [B] `swebla` |
| `sweart.cannon.2.2` | — | 10.0 | G1000 I2000 | [B] `swebla` |
| `sweart.cannon.2.3` | — | 10.0 | G2000 I3000 | [B] `swebla` |
| `sweart.cannon.2.4` | — | 15.6 | F2560 | [B] `swebla` |
| `sweart.cannon.2.5` | — | 15.6 | F3560 | [B] `swebla` |
| `sweart.cannon.2.6` | — | 15.6 | F5560 | [B] `swebla` |
| `sweart.howitzer.1.1` | — | 10.0 | W1000 S500 G300 | [B] `swebla` |
| `sweart.howitzer.1.2` | — | 10.0 | W3000 S1000 G500 | [B] `swebla` |
| `sweart.howitzer.1.3` | — | 10.0 | W6000 S2000 G1000 | [B] `swebla` |
| `sweart.howitzer.1.4` | — | 15.6 | F1760 G350 | [B] `swebla` |
| `sweart.howitzer.1.5` | — | 15.6 | F1760 G350 | [B] `swebla` |
| `sweart.howitzer.1.6` | — | 15.6 | F1760 G350 | [B] `swebla` |
| `sweart.howitzer.2.1` | — | 10.0 | G500 I1000 | [B] `swebla` |
| `sweart.howitzer.2.2` | — | 10.0 | G1000 I2000 | [B] `swebla` |
| `sweart.howitzer.2.3` | — | 10.0 | G2000 I3000 | [B] `swebla` |
| `sweart.howitzer.2.4` | — | 31.2 | F2560 | [B] `swebla` |
| `sweart.howitzer.2.5` | — | 31.2 | F3560 | [B] `swebla` |
| `sweart.howitzer.2.6` | — | 31.2 | F5560 | [B] `swebla` |
| `swebar.pikeman.1.6` | — | 15.6 | F15000 G1875 | [B] `swebla` |
| `swebar.pikeman.2.6` | — | 15.6 | F11250 G1500 | [B] `swebla` |
| `swebla.4` | Выковать штыки и тесаки для пехоты (сила удара мушкетера 18 века и гренадера +5) | 15.6 | W1300 G1500 I900 C5000 | [T] `swecen.1` |
| `swecen.1` | — | 9.4 | F37000 G5500 I1500 C1500 | [B] `sweaca`, [B] `swetem`, [B] `sweart` |

[↑ к содержанию](#содержание)

## SWI — Switzerland (Швейцария)

### `swi` — здания

| sid | имя | Время (g-сек) | цена | ферма | требует |
|---|---|---:|---|---:|---|
| `eurcoa` | Шахта | 93.8 | W100 S100 | — | — |
| `eurgol` | Шахта | 93.8 | W100 S100 | — | — |
| `euriro` | Шахта | 93.8 | W100 S100 | — | — |
| `eurmar` | Рынок | 234.4 | W450 | — | [B] `eurmil`, [B] `eursto` |
| `eurmil` | Мельница | 93.8 | W30 S150 | — | — |
| `eurpor` | Порт | 1562.5 | W1600 S800 I400 | — | [B] `eurmar` |
| `eursga` | Каменные ворота | 90.0 | S50 | — | — |
| `eursto` | Склад | 31.2 | W50 S20 | — | [B] `swicen` |
| `eurswa` | Стена | 90.0 | S50 | — | [B] `eursto` |
| `eurtow` | Башня | 1230.3 | W100 S100 G150 | — | [B] `eursto` |
| `swiaca` | Академия | 625.0 | W1250 S1100 | — | [B] `swibar` |
| `swiart` | Артиллерийское депо | 245.9 | W100 S1000 C1400 | — | [B] `swiaca` |
| `swiba2` | Казарма 18в. | 5625.0 | W1700 S2950 G4000 | 250 | [T] `swicen.1` |
| `swibar` | Казарма 17в. | 93.8 | W100 S100 G500 | 150 | [B] `swibla` |
| `swibla` | Кузница | 93.8 | W100 S30 I640 | — | [B] `swicen` |
| `swicen` | Городской центр | 156.2 | W700 S700 | 100 | — |
| `swidip` | Дипломатический центр | 312.5 | W4900 S1700 | — | [B] `swiaca` |
| `swihou` | Дом | 31.2 | W100 S100 | 25 | [B] `swicen` |
| `swista` | Конюшня | 625.0 | W2500 S100 G600 | — | [B] `swibla` |
| `switem` | Собор | 156.2 | W1000 S1200 I500 | — | [B] `swicen` |
| `ukrwga` | Деревянные ворота | 5.6 | W10 | — | — |
| `ukrwwa` | Частокол | 5.6 | W10 | — | [B] `eursto` |

### `swi` — юниты

| sid | имя | Время (g-сек) | цена | тренируется в | требует |
|---|---|---:|---|---|---|
| `archerdip` | Лучник (наемник) | 1.25 | G15 | swidip | [B] `swiaca`, [B] `swicen` |
| `archerturdip` | Турецкий лучник (наемник) | 1.25 | G15 | swidip | [B] `swiaca`, [B] `swicen` |
| `battleship` | Линейный корабль | 390.00 | W9000 G3200 I700 C6500 | eurpor | [T] `swiaca.29`, [B] `swiart` |
| `cannon` | Пушка | 75.00 | W250 G400 I400 | swiart | [B] `swibla` |
| `cossacksichdip` | Сечевой козак (наемник) | 2.50 | G60 | swidip | [B] `swiaca`, [B] `swicen` |
| `cuirassier` | Кирасир | 22.50 | F120 G35 I25 | swista | [B] `swibla`, [T] `swicen.1` |
| `dragoon` | Драгун 17в. | 15.00 | F90 G7 I5 | swista | [B] `swibla` |
| `dragoon18` | Драгун 18в. | 22.50 | F70 G60 I7 | swista | [B] `swibla`, [T] `swicen.1` |
| `dragoon18dip` | Драгун 18в. (наемник) | 2.00 | G120 | swidip | [B] `swiaca`, [B] `swicen` |
| `drummer` | Барабанщик 17в. | 5.00 | F60 G20 | swibar | [B] `swiaca` |
| `drummer18` | Барабанщик 18в. | 6.00 | F50 G30 | swiba2 | [B] `swiaca` |
| `ferry` | Транспорт | 56.00 | W300 G50 I100 | eurpor | [B] `swiart` |
| `fishboat` | Рыбацкая лодка | 40.00 | W600 | eurpor | — |
| `frigate` | Фрегат | 230.00 | W5000 G1100 I600 C800 | eurpor | [T] `swiaca.6`, [B] `swiart` |
| `galley` | Галера | 50.00 | W9500 G900 I800 | eurpor | [B] `swiart` |
| `grenadier` | Гренадер | 6.00 | F80 G60 I40 | swiba2 | [B] `swibla` |
| `grenadierdip` | Гренадер (наемник) | 1.50 | G25 | swidip | [B] `swiaca`, [B] `swicen` |
| `howitzer` | Гаубица | 94.00 | W250 G350 I300 | swiart | [B] `swibla` |
| `hussarswi` | Конный егерь | 19.50 | F120 G30 I2 | swista | [B] `swibla`, [T] `swicen.1` |
| `jagerswi` | Егерь | 8.50 | F40 G70 I20 | swiba2 | [B] `swibla` |
| `lightcavalrydip` | Легкий кавалерист (наемник) | 2.00 | G120 | swidip | [B] `swiaca`, [B] `swicen` |
| `lightinfantrydip` | Легкий пехотинец (наемник) | 1.25 | G4 | swidip | [B] `swiaca`, [B] `swicen` |
| `mortar` | Мортира | 25.00 | W100 G75 I200 | swiart | [B] `swibla` |
| `multicannon` | Многоствольное орудие | 50.00 | W200 G400 I250 | swiart | [T] `swiaca.19`, [B] `swibla` |
| `musketeer` | Мушкетер 17в. | 6.00 | F45 G6 I5 | swibar | [B] `swibla` |
| `musketeer18` | Мушкетер 18в. | 4.50 | F50 G40 I40 | swiba2 | [B] `swibla` |
| `officer` | Офицер 17в. | 10.00 | F50 G150 I30 | swibar | [B] `swiaca` |
| `officer18` | Офицер 18в. | 6.00 | F50 G200 I10 | swiba2 | [B] `swiaca` |
| `peaaus` | Крестьянин | 12.50 | F100 | swicen | — |
| `pikeman18` | Пикинер 18в. | 1.25 | F30 G2 | swiba2 | — |
| `pikemanswi` | Пикинер 17в. | 5.00 | F40 G6 I20 | swibar | [B] `swibla` |
| `priest` | Капеллан | 20.00 | F60 G25 | switem | — |
| `reiter` | Рейтар | 24.00 | F120 G10 I40 | swista | [B] `swibla` |
| `roundshierdip` | Рундашир (наемник) | 1.50 | G12 | swidip | [B] `swiaca`, [B] `swicen` |
| `unitbox` | — | 3.12 | F100 | — | — |
| `yacht` | Яхта | 48.00 | W900 G450 I150 C200 | eurpor | [B] `swiart` |

### `swi` — ключевые апгрейды (с зависимостями)

| sid | имя | Время (g-сек) | цена | требует |
|---|---|---:|---|---|
| `eurcoa.4` | — | 9.4 | F15800 G18500 | [T] `swicen.1` |
| `eurcoa.5` | — | 9.4 | F19800 G21050 | [T] `swicen.1` |
| `eurcoa.6` | — | 9.4 | F50200 G25950 | [T] `swicen.1` |
| `eurgol.4` | — | 9.4 | F15800 G18500 | [T] `swicen.1` |
| `eurgol.5` | — | 9.4 | F19800 G21050 | [T] `swicen.1` |
| `eurgol.6` | — | 9.4 | F50200 G25950 | [T] `swicen.1` |
| `euriro.4` | — | 9.4 | F15800 G18500 | [T] `swicen.1` |
| `euriro.5` | — | 9.4 | F19800 G21050 | [T] `swicen.1` |
| `euriro.6` | — | 9.4 | F50200 G25950 | [T] `swicen.1` |
| `eurpor.1` | — | 46.9 | W20000 G1500 | [B] `swiart` |
| `eurtow.1` | — | 31.2 | G250 | [B] `swiart` |
| `eurtow.2` | — | 31.2 | I350 | [B] `swiart` |
| `eurtow.3` | — | 31.2 | C400 | [B] `swiart` |
| `eurtow.4` | — | 31.2 | I450 | [B] `swiart` |
| `eurtow.5` | — | 31.2 | C500 | [B] `swiart` |
| `ferry.1` | Усовершенствовать конструкцию транспортного судна (+%value% посадочных мест) | 15.6 | F1000 G1250 | [T] `swicen.1` |
| `swiaca.12` | Улучшить стрелковое оружие: нарезной ствол (сила выстрела +10%) | 15.6 | I5000 | [B] `swibla` |
| `swiaca.13` | Исследовать гранулированный порох (сила выстрела +10%) | 15.6 | G4000 | [B] `swibla` |
| `swiaca.14` | Исследовать новые методы очистки серы (сила выстрела +15%) | 15.6 | G7000 | [B] `swibla` |
| `swiaca.15` | Исследовать новые методы очистки селитры (сила выстрела +25%) | 15.6 | C11000 | [B] `swibla` |
| `swiaca.16` | Исследовать новые добавки в порох (дальность стрельбы артиллерии +5%) | 15.6 | G2000 I12150 | [B] `swiart` |
| `swiaca.17` | Разработать новые виды стволов: единорог, карронада (дальность стрельбы артиллерии +10%) | 15.6 | S3000 G4550 I19200 | [B] `swiart` |
| `swiaca.18` | Разработать более прочный лафет для орудий: система Грибоваля (прочность пушек +50%) | 15.6 | G500 I3830 C1500 | [B] `swiart` |
| `swiaca.19` | Разработать многоствольное орудие | 15.6 | G1500 C2500 | [B] `swiart` |
| `swiaca.20` | Разработать новые прицельные системы для пушек (меткость стрельбы артиллерии +35%) | 15.6 | W3540 G2000 C7250 | [B] `swiart` |
| `swiaca.21` | Выделить деньги на ремонтные мастерские для пушек (отремонтировать все пушки) | 15.6 | W350 G100 C250 | [B] `swiart` |
| `swiaca.25` | Разработать монгольфьер (открывает всю карту) | 15.6 | G5750 | [T] `swicen.1` |
| `swiaca.27` | Развивать математику (меткость выстрела орудий +35%) | 15.6 | W9540 G12000 C65200 | [B] `swiart` |
| `swiaca.28` | Разработать новые парусные системы (скорость кораблей +40%) | 15.6 | W65400 G24050 | [B] `eurpor` |
| `swiaca.29` | Разработать новую систему шпангоутов и корпуса корабля (условие для постройки линейных кораблей) | 15.6 | W32300 G6800 I9000 C12800 | [B] `eurpor` |
| `swiaca.30` | Обучить плотников (скорость постройки кораблей увеличивается в 10 раз) | 15.6 | W2300 S42700 G1150 | [B] `eurpor` |
| `swiaca.32` | Разработать кремниевый замок к ружьям (цена мушкета -50%) | 15.6 | G6050 C7750 | [T] `swicen.1` |
| `swiaca.34` | Разработать новые сорта стали для кирас (защита солдат в доспехах +2) | 15.6 | G9750 | [B] `swibla` |
| `swiaca.35` | Разработать штык: вставляемый в ствол багинет, штык с трубкой (сила удара холодного оружия +5) | 15.6 | G11500 | [T] `swicen.1`, [B] `swibla` |
| `swiaca.36` | Разработать новые сорта стали (эффективность рукопашной атаки мушкетера 18 века и гренадера +25%) | 15.6 | G19500 | [T] `swicen.1`, [B] `swibla` |
| `swiaca.5` | Разработать новые снасти и сети для ловли рыбы (эффективность рыбацких лодок +100%) | 15.6 | W12400 G2520 | [B] `eurpor` |
| `swiaca.6` | Разработать новые методы древообработки (условие для постройки фрегатов) | 15.6 | W12400 G7040 | [B] `eurpor` |
| `swiaca.7` | Построить новые верфи для рыбацких лодок (стоимость рыбацкой лодки -85%) | 15.6 | W7300 G1220 | [B] `eurpor` |
| `swiaca.8` | Разработать новые инструменты для древообработки (эффективность добычи дерева +100%) | 15.6 | F5500 G550 | [B] `swibla` |
| `swiart.cannon.1.1` | — | 10.0 | W1000 S500 G300 | [B] `swibla` |
| `swiart.cannon.1.2` | — | 10.0 | W3000 S1000 G500 | [B] `swibla` |
| `swiart.cannon.1.3` | — | 10.0 | W6000 S2000 G1000 | [B] `swibla` |
| `swiart.cannon.1.4` | — | 15.6 | F1760 G350 | [B] `swibla` |
| `swiart.cannon.1.5` | — | 15.6 | F1760 G350 | [B] `swibla` |
| `swiart.cannon.1.6` | — | 15.6 | F1760 G350 | [B] `swibla` |
| `swiart.cannon.2.1` | — | 10.0 | G500 I1000 | [B] `swibla` |
| `swiart.cannon.2.2` | — | 10.0 | G1000 I2000 | [B] `swibla` |
| `swiart.cannon.2.3` | — | 10.0 | G2000 I3000 | [B] `swibla` |
| `swiart.cannon.2.4` | — | 15.6 | F2560 | [B] `swibla` |
| `swiart.cannon.2.5` | — | 15.6 | F3560 | [B] `swibla` |
| `swiart.cannon.2.6` | — | 15.6 | F5560 | [B] `swibla` |
| `swiart.howitzer.1.1` | — | 10.0 | W1000 S500 G300 | [B] `swibla` |
| `swiart.howitzer.1.2` | — | 10.0 | W3000 S1000 G500 | [B] `swibla` |
| `swiart.howitzer.1.3` | — | 10.0 | W6000 S2000 G1000 | [B] `swibla` |
| `swiart.howitzer.1.4` | — | 15.6 | F1760 G350 | [B] `swibla` |
| `swiart.howitzer.1.5` | — | 15.6 | F1760 G350 | [B] `swibla` |
| `swiart.howitzer.1.6` | — | 15.6 | F1760 G350 | [B] `swibla` |
| `swiart.howitzer.2.1` | — | 10.0 | G500 I1000 | [B] `swibla` |
| `swiart.howitzer.2.2` | — | 10.0 | G1000 I2000 | [B] `swibla` |
| `swiart.howitzer.2.3` | — | 10.0 | G2000 I3000 | [B] `swibla` |
| `swiart.howitzer.2.4` | — | 31.2 | F2560 | [B] `swibla` |
| `swiart.howitzer.2.5` | — | 31.2 | F3560 | [B] `swibla` |
| `swiart.howitzer.2.6` | — | 31.2 | F5560 | [B] `swibla` |
| `swibar.pikemanswi.1.6` | — | 15.6 | F15000 G1875 | [B] `swibla` |
| `swibar.pikemanswi.2.6` | — | 15.6 | F11250 G1500 | [B] `swibla` |
| `swibla.4` | Выковать штыки и тесаки для пехоты (сила удара мушкетера 18 века и гренадера +5) | 15.6 | W1300 G1500 I900 C5000 | [T] `swicen.1` |
| `swicen.1` | — | 9.4 | F30000 G5000 I2000 C2000 | [B] `swiaca`, [B] `switem`, [B] `swiart` |

[↑ к содержанию](#содержание)

## TUR — Turkey (Турция)

### `tur` — здания

| sid | имя | Время (g-сек) | цена | ферма | требует |
|---|---|---:|---|---:|---|
| `eurcoa` | Шахта | 93.8 | W100 S100 | — | — |
| `eurgol` | Шахта | 93.8 | W100 S100 | — | — |
| `euriro` | Шахта | 93.8 | W100 S100 | — | — |
| `turaca` | Минарет | 156.2 | W1450 S1100 | — | [B] `turbar` |
| `turart` | Артиллерийское депо | 245.9 | W500 S1200 C1400 | — | [B] `turaca` |
| `turbar` | Казарма | 93.8 | W400 S400 | 50 | [B] `turbla` |
| `turbla` | Кузница | 109.4 | W100 S30 I640 | — | [B] `turcen` |
| `turcen` | Городской центр | 156.2 | W600 S500 | 100 | — |
| `turdip` | Дипломатический центр | 312.5 | W4600 S2020 | — | [B] `turaca` |
| `turhou` | Дом | 31.2 | W100 S100 | 25 | [B] `turcen` |
| `turmar` | Базар | 234.4 | W450 S150 | — | [B] `turmil`, [B] `tursto` |
| `turmil` | Мельница | 93.8 | W30 S150 | — | — |
| `turpor` | Порт | 1562.5 | W800 S800 I400 | — | [B] `turmar` |
| `tursga` | Каменные ворота | 120.0 | S60 | — | — |
| `tursta` | Конюшня | 156.2 | W1000 S2600 | — | [B] `turbla` |
| `tursto` | Склад | 31.2 | W30 S10 | — | [B] `turcen` |
| `turswa` | Стена | 120.0 | S60 | — | [B] `tursto` |
| `turtem` | Мечеть | 93.8 | W1000 S1200 I500 | — | [B] `turcen` |
| `turtow` | Башня | 984.4 | W150 S90 G100 | — | [B] `tursto` |
| `ukrwga` | Деревянные ворота | 5.6 | W10 | — | — |
| `ukrwwa` | Частокол | 5.6 | W10 | — | [B] `tursto` |

### `tur` — юниты

| sid | имя | Время (g-сек) | цена | тренируется в | требует |
|---|---|---:|---|---|---|
| `archerdip` | Лучник (наемник) | 1.25 | G15 | turdip | [B] `turaca`, [B] `turcen` |
| `archertur` | Турецкий лучник | 3.00 | F45 W3 G4 | turbar | [B] `turbla` |
| `archerturdip` | Турецкий лучник (наемник) | 1.25 | G15 | turdip | [B] `turaca`, [B] `turcen` |
| `battleship` | Линейный корабль | 390.00 | W9000 G3200 I700 C6500 | turpor | [T] `turaca.29`, [B] `turart` |
| `cannon` | Пушка | 75.00 | W250 G400 I400 | turart | [B] `turbla` |
| `cossacksichdip` | Сечевой козак (наемник) | 2.50 | G60 | turdip | [B] `turaca`, [B] `turcen` |
| `dragoon18dip` | Драгун 18в. (наемник) | 2.00 | G120 | turdip | [B] `turaca`, [B] `turcen` |
| `drummertur` | Барабанщик | 4.00 | F30 G15 | turbar | [B] `turaca` |
| `ferry` | Транспорт | 56.00 | W300 G50 I100 | turpor | [B] `turart` |
| `fishboat` | Рыбацкая лодка | 40.00 | W600 | turpor | — |
| `galley` | Галера | 50.00 | W9500 G900 I800 | turpor | [B] `turart` |
| `grenadierdip` | Гренадер (наемник) | 1.50 | G25 | turdip | [B] `turaca`, [B] `turcen` |
| `howitzer` | Гаубица | 94.00 | W250 G350 I300 | turart | [B] `turbla` |
| `jannisary` | Янычар | 8.00 | F55 G13 I5 | turbar | [B] `turbla` |
| `lightcavalrydip` | Легкий кавалерист (наемник) | 2.00 | G120 | turdip | [B] `turaca`, [B] `turcen` |
| `lightinfantry` | Легкий пехотинец | 1.00 | F25 I1 | turbar | — |
| `lightinfantrydip` | Легкий пехотинец (наемник) | 1.25 | G4 | turdip | [B] `turaca`, [B] `turcen` |
| `mortar` | Мортира | 25.00 | W100 G75 I200 | turart | [B] `turbla` |
| `mullah` | Мулла | 15.00 | F30 G10 | turtem | — |
| `officertur` | Офицер | 7.50 | F50 G100 | turbar | [B] `turaca` |
| `peatur` | Крестьянин | 12.50 | F100 | turcen | — |
| `pikemantur` | Турецкий пикинер | 5.50 | F55 G5 | turbar | [B] `turbla` |
| `roundshierdip` | Рундашир (наемник) | 1.50 | G12 | turdip | [B] `turaca`, [B] `turcen` |
| `sipahi` | Тяжелый сипах | 18.00 | F130 G20 I70 | tursta | [B] `turbla` |
| `spakh` | Легкий сипах | 9.00 | F80 G6 I5 | tursta | — |
| `tatar` | Татарин | 11.25 | F70 W2 G6 | tursta | — |
| `unitbox` | — | 3.12 | F100 | — | — |
| `xebec` | Шебека | 230.00 | W7000 G1600 I320 C960 | turpor | [T] `turaca.6`, [B] `turart` |
| `yachttur` | Турецкая яхта | 48.00 | W900 G450 I150 C200 | turpor | [B] `turart` |

### `tur` — ключевые апгрейды (с зависимостями)

| sid | имя | Время (g-сек) | цена | требует |
|---|---|---:|---|---|
| `turaca.12` | Улучшить стрелковое оружие: нарезной ствол (сила выстрела +10%) | 15.6 | I5000 | [B] `turbla` |
| `turaca.13` | Исследовать гранулированный порох (сила выстрела +10%) | 15.6 | G4000 | [B] `turbla` |
| `turaca.14` | Исследовать новые методы очистки серы (сила выстрела +15%) | 15.6 | G7000 | [B] `turbla` |
| `turaca.15` | Исследовать новые методы очистки селитры (сила выстрела +25%) | 15.6 | C11000 | [B] `turbla` |
| `turaca.16` | Исследовать новые добавки в порох (дальность стрельбы артиллерии +5%) | 15.6 | G2000 | [B] `turart` |
| `turaca.17` | Разработать новые виды стволов: единорог, карронада (дальность стрельбы артиллерии +10%) | 15.6 | S3000 G4550 | [B] `turart` |
| `turaca.18` | Разработать более прочный лафет для орудий: система Грибоваля (прочность пушек +50%) | 15.6 | G500 I3830 C1500 | [B] `turart` |
| `turaca.20` | Разработать новые прицельные системы для пушек (меткость стрельбы артиллерии +35%) | 15.6 | W3540 G2000 C7250 | [B] `turart` |
| `turaca.21` | Выделить деньги на ремонтные мастерские для пушек (отремонтировать все пушки) | 15.6 | W350 G100 C250 | [B] `turart` |
| `turaca.27` | Развивать математику (меткость выстрела орудий +35%) | 15.6 | W9540 G12000 C65200 | [B] `turart` |
| `turaca.28` | Разработать новые парусные системы (скорость кораблей +40%) | 15.6 | G1900 | [B] `turpor` |
| `turaca.29` | Разработать новую систему шпангоутов и корпуса корабля (условие для постройки линейных кораблей) | 15.6 | W32300 G6800 I9000 C12800 | [B] `turpor` |
| `turaca.30` | Обучить плотников (скорость постройки кораблей увеличивается в 10 раз) | 15.6 | S42700 | [B] `turpor` |
| `turaca.34` | Разработать новые сорта стали для кирас (защита солдат в доспехах +2) | 15.6 | G6950 | [B] `turbla` |
| `turaca.5` | Разработать новые снасти и сети для ловли рыбы (эффективность рыбацких лодок +100%) | 15.6 | W12400 G2520 | [B] `turpor` |
| `turaca.6` | Разработать новые методы древообработки (условие для постройки шебек) | 15.6 | W9500 G7040 | [B] `turpor` |
| `turaca.7` | Построить новые верфи для рыбацких лодок (стоимость рыбацкой лодки -85%) | 15.6 | W7300 G1220 | [B] `turpor` |
| `turaca.8` | Разработать новые инструменты для древообработки (эффективность добычи дерева +100%) | 15.6 | F5500 G550 | [B] `turbla` |
| `turart.cannon.1.1` | — | 10.0 | W1000 S500 G300 | [B] `turbla` |
| `turart.cannon.1.2` | — | 10.0 | W3000 S1000 G500 | [B] `turbla` |
| `turart.cannon.1.3` | — | 10.0 | W6000 S2000 G1000 | [B] `turbla` |
| `turart.cannon.1.4` | — | 15.6 | F1760 G350 | [B] `turbla` |
| `turart.cannon.1.5` | — | 15.6 | F1760 G350 | [B] `turbla` |
| `turart.cannon.1.6` | — | 15.6 | F1760 G350 | [B] `turbla` |
| `turart.cannon.2.1` | — | 10.0 | G950 I1000 | [B] `turbla` |
| `turart.cannon.2.2` | — | 10.0 | G150 I2000 | [B] `turbla` |
| `turart.cannon.2.3` | — | 10.0 | G250 I3000 | [B] `turbla` |
| `turart.cannon.2.4` | — | 15.6 | F2560 G1350 | [B] `turbla` |
| `turart.cannon.2.5` | — | 15.6 | F3560 G2500 | [B] `turbla` |
| `turart.cannon.2.6` | — | 15.6 | F5560 G3350 | [B] `turbla` |
| `turart.howitzer.1.1` | — | 10.0 | W1000 S500 G300 | [B] `turbla` |
| `turart.howitzer.1.2` | — | 10.0 | W3000 S1000 G500 | [B] `turbla` |
| `turart.howitzer.1.3` | — | 10.0 | W6000 S2000 G1000 | [B] `turbla` |
| `turart.howitzer.1.4` | — | 15.6 | F1760 G350 | [B] `turbla` |
| `turart.howitzer.1.5` | — | 15.6 | F1760 G350 | [B] `turbla` |
| `turart.howitzer.1.6` | — | 15.6 | F1760 G350 | [B] `turbla` |
| `turart.howitzer.2.1` | — | 10.0 | G350 I1000 | [B] `turbla` |
| `turart.howitzer.2.2` | — | 10.0 | G450 I2000 | [B] `turbla` |
| `turart.howitzer.2.3` | — | 10.0 | G550 I3000 | [B] `turbla` |
| `turart.howitzer.2.4` | — | 31.2 | F2560 G1150 | [B] `turbla` |
| `turart.howitzer.2.5` | — | 31.2 | F3560 G3200 | [B] `turbla` |
| `turart.howitzer.2.6` | — | 31.2 | F5560 G4500 | [B] `turbla` |
| `turbar.jannisary.1.4` | — | 15.6 | F5000 G1600 | [B] `turbla` |
| `turbar.jannisary.1.5` | — | 15.6 | F7500 G3200 | [B] `turbla` |
| `turbar.jannisary.1.6` | — | 15.6 | F10000 G4800 | [B] `turbla` |
| `turbar.lightinfantry.1.4` | — | 15.6 | F3000 G360 | [B] `turbla` |
| `turbar.lightinfantry.1.5` | — | 15.6 | F4500 G540 | [B] `turbla` |
| `turbar.lightinfantry.1.6` | — | 15.6 | F9375 G1125 | [B] `turbla` |
| `turbar.lightinfantry.2.4` | — | 15.6 | F3600 G600 | [B] `turbla` |
| `turbar.lightinfantry.2.5` | — | 15.6 | F5400 G900 | [B] `turbla` |
| `turbar.lightinfantry.2.6` | — | 15.6 | F11250 G1875 | [B] `turbla` |
| `turbar.pikemantur.1.6` | — | 15.6 | F18750 G2350 | [B] `turbla` |
| `turbar.pikemantur.2.6` | — | 15.6 | F16875 G2250 | [B] `turbla` |
| `turpor.1` | — | 46.9 | W20000 G1500 | [B] `turart` |
| `turtow.1` | — | 31.2 | G250 | [B] `turart` |
| `turtow.2` | — | 31.2 | I350 | [B] `turart` |
| `turtow.3` | — | 31.2 | C400 | [B] `turart` |
| `turtow.4` | — | 31.2 | I450 | [B] `turart` |
| `turtow.5` | — | 31.2 | C500 | [B] `turart` |

[↑ к содержанию](#содержание)

## UKR — Ukraine (Украина)

### `ukr` — здания

| sid | имя | Время (g-сек) | цена | ферма | требует |
|---|---|---:|---|---:|---|
| `eurcoa` | Шахта | 93.8 | W100 S100 | — | — |
| `eurgol` | Шахта | 93.8 | W100 S100 | — | — |
| `euriro` | Шахта | 93.8 | W100 S100 | — | — |
| `rusmar` | Рынок | 234.4 | W450 | — | [B] `rusmil`, [B] `russto` |
| `rusmil` | Мельница | 93.8 | W210 | — | — |
| `russto` | Склад | 31.2 | W50 S20 | — | [B] `ukrcen` |
| `ukraca` | Академия | 46.9 | W1350 S1200 | — | [B] `ukrbar` |
| `ukrart` | Артиллерийское депо | 245.9 | W4250 S4400 G100 C1400 | — | [B] `ukraca` |
| `ukrbar` | Козацкий дом | 93.8 | W150 S150 | 75 | [B] `ukrbla` |
| `ukrbla` | Кузница | 62.5 | W100 S30 I640 | — | [B] `ukrcen` |
| `ukrcen` | Городской центр | 156.2 | W700 | 200 | — |
| `ukrdip` | Дипломатический центр | 312.5 | W3900 S2700 | — | [B] `ukraca` |
| `ukrhou` | Хижина | 31.2 | W120 | 25 | [B] `ukrcen` |
| `ukrpor` | Порт | 1562.5 | W2000 | — | [B] `rusmar` |
| `ukrsta` | Конюшня | 156.2 | W3200 S850 G850 | — | [B] `ukrbla` |
| `ukrtem` | Православная церковь | 156.2 | W1100 S1400 I300 | — | [B] `ukrcen` |
| `ukrwga` | Деревянные ворота | 8.1 | W12 | — | — |
| `ukrwwa` | Частокол | 8.1 | W12 | — | [B] `russto` |

### `ukr` — юниты

| sid | имя | Время (g-сек) | цена | тренируется в | требует |
|---|---|---:|---|---|---|
| `archerdip` | Лучник (наемник) | 1.25 | G15 | ukrdip | [B] `ukraca`, [B] `ukrcen` |
| `archerturdip` | Турецкий лучник (наемник) | 1.25 | G15 | ukrdip | [B] `ukraca`, [B] `ukrcen` |
| `cannon` | Пушка | 75.00 | W250 G400 I400 | ukrart | [B] `ukrbla` |
| `chaika` | — | 40.00 | W1050 G600 I200 C400 | ukrpor | [B] `ukrart` |
| `cossackregister` | Реестровый козак | 10.50 | F70 G15 | ukrsta | [B] `ukrbla` |
| `cossacksich` | Сечевой козак | 13.50 | F130 I2 | ukrsta | — |
| `cossacksichdip` | Сечевой козак (наемник) | 2.50 | G60 | ukrdip | [B] `ukraca`, [B] `ukrcen` |
| `dragoon18dip` | Драгун 18в. (наемник) | 2.00 | G120 | ukrdip | [B] `ukraca`, [B] `ukrcen` |
| `ferry` | Транспорт | 56.00 | W300 G50 I100 | ukrpor | [B] `ukrart` |
| `fishboat` | Рыбацкая лодка | 40.00 | W600 | ukrpor | — |
| `galley` | Галера | 50.00 | W9500 G900 I800 | ukrpor | [B] `ukrart` |
| `grenadierdip` | Гренадер (наемник) | 1.50 | G25 | ukrdip | [B] `ukraca`, [B] `ukrcen` |
| `hetman` | Гетьман | 16.50 | F150 G150 I10 | ukrsta | — |
| `howitzer` | Гаубица | 94.00 | W250 G350 I300 | ukrart | [B] `ukrbla` |
| `lightcavalrydip` | Легкий кавалерист (наемник) | 2.00 | G120 | ukrdip | [B] `ukraca`, [B] `ukrcen` |
| `lightinfantrydip` | Легкий пехотинец (наемник) | 1.25 | G4 | ukrdip | [B] `ukraca`, [B] `ukrcen` |
| `mortar` | Мортира | 25.00 | W100 G75 I200 | ukrart | [B] `ukrbla` |
| `peaukr` | Крестьянин | 11.25 | F100 | ukrcen | — |
| `pope` | Поп | 20.00 | F40 G20 | ukrtem | — |
| `roundshierdip` | Рундашир (наемник) | 1.50 | G12 | ukrdip | [B] `ukraca`, [B] `ukrcen` |
| `serdiuk` | Сердюк | 11.00 | F60 G11 I5 | ukrbar | — |
| `unitbox` | — | 3.12 | F100 | — | — |

### `ukr` — ключевые апгрейды (с зависимостями)

| sid | имя | Время (g-сек) | цена | требует |
|---|---|---:|---|---|
| `ukraca.12` | Улучшить стрелковое оружие: нарезной ствол (сила выстрела +10%) | 15.6 | I5000 | [B] `ukrbla` |
| `ukraca.13` | Исследовать гранулированный порох (сила выстрела +10%) | 15.6 | G4000 | [B] `ukrbla` |
| `ukraca.14` | Исследовать новые методы очистки серы (сила выстрела +15%) | 15.6 | G7000 | [B] `ukrbla` |
| `ukraca.15` | Исследовать новые методы очистки селитры (сила выстрела +25%) | 15.6 | C11000 | [B] `ukrbla` |
| `ukraca.16` | Исследовать новые добавки в порох (дальность стрельбы артиллерии +5%) | 15.6 | G2000 I12150 | [B] `ukrart` |
| `ukraca.17` | Разработать новые виды стволов: единорог, карронада (дальность стрельбы артиллерии +10%) | 15.6 | S3000 G4550 I19200 | [B] `ukrart` |
| `ukraca.18` | Разработать более прочный лафет для орудий: система Грибоваля (прочность пушек +50%) | 15.6 | G500 I3830 C1500 | [B] `ukrart` |
| `ukraca.20` | Разработать новые прицельные системы для пушек (меткость стрельбы артиллерии +35%) | 15.6 | W3540 G2000 C7250 | [B] `ukrart` |
| `ukraca.21` | Выделить деньги на ремонтные мастерские для пушек (отремонтировать все пушки) | 15.6 | W350 G100 C250 | [B] `ukrart` |
| `ukraca.27` | Развивать математику (меткость выстрела орудий +35%) | 15.6 | W9540 G12000 C65200 | [B] `ukrart` |
| `ukraca.28` | Разработать новые парусные системы (скорость кораблей +40%) | 15.6 | G900 | [B] `ukrpor` |
| `ukraca.30` | Обучить плотников (скорость постройки кораблей увеличивается в 10 раз) | 15.6 | W2300 S42700 G1150 | [B] `ukrpor` |
| `ukraca.5` | Разработать новые снасти и сети для ловли рыбы (эффективность рыбацких лодок +100%) | 15.6 | W12400 G2520 | [B] `ukrpor` |
| `ukraca.7` | Построить новые верфи для рыбацких лодок (стоимость рыбацкой лодки -85%) | 15.6 | W7300 G1220 | [B] `ukrpor` |
| `ukraca.8` | Разработать новые инструменты для древообработки (эффективность добычи дерева +100%) | 15.6 | F5500 G550 | [B] `ukrbla` |
| `ukrart.cannon.1.1` | — | 10.0 | W1000 S500 G300 | [B] `ukrbla` |
| `ukrart.cannon.1.2` | — | 10.0 | W3000 S1000 G500 | [B] `ukrbla` |
| `ukrart.cannon.1.3` | — | 10.0 | W6000 S2000 G1000 | [B] `ukrbla` |
| `ukrart.cannon.1.4` | — | 15.6 | F1760 G350 | [B] `ukrbla` |
| `ukrart.cannon.1.5` | — | 15.6 | F1760 G350 | [B] `ukrbla` |
| `ukrart.cannon.1.6` | — | 15.6 | F1760 G350 | [B] `ukrbla` |
| `ukrart.cannon.2.1` | — | 10.0 | G500 I1000 | [B] `ukrbla` |
| `ukrart.cannon.2.2` | — | 10.0 | G1000 I2000 | [B] `ukrbla` |
| `ukrart.cannon.2.3` | — | 10.0 | G2000 I3000 | [B] `ukrbla` |
| `ukrart.cannon.2.4` | — | 15.6 | F2560 | [B] `ukrbla` |
| `ukrart.cannon.2.5` | — | 15.6 | F3560 | [B] `ukrbla` |
| `ukrart.cannon.2.6` | — | 15.6 | F5560 | [B] `ukrbla` |
| `ukrart.howitzer.1.1` | — | 10.0 | W1000 S500 G300 | [B] `ukrbla` |
| `ukrart.howitzer.1.2` | — | 10.0 | W3000 S1000 G500 | [B] `ukrbla` |
| `ukrart.howitzer.1.3` | — | 10.0 | W6000 S2000 G1000 | [B] `ukrbla` |
| `ukrart.howitzer.1.4` | — | 15.6 | F1760 G350 | [B] `ukrbla` |
| `ukrart.howitzer.1.5` | — | 15.6 | F1760 G350 | [B] `ukrbla` |
| `ukrart.howitzer.1.6` | — | 15.6 | F1760 G350 | [B] `ukrbla` |
| `ukrart.howitzer.2.1` | — | 10.0 | G500 I1000 | [B] `ukrbla` |
| `ukrart.howitzer.2.2` | — | 10.0 | G1000 I2000 | [B] `ukrbla` |
| `ukrart.howitzer.2.3` | — | 10.0 | G2000 I3000 | [B] `ukrbla` |
| `ukrart.howitzer.2.4` | — | 31.2 | F2560 | [B] `ukrbla` |
| `ukrart.howitzer.2.5` | — | 31.2 | F3560 | [B] `ukrbla` |
| `ukrart.howitzer.2.6` | — | 31.2 | F5560 | [B] `ukrbla` |
| `ukrbar.serdiuk.1.6` | — | 15.6 | F60000 G8000 | [B] `ukrbla` |
| `ukrbar.serdiuk.2.6` | — | 15.6 | F11250 G1125 | [B] `ukrbla` |
| `ukrpor.1` | — | 46.9 | W20000 G1500 | [B] `ukrart` |

[↑ к содержанию](#содержание)

## VEN — Venice (Венеция)

### `ven` — здания

| sid | имя | Время (g-сек) | цена | ферма | требует |
|---|---|---:|---|---:|---|
| `eurcoa` | Шахта | 93.8 | W100 S100 | — | — |
| `eurgol` | Шахта | 93.8 | W100 S100 | — | — |
| `euriro` | Шахта | 93.8 | W100 S100 | — | — |
| `eurmar` | Рынок | 234.4 | W450 | — | [B] `eurmil`, [B] `eursto` |
| `eurmil` | Мельница | 93.8 | W30 S150 | — | — |
| `eurpor` | Порт | 1562.5 | W1600 S800 I400 | — | [B] `eurmar` |
| `eursga` | Каменные ворота | 90.0 | S50 | — | — |
| `eursto` | Склад | 31.2 | W50 S20 | — | [B] `vencen` |
| `eurswa` | Стена | 90.0 | S50 | — | [B] `eursto` |
| `eurtow` | Башня | 1230.3 | W100 S100 G150 | — | [B] `eursto` |
| `ukrwga` | Деревянные ворота | 5.6 | W10 | — | — |
| `ukrwwa` | Частокол | 5.6 | W10 | — | [B] `eursto` |
| `venaca` | Академия | 625.0 | W1090 S1260 | — | [B] `venbar` |
| `venart` | Артиллерийское депо | 245.9 | W100 S1000 C1400 | — | [B] `venaca` |
| `venba2` | Казарма 18в. | 5625.0 | W1700 S2950 G4000 | 250 | [T] `vencen.1` |
| `venbar` | Казарма 17в. | 93.8 | W100 S100 G500 | 150 | [B] `venbla` |
| `venbla` | Кузница | 93.8 | W100 S30 I640 | — | [B] `vencen` |
| `vencen` | Городской центр | 156.2 | W700 S700 | 100 | — |
| `vendip` | Дипломатический центр | 312.5 | W4900 S1700 | — | [B] `venaca` |
| `venhou` | Дом | 31.2 | W100 S100 | 25 | [B] `vencen` |
| `vensta` | Конюшня | 625.0 | W2500 S100 G600 | — | [B] `venbla` |
| `ventem` | Собор | 156.2 | W1000 S1200 I500 | — | [B] `vencen` |

### `ven` — юниты

| sid | имя | Время (g-сек) | цена | тренируется в | требует |
|---|---|---:|---|---|---|
| `archerdip` | Лучник (наемник) | 1.25 | G15 | vendip | [B] `venaca`, [B] `vencen` |
| `archerturdip` | Турецкий лучник (наемник) | 1.25 | G15 | vendip | [B] `venaca`, [B] `vencen` |
| `battleship` | Линейный корабль | 390.00 | W9000 G3200 I700 C6500 | eurpor | [T] `venaca.29`, [B] `venart` |
| `cannon` | Пушка | 75.00 | W250 G400 I400 | venart | [B] `venbla` |
| `cossacksichdip` | Сечевой козак (наемник) | 2.50 | G60 | vendip | [B] `venaca`, [B] `vencen` |
| `cuirassier` | Кирасир | 22.50 | F120 G35 I25 | vensta | [B] `venbla`, [T] `vencen.1` |
| `dragoon` | Драгун 17в. | 15.00 | F90 G7 I5 | vensta | [B] `venbla` |
| `dragoon18` | Драгун 18в. | 22.50 | F70 G60 I7 | vensta | [B] `venbla`, [T] `vencen.1` |
| `dragoon18dip` | Драгун 18в. (наемник) | 2.00 | G120 | vendip | [B] `venaca`, [B] `vencen` |
| `drummer` | Барабанщик 17в. | 5.00 | F60 G20 | venbar | [B] `venaca` |
| `drummer18` | Барабанщик 18в. | 6.00 | F50 G30 | venba2 | [B] `venaca` |
| `ferry` | Транспорт | 56.00 | W300 G50 I100 | eurpor | [B] `venart` |
| `fishboat` | Рыбацкая лодка | 40.00 | W600 | eurpor | — |
| `frigate` | Фрегат | 230.00 | W5000 G1100 I600 C800 | eurpor | [T] `venaca.6`, [B] `venart` |
| `galley` | Галера | 50.00 | W9500 G900 I800 | eurpor | [B] `venart` |
| `grenadier` | Гренадер | 6.00 | F80 G60 I40 | venba2 | [B] `venbla` |
| `grenadierdip` | Гренадер (наемник) | 1.50 | G25 | vendip | [B] `venaca`, [B] `vencen` |
| `howitzer` | Гаубица | 94.00 | W250 G350 I300 | venart | [B] `venbla` |
| `hussar` | Гусар | 15.00 | F70 G20 I2 | vensta | [B] `venbla`, [T] `vencen.1` |
| `lightcavalrydip` | Легкий кавалерист (наемник) | 2.00 | G120 | vendip | [B] `venaca`, [B] `vencen` |
| `lightinfantrydip` | Легкий пехотинец (наемник) | 1.25 | G4 | vendip | [B] `venaca`, [B] `vencen` |
| `mortar` | Мортира | 25.00 | W100 G75 I200 | venart | [B] `venbla` |
| `multicannon` | Многоствольное орудие | 50.00 | W200 G400 I250 | venart | [T] `venaca.19`, [B] `venbla` |
| `musketeer` | Мушкетер 17в. | 6.00 | F45 G6 I5 | venbar | [B] `venbla` |
| `musketeer18` | Мушкетер 18в. | 4.50 | F50 G40 I40 | venba2 | [B] `venbla` |
| `officer` | Офицер 17в. | 10.00 | F50 G150 I30 | venbar | [B] `venaca` |
| `officer18` | Офицер 18в. | 6.00 | F50 G200 I10 | venba2 | [B] `venaca` |
| `peaspa` | Крестьянин | 12.50 | F100 | vencen | — |
| `pikeman` | Пикинер 17в. | 4.50 | F25 G3 I20 | venbar | [B] `venbla` |
| `pikeman18` | Пикинер 18в. | 1.25 | F30 G2 | venba2 | — |
| `priest` | Капеллан | 20.00 | F60 G25 | ventem | — |
| `reiter` | Рейтар | 24.00 | F120 G10 I40 | vensta | [B] `venbla` |
| `roundshierdip` | Рундашир (наемник) | 1.50 | G12 | vendip | [B] `venaca`, [B] `vencen` |
| `unitbox` | — | 3.12 | F100 | — | — |
| `yacht` | Яхта | 48.00 | W900 G450 I150 C200 | eurpor | [B] `venart` |

### `ven` — ключевые апгрейды (с зависимостями)

| sid | имя | Время (g-сек) | цена | требует |
|---|---|---:|---|---|
| `eurcoa.4` | — | 9.4 | F15800 G18500 | [T] `vencen.1` |
| `eurcoa.5` | — | 9.4 | F19800 G21050 | [T] `vencen.1` |
| `eurcoa.6` | — | 9.4 | F50200 G25950 | [T] `vencen.1` |
| `eurgol.4` | — | 9.4 | F15800 G18500 | [T] `vencen.1` |
| `eurgol.5` | — | 9.4 | F19800 G21050 | [T] `vencen.1` |
| `eurgol.6` | — | 9.4 | F50200 G25950 | [T] `vencen.1` |
| `euriro.4` | — | 9.4 | F15800 G18500 | [T] `vencen.1` |
| `euriro.5` | — | 9.4 | F19800 G21050 | [T] `vencen.1` |
| `euriro.6` | — | 9.4 | F50200 G25950 | [T] `vencen.1` |
| `eurpor.1` | — | 46.9 | W20000 G1500 | [B] `venart` |
| `eurtow.1` | — | 31.2 | G250 | [B] `venart` |
| `eurtow.2` | — | 31.2 | I350 | [B] `venart` |
| `eurtow.3` | — | 31.2 | C400 | [B] `venart` |
| `eurtow.4` | — | 31.2 | I450 | [B] `venart` |
| `eurtow.5` | — | 31.2 | C500 | [B] `venart` |
| `ferry.1` | Усовершенствовать конструкцию транспортного судна (+%value% посадочных мест) | 15.6 | F1000 G1250 | [T] `vencen.1` |
| `venaca.12` | Улучшить стрелковое оружие: нарезной ствол (сила выстрела +10%) | 15.6 | I5000 | [B] `venbla` |
| `venaca.13` | Исследовать гранулированный порох (сила выстрела +10%) | 15.6 | G4000 | [B] `venbla` |
| `venaca.14` | Исследовать новые методы очистки серы (сила выстрела +15%) | 15.6 | G7000 | [B] `venbla` |
| `venaca.15` | Исследовать новые методы очистки селитры (сила выстрела +25%) | 15.6 | C11000 | [B] `venbla` |
| `venaca.16` | Исследовать новые добавки в порох (дальность стрельбы артиллерии +5%) | 15.6 | G2000 I12150 | [B] `venart` |
| `venaca.17` | Разработать новые виды стволов: единорог, карронада (дальность стрельбы артиллерии +10%) | 15.6 | S3000 G4550 I19200 | [B] `venart` |
| `venaca.18` | Разработать более прочный лафет для орудий: система Грибоваля (прочность пушек +50%) | 15.6 | G500 I3830 C1500 | [B] `venart` |
| `venaca.19` | Разработать многоствольное орудие | 15.6 | G1500 C2500 | [B] `venart` |
| `venaca.20` | Разработать новые прицельные системы для пушек (меткость стрельбы артиллерии +35%) | 15.6 | W3540 G2000 C7250 | [B] `venart` |
| `venaca.21` | Выделить деньги на ремонтные мастерские для пушек (отремонтировать все пушки) | 15.6 | W350 G100 C250 | [B] `venart` |
| `venaca.25` | Разработать монгольфьер (открывает всю карту) | 15.6 | G5750 | [T] `vencen.1` |
| `venaca.27` | Развивать математику (меткость выстрела орудий +35%) | 15.6 | W9540 G12000 C65200 | [B] `venart` |
| `venaca.28` | Разработать новые парусные системы (скорость кораблей +40%) | 15.6 | W65400 G24050 | [B] `eurpor` |
| `venaca.29` | Разработать новую систему шпангоутов и корпуса корабля (условие для постройки линейных кораблей) | 15.6 | W32300 G6800 I9000 C12800 | [B] `eurpor` |
| `venaca.30` | Обучить плотников (скорость постройки кораблей увеличивается в 10 раз) | 15.6 | W2300 S42700 G1150 | [B] `eurpor` |
| `venaca.32` | Разработать кремниевый замок к ружьям (цена мушкета -50%) | 15.6 | G6050 C7750 | [T] `vencen.1` |
| `venaca.34` | Разработать новые сорта стали для кирас (защита солдат в доспехах +2) | 15.6 | G9750 | [B] `venbla` |
| `venaca.35` | Разработать штык: вставляемый в ствол багинет, штык с трубкой (сила удара холодного оружия +5) | 15.6 | G11500 | [T] `vencen.1`, [B] `venbla` |
| `venaca.36` | Разработать новые сорта стали (эффективность рукопашной атаки мушкетера 18 века и гренадера +25%) | 15.6 | G19500 | [T] `vencen.1`, [B] `venbla` |
| `venaca.5` | Разработать новые снасти и сети для ловли рыбы (эффективность рыбацких лодок +100%) | 15.6 | W12400 G2520 | [B] `eurpor` |
| `venaca.6` | Разработать новые методы древообработки (условие для постройки фрегатов) | 15.6 | W12400 G7040 | [B] `eurpor` |
| `venaca.7` | Построить новые верфи для рыбацких лодок (стоимость рыбацкой лодки -85%) | 15.6 | W7300 G1220 | [B] `eurpor` |
| `venaca.8` | Разработать новые инструменты для древообработки (эффективность добычи дерева +100%) | 15.6 | F5500 G550 | [B] `venbla` |
| `venart.cannon.1.1` | — | 10.0 | W1000 S500 G300 | [B] `venbla` |
| `venart.cannon.1.2` | — | 10.0 | W3000 S1000 G500 | [B] `venbla` |
| `venart.cannon.1.3` | — | 10.0 | W6000 S2000 G1000 | [B] `venbla` |
| `venart.cannon.1.4` | — | 15.6 | F1760 G350 | [B] `venbla` |
| `venart.cannon.1.5` | — | 15.6 | F1760 G350 | [B] `venbla` |
| `venart.cannon.1.6` | — | 15.6 | F1760 G350 | [B] `venbla` |
| `venart.cannon.2.1` | — | 10.0 | G500 I1000 | [B] `venbla` |
| `venart.cannon.2.2` | — | 10.0 | G1000 I2000 | [B] `venbla` |
| `venart.cannon.2.3` | — | 10.0 | G2000 I3000 | [B] `venbla` |
| `venart.cannon.2.4` | — | 15.6 | F2560 | [B] `venbla` |
| `venart.cannon.2.5` | — | 15.6 | F3560 | [B] `venbla` |
| `venart.cannon.2.6` | — | 15.6 | F5560 | [B] `venbla` |
| `venart.howitzer.1.1` | — | 10.0 | W1000 S500 G300 | [B] `venbla` |
| `venart.howitzer.1.2` | — | 10.0 | W3000 S1000 G500 | [B] `venbla` |
| `venart.howitzer.1.3` | — | 10.0 | W6000 S2000 G1000 | [B] `venbla` |
| `venart.howitzer.1.4` | — | 15.6 | F1760 G350 | [B] `venbla` |
| `venart.howitzer.1.5` | — | 15.6 | F1760 G350 | [B] `venbla` |
| `venart.howitzer.1.6` | — | 15.6 | F1760 G350 | [B] `venbla` |
| `venart.howitzer.2.1` | — | 10.0 | G500 I1000 | [B] `venbla` |
| `venart.howitzer.2.2` | — | 10.0 | G1000 I2000 | [B] `venbla` |
| `venart.howitzer.2.3` | — | 10.0 | G2000 I3000 | [B] `venbla` |
| `venart.howitzer.2.4` | — | 31.2 | F2560 | [B] `venbla` |
| `venart.howitzer.2.5` | — | 31.2 | F3560 | [B] `venbla` |
| `venart.howitzer.2.6` | — | 31.2 | F5560 | [B] `venbla` |
| `venbar.pikeman.1.6` | — | 15.6 | F15000 G1875 | [B] `venbla` |
| `venbar.pikeman.2.6` | — | 15.6 | F11250 G1500 | [B] `venbla` |
| `venbla.4` | Выковать штыки и тесаки для пехоты (сила удара мушкетера 18 века и гренадера +5) | 15.6 | W1300 G1500 I900 C5000 | [T] `vencen.1` |
| `vencen.1` | — | 9.4 | F40000 G3000 I2500 C2500 | [B] `venaca`, [B] `ventem`, [B] `venart` |

[↑ к содержанию](#содержание)
