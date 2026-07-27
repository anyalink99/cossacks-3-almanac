<a id="как-создаётся-случайная-карта"></a>
# How a Random Map Is Generated

[← How the Game Works](../../README.md)

A random map is assembled in stages: the game chooses the underlying terrain
shape, assigns starting positions, places nearby resources, fills the
remaining space, and creates the starting armies. Two generation keys allow
the same result to be reconstructed in a save or replay.

<a id="коротко"></a>
## At a Glance

- The lobby settings define a class of maps, not one fixed layout.
- A specific map is determined by its base mask, two generation keys, and
  generator version.
- The game reserves open space around every starting position and guarantees
  essential nearby forests, stone, and mineral deposits.
- The “Allies Nearby” option attempts to assign neighboring starting points
  to members of the same team.
- A standard start creates 18 Peasants.
- Peace time adds a technical border between player territories.

<a id="что-определяет-результат"></a>
## What Determines the Result

| Setting or value | Effect |
|---|---|
| Terrain type | Shape of land and water, coastlines, and available starting positions. |
| Relief | Balance of plains, hills, mountains, and buildable ground. |
| Deposits | Number of attempts to place nearby and distant Gold, Iron, and Coal deposits. |
| Season | Textures and environment sets; the desert uses separate variants. |
| Map size | Total area and placement density. |
| Teams | Standard position assignment or an attempt to keep allies together. |
| Base mask | Specific map shape and set of possible starting points. |
| Generation keys | Reproducible choices within the same mask and settings. |

Matching lobby settings without matching keys do not guarantee the same map.
Conversely, recorded settings and keys allow a replay to reconstruct the
original terrain.

<a id="пять-этапов-генерации"></a>
## The Five Generation Stages

| Stage | Result |
|---|---|
| 1. Preparation | Service masks are cleared and environment patterns are loaded. |
| 2. Relief | The surface, elevation, water, and coastlines are created. |
| 3. Starting positions | Players receive positions and the first resources and deposits are placed nearby. |
| 4. Remaining map | Distant deposits, forests, stone, swamps, lakes, and decoration are added. |
| 5. Finalization | Starting units appear, territories are assigned, and peace-time borders are created when needed. |

The order matters. Nearby resources reserve their space before the rest of
the map is filled, so a distant random forest cannot displace the guaranteed
forest beside a starting Town Hall.

<a id="стартовые-позиции"></a>
## Starting Positions

The set of possible positions is embedded in the map's base mask. The engine
reads markers from the terrain image and then assigns players to those
positions.

<a id="обычная-расстановка"></a>
### Standard Placement

Each player receives a random unoccupied position. Team numbers are not used
to bring allies together, so partners may begin on opposite sides of the
map.

<a id="союзники-рядом"></a>
### Allies Nearby

Members of one team are grouped first. The game chooses a cluster of nearby
starting points for the group and then distributes those positions among
its members. A player without teammates is handled as an individual group.

The algorithm tries to keep allies close, but it is limited to the points
provided by the base mask. Distances can still vary considerably on an
awkwardly shaped map.

<a id="4-setupstartingresourcespointx-pointy--что-спавнится-возле-города"></a>
<a id="ресурсы-возле-стартового-города"></a>
## Resources Near the Starting Town Hall

The game reserves the following resources roughly 5–22 cells from the
starting position:

- one mixed stone-and-forest area;
- two stone areas;
- three medium or large forests.

It first keeps an inner area clear for the starting army, then places the
resources in successive outer rings. The full area is reserved afterwards
so that distant objects cannot interfere with the starting economy.

Desert maps use their own forest, stone, and mixed-area variants while
following the same general rule.

<a id="8-как-размещаются-месторождения"></a>
<a id="8-что-значит-phase-1-vs-phase-2-mines"></a>
<a id="8-how-mineral-deposits-are-placed"></a>
<a id="как-размещаются-месторождения"></a>
## How Mineral Deposits Are Placed

Gold, Iron, and Coal deposits are placed in several rounds.

1. The first round creates nearby deposits about 14–22 cells from the start.
2. Later rounds add more distant deposits.
3. The game tests many valid locations for each deposit.
4. If no free, non-overlapping location is found, that deposit may be
   omitted.

On a Tiny map with Rich deposits, the calculation allows up to 12 deposits
per player, but the observed result is usually 9–12. The most distant
deposits may appear near the edges and corners, becoming contested neutral
resources.

<a id="стартовые-крестьяне-и-армии"></a>
## Starting Peasants and Armies

With the standard setting, the game creates 18 Peasants in a 6 × 3 grid and
adds a small random offset to each position. The number is the same for
every nation.

When a special starting-army preset is selected, the standard group is
replaced by the corresponding national force. The full list appears in the
[lobby-settings reference](../../../reports/map/lobby_settings.md#startingunits--стартовая-армия).

<a id="территории-и-время-мира"></a>
## Territories and Peace Time

After placing the players, the game divides the map according to the nearest
starting positions. Each area belongs to the player whose start is closest
on the territory grid.

When peace time is enabled, border objects are created along the boundaries
between neighboring territories. Land and water use different objects.
Once peace time ends, the border no longer protects the players.

See [Game Settings](game_settings.md#32-peacetime--как-устроен-мир) for the
rules of the mode.

<a id="12-seed-space"></a>
<a id="почему-карты-с-теми-же-настройками-различаются"></a>
## Why Identical Settings Produce Different Maps

The lobby settings define ranges and rules, while the keys select specific
choices within those rules:

- which valid starting point a player receives;
- the angle and distance of each forest placement;
- which attempted mineral-deposit locations succeed;
- where enough free space remains for a large pattern;
- which decorative objects fit into the available areas.

Two maps generated with different keys therefore retain the same broad
character while differing in detail.

<a id="что-видно-в-реплее"></a>
## What a Replay Records

The replay header stores the settings, base map record, and generation keys.
This allows the original terrain to be reconstructed before player orders
are replayed. A map preview is also stored in the header, but the image does
not replace the generator parameters.

For analysis, keep four concepts separate:

- **settings** — rules selected by the players;
- **keys** — the specific random variant;
- **generator version** — the algorithms and distance tables in use;
- **result** — the objects and starting positions actually placed.

<a id="практические-выводы"></a>
## Practical Takeaways

- When comparing matches, check both generation keys as well as the lobby
  settings.
- “Rich” means more placement attempts, not a guaranteed identical number
  of deposits.
- “Allies Nearby” improves team placement but cannot change the geometry of
  the available starting points.
- Starting forests and stone are placed before the distant environment and
  therefore take priority.
- With peace time enabled, starting positions determine the eventual
  territorial border.

<a id="техническое-приложение"></a>
## Technical Appendix

The full call sequence, distance formulas, pattern densities, replay-based
model validation, and version-specific behavior are documented in the
[technical map-generation analysis](../../../../internals_en/scripts/map_generation_evidence.md).
