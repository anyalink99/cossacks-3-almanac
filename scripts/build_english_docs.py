"""Build and verify the English documentation mirror.

The committed English files are normal Markdown, so readers and GitHub Pages
never depend on a translation service. This script is only a maintainer tool:

    python scripts/build_english_docs.py --check  # verify coverage/freshness
    python scripts/build_english_docs.py --adopt-existing
    python scripts/build_english_docs.py --capture-fenced-translations

Canonical game labels are substituted from ``canonical_terms.json`` and
``data.json`` before prose is translated. Code, link destinations, and HTML
tags are preserved. Author-written diagrams, tables, and pseudocode inside
fences use the committed manual translations in
``manual_fenced_translations.json``; literal game data can be explicitly
marked as such. The translation source hashes are committed in
``translation_sources.json`` so CI can detect stale mirrors.
"""
from __future__ import annotations

import argparse
import collections
import hashlib
import html
import json
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Callable


if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parent.parent
MANIFEST_PATH = ROOT / "translation_sources.json"
MANUAL_FENCES_PATH = ROOT / "manual_fenced_translations.json"
TRANSLATE_URL = "https://translate.googleapis.com/translate_a/single"
TRANSLATION_ENGINE = "google"
CYRILLIC_RE = re.compile(r"[\u0400-\u04ff]")
FENCE_RE = re.compile(r"^\s*(```|~~~)")
HEADING_RE = re.compile(r"^(#{1,6})\s+(.+?)\s*$")
INLINE_CODE_RE = re.compile(r"`[^`\r\n]+`")
LINK_TARGET_RE = re.compile(r"(?<=\]\()[^)]+(?=\))")
HTML_TAG_RE = re.compile(r"</?[^>\r\n]+>")
URL_RE = re.compile(r"https?://[^\s)>]+")
FOOTNOTE_RE = re.compile(r"\[\^[^\]]+]")
MARKER_RE = re.compile(r"ZXQ[A-Z]+\d{5}QXZ")
PROTECTOR_ARTIFACT_RE = re.compile(r"\b(?:ZXQ|ZXX)[A-Z0-9]*\d+[A-Z0-9]*\b")
EXPLICIT_ID_LINE_RE = re.compile(
    r"\s*<(?:a|span)\s+[^>]*\bid=(?P<quote>[\"'])"
    r"(?P<id>[^\"']+)(?P=quote)[^>]*>\s*"
    r"</(?:a|span)>\s*",
    re.IGNORECASE,
)
MALFORMED_ATX_RE = re.compile(r"^#{1,6}[^#\s]")
MALFORMED_LINK_RE = re.compile(
    r"\]\s+\((?:\.{0,2}/|[A-Za-z0-9_.-]+/|"
    r"[A-Za-z0-9_.-]+\.(?:md|json|py|html)\b)"
)
TRUNCATION_MARKERS = (
    "tokens truncated",
    "characters truncated",
    "output truncated",
    "content omitted",
    "<snip>",
)
TRANSLATION_CLEANUPS = {
    "#Switzerland": "# Switzerland",
    "#Scotland": "# Scotland",
    "#Academies": "# Academies",
    "#Markets": "# Markets",
    "#Mills": "# Mills",
    "#Towers": "# Towers",
    "#Ships": "# Ships",
    "###Building from scratch": "### Building from scratch",
    "###Phase": "### Phase",
    "###Who can be captured as a unit": "### Who can be captured as a unit",
    "###Who's taking over": "### Who captures the unit",
    "###Cannons": "### Cannons",
    "Archerand": "Archers",
    "Drummer, 17th centuryand pipers": "Drummers and pipers",
    "Roster size and Mythic access": "Roster size and access to the 18th century",
    "| Combat | Strelkov | Cavalry |": "| Combat | Ranged units | Cavalry |",
    "`mapsize` - card size": "`mapsize` — map size",
    "The card size is square": "The map is square",
    "`gamespeed` - batch speed": "`gamespeed` — game speed",
    "Urban centers (cen)": "Town Halls (cen)",
    "Forges (bla)": "Blacksmiths (bla)",
    "Barracks 17th century. (bar)": "17th-century Barracks (bar)",
    "Barracks 18th century. (ba2)": "18th-century Barracks (ba2)",
    "**eng** Russia": "**Russia** (`rus`)",
    "| `chaika` | Yacht |": "| **Chaika** `chaika` | Yacht |",
    "### Shared cluster (": "### Shared buildings (",
    "game secondsы": "game seconds",
    "game secondsа": "game seconds",
    "game secondы": "game seconds",
    "Officerы": "Officers",
    "Archer и": "Archers",
    "Archerа": "Archer",
    "Frigateа": "Frigate",
    "Hetmanа": "Hetman",
    "Housingа": "Housing",
    "Storehouseы": "Storehouses",
    "Janissaryы": "Janissaries",
    "Mamelukeи": "Mamelukes",
    "Shipyardа": "Shipyard",
    "Shipyardы": "Shipyards",
    "Cathedralы": "Cathedrals",
    "Bazaarы": "Markets",
    "Mediumе `attack0`": "Average `attack0`",
    "Poorе HP": "Low HP",
    "`pathfinding`'у**": "`pathfinding`**",
    "[Sources](#источники)": "[Sources](#sources)",
    "[Sources] section (#источники)": "[Sources](#sources) section",
    "[Sources] section(#источники)": "[Sources](#sources) section",
    "<скрипт>": "<script>",
    "<раздел>": "<section>",
    "<имя>": "<name>",
    "<тип>": "<type>",
    "<параметр>": "<parameter>",
    "Использует `gSoundManager": "Uses `gSoundManager",
    "score жертвы": "victim score",
    "`, вызывает `_misc_CheckEndGame`": "`, calls `_misc_CheckEndGame`",
    "` и `gc_LAN_GAME": "` and `gc_LAN_GAME",
    "Проверка вероятности через": "Probability check via",
    "+7 щит": "+7 armor",
    "+7 шит": "+7 armor",
    "+7 `щит`": "+7 `armor`",
    "+атакующий": "+attacker",
    "−цель": "−target",
    "g-сек": "game s",
    "g-минуты": "game minutes",
    "g-минуту": "game minute",
    "g-мин": "game min",
    "g-минут": "game min",
    "game minы": "game minutes",
    " попаданий": " hits",
    " тайла": " cells",
    "% юнитов": "% units",
    "%value% юнитов": "%value% units",
    "минус i=4 если Tiny": "minus i=4 when Tiny",
    "конкретный env-object class": "a specific env-object class",
    "Σ(апгрейды)": "Σ(upgrades)",
    "(оружие)": "(weapon)",
    "`оружие`": "`weapon`",
    "`все 21`": "`all 21`",
    "`комп.`": "`components`",
    "`метод`": "`method`",
    "`слоты`": "`slots`",
    "`Полуострова` / `Острова` / `Континенты`": "`Peninsulas` / `Islands` / `Continents`",
    '"имя_трека"': '"track_name"',
    "то есть `random`": "that is, `random`",
    "pid = индекс в этом отфильтрованном списке": "pid = index in this filtered list",
    "использует `_Stream_WriteByte": "uses `_Stream_WriteByte",
    "× 500)`. Probability check via `random < 0.05`": "× 500)`. Probability check: `random < 0.05`",
    "`+7 armor`": "`+7 armor`",
    "`+attacker`": "`+attacker`",
    "`−target`": "`−target`",
    "где `_misc_RandomInt": "where `_misc_RandomInt",
    "` и `threshold` зависит от": "` and `threshold` depends on",
    "The rows are grouped by `(sid, weapon)`": "Rows are grouped by `(sid, weapon)`",
    "**Reading:** bold - kills quickly (TTK <1 сек), курсивом — почти не убивает": "**Reading:** bold means a quick kill (TTK <1 sec); italics means almost no damage",
    "`Хил/такт × тики_в_секунду`": "`healing_per_tick × ticks_per_second`",
    "Стена `consume.stone`": "Wall segment `consume.stone`",
    "У сегмента стены `consume.stone`": "A wall segment has `consume.stone`",
    "`, после чего `_player_OrderUnitsToBuild`": "`, after which `_player_OrderUnitsToBuild`",
    "(sid, оружие)": "(sid, weapon)",
    "gold/г-сек": "gold/game s",
    ". То есть `random`": ". That is, `random`",
    "| Unit | nations | HP | Time (g-sec) | F | G | I | damage | far (tile) | recharge | peak | sword | bullet | buckshot | arrow | core |":
        "| Unit | Nations | Health | Training time, game s | Food | Gold | Iron | Damage | Range, cells | Reload, s | Pike | Sword | Bullet | Grapeshot | Arrow | Cannonball |",
    "| Unit | Nation | HP | Time (g-sec) | F | G | I | upkip F | upkip G | speed | damage | far (tile) | recharge (s) | peak | sword | bullet | buckshot | arrow | core | uniqueness |":
        "| Unit | Nation | Health | Training time, game s | Food | Gold | Iron | Food/game s | Gold/game s | Speed | Damage | Range, cells | Reload, s | Pike | Sword | Bullet | Grapeshot | Arrow | Cannonball | Availability |",
    "| Unit | Nation | HP | Time (g-sec) | F | G | I | upkeep F | upkip G | speed | damage | far (tile) | recharge (s) | peak | sword | bullet | buckshot | arrow | core | uniqueness |":
        "| Unit | Nation | Health | Training time, game s | Food | Gold | Iron | Food/game s | Gold/game s | Speed | Damage | Range, cells | Reload, s | Pike | Sword | Bullet | Grapeshot | Arrow | Cannonball | Availability |",
    "| Unit | Nation | Health | Time for hiring, games. with | Food | Gold | Iron | Food/games. with | Gold/games. with | Speed | Damage | Range, cells | Reload, s | Pike | Sword | Bullet | Buckshot | Arrow | Core | Prevalence |":
        "| Unit | Nation | Health | Training time, game s | Food | Gold | Iron | Food/game s | Gold/game s | Speed | Damage | Range, cells | Reload, s | Pike | Sword | Bullet | Grapeshot | Arrow | Cannonball | Availability |",
    "| Unit | Sid | HP | Time (g-sec) | F | G | Heal/tact | Healing radius (tile) | Gold-upkeep (per tick = 1 game-sec) | Use nations |":
        "| Unit | Internal ID | Health | Training time (game s) | Food | Gold | Healing per update | Healing range (cells) | Gold upkeep (per game s) | Nations |",
    "| Building | Nation | HP | Time (g-sec) | cost% | W | S | G | farm | produces |":
        "| Building | Nation | Health | Construction time, game s | Price growth, % | Wood | Stone | Gold | Population | Produces |",
    "| Building | Nation | Health | Time for construction and games. with | Price growth, % | Wood | Stone | Gold | Population places | Produces |":
        "| Building | Nation | Health | Construction time, game s | Price growth, % | Wood | Stone | Gold | Population | Produces |",
    "| Building | Cluster | Resource | HP | Time (g-sec) | W | S | G | rate (per beat) | Add. workers |":
        "| Building | Architectural group | Resource | Health | Construction time, game s | Wood | Stone | Gold | Income value per worker | Initial worker slots |",
    "| weaponsid | kind | dmg | reload(s) | range(t) | cost (per shot) | Carrier units |":
        "| Internal weapon ID | Damage type | Damage | Reload (s) | Range (cells) | Shot cost | Units |",
    "| HP % |": "| Health, % |",
    "| +field HP % |": "| Field capacity, % |",
    "| Upgrade | Nations | Effect | Value | Price change | Food | Wood | Stone | Gold | Iron | Coal | Time |":
        "| Upgrade | Nations | Effect | Value | Price change | Food | Wood | Stone | Gold | Iron | Coal | Research time, game s |",
}


def sha256(path: Path) -> str:
    """Hash text reproducibly regardless of checkout line endings."""
    normalized = path.read_bytes().replace(b"\r\n", b"\n").replace(b"\r", b"\n")
    return hashlib.sha256(normalized).hexdigest()


def translation_pairs() -> dict[Path, Path]:
    pairs: dict[Path, Path] = {}
    for source_root, target_root in (
        (ROOT / "docs", ROOT / "docs_en"),
        (ROOT / "internals", ROOT / "internals_en"),
    ):
        for source in source_root.rglob("*.md"):
            pairs[source] = target_root / source.relative_to(source_root)

    # Use a wildcard and compare the discovered filename case-insensitively.
    # ``rglob("README.md")`` changes behaviour between Windows and Linux for
    # the tracked lowercase ``reference/compare/readme.md``.
    for source in ROOT.rglob("*.md"):
        if source.name.casefold() != "readme.md":
            continue
        if any(part in {
            ".git", ".pytest_cache", ".codex_probe",
            ".venv", "venv", "node_modules", "test-results",
            "playwright-report",
            "docs", "docs_en", "internals", "internals_en",
        }
               for part in source.relative_to(ROOT).parts):
            continue
        target = source.with_name("README.en.md")
        pairs[source] = target

    pairs[ROOT / "CONTRIBUTING.md"] = ROOT / "CONTRIBUTING.en.md"
    return dict(sorted(pairs.items(), key=lambda item: item[0].as_posix()))


def canonical_dictionary() -> list[tuple[str, str]]:
    """Return longest-first canonical Russian → English labels."""
    labels: dict[str, str] = {}

    canonical = json.loads(
        (ROOT / "derived" / "canonical_terms.json").read_text(encoding="utf-8")
    )
    for category, values in canonical.items():
        if category.startswith("_") or not isinstance(values, dict):
            continue
        for value in values.values():
            if not isinstance(value, dict):
                continue
            ru = str(value.get("ru") or "").strip()
            en = str(value.get("en") or "").strip()
            if ru and en and ru != en:
                labels.setdefault(ru, en)

    data = json.loads((ROOT / "data.json").read_text(encoding="utf-8"))
    for category in ("nations", "buildings", "units", "upgrades"):
        values = data.get(category, [])
        if isinstance(values, dict):
            values = values.values()
        for value in values:
            if not isinstance(value, dict):
                continue
            ru = str(value.get("name_ru") or "").strip()
            en = str(value.get("name_en") or "").strip()
            if ru and en and ru != en:
                labels.setdefault(ru, en)

    # Game-facing terminology that is intentionally canonical even when a
    # generic translator would choose a synonym.
    labels.update({
        "игровая секунда": "game second",
        "игровые секунды": "game seconds",
        "игровых секунд": "game seconds",
        "время мира": "peace time",
        "переход в 18 век": "advance to the 18th century",
    })
    return sorted(labels.items(), key=lambda item: (-len(item[0]), item[0]))


def markdown_heading_text(text: str) -> str:
    """Return the text a rendered Markdown heading exposes to the DOM."""

    protected_code: dict[str, str] = {}

    def preserve_code(match: re.Match[str]) -> str:
        marker = f"\x00CODE{len(protected_code)}\x00"
        protected_code[marker] = match.group(1)
        return marker

    value = re.sub(r"`([^`\n]+)`", preserve_code, text)
    value = re.sub(r"!\[([^\]]*)\]\([^)]+\)", r"\1", value)
    value = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", value)
    value = re.sub(r"<[^>]+>", "", value)
    # Remove Markdown emphasis delimiters, but keep literal underscores exposed
    # by the rendered heading (for example ``state_id`` or ``game_object``).
    value = re.sub(r"(\*\*|__)(?=\S)(.+?)(?<=\S)\1", r"\2", value)
    value = re.sub(
        r"(?<![\w\\])([*_])(?=\S)(.+?)(?<=\S)\1(?!\w)",
        r"\2",
        value,
    )
    value = re.sub(r"~~(?=\S)(.+?)(?<=\S)~~", r"\1", value)
    for marker, code_text in protected_code.items():
        value = value.replace(marker, code_text)
    return html.unescape(value)


def github_slug(text: str) -> str:
    value = markdown_heading_text(text).strip().lower()
    value = re.sub(r"[^\w\s-]", "", value, flags=re.UNICODE)
    return re.sub(r"\s", "-", value)


def _legacy_github_slug(text: str) -> str:
    """Return IDs emitted by the pre-rendered-text heading slugger.

    This intentionally retains the old parser's mistakes so existing bad
    aliases can be identified and migrated without guessing from their shape.
    """

    value = re.sub(r"<[^>]+>", "", text)
    value = re.sub(r"[`*_~]", "", value).strip().lower()
    value = re.sub(r"[^\w\s-]", "", value, flags=re.UNICODE)
    return value.replace(" ", "-")


class Protector:
    def __init__(self, canonical: list[tuple[str, str]]) -> None:
        self.canonical = canonical
        self.restore: dict[str, str] = {}
        self.counter = 0

    def marker(self, kind: str, value: str) -> str:
        token = f"ZXQ{kind}{self.counter:05d}QXZ"
        self.counter += 1
        self.restore[token] = value
        return token

    def protect(self, text: str) -> str:
        def preserve(pattern: re.Pattern[str], kind: str, value: str) -> str:
            return pattern.sub(lambda m: self.marker(kind, m.group(0)), value)

        text = preserve(INLINE_CODE_RE, "CODE", text)
        text = preserve(LINK_TARGET_RE, "LINK", text)
        text = preserve(HTML_TAG_RE, "HTML", text)
        text = preserve(URL_RE, "URL", text)
        text = preserve(FOOTNOTE_RE, "NOTE", text)
        for ru, en in self.canonical:
            if ru in text:
                text = text.replace(ru, self.marker("TERM", en))
        return text

    def unprotect(self, text: str) -> str:
        for marker, value in reversed(self.restore.items()):
            shortened = marker[:-1]
            full_count = text.count(marker)
            shortened_count = text.count(shortened)
            if full_count == 0 and shortened_count == 1:
                text = text.replace(shortened, marker)
                full_count = 1
            if full_count != 1:
                raise RuntimeError(
                    f"translation changed protected marker {marker}: "
                    f"expected once, found {full_count}"
                )
            text = text.replace(marker, value, 1)
        artifacts = PROTECTOR_ARTIFACT_RE.findall(text)
        if artifacts:
            raise RuntimeError(
                f"translation returned unknown markers: {artifacts[:3]}"
            )
        return text


def translate_request(text: str, attempts: int = 6) -> str:
    if not CYRILLIC_RE.search(text):
        return text
    if TRANSLATION_ENGINE == "argos":
        try:
            import argostranslate.translate
        except ImportError as error:
            raise RuntimeError(
                "Argos Translate is not installed. Install argostranslate and "
                "its Russian → English model, or use --engine google."
            ) from error
        return argostranslate.translate.translate(text, "ru", "en")
    payload = urllib.parse.urlencode({
        "client": "gtx",
        "sl": "ru",
        "tl": "en",
        "dt": "t",
        "q": text,
    }).encode("utf-8")
    request = urllib.request.Request(
        TRANSLATE_URL,
        data=payload,
        headers={"User-Agent": "Cossacks3Almanac/1.0"},
        method="POST",
    )
    for attempt in range(attempts):
        try:
            with urllib.request.urlopen(request, timeout=45) as response:
                result = json.loads(response.read().decode("utf-8"))
            return "".join(part[0] for part in result[0] if part and part[0])
        except (OSError, ValueError, urllib.error.HTTPError) as error:
            if attempt + 1 == attempts:
                raise RuntimeError(f"translation failed after {attempts} attempts") from error
            time.sleep(min(12, 1.5 ** attempt))
    raise AssertionError("unreachable")


def translate_chunk(text: str, canonical: list[tuple[str, str]]) -> str:
    protector = Protector(canonical)
    protected = protector.protect(text)
    translated = translate_request(protected)
    return protector.unprotect(translated)


def canonicalize_fenced_blocks(
    text: str,
    canonical: list[tuple[str, str]],
) -> str:
    """Use game-localized English labels inside diagrams and code samples."""
    output: list[str] = []
    in_fence = False
    for line in text.splitlines():
        if FENCE_RE.match(line):
            in_fence = not in_fence
            output.append(line)
            continue
        if in_fence:
            for russian, english in canonical:
                if russian in line:
                    line = line.replace(russian, english)
        output.append(line)
    return "\n".join(output) + ("\n" if text.endswith("\n") else "")


def fenced_blocks(text: str) -> list[tuple[int, str]]:
    """Return (opening line number, body) for every fenced Markdown block."""
    blocks: list[tuple[int, str]] = []
    body: list[str] = []
    start_line = 0
    in_fence = False
    for line_number, line in enumerate(text.splitlines(), start=1):
        if FENCE_RE.match(line):
            if in_fence:
                blocks.append((start_line, "\n".join(body)))
                body = []
            else:
                start_line = line_number
            in_fence = not in_fence
            continue
        if in_fence:
            body.append(line)
    return blocks


def fenced_block_key(body: str) -> str:
    return hashlib.sha256(body.encode("utf-8")).hexdigest()


def load_manual_fenced_translations() -> dict[str, dict[str, object]]:
    if not MANUAL_FENCES_PATH.is_file():
        return {}
    payload = json.loads(MANUAL_FENCES_PATH.read_text(encoding="utf-8"))
    return payload.get("blocks", {})


def apply_manual_fenced_translations(
    text: str,
    translations: dict[str, dict[str, object]],
) -> str:
    """Replace source fence bodies with their reviewed English equivalents."""
    if not translations:
        return text

    had_final_newline = text.endswith("\n")
    output: list[str] = []
    body: list[str] = []
    in_fence = False
    for line in text.splitlines():
        if not FENCE_RE.match(line):
            if in_fence:
                body.append(line)
            else:
                output.append(line)
            continue

        if not in_fence:
            output.append(line)
            body = []
            in_fence = True
            continue

        key = fenced_block_key("\n".join(body))
        entry = translations.get(key)
        if entry and not entry.get("literal"):
            replacement = entry.get("text")
            if not isinstance(replacement, str):
                raise ValueError(f"manual fence {key} has no translated text")
            output.extend(replacement.splitlines())
        else:
            output.extend(body)
        output.append(line)
        body = []
        in_fence = False

    if in_fence:
        output.extend(body)
    return "\n".join(output) + ("\n" if had_final_newline else "")


def capture_manual_fenced_translations(
    pairs: dict[Path, Path],
) -> dict[str, dict[str, object]]:
    """Capture reviewed target fences corresponding to Cyrillic source fences."""
    captured: dict[str, dict[str, object]] = {}
    for source, target in pairs.items():
        if not target.is_file():
            raise ValueError(f"missing translation: {target.relative_to(ROOT)}")
        source_blocks = fenced_blocks(source.read_text(encoding="utf-8"))
        target_blocks = fenced_blocks(target.read_text(encoding="utf-8"))
        if len(source_blocks) != len(target_blocks):
            raise ValueError(
                f"fence count differs for {source.relative_to(ROOT)}: "
                f"{len(source_blocks)} source, {len(target_blocks)} target"
            )
        source_rel = source.relative_to(ROOT).as_posix()
        for (line_number, source_body), (_, target_body) in zip(
            source_blocks,
            target_blocks,
        ):
            if not CYRILLIC_RE.search(source_body):
                continue
            key = fenced_block_key(source_body)
            literal = source_body == target_body
            existing = captured.get(key)
            translated_body = None if literal else target_body
            if existing and (
                existing.get("literal") != literal
                or existing.get("text") != translated_body
                or existing.get("literal_cyrillic")
                != bool(CYRILLIC_RE.search(target_body))
            ):
                raise ValueError(
                    f"one source fence has conflicting translations: "
                    f"{source_rel}:{line_number}"
                )
            if existing:
                sources = existing.setdefault("sources", [])
                assert isinstance(sources, list)
                sources.append(f"{source_rel}:{line_number}")
                continue
            captured[key] = {
                "literal": literal,
                "literal_cyrillic": bool(CYRILLIC_RE.search(target_body)),
                "text": translated_body,
                "sources": [f"{source_rel}:{line_number}"],
            }
    return captured


def write_manual_fenced_translations(
    translations: dict[str, dict[str, object]],
) -> None:
    payload = {
        "schema": 1,
        "note": (
            "Reviewed English replacements for author-written Cyrillic fenced "
            "blocks. Keys are SHA-256 hashes of the exact Russian fence body; "
            "literal=true preserves a whole genuine game-data block, while "
            "literal_cyrillic=true permits reviewed localization literals "
            "inside an otherwise translated block."
        ),
        "blocks": dict(sorted(translations.items())),
    }
    MANUAL_FENCES_PATH.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def _markdown_headings_with(
    text: str,
    slugger: Callable[[str], str],
) -> list[tuple[int, str, int]]:
    """Return (level, slug, line index) for headings outside fenced blocks."""
    headings: list[tuple[int, str, int]] = []
    used: set[str] = set()
    in_fence = False
    for index, line in enumerate(text.splitlines()):
        if FENCE_RE.match(line):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        match = HEADING_RE.match(line)
        if match:
            base = slugger(match.group(2))
            if not base:
                continue
            slug = base
            suffix = 1
            while slug in used:
                slug = f"{base}-{suffix}"
                suffix += 1
            used.add(slug)
            headings.append((len(match.group(1)), slug, index))
    return headings


def markdown_headings(text: str) -> list[tuple[int, str, int]]:
    return _markdown_headings_with(text, github_slug)


def _legacy_markdown_headings(text: str) -> list[tuple[int, str, int]]:
    return _markdown_headings_with(text, _legacy_github_slug)


def _aligned_heading_pairs(
    source_text: str,
    translated_text: str,
) -> list[tuple[tuple[int, str, int], tuple[int, str, int]]]:
    """Pair source and translated headings in document order.

    Normal mirrors have identical heading-level sequences and can be paired
    directly. The fallback tolerates extra translated headings at other
    levels without discarding the next unmatched source heading.
    """
    source_headings = markdown_headings(source_text)
    target_headings = markdown_headings(translated_text)
    if [level for level, _, _ in source_headings] == [
        level for level, _, _ in target_headings
    ]:
        return list(zip(source_headings, target_headings))

    pairs = []
    target_cursor = 0
    for source_heading in source_headings:
        source_level = source_heading[0]
        while (
            target_cursor < len(target_headings)
            and target_headings[target_cursor][0] != source_level
        ):
            target_cursor += 1
        if target_cursor >= len(target_headings):
            break
        pairs.append((source_heading, target_headings[target_cursor]))
        target_cursor += 1
    return pairs


def _standalone_explicit_id(line: str) -> str | None:
    """Return the ID when *line* contains only one explicit heading anchor."""
    match = re.fullmatch(r'\s*<a\s+id="([^"]+)"\s*></a>\s*', line)
    return match.group(1) if match else None


def _explicit_ids_outside_fences(text: str) -> list[str]:
    """Return standalone HTML anchor IDs exposed in the rendered DOM."""
    ids: list[str] = []
    in_fence = False
    for line in text.splitlines():
        if FENCE_RE.match(line):
            in_fence = not in_fence
            continue
        if not in_fence:
            match = EXPLICIT_ID_LINE_RE.fullmatch(line)
            if match:
                ids.append(match.group("id"))
    return ids


def _aliases_immediately_before_headings(text: str) -> dict[int, set[str]]:
    """Return standalone alias IDs attached to each heading line index."""
    lines = text.splitlines()
    attached: dict[int, set[str]] = {}
    for _, _, heading_line in markdown_headings(text):
        aliases: set[str] = set()
        cursor = heading_line - 1
        while cursor >= 0:
            alias = _standalone_explicit_id(lines[cursor])
            if alias is None:
                break
            aliases.add(alias)
            cursor -= 1
        attached[heading_line] = aliases
    return attached


def ensure_heading_aliases(source_text: str, translated_text: str) -> str:
    """Preserve Russian heading fragments as aliases in the English mirror."""
    heading_pairs = _aligned_heading_pairs(source_text, translated_text)
    if not heading_pairs:
        return translated_text

    target_heading_slugs = {
        slug for _, slug, _ in markdown_headings(translated_text)
    }
    movable_aliases = {
        source_slug
        for (_, source_slug, _), (_, target_slug, _) in heading_pairs
        if source_slug != target_slug and source_slug not in target_heading_slugs
    }
    current_source_slugs = {
        slug for _, slug, _ in markdown_headings(source_text)
    }
    legacy_source_slugs = {
        line: slug for _, slug, line in _legacy_markdown_headings(source_text)
    }
    obsolete_legacy_aliases = {
        legacy_source_slugs[source_line]
        for (source_level, source_slug, source_line), _ in heading_pairs
        if source_line in legacy_source_slugs
        and legacy_source_slugs[source_line] != source_slug
        and legacy_source_slugs[source_line] not in current_source_slugs
        and legacy_source_slugs[source_line] not in target_heading_slugs
    }
    removable_aliases = movable_aliases | obsolete_legacy_aliases

    had_final_newline = translated_text.endswith("\n")
    lines = [
        line
        for line in translated_text.splitlines()
        if _standalone_explicit_id(line) not in removable_aliases
    ]
    without_movable_aliases = "\n".join(lines) + (
        "\n" if had_final_newline else ""
    )
    heading_pairs = _aligned_heading_pairs(source_text, without_movable_aliases)
    existing_ids = set(
        re.findall(
            r'<a\s+id="([^"]+)"\s*></a>',
            without_movable_aliases,
        )
    )
    target_heading_slugs = {
        slug for _, slug, _ in markdown_headings(without_movable_aliases)
    }
    insertions: dict[int, list[str]] = {}
    for (_, source_slug, _), (_, target_slug, target_line) in heading_pairs:
        if (
            source_slug == target_slug
            or source_slug in target_heading_slugs
            or source_slug in existing_ids
        ):
            continue
        insertions.setdefault(target_line, []).append(
            f'<a id="{html.escape(source_slug)}"></a>'
        )
        existing_ids.add(source_slug)

    if not insertions:
        return without_movable_aliases
    output: list[str] = []
    for index, line in enumerate(without_movable_aliases.splitlines()):
        output.extend(insertions.get(index, ()))
        output.append(line)
    return "\n".join(output) + ("\n" if had_final_newline else "")


def translate_markdown(
    text: str,
    canonical: list[tuple[str, str]],
    manual_fences: dict[str, dict[str, object]] | None = None,
) -> str:
    """Translate Markdown in bounded chunks while preserving source syntax."""
    had_final_newline = text.endswith("\n")
    lines = text.splitlines()
    output: list[str] = []
    pending: list[str] = []
    pending_size = 0
    in_fence = False
    source_headings: list[tuple[int, str]] = []

    def flush() -> None:
        nonlocal pending, pending_size
        if not pending:
            return
        source = "\n".join(pending)
        translated = translate_chunk(source, canonical)
        translated_lines = translated.splitlines()

        # Google normally preserves line breaks, but it may occasionally fold
        # a prose paragraph. Heading aliases are only added when line counts
        # still match; file integrity does not depend on them.
        if len(translated_lines) == len(pending):
            for source_line, translated_line in zip(pending, translated_lines):
                match = HEADING_RE.match(source_line)
                translated_match = HEADING_RE.match(translated_line)
                if match and translated_match:
                    source_slug = github_slug(match.group(2))
                    translated_slug = github_slug(translated_match.group(2))
                    if source_slug and source_slug != translated_slug:
                        output.append(f'<a id="{html.escape(source_slug)}"></a>')
                output.append(translated_line)
        else:
            output.extend(translated_lines)
        pending = []
        pending_size = 0

    for line in lines:
        fence = FENCE_RE.match(line)
        if fence:
            flush()
            output.append(line)
            in_fence = not in_fence
            continue
        if in_fence:
            output.append(line)
            continue

        projected = pending_size + len(line) + 1
        if pending and projected > 3600:
            flush()
        pending.append(line)
        pending_size += len(line) + 1
    flush()

    result = "\n".join(output)
    # Canonical bilingual cells become duplicates after RU → EN substitution.
    result = re.sub(r"\*\*([^*\n]+)\*\*\s*/\s*\1(?=\s|·|$)", r"**\1**", result)
    result = re.sub(r"\b([^()\n]{2,60})\s+\(\1\)", r"\1", result)
    result = apply_manual_fenced_translations(result, manual_fences or {})
    result = canonicalize_fenced_blocks(result, canonical)
    result = clean_translation_artifacts(result)
    if had_final_newline:
        result += "\n"
    return result


def clean_translation_artifacts(text: str) -> str:
    text = text.replace("\u200b", "")
    for source, target in TRANSLATION_CLEANUPS.items():
        text = text.replace(source, target)
    return text


def clean_reader_report(text: str) -> str:
    """Keep generated report provenance out of the reader's opening screen."""
    text = re.sub(
        r"(?ms)^\*\*Derived[^\n]*\n(?:[^\n]*\n)*?\s*\n",
        "",
        text,
    )
    text = re.sub(
        r"(?m)^(?:---\s*\n\s*)?Regeneration:\s*`[^`\n]+`\.?\s*\n?",
        "",
        text,
    )
    if "[← Tables and calculations]" in text:
        return text

    lines = text.splitlines()
    for index, line in enumerate(lines):
        if re.match(r"^#\s+", line):
            lines[index + 1:index + 1] = [
                "",
                "[← Tables and calculations](../README.md)",
            ]
            break
    return "\n".join(lines) + ("\n" if text.endswith("\n") else "")


def canonicalize_reader_table_codes(text: str) -> str:
    """Expand bare nation codes in English reader-facing Markdown tables."""
    canonical = json.loads(
        (ROOT / "derived" / "canonical_terms.json").read_text(encoding="utf-8")
    )
    nation_names = {
        sid: str(names.get("en") or sid)
        for sid, names in (canonical.get("nations") or {}).items()
    }
    if not nation_names:
        return text

    code_list = re.compile(
        rf"(?:{'|'.join(map(re.escape, nation_names))})"
        rf"(?:\s*,\s*(?:{'|'.join(map(re.escape, nation_names))}))*"
    )
    had_final_newline = text.endswith("\n")
    output: list[str] = []
    in_fence = False
    for line in text.splitlines():
        if FENCE_RE.match(line):
            in_fence = not in_fence
            output.append(line)
            continue
        if in_fence or not line.startswith("|"):
            output.append(line)
            continue

        cells = line.split("|")
        for index in range(1, len(cells) - 1):
            value = cells[index].strip()
            nation_label = re.fullmatch(
                r"\*\*([a-z]{3})\*\*\s+[^|]+",
                value,
            )
            if nation_label and nation_label.group(1) in nation_names:
                sid = nation_label.group(1)
                cells[index] = f" **{nation_names[sid]}** (`{sid}`) "
                continue
            if not code_list.fullmatch(value):
                continue
            cells[index] = " " + ", ".join(
                nation_names[code.strip()] for code in value.split(",")
            ) + " "
        output.append("|".join(cells))
    return "\n".join(output) + ("\n" if had_final_newline else "")


def canonicalize_english_upgrade_names(text: str) -> str:
    """Replace generated mixed SID/English labels with canonical card names."""
    catalog_path = ROOT / "assets" / "data" / "entity-catalog.json"
    if not catalog_path.is_file():
        return text
    catalog = json.loads(catalog_path.read_text(encoding="utf-8"))
    names = {
        sid: str(entity.get("name", {}).get("en") or "").strip()
        for sid, entity in (
            catalog.get("entities", {}).get("upgrade", {}) or {}
        ).items()
    }
    names.update(
        {
            "eurswa.1": "Convert Stone Wall to Gate",
            "ukrwwa.1": "Convert Palisade to Gate",
        }
    )

    def replace(match: re.Match[str]) -> str:
        sid = match.group("sid")
        name = names.get(sid)
        if not name:
            return match.group(0)
        return f"**{name}** `{sid}`"

    text = re.sub(
        r"\*\*[^*\n]+\*\*\s+`(?P<sid>[a-z0-9.]+)`",
        replace,
        text,
    )

    def replace_bare(match: re.Match[str]) -> str:
        sid = match.group("sid")
        name = names.get(sid)
        if not name:
            return match.group(0)
        return f"| **{name}** `{sid}` |"

    return re.sub(
        r"^\|\s*`(?P<sid>[a-z0-9.]+)`\s*\|",
        replace_bare,
        text,
        flags=re.MULTILINE,
    )


def _is_markdown_table_separator(line: str) -> bool:
    """Return whether *line* is the separator immediately below a table header."""
    if not line.startswith("|") or not line.rstrip().endswith("|"):
        return False
    cells = line.split("|")[1:-1]
    return bool(cells) and all(
        re.fullmatch(r"\s*:?-{3,}:?\s*", cell) for cell in cells
    )


def clean_english_upgrade_table(text: str) -> str:
    """Replace generator labels with reader-facing English in upgrade tables."""
    effect_labels = {
        "build time %": "Construction time",
        "price %": "Price, %",
        "enable unit": "Unlocks unit",
        "+shield": "Durability / protection",
        "+food eff %": "Food gathering, %",
        "accuracy %": "Accuracy, %",
        "+damage %": "Damage, %",
        "+damage": "Damage",
        "single reload %": "Building reload, %",
        "range %": "Range, %",
        "healing": "Healing",
        "speed %": "Speed, %",
        "+fish eff %": "Fishing, %",
        "+stone eff %": "Stone gathering, %",
        "balloon": "Reveals map",
        "reload %": "Reload, %",
        "build gate": "Converts to gate",
        "geology": "Reveals deposits",
        "+wood eff %": "Wood gathering, %",
        "+building capacity": "Capacity",
    }
    lines = text.splitlines()
    effect_column: int | None = None
    value_column: int | None = None
    for line_index, line in enumerate(lines):
        if not line.startswith("|"):
            effect_column = None
            value_column = None
            continue
        cells = line.split("|")
        normalized = [cell.strip() for cell in cells]
        if (
            "Effect" in normalized
            and "Value" in normalized
            and line_index + 1 < len(lines)
            and _is_markdown_table_separator(lines[line_index + 1])
        ):
            effect_column = normalized.index("Effect")
            value_column = normalized.index("Value")
            continue
        if (
            effect_column is None
            or value_column is None
            or value_column >= len(cells) - 1
        ):
            continue
        raw_effect = cells[effect_column].strip()
        if raw_effect == "build time %":
            raw_value = cells[value_column].strip()
            if re.fullmatch(r"-?\d+", raw_value):
                percentage = int(raw_value) / 100_000
                formatted = f"{percentage:.4f}".rstrip("0").rstrip(".")
                cells[value_column] = f" {formatted}% "
        label = effect_labels.get(raw_effect)
        if label:
            cells[effect_column] = f" {label} "
            lines[line_index] = "|".join(cells)
    return "\n".join(lines) + ("\n" if text.endswith("\n") else "")


def canonicalize_english_unit_names(text: str) -> str:
    """Use the game's canonical English unit label before every preserved SID."""
    canonical = json.loads(
        (ROOT / "derived" / "canonical_terms.json").read_text(encoding="utf-8")
    )
    names = {
        sid: str(value.get("en") or "").strip()
        for sid, value in (canonical.get("units") or {}).items()
        if isinstance(value, dict)
    }
    names["unitbox"] = "Mission placeholder"

    def replace(match: re.Match[str]) -> str:
        sid = match.group("sid")
        name = names.get(sid)
        return f"**{name}** `{sid}`" if name else match.group(0)

    text = re.sub(
        r"\*\*[^*\n]+\*\*(?:\s*/\s*[^`|\n]+)?\s+`(?P<sid>[a-z0-9_]+)`",
        replace,
        text,
    )

    def replace_bare(match: re.Match[str]) -> str:
        sid = match.group("sid")
        name = names.get(sid)
        if not name:
            return match.group(0)
        return f"| **{name}** `{sid}` |"

    return re.sub(
        r"^\|\s*`(?P<sid>[a-z0-9_]+)`\s*\|",
        replace_bare,
        text,
        flags=re.MULTILINE,
    )


def canonicalize_english_reader_links(
    text: str,
    document_path: Path | None = None,
) -> str:
    """Give repository-path links ordinary reader-facing English labels."""
    labels = {
        "recon/world/combat/towers.md": "tower and garrison mechanics",
        "reference/05_upgrades/README.md": "upgrades",
        "05_upgrades/README.md": "upgrades",
        "reference/compare/README.md": "comparison index",
        "compare/README.md": "comparison index",
        "reference/compare/units/priests.md": "priest comparison",
        "internals_en/engine/ticks_and_subticks.md": "ticks and subticks",
        "recon/world/combat/target_selection.md": "target selection",
        "reference/07_naval/README.md": "Navy",
        "reports/combat/combat_stats.md": "combat statistics",
        "recon/world/combat/combat_damage_pipeline.md": "damage calculation",
        "recon/world/economy/hunger_and_rebellion.md": "hunger and rebellion",
        "recon/world/combat/ranged_units_behavior.md": "ranged-unit behavior",
        "recon/world/economy/building_mechanics.md": "construction and repair",
        "reports/economy/builder_slots.md": "builder limits",
        "reports/map/map_resources.md": "map resource estimates",
        "recon/world/map/map_generation_pipeline.md": "map generation",
        "recon/world/map/game_settings.md": "match settings",
        "recon/world/economy/capture_mechanics.md": "building capture",
        "recon/systems/mercenaries_diplomacy.md": "mercenaries and diplomacy",
        "recon/systems/ai_behavior.md": "computer-player behavior",
        "recon/world/economy/peasant_extraction.md": "peasant resource gathering",
        "reports/map/lobby_settings.md": "lobby settings",
        "reference/01_economy/README.md": "economy guide",
        "reference/03_buildings/README.md": "building guide",
        "reference/06_market/README.md": "market guide",
        "reports/economy/scaling_prices.md": "building price growth",
    }
    link_re = re.compile(r"\[([^\]\n]*\.md[^\]\n]*)\]\(([^)\n]+)\)")
    had_final_newline = text.endswith("\n")
    output: list[str] = []
    in_fence = False
    for line in text.splitlines():
        if FENCE_RE.match(line):
            in_fence = not in_fence
            output.append(line)
            continue
        if in_fence:
            output.append(line)
            continue

        def replace(match: re.Match[str]) -> str:
            target = urllib.parse.unquote(match.group(2)).split("#", 1)[0]
            normalized = target.replace("\\", "/").lstrip("./")
            visible = match.group(1).replace("`", "")
            friendly = None
            if document_path and not re.match(r"^[a-z]+:", target, re.I):
                linked_path = (document_path.parent / target).resolve()
                if linked_path.is_relative_to(ROOT) and linked_path.is_file():
                    for linked_line in linked_path.read_text(
                        encoding="utf-8"
                    ).splitlines():
                        heading = re.match(r"^#\s+(.+?)\s*$", linked_line)
                        if not heading:
                            continue
                        friendly = heading.group(1)
                        friendly = re.sub(
                            r"\[([^\]]+)\]\([^)]+\)", r"\1", friendly
                        )
                        friendly = friendly.replace("`", "").replace("*", "")
                        break
            if not friendly:
                friendly = next(
                    (
                        label
                        for suffix, label in labels.items()
                        if normalized.endswith(suffix)
                        or visible.endswith(suffix)
                        or suffix.endswith(visible)
                    ),
                    None,
                )
            visible_suffix = re.sub(
                r"^.*?\.md", "", visible, count=1, flags=re.IGNORECASE
            ).strip()
            if friendly and visible_suffix:
                friendly = f"{friendly} {visible_suffix}"
            return (
                f"[{friendly}]({match.group(2)})"
                if friendly
                else match.group(0)
            )

        output.append(link_re.sub(replace, line))
    return "\n".join(output) + ("\n" if had_final_newline else "")


def canonicalize_reader_nation_headings(text: str) -> str:
    """Put canonical nation names before internal codes in report headings."""
    canonical = json.loads(
        (ROOT / "derived" / "canonical_terms.json").read_text(encoding="utf-8")
    )
    nation_names = {
        sid: str(names.get("en") or sid)
        for sid, names in (canonical.get("nations") or {}).items()
    }
    for sid, name in nation_names.items():
        text = re.sub(
            rf"^(##{{1,2}})\s+{sid.upper()}\s+[-—–]\s+{re.escape(name)}\s*$",
            rf"\1 {name} (`{sid}`)",
            text,
            flags=re.MULTILINE,
        )
    return text


def canonicalize_english_unit_list_column(
    text: str,
    column_name: str,
) -> str:
    """Show canonical unit names before preserved IDs in generated list cells."""
    canonical = json.loads(
        (ROOT / "derived" / "canonical_terms.json").read_text(encoding="utf-8")
    )
    unit_names = {
        sid: str(names.get("en") or sid)
        for sid, names in (canonical.get("units") or {}).items()
    }
    unit_names["unitbox"] = "Mission placeholder"
    lines = text.splitlines()
    target_column: int | None = None
    for line_index, line in enumerate(lines):
        if not line.startswith("|"):
            target_column = None
            continue
        cells = line.split("|")
        normalized = [cell.strip().casefold() for cell in cells]
        if (
            column_name.casefold() in normalized
            and line_index + 1 < len(lines)
            and _is_markdown_table_separator(lines[line_index + 1])
        ):
            target_column = normalized.index(column_name.casefold())
            continue
        if target_column is None or target_column >= len(cells) - 1:
            continue
        value = cells[target_column].strip()
        if not value or value == "—" or set(value) <= {":", "-", " "}:
            continue
        converted: list[str] = []
        changed = False
        for item in value.split(","):
            raw = item.strip()
            match = re.fullmatch(
                r"`?([a-z0-9_]+)`?(\s+\(\+\d+\))?",
                raw,
            )
            if not match:
                converted.append(raw)
                continue
            unit_sid, suffix = match.groups()
            name = unit_names.get(unit_sid)
            if not name:
                converted.append(raw)
                continue
            converted.append(f"{name} (`{unit_sid}`){suffix or ''}")
            changed = True
        if changed:
            cells[target_column] = " " + ", ".join(converted) + " "
            lines[line_index] = "|".join(cells)
    return "\n".join(lines) + ("\n" if text.endswith("\n") else "")


def clean_english_building_comparison(text: str) -> str:
    """Expand resource abbreviations in reader-facing comparison prose."""
    replacements = {
        "HP": "health",
        "W": "wood",
        "S": "stone",
        "G": "gold",
    }
    output: list[str] = []
    in_fence = False
    for line in text.splitlines():
        if FENCE_RE.match(line):
            in_fence = not in_fence
            output.append(line)
            continue
        if in_fence:
            output.append(line)
            continue
        segments = re.split(r"(`[^`\r\n]+`)", line)
        for index in range(0, len(segments), 2):
            for token, label in replacements.items():
                segments[index] = re.sub(
                    rf"(?<![A-Za-z0-9_]){token}(?=\s*=)",
                    label,
                    segments[index],
                )
        output.append("".join(segments))
    return "\n".join(output) + ("\n" if text.endswith("\n") else "")


def _replace_english_table_column_values(
    text: str,
    column_name: str,
    replacements: dict[str, str],
) -> str:
    """Replace exact values in one named Markdown-table column."""
    lines = text.splitlines()
    target_column: int | None = None
    for line_index, line in enumerate(lines):
        if not line.startswith("|"):
            target_column = None
            continue
        cells = line.split("|")
        normalized = [cell.strip().casefold() for cell in cells]
        if (
            column_name.casefold() in normalized
            and line_index + 1 < len(lines)
            and _is_markdown_table_separator(lines[line_index + 1])
        ):
            target_column = normalized.index(column_name.casefold())
            continue
        if target_column is None or target_column >= len(cells) - 1:
            continue
        value = cells[target_column].strip()
        replacement = replacements.get(value)
        if replacement is None:
            continue
        cells[target_column] = f" {replacement} "
        lines[line_index] = "|".join(cells)
    return "\n".join(lines) + ("\n" if text.endswith("\n") else "")


def clean_english_nation_page(text: str) -> str:
    """Turn generated nation sheets into reader-facing reference pages."""
    canonical = json.loads(
        (ROOT / "derived" / "canonical_terms.json").read_text(encoding="utf-8")
    )
    unit_names = {
        sid: str(names.get("en") or sid)
        for sid, names in (canonical.get("units") or {}).items()
    }

    heading = re.search(
        r"^#\s+(.+?)[ \t]+\(`([a-z]{3})`\)[ \t]*$",
        text,
        re.MULTILINE,
    )
    if heading:
        name, sid = heading.groups()
        text = text.replace(f"_{name}_\n\n", "", 1)
        text = text.replace(
            heading.group(0) + "\n[←",
            heading.group(0) + "\n\n[←",
            1,
        )
        text = text.replace(
            "[← Quick reference](../README.md) · [← All nations](README.md)",
            "[← All nations](README.md) · [← Quick reference](../README.md)",
            1,
        )
        # Older cleanup passes could accumulate a blank line because ``\s*$``
        # consumed the line breaks after the heading.  Keep the intentionally
        # airy three-line separation stable and idempotent.
        text = re.sub(
            rf"({re.escape(heading.group(0))}\n)\n{{4,}}",
            r"\1\n\n\n",
            text,
            count=1,
        )

    cluster_pattern = re.compile(
        r"## Cluster\n\n"
        r"- \*\*Shared cluster:\*\* `([^`]+)` \([^\n]+\)\n"
        r"- \*\*Peasant:\*\* `([^`]+)`\n"
        r"- \*\*Cluster infantry:\*\* cluster `[^\n]+`"
    )

    def replace_cluster(match: re.Match[str]) -> str:
        cluster, peasant = match.groups()
        peasant_name = unit_names.get(peasant, "Peasant")
        return (
            "## Shared features\n\n"
            f"- **Base peasant:** **{peasant_name}** (`{peasant}`).\n"
            "- The Mill, Storehouse, Market, and Tower use the same shared "
            "architectural set."
        )

    text = cluster_pattern.sub(replace_cluster, text)
    text = re.sub(
        r"The Mill, Storehouse, Market, and Tower use one of the game's "
        r"shared architectural sets \(internal group `[^`]+`\)\.",
        "The Mill, Storehouse, Market, and Tower use the same shared "
        "architectural set.",
        text,
    )
    text = text.replace(
        "| Unit | role | HP | damage | recharge | far (tile) |",
        "| Unit | Role | Health | Damage | Reload, game s | Range, cells |",
    )
    text = _replace_english_table_column_values(
        text,
        "Role",
        {
            "Shooter": "Ranged Infantry",
            "Horse Rifleman": "Mounted Ranged Unit",
            "Cannon": "Artillery",
            "Yacht": "Warship",
        },
    )
    text = text.replace(
        "> **Bold** - values that differ from the basic ones (fashion for all nations) for the same type of building.",
        "> **Bold** marks values that differ from the most common version of the same building.",
    )
    text = text.replace(
        "| Building | HP | Time (g-sec) | cost% | F | W | S | G | I | C | farm | produces |",
        "| Building | Health | Build time, game s | Price growth, % | Food | Wood | Stone | Gold | Iron | Coal | Population | Produces |",
    )
    text = text.replace(
        "| Building | HP | Time (g-sec) | cost% | F | W | S | G | I | C | Add. |",
        "| Building | Health | Construction time, game s | Price growth, % | Food | Wood | Stone | Gold | Iron | Coal | Details |",
    )
    text = text.replace(
        "| Unit | HP | Time (g-sec) | F | G | I | damage | far (tile) | recharge | uniqueness |",
        "| Unit | Health | Training time, game s | Food | Gold | Iron | Damage | Range, cells | Reload, s | Availability |",
    )
    text = text.replace(
        "Each officer leads the formation of his units. Standard formations: **LINE / SQUARE / KARE × 15/36/72/120/196/400**.",
        "Officers command formations of the compatible units listed below. Standard formation sizes are 15, 36, 72, 120, 196, and 400.",
    )
    text = text.replace(
        "| officer | drummer | units |",
        "| Officer | Drummer or Bagpiper | Compatible units |",
    )
    text = re.sub(
        r"^### (?:Drummers and pipers|Drummer, 17th century and bagpipers)$",
        "### Drummers and Bagpipers",
        text,
        flags=re.MULTILINE,
    )
    text = re.sub(
        r"^### Mortars$",
        "### Bombards and Howitzers",
        text,
        flags=re.MULTILINE,
    )
    text = re.sub(
        r"^By buildings:$",
        "Upgrade counts by research building:",
        text,
        flags=re.MULTILINE,
    )
    research_buildings = {
        "aca": "Academy",
        "mil": "Mill",
        "bla": "Blacksmith",
        "sta": "Stable",
        "bar": "Barracks, 17th century",
        "ba2": "Barracks, 18th century",
        "art": "Artillery Depot",
        "tem": "Cathedral, Church, or Mosque",
        "cen": "Town Hall",
        "dip": "Diplomatic Center",
        "mines": "Mines",
    }
    for code, label in research_buildings.items():
        text = re.sub(
            rf"^- \*\*{re.escape(code)}\*\* \({re.escape(code)}\):",
            f"- **{label}** (`{code}`):",
            text,
            flags=re.MULTILINE,
        )
    detail_labels = {
        'content {"wood": 32}': "Contains 32 Wood",
        'content {"wood": 40}': "Contains 40 Wood",
        'content {"stone": 150}': "Contains 150 Stone",
        'content {"stone": 200}': "Contains 200 Stone",
        'content {"stone": 250}': "Contains 250 Stone",
        'produces {"coal": 13}; +5 workers':
            "Produces Coal; 5 initial worker slots",
        'produces {"gold": 13}; +5 workers':
            "Produces Gold; 5 initial worker slots",
        'produces {"iron": 13}; +5 workers':
            "Produces Iron; 5 initial worker slots",
        'damage 1000; content {"gold": 500}':
            "Damage 1,000; upkeep 0.8 Gold/game s",
        'damage 1200; content {"gold": 500}':
            "Damage 1,200; upkeep 0.8 Gold/game s",
        'damage 1000; content {"gold": 250}':
            "Damage 1,000; upkeep 0.4 Gold/game s",
    }
    for raw, label in detail_labels.items():
        text = text.replace(raw, label)
    text = text.replace("- **mines** (Mine):", "- **Mines**:")
    lines = text.splitlines()
    produces_column: int | None = None
    for line_index, line in enumerate(lines):
        if not line.startswith("|"):
            produces_column = None
            continue
        cells = line.split("|")
        normalized = [cell.strip().lower() for cell in cells]
        if "produces" in normalized:
            produces_column = normalized.index("produces")
            continue
        if produces_column is None or produces_column >= len(cells) - 1:
            continue
        value = cells[produces_column].strip()
        if not value or value == "—" or set(value) <= {":", "-", " "}:
            continue
        converted: list[str] = []
        for item in value.split(","):
            raw = item.strip()
            match = re.fullmatch(r"([a-z0-9_]+)(\s+\(\+\d+\))?", raw)
            if not match:
                converted.append(raw)
                continue
            unit_sid, suffix = match.groups()
            converted.append(unit_names.get(unit_sid, unit_sid) + (suffix or ""))
        cells[produces_column] = " " + ", ".join(converted) + " "
        lines[line_index] = "|".join(cells)
    return "\n".join(lines) + ("\n" if text.endswith("\n") else "")


def rewrite_translated_links(
    source: Path,
    target: Path,
    text: str,
    pairs: dict[Path, Path],
) -> str:
    file_map = {path.resolve(): translated.resolve() for path, translated in pairs.items()}
    dir_map = {
        (ROOT / "docs").resolve(): (ROOT / "docs_en").resolve(),
        (ROOT / "internals").resolve(): (ROOT / "internals_en").resolve(),
    }

    def replace(match: re.Match[str]) -> str:
        raw = match.group(0)
        path_part, sep, anchor = raw.partition("#")
        if (
            not path_part
            or re.match(r"^[a-z]+:", path_part, flags=re.I)
            or path_part.startswith("/")
        ):
            return raw
        resolved = (source.parent / urllib.parse.unquote(path_part)).resolve()
        translated = file_map.get(resolved) or dir_map.get(resolved)
        if translated is None:
            return raw
        relative = Path(os.path.relpath(translated, target.parent)).as_posix()
        if resolved in dir_map and path_part.endswith("/") and not relative.endswith("/"):
            relative += "/"
        return relative + (sep + anchor if sep else "")

    return LINK_TARGET_RE.sub(replace, text)


def load_manifest() -> dict[str, dict[str, str]]:
    if not MANIFEST_PATH.is_file():
        return {}
    payload = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    sources = payload.get("sources", {})
    if payload.get("schema") == 1:
        return {
            path: {"source_sha256": digest}
            for path, digest in sources.items()
        }
    return {
        path: value
        for path, value in sources.items()
        if isinstance(value, dict)
    }


def write_manifest(pairs: dict[Path, Path]) -> None:
    manifest = {
        "schema": 2,
        "note": (
            "Normalized-LF SHA-256 of each Russian source and its committed "
            "English mirror."
        ),
        "sources": {
            source.relative_to(ROOT).as_posix(): {
                "source_sha256": sha256(source),
                "target": target.relative_to(ROOT).as_posix(),
                "target_sha256": sha256(target),
            }
            for source, target in pairs.items()
        },
    }
    MANIFEST_PATH.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def markdown_structure(text: str) -> dict[str, object]:
    """Return translation-preserved Markdown structure outside fences."""
    heading_levels: list[int] = []
    table_rows = 0
    footnotes: list[str] = []
    malformed_headings: list[int] = []
    in_fence = False
    fence_count = 0
    for line_number, line in enumerate(text.splitlines(), 1):
        if FENCE_RE.match(line):
            in_fence = not in_fence
            fence_count += 1
            continue
        if in_fence:
            continue
        if MALFORMED_ATX_RE.match(line):
            malformed_headings.append(line_number)
        heading = HEADING_RE.match(line)
        if heading:
            heading_levels.append(len(heading.group(1)))
        if line.lstrip().startswith("|"):
            table_rows += 1
        footnote = re.match(r"^\[\^([^\]]+)\]:", line)
        if footnote:
            footnotes.append(footnote.group(1))
    return {
        "heading_levels": heading_levels,
        "table_rows": table_rows,
        "footnotes": footnotes,
        "fence_count": fence_count,
        "unclosed_fence": in_fence,
        "malformed_headings": malformed_headings,
    }


def translation_artifact_errors(text: str) -> list[str]:
    errors: list[str] = []
    lowered = text.lower()
    for marker in TRUNCATION_MARKERS:
        if marker in lowered:
            errors.append(f"contains forbidden truncation marker {marker!r}")
    artifacts = PROTECTOR_ARTIFACT_RE.findall(text)
    if artifacts:
        errors.append(f"contains protector artifacts {artifacts[:3]}")
    malformed_links = len(MALFORMED_LINK_RE.findall(text))
    if malformed_links:
        errors.append(f"contains {malformed_links} malformed '] (' link(s)")
    ids = _explicit_ids_outside_fences(text)
    duplicate_ids = [
        value
        for value, count in collections.Counter(ids).items()
        if count > 1
    ]
    if duplicate_ids:
        errors.append(f"contains duplicate explicit IDs {duplicate_ids[:5]}")
    natural_heading_ids = {
        slug for _, slug, _ in markdown_headings(text)
    }
    heading_id_collisions = sorted(natural_heading_ids.intersection(ids))
    if heading_id_collisions:
        errors.append(
            "contains explicit IDs that duplicate natural heading IDs "
            f"{heading_id_collisions[:5]}"
        )
    return errors


def validate_pair_text(
    source: Path,
    target: Path,
    source_text: str,
    target_text: str,
    *,
    strict: bool = False,
) -> list[str]:
    """Validate that an English mirror has not lost Markdown structure."""
    rel = source.relative_to(ROOT).as_posix()
    source_structure = markdown_structure(source_text)
    target_structure = markdown_structure(target_text)
    errors = [
        f"{rel}: {message}"
        for message in translation_artifact_errors(target_text)
    ]
    if target_structure["unclosed_fence"]:
        errors.append(f"{rel}: target has an unclosed fenced block")
    malformed = target_structure["malformed_headings"]
    if malformed:
        errors.append(f"{rel}: malformed ATX heading(s) at lines {malformed[:5]}")

    source_levels = source_structure["heading_levels"]
    target_levels = target_structure["heading_levels"]
    if strict:
        if target_levels != source_levels:
            errors.append(
                f"{rel}: heading levels differ: "
                f"{source_levels} source, {target_levels} target"
            )
        for key, label in (
            ("table_rows", "table row"),
            ("footnotes", "footnote"),
            ("fence_count", "fence delimiter"),
        ):
            if target_structure[key] != source_structure[key]:
                errors.append(
                    f"{rel}: {label} structure differs: "
                    f"{source_structure[key]} source, "
                    f"{target_structure[key]} target"
                )
    else:
        if len(target_levels) < len(source_levels):
            errors.append(
                f"{rel}: headings were lost: "
                f"{len(source_levels)} source, {len(target_levels)} target"
            )
        if target_structure["table_rows"] < source_structure["table_rows"]:
            errors.append(
                f"{rel}: table rows were lost: "
                f"{source_structure['table_rows']} source, "
                f"{target_structure['table_rows']} target"
            )

    target_ids = set(_explicit_ids_outside_fences(target_text))
    target_ids.update(slug for _, slug, _ in markdown_headings(target_text))
    missing_aliases = [
        slug
        for _, slug, _ in markdown_headings(source_text)
        if slug not in target_ids
    ]
    if missing_aliases:
        errors.append(
            f"{rel}: missing source heading aliases {missing_aliases[:5]}"
        )
    attached_aliases = _aliases_immediately_before_headings(target_text)
    misplaced_aliases = []
    for (_, source_slug, _), (_, target_slug, target_line) in (
        _aligned_heading_pairs(source_text, target_text)
    ):
        if source_slug == target_slug or source_slug in missing_aliases:
            continue
        if source_slug not in attached_aliases.get(target_line, set()):
            misplaced_aliases.append(source_slug)
    if misplaced_aliases:
        errors.append(
            f"{rel}: source heading aliases are attached to the wrong "
            f"translated headings {misplaced_aliases[:5]}"
        )
    return errors


def validate_pair(
    source: Path,
    target: Path,
    *,
    strict: bool = False,
) -> list[str]:
    return validate_pair_text(
        source,
        target,
        source.read_text(encoding="utf-8"),
        target.read_text(encoding="utf-8"),
        strict=strict,
    )


def check(pairs: dict[Path, Path]) -> list[str]:
    manifest = load_manifest()
    manual_fences = load_manual_fenced_translations()
    errors: list[str] = []
    expected_keys = {source.relative_to(ROOT).as_posix() for source in pairs}
    if set(manifest) != expected_keys:
        missing = sorted(expected_keys - set(manifest))
        extra = sorted(set(manifest) - expected_keys)
        if missing:
            errors.append(f"manifest missing {len(missing)} source(s): {missing[:5]}")
        if extra:
            errors.append(f"manifest has {len(extra)} stale source(s): {extra[:5]}")
    for source, target in pairs.items():
        rel = source.relative_to(ROOT).as_posix()
        if not target.is_file():
            errors.append(f"missing translation: {target.relative_to(ROOT)}")
            continue
        entry = manifest.get(rel, {})
        if entry.get("source_sha256") != sha256(source):
            errors.append(f"stale translation: {rel}")
        expected_target = target.relative_to(ROOT).as_posix()
        if entry.get("target") != expected_target:
            errors.append(f"manifest target differs for {rel}: {entry.get('target')}")
        if entry.get("target_sha256") != sha256(target):
            errors.append(f"target changed without manifest update: {expected_target}")
        errors.extend(validate_pair(source, target))
        source_blocks = fenced_blocks(source.read_text(encoding="utf-8"))
        target_blocks = fenced_blocks(target.read_text(encoding="utf-8"))
        if len(source_blocks) != len(target_blocks):
            errors.append(
                f"fence count differs for {rel}: "
                f"{len(source_blocks)} source, {len(target_blocks)} target"
            )
            continue
        for (line_number, source_body), (_, target_body) in zip(
            source_blocks,
            target_blocks,
        ):
            if not CYRILLIC_RE.search(source_body):
                continue
            entry = manual_fences.get(fenced_block_key(source_body))
            if not entry:
                continue
            expected = source_body if entry.get("literal") else entry.get("text")
            if target_body != expected:
                errors.append(f"manual fence translation differs: {rel}:{line_number}")
    expected_fences = {
        fenced_block_key(body)
        for source in pairs
        for _, body in fenced_blocks(source.read_text(encoding="utf-8"))
        if CYRILLIC_RE.search(body)
    }
    missing_fences = sorted(expected_fences - set(manual_fences))
    stale_fences = sorted(set(manual_fences) - expected_fences)
    if missing_fences:
        errors.append(
            f"manual fence catalog missing {len(missing_fences)} block(s): "
            f"{missing_fences[:3]}"
        )
    if stale_fences:
        errors.append(
            f"manual fence catalog has {len(stale_fences)} stale block(s): "
            f"{stale_fences[:3]}"
        )
    untranslated_fences = [
        key
        for key, entry in manual_fences.items()
        if not entry.get("literal")
        and not entry.get("literal_cyrillic")
        and (
            not isinstance(entry.get("text"), str)
            or CYRILLIC_RE.search(str(entry.get("text")))
        )
    ]
    if untranslated_fences:
        errors.append(
            f"manual fence catalog has {len(untranslated_fences)} "
            f"untranslated block(s): {untranslated_fences[:3]}"
        )
    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    parser.add_argument(
        "--adopt-existing",
        action="store_true",
        help="record existing complete translations without contacting the service",
    )
    parser.add_argument(
        "--cleanup-existing",
        action="store_true",
        help="apply deterministic post-translation cleanup to committed targets",
    )
    parser.add_argument(
        "--capture-fenced-translations",
        action="store_true",
        help="capture reviewed English fence bodies from the current mirrors",
    )
    args = parser.parse_args()

    pairs = translation_pairs()
    if args.capture_fenced_translations:
        try:
            captured = capture_manual_fenced_translations(pairs)
        except ValueError as error:
            print(error, file=sys.stderr)
            return 1
        write_manual_fenced_translations(captured)
        print(f"Captured {len(captured)} reviewed fenced translations")
        return 0
    if args.check:
        errors = check(pairs)
        if errors:
            print("\n".join(errors))
            return 1
        print(f"English documentation current ({len(pairs)} translations)")
        return 0
    if args.adopt_existing:
        missing = [target for target in pairs.values() if not target.is_file()]
        if missing:
            for target in missing:
                print(f"missing translation: {target.relative_to(ROOT)}", file=sys.stderr)
            return 1
        validation_errors = [
            error
            for source, target in pairs.items()
            for error in validate_pair(source, target)
        ]
        if validation_errors:
            print("\n".join(validation_errors), file=sys.stderr)
            return 1
        write_manifest(pairs)
        print(f"Adopted {len(pairs)} existing translations")
        return 0
    if args.cleanup_existing:
        canonical = canonical_dictionary()
        changed_count = 0
        for source, target in pairs.items():
            if not target.is_file():
                continue
            current = target.read_text(encoding="utf-8")
            cleaned = clean_translation_artifacts(
                canonicalize_fenced_blocks(current, canonical)
            )
            if target.is_relative_to(ROOT / "docs_en"):
                cleaned = canonicalize_reader_table_codes(cleaned)
                cleaned = canonicalize_reader_nation_headings(cleaned)
                cleaned = canonicalize_english_reader_links(cleaned, target)
            if target.is_relative_to(ROOT / "docs_en" / "reference"):
                cleaned = canonicalize_english_unit_names(cleaned)
                cleaned = canonicalize_english_upgrade_names(cleaned)
            if (
                target.parent
                == ROOT / "docs_en" / "reference" / "compare" / "buildings"
            ):
                cleaned = clean_english_building_comparison(cleaned)
                cleaned = canonicalize_english_unit_list_column(
                    cleaned,
                    "Produces",
                )
            if (
                target.parent
                == ROOT / "docs_en" / "reference" / "compare" / "weapons"
            ):
                cleaned = canonicalize_english_unit_list_column(
                    cleaned,
                    "Units",
                )
            if target.parent == ROOT / "docs_en" / "reference" / "05_upgrades":
                cleaned = clean_english_upgrade_table(cleaned)
            if (
                target.parent == ROOT / "docs_en" / "reference" / "nations"
                and target.name != "README.md"
            ):
                cleaned = clean_english_nation_page(cleaned)
                for column_name in (
                    "Officer",
                    "Drummer or Bagpiper",
                    "Compatible units",
                ):
                    cleaned = canonicalize_english_unit_list_column(
                        cleaned,
                        column_name,
                    )
            if (
                target.is_relative_to(ROOT / "docs_en" / "reports")
                and target.name != "README.md"
            ):
                cleaned = clean_reader_report(cleaned)
            cleaned = ensure_heading_aliases(
                source.read_text(encoding="utf-8"),
                cleaned,
            )
            if cleaned != current:
                target.write_text(cleaned, encoding="utf-8")
                changed_count += 1
        validation_errors = [
            error
            for source, target in pairs.items()
            for error in validate_pair(source, target)
        ]
        if validation_errors:
            print("\n".join(validation_errors), file=sys.stderr)
            return 1
        print(f"Cleaned {changed_count} existing translations")
        return 0

    previous = load_manifest()
    changed = [
        (source, target)
        for source, target in pairs.items()
        if not target.is_file()
        or previous.get(source.relative_to(ROOT).as_posix(), {}).get(
            "source_sha256"
        ) != sha256(source)
    ]
    print(
        "Automatic translation is disabled. Edit every English mirror "
        "manually, review it, then run --adopt-existing and --check.",
        file=sys.stderr,
    )
    for source, target in changed[:30]:
        print(
            f"manual translation required: {source.relative_to(ROOT)} "
            f"→ {target.relative_to(ROOT)}",
            file=sys.stderr,
        )
    if len(changed) > 30:
        print(f"…and {len(changed) - 30} more", file=sys.stderr)
    return 1


if __name__ == "__main__":
    sys.exit(main())
