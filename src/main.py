"""Main entry point for KSP Science Tracker."""

import sys
from gui.main_window import MainWindow


def main():
    """Launch the application."""
    app = MainWindow()
    app.run()


if __name__ == "__main__":
    main()
