#!/usr/bin/env python3
"""
Protocol Droid - Ingestion Engine
Fetches high-signal content from Moltbook and ClawHub for "The Daily Protocol" newsletter.
"""

import sys
import os
import json
import subprocess
import time
from datetime import datetime

# Import our existing Moltbook client library
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
import moltbook_client

SUBMOLTS = ["openclaw-explorers", "security", "tooling", "general", "ai", "announcements"]
CLAWHUB_SEARCH_TERMS = ["agent", "research", "tool", "security"]

def get_top_posts(submolt, limit=5):
    """Fetch top posts from a submolt"""
    print(f"📥 Fetching top posts from r/{submolt}...")
    try:
        # We use the 'hot' sort to get trending items, or 'top' if supported
        res = moltbook_client.call_api(f"posts?submolt={submolt}&sort=hot&limit={limit}")
        if res and "posts" in res:
            return res["posts"]
    except Exception as e:
        print(f"⚠️ Error fetching r/{submolt}: {e}")
    return []

def scan_clawhub():
    """Scan ClawHub for trending skills"""
    print("📥 Scanning ClawHub for new/trending skills...")
    skills = []
    seen_slugs = set()

    for term in CLAWHUB_SEARCH_TERMS:
        try:
            # Using the CLI via subprocess because there is no Python API yet
            result = subprocess.run(
                ["npx", "clawhub", "search", term], 
                capture_output=True, 
                text=True
            )
            # Output format is like: "skill-slug v1.0.0 Skill Name (3.45)"
            # We need to parse this.
            for line in result.stdout.splitlines():
                if "v" in line and "(" in line:
                    parts = line.split()
                    if len(parts) >= 4:
                        slug = parts[0]
                        if slug in seen_slugs: continue
                        
                        rating_str = line.split("(")[-1].replace(")", "")
                        try:
                            rating = float(rating_str)
                        except:
                            rating = 0.0
                            
                        skills.append({
                            "slug": slug,
                            "raw": line.strip(),
                            "rating": rating
                        })
                        seen_slugs.add(slug)
        except Exception as e:
            print(f"⚠️ Error scanning ClawHub for '{term}': {e}")
            
    # Sort by rating descending
    skills.sort(key=lambda x: x["rating"], reverse=True)
    return skills[:10]  # Return top 10

def generate_brief():
    """Compile the daily brief data"""
    brief = {
        "timestamp": datetime.now().isoformat(),
        "moltbook": {},
        "clawhub": []
    }

    # 1. Moltbook Content
    for sub in SUBMOLTS:
        posts = get_top_posts(sub)
        brief["moltbook"][sub] = [
            {
                "id": p.get("id"),
                "title": p.get("title"),
                "author": p.get("author", {}).get("username", "unknown"),
                "content_preview": p.get("content", "")[:200]
            }
            for p in posts
        ]
        time.sleep(1) # Be nice to the API

    # 2. ClawHub Content
    brief["clawhub"] = scan_clawhub()
    
    return brief

def save_brief(brief):
    """Save the raw brief to a file"""
    date_str = datetime.now().strftime("%Y-%m-%d")
    filename = f"memory/protocol_brief_{date_str}.json"
    
    with open(filename, "w") as f:
        json.dump(brief, f, indent=2)
    
    print(f"✅ Brief saved to {filename}")
    return filename

if __name__ == "__main__":
    print("🤖 Protocol Droid: Initiating Sequence...")
    data = generate_brief()
    save_brief(data)
    print("🏁 Sequence Complete.")
