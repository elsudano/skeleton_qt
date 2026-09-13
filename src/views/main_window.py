from PySide6.QtWidgets import QMainWindow, QStackedWidget
from src.core.config import WINDOW_HEIGHT, WINDOW_WIDTH

class MainWindow(QMainWindow):
    """Main application window.

    Provides the permanent application window and the navigation container
    used to display application views.
    """

    def __init__(self):
        """Initialize the main application window."""
        super().__init__()
        self._stacked_widget = QStackedWidget()
        self._setup_window()
        self._setup_central_widget()

    def _setup_window(self):
        """Configure the main window properties."""
        self.setWindowTitle(self.tr("Skeleton Qt"))
        self.resize(WINDOW_WIDTH, WINDOW_HEIGHT)

    def _setup_central_widget(self):
        """Configure the central widget used for application navigation."""
        self.setCentralWidget(self._stacked_widget)

    def add_view(self, view):
        """Add a view to the navigation container.

        Parameters
        ----------
        view : QWidget
            View to add to the application.
        """
        self._stacked_widget.addWidget(view)

    def show_view(self, view):
        """Display a view in the navigation container.

        Parameters
        ----------
        view : QWidget
            View to display.
        """
        self._stacked_widget.setCurrentWidget(view)