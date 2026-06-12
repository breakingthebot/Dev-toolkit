# tests/test_cli.py
# Verifies Click command wiring and user-facing command behavior.
# Connects to: src/dev_toolkit/cli.py
# Created: 2026-06-12

"""Tests for the Dev Toolkit Click interface."""

from click.testing import CliRunner

from dev_toolkit.cli import cli


def test_cli_version_outputs_package_version() -> None:
    """Confirm the CLI exposes a stable version flag."""
    result = CliRunner().invoke(cli, ["--version"])
    assert result.exit_code == 0
    assert "0.1.0" in result.output


def test_cli_base64_encode_command_outputs_encoded_text() -> None:
    """Confirm the base64 encode command prints encoded text."""
    result = CliRunner().invoke(cli, ["base64", "encode", "hello"])
    assert result.exit_code == 0
    assert result.output.strip() == "aGVsbG8="


def test_cli_invalid_base64_decode_returns_error() -> None:
    """Confirm invalid base64 input returns a user-facing CLI error."""
    result = CliRunner().invoke(cli, ["base64", "decode", "not valid"])
    assert result.exit_code != 0
    assert "valid base64" in result.output

