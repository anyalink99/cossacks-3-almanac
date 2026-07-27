<a id="поиск-пути-и-движение-юнитов"></a>
# Pathfinding and Unit Movement

[← How the Game Works](../../README.md)

This article explains why units stretch out in narrow passages, catch on
building corners, or stop in front of a newly placed obstacle. The game
solves two separate problems: it first finds a route across the map, then
separates nearby objects on each frame so that they do not occupy the same
space.

<a id="коротко"></a>
## At a Glance

- Land and water routes are calculated separately.
- Requests issued at nearly the same time are processed as one batch.
- A global route is a chain of intermediate points; a unit may skip a bend
  when the next section is clear.
- Allied units gently push each other aside, buildings remain fixed, and
  ships displace nearby objects more strongly than land units do.
- A formation has no single leader: every soldier receives an individual
  destination.
- If no route can be found, the unit stops. There is no universal
  teleport-out-of-trouble mechanism.

<a id="как-строится-движение"></a>
## How Movement Is Calculated

<a id="глобальный-маршрут"></a>
### The Global Route

After receiving an order, the game looks for a passable chain from the
unit's current position to its destination. This is the broad route around
coastlines, buildings, walls, and other blocked areas. Land and naval
movement use separate queues, so a ship cannot receive a land route and an
infantry unit cannot receive a water route.

The calculation is not performed independently at the exact moment of every
click. Requests are collected and passed to the engine as a batch roughly
once every 20 ms. A mass order therefore creates one short burst of work
rather than hundreds of evenly spaced calculations.

The resulting route contains intermediate points. When the line to a later
point is clear, the unit can omit an unnecessary bend. This makes movement
look smoother than the underlying route.

<a id="локальный-обход"></a>
### Local Avoidance

The global route does not predict the exact position of every soldier. Local
avoidance is applied while units are moving:

| Neighbor | Response |
|---|---|
| Allied unit | Both objects move apart slightly without starting combat. |
| Enemy directly ahead | The moving unit may stop and switch to an attack. |
| Building or wall | The obstacle remains fixed; the unit adjusts its own movement. |
| Ship | Its greater mass and radius push nearby vessels more strongly. |

The combination of a global route and local avoidance explains why a unit
may know how to reach its destination yet still struggle through a crowd.

<a id="почему-юниты-застревают"></a>
## Why Units Get Stuck

When no route is available, the unit stays where it is. The guaranteed way
to create a fresh path request is to issue another movement order. How an
existing route reacts automatically to a new obstacle depends on the native
pathfinding system; no fixed recalculation interval has been established.

When more than three objects are standing nearby and several have remained
still for about three game seconds, the unit periodically searches for a
free position in a small outward spiral. This clears ordinary jams near
gates and construction sites, but it cannot rescue a unit from a completely
sealed area.

Common causes include:

- opposing streams trying to use the same narrow passage;
- a building completed after the movement order was issued;
- a wide formation entering a one-column gap;
- a destination placed inside an occupied area;
- too little clearance around a shoreline or building corner.

<a id="движение-в-строю"></a>
## Formation Movement

A formation does not follow an invisible leader along one shared route. The
game calculates each soldier's place in the formation grid, adds a small
random offset, and assigns an individual destination.

This produces three visible effects:

1. a wide formation stretches out when entering a narrow passage;
2. the front ranks may already be turning while the rear ranks are still
   avoiding an obstacle;
3. after stopping, the formation regroups around its assigned positions.

For a long march through dense construction, use a narrower formation or
guide the army with several shorter orders.

<a id="когда-маршрут-пересчитывается"></a>
<a id="when-a-route-is-recalculated"></a>
<a id="как-запросить-новый-маршрут"></a>
## How to Request a New Route

A new movement order creates a fresh path request. This is the reliable way
to rebuild a route after the situation changes. If a newly completed wall or
building blocks the army and it stops, issue the order again after the new
obstacle has appeared.

The obstacle's appearance by itself carries no confirmed guarantee of an
immediate full recalculation. Local separation and the search for a free
place in a crowd help units move around neighbors, but do not replace a new
global path request.

<a id="что-влияет-на-производительность"></a>
## Performance Considerations

A mass command collects the route requests for every selected unit and sends
them to the engine in one batch. The workload therefore rises abruptly when a
large group receives an order at the same time.

The heaviest situations are:

- hundreds of units receiving a new long-distance destination at once;
- several wide formations moving through dense construction;
- opposing streams meeting at gates or bridges;
- ships maneuvering in a narrow coastal area.

Several smaller orders usually produce steadier movement than sending an
entire army through a complicated maze at once.

<a id="практические-советы"></a>
## Practical Advice

- Clear idle workers away from gates before moving a large army.
- Narrow a formation before a bridge, gate, or dense city block.
- Repeat the order when a newly completed structure blocks the old route.
- Do not place the destination inside a building, wall, or dense group.
- Split a very large army into several columns when parallel routes exist.
- Give ships extra room to turn and pass one another.

<a id="техническое-приложение"></a>
## Technical Appendix

Internal queue names, collision geometry, mass values, stuck-unit handling,
and script excerpts are documented in the
[technical pathfinding analysis](../../../../internals_en/scripts/pathfinding_evidence.md).
