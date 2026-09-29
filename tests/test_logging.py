from PySide6.QtCore import QLoggingCategory, qCInfo

from src.core import config
from src.core.logging import LoggingManager


def test_logging_manager_captures_messages(qtbot, monkeypatch):
    monkeypatch.setattr(config, "LOG_OUTPUTS", (config.LOG_OUTPUT_GUI,))
    manager = LoggingManager()
    received = []
    manager.message_logged.connect(lambda *args: received.append(args))

    # We need to declare this in this way just to handle the known issue: use-after-free
    # in python, in this case PySide6 when you create a category, PySide6 is creating a buffer
    # and this buffet pointing a different memory directions, for that reason fail.
    _CATEGORY = "skeleton.core.application"
    category = QLoggingCategory(_CATEGORY)
    qCInfo(category, "test message")

    assert any(message[2] == "test message" for message in received)
    manager.close()
