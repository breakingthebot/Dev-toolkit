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
    assert "0.9.2" in result.output


def test_cli_help_includes_examples() -> None:
    """Confirm top-level help includes usage examples."""
    result = CliRunner().invoke(cli, ["--help"])
    assert result.exit_code == 0
    assert "Examples:" in result.output
    assert "dev-toolkit json validate --input-file data.json" in result.output


def test_cli_group_help_includes_examples() -> None:
    """Confirm command group help includes practical examples."""
    result = CliRunner().invoke(cli, ["hash", "--help"])
    assert result.exit_code == 0
    assert "Examples:" in result.output
    assert "dev-toolkit hash file sha512 archive.zip" in result.output


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


def test_cli_file_size_outputs_bytes() -> None:
    """Confirm file size command prints byte count."""
    runner = CliRunner()
    with runner.isolated_filesystem():
        with open("plain.txt", "w", encoding="utf-8") as input_file:
            input_file.write("hello")

        result = runner.invoke(cli, ["file", "size", "plain.txt"])

    assert result.exit_code == 0
    assert result.output.strip() == "5"


def test_cli_file_size_outputs_human_readable_size() -> None:
    """Confirm file size command can print human-readable size."""
    runner = CliRunner()
    with runner.isolated_filesystem():
        with open("plain.txt", "w", encoding="utf-8") as input_file:
            input_file.write("hello")

        result = runner.invoke(cli, ["file", "size", "--human", "plain.txt"])

    assert result.exit_code == 0
    assert result.output.strip() == "5 B"


def test_cli_file_lines_outputs_line_count() -> None:
    """Confirm file lines command prints line count."""
    runner = CliRunner()
    with runner.isolated_filesystem():
        with open("plain.txt", "w", encoding="utf-8") as input_file:
            input_file.write("first\nsecond\n")

        result = runner.invoke(cli, ["file", "lines", "plain.txt"])

    assert result.exit_code == 0
    assert result.output.strip() == "2"


def test_cli_file_stats_outputs_text_counts() -> None:
    """Confirm file stats command prints file text statistics."""
    runner = CliRunner()
    with runner.isolated_filesystem():
        with open("plain.txt", "w", encoding="utf-8") as input_file:
            input_file.write("hello world\nagain")

        result = runner.invoke(cli, ["file", "stats", "plain.txt"])

    assert result.exit_code == 0
    assert "bytes: 18" in result.output
    assert "lines: 2" in result.output
    assert "words: 3" in result.output
    assert "characters: 17" in result.output


def test_cli_hash_text_outputs_sha256_digest() -> None:
    """Confirm hash text command prints a SHA-256 digest."""
    result = CliRunner().invoke(cli, ["hash", "text", "sha256", "hello"])
    assert result.exit_code == 0
    assert (
        result.output.strip()
        == "2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824"
    )


def test_cli_hash_file_outputs_sha512_digest() -> None:
    """Confirm hash file command prints a SHA-512 digest."""
    runner = CliRunner()
    with runner.isolated_filesystem():
        with open("plain.txt", "w", encoding="utf-8") as input_file:
            input_file.write("hello")

        result = runner.invoke(cli, ["hash", "file", "sha512", "plain.txt"])

    assert result.exit_code == 0
    assert result.output.strip().startswith("9b71d224bd62f378")


def test_cli_hash_verify_outputs_ok_for_matching_digest() -> None:
    """Confirm hash verify command succeeds when the checksum matches."""
    runner = CliRunner()
    digest = "2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824"
    with runner.isolated_filesystem():
        with open("plain.txt", "w", encoding="utf-8") as input_file:
            input_file.write("hello")

        result = runner.invoke(cli, ["hash", "verify", "sha256", digest, "plain.txt"])

    assert result.exit_code == 0
    assert result.output.strip() == "OK"


def test_cli_hash_verify_fails_for_mismatched_digest() -> None:
    """Confirm hash verify command fails when the checksum mismatches."""
    runner = CliRunner()
    with runner.isolated_filesystem():
        with open("plain.txt", "w", encoding="utf-8") as input_file:
            input_file.write("hello")

        result = runner.invoke(cli, ["hash", "verify", "sha256", "abc123", "plain.txt"])

    assert result.exit_code != 0
    assert "Checksum mismatch" in result.output


def test_cli_json_format_outputs_pretty_json() -> None:
    """Confirm JSON format command prints formatted JSON."""
    result = CliRunner().invoke(cli, ["json", "format", '{"b":2,"a":1}'])
    assert result.exit_code == 0
    assert result.output.strip() == '{\n  "a": 1,\n  "b": 2\n}'


def test_cli_json_format_uses_environment_indent() -> None:
    """Confirm JSON format uses the configured default indentation."""
    result = CliRunner().invoke(
        cli,
        ["json", "format", '{"a":{"b":1}}'],
        env={"DEV_TOOLKIT_JSON_INDENT": "4"},
    )
    assert result.exit_code == 0
    assert result.output.strip() == '{\n    "a": {\n        "b": 1\n    }\n}'


def test_cli_json_format_flag_overrides_environment_indent() -> None:
    """Confirm explicit JSON indent overrides environment defaults."""
    result = CliRunner().invoke(
        cli,
        ["json", "format", "--indent", "2", '{"a":{"b":1}}'],
        env={"DEV_TOOLKIT_JSON_INDENT": "4"},
    )
    assert result.exit_code == 0
    assert result.output.strip() == '{\n  "a": {\n    "b": 1\n  }\n}'


def test_cli_password_uses_environment_length() -> None:
    """Confirm password command uses the configured default length."""
    result = CliRunner().invoke(
        cli,
        ["password", "--no-symbols"],
        env={"DEV_TOOLKIT_PASSWORD_LENGTH": "32"},
    )
    assert result.exit_code == 0
    assert len(result.output.strip()) == 32


def test_cli_password_flag_overrides_environment_length() -> None:
    """Confirm explicit password length overrides environment defaults."""
    result = CliRunner().invoke(
        cli,
        ["password", "--length", "12", "--no-symbols"],
        env={"DEV_TOOLKIT_PASSWORD_LENGTH": "32"},
    )
    assert result.exit_code == 0
    assert len(result.output.strip()) == 12


def test_cli_json_minify_outputs_compact_json() -> None:
    """Confirm JSON minify command prints compact JSON."""
    result = CliRunner().invoke(cli, ["json", "minify", '{ "b": 2, "a": 1 }'])
    assert result.exit_code == 0
    assert result.output.strip() == '{"a":1,"b":2}'


def test_cli_json_validate_outputs_ok() -> None:
    """Confirm JSON validate command prints OK for valid JSON."""
    result = CliRunner().invoke(cli, ["json", "validate", '{"a":1}'])
    assert result.exit_code == 0
    assert result.output.strip() == "OK"


def test_cli_json_validate_reports_invalid_json() -> None:
    """Confirm JSON validate command reports parse errors."""
    result = CliRunner().invoke(cli, ["json", "validate", '{"a":}'])
    assert result.exit_code != 0
    assert "Invalid JSON" in result.output


def test_cli_json_format_reads_and_writes_files() -> None:
    """Confirm JSON format can read and write files."""
    runner = CliRunner()
    with runner.isolated_filesystem():
        with open("input.json", "w", encoding="utf-8") as input_file:
            input_file.write('{"b":2,"a":1}')

        result = runner.invoke(
            cli,
            [
                "json",
                "format",
                "--input-file",
                "input.json",
                "--output-file",
                "output.json",
            ],
        )
        with open("output.json", encoding="utf-8") as output_file:
            formatted_json = output_file.read()

    assert result.exit_code == 0
    assert formatted_json == '{\n  "a": 1,\n  "b": 2\n}'


def test_cli_json_format_rejects_missing_input() -> None:
    """Confirm JSON format reports a usage error when no input is provided."""
    result = CliRunner().invoke(cli, ["json", "format"])
    assert result.exit_code != 0
    assert "Provide TEXT or --input-file" in result.output


def test_cli_timestamp_converts_unix_to_iso() -> None:
    """Confirm timestamp command keeps Unix-to-ISO behavior."""
    result = CliRunner().invoke(cli, ["timestamp", "0"])
    assert result.exit_code == 0
    assert result.output.strip() == "1970-01-01T00:00:00+00:00"


def test_cli_timestamp_converts_iso_to_unix() -> None:
    """Confirm timestamp command converts ISO datetimes to Unix seconds."""
    result = CliRunner().invoke(
        cli,
        ["timestamp", "--to-unix", "1970-01-01T00:00:00+00:00"],
    )
    assert result.exit_code == 0
    assert result.output.strip() == "0"


def test_cli_timestamp_converts_iso_to_unix_milliseconds() -> None:
    """Confirm timestamp command converts ISO datetimes to Unix milliseconds."""
    result = CliRunner().invoke(
        cli,
        ["timestamp", "--to-unix", "--milliseconds", "2001-09-09T01:46:40Z"],
    )
    assert result.exit_code == 0
    assert result.output.strip() == "1000000000000"
