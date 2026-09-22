"""Application configuration constants.

This module only contains immutable constants. Runtime-mutable state
(e.g. the active language) belongs to the ``Application`` class.
"""

from pathlib import Path

# Directory variables
PROJECT_ROOT = Path(__file__).resolve().parents[2]
RESOURCES_DIR = PROJECT_ROOT / "resources"
ASSETS_DIR = RESOURCES_DIR / "assets"
TRANSLATIONS_DIR = RESOURCES_DIR / "translations"
# Basic configuration
WINDOW_WIDTH = 240
WINDOW_HEIGHT = 165
DEFAULT_LANGUAGE = "es_ES"