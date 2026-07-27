<a id="recon-обзор-и-туман-войны"></a>
<a id="обзор-и-туман-войны"></a>
# Vision and Fog of War

[← How the game works](../../README.md)

How each unit's vision radius is calculated, when fog of war is disabled,
and how allied vision is shared. Script references are collected in
[Sources](#sources).

<a id="коротко"></a>
## TL;DR

- A unit's **vision radius** is `20 + 4 × vision`, where `vision` is an
  internal field from `data.json` [^1].
- Only living (`bdead = False`), visible, and completed
  (`bbuilt = True`) objects provide vision.
- Fog of war is controlled by native `SetFOWEnable(b)` and is
  **disabled** if the player has a Balloon (`bballoon`), the lobby
  option “with Balloon” (`balloon = with`) is active, or
  the game ended in victory/defeat [^2].
- Allied vision is shared automatically: every teammate is added through
  `AddFOWPlayers` [^2].
- The engine calculates line of sight. The script only supplies
  `_unit_GetVision(handle) → radius` through `SetFOWDovFunc`; the rest
  is hidden in native code.
- Scout shells (`fogreveal`-property) for a short time
  open the area around the landing point - for example, rockets
  balloon, flight lantern.

---

<a id="1-радиус-обзора-каждого-юнита"></a>
## 1. Vision Radius of Each Unit

The source is `_unit_GetVision`, which the engine calls
for each visible object on the map [^1]. There are two constants inside
(`cBaseVal = 20`, `cModVal = 4`) and one formula: if the object
is rendered, alive, and completed,
`res := floor(cBaseVal + cModVal × objprop.vision)`; otherwise - `res := 0`.

Formula: **`radius = 20 + 4 × vision`**, in conventional units
engine (≈ pixels / `pixels_to_tile`).

| Vision (`vision`, `data.json` field) | Typical objects |
|---:|---|
| `0` | Most are simple infantrymen and peasants. |
| `2` | Cavalry, horse artillery. |
| `3` | Rifle infantry 18th century. (musketeers, grenadiers). |

Numerical examples:

| Unit | `vision` | Radius, tiles |
|---|---:|---:|
| Peasant | 0 | 20 |
| Pikeman, 17th century | 0 | 20 |
| Dragoon | 2 | 28 |
| Musketeer, 18th century | 3 | 32 |
| Tower | 3 | 32 |

**Unit - tiles directly.** Unlike weapon radii (where
the number is stored in pixels and divided by `gc_pixels_to_tile = 53.3333`),
The fog-of-war radius is returned directly in tiles: `vision = 0`
provides 20 tiles, while `vision = 3` provides 32. This matches the
Tower (`vision = 3`, radius 32), whose vision exceeds its own
26.25-tile target-search radius (`searchradius`; see
[`towers.md` §2.2](towers.md)).

<a id="2-условия-выдачи-обзора"></a>
## 2. Conditions for Providing Vision

An object provides vision only when all three conditions are true:

1. `GetGameObjectVisibleByHandle(handle) = True` - game object
   physically rendered.
2. `not bdead` - not dead.
3. `bbuilt = True` - the building has been completed (this is critical for buildings:
   the construction site does not show up on the map).

If any condition fails, `res := 0`. A Tower under construction therefore
**does not reveal its surroundings**. Once completed, its `vision = 3`
reveals a 32-tile radius.

<a id="3-снаряды-разведчики-fogreveal"></a>
## 3. Vision-Revealing Projectiles (`fogreveal`)

A special case is shells with the tag `fogreveal` (property
`StringPropertyTag = gc_properties_stringtag_fogreveal`) [^3].
For them, instead of the standard calculation, `floor(TProj(pproj).dx)` is returned
- that is, `dx` of the projectile (trajectory length / radius of expansion).
Used for:

- **Balloon projectiles** reveal the area around their landing point.
- **Flares and flying lanterns** use the same mechanism in campaigns.

The effect is temporary (while the projectile exists) and is applied
on top of the regular fog-of-war map.
<a id="4-туман-войны-включение-и-отключение"></a>
## 4. Enabling and Disabling Fog of War

The controlling procedure is `_player_UpdateFOW` in
`lib/player.script` [^2]. It performs four steps:

1. Reads the base value `bFOW := True`, then resets to
   `False` if the player has a balloon, lobby option
   “with Balloon” (`balloon = with`) is active or the match has ended
   (`victorystate ≠ none`); the editor can also turn off FOW
   via `gbool_editor_fogofwar = False`.
2. Clears the list of observers (`ClearFOWPlayers`).
3. If `bFOW = True` - adds the player himself to FOW via
   `AddFOWPlayers(GetPlayerHandleByIndex(plInd))`, then
   goes through `gc_MaxPlayerCount` and **adds all allies
   by command** (with an exception for neutrals in the campaign).
4. Registers the vision-calculation callback via
   `SetFOWDovFunc('_unit_GetVision')` and activates the fog through
   `SetFOWEnable(bFOW)`.

<a id="41-когда-fow-отключён-полностью"></a>
<a id="41-когда-туман-войны-отключён-полностью"></a>
### 4.1. When fog of war is completely disabled

| Reason | Effect |
|---|---|
| The player built a hot air balloon (`bballoon = True`) | Sees the entire map until the end of the game. |
| Lobby option “with Balloon” (`balloon = with`) | All players start with full-map vision. |
| Player won/lost (`victorystate ≠ none`) | After the game ends, the entire map is visible. |
| Map editor has disabled FOW (`gbool_editor_fogofwar = False`) | Only in the editor. |

<a id="42-союзный-обзор"></a>
### 4.2. Shared allied vision

Each teammate is added through `AddFOWPlayers`.
**Allies automatically share vision.** No separate “share vision”
button is required; this behavior is built in and cannot be disabled.

There is one campaign exception: the main hero player's vision
(`plInd = 0`) is not shared with **neutral** characters
(`bneutral = True`), so neutral NPCs do not reveal the player's position.

<a id="5-связь-с-другими-системами"></a>
## 5. Interaction with Other Systems

<a id="50-звук"></a>
### 5.0. Sound

The sound system is **not tied to fog of war**. Emitters
(`SndGetOrCreateSound`) only check the distance from the listener
(camera or object). An enemy hidden by fog of war can therefore still
be **heard** when within the camera's hearing radius. See
[`../../systems/ui_input_and_feedback.md` §5](../../systems/ui_input_and_feedback.md).

<a id="51-целеуказание"></a>
### 5.1. Target acquisition

Vision and targeting are **separate** mechanics:
- Vision uses the radius `20 + 4 × vision` (see §1).
- Target acquisition (`_unit_SearchEnemy*`) uses weapon radii:
  `weapon.radiusmin`, `weapon.radiusmax`. See
  [`target_selection.md`](target_selection.md).

A unit can therefore **see** farther than it can **shoot**. A Tower with
`vision = 3` (32 tiles) sees its surroundings, but its
`weapon.radiusmax` is shorter: the enemy is known but still out of range.

<a id="52-поиск-пути"></a>
### 5.2. Pathfinding

Vision **does not affect** pathfinding. Routes use the full obstacle map,
not only the visible area.
If the enemy builds a trap (wall) while you are moving, the unit
will go around it, even if you don’t “see” it.

<a id="53-компьютерный-игрок"></a>
### 5.3. Computer player

The computer player also **sees only through fog of war**. A raid along
an unseen route can therefore work: if your troops do not reveal
themselves, the AI does not react. See
[`../systems/ai_behavior.md`](../../systems/ai_behavior.md).

<a id="6-открытые-эмпирические-вопросы"></a>
<a id="6-что-ещё-требует-проверки"></a>
## 6. Questions Requiring Further Testing

1. **Exact conversion of `radius` to tiles.** The formula may use a
   dedicated fog-of-war unit. Measure the visible distance for a unit
   with known `vision`.
2. **Fog-of-war update rate.** The script registers
   `SetFOWDovFunc`, but native code controls updates. Fast cavalry can
   reveal whether vision trails a moving unit by one or more frames.
3. **Fog-of-war memory.** Explored terrain remains under grey fog, but
   it is unclear which objects are remembered. The working hypothesis
   is that terrain persists while units and buildings require current vision.

<a id="источники"></a>
## Sources

[^1]: `data/scripts/lib/unit.script:11563` - procedure
      `_unit_GetVision`. Returns radius = 20 + 4 × `vision` for
      living visible completed objects. Registered as
      DOV-callback via `SetFOWDovFunc('_unit_GetVision')`.

[^2]: `data/scripts/lib/player.script:455-477` - procedure
      `_player_UpdateFOW`. FOW shutdown conditions (balloon/
      lobby option / victory state / editor) and automatic
      login to the team via `AddFOWPlayers`.

[^3]: `data/scripts/lib/unit.script:11572` - handler
      `gc_properties_stringtag_fogreveal` for projectiles: returns
      `floor(TProj(pproj).dx)` as the radius of temporary “opening”
      FOW.
