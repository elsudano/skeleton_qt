"""Base classes and shared behavior for application views."""

from PySide6.QtCore import QEvent, Signal, qCInfo
from PySide6.QtWidgets import (QApplication, QPlainTextEdit, QVBoxLayout, QHBoxLayout, QPushButton, QWidget)
from src.core.text_binder import TextBinder
from src.views.views import Views


class BaseView(QWidget):
    """Provide common behavior shared by application views, including logging and translation bindings."""

    navigation_requested = Signal(str)

    def __init__(self, parent=None):
        """Initialize the view.

        Parameters
        ----------
        controller : Controller
            Global application controller used for application-level interactions.
        parent : QWidget, optional
            Parent widget for the view."""
        super().__init__(parent)
        self._texts = TextBinder()
        self._log_categories = ()
        self._log_panel = None

    def setup_log_panel(self, layout: QVBoxLayout, categories: tuple[str, ...]):
        """Add the log panel for this view to the supplied layout.

        Parameters
        ----------
        layout : QLayout
            Layout that receives the log panel.
        categories : Iterable[str]
            Logging categories that should be displayed by this view."""
        self._log_categories = categories
        self._log_panel = QPlainTextEdit()
        self._log_panel.setReadOnly(True)
        self._log_panel.setMaximumBlockCount(500)
        layout.addWidget(self._log_panel)

    def setup_navigation_buttons(self, layout: QVBoxLayout):
        bottom_layout = QHBoxLayout()
        self._back_button = self.bind_text(
            QPushButton(), lambda: self.tr("&Back"),)
        self._back_button.setMinimumHeight(50)
        self._back_button.setMinimumWidth(100)
        self._exit_button = self.bind_text(
            QPushButton(), lambda: self.tr("E&xit"),)
        self._exit_button.setMinimumHeight(50)
        self._exit_button.setMinimumWidth(100)
        if self.__class__.__name__ != "HomeView":
            bottom_layout.addWidget(self._back_button)
        bottom_layout.addStretch()
        bottom_layout.addWidget(self._exit_button)
        self._back_button.clicked.connect(self._action_back_button)
        self._exit_button.clicked.connect(self._action_exit_button)
        layout.addLayout(bottom_layout)

    def _action_back_button(self):
        """This will be the actions that we can make when we press back_button"""
        qCInfo(self._log, "The back_button was clicked")
        self.request_navigation(Views.HOME)
        # raise NotImplementedError(
        #     f"{self.__class__.__name__} debe implementar setup_navigation_buttons()"
        # )

    def _action_exit_button(self):
        """This will be the actions that we can make when we press exit_button"""
        qCInfo(self._log, "The exit_button was clicked")
        QApplication.instance().quit()

    def append_log(self, category: str, level: str, message: str, formatted: str):
        """Append a log message when it belongs to this view's categories.

        Parameters
        ----------
        category : str
            Logging category that produced the message.
        level : str
            Human-readable logging level.
        message : str
            Log message text.
        formatted : str
            Fully formatted message ready for display."""
        if self._log_panel is None:
            return
        if any(
            category == expected or category.startswith(f"{expected}.")
            for expected in self._log_categories
        ):
            self._log_panel.appendPlainText(formatted)

    def request_navigation(self, name: str):
        """Request navigation to another view.

        Parameters
        ----------
        name : str
            Identifier of the target view."""
        self.navigation_requested.emit(name)

    def bind_text(self, widget, source, setter: str = "setText"):
        """Bind a text to a widget and keep it synchronized with the active language.

        Parameters
        ----------
        widget : QObject
            Widget, action or window that displays the text.
        source : callable or str
            Callable returning the text or a plain string that is applied as-is.
        setter : str, optional
            Name of the widget method that receives the text.

        Returns
        -------
        QObject
            The same widget, so it can be created and bound in one line."""
        return self._texts.bind(widget, source, setter)

    def changeEvent(self, event):
        """Re-apply bound texts when the application language changes.

        Parameters
        ----------
        event : QEvent
            Change event sent by Qt."""
        if event.type() == QEvent.Type.LanguageChange:
            self._texts.refresh()
        super().changeEvent(event)
