@echo off
REM KSP Science Tracker Launcher for Windows

echo Starting KSP Science Tracker...
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo.
    echo Please install Python 3.8 or higher from https://www.python.org/
    echo Make sure to check "Add Python to PATH" during installation
    pause
    exit /b 1
)

REM Check if requirements are installed
python -c "import sfsutils" >nul 2>&1
if errorlevel 1 (
    echo Installing required dependencies...
    python -m pip install -r requirements.txt
    if errorlevel 1 (
        echo ERROR: Failed to install dependencies
        pause
        exit /b 1
    )
    echo.
)

REM Run the application
python src\main.py

REM If there was an error, pause to show it
if errorlevel 1 (
    echo.
    echo ERROR: Application encountered an error
    pause
)
