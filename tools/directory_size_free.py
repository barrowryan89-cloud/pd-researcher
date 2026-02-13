#!/usr/bin/env python3
"""
Directory Size - Free Tool
Calculate directory sizes and find largest directories
Free version: Single directory tree
Paid upgrade: Multiple directories, sorting, export, visualization

Usage: python3 directory_size_free.py <directory> [depth]
"""

import sys
import os
from collections import defaultdict

def get_dir_size(path):
    """Get total size of directory"""
    total = 0
    try:
        for entry in os.scandir(path):
            if entry.is_file(follow_symlinks=False):
                total += entry.stat().st_size
            elif entry.is_dir(follow_symlinks=False):
                total += get_dir_size(entry.path)
    except (PermissionError, OSError):
        pass
    return total

def scan_directory(path, depth=0, max_depth=1):
    """Scan directory and return sizes"""
    sizes = []
    
    try:
        for entry in os.scandir(path):
            if entry.is_dir(follow_symlinks=False):
                size = get_dir_size(entry.path)
                sizes.append((entry.path, size))
                
                if depth < max_depth:
                    sub_sizes = scan_directory(entry.path, depth + 1, max_depth)
                    sizes.extend(sub_sizes)
    except (PermissionError, OSError):
        pass
    
    return sizes

def format_size(size_bytes):
    """Format file size"""
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if abs(size_bytes) < 1024.0:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.2f} PB"

def print_banner():
    print("""
╔════════════════════════════════════════════════════════════╗
║                   DIRECTORY SIZE v1.0                      ║
║              Free Tool by Sand Street Holdings             ║
╠════════════════════════════════════════════════════════════╣
║  Calculate directory sizes and find disk space usage       ║
║                                                            ║
║  💎 Want more power?                                       ║
║     → Sort by size (largest first)                         ║
║     → Export to CSV/JSON                                   ║
║     → Visual tree view                                     ║
║     → Find largest files within directories                ║
║     → Historical tracking                                  ║
║     → Check out PD_Researcher v1 ($29)                     ║
║        Solana: FEKY6bDoqBnsQZVT3XbEYS4b1DJ8QoA64G5hXycfTAhQ ║
╚════════════════════════════════════════════════════════════╝
""")

def main():
    print_banner()
    
    if len(sys.argv) < 2:
        print("❌ No directory provided.")
        print("\nUsage:")
        print("  python3 directory_size_free.py /path/to/directory")
        print("  python3 directory_size_free.py /path 2")
        sys.exit(1)
    
    directory = sys.argv[1]
    max_depth = int(sys.argv[2]) if len(sys.argv) > 2 else 1
    
    if not os.path.isdir(directory):
        print(f"❌ Not a directory: {directory}")
        sys.exit(1)
    
    print(f"🔄 Scanning: {directory}")
    print(f"Depth: {max_depth} level(s)\n")
    
    total_size = get_dir_size(directory)
    sizes = scan_directory(directory, max_depth=max_depth)
    
    print(f"{'='*60}")
    print(f"📊 DIRECTORY SIZE REPORT")
    print(f"{'='*60}")
    print(f"\nTotal size: {format_size(total_size)}\n")
    
    if sizes:
        print(f"Subdirectories ({len(sizes)} found):\n")
        for path, size in sizes[:20]:  # Show top 20
            # Shorten path for display
            display_path = path.replace(directory, '.')
            print(f"{format_size(size):>12}  {display_path}")
        
        if len(sizes) > 20:
            print(f"\n... and {len(sizes) - 20} more directories")
    
    print(f"\n{'='*60}")
    print("\n💡 Want sorting and detailed reports?")
    print("   Upgrade to PD_Researcher v1 for advanced disk analysis")
    print("   Pay with crypto: FEKY6bDoqBnsQZVT3XbEYS4b1DJ8QoA64G5hXycfTAhQ")
    print(f"\n☁️  Need more storage? Get $200 credit at DigitalOcean:")
    print("   https://m.do.co/c/pdresearcher [affiliate]")
    print("="*60)

if __name__ == "__main__":
    main()
