#!/usr/bin/env python3
"""
base64tool — Base64 encoder/decoder
Tool #64 — Free CLI Tool for PD Researcher
"""

import argparse
import base64
import sys


def encode(data, url_safe=False):
    """Encode data to base64."""
    if isinstance(data, str):
        data = data.encode('utf-8')
    
    if url_safe:
        return base64.urlsafe_b64encode(data).decode('ascii')
    else:
        return base64.b64encode(data).decode('ascii')


def decode(data, url_safe=False):
    """Decode base64 data."""
    try:
        if url_safe:
            return base64.urlsafe_b64decode(data).decode('utf-8')
        else:
            return base64.b64decode(data).decode('utf-8')
    except Exception as e:
        return f"Error decoding: {e}"


def encode_file(filepath, url_safe=False):
    """Encode file to base64."""
    try:
        with open(filepath, 'rb') as f:
            return encode(f.read(), url_safe)
    except FileNotFoundError:
        return f"Error: File not found: {filepath}"


def decode_to_file(data, output_path, url_safe=False):
    """Decode base64 to file."""
    try:
        if url_safe:
            decoded = base64.urlsafe_b64decode(data)
        else:
            decoded = base64.b64decode(data)
        
        with open(output_path, 'wb') as f:
            f.write(decoded)
        return f"Decoded to: {output_path}"
    except Exception as e:
        return f"Error: {e}"


def main():
    parser = argparse.ArgumentParser(
        description='Base64 encoder/decoder',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  base64tool "hello world"               # Encode string
  base64tool "aGVsbG8=" -d               # Decode string
  base64tool file.txt -f                 # Encode file
  base64tool "data" -u                   # URL-safe encoding
  echo "hello" | base64tool -            # Encode from stdin
  cat data.b64 | base64tool -d -         # Decode from stdin
        """
    )
    
    parser.add_argument('input', help='Data to process, file path, or - for stdin')
    parser.add_argument('-d', '--decode', action='store_true',
                       help='Decode instead of encode')
    parser.add_argument('-f', '--file', action='store_true',
                       help='Treat input as file path')
    parser.add_argument('-u', '--url-safe', action='store_true',
                       help='Use URL-safe base64')
    parser.add_argument('-o', '--output',
                       help='Output file (for decode mode)')
    parser.add_argument('--no-newline', action='store_true',
                       help='Do not add newline to output')
    
    args = parser.parse_args()
    
    # Get input data
    if args.input == '-':
        data = sys.stdin.read()
    elif args.file:
        if args.decode:
            # For decoding file, read as text
            try:
                with open(args.input, 'r') as f:
                    data = f.read().strip()
            except FileNotFoundError:
                print(f"Error: File not found: {args.input}", file=sys.stderr)
                sys.exit(1)
        else:
            # Encoding file
            result = encode_file(args.input, args.url_safe)
            if result.startswith("Error:"):
                print(result, file=sys.stderr)
                sys.exit(1)
            print(result, end='' if args.no_newline else '\n')
            return
    else:
        data = args.input
    
    # Process
    if args.decode:
        result = decode(data.strip(), args.url_safe)
        if result.startswith("Error:"):
            print(result, file=sys.stderr)
            sys.exit(1)
        if args.output:
            with open(args.output, 'w') as f:
                f.write(result)
            print(f"Decoded to: {args.output}")
        else:
            print(result, end='' if args.no_newline else '\n')
    else:
        result = encode(data, args.url_safe)
        print(result, end='' if args.no_newline else '\n')


if __name__ == '__main__':
    main()

    # Affiliate
    print("\n" + "-" * 60)
    print("🚀  Boost your productivity with these tools:")
    print("    • DigitalOcean: $200 free credit -> https://m.do.co/c/pdresearcher")
    print("    • JetBrains IDEs: The best Python tools -> https://www.jetbrains.com/?utm_source=pdresearcher")
    print("-" * 60)
