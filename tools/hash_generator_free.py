#!/usr/bin/env python3
"""
Hash Generator - Free Tool
Generate MD5, SHA1, SHA256 hashes for strings and files
Free version: Common hash algorithms
Paid upgrade: File integrity checking, hash comparison, more algorithms

Usage: python3 hash_generator_free.py <string or file>
"""

import sys
import hashlib
import os

def hash_string(text, algorithm='sha256'):
    """Hash a string"""
    if algorithm == 'md5':
        return hashlib.md5(text.encode()).hexdigest()
    elif algorithm == 'sha1':
        return hashlib.sha1(text.encode()).hexdigest()
    elif algorithm == 'sha256':
        return hashlib.sha256(text.encode()).hexdigest()
    else:
        return None

def hash_file(filepath, algorithm='sha256', block_size=65536):
    """Hash a file"""
    hasher = hashlib.new(algorithm)
    try:
        with open(filepath, 'rb') as f:
            while chunk := f.read(block_size):
                hasher.update(chunk)
        return hasher.hexdigest()
    except Exception as e:
        return f"Error: {e}"

def print_banner():
    print("""
╔════════════════════════════════════════════════════════════╗
║                   HASH GENERATOR v1.0                      ║
║              Free Tool by Sand Street Holdings             ║
╠════════════════════════════════════════════════════════════╣
║  Generate MD5, SHA1, SHA256 hashes for strings and files   ║
║                                                            ║
║  💎 Want more power?                                       ║
║     → SHA512, Blake2, SHA3 support                         ║
║     → File integrity verification                          ║
║     → Hash comparison (find duplicates)                    ║
║     → HMAC support                                         ║
║     → Check out PD_Researcher v1 ($29)                     ║
║        Solana: FEKY6bDoqBnsQZVT3XbEYS4b1DJ8QoA64G5hXycfTAhQ ║
╚════════════════════════════════════════════════════════════╝
""")

def main():
    print_banner()
    
    if len(sys.argv) < 2:
        print("❌ No input provided.")
        print("\nUsage:")
        print("  python3 hash_generator_free.py \"Hello World\"")
        print("  python3 hash_generator_free.py file.txt")
        sys.exit(1)
    
    input_data = sys.argv[1]
    
    # Check if input is a file
    if os.path.isfile(input_data):
        print(f"🔄 Hashing file: {input_data}\n")
        
        md5 = hash_file(input_data, 'md5')
        sha1 = hash_file(input_data, 'sha1')
        sha256 = hash_file(input_data, 'sha256')
        
        print(f"📁 File: {input_data}")
        print(f"📊 Size: {os.path.getsize(input_data)} bytes\n")
        
        print(f"MD5:    {md5}")
        print(f"SHA1:   {sha1}")
        print(f"SHA256: {sha256}")
    else:
        print(f"🔄 Hashing string: {input_data[:50]}{'...' if len(input_data) > 50 else ''}\n")
        
        md5 = hash_string(input_data, 'md5')
        sha1 = hash_string(input_data, 'sha1')
        sha256 = hash_string(input_data, 'sha256')
        
        print(f"MD5:    {md5}")
        print(f"SHA1:   {sha1}")
        print(f"SHA256: {sha256}")
    
    print("\n" + "="*60)
    print("\n💡 Want file integrity checking and duplicate detection?")
    print("   Upgrade to PD_Researcher v1 for advanced hash tools")
    print("   Pay with crypto: FEKY6bDoqBnsQZVT3XbEYS4b1DJ8QoA64G5hXycfTAhQ")
    print("\n🔐 Security tip: Store sensitive files securely with 1Password")
    print("   → https://1password.com [affiliate link]")
    print("="*60)

if __name__ == "__main__":
    main()
