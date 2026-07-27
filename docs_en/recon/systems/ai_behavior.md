<a id="recon-поведение-ии"></a>
<a id="как-играет-компьютер"></a>
# How the Computer Player Works

[← How the game works](../README.md)

This analysis is based on `data/scripts/` from an installed copy of
Cossacks 3. Source references and Pascal excerpts are collected under
[Sources](#sources).

<a id="кратко"></a>
## TL;DR

- An AI player updates once every **2.4 game seconds**. Each cycle has an
  economic phase (`progresseconomicai`: build order, gathering, upgrades)
  and a military phase (`progresswarai`: armies, attacks, and raids).
- **Difficulty mainly multiplies construction and recruitment speed:**
  `easy` 30%, `normal` 50%, `hard` 75%, `veryhard` 100%, and
  `impossible` 125%. The AI receives **no extra starting resources**.
- **The build order is rule-based and nation-specific.** It uses neither
  machine learning nor a random plan; a sequence of conditions examines
  the current game state.
- **The first offensive wave** (`aggressor`) consists of five squads.
  Once assembled, the AI sends them
  to the nearest target.
- **Diplomacy is static:** teams come from the lobby, and the AI neither
  forms nor breaks alliances during a match.

<a id="исходные-файлы"></a>
## Source files

| Path | Size | Role |
|---|---:|---|
| `lib/ai.script` | 95.6 KB | Helper library: army queries (`_ai_GetArmyForce`, `_ai_GetArmyUnitsCount`), unit-role mappings (`_ai_FillUnitUpgradeList`), upgrade tables, deposit discovery, `_ai_IsTeamAI`, and `_ai_GetCommonNationName` (four groups: `rus`, `tur`, `mis`, `eur`). |
| `units/global.inc/progressai.inc` | 0.8 KB | **Dispatcher.** Each `gc_global_TimeProgressAI` tick calls `ProgressEconomicAI`, then `ProgressWarAI`. |
| `units/global.inc/progresseconomicai.inc` | 226 KB | Economic AI: build order, production goals, resource balance, choice of upgrades. |
| `units/global.inc/progresswarai.inc` | 223 KB | Military AI: army formation, attack/withdrawal decisions, sabotage groups, transport operations. |
| `misc/airegion.aix` | 3.0 KB | AI zone triggers for scenarios. Has nothing to do with the main AI. |

The update interval is
`gc_global_TimeProgressAI = 0.03 × 16 × 5 = 2.4` game seconds [^1].
`lastprogressaitime` is offset by player number
(`id × 0.25 + gc_global_TimeProgressAI`) so that all AI players do not
update on the same tick [^2].

The dispatcher runs the economic and military phases in sequence [^3].

<a id="уровни-сложности"></a>
## Difficulty levels

The code defines five levels from `easy` to `impossible`, plus the sentinel
`none = -1` [^4]. `gc_MaxAIDifficultyCount = 4` [^5]. The interface shows
four levels (`easy`, `normal`, `hard`, and `veryhard`); `impossible` is
reserved for scenarios—for example,
`initmaphistoricalbattle.inc` puts historical battles on this
level [^6].

Difficulty is stored in `gMap.players[i].aidifficulty` [^7], copied
to `gPlayer[i].difficulty` when the match starts [^8]. The lobby default
is `easy` [^9]. The full table of multipliers is in
[lobby settings](../../reports/map/lobby_settings.md#difficulty--сложность);
and engine behavior is covered by
[match settings](../world/map/game_settings.md) §4.

<a id="что-меняется-между-уровнями"></a>
### What changes between levels

<a id="1-скорость-постройки-и-найма--главный-чит"></a>
#### 1. Construction and recruitment speed

`deltabuildtime` is the construction or recruitment progress added each
tick. For the AI, it is multiplied by the difficulty factor [^10]:

- **easy** — AI builds at **30%** player speed (3.33 times slower);
- **normal** — 50% (2 times slower);
- **hard** — 75%;
- **veryhard** — parity with the player;
- **impossible** — 125% (25% faster), the only level with an actual advantage.

The `aiData.bhumanai` flag (default `False` [^11]) disables
multiplier, making the AI play at full speed regardless of level.

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
<a id="5-ограничения-лёгкого-уровня"></a>
#### 5. Restrictions on Easy

Easy does not research `bricks1`, `fort`, `armor1`, `accurency1`,
`artlife`, or `horseswords`, and does not build howitzers or mortars [^15].

<a id="6-дополнительные-проверки-на-hard"></a>
<a id="6-дополнительные-проверки-на-сложном-уровне-и-выше"></a>
#### 6. Additional checks on Hard and above

Only `difficulty >= hard` enables emergency recruitment of mercenary
Dragoons when gold is scarce [^16].

<a id="7-bricks1--только-veryhard-и-impossible"></a>
<a id="7-bricks1--только-на-очень-сложном-и-невозможном-уровнях"></a>
#### 7. `bricks1` - only veryhard and impossible

See [^17].

<a id="8-поблажка-игроку-на-низких-уровнях"></a>
#### 8. Assistance for the player at low levels

The player's ranged units have a relaxed `standtime` check at
`difficulty <= normal`, making them easier to control [^18]. This helps
the **player**, not the AI.

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

<a id="порядок-строительства"></a>
## Build order

The economic AI is **adaptive but rule-based**. Its build order is not a
fixed array; it is a long sequence of calls such as
`_ai_TryUnit(plind, cid, gc_ai_unit_<X>, target_count, false)`, whose
conditions usually inspect the current counts of other buildings—for
example, `_ai_GetUnitCount(plind, cid, gc_ai_unit_ba17) >= 2`.

Macro phases [^20]:

1. Always attempts a **Town Hall** (from one to two early), **Market**, and **Mill**.
2. Algeria and Turkey may add a **House** when they already have a Blacksmith, Storehouse, Market, and 17th-century Barracks.
3. **Mines** (`gc_ai_unit_minegold`, `_mineiron`, `_minecoal`) - via `_ai_BuildMines` (uses `gc_ai_dist_mines_lvl1 = 30`, `lvl2 = 60`, `expansion = 85` [^21]).
4. One **Blacksmith**.
5. **17th-century Barracks** (`ba17`): target counts of 1 → 2 → 3 →
   6 or 8 depending on Town Hall count and whether the map is naval.
   Most nations aim for eight; Russia aims for six [^22].
6. Expansion to **five Town Halls** once `centercount >= 2`.
7. An **Academy** after at least two 17th-century Barracks and two Town Halls.
8. A **Stable**, **Artillery Depot**, **Diplomatic Center**, and **Cathedral** after the Academy.
9. **18th-century Barracks** (`ba18`) after the Academy's century upgrade (`gc_ai_upg_century`).
10. Up to three **Towers** after an Academy, once military AI is active
    above Easy: `numTowers = Min(3, peasants div 75)` [^23].

Build order varies substantially by nation. Each of the 24 nation codes
(`cid_<nat>`, from `aus` through `lit`) has its own branches. Ukraine
(`cid_ukr`) often skips the 17th-century Barracks (`ba17`) and Officer
chain in favor of mass 17th-century Musketeers (`musk17`). Algeria and
Turkey (`cid_alg`, `cid_tur`) recruit Archers through the Academy. Russia
(`cid_rus`) limits itself to six Barracks with “millions” of starting
resources.

Build order checkpoints (representative):

- two 17th-century Barracks (`ba17`) and two Town Halls → Academy [^24];
- two 17th-century Barracks and four Town Halls → resource balance shifts toward gold [^25];
- at least five 18th-century Barracks (`ba18`) → three more
  17th-century Barracks and a sixth Town Hall [^26];
- `pikemanCount >= 36 × 4` → recruit both Pikemen and Musketeers [^27];
- `pikemanCount >= 36 × 7 + gc_ai_max_guards (120)` → recruit only
  17th-century Musketeers (`musk17`) [^28].

The balance of resources adapts to the number of peasants: the share of food increases 12 →
21 → 27 → 36 → 45 (× 1.3 if pikemen are not yet upgraded) per
at thresholds of 30 / 45 / 85 / 120 Peasants [^29]. Russia and Poland
use 16 → 24 → 31 → 40 → 49.

<a id="цели-по-производству"></a>
## Production goals

The entry point is `_ai_RequestUnitsProduction` [^30].

<a id="крестьяне"></a>
### Peasants

Hard cap: **400 Peasants in total** across all controlled nations or
**30 per nation**, whichever comes first [^31]. “Two per Town Hall” is
the replenishment rate. `_ai_DecreasePeasants` lowers the target once the
cap is exceeded [^32].

<a id="военные-цели"></a>
### Military targets

In the block `:2103-2150` and further [^33]:

- `numOfficers = pikemanCount div 36` (minimum one when `pikemanCount > 28`);
- `numReiters = stable_count × 2`;
- `numInf18 = ba18_count × 2`;
- `bar_count` (17th-century infantry target, `inf17`) = `ba17_count × 2`;
- `cannon_count = ClampInt(num_depo × 6, 6, 30)`;
- `howitzer_count = ClampInt(num_depo × 2, 2, 8)`;
- `mortar_count = ClampInt(num_depo × 8, 8, 40)`;
- 18th-century Dragoons and Pikemen depend on the nation and
  `gc_ai_upg_horse`;
- Archers for Algeria and Scotland (`alg`, `sco`) use
  `_ai_GetUnitCount < farmused / 3`, or `/5` on a naval map.

These are **production-queue targets** passed to `_ai_TryUnit`, not hard
limits. Barracks train until a target is reached and resume on later AI
updates when the count falls.

`gc_ai_max_guards = 120` [^34] - buffer above the pike threshold, after
which switches production to 17th-century Musketeers only.

<a id="триггеры-агрессии-и-атаки"></a>
## When the AI attacks

Constants [^35]:

| Name | Value | Meaning |
|---|---:|---|
| `gc_ai_AgressorsCount` | 5 | squads in the first offensive wave |
| `gc_ai_MaxDiverArmies` | 2 | maximum sabotage armies at the same time |
| `gc_ai_OfficerWaitTime` | 20 | sec at normal speed waiting for a drummer or officer |
| `gc_ai_GreArmyBattleDist` | 2 | Grenadier search distance in grid cells |
| `gc_ai_ArmyBattleDist` | 4 | normal search distance in grid cells |
| `gc_ai_BitvaInterval` | 8 | recheck interval in battle |
| `gc_ai_CityDangerDist` | 20 | |
| `gc_ai_MergeArmyCityDist` | 25 | |
| `gc_ai_MergeApproachDist` | 10 | |
| `gc_ai_MinStoreHouseDist` | 9 | |

Attack sequence:

- `progresswarai.inc` gathers armies and distributes orders. The
  `gc_ai_armyorder_*` enumeration [^36] contains `none`, `makebattle`,
  `bitva`, `buildmine`, `sabotage`, `aggressor`, `makewaterbattle`,
  `transport`, and `attackwall`.
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
