#!/usr/bin/env python3
"""
Diff Tool - Free Tool
Compare two files and show differences
Free version: Line-by-line diff
Paid upgrade: Word/character diff, merge tools, directory comparison

Usage: python3 diff_tool_free.py <file1> <file2>
"""

import sys

def read_file(filepath):
    """Read file lines"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.readlines()
    except Exception as e:
        print(f"❌ Error reading {filepath}: {e}")
        return None

def diff_lines(lines1, lines2):
    """Simple line diff"""
    diff = []
    max_len = max(len(lines1), len(lines2))
    
    for i in range(max_len):
        line1 = lines1[i] if i < len(lines1) else None
        line2 = lines2[i] if i < len(lines2) else None
        
        if line1 is None:
            diff.append(('+', i+1, line2.rstrip()))
        elif line2 is None:
            diff.append(('-', i+1, line1.rstrip()))
        elif line1 != line2:
            diff.append(('!', i+1, line1.rstrip(), line2.rstrip()))
    
    return diff

def print_banner():
    print("""
╔════════════════════════════════════════════════════════════╗
║                     DIFF TOOL v1.0                         ║
║              Free Tool by Sand Street Holdings             ║
╠════════════════════════════════════════════════════════════╣
║  Compare two files and show line-by-line differences       ║
║                                                            ║
║  💎 Want more power?                                       ║
║     → Word-level and character-level diff                  ║
║     → Side-by-side comparison                              ║
║     → Directory comparison                                 ║
║     → Patch file generation                                ║
║     → 3-way merge tools                                    ║
║     → Check out PD_Researcher v1 ($29)                     ║
║        Solana: FEKY6bDoqBnsQZVT3XbEYS4b1DJ8QoA64G5hXycfTAhQ ║
╚════════════════════════════════════════════════════════════╝
""")

def main():
    print_banner()
    
    if len(sys.argv) < 3:
        print("❌ Missing files to compare.")
        print("\nUsage:")
        print("  python3 diff_tool_free.py file1.txt file2.txt")
        sys.exit(1)
    
    file1 = sys.argv[1]
    file2 = sys.argv[2]
    
    lines1 = read_file(file1)
    lines2 = read_file(file2)
    
    if lines1 is None or lines2 is None:
        sys.exit(1)
    
    print(f"🔄 Comparing:")
    print(f"   A: {file1} ({len(lines1)} lines)")
    print(f"   B: {file2} ({len(lines2)} lines)\n")
    
    diff = diff_lines(lines1, lines2)
    
    print(f"{'='*60}")
    print(f"📊 DIFF RESULTS")
    print(f"{'='*60}\n")
    
    if not diff:
        print("✅ Files are identical!")
    else:
        changes = len(diff)
        print(f"Found {changes} difference(s):\n")
        
        for item in diff:
            if item[0] == '+':
                print(f"  \033[32m+ Line {item[1]}: {item[2]}\033[0m")
            elif item[0] == '-':
                print(f"  \033[31m- Line {item[1]}: {item[2]}\033[0m")
            elif item[0] == '!':
                print(f"  \033[33m! Line {item[1]} changed:\033[0m")
                print(f"    < {item[2]}")
                print(f"    > {item[3]}")
    
    print(f"\n{'='*60}")
    print("\n💡 Want side-by-side and word-level diff?")
    print("   Upgrade to PD_Researcher v1 for advanced comparison tools")
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
