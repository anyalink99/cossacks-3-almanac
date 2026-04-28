"""Parser for Cossacks 3 .pattern files (data/pattern/*.pattern).

The .pattern format describes "stamps" the map generator drops on the world:
forests, brush patches, rocks, hills, ravines, etc.  Reverse-engineered from
the binary by comparing many files of varying size against the engine's
exposed accessors (`GetPatternMaskWidth/Height/Value`, `GetPatternOffsetX/Z`).

Layout (all little-endian):

    offset  bytes              meaning
    ------  -----------------  ---------------------------------------
    0       u32 width          mask width  (in tile corners)
    4       u32 height         mask height (in tile corners)
    8       u8 * cells         placement mask, row-major; 1 = "object
                               occupies this corner", 0 = empty
    8+C     f32 * w*h          heightmap, row-major (per-tile heights;
                               default value 3.20349 ≈ baseline)
    ...     u8 * 4             4 zero-pad bytes
    ...     rec * cells        24-byte per-corner record:
                                 u32  variant_id (1..255 random-ish;
                                                   used to pick tree
                                                   variant / rotation)
                                 f32  scale_x  (≈ 1.0 default)
                                 f32  scale_y  (≈ 1.0)
                                 f32  scale_z  (≈ 1.0)
                                 f32  ?       (≈ 1.0)
                                 u32  flags    (= 0 in every shipped file)
    ...     u8 * cells * 16    reserved-zero block (16 bytes per corner;
                               populated only when the pattern is hand-
                               edited in the editor — empty in shipped
                               files).
    ...     u8 * cells * 13    secondary-record block — every record is
                               `00 00 00 00 00 00 00 00 00 00 ff ff 00`,
                               i.e. ten zero bytes + an `0xFFFF` sentinel
                               + one zero. Acts as a delimiter array; not
                               useful for object counting.

    cells  = (width - 1) * (height - 1)

So total file size is exactly:

    8 + cells + w*h*4 + cells*53

This formula is verified against every .pattern in `data/pattern/`.

Object count
------------
The `mask` array (one byte per corner, value 0/1) IS the placement layout.
For forest patterns each `mask[i]==1` is one tree slot; for brush patterns
each is one bush.  This matches the engine's `GetPatternMaskValue(name,i,j)`
accessor that the LUA scripts call when stamping patterns onto the world.

The 24-byte per-corner record stores per-tree randomness (variant id /
rotation) but is present for **every** corner regardless of mask value, so
it cannot be used to discriminate "tree vs empty" — the mask is what
matters.
"""

from __future__ import annotations

import struct
from dataclasses import dataclass, field
from pathlib import Path
from typing import List


@dataclass
class PatternRecord:
    cell_x: int
    cell_y: int
    variant_id: int
    scale: tuple[float, float, float, float]


@dataclass
class Pattern:
    name: str
    width: int                       # mask corners along X
    height: int                      # mask corners along Y
    file_size: int
    mask: List[List[bool]]           # [y][x], len = (h-1)*(w-1) cells
    heightmap: List[List[float]]     # [y][x], w*h floats
    objects: List[PatternRecord] = field(default_factory=list)

    @property
    def occupied_cells(self) -> int:
        return sum(1 for row in self.mask for v in row if v)

    @property
    def object_count(self) -> int:
        return self.occupied_cells

    @property
    def cells(self) -> int:
        return (self.width - 1) * (self.height - 1)


def parse_pattern(path: str | Path) -> Pattern:
    """Read a .pattern file and decode every section.

    Raises ValueError if the file size doesn't match the layout we expect.
    """
    p = Path(path)
    data = p.read_bytes()
    fs = len(data)

    if fs < 8:
        raise ValueError(f"{p.name}: file too short ({fs} bytes)")

    width, height = struct.unpack_from("<II", data, 0)
    if width <= 0 or height <= 0 or width > 4096 or height > 4096:
        raise ValueError(
            f"{p.name}: implausible dimensions {width}x{height}"
        )

    cells = (width - 1) * (height - 1)
    expected_fs = 8 + cells + width * height * 4 + cells * 53

    if fs != expected_fs:
        raise ValueError(
            f"{p.name}: size mismatch (got {fs}, expected {expected_fs} "
            f"for {width}x{height}; cells={cells})"
        )

    # 1. Mask
    mask_offset = 8
    mask_bytes = data[mask_offset : mask_offset + cells]
    # Mask is stored row-major over (h-1) rows of (w-1) corners each.
    mw, mh = width - 1, height - 1
    mask: List[List[bool]] = []
    for y in range(mh):
        row = [bool(mask_bytes[y * mw + x]) for x in range(mw)]
        mask.append(row)

    # 2. Heightmap (w*h floats)
    hm_offset = mask_offset + cells
    heightmap: List[List[float]] = []
    for y in range(height):
        row_floats = struct.unpack_from(
            f"<{width}f", data, hm_offset + y * width * 4
        )
        heightmap.append(list(row_floats))

    # 3. Per-corner records (24 bytes each; cells of them; preceded by 4 zero bytes)
    rec_section_off = hm_offset + width * height * 4 + 4
    objects: List[PatternRecord] = []
    for idx in range(cells):
        o = rec_section_off + idx * 24
        variant_id, sx, sy, sz, sw = struct.unpack_from("<Iffff", data, o)
        cy, cx = divmod(idx, mw)
        if mask[cy][cx]:
            objects.append(
                PatternRecord(
                    cell_x=cx,
                    cell_y=cy,
                    variant_id=variant_id,
                    scale=(sx, sy, sz, sw),
                )
            )

    return Pattern(
        name=p.stem,
        width=width,
        height=height,
        file_size=fs,
        mask=mask,
        heightmap=heightmap,
        objects=objects,
    )


def parse_pattern_summary(path: str | Path) -> dict:
    """Cheap summary parser — skips full mask/heightmap/object decoding."""
    p = Path(path)
    data = p.read_bytes()
    fs = len(data)
    if fs < 8:
        return {
            "name": p.stem,
            "file_size": fs,
            "valid": False,
            "error": "file_too_short",
        }
    width, height = struct.unpack_from("<II", data, 0)
    cells = (width - 1) * (height - 1)
    expected_fs = 8 + cells + width * height * 4 + cells * 53

    if width <= 0 or height <= 0 or fs != expected_fs:
        return {
            "name": p.stem,
            "file_size": fs,
            "width": width,
            "height": height,
            "valid": False,
            "error": "size_mismatch",
            "expected_size": expected_fs,
        }

    mask_bytes = data[8 : 8 + cells]
    occupied = sum(1 for b in mask_bytes if b)

    return {
        "name": p.stem,
        "file_size": fs,
        "width": width,
        "height": height,
        "cells": cells,
        "occupied_cells": occupied,
        "object_count": occupied,
        "valid": True,
    }


# ---------------------------------------------------------------------------
# CLI / smoke test
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    import sys

    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from config import GAME_ROOT  # type: ignore

    pattern_dir = GAME_ROOT / "data" / "pattern"

    samples = [
        "brush_plt_1x1.pattern",
        "d_frt_small_1.pattern",
        "d_frt_mid_1.pattern",
        "d_frt_big_1.pattern",
    ]

    for fn in samples:
        try:
            pat = parse_pattern(pattern_dir / fn)
            print(
                f"{fn:30s}  {pat.width:>3}x{pat.height:<3}  "
                f"size={pat.file_size:>7}  "
                f"cells={pat.cells:>5}  objects={pat.object_count:>4}"
            )
        except Exception as exc:  # noqa: BLE001
            print(f"{fn}: ERROR {exc}")
