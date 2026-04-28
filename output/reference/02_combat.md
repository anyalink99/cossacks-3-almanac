# 02. Бой и движение

[← Index](README.md)

## Содержание

- [Damage formula (полная)](#damage-formula)
- [Headshot — критический удар](#headshot-критический-удар--главная-скрытая-механика)
- [Формационные бонусы (LINE/SQUARE/KARE)](#формационные-бонусы)
- [Dispersion — рассеяние выстрелов](#dispersion--почему-выстрелы-промахиваются)
- [uniqrnd — индивидуальное случайное число юнита](#uniqrnd--индивидуальное-случайное-число-юнита)
- [AoE damage cap](#aoe-damage-cap--как-кучкование-защищает)
- [Высокая позиция (high ground)](#высокая-позиция-high-ground)
- [Score multipliers](#score-за-убийство)
- [Standground / bartprepare — режимы атаки](#standground--bartprepare--режимы-атаки)
- [RunAway — авто-кайтинг стрелков](#runaway--авто-кайтинг-стрелков)
- [Friendly fire — дружественный огонь](#friendly-fire--дружественный-огонь)
- [Multi-weapon switching (картечь, штык, огненные стрелы)](#multi-weapon-switching--переключение-оружия-по-дистанции)
- [Movement penalty к дальности (standtime)](#movement-penalty--штраф-к-дальности-при-движении)
- [Idle bonus к дальности (addradius)](#idle-bonus--бонус-к-дальности-в-покое)
- [Capture mechanic — захват юнитов](#capture-mechanic--захват-юнитов)
- [Priest healing — лечение священниками](#priest-healing--лечение-священниками)
- [Shield /3 при недостроенном здании](#shield-3-при-недостроенном-здании)
- [AI aggression flip от damage](#ai-aggression-flip--ai-переходит-в-атаку-от-одного-удара)
- [Officers — миф о combat-aura](#officers--миф-о-combat-aura)
- [Чего НЕТ в игре](#чего-нет-в-игре-confirmed-absent)
- [Свойства damage formula](#свойства-damage-formula)
- [Типы оружия](#типы-оружия-gc_obj_weapon_kind_)
- [Скорости юнитов](#скорости-юнитов)
- [Офицеры и формации](#офицеры-и-формации)
- [Counter matrix (приближённый TTK)](#counter-matrix-приближённый-ttk)
- [Upgrade × stat cross-reference](#upgrade--stat-cross-reference)
- [Стоимость одного выстрела](#стоимость-одного-выстрела)

## Damage formula

```
damage = weapon.damage

# 1. Anti-headshot для мобильной кавалерии
if (target.usage == fasthorse AND target is on the move
    AND weapon.kind in {arrow, bullet}):
    damage -= 5  # 'penalty' shot — лёгкая кавалерия на ходу труднее ловится

# 2. Shield (одно из главных свойств танков)
if (target.bbuilt):
    damage -= target.shield
else:  # ещё строится
    damage -= target.shield // 3

# 3. Squad shield bonus (формация)
if (target in formation):
    damage -= squad.fAddShieldHold  (если hold-mode)
    damage -= squad.fAddShield      (иначе)

# 4. Squad damage bonus у атакующего (формация)
if (attacker in formation AND weapon.kind != firearrow):
    damage += squad.fAddDamageHold  (если hold-mode)
    damage += squad.fAddDamage      (иначе)

# 5. Protection
damage -= target.protection[weapon.kind]

# 6. HEADSHOT — критический удар
bCanHeadShot = (weapon.kind in {arrow, bullet}) AND (target NOT building)
bHeadShot = bCanHeadShot AND (random < 0.05)  AND (NOT fast-cavalry-on-the-move)
if bHeadShot:
    damage += floor(attacker.uniqrnd * 500)  # +0..+499 hp бонусного урона!

damage = max(1, damage)  # минимум 1 хп
target.hp -= damage
```
Источник: `miscext2.script:_misc_DoDamage` (строки 274-510).

### Headshot (критический удар) — главная скрытая механика

**5% шанс на каждый выстрел** добавить `floor(uniqrnd × 500)` damage. Где `uniqrnd` — фиксированное случайное число юнита-стрелка [0..1].

**Ключевые свойства:**

- Работает только для **arrow** и **bullet** оружия.
- НЕ работает по **зданиям**.
- НЕ работает по **light cavalry на ходу** (`usage=fasthorse + state=walk`) — у них наоборот -5 dmg штраф.
- `uniqrnd` **зафиксирован при спавне** юнита-стрелка → у каждого индивидуального мушкетёра свой headshot damage. В отряде из 36 мушкетёров будут «снайперы» (uniqrnd≈0.9 → +450 dmg) и «мазилы» (uniqrnd≈0.05 → +25 dmg).
- Среднее ожидаемое: `0.05 × 250 = 12.5` дополнительного damage на выстрел (выровненный по случайным uniqrnd ~0.5).

**Пример:** мушкетёр стреляет в Reiter (282 hp). Обычный damage — 6 hp. На случайном выстреле (5%) случается headshot, и тот же мушкетёр (uniqrnd≈0.252) наносит `6 + floor(0.252 × 500) = 6 + 126 = 132 hp`. Reiter падает с 282 → 150 hp.

**Почему это важно для стратегии:**

- Стрелковые отряды против Heavy Cavalry/Light Infantry статистически окупаются сильно лучше чем damage formula показывает.
- Light Cavalry **в движении** иммунна к headshot → главный counter к стрелковому отряду.
- C1 имел 4% шанс instant-kill (комментарий в коде); в C3 механика была ребалансирована в текущий вариант. Комментарий упоминает 2%, но в реальном коде осталось `<0.05` = **5%**.

### Формационные бонусы

Источник: [`data/game/var/formations.cfg`](file:///C:/Program%20Files%20(x86)/Steam/steamapps/common/Cossacks%203/data/game/var/formations.cfg)

Юниты в строю получают **+damage / +shield** к каждому выстрелу/попаданию. В **hold-mode** (приказ «Стоять») бонусы значительно больше:

| Формация | размер | regular dmg/shield | **hold-mode dmg/shield** |
|---|---:|---:|---:|
| LINE / SQUARE / KARE | 15-196 | +2 / +2 | **+7 / +7** |
| LINE / SQUARE / KARE | **400** | **+3 / +3** | **+7 / +7** |
| Cavalry (PRUS, SHER, TRI) | любой | +1 / +1 | +1 / +1 |

**Ключевое:** мушкетёр с base damage 6 → **в LINE-формации hold-mode наносит 13 damage** за выстрел (6 + 7 hold). И принимает -7 от каждого входящего попадания (поверх protection).

**Что это значит для боя:**
- Стрелковые отряды в **hold-mode на формации** = **+117% damage** (с 6 до 13).
- Без формации (рассыпная) — никаких бонусов.
- Кавалерийские формации (treugol'nik, klin) дают только +1/+1 — формация для них не главное.
- **firearrow** (зажигательная стрела) НЕ получает squad damage bonus.

### AoE damage cap — как кучкование защищает

Источник: [`miscext2.script:_misc_DoRoundDamage:576`](file:///C:/Program%20Files%20(x86)/Steam/steamapps/common/Cossacks%203/data/scripts/lib/miscext2.script)

Взрывы (cannon, mortar, gun, grenade) попадают по всем юнитам в радиусе `r`, **но только первые N получают damage**:

```
count = floor(1 + (r / 0.35)²)
```
| Оружие | radius | максимум юнитов под взрыв |
|---|---:|---:|
| Cannon (ядро) | ~1 t | **9** |
| Mortar (бомба) | ~2 t | **33** |
| Grenade (граната) | ~0.5 t | **3** |
| Howitzer | ~1 t | **9** |

**Стратегический вывод:** **плотная толпа защищена** — 50 юнитов в одной точке теряют максимум 9 от ядра, остальные нетронуты. Растянутая линия страдает гораздо больше.

Стрелы с зажигалкой (`barrow`) имеют другую логику: damage всем в радиусе если юнитов в области <= 300; иначе только тем, кто внутри строгого `r`.

### Высокая позиция (high ground)

Источник: [`unit.script:5469, 7272`](file:///C:/Program%20Files%20(x86)/Steam/steamapps/common/Cossacks%203/data/scripts/lib/unit.script)

Если ranged-юнит стоит на возвышенности (Y > 0), его **search distance** увеличивается:

```
searchdist += goHeight × 2  (только для ranged юнитов: minsearchdist > melee_radius)
```
- `goHeight` — Y-координата юнита в тайлах (высота над уровнем 0).
- Бонус **только к detection range** (видят дальше / start firing раньше).
- Сам выстрел (`radiusmax`) технически тот же, но если враг ещё не в радиусе атаки, юнит начинает движение и выстрелит как только цель войдёт в radius. На практике **мушкетёры с холма стреляют по атакующим раньше** = больше выстрелов до melee.
- НЕ работает на melee юнитов (pikemen в milee remain melee).
- Холмы на карте создаются по `relief` map gen параметру (Highlands map даёт максимум гор).

### Score за убийство

Источник: [`miscext2.script:445-461`](file:///C:/Program%20Files%20(x86)/Steam/steamapps/common/Cossacks%203/data/scripts/lib/miscext2.script)

- За убийство юнита: **score += target.score × 2**
- За убийство **наёмника-внутри-дип-центра**, юнита-в-транспорте, и т.п.: **score += inside_unit.score × 3**
- Эти бонусы складываются (1 ракетой убил наёмника в дип-центре + само здание = score за оба)

### Standground / bartprepare — режимы атаки

Источник: [`unit.script:7259-7286`](file:///C:/Program%20Files%20(x86)/Steam/steamapps/common/Cossacks%203/data/scripts/lib/unit.script), [`player.script:2456-2463`](file:///C:/Program%20Files%20(x86)/Steam/steamapps/common/Cossacks%203/data/scripts/lib/player.script)

**Главный механизм:** дальность авто-обнаружения врага (`maxsearchdist`) **радикально различается** в режимах standground и обычном:

```
if (bstandground AND order != move):
    maxsearchdist := MIN(searchradius, GetMaxAttackRadius)   # полная дальность оружия
else:
    maxsearchdist := minsearchdist + 0.375                    # почти melee (!)
```
**Что это значит на практике:**

- **Без standground** мушкетёр (radiusmax≈9 t) обнаруживает врага только когда тот входит в **0.375 t от minsearchdist** — то есть подходит вплотную. Получается **1-2 выстрела** и сразу melee. Это объясняет почему стрелковые юниты «стоят и не стреляют» по дальним целям.
- **С standground** обнаружение работает на полную `searchradius` (1500-2400 px ≈ 28-45 t). Мушкетёр стреляет по любому врагу в радиусе обзора — успевает 5-10 выстрелов до melee.
- **Standground также отключает RunAway** (см. ниже): юнит держит позицию, не пытается отступать.
- **Move-приказы стирают standground**: если юниту приказали идти куда-то, он не стреляет даже если bstandground=True (см. условие `order != move` в коде).

**bartprepare** (artillery preparation) — флаг для **артиллерии, башен и портов**. Установлен на `cannon`, `howitzer`, `framegun`, `multicannon`, `tow` (towers), `port` (shipyards). При получении `attackpoint`-приказа (по площади) такие юниты:

- Принудительно выключают `bstandground` → переходят в обычный режим обнаружения
- Принудительно включают `bsearchenemy` → активно сканируют цели вокруг точки
- Получают приказ `attackpoint(trgx, trgz)` с задержкой подготовки (`attackdelay/attackmaxdelay`)

**Стратегические выводы:**

- **Всегда ставь стрелков в standground** при обороне или подготовленной засаде. Без него мушкетёры сделают 1-2 выстрела вместо 5-10.
- **При продвижении** (`bstandground=False`) стрелки кайтят (RunAway) — это иногда плюс (не дают подойти), иногда минус (тормозят свой же штурм).
- **Артиллерию лучше use attackpoint** (Ctrl+ЛКМ) — `bartprepare` правильно настраивает режимы. Если просто переместить пушку и ждать — она в movement-режиме НЕ откроет огонь.

### RunAway — авто-кайтинг стрелков

Источник: [`unit.script:7363-7369`](file:///C:/Program%20Files%20(x86)/Steam/steamapps/common/Cossacks%203/data/scripts/lib/unit.script)

Если у стрелкового юнита (`minsearchdist > 0`, т.е. min range > 0) враг входит в **мёртвую зону** (между 0 и `minsearchdist`), юнит автоматически отступает:

```
if (cell_search_found_no_target AND враг_в_minsearchdist):
    if (NOT bstandground)
       AND (standtime=0 OR standtime > gc_unit_runawaydelay (1.3 sec)
            OR (player_is_human AND difficulty <= normal)):
        DoRunAway(toward_safe_direction, distance=gc_unit_runawaydist (3.5 t))
```
**Условия отступления (все должны выполниться):**

- Юнит **не в standground**.
- Юнит либо только что подошёл (`standtime=0`), либо стоит уже >1.3 сек, либо игрок-человек на easy/normal сложности (поблажка для новичков).
- Враг — в `minsearchdist` зоне.

**Эффект:** стрелок отступает на 3.5 тайла от врага, пытаясь восстановить дистанцию для выстрела. Это создаёт классический **kiting-pattern** мушкетёров: подошёл → стрельнул → отступил → стрельнул.

**Когда RunAway ВЫКЛЮЧЕН:**

- В `standground` (явный приказ держать позицию).
- AI-противник на hard+ — продолжает стрелять до самого melee, не отступает (опасный нюанс).
- На AI-hard+ человеческий игрок: AI кайтит как обычно, но human player на hard+ тоже не получает RunAway-помощь.

**Стратегические выводы:**

- Для отступательной тактики (kite-and-shoot) — **сними standground** и работай по уязвимой кавалерии/пехоте.
- Для удержания позиции (например, на холме) — **standground обязателен**, иначе мушкетёры разбегутся при подходе melee.
- Лёгкая кавалерия может **догнать кайтящих мушкетёров** (fasthorse=96 vs default=32 → ~3× быстрее).

### Friendly fire — дружественный огонь

Источник: [`miscext2.script:_misc_DoDamage:274`](file:///C:/Program%20Files%20(x86)/Steam/steamapps/common/Cossacks%203/data/scripts/lib/miscext2.script), [`weapon.script:482-492`](file:///C:/Program%20Files%20(x86)/Steam/steamapps/common/Cossacks%203/data/scripts/lib/weapon.script), [`unit.script:7686-7714`](file:///C:/Program%20Files%20(x86)/Steam/steamapps/common/Cossacks%203/data/scripts/lib/unit.script)

**Дружественный огонь ВКЛЮЧЁН для большинства снарядов.** В функции `_misc_DoDamage` **нет проверки на team/owner** — урон применяется к любому объекту, попавшему под траекторию.

**Что попадает по своим:**

- Стрелы лучников (`STRELA`, `OSTRELA` fire arrows)
- Пули мушкетов (`SHOTMUSKET`)
- Гранаты (`NUCLGRE`)
- Артиллерия (`PSMPOINTTPUS`, `DIMMORT1`, `DIMMORT2NEW`, `PSMPOINTT`, `DIMMORT2KOR`)
- AoE взрывы (картечь, ядра, бомбы) — поражают **всё в радиусе**, включая своих (`_misc_DoRoundDamage` без team-фильтра).

**Что НЕ ранит союзников:**

- **Корабли** — есть отдельная защита `// prevent ships from friendly fire` в weapon.script. Торговцы и боевые корабли одного игрока не топят друг друга.
- Башни и пушки с `bcheckfriendonline=True` (по умолчанию ON) — **не выстрелят, если на линии огня стоит дружественное здание** (см. `_misc_IsBuildingInRay`). Но это про блокировку выстрела, а не про урон при пролёте.

**Список оружия с явно ОТКЛЮЧЁННОЙ проверкой `bcheckfriendonline`** (стреляют сквозь свои здания, не блокируются):

`STRELA`, `OSTRELA`, `SHOTMUSKET`, `SHOTBLOCKHOUSE`, `NUCLGRE`, `PSMPOINTTPUS`, `DIMMORT1`, `DIMMORT2NEW`, `PSMPOINTT`, `DIMMORT2KOR` — то есть **все стрелы, мушкетные пули и почти вся артиллерия**.

**Стратегические выводы:**

- **Не ставь свою пехоту на линию огня артиллерии** — ядро/бомба прошьёт строй и взорвётся среди своих.
- **Лучники и мушкетёры стреляют сквозь свои ряды** — стой во второй линии без проблем, но **бомба в массу твоих юнитов = твои потери**.
- **Башни без line-of-sight** через здания не выстрелят (если их weapon `bcheckfriendonline=True`), но снаряд при выстреле уже не различает свой/чужой.

### Multi-weapon switching — переключение оружия по дистанции

Источник: [`unit.script:_unit_GetWeaponToAttackIndex:6376-6451`](file:///C:/Program%20Files%20(x86)/Steam/steamapps/common/Cossacks%203/data/scripts/lib/unit.script)

Многие юниты имеют **несколько слотов оружия** (`weapon[0]`, `weapon[1]`, ...). Игра автоматически выбирает нужный слот по дистанции до цели — каждое оружие имеет `radiusmin..radiusmax`. Если враг вошёл в близкий диапазон — выбирается оружие с маленьким `radiusmin`, иначе — дальнее.

Дополнительно учитывается `attmask`: если у цели `mmask` совпадает с `weapon[i].attmask` (материал брони), это оружие приоритетнее. Поэтому fire arrows выбираются для построек (их attmask содержит `gc_obj_material_building`).

**Главные пары:**

**1. Cannon (пушка) — ядро vs картечь:**

| Слот | Тип | dmg | Pause | Range (px) | Когда стреляет |
|---|---|---:|---:|---|---|
| `weapon[0]` PPOINTT | cannonball (ядро) | 1800 | 350 | **550-2160** | дистанция ≥ 550 px (~10.3 t) |
| `weapon[1]` PSMPOINTTPUS | cannister (картечь) | AoE по `gWeapons[]` | 350 | **0-450** | враг ближе 450 px (~8.4 t) |

**Это значит:** если пехота подошла на ~8 тайлов к пушке — она автоматически переходит в картечный режим. **Картечь — массовый урон по толпе** (AoE). Поэтому гасить пушку «навалом пехоты» = получить картечь в упор. **Атаковать пушку нужно растянутой линией** (не больше 9 в радиусе AoE — см. AoE damage cap).

**2. Musketeer 18c — пуля vs штык (bayonet):**

| Слот | Тип | dmg | Pause | Range (px) | Когда стреляет |
|---|---|---:|---:|---|---|
| `weapon[0]` (bayonet) | pike | 5-10 (по нации) | **0** (мгновенно) | **35-65** (~0.66-1.22 t) | в упор |
| `weapon[1]` SHOTMUSKET | bullet | 16-29 (по нации) | 140-190 | **400-900** (~7.5-16.9 t) | дальше 7.5 t |

**Стратегический смысл:** мушкетёр после выстрела не беспомощен в melee — у него **штык** с pause=0 (бьёт каждый animation cycle). Атаковать перезаряжающихся мушкетёров кавалерией = получить штыковой бой. Прусские мушкетёры (dmg штыка 10) сильнее в melee чем баварские (5).

**Прокачки штыка** идут отдельно от прокачек пули — `bla.musketeer18.1.X` качает урон bullet, штык остаётся базовый.

**3. Archer — обычная стрела vs огненная (firearrow):**

| Слот | Тип | dmg | Pause | Range (px) | Dispertion | Особенности |
|---|---|---:|---:|---|---:|---|
| `weapon[0]` STRELA | arrow | 15 | 75 | 400-800 | 175 px | основная стрельба |
| `weapon[1]` OSTRELA | firearrow | **150** | 125 | 400-600 | 200 px | attmask = building+wood+woodwall |

**Огненные стрелы — главное оружие лучников против построек.** Урон 150 (×10 от обычной), но: ниже скорострельность (-40%), хуже точность (+14% дисп.), не получают **squad damage bonus** (см. секцию Headshot/Damage formula). Игра автоматически переключает лучника на OSTRELA когда цель — здание/wood/палисад. **Лучники — лучший анти-билдинг ranged юнит** (если успевают подойти).

**4. Другие multi-weapon юниты** (поищи `weapon[1]` в их sid):

- **Janissary (jannisary)** — пуля + сабля melee.
- **Strelet** — пищаль + бердыш melee.
- **Jaeger / dragoon** — пуля + сабля.
- **Cavalry shooters** (drabant, mounted strelet) — пуля + сабля верхом.

Во всех случаях работа одинакова: близко = melee weapon, далеко = ranged. **Разница cooldown'ов:** например мушкетёр перезаряжается 150 frames пулю и 0 штык — значит **сразу после выстрела** может ткнуть штыком если враг близко (а потом перезарядка пули продолжится в фоне).

### Movement penalty — штраф к дальности при движении

Источник: [`unit.script:8011-8023`](file:///C:/Program%20Files%20(x86)/Steam/steamapps/common/Cossacks%203/data/scripts/lib/unit.script), константа `gc_obj_maxattackradiusdisp = 3` (`dmscript.global:116`)

Юнит, который только что двигался (`standtime < 0.25 sec`), теряет в дальности:

```
if (standtime < 0.25) AND (weapon.kind != cannister):
    if (NOT bArtillery):
        radiusmax -= 3 × uniqrnd          # пехота: до -3 тайла
    else:
        radiusmax -= 3 × uniqrnd × 0.5    # артиллерия: до -1.5 тайла
```
**uniqrnd** — индивидуальный коэффициент юнита (см. секцию uniqrnd выше) ∈ [0..1]. Так что у разных стрелков в отряде штраф разный: «снайперы» (низкий uniqrnd) теряют меньше, «мазилы» (высокий uniqrnd) — почти весь штраф.

**Стратегические выводы:**

- **Стрелок в движении не выстрелит на полную дальность** — нужно ~0.25 сек постоять. Это объясняет почему мушкетёры «промахиваются» по дальним целям при подходе.
- **Картечь не штрафуется** — пушка может бить картечью даже на ходу (но в реальности пушка `bartillery` всё равно `bstandground=True` по умолчанию).
- **Артиллерия штрафуется в 2 раза меньше** — мортира/пушка после короткого movement готова стрелять почти на полную дальность.
- В сочетании с RunAway создаёт **kite-pause-shoot**: мушкетёр отбежал на 3.5 t, ждёт 0.25 сек чтобы вернуть полную дальность, стреляет, и снова кайтит.

### Idle bonus — бонус к дальности в покое

Источник: [`unit.script:8026-8028`](file:///C:/Program%20Files%20(x86)/Steam/steamapps/common/Cossacks%203/data/scripts/lib/unit.script)

Если юнит в состоянии **idle** (флаг `gc_statetag_move_idle`), он получает бонус к дальности:

```
rbonus += weapon[i].addradius   # обычно _misc_PixelsToTiles(32) = ~0.6 тайла
```
**Кому даётся:** мушкетёрам, лучникам, пушкам — у всех `addradius = 32 px = 0.6 t`. Для слабых стен (`gc_obj_usage_weakwall`) — дополнительно **+0.36 тайла** rbonus.

**Эффект:** стационарная защита (например, гарнизон на холме в standground) стреляет на **~0.6 t дальше** чем тот же отряд в движении. Мелочь, но в сочетании с high-ground (см. выше) и устранением movement penalty получается заметный буст эффективной дальности обороны.

### Capture mechanic — захват юнитов

Источник: [`unit.script:7289-7307`](file:///C:/Program%20Files%20(x86)/Steam/steamapps/common/Cossacks%203/data/scripts/lib/unit.script)

Военные юниты могут **захватывать** мирные/нейтральные юниты противника (не убивая). Каждый scan tick (раз в ~0.5 сек) с шансом **5%** проверяется условие захвата:

```
if (random < 0.05) AND (target.bcapture=True) AND (NOT target.bbuilding)
    AND (NOT attacker.bcapture)  # сам не захватываемый
    AND (NOT attacker.media=water)
    AND (target.orderlist.count < cMinCaptureOrdListCount)  # цель «занята делом»
    AND (path_distance(attacker, target) <= attacker.searchradius):
        attacker.OrderMove(target.position)
        attacker.SetOrderTrg(target)  # лочится на захват
```
**Кто может захватывать (`bcancapture=True`):** все военные юниты-некрестьяне.

**Кого можно захватить (`bcapture=True`):**

- Большинство **крестьян** (peasant, peabav, peaaus, ...) — кроме `Ukrainian` и `Scottish` (их крестьяне `bcapture := False` явно).
- **Артиллерия** (`cannon`, `howitzer`, `mortar`, `multicannon`, `framegun`) — `bcapture := True` при определении ([unit.script:1721](file:///C:/Program%20Files%20(x86)/Steam/steamapps/common/Cossacks%203/data/scripts/lib/unit.script)).
- **Здания** (`bbuilding=True`) тоже захватываются (но через отдельный механизм — пехота окружает).

**Стратегические выводы:**

- **Захваченная пушка переходит на твою сторону полностью** — со всеми прокачками атакующей нации! Это очень мощный экономический эффект.
- **Защищай пушки пехотой** — пехота противника в радиусе захвата может «увести» пушку без боя.
- **Украинские/шотландские крестьяне иммунны к захвату** — сильное национальное преимущество (не теряешь экономику от соседа-кавалериста).
- **5% chance per tick** — захват не мгновенный, нужно несколько секунд возле цели. За 5-7 сек шанс ~25-30% завершить попытку.

### Priest healing — лечение священниками

Источник: [`unit.script:1151-1188`](file:///C:/Program%20Files%20(x86)/Steam/steamapps/common/Cossacks%203/data/scripts/lib/unit.script), формула в [`miscext2.script:371-398`](file:///C:/Program%20Files%20(x86)/Steam/steamapps/common/Cossacks%203/data/scripts/lib/miscext2.script)

Священники (`priest`, `pope`, `mullah`, `padre`) лечат союзных юнитов. Используют псевдо-оружие `gc_obj_weapon_kind_heal`. Формула:

```
target.hp += weapon.damage      # БЕЗ shield, БЕЗ protection!
target.hp = min(target.hp, target.maxhp)
```
**Heal pause = 0** — лечат каждый animation cycle (~0.7 сек), пока цель не full HP.

| Юнит | heal/удар | range (px / tiles) | Где доступен |
|---|---:|---|---|
| Priest | 20 | 0-400 / 7.5 t | большинство европейских наций |
| Pope | 25 | 0-350 / 6.6 t | Папская область / Венеция |
| Mullah | 15 | 0-500 / **9.4 t** | Турция / Алжир (самый дальний heal) |
| Padre | 30 | 0-400 / 7.5 t | Испания / Португалия (самый сильный heal) |

**Стратегические выводы:**

- **Heal игнорирует броню** — лечит на полное значение независимо от того, кто-кого защитного.
- **Несколько священников лечат одну цель параллельно** — рейтер с 282 HP лечится 4 priest'ами = +80 HP/cycle = ~115 HP/sec. Можно держать тяжёлую кавалерию вечно.
- **Mullah имеет самую большую дальность** (9.4 t) — лечит из второй линии, недосягаем для melee.
- **Padre самый эффективный** (30/удар) — испанско-португальская армия очень живуча.
- Священники сами **уязвимы** (низкий HP, нет брони) — главный таргет для рейдов.

### Shield /3 при недостроенном здании

Источник: [`miscext2.script:339-342`](file:///C:/Program%20Files%20(x86)/Steam/steamapps/common/Cossacks%203/data/scripts/lib/miscext2.script)

При расчёте damage: если здание **ещё строится** (`bbuilt=False`), его shield делится на 3:

```
if (target.bbuilt):  damage -= shield        # достроено: полный shield
else:                 damage -= shield // 3   # стройка: 1/3 shield
```
**Стратегический смысл:** **сноси здания пока они строятся**. Например, башня на стройке имеет shield ~33 (вместо 100), и каждый удар по ней проходит почти полностью. Контр-стройка (rush на возводимое здание противника) гораздо эффективнее чем атака готового.

Касается ТОЛЬКО зданий — юниты не имеют состояния «строится».

### AI aggression flip — AI переходит в атаку от одного удара

Источник: [`miscext2.script:406-417`](file:///C:/Program%20Files%20(x86)/Steam/steamapps/common/Cossacks%203/data/scripts/lib/miscext2.script)

Любой не-артиллерийский юнит AI, **получивший damage**, флипает свой отряд (`squad`) в `fAgressive=True` и обновляет `fLastBattleTime`.

**Эффект:** один поражающий выстрел/удар по AI-отряду переводит его в боевой режим. AI начинает контратаковать, преследовать, искать врага активно.

**Стратегические выводы:**

- **Поклёвывание AI** (один лучник в крестьянина) **триггерит реакцию всего AI-отряда**. Может быть полезно: отвлекаешь лучником, основная сила атакует с другой стороны.
- AI на artillery (пушки/мортиры) — НЕ флипает (особый case в коде).
- Если хочешь скрытно собрать ресурсы рядом с AI — **не атакуй вообще**, иначе вся армия зашевелится.

### Officers — миф о combat-aura

Источник: [`player.script:810-858`](file:///C:/Program%20Files%20(x86)/Steam/steamapps/common/Cossacks%203/data/scripts/lib/player.script), [`unit.script:163-164`](file:///C:/Program%20Files%20(x86)/Steam/steamapps/common/Cossacks%203/data/scripts/lib/unit.script)

**В игре НЕТ персональной aura-бонуса от офицера.** Офицеры/барабанщики занимают слоты `maskOfficers` в формационной сетке, но в коде **нет** проверок типа `if (officer in radius) then damage += X`.

**Что реально даёт офицер:**

- Без офицера **нельзя сформировать отряд** — а без отряда нет `fAddDamage` / `fAddShield` (см. секцию Формационные бонусы).
- Офицер ходит в составе строя и держит формацию.
- При смерти офицера отряд **рассыпается** → теряет все формационные бонусы (это и есть «потеря aura» которую ощущают игроки).

**Стратегический вывод:** **убийство офицера = убийство всех бонусов отряда**. Если в LINE-формации все мушкетёры имели +7 hold dmg / +7 hold shield — после смерти офицера это всё пропадает мгновенно. **Офицеры — снайперский target №1.**

### Чего НЕТ в игре (confirmed absent)

После проверки `unit.script`, `weapon.script`, `miscext2.script`, `player.script`:

- **НЕТ cavalry charge bonus.** Кавалерия не получает бонусного урона на разгоне или при первом ударе. Поиск `bcharging`/`firsthit`/`chargebonus` ничего не находит. Урон кавалерии = базовый damage оружия.
- **НЕТ anti-horse damage type.** Pikemen не имеют умножителя «×N против кавалерии». Эффективность пикинёра против рейтара — это просто `weapon.damage(pike)` против `target.protection[pike]` где у кавалерии этот protection обычно низкий.
- **НЕТ drummer aura.** Барабанщик — просто слот в формации (формальное наполнение). Не даёт +damage, +speed, +morale.
- **НЕТ grenadier-special arc.** Гранатомёт использует обычный AoE-pipeline (cannonball-kind с explosion radius). Никакого specials у траектории нет.
- **НЕТ stealth/invisibility.** Все юниты видны если в vision'е игрока. Нет флага `bstealth`.

**Что это меняет:** **формация — единственный способ умножить урон**. Никаких скрытых буффов от позиции (кроме high-ground / standground). Прокачки + формация + тип оружия vs тип брони — это вся боевая математика.

### Свойства damage formula

- `protection` и `shield` уменьшают урон **аддитивно** (не процентно).
- **Минимум 1 хп** урона: даже если `protection > damage + bonuses`, пройдёт 1 hp.
- Shield применяется ВСЕГДА (включая поверх protection). Танки с shield эффективнее тяжёлых protection.
- При постройке здания shield делится на 3.
- `firearrow` (зажигательная стрела лучников) НЕ получает squad damage bonus.

### Dispersion — почему выстрелы промахиваются

Источник: [`weapon.script:_weapon_CalcShotDispertion:625`](file:///C:/Program%20Files%20(x86)/Steam/steamapps/common/Cossacks%203/data/scripts/lib/weapon.script)

При каждом выстреле снаряд **рассеивается** относительно цели:

```
maxdisp = dist × disp × 0.0267   # в тайлах
shot_x = target_x + (1 - random*2) × maxdisp
shot_z = target_z + (1 - random*2) × maxdisp
```
Где `dist` — дистанция до цели (тайлы), `disp` — `weapon.dispertion` (тайлы, после _misc_PixelsToTiles). **Чем дальше — тем больше рассеяние** (линейно).

**Базовые значения dispertion** (из unit.script):
| Оружие | dispertion (px / tiles) | На 15 t отклонение |
|---|---:|---:|
| Strelet (SHOTMUSKET, base) | 200 / 3.75 | **±1.50 t** |
| Archer (STRELA) | 175 / 3.28 | ±1.31 t |
| Archer (OSTRELA fire) | 200 / 3.75 | ±1.50 t |
| Musketeer base | 250 / 4.69 | ±1.88 t |
| Cannon (PPOINTT) | ~250 / 4.69 | ±1.88 t |
| Tower (PPOINTTTOW) | ~100 / 1.88 | ±0.75 t |
| Yacht/galley (PPOINTTKOR) | 25 / 0.47 | ±0.19 t |

**Шанс попасть в юнит размером 1×1 t** на дистанции d:

- Если 2×maxdisp ≤ 1 → ~100% попадание
- Если 2×maxdisp > 1 → шанс ≈ 1 / (2×maxdisp) попасть точно в нужный квадрат

Пример: мушкетёр (disp=3.75) на 15 t → maxdisp=1.50, окно ±1.50 = 3.00 → шанс попасть в 1×1 цель ≈ 1/3 = **~33%** одним выстрелом. Это означает что **counter matrix TTK ниже реального в 3 раза для дальних bullet/arrow**.

**Апгрейды dispertion** — только для **артиллерии**:
- `aca.20` (Research new sighting devices for artillery): **-35% dispersion**
- `aca.27` (Develop mathematics): **-35% dispersion** (накапливается с aca.20)
- ⚠ Для **мушкетёров и лучников** прямого dispersion-апгрейда нет.

### uniqrnd — индивидуальное случайное число юнита

При спавне каждый юнит получает `uniqrnd ∈ [0..1]` ([`unit.script:2726`](file:///C:/Program%20Files%20(x86)/Steam/steamapps/common/Cossacks%203/data/scripts/lib/unit.script)). Это **зафиксированное** число, остаётся неизменным до смерти. Используется в **4 механиках одновременно**:

| # | Где применяется | Эффект |
|---:|---|---|
| 1 | Headshot bonus | `+floor(uniqrnd × 500)` дополнительного damage при крите |
| 2 | Эффективная max range | `radiusmax -= uniqrnd × 3` тайла. Каждый стрелок шарашит чуть на разную дистанцию (асинхронные залпы) |
| 3 | Search timing | `nextSearch = now + uniqrnd × 0.15 + 0.3` сек. Юниты не сканируют синхронно |
| 4 | Multiplayer sync seed | `SetRandomKey(floor(uniqrnd × MaxInt))` для синхронизации |

Эффекты — это **trade-off** built into каждый юнит: высокий uniqrnd → большие криты, но меньшая дальность. Низкий → дальше стреляет, но слабее криты.

В C3 разработчики **специально расширили base range на +100 px** для лучников (`unit.script:999` комментарий: `// c3 added range +100 cause of uniqrnd range dispertion`) — компенсировать uniqrnd usage #2.

## Типы оружия (gc_obj_weapon_kind_*)

| Kind | Описание | Носители |
|---|---|---|
| `pike` | Длинное копьё/пика | Pikemen, Pikeman18 |
| `sword` | Меч/сабля | Light infantry, swordsmen, кавалерия в melee |
| `bullet` | Пуля огнестрела | Musketeer, Strelet, Janissary, Dragoon, etc. |
| `arrow` | Стрела/болт | Archer (`SHOTLU` ammo) |
| `cannonball` | Пушечное ядро | Cannon, Tower, Frigate (single shot) |
| `cannister` | Картечь | Cannon close-range, multi-cannon |

Каждый юнит имеет `protection[kind]` отдельно по каждому типу — см. колонки `prot_*` в [04_units.md](04_units.md).

## Скорости юнитов

Базовые `gc_obj_speed_*` из `dmscript.global:603-620`. **Абстрактные единицы** (не tiles/sec). Реальная скорость в тайлах/сек зависит от animation `walkInterval`, `walkintervalfactor` и game speed. Для перевода нужен empirical test.

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

## Counter matrix (приближённый TTK)

Для каждой пары (атакующий класс, защищающийся класс) — **приближённое время убийства** (time-to-kill, TTK) в **игровых секундах** при 1v1, без учёта формаций, движения, промахов и shield-бонусов отрядов.

Расчёт: для атакующего берём **репрезентативного юнита класса** (медианный по damage); для защитника — медианный по HP. Применяется damage formula:

```
applied = max(1, weapon.dmg - target.shield - target.protection[weapon.kind])
DPS = applied / weapon.pause_sec
TTK = target.HP / DPS
```

⚠ Цифры ориентировочные. Реальный TTK будет выше из-за: дороги к цели, подготовки выстрела (`bartprepare`), формационных бонусов (squad shield, формация LINE/SQUARE/KARE), movement penalty к accuracy, fast-cavalry headshot bonus.

**Median представители классов** (использованы для расчёта):

| Класс | Atk-репрезентант | dmg | reload (s) | kind | Def-репрезентант | HP | shield |
|---|---|---:|---:|---|---|---:|---:|
| Peasant | `peatur` (Peasant) | 20 | 0.7 | sword | `peatur` (Peasant) | 50 | 0 |
| Pikemen 17c | `pikeman` (Pikeman, 17th century) | 8 | 0.7 | pike | `pikeman` (Pikeman, 17th century) | 90 | 0 |
| Pikemen 18c | `pikeman18` (Pikeman, 18th century) | 9 | 0.7 | pike | `pikeman18` (Pikeman, 18th century) | 85 | 0 |
| Light Infantry | `roundshier` (Roundshier) | 6 | 0.7 | sword | `roundshier` (Roundshier) | 100 | 0 |
| Musketeers 17c | `musketeerspa` (Musketeer, 17th century) | 9 | 2.81 | bullet | `jannisary` (Janissary) | 70 | 0 |
| Musketeers 18c | `musketeer18` (Musketeer, 18th century) | 10 | 0.7 | pike | `musketeer18pru` (Musketeer, 18th century) | 100 | 0 |
| Grenadiers | `grenadierdip` (Grenadier (mercenary)) | 18 | 0.7 | pike | `grenadierdip` (Grenadier (mercenary)) | 120 | 0 |
| Archers | `archerturdip` (Turkish archer (mercenary)) | 15 | 2.34 | arrow | `archerturdip` (Turkish archer (mercenary)) | 40 | 0 |
| Light Cavalry | `lightcavalrydip` (Light cavalry (mercenary)) | 15 | 5.62 | bullet | `lightcavalrydip` (Light cavalry (mercenary)) | 220 | 0 |
| Dragoons | `dragoon18dip` (Dragoon, 18th century (mercenary)) | 15 | 5.62 | bullet | `dragoon18dip` (Dragoon, 18th century (mercenary)) | 220 | 0 |
| Heavy Cavalry | `cossackdon` (Don Cossack) | 15 | 0.7 | pike | `reiter` (Reiter) | 300 | 0 |
| Cannons | `cannon` (Cannon) | 1800 | 10.94 | cannonball | `cannon` (Cannon) | 9000 | 75 |
| Mortars | `howitzer` (Howitzer) | 4000 | 18.75 | cannonball | `howitzer` (Howitzer) | 3000 | 75 |

### Counter matrix — TTK в игр-сек

Строки = **атакующий**. Колонки = **защищающийся**. Ячейка = TTK (game-sec). Зелёные/низкие = атакующий быстро убивает; красные/высокие = защитник долго стоит.

| Atk \ Def | Pea | Pik17 | Pik18 | LtInf | Mus17 | Mus18 | Gren | Arch | LtCav | Drag | HvCav | Cnn | Mor |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| **Pea** (Peasant) | 1.8 | 3.5 | 3.0 | 4.1 | 2.4 | 3.5 | 4.2 | 1.4 | 7.7 | 7.7 | 15 | _6300_ | _2100_ |
| **Pik17** (Pikemen 17c) | 4.4 | 13 | 7.4 | 14 | 6.1 | 8.8 | 10 | 3.5 | 19 | 19 | 35 | _6300_ | _2100_ |
| **Pik18** (Pikemen 18c) | 3.9 | 10 | 6.6 | 12 | 5.4 | 7.8 | 9.3 | 3.1 | 17 | 17 | 30 | _6300_ | _2100_ |
| **LtInf** (Light Infantry) | 5.8 | 16 | 9.9 | 23 | 8.2 | 12 | 14 | 4.7 | 26 | 26 | _210_ | _6300_ | _2100_ |
| **Mus17** (Musketeers 17c) | 16 | 51 | 27 | _140_ | 22 | 31 | 37 | 12 | 69 | 69 | _281_ | _25290_ | _8430_ |
| **Mus18** (Musketeers 18c) | 3.5 | 9.0 | 5.9 | 10 | 4.9 | 7.0 | 8.4 | 2.8 | 15 | 15 | 26 | _6300_ | _2100_ |
| **Gren** (Grenadiers) | 1.9 | 4.2 | 3.3 | 4.7 | 2.7 | 3.9 | 4.7 | 1.6 | 8.6 | 8.6 | 13 | _6300_ | _2100_ |
| **Arch** (Archers) | 7.8 | 23 | 13 | _234_ | 11 | 16 | 19 | 6.2 | 34 | 34 | _702_ | _21060_ | _7020_ |
| **LtCav** (Light Cavalry) | 19 | 46 | 32 | 70 | 26 | 37 | 45 | 15 | 82 | 82 | _187_ | _50580_ | _16860_ |
| **Drag** (Dragoons) | 19 | 46 | 32 | 70 | 26 | 37 | 45 | 15 | 82 | 82 | _187_ | _50580_ | _16860_ |
| **HvCav** (Heavy Cavalry) | 2.3 | 5.2 | 4.0 | 5.8 | 3.3 | 4.7 | 5.6 | 1.9 | 10 | 10 | 16 | _6300_ | _2100_ |
| **Cnn** (Cannons) | **0.3** | **0.6** | **0.5** | **0.6** | **0.4** | **0.6** | **0.7** | **0.2** | 1.3 | 1.3 | 1.9 | 57 | 19 |
| **Mor** (Mortars) | **0.2** | **0.4** | **0.4** | **0.5** | **0.3** | **0.5** | **0.6** | **0.2** | 1.0 | 1.0 | 1.4 | 43 | 14 |

**Чтение:** жирным — быстро убивает (TTK<1 sec), курсивом — почти не убивает (TTK>100 sec).

### Counter matrix с поправкой на промахи (для bullet/arrow)

Для bullet/arrow атакующих TTK выше из-за **dispersion**: на дистанции 15 t мушкетёр попадает только ~33% выстрелов (см. секцию Dispersion). Здесь TTK умножен на коэффициент промахов:

```
hit_chance(dist) = min(1.0, 1 / (2 × maxdisp))
                 = min(1.0, 1 / (2 × dist × disp × 0.0267))
real_TTK = ideal_TTK / hit_chance
```
Считаю на дистанции 12 t (типичная дистанция боя стрелков), с baseline dispersion=200 px/3.75 t. Для melee (cannon/mortar в melee?) дистанция 6 t как fallback. Ниже — relative TTK для стрелков (только rows: Mus17, Mus18, Arch, Drag, LtCav (если стрельба)):

| Atk \ Def | Pea | Pik17 | LtInf | Mus17 | Gren | Arch | LtCav | HvCav |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| **Mus17** (Musketeers 17c, hit≈41%) | 38 | _122_ | _338_ | 53 | _90_ | 30 | _165_ | _675_ |
| **Mus18** (Musketeers 18c, hit≈100%) | 3.5 | 9 | 10 | 4.9 | 8 | 2.8 | 15 | 26 |
| **Gren** (Grenadiers, hit≈100%) | 1.9 | 4.2 | 4.7 | 2.7 | 4.7 | 1.6 | 9 | 13 |
| **Arch** (Archers, hit≈41%) | 19 | 56 | _562_ | 26 | 45 | 15 | _82_ | _1687_ |
| **LtCav** (Light Cavalry, hit≈41%) | 45 | _110_ | _169_ | _63_ | _108_ | 36 | _198_ | _450_ |
| **Drag** (Dragoons, hit≈41%) | 45 | _110_ | _169_ | _63_ | _108_ | 36 | _198_ | _450_ |

**Что добавилось** относительно ideal TTK:
- Стрелки на дистанции 12 t **попадают ~50%** выстрелов → TTK ×2.
- Лучники с disp 175 px (немного лучше) — попадают чуть чаще.
- На большой дистанции (15-17 t у мушкета) — TTK еще +30-50%.
- В **hold-mode формации** damage +7 (с 6 до 13) → TTK падает в ~2 раза. С учётом промахов — формация компенсирует dispersion примерно как раз.
- **На холме** мушкетёры начинают стрелять на 2-4 t дальше → +1-2 выстрела до того, как враг подойдёт. Эффективный TTK снижается на ~10-30% за счёт лишних залпов.

**Примеры выводов** (на default protection данных):
- **Cannons / Mortars** против пехоты — TTK <1 (полный one-shot за выстрел).
- **Pikemen** против Heavy Cavalry — TTK высокий, потому что cavalry имеет prot_pike. Но в формации pikeman даёт сильно больше DPS.
- **Musketeers** против пехоты с prot_bullet=4-6 — TTK ~10-15 sec, реалистично.
- **Light Cavalry** vs **Cannons** — низкий TTK (cannon без брони, легко убивается).

## Upgrade × stat cross-reference

Какой апгрейд на что влияет. Сводка по `itype` (расшифровано в [05_upgrades.md](05_upgrades.md)). Цены даны для baseline нации (отличаются по нациям — см. [05_upgrades.md](05_upgrades.md)).

**Подсказки по нотации:** `aca.X` = academy.X, `bla.<unit>.1.X` = blacksmith damage X-th level for unit. `mil.X` = mill.X. Названия — из локали (en).

### Глобальные апгрейды (academy, mill)

| Apgrade | Effect | val | Cost (F/W/S/G/I/C) | Что улучшает |
|---|---|---:|---|---|
| `aca.1` (Academy) | **+food eff %** | 40 | F0/W200/S0/G325/I0/C0 | Cultivate new cultures of wheat (harvesting +40%) |
| `aca.2` (Academy) | **+food eff %** | 50 | F0/W2400/S0/G625/I0/C0 | Cultivate new cultures of rye (harvesting +50%) |
| `aca.3` (Academy) | **+food eff %** | 50 | F0/W3600/S0/G850/I0/C0 | Raise agriculturists' salary (harvesting +50%) |
| `aca.4` (Academy) | **+field HP %** | 200 | F0/W1000/S0/G475/I0/C0 | Carry out field melioration (field capacity +200%) |
| `aca.5` (Academy) | **+fish eff %** | 100 | F0/W12400/S0/G2520/I0/C0 | Design new tackle and fishing nets (boat efficiency +100%) |
| `aca.6` (Academy) | **enable unit** | 0 | F0/W12400/S0/G7040/I0/C0 | Develop new woodworking methods (frigate building) |
| `aca.7` (Academy) | **price %** | 0 | F0/W7300/S0/G1220/I0/C0 | Build new shipyards for fishing boats (fishing boat cost -85 |
| `aca.8` (Academy) | **+wood eff %** | 100 | F5500/W0/S0/G550/I0/C0 | Design new woodworking tools (woodcutting efficiency +100%) |
| `aca.9` (Academy) | **+shield** | 85 | F0/W9400/S7850/G1150/I0/C0 | Use new construction materials (durability of buildings +85) |
| `aca.10` (Academy) | **build time %** | -7500000 | F0/W0/S0/G6950/I0/C0 | Raise builders' salary (building construction time -75%) |
| `aca.11` (Academy) | **+shield** | 80 | F0/W0/S16200/G1500/I0/C0 | Research new fortification grades (durability of walls and t |
| `aca.12` (Academy) | **+damage %** | 10 | F0/W0/S0/G0/I5000/C0 | Improve firearms: rifled barrel (fire power +10%) |
| `aca.13` (Academy) | **+damage %** | 10 | F0/W0/S0/G4000/I0/C0 | Research granular gunpowder (fire power +10%) |
| `aca.14` (Academy) | **+damage %** | 15 | F0/W0/S0/G7000/I0/C0 | Research new sulphur purification methods (fire power +15%) |
| `aca.15` (Academy) | **+damage %** | 25 | F0/W0/S0/G0/I0/C11000 | Research new nitre purification methods (fire power +25%) |
| `aca.16` (Academy) | **range %** | 5 | F0/W0/S0/G2000/I12150/C0 | Research improved additions to gunpowder formula (artillery  |
| `aca.17` (Academy) | **range %** | 10 | F0/W0/S3000/G4550/I19200/C0 | Design new barrel types: unicorn, carronade (artillery range |
| `aca.18` (Academy) | **HP %** | 50 | F0/W0/S0/G500/I3830/C1500 | Design more durable gun carriage: Gribovalle system (artille |
| `aca.19` (Academy) | **enable unit** | 0 | F0/W0/S0/G1500/I0/C2500 | Design multi-barrelled cannon |
| `aca.20` (Academy) | **accuracy %** | -35 | F0/W3540/S0/G2000/I0/C7250 | Research new sighting devices for artillery (artillery accur |
| `aca.21` (Academy) | **healing** | 25 | F0/W350/S0/G100/I0/C250 | Finance artillery repair shops (repair all artillery) |
| `aca.22` (Academy) | **geology** | 0 | F0/W0/S0/G250/I0/C0 | Develop geology (previously hidden deposits appear on the ma |
| `aca.23` (Academy) | **+stone eff %** | 100 | F0/W0/S0/G1550/I3000/C0 | Develop mining (stone excavation efficiency +100%) |
| `aca.24` (Academy) | **+stone eff %** | 200 | F4200/W0/S0/G1550/I0/C12520 | Raise miners' salary (stone excavation efficiency +200%) |
| `aca.25` (Academy) | **balloon** | 0 | F0/W0/S0/G5750/I0/C0 | Design Montgolfier (reveals the whole map) |
| `aca.26` (Academy) | **healing** | 50 | F0/W0/S0/G200/I0/C200 | Develop medical science (heals all live units) |
| `aca.27` (Academy) | **accuracy %** | -35 | F0/W9540/S0/G12000/I0/C65200 | Develop mathematics (artillery accuracy +35%) |
| `aca.28` (Academy) | **speed %** | 40 | F0/W65400/S0/G24050/I0/C0 | Design new rigging types (ship speed +40%) |
| `aca.29` (Academy) | **enable unit** | 0 | F0/W32300/S0/G6800/I9000/C12800 | Design new rib system and new hulls (battleship construction |
| `aca.30` (Academy) | **build time %** | -5000000 | F0/W2300/S42700/G1150/I0/C0 | Train carpenters (shipbuilding speed x10) |
| `aca.31` (Academy) | **reload %** | -30 | F0/W0/S6000/G5500/I4200/C0 | Design wheellock (rate of fire +30%) |
| `aca.32` (Academy) | **price %** | 0 | F0/W0/S0/G6050/I0/C7750 | Design flintlock (musket cost -50%) |
| `aca.33` (Academy) | **reload %** | -30 | F0/W5000/S0/G5500/I0/C15200 | Design paper cartridge and iron ramrod (rate of fire +30%) |
| `aca.34` (Academy) | **+shield** | 2 | F0/W0/S0/G9750/I0/C0 | Research improved steel grades for cuirasses (armoured soldi |
| `aca.35` (Academy) | **+damage** | 5 | F0/W0/S0/G11500/I0/C0 | Design bayonet: barrel-inserted, bayonet with a tube (cold s |
| `aca.36` (Academy) | **+damage %** | 25 | F0/W0/S0/G19500/I0/C0 | Research new steel grades (18c musketeer/grenadier melee att |

**Apgrade-стек по эффектам** (cumulative):

- **+food extraction**: `mil.1` (+140%? note: mill upgrade values vary) + `aca.1` (+40%) + `aca.2` (+50%) + `aca.3` (+50%). Eff может выйти на 100+140+40+50+50 = **380%**.
- **+wood extraction**: `aca.8` (+100%). Удваивает wood/trip.
- **+stone extraction**: `aca.23` (+100%) + `aca.24` (+200%). До 100+100+200 = **400% eff**.
- **+fishing**: `aca.5` (+100%). Удваивает `fishingmax` лодки → 1000→2000.
- **+field HP** (`fieldlife`): `aca.4` (+200) + `bla.1` (+100). Меняет урон полю с 100/удар до 25/удар → +4× food per field.
- **+firearm damage %**: `aca.12` (+10) + `aca.13` (+10) + `aca.14` (+15) + `aca.15` (+25) = **+60% damage** для всех bullet/arrow юнитов.
- **+artillery range %**: `aca.16` (+5) + `aca.17` (+10) = **+15% range**.
- **+artillery accuracy %**: `aca.20` (-35%) + `aca.27` (-35%) = **-70% dispersion** (почти точные выстрелы).
- **+artillery durability %**: `aca.18` (+50%).
- **+firearm reload %**: `aca.31` (-30%) + `aca.33` (-30%) = **-60% reload time** (скорость стрельбы +250%). Применяется ко **ВСЕМ bullet-стрелкам** — мушкетёрам, стрельцам, янычарам, драгунам и пр. (через `garr_UnitsShooters` / `garr_UnitsBayonet`), не только артиллерии.
- **+building shield**: `aca.9` (+85, всех зданий) + `aca.11` (+80, walls/towers).
- **+building speed**: `aca.10` (-75% buildtime).
- **+ship speed**: `aca.28` (+40%).
- **One-time effects**: `aca.21` (heal artillery), `aca.22` (geology — reveal mines), `aca.25` (Montgolfier — reveal map), `aca.26` (heal all units), `aca.30` (×10 ship build speed), `aca.32` (-50% musket cost).
- **Enable units**: `aca.6` (frigate), `aca.19` (multicannon), `aca.29` (battleship).

### Per-unit апгрейды (blacksmith / barracks / stable)

Кузница (`bla`), бараки (`bar`/`ba2`), конюшня (`sta`) содержат **per-unit damage и protection** апгрейды (5 уровней + level 7 special). Формат sid: `<nat><place>.<unit>.<itype>.<level>` где itype=1 (damage) или 2 (protection).

Пример полного стека для **rusbar.pikemanrus** (Russian Spearman):
- 5 уровней damage (`.1.1` … `.1.5`): +1, +2, +2, +1, +2 = **+8 damage**
- 5 уровней protection (`.2.1` … `.2.5`): +1, +1, +2, +1, +1 = **+6 protection** (pike, sword, arrow)
- Level 7 unique (`.1.6` / `.2.6`): +2 damage / +2 protection (rus override)
- **Полный стек: +10 damage / +8 protection** на топовом prepared Russian pikeman.

Полный список — в [05_upgrades.md](05_upgrades.md) (~4500 строк, по местам).

## Стоимость одного выстрела

Многие огнестрельные юниты и башни/корабли тратят `iron`/`coal`/`gold` за каждый выстрел.

| sid | nation | weapon | dmg | reload (s) | shots/min | iron/выстрел | coal/выстрел | gold/выстрел |
|---|---|---|---:|---:|---:|---:|---:|---:|
| `archer` | alg | `OSTRELA` | 150 | 3.91 | 15.3 | — | — | — |
| `archerdip` | alg | `OSTRELA` | 150 | 3.91 | 15.3 | — | — | — |
| `archerdip` | aus | `OSTRELA` | 150 | 3.91 | 15.3 | — | — | — |
| `archerdip` | bav | `OSTRELA` | 150 | 3.91 | 15.3 | — | — | — |
| `archerdip` | den | `OSTRELA` | 150 | 3.91 | 15.3 | — | — | — |
| `archerdip` | eng | `OSTRELA` | 150 | 3.91 | 15.3 | — | — | — |
| `archerdip` | fra | `OSTRELA` | 150 | 3.91 | 15.3 | — | — | — |
| `archerdip` | hun | `OSTRELA` | 150 | 3.91 | 15.3 | — | — | — |
| `archerdip` | net | `OSTRELA` | 150 | 3.91 | 15.3 | — | — | — |
| `archerdip` | pie | `OSTRELA` | 150 | 3.91 | 15.3 | — | — | — |
| `archerdip` | pol | `OSTRELA` | 150 | 3.91 | 15.3 | — | — | — |
| `archerdip` | por | `OSTRELA` | 150 | 3.91 | 15.3 | — | — | — |
| `archerdip` | pru | `OSTRELA` | 150 | 3.91 | 15.3 | — | — | — |
| `archerdip` | rus | `OSTRELA` | 150 | 3.91 | 15.3 | — | — | — |
| `archerdip` | sax | `OSTRELA` | 150 | 3.91 | 15.3 | — | — | — |
| `archerdip` | sco | `OSTRELA` | 150 | 4.38 | 13.7 | — | — | — |
| `archerdip` | spa | `OSTRELA` | 150 | 3.91 | 15.3 | — | — | — |
| `archerdip` | swe | `OSTRELA` | 150 | 3.91 | 15.3 | — | — | — |
| `archerdip` | swi | `OSTRELA` | 150 | 3.91 | 15.3 | — | — | — |
| `archerdip` | tur | `OSTRELA` | 150 | 4.38 | 13.7 | — | — | — |
| `archerdip` | ukr | `OSTRELA` | 150 | 3.91 | 15.3 | — | — | — |
| `archerdip` | ven | `OSTRELA` | 150 | 3.91 | 15.3 | — | — | — |
| `archersco` | sco | `OSTRELA` | 150 | 4.38 | 13.7 | — | — | — |
| `archertur` | tur | `OSTRELA` | 150 | 4.38 | 13.7 | — | — | — |
| `archerturdip` | alg | `OSTRELA` | 150 | 3.91 | 15.3 | — | — | — |
| `archerturdip` | aus | `OSTRELA` | 150 | 3.91 | 15.3 | — | — | — |
| `archerturdip` | bav | `OSTRELA` | 150 | 3.91 | 15.3 | — | — | — |
| `archerturdip` | den | `OSTRELA` | 150 | 3.91 | 15.3 | — | — | — |
| `archerturdip` | eng | `OSTRELA` | 150 | 3.91 | 15.3 | — | — | — |
| `archerturdip` | fra | `OSTRELA` | 150 | 3.91 | 15.3 | — | — | — |
| `archerturdip` | hun | `OSTRELA` | 150 | 3.91 | 15.3 | — | — | — |
| `archerturdip` | net | `OSTRELA` | 150 | 3.91 | 15.3 | — | — | — |
| `archerturdip` | pie | `OSTRELA` | 150 | 3.91 | 15.3 | — | — | — |
| `archerturdip` | pol | `OSTRELA` | 150 | 3.91 | 15.3 | — | — | — |
| `archerturdip` | por | `OSTRELA` | 150 | 3.91 | 15.3 | — | — | — |
| `archerturdip` | pru | `OSTRELA` | 150 | 3.91 | 15.3 | — | — | — |
| `archerturdip` | rus | `OSTRELA` | 150 | 3.91 | 15.3 | — | — | — |
| `archerturdip` | sax | `OSTRELA` | 150 | 3.91 | 15.3 | — | — | — |
| `archerturdip` | sco | `OSTRELA` | 150 | 4.38 | 13.7 | — | — | — |
| `archerturdip` | spa | `OSTRELA` | 150 | 3.91 | 15.3 | — | — | — |
| `archerturdip` | swe | `OSTRELA` | 150 | 3.91 | 15.3 | — | — | — |
| `archerturdip` | swi | `OSTRELA` | 150 | 3.91 | 15.3 | — | — | — |
| `archerturdip` | tur | `OSTRELA` | 150 | 4.38 | 13.7 | — | — | — |
| `archerturdip` | ukr | `OSTRELA` | 150 | 3.91 | 15.3 | — | — | — |
| `archerturdip` | ven | `OSTRELA` | 150 | 3.91 | 15.3 | — | — | — |
| `battleship` | alg | `PPOINTTKOR` | 1800 | 2.34 | 25.6 | 25 | 35 | — |
| `battleship` | aus | `PPOINTTKOR` | 1800 | 2.34 | 25.6 | 25 | 35 | — |
| `battleship` | bav | `PPOINTTKOR` | 1800 | 2.34 | 25.6 | 25 | 35 | — |
| `battleship` | den | `PPOINTTKOR` | 1800 | 2.34 | 25.6 | 25 | 35 | — |
| `battleship` | eng | `PPOINTTKOR` | 1800 | 2.34 | 25.6 | 25 | 35 | — |
| `battleship` | fra | `PPOINTTKOR` | 1800 | 2.34 | 25.6 | 25 | 35 | — |
| `battleship` | hun | `PPOINTTKOR` | 1800 | 2.34 | 25.6 | 25 | 35 | — |
| `battleship` | net | `PPOINTTKOR` | 1800 | 2.34 | 25.6 | 25 | 35 | — |
| `battleship` | pie | `PPOINTTKOR` | 1800 | 2.34 | 25.6 | 25 | 35 | — |
| `battleship` | pol | `PPOINTTKOR` | 1800 | 2.34 | 25.6 | 25 | 35 | — |
| `battleship` | por | `PPOINTTKOR` | 1800 | 2.34 | 25.6 | 25 | 35 | — |
| `battleship` | pru | `PPOINTTKOR` | 1800 | 2.34 | 25.6 | 25 | 35 | — |
| `battleship` | rus | `PPOINTTKOR` | 1800 | 2.34 | 25.6 | 25 | 35 | — |
| `battleship` | sax | `PPOINTTKOR` | 1800 | 2.34 | 25.6 | 25 | 35 | — |
| `battleship` | sco | `PPOINTTKOR` | 1800 | 2.34 | 25.6 | 25 | 35 | — |
| `battleship` | spa | `PPOINTTKOR` | 1800 | 2.34 | 25.6 | 25 | 35 | — |
| `battleship` | swe | `PPOINTTKOR` | 1800 | 2.34 | 25.6 | 25 | 35 | — |
| `battleship` | swi | `PPOINTTKOR` | 1800 | 2.34 | 25.6 | 25 | 35 | — |
| `battleship` | tur | `PPOINTTKOR` | 1800 | 2.34 | 25.6 | 25 | 35 | — |
| `battleship` | ven | `PPOINTTKOR` | 1800 | 2.34 | 25.6 | 25 | 35 | — |
| `cannon` | alg | `PPOINTT` | 1800 | 10.94 | 5.5 | 20 | 40 | — |
| `cannon` | aus | `PPOINTT` | 1800 | 10.94 | 5.5 | 20 | 40 | — |
| `cannon` | bav | `PPOINTT` | 1800 | 10.94 | 5.5 | 20 | 40 | — |
| `cannon` | den | `PPOINTT` | 1800 | 10.94 | 5.5 | 20 | 40 | — |
| `cannon` | eng | `PPOINTT` | 1800 | 10.94 | 5.5 | 20 | 40 | — |
| `cannon` | fra | `PPOINTT` | 1800 | 10.94 | 5.5 | 20 | 40 | — |
| `cannon` | hun | `PPOINTT` | 1800 | 10.94 | 5.5 | 20 | 40 | — |
| `cannon` | net | `PPOINTT` | 1800 | 10.94 | 5.5 | 20 | 40 | — |
| `cannon` | pie | `PPOINTT` | 1800 | 10.94 | 5.5 | 20 | 40 | — |
| `cannon` | pol | `PPOINTT` | 1800 | 10.94 | 5.5 | 20 | 40 | — |
| `cannon` | por | `PPOINTT` | 1800 | 10.94 | 5.5 | 20 | 40 | — |
| `cannon` | pru | `PPOINTT` | 1800 | 10.94 | 5.5 | 20 | 40 | — |
| `cannon` | rus | `PPOINTT` | 1800 | 10.94 | 5.5 | 20 | 40 | — |
| `cannon` | sax | `PPOINTT` | 1800 | 10.94 | 5.5 | 20 | 40 | — |
| `cannon` | sco | `PPOINTT` | 1800 | 10.94 | 5.5 | 20 | 40 | — |
| `cannon` | spa | `PPOINTT` | 1800 | 10.94 | 5.5 | 20 | 40 | — |
| `cannon` | swe | `PPOINTT` | 1800 | 10.94 | 5.5 | 20 | 40 | — |
| `cannon` | swi | `PPOINTT` | 1800 | 10.94 | 5.5 | 20 | 40 | — |
| `cannon` | tur | `PPOINTT` | 1800 | 10.94 | 5.5 | 20 | 40 | — |
| `cannon` | ukr | `PPOINTT` | 1800 | 10.94 | 5.5 | 20 | 40 | — |
| `cannon` | ven | `PPOINTT` | 1800 | 10.94 | 5.5 | 20 | 40 | — |
| `chaika` | ukr | `PPOINTTKOR` | 1800 | 2.34 | 25.6 | 25 | 35 | — |
| `dragoon` | aus | `SHOTMUSKET` | 15 | 5.62 | 10.7 | 2 | 4 | — |
| `dragoon` | bav | `SHOTMUSKET` | 15 | 5.62 | 10.7 | 2 | 4 | — |
| `dragoon` | den | `SHOTMUSKET` | 15 | 5.62 | 10.7 | 2 | 4 | — |
| `dragoon` | eng | `SHOTMUSKET` | 15 | 5.62 | 10.7 | 2 | 4 | — |
| `dragoon` | fra | `SHOTMUSKET` | 15 | 5.62 | 10.7 | 2 | 4 | — |
| `dragoon` | hun | `SHOTMUSKET` | 15 | 5.62 | 10.7 | 2 | 4 | — |
| `dragoon` | net | `SHOTMUSKET` | 15 | 5.62 | 10.7 | 2 | 4 | — |
| `dragoon` | pie | `SHOTMUSKET` | 15 | 5.62 | 10.7 | 2 | 4 | — |
| `dragoon` | pol | `SHOTMUSKET` | 15 | 5.62 | 10.7 | 2 | 4 | — |
| `dragoon` | por | `SHOTMUSKET` | 15 | 5.62 | 10.7 | 2 | 4 | — |
| `dragoon` | pru | `SHOTMUSKET` | 15 | 5.62 | 10.7 | 2 | 4 | — |
| `dragoon` | sax | `SHOTMUSKET` | 15 | 5.62 | 10.7 | 2 | 4 | — |
| `dragoon` | spa | `SHOTMUSKET` | 15 | 5.62 | 10.7 | 2 | 4 | — |
| `dragoon` | swe | `SHOTMUSKET` | 15 | 5.62 | 10.7 | 2 | 4 | — |
| `dragoon` | swi | `SHOTMUSKET` | 15 | 5.62 | 10.7 | 2 | 4 | — |
| `dragoon` | ven | `SHOTMUSKET` | 15 | 5.62 | 10.7 | 2 | 4 | — |
| `dragoon18` | aus | `SHOTMUSKET` | 15 | 5.62 | 10.7 | 2 | 4 | — |
| `dragoon18` | bav | `SHOTMUSKET` | 15 | 5.62 | 10.7 | 2 | 4 | — |
| `dragoon18` | den | `SHOTMUSKET` | 15 | 5.62 | 10.7 | 2 | 4 | — |
| `dragoon18` | eng | `SHOTMUSKET` | 15 | 5.62 | 10.7 | 2 | 4 | — |
| `dragoon18` | pol | `SHOTMUSKET` | 15 | 5.62 | 10.7 | 2 | 4 | — |
| `dragoon18` | por | `SHOTMUSKET` | 15 | 5.62 | 10.7 | 2 | 4 | — |
| `dragoon18` | pru | `SHOTMUSKET` | 15 | 5.62 | 10.7 | 2 | 4 | — |
| `dragoon18` | rus | `SHOTMUSKET` | 15 | 5.62 | 10.7 | 2 | 4 | — |
| `dragoon18` | sax | `SHOTMUSKET` | 15 | 5.62 | 10.7 | 2 | 4 | — |
| `dragoon18` | spa | `SHOTMUSKET` | 15 | 5.62 | 10.7 | 2 | 4 | — |
| `dragoon18` | swe | `SHOTMUSKET` | 15 | 5.62 | 10.7 | 2 | 4 | — |
| `dragoon18` | swi | `SHOTMUSKET` | 15 | 5.62 | 10.7 | 2 | 4 | — |
| `dragoon18` | ven | `SHOTMUSKET` | 15 | 5.62 | 10.7 | 2 | 4 | — |
| `dragoon18dip` | alg | `SHOTMUSKET` | 15 | 5.62 | 10.7 | 2 | 4 | — |
| `dragoon18dip` | aus | `SHOTMUSKET` | 15 | 5.62 | 10.7 | 2 | 4 | — |
| `dragoon18dip` | bav | `SHOTMUSKET` | 15 | 5.62 | 10.7 | 2 | 4 | — |
| `dragoon18dip` | den | `SHOTMUSKET` | 15 | 5.62 | 10.7 | 2 | 4 | — |
| `dragoon18dip` | eng | `SHOTMUSKET` | 15 | 5.62 | 10.7 | 2 | 4 | — |
| `dragoon18dip` | fra | `SHOTMUSKET` | 15 | 5.62 | 10.7 | 2 | 4 | — |
| `dragoon18dip` | hun | `SHOTMUSKET` | 15 | 5.62 | 10.7 | 2 | 4 | — |
| `dragoon18dip` | net | `SHOTMUSKET` | 15 | 5.62 | 10.7 | 2 | 4 | — |
| `dragoon18dip` | pie | `SHOTMUSKET` | 15 | 5.62 | 10.7 | 2 | 4 | — |
| `dragoon18dip` | pol | `SHOTMUSKET` | 15 | 5.62 | 10.7 | 2 | 4 | — |
| `dragoon18dip` | por | `SHOTMUSKET` | 15 | 5.62 | 10.7 | 2 | 4 | — |
| `dragoon18dip` | pru | `SHOTMUSKET` | 15 | 5.62 | 10.7 | 2 | 4 | — |
| `dragoon18dip` | rus | `SHOTMUSKET` | 15 | 5.62 | 10.7 | 2 | 4 | — |
| `dragoon18dip` | sax | `SHOTMUSKET` | 15 | 5.62 | 10.7 | 2 | 4 | — |
| `dragoon18dip` | sco | `SHOTMUSKET` | 15 | 5.62 | 10.7 | 2 | 4 | — |
| `dragoon18dip` | spa | `SHOTMUSKET` | 15 | 5.62 | 10.7 | 2 | 4 | — |
| `dragoon18dip` | swe | `SHOTMUSKET` | 15 | 5.62 | 10.7 | 2 | 4 | — |
| `dragoon18dip` | swi | `SHOTMUSKET` | 15 | 5.62 | 10.7 | 2 | 4 | — |
| `dragoon18dip` | tur | `SHOTMUSKET` | 15 | 5.62 | 10.7 | 2 | 4 | — |
| `dragoon18dip` | ukr | `SHOTMUSKET` | 15 | 5.62 | 10.7 | 2 | 4 | — |
| `dragoon18dip` | ven | `SHOTMUSKET` | 15 | 5.62 | 10.7 | 2 | 4 | — |
| `dragoon18fra` | fra | `SHOTMUSKET` | 15 | 5.62 | 10.7 | 2 | 4 | — |
| `dragoon18net` | net | `SHOTMUSKET` | 15 | 5.62 | 10.7 | 2 | 4 | — |
| `dragoon18pie` | pie | `SHOTMUSKET` | 15 | 5.62 | 10.7 | 2 | 4 | — |
| `dragoonpol` | pol | `SHOTMUSKET` | 15 | 5.62 | 10.7 | 2 | 4 | — |
| `eurtow` | aus | `cannonball` | 1000 | 12.5 | 4.8 | 10 | 30 | — |
| `eurtow` | bav | `cannonball` | 1000 | 12.5 | 4.8 | 10 | 30 | — |
| `eurtow` | den | `cannonball` | 1000 | 12.5 | 4.8 | 10 | 30 | — |
| `eurtow` | eng | `cannonball` | 1000 | 12.5 | 4.8 | 10 | 30 | — |
| `eurtow` | fra | `cannonball` | 1000 | 12.5 | 4.8 | 10 | 30 | — |
| `eurtow` | hun | `cannonball` | 1000 | 12.5 | 4.8 | 10 | 30 | — |
| `eurtow` | net | `cannonball` | 1000 | 12.5 | 4.8 | 10 | 30 | — |
| `eurtow` | pie | `cannonball` | 1000 | 12.5 | 4.8 | 10 | 30 | — |
| `eurtow` | pol | `cannonball` | 1000 | 12.5 | 4.8 | 10 | 30 | — |
| `eurtow` | por | `cannonball` | 1000 | 12.5 | 4.8 | 10 | 30 | — |
| `eurtow` | pru | `cannonball` | 1000 | 12.5 | 4.8 | 10 | 30 | — |
| `eurtow` | sax | `cannonball` | 1000 | 12.5 | 4.8 | 10 | 30 | — |
| `eurtow` | sco | `cannonball` | 1000 | 12.5 | 4.8 | 10 | 30 | — |
| `eurtow` | spa | `cannonball` | 1000 | 12.5 | 4.8 | 10 | 30 | — |
| `eurtow` | swe | `cannonball` | 1000 | 12.5 | 4.8 | 10 | 30 | — |
| `eurtow` | swi | `cannonball` | 1000 | 12.5 | 4.8 | 10 | 30 | — |
| `eurtow` | ven | `cannonball` | 1000 | 12.5 | 4.8 | 10 | 30 | — |
| `framegun` | sco | `PPOINTTFRAME` | 500 | 2.81 | 21.4 | 30 | 40 | — |
| `frigate` | aus | `PPOINTTKOR` | 1800 | 2.34 | 25.6 | 25 | 35 | — |
| `frigate` | bav | `PPOINTTKOR` | 1800 | 2.34 | 25.6 | 25 | 35 | — |
| `frigate` | den | `PPOINTTKOR` | 1800 | 2.34 | 25.6 | 25 | 35 | — |
| `frigate` | eng | `PPOINTTKOR` | 1800 | 2.34 | 25.6 | 25 | 35 | — |
| `frigate` | fra | `PPOINTTKOR` | 1800 | 2.34 | 25.6 | 25 | 35 | — |
| `frigate` | hun | `PPOINTTKOR` | 1800 | 2.34 | 25.6 | 25 | 35 | — |
| `frigate` | net | `PPOINTTKOR` | 1800 | 2.34 | 25.6 | 25 | 35 | — |
| `frigate` | pie | `PPOINTTKOR` | 1800 | 2.34 | 25.6 | 25 | 35 | — |
| `frigate` | pol | `PPOINTTKOR` | 1800 | 2.34 | 25.6 | 25 | 35 | — |
| `frigate` | por | `PPOINTTKOR` | 1800 | 2.34 | 25.6 | 25 | 35 | — |
| `frigate` | pru | `PPOINTTKOR` | 1800 | 2.34 | 25.6 | 25 | 35 | — |
| `frigate` | rus | `PPOINTTKOR` | 1800 | 2.34 | 25.6 | 25 | 35 | — |
| `frigate` | sax | `PPOINTTKOR` | 1800 | 2.34 | 25.6 | 25 | 35 | — |
| `frigate` | sco | `PPOINTTKOR` | 1800 | 2.34 | 25.6 | 25 | 35 | — |
| `frigate` | spa | `PPOINTTKOR` | 1800 | 2.34 | 25.6 | 25 | 35 | — |
| `frigate` | swe | `PPOINTTKOR` | 1800 | 2.34 | 25.6 | 25 | 35 | — |
| `frigate` | swi | `PPOINTTKOR` | 1800 | 2.34 | 25.6 | 25 | 35 | — |
| `frigate` | ven | `PPOINTTKOR` | 1800 | 2.34 | 25.6 | 25 | 35 | — |
| `galley` | alg | `DIMMORT2KOR` | 1000 | 1.56 | 38.5 | 4 | 9 | — |
| `galley` | aus | `DIMMORT2KOR` | 1000 | 1.56 | 38.5 | 4 | 9 | — |
| `galley` | bav | `DIMMORT2KOR` | 1000 | 1.56 | 38.5 | 4 | 9 | — |
| `galley` | den | `DIMMORT2KOR` | 1000 | 1.56 | 38.5 | 4 | 9 | — |
| `galley` | eng | `DIMMORT2KOR` | 1000 | 1.56 | 38.5 | 4 | 9 | — |
| `galley` | fra | `DIMMORT2KOR` | 1000 | 1.56 | 38.5 | 4 | 9 | — |
| `galley` | hun | `DIMMORT2KOR` | 1000 | 1.56 | 38.5 | 4 | 9 | — |
| `galley` | net | `DIMMORT2KOR` | 1000 | 1.56 | 38.5 | 4 | 9 | — |
| `galley` | pie | `DIMMORT2KOR` | 1000 | 1.56 | 38.5 | 4 | 9 | — |
| `galley` | pol | `DIMMORT2KOR` | 1000 | 1.56 | 38.5 | 4 | 9 | — |
| `galley` | por | `DIMMORT2KOR` | 1000 | 1.56 | 38.5 | 4 | 9 | — |
| `galley` | pru | `DIMMORT2KOR` | 1000 | 1.56 | 38.5 | 4 | 9 | — |
| `galley` | rus | `DIMMORT2KOR` | 1000 | 1.56 | 38.5 | 4 | 9 | — |
| `galley` | sax | `DIMMORT2KOR` | 1000 | 1.56 | 38.5 | 4 | 9 | — |
| `galley` | spa | `DIMMORT2KOR` | 1000 | 1.56 | 38.5 | 4 | 9 | — |
| `galley` | swe | `DIMMORT2KOR` | 1000 | 1.56 | 38.5 | 4 | 9 | — |
| `galley` | swi | `DIMMORT2KOR` | 1000 | 1.56 | 38.5 | 4 | 9 | — |
| `galley` | tur | `DIMMORT2KOR` | 1000 | 1.56 | 38.5 | 4 | 9 | — |
| `galley` | ukr | `DIMMORT2KOR` | 1000 | 1.56 | 38.5 | 4 | 9 | — |
| `galley` | ven | `DIMMORT2KOR` | 1000 | 1.56 | 38.5 | 4 | 9 | — |
| `grenadier` | aus | `SHOTMUSKET` | 16 | 5.31 | 11.3 | 2 | 3 | — |
| `grenadier` | eng | `SHOTMUSKET` | 16 | 5.31 | 11.3 | 2 | 3 | — |
| `grenadier` | fra | `SHOTMUSKET` | 16 | 5.31 | 11.3 | 2 | 3 | — |
| `grenadier` | net | `SHOTMUSKET` | 16 | 5.31 | 11.3 | 2 | 3 | — |
| `grenadier` | pie | `SHOTMUSKET` | 16 | 5.31 | 11.3 | 2 | 3 | — |
| `grenadier` | pol | `SHOTMUSKET` | 16 | 5.31 | 11.3 | 2 | 3 | — |
| `grenadier` | por | `SHOTMUSKET` | 16 | 5.31 | 11.3 | 2 | 3 | — |
| `grenadier` | pru | `SHOTMUSKET` | 16 | 5.31 | 11.3 | 2 | 3 | — |
| `grenadier` | rus | `SHOTMUSKET` | 16 | 5.31 | 11.3 | 2 | 3 | — |
| `grenadier` | spa | `SHOTMUSKET` | 16 | 5.31 | 11.3 | 2 | 3 | — |
| `grenadier` | swe | `SHOTMUSKET` | 16 | 5.31 | 11.3 | 2 | 3 | — |
| `grenadier` | swi | `SHOTMUSKET` | 16 | 5.31 | 11.3 | 2 | 3 | — |
| `grenadier` | ven | `SHOTMUSKET` | 16 | 5.31 | 11.3 | 2 | 3 | — |
| `grenadierbav` | bav | `SHOTMUSKET` | 16 | 5.31 | 11.3 | 2 | 3 | — |
| `grenadierden` | den | `SHOTMUSKET` | 16 | 5.31 | 11.3 | 2 | 3 | — |
| `grenadierdip` | alg | `SHOTMUSKET` | 16 | 5.31 | 11.3 | 2 | 3 | — |
| `grenadierdip` | aus | `SHOTMUSKET` | 16 | 5.31 | 11.3 | 2 | 3 | — |
| `grenadierdip` | bav | `SHOTMUSKET` | 16 | 5.31 | 11.3 | 2 | 3 | — |
| `grenadierdip` | den | `SHOTMUSKET` | 16 | 5.31 | 11.3 | 2 | 3 | — |
| `grenadierdip` | eng | `SHOTMUSKET` | 16 | 5.31 | 11.3 | 2 | 3 | — |
| `grenadierdip` | fra | `SHOTMUSKET` | 16 | 5.31 | 11.3 | 2 | 3 | — |
| `grenadierdip` | hun | `SHOTMUSKET` | 16 | 5.31 | 11.3 | 2 | 3 | — |
| `grenadierdip` | net | `SHOTMUSKET` | 16 | 5.31 | 11.3 | 2 | 3 | — |
| `grenadierdip` | pie | `SHOTMUSKET` | 16 | 5.31 | 11.3 | 2 | 3 | — |
| `grenadierdip` | pol | `SHOTMUSKET` | 16 | 5.31 | 11.3 | 2 | 3 | — |
| `grenadierdip` | por | `SHOTMUSKET` | 16 | 5.31 | 11.3 | 2 | 3 | — |
| `grenadierdip` | pru | `SHOTMUSKET` | 16 | 5.31 | 11.3 | 2 | 3 | — |
| `grenadierdip` | rus | `SHOTMUSKET` | 16 | 5.31 | 11.3 | 2 | 3 | — |
| `grenadierdip` | sax | `SHOTMUSKET` | 16 | 5.31 | 11.3 | 2 | 3 | — |
| `grenadierdip` | sco | `SHOTMUSKET` | 16 | 5.31 | 11.3 | 2 | 3 | — |
| `grenadierdip` | spa | `SHOTMUSKET` | 16 | 5.31 | 11.3 | 2 | 3 | — |
| `grenadierdip` | swe | `SHOTMUSKET` | 16 | 5.31 | 11.3 | 2 | 3 | — |
| `grenadierdip` | swi | `SHOTMUSKET` | 16 | 5.31 | 11.3 | 2 | 3 | — |
| `grenadierdip` | tur | `SHOTMUSKET` | 16 | 5.31 | 11.3 | 2 | 3 | — |
| `grenadierdip` | ukr | `SHOTMUSKET` | 16 | 5.31 | 11.3 | 2 | 3 | — |
| `grenadierdip` | ven | `SHOTMUSKET` | 16 | 5.31 | 11.3 | 2 | 3 | — |
| `grenadierhun` | hun | `SHOTMUSKET` | 16 | 5.31 | 11.3 | 2 | 3 | — |
| `grenadierpru` | pru | `SHOTMUSKET` | 16 | 5.31 | 11.3 | 2 | 3 | — |
| `grenadiersax` | sax | `SHOTMUSKET` | 16 | 5.31 | 11.3 | 2 | 3 | — |
| `howitzer` | alg | `DIMMORT1` | 4000 | 18.75 | 3.2 | 20 | 100 | — |
| `howitzer` | aus | `DIMMORT1` | 4000 | 18.75 | 3.2 | 20 | 100 | — |
| `howitzer` | bav | `DIMMORT1` | 4000 | 18.75 | 3.2 | 20 | 100 | — |
| `howitzer` | den | `DIMMORT1` | 4000 | 18.75 | 3.2 | 20 | 100 | — |
| `howitzer` | eng | `DIMMORT1` | 4000 | 18.75 | 3.2 | 20 | 100 | — |
| `howitzer` | fra | `DIMMORT1` | 4000 | 18.75 | 3.2 | 20 | 100 | — |
| `howitzer` | hun | `DIMMORT1` | 4000 | 18.75 | 3.2 | 20 | 100 | — |
| `howitzer` | net | `DIMMORT1` | 4000 | 18.75 | 3.2 | 20 | 100 | — |
| `howitzer` | pie | `DIMMORT1` | 4000 | 18.75 | 3.2 | 20 | 100 | — |
| `howitzer` | pol | `DIMMORT1` | 4000 | 18.75 | 3.2 | 20 | 100 | — |
| `howitzer` | por | `DIMMORT1` | 4000 | 18.75 | 3.2 | 20 | 100 | — |
| `howitzer` | pru | `DIMMORT1` | 4000 | 18.75 | 3.2 | 20 | 100 | — |
| `howitzer` | rus | `DIMMORT1` | 4000 | 18.75 | 3.2 | 20 | 100 | — |
| `howitzer` | sax | `DIMMORT1` | 4000 | 18.75 | 3.2 | 20 | 100 | — |
| `howitzer` | sco | `DIMMORT1` | 4000 | 18.75 | 3.2 | 20 | 100 | — |
| `howitzer` | spa | `DIMMORT1` | 4000 | 18.75 | 3.2 | 20 | 100 | — |
| `howitzer` | swe | `DIMMORT1` | 4000 | 18.75 | 3.2 | 20 | 100 | — |
| `howitzer` | swi | `DIMMORT1` | 4000 | 18.75 | 3.2 | 20 | 100 | — |
| `howitzer` | tur | `DIMMORT1` | 4000 | 18.75 | 3.2 | 20 | 100 | — |
| `howitzer` | ukr | `DIMMORT1` | 4000 | 18.75 | 3.2 | 20 | 100 | — |
| `howitzer` | ven | `DIMMORT1` | 4000 | 18.75 | 3.2 | 20 | 100 | — |
| `kingmusketeer` | fra | `SHOTMUSKET` | 15 | 5.62 | 10.7 | 2 | 4 | — |
| `lightcavalry` | hun | `SHOTMUSKET` | 15 | 5.62 | 10.7 | 2 | 4 | — |
| `lightcavalrydip` | alg | `SHOTMUSKET` | 15 | 5.62 | 10.7 | 2 | 4 | — |
| `lightcavalrydip` | aus | `SHOTMUSKET` | 15 | 5.62 | 10.7 | 2 | 4 | — |
| `lightcavalrydip` | bav | `SHOTMUSKET` | 15 | 5.62 | 10.7 | 2 | 4 | — |
| `lightcavalrydip` | den | `SHOTMUSKET` | 15 | 5.62 | 10.7 | 2 | 4 | — |
| `lightcavalrydip` | eng | `SHOTMUSKET` | 15 | 5.62 | 10.7 | 2 | 4 | — |
| `lightcavalrydip` | fra | `SHOTMUSKET` | 15 | 5.62 | 10.7 | 2 | 4 | — |
| `lightcavalrydip` | hun | `SHOTMUSKET` | 15 | 5.62 | 10.7 | 2 | 4 | — |
| `lightcavalrydip` | net | `SHOTMUSKET` | 15 | 5.62 | 10.7 | 2 | 4 | — |
| `lightcavalrydip` | pie | `SHOTMUSKET` | 15 | 5.62 | 10.7 | 2 | 4 | — |
| `lightcavalrydip` | pol | `SHOTMUSKET` | 15 | 5.62 | 10.7 | 2 | 4 | — |
| `lightcavalrydip` | por | `SHOTMUSKET` | 15 | 5.62 | 10.7 | 2 | 4 | — |
| `lightcavalrydip` | pru | `SHOTMUSKET` | 15 | 5.62 | 10.7 | 2 | 4 | — |
| `lightcavalrydip` | rus | `SHOTMUSKET` | 15 | 5.62 | 10.7 | 2 | 4 | — |
| `lightcavalrydip` | sax | `SHOTMUSKET` | 15 | 5.62 | 10.7 | 2 | 4 | — |
| `lightcavalrydip` | sco | `SHOTMUSKET` | 15 | 5.62 | 10.7 | 2 | 4 | — |
| `lightcavalrydip` | spa | `SHOTMUSKET` | 15 | 5.62 | 10.7 | 2 | 4 | — |
| `lightcavalrydip` | swe | `SHOTMUSKET` | 15 | 5.62 | 10.7 | 2 | 4 | — |
| `lightcavalrydip` | swi | `SHOTMUSKET` | 15 | 5.62 | 10.7 | 2 | 4 | — |
| `lightcavalrydip` | tur | `SHOTMUSKET` | 15 | 5.62 | 10.7 | 2 | 4 | — |
| `lightcavalrydip` | ukr | `SHOTMUSKET` | 15 | 5.62 | 10.7 | 2 | 4 | — |
| `lightcavalrydip` | ven | `SHOTMUSKET` | 15 | 5.62 | 10.7 | 2 | 4 | — |
| `mortar` | alg | `DIMMORT2` | 200 | 7.81 | 7.7 | 20 | 30 | — |
| `mortar` | aus | `DIMMORT2` | 200 | 7.81 | 7.7 | 20 | 30 | — |
| `mortar` | bav | `DIMMORT2` | 200 | 7.81 | 7.7 | 20 | 30 | — |
| `mortar` | den | `DIMMORT2` | 200 | 7.81 | 7.7 | 20 | 30 | — |
| `mortar` | eng | `DIMMORT2` | 200 | 7.81 | 7.7 | 20 | 30 | — |
| `mortar` | fra | `DIMMORT2` | 200 | 7.81 | 7.7 | 20 | 30 | — |
| `mortar` | hun | `DIMMORT2` | 200 | 7.81 | 7.7 | 20 | 30 | — |
| `mortar` | net | `DIMMORT2` | 200 | 7.81 | 7.7 | 20 | 30 | — |
| `mortar` | pie | `DIMMORT2` | 200 | 7.81 | 7.7 | 20 | 30 | — |
| `mortar` | pol | `DIMMORT2` | 200 | 7.81 | 7.7 | 20 | 30 | — |
| `mortar` | por | `DIMMORT2` | 200 | 7.81 | 7.7 | 20 | 30 | — |
| `mortar` | pru | `DIMMORT2` | 200 | 7.81 | 7.7 | 20 | 30 | — |
| `mortar` | rus | `DIMMORT2` | 200 | 7.81 | 7.7 | 20 | 30 | — |
| `mortar` | sax | `DIMMORT2` | 200 | 7.81 | 7.7 | 20 | 30 | — |
| `mortar` | sco | `DIMMORT2` | 200 | 7.81 | 7.7 | 20 | 30 | — |
| `mortar` | spa | `DIMMORT2` | 200 | 7.81 | 7.7 | 20 | 30 | — |
| `mortar` | swe | `DIMMORT2` | 200 | 7.81 | 7.7 | 20 | 30 | — |
| `mortar` | swi | `DIMMORT2` | 200 | 7.81 | 7.7 | 20 | 30 | — |
| `mortar` | tur | `DIMMORT2` | 200 | 7.81 | 7.7 | 20 | 30 | — |
| `mortar` | ukr | `DIMMORT2` | 200 | 7.81 | 7.7 | 20 | 30 | — |
| `mortar` | ven | `DIMMORT2` | 200 | 7.81 | 7.7 | 20 | 30 | — |
| `multicannon` | aus | `PSMPOINTT` | 500 | 1.88 | 31.9 | 40 | 30 | — |
| `multicannon` | bav | `PSMPOINTT` | 500 | 1.88 | 31.9 | 40 | 30 | — |
| `multicannon` | den | `PSMPOINTT` | 500 | 1.88 | 31.9 | 40 | 30 | — |
| `multicannon` | eng | `PSMPOINTT` | 500 | 1.88 | 31.9 | 40 | 30 | — |
| `multicannon` | fra | `PSMPOINTT` | 500 | 1.88 | 31.9 | 40 | 30 | — |
| `multicannon` | hun | `PSMPOINTT` | 500 | 1.88 | 31.9 | 40 | 30 | — |
| `multicannon` | net | `PSMPOINTT` | 500 | 1.88 | 31.9 | 40 | 30 | — |
| `multicannon` | pie | `PSMPOINTT` | 500 | 1.88 | 31.9 | 40 | 30 | — |
| `multicannon` | pol | `PSMPOINTT` | 500 | 1.88 | 31.9 | 40 | 30 | — |
| `multicannon` | por | `PSMPOINTT` | 500 | 1.88 | 31.9 | 40 | 30 | — |
| `multicannon` | pru | `PSMPOINTT` | 500 | 1.88 | 31.9 | 40 | 30 | — |
| `multicannon` | rus | `PSMPOINTT` | 500 | 1.88 | 31.9 | 40 | 30 | — |
| `multicannon` | sax | `PSMPOINTT` | 500 | 1.88 | 31.9 | 40 | 30 | — |
| `multicannon` | spa | `PSMPOINTT` | 500 | 1.88 | 31.9 | 40 | 30 | — |
| `multicannon` | swe | `PSMPOINTT` | 500 | 1.88 | 31.9 | 40 | 30 | — |
| `multicannon` | swi | `PSMPOINTT` | 500 | 1.88 | 31.9 | 40 | 30 | — |
| `multicannon` | ven | `PSMPOINTT` | 500 | 1.88 | 31.9 | 40 | 30 | — |
| `musketeer18` | aus | `SHOTMUSKET` | 16 | 4.69 | 12.8 | 2 | 3 | — |
| `musketeer18` | eng | `SHOTMUSKET` | 16 | 4.69 | 12.8 | 2 | 3 | — |
| `musketeer18` | fra | `SHOTMUSKET` | 16 | 4.69 | 12.8 | 2 | 3 | — |
| `musketeer18` | hun | `SHOTMUSKET` | 16 | 4.69 | 12.8 | 2 | 3 | — |
| `musketeer18` | net | `SHOTMUSKET` | 16 | 4.69 | 12.8 | 2 | 3 | — |
| `musketeer18` | pie | `SHOTMUSKET` | 16 | 4.69 | 12.8 | 2 | 3 | — |
| `musketeer18` | pol | `SHOTMUSKET` | 16 | 4.69 | 12.8 | 2 | 3 | — |
| `musketeer18` | por | `SHOTMUSKET` | 16 | 4.69 | 12.8 | 2 | 3 | — |
| `musketeer18` | rus | `SHOTMUSKET` | 16 | 4.69 | 12.8 | 2 | 3 | — |
| `musketeer18` | spa | `SHOTMUSKET` | 16 | 4.69 | 12.8 | 2 | 3 | — |
| `musketeer18` | swe | `SHOTMUSKET` | 16 | 4.69 | 12.8 | 2 | 3 | — |
| `musketeer18` | swi | `SHOTMUSKET` | 16 | 4.69 | 12.8 | 2 | 3 | — |
| `musketeer18` | ven | `SHOTMUSKET` | 16 | 4.69 | 12.8 | 2 | 3 | — |
| `musketeer18bav` | bav | `SHOTMUSKET` | 22 | 5.94 | 10.1 | 3 | 4 | — |
| `musketeer18den` | den | `SHOTMUSKET` | 29 | 5.94 | 10.1 | 4 | 5 | — |
| `musketeer18pru` | pru | `SHOTMUSKET` | 22 | 4.69 | 12.8 | 3 | 4 | — |
| `musketeer18sax` | sax | `SHOTMUSKET` | 19 | 4.38 | 13.7 | 3 | 3 | — |
| `musketeeraus` | aus | `SHOTMUSKET` | 9 | 2.81 | 21.4 | 2 | 4 | — |
| `musketeerspa` | spa | `SHOTMUSKET` | 9 | 2.81 | 21.4 | 2 | 4 | — |
| `porpor` | por | `cannonball` | 1000 | 8.75 | 6.9 | 10 | 30 | — |
| `rustow` | rus | `cannonball` | 1000 | 9.38 | 6.4 | 10 | 30 | — |
| `strelet` | rus | `SHOTMUSKET` | 9 | 2.81 | 21.4 | 2 | 4 | — |
| `tatar` | tur | `STRELA` | 15 | 1.56 | 38.5 | — | — | — |
| `turtow` | alg | `cannonball` | 1200 | 15.62 | 3.8 | 15 | 40 | — |
| `turtow` | tur | `cannonball` | 1200 | 15.62 | 3.8 | 15 | 40 | — |
| `xebec` | alg | `PPOINTTKOR` | 1800 | 2.34 | 25.6 | 25 | 35 | — |
| `xebec` | tur | `PPOINTTKOR` | 1800 | 2.34 | 25.6 | 25 | 35 | — |
| `yacht` | aus | `PPOINTTKOR` | 1000 | 10.94 | 5.5 | 4 | 9 | — |
| `yacht` | bav | `PPOINTTKOR` | 1000 | 10.94 | 5.5 | 4 | 9 | — |
| `yacht` | den | `PPOINTTKOR` | 1000 | 10.94 | 5.5 | 4 | 9 | — |
| `yacht` | eng | `PPOINTTKOR` | 1000 | 10.94 | 5.5 | 4 | 9 | — |
| `yacht` | fra | `PPOINTTKOR` | 1000 | 10.94 | 5.5 | 4 | 9 | — |
| `yacht` | hun | `PPOINTTKOR` | 1000 | 10.94 | 5.5 | 4 | 9 | — |
| `yacht` | net | `PPOINTTKOR` | 1000 | 10.94 | 5.5 | 4 | 9 | — |
| `yacht` | pie | `PPOINTTKOR` | 1000 | 10.94 | 5.5 | 4 | 9 | — |
| `yacht` | pol | `PPOINTTKOR` | 1000 | 10.94 | 5.5 | 4 | 9 | — |
| `yacht` | por | `PPOINTTKOR` | 1000 | 10.94 | 5.5 | 4 | 9 | — |
| `yacht` | pru | `PPOINTTKOR` | 1000 | 10.94 | 5.5 | 4 | 9 | — |
| `yacht` | rus | `PPOINTTKOR` | 1000 | 10.94 | 5.5 | 4 | 9 | — |
| `yacht` | sax | `PPOINTTKOR` | 1000 | 10.94 | 5.5 | 4 | 9 | — |
| `yacht` | sco | `PPOINTTKOR` | 1000 | 10.94 | 5.5 | 4 | 9 | — |
| `yacht` | spa | `PPOINTTKOR` | 1000 | 10.94 | 5.5 | 4 | 9 | — |
| `yacht` | swe | `PPOINTTKOR` | 1000 | 10.94 | 5.5 | 4 | 9 | — |
| `yacht` | swi | `PPOINTTKOR` | 1000 | 10.94 | 5.5 | 4 | 9 | — |
| `yacht` | ven | `PPOINTTKOR` | 1000 | 10.94 | 5.5 | 4 | 9 | — |
| `yachttur` | tur | `PPOINTTKOR` | 1000 | 10.94 | 5.5 | 4 | 9 | — |