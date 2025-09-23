from src.processor import process_line
from src.loader import (
    Config,
    Pattern,
    get_foreground_color,
    get_background_color,
    get_attributes,
    get_reset,
)


class TestProcessLines:
    def test_process_lines_no_matches(self):
        """lines with no matching patterns are returned unchanged.

        Example:
            >>> config = Config(patterns={})
            >>> process_line(config, "hello world")
            'hello world'
        """
        config = Config(patterns={})
        lines = ["hello world"]
        result = [process_line(config, line) for line in lines]

        assert result == ["hello world"]

    def test_process_lines_single_match(self):
        """a single pattern match applies the correct styling.

        Example:
            >>> config = Config(patterns={
            ...     "test": Pattern(
            ...         pattern="fox",
            ...         foreground_color="[fg:red]",
            ...         background_color="",
            ...         attributes=""
            ...     )
            ... })
            >>> process_line(config, "The quick brown fox jumps over the lazy dog.")
            'The quick brown [fg:red]fox[fg:reset] jumps over the lazy dog.'
        """
        config = Config(
            patterns={
                "test": Pattern(
                    pattern="fox",
                    foreground_color=get_foreground_color("red"),
                    background_color="",
                    attributes="",
                )
            }
        )
        lines = ["The quick brown fox jumps over the lazy dog."]
        result = [process_line(config, line) for line in lines]

        expected = f"The quick brown {get_foreground_color('red')}fox{get_reset()} jumps over the lazy dog."
        assert result == [expected]

    def test_process_lines_multiple_matches(self):
        """multiple non-overlapping patterns are styled correctly.

        Example:
            >>> config = Config(patterns={
            ...     "fox": Pattern(
            ...         pattern="fox",
            ...         foreground_color="[fg:red]"
            ...     ),
            ...     "dog": Pattern(
            ...         pattern="dog",
            ...         foreground_color="[fg:green]"
            ...     )
            ... })
            >>> process_line(config, "The quick brown fox jumps over the lazy dog.")
            'The quick brown [fg:red]fox[fg:reset] jumps over the lazy [fg:green]dog[fg:reset].'
        """
        config = Config(
            patterns={
                "fox": Pattern(
                    pattern="fox",
                    foreground_color=get_foreground_color("red"),
                    background_color="",
                    attributes="",
                ),
                "dog": Pattern(
                    pattern="dog",
                    foreground_color=get_foreground_color("green"),
                    background_color="",
                    attributes="",
                ),
            }
        )
        lines = ["The quick brown fox jumps over the lazy dog."]
        result = [process_line(config, line) for line in lines]

        expected = f"The quick brown {get_foreground_color('red')}fox{get_reset()} jumps over the lazy {get_foreground_color('green')}dog{get_reset()}."
        assert result == [expected]

    def test_process_lines_overlapping_fully(self):
        """handling of fully overlapping patterns.

        Example:
            >>> config = Config(patterns={
            ...     "section": Pattern(
            ...         pattern="fox jumps over",
            ...         foreground_color="[fg:green]"
            ...     ),
            ...     "jumps": Pattern(
            ...         pattern="jumps",
            ...         foreground_color="[fg:yellow]"
            ...     )
            ... })
            >>> process_line(config, "The quick brown fox jumps over the lazy dog.")
            'The quick brown [fg:green]fox [fg:yellow]jumps[fg:green] over[fg:reset] the lazy dog.'
        """
        config = Config(
            patterns={
                "section": Pattern(
                    pattern="fox jumps over",
                    foreground_color=get_foreground_color("green"),
                    background_color="",
                    attributes="",
                ),
                "jumps": Pattern(
                    pattern="jumps",
                    foreground_color=get_foreground_color("yellow"),
                    background_color="",
                    attributes="",
                ),
            }
        )
        lines = ["The quick brown fox jumps over the lazy dog."]
        result = [process_line(config, line) for line in lines]

        expected = f"The quick brown {get_foreground_color('green')}fox {get_foreground_color('yellow')}jumps{get_foreground_color('green')} over{get_reset()} the lazy dog."
        assert result == [expected]

    def test_process_lines_overlapping_fully_nested(self):
        """handling of nested overlapping patterns.

        Example:
            >>> config = Config(patterns={
            ...     "all": Pattern(
            ...         pattern="The quick brown fox jumps over the lazy dog.",
            ...         foreground_color="[fg:red]"
            ...     ),
            ...     "section": Pattern(
            ...         pattern="fox jumps over",
            ...         foreground_color="[fg:green]"
            ...     ),
            ...     "jumps": Pattern(
            ...         pattern="jumps",
            ...         foreground_color="[fg:yellow]"
            ...     )
            ... })
            >>> process_line(config, "The quick brown fox jumps over the lazy dog.")
            '[fg:red]The quick brown [fg:green]fox [fg:yellow]jumps[fg:green] over[fg:red] the lazy dog.[fg:reset]'
        """
        config = Config(
            patterns={
                "all": Pattern(
                    pattern="The quick brown fox jumps over the lazy dog.",
                    foreground_color=get_foreground_color("red"),
                    background_color="",
                    attributes="",
                ),
                "section": Pattern(
                    pattern="fox jumps over",
                    foreground_color=get_foreground_color("green"),
                    background_color="",
                    attributes="",
                ),
                "jumps": Pattern(
                    pattern="jumps",
                    foreground_color=get_foreground_color("yellow"),
                    background_color="",
                    attributes="",
                ),
            }
        )
        lines = ["The quick brown fox jumps over the lazy dog."]
        result = [process_line(config, line) for line in lines]

        expected = f"{get_foreground_color('red')}The quick brown {get_foreground_color('green')}fox {get_foreground_color('yellow')}jumps{get_foreground_color('green')} over{get_foreground_color('red')} the lazy dog.{get_reset()}"
        assert result == [expected]

    def test_process_lines_empty_input(self):
        """empty input lines are handled correctly.

        Example:
            >>> config = Config(patterns={})
            >>> [process_line(config, line) for line in []]
            []
        """
        config = Config(patterns={})
        lines: list[str] = []
        result = [process_line(config, line) for line in lines]

        assert result == []

    def test_process_lines_with_newlines(self):
        """lines with newlines are processed correctly.

        Example:
            >>> config = Config(patterns={})
            >>> process_line(config, "line1\\n")
            'line1\\n'
        """
        config = Config(patterns={})
        lines = ["line1\n", "line2\n"]
        result = [process_line(config, line) for line in lines]

        expected = ["line1\n", "line2\n"]
        assert result == expected

    def test_process_lines_style_reset(self):
        """styles are reset after each match.

        Example:
            >>> config = Config(patterns={
            ...     "fox": Pattern(
            ...         pattern="fox",
            ...         foreground_color="[fg:red]"
            ...     ),
            ...     "dog": Pattern(
            ...         pattern="dog",
            ...         foreground_color="[fg:green]"
            ...     )
            ... })
            >>> process_line(config, "The quick brown fox jumps over the lazy dog.")
            'The quick brown [fg:red]fox[fg:reset] jumps over the lazy [fg:green]dog[fg:reset].'
        """
        config = Config(
            patterns={
                "fox": Pattern(
                    pattern="fox",
                    foreground_color=get_foreground_color("red"),
                    background_color="",
                    attributes="",
                ),
                "dog": Pattern(
                    pattern="dog",
                    foreground_color=get_foreground_color("green"),
                    background_color="",
                    attributes="",
                ),
            }
        )
        lines = ["The quick brown fox jumps over the lazy dog."]
        result = [process_line(config, line) for line in lines]

        expected = f"The quick brown {get_foreground_color('red')}fox{get_reset()} jumps over the lazy {get_foreground_color('green')}dog{get_reset()}."
        assert result == [expected]

    def test_process_lines_overlapping_style_on_right(self):
        """handling of overlapping styles where one pattern is contained in another.

        Example:
            >>> config = Config(patterns={
            ...     "all": Pattern(
            ...         pattern=".+",
            ...         foreground_color="[fg:red]",
            ...         background_color="[bg:default]",
            ...         attributes="[italic]"
            ...     ),
            ...     "fox": Pattern(
            ...         pattern="fox",
            ...         foreground_color="[fg:white]",
            ...         background_color="[bg:red]",
            ...         attributes="[bold]"
            ...     )
            ... })
            >>> process_line(config, "The quick brown fox jumps over the lazy dog.")
            '[fg:red][bg:default][italic]The quick brown [fg:white][bg:red][bold]fox[fg:red][bg:default][italic] jumps over the lazy dog.[reset][bg:reset][fg:reset]'
        """
        config = Config(
            patterns={
                "all": Pattern(
                    pattern=".+",
                    foreground_color=get_foreground_color("red"),
                    background_color=get_background_color(""),
                    attributes=get_attributes("italic"),
                ),
                "fox": Pattern(
                    pattern="fox",
                    foreground_color=get_foreground_color("white"),
                    background_color=get_background_color("red"),
                    attributes=get_attributes("bold"),
                ),
            }
        )
        lines = ["The quick brown fox jumps over the lazy dog."]
        result = [process_line(config, line) for line in lines]
        expected = f"{get_foreground_color('red')}{get_background_color('')}{get_attributes('italic')}The quick brown {get_foreground_color('white')}{get_background_color('red')}{get_attributes('bold')}fox{get_foreground_color('red')}{get_background_color('')}{get_attributes('italic')} jumps over the lazy dog.{get_reset()}"
        assert result == [expected]

    def test_process_lines_overlapping_style_on_left(self):
        """handling of overlapping patterns at the start.

        Example:
            >>> config = Config(patterns={
            ...     "brown_fox": Pattern(
            ...         pattern="brown fox",
            ...         foreground_color="[fg:red]"
            ...     ),
            ...     "fox_jumps": Pattern(
            ...         pattern="fox jumps",
            ...         foreground_color="[fg:green]"
            ...     )
            ... })
            >>> process_line(config, "The quick brown fox jumps over the lazy dog.")
            'The quick [fg:red]brown [fg:green]fox jumps[fg:reset] over the lazy dog.'
        """
        config = Config(
            patterns={
                "brown_fox": Pattern(
                    pattern="brown fox",
                    foreground_color=get_foreground_color("red"),
                    background_color="",
                    attributes="",
                ),
                "fox_jumps": Pattern(
                    pattern="fox jumps",
                    foreground_color=get_foreground_color("green"),
                    background_color="",
                    attributes="",
                ),
            }
        )
        lines = ["The quick brown fox jumps over the lazy dog."]
        result = [process_line(config, line) for line in lines]
        expected = f"The quick {get_foreground_color('red')}brown {get_foreground_color('green')}fox jumps{get_reset()} over the lazy dog."
        assert result == [expected]

    def test_attributes_underline_blink(self):
        """attributes like underline and blink are applied correctly.

        Example:
            >>> config = Config(patterns={
            ...     "fox": Pattern(
            ...         pattern="fox",
            ...         attributes="[underline,blink]"
            ...     )
            ... })
            >>> process_line(config, "The quick brown fox jumps over the lazy dog.")
            'The [underline,blink]fox[reset].'
        """
        config = Config(
            patterns={
                "fox": Pattern(
                    pattern="fox",
                    foreground_color="",
                    background_color="",
                    attributes=get_attributes("underline,blink"),
                ),
            }
        )
        lines = ["The quick brown fox jumps over the lazy dog."]
        result = [process_line(config, line) for line in lines]

        expected = f"The quick brown {get_attributes('underline,blink')}fox{get_reset()} jumps over the lazy dog."
        assert result == [expected]

    def test_mixed_hex_preset_colors(self):
        """mixing hex and preset colors.

        Example:
            >>> config = Config(patterns={
            ...     "fox": Pattern(
            ...         pattern="fox",
            ...         foreground_color="[fg:#FF0000]",
            ...         background_color="[bg:blue]"
            ...     )
            ... })
            >>> process_line(config, "The quick brown fox jumps over the lazy dog.")
            'The quick brown [fg:#FF0000][bg:blue]fox[bg:reset][fg:reset] jumps over the lazy dog.'
        """
        config = Config(
            patterns={
                "fox": Pattern(
                    pattern="fox",
                    foreground_color=get_foreground_color("#FF0000"),
                    background_color=get_background_color("blue"),
                    attributes="",
                ),
            }
        )
        lines = ["The quick brown fox jumps over the lazy dog."]
        result = [process_line(config, line) for line in lines]

        expected = f"The quick brown {get_foreground_color('#FF0000')}{get_background_color('blue')}fox{get_reset()} jumps over the lazy dog."
        assert result == [expected]

    def test_overlapping_three_patterns(self):
        """handling of three overlapping patterns.

        Example:
            >>> config = Config(patterns={
            ...     "brown_fox": Pattern(
            ...         pattern="brown fox",
            ...         foreground_color="[fg:red]"
            ...     ),
            ...     "fox_jumps": Pattern(
            ...         pattern="fox jumps",
            ...         foreground_color="[fg:blue]"
            ...     ),
            ...     "jumps": Pattern(
            ...         pattern="jumps",
            ...         foreground_color="[fg:green]"
            ...     )
            ... })
            >>> process_line(config, "The quick brown fox jumps over the lazy dog.")
            'The quick [fg:red]brown [fg:blue]fox [fg:green]jumps[fg:reset] over the lazy dog.'
        """
        config = Config(
            patterns={
                "brown_fox": Pattern(
                    pattern="brown fox",
                    foreground_color=get_foreground_color("red"),
                    background_color="",
                    attributes="",
                ),
                "fox_jumps": Pattern(
                    pattern="fox jumps",
                    foreground_color=get_foreground_color("blue"),
                    background_color="",
                    attributes="",
                ),
                "jumps": Pattern(
                    pattern="jumps",
                    foreground_color=get_foreground_color("green"),
                    background_color="",
                    attributes="",
                ),
            }
        )
        lines = ["The quick brown fox jumps over the lazy dog."]
        result = [process_line(config, line) for line in lines]

        expected = f"The quick {get_foreground_color('red')}brown {get_foreground_color('blue')}fox {get_foreground_color('green')}jumps{get_reset()} over the lazy dog."
        assert result == [expected]

    def test_pattern_zero_width(self):
        """handling of zero-width patterns like word boundaries.

        Example:
            >>> config = Config(patterns={
            ...     "boundary": Pattern(
            ...         pattern=r"\\b",
            ...         foreground_color="[fg:red]"
            ...     )
            ... })
            >>> process_line(config, "The quick brown fox jumps over the lazy dog.")
            '[fg:red][fg:reset]The quick brown fox jumps over the lazy dog.'
        """
        config = Config(
            patterns={
                "boundary": Pattern(
                    pattern=r"\b",
                    foreground_color=get_foreground_color("red"),
                    background_color="",
                    attributes="",
                ),
            }
        )
        lines = ["The quick brown fox jumps over the lazy dog."]
        result = [process_line(config, line) for line in lines]

        # \b matches at position 0 (first match)
        expected = f"{get_foreground_color('red')}{get_reset()}The quick brown fox jumps over the lazy dog."
        assert result == [expected]

    def test_long_line_performance(self):
        """long lines are processed without issues.

        Example:
            >>> long_line = "The quick brown fox jumps over the lazy dog. " * 10
            >>> config = Config(patterns={
            ...     "fox": Pattern(
            ...         pattern="fox",
            ...         foreground_color="[fg:red]"
            ...     )
            ... })
            >>> result = process_line(config, long_line)
            >>> "[fg:red]" in result and "fox" in result
            True
        """
        # Test with a long line to ensure no issues
        long_line = "The quick brown fox jumps over the lazy dog. " * 10
        config = Config(
            patterns={
                "fox": Pattern(
                    pattern="fox",
                    foreground_color=get_foreground_color("red"),
                    background_color="",
                    attributes="",
                ),
            }
        )
        lines = [long_line]
        result = [process_line(config, line) for line in lines]

        assert "fox" in result[0] and get_foreground_color("red") in result[0]

    def test_overlapping_at_line_end(self):
        """overlapping patterns at the end of the line.

        Example:
            >>> config = Config(patterns={
            ...     "fox": Pattern(
            ...         pattern="fox",
            ...         foreground_color="[fg:red]"
            ...     ),
            ...     "x": Pattern(
            ...         pattern="x",
            ...         foreground_color="[fg:blue]"
            ...     )
            ... })
            >>> process_line(config, "The quick brown fox jumps over the lazy dog.")
            'The quick brown [fg:red]fo[fg:blue]x[fg:reset] jumps over the lazy dog.'
        """
        config = Config(
            patterns={
                "fox": Pattern(
                    pattern="fox",
                    foreground_color=get_foreground_color("red"),
                    background_color="",
                    attributes="",
                ),
                "x": Pattern(
                    pattern="x",
                    foreground_color=get_foreground_color("blue"),
                    background_color="",
                    attributes="",
                ),
            }
        )
        lines = ["The quick brown fox jumps over the lazy dog."]
        result = [process_line(config, line) for line in lines]

        expected = f"The quick brown {get_foreground_color('red')}fo{get_foreground_color('blue')}x{get_reset()} jumps over the lazy dog."
        assert result == [expected]

    def test_foreground_colors_preset(self):
        """application of preset foreground colors.

        Example:
            >>> config = Config(patterns={
            ...     "fox": Pattern(pattern="fox", foreground_color="[fg:red]", ...),
            ...     "dog": Pattern(pattern="dog", foreground_color="[fg:blue]", ...)
            ... })
            >>> process_line(config, "The quick brown fox jumps over the lazy dog.")
            'The quick brown [fg:red]fox[fg:reset] jumps over the lazy dog.'
        """
        config = Config(
            patterns={
                "fox": Pattern(
                    pattern="fox",
                    foreground_color=get_foreground_color("red"),
                    background_color="",
                    attributes="",
                ),
                "dog": Pattern(
                    pattern="dog",
                    foreground_color=get_foreground_color("blue"),
                    background_color="",
                    attributes="",
                ),
            }
        )
        lines = ["The quick brown fox jumps over the lazy dog."]
        result = [process_line(config, line) for line in lines]

        expected = f"The quick brown {get_foreground_color('red')}fox{get_reset()} jumps over the lazy {get_foreground_color('blue')}dog{get_reset()}."
        assert result == [expected]

    def test_foreground_colors_hex(self):
        """application of hex foreground colors.

        Example:
            >>> config = Config(patterns={
            ...     "fox": Pattern(
            ...         pattern="fox",
            ...         foreground_color="[fg:#FF0000]"
            ...     )
            ... })
            >>> process_line(config, "The quick brown fox jumps over the lazy dog.")
            'The quick brown [fg:#FF0000]fox[fg:reset] jumps over the lazy dog.'
        """
        config = Config(
            patterns={
                "fox": Pattern(
                    pattern="fox",
                    foreground_color=get_foreground_color("#FF0000"),
                    background_color="",
                    attributes="",
                ),
            }
        )
        lines = ["The quick brown fox jumps over the lazy dog."]
        result = [process_line(config, line) for line in lines]

        expected = f"The quick brown {get_foreground_color('#FF0000')}fox{get_reset()} jumps over the lazy dog."
        assert result == [expected]

    def test_background_colors_preset(self):
        """application of preset background colors.

        Example:
            >>> config = Config(patterns={
            ...     "fox": Pattern(
            ...         pattern="fox",
            ...         background_color="[bg:red]"
            ...     )
            ... })
            >>> process_line(config, "The quick brown fox jumps over the lazy dog.")
            'The quick brown [bg:red]fox[bg:reset] jumps over the lazy dog.'
        """
        config = Config(
            patterns={
                "fox": Pattern(
                    pattern="fox",
                    foreground_color="",
                    background_color=get_background_color("red"),
                    attributes="",
                ),
            }
        )
        lines = ["The quick brown fox jumps over the lazy dog."]
        result = [process_line(config, line) for line in lines]

        expected = f"The quick brown {get_background_color('red')}fox{get_reset()} jumps over the lazy dog."
        assert result == [expected]

    def test_background_colors_hex(self):
        """application of hex background colors.

        Example:
            >>> config = Config(patterns={
            ...     "fox": Pattern(
            ...         pattern="fox",
            ...         background_color="[bg:#00FF00]"
            ...     )
            ... })
            >>> process_line(config, "The quick brown fox jumps over the lazy dog.")
            'The quick brown [bg:#00FF00]fox[bg:reset] jumps over the lazy dog.'
        """
        config = Config(
            patterns={
                "fox": Pattern(
                    pattern="fox",
                    foreground_color="",
                    background_color=get_background_color("#00FF00"),
                    attributes="",
                ),
            }
        )
        lines = ["The quick brown fox jumps over the lazy dog."]
        result = [process_line(config, line) for line in lines]

        expected = f"The quick brown {get_background_color('#00FF00')}fox{get_reset()} jumps over the lazy dog."
        assert result == [expected]

    def test_attributes_single(self):
        """application of a single attribute.

        Example:
            >>> config = Config(patterns={
            ...     "fox": Pattern(
            ...         pattern="fox",
            ...         attributes="[bold]"
            ...     )
            ... })
            >>> process_line(config, "The quick brown fox jumps over the lazy dog.")
            'The quick brown [bold]fox[reset] jumps over the lazy dog.'
        """
        config = Config(
            patterns={
                "fox": Pattern(
                    pattern="fox",
                    foreground_color="",
                    background_color="",
                    attributes=get_attributes("bold"),
                ),
            }
        )
        lines = ["The quick brown fox jumps over the lazy dog."]
        result = [process_line(config, line) for line in lines]

        expected = f"The quick brown {get_attributes('bold')}fox{get_reset()} jumps over the lazy dog."
        assert result == [expected]

    def test_attributes_combined(self):
        """application of combined attributes.

        Example:
            >>> config = Config(patterns={
            ...     "fox": Pattern(
            ...         pattern="fox",
            ...         attributes="[bold,italic]"
            ...     )
            ... })
            >>> process_line(config, "The quick brown fox jumps over the lazy dog.")
            'The quick brown [bold,italic]fox[reset] jumps over the lazy dog.'
        """
        config = Config(
            patterns={
                "fox": Pattern(
                    pattern="fox",
                    foreground_color="",
                    background_color="",
                    attributes=get_attributes("bold,italic"),
                ),
            }
        )
        lines = ["The quick brown fox jumps over the lazy dog."]
        result = [process_line(config, line) for line in lines]

        expected = f"The quick brown {get_attributes('bold,italic')}fox{get_reset()} jumps over the lazy dog."
        assert result == [expected]

    def test_combined_fg_bg_attr(self):
        """combination of foreground color, background color, and attributes.

        Example:
            >>> config = Config(patterns={
            ...     "fox": Pattern(
            ...         pattern="fox",
            ...         foreground_color="[fg:red]",
            ...         background_color="[bg:blue]",
            ...         attributes="[bold]"
            ...     )
            ... })
            >>> process_line(config, "The quick brown fox jumps over the lazy dog.")
            'The quick brown [fg:red][bg:blue][bold]fox[reset][bg:reset][fg:reset] jumps over the lazy dog.'
        """
        config = Config(
            patterns={
                "fox": Pattern(
                    pattern="fox",
                    foreground_color=get_foreground_color("red"),
                    background_color=get_background_color("blue"),
                    attributes=get_attributes("bold"),
                ),
            }
        )
        lines = ["The quick brown fox jumps over the lazy dog."]
        result = [process_line(config, line) for line in lines]

        expected = f"The quick brown {get_foreground_color('red')}{get_background_color('blue')}{get_attributes('bold')}fox{get_reset()} jumps over the lazy dog."
        assert result == [expected]

    def test_overlapping_entirely_nested(self):
        """handling of entirely nested patterns.

        Example:
            >>> config = Config(patterns={
            ...     "sentence": Pattern(
            ...         pattern="The quick brown fox jumps over the lazy dog.",
            ...         foreground_color="[fg:yellow]"
            ...     ),
            ...     "fox": Pattern(
            ...         pattern="fox",
            ...         foreground_color="[fg:red]"
            ...     )
            ... })
            >>> process_line(config, "The quick brown fox jumps over the lazy dog.")
            '[fg:yellow]The quick brown [fg:red]fox[fg:yellow] jumps over the lazy dog.[fg:reset]'
        """
        config = Config(
            patterns={
                "sentence": Pattern(
                    pattern="The quick brown fox jumps over the lazy dog.",
                    foreground_color=get_foreground_color("yellow"),
                    background_color="",
                    attributes="",
                ),
                "fox": Pattern(
                    pattern="fox",
                    foreground_color=get_foreground_color("red"),
                    background_color="",
                    attributes="",
                ),
            }
        )
        lines = ["The quick brown fox jumps over the lazy dog."]
        result = [process_line(config, line) for line in lines]

        # Nested: sentence contains fox
        expected = f"{get_foreground_color('yellow')}The quick brown {get_foreground_color('red')}fox{get_foreground_color('yellow')} jumps over the lazy dog.{get_reset()}"
        assert result == [expected]

    def test_overlapping_multiple(self):
        """handling of multiple overlapping patterns.

        Example:
            >>> config = Config(patterns={
            ...     "brown_fox": Pattern(
            ...         pattern="brown fox",
            ...         foreground_color="[fg:red]"
            ...     ),
            ...     "fox_jumps": Pattern(
            ...         pattern="fox jumps",
            ...         foreground_color="[fg:blue]"
            ...     ),
            ...     "jumps_over": Pattern(
            ...         pattern="jumps over",
            ...         foreground_color="[fg:green]"
            ...     )
            ... })
            >>> process_line(config, "The brown fox jumps over the lazy dog.")
            'The [fg:red]brown [fg:blue]fox [fg:green]jumps over[fg:reset] the lazy dog.'
        """
        config = Config(
            patterns={
                "brown_fox": Pattern(
                    pattern="brown fox",
                    foreground_color=get_foreground_color("red"),
                    background_color="",
                    attributes="",
                ),
                "fox_jumps": Pattern(
                    pattern="fox jumps",
                    foreground_color=get_foreground_color("blue"),
                    background_color="",
                    attributes="",
                ),
                "jumps_over": Pattern(
                    pattern="jumps over",
                    foreground_color=get_foreground_color("green"),
                    background_color="",
                    attributes="",
                ),
            }
        )
        lines = ["The brown fox jumps over the lazy dog."]
        result = [process_line(config, line) for line in lines]

        # Complex overlaps
        expected = f"The {get_foreground_color('red')}brown {get_foreground_color('blue')}fox {get_foreground_color('green')}jumps over{get_reset()} the lazy dog."
        assert result == [expected]
