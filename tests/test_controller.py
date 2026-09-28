import pytest
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QStackedWidget

from src.controllers.controller import Controller
from src.core import config
from src.core.logging import LoggingManager
from src.views.home_view import HomeView
from src.views.settings_view import SettingsView
from src.views.views import Views


@pytest.fixture
def logging_manager(monkeypatch):
    monkeypatch.setattr(config, "LOG_OUTPUTS", (config.LOG_OUTPUT_GUI,))
    manager = LoggingManager()
    yield manager
    manager.close()


def _make_controller(qtbot, logging_manager):
    container = QStackedWidget()
    qtbot.addWidget(container)
    return Controller(container, logging_manager), container


def test_navigate_creates_views_lazily(qtbot, logging_manager):
    controller, container = _make_controller(qtbot, logging_manager)
    assert container.count() == 0
    controller.navigate(Views.HOME)
    assert container.count() == 1
    assert isinstance(container.currentWidget(), HomeView)


def test_navigate_reuses_cached_views(qtbot, logging_manager):
    controller, container = _make_controller(qtbot, logging_manager)
    controller.navigate(Views.HOME)
    home = container.currentWidget()
    controller.navigate(Views.SETTINGS)
    assert isinstance(container.currentWidget(), SettingsView)
    assert container.count() == 2
    controller.navigate(Views.HOME)
    assert container.currentWidget() is home


def test_welcome_button_shows_model_message(qtbot, logging_manager):
    controller, container = _make_controller(qtbot, logging_manager)
    controller.navigate(Views.HOME)
    home = container.currentWidget()
    qtbot.mouseClick(home._welcome_button, Qt.MouseButton.LeftButton)
    assert home._message_label.text() == "Welcome to Skeleton Qt"
