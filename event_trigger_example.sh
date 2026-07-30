#!/bin/bash
# ==============================================================================
#  event_trigger_example.sh — Demonstrates event-driven automation
# ==============================================================================
#  Use this pattern when an automated system event completes (e.g., build finished,
#  test suite passed, daily pipeline complete) to push new numbers into your deck.
# ==============================================================================

PROJECT_DIR="/usr/local/google/home/jasminesummers/Documents/test/slides_updater"
cd "$PROJECT_DIR" || exit 1

# 1. Capture dynamic values from your system event
CURRENT_TIME=$(date -u +"%Y-%m-%d %H:%M UTC")
NEW_STATUS="All automated tests passed (100% success rate)"
NEW_METRIC="42ms avg latency"

echo "⚡ Event received at $CURRENT_TIME! Updating slide config..."

# 2. Update config.json with fresh values
cat << EOF > config.json
{
  "presentation_id": "1vv-PqZtuvxPAGcJothd_o-T4g4xOZ4SEFK-8lYEbNhw",
  "placeholders": {
    "{{PROJECT_NAME}}": "Event-Driven Automated Project",
    "{{LAST_UPDATED}}": "$CURRENT_TIME",
    "{{STATUS_SUMMARY}}": "$NEW_STATUS",
    "{{METRIC_KEY_PERFORMANCE}}": "$NEW_METRIC",
    "{{METRIC_TOTAL_TASKS}}": "$(($(date +%s) % 5000))"
  }
}
EOF

# 3. Trigger the Slides API update
./run_update.sh
