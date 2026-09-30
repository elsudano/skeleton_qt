"""Shared pytest fixtures for the test suite."""

import pytest

from src.core import config
from src.core.logging import LoggingManager


@pytest.fixture
def logging_manager(monkeypatch, tmp_path):
    """Provide a LoggingManager isolated from the real application output.

    GUI output is the only enabled output, so tests never print to the
    console; the log directory is redirected to a pytest-managed temporary
    path, so tests never read or write the developer's real log file.

    Parameters
    ----------
    monkeypatch : MonkeyPatch
        Pytest fixture used to override configuration for the test.
    tmp_path : Path
        Pytest-managed temporary directory unique to the test.

    Yields
    ------
    LoggingManager
        Logging manager ready for use by the test."""
    monkeypatch.setattr(config, "LOG_OUTPUTS", (config.LOG_OUTPUT_GUI,))
    monkeypatch.setattr(config, "LOGS_DIR", tmp_path)
    manager = LoggingManager()
    yield manager
    manager.close()


@pytest.fixture
def logging_manager_with_file(monkeypatch, tmp_path):
    """Provide a LoggingManager with file output enabled, isolated in a
    temporary directory, for tests that exercise persisted log behavior.

    Parameters
    ----------
    monkeypatch : MonkeyPatch
        Pytest fixture used to override configuration for the test.
    tmp_path : Path
        Pytest-managed temporary directory unique to the test.

    Yields
    ------
    LoggingManager
        Logging manager, with file output enabled, ready for use by the
        test."""
    monkeypatch.setattr(
        config, "LOG_OUTPUTS",
        (config.LOG_OUTPUT_GUI, config.LOG_OUTPUT_FILE))
    monkeypatch.setattr(config, "LOGS_DIR", tmp_path)
    manager = LoggingManager()
    yield manager
    manager.close()
