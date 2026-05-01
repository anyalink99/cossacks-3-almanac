"""Extract strings from cossacks.exe in two flavors:

1. Plain ASCII runs (>=4 printable chars, NUL or non-printable terminated).
2. Pascal ShortString-style (`<len_byte><len_byte chars of A-Za-z_0-9>`).
   Delphi RTTI stores class names, method names, and field names this way.

Output: derived/exe_strings.json with virtual-address (RVA) for each hit
so we can later cross-reference with PE sections / IDA / Ghidra.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

import pefile

EXE_PATH = Path(r"C:\Program Files (x86)\Steam\steamapps\common\Cossacks 3\cossacks.exe")
OUT_PATH = Path(__file__).resolve().parents[2] / "derived" / "exe_strings.json"

ASCII_RE = re.compile(rb"[\x20-\x7e]{4,}")
# Pascal ShortString class/identifier. Identifier chars only, length 1..63.
PASCAL_SHORTSTR_RE = re.compile(rb"([\x01-\x3f])([A-Za-z_][A-Za-z_0-9.]{0,62})")


def main() -> None:
    if not EXE_PATH.exists():
        print(f"exe not found: {EXE_PATH}", file=sys.stderr)
        sys.exit(1)

    pe = pefile.PE(str(EXE_PATH), fast_load=True)
    image_base = pe.OPTIONAL_HEADER.ImageBase
    print(f"image_base=0x{image_base:08x}")
    sections = []
    for s in pe.sections:
        name = s.Name.rstrip(b"\x00").decode("latin1")
        sections.append({
            "name": name,
            "vaddr": image_base + s.VirtualAddress,
            "vsize": s.Misc_VirtualSize,
            "raw_off": s.PointerToRawData,
            "raw_size": s.SizeOfRawData,
            "characteristics": s.Characteristics,
        })
        print(
            f"  {name:8s}  va=0x{image_base + s.VirtualAddress:08x}  vsize={s.Misc_VirtualSize:#x}  "
            f"raw=0x{s.PointerToRawData:08x}+{s.SizeOfRawData:#x}"
        )

    data = EXE_PATH.read_bytes()
    n = len(data)
    print(f"file size={n} bytes")

    # File-offset -> RVA helper.
    def file_to_rva(off: int) -> int | None:
        for s in pe.sections:
            start = s.PointerToRawData
            end = start + s.SizeOfRawData
            if start <= off < end:
                return image_base + s.VirtualAddress + (off - start)
        return None

    # Plain ASCII.
    ascii_hits = []
    for m in ASCII_RE.finditer(data):
        s = m.group(0).decode("latin1")
        rva = file_to_rva(m.start())
        if rva is None:
            continue
        ascii_hits.append((s, rva, m.start(), len(s)))
    print(f"ASCII strings: {len(ascii_hits)}")

    # Pascal ShortStrings — these are the Delphi RTTI class/method names.
    pascal_hits = []
    for m in PASCAL_SHORTSTR_RE.finditer(data):
        length_byte = m.group(1)[0]
        payload = m.group(2)
        # The length byte must equal the actual identifier length we matched.
        # Our regex captures up to 62 chars, but a real ShortString has the
        # exact length encoded. Trim payload to length_byte.
        if length_byte > len(payload):
            continue
        # Trim to the declared length so we don't over-match.
        text = payload[:length_byte].decode("latin1")
        if not text or len(text) < 3:
            continue
        rva = file_to_rva(m.start())
        if rva is None:
            continue
        # The "string" itself starts at length_byte +1 in file.
        pascal_hits.append((text, rva, m.start()))
    print(f"Pascal ShortStrings: {len(pascal_hits)}")

    # Collect unique Pascal class-like names (T*, F*, I*, E* — Delphi conventions).
    delphi_classes = sorted({
        t for t, _, _ in pascal_hits
        if len(t) >= 4 and t[0] in "TFIE" and t[1].isupper()
    })
    print(f"Delphi-style class names (T*/F*/I*/E*): {len(delphi_classes)}")

    out = {
        "exe": str(EXE_PATH),
        "image_base": image_base,
        "sections": sections,
        "ascii_strings": [
            {"text": t, "rva": f"0x{rva:08x}", "off": off, "len": ln}
            for t, rva, off, ln in ascii_hits
        ],
        "pascal_shortstrings": [
            {"text": t, "rva": f"0x{rva:08x}", "off": off}
            for t, rva, off in pascal_hits
        ],
        "delphi_class_names": delphi_classes,
    }
    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUT_PATH.write_text(json.dumps(out, indent=1, ensure_ascii=False), encoding="utf-8")
    print(f"wrote {OUT_PATH} ({OUT_PATH.stat().st_size/1024:.1f} KiB)")
    print()
    print("Sample Delphi class names:")
    for c in delphi_classes[:40]:
        print(f"  {c}")


if __name__ == "__main__":
    main()
