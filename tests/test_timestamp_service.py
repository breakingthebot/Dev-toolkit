# tests/test_timestamp_service.py
# Verifies Unix timestamp conversion behavior.
# Connects to: src/dev_toolkit/services/timestamp_service.py
# Created: 2026-06-12

"""Tests for timestamp conversion service functions."""

import pytest

from dev_toolkit.services.timestamp_service import (
    convert_datetime_to_timestamp,
    convert_timestamp,
)


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


def test_convert_datetime_to_timestamp_returns_seconds() -> None:
    """Confirm ISO 8601 UTC datetimes convert to Unix seconds."""
    assert convert_datetime_to_timestamp("1970-01-01T00:00:00+00:00") == "0"


def test_convert_datetime_to_timestamp_accepts_z_suffix() -> None:
    """Confirm ISO 8601 Z suffix datetimes convert to Unix seconds."""
    assert convert_datetime_to_timestamp("2001-09-09T01:46:40Z") == "1000000000"


def test_convert_datetime_to_timestamp_handles_offsets() -> None:
    """Confirm offset-aware datetimes convert to UTC Unix seconds."""
    assert convert_datetime_to_timestamp("1970-01-01T01:00:00+01:00") == "0"


def test_convert_datetime_to_timestamp_returns_milliseconds() -> None:
    """Confirm ISO 8601 datetimes can convert to Unix milliseconds."""
    assert (
        convert_datetime_to_timestamp("2001-09-09T01:46:40+00:00", milliseconds=True)
        == "1000000000000"
    )


def test_convert_datetime_to_timestamp_treats_naive_datetime_as_utc() -> None:
    """Confirm timezone-free datetimes are interpreted as UTC."""
    assert convert_datetime_to_timestamp("1970-01-01T00:00:00") == "0"


def test_convert_datetime_to_timestamp_rejects_invalid_datetime() -> None:
    """Confirm invalid ISO 8601 datetime text raises a clear error."""
    with pytest.raises(ValueError, match="ISO 8601"):
        convert_datetime_to_timestamp("yesterday")
