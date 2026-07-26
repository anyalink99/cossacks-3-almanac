<a id="глоссарий-извлечённых-полей-игры"></a>
# Extracted game-field glossary

[← Technical documentation](../README.md)

These internal fields appear in `data.json`, game scripts, and generated
reports. Reader-facing documentation uses ordinary game terminology instead.

<a id="идентификация-объектов"></a>
## Object identification

| Field | Meaning |
|---|---|
| `sid` | Stable internal object identifier from `unit.script`, such as `bavcen` or `peaaus`. |
| `cid` | Numeric nation identifier. |
| `usage` / `usage_short` | Object role used by the AI and game formulas. |
| `commonsid` / `cluster` | Architectural group used by shared buildings. |
| `costpercent` | Price multiplier for each additional building of the same type. |
| `farm` | Increase to the population limit. |

<a id="экономика"></a>
## Economy

| Field | Meaning |
|---|---|
| `resefficiency[cid][restype]` | Current resource-gathering efficiency, as a percentage. |
| `consume[restype]` | Periodic resource upkeep, separate from construction or recruitment cost. |
| `peasantabsorber` | Number of peasants who can work inside the building. |
| `produce[restype]` | Resource income per worker inside a producing building. |
| `fieldlife` | Field durability modifier. |

<a id="боевые-поля-и-флаги-состояния"></a>
## Combat fields and state flags

| Field | Meaning |
|---|---|
| `bbuilt` | Whether construction is complete. An unfinished building receives only one third of its normal armor value. |
| `bcapture` | Whether the object can be captured. |
| `bnohungry` | Whether the object is exempt from food consumption and starvation losses. |
| `bmercenary` | Mercenary flag used by gold upkeep and rebellion mechanics. |
| `bfamine` | Player starvation state. |
| `brebellion` | Player mercenary-rebellion state. |
| `brised` | Whether a resource object is available for gathering. |
| `uniqrnd` | Deterministic per-object random number in the range `[0, 1)`. |
| `gc_obj_weapon_kind_*` | Weapon type that selects the target's matching protection value. |

<a id="пересчёт-времени"></a>
## Time conversion

| Field | Meaning |
|---|---|
| `gc_time_to_frames = 32` | Simulation frames in one game second. |
| `gc_buildtime_modifier = 10` | Additional multiplier used only for building construction time. |
| `slow / normal / fast = 7 / 10 / 14` | Simulation-speed levels. On Fast, one game second lasts about 0.71 real seconds. |
