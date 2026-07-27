<a id="recon-применение-апгрейдов"></a>
<a id="как-применяются-улучшения"></a>
# How Upgrades Are Applied

[← How the game works](../../README.md)

This article explains how an upgrade is applied to units and
buildings after research: where effects are stored, whether research
can be cancelled, how efficiency (`eff`) is combined, and what
happens on a second research attempt. Code references are collected
under [Sources](#sources).

> Canonical upgrade names and parameters (prices, bonuses, requirements) are in
> [upgrades](../../../reference/05_upgrades/README.md). Here
> covers the **application process**.

<a id="коротко-о-главном"></a>
## In brief

- The upgrade is stored in `country.upgrade[1..N]` - an array of records with
  parameters `cost`, `time`, `prerequisites`, effects on the target [^1].
- Upgrade targets (`targets`) are internal IDs of units or buildings to which
  the effect applies. For example, Mill upgrades (`mill.X`) apply to
  the nation's Peasants, while Academy upgrades (`aca.X`) commonly
  target military units.
- Effects apply **immediately** to **existing** units and buildings.
  A Food-efficiency upgrade researched at the Mill affects every
  Peasant already on the map as soon as research completes.
- The effects are **additive**, not multiplicative. For example,
  `eff = 100 + 5 + 10 + 15 = 130 %`, not `1.05 × 1.10 × 1.15`.
- Research **can be cancelled** through the building interface.
  Part of the cost is returned (about 50% by default), and no effect
  is applied.
- `priceperc` upgrades reduce the price of future orders, but **not**
  They return the difference for those already built.
- `buildtimeperc` upgrades affect the time of **new** buildings /
  hiring, not for those already in progress.

---

<a id="1-как-хранится-апгрейд"></a>
<a id="1-как-хранится-улучшение"></a>
## 1. How the upgrade is stored

In `lib/country.script` an array is defined for each nation
`country.upgrade[ind]` (ind = 1..N) with fields [^1]:

| Field | What |
|---|---|
| `sid` | String identifier (`mill.1`, `aca.4`, `bla.2` ...). |
| `cost` | Cost in Food, Wood, Stone, Gold, Iron, and Coal. |
| `time` | Research time in frames (`frames`; 1/32 game second). |
| `prerequisites` | Internal IDs of required upgrades or buildings. |
| `targets` | Internal IDs of units and buildings that receive the effect. |
| `effect` | What changes (value, field). |
| `cid` | Country identifier. |

There are three types of effects:
- **Numerical increases** to unit fields (`hp += 50`, `damage += 2`).
- **Percentage** (`buildtimeperc -= 25 %` - buildings are built at 25%
  faster).
- **Efficiency** (`eff += 10 %` - resource extraction is 10% higher).

Full analysis - via `parser/simulate_upgrades.py` (see.
[Structure of the Cossacks 3 scripting environment](../../../../internals_en/scripts/structure.md)),
which inlines `SetUpgStruct`/`AddUpgradePack` and produces ~4,000
fully resolved strings.

---

<a id="2-когда-применяется-эффект"></a>
## 2. When the effect is applied

Each upgrade has a **completion point** - the moment when the player
paid, waited for `time`-seconds, and got the effect. At this moment
script `_country_DoUpgrade(plInd, upgrade_ind)` [^2]:

1. Marks the upgrade as “purchased” in `gPlayer[plInd].upgrades[]`.
2. Iterates through `targets` upgrade.
3. For each target, applies the effect **immediately**:
   - To existing units: changes their fields directly to `objbase`/`objprop`.
   - To future units: changes the “template” (`gObjProp[cid][id]`),
     from where units copy properties when created.

A Mill Food-efficiency upgrade therefore applies to **all 18
Peasants on the map** at the same time.

<a id="21-эффект-на-уже-в-работе"></a>
### 2.1. Effect on already-in-work

| Type | Apply to a process already in progress? |
|---|---|
| `eff += X %` | Yes, the next portion is already mined with a new eff. |
| `hp += X` | Yes, a living unit's HP increases (and `maxhp` too). |
| `damage += X` | Yes, the next blow will deal with new damage. |
| `buildtimeperc` (construction) | **No**, the ongoing construction is being completed with the old time. |
| `priceperc` (price) | **No**, already ordered units do not become cheaper. |

This is an important asymmetry: upgrades to "stats" are applied
immediately, upgrades to “processes” - only to new ones.

---

<a id="3-прерывание-апгрейда"></a>
<a id="3-прерывание-исследования"></a>
## 3. Cancelling research

The player can cancel ongoing research through the interface of the
building conducting it:

1. Research time is reset.
2. Part of the resources is returned (standard **50%**).
3. A slot in the building queue becomes free.
4. The effect **does not apply** (since the end point was not
   achieved).

An interrupt is used as a reaction to changes in priorities:
if an expensive upgrade is underway when the base comes under attack,
the player can cancel it, recover part of the cost, and redirect those
resources to defence.

---

<a id="4-аддитивная-композиция-eff"></a>
<a id="4-как-складывается-эффективность-eff"></a>
## 4. How efficiency (`eff`) is combined

Unlike many real-time strategy games, Cossacks 3 combines efficiency
bonuses **additively**:
```
eff(food, peasant) = 100 + Σ(mill.X) + Σ(aca.X) + Σ(bla.X)
```
For example, consider four notional Food upgrades worth +5/+10/+15/+20:

`eff = 100 + 5 + 10 + 15 + 20 = 150 %`. The base Food portion
of 45 becomes `floor(45 × 150 / 100) = 67`.

This is **not** multiplicative: it would be `1.05 × 1.10 × 1.15 × 1.20 = 1.59`
(159%), which is higher. The additive scheme gives a more predictable
final ceiling.

See [How Peasants Gather Resources §4](peasant_extraction.md) for details.

---

<a id="5-цели-апгрейда-targets"></a>
<a id="5-цели-улучшения-targets"></a>
## 5. Upgrade targets (`targets`)

`targets` determines **who** the upgrade applies to. Possible
values:

| Technical template | Affected objects |
|---|---|
| `'peaXXX'` | A specific internal ID (for example, Austrian Peasant: `peaaus`). |
| `'BuildingsAll'` | All nation buildings (hardcode). |
| `'UnitsAll'` | All units of the nation (hardcode). |
| `'<class>'` | All units of the class (`musket18`, `pike17`, ...). |
| List | Several internal IDs separated by a delimiter. |

For complex purposes (`buildtimeperc`, `priceperc`) there are separate
parameters:
- `sarrparam2[gc_resource_type_X]` stores a separate `priceperc`
  percentage for each resource.
- `targets = 'BuildingsAll'` - for `buildtimeperc`: applies to
  all 294 buildings of the nation.

---

<a id="6-priceperc-и-buildtimeperc"></a>
## 6. `priceperc` and `buildtimeperc`

Two special types of upgrades with an effect on the economy:

### 6.1. `priceperc`

Reduces the price of future orders by N%. Per-resource is used:
the upgrade has an array of percentages for food / wood / stone / gold /
iron/coal For example, the “Cheap Artillery” upgrade reduces gold
+ iron the price of guns by 25%, does not touch other resources.

In `data.json` it is represented as:
```
upgrade.priceperc[restype] = pct
```
### 6.2. `buildtimeperc`

Reduces the time to **build buildings** or **recruit units** by N%.
Standard values: −25%, −50%, −75% (well-researched upgrades
type "masons' guild").

Used as:
```
buildtime_new = floor(buildtime_base × (100 − buildtimeperc) / 100)
```
Applicable **only to new** orders - already under construction
ends with old time.

---

<a id="7-лимиты-и-переисследование"></a>
## 7. Limits and re-examination

In the standard game, each upgrade is researched **once** and forever.
After this:
- The upgrade button disappears from the UI.
- `gPlayer[plInd].upgrades[upgrade_ind] := True`.
- Resources for repeated purchases are not debited (UI blocks).

Some **level** upgrades (`mill.1`, `mill.2`, `mill.3`) -
these are **different upgrades** in `country.upgrade[]`. Everyone is examined
separately, the effect adds up:
`eff(food) = 100 + mill.1(+5) + mill.2(+10) + mill.3(+15) = 130 %`.

Unique (`uniqupgrade`) - a special class of 13 upgrades: they
affect a specific sid, not a class. For example, "Prussian
dragoons" - upgrade for only one sid.

---

<a id="75-эпохальный-переход-17--18-век"></a>
## 7.5. Epochal transition 17th → 18th century

In Cossacks 3, advancing to the 18th century is **not a timer or an
Age of Empires-style age**. It is the canonical “Progress to the
18th Century” upgrade in the Town Hall (SID `<nat>cen.1`), gated by
several required buildings.

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
### 7.5.2. Who's locked up in the 17th century

Three nations do not have `<nat>ba2`:

| Nation | “Progress to the 18th Century” (`<nat>cen.1`) | 18th-century Barracks (`<nat>ba2`) | Result |
|---|:---:|:---:|---|
| Algeria (`alg`) | ✅ | ❌ | The upgrade unlocks other research, but no 18th-century infantry |
| Turkey (`tur`) | ✅ | ❌ | Same |
| Ukraine (`ukr`) | ✅ | ❌ | Same |

These nations lack 18th-century Musketeers, Grenadiers, and Dragoons
(technically, units with suffix `18` or `kind = Grenadier`). Their
unique 17th-century units—Janissaries, Mamelukes, Cossacks, and
others—compensate for the missing Barracks.

<a id="753-что-даёт-cen1-для-апгрейдов-академии"></a>
### 7.5.3. What does `<nat>cen.1` give for academy upgrades

After researching `<nat>cen.1`, the academy opens
additional upgrades (they are visible as `<nat>aca.X` with
prerequisite to `cen.1`). Some of them are **`gc_ai_upg_century`**
for AI: this flag puts the AI opponent into the 18-eternal phase
production. See [How the Computer Player Works](../../systems/ai_behavior.md)
§ on build sequence (phases 7–9).

<a id="754-стратегические-выводы"></a>
### 7.5.4. Strategic Conclusions

- **“Progress to the 18th Century” (`cen.1`) is cheap and fast.**
  Constructing the required buildings is the bottleneck.
- **The 18th-century Barracks (`ba2`) takes a long time to build.**
  `buildtime = 5625` game seconds for one
  builder; with 8 builders the time is reduced proportionally
  rule `buildtime × 1.13 / N` (see
  [Building Construction, Repair, and Destruction §3.2](building_mechanics.md)).
- **Turkey, Algeria, Ukraine - nations of the 17th century.** If you play against
  them, do not expect the enemy to go into the 18th century.
- **Building an academy for other reasons** (for example, for
  efficiency or damage upgrades) automatically takes one step towards the 18th century.
  Useful even if the transition is not planned.

---

<a id="76-математика-применения-порядок-и-комбинирование"></a>
## 7.6. Application Mathematics: Order and Combination

**Main observation:** in Cossacks 3 the order of upgrade research
**does not affect** the final parameters of the unit and building in almost all cases
cases, even when a flat bonus and
percentage bonus from different places (for example, forge "+5 damage" and
Academy "+25% damage"). This is different from naive arithmetic, where
`(B + 5) × 1.25 ≠ B × 1.25 + 5`.

The reason is the implementation of `_player_ApplyUpgrade` [^om1]: every
upgrade accumulates its term in a **separate field** of the object
(`damagestatic`, `damagepercent`, `protection[kind]`, `shield`,
`resefficiency[*]`, ...), and the final value **is recalculated from the
unchanged base** (`damageinit`) using a formula that takes only
summary state, not previous value. Accumulative chain
“one step → next step” is not here.

<a id="761-урон-damage-flat-и-damage-"></a>
<a id="761-урон-постоянная-прибавка-damage-и-процент-damage-"></a>
### 7.6.1. Damage (flat `+damage` and percentage `+damage %`)

**three** fields are stored: `damageinit` (base), `damagestatic` (amount
all flat bonuses), `damagepercent` (sum of all % bonuses). Everyone
upgrade `gc_upg_type_damage` [^om2] increases `damagestatic` by
`value` and recalculates `damage` from `damageinit + damagestatic` with
amendment to `damagepercent`. Each `gc_upg_type_damageperc` [^om3]
does the same thing, but updates `damagepercent` instead
`damagestatic`. In both cases, the total value is read from
bases:
```
damage = floor((damageinit + Σflat) × (1 + Σ% / 100))
```
Example: base 10, bonuses `+5` and `+25 %`. It will work in both orders
`floor((10 + 5) × 1.25) = 18`. In ordinary arithmetic
`(10 + 5) × 1.25 = 18.75` vs `(10 × 1.25) + 5 = 17.5` - then
there is a difference that Cossacks doesn't have.

<a id="762-защита-protection-shield-оба-только-flat"></a>
<a id="762-защита-protection-shield-только-постоянные-прибавки"></a>
### 7.6.2. Protection (`protection`, `shield`; flat bonuses only)

`protection[kind] += value`; `shield += value`. Net amount -
the order doesn't matter.

<a id="763-прочность-юнита-lifeperc-"></a>
<a id="763-hp-юнита-lifeperc-"></a>
### 7.6.3. Unit durability (`lifeperc`, %)

`maxhp = round(maxhp × (1 + value / 100))`. Cumulative multiplication
commutative (`H · (1 + a) · (1 + b) = H · (1 + b) · (1 + a)`).
The order is not important (up to rounding, see below).

<a id="764-эффективность-добычи-effectfoodwoodstone--perc"></a>
### 7.6.4. Production efficiency (`effectfood/wood/stone` + `…perc`)

The same array `resefficiency[res]` (base = 100). All four
variants (`flat` / `perc`) do **the same thing**:
```
resefficiency[res] := resefficiency[res] + round(value);
                                          // percentage variants also use += value, not *=
```
That is, the sum of all vals, the order does not matter. **Nuance:** flat and %
here are indistinguishable - both are added. Multiplier `resefficiency / 100`
then applied in the extraction formula (`_unit_GetPeasantResPortion`).

<a id="765-жизнь-поля-fieldlifeperc-"></a>
### 7.6.5. Life of the field (`fieldlifeperc`, %)

`fieldlife += value`. Additive (not multiplicative). Order
indifferent.

<a id="766-время-постройки-buildtimeperc-"></a>
### 7.6.6. Construction time (`buildtimeperc`, %)

`buildtime *= (1 + value / (100 × 100000))` - cumulative
multiplication, commutative. Strange divisor `100 × 100000`
explains storing val as `−7500000` for −75% (see note
about scale at the beginning of the document).

<a id="767-скорострельность--дальность--разлёт-attpauseperc-attrangeperc-attdispertionperc"></a>
### 7.6.7. Rate of fire / range / expansion (`attpauseperc`, `attrangeperc`, `attdispertionperc`)

All types `field *= (1 + value / 100)` - cumulative multiplication,
commutative.

<a id="768-цена-priceperc-"></a>
### 7.6.8. Price (`priceperc`, %)

`price[j] = round(price[j] × (1 + value / 100))`. Multiplication
commutative, but `round()` after each step **may** give
±1 difference for different orders. In practice, several `priceperc`
on one object almost do not intersect.

<a id="769-рыболовство-fishingperc-"></a>
### 7.6.9. Fishing (`fishingperc`, %)

`fishingmax = round(fishingmax × (1 + value / 100))` - the same
situation: theoretically ±1 of the order due to rounding, on
In practice, there is one upgrade per boat.

<a id="7610-скорость-движения-speedperc---аномалия"></a>
### 7.6.10. Movement speed (`speedperc`, %) - **anomaly**

`gc_upg_type_speedperc` [^om4] instead of the usual
`*= (1 + value / 100)` recalculates the field as
`speed := 1 / (speed × (1 + value / 100))`. Field `speed` is stored
as `1 / v` (reciprocal), and the operation inverts the value.
Two consecutive applications give
`V₀ × (1 + p₂) / (1 + p₁)` - **order-dependent**, obvious bug. B
does not appear in the current version only because it exists in the data
**exactly one** `speedperc`-upgrade per unit type (`aca.28` -
ship speed +40%), it cannot be reapplied
(`upgstate.done := True` blocks).

<a id="7611-сводная-таблица"></a>
### 7.6.11. Pivot table

| `itype` | Accumulation | Does it depend on the order? |
|---|---|---|
| `damage` (flat) | `damagestatic += val`, recalculation from `damageinit` | No |
| `damageperc` (%) | `damagepercent += val`, recalculation from `damageinit` | No |
| `protection`, `shield` | `+= val` | No |
| `lifeperc` (%) | `maxhp = round(maxhp × (1 + val/100))` | No (commut. mind; `round` can give ±1) |
| `effectfood/wood/stone[perc]` | `resefficiency += val` | No (flat and % are indistinguishable) |
| `fieldlifeperc` | `fieldlife += val` | No |
| `buildtimeperc` (%) | `*= (1 + val / (100 × 10⁵))` | No |
| `priceperc` (%) | `= round(· × (1 + val/100))` | Rounding only (±1) |
| `attpauseperc/rangeperc/dispertionperc` | `*= (1 + val/100)` | No |
| `fishingperc` (%) | `= round(· × (1 + val/100))` | Rounding only (±1) |
| `speedperc` (%) | `speed = 1 / (speed × (1 + val/100))` | **Yes, but there is only one upgrade in the data** |

<a id="7612-практический-вывод"></a>
### 7.6.12. Practical conclusion

**Upgrades can be purchased in any convenient order - final performance characteristics
units/buildings are identical.** The order only matters for
**economy in time** (what will be built first) and for
sequences of **enable** upgrades (frigates, linear
ships, multi-barreled guns) - but not for bonus arithmetic.
This simplifies planning: in economic and combat simulators you can
aggregate upgrades as sets without tracking
the sequence of their use.

The only thin places are `priceperc`, `lifeperc`, `fishingperc`
(cumulative `round()` can give ±1 of the order) and a bug
`speedperc` (but not reapplied). For everything else
mathematics is designed in such a way that the result is a function of the set
researched upgrades, not history.

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

The complete graph is in [Cossacks 3 - Tech Tree (by nation)](../../../reports/tech/tech_tree.md)
+ [`derived/tech_tree.json`](../../../../derived/tech_tree.json).

---

<a id="9-открытые-эмпирические-вопросы"></a>
## 9. Open empirical questions

1. **Exact refund percentage upon cancellation**. Standard is 50%, but for
   may differ for some upgrades. Find a constant
   `gc_upgrade_cancelrefund` to `dmscript.global` or in a script.
2. **Applying `priceperc` to upgrades already open in the UI.** If
   bought `priceperc`-upgrade during the order queue, new orders
   will they get a discount?
3. **Conflict resolution**. If two upgrades affect the same field
   (`hp += 30` and `hp += 20`), do they add up additively (50)
   or does only the latter apply?

---

<a id="источники"></a>
## Sources

[^1]: `data/scripts/lib/country.script` - definition
      `country.upgrade[]` via `SetUpgStruct` and `AddUpgradePack`.
      Parser `parser/simulate_upgrades.py` inlines these
      macro wrappers and produces fully permitted upgrade lines.

[^2]: `data/scripts/lib/country.script` - function
      `_country_DoUpgrade(plInd, ind)` or similar: applies
      effects at study completion. Iterates through `targets`
      and changes the corresponding fields in `objbase`/`objprop`/`gObjProp`.

[^om1]: `_player_ApplyUpgrade` - `lib/player.script:1707-1983`. All
        branches `gc_upg_type_*` are dispatched here; general template
        — change the slot field and recalculate the total from the unchanged base.

[^om2]: Branch `gc_upg_type_damage` - `lib/player.script:1764`:
        ```pascal
        damagestatic := damagestatic + round(value);
        damage := floor((damageinit + damagestatic) * (1 + damagepercent/100));
        ```
[^om3]: Branch `gc_upg_type_damageperc` - `lib/player.script:1783`:
        ```pascal
        damagepercent := damagepercent + round(value);
        damage := floor((damageinit + damagestatic) * (1 + damagepercent/100));
        ```
[^om4]: Branch `gc_upg_type_speedperc` - `lib/player.script:1930`:
        ```pascal
        speed := 1 / (speed * (1 + value/100));
        ```
