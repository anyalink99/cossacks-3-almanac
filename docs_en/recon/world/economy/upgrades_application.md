<a id="recon-применение-апгрейдов"></a>
<a id="как-применяются-улучшения"></a>
# How Upgrades Are Applied

[← How the game works](../../README.md)

An upgrade takes effect when research finishes. Combat attributes and
gathering efficiency change on existing objects, and faster construction or
training immediately affects work already in progress. Discounts apply only
to new orders.

<a id="коротко-о-главном"></a>
## In brief

- A completed upgrade affects both existing and future objects.
- Damage, protection, durability, and gathering efficiency change
  immediately: the next attack or delivered portion uses the new value.
- A price reduction does not refund the difference for existing orders.
- Reduced production or construction time accelerates a process that has
  already started from its next progress update.
- Most bonuses combine in a way that makes final attributes independent of
  research order.
- Research can be canceled before completion. No effect is applied, the queue
  slot is released, and the full base cost is refunded.
- Every ordinary upgrade is researched once. Levels in one chain are separate
  upgrades and their effects combine.

<a id="когда-появляется-эффект"></a>
## When the effect appears

Research occupies a slot in the building queue. At completion, the game marks
the upgrade as done, finds every eligible target, and applies the effect.

| Effect type | Existing objects | New objects and orders |
|---|---|---|
| Damage, protection, durability | change immediately | are created with the bonus |
| Gathering efficiency | the next delivered portion uses the bonus | new Peasants receive the same bonus |
| Price | paid orders are not recalculated | new orders receive the discount |
| Construction or training time | the next progress step uses the reduced base duration | a new process uses the reduced duration immediately |

A Mill upgrade therefore improves every Peasant already working on the map,
while faster construction immediately accelerates a building started before
research finished.

<a id="на-кого-действует-улучшение"></a>
## Upgrade targets

An upgrade may affect:

- one specific unit or building;
- a unit class, such as 17th-century Pikemen;
- several listed objects;
- every unit of a nation;
- every building of a nation.

The canonical name explains the game-facing purpose, while the complete target
list reveals national exceptions. Names, prices, prerequisites, and targets
are listed in the [upgrade reference](../../../reference/05_upgrades/README.md).

<a id="как-складываются-бонусы"></a>
## Combining bonuses

Gathering efficiency starts at 100 and bonuses are added to it. Four upgrades
granting +5, +10, +15, and +20 result in 150%, rather than a chain of
multiplications.

A base food portion of 45 at 150% efficiency becomes 67 after rounding down.
The order in which the four upgrades were researched does not change that
result.

Damage stores its base separately from the sum of flat and percentage bonuses.
The final value is recalculated from the complete totals. With base damage 10,
a +5 bonus, and +25%, the result is 18 whichever upgrade finished first.

<a id="какие-показатели-складываются-одинаково"></a>
## Attribute rules

| Attribute | Rule | Does order matter? |
|---|---|---|
| Flat and percentage damage | bonuses are totalled before recalculation from the base | No |
| Protection and shield | flat bonuses are added | No |
| Food, wood, and stone efficiency | every bonus is added to the initial 100 | No |
| Field durability | bonuses are added | No |
| Unit durability | percentage multipliers are applied in succession | Usually no; rounding may differ by 1 |
| Time, range, and firing rate | percentage multipliers are applied in succession | No |
| Price and fishing | rounding occurs after each step | A difference of 1 is possible |

Movement speed uses an unusual reciprocal formula in the script. Several such
upgrades could make the result order-dependent, but ordinary data contains
only one relevant upgrade for each unit type, so the issue cannot be repeated
in the standard game.

<a id="скидки-и-ускорение"></a>
## Discounts and faster production

A discount may affect individual resources. An artillery upgrade can reduce
gold and iron costs without changing the wood or coal component. The discount
is applied when a new order is created.

A production- or construction-speed upgrade reduces the corresponding base
time by its stated percentage. A production queue reads that duration again
on every progress update, while a building under construction uses it on
every subsequent builder strike. Both new and ongoing work therefore
accelerate; progress accumulated before the upgrade is not recalculated.

<a id="отмена-исследования"></a>
## Canceling research

Before completion, research can be canceled in its building:

1. progress is reset;
2. the effect is not applied;
3. the queue slot becomes free;
4. the player receives the upgrade's full base cost.

The game refunds 100% of the upgrade's base cost. Unlike escalating unit
prices, upgrade refunds do not scale with the number of previously completed
copies.

<a id="повторное-исследование"></a>
## Repeat research

An ordinary completed upgrade disappears from the available set and cannot be
ordered again. First, second, and third levels are distinct entries; each must
be researched separately and their effects combine.

Unique upgrades target particular national objects rather than an entire
class. Two nations may therefore have superficially similar chains with
different effective target sets.

<a id="переход-в-xviii-век"></a>
## Advancing to the 18th century

Progress to the 18th Century is a specific Town Hall upgrade, not a timer.
Most nations require:

- a Town Hall;
- an Academy;
- a Cathedral;
- an Artillery Depot.

The upgrade itself costs roughly 30,000 food, 5,000 gold, 2,000 iron, and
2,000 coal and takes about 9.38 game seconds to research. Required buildings
are normally the real delay.

After the transition, the Barracks, 18th century, becomes available. Its
approximate price is 1,700 wood, 2,950 stone, and 4,000 gold. The base
construction-time value is 5,625 game seconds; because progress is applied on
hammer cycles, one Peasant finishes it in about 6,356 game seconds. Additional
builders reduce this time according to the rules in
[Building Construction, Repair, and Destruction](building_mechanics.md).

Ukraine, Turkey, and Algeria have neither an available 18th-century transition
nor the Barracks, 18th century. These nations remain in the 17th century and
develop their own national unit and upgrade chains.

<a id="требования-и-дерево-развития"></a>
## Prerequisites and the technology tree

An upgrade button appears after every prerequisite is met. Requirements may
include buildings, earlier levels in a chain, and the 18th-century transition.

Order matters for **when an effect becomes available** and for unlocking later
options, but almost never for the final bonus arithmetic. Fully developed
armies can therefore be compared by their upgrade set; a match analysis must
still account for which benefit arrived first.

The full prerequisite graph is available in the
[technology tree](../../../reports/tech/tech_tree.md).

<a id="технические-подробности-и-источники"></a>
## Technical details and sources

Internal effect types, target fields, formulas for every branch, the unusual
movement-speed calculation, century-transition identifiers, and exact line
references are kept in the
[technical appendix](../../../../internals_en/scripts/upgrades_application_evidence.md).
