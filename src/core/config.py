from pathlib import Path

# Directory Variables
PROJECT_ROOT = Path(__file__).resolve().parents[2]
RESOURCES_DIR = PROJECT_ROOT / "resources"
ASSETS_DIR = RESOURCES_DIR / "assets"
TRANSLATIONS_DIR = RESOURCES_DIR / "translations"

# Basic Configuration
WINDOW_TITLE = "Skeleton Qt"
WINDOW_WIDTH = 240
WINDOW_HEIGHT = 165
DEFAULT_LANGUAGE = "es_ES"