@echo off
REM ============================================================================
REM Texas Roofing Scraper - ONE-TIME SETUP
REM ============================================================================
REM This file installs all required software and libraries.
REM You only need to run this ONCE!
REM ============================================================================

color 0A
title Texas Roofing Scraper - Setup

echo ============================================================================
echo    TEXAS ROOFING SCRAPER - ONE-TIME SETUP
echo ============================================================================
echo.
echo This will install all required libraries. Please wait...
echo.
echo ============================================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed or not in PATH!
    echo.
    echo Please install Python first:
    echo 1. Go to https://www.python.org/downloads/
    echo 2. Download and run the installer
    echo 3. CHECK THE BOX: "Add Python to PATH"
    echo 4. Run this setup file again
    echo.
    pause
    exit /b 1
)

echo [Step 1/3] Python found! Installing libraries...
echo.

REM Install required Python packages
python -m pip install --upgrade pip
python -m pip install playwright pandas openpyxl tqdm

if errorlevel 1 (
    echo.
    echo [ERROR] Failed to install Python libraries!
    echo Please check your internet connection and try again.
    echo.
    pause
    exit /b 1
)

echo.
echo ============================================================================
echo [Step 2/3] Installing Playwright browser (this may take 3-5 minutes)...
echo ============================================================================
echo.

REM Install Playwright browsers
python -m playwright install chromium

if errorlevel 1 (
    echo.
    echo [ERROR] Failed to install Playwright browser!
    echo Please check your internet connection and try again.
    echo.
    pause
    exit /b 1
)

echo.
echo ============================================================================
echo [Step 3/3] Verifying installation...
echo ============================================================================
echo.

REM Verify installations
python -c "import playwright; import pandas; import openpyxl; import tqdm; print('All libraries installed successfully!')"

if errorlevel 1 (
    echo.
    echo [ERROR] Verification failed!
    echo Some libraries may not have installed correctly.
    echo.
    pause
    exit /b 1
)

echo.
echo ============================================================================
echo                           SETUP COMPLETE!
echo ============================================================================
echo.
echo [SUCCESS] Everything is installed and ready to go!
echo.
echo Next steps:
echo   1. Close this window
echo   2. Double-click "RUN_DEMO.bat" to test (quick 10-15 min run)
echo   3. Or double-click "RUN_FULL_SCRAPER.bat" for the full scan (2-4 hours)
echo.
echo ============================================================================
echo.
pause
