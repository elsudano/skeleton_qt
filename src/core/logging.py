"""Central Qt logging infrastructure and output management."""

from __future__ import annotations

import sys
from collections import deque
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from threading import Lock

from PySide6.QtCore import (
    QLoggingCategory,
    QObject,
    QtMsgType,
    Signal,
    qInstallMessageHandler,
)

from src.core import config
from src.core.category_discovery import CategoryDiscovery


@dataclass(frozen=True)
class LogRecord:
    """Store one application log message."""

    level: str
    category: str
    message: str
    formatted: str


class LoggingManager(QObject):
    """Manage Qt logging categories, message delivery, buffering, and configured outputs."""

    message_logged = Signal(str, str, str, str)

    def __init__(self, parent=None):
        """Initialize the logging manager.

        Parameters
        ----------
        parent : QObject, optional
            Parent object for the manager."""
        super().__init__(parent)
        self._lock = Lock()
        self._records = deque(maxlen=config.LOG_MAX_RECORDS)
        self._previous_handler = None
        self._gui_enabled = (
            config.LOG_OUTPUT_GUI in config.LOG_OUTPUTS and config.LOG_GUI_ENABLED
        )
        # Discover categories automatically from source code only
        self._discovered_categories = set(CategoryDiscovery.discover_from_source())

        self._apply_filter_rules()
        self._configure_file()
        self._previous_handler = qInstallMessageHandler(self._handle_message)

    def close(self):
        """Restore Qt's previous message handler.

        No persistent file handle needs releasing: the log file is opened,
        written, and closed independently for every message (see
        ``_handle_message``)."""
        qInstallMessageHandler(self._previous_handler)
        self._previous_handler = None

    def set_gui_enabled(self, enabled: bool):
        """Enable or disable delivery of messages to GUI consumers.

        Parameters
        ----------
        enabled : bool
            Whether GUI log delivery should be enabled."""
        self._gui_enabled = enabled

    @property
    def gui_enabled(self) -> bool:
        """Return whether GUI logging is currently enabled.

        Returns
        -------
        bool
            ``True`` when GUI delivery is enabled; otherwise ``False``."""
        return self._gui_enabled

    def categories(self) -> tuple[str, ...]:
        """Return the known application logging categories.

        Returns
        -------
        tuple[str, ...]
            Registered application logging category names."""
        # Return only discovered categories (no manual configuration)
        return tuple(self._discovered_categories)

    def records(self, category_prefix: str | None = None) -> tuple[LogRecord, ...]:
        """Return buffered messages, optionally restricted to a category prefix.

        Parameters
        ----------
        prefix : str, optional
            Category prefix used to filter the returned records."""
        with self._lock:
            records = tuple(self._records)
        if category_prefix is None:
            return records
        return tuple(
            record
            for record in records
            if record.category == category_prefix
            or record.category.startswith(f"{category_prefix}.")
        )

    def clear(self):
        """Clear the buffered records and truncate the persisted log file.

        The GUI display is cleared separately by the log view itself
        (``LogsView.clear``); this method only resets the data the view
        would otherwise reload on the next application start."""
        with self._lock:
            self._records.clear()
            if config.LOG_OUTPUT_FILE in config.LOG_OUTPUTS:
                self.log_file_path().write_text("", encoding="utf-8")

    def _apply_filter_rules(self):
        """Apply category and severity rules through Qt's logging system."""
        rules = []
        for category in self._discovered_categories:
            enabled = category in self._discovered_categories
            rules.append(f"{category}.debug={'true' if enabled else 'false'}")
            rules.append(f"{category}.info={'true' if enabled else 'false'}")
            rules.append(f"{category}.warning={'true' if enabled else 'false'}")
            rules.append(f"{category}.critical={'true' if enabled else 'false'}")
        QLoggingCategory.setFilterRules("\n".join(rules))

    def _configure_file(self):
        """Ensure the log directory exists when file output is selected.

        The log file itself is not opened here: it is opened, written to,
        and closed independently for every message (see
        ``_handle_message``), so it is recreated automatically if it is
        deleted while the application is running."""
        if config.LOG_OUTPUT_FILE not in config.LOG_OUTPUTS:
            return
        self.log_file_path().parent.mkdir(parents=True, exist_ok=True)

    @staticmethod
    def log_file_path() -> Path:
        """Return the persistent log file path for the current runtime.

        Returns
        -------
        Path
            Path of the configured persistent log file."""
        if getattr(sys, "frozen", False):
            return config.PROJECT_ROOT / "logs" / config.LOG_FILE_NAME
        return config.LOGS_DIR / config.LOG_FILE_NAME

    def _handle_message(self, message_type, context, message):
        """Handle a message emitted by Qt's logging infrastructure.

        Parameters
        ----------
        message_type : QtMsgType
            Qt message severity.
        context : QMessageLogContext
            Qt logging context for the message.
        message : str
            Raw message text."""
        category = context.category or "default"
        level = self._level_name(message_type)
        timestamp = datetime.now().astimezone().isoformat(timespec="seconds")
        formatted = f"[{timestamp}] [{level}] [{category}] {message}"
        record = LogRecord(level, category, message, formatted)

        with self._lock:
            self._records.append(record)
            if config.LOG_OUTPUT_FILE in config.LOG_OUTPUTS:
                with self.log_file_path().open("a", encoding="utf-8") as file_handle:
                    file_handle.write(formatted + "\n")

        if config.LOG_OUTPUT_CONSOLE in config.LOG_OUTPUTS:
            print(formatted, file=sys.stderr, flush=True)

        if self._gui_enabled and config.LOG_OUTPUT_GUI in config.LOG_OUTPUTS:
            self.message_logged.emit(category, level, message, formatted)

    @staticmethod
    def _level_name(message_type: QtMsgType) -> str:
        """Return a readable name for a Qt message type.

        Parameters
        ----------
        message_type : QtMsgType
            Qt message severity.

        Returns
        -------
        str
            Human-readable severity name."""
        return {
            QtMsgType.QtDebugMsg: "DEBUG",
            QtMsgType.QtInfoMsg: "INFO",
            QtMsgType.QtWarningMsg: "WARNING",
            QtMsgType.QtCriticalMsg: "CRITICAL",
            QtMsgType.QtFatalMsg: "FATAL",
        }.get(message_type, "UNKNOWN")


def category(name: str) -> QLoggingCategory:
    """Return a Qt logging category for the application.

    Parameters
    ----------
    name : str
        Logging category name.

    Returns
    -------
    QLoggingCategory
        Qt logging category associated with the supplied name."""
    return QLoggingCategory(name)
