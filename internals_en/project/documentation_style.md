<a id="правила-читательской-документации"></a>
# Reader-facing documentation rules

**English** · [Русский](../../internals/project/documentation_style.md)

[← Project architecture and maintenance](README.md)

These rules apply to `docs/**/*.md`, the templates under
`writers/templates/`, reader-facing passages in `internals/**/*.md`, and
their English mirrors. The goal is to explain the game to an ordinary reader
without losing the precision needed to verify a claim against the scripts.

<a id="1-сначала-игровое-понятие-затем-внутренний-идентификатор"></a>
## 1. Use the game-facing name before the internal identifier

Main prose always uses the canonical localized name. An internal code, SID,
field, or function name appears only after that name and is formatted as
`code`.

| Avoid | Prefer |
|---|---|
| the `eurtow` object | the **Tower** (`eurtow`) |
| `gainres` is a Peasant order | the “gather resource” order (`gainres`) |
| a unit with `priest` heals the target | the **Priest** (`priest`) heals an ally |
| the `capture` setting | object-capture rules (`capture`) |

In a table, put the canonical name in the first column. If readers need the
internal code, give it a separate “Internal code” column or place it after the
name: **Tower** (`eurtow`).

Canonical names come from:

- [`derived/canonical_terms.json`](../../derived/canonical_terms.json);
- the functions and dictionaries in
  [`parser/config.py`](../../parser/config.py);
- the Russian and English game locales used to build the glossary.

If a name is missing, fix the glossary source first. Do not invent a private
mapping inside an article or generator.

<a id="2-русский-читательский-текст-не-смешивается-с-жаргоном-движка"></a>
## 2. Do not mix reader-facing prose with engine jargon

Use ordinary English game terminology in explanations. Preserve the exact
engine term only as a secondary technical reference:

| Avoid as an unexplained engine term | Explain as |
|---|---|
| `build order` | the planned sequence of construction and production |
| `attack-move` | moving while attacking enemies encountered on the way |
| `handler`, `callback` | the code that handles an event |
| `queue` | the production or command queue |
| `target`, `owner` | the affected object or the player that owns it |
| `spawn` | creating an object or making it appear |
| `range`, `damage`, `pause` | firing range, damage, or reload time |
| `HP`, `max HP` | health or maximum health |
| `DPS` | damage per second |
| `UI`, `FOW` | the interface or fog of war |
| `state machine` | the set of states and transitions between them |

- “maximum health (`maxhp`)”;
- “attack-move (`move_mode_attack`)”;
- “the `_unit_OnDeath` handler”;
- “fog of war (`FOW` in the engine field name)”.

Do not lead a heading or table row with an unexplained SID. Do not turn
identifiers into prose by adding grammatical suffixes. Describe the concept
first, then show the literal identifier in `code`.

<a id="3-читательский-и-технический-слои-разделяются"></a>
## 3. Separate the reader-facing and technical layers

An article under `docs/` should present information in this order:

1. a short answer or practical conclusion;
2. a plain-language explanation of the mechanic;
3. formulas and numerical examples;
4. internal fields, functions, and supporting excerpts;
5. sources and concise caveats where they prevent overclaiming.

Do not open with a list of functions, SIDs, or unresolved research tasks.
Material intended only for developers or modders belongs under `internals/`;
the reader-facing article can link to it.

Do not duplicate detailed hypotheses or experiment plans in reader articles or
`known_issues.md`. Keep them in
`internals/project/research_backlog_combat.md` or
`internals/project/research_backlog_systems.md`. A technical evidence article
under `internals/` may link to the relevant section when needed; a
reader-facing article should not. Reserve `known_issues.md` for current parser
limitations, data discrepancies, and verified caveats.

An internal key may appear in a heading only after a descriptive label:
“Peace time (`peacetime`)”, not just “`peacetime`”.

<a id="4-факт-вывод-и-гипотеза-не-смешиваются"></a>
## 4. Keep facts, inferences, and hypotheses distinct

- A claim confirmed by scripts or data is presented as a fact and cites its
  source.
- A conclusion derived from several sources is explicitly identified as an
  inference.
- Unverified behavior is omitted from reader-facing articles. Record it in a
  research backlog and label it there as a hypothesis or open question.
- If a function, state machine, or loader was not found, do not claim that it
  exists.
- Readers see only the current verified rule. Do not write that an earlier
  article was wrong, that a previous version confused two cases, or that “we
  fixed” an error. Correction history belongs in Git, not in the encyclopedia.

A technical correction log is allowed only in
`internals/project/known_issues_archive.md`; do not carry that narrative into
reader-facing articles.

Do not rewrite literal names, values, or source excerpts for stylistic
reasons. Translate the explanation around them; keep the literal content
unchanged in `code` or a real code block.

<a id="5-кодовые-блоки-используются-только-по-назначению"></a>
## 5. Use fenced blocks only when formatting is meaningful

Fenced blocks are for:

- real code or pseudocode;
- literal game data;
- Mermaid diagrams;
- layouts whose monospaced alignment matters.

Do not hide ordinary prose, tables, or author-written explanations in a code
block. Translate author-written labels, comments, and diagrams in the English
mirror. Do not translate genuine identifiers or literal game data.

After changing an author-written fenced block and reviewing both languages,
update the manual translation catalog:

```bash
python scripts/build_english_docs.py --capture-fenced-translations
```

<a id="6-английское-зеркало-обновляется-вместе-с-русской-статьёй"></a>
## 6. Update the English mirror with the Russian source

Every file under `docs/` or `internals/` must have a mirror under `docs_en/`
or `internals_en/`.

- Use canonical English names from `canonical_terms.json`.
- Translate and edit the English prose manually. Do not use machine
  translation, even as a publication draft.
- Use American spelling in English prose: `behavior`, `armor`, `neighbor`,
  `center`, `localization`, and `canceled`. Preserve canonical names and
  literal quotations from the game unchanged.
- Keep real SIDs, fields, functions, and values unchanged.
- Translate meaning rather than Russian word order.
- Add each new Russian heading slug to the English file as a compatible
  `<a id="..."></a>` immediately before the corresponding English heading.
- Keep an old anchor as an additional alias if external links may already use
  it.
- Heading, table, footnote, and fenced-block structure must remain aligned
  unless a difference is deliberate and reviewed.

<a id="7-markdown-и-навигация"></a>
## 7. Markdown and navigation

- Put a space after the `#` characters in a heading.
- Explicit IDs must be unique within the page.
- Link labels must explain their destination; avoid “Index” and bare
  filenames in reader-facing navigation.
- Russian reader-facing text uses “клетка”, “игровая секунда” (`игр. с` in
  compact tables), and “попадание в голову” instead of the borrowed terms
  “тайл”, “game sec”, and “хедшот”.
- English reader-facing text uses `cells` and `game seconds` (`game s` in
  compact tables), not `tiles` or `g-sec`.
- Test in-page links in the browser after renaming a heading.
- Articles under `docs/recon/` link back to “How the Game Works”; technical
  articles link to the appropriate `internals/` index.

<a id="8-проверки-перед-коммитом"></a>
## 8. Checks before committing

After editing a Russian source and its English mirror:

```bash
# If author-written fenced blocks changed:
python scripts/build_english_docs.py --capture-fenced-translations

# Record the reviewed pair and rebuild search:
python scripts/build_english_docs.py --adopt-existing
python compute/build_md_manifest.py

# Required checks:
python scripts/build_english_docs.py --check
python scripts/check_markdown_links.py
python -m unittest discover -s tests -v
git diff --check
```

The tests in
[`tests/test_reader_facing_docs.py`](../../tests/test_reader_facing_docs.py)
also reject bare object SIDs, unformatted Latin engine terms, and known engine
jargon in Russian `docs/recon/` prose.
