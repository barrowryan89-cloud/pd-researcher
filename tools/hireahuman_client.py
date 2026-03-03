#!/usr/bin/env python3
"""
HireAHuman.ai Client
Generates payment requests for human tasks.
Budget: $100 (Approved by Ryan)
"""

import json
import os
import time

BUDGET_LIMIT = 100.00
REQUESTS_FILE = "/home/barrowryan89/.openclaw/workspace/hireahuman_requests.json"

def create_request(title, description, amount, urgency="normal"):
    """Create a payment request for Ryan to approve"""
    requests = []
    if os.path.exists(REQUESTS_FILE):
        with open(REQUESTS_FILE) as f:
            requests = json.load(f)
            
    # Check budget
    spent = sum(r.get("amount", 0) for r in requests if r.get("status") in ["approved", "pending"])
    if spent + amount > BUDGET_LIMIT:
        print(f"❌ Budget exceeded. Spent: ${spent}, Requested: ${amount}, Limit: ${BUDGET_LIMIT}")
        return False
        
    request = {
        "id": int(time.time()),
        "title": title,
        "description": description,
        "amount": amount,
        "urgency": urgency,
        "status": "pending",
        "created_at": time.time()
    }
    
    requests.append(request)
    with open(REQUESTS_FILE, 'w') as f:
        json.dump(requests, f, indent=2)
        
    print(f"✅ Request created: {title} (${amount})")
    print(f"   Status: Pending Approval (6 PM Window)")
    return True

def list_pending():
    if not os.path.exists(REQUESTS_FILE):
        print("No pending requests.")
        return
        
    with open(REQUESTS_FILE) as f:
        requests = json.load(f)
        
    pending = [r for r in requests if r["status"] == "pending"]
    if not pending:
        print("No pending requests.")
        return
        
    print(f"📋 Pending Approvals ({len(pending)}):")
    for r in pending:
        print(f"  [${r['amount']}] {r['title']} ({r['urgency']})")

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "create":
        # Usage: create "Title" "Desc" Amount
        create_request(sys.argv[2], sys.argv[3], float(sys.argv[4]))
    elif len(sys.argv) > 1 and sys.argv[1] == "list":
        list_pending()
    else:
        print("Usage: python3 hireahuman_client.py create <title> <desc> <amount> | list")
