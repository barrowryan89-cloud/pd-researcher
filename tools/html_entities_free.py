#!/usr/bin/env python3
"""
html_entities_free.py - HTML Entity Encoder/Decoder
Encode special characters to HTML entities and decode them back.
Zero dependencies. Pure Python 3.
"""

import sys
import html

# Common HTML entities
HTML_ENTITIES = {
    '&': '&amp;',
    '<': '&lt;',
    '>': '&gt;',
    '"': '&quot;',
    "'": '&#x27;',
    '/': '&#x2F;',
}

# Extended entities
EXTENDED_ENTITIES = {
    ' ': '&nbsp;',
    '©': '&copy;',
    '®': '&reg;',
    '™': '&trade;',
    '€': '&euro;',
    '£': '&pound;',
    '¥': '&yen;',
    '¢': '&cent;',
    '§': '&sect;',
    '¶': '&para;',
    '•': '&bull;',
    '…': '&hellip;',
    '—': '&mdash;',
    '–': '&ndash;',
    '“': '&ldquo;',
    '”': '&rdquo;',
    '‘': '&lsquo;',
    '’': '&rsquo;',
    '«': '&laquo;',
    '»': '&raquo;',
    '→': '&rarr;',
    '←': '&larr;',
    '↑': '&uarr;',
    '↓': '&darr;',
    '✓': '&check;',
    '✗': '&cross;',
    '°': '&deg;',
    '±': '&plusmn;',
    '×': '&times;',
    '÷': '&divide;',
    '¼': '&frac14;',
    '½': '&frac12;',
    '¾': '&frac34;',
    '∞': '&infin;',
    '≈': '&asymp;',
    '≠': '&ne;',
    '≤': '&le;',
    '≥': '&ge;',
    '√': '&radic;',
    '∑': '&sum;',
    '∏': '&prod;',
    '∫': '&int;',
    'α': '&alpha;',
    'β': '&beta;',
    'π': '&pi;',
    'Ω': '&Omega;',
    'µ': '&micro;',
    '¶': '&para;',
    '†': '&dagger;',
    '‡': '&Dagger;',
}

def encode(text: str, extended: bool = False) -> str:
    """Encode special characters to HTML entities."""
    # Use Python's html.escape for basic encoding
    result = html.escape(text)
    
    if extended:
        # Add extended entities
        for char, entity in EXTENDED_ENTITIES.items():
            result = result.replace(char, entity)
    
    return result

def decode(text: str) -> str:
    """Decode HTML entities to characters."""
    return html.unescape(text)

def encode_all_chars(text: str) -> str:
    """Encode all non-ASCII characters to numeric entities."""
    result = []
    for char in text:
        if ord(char) > 127:
            result.append(f"&#{ord(char)};")
        elif char in HTML_ENTITIES:
            result.append(HTML_ENTITIES[char])
        else:
            result.append(char)
    return ''.join(result)

def show_entities():
    """Show common HTML entities."""
    print("Common HTML Entities:")
    print("=" * 50)
    for char, entity in sorted(HTML_ENTITIES.items(), key=lambda x: x[1]):
        print(f"  {entity:10} → '{char}'")
    
    print("\nExtended Entities:")
    print("=" * 50)
    for char, entity in sorted(EXTENDED_ENTITIES.items(), key=lambda x: x[1]):
        display = char if char.strip() else '(space)'
        print(f"  {entity:15} → {display}")

def main():
    if len(sys.argv) < 2:
        print("Usage: html_entities_free.py <encode|decode|all> <text>")
        print("       html_entities_free.py entities")
        print("       echo '<text>' | html_entities_free.py decode --stdin")
        print("\nModes:")
        print("  encode    - Encode basic entities (& < > \" ')")
        print("  decode    - Decode all entities")
        print("  all       - Encode all non-ASCII chars")
        print("  extended  - Encode with extended entities")
        print("  entities  - Show entity reference table")
        print("\nExamples:")
        print('  html_entities_free.py encode "5 < 10 & 10 > 5"')
        print('  html_entities_free.py decode "&lt;div&gt;Hello&lt;/div&gt;"')
        print('  html_entities_free.py all "Café résumé"')
        sys.exit(1)
    
    if sys.argv[1] == 'entities':
        show_entities()
        return
    
    mode = sys.argv[1].lower()
    
    # Get text
    if '--stdin' in sys.argv:
        text = sys.stdin.read()
    elif len(sys.argv) >= 3:
        text = sys.argv[2]
    else:
        print("Error: No text provided")
        sys.exit(1)
    
    if mode == 'encode':
        result = encode(text)
    elif mode == 'decode':
        result = decode(text)
    elif mode == 'all':
        result = encode_all_chars(text)
    elif mode == 'extended':
        result = encode(text, extended=True)
    else:
        print(f"Error: Unknown mode '{mode}'")
        print("Use: encode, decode, all, extended, or entities")
        sys.exit(1)
    
    print(result)

if __name__ == "__main__":
    main()
