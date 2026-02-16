#!/usr/bin/env python3
"""
Line Counter - Free Tool
Count lines, words, characters in files
Free version: Basic counting
Paid upgrade: Stats by file type, trends, visualizations

Usage: python3 line_counter_free.py <file or directory>
"""

import sys
import os

def count_file(filepath):
    """Count lines, words, chars in a file"""
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        
        lines = content.split('\n')
        words = content.split()
        chars = len(content)
        
        return {
            'lines': len(lines),
            'words': len(words),
            'chars': chars,
            'bytes': len(content.encode('utf-8'))
        }
    except Exception as e:
        return {'error': str(e)}

def count_directory(directory, extensions=None):
    """Count all files in directory"""
    totals = {'files': 0, 'lines': 0, 'words': 0, 'chars': 0, 'bytes': 0}
    file_stats = []
    
    for root, dirs, files in os.walk(directory):
        for filename in files:
            if extensions and not any(filename.endswith(ext) for ext in extensions):
                continue
            
            filepath = os.path.join(root, filename)
            stats = count_file(filepath)
            
            if 'error' not in stats:
                totals['files'] += 1
                totals['lines'] += stats['lines']
                totals['words'] += stats['words']
                totals['chars'] += stats['chars']
                totals['bytes'] += stats['bytes']
                
                file_stats.append((filepath, stats))
    
    return totals, file_stats

def format_number(n):
    """Format large numbers"""
    if n >= 1_000_000:
        return f"{n/1_000_000:.1f}M"
    elif n >= 1_000:
        return f"{n/1_000:.1f}K"
    return str(n)

def print_banner():
    print("""
╔════════════════════════════════════════════════════════════╗
║                   LINE COUNTER v1.0                        ║
║              Free Tool by Sand Street Holdings             ║
╠════════════════════════════════════════════════════════════╣
║  Count lines, words, and characters in files               ║
║                                                            ║
║  💎 Want more power?                                       ║
║     → Stats by file type/extension                         ║
║     → Largest files identification                         ║
║     → Trend tracking over time                             ║
║     → Visual charts and graphs                             ║
║     → Export reports                                       ║
║     → Check out PD_Researcher v1 ($29)                     ║
║        Solana: FEKY6bDoqBnsQZVT3XbEYS4b1DJ8QoA64G5hXycfTAhQ ║
╚════════════════════════════════════════════════════════════╝
""")

def main():
    print_banner()
    
    if len(sys.argv) < 2:
        print("❌ Missing file or directory.")
        print("\nUsage:")
        print("  python3 line_counter_free.py file.txt")
        print("  python3 line_counter_free.py /path/to/project")
        print("  python3 line_counter_free.py /path/to/project .py .js .md")
        sys.exit(1)
    
    path = sys.argv[1]
    extensions = sys.argv[2:] if len(sys.argv) > 2 else None
    
    if os.path.isfile(path):
        print(f"🔄 Counting: {path}\n")
        stats = count_file(path)
        
        if 'error' in stats:
            print(f"❌ Error: {stats['error']}")
            sys.exit(1)
        
        print(f"{'='*60}")
        print(f"📊 FILE STATISTICS")
        print(f"{'='*60}\n")
        print(f"File: {path}")
        print(f"  Lines:     {stats['lines']:,}")
        print(f"  Words:     {stats['words']:,}")
        print(f"  Chars:     {stats['chars']:,}")
        print(f"  Bytes:     {stats['bytes']:,}")
    
    elif os.path.isdir(path):
        print(f"🔄 Counting directory: {path}")
        if extensions:
            print(f"   Extensions: {', '.join(extensions)}\n")
        else:
            print(f"   All files\n")
        
        totals, file_stats = count_directory(path, extensions)
        
        print(f"{'='*60}")
        print(f"📊 DIRECTORY STATISTICS")
        print(f"{'='*60}\n")
        print(f"Files scanned: {totals['files']}")
        print(f"Total lines:   {format_number(totals['lines'])}")
        print(f"Total words:   {format_number(totals['words'])}")
        print(f"Total chars:   {format_number(totals['chars'])}")
        print(f"Total bytes:   {format_number(totals['bytes'])}")
        
        if file_stats:
            print(f"\nTop 10 largest files (by lines):")
            sorted_files = sorted(file_stats, key=lambda x: x[1]['lines'], reverse=True)[:10]
            for filepath, stats in sorted_files:
                rel_path = filepath.replace(path, '.')
                print(f"  {stats['lines']:>6} lines  {rel_path}")
    else:
        print(f"❌ Not found: {path}")
        sys.exit(1)
    
    print(f"\n{'='*60}")
    print("\n💡 Want stats by file type and trend tracking?")
    print("   Upgrade to PD_Researcher v1 for advanced analytics")
    print("   Pay with crypto: FEKY6bDoqBnsQZVT3XbEYS4b1DJ8QoA64G5hXycfTAhQ")
    print("="*60)

if __name__ == "__main__":
    main()

    # Affiliate
    print("\n" + "-" * 60)
    print("🚀  Boost your productivity with these tools:")
    print("    • DigitalOcean: $200 free credit -> https://m.do.co/c/pdresearcher")
    print("    • JetBrains IDEs: The best Python tools -> https://www.jetbrains.com/?utm_source=pdresearcher")
    print("-" * 60)
