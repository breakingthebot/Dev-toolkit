# src/dev_toolkit/services/timestamp_service.py
# Converts Unix timestamps and ISO 8601 datetimes.
# Connects to: src/dev_toolkit/cli.py
# Created: 2026-06-12

"""Timestamp conversion utilities."""

from datetime import UTC, datetime

MILLISECONDS_THRESHOLD = 10_000_000_000
MILLISECONDS_MULTIPLIER = 1000


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


def convert_datetime_to_timestamp(value: str, milliseconds: bool = False) -> str:
    """Convert an ISO 8601 datetime to a Unix timestamp.

    Parameters:
        value: ISO 8601 datetime text.
        milliseconds: Whether to return milliseconds instead of seconds.

    Returns:
        Unix timestamp string.

    Raises:
        ValueError: If the datetime cannot be parsed.
    """
    normalized_value = value.strip().replace("Z", "+00:00")

    try:
        parsed_datetime = datetime.fromisoformat(normalized_value)
    except ValueError as error:
        raise ValueError("Datetime must be valid ISO 8601 text.") from error

    if parsed_datetime.tzinfo is None:
        parsed_datetime = parsed_datetime.replace(tzinfo=UTC)

    timestamp = parsed_datetime.timestamp()
    if milliseconds:
        return str(round(timestamp * MILLISECONDS_MULTIPLIER))

    return str(round(timestamp))
