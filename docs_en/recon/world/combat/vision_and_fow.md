<a id="recon-обзор-и-туман-войны"></a>
<a id="обзор-и-туман-войны"></a>
# Vision and Fog of War

[← How the game works](../../README.md)

Deep analysis: how is the viewing radius of each unit calculated, how
How the fog of war works, in what situations it is disabled, how it works
general overview of the allies. All links to the code are in
[Sources](#sources).

## TL;DR

- **View radius** of one unit - `20 + 4 × vision`, where `vision`
  — field from `data.json` (values 0..8) [^1].
- Review depends on condition: live only (`bdead = False`) and
  completed (`bbuilt = True`) objects provide visibility; invisible
  (`GetGameObjectVisible = False`) - no.
- Fog of War is enabled/disabled via native
  `SetFOWEnable(b)`; **disabled** if player has air
  ball (`bballoon`), the lobby option “balloon = with” is activated, or
  the game ended in victory/defeat [^2].
- Allied vision is automatically searched: each observer player
  added to FOW via `AddFOWPlayers` for all allies by
  team [^2].
- LOS calculation is done by the engine, not by the script. Script only
  supplies function `_unit_GetVision(handle) → radius` via
  `SetFOWDovFunc`; everything else is hidden in the native.
- Scout shells (`fogreveal`-property) for a short time
  open the area around the landing point - for example, rockets
  balloon, flight lantern.

---

<a id="1-радиус-обзора-каждого-юнита"></a>
## 1. View radius of each unit

Source - procedure `_unit_GetVision`, which the engine calls
for each visible object on the map [^1]. There are two constants inside
(`cBaseVal = 20`, `cModVal = 4`) and one formula: if the object
physically rendered, not dead and completed,
`res := floor(cBaseVal + cModVal × objprop.vision)`; otherwise - `res := 0`.

Formula: **`radius = 20 + 4 × vision`**, in conventional units
engine (≈ pixels / `pixels_to_tile`).

| `vision` (data.json field) | Who |
|---:|---|
| `0` | Most are simple infantrymen and peasants. |
| `2` | Cavalry, horse artillery. |
| `3` | Rifle infantry 18th century. (musketeers, grenadiers). |
| `8` | Towers, observers on the towers. |

Numerical examples:

| Unit | `vision` | Radius (units) |
|---|---:|---:|
| Peasant | 0 | 20 |
| Pikeman 17th century | 0 | 20 |
| Dragoon | 2 | 28 |
| Musketeer 18th century | 3 | 32 |
| Tower | 8 | 52 |

**Unit - tiles directly.** Unlike weapon radii (where
the number is stored in pixels and divided by `gc_pixels_to_tile = 53.3333`),
The FOW radius returns in tiles. That is, `vision = 0` gives
20 review tiles, `vision = 8` - 52 tiles. This is confirmed
visually and consistent with what the tower (`vision = 3`, radius 32)
opens up a noticeably larger area than her own
`searchradius = 26.25` tile (see.
[`towers.md` §2.2](towers.md)).

<a id="2-условия-выдачи-обзора"></a>
## 2. Conditions for issuing a review

The object gives an overview only if all conditions are true:

1. `GetGameObjectVisibleByHandle(handle) = True` - game object
   physically rendered.
2. `not bdead` - not dead.
3. `bbuilt = True` - the building has been completed (this is critical for buildings:
   the construction site does not show up on the map).

If any condition is violated - `res := 0`. That is, the construction of a tower
**does not show to district** until completion. But as soon as the tower
completed and the defense built inside - 8-vision reveals it
large space.

<a id="3-снаряды-разведчики-fogreveal"></a>
## 3. Scout shells (`fogreveal`)

A special case is shells with the tag `fogreveal` (property
`StringPropertyTag = gc_properties_stringtag_fogreveal`) [^3].
For them, instead of the standard calculation, `floor(TProj(pproj).dx)` is returned
- that is, `dx` of the projectile (trajectory length / radius of expansion).
Used for:

- **Balloon Shooting** - opens up the area around the landing.
- **Flares/flight lights** in the campaign.

The effect is temporary (while the projectile exists) and is applied
on top of a regular FOW card.
<a id="4-туман-войны-включение-и-отключение"></a>
## 4. Fog of war: enable and disable

Control point - procedure `_player_UpdateFOW` in
`lib/player.script` [^2]. It follows four steps:

1. Reads the base value `bFOW := True`, then resets to
   `False` if the player has a balloon, lobby option
   `balloon = with` is active or the batch has ended
   (`victorystate ≠ none`); the editor can also turn off FOW
   via `gbool_editor_fogofwar = False`.
2. Clears the list of observers (`ClearFOWPlayers`).
3. If `bFOW = True` - adds the player himself to FOW via
   `AddFOWPlayers(GetPlayerHandleByIndex(plInd))`, then
   goes through `gc_MaxPlayerCount` and **adds all allies
   by command** (with an exception for neutrals in the campaign).
4. Registers the review calculation callback via
   `SetFOWDovFunc('_unit_GetVision')` and activates the fog through
   `SetFOWEnable(bFOW)`.

<a id="41-когда-fow-отключён-полностью"></a>
### 4.1. When FOW is completely disabled

| Reason | Effect |
|---|---|
| The player built a hot air balloon (`bballoon = True`) | Sees the entire map until the end of the game. |
| Lobby option `balloon = with` | All players start with everyone's view. |
| Player won/lost (`victorystate ≠ none`) | After the game ends, the entire map is visible. |
| Map editor has disabled FOW (`gbool_editor_fogofwar = False`) | Only in the editor. |

<a id="42-союзный-обзор"></a>
### 4.2. Union review

Each team member is added to FOW via `AddFOWPlayers`.
**Allies automatically shares a review on command**.
No separate “share vision” button is needed - this is the behavior
built in and cannot be disabled.

Exception in script - for scripts (`plInd = 0`, main
hero player): his review is not shared with **neutrals**
characters (`bneutral = True`). This is done so that NPC peasants
campaigns did not “give away” the player’s position.

<a id="5-связь-с-другими-системами"></a>
## 5. Communication with other systems

<a id="50-звук"></a>
### 5.0. Sound

The sound system is **not tied to FOW**. Emitters
(`SndGetOrCreateSound`) only check the distance from the listener
(camera or object). This means: enemy unit in enemy FOW
(you can't see him) **audible** if he's within earshot
cameras. Full analysis - in
[`../../systems/ui_input_and_feedback.md` §5](../../systems/ui_input_and_feedback.md).

<a id="51-целеуказание"></a>
### 5.1. Target designation

Overview and targeting - **different** mechanics:
- The overview works with the radius `20 + 4 × vision` (see §1).
- Target designation (`_unit_SearchEnemy*`) works with weapon radius -
  `weapon.radiusmin`, `weapon.radiusmax`. See
  [`target_selection.md`](target_selection.md).

That is, the unit can **see** further than it can **shoot**. Tower with
`vision = 8` (radius = 52) sees the surroundings, but `weapon.radiusmax`
less shot - she “knows” that the enemy is there, but does not reach him.

### 5.2. Pathfinding

The overview **does not affect** the path building. Pathfinding works by
full map (sees obstacles everywhere, not only in the viewing area).
If the enemy builds a trap (wall) while you are moving, the unit
will go around it, even if you don’t “see” it.

### 5.3. A.I.

The enemy AI also **only sees through FOW**. That is, a raid on
Hidden paths in the back work - if you don’t shine your troops,
AI doesn't react. Details - in
[`../systems/ai_behavior.md`](../../systems/ai_behavior.md).

<a id="6-открытые-эмпирические-вопросы"></a>
## 6. Open empirical questions

1. **Exact conversion of `radius` to tiles.** The formula returns
   value in unclear units (probably own FOW unit
   engine). You need to measure: put a unit with the known `vision`,
   measure the visible distance with a ruler through the screenshot.
2. **FOW update rate.** FOW is updated every frame or
   every N ms? The script only installs the function via
   `SetFOWDovFunc`; update is native. Need to measure through
fast moving cavalry: how many frames is FOW behind
   unit positions.
3. **Memory of FOW.** Once explored, areas of the map remain
   visible (like "grey fog"), but we are not sure whether
   there are objects. Hypothesis: only terrain, units and
   building views only in real FOW. Measure it.

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
