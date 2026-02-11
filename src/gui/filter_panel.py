"""Filter panel for experiment display."""

import tkinter as tk
from tkinter import ttk
from typing import Callable, Optional

from models.science_database import ScienceDatabase
from utils.config import SHOW_OPTIONS, GROUP_BY_OPTIONS


class FilterPanel(ttk.Frame):
    """Widget for filtering and grouping experiments."""

    def __init__(self, parent, science_db: ScienceDatabase,
                 on_filter_changed: Callable):
        """
        Initialize filter panel.

        Args:
            parent: Parent widget
            science_db: Science database for filter options
            on_filter_changed: Callback when filters change
        """
        super().__init__(parent)
        self.science_db = science_db
        self.on_filter_changed = on_filter_changed

        self._build_ui()

    def _build_ui(self):
        """Build the filter panel UI."""
        # Filter frame
        filter_frame = ttk.LabelFrame(self, text="Filters", padding=10)
        filter_frame.pack(fill=tk.X, padx=5, pady=5)

        # Body filter
        ttk.Label(filter_frame, text="Body:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.body_var = tk.StringVar(value="All")
        body_values = ["All"] + self.science_db.get_body_names()
        self.body_combo = ttk.Combobox(
            filter_frame,
            textvariable=self.body_var,
            values=body_values,
            state='readonly',
            width=20
        )
        self.body_combo.grid(row=0, column=1, sticky=tk.W, padx=5, pady=5)
        self.body_combo.bind('<<ComboboxSelected>>', lambda e: self.on_filter_changed())

        # Experiment type filter
        ttk.Label(filter_frame, text="Experiment:").grid(row=0, column=2, sticky=tk.W, padx=5, pady=5)
        self.experiment_var = tk.StringVar(value="All")
        exp_values = ["All"] + [name for _, name in self.science_db.get_experiment_types()]
        self.experiment_combo = ttk.Combobox(
            filter_frame,
            textvariable=self.experiment_var,
            values=exp_values,
            state='readonly',
            width=25
        )
        self.experiment_combo.grid(row=0, column=3, sticky=tk.W, padx=5, pady=5)
        self.experiment_combo.bind('<<ComboboxSelected>>', lambda e: self.on_filter_changed())

        # Show options
        ttk.Label(filter_frame, text="Show:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        self.show_var = tk.StringVar(value=SHOW_OPTIONS[0])
        self.show_combo = ttk.Combobox(
            filter_frame,
            textvariable=self.show_var,
            values=SHOW_OPTIONS,
            state='readonly',
            width=20
        )
        self.show_combo.grid(row=1, column=1, sticky=tk.W, padx=5, pady=5)
        self.show_combo.bind('<<ComboboxSelected>>', lambda e: self.on_filter_changed())

        # Group by options
        ttk.Label(filter_frame, text="Group By:").grid(row=1, column=2, sticky=tk.W, padx=5, pady=5)
        self.group_by_var = tk.StringVar(value=GROUP_BY_OPTIONS[0])
        self.group_by_combo = ttk.Combobox(
            filter_frame,
            textvariable=self.group_by_var,
            values=GROUP_BY_OPTIONS,
            state='readonly',
            width=20
        )
        self.group_by_combo.grid(row=1, column=3, sticky=tk.W, padx=5, pady=5)
        self.group_by_combo.bind('<<ComboboxSelected>>', lambda e: self.on_filter_changed())

    def get_selected_body(self) -> Optional[str]:
        """Get selected body filter (None if 'All')."""
        body = self.body_var.get()
        return body if body != "All" else None

    def get_selected_experiment(self) -> Optional[str]:
        """Get selected experiment filter (None if 'All')."""
        exp_name = self.experiment_var.get()
        if exp_name == "All":
            return None

        # Convert display name back to experiment ID
        for exp_id, name in self.science_db.get_experiment_types():
            if name == exp_name:
                return exp_id
        return None

    def get_show_mode(self) -> str:
        """Get show mode ('Available Only' or 'All Experiments')."""
        return self.show_var.get()

    def get_group_by(self) -> str:
        """Get grouping mode ('Body', 'Experiment', or 'Situation')."""
        return self.group_by_var.get()
