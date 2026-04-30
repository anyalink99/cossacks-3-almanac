"""Validate compute_map_resources predictions against replay ground truth.

For each replay in `docs/derived/replay_ground_truth.json`:
  1. Reconstruct game settings (mapsize, relieftype, resourcemines, foreststype, ...)
  2. Run `compute_counts(...)` from compute_map_resources to get the model prediction
  3. Compare predicted clusters/type to actual clusters/type from replay

Outputs:
  - stdout: per-replay diff table
  - docs/reports/map/map_predictions_validation.md: aggregate calibration report

This is the empirical-validation harness that lets us tune compute_map_resources
without needing to play 100 games — we already have replays.
"""
from __future__ import annotations
import collections
import json
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "parser"))
from config import DERIVED_DIR, REPORTS_DIR, REPORTS_MAP_DIR
from compute_map_resources import compute_counts

GROUND_TRUTH = DERIVED_DIR / "replay_ground_truth.json"
OUT_MD = REPORTS_MAP_DIR / "map_predictions_validation.md"


def spcount_from_maskname(maskname: str | None) -> int:
    """Extract starting-position count from mask filename like '4pl_mask_continent_42_gauss.tga'.
    This is the TOTAL number of starting points on the bitmap (= max players)."""
    if not maskname:
        return 4
    import re
    m = re.match(r"(\d+)pl_", maskname)
    if m:
        return int(m.group(1))
    return 4


def predicted_mines_per_type(mapsize: int, mines: int, n_real_players: int,
                              spcount: int) -> int:
    """Total mine clusters per resource (mng / mni / mnc).

    Verified against dogenerate.inc:522-720 + 985 + 1770:
      - CreateStartPoint(plInd, ...) calls SetupMines(.., 0, 1, ...) — only round 0,
        only for actual-player positions.
      - After CreateStartPoint loop: SetupMines(..., 1, 0, ...) for ALL spcount
        positions — rounds 1..rounds-1 (tiny skips i=4).

    So per position:
      player: 1 (round 0 from CreateStartPoint) + (rounds_after - tiny_skip)
      unused: 0 + (rounds_after - tiny_skip)

    For mines=2 (Rich), rounds=5, tiny skips round 4 → 4 effective rounds.
      → player: 4, unused: 3
    For mines=1 (Medium), rounds=4, tiny skips round 4 (no-op) → 4.
      → player: 4, unused: 3
    For mines=0 (Poor), rounds=3, tiny no skip → 3.
      → player: 3, unused: 2
    """
    rounds_lookup = {0: 3, 1: 4, 2: 5}
    rounds = rounds_lookup.get(mines, 5)
    is_tiny = (mapsize == 3)
    # Second SetupMines call: minround=1, maxround=0 (no cap), so rounds 1..rounds-1
    # On tiny, i=4 is skipped via `continue`.
    rounds_after_iters = list(range(1, rounds))
    if is_tiny:
        rounds_after_iters = [i for i in rounds_after_iters if i != 4]
    n_after = len(rounds_after_iters)
    player_mines = 1 + n_after
    unused_mines = n_after
    n_unused = max(0, spcount - n_real_players)
    return n_real_players * player_mines + n_unused * unused_mines


def infer_n_real_players(d: dict) -> int | None:
    """Infer the actual player count from the replay's mng cluster count.

    For Land terrain (terraintype=0), mines_per_type = P × (1+n_after) +
    (spcount-P) × n_after = P + spcount × n_after. So P = mng - spcount × n_after.

    Returns None on non-Land (formula doesn't hold — engine logic differs) or
    when the inferred P is implausible (negative, > spcount).
    """
    s = d.get("settings", {})
    if s.get("terraintype") != 0:
        return None  # only Land follows the simple formula
    mapsize = s.get("mapsize") if isinstance(s.get("mapsize"), int) else 3
    mines = s.get("resourcemines") if isinstance(s.get("resourcemines"), int) else 2
    spcount = spcount_from_maskname(s.get("maskname"))
    rounds_lookup = {0: 3, 1: 4, 2: 5}
    rounds = rounds_lookup.get(mines, 5)
    iters = list(range(1, rounds))
    if mapsize == 3:  # tiny skips i=4
        iters = [i for i in iters if i != 4]
    n_after = len(iters)
    mng_count = (d.get("type_counts", {}).get("mng", 0)
                 + d.get("type_counts", {}).get("desert_mng", 0))
    P = mng_count - spcount * n_after
    if P < 1 or P > spcount:
        return None
    return P


def predict_for_replay(d: dict) -> dict[str, int]:
    """Run compute_counts with this replay's settings → return predicted clusters per type."""
    s = d.get("settings", {})
    mapsize = s.get("mapsize") if isinstance(s.get("mapsize"), int) else 3
    relief = s.get("relieftype") if isinstance(s.get("relieftype"), int) else 3
    # relieftype=5 means "Random" in lobby — engine rolls 0..4 (dogenerate.inc:1621-1622).
    # We don't know what value engine picked; default to Highlands (3) which is the
    # most common in user's data and a reasonable midpoint for forest densities.
    if relief > 4:
        relief = 3
    mines = s.get("resourcemines") if isinstance(s.get("resourcemines"), int) else 2
    spcount = spcount_from_maskname(s.get("maskname"))
    # Try to infer real player count from mng cluster count (Land only).
    # Falls back to spcount (= bitmap max) for non-Land or implausible inferences.
    inferred_P = infer_n_real_players(d)
    n_real_players = s.get("n_real_players", inferred_P if inferred_P is not None else spcount)
    # Foreststype is forced to 0 on Land (per dogenerate.inc:6); for non-Land
    # it can vary. We assume 0 here — non-Land replays will diverge somewhat.
    foreststype = 0
    try:
        r = compute_counts(
            mapsize_tag=mapsize,
            relieftype=relief,
            resourcemines=mines,
            foreststype=foreststype,
            water_blocking_pct=0.02,
            placement_success=0.65,
        )
    except Exception as e:
        return {"_error": str(e), "_spcount": spcount}
    # Extract per-type cluster predictions
    type_counts: dict[str, int] = {}
    for tn, n in r.get("big_real_per_call", []):
        type_counts[tn] = type_counts.get(tn, 0) + n
    for tn, n in r.get("mid_real_per_call", []):
        type_counts[tn] = type_counts.get(tn, 0) + n
    for tn, n in r.get("small_real_per_call", []):
        type_counts[tn] = type_counts.get(tn, 0) + n
    type_counts["stones"] = r.get("stone_real", 0)
    # Mines: depend on player vs unused starting positions (see predicted_mines_per_type).
    mines_per_type = predicted_mines_per_type(mapsize, mines, n_real_players, spcount)
    type_counts["mng"] = mines_per_type
    type_counts["mni"] = mines_per_type
    type_counts["mnc"] = mines_per_type
    type_counts["_spcount"] = spcount
    type_counts["_n_real_players"] = n_real_players
    return type_counts


def diff_replay(actual: dict, predicted: dict) -> dict:
    """Return {type: (actual, predicted, ratio)} where ratio = actual/predicted (or None)."""
    out = {}
    all_types = set(actual.keys()) | set(predicted.keys())
    for t in all_types:
        a = actual.get(t, 0)
        p = predicted.get(t, 0)
        ratio = a / p if p > 0 else None
        out[t] = (a, p, ratio)
    return out


def main():
    if not GROUND_TRUTH.exists():
        print(f"Run parser/parse_replay_aggregates.py first to populate {GROUND_TRUTH}")
        sys.exit(1)
    truth = json.loads(GROUND_TRUTH.read_text(encoding="utf-8"))

    # Filter to replays with default-ish settings (4pl, no special map options)
    # The model is calibrated for foreststype=0 = pinefir/pine/spruce mix on Land.
    # Replays on Plateaus (relief=5) or non-Land terrain will diverge.
    print(f"Total replays: {len(truth)}")

    rows = []
    for d in truth:
        pred = predict_for_replay(d)
        # Backwards compat: older JSONs used "file" key, newer use "id"
        rid = d.get("id") or d.get("file") or "?"
        if "_error" in pred:
            print(f"  {rid}: ERROR {pred['_error']}")
            continue
        actual = d.get("type_counts", {})
        diff = diff_replay(actual, pred)
        rows.append({
            "id": rid,
            "settings": d["settings"],
            "actual": actual,
            "predicted": pred,
            "diff": diff,
        })

    def bucket_key(s: dict) -> tuple:
        """Identify a calibration bucket: (mapsize, relief, terraintype, mask_kind).
        Random relief (5) lumped together — engine rolled an unknown 0..4."""
        msk = s.get("maskname") or ""
        # Mask kind = "Npl_<family>" (e.g., "4pl_nowater", "3pl_coastal")
        m = re.match(r"(\d+pl)_mask_(\w+?)_\d", msk)
        mask_kind = f"{m.group(1)}_{m.group(2)}" if m else msk[:20]
        return (s.get("mapsize"), s.get("relieftype"), s.get("terraintype"), mask_kind)

    def summarize(rs: list[dict], label: str) -> list[tuple]:
        """Compute per-type calibration summary for a list of replay rows."""
        ta: dict[str, list[int]] = collections.defaultdict(list)
        tp: dict[str, list[int]] = collections.defaultdict(list)
        for r in rs:
            for t, (a, p, _) in r["diff"].items():
                if t.startswith("_"):
                    continue  # internal metadata (_spcount, _n_real_players)
                if a > 0 or p > 0:
                    ta[t].append(a)
                    tp[t].append(p)
        out = []
        for t in ta:
            a_avg = sum(ta[t]) / len(ta[t])
            p_avg = sum(tp[t]) / len(tp[t])
            ratio = a_avg / p_avg if p_avg > 0 else None
            out.append((t, a_avg, p_avg, ratio, len(ta[t])))
        out.sort(key=lambda x: -x[1])
        return out

    # Bucket replays by setting
    buckets: dict[tuple, list[dict]] = collections.defaultdict(list)
    for r in rows:
        buckets[bucket_key(r["settings"])].append(r)

    # Print per-bucket calibration
    print(f"\n=== Replays bucketed by (mapsize, relief, terraintype, mask) ===")
    sorted_buckets = sorted(buckets.items(), key=lambda x: -len(x[1]))
    for key, brows in sorted_buckets:
        msz, rel, tt, mk = key
        rel_str = f"rel={rel}" + (" (Random)" if rel == 5 else "")
        print(f"  msz={msz} {rel_str} tt={tt} mask={mk}: {len(brows)} replays")

    # Detailed per-type for the largest homogeneous bucket
    biggest = sorted_buckets[0]
    print(f"\n=== Per-type calibration for largest bucket "
          f"(msz={biggest[0][0]}, rel={biggest[0][1]}, tt={biggest[0][2]}, "
          f"mask={biggest[0][3]}, n={len(biggest[1])}) ===")
    print(f"{'type':<35} {'actual_avg':>10} {'pred_avg':>9} {'ratio':>6} {'n':>3}")
    print(f"{'(want ratio close to 1.0)':<35}")
    bucket_summary = summarize(biggest[1], "biggest")
    for t, a, p, ratio, n in bucket_summary[:30]:
        ratio_str = f"{ratio:.2f}" if ratio is not None else "  ∞"
        print(f"  {t:<33} {a:>10.1f} {p:>9.1f} {ratio_str:>6} {n:>3}")

    # Cross-bucket aggregate (kept for backwards compat — but caveat noted)
    print(f"\n=== MIXED-BUCKET aggregate (across all {len(rows)} replays) ===")
    print(f"⚠ This averages predictions across different mapsizes/reliefs — ")
    print(f"   ratio≈1.0 here can be coincidence, not real calibration. Use bucket above.")
    type_summary = summarize(rows, "all")
    for t, a, p, ratio, n in type_summary[:30]:
        ratio_str = f"{ratio:.2f}" if ratio is not None else "  ∞"
        print(f"  {t:<33} {a:>10.1f} {p:>9.1f} {ratio_str:>6} {n:>3}")

    # Markdown report
    OUT_MD.parent.mkdir(parents=True, exist_ok=True)
    L = []
    A = L.append
    A("# Map predictions vs replay ground truth")
    A("")
    A("Сравнение модели `compute_map_resources.compute_counts(...)` с фактическими "
      "cluster counts из replay / save файлов "
      "(`docs/derived/replay_ground_truth.json`). Расшифровка значений "
      "`mapsize` / `relieftype` / `terraintype` / `season` — "
      "[`lobby_settings.md`](lobby_settings.md).")
    A("")
    A(f"**Replays processed:** {len(rows)}")
    A("")
    A("## Buckets")
    A("")
    A("Replays сгруппированы по `(mapsize, relieftype, terraintype, mask_kind)` — "
      "**только внутри одного bucket** калибровка имеет смысл (там одинаковые predictions). "
      "Cross-bucket averages могут оказаться ratio≈1.0 чисто случайно (Tiny занижено, Huge завышено — кросс-сумма ~ правде).")
    A("")
    A("| msz | rel | tt | mask | n_replays |")
    A("| --- | --- | --- | --- | ---: |")
    for key, brows in sorted_buckets:
        msz, rel, tt, mk = key
        rel_str = f"{rel}" + (" (Random)" if rel == 5 else "")
        A(f"| {msz} | {rel_str} | {tt} | `{mk}` | {len(brows)} |")
    A("")
    A(f"## Per-type calibration — LARGEST BUCKET (n={len(biggest[1])})")
    A("")
    A(f"Bucket: msz={biggest[0][0]} (Tiny=3, Normal=0, Large=1, Huge=2), "
      f"rel={biggest[0][1]} (Highlands=3, Random=5), tt={biggest[0][2]} (Land=0), "
      f"mask=`{biggest[0][3]}`.")
    A("")
    A("| pattern_type | actual avg | predicted avg | ratio | n_replays |")
    A("| --- | ---: | ---: | ---: | ---: |")
    for t, a, p, ratio, n in bucket_summary:
        ratio_str = f"{ratio:.2f}" if ratio is not None else "—"
        warn = " ⚠" if (ratio is not None and (ratio < 0.5 or ratio > 2.0)) else ""
        A(f"| `{t}` | {a:.1f} | {p:.1f} | {ratio_str}{warn} | {n} |")
    A("")
    A("## Per-pattern-type calibration — MIXED (all replays)")
    A("")
    A("⚠ Усреднение через разные mapsizes/reliefs. Может маскировать per-setting bias. "
      "См. bucket выше.")
    A("")
    A("| pattern_type | actual avg | predicted avg | ratio | n_replays |")
    A("| --- | ---: | ---: | ---: | ---: |")
    for t, a, p, ratio, n in type_summary:
        ratio_str = f"{ratio:.2f}" if ratio is not None else "—"
        A(f"| `{t}` | {a:.1f} | {p:.1f} | {ratio_str} | {n} |")
    A("")
    A("## Per-replay detail")
    A("")
    A("Для каждой replay-выборки: settings + diff таблица. Pattern types с большими "
      "расхождениями отмечены ⚠. Имена опаковые (`Replay NN` назначены детерминированно по "
      "хешу содержимого — см. `parse_replay_aggregates.py`).")
    A("")
    # Sort replays by bucket key for stable output, then by mask + randkey for tie-break
    sorted_rows = sorted(rows, key=lambda r: (
        bucket_key(r["settings"]),
        r["settings"].get("maskname", ""),
        r["settings"].get("randkey1", 0),
    ))
    for r in sorted_rows:
        s = r["settings"]
        nrp = r["predicted"].get("_n_real_players", "?")
        sp = r["predicted"].get("_spcount", "?")
        A(f"### {r['id']}")
        A("")
        A(f"- mask: `{s.get('maskname', '?')}`")
        A(f"- mapsize={s.get('mapsize')}, relief={s.get('relieftype')}, "
          f"mines={s.get('resourcemines')}, terraintype={s.get('terraintype')}, "
          f"season={s.get('season')}")
        A(f"- inferred players: **{nrp}/{sp}** (from mng count, Land only)")
        A("")
        A("| pattern_type | actual | predicted | actual/pred |")
        A("| --- | ---: | ---: | ---: |")
        for t, (a, p, ratio) in sorted(r["diff"].items(), key=lambda x: -x[1][0]):
            if a == 0 and p == 0:
                continue
            ratio_str = f"{ratio:.2f}" if ratio is not None else "—"
            warn = " ⚠" if (ratio is not None and (ratio < 0.5 or ratio > 2.0)) else ""
            A(f"| `{t}` | {a} | {p} | {ratio_str}{warn} |")
        A("")

    OUT_MD.write_text("\n".join(L), encoding="utf-8")
    print(f"\nWrote {OUT_MD}")


if __name__ == "__main__":
    main()
