#!/usr/bin/env python3
"""
Tool #33: Markdown to HTML Converter
Convert Markdown files to HTML with optional CSS styling
"""

import sys
import re
import html


def parse_markdown(text):
    """Simple markdown to HTML parser."""
    # Escape HTML entities first
    text = html.escape(text)
    
    # Code blocks (must be before inline code)
    text = re.sub(r'```(\w+)?\n(.*?)```', r'<pre><code>\2</code></pre>', text, flags=re.DOTALL)
    
    # Headers
    text = re.sub(r'^###### (.*?)$', r'<h6>\1</h6>', text, flags=re.MULTILINE)
    text = re.sub(r'^##### (.*?)$', r'<h5>\1</h5>', text, flags=re.MULTILINE)
    text = re.sub(r'^#### (.*?)$', r'<h4>\1</h4>', text, flags=re.MULTILINE)
    text = re.sub(r'^### (.*?)$', r'<h3>\1</h3>', text, flags=re.MULTILINE)
    text = re.sub(r'^## (.*?)$', r'<h2>\1</h2>', text, flags=re.MULTILINE)
    text = re.sub(r'^# (.*?)$', r'<h1>\1</h1>', text, flags=re.MULTILINE)
    
    # Bold and italic
    text = re.sub(r'\*\*\*(.*?)\*\*\*', r'<strong><em>\1</em></strong>', text)
    text = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', text)
    text = re.sub(r'\*(.*?)\*', r'<em>\1</em>', text)
    text = re.sub(r'___(.*?)___', r'<strong><em>\1</em></strong>', text)
    text = re.sub(r'__(.*?)__', r'<strong>\1</strong>', text)
    text = re.sub(r'_(.*?)_', r'<em>\1</em>', text)
    
    # Inline code
    text = re.sub(r'`([^`]+)`', r'<code>\1</code>', text)
    
    # Links
    text = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2">\1</a>', text)
    
    # Images
    text = re.sub(r'!\[([^\]]*)\]\(([^)]+)\)', r'<img src="\2" alt="\1">', text)
    
    # Blockquotes
    lines = text.split('\n')
    result = []
    in_quote = False
    
    for line in lines:
        if line.startswith('&gt; '):
            if not in_quote:
                result.append('<blockquote>')
                in_quote = True
            result.append(line[5:])
        else:
            if in_quote:
                result.append('</blockquote>')
                in_quote = False
            result.append(line)
    
    if in_quote:
        result.append('</blockquote>')
    
    text = '\n'.join(result)
    
    # Lists
    lines = text.split('\n')
    result = []
    in_list = False
    
    for line in lines:
        list_match = re.match(r'^(\s*)[-*+] (.+)$', line)
        if list_match:
            if not in_list:
                result.append('<ul>')
                in_list = True
            result.append(f'<li>{list_match.group(2)}</li>')
        else:
            if in_list:
                result.append('</ul>')
                in_list = False
            result.append(line)
    
    if in_list:
        result.append('</ul>')
    
    text = '\n'.join(result)
    
    # Paragraphs (wrap non-tag lines)
    lines = text.split('\n')
    result = []
    
    for line in lines:
        stripped = line.strip()
        if stripped and not stripped.startswith('<'):
            result.append(f'<p>{line}</p>')
        else:
            result.append(line)
    
    return '\n'.join(result)


def main():
    if len(sys.argv) < 2 or sys.argv[1] in ('-h', '--help'):
        print("Usage: python3 markdown_to_html_free.py <input.md> [output.html]")
        print("Example: python3 markdown_to_html_free.py README.md README.html")
        sys.exit(0)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else input_file.replace('.md', '.html')
    
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            markdown_text = f.read()
    except Exception as e:
        print(f"Error reading file: {e}")
        sys.exit(1)
    
    html_content = parse_markdown(markdown_text)
    
    full_html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Converted Markdown</title>
    <style>
        body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; max-width: 800px; margin: 40px auto; padding: 0 20px; line-height: 1.6; color: #333; }}
        h1, h2, h3 {{ color: #2c3e50; }}
        code {{ background: #f4f4f4; padding: 2px 6px; border-radius: 3px; font-family: 'Courier New', monospace; }}
        pre {{ background: #f4f4f4; padding: 16px; overflow-x: auto; border-radius: 5px; }}
        pre code {{ background: none; padding: 0; }}
        blockquote {{ border-left: 4px solid #ddd; padding-left: 16px; margin-left: 0; color: #666; }}
        a {{ color: #3498db; }}
        ul {{ padding-left: 20px; }}
    </style>
</head>
<body>
{html_content}
</body>
</html>"""
    
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(full_html)
        print(f"✓ Converted: {input_file} → {output_file}")
    except Exception as e:
        print(f"Error writing file: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()

    # Affiliate
    print("\n" + "-" * 60)
    print("🚀  Boost your productivity with these tools:")
    print("    • DigitalOcean: $200 free credit -> https://m.do.co/c/pdresearcher")
    print("    • JetBrains IDEs: The best Python tools -> https://www.jetbrains.com/?utm_source=pdresearcher")
    print("-" * 60)
