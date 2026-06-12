# src/dev_toolkit/services/password_service.py
# Generates cryptographically secure passwords for the CLI.
# Connects to: src/dev_toolkit/cli.py
# Created: 2026-06-12

"""Password generation utilities."""

import secrets
import string

DEFAULT_MIN_LENGTH = 8


def generate_password(length: int, include_symbols: bool = True) -> str:
    """Generate a secure random password.

    Parameters:
        length: Number of characters to generate.
        include_symbols: Whether punctuation symbols are allowed.

    Returns:
        Generated password text.

    Raises:
        ValueError: If length is below the supported minimum.
    """
    if length < DEFAULT_MIN_LENGTH:
        raise ValueError(f"Password length must be at least {DEFAULT_MIN_LENGTH}.")

    alphabet = string.ascii_letters + string.digits
    if include_symbols:
        alphabet += string.punctuation

    return "".join(secrets.choice(alphabet) for _ in range(length))

