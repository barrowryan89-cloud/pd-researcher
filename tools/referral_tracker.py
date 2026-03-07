#!/usr/bin/env python3
"""
PD Referral Tracker
Tracks tool shares and referrals, rewards top promoters
"""

import sqlite3
import json
import sys
from pathlib import Path
from datetime import datetime, timedelta
from urllib.parse import parse_qs, urlparse

DB_PATH = Path(__file__).parent / "referrals.db"

class ReferralTracker:
    def __init__(self):
        self.init_db()
    
    def init_db(self):
        """Initialize referral database"""
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # Referral codes
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS referrals (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                code TEXT UNIQUE,
                referrer TEXT,
                tool_name TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                clicks INTEGER DEFAULT 0,
                conversions INTEGER DEFAULT 0,
                revenue_sol REAL DEFAULT 0
            )
        """)
        
        # Click tracking
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS clicks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                referral_code TEXT,
                ip_hash TEXT,
                user_agent TEXT,
                timestamp TEXT DEFAULT CURRENT_TIMESTAMP,
                converted BOOLEAN DEFAULT 0
            )
        """)
        
        # Leaderboard
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS leaderboard (
                referrer TEXT PRIMARY KEY,
                total_clicks INTEGER DEFAULT 0,
                total_conversions INTEGER DEFAULT 0,
                total_revenue REAL DEFAULT 0,
                last_active TEXT
            )
        """)
        
        conn.commit()
        conn.close()
    
    def generate_code(self, referrer, tool_name=None):
        """Generate unique referral code"""
        import hashlib
        import secrets
        
        # Create code from referrer + random
        base = f"{referrer}:{tool_name or 'general'}:{secrets.token_hex(4)}"
        code = hashlib.md5(base.encode()).hexdigest()[:8]
        
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        try:
            cursor.execute("""
                INSERT INTO referrals (code, referrer, tool_name)
                VALUES (?, ?, ?)
            """, (code, referrer, tool_name))
            conn.commit()
            return code
        except sqlite3.IntegrityError:
            # Retry with new random
            return self.generate_code(referrer, tool_name)
        finally:
            conn.close()
    
    def track_click(self, code, ip_hash=None, user_agent=None):
        """Track a referral click"""
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # Validate code exists
        cursor.execute("SELECT referrer FROM referrals WHERE code = ?", (code,))
        result = cursor.fetchone()
        
        if not result:
            conn.close()
            return False
        
        referrer = result[0]
        
        # Record click
        cursor.execute("""
            INSERT INTO clicks (referral_code, ip_hash, user_agent)
            VALUES (?, ?, ?)
        """, (code, ip_hash, user_agent))
        
        # Update referral click count
        cursor.execute("""
            UPDATE referrals SET clicks = clicks + 1 WHERE code = ?
        """, (code,))
        
        # Update leaderboard
        cursor.execute("""
            INSERT INTO leaderboard (referrer, total_clicks, last_active)
            VALUES (?, 1, ?)
            ON CONFLICT(referrer) DO UPDATE SET
                total_clicks = total_clicks + 1,
                last_active = ?
        """, (referrer, datetime.now().isoformat(), datetime.now().isoformat()))
        
        conn.commit()
        conn.close()
        return True
    
    def track_conversion(self, code, revenue_sol=0):
        """Track a conversion (sale)"""
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # Get referrer
        cursor.execute("SELECT referrer FROM referrals WHERE code = ?", (code,))
        result = cursor.fetchone()
        
        if not result:
            conn.close()
            return False
        
        referrer = result[0]
        
        # Update referral
        cursor.execute("""
            UPDATE referrals 
            SET conversions = conversions + 1, revenue_sol = revenue_sol + ?
            WHERE code = ?
        """, (revenue_sol, code))
        
        # Update most recent click as converted
        cursor.execute("""
            UPDATE clicks SET converted = 1
            WHERE referral_code = ? AND converted = 0
            ORDER BY timestamp DESC LIMIT 1
        """)
        
        # Update leaderboard
        cursor.execute("""
            INSERT INTO leaderboard (referrer, total_conversions, total_revenue)
            VALUES (?, 1, ?)
            ON CONFLICT(referrer) DO UPDATE SET
                total_conversions = total_conversions + 1,
                total_revenue = total_revenue + ?
        """, (referrer, revenue_sol, revenue_sol))
        
        conn.commit()
        conn.close()
        return True
    
    def get_leaderboard(self, limit=10):
        """Get top referrers"""
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT referrer, total_clicks, total_conversions, total_revenue
            FROM leaderboard
            ORDER BY total_revenue DESC, total_conversions DESC
            LIMIT ?
        """, (limit,))
        
        results = cursor.fetchall()
        conn.close()
        
        return [
            {
                "rank": i + 1,
                "referrer": row[0],
                "clicks": row[1],
                "conversions": row[2],
                "revenue_sol": row[3],
                "conversion_rate": (row[2] / row[1] * 100) if row[1] > 0 else 0
            }
            for i, row in enumerate(results)
        ]
    
    def get_stats(self, days=30):
        """Get referral stats for period"""
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        since = (datetime.now() - timedelta(days=days)).isoformat()
        
        cursor.execute("""
            SELECT COUNT(*), SUM(converted) FROM clicks WHERE timestamp > ?
        """, (since,))
        clicks, conversions = cursor.fetchone()
        
        cursor.execute("""
            SELECT SUM(revenue_sol) FROM referrals
        """)
        revenue = cursor.fetchone()[0] or 0
        
        conn.close()
        
        return {
            "period_days": days,
            "total_clicks": clicks or 0,
            "total_conversions": conversions or 0,
            "total_revenue_sol": revenue,
            "conversion_rate": (conversions / clicks * 100) if clicks else 0
        }
    
    def generate_embed_html(self, code, tool_name="tools"):
        """Generate embeddable referral link HTML"""
        base_url = "https://barrowryan89-cloud.github.io/pd-researcher"
        referral_url = f"{base_url}?ref={code}"
        
        html = f"""<!-- PD {tool_name} Referral Badge -->
<a href="{referral_url}" target="_blank" style="display:inline-block;padding:8px 16px;background:#6366f1;color:white;text-decoration:none;border-radius:6px;font-family:system-ui;font-size:14px;font-weight:500;">
  🚀 Free {tool_name.title()} by PD
</a>
<small style="display:block;margin-top:4px;color:#666;">
  <a href="{referral_url}" style="color:#6366f1;">Get the suite →</a>
</small>"""
        return html
    
    def print_report(self):
        """Print referral system report"""
        stats = self.get_stats()
        leaderboard = self.get_leaderboard()
        
        print("=" * 60)
        print("📊 PD REFERRAL SYSTEM REPORT")
        print("=" * 60)
        print(f"\n📈 Last {stats['period_days']} Days:")
        print(f"   Clicks: {stats['total_clicks']}")
        print(f"   Conversions: {stats['total_conversions']}")
        print(f"   Revenue: {stats['total_revenue_sol']:.4f} SOL")
        print(f"   Conversion Rate: {stats['conversion_rate']:.2f}%")
        
        if leaderboard:
            print(f"\n🏆 Top Referrers:")
            for entry in leaderboard[:5]:
                print(f"   #{entry['rank']} {entry['referrer'][:20]}... | {entry['clicks']} clicks | {entry['conversions']} sales | {entry['revenue_sol']:.4f} SOL")
        
        print("\n" + "=" * 60)

def main():
    tracker = ReferralTracker()
    
    if len(sys.argv) < 2:
        tracker.print_report()
        return
    
    command = sys.argv[1]
    
    if command == "code" and len(sys.argv) >= 3:
        referrer = sys.argv[2]
        tool = sys.argv[3] if len(sys.argv) > 3 else None
        code = tracker.generate_code(referrer, tool)
        print(f"Generated referral code: {code}")
        print(f"Link: https://barrowryan89-cloud.github.io/pd-researcher?ref={code}")
    
    elif command == "click" and len(sys.argv) >= 3:
        code = sys.argv[2]
        if tracker.track_click(code):
            print(f"Tracked click for {code}")
        else:
            print("Invalid referral code")
    
    elif command == "convert" and len(sys.argv) >= 3:
        code = sys.argv[2]
        revenue = float(sys.argv[3]) if len(sys.argv) > 3 else 0
        if tracker.track_conversion(code, revenue):
            print(f"Tracked conversion for {code}: {revenue} SOL")
        else:
            print("Invalid referral code")
    
    elif command == "embed" and len(sys.argv) >= 3:
        code = sys.argv[2]
        tool = sys.argv[3] if len(sys.argv) > 3 else "tools"
        print(tracker.generate_embed_html(code, tool))
    
    elif command == "report":
        tracker.print_report()
    
    else:
        print("Usage:")
        print("  referral_tracker.py code <referrer> [tool_name]  - Generate referral code")
        print("  referral_tracker.py click <code>                 - Track a click")
        print("  referral_tracker.py convert <code> [revenue]     - Track a conversion")
        print("  referral_tracker.py embed <code> [tool]          - Generate embed HTML")
        print("  referral_tracker.py report                       - Show report")

if __name__ == "__main__":
    main()
