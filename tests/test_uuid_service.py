# tests/test_uuid_service.py
# Verifies UUID generation behavior.
# Connects to: src/dev_toolkit/services/uuid_service.py
# Created: 2026-06-12

"""Tests for UUID service functions."""

from uuid import UUID

from dev_toolkit.services.uuid_service import generate_uuid


def test_generate_uuid_returns_uuid4_text() -> None:
    """Confirm generated UUID text parses as a version 4 UUID."""
    generated_uuid = UUID(generate_uuid())
    assert generated_uuid.version == 4

