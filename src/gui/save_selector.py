"""Save game selector widget."""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from pathlib import Path
from typing import Callable, Optional, List

from parsers.sfs_parser import SFSParser
from utils.config import DEFAULT_KSP_PATHS


class SaveSelector(ttk.Frame):
    """Widget for selecting KSP directory and save game."""

    def __init__(self, parent, on_save_selected: Callable[[str, str], None]):
        """
        Initialize save selector.

        Args:
            parent: Parent widget
            on_save_selected: Callback(save_name, save_path) when save is selected
        """
        super().__init__(parent)
        self.on_save_selected = on_save_selected
        self.parser = SFSParser()

        self._build_ui()
        self._refresh_saves()

    def _build_ui(self):
        """Build the save selector UI."""
        # KSP Directory section
        dir_frame = ttk.LabelFrame(self, text="KSP Installation", padding=10)
        dir_frame.pack(fill=tk.X, padx=5, pady=5)

        self.ksp_dir_var = tk.StringVar()
        ksp_dir = self.parser.get_ksp_directory()
        if ksp_dir:
            self.ksp_dir_var.set(ksp_dir)

        ttk.Label(dir_frame, text="Directory:").grid(row=0, column=0, sticky=tk.W, padx=5)

        dir_entry = ttk.Entry(dir_frame, textvariable=self.ksp_dir_var, width=50)
        dir_entry.grid(row=0, column=1, sticky=tk.EW, padx=5)

        browse_btn = ttk.Button(dir_frame, text="Browse...", command=self._browse_directory)
        browse_btn.grid(row=0, column=2, padx=5)

        dir_frame.columnconfigure(1, weight=1)

        # Save Game section
        save_frame = ttk.LabelFrame(self, text="Save Game", padding=10)
        save_frame.pack(fill=tk.X, padx=5, pady=5)

        ttk.Label(save_frame, text="Select Save:").grid(row=0, column=0, sticky=tk.W, padx=5)

        self.save_combo = ttk.Combobox(save_frame, state='readonly', width=40)
        self.save_combo.grid(row=0, column=1, sticky=tk.EW, padx=5)
        self.save_combo.bind('<<ComboboxSelected>>', self._on_save_selected)

        refresh_btn = ttk.Button(save_frame, text="Refresh", command=self._refresh_saves)
        refresh_btn.grid(row=0, column=2, padx=5)

        save_frame.columnconfigure(1, weight=1)

        # Status label
        self.status_label = ttk.Label(self, text="", foreground="gray")
        self.status_label.pack(fill=tk.X, padx=5, pady=2)

    def _browse_directory(self):
        """Open directory browser for KSP installation."""
        initial_dir = self.ksp_dir_var.get() or "C:\\"
        directory = filedialog.askdirectory(
            title="Select KSP Installation Directory",
            initialdir=initial_dir
        )

        if directory:
            if SFSParser.validate_ksp_directory(directory):
                self.ksp_dir_var.set(directory)
                self.parser.set_ksp_directory(directory)
                self._refresh_saves()
            else:
                messagebox.showerror(
                    "Invalid Directory",
                    "The selected directory does not appear to be a valid KSP installation.\n\n"
                    "Please select the main KSP directory (should contain 'saves' and 'GameData' folders)."
                )

    def _refresh_saves(self):
        """Refresh the list of available save games."""
        ksp_dir = self.ksp_dir_var.get()

        if not ksp_dir:
            self.status_label.config(text="No KSP directory selected", foreground="red")
            self.save_combo['values'] = []
            return

        if not SFSParser.validate_ksp_directory(ksp_dir):
            self.status_label.config(text="Invalid KSP directory", foreground="red")
            self.save_combo['values'] = []
            return

        self.parser.set_ksp_directory(ksp_dir)
        save_games = self.parser.find_save_games()

        if not save_games:
            self.status_label.config(text="No save games found", foreground="orange")
            self.save_combo['values'] = []
            return

        # Store save games and populate combo box
        self.save_games = save_games
        save_names = [name for name, _ in save_games]
        self.save_combo['values'] = save_names

        self.status_label.config(
            text=f"Found {len(save_games)} save game(s)",
            foreground="green"
        )

        # Auto-select first save if available
        if save_names:
            self.save_combo.current(0)
            self._on_save_selected(None)

    def _on_save_selected(self, event):
        """Handle save game selection."""
        selected_index = self.save_combo.current()
        if selected_index >= 0 and selected_index < len(self.save_games):
            save_name, save_path = self.save_games[selected_index]
            self.on_save_selected(save_name, save_path)

    def get_selected_save(self) -> Optional[tuple]:
        """
        Get currently selected save game.

        Returns:
            Tuple of (save_name, save_path) or None if no selection
        """
        selected_index = self.save_combo.current()
        if selected_index >= 0 and selected_index < len(self.save_games):
            return self.save_games[selected_index]
        return None
