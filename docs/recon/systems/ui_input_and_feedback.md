# Recon: интерфейс, ввод и обратная связь

Глубокий разбор: как игра реагирует на ввод (мышь, клавиатура,
скролл), какая обратная связь идёт игроку (alarm-уведомления,
звуки, выделение). Про связь со зрением и FOW — см. отдельную
секцию §5.

> **Связанные документы:**
> [`../world/combat/vision_and_fow.md`](../world/combat/vision_and_fow.md)
> — туман войны и обзор; [`../world/combat/unit_commands.md`](../world/combat/unit_commands.md)
> — какие приказы юнит понимает.

## TL;DR

- Ввод в C3 обрабатывается через **GUI-обёртку движка**: мышь,
  клавиатура, скролл — каждое событие триггерит конкретное
  скриптовое состояние (`SetGUIEventStateOnMouseDown` и т. п.).
- **Селекция** — через нативные `GameManagerStartSelection` /
  `EndSelection` с режимом `'spmRunTime'` (run-time pick) или
  `'spmFrame'` (frame-by-frame). Алгоритм выбора объекта под
  курсором — `RayCastIntersectGameObjectFromMouseRay` (нативно в
  движке).
- **Звуки и FOW — две независимые системы.** Звук эмитируется по
  расстоянию от listener'а (камеры или объекта), а **не по FOW**.
  Юнит во вражеском «тумане» **слышен**, если попадает в радиус
  слышимости камеры.
- **Alarm-уведомления** ("вас атакуют", "захватывают") срабатывают
  только если событие происходит **вне frustum'а камеры** (то
  есть игрок физически не смотрит туда).
- Лимит alarm-частоты: один alarm в `gc_gui_underattackalarminterval`
  игровых секунд (типично ~5 g-сек) — чтобы не спамить.

---

## 1. Селекция объектов

### 1.1. Старт сессии селекции

Когда игрок начинает выделять (рамкой или одиночным кликом):

1. Скрипт зовёт `GameManagerBeginSelection` — нативный API
   подготавливает буфер выбранных объектов.
2. `GameManagerStartSelection(mode)` запускает режим:
   - `'spmRunTime'` — для real-time клика (один frame).
   - `'spmFrame'` — для рамки выделения (каждый frame пока кнопка
     зажата).
3. Каждый кадр рамки скрипт зовёт `_control_*` функцию для обхода
   объектов и помечает попавших через `SetGameObjectPickedByHandle`.

### 1.2. Какие объекты могут быть выбраны

`SetGameManagerSelectionSettings(pickgroups, pickgamemanagerplayer,
pickplayableObject, ...)`:

| Параметр | Что |
|---|---|
| `pickgroups` | Можно ли выделять группы (отряды). |
| `pickgamemanagerplayer` | Можно ли выделить только своих или всех. |
| `pickplayableObject` | Только playable (юниты + здания), не декоративные NPC. |

Игрок-человек обычно работает в режиме «pickplayableObject = True
+ свой игрок». ИИ или редактор могут менять.

### 1.3. Команды селекции

Скриптовые функции в `lib/control.script`:

| Функция | Что |
|---|---|
| `_control_SelectAllUnits(bBuildings, bExcludePeasants)` | Выделить всё доступное на карте (Ctrl+A). |
| `_control_SelectAllShips()` | Все корабли. |
| `_control_SelectAllPeasants()` | Все крестьяне. |
| `_control_SelectIdlePeasants()` | Простаивающих крестьян (без ордера). |
| `_control_SelectIdleMines()` | Шахты с местом для крестьян. |
| `_control_DeselectAllUnits(bUpdateSelection)` | Сбросить выделение. |
| `_control_GetUnitUnderCursor()` | Возвратить handle юнита под курсором. |
| `_control_SelectOnlySquad()` | Оставить только отряды. |

**Control groups** (Ctrl+1 .. Ctrl+9 — связь группы с цифрой) на
уровне скриптов **не вычитаны как отдельные функции**. Возможно,
обрабатываются нативно через `SetGUIEventStateOn*`-callback'ы.

---

## 2. Ввод: мышь, скролл, клавиатура

### 2.1. Mouse-события

| Native API | Что регистрирует |
|---|---|
| `SetGUIEventStateOnMouseDown(state)` | Имя FSM-состояния, в которое перейдёт скрипт при mouse-down. |
| `SetGUIEventStateOnMouseUp(state)` | … при mouse-up. |
| `SetGUIEventStateOnMouseMove(state)` | … при движении мыши. |
| `SetGUIEventStateOnMouseWheel(state)` | … при скролле. |
| `SetGUIEventStateOnMouseEnterGUI(state)` / `OnMouseLeaveGUI(state)` | Когда курсор заходит / уходит из UI-элемента. |

То есть скриптовые событие-обработчики — это переходы FSM-сценария
GUI. Все они зарегистрированы единой системой через
`SetGUIEventState*`-функции.

### 2.2. Получение текущего ввода

| Функция | Возвращает |
|---|---|
| `GetGUICurrentMouseCoord(var ax, ay)` | Текущие пиксельные координаты курсора. |
| `GetGUIPreviousMouseCoord(var ax, ay)` | Предыдущие (для дельты). |
| `GetCurrentMouseWorldCoord(var x, y, z)` | Координаты в мировом пространстве (через raycast от курсора в землю). |
| `GameObjectRayCastMouseRay()` | Raycast от позиции курсора в мир — возвращает GameObject под курсором. |
| `GetGUIElementUnderMouse()` | Какой UI-элемент под курсором. |
| `GetGUIMinimapUnderMouse()` | Является ли курсор над миникартой. |

Ключевая функция: **`GetRayCastIntersectGameObjectFromMouseRay()`**
— берёт current mouse ray и возвращает **первый GameObject**, в
который этот ray попал. Это и есть то, что игрок «кликает» — юнит
или здание.

### 2.3. Скролл колеса

`GetGUIEventMouseWheelDelta()` — возвращает дельту последнего
скролла (положительная = вверх, отрицательная = вниз). По
умолчанию используется для приближения камеры:
- `SetCameraControlMouseWheelDistance(True)` — колесо меняет
  дистанцию.
- `SetCameraControlMouseWheelRotate(True)` — колесо поворачивает.

Только один из режимов активен. Профильные настройки через
`gProfile.*` — игрок может сменить.

### 2.4. Клавиатура

Прямого `OnKeyDown`-API в скриптах **не нашлось** — обработка
hotkey'ов и горячих клавиш делается на стороне **движка** через
GUI-FSM-callbacks (имена типа `OnKey_F1`, `OnKey_Ctrl_A`
регистрируются нативно).

Это значит, переназначить hotkey через скрипт — нельзя; нужно
менять в native-коде или через настройки `editor.exe`.

---

## 3. Курсор

| Функция | Что |
|---|---|
| `GUIGetCursorPos(var screenx, screeny)` | Текущие координаты в экранных пикселях. |
| `GUISetCursorPos(screenx, screeny)` | Программно переместить курсор. |
| `GUIShowCursor(show)` | Скрыть / показать. |
| `SetClipCursor(val)` | Залочить курсор внутри окна (для рамки выделения). |
| `SetGUICursorByName('cursor_name')` | Сменить визуал курсора. |

Курсорные образы — в `data/cursors/` (см.
[`../../../internals/data/layout.md`](../../../internals/data/layout.md)).
Например, при наведении на врага курсор меняется на «меч» — это
смена через `SetGUICursorByName('attack')`.

---

## 4. Камера

### 4.1. Управление

| Функция | Что |
|---|---|
| `SetCameraMouseRotateFactor(val)` | Чувствительность вращения. |
| `SetCameraMouseDistanceSpeed(val)` | Скорость зума. |
| `SetCameraControlMouseWheelDistance(b)` | Колесо = зум (по умолчанию `True`). |
| `SetCameraControlMouseWheelRotate(b)` | Колесо = поворот (по умолчанию `False`). |
| `MoveCameraToPosition(x, z, time)` | Плавное движение к точке (`time` в g-сек). |
| `MoveCameraToUnitsListCenter(list)` | К центру списка юнитов. |
| `MoveCameraToSelectedUnits()` | К выделенным (двойной-клик-на-портрет в C&C). |

Игрок прыгает к группе цифрой (1–9) через `_control_MoveCameraTo*`
+ выделение.

### 4.2. Listener (точка прослушки звука)

Звук в C3 эмитируется относительно **listener'а** — невидимой
точки, к которой привязан источник «уха» игрока:

- `GetSoundManagerListenerHandle()` — handle listener'а.
- `GetUseSoundManagerListenerAsCamera()` — `True` = listener
  привязан к камере (вы слышите то, на что смотрите).
- `GetUseSoundManagerListenerAsObject()` — listener привязан к
  объекту (например, к выбранному юниту).
- `SetPosSoundManagerListenerAsObject(x, y, z)` — программно
  поставить listener в точку.

В обычном skirmish listener = камера. Поэтому игрок слышит то, что
рядом с **камерой**, а не с выделенным юнитом или базой.

---

## 5. Звуки и FOW — две независимые системы

Это критическая деталь, **которую часто понимают неправильно**.

### 5.1. Как эмитируется звук юнита

Когда юнит совершает действие (выстрел, шаг, бой, смерть), скрипт
зовёт `SndGetOrCreateSound(emittertag, 'units', owner)` — нативная
функция создаёт звук-эмиттер на координатах **owner**-объекта.
Параметры эмиттера:

| Параметр | Что |
|---|---|
| `SetSndSoundMaxRadius(maxradius, sound)` | Радиус слышимости в мире. |
| `SetSndSoundMinDist(value, sound)` / `MaxDist` | Расстояние полной громкости / нулевой громкости (linear falloff). |
| `SetSndSoundMaxRadiuses(rmaxvolume, radius, sound)` | Радиус 100 % громкости + общий радиус. |
| `SetSndSoundLoop(value, sound)` | Зацикленный звук (фоновый). |
| `SetSndSoundKillSndOutRad(value, sound)` | «Убить звук, если listener вне радиуса». |
| `SetSndSoundConeOutsideVolume`, `InsideConeAngle`, `OutsideConeAngle` | Направленный звук. |

Решение «играть или нет» — на основе **расстояния от listener'а**.
**Никаких проверок FOW в этих функциях нет.**

### 5.2. Что это значит

- **Юнит во вражеском FOW** (вы его не видите) **слышен**, если
  он попадает в радиус слышимости (`SetSndSoundMaxRadius`).
- Например: вражеский мушкетёр стреляет в скрытом лесу — вы
  **слышите выстрел**, но **не видите** ни юнита, ни вспышку.
- Это даёт игроку **акустическую разведку**: можно по звукам
  определить, что вражеский отряд зашёл с фланга, ещё до того как
  его увидит ваш скаут.

### 5.3. Почему так сделано

Два технических решения:

1. **Один listener (камера)** в стандартном режиме. FOW считается
   per-player, но звук — per-listener. Если бы движок проверял
   FOW для звука, пришлось бы фильтровать каждый эмиттер по
   текущему игроку — дорого по CPU.
2. **Realism trade-off.** Звук распространяется в реальности
   независимо от того, видишь ли ты источник. Cossacks 3 это
   эмулирует.

См. также [`vision_and_fow.md`](../world/combat/vision_and_fow.md)
о структуре FOW.

---

## 6. Alarm-уведомления

`_misc_DoAlarm(goHnd, trgHnd, event)` [^1] — главная функция для
сигнала «обратите внимание». Срабатывает когда:

- Юнит игрока получил атаку (`gc_gui_alarmevent_attack`).
- Здание игрока захватывают (`gc_gui_alarmevent_capture`).
- И другие события (`gc_gui_alarmevent_*`).

### 6.1. Условия срабатывания

```pascal
if (gPlayer[plIO].lastattacktime = 0) then  // не было недавнего alarm
   if (trgPlHnd = plIOHnd or plHnd = plIOHnd) then  // событие касается игрока
      if (not gSoundManager.IsObjInFrustum(handle)) then  // объект НЕ в frustum камеры
         alarm fire
```

Ключевое: **alarm срабатывает только если объект НЕ в frustum**
камеры. То есть если игрок физически смотрит на свою базу и в
этот момент её атакуют — уведомление **не будет**, потому что
игрок и так это видит.

### 6.2. Лимит частоты

После срабатывания alarm устанавливается
`gPlayer[plIO].lastattacktime = currenttime + gc_gui_underattackalarminterval`.
Следующие события блокируются до истечения интервала. Типично
интервал ~5 g-сек, чтобы не получать «вас атакуют» каждый тик
длительного боя.

### 6.3. Что игрок видит и слышит

| Эффект | Источник |
|---|---|
| Звук «трубы / barbarian shout» | Скрипт ставит `gbool_gui_doalarm := True`, GUI воспроизводит звук. |
| Мигающая рамка по краю экрана | UI-элемент, реагирует на `gbool_gui_doalarm`. |
| Стрелка-указатель к месту события | По координатам `gfloat_gui_alarmx`, `gfloat_gui_alarmz`. |

Игрок может прыгнуть камерой к месту через хоткей (двойной space
или Ctrl+W в зависимости от профиля) — это вызывает
`MoveCameraToPosition(alarmx, alarmz, ...)`.

### 6.4. Не алармирует

- **Атаки на не-владельца.** `_misc_DoAlarm` проверяет
  `plIOHnd = trgPlHnd or plIOHnd = plHnd`. Союзник в команде по
  умолчанию **не получит алярм** про атаку союзника — у каждого
  свой `plIO`.
- **Атаки священника** (он в `bpriest` — лечит, не атакует).
  Скрипт пропускает alarm-вызов в `_misc_DoDamage`, если атакующий
  — священник.

---

## 7. Hotkey-конфиг

Hotkey'и определены в `data/game/var/hotkeys.cfg` —
parser-формат с записями вида:

```
[*] : struct.begin
   Key = Ctrl+A
   Action = select|allunits
   Repeat = True
struct.end
```

### 7.1. Структура записи

| Поле | Что |
|---|---|
| `Key` | Основная клавиша или комбинация (`A`, `Ctrl+A`, `Ctrl+Alt+A`, `Shift+Z` и т. п.). Пустое значение означает, что hotkey не назначен по умолчанию. |
| `AlternativeKey` | Запасная комбинация (опционально). |
| `Action` | Описание действия в формате `<тип>\|<параметр>`. |
| `Repeat` | Если `True`, повторное нажатие циклирует через варианты (например, `select|allunits` → следующий выделенный отряд того же типа). |
| `Up` | Если `True`, действие срабатывает по отпусканию клавиши, не по нажатию. |

### 7.2. Шесть типов `Action`

| Тип | Что делает | Примеры |
|---|---|---|
| `build` | Поставить здание из меню постройки | `build\|%nat%cen` (Городской центр), `build\|%com%mil` (мельница). `%nat%` подставляется на текущий sid нации, `%com%` — кластер (`eur` / `rus` / `tur` …). |
| `unit` | Команда выбранным юнитам | `unit\|attack`, `unit\|standground`, `unit\|nostandground`, `unit\|guard`, `unit\|cancelguard`, `unit\|attackpoint`, `unit\|enableattack`, `unit\|disableattack`, `unit\|stop`, `unit\|unloadall` |
| `squad` | Команды отряду | `squad\|fill`, `squad\|disband`, `squad\|rank` (LINE), `squad\|column`, `squad\|square` |
| `select` | Селекция по фильтру | `select\|allunits`, `select\|allships`, `select\|allbuildings`, `select\|allpeasants`, `select\|idlepeasants`, `select\|idlemines`, `select\|militaryunits`, `select\|unitsofsametype`, `select\|addunitsofsametype`, `select\|allunitsofsametype`, `select\|addallunitsofsametype` |
| `interface` | UI-эффект | `interface\|minimap` (свернуть/развернуть миникарту), `interface\|viewcollision` (debug — collision grid). |
| `event` | Триггер UI-state | `event\|eventmainmenu\|bcampaign` (открыть кампанию), `event\|eventmainmenu\|brandommap`, и т. д. |

### 7.3. Дефолтные хоткеи (фрагмент)

| Клавиша | Действие |
|---|---|
| `A` | `unit\|attack` (атака-move) |
| `S` | `unit\|standground` |
| `C` | `unit\|nostandground` (снять standground) |
| `G` | `unit\|guard` |
| `R` | `unit\|attackpoint` (артиллерийская стрельба по точке) |
| `F` | `squad\|fill` (пополнить отряд) |
| `J` / `K` / `L` | `squad\|rank` / `squad\|column` / `squad\|square` |
| `Ctrl+S` | `unit\|stop` |
| `U` | `unit\|unloadall` (выгрузить из транспорта / гарнизона) |
| `Z` | `select\|unitsofsametype` (Repeat — следующий) |
| `Shift+Z` | `select\|addunitsofsametype` |
| `Ctrl+A` | `select\|allunits` |
| `Ctrl+B` | `select\|allbuildings` |
| `Ctrl+M` | `select\|idlemines` |
| `Ctrl+P` или `` ` `` | `select\|idlepeasants` |
| `Ctrl+\`` | `select\|allpeasants` |
| `Ctrl+Q` | `select\|allships` |
| `Ctrl+Alt+A` или `Ctrl+Shift+A` | `select\|militaryunits` |
| `Q` | `interface\|viewcollision` |
| `Alt+M` | `interface\|minimap` |

И большой набор `build|...` (по одной букве на каждое здание) — `C` = Cen, `H` = House, `B` = Bar, `L` = Bla, `E` = Aca, `S` = Sta, `D` = Dip, `M` = Mar, `T` = Tow, `P` = Por, и т. д.

> **Дубликаты** разрешены: `S` встречается у `build|sta`, `unit|standground`
> и `event|eventmainmenu|bsettings`. Контекст разрешения — какое
> состояние GUI активно (in-game / unit-selected / menu-open).

## 8. Reserved keys — нельзя переназначить

Файл `data/gui/menu.inc/hotkeysettings.inc` содержит два списка
`forbiddenkeys` (нельзя поставить как одиночную клавишу) и
`forbiddencombokeys` (запрещённые комбинации). Это и есть «движковые»
hotkey'и — которые не настраиваются через UI, потому что встроены в
поведение игры.

### 8.1. Одиночные зарезервированные клавиши

| Клавиша | Зарезервирована за |
|---|---|
| `LButton`, `RButton`, `MButton` | Кнопки мыши — селекция / приказ / drag-камера. |
| `Left`, `Right`, `Up`, `Down` | Скролл камеры по сторонам света. |
| `Space` | Прыжок к последнему алярму (центрировать камеру). |
| `Return` (Enter) | Открыть chat в multiplayer. |
| `Escape` | Закрыть UI / отменить режим (build mode, attack-move). |
| `Shift`, `Ctrl`, `Alt` (+ их up-варианты) | Модификаторы — нельзя переназначить как одиночные. |
| **`0`, `1`, …, `9`** | **Control groups — выделить группу.** |
| **`NUM0`–`NUM9`** | Дублёры цифр на numpad'е для control groups. |
| `F5`, `F7`, `F10` | Quick-save / quick-load / debug. |
| `PrintScreen0/1/2` | Снимок экрана (стандартное Windows-поведение). |
| `Sub`, `Add`, `-`, `=` | Скорость игры (slow / fast). |
| `PGUP`, `PGDN`, `Home`, `Del`, `Back` | Навигация по логу / удаление. |
| `P` | Pause. |
| `[`, `]` | Прокрутка алярмов / уведомлений. |

### 8.2. Зарезервированные комбинации (control groups + системные)

**Control groups (10 штук, цифры 0–9):**

| Комбинация | Что |
|---|---|
| **`Ctrl+0` … `Ctrl+9`** | **Назначить** текущее выделение в control group N. |
| **`Shift+0` … `Shift+9`** | **Добавить** текущее выделение в control group N. |
| **`Alt+0` … `Alt+9`** | **Выделить** control group N. |
| **`Shift+Alt+0` … `Shift+Alt+9`** | Дополнительный режим (вероятно: добавить группу N к текущему выделению). |

То есть в Cossacks 3 — **10 control groups** (0–9), стандартный набор управления.

**Камера и системные:**

| Комбинация | Назначение |
|---|---|
| `Alt+F4` | Закрыть приложение. |
| `Ctrl+S` | Quick save. |
| `Ctrl+Tab` | Переключение игрока (spectator / replay). |
| `Ctrl+Home` | Центрировать камеру на стартовую точку игрока. |
| `Ctrl+PGUP` / `Ctrl+PGDN` | Прокрутка вкладок UI / переключение игрока. |
| `Ctrl+W`, `Ctrl+F` | Camera quick-jump (наверное — к Городскому центру / к выделенному). |
| `Ctrl+Add` / `Ctrl+Sub` | Zoom in / out. |
| `Ctrl+Shift+P` | Debug-режим. |
| `Ctrl+T` | Team chat (отдельно от обычного chat по `Return`). |
| `Alt+Mul` (numpad *) | Сменить режим миникарты. |
| `Shift+Alt+Mul` | Расширенный режим миникарты. |

### 8.3. RTTI-классы для группы

В RTTI exe найдены классы `TXGroup4` (один из десяти?) и
`TXGroupSelectionViewer` — последний рисует **зелёные подсветки**
вокруг юнитов, входящих в активную control group. Реализация
control-group-привязки на скриптовом уровне отсутствует
(`SetGUIEventStateOnKeyDown` в `lib/*.script` зовётся только для
`'EventMultiplayerChat'`). Значит обработка цифровых клавиш для
control groups делается **в native exe**, без вызова скриптов.

## 9. Игровой темп и пауза

### 9.1. Скорость игры

`_control_GetGameSpeedMode` / `_control_SetGameSpeedByMode`:

| Mode | Значение |
|---|---:|
| `slow` (0) | 7 тиков/сек |
| `normal` (1) | 10 тиков/сек |
| `fast` (2) | **14 тиков/сек** (по умолчанию в skirmish) |

Hotkey: `Ctrl+Add` (numpad +) / `Ctrl+Sub` (numpad −) — оба
зарезервированы (см. §8.2).

### 9.2. Pause

Hotkey `P` — зарезервирован (см. §8.1). Лимит: **4 паузы по 120
секунд** на партию (упомянуто в старом ref: «pause-limit
(4 × 120 секунд)»).

## 10. Доступ скрипта к клавиатуре

Native API для проверки клавиш [^2]:

| Функция | Что |
|---|---|
| `IsKeyDown(vk: Integer): Boolean` | Нажата ли клавиша по virtual-key code. |
| `IsKeyDownByName(sname: String): Boolean` | По имени (`'Ctrl'`, `'Shift'`, `'A'`). |
| `KeyPressed(minvkcode: Integer): Integer` | Код последней нажатой клавиши с `vkcode >= minvkcode`. |

В скриптах **не вызываются** вообще — обработка ввода идёт
полностью через GUI-FSM-callback'и (`SetGUIEventStateOn*`). Скриптам
проверять «нажат ли Shift» обычно не нужно, потому что GUI-state
уже учитывает модификаторы.

---

## 11. Открытые вопросы

1. **Точная семантика `Shift+Alt+0..9`.** Forbidden-список
   подтверждает, что комбинация зарезервирована, но что она делает —
   не вычитано из кода.
2. **Звук + FOW для дружественных объектов.** Если юнит союзника
   вне твоего FOW (но в его FOW), слышишь ли ты его? Гипотеза: да,
   listener видит весь мир по расстоянию.
3. ~~`gc_gui_underattackalarminterval` — точное значение~~ ✅
   **Закрыто:** `= 135` (`dmscript.global`). Единица — внутренний
   счётчик `GetCurrentTime`, скорее всего **frames** → `135 / 32 ≈
   4.22 g-sec`. То есть alarm не срабатывает чаще одного раза в
   ~4 g-secунды.
4. **Двойной-клик на портрет юнита** — прыгает ли камера? В коде
   `MoveCameraToSelectedUnits` есть, но триггер не уточнён в
   скриптах.

---

## Источники

[^1]: `data/scripts/lib/misc.script` — `_misc_DoAlarm(goHnd,
      trgHnd, event)`. Использует `gSoundManager.IsObjInFrustum(handle)`
      для проверки «вне поля зрения камеры». Гейт через
      `gPlayer[plIO].lastattacktime` и
      `gc_gui_underattackalarminterval`.

[^2]: Native API `IsKeyDown`, `IsKeyDownByName`, `KeyPressed` —
      см. [`derived/dws_native_signatures.json`](../../../derived/dws_native_signatures.json).
      Hotkey-конфиг — `data/game/var/hotkeys.cfg`. Forbidden-keys —
      `data/gui/menu.inc/hotkeysettings.inc:1-100`.
