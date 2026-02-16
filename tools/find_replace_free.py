#!/usr/bin/env python3
"""
Find Replace - Free Tool
Find and replace text in files
Free version: Single file, basic replacement
Paid upgrade: Regex, multiple files, preview, dry-run

Usage: python3 find_replace_free.py <file> <find> <replace>
"""

import sys
import re

def find_replace(filepath, find_text, replace_text, use_regex=False):
    """Find and replace in file"""
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        
        original = content
        
        if use_regex:
            new_content = re.sub(find_text, replace_text, content)
        else:
            new_content = content.replace(find_text, replace_text)
        
        changes = original.count(find_text) if not use_regex else len(re.findall(find_text, original))
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        return {
            'changes': changes,
            'original_length': len(original),
            'new_length': len(new_content)
        }
    except Exception as e:
        return {'error': str(e)}

def print_banner():
    print("""
╔════════════════════════════════════════════════════════════╗
║                  FIND REPLACE v1.0                         ║
║              Free Tool by Sand Street Holdings             ║
╠════════════════════════════════════════════════════════════╣
║  Find and replace text in files                            ║
║                                                            ║
║  💎 Want more power?                                       ║
║     → Regex pattern matching                               ║
║     → Multiple file processing                             ║
║     → Preview changes before applying                      ║
║     → Dry-run mode                                         ║
║     → Backup creation                                      ║
║     → Check out PD_Researcher v1 ($29)                     ║
║        Solana: FEKY6bDoqBnsQZVT3XbEYS4b1DJ8QoA64G5hXycfTAhQ ║
╚════════════════════════════════════════════════════════════╝
""")

def main():
    print_banner()
    
    if len(sys.argv) < 4:
        print("❌ Missing arguments.")
        print("\nUsage:")
        print('  python3 find_replace_free.py file.txt "old" "new"')
        print('  python3 find_replace_free.py file.txt "old" "new" --regex')
        sys.exit(1)
    
    filepath = sys.argv[1]
    find_text = sys.argv[2]
    replace_text = sys.argv[3]
    use_regex = '--regex' in sys.argv
    
    print(f"🔄 Processing: {filepath}")
    print(f"   Find: {find_text}")
    print(f"   Replace: {replace_text}")
    if use_regex:
        print(f"   Mode: Regex")
    print()
    
    result = find_replace(filepath, find_text, replace_text, use_regex)
    
    if 'error' in result:
        print(f"❌ Error: {result['error']}")
        sys.exit(1)
    
    print(f"{'='*60}")
    print(f"📊 REPLACE COMPLETE")
    print(f"{'='*60}\n")
    
    print(f"Changes made: {result['changes']}")
    print(f"Original size: {result['original_length']:,} chars")
    print(f"New size: {result['new_length']:,} chars")
    
    if result['changes'] == 0:
        print("\n⚠️  No matches found")
    else:
        print(f"\n✅ File updated successfully")
    
    print(f"\n{'='*60}")
    print("\n💡 Want regex and multi-file processing?")
    print("   Upgrade to PD_Researcher v1 for advanced find/replace")
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
