import pytest
from src.loader import load_config


class TestLoadConfig:
    def test_load_config_valid(self, tmp_path):
        """load_config correctly parses a valid TOML configuration.

        Example:
            config_content = '''
            [patterns.test]
            pattern = "test"
            foreground_color = "#FF0000"
            background_color = "green"
            attributes = "bold"
            '''
            >>> config = load_config("path/to/config.toml")
            >>> config.patterns["test"].foreground_color
            '\\x1b[38;2;255;0;0m'
        """
        config_content = """
[patterns.test]
pattern = "test"
foreground_color = "#FF0000"
background_color = "green"
attributes = "bold"
"""
        config_file = tmp_path / "test.toml"
        config_file.write_text(config_content)
        config = load_config(str(config_file))

        assert "test" in config.patterns
        assert config.patterns["test"].foreground_color == "\x1b[38;2;255;0;0m"
        assert config.patterns["test"].background_color == "\x1b[42m"
        assert config.patterns["test"].attributes == "\x1b[1m"

    def test_load_config_invalid_toml(self, tmp_path):
        """load_config raises ValueError for invalid TOML.

        Example:
            >>> load_config("invalid.toml")
            Traceback (most recent call last):
                ...
            ValueError
        """
        config_file = tmp_path / "invalid.toml"
        config_file.write_text("invalid toml")

        with pytest.raises(ValueError):
            load_config(str(config_file))

    def test_load_config_invalid_attribute(self, tmp_path):
        """load_config raises ValueError for invalid attribute in config.

        Example:
            config_content = '''
            [patterns.test]
            pattern = "test"
            attributes = "invalid"
            '''
            >>> load_config("path/to/config.toml")
            Traceback (most recent call last):
                ...
            ValueError: Invalid attribute: invalid
        """
        config_content = """
[patterns.test]
pattern = "test"
foreground_color = "#FF0000"
background_color = ""
attributes = "invalid"
"""
        config_file = tmp_path / "test.toml"
        config_file.write_text(config_content)

        with pytest.raises(ValueError, match="Invalid attribute: invalid"):
            load_config(str(config_file))

