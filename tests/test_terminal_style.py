from src.processor import get_terminal_style, Style


class TestTerminalStyle:
    def test_get_terminal_style_none(self):
        assert get_terminal_style(None) == "\x1b[0m"

    def test_get_terminal_style_with_styles(self):
        style = Style(
            index=0,
            type="start",
            id="test",
            foreground_color="\x1b[31m",
            background_color="\x1b[42m",
            attributes="\x1b[1m",
        )
        assert get_terminal_style(style) == "\x1b[31m\x1b[42m\x1b[1m"