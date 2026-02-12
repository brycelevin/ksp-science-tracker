"""Tree view widget for displaying experiments."""

import tkinter as tk
from tkinter import ttk
from typing import List, Dict, Optional
from collections import defaultdict

from models.experiment import AvailableExperiment
from models.science_database import ScienceDatabase
from utils.config import TREE_COLUMN_WIDTH_NAME, TREE_COLUMN_WIDTH_SCIENCE


class ExperimentTree(ttk.Frame):
    """Tree view for displaying science experiments hierarchically."""

    def __init__(self, parent, science_db: ScienceDatabase):
        """
        Initialize experiment tree.

        Args:
            parent: Parent widget
            science_db: Science database for experiment names
        """
        super().__init__(parent)
        self.science_db = science_db

        self._build_ui()

    def _build_ui(self):
        """Build the tree view UI."""
        # Create tree with scrollbars
        tree_frame = ttk.Frame(self)
        tree_frame.pack(fill=tk.BOTH, expand=True)

        # Scrollbars
        vsb = ttk.Scrollbar(tree_frame, orient="vertical")
        hsb = ttk.Scrollbar(tree_frame, orient="horizontal")

        # Tree view
        self.tree = ttk.Treeview(
            tree_frame,
            columns=("science",),
            yscrollcommand=vsb.set,
            xscrollcommand=hsb.set
        )

        vsb.config(command=self.tree.yview)
        hsb.config(command=self.tree.xview)

        # Layout
        self.tree.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky="ns")
        hsb.grid(row=1, column=0, sticky="ew")

        tree_frame.grid_rowconfigure(0, weight=1)
        tree_frame.grid_columnconfigure(0, weight=1)

        # Configure columns
        self.tree.heading("#0", text="Experiment", anchor=tk.W)
        self.tree.heading("science", text="Science Available", anchor=tk.E)

        self.tree.column("#0", width=TREE_COLUMN_WIDTH_NAME, anchor=tk.W)
        self.tree.column("science", width=TREE_COLUMN_WIDTH_SCIENCE, anchor=tk.E)

    def populate(self, experiments: List[AvailableExperiment], group_by: str):
        """
        Populate tree with experiments.

        Args:
            experiments: List of available experiments
            group_by: Grouping mode ('Body', 'Experiment', or 'Situation')
        """
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)

        if not experiments:
            self.tree.insert("", "end", text="No experiments found", values=("",))
            return

        # Group experiments
        if group_by == "Body":
            self._populate_by_body(experiments)
        elif group_by == "Experiment":
            self._populate_by_experiment(experiments)
        elif group_by == "Situation":
            self._populate_by_situation(experiments)

    def _populate_by_body(self, experiments: List[AvailableExperiment]):
        """Populate tree grouped by celestial body."""
        # Group: Body → Situation → Biome → Experiment
        body_groups = defaultdict(lambda: defaultdict(lambda: defaultdict(list)))

        for exp in experiments:
            exp_id = exp.experiment_id
            body = exp.body_name
            situation = exp_id.situation
            biome = exp_id.biome or "No Biome"

            body_groups[body][situation][biome].append(exp)

        # Build tree
        for body in sorted(body_groups.keys()):
            # Calculate totals for body level
            all_body_exps = [
                exp
                for situation in body_groups[body].values()
                for biome in situation.values()
                for exp in biome
            ]
            body_total = sum(exp.available_science for exp in all_body_exps)
            body_completed = sum(1 for exp in all_body_exps if exp.available_science <= 0.1)
            body_status = self._get_category_status(body_total, len(all_body_exps), body_completed)

            body_node = self.tree.insert(
                "", "end",
                text=f"{body_status} {body}",
                values=(f"{body_total:.1f}",),
                open=False
            )

            for situation in sorted(body_groups[body].keys()):
                # Calculate totals for situation level
                all_situation_exps = [
                    exp
                    for biome in body_groups[body][situation].values()
                    for exp in biome
                ]
                situation_total = sum(exp.available_science for exp in all_situation_exps)
                situation_completed = sum(1 for exp in all_situation_exps if exp.available_science <= 0.1)
                situation_status = self._get_category_status(
                    situation_total, len(all_situation_exps), situation_completed
                )

                situation_node = self.tree.insert(
                    body_node, "end",
                    text=f"{situation_status} {self._format_situation(situation)}",
                    values=(f"{situation_total:.1f}",),
                    open=False
                )

                for biome in sorted(body_groups[body][situation].keys()):
                    biome_exps = body_groups[body][situation][biome]
                    biome_total = sum(exp.available_science for exp in biome_exps)
                    biome_completed = sum(1 for exp in biome_exps if exp.available_science <= 0.1)

                    # Only show biome level if biome exists
                    if biome != "No Biome":
                        biome_status = self._get_category_status(
                            biome_total, len(biome_exps), biome_completed
                        )
                        biome_node = self.tree.insert(
                            situation_node, "end",
                            text=f"{biome_status} {biome}",
                            values=(f"{biome_total:.1f}",),
                            open=False
                        )
                        parent = biome_node
                    else:
                        parent = situation_node

                    # Add individual experiments
                    for exp in sorted(biome_exps, key=lambda e: e.experiment_name):
                        status = self._get_experiment_status(exp)
                        self.tree.insert(
                            parent, "end",
                            text=f"{status} {exp.experiment_name}",
                            values=(f"{exp.available_science:.1f}",)
                        )

    def _populate_by_experiment(self, experiments: List[AvailableExperiment]):
        """Populate tree grouped by experiment type."""
        # Group: Experiment → Body → Situation → Biome
        exp_groups = defaultdict(lambda: defaultdict(lambda: defaultdict(list)))

        for exp in experiments:
            exp_id = exp.experiment_id
            exp_name = exp.experiment_name
            body = exp.body_name
            situation = exp_id.situation

            exp_groups[exp_name][body][situation].append(exp)

        # Build tree
        for exp_name in sorted(exp_groups.keys()):
            # Calculate totals for experiment level
            all_exp_exps = [
                exp
                for body in exp_groups[exp_name].values()
                for situation in body.values()
                for exp in situation
            ]
            exp_total = sum(exp.available_science for exp in all_exp_exps)
            exp_completed = sum(1 for exp in all_exp_exps if exp.available_science <= 0.1)
            exp_status = self._get_category_status(exp_total, len(all_exp_exps), exp_completed)

            exp_node = self.tree.insert(
                "", "end",
                text=f"{exp_status} {exp_name}",
                values=(f"{exp_total:.1f}",),
                open=False
            )

            for body in sorted(exp_groups[exp_name].keys()):
                # Calculate totals for body level
                all_body_exps = [
                    exp
                    for situation in exp_groups[exp_name][body].values()
                    for exp in situation
                ]
                body_total = sum(exp.available_science for exp in all_body_exps)
                body_completed = sum(1 for exp in all_body_exps if exp.available_science <= 0.1)
                body_status = self._get_category_status(body_total, len(all_body_exps), body_completed)

                body_node = self.tree.insert(
                    exp_node, "end",
                    text=f"{body_status} {body}",
                    values=(f"{body_total:.1f}",),
                    open=False
                )

                for situation in sorted(exp_groups[exp_name][body].keys()):
                    situation_exps = exp_groups[exp_name][body][situation]
                    situation_total = sum(exp.available_science for exp in situation_exps)
                    situation_completed = sum(1 for exp in situation_exps if exp.available_science <= 0.1)
                    situation_status = self._get_category_status(
                        situation_total, len(situation_exps), situation_completed
                    )

                    situation_node = self.tree.insert(
                        body_node, "end",
                        text=f"{situation_status} {self._format_situation(situation)}",
                        values=(f"{situation_total:.1f}",),
                        open=False
                    )

                    # Add individual experiments (with biomes if applicable)
                    for exp in sorted(situation_exps, key=lambda e: e.experiment_id.biome or ""):
                        biome_str = f" - {exp.experiment_id.biome}" if exp.experiment_id.biome else ""
                        status = self._get_experiment_status(exp)
                        self.tree.insert(
                            situation_node, "end",
                            text=f"{status} {exp.body_name}{biome_str}",
                            values=(f"{exp.available_science:.1f}",)
                        )

    def _populate_by_situation(self, experiments: List[AvailableExperiment]):
        """Populate tree grouped by situation."""
        # Group: Situation → Body → Biome → Experiment
        situation_groups = defaultdict(lambda: defaultdict(lambda: defaultdict(list)))

        for exp in experiments:
            exp_id = exp.experiment_id
            situation = exp_id.situation
            body = exp.body_name
            biome = exp_id.biome or "No Biome"

            situation_groups[situation][body][biome].append(exp)

        # Build tree
        for situation in sorted(situation_groups.keys()):
            # Calculate totals for situation level
            all_situation_exps = [
                exp
                for body in situation_groups[situation].values()
                for biome in body.values()
                for exp in biome
            ]
            situation_total = sum(exp.available_science for exp in all_situation_exps)
            situation_completed = sum(1 for exp in all_situation_exps if exp.available_science <= 0.1)
            situation_status = self._get_category_status(
                situation_total, len(all_situation_exps), situation_completed
            )

            situation_node = self.tree.insert(
                "", "end",
                text=f"{situation_status} {self._format_situation(situation)}",
                values=(f"{situation_total:.1f}",),
                open=False
            )

            for body in sorted(situation_groups[situation].keys()):
                # Calculate totals for body level
                all_body_exps = [
                    exp
                    for biome in situation_groups[situation][body].values()
                    for exp in biome
                ]
                body_total = sum(exp.available_science for exp in all_body_exps)
                body_completed = sum(1 for exp in all_body_exps if exp.available_science <= 0.1)
                body_status = self._get_category_status(body_total, len(all_body_exps), body_completed)

                body_node = self.tree.insert(
                    situation_node, "end",
                    text=f"{body_status} {body}",
                    values=(f"{body_total:.1f}",),
                    open=False
                )

                for biome in sorted(situation_groups[situation][body].keys()):
                    biome_exps = situation_groups[situation][body][biome]
                    biome_total = sum(exp.available_science for exp in biome_exps)
                    biome_completed = sum(1 for exp in biome_exps if exp.available_science <= 0.1)

                    if biome != "No Biome":
                        biome_status = self._get_category_status(
                            biome_total, len(biome_exps), biome_completed
                        )
                        biome_node = self.tree.insert(
                            body_node, "end",
                            text=f"{biome_status} {biome}",
                            values=(f"{biome_total:.1f}",),
                            open=False
                        )
                        parent = biome_node
                    else:
                        parent = body_node

                    # Add individual experiments
                    for exp in sorted(biome_exps, key=lambda e: e.experiment_name):
                        status = self._get_experiment_status(exp)
                        self.tree.insert(
                            parent, "end",
                            text=f"{status} {exp.experiment_name}",
                            values=(f"{exp.available_science:.1f}",)
                        )

    def _format_situation(self, situation: str) -> str:
        """Format situation name for display."""
        # Convert camelCase to readable format
        situation_names = {
            'SrfLanded': 'Surface (Landed)',
            'SrfSplashed': 'Surface (Splashed)',
            'FlyingLow': 'Flying (Low)',
            'FlyingHigh': 'Flying (High)',
            'InSpaceLow': 'Space (Low)',
            'InSpaceHigh': 'Space (High)',
        }
        return situation_names.get(situation, situation)

    def _get_experiment_status(self, exp: AvailableExperiment) -> str:
        """Get status symbol for an experiment."""
        if exp.available_science <= 0.1:  # Completed (account for floating point)
            return "✓"
        elif exp.is_partial:  # Partially completed
            return "◐"
        else:  # Not started
            return "☐"

    def _get_category_status(self, total_science: float, child_count: int, completed_count: int) -> str:
        """Get status symbol for a category based on its children."""
        if completed_count == child_count and child_count > 0:
            return "✓"  # All children completed
        elif total_science <= 0.1:
            return "✓"  # No science remaining
        elif completed_count > 0:
            return "◐"  # Some children completed
        else:
            return "☐"  # None completed

    def clear(self):
        """Clear all items from the tree."""
        for item in self.tree.get_children():
            self.tree.delete(item)
