#!/usr/bin/env python3
"""
Duplicate File Finder - Free Tool
Find duplicate files in a directory by comparing hashes
Free version: Single directory, MD5 hash
Paid upgrade: Multiple directories, different hash algorithms, auto-delete, reporting

Usage: python3 duplicate_finder_free.py <directory>
"""

import sys
import os
import hashlib
from collections import defaultdict

def hash_file(filepath, block_size=65536):
    """Hash a file using MD5"""
    hasher = hashlib.md5()
    try:
        with open(filepath, 'rb') as f:
            while chunk := f.read(block_size):
                hasher.update(chunk)
        return hasher.hexdigest()
    except Exception as e:
        return None

def scan_directory(directory):
    """Scan directory and return file hashes"""
    files_by_hash = defaultdict(list)
    
    for root, dirs, files in os.walk(directory):
        for filename in files:
            filepath = os.path.join(root, filename)
            try:
                file_hash = hash_file(filepath)
                if file_hash:
                    files_by_hash[file_hash].append(filepath)
            except Exception as e:
                print(f"⚠️  Error hashing {filepath}: {e}")
    
    return files_by_hash

def find_duplicates(files_by_hash):
    """Find files with duplicate hashes"""
    return {h: files for h, files in files_by_hash.items() if len(files) > 1}

def format_size(size_bytes):
    """Format file size"""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.2f} TB"

def print_banner():
    print("""
╔════════════════════════════════════════════════════════════╗
║                DUPLICATE FILE FINDER v1.0                  ║
║              Free Tool by Sand Street Holdings             ║
╠════════════════════════════════════════════════════════════╣
║  Find duplicate files by comparing MD5 hashes              ║
║                                                            ║
║  💎 Want more power?                                       ║
║     → SHA256 hash verification                             ║
║     → Multiple directory comparison                        ║
║     → Auto-delete duplicates (keep first)                  ║
║     → Export reports (CSV, JSON)                           ║
║     → Preview images before deletion                       ║
║     → Check out PD_Researcher v1 ($29)                     ║
║        Solana: FEKY6bDoqBnsQZVT3XbEYS4b1DJ8QoA64G5hXycfTAhQ ║
╚════════════════════════════════════════════════════════════╝
""")

def main():
    print_banner()
    
    if len(sys.argv) < 2:
        print("❌ No directory provided.")
        print("\nUsage:")
        print("  python3 duplicate_finder_free.py /path/to/directory")
        sys.exit(1)
    
    directory = sys.argv[1]
    
    if not os.path.isdir(directory):
        print(f"❌ Not a directory: {directory}")
        sys.exit(1)
    
    print(f"🔄 Scanning: {directory}\n")
    
    files_by_hash = scan_directory(directory)
    duplicates = find_duplicates(files_by_hash)
    
    print(f"{'='*60}")
    print(f"📊 SCAN RESULTS")
    print(f"{'='*60}")
    print(f"Total files scanned: {sum(len(files) for files in files_by_hash.values())}")
    print(f"Unique files: {len(files_by_hash)}")
    print(f"Duplicate groups: {len(duplicates)}")
    
    if duplicates:
        total_wasted = 0
        print(f"\n🔴 DUPLICATES FOUND:\n")
        
        for file_hash, files in sorted(duplicates.items(), key=lambda x: len(x[1]), reverse=True):
            print(f"Hash: {file_hash[:16]}...")
            
            # Get size of first file (all should be same size)
            try:
                size = os.path.getsize(files[0])
                total_wasted += size * (len(files) - 1)
                print(f"Size: {format_size(size)}")
            except:
                print(f"Size: Unknown")
            
            print(f"Copies: {len(files)}")
            print("Files:")
            for i, filepath in enumerate(files, 1):
                print(f"  {i}. {filepath}")
            print()
        
        print(f"{'='*60}")
        print(f"💾 WASTED SPACE: {format_size(total_wasted)}")
        print(f"{'='*60}")
    else:
        print("\n✅ No duplicates found!")
    
    print(f"\n{'='*60}")
    print("\n💡 Want auto-delete and detailed reports?")
    print("   Upgrade to PD_Researcher v1 for advanced duplicate management")
    print("   Pay with crypto: FEKY6bDoqBnsQZVT3XbEYS4b1DJ8QoA64G5hXycfTAhQ")
    print("="*60)

if __name__ == "__main__":
    main()
