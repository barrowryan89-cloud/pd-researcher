#!/usr/bin/env python3
"""
Tool #55: HTML Formatter & Beautifier
Free CLI tool for formatting, minifying, and validating HTML.
Part of the 50+ Free Developer Tools collection.
GitHub: https://github.com/barrowryan89-cloud/pd-researcher
"""

import argparse
import sys
import re
from pathlib import Path

__version__ = "1.0.0"
__author__ = "PD Researcher"

def format_html(html: str, indent_size: int = 2, max_line_length: int = 120) -> str:
    """Format/beautify HTML with proper indentation."""
    # Remove existing whitespace between tags for clean slate
    html = re.sub(r'>\s+<', '><', html.strip())
    
    formatted = []
    indent_level = 0
    indent_str = ' ' * indent_size
    
    # Self-closing tags that don't need indentation change
    self_closing = {'area', 'base', 'br', 'col', 'embed', 'hr', 'img', 
                    'input', 'link', 'meta', 'param', 'source', 'track', 'wbr'}
    
    # Tags that should stay inline (no newlines around content)
    inline_tags = {'span', 'a', 'strong', 'em', 'b', 'i', 'u', 'code', 
                   'small', 'sub', 'sup', 'mark', 'del', 'ins'}
    
    i = 0
    while i < len(html):
        if html[i] == '<':
            # Find end of tag
            tag_end = html.find('>', i)
            if tag_end == -1:
                formatted.append(html[i:])
                break
            
            tag_content = html[i:tag_end+1]
            
            # Check if it's a closing tag
            if tag_content.startswith('</'):
                tag_name = re.search(r'</(\w+)', tag_content)
                if tag_name:
                    tag_name = tag_name.group(1).lower()
                    # Decrease indent before closing tag (unless inline)
                    if tag_name not in inline_tags:
                        indent_level = max(0, indent_level - 1)
                        # New line before closing block tag
                        if formatted and not formatted[-1].endswith('\n'):
                            formatted.append('\n')
                        formatted.append(indent_str * indent_level + tag_content)
                    else:
                        formatted.append(tag_content)
            else:
                # Opening or self-closing tag
                tag_name = re.search(r'<(\w+)', tag_content)
                if tag_name:
                    tag_name = tag_name.group(1).lower()
                    
                    # New line before block-level opening tag
                    if tag_name not in inline_tags:
                        if formatted and not formatted[-1].endswith('\n'):
                            formatted.append('\n')
                        formatted.append(indent_str * indent_level + tag_content)
                        
                        # Increase indent after opening tag (unless self-closing)
                        if tag_name not in self_closing and not tag_content.endswith('/>'):
                            indent_level += 1
                    else:
                        formatted.append(tag_content)
                else:
                    # Special tags like <!DOCTYPE>
                    if formatted and not formatted[-1].endswith('\n'):
                        formatted.append('\n')
                    formatted.append(indent_str * indent_level + tag_content)
            
            i = tag_end + 1
            
            # Add newline after block tags
            if formatted and tag_name not in inline_tags:
                formatted.append('\n')
        else:
            # Text content
            text_end = html.find('<', i)
            if text_end == -1:
                text_content = html[i:]
            else:
                text_content = html[i:text_end]
            
            text_content = text_content.strip()
            if text_content:
                # Add proper indentation for text
                if formatted and formatted[-1].endswith('\n'):
                    formatted.append(indent_str * indent_level)
                formatted.append(text_content)
            
            if text_end == -1:
                break
            i = text_end
    
    result = ''.join(formatted)
    
    # Clean up: remove empty lines at start/end, normalize multiple newlines
    result = result.strip()
    result = re.sub(r'\n{3,}', '\n\n', result)
    
    return result

def minify_html(html: str) -> str:
    """Minify HTML by removing unnecessary whitespace."""
    # Remove comments (except IE conditionals)
    html = re.sub(r'<!--(?!\s*\[if)[\s\S]*?-->', '', html)
    
    # Remove whitespace between tags
    html = re.sub(r'>\s+<', '><', html)
    
    # Remove leading/trailing whitespace in text nodes
    html = re.sub(r'>\s+', '>', html)
    html = re.sub(r'\s+<', '<', html)
    
    # Normalize spaces
    html = re.sub(r'\s+', ' ', html)
    
    return html.strip()

def validate_html(html: str) -> list:
    """Basic HTML validation - returns list of issues."""
    issues = []
    
    # Check for unclosed tags
    tag_pattern = re.compile(r'<(/?)(\w+)[^>]*>')
    stack = []
    
    self_closing = {'area', 'base', 'br', 'col', 'embed', 'hr', 'img', 
                    'input', 'link', 'meta', 'param', 'source', 'track', 'wbr'}
    
    for match in tag_pattern.finditer(html):
        is_closing = match.group(1) == '/'
        tag_name = match.group(2).lower()
        
        if is_closing:
            if stack and stack[-1] == tag_name:
                stack.pop()
            elif tag_name not in self_closing:
                issues.append(f"Unexpected closing tag: </{tag_name}>")
        elif tag_name not in self_closing:
            stack.append(tag_name)
    
    # Remaining tags in stack are unclosed
    for tag in stack:
        issues.append(f"Unclosed tag: <{tag}>")
    
    # Check for doctype
    if not re.search(r'<!doctype', html, re.IGNORECASE):
        issues.append("Missing DOCTYPE declaration")
    
    # Check for html tag
    if not re.search(r'<html', html, re.IGNORECASE):
        issues.append("Missing <html> tag")
    
    # Check for common issues
    if re.search(r'<script\s+src=["\'][^"\']*["\']\s*>[^<]', html, re.IGNORECASE):
        issues.append("Script tag may be missing type attribute or has inline content with src")
    
    return issues

def extract_stats(html: str) -> dict:
    """Extract statistics about the HTML document."""
    stats = {
        'total_chars': len(html),
        'total_lines': html.count('\n') + 1,
        'tag_count': len(re.findall(r'<[^>]+>', html)),
        'text_content_size': len(re.sub(r'<[^>]+>', '', html)),
        'links': len(re.findall(r'<a\s', html, re.IGNORECASE)),
        'images': len(re.findall(r'<img\s', html, re.IGNORECASE)),
        'scripts': len(re.findall(r'<script', html, re.IGNORECASE)),
        'stylesheets': len(re.findall(r'<link[^>]*stylesheet', html, re.IGNORECASE)),
        'inline_styles': len(re.findall(r'style=["\']', html, re.IGNORECASE)),
    }
    return stats

def main():
    parser = argparse.ArgumentParser(
        description="HTML Formatter & Beautifier — Tool #55",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s -f input.html -o output.html          # Format file
  %(prog)s -m input.html -o minified.html        # Minify file
  %(prog)s -v input.html                         # Validate HTML
  cat file.html | %(prog)s -f                    # Read from stdin
  echo '<div><span>text</span></div>' | %(prog)s -f
        """
    )
    
    parser.add_argument('input', nargs='?', help='Input HTML file (default: stdin)')
    parser.add_argument('-o', '--output', help='Output file (default: stdout)')
    parser.add_argument('-f', '--format', action='store_true', 
                        help='Format/beautify HTML (default action)')
    parser.add_argument('-m', '--minify', action='store_true', 
                        help='Minify HTML (remove whitespace)')
    parser.add_argument('-v', '--validate', action='store_true', 
                        help='Validate HTML and report issues')
    parser.add_argument('-s', '--stats', action='store_true', 
                        help='Show document statistics')
    parser.add_argument('--indent', type=int, default=2, 
                        help='Indentation size (default: 2 spaces)')
    parser.add_argument('--no-preserve', action='store_true',
                        help='Do not preserve original file as .backup')
    parser.add_argument('--version', action='version', version=f'%(prog)s {__version__}')
    
    args = parser.parse_args()
    
    # Read input
    if args.input:
        try:
            html = Path(args.input).read_text(encoding='utf-8')
        except FileNotFoundError:
            print(f"Error: File not found: {args.input}", file=sys.stderr)
            sys.exit(1)
        except UnicodeDecodeError:
            print(f"Error: Could not decode file as UTF-8: {args.input}", file=sys.stderr)
            sys.exit(1)
    else:
        html = sys.stdin.read()
    
    if not html.strip():
        print("Error: No HTML content provided", file=sys.stderr)
        sys.exit(1)
    
    # Determine action
    action = 'format'
    if args.minify:
        action = 'minify'
    elif args.validate:
        action = 'validate'
    elif args.stats:
        action = 'stats'
    
    # Execute action
    if action == 'format':
        result = format_html(html, args.indent)
        
        # Save backup if outputting to same file
        if args.output and args.input and args.output == args.input and not args.no_preserve:
            backup_path = args.input + '.backup'
            Path(backup_path).write_text(html, encoding='utf-8')
            print(f"Backup saved: {backup_path}", file=sys.stderr)
        
        if args.output:
            Path(args.output).write_text(result, encoding='utf-8')
            print(f"Formatted HTML saved to: {args.output}")
        else:
            print(result)
    
    elif action == 'minify':
        result = minify_html(html)
        size_before = len(html)
        size_after = len(result)
        savings = ((size_before - size_after) / size_before) * 100
        
        if args.output:
            Path(args.output).write_text(result, encoding='utf-8')
            print(f"Minified HTML saved to: {args.output}")
        else:
            print(result)
        
        print(f"\nSize: {size_before:,} → {size_after:,} bytes ({savings:.1f}% reduction)", 
              file=sys.stderr)
    
    elif action == 'validate':
        issues = validate_html(html)
        if issues:
            print(f"Found {len(issues)} issue(s):", file=sys.stderr)
            for issue in issues:
                print(f"  ⚠️  {issue}")
            sys.exit(1)
        else:
            print("✅ HTML appears valid (basic checks passed)")
    
    elif action == 'stats':
        stats = extract_stats(html)
        print("HTML Document Statistics:")
        print(f"  Total characters:   {stats['total_chars']:,}")
        print(f"  Total lines:        {stats['total_lines']:,}")
        print(f"  Tag count:          {stats['tag_count']:,}")
        print(f"  Text content:       {stats['text_content_size']:,} chars")
        print(f"  Links:              {stats['links']}")
        print(f"  Images:             {stats['images']}")
        print(f"  Scripts:            {stats['scripts']}")
        print(f"  Stylesheets:        {stats['stylesheets']}")
        print(f"  Inline styles:      {stats['inline_styles']}")

if __name__ == '__main__':
    main()
