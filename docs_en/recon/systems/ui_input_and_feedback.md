<a id="recon-интерфейс-ввод-и-обратная-связь"></a>
<a id="управление-и-обратная-связь"></a>
# Controls and Player Feedback

[← How the game works](../README.md)

How the game responds to the mouse, keyboard, and wheel, and how it
reports events through sound, highlighting, and warnings. Section §5
explains the relationship with vision and fog of war.

> **Related documents:**
> [`../world/combat/vision_and_fow.md`](../world/combat/vision_and_fow.md)
> — fog of war and overview; [`../world/combat/unit_commands.md`](../world/combat/unit_commands.md)
> - what orders the unit understands.

<a id="кратко"></a>
## TL;DR

- C3 routes mouse, keyboard, and wheel input through an engine interface
  layer. Each event activates a script state such as
  `SetGUIEventStateOnMouseDown`.
- **Selection** uses the engine functions `GameManagerStartSelection` and
  `EndSelection`, with `spmRunTime` for a single pick or `spmFrame` for
  a selection box. `RayCastIntersectGameObjectFromMouseRay` finds the
  object under the cursor.
- **Sound and fog of war are independent.** Audibility depends on distance
  from the listener—the camera or an object—not on visibility. A hidden
  enemy unit can still be heard.
- **Warnings** such as “under attack” or “being captured” appear only
  when the event is **outside the camera frustum**.
- `gc_gui_underattackalarminterval` limits warning frequency to roughly
  one every five game seconds.

---

<a id="1-селекция-объектов"></a>
<a id="1-выделение-объектов"></a>
## 1. Object selection

<a id="11-старт-сессии-селекции"></a>
<a id="11-начало-выделения"></a>
### 1.1. Starting a selection

When the player begins a box selection or clicks a unit:

1. `GameManagerBeginSelection` prepares the selection buffer.
2. `GameManagerStartSelection(mode)` starts either:
   - `spmRunTime` for a one-frame click;
   - `spmFrame` for a box updated every frame while the button is held.
3. Each box-selection frame, a `_control_*` function scans objects and
   marks matches with `SetGameObjectPickedByHandle`.

<a id="12-какие-объекты-могут-быть-выбраны"></a>
### 1.2. What objects can be selected

`SetGameManagerSelectionSettings(pickgroups, pickgamemanagerplayer, pickplayableObject, ...)`:

| Parameter | What |
|---|---|
| `pickgroups` | Whether squads can be selected. |
| `pickgamemanagerplayer` | Whether selection is restricted by owner. |
| `pickplayableObject` | Whether to select only playable units and buildings, excluding decorative NPCs. |

Human players normally use `pickplayableObject = True` and an owner
filter for their own player. AI and editor tools can change these settings.

<a id="13-команды-селекции"></a>
### 1.3. Selection commands

Script functions in `lib/control.script`:

| Function | What |
|---|---|
| `_control_SelectAllUnits(bBuildings, bExcludePeasants)` | Select everything available on the map (Ctrl+A). |
| `_control_SelectAllShips()` | All ships. |
| `_control_SelectAllPeasants()` | All peasants. |
| `_control_SelectIdlePeasants()` | Idle Peasants without an order. |
| `_control_SelectIdleMines()` | Mines with space for peasants. |
| `_control_DeselectAllUnits(bUpdateSelection)` | Reset selection. |
| `_control_GetUnitUnderCursor()` | Return the handle of the unit under the cursor. |
| `_control_SelectOnlySquad()` | Keep only squads selected. |

**Control groups** (Ctrl+1 .. Ctrl+9 - linking a group with a number) on
the script layer are **not exposed as separate functions**. They are
probably handled by the engine through `SetGUIEventStateOn*`.

---

<a id="2-ввод-мышь-скролл-клавиатура"></a>
## 2. Input: mouse, scroll, keyboard

<a id="21-mouse-события"></a>
<a id="21-события-мыши"></a>
### 2.1. Mouse events

| Engine function | Registered transition |
|---|---|
| `SetGUIEventStateOnMouseDown(state)` | Interface state for pressing a mouse button. |
| `SetGUIEventStateOnMouseUp(state)` | Interface state for releasing the button. |
| `SetGUIEventStateOnMouseMove(state)` | Interface state for mouse movement. |
| `SetGUIEventStateOnMouseWheel(state)` | ... when scrolling. |
| `SetGUIEventStateOnMouseEnterGUI(state)` / `OnMouseLeaveGUI(state)` | When the cursor enters/leaves a UI element. |

Input handlers therefore switch interface states. The
`SetGUIEventState*` family registers all of these transitions.

<a id="22-получение-текущего-ввода"></a>
### 2.2. Getting current input

| Function | Returns |
|---|---|
| `GetGUICurrentMouseCoord(var ax, ay)` | Current pixel coordinates of the cursor. |
| `GetGUIPreviousMouseCoord(var ax, ay)` | Previous (for delta). |
| `GetCurrentMouseWorldCoord(var x, y, z)` | Coordinates in world space (via raycast from the cursor to the ground). |
| `GameObjectRayCastMouseRay()` | Cast a ray from the cursor into the world and return the game object under it. |
| `GetGUIElementUnderMouse()` | Which UI element is under the cursor. |
| `GetGUIMinimapUnderMouse()` | Whether the cursor is above the minimap. |

Key function: **`GetRayCastIntersectGameObjectFromMouseRay()`**
casts the current mouse ray and returns **the first game object** it hits.
That object is the unit or building the player clicked.

<a id="23-скролл-колеса"></a>
### 2.3. Mouse wheel

`GetGUIEventMouseWheelDelta()` - returns the delta of the last
scroll (positive = up, negative = down). By
default used for camera zoom:
- `SetCameraControlMouseWheelDistance(True)` — wheel changes
  distance.
- `SetCameraControlMouseWheelRotate(True)` - the wheel turns.

Only one of the modes is active. Profile settings via
`gProfile.*` - the player can change.

<a id="24-клавиатура"></a>
### 2.4. Keyboard

No direct `OnKeyDown` API call was found in the scripts. The engine handles
hotkeys by switching interface states such as `OnKey_F1` and
`OnKey_Ctrl_A`.

Consequently, hotkeys cannot be rebound through a script; they must be
changed in engine code or the `editor.exe` settings.

---

<a id="3-курсор"></a>
## 3. Cursor

| Function | What |
|---|---|
| `GUIGetCursorPos(var screenx, screeny)` | Current coordinates in screen pixels. |
| `GUISetCursorPos(screenx, screeny)` | Programmatically move the cursor. |
| `GUIShowCursor(show)` | Hide/show. |
| `SetClipCursor(val)` | Lock the cursor inside the window (for the selection frame). |
| `SetGUICursorByName('cursor_name')` | Change cursor visual. |

Cursor images - in `data/cursors/` (see.
[`../../../internals/data/layout.md`](../../../internals_en/data/layout.md)).
For example, when you hover over an enemy, the cursor changes to “sword” - this
change via `SetGUICursorByName('attack')`.

---

<a id="4-камера"></a>
## 4. Camera

<a id="41-управление"></a>
### 4.1. Management

| Function | What |
|---|---|
| `SetCameraMouseRotateFactor(val)` | Rotation sensitivity. |
| `SetCameraMouseDistanceSpeed(val)` | Zoom speed. |
| `SetCameraControlMouseWheelDistance(b)` | Wheel = zoom (default `True`). |
| `SetCameraControlMouseWheelRotate(b)` | Wheel = turn (default `False`). |
| `MoveCameraToPosition(x, z, time)` | Smooth movement to the point (`time` in g-sec). |
| `MoveCameraToUnitsListCenter(list)` | To the center of the list of units. |
| `MoveCameraToSelectedUnits()` | To selected ones (double-click-on-portrait in C&C). |

The player jumps to the group number (1–9) via `_control_MoveCameraTo*`
+ selection.

<a id="42-listener-точка-прослушки-звука"></a>
<a id="42-точка-прослушивания-звука"></a>
### 4.2. Listener (sound listening point)

The sound in C3 is emitted relative to the **listener** - invisible
the point to which the source of the player’s “ear” is attached:

- `GetSoundManagerListenerHandle()` — handle listener.
- `GetUseSoundManagerListenerAsCamera()` — `True` = listener
  tied to the camera (you hear what you're looking at).
- `GetUseSoundManagerListenerAsObject()` — listener is bound to
  object (for example, to the selected unit).
- `SetPosSoundManagerListenerAsObject(x, y, z)` - programmatically
  put listener to the point.

In a regular skirmish listener = camera. Therefore, the player hears what
next to the **camera**, and not to the selected unit or base.

---

<a id="5-звуки-и-fow--две-независимые-системы"></a>
<a id="5-звуки-и-туман-войны--две-независимые-системы"></a>
## 5. Sounds and FOW are two independent systems

This is a critical detail that is **often misunderstood**.

<a id="51-как-эмитируется-звук-юнита"></a>
<a id="51-как-создаётся-звук-юнита"></a>
### 5.1. How a unit's sound is emitted

When a unit performs an action (shot, step, fight, death), the script
calling `SndGetOrCreateSound(emittertag, 'units', owner)` - native
The function creates a sound emitter at the coordinates of the **owner** object.
Emitter parameters:

| Parameter | What |
|---|---|
| `SetSndSoundMaxRadius(maxradius, sound)` | Hearing radius in the world. |
| `SetSndSoundMinDist(value, sound)` / `MaxDist` | Full volume/zero volume distance (linear falloff). |
| `SetSndSoundMaxRadiuses(rmaxvolume, radius, sound)` | Radius 100% volume + total radius. |
| `SetSndSoundLoop(value, sound)` | Looped sound (background). |
| `SetSndSoundKillSndOutRad(value, sound)` | "Kill sound if listener is out of range." |
| `SetSndSoundConeOutsideVolume`, `InsideConeAngle`, `OutsideConeAngle` | Directional sound. |

The decision whether to play or not is based on **distance from the listener**.
**There are no FOW checks in these functions.**

<a id="52-что-это-значит"></a>
### 5.2. What does this mean

- **Unit in enemy FOW** (you can't see it) **audible** if
  it falls within the hearing radius (`SetSndSoundMaxRadius`).
- For example: an enemy musketeer shoots in a hidden forest - you
  **hear a shot**, but **do not see** either the unit or the flash.
- This gives the player **acoustic reconnaissance**: you can use sounds
  determine that the enemy unit has entered the flank, even before
  your scout will see it.

<a id="53-почему-так-сделано"></a>
### 5.3. Why is this done

Two technical solutions:

1. **One listener (camera)** in standard mode. FOW is considered
   per-player, but the sound is per-listener. If I checked the engine
   FOW for sound, you would have to filter each emitter by
   for the current player - expensive in terms of CPU.
2. **Realism trade-off.** Sound travels in reality
   regardless of whether you can see the source. Cossacks 3 is
   emulates.

See also [`vision_and_fow.md`](../world/combat/vision_and_fow.md)
about the structure of FOW.

---

<a id="6-alarm-уведомления"></a>
<a id="6-предупреждения"></a>
## 6. Alarm notifications

`_misc_DoAlarm(goHnd, trgHnd, event)` [^1] - main function for
"pay attention" signal. Fires when:

- The player's unit received an attack (`gc_gui_alarmevent_attack`).
- The player's building is captured (`gc_gui_alarmevent_capture`).
- And other events (`gc_gui_alarmevent_*`).

<a id="61-условия-срабатывания"></a>
### 6.1. Trigger conditions
```pascal
if (gPlayer[plIO].lastattacktime = 0) then  // no recent alarm
   if (trgPlHnd = plIOHnd or plHnd = plIOHnd) then  // event concerns the player
      if (not gSoundManager.IsObjInFrustum(handle)) then  // object is NOT in the camera frustum
         alarm fire
```
Key: **alarm is triggered only if the object is NOT in frustum**
cameras. That is, if a player physically looks at his base and
at this moment she is being attacked - there will be no notification because
the player sees it that way.

<a id="62-лимит-частоты"></a>
### 6.2. Frequency limit

After triggering, alarm is set
`gPlayer[plIO].lastattacktime = currenttime + gc_gui_underattackalarminterval`.
The following events are blocked until the interval expires. Typically
interval ~5 g-sec, so as not to receive “you are under attack” every tick
long battle.

<a id="63-что-игрок-видит-и-слышит"></a>
### 6.3. What the player sees and hears

| Effect | Source |
|---|---|
| The sound of a trumpet / barbarian shout | The script puts `gbool_gui_doalarm := True`, the GUI plays the sound. |
| Flashing frame around the edge of the screen | UI element, responds to `gbool_gui_doalarm`. |
| Arrow pointer to the event location | At coordinates `gfloat_gui_alarmx`, `gfloat_gui_alarmz`. |

The player can jump the camera to a location through a hotkey (double space
or Ctrl+W depending on the profile) - this causes
`MoveCameraToPosition(alarmx, alarmz, ...)`.

<a id="64-не-алармирует"></a>
<a id="64-когда-предупреждения-нет"></a>
### 6.4. Does not alarm

- **Attacks on non-owner.** `_misc_DoAlarm` checks
  `plIOHnd = trgPlHnd or plIOHnd = plHnd`. Teammate
  by default **will not receive an alarm** about an ally’s attack - for everyone
  your `plIO`.
- **Attacks of the priest** (he is in `bpriest` - heals, does not attack).
  The script skips the alarm call at `_misc_DoDamage` if the attacker
  - priest.

---

<a id="7-hotkey-конфиг"></a>
<a id="7-настройка-горячих-клавиш"></a>
## 7. Hotkey config

Hotkeys are defined in `data/game/var/hotkeys.cfg` -
parser format with records like:
```
[*] : struct.begin
   Key = Ctrl+A
   Action = select|allunits
   Repeat = True
struct.end
```
<a id="71-структура-записи"></a>
### 7.1. Record structure

| Field | What |
|---|---|
| `Key` | Main key or combination (`A`, `Ctrl+A`, `Ctrl+Alt+A`, `Shift+Z`, etc.). None means that the hotkey is not assigned by default. |
| `AlternativeKey` | Spare combination (optional). |
| `Action` | Description of the action in the format `<type>\|<parameter>`. |
| `Repeat` | If `True`, pressing again cycles through the options (e.g. `select\|allunits` → next highlighted unit of the same type). |
| `Up` | If `True`, the action is triggered by releasing the key, not by pressing it. |

<a id="72-шесть-типов-action"></a>
<a id="72-шесть-видов-действий-action"></a>
### 7.2. Six types `Action`

| Type | What does | Examples |
|---|---|---|
| `build` | Place a building from the build menu | `build\|%nat%cen` (Town Hall), `build\|%com%mil` (mill). `%nat%` is substituted for the current sid of the nation, `%com%` is a cluster (`eur` / `rus` / `tur` ...). |
| `unit` | Command to selected units | `unit\|attack`, `unit\|standground`, `unit\|nostandground`, `unit\|guard`, `unit\|cancelguard`, `unit\|attackpoint`, `unit\|enableattack`, `unit\|disableattack`, `unit\|stop`, `unit\|unloadall` |
| `squad` | Squad commands | `squad\|fill`, `squad\|disband`, `squad\|rank` (LINE), `squad\|column`, `squad\|square` |
| `select` | Selection by filter | `select\|allunits`, `select\|allships`, `select\|allbuildings`, `select\|allpeasants`, `select\|idlepeasants`, `select\|idlemines`, `select\|militaryunits`, `select\|unitsofsametype`, `select\|addunitsofsametype`, `select\|allunitsofsametype`, `select\|addallunitsofsametype` |
| `interface` | UI effect | `interface\|minimap` (collapse/expand minimap), `interface\|viewcollision` (debug - collision grid). |
| `event` | Trigger UI-state | `event\|eventmainmenu\|bcampaign` (open campaign), `event\|eventmainmenu\|brandommap`, etc. |

<a id="73-дефолтные-хоткеи-фрагмент"></a>
<a id="73-горячие-клавиши-по-умолчанию-фрагмент"></a>
### 7.3. Default hotkeys (fragment)

| Key | Action |
|---|---|
| `A` | `unit\|attack` (attack-move) |
| `S` | `unit\|standground` |
| `C` | `unit\|nostandground` (remove standground) |
| `G` | `unit\|guard` |
| `R` | `unit\|attackpoint` (artillery shooting at a point) |
| `F` | `squad\|fill` (replenish the squad) |
| `J` / `K` / `L` | `squad\|rank` / `squad\|column` / `squad\|square` |
| `Ctrl+S` | `unit\|stop` |
| `U` | `unit\|unloadall` (unload from transport / garrison) |
| `Z` | `select\|unitsofsametype` (Repeat - next) |
| `Shift+Z` | `select\|addunitsofsametype` |
| `Ctrl+A` | `select\|allunits` |
| `Ctrl+B` | `select\|allbuildings` |
| `Ctrl+M` | `select\|idlemines` |
| `Ctrl+P` or the backtick key | `select\|idlepeasants` |
| `Ctrl` plus the backtick key | `select\|allpeasants` |
| `Ctrl+Q` | `select\|allships` |
| `Ctrl+Alt+A` or `Ctrl+Shift+A` | `select\|militaryunits` |
| `Q` | `interface\|viewcollision` |
| `Alt+M` | `interface\|minimap` |

And a large set of `build|...` (one letter for each building) - `C` = Cen, `H` = House, `B` = Bar, `L` = Bla, `E` = Aca, `S` = Sta, `D` = Dip, `M` = Mar, `T` = Tow, `P` = Por, etc.

> **Duplicates** allowed: `S` found in `build|sta`, `unit|standground`
> and `event|eventmainmenu|bsettings`. Permission context - what
> GUI state is active (in-game / unit-selected / menu-open).

<a id="8-reserved-keys--нельзя-переназначить"></a>
<a id="8-клавиши-которые-нельзя-переназначить"></a>
## 8. Reserved keys - cannot be reassigned

The file `data/gui/menu.inc/hotkeysettings.inc` contains two lists
`forbiddenkeys` (cannot be set as a single key) and
`forbiddencombokeys` (prohibited combinations). These are the “engine engines”
hotkeys - which are not configured through the UI, because they are built into
game behavior.

<a id="81-одиночные-зарезервированные-клавиши"></a>
### 8.1. Single reserved keys

| Key | Reserved for |
|---|---|
| `LButton`, `RButton`, `MButton` | Mouse buttons - selection / order / drag camera. |
| `Left`, `Right`, `Up`, `Down` | Scroll the camera to the cardinal points. |
| `Space` | Jump to the last alarm (center the camera). |
| `Return` (Enter) | Open chat in multiplayer. |
| `Escape` | Close UI / cancel mode (build mode, attack-move). |
| `Shift`, `Ctrl`, `Alt` (+ their up-variants) | Modifiers - cannot be reassigned as single modifiers. |
| **`0`, `1`, …, `9`** | **Control groups — select a group.** |
| **`NUM0`–`NUM9`** | Double numbers on the numpad for control groups. |
| `F5`, `F7`, `F10` | Quick-save / quick-load / debug. |
| `PrintScreen0/1/2` | Screenshot (standard Windows behavior). |
| `Sub`, `Add`, `-`, `=` | Game speed (slow / fast). |
| `PGUP`, `PGDN`, `Home`, `Del`, `Back` | Log navigation / deletion. |
| `P` | Pause. |
| `[`, `]` | Scrolling alarms/notifications. |

<a id="82-зарезервированные-комбинации-control-groups--системные"></a>
<a id="82-зарезервированные-комбинации-для-групп-и-системы"></a>
### 8.2. Reserved combinations (control groups + system)

**Control groups (10 pieces, numbers 0–9):**

| Combination | What |
|---|---|
| **`Ctrl+0` … `Ctrl+9`** | **Assign** current selection to control group N. |
| **`Shift+0` … `Shift+9`** | **Add** current selection to control group N. |
| **`Alt+0` … `Alt+9`** | **Select** control group N. |
| **`Shift+Alt+0` … `Shift+Alt+9`** | Additional mode (probably: add group N to current selection). |

That is, in Cossacks 3 there are **10 control groups** (0–9), a standard set of controls.

**Camera and system:**

| Combination | Destination |
|---|---|
| `Alt+F4` | Close the application. |
| `Ctrl+S` | Quick save. |
| `Ctrl+Tab` | Switching player (spectator / replay). |
| `Ctrl+Home` | Center the camera on the player's starting point. |
| `Ctrl+PGUP` / `Ctrl+PGDN` | UI tab scrolling / player switching. |
| `Ctrl+W`, `Ctrl+F` | Camera quick-jump (probably to the City Center / to the selected one). |
| `Ctrl+Add` / `Ctrl+Sub` | Zoom in/out. |
| `Ctrl+Shift+P` | Debug mode. |
| `Ctrl+T` | Team chat (separate from regular chat by `Return`). |
| `Alt+Mul` (numpad *) | Change minimap mode. |
| `Shift+Alt+Mul` | Advanced minimap mode. |

<a id="83-rtti-классы-для-группы"></a>
<a id="83-классы-групп-найденные-в-rtti"></a>
### 8.3. RTTI classes for a group

Classes `TXGroup4` (one of ten?) and
`TXGroupSelectionViewer` - the last one draws **green highlights**
around units that are part of the active control group. Implementation
there is no control-group binding at the script level
(`SetGUIEventStateOnKeyDown` in `lib/*.script` is called only for
`'EventMultiplayerChat'`). This means processing numeric keys for
control groups is done **in native exe**, without calling scripts.

<a id="9-игровой-темп-и-пауза"></a>
## 9. Game tempo and pause

<a id="91-скорость-игры"></a>
### 9.1. Game speed

`_control_GetGameSpeedMode` / `_control_SetGameSpeedByMode`:

| Mode | Meaning |
|---|---:|
| `slow` (0) | 7 ticks/sec |
| `normal` (1) | 10 ticks/sec |
| `fast` (2) | **14 ticks/sec** (default in skirmish) |

Hotkey: `Ctrl+Add` (numpad +) / `Ctrl+Sub` (numpad −) - both
reserved (see §8.2).

<a id="92-пауза"></a>
### 9.2. Pause

Hotkey `P` - reserved (see §8.1). Limit: **4 pauses of 120
seconds** per game (mentioned in the old ref: “pause-limit
(4 × 120 seconds)").

<a id="10-доступ-скрипта-к-клавиатуре"></a>
## 10. Script access to keyboard

Native API for checking keys [^2]:

| Function | What |
|---|---|
| `IsKeyDown(vk: Integer): Boolean` | Whether the key is pressed according to the virtual-key code. |
| `IsKeyDownByName(sname: String): Boolean` | By name (`'Ctrl'`, `'Shift'`, `'A'`). |
| `KeyPressed(minvkcode: Integer): Integer` | The code of the last key pressed is `vkcode >= minvkcode`. |

In scripts **not called** at all - input processing is ongoing
entirely through GUI-FSM-callbacks (`SetGUIEventStateOn*`). Scripts
checking “whether Shift is pressed” is usually not necessary, because GUI-state
already takes modifiers into account.

---

<a id="11-открытые-вопросы"></a>
## 11. Open questions

1. **Exact semantics of `Shift+Alt+0..9`.** Forbidden list
   confirms that the combination is reserved, but what does it do -
   not read from the code.
2. **Sound + FOW for friendly objects.** If the unit is an ally
   outside of your FOW (but in his FOW), can you hear him? Hypothesis: yes,
   listener sees the whole world by distance.
3. ~~`gc_gui_underattackalarminterval` - exact value~~ ✅
   **Closed:** `= 135` (`dmscript.global`). Unit - internal
   counter `GetCurrentTime`, most likely **frames** →
   `135 / 32 ≈ 4.22 g-sec`. That is, alarm does not go off more than once per
   ~4 g-seconds.
4. **Double-click on a unit portrait** - does the camera jump? In code
   `MoveCameraToSelectedUnits` exists, but the trigger is not specified in
   scripts.

---

<a id="источники"></a>
## Sources

[^1]: `data/scripts/lib/misc.script` —
      `_misc_DoAlarm(goHnd, trgHnd, event)`. Uses
      `gSoundManager.IsObjInFrustum(handle)`
      for testing "out of camera view". Gate through
      `gPlayer[plIO].lastattacktime` and
      `gc_gui_underattackalarminterval`.

[^2]: Native API `IsKeyDown`, `IsKeyDownByName`, `KeyPressed` —
      see [`derived/dws_native_signatures.json`](../../../derived/dws_native_signatures.json).
      Hotkey config - `data/game/var/hotkeys.cfg`. Forbidden-keys —
      `data/gui/menu.inc/hotkeysettings.inc:1-100`.
