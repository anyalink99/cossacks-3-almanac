# Cossacks 3 — Тренажёр стратегий (v0.2)

> ⚠ **СТАТУС: НЕ РАБОТАЕТ — work in progress.**
> Редактор в текущем виде сломан и не годится к использованию. Лежит в репо
> как заготовка, доделывается отдельной задачей. **Не использовать**, не
> ссылаться из других документов, не считать частью справочника.

Браузерный редактор билд-ордеров. Загружает игровые данные из `docs/data.json` и прогоняет симулятор экономики (`simulator/simulate_economy.py`) прямо в браузере через Pyodide.

## Что умеет

- ✅ **Полностью на русском.** Все UI-элементы, имена наций / зданий / юнитов / апгрейдов из локализации игры.
- ✅ **Действия выбираются мышкой**, без правки JSON:
  - **📦 Построить** — dropdown зданий нации с ценами, число строителей.
  - **👥 Обучить** — выбор здания-производителя, потом dropdown юнитов, доступных в нём.
  - **🔬 Исследовать** — апгрейды сгруппированы по месту (Академия / Кузница / Шахта золота / …).
  - **⛏ Раскидать крестьян** — раздельные поля для food/wood/stone/gold/iron/coal.
- ✅ **Live-симуляция** — кнопка ▶ Прогнать, результат через 100-300мс.
- ✅ **Графики**: ресурсы во времени, население / ферма cap.
- ✅ **Итоговая сводка** — карточки по 6 ресурсам + крестьяне / ферма / здания.
- ✅ **События** из симулятора (SKIP/WARN/ERROR подсвечены).
- ✅ **Save/load** в LocalStorage, экспорт/импорт JSON совместим с CLI.
- ✅ **Адаптивная вёрстка** — на узких экранах двух-колоночный layout сворачивается в одну.

## Как запустить

В корне репозитория:

```bash
python -m http.server 8000
```

Открой `http://localhost:8000/editor/`.

> ⚠ Не открывай `index.html` через `file://` — Pyodide и fetch'и ломятся на CORS.

Первая загрузка ~5-10 сек (Pyodide ~6MB кешируется браузером). Потом мгновенно.

## Структура

```
editor/
├── index.html
├── README.md
├── css/
│   └── editor.css           # Тёмная тема с золотыми акцентами
└── js/
    ├── main.js              # Точка входа, оркестратор UI
    ├── data_loader.js       # fetch data.json + tech_tree.json + builder_slots.json
    ├── pyodide_runner.js    # Pyodide bootstrap + simulate_in_memory
    ├── build_order.js       # Модель + LocalStorage + import/export
    └── ui/
        ├── i18n.js          # Русские названия, иконки ресурсов
        ├── catalog.js       # Per-nation выборки зданий/юнитов/апгрейдов
        ├── action_form.js   # Inline-форма добавления действий
        ├── action_list.js   # Карточки действий
        └── charts.js        # Chart.js обёртки
```

`simulator/simulate_economy.py` имеет функцию `simulate_in_memory(build_order, data, tree, slots) → dict`, тот же engine что и для CLI, без файлового IO.

## Что НЕ работает (план — `project_visual_editor_phase1_concrete.md`)

- ❌ Редактирование уже добавленного действия — пока только удаление + добавление заново.
- ❌ Drag-and-drop reorder списка действий.
- ❌ Timeline Gantt — только список карточек.
- ❌ Tech tree graph view — Phase 2.
- ❌ Compare mode (два билд-ордера side-by-side).
- ❌ Map view (нужен Level C симулятор).

## Sanity-check (CLI vs editor)

```bash
# CLI:
python simulator/simulate_economy.py simulator/build_orders/bav_basic_5min.json
# смотрим docs/simulations/sim_bav_basic_5min.csv → последняя строка
```

В редакторе: ⬆ Импорт JSON → выбрать `bav_basic_5min.json` → ▶ Прогнать. Финальные числа должны совпасть один-в-один (food=2001, wood=2870, peasants=15 для bav_basic_5min @ fast).
