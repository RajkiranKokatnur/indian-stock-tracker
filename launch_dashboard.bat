@echo off
REM Launch Stock Movement Dashboard
echo ========================================
echo Stock Movement Dashboard
echo ========================================
echo.
echo Starting dashboard on http://localhost:8501
echo Press Ctrl+C to stop
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    pause
    exit /b 1
)

REM Check if Streamlit is installed
python -c "import streamlit" >nul 2>&1
if errorlevel 1 (
    echo Installing Streamlit...
    pip install streamlit plotly
)

REM Launch dashboard
streamlit run dashboard.py

pause
