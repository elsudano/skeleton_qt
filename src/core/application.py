from PySide6.QtCore import QTranslator
from PySide6.QtGui import QAction
from src.controllers.controller import Controller
from src.core import config
from src.core.main_window import MainWindow
from src.views.views import Views

class Application:
    """Compose and start the application."""

    _MENU_DEFINITIONS = (
        ("file", "&File"),
        ("views", "&Views"),
    )

    _ACTION_DEFINITIONS = (
        ("&Exit", "file", "exit"),
        ("&Home", "views", "home"),
        ("&Settings", "views", "settings"),
    )

    def __init__(self, qt_application):
        """Initialize the application.

        Parameters
        ----------
        qt_application : QApplication
            Qt application instance.
        """
        self._qt_application = qt_application
        self._translator = QTranslator()
        self._load_translation()
        self._main_window = MainWindow()
        self._controller = Controller(
            self._main_window.navigation_container
        )
        self._setup_menus()
        self._controller.navigate(Views.HOME)

    def _load_translation(self):
        """Load and install the configured translation, if available."""
        translation_file = (
            config.TRANSLATIONS_DIR
            / f"skeleton_{config.DEFAULT_LANGUAGE}.qm"
        )

        if self._translator.load(str(translation_file)):
            self._qt_application.installTranslator(self._translator)

    def _setup_menus(self):
        """Create menus and configure their actions."""
        menus = (
            ("file", self._main_window.tr("&File")),
            ("views", self._main_window.tr("&Views")),
        )
        self._main_window.create_menus(menus)

        translated_titles = {
            "&Exit": self._main_window.tr("&Exit"),
            "&Home": self._main_window.tr("&Home"),
            "&Settings": self._main_window.tr("&Settings"),
        }
        callbacks = {
            "exit": self._qt_application.quit,
            "home": lambda: self._controller.navigate(Views.HOME),
            "settings": lambda: self._controller.navigate(Views.SETTINGS),
        }

        for title, menu_name, callback_name in self._ACTION_DEFINITIONS:
            action = QAction(
                translated_titles[title],
                self._main_window,
            )
            action.triggered.connect(callbacks[callback_name])
            self._main_window.add_action(menu_name, action)

    def start(self):
        """Show the application window."""
        self._main_window.show()