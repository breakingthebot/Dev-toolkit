# tests/test_base64_service.py
# Verifies base64 encoding and decoding behavior.
# Connects to: src/dev_toolkit/services/base64_service.py
# Created: 2026-06-12

"""Tests for base64 service functions."""

import pytest

from dev_toolkit.services.base64_service import decode_base64, encode_base64


def test_encode_base64_returns_expected_text() -> None:
    """Confirm plain text encodes to the expected base64 value."""
    assert encode_base64("hello") == "aGVsbG8="


def test_decode_base64_returns_expected_text() -> None:
    """Confirm base64 text decodes to the expected plain value."""
    assert decode_base64("aGVsbG8=") == "hello"


def test_decode_base64_rejects_invalid_text() -> None:
    """Confirm invalid base64 text raises a clear error."""
    with pytest.raises(ValueError, match="valid base64"):
        decode_base64("not valid")

