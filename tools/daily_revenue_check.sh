#!/bin/bash
# Daily Revenue Check Script
# Run this daily to check status and prompt for actions

echo "💰 DAILY REVENUE CHECK"
echo "====================="
echo ""
echo "Date: $(date)"
echo ""

# Check for payments
echo "📊 Checking for payments..."
python3 ~/.openclaw/workspace/tools/payment_monitor.py pending 2>/dev/null || echo "No payment monitor data"
echo ""

# Check farming status
echo "🚜 Farming Status:"
python3 ~/.openclaw/workspace/tools/farming_tracker.py status 2>/dev/null || echo "No farming data yet"
echo ""

# Show asset count
echo "📦 Assets:"
ls -1 ~/.openclaw/workspace/*.html 2>/dev/null | wc -l | xargs echo "  Landing pages:"
ls -1 ~/.openclaw/workspace/content/*.* 2>/dev/null | wc -l | xargs echo "  Content pieces:"
ls -1 ~/.openclaw/workspace/tools/*.* 2>/dev/null | wc -l | xargs echo "  Tools:"
echo ""

# Daily question
echo "❓ DAILY QUESTION:"
echo "   How can I make money today?"
echo ""
echo "Options:"
echo "  1. Create more content"
echo "  2. Build more tools"
echo "  3. Check human deliverables"
echo "  4. Post to communities (needs human)"
echo ""
