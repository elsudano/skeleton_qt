from PySide6.QtCore import QEvent
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
        self.bind_text(self, lambda: self.tr(config.WINDOW_TITLE), "setWindowTitle")
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

    def create_menu(self, menu):
        """Create and register an application menu.

        Parameters
        ----------
        menu : dict
            Menu definition: internal ``name`` and untranslated ``title``.
        """
        title = menu["title"]
        m = self.menuBar().addMenu("")
        self._menu_registry[menu["name"]] = m
        self.bind_text(m, lambda: self.tr(title), "setTitle")

    def add_action(self, menu_name: str, action):
        """Add an action to a registered menu.

        Parameters
        ----------
        menu_name : str
            Internal menu name.
        action : QAction
            Action to add, created with its untranslated text.

        Raises
        ------
        KeyError
            If the menu does not exist.
        """
        self._menu_registry[menu_name].addAction(action)
        source_text = action.text()
        self.bind_text(action, lambda: self.tr(source_text))

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
    def navigation_container(self):
        """Return the navigation container.

        Returns
        -------
        QStackedWidget
            Navigation container.
        """
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
