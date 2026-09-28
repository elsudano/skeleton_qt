"""Model exposing buffered and persisted application log records."""

from src.core import config
from src.core.logging import LoggingManager, LogRecord
from src.models.model import Model


class LogsModel(Model):
    """Provide buffered and persisted log records to the global log view."""

    def __init__(self, logging_manager: LoggingManager):
        """Initialize the log model.

        Parameters
        ----------
        logging_manager : LoggingManager
            Central logging manager providing buffered records and log file access."""
        self._logging_manager = logging_manager

    def records(self) -> tuple[LogRecord, ...]:
        """Return the buffered log records.

        Returns
        -------
        tuple[LogRecord, ...]
            Buffered log records in chronological order."""
        return self._logging_manager.records()

    def file_lines(self) -> tuple[str, ...]:
        """Return the last persisted log lines when a log file exists.

        Returns
        -------
        tuple[str, ...]
            Persisted log lines, or an empty tuple when no log file is available."""
        log_file = self._logging_manager.log_file_path()
        if not log_file.exists():
            return ()
        lines = log_file.read_text(encoding="utf-8").splitlines()
        return tuple(lines[-config.LOG_MAX_RECORDS:])
