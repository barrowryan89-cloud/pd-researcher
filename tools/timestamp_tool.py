#!/usr/bin/env python3
"""
timestamp_tool.py — Unix timestamp converter
Tool #38 in the PD Researcher free tools collection
"""

import argparse
import sys
from datetime import datetime, timezone
from typing import Optional


def now_timestamp() -> int:
    """Get current Unix timestamp."""
    return int(datetime.now(timezone.utc).timestamp())


def timestamp_to_datetime(ts: int, tz: Optional[str] = None) -> str:
    """Convert Unix timestamp to human-readable datetime."""
    try:
        dt = datetime.fromtimestamp(ts, tz=timezone.utc)
        if tz:
            import pytz
            dt = dt.astimezone(pytz.timezone(tz))
        return dt.strftime('%Y-%m-%d %H:%M:%S %Z')
    except Exception as e:
        print(f"Error converting timestamp: {e}", file=sys.stderr)
        sys.exit(1)


def datetime_to_timestamp(date_str: str, fmt: Optional[str] = None) -> int:
    """Convert datetime string to Unix timestamp."""
    try:
        if fmt:
            dt = datetime.strptime(date_str, fmt)
        else:
            # Try common formats
            formats = [
                '%Y-%m-%d %H:%M:%S',
                '%Y-%m-%d',
                '%m/%d/%Y %H:%M:%S',
                '%m/%d/%Y',
                '%d/%m/%Y %H:%M:%S',
                '%d/%m/%Y',
                '%Y-%m-%dT%H:%M:%S',
                '%Y-%m-%dT%H:%M:%SZ',
            ]
            for f in formats:
                try:
                    dt = datetime.strptime(date_str, f)
                    break
                except ValueError:
                    continue
            else:
                raise ValueError(f"Could not parse date: {date_str}")
        
        return int(dt.replace(tzinfo=timezone.utc).timestamp())
    except Exception as e:
        print(f"Error parsing datetime: {e}", file=sys.stderr)
        sys.exit(1)


def format_duration(seconds: int) -> str:
    """Format duration in seconds to human-readable string."""
    units = [
        ('year', 365 * 24 * 60 * 60),
        ('month', 30 * 24 * 60 * 60),
        ('week', 7 * 24 * 60 * 60),
        ('day', 24 * 60 * 60),
        ('hour', 60 * 60),
        ('minute', 60),
        ('second', 1),
    ]
    
    parts = []
    remaining = seconds
    
    for name, secs in units:
        if remaining >= secs:
            count = remaining // secs
            remaining %= secs
            parts.append(f"{count} {name}{'s' if count != 1 else ''}")
    
    return ', '.join(parts) if parts else '0 seconds'


def main():
    parser = argparse.ArgumentParser(
        description="Unix timestamp converter",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s now                    # Get current timestamp
  %(prog)s to-date 1704067200     # Convert timestamp to date
  %(prog)s to-ts "2024-01-01"     # Convert date to timestamp
  %(prog)s diff 1704067200        # Time difference from now
  %(prog)s diff 1704067200 1706745600  # Time between two timestamps
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Command to run')
    
    # Now command
    subparsers.add_parser('now', help='Get current timestamp')
    
    # To-date command
    to_date_parser = subparsers.add_parser('to-date', help='Convert timestamp to date')
    to_date_parser.add_argument('timestamp', type=int, help='Unix timestamp')
    to_date_parser.add_argument('-t', '--timezone', help='Target timezone (e.g., US/Eastern)')
    
    # To-ts command
    to_ts_parser = subparsers.add_parser('to-ts', help='Convert date to timestamp')
    to_ts_parser.add_argument('date', help='Date string to convert')
    to_ts_parser.add_argument('-f', '--format', help='Date format (e.g., %%Y-%%m-%%d)')
    
    # Diff command
    diff_parser = subparsers.add_parser('diff', help='Calculate time difference')
    diff_parser.add_argument('timestamp1', type=int, help='First timestamp')
    diff_parser.add_argument('timestamp2', type=int, nargs='?', help='Second timestamp (defaults to now)')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    if args.command == 'now':
        print(now_timestamp())
    
    elif args.command == 'to-date':
        result = timestamp_to_datetime(args.timestamp, args.timezone)
        print(result)
    
    elif args.command == 'to-ts':
        result = datetime_to_timestamp(args.date, args.format)
        print(result)
    
    elif args.command == 'diff':
        ts1 = args.timestamp1
        ts2 = args.timestamp2 if args.timestamp2 else now_timestamp()
        diff = abs(ts2 - ts1)
        print(f"Seconds: {diff}")
        print(f"Duration: {format_duration(diff)}")
        
        if ts2 > ts1:
            print(f"Status: {ts1} is in the past")
        elif ts2 < ts1:
            print(f"Status: {ts1} is in the future")
        else:
            print(f"Status: Same time")


if __name__ == '__main__':
    main()
