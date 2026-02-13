#!/usr/bin/env python3
"""
crontool — Cron expression parser and human-readable translator
Tool #66 — Free CLI Tool for PD Researcher
"""

import argparse
import re
import sys
from datetime import datetime


def parse_cron(expression):
    """Parse cron expression and return components."""
    parts = expression.strip().split()
    
    if len(parts) != 5:
        return None, "Invalid cron expression: must have 5 fields"
    
    minute, hour, day_of_month, month, day_of_week = parts
    
    return {
        'minute': minute,
        'hour': hour,
        'day_of_month': day_of_month,
        'month': month,
        'day_of_week': day_of_week
    }, None


def describe_field(value, field_type):
    """Convert cron field value to human description."""
    
    descriptions = {
        'minute': {
            '*': 'every minute',
            '*/5': 'every 5 minutes',
            '*/10': 'every 10 minutes',
            '*/15': 'every 15 minutes',
            '*/30': 'every 30 minutes',
            '0': 'at minute 0',
        },
        'hour': {
            '*': 'every hour',
            '*/2': 'every 2 hours',
            '*/3': 'every 3 hours',
            '*/6': 'every 6 hours',
            '*/12': 'every 12 hours',
            '0': 'at midnight',
            '12': 'at noon',
        },
        'day_of_month': {
            '*': 'every day',
            '1': 'on the 1st',
            '15': 'on the 15th',
            'L': 'on the last day',
        },
        'month': {
            '*': 'every month',
            '1': 'in January',
            '2': 'in February',
            '3': 'in March',
            '4': 'in April',
            '5': 'in May',
            '6': 'in June',
            '7': 'in July',
            '8': 'in August',
            '9': 'in September',
            '10': 'in October',
            '11': 'in November',
            '12': 'in December',
            '*/3': 'every 3 months',
        },
        'day_of_week': {
            '*': 'every day',
            '0': 'on Sunday',
            '1': 'on Monday',
            '2': 'on Tuesday',
            '3': 'on Wednesday',
            '4': 'on Thursday',
            '5': 'on Friday',
            '6': 'on Saturday',
            '0,6': 'on weekends',
            '1-5': 'on weekdays',
        }
    }
    
    # Check predefined descriptions
    if value in descriptions.get(field_type, {}):
        return descriptions[field_type][value]
    
    # Handle ranges
    if '-' in value and ',' not in value:
        start, end = value.split('-')
        if field_type == 'day_of_week':
            days = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']
            return f"from {days[int(start)]} to {days[int(end)]}"
        return f"from {start} to {end}"
    
    # Handle lists
    if ',' in value:
        items = value.split(',')
        if field_type == 'day_of_week':
            days = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']
            return f"on {', '.join(days[int(i)] for i in items if i.isdigit())}"
        return f"at {', '.join(items)}"
    
    # Handle step values
    if value.startswith('*/'):
        step = value[2:]
        unit = 'minutes' if field_type == 'minute' else 'hours' if field_type == 'hour' else 'days'
        return f"every {step} {unit}"
    
    # Default
    if field_type == 'minute':
        return f"at minute {value}"
    if field_type == 'hour':
        return f"at {value}:00"
    if field_type == 'day_of_month':
        return f"on the {value}{'th' if value not in ['1','21','31'] else 'st' if value in ['1','21','31'] else 'nd' if value == '2' else 'rd'}"
    
    return value


def to_human_readable(parsed):
    """Convert parsed cron to human readable description."""
    parts = []
    
    # Handle special cases first
    if parsed['minute'] == '0' and parsed['hour'] == '0':
        parts.append("At midnight")
    elif parsed['minute'] == '0' and parsed['hour'] == '12':
        parts.append("At noon")
    elif parsed['minute'] == '0':
        parts.append(f"At {parsed['hour']}:00")
    elif parsed['hour'] == '*':
        parts.append(describe_field(parsed['minute'], 'minute'))
    else:
        parts.append(f"At {parsed['hour']}:{parsed['minute'].zfill(2)}")
    
    # Add other fields
    if parsed['day_of_month'] != '*':
        parts.append(describe_field(parsed['day_of_month'], 'day_of_month'))
    
    if parsed['month'] != '*':
        parts.append(describe_field(parsed['month'], 'month'))
    
    if parsed['day_of_week'] != '*':
        parts.append(describe_field(parsed['day_of_week'], 'day_of_week'))
    
    return ' '.join(parts)


def get_next_runs(expression, count=5):
    """Get next scheduled times (simplified)."""
    # This is a simplified version - full implementation would need croniter
    return ["Install 'croniter' for next run calculation: pip install croniter"]


def main():
    parser = argparse.ArgumentParser(
        description='Cron expression parser and translator',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  crontool "0 9 * * 1-5"              # Describe a cron expression
  crontool "*/5 * * * *" -v          # Verbose output
  crontool "0 0 * * *" --next        # Show next scheduled times
        """
    )
    
    parser.add_argument('expression', help='Cron expression (5 fields)')
    parser.add_argument('-v', '--verbose', action='store_true',
                       help='Show detailed breakdown')
    parser.add_argument('-n', '--next', type=int, nargs='?', const=5, metavar='N',
                       help='Show next N scheduled times (default: 5)')
    parser.add_argument('--validate', action='store_true',
                       help='Only validate the expression')
    
    args = parser.parse_args()
    
    # Parse
    parsed, error = parse_cron(args.expression)
    
    if error:
        print(f"Error: {error}", file=sys.stderr)
        sys.exit(1)
    
    if args.validate:
        print("✅ Valid cron expression")
        return
    
    # Output
    if args.verbose:
        print(f"Expression: {args.expression}")
        print(f"Minute:       {parsed['minute']:10} → {describe_field(parsed['minute'], 'minute')}")
        print(f"Hour:         {parsed['hour']:10} → {describe_field(parsed['hour'], 'hour')}")
        print(f"Day of Month: {parsed['day_of_month']:10} → {describe_field(parsed['day_of_month'], 'day_of_month')}")
        print(f"Month:        {parsed['month']:10} → {describe_field(parsed['month'], 'month')}")
        print(f"Day of Week:  {parsed['day_of_week']:10} → {describe_field(parsed['day_of_week'], 'day_of_week')}")
        print(f"\nHuman readable: {to_human_readable(parsed)}")
    else:
        print(to_human_readable(parsed))
    
    if args.next:
        print("\nNext runs:")
        for run in get_next_runs(args.expression, args.next):
            print(f"  {run}")


if __name__ == '__main__':
    main()
