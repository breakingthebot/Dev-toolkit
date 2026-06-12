# tests/test_password_service.py
# Verifies secure password generation constraints.
# Connects to: src/dev_toolkit/services/password_service.py
# Created: 2026-06-12

"""Tests for password service functions."""

import string

import pytest

from dev_toolkit.services.password_service import generate_password


def test_generate_password_returns_requested_length() -> None:
    """Confirm generated passwords match the requested length."""
    password = generate_password(length=24)
    assert len(password) == 24


def test_generate_password_without_symbols_uses_safe_alphabet() -> None:
    """Confirm symbol-free passwords contain only letters and digits."""
    password = generate_password(length=32, include_symbols=False)
    allowed_characters = set(string.ascii_letters + string.digits)
    assert set(password).issubset(allowed_characters)


def test_generate_password_rejects_short_length() -> None:
    """Confirm unsupported password lengths are rejected."""
    with pytest.raises(ValueError, match="at least 8"):
        generate_password(length=7)

