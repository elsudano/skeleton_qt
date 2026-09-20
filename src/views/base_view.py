from PySide6.QtCore import QEvent, Signal
from PySide6.QtWidgets import QWidget
from src.core.text_binder import TextBinder

class BaseView(QWidget):
    """Base class for application views."""

    navigation_requested = Signal(str)

    def __init__(self, parent=None):
        """Initialize the view.

        Parameters
        ----------
        parent : QWidget, optional
            Parent widget.
        """
        super().__init__(parent)
        self._texts = TextBinder()

    def request_navigation(self, name: str):
        """Request navigation to another view.

        Parameters
        ----------
        name : str
            View identifier.
        """
        self.navigation_requested.emit(name)

    def bind_text(self, widget, source, setter: str = "setText"):
        """Show a text and keep it in sync with the active language.

        Parameters
        ----------
        widget : QObject
            Widget that displays the text.
        source : callable or str
            Callable returning the text (``lambda: self.tr("Back")`` or a model
            getter). A plain ``str`` is applied as-is and never re-translated.
        setter : str, optional
            Name of the widget method that receives the text.

        Returns
        -------
        QObject
            The same widget, so it can be created and bound in one line.
        """
        return self._texts.bind(widget, source, setter)

    def changeEvent(self, event):
        """Re-apply the bound texts when Qt reports a language change.

        Parameters
        ----------
        event : QEvent
            Change event sent by Qt.
        """
        if event.type() == QEvent.Type.LanguageChange:
            self._texts.refresh()
        super().changeEvent(event)
