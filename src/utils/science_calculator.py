"""Calculate available science by comparing possible vs completed experiments."""

from typing import List, Dict
from models.experiment import AvailableExperiment, PossibleExperiment, ExperimentID
from models.save_data import SaveGameData
from models.science_database import ScienceDatabase


class ScienceCalculator:
    """Calculates available science experiments."""

    # Default science values (multiplied by situation/body modifiers in game)
    # These are rough estimates - actual values depend on many factors
    DEFAULT_SCIENCE_VALUES = {
        'crewReport': 5.0,
        'evaReport': 8.0,
        'surfaceSample': 30.0,
        'temperatureScan': 8.0,
        'barometerScan': 12.0,
        'seismicScan': 20.0,
        'gravityScan': 20.0,
        'atmosphereAnalysis': 12.0,
        'asteroidSample': 70.0,
        'mysteryGoo': 10.0,
        'mobileMaterialsLab': 25.0,
    }

    def __init__(self, science_db: ScienceDatabase):
        """
        Initialize science calculator.

        Args:
            science_db: Science database containing all possible experiments
        """
        self.science_db = science_db

    def calculate_available_science(
        self,
        save_data: SaveGameData
    ) -> List[AvailableExperiment]:
        """
        Calculate all available (not fully completed) science experiments.

        Args:
            save_data: Save game data with completed experiments

        Returns:
            List of available experiments with remaining science
        """
        available = []

        for possible_exp in self.science_db.get_all_experiments():
            exp_id = possible_exp.experiment_id
            completed = save_data.get_completed_experiment(exp_id)

            if completed is None:
                # Experiment not started - fully available
                estimated_science = self._estimate_science_value(
                    possible_exp.experiment_id
                )
                available.append(
                    AvailableExperiment(
                        experiment_id=exp_id,
                        experiment_name=possible_exp.experiment_name,
                        body_name=possible_exp.body_name,
                        available_science=estimated_science,
                        is_partial=False
                    )
                )
            elif not completed.is_fully_completed:
                # Experiment partially completed
                available.append(
                    AvailableExperiment(
                        experiment_id=exp_id,
                        experiment_name=possible_exp.experiment_name,
                        body_name=possible_exp.body_name,
                        available_science=completed.remaining_science,
                        is_partial=True
                    )
                )
            # If fully completed, don't include in available list

        return available

    def _estimate_science_value(self, exp_id: ExperimentID) -> float:
        """
        Estimate science value for an uncompleted experiment.

        Note: This is a rough estimate. Actual values depend on:
        - Situation multipliers (surface vs space vs flying)
        - Body multipliers (Mun vs Jool vs Kerbin)
        - Transmission penalties
        - Whether it's the first time or a repeat

        For now, we use conservative base values.
        """
        return self.DEFAULT_SCIENCE_VALUES.get(
            exp_id.experiment_type,
            10.0  # Default fallback value
        )

    def calculate_statistics(
        self,
        available_experiments: List[AvailableExperiment],
        save_data: SaveGameData
    ) -> Dict[str, float]:
        """
        Calculate statistics about science progress.

        Args:
            available_experiments: List of available experiments
            save_data: Save game data

        Returns:
            Dictionary with statistics
        """
        total_possible = self.science_db.get_total_experiment_count()
        total_completed = save_data.get_completed_count()
        total_available = len(available_experiments)

        # Sum estimated available science
        total_available_science = sum(
            exp.available_science for exp in available_experiments
        )

        # Science already earned
        total_earned_science = save_data.get_total_science()

        return {
            'total_possible_experiments': total_possible,
            'total_completed_experiments': total_completed,
            'total_available_experiments': total_available,
            'total_available_science': total_available_science,
            'total_earned_science': total_earned_science,
            'completion_percentage': (total_completed / total_possible * 100)
                                    if total_possible > 0 else 0
        }
