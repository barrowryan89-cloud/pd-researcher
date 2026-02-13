#!/usr/bin/env python3
"""
html_extractor.py — Extract text and data from HTML
Tool #39 in the PD Researcher free tools collection
"""

import argparse
import re
import sys
from pathlib import Path
from urllib.parse import urljoin, urlparse
from html.parser import HTMLParser


class HTMLTextExtractor(HTMLParser):
    """Extract text content from HTML."""
    
    def __init__(self):
        super().__init__()
        self.text_parts = []
        self.in_script = False
        self.in_style = False
        
    def handle_starttag(self, tag, attrs):
        if tag in ('script', 'style'):
            self.in_script = True
        elif tag == 'br':
            self.text_parts.append('\n')
        elif tag in ('p', 'div', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'li'):
            self.text_parts.append('\n')
            
    def handle_endtag(self, tag):
        if tag in ('script', 'style'):
            self.in_script = False
        elif tag in ('p', 'div', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'li', 'tr'):
            self.text_parts.append('\n')
            
    def handle_data(self, data):
        if not self.in_script and not self.in_style:
            self.text_parts.append(data)
            
    def get_text(self):
        text = ''.join(self.text_parts)
        # Clean up whitespace
        text = re.sub(r'\n\s*\n', '\n\n', text)
        text = re.sub(r'[ \t]+', ' ', text)
        return text.strip()


def extract_links(html: str, base_url: str = '') -> list:
    """Extract all links from HTML."""
    links = []
    pattern = r'<a[^>]+href=["\']([^"\']+)["\'][^>]*>([^<]*)</a>'
    
    for match in re.finditer(pattern, html, re.IGNORECASE):
        href = match.group(1)
        text = match.group(2).strip()
        
        # Resolve relative URLs
        if base_url:
            href = urljoin(base_url, href)
        
        links.append({
            'url': href,
            'text': text or '[no text]'
        })
    
    return links


def extract_images(html: str, base_url: str = '') -> list:
    """Extract all images from HTML."""
    images = []
    pattern = r'<img[^>]+src=["\']([^"\']+)["\'][^>]*>'
    
    for match in re.finditer(pattern, html, re.IGNORECASE):
        src = match.group(1)
        
        # Get alt text
        alt_match = re.search(r'alt=["\']([^"\']*)["\']', match.group(0), re.IGNORECASE)
        alt = alt_match.group(1) if alt_match else ''
        
        # Resolve relative URLs
        if base_url:
            src = urljoin(base_url, src)
        
        images.append({
            'src': src,
            'alt': alt
        })
    
    return images


def extract_tables(html: str) -> list:
    """Extract tables from HTML as lists of lists."""
    tables = []
    table_pattern = r'<table[^>]*>(.*?)</table>'
    row_pattern = r'<tr[^>]*>(.*?)</tr>'
    cell_pattern = r'<t[dh][^>]*>(.*?)</t[dh]>'
    
    for table_match in re.finditer(table_pattern, html, re.IGNORECASE | re.DOTALL):
        table_html = table_match.group(1)
        table_data = []
        
        for row_match in re.finditer(row_pattern, table_html, re.IGNORECASE | re.DOTALL):
            row_html = row_match.group(1)
            row_data = []
            
            for cell_match in re.finditer(cell_pattern, row_html, re.IGNORECASE | re.DOTALL):
                # Strip HTML tags from cell content
                cell_text = re.sub(r'<[^>]+>', '', cell_match.group(1))
                row_data.append(cell_text.strip())
            
            if row_data:
                table_data.append(row_data)
        
        if table_data:
            tables.append(table_data)
    
    return tables


def extract_title(html: str) -> str:
    """Extract title from HTML."""
    match = re.search(r'<title[^>]*>([^<]*)</title>', html, re.IGNORECASE)
    return match.group(1).strip() if match else ''


def extract_meta(html: str) -> dict:
    """Extract meta tags from HTML."""
    meta = {}
    pattern = r'<meta[^>]+name=["\']([^"\']+)["\'][^>]+content=["\']([^"\']*)["\'][^>]*>'
    
    for match in re.finditer(pattern, html, re.IGNORECASE):
        meta[match.group(1).lower()] = match.group(2)
    
    # Also check for property (OpenGraph)
    og_pattern = r'<meta[^>]+property=["\']([^"\']+)["\'][^>]+content=["\']([^"\']*)["\'][^>]*>'
    for match in re.finditer(og_pattern, html, re.IGNORECASE):
        meta[match.group(1).lower()] = match.group(2)
    
    return meta


def main():
    parser = argparse.ArgumentParser(
        description="Extract text and data from HTML",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s --file page.html --text              # Extract text content
  %(prog)s --file page.html --links             # Extract links
  %(prog)s --file page.html --images            # Extract images
  %(prog)s --file page.html --tables            # Extract tables
  %(prog)s --file page.html --title             # Extract title
  %(prog)s --file page.html --meta              # Extract meta tags
  %(prog)s --file page.html --all               # Extract everything
        """
    )
    
    parser.add_argument('-f', '--file', required=True, help='HTML file to parse')
    parser.add_argument('-u', '--base-url', help='Base URL for resolving relative links')
    parser.add_argument('--text', action='store_true', help='Extract text content')
    parser.add_argument('--links', action='store_true', help='Extract links')
    parser.add_argument('--images', action='store_true', help='Extract images')
    parser.add_argument('--tables', action='store_true', help='Extract tables')
    parser.add_argument('--title', action='store_true', help='Extract page title')
    parser.add_argument('--meta', action='store_true', help='Extract meta tags')
    parser.add_argument('--all', action='store_true', help='Extract everything')
    
    args = parser.parse_args()
    
    try:
        with open(args.file, 'r', encoding='utf-8') as f:
            html = f.read()
    except FileNotFoundError:
        print(f"File not found: {args.file}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error reading file: {e}", file=sys.stderr)
        sys.exit(1)
    
    # If no specific option, default to text
    if not any([args.text, args.links, args.images, args.tables, args.title, args.meta, args.all]):
        args.text = True
    
    if args.all:
        args.text = args.links = args.images = args.tables = args.title = args.meta = True
    
    if args.title:
        title = extract_title(html)
        if title:
            print(f"Title: {title}")
            print()
    
    if args.meta:
        meta = extract_meta(html)
        if meta:
            print("Meta Tags:")
            for key, value in meta.items():
                print(f"  {key}: {value}")
            print()
    
    if args.text:
        extractor = HTMLTextExtractor()
        extractor.feed(html)
        text = extractor.get_text()
        if text:
            print("Text Content:")
            print(text)
            print()
    
    if args.links:
        links = extract_links(html, args.base_url)
        if links:
            print(f"Links ({len(links)} found):")
            for link in links[:50]:  # Limit to 50
                print(f"  {link['url']}")
                if link['text'] != '[no text]':
                    print(f"    Text: {link['text']}")
            if len(links) > 50:
                print(f"  ... and {len(links) - 50} more")
            print()
    
    if args.images:
        images = extract_images(html, args.base_url)
        if images:
            print(f"Images ({len(images)} found):")
            for img in images:
                print(f"  {img['src']}")
                if img['alt']:
                    print(f"    Alt: {img['alt']}")
            print()
    
    if args.tables:
        tables = extract_tables(html)
        if tables:
            print(f"Tables ({len(tables)} found):")
            for i, table in enumerate(tables, 1):
                print(f"\nTable {i}:")
                for row in table:
                    print(f"  {' | '.join(row)}")


if __name__ == '__main__':
    main()
