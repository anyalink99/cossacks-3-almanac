<a id="recon-стены-и-ворота"></a>
<a id="стены-и-ворота"></a>
# Walls and Gates

[← How the game works](../../README.md)

How the game joins segments into wall lines (`gWallSystem` /
`TWallCluster`), how Peasants construct them, how Gates differ from
ordinary wall segments, and what happens during a capture attempt.

<a id="коротко"></a>
## TL;DR

- A wall segment is a building with `usage = gc_obj_usage_hardwall` or
  `gc_obj_usage_weakwall` and the flag `bwall = True` [^1]. The player "draws"
  line with the mouse, after clicking unfinished segments appear
  (`bbuilt = False, hp = 10`), and the peasants build them **like ordinary ones
  buildings** via standard path `_player_ConstructBuildingList` →
  `_player_OrderUnitsToBuild` [^2][^3].
- One segment occupies 1 × 1 tile. A longer wall is a sequence of
  segments in `TWallCluster` [^4].
- Builder slots for each segment are taken from
  `gCustomBuildPointsWall[wallvariation]` (source -
  `data/game/var/wallcustom.cfg`); variation = 0 is treated as
  ordinary building [^5].
- All 21 nations have a **Palisade** (`ukrwwa`) and Palisade Gate
  (`ukrwga`). A **Stone Wall** (`eurswa`, `russwa`, or `turswa`, with
  matching Gates) is available to every nation **except Ukraine** [^6].
  The European, Russian, or Ottoman variant (`eur`, `rus`, `tur`) is
  selected by nation family.
- A Gate is an individual upgrade (`gc_upg_type_single_buildgate`)
  applied to a selected completed segment [^7]. It costs 400 wood for
  a Palisade or 500 stone for a Stone Wall. It requires **a straight run of
  three identical completed segments**: corners and ends of the wall,
  T-intersections, construction are rejected [^8].
- Gate construction is **instant**: `_player_ConstructGates`
  exposes `individual.upglevel := 1` on the new segment, after which
  `_unit_ControlBuildProgress` via a special branch
  `if (bwall) and (upglevel>0) then hp := maxhp` sets full HP, and
  the `OnTagStates.essential_none` state handler immediately
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
## 1. Wall Types and Availability

The engine distinguishes two broad classes through `usage` and
`material` [^1]:

| Class | Internal wall / gate IDs | Engine properties | Availability |
|---|---|---|---|
| **Palisade and Palisade Gate** | `ukrwwa` / `ukrwga` | `gc_obj_usage_weakwall`, `gc_obj_material_woodwall` | **All 21 nations** |
| **European Stone Wall and Gate** | `eurswa` / `eursga` | `gc_obj_usage_hardwall`, `gc_obj_material_building` | All except Ukraine, Russia, Turkey, and Algeria |
| **Russian Stone Wall and Gate** | `russwa` / `russga` | `gc_obj_usage_hardwall`, `gc_obj_material_building` | Russia |
| **Ottoman Stone Wall and Gate** | `turswa` / `tursga` | `gc_obj_usage_hardwall`, `gc_obj_material_building` | Turkey and Algeria |

Ukraine has only the Palisade; it has no Stone Wall [^6].

Parameters from code [^1]:

**Palisade (`ukrwwa`) and Palisade Gate (`ukrwga`).** Wall hit points
are 1,500 normally and 2,500 for Ukraine; Gate hit points are 1,000 and
1,500 respectively. The price is 10 wood, or 12 for Ukraine. Build time
is 18 frames, or 26 for Ukraine. Only `ukrwga` carries the `bgate` flag.

**Stone Wall (`*swa`) and Gate (`*sga`).** The Wall has 50,000 hit
points and the Gate 32,000. Price is 50 stone for the European variant
and 60 for the Russian and Ottoman variants. Build time is 288, 640,
and 384 frames respectively. All three variants set
`bwall = True`, `bgate = True` (only for `*sga`), `usage =
gc_obj_usage_hardwall`. A wall segment has `consume.stone` = 250
(eur) / 200 (rus) / 150 (tur) - constant consumption of stone, for now
the segment costs [^1].

Specific numbers by nation - in
[building guide](../../../reference/03_buildings/README.md).

<a id="2-footprint-и-кластеры"></a>
<a id="2-занимаемая-площадь-и-линии-стен"></a>
## 2. Footprint and Wall Lines

The wall segment has a collision-mask of 2 × 2 cells (1 tile). Several
consecutive segments:
```
[wall][wall][wall]   ← a 3-tile line
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

<a id="21-wall-variations-и-builder-slots"></a>
<a id="21-варианты-сегментов-и-места-для-строителей"></a>
### 2.1. Segment variants and builder positions

Builder positions depend on the segment's geometric orientation within
the wall line (`wallvariation`). When collecting a list of builders,
`_player_OrderUnitsToBuild` logic selects an array of points from
`gCustomBuildPointsWall[variation]` for all buildings with
`bwall or bgate = True`, **except in the case of `variation = 0`** - then
the usual `gCustomObjPoints[cid, id]` is used, as for non-walls
[^5].

The same `builderPoints` are used for both construction and repair -
both branches go through `_unit_OrderBuild` [^3].

The engine allows at most 16 positions
(`gc_MaxWallBuilderPointsCount`). They are loaded from
`data/game/var/wallcustom.cfg` [^14].

<a id="3-постройка-стены-крестьянами"></a>
## 3. Wall Construction by Peasants

The player selects a wall type in the interface and drags a line with
the mouse. `_misc_UpdateWall(gWallCluster)` draws the preview with
blue-blinking temporary objects [^15]. On confirmation, every segment
is created through the standard
`_player_ConstructBuildingList` [^2] - the same as used for
any building. The segment starts with `bbuilt = False, buildprogress = 0,
hp = 10`, after which `_player_OrderUnitsToBuild` sends peasants to
construction.

The peasants receive the order `gc_obj_order_type_build`, go to the point from
`gCustomBuildPointsWall[wallvariation]`, hit with a hammer, raise HP and
buildprogress according to the usual construction formula (see.
[Building Construction, Repair, and Destruction §3](../economy/building_mechanics.md)).
On each tick, the building's `nothing` state calls
`_unit_ControlBuildProgress(myHnd)` [^16], which recalculates
`buildprogress = hp / maxhp`, when `hp >= maxhp` sets the tag
`gc_statetag_essential_none`; the `OnTagStates` handler then changes the
segment to `bbuilt := True` [^10].

For a regular wall `individual.upglevel = 0`, so fast-path
"hp := maxhp" in `_unit_ControlBuildProgress` does not work, and
the segment is completed at the normal Peasant construction rate. Each
segment is charged separately through `_unit_ApplyCostByID`. Cancelling
an unfinished segment uses the standard demolition and refund rules.

<a id="4-захват-и-снос-сегмента"></a>
## 4. Capturing and Demolishing a Segment

The standard capture mechanism runs through `_misc_CheckCapture`: when
an enemy infantryman comes within four tiles
(`gc_gameplay_captureradius = 4`) of an undefended object with
`bcapture = True`, that object
changes owner [^11]. For walls and gates this procedure works differently:

1. `_unit_SearchCapturersForWall` searches for nearby capturers using a
   less restrictive filter than ordinary buildings (the target does not
   need `bcancapture`) [^11].
2. If the segment has less than one-third of `maxhp`, the remaining
   capture logic is skipped; weapons must finish it
   [^12].
3. Otherwise, finding a capturer forces `bDie := True` in the special
   `bwall` branch. The segment receives
   `gc_statetag_essential_death` and is destroyed [^11].

The behavior is the same for both a finished wall and an unfinished one.
(`bbuilt = False`): in both cases, an enemy infantryman in
within four tiles is enough to demolish the segment instantly. Ownership
is never transferred.

The gate has `bwall = True` (plus an additional `bgate = True`), so
branch `bDie := True` works for them too.

<a id="5-ворота-как-моментальный-апгрейд"></a>
<a id="5-ворота-как-мгновенное-улучшение"></a>
## 5. Gates as an Instant Upgrade

Gates are created exclusively through `gc_upg_type_single_buildgate` -
an individual upgrade applied to one selected wall segment [^7][^17].
Its cost and target are defined in `country.script`
[^18]:

| Wall type | Price | Applied to |
|---|---|---|
| **Palisade** (`ukrwwa.1`) | 400 wood | selected Palisade segment (`ukrwwa`) |
| **European Stone Wall** (`eurswa.1`) | 500 stone | selected European segment (`eurswa`) |
| **Russian Stone Wall** (`russwa.1`) | 500 stone | selected Russian segment (`russwa`) |
| **Ottoman Stone Wall** (`turswa.1`) | 500 stone | selected Ottoman segment (`turswa`) |

Before starting the upgrade, `_misc_GetGateBaseSprite` checks the wall's
geometry [^8] and returns a valid Gate sprite only when:

1. the selected segment is **not at the end** of the cluster (there are neighbors on the left and
   right);
2. both neighbors have the same sprite (the wall goes straight - not a corner, not
   T-junction);
3. all three segments (`p1, p2, p3`) **completed** (`bbuilt = True`);
4. within a radius of 1.85 tiles from the center there are exactly three walls (no more).

If any condition fails, the function returns `Result = -1` and the
upgrade does not start. A Gate can therefore be placed only in the
middle of a straight run of at least three completed segments.

<a id="51-что-происходит-при-срабатывании-апгрейда"></a>
<a id="51-что-происходит-при-создании-ворот"></a>
### 5.1. What happens when a Gate is created

`_player_ConstructGates(goHnd)` [^9]:

1. Sets `gbool_gui_gatefinished := True` (used later
   by `_unit_DoExplosion` to suppress the visual explosion of Stone Wall
   segments after the first Gate is built in a match [^19]).
2. Finds the wall line (`wallcluster`) containing `goHnd` and the index
   of its central cell.
3. Clears the neighboring cell sprites (`p1` and `p3`) and assigns the
   Gate sprite to the central cell (`p2`).
4. Creates a new gate object at the same position via
   `_player_ConstructBuildingList` with **empty list of peasants**
   (`gIntegerList.Clear` before the call). The object at this stage has
   a typical set for construction: `bbuilt = False, hp = 10,
   buildprogress = 0`.
5. **Immediately after return** puts `TObj(pobj).individual.upglevel :=
   upglevel + 1` - this increment activates the next step.
6. Binds the new handle to the cell:
   `TWallCell(p2).goHnd := trgHnd`.
7. If the player is an observer, switches the UI selection from the old one
   segment to a new gate object.

On the next tick, the building's `nothing` state calls
`_unit_ControlBuildProgress(myHnd)` [^16]. At the newly created gate
now `bwall = True` and `upglevel = 1 > 0`, and a special
branch [^20]:

> `if (bwall) and (upglevel>0) then hp := maxhp;`

After assigning hit points, the code immediately checks
`if hp >= maxhp then SetTagStates(essential_none)`. The `OnTagStates`
handler ([building.inc/ontagstates.inc:134][^10]) then moves the object
to its final state—`bbuilt := True, hp := maxhp, buildprogress := 1`—
and updates player counters and visuals.

From the player's point of view, the gate appears **fully constructed**
immediately after the upgrade. There is no construction delay, and no
Peasants are required.

<a id="52-подмена-цели-при-создании-ворот"></a>
<a id="52-почему-атакующие-могут-потерять-цель"></a>
### 5.2. Why attackers can lose their target

The replacement sequence has a practical combat consequence:

- the enemy attacks a wall segment (`goHnd_old`); the attack is on
  a specific handle (`gc_obj_order_type_attackobj` stores `trg`);
- the player applies the Gate upgrade (`buildgate`) if the wall geometry
  allows it;
- `_player_ConstructGates` creates a new gate handle (`goHnd_new`),
  moves the cell pointer to it and increments `upglevel`;
  the old segment loses its role as an active point in the cluster;
- attacking units lose their target - to resume attacking the enemy
  you need to issue a new command to a new object;
- damage accumulated in the old segment is not transferred: the gate is already
  appears with full hit points (`maxhp = 32000` for a Stone Wall Gate,
  roughly 1,000–1,500 for the Palisade Gate `ukrwga`). The defender has
  effectively replaced a damaged wall segment with a fresh Gate.

<a id="6-стенные-башни"></a>
## 6. Wall Towers

Some nations have dedicated Wall Towers (internal ID
`stonewalltower` and related variants). They fit into a wall line without
a gap and fire like an ordinary Tower. For targeting and shot costs, see
[tower and garrison mechanics](towers.md).

<a id="7-открытые-эмпирические-вопросы"></a>
<a id="7-что-ещё-требует-проверки"></a>
## 7. Questions Requiring Further Testing

1. How exactly does `costpercent` apply to wall segments when
   mass construction: for each segment or for the entire drawing.
2. The exact Peasant construction speed for each `wallvariation`.
   Variant 0 follows the standard formula; the others use explicit
   `builderPoints`.
3. What happens if a Gate upgrade (`buildgate`) begins but neighboring
   segments are destroyed before completion: does the Gate remain in the
   wall line or become a detached building?

---

<a id="источники"></a>
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
