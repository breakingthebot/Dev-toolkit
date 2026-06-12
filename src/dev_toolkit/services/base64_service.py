# src/dev_toolkit/services/base64_service.py
# Handles base64 encoding and decoding for CLI commands.
# Connects to: src/dev_toolkit/cli.py
# Created: 2026-06-12

"""Base64 utility functions."""

import base64
import binascii

TEXT_ENCODING = "utf-8"


def encode_base64(text: str) -> str:
    """Encode text into a base64 string.

    Parameters:
        text: Plain text to encode.

    Returns:
        Base64 encoded text.
    """
    encoded_bytes = base64.b64encode(text.encode(TEXT_ENCODING))
    return encoded_bytes.decode(TEXT_ENCODING)


def decode_base64(text: str) -> str:
    """Decode a base64 string into plain text.

    Parameters:
        text: Base64 text to decode.

    Returns:
        Decoded plain text.

    Raises:
        ValueError: If the input is not valid base64 or UTF-8 text.
    """
    try:
        decoded_bytes = base64.b64decode(text.encode(TEXT_ENCODING), validate=True)
        return decoded_bytes.decode(TEXT_ENCODING)
    except (binascii.Error, UnicodeDecodeError) as error:
        raise ValueError("Input must be valid base64-encoded UTF-8 text.") from error

