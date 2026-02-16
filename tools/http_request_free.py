#!/usr/bin/env python3
"""
HTTP Request Tool - Free Tool
Make HTTP requests from the command line
Free version: GET/POST requests with headers
Paid upgrade: All HTTP methods, auth, sessions, scripting

Usage: python3 http_request_free.py <url> [method] [data]
"""

import sys
import urllib.request
import urllib.parse
import json

def make_request(url, method='GET', data=None, headers=None):
    """Make HTTP request"""
    try:
        req = urllib.request.Request(url, method=method)
        
        # Add headers
        req.add_header('User-Agent', 'PD_Researcher_HTTP_Tool/1.0')
        if headers:
            for key, value in headers.items():
                req.add_header(key, value)
        
        # Add data for POST/PUT
        if data and method in ['POST', 'PUT', 'PATCH']:
            if isinstance(data, dict):
                data = json.dumps(data).encode('utf-8')
                req.add_header('Content-Type', 'application/json')
            else:
                data = data.encode('utf-8')
        
        with urllib.request.urlopen(req, data=data, timeout=30) as response:
            body = response.read().decode('utf-8')
            return {
                'status': response.status,
                'headers': dict(response.headers),
                'body': body[:2000]  # Limit body size
            }
    except urllib.error.HTTPError as e:
        return {
            'status': e.code,
            'headers': dict(e.headers),
            'body': e.read().decode('utf-8')[:500]
        }
    except Exception as e:
        return {'error': str(e)}

def print_banner():
    print("""
╔════════════════════════════════════════════════════════════╗
║                  HTTP REQUEST TOOL v1.0                    ║
║              Free Tool by Sand Street Holdings             ║
╠════════════════════════════════════════════════════════════╣
║  Make HTTP requests from the command line                  ║
║                                                            ║
║  💎 Want more power?                                       ║
║     → All HTTP methods (PUT, DELETE, PATCH)                ║
║     → Authentication (Bearer, Basic, OAuth)                ║
║     → Custom headers and cookies                           ║
║     → Response saving and scripting                        ║
║     → Request chaining and sessions                        ║
║     → Check out PD_Researcher v1 ($29)                     ║
║        Solana: FEKY6bDoqBnsQZVT3XbEYS4b1DJ8QoA64G5hXycfTAhQ ║
╚════════════════════════════════════════════════════════════╝
""")

def main():
    print_banner()
    
    if len(sys.argv) < 2:
        print("❌ No URL provided.")
        print("\nUsage:")
        print("  python3 http_request_free.py https://api.example.com/data")
        print("  python3 http_request_free.py https://api.example.com/data POST '{\"key\":\"value\"}'")
        sys.exit(1)
    
    url = sys.argv[1]
    method = sys.argv[2].upper() if len(sys.argv) > 2 else 'GET'
    data = sys.argv[3] if len(sys.argv) > 3 else None
    
    print(f"🔄 {method} {url}\n")
    
    result = make_request(url, method, data)
    
    if 'error' in result:
        print(f"❌ Error: {result['error']}")
        sys.exit(1)
    
    print(f"{'='*60}")
    print(f"📊 RESPONSE")
    print(f"{'='*60}")
    print(f"\nStatus: {result['status']}")
    
    print(f"\nHeaders:")
    for key, value in list(result['headers'].items())[:10]:
        print(f"  {key}: {value}")
    
    print(f"\nBody (truncated):")
    print(result['body'][:1000])
    if len(result['body']) > 1000:
        print(f"\n... ({len(result['body'])} characters total)")
    
    print(f"\n{'='*60}")
    print("\n💡 Want authentication and scripting support?")
    print("   Upgrade to PD_Researcher v1 for advanced HTTP tools")
    print("   Pay with crypto: FEKY6bDoqBnsQZVT3XbEYS4b1DJ8QoA64G5hXycfTAhQ")
    print("="*60)

if __name__ == "__main__":
    main()
