<a id="recon-голод-и-бунт"></a>
<a id="голод-и-бунт-наёмников"></a>
# Famine and Mercenary Rebellion

[← How the game works](../../README.md)

This article explains when the game sets the technical flags
`bfamine` (famine) and `brebellion` (rebellion), what happens next,
which units are affected, and how a player can respond. Code
references are collected under [Sources](#sources).

<a id="коротко-о-главном"></a>
## TL;DR

- **Famine** (`bfamine = True`) begins when Food runs out
  (`food = 0`) and the next consumption tick produces a deficit.
  It ends when Food becomes positive again or consumption stops
  (`consume.food <= 0`).
- **Rebellion** (`brebellion = True`) begins when Gold runs out and
  Gold consumption exceeds income (`consume[gold] > income[gold]`).
  It ends at two or more Gold, or when consumption stops.
- Hunger kills normal units that have `bnohungry = False`
  (peasants, infantry). Buildings, mercenaries, and landsknechts are not touched.
- Rebellion affects **mercenaries only** (`bmercenary = True`), with
  a probability of about 18.3% per tick on Hard and above. See
  [`mercenaries_diplomacy.md` §3](../../systems/mercenaries_diplomacy.md).
- Points for destroying a rebel mercenary are counted with a multiplier
  `× 3` (not `× 2`), which makes raids on a starving enemy
  more valuable in score terms [^1].

---

<a id="1-где-и-когда-поднимается-флаг"></a>
<a id="1-где-и-когда-включается-состояние"></a>
## 1. When the state is enabled

The logic in `lib/player.script` is the procedure for consuming resources,
[^2] is called every game tick. For each resource:

- If the player has a sufficient amount (`res[i] >= value`) - resource
  is written off, the flag (`bfamine` or `brebellion`) is reset to
  `False`.
- If the amount is insufficient, the remaining stock is consumed.
  For Food (`food`) the game immediately sets `bfamine := True`.
  For Gold (`gold`), `brebellion` is set only if
  `consume[gold] > income[gold]`.

Gold therefore has partial-payment protection: if the Mines cover
mercenary consumption, rebellion does not begin even at `gold = 0`.
Food has no equivalent protection; famine starts as soon as the
stock is empty and units still consume it.

After the calculation, at the very end of the procedure, the flag is automatically removed: if
`brebellion = True` but the condition no longer applies (at least
two Gold, or zero Gold consumption), the flag is cleared. The same
applies to `bfamine` when Food becomes positive or consumption
falls to zero [^2].

That is, **on the same tick** the flag can light up immediately
go out - for example, if exactly on the same tick the player sold for
Food on the Market or received a caravan. In the interface this
appears as a single red flash.

<a id="11-период-тика"></a>
<a id="11-период-проверки"></a>
### 1.1. Check interval

Resource consumption tick - `_player_DoTickResources` or similar,
called once every **`_misc_GetTickRes()` seconds**, usually ~1 g-sec
(See [`internals/engine/ticks_and_subticks.md`](../../../../internals_en/engine/ticks_and_subticks.md)).
The flag is therefore checked about 14 times per real second at
Fast game speed.

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

<a id="22-вероятность-гибели-от-голода"></a>
### 2.2. Chance of dying from starvation

The exact formula is a random-number check whose threshold depends
on the player's difficulty [^3]:

| Difficulty | Threshold | Chance of death per tick | Expected time until death of 1 unit |
|---|---:|---:|---|
| 0 (easy) | `RandomInt < 5` | ≈ 0.0076% | very slowly (hours) |
| 1 (normal) | `RandomInt < 12` | ≈ 0.018% | hours |
| 2+ (hard / very hard / impossible) | `RandomInt < 50` | ≈ 0.076% | minutes (4-10× faster than normal) |

`_misc_RandomInt = floor(random × 32768)`, so the actual
chance - `threshold / 32768`. The transition to death occurs at
`Nothing`-tike (see [`internals/engine/ticks_and_subticks.md`](../../../../internals_en/engine/ticks_and_subticks.md)).

Practical guide:

- The first Peasants begin to die 30–60 game seconds after
  `bfamine = True`.
- After 3–5 minutes of famine on Hard, a player may lose about half
  their Peasants and much of the infantry.
- Restoring Food—by gathering it or selling Gold on the Market—clears
  the flag and stops the deaths.

<a id="23-расход-food-формула-upkeep"></a>
<a id="23-расход-еды"></a>
### 2.3. Food consumption

Each unit without `bnohungry = True` accumulates from the player
`gPlayer.counter.resconsume[food]` via increment when creating [^5]:
```
per_unit_resconsume_food = consume.food          # from the case branch in unit.script
                         + gc_obj_foodperunit    # = 30 when !bnohungry and !bbuilding
```
Food consumption per game second (`player.script:_player_ProcessResourceConsume`):
```
food_per_g_sec = sum_of_resconsume_food × gc_time_to_frames / 20000
               = sum × 32 / 20000  =  sum × 0.0016
```
**Empirical check from April 29, 2026:** 18 Austrian Peasants
(`consume.food = 32`, `bnohungry = False`) remain idle for two
game minutes:
```
sum = 18 × (32 + 30) = 1116
food / g-sec = 1116 × 32 / 20000 ≈ 1.786
over 120 game sec ≈ 214 food   ✓
```
Food consumption per game second and unit (for `bnohungry = False`):

| Canonical name | `consume.food` | + `gc_obj_foodperunit` | Total | Food per game second |
|---|---:|---:|---:|---:|
| Peasant of Austria, Poland, Spain, England, Ukraine, or Scotland | 32 | +30 | 62 | 0.0992 |
| Peasant of Turkey or Algeria (`peatur`, `peaalg`) | 28 | +30 | 58 | 0.0928 |
| Russian Serf (`pearus`) | 26 | +30 | 56 | 0.0896 |
| Infantry without explicit `consume.food` | 0 | +30 | 30 | 0.0480 |

<a id="23-связь-с-pop-cap"></a>
<a id="24-связь-с-пределом-населения"></a>
### 2.4. Population-limit connection

Falling below the population limit `farmused` (see
[`reference/01_economy/README.md`](../../../reference/01_economy/README.md))
does **not** set `bfamine`. Famine starts only when Food is actually
zero. A shortage of Houses does not kill units; a real Food shortage does.

---

<a id="3-что-происходит-при-бунте"></a>
## 3. What happens during a riot

`brebellion = True` applies **only** to mercenaries
(`bmercenary = True`). Logic in `lib/unit.script` [^4]: each
on each technical `Nothing` state tick (about 0.625 game seconds),
every mercenary makes the check
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

<a id="31-кто-иммунен-к-бунту"></a>
### 3.1. Who is immune to riot

| Type | Rebellious? |
|---|---|
| Normal units | No (riot only triggers with `bmercenary = True`). |
| Mercenaries from the deep center | Yes. |
| Buildings | No. |

<a id="32-score-бонус-противнику"></a>
<a id="32-дополнительные-очки-противнику"></a>
### 3.2. Additional score for the opponent

When a mercenary dies in a riot from an enemy blow, the enemy
receives **×3** points, not ×2 [^1]. This is an intentional reward:
“caught a moment of weakness - more points.” In practice this is rare
important, but in a close game on points it can affect the winner.

---

<a id="4-защита-от-голода-и-бунта"></a>
## 4. Protection from hunger and rebellion

<a id="41-от-голода"></a>
### 4.1. From hunger

1. **Place Storehouses near Fields** so Food is delivered sooner.
2. **Do not recruit too much infantry early**: its `consume.food`
   value is usually higher than a Peasant's.
3. **Reduce the number of consuming units** if Food reserves are
   expected to shrink; dismiss surplus recruits.
4. **Keep Food in reserve**, especially before an attack that may
   draw Peasants away from work or get them killed.

<a id="42-от-бунта"></a>
### 4.2. From rebellion

1. **Upgrade Gold Mines** to raise income and cover mercenary upkeep.
2. **Build the Diplomatic Center after an Academy and a pair of Gold
   Mines**, not before.
3. **Do not hire more mercenaries than Gold income (`income[gold]`)
   can support.**
4. **Use the Market** to sell Food or Wood for Gold before reserves
   become critically low.
5. **Enemy attack** - sometimes the riot itself burns the mercenary army
   faster than the enemy can destroy it. If you already go, attack
   something valuable, so that at least you can get something for the death of the squad.

---

<a id="5-связь-с-другими-флагами"></a>
<a id="5-связь-с-другими-состояниями"></a>
## 5. Related states

| Flag | Description | File |
|---|---|---|
| `farmused = 0` | The population limit is exhausted; results in **defeat** (see [`../systems/victory_conditions.md`](../../systems/victory_conditions.md)). |
| `bfamine` | Does not lead to defeat by itself; kills units. |
| `brebellion` | Does not lead to defeat; only kills mercenaries. |
| `bleave` | The player surrendered through the interface. Defeat is immediate. |

Note: `farmused = 0` (victory trigger) and `bfamine` (hunger)
are **different conditions**. `farmused = 0` is the population-limit
defeat trigger. `bfamine` means that Food is zero while units still
need to eat, which causes gradual deaths.

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
      unit death:

      ```pascal
      if (gPlayer[pl].brebellion) and bmercenary then
        scoremodifier := 3
      else
        scoremodifier := 2;
      ```

      Then `gPlayer[pl].counter.scores -= score * scoremodifier`.

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
