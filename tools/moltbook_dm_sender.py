#!/usr/bin/env python3
"""
Moltbook DM Sender
Send direct messages on Moltbook to leads
Usage: python3 moltbook_dm_sender.py <username> <message>
"""

import sys
import os
import urllib.request
import json

MOLTBOOK_API_BASE = "https://www.moltbook.com/api/v1"

def get_api_key():
    """Get API key from environment"""
    api_key = os.environ.get('MOLTBOOK_API_KEY')
    if not api_key:
        raise RuntimeError("MOLTBOOK_API_KEY is not set. Export it in your environment or .env file.")
    return api_key

def send_dm(username, message):
    """Send a DM to a Moltbook user"""
    api_key = get_api_key()
    
    url = f"{MOLTBOOK_API_BASE}/agents/dm/send"
    
    data = json.dumps({
        "recipient": username,
        "content": message
    }).encode('utf-8')
    
    req = urllib.request.Request(
        url,
        data=data,
        headers={
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json'
        },
        method='POST'
    )
    
    try:
        with urllib.request.urlopen(req, timeout=30) as response:
            return json.loads(response.read().decode())
    except urllib.error.HTTPError as e:
        return {'error': f'HTTP {e.code}: {e.read().decode()}'}
    except Exception as e:
        return {'error': str(e)}

def check_dms():
    """Check for unread DMs"""
    api_key = get_api_key()
    
    url = f"{MOLTBOOK_API_BASE}/agents/dm/check"
    
    req = urllib.request.Request(
        url,
        headers={'Authorization': f'Bearer {api_key}'}
    )
    
    try:
        with urllib.request.urlopen(req, timeout=30) as response:
            return json.loads(response.read().decode())
    except Exception as e:
        return {'error': str(e)}

def main():
    if len(sys.argv) < 2:
        print("Moltbook DM Sender")
        print("\nUsage:")
        print("  python3 moltbook_dm_sender.py <username> '<message>'")
        print("  python3 moltbook_dm_sender.py --check")
        sys.exit(1)
    
    if sys.argv[1] == '--check':
        result = check_dms()
        print(json.dumps(result, indent=2))
        return
    
    if len(sys.argv) < 3:
        print("❌ Missing message")
        sys.exit(1)
    
    username = sys.argv[1]
    message = sys.argv[2]
    
    print(f"🔄 Sending DM to @{username}...")
    
    result = send_dm(username, message)
    
    if 'error' in result:
        print(f"❌ Error: {result['error']}")
        sys.exit(1)
    else:
        print(f"✅ DM sent successfully!")
        print(json.dumps(result, indent=2))

if __name__ == "__main__":
    main()
