#!/usr/bin/env python3
"""
jsonfmt - JSON formatter and validator
Part of PD Researcher Tool Suite
"""

import sys
import json
import argparse
from collections import OrderedDict

def format_json(data, indent=2, sort_keys=False, compact=False):
    """Format JSON with specified options."""
    if compact:
        return json.dumps(data, separators=(',', ':'), sort_keys=sort_keys)
    return json.dumps(data, indent=indent, sort_keys=sort_keys, ensure_ascii=False)

def validate_json(text):
    """Validate JSON and return parsed data or raise error."""
    return json.loads(text, object_pairs_hook=OrderedDict)

def get_stats(data):
    """Get statistics about JSON structure."""
    def count_items(obj):
        if isinstance(obj, dict):
            return sum(count_items(v) for v in obj.values()) + len(obj)
        elif isinstance(obj, list):
            return sum(count_items(item) for item in obj) + len(obj)
        return 1
    
    def get_depth(obj, level=0):
        if isinstance(obj, dict):
            return max((get_depth(v, level + 1) for v in obj.values()), default=level)
        elif isinstance(obj, list):
            return max((get_depth(item, level + 1) for item in obj), default=level)
        return level
    
    return {
        'items': count_items(data),
        'depth': get_depth(data),
        'type': type(data).__name__
    }

def main():
    parser = argparse.ArgumentParser(
        description='JSON formatter and validator',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s file.json
  %(prog)s -c file.json                    # compact
  %(prog)s -s file.json                    # sort keys
  %(prog)s -i 4 file.json                  # indent 4 spaces
  echo '{"a":1}' | %(prog)s                # from stdin
  cat ugly.json | %(prog)s > pretty.json   # reformat
        """
    )
    parser.add_argument('file', nargs='?', help='JSON file (or use stdin)')
    parser.add_argument('-c', '--compact', action='store_true', help='Compact output (no whitespace)')
    parser.add_argument('-s', '--sort', action='store_true', help='Sort keys alphabetically')
    parser.add_argument('-i', '--indent', type=int, default=2, help='Indentation spaces (default: 2)')
    parser.add_argument('--stats', action='store_true', help='Show statistics only')
    parser.add_argument('--validate', action='store_true', help='Validate only, no output')
    
    args = parser.parse_args()
    
    # Read input
    try:
        if args.file:
            with open(args.file, 'r', encoding='utf-8') as f:
                text = f.read()
        elif not sys.stdin.isatty():
            text = sys.stdin.read()
        else:
            parser.print_help()
            sys.exit(1)
    except FileNotFoundError:
        print(f"Error: File not found: {args.file}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error reading file: {e}", file=sys.stderr)
        sys.exit(1)
    
    # Validate
    try:
        data = validate_json(text)
    except json.JSONDecodeError as e:
        print(f"Invalid JSON: {e}", file=sys.stderr)
        sys.exit(1)
    
    if args.validate:
        print("Valid JSON ✓")
        sys.exit(0)
    
    if args.stats:
        stats = get_stats(data)
        print(f"Type:   {stats['type']}")
        print(f"Items:  {stats['items']}")
        print(f"Depth:  {stats['depth']}")
        print(f"Size:   {len(text)} bytes")
        sys.exit(0)
    
    # Output formatted JSON
    formatted = format_json(data, args.indent, args.sort, args.compact)
    print(formatted)

if __name__ == '__main__':
    main()
