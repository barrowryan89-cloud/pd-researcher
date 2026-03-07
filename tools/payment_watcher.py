#!/usr/bin/env python3
"""
PD Payment Watcher
Monitors Solana wallet for incoming payments and triggers instant fulfillment
"""

import asyncio
import json
import sqlite3
import sys
from datetime import datetime
from pathlib import Path

# Wallet configuration
WALLET_ADDRESS = "FEKY6bDoqBnsQZVT3XbEYS4b1DJ8QoA64G5hXycfTAhQ"
DB_PATH = Path(__file__).parent / "payments.db"

class PaymentWatcher:
    def __init__(self):
        self.init_db()
        
    def init_db(self):
        """Initialize payments database"""
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS payments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                signature TEXT UNIQUE,
                amount_lamports INTEGER,
                amount_sol REAL,
                sender TEXT,
                timestamp TEXT,
                processed BOOLEAN DEFAULT 0,
                fulfillment_sent BOOLEAN DEFAULT 0,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS wallet_balance (
                id INTEGER PRIMARY KEY,
                balance_lamports INTEGER,
                checked_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit()
        conn.close()
    
    def get_balance(self):
        """Get current wallet balance via Solana RPC"""
        import urllib.request
        import ssl
        
        rpc_url = "https://api.mainnet-beta.solana.com"
        payload = json.dumps({
            "jsonrpc": "2.0",
            "id": 1,
            "method": "getBalance",
            "params": [WALLET_ADDRESS]
        }).encode()
        
        req = urllib.request.Request(
            rpc_url,
            data=payload,
            headers={"Content-Type": "application/json"},
            method="POST"
        )
        
        try:
            with urllib.request.urlopen(req, timeout=10) as response:
                data = json.loads(response.read())
                if "result" in data:
                    return data["result"]["value"]
        except Exception as e:
            print(f"Balance check error: {e}")
        return None
    
    def get_recent_transactions(self, limit=10):
        """Get recent transactions for the wallet"""
        import urllib.request
        
        rpc_url = "https://api.mainnet-beta.solana.com"
        payload = json.dumps({
            "jsonrpc": "2.0",
            "id": 1,
            "method": "getSignaturesForAddress",
            "params": [WALLET_ADDRESS, {"limit": limit}]
        }).encode()
        
        req = urllib.request.Request(
            rpc_url,
            data=payload,
            headers={"Content-Type": "application/json"},
            method="POST"
        )
        
        try:
            with urllib.request.urlopen(req, timeout=10) as response:
                data = json.loads(response.read())
                if "result" in data:
                    return data["result"]
        except Exception as e:
            print(f"Transaction fetch error: {e}")
        return []
    
    def get_transaction_details(self, signature):
        """Get detailed transaction info"""
        import urllib.request
        
        rpc_url = "https://api.mainnet-beta.solana.com"
        payload = json.dumps({
            "jsonrpc": "2.0",
            "id": 1,
            "method": "getTransaction",
            "params": [signature, {"encoding": "json", "maxSupportedTransactionVersion": 0}]
        }).encode()
        
        req = urllib.request.Request(
            rpc_url,
            data=payload,
            headers={"Content-Type": "application/json"},
            method="POST"
        )
        
        try:
            with urllib.request.urlopen(req, timeout=10) as response:
                data = json.loads(response.read())
                if "result" in data and data["result"]:
                    return data["result"]
        except Exception as e:
            print(f"Transaction detail error: {e}")
        return None
    
    def check_for_new_payments(self):
        """Check for new incoming payments"""
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # Get known signatures
        cursor.execute("SELECT signature FROM payments")
        known_sigs = {row[0] for row in cursor.fetchall()}
        
        # Get recent transactions
        transactions = self.get_recent_transactions(limit=20)
        new_payments = []
        
        for tx in transactions:
            sig = tx.get("signature")
            if not sig or sig in known_sigs:
                continue
            
            # Check if this is an incoming transfer (not our own outgoing)
            details = self.get_transaction_details(sig)
            if not details:
                continue
            
            # Parse transaction for incoming SOL to our wallet
            meta = details.get("meta", {})
            post_balances = meta.get("postBalances", [])
            pre_balances = meta.get("preBalances", [])
            account_keys = details.get("transaction", {}).get("message", {}).get("accountKeys", [])
            
            # Find our wallet index
            our_index = None
            for i, acc in enumerate(account_keys):
                if acc == WALLET_ADDRESS:
                    our_index = i
                    break
            
            if our_index is not None and len(post_balances) > our_index and len(pre_balances) > our_index:
                balance_change = post_balances[our_index] - pre_balances[our_index]
                if balance_change > 0:  # Incoming payment
                    amount_sol = balance_change / 1e9
                    
                    # Find sender (first account that decreased balance)
                    sender = "unknown"
                    for i, (pre, post) in enumerate(zip(pre_balances, post_balances)):
                        if post < pre and i < len(account_keys):
                            sender = account_keys[i]
                            break
                    
                    # Store payment
                    cursor.execute("""
                        INSERT INTO payments (signature, amount_lamports, amount_sol, sender, timestamp)
                        VALUES (?, ?, ?, ?, ?)
                    """, (sig, balance_change, amount_sol, sender, tx.get("blockTime")))
                    
                    new_payments.append({
                        "signature": sig,
                        "amount_sol": amount_sol,
                        "sender": sender,
                        "timestamp": tx.get("blockTime")
                    })
                    
                    print(f"🎉 NEW PAYMENT: {amount_sol:.4f} SOL from {sender[:20]}...")
        
        conn.commit()
        conn.close()
        
        return new_payments
    
    def generate_fulfillment_email(self, payment):
        """Generate fulfillment email for customer"""
        email_template = f"""Subject: Your PD_Researcher v1 Download Link

Thank you for your purchase!

Payment received: {payment['amount_sol']:.4f} SOL
Transaction: {payment['signature'][:30]}...

DOWNLOAD LINK:
https://github.com/barrowryan89-cloud/pd-researcher/releases/download/v1.0/PD_Researcher_v1.zip

INSTALLATION:
1. Unzip the file
2. Read README.md for setup instructions
3. Start researching like a pro

SUPPORT:
Reply to this email or contact support@sandstreet.holdings

Thanks for supporting independent tools!

— PD
"""
        return email_template
    
    def run_check(self):
        """Run a single check cycle"""
        print(f"[{datetime.now().isoformat()}] Checking wallet {WALLET_ADDRESS[:16]}...")
        
        balance = self.get_balance()
        if balance is not None:
            balance_sol = balance / 1e9
            print(f"  Balance: {balance_sol:.4f} SOL")
            
            # Update balance record
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            cursor.execute("DELETE FROM wallet_balance")
            cursor.execute("INSERT INTO wallet_balance (balance_lamports) VALUES (?)", (balance,))
            conn.commit()
            conn.close()
        
        new_payments = self.check_for_new_payments()
        
        if new_payments:
            print(f"\n🚨 {len(new_payments)} NEW PAYMENT(S) DETECTED!\n")
            for payment in new_payments:
                print(self.generate_fulfillment_email(payment))
                print("-" * 50)
            return True  # Signal that action needed
        else:
            print("  No new payments")
        
        return False

def main():
    watcher = PaymentWatcher()
    
    # Check for --daemon mode
    if len(sys.argv) > 1 and sys.argv[1] == "--daemon":
        print("Starting payment watcher daemon...")
        print(f"Monitoring: {WALLET_ADDRESS}")
        print("Press Ctrl+C to stop\n")
        
        try:
            while True:
                action_needed = watcher.run_check()
                if action_needed:
                    # In daemon mode, this would trigger a notification
                    pass
                time.sleep(60)  # Check every minute
        except KeyboardInterrupt:
            print("\nStopping watcher...")
    else:
        # Single check
        watcher.run_check()

if __name__ == "__main__":
    import time
    main()
