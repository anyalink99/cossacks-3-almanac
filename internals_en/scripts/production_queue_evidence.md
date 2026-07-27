<a id="recon-очередь-производства"></a>
<a id="очередь-производства"></a>
<a id="технический-разбор-очереди-производства"></a>
# Technical Evidence for Production Queues

[← Scripts and Scenarios](structure.md)

[Reader-facing production queue article](../../docs_en/recon/world/economy/production_queue.md)

An analysis of production queues in Barracks, Academies, Stables,
and Town Halls: repeated orders, infinite production, cancellation,
capture, and demolition. Code references are collected under
[Sources](#sources).

> **Related documents:**
> [Building Construction, Repair, and Destruction §6.3](../../docs_en/recon/world/economy/building_mechanics.md) — resource refunds after
> cancellation/destruction; [How Upgrades Are Applied §3](../../docs_en/recon/world/economy/upgrades_application.md)
> — upgrade research;
> [Unit Orders](../../docs_en/recon/world/combat/unit_commands.md) — the
> general order model used by units.

<a id="коротко-о-главном"></a>
## In brief

- A building can hold up to **12 simultaneous orders** (technical
  limit `gc_obj_MaxOrderCount`) [^1]. This total is shared by
  production, upgrades, repairs, and other actions.
- Each production order is stored in a `TOrder` record with
  `produceid` (the produced unit's internal ID), `amount` (units remaining),
  `progress` (progress of the current unit), and `restype` (the count
  of completed copies **when the order was placed**, preserving the correct
  `costpercent` tier for a refund).
- `amount = -1` (`gc_obj_order_produce_infinite`) means
  **infinite production**: the building keeps producing until the player
  cancels the order.
- **A repeated order for the same unit merges with the existing one**.
  For example, new Austrian Peasants (`peaaus`) are added to the
  open order when `costpercent` is `100` or `0`.
- If the unit price changes after each completed copy
  (`costpercent` is neither `100` nor `0`),
  orders merge only while `unitcount = restype`, meaning that no additional
  unit of that type was completed between the two orders.
- **A nearby enemy capturer stops production.** If an enemy unit
  capable of capturing (`bcancapture`) approaches and no defender
  (`bprotector`) is nearby, the building **stops** processing the order.
- When a building is destroyed, its queue is canceled and the resources
  spent on unfinished units and upgrades are refunded (see
  [Building Construction, Repair, and Destruction §6.2](../../docs_en/recon/world/economy/building_mechanics.md)).

---

<a id="1-структура-ордера-на-производство"></a>
<a id="1-как-хранится-заказ-на-производство"></a>
## 1. How a production order is stored

`TOrder` is an entry in the
`TObj.orders[0..gc_obj_MaxOrderCount-1]` array [^1].
Fields for type `gc_obj_order_type_produce = 4`:

| Field | What |
|---|---|
| `itype` | Order type. `4` means unit production. See §1.1 for the complete list. |
| `info.produceid` | Internal ID of the unit being produced. |
| `info.amount` | Remaining quantity; `-1` (`gc_obj_order_produce_infinite`) means infinite production. |
| `info.progress` | Progress of the current instance (`0..buildtime`). |
| `info.restype` | Number of completed copies **when the order was placed**. `_unit_CancelUnitProduction` uses it to preserve the same `costpercent` tier; if the base price has since changed, the refund changes too. |

<a id="11-все-типы-ордеров-gcobjordertype"></a>
<a id="11-все-типы-приказов-gc_obj_order_type_"></a>
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
3. **If the merge conditions in §2.1 are met,** increases the existing
   order's `amount`.
4. **If none is found**, adds a new order to the first free slot
   through `_unit_AddOrder` [^3].
5. If all 12 slots are occupied, the order is silently discarded.

<a id="21-условия-слития-ордера"></a>
<a id="21-когда-заказы-объединяются"></a>
### 2.1. When orders merge

The game merges a new quantity into an existing order when:

- **`costpercent = 100`** — price does not increase, so orders always merge.
- **`costpercent = 0`** (special “no scaling”) —
  also merges.
- **`unitcount = order.restype`** — no unit of this type has completed
  since the earlier order, so its saved refund tier remains valid.

Otherwise the game creates a **separate** order with the current
`restype = unitcount`. This preserves the correct refund tier: after
several increasingly expensive units have completed, an older
`costmodifier` would select the wrong tier. Cancellation reads the base price
again, so a `priceperc` upgrade completed after ordering changes the refund
amount.

<a id="22-бесконечный-режим"></a>
### 2.2. Infinite production

`amount = gc_obj_order_produce_infinite = -1` means “continue until
explicitly canceled.” If `_unit_OrderProduce` finds an existing infinite
order and receives a finite request for the same unit, the finite request is
ignored because the infinite order already covers it.

The inverse operation appears in `_unit_CancelUnitProduction` with
`bConvertToInfinite = True` [^4]: when the finite amount reaches zero or
one, the command can convert the entry into an infinite order.

---

<a id="3-прогресс-и-завершение"></a>
## 3. Progress and completion

Each game tick, `_unit_DoOrderProgress` increases `info.progress` by
`deltatime × buildtime_modifier`. When `progress >= buildtime`:

1. A unit is created via `_unit_ProduceUnit` [^5].
2. The unit appears at the building's rally point (`rallypoint`), or
   at its entrance if no rally point is set.
3. `info.amount -= 1`. If it becomes 0, the order is completed and deleted.
4. If `amount = -1`, the infinite order remains active.

`_unit_ProduceUnit` distributes production **among several buildings of the
same type**. If the selected group contains multiple Barracks, it chooses the
one with the lowest `produceind`, representing the least-loaded production
queue. A shared order such as twenty Pikemen is therefore spread across the
selected Barracks.

---

<a id="4-отмена-заказа"></a>
## 4. Order cancellation

`_unit_CancelUnitProduction(goHnd, cid, unitID, amount, bConvertToInfinite)` [^4]:

1. Finds an order with the required `produceid`.
2. Decreases `info.amount` by the requested quantity; an ordinary interface
   click cancels one copy.
3. If the remaining `info.amount` reaches 0:
   - **Without `bConvertToInfinite`**, resets `progress` and deletes the
     order.
   - **With `bConvertToInfinite`**, converts it to `gc_obj_order_produce_infinite`
     (the order will continue indefinitely).
4. **Resource refund**: if the order has been paid (`amount > 0` or
   `progress > 0`), the game returns:
   ```
   refund[k] = floor(current_price[k] × (costpercent / 100)^restype)
   ```
   The calculation applies the same modifier caps used when the order is
   placed.

The loop `i := 0 to Abs(amount)-1` calculates a separate refund for every
canceled copy, but `i` does not enter the formula: every copy in one queue
entry has the same saved `restype`. The game cancels the newest matching
entries first and may then cross into older entries with a different
`restype`. This is why a request made after the completed-unit count changes
must create a separate queue entry.

---

<a id="5-прерывание-производства-захватчиками"></a>
## 5. Production blocked by a nearby capturer

`_unit_CheckCapturersStopProduce(goHnd)` [^6] is called every
tick of progress. Algorithm:

1. Takes the building's spatial-grid coordinates (`scangridx`,
   `scangridy`) and includes one adjacent cell in every direction.
2. In cells covered by `enemyplmask`, searches for an enemy unit with
   `bcancapture` through `_unit_SearchCapturers`.
3. If a capturer is found, searches for a friendly `bprotector`. Without
   such a defender, the function returns `True` and production makes no
   progress during that tick.

**Special case:** if a Wall is below one-third of `maxhp`, this check is
skipped.

A cavalry raid can therefore **freeze production** at a Barracks even though
a completed Barracks cannot itself be captured. A nearby defender with
`bprotector` removes the block.

---

<a id="6-захват-здания-с-очередью"></a>
## 6. Capturing a building with a queue

When `_misc_ChangePlayer` captures a building, it processes every production
and research order:

1. Run through `_unit_CancelUnitProduction(... bState=False)`
   and `_unit_CancelUpgradePerform` respectively.
2. Resources return to the **previous** owner, not the capturer.
3. The new owner's queue starts empty.

The capturer never inherits nearly completed units or research. New orders
must be placed after ownership changes.

---

<a id="7-снос-здания-с-очередью"></a>
## 7. Destroying a building with a queue

When `bDie := True` or `hp <= 0`, the `OnDeath` handler passes every queue
entry through the relevant cancellation function [^7]. Destroying one's own
Barracks therefore refunds unfinished production.

The same applies when an enemy or scenario effect destroys the building:
resources spent on unfinished units return to the owner.

---

<a id="8-очередь-апгрейдов"></a>
<a id="8-очередь-улучшений"></a>
## 8. Upgrade queue

In parallel with production, the building can hold orders like
`gc_obj_order_type_performupgrade = 8` via `_unit_OrderUpgrade`.
The semantics are similar:

- The same upgrade **cannot** be ordered twice (check via
  `gPlayer[pl].upgstate[cid][upgind]`).
- Cancellation returns the upgrade's base cost; upgrades do not use
  `costpercent` scaling.
- Completing the research applies the effect and deletes the order.

More details in [How Upgrades Are Applied](../../docs_en/recon/world/economy/upgrades_application.md).

---

<a id="9-ui-ограничения"></a>
<a id="9-ограничения-интерфейса"></a>
## 9. Interface limits

Although `MaxOrderCount = 12`, the visible building queue commonly shows
**five or six entries**. The count varies with window size and interface
scale. The hidden capacity also leaves room for service actions such as
repair.

The exact UI logic is in `lib/gui.script`, not in the production logic.

---

<a id="10-открытые-эмпирические-вопросы"></a>
## 10. Open empirical questions

1. **Exact progress rate.** `info.progress += delta` —
   `delta` is proportional to `buildtime_modifier × deltatime`, with an
   additional AI difficulty multiplier (`0.30 / 0.50 / 0.75 / 1.00 / 1.25`;
   see [How the Computer Player Works](../../docs_en/recon/systems/ai_behavior.md)).
   The remaining coefficients still need to be traced.
2. **How many queue slots are visible at different window sizes?**
   Measure wide and standard layouts; current estimates range from five
   to eight.

---

<a id="источники"></a>
## Sources

[^1]: `data/scripts/dmscript.global` — `gc_obj_MaxOrderCount = 12`,
      `gc_obj_order_type_*` enum (`produce = 4`,
      `performupgrade = 8`, etc.),
      and `gc_obj_order_produce_infinite = -1`. `TOrder` is defined in
      `lib/classes.script`.

[^2]: `_unit_OrderProduce` — `lib/unit.script`. Its merge logic uses
      `costpercent` and `unitcount = restype`, as explained by the source
      comment:

      ```pascal
      // restype stores amount of units,
      // that we had at the moment of ordering produce. it is needed
      // to properly give player moneyback, when unit costpercent is
      // different from 100%, when player cancel unit production.
      ```

[^3]: `_unit_AddOrder` — `lib/unit.script`. Places an order in
      the first free cell `orders[i]`.

[^4]: `_unit_CancelUnitProduction` — `lib/unit.script:5891-5977`.
      The `bConvertToInfinite` parameter controls the behavior when
      `amount = 0`.

[^5]: `_unit_ProduceUnit` — `lib/unit.script:10351`. Distributes
      production among several buildings of the same type by selecting the
      lowest `produceind`.

[^6]: `_unit_CheckCapturersStopProduce` — `lib/unit.script`. See also
      the `bcancapture` discussion in
      [building capture](../../docs_en/recon/world/economy/capture_mechanics.md).

[^7]: Building `OnDeath` handler —
      `data/scripts/units/building.inc/ondeath.inc:11-25`. It passes every
      `produce` and `performupgrade` order to the relevant cancellation
      function with `bState = False`.
