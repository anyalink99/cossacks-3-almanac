<a id="recon-дипломатические-центры-и-наёмники"></a>
# Recon: diplomatic centers and mercenaries

Reverse engineering of the subsystem for hiring mercenaries through the diplomatic center
(`<nat>dip`): economy, upkeep with gold, riot `Rebellion`, scaling limit
prices. All links to the code and the Pascal blocks themselves are collected in the section
[Sources](#sources) at the end of the document.

**Related documents:**

- [peasant_extraction.md](../world/economy/peasant_extraction.md) - flag semantics
  `bnohungry`; for mercenaries it is `True` - they do not eat food.
- [building_mechanics.md](../world/economy/building_mechanics.md) – footprint and model
  construction of a diplomatic center.
- [server_sync_architecture.md](../../../internals_en/engine/server_sync_architecture.md) —
  Reassignment of mercenaries during a riot occurs through `_misc_ChangePlayer`,
  this is a server-authoritative event.
- [determinism_audit.md](../../../internals_en/engine/determinism_audit.md) - transition during a riot
  uses `_misc_RandomInt` (seeded RNG).

## TL;DR

- **Diplomatic Center** (`<nat>dip`) - mid-game building for each
  21 nations. Price ≈ 6.6k wood + stone, 4500 HP, prerequisites - Academy
  and Town Hall.
- Produces **8 mercenaries** (6 basic + 2 from Early Bird-DLC). Catalog
  **same for all nations** - unit stats do not depend on who owns them
  hires; only `sid` changes.
- Mercenary costs **only gold** when hired, flag `bnohungry = True`
  (doesn't eat food), but **constantly consumes gold** as upkeep
  (`consume.gold > 0`).
- When a player runs out of gold **and** `resconsume[gold] > resincome[gold]`,
  flag `brebellion` is raised. On every Nothing tick every mercenary
  has a chance to move to the global NPC slot “mercenary”
  (`gc_player_mercenaryind = MaxPlayerCount - 1`):
  - **easy:** 0.305% per tick
  - **normal:** 0.610% per tick
  - **hard and higher:** 18.31% per tick
- This NPC slot is always hostile to all real players.

---

<a id="1-дипломатические-здания-по-нациям"></a>
## 1. Diplomatic buildings (by nation)

All 21 nations have exactly one diplomatic center, registered uniformly
to `country.script` via `_country_AddMember` with category
`gc_country_editorplace_category_buildings` and AI role
`gc_ai_unit_dipcenter` [^1].

Stats are dispatched in `unit.script` by `csid+'dip'`: base values for
17 "European" nations, and individual overrides for `rus`, `ukr`,
`tur`, `alg` [^2].

Argument order `SetObjBuildingExtProperties`:
`maxhp, buildtime, costpercent, bcapture, score, usage, food, wood, stone, gold, iron, coal` [^3].

Please note: in individual branches the argument `gold` is set to `0`,
but next to it is the comment `0{1000}`. This is a marker that in Cossacks 1 the price was
1000 gold, but in Cossacks 3 it was reset.

| Building | nation(s) | HP | buildtime (frames/wall-sec/32/g-sec ×10/32) | wood | stone | gold | bcapture |
|---|---|---:|---:|---:|---:|---:|---|
| `<nat>dip` (default - 17 of 21) | aus, fra, eng, spa, pol, swe, pru, ven, net, den, por, pie, sax, bav, hun, swi, sco | 4500 | 1000 / 31.25s / 312.5g-s | 4900 | 1700 | 0 | False |
| `rusdip` | rus | 6500 | 1000 | 7900 | 3700 | 0 | False |
| `ukrdip` | ukr | 5000 | 1000 | 3900 | 2700 | 0 | False |
| `turdip` / `algdip` | tur, alg | 5500 | 1000 | 4600 | 2020 | 0 | False |

Preconditions (from field `prereqs` to `data.json["buildings"]`, for example
`ausdip → ['ausaca']`): deepcenter requires that Academy already exist.
The building is **not captured** (`bcapture=False`).

`costpercent=100`, so each subsequent diplomatic center is no more expensive than the previous one -
but the localization is unambiguous: `data/locale/en/units.txt @%nat%dip.ext` reads
**"You can only build one diplomatic center."** Mechanism: probably
the limitation is implemented through the GUI / switch `bproduceenabled`, not
via costpercent. An open question (see §8).

`gc_obj_usage_dipcenter = 32` [^4] - used by the map setting `marketdip`
(see §5).

---

<a id="2-каталог-наёмников"></a>
## 2. Mercenary catalog

8 mercenary members - registered in **each** nation in a uniform set
calls `_country_AddMember`: 6 basic (`lightinfantrydip`, `roundshierdip`,
`grenadierdip`, `archerdip`, `cossacksichdip`, `dragoon18dip`) and 2 of
Early Bird-DLC (`archerturdip`, `lightcavalrydip`) [^5].

All 21 nations also receive FixedProduce posting via
`_country_AddFixedProduceWithAccessControl` with the same set of names, with
standard prereqs `csid+'cen'` and `csid+'aca'` [^6]. This means: for
production of a mercenary requires Town Hall, Academy **and** diplomatic center (the last one is
the building itself in which `member` lives).

<a id="21-детектирование-bmercenary"></a>
### 2.1 Detection `bmercenary`

The `bmercenary := True` flag is set by a list of names, not by a field
data - the dispatcher compares `sid` with eight dip suffixes through
`StrExists(sid, 'dip')` and an explicit enumeration of [^7].

Inside `case` of each unit (for example, `'archer','archerdip','archertur','archerturdip',...`)
block `if (bmercenary) then begin ... end` overrides hp/weapon/price/`consume`/`bnohungry`/`costpercent`.
The dispatcher uses the same `case` as for a normal unit and then narrows it down.

> From 2026-04-30 `docs/data.json` correctly takes into account `if (bmercenary)` -
> `parse_units.py` retrieves the merc block and `_compute_effective_unit` applies
> it for sids from `BMERCENARY_SIDS` (8 dip suffixes). All 168 lines
> (8 sid × 21 nations) now have merc stats. The values below are read from
> `unit.script` and coincide with what is in `data.json`.

<a id="22-статы-каждого-наёмника"></a>
### 2.2 Stats of each mercenary

| sid | dispatch | HP | buildtime(frames) | gold (price) | consume.gold | costpercent | weapon (damage/range/type) |
|---|---|---:|---:|---:|---:|---:|---|
| `lightinfantrydip` | `'lightinfantry','lightinfantrydip'` | 50 | 40 | 4 | 4 | 100 (default) | sword 16, range 50px |
| `roundshierdip` | `'roundshier','roundshierdip','swordsmansco'` | 75 | 48 | 12 | 20 | 100 (default) | sword 6, range 50px |
| `archerdip` | `'archer','archerdip','archertur','archerturdip','archersco','archerscodip'` | 20 | 40 | 15 | 16 | 100.5 | 25 arrow / 100 firearm, range 700/750 |
| `archerturdip` | same case | 20 | 40 | 15 | 16 | 100.5 | same |
| `grenadierdip` | `'grenadier','grenadierdip',…` | 30 | 48 | 25 | 60 | 100.5 | pike 30 / bullet 16 (range 800) / grenade 200 (range 400) |
| `cossacksichdip` | `'croat','hussar',…,'cossacksich','cossacksichdip',…` | 150 | 80 | 60 | 150 | 100.5 | horse saber 8, range 20px |
| `dragoon18dip` | `'dragoon',…,'dragoon18','dragoon18dip','lightcavalry','lightcavalrydip'` | 100 | 64 | 120 | 120 | 102 | horse bullet 18, range 800 |
| `lightcavalrydip` | same case | 100 | 64 | 120 | 120 | 102 | same |

Exact lines in `unit.script` for each unit and location of `bnohungry`
and resetting food/wood/stone/iron/coal - see [^8].

`bnohungry := True` is placed in every Mercenary block - mercenaries do not pay
food upkeep (`reference_food_upkeep.md`).

Price components food/wood/stone/iron/coal for mercenaries are all equal to 0 - challenges
`SetObjBasePrice(objbase, 0, 0, 0, gold, 0, 0)` reset everything except gold.
That is, **mercenaries only cost gold** when hired.

<a id="23-масштабирование-цены-и-общий-счётчик"></a>
### 2.3 Price scaling and general counter

`costpercent` for mercenaries = 100, 100.5 or 102 - each subsequent copy costs
`floor(base × (costpercent/100)^N)` (see `reference_costpercent_scaling.md`).
For mercenaries the limit is **lower than for regular units** [^9]:

- Paired `sid` divide the counter: `archerdip ↔ archerturdip` and
  `dragoon18dip ↔ lightcavalrydip` via branch `case sid of` summarize
  `gPlayer[plInd].counter.all[cid][tmpid]`.
- Multiplier `costmodifier = pow(costpercent/100, count)` is cut off by
  condition `if bmercenary and (costmodifier > 2) then costmodifier := 2`,
  whereas for normal units the ceiling is `20000`.

Two consequences:

1. **`archerdip` and `archerturdip` share the price counter** (same for
   `dragoon18dip ↔ lightcavalrydip`). Hiring 100 `archerturdip` increases
   price `archerdip`.
2. The price of a mercenary can increase to a maximum of **2×** from the base, and not up to 20000×.
   That is, unlike ordinary units, mercenaries do not become exorbitantly
   expensive - with `costpercent=100.5` the 2× ceiling is achieved approximately
   `ln(2)/ln(1.005) ≈ 139` for mercenaries (hereinafter the price is flat).

---

<a id="3-механика-upkeep--потребление-золота"></a>
## 3. Upkeep mechanics - gold consumption

Upkeep is consumed every frame in the same general cycle as food
(`reference_food_upkeep.md`). Handler – `_player_ProcessResourceConsume`
in `player.script` [^10].

Pseudocode:

- For each resource `i`, `resconsume = gPlayer[plInd].counter.resconsume[i]` is taken.
- `resconsume × gc_time_to_frames × deltatime` is added to the bank once per frame,
  where `gc_time_to_frames = 32`.
- `value = floor(bank / 20000)` — integer number of resource units to be written off.
- If the player has enough stock, `value`, the riot/hunger flag, is written off
  removed.
- If there is not enough, everything that is is written off and the corresponding one is raised
  flag (`bfamine` for food, `brebellion` for gold).

<a id="скорость-утечки-золота"></a>
### Gold Leakage Rate

Same formula as for food upkeep - *`consume.gold` units per game
second per player*:
```
drain_per_g_sec = sum_over_units(consume.gold) × 32 / 20000
```
That is, one `dragoon18dip` with `consume.gold=120` pumps out
`120 × 32 / 20000 = 0.192 gold/g-sec` ≈ **11.5 gold/g-min**. Army mid-game
out of 50 `dragoon18dip` takes away `50 × 0.192 = 9.6 gold/g-sec` ≈ 576 gold/g-min —
this is only supported by the market+gold mine combination.

<a id="bfamine-vs-brebellion--асимметрия"></a>
### `bfamine` vs `brebellion` - asymmetry

Both flags are reset to `False` when the player has the resources to pay.
Both are put in `True` when there are no resources. **But for gold** there is
additional protection: riot only triggers if
`resconsume[gold] > resincome[gold]` [^11]. This means: if your income is from
gold covers the leak, then even a momentary zero in the account will not cause
riot. Only when you are **structurally** in deficit AND the gold buffer is empty -
The riot flag snaps on.

Additional insurance: `brebellion` is reset if `res[gold] >= 2`
or if `resconsume[gold] <= 0` (there is no one else to pay for) [^12]. That is
the dismissal of all mercenaries immediately ends the rebellion.

---

<a id="4-триггер-бунта"></a>
## 4. Riot trigger

The logic of defection lives in the per-unit Nothing handler
`units/unit.inc/nothing.inc` (in the same place where the cycle of random death from
hunger) [^13]. Launch conditions:

- `gPlayer[plInd].brebellion = True`,
- `objprop.bmercenary = True`,
- `plInd <> gc_player_mercenaryind` (not the mercenary slot itself),
- unit - `bplayable`.

Next - throw RNG `_misc_RandomInt` (`floor(random × 32768)`,
`gc_c1rand_to_random = 32768`) [^14] with a threshold depending on complexity
player.

| difficulty | `_misc_RandomInt < threshold` | probability for one Nothing-tick |
|---|---|---:|
| 0 (easy) | 100 | 100/32768 ≈ **0.305%** |
| 1 (normal) | 200 | 200/32768 ≈ **0.610%** |
| >1 (hard / very hard / impossible) | 6000 | 6000/32768 ≈ **18.31%** |

The Nothing handler runs on every progress tick for idle/walking units,
therefore, on hard levels **a typical mercenary deserts within 5-6 ticks
after `brebellion = True`** - in fact the entire army of mercenaries goes to
to the enemy for several game seconds.

When RNG is triggered, the unit is transferred to the NPC slot via
`_misc_ChangePlayer(myHnd, plMercHnd, False, False, True)`. Mercenary slot -
`gc_player_mercenaryind = gc_MaxPlayerCount-1` [^15]. This player is tough
registered as an enemy for all other slots when initializing the map:
each real player's mask `enemyplmask` includes the NPC slot bit [^16].

Therefore, deserted mercenaries become hostile to **everyone**, including
former owner. They are not destroyed.

The mercenary player slot starts with a fixed supply of resources: 20k gold
and 10k of the rest [^17]. This is necessary so that deserted mercenaries can
pay themselves upkeep before they themselves start a rebellion - but since they are already in
mercenary slot, it doesn't matter.

<a id="реакция-ai"></a>
### AI reaction

Riot status also affects AI defense scoring [^18]: for already captured
units `scoremodifier = 5`, for their mercenaries with `brebellion = True` -
`scoremodifier = 3`, for others - `scoremodifier = 2`. AI reduces
the priority of protecting one's own mercenaries when they are on the verge of desertion.

---

<a id="5-map-настройка-marketdip"></a>
## 5. Map setting `marketdip`

`gMap.settings.additional.marketdip` controls the availability of markets and
diplomatic centers in the party. All 5 meanings with canonical Russian names -
[`reports/map/lobby_settings.md`](../../reports/map/lobby_settings.md#marketdip--рынок-и-дипцентр);
engine behavior - [`game_settings.md`](../world/map/game_settings.md) §3.5.

Constants [^19]:

- `gc_mapsettings_marketdip_default = 0` - both are enabled,
- `gc_mapsettings_marketdip_nodip = 1` — deep centers are disabled (`bproduceenabled := False`),
- `gc_mapsettings_marketdip_nomarket = 2` - markets are disabled,
- `gc_mapsettings_marketdip_noboth = 3` - both are disabled,
- `gc_mapsettings_marketdip_expensivemercs = 4` — the price of each mercenary × 3.

Branch `expensivemercs` lives in `player.script` [^20]: if
`objprop.bmercenary = True`, then for each resource
`TObjBase(pobjbase).price[res]` is multiplied by `gc_gameplay_expensivemercskoef = 3` [^21].
In the lobby with `expensivemercs`, the gold price of mercenaries is tripled
(4 → 12, 60 → 180, 120 → 360, 150 → 450, …). The multiplier is applied to
**all** slot prices, but since mercenaries only have non-zero
`price[gold]`, only the gold value is tripled.

---

<a id="6-нейтральные-дипцентры--точки-найма"></a>
## 6. Neutral deep centers / hiring points

**No.** Search in `data/scripts` for substrings `peasantdip`, `townhalldip`,
`tradehouse`, `gc_player_neutralind`, `bneutral` - none of these patterns
does not spawn neutral villages or pre-placed deep buildings on
standard skirmish maps. The only "neutral" concepts are:

- Field `bneutral` for `gPlayer` [^22] - set/removed only from
  scripted scenarios. On skirmish all real players have `bneutral = False`.
- Mercenary owner slot `gc_player_mercenaryind` exists from initialization
  card, but has *no buildings* - he is purely a recipient for
  deserted units.

Therefore, on standard random maps **the only way to recruit
mercenaries - build your own `<nat>dip`** (price + prereqs as in §1).

Custom scenarios can pre-deploy neutral deep centers and use
`_misc_ChangePlayer`, etc. (for example, some campaign maps), but this
specificity of the content, not the engine.

---

<a id="7-кросс-национальная-доступность"></a>
## 7. Cross-national availability

Since all 8 mercenaries are added via `_country_AddMember` in **each**
national roster, and the FixedProduce posting is in the same thread
"for all nations", **any nation can hire any mercenary**. 6 basic
(`roundshierdip`, `lightinfantrydip`, `archerdip`, `grenadierdip`,
`cossacksichdip`, `dragoon18dip`) - certainly. 2 EarlyBird mercenaries
(`lightcavalrydip`, `archerturdip`) require `bEarlyBird` (DLC purchased) [^5].

No mercenary has a nation suffix in `sid` (unlike `pikemanrus`,
`pikemansco`, etc.), and unit initialization puts `bmercenary` without
filtering by nation [^7].

“National” infix in paired `sid` (`archerdip` vs `archerturdip`,
`dragoon18dip` vs `lightcavalrydip`) is a purely **art/model option**:
same stats, same general price counter (§2.3), just aesthetic
“Western”/“Eastern” variation of the same combat functionality.

The rules for officer formations differ slightly [^23]: `roundshierdip` and
`grenadierdip` can be included in standard infantry formations along with
national pikemen/musketeers. `archerdip`, `archerturdip`,
`lightinfantrydip` go through a separate registration `…NoOfficersExtDip` -
form their own formations without a national officer.

---

<a id="8-наёмник-vs-обычный-юнит--сравнение"></a>
## 8. Mercenary vs regular unit - comparison

<a id="стоимость"></a>
### Cost

Mercenaries cost **gold only + construction time**; regular units – food +
iron + coal (plus food for upkeep). For example, for a heavy mounted rifleman:

| Unit | food | iron | coal | gold | weapons.cost (per shot, iron+coal) | hp | buildtime |
|---|---:|---:|---:|---:|---|---:|---:|
| `dragoon18` (regular, eu) | 70 | 7 | 0 | 60 | iron 4 + coal 5 | 225 | 720 frames |
| `dragoon18dip` (mercenary) | 0 | 0 | 0 | 120 | iron 5 + coal 8 | **100** | **64 frames** |

That is, a hired Dragoon costs +60 gold and zero food/iron/coal when hired,
**builds 11x faster**, but has 44% of normal HP and burns a little
more iron+coal per shot. And he constantly loses 120 gold.
The same pattern for Archer (`archer` btf 32 → `archerdip` btf 40 - formally
a little slower, but a mercenary of this tier costs 0 food versus 20 and has damage
25 versus 15).

### Upkeep

- Normal units: food upkeep `(consume.food + (bnohungry?0:30)) × 32/20000`
  for g-sec (`reference_food_upkeep.md`). Mercenaries with `bnohungry` → no leak
  food.
- Mercenaries: gold upkeep `consume.gold × 32/20000` for g-sec, depends on
  `consume.gold` (4–150 per mercenary).
- Officers/Royal Musketeers also have `consume.gold` (60–150), but they
  **not** `bmercenary`, so they don’t rebel.

<a id="когда-брать-наёмников-стратегический-профиль"></a>
### When to take mercenaries (strategic profile)

The Mercenary Catalog is essentially a **quick deployment army for gold**:

- **Early game.** Nations with an abundance of wood and poor access to iron/coal
  can instantly get infantry by exchanging wood and stone for gold
  through the market and immediately hiring `roundshierdip` or `lightinfantrydip`.
- **Mid-game.** Goldth peak (allied trade, captured gold
  mines) converts well into a fast army `dragoon18dip` - without
  waiting for coal mines.
- **Glass cannon.** HP is about half that of regular units
  the same class - but the advantage is the speed of hiring at the top tier
  huge: `dragoon18dip` trains 64 frames versus 720 for a regular one
  `dragoon18` - **11.25 times faster**.

**The main risk is the loss of income from gold during a riot.** It’s worth losing
`income[gold]`, and the entire army of mercenaries deserts in seconds (on hard and
above). Standard counter-play - disband the mercenaries **before**
as `gold` will drop to zero.

---

<a id="9-открытые-вопросы"></a>
## 9. Open questions

| # | Question | Where to dig |
|---:|---|---|
| 1 | Limit “one diplomatic center per player” - the localization states “you can only build one diplomatic center”, but there is no explicit check in the scripts of the form `if count(dip) >= 1 then bproduceenabled := False`. `<nat>dip` `costpercent = 100` also does not block. | `gui.script`, or quota `_ai_TryUnit`. The AI ​​logic checks for `_ai_GetUnitCount(plind, cid, gc_ai_unit_dipcenter) > 0`, but this is not enforcement for the human player. |
| 2 | `bnoreputation` - does not appear in any installation script. It's possible that this field referred to Cossacks 1/2, or that we have the wrong name. | grep over all .script + .global. |
| 3 | Riot tick frequency in real time - Nothing-handler fires once every progress-tick. | Reconciliation with [`ticks_and_subticks.md`](../../../internals_en/engine/ticks_and_subticks.md) §3. Reference point: with Nothing-tick ≈ 135 ms, mercenaries switch to hard in less than 1 second; at ≈ 100 ms - in ~0.5 seconds. |
| 4 | `bmercenary = True` for a battleship in `data.json` - 20 battleship lines are marked `bmercenary = True`, but in `case 'battleship'` this flag is not explicitly set inside `unit.script`. | Perhaps this is a separate branch (ports?) or a parser artifact. 5 minutes check. |

---

See also **TL;DR** at the beginning of the file - there is a short overview of the same
facts in the form of a bulleted list.

---

<a id="источники"></a>
## Sources

All links are relative to `data/scripts/` in the Cossacks 3 installation.

[^1]: Registration of the diplomatic center in the national roster - `lib/country.script:2829`:
    ```pascal
    _country_AddMember(country, csid+'dip', ind, True,
                       gc_country_editorplace_category_buildings, 20,
                       gc_ai_unit_dipcenter);
    ```
[^2]: Stat dispatching by `csid+'dip'` with national overrides —
    `lib/unit.script:2451-2459`:
    ```pascal
    csid+'dip' : begin
       SetObjBuildingExtProperties(objprop, objbase,
           4500, 1000, 100, False, 500,
           gc_obj_usage_dipcenter,
           0, 4900, 1700, 0{1000}, 0, 0);
       case i of
          rus : SetObjBuildingExtProperties(objprop, objbase,
                  6500, default, default, False, default, default,
                  0, 7900, 3700, 0{2500}, 0, 0);
          ukr : SetObjBuildingExtProperties(objprop, objbase,
                  5000, default, default, False, default, default,
                  0, 3900, 2700, 0{500}, 0, 0);
          tur : SetObjBuildingExtProperties(objprop, objbase,
                  5500, default, default, False, default, default,
                  0, 4600, 2020, 0{1300}, 0, 0);
          alg : SetObjBuildingExtProperties(objprop, objbase,
                  5500, default, default, False, default, default,
                  0, 4600, 2020, 0{1300}, 0, 0);
       end;
    end;
    ```
[^3]: Signature `SetObjBuildingExtProperties` - `lib/unit.script:503`. Order
    arguments: `maxhp, buildtime, costpercent, bcapture, score, usage, food, wood, stone, gold, iron, coal`.

[^4]: `gc_obj_usage_dipcenter = 32` - `dmscript.global:339`.

[^5]: Registration of 8 mercenaries via `_country_AddMember` —
    `lib/country.script:2786-2793, 2900-2901`:
    ```pascal
    _country_AddMember(country, 'lightinfantrydip', ind, True, ...gc_ai_unit_light_dip);
    _country_AddMember(country, 'roundshierdip',    ind, True, ...gc_ai_unit_round_dip);
    _country_AddMember(country, 'grenadierdip',     ind, True, ...gc_ai_unit_grendip);
    _country_AddMember(country, 'archerdip',        ind, True, ...airole);
    _country_AddMember(country, 'cossacksichdip',   ind, True, ...gc_ai_unit_cossackdip);
    _country_AddMember(country, 'dragoon18dip',     ind, True, ...gc_ai_unit_dragundip);
    // "early-bird" extension (DLC):
    _country_AddMember(country, 'archerturdip',     ind, True, ..., gc_ai_unit_none);
    _country_AddMember(country, 'lightcavalrydip',  ind, True, ..., gc_ai_unit_none);
    ```
[^6]: FixedProduce wiring for 8 mercenaries - `lib/country.script:3010-3022`:
    ```pascal
    member := csid+'dip';
    fixedproduceind := _country_GetFixedProduceIndexBySID(cid, member, bAddIfNotExist);
    _country_AddFixedProduceWithAccessControl(country, fixedproduceind, member,
       'roundshierdip',    0, 0, ind, csid+'cen', csid+'aca', '');
    _country_AddFixedProduceWithAccessControl(country, ..., 'lightinfantrydip', 1, 0, ind, csid+'cen', csid+'aca', '');
    _country_AddFixedProduceWithAccessControl(country, ..., 'archerdip',        2, 0, ind, csid+'cen', csid+'aca', '');
    _country_AddFixedProduceWithAccessControl(country, ..., 'grenadierdip',     3, 0, ind, csid+'cen', csid+'aca', '');
    _country_AddFixedProduceWithAccessControl(country, ..., 'cossacksichdip',   4, 0, ind, csid+'cen', csid+'aca', '');
    _country_AddFixedProduceWithAccessControl(country, ..., 'dragoon18dip',     5, 0, ind, csid+'cen', csid+'aca', '');
    if (bEarlyBird) then
    begin
       _country_AddFixedProduceWithAccessControl(country, ..., 'lightcavalrydip', 5, 1, ind, csid+'cen', csid+'aca', '');
       _country_AddFixedProduceWithAccessControl(country, ..., 'archerturdip',    2, 1, ind, csid+'cen', csid+'aca', '');
    end;
    ```
[^7]: Detection of `bmercenary` by `sid` - `lib/unit.script:611-614`:
    ```pascal
    var bmercenary : Boolean;
    if StrExists(sid, 'dip') and ((sid='roundshierdip') or (sid='lightinfantrydip')
       or (sid='archerdip') or (sid='grenadierdip') or (sid='cossacksichdip')
       or (sid='dragoon18dip') or (sid='archerturdip') or (sid='lightcavalrydip')) then
    bmercenary := True;
    ```
[^8]: `if (bmercenary) then begin ... end` blocks for each mercenary
    in `lib/unit.script`:

    - `lightinfantrydip` - lines 712-734.
    - `roundshierdip` - lines 735-770.
    - `archerdip` / `archerturdip` (same `case`) - lines 997-1061.
    - `grenadierdip` - lines 1226-1318.
    - `cossacksichdip` - lines 1320-1391.
    - `dragoon18dip` / `lightcavalrydip` (same `case`) - lines 1544-1662.

    Resetting food/wood/stone/iron/coal — `SetObjBasePrice(objbase, 0, 0, 0, gold, 0, 0)`,
    for example: line 725 for `lightinfantry`, 1048 for `archer`, 1382 for
    `cossacksich`, 1651 for `dragoon18`.

[^9]: 2× limit for mercenaries in `_unit_GetCostModifier` —
    `lib/unit.script:5660-5678`:
    ```pascal
    if (bmercenary) then
    begin
       var sid : String = gObjProp[cid][unitID].sid;
       var tmpsid : String;
       case sid of
          'archerdip'       : tmpsid := 'archerturdip';
          'archerturdip'    : tmpsid := 'archerdip';
          'dragoon18dip'    : tmpsid := 'lightcavalrydip';
          'lightcavalrydip' : tmpsid := 'dragoon18dip';
       end;
       var tmpid : Integer = _unit_ConvertObjSIDToID(cid, tmpsid);
       count := count+gPlayer[plInd].counter.all[cid][tmpid];
    end;
    costmodifier := pow(costpercent/100, count);
    if bmercenary and (costmodifier>2) then
    costmodifier := 2
    else
    if (costmodifier>20000) then
    costmodifier := 20000;
    ```

[^10]: `_player_ProcessResourceConsume` — `lib/player.script:268-322`:
    ```pascal
    procedure _player_ProcessResourceConsume(const plInd : Integer; const deltatime : Float);
    begin
       var i : Integer;
       for i:=0 to gc_ResCount-1 do
       begin
          var resconsume : Integer = gPlayer[plInd].counter.resconsume[i];
          if (resconsume>0) then
          begin
             const mult = 100;
             const speed = 20000;
             var resconsumerem : Float = gPlayer[plInd].counter.resconsumeremains[i]/mult;
             resconsume := resconsume*gc_time_to_frames;     // gc_time_to_frames = 32
             var bank : Float = resconsumerem+resconsume*deltatime;
             var realbank : Float = bank/speed;              // speed = 20000
             var value : Integer = floor(realbank);
             if (value<>0) then
             begin
                if (not gPlayer[plInd].res[i]>=value) then
                begin
                   _res_AddResToPlayerByIndex(plInd, i, -value);
                   case i of
                      gc_resource_type_food : gPlayer[plInd].bfamine := False;
                      gc_resource_type_gold : gPlayer[plInd].brebellion := False;
                   end;
                end
                else
                begin
                   _res_AddResToPlayerByIndex(plInd, i, -(not gPlayer[plInd].res[i]));
                   case i of
                      gc_resource_type_food : gPlayer[plInd].bfamine := True;
                      gc_resource_type_gold : begin
                         if (gPlayer[plInd].counter.resconsume[i]>gPlayer[plInd].counter.resincome[i]) then
                         gPlayer[plInd].brebellion := True
                         else
                         gPlayer[plInd].brebellion := False;
                      end;
                   end;
                end;
             end;
             bank := (realbank-value)*speed;
             gPlayer[plInd].counter.resconsumeremains[i] := floor(bank*mult);
          end;
       end;
       ...
    end;
    ```
[^11]: Condition for structural deficit - `lib/player.script:306`:
    ```pascal
    if (gPlayer[plInd].counter.resconsume[i]>gPlayer[plInd].counter.resincome[i]) then
       gPlayer[plInd].brebellion := True
    else
       gPlayer[plInd].brebellion := False;
    ```
[^12]: Final reset `brebellion` - `lib/player.script:318-320`:
    ```pascal
    if (gPlayer[plInd].brebellion) and ((not gPlayer[plInd].res[gc_resource_type_gold]>=2)
       or (gPlayer[plInd].counter.resconsume[gc_resource_type_gold]<=0)) then
    gPlayer[plInd].brebellion := False;
    ```
[^13]: Riot trigger in Nothing handler - `units/unit.inc/nothing.inc:487-506`:
    ```pascal
    if (gPlayer[plInd].brebellion) and (TObjProp(pobjprop).bmercenary)
       and (plInd<>gc_player_mercenaryind) and (bplayable) then
    begin
       if (gInterface.gamemode=gc_gamemode_game) or (gInterface.gamemode=gc_gamemode_spectator) then
       begin
          if ((gPlayer[plInd].difficulty>1) and (_misc_RandomInt<6000))
             or ((gPlayer[plInd].difficulty=0) and (_misc_RandomInt<100))
             or ((gPlayer[plInd].difficulty=1) and (_misc_RandomInt<200)) then
          begin
             var plMercHnd : Integer = GetPlayerHandleByIndex(gc_player_mercenaryind);
             _misc_ChangePlayer(myHnd, plMercHnd, False, False, True);
          end;
       end
       else
       if (plHnd=GetPlayerHandleInterfaceIO) then
       begin
          var s1 : String = 'Rebel, but in editor mode your units wont die';
          ...
       end;
    end;
    ```
[^14]: `_misc_RandomInt` returns `floor(random × 32768)` —
    `lib/misc.script:494-498`. Constant `gc_c1rand_to_random = 32768`.

[^15]: `gc_player_mercenaryind = gc_MaxPlayerCount-1` - `dmscript.global:776`.

[^16]: NPC slot hostility towards all real players - `common.inc/initmap.inc:48-49`:
    ```pascal
    if i<>gc_MaxPlayerCount-1 then
    gPlayer[i].enemyplmask:=1 shl (gc_MaxPlayerCount-1);
    ```
[^17]: Starting resources for the mercenary NPC slot - `lib/player.script:89-99`:
    ```pascal
    if (id=gc_player_mercenaryind) then
    begin
       case i of
          gc_resource_type_food : _res_SetResToPlayerByIndex(id, i, 10000);
          gc_resource_type_gold : _res_SetResToPlayerByIndex(id, i, 20000);
          gc_resource_type_iron : _res_SetResToPlayerByIndex(id, i, 10000);
          gc_resource_type_coal : _res_SetResToPlayerByIndex(id, i, 10000);
          else
          _res_SetResToPlayerByIndex(id, i, 10000);
       end;
    end
    ```
[^18]: AI scoring of unit defense - `lib/unit.script:3941-3946`:
    ```pascal
    if (bcaptured) then
       scoremodifier := 5
    else
    if (gPlayer[pl].brebellion) and (TObjProp(pobjprop).bmercenary) then
       scoremodifier := 3
    else
       scoremodifier := 2;
    ```
[^19]: Constants `gc_mapsettings_marketdip_*` - `dmscript.global:1077-1081`.

[^20]: Applying `expensivemercs` to mercenary prices - `lib/player.script:2741-2774`:
    ```pascal
    gc_mapsettings_marketdip_expensivemercs : begin
       if (TObjProp(pobjprop).bmercenary) then
       begin
          var res : Integer;
          for res:=0 to gc_ResCount-1 do
          TObjBase(pobjbase).price[res] := TObjBase(pobjbase).price[res]*gc_gameplay_expensivemercskoef;
       end;
    end;
    ```
[^21]: `gc_gameplay_expensivemercskoef = 3` - `dmscript.global:214`.

[^22]: Field `bneutral` for `gPlayer` is `lib/classes.script:3698`. Installation/removal
    flag in script scripts - `lib/scenario.script:2182-2238`.

[^23]: Registration of formations for mercenaries - `lib/country.script:2515-2535`.
    `roundshierdip` and `grenadierdip` go through standard infantry
    formations; `archerdip`, `archerturdip`, `lightinfantrydip` —
    via `…NoOfficersExtDip`.
