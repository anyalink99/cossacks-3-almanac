<a id="recon-очередь-производства"></a>
<a id="очередь-производства"></a>
# Production Queues

[← How the game works](../../README.md)

An analysis of production queues in Barracks, Academies, Stables,
and Town Halls: repeated orders, infinite production, cancellation,
capture, and demolition. Code references are collected under
[Sources](#sources).

> **Related documents:**
> [`building_mechanics.md` §6.3](building_mechanics.md) - resource refunds after
> cancellation/destruction; [`upgrades_application.md` §3](upgrades_application.md)
> - the separate upgrade queue;
> [`unit_commands.md`](../combat/unit_commands.md) - general model
> orders on units (also uses `gOrders`).

<a id="коротко-о-главном"></a>
## In brief

- A building can hold up to **12 simultaneous orders** (technical
  limit `gc_obj_MaxOrderCount`) [^1]. This total is shared by
  production, upgrades, repairs, and other actions.
- Each production order is stored in a `TOrder` record with
  `produceid` (the produced unit's internal ID), `amount` (units remaining),
  `progress` (progress of the current instance), `restype` (counter
  of completed copies **when the order was placed**, used to calculate
  an exact refund).
- `amount = -1` (`gc_obj_order_produce_infinite`) means
  **endless mode** - the building produces a unit until the order is
  will be canceled obviously.
- **A repeated order for the same unit merges with the existing one**.
  For example, new Austrian Peasants (`peaaus`) are added to the
  open order when `costpercent` is `100` or `0`.
- If the unit price changes after each completed copy
  (`costpercent` is neither `100` nor `0`),
  the merge occurs only if `unitcount = restype` - that is
  the player did not have time to build other units of the same type between
  orders.
- **A nearby enemy capturer stops production.** If an enemy unit
  capable of capturing (`bcancapture`) approaches and no defender
  (`bprotector`) is nearby, the building **stops** processing the order.
- When a building is demolished, all orders are scrolled back - paid
  units and upgrades are returned to the player (see.
  [`building_mechanics.md` §6.2](building_mechanics.md)).

---

<a id="1-структура-ордера-на-производство"></a>
<a id="1-как-хранится-заказ-на-производство"></a>
## 1. How a production order is stored

`TOrder` — entry in the `TObj.orders[0..gc_obj_MaxOrderCount-1]` [^1] array.
Fields for type `gc_obj_order_type_produce = 4`:

| Field | What |
|---|---|
| `itype` | Order type. `4` means unit production. See §1.1 for the complete list. |
| `info.produceid` | Internal ID of the unit being produced. |
| `info.amount` | How much more to produce? `-1` (`gc_obj_order_produce_infinite`) = infinite. |
| `info.progress` | Progress of the current instance (`0..buildtime`). |
| `info.restype` | Number of completed copies **when the order was placed**. `_unit_CancelUnitProduction` uses it to return the correct amount when `costpercent ≠ 100`. |

<a id="11-все-типы-ордеров-gcobjordertype"></a>
<a id="11-все-типы-приказов-gcobjordertype"></a>
### 1.1. All order types (`gc_obj_order_type_*`)

| ID | Player action | Technical name |
|---:|---|---|
| 0 | Empty queue slot | `none` |
| 1 | Move to a point | `move` |
| 2 | Attack a selected object | `attackobj` |
| 3 | Gather a resource | `gainres` |
| 4 | **Produce a unit** | `produce` |
| 5 | Patrol | `patrol` |
| 6 | Fire at a point | `attackpoint` |
| 7 | Continue firing at a point | `continueattackpoint` |
| 8 | **Research an upgrade** | `performupgrade` |
| 9 | Fish | `fishing` |
| 10 | Create a gate | `creategates` |
| 11 | Continue building a wall | `buildwallcontinue` |
| 12 | Build a wall | `buildwall` |
| 13 | Enter a Mine | `gotomine` |
| 14 | Board a transport ship | `gototransport` |
| 15 | Leave a transport ship | `leavetransport` |
| 16 | Leave a building | `leavebuilding` |
| 17 | Construct a building | `build` |
| 18 | Guard | `guard` |
| 19 | Repair | `repair` |
| 20 | Release everyone from a building | `exitunits` |

**Twelve orders is the shared limit**: a building may hold, for
example, five production orders, two upgrades, and one repair order
at the same time. A combat unit normally uses only actions such as
`move`, `attack`, and `guard`, but the underlying limit is the same.

---

<a id="2-добавление-ордера-в-очередь"></a>
<a id="2-добавление-заказа-в-очередь"></a>
## 2. Adding a production order

`_unit_OrderProduce(goHnd, ordercid, orderid, amount)` [^2]:

1. Scans existing orders from the end (`MaxOrderCount-1
   downto 0`).
2. Searches for an existing order of the same `produceid`.
3. **If found and the merging conditions are suitable** (see §2.1) - increases
   `amount` of an existing order.
4. **If none is found**, adds a new order to the first free slot
   through `_unit_AddOrder` [^3].
5. If all 12 slots are occupied, the order is silently discarded.

<a id="21-условия-слития-ордера"></a>
<a id="21-когда-заказы-объединяются"></a>
### 2.1. When orders merge

Orders are merged (new units are added to existing ones `amount`)
if:

- **`costpercent = 100`** (price does not increase) - always merges.
- **`costpercent = 0`** (special “no scaling”) —
  also merges.
- **`unitcount = order.restype`** - the player has not yet built any
  one unit of this type after the first order. Then `costmodifier`
  used for the refund remains valid, so merging is safe.

Otherwise the game creates a **new** order with the current
`restype = unitcount`. This preserves the correct refund: after
several increasingly expensive units have completed, an older
`costmodifier` would return the wrong amount.

<a id="22-бесконечный-режим"></a>
### 2.2. Endless Mode

`amount = gc_obj_order_produce_infinite = -1` means "continue"
until explicit cancellation." When `_unit_OrderProduce` meets
existing endless order and a request comes with a specific
number (`amount > 0`) - a specific order **ignored** (inside
infinite and so everything will happen).

Mirror semantics in `_unit_CancelUnitProduction` with
`bConvertToInfinite = True` [^4]: one cancelable unit from the final
order can **turn it** into an infinite one (if `amount`
reached 0 or 1).

---

<a id="3-прогресс-и-завершение"></a>
## 3. Progress and completion

Each game tick function `_unit_DoOrderProgress` (located in
`units/global.inc` or similar) increases `info.progress` by
`deltatime × buildtime_modifier`. When `progress >= buildtime`:

1. A unit is created via `_unit_ProduceUnit` [^5].
2. The unit appears at the building's rally point (`rallypoint`), or
   at its entrance if no rally point is set.
3. `info.amount -= 1`. If it becomes 0, the order is completed and deleted.
4. If `amount = -1` (infinite) - the order continues.

`_unit_ProduceUnit` distributes production **over several
buildings of the same type**: if the internal `list` contains several Barracks, it selects
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
     order.
   - **With bConvertToInfinite** - converts to `gc_obj_order_produce_infinite`
     (the order will continue indefinitely).
4. **Resource refund**: if the order has been paid (`amount > 0` or
   `progress > 0`), the game returns:
   ```
   refund[k] = price[k] × (costpercent / 100)^(restype + i)
   ```
That is, exactly as much as was written off at the time of order.

The refund is calculated **one unit per call** in the loop `i:=0 to
Abs(amount)-1`. That is, canceling 5 pikemen will return exactly 5 prices,
each with a current `costmodifier` for its position in the counter.

---

<a id="5-прерывание-производства-захватчиками"></a>
## 5. Interruption of production by invaders

`_unit_CheckCapturersStopProduce(goHnd)` [^6] is called every
tick of progress. Algorithm:

1. Takes the building's spatial-grid coordinates (`scangridx`,
   `scangridy`) and includes one adjacent cell in every direction.
2. In cells with `enemyplmask` enabled, searches for enemy
   `bcancapture`-unit via `_unit_SearchCapturers`.
3. If found, checks whether it has a `bprotector` protector
   nearby. If there is **no** defender, it returns `True`, and
   production in this tick **does not progress**.

**Special case:** Walls (flag `bwall`). If the Wall's durability is below
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
receives the resources back**; the capturer never inherits the old queue.

---

<a id="7-снос-здания-с-очередью"></a>
## 7. Demolition of a building with a queue

When `bDie := True` or `hp <= 0` `OnDeath` the hook also runs through all
queue through the cancellation functions [^7]. Thus **destroying one's own
barracks returns resources** during production.

In practice, a rare case: if AI or a trap destroys your
working barracks, you get back the cost of unproduced
units. This mitigates the damage from the raid.

---

<a id="8-очередь-апгрейдов"></a>
<a id="8-очередь-улучшений"></a>
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
<a id="9-ограничения-интерфейса"></a>
## 9. Interface restrictions

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
      code author's comment:

      ```pascal
      // restype stores amount of units,
      // that we had at the moment of ordering produce. it is needed
      // to properly give player moneyback, when unit costpercent is
      // different from 100%, when player cancel unit production.
      ```

[^3]: `_unit_AddOrder` - `lib/unit.script`. Places an order in
      the first free cell `orders[i]`.

[^4]: `_unit_CancelUnitProduction` - `lib/unit.script:5891-5977`.
      The `bConvertToInfinite` parameter controls the behavior when
      `amount = 0`.

[^5]: `_unit_ProduceUnit` - `lib/unit.script:10351`. Distributes
      production of several buildings of the same type through
      selecting the minimum `produceind`.

[^6]: `_unit_CheckCapturersStopProduce` - `lib/unit.script` (see.
      See also the section on `bcancapture` in [building capture](capture_mechanics.md)).

[^7]: `OnDeath` building hook - `data/scripts/units/building.inc/ondeath.inc:11-25`.
      Scrolls through all `produce`/`performupgrade` orders through
      cancel function with `bState = False`.
