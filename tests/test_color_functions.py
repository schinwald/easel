import pytest
from src.loader import get_foreground_color, get_background_color


class TestColorFunctions:
    def test_get_foreground_color_hex(self):
        assert get_foreground_color("#FF0000") == "\x1b[38;2;255;0;0m"

    def test_get_foreground_color_preset(self):
        assert get_foreground_color("red") == "\x1b[31m"

    def test_get_foreground_color_invalid(self):
        assert get_foreground_color("") == "\x1b[39m"
        with pytest.raises(ValueError):
            get_foreground_color("invalid")

    def test_get_background_color_hex(self):
        assert get_background_color("#00FF00") == "\x1b[48;2;0;255;0m"

    def test_get_background_color_preset(self):
        assert get_background_color("blue") == "\x1b[44m"

    def test_get_background_color_invalid(self):
        assert get_background_color("") == "\x1b[49m"