<a id="реализация-rng-в-cossacks-3"></a>
# RNG Implementation in Cossacks 3

What `random` and `RandomExt` actually generate, how their state is stored, and
why `SetRandomKey` behaves the way it does.

> Read this alongside [`determinism_audit.md`](determinism_audit.md), which
> traces random-number use in resource gathering and combat, and
> [`native_api.md` §2.4](native_api.md), which lists the engine's RNG streams.

> **This document has been cross-checked against the private
> `cossacks-deep` analysis (`findings/rng_implementation.md`), which records
> exact addresses, seed layouts, and formulas.** Sections 1–10 below describe
> the verified behavior without publishing binary offsets.

<a id="1-общая-картина"></a>
## 1. Overview

C3 scripts use (in descending frequency):

| Function | Calls in scripts | Purpose |
|---|---:|---|
| `random` | 100 | Floating-point value in [0, 1), from the global stream |
| `RandomExt` | 60 | Floating-point value in [0, 1), from the parallel extended stream |
| `SetRandomKey(seed: Integer)` | 4 | Reseeds the extended stream |
| `SetRandomExtKey64(k0, k1)` | 0 | Reseeds the full 64-bit extended stream (present in the executable, unused by scripts) |

These functions are registered with DWS by the host engine. The standard
`random` path uses Delphi's `Random` and `RandSeed`; the extended path keeps
separate 64-bit state, as described below.

<a id="2-алгоритм-delphi-random"></a>
## 2. Delphi's `Random` Algorithm

Delphi's `System.Random` is a linear congruential generator (LCG):
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
- **Seed:** a 32-bit `Integer` stored in `System.RandSeed`.
- **One global `RandSeed`** for the entire process (not per-thread).

This is a **well-known** Delphi constant, used since the Borland Pascal era.

<a id="3-реализация-randomext"></a>
## 3. Implementation of `RandomExt`

`RandomExt` is a **64-bit LCG**, not Xorshift. Its recurrence is
`seed64 := seed64 * M + I` with specific constants, executed
as 64-bit arithmetic on a 32-bit ISA through Delphi RTL helpers
(`__llmul` / `__lladd`).

Its **state** is stored in a separate 64-bit cell, referred to below as the
“extended seed.” It is controlled by:

- `SetRandomKey(key: Integer)` — writes `key` to the low half and
  sign-extends it into the high half (`0` for positive values and
  `0xFFFFFFFF` for negative values).
- `SetRandomExtKey64(const key0, key1: Integer)` — writes the full 64-bit
  state (low half = `key0`, high half = `key1`).

**`Random` uses a different state cell**: Delphi's standard 32-bit
`System.RandSeed`. This is a **different** global variable. So
`Random` and `RandomExt` have independent seeds.

An important naming subtlety follows from this: the name `SetRandomKey` sounds
as if it seeds `Random()`, but it actually controls the **extended seed** used
by `RandomExt`. Seeding `Random` itself requires Delphi's `Randomize` or a
direct write to `System.RandSeed`; DWS exposes neither option. Consequently,
the pattern `SetRandomKey(N); arg.frnd := random;` found in `lib/unit.script`
does not synchronize `random`; it prepares the next `RandomExt` call.

Addresses and decompilation details are recorded in the private
`cossacks-deep/findings/rng_implementation.md` §§ 1–3.

<a id="4-семантика-глобальный-rng"></a>
## 4. Semantics of “global RNG”

As established in `determinism_audit.md`, `random` is global and shared by:

- gameplay logic (target selection, headshots, stump placement),
- UI / GUI effects (`gui.script` calls `random` for random
  combo-box material, for example),
- AI decisions.

This means that **the GUI consumes values from the same sequence as gameplay**,
and vice versa. If two multiplayer clients execute a different set of
GUI-side random calls, their global `RandSeed` values diverge, potentially
affecting gameplay calls as well.

Gameplay-critical operations avoid this problem through **local reseeding**
(see §5): `SetRandomKey` sets the extended seed, making the following
`RandomExt` sequence reproducible regardless of what the GUI does with
`random`. Visual and UI code that
uses only `random` (not `RandomExt`), mutates only
`System.RandSeed` without touching the extended seed. This separation is what
allows critical calculations to remain deterministic.

Separate named streams with their own state—`AirWeatherRandom`,
`MakeRandomClouds` derivatives, and the map generators—remain independent of
both general-purpose seed cells.

<a id="5-главный-паттерн-детерминизма-пересев-перед-операцией"></a>
## 5. The Main Determinism Pattern: Reseeding Before an Operation

`lib/unit.script` contains four calls to `SetRandomKey`, all made
**specifically for synchronization**. Their context is:
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
**Architectural pattern:** before an operation that must produce the same
result on every client, the script **reseeds the extended RNG**
from a source that is **guaranteed to be the same on all clients**:

| Seed source | Why it is deterministic |
|---|---|
| `random` (previous value) | It is identical if the preceding state was already synchronized. |
| `TObj(pobj).uniqrnd * gc_MaxInt` | A unit's `uniqrnd` is fixed at spawn and **saved as synchronized state** (see `uniqrnd` in [`server_sync_packet_format.md` §3.1](server_sync_packet_format.md)). |

This is **not lockstep**, but a **deterministic seed for each decision**. The
same calculation on the server and client—for example, choosing a squad
formation—can produce an identical bit-for-bit result without maintaining one
continuously synchronized RNG state.

<a id="6-воспроизводимость-значений"></a>
## 6. Reproducibility of values

Given the LCG in §2, setting a seed allows the next N values in the
corresponding stream to be reproduced. A simple Python model for Delphi's
`Random` stream is:
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
This means that **a unit's `uniqrnd` can make its seeded RNG-dependent values
predictable**, including projectile dispersion and choices among equivalent
candidates. A simulator can use this property to reproduce battles from saves.

<a id="7-что-насчёт-mt-19937"></a>
## 7. What About MT-19937?

The standard DWS distribution provides **both an LCG (`Random`) and
Mersenne Twister** (via `dwsRandomFunctions.pas`). But in C3 the name
`Random` is registered by the executable as the **ordinary 32-bit LCG**.
Decompilation confirms that `Random()` wraps `System._Random`
with the classic Delphi formula `seed := seed * 0x8088405 + 1`.

Therefore, although DWS supports MT-19937, C3 **does not use it**.
`RandomExt` is not MT either; it is a 64-bit LCG over **its own
separate** extended seed (see §3).

<a id="8-связь-с-другими-rng-потоками"></a>
## 8. Relationship to Other RNG Streams

The engine has **four independent seed stores**, each used by its own
algorithm:
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
All four stores are **physically separate**: calling one algorithm affects only
its own seed. The pair `(randkey0, randkey1)` is the standard representation of
the map-generation seed in saves and the lobby (see
[`map_generation_pipeline.md`](../../docs_en/recon/world/map/map_generation_pipeline.md) §12).
Gameplay-critical script paths use `SetRandomKey + RandomExt` so that the
extended stream remains deterministic regardless of the UI's calls to ordinary
`random`.

<a id="9-что-это-значит-для-симулятора"></a>
## 9. Implications for the Simulator

For the resource-gathering model (see
[`peasant_extraction.md`](../../docs_en/recon/world/economy/peasant_extraction.md)),
to reproduce resource gathering from a save **bit for bit**:

1. The simulator cannot read `RandSeed` because it is not saved as a separate
   field.
2. Instead, use each peasant's `uniqrnd`, which is present in the
   synchronization snapshot.
3. For every RNG-dependent operation in the hot loop—for example, selecting a
   point on a tree—the simulator must reproduce the script's reseeding logic.
4. An implementation must inspect `_unit_DoExtract` in `lib/unit.script` and
   determine whether each `random` call is preceded by `SetRandomKey`.

This is the long-term path for the Level C simulator described in
[`architecture.md`](../project/architecture.md), if it ever aims for
bit-perfect rather than statistical reproducibility.

<a id="10-открытое-и-закрытое"></a>
## 10. Open and Resolved Questions

| Item | Status |
|---|---|
| **Exact implementation of `RandomExt`** | **Resolved.** A 64-bit LCG with a seed cell separate from `Random`. See §§3 and 8 and the private `cossacks-deep/findings/rng_implementation.md`. |
| **Relationship between `SetRandomKey` and `Random`** | **Resolved.** `SetRandomKey` controls the extended seed used by `RandomExt`, not the standard `RandSeed`. Despite its name, `Random()` does not depend on `SetRandomKey`; see §3. |
| **`MapGenerator` / `GlobalMapGenerator` algorithms** | Partially resolved. Their seed stores are confirmed to be separate (see §8), but the value-generation algorithms have not yet been analyzed. That requires studying `_DoGenerate`. |
| **`PlayerCubeRandomValue`** | Partially resolved. It does not mutate an RNG seed; it is a **precomputed per-player nonce**, probably generated when the player connects and stable throughout the match. Its exact initialization point is still unknown. See the private `findings/rng_implementation.md`. |
| **Does `_DoGenerate` use the regular `Random()`** (which would silently mutate `System.RandSeed` during map generation) | Open. Next step on the RNG topic. |
| **Is `System.RandSeed` synchronized over the network** at the start of the match | Open. Candidates are package handlers `EconomyPackage`/sync. |
| **Race condition between `PathDataThread*` and the main `bProcess` RNG calls** | Open. This is the leading suspect for otherwise unexplained desynchronizations. |
