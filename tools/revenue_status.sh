#!/bin/bash
# Quick Revenue Status Check
# Usage: ./revenue_status.sh

echo "💰 REVENUE STATUS CHECK"
echo "======================="
echo ""

# Count assets
echo "📊 Assets Created:"
echo "  Landing pages: $(ls -1 *.html 2>/dev/null | wc -l)"
echo "  Content pieces: $(ls -1 content/*.md content/*.txt 2>/dev/null | wc -l)"
echo "  Tools: $(ls -1 tools/*.py tools/*.sh 2>/dev/null | wc -l)"
echo ""

# Wallets
echo "💼 Wallets:"
echo "  BTC: bc1qq0eanq0cj79jrz59nswdyae2zl7f24u5lse8mj"
echo "  SOL: FEKY6bDoqBnsQZVT3XbEYS4b1DJ8QoA64G5hXycfTAhQ"
echo "  Farm wallets: $(ls -1 keys/airdrop_wallets/*.json 2>/dev/null | wc -l)"
echo ""

# Products
echo "🛍️ Products:"
echo "  • Airdrop Farming Guide — $9"
echo "  • AI Agent Security Audit — $49"
echo "  • Complete Bundle — $29"
echo "  • Free Tools — Lead magnet"
echo ""

# Pending
echo "⏳ Pending Human Deliverables:"
echo "  • 3 tool icons (John Siesta)"
echo "  • 5 social graphics (vsevolod eremkin)"
echo "  • 3 affiliate apps (Michael Corrales)"
echo ""

# Blockers
echo "🚧 Blockers:"
echo "  • Need 1 SOL for airdrop farming"
echo "  • Need traffic for product sales"
echo ""

echo "Next: Get SOL funding or post content to drive sales"
