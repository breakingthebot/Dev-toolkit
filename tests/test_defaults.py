# tests/test_defaults.py
# Verifies environment-driven CLI default configuration.
# Connects to: src/dev_toolkit/config/defaults.py
# Created: 2026-06-17

"""Tests for environment default helpers."""

import pytest

from dev_toolkit.config.defaults import (
    DEFAULT_JSON_INDENT,
    DEFAULT_PASSWORD_LENGTH,
    get_json_indent_default,
    get_password_length_default,
)


def test_get_password_length_default_returns_fallback(monkeypatch: pytest.MonkeyPatch) -> None:
    """Confirm password length falls back when the environment is unset."""
    monkeypatch.delenv("DEV_TOOLKIT_PASSWORD_LENGTH", raising=False)
    assert get_password_length_default() == DEFAULT_PASSWORD_LENGTH


def test_get_password_length_default_reads_environment(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Confirm password length can be configured by environment variable."""
    monkeypatch.setenv("DEV_TOOLKIT_PASSWORD_LENGTH", "32")
    assert get_password_length_default() == 32


def test_get_json_indent_default_returns_fallback(monkeypatch: pytest.MonkeyPatch) -> None:
    """Confirm JSON indent falls back when the environment is unset."""
    monkeypatch.delenv("DEV_TOOLKIT_JSON_INDENT", raising=False)
    assert get_json_indent_default() == DEFAULT_JSON_INDENT


def test_get_json_indent_default_reads_environment(monkeypatch: pytest.MonkeyPatch) -> None:
    """Confirm JSON indent can be configured by environment variable."""
    monkeypatch.setenv("DEV_TOOLKIT_JSON_INDENT", "4")
    assert get_json_indent_default() == 4


def test_get_json_indent_default_rejects_invalid_environment(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Confirm invalid JSON indent values raise a clear error."""
    monkeypatch.setenv("DEV_TOOLKIT_JSON_INDENT", "wide")
    with pytest.raises(ValueError, match="DEV_TOOLKIT_JSON_INDENT"):
        get_json_indent_default()
