# tests/test_clipboard_service.py
# Verifies clipboard service wrappers for CLI clipboard integration.
# Connects to: src/dev_toolkit/services/clipboard_service.py
# Created: 2026-06-17

"""Tests for clipboard service functions."""

from dev_toolkit.services.clipboard_service import (
    read_clipboard_text,
    write_clipboard_text,
)


def test_read_clipboard_text_returns_pasted_text(monkeypatch) -> None:
    """Confirm clipboard reads return pasted text."""
    monkeypatch.setattr(
        "dev_toolkit.services.clipboard_service.pyperclip.paste",
        lambda: "hello",
    )
    assert read_clipboard_text() == "hello"


def test_write_clipboard_text_copies_text(monkeypatch) -> None:
    """Confirm clipboard writes copy text."""
    copied_text: list[str] = []
    monkeypatch.setattr(
        "dev_toolkit.services.clipboard_service.pyperclip.copy",
        copied_text.append,
    )
    write_clipboard_text("hello")
    assert copied_text == ["hello"]
