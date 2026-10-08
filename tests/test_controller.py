from PySide6.QtCore import QLoggingCategory, qCInfo
from PySide6.QtWidgets import QStackedWidget

from src.controllers.controller import Controller
from src.views.home_view import HomeView
from src.views.logs_view import LogsView
from src.views.settings_view import SettingsView
from src.views.views import Views


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


def test_settings_gui_logging_toggle_reaches_logging_manager(qtbot, logging_manager):
    controller, container = _make_controller(qtbot, logging_manager)
    controller.navigate(Views.SETTINGS)
    view = container.currentWidget()
    received = []
    logging_manager.message_logged.connect(lambda *args: received.append(args))

    view.logging_gui_changed.emit(False)
    qCInfo(QLoggingCategory("skeleton.core.application"), "should not reach gui")
    assert received == []

    view.logging_gui_changed.emit(True)
    qCInfo(QLoggingCategory("skeleton.core.application"), "should reach gui")
    assert any(message[2] == "should reach gui" for message in received)


def test_logs_clear_requested_clears_model_and_view(qtbot, logging_manager):
    # Regression test: clear_requested used to be wired only to the view,
    # so the on-disk/buffered history survived a click on "Clear logs".
    controller, container = _make_controller(qtbot, logging_manager)
    controller.navigate(Views.LOGS)
    view = container.currentWidget()
    assert isinstance(view, LogsView)

    qCInfo(QLoggingCategory("skeleton.core.application"), "line to clear")
    assert logging_manager.records()
    assert view._log_text.toPlainText() != ""

    view.clear_requested.emit()

    assert logging_manager.records() == ()
    assert view._log_text.toPlainText() == ""
