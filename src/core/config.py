"""Application configuration constants."""

from pathlib import Path

# Folders
PROJECT_ROOT = Path(__file__).resolve().parents[2]
RESOURCES_DIR = PROJECT_ROOT / "resources"
ASSETS_DIR = RESOURCES_DIR / "assets"
TRANSLATIONS_DIR = RESOURCES_DIR / "translations"
LOGS_DIR = PROJECT_ROOT / "logs"

LOG_FILE_NAME = "skeleton_qt.log"

# Application
WINDOW_WIDTH = 640
WINDOW_HEIGHT = 480
DEFAULT_LANGUAGE = "es_ES"
BUTTON_MINIMUM_HEIGHT_SIZE = 50
BUTTON_MINIMUM_WIDTH_SIZE = 100

# Logs
LOG_OUTPUT_CONSOLE = "console"
LOG_OUTPUT_FILE = "file"
LOG_OUTPUT_GUI = "gui"
LOG_OUTPUTS = (LOG_OUTPUT_CONSOLE, LOG_OUTPUT_FILE, LOG_OUTPUT_GUI)
LOG_GUI_ENABLED = True
LOG_MAX_RECORDS = 1000
LOG_CATEGORIES = (
    "skeleton.controller",
    "skeleton.core.application",
    "skeleton.core.main_window",
    "skeleton.core.translator",
    "skeleton.view.home",
    "skeleton.view.settings",
    "skeleton.model.home",
    "skeleton.model.settings",
)
