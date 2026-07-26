<a id="ограничения-скриптинга-при-модинге-dodamage-и-смерть-юнита"></a>
# Scripting restrictions when modding: DoDamage and unit death

Practical conclusions obtained during the development of the Deterministic Cossacks mod.
Describe engine behavior that is not directly documented in the source code.

> **Related documents:**
> [`combat_damage_pipeline` (recon)](../../docs_en/recon/world/combat/combat_damage_pipeline.md)
> - damage formula; [`animation_system.md`](animation_system.md)
> - order of calls during an attack.

---

<a id="1-структура-miscdodamage-miscext2script-line-250"></a>
## 1. Structure `_misc_DoDamage` (miscext2.script ~line 250)

The function is divided into two fundamentally different blocks:

**Block A - bookkeeping when killed** (`if TObj(pobj2).hp <= 0`, ~line 443):
- Awarding points to the attacker (`gPlayer[plInd].counter.scores`)
- Increment `TObj(pobj).kill`
- Enumeration `gc_argunit_inside` (kick units out of transport/mine)

**Block B - death trigger** (`if bProcessLogic`, ~line 510):
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
Block A and block B **not directly connected**: it is possible to enter block A without entering B
(if `bProcessLogic = false`), and vice versa.

`bSkipOnDeath` is set only in the peace-mode branch (~line 308/318).
In normal combat it is always `false`.

---

<a id="2-нельзя-убивать-атакующего-изнутри-miscdodamage"></a>
## 2. You cannot kill an attacker from within `_misc_DoDamage`

**Symptom:** `TObj(pobj).hp := 0` inside a kill block (block A) → unit freezes:
does not die, does not act, cannot be isolated.

**Cause:** C++ calls `_misc_DoDamage` in the middle of an attack sequence. After
returning from the script, the engine continues to process the attack for `goHnd`. If
the script managed to set `hp = 0`, block B of the same function calls
`_unit_SetTagStates(gc_statetag_essential_death)` - the unit receives a death state,
but the C++ attack sequence is not completed yet. The result is a state conflict.

**Output:** Any change in hp/status of ATTACKER (`goHnd/pobj`) from within
`_misc_DoDamage` is unreliable. Goal (`trgHnd/pobj2`) kill safely - engine
expects this.

---

<a id="3-рекурсивный-вызов-miscdodamage-вызывает-двойную-смерть"></a>
## 3. Recursive call `_misc_DoDamage` causes double death

When trying `_misc_DoDamage(goHnd, goHnd, 9999, weapind, weapkind)` from kill block:

1. Nested call: `TObj(pobj2).hp -= 9999` → block B → `_unit_SetTagStates(essential_death)` **first time**
2. The nested call is returned
3. The external call continues to work, reaches block B (~line 512): `TObj(pobj).hp <= 0` → `_unit_SetTagStates(essential_death)` **second time**

Double `_unit_SetTagStates(gc_statetag_essential_death)` breaks the animation
state machine - the unit gets stuck in an eternal attack animation.

`GameObjectExecuteStateByHandle(goHnd, 'OnDeath')` is protected by verification
`if (not TObj(pobj).bdead)`, but `_unit_SetTagStates(essential_death)` is not.

---

<a id="4-attackmaxdelay-нельзя-использовать-как-флагsentinel"></a>
## 4. `attackmaxdelay` cannot be used as a flag/sentinel

`attackmaxdelay` is read by the engine as the maximum cooldown attack time.
Setting `attackmaxdelay := 9999` effectively blocks the unit for 9999 g-sec -
he stops attacking completely. The field is not suitable for storing arbitrary
flags.

It's similarly dangerous to overuse `attackdelay` values >> for a weapon's normal pause.

---

<a id="5-безопасное-место-для-kill-trigger-извне-dodamage"></a>
## 5. Safe place for kill-trigger from outside DoDamage

Function `SearchEnemy` / retarget gate (unit.script ~line 8400) is called in
**regular update loop** of the unit, outside the attack sequence and outside `_misc_DoDamage`.
Install `hp := 0` + `_unit_SetTagStates(gc_statetag_essential_death)` here
works correctly.

Pattern: after killing `attackdelay` is set to ≥ 1.5 g-sec. Bye
`attackdelay > 0` retarget gate is called every tick. This creates a reliable
window for checking the post-kill state of the attacker without recursion.
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

Full cleanup function: removes from the minimap, clears orders, places
`bdead := True`, removes from player's counters. Never is not called from
scripts (only defined). Probably called from C++ directly or
is dead code. Forward link from the beginning of miscext2.script theoretically
works in DWS (two-pass compilation), but has hardly been tested.

---

<a id="7-gcargunitstolist--список-атакующих-юнита"></a>
## 7. `gc_argunit_stolist` - list of unit attackers
```pascal
var psto : Pointer = _misc_GetObjectArgData(hnd, gc_argunit_stolist);
var n : Integer = TIntegerList(psto).GetCount;
```
`n` = number of units **currently attacking** `hnd`. Available for anyone
handle - both the target and the attacker. Updated by the engine in real time.

---

<a id="8-порядок-вызовов-при-атаке-юнита"></a>
## 8. Order of calls when attacking a unit

Based on observations (exact C++ order unknown):

1. Attack animation reaches swing point → C++ callback → `_misc_DoDamage`
2. The animation ends → C++ → `_unit_ApplyAttackPause` (set to `attackdelay`)
3. The unit enters idle/retarget → `SearchEnemy` / retarget gate

`_unit_ApplyAttackPause` is called **after** `_misc_DoDamage`, not before.
Therefore, sentinel set in DoDamage is visible in `_unit_ApplyAttackPause` -
but only if the engine manages to call it before the next attack cycle.
In practice, it is more reliable to use retarget gate (item 5).
