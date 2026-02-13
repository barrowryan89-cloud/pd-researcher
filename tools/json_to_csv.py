#!/usr/bin/env python3
"""
JSON to CSV Converter — Tool #34
Convert JSON files to CSV format with nested object flattening.
Part of the PD_Researcher free tool suite.
"""

import argparse
import csv
import json
import sys
from pathlib import Path


def flatten_dict(d, parent_key='', sep='.'):
    """Flatten nested dictionaries for CSV compatibility."""
    items = []
    for k, v in d.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        if isinstance(v, dict):
            items.extend(flatten_dict(v, new_key, sep=sep).items())
        elif isinstance(v, list):
            # Store lists as JSON string
            items.append((new_key, json.dumps(v)))
        else:
            items.append((new_key, v))
    return dict(items)


def json_to_csv(input_file, output_file=None, delimiter=',', flatten=True, array_handling='first'):
    """Convert JSON to CSV."""
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Handle both single object and array of objects
    if isinstance(data, dict):
        data = [data]
    elif not isinstance(data, list):
        print("Error: JSON must be an object or array of objects", file=sys.stderr)
        sys.exit(1)
    
    if not data:
        print("Error: Empty JSON array", file=sys.stderr)
        sys.exit(1)
    
    # Flatten if requested
    if flatten:
        data = [flatten_dict(item) for item in data]
    
    # Get all unique headers
    headers = set()
    for item in data:
        headers.update(item.keys())
    headers = sorted(headers)
    
    # Determine output file
    if not output_file:
        output_file = str(Path(input_file).with_suffix('.csv'))
    
    # Write CSV
    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=headers, delimiter=delimiter)
        writer.writeheader()
        writer.writerows(data)
    
    return output_file


def main():
    parser = argparse.ArgumentParser(
        description='Convert JSON files to CSV format',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s data.json                    # Convert to data.csv
  %(prog)s data.json -o output.csv      # Specify output
  %(prog)s data.json -d ';'             # Use semicolon delimiter
  %(prog)s data.json --no-flatten       # Keep nested structure as JSON strings
        """
    )
    parser.add_argument('input', help='Input JSON file')
    parser.add_argument('-o', '--output', help='Output CSV file (default: input.csv)')
    parser.add_argument('-d', '--delimiter', default=',', help='CSV delimiter (default: comma)')
    parser.add_argument('--no-flatten', action='store_true', help='Do not flatten nested objects')
    parser.add_argument('--preview', type=int, metavar='N', help='Preview first N rows only')
    
    args = parser.parse_args()
    
    if not Path(args.input).exists():
        print(f"Error: File not found: {args.input}", file=sys.stderr)
        sys.exit(1)
    
    try:
        output = json_to_csv(
            args.input,
            args.output,
            args.delimiter,
            flatten=not args.no_flatten
        )
        print(f"✓ Converted: {args.input} → {output}")
        
        # Show preview
        with open(output, 'r') as f:
            reader = csv.reader(f)
            headers = next(reader)
            print(f"\nColumns ({len(headers)}): {', '.join(headers[:5])}" + ("..." if len(headers) > 5 else ""))
            
            if args.preview:
                rows = []
                for i, row in enumerate(reader):
                    if i >= args.preview:
                        break
                    rows.append(row)
                print(f"\nPreview (first {len(rows)} rows):")
                for row in rows:
                    preview = ', '.join(cell[:30] + '...' if len(cell) > 30 else cell for cell in row[:3])
                    print(f"  {preview}" + ("..." if len(row) > 3 else ""))
                    
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON - {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
