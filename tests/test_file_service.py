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

FIXTURE_DIR = Path(__file__).parent / "fixtures"
HELLO_FILE = FIXTURE_DIR / "hello.txt"
TWO_LINES_FILE = FIXTURE_DIR / "two_lines.txt"
WORDS_FILE = FIXTURE_DIR / "words.txt"


def test_get_file_size_returns_bytes() -> None:
    """Confirm file size returns raw byte count."""
    assert get_file_size(HELLO_FILE) == 6


def test_format_file_size_returns_bytes() -> None:
    """Confirm small sizes are formatted as bytes."""
    assert format_file_size(5) == "5 B"


def test_format_file_size_returns_kilobytes() -> None:
    """Confirm larger sizes are formatted as kilobytes."""
    assert format_file_size(1536) == "1.50 KB"


def test_count_lines_returns_line_count() -> None:
    """Confirm line count reads UTF-8 text files."""
    assert count_lines(TWO_LINES_FILE) == 2


def test_count_words_returns_word_count() -> None:
    """Confirm word count splits on whitespace."""
    assert count_words(WORDS_FILE) == 3


def test_count_characters_returns_character_count() -> None:
    """Confirm character count reads UTF-8 text."""
    assert count_characters(HELLO_FILE) == 6
