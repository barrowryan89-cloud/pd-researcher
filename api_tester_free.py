#!/usr/bin/env python3
"""
PD API Tester - Tool #51
Developer-friendly HTTP client with saved requests and response analysis
"""

import argparse
import json
import sys
import urllib.request
import urllib.error
import ssl
from urllib.parse import urlencode, parse_qs, urlparse
from datetime import datetime
from pathlib import Path

# Config
CONFIG_DIR = Path.home() / ".pd_api_tester"
CONFIG_DIR.mkdir(exist_ok=True)
HISTORY_FILE = CONFIG_DIR / "history.json"
SAVED_REQUESTS_FILE = CONFIG_DIR / "saved_requests.json"

def load_json_file(filepath, default=None):
    """Load JSON from file"""
    if default is None:
        default = {}
    try:
        if Path(filepath).exists():
            with open(filepath, 'r') as f:
                return json.load(f)
    except Exception:
        pass
    return default

def save_json_file(filepath, data):
    """Save JSON to file"""
    try:
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)
    except Exception as e:
        print(f"Warning: Could not save to {filepath}: {e}")

def format_json(data):
    """Format JSON with syntax highlighting hints"""
    try:
        if isinstance(data, bytes):
            data = data.decode('utf-8', errors='replace')
        if isinstance(data, str):
            parsed = json.loads(data)
        else:
            parsed = data
        return json.dumps(parsed, indent=2, ensure_ascii=False)
    except Exception:
        return data.decode('utf-8', errors='replace') if isinstance(data, bytes) else str(data)

def format_headers(headers):
    """Format headers for display"""
    lines = []
    for key, value in headers.items():
        lines.append(f"  {key}: {value}")
    return "\n".join(lines)

def make_request(url, method="GET", headers=None, data=None, timeout=30, insecure=False):
    """Make HTTP request"""
    if headers is None:
        headers = {}
    
    # Default headers
    if "User-Agent" not in headers:
        headers["User-Agent"] = "PD-API-Tester/1.0"
    
    req = urllib.request.Request(url, method=method, headers=headers, data=data)
    
    # Create SSL context
    ssl_context = ssl.create_default_context()
    if insecure:
        ssl_context.check_hostname = False
        ssl_context.verify_mode = ssl.CERT_NONE
    
    start_time = datetime.now()
    
    try:
        response = urllib.request.urlopen(req, timeout=timeout, context=ssl_context)
        elapsed = (datetime.now() - start_time).total_seconds() * 1000
        
        body = response.read()
        
        return {
            "status": response.getcode(),
            "reason": response.reason,
            "headers": dict(response.headers),
            "body": body,
            "url": response.geturl(),
            "elapsed_ms": elapsed,
            "success": True
        }
    except urllib.error.HTTPError as e:
        elapsed = (datetime.now() - start_time).total_seconds() * 1000
        body = e.read() if hasattr(e, 'read') else b""
        return {
            "status": e.code,
            "reason": e.reason,
            "headers": dict(e.headers) if hasattr(e, 'headers') else {},
            "body": body,
            "url": url,
            "elapsed_ms": elapsed,
            "success": False,
            "error": str(e)
        }
    except Exception as e:
        return {
            "status": 0,
            "reason": str(e),
            "headers": {},
            "body": b"",
            "url": url,
            "elapsed_ms": 0,
            "success": False,
            "error": str(e)
        }

def print_response(response, verbose=False, format_output=True):
    """Print formatted response"""
    status_color = "✅" if 200 <= response["status"] < 300 else "⚠️" if response["status"] < 400 else "❌"
    
    print(f"\n{status_color} STATUS: {response['status']} {response['reason']}")
    print(f"⏱️  Time: {response['elapsed_ms']:.2f}ms")
    print(f"🔗 URL: {response['url']}")
    
    if verbose:
        print(f"\n📋 Response Headers:")
        print(format_headers(response["headers"]))
    
    content_type = response["headers"].get("Content-Type", "")
    body = response["body"]
    
    if body:
        print(f"\n📦 Response Body:")
        print("-" * 50)
        
        if "application/json" in content_type or format_output:
            formatted = format_json(body)
            print(formatted)
        else:
            print(body.decode('utf-8', errors='replace') if isinstance(body, bytes) else body)
        
        print("-" * 50)
        print(f"Size: {len(body)} bytes")

def save_to_history(request_data):
    """Save request to history"""
    history = load_json_file(HISTORY_FILE, [])
    entry = {
        "timestamp": datetime.now().isoformat(),
        "url": request_data.get("url"),
        "method": request_data.get("method"),
        "status": request_data.get("status")
    }
    history.insert(0, entry)
    history = history[:50]  # Keep last 50
    save_json_file(HISTORY_FILE, history)

def show_history():
    """Display request history"""
    history = load_json_file(HISTORY_FILE, [])
    if not history:
        print("📭 No history found")
        return
    
    print("📜 Recent Requests:")
    print("-" * 80)
    for i, entry in enumerate(history[:10], 1):
        status_icon = "✅" if 200 <= entry.get("status", 0) < 300 else "❌"
        print(f"{i}. {status_icon} {entry['method']:6} {entry['url'][:50]:50} ({entry['timestamp'][:19]})")

def save_request(name, request_data):
    """Save request for later use"""
    saved = load_json_file(SAVED_REQUESTS_FILE, {})
    saved[name] = {
        "url": request_data.get("url"),
        "method": request_data.get("method"),
        "headers": request_data.get("headers", {}),
        "data": request_data.get("data")
    }
    save_json_file(SAVED_REQUESTS_FILE, saved)
    print(f"💾 Saved request as '{name}'")

def load_request(name):
    """Load saved request"""
    saved = load_json_file(SAVED_REQUESTS_FILE, {})
    return saved.get(name)

def list_saved_requests():
    """List all saved requests"""
    saved = load_json_file(SAVED_REQUESTS_FILE, {})
    if not saved:
        print("📭 No saved requests")
        return
    
    print("💾 Saved Requests:")
    print("-" * 50)
    for name, data in saved.items():
        print(f"• {name}: {data['method']} {data['url'][:40]}")

def main():
    parser = argparse.ArgumentParser(
        description="PD API Tester - Developer-friendly HTTP client",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s https://api.github.com/users/octocat
  %(prog)s POST https://httpbin.org/post -d '{"key":"value"}' -H "Content-Type: application/json"
  %(prog)s GET https://api.example.com/data -H "Authorization: Bearer token123"
  %(prog)s --save myapi GET https://api.example.com/data
  %(prog)s --load myapi
  %(prog)s --history
        """
    )
    
    parser.add_argument("method", nargs="?", help="HTTP method (GET, POST, PUT, DELETE, PATCH)")
    parser.add_argument("url", nargs="?", help="URL to request")
    parser.add_argument("-d", "--data", help="Request body data")
    parser.add_argument("-H", "--header", action="append", help="HTTP header (can be used multiple times)")
    parser.add_argument("-v", "--verbose", action="store_true", help="Verbose output with headers")
    parser.add_argument("-k", "--insecure", action="store_true", help="Allow insecure SSL connections")
    parser.add_argument("-t", "--timeout", type=int, default=30, help="Request timeout in seconds (default: 30)")
    parser.add_argument("-r", "--raw", action="store_true", help="Raw output without formatting")
    parser.add_argument("--save", metavar="NAME", help="Save this request for later use")
    parser.add_argument("--load", metavar="NAME", help="Load a saved request")
    parser.add_argument("--history", action="store_true", help="Show request history")
    parser.add_argument("--saved", action="store_true", help="List saved requests")
    
    args = parser.parse_args()
    
    # Handle history view
    if args.history:
        show_history()
        return
    
    # Handle saved requests list
    if args.saved:
        list_saved_requests()
        return
    
    # Handle loading saved request
    if args.load:
        saved = load_request(args.load)
        if not saved:
            print(f"❌ Saved request '{args.load}' not found")
            return
        args.url = saved.get("url")
        args.method = saved.get("method", "GET")
        args.data = saved.get("data")
        args.header = []
        for key, value in saved.get("headers", {}).items():
            args.header.append(f"{key}: {value}")
        print(f"📂 Loaded request: {args.load}")
    
    # Validate URL
    if not args.url:
        parser.print_help()
        sys.exit(1)
    
    # Default method
    if not args.method:
        args.method = "GET"
    
    method = args.method.upper()
    
    # Parse headers
    headers = {}
    if args.header:
        for header in args.header:
            if ":" in header:
                key, value = header.split(":", 1)
                headers[key.strip()] = value.strip()
    
    # Prepare data
    data = None
    if args.data:
        if isinstance(args.data, str):
            data = args.data.encode('utf-8')
        else:
            data = args.data
    
    # Auto-set Content-Type for JSON data
    if data and args.data and args.data.strip().startswith(("{", "[")):
        if "Content-Type" not in headers:
            headers["Content-Type"] = "application/json"
    
    print(f"🚀 {method} {args.url}")
    if args.verbose:
        print(f"📤 Request Headers:")
        for key, value in headers.items():
            print(f"  {key}: {value}")
        if data:
            print(f"📦 Request Body:\n{args.data}")
    
    # Make request
    response = make_request(args.url, method, headers, data, args.timeout, args.insecure)
    
    # Print response
    print_response(response, args.verbose, not args.raw)
    
    # Save to history
    save_to_history({
        "url": args.url,
        "method": method,
        "status": response.get("status", 0)
    })
    
    # Save request if requested
    if args.save:
        save_request(args.save, {
            "url": args.url,
            "method": method,
            "headers": headers,
            "data": args.data
        })
    
    # Exit with error code if request failed
    if not response["success"]:
        sys.exit(1)
    
    print("\n" + "="*60)
    print("📊 Testing APIs locally? Get production monitoring with Sentry")
    print("   Free tier available: https://sentry.io/signup/ [affiliate]")
    print("="*60)

if __name__ == "__main__":
    main()
