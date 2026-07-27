<a id="cossacks-3--тренажёр-стратегий-v02"></a>
# Cossacks 3 - Strategy Trainer (v0.2)

**English** · [Русский](README.md)

> ⚠ **STATUS: NOT WORKING - work in progress.**
> The editor in its current form is broken and unusable. It's in the repo
> as a blank, it is completed as a separate task. **Do not use**, do not
> referenced from other documents, not considered part of the reference book.

Browser build order editor. Loads game data from `data.json` and runs the economy simulator (`simulator/simulate_economy.py`) directly in the browser via Pyodide.

<a id="что-умеет"></a>
## What he can do

- ✅ **Completely in Russian.** All UI elements, names of nations/buildings/units/upgrades from the game localization.
- ✅ **Actions are selected with the mouse**, without editing JSON:
  - **📦 Build** — dropdown of nation buildings with prices, number of builders.
  - **👥 Train** - select a manufacturing building, then dropdown the units available in it.
  - **🔬 Explore** - upgrades are grouped by location (Academy / Blacksmith / Mine gold / ...).
  - **⛏ Scatter the peasants** - separate fields for food/wood/stone/gold/iron/coal.
- ✅ **Live simulation** - button ▶ Run, result in 100-300ms.
- ✅ **Charts**: resources over time, population/farm cap.
- ✅ **Final summary** - cards for 6 resources + peasants / farm / buildings.
- ✅ **Events** from the simulator (SKIP/WARN/ERROR are highlighted).
- ✅ **Save/load** in LocalStorage, JSON export/import is CLI compatible.
- ✅ **Adaptive layout** - on narrow screens, a two-column layout is collapsed into one.

<a id="как-запустить"></a>
## How to run

At the root of the repository:
```bash
python -m http.server 8000
```
Open `http://localhost:8000/editor/`.

> ⚠ Do not open `index.html` through `file://` - Pyodide and fetch are crashing on CORS.

First load ~5-10 sec (Pyodide ~6MB is cached by the browser). Then instantly.

<a id="структура"></a>
## Structure
```
editor/
├── index.html
├── README.md
├── css/
│   └── editor.css           # Dark theme with gold accents
└── js/
    ├── main.js              # Entry point and UI orchestrator
    ├── data_loader.js       # fetch data.json + tech_tree.json + builder_slots.json
    ├── pyodide_runner.js    # Pyodide bootstrap + simulate_in_memory
    ├── build_order.js       # Model, LocalStorage, import/export
    └── ui/
        ├── i18n.js          # Localized names and resource icons
        ├── catalog.js       # Per-nation building, unit, and upgrade selections
        ├── action_form.js   # Inline action form
        ├── action_list.js   # Action cards
        └── charts.js        # Chart.js wrappers
```
`simulator/simulate_economy.py` has the function `simulate_in_memory(build_order, data, tree, slots) → dict`, the same engine as for the CLI, without file IO.

<a id="что-не-работает-план--project_visual_editor_phase1_concretemd"></a>
## What does NOT work (plan - `project_visual_editor_phase1_concrete.md`)

- ❌ Editing an already added action - for now only deleting + adding again.
- ❌ Drag-and-drop reorder of the action list.
- ❌ Timeline Gantt - only a list of cards.
- ❌ Tech tree graph view - Phase 2.
- ❌ Compare mode (two side-by-side build orders).
- ❌ Map view (Level C simulator required).

## Sanity-check (CLI vs editor)

If you need to compare the CLI result with the editor, pass your
build order JSON to `python simulator/simulate_economy.py <bo.json>`
— the script will create `sim_<name>.csv` and `sim_<name>.md` in the current
directories. In the editor the same numbers must match
one-on-one.
