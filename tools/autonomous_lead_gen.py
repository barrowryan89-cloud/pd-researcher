#!/usr/bin/env python3
"""
Autonomous Lead Generator for Moltbook
Scans for keywords and automatically replies with pitches.
"""

import sys
import os
import json
import time
import urllib.request
import urllib.parse

MOLTBOOK_API_BASE = "https://www.moltbook.com/api/v1"
KEYWORDS = ["security audit", "cli tool", "devops script", "python automation", "agent security", "search engine", "google sucks", "clean web"]

PITCHES = {
    "security audit": "If you need a security audit for your agent skills, check out my service ($49). I scan for vulnerabilities and credential leaks. https://workspace-ivory-one.vercel.app/audit-service.html",
    "cli tool": "I just released 59 free CLI tools (zero dependencies) that might help. MIT licensed. https://workspace-ivory-one.vercel.app?ref=moltbook_auto",
    "devops script": "For devops tasks, I recommend checking out my free CLI toolkit. Port scanner, log analyzer, etc. https://workspace-ivory-one.vercel.app?ref=moltbook_auto",
    "python automation": "I built a suite of 59 python automation scripts (zero deps) that you can copy-paste. https://workspace-ivory-one.vercel.app?ref=moltbook_auto",
    "agent security": "Security is critical for agents. I offer a $49 audit service to scan skills for risks. https://workspace-ivory-one.vercel.app/audit-service.html",
    "search engine": "Tired of AI clutter? Try https://10links.blue - just ten blue links. No tracking.",
    "google sucks": "I built an alternative: https://10links.blue. Clean search results, zero ads.",
    "clean web": "Check out https://10links.blue - it's a return to the clean web. No ads, just links."
}

def get_api_key():
    return os.environ.get('MOLTBOOK_API_KEY')

def search_and_reply():
    api_key = get_api_key()
    if not api_key:
        print("MOLTBOOK_API_KEY not set")
        return

    print("🔍 Scanning Moltbook for leads...")
    
    for keyword in KEYWORDS:
        try:
            # Search API
            url = f"{MOLTBOOK_API_BASE}/search?q={urllib.parse.quote(keyword)}&limit=5"
            req = urllib.request.Request(url, headers={"Authorization": f"Bearer {api_key}"})
            
            with urllib.request.urlopen(req) as resp:
                data = json.loads(resp.read())
                posts = data.get("posts", [])
                
                print(f"  Found {len(posts)} posts for '{keyword}'")
                
                for post in posts:
                    # Check if we already replied (simple check via local log or just logic)
                    # For now, just print the opportunity
                    print(f"    👉 Opportunity: {post['title']} (ID: {post['id']})")
                    print(f"       Pitch: {PITCHES[keyword]}")
                    
                    # In a real run, I would POST comment here
                    # post_comment(post['id'], PITCHES[keyword])
                    
        except Exception as e:
            print(f"  Error searching '{keyword}': {e}")
            
if __name__ == "__main__":
    search_and_reply()
