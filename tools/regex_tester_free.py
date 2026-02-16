#!/usr/bin/env python3
"""
Regex Tester - Free Tool
Test regular expressions against text
Free version: Basic matching with groups
Paid upgrade: Replace, split, named groups, regex library

Usage: python3 regex_tester_free.py <pattern> <text>
"""

import sys
import re

def test_regex(pattern, text, flags=0):
    """Test regex pattern against text"""
    try:
        compiled = re.compile(pattern, flags)
    except re.error as e:
        return {'error': f'Invalid regex: {e}'}
    
    matches = list(compiled.finditer(text))
    
    return {
        'pattern': pattern,
        'text': text,
        'match_count': len(matches),
        'matches': matches
    }

def print_banner():
    print("""
╔════════════════════════════════════════════════════════════╗
║                   REGEX TESTER v1.0                        ║
║              Free Tool by Sand Street Holdings             ║
╠════════════════════════════════════════════════════════════╣
║  Test regular expressions with match highlighting          ║
║                                                            ║
║  💎 Want more power?                                       ║
║     → Replace and split operations                         ║
║     → Named capture groups                                 ║
║     → Regex library (save common patterns)                 ║
║     → Performance benchmarking                             ║
║     → Multi-line and verbose mode                          ║
║     → Check out PD_Researcher v1 ($29)                     ║
║        Solana: FEKY6bDoqBnsQZVT3XbEYS4b1DJ8QoA64G5hXycfTAhQ ║
╚════════════════════════════════════════════════════════════╝
""")

def main():
    print_banner()
    
    if len(sys.argv) < 3:
        print("❌ Missing pattern or text.")
        print("\nUsage:")
        print('  python3 regex_tester_free.py "[a-z]+" "Hello World 123"')
        print('  python3 regex_tester_free.py "\\d{3}-\\d{4}" "Call 555-1234"')
        sys.exit(1)
    
    pattern = sys.argv[1]
    text = sys.argv[2]
    
    print(f"🔄 Testing pattern: {pattern}")
    print(f"   Against text: {text[:50]}{'...' if len(text) > 50 else ''}\n")
    
    result = test_regex(pattern, text)
    
    if 'error' in result:
        print(f"❌ {result['error']}")
        sys.exit(1)
    
    print(f"{'='*60}")
    print(f"📊 REGEX RESULTS")
    print(f"{'='*60}\n")
    
    print(f"Pattern: {result['pattern']}")
    print(f"Matches found: {result['match_count']}")
    
    if result['matches']:
        print(f"\nMatch details:")
        for i, match in enumerate(result['matches'], 1):
            print(f"\n  Match {i}:")
            print(f"    Full match: '{match.group()}'")
            print(f"    Position: {match.start()}-{match.end()}")
            
            if match.groups():
                print(f"    Groups:")
                for j, group in enumerate(match.groups(), 1):
                    print(f"      Group {j}: '{group}'")
        
        # Highlight matches in text
        print(f"\nHighlighted:")
        highlighted = text
        for match in reversed(result['matches']):
            start, end = match.start(), match.end()
            highlighted = highlighted[:start] + f'\033[7m{highlighted[start:end]}\033[0m' + highlighted[end:]
        print(f"  {highlighted}")
    else:
        print("\n❌ No matches found")
    
    print(f"\n{'='*60}")
    print("\n💡 Want replace/split and regex library?")
    print("   Upgrade to PD_Researcher v1 for advanced regex tools")
    print("   Pay with crypto: FEKY6bDoqBnsQZVT3XbEYS4b1DJ8QoA64G5hXycfTAhQ")
    print("="*60)

if __name__ == "__main__":
    main()
