#!/usr/bin/env python3
"""
hashgen — Universal hash generator (MD5, SHA1, SHA256, SHA512, etc.)
Tool #61 — Free CLI Tool for PD Researcher
"""

import argparse
import hashlib
import sys
from pathlib import Path


def get_available_algorithms():
    """Get all available hash algorithms."""
    return sorted(hashlib.algorithms_available)


def hash_string(data, algorithm='sha256'):
    """Hash a string using specified algorithm."""
    try:
        h = hashlib.new(algorithm)
        h.update(data.encode('utf-8'))
        return h.hexdigest()
    except ValueError as e:
        return f"Error: {e}"


def hash_file(filepath, algorithm='sha256'):
    """Hash a file using specified algorithm."""
    try:
        h = hashlib.new(algorithm)
        with open(filepath, 'rb') as f:
            while chunk := f.read(8192):
                h.update(chunk)
        return h.hexdigest()
    except FileNotFoundError:
        return f"Error: File not found: {filepath}"
    except ValueError as e:
        return f"Error: {e}"


def main():
    parser = argparse.ArgumentParser(
        description='Generate cryptographic hashes',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  hashgen "hello world"                    # SHA256 of string
  hashgen file.txt --file                  # SHA256 of file
  hashgen "test" -a md5                    # MD5 hash
  hashgen "test" -a sha512                 # SHA512 hash
  hashgen --list                           # List all algorithms
  echo "hello" | hashgen -                 # Hash from stdin
        """
    )
    
    parser.add_argument('input', help='String to hash, file path, or - for stdin')
    parser.add_argument('-a', '--algorithm', default='sha256',
                       help='Hash algorithm (default: sha256)')
    parser.add_argument('-f', '--file', action='store_true',
                       help='Treat input as file path')
    parser.add_argument('-l', '--list', action='store_true',
                       help='List available algorithms')
    parser.add_argument('-c', '--compare',
                       help='Compare generated hash with this value')
    parser.add_argument('--upper', action='store_true',
                       help='Output uppercase hash')
    
    args = parser.parse_args()
    
    if args.list:
        print("Available algorithms:")
        for algo in get_available_algorithms():
            print(f"  {algo}")
        return
    
    # Get input data
    if args.input == '-':
        data = sys.stdin.read()
        args.file = False  # Force string mode
    elif args.file:
        result = hash_file(args.input, args.algorithm)
        if result.startswith("Error:"):
            print(result, file=sys.stderr)
            sys.exit(1)
    else:
        data = args.input
        result = hash_string(data, args.algorithm)
    
    if not args.file:
        result = hash_string(data, args.algorithm)
    
    if args.upper:
        result = result.upper()
    
    print(result)
    
    # Compare if requested
    if args.compare:
        expected = args.compare.lower() if not args.upper else args.compare.upper()
        if result == expected:
            print("✅ Match")
            sys.exit(0)
        else:
            print("❌ Mismatch")
            sys.exit(1)


if __name__ == '__main__':
    main()
