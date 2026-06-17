# tests/test_url_service.py
# Verifies URL encoding and decoding helpers.
# Connects to: src/dev_toolkit/services/url_service.py
# Created: 2026-06-17

"""Tests for URL service functions."""

from dev_toolkit.services.url_service import decode_url_text, encode_url_text


def test_encode_url_text_uses_query_style_spaces() -> None:
    """Confirm default URL encoding converts spaces to plus signs."""
    assert encode_url_text("hello world") == "hello+world"


def test_encode_url_text_component_uses_percent_spaces() -> None:
    """Confirm component URL encoding converts spaces to percent encoding."""
    assert encode_url_text("hello world", component=True) == "hello%20world"


def test_decode_url_text_uses_query_style_spaces() -> None:
    """Confirm default URL decoding converts plus signs to spaces."""
    assert decode_url_text("hello+world") == "hello world"


def test_decode_url_text_component_preserves_plus_signs() -> None:
    """Confirm component URL decoding leaves plus signs intact."""
    assert decode_url_text("hello+world", component=True) == "hello+world"
