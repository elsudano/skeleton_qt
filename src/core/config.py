from pathlib import Path

# Directory Variables
PROJECT_ROOT = Path(__file__).resolve().parents[2]
RESOURCES_DIR = PROJECT_ROOT / "resources"
TRANSLATIONS_DIR = RESOURCES_DIR / "translations"

# Basic Configuration
APP_NAME = "Skeleton Qt"
WINDOW_WIDTH = 600
WINDOW_HEIGHT = 400
DEFAULT_LANGUAGE = "es"