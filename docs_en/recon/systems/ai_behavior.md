<a id="recon-поведение-ии"></a>
# Recon: AI behavior

Reverse engineering using `data/scripts/` in the Cossacks 3 installation. All links
the code and the Pascal blocks themselves are collected in the [Sources](#sources) section
at the end of the document.

## TL;DR

- AI player ticks once every **2.4 game seconds**. Each cycle has two phases:
  `progresseconomicai` (build order, mining, upgrades) and `progresswarai`
  (army, attack, sabotage).
- **“Difficulty” is a multiplier for the speed of construction and recruitment**, nothing
  more: easy 30% / normal 50% / hard 75% / very hard 100% /
  impossible 125%. AI **does not receive** starting resources for any
  complexity.
- **Build order rule-based** and nation-dependent. No ML, no random -
  just an if-cascade from the current state (there is a barracks → the second formation
  warehouse; there is aca → explore cen.1 → put ba2; and so on).
- **`aggressor` wave** = 5 units. When they are collected, the AI sends them
  to the nearest target.
- **Diplomacy** static: commands are taken from the lobby, in the process
  AI parties do not make or break alliances.

<a id="исходные-файлы"></a>
## Source files

| Path | Size | Role |
|---|---:|---|
| `lib/ai.script` | 95.6 KB | Auxiliary library: army queries (`_ai_GetArmyForce`, `_ai_GetArmyUnitsCount`), mapping of unit roles (`_ai_FillUnitUpgradeList`), upgrade tables, filling out the list of deposits, `_ai_IsTeamAI`, `_ai_GetCommonNationName` (4 clusters: rus / tur / mis/eur). |
| `units/global.inc/progressai.inc` | 0.8 KB | **Dispatcher.** Each `gc_global_TimeProgressAI` tick calls `ProgressEconomicAI`, then `ProgressWarAI`. |
| `units/global.inc/progresseconomicai.inc` | 226 KB | Economic AI: build order, production goals, resource balance, choice of upgrades. |
| `units/global.inc/progresswarai.inc` | 223 KB | Military AI: army formation, attack/withdrawal decisions, sabotage groups, transport operations. |
| `misc/airegion.aix` | 3.0 KB | AI zone triggers for scenarios. Has nothing to do with the main AI. |

Tick interval: `gc_global_TimeProgressAI = 0.03 × 16 × 5 = 2.4` gaming
seconds [^1]. Each AI player runs a full cycle every 2.4 g-sec.
`lastprogressaitime` is offset by player-id (`id × 0.25 +
gc_global_TimeProgressAI`) so that all AIs do not launch in one tick [^2].

The dispatcher simply sequentially pulls the economic and military
phases [^3].

<a id="уровни-сложности"></a>
## Difficulty levels

The code defines five levels - from `easy` to `impossible` - plus
service value `none = -1` [^4]. `gc_MaxAIDifficultyCount = 4` [^5];
The UI shows four levels (easy / normal / hard / veryhard);
`impossible` is reserved for scripts - e.g.
`initmaphistoricalbattle.inc` puts historical battles on this
level [^6].

Difficulty is stored in `gMap.players[i].aidifficulty` [^7], copied
in `gPlayer[i].difficulty` when starting the batch [^8]. Default value
in the lobby - `easy` [^9]. Full table of 5 levels with multipliers -
[`reports/map/lobby_settings.md`](../../reports/map/lobby_settings.md#difficulty--сложность);
engine behavior - [`game_settings.md`](../world/map/game_settings.md) §4.

<a id="что-меняется-между-уровнями"></a>
### What changes between levels

<a id="1-скорость-постройки-и-найма--главный-чит"></a>
#### 1. The speed of construction and hiring is the main “cheat”

`deltabuildtime` is an increase per tick to the progress of construction and recruitment;
for AI it is multiplied by the difficulty factor [^10]. Effect:

- **easy** — AI builds at **30%** player speed (3.33 times slower);
- **normal** — 50% (2 times slower);
- **hard** — 75%;
- **veryhard** — parity with the player;
- **impossible** - 125% (25% faster) - the only mode where the AI ​​gets a real advantage.

The `aiData.bhumanai` flag (default `False` [^11]) disables
multiplier - AI plays at parity regardless of level.

<a id="2-лимит-апгрейдов-башни"></a>
#### 2. Tower upgrade limit

Maximum tower upgrade level: easy = 2, normal = 3, hard = 4,
veryhard = 5, impossible = 5 [^12].

<a id="3-размер-диверсионных-групп"></a>
#### 3. Size of sabotage groups

`numdiver` depends on the level: normal = 0, hard = 2, veryhard = 4,
impossible = 4 [^13]. Easy does not send sabotages at all. Veryhard and
impossible hold up to four parallel sabotage armies
(`cap = gc_ai_MaxDiverArmies = 2` plus existing ones).

<a id="4-лимит-апгрейдов-шахты"></a>
#### 4. Mine upgrade limit

Easy is limited to level 0, normal - 2/3, higher - up to 7 [^14].

<a id="5-базовые-ворота-через-if-difficulty--easy"></a>
#### 5. Basic gate via `if difficulty > easy`

Easy does not explore: `bricks1`, `fort`, `armor1`, `accurency1`, `artlife`,
`horseswords`. Does not build howitzers and mortars [^15].

<a id="6-дополнительные-проверки-на-hard"></a>
#### 6. Additional checks for hard+

Only `difficulty >= hard` triggers the emergency hiring logic
diplomat-dragoons (mercenaries) with a shortage of gold [^16].

<a id="7-bricks1--только-veryhard-и-impossible"></a>
#### 7. `bricks1` - only veryhard and impossible

See [^17].

<a id="8-поблажка-игроку-на-низких-уровнях"></a>
#### 8. Indulgence for the player at low levels

The player's arrows on difficulty `<= normal` have a weakened check
`standtime`, which makes them less intrusive to manage [^18]. This
the bonus is for the **player**, not the AI.

<a id="что-не-меняется-по-сложности"></a>
### What does NOT change in difficulty

- **Starting resources.** All players receive the same values for
  `resourcestart`: 0 → 1000 each, 1 → 4000, 2 → 5000, 3 → 1,000,000 [^19].
  AI does not receive bonus resources at any level.
- **Permanent “drip” income and income cheats.** Not in scripts
  found. AI extracts resources using standard mines, and challenges
  `_ai_SetResouceBalance` only manage production priorities
  and trade, but do not provide free resources.
- **Game speed.** `gc_settings_gamespeed_*` - global,
  not personal.

## Build order

Eco-AI is **adaptive but rule-based**. Solutions
about the building are not recorded as a fixed array - it is a long
sequence of calls `_ai_TryUnit(plind, cid, gc_ai_unit_<X>,
target_count, false)`, in which the condition usually refers to the current
counter of other buildings (for example, `_ai_GetUnitCount(plind, cid,
gc_ai_unit_ba17) >= 2`).

Macro phases [^20]:

1. Always tries: **Town Hall** (1 → 2 at the beginning), **market**, **mill**.
2. Only Algeria and Turkey: opportunistic **house**, if there is a forge, warehouse, market and 17th century barracks.
3. **Mines** (`gc_ai_unit_minegold`, `_mineiron`, `_minecoal`) - via `_ai_BuildMines` (uses `gc_ai_dist_mines_lvl1 = 30`, `lvl2 = 60`, `expansion = 85` [^21]).
4. **Blacksmith** (1 pc.).
5. **Barracks 17th century. (ba17)**: target 1 → 2 → 3 → 6 / 8 depending on the number of City Centers and the flag of the water map - for example, 8 for most nations and 6 for Russia [^22].
6. Expansion **up to 5 City Centers**, if `centercount >= 2`.
7. **Academy** at `>= 2` ba17 and `>= 2` City centers.
8. **Stable, artillery warehouse, diplomatic center, temple** after the academy.
9. **Barracks 18th century. (ba18)** appears after researching the academy and `gc_ai_upg_century`.
10. **Towers** if you have an academy and active war-AI on `difficulty > easy`: `numTowers = Min(3, peasants div 75)` [^23].

Build order greatly depends on the nation. Each `cid_<nat>` (24 nations:
aus..lit) has its own branch in many places. Three notable
approach: Ukraine (`cid_ukr`) often skips ba17 / officer chain
and bets on massive musk17; Algeria and Turkey (`cid_alg` /
`cid_tur`) lead a parallel thread “archers from the academy”; Russia
(`cid_rus`) lowers the count of barracks to 6 in the “millions” of resources mode.

Build order checkpoints (representative):

- 2 ba17 + 2 City centers → academy [^24];
- 2 ba17 + 4 City centers → resource balance shifts towards gold [^25];
- ba18 ≥ 5 → launch of 3 more ba17 and the sixth City Center [^26];
- pikemanCount ≥ 36 × 4 → switching from pikemen to pikeman + musk [^27];
- pikemanCount ≥ 36 × 7 + `gc_ai_max_guards (120)` → only musk17 [^28].

The balance of resources adapts to the number of peasants: the share of food increases 12 →
21 → 27 → 36 → 45 (× 1.3 if pikemen are not yet upgraded) per
breakpoint'ah 30 / 45 / 85 / 120 peasants [^29]. Russia and Poland
use 16 → 24 → 31 → 40 → 49.

<a id="цели-по-производству"></a>
## Production goals

The entry point is `_ai_RequestUnitsProduction` [^30].

<a id="крестьяне"></a>
### Peasants

Hard cap: **400 peasants in total** (for all controlled nations)
OR **30 per nation**, whichever comes first [^31]. Formula "2"
on Town Hall" is the replenishment speed. `_ai_DecreasePeasants`
reduces count when [^32] is exceeded.

<a id="военные-цели"></a>
### Military purposes

In the block `:2103-2150` and further [^33]:

- `numOfficers = pikemanCount div 36` (minimum 1 if pikemanCount > 28);
- `numReiters = stable_count × 2`;
- `numInf18 = ba18_count × 2`;
- `bar_count` (production target inf17) = `ba17_count × 2`;
- `cannon_count = ClampInt(num_depo × 6, 6, 30)`;
- `howitzer_count = ClampInt(num_depo × 2, 2, 8)`;
- `mortar_count = ClampInt(num_depo × 8, 8, 40)`;
- 18-eternal dragoon and pikeman: depend on the `gc_ai_upg_horse` upgrade and the nation;
- Archerand (alg/sco): `_ai_GetUnitCount < farmused / 3` (on the water card `/5`).

These numbers are the **counts for the production queue** passed
`_ai_TryUnit`, not hard limits. Barracks train until achievement
targets and wake up again on the next AI tick.

`gc_ai_max_guards = 120` [^34] - buffer above the pike threshold, after
which turns on “only musk17”.

<a id="триггеры-агрессии-и-атаки"></a>
## Triggers of aggression and attacks

Constants [^35]:

| Name | Meaning | Meaning |
|---|---:|---|
| `gc_ai_AgressorsCount` | 5 | detachments in the first aggressor wave |
| `gc_ai_MaxDiverArmies` | 2 | maximum sabotage armies at the same time |
| `gc_ai_OfficerWaitTime` | 20 | sec at normal speed waiting for a drummer or officer |
| `gc_ai_GreArmyBattleDist` | 2 | grenadier scan grid distance |
| `gc_ai_ArmyBattleDist` | 4 | normal scan grid distance |
| `gc_ai_BitvaInterval` | 8 | recheck interval in battle |
| `gc_ai_CityDangerDist` | 20 | |
| `gc_ai_MergeArmyCityDist` | 25 | |
| `gc_ai_MergeApproachDist` | 10 | |
| `gc_ai_MinStoreHouseDist` | 9 | |

Pipeline attacks:

- `progresswarai.inc` gathers armies and distributes orders. Transfer
  orders (`gc_ai_armyorder_*` [^36]): `none/makebattle/bitva/
  buildmine/sabotage/aggressor/makewaterbattle/transport/
  attackwall`.
- **First aggressor wave** (`_ai_SendAgressors` [^37]): AI
  sends one starting wave of 5 units as soon as in the pool
  `aiData.agressors` will have enough mobile units.
  Subsequent waves go through `_ai_ArmyMakeBattleLink`.
- **Digression** [^38]: `myForce = _ai_GetArmyForce(pArmy)`. If
  `uCount > 200` or `myForce > 3800`, `myForce := 100000` (interpreted
  as absolute superiority, retreat is not triggered). Otherwise
  multiplied by 8 (heavy bonus) or 2 (light). When `enForce > myForce`
  the army is retreating.
- **Sabotage** (`_ai_ArmyDiversia*`): if the enemy is weaker than my army
  within a radius of 30 - attack; within a radius of 400, we also go on the attack.
- **Wall Attack** (`_ai_ArmyCheckWallAttack`): if the target is a wall, all
  units in `searchRadius` armies switch to attack-wall
  (artillery excluded).
- **Peacetime** (`gbool_peacemode`): set when
  `gMap.settings.additional.peacetime <> default` [^39]. While active
all aggressor and sabotage branches do early-exit [^40].
- **Diplomacy and commands:** `gPlayer[i].team`. AI counts the player
  enemy if `team` is different from or equal to 0 [^41]. `_ai_IsTeamAI`
  determines whether the AI is on the team [^42]. Alliances do not run-time
  formed - commands are set in the lobby and do not change. Scenario
  trigger `gc_trigger_action_player_playerSetAsAlly = 19` exists,
  but the AI from random maps does not use it.

<a id="читы"></a>
## Cheats

| Level | Is the cheat applied? | Magnitude |
|---|---|---|
| Easy | Yes - handicap (slows down AI) | Build and hire at 30% speed |
| Normal | Yes - handicap | By 50% |
| Hard | Yes - low handicap | 75% |
| Very hard | No | Parity (100%) |
| Impossible | Yes - the only “honest” cheat | 125% (faster than the player) |

Source - multiplier `deltabuildtime` [^10]. Trigger condition:
`gPlayer[plind].bai and not aiData.bhumanai`. Flag `bhumanai` [^43]
default `False`; if you set it, the AI plays at parity
regardless of level.

**AI does not receive starting resources** - humans and AI have the same
issuing from `resourcestart` (1000 / 4000 / 5000 / 1,000,000),
confirmed in `initmapgen.inc` [^19].

**Income, overview, movement speed** - no cheats found. AI doesn't see
resources under the fog beyond what his own units discovered:
`_ai_FillOreList` uses `GetGameObjectVisibleByHandle` [^44].

<a id="дипломатия"></a>
## Diplomacy

- Commands are set in the lobby (`gMap.players[i].team`). Initialization
  makes players enemies if their `team` is different or one of
  commands is 0 [^45]. The command `0` means "no command" - all enemies.
- AI vs AI: `_ai_IsEnemiesExists` [^46] goes through all players
  and considers anyone with a different team an enemy. AI players in one
  the team are friends and do not attack each other.
- **There is no dynamic diplomacy.** Neither the logic of forming alliances,
  neither their gap was found in `lib/ai.script`, `progresseconomicai.inc`,
  `progresswarai.inc`. Scenarios can change relationships
  (`scenario.script` + `gc_trigger_action_player_playerSetAsAlly`),
  but in a random map such a mechanism does not exist.
- AI treats all enemies **symmetrically** - `_ai_GetRandomEnemy`
  [^47] Selects a random enemy to hit next. No
  prioritization of the weak, there is no constant “vendetta”.

<a id="открытые-вопросы"></a>
## Open questions

1. **Replenishment speed of `aggressor`-pool.** List
   `gPlayer[plInd].aiData.agressors` is filling somewhere. To
   predict the timing of the first attack on a fresh map, you need to track
   calls `aiData.agressors.Add`.
2. **Activation `bhumanai`.** The flag is in the code, but in scripts it is a setter
   not found. Possibly set from the C++ engine side - for example,
   through the “Fair AI” UI checkbox in the options or through the tournament mode.
   It's worth checking out `gui/options/`.
3. **`fAttackCount` per squad.** TSquad has fields `fAttackCount`,
   `fMoveCount`, `fDelayCount` (TArmy requests them). Where are they
   are they exhibiting? Most likely, in the `unit.inc/onattack*.inc` handlers.
4. **What exactly does `gc_ai_max_guards = 120` mean.** Used as
   buffer above the pike threshold, but the semantic role (number
   defenders at the base?) is unclear.
5. **Logic `centerfound`.** AI does not launch full bootstrap,
   bye `aidata.centerfound = True` [^48]. When does the flag switch?
   Most likely, during the first construction of the City Center.
6. **Speed of decision making in war-AI.** `progresswarai` ticks once
   at 2.4 g-sec per player, but each army has its own
   `fStateTime`-cooldowns. To know the delay of a specific action,
   you need to pass `progresswarai.inc:4100-4220`.
7. **The influence of difficulty on the frequency of attacks.** Triggers `aggressor` and
   sabotage use `gc_ai_AgressorsCount = 5` regardless
   from the level (only the number of parallel sabotages is scaled).
   That is, easy and impossible AI should send the first attack
   at the same time - only the speed of construction differs.
   It's worth testing empirically.
8. **`gc_ai_AgressorsCount = 5` vs `gc_ai_max_guards = 120`.**
   A very small first wave for an army of 100 pikemen - only 5
   detachments, the rest are at home. Need to check if they scale
   subsequent waves.
9. **Ranges `gc_ai_dist_mines_lvl1 = 30` / `lvl2 = 60` /
   `expansion = 85`.** It's in the tiles. It is worth verifying which
   AI level is used on Tiny versus Normal map.
10. **`bprogressWar` and `bprogressUpgrades`** in `aidata` - when
    switch to `True`? Most likely by timer, but traces
    not yet.

---

<a id="источники"></a>
## Sources

All links are relative to `data/scripts/` in the Cossacks 3 installation.

[^1]: `gc_global_TimeProgressAI = 0.03 × 16 × 5 = 2.4` - `dmscript.global:1486`.

[^2]: Shift `lastprogressaitime` by player-id — `player.script:140`:
    ```pascal
    lastprogressaitime := id * 0.25 + gc_global_TimeProgressAI;
    ```
[^3]: Dispatcher - `units/global.inc/progressai.inc`:
    ```pascal
    ExecuteState('ProgressEconomicAI');
    ExecuteState('ProgressWarAI');
    ```
[^4]: Listing difficulty levels - `dmscript.global:781-786`:
    ```pascal
    gc_player_difficulty_none       = -1;
    gc_player_difficulty_easy       =  0;
    gc_player_difficulty_normal     =  1;
    gc_player_difficulty_hard       =  2;
    gc_player_difficulty_veryhard   =  3;
    gc_player_difficulty_impossible =  4;
    ```
[^5]: `gc_MaxAIDifficultyCount = 4` - `dmscript.global:235`.

[^6]: Impossible for historical battles - `initmaphistoricalbattle.inc:121`.

[^7]: The `aidifficulty` field in the card record is `classes.script:105`.

[^8]: Copying to `gPlayer[i].difficulty` at startup - `initmapgen.inc:132`.

[^9]: Defaulted `easy` in the lobby - `map.script:244`, `player.script:118`.

[^10]: `deltabuildtime` multiplier on AI difficulty - `building.inc/doprogressorders.inc:222-230`:
    ```pascal
    if (gPlayer[plind].bai) and (not gPlayer[plInd].aiData.bhumanai) then
    case gPlayer[plind].difficulty of
       gc_player_difficulty_easy       : deltabuildtime *= 0.30;
       gc_player_difficulty_normal     : deltabuildtime *= 0.50;
       gc_player_difficulty_hard       : deltabuildtime *= 0.75;
       gc_player_difficulty_veryhard   : deltabuildtime *= 1.00;
       gc_player_difficulty_impossible : deltabuildtime *= 1.25;
    end;
    ```
[^11]: Default `aiData.bhumanai = False` - `classes.script:2688`.

[^12]: The tower upgrade limit is `progresseconomicai.inc:3653-3658`.

[^13]: Size of sabotage groups - `progresseconomicai.inc:2322-2326`:
    ```pascal
    case difficulty of
       gc_player_difficulty_normal     : numdiver := 0;
       gc_player_difficulty_hard       : numdiver := 2;
       gc_player_difficulty_veryhard   : numdiver := 4;
       gc_player_difficulty_impossible : numdiver := 4;
    end;
    ```
[^14]: The mine upgrade limit is `progresseconomicai.inc:2202-2212` and `~2396-2410`.

[^15]: Banning howitzers and mortars on easy - `progresseconomicai.inc:2349-2353`.

[^16]: Emergency hiring of mercenaries at `difficulty >= hard` - `progresseconomicai.inc:2306`.

[^17]: `bricks1` - only veryhard and impossible - `progresseconomicai.inc:2452`.

[^18]: Indulgence for the player's shooters at `<= normal` - `unit.script:7367`.

[^19]: The distribution of starting resources is the same for all players - `initmapgen.inc:166-189`.

[^20]: Macro phases build order - `progresseconomicai.inc:2700-2830`.

[^21]: Mine ranges - `dmscript.global:503-506` (`gc_ai_dist_mines_lvl1 = 30`, `lvl2 = 60`, `expansion = 85`).

[^22]: Target ba17 - `progresseconomicai.inc:2771`:
    ```pascal
    _ai_TryUnit(plind, cid, gc_ai_unit_ba17, 8, False)
    // 6 for Russia
    ```

[^23]: Towers — `progresseconomicai.inc:2926-2929`:
    ```pascal
    numTowers := Min(3, peasants div 75);
    ```
[^24]: 2 ba17 + 2 City centers → academy - `progresseconomicai.inc:2796`.

[^25]: 2 ba17 + 4 City centers → balance towards gold - `progresseconomicai.inc:2036-2039`.

[^26]: ba18 ≥ 5 → 3 more ba17 and the sixth Town Hall - `progresseconomicai.inc:2789-2793`.

[^27]: pikemanCount ≥ 36 × 4 → pikeman + musk - `progresseconomicai.inc:2134`.

[^28]: pikemanCount ≥ 36 × 7 + `gc_ai_max_guards` → musk17 only - `progresseconomicai.inc:2152-2158`.

[^29]: Food balance by number of peasants - `progresseconomicai.inc:1999-2031`.

[^30]: `_ai_RequestUnitsProduction` - `progresseconomicai.inc:2085+`.

[^31]: Cap of peasants - `progresseconomicai.inc:2088`:
    ```pascal
    var numpeasants : Integer = _ai_GetUnitCount(plind, cid, gc_ai_unit_center) * 2;
    if (peasants_total < 400) or (peasants_this_nation < 30) then
       if food < 700 then queue numpeasants
       else queue 1
    ```
[^32]: `_ai_DecreasePeasants` - `progresseconomicai.inc:3856`.

[^33]: Targets for military units - `progresseconomicai.inc:2103-2150` (and further `:2347`, `:2351`, `:2352` for guns, howitzers and mortars).

[^34]: `gc_ai_max_guards = 120` - `dmscript.global:500`.

[^35]: Aggression and attack constants - `dmscript.global:474-481`.

[^36]: Enumeration `gc_ai_armyorder_*` - `dmscript.global:430-438`.

[^37]: First aggressor wave - `progresswarai.inc:3560-3568` (`_ai_SendAgressors`):
    ```pascal
    if (not gbool_peacemode) and (agressorsSent = 0) and
       (agressors.GetCount >= gc_ai_AgressorsCount) then
    begin
       pArmy := _ai_CreateAgressorArmy(plInd, 5, agressors);
       _ai_ArmyMakeAgressorBattle(pArmy);
    end;
    ```
[^38]: Retreat logic - `progresswarai.inc:2398-2407`:
    ```pascal
    myForce := _ai_GetArmyForce(pArmy);
    if (uCount > 200) or (myForce > 3800) then
       myForce := 100000;
    // otherwise myForce *= 8 (heavy) or *= 2 (light)
    if (enForce > myForce) then ...retreat...
    ```
[^39]: Installation `gbool_peacemode` - `dogenerate.inc:2060-2064`.

[^40]: Early-exit aggression and sabotage during peacetime - `progresswarai.inc:2787` and `:3562`.

[^41]: Hostility by `team` - `initmapgen.inc:160`.

[^42]: `_ai_IsTeamAI` - `ai.script:527`.

[^43]: Field `bhumanai` - `classes.script:2611`.

[^44]: AI resource visibility is `ai.script:228` (`_ai_FillOreList` uses `GetGameObjectVisibleByHandle`).

[^45]: Initializing relationships by command - `initmapgen.inc:158-163`:
    ```pascal
    if (myteam <> histeam) or (histeam = 0) or (myteam = 0) then
       AddPlayerEnemyPlayerByHandle(...)
    else
       AddPlayerFriendPlayerByHandle(...);
    ```
[^46]: `_ai_IsEnemiesExists` - `ai.script:7-19`.

[^47]: `_ai_GetRandomEnemy` - `progresseconomicai.inc:67-94`.

[^48]: Condition `aidata.centerfound = True` - `ai.script:451`.
