"""Сноски-цитаты для compute-скриптов.

Convention:
    cites = Citations()
    L.append(f"Бонусы строя {cites.cite('lib/player.script:809-812')}")
    L.append(f"Распуск отряда — порог 25% {cites.cite('progress.inc:5-35', code='if count < ...')}")

    # at the end of the report:
    L.extend(cites.render())  # appends '## Источники' + footnote list

Same `target` deduplicates: повторный вызов `cite('lib/player.script:809-812')`
вернёт тот же `[^N]`-токен. Если в новом вызове передан код, а в первом
не было — код добавится к существующей сноске.

Формат сноски на выходе соответствует тому, что мы используем в handwritten
recon-файлах — see `docs/recon/world/target_selection.md` для эталона.
"""
from __future__ import annotations
from dataclasses import dataclass, field


@dataclass
class _CiteEntry:
    target: str
    label: str = ""
    code: str = ""


class Citations:
    """Накапливает сноски при рендере отчёта; в конце вызывает render()."""

    def __init__(self) -> None:
        self._items: list[_CiteEntry] = []
        self._index: dict[str, int] = {}  # target → 1-based number

    def cite(self, target: str, label: str = "", code: str = "") -> str:
        """Зарегистрировать цитату и вернуть `[^N]`-токен.

        target: путь и строки в виде "lib/file.script:NNN-MMM" (без обрамляющих
                backtick'ов — они добавятся при рендере).
        label:  короткий человекочитаемый заголовок (необязательно).
        code:   pascal-блок (без backtick'ов, без отступа). Многострочный.
        """
        if target not in self._index:
            self._index[target] = len(self._items) + 1
            self._items.append(_CiteEntry(target=target, label=label, code=code))
        else:
            entry = self._items[self._index[target] - 1]
            if not entry.label and label:
                entry.label = label
            if not entry.code and code:
                entry.code = code
        return f"[^{self._index[target]}]"

    def render(self) -> list[str]:
        """Вернуть список markdown-строк со списком сносок.

        Если ни одна сноска не зарегистрирована — возвращает пустой список.
        Иначе формирует раздел `## Источники` и список `[^N]: …` с кодом
        в теле сноски (когда передан).
        """
        if not self._items:
            return []
        lines: list[str] = ["", "## Источники", ""]
        lines.append(
            "Все ссылки относительно `data/scripts/` в установке Cossacks 3."
        )
        lines.append("")
        for n, entry in enumerate(self._items, start=1):
            head = f"[^{n}]: "
            if entry.label:
                head += f"{entry.label} — `{entry.target}`"
            else:
                head += f"`{entry.target}`"
            if entry.code:
                head += ":"
            else:
                head += "."
            lines.append(head)
            if entry.code:
                lines.append("")
                lines.append("    ```pascal")
                for code_line in entry.code.rstrip("\n").split("\n"):
                    lines.append(f"    {code_line}")
                lines.append("    ```")
            lines.append("")
        return lines


__all__ = ["Citations"]
