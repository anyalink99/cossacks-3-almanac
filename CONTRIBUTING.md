# Contributing

[English](CONTRIBUTING.en.md) · **Русский**

Этот документ — короткая шпаргалка по тому, как устроен репозиторий и где
что трогать. Если ты только пришёл, начни с [`internals/project/architecture.md`](internals/project/architecture.md)
— там диаграмма потока данных и принципы. Этот файл отвечает на конкретные
«как мне…» вопросы.

Для любых новых или изменяемых статей также обязательны
[правила читательской документации](internals/project/documentation_style.md).

## Перед началом работы

```bash
# Окружение: Python 3.11+, ничего больше (только stdlib).
# Игра: Cossacks 3 в стандартном Steam-пути либо переменная COSSACKS3_PATH.

# Проверь что pipeline вообще работает:
python -m unittest discover -s tests -v
python scripts/regen.py sanity   # парсер + 112 авто-проверок
```

CI на каждый PR прогоняет smoke-тесты, проверяет что `canonical_terms.json`
и `data.json` не сломаны и что `parser/config.py` импортируется.

## Где трогать что

| Хочу… | Иду в… |
|---|---|
| **Поправить русский лейбл нации/здания/опции** | НЕТ. Оно из локали игры. Поправь либо локаль (если у тебя свой мод), либо запусти `python parser/build_canonical_terms.py` после патча игры. |
| **Поправить формулу / число в справочнике** | Найди источник: парсер (если из `data.json`), compute-скрипт (если расчётное), шаблон (если ручная проза в reference/). Никогда не редактируй сгенерированный md в `docs/reference/` или `docs/reports/` — он будет переписан. |
| **Добавить новый раздел в reference** | Шаблон — в [`writers/templates/reference/<chapter>/`](writers/templates/reference/). Логика рендера — в [`writers/write_md_tree.py`](writers/write_md_tree.py). |
| **Добавить новый отчёт** | Создай `compute/compute_<тема>.py` по образцу соседних. Эмить в `docs/reports/<раздел>/<имя>.md`. Зарегистрируй в `scripts/regen.py` (`reports-*` target). Если новый раздел — добавь папку в `docs/reports/` и упомяни в `docs/reports/README.md`. |
| **Добавить новый JSON-датасет** | Парсер — в `parser/parse_<X>.py` (если читает игровые файлы) или `compute/compute_<X>.py` (если считает из `data.json`). Эмить в `derived/<имя>.json`. Опиши в [`derived/README.md`](derived/README.md). |
| **Поправить прозу в recon** | Прямо в файлах `docs/recon/*.md` — они handwritten. |
| **Поправить прозу в reference** | Шаблоны в `writers/templates/reference/<chapter>/*.md`. Перегенерируй: `python writers/write_md_tree.py`. |
| **Добавить тест** | Новый файл в `tests/test_<тема>.py`. Стандартный `unittest`, без зависимостей. |

## Правила

1. **Источник правды — файлы игры.** Никаких вручную выдуманных переводов
   или цифр. Если расходится с внешним гайдом — доверяй коду игры.
2. **Идемпотентность.** `python scripts/regen.py all` должен перегенерировать
   всё с нуля. Если ваша правка ломает идемпотентность — это баг.
3. **Канонические русские названия — через `parser/config.py`.** Никогда не
   хардкодь `NATION_NAMES = {...}` или `USAGE_RU = {...}` в новом скрипте.
   Импортируй: `from config import nation_label, USAGE_RU, decode_usage`.
   Если нужного маппинга там нет — добавь в config + canonical_terms.json,
   а не в свой скрипт.
4. **Не редактируй auto-generated md.** Список auto-gen файлов:
   - `data.json`
   - `derived/*.json`
   - `docs/reference/**/*.md`
   - `docs/reports/**/*.md`
   - `docs/README.md` (генерируется из `writers/templates/output_readme.md`)
   - `internals/engine/native_primitives.md` (генерируется из `parser/engine_recon/extract_dws_signatures.py`)

   Handwritten — значит править вручную:
   - `README.md`, `CONTRIBUTING.md` (top-level).
   - `internals/project/architecture.md`, `internals/project/known_issues*.md`,
     `docs/reports/README.md`, `docs/reference/README.md` (writer пишет
     краткую шапку, остальное руками).
   - `docs/recon/**/*.md` (включая README) — handwritten reverse-engineering.
   - `internals/**/*.md` (кроме `native_primitives.md`) — handwritten техническая
     документация движка / скриптов / `data/`-каталога.
   - `derived/README.md` — handwritten.
   - `mods/**/README.md` — handwritten.
5. **Sanity checks.** `parser/build_data.py` гоняет 112 проверок. Если упало
   — сначала разберись, ПОТОМ правь. Просто отключать проверку нельзя.
6. **Без эмодзи** в коде / документах, если не просили. С 🚫 за поведение
   движка можно эмодзи (✅/❌ в таблицах) — но не везде.
7. **Читательское название всегда важнее внутреннего кода.** Каноническое
   имя ставится первым, SID и поля — вторично в `code`; русская проза не
   смешивается с английским жаргоном. Полные правила и примеры:
   [`internals/project/documentation_style.md`](internals/project/documentation_style.md).
8. **Английская документация переводится вручную.** После правки обнови
   соответствующий файл в `docs_en/` или `internals_en/`, проверь пару и
   только затем выполни `python scripts/build_english_docs.py --adopt-existing`.
   Машинный перевод для публикуемого текста не используется.

## Как делается изменение

```bash
# 1. Меняешь источник (парсер / compute / шаблон / handwritten md).
# 2. Перегенерируешь то, что зависит:
python scripts/regen.py all       # полный круг (~4 мин)
# или точечно:
python scripts/regen.py reference
python scripts/regen.py reports-economy

# 3. Проверяешь:
python -m unittest discover -s tests
python scripts/regen.py sanity    # 112/112 PASS

# 4. Коммит. Логические коммиты, без co-authoring.
git add <files>
git commit -m "<краткое сообщение>"
```

## Стиль коммитов

`<type>(<scope>): <message>` (мягкая конвенция, без жёсткого linter'а):

- `feat(config): centralize Russian glossary`
- `refactor(generators): use canonical names`
- `chore(prose): clean kalki and unify time units`
- `chore(legacy): remove old monolithic reference`
- `docs: add architecture and derived/README`
- `fix(parser): bmercenary block extraction`

Body коммита — что и почему изменилось. Если меняешь несколько файлов одной
правкой — перечисляй главные.

## Когда сомневаешься

- Архитектура и потоки данных — [`internals/project/architecture.md`](internals/project/architecture.md).
- Канонические термины — [`derived/canonical_terms.json`](derived/canonical_terms.json) +
  [`parser/config.py`](parser/config.py).
- Известные пробелы — [`internals/project/known_issues.md`](internals/project/known_issues.md).
- Что куда генерится — [`derived/README.md`](derived/README.md) +
  [`docs/reports/README.md`](docs/reports/README.md) + [`scripts/regen.py`](scripts/regen.py).
