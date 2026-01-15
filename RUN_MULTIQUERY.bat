@echo off
REM ============================================================================
REM Texas Roofing Scraper - MULTI-QUERY VERSION
REM ============================================================================
REM Uses MULTIPLE search queries per zip code to find MORE variety!
REM Finds smaller companies and specialists that don't show up in basic searches.
REM ============================================================================

color 0E
title Texas Roofing Scraper - Multi-Query Version

echo ============================================================================
echo    TEXAS ROOFING SCRAPER - MULTI-QUERY VERSION
echo ============================================================================
echo.
echo This version uses MULTIPLE search queries per zip code:
echo   - "Roofing company"
echo   - "Commercial roofing contractor"
echo   - "Roof coating specialist"
echo   - "Roof restoration service"
echo   - And more!
echo.
echo Benefits:
echo   ✓ Finds MORE companies (wider variety)
echo   ✓ Discovers smaller/local businesses
echo   ✓ Targets specialists (more likely Tier 1!)
echo   ✓ Avoids seeing the same big companies repeatedly
echo.
echo Note: This takes longer than single-query version, but finds
echo       much more diverse leads!
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

if not exist "texas_roofing_multiquery.py" (
    echo [ERROR] Script not found!
    echo Please make sure texas_roofing_multiquery.py is in this folder.
    echo.
    pause
    exit /b 1
)

echo.
echo ============================================================================
echo                    STARTING MULTI-QUERY SCRAPER...
echo ============================================================================
echo.

python texas_roofing_multiquery.py

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
    echo Your results are saved in: [city]_roofing_leads_multiquery.xlsx
    echo.
    echo The file includes a "Search Query Used" column showing which
    echo search query found each lead!
    echo.
)

echo ============================================================================
echo.
pause
