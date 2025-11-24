#!/bin/bash

# Startup script for Excel Reconciliation Tool
# This script activates the virtual environment and runs the Streamlit app

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

# Activate virtual environment
source "$SCRIPT_DIR/venv/bin/activate"

# Set environment variables
export STREAMLIT_SERVER_PORT=8501
export STREAMLIT_SERVER_ADDRESS=0.0.0.0
export STREAMLIT_SERVER_HEADLESS=true
export STREAMLIT_BROWSER_GATHER_USAGE_STATS=false

# Run Streamlit app
exec streamlit run "$SCRIPT_DIR/app.py" \
    --server.port=${STREAMLIT_SERVER_PORT} \
    --server.address=${STREAMLIT_SERVER_ADDRESS} \
    --server.headless=${STREAMLIT_SERVER_HEADLESS} \
    --browser.gatherUsageStats=${STREAMLIT_BROWSER_GATHER_USAGE_STATS}

