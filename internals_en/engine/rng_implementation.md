<a id="реализация-rng-в-cossacks-3"></a>
# Implementation of RNG in Cossacks 3

What `random` and `RandomExt` actually generate, how their state is stored, and
why `SetRandomKey` behaves the way it does.

> Read this alongside [`determinism_audit.md`](determinism_audit.md), which
> traces random-number use in mining and combat, and
> [`native_api.md` §2.4](native_api.md), which lists the engine's RNG streams.

> **This document has been cross-checked against the private
> `cossacks-deep` analysis (`findings/rng_implementation.md`), which records
> exact addresses, seed layouts, and formulas.** Sections 1–10 below describe
> the verified behavior without publishing binary offsets.

> **History of edits.** In one of the early iterations (May 18), this document
> incorrectly claimed that `Random` and `RandomExt` shared one 64-bit seed.
> Decompilation of `_System_Random` instead showed a separate `RandSeed` cell
> from Delphi's `System` unit, independent of the 64-bit state installed by
> `SetRandomKey` and `SetRandomExtKey64`. The original observation therefore
> stands: `Random` and `RandomExt` are independent streams. Older provisional
> notes should be read in light of the final model presented here and in
> `native_api.md` §2.4: four independent seed stores.

<a id="1-общая-картина"></a>
## 1. The big picture

C3 scripts use (in descending frequency):

| Function | Calls in scripts | What |
|---|---:|---|
| `random` | 100 | Floating-point value in [0, 1), from the global stream |
| `RandomExt` | 60 | Floating-point value in [0, 1), from the parallel extended stream |
| `SetRandomKey(seed: Integer)` | 4 | Reseeds the global stream |
| `SetRandomExtKey64(k0, k1)` | 0 | Reseeding an extended 64-bit stream (in the exe, no scripts) |

These functions are registered with DWS by the host engine. The standard
`random` path uses Delphi's `Random` and `RandSeed`; the extended path keeps
separate 64-bit state, as described below.

<a id="2-алгоритм-delphi-random"></a>
## 2. Delphi algorithm `Random`

`System.Random` in Delphi - linear congruent generator (LCG):
```pascal
RandSeed := RandSeed * $08088405 + 1;
// $08088405 = 134775813
// addend = 1
// modulus = 2^32 (natural Cardinal overflow)
```
Convert to float:
```pascal
function Random: Double;
begin
    Result := RandSeed / $FFFFFFFF;
end;
```
Properties:
- **Period:** 2³² ≈ 4.29 × 10⁹ values.
- **Seed:** 32-bit `Integer` via `SetRandomKey(seed)`.
- **One global `RandSeed`** for the entire process (not per-thread).

This is a **well known** Delphi constant (same as in Borland
Pascal since the late 80s). Nothing esoteric.

<a id="3-реализация-randomext"></a>
## 3. Implementation of `RandomExt`

`RandomExt` is a **64-bit LCG**, not Xorshift. Algorithm:
`seed64 := seed64 * M + I` with specific constants, executed
like 64-bit arithmetic on a 32-bit ISA via Delphi RTL helpers
(`__llmul` / `__lladd`).

**State** is stored in a separate 64-bit cell (hereinafter referred to as “extended
seed"), which is controlled by:

- `SetRandomKey(key: Integer)` - writes the younger half = `key`,
  major via sign-extend (= 0 for positive, = −1 = `0xFFFFFFFF`
  for negative ones).
- `SetRandomExtKey64(const key0, key1: Integer)` - writes the entire 64-bit
  entire cell (bottom = `key0`, top = `key1`).

**`Random` uses a different cell** - standard 32-bit Delphi
`System.RandSeed`. This is a **different** global variable. So
`Random` and `RandomExt` are indeed sitting on independent seeds.

An important naming subtlety follows from this: the name `SetRandomKey` sounds
as if it sets the seed for `Random()`, but actually controls
extended seed** (the same one that reads `RandomExt`). To sow
`Random` itself, you need either Delphi's `Randomize`, or direct recording
in `System.RandSeed` - DWS does not provide this option. That is
script pattern "`SetRandomKey(N); arg.frnd := random;`" found
to `lib/unit.script`, synchronizes not `random`, but the next call
`RandomExt` - but the script author could have expected different behavior.

Details with addresses and decompilation - in private
`cossacks-deep/findings/rng_implementation.md` §§ 1–3.

<a id="4-семантика-глобальный-rng"></a>
## 4. Semantics of “global RNG”

From `determinism_audit.md` we knew that `random` is global, rummaging around
between:

- gameplay logic (target selection, headshots, stump placement),
- UI / GUI effects (`gui.script` calls `random` for random
  combobox material, for example),
- AI solutions.

This means: **GUI "steals" entropy from gameplay**, and vice versa. If
two clients in a multiplayer game lose differently replayable
GUI, their global `RandSeed` diverge, and gameplay will also diverge.

Protection occurs through **local reseeding** before gameplay-critical
operation (see §5) - `SetRandomKey` puts the extended seed, and
subsequent series of `RandomExt` calls becomes reproducible
no matter what the GUI does with `random`. Visual/UI code that
uses only `random` (not `RandomExt`), mutates only
`System.RandSeed`, without touching the extended seed - this is the actual
a division through which gameplay maintains determinism.

Separate named streams with their own state - `AirWeatherRandom`,
`MakeRandomClouds`-derivatives, map-generators - live completely outside
both common seed cells.

<a id="5-главный-паттерн-детерминизма-пересев-перед-операцией"></a>
## 5. The main pattern of determinism: reseeding before surgery

In scripts `lib/unit.script` 4 calls `SetRandomKey` - all
made **specifically for synchronization**. Context from code:
```pascal
// unit.script — before forming a squad
SetRandomKey(floor(random * gc_MaxInt));
// needed to sync multiplayer arg.frnd
arg.frnd := random;
```
```pascal
// unit.script — before a calculation that depends on an individual unit
SetRandomKey(floor(TObj(pobj).uniqrnd * gc_MaxInt));
// sync multiplayer
```
**Architectural pattern:** before an operation requiring the same
results on all clients, the script **reseeds the global RNG**
from a source that is **guaranteed to be the same on all clients**:

| Source of reseeding | Where is it determined from |
|---|---|
| `random` (previous value) | If there was already synchronization before, then it is the same. |
| `TObj(pobj).uniqrnd * gc_MaxInt` | Unit `uniqrnd` - fixed at spawn and **synchronously saved** (see field `uniqrnd` in [`server_sync_packet_format.md` §3.1](server_sync_packet_format.md)). |

This is **not a lockstep**, but a **per-decision deterministic seed**. Same
the decision itself made on the server and on the client (for example, “what
formation of units in a squad") will give the same result bit-for-bit, not
requiring synchronized RNG state.

<a id="6-воспроизводимость-значений"></a>
## 6. Reproducibility of values

Taking into account §2 (LCG) - by setting `SetRandomKey(seed)`, you can completely
reproduce the next N values `random`. Simple Python model:
```python
def delphi_random_stream(seed):
    s = seed & 0xFFFFFFFF
    while True:
        s = (s * 134775813 + 1) & 0xFFFFFFFF
        yield s / 0xFFFFFFFF

# Example for seed=42:
g = delphi_random_stream(42)
print([next(g) for _ in range(5)])
# [0.5263867462985266, 0.4017018212098335, 0.7770079020410776, ...]
```
This means - **for each `uniqrnd` unit you can predict in advance
any RNG-dependent value** (headshot, projectile spread, target selection
of equal candidates). The simulator can use this to
repeating battles from saves.

<a id="7-что-насчёт-mt-19937"></a>
## 7. What about MT-19937

The standard DWS (on GitHub) provides **both LCG (`Random`) and
Mersenne Twister** (via `dwsRandomFunctions.pas`). But in C3 the name
`Random` in exe is registered as **regular 32-bit LCG**, which
confirmed by decompilation: `Random()` wraps `System._Random`
with the classic Delphi formula `seed := seed * 0x8088405 + 1`.

Therefore, although MT-19937 is available in DWS, it is not available in C3
used**. `RandomExt` - also not MT, but a 64-bit LCG over **its own
separate** extended seed (see §3).

<a id="8-связь-с-другими-rng-потоками"></a>
## 8. Communication with other RNG streams

The engine has **four independent seed storages**, each with its own
algorithm from above:
```
Standard Delphi RandSeed (32-bit)
                        ↑
                  Random  (Delphi 32-bit LCG: seed = seed * 0x8088405 + 1)
                        (Randomize / direct System.RandSeed write — DWS does not expose it)

Extended 64-bit seed
                        ↑
                  RandomExt  (64-bit LCG with its own constant pair)
                        ↑
                  SetRandomKey (sign-extend 32→64), SetRandomExtKey64 (full 64-bit)

MapGenerator seed       (64-bit, separate storage in map state)
                        ↑
                  SetMapGeneratorRandomKey

GlobalMapGenerator seed (64-bit, separate storage)
                        ↑
                  SetGlobalMapGeneratorRandomKey

(Separate weather and cloud channels use the AirWeatherRandom family; not shown)
```
All four storages are **physically different**: calling any algorithm
affects only its seed. This explains why the pair `(randkey0,
randkey1)` to play the map - standard representation in
save and lobby (see
[`map_generation_pipeline.md`](../../docs_en/recon/world/map/map_generation_pipeline.md) §12)
and why gameplay-critical paths in scripts turn into
`SetRandomKey + RandomExt` - this guarantees determinism
extended flow regardless of what the UI does with the normal one
`random`.

<a id="9-что-это-значит-для-симулятора"></a>
## 9. What does this mean for the simulator

For the extraction model (see.
[`docs/recon/world/peasant_extraction.md`](../../docs_en/recon/world/economy/peasant_extraction.md)),
if we want to **bit-accurately** reproduce the loot from a given save:

1. You cannot read `RandSeed` - it is not saved as a separate field.
2. Instead, we count `uniqrnd` for each peasant (there is
   sync snapshot).
3. For each RNG-dependent operation in the hot-loop (for example, selecting
   points on the tree) the simulator must **know reseeding** in the script and
   repeat them.
4. Real implementation - go through `lib/unit.script` `_unit_DoExtract`
   and for each `random` call, determine whether there was
   `SetRandomKey` just before.

This is the plan for the Level C simulator
[`project_level_c_simulator_plan.md`](../project/architecture.md)
(if the simulator ever aims for bit-perfect
reproducibility rather than statistical accuracy).

<a id="10-открытое-и-закрытое"></a>
## 10. Open and closed

| Item | Status |
|---|---|
| **Exact implementation of `RandomExt`** | **Closed.** 64-bit LCG on a separate 64-bit seed cell (not the same one as `Random`). See §3, §8 and private `cossacks-deep/findings/rng_implementation.md`. |
| **Relationship `SetRandomKey` and `Random`** | **Closed.** `SetRandomKey` controls an extended seed (= seed `RandomExt`), not the standard `RandSeed`. Despite the name, `Random()` does not depend on `SetRandomKey` - see §3. |
| **Algorithms `MapGenerator` / `GlobalMapGenerator`** | Partially. Seed storages are confirmed to be separate (see §8). The algorithms themselves for generating values have not been analyzed; will be passed when we take on `_DoGenerate`. |
| **`PlayerCubeRandomValue`** | Partially. No RNG-seed mutates - it is a **pre-computed per-player nonce**, generated in advance (probably when the player connects) and stable throughout the match. The exact moment of initialization has not been confirmed. More details: private `findings/rng_implementation.md`. |
| **Does `_DoGenerate` use the regular `Random()`** (which would silently mutate `System.RandSeed` during map generation) | Open. Next step on the RNG topic. |
| **Is `System.RandSeed` synchronized over the network** at the start of the match | Open. Candidates are package handlers `EconomyPackage`/sync. |
| **Race condition between `PathDataThread*` and main `bProcess` on RNG calls** | Open. The main suspect due to unexplained desyncs. |
