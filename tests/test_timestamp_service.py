# tests/test_timestamp_service.py
# Verifies Unix timestamp conversion behavior.
# Connects to: src/dev_toolkit/services/timestamp_service.py
# Created: 2026-06-12

"""Tests for timestamp conversion service functions."""

import pytest

from dev_toolkit.services.timestamp_service import convert_timestamp


def test_convert_timestamp_seconds_to_iso_utc() -> None:
    """Confirm second-based timestamps convert to UTC ISO text."""
    assert convert_timestamp("0") == "1970-01-01T00:00:00+00:00"


def test_convert_timestamp_milliseconds_to_iso_utc() -> None:
    """Confirm millisecond-based timestamps are detected and converted."""
    assert convert_timestamp("1000000000000") == "2001-09-09T01:46:40+00:00"


def test_convert_timestamp_rejects_non_numeric_input() -> None:
    """Confirm invalid timestamp input raises a clear error."""
    with pytest.raises(ValueError, match="numeric"):
        convert_timestamp("yesterday")

