# src/dev_toolkit/config/defaults.py
# Reads validated environment defaults for CLI options.
# Connects to: src/dev_toolkit/cli.py, .env.example
# Created: 2026-06-17

"""Environment-driven default configuration for Dev Toolkit."""

import os

DEFAULT_JSON_INDENT = 2
DEFAULT_PASSWORD_LENGTH = 20
JSON_INDENT_ENV_VAR = "DEV_TOOLKIT_JSON_INDENT"
PASSWORD_LENGTH_ENV_VAR = "DEV_TOOLKIT_PASSWORD_LENGTH"
MIN_JSON_INDENT = 0
MAX_JSON_INDENT = 8
MIN_PASSWORD_LENGTH = 8
MAX_PASSWORD_LENGTH = 128


def get_json_indent_default() -> int:
    """Read the default JSON indentation width from the environment.

    Parameters:
        None.

    Returns:
        Validated indentation width.

    Raises:
        ValueError: If the environment value is invalid.
    """
    return read_int_default(
        env_var=JSON_INDENT_ENV_VAR,
        fallback=DEFAULT_JSON_INDENT,
        minimum=MIN_JSON_INDENT,
        maximum=MAX_JSON_INDENT,
    )


def get_password_length_default() -> int:
    """Read the default password length from the environment.

    Parameters:
        None.

    Returns:
        Validated password length.

    Raises:
        ValueError: If the environment value is invalid.
    """
    return read_int_default(
        env_var=PASSWORD_LENGTH_ENV_VAR,
        fallback=DEFAULT_PASSWORD_LENGTH,
        minimum=MIN_PASSWORD_LENGTH,
        maximum=MAX_PASSWORD_LENGTH,
    )


def read_int_default(env_var: str, fallback: int, minimum: int, maximum: int) -> int:
    """Read and validate an integer environment default.

    Parameters:
        env_var: Environment variable name.
        fallback: Value to use when the variable is unset.
        minimum: Inclusive minimum value.
        maximum: Inclusive maximum value.

    Returns:
        Validated integer default.

    Raises:
        ValueError: If the value is not an integer or is outside the range.
    """
    raw_value = os.getenv(env_var)
    if raw_value is None:
        return fallback

    try:
        parsed_value = int(raw_value)
    except ValueError as error:
        raise ValueError(f"{env_var} must be an integer.") from error

    if parsed_value < minimum or parsed_value > maximum:
        raise ValueError(f"{env_var} must be between {minimum} and {maximum}.")

    return parsed_value
