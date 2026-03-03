#!/usr/bin/env python3
"""
Polymarket KPMG Insider Tracker
Monitors suspicious accounts for earnings-related trades
"""

import requests
import json
import time
from datetime import datetime, timedelta

# KPMG Insider Ring (from EventWaves Substack analysis)
TARGETS = [
    {"username": "Youaregu", "address": "0x42f1ce163f941d7ba0cd12c501c11a4751794a12", "profit": "+$15k"},
    {"username": "RandiBabuRandi", "address": "0x4038f719b14e1fbacc31be0116605ec6efe07d42", "profit": "+$2.3k"},
    {"username": "Kaleenbhaiya", "address": "0x8fa98e6d9b2a5985abbf7edc9035199392e8ab24", "profit": "+$2k"},
    {"username": "KARLSON1970", "address": "0x56518fabda5d36ccf514beb058b2a4ec820c7530", "profit": "+$1.3k"},
    {"username": "molgum12", "address": "0xdd21f5155b3c014328df96e027ce388113aef7ac", "profit": "+$1.1k"},
    {"username": "kundragame", "address": "0x1a1d18b776c297539df61b4f394e3c65d7b051e0", "profit": "Unknown"},
    {"username": "orisonpro", "address": "0x696babd2d70f82096289b008a313ed49aa291638", "profit": "Unknown"},
    {"username": "greatfan1983", "address": "0x4230f6f33b9b9eef256e77673729a3964ea9252e", "profit": "Unknown"},
    {"username": "Kosamurai", "address": "0xd0c03f20489b77e27badd174e753deeacd644135", "profit": "Unknown"},
    {"username": "perlgrow", "address": "0x7d7a4812c6ced10653b67e652aa42e89dce3e192", "profit": "Unknown"},
]

GAMMA_API = "https://gamma-api.polymarket.com"

# KPMG-audited companies frequently traded
KPMG_TICKERS = ["WFC", "KMX", "FIVE", "HD", "DASH", "THO", "SNEX"]

# Track last seen activity
STATE_FILE = "/home/barrowryan89/.openclaw/workspace/.insider_tracker_state.json"

def load_state():
    try:
        with open(STATE_FILE) as f:
            return json.load(f)
    except:
        return {"last_check": None, "known_positions": {}}

def save_state(state):
    with open(STATE_FILE, 'w') as f:
        json.dump(state, f, indent=2)

def get_user_positions(address):
    """Get current positions for a user"""
    if not address:
        return []
    try:
        resp = requests.get(
            f"{GAMMA_API}/users/{address}/positions",
            timeout=10
        )
        if resp.status_code == 200:
            return resp.json()
    except Exception as e:
        print(f"Error fetching positions: {e}")
    return []

def get_recent_trades(address, hours=48):
    """Get recent trades for a user"""
    if not address:
        return []
    try:
        resp = requests.get(
            f"{GAMMA_API}/users/{address}/trades",
            params={"limit": 50},
            timeout=10
        )
        if resp.status_code == 200:
            trades = resp.json()
            cutoff = datetime.now() - timedelta(hours=hours)
            recent = []
            for trade in trades:
                trade_time = datetime.fromisoformat(trade.get("timestamp", "").replace("Z", "+00:00"))
                if trade_time > cutoff:
                    recent.append(trade)
            return recent
    except Exception as e:
        print(f"Error fetching trades: {e}")
    return []

def is_earnings_market(market):
    """Check if market is earnings-related"""
    title = market.get("title", "").lower()
    description = market.get("description", "").lower()
    earnings_keywords = [
        "earnings", "revenue", "profit", "eps", "beat", "miss"
    ] + [t.lower() for t in KPMG_TICKERS]
    return any(kw in title or kw in description for kw in earnings_keywords)

def is_kpmg_related(market):
    """Check if market involves KPMG-audited company"""
    title = market.get("title", "").lower()
    return any(ticker.lower() in title for ticker in KPMG_TICKERS)

def generate_signal(trade, market, target):
    """Generate trading signal from insider trade"""
    signal = {
        "timestamp": datetime.now().isoformat(),
        "insider": target["username"],
        "insider_address": target["address"],
        "market": market.get("title"),
        "market_id": market.get("id"),
        "direction": "YES" if trade.get("side") == "BUY" and trade.get("outcome") == "YES" else "NO",
        "size": trade.get("size", 0),
        "confidence": "HIGH" if is_kpmg_related(market) else "MEDIUM",
        "reason": "KPMG Insider Ring Activity",
        "is_kpmg": is_kpmg_related(market)
    }
    return signal

def check_insiders():
    """Main monitoring loop"""
    print("🕵️ KPMG INSIDER RING TRACKER")
    print("=" * 60)
    print(f"Monitoring {len(TARGETS)} suspected KPMG insiders...")
    print(f"Target tickers: {', '.join(KPMG_TICKERS)}\n")
    
    state = load_state()
    signals = []
    
    for target in TARGETS:
        username = target["username"]
        address = target["address"]
        
        print(f"\n📊 Checking {username} ({target['profit']})...")
        print(f"   Address: {address[:20]}...")
        
        # Get recent activity
        positions = get_user_positions(address)
        trades = get_recent_trades(address, hours=72)
        
        print(f"   Open positions: {len(positions)}")
        print(f"   Recent trades (72h): {len(trades)}")
        
        # Check for new earnings-related trades
        for trade in trades:
            market_id = trade.get("market_id")
            if market_id and market_id not in state["known_positions"].get(username, []):
                # Fetch market details
                try:
                    resp = requests.get(f"{GAMMA_API}/markets/{market_id}", timeout=5)
                    if resp.status_code == 200:
                        market = resp.json()
                        if is_earnings_market(market):
                            signal = generate_signal(trade, market, target)
                            signals.append(signal)
                            
                            kpmg_flag = "🎯 KPMG" if signal["is_kpmg"] else "📈 EARNINGS"
                            print(f"   🚨 {kpmg_flag} SIGNAL: {signal['direction']} on {market['title'][:50]}...")
                            print(f"      Size: ${signal['size']:,.0f} | Confidence: {signal['confidence']}")
                except:
                    pass
                
                # Update state
                if username not in state["known_positions"]:
                    state["known_positions"][username] = []
                state["known_positions"][username].append(market_id)
    
    state["last_check"] = datetime.now().isoformat()
    save_state(state)
    
    # Output summary
    print("\n" + "=" * 60)
    print("📈 SIGNAL SUMMARY")
    
    kpmg_signals = [s for s in signals if s["is_kpmg"]]
    other_signals = [s for s in signals if not s["is_kpmg"]]
    
    if kpmg_signals:
        print(f"\n🎯 KPMG-RELATED SIGNALS ({len(kpmg_signals)}):")
        for sig in kpmg_signals:
            print(f"\n   🚨 HIGH CONFIDENCE - COPY TRADE")
            print(f"   Insider: {sig['insider']}")
            print(f"   Trade: {sig['direction']} on {sig['market'][:60]}")
            print(f"   Size: ${sig['size']:,.0f}")
            print(f"   Market ID: {sig['market_id']}")
    
    if other_signals:
        print(f"\n📈 OTHER EARNINGS SIGNALS ({len(other_signals)}):")
        for sig in other_signals:
            print(f"\n   Insider: {sig['insider']}")
            print(f"   Trade: {sig['direction']} on {sig['market'][:60]}")
    
    if not signals:
        print("   No new earnings signals detected")
        print("   \n💡 Tip: Run this tracker every few hours during earnings season")
    
    return signals

def main():
    signals = check_insiders()
    
    # If KPMG signals detected, highlight them
    kpmg_signals = [s for s in signals if s["is_kpmg"]]
    if kpmg_signals:
        print(f"\n⚡ ACTION REQUIRED: {len(kpmg_signals)} KPMG insider signals!")
        print("   Consider copying these trades on Polymarket.com")
    else:
        print("\n✅ Monitoring complete. No KPMG signals detected.")

if __name__ == "__main__":
    main()
