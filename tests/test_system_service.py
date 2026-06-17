# tests/test_system_service.py
# Verifies read-only system diagnostics helpers.
# Connects to: src/dev_toolkit/services/system_service.py
# Created: 2026-06-17

"""Tests for system diagnostics service functions."""

import sys
from pathlib import Path

import pytest

from dev_toolkit.services.system_service import (
    get_current_directory,
    get_environment_value,
    get_platform_summary,
    get_python_executable,
    get_python_version,
    get_system_info,
)


def test_get_current_directory_returns_cwd() -> None:
    """Confirm current directory helper returns process cwd."""
    assert get_current_directory() == str(Path.cwd())


def test_get_python_version_returns_text() -> None:
    """Confirm Python version helper returns nonempty text."""
    assert get_python_version()


def test_get_python_executable_returns_sys_executable() -> None:
    """Confirm Python executable helper returns sys.executable."""
    assert get_python_executable() == sys.executable


def test_get_platform_summary_returns_text() -> None:
    """Confirm platform summary helper returns nonempty text."""
    assert get_platform_summary()


def test_get_environment_value_returns_set_variable(monkeypatch: pytest.MonkeyPatch) -> None:
    """Confirm environment helper returns set variable values."""
    monkeypatch.setenv("DEV_TOOLKIT_TEST_ENV", "available")
    assert get_environment_value("DEV_TOOLKIT_TEST_ENV") == "available"


def test_get_environment_value_rejects_missing_variable(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Confirm environment helper reports missing variables."""
    monkeypatch.delenv("DEV_TOOLKIT_TEST_ENV", raising=False)
    with pytest.raises(ValueError, match="not set"):
        get_environment_value("DEV_TOOLKIT_TEST_ENV")


def test_get_system_info_returns_expected_keys() -> None:
    """Confirm system info returns core diagnostic keys."""
    info = get_system_info()
    assert set(info) == {"cwd", "platform", "python", "executable"}
