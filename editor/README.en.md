<a id="cossacks-3--тренажёр-стратегий-v04"></a>
# Cossacks 3 — Build Order Planner (v0.4)

**English** · [Русский](README.md)

> **Status: working.** The planner loads game data, lays out a build order on
> a timeline, and runs the economy simulation directly in the browser.

Use it to test a build order: when resources become available, how many
peasants can be assigned, when a production building becomes free, and which
requirements are still missing.

<a id="что-умеет"></a>
## Features

- lists the buildings, units, and upgrades available to the selected nation;
- places construction, training, research, trade, and peasant assignments on
  one timeline;
- supports drag-to-reschedule and editing through the inspector;
- accounts for technology requirements, production queues, resources,
  population, and builder limits;
- supports finite and infinite unit production;
- plots resources and population and shows the simulation log;
- saves plans in the browser and imports or exports JSON;
- can start from actions recognized in a replay;
- supports Russian and English.

<a id="как-запустить"></a>
## Running locally

From the repository root:

```bash
python -m http.server 8000
```

Open `http://localhost:8000/editor/`. The tool cannot run from `file://`
because browsers block the required data and module requests.

Pyodide and Chart.js are downloaded on the first visit and are normally
served from the browser cache afterwards.

<a id="структура"></a>
## Structure

```text
editor/
├── index.html
├── css/
│   └── editor.css
└── js/
    ├── main.js
    ├── data_loader.js
    ├── pyodide_runner.js
    ├── build_order.js
    └── ui/
        ├── catalog_panel.js
        ├── inspector.js
        ├── timeline.js
        ├── timeline_view.js
        └── charts.js
```

The browser uses the same
`simulator/simulate_economy.py:simulate_in_memory` function as the command-line
tool.

<a id="границы-инструмента"></a>
## Scope

The planner currently has no side-by-side comparison mode, graphical
technology tree, or spatial map view. Those features are separate from its
core build-order workflow and can be added independently.

<a id="сверка-с-командной-строкой"></a>
## Comparing with the command line

Pass an exported plan to the command-line simulator:

```bash
python simulator/simulate_economy.py <plan.json>
```

The report and the browser planner should produce the same numbers.
