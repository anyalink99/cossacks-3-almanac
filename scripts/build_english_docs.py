"""Build and verify the English documentation mirror.

The committed English files are normal Markdown, so readers and GitHub Pages
never depend on a translation service. This script is only a maintainer tool:

    python scripts/build_english_docs.py          # refresh changed translations
    python scripts/build_english_docs.py --check  # verify coverage/freshness

Canonical game labels are substituted from ``canonical_terms.json`` and
``data.json`` before prose is translated. Code, link destinations, and HTML
tags are preserved; canonical game labels inside fenced examples are updated
without translating the surrounding source code. The translation source
hashes are committed in ``translation_sources.json`` so CI can detect stale
mirrors.
"""
from __future__ import annotations

import argparse
import concurrent.futures as futures
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


if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parent.parent
MANIFEST_PATH = ROOT / "translation_sources.json"
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
TRANSLATION_CLEANUPS = {
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
    "g-сек": "game sec",
    "g-минуты": "game minutes",
    "g-минуту": "game minute",
    "g-мин": "game min",
    "g-минут": "game min",
    "game minы": "game minutes",
    " попаданий": " hits",
    " тайла": " tiles",
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
    "gold/г-сек": "gold/game sec",
    ". То есть `random`": ". That is, `random`",
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def translation_pairs() -> dict[Path, Path]:
    pairs: dict[Path, Path] = {}
    for source_root, target_root in (
        (ROOT / "docs", ROOT / "docs_en"),
        (ROOT / "internals", ROOT / "internals_en"),
    ):
        for source in source_root.rglob("*.md"):
            pairs[source] = target_root / source.relative_to(source_root)

    for source in ROOT.rglob("README.md"):
        if any(part in {
            ".git", ".pytest_cache", ".codex_probe",
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


def github_slug(text: str) -> str:
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
            if marker not in text and shortened in text:
                text = text.replace(shortened, marker)
            text = text.replace(marker, value)
        missing = MARKER_RE.findall(text)
        if missing:
            raise RuntimeError(f"translation returned unknown markers: {missing[:3]}")
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


def translate_markdown(text: str, canonical: list[tuple[str, str]]) -> str:
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
    result = canonicalize_fenced_blocks(result, canonical)
    result = clean_translation_artifacts(result)
    if had_final_newline:
        result += "\n"
    return result


def clean_translation_artifacts(text: str) -> str:
    for source, target in TRANSLATION_CLEANUPS.items():
        text = text.replace(source, target)
    return text


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


def load_manifest() -> dict[str, str]:
    if not MANIFEST_PATH.is_file():
        return {}
    return json.loads(MANIFEST_PATH.read_text(encoding="utf-8")).get("sources", {})


def write_manifest(pairs: dict[Path, Path]) -> None:
    manifest = {
        "schema": 1,
        "note": "SHA-256 of each Russian source used for the committed English translation.",
        "sources": {
            source.relative_to(ROOT).as_posix(): sha256(source)
            for source in pairs
        },
    }
    MANIFEST_PATH.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def check(pairs: dict[Path, Path]) -> list[str]:
    manifest = load_manifest()
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
        if manifest.get(rel) != sha256(source):
            errors.append(f"stale translation: {rel}")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--force", action="store_true")
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
    parser.add_argument("--workers", type=int, default=6)
    parser.add_argument(
        "--engine",
        choices=("google", "argos"),
        default="google",
        help="Draft translation engine; committed output remains offline.",
    )
    args = parser.parse_args()
    global TRANSLATION_ENGINE
    TRANSLATION_ENGINE = args.engine

    pairs = translation_pairs()
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
        write_manifest(pairs)
        print(f"Adopted {len(pairs)} existing translations")
        return 0
    if args.cleanup_existing:
        canonical = canonical_dictionary()
        changed_count = 0
        for target in pairs.values():
            if not target.is_file():
                continue
            current = target.read_text(encoding="utf-8")
            cleaned = clean_translation_artifacts(
                canonicalize_fenced_blocks(current, canonical)
            )
            if cleaned != current:
                target.write_text(cleaned, encoding="utf-8")
                changed_count += 1
        print(f"Cleaned {changed_count} existing translations")
        return 0

    canonical = canonical_dictionary()
    previous = load_manifest()
    changed = [
        (source, target)
        for source, target in pairs.items()
        if args.force
        or not target.is_file()
        or previous.get(source.relative_to(ROOT).as_posix()) != sha256(source)
    ]
    print(
        f"Translating {len(changed)} of {len(pairs)} files "
        f"with {len(canonical)} canonical labels…",
        flush=True,
    )

    def process(item: tuple[Path, Path]) -> tuple[Path, Path]:
        source, target = item
        translated = translate_markdown(source.read_text(encoding="utf-8"), canonical)
        translated = rewrite_translated_links(source, target, translated, pairs)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(translated, encoding="utf-8")
        return source, target

    completed = 0
    with futures.ThreadPoolExecutor(max_workers=max(1, args.workers)) as pool:
        tasks = {pool.submit(process, item): item for item in changed}
        for task in futures.as_completed(tasks):
            source, target = task.result()
            completed += 1
            print(
                f"[{completed:>3}/{len(changed)}] "
                f"{source.relative_to(ROOT)} → {target.relative_to(ROOT)}",
                flush=True,
            )

    write_manifest(pairs)
    errors = check(pairs)
    if errors:
        print("\n".join(errors), file=sys.stderr)
        return 1
    print(f"English documentation current ({len(pairs)} translations)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
