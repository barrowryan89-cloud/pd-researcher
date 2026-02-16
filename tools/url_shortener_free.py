#!/usr/bin/env python3
"""
Tool #32: URL Shortener
Shorten long URLs using is.gd API
"""

import sys
import urllib.request
import urllib.parse
import json


def shorten_url(long_url):
    """Shorten URL using is.gd API."""
    encoded = urllib.parse.quote(long_url, safe='')
    api_url = f"https://is.gd/create.php?format=json&url={encoded}"
    
    try:
        with urllib.request.urlopen(api_url, timeout=10) as resp:
            data = json.loads(resp.read().decode())
            if 'shorturl' in data:
                return data['shorturl']
            elif 'errorcode' in data:
                return f"Error: {data.get('errormessage', 'Unknown error')}"
            return None
    except Exception as e:
        return f"Error: {e}"


def main():
    if len(sys.argv) < 2 or sys.argv[1] in ('-h', '--help'):
        print("Usage: python3 url_shortener_free.py <long_url>")
        print("Example: python3 url_shortener_free.py https://example.com/very/long/url")
        sys.exit(0)
    
    long_url = sys.argv[1]
    
    if not long_url.startswith(('http://', 'https://')):
        print("Error: URL must start with http:// or https://")
        sys.exit(1)
    
    print(f"Shortening: {long_url}")
    print("-" * 50)
    
    result = shorten_url(long_url)
    
    if result and result.startswith('http'):
        print(f"✓ Short URL: {result}")
        print(f"  Original:  {long_url}")
    else:
        print(f"✗ Failed: {result}")


if __name__ == "__main__":
    main()
