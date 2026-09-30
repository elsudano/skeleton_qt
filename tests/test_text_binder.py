import shiboken6
from PySide6.QtWidgets import QLabel

from src.core.text_binder import TextBinder


def test_bind_applies_plain_text(qtbot):
    label = QLabel()
    qtbot.addWidget(label)
    binder = TextBinder()
    binder.bind(label, "Hello")
    assert label.text() == "Hello"


def test_bind_applies_callable_result(qtbot):
    label = QLabel()
    qtbot.addWidget(label)
    binder = TextBinder()
    binder.bind(label, lambda: "Hi")
    assert label.text() == "Hi"


def test_refresh_re_evaluates_sources(qtbot):
    label = QLabel()
    qtbot.addWidget(label)
    binder = TextBinder()
    state = {"text": "one"}
    binder.bind(label, lambda: state["text"])
    state["text"] = "two"
    binder.refresh()
    assert label.text() == "two"


def test_bind_replaces_previous_source(qtbot):
    label = QLabel()
    qtbot.addWidget(label)
    binder = TextBinder()
    binder.bind(label, "first")
    binder.bind(label, "second")
    assert label.text() == "second"
    assert len(binder._bindings) == 1


def test_refresh_drops_bindings_for_destroyed_widgets(qtbot):
    # The widget is deliberately destroyed here (and not handed to qtbot,
    # which would try to close it again during teardown) to reproduce the
    # "already deleted" case that refresh() guards against.
    label = QLabel()
    binder = TextBinder()
    binder.bind(label, "Hello")
    assert len(binder._bindings) == 1

    shiboken6.delete(label)
    binder.refresh()

    assert len(binder._bindings) == 0
