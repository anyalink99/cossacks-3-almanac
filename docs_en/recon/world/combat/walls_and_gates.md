<a id="recon-стены-и-ворота"></a>
# Recon: walls and gates

Deep analysis: how wall clusters are arranged (`gWallSystem` /
`TWallCluster`), how the segments are built by peasants than the gates
different from a regular wall, what happens when you try to capture.

## TL;DR

- Wall - building with `usage = gc_obj_usage_hardwall` or
  `gc_obj_usage_weakwall` and the flag `bwall = True` [^1]. The player "draws"
  line with the mouse, after clicking unfinished segments appear
  (`bbuilt = False, hp = 10`), and the peasants build them **like ordinary ones
  buildings** via standard path `_player_ConstructBuildingList` →
  `_player_OrderUnitsToBuild` [^2][^3].
- Wall segment - 1 × 1 tile. Long Wall - Sequence
  segments in `TWallCluster` [^4].
- Builder slots for each segment are taken from
  `gCustomBuildPointsWall[wallvariation]` (source -
  `data/game/var/wallcustom.cfg`); variation = 0 is treated as
  ordinary building [^5].
- All 21 nations have a **picket fence** (`ukrwwa` / `ukrwga`). **Stone
  wall** (`eurswa` / `russwa` / `turswa` plus gate) everyone has,
  **except UKR** [^6]. Specific cluster (`eur` / `rus` / `tur`)
  selected by family of the nation.
- Gate is an upgrade `gc_upg_type_single_buildgate` applied to
  selected completed wall [^7]. Cost - 400 wood (UKR) or
  500 stone (rest of nations). Upgrade requires **direct section from
  three identical completed segments**: corners and ends of the wall,
  T-intersections, construction are rejected [^8].
- Construction of gates **instant**: `_player_ConstructGates`
  exposes `individual.upglevel := 1` on the new segment, after which
  `_unit_ControlBuildProgress` via a special branch
  `if (bwall) and (upglevel>0) then hp := maxhp` sets full HP, and
  state-machine handler `OnTagStates.essential_none` immediately
  switches `bbuilt := True, hp := maxhp, buildprogress := 1` [^9][^10].
  Peasants do not participate in the construction of the gate.
- Capture segment of the wall (or gate) by enemy infantry on
  `gc_gameplay_captureradius = 4` tile **does not transfer the owner**, but
  destroys the segment: in `_misc_CheckCapture` for all `bwall`
  `bDie := True` [^11] is forcibly set. If segment HP
  less than 1/3 of the maximum, the capture check is skipped altogether -
  such a segment is already only being finished off with weapons [^12].

---

<a id="1-типы-стен-и-их-доступность"></a>
## 1. Types of walls and their availability

Two classes according to `usage` and `material` [^1]:

| Class | `usage` | wall/gate sid | Material | Availability |
|---|---|---|---|---|
| Weak (Palisade) | `gc_obj_usage_weakwall` | `ukrwwa` / `ukrwga` | `gc_obj_material_woodwall` | **All 21 nations** |
| Durable (stone), eur-cluster | `gc_obj_usage_hardwall` | `eurswa` / `eursga` | `gc_obj_material_building` | Everything except UKR / RUS / TUR / ALG |
| Durable (stone), rus-cluster | `gc_obj_usage_hardwall` | `russwa` / `russga` | `gc_obj_material_building` | RUS |
| Durable (stone), tur-cluster | `gc_obj_usage_hardwall` | `turswa` / `tursga` | `gc_obj_material_building` | TUR/ALG |

UKR only has a palisade; This nation does not have a stone wall [^6].

Parameters from code [^1]:

**Palisade `ukrwwa` / `ukrwga`.** HP: 1500 for the general version and 2500 for
UKR (wall), 1000 for general and 1500 for UKR (gate). Price: 10 wood
(general) / 12 wood (UKR). Buildtime in frames: 18 (general) / 26 (UKR).
The Bgate flag is set only for `ukrwga`.

**Stone wall `*swa` / `*sga`.** HP: 50000 at the wall, 32000 at the gate.
Price: 50 stone (eur) / 60 stone (rus, tur). Buildtime in frames:
288 (eur) / 640 (rus) / 384 (tur). All three clusters put
`bwall = True`, `bgate = True` (only for `*sga`), `usage =
gc_obj_usage_hardwall`. A wall segment has `consume.stone` = 250
(eur) / 200 (rus) / 150 (tur) - constant consumption of stone, for now
the segment costs [^1].

Specific numbers by nation - in
[`reference/03_buildings/README.md`](../../../reference/03_buildings/README.md).

## 2. Footprint and clusters

The wall segment has a collision-mask of 2 × 2 cells (1 tile). Several
consecutive segments:
```
[wall][wall][wall]   ← 3 tiles линии
```
There is no gap between the segments; pathfinding does not allow enemies through
tight line.

`gWallSystem` - global object (`TWallSystem`) with a list
clusters (`TWallCluster`) [^4]. Each cluster contains `wallType`
(`hardwall` / `weakwall`), `cid` nation, `plIndex` owner, array
`Cells` (by `TWallCell` per segment), as well as construction mode flags
(`firstWall`, `buildWall`).

When a segment dies (HP = 0 or forced death-tag),
`_unit_OnDeath` calls `gWallSystem.RemoveHandle(pl, goHnd)` -
removes a cell from the cluster and updates neighbor connections [^13].

### 2.1. Wall variations and builder slots

Builder slots of a segment depend on its geometric orientation in
cluster (`wallvariation`). When collecting a list of builders in
`_player_OrderUnitsToBuild` logic selects an array of points from
`gCustomBuildPointsWall[variation]` for all buildings with
`bwall or bgate = True`, **except in the case of `variation = 0`** - then
the usual `gCustomObjPoints[cid, id]` is used, as for non-walls
[^5].

The same `builderPoints` are used for both construction and repair -
both branches go through `_unit_OrderBuild` [^3].

Engine cap - `gc_MaxWallBuilderPointsCount = 16`. Array Contents
filled in by the parser `data/game/var/wallcustom.cfg` [^14].

## 3. Construction of a wall by peasants

The player selects the sid of the wall in the UI and draws a line with the mouse; preview
drawn via `_misc_UpdateWall(gWallCluster)` (separate “phantom”
objects on players-misc, blinking blue) [^15]. On click
confirmation each segment is created using a standard procedure
`_player_ConstructBuildingList` [^2] - the same as used for
any building. The segment starts with `bbuilt = False, buildprogress = 0,
hp = 10`, after which `_player_OrderUnitsToBuild` sends peasants to
construction.

The peasants receive the order `gc_obj_order_type_build`, go to the point from
`gCustomBuildPointsWall[wallvariation]`, hit with a hammer, raise HP and
buildprogress according to the usual construction formula (see.
[`building_mechanics.md` §3](../economy/building_mechanics.md) o
mechanics in general). On every tick of state-machine `nothing` buildings
called `_unit_ControlBuildProgress(myHnd)` [^16] - it recalculates
`buildprogress = hp / maxhp`, when `hp >= maxhp` sets the tag
`gc_statetag_essential_none`, by which handler `OnTagStates`
translates the segment to `bbuilt := True` [^10].

For a regular wall `individual.upglevel = 0`, so fast-path
"hp := maxhp" in `_unit_ControlBuildProgress` does not work, and
The segment is being completed at the standard pace of peasants. Resources are written off
for each segment separately (`_unit_ApplyCostByID`). Cancel construction
specific segment until completion can be done using the standard button -
the unfinished segment is demolished with the return of resources according to the usual formula
refund.

## 4. Capture and segment demolition

The standard gripping mechanism goes through `_misc_CheckCapture`: when
enemy infantryman ends up in `gc_gameplay_captureradius = 4`
tile from object `bcapture = True` without its defenders, object
changes owner [^11]. For walls and gates this procedure works differently:

1. First, a separate function `_unit_SearchCapturersForWall` searches
   capturers nearby - with a less strict filter than for regular ones
   buildings (`bcancapture` no purpose required) [^11].
2. If the HP of the segment is less than 1/3 of `maxhp`, further logic
   skipped - the segment is already finished off with weapons, without the capture effect
   [^12].
3. Otherwise, when a capturer is found, it is forced to fire
   `bDie := True` (special branch for `bwall`) - segment
   receives `gc_statetag_essential_death` and is destroyed by [^11].

The behavior is the same for both a finished wall and an unfinished one.
(`bbuilt = False`): in both cases, an enemy infantryman in
within a radius of 4 tiles - the segment is instantly demolished. This is "demolition", not
"capture"; The segment does not become the owner.

The gate has `bwall = True` (plus an additional `bgate = True`), so
branch `bDie := True` works for them too.

<a id="5-ворота-как-моментальный-апгрейд"></a>
## 5. Gates as an instant upgrade

Gates are created exclusively through `gc_upg_type_single_buildgate` -
individual upgrade applied to one selected segment
walls [^7][^17]. Cost and location of the study according to `country.script`
[^18]:

| Nation/sid | Price | Where is being researched |
|---|---|---|
| `ukrwwa.1` | 400 wood | at the selected segment ukrwwa |
| `eurswa.1` | 500 stone | at the selected eurswa segment (eur-cluster) |
| `russwa.1` | 500 stone | at the selected segment russwa (RUS) |
| `turswa.1` | 500 stone | at the selected turswa segment (TUR / ALG) |

Before starting the upgrade, the engine checks the geometry through
`_misc_GetGateBaseSprite` [^8]: returns the correct gate sprite,
only if

1. the selected segment is **not at the end** of the cluster (there are neighbors on the left and
   right);
2. both neighbors have the same sprite (the wall goes straight - not a corner, not
   T-junction);
3. all three segments (`p1, p2, p3`) **completed** (`bbuilt = True`);
4. within a radius of 1.85 tiles from the center there are exactly three walls (no more).

If at least one condition is not met - `Result = -1`, and the upgrade is not
will start. Therefore, gates can only be placed in the middle of a straight line
wall section of at least three completed segments.

<a id="51-что-происходит-при-срабатывании-апгрейда"></a>
### 5.1. What happens when an upgrade is triggered?

`_player_ConstructGates(goHnd)` [^9]:

1. Sets `gbool_gui_gatefinished := True` (used later
   to `_unit_DoExplosion` to skip visual explosion
   hardwall segments after the first construction of the goal in the match [^19]).
2. Gets `wallcluster`, which contains `goHnd`, and the index
   central cell.
3. Clears sprite from neighboring cells (`p1` and `p3`) and puts it on
   central (`p2`) sprite gate.
4. Creates a new gate object at the same position via
   `_player_ConstructBuildingList` with **empty list of peasants**
   (`gIntegerList.Clear` before the call). The object at this stage has
   a typical set for construction: `bbuilt = False, hp = 10,
   buildprogress = 0`.
5. **Immediately after return** puts `TObj(pobj).individual.upglevel :=
   upglevel + 1` - this increment activates the next step.
6. Binds a new handle to cell: `TWallCell(p2).goHnd := trgHnd`.
7. If the player is an observer, switches the UI selection from the old one
   segment to a new gate object.

On the nearest tick state-machine handler `nothing` for buildings calls
`_unit_ControlBuildProgress(myHnd)` [^16]. At the newly created gate
now `bwall = True` and `upglevel = 1 > 0`, and a special
branch [^20]:

> `if (bwall) and (upglevel>0) then hp := maxhp;`

After assigning hp, a check is performed immediately
`if hp >= maxhp then SetTagStates(essential_none)`, by which handler
`OnTagStates` ([building.inc/ontagstates.inc:134][^10]) translates
object to final state: `bbuilt := True, hp := maxhp,
buildprogress := 1`, plus player-counters increment and
visual update.

From the player's point of view, the gate appears **fully constructed**
immediately after applying the upgrade. No pause for construction and no
They don't need peasants.

<a id="52-подмена-цели-при-создании-ворот"></a>
### 5.2. Changing the target when creating a gate

Application technique resulting from the sequence above:

- the enemy attacks a wall segment (`goHnd_old`); the attack is on
  specific handle (`gc_obj_order_type_attackobj` stores trg);
- the player applies the buildgate upgrade on this segment if the form
  walls allows;
- `_player_ConstructGates` creates a new gate handle (`goHnd_new`),
  moves the cell pointer to it and increments `upglevel`;
  the old segment loses its role as an active point in the cluster;
- attacking units lose their target - to resume attacking the enemy
  you need to issue a new command to a new object;
- damage accumulated in the old segment is not transferred: the gate is already
  cost with full HP (`maxhp = 32000` for hardwall, ~1000–1500 for
  palisade `ukrwga`). Defender gets direct replacement
  a shabby wall to a fresh one.

## 6. Wall towers

Some nations have separate sid's of wall towers (`stonewalltower` and
analogues), which fit into the line of the wall without a gap and shoot like
ordinary tower. For aiming mechanics and shot costs, see
[`towers.md`](towers.md).

## 7. Open empirical questions

1. How exactly does `costpercent` apply to wall segments when
   mass construction: for each segment or for the entire drawing.
2. The exact speed of construction of a segment by peasants, depending on
   `wallvariation` (variation = 0 follows the usual formula, the rest -
   by explicit `builderPoints`).
3. Behavior in a rare situation: the buildgate upgrade starts, but
   at the time of completion, the neighboring segments have already been destroyed - is it correct?
   the gate will remain in the cluster or become a “hanging” building.

---

## Sources

[^1]: `data/scripts/lib/unit.script:2258-2310` — `commonsid+'swa'` /
      `commonsid+'sga'` (stone walls and gates common to clusters
      eur / rus / tur), `'ukrwwa'` / `'ukrwga'` (palisade and
      wooden gates). `usage`, `bwall`,
      `bgate`, `material`, `maxhp`, prices, consume.
      ```pascal
      commonsid+'swa', commonsid+'sga' : begin
         SetObjBuildingProperties(objprop, objbase, 50000, 288, 0);
         SetObjBasePrice(objbase, 0, 0, 50, 0, 0, 0);
         objprop.consume[gc_resource_type_stone] := 250;
         objprop.bwall := True;
         objprop.usage := gc_obj_usage_hardwall;
         if (commonrus) then ... // 60 stone, consume 200, bt 640
         if (commontur) then ... // 60 stone, consume 150, bt 384
         if (objprop.sid=commonsid+'sga') then begin
            objprop.bgate := True;
            objbase.maxhp := 32000;
         end;
      end;
      'ukrwwa', 'ukrwga' : begin
         SetObjBuildingProperties(objprop, objbase, 1500, 18, 0);
         if (ukr) then SetObjBuildingProperties(objprop, objbase, 2500, 26, 0);
         SetObjBasePrice(objbase, 0, 10, 0, 0, 0, 0);
         if (ukr) then SetObjBasePrice(objbase, 0, 12, 0, 0, 0, 0);
         objprop.material := gc_obj_material_woodwall;
         objprop.bwall := True;
         objprop.usage := gc_obj_usage_weakwall;
         if (objprop.sid='ukrwga') then begin
            objprop.bgate := True;
            if (ukr) then objbase.maxhp := 1500
            else objbase.maxhp := 1000;
         end;
      end;
      ```
[^2]: `data/scripts/lib/player.script:1476-1581` —
      `_player_ConstructBuildingList`. Creates a building as standard
      by overwriting the initialized `_unit_InitObj`
      construction values:
      ```pascal
      trghnd := CreatePlayerGameObjectHandleByHandle(plHnd, gc_racename_buildings, sid, px, 0, pz);
      var pobj : Pointer = _unit_GetTObj(trghnd);
      if pobj <> nil then begin
         TObj(pobj).bbuilt := False;
         TObj(pobj).buildprogress := 0;
         TObj(pobj).hp := 10;
         _unit_ControlBuildProgress(trghnd);
      end;
      ...
      _player_OrderUnitsToBuild(list, trgHnd, bClearOrders, false, false);
      ```
[^3]: `data/scripts/lib/unit.script:9268-9378` - `_unit_OrderBuild`.
      Lines 9280-9286 select the builderPoints source for walls/gates:
      ```pascal
      var bwall : Boolean = gObjProp[cid][id].bwall;
      var variation : Integer = TObj(pTrgObj).wallvariation;
      var bCount : Integer;
      if (bwall) then
         bCount := gCustomBuildPointsWall[variation].builderCount
      else
         bCount := gCustomObjPoints[cid, id].builderCount;
      ```
Command `_unit_AddOrder(..., gc_obj_order_type_build, ...)`
      issued on 9371. The same function is used for
      `gc_obj_order_type_repair`.

[^4]: `data/scripts/lib/classes.script:2857-3232` - `TWallCluster` and
      `TWallSystem`: fields (`wallType`, `cid`, `plIndex`, `Cells`),
      methods `AddCell` / `DeleteCell` / `Clear` / `ConnectToPoint` /
      `KeepSegment` / `CreateSprites` / `SetWallBuildMode`.

[^5]: `data/scripts/lib/player.script:1137-1148` - array selection
      `builderPoints` for walls/gates when sending out peasants:
      ```pascal
      var bwall : Boolean = (gObjProp[cid][id].bwall) or (gObjProp[cid][id].bgate);
      var variation : Integer = TObj(pTrgObj).wallvariation;
      if (bwall) and (variation=0) then
         bwall := False;
      if (bwall) then
         bCount := gCustomBuildPointsWall[variation].builderCount
      else
         bCount := gCustomObjPoints[cid, id].builderCount;
      ```
`gCustomBuildPointsWall` declared in
      `classes.script:7664` as global length array
      `gc_MaxWallVariationCount`.

[^6]: `data/scripts/lib/country.script:2867-2886` - addition
      sid's walls to the nation. `ukrwwa` / `ukrwga` are added to all 21
      nations without conditions. The stone wall goes through cluster branches
      (`not ukr and not tur and not alg and not rus → eurswa`,
      `tur or alg → turswa`, `rus → russwa`):
      ```pascal
      _country_AddMember(country, 'ukrwwa', ind, True, ...);
      _country_AddMember(country, 'ukrwga', ind, True, ...);
      if (not ukr) and (not tur) and (not alg) and (not rus) then
      begin
         _country_AddMember(country, 'eurswa', ind, True, ...);
         _country_AddMember(country, 'eursga', ind, True, ...);
      end;
      if (tur) or (alg) then begin _country_AddMember(country, 'turswa', ...); ... end;
      if (rus) then        begin _country_AddMember(country, 'russwa', ...); ... end;
      ```
For UKR, none of the `swa` branches are activated - stone
      The nation does not get a wall.

[^7]: `data/scripts/lib/player.script:1974-1981` — upgrade handler
      `gc_upg_type_single_buildgate` to `_player_ApplyUpgrade`:
      ```pascal
      gc_upg_type_single_buildgate : begin
         var pobj : Pointer = _unit_GetTObj(goHnd);
         if (pobj<>nil) and (gObjProp[TObj(pobj).cid][TObj(pobj).id].bwall) then
         begin
            TObj(pobj).individual.benabled := True;
            TObj(pobj).individual.upglevel := TObj(pobj).individual.upglevel + 1;
            _player_ConstructGates(goHnd);
         end;
      end;
      ```
[^8]: `data/scripts/lib/misc.script:3998-4058` —
      `_misc_GetGateBaseSprite`. Returns sprite(14, 15, 16, 17),
      only if all the conditions are about the direct section and completion
      completed; otherwise `-1` (upgrade is blocked).

[^9]: `data/scripts/lib/player.script:1583-1645` —
      `_player_ConstructGates`. Line 1612 creates a new object
      gate via `_player_ConstructBuildingList`, line 1615
      increments `individual.upglevel`, line 1616
      rewrites `TWallCell(p2).goHnd` to a new handle.

[^10]: `data/scripts/units/building.inc/ontagstates.inc:134-137` —
       handler `OnTagStates` buildings, branch
       `gc_statetag_essential_none`. Here the object is final
       goes to built-state:
       ```pascal
       arg_obj.bbuilt := True;
       arg_obj.hp := gPlayer[arg_obj.pl].objBase[arg_obj.cid][arg_obj.id].maxhp;
       arg_obj.buildprogress := 1;
       _unit_AddObjToPlayerCounters(myHnd, True, False, False);
       ```
[^11]: `data/scripts/lib/miscext.script:961-1185` —
       `_misc_CheckCapture`. Line 975 - `bwall :=
       TObjProp(pobjprop).bwall`. Lines 1003-1006 switch
       search for capturers on `_unit_SearchCapturersForWall` (without
       requirements `bcancapture` from the capturer). Line 1106 -
       special branch for `bwall`:
       ```pascal
       var bDie : Boolean;
       var bAutoKill : Boolean;
       if (bAutoKill) or (TObjProp(pobjprop).bwall) then
       begin
          bDie := True;
       end;
       ```
Then the following is executed
       `_unit_SetTagStates(goHnd, gc_statetag_essential_death)`.

[^12]: `data/scripts/lib/miscext.script:1034` —
       `if (not ((bwall) and (TObj(pobj).hp<TObjBase(pobjbase).maxhp/3))) then`.
       When HP is less than 1/3 of max, the capture branch is completely skipped.

[^13]: `data/scripts/lib/unit.script:3954` - call
       `gWallSystem.RemoveHandle(pl, goHnd)` upon death of a segment in
       `_unit_OnDeath`.

[^14]: `data/scripts/lib/country.script:4096-4101` - filling
       `gCustomBuildPointsWall[variation].builderCount` and
       `builderPoints[j].x/y` parser
       `data/game/var/wallcustom.cfg`.
       `gc_MaxWallBuilderPointsCount = 16` - `dmscript.global`.

[^15]: `data/scripts/lib/miscext2.script:933-975` — `_misc_UpdateWall`:
       creates "phantom" objects on players-misc and lights up blue
       blink on hover, updates `gCanPlaceBuildingWalls`.

[^16]: `data/scripts/units/building.inc/nothing.inc:296-307` —
       state-machine handler `nothing` (idle) for buildings. Bye
       `not arg_obj.bbuilt`, is called on each trigger
       `_unit_ControlBuildProgress(myHnd)`:
       ```pascal
       if (not arg_obj.bbuilt) then
       begin
          if gametime>arg_obj.lasttimecheckcapture then
          begin
             arg_obj.lasttimecheckcapture := gametimewithrnd+gc_unit_TimeCheckCapture;
             _misc_CheckCapture(myHnd);
          end;
          _unit_ControlBuildProgress(myHnd);
       end;
       ```
[^17]: Field `bindividual := True` for buildgate upgrade ([country.script:3944][^18])
       marks it as individual - applies to one
       to the selected object, and not globally to the nation.

[^18]: `data/scripts/lib/country.script:3942-3973` - registration
       buildgate upgrades:
       ```pascal
       upgplace := 'ukrwwa';
       _country_AddUpgradeWithAccessControl(country, upgplace+'.1', 2, ..., gc_upg_type_single_buildgate, 5, ..., 0, 400, 0, ...);  // 400 wood
       country.upgrade[ind-1].bindividual := True;
       ...
       if (rus) then begin upgplace := 'russwa'; ... 0, 0, 500, ... end; // 500 stone
       if (tur) or (alg) then begin upgplace := 'turswa'; ... 0, 0, 500, ... end;
       if (not ukr) then begin upgplace := 'eurswa'; ... 0, 0, 500, ... end;
       ```
[^19]: `data/scripts/lib/unit.script:11429` - condition in
       `_unit_DoExplosion`:
       `if (not gbool_gui_gatefinished) or (TObjProp(pobjprop).usage<>gc_obj_usage_hardwall) then`.
       After the first `_player_ConstructGates` visual explosion
       debris for hardwall segments is disabled for the remaining match.

[^20]: `data/scripts/lib/unit.script:6572-6608` —
       `_unit_ControlBuildProgress`. Key branch for the gate in
       at the beginning of the procedure:
       ```pascal
       if (gObjProp[TObj(pobj).cid][TObj(pobj).id].bwall) and (TObj(pobj).individual.upglevel>0) then
          TObj(pobj).hp := gPlayer[TObj(pobj).pl].objbase[TObj(pobj).cid][TObj(pobj).id].maxhp;
       ```
After assignment it is checked
       `if hp >= maxhp then _unit_SetTagStates(hnd, gc_statetag_essential_none ...)`
       - this is the trigger OnTagStates handler [^10], in which
       `bbuilt := True`.
