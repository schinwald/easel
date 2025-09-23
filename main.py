from dataclasses import dataclass
import re
import tomllib
import sys
from typing import Literal
from pydantic import BaseModel, ValidationError


class Pattern(BaseModel):
    pattern: str
    attributes: str
    foreground_color: str
    background_color: str


class Config(BaseModel):
    patterns: dict[str, Pattern]


# Load configuration from TOML file
with open("./test/test1.toml", "rb") as f:
    raw_config = tomllib.load(f)


preset = {
    "colors": {
        "black": 0,
        "red": 1,
        "green": 2,
        "yellow": 3,
        "blue": 4,
        "magenta": 5,
        "cyan": 6,
        "white": 7,
    },
    "attributes": {
        "bold": 1,
        "dim": 2,
        "italic": 3,
        "underline": 4,
        "blink": 5,
        "reverse": 7,
        "hidden": 8,
    },
}


def get_foreground_color(color: str):
    # Use hex if available
    if color.startswith("#"):
        red = int(color[1:3], 16)
        green = int(color[3:5], 16)
        blue = int(color[5:7], 16)
        return f"\x1b[38;2;{red};{green};{blue}m"

    # Use preset if available
    if color in preset["colors"]:
        return f"\x1b[3{preset['colors'][color]}m"

    # Otherwise reset
    return "\x1b[39m"


def get_background_color(color: str):
    # Use hex if available
    if color.startswith("#"):
        red = int(color[1:3], 16)
        green = int(color[3:5], 16)
        blue = int(color[5:7], 16)
        return f"\x1b[48;2;{red};{green};{blue}m"

    # Use preset if available
    if color in preset["colors"]:
        return f"\x1b[4{preset['colors'][color]}m"

    # Otherwise reset
    return "\x1b[49m"


def get_attributes(attributes: str):
    result: list[str] = []
    for attribute in attributes.split(","):
        if attribute not in preset["attributes"]:
            raise ValueError(f"Invalid attribute: {attribute}")
        result.append(f"\x1b[{preset['attributes'][attribute]}m")
    return "".join(result)


# Validate TOML
try:
    config = Config(**raw_config)
    for key, value in config.patterns.items():
        value.foreground_color = get_foreground_color(value.foreground_color)
        value.background_color = get_background_color(value.background_color)
        value.attributes = get_attributes(value.attributes)
except ValidationError as e:
    print(f"TOML validation error: {e}")
    sys.exit(1)


@dataclass
class Style:
    index: int
    type: Literal["start"] | Literal["end"]
    id: str
    attributes: str
    foreground_color: str
    background_color: str


def get_terminal_style(style: Style | None):
    if not style:
        return "\x1b[0m"

    return f"{style.foreground_color}{style.background_color}{style.attributes}"


styles: list[Style] = []

# Process input lines
for line in sys.stdin:
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

        match style.type:
            case "start":
                # Add style to applied stack
                applied.append(style)
                result.append(get_terminal_style(style))
            case "end":
                # Attempt to pop from stack if matching ids
                if applied and applied[-1].id == style.id:
                    _ = applied.pop()

                    # Derrive next color from stack
                    while applied and applied[-1].id in queued:
                        _ = applied.pop()
                        queued.remove(applied[-1].id)

                    # Found the next color, now we need to apply it
                    previous_style = applied[-1] if applied else None
                    result.append(get_terminal_style(previous_style))
                # Otherwise, add to another queue
                else:
                    queued.add(style.id)

        previous = style.index

    result.append(line[previous:])
    print("".join(result))
