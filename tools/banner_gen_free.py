#!/usr/bin/env python3
"""
banner_gen_free.py - ASCII Banner Generator
Create large ASCII text banners from input strings.
Zero dependencies. Pure Python 3.
"""

import sys

# 5-line high font for basic characters
FONT = {
    'A': [
        " ███ ",
        "█   █",
        "█████",
        "█   █",
        "█   █"
    ],
    'B': [
        "████ ",
        "█   █",
        "████ ",
        "█   █",
        "████ "
    ],
    'C': [
        " ████",
        "█    ",
        "█    ",
        "█    ",
        " ████"
    ],
    'D': [
        "████ ",
        "█   █",
        "█   █",
        "█   █",
        "████ "
    ],
    'E': [
        "█████",
        "█    ",
        "████ ",
        "█    ",
        "█████"
    ],
    'F': [
        "█████",
        "█    ",
        "████ ",
        "█    ",
        "█    "
    ],
    'G': [
        " ████",
        "█    ",
        "█  ██",
        "█   █",
        " ████"
    ],
    'H': [
        "█   █",
        "█   █",
        "█████",
        "█   █",
        "█   █"
    ],
    'I': [
        "█████",
        "  █  ",
        "  █  ",
        "  █  ",
        "█████"
    ],
    'J': [
        "█████",
        "   █ ",
        "   █ ",
        "█  █ ",
        " ██  "
    ],
    'K': [
        "█   █",
        "█  █ ",
        "███  ",
        "█  █ ",
        "█   █"
    ],
    'L': [
        "█    ",
        "█    ",
        "█    ",
        "█    ",
        "█████"
    ],
    'M': [
        "█   █",
        "██ ██",
        "█ █ █",
        "█   █",
        "█   █"
    ],
    'N': [
        "█   █",
        "██  █",
        "█ █ █",
        "█  ██",
        "█   █"
    ],
    'O': [
        " ███ ",
        "█   █",
        "█   █",
        "█   █",
        " ███ "
    ],
    'P': [
        "████ ",
        "█   █",
        "████ ",
        "█    ",
        "█    "
    ],
    'Q': [
        " ███ ",
        "█   █",
        "█   █",
        "█  ██",
        " █████"
    ],
    'R': [
        "████ ",
        "█   █",
        "████ ",
        "█  █ ",
        "█   █"
    ],
    'S': [
        " ████",
        "█    ",
        " ███ ",
        "    █",
        "████ "
    ],
    'T': [
        "█████",
        "  █  ",
        "  █  ",
        "  █  ",
        "  █  "
    ],
    'U': [
        "█   █",
        "█   █",
        "█   █",
        "█   █",
        " ███ "
    ],
    'V': [
        "█   █",
        "█   █",
        "█   █",
        " █ █ ",
        "  █  "
    ],
    'W': [
        "█   █",
        "█   █",
        "█ █ █",
        "██ ██",
        "█   █"
    ],
    'X': [
        "█   █",
        " █ █ ",
        "  █  ",
        " █ █ ",
        "█   █"
    ],
    'Y': [
        "█   █",
        " █ █ ",
        "  █  ",
        "  █  ",
        "  █  "
    ],
    'Z': [
        "█████",
        "   █ ",
        "  █  ",
        " █   ",
        "█████"
    ],
    '0': [
        " ███ ",
        "█  ██",
        "█ █ █",
        "██  █",
        " ███ "
    ],
    '1': [
        "  █  ",
        " ██  ",
        "  █  ",
        "  █  ",
        "█████"
    ],
    '2': [
        " ███ ",
        "    █",
        " ███ ",
        "█    ",
        "█████"
    ],
    '3': [
        "████ ",
        "    █",
        " ███ ",
        "    █",
        "████ "
    ],
    '4': [
        "█   █",
        "█   █",
        "█████",
        "    █",
        "    █"
    ],
    '5': [
        "█████",
        "█    ",
        "████ ",
        "    █",
        "████ "
    ],
    '6': [
        " ███ ",
        "█    ",
        "████ ",
        "█   █",
        " ███ "
    ],
    '7': [
        "█████",
        "   █ ",
        "  █  ",
        " █   ",
        "█    "
    ],
    '8': [
        " ███ ",
        "█   █",
        " ███ ",
        "█   █",
        " ███ "
    ],
    '9': [
        " ███ ",
        "█   █",
        " ████",
        "    █",
        " ███ "
    ],
    ' ': [
        "     ",
        "     ",
        "     ",
        "     ",
        "     "
    ],
    '-': [
        "     ",
        "     ",
        "█████",
        "     ",
        "     "
    ],
    '_': [
        "     ",
        "     ",
        "     ",
        "     ",
        "█████"
    ],
    '.': [
        "     ",
        "     ",
        "     ",
        "     ",
        "  █  "
    ],
    '!': [
        "  █  ",
        "  █  ",
        "  █  ",
        "     ",
        "  █  "
    ],
    '?': [
        " ███ ",
        "    █",
        "  ██ ",
        "     ",
        "  █  "
    ],
}

def generate_banner(text: str, char: str = '█'):
    """Generate ASCII banner from text."""
    text = text.upper()
    lines = [[] for _ in range(5)]
    
    for letter in text:
        if letter in FONT:
            pattern = FONT[letter]
        else:
            pattern = FONT.get('?', FONT[' '])
        
        for i, line in enumerate(pattern):
            # Replace the default █ with user's chosen character
            if char != '█':
                line = line.replace('█', char)
            lines[i].append(line)
    
    # Join lines with spacing between letters
    result = []
    for line_parts in lines:
        result.append(" ".join(line_parts))
    
    return "\n".join(result)

def list_available():
    """List available characters."""
    chars = sorted(FONT.keys())
    print("Available characters:")
    for char in chars:
        if char == ' ':
            print("  ' ' (space)")
        else:
            print(f"  '{char}'")

def main():
    if len(sys.argv) < 2:
        print("Usage: banner_gen_free.py <text> [char]")
        print("       banner_gen_free.py chars")
        print("\nExamples:")
        print('  banner_gen_free.py "HELLO"')
        print('  banner_gen_free.py "HELLO" "#"')
        print('  banner_gen_free.py chars')
        sys.exit(1)
    
    if sys.argv[1].lower() == 'chars':
        list_available()
        return
    
    text = sys.argv[1]
    char = sys.argv[2] if len(sys.argv) > 2 else '█'
    
    if len(char) != 1:
        print("Error: Character must be a single character")
        sys.exit(1)
    
    banner = generate_banner(text, char)
    print(banner)

if __name__ == "__main__":
    main()
