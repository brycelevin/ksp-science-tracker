"""Data models for KSP science experiments."""

import re
from dataclasses import dataclass
from typing import Optional


@dataclass
class ExperimentID:
    """Represents a unique science experiment identifier."""

    experiment_type: str
    body: str
    situation: str
    biome: Optional[str] = None

    def to_ksp_id(self) -> str:
        """Convert to KSP save file format: experimentType@bodySituationBiome"""
        biome_part = self.biome if self.biome else ""
        return f"{self.experiment_type}@{self.body}{self.situation}{biome_part}"

    @classmethod
    def from_ksp_id(cls, ksp_id: str) -> 'ExperimentID':
        """
        Parse KSP science ID format.

        Format: experimentType@bodySituationBiome
        Example: crewReport@KerbinSrfLandedGrasslands

        Challenge: No delimiters between body/situation/biome.
        Strategy: Match known situations, extract body before and biome after.
        """
        # Split on @ to separate experiment type
        if '@' not in ksp_id:
            raise ValueError(f"Invalid KSP ID format (missing @): {ksp_id}")

        experiment_type, location = ksp_id.split('@', 1)

        # Known situations (order matters - match longer strings first)
        situations = [
            'SrfSplashed', 'SrfLanded',  # Surface situations
            'FlyingLow', 'FlyingHigh',    # Flying situations
            'InSpaceLow', 'InSpaceHigh'   # Space situations
        ]

        # Find which situation is in the location string
        situation_found = None
        situation_start = -1

        for situation in situations:
            if situation in location:
                situation_start = location.index(situation)
                situation_found = situation
                break

        if not situation_found:
            raise ValueError(f"Could not identify situation in: {location}")

        # Extract body (everything before situation)
        body = location[:situation_start]
        if not body:
            raise ValueError(f"Could not extract body from: {location}")

        # Extract biome (everything after situation)
        biome_start = situation_start + len(situation_found)
        biome = location[biome_start:] if biome_start < len(location) else None

        # Empty string biome should be None
        if biome == '':
            biome = None

        return cls(
            experiment_type=experiment_type,
            body=body,
            situation=situation_found,
            biome=biome
        )

    def __str__(self) -> str:
        biome_str = f" ({self.biome})" if self.biome else ""
        return f"{self.experiment_type} at {self.body} {self.situation}{biome_str}"

    def __hash__(self) -> int:
        return hash(self.to_ksp_id())

    def __eq__(self, other) -> bool:
        if not isinstance(other, ExperimentID):
            return False
        return self.to_ksp_id() == other.to_ksp_id()


@dataclass
class CompletedExperiment:
    """Represents a completed science experiment from a save file."""

    experiment_id: ExperimentID
    science_earned: float
    science_cap: float

    @property
    def is_fully_completed(self) -> bool:
        """Check if experiment is at maximum science."""
        return self.science_earned >= self.science_cap

    @property
    def remaining_science(self) -> float:
        """Calculate remaining science available."""
        return max(0, self.science_cap - self.science_earned)


@dataclass
class PossibleExperiment:
    """Represents a possible science experiment (from database)."""

    experiment_id: ExperimentID
    experiment_name: str
    body_name: str


@dataclass
class AvailableExperiment:
    """Represents an available (not yet completed) science experiment."""

    experiment_id: ExperimentID
    experiment_name: str
    body_name: str
    available_science: float
    is_partial: bool = False  # True if some science already collected

    def __str__(self) -> str:
        status = "partial" if self.is_partial else "new"
        return f"{self.experiment_name} at {self.body_name} ({self.available_science:.1f} pts, {status})"
