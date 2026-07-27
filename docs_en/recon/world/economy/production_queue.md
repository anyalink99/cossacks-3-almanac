<a id="recon-очередь-производства"></a>
<a id="очередь-производства"></a>
<a id="как-работает-очередь-производства"></a>
# How Production Queues Work

[← How the game works](../../README.md)

The queue determines the order in which a building trains units and researches
upgrades. It also governs infinite production, merging repeated orders, and
resource refunds after cancellation.

<a id="коротко-о-главном"></a>
## In brief

- Repeated orders for the same unit are normally merged into one queue entry.
- Infinite production continues until the player cancels it.
- If a unit becomes more expensive with every completed copy, the game keeps
  separate order groups so that cancellation refunds the correct amount.
- Several buildings of the same type distribute a shared order between them.
- An enemy capturer near a building may stop production before the building
  itself changes owner.
- When a building is captured or destroyed, unfinished orders are cancelled
  and their resources return to the previous owner.
- Upgrade research uses the same general queue, but the same upgrade cannot be
  ordered twice.

<a id="как-добавляются-заказы"></a>
## Adding orders

When the player clicks the same unit portrait again, the game first looks for
an existing entry. If the unit's price is constant, the new quantity is simply
added to it. Five successive Pikeman orders may therefore appear as one entry
with a quantity of five.

For units whose price rises with every completed copy, merging is safe only
until another unit of that type is produced between orders. The game otherwise
creates a separate entry. This preserves the price of each group and makes an
exact refund possible later.

A building's internal list can hold up to 12 actions of all kinds. Production,
research, repair, and other orders share that limit. The interface displays
fewer entries and normally prevents the player from filling all 12 manually.

<a id="бесконечное-производство"></a>
## Infinite production

Infinite production is not represented by an enormous hidden quantity. The
queue entry simply remains active after every completed unit.

- An ordinary finite request does not change an existing infinite order for
  the same unit.
- Cancellation can remove an entry or, when the corresponding interface
  action is used, convert a finite order into an infinite one.
- Production ends only after explicit cancellation, loss of the building, or
  another condition that prevents the order from continuing.

<a id="прогресс-и-выпуск-юнита"></a>
## Progress and unit release

The building gradually fills the active queue entry. Once the training time is
reached, the unit appears at the rally point and the remaining quantity
decreases by one. A zero entry disappears; an infinite one remains.

When several buildings of the same type are selected, the game tries to spread
orders between them. It prefers the less occupied building, so a large order
from several Barracks is normally processed in parallel instead of entirely
by one building.

<a id="отмена-и-возврат-ресурсов"></a>
## Cancellation and refunds

Cancellation refunds every copy that has not yet been completed. For a unit
with a constant price, this is simply its price multiplied by the quantity.
For a unit with escalating cost, the game accounts for the position of each
order in the player's overall unit count.

This is why the queue remembers how many units had already been completed when
the order was placed. Cancelling five escalating copies calculates five
separate prices rather than using one current price for all of them.

<a id="захватчик-рядом"></a>
## A capturer nearby

Production checks nearby enemies every game tick. If an eligible capturer is
close and no friendly defender is present, progress on the current entry
stops. A cavalry raid beside a Barracks can therefore freeze unit training
before the building is captured.

A nearby defender removes the block. The radii and eligible units are
explained in [How Buildings and Units Are Captured](capture_mechanics.md).

<a id="что-происходит-при-захвате"></a>
## Capture

When ownership changes, every production and research order is cancelled.
Resources return to the **previous** owner, while the new owner receives an
empty queue.

The capturer does not inherit nearly completed units and cannot continue the
opponent's research. New orders must be placed before the captured building
can be used.

<a id="что-происходит-при-разрушении"></a>
## Destruction

Destroying a building also cancels its whole queue and refunds unfinished
units and upgrades. This applies both to demolishing one's own building and to
losing it to an enemy attack.

The refund softens the loss of a production building, but does not compensate
for the building itself or units that were already completed.

<a id="очередь-улучшений"></a>
## Upgrade research

Research occupies an entry in the same general action list. It differs from
unit production in several ways:

- the same upgrade cannot be researched twice;
- cancellation refunds its base price;
- completion applies the effect to eligible objects and removes the entry.

The application order is covered in
[How Upgrades Are Applied](upgrades_application.md).

<a id="ограничения-интерфейса"></a>
## Interface limits

The internal limit is 12 actions, but the visible queue usually contains five
or six slots. The remainder accommodates service actions such as repair and
keeps the progress display manageable. The exact number of visible slots at
different window sizes still needs verification.

<a id="что-ещё-нужно-проверить-в-игре"></a>
## What still needs in-game verification

- The exact production speed multiplier for every AI difficulty.
- The number of entries shown at different resolutions and interface scales.
- Whether progress remains stopped for the entire time a capturer is nearby
  or only on individual detection ticks.

<a id="технические-подробности-и-источники"></a>
## Technical details and sources

The queue-entry structure, complete internal order-type list, refund formula,
merge conditions, and function references are kept in the
[technical appendix](../../../../internals_en/scripts/production_queue_evidence.md).
