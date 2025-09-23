import pytest
from src.loader import get_attributes


class TestAttributes:
    def test_get_attributes_single(self):
        assert get_attributes("bold") == "\x1b[1m"

    def test_get_attributes_multiple(self):
        assert get_attributes("bold,italic") == "\x1b[1m\x1b[3m"

    def test_get_attributes_empty(self):
        assert get_attributes("") == ""

    def test_get_attributes_invalid(self):
        with pytest.raises(ValueError, match="Invalid attribute: invalid"):
            get_attributes("invalid")

