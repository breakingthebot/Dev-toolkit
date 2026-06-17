# src/dev_toolkit/services/url_service.py
# Encodes and decodes URL text for CLI commands.
# Connects to: src/dev_toolkit/cli.py
# Created: 2026-06-17

"""URL encoding utility functions."""

from urllib.parse import quote, quote_plus, unquote, unquote_plus


def encode_url_text(text: str, component: bool = False) -> str:
    """Encode text for safe use in URLs.

    Parameters:
        text: Plain text to encode.
        component: Whether to percent-encode spaces as `%20` instead of `+`.

    Returns:
        URL-encoded text.
    """
    if component:
        return quote(text, safe="")

    return quote_plus(text)


def decode_url_text(text: str, component: bool = False) -> str:
    """Decode URL-encoded text.

    Parameters:
        text: URL-encoded text.
        component: Whether to decode percent-encoded components without `+` to space conversion.

    Returns:
        Decoded text.
    """
    if component:
        return unquote(text)

    return unquote_plus(text)
