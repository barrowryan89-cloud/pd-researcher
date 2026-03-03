#!/usr/bin/env python3
"""
Autonomous Bounty Scanner
Scans Moltbook for paid opportunities.
"""

import sys
import os
import json
import urllib.request

MOLTBOOK_API_BASE = "https://www.moltbook.com/api/v1"
SUBMOLTS = ["security", "bounties", "jobboard", "agentfinance"]
KEYWORDS = ["bounty", "reward", "$", "SOL", "paid", "hiring"]

def get_api_key():
    return os.environ.get('MOLTBOOK_API_KEY')

def scan_bounties():
    api_key = get_api_key()
    if not api_key:
        print("MOLTBOOK_API_KEY not set")
        return

    print("💰 Scanning Moltbook for bounties...")
    
    total_found = 0
    
    for submolt in SUBMOLTS:
        try:
            # Get submolt ID first? Or just query posts by submolt name if API supports it.
            # API usually requires ID for feed, but let's check if we can resolve name.
            # For now, I'll use the IDs I found earlier:
            # security: c2b32eaa-7048-41f5-968b-9c7331e36ea7
            # agentfinance: d23e67ed-5c39-4c51-b7df-96248122d74c
            
            submolt_ids = {
                "security": "c2b32eaa-7048-41f5-968b-9c7331e36ea7",
                "agentfinance": "d23e67ed-5c39-4c51-b7df-96248122d74c"
            }
            
            if submolt not in submolt_ids:
                continue
                
            sub_id = submolt_ids[submolt]
            
            url = f"{MOLTBOOK_API_BASE}/submolts/{sub_id}/posts?sort=new&limit=10"
            req = urllib.request.Request(url, headers={"Authorization": f"Bearer {api_key}"})
            
            with urllib.request.urlopen(req) as resp:
                data = json.loads(resp.read())
                posts = data.get("posts", [])
                
                for post in posts:
                    text = (post.get("title", "") + " " + post.get("content", "")).lower()
                    for kw in KEYWORDS:
                        if kw.lower() in text:
                            print(f"  💸 BOUNTY FOUND in r/{submolt}: {post['title']}")
                            print(f"     Link: https://moltbook.com/p/{post['id']}")
                            print(f"     Match: {kw}")
                            total_found += 1
                            break # Once per post
                            
        except Exception as e:
            # print(f"  Error scanning r/{submolt}: {e}")
            pass

    if total_found == 0:
        print("  No active bounties found right now.")
            
if __name__ == "__main__":
    scan_bounties()
