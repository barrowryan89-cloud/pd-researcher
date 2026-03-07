#!/usr/bin/env python3
"""
URL Encoder/Decoder — Tool #35
Encode and decode URLs, query parameters, and form data.
Part of the PD_Researcher free tool suite.
"""

import argparse
import sys
from urllib.parse import quote, unquote, parse_qs, urlencode, urlparse, urlunparse


def encode_url(url, safe='', encoding='utf-8'):
    """URL-encode a string."""
    return quote(url, safe=safe, encoding=encoding)


def decode_url(url, encoding='utf-8'):
    """URL-decode a string."""
    return unquote(url, encoding=encoding)


def encode_query(params):
    """Encode query parameters."""
    if isinstance(params, str):
        # Parse string like "key1=value1&key2=value2"
        parsed = parse_qs(params, keep_blank_values=True)
        return urlencode(parsed, doseq=True)
    return urlencode(params, doseq=True)


def decode_query(query_string):
    """Decode query parameters."""
    parsed = parse_qs(query_string, keep_blank_values=True)
    # Convert lists to single values where appropriate
    result = {}
    for k, v in parsed.items():
        result[k] = v[0] if len(v) == 1 else v
    return result


def parse_url(url):
    """Parse URL into components."""
    parsed = urlparse(url)
    return {
        'scheme': parsed.scheme,
        'netloc': parsed.netloc,
        'path': parsed.path,
        'params': parsed.params,
        'query': parsed.query,
        'fragment': parsed.fragment,
        'username': parsed.username,
        'password': parsed.password,
        'hostname': parsed.hostname,
        'port': parsed.port,
    }


def main():
    parser = argparse.ArgumentParser(
        description='URL encoder/decoder utility',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s encode "hello world"           # Encode: hello%20world
  %(prog)s decode "hello%20world"         # Decode: hello world
  %(prog)s parse "https://example.com"    # Parse URL components
  %(prog)s query-encode "key=value"       # Encode query string
  %(prog)s query-decode "key=value"       # Decode to key-value pairs
        """
    )
    parser.add_argument('action', choices=[
        'encode', 'decode', 'parse', 
        'query-encode', 'query-decode', 'qe', 'qd'
    ], help='Action to perform')
    parser.add_argument('input', nargs='?', help='Input string (or use --stdin)')
    parser.add_argument('--stdin', action='store_true', help='Read from stdin')
    parser.add_argument('--safe', default='', help='Characters to not encode')
    parser.add_argument('--plus', action='store_true', help='Use + for spaces (form encoding)')
    parser.add_argument('--component', choices=['path', 'query', 'fragment', 'userinfo'], 
                       help='URL component type for encoding')
    
    args = parser.parse_args()
    
    # Get input
    if args.stdin:
        text = sys.stdin.read().strip()
    elif args.input:
        text = args.input
    else:
        parser.error("Provide input or use --stdin")
    
    # Execute action
    if args.action == 'encode':
        safe = args.safe
        if args.component == 'path':
            safe = '/'
        elif args.component == 'query':
            safe = '&='
        elif args.component == 'fragment':
            safe = ''
        elif args.component == 'userinfo':
            safe = '@:'
        
        encoded = encode_url(text, safe=safe)
        if args.plus:
            encoded = encoded.replace('%20', '+')
        print(encoded)
    
    elif args.action == 'decode':
        if args.plus:
            text = text.replace('+', ' ')
        print(decode_url(text))
    
    elif args.action == 'parse':
        components = parse_url(text)
        max_len = max(len(k) for k in components.keys())
        for key, value in components.items():
            if value is not None:
                print(f"{key.ljust(max_len)}: {value}")
    
    elif args.action in ('query-encode', 'qe'):
        # Parse key=value pairs
        params = {}
        for pair in text.split('&'):
            if '=' in pair:
                k, v = pair.split('=', 1)
                params[k] = v
            elif pair:
                params[pair] = ''
        print(encode_query(params))
    
    elif args.action in ('query-decode', 'qd'):
        decoded = decode_query(text)
        for key, value in decoded.items():
            if isinstance(value, list):
                for v in value:
                    print(f"{key}={v}")
            else:
                print(f"{key}={value}")


if __name__ == '__main__':
    main()
