@echo off
REM ============================================================================
REM Texas Roofing Scraper - FULL VERSION
REM ============================================================================
REM This runs the COMPLETE scraper with all 150+ zip codes.
REM Expected runtime: 2-4 HOURS (best run overnight!)
REM ============================================================================

color 0E
title Texas Roofing Scraper - FULL VERSION

echo ============================================================================
echo    TEXAS ROOFING SCRAPER - FULL VERSION
echo ============================================================================
echo.
echo [WARNING] This is the FULL scraper with 150+ zip codes!
echo.
echo Expected runtime: 2-4 HOURS
echo Recommendation: Run overnight or during the day while you work
echo.
echo Cities: Houston, Dallas, Austin, San Antonio, Fort Worth
echo Zip codes: ~30 per city (150+ total)
echo.
echo A Chrome browser window will open - this is normal!
echo DO NOT CLOSE the browser or this window while running.
echo.
echo ============================================================================
echo.
echo Are you sure you want to start the FULL scan?
echo.
echo Press any key to START, or close this window to cancel...
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

REM Check if script exists
if not exist "texas_roofing_scraper.py" (
    echo [ERROR] Main script not found!
    echo Please make sure texas_roofing_scraper.py is in this folder.
    echo.
    pause
    exit /b 1
)

echo.
echo ============================================================================
echo                    STARTING FULL SCRAPER...
echo                    (This will take 2-4 hours)
echo ============================================================================
echo.
echo Started at: %TIME%
echo.

REM Run the full scraper
python texas_roofing_scraper.py

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
    echo   4. Try the demo version first: RUN_DEMO.bat
    echo.
) else (
    echo.
    echo ============================================================================
    echo                    FULL SCAN COMPLETE!
    echo ============================================================================
    echo.
    echo Started at: %TIME%
    echo.
    echo Your results are saved in: texas_roofing_leads.xlsx
    echo.
    echo Open the Excel file to see all your leads organized by tier!
    echo.
)

echo ============================================================================
echo.
echo Press any key to close this window...
pause >nul
