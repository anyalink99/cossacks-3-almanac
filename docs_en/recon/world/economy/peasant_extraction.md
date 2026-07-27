<a id="recon-добыча-ресурсов-крестьянами"></a>
<a id="как-крестьяне-добывают-ресурсы"></a>
# How Peasants Gather Resources

[← How the game works](../../README.md)

Gathering speed depends on more than the number of Peasants. The work-cycle
length, carried portion, distance to a drop-off point, competition for one
source, and researched upgrades all matter. Mines work differently: they add
resources continuously while Peasants remain inside.

<a id="коротко-о-главном"></a>
## In brief

- A Peasant works a source several times, fills a carried portion, delivers it
  to an eligible building, and then searches for another source near the
  original work location.
- Ignoring travel, one Peasant can gather at most 178 food or 213 wood or
  stone per game minute at initial efficiency.
- Actual wood and stone income is lower because of travel to a Storehouse.
  Food also depends on the distance to a Mill and on field regrowth.
- No more than two Peasants normally work one tree at once; a field or stone
  usually accepts no more than three.
- Stone is effectively inexhaustible. A felled tree becomes a stump, but a
  quirk of the game logic lets the stump continue producing wood forever.
- An ordinary Mine holds five Peasants and yields about 499 gold, iron, or
  coal per game minute. Upgrades raise capacity to 95.
- All rates below use game seconds. At Fast speed, game time runs 1.4 times as
  fast as at Normal speed.

<a id="рабочий-цикл"></a>
## The work cycle

Ordinary food, wood, and stone gathering follows four stages.

1. **Work at the source.** The Peasant repeats an animation, adding one hit to
   the carried portion after each completed cycle.
2. **Travel to a drop-off.** Once enough hits are collected, the Peasant
   chooses the nearest building that accepts the resource.
3. **Delivery.** Near the building's fixed drop-off point, the portion is
   multiplied by current efficiency and added to the player's stockpile.
4. **A new target.** The Peasant searches near the location where the original
   order was issued. The normal radius is six cells and may expand to twelve
   after a long idle period.

Target selection accounts for distance and other workers. An unused source is
preferred over one that other Peasants are already approaching or working.

<a id="порции-и-верхняя-граница-скорости"></a>
## Portions and maximum rates

| Resource | Hits before delivery | Portion | One hit | Maximum per game minute |
|---|---:|---:|---:|---:|
| Food | 22 | 45 | 0.6875 game seconds | about 178 |
| Wood | 14 | 28 | 0.5625 game seconds | about 213 |
| Stone | 20 | 40 | 0.5625 game seconds | about 213 |

These are travel-free ceilings. A Peasant moves about 1.20 cells per game
second, so a poorly placed Storehouse or Mill can reduce real income more than
a modest efficiency upgrade.

After delivery, the next source is searched for around the original order
point rather than around the building. This sends the Peasant back to the
assigned area, but may leave the worker idle when no eligible source remains
there.

<a id="куда-сдаются-ресурсы"></a>
## Resource drop-off points

- Food is accepted by the Mill and other buildings enabled for it.
- Wood and stone are normally delivered to a Storehouse or Town Hall.
- The Peasant walks to a fixed point rather than the nearest edge of the
  building model. Architectural variants place this point differently.

The Spanish and Portuguese Storehouse has no separate offset and uses the
building centre. Other main variants place the point on the northern side.
Exact coordinates for Storehouses, Mills, and Town Halls remain in the
[technical model](../../../../internals_en/scripts/peasant_extraction_evidence.md).

<a id="сколько-крестьян-помещается-у-одного-источника"></a>
## Workers at one source

| Source | Normal simultaneous-worker limit |
|---|---:|
| Field | 3 |
| Tree | 2 |
| Stone | 3 |
| Other ground resource | 4 |

Target search may occasionally bypass the limit, but stable gathering should
not be planned around that exception. In a forest, spreading workers between
several trees is normally better.

<a id="дерево-и-пни"></a>
## Trees and stumps

The game randomly chooses a tree's size when it is created. Large trees are
rare but contain vastly more durability than small ones.

| Variant | Probability | Durability | Approximate wood reserve |
|---|---:|---:|---:|
| Giant tree | 20% | 8,000–16,000 | 16,000–32,000 |
| Medium tree | 15% | 125–624 | 250–1,248 |
| Small tree | 45% | about 20–75 | about 40–150 |
| Spawned stump | 20% | 10 | about 20 |

Every hit yields an average of two wood. A rough expectation for a newly
created tree is about 4,956 wood before the first felling.

When durability reaches zero, the model changes to a stump but the source
remains eligible for work. Its durability proceeds into negative values while
Peasants continue to receive portions. **Wood is therefore effectively
infinite.**

Whole trees are usually selected before stumps because a busy source receives
a target-selection penalty, not because stumps are explicitly forbidden. An
unused stump and an unused tree are compared mainly by distance.

<a id="камень"></a>
## Stone

A stone object has 10,000,000 durability. That is ten million hits, roughly
500,000 complete trips, and about 20 million stone from one object. It can be
treated as inexhaustible in an ordinary match.

<a id="поля-и-еда"></a>
## Fields and food

A new Field receives 25,000 durability. At initial field durability, one hit
removes 100, so it survives 250 hits and yields about 511 food before the
first exhaustion.

| Total field-durability bonus | Durability lost per hit | Approximate food before exhaustion |
|---:|---:|---:|
| 0 | 100 | 511 |
| +100 | 50 | 1,023 |
| +200 | 33 | 1,549 |
| +300 | 25 | 2,045 |
| +500 | 16 | 3,196 |

While a Field remains in its mature visual stage, it periodically restores a
random portion of durability. After complete exhaustion it passes through
death and four growth stages; total downtime is about 109.375 game seconds.
Food cannot be gathered during growth.

For most European nations, an Academy upgrade grants +200 field durability
and a Blacksmith upgrade grants another +100. National exceptions should be
checked in the upgrade reference.

<a id="шахты"></a>
## Mines

Gold, iron, and coal are not carried to a Storehouse. A Peasant enters a Mine
and increases its continuous income.

| Ordinary Mine parameter | Value |
|---|---:|
| Initial capacity | 5 Peasants |
| Income per Peasant | about 1.664 resource per game second |
| Income of a full Mine | about 8.32 resource per game second |
| Income of a full Mine per game minute | about 499 |
| Building cost | 100 wood and 100 stone |
| Base construction-time value | 93.75 game seconds |

Because construction advances on hammer cycles, one Peasant finishes the Mine
in about 105.9 game seconds. Six successive upgrades increase the capacity of
the selected Mine:

| After level | Capacity |
|---:|---:|
| No upgrade | 5 |
| 1 | 10 |
| 2 | 18 |
| 3 | 28 |
| 4 | 40 |
| 5 | 55 |
| 6 | 95 |

A fully occupied 95-Peasant Mine yields about 158.08 resource per game second,
or 9,485 per game minute. All six upgrades cost 104,550 food and 80,950 gold.
They are individual: every Mine must be upgraded separately.

<a id="улучшения-эффективности"></a>
## Efficiency upgrades

Efficiency starts at 100. Bonuses increase the delivered portion but do not
shorten the journey or speed up the work animation.

Common upgrades include:

- three successive Mill upgrades: +40%, +50%, and another +50% food
  gathering;
- an Academy upgrade granting +100% wood gathering;
- two Academy upgrades granting +100% and +200% stone gathering.

The exact set and prerequisites vary by nation. Canonical names, prices, and
chains are listed in the [upgrade reference](../../../reference/05_upgrades/README.md).

<a id="влияние-карты"></a>
## Map influence

On a Tiny land map with Highlands terrain and Rich deposits, the generator
creates four gold, four iron, and four coal deposits for each player. They are
placed in several bands roughly 14 to 82 cells from the starting point.

The Town Hall area also receives one mixed stone-and-forest group, two stone
groups, and three forest groups. This starting set is separate from general
map filling.

For this setting combination, whole-map calculations give the following rough
figures:

| Measure | Estimate |
|---|---:|
| Choppable trees | about 8,200 |
| Stone objects | about 861 |
| Initial durability of all trees | about 40 million |
| Effective wood reserve including stumps | infinite |

Forest figures are approximate. A pattern mask records places for environment
objects, not a guaranteed count of choppable trees. Measurements support a
working estimate of about 30% of occupied mask cells.

Deposit, forest, and starting-resource placement is explained in
[How the Map Is Generated](../map/map_generation_pipeline.md).

<a id="практические-выводы"></a>
## Practical conclusions

- Place drop-off points close to the work area; travel is paid after every
  portion.
- Do not send a large group to one tree; distribute it through the forest.
- Efficiency upgrades matter most after travel distance has already been
  reduced.
- Estimate the payback time of Mine capacity upgrades: late levels are very
  expensive and affect only one building.
- An exhausted Field must be replaced or allowed to complete its growth cycle.
- Complete depletion of wood or stone is not a realistic concern in an
  ordinary match; worker throughput remains the main limit.

<a id="что-ещё-нужно-проверить"></a>
## What still needs verification

- The complete efficiency-upgrade set for each of the 21 nations.
- The real share of working time lost to obstacle avoidance.
- The effect of water transport on isolated forests.
- How animation-speed changes interact with physical walking speed.
- A more precise ratio between a forest-pattern mask and available trees.

<a id="технические-подробности-и-источники"></a>
## Technical details and sources

Target-selection formulas, drop-off coordinates, game-data fields, the full
map-pattern analysis, source-level pseudocode, and exact line references are
kept in the
[technical model](../../../../internals_en/scripts/peasant_extraction_evidence.md).
