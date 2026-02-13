#!/usr/bin/env python3
"""
HTML Cleaner - Free Tool
Cleans messy HTML into readable Markdown
Free version: Single URL processing
Paid upgrade: Batch processing, API access, custom rules

Usage: python3 html_cleaner_free.py <url>
"""

import sys
import re
import urllib.request
import urllib.error
from urllib.parse import urlparse

# Simple HTML to Markdown converter (no dependencies)
class SimpleHTMLCleaner:
    def __init__(self):
        self.title = ""
        self.content = []
        
    def fetch(self, url):
        """Fetch HTML from URL"""
        try:
            req = urllib.request.Request(
                url,
                headers={'User-Agent': 'Mozilla/5.0 (compatible; HTMLCleaner/1.0)'}
            )
            with urllib.request.urlopen(req, timeout=30) as response:
                return response.read().decode('utf-8', errors='ignore')
        except Exception as e:
            return f"Error fetching URL: {e}"
    
    def clean_html(self, html):
        """Remove scripts, styles, and clean HTML"""
        # Remove scripts
        html = re.sub(r'<script[^>]*>.*?</script>', '', html, flags=re.DOTALL | re.IGNORECASE)
        # Remove styles
        html = re.sub(r'<style[^>]*>.*?</style>', '', html, flags=re.DOTALL | re.IGNORECASE)
        # Remove nav/footer/header
        html = re.sub(r'<(nav|footer|header|aside)[^>]*>.*?</\1>', '', html, flags=re.DOTALL | re.IGNORECASE)
        # Remove comments
        html = re.sub(r'<!--.*?-->', '', html, flags=re.DOTALL)
        return html
    
    def extract_title(self, html):
        """Extract page title"""
        match = re.search(r'<title[^>]*>(.*?)</title>', html, re.IGNORECASE | re.DOTALL)
        if match:
            return self.clean_text(match.group(1))
        return "Untitled"
    
    def clean_text(self, text):
        """Clean whitespace and entities"""
        text = re.sub(r'\s+', ' ', text)
        text = text.replace('&amp;', '&')
        text = text.replace('&lt;', '<')
        text = text.replace('&gt;', '>')
        text = text.replace('&quot;', '"')
        text = text.replace('&#39;', "'")
        return text.strip()
    
    def html_to_markdown(self, html):
        """Convert HTML to simple Markdown"""
        # Headers
        html = re.sub(r'<h1[^>]*>(.*?)</h1>', r'# \1\n\n', html, flags=re.IGNORECASE | re.DOTALL)
        html = re.sub(r'<h2[^>]*>(.*?)</h2>', r'## \1\n\n', html, flags=re.IGNORECASE | re.DOTALL)
        html = re.sub(r'<h3[^>]*>(.*?)</h3>', r'### \1\n\n', html, flags=re.IGNORECASE | re.DOTALL)
        
        # Bold/Italic
        html = re.sub(r'<(strong|b)[^>]*>(.*?)</\1>', r'**\2**', html, flags=re.IGNORECASE | re.DOTALL)
        html = re.sub(r'<(em|i)[^>]*>(.*?)</\1>', r'*\2*', html, flags=re.IGNORECASE | re.DOTALL)
        
        # Links
        html = re.sub(r'<a[^>]+href="([^"]*)"[^>]*>(.*?)</a>', r'[\2](\1)', html, flags=re.IGNORECASE | re.DOTALL)
        
        # Paragraphs
        html = re.sub(r'<p[^>]*>(.*?)</p>', r'\1\n\n', html, flags=re.IGNORECASE | re.DOTALL)
        
        # Lists
        html = re.sub(r'<li[^>]*>(.*?)</li>', r'- \1\n', html, flags=re.IGNORECASE | re.DOTALL)
        html = re.sub(r'<ul[^>]*>.*?</ul>', lambda m: m.group(0) + '\n', html, flags=re.IGNORECASE | re.DOTALL)
        html = re.sub(r'<ol[^>]*>.*?</ol>', lambda m: m.group(0) + '\n', html, flags=re.IGNORECASE | re.DOTALL)
        
        # Line breaks
        html = re.sub(r'<br\s*/?>', '\n', html, flags=re.IGNORECASE)
        
        # Remove remaining tags
        html = re.sub(r'<[^>]+>', '', html)
        
        # Clean up whitespace
        html = re.sub(r'\n{3,}', '\n\n', html)
        
        return self.clean_text(html)
    
    def process(self, url):
        """Process URL and return Markdown"""
        html = self.fetch(url)
        if html.startswith("Error"):
            return html
        
        self.title = self.extract_title(html)
        cleaned_html = self.clean_html(html)
        markdown = self.html_to_markdown(cleaned_html)
        
        result = f"# {self.title}\n\nSource: {url}\n\n---\n\n{markdown}"
        return result

def print_banner():
    print("""
╔════════════════════════════════════════════════════════════╗
║                    HTML CLEANER v1.0                       ║
║              Free Tool by Sand Street Holdings             ║
╠════════════════════════════════════════════════════════════╣
║  Clean messy HTML into readable Markdown instantly         ║
║                                                            ║
║  💎 Want more power?                                       ║
║     → Batch processing                                     ║
║     → API access                                           ║
║     → Custom cleaning rules                                ║
║     → Check out PD_Researcher v1 ($29)                     ║
║        Solana: FEKY6bDoqBnsQZVT3XbEYS4b1DJ8QoA64G5hXycfTAhQ ║
╚════════════════════════════════════════════════════════════╝
""")

def main():
    print_banner()
    
    if len(sys.argv) < 2:
        print("Usage: python3 html_cleaner_free.py <url>")
        print("\nExample:")
        print("  python3 html_cleaner_free.py https://example.com/article")
        sys.exit(1)
    
    url = sys.argv[1]
    
    # Validate URL
    parsed = urlparse(url)
    if not parsed.scheme or not parsed.netloc:
        print("❌ Invalid URL. Please include http:// or https://")
        sys.exit(1)
    
    print(f"🔄 Fetching: {url}\n")
    
    cleaner = SimpleHTMLCleaner()
    result = cleaner.process(url)
    
    print(result)
    
    print("\n" + "="*60)
    print("✅ Cleaning complete!")
    print("\n💡 Want to process multiple URLs?")
    print("   Upgrade to PD_Researcher v1 for batch processing")
    print("   Pay with crypto: FEKY6bDoqBnsQZVT3XbEYS4b1DJ8QoA64G5hXycfTAhQ")
    print("\n🔒 Privacy Tip:")
    print("   Track your content performance without cookies")
    print("   Try Plausible: https://plausible.io/")
    print("="*60)

if __name__ == "__main__":
    main()
