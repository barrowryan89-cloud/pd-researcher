#!/usr/bin/env python3
"""
CSS Formatter & Beautifier - Tool #57
Format, minify, and validate CSS files.

Usage:
    css_formatter_free.py <file.css> [options]
    cat style.css | css_formatter_free.py [options]
    css_formatter_free.py --demo

Options:
    --minify          Minify CSS (remove whitespace, comments)
    --validate        Validate CSS syntax
    --analyze         Show CSS statistics (selectors, properties, colors)
    --backup          Create .bak backup file
    --indent N        Indentation spaces (default: 2)
    --output FILE     Output file (default: stdout or in-place)
"""

import sys
import re
import argparse
from pathlib import Path
from datetime import datetime


def parse_args():
    parser = argparse.ArgumentParser(
        description='CSS Formatter & Beautifier - Free Tool #57',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
    css_formatter_free.py style.css --backup
    css_formatter_free.py style.css --minify --output style.min.css
    cat style.css | css_formatter_free.py --validate
    css_formatter_free.py style.css --analyze
        '''
    )
    parser.add_argument('file', nargs='?', help='CSS file to process')
    parser.add_argument('--minify', action='store_true', help='Minify CSS')
    parser.add_argument('--validate', action='store_true', help='Validate CSS syntax')
    parser.add_argument('--analyze', action='store_true', help='Analyze CSS statistics')
    parser.add_argument('--backup', action='store_true', help='Create backup file')
    parser.add_argument('--indent', type=int, default=2, help='Indentation spaces (default: 2)')
    parser.add_argument('--output', '-o', help='Output file (default: stdout)')
    parser.add_argument('--demo', action='store_true', help='Show demo')
    return parser.parse_args()


def show_demo():
    demo_css = '''/* Demo CSS */
.container{max-width:1200px;margin:0 auto;padding:20px}
.header{background:#333;color:white;padding:10px}
.btn{display:inline-block;padding:8px 16px;background:#007bff;color:white;border-radius:4px}
'''
    print("=" * 60)
    print("🎨 CSS Formatter & Beautifier - Tool #57 Demo")
    print("=" * 60)
    print("\n📥 INPUT CSS:")
    print("-" * 40)
    print(demo_css)
    
    print("\n✨ FORMATTED OUTPUT:")
    print("-" * 40)
    formatted = format_css(demo_css, indent=2)
    print(formatted)
    
    print("\n🗜️  MINIFIED OUTPUT:")
    print("-" * 40)
    minified = minify_css(demo_css)
    print(minified)
    
    print("\n📊 ANALYSIS:")
    print("-" * 40)
    analyze_css(demo_css)


def format_css(css_text, indent=2):
    """Format and beautify CSS."""
    # Remove existing whitespace
    css_text = css_text.strip()
    
    # Preserve comments
    comments = []
    def save_comment(match):
        comments.append(match.group(0))
        return f"___COMMENT_{len(comments)-1}___"
    
    css_text = re.sub(r'/\*.*?\*/', save_comment, css_text, flags=re.DOTALL)
    
    # Add newlines after closing braces
    css_text = re.sub(r'\}', '}\n', css_text)
    
    # Split into rules
    rules = []
    current_rule = ""
    brace_count = 0
    
    for char in css_text:
        current_rule += char
        if char == '{':
            brace_count += 1
        elif char == '}':
            brace_count -= 1
            if brace_count == 0:
                rules.append(current_rule.strip())
                current_rule = ""
    
    if current_rule.strip():
        rules.append(current_rule.strip())
    
    # Format each rule
    formatted_rules = []
    indent_str = ' ' * indent
    
    for rule in rules:
        if not rule:
            continue
            
        # Handle media queries and other nested blocks
        if '@media' in rule or '@supports' in rule or '@keyframes' in rule:
            formatted_rules.append(format_nested_block(rule, indent))
            continue
        
        # Split selector and declarations
        if '{' in rule and '}' in rule:
            selector_part = rule[:rule.index('{')].strip()
            declarations = rule[rule.index('{')+1:rule.rindex('}')].strip()
            
            # Format declarations
            formatted_decls = []
            for decl in declarations.split(';'):
                decl = decl.strip()
                if decl:
                    formatted_decls.append(f"{indent_str}{decl};")
            
            formatted_rule = f"{selector_part} {{"
            if formatted_decls:
                formatted_rule += "\n" + "\n".join(formatted_decls) + "\n"
            formatted_rule += "}"
            formatted_rules.append(formatted_rule)
        else:
            formatted_rules.append(rule)
    
    # Restore comments
    result = "\n\n".join(formatted_rules)
    for i, comment in enumerate(comments):
        result = result.replace(f"___COMMENT_{i}___", f"\n{comment}\n")
    
    return result.strip()


def format_nested_block(block, indent):
    """Format @media, @supports, @keyframes blocks."""
    indent_str = ' ' * indent
    
    # Find the block name and content
    match = re.match(r'(@\w+[^\{]*)\{', block)
    if not match:
        return block
    
    rule_name = match.group(1).strip()
    content_start = match.end()
    content = block[content_start:block.rindex('}')]
    
    # Format inner rules
    inner_formatted = format_css(content, indent)
    inner_lines = inner_formatted.split('\n')
    indented_inner = '\n'.join(f"{indent_str}{line}" for line in inner_lines if line.strip())
    
    return f"{rule_name} {{\n{indented_inner}\n}}"


def minify_css(css_text):
    """Minify CSS by removing whitespace and comments."""
    # Remove comments
    css_text = re.sub(r'/\*.*?\*/', '', css_text, flags=re.DOTALL)
    
    # Remove newlines and extra spaces
    css_text = ' '.join(css_text.split())
    
    # Remove spaces around punctuation
    css_text = re.sub(r'\s*([{}:;,])\s*', r'\1', css_text)
    
    # Remove leading/trailing semicolons
    css_text = css_text.strip()
    
    return css_text


def validate_css(css_text):
    """Validate CSS for common syntax errors."""
    errors = []
    warnings = []
    
    # Check for unmatched braces
    open_braces = css_text.count('{')
    close_braces = css_text.count('}')
    if open_braces != close_braces:
        errors.append(f"Unmatched braces: {open_braces} opening, {close_braces} closing")
    
    # Check for unmatched parentheses
    open_parens = css_text.count('(')
    close_parens = css_text.count(')')
    if open_parens != close_parens:
        errors.append(f"Unmatched parentheses: {open_parens} opening, {close_parens} closing")
    
    # Check for missing semicolons before closing braces
    for match in re.finditer(r'([^};{\s])\s*\}', css_text):
        warnings.append(f"Missing semicolon before closing brace near: {match.group(1)}")
    
    # Check for empty rules
    for match in re.finditer(r'([^{]+)\{\s*\}', css_text):
        warnings.append(f"Empty rule: {match.group(1).strip()}")
    
    # Check for common typos
    common_typos = ['colour', 'wdith', 'heihgt', 'backgorund', 'bordre', 'paddign', 'margn']
    for typo in common_typos:
        if typo in css_text.lower():
            suggestions = {'colour': 'color', 'wdith': 'width', 'heihgt': 'height', 
                          'backgorund': 'background', 'bordre': 'border', 
                          'paddign': 'padding', 'margn': 'margin'}
            warnings.append(f"Possible typo: '{typo}' - did you mean '{suggestions.get(typo, typo)}'?")
    
    return errors, warnings


def analyze_css(css_text):
    """Analyze CSS and show statistics."""
    print("📊 CSS Analysis Report")
    print("=" * 40)
    
    # Count rules
    rules = re.findall(r'[^{]+\{[^}]*\}', css_text)
    print(f"Total CSS Rules: {len(rules)}")
    
    # Count selectors
    selectors = []
    for rule in rules:
        selector_part = rule[:rule.index('{')].strip()
        # Split by comma for multiple selectors
        for sel in selector_part.split(','):
            selectors.append(sel.strip())
    print(f"Total Selectors: {len(selectors)}")
    
    # Extract properties
    all_props = re.findall(r'([\w-]+)\s*:', css_text)
    unique_props = sorted(set(p.lower() for p in all_props))
    print(f"Unique Properties: {len(unique_props)}")
    
    # Extract colors
    hex_colors = re.findall(r'#([0-9a-fA-F]{3,8})', css_text)
    rgb_colors = re.findall(r'rgba?\([^)]+\)', css_text)
    hsl_colors = re.findall(r'hsla?\([^)]+\)', css_text)
    named_colors = re.findall(r':\s*(red|blue|green|black|white|yellow|orange|purple|pink|gray|grey|cyan|magenta)\s*[;}]', css_text, re.IGNORECASE)
    total_colors = len(hex_colors) + len(rgb_colors) + len(hsl_colors) + len(named_colors)
    print(f"Colors Used: {total_colors}")
    print(f"  - Hex: {len(hex_colors)}")
    print(f"  - RGB/RGBA: {len(rgb_colors)}")
    print(f"  - HSL/HSLA: {len(hsl_colors)}")
    print(f"  - Named: {len(named_colors)}")
    
    # Extract font families
    font_matches = re.findall(r'font-family\s*:\s*([^;]+)', css_text)
    fonts = [f.strip().strip('"\'') for f in font_matches]
    if fonts:
        print(f"Font Families: {len(fonts)}")
        for f in set(fonts):
            print(f"  - {f}")
    
    # Check for media queries
    media_queries = re.findall(r'@media\s+([^{]+)', css_text)
    if media_queries:
        print(f"Media Queries: {len(media_queries)}")
    
    # Check for animations
    keyframes = re.findall(r'@keyframes\s+(\w+)', css_text)
    if keyframes:
        print(f"Keyframe Animations: {len(keyframes)}")
        for anim in keyframes:
            print(f"  - {anim}")
    
    # File size
    original_size = len(css_text.encode('utf-8'))
    minified = minify_css(css_text)
    minified_size = len(minified.encode('utf-8'))
    savings = original_size - minified_size
    
    print(f"\n📦 Size Analysis:")
    print(f"  Original: {original_size:,} bytes")
    print(f"  Minified: {minified_size:,} bytes")
    print(f"  Savings: {savings:,} bytes ({savings/original_size*100:.1f}%)")


def process_file(filepath, args):
    """Process a CSS file."""
    path = Path(filepath)
    
    if not path.exists():
        print(f"❌ Error: File not found: {filepath}", file=sys.stderr)
        return 1
    
    try:
        css_text = path.read_text(encoding='utf-8')
    except Exception as e:
        print(f"❌ Error reading file: {e}", file=sys.stderr)
        return 1
    
    # Create backup
    if args.backup and not args.output:
        backup_path = path.with_suffix('.css.bak')
        backup_path.write_text(css_text, encoding='utf-8')
        print(f"💾 Backup created: {backup_path}")
    
    # Validation
    if args.validate:
        errors, warnings = validate_css(css_text)
        print(f"🔍 Validation Results for {path.name}:")
        print("=" * 40)
        if errors:
            print(f"❌ {len(errors)} Error(s):")
            for err in errors:
                print(f"   - {err}")
        if warnings:
            print(f"⚠️  {len(warnings)} Warning(s):")
            for warn in warnings:
                print(f"   - {warn}")
        if not errors and not warnings:
            print("✅ No issues found!")
        print()
    
    # Analysis
    if args.analyze:
        analyze_css(css_text)
        return 0
    
    # Format or minify
    if args.minify:
        result = minify_css(css_text)
    else:
        result = format_css(css_text, args.indent)
    
    # Output
    if args.output:
        output_path = Path(args.output)
        output_path.write_text(result, encoding='utf-8')
        print(f"✅ Written to: {output_path}")
    else:
        print(result)
    
    return 0


def main():
    args = parse_args()
    
    if args.demo:
        show_demo()
        return 0
    
    # Read from stdin if no file provided
    if not args.file:
        css_text = sys.stdin.read()
        
        if not css_text.strip():
            print("❌ Error: No CSS provided via stdin", file=sys.stderr)
            return 1
        
        if args.validate:
            errors, warnings = validate_css(css_text)
            print("🔍 Validation Results:")
            print("=" * 40)
            if errors:
                print(f"❌ {len(errors)} Error(s):")
                for err in errors:
                    print(f"   - {err}")
            if warnings:
                print(f"⚠️  {len(warnings)} Warning(s):")
                for warn in warnings:
                    print(f"   - {warn}")
            if not errors and not warnings:
                print("✅ No issues found!")
            return 0
        
        if args.analyze:
            analyze_css(css_text)
            return 0
        
        if args.minify:
            result = minify_css(css_text)
        else:
            result = format_css(css_text, args.indent)
        
        print(result)
        return 0
    
    return process_file(args.file, args)


if __name__ == '__main__':
    sys.exit(main())
