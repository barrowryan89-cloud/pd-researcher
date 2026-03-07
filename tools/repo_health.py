#!/usr/bin/env python3
"""
repo_health - GitHub repository health analyzer
Quick health check for any public GitHub repo.

Usage: repo_health <owner/repo> [--details]
Example: repo_health facebook/react --details
"""

import sys
import json
import urllib.request
import urllib.error
from datetime import datetime
from typing import Dict, Any, Optional


def fetch_repo(owner: str, repo: str) -> Optional[Dict[str, Any]]:
    """Fetch repo data from GitHub API."""
    url = f"https://api.github.com/repos/{owner}/{repo}"
    headers = {"Accept": "application/vnd.github.v3+json"}
    
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=10) as response:
            return json.loads(response.read().decode('utf-8'))
    except urllib.error.HTTPError as e:
        if e.code == 404:
            print(f"❌ Repo not found: {owner}/{repo}")
        elif e.code == 403:
            print("⚠️  API rate limit hit. Try again later.")
        else:
            print(f"❌ Error: {e}")
        return None
    except Exception as e:
        print(f"❌ Failed: {e}")
        return None


def format_number(n: int) -> str:
    """Format large numbers nicely."""
    if n >= 1_000_000:
        return f"{n/1_000_000:.1f}M"
    elif n >= 1_000:
        return f"{n/1_000:.1f}K"
    return str(n)


def days_since(date_str: str) -> int:
    """Calculate days since a date."""
    try:
        date = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
        return (datetime.now(datetime.timezone.utc) - date).days
    except:
        return -1


def health_score(data: Dict[str, Any]) -> tuple:
    """Calculate a 0-100 health score."""
    score = 50  # Base score
    
    # Popularity boost
    stars = data.get('stargazers_count', 0)
    if stars > 10000: score += 15
    elif stars > 1000: score += 10
    elif stars > 100: score += 5
    
    # Activity boost
    days = days_since(data.get('pushed_at', ''))
    if days < 7: score += 15
    elif days < 30: score += 10
    elif days < 90: score += 5
    else: score -= 10
    
    # Open issues penalty
    open_issues = data.get('open_issues_count', 0)
    if open_issues > 100: score -= 5
    if open_issues > 500: score -= 10
    
    # Has description + topics
    if data.get('description'): score += 5
    if data.get('topics'): score += 5
    
    # Has license
    if data.get('license'): score += 5
    
    return max(0, min(100, score)), days


def display_summary(data: Dict[str, Any], details: bool = False):
    """Display repo health summary."""
    owner = data['owner']['login']
    name = data['name']
    score, days_since_push = health_score(data)
    
    # Score emoji
    if score >= 80: emoji = "🟢"
    elif score >= 60: emoji = "🟡"
    elif score >= 40: emoji = "🟠"
    else: emoji = "🔴"
    
    print(f"\n{'='*50}")
    print(f"{emoji} {owner}/{name}")
    print(f"{'='*50}")
    
    if data.get('description'):
        print(f"📋 {data['description'][:70]}{'...' if len(data['description']) > 70 else ''}")
    
    print(f"\n📊 Health Score: {score}/100")
    print(f"⭐ Stars: {format_number(data.get('stargazers_count', 0))}")
    print(f"🍴 Forks: {format_number(data.get('forks_count', 0))}")
    print(f"👁️  Watchers: {format_number(data.get('watchers_count', 0))}")
    print(f"🐛 Open Issues: {format_number(data.get('open_issues_count', 0))}")
    
    # Activity indicator
    if days_since_push < 0:
        activity = "❓ Unknown"
    elif days_since_push == 0:
        activity = "🟢 Active today"
    elif days_since_push < 7:
        activity = f"🟢 Active {days_since_push}d ago"
    elif days_since_push < 30:
        activity = f"🟡 Active {days_since_push}d ago"
    else:
        activity = f"🔴 Stale ({days_since_push}d ago)"
    print(f"📝 Last Push: {activity}")
    
    print(f"🔤 Language: {data.get('language', 'Unknown')}")
    
    if data.get('license'):
        print(f"⚖️  License: {data['license'].get('spdx_id', 'Unknown')}")
    else:
        print(f"⚖️  License: ❌ None")
    
    if details:
        print(f"\n{'─'*50}")
        print("DETAILS:")
        print(f"{'─'*50}")
        print(f"📅 Created: {data.get('created_at', 'N/A')[:10]}")
        print(f"🔄 Updated: {data.get('updated_at', 'N/A')[:10]}")
        print(f"🌐 Homepage: {data.get('homepage') or 'None'}")
        print(f"🔗 URL: {data.get('html_url')}")
        print(f"📦 Size: {data.get('size', 0)} KB")
        
        if data.get('topics'):
            print(f"🏷️  Topics: {', '.join(data['topics'][:8])}")
        
        if data.get('archived'):
            print("⚠️  ARCHIVED - No longer maintained")
        if data.get('fork'):
            print("📌 This is a FORK")
    
    print(f"{'='*50}\n")


def main():
    if len(sys.argv) < 2:
        print("Usage: repo_health <owner/repo> [--details]")
        print("Example: repo_health vercel/next.js --details")
        sys.exit(1)
    
    repo_arg = sys.argv[1]
    if '/' not in repo_arg:
        print("❌ Format: owner/repo (e.g., facebook/react)")
        sys.exit(1)
    
    owner, repo = repo_arg.split('/', 1)
    details = '--details' in sys.argv
    
    print(f"🔍 Analyzing {owner}/{repo}...")
    
    data = fetch_repo(owner, repo)
    if data:
        display_summary(data, details)


if __name__ == "__main__":
    main()
