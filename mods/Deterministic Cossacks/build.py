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
        "name": "DoDamage: bHeadShot (random<0.05)",
        "expected_line": 420,
        "original": "                        var bHeadShot : Boolean = bCanHeadShot and (random<0.05) and (not bFastHorseBullet); // in C1 there is 4 percent chance to kill any unit with bullet, no matter how much hp. in c3 after shooters rebalance. changed change to 2 percent",
        "replacement": [
            "                        SetRandomKey(floor(TObj(pobj).uniqrnd*gc_MaxInt) + floor(TObj(pobj2).uniqrnd*gc_MaxInt) + (gProgress.progresstick mod 30000) + 8191);",
            "                        var bHeadShot : Boolean = bCanHeadShot and (random<0.05) and (not bFastHorseBullet); // headshot RNG: deterministic seed from attacker+target uniqrnd + progresstick (mod by Deterministic Cossacks)",
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
