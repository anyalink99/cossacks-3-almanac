<a id="жрецы"></a>
<a id="священники"></a>
# Priests

[← Unit comparisons](README.md) · [← All comparisons](../README.md) · [← Quick reference](../../README.md)

The Priest is the only unit with a healing ability (`weapon.kind = heal`). Four national sids - `priest` (Catholic template), `pope` (Russia/Ukraine), `mullah` (Turkey/Algeria), `padre` (Piedmont). All have `pause = 0` (heal-“shot” is initiated by the target without reloading), but **range** and **healing power per tick** differ. The consumed gold upkeep is also different (`consume.gold` per game-second according to the rule `consume × 32 / 20000`).

| Unit | Sid | HP | Time (g-sec) | F | G | Heal/tact | Healing radius (tile) | Gold-upkeep (per tick = 1 game-sec) | Use nations |
|---|---|---:|---:|---:|---:|---:|---:|---:|---|
| **Mullah** | `mullah` | 75 | 15.0 | 30 | 10 | 15 | 9.38 | 15 (≈ 0.0240/g-sec) | Algeria, Turkey |
| **Padre** | `padre` | 90 | 25.0 | 50 | 40 | 30 | 7.5 | 40 (≈ 0.0640/g-sec) | Piedmont |
| **Pope** | `pope` | 75 | 20.0 | 40 | 20 | 25 | 6.56 | 20 (≈ 0.0320/g-sec) | Russia, Ukraine |
| **Priest** | `priest` | 100 | 20.0 | 60 | 25 | 20 | 7.5 | 20 (≈ 0.0320/g-sec) | Austria, Bavaria, Denmark, England, France, Hungary, Netherlands, Poland, Portugal, Prussia, Saxony, Scotland, Spain, Sweden, Switzerland, Venice |

> **Pause = 0**: the priest begins to “pump up” the target’s health immediately after choosing, without a cooldown between ticks. Actual healing rate = `healing_per_tick × ticks_per_second` (see [ticks_and_subticks.md](../../../../internals_en/engine/ticks_and_subticks.md) - the heal tick is controlled by the same `gc_time_to_frames` cycle).

> **Source of stats**: `unit.script:1151-1188` - general block `'priest','pope','mullah','padre'` plus `if (objprop.sid='X') then begin … end` chain for per-sid overrides.
