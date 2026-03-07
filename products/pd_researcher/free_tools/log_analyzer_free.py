#!/usr/bin/env python3
"""
🪵 Log Analyzer Free — Extract insights from log files
Quickly analyze logs: find errors, count occurrences, spot patterns

FREE VERSION: Basic analysis (single file)
PAID UPGRADE: PD_Researcher v1 — Multi-file, real-time monitoring, alerting
Upgrade: Send $29 in SOL/USDC to: FEKY6bDoqBnsQZVT3XbEYS4b1DJ8QoA64G5hXycfTAhQ
Support: Email screenshot of payment to devilliers.cody@gmail.com
"""

import sys
import re
import argparse
from collections import Counter
from datetime import datetime

VERSION = "1.0.0"

PAYMENT_ADDRESS = "FEKY6bDoqBnsQZVT3XbEYS4b1DJ8QoA64G5hXycfTAhQ"

def print_banner():
    print("""
╔═══════════════════════════════════════════════════════════╗
║                  🪵 LOG ANALYZER FREE v1.0                 ║
║              Quick insights from your logs                 ║
╠═══════════════════════════════════════════════════════════╣
║  Analyze errors, patterns, and trends in log files        ║
║  💎 Upgrade: PD_Researcher v1 for advanced features       ║
╚═══════════════════════════════════════════════════════════╝
    """)

def print_upgrade_cta():
    print(f"""
┌─────────────────────────────────────────────────────────────┐
│ 💎 WANT MORE POWER?                                          │
│                                                              │
│   PD_Researcher v1 includes:                                 │
│   • Multi-file analysis & aggregation                        │
│   • Real-time log monitoring                                 │
│   • Pattern-based alerting (Slack, email, webhook)           │
│   • Custom regex rule engine                                 │
│   • Export to JSON/CSV/Excel                                 │
│                                                              │
│   Upgrade: Send $29 in SOL/USDC to:                          │
│   {PAYMENT_ADDRESS}     │
│                                                              │
│   Then email screenshot to: devilliers.cody@gmail.com        │
└─────────────────────────────────────────────────────────────┘
    """)

def parse_log_line(line):
    """Extract timestamp and level from common log formats."""
    patterns = [
        # ISO format: 2026-02-12 10:30:45
        (r'(\d{4}-\d{2}-\d{2}[T\s]\d{2}:\d{2}:\d{2})', 'iso'),
        # Apache/Nginx: [12/Feb/2026:10:30:45
        (r'\[(\d{2}/\w+/\d{4}:\d{2}:\d{2}:\d{2})', 'apache'),
        # Syslog: Feb 12 10:30:45
        (r'^(\w{3}\s+\d{1,2}\s+\d{2}:\d{2}:\d{2})', 'syslog'),
    ]
    
    timestamp = None
    for pattern, fmt in patterns:
        match = re.search(pattern, line)
        if match:
            timestamp = match.group(1)
            break
    
    # Extract log level
    level_match = re.search(r'\b(DEBUG|INFO|WARNING|WARN|ERROR|ERR|CRITICAL|FATAL)\b', line, re.IGNORECASE)
    level = level_match.group(1).upper() if level_match else 'UNKNOWN'
    
    return {'timestamp': timestamp, 'level': level, 'raw': line.strip()}

def analyze_log(filepath, top_errors=10, show_context=True):
    """Analyze a log file and return statistics."""
    print(f"\n📁 Analyzing: {filepath}\n")
    
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            lines = f.readlines()
    except FileNotFoundError:
        print(f"❌ Error: File not found: {filepath}")
        return
    except Exception as e:
        print(f"❌ Error reading file: {e}")
        return
    
    total_lines = len(lines)
    parsed_lines = []
    error_lines = []
    
    print(f"   Total lines: {total_lines:,}")
    
    # Parse each line
    for i, line in enumerate(lines, 1):
        parsed = parse_log_line(line)
        parsed['line_num'] = i
        parsed_lines.append(parsed)
        
        if parsed['level'] in ('ERROR', 'ERR', 'CRITICAL', 'FATAL'):
            error_lines.append(parsed)
    
    # Level distribution
    level_counts = Counter([p['level'] for p in parsed_lines])
    
    print(f"\n📊 Log Level Distribution:")
    print("   " + "-" * 40)
    for level, count in level_counts.most_common():
        pct = (count / total_lines) * 100
        bar = "█" * int(pct / 2)
        print(f"   {level:12} {count:>6,} ({pct:5.1f}%) {bar}")
    
    # Error summary
    error_count = len(error_lines)
    print(f"\n🚨 Error Summary:")
    print(f"   Total errors: {error_count}")
    if total_lines > 0:
        print(f"   Error rate: {(error_count/total_lines)*100:.2f}%")
    
    if error_count > 0 and show_context:
        print(f"\n🔍 Top {min(top_errors, error_count)} Errors:")
        print("   " + "-" * 70)
        
        # Group similar errors
        error_patterns = Counter([e['raw'] for e in error_lines])
        
        for error, count in error_patterns.most_common(top_errors):
            # Truncate long lines
            display = error[:80] + "..." if len(error) > 80 else error
            print(f"   [{count:>3}x] {display}")
    
    # Time range (if timestamps found)
    timestamps = [p['timestamp'] for p in parsed_lines if p['timestamp']]
    if timestamps:
        print(f"\n⏰ Time Range:")
        print(f"   First entry: {timestamps[0]}")
        print(f"   Last entry:  {timestamps[-1]}")
    
    # Common patterns
    print(f"\n📝 Common Patterns:")
    
    # IP addresses
    ip_pattern = re.compile(r'\b(?:\d{1,3}\.){3}\d{1,3}\b')
    ips = []
    for line in lines:
        ips.extend(ip_pattern.findall(line))
    if ips:
        top_ips = Counter(ips).most_common(5)
        print(f"   Top IP addresses:")
        for ip, count in top_ips:
            print(f"      {ip}: {count} occurrences")
    
    # HTTP status codes
    status_pattern = re.compile(r'\s(\d{3})\s')
    statuses = []
    for line in lines:
        matches = status_pattern.findall(line)
        statuses.extend(matches)
    if statuses:
        status_counts = Counter(statuses).most_common(5)
        print(f"   HTTP status codes:")
        for status, count in status_counts:
            emoji = "✅" if status.startswith('2') else "⚠️" if status.startswith('3') else "❌"
            print(f"      {emoji} {status}: {count} occurrences")
    
    print(f"\n✅ Analysis complete!")

def main():
    parser = argparse.ArgumentParser(
        description='🪵 Log Analyzer Free — Quick log file insights',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=f"""
Examples:
  %(prog)s app.log                    # Basic analysis
  %(prog)s app.log --errors 20        # Show top 20 errors
  %(prog)s app.log --no-context       # Hide error context

Upgrade to PD_Researcher v1:
  Send $29 in SOL/USDC to: {PAYMENT_ADDRESS}
        """
    )
    
    parser.add_argument('logfile', help='Path to log file to analyze')
    parser.add_argument('--errors', '-e', type=int, default=10, 
                        help='Number of top errors to show (default: 10)')
    parser.add_argument('--no-context', action='store_true',
                        help='Hide error context/details')
    parser.add_argument('--version', '-v', action='version', version=f'%(prog)s {VERSION}')
    
    args = parser.parse_args()
    
    print_banner()
    analyze_log(args.logfile, top_errors=args.errors, show_context=not args.no_context)
    print_upgrade_cta()

if __name__ == '__main__':
    main()
