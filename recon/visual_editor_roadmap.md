# Visual Strategy Editor — Roadmap

Зеркало плана из `~/.claude/projects/.../memory/project_visual_strategy_editor_plan.md` для удобства — чтобы план жил в репозитории и виделся в IDE.

## Vision (что делает редактор)

Single-page web app. Пользователь видит:
- **Timeline pane** (Gantt): здания/юниты/апгрейды на оси времени
- **Resource curves**: F/W/S/G/I/C по времени, warning'и при negative/cap
- **Tech tree pane**: clickable graph, нажатие на узел → если prereqs ok → "schedule build"
- **Action editor**: список действий с drag-to-reorder
- **Validation**: live warning'и ("not enough wood at t=120g")
- **Compare mode**: 2+ build orders бок-о-бок с overlay графиков

Core loop: click → edit → симулятор пересчитывает → curves обновляются. Sub-second feedback.

---

## Что не хватает (по категориям)

### A. Эмпирические данные (TBD)
| Item | Status | Blocks |
|---|---|---|
| Peasant speed (tiles/g-sec) | OPEN, P1 в extraction plan | Физический walk_overhead в editor |
| Animation FPS (32 assumption) | OPEN, P2 | Точность hit rate |
| Tree counts на конкретной карте | OPEN (P3 partially done) | Warning'и "лес выработан" |
| Combat damage formulas validation | Done in code | DPS/EHP нужны (item 4 of roadmap) |

### B. Reference data ещё не извлечена
| Item | Why needed | How |
|---|---|---|
| Unit/building icon paths (`data/images/icons/*`) | UI thumbnails | Glob по `data/images/`, маппинг к sids |
| Starting position layout (peasants, cen, sto) | Дефолт стартового state | Прочитать `CreateStartPointPeasants` в dogenerate.inc |
| Strategy templates по нациям | Editor presets | Курировать вручную или импорт community guides |
| Per-nation upgrade priority hints | Editor "suggested next" | Manual curation |

### C. Симулятор требует доработки
| Gap | Текущее | Что добавить |
|---|---|---|
| **Walking overhead физический** | static `walk_overhead=0.30` | Per-action distance до nearest storehouse, считается live |
| **Tree depletion** | unlimited pool | Track wood_remaining; warning при истощении |
| **Field regen / restart cycles** | infinite food per peasant | Симулировать field HP цикл (25000 max, regen, 109g restart on kill) |
| **Production cancel/refund** | not implemented | Add `cancel` action; refund cost partially |
| **Multiple unit types в очереди** | работает, но без UI | Editor показывает split queues |
| **Auto-rebuild destroyed buildings** | N/A | Future: opponent attacks |
| **Combat / attack simulation** | not implemented | Нужно сначала DPS/EHP |
| **Opponent AI** | not implemented | Out of scope для editor v1 |
| **Storehouse placement** | not modeled | Editor: drag storehouses на map view |
| **Mine deposit positions** | not modeled | Editor: показать 4×3=12 deposit positions |

### D. Новые расчётные инструменты (items 4-9 strategy roadmap)
| Item | Что даёт editor |
|---|---|
| **DPS/EHP таблицы** | "у этой армии 1500 DPS vs sword, 200 EHP vs bullet" |
| **Counter-unit matrix** | "musketeer хард-каунтер pikeman" tooltip |
| **Time-to-X calculator** (inverse: target → minimum build order) | "хочу 30 musketeers к t=10min, предложи build order" |
| **Income vs upkeep budget** | "армия ест 320 food/min, добываешь 280 — голод через 5 min" |
| **Per-nation tier list** | "Бавария сильная против ranged за счёт 18c гренадеров" |

### E. UI/UX engineering
| Component | Notes |
|---|---|
| Layout | 3-pane: tech tree (left), timeline (center), resource curves (right) |
| Timeline rendering | Gantt-like; rows = buildings/units/upgrades; bars = construction durations |
| Resource curves | Multi-line chart; threshold warnings (negative, cap) |
| Tech tree graph | Force-directed или hierarchical; nodes color-coded (built/in-progress/locked) |
| Action editor | Inline по timeline click + sidebar form |
| Drag-drop reorder | Reorderable; время авто-bump |
| Save/load | LocalStorage + export/import JSON (compatible с current build_order schema) |
| Compare mode | Two simulator instances, overlay curves разными цветами |
| Validation | Live warnings (red на negative resources, missing prereqs) |
| Suggest-next (опц.) | Кнопка "what's the optimal next action?" — micro-search |
| Map view (v2) | 2D top-down с mine positions, forest density, storehouse drop points |

### F. Тех-стек (3 опции)

**Option 1: Static HTML+JS (recommended for v1)**
- Pros: zero install, runs in browser, easy to share via static site, no server
- Cons: нужен порт симулятора с Python на JS (~500 LOC) ИЛИ Pyodide (~5MB download, медленнее)
- Stack: vanilla JS + chart.js + d3.js/cytoscape.js + custom Gantt или vis-timeline

**Option 2: Python+Tkinter desktop**
- Pros: reuse существующий симулятор directly, быстрее v1
- Cons: install required, less shareable, less polish on charts

**Option 3: Electron + Python backend**
- Pros: best of both
- Cons: complex, heavy

**Likely choice:** Option 1 для v1. Static files в `output/editor/index.html` читают `tech_tree.json` + `cossacks3_data.json` через fetch.

### G. Strategy library / community
| Item | Why |
|---|---|
| Starter pack: 5-10 build orders на нацию (early rush, eco boom, 18c tech, etc.) | Не пустой slate |
| Build order JSON schema versioning | Forward-compat |
| "Share via URL" (encode в querystring) | Расшарить с друзьями |
| Import/export to clipboard JSON | Power users iterate quickly |

---

## Roadmap (5 фаз)

### Phase 1: close blockers (items 4-9 of strategy roadmap)
- DPS/EHP таблицы → simulator extension + dedicated md output
- Counter-unit matrix → matrix md/json
- Time-to-X calculator → add to simulator
- Income/upkeep budget visualizer → add to sim CSV/MD
- Empirical peasant speed → in-game test → refine walk_overhead

### Phase 2: simulator polish (items A-C)
- Real walking distances (нужна map state model)
- Tree depletion + field regen cycles
- Cancel/refund action

### Phase 3: editor MVP (HTML+JS)
- Static page reading existing JSON files
- Timeline Gantt + resource curves
- Edit JSON build order через формы (без drag-drop)
- Live re-run симулятор on edit
- Validation warnings

### Phase 4: editor polish
- Tech tree graph view
- Drag-drop reorder
- Compare mode
- Map view с storehouse/mine positions
- Strategy library / starter pack

### Phase 5: community
- URL sharing
- Browser-side save/load

---

## Estimates (rough)

- Phase 1: 2-4 sessions (extending simulator + computation scripts)
- Phase 2: 2-3 sessions (bite-sized items)
- Phase 3: 4-6 sessions (порт симулятора на JS — самое крупное)
- Phase 4: 4-8 sessions (UI polish takes longer чем кажется)
- Phase 5: 1-2 sessions

**Total: 13-23 sessions** для полной версии. **MVP в конце Phase 3** уже useful — пользователь визуально создаёт стратегии с графиками, но без fancy graph view.

---

## Decision points (when activating)

1. Тех-стек (Option 1/2/3)?
2. Phase 1 priority (DPS first или Time-to-X first)?
3. Где hosting editor'а (`output/editor/`? gh-pages? Steam Workshop?)?
4. Multiplayer build orders (2 timelines одновременно для обоих игроков)?
5. Strategy library — curated или import community?
