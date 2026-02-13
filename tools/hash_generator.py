#!/usr/bin/env python3
"""
Hash Generator — Tool #36
Generate cryptographic hashes for files and strings.
Part of the PD_Researcher free tool suite.
"""

import argparse
import hashlib
import sys
from pathlib import Path


# Available hash algorithms
HASH_ALGORITHMS = {
    'md5': hashlib.md5,
    'sha1': hashlib.sha1,
    'sha224': hashlib.sha224,
    'sha256': hashlib.sha256,
    'sha384': hashlib.sha384,
    'sha512': hashlib.sha512,
    'blake2b': hashlib.blake2b,
    'blake2s': hashlib.blake2s,
    'sha3_224': hashlib.sha3_224,
    'sha3_256': hashlib.sha3_256,
    'sha3_384': hashlib.sha3_384,
    'sha3_512': hashlib.sha3_512,
}


def hash_string(text, algorithm='sha256', encoding='utf-8'):
    """Hash a string."""
    hasher = HASH_ALGORITHMS[algorithm]()
    hasher.update(text.encode(encoding))
    return hasher.hexdigest()


def hash_file(filepath, algorithm='sha256', block_size=8192):
    """Hash a file."""
    hasher = HASH_ALGORITHMS[algorithm]()
    with open(filepath, 'rb') as f:
        while chunk := f.read(block_size):
            hasher.update(chunk)
    return hasher.hexdigest()


def hash_bytes(data, algorithm='sha256'):
    """Hash bytes."""
    hasher = HASH_ALGORITHMS[algorithm]()
    hasher.update(data)
    return hasher.hexdigest()


def verify_hash(filepath, expected_hash, algorithm='sha256'):
    """Verify a file against an expected hash."""
    actual_hash = hash_file(filepath, algorithm)
    return actual_hash.lower() == expected_hash.lower()


def main():
    parser = argparse.ArgumentParser(
        description='Generate and verify cryptographic hashes',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s string "hello"                   # SHA256 hash of string
  %(prog)s file document.pdf                # Hash file
  %(prog)s file document.pdf -a md5         # MD5 hash
  %(prog)s verify file.zip abc123...        # Verify file hash
  %(prog)s string "test" --all              # All algorithm hashes
        """
    )
    parser.add_argument('action', choices=['string', 'file', 'verify', 'check'],
                       help='Action to perform')
    parser.add_argument('target', help='String, file path, or hash to verify')
    parser.add_argument('hash', nargs='?', help='Expected hash (for verify)')
    parser.add_argument('-a', '--algorithm', default='sha256',
                       choices=list(HASH_ALGORITHMS.keys()),
                       help='Hash algorithm (default: sha256)')
    parser.add_argument('--all', action='store_true', help='Show all algorithm hashes')
    parser.add_argument('--upper', action='store_true', help='Output uppercase')
    parser.add_argument('--stdin', action='store_true', help='Read string from stdin')
    parser.add_argument('--progress', action='store_true', help='Show progress for large files')
    
    args = parser.parse_args()
    
    # Handle stdin
    if args.stdin and args.action == 'string':
        args.target = sys.stdin.read()
    
    try:
        if args.action == 'string':
            if args.all:
                print(f"String: {args.target[:50]}{'...' if len(args.target) > 50 else ''}")
                print()
                for name in HASH_ALGORITHMS.keys():
                    h = hash_string(args.target, name)
                    if args.upper:
                        h = h.upper()
                    print(f"{name:12} {h}")
            else:
                h = hash_string(args.target, args.algorithm)
                if args.upper:
                    h = h.upper()
                print(h)
        
        elif args.action == 'file':
            filepath = Path(args.target)
            if not filepath.exists():
                print(f"Error: File not found: {filepath}", file=sys.stderr)
                sys.exit(1)
            
            if args.all:
                print(f"File: {filepath}")
                print(f"Size: {filepath.stat().st_size:,} bytes")
                print()
                for name in HASH_ALGORITHMS.keys():
                    h = hash_file(filepath, name)
                    if args.upper:
                        h = h.upper()
                    print(f"{name:12} {h}")
            else:
                if args.progress and filepath.stat().st_size > 1024 * 1024:
                    print(f"Hashing {filepath.name}...", file=sys.stderr)
                h = hash_file(filepath, args.algorithm)
                if args.upper:
                    h = h.upper()
                print(f"{args.algorithm}: {h}")
        
        elif args.action in ('verify', 'check'):
            if not args.hash:
                parser.error("verify requires expected hash as third argument")
            
            filepath = Path(args.target)
            if not filepath.exists():
                print(f"Error: File not found: {filepath}", file=sys.stderr)
                sys.exit(1)
            
            actual = hash_file(filepath, args.algorithm)
            expected = args.hash.lower()
            
            if actual.lower() == expected:
                print(f"✓ Hash matches ({args.algorithm})")
                sys.exit(0)
            else:
                print(f"✗ Hash mismatch!")
                print(f"  Expected: {expected}")
                print(f"  Actual:   {actual}")
                sys.exit(1)
    
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
