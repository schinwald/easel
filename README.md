# Easel

A terminal text highlighter that applies ANSI escape codes to input text based on regex patterns defined in TOML config files.

## Usage

```bash
cat input.txt | python main.py config.toml
```

## Config Format

TOML file with patterns section:

```toml
[patterns.name]
pattern = "regex"
attributes = "bold,italic"
foreground_color = "red"
background_color = "black"
```

Colors can be names (red, blue, etc.) or hex (#ff0000).