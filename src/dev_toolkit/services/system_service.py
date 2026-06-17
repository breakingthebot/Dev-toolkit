# src/dev_toolkit/services/system_service.py
# Collects read-only local system diagnostics for CLI commands.
# Connects to: src/dev_toolkit/cli.py
# Created: 2026-06-17

"""System diagnostics utility functions."""

import os
import platform
import sys
from pathlib import Path


def get_current_directory() -> str:
    """Return the current working directory.

    Parameters:
        None.

    Returns:
        Current working directory path.
    """
    return str(Path.cwd())


def get_python_version() -> str:
    """Return the active Python version.

    Parameters:
        None.

    Returns:
        Python version string.
    """
    return platform.python_version()


def get_python_executable() -> str:
    """Return the active Python executable path.

    Parameters:
        None.

    Returns:
        Python executable path.
    """
    return sys.executable


def get_platform_summary() -> str:
    """Return a platform summary string.

    Parameters:
        None.

    Returns:
        Platform summary string.
    """
    return platform.platform()


def get_environment_value(name: str) -> str:
    """Return an environment variable value.

    Parameters:
        name: Environment variable name.

    Returns:
        Environment variable value.

    Raises:
        ValueError: If the variable is not set.
    """
    value = os.getenv(name)
    if value is None:
        raise ValueError(f"Environment variable is not set: {name}")

    return value


def get_system_info() -> dict[str, str]:
    """Return core system diagnostics.

    Parameters:
        None.

    Returns:
        Mapping of diagnostic names to values.
    """
    return {
        "cwd": get_current_directory(),
        "platform": get_platform_summary(),
        "python": get_python_version(),
        "executable": get_python_executable(),
    }
