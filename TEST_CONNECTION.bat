@echo off
REM ============================================================================
REM Google Maps Connection Test
REM ============================================================================
REM Run this if you're getting timeout errors!
REM It will take screenshots to show you what's blocking the scraper.
REM ============================================================================

color 0D
title Google Maps Connection Test

echo ============================================================================
echo    GOOGLE MAPS CONNECTION TEST
echo ============================================================================
echo.
echo This diagnostic tool will:
echo   1. Open Google Maps
echo   2. Take screenshots of what you see
echo   3. Test if the search box is accessible
echo   4. Tell you what's blocking the scraper
echo.
echo ============================================================================
echo.
echo Press any key to start the test...
pause >nul

REM Change to script directory
cd /d "%~dp0"

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python not found!
    echo Please run SETUP.bat first.
    echo.
    pause
    exit /b 1
)

echo.
echo ============================================================================
echo                        STARTING CONNECTION TEST...
echo ============================================================================
echo.

REM Run the diagnostic script
python test_google_maps_connection.py

echo.
echo ============================================================================
echo.
echo Check the screenshots in this folder to see what's happening!
echo.
echo If you see a CAPTCHA or "I'm not a robot" message, Google is blocking you.
echo If you see a cookie consent dialog, the updated scraper should handle it now.
echo.
echo ============================================================================
echo.
pause
