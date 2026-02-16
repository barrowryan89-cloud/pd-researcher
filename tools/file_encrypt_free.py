#!/usr/bin/env python3
"""
file_encrypt_free.py - Simple File Encryption
Encrypt/decrypt files with password using XOR cipher.
Zero dependencies. Pure Python 3.
WARNING: This is for educational/utility purposes. Use proper encryption for sensitive data.
"""

import sys
import os
import hashlib
import getpass

def derive_key(password: str, salt: bytes = None) -> tuple:
    """Derive encryption key from password."""
    if salt is None:
        salt = os.urandom(16)
    
    # Simple key derivation using hash
    key = hashlib.pbkdf2_hmac('sha256', password.encode(), salt, 100000)
    return key, salt

def xor_cipher(data: bytes, key: bytes) -> bytes:
    """Simple XOR cipher for encryption/decryption."""
    return bytes(b ^ key[i % len(key)] for i, b in enumerate(data))

def encrypt_file(input_path: str, output_path: str, password: str):
    """Encrypt a file."""
    try:
        # Read file
        with open(input_path, 'rb') as f:
            data = f.read()
        
        # Derive key
        key, salt = derive_key(password)
        
        # Encrypt
        encrypted = xor_cipher(data, key)
        
        # Write with salt prefix
        with open(output_path, 'wb') as f:
            f.write(salt)
            f.write(encrypted)
        
        return True, len(data)
    except Exception as e:
        return False, str(e)

def decrypt_file(input_path: str, output_path: str, password: str):
    """Decrypt a file."""
    try:
        # Read file
        with open(input_path, 'rb') as f:
            data = f.read()
        
        # Extract salt (first 16 bytes)
        if len(data) < 16:
            return False, "Invalid encrypted file"
        
        salt = data[:16]
        encrypted = data[16:]
        
        # Derive key
        key, _ = derive_key(password, salt)
        
        # Decrypt
        decrypted = xor_cipher(encrypted, key)
        
        # Write
        with open(output_path, 'wb') as f:
            f.write(decrypted)
        
        return True, len(decrypted)
    except Exception as e:
        return False, str(e)

def get_password(prompt: str = "Password: ") -> str:
    """Get password from user."""
    if sys.stdin.isatty():
        return getpass.getpass(prompt)
    else:
        return sys.stdin.readline().strip()

def main():
    if len(sys.argv) < 4:
        print("Usage: file_encrypt_free.py <encrypt|decrypt> <input_file> <output_file>")
        print("\nExamples:")
        print('  file_encrypt_free.py encrypt secret.txt secret.enc')
        print('  file_encrypt_free.py decrypt secret.enc secret.txt')
        print("\n⚠️  WARNING:")
        print("This tool uses basic XOR encryption for simple file protection.")
        print("For sensitive data, use proper encryption tools like GPG.")
        sys.exit(1)
    
    operation = sys.argv[1].lower()
    input_file = sys.argv[2]
    output_file = sys.argv[3]
    
    # Validate operation
    if operation not in ('encrypt', 'decrypt', 'e', 'd'):
        print("Error: Operation must be 'encrypt' or 'decrypt'")
        sys.exit(1)
    
    # Check input file exists
    if not os.path.exists(input_file):
        print(f"Error: Input file not found: {input_file}")
        sys.exit(1)
    
    # Check output doesn't exist (unless force)
    if os.path.exists(output_file) and '--force' not in sys.argv:
        print(f"Error: Output file already exists: {output_file}")
        print("Use --force to overwrite")
        sys.exit(1)
    
    # Get password
    if operation in ('encrypt', 'e'):
        print(f"🔐 Encrypting: {input_file} -> {output_file}")
        password = get_password("Enter password: ")
        confirm = get_password("Confirm password: ")
        
        if password != confirm:
            print("❌ Error: Passwords do not match")
            sys.exit(1)
        
        if len(password) < 8:
            print("⚠️  Warning: Password is less than 8 characters")
        
        success, result = encrypt_file(input_file, output_file, password)
        
        if success:
            print(f"✅ Encrypted: {result} bytes")
            print(f"   Output: {output_file}")
            # Show size difference
            orig_size = os.path.getsize(input_file)
            new_size = os.path.getsize(output_file)
            print(f"   Size: {orig_size} -> {new_size} bytes (+16 salt)")
        else:
            print(f"❌ Error: {result}")
            sys.exit(1)
    else:
        print(f"🔓 Decrypting: {input_file} -> {output_file}")
        password = get_password("Enter password: ")
        
        success, result = decrypt_file(input_file, output_file, password)
        
        if success:
            print(f"✅ Decrypted: {result} bytes")
            print(f"   Output: {output_file}")
        else:
            print(f"❌ Error: {result}")
            print("Note: Wrong password or corrupted file")
            sys.exit(1)

if __name__ == "__main__":
    main()
