"""Base classes and shared behavior for application views."""

from PySide6.QtCore import QEvent, QLoggingCategory, Signal, qCDebug, qCInfo
from PySide6.QtWidgets import (
    QApplication,
    QHBoxLayout,
    QLabel,
    QPlainTextEdit,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from src.core.config import BUTTON_MINIMUM_HEIGHT_SIZE, BUTTON_MINIMUM_WIDTH_SIZE
from src.core.text_binder import TextBinder
from src.views.views import Views


class Base_View(QWidget):
    """Provide common behavior shared by application views, including logging and translation bindings."""

    # We need to declare this in this way just to handle the known issue: use-after-free
    # in python, in this case PySide6 when you create a category, PySide6 is creating a buffer
    # and this buffet pointing a different memory directions, for that reason fail.
    _CATEGORY = "skeleton.view.base_view"
    _log = QLoggingCategory(_CATEGORY)
    navigation_requested = Signal(str)

    def __init__(self, parent=None):
        """Initialize the view.

        Parameters
        ----------
        parent : QWidget, optional
            Parent widget for the view."""
        super().__init__(parent)
        self._texts = TextBinder()
        self._log_categories = ()
        self._log_panel = None
        self._content_layout = QVBoxLayout(self)
        self._content_layout.setContentsMargins(10, 10, 10, 10)
        self._content_layout.setSpacing(10)
        qCInfo(self._log, "The class Base_View was created")
        qCDebug(self._log, "The class Base_View was created")

    def setup_ui(self):
        """Build the common view interface.

        The base interface provides a content layout, a log panel, and the
        standard navigation buttons so newly created views have a useful
        interface immediately.
        """
        category = getattr(self, "_CATEGORY", None)
        categories = (category,) if category else ()
        if category and ".view." in category:
            categories += (category.replace(".view.", ".model.", 1),)
        if self.__class__.__name__ != "Logs_View":
            self.setup_log_panel(self._content_layout, categories)
        self.setup_navigation_buttons(self._content_layout)
        qCDebug(self._log, "The class Base_View was configured")

    def setup_log_panel(self, layout: QVBoxLayout, categories: tuple[str, ...]):
        """Add the log panel for this view to the supplied layout.

        Parameters
        ----------
        layout : QLayout
            Layout that receives the log panel.
        categories : Iterable[str]
            Logging categories that should be displayed by this view."""
        self._log_categories = categories
        self._logs_label = self.bind_text(QLabel(), lambda: self.tr("Logs"))
        font = self._logs_label.font()
        font.setBold(True)
        self._logs_label.setFont(font)
        layout.addWidget(self._logs_label)
        self._log_panel = QPlainTextEdit()
        self._log_panel.setReadOnly(True)
        self._log_panel.setMaximumBlockCount(500)
        layout.addWidget(self._log_panel)
        qCDebug(self._log, "The Log Panel was created")

    def setup_navigation_buttons(self, layout: QVBoxLayout):
        bottom_layout = QHBoxLayout()
        self._back_button = self.bind_text(
            QPushButton(), lambda: self.tr("&Back"),)
        self._back_button.setMinimumHeight(BUTTON_MINIMUM_HEIGHT_SIZE)
        self._back_button.setMinimumWidth(BUTTON_MINIMUM_WIDTH_SIZE)
        self._exit_button = self.bind_text(
            QPushButton(), lambda: self.tr("E&xit"),)
        self._exit_button.setMinimumHeight(BUTTON_MINIMUM_HEIGHT_SIZE)
        self._exit_button.setMinimumWidth(BUTTON_MINIMUM_WIDTH_SIZE)
        if self.__class__.__name__ != "Home_View":
            bottom_layout.addWidget(self._back_button)
        bottom_layout.addStretch()
        bottom_layout.addWidget(self._exit_button)
        self._back_button.clicked.connect(self._action_back_button)
        self._exit_button.clicked.connect(self._action_exit_button)
        layout.addLayout(bottom_layout)
        qCDebug(self._log, "We have added the default buttons Back/Exit")

    def _action_back_button(self):
        """This will be the actions that we can make when we press back_button"""
        qCDebug(self._log, "The back_button was clicked")
        self.request_navigation(Views.HOME)
        # raise NotImplementedError(
        #     f"{self.__class__.__name__} debe implementar setup_navigation_buttons()"
        # )

    def _action_exit_button(self):
        """This will be the actions that we can make when we press exit_button"""
        qCDebug(self._log, "The exit_button was clicked")
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
        qCDebug(self._log, f"The navigation was requested to: {name}")

    def bind_text(self, widget, source, setter=None):
        """Bind a translatable text source to a widget setter.

        This method intentionally mirrors :meth:`MainWindow.bind_text`.
        Both classes maintain their own :class:`TextBinder` instance because
        they manage independent UI scopes.

        Parameters
        ----------
        widget : QObject
            Widget, action or window that displays the text.
        source : callable or str
            Callable returning the text or a plain string that is applied as-is.
        setter : callable, optional
            Callable that receives the text. If omitted, ``widget.setText`` is used.

        Returns
        -------
        QObject
            The same widget, so it can be created and bound in one line."""
        qCDebug(self._log, f"We have translated {source()}")
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
