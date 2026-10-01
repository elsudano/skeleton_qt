"""Tests for global application themes."""

import pytest
from PySide6.QtWidgets import QApplication

from src.core import config
from src.core.application import Application


@pytest.mark.parametrize("theme", ["light", "dark"])
def test_theme_stylesheet_exists_and_is_not_empty(theme):
    """Ensure every supported theme has a stylesheet.

    Parameters
    ----------
    theme : str
        Theme identifier whose stylesheet is checked.
    """
    stylesheet = config.STYLES_DIR / f"{theme}.qss"
    assert stylesheet.is_file()
    assert stylesheet.read_text(encoding="utf-8").strip()


def test_application_applies_and_switches_global_theme(qtbot):
    """Verify theme changes update QApplication's global stylesheet."""
    qt_application = QApplication.instance()
    application = Application(qt_application)
    qtbot.addWidget(application._main_window)

    try:
        assert application.theme == "light"
        assert qt_application.styleSheet() == (
            config.STYLES_DIR / "light.qss"
        ).read_text(encoding="utf-8")

        application.set_theme("dark")
        assert application.theme == "dark"
        assert qt_application.styleSheet() == (
            config.STYLES_DIR / "dark.qss"
        ).read_text(encoding="utf-8")
    finally:
        qt_application.setStyleSheet("")
        application._logging_manager.close()
        application._main_window.close()


def test_options_theme_actions_are_exclusive_and_apply_theme(qtbot):
    """Verify the Options theme actions are exclusive and apply globally."""
    qt_application = QApplication.instance()
    application = Application(qt_application)
    qtbot.addWidget(application._main_window)

    try:
        light_action = application._theme_actions["light"]
        dark_action = application._theme_actions["dark"]
        assert light_action.isCheckable()
        assert dark_action.isCheckable()
        assert light_action.isChecked()
        assert not dark_action.isChecked()

        dark_action.trigger()
        assert application.theme == "dark"
        assert dark_action.isChecked()
        assert not light_action.isChecked()
    finally:
        qt_application.setStyleSheet("")
        application._logging_manager.close()
        application._main_window.close()
