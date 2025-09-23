![Logo](/logo.png)

# 🎨 Easel

A powerful, flexible terminal text highlighter that applies ANSI escape codes to input streams based on regex patterns defined in TOML configuration files. Perfect for colorizing logs, outputs, and any text data in your terminal.

## ✨ Features

- **Regex-Based Pattern Matching**: Use powerful regular expressions to match and highlight text.
- **Rich Color Support**: Supports named colors (red, blue, green, etc.) and hex codes (#FF0000).
- **Text Attributes**: Apply bold, italic, underline, blink, and more.
- **Composable Styles**: Combine foreground colors, background colors, and attributes.
- **Streaming Input**: Processes text from stdin, making it ideal for piping with other commands.
- **TOML Configuration**: Easy-to-read and write configuration files.
- **Extensible**: Add new patterns and styles without code changes.
- **Fast and Lightweight**: Minimal dependencies, optimized for performance.

## 📦 Installation

### Prerequisites

- uv for package management

## 🚀 Usage

Pipe text through Easel with a configuration file:

```bash
cat input.txt | uv run main.py --config config.toml
```

## ⚙️ Configuration Format

Easel uses TOML files for configuration. Each pattern is defined in the `[patterns]` section:

```toml
[patterns.name]
pattern = "regex"
foreground_color = "red"          # Optional: named color or hex (#FF0000)
background_color = "black"        # Optional: named color or hex
attributes = "bold,italic"        # Optional: comma-separated list
```

### Supported Colors

Preset colors
- black
- red
- green
- yellow
- blue
- magenta
- cyan
- white

> [!note]
> Preset colors will match your terminal's color scheme and is the preferred way to use colors.

Custom colors
- hex (#FF0000)

### Supported Attributes

- bold
- dim
- italic
- underline
- blink
- reverse
- hidden

### Advanced Patterns

Use regex groups, anchors, and quantifiers for complex matching:

```toml
[patterns.ip_address]
pattern = "\\b\\d{1,3}\\.\\d{1,3}\\.\\d{1,3}\\.\\d{1,3}\\b"
foreground_color = "#0000FF"

[patterns.timestamp]
pattern = "^\\d{4}-\\d{2}-\\d{2} \\d{2}:\\d{2}:\\d{2}"
foreground_color = "#808080"
```

## 📚 Examples

The `examples/` directory contains sample configurations for popular tools:

## 🛠️ Development Setup

### Prerequisites

- uv (dependency management)

### Setup

2. Install dependencies:
   ```bash
   uv sync
   ```

3. Run tests:
   ```bash
   uv run pytest
   ```

4. Lint code:
   ```bash
   uv run ruff check .
   uv run ruff format .
   ```

### Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Write tests for your changes
4. Ensure all tests pass: `uv run pytest`
5. Format code: `uv run ruff format .`
6. Submit a pull request

### Testing

Easel uses pytest for testing with comprehensive doctests:

```bash
# Run all tests
uv run pytest

# Run with coverage
uv run pytest --cov=src

# Run specific test file
uv run pytest tests/test_process_lines.py
```

## 💡 Motivation

In the world of software development, logs and terminal output are crucial for debugging and monitoring. However, raw text can be overwhelming, especially with large volumes of data. Traditional tools like `grep` or `awk` provide basic filtering, but lack visual distinction.

Easel was born from the need for a simple, powerful way to add visual structure to text streams. By leveraging regex patterns and ANSI colors, developers can quickly identify important information, spot errors, and understand log flows at a glance.

Key design principles:
- **Simplicity**: TOML configs are human-readable and easy to modify
- **Performance**: Minimal overhead for real-time processing
- **Flexibility**: Regex patterns can match complex text structures
- **Composability**: Mix and match colors and styles
- **Universality**: Works with any text stream, not tied to specific tools

## 🔮 Future Plans

- [ ] **Performance Optimizations**: Further reduce processing latency for high-throughput logs
- [ ] **Advanced Pattern Matching**: Support for lookbehinds/lookaheads, named groups
- [ ] **Theme System**: Predefined color schemes for different use cases
- [ ] **Multi-format Support**: JSON, YAML, XML configs in addition to TOML
- [ ] **Multi-line Formatting**: Support regex on multiple lines

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## ⚠️ Disclaimer

Easel is designed for enhancing terminal output readability and should not be used for security-critical color-based parsing. ANSI escape codes may not display correctly in all terminal environments. Always verify output independently for production use.

While Easel uses regex patterns for text matching, it does not guarantee perfect parsing of complex log formats. Test configurations thoroughly with your specific data sources.

The authors are not responsible for any issues arising from the use of this software. Use at your own risk.
