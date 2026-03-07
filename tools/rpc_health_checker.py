#!/usr/bin/env python3
"""
Solana RPC Health Checker
Check RPC endpoint status and latency
"""

import sys
import time

try:
    import requests
except ImportError:
    print("⚠️  requests not installed. Install with: pip install requests")
    sys.exit(1)

RPC_ENDPOINTS = {
    "Public": "https://api.mainnet-beta.solana.com",
    "Helius": "https://mainnet.helius-rpc.com/",
    "QuickNode": "https://api.quicknode.com/",
    "Ankr": "https://rpc.ankr.com/solana",
}

def check_rpc(name, url):
    """Check RPC endpoint health"""
    try:
        start = time.time()
        response = requests.post(
            url,
            headers={"Content-Type": "application/json"},
            json={"jsonrpc": "2.0", "id": 1, "method": "getHealth"},
            timeout=10
        )
        latency = (time.time() - start) * 1000  # ms
        
        if response.status_code == 200:
            data = response.json()
            if "result" in data:
                return {
                    "status": "✅ Healthy",
                    "latency": f"{latency:.0f}ms",
                    "block_height": data.get("result", "unknown")
                }
            else:
                return {"status": "⚠️  Error", "latency": f"{latency:.0f}ms", "error": data.get("error")}
        else:
            return {"status": "❌ Down", "latency": "N/A", "error": f"HTTP {response.status_code}"}
    except Exception as e:
        return {"status": "❌ Error", "latency": "N/A", "error": str(e)}

def main():
    print("🔌 Solana RPC Health Checker")
    print("=" * 50)
    print()
    
    for name, url in RPC_ENDPOINTS.items():
        print(f"Checking {name}...", end=" ", flush=True)
        result = check_rpc(name, url)
        print(f"{result['status']} ({result['latency']})")
    
    print()
    print("💡 Tip: For airdrop farming, use a dedicated RPC like Helius")
    print("   Free tier: 100k requests/day")
    print("   Sign up: helius.xyz")

if __name__ == "__main__":
    main()
