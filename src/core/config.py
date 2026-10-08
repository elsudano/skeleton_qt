"""Application configuration constants.

  Attributes
  ----------
  PROJECT_ROOT : Path
      The root directory of the project.
  RESOURCES_DIR : Path
      The directory containing all application resources.
  ASSETS_DIR : Path
      The directory for images and icons.
  TRANSLATIONS_DIR : Path
      The directory for translation files.
  STYLES_DIR : Path
      The directory for Qt Style Sheets (.qss).
  LOGS_DIR : Path
      The directory where log files are stored.
  LOG_FILE_NAME : str
      The name of the log file.
  WINDOW_WIDTH : int
      The default width of the main window.
  WINDOW_HEIGHT : int
      The default height of the main window.
  DEFAULT_LANGUAGE : str
      The default language code (e.g., 'es_ES').
  DEFAULT_THEME : str
      The default theme name (e.g., 'light').
  BUTTON_MINIMUM_HEIGHT_SIZE : int
      The minimum height for buttons in pixels.
  BUTTON_MINIMUM_WIDTH_SIZE : int
      The minimum width for buttons in pixels.
  LOG_OUTPUT_CONSOLE : str
      Identifier for console output.
  LOG_OUTPUT_FILE : str
      Identifier for file output.
  LOG_OUTPUT_GUI : str
      Identifier for GUI output.
  LOG_OUTPUTS : tuple[str, ...]
      Tuple of all enabled output identifiers.
  LOG_GUI_ENABLED : bool
      Flag to enable/disable GUI logging.
  LOG_MAX_RECORDS : int
      Maximum number of log records to keep in memory.
  LOG_CATEGORIES : tuple[str, ...]
      List of registered logging categories.
  """

import os
import sys
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

