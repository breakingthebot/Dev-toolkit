# src/dev_toolkit/services/timestamp_service.py
# Converts Unix timestamps into ISO 8601 UTC datetime strings.
# Connects to: src/dev_toolkit/cli.py
# Created: 2026-06-12

"""Timestamp conversion utilities."""

from datetime import UTC, datetime

MILLISECONDS_THRESHOLD = 10_000_000_000


def convert_timestamp(value: str) -> str:
    """Convert a Unix timestamp to an ISO 8601 UTC datetime.

    Parameters:
        value: Unix timestamp in seconds or milliseconds.

    Returns:
        ISO 8601 UTC datetime string.

    Raises:
        ValueError: If the timestamp cannot be parsed.
    """
    try:
        numeric_value = float(value)
    except ValueError as error:
        raise ValueError("Timestamp must be a numeric Unix timestamp.") from error

    if abs(numeric_value) >= MILLISECONDS_THRESHOLD:
        numeric_value /= 1000

    try:
        converted = datetime.fromtimestamp(numeric_value, tz=UTC)
    except (OverflowError, OSError) as error:
        raise ValueError("Timestamp is outside the supported datetime range.") from error

    return converted.isoformat()

