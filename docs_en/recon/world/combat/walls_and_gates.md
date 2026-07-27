<a id="recon-стены-и-ворота"></a>
<a id="стены-и-ворота"></a>
# Walls and Gates

[← How the game works](../../README.md)

This article explains how Wall lines are placed and built, where a Gate is
allowed, and why any enemy non-building object can destroy a segment instead
of capturing it. Internal structures and call sequences are collected under
[Technical Details](#technical-details).

<a id="коротко"></a>
## At a Glance

- The player drags a line with the mouse; Peasants then construct every
  segment **like an ordinary building** [^2][^3].
- One segment occupies one cell. A longer Wall is a gapless sequence of
  connected segments [^4].
- Segment orientation determines the available builder positions, with up
  to 16 positions supported [^5].
- All 21 nations have a **Palisade** and its **Gate**. Every nation except
  Ukraine also has a **Stone Wall** [^6].
- A Gate upgrades one selected completed segment [^7]. It costs 400 Wood for
  a Palisade or 500 stone for a Stone Wall. It requires **a straight run of
  three identical completed segments**; Wall ends, corners,
  T-intersections, and unfinished sections are rejected [^8].
- A Gate appears **instantly and at full durability**. Peasants do not
  participate [^9][^10].
- Any enemy non-building object within four cells—including a Peasant or an
  artillery piece—**does not take ownership** of a Wall or Gate; it destroys
  the segment [^11]. A friendly defender within roughly eight cells prevents
  demolition. Below one-third durability,
  this capture check is skipped and the segment must be finished with
  weapons [^12].

---

<a id="1-типы-стен-и-их-доступность"></a>
## 1. Wall Types and Availability

The game has Palisades and Stone Walls [^1]. All 21 nations can build a
Palisade. Every nation except Ukraine can build a Stone Wall; its appearance
and parameters differ for European nations, Russia, Turkey, and Algeria
[^6].

| Variant | Availability | Wall / Gate durability | Segment price | Build time | Segment upkeep |
|---|---|---:|---:|---:|---:|
| **Palisade** | every nation except Ukraine's special variant | 1,500 / 1,000 | 10 Wood | 18 frames | none |
| **Ukrainian Palisade** | Ukraine | 2,500 / 1,500 | 12 Wood | 26 frames | none |
| **European Stone Wall** | all except Ukraine, Russia, Turkey, and Algeria | 50,000 / 32,000 | 50 Stone | 288 frames | 0.4 Stone/s |
| **Russian Stone Wall** | Russia | 50,000 / 32,000 | 60 Stone | 640 frames | 0.32 Stone/s |
| **Turkish Stone Wall** | Turkey and Algeria | 50,000 / 32,000 | 60 Stone | 384 frames | 0.24 Stone/s |

Stone Wall upkeep is consumed continuously while a segment stands [^1].
One European segment consumes 24 Stone per game minute, a Russian segment
19.2, and a Turkish segment 14.4. Ukraine has only the Palisade and cannot
build a Stone Wall.

Nation-by-nation values are listed in the
[building guide](../../../reference/03_buildings/README.md).

<a id="2-footprint-и-кластеры"></a>
<a id="2-занимаемая-площадь-и-линии-стен"></a>
## 2. Footprint and Wall Lines

One Wall segment occupies one cell. Consecutive segments connect without
gaps:

```
[wall][wall][wall]   ← a 3-cell line
```

An unbroken line is a continuous pathfinding obstacle. Destroying one
segment opens a passage, and the remaining neighbors reconnect [^13].

<a id="21-wall-variations-и-builder-slots"></a>
<a id="21-варианты-сегментов-и-места-для-строителей"></a>
### 2.1. Segment variants and builder positions

The places from which Peasants build and repair a segment depend on its
orientation: a straight section, corner, and junction need different
approaches. Up to 16 such positions are supported. The default orientation
is handled like an ordinary building [^5][^14].

<a id="3-постройка-стены-крестьянами"></a>
## 3. Wall Construction by Peasants

The interface shows blue preview segments before placement is confirmed
[^15]. Each real segment then appears with 10 durability, and assigned
Peasants approach free builder positions to increase its durability and
completion. See
[Building Construction, Repair, and Destruction §3](../economy/building_mechanics.md).
An ordinary Wall uses the ordinary building rate, and completion is the
current durability divided by maximum durability [^10][^16].

Resources are charged separately for every segment. Canceling an unfinished
segment uses the ordinary demolition and refund rules.

<a id="4-захват-и-снос-сегмента"></a>
## 4. Capturing and Demolishing a Segment

An ordinary capturable building changes owner when an enemy unit capable of
capturing buildings comes within four cells and no defender is nearby. Walls
and Gates use a special rule [^11]:

1. The game looks for any nearby enemy non-building object. The ability to
   capture ordinary buildings is not required, so Peasants and artillery
   pieces also qualify.
2. Below one-third of maximum durability, the remaining capture logic is skipped
   and weapons must finish the segment [^12].
3. A friendly defender within roughly eight cells cancels demolition.
4. Otherwise, finding a valid enemy destroys the segment immediately.

This applies to both completed and unfinished segments **while they have at
least one third of their maximum durability**. Below that threshold, the
capture-based demolition check is skipped and weapons must finish the
segment. Ownership is never transferred.

The rule is identical for Walls and Gates.

<a id="5-ворота-как-моментальный-апгрейд"></a>
<a id="5-ворота-как-мгновенное-улучшение"></a>
<a id="5-как-создаются-ворота"></a>
## 5. Creating Gates

A Gate is an individual upgrade applied to one selected Wall segment
[^7][^17].

| Wall type | Price | Applied to |
|---|---|---|
| **Palisade** | 400 Wood | selected Palisade segment |
| **European Stone Wall** | 500 Stone | selected European segment |
| **Russian Stone Wall** | 500 Stone | selected Russian segment |
| **Turkish Stone Wall** | 500 Stone | selected Turkish segment |

Before the upgrade starts, the game checks the Wall's geometry [^8]. It
accepts the placement only when:

1. the selected segment is **not at the end** of the line, with
   neighbors on both sides;
2. both neighbors use the same sprite, so the Wall is straight rather
   than a corner or T-intersection;
3. all three segments are **complete**;
4. exactly three Wall segments, no more, lie within 1.85 cells of the
   center.

If any condition fails, the upgrade is blocked. A Gate can therefore be
placed only in the middle of a straight run of at least three completed
segments.

<a id="51-что-происходит-при-срабатывании-апгрейда"></a>
<a id="51-что-происходит-при-создании-ворот"></a>
### 5.1. What happens when a Gate is created

The game replaces the central segment with a new Gate object, updates the
neighbouring sprites, and transfers the interface selection to the new
object [^9]. No Peasants are assigned.

On the next tick, a special rule for an upgraded Wall immediately raises
durability to its maximum and marks the object complete [^10][^16][^20].
The Gate therefore appears **instantly and at full durability**.

<a id="52-подмена-цели-при-создании-ворот"></a>
<a id="52-почему-атакующие-могут-потерять-цель"></a>
### 5.2. Why attackers can lose their target

Replacing the object has a practical combat consequence:

- an enemy attacks a specific Wall segment;
- the defender turns it into a Gate if the Wall geometry allows;
- the old segment is replaced by a new object;
- the attackers lose their target and need a new attack order against
  the Gate;
- damage accumulated on the old segment does not carry over. The Gate
  appears at full durability: 32,000 when made from a Stone Wall and
  1,000–1,500 when made from a Palisade. A damaged Wall segment has
  effectively been replaced with a fresh Gate.

<a id="6-стенные-башни"></a>
## 6. Wall Towers

Some nations have dedicated Wall Towers. They fit into a Wall line without
a gap and fire like an ordinary Tower. Their targeting and ammunition costs
are covered in [Tower mechanics](towers.md).

<a id="technical-details"></a>
<a id="технические-подробности"></a>
<a id="7-технические-подробности"></a>
## 7. Technical Details

| Game variant | Wall / Gate | Class and material |
|---|---|---|
| Palisade | `ukrwwa` / `ukrwga` | `gc_obj_usage_weakwall`, `gc_obj_material_woodwall` |
| European Stone Wall | `eurswa` / `eursga` | `gc_obj_usage_hardwall`, `gc_obj_material_building` |
| Russian Stone Wall | `russwa` / `russga` | `gc_obj_usage_hardwall`, `gc_obj_material_building` |
| Turkish Stone Wall | `turswa` / `tursga` | `gc_obj_usage_hardwall`, `gc_obj_material_building` |

The `buildtime` and `consume.stone` fields set construction time and
continuous upkeep. The `consume.stone` values are 250 for the European,
200 for the Russian, and 150 for the Turkish variant; the per-second
deduction is `consume.stone × 32 / 20000`. A Gate is distinguished by
`bgate = True`; ordinary Wall completion is stored in `bbuilt`.

A Wall has `usage = gc_obj_usage_hardwall` or
`gc_obj_usage_weakwall` and `bwall = True`; a Gate additionally has
`bgate = True` [^1]. Lines are stored by `gWallSystem` as
`TWallCluster` records containing Wall type, nation, owner, and an array of
`TWallCell` entries [^4]. When a segment dies, `_unit_OnDeath` calls
`gWallSystem.RemoveHandle` to delete the cell and update neighbouring
connections [^13].

`_player_ConstructBuildingList` creates a segment with
`bbuilt = False`, `buildprogress = 0`, and `hp = 10`, after which
`_player_OrderUnitsToBuild` assigns Peasants [^2][^3]. Wall variants use
`gCustomBuildPointsWall[wallvariation]`; `wallvariation = 0` uses the
ordinary `gCustomObjPoints` instead [^5]. The limit is
`gc_MaxWallBuilderPointsCount = 16`, with data loaded from
`data/game/var/wallcustom.cfg` [^14].

Demolition runs through `_misc_CheckCapture`.
`_unit_SearchCapturersForWall` requires only an enemy owner and
`not bbuilding`, not `bcancapture`, so Peasants and artillery pieces also
qualify. `_unit_SearchProtectors` then looks for a friendly `bprotector`
within `gc_gameplay_protectionradius` (roughly eight cells) and clears
`bcapture` if one is present. Otherwise, the `bwall` branch sets
`bDie := True` and `gc_statetag_essential_death`; at
`hp < maxhp / 3`, this check is skipped [^11][^12].

The individual `gc_upg_type_single_buildgate` upgrade creates a Gate.
`_misc_GetGateBaseSprite` permits it only on a straight, completed,
three-segment run [^7][^8]. `_player_ConstructGates` replaces the central
object and increments `individual.upglevel` [^9]. Then
`_unit_ControlBuildProgress` executes
`if (bwall) and (upglevel > 0) then hp := maxhp`, while
`OnTagStates.essential_none` sets `bbuilt := True` and
`buildprogress := 1` [^10][^20]. After the first Gate,
`gbool_gui_gatefinished` also changes the visual Stone Wall explosion path
in `_unit_DoExplosion` [^19].

<a id="источники"></a>
## Sources

[^1]: `data/scripts/lib/unit.script:2258-2310` —
      `commonsid+'swa'` / `commonsid+'sga'` for Stone Walls and Gates
      in the `eur`, `rus`, and `tur` families; `'ukrwwa'` /
      `'ukrwga'` for the Palisade and its Gate. This code assigns
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
       `bcancapture` requirement. The exact condition in
       `data/scripts/lib/unit.script:4666-4691` accepts any enemy object with
       `not bbuilding`, including Peasants and artillery. Lines
       `miscext.script:1041-1068` search for a friendly `bprotector` within
       `gc_gameplay_protectionradius` and clear `bcapture` when one is
       present. Line 1106 enters the special `bwall`
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
