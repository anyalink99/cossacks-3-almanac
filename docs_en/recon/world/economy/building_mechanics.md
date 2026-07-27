<a id="recon-механика-зданий"></a>
<a id="строительство-ремонт-и-разрушение-зданий"></a>
# Building Construction, Repair, and Destruction

[← How the game works](../../README.md)

Buildings occupy the map through an invisible mask. Their construction speed
depends on base time, the number of Peasants, and available work positions
around the foundation. Completed buildings can be repaired for free; after
destruction, ruins continue blocking the site for a while.

<a id="коротко-о-главном"></a>
## In brief

- The model visible on screen and the space it actually occupies may differ.
- The full price is charged when the foundation is placed.
- One Peasant builds in roughly base time ×1.13. Additional builders provide
  nearly proportional acceleration while free work positions remain.
- No more than 30 Peasants can work at once, and the building perimeter
  normally imposes a lower practical limit.
- Repair costs no resources and restores about 49.3 durability per game second
  for each Peasant.
- Healthy buildings do not decay, but a critically damaged structure keeps
  losing durability and collapses unless repaired.
- Ordinary ruins disappear after about 60 game seconds; Mine ruins take about
  120.
- Canceling a foundation or research refunds its cost. A unit-order refund
  uses the current base price and the price-growth tier saved at ordering.
  Capture cancels the queue and refunds the previous owner.

<a id="сколько-места-занимает-здание"></a>
## Building footprint

The game uses a grid of occupied cells rather than the visible outline of the
model. One mask cell equals half a map cell. The shape may be rectangular,
diamond-like, or indented.

This mask determines:

- where another building cannot be placed;
- how paths are routed around the structure;
- which sides can hold builders;
- which part of the site remains blocked by ruins.

The visual boundary used for selection is calculated separately. An area that
looks empty may therefore reject a foundation. Exact masks and extraction
details remain in the
[technical appendix](../../../../internals_en/scripts/building_mechanics_evidence.md).

<a id="как-идёт-строительство"></a>
## Construction

Every Peasant occupies a free perimeter position and repeats a 13-frame hammer
animation. One cycle lasts about 0.406 game seconds. Completion progress and
current durability rise together at the end of each cycle.

A practical time estimate is:

**time ≈ base time × 1.13 / active Peasants**

The estimate works while every Peasant has a position and has already reached
the foundation. Travel, obstacle avoidance, and occupied points increase the
real time.

For Bavaria's Barracks, 18th century, with a base time of 5,625 game seconds:

| Builders | Approximate time | Game minutes |
|---:|---:|---:|
| 1 | 6,356 game seconds | 105.9 |
| 2 | 3,178 | 53.0 |
| 5 | 1,271 | 21.2 |
| 10 | 636 | 10.6 |
| 16 | 397 | 6.6 |

Calculations for every building are available in the
[construction-time table](../../../reports/economy/construction_times.md).

<a id="сколько-строителей-помещается-вокруг"></a>
## Builder capacity

Work positions are distributed along the perimeter at roughly one-cell
intervals. A simple convex shape has about as many positions as the sum of its
mask width and height. Indentations, sparse shapes, and inaccessible sides
change the result.

The engine permits at most 30 builders on one structure. National architecture
matters: the Barracks, 18th century, ranges from 19 positions for Venice to 30
for Scotland and Russia. A larger building is not automatically built faster
by the same group; the number of reachable positions is decisive.

Per-building calculations are listed in the
[builder-position reference](../../../reports/economy/builder_slots.md).

<a id="ремонт"></a>
## Repair

Repair works only after construction is complete.

- Every hammer cycle restores 20 durability.
- No resources are spent.
- One Peasant restores about 49.3 durability per game second.
- Several Peasants repair in parallel while work positions remain.
- Current durability cannot exceed the maximum.

A Town Hall with 4,000 durability takes one Peasant about 81 game seconds to
restore; twelve take roughly 6.75.

<a id="стены-и-ворота"></a>
## Walls and Gates

An ordinary Wall section occupies 2×2 collision-mask cells, or 1×1 map cell,
and has four builder positions. Corners, intersections, and Gates use other
variants with up to 12 positions; the technical maximum is 16.

| Variant | Durability | Base time | Price |
|---|---:|---:|---|
| Wall for most European nations | 50,000 | 90 game seconds | 50 stone |
| Russian Wall | 50,000 | 200 | 60 stone |
| Turkish and Algerian Wall | 50,000 | 120 | 60 stone |
| Palisade | 1,500 | 5.6 | 10 wood |
| Ukrainian Palisade | 2,500 | 8.1 | 12 wood |

The table gives the price of one Wall section.

A Gate is created from a suitable straight Wall section rather than placed as
an entirely separate building. The central section is replaced and
immediately enters its completed state.

Protection and destruction are covered in
[Walls and Gates](../combat/walls_and_gates.md).

<a id="юниты-внутри-зданий"></a>
## Units inside buildings

Capacity is configured separately for different mechanics.

- An ordinary Mine accepts five Peasants; six upgrades raise capacity to 95.
- The **Ferry** carries 120 units.
- A Tower has no infantry slots. It fires as a self-contained stationary
  weapon.

If a building or transport is destroyed with units inside, its occupants die
as well. On ordinary building capture, internal units change owner with it.

Tower parameters are covered in
[How Towers Work](../combat/towers.md).

<a id="производство-повреждённого-здания"></a>
## Production in a damaged building

Low durability alone does not stop production. A completed building continues
training units and researching upgrades until it is destroyed or its queue is
blocked by a nearby capturer.

An unfinished building cannot produce.

<a id="захват"></a>
## Capture

An unfinished building is checked for capture regardless of the rule for its
completed version. A Tower under construction can therefore be taken, while a
completed Tower cannot.

Completed buildings follow their own permissions and the match settings.
Mills, Markets, Storehouses, Mines, Town Halls, Housing, Academies, Artillery
Depots, and Blacksmiths are capturable. The complete list, distances, and
defender rules are in
[How Buildings and Units Are Captured](capture_mechanics.md#buildings).

On capture:

- current durability is preserved;
- units inside change owner;
- the production queue is canceled and its resources return to the previous
  owner;
- the building counts toward the new owner's total and may increase the price
  of the next building of the same type.

Walls and Gates do not change owner; capture logic marks them for destruction.

<a id="разрушение-и-руины"></a>
## Destruction and ruins

A healthy building does not lose durability merely as time passes. Once an
ordinary structure falls to 1,999 durability or less, however, it begins a
slow collapse: it keeps burning and losing durability until repaired. Below
10 durability, final destruction begins.

After direct damage reduces durability to zero, or slow collapse reaches its
final threshold:

1. the building stops working;
2. after 30 game seconds, the next ruin stage appears;
3. after another 30 seconds, the object is removed, collision is cleared, and
   the site becomes available.

Both delays are doubled for a Mine. A canceled unfinished foundation proceeds
straight to the final stage after 30 game seconds.

Until ruins are removed, their occupied cells cannot hold another building.
An object that has entered destruction cannot be repaired; the player must
wait for the site to clear and place a new foundation.

<a id="возврат-ресурсов"></a>
## Resource refunds

| Event | Refund |
|---|---|
| Canceling an unfinished building | 100% of the foundation cost |
| Canceling a unit order | the current base price at the price-growth tier saved when ordered |
| Canceling research | 100% of the base cost |
| Destroying a building with a queue | refunds for unfinished units and upgrades under the same rules |
| Capturing a building with a queue | the previous owner receives the same refunds for unfinished orders |

The destroyed or captured building itself is not refunded. Only canceled
orders inside it return resources. If a unit-price upgrade completed after
the order was placed, its refund may differ from the original charge: the
game uses the new base price but the previously saved price-growth tier.

<a id="технические-подробности-и-источники"></a>
## Technical details and sources

Collision masks, the builder-position algorithm, national source parameters,
internal destruction states, formulas, and exact code references are kept in
the
[technical appendix](../../../../internals_en/scripts/building_mechanics_evidence.md).
