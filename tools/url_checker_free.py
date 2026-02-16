#!/usr/bin/env python3
"""
URL Checker - Free Tool
Check if URLs are live, get status codes, response times
Free version: Single URL check
Paid upgrade: Batch processing, monitoring, alerts

Usage: python3 url_checker_free.py <url>
"""

import sys
import urllib.request
import urllib.error
import time
from urllib.parse import urlparse

def check_url(url, timeout=10):
    """Check a single URL"""
    start_time = time.time()
    
    try:
        req = urllib.request.Request(
            url,
            method='HEAD',
            headers={'User-Agent': 'Mozilla/5.0 (compatible; URLChecker/1.0)'}
        )
        
        with urllib.request.urlopen(req, timeout=timeout) as response:
            elapsed = (time.time() - start_time) * 1000
            return {
                'url': url,
                'status': response.status,
                'redirect': response.geturl() if response.geturl() != url else None,
                'content_type': response.headers.get('Content-Type', 'Unknown'),
                'response_time': round(elapsed, 2),
                'error': None
            }
            
    except urllib.error.HTTPError as e:
        elapsed = (time.time() - start_time) * 1000
        return {
            'url': url,
            'status': e.code,
            'redirect': None,
            'content_type': None,
            'response_time': round(elapsed, 2),
            'error': str(e.reason)
        }
    except Exception as e:
        return {
            'url': url,
            'status': None,
            'redirect': None,
            'content_type': None,
            'response_time': None,
            'error': str(e)
        }

def print_result(result):
    """Print formatted result"""
    status = result['status']
    status_icon = "✅" if status and 200 <= status < 300 else "❌" if status and status >= 400 else "⚠️"
    
    print(f"\n{status_icon} {result['url']}")
    print(f"   Status: {status if status else 'Failed'}")
    
    if result['redirect']:
        print(f"   Redirects to: {result['redirect']}")
    
    if result['response_time']:
        print(f"   Response time: {result['response_time']}ms")
    
    if result['content_type']:
        print(f"   Content-Type: {result['content_type']}")
    
    if result['error']:
        print(f"   Error: {result['error']}")

def print_banner():
    print("""
╔════════════════════════════════════════════════════════════╗
║                    URL CHECKER v1.0                        ║
║              Free Tool by Sand Street Holdings             ║
╠════════════════════════════════════════════════════════════╣
║  Check if websites are live, fast, and responding          ║
║                                                            ║
║  💎 Want more power?                                       ║
║     → Batch URL checking                                   ║
║     → Uptime monitoring                                    ║
║     → Response time tracking                               ║
║     → SSL certificate checks                               ║
║     → Check out PD_Researcher v1 ($29)                     ║
║        Solana: FEKY6bDoqBnsQZVT3XbEYS4b1DJ8QoA64G5hXycfTAhQ ║
╚════════════════════════════════════════════════════════════╝
""")

def main():
    print_banner()
    
    if len(sys.argv) < 2:
        print("❌ No URL provided.")
        print("\nUsage:")
        print("  python3 url_checker_free.py https://example.com")
        sys.exit(1)
    
    url = sys.argv[1]
    
    # Add scheme if missing
    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url
        print(f"📝 Added https:// → {url}\n")
    
    print(f"🔄 Checking: {url}\n")
    
    result = check_url(url)
    print_result(result)
    
    print("\n" + "="*60)
    print("\n💡 Want to check multiple URLs automatically?")
    print("   Upgrade to PD_Researcher v1 for batch monitoring")
    print("   Pay with crypto: FEKY6bDoqBnsQZVT3XbEYS4b1DJ8QoA64G5hXycfTAhQ")
    print("="*60)

if __name__ == "__main__":
    main()
