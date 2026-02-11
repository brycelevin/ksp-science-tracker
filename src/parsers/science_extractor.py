"""Extracts science data from parsed KSP save files."""

from typing import List, Dict, Any
from models.experiment import ExperimentID, CompletedExperiment
from models.save_data import SaveGameData


class ScienceExtractor:
    """Extracts science experiment data from parsed save files."""

    @staticmethod
    def extract_science_data(parsed_save: dict, save_name: str = "") -> SaveGameData:
        """
        Extract science experiments from parsed save file.

        Args:
            parsed_save: Parsed save data from sfsutils
            save_name: Name of the save game

        Returns:
            SaveGameData object containing all completed experiments
        """
        save_data = SaveGameData(save_name=save_name)

        # Navigate to ResearchAndDevelopment scenario
        try:
            game = parsed_save.get('GAME', {})
            scenarios = game.get('SCENARIO', [])

            # Normalize to list (sfsutils may return dict or list)
            if isinstance(scenarios, dict):
                scenarios = [scenarios]

            # Find ResearchAndDevelopment scenario
            rd_scenario = None
            for scenario in scenarios:
                if scenario.get('name') == 'ResearchAndDevelopment':
                    rd_scenario = scenario
                    break

            if not rd_scenario:
                # No R&D scenario found - likely new game with no science
                return save_data

            # Extract Science nodes
            science_nodes = rd_scenario.get('Science', [])

            # Normalize to list
            if isinstance(science_nodes, dict):
                science_nodes = [science_nodes]

            # Parse each science entry
            for science_node in science_nodes:
                try:
                    completed_exp = ScienceExtractor._parse_science_node(science_node)
                    if completed_exp:
                        save_data.add_completed_experiment(completed_exp)
                except (ValueError, KeyError) as e:
                    # Skip invalid science entries
                    print(f"Warning: Skipping invalid science entry: {e}")
                    continue

        except (KeyError, AttributeError) as e:
            print(f"Warning: Error navigating save structure: {e}")

        return save_data

    @staticmethod
    def _parse_science_node(science_node: dict) -> CompletedExperiment:
        """
        Parse a single Science node from save file.

        Args:
            science_node: Dictionary containing science data

        Returns:
            CompletedExperiment object

        Raises:
            ValueError: If node is invalid or cannot be parsed
        """
        # Extract fields
        ksp_id = science_node.get('id')
        if not ksp_id:
            raise ValueError("Science node missing 'id' field")

        # Parse science values (may be strings or floats)
        try:
            science_earned = float(science_node.get('sci', 0))
            science_cap = float(science_node.get('cap', 0))
        except (ValueError, TypeError):
            raise ValueError(f"Invalid science values for {ksp_id}")

        # Parse experiment ID
        try:
            exp_id = ExperimentID.from_ksp_id(ksp_id)
        except ValueError as e:
            raise ValueError(f"Failed to parse experiment ID '{ksp_id}': {e}")

        return CompletedExperiment(
            experiment_id=exp_id,
            science_earned=science_earned,
            science_cap=science_cap
        )

    @staticmethod
    def get_save_name_from_file(parsed_save: dict) -> str:
        """
        Extract save game name from parsed save file.

        Args:
            parsed_save: Parsed save data

        Returns:
            Save game name, or "Unknown" if not found
        """
        try:
            return parsed_save.get('GAME', {}).get('Title', 'Unknown')
        except (KeyError, AttributeError):
            return 'Unknown'
