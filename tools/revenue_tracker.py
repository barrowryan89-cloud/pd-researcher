#!/usr/bin/env python3
"""
Autonomous Revenue Tracker
Monitors affiliate revenue, crypto payments, and other income streams
"""

import json
import os
from datetime import datetime

REVENUE_LOG = "/home/barrowryan89/.openclaw/workspace/revenue_log.json"

def log_revenue(source, amount, currency="USD", notes=""):
    """Log a revenue event"""
    entry = {
        "timestamp": datetime.now().isoformat(),
        "source": source,
        "amount": amount,
        "currency": currency,
        "notes": notes
    }
    
    # Load existing log
    data = []
    if os.path.exists(REVENUE_LOG):
        with open(REVENUE_LOG) as f:
            data = json.load(f)
    
    data.append(entry)
    
    # Save
    with open(REVENUE_LOG, 'w') as f:
        json.dump(data, f, indent=2)
    
    return entry

def get_revenue_summary(days=30):
    """Get revenue summary for last N days"""
    if not os.path.exists(REVENUE_LOG):
        return {"total": 0, "by_source": {}}
    
    with open(REVENUE_LOG) as f:
        data = json.load(f)
    
    from datetime import timedelta
    cutoff = datetime.now() - timedelta(days=days)
    
    total = 0
    by_source = {}
    
    for entry in data:
        entry_date = datetime.fromisoformat(entry["timestamp"])
        if entry_date >= cutoff:
            amount = entry["amount"]
            total += amount
            source = entry["source"]
            by_source[source] = by_source.get(source, 0) + amount
    
    return {
        "total": round(total, 2),
        "by_source": by_source,
        "period_days": days
    }

def check_wallet():
    """Check Solana wallet for new payments"""
    wallet = "FEKY6bDoqBnsQZVT3XbEYS4b1DJ8QoA64G5hXycfTAhQ"
    # Placeholder - would need Solana RPC integration
    return {"balance": 0, "wallet": wallet}

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "summary":
        summary = get_revenue_summary()
        print(f"Revenue (last {summary['period_days']} days):")
        print(f"  Total: ${summary['total']}")
        for source, amount in summary['by_source'].items():
            print(f"  {source}: ${amount}")
    else:
        wallet = check_wallet()
        print(f"Wallet: {wallet['wallet']}")
        print(f"Balance: {wallet['balance']} SOL")
        print(f"\nRun with 'summary' arg for revenue report")
