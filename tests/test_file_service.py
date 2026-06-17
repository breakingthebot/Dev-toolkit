# tests/test_file_service.py
# Verifies file metadata and text counting helpers.
# Connects to: src/dev_toolkit/services/file_service.py
# Created: 2026-06-17

"""Tests for file service functions."""

from pathlib import Path

from dev_toolkit.services.file_service import (
    count_characters,
    count_lines,
    count_words,
    format_file_size,
    get_file_size,
)


def test_get_file_size_returns_bytes(tmp_path: Path) -> None:
    """Confirm file size returns raw byte count."""
    input_file = tmp_path / "plain.txt"
    input_file.write_text("hello", encoding="utf-8")

    assert get_file_size(input_file) == 5


def test_format_file_size_returns_bytes() -> None:
    """Confirm small sizes are formatted as bytes."""
    assert format_file_size(5) == "5 B"


def test_format_file_size_returns_kilobytes() -> None:
    """Confirm larger sizes are formatted as kilobytes."""
    assert format_file_size(1536) == "1.50 KB"


def test_count_lines_returns_line_count(tmp_path: Path) -> None:
    """Confirm line count reads UTF-8 text files."""
    input_file = tmp_path / "plain.txt"
    input_file.write_text("first\nsecond\n", encoding="utf-8")

    assert count_lines(input_file) == 2


def test_count_words_returns_word_count(tmp_path: Path) -> None:
    """Confirm word count splits on whitespace."""
    input_file = tmp_path / "plain.txt"
    input_file.write_text("hello world\nagain", encoding="utf-8")

    assert count_words(input_file) == 3


def test_count_characters_returns_character_count(tmp_path: Path) -> None:
    """Confirm character count reads UTF-8 text."""
    input_file = tmp_path / "plain.txt"
    input_file.write_text("hello", encoding="utf-8")

    assert count_characters(input_file) == 5
