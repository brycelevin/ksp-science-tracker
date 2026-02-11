"""Configuration constants for the application."""

import os
from pathlib import Path

# Application info
APP_NAME = "KSP Science Tracker"
APP_VERSION = "1.0.0"

# Default KSP paths for Windows
DEFAULT_KSP_PATHS = [
    r"C:\Program Files (x86)\Steam\steamapps\common\Kerbal Space Program",
    r"C:\Program Files\Steam\steamapps\common\Kerbal Space Program",
    os.path.expanduser(r"~\Documents\Kerbal Space Program"),
]

# Window configuration
WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 700
WINDOW_MIN_WIDTH = 800
WINDOW_MIN_HEIGHT = 600

# Data directory (relative to project root)
PROJECT_ROOT = Path(__file__).parent.parent.parent
DATA_DIR = PROJECT_ROOT / "data"

# UI Configuration
TREE_COLUMN_WIDTH_NAME = 500
TREE_COLUMN_WIDTH_SCIENCE = 150

# Filter options
SHOW_OPTIONS = ["Available Only", "All Experiments"]
GROUP_BY_OPTIONS = ["Body", "Experiment", "Situation"]
