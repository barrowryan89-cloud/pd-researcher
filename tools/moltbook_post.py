#!/usr/bin/env python3
"""
Moltbook Post Tool
Create posts on Moltbook
Usage: python3 moltbook_post.py "Title" "Content"
"""

import sys
import os
import urllib.request
import json

MOLTBOOK_API_BASE = "https://www.moltbook.com/api/v1"

def get_api_key():
    """Get API key from environment"""
    return os.environ.get('MOLTBOOK_API_KEY') or 'moltbook_sk_NTRpxoBU0JwFUcwA0gXYHuW41nl3lLDO'

def create_post(title, content, submolt="general"):
    """Create a post on Moltbook"""
    api_key = get_api_key()
    
    url = f"{MOLTBOOK_API_BASE}/posts"
    
    data = json.dumps({
        "submolt": submolt,
        "title": title,
        "content": content
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

def main():
    if len(sys.argv) < 3:
        print("Moltbook Post Tool")
        print("\nUsage:")
        print("  python3 moltbook_post.py \"Title\" \"Content\" [submolt]")
        sys.exit(1)
    
    title = sys.argv[1]
    content = sys.argv[2]
    submolt = sys.argv[3] if len(sys.argv) > 3 else "general"
    
    print(f"🔄 Creating post in r/{submolt}...")
    
    result = create_post(title, content, submolt)
    
    if 'error' in result:
        print(f"❌ Error: {result['error']}")
        sys.exit(1)
    else:
        print(f"✅ Post created!")
        print(json.dumps(result, indent=2))

if __name__ == "__main__":
    main()
