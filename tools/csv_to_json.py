#!/usr/bin/env python3
"""
CSV to JSON Converter — Free Tool #33
Convert CSV files to JSON with automatic type detection and schema inference.
Part of the PD_Researcher free tools collection.
https://github.com/barrowryan89-cloud/pd-researcher
"""

import argparse
import csv
import json
import re
import sys
from datetime import datetime
from pathlib import Path


def detect_type(value):
    """Detect the most appropriate data type for a value."""
    if value is None or value == "":
        return None, "null"
    
    value_str = str(value).strip()
    
    # Try boolean
    if value_str.lower() in ('true', 'yes', '1'):
        return True, "boolean"
    if value_str.lower() in ('false', 'no', '0'):
        return False, "boolean"
    
    # Try integer
    try:
        int_val = int(value_str)
        if str(int_val) == value_str:  # No leading zeros issue
            return int_val, "integer"
    except ValueError:
        pass
    
    # Try float
    try:
        float_val = float(value_str)
        return float_val, "number"
    except ValueError:
        pass
    
    # Try date/datetime
    date_patterns = [
        (r'^\d{4}-\d{2}-\d{2}$', '%Y-%m-%d', 'date'),
        (r'^\d{2}/\d{2}/\d{4}$', '%m/%d/%Y', 'date'),
        (r'^\d{4}-\d{2}-\d{2}[T ]\d{2}:\d{2}:\d{2}', '%Y-%m-%dT%H:%M:%S', 'datetime'),
        (r'^\d{4}-\d{2}-\d{2}[T ]\d{2}:\d{2}$', '%Y-%m-%dT%H:%M', 'datetime'),
    ]
    
    for pattern, fmt, dtype in date_patterns:
        if re.match(pattern, value_str):
            try:
                dt = datetime.strptime(value_str[:len(fmt)], fmt)
                return value_str, dtype
            except ValueError:
                pass
    
    # Default to string
    return value_str, "string"


def infer_schema(rows, headers):
    """Infer JSON schema from data rows."""
    schema = {
        "type": "object",
        "properties": {}
    }
    
    if not rows:
        return schema
    
    for header in headers:
        types_found = set()
        sample_values = []
        
        for row in rows[:100]:  # Sample first 100 rows
            if header in row:
                _, dtype = detect_type(row[header])
                types_found.add(dtype)
                if len(sample_values) < 3 and row[header]:
                    sample_values.append(row[header])
        
        # Determine final type
        if len(types_found) == 1:
            final_type = types_found.pop()
        elif 'null' in types_found and len(types_found) == 2:
            types_found.discard('null')
            final_type = types_found.pop()
        elif 'integer' in types_found and 'number' in types_found:
            final_type = 'number'
        else:
            final_type = 'string'
        
        schema["properties"][header] = {
            "type": final_type,
            "examples": sample_values[:3]
        }
    
    return schema


def convert_csv_to_json(input_file, detect_types=True, minify=False, output_file=None):
    """Convert CSV to JSON with optional type detection."""
    try:
        with open(input_file, 'r', encoding='utf-8-sig') as f:
            # Try to detect dialect
            sample = f.read(8192)
            f.seek(0)
            
            try:
                dialect = csv.Sniffer().sniff(sample, delimiters=',;\t|')
            except:
                dialect = None
            
            reader = csv.DictReader(f, dialect=dialect)
            headers = reader.fieldnames
            
            if not headers:
                return {"error": "No headers found in CSV file"}
            
            rows = []
            for row in reader:
                if detect_types:
                    converted_row = {}
                    for key, value in row.items():
                        converted_val, _ = detect_type(value)
                        converted_row[key] = converted_val
                    rows.append(converted_row)
                else:
                    rows.append(row)
            
            result = {
                "success": True,
                "count": len(rows),
                "headers": headers,
                "data": rows
            }
            
            if detect_types:
                result["schema"] = infer_schema(rows, headers)
            
            return result
            
    except FileNotFoundError:
        return {"error": f"File not found: {input_file}"}
    except Exception as e:
        return {"error": f"Conversion failed: {str(e)}"}


def print_summary(result, verbose=False):
    """Print conversion summary."""
    if "error" in result:
        print(f"\n❌ Error: {result['error']}")
        return
    
    print(f"\n{'='*60}")
    print(f"✓ Conversion Complete")
    print(f"{'='*60}")
    print(f"\n📊 Statistics:")
    print(f"  Rows converted: {result['count']:,}")
    print(f"  Columns: {len(result['headers'])}")
    
    if verbose and 'schema' in result:
        print(f"\n🔍 Detected Schema:")
        for field, info in result['schema']['properties'].items():
            examples = ', '.join(str(e) for e in info['examples'][:2])
            print(f"  {field}: {info['type']} (e.g., {examples})")
    
    print(f"\n📋 Columns: {', '.join(result['headers'])}")
    print(f"{'='*60}\n")


def main():
    parser = argparse.ArgumentParser(
        description="CSV to JSON Converter — Automatic type detection & schema inference",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Basic conversion
  python csv_to_json.py data.csv
  
  # Save to file (pretty printed)
  python csv_to_json.py data.csv -o output.json
  
  # Minified JSON (smaller file size)
  python csv_to_json.py data.csv -o output.json --minify
  
  # No type detection (all strings)
  python csv_to_json.py data.csv --no-types
  
  # Verbose output with schema
  python csv_to_json.py data.csv -v
  
  # Preview first 5 rows only
  python csv_to_json.py data.csv --preview 5
        """
    )
    
    parser.add_argument("input", help="Input CSV file path")
    parser.add_argument("-o", "--output", metavar="FILE",
                       help="Output JSON file (default: print to stdout)")
    parser.add_argument("--no-types", action="store_true",
                       help="Skip type detection (all values as strings)")
    parser.add_argument("--minify", action="store_true",
                       help="Output minified JSON (no indentation)")
    parser.add_argument("-v", "--verbose", action="store_true",
                       help="Verbose output with schema")
    parser.add_argument("--preview", type=int, metavar="N",
                       help="Only convert first N rows (preview mode)")
    
    args = parser.parse_args()
    
    # Check input file
    input_path = Path(args.input)
    if not input_path.exists():
        print(f"❌ Error: File not found: {args.input}")
        sys.exit(1)
    
    # Convert
    result = convert_csv_to_json(
        args.input,
        detect_types=not args.no_types,
        minify=args.minify,
        output_file=args.output
    )
    
    if "error" in result:
        print(f"\n❌ {result['error']}")
        sys.exit(1)
    
    # Handle preview mode
    data = result['data']
    if args.preview:
        data = data[:args.preview]
        result['count'] = len(data)
    
    # Output JSON
    indent = None if args.minify else 2
    json_output = json.dumps(data, indent=indent, ensure_ascii=False)
    
    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(json_output)
        print(f"✓ Saved to: {args.output}")
    else:
        print(json_output)
    
    # Print summary if verbose or output to file
    if args.verbose or args.output:
        # Adjust result for preview
        if args.preview:
            result['data'] = data
        print_summary(result, args.verbose)


if __name__ == "__main__":
    main()
