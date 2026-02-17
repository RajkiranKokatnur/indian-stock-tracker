#!/bin/bash
# Launch Stock Movement Dashboard

echo "========================================"
echo "Stock Movement Dashboard"
echo "========================================"
echo ""
echo "Starting dashboard on http://localhost:8501"
echo "Press Ctrl+C to stop"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed"
    exit 1
fi

# Check if Streamlit is installed
if ! python3 -c "import streamlit" 2>/dev/null; then
    echo "Installing Streamlit..."
    pip3 install streamlit plotly
fi

# Launch dashboard
streamlit run dashboard.py
