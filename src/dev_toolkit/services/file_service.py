# src/dev_toolkit/services/file_service.py
# Reads simple file metadata and text statistics for CLI commands.
# Connects to: src/dev_toolkit/cli.py
# Created: 2026-06-17

"""File utility functions."""

from pathlib import Path

TEXT_ENCODING = "utf-8"
SIZE_UNITS = ("B", "KB", "MB", "GB", "TB")
UNIT_STEP = 1024


def get_file_size(path: Path) -> int:
    """Return a file size in bytes.

    Parameters:
        path: File path to inspect.

    Returns:
        File size in bytes.
    """
    return path.stat().st_size


def format_file_size(size_bytes: int) -> str:
    """Format a byte count as a human-readable size.

    Parameters:
        size_bytes: Size in bytes.

    Returns:
        Human-readable size string.
    """
    size_value = float(size_bytes)
    for unit in SIZE_UNITS:
        if size_value < UNIT_STEP or unit == SIZE_UNITS[-1]:
            if unit == "B":
                return f"{int(size_value)} {unit}"

            return f"{size_value:.2f} {unit}"

        size_value /= UNIT_STEP

    return f"{size_value:.2f} {SIZE_UNITS[-1]}"


def count_lines(path: Path) -> int:
    """Count text lines in a file.

    Parameters:
        path: Text file path to inspect.

    Returns:
        Number of lines in the file.
    """
    with path.open("r", encoding=TEXT_ENCODING) as input_file:
        return sum(1 for _line in input_file)


def count_words(path: Path) -> int:
    """Count whitespace-delimited words in a text file.

    Parameters:
        path: Text file path to inspect.

    Returns:
        Number of words in the file.
    """
    return len(path.read_text(encoding=TEXT_ENCODING).split())


def count_characters(path: Path) -> int:
    """Count text characters in a file.

    Parameters:
        path: Text file path to inspect.

    Returns:
        Number of characters in the file.
    """
    return len(path.read_text(encoding=TEXT_ENCODING))
