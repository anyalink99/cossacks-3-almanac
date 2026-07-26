<a id="deterministic-cossacks--cossacks-3-mod"></a>
# Deterministic Cossacks - Cossacks 3 mod

**English** · [Русский](README.md)

Two areas of change: **RNG determinism** and **anti-snowball combat mechanics**.

---

<a id="на-каких-юнитов-распространяется"></a>
## Which units does it apply to?

**All combat changes (clauses 2.1–2.5) apply only to infantry and horses:**

| Type | usage constants |
|---|---|
| Infantry | `lightinfantry`, `grenadier`, `shooter`, `archer` |
| Horses | `fasthorse`, `hardhorse`, `horseshooter` |

Cannons, buildings, ships, priests and all other units receive stock behavior in everything related to damage, target selection and post-kill effects.

**Headshot +12** - additionally limited to musketeers and archers (`bCanHeadShot`, weapkind = bullet/arrow). Horses are invulnerable as in stock.

**Peasants** - RNG determinism of production only.

---

<a id="1-детерминизм-rng"></a>
## 1. RNG Determinism

10 calls `random` in hot-path mining and target selection replaced with
`SetRandomKey(seed) + random` with a seed from a persistent game-state.
The same save after repeated downloads → the same outcomes.

<a id="extraction-5-сайтов"></a>
### Extraction (5 sites)

| File | String | What |
|---|---|---|
| misc.script | 2790 | `FindResourceToExtract`: starting index in resgrid cell |
| misc.script | 2801 | `FindResourceToExtract`: wood vs stone |
| unit.script | 4055 | `SearchResourceInRadius`: standtime gate |
| unit.script | 4114 | `SearchResourceInRadius`: bskipcheck |
| unit.script | 4120 | `SearchResourceInRadius`: candidate starting index |

<a id="combat-4-сайта"></a>
### Combat (4 sites)

| File | String | What |
|---|---|---|
| unit.script | 4796 | `SearchEnemyInCellShips`: rndind |
| unit.script | 4872 | `SearchEnemyInCell`: rndind |
| unit.script | 4992 | `SearchEnemyScanCellsLongRange`: dx |
| unit.script | 4993 | `SearchEnemyScanCellsLongRange`: dy |

---

<a id="2-anti-snowball-механики"></a>
## 2. Anti-snowball mechanics

### 2.1 Headshot (miscext2.script:420, 436, 437)

**Stock:** 5% chance of → `+floor(uniqrnd×500)` damage. Mediume “raw” bonus 250,
but due to overkill, the effective bonus depends on the target’s HP.
`E[min(uniform[0,500], H)] = H − H²/1000` for `H ≤ 500`.

**Mod:** always works for `bCanHeadShot` → deterministic bonus,
calculated based on the target's max HP:

`bonus = floor((H − H²/1000) × 0.05)`, where `H = clamp(maxhp, 0, 500)`

| maxhp goals | bonus |
|---|---|
| 50 (early pikeman) | +2 |
| 80 (typical infantryman) | +3 |
| 100 (heavy infantry) | +4 |
| 200 (rates) | +8 |
| 500+ (heavy units) | +12 |

Dispersion and overkill have been eliminated, effective DPS is the same as stock.

**Suicidal shot (musketeers only, weapkind=bullet):** 5% shot chance
against **any target** deals **250 damage** and reduces the musketeer's HP to **1**.
Complete suicide (instant death in the retarget window via marker) triggers
**only if the target is a shooter** (`shooter` or `horseshooter`); by
For melee/archers, the musketeer simply remains at 1 hp without auto-death.
Bypasses all other damage modifiers.

<a id="22-модификаторы-урона-miscext2script437"></a>
### 2.2 Damage modifiers (miscext2.script:437)

Apply to the blow of **infantry and horses**, and **only when the attacker and the victim
stat-identical** - coincide at the same time `usage` + `maxhp` + `weapon[0].damage`.
This gives "balancing only in equal combat": national variants of one unit
with copied stats (for example, many European musketeers) pass
check, but really different units - no.

Examples:

| Couple | Check | Result |
|---|---|---|
| Russian musketeer vs Polish musketeer (stats copied) | usage/maxhp/damage match | modifiers are applied |
| Pikeman (90 hp) vs Rondashir (100 hp) | different maxhp | no modifiers apply |
| Russian pikeman (90 hp) vs Turkish pikeman (95 hp) | different maxhp | no modifiers apply |
| Musketeer vs pikeman | different usage and stat | no modifiers apply |

In cross-stat skirmishes, damage is dealt according to the stock formula (base - armor + squad bonuses).

| Condition | Effect | Logic |
|---|---|---|
| The target already has attackers | 2nd: ×0.75 / 3rd: ×0.50 / 4th+: ×0.30 | pile-on loses effectiveness |
| Attacker `hp > 80% maxhp` | ×0.80 (−20%) | fresh unit hits weaker |
| Attacker `hp < 50% maxhp` | ×1.20 (+20%) | wounded unit hits harder |
| The attacker is attacked by N enemies (cap 5) | ×(1 + N×0.50), max ×3.50 | surrounded unit hits harder |

<a id="23-пост-kill-эффекты-miscext2script463"></a>
### 2.3 Post-kill effects (miscext2.script:463)

After each kill by **infantry or horse**:

- **Retarget delay:** `attackdelay := max(attackdelay, 1.5 g-sec)` - the unit is not searching
  new target until delay expires.
- **Fatigue:** only applies when killing a unit **of the same combat category**.
  Melee fighters (`lightinfantry`, `grenadier`, `fasthorse`, `hardhorse`) get tired
  from melee killing; arrows (`shooter`, `archer`, `horseshooter`) - from
  killing shooters. Size: infantry - `-15% maxhp`; horses - `-5% maxhp`.
  Minimum 1 hp - fatigue does not kill directly.
- **Near-death kill:** only triggers on **same-category** kills when
  fatigue brought `hp < 3` - or with a suicidal shot from a musketeer. Technically:
  same-cat kill sets the marker `attackdelay := 100.0`, retarget gate checks
  `attackdelay > 50.0` and kills (see paragraph 2.5). Cross category and normal damage
  before `hp < 3` does not cause death.

Chain of fatigue (same-category): infantryman (maxhp ~80) loses 12 hp per
killing another melee combatant. After ~6 such kills, hp drops to 1.
On next kill hp=1 < 3 → death in retarget gate. Arrows similar
get tired of killing shooters.

<a id="24-выбор-цели--anti-clumping-unitscript5127-5191-5194"></a>
### 2.4 Target selection - anti-clumping (unit.script:5127, 5191, 5194)

Applies only when the target is looking for **infantry or horse**.

Stock C3: `relativeDist := distSqr × (1 + pstolist.count × K)`, K=0.1/0.125.

**Mod:** K raised to **0.5** for all three scans (long-range, melee, ranged).

| Attacking targets | Visible distance multiplier |
|---|---|
| 0 | ×1.0 |
| 1 | ×1.5 |
| 2 | ×2.0 |
| 3 | ×2.5 |

Additionally: targets with `hp < 50% maxhp` receive another ×2.5 to the distance -
units bypass the wounded and switch to fresh ones. This also applies to the dying
(`hp < 3`) - they are also depriority.

### 2.5 Retarget gate (unit.script:8400)

Applies only to **infantry and horses**.

- `attackdelay > 0` - the unit is not looking for a new target (forced idle).
- `hp < 3` + `attackdelay > 50.0` - death (`hp := 0` + `gc_statetag_essential_death`).
  The `attackdelay > 50` marker is placed only in the kill block with same-cat fatigue,
  bringing hp to < 3, or in a suicide shot - therefore it works strictly in the same-cat
  logic.

---

<a id="как-работает-anti-snowball-в-совокупности"></a>
## How anti-snowball works in total

Stock C3 problem: in symmetrical combat, the first few deaths create
numerical superiority → the winner receives “free” attacks on the remaining
→ cascade. 100v100 → 0 vs 40.

The mod attacks the cascade from several sides:

1. **Pile-on penalty** reduces the effectiveness of numerical superiority during an attack.
2. **Fresh penalty** reduces damage from “winners” with full HP.
3. **Outnumbered bonus** strengthens those surrounded, increasing the cost of encirclement.
4. **Fatigue** makes the “winners” fragile after killing gunshots.
5. **Near-death kill** disables units that have accumulated fatigue.
6. **Retarget delay** breaks chains of immediate switching to the next target.
7. **Suicidal shot** adds risk for musketeers with a powerful shot.
8. **Anti-clumping K=0.5** gently reduces the probability of pile-on when selecting a target.

---

<a id="как-собрать"></a>
## How to assemble
```bash
cd c:/projects/other/cossacks
python "mods/Deterministic Cossacks/build.py"
```
Reads original `lib/{misc,miscext2,unit}.script` from `$COSSACKS3_PATH`
(default `C:\Program Files (x86)\Steam\steamapps\common\Cossacks 3`),
applies patches, writes the result to `mods/Deterministic Cossacks/build/`.
```bash
python "mods/Deterministic Cossacks/build.py" --install
```
Additionally, copies to `<game>/mods/` and writes to `mods.ini`.

<a id="если-патч-не-находит-строку"></a>
### If the patch does not find the line

If the game has been updated and the lines have shifted, `build.py` will display
`RuntimeError: original line not found` or warning `drift > 5`.
Update `expected_line` and `original` to `PATCHES` to `build.py`.

---

<a id="ограничения"></a>
## Limitations

- **Async pathfinding** (`PathDataThread*`) - not available to the script, residual
  source of dispersion.
- **`_weapon_CalcShotDispertion`** — uses `RandomExt`, stock-bug engine;
  without `SetRandomExtKey64` it is not patched.
- **Adaptive game speed** - on different computers it takes equal real-time
  different game-time; compare outcomes by g-time.

---

<a id="откат"></a>
## Rollback

- In `<game>/mods/mods.ini` put `dis = True`, or
- Remove `<game>/mods/Deterministic Cossacks/`.

The original scripts in `<game>/data/scripts/` are not touched.

---

<a id="структура"></a>
## Structure
```
mods/Deterministic Cossacks/
├── README.md
├── build.py           ← patcher
├── src/
│   └── mod.ini        ← metadata
└── build/             ← generated build output (ignored by Git)
    └── Deterministic Cossacks/
        ├── mod.ini
        └── data/scripts/lib/
            ├── misc.script
            ├── miscext2.script
            └── unit.script
```
<a id="дополнительно"></a>
## Additional

- [internals/engine/script_modding_constraints.md](../../internals_en/engine/script_modding_constraints.md) —
  limitations of DWS scripting: why you can’t kill an attacker from within
  DoDamage, double essential_death bug, safe retarget gate pattern.
- [internals/engine/rng_implementation.md](../../internals_en/engine/rng_implementation.md) §3 —
  SetRandomKey vs SetRandomExtKey64.
- [docs/recon/world/economy/peasant_extraction.md](../../docs_en/recon/world/economy/peasant_extraction.md) —
  directory of extraction RNG sites.
