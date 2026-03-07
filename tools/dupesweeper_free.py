#!/usr/bin/env python3
"""
Dupesweeper - Find and manage duplicate files
Quickly scan directories for duplicate files by hash or content similarity.

Usage: python3 dupesweeper_free.py [options] <directory>
"""

import os
import sys
import hashlib
import argparse
from collections import defaultdict
from pathlib import Path


def get_file_hash(filepath, algorithm='md5', chunk_size=8192):
    """Calculate file hash."""
    hasher = hashlib.new(algorithm)
    try:
        with open(filepath, 'rb') as f:
            while chunk := f.read(chunk_size):
                hasher.update(chunk)
        return hasher.hexdigest()
    except (IOError, OSError):
        return None


def scan_directory(directory, recursive=True, exclude_patterns=None, min_size=1):
    """Scan directory and return file paths grouped by size first."""
    directory = Path(directory).expanduser().resolve()
    exclude_patterns = exclude_patterns or []
    
    files_by_size = defaultdict(list)
    
    if recursive:
        pattern = '**/*'
    else:
        pattern = '*'
    
    for filepath in directory.glob(pattern):
        if not filepath.is_file():
            continue
            
        # Check exclusions
        skip = False
        for pattern in exclude_patterns:
            if pattern in str(filepath):
                skip = True
                break
        if skip:
            continue
        
        try:
            size = filepath.stat().st_size
            if size >= min_size:
                files_by_size[size].append(filepath)
        except (IOError, OSError):
            continue
    
    return files_by_size


def find_duplicates(directory, recursive=True, algorithm='md5', 
                   exclude_patterns=None, min_size=1):
    """Find duplicate files in directory."""
    files_by_size = scan_directory(directory, recursive, exclude_patterns, min_size)
    
    # Only check files with same size (potential duplicates)
    duplicates = defaultdict(list)
    total_checked = 0
    
    for size, files in files_by_size.items():
        if len(files) < 2:
            continue
        
        # Group by hash
        hashes = defaultdict(list)
        for filepath in files:
            file_hash = get_file_hash(filepath, algorithm)
            total_checked += 1
            if file_hash:
                hashes[file_hash].append(filepath)
        
        # Add to duplicates if hash matches
        for file_hash, paths in hashes.items():
            if len(paths) > 1:
                duplicates[file_hash].extend(paths)
    
    return duplicates, total_checked


def format_size(size_bytes):
    """Format byte size to human readable."""
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.1f} PB"


def get_wasted_space(duplicates):
    """Calculate total wasted space from duplicates."""
    total = 0
    for paths in duplicates.values():
        if len(paths) > 1:
            try:
                size = paths[0].stat().st_size
                total += size * (len(paths) - 1)
            except (IOError, OSError):
                continue
    return total


def print_results(duplicates, algorithm):
    """Print duplicate findings."""
    if not duplicates:
        print("\n✅ No duplicates found!")
        return
    
    print(f"\n{'='*60}")
    print(f"🔍 DUPLICATE FILES FOUND ({len(duplicates)} groups)")
    print(f"{'='*60}")
    
    for i, (file_hash, paths) in enumerate(duplicates.items(), 1):
        try:
            size = paths[0].stat().st_size
            size_str = format_size(size)
        except (IOError, OSError):
            size_str = "Unknown"
        
        print(f"\n📁 Group {i} — {len(paths)} copies — {size_str} each")
        print(f"   Hash ({algorithm}): {file_hash[:16]}...")
        
        for j, path in enumerate(paths, 1):
            marker = "  📌" if j == 1 else "    "
            print(f"{marker} {j}. {path}")
    
    wasted = get_wasted_space(duplicates)
    print(f"\n{'='*60}")
    print(f"💾 Wasted Space: {format_size(wasted)}")
    print(f"{'='*60}")


def generate_delete_script(duplicates, output_file='delete_duplicates.sh'):
    """Generate a script to delete duplicate files (keeps first copy)."""
    with open(output_file, 'w') as f:
        f.write("#!/bin/bash\n")
        f.write("# Auto-generated script to remove duplicate files\n")
        f.write("# Keeping the first copy of each duplicate group\n\n")
        
        for file_hash, paths in duplicates.items():
            if len(paths) > 1:
                for path in paths[1:]:  # Skip first (keep it)
                    f.write(f'rm -f "{path}"\n')
        
        f.write("\necho 'Duplicate removal complete'\n")
    
    os.chmod(output_file, 0o755)
    return output_file


def main():
    parser = argparse.ArgumentParser(
        description='Dupesweeper — Find and manage duplicate files',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 dupesweeper_free.py ~/Downloads
  python3 dupesweeper_free.py --min-size 1MB ~/Documents
  python3 dupesweeper_free.py --no-recursive --exclude "node_modules" .
  python3 dupesweeper_free.py --script ~/Photos
        """
    )
    
    parser.add_argument('directory', help='Directory to scan')
    parser.add_argument('-r', '--no-recursive', action='store_true',
                       help='Don\'t scan subdirectories')
    parser.add_argument('-a', '--algorithm', default='md5',
                       choices=['md5', 'sha1', 'sha256'],
                       help='Hash algorithm (default: md5)')
    parser.add_argument('-m', '--min-size', default='1',
                       help='Minimum file size (e.g., 1KB, 1MB, default: 1 byte)')
    parser.add_argument('-e', '--exclude', action='append', default=[],
                       help='Exclude paths containing this pattern (can use multiple)')
    parser.add_argument('-s', '--script', action='store_true',
                       help='Generate delete script (keeps first copy)')
    parser.add_argument('-q', '--quiet', action='store_true',
                       help='Quiet mode (errors only)')
    
    args = parser.parse_args()
    
    # Parse min size
    min_size_str = args.min_size.upper()
    min_size = 1
    if min_size_str.endswith('KB'):
        min_size = int(min_size_str[:-2]) * 1024
    elif min_size_str.endswith('MB'):
        min_size = int(min_size_str[:-2]) * 1024 * 1024
    elif min_size_str.endswith('GB'):
        min_size = int(min_size_str[:-2]) * 1024 * 1024 * 1024
    else:
        try:
            min_size = int(args.min_size)
        except ValueError:
            print(f"Error: Invalid min-size format: {args.min_size}")
            sys.exit(1)
    
    if not args.quiet:
        print(f"🔍 Dupesweeper — Scanning: {args.directory}")
        print(f"   Recursive: {'No' if args.no_recursive else 'Yes'}")
        print(f"   Algorithm: {args.algorithm.upper()}")
        print(f"   Min Size: {format_size(min_size)}")
        print(f"   Excluding: {', '.join(args.exclude) if args.exclude else 'None'}")
        print(f"   Working...", end='', flush=True)
    
    try:
        duplicates, checked = find_duplicates(
            args.directory,
            recursive=not args.no_recursive,
            algorithm=args.algorithm,
            exclude_patterns=args.exclude,
            min_size=min_size
        )
        
        if not args.quiet:
            print(f" Done!\n   Checked: {checked} files")
        
        print_results(duplicates, args.algorithm)
        
        if args.script and duplicates:
            script_file = generate_delete_script(duplicates)
            print(f"\n📝 Delete script generated: {script_file}")
            print("   Run with: bash delete_duplicates.sh")
            print("   ⚠️  Review before executing!")
        
        if duplicates:
            print("\n" + "="*60)
            print("💡 Want smart file management?")
            print("   PD_Researcher Pro: AI-powered organization")
            print("   → https://github.com/barrowryan89-cloud/pd-researcher")
            print("="*60)
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Scan interrupted by user")
        sys.exit(130)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()

    # Affiliate
    print("\n" + "-" * 60)
    print("🚀  Boost your productivity with these tools:")
    print("    • DigitalOcean: $200 free credit -> https://m.do.co/c/pdresearcher")
    print("    • JetBrains IDEs: The best Python tools -> https://www.jetbrains.com/?utm_source=pdresearcher")
    print("-" * 60)
