# tests/test_json_service.py
# Verifies JSON formatting, minification, and validation behavior.
# Connects to: src/dev_toolkit/services/json_service.py
# Created: 2026-06-12

"""Tests for JSON service functions."""

import pytest

from dev_toolkit.services.json_service import format_json, minify_json, validate_json


def test_format_json_returns_sorted_pretty_output() -> None:
    """Confirm JSON formatting sorts keys and indents output."""
    assert format_json('{"b":2,"a":1}') == '{\n  "a": 1,\n  "b": 2\n}'


def test_format_json_honors_indent() -> None:
    """Confirm JSON formatting accepts a custom indentation width."""
    assert format_json('{"a":{"b":1}}', indent=4) == '{\n    "a": {\n        "b": 1\n    }\n}'


def test_minify_json_returns_compact_output() -> None:
    """Confirm JSON minification removes nonessential whitespace."""
    assert minify_json('{\n  "b": 2,\n  "a": 1\n}') == '{"a":1,"b":2}'


def test_validate_json_returns_true_for_valid_json() -> None:
    """Confirm valid JSON passes validation."""
    assert validate_json('{"a":1}')


def test_validate_json_rejects_invalid_json() -> None:
    """Confirm invalid JSON raises a clear error."""
    with pytest.raises(ValueError, match="Invalid JSON"):
        validate_json('{"a":}')
