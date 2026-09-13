import sys
from PySide6.QtWidgets import QApplication
from src.controllers.home_controller import HomeController
from src.models.home_model import HomeModel
from src.views.home_view import HomeView
from src.views.main_window import MainWindow


def main():
    """Start the application."""
    app = QApplication(sys.argv)
    window = MainWindow()
    home_view = HomeView()
    home_model = HomeModel()
    home_controller = HomeController(view=home_view, model=home_model,)
    window.add_view(home_view)
    window.show_view(home_view)
    window.show()
    return app.exec()

if __name__ == "__main__":
    sys.exit(main())