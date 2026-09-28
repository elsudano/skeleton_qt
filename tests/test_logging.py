from PySide6.QtCore import QLoggingCategory, qCInfo

from src.core import config
from src.core.logging import LoggingManager


def test_logging_manager_captures_messages(qtbot, monkeypatch):
    monkeypatch.setattr(config, "LOG_OUTPUTS", (config.LOG_OUTPUT_GUI,))
    manager = LoggingManager()
    received = []
    manager.message_logged.connect(lambda *args: received.append(args))

    category = QLoggingCategory("skeleton.application")
    qCInfo(category, "test message")

    assert any(message[2] == "test message" for message in received)
    manager.close()
