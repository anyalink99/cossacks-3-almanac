# 02. Бой и движение

[← Index](README.md)

## О чём эта глава

Сводные **таблицы** по бою и движению: типы оружия, скорости юнитов,
матрица контр-эффективности, перекрёстная таблица «апгрейды ×
характеристики», стоимость одного выстрела. Числа извлечены из
скриптов и сгенерированы автоматически из [`data.json`](../../data.json).

**Подробные разборы механик** — в `recon/world/combat/`:

- [combat_damage_pipeline.md](../recon/world/combat/combat_damage_pipeline.md)
  — конвейер урона: 6 шагов формулы, хедшот, AoE-кап, дружественный
  огонь, peace-mode, упрощения.
- [formations.md](../recon/world/combat/formations.md) — LINE /
  SQUARE / KARE: 149 формаций, бонусы строя, hold-mode FSM, порог
  расформирования.
- [ranged_units_behavior.md](../recon/world/combat/ranged_units_behavior.md)
  — поведение стрелков: standground, bartprepare, RunAway, штраф к
  дальности при движении, мульти-оружие, high ground.
- [target_selection.md](../recon/world/combat/target_selection.md)
  — алгоритм выбора цели через scan-grid, attack-move, лечение
  священниками, реакция отряда на удар, рассеяние выстрелов.
- [unit_commands.md](../recon/world/combat/unit_commands.md) —
  очередь приказов, режимы атаки, hold-fire, rally points.
- [vision_and_fow.md](../recon/world/combat/vision_and_fow.md) —
  туман войны и формула радиуса обзора `20 + 4 × vision`.
- [pathfinding.md](../recon/world/combat/pathfinding.md) —
  движение и push.
- [artillery_specifics.md](../recon/world/combat/artillery_specifics.md)
  — артиллерия: `bartprepare`, `attackpoint`, лимиты через арт-депо.
- [towers.md](../recon/world/combat/towers.md)
  — башни и гарнизон.
- [naval_combat.md](../recon/world/combat/naval_combat.md) —
  морской бой.
- [walls_and_gates.md](../recon/world/combat/walls_and_gates.md)
  — стены и ворота.

## Типы оружия (`gc_obj_weapon_kind_*`)

| Kind | Описание | Носители |
|---|---|---|
| `pike` | Длинное копьё / пика | Пикинёры 17 / 18 в. |
| `sword` | Меч / сабля | Лёгкая пехота, мечники, кавалерия в ближнем бою |
| `bullet` | Пуля огнестрела | Мушкетёр, стрелец, янычар, драгун и т.д. |
| `arrow` | Стрела / болт | Лучник (`SHOTLU`-боеприпас) |
| `cannonball` | Пушечное ядро | Пушка, башня, фрегат (одиночный выстрел) |
| `cannister` | Картечь | Пушка ближнего боя, многоствольная пушка |

Каждый `kind` имеет свою колонку `protection[kind]` у целей. См.
формулу урона в
[`recon/world/combat/combat_damage_pipeline.md` §2](../recon/world/combat/combat_damage_pipeline.md).

Детали — в
[`recon/world/combat/combat_damage_pipeline.md`](../recon/world/combat/combat_damage_pipeline.md)
и [`ranged_units_behavior.md`](../recon/world/combat/ranged_units_behavior.md).

## `uniqrnd` — индивидуальное случайное число юнита

При спавне каждый юнит получает `uniqrnd ∈ [0, 1)` — фиксированное
случайное число, остающееся неизменным до смерти (см.
[`internals/engine/rng_implementation.md`](../../internals/engine/rng_implementation.md)).
Используется в **четырёх** механиках одновременно:

| # | Где применяется | Эффект |
|---:|---|---|
| 1 | Бонус хедшота | `+floor(uniqrnd × 500)` дополнительного урона при крите |
| 2 | Эффективная max-range | `radiusmax −= uniqrnd × 3` тайла во время `standtime < 0.25` g-sec |
| 3 | Search timing | `nextSearch = now + uniqrnd × 0.15 + 0.3` сек — юниты не сканируют синхронно |
| 4 | Multiplayer sync seed | `SetRandomKey(floor(uniqrnd × MaxInt))` для синхронизации решений между клиентами |

Детали — в
[`recon/world/combat/combat_damage_pipeline.md`](../recon/world/combat/combat_damage_pipeline.md)
и [`ranged_units_behavior.md`](../recon/world/combat/ranged_units_behavior.md).
## Скорости юнитов

Базовые `gc_obj_speed_*` из `dmscript.global:603-620`. **Абстрактные единицы** (не tiles/sec). Реальная скорость в тайлах/сек зависит от animation `walkInterval`, `walkintervalfactor` и game speed. Для перевода нужен эмпирический замер.

| Класс | Speed | Заметка |
|---|---:|---|
| default | 32 | пехота, артиллерия и многие юниты по умолчанию |
| peasant | 40 | крестьянин — быстрее обычной пехоты |
| hardhorse | 56 | тяжёлая кавалерия (Reiter, Cuirassier, Vityaz) |
| fasthorse | 96 | лёгкая кавалерия (Hussar, Lancer, Cossack) — самые быстрые |
| cannon | 20 | пушка — медленная |
| mortar | 24 | мортира — чуть быстрее пушки |
| howitzer | 20 |  |
| multicannon | 16 |  |
| fishboat | 16 | рыбацкая лодка |
| ferry | 28 | паром (transport) |
| yacht | 40 | яхта (стрелковый корабль) |
| yachttur | 70 | турецкая яхта (быстрее стандартной) |
| chaika | 55 | украинская чайка — мобильная |
| galley | 40 |  |
| frigate | 30 | фрегат |
| xebec | 28 |  |
| battleship | 16 | баттлшип — самый медленный военный корабль |

**Закон:** относительные значения. fasthorse(96) ≈ ×3 от cannon(20). peasant(40) посередине. Самые медленные — battleship/multicannon (16).

## Офицеры и формации

Каждая нация имеет N групп офицеров. Один офицер ведёт **строй** определённых юнитов (чаще пехота/кавалерия одного класса). Формации стандартные для всех:

**LINE / SQUARE / KARE × 15 / 36 / 72 / 120 / 196 / 400 юнитов.**

Чем больше формация, тем сильнее бонусы (атака, защита, мораль).

Полные таблицы офицеров → секции в [nations/](nations/README.md) для каждой нации.

## Матрица контр-эффективности (приближённый TTK)

Для каждой пары (атакующий класс, защищающийся класс) — **приближённое время убийства** (time-to-kill, TTK) в **игровых секундах** при 1v1, без учёта формаций, движения, промахов и shield-бонусов отрядов.

Расчёт: для атакующего берём **репрезентативного юнита класса** (медианный по урону); для защитника — медианный по HP. Применяется формула урона:

```
applied = max(1, weapon.dmg - target.shield - target.protection[weapon.kind])
DPS = applied / weapon.pause_sec
TTK = target.HP / DPS
```

⚠ Цифры ориентировочные. Реальный TTK будет выше из-за: дороги к цели, подготовки выстрела (`bartprepare`), формационных бонусов (отрядный щит, формация LINE/SQUARE/KARE), movement penalty к accuracy, fast-cavalry headshot bonus.

**Медианные представители классов** (использованы для расчёта):

| Класс | Атакующий-репрезентант | урон | перезарядка (с) | тип | Защитник-репрезентант | HP | shield |
|---|---|---:|---:|---|---|---:|---:|
| Peasant | `peatur` (Крестьянин) | 20 | 0.5625 | sword | `peatur` (Крестьянин) | 50 | 0 |
| Pikemen 17c | `pikeman` (Пикинер 17в.) | 8 | 0.4688 | pike | `pikeman` (Пикинер 17в.) | 90 | 0 |
| Pikemen 18c | `pikeman18` (Пикинер 18в.) | 9 | 0.2812 | pike | `pikeman18` (Пикинер 18в.) | 85 | 0 |
| Light Infantry | `roundshierdip` (Рундашир (наемник)) | 6 | 0.4688 | sword | `roundshierdip` (Рундашир (наемник)) | 75 | 0 |
| Musketeers 17c | `musketeer` (Мушкетер 17в.) | 12 | 4.69 | bullet | `musketeer` (Мушкетер 17в.) | 70 | 0 |
| Musketeers 18c | `musketeer18` (Мушкетер 18в.) | 16 | 4.69 | bullet | `musketeer18pru` (Мушкетер 18в.) | 100 | 0 |
| Grenadiers | `grenadierdip` (Гренадер (наемник)) | 16 | 4.69 | bullet | `grenadierdip` (Гренадер (наемник)) | 30 | 0 |
| Archers | `archerturdip` (Турецкий лучник (наемник)) | 100 | 0.78 | firearrow | `archerdip` (Лучник (наемник)) | 20 | 0 |
| Light Cavalry | `lightcavalrydip` (Легкий кавалерист (наемник)) | 18 | 2.25 | bullet | `lightcavalry` (Легкий кавалерист) | 175 | 0 |
| Dragoons | `dragoon18dip` (Драгун 18в. (наемник)) | 18 | 2.25 | bullet | `dragoon` (Драгун 17в.) | 220 | 0 |
| Heavy Cavalry | `wingedhussar` (Крылатый гусар) | 14 | 0.375 | pike | `cuirassier` (Кирасир) | 300 | 0 |
| Cannons | `cannon` (Пушка) | 1800 | 10.94 | cannonball | `cannon` (Пушка) | 9000 | 75 |
| Mortars | `howitzer` (Гаубица) | 4000 | 18.75 | cannonball | `howitzer` (Гаубица) | 3000 | 75 |

### Матрица контр-эффективности — TTK в g-сек

Строки = **атакующий**. Колонки = **защищающийся**. Ячейка = TTK (game-sec). Зелёные/низкие = атакующий быстро убивает; красные/высокие = защитник долго стоит.

| Atk \ Def | Pea | Pik17 | Pik18 | LtInf | Mus17 | Mus18 | Gren | Arch | LtCav | Drag | HvCav | Cnn | Mor |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| **Pea** (Peasant) | 1.4 | 2.8 | 2.4 | 2.5 | 2.0 | 2.8 | **0.8** | **0.6** | 4.9 | 6.2 | 11 | _5062_ | _1688_ |
| **Pik17** (Pikemen 17c) | 2.9 | 8.4 | 5.0 | 12 | 4.1 | 5.9 | 1.8 | 1.2 | 10 | 13 | 23 | _4219_ | _1406_ |
| **Pik18** (Pikemen 18c) | 1.6 | 4.2 | 2.7 | 5.3 | 2.2 | 3.1 | **0.9** | **0.6** | 5.5 | 6.9 | 12 | _2531_ | _844_ |
| **LtInf** (Light Infantry) | 3.9 | 11 | 6.6 | 12 | 5.5 | 7.8 | 2.3 | 1.6 | 14 | 17 | 70 | _4219_ | _1406_ |
| **Mus17** (Musketeers 17c) | 20 | 53 | 33 | 88 | 27 | 39 | 12 | 7.8 | 68 | 86 | _704_ | _42210_ | _14070_ |
| **Mus18** (Musketeers 18c) | 15 | 35 | 25 | 44 | 21 | 29 | 8.8 | 5.9 | 51 | 64 | _235_ | _42210_ | _14070_ |
| **Gren** (Grenadiers) | 15 | 35 | 25 | 44 | 21 | 29 | 8.8 | 5.9 | 51 | 64 | _235_ | _42210_ | _14070_ |
| **Arch** (Archers) | **0.4** | **0.7** | **0.7** | **0.6** | **0.5** | **0.8** | **0.2** | **0.2** | 1.4 | 1.7 | 2.3 | _281_ | 94 |
| **LtCav** (Light Cavalry) | 6.2 | 14 | 11 | 17 | 8.8 | 12 | 3.8 | 2.5 | 22 | 28 | 84 | _20250_ | _6750_ |
| **Drag** (Dragoons) | 6.2 | 14 | 11 | 17 | 8.8 | 12 | 3.8 | 2.5 | 22 | 28 | 84 | _20250_ | _6750_ |
| **HvCav** (Heavy Cavalry) | 1.3 | 3.1 | 2.3 | 3.1 | 1.9 | 2.7 | **0.8** | **0.5** | 4.7 | 5.9 | 9.4 | _3375_ | _1125_ |
| **Cnn** (Cannons) | **0.3** | **0.6** | **0.5** | **0.5** | **0.4** | **0.6** | **0.2** | **0.1** | 1.1 | 1.3 | 1.9 | 57 | 19 |
| **Mor** (Mortars) | **0.2** | **0.4** | **0.4** | **0.4** | **0.3** | **0.5** | **0.1** | **0.1** | **0.8** | 1.0 | 1.4 | 43 | 14 |

**Чтение:** жирным — быстро убивает (TTK <1 сек), курсивом — почти не убивает (TTK >100 сек).

### Матрица контр-эффективности с поправкой на промахи (пули/стрелы)

Для bullet/arrow атакующих TTK выше из-за **рассеяния**: на дистанции 15 t мушкетёр попадает только ~33% выстрелов (см. секцию Рассеяние). Здесь TTK умножен на коэффициент промахов:

```
hit_chance(dist) = min(1.0, 1 / (2 × maxdisp))
                 = min(1.0, 1 / (2 × dist × disp × 0.0267))
real_TTK = ideal_TTK / hit_chance
```
Считаю на дистанции 12 t (типичная дистанция боя стрелков), с базовым рассеянием=200 px/3.75 t. Для ближнего боя (cannon/mortar в ближнем бою?) дистанция 6 t как запасное значение. Ниже — относительный TTK для стрелков (только строки: Mus17, Mus18, Arch, Drag, LtCav (если стрельба)):

| Atk \ Def | Pea | Pik17 | LtInf | Mus17 | Gren | Arch | LtCav | HvCav |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| **Mus17** (Musketeers 17c, hit≈41%) | 47 | _127_ | _211_ | _66_ | 28 | 19 | _164_ | _1691_ |
| **Mus18** (Musketeers 18c, hit≈41%) | 35 | _85_ | _106_ | 49 | 21 | 14 | _123_ | _564_ |
| **Gren** (Grenadiers, hit≈41%) | 35 | _85_ | _106_ | 49 | 21 | 14 | _123_ | _564_ |
| **Arch** (Archers, hit≈100%) | 0.4 | 0.7 | 0.6 | 0.5 | 0.2 | 0.2 | 1.4 | 2.3 |
| **LtCav** (Light Cavalry, hit≈41%) | 15 | 35 | 41 | 21 | 9 | 6 | 53 | _203_ |
| **Drag** (Dragoons, hit≈41%) | 15 | 35 | 41 | 21 | 9 | 6 | 53 | _203_ |

**Что добавилось** относительно идеального TTK:
- Стрелки на дистанции 12 t **попадают ~50%** выстрелов → TTK ×2.
- Лучники с disp 175 px (немного лучше) — попадают чуть чаще.
- На большой дистанции (15-17 t у мушкета) — TTK еще +30-50%.
- В **hold-mode формации** урон +7 (с 6 до 13) → TTK падает в ~2 раза. С учётом промахов — формация компенсирует рассеяние примерно как раз.
- **На холме** мушкетёры начинают стрелять на 2-4 t дальше → +1-2 выстрела до того, как враг подойдёт. Эффективный TTK снижается на ~10-30% за счёт лишних залпов.

**Примеры выводов** (на данных стандартной защиты):
- **Пушки / мортиры** против пехоты — TTK <1 (полный убой одним выстрелом за выстрел).
- **Пикинёры** против тяжёлой кавалерии — TTK высокий, потому что у кавалерии есть prot_pike. Но в формации пикинёр даёт значительно больше DPS.
- **Мушкетёры** против пехоты с prot_bullet=4-6 — TTK ~10-15 сек, реалистично.
- **Лёгкая кавалерия** против пушек — низкий TTK (cannon без брони, легко убивается).

## Перекрёстная таблица: апгрейды × характеристики

Какой апгрейд на что влияет. Сводка по `itype` (расшифровано в [05_upgrades.md](05_upgrades.md)). Цены даны для базовой нации (отличаются по нациям — см. [05_upgrades.md](05_upgrades.md)).

**Подсказки по нотации:** `aca.X` = academy.X, `bla.<unit>.1.X` = blacksmith damage X-уровня для юнита. `mil.X` = mill.X. Названия — из локали (en).

### Глобальные апгрейды (academy, mill)

| Апгрейд | Эффект | val | Стоимость (F/W/S/G/I/C) | Что улучшает |
|---|---|---:|---|---|
| `aca.1` (Академия) | **+food eff %** | 40 | F0/W200/S0/G325/I0/C0 | Cultivate new cultures of wheat (harvesting +40%) |
| `aca.2` (Академия) | **+food eff %** | 50 | F0/W2400/S0/G625/I0/C0 | Cultivate new cultures of rye (harvesting +50%) |
| `aca.3` (Академия) | **+food eff %** | 50 | F0/W3600/S0/G850/I0/C0 | Raise agriculturists' salary (harvesting +50%) |
| `aca.4` (Академия) | **+field HP %** | 200 | F0/W1000/S0/G475/I0/C0 | Carry out field melioration (field capacity +200%) |
| `aca.5` (Академия) | **+fish eff %** | 100 | F0/W12400/S0/G2520/I0/C0 | Design new tackle and fishing nets (boat efficiency +100%) |
| `aca.6` (Академия) | **enable unit** | 0 | F0/W12400/S0/G7040/I0/C0 | Develop new woodworking methods (frigate building) |
| `aca.7` (Академия) | **price %** | 0 | F0/W7300/S0/G1220/I0/C0 | Build new shipyards for fishing boats (fishing boat cost -85 |
| `aca.8` (Академия) | **+wood eff %** | 100 | F5500/W0/S0/G550/I0/C0 | Design new woodworking tools (woodcutting efficiency +100%) |
| `aca.9` (Академия) | **+shield** | 85 | F0/W9400/S7850/G1150/I0/C0 | Use new construction materials (durability of buildings +85) |
| `aca.10` (Академия) | **build time %** | -7500000 | F0/W0/S0/G6950/I0/C0 | Raise builders' salary (building construction time -75%) |
| `aca.11` (Академия) | **+shield** | 80 | F0/W0/S16200/G1500/I0/C0 | Research new fortification grades (durability of walls and t |
| `aca.12` (Академия) | **+damage %** | 10 | F0/W0/S0/G0/I5000/C0 | Improve firearms: rifled barrel (fire power +10%) |
| `aca.13` (Академия) | **+damage %** | 10 | F0/W0/S0/G4000/I0/C0 | Research granular gunpowder (fire power +10%) |
| `aca.14` (Академия) | **+damage %** | 15 | F0/W0/S0/G7000/I0/C0 | Research new sulphur purification methods (fire power +15%) |
| `aca.15` (Академия) | **+damage %** | 25 | F0/W0/S0/G0/I0/C11000 | Research new nitre purification methods (fire power +25%) |
| `aca.16` (Академия) | **range %** | 5 | F0/W0/S0/G2000/I12150/C0 | Research improved additions to gunpowder formula (artillery  |
| `aca.17` (Академия) | **range %** | 10 | F0/W0/S3000/G4550/I19200/C0 | Design new barrel types: unicorn, carronade (artillery range |
| `aca.18` (Академия) | **HP %** | 50 | F0/W0/S0/G500/I3830/C1500 | Design more durable gun carriage: Gribovalle system (artille |
| `aca.19` (Академия) | **enable unit** | 0 | F0/W0/S0/G1500/I0/C2500 | Design multi-barrelled cannon |
| `aca.20` (Академия) | **accuracy %** | -35 | F0/W3540/S0/G2000/I0/C7250 | Research new sighting devices for artillery (artillery accur |
| `aca.21` (Академия) | **healing** | 25 | F0/W350/S0/G100/I0/C250 | Finance artillery repair shops (repair all artillery) |
| `aca.22` (Академия) | **geology** | 0 | F0/W0/S0/G250/I0/C0 | Develop geology (previously hidden deposits appear on the ma |
| `aca.23` (Академия) | **+stone eff %** | 100 | F0/W0/S0/G1550/I3000/C0 | Develop mining (stone excavation efficiency +100%) |
| `aca.24` (Академия) | **+stone eff %** | 200 | F4200/W0/S0/G1550/I0/C12520 | Raise miners' salary (stone excavation efficiency +200%) |
| `aca.25` (Академия) | **balloon** | 0 | F0/W0/S0/G5750/I0/C0 | Design Montgolfier (reveals the whole map) |
| `aca.26` (Академия) | **healing** | 50 | F0/W0/S0/G200/I0/C200 | Develop medical science (heals all live units) |
| `aca.27` (Академия) | **accuracy %** | -35 | F0/W9540/S0/G12000/I0/C65200 | Develop mathematics (artillery accuracy +35%) |
| `aca.28` (Академия) | **speed %** | 40 | F0/W65400/S0/G24050/I0/C0 | Design new rigging types (ship speed +40%) |
| `aca.29` (Академия) | **enable unit** | 0 | F0/W32300/S0/G6800/I9000/C12800 | Design new rib system and new hulls (battleship construction |
| `aca.30` (Академия) | **build time %** | -5000000 | F0/W2300/S42700/G1150/I0/C0 | Train carpenters (shipbuilding speed x10) |
| `aca.31` (Академия) | **reload %** | -30 | F0/W0/S6000/G5500/I4200/C0 | Design wheellock (rate of fire +30%) |
| `aca.32` (Академия) | **price %** | 0 | F0/W0/S0/G6050/I0/C7750 | Design flintlock (musket cost -50%) |
| `aca.33` (Академия) | **reload %** | -30 | F0/W5000/S0/G5500/I0/C15200 | Design paper cartridge and iron ramrod (rate of fire +30%) |
| `aca.34` (Академия) | **+shield** | 2 | F0/W0/S0/G9750/I0/C0 | Research improved steel grades for cuirasses (armoured soldi |
| `aca.35` (Академия) | **+damage** | 5 | F0/W0/S0/G11500/I0/C0 | Design bayonet: barrel-inserted, bayonet with a tube (cold s |
| `aca.36` (Академия) | **+damage %** | 25 | F0/W0/S0/G19500/I0/C0 | Research new steel grades (18c musketeer/grenadier melee att |

**Стек апгрейдов по эффектам** (накопительно):

- **+food extraction**: `mil.1` (+140%? note: mill upgrade values vary) + `aca.1` (+40%) + `aca.2` (+50%) + `aca.3` (+50%). Eff может выйти на 100+140+40+50+50 = **380%**.
- **+wood extraction**: `aca.8` (+100%). Удваивает wood/trip.
- **+stone extraction**: `aca.23` (+100%) + `aca.24` (+200%). До 100+100+200 = **400% eff**.
- **+fishing**: `aca.5` (+100%). Удваивает `fishingmax` лодки → 1000→2000.
- **+field HP** (`fieldlife`): `aca.4` (+200) + `bla.1` (+100). Меняет урон полю с 100/удар до 25/удар → +4× food per field.
- **+firearm damage %**: `aca.12` (+10) + `aca.13` (+10) + `aca.14` (+15) + `aca.15` (+25) = **+60% урона** для всех bullet/arrow юнитов.
- **+artillery range %**: `aca.16` (+5) + `aca.17` (+10) = **+15% range**.
- **+artillery accuracy %**: `aca.20` (-35%) + `aca.27` (-35%) = **-70% рассеяния** (почти точные выстрелы).
- **+artillery durability %**: `aca.18` (+50%).
- **+firearm reload %**: `aca.31` (-30%) + `aca.33` (-30%) = **-60% к перезарядке** (скорость стрельбы +250%). Применяется ко **ВСЕМ стрелкам с пулевым оружием** — мушкетёрам, стрельцам, янычарам, драгунам и пр. (через `garr_UnitsShooters` / `garr_UnitsBayonet`), не только артиллерии.
- **+building shield**: `aca.9` (+85, всех зданий) + `aca.11` (+80, walls/towers).
- **+building speed**: `aca.10` (-75% buildtime).
- **+ship speed**: `aca.28` (+40%).
- **Разовые эффекты**: `aca.21` (лечит артиллерию), `aca.22` (геология — открывает шахты), `aca.25` (Монгольфьер — открывает карту), `aca.26` (лечит всех юнитов), `aca.30` (×10 скорость постройки кораблей), `aca.32` (-50% стоимость мушкетов).
- **Открывают юниты**: `aca.6` (фрегат), `aca.19` (многоствольная пушка), `aca.29` (линейный корабль).

### Поюнитные апгрейды (blacksmith / barracks / stable)

Кузница (`bla`), бараки (`bar`/`ba2`), конюшня (`sta`) содержат **поюнитные апгрейды урона и защиты** (5 уровней + специальный 7-й уровень). Формат sid: `<nat><place>.<unit>.<itype>.<level>` где itype=1 (damage) или 2 (protection).

Пример полного стека для **rusbar.pikemanrus** (Russian Spearman):
- 5 уровней damage (`.1.1` … `.1.5`): +1, +2, +2, +1, +2 = **+8 к урону**
- 5 уровней protection (`.2.1` … `.2.5`): +1, +1, +2, +1, +1 = **+6 к защите** (pike, sword, arrow)
- Level 7 unique (`.1.6` / `.2.6`): +2 к урону / +2 к защите (переопределение для rus)
- **Полный стек: +10 к урону / +8 к защите** на полностью прокачанном русском пикинёре.

Полный список — в [05_upgrades.md](05_upgrades.md) (~4500 строк, по местам).

## Стоимость одного выстрела

Многие огнестрельные юниты, башни и корабли тратят `iron` / `coal` / `gold` за каждый выстрел (независимо от цены постройки самого юнита). Это отдельный налог, помимо `consume[gold]` и `food upkeep`.

Строки сгруппированы по `(sid, оружие)`: если значения одинаковы для всех наций, показано одной строкой с `nation = all`. Если у нации своё значение — она в отдельной строке.

| Юнит | Нации | weapon | урон | перезарядка (с) | shots/min | iron / выстрел | coal / выстрел | gold / выстрел |
|---|---|---|---:|---:|---:|---:|---:|---:|
| **Лучник** `archer` | alg | `OSTRELA` | 150 | 3.91 | 15.3 | — | — | — |
| **Лучник** `archer` | alg | `STRELA` | 15 | 2.34 | 25.6 | — | — | — |
| **Лучник (наемник)** `archerdip` | all | `OSTRELA` | 100 | 0.78 | 76.9 | — | — | — |
| **Лучник (наемник)** `archerdip` | all | `STRELA` | 25 | 2.5 | 24.0 | — | — | — |
| **Лучник кланов** `archersco` | sco | `OSTRELA` | 150 | 4.38 | 13.7 | — | — | — |
| **Лучник кланов** `archersco` | sco | `STRELA` | 20 | 3.12 | 19.2 | — | — | — |
| **Турецкий лучник** `archertur` | tur | `OSTRELA` | 150 | 4.38 | 13.7 | — | — | — |
| **Турецкий лучник** `archertur` | tur | `STRELA` | 20 | 2.66 | 22.6 | — | — | — |
| **Турецкий лучник (наемник)** `archerturdip` | all | `OSTRELA` | 100 | 0.78 | 76.9 | — | — | — |
| **Турецкий лучник (наемник)** `archerturdip` | all | `STRELA` | 25 | 2.5 | 24.0 | — | — | — |
| **Линейный корабль** `battleship` | all | `PPOINTTKOR` | 1800 | 0.62 | 96.8 | 5 | 15 | — |
| **Пушка** `cannon` | all | `PPOINTT` | 1800 | 10.94 | 5.5 | 20 | 40 | — |
| **Пушка** `cannon` | all | `PSMPOINTTPUS` | 0 | 10.94 | 5.5 | 24 | 21 | — |
| `chaika` | ukr | `PPOINTTKOR` | 1000 | 2.34 | 25.6 | 4 | 9 | — |
| **Егерь** `chasseur` | fra | `SHOTMUSKET` | 20 | 5.94 | 10.1 | 4 | 8 | — |
| **Драгун 17в.** `dragoon` | aus, bav, den, eng, fra, hun, net, pie, pol, por, pru, sax, spa, swe, swi, ven | `SHOTMUSKET` | 15 | 5.62 | 10.7 | 2 | 4 | — |
| **Драгун 18в.** `dragoon18` | aus, bav, den, eng, pol, por, pru, rus, sax, spa, swe, swi, ven | `SHOTMUSKET` | 19 | 5.31 | 11.3 | 4 | 5 | — |
| **Драгун 18в. (наемник)** `dragoon18dip` | all | `SHOTMUSKET` | 18 | 2.25 | 26.7 | 5 | 8 | — |
| **Драгун 18в.** `dragoon18fra` | fra | `SHOTMUSKET` | 10 | 4.69 | 12.8 | 3 | 3 | — |
| **Драгун 18в.** `dragoon18net` | net | `SHOTMUSKET` | 17 | 5.0 | 12.0 | 3 | 4 | — |
| **Драгун 18в.** `dragoon18pie` | pie | `SHOTMUSKET` | 19 | 5.0 | 12.0 | 4 | 5 | — |
| **Посполитое рушение** `dragoonpol` | pol | `SHOTMUSKET` | 13 | 5.0 | 12.0 | 2 | 3 | — |
| **Башня** `eurtow` | aus, bav, den, eng, fra, hun, net, pie, pol, por, pru, sax, sco, spa, swe, swi, ven | `cannonball` | 1000 | 12.5 | 4.8 | 10 | 30 | — |
| **Рибадекин** `framegun` | sco | `PPOINTTFRAME` | 500 | 2.81 | 21.4 | 30 | 40 | — |
| **Фрегат** `frigate` | all | `PPOINTTKOR` | 1800 | 2.34 | 25.6 | 25 | 35 | — |
| **Галера** `galley` | all | `DIMMORT2KOR` | 1000 | 1.56 | 38.5 | 4 | 9 | — |
| **Галера** `galley` | all | `PPOINTTKOR` | 100 | 4.69 | 12.8 | 4 | 9 | — |
| **Гайдук** `gauduk` | hun | `SHOTMUSKET` | 9 | 3.12 | 19.2 | 1 | 2 | — |
| **Гренадер** `grenadier` | aus, eng, fra, net, pie, pol, por, pru, rus, spa, swe, swi, ven | `SHOTMUSKET` | 16 | 5.31 | 11.3 | 2 | 3 | — |
| **Гренадер** `grenadierbav` | bav | `SHOTMUSKET` | 19 | 5.31 | 11.3 | 3 | 3 | — |
| **Гренадер** `grenadierden` | den | `SHOTMUSKET` | 19 | 5.94 | 10.1 | 3 | 3 | — |
| **Гренадер (наемник)** `grenadierdip` | all | `SHOTMUSKET` | 16 | 4.69 | 12.8 | 2 | 5 | — |
| **Гренадер** `grenadierhun` | hun | `SHOTMUSKET` | 16 | 5.31 | 11.3 | 2 | 3 | — |
| **Гренадер** `grenadierpru` | pru | `SHOTMUSKET` | 16 | 4.38 | 13.7 | 2 | 3 | — |
| **Гренадер** `grenadiersax` | sax | `SHOTMUSKET` | 19 | 5.31 | 11.3 | 3 | 3 | — |
| **Шотландский стрелок** `highlander` | eng | `SHOTMUSKET` | 16 | 5.0 | 12.0 | 3 | 4 | — |
| **Гаубица** `howitzer` | all | `DIMMORT1` | 4000 | 18.75 | 3.2 | 20 | 100 | — |
| **Доброволец** `jagerpor` | por | `SHOTMUSKET` | 10 | 5.94 | 10.1 | 2 | 4 | — |
| **Егерь** `jagerswi` | swi | `SHOTMUSKET` | 20 | 6.88 | 8.7 | 4 | 9 | — |
| **Янычар** `jannisary` | tur | `SHOTMUSKET` | 12 | 4.69 | 12.8 | 3 | 5 | — |
| **Королевский мушкетер** `kingmusketeer` | fra | `SHOTMUSKET` | 43 | 6.88 | 8.7 | 6 | 10 | — |
| **Легкий кавалерист** `lightcavalry` | hun | `SHOTMUSKET` | 14 | 5.31 | 11.3 | 2 | 3 | — |
| **Легкий кавалерист (наемник)** `lightcavalrydip` | all | `SHOTMUSKET` | 18 | 2.25 | 26.7 | 5 | 8 | — |
| **Мортира** `mortar` | all | `DIMMORT2` | 200 | 7.81 | 7.7 | 20 | 30 | — |
| **Многоствольное орудие** `multicannon` | aus, bav, den, eng, fra, hun, net, pie, pol, por, pru, rus, sax, spa, swe, swi, ven | `PSMPOINTT` | 500 | 1.88 | 31.9 | 40 | 30 | — |
| **Мушкетер 17в.** `musketeer` | bav, den, eng, fra, pie, por, pru, sax, swe, swi, ven | `SHOTMUSKET` | 12 | 4.69 | 12.8 | 2 | 4 | — |
| **Мушкетер 18в.** `musketeer18` | aus, eng, fra, hun, net, pie, pol, por, rus, spa, swe, swi, ven | `SHOTMUSKET` | 16 | 4.69 | 12.8 | 2 | 3 | — |
| **Мушкетер 18в.** `musketeer18bav` | bav | `SHOTMUSKET` | 22 | 5.94 | 10.1 | 3 | 4 | — |
| **Мушкетер 18в.** `musketeer18den` | den | `SHOTMUSKET` | 29 | 5.94 | 10.1 | 4 | 5 | — |
| **Мушкетер 18в.** `musketeer18pru` | pru | `SHOTMUSKET` | 22 | 4.69 | 12.8 | 3 | 4 | — |
| **Мушкетер 18в.** `musketeer18sax` | sax | `SHOTMUSKET` | 19 | 4.38 | 13.7 | 3 | 3 | — |
| **Мушкетер 17в.** `musketeeraus` | aus | `SHOTMUSKET` | 12 | 5.0 | 12.0 | 2 | 4 | — |
| **Мушкетер 17в.** `musketeernet` | net | `SHOTMUSKET` | 10 | 3.75 | 16.0 | 1 | 3 | — |
| **Мушкетер 17в.** `musketeerpol` | pol | `SHOTMUSKET` | 9 | 3.12 | 19.2 | 1 | 2 | — |
| **Мушкетер Ковенанта** `musketeersco` | sco | `SHOTMUSKET` | 12 | 4.69 | 12.8 | 2 | 5 | — |
| **Мушкетер 17в.** `musketeerspa` | spa | `SHOTMUSKET` | 15 | 5.94 | 10.1 | 3 | 6 | — |
| **Пандур** `pandur` | aus | `SHOTMUSKET` | 17 | 4.69 | 12.8 | 3 | 6 | — |
| **Секей** `pandurhun` | hun | `SHOTMUSKET` | 19 | 5.0 | 12.0 | 3 | 7 | — |
| **Порт** `porpor` | por | `cannonball` | 1000 | 8.75 | 6.9 | 10 | 30 | — |
| **Башня** `rustow` | rus | `cannonball` | 1000 | 9.38 | 6.4 | 10 | 30 | — |
| **Сердюк** `serdiuk` | ukr | `SHOTMUSKET` | 12 | 4.06 | 14.8 | 3 | 6 | — |
| **Стрелец** `strelet` | rus | `SHOTMUSKET` | 12 | 4.69 | 12.8 | 2 | 4 | — |
| **Татарин** `tatar` | tur | `STRELA` | 15 | 1.56 | 38.5 | — | — | — |
| **Башня** `turtow` | alg, tur | `cannonball` | 1200 | 15.62 | 3.8 | 15 | 40 | — |
| **Шебека** `xebec` | alg, tur | `PPOINTTKOR` | 1800 | 1.56 | 38.5 | 25 | 35 | — |
| **Яхта** `yacht` | all | `PPOINTTKOR` | 1000 | 10.94 | 5.5 | 4 | 9 | — |
| **Турецкая яхта** `yachttur` | tur | `PPOINTTKOR` | 1000 | 10.94 | 5.5 | 4 | 9 | — |