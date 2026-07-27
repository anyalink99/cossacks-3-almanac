<a id="ограничения-скриптинга-при-модинге-dodamage-и-смерть-юнита"></a>
# Scripting Constraints: `DoDamage` and Unit Death

These practical findings from the Deterministic Cossacks mod document engine
behavior that is not explicit in the script sources.

> **Related documents:**
> [`combat_damage_pipeline` (recon)](../../docs_en/recon/world/combat/combat_damage_pipeline.md)
> — damage formula; [`animation_system.md`](animation_system.md)
> — call order during an attack.

---

<a id="1-структура-_misc_dodamage-miscext2script-line-250"></a>
## 1. Structure of `_misc_DoDamage` (`miscext2.script`, around line 250)

The function is divided into two fundamentally different blocks:

**Block A — death bookkeeping** (`if TObj(pobj2).hp <= 0`, around line 443):
- awards points to the attacker (`gPlayer[plInd].counter.scores`);
- increments `TObj(pobj).kill`;
- enumerates `gc_argunit_inside` to eject units from a transport or mine.

**Block B — death trigger** (`if bProcessLogic`, around line 510):
```pascal
// attacker (pobj / goHnd):
if (not bSkipOnDeath) and (pobj<>nil) and (TObj(pobj).hp<=0) then begin
   if (not TObj(pobj).bdead) then
   GameObjectExecuteStateByHandle(goHnd, 'OnDeath');
   _unit_SetTagStates(goHnd, gc_statetag_essential_death);
end;

// target (pobj2 / trgHnd):
if (TObj(pobj2).hp<=0) then begin
   GameObjectExecuteStateByHandle(trgHnd, 'OnDeath');
   _unit_SetTagStates(trgHnd, gc_statetag_essential_death);
end;
```
The blocks are **not directly coupled**: block A can run without block B
when `bProcessLogic = false`, and block B can run without block A.

`bSkipOnDeath` is set only in the peace-mode branch (~line 308/318).
In normal combat it is always `false`.

---

<a id="2-нельзя-убивать-атакующего-изнутри-_misc_dodamage"></a>
## 2. Do not kill the attacker from within `_misc_DoDamage`

**Symptom:** `TObj(pobj).hp := 0` inside a kill block (block A) → unit freezes:
it neither dies nor acts and cannot be selected.

**Cause:** C++ calls `_misc_DoDamage` in the middle of an attack sequence. After
the script returns, the engine continues processing the attack for `goHnd`.
If the script has set `hp = 0`, block B calls
`_unit_SetTagStates(gc_statetag_essential_death)`. The unit enters the death
state before the C++ attack sequence has finished, creating a state conflict.

**Conclusion:** changing the attacker's health or state (`goHnd` / `pobj`)
inside `_misc_DoDamage` is unreliable. Killing the target
(`trgHnd` / `pobj2`) is safe and expected by the engine.

---

<a id="3-рекурсивный-вызов-_misc_dodamage-вызывает-двойную-смерть"></a>
## 3. Recursive `_misc_DoDamage` calls trigger death twice

When trying `_misc_DoDamage(goHnd, goHnd, 9999, weapind, weapkind)` from kill block:

1. Nested call: `TObj(pobj2).hp -= 9999` → block B → `_unit_SetTagStates(essential_death)` **first time**
2. The nested call returns.
3. The outer call continues to block B (around line 512):
   `TObj(pobj).hp <= 0` → `_unit_SetTagStates(essential_death)` a
   **second time**.

Double `_unit_SetTagStates(gc_statetag_essential_death)` breaks the animation
state machine, leaving the unit stuck in an endless attack animation.

`GameObjectExecuteStateByHandle(goHnd, 'OnDeath')` is protected by the check
`if (not TObj(pobj).bdead)`, but `_unit_SetTagStates(essential_death)` is not.

---

<a id="4-attackmaxdelay-нельзя-использовать-как-флагsentinel"></a>
## 4. `attackmaxdelay` cannot be used as a flag/sentinel

The engine reads `attackmaxdelay` as the maximum attack cooldown.
`attackmaxdelay := 9999` effectively blocks the unit for 9,999 game seconds,
preventing it from attacking. The field cannot safely store arbitrary flags.

Likewise, `attackdelay` should not be set far above the weapon's normal
pause.

---

<a id="5-безопасное-место-для-kill-trigger-извне-dodamage"></a>
## 5. A safe kill trigger outside `DoDamage`

The `SearchEnemy` retarget gate in `unit.script`, around line 8400, runs
from the unit's **regular update loop**, outside both the attack sequence
and `_misc_DoDamage`. Setting `hp := 0` and calling
`_unit_SetTagStates(gc_statetag_essential_death)` there works correctly.

After a kill, `attackdelay` is at least 1.5 game seconds. While
`attackdelay > 0`, the retarget gate runs every tick, creating a reliable
window for checking the attacker's post-kill state without recursion.
```pascal
// unit.script retarget gate — safe kill trigger:
if (pobj<>nil) and (TObj(pobj).hp > 0) and (TObj(pobj).hp < 3)
and (TObj(pobj).attackdelay > 0) then begin
   TObj(pobj).hp := 0;
   _unit_SetTagStates(goHnd, gc_statetag_essential_death);
end
```
---

## 6. `_unit_DestroyObj` (miscext2.script:4205)

A full cleanup function that removes the object from the minimap, clears its
orders, sets `bdead := True`, and updates the player's counters. Scripts
define but never call it; it is either invoked directly from C++ or unused.
DWS should support the forward reference near the beginning of
`miscext2.script` through two-pass compilation, but this has not been
thoroughly tested.

---

<a id="7-gc_argunit_stolist--список-атакующих-юнита"></a>
## 7. `gc_argunit_stolist`: units attacking an object
```pascal
var psto : Pointer = _misc_GetObjectArgData(hnd, gc_argunit_stolist);
var n : Integer = TIntegerList(psto).GetCount;
```
`n` is the number of units **currently attacking** `hnd`. The list is
available for any handle, whether target or attacker, and the engine updates
it in real time.

---

<a id="8-порядок-вызовов-при-атаке-юнита"></a>
## 8. Order of calls when attacking a unit

Based on observations (exact C++ order unknown):

1. Attack animation reaches swing point → C++ callback → `_misc_DoDamage`
2. The animation ends → C++ → `_unit_ApplyAttackPause` (set to `attackdelay`)
3. The unit enters idle/retarget → `SearchEnemy` / retarget gate

`_unit_ApplyAttackPause` is called **after** `_misc_DoDamage`, not before.
Therefore, a sentinel set in `DoDamage` is visible in `_unit_ApplyAttackPause`,
but only if the engine manages to call it before the next attack cycle.
In practice, the retarget gate from §5 is more reliable.
