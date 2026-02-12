"""Main application window."""

import tkinter as tk
from tkinter import ttk, messagebox
from typing import Optional, List

from models.science_database import ScienceDatabase
from models.save_data import SaveGameData
from models.experiment import AvailableExperiment
from parsers.sfs_parser import SFSParser
from parsers.science_extractor import ScienceExtractor
from utils.science_calculator import ScienceCalculator
from utils.config import (
    APP_NAME, APP_VERSION,
    WINDOW_WIDTH, WINDOW_HEIGHT,
    WINDOW_MIN_WIDTH, WINDOW_MIN_HEIGHT
)

from .save_selector import SaveSelector
from .filter_panel import FilterPanel
from .experiment_tree import ExperimentTree


class MainWindow:
    """Main application window."""

    def __init__(self):
        """Initialize main window."""
        self.root = tk.Tk()
        self.root.title(f"{APP_NAME} v{APP_VERSION}")
        self.root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        self.root.minsize(WINDOW_MIN_WIDTH, WINDOW_MIN_HEIGHT)

        # Initialize data components
        self.science_db = ScienceDatabase()
        self.calculator = ScienceCalculator(self.science_db)
        self.parser = SFSParser()
        self.extractor = ScienceExtractor()

        # Current state
        self.save_data: Optional[SaveGameData] = None
        self.available_experiments: List[AvailableExperiment] = []

        self._build_ui()
        self._show_welcome()

    def _build_ui(self):
        """Build the main window UI."""
        # Menu bar (optional - placeholder for future features)
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)

        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Exit", command=self.root.quit)

        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About", command=self._show_about)

        # Main container
        main_container = ttk.Frame(self.root)
        main_container.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Statistics bar at bottom (created first so it exists for callbacks)
        stats_frame = ttk.Frame(main_container)
        stats_frame.pack(fill=tk.X, pady=5, side=tk.BOTTOM)

        self.stats_label = ttk.Label(
            stats_frame,
            text="Load a save game to view available science",
            font=("TkDefaultFont", 10, "bold")
        )
        self.stats_label.pack()

        # Save selector at top
        self.save_selector = SaveSelector(main_container, self._on_save_selected)
        self.save_selector.pack(fill=tk.X, side=tk.TOP)

        # Filter panel
        self.filter_panel = FilterPanel(
            main_container,
            self.science_db,
            self._on_filter_changed
        )
        self.filter_panel.pack(fill=tk.X, side=tk.TOP)

        # Experiment tree (main display area)
        tree_frame = ttk.LabelFrame(main_container, text="Available Experiments", padding=5)
        tree_frame.pack(fill=tk.BOTH, expand=True, pady=5, side=tk.TOP)

        self.experiment_tree = ExperimentTree(tree_frame, self.science_db)
        self.experiment_tree.pack(fill=tk.BOTH, expand=True)

    def _show_welcome(self):
        """Show welcome message in tree view."""
        total_experiments = self.science_db.get_total_experiment_count()
        self.stats_label.config(
            text=f"Ready! Database contains {total_experiments:,} possible experiments."
        )

    def _show_about(self):
        """Show about dialog."""
        about_text = (
            f"{APP_NAME} v{APP_VERSION}\n\n"
            "Track completed and available science experiments in Kerbal Space Program.\n\n"
            "Developed for KSP 1 on Windows 10"
        )
        messagebox.showinfo("About", about_text)

    def _on_save_selected(self, save_name: str, save_path: str):
        """
        Handle save game selection.

        Args:
            save_name: Name of the save
            save_path: Path to persistent.sfs file
        """
        try:
            # Parse save file
            self.stats_label.config(text="Loading save file...")
            self.root.update_idletasks()

            parsed_save = self.parser.parse_save_file(save_path)
            self.save_data = self.extractor.extract_science_data(parsed_save, save_name)

            # Calculate available science
            self.available_experiments = self.calculator.calculate_available_science(
                self.save_data
            )

            # Update display
            self._update_display()

            # Update stats
            stats = self.calculator.calculate_statistics(
                self.available_experiments,
                self.save_data
            )

            self.stats_label.config(
                text=(
                    f"Save: {save_name} | "
                    f"Science Earned: {stats['total_earned_science']:.1f} | "
                    f"Available Science: {stats['total_available_science']:.1f} | "
                    f"Completed: {stats['total_completed_experiments']}/{stats['total_possible_experiments']} "
                    f"({stats['completion_percentage']:.1f}%)"
                )
            )

        except FileNotFoundError as e:
            messagebox.showerror("Error", f"Save file not found:\n{e}")
        except ValueError as e:
            messagebox.showerror("Error", f"Failed to parse save file:\n{e}")
        except Exception as e:
            messagebox.showerror("Error", f"Unexpected error:\n{e}")

    def _on_filter_changed(self):
        """Handle filter/grouping changes."""
        if not self.save_data:
            return

        self._update_display()

    def _update_display(self):
        """Update experiment tree based on current filters."""
        # Check if UI components are initialized (may not be during startup)
        if not hasattr(self, 'filter_panel') or not hasattr(self, 'experiment_tree'):
            return

        if not self.available_experiments:
            self.experiment_tree.clear()
            self.stats_label.config(text="No available experiments found!")
            return

        # Apply filters
        filtered_experiments = self._apply_filters(self.available_experiments)

        # Get grouping preference
        group_by = self.filter_panel.get_group_by()

        # Update tree
        self.experiment_tree.populate(filtered_experiments, group_by)

    def _apply_filters(self, experiments: List[AvailableExperiment]) -> List[AvailableExperiment]:
        """
        Apply current filters to experiment list.

        Args:
            experiments: List of all available experiments

        Returns:
            Filtered list of experiments
        """
        filtered = experiments

        # Filter by body
        body_filter = self.filter_panel.get_selected_body()
        if body_filter:
            filtered = [exp for exp in filtered if exp.body_name == body_filter]

        # Filter by experiment type
        exp_filter = self.filter_panel.get_selected_experiment()
        if exp_filter:
            filtered = [exp for exp in filtered
                       if exp.experiment_id.experiment_type == exp_filter]

        # Filter by show mode
        show_mode = self.filter_panel.get_show_mode()
        if show_mode == "Available Only":
            # Already showing only available (not fully completed)
            pass
        # If "All Experiments" is selected in future, would include completed here

        return filtered

    def run(self):
        """Run the application."""
        self.root.mainloop()
