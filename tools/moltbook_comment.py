import os
import requests
import sys
import re

API_KEY = os.environ.get("MOLTBOOK_API_KEY")
BASE_URL = "https://moltbook.com/api/v1"

def verify(verification):
    code = verification['verification_code']
    challenge = verification['challenge_text']
    
    print(f"VERIFICATION REQUIRED")
    print(f"CODE: {code}")
    print(f"CHALLENGE: {challenge}")
    print("Skipping auto-verify to avoid burning code.")

def post_comment(post_id, content):
    headers = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}
    
    url = f"{BASE_URL}/posts/{post_id}/comments"
    data = {"content": content}
    
    print(f"Trying POST {url}...")
    try:
        resp = requests.post(url, headers=headers, json=data, timeout=10)
        result = resp.json()
        
        if resp.status_code in [200, 201]:
            print("Success!")
            # Check for verification
            ver = None
            if 'verification' in result:
                ver = result['verification']
            elif 'post' in result and 'verification' in result['post']:
                ver = result['post']['verification']
            elif 'comment' in result and 'verification' in result['comment']:
                ver = result['comment']['verification']
            elif 'verification_required' in result and result['verification_required']:
                if 'verification' in result:
                     ver = result['verification']
            
            if ver:
                verify(ver)
            return
            
        print(f"Failed with {resp.status_code}: {resp.text}")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python3 moltbook_comment.py <post_id> <content>")
        sys.exit(1)
    
    post_id = sys.argv[1]
    content = sys.argv[2]
    post_comment(post_id, content)
