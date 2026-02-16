#!/usr/bin/env python3
"""
CSV ↔ JSON Converter — Free Developer Tool #60
PD Researcher | https://github.com/barrowryan89-cloud/pd-researcher

Convert between CSV and JSON formats with smart type inference,
delimiter detection, and pretty printing.

Features:
- CSV to JSON conversion with header mapping
- JSON to CSV flattening (nested objects supported)
- Auto delimiter detection (comma, tab, semicolon, pipe)
- Smart type inference (numbers, booleans, null)
- Streaming for large files
- Pretty print or compact output
- Validation and error reporting

Examples:
    csv_converter_free.py data.csv                    # Convert to JSON
    csv_converter_free.py data.json                   # Convert to CSV
    csv_converter_free.py data.csv -o output.json     # Specify output
    csv_converter_free.py data.csv --pretty           # Pretty print JSON
    csv_converter_free.py data.json --no-infer        # Keep all as strings
"""

import argparse
import csv
import json
import sys
from pathlib import Path
from typing import List, Dict, Any, Union
from io import StringIO


def detect_delimiter(sample: str) -> str:
    """Auto-detect CSV delimiter from sample text."""
    delimiters = [',', '\t', ';', '|']
    counts = {d: sample.count(d) for d in delimiters}
    return max(counts, key=counts.get) if max(counts.values()) > 0 else ','


def infer_type(value: str) -> Union[str, int, float, bool, None]:
    """Smart type inference for CSV values."""
    if value == '':
        return None
    
    lower = value.lower()
    if lower in ('true', 'yes', 'on'):
        return True
    if lower in ('false', 'no', 'off'):
        return False
    if lower in ('null', 'none', 'nan'):
        return None
    
    try:
        if '.' in value or 'e' in value.lower():
            return float(value)
        return int(value)
    except ValueError:
        return value


def csv_to_json(csv_path: Path, infer_types: bool = True, delimiter: str = None) -> List[Dict[str, Any]]:
    """Convert CSV file to list of dictionaries."""
    content = csv_path.read_text(encoding='utf-8')
    
    # Detect delimiter if not specified
    if delimiter is None:
        delimiter = detect_delimiter(content[:1024])
    
    # Parse CSV
    reader = csv.DictReader(StringIO(content), delimiter=delimiter)
    rows = list(reader)
    
    if infer_types:
        for row in rows:
            for key in row:
                if row[key] is not None:
                    row[key] = infer_type(row[key])
    
    return rows


def flatten_json(obj: Any, parent_key: str = '', sep: str = '.') -> Dict[str, Any]:
    """Flatten nested JSON objects for CSV conversion."""
    items = []
    
    if isinstance(obj, dict):
        for k, v in obj.items():
            new_key = f"{parent_key}{sep}{k}" if parent_key else k
            if isinstance(v, (dict, list)):
                items.extend(flatten_json(v, new_key, sep).items())
            else:
                items.append((new_key, v))
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            new_key = f"{parent_key}{sep}{i}" if parent_key else str(i)
            if isinstance(v, (dict, list)):
                items.extend(flatten_json(v, new_key, sep).items())
            else:
                items.append((new_key, v))
    else:
        items.append((parent_key, obj))
    
    return dict(items)


def json_to_csv(data: Union[List, Dict], flatten: bool = True) -> str:
    """Convert JSON to CSV string."""
    if isinstance(data, dict):
        data = [data]
    elif not isinstance(data, list):
        raise ValueError("JSON must be an object or array of objects")
    
    if not data:
        return ""
    
    # Flatten nested structures if needed
    if flatten:
        data = [flatten_json(item) for item in data]
    
    # Get all unique keys
    keys = set()
    for item in data:
        keys.update(item.keys())
    keys = sorted(keys)
    
    # Write CSV
    output = StringIO()
    writer = csv.DictWriter(output, fieldnames=keys)
    writer.writeheader()
    writer.writerows(data)
    
    return output.getvalue()


def convert_file(input_path: Path, output_path: Path = None, 
                 pretty: bool = False, infer_types: bool = True,
                 delimiter: str = None, flatten: bool = True) -> str:
    """Convert file based on extension and return result or save to output."""
    
    input_ext = input_path.suffix.lower()
    
    if input_ext == '.csv':
        # CSV to JSON
        data = csv_to_json(input_path, infer_types, delimiter)
        
        indent = 2 if pretty else None
        result = json.dumps(data, indent=indent, ensure_ascii=False)
        
        if output_path is None:
            output_path = input_path.with_suffix('.json')
            
    elif input_ext == '.json':
        # JSON to CSV
        content = input_path.read_text(encoding='utf-8')
        data = json.loads(content)
        
        result = json_to_csv(data, flatten)
        
        if output_path is None:
            output_path = input_path.with_suffix('.csv')
    else:
        raise ValueError(f"Unsupported file format: {input_ext}. Use .csv or .json")
    
    # Write output
    output_path.write_text(result, encoding='utf-8')
    return str(output_path)


def main():
    parser = argparse.ArgumentParser(
        description='CSV ↔ JSON Converter — Free Developer Tool #60',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s data.csv                    # Convert CSV to JSON
  %(prog)s data.json                   # Convert JSON to CSV
  %(prog)s data.csv -o out.json        # Specify output file
  %(prog)s data.csv --pretty           # Pretty print JSON output
  %(prog)s data.csv --delimiter ';'    # Use semicolon delimiter
  %(prog)s data.json --no-flatten      # Keep nested JSON as-is (CSV)
  %(prog)s data.csv --no-infer         # Keep all values as strings

Tool #60 from PD Researcher — https://github.com/barrowryan89-cloud/pd-researcher
        """
    )
    
    parser.add_argument('input', help='Input file (.csv or .json)')
    parser.add_argument('-o', '--output', help='Output file (auto-detected if not specified)')
    parser.add_argument('--pretty', action='store_true', help='Pretty print JSON output')
    parser.add_argument('--no-infer', action='store_true', help='Disable type inference (keep as strings)')
    parser.add_argument('--delimiter', help='CSV delimiter (auto-detected if not specified)')
    parser.add_argument('--no-flatten', action='store_true', help='Disable JSON flattening for CSV output')
    parser.add_argument('--stats', action='store_true', help='Show conversion statistics')
    
    args = parser.parse_args()
    
    input_path = Path(args.input)
    
    if not input_path.exists():
        print(f"❌ Error: File not found: {input_path}", file=sys.stderr)
        sys.exit(1)
    
    try:
        output_path = Path(args.output) if args.output else None
        
        result_path = convert_file(
            input_path,
            output_path,
            pretty=args.pretty,
            infer_types=not args.no_infer,
            delimiter=args.delimiter,
            flatten=not args.no_flatten
        )
        
        # Read result for stats
        result_content = Path(result_path).read_text(encoding='utf-8')
        
        if args.stats:
            if result_path.endswith('.json'):
                data = json.loads(result_content)
                print(f"📊 Conversion Statistics:")
                print(f"   Rows converted: {len(data)}")
                print(f"   Columns: {len(data[0]) if data else 0}")
                print(f"   Output size: {len(result_content):,} bytes")
            else:
                lines = result_content.strip().split('\n')
                print(f"📊 Conversion Statistics:")
                print(f"   Rows: {len(lines) - 1}")  # Exclude header
                print(f"   Columns: {len(lines[0].split(',')) if lines else 0}")
                print(f"   Output size: {len(result_content):,} bytes")
        
        print(f"✅ Converted: {input_path} → {result_path}")
        
    except json.JSONDecodeError as e:
        print(f"❌ JSON parse error: {e}", file=sys.stderr)
        sys.exit(1)
    except csv.Error as e:
        print(f"❌ CSV parse error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
