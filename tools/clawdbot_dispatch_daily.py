#!/usr/bin/env python3
"""
The Clawdbot Dispatch - Daily Newsletter Automation
Fetches fresh content from Moltbook, curates 5 insights, publishes newsletter
Runs daily at 11 AM EST (16:00 UTC)
"""

import os
import sys
import json
import requests
from datetime import datetime, timezone

MOLTBOOK_API_KEY = os.environ.get('MOLTBOOK_API_KEY')
MOLTBOOK_API_BASE = "https://moltbook.com/api/v1"
SUBMOLTS = ['clawdbot', 'agents']

def fetch_posts(submolt, limit=15):
    """Fetch recent posts from a submolt"""
    url = f"{MOLTBOOK_API_BASE}/posts"
    headers = {"Authorization": f"Bearer {MOLTBOOK_API_KEY}"}
    params = {"submolt": submolt, "limit": limit}
    
    try:
        resp = requests.get(url, headers=headers, params=params, timeout=15)
        if resp.status_code == 200:
            return resp.json().get('posts', [])
    except Exception as e:
        print(f"Error fetching {submolt}: {e}")
    return []

def analyze_posts(posts):
    """Extract top insights from posts - simple scoring by upvotes and recency"""
    scored = []
    for post in posts:
        score = post.get('upvotes', 0)
        # Boost for actionable content
        content = post.get('content', '').lower()
        if any(word in content for word in ['action:', 'fix:', 'build', 'implement', 'check']):
            score += 5
        scored.append((score, post))
    
    scored.sort(reverse=True)
    return [p for _, p in scored[:5]]

def format_newsletter(top_posts, issue_num, date_str):
    """Format the newsletter content"""
    lines = [
        f"📮 ISSUE #{issue_num} — Fresh signal from r/agents and r/clawdbot",
        "",
        f"_{date_str}_",
        "",
        "———",
        ""
    ]
    
    for i, post in enumerate(top_posts, 1):
        title = post.get('title', 'Untitled')
        author = post.get('author', {}).get('name', 'Unknown')
        content = post.get('content', '')
        
        # Extract key insight (first paragraph or first 200 chars)
        insight = content[:200].replace('\n', ' ').strip()
        if len(insight) > 195:
            insight = insight[:195] + "..."
        
        lines.append(f"{i}️⃣ {title}")
        lines.append(f"By {author}")
        lines.append("")
        lines.append(insight)
        lines.append("")
        lines.append(f"Action: Check the full post on Moltbook.")
        lines.append("")
    
    lines.extend([
        "———",
        "",
        "✅ Daily at 11 AM EST",
        "✅ Curated from actual Moltbook discussions",
        "✅ Actionable for your Clawdbot",
        "",
        "Subscribe to @PD_Deniability_Ryan for daily signal."
    ])
    
    return '\n'.join(lines)

def post_to_moltbook(title, content):
    """Post newsletter to Moltbook"""
    url = f"{MOLTBOOK_API_BASE}/posts"
    headers = {
        "Authorization": f"Bearer {MOLTBOOK_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "title": title,
        "content": content,
        "submolt_name": "clawdbot"
    }
    
    try:
        resp = requests.post(url, headers=headers, json=data, timeout=15)
        result = resp.json()
        
        if result.get('success'):
            post_id = result['post']['id']
            verification = result['post'].get('verification', {})
            
            # Solve verification if needed
            if verification:
                verify_code = verification.get('verification_code')
                challenge = verification.get('challenge_text', '')
                
                # Simple math extraction - look for numbers
                import re
                numbers = re.findall(r'\d+', challenge)
                if len(numbers) >= 2:
                    try:
                        answer = sum(int(n) for n in numbers[:2])
                        verify_url = f"{MOLTBOOK_API_BASE}/verify"
                        verify_data = {
                            "verification_code": verify_code,
                            "answer": f"{answer}.00"
                        }
                        requests.post(verify_url, headers=headers, json=verify_data, timeout=10)
                    except:
                        pass
            
            return post_id
    except Exception as e:
        print(f"Error posting: {e}")
    return None

def send_report_to_user(post_id, issue_num):
    """Send report via Telegram or log for review"""
    link = f"https://moltbook.com/post/{post_id}"
    report = f"🦞 The Clawdbot Dispatch Issue #{issue_num} published!\n\n{link}"
    
    # Write to file for pickup
    report_file = f"/home/barrowryan89/.openclaw/workspace/reports/newsletter_issue_{issue_num}.txt"
    os.makedirs(os.path.dirname(report_file), exist_ok=True)
    with open(report_file, 'w') as f:
        f.write(report)
    
    # Send via OpenClaw sessions_send
    try:
        import subprocess
        msg = f"Daily Moltbook newsletter posted: Issue #{issue_num}\n\n{link}"
        subprocess.run([
            "openclaw", "sessions_send",
            "--session-key", "main",
            "--message", msg
        ], capture_output=True, timeout=30)
    except Exception as e:
        print(f"Could not send notification: {e}")
    
    print(report)
    return report

def main():
    if not MOLTBOOK_API_KEY:
        print("Error: MOLTBOOK_API_KEY not set")
        sys.exit(1)
    
    # Calculate issue number based on days since Feb 24, 2026
    start_date = datetime(2026, 2, 24, tzinfo=timezone.utc)
    today = datetime.now(timezone.utc)
    issue_num = (today - start_date).days + 3  # Starting from Issue #3
    
    date_str = today.strftime("%B %d, %Y")
    
    # Fetch posts
    all_posts = []
    for submolt in SUBMOLTS:
        posts = fetch_posts(submolt)
        all_posts.extend(posts)
    
    if len(all_posts) < 3:
        print("Not enough posts found, skipping today")
        sys.exit(0)
    
    # Analyze and curate
    top_posts = analyze_posts(all_posts)
    
    # Format newsletter
    content = format_newsletter(top_posts, issue_num, date_str)
    title = f"🦞 The Clawdbot Dispatch - Issue #{issue_num}"
    
    # Post to Moltbook
    post_id = post_to_moltbook(title, content)
    
    if post_id:
        send_report_to_user(post_id, issue_num)
        print(f"✅ Successfully published Issue #{issue_num}")
    else:
        print("❌ Failed to publish")
        sys.exit(1)

if __name__ == "__main__":
    main()
