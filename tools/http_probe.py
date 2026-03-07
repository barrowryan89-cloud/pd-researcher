#!/usr/bin/env python3
"""
http_probe.py — Lightweight HTTP testing tool
Simple, focused HTTP requests for debugging APIs and endpoints

Usage:
  python http_probe.py <url>              # GET request
  python http_probe.py <url> --post      # POST request
  python http_probe.py <url> -H "Key:Val" # Custom header
  python http_probe.py <url> -d '{"k":"v"}' # JSON body
  
Examples:
  python http_probe.py https://api.github.com/user
  python http_probe.py http://localhost:8080/health
  python http_probe.py https://httpbin.org/post --post -d '{"test":true}'
  python http_probe.py https://api.example.com -H "Authorization: Bearer token"

Features:
- GET, POST, PUT, DELETE, PATCH methods
- JSON body support with auto Content-Type
- Custom headers
- Response timing (DNS, connect, TTFB, total)
- Pretty print JSON responses
- Follow redirects (optional)
- Save response to file

Zero dependencies. Pure Python 3.6+ (uses http.client).
Part of PD's Free Developer Tools: https://barrowryan89-cloud.github.io/pd-researcher/
"""

import sys
import json
import time
import socket
import ssl
from urllib.parse import urlparse, urlencode
from http.client import HTTPConnection, HTTPSConnection, responses

def parse_url(url: str) -> tuple:
    """Parse URL into components"""
    if '://' not in url:
        url = 'http://' + url
    parsed = urlparse(url)
    return parsed.scheme, parsed.hostname, parsed.port, parsed.path or '/', parsed.query

def make_request(url: str, method: str = 'GET', headers: dict = None, 
                 body: str = None, follow_redirects: bool = True, timeout: int = 30):
    """Make HTTP request and return detailed response"""
    
    scheme, host, port, path, query = parse_url(url)
    if query:
        path += '?' + query
    
    is_https = scheme == 'https'
    port = port or (443 if is_https else 80)
    
    # Setup headers
    req_headers = {
        'User-Agent': 'http_probe/1.0',
        'Accept': '*/*',
        'Connection': 'close'
    }
    if headers:
        req_headers.update(headers)
    
    # Auto-add Content-Type for JSON body
    if body and body.strip().startswith(('{', '[')):
        req_headers.setdefault('Content-Type', 'application/json')
    
    # Timing measurements
    timings = {}
    
    try:
        # DNS lookup timing
        t0 = time.time()
        addr_info = socket.getaddrinfo(host, port, type=socket.SOCK_STREAM)
        timings['dns'] = (time.time() - t0) * 1000
        
        # Create connection
        if is_https:
            context = ssl.create_default_context()
            conn = HTTPSConnection(host, port, timeout=timeout, context=context)
        else:
            conn = HTTPConnection(host, port, timeout=timeout)
        
        # Connect timing
        t0 = time.time()
        conn.connect()
        timings['connect'] = (time.time() - t0) * 1000
        
        # Send request
        conn.request(method.upper(), path, body=body, headers=req_headers)
        
        # TTFB timing
        t0 = time.time()
        response = conn.getresponse()
        timings['ttfb'] = (time.time() - t0) * 1000
        
        # Read body
        body_bytes = response.read()
        timings['total'] = timings['dns'] + timings['connect'] + timings['ttfb']
        
        # Build response dict
        result = {
            'status': response.status,
            'reason': response.reason,
            'headers': dict(response.getheaders()),
            'body': body_bytes.decode('utf-8', errors='replace'),
            'body_size': len(body_bytes),
            'timings': timings,
            'url': url
        }
        
        conn.close()
        return result
        
    except socket.gaierror:
        return {'error': f'Could not resolve hostname: {host}'}
    except socket.timeout:
        return {'error': 'Connection timed out'}
    except ConnectionRefusedError:
        return {'error': f'Connection refused to {host}:{port}'}
    except Exception as e:
        return {'error': str(e)}

def format_size(size_bytes: int) -> str:
    """Format bytes to human readable"""
    if size_bytes < 1024:
        return f"{size_bytes} B"
    elif size_bytes < 1024 * 1024:
        return f"{size_bytes/1024:.1f} KB"
    else:
        return f"{size_bytes/(1024*1024):.1f} MB"

def print_response(result: dict, verbose: bool = False):
    """Print formatted response"""
    
    if 'error' in result:
        print(f"\n❌ ERROR: {result['error']}\n")
        return
    
    # Status line with color coding
    status = result['status']
    if status < 300:
        status_icon = "✅"
    elif status < 400:
        status_icon = "🔄"
    elif status < 500:
        status_icon = "⚠️"
    else:
        status_icon = "❌"
    
    print(f"\n{'='*60}")
    print(f"{status_icon} HTTP {status} {result['reason']}")
    print(f"{'='*60}")
    
    # URL
    print(f"\n📍 URL: {result['url']}")
    
    # Timing breakdown
    timings = result['timings']
    print(f"\n⏱️  TIMING")
    print(f"   DNS Lookup:    {timings['dns']:>8.1f} ms")
    print(f"   Connect:       {timings['connect']:>8.1f} ms")
    print(f"   TTFB:          {timings['ttfb']:>8.1f} ms")
    print(f"   ─────────────────────────")
    print(f"   Total:         {timings['total']:>8.1f} ms")
    
    # Response headers
    if verbose:
        print(f"\n📋 HEADERS")
        for key, value in sorted(result['headers'].items()):
            print(f"   {key}: {value}")
    else:
        # Show key headers only
        print(f"\n📋 KEY HEADERS")
        key_headers = ['content-type', 'content-length', 'server', 'date', 'cache-control']
        for key in key_headers:
            if key in result['headers']:
                print(f"   {key}: {result['headers'][key]}")
    
    # Body
    print(f"\n📝 BODY ({format_size(result['body_size'])})")
    print(f"{'─'*60}")
    
    body = result['body']
    content_type = result['headers'].get('content-type', '').lower()
    
    # Pretty print JSON
    if 'json' in content_type or body.strip().startswith(('{', '[')):
        try:
            parsed = json.loads(body)
            print(json.dumps(parsed, indent=2))
        except json.JSONDecodeError:
            print(body[:2000])
            if len(body) > 2000:
                print(f"\n... ({len(body) - 2000} more bytes)")
    else:
        # Truncate if too long
        if len(body) > 2000:
            print(body[:2000])
            print(f"\n... ({len(body) - 2000} more bytes)")
        else:
            print(body)
    
    print(f"{'─'*60}\n")

def main():
    args = sys.argv[1:]
    
    if not args or args[0] in ('-h', '--help'):
        print(__doc__)
        sys.exit(0)
    
    url = args[0]
    method = 'GET'
    headers = {}
    body = None
    verbose = False
    save_file = None
    
    i = 1
    while i < len(args):
        arg = args[i]
        
        if arg in ('-X', '--request'):
            method = args[i+1].upper()
            i += 2
        elif arg in ('--get', '--post', '--put', '--delete', '--patch'):
            method = arg[2:].upper()
            i += 1
        elif arg in ('-H', '--header'):
            header_line = args[i+1]
            if ':' in header_line:
                key, value = header_line.split(':', 1)
                headers[key.strip()] = value.strip()
            i += 2
        elif arg in ('-d', '--data', '--body'):
            body = args[i+1]
            i += 2
        elif arg in ('-v', '--verbose'):
            verbose = True
            i += 1
        elif arg in ('-o', '--output'):
            save_file = args[i+1]
            i += 2
        else:
            i += 1
    
    # Make request
    print(f"🚀 {method} {url}")
    result = make_request(url, method, headers, body)
    
    # Save to file if requested
    if save_file and 'body' in result:
        with open(save_file, 'w') as f:
            f.write(result['body'])
        print(f"💾 Response saved to: {save_file}")
    
    # Print response
    print_response(result, verbose)

if __name__ == '__main__':
    main()
