<a id="жрецы"></a>
<a id="священники"></a>
# Priests

[← Unit comparisons](README.md) · [← All comparisons](../README.md) · [← Quick reference](../../README.md)

Priests heal allied units instead of attacking. The four canonical variants—Priest, Pope, Mullah, and Padre—differ in durability, cost, healing range, healing strength, and Gold upkeep. Internal identifiers are included only for reference.

| Unit | Internal ID | Health | Training time (game s) | Food | Gold | Healing per update | Healing range (cells) | Gold upkeep (per game s) | Nations |
|---|---|---:|---:|---:|---:|---:|---:|---:|---|
| **Mullah** | `mullah` | 75 | 15.0 | 30 | 10 | 15 | 9.38 | 15 (≈ 0.0240/game s) | Algeria, Turkey |
| **Padre** | `padre` | 90 | 25.0 | 50 | 40 | 30 | 7.5 | 40 (≈ 0.0640/game s) | Piedmont |
| **Pope** | `pope` | 75 | 20.0 | 40 | 20 | 25 | 6.56 | 20 (≈ 0.0320/game s) | Russia, Ukraine |
| **Priest** | `priest` | 100 | 20.0 | 60 | 25 | 20 | 7.5 | 20 (≈ 0.0320/game s) | Austria, Bavaria, Denmark, England, France, Hungary, Netherlands, Poland, Portugal, Prussia, Saxony, Scotland, Spain, Sweden, Switzerland, Venice |

> **Reload time is zero:** a Priest begins healing as soon as a target is selected. The actual healing rate is `healing_per_update × updates_per_second`; see [ticks and subticks](../../../../internals_en/engine/ticks_and_subticks.md).

> **Source:** `unit.script:1151-1188` defines the shared Priest settings and the per-variant overrides.
