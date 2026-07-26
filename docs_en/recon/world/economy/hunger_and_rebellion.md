<a id="recon-голод-и-бунт"></a>
# Recon: Hunger and Riot

Deep analysis: under what conditions does a player’s flags go up?
`bfamine` (hunger) and `brebellion` (rebellion), what exactly does this mean?
happens, who dies first, how to protect yourself. All links to code -
in [Sources](#sources) at the end of the document.

## TL;DR

- **Hunger** (`bfamine = True`) turns on when the player has
  `food = 0` **and** on the next consumption tick it turns out
  negative remainder. Removed as soon as `food > 0` or
  `consume.food <= 0`.
- **Riot** (`brebellion = True`) is turned on when the player has
  `gold = 0` **and** `consume[gold] > income[gold]` (consumption
  exceeds production). Removed as soon as `gold >= 2` or
  `consume[gold] <= 0`.
- Hunger kills normal units that have `bnohungry = False`
  (peasants, infantry). Buildings, mercenaries, and landsknechts are not touched.
- Riot destroys **mercenaries only** (`bmercenary = True`) - with
  speed ≈ 18.3% per tick on hard+ difficulty. See
  [`mercenaries_diplomacy.md` §3](../../systems/mercenaries_diplomacy.md).
- Points for destroying a rebel mercenary are counted with a multiplier
  `× 3` (not `× 2`), which makes raids on a starving enemy
  more effective in terms of score [^1].

---

<a id="1-где-и-когда-поднимается-флаг"></a>
## 1. Where and when the flag is raised

The logic in `lib/player.script` is the procedure for consuming resources,
[^2] is called every game tick. For each resource:

- If the player has a sufficient amount (`res[i] >= value`) - resource
  is written off, the flag (`bfamine` or `brebellion`) is reset to
  `False`.
- If the amount is not enough, the balance is written off, and for `food` immediately
  `bfamine := True` rises. For `gold` additional
  check: `brebellion` is raised only if
  `consume[gold] > income[gold]`.

That is, for **gold** there is “pay-as-you-could” protection: if
the mines pay for the consumption of mercenaries, a riot will not break out even with
`gold = 0`. For **food** there is no such protection: hunger turns on immediately,
as soon as `food = 0` and there are starving people.

After the calculation, at the very end of the procedure, the flag is automatically removed: if
`brebellion = True`, but the condition has disappeared (there are ≥ 2 gold **or**
gold consumption has been reset) - the flag is extinguished. Likewise for
`bfamine` - if food is again > 0 or food consumption = 0 [^2].

That is, **on the same tick** the flag can light up immediately
go out - for example, if exactly on the same tick the player sold for
food market or hosted a caravan. In the UI this will give a single blink
red.

<a id="11-период-тика"></a>
### 1.1. Tick period

Resource consumption tick - `_player_DoTickResources` or similar,
called once every **`_misc_GetTickRes()` seconds**, usually ~1 g-sec
(See [`internals/engine/ticks_and_subticks.md`](../../../../internals_en/engine/ticks_and_subticks.md)).
That is, the flag is checked ≈ 14 times per real second at speed
fast.

---

<a id="2-что-происходит-при-голоде"></a>
## 2. What happens during hunger

`bfamine = True` triggers a side mechanism in
`lib/unit.script` — every tick all units are checked for the sign
"They might die of hunger." Conditions of death:

| Condition | Result |
|---|---|
| `bfamine = True` for player | Trigger. |
| `bnohungry = True` at unit | Immunity (will never die of hunger). |
| `consume.food = 0` at unit | Immunity (he doesn’t eat food → there’s nothing to punish him for). |

For a suitable unit: every tick with RNG probability
(see §2.2 below) `hp := 0`, the unit dies instantly.

<a id="21-кто-иммунен-bnohungry--true"></a>
### 2.1. Who is immune (`bnohungry = True`)

| Type | `bnohungry` |
|---|---|
| All buildings | `True` |
| Mercenaries (`bmercenary = True`) | `True` |
| Landsknechts, individual elite units | depends, see `data.json` |
| Peasants | `False` |
| Regular infantry, cavalry | `False` |

The exact value of `bnohungry` for each unit is in
[`../../../../data.json`](../../../../data.json), field `bnohungry`.

### 2.2. Chance of dying from starvation

The exact formula is an RNG gate per tick with a complexity threshold
player [^3]:

| Difficulty | Threshold | Chance of death per tick | Expected time until death of 1 unit |
|---|---:|---:|---|
| 0 (easy) | `RandomInt < 5` | ≈ 0.0076% | very slowly (hours) |
| 1 (normal) | `RandomInt < 12` | ≈ 0.018% | watch |
| 2+ (hard / very hard / impossible) | `RandomInt < 50` | ≈ 0.076% | minutes (4-10× faster than normal) |

`_misc_RandomInt = floor(random × 32768)`, so the actual
chance - `threshold / 32768`. The transition to death occurs at
`Nothing`-tike (see [`internals/engine/ticks_and_subticks.md`](../../../../internals_en/engine/ticks_and_subticks.md)).

Guide to the actual game:
- 30–60 g-sec after `bfamine = True` the first ones begin to die
  peasants.
- In 3–5 minutes of hunger on hard, the player loses ~50% of peasants and a large
  part of the infantry.
- If you manage to restore food (bring it from the field, sell gold
  on the market) - the flag goes out, the death stops.

### 2.3. Food consumption: upkeep formula

Each unit without `bnohungry = True` accumulates from the player
`gPlayer.counter.resconsume[food]` via increment when creating [^5]:
```
per_unit_resconsume_food = consume.food          # из case-ветки в unit.script
                         + gc_obj_foodperunit    # = 30, если !bnohungry и !bbuilding
```
Food consumption per game second (`player.script:_player_ProcessResourceConsume`):
```
food_per_g_sec = sum_of_resconsume_food × gc_time_to_frames / 20000
               = sum × 32 / 20000  =  sum × 0.0016
```
**Sanity-check (verified empirically 2026-04-29):** 18 Austrian
peasants (`consume.food = 32`, `bnohungry = False`) are idle 2
game minutes:
```
sum = 18 × (32 + 30) = 1116
food / g-sec = 1116 × 32 / 20000 ≈ 1.786
за 120 game sec ≈ 214 food   ✓
```
Consumption of food / g-sec per unit (for `bnohungry = False`):

| Unit | `consume.food` | + `gc_obj_foodperunit` | total | food/g-sec |
|---|---:|---:|---:|---:|
| peasant (aus / pol / spa / eng / ukr / sco) | 32 | +30 | 62 | 0.0992 |
| peasant `peatur` / `peaalg` | 28 | +30 | 58 | 0.0928 |
| peasant `pearus` | 26 | +30 | 56 | 0.0896 |
| infantry without explicit `consume.food` | 0 | +30 | 30 | 0.0480 |

### 2.3. Pop cap connection

If the player falls below the `farmused` limit (see.
[`reference/01_economy/README.md`](../../../reference/01_economy/README.md)) is
**not** runs `bfamine`. Hunger only triggers with `food = 0`.
That is, “no houses” does not automatically kill the population; kills
only real food shortage.

---

## 3. What happens during a riot

`brebellion = True` applies **only** to mercenaries
(`bmercenary = True`). Logic in `lib/unit.script` [^4]: each
`Nothing`-tick (~0.625 g-sec) each mercenary rolls
`_misc_RandomInt < threshold`, where `_misc_RandomInt = floor(random × 32768)`:

| Difficulty | Threshold | Chance to move per tick |
|---|---:|---:|
| 0 (easy) | 100 | 100 / 32768 ≈ **0.305 %** |
| 1 (normal) | 200 | 200 / 32768 ≈ **0.610 %** |
| ≥ 2 (hard / very hard / impossible) | **6000** | 6000 / 32768 ≈ **18.31%** |

On hard, the expected time before the transfer of one mercenary is
`0.625 / 0.1831 × 0.5 ≈ 1.7 game sec`. **Army of 50 mercenaries
runs up almost completely in 5–10 g-sec.** On easy and normal
the rebellion is almost decorative.

During the transition, the mercenary ends up in a **virtual mercenary player**
(`gc_player_mercenaryind = MaxPlayerCount − 1`), automatically
hostile to all real players. That is, a former ally
becomes an aggressive NPC unit rather than a neutral one.

Basic rule: “don’t start a deep center until you’re sure you can handle it.”
golden upkeep.”

Details and countermeasures are in
[`../systems/mercenaries_diplomacy.md` §3-4](../../systems/mercenaries_diplomacy.md).

### 3.1. Who is immune to riot

| Type | Rebellious? |
|---|---|
| Normal units | No (riot only triggers with `bmercenary = True`). |
| Mercenaries from the deep center | Yes. |
| Buildings | No. |

### 3.2. Score bonus to opponent

When a mercenary dies in a riot from an enemy blow, the enemy
receives **×3** points, not ×2 [^1]. This is an intentional reward:
“caught a moment of weakness - more points.” In practice this is rare
important, but in a close game on points it can affect the winner.

---

## 4. Protection from hunger and rebellion

### 4.1. From hunger

1. **Place warehouses near the fields** - food arrives faster.
2. **Don't gather too many infantry** at the beginning - `consume.food`
   infantry is higher than that of peasants (typically 2–4 per tick versus 1).
3. **Less consuming units** if you know what food will be
   compress. Dismiss extra recruits.
4. **Reserve food**, especially before the attack (when the peasants are
   killed) - otherwise a double blow: killed peasants + the onset of famine.

### 4.2. From rebellion

1. **Gold mines with upgrade** - sharply increase income, pay off
   upkeep mercenaries.
2. **The diplomatic center is built after the academy and a couple of gold mines**, not before.
3. **Do not dump more mercenaries in one place than `income gold`
   capable of feeding**.
4. **Market exchange** - sell food/wood for gold if there are reserves
   gold went into the red zone.
5. **Enemy attack** - sometimes the riot itself burns the mercenary army
   faster than the enemy can destroy it. If you already go, attack
   something valuable, so that at least you can get something for the death of the squad.

---

## 5. Connection with other flags

| Flag | Description | File |
|---|---|---|
| `farmused = 0` | The player has run out of food (via `pop cap`); results in **defeat** (see [`../systems/victory_conditions.md`](../../systems/victory_conditions.md)). |
| `bfamine` | Does not lead to defeat by itself; kills units. |
| `brebellion` | Does not lead to defeat; only kills mercenaries. |
| `bleave` | The player has given up (via the “leave” UI). Defeat immediately. |

Note: `farmused = 0` (victory trigger) and `bfamine` (hunger)
**different things**. `farmused = 0` means "you have no food"
in general,” which leads to defeat. `bfamine` means “you have
food = 0, and there are residents who need to eat", which leads to
gradual death.

---

<a id="6-открытые-эмпирические-вопросы"></a>
## 6. Open empirical questions

1. **Exact formula for the probability of death from starvation.** From the code
   `_unit_DoTickFamine` or similar function has not yet been read
   actual coefficient. Measure through a series: 100 peasants,
   `food = 0` for 60 g-sec, count how many died - display
   probability per tick.
2. **Who dies first: peasants or infantry?** Not in the code
   priority by unit type: `unit.inc/nothing.inc:482` passes by
   all non-`bnohungry` player units with the same RNG check
   `_misc_RandomInt < threshold`. Peasants die “first”
   only because there are usually more of them, and in the same RNG cycle
   statistically more fall into the lethal range. You can
   clarified by measuring an equal composition (for example, 50 peasants + 50
   pikemen): the proportions must match.
3. **What is considered a consumption tick for a riot?** The script mentions
   `Nothing-tick`, but what this is in g-seconds is not defined. Measure
   difference between easy (`5%`) and hard (`18.3%`) → tempo
   desertion.

---

<a id="источники"></a>
## Sources

[^1]: `data/scripts/lib/unit.script:3944` - score modifier for
      unit death: `if (gPlayer[pl].brebellion) and bmercenary then
      scoremodifier := 3 else scoremodifier := 2;`. Then
      `gPlayer[pl].counter.scores -= score * scoremodifier`.

[^2]: `data/scripts/lib/player.script:295-321` - main procedure
      resource consumption. First, `food`/`gold` are installed
      flags, then at the end they are removed if the condition has disappeared.

[^3]: `data/scripts/units/unit.inc/nothing.inc:445-505` - handler
      `Nothing`-tika. For units without `bnohungry`: `if _misc_RandomInt
      < threshold then hp := 0;` where `_misc_RandomInt = floor(random
      × 32768)` and `threshold` depends on `gPlayer[plInd].difficulty`
      (5 / 12 / 50). Switching by difficulty is in the same place.

[^4]: `data/scripts/units/unit.inc/nothing.inc:445-505` - ibid.
      handler `brebellion` and `bmercenary`. Threshold for riot:
      easy = 100, normal = 200, hard+ = 6000 (out of 32768).
      `gc_player_mercenaryind = MaxPlayerCount − 1` —
      virtual player-recipient of departed mercenaries.

[^5]: `data/scripts/lib/unit.script:3810, 3821` - increments
      `gPlayer.counter.resconsume[food]` when creating a unit.
      Installation `bnohungry = True` for buildings -
      `data/scripts/lib/unit.script:471` (inside
      `SetObjBuildingBaseSettings`). Food/gold flow handler
      per tick - `data/scripts/lib/player.script:280-322`.
