"""Extract Russian UI literals and build committed English dictionaries.

This is a maintainer command, not a runtime dependency. Browser tools import
the generated JavaScript modules synchronously and work fully offline after
their normal assets have loaded.

    python scripts/build_ui_translations.py
"""
from __future__ import annotations

import argparse
import concurrent.futures as futures
import json
import re
import sys
from html.parser import HTMLParser
from pathlib import Path

from build_english_docs import Protector, canonical_dictionary, translate_chunk


ROOT = Path(__file__).resolve().parent.parent
CYRILLIC_RE = re.compile(r"[\u0400-\u04ff]")
TAG_OR_TEMPLATE_RE = re.compile(r"<[^>]*>|\$\{[^}]*}")

TARGETS = {
    "replay-parser": (
        ROOT / "replay-parser",
        ROOT / "replay-parser" / "js" / "translations.en.js",
    ),
    "editor": (
        ROOT / "editor",
        ROOT / "editor" / "js" / "translations.en.js",
    ),
}

OVERRIDES = {
    "XVIII век": "18th century",
    "шаблонов генератора": "generator patterns",
    "Разбор реплеев": "Replay Analyzer",
    "Cossacks 3 — Разбор реплеев": "Cossacks 3 — Replay Analyzer",
    "Cossacks 3 — отчёт по реплею": "Cossacks 3 — Replay Report",
    "Анализ реплеев": "Replay analysis",
    "Разбор": "Analysis",
    "Разбор:": "Parsing:",
    "Разбираем": "Analyzing",
    "Ошибка при разборе": "Parsing error",
    "Ошибка разбора": "Parsing error",
    "Разложите партию по минутам — и карту по точкам.": "Explore the match minute by minute — and the map point by point.",
    "Изучайте порядок строительства, производство, торговлю, улучшения и расположение\n        объектов генерации карты.": "Study build orders, production, trade, upgrades, and the placement\n        of map-generation objects.",
    "Готов — загрузите .rep": "Ready — load a .rep file",
    "Готов — можно загрузить ещё": "Ready — you can load another replay",
    "Загрузка Pyodide…": "Loading Pyodide…",
    "Загрузка парсера…": "Loading parser…",
    "Загрузка движка…": "Loading engine…",
    "Загрузка данных…": "Loading data…",
    "Загрузка симулятора и парсера…": "Loading simulator and parser…",
    "Открыть .rep": "Open .rep",
    "Перетащите": "Drag",
    "выбрать файл": "choose a file",
    "Очистить": "Clear",
    "Закрыть": "Close",
    "Координаты": "Coordinates",
    "Игроки": "Players",
    "Карта": "Map",
    "Скорость": "Speed",
    "Объектов": "Objects",
    "Объектов внутри": "Objects inside",
    "Путь к маске": "Mask path",
    "Окружение": "Environment",
    "Схема": "Diagram",
    "Реестр размещённых фрагментов": "Placed-fragment registry",
    "Порядок строительства": "Build order",
    "Добыча ресурсов": "Resource gathering",
    "Обмен ресурсов": "Resource trade",
    "Исследование улучшений": "Upgrade research",
    "Исследование улучшения": "Research upgrade",
    "Применение улучшений": "Applying upgrades",
    "Улучшение": "Upgrade",
    "Улучшение №": "Upgrade no.",
    "Улучшения": "Upgrades",
    "Улучшения не распознаны.": "No upgrades recognized.",
    "Заказ отменён": "Order cancelled",
    "Заказано": "Queued",
    "· цель указана": "· target specified",
    "Неизвестное улучшение": "Unknown upgrade",
    "Двойных прокачек:": "Duplicate upgrades:",
    "Обнаружено эпизодов двойной прокачки:": "Duplicate-upgrade incidents detected:",
    "Повторных прокачек не обнаружено": "No duplicate upgrades detected",
    "двойные_прокачки": "duplicate_upgrades",
    "повторные клики": "repeated clicks",
    "Абуз": "Exploit",
    "Все события": "All events",
    "Вложенные события": "Nested events",
    "Прочие события": "Other events",
    "Появление объектов": "Object creation",
    "Создание объектов": "Object creation",
    "Служебная концовка файла не найдена.": "File trailer not found.",
    "Служебные настройки": "Internal settings",
    "Служебные остаточные данные": "Trailing internal data",
    "Служебные события": "Internal events",
    "Служебный объект": "Internal object",
    "Служебный таймер": "Internal timer",
    "Концовка файла": "File trailer",
    "Файл карты": "Map file",
    "Флаги карты": "Map flags",
    "Ход партии": "Match timeline",
    "Ход симуляции": "Simulation timeline",
    "Стороны": "Players",
    "Точки сбора": "Rally points",
    "Огонь по точке": "Fire at position",
    "Продолжение огня по точке": "Continue firing at position",
    "Отправка в шахту": "Enter mine",
    "Рыболовство": "Fishing",
    "Поиск цели": "Find target",
    "Перемещение": "Move",
    "Остановка": "Stop",
    "Охрана": "Guard",
    "Атака объекта": "Attack target",
    "Отмена очереди": "Cancel queue",
    "Отмена приказов": "Cancel orders",
    "Постройка стены": "Build wall",
    "Продолжение постройки стены": "Continue building wall",
    "Постройка ворот": "Build gate",
    "Строительство здания": "Build structure",
    "Производство юнита": "Train unit",
    "Производство юнитов": "Unit production",
    "Скачать JSON": "Download JSON",
    "Скачать CSV": "Download CSV",
    "Скачать TXT": "Download TXT",
    "Экспорт": "Export",
    "Сохранён": "Saved",
    "Ошибка:": "Error:",
    "Нет": "No",
    "Да": "Yes",
    "Не указано": "Not specified",
    "не определено": "not determined",
    "не определён": "not determined",
    "не определена": "not determined",
    "нация не определена": "nation not determined",
    "игрока": "players",
    "игроков": "players",
    "источник": "source",
    "источника": "sources",
    "источников": "sources",
    "категория": "category",
    "категории": "categories",
    "категорий": "categories",
    "постройка": "building",
    "построек": "buildings",
    "события": "events",
    "событий": "events",
    "строитель": "builder",
    "строителя": "builders",
    "строителей": "builders",
    "точка": "point",
    "точки": "points",
    "точек": "points",
    "улучшение": "upgrade",
    "улучшений": "upgrades",
    "юнит": "unit",
    "юнита": "units",
    "юнитов": "units",
    "мс": "ms",
    "распознано в реплее": "recognized in replay",
    "Проверены команды исследования и применения улучшений.": "Upgrade research and application commands verified.",
    "версия игры": "game version",
    "длительность_игровые_секунды": "duration_game_seconds",
    "время_игровые_секунды": "time_game_seconds",
    "высота_карты": "map_height",
    "высота_шаблона": "pattern_height",
    "ширина_карты": "map_width",
    "ширина_шаблона": "pattern_width",
    "имя_шаблона": "pattern_name",
    "позиция_в_файле": "file_offset",
    "число_объектов": "object_count",
    "фрагменты_карты": "map_fragments",
    "Тренажёр стратегий": "Build Order Planner",
    "Cossacks 3 — Тренажёр стратегий": "Cossacks 3 — Build Order Planner",
    "▶ Прогнать": "▶ Run",
    "Графики": "Charts",
    "Действие": "Action",
    "Действия": "Actions",
    "Действий:": "Actions:",
    "Итог": "Summary",
    "Обучить": "Train",
    "Исследовать": "Research",
    "Исследовать:": "Research:",
    "Раскидать": "Assign",
    "Реплей →": "Replay →",
    "Сброс": "Reset",
    "Кол-во": "Quantity",
    "Количество": "Quantity",
    "Параметры карты": "Map settings",
    "Правила игры": "Game rules",
    "Размер карты": "Map size",
    "Скорость партии": "Game speed",
    "Сложность ИИ": "AI difficulty",
    "Стартовая армия": "Starting army",
    "Стартовые ресурсы": "Starting resources",
    "Крестьян на старте": "Starting peasants",
    "Показать ресурсы поштучно": "Show individual resources",
    "Доп. настройки сценария": "Additional scenario settings",
    "Время начала (г-сек)": "Start time (game seconds)",
    "ВРЕМЯ (г-сек)": "TIME (game seconds)",
    "Окно (г-минут)": "Window (game minutes)",
    "px/г-сек": "px/game sec",
    "2 px/g-сек": "2 px/game sec",
    "Готов · нажми «Прогнать»": "Ready · click “Run”",
    "Клик по пункту — добавить в билд-ордер. Время подбирается автоматически на самый ранний валидный момент.": "Click an item to add it to the build order. Its time is set to the earliest valid moment automatically.",
    "Кликни по точке на таймлайне или добавь действие из левого каталога.": "Click a point on the timeline or add an action from the catalog on the left.",
    "Кликни по точке на таймлайне, чтобы редактировать действие.": "Click a point on the timeline to edit the action.",
    "Нажми «Прогнать» сверху, чтобы увидеть результат.": "Click “Run” above to see the result.",
    "К этому времени крестьян всего:": "Total peasants at this time:",
    "Обмен на рынке": "Market trade",
    "Запланируй постройку рынка.": "Schedule construction of a Market.",
    "Переход в 18 век": "Advance to the 18th century",
    "Тип ландшафта": "Terrain type",
    "Строителей": "Builders",
    "строителей": "builders",
    "юнитов": "units",
    "снимков": "snapshots",
    "ед.": "units",
    "Беск. производство:": "Infinite production:",
    "(своё)": "(custom)",
    "Стр": "Bld",
    "Об": "Trn",
    "Иc": "Rch",
    "Исс": "Rch",
    "Рк": "Asn",
    "Расп": "Asn",
    "Тор": "Trd",
    "Режим": "Mode",
    "Рельеф": "Relief",
    "Шахт": "Mines",
    "Шахта железа": "Iron mine",
    "Шахта золота": "Gold mine",
    "Шахта угля": "Coal mine",
    "Дипцентр": "Diplomatic Center",
    "Арт. депо": "Artillery Depot",
    "Казарма 17в": "17th-century Barracks",
    "Казарма 18в": "18th-century Barracks",
    "Активно с t=": "Active from t=",
    "г · Готово: t=": " game sec · Complete: t=",
    "г свободно": " game sec: available",
    "г, до конца": " game sec, until the end",
    "г.": " game sec",
    "г": " game sec",
    "в": "in",
    "— тяни мышкой чтобы изменить время —": "— drag to change the time —",
    "⚙ Настройки": "⚙ Settings",
    "🔒 нет плана": "🔒 no plan",
    "🔒 нужен рынок": "🔒 Market required",
    "Городской центр": "Town Hall",
    "Порт": "Shipyard",
    "Апгр.": "Upgrades",
    "г-сек": "g-sec",
    "игров. сек.": "game sec.",
    "Беск. производство": "Infinite production",
    "Раскидать крестьян": "Assign peasants",
    "Разбор выполняется локально": "Parsed locally",
    ".\n    Формат разобран в": ".\nThe format is documented in",
    "Положите реплей на стол": "Drop a replay here",
    "Открытый реплей": "Open replay",
    "Двойная прокачка": "Duplicate upgrade",
    "Рынок и дипцентр": "Market and Diplomatic Center",
    "Пушки/башни/стены": "Cannons, towers, and walls",
    "Воздушные шары": "Balloons",
}


def javascript_strings(source: str) -> list[str]:
    """Return JS string/template literal bodies without being confused by quotes.

    This is intentionally a small lexer rather than a JavaScript parser. UI
    messages do not need AST information, but regular expressions are unsafe
    here because a quote of another kind can occur inside a literal.
    """
    result: list[str] = []
    index = 0
    length = len(source)
    while index < length:
        char = source[index]
        next_char = source[index + 1] if index + 1 < length else ""
        if char == "/" and next_char == "/":
            newline = source.find("\n", index + 2)
            index = length if newline < 0 else newline + 1
            continue
        if char == "/" and next_char == "*":
            closing = source.find("*/", index + 2)
            index = length if closing < 0 else closing + 2
            continue
        if char not in {'"', "'", "`"}:
            index += 1
            continue
        quote = char
        index += 1
        buffer: list[str] = []
        while index < length:
            char = source[index]
            if quote != "`" and char in "\r\n":
                # A raw newline cannot occur in a normal JS string. Re-sync
                # after regex literals that happen to contain a quote.
                buffer = []
                break
            if char == "\\" and index + 1 < length:
                buffer.extend((char, source[index + 1]))
                index += 2
                continue
            if char == quote:
                index += 1
                break
            buffer.append(char)
            index += 1
        if buffer:
            value = "".join(buffer)
            result.append(value)
            # Template expressions may contain their own quoted UI forms,
            # notably plural arrays such as ["игрок", "игрока", "игроков"].
            if quote == "`" and "${" in value:
                result.extend(javascript_strings(value))
    return result


class UiHtmlParser(HTMLParser):
    """Collect visible text and user-facing attribute values."""

    ATTRIBUTES = {"title", "placeholder", "aria-label", "alt"}

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.values: list[str] = []

    def handle_data(self, data: str) -> None:
        self.values.append(data)

    def handle_starttag(
        self,
        tag: str,
        attrs: list[tuple[str, str | None]],
    ) -> None:
        for name, value in attrs:
            if name in self.ATTRIBUTES and value:
                self.values.append(value)


def extract_phrases(source_root: Path) -> list[str]:
    phrases: set[str] = set()
    for path in source_root.rglob("*"):
        if path.suffix not in {".js", ".html"} or path.name == "translations.en.js":
            continue
        text = path.read_text(encoding="utf-8")
        values: list[str]
        if path.suffix == ".html":
            parser = UiHtmlParser()
            parser.feed(text)
            values = parser.values
        else:
            values = javascript_strings(text)
        for value in values:
            if not CYRILLIC_RE.search(value):
                continue
            for part in TAG_OR_TEMPLATE_RE.split(value):
                part = part.replace("\\n", "\n").strip()
                if CYRILLIC_RE.search(part):
                    phrases.add(part)
    return sorted(phrases, key=lambda value: (-len(value), value))


def translate_phrases_google(phrases: list[str]) -> dict[str, str]:
    canonical = canonical_dictionary()
    result = {source: target for source, target in OVERRIDES.items() if source in phrases}
    pending = [phrase for phrase in phrases if phrase not in result]
    batches: list[list[str]] = []
    current: list[str] = []
    size = 0
    for phrase in pending:
        if current and size + len(phrase) > 3200:
            batches.append(current)
            current = []
            size = 0
        current.append(phrase)
        size += len(phrase) + 24
    if current:
        batches.append(current)

    def translate_batch(index_and_batch: tuple[int, list[str]]) -> dict[str, str]:
        index, batch = index_and_batch
        separator = f"\nZXQSEP{index:05d}QXZ\n"
        translated = translate_chunk(separator.join(batch), canonical)
        parts = translated.split(separator)
        if len(parts) != len(batch):
            # Rare service-side whitespace folding: retry this small batch
            # phrase-by-phrase rather than producing a shifted dictionary.
            return {
                source: translate_chunk(source, canonical).strip()
                for source in batch
            }
        return {
            source: target.strip()
            for source, target in zip(batch, parts)
        }

    with futures.ThreadPoolExecutor(max_workers=6) as pool:
        tasks = [
            pool.submit(translate_batch, item)
            for item in enumerate(batches)
        ]
        for index, task in enumerate(futures.as_completed(tasks), 1):
            result.update(task.result())
            print(f"  batch {index}/{len(tasks)}", flush=True)
    return dict(sorted(result.items()))


def translate_phrases_argos(phrases: list[str]) -> dict[str, str]:
    try:
        import argostranslate.translate
    except ImportError as error:
        raise RuntimeError(
            "Argos Translate is not installed. Install argostranslate and its "
            "Russian → English model, or run with --engine google."
        ) from error

    canonical = canonical_dictionary()
    result = {source: target for source, target in OVERRIDES.items() if source in phrases}
    pending = [phrase for phrase in phrases if phrase not in result]
    for index, source in enumerate(pending, 1):
        protector = Protector(canonical)
        protected = protector.protect(source)
        translated = argostranslate.translate.translate(protected, "ru", "en")
        # The current ru→en model trims the final Z from our placeholder.
        # Restore it before handing the text back to the shared protector.
        for marker in protector.restore:
            shortened = marker[:-1]
            if marker not in translated and shortened in translated:
                translated = translated.replace(shortened, marker)
        result[source] = protector.unprotect(translated).strip()
        if index % 25 == 0 or index == len(pending):
            print(f"  phrase {index}/{len(pending)}", flush=True)
    return dict(sorted(result.items()))


def write_module(path: Path, translations: dict[str, str]) -> None:
    payload = json.dumps(translations, ensure_ascii=False, indent=2)
    path.write_text(
        "// Generated by scripts/build_ui_translations.py; edit OVERRIDES there.\n"
        f"export default Object.freeze({payload});\n",
        encoding="utf-8",
    )


def read_module(path: Path) -> dict[str, str]:
    text = path.read_text(encoding="utf-8")
    prefix = "export default Object.freeze("
    if prefix not in text or not text.rstrip().endswith(");"):
        raise ValueError(f"unexpected translation module format: {path}")
    payload = text.split(prefix, 1)[1].rsplit(");", 1)[0]
    result = json.loads(payload)
    if not isinstance(result, dict):
        raise ValueError(f"translation module must contain an object: {path}")
    return {str(source): str(target) for source, target in result.items()}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--check",
        action="store_true",
        help="verify that committed dictionaries cover every Russian UI literal",
    )
    parser.add_argument(
        "--engine",
        choices=("argos", "google"),
        default="google",
        help="Draft translation engine; canonical overrides are always applied.",
    )
    args = parser.parse_args()
    errors: list[str] = []
    for name, (source_root, target) in TARGETS.items():
        phrases = extract_phrases(source_root)
        if args.check:
            if not target.is_file():
                errors.append(f"missing dictionary: {target.relative_to(ROOT)}")
                continue
            translations = read_module(target)
            missing = sorted(set(phrases) - set(translations))
            untranslated = sorted(
                source for source, value in translations.items()
                if CYRILLIC_RE.search(value)
            )
            if missing:
                errors.append(
                    f"{name}: {len(missing)} missing phrase(s): {missing[:5]}"
                )
            if untranslated:
                errors.append(
                    f"{name}: {len(untranslated)} English value(s) contain Cyrillic: "
                    f"{untranslated[:5]}"
                )
            print(
                f"{name}: {len(translations)} translations, "
                f"{len(missing)} missing",
                flush=True,
            )
            continue
        print(f"{name}: {len(phrases)} phrases", flush=True)
        if args.engine == "argos":
            translations = translate_phrases_argos(phrases)
        else:
            translations = translate_phrases_google(phrases)
        write_module(target, translations)
        print(f"wrote {target.relative_to(ROOT)}", flush=True)
    if errors:
        print("\n".join(errors), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
