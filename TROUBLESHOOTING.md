# Troubleshooting Guide

## Common Issues and Solutions

### Installation Issues

#### Problem: "Python is not recognized as an internal or external command"

**Cause**: Python is not installed or not in your system PATH.

**Solution**:
1. Download Python from https://www.python.org/downloads/
2. Run the installer
3. **IMPORTANT**: Check the box "Add Python to PATH" before clicking Install
4. If already installed without PATH:
   - Reinstall Python with the "Add to PATH" option
   - Or manually add Python to your system PATH:
     - Control Panel → System → Advanced System Settings
     - Environment Variables → System Variables → Path
     - Add: `C:\Python38` (or your Python installation directory)

#### Problem: "No module named 'sfsutils'"

**Cause**: Required dependencies not installed.

**Solution**:
```cmd
pip install -r requirements.txt
```

If pip is not found:
```cmd
python -m pip install -r requirements.txt
```

#### Problem: "pip is not recognized"

**Cause**: pip not in PATH.

**Solution**:
```cmd
python -m ensurepip
python -m pip install -r requirements.txt
```

---

### Application Launch Issues

#### Problem: Double-clicking main.py does nothing

**Cause**: Python not associated with .py files.

**Solution**:
- Use the provided `run.bat` launcher instead
- Or open Command Prompt and run:
  ```cmd
  python src\main.py
  ```

#### Problem: "ImportError: No module named 'models'"

**Cause**: Running from wrong directory.

**Solution**:
- Make sure you're running from the project root directory
- Command Prompt should show: `C:\path\to\ksp-science-tracker>`
- Run: `python src\main.py` (not `python main.py`)

#### Problem: Window opens then immediately closes

**Cause**: Python error occurred but window closed too fast to see.

**Solution**:
1. Open Command Prompt
2. Navigate to project directory
3. Run: `python src\main.py`
4. Error message will be visible in the console

---

### KSP Directory Issues

#### Problem: "No KSP directory selected" or auto-detection fails

**Cause**: KSP not installed in default location.

**Solution**:
1. Click the "Browse..." button
2. Navigate to your KSP installation folder
3. Select the main KSP folder (should contain "saves" and "GameData" subfolders)

Common KSP locations:
- Steam: `C:\Program Files (x86)\Steam\steamapps\common\Kerbal Space Program`
- Steam (alternative): `C:\Program Files\Steam\steamapps\common\Kerbal Space Program`
- Non-Steam: `C:\Users\[YourName]\Documents\Kerbal Space Program`
- Custom: Wherever you installed KSP

#### Problem: "Invalid KSP directory"

**Cause**: Selected folder is not a valid KSP installation.

**Solution**:
- Make sure you selected the ROOT KSP folder, not a subfolder
- The folder should contain:
  - `saves/` directory
  - `GameData/` directory
  - `KSP.exe` or `KSP_x64.exe`

#### Problem: "No save games found"

**Cause**: No save games exist or wrong KSP directory.

**Solution**:
1. Verify you've played KSP and created at least one save
2. Check the saves directory: `[KSP]/saves/[SaveName]/persistent.sfs`
3. If files exist but not detected, try:
   - Clicking "Refresh" button
   - Reselecting the KSP directory

---

### Save File Loading Issues

#### Problem: "Failed to parse save file"

**Cause**: Corrupted save file or incompatible format.

**Solution**:
1. Try loading a different save game
2. Verify the save works in KSP itself
3. Check if you're using KSP 1 (not KSP 2 - not supported)
4. If save is modded heavily, some mod experiments may cause issues

#### Problem: Science counts don't match in-game

**Cause**: Science values are estimates.

**Solution**:
- This is expected behavior
- The app shows estimated available science
- Actual values depend on:
  - Difficulty settings
  - Situation multipliers
  - Transmission penalties
  - First-time vs repeated experiments
- Use values as relative guides, not exact predictions

---

### Display Issues

#### Problem: Checkboxes show as squares or question marks

**Cause**: Font doesn't support Unicode symbols (☐, ◐).

**Solution**:
- This is cosmetic only - functionality is not affected
- Windows 10 with default fonts should display correctly
- If using custom system font, switch to a Unicode-compatible font

#### Problem: Tree view is empty

**Cause**: All experiments already completed, or filters too restrictive.

**Solution**:
1. Check "Show" dropdown - set to "Available Only"
2. Reset filters:
   - Body: "All"
   - Experiment: "All"
3. Load a save with incomplete science
4. Check statistics bar at bottom for completion percentage

#### Problem: Window too small / UI elements cut off

**Cause**: Low screen resolution.

**Solution**:
- Minimum resolution: 800x600
- Recommended: 1024x768 or higher
- Resize window by dragging edges
- UI will adjust automatically

---

### Performance Issues

#### Problem: Application is slow to load

**Cause**: Large save file or slow disk.

**Solution**:
- First load generates 1,049 possible experiments (one-time)
- Subsequent operations should be fast
- If consistently slow, check:
  - Antivirus not scanning Python
  - Disk not nearly full
  - Save file size (very large saves may take longer)

#### Problem: High memory usage

**Cause**: Normal for parsing large save files.

**Solution**:
- Typical usage: 50-100 MB RAM
- If much higher, try:
  - Closing and reopening the app
  - Loading smaller save files first

---

### Data Issues

#### Problem: Missing experiments from mods

**Cause**: App only includes stock KSP experiments.

**Solution**:
- This is by design
- Mod experiments are not supported
- Stock KSP includes 11 experiment types across 17 bodies
- Future versions may add mod support

#### Problem: Missing celestial bodies

**Cause**: Only stock KSP bodies included.

**Solution**:
- Stock KSP includes 17 bodies from the Kerbol system
- Mod planets/moons are not supported
- If a stock body is missing, please report as a bug

---

### Windows-Specific Issues

#### Problem: "Access is denied" when running

**Cause**: File permissions or antivirus blocking.

**Solution**:
1. Run as Administrator (right-click run.bat → Run as administrator)
2. Check antivirus isn't blocking Python
3. Verify you have read access to KSP saves folder

#### Problem: Path has spaces and causes errors

**Cause**: Improper path handling.

**Solution**:
- The app should handle spaces correctly
- If issues persist:
  - Try installing KSP in a path without spaces
  - Or use the 8.3 short path name (e.g., `PROGRA~2` for `Program Files (x86)`)

---

## Still Having Issues?

### Before Reporting a Bug

1. **Update Python**: Make sure you're using Python 3.8 or newer
   ```cmd
   python --version
   ```

2. **Update Dependencies**:
   ```cmd
   pip install --upgrade -r requirements.txt
   ```

3. **Try Fresh Install**:
   - Delete the project folder
   - Re-extract from zip
   - Reinstall dependencies
   - Test again

### Reporting Bugs

If you still have issues, provide:
- Python version (`python --version`)
- Windows version
- KSP installation type (Steam/Non-Steam)
- Full error message (from Command Prompt)
- Screenshot if UI-related
- Save file size and mod count (if applicable)

### Getting Help

- Check README.md for usage instructions
- Check QUICKSTART.md for installation steps
- Check DEVELOPMENT.md for technical details
- Report issues on GitHub (if available)

---

## Tips for Best Experience

1. **Keep saves organized**: Use descriptive save names in KSP
2. **Regular backups**: Back up your saves before major missions
3. **Filter effectively**: Use body/experiment filters to focus your planning
4. **Use grouping**: Change "Group By" to see data different ways
5. **Check statistics**: Bottom bar shows your overall progress
6. **Plan missions**: Use the app to identify high-value targets
7. **Update regularly**: Reload save after playing to see progress

---

## Advanced Troubleshooting

### Running with Verbose Output

To see detailed error messages:
```cmd
python src\main.py 2>&1 | more
```

### Testing Components Individually

Test if modules load:
```cmd
cd src
python -c "from models.science_database import ScienceDatabase; print('OK')"
```

Test if data files are valid:
```cmd
python -c "import json; json.load(open('data/experiments.json')); print('OK')"
```

### Clean Reinstall

1. Uninstall Python
2. Delete project folder
3. Reinstall Python (with "Add to PATH")
4. Re-extract project
5. Install dependencies
6. Test

---

Last Updated: February 9, 2026
