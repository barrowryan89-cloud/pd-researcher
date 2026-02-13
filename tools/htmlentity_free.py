#!/usr/bin/env python3
"""
htmlentity — HTML entity encoder/decoder
Tool #65 — Free CLI Tool for PD Researcher
"""

import argparse
import html
import sys


def encode(text):
    """Encode special characters to HTML entities."""
    return html.escape(text)


def decode(text):
    """Decode HTML entities to characters."""
    try:
        return html.unescape(text)
    except Exception as e:
        return f"Error: {e}"


def encode_all(text):
    """Encode all characters to numeric entities."""
    return ''.join(f'&#x{ord(c):X};' if ord(c) > 127 else c for c in text)


def main():
    parser = argparse.ArgumentParser(
        description='HTML entity encoder/decoder',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  htmlentity "<script>alert('xss')</script>"    # Encode HTML
  htmlentity "&lt;div&gt;" -d                   # Decode HTML
  htmlentity "café" --numeric                   # Encode non-ASCII
  echo "<p>Hello</p>" | htmlentity -            # Read from stdin
        """
    )
    
    parser.add_argument('text', help='Text to process, or - for stdin')
    parser.add_argument('-d', '--decode', action='store_true',
                       help='Decode instead of encode')
    parser.add_argument('-n', '--numeric', action='store_true',
                       help='Encode non-ASCII to numeric entities')
    parser.add_argument('--no-newline', action='store_true',
                       help='Do not add newline to output')
    
    args = parser.parse_args()
    
    # Get input
    if args.text == '-':
        text = sys.stdin.read()
    else:
        text = args.text
    
    # Process
    if args.decode:
        result = decode(text)
    elif args.numeric:
        result = encode_all(text)
    else:
        result = encode(text)
    
    if result.startswith("Error:"):
        print(result, file=sys.stderr)
        sys.exit(1)
    
    print(result, end='' if args.no_newline else '')


if __name__ == '__main__':
    main()
