<a id="recon-голод-и-бунт"></a>
<a id="голод-и-бунт-наёмников"></a>
<a id="технический-разбор-голода-и-бунта-наёмников"></a>
# Technical Evidence for Famine and Mercenary Rebellion

[← Scripts and Scenarios](structure.md)

[Reader-facing article on famine and rebellion](../../docs_en/recon/world/economy/hunger_and_rebellion.md)

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
- Famine can kill ordinary units with `bnohungry = False`, including
  Peasants and infantry. Buildings, mercenaries, and some elite units are
  immune.
- Rebellion affects **mercenaries only** (`bmercenary = True`), with
  a probability of about 18.3% per eligible background check on Hard and
  above. See
  [Mercenaries and the Diplomatic Center §3](../../docs_en/recon/systems/mercenaries_diplomacy.md).
- A mercenary's defection immediately subtracts score from its former owner
  with a `×3` multiplier instead of `×2` [^1]. This affects final statistics,
  not the match winner or rating.

---

<a id="1-где-и-когда-поднимается-флаг"></a>
<a id="1-где-и-когда-включается-состояние"></a>
## 1. When the state is enabled

The resource-consumption procedure in `lib/player.script` [^2] runs every
resource tick. For each resource:

- If the player has enough (`res[i] >= value`), the amount is deducted and
  the corresponding flag (`bfamine` or `brebellion`) is reset to `False`.
- If the amount is insufficient, the remaining stock is consumed.
  For Food (`food`) the game immediately sets `bfamine := True`.
  For Gold (`gold`), `brebellion` is set only if
  `consume[gold] > income[gold]`.

Gold therefore has partial-payment protection: if the Mines cover
mercenary consumption, rebellion does not begin even at `gold = 0`.
Food has no equivalent protection; famine starts as soon as the
stock is empty and units still consume it.

At the end of the procedure, the game clears `brebellion` when its condition
no longer applies—at least two Gold, or no Gold consumption. It likewise
clears `bfamine` when Food becomes positive or consumption falls to zero
[^2].

A state can therefore begin and end within one resource update, for example
when a Market transaction restores the missing resource during the same
interval. The interface may show only a brief red warning.

<a id="11-период-тика"></a>
<a id="11-период-проверки"></a>
### 1.1. Check interval

The resource update is controlled by `_misc_GetTickRes()` and normally runs
about once per game second. See
[Ticks and subticks](../engine/ticks_and_subticks.md) for the engine's time
model. The exact interval at each game speed remains an empirical question.

---

<a id="2-что-происходит-при-голоде"></a>
## 2. What happens during famine

When `bfamine = True`, the unit state handler performs an independent random
death check for every vulnerable unit:

| Condition | Result |
|---|---|
| `bfamine = True` for player | Trigger. |
| The unit has `bnohungry = True` | Immune |

If a vulnerable unit passes the random check described in §2.2, the script
places it in `essential_death`, after which the normal death sequence runs.
An explicit `consume.food = 0` does not provide immunity: a non-building unit
without `bnohungry` still receives the common consumption surcharge.

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
[`data.json`](../../data.json), field `bnohungry`.

<a id="22-вероятность-гибели-от-голода"></a>
### 2.2. Chance of dying from starvation

The exact formula depends on difficulty and network mode [^3]:

| Mode and difficulty | Check | Chance of death per check | Mean checks until death |
|---|---:|---:|---|
| Single-player, 0 (Easy) | `RandomInt < 5` | ≈ 0.0153% | ≈ 6,554 |
| Single-player, 1 (Normal) | `RandomInt < 12` | ≈ 0.0366% | ≈ 2,731 |
| Any mode, 2+ (Hard / Very Hard / Impossible) | `RandomInt < 50` | ≈ 0.1526% | ≈ 655 |
| Online / LAN, 0 (Easy) | `RandomInt₁ < 50` **or** an independent `RandomInt₂ < 5` | ≈ 0.167823% | ≈ 596 |
| Online / LAN, 1 (Normal) | `RandomInt₁ < 50` **or** an independent `RandomInt₂ < 12` | ≈ 0.189153% | ≈ 529 |

`_misc_RandomInt = floor(random × 32768)`. In single-player, the chance is
`threshold / 32768`; online Easy and Normal combine two independent checks.
Death is applied by the unit's `Nothing` state handler; see
[ticks and subticks](../engine/ticks_and_subticks.md).

Working in-game estimates that still require repeated measurements:

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
Food per game second = 1116 × 32 / 20000 ≈ 1.786
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
<a id="24-связь-с-населением"></a>
### 2.4. Population connection

`farmused` increases and decreases once for every non-building unit and serves
as the occupied-population count. It is neither housing capacity / the
population limit (`farm`) nor the famine flag. It participates in the defeat
check; see
[Victory, Defeat, and the End of a Match](../../docs_en/recon/systems/victory_conditions.md).
In an ordinary non-battle match, the player loses at `farmused = 0` even if
buildings remain. A housing shortage blocks recruitment but does not set
`bfamine`; famine starts only when Food is zero and consumption continues.

---

<a id="3-что-происходит-при-бунте"></a>
## 3. What happens during rebellion

`brebellion = True` applies **only** to mercenaries with
`bmercenary = True`. On each eligible `Nothing` state update, every mercenary
independently checks
`_misc_RandomInt < threshold`, where `_misc_RandomInt = floor(random × 32768)`:

| Difficulty | Threshold | Defection probability per check |
|---|---:|---:|
| 0 (easy) | 100 | 100 / 32768 ≈ **0.305 %** |
| 1 (normal) | 200 | 200 / 32768 ≈ **0.610 %** |
| ≥ 2 (hard / very hard / impossible) | **6000** | 6000 / 32768 ≈ **18.31%** |

On Hard, one mercenary takes an average of
`1 / 0.1831 ≈ 5.46` checks to defect. Converting that value to game seconds
requires the exact `Nothing` processing interval, which has not yet been
measured. Defection is much slower on Easy and Normal.

On defection, the mercenary moves to the **virtual mercenary player**
(`gc_player_mercenaryind = MaxPlayerCount − 1`), automatically
hostile to all real players. A former ally therefore becomes an aggressive
game-controlled unit rather than a harmless neutral.

Details and countermeasures are in
[Mercenaries and the Diplomatic Center §3-4](../../docs_en/recon/systems/mercenaries_diplomacy.md).

<a id="31-кто-иммунен-к-бунту"></a>
### 3.1. Who is affected

| Type | Can defect? |
|---|---|
| Ordinary units | No; rebellion requires `bmercenary = True`. |
| Mercenaries from the Diplomatic Center | Yes. |
| Buildings | No. |

<a id="32-score-бонус-противнику"></a>
<a id="32-дополнительные-очки-противнику"></a>
<a id="32-штраф-к-счёту-прежнего-владельца"></a>
### 3.2. Score penalty for the former owner

When a rebel mercenary transfers to the game-controlled side, the game
immediately subtracts `3 × score` from its former owner instead of the
ordinary `2 × score` [^1]. The new owner simultaneously receives the normal
`1 × score`; the unit's later death is processed separately. This changes
match statistics, but score does not determine victory or rating.

---

<a id="4-защита-от-голода-и-бунта"></a>
## 4. Preventing famine and rebellion

<a id="41-от-голода"></a>
### 4.1. Preventing famine

1. **Place Storehouses near Fields** so Food is delivered sooner.
2. **Do not recruit too much infantry early**: its `consume.food`
   value is usually higher than a Peasant's.
3. **Reduce the number of consuming units** if Food reserves are
   expected to shrink; dismiss surplus recruits.
4. **Keep Food in reserve**, especially before an attack that may
   draw Peasants away from work or get them killed.

<a id="42-от-бунта"></a>
### 4.2. Preventing rebellion

1. **Upgrade Gold Mines** to raise income and cover mercenary upkeep.
2. **Build the Diplomatic Center after an Academy and a pair of Gold
   Mines**, not before.
3. **Do not hire more mercenaries than Gold income (`income[gold]`)
   can support.**
4. **Use the Market** to sell Food or Wood for Gold before reserves
   become critically low.
5. **If rebellion has already begun,** restore the Gold balance immediately.
   On high difficulty, a mercenary force can disintegrate rapidly.

---

<a id="5-связь-с-другими-флагами"></a>
<a id="5-связь-с-другими-состояниями"></a>
## 5. Related states

| Flag | Description | File |
|---|---|---|
| `farmused = 0` | No counted non-building units remain; in an ordinary non-battle match, the player fails the existence check even if buildings remain (see [Victory, Defeat, and the End of a Match](../../docs_en/recon/systems/victory_conditions.md)). |
| `bfamine` | Does not lead to defeat by itself; kills units. |
| `brebellion` | Does not lead to defeat; transfers mercenaries to the game-controlled side. |
| `bleave` | The player surrendered through the interface. Defeat is immediate. |

`farmused` and `bfamine` are **different values**. The former counts
non-building units and participates in the player-existence check. The latter
means that Food is zero while consumption continues and triggers random death
checks.

---

<a id="6-открытые-вопросы"></a>
## 6. Open questions

1. The exact famine and rebellion check interval, in game seconds, at every
   game speed.
2. The distribution of losses between equal-sized Peasant and infantry
   groups.
3. The observed breakup time of identical mercenary groups at each
   difficulty.

<a id="источники"></a>
## Sources

[^1]: `data/scripts/lib/unit.script:3944-3948` — score modifier when the unit
      is removed from the former owner's counters during defection:

      ```pascal
      if (gPlayer[pl].brebellion) and bmercenary then
        scoremodifier := 3
      else
        scoremodifier := 2;
      ```

      Then `gPlayer[pl].counter.scores -= score * scoremodifier`.

[^2]: `data/scripts/lib/player.script:295-321` — main resource-consumption
      procedure. It sets the Food and Gold crisis flags when payment fails,
      then clears them when their conditions no longer apply.

[^3]: `data/scripts/units/unit.inc/nothing.inc:445-505` — `Nothing` state
      handler. For non-buildings without `bnohungry`, a successful check calls
      `_unit_SetTagStates(..., essential_death)`. `_misc_RandomInt =
      floor(random × 32768)`. The threshold-50 branch runs when
      `difficulty > 1` **or** `gbool_lan_isonlinecached`; on online difficulty
      0 or 1, a second independent check then runs with threshold 5 or 12.

[^4]: `data/scripts/units/unit.inc/nothing.inc:445-505` — the same handler's
      `brebellion` and `bmercenary` branch. The rebellion thresholds are
      Easy = 100, Normal = 200, and Hard or above = 6000 out of 32768.
      `gc_player_mercenaryind = MaxPlayerCount − 1` identifies the
      game-controlled recipient of defecting mercenaries.

[^5]: `data/scripts/lib/unit.script:3810, 3821` — increments
      `gPlayer.counter.resconsume[food]` when a unit is created.
      Buildings receive `bnohungry = True` in
      `data/scripts/lib/unit.script:471` (inside
      `SetObjBuildingBaseSettings`). The per-tick Food and Gold handler is
      `data/scripts/lib/player.script:280-322`.
