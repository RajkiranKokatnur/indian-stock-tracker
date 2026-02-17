#!/bin/bash
# Stock Tracker Quick Start Script for Linux/Mac
# Run with: bash run_tracker.sh or ./run_tracker.sh (after chmod +x)

echo "========================================"
echo "Stock Movement Tracker - Quick Start"
echo "========================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed"
    echo "Please install Python 3.8+ first"
    exit 1
fi

echo "[1/3] Checking dependencies..."
if ! python3 -c "import yfinance" 2>/dev/null; then
    echo "Installing dependencies..."
    pip3 install -r requirements.txt
else
    echo "Dependencies already installed"
fi

echo ""
echo "[2/3] Running stock tracker..."
echo ""
python3 stock_tracker.py

echo ""
echo "[3/3] Generating visualizations..."
echo ""
python3 visualize_trends.py

echo ""
echo "========================================"
echo "COMPLETE! Check the generated files."
echo "========================================"
