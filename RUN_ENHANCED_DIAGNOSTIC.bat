@echo off
REM ============================================================================
REM Enhanced Google Maps Diagnostic
REM ============================================================================
REM This will try MULTIPLE ways to find the search box and tell you which works
REM ============================================================================

color 0D
title Enhanced Google Maps Diagnostic

echo ============================================================================
echo    ENHANCED GOOGLE MAPS DIAGNOSTIC
echo ============================================================================
echo.
echo This will:
echo   1. Try 9 different ways to find the search box
echo   2. Show you which one works
echo   3. Test if search actually works
echo   4. Take screenshots at each step
echo   5. Tell you exactly what to fix
echo.
echo This is more thorough than the basic test!
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

echo.
echo ============================================================================
echo                    RUNNING ENHANCED DIAGNOSTIC...
echo ============================================================================
echo.

python diagnostic_enhanced.py

echo.
echo ============================================================================
echo.
echo Check the screenshots in this folder!
echo   - diagnostic_1_initial.png (what the page looks like)
echo   - diagnostic_2_typed.png (if it found the search box)
echo   - diagnostic_3_results.png (if search worked)
echo.
echo The diagnostic will tell you which selector works!
echo.
echo ============================================================================
echo.
pause
