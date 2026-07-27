<a id="recon-поведение-ии"></a>
<a id="как-играет-компьютер"></a>
# How the Computer Player Works

[← How the game works](../README.md)

This article explains how the computer player develops its economy, recruits
an army, and decides when to attack. Internal names and Pascal excerpts are
collected in the [technical source map](#technical-source-map) and
[Sources](#sources).

<a id="кратко"></a>
## Key points

- The computer revisits economic and military decisions once every
  **2.4 game seconds**.
- **Difficulty primarily changes construction and recruitment speed:**
  from 30% of player speed on Easy to 100% on Very Hard. The scenario-only
  Impossible level uses 125%. The AI receives **no extra starting resources**.
- **The build order is rule-based and nation-specific.** It uses neither
  machine learning nor a random plan; a sequence of conditions examines
  the current game state.
- **The first offensive wave** consists of five squads. Once assembled, the
  computer sends them to the nearest target.
- **Diplomacy is static:** teams come from the lobby, and the AI neither
  forms nor breaks alliances during a match.

<a id="уровни-сложности"></a>
## Difficulty levels

The interface shows four levels: Easy, Normal, Hard, and Very Hard. A fifth,
Impossible level is reserved for scenarios, including Historical Battles
[^4] [^5] [^6]. The full table of multipliers is in
[lobby settings](../../reports/map/lobby_settings.md#difficulty--сложность);
and engine behavior is covered by
[match settings](../world/map/game_settings.md) §4.

<a id="что-меняется-между-уровнями"></a>
### What changes between levels

<a id="1-скорость-постройки-и-найма--главный-чит"></a>
#### 1. Construction and recruitment speed

The difficulty factor multiplies construction and recruitment progress [^10]:

- **Easy** — **30%** of player speed (3.33 times slower);
- **Normal** — 50% (twice as slow);
- **Hard** — 75%;
- **Very Hard** — equal to the player;
- **Impossible** — 125%, the only level with an advantage.

<a id="2-лимит-апгрейдов-башни"></a>
#### 2. Tower upgrade limit

Maximum tower upgrade level: Easy = 2, Normal = 3, Hard = 4,
Very Hard = 5, Impossible = 5 [^12].

<a id="3-размер-диверсионных-групп"></a>
#### 3. Size of sabotage groups

Normal prepares no sabotage groups, Hard prepares two, and Very Hard and
Impossible prepare four [^13]. Easy does not send sabotage groups either.
Very Hard and Impossible can maintain up to four parallel sabotage armies.

<a id="4-лимит-апгрейдов-шахты"></a>
#### 4. Mine upgrade limit

Easy is limited to level 0, Normal to level 2 or 3, and higher
difficulties to level 7 [^14].

<a id="5-базовые-ворота-через-if-difficulty--easy"></a>
<a id="5-ограничения-лёгкого-уровня"></a>
#### 5. Restrictions on Easy

Easy skips several economic and military upgrades and does not build
Howitzers or Mortars [^15]. The exact internal codes are listed in the
technical section.

<a id="6-дополнительные-проверки-на-hard"></a>
<a id="6-дополнительные-проверки-на-сложном-уровне-и-выше"></a>
#### 6. Additional checks on Hard and above

From Hard upward, the computer can recruit emergency 18th-century Dragoons
from the Diplomatic Center when gold is scarce [^16].

<a id="7-bricks1--только-veryhard-и-impossible"></a>
<a id="7-bricks1--только-на-очень-сложном-и-невозможном-уровнях"></a>
<a id="7-дополнительное-экономическое-улучшение"></a>
#### 7. Additional economic upgrade

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
- **Permanent “drip” income and income cheats.** None were found in the
  scripts. The AI gathers resources through normal mines. Calls to
  `_ai_SetResouceBalance` only adjust production and trade priorities;
  they do not grant free resources.
- **Game speed.** The `gc_settings_gamespeed_*` value is global rather
  than player-specific.

<a id="порядок-строительства"></a>
## Build order

The economic AI is **adaptive but rule-based**. Its build order is not a
fixed array; it is a long sequence of calls such as
`_ai_TryUnit(plind, cid, gc_ai_unit_<X>, target_count, false)`, whose
conditions usually inspect the current counts of other buildings—for
example, `_ai_GetUnitCount(plind, cid, gc_ai_unit_ba17) >= 2`.

The main phases are [^20]:

1. Always attempts a **Town Hall** (from one to two early), **Market**, and **Mill**.
2. Algeria and Turkey may add **Housing** when they already have a
   Blacksmith, Storehouse, Market, and **Barracks, 17th century**.
3. **Mines** (`gc_ai_unit_minegold`, `_mineiron`, `_minecoal`) through
   `_ai_BuildMines`, using the distance thresholds
   `gc_ai_dist_mines_lvl1 = 30`, `lvl2 = 60`, and `expansion = 85` [^21].
4. One **Blacksmith**.
5. **Barracks, 17th century** (`ba17`): target counts of 1 → 2 → 3 →
   6 or 8 depending on Town Hall count and whether the map is naval.
   Most nations aim for eight; Russia aims for six [^22].
6. Expansion to **five Town Halls** once `centercount >= 2`.
7. An **Academy** after at least two **Barracks, 17th century** and two
   Town Halls.
8. A **Stable**, **Artillery Depot**, **Diplomatic Center**, and **Cathedral** after the Academy.
9. **Barracks, 18th century** (`ba18`) after the Academy's century
   upgrade (`gc_ai_upg_century`).
10. Up to three **Towers** after an Academy, once military AI is active
    above Easy: `numTowers = Min(3, peasants div 75)` [^23].

Build order varies substantially by nation. Each of the 24 nation codes
(`cid_<nat>`, from `aus` through `lit`) has its own branches. Ukraine
(`cid_ukr`) often skips the **Barracks, 17th century** (`ba17`) and
**Officer, 17th century** chain in favor of mass **Musketeers,
17th century** (`musk17`). Algeria and
Turkey (`cid_alg`, `cid_tur`) recruit Archers through the Academy. Russia
(`cid_rus`) limits itself to six Barracks with “millions” of starting
resources.

Build order checkpoints (representative):

- two **Barracks, 17th century** (`ba17`) and two Town Halls → Academy [^24];
- two **Barracks, 17th century** and four Town Halls → resource balance
  shifts toward gold [^25];
- at least five **Barracks, 18th century** (`ba18`) → three more
  Barracks, 17th century and a sixth Town Hall [^26];
- `pikemanCount >= 36 × 4` → recruit both **Pikemen, 17th century** and
  **Musketeers, 17th century** [^27];
- `pikemanCount >= 36 × 7 + gc_ai_max_guards (120)` → recruit only
  **Musketeers, 17th century** (`musk17`) [^28].

Resource priorities adapt to the Peasant count. The food weight rises
through 12 → 21 → 27 → 36 → 45 at thresholds of 30, 45, 85, and
120 Peasants, with a ×1.3 multiplier while Pikemen remain unupgraded [^29].
Russia and Poland instead use 16 → 24 → 31 → 40 → 49.

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

`gc_ai_max_guards = 120` [^34] is a buffer above the **Pikeman,
17th century** count threshold. Once that threshold is exceeded,
production switches to **Musketeers, 17th century** only.

<a id="триггеры-агрессии-и-атаки"></a>
## When the AI attacks

Constants [^35]:

| Name | Value | Meaning |
|---|---:|---|
| `gc_ai_AgressorsCount` | 5 | squads in the first offensive wave |
| `gc_ai_MaxDiverArmies` | 2 | maximum sabotage armies at the same time |
| `gc_ai_OfficerWaitTime` | 20 | seconds to wait for a Drummer or Officer at Normal speed |
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
- **First offensive wave** (`_ai_SendAgressors` [^37]): the AI sends
  five squads as soon as `aiData.agressors` contains enough mobile units.
  Subsequent waves go through `_ai_ArmyMakeBattleLink`.
- **Retreat** [^38]: `myForce = _ai_GetArmyForce(pArmy)`. If
  `uCount > 200` or `myForce > 3800`, `myForce := 100000` (interpreted
  as overwhelming superiority, so retreat is suppressed). Otherwise,
  the value is multiplied by eight for the heavy bonus or two for the
  light bonus. The army retreats when `enForce > myForce`.
- **Raid** (`_ai_ArmyDiversia*`): the army attacks when the enemy force
  within radius 30 is weaker; it also advances on a target within radius 400.
- **Wall attack** (`_ai_ArmyCheckWallAttack`): if the target is a wall,
  every non-artillery squad within the army's `searchRadius` switches to
  the wall-attack order
  (artillery excluded).
- **Peacetime** (`gbool_peacemode`): set when
  `gMap.settings.additional.peacetime <> default` [^39]. While active
  all offensive and raid branches exit immediately [^40].
- **Diplomacy and teams:** the AI considers another player an enemy when
  `gPlayer[i].team` differs or either value is zero [^41].
  `_ai_IsTeamAI` checks whether a team contains an AI player [^42].
  Alliances are not formed during a normal match: teams are set in the
  lobby and remain fixed. The scenario action
  `gc_trigger_action_player_playerSetAsAlly = 19` exists, but random-map
  AI does not use it.

<a id="читы"></a>
## Cheats

| Level | Is the cheat applied? | Magnitude |
|---|---|---|
| Easy | Yes — handicap (slows the AI) | Construction and recruitment at 30% speed |
| Normal | Yes — handicap | 50% speed |
| Hard | Yes — mild handicap | 75% speed |
| Very hard | No | Parity (100%) |
| Impossible | Yes — the only actual advantage | 125% (faster than the player) |

The source is the `deltabuildtime` multiplier [^10], applied when
`gPlayer[plind].bai and not aiData.bhumanai`. `bhumanai` defaults to
`False` [^43]; setting it makes construction and recruitment run at full
speed regardless of difficulty.

**AI receives no extra starting resources.** Humans and AI receive the
same `resourcestart` amount (1,000 / 4,000 / 5,000 / 1,000,000),
confirmed in `initmapgen.inc` [^19].

**Income, vision, and movement speed:** no advantages were found. The AI
cannot see resources under fog of war until its own units discover them:
`_ai_FillOreList` uses `GetGameObjectVisibleByHandle` [^44].

<a id="дипломатия"></a>
## Diplomacy

- Teams are set in the lobby (`gMap.players[i].team`). Initialization
  makes players enemies when their team values differ or either value is
  zero [^45]. Team `0` means “no team,” so everyone is an enemy.
- AI versus AI: `_ai_IsEnemiesExists` [^46] scans all players
  and treats anyone on a different team as an enemy. AI players on the
  same team do not attack one another.
- **There is no dynamic diplomacy.** No alliance-formation or
  alliance-breaking logic was found in `lib/ai.script`, `progresseconomicai.inc`,
  `progresswarai.inc`. Scenarios can change relationships
  (`scenario.script` + `gc_trigger_action_player_playerSetAsAlly`),
  but random maps have no equivalent mechanism.
- AI treats all enemies **symmetrically** - `_ai_GetRandomEnemy`
  [^47] selects a random enemy for the next strike. It does not prioritize
  weaker opponents or maintain a persistent “vendetta.”

<a id="открытые-вопросы"></a>
## Open questions

1. **How quickly the `aggressor` pool fills.**
   `gPlayer[plInd].aiData.agressors` is populated somewhere else in the
   code. Predicting the first attack requires tracing
   `aiData.agressors.Add`.
2. **How `bhumanai` is activated.** No script setter was found. The C++
   engine may set it through an option or tournament mode; `gui/options/`
   is the next place to inspect.
3. **Per-squad action counters.** `TSquad` contains `fAttackCount`,
   `fMoveCount`, and `fDelayCount`, which `TArmy` reads. Their writers are
   probably in `unit.inc/onattack*.inc`, but have not been traced.
4. **What exactly does `gc_ai_max_guards = 120` mean.** Used as
   a buffer above the Pikeman threshold, but its intended meaning—perhaps
   the number of base defenders—is unclear.
5. **The `centerfound` gate.** Full development does not begin until
   `aidata.centerfound = True` [^48]. The flag is probably set when the
   first Town Hall is built, but this has not been traced.
6. **Military decision latency.** `progresswarai` runs once every 2.4
   game seconds per player, but each army also has `fStateTime` cooldowns.
   Exact action delays require reviewing `progresswarai.inc:4100-4220`.
7. **Whether difficulty affects attack frequency.** `aggressor` and
   `sabotage` both use `gc_ai_AgressorsCount = 5` at every difficulty;
   only the number of parallel raids scales. Easy and Impossible should
   therefore launch their first attack at the same army threshold, with
   construction speed accounting for the timing difference.
8. **`gc_ai_AgressorsCount = 5` vs `gc_ai_max_guards = 120`.**
   Five squads is a very small first wave for an army of 100 **Pikemen,
   17th century**.
   Whether later waves scale up remains to be checked.
9. **Ranges `gc_ai_dist_mines_lvl1 = 30` / `lvl2 = 60` /
   `expansion = 85`.** These appear to be distances in cells. Which tier is
   used on Tiny and Normal maps still needs verification.
10. **When `bprogressWar` and `bprogressUpgrades` become `True`.**
    These `aidata` fields are probably timer-controlled, but their writers
    have not been traced.

---

<a id="исходные-файлы"></a>
<a id="техническая-карта-исходных-файлов"></a>
## Technical source map

The full cycle runs every 2.4 game seconds:
`gc_global_TimeProgressAI = 0.03 × 16 × 5` [^1]. The next update is offset
by `id × 0.25`, preventing all computer players from deciding on the same
tick [^2]. The dispatcher then runs the economic and military phases in
sequence [^3].

The internal levels are `easy`, `normal`, `hard`, `veryhard`, and
`impossible`; no AI is represented by `none = -1`. The choice is stored in
`gMap.players[i].aidifficulty` and copied to `gPlayer[i].difficulty`
[^7] [^8] [^9]. The multiplier applies to `deltabuildtime`;
`aiData.bhumanai` disables it [^10] [^11].

Easy skips `bricks1`, `fort`, `armor1`, `accurency1`, `artlife`, and
`horseswords` [^15]. A separate `bricks1` check enables it only on Very
Hard and Impossible [^17]. Sabotage-group size is stored in `numdiver`, and
the cap is related to `gc_ai_MaxDiverArmies` [^13].

| Path | Size | Role |
|---|---:|---|
| `lib/ai.script` | 95.6 KB | Helper library: army queries (`_ai_GetArmyForce`, `_ai_GetArmyUnitsCount`), unit-role mappings (`_ai_FillUnitUpgradeList`), upgrade tables, deposit discovery, `_ai_IsTeamAI`, and `_ai_GetCommonNationName` (four groups: `rus`, `tur`, `mis`, `eur`). |
| `units/global.inc/progressai.inc` | 0.8 KB | **Dispatcher.** Each `gc_global_TimeProgressAI` tick calls `ProgressEconomicAI`, then `ProgressWarAI`. |
| `units/global.inc/progresseconomicai.inc` | 226 KB | Economic AI: build order, production goals, resource balance, choice of upgrades. |
| `units/global.inc/progresswarai.inc` | 223 KB | Military AI: army formation, attack/withdrawal decisions, sabotage groups, transport operations. |
| `misc/airegion.aix` | 3.0 KB | AI zone triggers for scenarios. Has nothing to do with the main AI. |

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

[^7]: The `aidifficulty` field in the map-player record —
    `classes.script:105`.

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

[^15]: The Easy difficulty disables Howitzers and Mortars —
    `progresseconomicai.inc:2349-2353`.

[^16]: Emergency hiring of mercenaries at `difficulty >= hard` - `progresseconomicai.inc:2306`.

[^17]: `bricks1` is restricted to Very Hard and Impossible —
    `progresseconomicai.inc:2452`.

[^18]: Relaxed ranged-unit control for the player at `<= normal` —
    `unit.script:7367`.

[^19]: The distribution of starting resources is the same for all players - `initmapgen.inc:166-189`.

[^20]: Main build-order phases — `progresseconomicai.inc:2700-2830`.

[^21]: Mine ranges - `dmscript.global:503-506` (`gc_ai_dist_mines_lvl1 = 30`, `lvl2 = 60`, `expansion = 85`).

[^22]: Target number of **Barracks, 17th century** (`ba17`) —
    `progresseconomicai.inc:2771`:
    ```pascal
    _ai_TryUnit(plind, cid, gc_ai_unit_ba17, 8, False)
    // 6 for Russia
    ```

[^23]: Towers — `progresseconomicai.inc:2926-2929`:
    ```pascal
    numTowers := Min(3, peasants div 75);
    ```
[^24]: Two **Barracks, 17th century** (`ba17`) and two Town Halls unlock the
    Academy — `progresseconomicai.inc:2796`.

[^25]: Two **Barracks, 17th century** and four Town Halls shift resource
    priorities toward gold — `progresseconomicai.inc:2036-2039`.

[^26]: At least five **Barracks, 18th century** (`ba18`) lead to three more
    **Barracks, 17th century** and a sixth Town Hall —
    `progresseconomicai.inc:2789-2793`.

[^27]: `pikemanCount ≥ 36 × 4` enables both **Pikemen, 17th century** and
    **Musketeers, 17th century** —
    `progresseconomicai.inc:2134`.

[^28]: `pikemanCount ≥ 36 × 7 + gc_ai_max_guards` switches production
    to **Musketeers, 17th century** (`musk17`) only —
    `progresseconomicai.inc:2152-2158`.

[^29]: Food balance by number of peasants - `progresseconomicai.inc:1999-2031`.

[^30]: `_ai_RequestUnitsProduction` - `progresseconomicai.inc:2085+`.

[^31]: Peasant cap — `progresseconomicai.inc:2088`:
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
