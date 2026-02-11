"""Parser for KSP save files (.sfs format)."""

import os
from pathlib import Path
from typing import List, Optional
import sfsutils


class SFSParser:
    """Handles parsing of KSP save files."""

    # Default KSP installation paths for Windows
    DEFAULT_PATHS = [
        r"C:\Program Files (x86)\Steam\steamapps\common\Kerbal Space Program",
        r"C:\Program Files\Steam\steamapps\common\Kerbal Space Program",
        os.path.expanduser(r"~\Documents\Kerbal Space Program"),  # Non-Steam
    ]

    def __init__(self, ksp_directory: str = None):
        """
        Initialize SFS parser.

        Args:
            ksp_directory: Path to KSP installation directory.
                          If None, will attempt to auto-detect.
        """
        self.ksp_directory = Path(ksp_directory) if ksp_directory else None

        if self.ksp_directory is None:
            self.ksp_directory = self._find_ksp_directory()

    def _find_ksp_directory(self) -> Optional[Path]:
        """
        Attempt to auto-detect KSP installation directory.

        Returns:
            Path to KSP directory, or None if not found.
        """
        for path_str in self.DEFAULT_PATHS:
            path = Path(path_str)
            if path.exists() and (path / "saves").exists():
                return path
        return None

    def find_save_games(self) -> List[tuple]:
        """
        Find all save games in the KSP installation.

        Returns:
            List of tuples (save_name, save_path) for each save game found.
        """
        if not self.ksp_directory:
            return []

        saves_dir = self.ksp_directory / "saves"
        if not saves_dir.exists():
            return []

        save_games = []
        for save_folder in saves_dir.iterdir():
            if save_folder.is_dir():
                persistent_file = save_folder / "persistent.sfs"
                if persistent_file.exists():
                    save_games.append((save_folder.name, str(persistent_file)))

        return sorted(save_games)

    def parse_save_file(self, save_path: str) -> dict:
        """
        Parse a KSP save file.

        Args:
            save_path: Path to persistent.sfs file

        Returns:
            Parsed save data as nested dictionary

        Raises:
            FileNotFoundError: If save file doesn't exist
            ValueError: If save file is corrupted or invalid
        """
        save_path = Path(save_path)
        if not save_path.exists():
            raise FileNotFoundError(f"Save file not found: {save_path}")

        try:
            with open(save_path, 'r', encoding='utf-8') as f:
                save_data = sfsutils.parse_savefile(f)
            return save_data
        except Exception as e:
            raise ValueError(f"Failed to parse save file: {e}")

    def get_ksp_directory(self) -> Optional[str]:
        """Get current KSP directory path."""
        return str(self.ksp_directory) if self.ksp_directory else None

    def set_ksp_directory(self, directory: str):
        """Set KSP directory path."""
        self.ksp_directory = Path(directory)

    @staticmethod
    def validate_ksp_directory(directory: str) -> bool:
        """
        Validate that a directory is a valid KSP installation.

        Args:
            directory: Path to check

        Returns:
            True if valid KSP directory, False otherwise
        """
        path = Path(directory)
        return (path.exists() and
                (path / "saves").exists() and
                (path / "GameData").exists())
