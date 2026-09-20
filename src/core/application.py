from PySide6.QtCore import QTranslator
from PySide6.QtGui import QAction
from src.controllers.controller import Controller
from src.core import config
from src.core.main_window import MainWindow
from src.views.views import Views

class Application:
    """Compose and start the application."""

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

    def _load_translation(self, language: str = None):
        """Load and install a translation. Qt notifies every widget (LanguageChange)."""
        language = language or config.DEFAULT_LANGUAGE
        translation_file = config.TRANSLATIONS_DIR / f"skeleton_{language}.qm"
        translator = QTranslator()
        if not translator.load(str(translation_file)):
            return
        self._qt_application.removeTranslator(self._translator)
        self._qt_application.installTranslator(translator)
        self._translator = translator
        config.DEFAULT_LANGUAGE = language

    def _setup_menus(self):
        """Create menus and configure their actions."""

        _menu_definitions = (
            {"name":"file", "title":"&File"},
            {"name":"views", "title":"&Views"},
            {"name":"languages", "title":"&Languages"},
        )

        _action_definitions = (
            {"title":"&Exit", "menu_name":"file", "callback": self._qt_application.quit},
            {"title":"&Home", "menu_name":"views", "callback": lambda: self._controller.navigate(Views.HOME)},
            {"title":"&Settings", "menu_name":"views", "callback": lambda: self._controller.navigate(Views.SETTINGS)},
            {"title":"&Spain", "menu_name":"languages", "callback": lambda: self._load_translation("es_ES")},
            {"title":"&English", "menu_name":"languages", "callback": lambda: self._load_translation("en_US")},
        )

        for menu in _menu_definitions:
            self._main_window.create_menu(menu)

        for menu_action in _action_definitions:
            action = QAction(menu_action["title"], self._main_window,)
            action.triggered.connect(menu_action["callback"])
            self._main_window.add_action(menu_action["menu_name"], action)

    def start(self):
        """Show the application window."""
        self._main_window.show()