import tomllib
from pydantic import BaseModel, ValidationError


class Pattern(BaseModel):
    pattern: str
    attributes: str | None = None
    foreground_color: str | None = None
    background_color: str | None = None


class Config(BaseModel):
    patterns: dict[str, Pattern]


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


def get_reset():
    return "\x1b[0m"


def get_foreground_color(color: str | None):
    if not color:
        return "\x1b[39m"

    # Use hex if available
    if color.startswith("#"):
        red = int(color[1:3], 16)
        green = int(color[3:5], 16)
        blue = int(color[5:7], 16)
        return f"\x1b[38;2;{red};{green};{blue}m"

    # Use preset if available
    if color in preset["colors"]:
        return f"\x1b[3{preset['colors'][color]}m"

    raise ValueError(f"Invalid background color: {color}")


def get_background_color(color: str | None):
    if not color:
        return "\x1b[49m"

    # Use hex if available
    if color.startswith("#"):
        red = int(color[1:3], 16)
        green = int(color[3:5], 16)
        blue = int(color[5:7], 16)
        return f"\x1b[48;2;{red};{green};{blue}m"

    # Use preset if available
    if color in preset["colors"]:
        return f"\x1b[4{preset['colors'][color]}m"

    raise ValueError(f"Invalid background color: {color}")


def get_attributes(attributes: str | None):
    if not attributes:
        return ""

    result: list[str] = []
    for attribute in attributes.split(","):
        attribute = attribute.strip()
        if attribute and attribute not in preset["attributes"]:
            raise ValueError(f"Invalid attribute: {attribute}")
        if attribute:
            result.append(f"\x1b[{preset['attributes'][attribute]}m")
    return "".join(result)


def load_config(config_path: str) -> Config:
    with open(config_path, "rb") as f:
        raw_config = tomllib.load(f)
    try:
        config = Config(**raw_config)

        keys = set[str]()
        for key, value in config.patterns.items():
            if key in keys:
                raise ValueError(f"Duplicate pattern key: {key}")

            keys.add(key)
            value.foreground_color = get_foreground_color(value.foreground_color)
            value.background_color = get_background_color(value.background_color)
            value.attributes = get_attributes(value.attributes)
    except ValidationError as e:
        raise ValueError(f"TOML validation error: {e}")
    return config
