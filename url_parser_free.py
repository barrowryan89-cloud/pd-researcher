#!/usr/bin/env python3
"""
url_parser_free.py - URL Parser
Parse URLs into components: scheme, host, path, query, fragment.
Zero dependencies. Pure Python 3.
"""

import sys
from urllib.parse import urlparse, parse_qs, unquote

def parse_url(url: str):
    """Parse URL into components."""
    # Ensure URL has scheme
    if '://' not in url:
        url = 'https://' + url
    
    parsed = urlparse(url)
    
    # Parse query parameters
    params = parse_qs(parsed.query, keep_blank_values=True)
    # Flatten single-value lists
    params = {k: v[0] if len(v) == 1 else v for k, v in params.items()}
    
    return {
        'scheme': parsed.scheme,
        'netloc': parsed.netloc,
        'host': parsed.hostname,
        'port': parsed.port,
        'path': parsed.path,
        'params': parsed.params,
        'query': parsed.query,
        'query_params': params,
        'fragment': parsed.fragment,
        'username': parsed.username,
        'password': parsed.password,
    }

def print_url_info(url: str):
    """Print detailed URL information."""
    print(f"🔗 URL Analysis")
    print("=" * 60)
    print(f"\nOriginal: {url}")
    
    try:
        parts = parse_url(url)
    except Exception as e:
        print(f"\n❌ Error parsing URL: {e}")
        return
    
    print(f"\n📋 Components:")
    print(f"  Scheme:   {parts['scheme']}")
    print(f"  Host:     {parts['host']}")
    if parts['port']:
        print(f"  Port:     {parts['port']}")
    
    if parts['username']:
        auth = parts['username']
        if parts['password']:
            auth += ":***"
        print(f"  Auth:     {auth}")
    
    if parts['path'] and parts['path'] != '/':
        print(f"  Path:     {parts['path']}")
        # Show path segments
        segments = [s for s in parts['path'].split('/') if s]
        if segments:
            print(f"  Segments: {' / '.join(segments)}")
    
    if parts['query']:
        print(f"\n❓ Query String:")
        print(f"  Raw: {parts['query']}")
        print(f"\n  Parameters ({len(parts['query_params'])}):")
        for key, value in parts['query_params'].items():
            # Truncate long values
            display = value[:60] + "..." if len(str(value)) > 60 else value
            print(f"    {key}: {display}")
    
    if parts['fragment']:
        print(f"\n📌 Fragment:")
        print(f"  #{parts['fragment']}")
    
    # Reconstruct URL
    print(f"\n🔄 Reconstructed:")
    reconstructed = f"{parts['scheme']}://"
    if parts['username']:
        reconstructed += parts['username']
        if parts['password']:
            reconstructed += ":***"
        reconstructed += "@"
    reconstructed += parts['host']
    if parts['port']:
        reconstructed += f":{parts['port']}"
    reconstructed += parts['path'] or '/'
    if parts['query']:
        reconstructed += f"?{parts['query']}"
    if parts['fragment']:
        reconstructed += f"#{parts['fragment']}"
    print(f"  {reconstructed}")
    
    print("\n" + "=" * 60)

def main():
    if len(sys.argv) < 2:
        print("Usage: url_parser_free.py <url>")
        print("\nExamples:")
        print('  url_parser_free.py https://example.com')
        print('  url_parser_free.py example.com/path?foo=bar#section')
        print('  url_parser_free.py "https://api.example.com/v1/users?id=123"')
        sys.exit(1)
    
    url = sys.argv[1]
    print_url_info(url)

if __name__ == "__main__":
    main()
