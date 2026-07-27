# Contributing

**English** · [Русский](CONTRIBUTING.md)

This document is a short cheat sheet on how the repository is arranged and where
What to touch. If you just came, start with [`internals/project/architecture.md`](internals/project/architecture.md).
There is a data flow chart and principles. This file responds to specific
"like me..." questions.

All new and edited articles must also follow the
[reader-facing documentation rules](internals_en/project/documentation_style.md).

<a id="перед-началом-работы"></a>
## Before starting work
```bash
# Environment: Python 3.11+; the project itself uses only the standard library.
# Game: Cossacks 3 in the default Steam location, or set COSSACKS3_PATH.

# Verify that the pipeline works:
python -m unittest discover -s tests -v
python scripts/regen.py sanity   # parser + 112 automatic checks
```
CI for each PR runs smoke tests, checks that `canonical_terms.json`
`data.json` is not broken and that `parser/config.py` is imported.

<a id="где-трогать-что"></a>
## What to edit where

| I want to... | Going to... |
|---|---|
| **Pope Love Russian label nation/buildings/options** | NO. It's from the locale of the game. Pope either locale (if you have your own mod) or run `python parser/build_canonical_terms.py` after the game patch. |
| **Pope Compare formula/number in reference** | Find source: parser (if from `data.json`), compute script (if calculated), template (if manual prose in reference/). Do not edit the generated md in `docs/reference/` or `docs/reports/` - it will be rewritten. |
| **Add a new section to reference** | Template to [`writers/templates/reference/<chapter>/`](writers/templates/reference/). The render logic is in [`writers/write_md_tree.py`](writers/write_md_tree.py). |
| **Add a new report** | Create a `compute/compute_<тема>.py` modeled after the neighbors. Issue in `docs/reports/<section>/<name>.md`. Register with `scripts/regen.py` (`reports-*` target). If a new partition is added to `docs/reports/` and mentioned in `docs/reports/README.md`. |
| **Add a new JSON dataset** | Parser to `parser/parse_<X>.py` (if reading game files) or `compute/compute_<X>.py` (if counting from `data.json`). Issued in `derived/<name>.json`. Describe in [`derived/README.md`](derived/README.md). |
| **Pope Like prose in recon** | Right in the `docs/recon/*.md` files - they're handwritten. |
| **Pope Explore the prose in reference** | Templates in `writers/templates/reference/<chapter>/*.md`. Regenerate: `python writers/write_md_tree.py`. |
| **Add test** | New file in `tests/test_<тема>.py`. Standard `unittest`, no dependencies. |

<a id="правила"></a>
## Rules

1. **The source of truth is the game files. ** No manual translations
or numbers. If it differs from the external guide, trust the game code.
2. **Idempotence.** `python scripts/regen.py all` must regenerate
Everything from scratch. If your edit breaks idempotence, it's a bug.
3. **Canonical Russian names - via `parser/config.py`.** Never not
`NATION_NAMES = {...}` or `USAGE_RU = {...}` in the new script.
Import: `from config import nation_label, USAGE_RU, decode_usage`.
If there is no mapping, add to config + canonical terms.json.
Not your script.
4. **Do not edit auto-generated md.** List of auto-gen files:
- `data.json`
- `derived/*.json`
- `docs/reference/**/*.md`
- `docs/reports/**/*.md`
`docs/README.md` (generated from `writers/templates/output_readme.md`)
`internals/engine/native_primitives.md` (generated from `parser/engine_recon/extract_dws_signatures.py`)

Handwritten means manually editing:
- `README.md`, `CONTRIBUTING.md` (top-level).
- `internals/project/architecture.md`, `internals/project/known_issues*.md`,
`docs/reports/README.md`, `docs/reference/README.md`
Short cap, the rest with your hands.
`docs/recon/**/*.md` (including README) - handwritten reverse-engineering.
`internals/**/*.md` (except `native_primitives.md`) - handwritten technical
Documentation of the engine / scripts / `data/` directory.
- `derived/README.md` - handwritten.
- `mods/**/README.md` - handwritten.
5. **Sanity checks.** `parser/build_data.py` is running 112 checks. If it fell
- figure it out first, then rule. You can't just turn it off.
6. **No emoji in code/documents unless requested. C   for behavior
The engine can be emoji (ах/ах in tables) - but not everywhere.
7. **The reader-facing name comes before the internal code.** Put the
   canonical name first, keep SIDs and fields secondary in `code`, and do not
   mix ordinary prose with unexplained engine jargon. See the full rules and
   examples in
   [`internals_en/project/documentation_style.md`](internals_en/project/documentation_style.md).
8. **Translate English documentation manually.** Update the matching file
   under `docs_en/` or `internals_en/`, review both versions, and only then run
   `python scripts/build_english_docs.py --adopt-existing`. Do not use machine
   translation for published prose.

<a id="как-делается-изменение"></a>
## How to make a change
```bash
# 1. Edit the source: parser, compute script, template, or handwritten Markdown.
# 2. Regenerate its dependants:
python scripts/regen.py all       # full rebuild (about four minutes)
# Or run a targeted build:
python scripts/regen.py reference
python scripts/regen.py reports-economy

# 3. Verify:
python -m unittest discover -s tests
python scripts/regen.py sanity    # 112/112 PASS

# 4. Commit one logical change, without co-authoring.
git add <files>
git commit -m "<concise message>"
```
<a id="стиль-коммитов"></a>
## Commit style

`<type>(<scope>): <message>` (soft convention, no hard linter):

- `feat(config): centralize Russian glossary`
- `refactor(generators): use canonical names`
- `chore(prose): clean kalki and unify time units`
- `chore(legacy): remove old monolithic reference`
- `docs: add architecture and derived/README`
- `fix(parser): bmercenary block extraction`

Body Commit – What and Why Has Changed If you change several files in one
In addition, list the main ones.

<a id="когда-сомневаешься"></a>
## When in doubt

Architecture and data flows — [`internals/project/architecture.md`](internals/project/architecture.md).
Canonical terms - [`derived/canonical_terms.json`](derived/canonical_terms.json)
[`parser/config.py`](parser/config.py).
Known gaps are [`internals/project/known_issues.md`](internals_en/project/known_issues.md).
What is generated – [`derived/README.md`](derived/README.en.md)
[`docs/reports/README.md`](docs_en/reports/README.md) + [`scripts/regen.py`](scripts/regen.py).
