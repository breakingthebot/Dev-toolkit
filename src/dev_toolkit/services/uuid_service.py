# src/dev_toolkit/services/uuid_service.py
# Generates UUID values for CLI commands.
# Connects to: src/dev_toolkit/cli.py
# Created: 2026-06-12

"""UUID utility functions."""

from uuid import uuid4


def generate_uuid() -> str:
    """Generate a random UUID4 string.

    Parameters:
        None.

    Returns:
        UUID4 string.
    """
    return str(uuid4())

