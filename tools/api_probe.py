#!/usr/bin/env python3
"""
api_probe - Quick HTTP API Testing CLI
Like curl but with pretty output and sensible defaults.
"""

import argparse
import json
import sys
import urllib.request
import urllib.error
import ssl
from urllib.parse import urlencode

def colorize(text, color):
    """Add color to text."""
    colors = {
        'green': '\033[92m',
        'yellow': '\033[93m',
        'red': '\033[91m',
        'blue': '\033[94m',
        'cyan': '\033[96m',
        'magenta': '\033[95m',
        'bold': '\033[1m',
        'dim': '\033[2m',
        'reset': '\033[0m'
    }
    return f"{colors.get(color, '')}{text}{colors['reset']}"

def format_bytes(size):
    """Format bytes to human readable."""
    for unit in ['B', 'KB', 'MB']:
        if size < 1024:
            return f"{size:.1f} {unit}"
        size /= 1024
    return f"{size:.1f} GB"

def get_status_icon(code):
    """Get emoji for HTTP status code."""
    if code < 200:
        return "⏳"
    elif code < 300:
        return "✅"
    elif code < 400:
        return "↪️"
    elif code < 500:
        return "❌"
    else:
        return "💥"

def get_status_color(code):
    """Get color for HTTP status code."""
    if code < 300:
        return 'green'
    elif code < 400:
        return 'yellow'
    else:
        return 'red'

def make_request(url, method='GET', headers=None, data=None, timeout=30, no_ssl_verify=False, follow_redirects=True):
    """Make HTTP request and return response."""
    
    # Build request
    req = urllib.request.Request(url, method=method)
    
    # Add default headers
    req.add_header('User-Agent', 'api_probe/1.0')
    
    # Add custom headers
    if headers:
        for header in headers:
            if header and ':' in header:
                key, value = header.split(':', 1)
                req.add_header(key.strip(), value.strip())
    
    # Add body data
    if data:
        if isinstance(data, str):
            data = data.encode('utf-8')
        req.data = data
    
    # Create SSL context
    ssl_context = ssl.create_default_context()
    if no_ssl_verify:
        ssl_context.check_hostname = False
        ssl_context.verify_mode = ssl.CERT_NONE
    
    # Build opener
    if not follow_redirects:
        opener = urllib.request.build_opener(
            urllib.request.HTTPHandler(),
            urllib.request.HTTPSHandler(context=ssl_context)
        )
    else:
        opener = urllib.request.build_opener(
            urllib.request.HTTPRedirectHandler(),
            urllib.request.HTTPHandler(),
            urllib.request.HTTPSHandler(context=ssl_context)
        )
    
    # Make request
    start_time = __import__('time').time()
    try:
        with opener.open(req, timeout=timeout) as response:
            elapsed = (__import__('time').time() - start_time) * 1000
            body = response.read()
            return {
                'status': response.getcode(),
                'headers': dict(response.headers),
                'body': body,
                'elapsed_ms': elapsed,
                'url': response.geturl()
            }
    except urllib.error.HTTPError as e:
        elapsed = (__import__('time').time() - start_time) * 1000
        body = e.read()
        return {
            'status': e.code,
            'headers': dict(e.headers),
            'body': body,
            'elapsed_ms': elapsed,
            'url': e.url,
            'error': str(e)
        }

def try_parse_json(data):
    """Try to parse data as JSON."""
    try:
        return json.loads(data.decode('utf-8'))
    except:
        return None

def print_response(response, args):
    """Pretty print response."""
    c = lambda text, color: text if args.no_color else colorize(text, color)
    
    status = response['status']
    icon = get_status_icon(status)
    color = get_status_color(status)
    
    # Status line
    print()
    print(c(f"{icon} HTTP {status} ", color) + c(f"({response['elapsed_ms']:.0f}ms)", 'dim'))
    
    # URL (if redirected)
    if response.get('url') != args.url:
        print(c(f"↪️  Final URL: {response['url']}", 'cyan'))
    
    print()
    
    # Headers
    if args.verbose or args.show_headers:
        print(c("📋 Response Headers:", 'bold'))
        print(c("-" * 40, 'dim'))
        for key, value in response['headers'].items():
            print(f"  {c(key, 'cyan')}: {value}")
        print()
    
    # Body
    body = response['body']
    if not body:
        print(c("📄 (Empty response body)", 'dim'))
        return
    
    content_type = response['headers'].get('Content-Type', '')
    
    # Try JSON first
    if 'json' in content_type or args.json:
        json_data = try_parse_json(body)
        if json_data:
            print(c("📄 JSON Response:", 'bold'))
            print(c("-" * 40, 'dim'))
            print(json.dumps(json_data, indent=2, ensure_ascii=False))
            print()
            return
    
    # Print as text
    try:
        text = body.decode('utf-8')
        if args.verbose:
            print(c("📄 Response Body:", 'bold'))
            print(c("-" * 40, 'dim'))
        print(text)
        if args.verbose:
            print()
    except UnicodeDecodeError:
        print(c(f"📦 Binary response ({format_bytes(len(body))})", 'yellow'))
        if args.verbose:
            print(c(f"   First 100 bytes (hex): {body[:100].hex()}", 'dim'))

def main():
    parser = argparse.ArgumentParser(
        description='🚀 Quick HTTP API testing with pretty output',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  api_probe https://api.github.com/users/octocat
  api_probe https://httpbin.org/post -X POST -d '{"key":"value"}' -H "Content-Type: application/json"
  api_probe https://api.example.com/data -H "Authorization: Bearer TOKEN"
  api_probe https://example.com/api -X PUT -d @payload.json
  api_probe https://httpbin.org/status/404  # See error handling
        """
    )
    parser.add_argument('url', help='URL to request')
    parser.add_argument('-X', '--method', default='GET', 
                        help='HTTP method (default: GET)')
    parser.add_argument('-H', '--header', action='append', dest='headers',
                        help='Add header (format: "Key: Value")')
    parser.add_argument('-d', '--data', 
                        help='Request body (use @file to read from file)')
    parser.add_argument('-j', '--json', action='store_true',
                        help='Force JSON output formatting')
    parser.add_argument('-v', '--verbose', action='store_true',
                        help='Verbose output (show all headers)')
    parser.add_argument('-i', '--show-headers', action='store_true', dest='show_headers',
                        help='Show response headers')
    parser.add_argument('-L', '--location', action='store_true', default=True,
                        help='Follow redirects (default: true)')
    parser.add_argument('--no-redirects', action='store_true',
                        help='Do not follow redirects')
    parser.add_argument('-k', '--insecure', action='store_true',
                        help='Disable SSL certificate verification')
    parser.add_argument('-t', '--timeout', type=int, default=30,
                        help='Request timeout in seconds (default: 30)')
    parser.add_argument('--no-color', action='store_true',
                        help='Disable colored output')
    
    args = parser.parse_args()
    
    # Handle @file syntax for data
    data = None
    if args.data:
        if args.data.startswith('@'):
            file_path = args.data[1:]
            try:
                with open(file_path, 'rb') as f:
                    data = f.read()
            except FileNotFoundError:
                print(f"❌ File not found: {file_path}")
                sys.exit(1)
        else:
            data = args.data.encode('utf-8')
    
    # Auto-add Content-Type for JSON data
    if data:
        has_content_type = args.headers and any(h.lower().startswith('content-type') for h in args.headers)
        if not has_content_type:
            try:
                json.loads(data.decode('utf-8'))
                args.headers = args.headers or []
                args.headers.append('Content-Type: application/json')
            except:
                pass
    
    # Make request
    try:
        response = make_request(
            args.url,
            method=args.method.upper(),
            headers=args.headers,
            data=data,
            timeout=args.timeout,
            no_ssl_verify=args.insecure,
            follow_redirects=not args.no_redirects
        )
        print_response(response, args)
    except urllib.error.URLError as e:
        print(f"❌ Request failed: {e}")
        sys.exit(1)
    except TimeoutError:
        print(f"⏱️  Request timed out after {args.timeout}s")
        sys.exit(1)
    
    print("\n🚀 Building an API? Host it reliably:")
    print("   → DigitalOcean: $200 free credit for new users — https://m.do.co/c/pdresearcher")
    print("   → Track API errors with Sentry: https://sentry.io [affiliate]")

if __name__ == '__main__':
    main()
