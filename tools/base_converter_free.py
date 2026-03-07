#!/usr/bin/env python3
"""
base_converter_free.py - Number Base Converter
Convert between binary, octal, decimal, and hexadecimal.
Zero dependencies. Pure Python 3.
"""

import sys
import re

def detect_base(number_str: str) -> int:
    """Auto-detect the base of a number string."""
    s = number_str.strip().lower()
    
    # Check for prefixes
    if s.startswith('0b'):
        return 2
    elif s.startswith('0o'):
        return 8
    elif s.startswith('0x'):
        return 16
    
    # Check content
    if all(c in '01' for c in s):
        # Could be binary
        return 2
    elif all(c in '01234567' for c in s):
        # Could be octal
        return 8
    elif all(c in '0123456789abcdef' for c in s):
        # Has hex chars, check if valid hex
        if any(c in 'abcdef' for c in s):
            return 16
    
    # Default to decimal
    return 10

def to_decimal(number_str: str, base: int) -> int:
    """Convert any base to decimal."""
    # Remove prefixes
    s = number_str.strip().lower()
    if s.startswith('0b'):
        s = s[2:]
    elif s.startswith('0o'):
        s = s[2:]
    elif s.startswith('0x'):
        s = s[2:]
    
    return int(s, base)

def from_decimal(decimal: int, base: int) -> str:
    """Convert decimal to any base."""
    if decimal == 0:
        return '0'
    
    digits = "0123456789abcdef"
    negative = decimal < 0
    decimal = abs(decimal)
    result = ""
    
    while decimal > 0:
        result = digits[decimal % base] + result
        decimal //= base
    
    return '-' + result if negative else result

def format_number(number_str: str, base: int) -> str:
    """Format number with appropriate prefix."""
    s = number_str.strip().lower()
    
    # Remove existing prefix
    if s.startswith('0b'):
        s = s[2:]
    elif s.startswith('0o'):
        s = s[2:]
    elif s.startswith('0x'):
        s = s[2:]
    
    if base == 2:
        return f"0b{s}"
    elif base == 8:
        return f"0o{s}"
    elif base == 16:
        return f"0x{s}"
    else:
        return s

def convert(number_str: str, from_base: int = None, to_base: int = None):
    """Convert number between bases."""
    # Auto-detect source base if not specified
    if from_base is None:
        from_base = detect_base(number_str)
    
    # Convert to decimal first
    try:
        decimal = to_decimal(number_str, from_base)
    except ValueError as e:
        return f"Error: Invalid number for base {from_base}"
    
    # If target base specified, convert to it
    if to_base is not None:
        result = from_decimal(decimal, to_base)
        return format_number(result, to_base)
    
    # Otherwise show all conversions
    return {
        'decimal': decimal,
        'binary': format_number(from_decimal(decimal, 2), 2),
        'octal': format_number(from_decimal(decimal, 8), 8),
        'hex': format_number(from_decimal(decimal, 16), 16),
    }

def print_conversions(number_str: str, from_base: int = None):
    """Print all base conversions."""
    result = convert(number_str, from_base)
    
    if isinstance(result, str):
        print(result)
        return
    
    # Detect what base the input was
    detected = from_base if from_base else detect_base(number_str)
    base_names = {2: 'Binary', 8: 'Octal', 10: 'Decimal', 16: 'Hexadecimal'}
    detected_name = base_names.get(detected, f'Base {detected}')
    
    print(f"🔢 Base Conversion: \"{number_str.strip()}\" (detected as {detected_name})")
    print("=" * 50)
    print(f"\nBinary:      {result['binary']:>30}")
    print(f"Octal:       {result['octal']:>30}")
    print(f"Decimal:     {result['decimal']:>30,}")
    print(f"Hexadecimal: {result['hex']:>30}")
    
    # Show ASCII if in range
    if 32 <= result['decimal'] <= 126:
        print(f"\nASCII:       '{chr(result['decimal'])}'")
    
    print("\n" + "=" * 50)

def main():
    if len(sys.argv) < 2:
        print("Usage: base_converter_free.py <number> [from_base] [to_base]")
        print("\nBases:")
        print("  2  = Binary (prefix: 0b)")
        print("  8  = Octal (prefix: 0o)")
        print("  10 = Decimal")
        print("  16 = Hexadecimal (prefix: 0x)")
        print("\nExamples:")
        print('  base_converter_free.py 255')
        print('  base_converter_free.py 0b11111111')
        print('  base_converter_free.py 255 10 16    # dec to hex')
        print('  base_converter_free.py FF 16 2      # hex to bin')
        print('  base_converter_free.py 377 8 10     # oct to dec')
        sys.exit(1)
    
    number = sys.argv[1]
    from_base = int(sys.argv[2]) if len(sys.argv) > 2 else None
    to_base = int(sys.argv[3]) if len(sys.argv) > 3 else None
    
    if to_base:
        # Single conversion
        result = convert(number, from_base, to_base)
        print(result)
    else:
        # Show all conversions
        print_conversions(number, from_base)

if __name__ == "__main__":
    main()
