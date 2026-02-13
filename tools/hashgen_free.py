#!/usr/bin/env python3
"""
HashGen - Free CLI Tool #41
Generate hashes (MD5, SHA1, SHA256, SHA512) for files and strings
Zero dependencies, single file, MIT licensed
https://github.com/barrowryan89-cloud/pd-researcher
"""

import hashlib
import sys
import argparse
import os

__version__ = "1.0.0"

SUPPORTED_ALGORITHMS = ['md5', 'sha1', 'sha256', 'sha512', 'blake2b']

def hash_string(data, algorithm='sha256'):
    """Hash a string."""
    if algorithm not in SUPPORTED_ALGORITHMS:
        raise ValueError(f"Unsupported algorithm: {algorithm}")
    
    hasher = hashlib.new(algorithm)
    if isinstance(data, str):
        data = data.encode('utf-8')
    hasher.update(data)
    return hasher.hexdigest()

def hash_file(filepath, algorithm='sha256', chunk_size=8192):
    """Hash a file in chunks."""
    if algorithm not in SUPPORTED_ALGORITHMS:
        raise ValueError(f"Unsupported algorithm: {algorithm}")
    
    hasher = hashlib.new(algorithm)
    
    with open(filepath, 'rb') as f:
        while chunk := f.read(chunk_size):
            hasher.update(chunk)
    
    return hasher.hexdigest()

def hash_all(data):
    """Generate all supported hashes for data."""
    results = {}
    for algo in SUPPORTED_ALGORITHMS:
        try:
            results[algo] = hash_string(data, algo)
        except Exception as e:
            results[algo] = f"Error: {e}"
    return results

def hash_file_all(filepath):
    """Generate all supported hashes for a file."""
    results = {}
    for algo in SUPPORTED_ALGORITHMS:
        try:
            results[algo] = hash_file(filepath, algo)
        except Exception as e:
            results[algo] = f"Error: {e}"
    return results

def verify_hash(data, expected_hash, algorithm='sha256'):
    """Verify data against an expected hash."""
    actual_hash = hash_string(data, algorithm)
    return actual_hash.lower() == expected_hash.lower()

def main():
    parser = argparse.ArgumentParser(
        description="🔐 HashGen - Generate MD5, SHA1, SHA256, SHA512 hashes",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s -s "hello world"                    # Hash string
  %(prog)s -f document.pdf                     # Hash file
  %(prog)s -s "data" -a sha256                 # Specific algorithm
  %(prog)s -f file.zip --all                   # All algorithms
  %(prog)s -s "data" --verify abc123...        # Verify hash

Supported: md5, sha1, sha256, sha512, blake2b
        """
    )
    parser.add_argument('-s', '--string', help='String to hash')
    parser.add_argument('-f', '--file', help='File to hash')
    parser.add_argument('-a', '--algorithm', default='sha256',
                       choices=SUPPORTED_ALGORITHMS,
                       help='Hash algorithm (default: sha256)')
    parser.add_argument('--all', action='store_true',
                       help='Generate all supported hashes')
    parser.add_argument('--verify', metavar='HASH',
                       help='Verify against expected hash')
    parser.add_argument('--stdin', action='store_true',
                       help='Read from stdin')
    parser.add_argument('-v', '--version', action='version',
                       version=f"%(prog)s {__version__}")
    
    args = parser.parse_args()
    
    if not any([args.string, args.file, args.stdin]):
        parser.print_help()
        sys.exit(1)
    
    data = None
    is_file = False
    filepath = None
    
    if args.stdin:
        data = sys.stdin.read()
    elif args.file:
        if not os.path.exists(args.file):
            print(f"❌ File not found: {args.file}", file=sys.stderr)
            sys.exit(1)
        if not os.path.isfile(args.file):
            print(f"❌ Not a file: {args.file}", file=sys.stderr)
            sys.exit(1)
        is_file = True
        filepath = args.file
    elif args.string:
        data = args.string
    
    print("═" * 60)
    print("🔐 HashGen - Cryptographic Hash Generator")
    print("═" * 60)
    
    if is_file:
        file_size = os.path.getsize(filepath)
        print(f"\n📁 File: {filepath}")
        print(f"📊 Size: {file_size:,} bytes ({file_size / 1024 / 1024:.2f} MB)")
        
        if args.all:
            print("\n🔑 All Hashes:")
            results = hash_file_all(filepath)
            for algo, hashval in results.items():
                print(f"  {algo.upper():10} {hashval}")
        else:
            hashval = hash_file(filepath, args.algorithm)
            print(f"\n🔑 {args.algorithm.upper()}:")
            print(f"   {hashval}")
            
            if args.verify:
                match = hashval.lower() == args.verify.lower()
                status = "✅ MATCH" if match else "❌ MISMATCH"
                print(f"\n📝 Verification: {status}")
    else:
        print(f"\n📝 Input: {data[:50]}{'...' if len(data) > 50 else ''}")
        print(f"📊 Length: {len(data)} characters")
        
        if args.all:
            print("\n🔑 All Hashes:")
            results = hash_all(data)
            for algo, hashval in results.items():
                print(f"  {algo.upper():10} {hashval}")
        else:
            hashval = hash_string(data, args.algorithm)
            print(f"\n🔑 {args.algorithm.upper()}:")
            print(f"   {hashval}")
            
            if args.verify:
                match = hashval.lower() == args.verify.lower()
                status = "✅ MATCH" if match else "❌ MISMATCH"
                print(f"\n📝 Verification: {status}")
    
    print("═" * 60)
    print("\n💡 Pro Tip: Need batch hashing, HMAC, or file integrity monitoring?")
    print("   Check out PD_Researcher Pro → https://10links.blue")
    print("═" * 60)

if __name__ == '__main__':
    main()
