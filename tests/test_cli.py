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
    assert "0.2.0" in result.output


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


def test_cli_base64_encode_reads_input_file() -> None:
    """Confirm base64 encode can read file content."""
    runner = CliRunner()
    with runner.isolated_filesystem():
        with open("plain.txt", "wb") as input_file:
            input_file.write(b"hello")

        result = runner.invoke(cli, ["base64", "encode", "--input-file", "plain.txt"])

    assert result.exit_code == 0
    assert result.output.strip() == "aGVsbG8="


def test_cli_base64_encode_writes_output_file() -> None:
    """Confirm base64 encode can write encoded text to a file."""
    runner = CliRunner()
    with runner.isolated_filesystem():
        result = runner.invoke(
            cli,
            ["base64", "encode", "hello", "--output-file", "encoded.txt"],
        )
        with open("encoded.txt", encoding="utf-8") as output_file:
            encoded_text = output_file.read()

    assert result.exit_code == 0
    assert encoded_text == "aGVsbG8="


def test_cli_base64_decode_reads_and_writes_files() -> None:
    """Confirm base64 decode can read encoded text and write decoded bytes."""
    runner = CliRunner()
    with runner.isolated_filesystem():
        with open("encoded.txt", "w", encoding="utf-8") as input_file:
            input_file.write("aGVsbG8=")

        result = runner.invoke(
            cli,
            [
                "base64",
                "decode",
                "--input-file",
                "encoded.txt",
                "--output-file",
                "plain.txt",
            ],
        )
        with open("plain.txt", "rb") as output_file:
            decoded_content = output_file.read()

    assert result.exit_code == 0
    assert decoded_content == b"hello"


def test_cli_base64_encode_rejects_missing_input() -> None:
    """Confirm encode reports a usage error when no input is provided."""
    result = CliRunner().invoke(cli, ["base64", "encode"])
    assert result.exit_code != 0
    assert "Provide TEXT or --input-file" in result.output
