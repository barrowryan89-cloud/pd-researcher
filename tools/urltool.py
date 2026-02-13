#!/usr/bin/env python3
"""
urltool - URL encode/decode utility
Part of PD Researcher Tool Suite
"""

import sys
import argparse
from urllib.parse import quote, unquote, urlparse, parse_qs

def encode_url(text, safe=''):
    """URL encode a string."""
    return quote(text, safe=safe)

def decode_url(text):
    """URL decode a string."""
    return unquote(text)

def parse_url(url):
    """Parse URL into components."""
    parsed = urlparse(url)
    query_params = parse_qs(parsed.query)
    return {
        'scheme': parsed.scheme,
        'netloc': parsed.netloc,
        'path': parsed.path,
        'params': parsed.params,
        'query': parsed.query,
        'fragment': parsed.fragment,
        'query_params': query_params,
        'hostname': parsed.hostname,
        'port': parsed.port
    }

def main():
    parser = argparse.ArgumentParser(
        description='URL encode/decode utility',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s encode "hello world"
  %(prog)s decode "hello%20world"
  %(prog)s parse "https://example.com/path?q=test#frag"
  echo "hello world" | %(prog)s encode
        """
    )
    parser.add_argument('action', choices=['encode', 'decode', 'parse'],
                       help='Action to perform')
    parser.add_argument('input', nargs='?', help='Input string (or use stdin)')
    parser.add_argument('-s', '--safe', default='', help='Safe characters for encoding')
    parser.add_argument('-a', '--all', action='store_true', help='Show all transformations')
    
    args = parser.parse_args()
    
    # Read input
    if args.input:
        text = args.input
    elif not sys.stdin.isatty():
        text = sys.stdin.read()
    else:
        parser.print_help()
        sys.exit(1)
    
    text = text.strip()
    
    if args.action == 'encode':
        encoded = encode_url(text, args.safe)
        print(encoded)
        
        if args.all:
            print(f"\nOriginal: {text}")
            print(f"Encoded:  {encoded}")
            print(f"Length:   {len(encoded)} chars")
    
    elif args.action == 'decode':
        decoded = decode_url(text)
        print(decoded)
        
        if args.all:
            print(f"\nOriginal: {text}")
            print(f"Decoded:  {decoded}")
            print(f"Length:   {len(decoded)} chars")
    
    elif args.action == 'parse':
        if not text.startswith(('http://', 'https://')):
            text = 'https://' + text
        
        parsed = parse_url(text)
        
        print(f"URL:      {text}")
        print(f"Scheme:   {parsed['scheme']}")
        print(f"Hostname: {parsed['hostname']}")
        print(f"Port:     {parsed['port'] or 'default'}")
        print(f"Path:     {parsed['path'] or '/'}")
        print(f"Query:    {parsed['query'] or 'none'}")
        print(f"Fragment: {parsed['fragment'] or 'none'}")
        
        if parsed['query_params']:
            print(f"\nQuery Parameters:")
            for key, values in parsed['query_params'].items():
                for value in values:
                    print(f"  {key} = {value}")

if __name__ == '__main__':
    main()
