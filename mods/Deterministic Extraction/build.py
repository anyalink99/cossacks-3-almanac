"""
Builds the "Deterministic Extraction" Cossacks 3 mod.

Reads stock lib/misc.script and lib/unit.script from the Cossacks 3 install (path
from $COSSACKS3_PATH or default Steam location), applies 5 line-precise patches,
and emits a ready-to-install mod folder in mod/build/.

Each `random` in the resource-search hot path is replaced with a SetRandomKey +
RandomExt pair seeded from state that persists across save/load (goHnd or
position+plInd, combined with gProgress.progresstick). The resulting symbol is
deterministic from save state alone, so reload of the same save yields identical
peasant decisions.

See mod/README.md for the rationale and recon/determinism_audit.md §3 for the
RNG-site catalogue this addresses.
"""

import argparse
import shutil
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(REPO_ROOT))

from parser.config import GAME_ROOT, LIB  # reuse the canonical install path

MOD_NAME = "Deterministic Extraction"
SRC_DIR = Path(__file__).resolve().parent / "src"
BUILD_DIR = Path(__file__).resolve().parent / "build" / MOD_NAME

# Each patch: (file relative to LIB, expected line, original line text, replacement lines).
# `expected_line` is 1-indexed and used only for sanity (we still verify by exact text match).
PATCHES = [
    {
        "file": "misc.script",
        "name": "FindResourceToExtract: rndind (start index in resgrid cell)",
        "expected_line": 2790,
        "original": "         rndind := floor(random*count);",
        "replacement": [
            "         SetRandomKey(floor((px+10000)*97) + floor((py+10000)*101) + plInd*13 + (gProgress.progresstick mod 30000));",
            "         rndind := floor(RandomExt*count);",
        ],
    },
    {
        "file": "misc.script",
        "name": "FindResourceToExtract: wood vs stone choice",
        "expected_line": 2801,
        "original": "                  if (random<(testW/(testW+testS))) then",
        "replacement": [
            "                  SetRandomKey(floor((px+10000)*53) + floor((py+10000)*59) + plInd*17 + (gProgress.progresstick mod 30000) + 7919);",
            "                  if (RandomExt<(testW/(testW+testS))) then",
        ],
    },
    {
        "file": "unit.script",
        "name": "SearchResourceInRadius: standtime gate (random<waitrnd)",
        "expected_line": 4055,
        "original": "            if (random<waitrnd) then",
        "replacement": [
            "            SetRandomKey(goHnd*31 + (gProgress.progresstick mod 30000));",
            "            if (RandomExt<waitrnd) then",
        ],
    },
    {
        "file": "unit.script",
        "name": "SearchResourceInRadius: bskipcheck (random>0.75)",
        "expected_line": 4114,
        "original": "   var bskipcheck : Boolean = (random>0.75);",
        "replacement": [
            "   SetRandomKey(goHnd*37 + (gProgress.progresstick mod 30000) + 1009);",
            "   var bskipcheck : Boolean = (RandomExt>0.75);",
        ],
    },
    {
        "file": "unit.script",
        "name": "SearchResourceInRadius: rndind (start index in candidate list)",
        "expected_line": 4120,
        "original": "      rndind := floor(random*count);",
        "replacement": [
            "      SetRandomKey(goHnd*41 + (gProgress.progresstick mod 30000) + 2027);",
            "      rndind := floor(RandomExt*count);",
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
