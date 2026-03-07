#!/usr/bin/env python3
"""
Text Summarizer - Free Tool
Summarizes long text using extractive summarization
Free version: Single text input
Paid upgrade: API access, different models, batch processing

Usage: python3 text_summarizer_free.py <text_file> or pipe text to it
"""

import sys
import re
from collections import Counter
import math

def read_input():
    """Read text from file or stdin"""
    if len(sys.argv) > 1:
        with open(sys.argv[1], 'r', encoding='utf-8') as f:
            return f.read()
    else:
        print("Reading from stdin (paste text, then Ctrl+D)...", file=sys.stderr)
        return sys.stdin.read()

def tokenize_sentences(text):
    """Simple sentence tokenization"""
    # Split on sentence boundaries
    sentences = re.split(r'(?<=[.!?])\s+', text)
    return [s.strip() for s in sentences if len(s.strip()) > 10]

def tokenize_words(text):
    """Simple word tokenization"""
    words = re.findall(r'\b[a-zA-Z]+\b', text.lower())
    return [w for w in words if len(w) > 2]

def score_sentences(sentences, word_freq):
    """Score sentences based on word frequency"""
    scores = []
    for sentence in sentences:
        words = tokenize_words(sentence)
        if not words:
            scores.append(0)
            continue
        # Score is average word frequency
        score = sum(word_freq.get(word, 0) for word in words) / len(words)
        scores.append(score)
    return scores

def summarize(text, ratio=0.2):
    """Extractive summarization"""
    sentences = tokenize_sentences(text)
    
    if len(sentences) < 3:
        return text
    
    # Get word frequencies
    words = tokenize_words(text)
    word_freq = Counter(words)
    
    # Normalize frequencies
    max_freq = max(word_freq.values())
    word_freq = {word: freq/max_freq for word, freq in word_freq.items()}
    
    # Score sentences
    scores = score_sentences(sentences, word_freq)
    
    # Get top sentences
    num_sentences = max(1, int(len(sentences) * ratio))
    ranked = sorted(enumerate(scores), key=lambda x: x[1], reverse=True)
    top_indices = sorted([idx for idx, _ in ranked[:num_sentences]])
    
    # Return in original order
    summary = ' '.join(sentences[i] for i in top_indices)
    return summary

def print_stats(original, summary):
    """Print compression stats"""
    orig_words = len(original.split())
    sum_words = len(summary.split())
    compression = ((orig_words - sum_words) / orig_words) * 100 if orig_words > 0 else 0
    
    print(f"\n{'='*60}")
    print(f"📊 SUMMARY STATS")
    print(f"{'='*60}")
    print(f"Original: {orig_words} words")
    print(f"Summary:  {sum_words} words")
    print(f"Compression: {compression:.1f}%")
    print(f"{'='*60}")

def print_banner():
    print("""
╔════════════════════════════════════════════════════════════╗
║                  TEXT SUMMARIZER v1.0                      ║
║              Free Tool by Sand Street Holdings             ║
╠════════════════════════════════════════════════════════════╣
║  Summarize long articles, reports, documents instantly     ║
║                                                            ║
║  💎 Want more power?                                       ║
║     → Multiple summary lengths                             ║
║     → API access                                           ║
║     → Different algorithms (abstractive, GPT-based)        ║
║     → Batch file processing                                ║
║     → Check out PD_Researcher v1 ($29)                     ║
║        Solana: FEKY6bDoqBnsQZVT3XbEYS4b1DJ8QoA64G5hXycfTAhQ ║
╚════════════════════════════════════════════════════════════╝
""")

def main():
    print_banner()
    
    text = read_input()
    
    if not text.strip():
        print("❌ No text provided.")
        print("\nUsage:")
        print("  python3 text_summarizer_free.py article.txt")
        print("  cat article.txt | python3 text_summarizer_free.py")
        sys.exit(1)
    
    print("🔄 Summarizing...\n")
    
    summary = summarize(text, ratio=0.2)
    
    print(summary)
    
    print_stats(text, summary)
    
    print("\n💡 Want adjustable summary length or different algorithms?")
    print("   Upgrade to PD_Researcher v1 for advanced summarization")
    print("   Pay with crypto: FEKY6bDoqBnsQZVT3XbEYS4b1DJ8QoA64G5hXycfTAhQ")
    print("="*60)

if __name__ == "__main__":
    main()
