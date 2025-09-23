import pytest
from src.loader import get_foreground_color, get_background_color


class TestColorFunctions:
    def test_get_foreground_color_hex(self):
        """get_foreground_color returns the correct ANSI code for a hex color.

        Example:
            >>> get_foreground_color("#FF0000")
            '\\x1b[38;2;255;0;0m'
        """
        result = get_foreground_color("#FF0000")

        assert result == "\x1b[38;2;255;0;0m"

    def test_get_foreground_color_preset(self):
        """get_foreground_color returns the correct ANSI code for a preset color.

        Example:
            >>> get_foreground_color("red")
            '\\x1b[31m'
        """
        result = get_foreground_color("red")

        assert result == "\x1b[31m"

    def test_get_foreground_color_invalid(self):
        """get_foreground_color handles empty string and raises ValueError for invalid color.

        Example:
            >>> get_foreground_color("")
            '\\x1b[39m'
            >>> get_foreground_color("invalid")
            Traceback (most recent call last):
                ...
            ValueError
        """
        result = get_foreground_color("")

        assert result == "\x1b[39m"

        with pytest.raises(ValueError):
            get_foreground_color("invalid")

    def test_get_background_color_hex(self):
        """get_background_color returns the correct ANSI code for a hex color.

        Example:
            >>> get_background_color("#00FF00")
            '\\x1b[48;2;0;255;0m'
        """
        result = get_background_color("#00FF00")

        assert result == "\x1b[48;2;0;255;0m"

    def test_get_background_color_preset(self):
        """get_background_color returns the correct ANSI code for a preset color.

        Example:
            >>> get_background_color("blue")
            '\\x1b[44m'
        """
        result = get_background_color("blue")

        assert result == "\x1b[44m"

    def test_get_background_color_invalid(self):
        """get_background_color returns default for empty string.

        Example:
            >>> get_background_color("")
            '\\x1b[49m'
        """
        result = get_background_color("")

        assert result == "\x1b[49m"