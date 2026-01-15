@echo off
REM ============================================================================
REM Texas Roofing Scraper - SINGLE CITY SELECTOR
REM ============================================================================
REM Choose ONE city to focus on and scan all its zip codes.
REM This version shows VERBOSE output so you can see tier classification!
REM ============================================================================

color 0C
title Texas Roofing Scraper - Single City Version

echo ============================================================================
echo    TEXAS ROOFING SCRAPER - SINGLE CITY VERSION
echo ============================================================================
echo.
echo This version:
echo   ✓ Lets you choose ONE city to focus on
echo   ✓ Scans all zip codes for that city
echo   ✓ Shows VERBOSE logging (you'll see tier classification happen!)
echo   ✓ Perfect for focused prospecting in one market
echo.
echo You'll be able to see:
echo   - Which websites are being checked
echo   - Which keywords are found
echo   - Why each lead is classified as Tier 1, 2, or 3
echo.
echo ============================================================================
echo.
echo Press any key to start...
pause >nul

cd /d "%~dp0"

python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python not found!
    echo Please run SETUP.bat first.
    echo.
    pause
    exit /b 1
)

if not exist "texas_roofing_single_city.py" (
    echo [ERROR] Script not found!
    echo Please make sure texas_roofing_single_city.py is in this folder.
    echo.
    pause
    exit /b 1
)

echo.
echo ============================================================================
echo                    STARTING SINGLE CITY SCRAPER...
echo ============================================================================
echo.

python texas_roofing_single_city.py

if errorlevel 1 (
    echo.
    echo ============================================================================
    echo [ERROR] Scraper encountered an error!
    echo ============================================================================
    echo.
) else (
    echo.
    echo ============================================================================
    echo                        SCRAPING COMPLETE!
    echo ============================================================================
    echo.
    echo Your results are saved in: [city]_roofing_leads.xlsx
    echo.
)

echo ============================================================================
echo.
pause
