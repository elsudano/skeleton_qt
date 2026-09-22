"""Main application window."""
from PySide6.QtCore import QEvent
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QMainWindow, QStackedWidget
from src.core import config
from src.core.text_binder import TextBinder

class MainWindow(QMainWindow):
    """Main application window."""

    def __init__(self):
        """Initialize the main window."""
        super().__init__()
        self._menu_registry = {}
        self._texts = TextBinder()
        self._setup_window()

    def _setup_window(self):
        """Configure the main window."""
        self.bind_text(self, lambda: self.tr("Skeleton Qt"), "setWindowTitle")
        self.setWindowIcon(QIcon(str(config.ASSETS_DIR / "icon.ico")))
        self.resize(config.WINDOW_WIDTH, config.WINDOW_HEIGHT)
        self._navigation_container = QStackedWidget()
        self.setCentralWidget(self._navigation_container)

    def bind_text(self, widget, source, setter: str = "setText"):
        """Show a text and keep it in sync with the active language.

        Parameters
        ----------
        widget : QObject
            Widget, action or window that displays the text.
        source : callable or str
            Callable returning the text (``lambda: self.tr("Exit")``).
            A plain ``str`` is applied as-is and never re-translated.
        setter : str, optional
            Name of the widget method that receives the text.

        Returns
        -------
        QObject
            The same widget.
        """
        return self._texts.bind(widget, source, setter)

    def create_menu(self, name: str, title_source):
        """Create and register an application menu.

        Parameters
        ----------
        name : str
            Internal menu name used with :meth:`add_action`.
        title_source : callable or str
            Callable returning the untranslated menu title
            (``lambda: self.tr("&File")``) or a plain string.
        """
        menu = self.menuBar().addMenu("")
        self._menu_registry[name] = menu
        self.bind_text(menu, title_source, "setTitle")

    def add_action(self, menu_name: str, action, text_source=None):
        """Add an action to a registered menu.

        Parameters
        ----------
        menu_name : str
            Internal menu name.
        action : QAction
            Action to add.
        text_source : callable, optional
            Callable returning the action text (``lambda: self.tr("&Exit")``).
            When omitted, the action keeps the text it was created with.

        Raises
        ------
        KeyError
            If the menu does not exist.
        """
        self._menu_registry[menu_name].addAction(action)
        if text_source is not None:
            self.bind_text(action, text_source)

    def add_separator(self, menu_name: str):
        """Add a separator to a registered menu.

        Parameters
        ----------
        menu_name : str
            Internal menu name.

        Raises
        ------
        KeyError
            If the menu does not exist.
        """
        self._menu_registry[menu_name].addSeparator()

    @property
    def navigation_container(self) -> QStackedWidget:
        """Return the navigation container."""
        return self._navigation_container

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
