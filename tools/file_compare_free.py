#!/usr/bin/env python3
"""
file_compare_free.py - File Comparison Tool
Compare two files and show differences, similarity score, and stats.
Zero dependencies. Pure Python 3.
"""

import sys
import os
import hashlib

def read_file_lines(filepath: str) -> list:
    """Read file as list of lines."""
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            return f.read().splitlines()
    except Exception as e:
        print(f"Error reading {filepath}: {e}")
        return []

def read_file_bytes(filepath: str) -> bytes:
    """Read file as bytes."""
    try:
        with open(filepath, 'rb') as f:
            return f.read()
    except Exception as e:
        print(f"Error reading {filepath}: {e}")
        return b''

def file_hash(filepath: str) -> str:
    """Calculate MD5 hash of file."""
    data = read_file_bytes(filepath)
    return hashlib.md5(data).hexdigest() if data else ''

def similarity_score(lines1: list, lines2: list) -> float:
    """Calculate similarity percentage between two lists."""
    if not lines1 and not lines2:
        return 100.0
    if not lines1 or not lines2:
        return 0.0
    
    set1 = set(lines1)
    set2 = set(lines2)
    
    intersection = len(set1 & set2)
    union = len(set1 | set2)
    
    return (intersection / union) * 100 if union > 0 else 0.0

def find_differences(lines1: list, lines2: list, context: int = 2):
    """Find line-by-line differences."""
    import difflib
    
    diff = list(difflib.unified_diff(
        lines1, lines2,
        lineterm='',
        n=context
    ))
    
    return diff

def compare_files(file1: str, file2: str):
    """Compare two files comprehensively."""
    print(f"📊 File Comparison")
    print("=" * 60)
    print(f"\nFile 1: {file1}")
    print(f"File 2: {file2}")
    
    # Check existence
    if not os.path.exists(file1):
        print(f"\n❌ Error: File not found: {file1}")
        return
    if not os.path.exists(file2):
        print(f"\n❌ Error: File not found: {file2}")
        return
    
    # Basic stats
    size1 = os.path.getsize(file1)
    size2 = os.path.getsize(file2)
    hash1 = file_hash(file1)
    hash2 = file_hash(file2)
    
    print(f"\n📏 Size:")
    print(f"  File 1: {size1:,} bytes")
    print(f"  File 2: {size2:,} bytes")
    if size1 == size2:
        print(f"  ✅ Same size")
    else:
        diff = abs(size2 - size1)
        pct = (diff / max(size1, size2)) * 100
        print(f"  Difference: {diff:,} bytes ({pct:.1f}%)")
    
    print(f"\n🔐 MD5 Hash:")
    print(f"  File 1: {hash1}")
    print(f"  File 2: {hash2}")
    if hash1 == hash2:
        print(f"  ✅ Files are identical")
        return
    else:
        print(f"  ❌ Files are different")
    
    # Line-based comparison (for text files)
    lines1 = read_file_lines(file1)
    lines2 = read_file_lines(file2)
    
    if lines1 and lines2:
        print(f"\n📝 Line Count:")
        print(f"  File 1: {len(lines1)} lines")
        print(f"  File 2: {len(lines2)} lines")
        
        # Similarity
        sim = similarity_score(lines1, lines2)
        print(f"\n🎯 Similarity: {sim:.1f}%")
        
        if sim > 90:
            print(f"  ✅ Nearly identical")
        elif sim > 70:
            print(f"  🟡 Substantial similarity")
        elif sim > 30:
            print(f"  🟠 Partial similarity")
        else:
            print(f"  🔴 Very different")
        
        # Common lines
        common = set(lines1) & set(lines2)
        only_1 = set(lines1) - set(lines2)
        only_2 = set(lines2) - set(lines1)
        
        print(f"\n📋 Line Analysis:")
        print(f"  Common lines: {len(common)}")
        print(f"  Only in File 1: {len(only_1)}")
        print(f"  Only in File 2: {len(only_2)}")
        
        # Show first few differences
        if only_1 and len(only_1) <= 5:
            print(f"\n  Lines only in File 1:")
            for line in list(only_1)[:3]:
                display = line[:60] + "..." if len(line) > 60 else line
                print(f"    - {display}")
    
    print("\n" + "=" * 60)

def main():
    if len(sys.argv) < 3:
        print("Usage: file_compare_free.py <file1> <file2>")
        print("\nCompares two files and shows:")
        print("  • Size and hash comparison")
        print("  • Line count and similarity score")
        print("  • Unique lines in each file")
        print("\nExamples:")
        print('  file_compare_free.py file1.txt file2.txt')
        print('  file_compare_free.py config.ini config.ini.backup')
        sys.exit(1)
    
    file1 = sys.argv[1]
    file2 = sys.argv[2]
    
    compare_files(file1, file2)

if __name__ == "__main__":
    main()
