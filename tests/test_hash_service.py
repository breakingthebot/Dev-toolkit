# tests/test_hash_service.py
# Verifies SHA hashing and checksum comparison behavior.
# Connects to: src/dev_toolkit/services/hash_service.py
# Created: 2026-06-12

"""Tests for hash service functions."""

from pathlib import Path

import pytest

from dev_toolkit.services.hash_service import (
    hash_file,
    hash_text,
    normalize_algorithm,
    verify_checksum,
)

HELLO_SHA256 = "2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824"
HELLO_SHA512 = (
    "9b71d224bd62f3785d96d46ad3ea3d73319bfbc2890caadae2dff72519673ca7"
    "2323c3d99ba5c11d7c7acc6e14b8c5da0c4663475c2e5c3adef46f73bcdec043"
)


def test_hash_text_returns_sha256_digest() -> None:
    """Confirm text can be hashed with SHA-256."""
    assert hash_text("hello", "sha256") == HELLO_SHA256


def test_hash_text_returns_sha512_digest() -> None:
    """Confirm text can be hashed with SHA-512."""
    assert hash_text("hello", "sha512") == HELLO_SHA512


def test_hash_file_returns_digest(tmp_path: Path) -> None:
    """Confirm file content can be hashed."""
    input_file = tmp_path / "plain.txt"
    input_file.write_text("hello", encoding="utf-8")

    assert hash_file(input_file, "sha256") == HELLO_SHA256


def test_verify_checksum_accepts_matching_digest_case_insensitive() -> None:
    """Confirm checksum verification ignores digest casing."""
    assert verify_checksum(HELLO_SHA256.upper(), HELLO_SHA256)


def test_verify_checksum_rejects_mismatched_digest() -> None:
    """Confirm checksum verification returns false on mismatch."""
    assert not verify_checksum(HELLO_SHA256, HELLO_SHA512)


def test_normalize_algorithm_rejects_unsupported_algorithm() -> None:
    """Confirm unsupported algorithms raise a clear error."""
    with pytest.raises(ValueError, match="sha256, sha512"):
        normalize_algorithm("md5")
