#!/usr/bin/env python3
"""
Simple Blog Generator
Converts Markdown files to HTML using a template
"""

import sys
import os
import re
import datetime

def md_to_html(md_text):
    """Very basic MD to HTML converter"""
    html = md_text
    
    # Headers
    html = re.sub(r'^# (.*?)$', r'<h1>\1</h1>', html, flags=re.MULTILINE)
    html = re.sub(r'^## (.*?)$', r'<h2>\1</h2>', html, flags=re.MULTILINE)
    html = re.sub(r'^### (.*?)$', r'<h3>\1</h3>', html, flags=re.MULTILINE)
    
    # Bold/Italic
    html = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', html)
    html = re.sub(r'\*(.*?)\*', r'<em>\1</em>', html)
    
    # Links
    html = re.sub(r'\[(.*?)\]\((.*?)\)', r'<a href="\2">\1</a>', html)
    
    # Lists
    html = re.sub(r'^\- (.*?)$', r'<li>\1</li>', html, flags=re.MULTILINE)
    # Wrap lists (simple approximation)
    # This regex needs to be careful not to match too greedily across the whole file
    # A robust solution would line-by-line parse, but for this snippet we'll do a simple pass
    # Ideally, use a real library, but we want zero deps for this script too.
    
    # Code blocks (basic)
    html = re.sub(r'```(.*?)```', r'<pre><code>\1</code></pre>', html, flags=re.DOTALL)
    
    # Paragraphs (simple)
    lines = html.split('\n\n')
    new_lines = []
    for line in lines:
        if not line.strip():
            continue
        if not line.strip().startswith('<'):
            new_lines.append(f'<p>{line.strip()}</p>')
        else:
            new_lines.append(line)
    html = '\n'.join(new_lines)
    
    return html

def generate_blog_post(md_file, template_file, output_dir):
    with open(md_file, 'r') as f:
        content = f.read()
        
    # Parse frontmatter-like metadata or extract from content
    title = "Blog Post"
    date = datetime.date.today().isoformat()
    description = "Learn more about developer tools and productivity."
    
    # Extract H1 as title if present
    h1_match = re.search(r'^# (.*?)$', content, re.MULTILINE)
    if h1_match:
        title = h1_match.group(1)
        # Remove H1 from content since template handles it
        content = content.replace(h1_match.group(0), '')
        
    # Extract description if present
    # (Simple heuristic: first paragraph)
    
    html_content = md_to_html(content)
    
    with open(template_file, 'r') as f:
        template = f.read()
        
    # Use simple replacement to avoid CSS brace conflicts
    final_html = template.replace('{title}', title)
    final_html = final_html.replace('{date}', date)
    final_html = final_html.replace('{description}', description)
    final_html = final_html.replace('{content}', html_content)
    
    filename = os.path.basename(md_file).replace('.md', '.html')
    output_path = os.path.join(output_dir, filename)
    
    with open(output_path, 'w') as f:
        f.write(final_html)
    
    print(f"Generated {output_path}")

def main():
    if len(sys.argv) < 3:
        print("Usage: python3 generate_blog.py <md_file> <output_dir>")
        sys.exit(1)
        
    md_file = sys.argv[1]
    output_dir = sys.argv[2]
    # Adjust path to template as needed based on where script runs
    template_file = os.path.join(os.path.dirname(__file__), "blog_template.html")
    
    if not os.path.exists(template_file):
         # Fallback for current working directory execution
         template_file = "tools/blog_template.html"

    generate_blog_post(md_file, template_file, output_dir)

if __name__ == "__main__":
    main()
