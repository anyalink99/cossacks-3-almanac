"""Extract Cossacks 3 UI icons and build the reader-facing entity catalog.

The game keeps the small unit, building, upgrade, and order images in sprite
atlases.  ``data/hud/hud.mat`` is the authoritative mapping from material names
to atlas rectangles.  This script crops those rectangles and combines them with
the parsed gameplay data in ``data.json``.

The generated catalog is intentionally bilingual.  The documentation viewer
chooses the appropriate labels at runtime, so Russian and English cards always
describe the same underlying object.

Run:
    python scripts/build_entity_catalog.py

Override the installation path with ``COSSACKS3_PATH`` when necessary.
"""
from __future__ import annotations

import json
import re
import sys
from collections import defaultdict
from pathlib import Path
from typing import Any

from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "parser"))

from config import (  # noqa: E402
    BUILDING_NAMES_EN,
    BUILDING_NAMES_RU,
    DATA_JSON,
    GAME_ROOT,
    UNIT_NAMES_EN,
    UNIT_NAMES_RU,
    decode_upg_type,
    nation_en,
    nation_ru,
)

HUD_ROOT = GAME_ROOT / "data" / "hud"
HUD_MATERIALS = HUD_ROOT / "hud.mat"
ATLAS_ROOT = HUD_ROOT / "textures" / "ui"
ICON_ROOT = ROOT / "assets" / "game-icons"
CATALOG_PATH = ROOT / "assets" / "data" / "entity-catalog.json"
ENTITY_INDEX_PATHS = {
    "ru": ROOT / "assets" / "data" / "entity-index.ru.json",
    "en": ROOT / "assets" / "data" / "entity-index.en.json",
}

RESOURCE_KEYS = ("food", "wood", "stone", "gold", "iron", "coal")
PROTECTION_KEYS = (
    "prot_pike",
    "prot_sword",
    "prot_bullet",
    "prot_cannister",
    "prot_arrow",
    "prot_cannonball",
)


def parse_materials() -> dict[str, dict[str, Any]]:
    """Read active icon material blocks from ``hud.mat``."""

    if not HUD_MATERIALS.is_file():
        raise FileNotFoundError(
            f"Cossacks 3 HUD materials were not found at {HUD_MATERIALS}. "
            "Set COSSACKS3_PATH to the game installation directory."
        )
    text = HUD_MATERIALS.read_text(encoding="utf-8", errors="replace")
    # Commented experimental materials occur near the end of the file.  Strip
    # comment lines before block parsing so they cannot override live entries.
    text = re.sub(r"(?m)^\s*//.*$", "", text)
    materials: dict[str, dict[str, Any]] = {}
    for block in re.findall(r"section\.begin\b.*?section\.end", text, re.DOTALL):
        name_match = re.search(r"Material\.Name\s*=\s*([^\r\n]+)", block)
        atlas_match = re.search(r"Material\.LibTextureName\s*=\s*([^\r\n]+)", block)
        if not name_match or not atlas_match:
            continue
        name = name_match.group(1).strip()
        if not name.startswith(("icons.unit.", "icons.bld.", "icons.upg.", "icons.control.")):
            continue

        coords: dict[str, int] = {}
        for field in ("CoordX", "CoordY", "CoordW", "CoordH"):
            match = re.search(
                rf"Material\.TextureCoord\.{field}\s*=\s*(\d+)",
                block,
            )
            if not match:
                break
            coords[field] = int(match.group(1))
        if len(coords) != 4:
            continue
        materials[name] = {
            "atlas": atlas_match.group(1).strip(),
            "x": coords["CoordX"],
            "y": coords["CoordY"],
            "w": coords["CoordW"],
            "h": coords["CoordH"],
        }
    return materials


def safe_icon_name(material_name: str) -> str:
    value = material_name.split(".", 2)[-1]
    value = value.replace("%", "")
    value = re.sub(r"[^a-zA-Z0-9._-]+", "-", value)
    value = re.sub(r"-+", "-", value).strip("-")
    return f"{value}.png"


def extract_icons(materials: dict[str, dict[str, Any]]) -> dict[str, str]:
    """Crop all reader-relevant materials and return material → web path."""

    atlases: dict[str, Image.Image] = {}
    web_paths: dict[str, str] = {}
    category_dirs = {
        "unit": "units",
        "bld": "buildings",
        "upg": "upgrades",
        "control": "orders",
    }
    for material_name, material in sorted(materials.items()):
        category = material_name.split(".")[1]
        output_dir = ICON_ROOT / category_dirs[category]
        output_dir.mkdir(parents=True, exist_ok=True)
        atlas_name = material["atlas"]
        if atlas_name not in atlases:
            atlas_path = ATLAS_ROOT / f"{atlas_name}.bmp"
            if not atlas_path.is_file():
                raise FileNotFoundError(f"Icon atlas is missing: {atlas_path}")
            atlases[atlas_name] = Image.open(atlas_path).convert("RGB")
        atlas = atlases[atlas_name]
        x, y, w, h = (material[key] for key in ("x", "y", "w", "h"))
        if x + w > atlas.width or y + h > atlas.height:
            raise ValueError(
                f"{material_name} rectangle {(x, y, w, h)} exceeds "
                f"{atlas_name} size {atlas.size}"
            )
        output = output_dir / safe_icon_name(material_name)
        atlas.crop((x, y, x + w, y + h)).save(output, optimize=True)
        web_paths[material_name] = (
            "../assets/game-icons/"
            f"{category_dirs[category]}/{output.name}"
        )
    for atlas in atlases.values():
        atlas.close()
    return web_paths


def compact_dict(row: dict[str, Any], keys: tuple[str, ...]) -> dict[str, Any]:
    return {
        key: row[key]
        for key in keys
        if row.get(key) not in (None, "", [], {}, 0)
    }


def cost(row: dict[str, Any]) -> dict[str, int | float]:
    return {
        key: row[key]
        for key in RESOURCE_KEYS
        if row.get(key) not in (None, 0)
    }


def localized_name(
    rows: list[dict[str, Any]],
    sid: str,
    category: str,
) -> dict[str, str]:
    if category == "unit":
        ru = UNIT_NAMES_RU.get(sid)
        en = UNIT_NAMES_EN.get(sid)
    else:
        suffix = next(
            (
                suffix
                for suffix in sorted(BUILDING_NAMES_RU, key=len, reverse=True)
                if sid.endswith(suffix)
            ),
            "",
        )
        ru = BUILDING_NAMES_RU.get(suffix)
        en = BUILDING_NAMES_EN.get(suffix)
    ru = ru or next(
        (str(row.get("name_ru") or "").strip() for row in rows if row.get("name_ru")),
        sid,
    )
    en = en or next(
        (str(row.get("name_en") or "").strip() for row in rows if row.get("name_en")),
        sid,
    )
    return {"ru": ru, "en": en}


def unit_icon(sid: str, icons: dict[str, str]) -> str | None:
    candidates = [sid]
    if sid.endswith("dip"):
        candidates.append(sid.removesuffix("dip"))
    for candidate in candidates:
        path = icons.get(f"icons.unit.{candidate}")
        if path:
            return path
    return icons.get("icons.unit.empty")


def building_icon(sid: str, icons: dict[str, str]) -> str | None:
    exact = icons.get(f"icons.bld.{sid}")
    if exact:
        return exact
    suffixes = [
        name.removeprefix("icons.bld.")
        for name in icons
        if name.startswith("icons.bld.")
    ]
    for suffix in sorted(suffixes, key=len, reverse=True):
        if sid.endswith(suffix):
            return icons[f"icons.bld.{suffix}"]
    return icons.get("icons.bld.com")


def upgrade_pattern_regex(pattern: str) -> re.Pattern[str]:
    escaped = re.escape(pattern.removeprefix("icons.upg."))
    escaped = escaped.replace(re.escape("%nat%"), r"[a-z]+")
    escaped = escaped.replace(re.escape("%com%"), r"[a-z]+")
    escaped = escaped.replace(re.escape("%member%"), r"[a-z0-9.]+?")
    escaped = escaped.replace(re.escape("%num%"), r"\d+")
    return re.compile(f"^{escaped}$")


def upgrade_icon_resolver(icons: dict[str, str]):
    patterns = [
        (upgrade_pattern_regex(name), path)
        for name, path in icons.items()
        if name.startswith("icons.upg.") and not name.endswith(".old")
    ]

    def resolve(sid: str) -> str | None:
        return next((path for pattern, path in patterns if pattern.match(sid)), None)

    return resolve


def grouped_variants(
    rows: list[dict[str, Any]],
    variant_builder,
) -> list[dict[str, Any]]:
    grouped: dict[str, dict[str, Any]] = {}
    nations: dict[str, set[str]] = defaultdict(set)
    for row in rows:
        variant = variant_builder(row)
        signature = json.dumps(variant, ensure_ascii=False, sort_keys=True)
        grouped[signature] = variant
        nations[signature].add(str(row.get("nation") or ""))
    result = []
    for signature, variant in grouped.items():
        item = dict(variant)
        item["nations"] = sorted(value for value in nations[signature] if value)
        result.append(item)
    return sorted(result, key=lambda value: (value["nations"], json.dumps(value, sort_keys=True)))


def unit_variant(row: dict[str, Any]) -> dict[str, Any]:
    weapons = []
    for weapon in row.get("weapons") or []:
        weapons.append(
            compact_dict(
                weapon,
                (
                    "kind",
                    "damage",
                    "pause_sec",
                    "radiusmin_tiles",
                    "radiusmax_tiles",
                    "dispertion_tiles",
                    "cost",
                ),
            )
        )
    result: dict[str, Any] = compact_dict(
        row,
        ("hp", "buildtime_sec", "speed", "vision", "shield", "transport"),
    )
    if row.get("trained_in"):
        result["trained_in"] = sorted(set(row["trained_in"]))
    if cost_value := cost(row):
        result["cost"] = cost_value
    if protection := compact_dict(row, PROTECTION_KEYS):
        result["protection"] = protection
    if weapons:
        result["weapons"] = weapons
    return result


def building_variant(row: dict[str, Any]) -> dict[str, Any]:
    result: dict[str, Any] = compact_dict(
        row,
        (
            "hp",
            "buildtime_sec",
            "vision",
            "capturable",
            "farm",
            "peasantabsorber",
            "weapon_damage",
            "weapon_pause_frames",
            "weapon_radiusmax",
            "weapon_kind",
        ),
    )
    if cost_value := cost(row):
        result["cost"] = cost_value
    if row.get("produces"):
        result["produces"] = sorted(set(row["produces"]))
    if row.get("resourcebase"):
        result["resourcebase"] = sorted(set(row["resourcebase"]))
    return result


def upgrade_member(row: dict[str, Any]) -> str | None:
    if row.get("member"):
        return str(row["member"])
    match = re.match(
        r"^[a-z0-9]+\.([a-z0-9]+)\.([12])\.\d+$",
        str(row.get("sid") or ""),
    )
    return match.group(1) if match else None


def upgrade_name(
    row: dict[str, Any],
    lang: str,
    unit_names: dict[str, str],
) -> str:
    member = upgrade_member(row)
    match = re.search(r"\.([12])\.(\d+)$", str(row.get("sid") or ""))
    if member and match:
        effect = {
            ("ru", "1"): "урон",
            ("ru", "2"): "защита",
            ("en", "1"): "damage",
            ("en", "2"): "protection",
        }[(lang, match.group(1))]
        level_word = "уровень" if lang == "ru" else "level"
        member_name = unit_names.get(member, member)
        value = row.get("value")
        value_text = f"+{value}" if isinstance(value, (int, float)) and value >= 0 else str(value)
        return f"{member_name}: {effect} {value_text} ({level_word} {row.get('level')})"
    field = "name_ru" if lang == "ru" else "name_en"
    name = str(row.get(field) or row.get("name_en") or row.get("sid") or "").strip()
    value = row.get("value")
    return name.replace("%value%", str(value if value is not None else ""))


def upgrade_variant(row: dict[str, Any]) -> dict[str, Any]:
    effect_ru, _ = decode_upg_type(row.get("itype"), lang="ru")
    effect_en, effect_description_en = decode_upg_type(row.get("itype"), lang="en")
    result: dict[str, Any] = compact_dict(
        row,
        ("level", "value", "time_sec"),
    )
    result["effect"] = {
        "ru": effect_ru or "—",
        "en": effect_en or "—",
    }
    if effect_description_en:
        result["effect"]["description_en"] = effect_description_en
    for key in ("place", "member"):
        if row.get(key):
            result[key] = row[key]
    for key in ("targets", "prereqs"):
        if row.get(key):
            result[key] = sorted(set(row[key]))
    if cost_value := cost(row):
        result["cost"] = cost_value
    if row.get("resource_pcts"):
        result["resource_pcts"] = row["resource_pcts"]
    return result


def build_catalog(icons: dict[str, str]) -> dict[str, Any]:
    data = json.loads(DATA_JSON.read_text(encoding="utf-8"))
    by_kind: dict[str, dict[str, list[dict[str, Any]]]] = {}
    for kind, source_key in (
        ("unit", "units"),
        ("building", "buildings"),
        ("upgrade", "upgrades"),
    ):
        grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
        for row in data[source_key]:
            grouped[str(row["sid"])].append(row)
        by_kind[kind] = grouped

    entities: dict[str, dict[str, Any]] = {
        "unit": {},
        "building": {},
        "upgrade": {},
    }
    for sid, rows in sorted(by_kind["unit"].items()):
        entities["unit"][sid] = {
            "kind": "unit",
            "sid": sid,
            "name": localized_name(rows, sid, "unit"),
            "icon": unit_icon(sid, icons),
            "variants": grouped_variants(rows, unit_variant),
        }
    for sid, rows in sorted(by_kind["building"].items()):
        entities["building"][sid] = {
            "kind": "building",
            "sid": sid,
            "name": localized_name(rows, sid, "building"),
            "icon": building_icon(sid, icons),
            "variants": grouped_variants(rows, building_variant),
        }

    resolve_upgrade_icon = upgrade_icon_resolver(icons)
    for sid, rows in sorted(by_kind["upgrade"].items()):
        representative = rows[0]
        entities["upgrade"][sid] = {
            "kind": "upgrade",
            "sid": sid,
            "name": {
                "ru": upgrade_name(representative, "ru", UNIT_NAMES_RU),
                "en": upgrade_name(representative, "en", UNIT_NAMES_EN),
            },
            "icon": resolve_upgrade_icon(sid),
            "variants": grouped_variants(rows, upgrade_variant),
        }

    nation_labels = {
        sid: {"ru": nation_ru(sid), "en": nation_en(sid)}
        for sid in sorted({row["nation"] for rows in by_kind["unit"].values() for row in rows})
    }
    return {
        "schema": 1,
        "source": "Cossacks 3 game UI and parsed gameplay data",
        "counts": {kind: len(values) for kind, values in entities.items()},
        "nations": nation_labels,
        "entities": entities,
    }


def build_entity_index(
    catalog: dict[str, Any],
    language: str,
) -> dict[str, Any]:
    """Build the compact lookup loaded on Markdown pages with entity tables."""

    entities: dict[str, list[str]] = {}
    for kind, records in catalog["entities"].items():
        for sid, entity in records.items():
            if sid in entities:
                raise ValueError(f"entity SID is not unique across kinds: {sid}")
            entities[sid] = [kind, entity["name"][language], entity["icon"]]
    return {
        "schema": 1,
        "source": catalog["source"],
        "language": language,
        "count": len(entities),
        "entities": entities,
    }


def main() -> None:
    materials = parse_materials()
    icons = extract_icons(materials)
    catalog = build_catalog(icons)
    CATALOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    CATALOG_PATH.write_text(
        json.dumps(catalog, ensure_ascii=False, separators=(",", ":")) + "\n",
        encoding="utf-8",
    )
    entity_indexes = {
        language: build_entity_index(catalog, language)
        for language in ENTITY_INDEX_PATHS
    }
    for language, path in ENTITY_INDEX_PATHS.items():
        path.write_text(
            json.dumps(
                entity_indexes[language],
                ensure_ascii=False,
                separators=(",", ":"),
            )
            + "\n",
            encoding="utf-8",
        )
    print(
        f"wrote {CATALOG_PATH.relative_to(ROOT)} with "
        + ", ".join(
            f"{count} {kind}s"
            for kind, count in catalog["counts"].items()
        )
        + ", compact RU/EN table indexes with "
        + f"{entity_indexes['ru']['count']} entries each, and "
        + f"{len(icons)} extracted icons"
    )


if __name__ == "__main__":
    main()
