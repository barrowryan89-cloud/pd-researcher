#!/usr/bin/env python3
"""
Airdrop Farming Tracker Pro
Track your farming positions across Solana protocols
"""

import json
import os
from datetime import datetime, timedelta

DB_FILE = "farming_positions.json"

class FarmingTracker:
    def __init__(self):
        self.positions = self.load_positions()
    
    def load_positions(self):
        if os.path.exists(DB_FILE):
            with open(DB_FILE) as f:
                return json.load(f)
        return {}
    
    def save_positions(self):
        with open(DB_FILE, 'w') as f:
            json.dump(self.positions, f, indent=2)
    
    def add_position(self, protocol, wallet, amount, token):
        key = f"{protocol}_{wallet}"
        self.positions[key] = {
            "protocol": protocol,
            "wallet": wallet,
            "amount": amount,
            "token": token,
            "start_date": datetime.now().isoformat(),
            "last_check": datetime.now().isoformat()
        }
        self.save_positions()
        print(f"✅ Added: {protocol} - {wallet} - {amount} {token}")
    
    def check_positions(self):
        print("\n📊 FARMING POSITIONS")
        print("=" * 50)
        for key, pos in self.positions.items():
            days = (datetime.now() - datetime.fromisoformat(pos["start_date"])).days
            print(f"\n{pos['protocol']}:")
            print(f"  Wallet: {pos['wallet'][:8]}...{pos['wallet'][-4:]}")
            print(f"  Amount: {pos['amount']} {pos['token']}")
            print(f"  Days farming: {days}")
    
    def estimate_airdrop(self, protocol, token_price=1.0):
        """Estimate potential airdrop value"""
        positions = [p for p in self.positions.values() if p["protocol"] == protocol]
        total_value = sum(p["amount"] for p in positions)
        
        # Conservative estimate: 5-15% of deposited value
        low_estimate = total_value * 0.05 * token_price
        high_estimate = total_value * 0.15 * token_price
        
        print(f"\n🎯 {protocol} Airdrop Estimate:")
        print(f"  Total deposited: {total_value}")
        print(f"  Estimated airdrop: ${low_estimate:.2f} - ${high_estimate:.2f}")
        
        return low_estimate, high_estimate

if __name__ == "__main__":
    import sys
    tracker = FarmingTracker()
    
    if len(sys.argv) < 2:
        print("Usage:")
        print("  farming_tracker.py add <protocol> <wallet> <amount> <token>")
        print("  farming_tracker.py check")
        print("  farming_tracker.py estimate <protocol> [token_price]")
        sys.exit(1)
    
    cmd = sys.argv[1]
    
    if cmd == "add":
        tracker.add_position(sys.argv[2], sys.argv[3], float(sys.argv[4]), sys.argv[5])
    elif cmd == "check":
        tracker.check_positions()
    elif cmd == "estimate":
        price = float(sys.argv[3]) if len(sys.argv) > 3 else 1.0
        tracker.estimate_airdrop(sys.argv[2], price)
