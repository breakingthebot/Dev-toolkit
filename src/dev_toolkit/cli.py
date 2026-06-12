# src/dev_toolkit/cli.py
# Defines the Click command interface for developer utility commands.
# Connects to: services modules, config/logging_config.py
# Created: 2026-06-12

"""Command-line interface for Dev Toolkit."""

import logging

import click

from dev_toolkit import __version__
from dev_toolkit.config.logging_config import configure_logging
from dev_toolkit.services.base64_service import decode_base64, encode_base64
from dev_toolkit.services.password_service import generate_password
from dev_toolkit.services.timestamp_service import convert_timestamp
from dev_toolkit.services.uuid_service import generate_uuid

logger = logging.getLogger(__name__)


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
@click.argument("text")
def base64_encode_command(text: str) -> None:
    """Encode text as base64."""
    logger.info("Encoding base64 text")
    click.echo(encode_base64(text))


@base64_group.command("decode")
@click.argument("text")
def base64_decode_command(text: str) -> None:
    """Decode base64 text."""
    logger.info("Decoding base64 text")
    try:
        click.echo(decode_base64(text))
    except ValueError as error:
        raise click.ClickException(str(error)) from error


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

