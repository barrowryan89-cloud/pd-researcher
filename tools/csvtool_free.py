#!/usr/bin/env python3
"""
csvtool — CSV to JSON converter and processor
Tool #68 — Free CLI Tool for PD Researcher
"""

import argparse
import csv
import json
import sys
from pathlib import Path


def csv_to_json(filepath, headers=None):
    """Convert CSV file to JSON."""
    try:
        with open(filepath, 'r', newline='', encoding='utf-8') as f:
            if headers:
                reader = csv.DictReader(f, fieldnames=headers)
            else:
                reader = csv.DictReader(f)
            rows = list(reader)
        return rows, None
    except FileNotFoundError:
        return None, f"File not found: {filepath}"
    except Exception as e:
        return None, str(e)


def json_to_csv(data, output_path=None):
    """Convert JSON array to CSV."""
    if not data:
        return "Error: Empty data"
    
    if not isinstance(data, list):
        return "Error: JSON must be an array of objects"
    
    # Get headers from first row
    headers = list(data[0].keys())
    
    output = []
    writer = csv.writer(output)
    writer.writerow(headers)
    
    for row in data:
        writer.writerow([row.get(h, '') for h in headers])
    
    result = '\n'.join(output)
    
    if output_path:
        with open(output_path, 'w', newline='', encoding='utf-8') as f:
            f.write(result)
        return f"Saved to: {output_path}"
    
    return result


def preview_csv(filepath, rows=5):
    """Preview first N rows of CSV."""
    data, error = csv_to_json(filepath)
    if error:
        return error
    
    return data[:rows]


def main():
    parser = argparse.ArgumentParser(
        description='CSV processor and converter',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  csvtool data.csv                          # Convert CSV to JSON
  csvtool data.csv -o out.json              # Save to file
  csvtool data.csv -p 10                    # Preview 10 rows
  csvtool data.csv --headers name,email     # Custom headers
  cat data.csv | csvtool -                  # Read from stdin
        """
    )
    
    parser.add_argument('input', help='CSV file path or - for stdin')
    parser.add_argument('-o', '--output',
                       help='Output file (default: stdout)')
    parser.add_argument('-p', '--preview', type=int, nargs='?', const=5, metavar='N',
                       help='Preview first N rows (default: 5)')
    parser.add_argument('--headers',
                       help='Comma-separated custom headers')
    parser.add_argument('-f', '--format', choices=['json', 'csv'], default='json',
                       help='Output format (default: json)')
    parser.add_argument('--pretty', action='store_true',
                       help='Pretty print JSON output')
    parser.add_argument('--minify', action='store_true',
                       help='Minify JSON output')
    
    args = parser.parse_args()
    
    # Parse custom headers
    headers = args.headers.split(',') if args.headers else None
    
    # Read input
    if args.input == '-':
        # Read from stdin
        import tempfile
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.csv') as f:
            f.write(sys.stdin.read())
            temp_path = f.name
        data, error = csv_to_json(temp_path, headers)
        Path(temp_path).unlink()
    else:
        data, error = csv_to_json(args.input, headers)
    
    if error:
        print(f"Error: {error}", file=sys.stderr)
        sys.exit(1)
    
    # Preview mode
    if args.preview:
        print(f"Preview (first {min(args.preview, len(data))} of {len(data)} rows):\n")
        for i, row in enumerate(data[:args.preview], 1):
            print(f"Row {i}:")
            for key, value in row.items():
                print(f"  {key}: {value}")
            print()
        return
    
    # Output
    if args.format == 'json':
        if args.minify:
            output = json.dumps(data, separators=(',', ':'))
        elif args.pretty:
            output = json.dumps(data, indent=2)
        else:
            output = json.dumps(data)
    else:
        # CSV output
        output = json_to_csv(data)
    
    if args.output:
        with open(args.output, 'w') as f:
            f.write(output)
        print(f"Saved to: {args.output}")
    else:
        print(output)


if __name__ == '__main__':
    main()

    # Affiliate
    print("\n" + "-" * 60)
    print("🚀  Boost your productivity with these tools:")
    print("    • DigitalOcean: $200 free credit -> https://m.do.co/c/pdresearcher")
    print("    • JetBrains IDEs: The best Python tools -> https://www.jetbrains.com/?utm_source=pdresearcher")
    print("-" * 60)
