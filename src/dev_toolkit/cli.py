# src/dev_toolkit/cli.py
# Defines the Click command interface for developer utility commands.
# Connects to: services modules, config/logging_config.py
# Created: 2026-06-12

"""Command-line interface for Dev Toolkit."""

import logging
from pathlib import Path

import click

from dev_toolkit import __version__
from dev_toolkit.config.logging_config import configure_logging
from dev_toolkit.services.base64_service import (
    decode_base64,
    decode_base64_bytes,
    encode_base64,
    encode_base64_bytes,
)
from dev_toolkit.services.hash_service import hash_file, hash_text, verify_checksum
from dev_toolkit.services.password_service import generate_password
from dev_toolkit.services.timestamp_service import convert_timestamp
from dev_toolkit.services.uuid_service import generate_uuid

logger = logging.getLogger(__name__)
HASH_ALGORITHM_ARGUMENT = click.Choice(["sha256", "sha512"], case_sensitive=False)


@click.group()
@click.version_option(version=__version__, prog_name="dev-toolkit")
def cli() -> None:
    """Run developer utility commands from one terminal entry point."""
    configure_logging()


@cli.command("uuid")
def uuid_command() -> None:
    """Generate and print a random UUID4 value."""
    logger.info("Generating UUID4 value")
    click.echo(generate_uuid())


@cli.command("password")
@click.option(
    "--length",
    default=20,
    show_default=True,
    type=click.IntRange(min=8, max=128),
    help="Password length.",
)
@click.option(
    "--no-symbols",
    is_flag=True,
    help="Exclude punctuation symbols from the generated password.",
)
def password_command(length: int, no_symbols: bool) -> None:
    """Generate and print a cryptographically secure password."""
    logger.info("Generating password", extra={"length": length, "symbols": not no_symbols})
    click.echo(generate_password(length=length, include_symbols=not no_symbols))


@cli.group("base64")
def base64_group() -> None:
    """Encode or decode base64 text."""


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


@cli.group("hash")
def hash_group() -> None:
    """Calculate or verify SHA checksums."""


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


@cli.command("timestamp")
@click.argument("value")
def timestamp_command(value: str) -> None:
    """Convert a Unix timestamp to an ISO 8601 UTC datetime."""
    logger.info("Converting timestamp")
    try:
        click.echo(convert_timestamp(value))
    except ValueError as error:
        raise click.ClickException(str(error)) from error


if __name__ == "__main__":
    cli()
