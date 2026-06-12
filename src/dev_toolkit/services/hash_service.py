# src/dev_toolkit/services/hash_service.py
# Calculates and verifies SHA hashes for text and file content.
# Connects to: src/dev_toolkit/cli.py
# Created: 2026-06-12

"""Hashing utility functions."""

import hashlib
from pathlib import Path

TEXT_ENCODING = "utf-8"
SUPPORTED_ALGORITHMS = ("sha256", "sha512")


def hash_text(text: str, algorithm: str) -> str:
    """Hash plain text with a supported algorithm.

    Parameters:
        text: Plain text to hash.
        algorithm: Hash algorithm name.

    Returns:
        Hexadecimal digest string.

    Raises:
        ValueError: If the algorithm is unsupported.
    """
    return hash_bytes(text.encode(TEXT_ENCODING), algorithm)


def hash_file(path: Path, algorithm: str) -> str:
    """Hash file content with a supported algorithm.

    Parameters:
        path: File path to read and hash.
        algorithm: Hash algorithm name.

    Returns:
        Hexadecimal digest string.

    Raises:
        ValueError: If the algorithm is unsupported.
    """
    return hash_bytes(path.read_bytes(), algorithm)


def hash_bytes(content: bytes, algorithm: str) -> str:
    """Hash bytes with a supported algorithm.

    Parameters:
        content: Bytes to hash.
        algorithm: Hash algorithm name.

    Returns:
        Hexadecimal digest string.

    Raises:
        ValueError: If the algorithm is unsupported.
    """
    normalized_algorithm = normalize_algorithm(algorithm)
    digest = hashlib.new(normalized_algorithm)
    digest.update(content)
    return digest.hexdigest()


def verify_checksum(actual_digest: str, expected_digest: str) -> bool:
    """Compare two checksum strings securely.

    Parameters:
        actual_digest: Calculated hexadecimal digest.
        expected_digest: Expected hexadecimal digest.

    Returns:
        True when digests match, otherwise False.
    """
    return actual_digest.lower() == expected_digest.lower()


def normalize_algorithm(algorithm: str) -> str:
    """Normalize and validate a hash algorithm name.

    Parameters:
        algorithm: Hash algorithm name.

    Returns:
        Normalized algorithm name.

    Raises:
        ValueError: If the algorithm is unsupported.
    """
    normalized_algorithm = algorithm.lower()
    if normalized_algorithm not in SUPPORTED_ALGORITHMS:
        supported = ", ".join(SUPPORTED_ALGORITHMS)
        raise ValueError(f"Hash algorithm must be one of: {supported}.")

    return normalized_algorithm
