#!/usr/bin/env python3
"""
URL Parser & Query Builder - Tool #58
Parse, analyze, encode, decode, and manipulate URLs.
Part of the PD Researcher free tool collection.
"""

import argparse
import sys
import json
from urllib.parse import urlparse, parse_qs, urlencode, quote, unquote, urlunparse
from collections import OrderedDict

def format_bytes(size):
    """Human readable bytes."""
    for unit in ['B', 'KB', 'MB']:
        if size < 1024:
            return f"{size:.1f} {unit}"
        size /= 1024
    return f"{size:.1f} GB"

def parse_url(url):
    """Parse URL into components."""
    try:
        parsed = urlparse(url)
        query_params = parse_qs(parsed.query, keep_blank_values=True)
        # Flatten single-value lists for cleaner output
        query_flat = {k: v[0] if len(v) == 1 else v for k, v in query_params.items()}
        
        result = {
            'scheme': parsed.scheme or None,
            'netloc': parsed.netloc or None,
            'hostname': parsed.hostname,
            'port': parsed.port,
            'path': parsed.path or '/',
            'params': parsed.params or None,
            'query': parsed.query or None,
            'query_params': query_flat,
            'fragment': parsed.fragment or None,
            'username': parsed.username,
            'password': parsed.password,
            'is_secure': parsed.scheme in ('https', 'ftps', 'sftp'),
            'is_ip': parsed.hostname and parsed.hostname.replace('.', '').isdigit() if parsed.hostname else False
        }
        return result
    except Exception as e:
        return {'error': str(e)}

def build_url(args):
    """Build URL from components."""
    try:
        # Handle query params
        query = None
        if args.query:
            params = OrderedDict()
            for q in args.query:
                if '=' in q:
                    k, v = q.split('=', 1)
                    params[k] = v
            query = urlencode(params)
        
        # Handle port in netloc
        netloc = args.netloc
        if args.port and netloc:
            netloc = f"{netloc}:{args.port}"
        
        parts = (
            args.scheme or 'https',
            netloc or '',
            args.path or '/',
            args.params or '',
            query or '',
            args.fragment or ''
        )
        return urlunparse(parts)
    except Exception as e:
        return f"Error building URL: {e}"

def encode_url(url, safe=''):
    """Percent-encode URL."""
    return quote(url, safe=safe)

def decode_url(url):
    """Percent-decode URL."""
    return unquote(url)

def analyze_url(url_data):
    """Generate analysis report."""
    if 'error' in url_data:
        return f"Error: {url_data['error']}"
    
    lines = []
    lines.append("=" * 60)
    lines.append("URL ANALYSIS REPORT")
    lines.append("=" * 60)
    
    # Basic info
    lines.append(f"\n📍 SCHEME:       {url_data['scheme'] or 'N/A'}")
    lines.append(f"🌐 HOSTNAME:     {url_data['hostname'] or 'N/A'}")
    if url_data['port']:
        lines.append(f"🔌 PORT:         {url_data['port']}")
    lines.append(f"📁 PATH:         {url_data['path']}")
    
    # Security
    lines.append(f"\n🔒 SECURE:       {'Yes' if url_data['is_secure'] else 'No'}")
    if url_data['is_ip']:
        lines.append("⚠️  NOTE:         IP address used (not recommended)")
    
    # Auth
    if url_data['username']:
        lines.append(f"\n👤 USERNAME:     {url_data['username']}")
        if url_data['password']:
            lines.append("🔑 PASSWORD:     [PRESENT - Security risk in URL!]")
    
    # Query params
    if url_data['query_params']:
        lines.append(f"\n📋 QUERY PARAMETERS ({len(url_data['query_params'])}):")
        for key, value in url_data['query_params'].items():
            val_str = str(value)[:50] + "..." if len(str(value)) > 50 else str(value)
            lines.append(f"   • {key}: {val_str}")
    
    # Fragment
    if url_data['fragment']:
        lines.append(f"\n🔗 FRAGMENT:     #{url_data['fragment']}")
    
    lines.append("\n" + "=" * 60)
    return "\n".join(lines)

def main():
    parser = argparse.ArgumentParser(
        description='URL Parser & Query Builder - Parse, analyze, and build URLs',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s parse "https://example.com/search?q=python&page=1"
  %(prog)s build --scheme https --netloc api.example.com --path /v1/users
  %(prog)s encode "hello world & more"
  %(prog)s decode "hello%20world%20%26%20more"
  echo "https://site.com" | %(prog)s parse -
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Command to run')
    
    # Parse command
    parse_parser = subparsers.add_parser('parse', help='Parse and analyze a URL')
    parse_parser.add_argument('url', help='URL to parse (use - for stdin)')
    parse_parser.add_argument('--json', '-j', action='store_true', help='Output as JSON')
    
    # Build command
    build_parser = subparsers.add_parser('build', help='Build URL from components')
    build_parser.add_argument('--scheme', '-s', default='https', help='URL scheme (default: https)')
    build_parser.add_argument('--netloc', '-n', help='Network location (host:port)')
    build_parser.add_argument('--port', '-p', type=int, help='Port number')
    build_parser.add_argument('--path', help='URL path')
    build_parser.add_argument('--query', '-q', action='append', help='Query params (key=value)')
    build_parser.add_argument('--fragment', '-f', help='Fragment/anchor')
    build_parser.add_argument('--params', help='Parameters (rarely used)')
    
    # Encode command
    encode_parser = subparsers.add_parser('encode', help='Percent-encode string/URL')
    encode_parser.add_argument('text', help='Text to encode (use - for stdin)')
    encode_parser.add_argument('--safe', default='/', help='Safe characters (default: /)')
    
    # Decode command
    decode_parser = subparsers.add_parser('decode', help='Percent-decode string/URL')
    decode_parser.add_argument('text', help='Text to decode (use - for stdin)')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    # Handle stdin
    if hasattr(args, 'url') and args.url == '-':
        args.url = sys.stdin.read().strip()
    if hasattr(args, 'text') and args.text == '-':
        args.text = sys.stdin.read().strip()
    
    if args.command == 'parse':
        result = parse_url(args.url)
        if args.json:
            print(json.dumps(result, indent=2, default=str))
        else:
            print(analyze_url(result))
    
    elif args.command == 'build':
        url = build_url(args)
        print(url)
    
    elif args.command == 'encode':
        print(encode_url(args.text, safe=args.safe))
    
    elif args.command == 'decode':
        print(decode_url(args.text))

if __name__ == '__main__':
    main()
