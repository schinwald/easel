from src.processor import get_terminal_style, Style


class TestTerminalStyle:
    def test_get_terminal_style_none(self):
        """get_terminal_style returns reset code for None input.

        Example:
            >>> get_terminal_style(None)
            '\\x1b[0m'
        """
        result = get_terminal_style(None)

        assert result == "\x1b[0m"

    def test_get_terminal_style_with_styles(self):
        """get_terminal_style combines style components correctly.

        Example:
            >>> style = Style(
            ...     index=0,
            ...     type="start",
            ...     id="test",
            ...     foreground_color="[fg:red]",
            ...     background_color="[bg:green]",
            ...     attributes="[bold]"
            ... )
            >>> get_terminal_style(style)
            '[fg:red][bg:green][bold]'
        """
        style = Style(
            index=0,
            type="start",
            id="test",
            foreground_color="\x1b[31m",
            background_color="\x1b[42m",
            attributes="\x1b[1m",
        )
        result = get_terminal_style(style)

        assert result == "\x1b[31m\x1b[42m\x1b[1m"