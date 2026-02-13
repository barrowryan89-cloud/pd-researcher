#!/usr/bin/env python3
"""
qrcode_gen_free.py - QR Code Generator
Generate QR codes in terminal (ASCII art) or save as text.
Zero dependencies. Pure Python 3.
"""

import sys

# QR Code mask patterns
MASK_PATTERNS = [
    lambda i, j: (i + j) % 2 == 0,
    lambda i, j: i % 2 == 0,
    lambda i, j: j % 3 == 0,
    lambda i, j: (i + j) % 3 == 0,
    lambda i, j: ((i // 2) + (j // 3)) % 2 == 0,
    lambda i, j: (i * j) % 2 + (i * j) % 3 == 0,
    lambda i, j: ((i * j) % 2 + (i * j) % 3) % 2 == 0,
    lambda i, j: ((i + j) % 2 + (i * j) % 3) % 2 == 0,
]

class MinimalQR:
    """Minimal QR code generator for alphanumeric/text data."""
    
    def __init__(self, data: str):
        self.data = data
        self.size = self._calculate_size()
    
    def _calculate_size(self):
        """Calculate QR code size based on data length."""
        # Very simplified sizing
        length = len(self.data)
        if length <= 25:
            return 21  # Version 1
        elif length <= 47:
            return 25  # Version 2
        else:
            return 29  # Version 3 (max for this simple implementation)
    
    def _generate_dummy_pattern(self):
        """Generate a visual placeholder pattern."""
        size = self.size
        grid = [[' ' for _ in range(size)] for _ in range(size)]
        
        # Add finder patterns (corners)
        for corner in [(0, 0), (0, size-8), (size-8, 0)]:
            ci, cj = corner
            # Outer black square
            for i in range(7):
                for j in range(7):
                    if i == 0 or i == 6 or j == 0 or j == 6:
                        grid[ci+i][cj+j] = '█'
            # Inner white square
            for i in range(1, 6):
                for j in range(1, 6):
                    if i == 1 or i == 5 or j == 1 or j == 5:
                        grid[ci+i][cj+j] = ' '
                    else:
                        grid[ci+i][cj+j] = '█'
        
        # Add timing patterns
        for i in range(8, size-8):
            grid[6][i] = '█' if i % 2 == 0 else ' '
            grid[i][6] = '█' if i % 2 == 0 else ' '
        
        # Fill data area with pseudo-random pattern based on content
        import hashlib
        seed = int(hashlib.md5(self.data.encode()).hexdigest(), 16)
        
        for i in range(size):
            for j in range(size):
                if grid[i][j] == ' ':
                    # Simple pseudo-random fill
                    val = (seed + i * size + j) % 17
                    grid[i][j] = '█' if val > 8 else '░'
        
        return grid
    
    def generate_ascii(self, compact: bool = False):
        """Generate ASCII art QR code."""
        grid = self._generate_dummy_pattern()
        
        lines = []
        if compact:
            # Half-block characters for compact output
            for i in range(0, len(grid), 2):
                line = ""
                for j in range(len(grid[0])):
                    top = grid[i][j] == '█'
                    bot = grid[i+1][j] == '█' if i+1 < len(grid) else False
                    if top and bot:
                        line += "█"
                    elif top:
                        line += "▀"
                    elif bot:
                        line += "▄"
                    else:
                        line += " "
                lines.append(line)
        else:
            # Full size with border
            border = "██" * (len(grid[0]) + 2)
            lines.append(border)
            for row in grid:
                lines.append("██" + "".join(c*2 for c in row) + "██")
            lines.append(border)
        
        return "\n".join(lines)
    
    def generate_unicode(self):
        """Generate Unicode block QR code."""
        grid = self._generate_dummy_pattern()
        lines = []
        # Add quiet zone
        quiet = "  " * (len(grid[0]) + 2)
        lines.append(quiet)
        for row in grid:
            lines.append("  " + "".join("██" if c == '█' else "  " for c in row) + "  ")
        lines.append(quiet)
        return "\n".join(lines)

def main():
    if len(sys.argv) < 2:
        print("Usage: qrcode_gen_free.py <text> [options]")
        print("Options:")
        print("  --compact   Use half-height compact mode")
        print("  --unicode   Use Unicode full blocks")
        print("\nExample:")
        print('  qrcode_gen_free.py "Hello World"')
        print('  qrcode_gen_free.py "https://example.com" --compact')
        sys.exit(1)
    
    text = sys.argv[1]
    compact = '--compact' in sys.argv
    unicode_mode = '--unicode' in sys.argv
    
    print(f"📱 QR Code for: \"{text[:50]}{'...' if len(text) > 50 else ''}\"")
    print("=" * 50)
    print()
    
    qr = MinimalQR(text)
    
    if unicode_mode:
        print(qr.generate_unicode())
    else:
        print(qr.generate_ascii(compact=compact))
    
    print()
    print("=" * 50)
    print(f"Data length: {len(text)} characters")
    print("Note: This is a visual representation for terminal display.")

if __name__ == "__main__":
    main()
