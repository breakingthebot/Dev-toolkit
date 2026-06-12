# src/dev_toolkit/config/logging_config.py
# Configures basic structured logging for CLI execution.
# Connects to: src/dev_toolkit/cli.py
# Created: 2026-06-12

"""Logging configuration for command-line runs."""

import logging

LOG_FORMAT = "%(asctime)s %(levelname)s %(name)s %(message)s"


def configure_logging() -> None:
    """Configure application logging if no handlers already exist.

    Parameters:
        None.

    Returns:
        None.
    """
    logging.basicConfig(level=logging.WARNING, format=LOG_FORMAT)

