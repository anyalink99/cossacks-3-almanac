# Contributing

**English** · [Русский](CONTRIBUTING.md)

This document is a short cheat sheet on how the repository works and where
what to touch. If you just arrived, start with [`docs/architecture.md`](docs_en/architecture.md)
— there is a data flow diagram and principles. This file answers specific
“how do I…” questions.

## Before you start

```bash
# Environment: Python 3.11+; the project itself uses only the standard library.
# Game: Cossacks 3 in the default Steam location, or set COSSACKS3_PATH.

# Verify that the pipeline works:
python -m unittest discover -s tests -v
python scripts/regen.py sanity   # parser + 112 automatic checks
```
CI runs smoke tests for each PR, checking that `canonical_terms.json`
and `data.json` are not broken and that `parser/config.py` is imported.

## Where to touch what

| I want... | I'm going to... |
|---|---|
| **Correct a Russian nation/building/option label** | Do not edit it here: the label comes from the game locale. Change the locale in your own mod, or run `python parser/build_canonical_terms.py` after a game patch. |
| **Correct a formula or number in the reference** | Find its source: a parser for values from `data.json`, a compute script for calculated values, or a template for handwritten reference prose. Never edit generated Markdown under `docs/reference/` or `docs/reports/`; it will be overwritten. |
| **Add a new section to reference** | The template is in [`writers/templates/reference/<chapter>/`](writers/templates/reference/). Rendering logic is in [`writers/write_md_tree.py`](writers/write_md_tree.py). |
| **Add a report** | Create `compute/compute_<topic>.py` based on a neighboring report and emit `docs/reports/<section>/<name>.md`. Register it as a `reports-*` target in `scripts/regen.py`. For a new section, add its directory under `docs/reports/` and link it from `docs/reports/README.md`. |
| **Add a JSON dataset** | Add `parser/parse_<name>.py` if it reads game files, or `compute/compute_<name>.py` if it derives data from `data.json`. Emit `derived/<name>.json` and document it in [`derived/README.md`](derived/README.en.md). |
| **Edit recon prose** | Edit the relevant file under `docs/recon/`; those documents are handwritten. |
| **Edit reference prose** | Edit a template under `writers/templates/reference/<chapter>/`, then run `python writers/write_md_tree.py`. |
| **Add a test** | Add `tests/test_<topic>.py`. Tests use the standard-library `unittest` framework and have no external dependencies. |

## Rules

1. **The source of truth is the game files.** No manually invented translations
   or numbers. If it disagrees with the external guide, trust the game code.
2. **Idempotency.** `python scripts/regen.py all` must regenerate
   everything from scratch. If your edit breaks idempotency, it's a bug.
3. **Canonical names come through `parser/config.py`.** Never
   hardcode `NATION_NAMES = {...}` or `USAGE_RU = {...}` in a new script.
   Import: `from config import nation_label, USAGE_RU, decode_usage`.
   If a mapping is missing, add it to the canonical-term pipeline and expose
   it through the config instead of defining a private copy in your script.
4. **Do not edit auto-generated md.** List of auto-gen files:
   - `data.json`
   - `derived/*.json`
   - `docs/reference/**/*.md`
   - `docs/reports/**/*.md`
   - `docs/README.md` (generated from `writers/templates/output_readme.md`)
   - `internals/engine/native_primitives.md` (generated from `parser/engine_recon/extract_dws_signatures.py`)

   Handwritten means to edit by hand:
   - `README.md`, `CONTRIBUTING.md` (top-level).
   - `docs/architecture.md`, `docs/known_issues*.md`,
     `docs/reports/README.md`, `docs/reference/README.md` (writer writes
     a short hat, the rest by hand).
   - `docs/recon/**/*.md` (including README) - handwritten reverse-engineering.
   - `internals/**/*.md` (except `native_primitives.md`) - handwritten technical
     documentation of the engine / scripts / `data/`-directory.
   - `derived/README.md` - handwritten.
   - `mods/**/README.md` - handwritten.
5. **Sanity checks.** `parser/build_data.py` runs 112 checks. If one fails,
   identify and fix the cause; do not disable the check.
6. **No emoji** in code or documentation unless requested. Status symbols
   such as ✅/❌ may be useful in engine-behavior tables, but use them sparingly.

## How the change is made

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
## Commit style

`<type>(<scope>): <message>` (soft convention, without hard linter):

- `feat(config): centralize Russian glossary`
- `refactor(generators): use canonical names`
- `chore(prose): clean kalki and unify time units`
- `chore(legacy): remove old monolithic reference`
- `docs: add architecture and derived/README`
- `fix(parser): bmercenary block extraction`

Body of the commit - what changed and why. If you change several files of one
edit - list the main ones.

## When in doubt

- Architecture and data flows - [`docs/architecture.md`](docs_en/architecture.md).
- Canonical terms - [`derived/canonical_terms.json`](derived/canonical_terms.json) +
  [`parser/config.py`](parser/config.py).
- Known spaces - [`docs/known_issues.md`](docs_en/known_issues.md).
- What is generated where - [`derived/README.md`](derived/README.en.md) +
  [`docs/reports/README.md`](docs_en/reports/README.md) + [`scripts/regen.py`](scripts/regen.py).
