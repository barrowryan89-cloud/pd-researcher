#!/bin/bash
# Solana Airdrop Farming - Setup Script
# Run this to install dependencies

echo "🚜 Setting up Solana Airdrop Farming Infrastructure"
echo "==================================================="
echo ""

# Check if Solana CLI is installed
if ! command -v solana &> /dev/null; then
    echo "📦 Installing Solana CLI..."
    sh -c "$(curl -sSfL https://release.solana.com/v1.18.0/install)"
    export PATH="$HOME/.local/share/solana/install/active_release/bin:$PATH"
else
    echo "✅ Solana CLI already installed"
fi

# Install Python dependencies
echo ""
echo "📦 Installing Python dependencies..."
pip3 install --user solders solana asyncio aiohttp 2>/dev/null || pip3 install solders solana asyncio aiohttp --break-system-packages 2>/dev/null || echo "⚠️ Could not install Python packages automatically"

# Set up RPC
export SOLANA_RPC_URL="https://mainnet.helius-rpc.com/?api-key=YOUR_API_KEY_HERE"
echo ""
echo "⚠️  IMPORTANT: Get Helius API key at https://helius.xyz"
echo "   Free tier: 100k requests/month"
echo "   Then update SOLANA_RPC_URL in this script"

echo ""
echo "📊 Farming Wallets Created:"
ls -1 ~/.openclaw/workspace/keys/airdrop_wallets/*.json 2>/dev/null | wc -l | xargs echo "   Total wallets:"

echo ""
echo "💰 NEXT STEPS:"
echo "   1. Fund wallets with SOL (recommend 0.25 SOL each)"
echo "   2. Get Helius API key (free)"
echo "   3. Run: python3 tools/airdrop_farmer.py"
echo "   4. Start with MarginFi + Kamino deposits"
echo ""
echo "🎯 Target Protocols:"
echo "   • MarginFi (lending) - Points live"
echo "   • Kamino (yield) - Points live"  
echo "   • Drift (perps) - Points live"
echo "   • Jupiter (DEX) - Ongoing rounds"
echo "   • JitoSOL (staking) - May do more drops"
echo ""
