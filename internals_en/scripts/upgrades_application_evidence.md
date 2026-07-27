<a id="recon-применение-апгрейдов"></a>
<a id="как-применяются-улучшения"></a>
<a id="технический-разбор-применения-улучшений"></a>
# Technical Evidence for Upgrade Application

[← Scripts and Scenarios](structure.md)

[Reader-facing upgrade article](../../docs_en/recon/world/economy/upgrades_application.md)

This article explains how an upgrade is applied to units and
buildings after research: where effects are stored, whether research
can be canceled, how efficiency (`eff`) is combined, and what
happens on a second research attempt. Code references are collected
under [Sources](#sources).

> Canonical upgrade names and parameters (prices, bonuses, requirements) are in
> the [upgrade reference](../../docs_en/reference/05_upgrades/README.md).
> This article covers the **application process**.

<a id="коротко-о-главном"></a>
## In brief

- Upgrades are stored in `country.upgrade[1..N]`, an array of records
  containing `cost`, `time`, `prerequisites`, targets, and effects [^1].
- Upgrade targets (`targets`) are internal IDs of units or buildings to which
  the effect applies. For example, gathering-efficiency upgrades at the Mill
  (`mil.X`) target the nation's Peasants, while Academy (`aca.X`) targets vary
  by research and may include military units, ships, buildings, or economic
  properties.
- Effects apply **immediately** to **existing** units and buildings.
  A Food-efficiency upgrade researched at the Mill affects every
  Peasant already on the map as soon as research completes.
- Gathering-efficiency effects are **additive**, not multiplicative. For example,
  `eff = 100 + 5 + 10 + 15 = 130 %`, not `1.05 × 1.10 × 1.15`.
- Research **can be canceled** through the building interface.
  The full base cost is refunded, and no effect is applied.
- `priceperc` upgrades reduce the price of future orders, but do **not**
  refund the difference for orders already placed.
- `buildtimeperc` upgrades immediately accelerate both new and ongoing
  construction or training.

---

<a id="1-как-хранится-апгрейд"></a>
<a id="1-как-хранится-улучшение"></a>
## 1. How the upgrade is stored

In `lib/country.script` an array is defined for each nation
`country.upgrade[ind]` (ind = 1..N) with fields [^1]:

| Field | What |
|---|---|
| `sid` | String identifier (`mil.1`, `aca.4`, `bla.2` ...). |
| `cost` | Cost in Food, Wood, Stone, Gold, Iron, and Coal. |
| `time` | Research time in frames (`frames`; 1/32 game second). |
| `prerequisites` | Internal IDs of required upgrades or buildings. |
| `targets` | Internal IDs of units and buildings that receive the effect. |
| `effect` | What changes (value, field). |
| `cid` | Country identifier. |

At a high level, effects include:

- **Numerical increases** to unit fields (`hp += 50`, `damage += 2`).
- **Percentage changes** such as a 25% construction-time reduction.
- **Efficiency bonuses** such as +10% resource gathering.

`parser/simulate_upgrades.py` performs the full expansion (see
[Structure of the Cossacks 3 scripting environment](structure.md)),
which inlines `SetUpgStruct`/`AddUpgradePack` and produces 4,483
fully resolved upgrade records.

---

<a id="2-когда-применяется-эффект"></a>
## 2. When the effect is applied

The effect is applied when research reaches completion. At that moment,
`_country_DoUpgrade(plInd, upgrade_ind)` [^2]:

1. Marks the upgrade as “purchased” in `gPlayer[plInd].upgrades[]`.
2. Iterates over the upgrade's `targets`.
3. For each target, applies the effect **immediately**:
   - For existing objects, updates the relevant `objbase`/`objprop` values.
   - For future objects, updates the template in `gObjProp[cid][id]`.

A Mill Food-efficiency upgrade therefore applies to **all 18
Peasants on the map** at the same time.

<a id="21-эффект-на-уже-в-работе"></a>
### 2.1. Effect on work already in progress

| Type | Apply to a process already in progress? |
|---|---|
| `eff += X %` | Yes; the next delivered portion uses the new efficiency. |
| `hp += X` | Yes, a living unit's HP increases (and `maxhp` too). |
| `damage += X` | Yes; the next attack uses the new damage. |
| `buildtimeperc` (construction or training) | **Yes**; the active process reads the changed base duration on its next progress update. |
| `priceperc` (price) | **No**, already ordered units do not become cheaper. |

Object attributes and duration change immediately. Price, by contrast, is
fixed when an order is placed.

---

<a id="3-прерывание-апгрейда"></a>
<a id="3-прерывание-исследования"></a>
## 3. Canceling research

The player can cancel ongoing research through the interface of the
building conducting it:

1. Research time is reset.
2. **100% of the base cost** is refunded.
3. A slot in the building queue becomes free.
4. The effect **does not apply** (since the end point was not
   achieved).

Cancellation lets the player react to changing priorities:
if an expensive upgrade is underway when the base comes under attack,
the player can cancel it, recover the full base cost, and redirect those
resources to defense.

---

<a id="4-аддитивная-композиция-eff"></a>
<a id="4-как-складывается-эффективность-eff"></a>
## 4. How efficiency (`eff`) is combined

Unlike many real-time strategy games, Cossacks 3 combines efficiency
bonuses **additively**:
```
eff(resource, Peasant) =
    100 + Σ(completed effectfood/effectwood/effectstone[perc]
            bonuses for the selected resource)
```
Food bonuses include, for example, `mil.1`, `mil.2`, and `aca.1..3`;
`aca.8` affects Wood, while `aca.23` and `aca.24` affect Stone. For four
notional bonuses worth +5/+10/+15/+20:

`eff = 100 + 5 + 10 + 15 + 20 = 150 %`. The base Food portion
of 45 becomes `floor(45 × 150 / 100) = 67`.

This is **not** multiplicative: it would be `1.05 × 1.10 × 1.15 × 1.20 = 1.59`
(159%), which is higher. The additive scheme gives a more predictable
final ceiling.

See [How Peasants Gather Resources](../../docs_en/recon/world/economy/peasant_extraction.md) for details.

---

<a id="5-цели-апгрейда-targets"></a>
<a id="5-цели-улучшения-targets"></a>
## 5. Upgrade targets (`targets`)

`targets` determines **who** the upgrade applies to. Possible
values:

| Technical template | Affected objects |
|---|---|
| `'peaXXX'` | A specific internal ID (for example, Austrian Peasant: `peaaus`). |
| `'BuildingsAll'` | Every building of the nation (hard-coded group). |
| `'UnitsAll'` | Every unit of the nation (hard-coded group). |
| `'<class>'` | All units of the class (`musket18`, `pike17`, ...). |
| List | Several internal IDs separated by a delimiter. |

Additional parameters support complex economic effects:
- `sarrparam2[gc_resource_type_X]` stores a separate `priceperc`
  percentage for each resource.
- `targets = 'BuildingsAll'` applies a `buildtimeperc` effect to every
  eligible national building.

---

<a id="6-priceperc-и-buildtimeperc"></a>
## 6. `priceperc` and `buildtimeperc`

Two upgrade types modify economic actions:

### 6.1. `priceperc`

Reduces the price of future orders by N%. The modifier is stored separately
for Food, Wood, Stone, Gold, Iron, and Coal. An artillery discount may reduce
the Gold and Iron components while leaving the other resources unchanged.

In `data.json` it is represented as:
```
upgrade.resource_pcts[restype] = pct
```
### 6.2. `buildtimeperc`

Reduces the time to **build buildings** or **recruit units**. The raw `value`
stores a negative percentage scaled by 100,000: for example, −25% is stored
as `−2500000`.

Used as:
```
buildtime_new = buildtime_base × (1 + value / (100 × 100000))
```
When research finishes, `_player_ApplyUpgrade` immediately changes
`buildtime` in the player's object template. A production queue reads that
live value on every progress update, while construction reads it on every
builder strike. The upgrade therefore accelerates both ongoing recruitment
and unfinished buildings immediately [^bt].

---

<a id="7-лимиты-и-переисследование"></a>
## 7. Research limits and upgrade chains

In the standard game, each upgrade can be researched **once**. After
completion:

- The upgrade button disappears from the UI.
- `gPlayer[plInd].upgrades[upgrade_ind] := True`.
- The interface prevents another purchase.

Successive levels such as `aca.1`, `aca.2`, and `aca.3` are
**separate records** in `country.upgrade[]`. Each is researched once and
their effects combine:
`eff(food) = 100 + aca.1(+40) + aca.2(+50) + aca.3(+50) = 240 %`.

`uniqupgrade` entries target a specific internal object rather than a class.

---

<a id="75-эпохальный-переход-17--18-век"></a>
## 7.5. Advancing from the 17th to the 18th century

Advancement is the canonical **Progress to the 18th Century** upgrade in the
Town Hall (internal ID `<nat>cen.1`). It becomes available after the required
buildings are complete.

<a id="751-цепочка"></a>
### 7.5.1. Chain
```
Town Hall (SID `<nat>cen`) built
    + Academy (SID `<nat>aca`) built
    + Cathedral (SID `<nat>tem`) built
    + Artillery Depot (SID `<nat>art`) built
        ↓
research “Progress to the 18th Century” (SID `<nat>cen.1`) at the Town Hall
    cost ≈ 30,000 Food + 5,000 Gold + 2,000 Iron + 2,000 Coal
    time = 9.38 game sec
        ↓
you can now build the 18th-century Barracks (SID `<nat>ba2`)
    cost ≈ 1,700 Wood + 2,950 Stone + 4,000 Gold
    buildtime = 5625 game sec
        ↓
the Barracks produces Musketeers, Pikemen, Grenadiers, Dragoons,
and special national infantry of the 18th century
```
**The required buildings are the bottleneck**, not the upgrade itself.
The Town Hall, Academy, Cathedral, and Artillery Depot cost about
7,000 Wood, 4,000 Stone, and 1,000 Gold in total, excluding the Town
Hall already in place. A normal team of 6–8 builders cuts the long
single-builder construction time substantially.

<a id="752-кто-заперт-в-17-веке"></a>
### 7.5.2. Nations without 18th-century Barracks

Three nations have neither an available transition nor `<nat>ba2`:

| Nation | Available transition (`<nat>cen.1`) | 18th-century Barracks (`<nat>ba2`) | Result |
|---|:---:|:---:|---|
| Algeria (`alg`) | ❌ | ❌ | Remains in the 17th century |
| Turkey (`tur`) | ❌ | ❌ | Remains in the 17th century |
| Ukraine (`ukr`) | ❌ | ❌ | Remains in the 17th century |

`data.json` contains records named `algcen.1`, `turcen.1`, and `ukrcen.1`,
but they do not describe upgrades available in a match: their `place` and
`member` fields are null, their prerequisite lists are empty, and `_source`
is empty. The generated technology tree does not contain these transitions
either. Availability is established by registration in the national upgrade
chain, not by the presence of a record with a matching internal identifier.

These nations therefore lack 18th-century Musketeers, Grenadiers, and Dragoons
(technically, units with suffix `18` or `kind = Grenadier`). They develop
unique 17th-century chains instead, including Janissaries, Mamelukes,
Cossacks, and other national units.

<a id="753-что-даёт-natcen1-для-апгрейдов-академии"></a>
<a id="753-что-даёт-natcen1-у-наций-с-переходом"></a>
### 7.5.3. Academy upgrades for nations with `<nat>cen.1`

For nations with an available transition, completing `<nat>cen.1` exposes
additional `<nat>aca.X` upgrades whose prerequisite is `cen.1`. The AI uses
`gc_ai_upg_century` to enter the corresponding late-game production phase;
see [How the Computer Player Works](../../docs_en/recon/systems/ai_behavior.md).

<a id="754-стратегические-выводы"></a>
### 7.5.4. Strategic conclusions

- **“Progress to the 18th Century” (`cen.1`) is cheap and fast.**
  Constructing the required buildings is the bottleneck.
- **The 18th-century Barracks (`ba2`) takes a long time to build.**
  Its base construction-time value is 5,625 game seconds. Actual time follows
  `buildtime × 1.13 / N` while all N builders have work positions (see
  [Building Construction, Repair, and Destruction §3.2](../../docs_en/recon/world/economy/building_mechanics.md)).
- **Turkey, Algeria, and Ukraine remain in the 17th century.** They have
  neither an available transition nor the 18th-century Barracks.
- **An Academy serves several purposes.** Economy and combat research also
  satisfies one prerequisite for Progress to the 18th Century.

---

<a id="76-математика-применения-порядок-и-комбинирование"></a>
## 7.6. Application mathematics: order and combination

In almost every branch, research order **does not affect** an object's final
attributes. This remains true when flat and percentage bonuses come from
different upgrades, even though ordinary step-by-step arithmetic would give
`(B + 5) × 1.25 ≠ B × 1.25 + 5`.

`_player_ApplyUpgrade` [^om1] accumulates each type of bonus in a
**separate field**
(`damagestatic`, `damagepercent`, `protection[kind]`, `shield`,
`resefficiency[*]`, and so on). It then recalculates the final value from the
unchanged base, such as `damageinit`, and the accumulated totals rather than
from the previous result.

<a id="761-урон-damage-flat-и-damage-"></a>
<a id="761-урон-постоянная-прибавка-damage-и-процент-damage-"></a>
### 7.6.1. Damage (flat `+damage` and percentage `+damage %`)

Three fields are stored: `damageinit` (base damage), `damagestatic` (the
sum of flat bonuses), and `damagepercent` (the sum of percentage bonuses).
`gc_upg_type_damage` [^om2] updates `damagestatic`, while
`gc_upg_type_damageperc` [^om3] updates `damagepercent`. Both branches
recalculate from the same base:
```
damage = floor((damageinit + Σflat) × (1 + Σ% / 100))
```
With base damage 10 and bonuses of +5 and +25%, both research orders produce
`floor((10 + 5) × 1.25) = 18`.

<a id="762-защита-protection-shield-оба-только-flat"></a>
<a id="762-защита-protection-shield-только-постоянные-прибавки"></a>
### 7.6.2. Protection (`protection`, `shield`; flat bonuses only)

Both fields use direct addition: `protection[kind] += value` and
`shield += value`. Order does not matter.

<a id="763-hp-юнита-lifeperc-"></a>
<a id="763-прочность-юнита-lifeperc-"></a>
### 7.6.3. Unit durability (`lifeperc`, %)

`maxhp = round(maxhp × (1 + value / 100))`. Multiplication is commutative,
although rounding after each step can produce a one-point difference.

<a id="764-эффективность-добычи-effectfoodwoodstone--perc"></a>
### 7.6.4. Gathering efficiency (`effectfood/wood/stone` + `…perc`)

The same array `resefficiency[res]` (base = 100). All four
variants (`flat` / `perc`) do **the same thing**:
```
resefficiency[res] := resefficiency[res] + round(value);
                                          // percentage variants also use += value, not *=
```
Every value is added, so order does not matter. Flat and percentage variants
are indistinguishable in this branch. The gathering formula later uses
`resefficiency / 100` in `_unit_GetPeasantResPortion`.

<a id="765-жизнь-поля-fieldlifeperc-"></a>
### 7.6.5. Field durability (`fieldlifeperc`, %)

`fieldlife += value`; bonuses are additive and order-independent.

<a id="766-время-постройки-buildtimeperc-"></a>
### 7.6.6. Construction time (`buildtimeperc`, %)

`buildtime *= (1 + value / (100 × 100000))`. Successive multipliers commute.
The `100 × 100000` divisor reflects the stored scale: −75% is represented as
`−7500000`.

<a id="767-скорострельность--дальность--разлёт-attpauseperc-attrangeperc-attdispertionperc"></a>
### 7.6.7. Rate of fire, range, and dispersion (`attpauseperc`, `attrangeperc`, `attdispertionperc`)

Each branch uses `field *= (1 + value / 100)`, so successive bonuses commute.

<a id="768-цена-priceperc-"></a>
### 7.6.8. Price (`priceperc`, %)

`price[j] = round(price[j] × (1 + value / 100))`. The multipliers commute,
but rounding after every step may produce a one-point difference between
orders. Multiple `priceperc` effects rarely overlap on one object.

<a id="769-рыболовство-fishingperc-"></a>
### 7.6.9. Fishing (`fishingperc`, %)

`fishingmax = round(fishingmax × (1 + value / 100))` has the same rounding
caveat. Standard data provides one such upgrade per boat.

<a id="7610-скорость-движения-speedperc---аномалия"></a>
### 7.6.10. Movement speed (`speedperc`, %): anomaly

`gc_upg_type_speedperc` [^om4] instead of the usual
`*= (1 + value / 100)` recalculates the field as
`speed := 1 / (speed × (1 + value / 100))`. Field `speed` is stored
as `1 / v` (reciprocal), and the operation inverts the value.
Two consecutive applications give
`V₀ × (1 + p₂) / (1 + p₁)`, which is **order-dependent**. Standard data
avoids the issue because each affected unit type has only one
`speedperc` upgrade (`aca.28`, ship speed +40%), and completed research
cannot be repeated.

<a id="7611-сводная-таблица"></a>
### 7.6.11. Summary table

| `itype` | Accumulation | Does it depend on the order? |
|---|---|---|
| `damage` (flat) | `damagestatic += val`, recalculation from `damageinit` | No |
| `damageperc` (%) | `damagepercent += val`, recalculation from `damageinit` | No |
| `protection`, `shield` | `+= val` | No |
| `lifeperc` (%) | `maxhp = round(maxhp × (1 + val/100))` | Rounding only (±1) |
| `effectfood/wood/stone[perc]` | `resefficiency += val` | No (flat and % are indistinguishable) |
| `fieldlifeperc` | `fieldlife += val` | No |
| `buildtimeperc` (%) | `*= (1 + val / (100 × 10⁵))` | No |
| `priceperc` (%) | `= round(· × (1 + val/100))` | Rounding only (±1) |
| `attpauseperc/rangeperc/dispertionperc` | `*= (1 + val/100)` | No |
| `fishingperc` (%) | `= round(· × (1 + val/100))` | Rounding only (±1) |
| `speedperc` (%) | `speed = 1 / (speed × (1 + val/100))` | **Yes, but there is only one upgrade in the data** |

<a id="7612-практический-вывод"></a>
### 7.6.12. Practical conclusion

For most simulations, upgrades can be represented as a set without tracking
research order. Sequence still matters to match timing and to prerequisite
chains that unlock Frigates, Ships of the Line, Multi-barrelled Cannons, and
other options.

The exceptions are successive rounding in `priceperc`, `lifeperc`, and
`fishingperc`, which can change the result by one point, and the
order-dependent `speedperc` formula. Standard data does not stack the latter
on one unit type.

---

<a id="8-tech-tree-и-prerequisites"></a>
<a id="8-дерево-технологий-и-требования"></a>
## 8. Technology tree and requirements

Each upgrade has requirements (`prerequisites`) that determine when
its button appears:

- A building, such as Housing (`hou`), Academy (`aca`), or Blacksmith (`bla`).
- Another upgrade, usually the preceding tier.
- The century: technical flag `century18` opens some upgrades only
  after the transition to the 18th century.

When all requirements are met, the upgrade **appears in the
interface** and becomes available for research.

The complete graph is in [Cossacks 3 - Tech Tree (by nation)](../../docs_en/reports/tech/tech_tree.md)
+ [`derived/tech_tree.json`](../../derived/tech_tree.json).

<a id="9-открытые-вопросы"></a>
## 9. Open questions

1. The complete set of cases in which successive rounding of price,
   durability, or fishing capacity changes the result by one point.

<a id="источники"></a>
## Sources

[^1]: `data/scripts/lib/country.script` — definition of
      `country.upgrade[]` via `SetUpgStruct` and `AddUpgradePack`.
      `parser/simulate_upgrades.py` inlines these macro wrappers and produces
      fully resolved upgrade records.

[^2]: `data/scripts/lib/country.script` — function
      `_country_DoUpgrade(plInd, ind)` or similar: applies
      effects when research completes. It iterates through `targets`
      and changes the corresponding fields in `objbase`/`objprop`/`gObjProp`.

[^bt]: `buildtimeperc` application — `lib/player.script:1845-1848`;
       live `buildtime` reads by production —
       `units/building.inc/doprogressorders.inc:217-232`, and by construction —
       `units/unit.inc/onaclanimationreachedconstruct.inc:26-27`.

[^om1]: `_player_ApplyUpgrade` — `lib/player.script:1707-1983`. All
        branches `gc_upg_type_*` are dispatched here; general template
        — update an accumulator field and recalculate the result from the
        unchanged base.

[^om2]: Branch `gc_upg_type_damage` — `lib/player.script:1764`:
        ```pascal
        damagestatic := damagestatic + round(value);
        damage := floor((damageinit + damagestatic) * (1 + damagepercent/100));
        ```
[^om3]: Branch `gc_upg_type_damageperc` — `lib/player.script:1783`:
        ```pascal
        damagepercent := damagepercent + round(value);
        damage := floor((damageinit + damagestatic) * (1 + damagepercent/100));
        ```
[^om4]: Branch `gc_upg_type_speedperc` — `lib/player.script:1930`:
        ```pascal
        speed := 1 / (speed * (1 + value/100));
        ```
