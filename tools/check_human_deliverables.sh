#!/bin/bash
# Check for completed human deliverables

echo "🔍 Checking Human Hire Status"
echo "=============================="
echo ""

cat ~/.openclaw/workspace/rentahuman_bookings.json | grep -E '"status"|"task"|"human"' | head -30

echo ""
echo "No active human tasks."
echo ""
echo "Auto-check again in 12 hours."
