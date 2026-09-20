from PySide6.QtCore import QEvent
from PySide6.QtWidgets import QMainWindow, QStackedWidget
from src.core import config

class MainWindow(QMainWindow):
    """Main application window."""

    def __init__(self):
        """Initialize the main window."""
        super().__init__()
        self._menu_registry = {}
        self._translatable = []
        self._setup_window()

    def _setup_window(self):
        """Configure the main window."""
        self.resize(config.WINDOW_WIDTH, config.WINDOW_HEIGHT)
        self._navigation_container = QStackedWidget()
        self.setCentralWidget(self._navigation_container)
        self.retranslate_ui()

    def create_menu(self, menu):
        """Create and register application menus.

        Parameters
        ----------
        menus : tuple of tuple
            Menu definitions containing the internal name and translated title.
        """
        m = self.menuBar().addMenu("")
        self._menu_registry[menu["name"]] = m
        self._register_translatable(m.setTitle, menu["title"])

    def add_action(self, menu_name: str, action):
        """Add an action to a registered menu.

        Parameters
        ----------
        menu_name : str
            Internal menu name.
        action : QAction
            Action to add.

        Raises
        ------
        KeyError
            If the menu does not exist.
        """
        self._menu_registry[menu_name].addAction(action)
        self._register_translatable(action.setText, action.text())

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

    def _register_translatable(self, setter, source_text: str):
        """Remember the source text and apply its current translation.

        Parameters
        ----------
        setter : str
            This will be the text that we want to translate.
        source_text : str
            this is the text that want to set in translation.
        """
        self._translatable.append((setter, source_text))
        setter(self.tr(source_text))

    def retranslate_ui(self):
        """Apply window title and menu texts in the current language."""
        self.setWindowTitle(self.tr(config.WINDOW_TITLE))
        for setter, source_text in self._translatable:
            setter(self.tr(source_text))

    def changeEvent(self, event):
        """React to language changes."""
        if event.type() == QEvent.Type.LanguageChange:
            self.retranslate_ui()
        super().changeEvent(event)

    @property
    def navigation_container(self):
        """Return the navigation container.

        Returns
        -------
        QStackedWidget
            Navigation container.
        """
        return self._navigation_container