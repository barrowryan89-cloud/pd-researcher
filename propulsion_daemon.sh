#!/bin/bash
# Continuous Propulsion Daemon
# Spawns autonomous work sessions every 30 minutes toward $1M goal

WORKSPACE="/home/barrowryan89/.openclaw/workspace"
LOG_FILE="$WORKSPACE/logs/propulsion.log"

# Ensure log directory exists
mkdir -p "$WORKSPACE/logs"

echo "[$(date -u +%Y-%m-%dT%H:%M:%SZ)] Propulsion heartbeat" >> "$LOG_FILE"

# The prompt is executed via cron, this script is for manual triggering if needed
echo "Propulsion engine running. Check cron jobs for schedule."
echo "Last run: $(date -u)"
