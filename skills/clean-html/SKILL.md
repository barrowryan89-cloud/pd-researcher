# Clean HTML Skill

## Purpose
This skill provides tools to fetch web pages and convert their content into clean, readable Markdown, stripping out ads, navigation, and footers. It is optimized for RAG (Retrieval-Augmented Generation) agents that need concise text without clutter.

## Tools

### `clean_html`
Fetch a URL and return clean Markdown content.

- **Usage**: `tools/clean_html.py <URL>`
- **Description**: Fetches the HTML from the given URL, removes unwanted elements (ads, navigation, footers, scripts, styles), and converts the main content into Markdown format.
- **Parameters**:
    - `URL`: The full URL of the page to fetch (e.g., `https://example.com`).
- **Output**: Cleaned Markdown text to stdout. Errors are printed to stderr.

## Example

```bash
python3 tools/clean_html.py https://example.com
```

## Notes
- Requires `requests`, `beautifulsoup4`, and `markdownify` Python libraries.
- Recommended to run within a virtual environment:
  ```bash
  python3 -m venv tools/venv
  source tools/venv/bin/activate
  pip install requests beautifulsoup4 markdownify
  python3 tools/clean_html.py <URL>
  ```
- Handles basic cleanup of common ad/popup classes and IDs.
- Returns non-zero exit code on failure.
