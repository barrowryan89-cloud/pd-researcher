#!/bin/bash
# Simple Solana Wallet Balance Checker
# Usage: ./solana_balance.sh <WALLET_ADDRESS>

if [ -z "$1" ]; then
    echo "Usage: $0 <WALLET_ADDRESS>"
    echo "Example: $0 FEKY6bDoqBnsQZVT3XbEYS4b1DJ8QoA64G5hXycfTAhQ"
    exit 1
fi

WALLET=$1
RPC_URL="https://api.mainnet-beta.solana.com"

echo "🔍 Checking balance for: $WALLET"
echo ""

# Get SOL balance
BALANCE=$(curl -s -X POST $RPC_URL \
  -H "Content-Type: application/json" \
  -d "{\"jsonrpc\":\"2.0\",\"id\":1,\"method\":\"getBalance\",\"params\":[\"$WALLET\"]}" | \
  grep -o '"lamports":[0-9]*' | cut -d: -f2)

if [ -z "$BALANCE" ]; then
    echo "❌ Error: Could not fetch balance"
    exit 1
fi

# Convert lamports to SOL
SOL=$(echo "scale: 4; $BALANCE / 1000000000" | bc 2>/dev/null || echo "0")
echo "💰 Balance: $SOL SOL"
echo "   ($BALANCE lamports)"
echo ""
echo "📊 USD Value (approx):"
echo "   At \$150/SOL: \$$(echo "$SOL * 150" | bc 2>/dev/null || echo "N/A")"
echo ""
