<a id="recon-очередь-производства"></a>
# Recon: production queue

In-depth analysis: how the order queue in buildings works
(barracks/academy/stable/town hall), how replays work and
endless mode, what happens when canceling, when capturing, when
demolition All links to the code are in [Sources](#sources).

> **Related documents:**
> [`building_mechanics.md` §6.3](building_mechanics.md) - refund when
> cancellation/destruction; [`upgrades_application.md` §3](upgrades_application.md)
> - separate queue for upgrades;
> [`unit_commands.md`](../combat/unit_commands.md) - general model
> orders on units (also uses `gOrders`).

## TL;DR

- The building holds up to **`gc_obj_MaxOrderCount = 12`** simultaneous
  orders [^1]. This is a general limit for all types (production,
  upgrade, repair, etc.), not for each separately.
- Each production order is a record `TOrder` with fields
  `produceid` (unit sid), `amount` (how much more to produce),
  `progress` (progress of the current instance), `restype` (counter
  built copies **at the time of order** - needed for refund).
- `amount = -1` (`gc_obj_order_produce_infinite`) means
  **endless mode** - the building produces a unit until the order is
  will be canceled obviously.
- **Order of the same unit into an existing order is merged**: if in
  the queue already has `peaaus` order and `costpercent = 100` (or
  zero) - new `peaaus` will be added to the existing `amount`, not
  will create a separate order.
- With different `costpercent` (`peaaus` becomes more expensive with each new one)
  the merge occurs only if `unitcount = restype` - that is
  the player did not have time to build other units of the same type between
  orders.
- **Capture The person nearby stops production.** If in the zone
  scan-grid a `bcancapture` enemy unit appears near the building without
  `bprotector`-defender - the building **stops** order progress.
- When a building is demolished, all orders are scrolled back - paid
  units and upgrades are returned to the player (see.
  [`building_mechanics.md` §6.2](building_mechanics.md)).

---

<a id="1-структура-ордера-на-производство"></a>
## 1. Production order structure

`TOrder` — entry in the `TObj.orders[0..gc_obj_MaxOrderCount-1]` [^1] array.
Fields for type `gc_obj_order_type_produce = 4`:

| Field | What |
|---|---|
| `itype` | Order type. `4` = unit production. For a complete list, see §1.1. |
| `info.produceid` | sid of the unit we are producing. |
| `info.amount` | How much more to produce? `-1` (`gc_obj_order_produce_infinite`) = infinite. |
| `info.progress` | Progress of the current instance (`0..buildtime`). |
| `info.restype` | Counter of built copies **at the time of order**. Used in `_unit_CancelUnitProduction` to return the correct amount when `costpercent ≠ 100`. |

<a id="11-все-типы-ордеров-gcobjordertype"></a>
### 1.1. All order types (`gc_obj_order_type_*`)

| ID | Type | Application |
|---:|---|---|
| 0 | `none` | Empty queue cell. |
| 1 | `move` | Go to the point. |
| 2 | `attackobj` | Attack a specific unit. |
| 3 | `gainres` | Extract a resource. |
| 4 | `produce` | **Unit production** (this article). |
| 5 | `patrol` | Patrolling. |
| 6 | `attackpoint` | Shooting at a point (artillery). |
| 7 | `continueattackpoint` | Continuation of the point attack. |
| 8 | `performupgrade` | **Upgrade Research.** |
| 9 | `fishing` | Fishing (for `fishboat`). |
| 10 | `creategates` | Construction of gates. |
| 11 | `buildwallcontinue` | Continued construction of the wall. |
| 12 | `buildwall` | Building a wall. |
| 13 | `gotomine` | Go to the mine. |
| 14 | `gototransport` | Go to the transport ship. |
| 15 | `leavetransport` | Get out of the vehicle. |
| 16 | `leavebuilding` | Leave the building (garrison). |
| 17 | `build` | Build a building. |
| 18 | `guard` | Protect. |
| 19 | `repair` | Repair. |
| 20 | `exitunits` | Release all units from the garrison. |

`MaxOrderCount = 12` orders **total** limit - that is, the building
can simultaneously hold a mixture of, for example, 5 orders for
production, 2 for upgrade and 1 for repair. Unit fighter is usually
uses only `move`, `attack`, `guard`, etc., but the limit
the same.

---

<a id="2-добавление-ордера-в-очередь"></a>
## 2. Adding an order to the queue

`_unit_OrderProduce(goHnd, ordercid, orderid, amount)` [^2]:

1. Goes through existing orders from the end (`MaxOrderCount-1
   downto 0`).
2. Searches for an existing order of the same `produceid`.
3. **If found and the merging conditions are suitable** (see §2.1) - increases
   `amount` of an existing order.
4. **If not found** - adds a new order to the first free one
   cell via `_unit_AddOrder` [^3].
5. If there are no more cells (12 are occupied) - the order is **discarded**
   silently.

<a id="21-условия-слития-ордера"></a>
### 2.1. Conditions for merging an order

Orders are merged (new units are added to existing ones `amount`)
if:

- **`costpercent = 100`** (price does not increase) - always merges.
- **`costpercent = 0`** (special “no scaling”) —
  also merges.
- **`unitcount = order.restype`** - the player has not yet built any
  one unit of this type after the first order. Then `costmodifier`
  for refund remains valid, and the merge is safe.

In other cases, a **new** order is created with the correct
`restype = unitcount` (current counter). This is critical for refund:
if it were possible to merge everything into one order, and the player built 5
expensive units between orders, the refund would be calculated with
irrelevant `costmodifier`.

<a id="22-бесконечный-режим"></a>
### 2.2. Endless Mode

`amount = gc_obj_order_produce_infinite = -1` means "continue"
until explicit cancellation." When `_unit_OrderProduce` meets
existing endless order and a request comes with a specific
number (`amount > 0`) - a specific order **ignored** (inside
infinite and so everything will happen).

Mirror semantics in `_unit_CancelUnitProduction` with
`bConvertToInfinite = True` [^4]: one cancelable unit from the final
orders can **turn** an order into an endless one (if `amount`
reached 0 or 1).

---

<a id="3-прогресс-и-завершение"></a>
## 3. Progress and completion

Each game tick function `_unit_DoOrderProgress` (located in
`units/global.inc` or similar) increases `info.progress` by
`deltatime × buildtime_modifier`. When `progress >= buildtime`:

1. A unit is created via `_unit_ProduceUnit` [^5].
2. The unit will spawn at the `rallypoint` building (or at the entrance, if rally
   not specified).
3. `info.amount -= 1`. If it becomes 0, the order is completed and deleted.
4. If `amount = -1` (infinite) - the order continues.

`_unit_ProduceUnit` distributes production **over several
buildings of the same type**: if there are several barracks in `list`, select
the one with the minimum `produceind` (i.e. the least
orders in queue). This is automatic balancing: the player can
request "20 pikemen from all barracks", and they are uniformly
will be distributed.

---

<a id="4-отмена-заказа"></a>
## 4. Order cancellation

`_unit_CancelUnitProduction(goHnd, cid, unitID, amount, bConvertToInfinite)` [^4]:

1. Finds an order with the required `produceid`.
2. Decreases `info.amount` by 1.
3. If `amount` reaches 0:
   - **Without bConvertToInfinite** - resets `progress` and deletes
     warrant
   - **With bConvertToInfinite** - converts to `gc_obj_order_produce_infinite`
     (the order will continue indefinitely).
4. **Refund**: if the order has been “paid” (`amount > 0` or
   `progress > 0`) - returns to the player:
   ```
   refund[k] = price[k] × (costpercent / 100)^(restype + i)
   ```
That is, exactly as much as was written off at the time of order.

Refund is valid **1 unit per call** - in the cycle `i:=0 to
Abs(amount)-1`. That is, canceling 5 pikemen will return exactly 5 prices,
each with a current `costmodifier` for its position in the counter.

---

<a id="5-прерывание-производства-захватчиками"></a>
## 5. Interruption of production by invaders

`_unit_CheckCapturersStopProduce(goHnd)` [^6] is called every
tick of progress. Algorithm:

1. Takes `scangridx`, `scangridy` buildings and expands to `rx1 = 1`
   scan-grid cell in each direction.
2. In cells with `enemyplmask` enabled, searches for enemy
   `bcancapture`-unit via `_unit_SearchCapturers`.
3. If found, checks whether it has a `bprotector` protector
   nearby. If there is **no** defender, it returns `True`, and
   production in this tick **does not progress**.

**Special case:** walls (`bwall`-buildings). If the HP of the wall is lower
third `maxhp`, the check is skipped - the wall has almost been destroyed,
it makes sense to complete it to the end.

Effect: a cavalry raid on a barracks not only captures it, but also
**freezes production** even before the capture. Defender
(`bprotector`) nearby removes the freeze.

---

<a id="6-захват-здания-с-очередью"></a>
## 6. Capture buildings with a queue

When `_misc_ChangePlayer` (capture) the building has all orders for
production and upgrades:

1. Run through `_unit_CancelUnitProduction(... bState=False)`
   and `_unit_CancelUpgradePerform` respectively.
2. Resources are returned to the **previous** owner (via `bProcess`
   check), not new.
3. The new owner’s queue starts empty - he can immediately
   place your orders.

This means: **by capturing the enemy barracks, you will not get it
orders automatically**. If you want to continue to rivet the same
units, you need to place your orders. But: ** back to the previous owner
will receive a refund** - this is already an investment in the “controversial” building, which
you won't get it.

---

<a id="7-снос-здания-с-очередью"></a>
## 7. Demolition of a building with a queue

When `bDie := True` or `hp <= 0` `OnDeath` the hook also runs through all
queue via cancel function [^7]. That is, **destruction of one's own
barracks returns resources** during production.

In practice, a rare case: if AI or a trap destroys your
working barracks, you get back the cost of unproduced
units. This mitigates the damage from the raid.

---

<a id="8-очередь-апгрейдов"></a>
## 8. Upgrade queue

In parallel with production, the building can hold orders like
`gc_obj_order_type_performupgrade = 8` via `_unit_OrderUpgrade`.
The semantics are similar:

- The same upgrade **cannot** be ordered twice (check via
  `gPlayer[pl].upgstate[cid][upgind]`).
- Cancel returns the base cost of the upgrade (without
  `costpercent`-scaling - upgrades do not have it).
- Completing the research applies the effect and deletes the order.

More details in [`upgrades_application.md`](upgrades_application.md).

---

<a id="9-ui-ограничения"></a>
## 9. UI restrictions

In addition to the technical `MaxOrderCount = 12`, the player sees buildings in the UI
**five or six slots** queue. Exceeding is prohibited for
GUI level: the “order more” button becomes inactive. This
provides reserve for repair orders / simplifies visualization
progress bar.

The exact UI logic is in `lib/gui.script`, not in the production logic.

---

<a id="10-открытые-эмпирические-вопросы"></a>
## 10. Open empirical questions

1. **Exact progress rate.** `info.progress += delta` —
   `delta` proportional `buildtime_modifier × deltatime` plus
   difficulty multiplier (for AI - `0.30 / 0.50 / 0.75 / 1.00 / 1.25`,
   see [`../../systems/ai_behavior.md`](../../systems/ai_behavior.md)).
   The exact coefficients are not subtracted from the code.
2. **How many slots are real in the UI at different window sizes.**
   on a wide screen it can be 7-8, on a standard screen - 5. Measure.
3. **Production blocking upon capture - for how long?
   ticks no progress?** One tick “invader found” or the whole
   period while he is in radius?

---

<a id="источники"></a>
## Sources

[^1]: `data/scripts/dmscript.global` — `gc_obj_MaxOrderCount = 12`,
      `gc_obj_order_type_*` enum (`produce = 4`,
      `performupgrade = 8`, etc.),
      `gc_obj_order_produce_infinite = -1`. `TOrder` - definition
      entries in `lib/classes.script`.

[^2]: `_unit_OrderProduce` - `lib/unit.script`. Merge logic
      orders via `costpercent` and `unitcount = restype` - see.
      code author's comment: `// restype stores amount of units,
      that we had at the moment of ordering produce. it is needed
      to properly give player moneyback, when unit costpercent is
      different from 100%, when player cancel unit production.`

[^3]: `_unit_AddOrder` - `lib/unit.script`. Places an order in
      the first free cell `orders[i]`.

[^4]: `_unit_CancelUnitProduction` - `lib/unit.script:5891-5977`.
      The `bConvertToInfinite` parameter controls the behavior when
      `amount = 0`.

[^5]: `_unit_ProduceUnit` - `lib/unit.script:10351`. Distributes
      production of several buildings of the same type through
      selecting the minimum `produceind`.

[^6]: `_unit_CheckCapturersStopProduce` - `lib/unit.script` (see.
      See also the section on `bcancapture` in [`capture_mechanics.md`](capture_mechanics.md)).

[^7]: `OnDeath` building hook - `data/scripts/units/building.inc/ondeath.inc:11-25`.
      Scrolls through all `produce`/`performupgrade` orders through
      cancel function with `bState = False`.
