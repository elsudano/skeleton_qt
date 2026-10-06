"""Application configuration constants."""
import os, sys

from pathlib import Path

PROJECT_ROOT = ""

if getattr(sys, 'frozen', False):
    # Binary environment: We are using the binary folder
    PROJECT_ROOT = os.path.dirname(sys.executable)
    PROJECT_ROOT = Path(PROJECT_ROOT).resolve()
else:
    # Normal Python environment: take the folder where we have the script
    PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
    PROJECT_ROOT = Path(PROJECT_ROOT).resolve().parents[1]

RESOURCES_DIR = PROJECT_ROOT / "resources"
ASSETS_DIR = RESOURCES_DIR / "assets"
TRANSLATIONS_DIR = RESOURCES_DIR / "translations"
STYLES_DIR = RESOURCES_DIR / "styles"
LOGS_DIR = PROJECT_ROOT / "logs"
LOG_FILE_NAME = "skeleton_qt.log"

# Application
WINDOW_WIDTH = 640
WINDOW_HEIGHT = 480
DEFAULT_LANGUAGE = "es_ES"
DEFAULT_THEME = "light"
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
    "skeleton.controllers.controller",
    "skeleton.core.application",
    "skeleton.core.main_window",
    "skeleton.core.text_binder",
    "skeleton.view.base_view",
    "skeleton.view.home",
    "skeleton.view.video_uploader",
    "skeleton.view.route_designer",
    "skeleton.view.settings",
    "skeleton.view.logs_view",
    "skeleton.model.home",
    "skeleton.model.video_uploader",
    "skeleton.model.route_designer",
    "skeleton.model.settings",
)
