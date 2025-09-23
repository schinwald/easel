import pytest
from src.loader import get_attributes


class TestAttributes:
    def test_get_attributes_single(self):
        """get_attributes returns the correct ANSI code for a single attribute.

        Example:
            >>> get_attributes("bold")
            '\\x1b[1m'
        """
        result = get_attributes("bold")

        assert result == "\x1b[1m"

    def test_get_attributes_multiple(self):
        """get_attributes returns combined ANSI codes for multiple attributes.

        Example:
            >>> get_attributes("bold,italic")
            '\\x1b[1m\\x1b[3m'
        """
        result = get_attributes("bold,italic")

        assert result == "\x1b[1m\x1b[3m"

    def test_get_attributes_empty(self):
        """get_attributes returns an empty string for no attributes.

        Example:
            >>> get_attributes("")
            ''
        """
        result = get_attributes("")

        assert result == ""

    def test_get_attributes_invalid(self):
        """get_attributes raises ValueError for an invalid attribute.

        Example:
            >>> get_attributes("invalid")
            Traceback (most recent call last):
                ...
            ValueError: Invalid attribute: invalid
        """

        with pytest.raises(ValueError, match="Invalid attribute: invalid"):
            get_attributes("invalid")

