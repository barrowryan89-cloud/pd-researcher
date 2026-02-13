import argparse
import json
import os
import requests
import sys
from bs4 import BeautifulSoup
from urllib.parse import quote_plus

def clean_html(html_content):
    """
    Cleans HTML content to extract readable text.
    Removes scripts, styles, and other non-content elements.
    """
    if not html_content:
        return ""
    
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Remove unwanted tags
    for element in soup(['script', 'style', 'header', 'footer', 'nav', 'iframe', 'noscript', 'svg', 'button', 'input', 'form']):
        element.decompose()
        
    # Get text
    text = soup.get_text(separator=' ')
    
    # Clean up whitespace
    lines = (line.strip() for line in text.splitlines())
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    text = ' '.join(chunk for chunk in chunks if chunk)
    
    return text

def search_10links(query):
    """
    Searches using a simple scraper or API simulation since 10links isn't a standard library.
    We will use a standard search engine scraper approach (DuckDuckGo HTML or similar)
    to get the top links.
    """
    # Using DuckDuckGo HTML version for easier scraping without JS
    url = f"https://html.duckduckgo.com/html/?q={quote_plus(query)}"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        results = []
        
        # DuckDuckGo HTML selectors (subject to change, but usually stableish)
        for link in soup.select('.result__a')[:3]: # Top 3
            title = link.get_text()
            href = link['href']
            # DDG redirects, need to parse if possible, or just use as is if direct
            # usually href is like /l/?kh=-1&uddg=https%3A%2F%2Fexample.com...
            # But simple scraper might just get the redirect url.
            # Let's try to follow or parse.
            
            # Simple approach: just use the href
            results.append({'title': title, 'url': href})
            
        return results
    except Exception as e:
        sys.stderr.write(f"Search failed: {e}\n")
        return []

def scrape_content(url):
    """
    Fetches and cleans content from a URL.
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    try:
        # specific handling for DDG redirect links if necessary, 
        # but requests usually follows redirects.
        # If the URL is relative (from scraping DDG), we need to prepend base
        if url.startswith('//'):
            url = 'https:' + url
        elif url.startswith('/'):
            url = 'https://html.duckduckgo.com' + url
            
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        return clean_html(response.text)
    except Exception as e:
        return f"Error scraping {url}: {e}"

def summarize(query, sources):
    """
    Constructs a simple summary payload. 
    Since this script runs locally without LLM access inside it (unless we call an API),
    we will structure the output for the AGENT to summarize, OR we provide a
    concatenated context.
    
    The prompt asks for a "summarized JSON answer". 
    Without an internal LLM call, "summarizing" logic is limited to extraction or concatenation.
    However, often "tools" pass data back to the Agent.
    
    If the prompt implies the script itself does the intelligent summarization, 
    it might need an API key. 
    
    BUT: The Agent (me) usually does the thinking. 
    The tool just fetches.
    
    Re-reading: "returns a summarized JSON answer".
    
    I will package the scraped data into a clean JSON structure 
    so the calling Agent (or user) can read it easily.
    """
    
    output = {
        "query": query,
        "results": [],
        "combined_text": ""
    }
    
    for source in sources:
        content = scrape_content(source['url'])
        # Limit content length to avoid massive payloads
        truncated_content = content[:4000] 
        
        output["results"].append({
            "title": source['title'],
            "url": source['url'],
            "content": truncated_content
        })
        output["combined_text"] += f"\n--- Source: {source['title']} ---\n{truncated_content}\n"
        
    return output

def main():
    parser = argparse.ArgumentParser(description='Research Pro CLI')
    parser.add_argument('--query', required=True, help='Search query')
    args = parser.parse_args()
    
    print(f"Searching for: {args.query}...", file=sys.stderr)
    links = search_10links(args.query)
    
    if not links:
        print(json.dumps({"error": "No results found"}))
        return

    print(f"Found {len(links)} links. Scraping...", file=sys.stderr)
    final_data = summarize(args.query, links)
    
    print(json.dumps(final_data, indent=2))

if __name__ == "__main__":
    main()
