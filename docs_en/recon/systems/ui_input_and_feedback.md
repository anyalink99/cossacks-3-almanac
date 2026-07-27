<a id="recon-интерфейс-ввод-и-обратная-связь"></a>
<a id="управление-и-обратная-связь"></a>
# Controls and Player Feedback

[← How the game works](../README.md)

How selection, camera controls, hotkeys, sound, and warnings work. The main
sections describe the result for the player; exact engine functions are kept
in technical tables and source notes.

> **Related documents:**
> [Vision and Fog of War](../world/combat/vision_and_fow.md)
> — fog of war and overview; [Unit Orders](../world/combat/unit_commands.md)
> - what orders the unit understands.

<a id="кратко"></a>
## Key points

- A single click selects the object under the cursor; a selection box
  updates the selected set while the mouse button is held.
- **Sound and fog of war are independent.** Audibility depends on distance
  from the listener—the camera or an object—not on visibility. A hidden
  enemy unit can still be heard.
- **Warnings** such as “under attack” or “being captured” appear only
  when the event is **outside the camera frustum**.
- The same warning sounds no more than about once every 4.2 game seconds.

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
default, it controls camera zoom:
- `SetCameraControlMouseWheelDistance(True)` — wheel changes
  distance.
- `SetCameraControlMouseWheelRotate(True)` - the wheel turns.

Only one mode is active at a time. The player can change it through profile
settings stored in `gProfile.*`.

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

Cursor images are stored in `data/cursors/`; see
[Cossacks 3 `data/` layout](../../../internals_en/data/layout.md).
For example, hovering over an enemy changes the cursor to a sword through
`SetGUICursorByName('attack')`.

---

<a id="4-камера"></a>
## 4. Camera

<a id="41-управление"></a>
### 4.1. Controls

| Function | What |
|---|---|
| `SetCameraMouseRotateFactor(val)` | Rotation sensitivity. |
| `SetCameraMouseDistanceSpeed(val)` | Zoom speed. |
| `SetCameraControlMouseWheelDistance(b)` | Wheel = zoom (default `True`). |
| `SetCameraControlMouseWheelRotate(b)` | Wheel = turn (default `False`). |
| `MoveCameraToPosition(x, z, time)` | Move smoothly to a point (`time` is in game seconds). |
| `MoveCameraToUnitsListCenter(list)` | Move to the center of a unit list. |
| `MoveCameraToSelectedUnits()` | Move to the selected units. |

Jumping to a numbered control group (1–9) combines selection with one of
the `_control_MoveCameraTo*` functions.

<a id="42-listener-точка-прослушки-звука"></a>
<a id="42-точка-прослушивания-звука"></a>
### 4.2. Listener (the point from which sound is heard)

Cossacks 3 positions sound relative to an invisible **listener**, which
acts as the player's point of hearing:

- `GetSoundManagerListenerHandle()` — returns the listener handle.
- `GetUseSoundManagerListenerAsCamera()` — when `True`, the listener is
  attached to the camera, so the player hears the area currently on screen.
- `GetUseSoundManagerListenerAsObject()` — reports whether the listener is
  attached to an object, such as the selected unit.
- `SetPosSoundManagerListenerAsObject(x, y, z)` — moves the listener to
  specified world coordinates.

In a normal skirmish, the listener follows the camera. The player therefore
hears activity near the **camera**, not activity near the selected unit or
the player's base.

---

<a id="5-звуки-и-fow--две-независимые-системы"></a>
<a id="5-звуки-и-туман-войны--две-независимые-системы"></a>
## 5. Sound and fog of war are independent systems

This is a critical detail that is **often misunderstood**.

<a id="51-как-эмитируется-звук-юнита"></a>
<a id="51-как-создаётся-звук-юнита"></a>
### 5.1. How unit sounds are emitted

When a unit fires, moves, fights, or dies, the script calls
`SndGetOrCreateSound(emittertag, 'units', owner)`. This native function
creates a sound emitter at the coordinates of the **owner** object.
The following functions configure that emitter:

| Function | What it controls |
|---|---|
| `SetSndSoundMaxRadius(maxradius, sound)` | Maximum audible radius in the game world. |
| `SetSndSoundMinDist(value, sound)` / `MaxDist` | Full-volume and zero-volume distances for linear falloff. |
| `SetSndSoundMaxRadiuses(rmaxvolume, radius, sound)` | Full-volume radius and total audible radius. |
| `SetSndSoundLoop(value, sound)` | Whether the sound loops. |
| `SetSndSoundKillSndOutRad(value, sound)` | Whether playback stops when the listener leaves the audible radius. |
| `SetSndSoundConeOutsideVolume`, `InsideConeAngle`, `OutsideConeAngle` | Directional sound. |

Playback depends on the **distance from the listener**.
**There are no FOW checks in these functions.**

<a id="52-что-это-значит"></a>
### 5.2. What this means in play

- A unit hidden by the enemy's fog of war can still be **heard** when it
  lies within the audible radius set by `SetSndSoundMaxRadius`.
- For example, if an enemy Musketeer fires in an unexplored forest, the
  player can **hear the shot** without seeing the unit or its muzzle flash.
- Sound can therefore reveal nearby enemy activity before a Scout provides
  vision.

<a id="53-почему-так-сделано"></a>
### 5.3. Why the systems are separate

There are two practical reasons:

1. **A single listener follows the camera** in the standard mode. Fog of
   war is calculated per player, whereas sound is calculated for a listener.
   Filtering every sound emitter through the current player's visibility
   would add work to the audio path.
2. **Sound does not require line of sight.** The design lets players hear
   nearby activity even when they cannot see its source.

See also [Vision and Fog of War](../world/combat/vision_and_fow.md)
about the structure of FOW.

---

<a id="6-alarm-уведомления"></a>
<a id="6-предупреждения"></a>
## 6. Alarm notifications

An attention warning [^1] is triggered when:

- the player's unit is attacked;
- the player's building is being captured;
- another event with a dedicated warning occurs.

<a id="61-условия-срабатывания"></a>
### 6.1. Trigger conditions
The game checks that the previous warning has expired, that the event concerns
the current player, and that the object is outside the camera view. If the
player is already looking at a base when it comes under attack, no additional
warning is shown.

<a id="62-лимит-частоты"></a>
### 6.2. Frequency limit

Further warnings are suppressed for roughly 4.2 game seconds, preventing a
long battle from producing an alert every tick.

<a id="63-что-игрок-видит-и-слышит"></a>
### 6.3. What the player sees and hears

| What the player receives | Presentation |
|---|---|
| Audio warning | A trumpet or battle cry. |
| Visual warning | A flashing frame around the screen edge. |
| Direction | An arrow pointing toward the event. |

The player can jump the camera to the event with a hotkey (double Space or
Ctrl+W, depending on the profile).

<a id="64-не-алармирует"></a>
<a id="64-когда-предупреждения-нет"></a>
### 6.4. When no warning is shown

- **An ally is attacked.** `_misc_DoAlarm` checks
  `plIOHnd = trgPlHnd or plIOHnd = plHnd`. Each client has its own `plIO`,
  so a teammate does **not** receive the local player's warning.
- **A Priest performs an action.** Priests have the `bpriest` flag and heal
  rather than attack. `_misc_DoDamage` skips the warning call when the
  acting unit is a Priest.

---

<a id="7-hotkey-конфиг"></a>
<a id="7-настройка-горячих-клавиш"></a>
## 7. Hotkey config

Hotkeys are stored in a separate profile. Each record connects a key to an
action and can also specify an alternative combination, activation on key
release, and repeated target cycling. The literal record format is shown in
[Sources](#sources).
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

| Type | What it does | Examples |
|---|---|---|
| `build` | Places a building from the construction menu | `build\|%nat%cen` (Town Hall), `build\|%com%mil` (Mill). `%nat%` is replaced with the current nation ID; `%com%` is replaced with a nation group such as `eur`, `rus`, or `tur`. |
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

There is also a large set of `build|...` actions, usually with one letter
per building: `C` = Town Hall (`cen`), `H` = Housing (`hou`),
`B` = Barracks, 17th century (`bar`), `L` = Blacksmith (`bla`),
`E` = Academy (`aca`),
`S` = Stable (`sta`), `D` = Diplomatic Center (`dip`), `M` = Market
(`mar`), `T` = Tower (`tow`), and `P` = Shipyard (`por`).

> **Duplicate bindings are allowed.** For example, `S` appears in
> `build|sta`, `unit|standground`, and `event|eventmainmenu|bsettings`.
> The active GUI context—construction menu, selected unit, or main
> menu—determines which action runs.

<a id="8-reserved-keys--нельзя-переназначить"></a>
<a id="8-клавиши-которые-нельзя-переназначить"></a>
## 8. Reserved keys - cannot be reassigned

The file `data/gui/menu.inc/hotkeysettings.inc` contains two lists
`forbiddenkeys` (cannot be set as a single key) and
`forbiddencombokeys` (prohibited combinations). These are engine-level
hotkeys that cannot be configured through the UI because their behavior is
built into the game.

<a id="81-одиночные-зарезервированные-клавиши"></a>
### 8.1. Single reserved keys

| Key | Reserved for |
|---|---|
| `LButton`, `RButton`, `MButton` | Mouse buttons - selection / order / drag camera. |
| `Left`, `Right`, `Up`, `Down` | Move the camera in the four cardinal directions. |
| `Space` | Jump to the last alarm (center the camera). |
| `Return` (Enter) | Open chat in multiplayer. |
| `Escape` | Close UI / cancel mode (build mode, attack-move). |
| `Shift`, `Ctrl`, `Alt` (and their key-up variants) | Modifier keys; they cannot be assigned as standalone actions. |
| **`0`, `1`, …, `9`** | **Control groups — select a group.** |
| **`NUM0`–`NUM9`** | Double numbers on the numpad for control groups. |
| `F5`, `F7`, `F10` | Quick-save / quick-load / debug. |
| `PrintScreen0/1/2` | Take a screenshot. |
| `Sub`, `Add`, `-`, `=` | Game speed (slow / fast). |
| `PGUP`, `PGDN`, `Home`, `Del`, `Back` | Navigate or clear interface logs. |
| `P` | Pause. |
| `[`, `]` | Scrolling alarms/notifications. |

<a id="82-зарезервированные-комбинации-control-groups--системные"></a>
<a id="82-зарезервированные-комбинации-для-групп-и-системы"></a>
### 8.2. Reserved combinations (control groups + system)

**Control groups (ten groups, numbered 0–9):**

| Combination | What |
|---|---|
| **`Ctrl+0` … `Ctrl+9`** | **Assign** current selection to control group N. |
| **`Shift+0` … `Shift+9`** | **Add** current selection to control group N. |
| **`Alt+0` … `Alt+9`** | **Select** control group N. |
| **`Shift+Alt+0` … `Shift+Alt+9`** | Additional mode (probably: add group N to current selection). |

Cossacks 3 therefore provides **ten control groups**, numbered 0–9.

**Camera and system:**

| Combination | Action |
|---|---|
| `Alt+F4` | Close the application. |
| `Ctrl+S` | Quick save. |
| `Ctrl+Tab` | Switching player (spectator / replay). |
| `Ctrl+Home` | Center the camera on the player's starting point. |
| `Ctrl+PGUP` / `Ctrl+PGDN` | Cycle interface tabs or switch players. |
| `Ctrl+W`, `Ctrl+F` | Quick camera jump, probably to the Town Hall or the selected object. |
| `Ctrl+Add` / `Ctrl+Sub` | Zoom in/out. |
| `Ctrl+Shift+P` | Debug mode. |
| `Ctrl+T` | Team chat (separate from regular chat by `Return`). |
| `Alt+Mul` (numpad *) | Change minimap mode. |
| `Shift+Alt+Mul` | Advanced minimap mode. |

<a id="83-rtti-классы-для-группы"></a>
<a id="83-классы-групп-найденные-в-rtti"></a>
### 8.3. RTTI classes for a group

The RTTI contains `TXGroup4`—apparently one of the ten groups—and
`TXGroupSelectionViewer`, which draws **green highlights** around units
in the active control group. No control-group key binding exists at the
script level: `SetGUIEventStateOnKeyDown` in `lib/*.script` is called only
for `'EventMultiplayerChat'`. Numeric control-group keys are therefore
handled **by the native executable**, without a script callback.

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

The reserved hotkeys are `Ctrl+Add` (numpad +) and `Ctrl+Sub`
(numpad −); see §8.2.

<a id="92-пауза"></a>
### 9.2. Pause

The reserved hotkey is `P` (see §8.1). Each player may pause at most
**four times for 120 seconds** per match.

<a id="10-доступ-скрипта-к-клавиатуре"></a>
## 10. Script access to keyboard

Native API for checking keys [^2]:

| Function | What |
|---|---|
| `IsKeyDown(vk: Integer): Boolean` | Whether the key is pressed according to the virtual-key code. |
| `IsKeyDownByName(sname: String): Boolean` | By name (`'Ctrl'`, `'Shift'`, `'A'`). |
| `KeyPressed(minvkcode: Integer): Integer` | Code of the last pressed key whose `vkcode >= minvkcode`. |

These functions are **not called by the inspected scripts**. Input is
instead processed through GUI state-machine callbacks
(`SetGUIEventStateOn*`). Scripts normally do not need to ask whether
Shift is held because the active GUI state already includes modifiers.

---

<a id="11-открытые-вопросы"></a>
## 11. Open questions

1. **Exact semantics of `Shift+Alt+0..9`.** The forbidden-key list
   confirms that the combinations are reserved, but their behavior is
   not visible in the scripts.
2. **Sound + FOW for friendly objects.** If the unit is an ally
   outside of your FOW (but in his FOW), can you hear him? Hypothesis: yes,
   listener sees the whole world by distance.
3. **Exact warning delay.** The threshold is 135 internal units, which gives
   about 4.22 game seconds when converted at 32 frames per game second.
   Verify in play that the warning counter uses that exact time scale.
4. **Double-click on a unit portrait** - does the camera jump? In code
   `MoveCameraToSelectedUnits` exists, but the trigger is not specified in
   scripts.

---

<a id="источники"></a>
## Sources

[^1]: `data/scripts/lib/misc.script` —
      `_misc_DoAlarm(goHnd, trgHnd, event)`. Uses
      `gSoundManager.IsObjInFrustum(handle)`
      to test whether the object is outside the camera view. Frequency is
      limited through
      `gPlayer[plIO].lastattacktime` and
      `gc_gui_underattackalarminterval`.

[^2]: Native API `IsKeyDown`, `IsKeyDownByName`, `KeyPressed` —
      see [`derived/dws_native_signatures.json`](../../../derived/dws_native_signatures.json).
      Hotkey config - `data/game/var/hotkeys.cfg`. Forbidden-keys —
      `data/gui/menu.inc/hotkeysettings.inc:1-100`.

      Literal record example:

      ```text
      [*] : struct.begin
         Key = Ctrl+A
         Action = select|allunits
         Repeat = True
      struct.end
      ```
