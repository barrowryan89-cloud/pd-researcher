#!/usr/bin/env python3
"""
Crypto Wallet Monitor - Free Tool
Check Solana wallet balance and recent transactions
Free version: Basic balance check
Paid upgrade: Multi-wallet, alerts, transaction analysis, token tracking

Usage: python3 wallet_monitor_free.py [address]
"""

import sys
import urllib.request
import json

def get_wallet_info(address):
    """Get wallet info from Helius API (public endpoint)"""
    # Using public Solana RPC via Helius
    url = f"https://api.helius.xyz/v0/addresses/?api-key=helius-public&address={address}"
    
    try:
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req, timeout=10) as response:
            return json.loads(response.read().decode())
    except:
        # Fallback: try simple balance check via public RPC
        return check_balance_fallback(address)

def check_balance_fallback(address):
    """Fallback balance check"""
    rpc_url = "https://api.mainnet-beta.solana.com"
    
    data = json.dumps({
        "jsonrpc": "2.0",
        "id": 1,
        "method": "getBalance",
        "params": [address]
    }).encode()
    
    try:
        req = urllib.request.Request(
            rpc_url,
            data=data,
            headers={'Content-Type': 'application/json'},
            method='POST'
        )
        with urllib.request.urlopen(req, timeout=10) as response:
            result = json.loads(response.read().decode())
            if 'result' in result and 'value' in result['result']:
                lamports = result['result']['value']
                sol = lamports / 1e9
                return {'sol_balance': sol, 'lamports': lamports}
    except Exception as e:
        return {'error': str(e)}
    
    return {'error': 'Could not fetch balance'}

def print_banner():
    print("""
╔════════════════════════════════════════════════════════════╗
║                 CRYPTO WALLET MONITOR v1.0                 ║
║              Free Tool by Sand Street Holdings             ║
╠════════════════════════════════════════════════════════════╣
║  Check Solana wallet balances and transactions             ║
║                                                            ║
║  💎 Want more power?                                       ║
║     → Multi-wallet tracking                                ║
║     → Transaction alerts (webhooks)                        ║
║     → Token balance tracking (USDC, etc.)                  ║
║     → Price feeds and portfolio value                      ║
║     → NFT tracking                                         ║
║     → Check out PD_Researcher v1 ($29)                     ║
║        Solana: FEKY6bDoqBnsQZVT3XbEYS4b1DJ8QoA64G5hXycfTAhQ ║
╚════════════════════════════════════════════════════════════╝
""")

def main():
    print_banner()
    
    # Default to PD_Researcher wallet
    default_address = "FEKY6bDoqBnsQZVT3XbEYS4b1DJ8QoA64G5hXycfTAhQ"
    
    address = sys.argv[1] if len(sys.argv) > 1 else default_address
    
    print(f"🔄 Checking wallet: {address}\n")
    
    result = get_wallet_info(address)
    
    if 'error' in result:
        print(f"❌ Error: {result['error']}")
        sys.exit(1)
    
    print(f"{'='*60}")
    print(f"💰 WALLET INFO")
    print(f"{'='*60}\n")
    
    if 'sol_balance' in result:
        print(f"Address: {address}")
        print(f"Balance: {result['sol_balance']:.9f} SOL")
        print(f"         ({result['lamports']:,} lamports)")
        
        # Rough USD estimate (would need price feed for accuracy)
        usd_estimate = result['sol_balance'] * 95  # Approximate
        print(f"         ~${usd_estimate:.2f} USD (estimated)")
    else:
        print(json.dumps(result, indent=2))
    
    print(f"\n{'='*60}")
    print("\n💡 Want transaction alerts and token tracking?")
    print("   Upgrade to PD_Researcher v1 for advanced wallet monitoring")
    print("   Pay with crypto: FEKY6bDoqBnsQZVT3XbEYS4b1DJ8QoA64G5hXycfTAhQ")
    print(f"\n🔒 Holding significant crypto? Secure it with a hardware wallet:")
    print("   Shop Ledger Nano → https://shop.ledger.com/?r=pdresearcher [affiliate]")
    print("="*60)

if __name__ == "__main__":
    main()
