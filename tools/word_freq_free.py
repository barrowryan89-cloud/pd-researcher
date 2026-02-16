#!/usr/bin/env python3
"""
Word Frequency - Free Tool
Count word frequency in text files
Free version: Basic word counting
Paid upgrade: N-grams, stop words, stemming, visualization

Usage: python3 word_freq_free.py <file> [top_n]
"""

import sys
import re
from collections import Counter

def count_words(filepath, top_n=20):
    """Count word frequency"""
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            text = f.read().lower()
        
        # Extract words
        words = re.findall(r'\b[a-z]+\b', text)
        
        # Simple stop words
        stop_words = {'the', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'a', 'an', 'is', 'are', 'was', 'were', 'be', 'been', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could', 'should'}
        
        # Filter stop words
        filtered_words = [w for w in words if w not in stop_words and len(w) > 2]
        
        return Counter(filtered_words).most_common(top_n)
    except Exception as e:
        return {'error': str(e)}

def print_banner():
    print("""
╔════════════════════════════════════════════════════════════╗
║                 WORD FREQUENCY v1.0                        ║
║              Free Tool by Sand Street Holdings             ║
╠════════════════════════════════════════════════════════════╣
║  Analyze word frequency in text files                      ║
║                                                            ║
║  💎 Want more power?                                       ║
║     → N-gram analysis (2-word, 3-word phrases)             ║
║     → Custom stop word lists                               ║
║     → Stemming and lemmatization                           ║
║     → TF-IDF scoring                                       ║
║     → Visual word clouds                                   ║
║     → Check out PD_Researcher v1 ($29)                     ║
║        Solana: FEKY6bDoqBnsQZVT3XbEYS4b1DJ8QoA64G5hXycfTAhQ ║
╚════════════════════════════════════════════════════════════╝
""")

def main():
    print_banner()
    
    if len(sys.argv) < 2:
        print("❌ Missing file.")
        print("\nUsage:")
        print("  python3 word_freq_free.py article.txt")
        print("  python3 word_freq_free.py article.txt 30")
        sys.exit(1)
    
    filepath = sys.argv[1]
    top_n = int(sys.argv[2]) if len(sys.argv) > 2 else 20
    
    print(f"🔄 Analyzing: {filepath}")
    print(f"   Top {top_n} words\n")
    
    result = count_words(filepath, top_n)
    
    if isinstance(result, dict) and 'error' in result:
        print(f"❌ Error: {result['error']}")
        sys.exit(1)
    
    print(f"{'='*60}")
    print(f"📊 WORD FREQUENCY")
    print(f"{'='*60}\n")
    
    print(f"{'Rank':<6} {'Word':<20} {'Count':<10} {'Bar'}")
    print("-" * 60)
    
    max_count = result[0][1] if result else 1
    
    for i, (word, count) in enumerate(result, 1):
        bar_len = int((count / max_count) * 20)
        bar = '█' * bar_len
        print(f"{i:<6} {word:<20} {count:<10} {bar}")
    
    print(f"\n{'='*60}")
    print("\n💡 Want N-grams and word clouds?")
    print("   Upgrade to PD_Researcher v1 for advanced text analysis")
    print("   Pay with crypto: FEKY6bDoqBnsQZVT3XbEYS4b1DJ8QoA64G5hXycfTAhQ")
    print("="*60)

if __name__ == "__main__":
    main()
