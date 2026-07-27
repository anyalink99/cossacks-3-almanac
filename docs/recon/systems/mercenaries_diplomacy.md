# Наёмники и Дипломатический центр

[← Как устроена игра](../README.md)

Как устроены найм в Дипломатическом центре, содержание армии за золото,
рост цены и бунт при пустой казне. Внутренние идентификаторы и выдержки
из Pascal собраны в [технических подробностях](#технические-подробности)
и [источниках](#источники).

**Связанные документы:**

- [Добыча ресурсов крестьянами](../world/economy/peasant_extraction.md) —
  почему наёмники не расходуют пищу.
- [Строительство и свойства зданий](../world/economy/building_mechanics.md) — занимаемая площадь и модель
  постройки дипломатического центра.
- [Синхронизация сетевой игры](../../../internals/engine/server_sync_architecture.md) —
  почему смену владельца при бунте подтверждает сервер.
- [Проверка детерминизма](../../../internals/engine/determinism_audit.md) —
  как согласуется случайный выбор перебежчиков.

## Кратко

- **Дипломатический центр** — здание середины партии у каждой
  из 21 нации. Обычная цена — 4900 дерева и 1700 камня, прочность —
  4500; для постройки нужны Академия и Городской центр.
- Производит **6 базовых наёмников**; набор Early Bird добавляет ещё
  **2 варианта**. Доступный состав одинаков у всех наций, а характеристики
  юнитов не зависят от нанявшей их стороны.
- Наёмник стоит **только золото**, не расходует пищу, но
  **постоянно потребляет золото** на содержание.
- Если золото закончилось, а расходы выше дохода, каждый наёмник может
  перейти на сторону враждебной всем армии:
  - **лёгкий уровень**: 0,305 % за проверку;
  - **обычный уровень**: 0,610 %;
  - **сложный и выше**: 18,31 %.

---

## Дипломатический центр у разных наций

У каждой из 21 нации доступен один вариант здания. Большинство европейских
стран используют общие характеристики; Россия, Украина, Турция и Алжир
имеют собственные значения [^1] [^2].

| Здание | Нации | Прочность | Время постройки, игровых секунд | Дерево | Камень | Золото | Можно захватить |
|---|---|---:|---:|---:|---:|---:|---|
| Дипломатический центр | Австрия, Франция, Англия, Испания, Польша, Швеция, Пруссия, Венеция, Нидерланды, Дания, Португалия, Пьемонт, Саксония, Бавария, Венгрия, Швейцария, Шотландия | 4500 | 312,5 | 4900 | 1700 | 0 | Нет |
| Дипломатический центр | Россия | 6500 | 312,5 | 7900 | 3700 | 0 | Нет |
| Дипломатический центр | Украина | 5000 | 312,5 | 3900 | 2700 | 0 | Нет |
| Дипломатический центр | Турция, Алжир | 5500 | 312,5 | 4600 | 2020 | 0 | Нет |

Для строительства нужна Академия. **Дипломатический центр захватить
нельзя**, а предшествующую ему Академию — можно.

---

## Кого можно нанять

В **каждой** нации доступны шесть базовых наёмников: Лёгкий пехотинец,
Рундашир, Гренадер, Лучник, Сечевой козак и Драгун XVIII века.
При наличии набора Early Bird к ним добавляются Турецкий лучник и Лёгкий
кавалерист [^5].
Для найма нужны Городской центр, Академия и сам Дипломатический центр [^6].

### Общие правила

Все нации получают один и тот же набор с одинаковыми характеристиками.
Наёмные версии используют отдельные цену, прочность, оружие и содержание,
даже если происходят от похожего обычного юнита [^7].

### Характеристики наёмников

| Наёмник | Доступность | Прочность | Время найма, игровых секунд | Цена, золото | Содержание золотом | Рост цены, % | Оружие: урон / дальность, клетки |
|---|---|---:|---:|---:|---:|---:|---|
| **Лёгкий пехотинец** | Основной набор | 50 | 1,25 | 4 | 4 | 100 | меч: 16 / 0,94 |
| **Рундашир** | Основной набор | 75 | 1,5 | 12 | 20 | 100 | меч: 6 / 0,94 |
| **Лучник** | Основной набор | 20 | 1,25 | 15 | 16 | 100,5 | стрела: 25 / 13,13; огненная стрела: 100 / 14,06 |
| **Турецкий лучник** | Early Bird | 20 | 1,25 | 15 | 16 | 100,5 | как у Лучника |
| **Гренадер** | Основной набор | 30 | 1,5 | 25 | 60 | 100,5 | пика: 30; пуля: 16 / 15; граната: 200 / 7,5 |
| **Сечевой козак** | Основной набор | 150 | 2,5 | 60 | 150 | 100,5 | конная сабля: 8 / 0,38 |
| **Драгун XVIII века** | Основной набор | 100 | 2 | 120 | 120 | 102 | конная пуля: 18 / 15 |
| **Лёгкий кавалерист** | Early Bird | 100 | 2 | 120 | 120 | 102 | как у Драгуна XVIII века |

Все ветки наёмников отключают расход пищи, а в цене найма оставляют только
золото [^8]. Поэтому **наёмники стоят только золото** и не расходуют пищу
на содержание (см. [голод и содержание армии](../world/economy/hunger_and_rebellion.md)).

### Рост цены и общие счётчики

В таблице выше рост цены равен 100 %, 100,5 % или 102 %. Стоимость следующего
наёмника рассчитывается так [^9]:

**цена = базовая цена × (рост / 100)<sup>N</sup>, с округлением вниз**,

где N — число ранее нанятых юнитов в соответствующей группе. Лучник делит
такой счётчик с Турецким лучником, а Драгун XVIII века — с Лёгким
кавалеристом. Поэтому найм 100 Турецких лучников повышает цену обычного
Лучника; то же правило действует внутри второй пары.

Цена наёмника может вырасти максимум до **2×** от базовой. Для сравнения,
обычный юнит может достичь технического потолка 20 000×. При росте 100,5 %
предел 2× достигается примерно после
**логарифм(2) / логарифм(1,005) ≈ 139** общих наймов, после чего цена
перестаёт расти.

---

## Содержание за золото

Золото на содержание списывается тем же непрерывным расчётом, что и пища
(см. [голод и содержание армии](../world/economy/hunger_and_rebellion.md)).
Дробный расход накапливается каждый кадр, а целые единицы периодически
снимаются из казны [^10]. Если запаса не хватает, игра списывает остаток и
проверяет условия бунта.

### Скорость утечки золота

Формула использует значения из столбца «Содержание золотом»:

**золота в игровую секунду = сумма содержания всех юнитов × 32 / 20 000**.

Один наёмный Драгун XVIII века со значением 120 расходует
**120 × 32 / 20 000 = 0,192** золота в игровую секунду, или примерно
**11,5 золота в игровую минуту**. Пятьдесят таких Драгунов расходуют
9,6 золота в игровую секунду, или 576 в игровую минуту. Такой отряд обычно
требует Рынка и нескольких золотых Шахт.

### Почему пустая казна не всегда вызывает бунт

Для бунта недостаточно на мгновение остаться без золота. Одновременно должны
выполняться два условия: запас равен нулю, а расход золота выше текущего
дохода [^11]. Если Шахты полностью покрывают содержание, наёмники остаются
верны даже при пустой казне.

Бунт прекращается, когда запас достигает хотя бы двух единиц золота или
содержание наёмников падает до нуля [^12]. Поэтому расформирование всех
наёмников немедленно прекращает кризис.

---

## Как начинается бунт

После начала бунта каждый живой наёмник отдельно проходит случайную проверку
во время бездействия или движения [^13] [^14]:

| Сложность | Подходящих исходов из 32 768 | Вероятность за одну фоновую проверку |
|---|---:|---:|
| Легко | 100 | 100 / 32 768 ≈ **0,305 %** |
| Нормально | 200 | 200 / 32 768 ≈ **0,610 %** |
| Сложно, Очень сложно или Невозможно | 6 000 | 6 000 / 32 768 ≈ **18,31 %** |

На сложном уровне и выше типичному наёмнику требуется около **5–6 подходящих
проверок** до дезертирства. Это оценка риска за проверку, а не таймер:
фактическое время также зависит от интервала обработки состояния юнита.

При успешной проверке юнит переходит к управляемой игрой стороне, которая
изначально враждебна всем обычным участникам [^15] [^16].

Поэтому дезертировавшие наёмники становятся враждебны **всем**, включая
бывшего хозяина. Их не уничтожают.

Управляемая игрой армия начинает с фиксированным запасом: 20 000 золота и
по 10 000 остальных ресурсов [^17]. Дезертиры продолжают оплачивать
содержание, но повторно перейти на другую сторону уже не могут.

### Штраф к очкам

Когда мятежный наёмник переходит к управляемой игрой стороне, из счёта
прежнего владельца сразу вычитается **3× базовая ценность юнита** [^18].
В тот же момент новому владельцу начисляется обычная **1× базовая
ценность**. Это штраф именно за **смену владельца во время бунта**, а не за
последующую гибель или потерю юнита.

Для сравнения, при удалении объекта из счётчиков прежнего владельца обычный
множитель равен **2×**, а для ранее захваченного объекта — **5×**. Очки
влияют на итоговую статистику, но не на решения компьютерного игрока и не
на исход партии.

---

## Настройка лобби «Рынок и Дипломатический центр»

Настройка имеет пять вариантов [^19]:

| Вариант | Результат |
|---|---|
| По умолчанию | Рынок и Дипломатический центр доступны |
| Без дип. центра | Дипломатический центр недоступен |
| Без рынка | Рынок недоступен |
| Не доступны | Оба здания недоступны |
| Дорогие наёмники | Цена найма каждого наёмника утраивается |

При варианте «Дорогие наёмники» стоимость меняется так: 4 → 12, 60 → 180,
120 → 360, 150 → 450 и далее [^20] [^21]. Наёмники покупаются только за
золото, поэтому игрок видит именно утроенную золотую цену. Полная таблица
значений приведена в [настройках матча](../../reports/map/lobby_settings.md#marketdip--рынок-и-дипцентр).

---

## Где нанимают наёмников

На стандартной случайной карте **наёмников нанимают только в собственном
Дипломатическом центре** с требованиями, перечисленными выше. У управляемой
игрой армии, к которой переходят дезертиры, нет зданий для найма.

Нейтральный Дипломатический центр может быть заранее размещён автором
сценария, но это правило конкретной миссии, а не обычной случайной карты.

---

## Доступность для разных наций

**Любая нация может нанимать любого наёмника.** Рундашир, Лёгкий пехотинец,
Лучник, Гренадер, Сечевой козак и Драгун XVIII века доступны всегда.
Лёгкий кавалерист и Турецкий лучник требуют дополнительного набора [^5].

Различие внутри пар — только **вариант оформления и модели**: Лучник и
Турецкий лучник, как и Драгун XVIII века и Лёгкий кавалерист, имеют
одинаковые характеристики, а их цена растёт от общего количества наймов
([см. рост цены](#рост-цены-и-общие-счётчики)). Отличается только внешний
вид: «западный» или «восточный».

Правила офицерских формаций немного отличаются [^23]: Рундаширы и
Гренадеры могут входить в стандартные пехотные формации вместе с
национальными Пикинёрами и Мушкетёрами. Лучники, Турецкие лучники и Лёгкие
пехотинцы формируют собственные строи без национального Офицера.

---

## Сравнение с обычными юнитами

### Стоимость

Наёмники требуют **только золото и время найма**; обычным юнитам нужны
пища, железо и уголь, а затем пища на содержание. Например, для тяжёлого
конного стрелка:

| Юнит | Пища | Железо | Уголь | Золото | Цена выстрела | Прочность | Время найма |
|---|---:|---:|---:|---:|---|---:|---:|
| **Драгун XVIII века** (обычный европейский) | 70 | 7 | 0 | 60 | 4 железа + 5 угля | 225 | 22,5 игровой секунды |
| **Драгун XVIII века (наёмник)** | 0 | 0 | 0 | 120 | 5 железа + 8 угля | **100** | **2 игровые секунды** |

То есть наёмный Драгун стоит на 60 золота дороже и не требует пищи,
железа или угля при найме. Он **нанимается в 11 раз быстрее**, но имеет
44 % прочности обычного Драгуна, расходует немного больше железа и угля
за выстрел и постоянно требует золото на содержание.

Сходное соотношение у Лучника: наёмная версия нанимается немного медленнее,
но не требует пищи и наносит 25 урона вместо 15.

### Содержание

- Обычный уязвимый к голоду юнит получает общую надбавку 30 к личному
  показателю содержания. Расход пищи в игровую секунду равен этой сумме,
  умноженной на 32 / 20 000 (см.
  [голод и содержание армии](../world/economy/hunger_and_rebellion.md)).
  Наёмники пищу не расходуют.
- Значение золотого содержания в таблице составляет от 4 до 150; расход за
  игровую секунду равен этому значению, умноженному на 32 / 20 000.
- Офицеры и Королевские мушкетёры тоже расходуют золото, но к наёмникам не
  относятся и поэтому не бунтуют.

### Когда брать наёмников (стратегический профиль)

Наёмники — это, по сути, **армия быстрого развёртывания за золото**:

- **Ранняя игра.** Нации с избытком дерева и слабым доступом к железу
  и углю могут быстро получить пехоту: обменять дерево и камень на
  золото и нанять Рундаширов или Лёгких пехотинцев.
- **Середина партии.** Избыток золота от союзной торговли или захваченных
  шахт можно быстро превратить в армию Драгунов XVIII века без
  ожидания угольных шахт.
- **Высокий урон ценой живучести.** Прочность примерно вдвое ниже, чем у
  обычных юнитов того же класса, — но преимущество в скорости найма у
  дорогих конных стрелков огромное: наёмный Драгун XVIII века тренируется
  2 игровые секунды против 22,5 у обычного — **в 11,25 раза быстрее**.

**Главный риск — обрыв дохода золота.** Если доход становится меньше
расходов, а запас падает до нуля, на сложном уровне и выше наёмники начинают
часто проверять вероятность дезертирства. Безопасный ответ — расформировать
их **до** опустошения казны.

---

## Технические подробности

Точные поля, обработчики и ветви, убранные из читательских разделов,
сгруппированы в источниках ниже: расчёт цены и парные идентификаторы — [^9],
накопитель содержания и условия дефицита — [^10] [^11] [^12], проверка
бунта и служебный владелец — [^13] [^14] [^15] [^16] [^17], изменение
очков — [^18], варианты настройки лобби — [^19] [^20] [^21].

Дипломатический центр регистрируется как `<nat>dip` через
`_country_AddMember`; его роль для ИИ — `gc_ai_unit_dipcenter`, а назначение
объекта — `gc_obj_usage_dipcenter = 32` [^1] [^4]. Общий вариант используют
`aus`, `fra`, `eng`, `spa`, `pol`, `swe`, `pru`, `ven`, `net`, `den`,
`por`, `pie`, `sax`, `bav`, `hun`, `swi`, `sco`; отдельные ветки имеют
`rusdip`, `ukrdip`, `turdip` и `algdip` [^2].

Вызов `SetObjBuildingExtProperties` передаёт
`maxhp, buildtime, costpercent, bcapture, score, usage, food, wood, stone,
gold, iron, coal` [^3]. У Дипломатического центра `bcapture=False` и
`costpercent=100`; у Академии `bcapture=True`. Комментарий `0{1000}` рядом
с нулевой золотой ценой сохраняет старое значение из первых «Казаков».

Наёмники распознаются по восьми внутренним идентификаторам:
`lightinfantrydip`, `roundshierdip`, `grenadierdip`, `archerdip`,
`cossacksichdip`, `dragoon18dip`, `archerturdip`, `lightcavalrydip`.
Ветка `bmercenary` переопределяет их прочность, оружие, цену,
`consume.gold`, `bnohungry` и `costpercent` [^7] [^8].

На случайной карте у обычных игроков `bneutral = False`; это поле меняют
сценарии [^22]. Служебный владелец `gc_player_mercenaryind` не имеет
зданий и нужен только для дезертировавших юнитов. Рундашир и Гренадер
регистрируются для обычных офицерских формаций, а Лучник, Турецкий лучник
и Лёгкий пехотинец используют ветку `…NoOfficersExtDip` [^23].

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

[^5]: Регистрация шести базовых наёмников и двух вариантов Early Bird через
      `_country_AddMember` —
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

[^6]: Настройка производства шести базовых и двух дополнительных наёмников —
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

[^18]: Штраф к очкам прежнего владельца при потере объекта —
       `lib/unit.script:3941-3947`:

    ```pascal
    if (bcaptured) then
       scoremodifier := 5
    else
    if (gPlayer[pl].brebellion) and (TObjProp(pobjprop).bmercenary) then
       scoremodifier := 3
    else
       scoremodifier := 2;
    ```

    Затем выполняется
    `gPlayer[pl].counter.scores -= score * scoremodifier`.

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
