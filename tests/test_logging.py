from PySide6.QtCore import QLoggingCategory, qCInfo


def test_logging_manager_captures_messages(qtbot, logging_manager):
    received = []
    logging_manager.message_logged.connect(lambda *args: received.append(args))

    category = QLoggingCategory("skeleton.core.application")
    qCInfo(category, "test message")

    assert any(message[2] == "test message" for message in received)


def test_records_are_buffered(qtbot, logging_manager):
    qCInfo(QLoggingCategory("skeleton.core.application"), "buffered message")

    messages = [record.message for record in logging_manager.records()]
    assert "buffered message" in messages


def test_records_can_be_filtered_by_category_prefix(qtbot, logging_manager):
    qCInfo(QLoggingCategory("skeleton.controller"), "controller message")
    qCInfo(QLoggingCategory("skeleton.view.home"), "view message")

    controller_messages = [
        record.message for record in logging_manager.records("skeleton.controller")
    ]

    assert "controller message" in controller_messages
    assert "view message" not in controller_messages


def test_clear_empties_the_buffered_records(qtbot, logging_manager):
    qCInfo(QLoggingCategory("skeleton.core.application"), "to be cleared")
    assert logging_manager.records()

    logging_manager.clear()

    assert logging_manager.records() == ()


def test_clear_truncates_the_persisted_log_file(qtbot, logging_manager_with_file):
    qCInfo(QLoggingCategory("skeleton.core.application"), "persisted line")
    log_file = logging_manager_with_file.log_file_path()
    assert log_file.read_text(encoding="utf-8") != ""

    logging_manager_with_file.clear()

    assert log_file.read_text(encoding="utf-8") == ""


def test_log_file_is_recreated_after_being_deleted_while_running(
    qtbot, logging_manager_with_file
):
    # Regression test: the log file used to be opened once at startup and
    # kept open for the whole run, so deleting it while the app was still
    # running meant it never came back until a full restart.
    qCInfo(QLoggingCategory("skeleton.core.application"), "first line")
    log_file = logging_manager_with_file.log_file_path()
    assert log_file.exists()

    log_file.unlink()
    assert not log_file.exists()

    qCInfo(QLoggingCategory("skeleton.core.application"), "second line")

    assert log_file.exists()
    assert "second line" in log_file.read_text(encoding="utf-8")


def test_set_categories_filters_future_messages(qtbot, logging_manager):
    logging_manager.set_categories({"skeleton.controller"})

    qCInfo(QLoggingCategory("skeleton.core.application"), "should be filtered out")
    qCInfo(QLoggingCategory("skeleton.controller"), "should pass through")

    messages = [record.message for record in logging_manager.records()]
    assert "should be filtered out" not in messages
    assert "should pass through" in messages


def test_set_gui_enabled_gates_the_message_signal(qtbot, logging_manager):
    received = []
    logging_manager.message_logged.connect(lambda *args: received.append(args))

    logging_manager.set_gui_enabled(False)
    qCInfo(QLoggingCategory("skeleton.core.application"), "should not reach gui")
    assert received == []

    logging_manager.set_gui_enabled(True)
    qCInfo(QLoggingCategory("skeleton.core.application"), "should reach gui")
    assert any(message[2] == "should reach gui" for message in received)
