@echo off
REM ============================================================================
REM Texas Roofing Scraper - DEMO VERSION (Quick Test)
REM ============================================================================
REM This runs the DEMO version with only 3 zip codes per city.
REM Perfect for testing! Takes about 10-15 minutes.
REM ============================================================================

color 0B
title Texas Roofing Scraper - DEMO VERSION

echo ============================================================================
echo    TEXAS ROOFING SCRAPER - DEMO VERSION
echo ============================================================================
echo.
echo This will run a QUICK TEST with only 3 zip codes per city.
echo Expected runtime: 10-15 minutes
echo.
echo Cities: Houston, Dallas, Austin (3 zips each)
echo.
echo A Chrome browser window will open - this is normal!
echo DO NOT CLOSE the browser or this window while running.
echo.
echo ============================================================================
echo.
echo Press any key to start the demo scraper...
pause >nul

REM Change to script directory
cd /d "%~dp0"

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python not found!
    echo Please run SETUP.bat first to install Python and required libraries.
    echo.
    pause
    exit /b 1
)

REM Check if demo script exists
if not exist "texas_roofing_scraper_DEMO.py" (
    echo [ERROR] Demo script not found!
    echo Please make sure texas_roofing_scraper_DEMO.py is in this folder.
    echo.
    pause
    exit /b 1
)

echo.
echo ============================================================================
echo                        STARTING DEMO SCRAPER...
echo ============================================================================
echo.

REM Run the demo scraper
python texas_roofing_scraper_DEMO.py

REM Check if it completed successfully
if errorlevel 1 (
    echo.
    echo ============================================================================
    echo [ERROR] Scraper encountered an error!
    echo ============================================================================
    echo.
    echo Common solutions:
    echo   1. Make sure you ran SETUP.bat first
    echo   2. Check your internet connection
    echo   3. Try running SETUP.bat again
    echo.
) else (
    echo.
    echo ============================================================================
    echo                        DEMO COMPLETE!
    echo ============================================================================
    echo.
    echo Your results are saved in: texas_roofing_leads_DEMO.xlsx
    echo.
    echo Ready for the full version?
    echo Double-click "RUN_FULL_SCRAPER.bat" to scan all 150+ zip codes!
    echo.
)

echo ============================================================================
echo.
pause
