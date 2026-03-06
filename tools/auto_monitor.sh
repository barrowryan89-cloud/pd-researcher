#!/bin/bash
# Self-monitoring script - runs every 30 min

while true; do
    echo "=== $(date) ===" >> /tmp/pd_monitor.log
    
    # Check farming
    cd /home/barrowryan89/.openclaw/workspace
    source .venv/bin/activate
    python tools/farming_v2.py >> /tmp/pd_monitor.log 2>&1
    
    # Check balances
    echo "Checking balances..." >> /tmp/pd_monitor.log
    
    # Build more content
    echo "Building SEO content..." >> /tmp/pd_monitor.log
    
    echo "Cycle complete. Sleeping 30 min..." >> /tmp/pd_monitor.log
    sleep 1800
done
