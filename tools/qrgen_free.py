#!/usr/bin/env python3
"""
qrgen — QR code generator
Tool #63 — Free CLI Tool for PD Researcher
"""

import argparse
import sys

try:
    import qrcode
except ImportError:
    print("Error: qrcode module required. Install with: pip install qrcode[pil]", file=sys.stderr)
    sys.exit(1)


def generate_qr(data, output=None, size=10, border=2, error_correction='M'):
    """Generate QR code."""
    
    error_levels = {
        'L': qrcode.constants.ERROR_CORRECT_L,  # ~7%
        'M': qrcode.constants.ERROR_CORRECT_M,  # ~15%
        'Q': qrcode.constants.ERROR_CORRECT_Q,  # ~25%
        'H': qrcode.constants.ERROR_CORRECT_H,  # ~30%
    }
    
    qr = qrcode.QRCode(
        version=None,  # Auto-fit
        error_correction=error_levels.get(error_correction, qrcode.constants.ERROR_CORRECT_M),
        box_size=size,
        border=border,
    )
    
    qr.add_data(data)
    qr.make(fit=True)
    
    if output:
        img = qr.make_image(fill_color="black", back_color="white")
        img.save(output)
        return f"QR code saved to: {output}"
    else:
        # Terminal output
        return qr.get_ascii_art()


def main():
    parser = argparse.ArgumentParser(
        description='Generate QR codes',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  qrgen "https://example.com"              # Terminal output
  qrgen "Hello World" -o qr.png            # Save to file
  qrgen "data" -s 20                       # Larger QR code
  qrgen "data" -e H                        # High error correction
  echo "text" | qrgen -                    # Read from stdin
        """
    )
    
    parser.add_argument('data', help='Data to encode, or - for stdin')
    parser.add_argument('-o', '--output', help='Output file (PNG)')
    parser.add_argument('-s', '--size', type=int, default=10,
                       help='Box size (default: 10)')
    parser.add_argument('-b', '--border', type=int, default=2,
                       help='Border size (default: 2)')
    parser.add_argument('-e', '--error', choices=['L', 'M', 'Q', 'H'], default='M',
                       help='Error correction level (default: M)')
    parser.add_argument('--ascii', action='store_true',
                       help='Force ASCII output even with -o')
    
    args = parser.parse_args()
    
    # Get input data
    if args.data == '-':
        data = sys.stdin.read().strip()
    else:
        data = args.data
    
    if not data:
        print("Error: No data provided", file=sys.stderr)
        sys.exit(1)
    
    try:
        result = generate_qr(data, args.output, args.size, args.border, args.error)
        print(result)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
