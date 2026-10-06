"""Application entry point."""

import sys

from PySide6.QtCore import QCoreApplication
from PySide6.QtWidgets import QApplication

from src.core.application import Application


def main() -> int:
    """Create and start the Qt application.

    Returns
    -------
    int
        Application exit status."""
    QCoreApplication.setOrganizationName("SkeletonQt")
    QCoreApplication.setApplicationName("Skeleton Qt")
    QCoreApplication.setApplicationVersion("0.1.0")
    qt_application = QApplication(sys.argv)
    application = Application(qt_application)
    application.start()
    return qt_application.exec()

if __name__ == "__main__":
    raise SystemExit(main())
