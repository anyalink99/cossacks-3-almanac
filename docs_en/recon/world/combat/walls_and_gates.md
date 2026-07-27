<a id="recon-стены-и-ворота"></a>
<a id="стены-и-ворота"></a>
# Walls and Gates

[← How the game works](../../README.md)

How the game joins segments into continuous Walls, how Peasants construct
them, how Gates differ from ordinary segments, and what happens when enemy
infantry attempts to capture one. Internal systems such as `gWallSystem`
and `TWallCluster` are cited only where they explain the mechanic.

<a id="коротко"></a>
## TL;DR

- A Wall segment is internally a building with
  `usage = gc_obj_usage_hardwall` or `gc_obj_usage_weakwall` and
  `bwall = True` [^1]. The player draws a line with the mouse; confirming
  it places unfinished segments (`bbuilt = False, hp = 10`). Peasants
  then construct them **like ordinary buildings** through
  `_player_ConstructBuildingList` → `_player_OrderUnitsToBuild` [^2][^3].
- One segment occupies 1 × 1 tile. A longer wall is a sequence of
  segments in `TWallCluster` [^4].
- Builder positions for each segment come from
  `gCustomBuildPointsWall[wallvariation]` (source:
  `data/game/var/wallcustom.cfg`); variation = 0 is treated as
  ordinary building [^5].
- All 21 nations have a **Palisade** (`ukrwwa`) and Wooden Gate
  (`ukrwga`). A **Stone Wall** (`eurswa`, `russwa`, or `turswa`, with
  matching Gates) is available to every nation **except Ukraine** [^6].
  The European, Russia, or Turkey variant (`eur`, `rus`, `tur`) is
  selected by nation family.
- A Gate is an individual upgrade (`gc_upg_type_single_buildgate`)
  applied to a selected completed segment [^7]. It costs 400 Wood for
  a Palisade or 500 stone for a Stone Wall. It requires **a straight run of
  three identical completed segments**; Wall ends, corners,
  T-intersections, and unfinished sections are rejected [^8].
- Gate construction is **instant**: `_player_ConstructGates`
  exposes `individual.upglevel := 1` on the new segment, after which
  `_unit_ControlBuildProgress` via a special branch
  `if (bwall) and (upglevel>0) then hp := maxhp` sets full HP, and
  the `OnTagStates.essential_none` state handler immediately
  switches `bbuilt := True, hp := maxhp, buildprogress := 1` [^9][^10].
  Peasants do not participate in Gate construction.
- Enemy infantry within the four-tile capture radius
  (`gc_gameplay_captureradius = 4`) **does not take ownership** of a
  Wall or Gate. Instead, `_misc_CheckCapture` forces `bDie := True` for
  every `bwall`, destroying the segment [^11]. Below one-third durability,
  this capture check is skipped and the segment must be finished with
  weapons [^12].

---

<a id="1-типы-стен-и-их-доступность"></a>
## 1. Wall Types and Availability

The game has two broad classes, identified internally by `usage` and
`material` [^1]:

| Class | Internal wall / gate IDs | Engine properties | Availability |
|---|---|---|---|
| **Palisade and Wooden Gate** | `ukrwwa` / `ukrwga` | `gc_obj_usage_weakwall`, `gc_obj_material_woodwall` | **All 21 nations** |
| **European Stone Wall and Gate** | `eurswa` / `eursga` | `gc_obj_usage_hardwall`, `gc_obj_material_building` | All except Ukraine, Russia, Turkey, and Algeria |
| **Russia Stone Wall and Gate** | `russwa` / `russga` | `gc_obj_usage_hardwall`, `gc_obj_material_building` | Russia |
| **Turkey Stone Wall and Gate** | `turswa` / `tursga` | `gc_obj_usage_hardwall`, `gc_obj_material_building` | Turkey and Algeria |

Ukraine has only the Palisade; it has no Stone Wall [^6].

Parameters from code [^1]:

**Palisade (`ukrwwa`) and Wooden Gate (`ukrwga`).** Palisade durability
is 1,500 normally and 2,500 for Ukraine; Gate durability is 1,000 and
1,500 respectively. The price is 10 Wood, or 12 for Ukraine.
`buildtime` is 18 frames, or 26 for Ukraine. Only the Gate carries the
`bgate` flag.

**Stone Wall (`*swa`) and Gate (`*sga`).** The Wall has 50,000
durability and the Gate 32,000. The European version costs 50 Stone;
the Russia and Turkey versions cost 60. Their `buildtime` values are
288, 640, and 384 frames respectively. All three versions set
`bwall = True`, `bgate = True` (only for `*sga`), `usage =
gc_obj_usage_hardwall`. A standing segment continuously consumes Stone:
250 for the European version, 200 for Russia, and 150 for Turkey [^1].

Nation-by-nation values are listed in the
[building guide](../../../reference/03_buildings/README.md).

<a id="2-footprint-и-кластеры"></a>
<a id="2-занимаемая-площадь-и-линии-стен"></a>
## 2. Footprint and Wall Lines

One Wall segment occupies a 2 × 2-cell collision mask, equivalent to
one tile. Several consecutive segments form a line:

```
[wall][wall][wall]   ← a 3-tile line
```

There are no gaps between segments, so pathfinding cannot route enemies
through an unbroken line.

The global `gWallSystem` object (`TWallSystem`) maintains a list of Wall
lines (`TWallCluster`) [^4]. Each line records its `wallType`
(`hardwall` or `weakwall`), nation (`cid`), owner (`plIndex`), one
`TWallCell` per segment in `Cells`, and construction-state flags such as
`firstWall` and `buildWall`.

When a segment is destroyed—through zero durability or a forced death
state—`_unit_OnDeath` calls `gWallSystem.RemoveHandle(pl, goHnd)`.
This removes its cell from the line and updates the neighbouring
connections [^13].

<a id="21-wall-variations-и-builder-slots"></a>
<a id="21-варианты-сегментов-и-места-для-строителей"></a>
### 2.1. Segment variants and builder positions

Builder positions depend on a segment's orientation in the Wall line
(`wallvariation`). For objects with `bwall` or `bgate`,
`_player_OrderUnitsToBuild` normally selects
`gCustomBuildPointsWall[variation]`. **Variation 0 is the exception:**
it uses the ordinary `gCustomObjPoints[cid, id]`, like a non-wall
building [^5].

The same `builderPoints` are used for both construction and repair;
both branches go through `_unit_OrderBuild` [^3].

The engine allows at most 16 positions
(`gc_MaxWallBuilderPointsCount`). Their coordinates are loaded from
`data/game/var/wallcustom.cfg` [^14].

<a id="3-постройка-стены-крестьянами"></a>
## 3. Wall Construction by Peasants

The player selects a Wall type and drags a line with the mouse.
`_misc_UpdateWall(gWallCluster)` renders the preview as temporary blue,
blinking objects [^15]. Once confirmed, the ordinary
`_player_ConstructBuildingList` procedure [^2] creates every segment.
Each starts at `bbuilt = False`, `buildprogress = 0`, and `hp = 10`;
`_player_OrderUnitsToBuild` then assigns Peasants.

The Peasants receive the internal `gc_obj_order_type_build` order, walk
to positions from `gCustomBuildPointsWall[wallvariation]`, and use their
hammers to increase durability and `buildprogress` according to the
ordinary construction formula. See
[Building Construction, Repair, and Destruction §3](../economy/building_mechanics.md).
On each tick, the building's `nothing` state calls
`_unit_ControlBuildProgress(myHnd)` [^16]. It recalculates
`buildprogress = hp / maxhp`; at `hp >= maxhp`, it sets
`gc_statetag_essential_none`, and `OnTagStates` changes the segment to
`bbuilt := True` [^10].

An ordinary Wall has `individual.upglevel = 0`, so the `hp := maxhp`
shortcut in `_unit_ControlBuildProgress` does not apply. Its segments
are completed at the normal Peasant construction rate. Each segment is
charged separately through `_unit_ApplyCostByID`; cancelling an
unfinished segment uses the ordinary demolition and refund rules.

<a id="4-захват-и-снос-сегмента"></a>
## 4. Capturing and Demolishing a Segment

Ordinary capture runs through `_misc_CheckCapture`: an undefended object
with `bcapture = True` changes owner when enemy infantry comes within
four tiles (`gc_gameplay_captureradius = 4`) [^11]. Walls and Gates use
a different path:

1. `_unit_SearchCapturersForWall` looks for nearby infantry with a less
   restrictive filter than the ordinary building check; the target does
   not need `bcancapture` [^11].
2. Below one-third of `maxhp`, the remaining capture logic is skipped
   and weapons must finish the segment [^12].
3. Otherwise, finding a valid capturer forces `bDie := True` in the
   special `bwall` branch. The segment enters
   `gc_statetag_essential_death` and is destroyed [^11].

This applies to both a completed Wall and an unfinished one
(`bbuilt = False`): enemy infantry within four tiles demolishes the
segment instantly. Ownership is never transferred.

A Gate has `bwall = True` as well as `bgate = True`, so the same
`bDie := True` branch applies.

<a id="5-ворота-как-моментальный-апгрейд"></a>
<a id="5-ворота-как-мгновенное-улучшение"></a>
## 5. Gates as an Instant Upgrade

Gates are created through `gc_upg_type_single_buildgate`, an individual
upgrade applied to one selected Wall segment [^7][^17]. Its price and
target are defined in `country.script` [^18]:

| Wall type | Price | Applied to |
|---|---|---|
| **Palisade** (`ukrwwa.1`) | 400 Wood | selected Palisade segment (`ukrwwa`) |
| **European Stone Wall** (`eurswa.1`) | 500 Stone | selected European segment (`eurswa`) |
| **Russia Stone Wall** (`russwa.1`) | 500 Stone | selected Russia segment (`russwa`) |
| **Turkey Stone Wall** (`turswa.1`) | 500 Stone | selected Turkey segment (`turswa`) |

Before the upgrade starts, `_misc_GetGateBaseSprite` checks the Wall's
geometry [^8]. It accepts the placement only when:

1. the selected segment is **not at the end** of the line, with
   neighbours on both sides;
2. both neighbours use the same sprite, so the Wall is straight rather
   than a corner or T-intersection;
3. all three segments (`p1`, `p2`, `p3`) are **complete**
   (`bbuilt = True`);
4. exactly three Wall segments, no more, lie within 1.85 tiles of the
   centre.

If any condition fails, the function returns `Result = -1` and blocks
the upgrade. A Gate can therefore be placed only in the middle of a
straight run of at least three completed segments.

<a id="51-что-происходит-при-срабатывании-апгрейда"></a>
<a id="51-что-происходит-при-создании-ворот"></a>
### 5.1. What happens when a Gate is created

`_player_ConstructGates(goHnd)` [^9]:

1. Set `gbool_gui_gatefinished := True`. `_unit_DoExplosion` later uses
   this flag to suppress the visual explosion of Stone Wall segments
   after the first Gate is built in a match [^19].
2. Find the Wall line (`wallcluster`) containing `goHnd` and the index
   of its central cell.
3. Clear the neighbouring cell sprites (`p1` and `p3`) and assign the
   Gate sprite to the central cell (`p2`).
4. Create a new Gate at the same position through
   `_player_ConstructBuildingList`, with an **empty Peasant list**
   (`gIntegerList.Clear` before the call). It initially has the normal
   construction values: `bbuilt = False`, `hp = 10`,
   `buildprogress = 0`.
5. **Immediately after the call returns**, increment
   `TObj(pobj).individual.upglevel := upglevel + 1`, activating the
   shortcut described below.
6. Bind the new object handle to the cell:
   `TWallCell(p2).goHnd := trgHnd`.
7. For an observing player, move the interface selection from the old
   segment to the new Gate.

On the next tick, the building's `nothing` state calls
`_unit_ControlBuildProgress(myHnd)` [^16]. The new Gate has
`bwall = True` and `upglevel = 1 > 0`, which activates a special branch
[^20]:

> `if (bwall) and (upglevel>0) then hp := maxhp;`

After assigning full durability, the code immediately checks
`if hp >= maxhp then SetTagStates(essential_none)`. The `OnTagStates`
handler ([`building.inc/ontagstates.inc:134`][^10]) then moves the
object to its final state—`bbuilt := True`, `hp := maxhp`,
`buildprogress := 1`—and updates the player's counters and visuals.

From the player's point of view, the gate appears **fully constructed**
immediately after the upgrade. There is no construction delay, and no
Peasants are required.

<a id="52-подмена-цели-при-создании-ворот"></a>
<a id="52-почему-атакующие-могут-потерять-цель"></a>
### 5.2. Why attackers can lose their target

Replacing the object has a practical combat consequence:

- an enemy attacks a Wall segment (`goHnd_old`), targeting its specific
  object handle (`gc_obj_order_type_attackobj` stores `trg`);
- the defender applies the Gate upgrade (`buildgate`) if the Wall geometry
  allows it;
- `_player_ConstructGates` creates a new Gate handle (`goHnd_new`),
  redirects the cell to it, and increments `upglevel`; the old segment
  is no longer the active object in that cell;
- the attackers lose their target and need a new attack order against
  the Gate;
- damage accumulated on the old segment does not carry over. The Gate
  appears at full durability: 32,000 for a Stone Gate and 1,000–1,500
  for a Wooden Gate (`ukrwga`). A damaged Wall segment has effectively
  been replaced with a fresh Gate.

<a id="6-стенные-башни"></a>
## 6. Wall Towers

Some nations have dedicated Wall Towers (`stonewalltower` and related
internal identifiers). They fit into a Wall line without a gap and fire
like an ordinary Tower. Their targeting and ammunition costs are covered
in [Tower mechanics](towers.md).

<a id="7-открытые-эмпирические-вопросы"></a>
<a id="7-что-ещё-требует-проверки"></a>
## 7. Questions Requiring Further Testing

1. Does `costpercent` apply separately to every Wall segment in a drawn
   line, or once to the entire placement?
2. What is the exact Peasant construction rate for every
   `wallvariation`? Variation 0 follows the ordinary formula; the others
   use explicit `builderPoints`.
3. If a Gate upgrade (`buildgate`) starts and neighbouring segments are
   destroyed before it resolves, does the Gate remain in the Wall line
   or become a detached building?

---

<a id="источники"></a>
## Sources

[^1]: `data/scripts/lib/unit.script:2258-2310` —
      `commonsid+'swa'` / `commonsid+'sga'` for Stone Walls and Gates
      in the `eur`, `rus`, and `tur` families; `'ukrwwa'` /
      `'ukrwga'` for the Palisade and Wooden Gate. This code assigns
      `usage`, `bwall`, `bgate`, `material`, `maxhp`, prices, and
      continuing resource consumption.
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
      `_player_ConstructBuildingList`. It creates a building through
      the standard path and replaces the `_unit_InitObj` values with
      the initial construction state:
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
[^3]: `data/scripts/lib/unit.script:9268-9378` —
      `_unit_OrderBuild`. Lines 9280–9286 select the source of builder
      positions for Walls and Gates:
      ```pascal
      var bwall : Boolean = gObjProp[cid][id].bwall;
      var variation : Integer = TObj(pTrgObj).wallvariation;
      var bCount : Integer;
      if (bwall) then
         bCount := gCustomBuildPointsWall[variation].builderCount
      else
         bCount := gCustomObjPoints[cid, id].builderCount;
      ```
      Line 9371 issues
      `_unit_AddOrder(..., gc_obj_order_type_build, ...)`. The same
      function handles `gc_obj_order_type_repair`.

[^4]: `data/scripts/lib/classes.script:2857-3232` — `TWallCluster` and
      `TWallSystem`: fields (`wallType`, `cid`, `plIndex`, `Cells`),
      methods `AddCell` / `DeleteCell` / `Clear` / `ConnectToPoint` /
      `KeepSegment` / `CreateSprites` / `SetWallBuildMode`.

[^5]: `data/scripts/lib/player.script:1137-1148` — selecting the
      `builderPoints` array for Walls and Gates when assigning Peasants:
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
      `gCustomBuildPointsWall` is declared in `classes.script:7664` as
      a global array of length `gc_MaxWallVariationCount`.

[^6]: `data/scripts/lib/country.script:2867-2886` — adding Wall and
      Gate members to nations. `ukrwwa` and `ukrwga` are added to all
      21 nations unconditionally. Stone Walls use nation-family branches
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
      None of the `swa` branches applies to Ukraine, so it receives no
      Stone Wall.

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
      `_misc_GetGateBaseSprite`. It returns sprite 14, 15, 16, or 17
      only for a valid straight, completed section; otherwise it returns
      `-1` and blocks the upgrade.

[^9]: `data/scripts/lib/player.script:1583-1645` —
      `_player_ConstructGates`. Line 1612 creates the new Gate through
      `_player_ConstructBuildingList`; line 1615 increments
      `individual.upglevel`; line 1616 assigns the new handle to
      `TWallCell(p2).goHnd`.

[^10]: `data/scripts/units/building.inc/ontagstates.inc:134-137` —
       the building `OnTagStates` handler, in the
       `gc_statetag_essential_none` branch. This finalizes construction:
       ```pascal
       arg_obj.bbuilt := True;
       arg_obj.hp := gPlayer[arg_obj.pl].objBase[arg_obj.cid][arg_obj.id].maxhp;
       arg_obj.buildprogress := 1;
       _unit_AddObjToPlayerCounters(myHnd, True, False, False);
       ```
[^11]: `data/scripts/lib/miscext.script:961-1185` —
       `_misc_CheckCapture`. Line 975 reads `bwall :=
       TObjProp(pobjprop).bwall`. Lines 1003–1006 use
       `_unit_SearchCapturersForWall`, without the ordinary
       `bcancapture` requirement. Line 1106 enters the special `bwall`
       branch:
       ```pascal
       var bDie : Boolean;
       var bAutoKill : Boolean;
       if (bAutoKill) or (TObjProp(pobjprop).bwall) then
       begin
          bDie := True;
       end;
       ```
       The code then calls
       `_unit_SetTagStates(goHnd, gc_statetag_essential_death)`.

[^12]: `data/scripts/lib/miscext.script:1034` —
       `if (not ((bwall) and (TObj(pobj).hp<TObjBase(pobjbase).maxhp/3))) then`.
       Below one-third of maximum durability, the capture branch is
       skipped completely.

[^13]: `data/scripts/lib/unit.script:3954` — `_unit_OnDeath` calls
       `gWallSystem.RemoveHandle(pl, goHnd)` when a segment is destroyed.

[^14]: `data/scripts/lib/country.script:4096-4101` — parsing
       `data/game/var/wallcustom.cfg` into
       `gCustomBuildPointsWall[variation].builderCount` and
       `builderPoints[j].x/y`.
       `gc_MaxWallBuilderPointsCount = 16` — `dmscript.global`.

[^15]: `data/scripts/lib/miscext2.script:933-975` — `_misc_UpdateWall`:
       creates temporary objects for the service player, gives them a
       blue blinking highlight, and updates `gCanPlaceBuildingWalls`.

[^16]: `data/scripts/units/building.inc/nothing.inc:296-307` —
       the building `nothing` (idle) state handler. While
       `not arg_obj.bbuilt`, each trigger calls
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
[^17]: `bindividual := True` for the Gate upgrade
       ([country.script:3944][^18]) makes it apply to one selected object,
       not globally to the nation.

[^18]: `data/scripts/lib/country.script:3942-3973` — registering the
       Gate upgrades:
       ```pascal
       upgplace := 'ukrwwa';
       _country_AddUpgradeWithAccessControl(country, upgplace+'.1', 2, ..., gc_upg_type_single_buildgate, 5, ..., 0, 400, 0, ...);  // 400 wood
       country.upgrade[ind-1].bindividual := True;
       ...
       if (rus) then begin upgplace := 'russwa'; ... 0, 0, 500, ... end; // 500 stone
       if (tur) or (alg) then begin upgplace := 'turswa'; ... 0, 0, 500, ... end;
       if (not ukr) then begin upgplace := 'eurswa'; ... 0, 0, 500, ... end;
       ```
[^19]: `data/scripts/lib/unit.script:11429` — condition in
       `_unit_DoExplosion`:
       `if (not gbool_gui_gatefinished) or (TObjProp(pobjprop).usage<>gc_obj_usage_hardwall) then`.
       After the first `_player_ConstructGates` call, hard-Wall
       explosion debris is disabled for the rest of the match.

[^20]: `data/scripts/lib/unit.script:6572-6608` —
       `_unit_ControlBuildProgress`. The Gate-specific branch at the
       start of the procedure:
       ```pascal
       if (gObjProp[TObj(pobj).cid][TObj(pobj).id].bwall) and (TObj(pobj).individual.upglevel>0) then
          TObj(pobj).hp := gPlayer[TObj(pobj).pl].objbase[TObj(pobj).cid][TObj(pobj).id].maxhp;
       ```
       The subsequent
       `if hp >= maxhp then _unit_SetTagStates(hnd, gc_statetag_essential_none ...)`
       triggers the `OnTagStates` handler [^10], which sets
       `bbuilt := True`.
