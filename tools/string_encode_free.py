#!/usr/bin/env python3
"""
string_encode_free.py - String Encoding Tool
Encode/decode strings: Base64, Base32, URL, ROT13, hex, binary.
Zero dependencies. Pure Python 3.
"""

import sys
import base64
import urllib.parse
import codecs
import binascii

def to_rot13(text: str) -> str:
    """Apply ROT13 encoding."""
    return codecs.encode(text, 'rot_13')

def to_base64(text: str) -> str:
    """Encode to Base64."""
    return base64.b64encode(text.encode()).decode()

def from_base64(text: str) -> str:
    """Decode from Base64."""
    try:
        return base64.b64decode(text).decode()
    except:
        return "Error: Invalid Base64"

def to_base32(text: str) -> str:
    """Encode to Base32."""
    return base64.b32encode(text.encode()).decode()

def from_base32(text: str) -> str:
    """Decode from Base32."""
    try:
        return base64.b32decode(text).decode()
    except:
        return "Error: Invalid Base32"

def to_url(text: str) -> str:
    """URL encode."""
    return urllib.parse.quote(text)

def from_url(text: str) -> str:
    """URL decode."""
    return urllib.parse.unquote(text)

def to_hex(text: str) -> str:
    """Convert to hex."""
    return text.encode().hex()

def from_hex(text: str) -> str:
    """Convert from hex."""
    try:
        return bytes.fromhex(text).decode()
    except:
        return "Error: Invalid hex"

def to_binary(text: str) -> str:
    """Convert to binary."""
    return ' '.join(format(ord(c), '08b') for c in text)

def from_binary(text: str) -> str:
    """Convert from binary."""
    try:
        # Remove spaces and convert
        binary = text.replace(' ', '')
        return ''.join(chr(int(binary[i:i+8], 2)) for i in range(0, len(binary), 8))
    except:
        return "Error: Invalid binary"

def to_morse(text: str) -> str:
    """Convert to Morse code."""
    MORSE = {
        'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.',
        'F': '..-.', 'G': '--.', 'H': '....', 'I': '..', 'J': '.---',
        'K': '-.-', 'L': '.-..', 'M': '--', 'N': '-.', 'O': '---',
        'P': '.--.', 'Q': '--.-', 'R': '.-.', 'S': '...', 'T': '-',
        'U': '..-', 'V': '...-', 'W': '.--', 'X': '-..-', 'Y': '-.--',
        'Z': '--..', '0': '-----', '1': '.----', '2': '..---', '3': '...--',
        '4': '....-', '5': '.....', '6': '-....', '7': '--...', '8': '---..',
        '9': '----.', ' ': '/', '.': '.-.-.-', ',': '--..--', '?': '..--..',
    }
    return ' '.join(MORSE.get(c.upper(), c) for c in text)

def show_all(text: str):
    """Show all encodings of text."""
    print(f"📝 String Encoding: \"{text[:50]}{'...' if len(text) > 50 else ''}\"")
    print("=" * 60)
    
    encodings = [
        ("Original", text),
        ("Base64", to_base64(text)),
        ("Base32", to_base32(text)),
        ("URL Encoded", to_url(text)),
        ("Hex", to_hex(text)),
        ("Binary", to_binary(text)),
        ("ROT13", to_rot13(text)),
        ("Morse", to_morse(text)),
    ]
    
    for name, value in encodings:
        # Truncate long values
        display = value[:70] + "..." if len(value) > 70 else value
        print(f"\n{name:12} {display}")

def main():
    if len(sys.argv) < 3:
        print("Usage: string_encode_free.py <mode> <text>")
        print("       echo '<text>' | string_encode_free.py <mode> --stdin")
        print("\nModes:")
        print("  all         Show all encodings")
        print("  base64      Encode to Base64")
        print("  unbase64    Decode from Base64")
        print("  base32      Encode to Base32")
        print("  unbase32    Decode from Base32")
        print("  url         URL encode")
        print("  unurl       URL decode")
        print("  hex         Convert to hex")
        print("  unhex       Convert from hex")
        print("  binary      Convert to binary")
        print("  unbinary    Convert from binary")
        print("  rot13       ROT13 encode/decode")
        print("  morse       Convert to Morse code")
        print("\nExamples:")
        print('  string_encode_free.py all "Hello World"')
        print('  string_encode_free.py base64 "Hello"')
        print('  string_encode_free.py unbase64 "SGVsbG8="')
        print('  string_encode_free.py rot13 "Hello"')
        sys.exit(1)
    
    mode = sys.argv[1].lower()
    
    # Get text
    if '--stdin' in sys.argv:
        text = sys.stdin.read()
    else:
        text = sys.argv[2]
    
    # Process
    if mode == 'all':
        show_all(text)
    elif mode == 'base64':
        print(to_base64(text))
    elif mode == 'unbase64':
        print(from_base64(text))
    elif mode == 'base32':
        print(to_base32(text))
    elif mode == 'unbase32':
        print(from_base32(text))
    elif mode == 'url':
        print(to_url(text))
    elif mode == 'unurl':
        print(from_url(text))
    elif mode == 'hex':
        print(to_hex(text))
    elif mode == 'unhex':
        print(from_hex(text))
    elif mode == 'binary':
        print(to_binary(text))
    elif mode == 'unbinary':
        print(from_binary(text))
    elif mode == 'rot13':
        print(to_rot13(text))
    elif mode == 'morse':
        print(to_morse(text))
    else:
        print(f"Error: Unknown mode '{mode}'")
        sys.exit(1)

if __name__ == "__main__":
    main()
