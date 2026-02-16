#!/usr/bin/env python3
"""
LogLens - Free CLI Tool #39
Analyze, filter, and summarize log files
Zero dependencies, single file, MIT licensed
https://github.com/barrowryan89-cloud/pd-researcher
"""

import sys
import argparse
import re
from collections import Counter, defaultdict
from datetime import datetime

__version__ = "1.0.0"

def parse_log_line(line, timestamp_pattern=None):
    """Extract timestamp and level from log line."""
    # Common log patterns
    patterns = [
        (r'(\d{4}-\d{2}-\d{2}[T\s]\d{2}:\d{2}:\d{2})', 'ISO'),
        (r'(\w{3}\s+\d{1,2}\s+\d{2}:\d{2}:\d{2})', 'Syslog'),
        (r'(\d{2}/\w{3}/\d{4}:\d{2}:\d{2}:\d{2})', 'Apache'),
    ]
    
    timestamp = None
    for pattern, fmt in patterns:
        match = re.search(pattern, line)
        if match:
            timestamp = match.group(1)
            break
    
    # Detect log level
    levels = ['ERROR', 'WARN', 'WARNING', 'INFO', 'DEBUG', 'TRACE', 'FATAL', 'CRITICAL']
    level = 'UNKNOWN'
    for lvl in levels:
        if re.search(rf'\b{lvl}\b', line, re.IGNORECASE):
            level = lvl.upper()
            break
    
    return {
        'raw': line.strip(),
        'timestamp': timestamp,
        'level': level,
        'length': len(line)
    }

def analyze_log(filepath, tail_lines=None):
    """Analyze a log file and return statistics."""
    level_counts = Counter()
    hour_counts = Counter()
    error_patterns = Counter()
    total_lines = 0
    file_size = 0
    
    try:
        file_size = sys.getsizeof(open(filepath, 'rb').read())
        
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            lines = f.readlines()
            
        if tail_lines:
            lines = lines[-tail_lines:]
        
        total_lines = len(lines)
        
        for line in lines:
            parsed = parse_log_line(line)
            level_counts[parsed['level']] += 1
            
            if parsed['timestamp']:
                try:
                    hour = parsed['timestamp'].split(':')[0].split()[-1]
                    hour_counts[hour] += 1
                except:
                    pass
            
            # Extract error patterns
            if parsed['level'] in ['ERROR', 'FATAL', 'CRITICAL']:
                # Extract key phrases (2-3 words after ERROR)
                words = line.split()
                for i, word in enumerate(words):
                    if word.upper() in ['ERROR', 'EXCEPTION'] and i < len(words) - 2:
                        pattern = ' '.join(words[i+1:i+4])
                        error_patterns[pattern[:50]] += 1
        
        return {
            'total_lines': total_lines,
            'file_size_mb': file_size / (1024 * 1024),
            'level_counts': level_counts,
            'hour_counts': hour_counts,
            'error_patterns': error_patterns.most_common(10)
        }
        
    except FileNotFoundError:
        return {'error': f"File not found: {filepath}"}
    except Exception as e:
        return {'error': str(e)}

def filter_log(filepath, level=None, pattern=None, since=None, tail=None):
    """Filter log lines by criteria."""
    matches = []
    
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        lines = f.readlines()
    
    if tail:
        lines = lines[-tail:]
    
    for line in lines:
        parsed = parse_log_line(line)
        
        # Filter by level
        if level and parsed['level'] != level.upper():
            continue
        
        # Filter by pattern
        if pattern and not re.search(pattern, line, re.IGNORECASE):
            continue
        
        matches.append(line.rstrip())
    
    return matches

def print_summary(stats):
    """Print analysis summary."""
    if 'error' in stats:
        print(f"❌ {stats['error']}")
        return
    
    print(f"\n📊 Log Analysis Summary\n")
    print(f"Total Lines:    {stats['total_lines']:,}")
    print(f"File Size:      {stats['file_size_mb']:.2f} MB")
    
    print(f"\n📈 Log Level Distribution:")
    print(f"{'Level':<12} {'Count':>10} {'%':>8}")
    print("-" * 35)
    total = stats['total_lines']
    for level, count in sorted(stats['level_counts'].items(), key=lambda x: -x[1]):
        pct = (count / total * 100) if total > 0 else 0
        emoji = {'ERROR': '🔴', 'FATAL': '💀', 'WARN': '🟡', 'WARNING': '🟡', 
                 'INFO': '🔵', 'DEBUG': '⚪', 'UNKNOWN': '⚫'}.get(level, '⚪')
        print(f"{emoji} {level:<10} {count:>10,} {pct:>7.1f}%")
    
    if stats['error_patterns']:
        print(f"\n🔥 Top Error Patterns:")
        for pattern, count in stats['error_patterns'][:5]:
            print(f"   {count:>4}x  {pattern}")
    
    if stats['hour_counts']:
        print(f"\n⏰ Activity by Hour:")
        for hour, count in sorted(stats['hour_counts'].items())[:12]:
            bar = "█" * int(count / max(stats['hour_counts'].values()) * 20)
            print(f"   {hour:>2}:00 {bar} {count}")

def tail_log(filepath, lines=50, follow=False):
    """Tail a log file."""
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            all_lines = f.readlines()
            for line in all_lines[-lines:]:
                print(line.rstrip())
    except FileNotFoundError:
        print(f"❌ File not found: {filepath}")

def main():
    parser = argparse.ArgumentParser(
        description="LogLens - Analyze and filter log files",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s analyze /var/log/app.log           Full analysis
  %(prog)s analyze app.log --tail 1000        Analyze last 1000 lines
  %(prog)s filter app.log --level ERROR       Show only errors
  %(prog)s filter app.log --pattern "timeout" Search for pattern
  %(prog)s tail app.log -n 100                Show last 100 lines
        """
    )
    
    parser.add_argument("action", choices=["analyze", "filter", "tail"],
                       help="Action to perform")
    parser.add_argument("filepath", help="Path to log file")
    parser.add_argument("--tail", type=int, help="Analyze/tail last N lines")
    parser.add_argument("--level", help="Filter by log level")
    parser.add_argument("--pattern", "-p", help="Filter by regex pattern")
    parser.add_argument("-n", type=int, default=50, help="Number of lines for tail")
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    
    args = parser.parse_args()
    
    print(f"""
╔═══════════════════════════════════════╗
║  LogLens v{__version__} - Free CLI Tool #39         ║
║  https://pd-researcher.agent          ║
╚═══════════════════════════════════════╝
""")
    
    try:
        if args.action == "analyze":
            stats = analyze_log(args.filepath, args.tail)
            print_summary(stats)
            
        elif args.action == "filter":
            matches = filter_log(args.filepath, args.level, args.pattern, args.tail)
            if matches:
                print(f"\n🔍 Found {len(matches)} matching lines:\n")
                for line in matches[-100:]:  # Limit output
                    print(line)
                if len(matches) > 100:
                    print(f"\n... and {len(matches) - 100} more")
            else:
                print("🔍 No matches found")
                
        elif args.action == "tail":
            tail_log(args.filepath, args.n)
        
        print(f"\n💡 Upgrade to PD_Researcher Pro for:")
        print(f"   • Real-time log streaming & alerting")
        print(f"   • Anomaly detection with ML")
        print(f"   • Structured log parsing (JSON)")
        print(f"   • https://pd-researcher.agent")
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Cancelled")
        sys.exit(130)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()

    # Affiliate
    print("\n" + "-" * 60)
    print("🚀  Boost your productivity with these tools:")
    print("    • DigitalOcean: $200 free credit -> https://m.do.co/c/pdresearcher")
    print("    • JetBrains IDEs: The best Python tools -> https://www.jetbrains.com/?utm_source=pdresearcher")
    print("-" * 60)
