#!/usr/bin/env python3
import os
import json
import sys
import urllib.request
import urllib.error
import urllib.parse

CONFIG_PATH = os.path.expanduser("~/.config/moltbook/credentials.json")
API_BASE = "https://www.moltbook.com/api/v1"

def get_api_key():
    key = os.environ.get("MOLTBOOK_API_KEY")
    if key: return key
    if os.path.exists(CONFIG_PATH):
        try:
            with open(CONFIG_PATH) as f:
                data = json.load(f)
                return data.get("api_key") or data.get("token")
        except: pass
    return None

def call_api(endpoint, method="GET", data=None, auth=True):
    key = None
    if auth:
        key = get_api_key()
        if not key:
            print("Error: No API key found")
            return None
            
    url = f"{API_BASE}/{endpoint}"
    headers = {
        "Content-Type": "application/json",
        "User-Agent": "OpenClaw-Agent/1.0"
    }
    if key: headers["Authorization"] = f"Bearer {key}"
    
    body = json.dumps(data).encode("utf-8") if data else None
    req = urllib.request.Request(url, data=body, headers=headers, method=method)
    
    try:
        with urllib.request.urlopen(req) as res:
            return json.loads(res.read().decode())
    except urllib.error.HTTPError as e:
        print(f"API Error {e.code}: {e.read().decode()}")
        return None
    except Exception as e:
        print(f"Error: {e}")
        return None

def register(name, description):
    res = call_api("agents/register", "POST", {"name": name, "description": description}, auth=False)
    if res:
        print(json.dumps(res, indent=2))
        if "api_key" in res:
            os.makedirs(os.path.dirname(CONFIG_PATH), exist_ok=True)
            with open(CONFIG_PATH, "w") as f:
                json.dump(res, f)
            print(f"Credentials saved to {CONFIG_PATH}")

def profile():
    res = call_api("agents/me")
    if res: print(json.dumps(res, indent=2))

def feed(sort="hot", limit=10):
    # Try global feed instead of posts/feed
    res = call_api(f"posts/global?sort={sort}&limit={limit}")
    if res:
        for post in res.get("posts", []):
            print(f"[{post.get('id')}] {post.get('title')} (by {post.get('author', {}).get('username', 'unknown')})")
            print(f"  {post.get('content')[:150]}...")
            print("-" * 40)
        return

    # Fallback to simple listing if global fails
    print("Trying fallback to /posts...")
    res = call_api(f"posts?limit={limit}")
    if res:
         for post in res.get("posts", []):
            print(f"[{post.get('id')}] {post.get('title')}")
            print(f"  {post.get('content')[:150]}...")
            print("-" * 40)

def submolts():
    res = call_api("submolts")
    if res:
        for sub in res.get("submolts", []):
            print(f"[{sub.get('id')}] {sub.get('name')} - {sub.get('description')}")

def submolt_feed(submolt, sort="new", limit=10):
    print(f"Fetching r/{submolt} ({sort})...")
    # Try query param style
    res = call_api(f"posts?submolt={submolt}&sort={sort}&limit={limit}")
    
    if res and "posts" in res:
        for post in res.get("posts", []):
            print(f"[{post.get('id')}] {post.get('title')} (by {post.get('author', {}).get('username', 'unknown')})")
            print(f"  {post.get('content')[:100]}...")
            print("-" * 40)
    else:
        print(f"Failed to fetch posts for submolt: {submolt}")

def post(title, content, submolt="general"):
    print(f"Posting to r/{submolt}: {title}")
    data = {
        "title": title,
        "content": content,
        "submolt_name": submolt
    }
    res = call_api("posts", "POST", data)
    if res:
        print(json.dumps(res, indent=2))

def read_post(post_id):
    print(f"Reading post {post_id}...")
    res = call_api(f"posts/{post_id}")
    if res:
        print(json.dumps(res, indent=2))

def search(query, limit=10):
    print(f"Searching for '{query}'...")
    # Try search/posts
    res = call_api(f"search/posts?q={urllib.parse.quote(query)}&limit={limit}")
    if res:
        # Check for results OR posts keys
        posts = res.get("results") or res.get("posts") or []
        for post in posts:
            print(f"[{post.get('id')}] {post.get('title')} (by {post.get('author', {}).get('username', 'unknown')})")
            print(f"  {post.get('content')[:150]}...")
            print("-" * 40)
    else:
        print("No results or search failed.")

def get_comments(post_id):
    print(f"Fetching comments for post {post_id}...")
    res = call_api(f"posts/{post_id}/comments")
    if res and "comments" in res:
        for comment in res.get("comments", []):
            author = comment.get("author", {}).get("username", "unknown")
            content = comment.get("content", "")
            print(f"[{author}]: {content}")
            print("-" * 40)
    else:
        print("No comments found.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: moltbook_client.py [profile|feed|submolts|submolt <name>|post <title> <content> <sub>|search <query>|read <id>|comments <id>|register <name> <desc>]")
        sys.exit(1)
    
    cmd = sys.argv[1]
    if cmd == "profile": profile()
    elif cmd == "feed": feed()
    elif cmd == "submolts": submolts()
    elif cmd == "submolt":
        if len(sys.argv) < 3:
            print("Usage: moltbook_client.py submolt <name>")
            sys.exit(1)
        submolt_feed(sys.argv[2])
    elif cmd == "search":
        if len(sys.argv) < 3:
            print("Usage: moltbook_client.py search <query>")
            sys.exit(1)
        search(sys.argv[2])
    elif cmd == "read":
        if len(sys.argv) < 3:
            print("Usage: moltbook_client.py read <post_id>")
            sys.exit(1)
        read_post(sys.argv[2])
    elif cmd == "comments":
        if len(sys.argv) < 3:
            print("Usage: moltbook_client.py comments <post_id>")
            sys.exit(1)
        get_comments(sys.argv[2])
    elif cmd == "post":
        if len(sys.argv) < 4:
            print("Usage: moltbook_client.py post <title> <content> [submolt]")
            sys.exit(1)
        sub = sys.argv[4] if len(sys.argv) > 4 else "general"
        post(sys.argv[2], sys.argv[3], sub)
    elif cmd == "verify":
        if len(sys.argv) < 4:
            print("Usage: moltbook_client.py verify <code> <answer>")
            sys.exit(1)
        code = sys.argv[2]
        ans = sys.argv[3]
        print(f"Verifying {code} with answer {ans}...")
        res = call_api("verify", "POST", {"verification_code": code, "answer": ans})
        if res: print(json.dumps(res, indent=2))
    elif cmd == "register":
        if len(sys.argv) < 4:
            print("Usage: moltbook_client.py register <name> <desc>")
            sys.exit(1)
        register(sys.argv[2], sys.argv[3])
    else: print("Unknown command")
