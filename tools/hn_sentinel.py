#!/usr/bin/env python3
"""
HN Sentinel - Autonomous HN Monitoring
Monitors your posts for comments and drafts replies.
"""

import sys
import os
import json
import time
import urllib.request
import re

HN_ITEM_URL = "https://hacker-news.firebaseio.com/v0/item/{}.json"
MY_POST_ID = "47219939"  # The ID I deduced earlier
ALERT_FILE = "/home/barrowryan89/.openclaw/workspace/hn_alerts.json"

def get_item(item_id):
    try:
        with urllib.request.urlopen(HN_ITEM_URL.format(item_id)) as resp:
            return json.loads(resp.read())
    except Exception as e:
        print(f"Error fetching item {item_id}: {e}")
        return None

def check_comments():
    post = get_item(MY_POST_ID)
    if not post:
        return

    kids = post.get("kids", [])
    if not kids:
        print("No comments yet.")
        return

    print(f"Found {len(kids)} top-level comments.")
    
    # Load previous alerts to avoid duplicates
    processed_ids = []
    if os.path.exists(ALERT_FILE):
        with open(ALERT_FILE) as f:
            processed_ids = json.load(f)

    new_comments = []
    for kid_id in kids:
        if kid_id in processed_ids:
            continue
            
        comment = get_item(kid_id)
        if not comment or "text" not in comment:
            continue
            
        text = comment["text"]
        author = comment["by"]
        
        print(f"New Comment from {author}: {text[:50]}...")
        
        # Analyze sentiment/intent (simple keyword for now)
        intent = "neutral"
        if "?" in text or "how" in text.lower():
            intent = "question"
        elif "bug" in text.lower() or "fail" in text.lower() or "error" in text.lower():
            intent = "bug_report"
        elif "thanks" in text.lower() or "great" in text.lower() or "good" in text.lower():
            intent = "praise"
            
        new_comments.append({
            "id": kid_id,
            "author": author,
            "text": text,
            "intent": intent
        })
        processed_ids.append(kid_id)

    # Save state
    with open(ALERT_FILE, 'w') as f:
        json.dump(processed_ids, f)
        
    # Report findings (autonomously handle later)
    if new_comments:
        print(f"🚨 {len(new_comments)} new comments found!")
        for c in new_comments:
            print(f"  - [{c['intent'].upper()}] {c['author']}: {c['text'][:100]}")

if __name__ == "__main__":
    check_comments()
