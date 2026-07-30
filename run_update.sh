#!/bin/bash
# ==============================================================================
#  run_update.sh — One-click runner for Google Slides auto-updates
# ==============================================================================
#  Run this script whenever you want to push new events/data into your deck:
#    ./run_update.sh
# ==============================================================================

PROJECT_DIR="/usr/local/google/home/jasminesummers/Documents/Insights Wizard"
cd "$PROJECT_DIR" || exit 1

echo "🔄 Triggering Google Slides Update Event..."
python3 update_slides.py "$@"
