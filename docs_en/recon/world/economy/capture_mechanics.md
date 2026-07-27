<a id="recon-механика-захвата"></a>
<a id="как-захватываются-здания-и-юниты"></a>
# How Buildings and Units Are Captured

[← How the game works](../../README.md)

Capture in Cossacks 3 does not use a long progress bar or a priest ability.
An eligible land unit must come close to the object while no defender is
nearby. The object changes owner as soon as the next capture check runs.

<a id="коротко-о-главном"></a>
## In brief

- Ordinary infantry or cavalry can capture buildings, peasants, and guns.
  Peasants and artillery pieces are not capturers themselves.
- One soldier within 4.013 cells of the object's reference point is enough.
- One defending unit within 7.987 cells prevents capture. Buildings do not
  defend one another.
- Ordinary buildings and peasants are checked about once every 1.9 game
  seconds; artillery is checked every 0.5 game seconds. Capture is therefore
  immediate once checked, but may appear slightly delayed.
- An Academy, or a Minaret for Turkey and Algeria, can be captured. Completed
  Towers, Barracks, Stables, and religious buildings cannot.
- An unfinished building can be captured even when its completed version
  cannot. A Tower can therefore change owner during construction, but not
  after completion.
- Walls and Gates do not change owner: triggering their capture logic destroys
  them.

<a id="что-можно-захватить"></a>
## What can be captured

The exact set depends on the capture rule selected before the match. The
tables below describe the Default option.

<a id="юниты"></a>
### Units

| Can be captured | Cannot be captured |
|---|---|
| A Peasant or Serf of any nation | Infantry |
| Cannon | Cavalry |
| Howitzer | Ships |
| Mortar | All other combat and support units |
| Multi-barrelled Cannon | |
| Ribauldequin | |

Standard Deathmatch and Historical Battle games use No Capturing Peasants.
Only the artillery listed above is therefore capturable in those matches.

<a id="здания"></a>
### Buildings

| Result | Canonical name |
|---|---|
| Capturable | Mill |
| Capturable | Market |
| Capturable | Storehouse |
| Capturable | Mine |
| Capturable | Town Hall |
| Capturable | Housing, Izba, or Hut |
| Capturable | Academy; Minaret for Turkey and Algeria |
| Capturable | Artillery Depot |
| Capturable | Blacksmith |
| Not capturable | Shipyard |
| Not capturable | Tower |
| Not capturable | Wall or Gate |
| Not capturable | Diplomatic Center |
| Not capturable | Cathedral, Orthodox Cathedral, or Mosque |
| Not capturable | Barracks, 17th century, and its national variants |
| Not capturable | Barracks, 18th century |
| Not capturable | Stable |
| Not capturable | Mission buildings and scenery objects |

The **Academy is capturable**, while both ordinary Barracks categories are
not. This is defined in the game data and does not vary by nation.

<a id="кто-захватывает-и-кто-защищает"></a>
## Who captures and who defends

A capturer is an ordinary enemy land unit that is not itself capturable. In
practice, this means infantry or cavalry. A whole formation is unnecessary:
one eligible soldier is sufficient.

Peasants, Serfs, and capturable artillery pieces cannot take enemy buildings.
They do not protect their own objects from capture either.

Almost any other friendly land unit acts as a defender. If one such unit is
inside the protection radius, the number of attackers no longer matters and
the ownership change is cancelled. Buildings, ships, and the rebel mercenary
side do not participate in this search.

<a id="расстояние-и-скорость"></a>
## Distance and timing

The game measures straight-line distance between object reference points.

| Check | Distance or period | What the player sees |
|---|---:|---|
| Capturer nearby | less than 4.013 cells | the object may change owner |
| Capturer extremely close | less than 3 cells | the captured object's fire is delayed by about 3.125 game seconds |
| Defender nearby | less than 7.987 cells | capture is cancelled |
| Building or peasant check | about every 1.9 game seconds | a short delay after approaching is possible |
| Artillery check | about every 0.5 game seconds | guns are captured noticeably faster |

For a large building, distance is measured from one reference point near its
centre rather than from the nearest edge of the model. A soldier standing at
the edge of a large Town Hall may therefore still be too far away. The first
check receives a small random offset so that every object on the map is not
processed at once.

<a id="что-происходит-после-захвата"></a>
## What happens after capture

In the ordinary case, the object immediately receives a new owner.

- A captured Peasant or Serf keeps the resource being carried, leaves the old
  formation, and adopts the new player's behaviour.
- A captured gun keeps its loaded shot, leaves its artillery formation, and
  comes under the new owner's control.
- Production and upgrade research in a captured building are cancelled. The
  resources spent on cancelled orders are refunded.
- Units inside a building change owner with it. This applies to actual
  internal slots; Towers have no garrison slots.
- If the building is destroyed rather than captured, units inside it die as
  well.

Computer players behave less predictably. When losing a building, an AI has a
75% chance to start destroying it instead of handing it over. Peasants and
different artillery types have separate difficulty-dependent checks and may
die before ownership changes. Exact probabilities and branches remain in the
[technical evidence](../../../../internals_en/scripts/capture_mechanics_evidence.md).

<a id="настройки-матча"></a>
## Match settings

| Capture rule | Result |
|---|---|
| Default | all cases listed above are enabled |
| No Capturing Peasants | peasants are killed rather than taken; this is standard in Deathmatch and Historical Battle |
| No Capturing Peasants or Centres | Town Halls cannot be captured either |
| Artillery Only | only artillery can be captured |

The complete setting table is in the
[match settings reference](../../../reports/map/lobby_settings.md#capture--правила-захвата).
During peacetime, capture is also blocked in territory that is not yet treated
as enemy territory; see
[How match settings affect the game](../map/game_settings.md).

<a id="особые-случаи"></a>
## Special cases

<a id="недостроенные-здания"></a>
### Unfinished buildings

Until construction is complete, the game checks every building for capture,
even when the finished object is normally immune. A Tower, Barracks, or Stable
can therefore be taken while it is being built. Its normal rule takes effect
once construction finishes.

<a id="башни"></a>
### Towers

A completed Tower cannot be captured. It has no unit slots and behaves as a
self-contained weapon rather than a garrisoned building. See
[building mechanics](building_mechanics.md#units-inside-buildings)
for the relation between buildings and internal unit slots.

<a id="стены-и-ворота"></a>
### Walls and Gates

Walls and Gates do not change owner. When an eligible enemy object comes
close, capture logic instead marks the section for destruction. Unlike an
ordinary building, any enemy non-building object is sufficient, so even a
peasant or a gun may trigger it. A Wall section below one third of its maximum
durability skips the ordinary defender check and firing delay.

<a id="священники"></a>
### Priests

Priests, Chaplains, Mullahs, and Padres heal allies; they do not convert
enemies. Healing restores the target's durability and never invokes an
ownership change.

<a id="нейтральные-объекты-и-наёмники"></a>
### Neutral objects and mercenaries

Starting peasants on a random map already belong to their players; the map
contains no neutral peasants or buildings. Scenarios may create neutral
players and change their diplomatic relations.

Mercenaries who rebel because their owner lacks gold move to a separate
game-controlled side that is hostile to every participant in the match. This
is not enemy capture, and those mercenaries are not treated as capturers. No
neutral treasure or chest system resembling the first Cossacks game was found
in the scripts examined for Cossacks 3.

<a id="что-ещё-нужно-проверить-в-игре"></a>
## What still needs in-game verification

- Which exact model point is used as the reference for asymmetric buildings.
- Whether a peasant or artillery piece can indeed destroy a Wall solely by
  approaching it under every relevant setting combination.
- Whether the observed maximum artillery capture delay matches the calculated
  0.5 game seconds.
- Whether the check runs for an object hidden by the fog of war.
- Whether a gun switching to its close-range behaviour affects capture.

<a id="технические-подробности-и-источники"></a>
## Technical details and sources

The complete account of game fields, call sites, peacetime conditions, AI
probabilities, and source-level pseudocode is kept in the
[technical appendix](../../../../internals_en/scripts/capture_mechanics_evidence.md).
It also records the exact paths and line numbers under `data/scripts/` used to
verify every claim in this article.
