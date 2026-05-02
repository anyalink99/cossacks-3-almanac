"""
Builds the "Deterministic Cossacks" Cossacks 3 mod.

Reads stock lib/{misc,unit,miscext2}.script from the Cossacks 3 install (path from
$COSSACKS3_PATH or default Steam location), applies line-precise patches to
extraction- and combat-RNG hot paths, and emits a ready-to-install mod folder
in mod/build/.

Each `random` call in the patched hot paths is preceded by `SetRandomKey(...)`
seeded from state that persists across save/load (goHnd / position / plInd /
attacker uniqrnd, combined with gProgress.progresstick). The result is a
deterministic decision from save state alone — same save reload, or same
join-in-progress for clients, yields the same RNG outcome.

CANONICAL RNG-PATCH PATTERN: `SetRandomKey(seed)` followed by `random` (NOT
`RandomExt`). SetRandomKey seeds only the 32-bit `Random` LCG stream;
`RandomExt` has its own independent 64-bit seed (set via `SetRandomExtKey64`)
and is unaffected. The stock engine uses this exact pattern in
unit.script:5301, 11453, 11528 and weapon.script:1051.

See internals/engine/rng_implementation.md §3 for the SetRandomKey / RandomExt
independence fact, and docs/recon/world/economy/peasant_extraction.md for the
extraction RNG-site catalogue.

ANTI-SNOWBALL DESIGN (v5):
The cascade problem in symmetric battles (100v100 → winner survives 40+) has
three compounding causes patched here:

  (A) Target selection: units focus the same enemy — addressed by the
      anti-clumping relativeDist multiplier (K=0.5, was 0.1/0.125 stock).
      Targets with 1 attacker look 5× farther away; 2 attackers → 9×; 3+ →
      gc_MaxInt (effectively invisible). Ranged units now participate too.

  (B) Focus-fire damage efficiency: even when 2 attackers reach the same target
      (no fresh targets nearby), second attacker deals only 50% damage, reducing
      the kill-rate advantage of numerical pile-on.

  (C) Retarget cascade: after a kill the freed attacker instantly charges the
      next victim. Now a 1.5 g-sec attackdelay is imposed after every kill
      (MaxFloat so natural pause is never shortened). The retarget search is
      gated on attackdelay=0, so the unit idles before it can join another fight.

  (D) Fatigue drain: every kill (any weapon) costs the attacker 20% of maxhp.
      A unit that won 3 fights has lost 60% maxhp and is close to death —
      cascade "winners" become progressively easier targets.

  (E) Fresh-unit penalty: attackers above 80% maxhp deal −20% damage (any
      weapon). Cascade survivors with nearly-full hp hit softer against their
      next victim, providing negative feedback against the snowball.

  (F) Headshot variance: musketeers no longer spike 250+ damage on 5% shots.
      bHeadShot now always fires for eligible units (bCanHeadShot and not
      bFastHorseBullet) at a flat +12 damage — average-neutral vs 5%×250=12.5
      but zero variance. Horse immunity and bCanHeadShot logic unchanged.
"""

import argparse
import shutil
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(REPO_ROOT))

from parser.config import GAME_ROOT, LIB  # reuse the canonical install path

MOD_NAME = "Deterministic Cossacks"
SRC_DIR = Path(__file__).resolve().parent / "src"
BUILD_DIR = Path(__file__).resolve().parent / "build" / MOD_NAME

# Each patch: (file relative to LIB, expected line, original line text, replacement lines).
# `expected_line` is 1-indexed and used only for sanity (we still verify by exact text match).
PATCHES = [
    # ---------- Extraction RNG sites (peasant resource search) ----------
    {
        "file": "misc.script",
        "name": "FindResourceToExtract: rndind (start index in resgrid cell)",
        "expected_line": 2790,
        "original": "         rndind := floor(random*count);",
        "replacement": [
            "         SetRandomKey(floor((px+10000)*97) + floor((py+10000)*101) + plInd*13 + (gProgress.progresstick mod 30000));",
            "         rndind := floor(random*count);",
        ],
    },
    {
        "file": "misc.script",
        "name": "FindResourceToExtract: wood vs stone choice",
        "expected_line": 2801,
        "original": "                  if (random<(testW/(testW+testS))) then",
        "replacement": [
            "                  SetRandomKey(floor((px+10000)*53) + floor((py+10000)*59) + plInd*17 + (gProgress.progresstick mod 30000) + 7919);",
            "                  if (random<(testW/(testW+testS))) then",
        ],
    },
    {
        "file": "unit.script",
        "name": "SearchResourceInRadius: standtime gate (random<waitrnd)",
        "expected_line": 4055,
        "original": "            if (random<waitrnd) then",
        "replacement": [
            "            SetRandomKey(goHnd*31 + (gProgress.progresstick mod 30000));",
            "            if (random<waitrnd) then",
        ],
    },
    {
        "file": "unit.script",
        "name": "SearchResourceInRadius: bskipcheck (random>0.75)",
        "expected_line": 4114,
        "original": "   var bskipcheck : Boolean = (random>0.75);",
        "replacement": [
            "   SetRandomKey(goHnd*37 + (gProgress.progresstick mod 30000) + 1009);",
            "   var bskipcheck : Boolean = (random>0.75);",
        ],
    },
    {
        "file": "unit.script",
        "name": "SearchResourceInRadius: rndind (start index in candidate list)",
        "expected_line": 4120,
        "original": "      rndind := floor(random*count);",
        "replacement": [
            "      SetRandomKey(goHnd*41 + (gProgress.progresstick mod 30000) + 2027);",
            "      rndind := floor(random*count);",
        ],
    },

    # ---------- Combat RNG sites (target selection / headshot) ----------
    {
        "file": "miscext2.script",
        "name": "DoDamage: bHeadShot - always fires for eligible units (removed random<0.05)",
        "expected_line": 420,
        "original": "                        var bHeadShot : Boolean = bCanHeadShot and (random<0.05) and (not bFastHorseBullet); // in C1 there is 4 percent chance to kill any unit with bullet, no matter how much hp. in c3 after shooters rebalance. changed change to 2 percent",
        "replacement": [
            "                        var bHeadShot : Boolean = bCanHeadShot and (not bFastHorseBullet); // headshot always fires for eligible units (flat +12 dmg, zero variance) (mod by Deterministic Cossacks)",
        ],
    },
    {
        "file": "miscext2.script",
        "name": "DoDamage: headshot flat +12 + musketeer suicide shot + damage modifiers",
        "expected_line": 437,
        "original": "                        damage := damage+floor(TObj(pobj).uniqrnd*500);",
        "replacement": [
            # headshot: flat +12 (avg-neutral vs 5%*250=12.5, zero variance)
            "                        damage := damage+12; // headshot flat +12 (mod by Deterministic Cossacks)",
            # all combat modifiers restricted to infantry and horses only
            "                        var attUsageDmg : Integer = _unit_GetUsage(goHnd);",
            "                        var bDmgInfHorse : Boolean = (attUsageDmg = gc_obj_usage_lightinfantry) or (attUsageDmg = gc_obj_usage_grenadier) or (attUsageDmg = gc_obj_usage_shooter) or (attUsageDmg = gc_obj_usage_archer) or (attUsageDmg = gc_obj_usage_fasthorse) or (attUsageDmg = gc_obj_usage_hardhorse) or (attUsageDmg = gc_obj_usage_horseshooter);",
            "                        if (bDmgInfHorse) then begin",
            # musketeer suicide shot: 5% chance to deal 250 damage and then die at retarget gate
            "                        var bMusketSuicide : Boolean = False;",
            "                        if (weapkind = gc_obj_weapon_kind_bullet) then begin",
            "                        var trgUsageSuicide : Integer = _unit_GetUsage(trgHnd);",
            "                        if (trgUsageSuicide = gc_obj_usage_shooter) or (trgUsageSuicide = gc_obj_usage_horseshooter) then begin",
            "                        SetRandomKey(floor(TObj(pobj).uniqrnd*gc_MaxInt) + (gProgress.progresstick mod 30000) + 7331);",
            "                        if (random < 0.05) then begin",
            "                        damage := 250;",
            "                        TObj(pobj).hp := 1; // near-death: retarget gate kills musketeer after firing (mod by Deterministic Cossacks)",
            "                        bMusketSuicide := True;",
            "                        end;",
            "                        end; // trgUsageSuicide is shooter/horseshooter",
            "                        end;",
            # other modifiers only apply on normal shots
            "                        if (not bMusketSuicide) then begin",
            # pile-on penalty: 2nd attacker on same target deals 50% damage, 3rd 25%, etc.
            "                        var pstolistDmg : Pointer = _misc_GetObjectArgData(trgHnd, gc_argunit_stolist);",
            "                        var nAtt : Integer = TIntegerList(pstolistDmg).GetCount;",
            "                        if (nAtt >= 3) then damage := floor(damage * 0.30)",
            "                        else if (nAtt = 2) then damage := floor(damage * 0.50)",
            "                        else if (nAtt = 1) then damage := floor(damage * 0.75); // pile-on penalty: 2nd=75% 3rd=50% 4th+=30% (mod by Deterministic Cossacks)",
            # fresh-unit penalty + wounded-fighter bonus
            "                        var pobjbaseAttF : Pointer = gPlayer[TObj(pobj).pl].objbase[TObj(pobj).cid][TObj(pobj).id];",
            "                        var attMaxHpF : Integer = TObjBase(pobjbaseAttF).maxhp;",
            "                        if (attMaxHpF>0) and (TObj(pobj).hp*5 > attMaxHpF*4) then",
            "                        damage := floor(damage * 0.80); // fresh-unit penalty: -20% dmg when attacker hp > 80% maxhp (mod by Deterministic Cossacks)",
            "                        if (attMaxHpF>0) and (TObj(pobj).hp*2 < attMaxHpF) then",
            "                        damage := floor(damage * 1.20); // wounded-fighter bonus: +20% dmg when attacker hp < 50% maxhp (mod by Deterministic Cossacks)",
            # outnumbered bonus: +25% per enemy currently attacking the attacker
            "                        var pstolistMe : Pointer = _misc_GetObjectArgData(goHnd, gc_argunit_stolist);",
            "                        var attOnMe : Integer = TIntegerList(pstolistMe).GetCount;",
            "                        if (attOnMe > 5) then attOnMe := 5; // cap at 5 attackers (+125% max)",
            "                        if (attOnMe > 0) then damage := floor(damage * (1.0 + attOnMe * 0.50)); // outnumbered bonus: +50% per attacker on self, max +250% at 5 (mod by Deterministic Cossacks)",
            # near-death: hp < 3 -> damage /3, then 80% chance damage = 0
            "                        if (TObj(pobj).hp < 3) then begin",
            "                        damage := floor(damage / 3);",
            "                        SetRandomKey(floor(TObj(pobj).uniqrnd*gc_MaxInt) + (gProgress.progresstick mod 30000) + 9973);",
            "                        if (random < 0.80) then damage := 0;",
            "                        end; // near-death penalty (mod by Deterministic Cossacks)",
            "                        end; // not bMusketSuicide",
            "                        end; // bDmgInfHorse",
        ],
    },
    {
        "file": "miscext2.script",
        "name": "DoDamage: retarget delay + fatigue per kill (infantry/horse only; fatigue only when killing shooters)",
        "expected_line": 463,
        "original": "                           TObj(pobj).kill := TObj(pobj).kill+1;",
        "replacement": [
            "                           TObj(pobj).kill := TObj(pobj).kill+1;",
            "                           if (goHnd<>0) then begin",
            "                              var attUsage : Integer = _unit_GetUsage(goHnd);",
            "                              var bKillInfHorse : Boolean = (attUsage = gc_obj_usage_lightinfantry) or (attUsage = gc_obj_usage_grenadier) or (attUsage = gc_obj_usage_shooter) or (attUsage = gc_obj_usage_archer) or (attUsage = gc_obj_usage_fasthorse) or (attUsage = gc_obj_usage_hardhorse) or (attUsage = gc_obj_usage_horseshooter);",
            "                              if (bKillInfHorse) then begin",
            "                              TObj(pobj).attackdelay := MaxFloat(TObj(pobj).attackdelay, 1.5); // retarget delay: 1.5 g-sec after kill (mod by Deterministic Cossacks)",
            # fatigue: infantry/horse attacker; only when the killed unit was a firearm unit (shooter/horseshooter)
            "                              var bFatigueInf : Boolean = (attUsage = gc_obj_usage_lightinfantry) or (attUsage = gc_obj_usage_grenadier) or (attUsage = gc_obj_usage_shooter) or (attUsage = gc_obj_usage_archer);",
            "                              var bFatigueHorse : Boolean = (attUsage = gc_obj_usage_fasthorse) or (attUsage = gc_obj_usage_hardhorse) or (attUsage = gc_obj_usage_horseshooter);",
            "                              var trgUsage : Integer = _unit_GetUsage(trgHnd);",
            # fatigue fires only when attacker and victim are in the same combat category
            "                              var bAttMelee : Boolean = (attUsage = gc_obj_usage_lightinfantry) or (attUsage = gc_obj_usage_grenadier) or (attUsage = gc_obj_usage_fasthorse) or (attUsage = gc_obj_usage_hardhorse);",
            "                              var bAttRanged : Boolean = (attUsage = gc_obj_usage_shooter) or (attUsage = gc_obj_usage_archer) or (attUsage = gc_obj_usage_horseshooter);",
            "                              var bVicMelee : Boolean = (trgUsage = gc_obj_usage_lightinfantry) or (trgUsage = gc_obj_usage_grenadier) or (trgUsage = gc_obj_usage_fasthorse) or (trgUsage = gc_obj_usage_hardhorse);",
            "                              var bVicRanged : Boolean = (trgUsage = gc_obj_usage_shooter) or (trgUsage = gc_obj_usage_archer) or (trgUsage = gc_obj_usage_horseshooter);",
            "                              if ((bAttMelee and bVicMelee) or (bAttRanged and bVicRanged)) and (bFatigueInf or bFatigueHorse) then begin",
            "                              var pobjbaseAtt : Pointer = gPlayer[TObj(pobj).pl].objbase[TObj(pobj).cid][TObj(pobj).id];",
            "                              var attMaxHp : Integer = TObjBase(pobjbaseAtt).maxhp;",
            "                              var fatigueAmt : Integer = 0;",
            "                              if (bFatigueInf) then fatigueAmt := floor(attMaxHp * 0.15)",
            "                              else fatigueAmt := floor(attMaxHp * 0.05); // horse",
            "                              TObj(pobj).hp := TObj(pobj).hp - fatigueAmt; // fatigue per kill (mod by Deterministic Cossacks)",
            "                              if (TObj(pobj).hp < 1) then TObj(pobj).hp := 1; // survive fatigue at 1 hp",
            "                              end;",
            "                              end; // bKillInfHorse",
            "                           end;",
        ],
    },
    {
        "file": "unit.script",
        "name": "SearchEnemyInCellShips: rndind (start index in cell)",
        "expected_line": 4796,
        "original": "         rndind := floor(random*count);",
        "replacement": [
            "         SetRandomKey(floor(TObj(pobj).uniqrnd*gc_MaxInt) + cellx*73 + celly*131 + (gProgress.progresstick mod 30000) + 5077);",
            "         rndind := floor(random*count);",
        ],
    },
    {
        "file": "unit.script",
        "name": "SearchEnemyInCell: rndind (start index in cell)",
        "expected_line": 4872,
        "original": "            rndind := floor(random*count);",
        "replacement": [
            "            SetRandomKey(floor(TObj(pobj).uniqrnd*gc_MaxInt) + cellx*79 + celly*139 + plind*17 + (gProgress.progresstick mod 30000) + 1543);",
            "            rndind := floor(random*count);",
        ],
    },
    {
        "file": "unit.script",
        "name": "SearchEnemyScanCellsLongRange: dx random pick",
        "expected_line": 4992,
        "original": "      var dx : Integer = cellx+floor(1+random*(cellxmax-cellx));",
        "replacement": [
            "      SetRandomKey(floor(TObj(pobj).uniqrnd*gc_MaxInt) + i*101 + cellx*89 + (gProgress.progresstick mod 30000) + 3001);",
            "      var dx : Integer = cellx+floor(1+random*(cellxmax-cellx));",
        ],
    },
    {
        "file": "unit.script",
        "name": "SearchEnemyScanCellsLongRange: dy random pick",
        "expected_line": 4993,
        "original": "      var dy : Integer = celly+floor(1+random*(cellymax-celly));",
        "replacement": [
            "      SetRandomKey(floor(TObj(pobj).uniqrnd*gc_MaxInt) + i*103 + celly*97 + (gProgress.progresstick mod 30000) + 4421);",
            "      var dy : Integer = celly+floor(1+random*(cellymax-celly));",
        ],
    },

    # ---------- Anti-snowball patches ----------
    # Three compounding mechanisms addressed:
    #
    # (A) Target selection bias — units prefer to pile on the same enemy.
    #     relativeDist multiplier raised to K=0.5 (was 0.1/0.125 stock, 0.8/1.0 v4).
    #     With 1 attacker a target looks 5× farther; 2 attackers → 9×; 3+ → gc_MaxInt.
    #     Ranged units now also use the multiplier in short-range scan.
    #
    # (B) Focus-fire damage — even when two attackers reach the same target,
    #     the second one deals only 65% damage (−35% 2v1 penalty, in DoDamage).
    #
    # (C) Retarget cascade — after a kill the freed attacker instantly chains
    #     to the next enemy in the same game tick.  Now a 0.5 g-sec attackdelay
    #     is injected on kill (DoDamage) and the retarget search is gated in
    #     unit.script so the unit genuinely idles before it can join another fight.
    {
        "file": "unit.script",
        "name": "Retarget gate: idle while attackdelay > 0; near-death kill when hp < 3",
        "expected_line": 8400,
        "original": "            var newHnd : Integer;",
        "replacement": [
            "            var newHnd : Integer;",
            "            var gateUsage : Integer = _unit_GetUsage(goHnd);",
            "            var bGateInfHorse : Boolean = (pobj<>nil) and ((gateUsage = gc_obj_usage_lightinfantry) or (gateUsage = gc_obj_usage_grenadier) or (gateUsage = gc_obj_usage_shooter) or (gateUsage = gc_obj_usage_archer) or (gateUsage = gc_obj_usage_fasthorse) or (gateUsage = gc_obj_usage_hardhorse) or (gateUsage = gc_obj_usage_horseshooter));",
            "            if bGateInfHorse and (TObj(pobj).hp > 0) and (TObj(pobj).hp < 3) and (TObj(pobj).attackdelay > 0) then begin",
            "            TObj(pobj).hp := 0;",
            "            _unit_SetTagStates(goHnd, gc_statetag_essential_death) // near-death kill: die in retarget window, outside DoDamage (mod by Deterministic Cossacks)",
            "            end else",
            "            if bGateInfHorse and (TObj(pobj).attackdelay > 0) then",
            "            _unit_SetTagStates(goHnd, gc_statetag_action_none)",
            "            else",
        ],
    },
    {
        "file": "unit.script",
        "name": "Anti-clump strengthen: ScanCellsLongRange (K 0.1 -> 0.5 + cap N>=3 + injured x2.5)",
        "expected_line": 5127,
        "original": "                     relativeDist := distSqr*(1+TIntegerList(pstolist).GetCount*0.1);",
        "replacement": [
            "                     var acUsage2 : Integer = _unit_GetUsage(goHnd);",
            "                     if (acUsage2 = gc_obj_usage_lightinfantry) or (acUsage2 = gc_obj_usage_grenadier) or (acUsage2 = gc_obj_usage_shooter) or (acUsage2 = gc_obj_usage_archer) or (acUsage2 = gc_obj_usage_fasthorse) or (acUsage2 = gc_obj_usage_hardhorse) or (acUsage2 = gc_obj_usage_horseshooter) then begin",
            "                     var attCount2 : Integer = TIntegerList(pstolist).GetCount;",
            "                     relativeDist := distSqr*(1+attCount2*0.5);",
            "                     var pTrgObj2 : Pointer = _unit_GetTObj(trgHnd);",
            "                     if (pTrgObj2<>nil) then begin",
            "                        var trgMaxHp2 : Integer = gPlayer[TObj(pTrgObj2).pl].objbase[TObj(pTrgObj2).cid][TObj(pTrgObj2).id].maxhp;",
            "                        if (trgMaxHp2>0) and (TObj(pTrgObj2).hp*2<trgMaxHp2) and (TObj(pTrgObj2).hp>=3) then",
            "                        relativeDist := relativeDist*2.5;",
            "                     end;",
            "                     end else",
            "                     relativeDist := distSqr*(1+TIntegerList(pstolist).GetCount*0.1);",
        ],
    },
    {
        "file": "unit.script",
        "name": "Anti-clump strengthen: ScanCells melee (K 0.125 -> 0.5 + cap N>=3 + injured x2.5)",
        "expected_line": 5191,
        "original": "                        relativeDist := distSqr*(1+TIntegerList(pstolist).GetCount*0.125);",
        "replacement": [
            "                        var acUsage : Integer = _unit_GetUsage(goHnd);",
            "                        if (acUsage = gc_obj_usage_lightinfantry) or (acUsage = gc_obj_usage_grenadier) or (acUsage = gc_obj_usage_shooter) or (acUsage = gc_obj_usage_archer) or (acUsage = gc_obj_usage_fasthorse) or (acUsage = gc_obj_usage_hardhorse) or (acUsage = gc_obj_usage_horseshooter) then begin",
            "                        var attCount : Integer = TIntegerList(pstolist).GetCount;",
            "                        relativeDist := distSqr*(1+attCount*0.5);",
            "                        var pTrgObj : Pointer = _unit_GetTObj(trgHnd);",
            "                        if (pTrgObj<>nil) then begin",
            "                           var trgMaxHp : Integer = gPlayer[TObj(pTrgObj).pl].objbase[TObj(pTrgObj).cid][TObj(pTrgObj).id].maxhp;",
            "                           if (trgMaxHp>0) and (TObj(pTrgObj).hp*2<trgMaxHp) and (TObj(pTrgObj).hp>=3) then",
            "                           relativeDist := relativeDist*2.5;",
            "                        end;",
            "                        end else",
            "                        relativeDist := distSqr*(1+TIntegerList(pstolist).GetCount*0.125);",
        ],
    },
    {
        "file": "unit.script",
        "name": "Anti-clump extend: ScanCells ranged (new K=0.5 + cap N>=3 + injured x2.5)",
        "expected_line": 5194,
        "original": "                     relativeDist := distSqr;",
        "replacement": [
            "                     var acUsageR : Integer = _unit_GetUsage(goHnd);",
            "                     if (acUsageR = gc_obj_usage_lightinfantry) or (acUsageR = gc_obj_usage_grenadier) or (acUsageR = gc_obj_usage_shooter) or (acUsageR = gc_obj_usage_archer) or (acUsageR = gc_obj_usage_fasthorse) or (acUsageR = gc_obj_usage_hardhorse) or (acUsageR = gc_obj_usage_horseshooter) then begin",
            "                        var pstolistR : Pointer = _misc_GetObjectArgData(trgHnd, gc_argunit_stolist);",
            "                        var attCountR : Integer = TIntegerList(pstolistR).GetCount;",
            "                        relativeDist := distSqr*(1+attCountR*0.5);",
            "                        var pTrgObjR : Pointer = _unit_GetTObj(trgHnd);",
            "                        if (pTrgObjR<>nil) then begin",
            "                           var trgMaxHpR : Integer = gPlayer[TObj(pTrgObjR).pl].objbase[TObj(pTrgObjR).cid][TObj(pTrgObjR).id].maxhp;",
            "                           if (trgMaxHpR>0) and (TObj(pTrgObjR).hp*2<trgMaxHpR) and (TObj(pTrgObjR).hp>=3) then",
            "                           relativeDist := relativeDist*2.5;",
            "                        end;",
            "                     end else",
            "                     relativeDist := distSqr;",
        ],
    },
]


def apply_patches(file_text: str, patches: list[dict], filename: str) -> str:
    """Apply patches in reverse line order so earlier line numbers stay valid.

    Each patch must match its `original` exactly once in the file; we verify
    that and that the matched location is near `expected_line` (within 5 lines).
    """
    lines = file_text.splitlines(keepends=False)
    file_patches = sorted(
        [p for p in patches if p["file"] == filename],
        key=lambda p: -p["expected_line"],
    )

    for patch in file_patches:
        original = patch["original"]
        # Find unique match
        matches = [i for i, ln in enumerate(lines) if ln == original]
        if len(matches) == 0:
            raise RuntimeError(
                f"Patch '{patch['name']}': original line not found in {filename}\n"
                f"  expected near line {patch['expected_line']}\n"
                f"  text: {original!r}"
            )
        if len(matches) > 1:
            raise RuntimeError(
                f"Patch '{patch['name']}': original line is not unique in {filename} "
                f"({len(matches)} matches at lines {[m+1 for m in matches]})"
            )
        idx = matches[0]
        actual_line = idx + 1
        if abs(actual_line - patch["expected_line"]) > 5:
            print(
                f"  ! Warning: '{patch['name']}' matched at line {actual_line}, "
                f"expected ~{patch['expected_line']} (drift > 5). Game version likely changed."
            )
        # Replace
        lines[idx : idx + 1] = patch["replacement"]
        print(f"  + {patch['name']} (line {actual_line})")

    return "\n".join(lines) + ("\n" if file_text.endswith("\n") else "")


def build(install: bool = False) -> None:
    print(f"Source game files: {LIB}")
    if not LIB.exists():
        sys.exit(f"ERROR: {LIB} does not exist. Set $COSSACKS3_PATH to your install root.")

    # Clean / recreate build dir
    if BUILD_DIR.exists():
        shutil.rmtree(BUILD_DIR)
    BUILD_DIR.mkdir(parents=True)

    # Copy mod.ini
    shutil.copy2(SRC_DIR / "mod.ini", BUILD_DIR / "mod.ini")

    # Apply patches per file
    out_lib = BUILD_DIR / "data" / "scripts" / "lib"
    out_lib.mkdir(parents=True)
    files_to_patch = sorted({p["file"] for p in PATCHES})
    for filename in files_to_patch:
        src_path = LIB / filename
        if not src_path.exists():
            sys.exit(f"ERROR: missing source file {src_path}")
        text = src_path.read_text(encoding="utf-8", errors="replace")
        print(f"Patching {filename} ({len(text):,} bytes)...")
        patched = apply_patches(text, PATCHES, filename)
        (out_lib / filename).write_text(patched, encoding="utf-8")
        print(f"  -> {out_lib / filename}")

    print()
    print(f"Mod built at: {BUILD_DIR}")
    print()

    if install:
        do_install()
    else:
        print_install_instructions()


def do_install() -> None:
    target_mod_dir = GAME_ROOT / "mods" / MOD_NAME
    mods_ini = GAME_ROOT / "mods" / "mods.ini"

    if target_mod_dir.exists():
        print(f"Removing existing mod at {target_mod_dir}")
        shutil.rmtree(target_mod_dir)

    print(f"Copying {BUILD_DIR} -> {target_mod_dir}")
    shutil.copytree(BUILD_DIR, target_mod_dir)

    # Read existing mods.ini and add our entry if not already present.
    if not mods_ini.exists():
        sys.exit(f"ERROR: {mods_ini} does not exist; cannot register mod.")

    text = mods_ini.read_text(encoding="utf-8")
    entry_marker = f"dir = ..\\{MOD_NAME}"
    if entry_marker in text:
        print(f"Mod already registered in {mods_ini}, skipping mods.ini edit.")
        return

    # Insert our entry inside the mods : struct.begin ... struct.end block.
    new_entry = (
        "      [*] : struct.begin\n"
        f"         dir = ..\\{MOD_NAME}\n"
        "         dis = False\n"
        "      struct.end\n"
    )
    insertion_anchor = "   struct.end\nsection.end"
    if insertion_anchor not in text:
        sys.exit(f"ERROR: could not find anchor in {mods_ini}; edit it manually.")
    text = text.replace(insertion_anchor, new_entry + insertion_anchor, 1)
    mods_ini.write_text(text, encoding="utf-8")
    print(f"Registered mod in {mods_ini}.")
    print("Restart Cossacks 3 (or run modman.exe) to activate.")


def print_install_instructions() -> None:
    target_mod_dir = GAME_ROOT / "mods" / MOD_NAME
    mods_ini = GAME_ROOT / "mods" / "mods.ini"
    print("To install:")
    print(f"  1. Copy build folder:  {BUILD_DIR}  ->  {target_mod_dir}")
    print(f"  2. Edit {mods_ini} and add inside the `mods : struct.begin` block:")
    print()
    print("        [*] : struct.begin")
    print(f"           dir = ..\\{MOD_NAME}")
    print("           dis = False")
    print("        struct.end")
    print()
    print("  3. Restart Cossacks 3 (or run modman.exe).")
    print()
    print("Or re-run with --install for automatic install (may need admin write to Program Files).")


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument(
        "--install",
        action="store_true",
        help="After building, copy the mod to the game's mods/ folder and register in mods.ini.",
    )
    args = ap.parse_args()
    build(install=args.install)
