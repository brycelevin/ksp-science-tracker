# KSP Science Tracker

A desktop GUI application for tracking completed and available science experiments in Kerbal Space Program (KSP 1).

## Features

- **Load KSP Save Games**: Browse and load any save game from your KSP installation
- **Track Available Science**: See all science experiments you haven't completed yet
- **Filter by Body or Experiment**: Focus on specific celestial bodies or experiment types
- **Multiple Grouping Options**: View experiments grouped by Body, Experiment Type, or Situation
- **Science Statistics**: Track total science earned and available
- **Hierarchical Tree View**: Easy-to-navigate display of all experiments

## Requirements

- Python 3.8 or higher
- Windows 10
- Kerbal Space Program 1 installation

## Installation

1. Clone or download this repository

2. Install Python dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
python src/main.py
```

## Usage

### First Launch

1. The application will attempt to auto-detect your KSP installation
   - Default locations checked:
     - `C:\Program Files (x86)\Steam\steamapps\common\Kerbal Space Program`
     - `C:\Program Files\Steam\steamapps\common\Kerbal Space Program`
     - `~\Documents\Kerbal Space Program` (non-Steam)

2. If auto-detection fails, click **Browse** to manually select your KSP installation directory

### Loading a Save Game

1. Once KSP directory is set, the **Select Save** dropdown will populate with available saves
2. Choose a save game from the dropdown
3. The application will parse the save and display available experiments

### Filtering and Viewing

- **Body Filter**: Show only experiments for a specific celestial body (Kerbin, Mun, etc.)
- **Experiment Filter**: Show only specific experiment types (Crew Report, EVA Report, etc.)
- **Show Mode**:
  - "Available Only" - Shows only incomplete experiments (default)
  - "All Experiments" - Would show all experiments (future feature)
- **Group By**:
  - "Body" - Organize by celestial body → situation → biome → experiment
  - "Experiment" - Organize by experiment type → body → situation
  - "Situation" - Organize by situation (surface, flying, space) → body → experiment

### Understanding the Display

- **☐** - Experiment not started (full science available)
- **◐** - Experiment partially completed (some science remaining)
- **Science Values** - Estimated science points available
  - Note: Actual values depend on difficulty settings and situation multipliers

### Statistics Bar

The bottom of the window shows:
- Current save game name
- Total science earned
- Estimated available science
- Completion percentage

## Project Structure

```
ksp-science-tracker/
├── src/
│   ├── main.py              # Application entry point
│   ├── models/              # Data models
│   │   ├── experiment.py    # Experiment data structures
│   │   ├── science_database.py  # Database of all possible experiments
│   │   └── save_data.py     # Save game data model
│   ├── parsers/             # Save file parsing
│   │   ├── sfs_parser.py    # SFS file parser wrapper
│   │   └── science_extractor.py  # Science data extraction
│   ├── gui/                 # GUI components
│   │   ├── main_window.py   # Main application window
│   │   ├── save_selector.py # Save game selector widget
│   │   ├── filter_panel.py  # Filter controls
│   │   └── experiment_tree.py  # Tree view display
│   └── utils/               # Utilities
│       ├── config.py        # Configuration constants
│       └── science_calculator.py  # Science calculation logic
├── data/                    # Game data
│   ├── experiments.json     # All experiment definitions
│   └── celestial_bodies.json  # All celestial bodies and biomes
├── tests/                   # Unit tests
├── requirements.txt         # Python dependencies
└── README.md               # This file
```

## Data Files

The application includes hardcoded data for all stock KSP experiments and celestial bodies:

- **experiments.json**: 11 experiment types with their properties
- **celestial_bodies.json**: 17 celestial bodies with situations and biomes

This data represents stock KSP 1 and does not include mod content.

## How It Works

1. **Save File Parsing**: Uses `sfsutils` library to parse KSP's `.sfs` save files
2. **Science Extraction**: Extracts completed experiments from the ResearchAndDevelopment scenario
3. **Experiment Generation**: Generates all ~10,000 possible experiment combinations from game data
4. **Comparison**: Compares possible experiments against completed ones to find what's available
5. **Display**: Shows results in an organized, filterable tree view

## Limitations

- **Stock KSP Only**: Only includes stock experiments and bodies (no mod support)
- **Estimated Science Values**: Science values are estimates and may not match exact in-game values
- **KSP 1 Only**: Designed for Kerbal Space Program 1, not KSP 2
- **Windows 10**: Primarily tested on Windows 10

## Troubleshooting

### "No KSP directory selected"
- Click Browse and navigate to your KSP installation folder
- The folder should contain "saves" and "GameData" subdirectories

### "No save games found"
- Ensure you've played KSP and created at least one save
- Check that the KSP directory is correct
- Verify that `saves/[SaveName]/persistent.sfs` files exist

### "Failed to parse save file"
- Save file may be corrupted
- Try loading a different save
- Ensure you're using KSP 1 (not KSP 2)

### Science values don't match in-game
- Values shown are estimates based on experiment type
- Actual values vary by:
  - Difficulty settings
  - Situation (surface vs space)
  - Celestial body (Kerbin vs Jool)
  - Whether you've done the experiment before
  - Whether you transmitted or recovered the data

## Future Enhancements

Potential features for future versions:
- Export to CSV/Excel
- Auto-refresh when save file changes
- Mod support (custom experiments and bodies)
- Mission planning suggestions
- Multi-save comparison
- More accurate science value calculations

## License

This project is intended for personal use with Kerbal Space Program.

## Credits

- Built for the Kerbal Space Program community
- Uses `sfsutils` library for save file parsing
- KSP game data from the official KSP Wiki

## Contributing

This is a personal project, but suggestions and bug reports are welcome via GitHub issues.
