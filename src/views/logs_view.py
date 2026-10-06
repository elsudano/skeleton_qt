"""Global log view implementation."""

from PySide6.QtCore import QLoggingCategory, Signal, qCDebug, qCInfo
from PySide6.QtWidgets import QPlainTextEdit, QPushButton

from src.views.base_view import BaseView


class LogsView(BaseView):
    """Display the complete application log history and incoming messages."""

    # We need to declare this in this way just to handle the known issue: use-after-free
    # in python, in this case PySide6 when you create a category, PySide6 is creating a buffer
    # and this buffet pointing a different memory directions, for that reason fail.
    _CATEGORY = "skeleton.view.logs_view"
    _log = QLoggingCategory(_CATEGORY)

    clear_requested = Signal()

    def __init__(self, parent=None):
        """Initialize the log view.

        Parameters
        ----------
        parent : QWidget, optional
            Parent widget for the view."""
        super().__init__(parent)
        self.setup_ui()
        super().setup_ui()
        qCInfo(self._log, "The class LogsView was created")
        qCDebug(self._log, "The class LogsView was created")

    def setup_ui(self):
        """Build the log viewer interface."""
        self._log_text = QPlainTextEdit()
        self._log_text.setReadOnly(True)
        self._log_text.setMaximumBlockCount(2000)
        self._clear_button = self.bind_text(
            QPushButton(), lambda: self.tr("Clear logs")
        )
        self._content_layout.addWidget(self._log_text)
        self._content_layout.addWidget(self._clear_button)
        self._clear_button.clicked.connect(self.clear_requested.emit)
        qCDebug(self._log, "The class LogsView was configured")

    def load_history(self, lines):
        """Load persisted log lines into the viewer.

        Parameters
        ----------
        lines : Iterable[str]
            Log lines to display."""
        self._log_text.setPlainText("\n".join(lines))
        qCDebug(self._log, "The Logs history was loaded")

    def append_log(self, category: str, level: str, message: str, formatted: str):
        """Append a log message to the global log viewer.

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
        self._log_text.appendPlainText(formatted)

    def clear(self):
        """Clear displayed log messages."""
        qCDebug(self._log, "The Logs history was cleaned")
        self._log_text.clear()
