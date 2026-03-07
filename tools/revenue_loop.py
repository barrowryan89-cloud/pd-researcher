#!/usr/bin/env python3
"""
Revenue Loop Reminder
Triggers the "how can I make money" mindset check
"""

import os
import json
from datetime import datetime

WALLET_BTC = "bc1qq0eanq0cj79jrz59nswdyae2zl7f24u5lse8mj"
WALLET_SOL = "FEKY6bDoqBnsQZVT3XbEYS4b1DJ8QoA64G5hXycfTAhQ"

def log_revenue_check(action_taken=""):
    """Log that the revenue question was asked and what action was taken"""
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "question_asked": "How can I make money right now?",
        "action_taken": action_taken
    }
    
    log_file = os.path.expanduser("~/.openclaw/workspace/logs/revenue_loop.jsonl")
    os.makedirs(os.path.dirname(log_file), exist_ok=True)
    
    with open(log_file, "a") as f:
        f.write(json.dumps(log_entry) + "\n")
    
    return log_entry

def get_revenue_stats():
    """Get stats on revenue loop adherence"""
    log_file = os.path.expanduser("~/.openclaw/workspace/logs/revenue_loop.jsonl")
    
    if not os.path.exists(log_file):
        return {"checks_today": 0, "total_checks": 0}
    
    today = datetime.now().strftime("%Y-%m-%d")
    checks_today = 0
    total_checks = 0
    
    with open(log_file, "r") as f:
        for line in f:
            try:
                entry = json.loads(line.strip())
                total_checks += 1
                if entry["timestamp"].startswith(today):
                    checks_today += 1
            except:
                continue
    
    return {
        "checks_today": checks_today,
        "total_checks": total_checks
    }

def get_target_checks():
    return 20  # Every 30 min during 10-hour workday

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "--stats":
        stats = get_revenue_stats()
        target = get_target_checks()
        print(f"Revenue loop checks today: {stats['checks_today']}/{target}")
        print(f"Total checks logged: {stats['total_checks']}")
        print(f"BTC: {WALLET_BTC}")
        print(f"SOL: {WALLET_SOL}")
    else:
        print("💰 REVENUE LOOP TRIGGERED")
        print(f"Question: How can I make money right now?")
        print(f"BTC: {WALLET_BTC}")
        print(f"SOL: {WALLET_SOL}")
        print("\nExecute highest ROI action immediately.")
