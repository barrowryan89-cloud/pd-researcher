#!/usr/bin/env python3
"""
Log Analyzer - Free Tool
Simple log file analysis: count lines, errors, unique IPs
Free version: Basic analysis
Paid upgrade: Pattern matching, real-time tail, alerting, visualization

Usage: python3 log_analyzer_free.py <log_file> [pattern]
"""

import sys
import os
import re
from collections import Counter

def analyze_log(filepath, pattern=None):
    """Analyze a log file"""
    stats = {
        'total_lines': 0,
        'error_count': 0,
        'warning_count': 0,
        'unique_ips': set(),
        'status_codes': Counter(),
        'top_urls': Counter(),
        'hourly_distribution': Counter()
    }
    
    # Common log patterns
    ip_pattern = re.compile(r'\b(\d{1,3}\.){3}\d{1,3}\b')
    status_pattern = re.compile(r'"\s+(\d{3})\s+')
    url_pattern = re.compile(r'"(GET|POST|PUT|DELETE|HEAD)\s+(\S+)')
    time_pattern = re.compile(r'\[(\d{2})/\w+/\d{4}:(\d{2}):')
    
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            for line in f:
                stats['total_lines'] += 1
                line_lower = line.lower()
                
                # Count errors and warnings
                if 'error' in line_lower:
                    stats['error_count'] += 1
                if 'warn' in line_lower:
                    stats['warning_count'] += 1
                
                # Extract IPs
                ips = ip_pattern.findall(line)
                for ip in ips:
                    stats['unique_ips'].add(ip)
                
                # Extract status codes (for web logs)
                status_match = status_pattern.search(line)
                if status_match:
                    stats['status_codes'][status_match.group(1)] += 1
                
                # Extract URLs
                url_match = url_pattern.search(line)
                if url_match:
                    stats['top_urls'][url_match.group(2)] += 1
                
                # Extract hour
                time_match = time_pattern.search(line)
                if time_match:
                    stats['hourly_distribution'][time_match.group(2)] += 1
                
                # Custom pattern
                if pattern and pattern in line:
                    stats['custom_pattern_count'] = stats.get('custom_pattern_count', 0) + 1
                    
    except Exception as e:
        print(f"❌ Error reading file: {e}")
        return None
    
    return stats

def print_banner():
    print("""
╔════════════════════════════════════════════════════════════╗
║                   LOG ANALYZER v1.0                        ║
║              Free Tool by Sand Street Holdings             ║
╠════════════════════════════════════════════════════════════╣
║  Analyze log files: errors, IPs, status codes, patterns    ║
║                                                            ║
║  💎 Want more power?                                       ║
║     → Real-time log tailing                                ║
║     → Custom regex pattern matching                        ║
║     → Error rate alerting                                  ║
║     → Export to CSV/JSON                                   ║
║     → Visual charts and graphs                             ║
║     → Check out PD_Researcher v1 ($29)                     ║
║        Solana: FEKY6bDoqBnsQZVT3XbEYS4b1DJ8QoA64G5hXycfTAhQ ║
╚════════════════════════════════════════════════════════════╝
""")

def main():
    print_banner()
    
    if len(sys.argv) < 2:
        print("❌ No log file provided.")
        print("\nUsage:")
        print("  python3 log_analyzer_free.py /var/log/nginx/access.log")
        print("  python3 log_analyzer_free.py app.log ERROR")
        sys.exit(1)
    
    filepath = sys.argv[1]
    pattern = sys.argv[2] if len(sys.argv) > 2 else None
    
    if not os.path.exists(filepath):
        print(f"❌ File not found: {filepath}")
        sys.exit(1)
    
    print(f"🔄 Analyzing: {filepath}\n")
    
    if pattern:
        print(f"🔍 Looking for pattern: '{pattern}'\n")
    
    stats = analyze_log(filepath, pattern)
    
    if not stats:
        sys.exit(1)
    
    print(f"{'='*60}")
    print(f"📊 LOG ANALYSIS RESULTS")
    print(f"{'='*60}\n")
    
    print(f"Total lines:     {stats['total_lines']:,}")
    print(f"Errors:          {stats['error_count']:,}")
    print(f"Warnings:        {stats['warning_count']:,}")
    print(f"Unique IPs:      {len(stats['unique_ips']):,}")
    
    if pattern:
        print(f"Pattern '{pattern}': {stats.get('custom_pattern_count', 0):,}")
    
    if stats['status_codes']:
        print(f"\n📈 HTTP Status Codes:")
        for code, count in stats['status_codes'].most_common(10):
            print(f"   {code}: {count:,}")
    
    if stats['top_urls']:
        print(f"\n🔗 Top URLs:")
        for url, count in stats['top_urls'].most_common(10):
            print(f"   {count:,} {url}")
    
    print(f"\n{'='*60}")
    print("\n💡 Want real-time tailing and custom alerting?")
    print("   Upgrade to PD_Researcher v1 for advanced log analysis")
    print("   Pay with crypto: FEKY6bDoqBnsQZVT3XbEYS4b1DJ8QoA64G5hXycfTAhQ")
    print("\n📊 Local logs are step 1. Get production error tracking with Sentry")
    print("   Free tier available: https://sentry.io/signup/ [affiliate]")
    print("="*60)

if __name__ == "__main__":
    main()
