# src/dev_toolkit/services/clipboard_service.py
# Wraps clipboard read/write behavior for text-oriented CLI commands.
# Connects to: src/dev_toolkit/cli.py
# Created: 2026-06-17

"""Clipboard utility functions."""

import pyperclip


def read_clipboard_text() -> str:
    """Read text from the system clipboard.

    Parameters:
        None.

    Returns:
        Clipboard text.

    Raises:
        RuntimeError: If clipboard access is unavailable.
    """
    try:
        return pyperclip.paste()
    except pyperclip.PyperclipException as error:
        raise RuntimeError("Clipboard input is unavailable on this system.") from error


def write_clipboard_text(text: str) -> None:
    """Write text to the system clipboard.

    Parameters:
        text: Text to copy.

    Returns:
        None.

    Raises:
        RuntimeError: If clipboard access is unavailable.
    """
    try:
        pyperclip.copy(text)
    except pyperclip.PyperclipException as error:
        raise RuntimeError("Clipboard output is unavailable on this system.") from error
