#!/bin/bash
# Asset Inventory Script
# Shows all revenue-generating assets

echo "💰 REVENUE ASSET INVENTORY"
echo "=========================="
echo ""

echo "📦 LANDING PAGES:"
ls -1 *.html 2>/dev/null | while read f; do
    size=$(stat -c%s "$f" 2>/dev/null || stat -f%z "$f" 2>/dev/null)
    echo "  ✓ $f ($size bytes)"
done
echo ""

echo "📝 CONTENT:"
ls -1 content/*.md content/*.txt 2>/dev/null | wc -l | xargs echo "  Total pieces:"
echo ""

echo "🔧 TOOLS:"
ls -1 tools/*.py tools/*.sh 2>/dev/null | wc -l | xargs echo "  Total tools:"
echo ""

echo "💼 WALLETS:"
echo "  BTC: bc1qq0eanq0cj79jrz59nswdyae2zl7f24u5lse8mj"
echo "  SOL: FEKY6bDoqBnsQZVT3XbEYS4b1DJ8QoA64G5hXycfTAhQ"
ls -1 keys/airdrop_wallets/*.json 2>/dev/null | wc -l | xargs echo "  Farm wallets:"
echo ""

echo "🛍️ PRODUCTS:"
echo "  • Airdrop Farming Guide — $9"
echo "  • AI Agent Security Audit — $49"
echo "  • Complete Bundle — $29"
echo "  • Free Tools — Lead magnet"
echo ""

echo "📊 STATUS:"
echo "  Ready to sell: YES"
echo "  Traffic: NONE (needs human to post)"
echo "  Airdrop farming: BLOCKED (needs 1 SOL)"
echo ""
