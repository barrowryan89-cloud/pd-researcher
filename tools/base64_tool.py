#!/usr/bin/env python3
"""
base64_tool.py — Base64 encode/decode utility
Tool #37 in the PD Researcher free tools collection
"""

import argparse
import base64
import sys
from pathlib import Path


def encode_text(text: str, url_safe: bool = False) -> str:
    """Encode text to base64."""
    encoded = base64.urlsafe_b64encode(text.encode()) if url_safe else base64.b64encode(text.encode())
    return encoded.decode()


def decode_text(encoded: str, url_safe: bool = False) -> str:
    """Decode base64 to text."""
    try:
        decoded = base64.urlsafe_b64decode(encoded.encode()) if url_safe else base64.b64decode(encoded.encode())
        return decoded.decode()
    except Exception as e:
        print(f"Error decoding: {e}", file=sys.stderr)
        sys.exit(1)


def encode_file(filepath: str, url_safe: bool = False) -> str:
    """Encode file contents to base64."""
    try:
        with open(filepath, 'rb') as f:
            content = f.read()
        encoded = base64.urlsafe_b64encode(content) if url_safe else base64.b64encode(content)
        return encoded.decode()
    except FileNotFoundError:
        print(f"File not found: {filepath}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error encoding file: {e}", file=sys.stderr)
        sys.exit(1)


def decode_to_file(encoded: str, output_path: str, url_safe: bool = False):
    """Decode base64 and save to file."""
    try:
        decoded = base64.urlsafe_b64decode(encoded.encode()) if url_safe else base64.b64decode(encoded.encode())
        with open(output_path, 'wb') as f:
            f.write(decoded)
        print(f"Decoded content saved to: {output_path}")
    except Exception as e:
        print(f"Error decoding to file: {e}", file=sys.stderr)
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(
        description="Base64 encode/decode utility",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s encode "Hello World"
  %(prog)s decode "SGVsbG8gV29ybGQ="
  %(prog)s encode --file image.png
  %(prog)s decode --file encoded.txt --output decoded.bin
  %(prog)s encode --url-safe "Hello/World"
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Command to run')
    
    # Encode command
    encode_parser = subparsers.add_parser('encode', help='Encode to base64')
    encode_parser.add_argument('input', nargs='?', help='Text to encode')
    encode_parser.add_argument('-f', '--file', help='File to encode')
    encode_parser.add_argument('-u', '--url-safe', action='store_true', help='Use URL-safe base64')
    
    # Decode command
    decode_parser = subparsers.add_parser('decode', help='Decode from base64')
    decode_parser.add_argument('input', nargs='?', help='Base64 text to decode')
    decode_parser.add_argument('-f', '--file', help='File containing base64 text')
    decode_parser.add_argument('-o', '--output', help='Output file for decoded content')
    decode_parser.add_argument('-u', '--url-safe', action='store_true', help='Use URL-safe base64')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    if args.command == 'encode':
        if args.file:
            result = encode_file(args.file, args.url_safe)
            print(result)
        elif args.input:
            result = encode_text(args.input, args.url_safe)
            print(result)
        else:
            # Read from stdin
            text = sys.stdin.read()
            result = encode_text(text, args.url_safe)
            print(result)
    
    elif args.command == 'decode':
        if args.file:
            with open(args.file, 'r') as f:
                encoded = f.read().strip()
            if args.output:
                decode_to_file(encoded, args.output, args.url_safe)
            else:
                result = decode_text(encoded, args.url_safe)
                print(result)
        elif args.input:
            if args.output:
                decode_to_file(args.input, args.output, args.url_safe)
            else:
                result = decode_text(args.input, args.url_safe)
                print(result)
        else:
            # Read from stdin
            encoded = sys.stdin.read().strip()
            if args.output:
                decode_to_file(encoded, args.output, args.url_safe)
            else:
                result = decode_text(encoded, args.url_safe)
                print(result)


if __name__ == '__main__':
    main()
