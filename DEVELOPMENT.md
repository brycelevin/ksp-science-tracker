# Development Notes

## Windows-Specific Considerations

This application is targeted for Windows 10 users, even though development may occur on macOS or Linux.

### Path Handling

- Windows uses backslashes (`\`) for paths, but Python's `pathlib.Path` handles this automatically
- Default KSP paths are Windows-specific:
  - Steam: `C:\Program Files (x86)\Steam\steamapps\common\Kerbal Space Program`
  - Non-Steam: `~\Documents\Kerbal Space Program`

### Testing on Windows

To test the application on Windows 10:

1. Install Python 3.8+: https://www.python.org/downloads/
   - Check "Add Python to PATH" during installation

2. Install dependencies:
   ```cmd
   pip install -r requirements.txt
   ```

3. Run the application:
   ```cmd
   python src\main.py
   ```

   Or use the launcher:
   ```cmd
   run.bat
   ```

### Known Issues

- **Path Spaces**: Windows paths often contain spaces (e.g., "Program Files"). The application uses `pathlib.Path` which handles this correctly.
- **Backslashes**: Raw strings (r"...") are used in path constants to avoid escape sequence issues.

## Architecture

### Data Flow

1. **User selects save** → `SaveSelector`
2. **Parse .sfs file** → `SFSParser` + `ScienceExtractor`
3. **Extract completed experiments** → `SaveGameData`
4. **Compare with all possible experiments** → `ScienceCalculator`
5. **Apply filters** → `FilterPanel`
6. **Display in tree** → `ExperimentTree`

### Key Design Decisions

1. **Hardcoded Game Data**: All experiments and bodies are in JSON files rather than parsed from KSP installation. This makes the app independent of KSP file structure and easier to maintain.

2. **Estimated Science Values**: Actual science values depend on many factors (difficulty, situation multipliers, body multipliers, transmission penalties). The app uses conservative estimates.

3. **sfsutils Library**: KSP save files use a custom ConfigNode format. Rather than write a parser, we use the existing `sfsutils` library.

4. **No Mod Support**: Stock KSP only. Mod experiments and bodies would require dynamic loading and are out of scope.

## Testing

### Unit Tests

Run tests with:
```bash
python tests/test_experiment_parsing.py
```

Tests cover:
- KSP science ID parsing (with various formats)
- Round-trip conversion (parse → to_ksp_id → parse)
- Science database generation
- Experiment filtering

### Manual Testing Checklist

- [ ] Application launches without errors
- [ ] KSP directory auto-detection works
- [ ] Browse button opens file dialog
- [ ] Save games are detected and listed
- [ ] Loading a save parses science correctly
- [ ] Filters update the tree view
- [ ] Group By changes reorganize the tree
- [ ] Statistics display correctly
- [ ] Tree can be collapsed/expanded
- [ ] Unicode symbols (☐, ◐) display correctly

### Test Data

To test the application, you need:
1. A Windows 10 machine
2. KSP 1 installed (Steam or non-Steam)
3. At least one save game with some science completed

## Future Improvements

### High Priority
- Better science value estimates (use actual KSP data if possible)
- Error handling for corrupted saves
- Loading indicator for large save files

### Medium Priority
- Export to CSV
- Search/filter by experiment name
- Show completed experiments (not just available)
- Dark mode / theme support

### Low Priority
- Mod support
- Auto-refresh on save file change
- Multiple save comparison
- Science mission planner

## Contributing

When adding features:

1. Test on Windows 10 if possible
2. Update JSON data files for new experiments/bodies
3. Add unit tests for new parsing logic
4. Update README with new features
5. Consider backward compatibility

## Code Style

- Follow PEP 8
- Use type hints
- Document complex logic
- Keep functions focused and small
- Use descriptive variable names
