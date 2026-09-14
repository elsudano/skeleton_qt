import sys
from PySide6.QtWidgets import QApplication
from src.core.application import Application

def main():
    """Start the application."""
    qt_application = QApplication(sys.argv)
    application = Application(qt_application)
    application.start()
    return qt_application.exec()

if __name__ == "__main__":
    sys.exit(main())