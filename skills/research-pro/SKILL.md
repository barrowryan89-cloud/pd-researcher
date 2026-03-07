# Research Pro Skill

This skill provides a comprehensive research tool that searches the web, scrapes top results, and returns summarized content.

## Tools

### `research_pro`

**Description:**  
Performs a deep research task: searches for the query, picks top 3 results, scrapes their content, and returns a JSON object with the gathered knowledge.

**Usage:**
```bash
# Ensure you have a virtual environment set up
# python3 -m venv .venv
# .venv/bin/pip install requests beautifulsoup4

.venv/bin/python3 tools/research_pro.py --query "your search query"
```

**Output:**
JSON object containing:
- `query`: The original query
- `results`: Array of objects with `title`, `url`, and `content` (cleaned text)
- `combined_text`: A concatenated string of all scraped text, ready for LLM processing.

## Implementation Details

- **Search:** Uses DuckDuckGo HTML scraping (no API key required) to find top links.
- **Scraping:** Uses `requests` and `BeautifulSoup` to extract main text, removing boilerplate (scripts, nav, etc.).
- **Summary:** Returns raw cleaned text for the AI agent to synthesize.

## Dependencies

Requires `requests` and `beautifulsoup4`.

```bash
pip install requests beautifulsoup4
```
