from PySide6.QtCore import QLoggingCategory, qCInfo

from src.models.home_model import Home_Model
from src.models.logs_model import Logs_Model
from src.models.model import Model
from src.models.settings_model import Settings_Model


def test_home_model_is_a_model(qapp):
    assert isinstance(Home_Model(), Model)


def test_settings_model_is_a_model(qapp):
    assert isinstance(Settings_Model(), Model)


def test_logs_model_records_returns_buffered_records(qapp, logging_manager):
    qCInfo(QLoggingCategory("skeleton.core.application"), "buffered message")
    model = Logs_Model(logging_manager)

    messages = [record.message for record in model.records()]
    assert "buffered message" in messages


def test_logs_model_file_lines_returns_empty_tuple_without_a_log_file(
    qapp, logging_manager
):
    model = Logs_Model(logging_manager)
    assert model.file_lines() == ()


def test_logs_model_file_lines_reads_the_persisted_file(
    qapp, logging_manager_with_file
):
    qCInfo(QLoggingCategory("skeleton.core.application"), "persisted line")
    model = Logs_Model(logging_manager_with_file)

    lines = model.file_lines()
    assert any("persisted line" in line for line in lines)


def test_logs_model_clear_delegates_to_the_logging_manager(qapp, logging_manager):
    qCInfo(QLoggingCategory("skeleton.core.application"), "to be cleared")
    model = Logs_Model(logging_manager)
    assert model.records()

    model.clear()

    assert model.records() == ()
