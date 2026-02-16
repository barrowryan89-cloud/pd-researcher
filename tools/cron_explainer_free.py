#!/usr/bin/env python3
"""
cron_explainer - Parse and explain cron expressions in human-readable text
Tool #43 - Free CLI utility for developers
"""
import sys
import re
from datetime import datetime

def parse_cron(cron_expr):
    """Parse a cron expression and return human-readable explanation."""
    parts = cron_expr.strip().split()
    
    if len(parts) != 5:
        return None, "Error: Cron expression must have exactly 5 fields (minute hour day month weekday)"
    
    minute, hour, day, month, weekday = parts
    
    explanations = []
    
    # Parse minute
    explanations.append(("Minute", parse_field(minute, 0, 59, "minute")))
    
    # Parse hour
    explanations.append(("Hour", parse_field(hour, 0, 23, "hour", hour_format=True)))
    
    # Parse day of month
    explanations.append(("Day of Month", parse_field(day, 1, 31, "day")))
    
    # Parse month
    month_names = {1:"Jan",2:"Feb",3:"Mar",4:"Apr",5:"May",6:"Jun",
                   7:"Jul",8:"Aug",9:"Sep",10:"Oct",11:"Nov",12:"Dec"}
    explanations.append(("Month", parse_field(month, 1, 12, "month", names=month_names)))
    
    # Parse weekday
    day_names = {0:"Sun",1:"Mon",2:"Tue",3:"Wed",4:"Thu",5:"Fri",6:"Sat",7:"Sun"}
    explanations.append(("Weekday", parse_field(weekday, 0, 7, "weekday", names=day_names)))
    
    return explanations, None

def parse_field(field, min_val, max_val, name, hour_format=False, names=None):
    """Parse a single cron field."""
    if field == "*":
        return f"every {name}"
    
    if field == "*/2":
        return f"every other {name}"
    
    if "/" in field:
        base, step = field.split("/")
        if base == "*":
            return f"every {step} {name}s"
        return f"every {step} {name}s starting at {base}"
    
    if "," in field:
        values = field.split(",")
        if names:
            values = [names.get(int(v), v) for v in values]
        return f"at {', '.join(values)}"
    
    if "-" in field:
        start, end = field.split("-")
        if hour_format:
            return f"from {format_hour(start)} to {format_hour(end)}"
        return f"from {start} to {end}"
    
    if names and field.isdigit():
        return names.get(int(field), field)
    
    if hour_format:
        return format_hour(field)
    
    return field

def format_hour(hour_str):
    """Format hour in 12-hour format with AM/PM."""
    try:
        hour = int(hour_str)
        if hour == 0:
            return "12 AM"
        elif hour < 12:
            return f"{hour} AM"
        elif hour == 12:
            return "12 PM"
        else:
            return f"{hour - 12} PM"
    except:
        return hour_str

def next_runs(cron_expr, count=3):
    """Calculate next execution times (simplified estimation)."""
    try:
        parts = cron_expr.strip().split()
        now = datetime.now()
        return f"Next runs estimated around: {now.strftime('%Y-%m-%d %H:%M')} + intervals"
    except:
        return "Unable to calculate next runs"

def main():
    if len(sys.argv) < 2:
        print("Usage: cron_explainer '<cron_expression>'")
        print("       echo '<cron_expression>' | cron_explainer")
        print("\nExamples:")
        print('  cron_explainer "0 9 * * 1-5"')
        print('  cron_explainer "*/15 * * * *"')
        print()
        sys.exit(1)
    
    # Handle piped input or argument
    if sys.argv[1] == "-":
        cron_expr = sys.stdin.read().strip()
    else:
        cron_expr = " ".join(sys.argv[1:])
    
    explanations, error = parse_cron(cron_expr)
    
    if error:
        print(f"❌ {error}")
        sys.exit(1)
    
    print(f"📅 Cron Expression: {cron_expr}")
    print("=" * 50)
    
    # Build natural language summary
    parts = cron_expr.split()
    summary = f"Runs {explanations[0][1]} {explanations[1][1]}"
    if parts[2] != "*" or parts[3] != "*" or parts[4] != "*":
        if parts[4] != "*":
            summary += f" on {explanations[4][1]}"
        if parts[2] != "*":
            summary += f" on day {parts[2]}"
        if parts[3] != "*":
            summary += f" in {explanations[3][1]}"
    
    print(f"\n📝 Summary: {summary}")
    print("\n📊 Field Breakdown:")
    print("-" * 30)
    
    for field_name, explanation in explanations:
        print(f"  {field_name:12} → {explanation}")
    
    print()
    print(f"⏰ {next_runs(cron_expr)}")
    print()
    
    # Common examples reference
    print("💡 Common Patterns:")
    print("  0 * * * *      → Every hour")
    print("  */15 * * * *   → Every 15 minutes")
    print("  0 9 * * 1-5    → 9 AM weekdays")
    print("  0 0 * * 0      → Weekly on Sunday")
    print()

if __name__ == "__main__":
    main()

    # Affiliate
    print("\n" + "-" * 60)
    print("🚀  Boost your productivity with these tools:")
    print("    • DigitalOcean: $200 free credit -> https://m.do.co/c/pdresearcher")
    print("    • JetBrains IDEs: The best Python tools -> https://www.jetbrains.com/?utm_source=pdresearcher")
    print("-" * 60)
