from PySide6.QtWidgets import QMainWindow
from src.core.config import WINDOW_HEIGHT, WINDOW_WIDTH

class MainWindow(QMainWindow):
    """Main application window.

    Provides the permanent application window and the navigation container
    used to display application views.
    """

    def __init__(self):
        """Initialize the main application window."""
        super().__init__()
        self._setup_window()

    def _setup_window(self):
        """Configure the main window properties."""
        self.setWindowTitle(self.tr("Skeleton Qt"))
        self.resize(WINDOW_WIDTH, WINDOW_HEIGHT)

    def set_central_widget(self, widget):
        """Set the central application widget.

        Parameters
        ----------
        widget : QWidget
            Widget to use as the central widget.
        """
        self.setCentralWidget(widget)