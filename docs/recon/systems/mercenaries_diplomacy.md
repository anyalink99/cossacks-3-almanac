# Наёмники и Дипломатический центр

[← Как устроена игра](../README.md)

Реверс-инжиниринг подсистемы найма наёмников через дипломатический центр
(`<nat>dip`): экономика, upkeep золотом, бунт `Rebellion`, лимит масштабирования
цены. Все ссылки на код и сами Pascal-блоки собраны в разделе
[Источники](#источники) в конце документа.

**Связанные документы:**

- [peasant_extraction.md](../world/economy/peasant_extraction.md) — семантика флага
  `bnohungry`; у наёмников он `True` — пищу они не едят.
- [building_mechanics.md](../world/economy/building_mechanics.md) — footprint и модель
  постройки дипломатического центра.
- [server_sync_architecture.md](../../../internals/engine/server_sync_architecture.md) —
  переназначение наёмников при бунте идёт через `_misc_ChangePlayer`,
  это server-authoritative событие.
- [determinism_audit.md](../../../internals/engine/determinism_audit.md) — переход при бунте
  использует `_misc_RandomInt` (seeded RNG).

## TL;DR

- **Дипломатический центр** (`<nat>dip`) — мид-гейм здание у каждой из
  21 наций. Цена ≈ 6.6k wood + stone, 4500 HP, пререквизиты — Академия
  и Городской центр.
- Производит **8 наёмников** (6 базовых + 2 из Early Bird-DLC). Каталог
  **одинаковый у всех наций** — статы юнитов не зависят от того, кто их
  нанимает; меняется только `sid`.
- Наёмник стоит **только золото** при найме, флаг `bnohungry = True`
  (пищу не ест), но **постоянно потребляет золото** в качестве upkeep
  (`consume.gold > 0`).
- Когда у игрока кончилось золото **и** `resconsume[gold] > resincome[gold]`,
  поднимается флаг `brebellion`. На каждом Nothing-тике каждый наёмник
  имеет шанс перейти к глобальному NPC-слоту «наёмник»
  (`gc_player_mercenaryind = MaxPlayerCount - 1`):
  - **easy:** 0.305% за тик
  - **normal:** 0.610% за тик
  - **hard и выше:** 18.31% за тик
- Этот NPC-слот всегда враждебен ко всем реальным игрокам.

---

## 1. Дипломатические здания (по нациям)

У всех 21 наций ровно один дипломатический центр, регистрируется единообразно
в `country.script` через `_country_AddMember` с категорией
`gc_country_editorplace_category_buildings` и AI-ролью
`gc_ai_unit_dipcenter` [^1].

Статы диспетчеризуются в `unit.script` по `csid+'dip'`: базовые значения для
17 «европейских» наций, и индивидуальные переопределения для `rus`, `ukr`,
`tur`, `alg` [^2].

Порядок аргументов `SetObjBuildingExtProperties`:
`maxhp, buildtime, costpercent, bcapture, score, usage, food, wood, stone, gold, iron, coal` [^3].

Обратите внимание: в индивидуальных ветках аргумент `gold` выставлен в `0`,
но рядом — комментарий `0{1000}`. Это маркер, что в Cossacks 1 цена была
1000 золота, а в Cossacks 3 её обнулили.

| Здание | нация(-и) | HP | buildtime (frames / wall-sec /32 / g-sec ×10/32) | wood | stone | gold | bcapture |
|---|---|---:|---:|---:|---:|---:|---|
| `<nat>dip` (default — 17 из 21) | aus, fra, eng, spa, pol, swe, pru, ven, net, den, por, pie, sax, bav, hun, swi, sco | 4500 | 1000 / 31.25s / 312.5g-s | 4900 | 1700 | 0 | False |
| `rusdip` | rus | 6500 | 1000 | 7900 | 3700 | 0 | False |
| `ukrdip` | ukr | 5000 | 1000 | 3900 | 2700 | 0 | False |
| `turdip` / `algdip` | tur, alg | 5500 | 1000 | 4600 | 2020 | 0 | False |

Предусловия (из поля `prereqs` в `data.json["buildings"]`, например
`ausdip → ['ausaca']`): дипцентр требует, чтобы Академия уже существовала.
Здание **не захватывается** (`bcapture=False`).

`costpercent=100`, поэтому каждый следующий дипцентр не дороже предыдущего —
но локализация однозначна: `data/locale/en/units.txt @%nat%dip.ext` гласит
**"You can only build one diplomatic center."** Механизм: вероятно,
ограничение реализовано через GUI / переключение `bproduceenabled`, а не
через costpercent. Открытый вопрос (см. §8).

`gc_obj_usage_dipcenter = 32` [^4] — используется map-настройкой `marketdip`
(см. §5).

---

## 2. Каталог наёмников

8 наёмников член-регистрируются в **каждой** нации единообразным набором
вызовов `_country_AddMember`: 6 базовых (`lightinfantrydip`, `roundshierdip`,
`grenadierdip`, `archerdip`, `cossacksichdip`, `dragoon18dip`) и 2 из
Early Bird-DLC (`archerturdip`, `lightcavalrydip`) [^5].

Все 21 нации также получают FixedProduce-проводку через
`_country_AddFixedProduceWithAccessControl` с тем же набором имён, со
стандартными prereqs `csid+'cen'` и `csid+'aca'` [^6]. Это означает: для
производства наёмника нужны Городской центр, Академия **и** дипцентр (последний —
само здание, в котором живёт `member`).

### 2.1 Детектирование `bmercenary`

Флаг `bmercenary := True` выставляется по списку имён, а не по полю
данных — диспетчер сравнивает `sid` с восьмью dip-суффиксами через
`StrExists(sid, 'dip')` и явное перечисление [^7].

Внутри `case` каждого юнита (например, `'archer','archerdip','archertur','archerturdip',...`)
блок `if (bmercenary) then begin ... end` переопределяет hp/оружие/цену/`consume`/`bnohungry`/`costpercent`.
Диспетчер использует тот же `case`, что и для обычного юнита, и затем сужает.

> С 2026-04-30 `docs/data.json` корректно учитывает `if (bmercenary)` —
> `parse_units.py` извлекает merc-блок и `_compute_effective_unit` применяет
> его для sid'ов из `BMERCENARY_SIDS` (8 dip-суффиксов). Все 168 строк
> (8 sid × 21 нация) теперь имеют merc-статы. Значения ниже считаны из
> `unit.script` и совпадают с тем, что в `data.json`.

### 2.2 Статы каждого наёмника

| sid | dispatch | HP | buildtime (frames) | gold (price) | consume.gold | costpercent | оружие (урон / дальность / тип) |
|---|---|---:|---:|---:|---:|---:|---|
| `lightinfantrydip` | `'lightinfantry','lightinfantrydip'` | 50 | 40 | 4 | 4 | 100 (default) | меч 16, дальность 50px |
| `roundshierdip` | `'roundshier','roundshierdip','swordsmansco'` | 75 | 48 | 12 | 20 | 100 (default) | меч 6, дальность 50px |
| `archerdip` | `'archer','archerdip','archertur','archerturdip','archersco','archerscodip'` | 20 | 40 | 15 | 16 | 100.5 | стрела 25 / огнестрел 100, дальность 700/750 |
| `archerturdip` | тот же case | 20 | 40 | 15 | 16 | 100.5 | то же |
| `grenadierdip` | `'grenadier','grenadierdip',…` | 30 | 48 | 25 | 60 | 100.5 | пика 30 / пуля 16 (дальность 800) / граната 200 (дальность 400) |
| `cossacksichdip` | `'croat','hussar',…,'cossacksich','cossacksichdip',…` | 150 | 80 | 60 | 150 | 100.5 | конная сабля 8, дальность 20px |
| `dragoon18dip` | `'dragoon',…,'dragoon18','dragoon18dip','lightcavalry','lightcavalrydip'` | 100 | 64 | 120 | 120 | 102 | конная пуля 18, дальность 800 |
| `lightcavalrydip` | тот же case | 100 | 64 | 120 | 120 | 102 | то же |

Точные строки в `unit.script` для каждого юнита и место выставления `bnohungry`
и обнуления food/wood/stone/iron/coal — см. [^8].

`bnohungry := True` ставится в каждом мерсенарском блоке — наёмники не платят
food upkeep (`reference_food_upkeep.md`).

Компоненты цены food/wood/stone/iron/coal у наёмников все равны 0 — вызовы
`SetObjBasePrice(objbase, 0, 0, 0, gold, 0, 0)` обнуляют всё, кроме золота.
То есть **наёмники стоят только золото** при найме.

### 2.3 Масштабирование цены и общий счётчик

`costpercent` у наёмников = 100, 100.5 или 102 — каждая следующая копия стоит
`floor(base × (costpercent/100)^N)` (см. `reference_costpercent_scaling.md`).
Для наёмников лимит **ниже, чем у обычных юнитов** [^9]:

- Парные `sid` делят счётчик: `archerdip ↔ archerturdip` и
  `dragoon18dip ↔ lightcavalrydip` через ветку `case sid of` суммируют
  `gPlayer[plInd].counter.all[cid][tmpid]`.
- Множитель `costmodifier = pow(costpercent/100, count)` срезается по
  условию `if bmercenary and (costmodifier > 2) then costmodifier := 2`,
  тогда как у обычных юнитов потолок — `20000`.

Два следствия:

1. **`archerdip` и `archerturdip` делят счётчик цены** (то же самое для
   `dragoon18dip ↔ lightcavalrydip`). Найм 100 `archerturdip` увеличивает
   цену `archerdip`.
2. Цена наёмника может вырасти максимум до **2×** от базы, а не до 20000×.
   То есть, в отличие от обычных юнитов, наёмники не становятся непомерно
   дорогими — при `costpercent=100.5` потолок 2× достигается примерно к
   `ln(2)/ln(1.005) ≈ 139` наёмникам (далее цена плоская).

---

## 3. Механика upkeep — потребление золота

Upkeep потребляется каждый кадр тем же общим циклом, что и пища
(`reference_food_upkeep.md`). Хендлер — `_player_ProcessResourceConsume`
в `player.script` [^10].

Псевдокод:

- Для каждого ресурса `i` берётся `resconsume = gPlayer[plInd].counter.resconsume[i]`.
- Раз в кадр в банк добавляется `resconsume × gc_time_to_frames × deltatime`,
  где `gc_time_to_frames = 32`.
- `value = floor(bank / 20000)` — целое число единиц ресурса к списанию.
- Если у игрока хватает запаса — списывается `value`, флаг бунта/голода
  снимается.
- Если не хватает — списывается всё, что есть, и поднимается соответствующий
  флаг (`bfamine` для пищи, `brebellion` для золота).

### Скорость утечки золота

Та же формула, что и для food upkeep — *единиц `consume.gold` за игровую
секунду на игрока*:

```
drain_per_g_sec = sum_over_units(consume.gold) × 32 / 20000
```

То есть один `dragoon18dip` с `consume.gold=120` выкачивает
`120 × 32 / 20000 = 0.192 gold/g-sec` ≈ **11.5 gold/g-min**. Армия мид-гейма
из 50 `dragoon18dip` уносит `50 × 0.192 = 9.6 gold/g-sec` ≈ 576 gold/g-min —
это поддерживается только связкой market+gold mine.

### `bfamine` vs `brebellion` — асимметрия

Оба флага сбрасываются в `False`, когда у игрока есть ресурсы для оплаты.
Оба ставятся в `True`, когда ресурсов нет. **Но для золота** есть
дополнительная защита: бунт срабатывает только если
`resconsume[gold] > resincome[gold]` [^11]. Это значит: если ваш доход с
золота покрывает утечку, то даже моментальный ноль на счету не вызовет
бунта. Только когда вы **структурно** в дефиците И буфер золота пуст —
флаг бунта защёлкивается.

Дополнительная страховка: `brebellion` сбрасывается, если `res[gold] >= 2`
или если `resconsume[gold] <= 0` (платить больше не за кого) [^12]. То есть
увольнение всех наёмников моментально прекращает бунт.

---

## 4. Триггер бунта

Логика дефекции живёт в per-unit Nothing-обработчике
`units/unit.inc/nothing.inc` (там же, где крутится цикл случайной смерти от
голода) [^13]. Условия запуска:

- `gPlayer[plInd].brebellion = True`,
- `objprop.bmercenary = True`,
- `plInd <> gc_player_mercenaryind` (не сам слот наёмника),
- юнит — `bplayable`.

Дальше — бросок RNG `_misc_RandomInt` (`floor(random × 32768)`,
`gc_c1rand_to_random = 32768`) [^14] с порогом, зависящим от сложности
игрока.

| difficulty | `_misc_RandomInt < threshold` | вероятность за один Nothing-тик |
|---|---|---:|
| 0 (easy) | 100 | 100/32768 ≈ **0.305%** |
| 1 (normal) | 200 | 200/32768 ≈ **0.610%** |
| >1 (hard / very hard / impossible) | 6000 | 6000/32768 ≈ **18.31%** |

Nothing-обработчик запускается на каждом progress-тике для idle/walking-юнитов,
поэтому на hard-уровнях **типичный наёмник дезертирует в течение 5-6 тиков
после `brebellion = True`** — фактически вся армия наёмников переходит к
врагу за несколько игровых секунд.

При срабатывании RNG юнит передаётся NPC-слоту через
`_misc_ChangePlayer(myHnd, plMercHnd, False, False, True)`. Слот наёмника —
`gc_player_mercenaryind = gc_MaxPlayerCount-1` [^15]. Этот игрок жёстко
прописан как враг для всех остальных слотов при инициализации карты:
маска `enemyplmask` каждого реального игрока включает бит NPC-слота [^16].

Поэтому дезертировавшие наёмники становятся враждебны **всем**, включая
бывшего хозяина. Их не уничтожают.

Слот игрока-наёмника стартует с фиксированным запасом ресурсов: 20k золота
и по 10k остальных [^17]. Это нужно, чтобы дезертировавшие наёмники могли
платить себе upkeep до того, как сами поднимут бунт, — но раз они уже в
слоте наёмника, это не имеет значения.

### Реакция AI

Состояние бунта также влияет на AI-скоринг защиты [^18]: для уже захваченных
юнитов `scoremodifier = 5`, для своих наёмников при `brebellion = True` —
`scoremodifier = 3`, для прочих своих — `scoremodifier = 2`. AI снижает
приоритет защиты собственных наёмников, когда те на грани дезертирства.

---

## 5. Map-настройка `marketdip`

`gMap.settings.additional.marketdip` контролирует доступность рынков и
дипцентров в партии. Все 5 значений с каноническими русскими названиями —
[`reports/map/lobby_settings.md`](../../reports/map/lobby_settings.md#marketdip--рынок-и-дипцентр);
поведение движка — [`game_settings.md`](../world/map/game_settings.md) §3.5.

Константы [^19]:

- `gc_mapsettings_marketdip_default = 0` — оба включены,
- `gc_mapsettings_marketdip_nodip = 1` — дипцентры отключены (`bproduceenabled := False`),
- `gc_mapsettings_marketdip_nomarket = 2` — рынки отключены,
- `gc_mapsettings_marketdip_noboth = 3` — оба отключены,
- `gc_mapsettings_marketdip_expensivemercs = 4` — цена каждого наёмника × 3.

Ветка `expensivemercs` живёт в `player.script` [^20]: если
`objprop.bmercenary = True`, то для каждого ресурса
`TObjBase(pobjbase).price[res]` умножается на `gc_gameplay_expensivemercskoef = 3` [^21].
В лобби с `expensivemercs` золотая цена наёмников утраивается
(4 → 12, 60 → 180, 120 → 360, 150 → 450, …). Множитель применяется ко
**всем** слотам цены, но поскольку у наёмников ненулевой только
`price[gold]`, утраивается только золотая стоимость.

---

## 6. Нейтральные дипцентры / точки найма

**Нет.** Поиск в `data/scripts` подстрок `peasantdip`, `townhalldip`,
`tradehouse`, `gc_player_neutralind`, `bneutral` — ни один из этих паттернов
не порождает нейтральные деревни или предразмещённые дип-здания на
стандартных skirmish-картах. Единственные «нейтральные» концепты:

- Поле `bneutral` у `gPlayer` [^22] — устанавливается/снимается только из
  скриптовых сценариев. На skirmish у всех реальных игроков `bneutral = False`.
- Слот владельца наёмников `gc_player_mercenaryind` существует с инициализации
  карты, но не имеет *никаких зданий* — он чисто получатель для
  дезертировавших юнитов.

Поэтому на стандартных рандомных картах **единственный способ нанимать
наёмников — построить свой `<nat>dip`** (цена + prereqs как в §1).

Кастомные сценарии могут предразмещать нейтральные дипцентры и использовать
`_misc_ChangePlayer` и т. п. (например, некоторые карты кампании), но это
специфика контента, а не движка.

---

## 7. Кросс-национальная доступность

Поскольку все 8 наёмников добавляются через `_country_AddMember` в **каждый**
национальный roster, и проводка FixedProduce находится в той же ветке
«для всех наций», **любая нация может нанимать любого наёмника**. 6 базовых
(`roundshierdip`, `lightinfantrydip`, `archerdip`, `grenadierdip`,
`cossacksichdip`, `dragoon18dip`) — безусловно. 2 EarlyBird-наёмника
(`lightcavalrydip`, `archerturdip`) требуют `bEarlyBird` (DLC куплен) [^5].

Ни у одного наёмника нет суффикса нации в `sid` (в отличие от `pikemanrus`,
`pikemansco` и т. п.), а инициализация юнита ставит `bmercenary` без
фильтрации по нации [^7].

«Национальный» инфикс в парных `sid` (`archerdip` vs `archerturdip`,
`dragoon18dip` vs `lightcavalrydip`) — это чисто **арт/модельный вариант**:
те же статы, тот же общий счётчик цены (§2.3), просто эстетическая
«западная»/«восточная» вариация одного и того же боевого функционала.

Правила офицерских формаций отличаются слегка [^23]: `roundshierdip` и
`grenadierdip` могут входить в стандартные пехотные формации вместе с
национальными пикинёрами/мушкетёрами. `archerdip`, `archerturdip`,
`lightinfantrydip` идут через отдельную регистрацию `…NoOfficersExtDip` —
формируют собственные строи без национального офицера.

---

## 8. Наёмник vs обычный юнит — сравнение

### Стоимость

Наёмники стоят **только золото + время постройки**; обычные юниты — food +
iron + coal (плюс пища на upkeep). Например, для тяжёлого конного стрелка:

| Юнит | food | iron | coal | gold | weapons.cost (за выстрел, iron+coal) | hp | buildtime |
|---|---:|---:|---:|---:|---|---:|---:|
| `dragoon18` (обычный, eu) | 70 | 7 | 0 | 60 | iron 4 + coal 5 | 225 | 720 frames |
| `dragoon18dip` (наёмник) | 0 | 0 | 0 | 120 | iron 5 + coal 8 | **100** | **64 frames** |

То есть наёмный Драгун стоит +60 золота и нулевые food/iron/coal при найме,
**строится в 11× быстрее**, но имеет 44% от обычного HP и сжигает чуть
больше iron+coal за выстрел. И постоянно теряет 120 золота.

Тот же паттерн для Лучника (`archer` btf 32 → `archerdip` btf 40 — формально
чуть медленнее, но наёмник этого тира стоит 0 пищи против 20 и имеет урон
25 против 15).

### Upkeep

- Обычные юниты: food upkeep `(consume.food + (bnohungry?0:30)) × 32/20000`
  за g-sec (`reference_food_upkeep.md`). Наёмники с `bnohungry` → нет утечки
  пищи.
- Наёмники: gold upkeep `consume.gold × 32/20000` за g-sec, зависит от
  `consume.gold` (4–150 на наёмника).
- Офицеры/королевские мушкетёры также имеют `consume.gold` (60–150), но они
  **не** `bmercenary`, поэтому не бунтуют.

### Когда брать наёмников (стратегический профиль)

Каталог наёмников — это, по сути, **армия быстрого развёртывания за золото**:

- **Ранняя игра.** Нации с избытком леса и слабым доступом к iron/coal
  могут моментально получить пехоту, обменяв wood и stone на золото
  через рынок и тут же наняв `roundshierdip` или `lightinfantrydip`.
- **Мид-гейм.** Золотой пик (союзная торговля, захваченные золотые
  шахты) хорошо конвертируется в быструю армию `dragoon18dip` — без
  ожидания угольных шахт.
- **Glass cannon.** HP примерно вдвое ниже, чем у обычных юнитов того
  же класса, — но преимущество в скорости найма на верхнем тире
  огромное: `dragoon18dip` тренируется 64 кадра против 720 у обычного
  `dragoon18` — **в 11.25 раза быстрее**.

**Главный риск — обрыв дохода с золота при бунте.** Стоит просесть
`income[gold]`, и вся армия наёмников дезертирует за секунды (на hard и
выше). Стандартный counter-play — расформировать наёмников **до** того,
как `gold` упадёт до нуля.

---

## 9. Открытые вопросы

| # | Вопрос | Где копать |
|---:|---|---|
| 1 | Ограничение «один дипцентр на игрока» — локализация утверждает «you can only build one diplomatic center», но в скриптах нет явной проверки вида `if count(dip) >= 1 then bproduceenabled := False`. У `<nat>dip` `costpercent = 100` тоже не блокирует. | `gui.script`, либо квота `_ai_TryUnit`. AI-логика проверяет `_ai_GetUnitCount(plind, cid, gc_ai_unit_dipcenter) > 0`, но это не enforcement для игрока-человека. |
| 2 | `bnoreputation` — не встречается ни в одном скрипте установки. Возможно, это поле относилось к Cossacks 1 / 2, либо имя у нас неправильное. | grep по всем .script + .global. |
| 3 | Частота тиков бунта в реальном времени — Nothing-handler срабатывает раз в один progress-tick. | Сверка с [`ticks_and_subticks.md`](../../../internals/engine/ticks_and_subticks.md) §3. Ориентир: при Nothing-tick ≈ 135 мс наёмники на hard переходят меньше чем за 1 секунду; при ≈ 100 мс — за ~0.5 секунды. |
| 4 | `bmercenary = True` у линейного корабля в `data.json` — 20 строк battleship помечены `bmercenary = True`, но в `case 'battleship'` внутри `unit.script` этот флаг явно не выставляется. | Возможно, это отдельная ветка (порты?) или артефакт парсера. 5 минут проверки. |

---

См. также **TL;DR** в начале файла — там собран короткий обзор тех же
фактов в виде маркированного списка.

---

## Источники

Все ссылки относительно `data/scripts/` в установке Cossacks 3.

[^1]: Регистрация дипцентра в национальном roster — `lib/country.script:2829`:

    ```pascal
    _country_AddMember(country, csid+'dip', ind, True,
                       gc_country_editorplace_category_buildings, 20,
                       gc_ai_unit_dipcenter);
    ```

[^2]: Диспетчеризация статов по `csid+'dip'` с national overrides —
    `lib/unit.script:2451-2459`:

    ```pascal
    csid+'dip' : begin
       SetObjBuildingExtProperties(objprop, objbase,
           4500, 1000, 100, False, 500,
           gc_obj_usage_dipcenter,
           0, 4900, 1700, 0{1000}, 0, 0);
       case i of
          rus : SetObjBuildingExtProperties(objprop, objbase,
                  6500, default, default, False, default, default,
                  0, 7900, 3700, 0{2500}, 0, 0);
          ukr : SetObjBuildingExtProperties(objprop, objbase,
                  5000, default, default, False, default, default,
                  0, 3900, 2700, 0{500}, 0, 0);
          tur : SetObjBuildingExtProperties(objprop, objbase,
                  5500, default, default, False, default, default,
                  0, 4600, 2020, 0{1300}, 0, 0);
          alg : SetObjBuildingExtProperties(objprop, objbase,
                  5500, default, default, False, default, default,
                  0, 4600, 2020, 0{1300}, 0, 0);
       end;
    end;
    ```

[^3]: Сигнатура `SetObjBuildingExtProperties` — `lib/unit.script:503`. Порядок
    аргументов: `maxhp, buildtime, costpercent, bcapture, score, usage, food, wood, stone, gold, iron, coal`.

[^4]: `gc_obj_usage_dipcenter = 32` — `dmscript.global:339`.

[^5]: Регистрация 8 наёмников через `_country_AddMember` —
    `lib/country.script:2786-2793, 2900-2901`:

    ```pascal
    _country_AddMember(country, 'lightinfantrydip', ind, True, ...gc_ai_unit_light_dip);
    _country_AddMember(country, 'roundshierdip',    ind, True, ...gc_ai_unit_round_dip);
    _country_AddMember(country, 'grenadierdip',     ind, True, ...gc_ai_unit_grendip);
    _country_AddMember(country, 'archerdip',        ind, True, ...airole);
    _country_AddMember(country, 'cossacksichdip',   ind, True, ...gc_ai_unit_cossackdip);
    _country_AddMember(country, 'dragoon18dip',     ind, True, ...gc_ai_unit_dragundip);
    // "early-bird" extension (DLC):
    _country_AddMember(country, 'archerturdip',     ind, True, ..., gc_ai_unit_none);
    _country_AddMember(country, 'lightcavalrydip',  ind, True, ..., gc_ai_unit_none);
    ```

[^6]: FixedProduce-проводка для 8 наёмников — `lib/country.script:3010-3022`:

    ```pascal
    member := csid+'dip';
    fixedproduceind := _country_GetFixedProduceIndexBySID(cid, member, bAddIfNotExist);
    _country_AddFixedProduceWithAccessControl(country, fixedproduceind, member,
       'roundshierdip',    0, 0, ind, csid+'cen', csid+'aca', '');
    _country_AddFixedProduceWithAccessControl(country, ..., 'lightinfantrydip', 1, 0, ind, csid+'cen', csid+'aca', '');
    _country_AddFixedProduceWithAccessControl(country, ..., 'archerdip',        2, 0, ind, csid+'cen', csid+'aca', '');
    _country_AddFixedProduceWithAccessControl(country, ..., 'grenadierdip',     3, 0, ind, csid+'cen', csid+'aca', '');
    _country_AddFixedProduceWithAccessControl(country, ..., 'cossacksichdip',   4, 0, ind, csid+'cen', csid+'aca', '');
    _country_AddFixedProduceWithAccessControl(country, ..., 'dragoon18dip',     5, 0, ind, csid+'cen', csid+'aca', '');
    if (bEarlyBird) then
    begin
       _country_AddFixedProduceWithAccessControl(country, ..., 'lightcavalrydip', 5, 1, ind, csid+'cen', csid+'aca', '');
       _country_AddFixedProduceWithAccessControl(country, ..., 'archerturdip',    2, 1, ind, csid+'cen', csid+'aca', '');
    end;
    ```

[^7]: Детектирование `bmercenary` по `sid` — `lib/unit.script:611-614`:

    ```pascal
    var bmercenary : Boolean;
    if StrExists(sid, 'dip') and ((sid='roundshierdip') or (sid='lightinfantrydip')
       or (sid='archerdip') or (sid='grenadierdip') or (sid='cossacksichdip')
       or (sid='dragoon18dip') or (sid='archerturdip') or (sid='lightcavalrydip')) then
    bmercenary := True;
    ```

[^8]: Блоки `if (bmercenary) then begin ... end` для каждого наёмника
    в `lib/unit.script`:

    - `lightinfantrydip` — строки 712-734.
    - `roundshierdip` — строки 735-770.
    - `archerdip` / `archerturdip` (тот же `case`) — строки 997-1061.
    - `grenadierdip` — строки 1226-1318.
    - `cossacksichdip` — строки 1320-1391.
    - `dragoon18dip` / `lightcavalrydip` (тот же `case`) — строки 1544-1662.

    Обнуление food/wood/stone/iron/coal — `SetObjBasePrice(objbase, 0, 0, 0, gold, 0, 0)`,
    например: строка 725 для `lightinfantry`, 1048 для `archer`, 1382 для
    `cossacksich`, 1651 для `dragoon18`.

[^9]: Лимит 2× для наёмников в `_unit_GetCostModifier` —
    `lib/unit.script:5660-5678`:

    ```pascal
    if (bmercenary) then
    begin
       var sid : String = gObjProp[cid][unitID].sid;
       var tmpsid : String;
       case sid of
          'archerdip'       : tmpsid := 'archerturdip';
          'archerturdip'    : tmpsid := 'archerdip';
          'dragoon18dip'    : tmpsid := 'lightcavalrydip';
          'lightcavalrydip' : tmpsid := 'dragoon18dip';
       end;
       var tmpid : Integer = _unit_ConvertObjSIDToID(cid, tmpsid);
       count := count+gPlayer[plInd].counter.all[cid][tmpid];
    end;
    costmodifier := pow(costpercent/100, count);
    if bmercenary and (costmodifier>2) then
    costmodifier := 2
    else
    if (costmodifier>20000) then
    costmodifier := 20000;
    ```

[^10]: `_player_ProcessResourceConsume` — `lib/player.script:268-322`:

    ```pascal
    procedure _player_ProcessResourceConsume(const plInd : Integer; const deltatime : Float);
    begin
       var i : Integer;
       for i:=0 to gc_ResCount-1 do
       begin
          var resconsume : Integer = gPlayer[plInd].counter.resconsume[i];
          if (resconsume>0) then
          begin
             const mult = 100;
             const speed = 20000;
             var resconsumerem : Float = gPlayer[plInd].counter.resconsumeremains[i]/mult;
             resconsume := resconsume*gc_time_to_frames;     // gc_time_to_frames = 32
             var bank : Float = resconsumerem+resconsume*deltatime;
             var realbank : Float = bank/speed;              // speed = 20000
             var value : Integer = floor(realbank);
             if (value<>0) then
             begin
                if (not gPlayer[plInd].res[i]>=value) then
                begin
                   _res_AddResToPlayerByIndex(plInd, i, -value);
                   case i of
                      gc_resource_type_food : gPlayer[plInd].bfamine := False;
                      gc_resource_type_gold : gPlayer[plInd].brebellion := False;
                   end;
                end
                else
                begin
                   _res_AddResToPlayerByIndex(plInd, i, -(not gPlayer[plInd].res[i]));
                   case i of
                      gc_resource_type_food : gPlayer[plInd].bfamine := True;
                      gc_resource_type_gold : begin
                         if (gPlayer[plInd].counter.resconsume[i]>gPlayer[plInd].counter.resincome[i]) then
                         gPlayer[plInd].brebellion := True
                         else
                         gPlayer[plInd].brebellion := False;
                      end;
                   end;
                end;
             end;
             bank := (realbank-value)*speed;
             gPlayer[plInd].counter.resconsumeremains[i] := floor(bank*mult);
          end;
       end;
       ...
    end;
    ```

[^11]: Условие на структурный дефицит — `lib/player.script:306`:

    ```pascal
    if (gPlayer[plInd].counter.resconsume[i]>gPlayer[plInd].counter.resincome[i]) then
       gPlayer[plInd].brebellion := True
    else
       gPlayer[plInd].brebellion := False;
    ```

[^12]: Финальный сброс `brebellion` — `lib/player.script:318-320`:

    ```pascal
    if (gPlayer[plInd].brebellion) and ((not gPlayer[plInd].res[gc_resource_type_gold]>=2)
       or (gPlayer[plInd].counter.resconsume[gc_resource_type_gold]<=0)) then
    gPlayer[plInd].brebellion := False;
    ```

[^13]: Триггер бунта в Nothing-обработчике — `units/unit.inc/nothing.inc:487-506`:

    ```pascal
    if (gPlayer[plInd].brebellion) and (TObjProp(pobjprop).bmercenary)
       and (plInd<>gc_player_mercenaryind) and (bplayable) then
    begin
       if (gInterface.gamemode=gc_gamemode_game) or (gInterface.gamemode=gc_gamemode_spectator) then
       begin
          if ((gPlayer[plInd].difficulty>1) and (_misc_RandomInt<6000))
             or ((gPlayer[plInd].difficulty=0) and (_misc_RandomInt<100))
             or ((gPlayer[plInd].difficulty=1) and (_misc_RandomInt<200)) then
          begin
             var plMercHnd : Integer = GetPlayerHandleByIndex(gc_player_mercenaryind);
             _misc_ChangePlayer(myHnd, plMercHnd, False, False, True);
          end;
       end
       else
       if (plHnd=GetPlayerHandleInterfaceIO) then
       begin
          var s1 : String = 'Rebel, but in editor mode your units wont die';
          ...
       end;
    end;
    ```

[^14]: `_misc_RandomInt` возвращает `floor(random × 32768)` —
    `lib/misc.script:494-498`. Константа `gc_c1rand_to_random = 32768`.

[^15]: `gc_player_mercenaryind = gc_MaxPlayerCount-1` — `dmscript.global:776`.

[^16]: Враждебность NPC-слота ко всем реальным игрокам — `common.inc/initmap.inc:48-49`:

    ```pascal
    if i<>gc_MaxPlayerCount-1 then
    gPlayer[i].enemyplmask:=1 shl (gc_MaxPlayerCount-1);
    ```

[^17]: Стартовые ресурсы NPC-слота наёмника — `lib/player.script:89-99`:

    ```pascal
    if (id=gc_player_mercenaryind) then
    begin
       case i of
          gc_resource_type_food : _res_SetResToPlayerByIndex(id, i, 10000);
          gc_resource_type_gold : _res_SetResToPlayerByIndex(id, i, 20000);
          gc_resource_type_iron : _res_SetResToPlayerByIndex(id, i, 10000);
          gc_resource_type_coal : _res_SetResToPlayerByIndex(id, i, 10000);
          else
          _res_SetResToPlayerByIndex(id, i, 10000);
       end;
    end
    ```

[^18]: AI-скоринг защиты юнитов — `lib/unit.script:3941-3946`:

    ```pascal
    if (bcaptured) then
       scoremodifier := 5
    else
    if (gPlayer[pl].brebellion) and (TObjProp(pobjprop).bmercenary) then
       scoremodifier := 3
    else
       scoremodifier := 2;
    ```

[^19]: Константы `gc_mapsettings_marketdip_*` — `dmscript.global:1077-1081`.

[^20]: Применение `expensivemercs` к ценам наёмников — `lib/player.script:2741-2774`:

    ```pascal
    gc_mapsettings_marketdip_expensivemercs : begin
       if (TObjProp(pobjprop).bmercenary) then
       begin
          var res : Integer;
          for res:=0 to gc_ResCount-1 do
          TObjBase(pobjbase).price[res] := TObjBase(pobjbase).price[res]*gc_gameplay_expensivemercskoef;
       end;
    end;
    ```

[^21]: `gc_gameplay_expensivemercskoef = 3` — `dmscript.global:214`.

[^22]: Поле `bneutral` у `gPlayer` — `lib/classes.script:3698`. Установка/снятие
    флага в скриптовых сценариях — `lib/scenario.script:2182-2238`.

[^23]: Регистрация формаций для наёмников — `lib/country.script:2515-2535`.
    `roundshierdip` и `grenadierdip` идут через стандартные пехотные
    формации; `archerdip`, `archerturdip`, `lightinfantrydip` —
    через `…NoOfficersExtDip`.
