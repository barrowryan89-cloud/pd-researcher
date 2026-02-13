#!/usr/bin/env python3
"""
csv_formatter - Format, validate, and transform CSV files
Tool #44 - Free CLI utility for data workers
"""
import sys
import csv
import json
import argparse
from io import StringIO
from collections import Counter

def detect_dialect(sample):
    """Auto-detect CSV dialect."""
    try:
        sniffer = csv.Sniffer()
        dialect = sniffer.sniff(sample)
        return dialect
    except:
        return csv.excel

def format_csv(input_data, output_delimiter=',', output_quote='minimal', align=False):
    """Format CSV with consistent styling."""
    lines = input_data.strip().split('\n')
    if not lines:
        return ""
    
    # Detect input dialect
    sample = '\n'.join(lines[:5])
    dialect = detect_dialect(sample)
    
    # Parse input
    reader = csv.reader(StringIO(input_data), dialect=dialect)
    rows = list(reader)
    
    if not rows:
        return ""
    
    # Determine output formatting
    if output_quote == 'all':
        quoting = csv.QUOTE_ALL
    elif output_quote == 'none':
        quoting = csv.QUOTE_NONE
    else:
        quoting = csv.QUOTE_MINIMAL
    
    # Calculate column widths if aligning
    if align:
        col_widths = []
        for row in rows:
            for i, cell in enumerate(row):
                if i >= len(col_widths):
                    col_widths.append(0)
                col_widths[i] = max(col_widths[i], len(str(cell)))
    
    # Generate output
    output = StringIO()
    writer = csv.writer(output, delimiter=output_delimiter, quoting=quoting, lineterminator='\n')
    
    for row in rows:
        if align:
            # Pad cells for alignment
            padded = []
            for i, cell in enumerate(row):
                if i < len(col_widths):
                    padded.append(str(cell).ljust(col_widths[i]))
                else:
                    padded.append(str(cell))
            writer.writerow(padded)
        else:
            writer.writerow(row)
    
    return output.getvalue()

def validate_csv(input_data):
    """Validate CSV structure and report issues."""
    lines = input_data.strip().split('\n')
    if not lines:
        return {"valid": False, "error": "Empty input"}
    
    sample = '\n'.join(lines[:5])
    dialect = detect_dialect(sample)
    
    try:
        reader = csv.reader(StringIO(input_data), dialect=dialect)
        rows = list(reader)
        
        if not rows:
            return {"valid": False, "error": "No data rows found"}
        
        col_count = len(rows[0])
        issues = []
        
        for i, row in enumerate(rows):
            if len(row) != col_count:
                issues.append(f"Row {i+1}: {len(row)} columns (expected {col_count})")
        
        # Check for empty cells
        empty_cells = sum(1 for row in rows for cell in row if not cell.strip())
        
        return {
            "valid": len(issues) == 0,
            "rows": len(rows),
            "columns": col_count,
            "issues": issues,
            "empty_cells": empty_cells,
            "dialect": {
                "delimiter": dialect.delimiter,
                "quotechar": dialect.quotechar
            }
        }
    except Exception as e:
        return {"valid": False, "error": str(e)}

def csv_to_json(input_data):
    """Convert CSV to JSON."""
    sample = '\n'.join(input_data.strip().split('\n')[:5])
    dialect = detect_dialect(sample)
    
    reader = csv.DictReader(StringIO(input_data), dialect=dialect)
    return json.dumps(list(reader), indent=2)

def transpose_csv(input_data):
    """Transpose rows to columns."""
    sample = '\n'.join(input_data.strip().split('\n')[:5])
    dialect = detect_dialect(sample)
    
    reader = csv.reader(StringIO(input_data), dialect=dialect)
    rows = list(reader)
    
    if not rows:
        return ""
    
    max_cols = max(len(row) for row in rows)
    
    # Transpose
    transposed = []
    for col_idx in range(max_cols):
        new_row = []
        for row in rows:
            if col_idx < len(row):
                new_row.append(row[col_idx])
            else:
                new_row.append("")
        transposed.append(new_row)
    
    output = StringIO()
    writer = csv.writer(output, lineterminator='\n')
    writer.writerows(transposed)
    return output.getvalue()

def stats_csv(input_data):
    """Generate statistics about CSV data."""
    sample = '\n'.join(input_data.strip().split('\n')[:5])
    dialect = detect_dialect(sample)
    
    reader = csv.reader(StringIO(input_data), dialect=dialect)
    rows = list(reader)
    
    if not rows:
        return {}
    
    stats = {
        "total_rows": len(rows),
        "total_columns": len(rows[0]),
        "column_stats": []
    }
    
    for col_idx in range(len(rows[0])):
        values = [row[col_idx] if col_idx < len(row) else "" for row in rows[1:]]
        non_empty = [v for v in values if v.strip()]
        
        # Try numeric analysis
        numeric = []
        for v in non_empty:
            try:
                numeric.append(float(v.replace(',', '')))
            except:
                pass
        
        col_stat = {
            "column": rows[0][col_idx] if rows[0] else f"Col {col_idx+1}",
            "non_empty": len(non_empty),
            "empty": len(values) - len(non_empty),
            "unique": len(set(non_empty)),
            "numeric_count": len(numeric)
        }
        
        if numeric:
            col_stat["min"] = min(numeric)
            col_stat["max"] = max(numeric)
            col_stat["avg"] = round(sum(numeric) / len(numeric), 2)
        
        stats["column_stats"].append(col_stat)
    
    return stats

def main():
    parser = argparse.ArgumentParser(description='Format, validate, and transform CSV files')
    parser.add_argument('file', nargs='?', help='Input file (default: stdin)')
    parser.add_argument('-d', '--delimiter', default=',', help='Output delimiter')
    parser.add_argument('-q', '--quote', choices=['minimal', 'all', 'none'], default='minimal',
                        help='Quote style')
    parser.add_argument('-a', '--align', action='store_true', help='Align columns')
    parser.add_argument('-v', '--validate', action='store_true', help='Validate structure')
    parser.add_argument('-j', '--json', action='store_true', help='Convert to JSON')
    parser.add_argument('-t', '--transpose', action='store_true', help='Transpose rows/columns')
    parser.add_argument('-s', '--stats', action='store_true', help='Show statistics')
    parser.add_argument('--tsv', action='store_true', help='Output as TSV')
    
    args = parser.parse_args()
    
    # Read input
    if args.file and args.file != '-':
        with open(args.file, 'r') as f:
            input_data = f.read()
    else:
        input_data = sys.stdin.read()
    
    if not input_data.strip():
        print("❌ No input data provided")
        sys.exit(1)
    
    # Handle TSV output shorthand
    if args.tsv:
        args.delimiter = '\t'
    
    # Execute requested operation
    if args.validate:
        result = validate_csv(input_data)
        print("📋 CSV Validation Report")
        print("=" * 40)
        print(f"Status: {'✅ Valid' if result['valid'] else '❌ Invalid'}")
        print(f"Rows: {result.get('rows', 'N/A')}")
        print(f"Columns: {result.get('columns', 'N/A')}")
        print(f"Empty cells: {result.get('empty_cells', 'N/A')}")
        if 'dialect' in result:
            print(f"Delimiter detected: '{result['dialect']['delimiter']}'")
        if result.get('issues'):
            print("\n⚠️ Issues found:")
            for issue in result['issues']:
                print(f"  - {issue}")
    
    elif args.json:
        print(csv_to_json(input_data))
    
    elif args.transpose:
        print(transpose_csv(input_data), end='')
    
    elif args.stats:
        stats = stats_csv(input_data)
        print("📊 CSV Statistics")
        print("=" * 40)
        print(f"Total rows: {stats['total_rows']}")
        print(f"Total columns: {stats['total_columns']}")
        print("\nColumn breakdown:")
        for col in stats['column_stats']:
            print(f"\n  {col['column']}:")
            print(f"    Non-empty: {col['non_empty']}, Empty: {col['empty']}, Unique: {col['unique']}")
            if 'min' in col:
                print(f"    Numeric: min={col['min']}, max={col['max']}, avg={col['avg']}")
    
    else:
        # Default: format
        output = format_csv(input_data, args.delimiter, args.quote, args.align)
        print(output, end='')

if __name__ == "__main__":
    main()
