#!/usr/bin/env python3
"""
CSV Processor - Free Tool
Basic CSV operations: view, filter, convert
Free version: Single file operations
Paid upgrade: Batch processing, SQL export, data analysis

Usage: python3 csv_processor_free.py <file.csv> [command] [args]
"""

import sys
import csv
import json

def read_csv(filepath):
    """Read CSV and return as list of dicts"""
    data = []
    with open(filepath, 'r', newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            data.append(row)
    return data

def preview_csv(data, rows=10):
    """Show first N rows"""
    if not data:
        print("No data")
        return
    
    headers = list(data[0].keys())
    print(f"\nColumns: {', '.join(headers)}")
    print(f"Total rows: {len(data)}\n")
    
    print(f"First {min(rows, len(data))} rows:")
    print("-" * 80)
    for i, row in enumerate(data[:rows]):
        print(f"\nRow {i+1}:")
        for key, value in row.items():
            print(f"  {key}: {value[:50]}{'...' if len(str(value)) > 50 else ''}")

def convert_to_json(data, output_path):
    """Convert CSV to JSON"""
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)
    print(f"✅ Converted to JSON: {output_path}")

def filter_rows(data, column, value):
    """Filter rows where column contains value"""
    filtered = [row for row in data if value.lower() in str(row.get(column, '')).lower()]
    return filtered

def print_banner():
    print("""
╔════════════════════════════════════════════════════════════╗
║                   CSV PROCESSOR v1.0                       ║
║              Free Tool by Sand Street Holdings             ║
╠════════════════════════════════════════════════════════════╣
║  Process CSV files: view, filter, convert to JSON          ║
║                                                            ║
║  💎 Want more power?                                       ║
║     → SQL export scripts                                   ║
║     → Data analysis (stats, aggregation)                   ║
║     → Batch file processing                                ║
║     → Column manipulation (merge, split)                   ║
║     → Check out PD_Researcher v1 ($29)                     ║
║        Solana: FEKY6bDoqBnsQZVT3XbEYS4b1DJ8QoA64G5hXycfTAhQ ║
╚════════════════════════════════════════════════════════════╝
""")

def main():
    print_banner()
    
    if len(sys.argv) < 2:
        print("❌ No CSV file provided.")
        print("\nUsage:")
        print("  python3 csv_processor_free.py data.csv")
        print("  python3 csv_processor_free.py data.csv preview 5")
        print("  python3 csv_processor_free.py data.csv json output.json")
        print("  python3 csv_processor_free.py data.csv filter column_name search_term")
        sys.exit(1)
    
    filepath = sys.argv[1]
    command = sys.argv[2] if len(sys.argv) > 2 else 'preview'
    
    try:
        data = read_csv(filepath)
    except Exception as e:
        print(f"❌ Error reading CSV: {e}")
        sys.exit(1)
    
    if command == 'preview':
        rows = int(sys.argv[3]) if len(sys.argv) > 3 else 10
        preview_csv(data, rows)
    
    elif command == 'json':
        output = sys.argv[3] if len(sys.argv) > 3 else 'output.json'
        convert_to_json(data, output)
    
    elif command == 'filter':
        if len(sys.argv) < 5:
            print("❌ Missing filter arguments")
            print("Usage: csv_processor_free.py file.csv filter column_name search_term")
            sys.exit(1)
        column = sys.argv[3]
        term = sys.argv[4]
        filtered = filter_rows(data, column, term)
        print(f"\nFound {len(filtered)} matching rows:")
        preview_csv(filtered, rows=min(10, len(filtered)))
    
    else:
        print(f"❌ Unknown command: {command}")
        print("Commands: preview, json, filter")
        sys.exit(1)
    
    print("\n" + "="*60)
    print("\n💡 Want SQL export and data analysis?")
    print("   Upgrade to PD_Researcher v1 for advanced CSV tools")
    print("   Pay with crypto: FEKY6bDoqBnsQZVT3XbEYS4b1DJ8QoA64G5hXycfTAhQ")
    print("="*60)

if __name__ == "__main__":
    main()
