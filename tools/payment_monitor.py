#!/usr/bin/env python3
"""
Payment Monitor
Checks for crypto payments and sends notifications
"""

import json
import os
from datetime import datetime

LOG_FILE = os.path.expanduser("~/.openclaw/workspace/logs/payments.jsonl")
WALLETS = {
    "BTC": "bc1qq0eanq0cj79jrz59nswdyae2zl7f24u5lse8mj",
    "SOL": "FEKY6bDoqBnsQZVT3XbEYS4b1DJ8QoA64G5hXycfTAhQ"
}

def log_payment(crypto, amount, tx_hash, product):
    """Log an incoming payment"""
    entry = {
        "timestamp": datetime.now().isoformat(),
        "crypto": crypto,
        "amount": amount,
        "tx_hash": tx_hash,
        "product": product,
        "status": "pending_delivery"
    }
    
    os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
    with open(LOG_FILE, 'a') as f:
        f.write(json.dumps(entry) + '\n')
    
    print(f"💰 Payment logged: {amount} {crypto} for {product}")
    print(f"   TX: {tx_hash}")
    print(f"   Action needed: Deliver {product} to customer")

def show_pending():
    """Show pending payments awaiting delivery"""
    if not os.path.exists(LOG_FILE):
        print("No payments yet")
        return
    
    pending = []
    with open(LOG_FILE, 'r') as f:
        for line in f:
            try:
                entry = json.loads(line.strip())
                if entry.get('status') == 'pending_delivery':
                    pending.append(entry)
            except:
                continue
    
    print(f"\n⏳ Pending Deliveries: {len(pending)}")
    for p in pending:
        print(f"  {p['timestamp'][:10]}: {p['amount']} {p['crypto']} — {p['product']}")
        print(f"    TX: {p['tx_hash']}")

def main():
    import sys
    
    print("💳 Payment Monitor")
    print("=" * 50)
    print("\nMonitored wallets:")
    for crypto, addr in WALLETS.items():
        print(f"  {crypto}: {addr}")
    
    if len(sys.argv) < 2:
        show_pending()
        print("\nUsage:")
        print("  payment_monitor.py log <crypto> <amount> <tx_hash> <product>")
        print("  payment_monitor.py pending")
        return
    
    cmd = sys.argv[1]
    
    if cmd == "log" and len(sys.argv) >= 6:
        log_payment(sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5])
    elif cmd == "pending":
        show_pending()
    else:
        print("Invalid command")

if __name__ == "__main__":
    main()
