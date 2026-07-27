<a id="recon-обзор-и-туман-войны"></a>
<a id="обзор-и-туман-войны"></a>
# Vision and Fog of War

[← How the game works](../../README.md)

Vision radius determines how much of the map each unit or building reveals.
It is separate from weapon range and does not limit pathfinding: this system
is primarily about scouting.

<a id="коротко"></a>
## At a Glance

- The base vision value is 20 and grows by four for each point of the vision
  rating [^1].
- Only living, visible, and fully completed objects provide vision.
- A **Balloon** reveals the entire map to its owner. The same happens after
  the match ends and when the “with Balloon” lobby option is enabled [^2].
- Teammates share vision automatically.
- Some projectiles reveal an area around their point of impact temporarily.
- Sound and pathfinding are not restricted by fog of war.

<a id="1-радиус-обзора-каждого-юнита"></a>
<a id="1-как-считается-радиус-обзора"></a>
## 1. Calculating Vision Radius

The formula is **20 + 4 × vision rating**. Each object type has its own
rating, usually between 0 and 8 [^1].

| Vision rating | Typical objects |
|---:|---|
| 0 | Most basic infantry and peasants. |
| 2 | Cavalry and horse artillery. |
| 3 | 18th-century firearm infantry: Musketeers and Grenadiers. |

| Unit or building | Vision rating | Nominal radius |
|---|---:|---:|
| Peasant | 0 | 20 |
| 17th-century Pikeman | 0 | 20 |
| Dragoon | 2 | 28 |
| 18th-century Musketeer | 3 | 32 |
| Tower | 3 | 32 |

Unlike weapon range, this value is passed directly to the fog-of-war system
rather than converted from pixels. A **Tower** receives a nominal vision
radius of 32 and a separate target-search radius of 26.25 cells; see
[How Towers Work](towers.md). These values come from different
coordinate systems and should not be compared directly.

<a id="2-условия-выдачи-обзора"></a>
<a id="2-когда-объект-даёт-обзор"></a>
## 2. When an Object Provides Vision

An object reveals the map only when all three conditions hold:

1. it exists visibly in the game world and is being rendered;
2. it is alive;
3. if it is a building, construction is complete.

If any condition fails, its vision radius becomes zero. A **Tower** under
construction reveals nothing; immediately after completion, it begins
providing its full nominal radius of 32.

<a id="3-снаряды-разведчики-fogreveal"></a>
<a id="3-снаряды-открывающие-местность"></a>
## 3. Vision-Revealing Projectiles

Some projectiles reveal the area around themselves while in flight [^3].
The mechanism is used, for example, by:

- **Balloon** projectiles, which reveal the impact area;
- signal rockets and flying lanterns in campaigns.

The effect is temporary and overlays the ordinary fog-of-war map.

<a id="4-туман-войны-включение-и-отключение"></a>
<a id="4-когда-открывается-вся-карта"></a>
## 4. When the Entire Map Is Revealed

Normally, a player sees only explored terrain and the current vision areas
of their objects. Fog of war is disabled in four cases [^2].

| Cause | Effect |
|---|---|
| The player builds a **Balloon** | The entire map remains visible until the match ends. |
| The “with Balloon” lobby option is selected | Every player starts with full-map vision. |
| The player wins or loses | The entire map is revealed after the result. |
| The scenario author disables fog of war | The map is open in the editor or scenario. |

<a id="42-союзный-обзор"></a>
<a id="41-союзный-обзор"></a>
### 4.1. Shared Allied Vision

**Teammates share vision automatically.** No separate button is needed, and
ordinary match settings cannot disable this behavior.

Scenarios have one exception: the main hero player's vision is not shared
with **neutral** characters, preventing them from revealing the hero's
position.

<a id="5-связь-с-другими-системами"></a>
## 5. Interaction with Other Systems

<a id="50-звук"></a>
<a id="51-звук"></a>
### 5.1. Sound

Sound is **not tied to fog of war**. It checks only the distance between the
source and the listener—the camera or an object. An enemy hidden by fog can
therefore still be heard when close enough. See
[Controls and Player Feedback §5](../../systems/ui_input_and_feedback.md).

<a id="51-целеуказание"></a>
<a id="52-выбор-цели"></a>
### 5.2. Target Acquisition

Vision and target acquisition are **separate mechanics**. The former uses
the fog-of-war coordinates described above, while the latter uses combat
range coordinates. For example, a **Tower** has a vision value of 32 and a
26.25-cell target-search radius; those numbers cannot be compared directly.
See [Target Selection and Attack-Move](target_selection.md).

<a id="52-поиск-пути"></a>
<a id="53-поиск-пути"></a>
### 5.3. Pathfinding

Vision **does not affect** route planning. Paths use the obstacle map rather
than only the visible area. Automatic rebuilding of an already issued route
after a new wall appears is a separate matter: if the formation stops,
issuing the movement order again is the reliable response. See
[Pathfinding and Movement](pathfinding.md).

<a id="53-компьютерный-игрок"></a>
<a id="54-компьютерный-игрок"></a>
### 5.4. Computer Player

The computer player is also limited by fog of war. A concealed flanking raid
can therefore remain unnoticed. See
[How the Computer Player Works](../../systems/ai_behavior.md).

<a id="технические-подробности"></a>
<a id="6-технические-подробности"></a>
## 6. Technical Details

The script registers `_unit_GetVision` with the engine through
`SetFOWDovFunc`. It returns
`floor(20 + 4 × objprop.vision)` only when
`GetGameObjectVisibleByHandle(handle)`, `not bdead`, and `bbuilt` are all
true; otherwise it returns zero [^1]. Native code handles line of sight and
the update rate.

`_player_UpdateFOW` starts with fog enabled, then disables it for
`bballoon = True`, `balloon = with`, `victorystate ≠ none`, or
`gbool_editor_fogofwar = False`. After `ClearFOWPlayers`, it adds the
current player and teammates through `AddFOWPlayers`, registers the vision
callback, and calls `SetFOWEnable(bFOW)` [^2]. Neutral characters
(`bneutral = True`) are excluded from the main scenario hero's shared vision
when `plInd = 0`.

For projectiles with
`StringPropertyTag = gc_properties_stringtag_fogreveal`, the temporary
reveal radius is `floor(TProj(pproj).dx)` [^3].

<a id="источники"></a>
## Sources

[^1]: `data/scripts/lib/unit.script:11563` — `_unit_GetVision`, including
      the vision formula and object-state checks.

[^2]: `data/scripts/lib/player.script:455-477` — `_player_UpdateFOW`,
      including fog-disable conditions and shared allied vision.

[^3]: `data/scripts/lib/unit.script:11572` — handling of
      `gc_properties_stringtag_fogreveal` on projectiles.
