#!/usr/bin/env python3
"""
regextest — Regex pattern tester
Tool #67 — Free CLI Tool for PD Researcher
"""

import argparse
import re
import sys


def test_regex(pattern, text, flags=0):
    """Test regex pattern against text."""
    try:
        compiled = re.compile(pattern, flags)
        matches = list(compiled.finditer(text))
        return matches, None
    except re.error as e:
        return None, f"Invalid regex: {e}"


def get_flags(args):
    """Get regex flags from arguments."""
    flags = 0
    if args.ignore_case:
        flags |= re.IGNORECASE
    if args.multiline:
        flags |= re.MULTILINE
    if args.dotall:
        flags |= re.DOTALL
    return flags


def main():
    parser = argparse.ArgumentParser(
        description='Test regex patterns against text',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  regextest "\\d+" "abc123def"              # Find numbers
  regextest "^hello" "hello world" -m      # Match at start
  regextest "(\\w+)@(\\w+)" "test@example.com" --groups
  echo "test data" | regextest "\\w+" -     # Read text from stdin
        """
    )
    
    parser.add_argument('pattern', help='Regex pattern')
    parser.add_argument('text', help='Text to test, or - for stdin')
    parser.add_argument('-i', '--ignore-case', action='store_true',
                       help='Case-insensitive matching')
    parser.add_argument('-m', '--multiline', action='store_true',
                       help='Multiline mode (^ and $ match lines)')
    parser.add_argument('-s', '--dotall', action='store_true',
                       help='Dot matches newlines')
    parser.add_argument('-g', '--groups', action='store_true',
                       help='Show capture groups')
    parser.add_argument('-r', '--replace',
                       help='Replace matches with this string')
    parser.add_argument('--count', action='store_true',
                       help='Count matches only')
    parser.add_argument('--split', action='store_true',
                       help='Split text by pattern')
    
    args = parser.parse_args()
    
    # Get text input
    if args.text == '-':
        text = sys.stdin.read()
    else:
        text = args.text
    
    flags = get_flags(args)
    
    # Handle split mode
    if args.split:
        parts = re.split(args.pattern, text, flags=flags)
        for i, part in enumerate(parts):
            print(f"[{i}] {repr(part)}")
        return
    
    # Handle replace mode
    if args.replace is not None:
        result = re.sub(args.pattern, args.replace, text, flags=flags)
        print(result)
        return
    
    # Test pattern
    matches, error = test_regex(args.pattern, text, flags)
    
    if error:
        print(error, file=sys.stderr)
        sys.exit(1)
    
    if args.count:
        print(len(matches))
        return
    
    if not matches:
        print("No matches found")
        sys.exit(1)
    
    # Show matches
    print(f"Found {len(matches)} match(es):\n")
    
    for i, match in enumerate(matches, 1):
        print(f"Match {i}:")
        print(f"  Full match: {repr(match.group())}")
        print(f"  Position:   {match.start()}-{match.end()}")
        
        if args.groups and match.groups():
            for j, group in enumerate(match.groups(), 1):
                print(f"  Group {j}:    {repr(group)}")
        print()


if __name__ == '__main__':
    main()
