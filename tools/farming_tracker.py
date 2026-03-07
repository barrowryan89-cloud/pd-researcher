#!/usr/bin/env python3
"""
Airdrop Farming Tracker
Tracks your farming activity across protocols
"""

import json
import os
from datetime import datetime
from typing import Dict, List

DATA_FILE = os.path.expanduser("~/.openclaw/workspace/logs/farming_tracker.json")

def load_data() -> Dict:
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    return {"wallets": {}, "protocols": {}, "history": []}

def save_data(data: Dict):
    os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=2)

def add_wallet(data: Dict, name: str, address: str):
    data["wallets"][name] = {
        "address": address,
        "added": datetime.now().isoformat(),
        "protocols": {}
    }
    print(f"✅ Added wallet: {name}")

def log_interaction(data: Dict, wallet: str, protocol: str, action: str, amount: float = 0):
    entry = {
        "timestamp": datetime.now().isoformat(),
        "wallet": wallet,
        "protocol": protocol,
        "action": action,
        "amount": amount
    }
    data["history"].append(entry)
    
    # Update wallet's protocol tracking
    if wallet in data["wallets"]:
        if protocol not in data["wallets"][wallet]["protocols"]:
            data["wallets"][wallet]["protocols"][protocol] = []
        data["wallets"][wallet]["protocols"][protocol].append(entry)
    
    print(f"📝 Logged: {action} on {protocol} ({wallet})")

def show_status(data: Dict):
    print("\n🚜 Airdrop Farming Status")
    print("=" * 50)
    
    print(f"\n📊 Wallets: {len(data['wallets'])}")
    for name, info in data["wallets"].items():
        print(f"  • {name}: {info['address'][:20]}...")
        print(f"    Protocols: {', '.join(info.get('protocols', {}).keys()) or 'None'}")
    
    print(f"\n📈 Total Interactions: {len(data['history'])}")
    
    if data['history']:
        print("\n🕐 Recent Activity:")
        for entry in data['history'][-5:]:
            print(f"  {entry['timestamp'][:10]}: {entry['action']} on {entry['protocol']}")

def main():
    data = load_data()
    
    import sys
    
    if len(sys.argv) < 2:
        show_status(data)
        print("\nUsage:")
        print("  farming_tracker.py add <wallet_name> <address>")
        print("  farming_tracker.py log <wallet> <protocol> <action> [amount]")
        print("  farming_tracker.py status")
        return
    
    cmd = sys.argv[1]
    
    if cmd == "add" and len(sys.argv) >= 4:
        add_wallet(data, sys.argv[2], sys.argv[3])
    elif cmd == "log" and len(sys.argv) >= 5:
        amount = float(sys.argv[5]) if len(sys.argv) >= 6 else 0
        log_interaction(data, sys.argv[2], sys.argv[3], sys.argv[4], amount)
    elif cmd == "status":
        show_status(data)
    else:
        print("Invalid command")
    
    save_data(data)

if __name__ == "__main__":
    main()
