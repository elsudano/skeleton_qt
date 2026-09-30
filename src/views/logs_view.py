"""Global log view implementation."""

from PySide6.QtCore import Signal
from PySide6.QtWidgets import QPlainTextEdit, QPushButton, QVBoxLayout

from src.views.base_view import BaseView


class LogsView(BaseView):
    """Display the complete application log history and incoming messages."""

    clear_requested = Signal()

    def __init__(self, parent=None):
        """Initialize the log view.

        Parameters
        ----------
        controller : Controller
            Global application controller.
        parent : QWidget, optional
            Parent widget for the view."""
        super().__init__(parent)
        self.setup_ui()

    def setup_ui(self):
        """Build the log viewer interface."""
        layout = QVBoxLayout(self)
        self._log_text = QPlainTextEdit()
        self._log_text.setReadOnly(True)
        self._log_text.setMaximumBlockCount(2000)
        self._clear_button = self.bind_text(
            QPushButton(), lambda: self.tr("Clear logs")
        )
        layout.addWidget(self._log_text)
        layout.addWidget(self._clear_button)
        # We want the same bottom buttons, for that reason
        # we have used the base_view to config the navigation buttons
        self.setup_navigation_buttons(layout)
        self._clear_button.clicked.connect(self.clear_requested.emit)

    def load_history(self, lines):
        """Load persisted log lines into the viewer.

        Parameters
        ----------
        lines : Iterable[str]
            Log lines to display."""
        self._log_text.setPlainText("\n".join(lines))

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
        self._log_text.clear()
