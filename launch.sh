#!/bin/bash
# Launcher script for auto-starting the GUI

# Navigate to script directory
cd "$(dirname "$0")"

# Set display (if running from boot)
export DISPLAY=:0

# Run the application
python3 heart_sound_classifier.py

# If app crashes, wait before allowing restart
sleep 5
