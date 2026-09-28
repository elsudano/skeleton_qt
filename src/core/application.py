"""Application composition, configuration, and startup."""

from PySide6.QtCore import QLoggingCategory, QObject, QTranslator, qCInfo
from PySide6.QtGui import QAction

from src.controllers.controller import Controller
from src.core import config
from src.core.logging import LoggingManager
from src.core.main_window import MainWindow
from src.views.views import Views


class Application(QObject):
    """Compose and start the Qt application."""

    _log = QLoggingCategory("skeleton.core.application")

    def __init__(self, qt_application):
        """Initialize the application.

        Parameters
        ----------
        qt_application : QApplication
            Qt application instance used by the application."""
        super().__init__()
        self._qt_application = qt_application
        self._translator = None
        self._language = config.DEFAULT_LANGUAGE
        self._logging_manager = LoggingManager()
        self._qt_application.aboutToQuit.connect(self._logging_manager.close)
        self._main_window = MainWindow()
        self._controller = Controller(
            self._main_window.navigation_container,
            self._logging_manager,
        )
        self._load_translation(self._language)
        self._setup_menus()
        qCInfo(self._log, self.tr("Application initialized"))
        self._controller.navigate(Views.HOME)

    @property
    def language(self) -> str:
        """Return the active language code.

        Returns
        -------
        str
            Active language code."""
        return self._language

    def _load_translation(self, language: str = None):
        """Load and install a translation.

        Parameters
        ----------
        language : str
            Language code used to locate the translation source."""
        language = language or config.DEFAULT_LANGUAGE
        translation_file = config.TRANSLATIONS_DIR / f"skeleton_{language}.qm"
        translator = QTranslator()
        if not translator.load(str(translation_file)):
            return
        if self._translator is not None:
            self._qt_application.removeTranslator(self._translator)
        self._qt_application.installTranslator(translator)
        self._translator = translator
        self._language = language
        qCInfo(self._log, self.tr("The Language was changed"))

    def _setup_menus(self):
        """Create application menus and actions."""
        menu_definitions = (
            ("file", lambda: self.tr("&File")),
            ("edit", lambda: self.tr("&Edit")),
            ("tools", lambda: self.tr("&Tools")),
            ("options", lambda: self.tr("&Options")),
            ("help", lambda: self.tr("&Help")),
        )
        for name, title in menu_definitions:
            self._main_window.create_menu(name, title)

        action_definitions = (
            (lambda: self.tr("&Home"), "file",
             lambda: self._controller.navigate(Views.HOME)),
            ("separator", "file", None),
            (lambda: self.tr("E&xit"), "file",
             self._qt_application.quit),
            (lambda: self.tr("Cu&t"), "edit", lambda: None),
            (lambda: self.tr("&Copy"), "edit", lambda: None),
            (lambda: self.tr("&Paste"), "edit", lambda: None),
            (lambda: self.tr("&Video Uploader"), "tools",
             lambda: self._controller.navigate(Views.VIDEO_UPLOADER)),
            (lambda: self.tr("&Route Designer"), "tools",
             lambda: self._controller.navigate(Views.ROUTE_DESIGNER)),
            (lambda: self.tr("&Settings"), "tools",
             lambda: self._controller.navigate(Views.SETTINGS)),
            (lambda: self.tr("&Logs"), "tools",
             lambda: self._controller.navigate(Views.LOGS)),
            (lambda: self.tr("&Spain"), "options",
             lambda: self._load_translation("es_ES")),
            (lambda: self.tr("&English"), "options",
             lambda: self._load_translation("en_US")),
            ("separator", "options", None),
            (lambda: self.tr("&Configuration"), "options",
             lambda: self._controller.navigate(Views.SETTINGS)),
            (lambda: self.tr("&About"), "help",
             lambda: self._controller.navigate(Views.HOME)),
        )
        for title_source, menu_name, callback in action_definitions:
            if title_source == "separator":
                self._main_window.add_separator(menu_name)
            else:
                action = QAction(title_source(), self._main_window)
                action.triggered.connect(callback)
                self._main_window.add_action(menu_name, action, title_source)

    def start(self):
        """Show the application window and start the application lifecycle."""
        self._main_window.show()
