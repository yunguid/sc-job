#!/bin/bash

# Path to your project directory
PROJECT_DIR="$(dirname "$0")"

# Path to your virtual environment
VENV_PATH="$PROJECT_DIR/env"

# Path to your folder_monitor.py script
SCRIPT_PATH="$PROJECT_DIR/folder_monitor.py"

# Check if the script exists
if [ ! -f "$SCRIPT_PATH" ]; then
    echo "Error: folder_monitor.py not found at $SCRIPT_PATH"
    exit 1
fi

# Check if the virtual environment exists
if [ ! -d "$VENV_PATH" ]; then
    echo "Error: Virtual environment not found at $VENV_PATH"
    exit 1
fi

# Activate the virtual environment and run the script
source "$VENV_PATH/bin/activate" && python3 "$SCRIPT_PATH"

# Deactivate the virtual environment when the script exits
deactivate
