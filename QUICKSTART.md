# Quick Start Guide

## For Windows 10 Users

### Step 1: Install Python

1. Download Python 3.8 or higher from https://www.python.org/downloads/
2. Run the installer
3. **IMPORTANT**: Check the box "Add Python to PATH" before clicking Install

### Step 2: Install the Application

1. Download/extract this application to a folder (e.g., `C:\KSP-Science-Tracker`)
2. Open Command Prompt in the application folder:
   - Press `Win + R`
   - Type `cmd`
   - Navigate to the folder: `cd C:\KSP-Science-Tracker`

3. Install dependencies:
   ```cmd
   pip install -r requirements.txt
   ```

### Step 3: Run the Application

**Option A: Use the Launcher (Recommended)**
- Double-click `run.bat`

**Option B: Command Line**
```cmd
python src\main.py
```

### Step 4: First Use

1. **Set KSP Directory**:
   - If auto-detected, skip to step 2
   - If not found, click "Browse..." and navigate to your KSP installation
   - Common locations:
     - `C:\Program Files (x86)\Steam\steamapps\common\Kerbal Space Program`
     - `C:\Program Files\Steam\steamapps\common\Kerbal Space Program`
     - `C:\Users\[YourName]\Documents\Kerbal Space Program`

2. **Select a Save Game**:
   - Choose a save from the dropdown
   - The app will load and analyze your science data

3. **Explore Available Science**:
   - Use filters to narrow down by body or experiment type
   - Change "Group By" to organize differently
   - Expand/collapse tree nodes to explore

### Troubleshooting

**"Python is not recognized..."**
- Python is not in your PATH
- Reinstall Python and check "Add Python to PATH"
- Or add Python manually to system PATH

**"No module named 'sfsutils'"**
- Dependencies not installed
- Run: `pip install -r requirements.txt`

**"No KSP directory selected"**
- Click Browse and select your KSP folder
- Make sure it contains "saves" and "GameData" folders

**"No save games found"**
- Make sure you have at least one save game in KSP
- Check that persistent.sfs files exist in: `KSP\saves\[SaveName]\persistent.sfs`

**Unicode symbols (☐) not displaying**
- Your terminal font may not support these characters
- The app will still work, just with different checkbox symbols

### Tips

- **Filter by Body**: Focus on one planet/moon at a time
- **Group by Experiment**: See all locations for a specific experiment
- **Sort by Science**: Higher values = more worthwhile missions
- **Partial Completion (◐)**: You started this experiment but can get more science

### Understanding Science Values

The science values shown are **estimates**. Actual values vary based on:
- Your difficulty settings (Science rewards multiplier)
- Location (Space gives less than surface for most experiments)
- First time vs repeated experiments
- Transmission penalties (transmitting vs recovering)

Use the values as a **relative guide** to plan missions, not as exact predictions.

### Need Help?

- Read the full README.md for detailed information
- Check DEVELOPMENT.md for technical details
- Report bugs or issues on GitHub

## Example Usage

**Scenario: Planning a Mun Mission**

1. Set Body filter to "Mun"
2. Group By "Situation"
3. Look at "Surface (Landed)" section
4. See which experiments you still need to do
5. Plan your mission to hit multiple biomes!

**Scenario: Finding High-Value Experiments**

1. Leave filters on "All"
2. Group By "Body"
3. Expand bodies you can reach
4. Look for experiments with high science values
5. Prioritize missions to those locations

**Scenario: Completing All Crew Reports**

1. Set Experiment filter to "Crew Report"
2. Group By "Body"
3. See all locations where you haven't done crew reports yet
4. Plan missions or use existing vessels to collect them
