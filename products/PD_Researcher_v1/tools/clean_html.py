#!/usr/bin/env python3
import sys
import requests
from bs4 import BeautifulSoup
from markdownify import markdownify as md

def clean_html(url):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching URL: {e}", file=sys.stderr)
        return None

    soup = BeautifulSoup(response.content, 'html.parser')

    # Remove unwanted tags
    for tag in soup(["script", "style", "nav", "footer", "header", "aside", "iframe", "noscript", "meta", "link"]):
        tag.decompose()
    
    # Remove elements by class/id commonly associated with ads/popups
    unwanted_classes = ['ad', 'ads', 'advertisement', 'popup', 'cookie-consent', 'newsletter-signup', 'social-share']
    for element in soup.find_all(class_=lambda x: x and any(cls in x for cls in unwanted_classes)):
        element.decompose()
        
    for element in soup.find_all(id=lambda x: x and any(cls in x for cls in unwanted_classes)):
        element.decompose()


    # Remove elements with only '×' or similar close button text
    for element in soup.find_all(string=lambda text: text and text.strip() in ['×', '&times;', '✕']):
        parent = element.parent
        if parent and parent.name in ['button', 'a', 'span', 'div']:
            parent.decompose()
            
    # Remove empty links or links with just '#'
    for a in soup.find_all('a', href=True):
        if not a.get_text(strip=True) or a['href'] == '#':
            a.decompose()

    # Get the cleaned HTML
    cleaned_html = str(soup)

    # Convert to Markdown
    markdown_text = md(cleaned_html, heading_style="ATX")
    
    # Basic cleanup of excessive newlines
    markdown_text = '\n'.join([line.strip() for line in markdown_text.splitlines() if line.strip()])

    return markdown_text

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 clean_html.py <URL>", file=sys.stderr)
        sys.exit(1)

    url = sys.argv[1]
    result = clean_html(url)
    
    if result:
        print(result)
    else:
        sys.exit(1)
