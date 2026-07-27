# Наёмники и Дипломатический центр

[← Как устроена игра](../README.md)

Разбор найма через Дипломатический центр (`<nat>dip`): экономика,
содержание за золото, бунт (`Rebellion`) и предел роста цены. Все ссылки
на исходные тексты и выдержки на Pascal собраны в разделе
[Источники](#источники) в конце документа.

**Связанные документы:**

- [Добыча ресурсов крестьянами](../world/economy/peasant_extraction.md) — смысл флага
  `bnohungry`; у наёмников он `True` — пищу они не едят.
- [Строительство и свойства зданий](../world/economy/building_mechanics.md) — занимаемая площадь и модель
  постройки дипломатического центра.
- [Синхронизация сетевой игры](../../../internals/engine/server_sync_architecture.md) —
  переназначение наёмников при бунте идёт через `_misc_ChangePlayer`,
  это событие обрабатывает сервер.
- [Проверка детерминизма](../../../internals/engine/determinism_audit.md) — переход при бунте
  использует `_misc_RandomInt` (генератор псевдослучайных чисел с общим начальным значением).

## Кратко

- **Дипломатический центр** (`<nat>dip`) — здание середины партии у каждой
  из 21 нации. Обычная цена — 4900 дерева и 1700 камня, прочность —
  4500; для постройки нужны Академия и Городской центр.
- Производит **8 наёмников** (6 базовых + 2 из дополнения `Early Bird`).
  Набор **одинаков у всех наций** — характеристики юнитов не зависят
  от нанявшей их стороны; внутренний идентификатор (`sid`) тот же.
- Наёмник стоит **только золото** при найме, флаг `bnohungry = True`
  (пищу не ест), но **постоянно потребляет золото** на содержание
  (`consume.gold > 0`).
- Когда у игрока кончилось золото **и** `resconsume[gold] > resincome[gold]`,
  поднимается флаг `brebellion`. При каждой фоновой проверке бездействия
  каждый наёмник имеет шанс перейти к служебному игроку «наёмники»
  (`gc_player_mercenaryind = MaxPlayerCount - 1`):
  - **лёгкий уровень** (`easy`): 0,305 % за проверку;
  - **обычный уровень** (`normal`): 0,610 %;
  - **сложный и выше** (`hard` и выше): 18,31 %.
- Этот служебный игрок всегда враждебен всем участникам партии.

---

## 1. Дипломатические здания (по нациям)

У всех 21 наций ровно один дипломатический центр, регистрируется единообразно
в `country.script` через `_country_AddMember` с категорией
`gc_country_editorplace_category_buildings` и ролью для ИИ
`gc_ai_unit_dipcenter` [^1].

Характеристики выбираются в `unit.script` по `csid+'dip'`: базовые значения
для 17 «европейских» наций и отдельные значения для `rus`, `ukr`,
`tur`, `alg` [^2].

Порядок аргументов `SetObjBuildingExtProperties`:
`maxhp, buildtime, costpercent, bcapture, score, usage, food, wood, stone, gold, iron, coal` [^3].

Обратите внимание: в индивидуальных ветках аргумент `gold` выставлен в `0`,
но рядом — комментарий `0{1000}`. Это маркер, что в Cossacks 1 цена была
1000 золота, а в Cossacks 3 её обнулили.

| Здание | Нации | Прочность | Время постройки (`buildtime`) | Дерево | Камень | Золото | Можно захватить |
|---|---|---:|---:|---:|---:|---:|---|
| Дипломатический центр (`<nat>dip`, обычный вариант для 17 из 21 наций) | `aus`, `fra`, `eng`, `spa`, `pol`, `swe`, `pru`, `ven`, `net`, `den`, `por`, `pie`, `sax`, `bav`, `hun`, `swi`, `sco` | 4500 | 1000 кадров | 4900 | 1700 | 0 | Нет |
| Дипломатический центр России (`rusdip`) | `rus` | 6500 | 1000 кадров | 7900 | 3700 | 0 | Нет |
| Дипломатический центр Украины (`ukrdip`) | `ukr` | 5000 | 1000 кадров | 3900 | 2700 | 0 | Нет |
| Дипломатический центр Турции / Алжира (`turdip` / `algdip`) | `tur`, `alg` | 5500 | 1000 кадров | 4600 | 2020 | 0 | Нет |

Предусловия (из поля `prereqs` в `data.json["buildings"]`, например
`ausdip → ['ausaca']`): дипцентр требует, чтобы Академия уже существовала.
Здание **не захватывается** (`bcapture=False`).

`costpercent=100`, поэтому каждый следующий дипцентр не дороже предыдущего —
но локализация однозначна: `data/locale/en/units.txt @%nat%dip.ext` гласит
«Можно построить только один Дипломатический центр». Вероятно,
ограничение реализовано через интерфейс или переключение
`bproduceenabled`, а не через `costpercent`. Это ещё требует проверки
(см. §9).

`gc_obj_usage_dipcenter = 32` [^4] — используется настройкой карты `marketdip`
(см. §5).

---

## 2. Каталог наёмников

В **каждой** нации одинаково регистрируются 8 наёмников: Лёгкий пехотинец
(`lightinfantrydip`), Рундашир (`roundshierdip`), Гренадер
(`grenadierdip`), Лучник (`archerdip`), Сечевой казак
(`cossacksichdip`), Драгун 18 века (`dragoon18dip`), а также Турецкий
лучник (`archerturdip`) и Лёгкий кавалерист (`lightcavalrydip`) из
дополнения `Early Bird` [^5].

Для всех 21 наций доступ к производству задаётся через
`_country_AddFixedProduceWithAccessControl` с тем же набором имён, со
стандартными требованиями `csid+'cen'` и `csid+'aca'` [^6]. Это означает: для
производства наёмника нужны Городской центр, Академия **и** дипцентр (последний —
само здание, в котором живёт `member`).

### 2.1 Как игра распознаёт наёмника

Флаг `bmercenary := True` выставляется по списку внутренних имён, а не
по полю данных: игра сравнивает `sid` с восемью идентификаторами,
оканчивающимися на `dip`, через
`StrExists(sid, 'dip')` и явное перечисление [^7].

Внутри `case` каждого юнита (например, `'archer','archerdip','archertur','archerturdip',...`)
блок `if (bmercenary) then begin ... end` переопределяет прочность,
оружие, цену, `consume`, `bnohungry` и `costpercent`.
Диспетчер использует тот же `case`, что и для обычного юнита, и затем сужает.

> С 2026-04-30 `docs/data.json` корректно учитывает `if (bmercenary)` —
> `parse_units.py` извлекает ветку наёмников, а `_compute_effective_unit`
> применяет её к идентификаторам из `BMERCENARY_SIDS`. Все 168 сочетаний
> (8 наёмников × 21 нация) теперь имеют правильные характеристики.
> Значения ниже считаны из
> `unit.script` и совпадают с тем, что в `data.json`.

### 2.2 Характеристики наёмников

| Наёмник | Ветка в скрипте | Прочность | Время найма, кадров | Цена, золото | Содержание (`consume.gold`) | Рост цены (`costpercent`) | Оружие (урон / дальность / тип) |
|---|---|---:|---:|---:|---:|---:|---|
| **Лёгкий пехотинец** (`lightinfantrydip`) | `'lightinfantry','lightinfantrydip'` | 50 | 40 | 4 | 4 | 100 | меч 16, дальность 50 пикселей |
| **Рундашир** (`roundshierdip`) | `'roundshier','roundshierdip','swordsmansco'` | 75 | 48 | 12 | 20 | 100 | меч 6, дальность 50 пикселей |
| **Лучник** (`archerdip`) | `'archer','archerdip','archertur','archerturdip','archersco','archerscodip'` | 20 | 40 | 15 | 16 | 100,5 | стрела 25 / огнестрел 100, дальность 700/750 |
| **Турецкий лучник** (`archerturdip`) | та же ветка | 20 | 40 | 15 | 16 | 100,5 | то же |
| **Гренадер** (`grenadierdip`) | `'grenadier','grenadierdip',…` | 30 | 48 | 25 | 60 | 100,5 | пика 30 / пуля 16 (дальность 800) / граната 200 (дальность 400) |
| **Сечевой казак** (`cossacksichdip`) | `'croat','hussar',…,'cossacksich','cossacksichdip',…` | 150 | 80 | 60 | 150 | 100,5 | конная сабля 8, дальность 20 пикселей |
| **Драгун 18 века** (`dragoon18dip`) | `'dragoon',…,'dragoon18','dragoon18dip','lightcavalry','lightcavalrydip'` | 100 | 64 | 120 | 120 | 102 | конная пуля 18, дальность 800 |
| **Лёгкий кавалерист** (`lightcavalrydip`) | та же ветка | 100 | 64 | 120 | 120 | 102 | то же |

Точные строки в `unit.script` для каждого юнита и место выставления
`bnohungry` и обнуления пищи, дерева, камня, железа и угля — см. [^8].

`bnohungry := True` ставится в каждой ветке наёмников — они не расходуют
пищу на содержание (см. `reference_food_upkeep.md`).

Компоненты цены пищи, дерева, камня, железа и угля у наёмников равны нулю:
`SetObjBasePrice(objbase, 0, 0, 0, gold, 0, 0)` обнуляют всё, кроме золота.
То есть **наёмники стоят только золото** при найме.

### 2.3 Масштабирование цены и общий счётчик

`costpercent` у наёмников = 100, 100.5 или 102 — каждая следующая копия стоит
`floor(base × (costpercent/100)^N)` (см. `reference_costpercent_scaling.md`).
Для наёмников лимит **ниже, чем у обычных юнитов** [^9]:

- Парные виды делят счётчик: Лучник (`archerdip`) ↔ Турецкий лучник
  (`archerturdip`) и
  `dragoon18dip ↔ lightcavalrydip` через ветку `case sid of` суммируют
  `gPlayer[plInd].counter.all[cid][tmpid]`.
- Множитель `costmodifier = pow(costpercent/100, count)` срезается по
  условию `if bmercenary and (costmodifier > 2) then costmodifier := 2`,
  тогда как у обычных юнитов потолок — `20000`.

Два следствия:

1. **Лучник (`archerdip`) и Турецкий лучник (`archerturdip`) делят
   счётчик цены**; то же верно для Драгуна 18 века (`dragoon18dip`) и
   Лёгкого кавалериста (`lightcavalrydip`). Найм 100 Турецких лучников
   увеличивает цену Лучника.
2. Цена наёмника может вырасти максимум до **2×** от базы, а не до 20000×.
   То есть, в отличие от обычных юнитов, наёмники не становятся непомерно
   дорогими — при `costpercent=100.5` потолок 2× достигается примерно к
   `ln(2)/ln(1.005) ≈ 139` наёмникам (далее цена плоская).

---

## 3. Содержание за золото

Золото на содержание списывается каждый кадр тем же общим циклом, что и пища
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

Та же формула, что и для содержания пищей: *единиц `consume.gold` за игровую
секунду на игрока*:

```
drain_per_g_sec = sum_over_units(consume.gold) × 32 / 20000
```

То есть один `dragoon18dip` с `consume.gold=120` выкачивает
`120 × 32 / 20000 = 0,192` золота в игровую секунду, или примерно
**11,5 золота в игровую минуту**. Армия из 50 Драгунов 18 века
(`dragoon18dip`) расходует `50 × 0.192 = 9.6` золота в игровую секунду,
или около 576 золота в игровую минуту. Такой расход требует рынка и
золотых шахт.

### Различие голода (`bfamine`) и бунта (`brebellion`)

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

## 4. Как начинается бунт

Логика дезертирства живёт в обработчике состояния бездействия каждого юнита
`units/unit.inc/nothing.inc` (там же, где крутится цикл случайной смерти от
голода) [^13]. Условия запуска:

- `gPlayer[plInd].brebellion = True`,
- `objprop.bmercenary = True`,
- `plInd <> gc_player_mercenaryind` (не сам слот наёмника),
- юнит — `bplayable`.

Дальше игра получает псевдослучайное число функцией `_misc_RandomInt`
(`floor(random × 32768)`,
`gc_c1rand_to_random = 32768`) [^14] с порогом, зависящим от сложности
игрока.

| Сложность | Условие | Вероятность за одну фоновую проверку |
|---|---|---:|
| 0, лёгкая (`easy`) | `_misc_RandomInt < 100` | 100/32768 ≈ **0,305 %** |
| 1, обычная (`normal`) | `_misc_RandomInt < 200` | 200/32768 ≈ **0,610 %** |
| выше 1, сложная и выше | `_misc_RandomInt < 6000` | 6000/32768 ≈ **18,31 %** |

Фоновая проверка запускается на каждом такте обработки для бездействующих
или идущих юнитов, поэтому на сложном уровне и выше **типичный наёмник
дезертирует в течение 5–6 проверок
после `brebellion = True`** — фактически вся армия наёмников переходит к
врагу за несколько игровых секунд.

При успешной случайной проверке юнит передаётся служебному игроку через
`_misc_ChangePlayer(myHnd, plMercHnd, False, False, True)`. Слот наёмника —
`gc_player_mercenaryind = gc_MaxPlayerCount-1` [^15]. Этот игрок жёстко
прописан как враг для всех остальных слотов при инициализации карты:
маска `enemyplmask` каждого реального игрока включает бит служебного
игрока [^16].

Поэтому дезертировавшие наёмники становятся враждебны **всем**, включая
бывшего хозяина. Их не уничтожают.

Служебный игрок-наёмник начинает с фиксированным запасом: 20 000 золота
и по 10 000 остальных ресурсов [^17]. Это позволяет дезертировавшим
наёмникам оплачивать содержание до собственного бунта, но раз они уже в
слоте наёмника, это не имеет значения.

### Реакция ИИ

Состояние бунта также влияет на оценку важности защиты [^18]: для уже
захваченных юнитов `scoremodifier = 5`, для своих наёмников при
`brebellion = True` — `scoremodifier = 3`, для прочих своих —
`scoremodifier = 2`. ИИ снижает
приоритет защиты собственных наёмников, когда те на грани дезертирства.

---

## 5. Настройка лобби «Рынок и Дипломатический центр» (`marketdip`)

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

## 6. Есть ли нейтральные точки найма

**Нет.** Поиск в `data/scripts` подстрок `peasantdip`, `townhalldip`,
`tradehouse`, `gc_player_neutralind`, `bneutral` — ни один из этих паттернов
не порождает нейтральные деревни или предразмещённые дип-здания на
стандартных случайных картах. Единственные связанные служебные механизмы:

- Поле `bneutral` у `gPlayer` [^22] — устанавливается/снимается только из
  сценариев. На обычной случайной карте у всех реальных игроков
  `bneutral = False`.
- Слот владельца наёмников `gc_player_mercenaryind` существует с инициализации
  карты, но не имеет *никаких зданий* — он чисто получатель для
  дезертировавших юнитов.

Поэтому на стандартных рандомных картах **единственный способ нанимать
наёмников — построить свой Дипломатический центр (`<nat>dip`)** с
требованиями из §1.

Кастомные сценарии могут предразмещать нейтральные дипцентры и использовать
`_misc_ChangePlayer` и т. п. (например, некоторые карты кампании), но это
специфика контента, а не движка.

---

## 7. Доступность для разных наций

Поскольку все 8 наёмников добавляются через `_country_AddMember` в набор
юнитов **каждой** нации, а правила производства находятся в общей ветке,
**любая нация может нанимать любого наёмника**. Шесть базовых доступны
всегда: Рундашир (`roundshierdip`), Лёгкий пехотинец
(`lightinfantrydip`), Лучник (`archerdip`), Гренадер
(`grenadierdip`), Сечевой казак (`cossacksichdip`) и Драгун 18 века
(`dragoon18dip`). Лёгкий кавалерист (`lightcavalrydip`) и Турецкий лучник
(`archerturdip`) требуют купленного дополнения `Early Bird` [^5].

Ни у одного наёмника нет суффикса нации в `sid` (в отличие от `pikemanrus`,
`pikemansco` и т. п.), а инициализация юнита ставит `bmercenary` без
фильтрации по нации [^7].

«Национальная» часть парных идентификаторов — это только **вариант
оформления и модели**: у Лучника (`archerdip`) и Турецкого лучника
(`archerturdip`), как и у Драгуна 18 века (`dragoon18dip`) и Лёгкого
кавалериста (`lightcavalrydip`), одинаковые характеристики и общий счётчик
цены (§2.3). Отличается только эстетическая
«западная»/«восточная» вариация одного и того же боевого функционала.

Правила офицерских формаций отличаются слегка [^23]: `roundshierdip` и
`grenadierdip` могут входить в стандартные пехотные формации вместе с
национальными пикинёрами/мушкетёрами. `archerdip`, `archerturdip`,
`lightinfantrydip` идут через отдельную регистрацию `…NoOfficersExtDip` —
формируют собственные строи без национального офицера.

---

## 8. Сравнение с обычными юнитами

### Стоимость

Наёмники требуют **только золото и время найма**; обычным юнитам нужны
пища, железо и уголь, а затем пища на содержание. Например, для тяжёлого
конного стрелка:

| Юнит | Пища | Железо | Уголь | Золото | Цена выстрела | Прочность | Время найма |
|---|---:|---:|---:|---:|---|---:|---:|
| **Драгун 18 века** (`dragoon18`, обычный европейский) | 70 | 7 | 0 | 60 | 4 железа + 5 угля | 225 | 720 кадров |
| **Драгун 18 века (наёмник)** (`dragoon18dip`) | 0 | 0 | 0 | 120 | 5 железа + 8 угля | **100** | **64 кадра** |

То есть наёмный Драгун стоит на 60 золота дороже и не требует пищи,
железа или угля при найме. Он **нанимается в 11 раз быстрее**, но имеет
44 % прочности обычного Драгуна, расходует немного больше железа и угля
за выстрел и постоянно требует золото на содержание.

Сходное соотношение у Лучника (`archer`: `btf = 32`; наёмный
`archerdip`: `btf = 40`) — формально
чуть медленнее, но наёмник этого тира стоит 0 пищи против 20 и имеет урон
25 против 15).

### Содержание

- Обычные юниты расходуют пищу по формуле
  `(consume.food + (bnohungry?0:30)) × 32/20000` за игровую секунду
  (см. `reference_food_upkeep.md`). Наёмники с `bnohungry` пищу не расходуют.
- Наёмники расходуют золото по формуле `consume.gold × 32/20000` за
  игровую секунду; величина зависит от
  `consume.gold` (4–150 на наёмника).
- Офицеры/королевские мушкетёры также имеют `consume.gold` (60–150), но они
  **не** `bmercenary`, поэтому не бунтуют.

### Когда брать наёмников (стратегический профиль)

Каталог наёмников — это, по сути, **армия быстрого развёртывания за золото**:

- **Ранняя игра.** Нации с избытком дерева и слабым доступом к железу
  и углю могут быстро получить пехоту: обменять дерево и камень на
  золото и нанять Рундаширов (`roundshierdip`) или Лёгких пехотинцев
  (`lightinfantrydip`).
- **Середина партии.** Избыток золота от союзной торговли или захваченных
  шахт можно быстро превратить в армию Драгунов 18 века (`dragoon18dip`) без
  ожидания угольных шахт.
- **Высокий урон ценой живучести.** Прочность примерно вдвое ниже, чем у обычных юнитов того
  же класса, — но преимущество в скорости найма на верхнем тире
  огромное: `dragoon18dip` тренируется 64 кадра против 720 у обычного
  `dragoon18` — **в 11.25 раза быстрее**.

**Главный риск — обрыв дохода с золота при бунте.** Стоит просесть
доходу золота (`income[gold]`), и вся армия наёмников дезертирует за
секунды на сложном уровне и выше. Безопасный ответ — расформировать
наёмников **до** того,
как `gold` упадёт до нуля.

---

## 9. Открытые вопросы

| № | Вопрос | Как проверить |
|---:|---|---|
| 1 | Ограничение «один Дипломатический центр на игрока» заявлено в локализации, но в скриптах не найдено явной проверки `if count(dip) >= 1 then bproduceenabled := False`. У `<nat>dip` значение `costpercent = 100` тоже не блокирует повторную постройку. | Проверить `gui.script` и квоту `_ai_TryUnit`. ИИ проверяет `_ai_GetUnitCount(plind, cid, gc_ai_unit_dipcenter) > 0`, но это не ограничивает игрока-человека. |
| 2 | `bnoreputation` не задаётся ни в одном изученном скрипте. Возможно, поле относилось к первым или вторым «Казакам» либо его имя определено неверно. | Выполнить поиск по всем `.script` и `.global`. |
| 3 | Частота проверок бунта в реальном времени: обработчик состояния бездействия срабатывает раз за один такт обработки. | Сверить с [`ticks_and_subticks.md`](../../../internals/engine/ticks_and_subticks.md) §3. При интервале около 135 мс наёмники на сложном уровне переходят меньше чем за секунду; при 100 мс — примерно за полсекунды. |
| 4 | В `data.json` 20 вариантов Линейного корабля (`battleship`) помечены `bmercenary = True`, но в ветке `case 'battleship'` внутри `unit.script` этот флаг явно не выставляется. | Проверить отдельную портовую ветку и исключить артефакт парсера. |

---

См. также раздел **Кратко** в начале файла — там собран короткий обзор тех же
фактов в виде маркированного списка.

---

## Источники

Все ссылки относительно `data/scripts/` в установке Cossacks 3.

[^1]: Регистрация Дипломатического центра в наборе нации —
      `lib/country.script:2829`:

    ```pascal
    _country_AddMember(country, csid+'dip', ind, True,
                       gc_country_editorplace_category_buildings, 20,
                       gc_ai_unit_dipcenter);
    ```

[^2]: Выбор характеристик по `csid+'dip'` с национальными вариантами —
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

[^6]: Настройка производства 8 наёмников —
      `lib/country.script:3010-3022`:

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

Обнуление пищи, дерева, камня, железа и угля —
`SetObjBasePrice(objbase, 0, 0, 0, gold, 0, 0)`,
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

[^13]: Проверка бунта в обработчике бездействия —
       `units/unit.inc/nothing.inc:487-506`:

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

[^16]: Враждебность служебного игрока ко всем участникам —
       `common.inc/initmap.inc:48-49`:

    ```pascal
    if i<>gc_MaxPlayerCount-1 then
    gPlayer[i].enemyplmask:=1 shl (gc_MaxPlayerCount-1);
    ```

[^17]: Стартовые ресурсы служебного игрока-наёмника —
       `lib/player.script:89-99`:

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

[^18]: Оценка ИИ важности защиты юнитов — `lib/unit.script:3941-3946`:

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
