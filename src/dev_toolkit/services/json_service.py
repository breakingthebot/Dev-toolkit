# src/dev_toolkit/services/json_service.py
# Formats and validates JSON text for CLI commands.
# Connects to: src/dev_toolkit/cli.py
# Created: 2026-06-12

"""JSON utility functions."""

import json
from typing import Any

DEFAULT_INDENT = 2


def format_json(text: str, indent: int = DEFAULT_INDENT) -> str:
    """Format JSON text with stable indentation and sorted keys.

    Parameters:
        text: JSON text to format.
        indent: Number of spaces to use for indentation.

    Returns:
        Pretty-printed JSON text.

    Raises:
        ValueError: If the input is invalid JSON.
    """
    parsed_json = parse_json(text)
    return json.dumps(parsed_json, indent=indent, sort_keys=True)


def minify_json(text: str) -> str:
    """Minify JSON text by removing nonessential whitespace.

    Parameters:
        text: JSON text to minify.

    Returns:
        Compact JSON text.

    Raises:
        ValueError: If the input is invalid JSON.
    """
    parsed_json = parse_json(text)
    return json.dumps(parsed_json, separators=(",", ":"), sort_keys=True)


def validate_json(text: str) -> bool:
    """Validate JSON text.

    Parameters:
        text: JSON text to validate.

    Returns:
        True when the text is valid JSON.

    Raises:
        ValueError: If the input is invalid JSON.
    """
    parse_json(text)
    return True


def parse_json(text: str) -> Any:
    """Parse JSON text into Python data.

    Parameters:
        text: JSON text to parse.

    Returns:
        Parsed JSON data.

    Raises:
        ValueError: If the input is invalid JSON.
    """
    try:
        return json.loads(text)
    except json.JSONDecodeError as error:
        message = f"Invalid JSON at line {error.lineno}, column {error.colno}: {error.msg}."
        raise ValueError(message) from error
