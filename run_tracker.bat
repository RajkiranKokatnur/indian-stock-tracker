@echo off
REM Stock Tracker Quick Start Script for Windows
REM Double-click this file to run

echo ========================================
echo Stock Movement Tracker - Quick Start
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8+ from python.org
    pause
    exit /b 1
)

echo [1/3] Checking dependencies...
pip show yfinance >nul 2>&1
if errorlevel 1 (
    echo Installing dependencies...
    pip install -r requirements.txt
) else (
    echo Dependencies already installed
)

echo.
echo [2/3] Running stock tracker...
echo.
python stock_tracker.py

echo.
echo [3/3] Generating visualizations...
echo.
python visualize_trends.py

echo.
echo ========================================
echo COMPLETE! Check the generated files.
echo ========================================
pause
