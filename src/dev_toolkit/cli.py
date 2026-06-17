# src/dev_toolkit/cli.py
# Defines the Click command interface for developer utility commands.
# Connects to: services modules, config/logging_config.py
# Created: 2026-06-12

"""Command-line interface for Dev Toolkit."""

import logging
from pathlib import Path

import click

from dev_toolkit import __version__
from dev_toolkit.config.defaults import (
    DEFAULT_JSON_INDENT,
    DEFAULT_PASSWORD_LENGTH,
    get_json_indent_default,
    get_password_length_default,
)
from dev_toolkit.config.logging_config import configure_logging
from dev_toolkit.services.base64_service import (
    decode_base64,
    decode_base64_bytes,
    encode_base64,
    encode_base64_bytes,
)
from dev_toolkit.services.file_service import (
    count_characters,
    count_lines,
    count_words,
    format_file_size,
    get_file_size,
)
from dev_toolkit.services.hash_service import hash_file, hash_text, verify_checksum
from dev_toolkit.services.json_service import format_json, minify_json, validate_json
from dev_toolkit.services.password_service import generate_password
from dev_toolkit.services.timestamp_service import (
    convert_datetime_to_timestamp,
    convert_timestamp,
)
from dev_toolkit.services.uuid_service import generate_uuid

logger = logging.getLogger(__name__)
HASH_ALGORITHM_ARGUMENT = click.Choice(["sha256", "sha512"], case_sensitive=False)
JSON_INDENT_RANGE = click.IntRange(min=0, max=8)


@click.group()
@click.version_option(version=__version__, prog_name="dev-toolkit")
def cli() -> None:
    """Run developer utility commands from one terminal entry point.

    Examples:

      dev-toolkit uuid

      dev-toolkit password --length 24

      dev-toolkit json validate --input-file data.json
    """
    configure_logging()


@cli.command("uuid")
def uuid_command() -> None:
    """Generate and print a random UUID4 value."""
    logger.info("Generating UUID4 value")
    click.echo(generate_uuid())


@cli.command("password")
@click.option(
    "--length",
    default=None,
    show_default=f"{DEFAULT_PASSWORD_LENGTH} or DEV_TOOLKIT_PASSWORD_LENGTH",
    type=click.IntRange(min=8, max=128),
    help="Password length.",
)
@click.option(
    "--no-symbols",
    is_flag=True,
    help="Exclude punctuation symbols from the generated password.",
)
def password_command(length: int | None, no_symbols: bool) -> None:
    """Generate and print a cryptographically secure password."""
    try:
        resolved_length = length if length is not None else get_password_length_default()
    except ValueError as error:
        raise click.ClickException(str(error)) from error

    logger.info(
        "Generating password",
        extra={"length": resolved_length, "symbols": not no_symbols},
    )
    click.echo(generate_password(length=resolved_length, include_symbols=not no_symbols))


@cli.group("base64")
def base64_group() -> None:
    """Encode or decode base64 text.

    Examples:

      dev-toolkit base64 encode "hello"

      dev-toolkit base64 decode "aGVsbG8="

      dev-toolkit base64 encode --input-file plain.txt --output-file encoded.txt
    """


@base64_group.command("encode")
@click.argument("text", required=False)
@click.option(
    "--input-file",
    "-i",
    type=click.Path(exists=True, dir_okay=False, path_type=Path),
    help="Read raw input from a file instead of the text argument.",
)
@click.option(
    "--output-file",
    "-o",
    type=click.Path(dir_okay=False, writable=True, path_type=Path),
    help="Write encoded output to a file instead of stdout.",
)
def base64_encode_command(
    text: str | None,
    input_file: Path | None,
    output_file: Path | None,
) -> None:
    """Encode text or file content as base64."""
    logger.info("Encoding base64 text")
    if text is None and input_file is None:
        raise click.UsageError("Provide TEXT or --input-file.")

    if text is not None and input_file is not None:
        raise click.UsageError("Use either TEXT or --input-file, not both.")

    encoded_text = (
        encode_base64_bytes(input_file.read_bytes())
        if input_file is not None
        else encode_base64(text or "")
    )

    if output_file is not None:
        output_file.write_text(encoded_text, encoding="utf-8")
        return

    click.echo(encoded_text)


@base64_group.command("decode")
@click.argument("text", required=False)
@click.option(
    "--input-file",
    "-i",
    type=click.Path(exists=True, dir_okay=False, path_type=Path),
    help="Read base64 text from a file instead of the text argument.",
)
@click.option(
    "--output-file",
    "-o",
    type=click.Path(dir_okay=False, writable=True, path_type=Path),
    help="Write decoded bytes to a file instead of stdout.",
)
def base64_decode_command(
    text: str | None,
    input_file: Path | None,
    output_file: Path | None,
) -> None:
    """Decode base64 text or file content."""
    logger.info("Decoding base64 text")
    if text is None and input_file is None:
        raise click.UsageError("Provide TEXT or --input-file.")

    if text is not None and input_file is not None:
        raise click.UsageError("Use either TEXT or --input-file, not both.")

    source_text = (
        input_file.read_text(encoding="utf-8")
        if input_file is not None
        else text or ""
    )

    try:
        if output_file is not None:
            output_file.write_bytes(decode_base64_bytes(source_text.strip()))
            return

        click.echo(decode_base64(source_text.strip()))
    except ValueError as error:
        raise click.ClickException(str(error)) from error


@cli.group("file")
def file_group() -> None:
    """Inspect file size and text counts.

    Examples:

      dev-toolkit file size README.md

      dev-toolkit file lines README.md

      dev-toolkit file stats README.md
    """


@file_group.command("size")
@click.argument(
    "input_file",
    type=click.Path(exists=True, dir_okay=False, path_type=Path),
)
@click.option(
    "--human",
    is_flag=True,
    help="Print a human-readable size instead of raw bytes.",
)
def file_size_command(input_file: Path, human: bool) -> None:
    """Print file size in bytes or human-readable units."""
    logger.info("Reading file size")
    size_bytes = get_file_size(input_file)
    if human:
        click.echo(format_file_size(size_bytes))
        return

    click.echo(size_bytes)


@file_group.command("lines")
@click.argument(
    "input_file",
    type=click.Path(exists=True, dir_okay=False, path_type=Path),
)
def file_lines_command(input_file: Path) -> None:
    """Print the number of lines in a text file."""
    logger.info("Counting file lines")
    try:
        click.echo(count_lines(input_file))
    except UnicodeDecodeError as error:
        raise click.ClickException("Input file must be UTF-8 text.") from error


@file_group.command("stats")
@click.argument(
    "input_file",
    type=click.Path(exists=True, dir_okay=False, path_type=Path),
)
def file_stats_command(input_file: Path) -> None:
    """Print size, line, word, and character counts for a text file."""
    logger.info("Reading file statistics")
    try:
        click.echo(f"bytes: {get_file_size(input_file)}")
        click.echo(f"lines: {count_lines(input_file)}")
        click.echo(f"words: {count_words(input_file)}")
        click.echo(f"characters: {count_characters(input_file)}")
    except UnicodeDecodeError as error:
        raise click.ClickException("Input file must be UTF-8 text.") from error


@cli.group("hash")
def hash_group() -> None:
    """Calculate or verify SHA checksums.

    Examples:

      dev-toolkit hash text sha256 "hello"

      dev-toolkit hash file sha512 archive.zip

      dev-toolkit hash verify sha256 "<expected-digest>" archive.zip
    """


@hash_group.command("text")
@click.argument("algorithm", type=HASH_ALGORITHM_ARGUMENT)
@click.argument("text")
def hash_text_command(algorithm: str, text: str) -> None:
    """Hash direct text with SHA-256 or SHA-512."""
    logger.info("Hashing text", extra={"algorithm": algorithm})
    try:
        click.echo(hash_text(text, algorithm))
    except ValueError as error:
        raise click.ClickException(str(error)) from error


@hash_group.command("file")
@click.argument("algorithm", type=HASH_ALGORITHM_ARGUMENT)
@click.argument(
    "input_file",
    type=click.Path(exists=True, dir_okay=False, path_type=Path),
)
def hash_file_command(algorithm: str, input_file: Path) -> None:
    """Hash file content with SHA-256 or SHA-512."""
    logger.info("Hashing file", extra={"algorithm": algorithm})
    try:
        click.echo(hash_file(input_file, algorithm))
    except ValueError as error:
        raise click.ClickException(str(error)) from error


@hash_group.command("verify")
@click.argument("algorithm", type=HASH_ALGORITHM_ARGUMENT)
@click.argument("expected_digest")
@click.argument(
    "input_file",
    type=click.Path(exists=True, dir_okay=False, path_type=Path),
)
def hash_verify_command(
    algorithm: str,
    expected_digest: str,
    input_file: Path,
) -> None:
    """Verify a file checksum against an expected digest."""
    logger.info("Verifying file checksum", extra={"algorithm": algorithm})
    try:
        actual_digest = hash_file(input_file, algorithm)
    except ValueError as error:
        raise click.ClickException(str(error)) from error

    if verify_checksum(actual_digest, expected_digest):
        click.echo("OK")
        return

    raise click.ClickException(f"Checksum mismatch. Actual digest: {actual_digest}")


@cli.group("json")
def json_group() -> None:
    """Format, minify, or validate JSON text.

    Examples:

      dev-toolkit json format "{\\"b\\":2,\\"a\\":1}"

      dev-toolkit json minify --input-file data.json

      dev-toolkit json validate --input-file data.json
    """


@json_group.command("format")
@click.argument("text", required=False)
@click.option(
    "--input-file",
    "-i",
    type=click.Path(exists=True, dir_okay=False, path_type=Path),
    help="Read JSON from a file instead of the text argument.",
)
@click.option(
    "--output-file",
    "-o",
    type=click.Path(dir_okay=False, writable=True, path_type=Path),
    help="Write formatted JSON to a file instead of stdout.",
)
@click.option(
    "--indent",
    default=None,
    show_default=f"{DEFAULT_JSON_INDENT} or DEV_TOOLKIT_JSON_INDENT",
    type=JSON_INDENT_RANGE,
    help="Number of spaces for formatted output.",
)
def json_format_command(
    text: str | None,
    input_file: Path | None,
    output_file: Path | None,
    indent: int | None,
) -> None:
    """Format JSON from direct text or a file."""
    logger.info("Formatting JSON")
    source_text = read_text_argument_or_file(text, input_file)
    try:
        resolved_indent = indent if indent is not None else get_json_indent_default()
        formatted_json = format_json(source_text, indent=resolved_indent)
    except ValueError as error:
        raise click.ClickException(str(error)) from error

    write_text_or_echo(formatted_json, output_file)


@json_group.command("minify")
@click.argument("text", required=False)
@click.option(
    "--input-file",
    "-i",
    type=click.Path(exists=True, dir_okay=False, path_type=Path),
    help="Read JSON from a file instead of the text argument.",
)
@click.option(
    "--output-file",
    "-o",
    type=click.Path(dir_okay=False, writable=True, path_type=Path),
    help="Write minified JSON to a file instead of stdout.",
)
def json_minify_command(
    text: str | None,
    input_file: Path | None,
    output_file: Path | None,
) -> None:
    """Minify JSON from direct text or a file."""
    logger.info("Minifying JSON")
    source_text = read_text_argument_or_file(text, input_file)
    try:
        minified_json = minify_json(source_text)
    except ValueError as error:
        raise click.ClickException(str(error)) from error

    write_text_or_echo(minified_json, output_file)


@json_group.command("validate")
@click.argument("text", required=False)
@click.option(
    "--input-file",
    "-i",
    type=click.Path(exists=True, dir_okay=False, path_type=Path),
    help="Read JSON from a file instead of the text argument.",
)
def json_validate_command(text: str | None, input_file: Path | None) -> None:
    """Validate JSON from direct text or a file."""
    logger.info("Validating JSON")
    source_text = read_text_argument_or_file(text, input_file)
    try:
        validate_json(source_text)
    except ValueError as error:
        raise click.ClickException(str(error)) from error

    click.echo("OK")


@cli.command("timestamp")
@click.argument("value")
@click.option(
    "--to-unix",
    is_flag=True,
    help="Treat VALUE as an ISO 8601 datetime and convert it to a Unix timestamp.",
)
@click.option(
    "--milliseconds",
    is_flag=True,
    help="Return Unix milliseconds when used with --to-unix.",
)
def timestamp_command(value: str, to_unix: bool, milliseconds: bool) -> None:
    """Convert between Unix timestamps and ISO 8601 UTC datetimes.

    Examples:

      dev-toolkit timestamp 1718064000

      dev-toolkit timestamp --to-unix "2024-06-11T00:00:00+00:00"

      dev-toolkit timestamp --to-unix --milliseconds "2001-09-09T01:46:40Z"
    """
    logger.info("Converting timestamp")
    try:
        if to_unix:
            click.echo(convert_datetime_to_timestamp(value, milliseconds=milliseconds))
            return

        click.echo(convert_timestamp(value))
    except ValueError as error:
        raise click.ClickException(str(error)) from error


def read_text_argument_or_file(text: str | None, input_file: Path | None) -> str:
    """Read text from either a direct argument or an input file.

    Parameters:
        text: Optional direct text argument.
        input_file: Optional path to read.

    Returns:
        Text read from the selected source.

    Raises:
        click.UsageError: If the source selection is invalid.
    """
    if text is None and input_file is None:
        raise click.UsageError("Provide TEXT or --input-file.")

    if text is not None and input_file is not None:
        raise click.UsageError("Use either TEXT or --input-file, not both.")

    if input_file is not None:
        return input_file.read_text(encoding="utf-8")

    return text or ""


def write_text_or_echo(text: str, output_file: Path | None) -> None:
    """Write text to an output file or stdout.

    Parameters:
        text: Text to write.
        output_file: Optional output file path.

    Returns:
        None.
    """
    if output_file is not None:
        output_file.write_text(text, encoding="utf-8")
        return

    click.echo(text)


if __name__ == "__main__":
    cli()
