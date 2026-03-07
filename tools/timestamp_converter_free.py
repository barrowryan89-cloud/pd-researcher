#!/usr/bin/env python3
"""
Timestamp Converter - Free Tool
Convert between Unix timestamps and human-readable dates
Free version: Single conversion
Paid upgrade: Batch processing, timezone handling, formatting options

Usage: python3 timestamp_converter_free.py <timestamp or date>
"""

import sys
import time
from datetime import datetime, timezone

def parse_input(user_input):
    """Try to parse input as timestamp or date string"""
    user_input = user_input.strip()
    
    # Try Unix timestamp (numeric)
    try:
        timestamp = float(user_input)
        # Determine if seconds or milliseconds
        if timestamp > 1e12:  # Likely milliseconds
            timestamp = timestamp / 1000
        return ('timestamp', timestamp)
    except ValueError:
        pass
    
    # Try ISO format
    try:
        dt = datetime.fromisoformat(user_input.replace('Z', '+00:00'))
        return ('iso', dt)
    except ValueError:
        pass
    
    # Try common date formats
    formats = [
        '%Y-%m-%d %H:%M:%S',
        '%Y-%m-%d',
        '%m/%d/%Y %H:%M:%S',
        '%m/%d/%Y',
        '%d/%m/%Y %H:%M:%S',
        '%d/%m/%Y',
    ]
    
    for fmt in formats:
        try:
            dt = datetime.strptime(user_input, fmt)
            return ('date', dt)
        except ValueError:
            continue
    
    return (None, None)

def convert_timestamp(ts):
    """Convert Unix timestamp to various formats"""
    dt_utc = datetime.fromtimestamp(ts, tz=timezone.utc)
    dt_local = datetime.fromtimestamp(ts)
    
    return {
        'unix_seconds': int(ts),
        'unix_millis': int(ts * 1000),
        'iso_utc': dt_utc.isoformat(),
        'iso_local': dt_local.isoformat(),
        'readable_utc': dt_utc.strftime('%Y-%m-%d %H:%M:%S UTC'),
        'readable_local': dt_local.strftime('%Y-%m-%d %H:%M:%S'),
        'date_only': dt_utc.strftime('%Y-%m-%d'),
        'time_only': dt_utc.strftime('%H:%M:%S'),
    }

def convert_datetime(dt):
    """Convert datetime to timestamp"""
    # Assume local time if no timezone
    if dt.tzinfo is None:
        timestamp = dt.timestamp()
    else:
        timestamp = dt.timestamp()
    
    return convert_timestamp(timestamp)

def print_banner():
    print("""
╔════════════════════════════════════════════════════════════╗
║               TIMESTAMP CONVERTER v1.0                     ║
║              Free Tool by Sand Street Holdings             ║
╠════════════════════════════════════════════════════════════╣
║  Convert between Unix timestamps and human-readable dates  ║
║                                                            ║
║  💎 Want more power?                                       ║
║     → Timezone conversion                                  ║
║     → Batch file processing                                ║
║     → Custom output formats                                ║
║     → Date arithmetic (add/subtract time)                  ║
║     → Check out PD_Researcher v1 ($29)                     ║
║        Solana: FEKY6bDoqBnsQZVT3XbEYS4b1DJ8QoA64G5hXycfTAhQ ║
╚════════════════════════════════════════════════════════════╝
""")

def main():
    print_banner()
    
    if len(sys.argv) < 2:
        print("❌ No input provided.")
        print("\nUsage:")
        print("  python3 timestamp_converter_free.py 1707772800")
        print("  python3 timestamp_converter_free.py \"2024-02-12 15:30:00\"")
        print("  python3 timestamp_converter_free.py \"2024-02-12\"")
        sys.exit(1)
    
    user_input = ' '.join(sys.argv[1:])
    
    print(f"🔄 Converting: {user_input}\n")
    
    input_type, parsed = parse_input(user_input)
    
    if input_type is None:
        print("❌ Could not parse input.")
        print("\nSupported formats:")
        print("  - Unix timestamp: 1707772800")
        print("  - ISO date: 2024-02-12T15:30:00")
        print("  - Date: 2024-02-12")
        print("  - Datetime: \"2024-02-12 15:30:00\"")
        sys.exit(1)
    
    if input_type == 'timestamp':
        result = convert_timestamp(parsed)
        print(f"{'='*60}")
        print(f"🕐 TIMESTAMP CONVERSION")
        print(f"{'='*60}")
        print(f"\nInput: {int(parsed)} seconds")
        print(f"\n📅 Human Readable:")
        print(f"   {result['readable_utc']}")
        print(f"   {result['readable_local']} (local)")
        print(f"\n🔢 Unix Timestamps:")
        print(f"   Seconds:     {result['unix_seconds']}")
        print(f"   Milliseconds: {result['unix_millis']}")
        print(f"\n📝 ISO Format:")
        print(f"   {result['iso_utc']}")
        print(f"\n📆 Date Only: {result['date_only']}")
        print(f"🕐 Time Only: {result['time_only']}")
    else:
        result = convert_datetime(parsed)
        print(f"{'='*60}")
        print(f"📅 DATE CONVERSION")
        print(f"{'='*60}")
        print(f"\nInput: {user_input}")
        print(f"\n🔢 Unix Timestamps:")
        print(f"   Seconds:     {result['unix_seconds']}")
        print(f"   Milliseconds: {result['unix_millis']}")
        print(f"\n📝 ISO Format:")
        print(f"   {result['iso_utc']}")
    
    print(f"\n{'='*60}")
    print("\n💡 Want timezone conversion and batch processing?")
    print("   Upgrade to PD_Researcher v1 for advanced time tools")
    print("   Pay with crypto: FEKY6bDoqBnsQZVT3XbEYS4b1DJ8QoA64G5hXycfTAhQ")
    print("="*60)

if __name__ == "__main__":
    main()
