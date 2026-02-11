"""Save game data model."""

from typing import Dict, Optional, List
from .experiment import ExperimentID, CompletedExperiment


class SaveGameData:
    """Represents science data from a KSP save file."""

    def __init__(self, save_name: str = ""):
        """
        Initialize save game data.

        Args:
            save_name: Name of the save game
        """
        self.save_name = save_name
        self.completed_experiments: Dict[ExperimentID, CompletedExperiment] = {}

    def add_completed_experiment(self, experiment: CompletedExperiment):
        """Add a completed experiment to the save data."""
        self.completed_experiments[experiment.experiment_id] = experiment

    def get_completed_experiment(self, exp_id: ExperimentID) -> Optional[CompletedExperiment]:
        """Get completed experiment by ID, or None if not completed."""
        return self.completed_experiments.get(exp_id)

    def is_experiment_completed(self, exp_id: ExperimentID) -> bool:
        """Check if an experiment has been completed (even partially)."""
        return exp_id in self.completed_experiments

    def is_experiment_fully_completed(self, exp_id: ExperimentID) -> bool:
        """Check if an experiment is fully completed (at max science)."""
        completed = self.completed_experiments.get(exp_id)
        return completed.is_fully_completed if completed else False

    def get_total_science(self) -> float:
        """Calculate total science earned in this save."""
        return sum(exp.science_earned for exp in self.completed_experiments.values())

    def get_completed_count(self) -> int:
        """Get count of completed experiments."""
        return len(self.completed_experiments)

    def get_all_completed_experiments(self) -> List[CompletedExperiment]:
        """Get list of all completed experiments."""
        return list(self.completed_experiments.values())
