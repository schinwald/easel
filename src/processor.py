from dataclasses import dataclass
import re
from typing import Literal

from .loader import Config


@dataclass
class Style:
    index: int
    type: Literal["start"] | Literal["end"]
    id: str
    attributes: str | None
    foreground_color: str | None
    background_color: str | None


def get_terminal_style(style: Style | None):
    if not style:
        return "\x1b[0m"

    return f"{style.foreground_color}{style.background_color}{style.attributes}"


def process_line(config: Config, line: str) -> str:
    styles: list[Style] = []
    for key, values in config.patterns.items():
        matching = re.search(values.pattern, line)
        if not matching:
            continue

        styles.append(
            Style(
                index=matching.start(),
                type="start",
                id=key,
                foreground_color=values.foreground_color,
                background_color=values.background_color,
                attributes=values.attributes,
            )
        )
        styles.append(
            Style(
                index=matching.end(),
                type="end",
                id=key,
                foreground_color=values.foreground_color,
                background_color=values.background_color,
                attributes=values.attributes,
            )
        )

    styles.sort(key=lambda x: x.index)
    queued = set[str]()

    result: list[str] = []
    applied: list[Style] = []
    previous = 0

    for style in styles:
        result.append(line[previous : style.index])

        if style.type == "start":
            # Add style to applied stack
            applied.append(style)
            result.append(get_terminal_style(style))
        elif style.type == "end":
            # Attempt to pop from stack if matching ids
            if applied and applied[-1].id == style.id:
                _ = applied.pop()

                # Derive next color from stack
                while applied and applied[-1].id in queued:
                    queued.remove(applied[-1].id)
                    _ = applied.pop()

                # Found the next color, now we need to apply it
                previous_style = applied[-1] if applied else None
                result.append(get_terminal_style(previous_style))
            else:
                queued.add(style.id)

        previous = style.index

    result.append(line[previous:])

    return "".join(result)
