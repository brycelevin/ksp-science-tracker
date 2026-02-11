"""Science database that generates all possible experiments."""

import json
import os
from typing import List, Dict, Set
from pathlib import Path

from .experiment import ExperimentID, PossibleExperiment


class ScienceDatabase:
    """Manages all possible science experiments in KSP."""

    def __init__(self, data_dir: str = None):
        """
        Initialize science database from JSON files.

        Args:
            data_dir: Path to data directory containing JSON files.
                     Defaults to project data/ directory.
        """
        if data_dir is None:
            # Default to data/ directory relative to this file
            project_root = Path(__file__).parent.parent.parent
            data_dir = project_root / "data"

        self.data_dir = Path(data_dir)
        self.experiments: Dict[str, dict] = {}
        self.bodies: Dict[str, dict] = {}
        self._possible_experiments: List[PossibleExperiment] = []

        self._load_data()
        self._generate_experiments()

    def _load_data(self):
        """Load experiment and celestial body data from JSON files."""
        # Load experiments
        experiments_file = self.data_dir / "experiments.json"
        with open(experiments_file, 'r') as f:
            data = json.load(f)
            for exp in data['experiments']:
                self.experiments[exp['id']] = exp

        # Load celestial bodies
        bodies_file = self.data_dir / "celestial_bodies.json"
        with open(bodies_file, 'r') as f:
            data = json.load(f)
            for body in data['bodies']:
                self.bodies[body['name']] = body

    def _generate_experiments(self):
        """Generate all valid experiment combinations."""
        self._possible_experiments = []

        for exp_id, exp_data in self.experiments.items():
            for body_name, body_data in self.bodies.items():
                # Skip asteroids (special handling needed)
                if exp_id == "asteroidSample" and body_name != "Sun":
                    continue

                # Get valid situations for this body
                valid_situations = set(body_data['situations'])
                exp_situations = set(exp_data['situations'])

                # Only use situations valid for both experiment and body
                available_situations = valid_situations & exp_situations

                for situation in available_situations:
                    if exp_data['requires_biome'] and body_data['biomes']:
                        # Generate experiment for each biome
                        for biome in body_data['biomes']:
                            exp_id_obj = ExperimentID(
                                experiment_type=exp_id,
                                body=body_name,
                                situation=situation,
                                biome=biome
                            )
                            self._possible_experiments.append(
                                PossibleExperiment(
                                    experiment_id=exp_id_obj,
                                    experiment_name=exp_data['name'],
                                    body_name=body_name
                                )
                            )
                    else:
                        # Generate experiment without biome
                        exp_id_obj = ExperimentID(
                            experiment_type=exp_id,
                            body=body_name,
                            situation=situation,
                            biome=None
                        )
                        self._possible_experiments.append(
                            PossibleExperiment(
                                experiment_id=exp_id_obj,
                                experiment_name=exp_data['name'],
                                body_name=body_name
                            )
                        )

    def get_all_experiments(self) -> List[PossibleExperiment]:
        """Get list of all possible experiments."""
        return self._possible_experiments

    def get_experiments_by_body(self, body_name: str) -> List[PossibleExperiment]:
        """Get all possible experiments for a specific celestial body."""
        return [exp for exp in self._possible_experiments
                if exp.body_name == body_name]

    def get_experiments_by_type(self, experiment_type: str) -> List[PossibleExperiment]:
        """Get all possible experiments of a specific type."""
        return [exp for exp in self._possible_experiments
                if exp.experiment_id.experiment_type == experiment_type]

    def get_body_names(self) -> List[str]:
        """Get list of all celestial body names."""
        return sorted(self.bodies.keys())

    def get_experiment_types(self) -> List[tuple]:
        """Get list of all experiment types as (id, name) tuples."""
        return [(exp_id, exp_data['name'])
                for exp_id, exp_data in sorted(self.experiments.items())]

    def get_experiment_name(self, experiment_type: str) -> str:
        """Get human-readable name for an experiment type."""
        return self.experiments.get(experiment_type, {}).get('name', experiment_type)

    def get_situations(self) -> List[str]:
        """Get list of all possible situations."""
        return [
            "SrfLanded", "SrfSplashed",
            "FlyingLow", "FlyingHigh",
            "InSpaceLow", "InSpaceHigh"
        ]

    def get_total_experiment_count(self) -> int:
        """Get total number of possible experiments."""
        return len(self._possible_experiments)
